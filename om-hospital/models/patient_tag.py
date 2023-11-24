from odoo import models, fields, api, _


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True, copy=False)
    color = fields.Char(string="Color")
    color_2 = fields.Integer(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)") % self.name
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_name', 'unique(name)', "the name must be unique"),
        ('check_sequence', 'check(sequence > 0)', "the sequence must be greater than 0")
    ]
