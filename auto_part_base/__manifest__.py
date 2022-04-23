# -*- coding: utf-8 -*-
{
    'name': "Auto Parts Base",

    'summary': """Manage Vehicle's Spare Parts""",

    'description': """This module allow you manage your auto spare part shop, work as a base module for the advance 
    auto part search for website""",

    'author': 'ErpMstar Solutions',
    'category': 'Management System',
    'version': '1.0',
    'live_test_url':  "https://youtu.be/tNyPFy_RhQo",
    # any module necessary for this one to work correctly
    'depends': ['product'],

    # always loaded
    'data': [
        'security/auto_part_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'website': '',
    'auto_install': False,
    'price': 35,
    'currency': 'EUR',
}
