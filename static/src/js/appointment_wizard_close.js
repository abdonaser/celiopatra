odoo.define('hospitalme.appointment_wizard_close', function (require) {
    "use strict";

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');

    const AppointmentWizardClose = AbstractAction.extend({
        start: function () {
            const title = this.options.params?.title || "Success";
            const message = this.options.params?.message || "Doctor changed successfully.";

            // Show notification
            this.do_notify(title, message);

            // Close wizard
            this.do_action({ type: 'ir.actions.act_window_close' });
        },
    });

    core.action_registry.add('appointment_wizard_close_action', AppointmentWizardClose);

    return AppointmentWizardClose;
});
