# -*- coding: utf-8 -*-
{
    'name': 'Odoo Approval',
    'version': '16.0.1.0',
    'category': 'Đề xuất',
    'description': """
Odoo Approval Module: Create and validate approvals requests.
Each request can be approve by many levels of different managers.
The managers wil review and approve sequentially
    """,
    'summary': '''
    Create and validate approval requests. Each request can be approved by many levels of different managers
    ''',
    'author': '',
    'license': 'OPL-1',
    'support': '',
    'website': '',
    'depends': [
        'hr',
        'mail',
        'product',
        'stock'
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'data/mail_template_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

        # wizard
        'wizard/refused_reason_views.xml',
        'wizard/action_check_views.xml',
        'wizard/line_import_wizard.xml',

        'views/multi_approval_item_line_views.xml',
        'views/multi_approval_product_line_views.xml',
        'views/multi_approval_type_views.xml',
        'views/multi_approval_views.xml',
        'views/report_don_ra_cong_view.xml',

        'views/hr_khoi_employee_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_nha_may_view.xml',
        'views/hr_xuong_view.xml',
        'views/res_users_view.xml',

        # Add actions after all views.
        'views/actions.xml',

        # Add menu after actions.
        'views/menu.xml',

        #Add report printer
        'report/report_approval.xml',
        'report/report_proposal_approval.xml',
        
    ],
    'images': ['static/description/banner.jpg'],
    'test': [],
    'demo': [],
    'installable': True,
    'active': False,
    'application': True,
}
