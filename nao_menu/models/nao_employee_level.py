# -*- coding: utf-8 -*-
from odoo import fields, models


class NaoEmployeeLevel(models.Model):
    _name = "nao.employee.level"
    _description = "Employee Level"

    name = fields.Char(string='Nivel', required=True)