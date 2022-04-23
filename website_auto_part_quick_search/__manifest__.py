# -*- coding: utf-8 -*-
{
    'name': "Auto Parts Website Quick Search",

    'summary': """Quickly Find the Spare Parts for a Vehicle""",

    'description': """
        This module provides a flexibility to the users to quickly search the auto parts for there vehicle.
    """,

    'author': 'ErpMstar Solutions',
    'category': 'Management System',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['auto_part_base', 'website_sale'],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_auto_part_quick_search/static/src/js/auto_parts.js',
            '/website_auto_part_quick_search/static/src/css/select_auto.css',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'price': 35,
    'currency': 'EUR',
}
