from odoo import api, models, fields, api, _


class Appointment(models.Model):
    _name = 'hospitalme.appointment'
    _description = 'Appointment'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

# Fields
    code = fields.Char(default="APP000", readonly=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    date = fields.Date(string='Date')
    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('scheduled', 'Scheduled'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string="State",
        required=True,
        default='draft',
        tracking=True,
        help="The state of the appointment. "
             "Draft: Initial state, Scheduled: Appointment is scheduled, "
             "In Progress: Appointment is ongoing, Done: Appointment completed, "
             "Cancelled: Appointment was cancelled."
    )
    department_id = fields.Many2one(
        'hospitalme.department', string="Department Name", required=True)
    patient_id = fields.Many2one(
        "hospitalme.patientclient", string="Patient", required=True)
    doctor_id = fields.Many2one(
        "hospitalme.doctor", string="Doctor", required=True)
    medicine_line_ids = fields.One2many(
        "hospitalme.medicine.line", "appointment_id", string="Medicine Lines")
    symptoms = fields.Text(string="Symptoms")
    isDoctor = fields.Boolean(compute='_compute_isDoctor', store=False)

    appointment_fees = fields.Float(string="Appointment Fees")
    x_ray_fees = fields.Float(string="x-Ray Fees")
    chair_fees = fields.Float(string="Chair Fees")
    total_price = fields.Float(
        string="Total Price", compute="_compute_total_price", store=True)
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True
    )
# Business Logic

    @api.depends()
    def _compute_isDoctor(self):
        for rec in self:
            rec.isDoctor = not self.env.user.has_group(
                'celiopatra_system.doctor_hospital_group')

    @api.depends("appointment_fees", 'x_ray_fees', "chair_fees")
    def _compute_total_price(self):
        for appointment in self:
            appointment.total_price = appointment.appointment_fees + \
                appointment.x_ray_fees + appointment.chair_fees

    # Create override
    @api.model
    def create(self, vals):
        # Auto assign code
        if vals.get('code', 'APP000') == 'APP000':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'appointment.sequence') or 'APP-UNKNOWN'
        result = super(Appointment, self).create(vals)
        # ✅ Add follower only if not already present
        partner = self.env.user.partner_id
        if partner.id not in result.message_partner_ids.ids:
            result.message_subscribe([partner.id])

        return result

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.doctor_id = False

    # ensure code is unique and follows the format

    @api.model
    def copy(self, default=None):
        default = dict(default or {})
        default['code'] = self.env['ir.sequence'].next_by_code(
            'appointment.sequence') or 'APP-UNKNOWN'
        return super(Appointment, self).copy(default)

    def action_open_related_doctor(self):
        action = self.env['ir.actions.actions']._for_xml_id(
            'celiopatra_system.all_doctors_action')  # Load action
        # Get doctor form view ID
        view_id = self.env.ref('celiopatra_system.doctor_view_form').id

        action['res_id'] = self.doctor_id.id  # Open specific doctor record
        action['views'] = [(view_id, 'form')]  # Show in form view
        return action

    def set_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def set_to_scheduled(self):
        for rec in self:
            rec.state = 'scheduled'

    def set_to_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def set_to_done(self):
        for rec in self:
            rec.state = 'done'

    def set_to_cancelled(self):
        for rec in self:
            rec.state = 'cancelled'
