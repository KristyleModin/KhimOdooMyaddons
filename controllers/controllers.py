# -*- coding: utf-8 -*-
# from odoo import http


# class Myaddons/hotel(http.Controller):
#     @http.route('/myaddons/hotel/myaddons/hotel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/myaddons/hotel/myaddons/hotel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('myaddons/hotel.listing', {
#             'root': '/myaddons/hotel/myaddons/hotel',
#             'objects': http.request.env['myaddons/hotel.myaddons/hotel'].search([]),
#         })

#     @http.route('/myaddons/hotel/myaddons/hotel/objects/<model("myaddons/hotel.myaddons/hotel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('myaddons/hotel.object', {
#             'object': obj
#         })

