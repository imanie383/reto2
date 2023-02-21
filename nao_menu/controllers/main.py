# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from pushbullet import PushBullet
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time


class MenuController(odoo.http.Controller):

    # ------------------------------------------------------------
    # My Invoices
    # ------------------------------------------------------------

    @http.route(['/employee/<model("nao.employee"):employee/menu'], type='json', auth="public", methods=['GET'], website=True)
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

        message = "Hola %s, ¡tu orden ha sido recibida!" % employee.id
        this.notificacion(message)

        return {
            'message': message,
            'success': True,
        }

    def notificacion(self, message=''):
        access_token = "o.q1QIkYnI2WUdNX3wPSiWSp"
        title = input('Title')
        pb = PushBullet(access_token)
        push = pb.push_note(title, message)
        hold()
