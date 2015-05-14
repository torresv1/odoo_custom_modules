# -*- coding: utf-8 -*-


import logging

import os
import sys
import shutil
import glob
import os



import base64
import xmlrpclib


import time
import datetime
from dateutil import tz

import pytz


from dateutil import parser


from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import html2text
from openerp import netsvc
import openerp.tools as tools

from openerp import models, api


import csv
import re

_logger = logging.getLogger(__name__) # Need for message in console.


class product_category(osv.osv):
    _inherit = "product.category"

    _columns = {

        'imp_id': fields.integer('Import Id', required=False),
        'imp_parent_id': fields.integer('Parent iD', required=False),
        'imp_ok': fields.boolean('Import', help="All ok"),

    }

    _default = {
        'imp_ok': False
    }



class imp_category(osv.osv):

    _name = 'imp.category'
    _columns = {
                    'name': fields.char('Name', size=100, required='True'),
                    'path': fields.char('Path for import', size=100, required='True'),

                }


    def import_category(self, cr, uid, ids, context=None):

        context = dict(context or {})

        imp_category_obj = self.pool.get('imp.category')
        imp_category_data = imp_category_obj.browse(cr, uid, ids, context=context)

        file_name = imp_category_data.name
        dir_path = imp_category_data.path


        filename = file_name
        source_dir = dir_path


        try:
            import_file = open(os.path.join(source_dir, filename), 'r')
        except Exception, e:
             ierror = tools.ustr(e)
             return self.pool.get('warning').info(cr, uid, title='Error source', message="Error: %s " %( ierror ))

        #csvData = csv.reader(import_file, delimiter=',', quotechar="'")
        csvData = csv.reader(import_file)


        product_category_obj = self.pool.get('product.category')

        context = dict(context or {})

        rowNum = 0
        rownew = 0
        for row in csvData:

            if rowNum > 0:

                imp_id = row[0]
                imp_parent_id = row[1]
                #imp_top_parent_id = row[2]
                imp_title  = row[3]
                #imp_full_path = row[4]

                imp_title= re.sub("([\s/]+)[^\w\d]", "-", imp_title)

                #_logger.warning("Import: id = %s, parent_id = %s, title = %s ", imp_id, imp_parent_id, imp_title)


                product_category_search = product_category_obj.search(cr, uid, [('imp_id', '=', imp_id)], context=context, count=False)

                if not product_category_search:

                    values = {
                        'name': imp_title,
                        'imp_id': imp_id,
                        'imp_parent_id': imp_parent_id,
                    }
                    product_category_obj.create(cr, SUPERUSER_ID, values)
                    rownew += 1

            rowNum += 1

        return self.pool.get('warning').info(cr, uid, title='Import Category', message="Import for: %s  - %s , try import = %s, but only new = %s" %( file_name, dir_path, rowNum-1, rownew))



    def search_parent(self, cr, uid, ids, context=None):

        context = dict(context or {})

        product_category_obj = self.pool.get('product.category')

        context = dict(context or {})

        rowNum = 0
        rowFix = 0

        #[ '|' , ( 'partner_id' , '!=',34),'!', ('name','ilike','spam'),]
        product_category_search = product_category_obj.search(cr, uid, [('imp_id', '>', 0), ('imp_ok', '=', False)], context=context, count=False)

        for product_cat in product_category_search:

            product_cat_data = product_category_obj.browse(cr, uid, product_cat, context=context)

            odoo_id = product_cat
            imp_parent_id = product_cat_data.imp_parent_id

            if imp_parent_id  > 0 :

                new_parent = product_category_obj.search(cr, uid, [('imp_id', '=', imp_parent_id)], context=context, count=False)

                if new_parent:

                    product_category_obj.write(cr, uid, odoo_id, {'parent_id': new_parent[0], 'imp_ok': True}, context=context)
                    rowFix += 1

            rowNum += 1


        return self.pool.get('warning').info(cr, uid, title='Search Parent', message="Search = %s, fix = %s" %( rowNum, rowFix))



















