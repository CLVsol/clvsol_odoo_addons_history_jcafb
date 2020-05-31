# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonAuxLabTestRequestSetup(models.TransientModel):
    _inherit = 'clv.person_aux.lab_test.request.setup'

    def _default_phase_id(self):
        phase_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip())
        return phase_id
    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        default=_default_phase_id,
        ondelete='restrict'
    )

    # @api.multi
    def do_person_aux_lab_test_request_setup(self):
        self.ensure_one()

        # super().do_person_aux_lab_test_request_setup()

        LabTestRequest = self.env['clv.lab_test.request']

        for person_aux in self.person_aux_ids:

            _logger.info(u'%s %s', '>>>>>', person_aux.name)

            for lab_test_type in self.lab_test_type_ids:
                m2m_list = []
                m2m_list.append((4, lab_test_type.id))

                ref_id = person_aux._name + ',' + str(person_aux.id)

                _logger.info(u'%s %s %s', '>>>>>>>>>>', ref_id, m2m_list)

                values = {
                    'code_sequence': 'clv.lab_test.request.code',
                    'lab_test_type_ids': m2m_list,
                    'ref_id': ref_id,
                    'phase_id': self.phase_id.id,
                }
                lab_test_request = LabTestRequest.create(values)

                _logger.info(u'%s %s', '>>>>>>>>>>', lab_test_request.code)

        return True
