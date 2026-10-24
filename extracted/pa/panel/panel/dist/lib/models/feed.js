var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var ScrollLatestEvent_1;
import { Column, ColumnView } from "./column";
import { ModelEvent, server_event } from "@bokehjs/core/bokeh_events";
import { build_views } from "@bokehjs/core/build_views";
import { ColumnView as BkColumnView } from "@bokehjs/models/layouts/column";
let ScrollLatestEvent = ScrollLatestEvent_1 = class ScrollLatestEvent extends ModelEvent {
    model;
    rerender;
    scroll_limit;
    constructor(model, rerender, scroll_limit) {
        super();
        this.model = model;
        this.rerender = rerender;
        this.scroll_limit = scroll_limit;
        this.origin = model;
        this.rerender = rerender;
        this.scroll_limit = scroll_limit;
    }
    get event_values() {
        return { model: this.origin, rerender: this.rerender, scroll_limit: this.scroll_limit };
    }
    static from_values(values) {
        const { model, rerender, scroll_limit } = values;
        return new ScrollLatestEvent_1(model, rerender, scroll_limit);
    }
};
ScrollLatestEvent = ScrollLatestEvent_1 = __decorate([
    server_event("scroll_latest_event")
], ScrollLatestEvent);
export { ScrollLatestEvent };
export class FeedView extends ColumnView {
    _intersection_observer;
    _visibility_pending = false;
    _visibility_listener = false;
    _latest_pending = false;
    _last_visible;
    _rendered = false;
    _sync;
    _reference = null;
    _reference_view = null;
    _children_update = null;
    _latest_scroll_pending = false;
    _latest_last = null;
    initialize() {
        super.initialize();
        this._sync = true;
        // A Feed that does not clip lets an ancestor scroll, and rooting on it
        // would report every child visible until all objects load (#8661).
        const is_scroll_container = this.is_scroll_container;
        const root = is_scroll_container ? this.el : null;
        this._intersection_observer = new IntersectionObserver((entries) => {
            // Until its stylesheets load the Feed does not clip, so all children intersect.
            // Before the initial scroll to the latest child the top children are
            // visible; reporting them makes the server load the wrong range.
            if (this._latest_pending || (is_scroll_container && getComputedStyle(this.el).overflowY === "visible")) {
                this._visibility_pending = true;
                return;
            }
            const visible = [...this.model.visible_children];
            const nodes = this.node_map;
            for (const entry of entries) {
                const id = nodes.get(entry.target)?.id;
                if (entry.isIntersecting) {
                    if (!visible.includes(id)) {
                        visible.push(id);
                    }
                }
                else if (visible.includes(id)) {
                    visible.splice(visible.indexOf(id), 1);
                }
            }
            if (this._sync) {
                this.model.visible_children = visible;
            }
            if (visible.length > 0) {
                const refs = this.child_models.map((model) => model.id);
                const indices = visible.map((ref) => refs.indexOf(ref));
                this._last_visible = this.child_views[Math.min(...indices)];
            }
            else {
                this._last_visible = null;
            }
        }, {
            root,
            threshold: 0.01,
        });
    }
    connect_signals() {
        super.connect_signals();
        this.model.on_event(ScrollLatestEvent, async (event) => {
            if (event.rerender) {
                this._rendered = false;
            }
            const limit = event.scroll_limit;
            if (limit != null && this.distance_from_latest > limit) {
                return;
            }
            if (event.rerender) {
                // The children it rerendered may not have arrived yet
                this._latest_scroll_pending = true;
                this._latest_last = null;
            }
            // Until the scroll lands, the children at the old position report as
            // visible and make the server load that range again.
            this._latest_pending = this.is_scroll_container;
            await this._children_update;
            this._scroll_to_latest_children();
        });
    }
    get node_map() {
        const nodes = new Map();
        for (const view of this.child_views) {
            nodes.set(view.el, view.model);
        }
        return nodes;
    }
    async update_children() {
        const at_latest = this.distance_from_latest <= 1;
        const update = this._rebuild_children();
        this._children_update = update;
        try {
            await update;
        }
        finally {
            if (this._children_update === update) {
                this._children_update = null;
            }
        }
        if (this._latest_scroll_pending) {
            // The server may still answer with another window
            const last = this.child_views.at(-1)?.model.id ?? null;
            this._latest_scroll_pending = last !== this._latest_last;
            this._latest_last = last;
            this._scroll_to_latest_children();
        }
        else if (at_latest && this.distance_from_latest > 1) {
            // A rebuild can grow the children below a Feed at its latest one
            this.scroll_to_latest();
        }
    }
    _scroll_to_latest_children() {
        // A Feed that cannot scroll yet reports nothing, so leave the retry to
        // scroll_position rather than holding the visibility.
        if (!this._latest_pending || !this._land_latest_scroll()) {
            this._latest_pending = false;
            this._reobserve_children();
            this.scroll_to_latest();
        }
    }
    async _rebuild_children() {
        const last = this._last_visible;
        const scroll_top = this.el.scrollTop;
        this._reference_view = last;
        this._reference = last?.el.offsetTop || 0;
        this._sync = false;
        const created = await this.build_child_views();
        const created_children = new Set(created);
        const createdLength = created.length;
        const views_length = this.child_views.length;
        // Check whether we simply have to prepend or append items
        // instead of removing and reordering them
        const is_prepended = created.every((view, index) => view === this.child_views[index]);
        const is_appended = created.every((view, index) => view === this.child_views[views_length - createdLength + index]);
        const reorder = !(is_prepended || is_appended);
        if (reorder) {
            // First remove and then either reattach existing elements or render and
            // attach new elements, so that the order of children is consistent, while
            // avoiding expensive re-rendering of existing views.
            for (const child_view of this.child_views) {
                child_view.el.remove();
            }
        }
        const prepend = [];
        for (const child_view of this.child_views) {
            const is_new = created_children.has(child_view);
            const target = this.shadow_el;
            if (reorder) {
                if (is_new) {
                    child_view.render_to(target);
                }
                else {
                    target.append(child_view.el);
                }
            }
            else {
                if (is_new) {
                    child_view.render();
                    child_view.r_after_render();
                    if (is_appended) {
                        target.append(child_view.el);
                    }
                    else if (is_prepended) {
                        prepend.push(child_view.el);
                    }
                }
            }
        }
        if (is_prepended) {
            this.shadow_el.prepend(...prepend);
        }
        this.r_after_render();
        this._update_children();
        this.invalidate_layout();
        this._sync = true;
        // Ensure we adjust the scroll position in case we prepended items
        // The reference child may have been removed, its offset is then meaningless.
        const reference = this._reference_view;
        const reference_top = this._reference || 0;
        if (is_prepended && reference != null && this.child_views.includes(reference)) {
            requestAnimationFrame(() => {
                const offset = reference.el.offsetTop - reference_top;
                // A scroll to where it already is would cancel one in progress.
                if (offset !== 0) {
                    this.el.scrollTo({ top: scroll_top + offset, behavior: "smooth" });
                }
            });
        }
    }
    async build_child_views() {
        const { created, removed } = await build_views(this._child_views, this.child_models, { parent: this });
        const visible = this.model.visible_children;
        for (const view of removed) {
            if (visible.includes(view.model.id)) {
                visible.splice(visible.indexOf(view.model.id), 1);
            }
            this._resize_observer.unobserve(view.el);
            this._intersection_observer.unobserve(view.el);
        }
        this.model.visible_children = [...visible];
        for (const view of created) {
            this._resize_observer.observe(view.el, { box: "border-box" });
            this._intersection_observer.observe(view.el);
        }
        return created;
    }
    _update_layout() {
        super._update_layout();
        this.style.append(":host > div", { max_height: "unset" });
    }
    render() {
        this._rendered = false;
        this._latest_pending = this.model.view_latest && this.is_scroll_container;
        super.render();
        if (!this._visibility_listener) {
            this._visibility_listener = true;
            this.shadow_el.addEventListener("load", (event) => {
                if (!(event.target instanceof HTMLLinkElement)) {
                    return;
                }
                if (this._latest_pending) {
                    this._land_latest_scroll();
                }
                else {
                    this._reobserve_children();
                }
            }, true);
        }
    }
    _reobserve_children() {
        if (!this._visibility_pending || getComputedStyle(this.el).overflowY === "visible") {
            return;
        }
        this._visibility_pending = false;
        // An observed child is only reported again once its intersection changes.
        for (const view of this.child_views) {
            this._intersection_observer.unobserve(view.el);
            this._intersection_observer.observe(view.el);
        }
    }
    trigger_auto_scroll() { }
    _land_latest_scroll() {
        // Scroll now rather than frames later via scroll_position, so the
        // children are measured at the latest position.
        this.el.scrollTo({ top: this.el.scrollHeight, behavior: "instant" });
        // Until its stylesheets load the scroll is a no-op, so keep waiting.
        if (getComputedStyle(this.el).overflowY === "visible") {
            return false;
        }
        this._latest_pending = false;
        this._reobserve_children();
        return true;
    }
    after_render() {
        BkColumnView.prototype.after_render.call(this);
        requestAnimationFrame(() => {
            if (this.model.view_latest && !this._rendered) {
                this._land_latest_scroll();
                this.scroll_to_latest();
            }
            else if (this.model.scroll_position) {
                this.scroll_to_position();
            }
            this.toggle_scroll_button();
            this._rendered = true;
        });
    }
}
export class Feed extends Column {
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "panel.models.feed";
    static {
        this.prototype.default_view = FeedView;
        this.define(({ List, Str }) => ({
            visible_children: [List(Str), []],
        }));
    }
}
//# sourceMappingURL=feed.js.map