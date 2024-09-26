# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from pytz import UTC
from datetime import datetime, time
from random import choice
from string import digits
from werkzeug.urls import url_encode
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.osv import expression
from odoo.tools import format_date, Query


class ResUsers(models.Model):
    _inherit = 'res.users'

    authority_id = fields.Many2one(related='employee_id.authority_id',
                                   readonly=False, related_sudo=False, string='Người được ủy quyền')
    employee_mnv = fields.Char(related='employee_id.description',
                               readonly=False, related_sudo=False, string='Mã nhân viên')
    
    # @property
    # def SELF_READABLE_FIELDS(self):
    #     return super().SELF_READABLE_FIELDS + HR_READABLE_FIELDS + HR_WRITABLE_FIELDS

    # @property
    # def SELF_WRITEABLE_FIELDS(self):
    #     return super().SELF_WRITEABLE_FIELDS + HR_WRITABLE_FIELDS

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            'authority_id',
            'employee_mnv',
        ]
    
    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + [
            'authority_id',
        ]