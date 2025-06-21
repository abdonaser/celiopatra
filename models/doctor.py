from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import re
import base64
from odoo.modules.module import get_module_resource


class HospitalDoctor(models.Model):
    _name = 'hospitalme.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name asc'

# Fields
    code = fields.Char(default="DOC000", readonly=True)
    name = fields.Char(string='Name', )
    specialization = fields.Char(string="Specialization", )
    patient_ids = fields.One2many(
        'hospitalme.patientclient',
        'doctor_id',
        string='Patients'
    )
    license_number = fields.Char(
        string='License Number', tracking=True)
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state',
                               string="State", domain="[('country_id', '=', country_id)]")

    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")

    available_from = fields.Datetime(string="Available From", )
    available_to = fields.Datetime(string="Available To", )
    is_available = fields.Boolean(
        string="Currently Available", compute="_compute_is_available", store=True)

    department_id = fields.Many2one(
        'hospitalme.department', string='Department', tracking=True)

    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True
    )

    image_1920 = fields.Binary(
        string="Image",
        attachment=True,
        help="This field holds the image used as doctor profile picture, limited to 1024x1024px."
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string="Gender"
    )

# Constraints
    # _sql_constraints = [
    #     ('email_unique', 'unique(email)', 'Email must be unique.')
    # ]

    # @api.constrains('mobile')
    # def _check_mobile(self):
    #     pattern = r'^(02\s)?01[0125]\d{8}$'
    #     for rec in self:
    #         if rec.mobile and not re.match(pattern, rec.mobile):
    #             raise ValidationError(
    #                 "Mobile number is not valid. It should be like '01114189522' or '02 01114189522'.")


# Business Logic


    @api.depends('available_from', 'available_to')
    def _compute_is_available(self):
        now = fields.Datetime.now()
        for rec in self:
            if rec.available_from and rec.available_to:
                rec.is_available = rec.available_from <= now < rec.available_to
            else:
                rec.is_available = False

    # Get default image from static folder

    def _get_default_image(self, image_name):
        image_path = get_module_resource(
            'celiopatra_system', 'static/img', image_name)
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read())

    # ensure code is unique and follows the format
    @api.model
    def copy(self, default=None):
        default = dict(default or {})
        default['code'] = self.env['ir.sequence'].next_by_code(
            'doctor.sequence') or 'DOC-UNKNOWN'
        return super(HospitalDoctor, self).copy(default)

    # Create override
    @api.model
    def create(self, vals):
        # Auto assign code
        if vals.get('code', 'DOC000') == 'DOC000':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'doctor.sequence') or 'DOC-UNKNOWN'

        # Set default gender image
        if not vals.get('image_1920'):
            gender = vals.get('gender')
            if gender == 'male':
                image_name = "doctor_male_character.jpeg"
            elif gender == 'female':
                image_name = "doctor_femal_character.jpeg"
            else:
                image_name = "default_image.png"

            vals['image_1920'] = self._get_default_image(image_name)

        return super(HospitalDoctor, self).create(vals)

    # Fix records with old code manually (optional tool)
    def update_refs(self):
        for record in self.env['hospitalme.doctor'].search([('code', '=', 'DOC000')]):
            record.code = self.env['ir.sequence'].next_by_code(
                'doctor.sequence') or 'DOC-UNKNOWN'
