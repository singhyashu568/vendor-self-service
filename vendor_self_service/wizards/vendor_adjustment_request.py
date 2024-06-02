from odoo import api, fields, models
from odoo.tools import float_round
from datetime import timedelta
import logging

from datetime import time

class VendorAdjustmentRequest(models.TransientModel):
    _name = 'vendor.adjustment.request'
    _description = 'Vendor Adjustment Request'

    
    order_id = fields.Many2one(
        string='Order\'s',
        comodel_name='sale.order',
    )
    
    adjustment_detail = fields.Text(
        string='Adjustment Detail',
    )
    
    comment = fields.Text(
        string='Comment',
    )


    def request_submission(self):
        self.ensure_one()
        template = self.env.ref('vendor_self_service.email_template_order_adjustment_request')
        self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)


    def action_name(self):
        products = self.env['product.product'].search([])

        stock_moves = self.env['stock.move'].search([])

        stock_data = {}
        for product in products:
            stock_sold = sum(stock_moves.filtered(
                lambda m: m.product_id == product and m.location_dest_id.usage == 'customer'
            ).mapped('product_uom_qty'))
            

            stock_data[product.id] = {
                'sku': product.default_code,
                'ean': product.barcode,
                'stock_sold': stock_sold,

        }

        print("-----------------------Action -----------",stock_data)


# class ProductProduct(models.Model):
#     _inherit = 'product.product'

#     sales_count = fields.Float(compute='_compute_sales_count', string='Sold')

#     def _compute_sales_count(self):
#         r = {}
#         self.sales_count = 0
#         if not self.user_has_groups('sales_team.group_sale_salesman'):
#             return r
#         date_from = fields.Datetime.to_string(fields.datetime.combine(fields.datetime.now() - timedelta(days=200),
#                                                                       time.min))
#         done_states = self.env['sale.report']._get_done_states()
#         domain = [('state', 'in', done_states),
#             ('product_id', 'in', self.ids),
#             ('date', '>=', date_from)]
#         for group in self.env['sale.report'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id']):
#             r[group['product_id'][0]] = group['product_uom_qty']
#         for product in self:
#             if not product.id:
#                 product.sales_count = 0.0
#                 continue
#             product.sales_count = float_round(r.get(product.id, 0), precision_rounding=product.uom_id.rounding)
#         print("---------------------------Sales Count----------------",r)
#         return r
    
    
    
    
    