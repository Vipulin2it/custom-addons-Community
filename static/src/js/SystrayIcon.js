/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, useState, onWillStart } = owl;

class EstateSystrayIcon extends Component {
    setup() {
        this.action = useService("action");
        this.orm = useService("orm"); // Use ORM service to fetch model data
        this.state = useState({ count: 0, latestId: null });

        onWillStart(async () => {
            await this._updateData();
        });
    }

    async _updateData() {
        // Fetch the count of "New" properties and the ID of the most 
        const domain = [['state', '=', 'new']];
        const records = await this.orm.searchRead("estate.property", domain, ["id"], { limit: 1, order: 'id desc' });
        this.state.count = await this.orm.searchCount("estate.property", domain);
        if (records.length > 0) {
            this.state.latestId = records[0].id;
        }
    }

    async _onClickNotification(ev) {
        if (this.state.latestId) {
            // 1. Open the Form View for the specific record
            await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "estate.property",
                res_id: this.state.latestId,
                views: [[false, "form"]],
                target: "current",
            });

            // 2. Mark as read visually (remove from bar count)
            // This satisfies your requirement: remove from bar but data remains in DB
            this.state.count = 0; 
        }
    }
}

EstateSystrayIcon.template = "estate_SystrayIcon";
export const systrayItem = { Component: EstateSystrayIcon };
registry.category("systray").add("EstateSystray", systrayItem, { sequence: 10 });
