# -*- coding: utf-8 -*-

{
    'name': "hotel",
    'summary': "Hotel Management System",
    'description': "Hotel Guest Registration and Billing System",
    'author': "ROYTEK",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/mainmenu.xml',
        'views/charges.xml',
        'views/roomtypes.xml',
        'views/rooms.xml',
        'views/guests.xml',
        'views/guestregistration.xml'
    ],
}
