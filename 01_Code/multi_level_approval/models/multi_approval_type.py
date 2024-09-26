# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright Domiup (<http://domiup.com>).
#
##############################################################################


from odoo import api, models, fields , tools, Command, _
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource
import logging

_logger = logging.getLogger(__name__)

class MultiApprovalType(models.Model):
    _name = 'multi.approval.type'
    _description = 'Multi Approval Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    image = fields.Binary(attachment=True)
    active = fields.Boolean(string='Active', default=True, readonly=False)
    mail_notification = fields.Boolean()
    mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Template for the request",
        help="Let it empty if you want to send the description of the request"
    )
    approve_mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Template of `Approved` Case",
        help="Let it empty if don't want notify"
    )
    refuse_mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Template of `Refused` Case",
        help="Let it empty if don't want notify"
    )
    user_ids = fields.Many2many('res.users', compute='_compute_user_ids', string="Approver Users")
    approv_ids = fields.One2many(
        'multi.approval.type.line.noti', 'approv_id', string="Approv",
        required=True)
    # user_xuong_ids = fields.Many2many('res.users', compute='_compute_user_xuong_ids', string="Approver Users")
    # xuong_ids = fields.One2many(
    #     'multi.approval.type.line.xuong', 'type_id', string="Approve Xuong",
    #     required=True)
    user_line_ids = fields.Many2many('res.users', compute='_compute_user_line_ids', string="Approver Users")
    line_ids = fields.One2many(
        'multi.approval.type.line', 'type_id', string="Approvers",
        required=True)
    approval_minimum = fields.Integer(
        string='Minimum Approvers', compute='_get_approval_minimum',
        readonly=True)
    approv_minimum = fields.Integer(
        string='Minimum Approvers', compute='_get_approv_minimum',
        readonly=True)
    manager_approval = fields.Selection([('Optional', 'Is Approver'), ('Required', 'Is Required Approver')],
                                        string="Employee's Manager",
                                        help="""How the employee's manager interacts with this type of approval.

            Empty: do nothing
            Is Approver: the employee's manager will be in the approver list
            Is Required Approver: the employee's manager will be required to approve the request.
        """)
    manager_stt = fields.Integer(string=' STT người quản lý')
    manager_name = fields.Char(string='Tiêu đề người quản lý')
    warehouse_approval = fields.Selection([('Optional', 'Nhận thông tin'), ('Required', 'Phê duyệt')]
                                          , string="Người quản lý kho")
    warehouse_stt = fields.Integer(string=' STT người quản lý kho')
    warehouse_name = fields.Char(string='Tiêu đề người quản lý kho')
    quanly_approval = fields.Selection([('Optional', 'Nhận thông tin'), ('Required', 'Phê duyệt')]
                                          , string="Người quản lý cấp 2")
    quanly_stt = fields.Integer(string=' STT người quản lý cấp 2')
    quanly_name = fields.Char(string='Tiêu đề người quản lý cấp 2')
    document_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ], string="Document", default='Optional')
    contact_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Contact", default='None')
    date_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Date", default='None')
    period_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Period", default='None')
    item_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Item", default='None')
    multi_items_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Multi Items", default='None')

    quantity_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Quantity", default='None')
    amount_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Amount", default='None')
    reference_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Reference", default='None')
    payment_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Payment", default='None')
    location_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Location", default='None')
    tt_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="TT Item", default='None')
    reason_wl_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Lý do", default='None')
    warehouse_wl_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Kho", default='None')
    nhamay_wl_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Nhà máy", default='None')
    nha_may_opt = fields.Many2one('hr.nha.may', string='Nhà máy')
    submitted_nb = fields.Integer(
        string="To Review",
        compute="_get_submitted_request")
    activity_notification = fields.Boolean()
    domain_type = fields.Text(string='Domain')
    product_category_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Nhóm hàng hóa", default='None')
    NM_opt = fields.Boolean(string="Bảo vệ theo NM")
    type_approval = fields.Boolean(string="Áp dụng ĐK phê duyệt")
    ticket_properties = fields.PropertiesDefinition('Ticket Properties')
    xuong_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Xưởng", default='None')
    # properties = fields.Properties(
    #     'Properties', definition='ticket_properties',
    #     copy=True)

    def _get_submitted_request(self):
        for r in self:
            print('id type:', r.id)

            domain = [('type_id', '=', r.id), ('state', '=', 'Submitted')]
            _logger.debug('Domain for submitted request count: %s', domain)
            abc = self.env['multi.approval'].search([('type_id', '=', r.id)])
            print('approval type1:', abc)
            ab = self.env['multi.approval'].search_count(domain)
            print('approval type:', ab)
            # r.submitted_nb = int(self.env['multi.approval'].search_count(domain))
            r.submitted_nb = int(self.env['multi.approval'].search_count(
                [('type_id', '=', r.id), ('state', '=', 'Submitted')])) if self.env['multi.approval'].search_count(
                [('type_id', '=', r.id), ('state', '=', 'Submitted')]) else 0

    @api.depends('line_ids')
    def _get_approval_minimum(self):
        for rec in self:
            required_lines = rec.line_ids.filtered(
                lambda l: l.require_opt == 'Required')
            rec.approval_minimum = len(required_lines)

    @api.depends('approv_ids')
    def _get_approv_minimum(self):
        for rec in self:
            optional_lines = rec.approv_ids.filtered(
                lambda l: l.require_opt == 'Optional')
            rec.approv_minimum = len(optional_lines)


    @api.depends('approv_ids')
    def _compute_user_ids(self):
        for record in self:
            record.user_ids = record.approv_ids.user_id

    @api.depends('line_ids')
    def _compute_user_line_ids(self):
        for record in self:
            record.user_line_ids = record.line_ids.user_id

    @api.constrains('approv_ids')
    def _constrains_approver_ids(self):
        # There seems to be a problem with how the database is updated which doesn't let use to an sql constraint for this
        # Issue is: records seem to be created before others are saved, meaning that if you originally have only user a
        #  change user a to user b and add a new line with user a, the second line will be created and will trigger the constraint
        #  before the first line will be updated which wouldn't trigger a ValidationError
        for record in self:
            if len(record.approv_ids) != len(record.approv_ids.user_id):
                raise ValidationError(_('An user may not be in the approver list multiple times.'))

    def create_request(self):
        view_id = self.env.ref(
            'multi_level_approval.multi_approval_view_form', False)
        return {
            'name': _('New Request'),
            'view_mode': 'form',
            'res_model': 'multi.approval',
            'view_id': view_id and view_id.id or False,
            'type': 'ir.actions.act_window',
            'context': {
                'default_type_id': self.id,
            }
        }

    def open_submitted_request(self):
        return {
            'name': _(self.name),
            'view_mode': 'tree,form',
            'res_model': 'multi.approval',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('type_id', '=', self.id), ('state', '=', 'Submitted')],
            'context': {
                'default_type_id': self.id,
            }
        }
