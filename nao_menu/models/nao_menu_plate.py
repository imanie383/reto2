# -*- coding: utf-8 -*-
from odoo import fields, models


class NaoMenuPlate(models.Model):
    _name = "nao.menu.plate"
    _inherit = 'image.mixin'
    _description = "Menu Plates"

    name = fields.Char(string='Platillo', required=True)
    category_id = fields.Many2one('nao.menu.category', 'Product Category', required=True)
    level_id = fields.Many2one('nao.employee.level', 'Level', required=True)