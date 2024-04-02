# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryOwnerTransfer(http.Controller):
#     @http.route('/inventory_owner_transfer/inventory_owner_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_owner_transfer/inventory_owner_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_owner_transfer.listing', {
#             'root': '/inventory_owner_transfer/inventory_owner_transfer',
#             'objects': http.request.env['inventory_owner_transfer.inventory_owner_transfer'].search([]),
#         })

#     @http.route('/inventory_owner_transfer/inventory_owner_transfer/objects/<model("inventory_owner_transfer.inventory_owner_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_owner_transfer.object', {
#             'object': obj
#         })
