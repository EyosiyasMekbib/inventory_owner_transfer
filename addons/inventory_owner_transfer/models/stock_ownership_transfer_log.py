from odoo import models, fields

class StockOwnershipTransferLog(models.Model):
    _name = 'stock.ownership.transfer.log'
    _description = 'Stock Ownership Transfer Log'

    previous_owner_id = fields.Many2one('res.partner', string='Previous Owner', required=True)
    new_owner_id = fields.Many2one('res.partner', string='New Owner', required=True)
    transferred_quantity = fields.Float(string='Transferred Quantity')
    product_id = fields.Many2one('product.product', string='Product')
    transfer_time = fields.Datetime(string='Transfer Time')
