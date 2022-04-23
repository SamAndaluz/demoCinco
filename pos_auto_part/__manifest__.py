# -*- coding: utf-8 -*-
{
    'name': "Pos Auto Parts",

    'summary': """Manage Vehicle's Spare Parts in POS""",

    'description': """This module allow you manage your auto spare part shop, work as a base module for the advance 
    auto part search for website""",

    'author': 'ErpMstar Solutions',
    'category': 'Point of Sale',
    'version': '1.0',
    'live_test_url':  "",
    # any module necessary for this one to work correctly
    'depends': ['point_of_sale','auto_part_base'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            "pos_auto_part/static/src/js/pos.js",
            "pos_auto_part/static/src/css/pos.css",
        ],
        'web.assets_qweb': [
            'pos_auto_part/static/src/xml/**/*',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'website': '',
    'auto_install': False,
    'price': 50,
    'currency': 'EUR',
}
