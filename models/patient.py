from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
from dateutil import relativedelta
import base64
from odoo.modules.module import get_module_resource


class HospitalPatient(models.Model):
    _name = 'hospitalme.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

# ==================
# Fields
# ==================
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True
    )
    code = fields.Char(default="PAT000", readonly=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    date_of_birth = fields.Date(string="Date Of Birth")
    mobile = fields.Char(
        string="Mobile",
        tracking=True,
        help="Enter the patient's mobile number."
    )
    age = fields.Integer(
        string="Age", compute="compute_calculate_age", store=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string="Gender",
        tracking=True,
    )
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', required='1',
                               string="State", domain="[('country_id' , '='  , country_id)]")

    national_id_number = fields.Char(string="National ID", required='1')

    doctor_id = fields.Many2one('hospitalme.doctor', string='Doctor')

    insurance_policy_number = fields.Char(string='Insurance Policy Number')
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string='Blood Type')
    # This method is used to get the default image for the patient

    def _get_default_image(self):
        image_path = get_module_resource(
            'celiopatra_system', 'static/img', 'default_image.png')
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read())

    image_1920 = fields.Binary(
        string="Image",
        attachment=True,
        default=lambda self: self._get_default_image(),
        help="This field holds the image used as patient profile picture, limited to 1024x1024px."
    )

# ==================
# Constraints
# ==================
    _sql_constraints = [
        (
            'national_id_number_check',
            "CHECK (national_id_number ~ '^[23][0-9]{13}$')",
            "National ID must be exactly 14 digits long, contain only numbers, and start with 2 or 3."
        ),
        (
            'national_id_number_unique',
            "unique(national_id_number)",
            "National ID Already Exist."
        ),
    ]

    # @api.constrains('mobile')
    # def _check_mobile(self):
    #     pattern = r'^(02\s)?01[0125]\d{8}$'
    #     for rec in self:
    #         if rec.mobile and not re.match(pattern, rec.mobile):
    #             raise ValidationError(
    #                 "Mobile number is not valid. It should be like '01114189522' or '02 01114189522'.")

    # national_id_number validation
    # @api.constrains('national_id_number')
    # def _national_id_constrains(self):
    #     allowed_prefix  = ['2' , '3']
    #     if self.national_id_number:
    #         if len(self.national_id_number) != 14 or not self.national_id_number.isdigit():
    #              raise ValidationError(_("National ID must be exactly 14 digits long and contain only numbers."))
    #         if self.national_id_number[0] not in allowed_prefix:
    #             raise ValidationError(_("National ID must Start With 2 Or 3."))


# ==================
# Business Logic
# ==================

# claculate age according to the date of birth

    @api.depends('date_of_birth')
    def compute_calculate_age(self):
        for rec in self:
            if rec.date_of_birth:
                date_today = fields.Date.today()  # from Odoo
                age = relativedelta.relativedelta(
                    date_today, rec.date_of_birth).years
                rec.age = age
            else:
                rec.age = 0


# restrict states according to the selected country

    @api.onchange('country_id')
    def _restrict_states(self):
        if self.country_id:
            print("="*50)
            print("self.country.id", self.country_id.id)
            print("self.country_name", self.country_id.name)
            print("self.country_code", self.country_id.code)
            print("self.state_id", self.state_id)
            print("="*50)

    # ensure code is unique and follows the format
    @api.model
    def copy(self, default=None):
        default = dict(default or {})
        default['code'] = self.env['ir.sequence'].next_by_code(
            'patient.sequence') or 'PAT-UNKNOWN'
        return super(HospitalPatient, self).copy(default)

# To assign the sequence to the `code` field when a record is created
    @api.model
    def create(self, vals):
        res = super(HospitalPatient, self).create(vals)
        # If the code is not provided, generate it using the sequence
        if res.code == 'PAT000':
            res.code = self.env['ir.sequence'].next_by_code('patient.sequence')

        return res

    def update_refs(self):
        for record in self.env['hospitalme.patient'].search([('code', '=', 'PAT-000')]):
            record.code = self.env['ir.sequence'].next_by_code(
                'patient.sequence') or 'PAT-UNKNOWN'
