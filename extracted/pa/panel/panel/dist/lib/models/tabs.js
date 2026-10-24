import * as tabs from "@bokehjs/styles/tabs.css";
import { Container } from "@bokehjs/core/layout/grid";
import { Location } from "@bokehjs/core/enums";
import { GridAlignmentLayout } from "@bokehjs/models/layouts/alignments";
import { Tabs as BkTabs, TabsView as BkTabsView } from "@bokehjs/models/layouts/tabs";
import { LayoutDOMView } from "@bokehjs/models/layouts/layout_dom";
function show(element) {
    element.style.visibility = "";
    element.style.opacity = "";
    element.style.pointerEvents = "auto";
    element.removeAttribute("aria-hidden");
}
function hide(element) {
    element.style.visibility = "hidden";
    element.style.opacity = "0";
    element.style.pointerEvents = "none";
    element.setAttribute("aria-hidden", "true");
}
export class TabsView extends BkTabsView {
    connect_signals() {
        super.connect_signals();
        let view = this;
        while (view != null) {
            if (view.model.type.endsWith("Tabs")) {
                view.connect(view.model.properties.active.change, () => this.update_active());
            }
            view = view.parent || view._parent; // Handle ReactiveHTML
        }
    }
    update_active() {
        super.update_active();
        this._update_child_visibility();
        this.update_zindex();
    }
    _active_child_view() {
        const tab = this.model.tabs[this.model.active];
        if (tab == null) {
            return undefined;
        }
        return this.child_views.find((child_view) => child_view.model == tab.child);
    }
    _update_child_visibility() {
        const { child_views } = this;
        for (const child_view of child_views) {
            if (child_view != null) {
                hide(child_view.el);
            }
        }
        const active = this._active_child_view();
        if (active != null) {
            show(active.el);
        }
    }
    get is_visible() {
        let parent = this.parent;
        let current_view = this;
        while (parent != null) {
            if (parent.model.type.endsWith("Tabs")) {
                if (parent._active_child_view() !== current_view) {
                    return false;
                }
            }
            current_view = parent;
            parent = parent.parent || parent._parent; // Handle ReactiveHTML
        }
        return true;
    }
    render() {
        super.render();
        this.update_zindex();
    }
    update_zindex() {
        const { child_views } = this;
        for (const child_view of child_views) {
            if (child_view != null && child_view.el != null) {
                child_view.el.style.zIndex = "";
            }
        }
        if (this.is_visible) {
            const active = this._active_child_view();
            if (active != null && active.el != null) {
                active.el.style.zIndex = "1";
            }
        }
    }
    _after_layout() {
        LayoutDOMView.prototype._after_layout.call(this);
        this._update_child_visibility();
    }
    _update_layout() {
        LayoutDOMView.prototype._update_layout.call(this);
        const loc = this.model.tabs_location;
        this.class_list.remove([...Location].map((loc) => tabs[loc]));
        this.class_list.add(tabs[loc]);
        const layoutable = new Container();
        for (const view of this.child_views) {
            if (view == undefined) {
                continue;
            }
            view.style.append(":host", { grid_area: "stack" });
            if (view instanceof LayoutDOMView && view.layout != null) {
                layoutable.add({ r0: 0, c0: 0, r1: 1, c1: 1 }, view);
            }
        }
        if (layoutable.size != 0) {
            this.layout = new GridAlignmentLayout(layoutable);
            this.layout.set_sizing();
        }
        else {
            delete this.layout;
        }
    }
}
export class Tabs extends BkTabs {
    static __module__ = "panel.models.tabs";
    static {
        this.prototype.default_view = TabsView;
    }
}
//# sourceMappingURL=tabs.js.map