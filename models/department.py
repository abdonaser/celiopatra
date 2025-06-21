from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import base64


class HospitalDepartment(models.Model):
    _name = 'hospitalme.department'
    _description = 'Hospital Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name asc'

# ==============================
# Fields
# ==============================
    code = fields.Char(default="DEP000", readonly=True)
    name = fields.Char(string='Department Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    responsible_doctor_id = fields.Many2one(
        'hospitalme.doctor',
        string='Responsible Doctor',
        required=True,
        tracking=True
    )
    image_1920 = fields.Image(
        compute='_compute_responsible_doctor_image', readonly=True, string="Doctor Image")

    doctor_ids = fields.One2many(
        'hospitalme.doctor', 'department_id', string='Doctors')

    # number of doctors in the department
    doctors_num = fields.Integer(
        compute='_compute_doctors_num', string='Number of Doctors', readonly=True, store=True)

    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True
    )

# ==============================
# Compute methods
# ==============================

    def _get_default_image(self, image_name):
        image_path = get_module_resource(
            'celiopatra_system', 'static/img', image_name)
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read())

    @api.depends('responsible_doctor_id')
    def _compute_responsible_doctor_image(self):
        for rec in self:
            if rec.responsible_doctor_id and rec.responsible_doctor_id.image_1920:
                rec.image_1920 = rec.responsible_doctor_id.image_1920
            else:
                # Set default image based On Gender
                if not rec.image_1920:
                    gender = rec.responsible_doctor_id.gender
                    if gender == 'male':
                        image_name = "doctor_male_character.jpeg"
                    elif gender == 'female':
                        image_name = "doctor_femal_character.jpeg"
                    else:
                        image_name = "default_image.png"
                    rec.image_1920 = self._get_default_image(image_name)

    @api.depends('doctor_ids')
    def _compute_doctors_num(self):
        for rec in self:
            rec.doctors_num = len(rec.doctor_ids)


# ==============================
# Constraints and validations
# ==============================

    # This method checks if the responsible doctor is assigned to the department

    @api.constrains('responsible_doctor_id')
    def _check_responsible_doctor(self):
        for rec in self:
            if not rec.responsible_doctor_id:
                raise ValidationError(
                    "A responsible doctor must be assigned to the department.")

    # department name cannot be empty or whitespace
    @api.constrains('name')
    def _check_name_validity(self):
        for rec in self:
            if not rec.name.strip():
                raise ValidationError(
                    "Department name cannot be empty or whitespace.")

# ==============================
# CRUD Operations & Overrides & Business Logic
# ==============================
    # ensure code is unique and follows the format
    @api.model
    def copy(self, default=None):
        default = dict(default or {})
        default['code'] = self.env['ir.sequence'].next_by_code(
            'department.sequence') or 'DEP-UNKNOWN'
        return super(HospitalDepartment, self).copy(default)

    # Create override
    @api.model
    def create(self, vals):
        # Auto assign code
        if vals.get('code', 'DEP000') == 'DEP000':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'department.sequence') or 'DEP-UNKNOWN'
        res = super(HospitalDepartment, self).create(vals)
        return res

    # Fix records with old code manually (optional tool)
    def update_refs(self):
        for record in self.env['hospitalme.department'].search([('code', '=', 'DEP000')]):
            record.code = self.env['ir.sequence'].next_by_code(
                'department.sequence') or 'DEP-UNKNOWN'
