# -*- coding: utf-8 -*-
from odoo import fields, models


class NaoMenuCategory(models.Model):
    _name = "nao.menu.category"
    _description = "Menu Category"

    name = fields.Char(string='Category', required=True)