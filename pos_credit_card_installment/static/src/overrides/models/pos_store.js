/** @odoo-module */

/*
 * Copyright (C) 2024 Axcelere.
 * Licensed under the GPL-3.0 License or later.
 */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
// import { Order } from "@point_of_sale/app/store/models";

// patch(Order.prototype, {
//
//     setup(order) {
//         super.setup(...arguments);
//         this.installment_id = order.installment_id;
//     },
// });

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

    // async _flush_orders(orders, options = {}) {
    //     console.log('_flush_orders', orders);
    //     console.log(orders[0][0]['data']);
    //     try {
    //         const server_ids = await this._save_to_server(orders, options);
    //         for (let i = 0; i < server_ids.length; i++) {
    //             this.validated_orders_name_server_id_map[server_ids[i].pos_reference] =
    //                 server_ids[i].id;
    //         }
    //         return server_ids;
    //     } catch (error) {
    //         if (!(error instanceof ConnectionLostError) && !options.printedOrders) {
    //             for (const order of orders) {
    //                 const reactiveOrder = this.orders.find((o) => o.uid === order.id);
    //                 reactiveOrder.finalized = false;
    //                 this.db.remove_order(reactiveOrder.uid);
    //                 this.db.save_unpaid_order(reactiveOrder);
    //             }
    //             this.set_synch("connected");
    //         }
    //         throw error;
    //     } finally {
    //         this._after_flush_orders(orders);
    //     }
    // },

    async _save_to_server(orders, options) {
        if (!orders || !orders.length) {
            return Promise.resolve([]);
        }
        this.set_synch("connecting", orders.length);
        options = options || {};

        // Keep the order ids that are about to be sent to the
        // backend. In between create_from_ui and the success callback
        // new orders may have been added to it.
        var order_ids_to_sync = orders.map((o) => o.id);


        for (const order of orders) {
            console.log("AQUI OBTENGO LA ORDEN ANTES DE")
            // const installment = this.env.pos.installment
            console.log(order)
            console.log('ADD INSTALLMENT')
            // console.log(installment)
            // order['']
            //  console.log('ADD INSTALLMENT')
            // console.log(order[0][0])
            order.to_invoice = options.to_invoice || false;
            order['data']['installment'] = '1'
            // order.installment = this.pos.installment || false;
        }
        // we try to send the order. silent prevents a spinner if it takes too long. (unless we are sending an invoice,
        // then we want to notify the user that we are waiting on something )
        const orm = options.to_invoice ? this.orm : this.orm.silent;
        console.log("Testing")
        console.log(orders)
        console.log(options)

        try {
            // FIXME POSREF timeout
            // const timeout = typeof options.timeout === "number" ? options.timeout : 30000 * orders.length;
            const serverIds = await orm.call(
                "pos.order",
                "create_from_ui",
                [orders, options.draft || false],
                {
                    context: this._getCreateOrderContext(orders, options),
                }
            );

            for (const serverId of serverIds) {
                const order = this.env.services.pos.orders.find(
                    (order) => order.name === serverId.pos_reference
                );

                if (order) {
                    order.server_id = serverId.id;
                }
            }

            for (const order_id of order_ids_to_sync) {
                this.db.remove_order(order_id);
            }

            this.failed = false;
            this.set_synch("connected");
            return serverIds;
        } catch (error) {
            console.warn("Failed to send orders:", orders);
            if (error.code === 200) {
                // Business Logic Error, not a connection problem
                // Hide error if already shown before ...
                if ((!this.failed || options.show_error) && !options.to_invoice) {
                    this.failed = error;
                    this.set_synch("error");
                    throw error;
                }
            }
            this.set_synch("disconnected");
            throw error;
        }
    }
});