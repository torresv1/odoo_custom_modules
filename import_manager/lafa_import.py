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


class ImpLafaCategory(osv.osv):

    _name = 'imp.lafa.category'
    _columns = {
                    'name': fields.char('Name', size=100, required='True'),
                    'path': fields.char('Path for import', size=100, required='True'),

                }


    def import_category(self, cr, uid, ids, context=None):

        context = dict(context or {})

        imp_category_obj = self.pool.get('imp.lafa.category')
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


        product_category_obj = self.pool.get('pos.category')

        context = dict(context or {})

        rowNum = 0
        rownew = 0
        for row in csvData:

            if rowNum > 0:

                imp_name = row[0]

                #imp_id = row[0]
                #imp_parent_id = row[1]
                #imp_top_parent_id = row[2]
                #imp_title  = row[3]
                #imp_full_path = row[4]

                #imp_title= re.sub("([\s/]+)[^\w\d]", "-", imp_title) #zamena / i probela na -

                #_logger.warning("Import: id = %s, parent_id = %s, title = %s ", imp_id, imp_parent_id, imp_title)
                _logger.warning("Import: Name = %s, ", imp_name)


                product_category_search = product_category_obj.search(cr, uid, [('name', 'like', imp_name)], context=context, count=False)

                if not product_category_search:

                    values = {
                        'name': imp_name,
                    }
                    product_category_obj.create(cr, SUPERUSER_ID, values)
                    rownew += 1

            rowNum += 1

        return self.pool.get('warning').info(cr, uid, title='Import Category', message="Import for: %s  - %s , try import = %s, but only new = %s" %( file_name, dir_path, rowNum-1, rownew))




















