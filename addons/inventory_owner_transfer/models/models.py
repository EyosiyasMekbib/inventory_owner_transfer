from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class StockPickingExtension(models.Model):
    _inherit = 'stock.picking'

    new_owner_id = fields.Many2one('res.partner', string='New Owner', help='The new owner of the goods after the transfer.')

    def button_validate(self):
        res = super(StockPickingExtension, self).button_validate()
        if self.picking_type_id.code == 'internal' and self.new_owner_id:
            for move in self.move_lines.filtered(lambda m: m.state == 'done'):
                # Determine the previous owner. If not explicitly set, use the current owner as the previous owner.
                previous_owner_id = move.restrict_partner_id.id if move.restrict_partner_id else self.env['stock.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_id.id)
                ], limit=1).owner_id.id
                
                # Check if there's a change in ownership before proceeding.
                if previous_owner_id != self.new_owner_id.id:
                    # Update the owner on the stock move and its related stock move lines.
                    move.write({'restrict_partner_id': self.new_owner_id.id})
                    move.move_line_ids.write({'owner_id': self.new_owner_id.id})

                    # Log the ownership transfer.
                    transfer_log_vals = {
                        'previous_owner_id': previous_owner_id,
                        'new_owner_id': self.new_owner_id.id,
                        'transfer_quantity': sum(move.move_line_ids.mapped('qty_done')),
                        'transfer_date': fields.Date.context_today(self),
                        'stock_move_id': move.id,
                        'picking_id': self.id,
                    }
                    self.env['stock.ownership.transfer.log'].create(transfer_log_vals)

        return res

    @api.constrains('new_owner_id')
    def _check_new_owner_id(self):
        if self.picking_type_id.code == 'internal' and not self.new_owner_id:
            raise ValidationError("New Owner must be set for internal transfers when changing ownership.")
