# -*- coding: utf-8 -*-
{
    "name": "Implent in pos credit card instalment",
    "summary": "",
    "description": """
    """,
    "author": "Axcelere",
    "website": "http://www.axcelere.com",
    "category": "pos",
    "version": "16.0.0.1",
    "depends": ["point_of_sale", "card_installment"],
    "data": [
        # 'security/ir.model.access.csv',
        "views/pos_payment_method.xml",
        "views/pos_make_payment.xml",
        # "views/point_of_sale.xml",
        "views/pos_payment.xml",
    ],
    'assets': {
            'point_of_sale.assets': [
                'credit_card_instalment_pos/static/src/css/card_instalment.css',
                'credit_card_instalment_pos/static/src/xml/**/*',
                'credit_card_instalment_pos/static/src/js/card_instalment.js',
            ],
        },
    "qweb": [
        "static/src/xml/card_instalment.xml",
    ],
}
