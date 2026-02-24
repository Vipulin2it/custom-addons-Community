/** @odoo-module **/

import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";
import { registry } from "@web/core/registry";
import { formatSelection } from "@web/views/fields/formatters";

export class Customtrial extends StateSelectionField {
    setup() {
        super.setup();

        this.icons = {
            vipul: "fa fa-circle-o",
            sachin: "o_status",
            rahul: "fa fa-exclamation-circle",
            rohit: "o_status o_status_green",
            suresh: "fa fa-check-circle",
        };

        this.colors = {
            vipul: "text-info",
            sachin: "text-primary",
            rahul: "text-warning",
            rohit: "text-success",
            suresh: "text-danger",
        };

        this.buttonColors = {
            vipul: "btn-outline-info",
            sachin: "btn-outline-primary",
            rahul: "btn-outline-warning",
            rohit: "btn-outline-success",
            suresh: "btn-outline-danger",
        };
    }

    get label() {
        return formatSelection(this.currentValue, {
            selection: this.options,
        });
    }

    stateIcon(value) {
        return this.icons[value] || "";
    }

    statusColor(value) {
        return this.colors[value] || "";
    }

    getTogglerClass(value) {
        return `o_state_button btn rounded-pill ${this.buttonColors[value]}`;
    }
}

Customtrial.template = "CustomtrialTemplate";

export const custom_trial = {
    ...stateSelectionField,
    component: Customtrial,
};

registry.category("fields").add("custom_trial", custom_trial);