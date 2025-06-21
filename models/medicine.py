from odoo import models, fields, api, _


class Medicine(models.Model):
    _name = 'hospitalme.medicine'
    _description = 'Hospital Medicine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
# Fields
    code = fields.Char(default="MED000", readonly=True)
    name = fields.Char(string='Medicine Name', tracking=True)
    expiration_date = fields.Date(string='Date Expiration', tracking=True)
    description = fields.Text(string='Description',
                              default='No description provided', tracking=True)
    price = fields.Float(string='Price', digits=(12, 2), tracking=True)
    active = fields.Boolean(string='Active', default=True)
# constraints & Validations


# Business Logic


    @api.model
    def create(self, vals):
        # Auto assign code
        if vals.get('code', 'MED000') == 'MED000':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'medicine.sequence') or 'MED-UNKNOWN'
        result = super(Medicine, self).create(vals)
        return result

    # ensure code is unique and follows the format
    @api.model
    def copy(self, default=None):
        default = dict(default or {})
        default['code'] = self.env['ir.sequence'].next_by_code(
            'medicine.sequence') or 'MED-UNKNOWN'
        return super(Medicine, self).copy(default)


class MedicineLine(models.Model):
    _name = 'hospitalme.medicine.line'
    _description = 'Hospital Medicine Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

# Fields
    medicine_id = fields.Many2one(
        'hospitalme.medicine', string='Medicine', tracking=True)
    quantity = fields.Float(string='Quantity', digits=(
        12, 2), tracking=True)
    doze_per_day = fields.Float(string='Doze Per Day', digits=(
        12, 2), tracking=True)

    appointment_id = fields.Many2one(
        'hospitalme.appointment', string='Appointment', tracking=True)
    doctor = fields.Char(
        string='Doctor', related='appointment_id.doctor_id.name', store=True, tracking=True)
    patient = fields.Char(
        string='Patient', related='appointment_id.patient_id.name', store=True, tracking=True)
# constraints & Validations

# Business Logic
