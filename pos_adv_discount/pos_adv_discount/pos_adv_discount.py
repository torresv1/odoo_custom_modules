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

import time
import datetime

from dateutil import rrule


_logger = logging.getLogger(__name__)


class pos_adv_discount(osv.osv):
    _name = 'pos.adv_discount'
    _description = "POS advance discount info"



    def _get_available_pfilters(self, cr, uid, context=None):
        """
           This function will return the list of filter allowed according
           :pres_filter: list of tuple
        """
        #default available choices
       # pres_filter = [('all', _('All products')), ('category', _('Specific product categories')),('product', _('Specific products')), ('special', _('Special Rules')) ]
        pres_filter = [
            ('all', _('All products')),
            ('category', _('Specific product categories')),
            ('product', _('Specific products')) ]

        return pres_filter

    def _get_available_cfilters(self, cr, uid, context=None):
        """
           This function will return the list of filter allowed according
           :pres_filter: list of tuple
        """
        #default available choices
        pres_filter = [
            ('all', _('All customer')),
            ('customer', _('Specific customers'))]

        return pres_filter

    def _get_special_rule(self, cr, uid, context=None):
        """
           This function will return the list of filter allowed according
           :pres_filter: list of tuple
        """
        #default available choices
        pres_filter = [
            ('b1gdisc', _('Buy one and get another Discount')),
            ('b1gfree', _('Buy one and get another Free'))]

        return pres_filter

    def _get_value_method(self, cr, uid, context=None):
        """
           This function will return the list of filter allowed according
           :pres_filter: list of tuple
        """
        #default available choices
        pres_filter = [
            ('percent', _('Percentage off')),
            ('amount', _('Amount off'))]

        return pres_filter


    def _get_discount_type(self, cr, uid, context=None):
        """
           This function will return the list of filter allowed according
           :pres_filter: list of tuple
        """
        #default available choices
        pres_filter = [
            ('simple_dsc', _('Simple Discount')),
            ('min_purchase_dsc', _('Minimum Purchase Discount')),
            ('buygetfree', _('Buy N Get one Free')),
            ('BuyXforpriceY', _('Buy X for the price of Y')),
            ('paired_dsc', _('Paired Discount')),
            ('paired_set_dsc', _('Paired set Discount')),
            ('BuyXforFixedpriceY', _('Buy X for Fixed price Y')),

            ]

        return pres_filter


    def on_change_amount(self, cr, uid, ids, amount=False, context=None):

        res = {}

        if amount > 100:
            res['amount'] = 0

            warning = {
                'title': _('Ammount off!'),
                'message' : _('Amount - is above > 100%')
            }
            return {'warning': warning, 'value': res}


    def on_change_value_method(self, cr, uid, ids, value_method=False, context=None):

        res = {}

        if value_method == "" or value_method == "none" or value_method is False:
            #res['amount'] = 0
            res['value_method'] = 'percent'
            return {'value': res}

        if value_method == "amount":
            #res['amount'] = 0
            res['value_method'] = 'percent'

            warning = {
                'title': _('Ammount off!'),
                'message' : _('If you require this feature please contact your system administrator.')
            }
            return {'warning': warning, 'value': res}


    def on_change_discount_type(self, cr, uid, ids, discount_type=False, context=None):

        res = {}

        if discount_type == "" or discount_type == "none" or discount_type is False:
            #res['amount'] = 0
            res['discount_type'] = 'simple_dsc'
            return {'value': res}


        if discount_type == "BuyXforpriceY":

            res['discount_type'] = 'BuyXforpriceY'

            return {'value': res}

        if discount_type == "BuyXforFixedpriceY":

            res['discount_type'] = 'BuyXforFixedpriceY'

            return {'value': res}


        if discount_type == "buygetfree":

            res['discount_type'] = 'buygetfree'

            warning = {
                'title': _('Discount type!'),
                'message' : _('If you require this feature please contact your system administrator.')
            }

            return {'warning': warning, 'value': res}


        if discount_type == "min_purchase_dsc":

            res['discount_type'] = 'simple_dsc'

            warning = {
                'title': _('Discount type!'),
                'message' : _('If you require this feature please contact your system administrator.')
            }

            return {'warning': warning, 'value': res}


        if discount_type == "paired_dsc":

            res['discount_type'] = 'simple_dsc'

            warning = {
                'title': _('Discount type!'),
                'message' : _('If you require this feature please contact your system administrator.')
            }

            return {'warning': warning, 'value': res}

        if discount_type == "paired_set_dsc":

            res['discount_type'] = 'simple_dsc'

            warning = {
                'title': _('Discount type!'),
                'message' : _('If you require this feature please contact your system administrator.')
            }

            return {'warning': warning, 'value': res}






    def on_change_date(self, cr, uid, ids, start_date=False, end_date=False, context=None):

        context = dict(context or {})
        res = {}

        if end_date != False:
            if end_date < start_date or start_date > end_date:
                res['end_date'] = ''
                warning = {
                    'title': _('Date incorect!'),
                    'message' : _('Error: End date is earlier than Start Date')
                }
                return {'warning': warning, 'value': res}
        else:
            return

       # counter_id = context.get('active_id')

        """
        if discount_type == "" or discount_type == "none" or discount_type is False:
            #res['amount'] = 0
            res['discount_type'] = 'simple_dsc'
            return {'value': res}

        if discount_type not in "simple_dsc":
            #res['amount'] = 0
            res['discount_type'] = 'simple_dsc'

            warning = {
                'title': _('Discount type!'),
                'message' : _('If you require this feature please contact your system administrator.')
            }

        """



    _columns = {

        'name': fields.char('Name', size=50, required=True),
        'code': fields.char('Code', size=50, required=True),
        'default_debt_account': fields.char('Default debt account', size=20),
        'default_credit_account': fields.char('Default credit account', size=20),

        #'default_debt_account': fields.many2one('account.account', 'Credit Account'),
        #'default_credit_account': fields.many2one('account.account', 'Debit Account'),

        'journal_id': fields.many2one('account.journal', 'Available Journal'),

        'start_date': fields.datetime('Start Date'),
        'end_date': fields.datetime('End Date'),

        'value_method': fields.selection(_get_value_method, 'Value Method', required=True),
        'amount': fields.integer('Amount', required=True),


        'cfilter': fields.selection(_get_available_cfilters, 'Selection Customer Filter', required=True),



        'discount_type': fields.selection(_get_discount_type, 'Selection Discount', required=True),


        'partner': fields.many2many('res.partner', 'pos_adv_disc_partner_rel', 'pos_ad_dic_id', 'partner_id', 'Customer'),
        'product': fields.many2many('product.product', 'pos_adv_disc_product_rel', 'pos_ad_dic_id', 'product_id', 'Product'),
        'pcategory': fields.many2many('pos.category', 'pos_adv_disc_pcategory_rel', 'pos_ad_dic_id', 'category_id', 'POS category'),



        'pfilter': fields.selection(_get_available_pfilters, 'Selection Product Filter', required=True),

        'special_rule': fields.selection(_get_special_rule, 'Selection Discount Rule', required=False),

        'active': fields.boolean('Active Discount', default=True),

        # 'special_rule_ids': fields.one2many('fleet.vehicle.cost', 'parent_id', 'Included Services'),
        # 'product_1': fields.one2many('product.template', 'ad_product_1', 'Product 1'),

        'product_1': fields.many2one('product.product', 'Product 1', change_default=True, select=True),
        'pro_val_1': fields.integer('val 1'),

        #'product_2': fields.one2many('product.template', 'ad_product_2', 'Product 2'),
        'product_2': fields.many2one('product.product', 'Product 2', change_default=True, select=True),
        'pro_val_2': fields.integer('val 2'),


        }

    _defaults = {

        'cfilter': 'all',
        'pfilter': 'all',
        'start_date': datetime.datetime.today(),


    }

    def create(self, cr, uid, vals, context=None):
        context = dict(context or {})

        result = super(pos_adv_discount, self).create(cr, uid, vals, context)

                    #result = super(account_move, self).create(cr, uid, vals, c)
       # tmp = self.validate(cr, uid, [result], context)

        self.validate(cr, uid, [result], context=context)
        self.validate_amount(cr, uid, [result], context=context)

        return result




    def write(self, cr, uid, ids, vals, context=None):

        if context is None:
            context = {}
        #_logger.warning("vals %s", vals )

        result = super(pos_adv_discount, self).write(cr, uid, ids, vals, context=context)
        self.validate(cr, uid, ids, context=context)
        self.validate_amount(cr, uid, ids, context=context)

        return result


    def _get_date_range(self, cr, uid, ids, date_from=None, date_to=None ,  context=None):

        date_list = []

        for dd in rrule.rrule(rrule.DAILY,

                  dtstart=datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S"),
                  until=datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")):

            date_list.append(dd)

        return date_list




    def validate_amount(self, cr, uid, ids, context=None):


        for discount in self.browse(cr, uid, ids, context):

            start_date = discount.start_date
            end_date = discount.end_date

        #date_data = self._get_date_range(cr, uid, ids, start_date, end_date, context=context)

        #_logger.warning("date_data %s", date_data )

        _logger.warning("start_date %s", start_date )
        _logger.warning("end_date %s", end_date )

        adv_discount_ids = self.pool['pos.adv_discount'].search(cr, uid, [

            ('active', '=', True),
            ('start_date', '<=', start_date),'|',
            ('end_date', '<=', end_date),
            ('end_date', '=', False)

                ], context=context)


        _logger.warning("adv_discount_ids %s", adv_discount_ids )





    def validate(self, cr, uid, ids, context=None):


        for discount in self.browse(cr, uid, ids, context):

            cfilter = discount.cfilter
            partners = discount.partner

            pfilter = discount.pfilter

            products = discount.product
            categories = discount.pcategory


            if cfilter in 'customer' and len(partners.ids) == 0:

                raise osv.except_osv(_('Error!'), _("Cannot save! You must select customers."))

            if pfilter in 'product' and len(products.ids) == 0:

                raise osv.except_osv(_('Error!'), _("Cannot save! You must need select products."))

            if pfilter in 'category' and len(categories.ids) == 0:

                raise osv.except_osv(_('Error!'), _("Cannot save! You must need select categories."))



pos_adv_discount()

    
class res_users(osv.osv):
    _inherit = 'res.partner'
    _columns = {

        'pos_ad_dic': fields.many2many('pos.adv_discount', 'pos_adv_disc_partner_rel', 'partner_id', 'pos_ad_dic_id', 'POS advance discount'),

    }

res_users()


class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {

        'pos_ad_dic': fields.many2many('pos.adv_discount', 'pos_adv_disc_product_rel', 'product_id', 'pos_ad_dic_id', 'POS advance discount'),

        }

product_product()






