/** @odoo-module **/

import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";
import { registry } from "@web/core/registry";
import { formatSelection } from "@web/views/fields/formatters";

export class OfferStateSelection extends StateSelectionField {

    setup() {
        super.setup();

        // icons per state
        this.icons = {
            new: "fa fa-circle-o",
            in_progress: "o_status",
            changes_requested: "fa fa-exclamation-circle",
            approved: "o_status o_status_green",
            done: "fa fa-check-circle",
            cancel: "fa fa-times-circle",
        };

        // colors
        this.colors = {
            new: "text-secondary",
            in_progress: "",
            changes_requested: "text-warning",
            approved: "text-success",
            done: "text-success",
            cancel: "text-danger",
        };

        // button styles
        this.buttonColors = {
            new: "btn-outline-secondary",
            in_progress: "btn-outline-primary",
            changes_requested: "btn-outline-warning",
            approved: "btn-outline-success",
            done: "btn-outline-success",
            cancel: "btn-outline-danger",
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

OfferStateSelection.template = "offer.OfferStateSelection";

export const offerStateSelection = {
    ...stateSelectionField,
    component: OfferStateSelection,
};

registry.category("fields").add(
    "offer_state_selection",
    offerStateSelection
);