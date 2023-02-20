# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request


class MenuController(odoo.http.Controller):

    # ------------------------------------------------------------
    # My Invoices
    # ------------------------------------------------------------

    @http.route(['/employee/<model("nao.employee"):employee/menu'], type='json', auth="public", methods=['GET'], website=True)
    def employee_get_menu(self, employee, **kw):
        menus = request.env['nao.menu.plate'].search([
            ('level_id', '=', employee.level_id)
        ], order='category_id')
        return menus.read()

    @http.route(['/employee/<model("nao.employee"):employee/menu'], type='json', auth="public", methods=['POST'], website=True)
    def employee_get_menu(self, employee, plates, **kw):
       if not plates:
            return {
                'message': "No existen platillos para registrar",
                'success': False,
            }

        for plate in plates:
            request.env['nao.menu.order'].create({
                'employee_id': employee.id,
                'plate_id': plate['id'],
            })

        return {
            'message': "Hola %s, ¡tu orden ha sido recibida!" % employee.id,
            'success': True,
        }
