from odoo import api, fields, models, tools, _


import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def create_from_ui(self, orders, draft=False):

        _logger.info(orders)
        return super().create_from_ui(orders, draft)

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        payment = super()._payment_fields(order, ui_paymentline)
        payment["instalment_id"] = ui_paymentline.get("instalment_id", False)
        payment["card_number"] = ui_paymentline.get("card_number", False)
        payment["tiket_number"] = ui_paymentline.get("tiket_number", False)
        payment["lot_number"] = ui_paymentline.get("lot_number", False)
        payment["fee"] = ui_paymentline.get("fee", False)
        return payment


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_pos_payment_method(self):
        return {
            'search_params': {
                'domain': [('card_id', '!=', False)],
                'fields': [
                    'card_id', 'instalment_ids', 'instalment_product_id',
                ],
            }
        }

    def _get_pos_ui_pos_payment_method_by_params(self, custom_search_params):
        """
        :param custom_search_params: a dictionary containing params of a search_read()
        """
        params = self._loader_params_pos_payment_method()
        # custom_search_params will take priority
        params['search_params'] = {**params['search_params'], **custom_search_params}
        payment = self.env['pos.payment.method'].search_read(**params['search_params'])
        return payment

    def _loader_params_account_card_instalment(self):
        return {
            'search_params': {
                'fields': [
                    'card_id', 'name', 'instalment', 'product_id', 'amount', 'coefficient', 'discount', 'bank_discount', 'active', 'card_type'
                ],
            }
        }

    def _get_pos_ui_account_card_instalment_by_params(self, custom_search_params):
        """
        :param custom_search_params: a dictionary containing params of a search_read()
        """
        params = self._loader_params_account_card_instalment()
        # custom_search_params will take priority
        params['search_params'] = {**params['search_params'], **custom_search_params}
        payment = self.env['account.card.instalment'].search_read(**params['search_params'])
        return payment




