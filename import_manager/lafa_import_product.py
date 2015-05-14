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

import openerp.exceptions


from dateutil import parser


from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import html2text
from openerp import netsvc
import openerp.tools as tools

from openerp import models, api

import os
import csv

import re
import io
import codecs

import itertools
import operator



_logger = logging.getLogger(__name__) # Need for message in console.

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


class ImpLafaProduct(osv.osv):

    _name = 'imp.lafa.product'
    _columns = {
                    'name': fields.char('Name', size=100, required='True'),
                    'path': fields.char('Path for import', size=100, required='True'),

                }

    def _log_import(self, cr, uid, l_file, rwa, l_messagem): # File name , Type accees to file r- read, w - write, a - append, Text message

        try:
            log_import_file = codecs.open(l_file, rwa, encoding='utf-8')
        except Exception, e:
             ierror = tools.ustr(e)
             return self.pool.get('warning').info(cr, uid, title='Error source log', message="Error: %s " %(ierror))

        #_logger.warning("Error: %s", l_messagem )
        log_import_file.write(l_messagem + os.linesep)
        log_import_file.close()



    def _create_product(self, cr, uid, values, source_log, context=None):

        product_product_obj = self.pool.get('product.product')

        try:
            newid = product_product_obj.create(cr, SUPERUSER_ID, values)
        except Exception, e:

            #_logger.warning("Error: %s", e )
            self._log_import(cr, uid, source_log, 'a',  'Error: %s' % (e) )

            return 0
        return newid

    def _check_double(self, cr, uid, source_dir, filename):

        keys = []

        try:
            import_file = codecs.open(os.path.join(source_dir, filename), 'r', encoding='utf-8')

        except Exception, e:
             ierror = tools.ustr(e)
             return self.pool.get('warning').info(cr, uid, title='Error source double', message="Error: %s " %( ierror ))

        csvData = csv.reader(utf_8_encoder(import_file))

        #Add date time to already log file
        filename_log_double = filename+'__import_log_double.txt'
        source_log_double = os.path.join(source_dir, filename_log_double)
        self._log_import(cr, uid, source_log_double, 'w', datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%SZ") )

        for key, grp in itertools.groupby(sorted(csvData, key=operator.itemgetter(0)), key=operator.itemgetter(0)):
            rowss = list(grp)

            if len(rowss) > 1:
                #_logger.warning("Double: %s", key )
                keys.append(key)

                for row in rowss:
                    self._log_import(cr, uid, source_log_double, 'a', "%s" % row )




        import_file.close()

        return keys




    def import_product(self, cr, uid, ids, context=None):

        context = dict(context or {})
#Get import paramets
        imp_category_obj = self.pool.get('imp.lafa.product')
        imp_category_data = imp_category_obj.browse(cr, uid, ids, context=context)

        file_name = imp_category_data.name
        dir_path = imp_category_data.path

        filename = file_name
        source_dir = dir_path

#Add date time to main log file
        filename_log = filename+'__import_log.txt'
        source_log = os.path.join(source_dir, filename_log)
        self._log_import(cr, uid, source_log, 'a', datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%SZ") )

#Add date time to already log file
        filename_log_already = filename+'__import_log_already.txt'
        source_log_already = os.path.join(source_dir, filename_log_already)
        self._log_import(cr, uid, source_log_already, 'a', datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%SZ") )


        try:
            import_file = codecs.open(os.path.join(source_dir, filename), 'r', encoding='utf-8')
        except Exception, e:
             ierror = tools.ustr(e)
             return self.pool.get('warning').info(cr, uid, title='Error source import', message="Error: %s " %( ierror ))

        #csvData = csv.reader(import_file, delimiter=',', quotechar="'")
        #csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),dialect=dialect, **kwargs)
        csvData = csv.reader(utf_8_encoder(import_file))

#check double ref. number in csv
        d_keys = self._check_double(cr, uid, source_dir, filename)
        #_logger.warning("Double: Keys = %s", d_keys)

        pos_category_obj = self.pool.get('pos.category')
        product_product_obj = self.pool.get('product.product')

        rowNum = 0
        rownew = 0

#Start reading CSV
        for row in csvData:

            if rowNum > 0 and row[0] not in d_keys:

                imp_ref = row[0]
                imp_name = row[1].decode('utf-8')
                imp_sale_price = row[2]
                imp_pos_cat = row[3]


                #imp_title= re.sub("([\s/]+)[^\w\d]", "-", imp_title) #zamena / i probela na -


#debug view
                #_logger.warning("-------------------------------------------------")
                #_logger.warning("Import: Ref = %s, name = %s, Cat = %s", imp_ref,imp_name, imp_pos_cat )

#write to log file
                #self._log_import(cr, uid, source_log, 'a', '-------------------------------------------------')
                #self._log_import(cr, uid, source_log, 'a', 'Import: Ref = %s, name = %s, Cat = %s' % (imp_ref, imp_name, imp_pos_cat) )


                product_search = product_product_obj.search(cr, uid, [('default_code', '=', imp_ref), '|', ('active', '=', True), ('active', '=', False)], context=context, count=False)

                if not product_search:

                    pos_category_search = pos_category_obj.search(cr, uid, [('name', '=', imp_pos_cat)], context=context, count=False)

                    values = {
                        'default_code': imp_ref,
                        'name': imp_name,
                        'list_price' : imp_sale_price,
                        'pos_categ_id': pos_category_search[0]
                    }

                    #_logger.warning("No in database: Ref = %s, Name = %s, Cat = %s, POS category ID = %s", imp_ref, imp_name, imp_pos_cat, pos_category_search[0] )
                    #_logger.warning("Try Import: %s", imp_ref )


                    try_import = self._create_product(cr, uid, values, source_log)

                    #_logger.warning("Import Result: %s", try_import )

                    rownew += 1


                else:

# Write to log already in database
                    product_data = product_product_obj.browse(cr, uid, product_search, context=context)
                    self._log_import(cr, uid, source_log_already,'a', 'CSV -> Ref = %s, Name = %s : Odoo -> oRef = %s, oName = %s' % (imp_ref, imp_name, product_data.default_code, product_data.name )  )
# Debug log
                    #_logger.warning("Already in: Ref = %s, oRef = %s, oNAme = %s", imp_ref, product_data.default_code, product_data.name )


            rowNum += 1

        if rowNum == 0:
            rowNum+1

        self._log_import(cr, uid, source_log, 'a', 'Import for: %s  - %s , try import = %s, but only new = %s' % (file_name, dir_path, rowNum-1, rownew) )

        return self.pool.get('warning').info(cr, uid, title='Import Category', message="Import for: %s  - %s , try import = %s, but only new = %s" %( file_name, dir_path, rowNum-1, rownew))




















