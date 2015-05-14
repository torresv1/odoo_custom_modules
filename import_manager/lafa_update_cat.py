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


class UpdLafaProduct(osv.osv):

    _name = 'upd.lafa.product'
    _columns = {
                    'name': fields.char('Name', size=100, required='True'),
                    'path': fields.char('Path for import', size=100, required='True'),

                }


    def update_category(self, cr, uid, ids, context=None):

        context = dict(context or {})

        imp_category_obj = self.pool.get('upd.lafa.product')
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


        pos_category_obj = self.pool.get('pos.category')
        product_product_obj = self.pool.get('product.product')

        context = dict(context or {})

        rowNum = 0
        rownew = 0
        for row in csvData:

            if rowNum > 0:

                imp_ref = row[0]
                imp_cat = row[3]

                #imp_id = row[0]
                #imp_parent_id = row[1]
                #imp_top_parent_id = row[2]
                #imp_title  = row[3]
                #imp_full_path = row[4]

                #imp_title= re.sub("([\s/]+)[^\w\d]", "-", imp_title) #zamena / i probela na -

                #_logger.warning("Import: id = %s, parent_id = %s, title = %s ", imp_id, imp_parent_id, imp_title)
                _logger.warning("Import: ref = %s, pos category = %s ", imp_ref, imp_cat)

                product_product_search = product_product_obj.search(cr, uid, [('default_code', '=', imp_ref)], context=context, count=False)


                if product_product_search:


                    pos_category_search = pos_category_obj.search(cr, uid, [('name', 'like', imp_cat)], context=context, count=False)

                    if pos_category_search:

                        product_product_obj.write(cr, uid, product_product_search[0], {'pos_categ_id': pos_category_search[0]}, context=context)




                        _logger.warning("Search: ID = %s, categ pos ID = %s ", product_product_search[0], pos_category_search[0] )

                        rownew += 1


                    #values = {
                      #  'name': imp_name,
                    #}
                    #product_category_obj.create(cr, SUPERUSER_ID, values)
                    #rownew += 1

                #pos_categ_id

                #product_category_search = pos_category_obj.search(cr, uid, [('name', 'like', imp_name)], context=context, count=False)

                #if not product_category_search:

                    #values = {
                        #'name': imp_name,
                   # }
                    #product_category_obj.create(cr, SUPERUSER_ID, values)
                    #rownew += 1





            rowNum += 1

        return self.pool.get('warning').info(cr, uid, title='Import Category', message="Import for: %s  - %s , try import = %s, but only new = %s" %( file_name, dir_path, rowNum-1, rownew))




















