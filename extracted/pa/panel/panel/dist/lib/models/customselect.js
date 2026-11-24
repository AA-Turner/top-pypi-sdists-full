import { Select, SelectView } from "@bokehjs/models/widgets/select";
export class CustomSelectView extends SelectView {
    connect_signals() {
        super.connect_signals();
        const { disabled_options } = this.model.properties;
        this.on_change(disabled_options, () => this._update_disabled_options());
    }
    options_el() {
        const opts = super.options_el();
        const elements = opts.flatMap((element) => element instanceof HTMLOptGroupElement
            ? Array.from(element.querySelectorAll("option")) : [element]);
        this._set_disabled_options(elements);
        return opts;
    }
    _update_disabled_options() {
        this._set_disabled_options(Array.from(this.input_el.options));
    }
    _set_disabled_options(elements) {
        const { options, disabled_options } = this.model;
        const values = Array.isArray(options) ? options : Object.values(options).flat();
        elements.forEach((element, index) => {
            const option = values[index];
            if (option === undefined) {
                return;
            }
            const value = typeof option === "string" ? option : option[0];
            element.disabled = disabled_options.includes(String(value));
        });
    }
}
export class CustomSelect extends Select {
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "panel.models.widgets";
    static {
        this.prototype.default_view = CustomSelectView;
        this.define(({ List, Str }) => {
            return {
                disabled_options: [List(Str), []],
            };
        });
    }
}
//# sourceMappingURL=customselect.js.map