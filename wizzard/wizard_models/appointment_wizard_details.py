from odoo import models, fields, api, _


class AppointmentWizardDetails(models.TransientModel):
    _name = 'hospitalme.appointment.wizard.details'
    _description = 'Appointment Wizard Details'

    doctor_id =fields.Char(string='Current Doctor', readonly=True)

    appointment = fields.Many2one('hospitalme.appointment', string='Current Appointment', readonly=True)

# compute the old doctor name by default_get method that retrieves the current appointment's doctor
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            appointment = self.env['hospitalme.appointment'].browse(active_id)
            if appointment.exists():
                res['appointment'] = appointment.id
                res['doctor_id'] = appointment.doctor_id.name
        return res

    def show_doctor_details(self):
        action = self.env['ir.actions.actions']._for_xml_id(
            'celiopatra_system.all_doctors_action')
        # Get doctor form view ID
        view_id = self.env.ref('celiopatra_system.doctor_view_form').id
        action['res_id'] = self.appointment.doctor_id.id  # Open specific doctor record
        action['views'] = [(view_id, 'form')]  # Show in form view
        return action

    def show_patient_details(self):
        action = self.env['ir.actions.actions']._for_xml_id(
            'celiopatra_system.patientclient_action')
        # Get patient form view ID
        view_id = self.env.ref('celiopatra_system.patientclient_view_form').id
        action['res_id'] = self.appointment.patient_id.id  # Open specific doctor record
        action['views'] = [(view_id, 'form')]  # Show in form view
        return action



    def print_appointment_report(self):
            self.ensure_one()
            return self.env.ref('celiopatra_system.appointment_report').report_action(self.appointment)