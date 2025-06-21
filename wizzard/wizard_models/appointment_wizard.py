from odoo import models, fields, api, _


class AppointmentWizard(models.TransientModel):
    _name = 'hospitalme.appointment.wizard'
    _description = 'Appointment Wizard'

    new_doctor_id = fields.Many2one('hospitalme.doctor', string='New Doctor')
    department_id = fields.Char(string='Current Department', readonly=True)
    old_doctor = fields.Char(string='Current Doctor', readonly=True)

# compute the old doctor name by default_get method that retrieves the current appointment's doctor
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        print("=" * 50)
        print("Default Get Triggered - active_id:", active_id)
        print("=" * 50)

        if active_id:
            appointment = self.env['hospitalme.appointment'].browse(active_id)
            if appointment.exists():
                res['old_doctor'] = appointment.doctor_id.name
                res['department_id'] = appointment.department_id.name
        return res

    def change_doctor_action(self):
        active_id = self.env.context.get('active_id')
        appointment = self.env['hospitalme.appointment'].browse(active_id)
        if appointment.exists():
            previous_doctor = appointment.doctor_id.name
            appointment.doctor_id = self.new_doctor_id.id
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                        'message': _('Doctor has been changed from %s to %s') % (
                            previous_doctor, self.new_doctor_id.name),
                        'sticky': False,
                }
            }
