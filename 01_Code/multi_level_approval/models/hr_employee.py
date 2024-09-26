# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from pytz import UTC
from datetime import datetime, time
from random import choice
from string import digits
from werkzeug.urls import url_encode
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError
from odoo.osv import expression
from odoo.tools import format_date, Query


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _order = 'name, description'

    description = fields.Char(string='Mã nhân viên', required=True, store=True)
    MST = fields.Char(string='MST')
    nha_may_id = fields.Many2one('hr.nha.may', string='Nhà máy TN')
    khoi = fields.Many2one('hr.khoi.employee', string='Khối PB')
    authority_id = fields.Many2one('res.users', compute='_compute_authority'
                                   , store=True, readonly=False, string='Người được ủy quyền')

    # _sql_constraints = [
    #     ('unique_description', 'unique (description)', "Tag code already exists !"),
    # ]
    _sql_constraints = []
    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'description'])
        return [(template.id, '%s%s' % (template.name and '[%s] ' % template.name, template.description or ''))
                for template in self]

    @api.depends('user_id')
    def _compute_authority(self):
        for employee in self:
            manager = employee.user_id
            previous_manager = employee._origin.user_id
            if manager and (employee.authority_id == previous_manager or not employee.authority_id):
                employee.authority_id = manager
            elif not employee.authority_id:
                employee.authority_id = False

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    description = fields.Char("Mã nhân viên", related='employee_id.description', compute_sudo=True)
    MST = fields.Char("MST", related='employee_id.MST', compute_sudo=True)
    nha_may_id = fields.Many2one('hr.nha.may', related='employee_id.nha_may_id'
                               , compute_sudo=True, string="Nhà máy TN")
    khoi = fields.Many2one('hr.khoi.employee', related='employee_id.khoi'
                           , compute_sudo=True, string="khoi")
    authority_id = fields.Many2one('res.users', related='employee_id.authority_id'
                                   , compute_sudo=True, string='Người được ủy quyền')
