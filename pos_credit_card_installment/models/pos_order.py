from odoo import api, fields, models, tools, _

import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    # @api.model
    # def create_from_ui(self, orders, draft=False):
    #     _logger.info(orders)
    #     installment_id = self.env['account.card.installment'].search([('id', '=', orders[0]['data']['installment'])])
    #     ctx = dict(self.env.context or {})
    #     ctx.update({'installment_id': installment_id})
    #     return super(PosOrder, self.with_context(ctx)).create_from_ui(orders, draft)

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        payment = super()._payment_fields(order, ui_paymentline)
        payment["instalment_id"] = ui_paymentline.get("instalment_id", False)
        payment["card_number"] = ui_paymentline.get("card_number", False)
        payment["tiket_number"] = ui_paymentline.get("tiket_number", False)
        payment["lot_number"] = ui_paymentline.get("lot_number", False)
        payment["fee"] = ui_paymentline.get("fee", False)
        return payment

    @api.model
    def _process_order(self, order, draft, existing_order):
        res = super(PosOrder, self)._process_order(order, draft, existing_order)
        return res
        # order_id = self.env['pos.order'].search([('id', '=', res)])
        # payment_method_id = order['data']['statement_ids'][0][2]['payment_method_id']
        # installment_id = self.env['account.card.installment'].search([('id', '=', order['data']['installment'])])
        # if installment_id and installment_id.surcharge_coefficient:
        #     surcharge_coefficient = order['data']['amount_total'] * installment_id.surcharge_coefficient
        #     payment_id = self.env['pos.make.payment'].with_context(active_id=order_id.id).create({'amount':surcharge_coefficient, 'payment_method_id': payment_method_id})
        #     payment_id.check()
        # return res

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        return res
        # installment_id = self.env['account.card.installment'].search([('id', '=', ui_order['installment'])])
        # if installment_id and installment_id.surcharge_coefficient:
        #     surcharge_coefficient = res['amount_total'] * installment_id.surcharge_coefficient
        #     product_id = self.env['product.product'].search([('is_financial_charge', '=', True)])
        #     pos_session_id = self.env['pos.session'].search([('id', '=', ui_order['pos_session_id'])])
        #     res['amount_total'] += surcharge_coefficient
        #     res['amount_paid'] += surcharge_coefficient
        #     res['lines'].append((0, 0, {
        #         'name': pos_session_id.name,
        #         'full_product_name': product_id.name,
        #         'price_unit': surcharge_coefficient,
        #         'product_id': product_id.id,
        #         'qty': 1,
        #         'discount': 0,
        #         'price_extra': 1,
        #         'price_subtotal': surcharge_coefficient,
        #         'price_subtotal_incl': surcharge_coefficient,
        #         'tax_ids': [],
        #         'pack_lot_ids': [],
        #     }))
        # return res