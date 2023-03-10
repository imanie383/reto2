# -*- coding: utf-8 -*-
from odoo import fields, models


class NaoMenuPlate(models.Model):
    _name = "nao.menu.order"
    _description = "Menu orders"

    employee_id = fields.Many2one('nao.employee', string='Employee', required=True)
    plate_id = fields.Many2one('nao.menu.plate', string='Menu', required=True)
    category_id = fields.Many2one('nao.menu.category', 'Product Category', related='plate_id.category_id', store=True)
    selection_date = fields.Date(string='Selection Date', default=lambda self: fields.Date.today(), required=True)

    # _sql_constraints = [
    #     ('code_order_uniq', 'unique (employee_id, category_id, selection_date)', 'Solo se puede registrar una orden por dia'),
    # ]
