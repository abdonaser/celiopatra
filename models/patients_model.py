from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil import relativedelta
import base64
from odoo.modules.module import get_module_resource


class HospitalPatientClient(models.Model):
    _name = 'hospitalme.patientclient'
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
    state_id = fields.Many2one(
        'res.country.state',
        string="State",
        domain="[('country_id', '=', country_id)]"
    )
    national_id_number = fields.Char(string="National ID")

    doctor_id = fields.Many2one('hospitalme.doctor', string='Doctor')

    insurance_policy_number = fields.Char(string='Insurance Policy Number')
    blood_type = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-'),
    ], string='Blood Type')

    image_1920 = fields.Binary(
        string="Image",
        attachment=True,
        help="This field holds the image used as patient profile picture, limited to 1024x1024px."
    )

    # ==================
    # Constraints
    # ==================
    # _sql_constraints = [
    #     (
    #         'national_id_number_check',
    #         "CHECK (national_id_number ~ '^[23][0-9]{13}$')",
    #         "National ID must be exactly 14 digits long, contain only numbers, and start with 2 or 3."
    #     ),
    #     (
    #         'national_id_number_unique',
    #         "unique(national_id_number)",
    #         "National ID Already Exist."
    #     ),
    # ]

    # ==================
    # Business Logic
    # ==================
    def test_createdBy(self):
        print("="*50)
        for rec in self:
            print(f"Created By: {rec.create_uid.name} (ID: {rec.create_uid.id})")
        print("="*50)

    # Age Calculation
    @api.depends('date_of_birth')
    def compute_calculate_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = fields.Date.today()
                rec.age = relativedelta.relativedelta(
                    today, rec.date_of_birth).years
            else:
                rec.age = 0

    # Get default image from static folder
    def _get_default_image(self, image_name):
        image_path = get_module_resource(
            'celiopatra_system', 'static/img', image_name)
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read())

    # Create override
    @api.model
    def create(self, vals):
        if 'created_by' not in vals:
            vals['created_by'] = self.env.uid
        # Auto assign code
        if vals.get('code', 'PAT000') == 'PAT000':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'patient.sequence') or 'PAT-UNKNOWN'

        # Set default gender image
        if not vals.get('image_1920'):
            gender = vals.get('gender')
            if gender == 'male':
                image_name = "patient_male_character.png"
            elif gender == 'female':
                image_name = "patient_female_character.jpeg"
            else:
                image_name = "default_image.png"

            vals['image_1920'] = self._get_default_image(image_name)

        return super(HospitalPatientClient, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})

        # Old value
        old_gender = self.gender

        # Get new gender value: use the one passed in default, or fallback to old
        new_gender = default.get('gender', self.gender)

        print("=" * 60)
        print("Old Gender:", old_gender)
        print("New Gender:", new_gender)
        print("=" * 60)

        return super(HospitalPatientClient, self).copy(default)

    # Optional: onchange to update image in form view
    # @api.onchange('gender')
    # def _onchange_gender(self):
    #     for rec in self:
    #         if not rec.image_1920:
    #             if rec.gender == 'male':
    #                 image_name = "patient_male_character.png"
    #             elif rec.gender == 'female':
    #                 image_name = "patient_female_character.jpeg"
    #             else:
    #                 image_name = "default_image.png"

    #             rec.image_1920 = self._get_default_image(image_name)
    # @api.onchange('gender')
    # def _onchange_gender(self):
    #     for rec in self:
    #         rec.image_1920 =False