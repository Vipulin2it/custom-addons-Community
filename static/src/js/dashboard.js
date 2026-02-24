/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Card, TODOCard } from "./card.js";

/* -------- CHILD COMPONENT -------- */
export class CounterDisplay extends Component {
    static template = "CounterDisplayTemplate";
    static props = {
        counter1: { type: Number },
        counter2: { type: Number },
    };
}

/* -------- PARENT COMPONENT -------- */
export class Dashboard extends Component {
    static template = "DashboardTemplate";
    static components = { CounterDisplay, Card, TODOCard };

    static props = {
        counter: { type: Number, optional: true },
    };

    setup() {
        this.state = useState({
            counter1: this.props.counter || 0,
            counter2: this.props.counter || 0,

            Todo: [
                { id: 1, name: "Learn OWL", iscomplete: false },
                { id: 2, name: "Build an Odoo App", iscomplete: false },
            ],
        });
        this.updateParentCount = this.updateParentCount.bind(this);

        this.htmlContent = markup(
            '<span class="badge bg-success">Active</span> <strong>verified</strong>'
        );

        this.unsafeContent = "<b>This will look like text, not bold</b>";
    }

    incrementCounter1() {
        this.state.counter1++;
    }

    decrementCounter1() {
        this.state.counter1--;
    }

    incrementCounter2() {
        this.state.counter2++;
    }

    decrementCounter2() {
        this.state.counter2--;
    }

    updateParentCount() {
        this.state.counter1 += 100;
    }

    getSum() {
        return this.state.counter1 + this.state.counter2;
    }
}

registry.category("actions").add("Dashboard", Dashboard);