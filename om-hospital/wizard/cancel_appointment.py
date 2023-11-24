from datetime import datetime, date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment",
                                     domain=[('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string="Reason")
    cancel_date = fields.Date(string="Date Cancel", default=datetime.today())

    def action_cancel_wizard(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om-hospital.cancel_days')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if cancel_day != 0 and allowed_date < date.today():
            raise ValidationError(_("Cancellation Not allowed for this Appointment"))
        self.appointment_id.state = 'cancelled'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.appointment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id
        }

