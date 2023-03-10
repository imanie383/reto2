# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

# from pushbullet import PushBullet
# from pywebio.input import *
# from pywebio.output import *
# from pywebio.session import *
import time


class MenuController(http.Controller):

    # ------------------------------------------------------------
    # My Invoices
    # ------------------------------------------------------------

    @http.route(['/employee/<model("nao.employee"):employee>/menu'], type='json', auth="public", methods=['GET'], website=True)
    def employee_get_menu(self, employee, **kw):
        today = fields.Date.today()
        now = fields.datetime.now()
        limit = now.replace(hour=11, minute=0, second=0, microsecond=0)

        if today.weekday() != 0 or now > limit:
            return {
                'message': "Solo puedes reservar los lunes antes de las 11 AM",
                'success': False,
            }

        menus = request.env['nao.menu.plate'].search([
            ('level_id', '=', employee.level_id)
        ], order='category_id')


        return {
            'message': "Exito",
            'success': True,
            'menus': menus.read(),
        }


    @http.route(['/employee/<model("nao.employee"):employee>/menu'], type='json', auth="public", methods=['POST'], website=True)
    def employee_set_menu(self, employee, plates, **kw):
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

        message = "Hola %s, ¡tu orden ha sido recibida!" % employee.id
        this.notificacion(message)

        return {
            'message': message,
            'success': True,
        }

    @http.route(['/test'], type='http', auth="public", website=True)
    def test(self, **kw):
        url = 'http://localhost:8064'
        db = 'nao_14'
        username = 'admin'
        password = 'admin'

        import xmlrpc.client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        empleado = models.execute_kw(db, uid, password, 'nao.employee', 'search_read', [[['code', '=', '111']]], {'fields': ['name', 'level_id']})

        if not empleado:
            return False

        empleado = empleado[0]

        platos = models.execute_kw(db, uid, password, 'nao.menu.plate', 'search_read', [[['level_id', '=', empleado['level_id'][0] ]]], {'fields': ['name', 'category_id']})

    @http.route(['/test2'], type='json', auth="public", website=True)
    def test2(self, platos=False, **kw):
        url = 'http://localhost:8064'
        db = 'nao_14'
        username = 'admin'
        password = 'admin'


        import xmlrpc.client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        for plato in platos:
            models.execute_kw(db, uid, password, 'nao.menu.order', 'create', [plato])

    def notificacion(self, message=''):
        access_token = "o.q1QIkYnI2WUdNX3wPSiWSp"
        title = input('Title')
        pb = PushBullet(access_token)
        push = pb.push_note(title, message)
        hold()
