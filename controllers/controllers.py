# -*- coding: utf-8 -*-
from odoo import http

# class Hoteltrivago(http.Controller):
#     @http.route('/hoteltrivago/hoteltrivago/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hoteltrivago/hoteltrivago/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hoteltrivago.listing', {
#             'root': '/hoteltrivago/hoteltrivago',
#             'objects': http.request.env['hoteltrivago.hoteltrivago'].search([]),
#         })

#     @http.route('/hoteltrivago/hoteltrivago/objects/<model("hoteltrivago.hoteltrivago"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hoteltrivago.object', {
#             'object': obj
#         })