odoo.define("nao_menu.home_donation", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    // var wSaleUtils = require("website_sale.utils");
    var config = require("web.config");
    var {_t} = require("web.core");
    var Session = require('web.Session');

    publicWidget.registry.HomeDonations = publicWidget.Widget.extend({
        selector: ".js_reservation",
        events: {
            "click .__check_code": "_onClickCheckCode",
            "click .btn-donation-type:not(.active)": "_onClickDonationType",
            "click .btn-donation-price:not(.active)": "_onClickDonationPrice",
            "click .btn-donation-do": "_onClickDonationDo",
            "keypress .only_numbers": "_onlyNumbers",
            "input .js_donation_amount": "_checkAmount",
        },

        init: function (url, pos) {
            this._super.apply(this, arguments);
        
            this.connection = new Session(undefined, 'http://localhost:8064', { use_cors: false});
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * Product list
         */
        _onClickCheckCode(ev) {
            var $currentButton = $(ev.currentTarget);
            var code = this.$('form #code').val();

            if (!code.trim()) {
                return this. do_notify('Validación', "Ingresa un codigo", false, "");
            }

            this._rpc({
                route: "https://0kcqfphjm9.execute-api.us-east-2.amazonaws.com/Demo/usuarios",
                params: {code},
            }).then((data) => {
                if (data.error)
                    return this. do_notify('Error', data.error, false, "");
            });



        },
    });

    return publicWidget.registry.HomeDonations;
});
