# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Person (Aux) History (customizations for CLVhealth-JCAFB Solution)',
    'summary': 'Person (Aux) History Module customizations for CLVhealth-JCAFB Solution.',
    'version': '12.0.4.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_person_aux_history',
        'clv_person_aux_jcafb',
    ],
    'data': [
        'wizard/person_aux_event_setup_view.xml',
        'wizard/person_aux_document_setup_view.xml',
        'wizard/person_aux_lab_test_request_setup_view.xml',
    ],
    'demo': [],
    'test': [],
    'init_xml': [],
    'test': [],
    'update_xml': [],
    'installable': True,
    'application': False,
    'active': False,
    'css': [],
}
