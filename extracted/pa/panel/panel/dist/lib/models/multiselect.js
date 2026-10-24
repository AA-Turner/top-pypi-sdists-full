import { MultiSelect, MultiSelectView } from "@bokehjs/models/widgets/multiselect";
import { ModelEvent } from "@bokehjs/core/bokeh_events";
export class DoubleClickEvent extends ModelEvent {
    option;
    constructor(option) {
        super();
        this.option = option;
    }
    get event_values() {
        return { model: this.origin, option: this.option };
    }
    static {
        this.prototype.event_name = "dblclick_event";
    }
}
export class CustomMultiSelectView extends MultiSelectView {
    render() {
        super.render();
        for (const option of this.input_el.children) {
            option.addEventListener("dblclick", (event) => {
                if (event.target) {
                    this.model.trigger_event(new DoubleClickEvent(event.target.value));
                }
            });
        }
    }
}
export class CustomMultiSelect extends MultiSelect {
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "panel.models.widgets";
    static {
        this.prototype.default_view = CustomMultiSelectView;
    }
}
//# sourceMappingURL=multiselect.js.map