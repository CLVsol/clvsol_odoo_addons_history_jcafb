# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PersonAuxEventSetUp(models.TransientModel):
    _inherit = 'clv.person_aux.event_setup'

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

    @api.multi
    def do_person_aux_event_setup(self):
        self.ensure_one()

        # super().do_person_aux_event_setup()

        EventAttendee = self.env['clv.event.attendee']

        Document = self.env['clv.document']
        DocumentType = self.env['clv.document.type']

        LabTestRequest = self.env['clv.lab_test.request']

        for person_aux in self.person_aux_ids:

            ref_id = person_aux._name + ',' + str(person_aux.id)

            _logger.info(u'%s %s %s', '>>>>>', person_aux.name, ref_id)

            for event in self.event_ids:

                _logger.info(u'%s %s', '>>>>>>>>>>', event.name)

                event_attendee = EventAttendee.search([
                    ('event_id', '=', event.id),
                    ('ref_id', '=', ref_id),
                ])

                if event_attendee.id is False:

                    values = {
                        'event_id': event.id,
                        'ref_id': ref_id,
                    }
                    new_event_attendee = EventAttendee.create(values)

                    _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', new_event_attendee.event_id.name)

            for document_type in self.document_type_ids:

                _logger.info(u'%s %s', '>>>>>>>>>>', document_type.name)

                document = Document.search([
                    ('document_type_id', '=', document_type.id),
                    ('ref_id', '=', ref_id),
                ])

                if document.id is False:

                    values = {
                        'name': document_type.name,
                        'code_sequence': 'clv.document.code',
                        'date_foreseen': self.date_foreseen,
                        'date_deadline': self.date_deadline,
                        'survey_id': document_type.survey_id.id,
                        # 'category_id': self.category_id.id,
                        'ref_id': ref_id,
                        'phase_id': self.phase_id.id,
                    }
                    new_document = Document.create(values)

                    if self.category_id.id is not False:

                        values = {
                            'category_ids': [(4, self.category_id.id)],
                        }
                        new_document.write(values)

                    else:

                        for category_id in document_type.category_ids:

                            values = {
                                'category_ids': [(4, category_id.id)],
                            }

                        new_document.write(values)

                    document_type = DocumentType.search([
                        ('code', '=', new_document.survey_id.code),
                    ])

                    document_type_id = False
                    if document_type.id is not False:
                        document_type_id = document_type.id

                    values = {
                        'document_type_id': document_type_id,
                    }
                    new_document.write(values)

                    _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', new_document.name)

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
