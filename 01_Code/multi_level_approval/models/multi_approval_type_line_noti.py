# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright Domiup (<http://domiup.com>).
#
##############################################################################

from odoo import api, models, fields
import logging

# _logger = logging.getLogger(__name__)


class MultiApprovalTypeLineNoti(models.Model):
    _name = 'multi.approval.type.line.noti'
    _description = 'Multi Aproval Type Lines Noti'
    _rec_name = 'user_id'
    _order = 'sequence'

    name = fields.Char(string='Title')
    user_id = fields.Many2one(string='User', comodel_name="res.users",
                              required=True, ondelete='cascade'
                              )
    department_id = fields.Many2one(string='Department', comodel_name='hr.department')
    sequence = fields.Integer(string='Sequence')
    require_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ], string="Type of Approval", default='Optional')
    approv_id = fields.Many2one(
        string="Type", comodel_name="multi.approval.type", required=True)
    existing_user_ids = fields.Many2many('res.users', compute='_compute_existing_user_ids')
    product_category = fields.Many2one('product.category', string='Nhóm hàng hóa')
    nha_may_ids = fields.Many2many('hr.nha.may', string='Nhà máy')
    xuong_ids = fields.Many2many('hr.xuong', string='Xưởng')

    @api.depends('approv_id')
    def _compute_existing_user_ids(self):
        for record in self:
            record.existing_user_ids = record.approv_id.approv_ids.user_id

    @api.onchange("user_id")
    def _onchange_department_id(self):
        self.department_id = self.user_id.department_id



