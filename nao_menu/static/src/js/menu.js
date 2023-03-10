odoo.define("nao_menu.home_donation", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    // var wSaleUtils = require("website_sale.utils");
    var config = require("web.config");
    var {_t, qweb} = require("web.core");
    var Session = require('web.Session');

    publicWidget.registry.HomeDonations = publicWidget.Widget.extend({
        selector: ".js_reservation",
        xmlDependencies: ["/nao_menu/static/src/xml/menu.xml"],
        events: {
            "click .__check_code": "_onClickCheckCode",
            "click .__set_menu": "_onClickSetMenu",
        },

        init: function (url, pos) {
            this._super.apply(this, arguments);
            this.__user = null;
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
            let body = this.$('.js_menus');
            let btton = this.$('.__check_code');

            if (!code.trim()) {
                return this. do_notify('Validación', "Ingresa un codigo", false, "");
            }

            this._rpc({
                route: "https://0kcqfphjm9.execute-api.us-east-2.amazonaws.com/Demo/usuarios",
                params: {code},
            }).then((data) => {
                if (data.error){
                    body.html("");
                    return this. do_notify('Error', data.error, false, "");
                }
                
                let menus = $(qweb.render('nao_menu.menu',{
                    platos: data.platos,
                    employee_id: data.empleado,
                }));

                body.html(menus);
                btton.hide();
                this.$('.__set_menu').removeClass("d-none");
            });
        },
        _onClickSetMenu(ev) {
            $(ev.currentTarget).attr('disabled', true);
            var $menu_form = this.$(".js_menus input:checked");
            var platos = this.getFormData($menu_form);
            if (_.isEmpty(platos))
                return this. do_notify('Error', "Selecciona un plato", false, "");

            this._rpc({
                route: "https://0kcqfphjm9.execute-api.us-east-2.amazonaws.com/Demo/menu",
                // route: "/test2",
                params: {platos},
            }).then((data) => {
                return this. do_notify('Existo', "Reservación de menús exitosa desde " + data.platform, false, "");
            });
                
        },
        getFormData($inputs) {
            let indexed_array = []
            $inputs.each(function( index ) {
              console.log( index + ": " + $( this ).text() );
              indexed_array.push({
                employee_id: $( this ).data('employee_id'),
                plate_id: $( this ).data('plate_id')
              });
            });
            return indexed_array;
        },
    });

    return publicWidget.registry.HomeDonations;
});
