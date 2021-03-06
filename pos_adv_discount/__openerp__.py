# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Today OpenERP SA (<http://www.openerp.com>).
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
    'name': 'POS Advance Discount',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'summary': 'POS Advance Discount for the Point of Sale ',
    'description': """

=======================

This module adds POS Advance Discount features to the Point of Sale:

-Percentage off the price of the product
-X amount of product for the price of Y quantity of the same product

""",
    'author': 'Viktor Vorobjov',
    'depends': ['point_of_sale'],
    'website': 'https://www.prolv.net',
    'data': [
        'views/templates.xml',
        'pos_adv_discount_views.xml',
        'pos_order_in_views.xml',
        'security/ir.model.access.csv',
    ],
    'qweb':[

        'static/src/xml/adv_discount.xml',
    ],
    'installable': True,
    'auto_install': False,
}

