# -*- coding: utf-8 -*-

import logging

from openerp import models, fields, api
from openerp.tools.translate import _

from datetime import datetime

_logger = logging.getLogger(__name__) # Need for message in console.


class FixCategory(models.TransientModel):

    _name = 'fix.category'
    _description = 'Fix POS category'

    first_pos_cat_id = fields.Many2one('pos.category', 'From POS Category')
    second_pos_cat_id = fields.Many2one('pos.category', 'To POS Category')

    @api.one
    def check_category(self):

        #_logger.warning("Cat ID = %s, Cat Name = %s", self.first_pos_cat_id.id, self.first_pos_cat_id.name)

        product_product_obj = self.env['product.product']
        product_product_search = product_product_obj.search([('pos_categ_id', '=', self.first_pos_cat_id.id)])
        product_product_search.write({'pos_categ_id': self.second_pos_cat_id.id })

        return True
