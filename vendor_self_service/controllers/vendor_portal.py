from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import http


class VendorPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'forecast_count' in counters:
            forecast_count = request.env['vendor.forecast'].search_count([])
            values['forecast_count'] = forecast_count
        return values


    @http.route(['/my/forecast'], type="http", auth="user", website=True)
    def portal_my_forecast(self):
       forecast_id = request.env["vendor.forecast"].sudo().search([])
       return http.request.render("vendor_self_service.portal_vendor_forecast",{"forecast_id" : forecast_id})