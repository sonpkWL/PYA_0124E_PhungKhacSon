# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrKhoiEmployee(models.Model):
    _name = 'hr.khoi.employee'
    _description = "Khoi Employee WL"

    name = fields.Char(string='Mã khối', required=True)
    description = fields.Char(string='Tên khối')

    _sql_constraints = [
        ('name_uniq', 'unique (description)', "Tag name already exists !"),
    ]
class NhaMay(models.Model):
    _name = 'hr.nha.may'
    _description = 'Nha may'
    _rec_name = 'description'

    name = fields.Char(string='Mã NM', required=True)
    description = fields.Char(string='Tên NM')

class Xuong(models.Model):
    _name = 'hr.xuong'
    _description = 'Xưởng'
    _rec_name = 'description'

    name = fields.Char(string='Mã xưởng', required=True)
    description = fields.Char(string='Tên xưởng')