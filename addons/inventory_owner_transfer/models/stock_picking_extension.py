from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPickingExtension(models.Model):
    _inherit = 'stock.picking'

    new_owner_id = fields.Many2one('res.partner', string='New Owner')

    picking_type_code = fields.Selection(
        related='picking_type_id.code',
        string='Picking Type Code',
        readonly=True,
        store=True,
    )


    def button_validate(self):
        # Save the initial owners before the transfer is done
        initial_owners = {line: line.owner_id for line in self.move_line_ids}
        res = super(StockPickingExtension, self).button_validate()
        if res and self.picking_type_id.code == 'internal' and self.new_owner_id:
            for line in self.move_line_ids.filtered(lambda l: l.qty_done > 0):
                # Log the ownership transfer
                self.env['stock.ownership.transfer.log'].create({
                    'previous_owner_id': initial_owners[line].id,
                    'new_owner_id': self.new_owner_id.id,
                    'transferred_quantity': line.qty_done,
                    'product_id': line.product_id.id,
                    'transfer_time': fields.Datetime.now(),
                })
                # Change the owner of the quant
                quants = self.env['stock.quant'].search([
                    ('location_id', '=', line.location_id.id),
                    ('lot_id', '=', line.lot_id.id),
                    ('product_id', '=', line.product_id.id)
                ])
                if not quants:
                    raise UserError("No quants found for the product to transfer.")
                quants.write({'owner_id': self.new_owner_id.id})
        return res
