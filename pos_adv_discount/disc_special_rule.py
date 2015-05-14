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

import logging

import openerp
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class disc_special_rule(osv.osv):
    _name = 'disc.special.rule'
    _inherits = {'pos.adv_discount': "special_rule_id"}

    _columns = {
             'name':fields.char('Name', size=20),

             'special_rule_id':fields.many2one('pos.adv_discount', 'Special Rule',help="Specail Rule details", ondelete="cascade", required=True),

             'product_1':fields.char('Product One',size=20),
             'number_1':fields.char('Number One',size=20),
             'product_2':fields.char('Product Two',size=20),
             'number_2':fields.char('Number Two',size=20),
             'type':fields.char('Type',size=20),

    }






