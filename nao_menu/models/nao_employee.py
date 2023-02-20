# -*- coding: utf-8 -*-
from odoo import fields, models


class NaoEmployee(models.Model):
    _name = "nao.employee"
    _description = "Employee"

    name = fields.Char(string='Nombre', required=True)
    code = fields.Integer(string='número de empleado', required=True)
    level_id = fields.Many2one('nao.employee.level', 'Nivel de empleado', required=True)