# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Multi Assembly Order Report',
    'version': '1.0',
    'category': 'MRP',
    "description": """
        This module is used to generate 'Multi Assembly Order (Manufacturing Order) Report' for 'mrp.production' object.We have added two many2many fields for product_ids and bom_ids to generate Manufacturing order for more than one products.
        'Migrated from openerp-7 to odoo-8'
    """,
    'author': 'Browseinfo',
    'website': 'http://www.browseinfo.in',
    'depends': ['mrp', 'product'],
    'data': ['views/mrp_assembly_order_report_view.xml',
			'report/mrp_assembly_order_menu.xml',
			'views/mrp_production_view.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
