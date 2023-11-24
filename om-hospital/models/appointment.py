# -*- coding: utf-8 -*-
import random
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete="cascade", tracking=1)
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today, tracking=True)
    ref = fields.Char(string="Reference", help="The Reference Of the Patient")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')],
                                'Priority',
                                )
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'), ('cancelled', 'Cancelled')], default="draft", string="Status")
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=10)
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines',
                                         'appointment_id', string="Pharmacy Lines")
    hide_price = fields.Boolean(string="Hide Price")
    operation_id = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer("Progress", compute='_compute_progress')
    duration = fields.Float(digits=(6, 2), help="Durations Od Appointment", tracking=25)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related="company_id.currency_id")
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.depends('pharmacy_lines_ids.price_subtotal')
    def _compute_total(self):
        for rec in self:
            total = sum(line.price_subtotal for line in rec.pharmacy_lines_ids)
            rec.total = total

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("you can delete appointment in draft state only"))

    def button_notification(self):
        action = self.env.ref('om-hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Click to Open the patient record'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient',
                }],
                'sticky': False,
            }
        }

    def action_redirect(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https:/www.odoo.com'
        }

    def send_whatsapp(self):
        message = 'Hi %s Your Appointment is %s' % (self.patient_id.name, self.ref)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, message)
        self.message_post(body=message, subject='Whatsapp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successful',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        action = self.env.ref('om-hospital.cancel_appointment_action').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related="product_id.list_price", digits="Product Price")
    qty = fields.Integer(string="Quantity", default="1")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    currency_id = fields.Many2one('res.currency', related="appointment_id.currency_id")
    price_subtotal = fields.Monetary(string="Sub Total", compute='_compute_price_sub_total',
                                     currency_field='currency_id')

    @api.depends('price_unit', 'qty')
    def _compute_price_sub_total(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
