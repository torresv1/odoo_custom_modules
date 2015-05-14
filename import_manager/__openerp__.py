# -*- coding: utf-8 -*-

{
    'name' : 'Import Manager Odoo',
    'version' : '8.0.0.2',
    'author' : 'Viktor Vorobjov',
    'category': 'default',
    'description' : """

    
    """,
    'website' : 'http://www.prolv.net',
    'depends' : ['base_setup','warning_popup', 'product','sale'],
    'data': [
        'ean_import_view.xml',
        'wizard/fix_category_view.xml',
    ],
    'installable': True,
}

