# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'sequence': -100,
    'application': True,
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """Hospital Management System""",

    'author': "Abdo Ahmed",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hospital',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'wizard/cancel_appointment.xml',
        'views/menu.xml',
        'views/views.xml',
        'views/patient_tag.xml',
        'views/female_patient_view.xml',
        'views/appointment_patient.xml',
        'views/res_config_settings_views.xml',
        'views/operation.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
                'data/patient_tag_data.xml',
    ],
}
