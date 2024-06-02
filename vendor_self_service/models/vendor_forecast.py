from odoo import api, fields, models
import base64
from io import StringIO
import csv

class VendorForecast(models.Model):
    _name = 'vendor.forecast'
    _description = 'Vendor Forecast'
    _rec_name = 'product_id'

    
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
    )
    
    expected_quantity = fields.Integer(
        string='Expected Quantity',
    )
    
    forecast_date = fields.Datetime(
        string='Forecast Date',
    )
    

    def forecast_report(self):
        file_data = StringIO()
        csv_writer = csv.writer(file_data)
        csv_writer.writerow(['Product', 'Expected Quantity', 'Forecast Date'])
        for rec in self:
            csv_writer.writerow([
                rec.product_id.name, rec.expected_quantity, rec.forecast_date
            ])

        file_data.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': "forecast_report.csv",
            'datas': base64.b64encode(file_data.getvalue().encode()),
            'type': 'binary',
            'store_fname': "forecast_report.csv",
            'res_model': 'vendor.forecast',
            'res_id': self[0].id,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
    
    