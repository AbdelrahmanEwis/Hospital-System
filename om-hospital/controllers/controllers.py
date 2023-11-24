# -*- coding: utf-8 -*-
# from odoo import http


# class Om-hospital(http.Controller):
#     @http.route('/om-hospital/om-hospital/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om-hospital/om-hospital/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('om-hospital.listing', {
#             'root': '/om-hospital/om-hospital',
#             'objects': http.request.env['om-hospital.om-hospital'].search([]),
#         })

#     @http.route('/om-hospital/om-hospital/objects/<model("om-hospital.om-hospital"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om-hospital.object', {
#             'object': obj
#         })
