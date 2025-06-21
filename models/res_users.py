from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender'
    )
    doctor_id = fields.Many2one(
        'hospitalme.doctor',
        string='Doctor',
        help='Doctor associated with this user. This field is used to link the user to a doctor profile in the hospital management system.'
    )
