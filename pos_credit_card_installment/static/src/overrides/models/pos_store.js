/** @odoo-module */

/*
 * Copyright (C) 2024 Axcelere.
 * Licensed under the GPL-3.0 License or later.
 */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {

    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.installment_id = this.installment_id || options.installment_id;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.installment_id = json.installment_id;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.installment_id = this.installment_id;
        return json;
    },
});

patch(PosStore.prototype, {

    async _processData(loadedData) {
        console.log('_processData')
        await super._processData(...arguments);
        this.account_card_installment = loadedData["account.card.installment"];
    },

    async send_payway() {
    },

    captureChange(event) {
        const order = this.pos.get_order();
        const selectedInstallmentId = parseInt(event.target.value);  // Asegúrate de que sea un entero
        const selectedInstallment = this.pos.account_card_installment.find(inst => inst.id === selectedInstallmentId);

        if (selectedInstallment) {
            order.selected_paymentline.installment_id = selectedInstallment.id;  // Guarda el ID en la línea de pago seleccionada
            this.pos.installment_id = selectedInstallment.id;  // Actualiza el valor de `installment` en `this.pos`
            this.pos.surcharge_coefficient = selectedInstallment.surcharge_coefficient;  // Actualiza el surcharge coefficient
        }
        console.log('Installment selected:', this.pos.installment_id);
    },
});