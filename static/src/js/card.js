/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "CardTemplate";
    static props = {
        title: { type: String },
        content: { type: String },
        optionalContent: { type: String, optional: true },
        onButtonClick: { type: Function, optional: true },
    };
}

export class TODOCard extends Component {
    static template = "TODOCardTemplate";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                name: String,
                iscomplete: Boolean,
            },
        },
    };
}