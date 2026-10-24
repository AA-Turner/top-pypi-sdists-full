var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var ESMEvent_1;
import { transform } from "sucrase";
import { ModelEvent, server_event } from "@bokehjs/core/bokeh_events";
import { div } from "@bokehjs/core/dom";
import { ImportedStyleSheet } from "@bokehjs/core/dom";
import { DOMView } from "@bokehjs/core/dom_view";
import { Enum } from "@bokehjs/core/kinds";
import { LayoutDOMView } from "@bokehjs/models/layouts/layout_dom";
import { isArray } from "@bokehjs/core/util/types";
import { UIElementView } from "@bokehjs/models/ui/ui_element";
import { serializeEvent } from "./event-to-object";
import { DOMEvent } from "./html";
import { HTMLBox, HTMLBoxView, rerender_view, set_size } from "./layout";
import { resource_url, resources } from "./resources";
import { convertUndefined, formatError } from "./util";
import esm_css from "styles/models/esm.css";
// Deliberately module local rather than on the shared resource registry:
// its keys are logical (class name plus source length), so two Panel
// versions on one page must not be able to satisfy each other from it.
const MODULE_CACHE = new Map();
// Transpiled source by model type and module cache key, so instances of one
// component class do not each run sucrase over the same source.
const COMPILE_CACHE = new Map();
// Interns ESM sources so cache keys stay short and cannot collide, unlike
// keys derived from the source length.
const SOURCE_IDS = new Map();
const DECLARED_IMPORTMAPS = new Set();
function source_id(source) {
    let id = SOURCE_IDS.get(source);
    if (id === undefined) {
        id = SOURCE_IDS.size;
        SOURCE_IDS.set(source, id);
    }
    return id;
}
export class DataEvent extends ModelEvent {
    data;
    constructor(data) {
        super();
        this.data = data;
    }
    get event_values() {
        return { model: this.origin, data: this.data };
    }
    static {
        this.prototype.event_name = "data_event";
    }
}
let ESMEvent = ESMEvent_1 = class ESMEvent extends DataEvent {
    static from_values(values) {
        const { model, data } = values;
        const event = new ESMEvent_1(data);
        event.origin = model;
        return event;
    }
};
ESMEvent = ESMEvent_1 = __decorate([
    server_event("esm_event")
], ESMEvent);
export { ESMEvent };
const PROXY_METHODS = new Set(["get_child", "send_msg", "send_event", "off", "on"]);
export function model_getter(target, name) {
    const model = target.model;
    if (PROXY_METHODS.has(name)) {
        // Cached so the methods are stable across accesses, e.g. as hook
        // dependencies, instead of a new closure per property read.
        let method = target._proxy_methods.get(name);
        if (method === undefined) {
            method = proxy_method(target, name);
            target._proxy_methods.set(name, method);
        }
        return method;
    }
    else if (Reflect.has(model.data, name)) {
        if (name in model.data.attributes && !target.accessed_properties.includes(name)) {
            target.accessed_properties.push(name);
        }
        return Reflect.get(model.data, name);
    }
    else if (Reflect.has(model, name)) {
        return Reflect.get(model, name);
    }
    return undefined;
}
function proxy_method(target, name) {
    const model = target.model;
    if (name === "get_child") {
        return (child) => {
            if (!target.accessed_children.includes(child)) {
                target.accessed_children.push(child);
            }
            const child_model = model.data[child];
            if (isArray(child_model)) {
                const children = [];
                for (const subchild of child_model) {
                    children.push(target.get_child_view(subchild)?.el);
                }
                return children;
            }
            else if (model != null) {
                return target.get_child_view(child_model)?.el;
            }
            return null;
        };
    }
    else if (name === "send_msg") {
        return (data) => {
            model.trigger_event(new DataEvent(data));
        };
    }
    else if (name === "send_event") {
        return (name, event) => {
            const serialized = convertUndefined(serializeEvent(event));
            model.trigger_event(new DOMEvent(name, serialized));
        };
    }
    else if (name === "off") {
        return (prop, callback) => {
            const props = isArray(prop) ? prop : [prop];
            for (let p of props) {
                if (p.startsWith("change:")) {
                    p = p.slice("change:".length);
                }
                if (p in model.attributes || p.split(".")[0] in model.data.attributes) {
                    model.unwatch(target, p, callback);
                    continue;
                }
                else if (p === "msg:custom") {
                    target.remove_on_event(callback);
                    continue;
                }
                if (p.startsWith("lifecycle:")) {
                    p = p.slice("lifecycle:".length);
                }
                if (target._lifecycle_handlers.has(p)) {
                    const handlers = target._lifecycle_handlers.get(p);
                    if (handlers && handlers.includes(callback)) {
                        target._lifecycle_handlers.set(p, handlers.filter(v => v !== callback));
                    }
                    continue;
                }
                console.warn(`Could not unregister callback for event type '${p}'`);
            }
        };
    }
    else if (name === "on") {
        return (prop, callback, force = false) => {
            const props = isArray(prop) ? prop : [prop];
            for (let p of props) {
                if (p.startsWith("change:")) {
                    p = p.slice("change:".length);
                }
                if (p in model.attributes || p.split(".")[0] in model.data.attributes) {
                    model.watch(target, p, callback, force);
                    continue;
                }
                else if (p === "msg:custom") {
                    target.on_event(callback);
                    continue;
                }
                if (p.startsWith("lifecycle:")) {
                    p = p.slice("lifecycle:".length);
                }
                if (target._lifecycle_handlers.has(p)) {
                    (target._lifecycle_handlers.get(p) || []).push(callback);
                    continue;
                }
                console.warn(`Could not register callback for event type '${p}'`);
            }
        };
    }
    throw new Error(`unknown proxy method '${name}'`);
}
export function model_setter(target, name, value) {
    const model = target.model;
    if (Reflect.has(model.data, name)) {
        return Reflect.set(model.data, name, value);
    }
    else if (Reflect.has(model, name)) {
        return Reflect.set(model, name, value);
    }
    return false;
}
function init_model_getter(target, name) {
    if (Reflect.has(target.data, name)) {
        return Reflect.get(target.data, name);
    }
    else if (Reflect.has(target, name)) {
        return Reflect.get(target, name);
    }
}
function init_model_setter(target, name, value) {
    if (Reflect.has(target.data, name)) {
        return Reflect.set(target.data, name, value);
    }
    else if (Reflect.has(target, name)) {
        return Reflect.set(target, name, value);
    }
    return false;
}
function render_esm_view(view) {
    if (view.is_destroyed) {
        return;
    }
    const output = view.render_fn({
        view, model: view.model_proxy, data: view.model.data, el: view.container,
    });
    Promise.resolve(output).then((out) => {
        if (out instanceof Element) {
            view.container.replaceChildren(out);
        }
        view.after_rendered();
    });
}
// Resolved values of render module promises, so a view whose module has
// already loaded can render synchronously instead of a microtask later.
const RESOLVED_MODULES = new WeakMap();
function track_module(module) {
    module.then((value) => RESOLVED_MODULES.set(module, value), () => { });
    return module;
}
const ESM_RENDER_MODULE = track_module(Promise.resolve({ default: { render: render_esm_view } }));
const PENDING_FINISHED = new Set();
export class ReactiveESMView extends HTMLBoxView {
    container;
    accessed_properties = [];
    accessed_children = [];
    compiled_module = null;
    model_proxy;
    _child_callbacks;
    _child_rendered = new Map();
    _event_handlers = [];
    _lifecycle_handlers = new Map([
        ["update_layout", []],
        ["after_layout", []],
        ["after_render", []],
        ["resize", []],
        ["remove", []],
        ["mounted", []],
    ]);
    _module_cache;
    _rendered = false;
    _stale_children = false;
    _mounted = new Map();
    _update_children_chain = Promise.resolve();
    _layout_pending = false;
    _proxy_methods = new Map();
    _last_size = null;
    initialize() {
        super.initialize();
        this._module_cache = MODULE_CACHE;
        this._child_callbacks = new Map();
        this.model_proxy = new Proxy(this, {
            get: model_getter,
            set: model_setter,
        });
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        this.compiled_module = await this.model.compiled_module;
    }
    stylesheets() {
        const stylesheets = super.stylesheets();
        stylesheets.push(esm_css);
        if (this.model.css_bundle) {
            if (this.model.bundle === "url") {
                stylesheets.push(new ImportedStyleSheet(resource_url(this.model.css_bundle)));
            }
            else {
                stylesheets.push(this.model.css_bundle);
            }
        }
        return stylesheets;
    }
    connect_signals() {
        super.connect_signals();
        const { esm, importmap, class_name } = this.model.properties;
        this.on_change([esm, importmap], async () => {
            this.compiled_module = await this.model.compiled_module;
            this.invalidate_render();
        });
        this.on_change(class_name, () => {
            this.container.className = this.model.class_name.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
        });
        const child_props = this.model.children.map((child) => this.model.data.properties[child]);
        for (const cp of child_props) {
            this.connect(cp.change, () => this.update_children());
        }
        this.model._event_views.add(this);
    }
    disconnect_signals() {
        super.disconnect_signals();
        this._child_callbacks = new Map();
        this.model._event_views.delete(this);
        this.model.disconnect_watchers(this);
    }
    _dispatch_event(data) {
        for (const cb of this._event_handlers) {
            cb(data);
        }
    }
    _on_mounted() { }
    /**
     * Bokeh walks the whole view tree from `r_after_render`, but ESM components
     * do not render their children themselves: the children are mounted later,
     * by the component, once it commits. Recursing into a child that has not
     * been mounted yet would run `after_render` (and with it style updates,
     * measurement and layout) on a view that is still detached and therefore
     * measures 0x0, which permanently poisons anything latching onto its first
     * measurement. Such children are skipped here and walked when they mount.
     */
    r_after_render() {
        for (const child_view of this.children_views()) {
            if (child_view instanceof DOMView && this._is_mountable(child_view)) {
                child_view.r_after_render();
            }
        }
        this.after_render();
        this._was_built = true;
    }
    /**
     * Whether Bokeh's render walk may descend into a child view. Views this
     * component owns are only walkable once mounted; anything else (e.g. a
     * context menu) is not ours to defer.
     */
    _is_mountable(child_view) {
        if (!this._child_views.has(child_view.model)) {
            return true;
        }
        return child_view.el.isConnected;
    }
    notify_mount(child, id, remove = false) {
        if (!this._mounted.has(child)) {
            this._mounted.set(child, new Set());
        }
        if (remove) {
            this._mounted.get(child)?.delete(id);
        }
        else {
            this._mounted.get(child)?.add(id);
        }
        let children = this.model.data[child];
        if (!isArray(children)) {
            children = [children];
        }
        const mounted = this._mounted.get(child);
        // The size check skips the full scan while children are still mounting,
        // which would otherwise make mounting a list quadratic in its length.
        if (mounted.size >= children.length && children.every((model) => mounted.has(model.id))) {
            this._on_mounted();
            for (const cb of this._lifecycle_handlers.get("mounted") || []) {
                cb(child);
            }
        }
    }
    on_event(callback) {
        this._event_handlers.push(callback);
    }
    remove_on_event(callback) {
        if (this._event_handlers.includes(callback)) {
            this._event_handlers = this._event_handlers.filter((item) => item !== callback);
            return true;
        }
        return false;
    }
    get_child_view(model) {
        return this._child_views.get(model);
    }
    get render_fn() {
        if (this.compiled_module === null) {
            return null;
        }
        else if (this.compiled_module.default) {
            return this.compiled_module.default.render;
        }
        else {
            return this.compiled_module.render;
        }
    }
    get child_models() {
        const children = [];
        for (const child of this.model.children) {
            const model = this.model.data[child];
            if (isArray(model)) {
                for (const subchild of model) {
                    children.push(subchild);
                }
            }
            else if (model != null) {
                children.push(model);
            }
        }
        return children;
    }
    render_error(error) {
        const error_div = div({ class: "error" });
        error_div.innerHTML = formatError(error, this.model.esm);
        this.container.appendChild(error_div);
    }
    render() {
        this.empty();
        this._update_stylesheets();
        this._update_css_classes();
        this._apply_styles();
        this._update_css_variables();
        this._apply_visible();
        this._child_callbacks = new Map();
        this._child_rendered.clear();
        this._rendered = false;
        set_size(this.el, this.model);
        this.container = div();
        this.container.className = this.model.class_name.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
        set_size(this.container, this.model, false);
        this.shadow_el.append(this.container);
        if (this.model.compile_error) {
            this.render_error(this.model.compile_error);
        }
        else {
            this.render_esm();
        }
        for (const element_view of this.element_views) {
            // this.shadow_el is needed for Bokeh < 3.7.0 as this.self_target is not defined
            // can be removed when our minimum version is Bokeh 3.7.0
            // https://github.com/holoviz/panel/pull/7948
            const target = element_view.rendering_target() ?? this.self_target ?? this.shadow_el;
            element_view.render_to(target);
        }
    }
    get is_managed() {
        return this.parent instanceof LayoutDOMView && !(this.parent instanceof ReactiveESMView);
    }
    /**
     * Renders a child without laying it out and schedules a single layout pass
     * instead. Children mount one at a time (e.g. once per React
     * `componentDidMount`), and a child's `compute_layout` lays out, and so
     * measures, the whole tree; doing that per child is quadratic in the
     * number of children.
     */
    render_child(view) {
        rerender_view(view, false);
        this.schedule_layout();
    }
    /**
     * Lays out once all synchronous work queued in the current task (such as
     * a React commit mounting every child) has run. A pass that happens in the
     * meantime, e.g. `_on_mounted`'s, makes the scheduled one a no-op.
     */
    schedule_layout() {
        if (this._layout_pending) {
            return;
        }
        this._layout_pending = true;
        queueMicrotask(() => {
            if (!this._layout_pending || this.is_destroyed) {
                return;
            }
            this.compute_layout();
            // `finish()` may already have run and found the layout missing, and
            // nothing else re-checks once it exists.
            this.notify_finished();
        });
    }
    compute_layout() {
        this._layout_pending = false;
        if (this.is_managed) {
            super.compute_layout();
            return;
        }
        this.measure_layout();
        this.update_bbox();
        this._compute_layout();
        this.after_layout();
        // Override private property
        this._layout_computed = true;
    }
    _update_bbox() {
        const displayed = (() => {
            // Consider using Element.checkVisibility() in the future.
            // https://w3c.github.io/csswg-drafts/cssom-view-1/#dom-element-checkvisibility
            if (!this.el.isConnected) {
                return false;
            }
            else if (this.el.offsetParent != null) {
                return true;
            }
            else {
                const { position, display } = getComputedStyle(this.el);
                return position == "fixed" && display != "none";
            }
        })();
        // Override private property
        this._is_displayed = displayed;
        // `after_resize` lays out the whole root whenever this reports a change.
        // Reporting only actual size changes lets the first sibling's root pass,
        // which visits every view, absorb the resize callbacks of all the others;
        // always reporting one made initial render quadratic in sibling count.
        const width = displayed ? this.el.offsetWidth : 0;
        const height = displayed ? this.el.offsetHeight : 0;
        const last = this._last_size;
        if (last != null && last[0] === width && last[1] === height) {
            return false;
        }
        this._last_size = [width, height];
        return true;
    }
    after_rendered() {
        const handlers = (this._lifecycle_handlers.get("after_render") || []);
        for (const cb of handlers) {
            cb();
        }
        this.render_children();
        this.model_proxy.on(this.accessed_children, () => { this._stale_children = true; });
        if (!this._rendered) {
            for (const cb of (this._lifecycle_handlers.get("after_layout") || [])) {
                cb();
            }
        }
        this._rendered = true;
    }
    render_esm() {
        if (this.model.compiled === null || this.model.render_module === null) {
            return;
        }
        this.container.replaceChildren();
        this.accessed_properties = [];
        for (const lf of this._lifecycle_handlers.keys()) {
            (this._lifecycle_handlers.get(lf) || []).splice(0);
        }
        this.model.disconnect_watchers(this);
        // The view is passed rather than looked up by id: `Bokeh.index` lookups
        // walk every view on the page and pick the first view of a model that
        // is displayed more than once.
        const render_promise = this.model.render_module.then((mod) => mod.default.render(this));
        this._await_ready(render_promise);
    }
    render_children() {
        for (const child of this.accessed_children) {
            const child_model = this.model.data[child];
            const children = isArray(child_model) ? child_model : [child_model];
            for (const subchild of children) {
                const view = this._child_views.get(subchild);
                if (!view || this._child_rendered.get(view)) {
                    continue;
                }
                const parent = view.el.parentNode;
                if (parent) {
                    this._child_rendered.set(view, false);
                    this.render_child(view);
                    this._child_rendered.set(view, true);
                }
            }
        }
        this._stale_children = false;
        this.after_render();
    }
    has_finished() {
        if (!UIElementView.prototype.has_finished.call(this)) {
            return false;
        }
        if (this.is_layout_root && !this._layout_computed) {
            return false;
        }
        for (const child_view of this.child_views) {
            if (this._child_rendered.has(child_view) && !child_view.has_finished()) {
                return false;
            }
        }
        return true;
    }
    /**
     * Each notification makes the root walk the whole tree in `has_finished`,
     * and every component and child reports finishing separately, so loading
     * N components would walk the tree N times. Notifications issued in the
     * same task are coalesced into one per root.
     */
    notify_finished() {
        if (this.is_root) {
            super.notify_finished();
            return;
        }
        const root = this.root;
        if (PENDING_FINISHED.has(root)) {
            return;
        }
        PENDING_FINISHED.add(root);
        queueMicrotask(() => {
            PENDING_FINISHED.delete(root);
            if (!root.is_destroyed) {
                root.notify_finished();
            }
        });
    }
    invalidate_layout() {
        if (this.is_managed) {
            super.invalidate_layout();
            return;
        }
        // Deferred so that the children of one parent, which each invalidate on
        // render, do not interleave DOM writes with the measurements of their
        // own layout passes, forcing a reflow per child.
        this.update_layout();
        this.schedule_layout();
    }
    remove() {
        super.remove();
        for (const cb of (this._lifecycle_handlers.get("remove") || [])) {
            cb();
        }
        this._child_callbacks.clear();
        this._child_rendered.clear();
        this._mounted.clear();
    }
    after_resize() {
        if (this._rendered) {
            super.after_resize();
            for (const cb of (this._lifecycle_handlers.get("resize") || [])) {
                cb();
            }
        }
    }
    after_layout() {
        super.after_layout();
        if (this._rendered) {
            for (const cb of (this._lifecycle_handlers.get("after_layout") || [])) {
                cb();
            }
        }
    }
    /**
     * Maps each child model to the name of the children property holding it,
     * built once per update pass rather than searched per child view.
     */
    _child_names() {
        const names = new Map();
        for (const child of this.model.children) {
            const models = this.model.data[child];
            for (const model of isArray(models) ? models : [models]) {
                if (model != null && !names.has(model)) {
                    names.set(model, child);
                }
            }
        }
        return names;
    }
    /**
     * A children property can trigger more than one update pass for the same
     * change, e.g. the property change signal and the manual render policy path
     * in `ReactiveESM.watch`. `build_child_views` is async, so two passes that
     * overlap both create a view for the same model and only the last one is kept
     * in `_child_views`; the other is dropped without `remove()`. An orphaned
     * ReactComponent never mounts, so the promise it handed to `root._await_ready`
     * is never settled and the root's ready chain stays pending for the rest of
     * the session, which silently blocks anything waiting on it. Serializing the
     * passes makes the later one a no-op instead of a competing build.
     */
    async update_children() {
        const run = this._update_children_chain.then(() => this._update_children_pass());
        this._update_children_chain = run.then(() => undefined, () => undefined);
        return run;
    }
    /**
     * Groups newly created child views by the children property they belong to.
     */
    _group_new_views(created) {
        const names = this._child_names();
        const new_views = new Map();
        for (const child_view of this.child_views) {
            if (!created.has(child_view)) {
                continue;
            }
            const child = names.get(child_view.model);
            if (child == null) {
                continue;
            }
            const views = new_views.get(child);
            if (views == null) {
                new_views.set(child, [child_view]);
            }
            else {
                views.push(child_view);
            }
        }
        return new_views;
    }
    async _update_children_pass() {
        const created_children = new Set(await this.build_child_views());
        const all_views = this.child_views;
        if (this.model.render_policy !== "manual") {
            for (const child_view of all_views) {
                child_view.el.remove();
            }
        }
        const new_views = this._group_new_views(created_children);
        const current = new Set(all_views);
        for (const view of this._child_rendered.keys()) {
            if (!current.has(view)) {
                this._child_rendered.delete(view);
            }
        }
        for (const child of this.model.children) {
            const callbacks = this._child_callbacks.get(child) || [];
            const new_children = new_views.get(child) || [];
            for (const callback of callbacks) {
                callback(new_children);
            }
        }
        if (this._stale_children && this.model.render_policy !== "manual") {
            this.render_esm();
            this._update_children();
            this.invalidate_layout();
        }
        this._stale_children = false;
    }
    on_child_render(child, callback) {
        if (!this._child_callbacks.has(child)) {
            this._child_callbacks.set(child, []);
        }
        const callbacks = this._child_callbacks.get(child) || [];
        callbacks.push(callback);
    }
    remove_on_child_render(child, callback) {
        if (!this._child_callbacks.has(child)) {
            return;
        }
        if (callback === undefined) {
            this._child_callbacks.delete(child);
        }
        else {
            let callbacks = this._child_callbacks.get(child) || [];
            callbacks = callbacks.filter((cb) => cb !== callback);
            this._child_callbacks.set(child, callbacks);
        }
    }
}
export const RenderPolicy = Enum("manual", "children");
export class ReactiveESM extends HTMLBox {
    compiled = null;
    compiled_module = null;
    compile_error = null;
    model_proxy;
    render_module = null;
    sucrase_transforms = ["typescript"];
    _destroyer = null;
    // Keyed by the watched path; `orig` is the callback the caller passed,
    // `cb` the wrapper actually connected to `signal`.
    _esm_watchers = new Map();
    _event_views = new Set();
    constructor(attrs) {
        super(attrs);
    }
    initialize() {
        super.initialize();
        this.model_proxy = new Proxy(this, {
            get: init_model_getter,
            set: init_model_setter,
        });
        this.recompile();
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.properties.esm.change, () => this.recompile());
        this.connect(this.properties.importmap.change, () => this.recompile());
        // Registered once per model: `on_event` cannot be undone, so views
        // subscribe through `_event_views` instead.
        this.on_event(ESMEvent, (event) => {
            for (const view of this._event_views) {
                view._dispatch_event(event.data);
            }
        });
    }
    /**
     * Resolves a possibly dotted property path to the property's change
     * signal and the model owning it, falling back to the component model's
     * own properties.
     */
    _resolve_watch(prop) {
        const path = prop.split(".");
        let target = this.data;
        for (let i = 0; i < path.length - 1; i++) {
            if (target != null && target.properties != null && path[i] in target.properties) {
                target = target[path[i]];
            }
            else {
                target = null;
                break;
            }
        }
        const name = path[path.length - 1];
        if (target != null && target.properties != null && name in target.properties) {
            return { target, name, signal: target.property(name).change };
        }
        else if (prop in this.properties) {
            return { target: this, name: prop, signal: this.property(prop).change };
        }
        return null;
    }
    watch(view, prop, cb, force = false) {
        const resolved = this._resolve_watch(prop);
        if (resolved == null) {
            return;
        }
        const { target, name, signal } = resolved;
        const orig = cb;
        // Handle reset of param.Event properties
        if (!force && target === this.data && this.events.includes(name)) {
            const event_cb = cb;
            cb = () => {
                if (this.data[name]) {
                    event_cb();
                    this.data.setv({ [name]: false });
                }
            };
        }
        if (target === this.data && this.children.includes(name)) {
            const children_cb = cb;
            cb = async () => {
                if (view == null) {
                    children_cb();
                    return;
                }
                view._stale_children = true;
                // The view connected `update_children` to this signal before any
                // watcher, so the pass handling this change is already queued.
                await view._update_children_chain;
                if (this.render_policy !== "manual") {
                    children_cb();
                    return;
                }
                let resolve_ready;
                view.root._await_ready(new Promise((r) => { resolve_ready = r; }));
                children_cb();
                view.render_children();
                view._update_children();
                view.invalidate_layout();
                const collect_ready = (v) => {
                    const promises = [v.ready];
                    for (const child of v.child_views || []) {
                        promises.push(...collect_ready(child));
                    }
                    return promises;
                };
                const all_ready = [];
                for (const child_view of view.child_views) {
                    all_ready.push(...collect_ready(child_view));
                }
                if (all_ready.length > 0) {
                    Promise.all(all_ready).then(() => resolve_ready());
                }
                else {
                    resolve_ready();
                }
            };
        }
        signal.connect(cb);
        const watchers = this._esm_watchers.get(prop);
        const watcher = { view, orig, cb, signal };
        if (watchers == null) {
            this._esm_watchers.set(prop, [watcher]);
        }
        else {
            watchers.push(watcher);
        }
    }
    unwatch(view, prop, cb) {
        const watchers = this._esm_watchers.get(prop);
        if (watchers == null) {
            return false;
        }
        let disconnected = false;
        const remaining = [];
        for (const watcher of watchers) {
            if (watcher.view === view && watcher.orig === cb) {
                disconnected = watcher.signal.disconnect(watcher.cb) || disconnected;
            }
            else {
                remaining.push(watcher);
            }
        }
        if (remaining.length > 0) {
            this._esm_watchers.set(prop, remaining);
        }
        else {
            this._esm_watchers.delete(prop);
        }
        return disconnected;
    }
    disconnect_watchers(view) {
        for (const [prop, watchers] of this._esm_watchers) {
            const remaining = [];
            for (const watcher of watchers) {
                if (watcher.view === view) {
                    watcher.signal.disconnect(watcher.cb);
                }
                else {
                    remaining.push(watcher);
                }
            }
            if (remaining.length > 0) {
                this._esm_watchers.set(prop, remaining);
            }
            else {
                this._esm_watchers.delete(prop);
            }
        }
    }
    async _declare_importmap() {
        await resources.ensure_shim(this.external_resources?.shim);
        if (this.importmap) {
            // Every instance of a component class carries the same map, and
            // es-module-shims re-resolves the whole map on each addition.
            const key = JSON.stringify(this.importmap);
            if (!DECLARED_IMPORTMAPS.has(key)) {
                DECLARED_IMPORTMAPS.add(key);
                resources.add_import_map(this.importmap);
            }
        }
    }
    _run_initializer(initialize) {
        const props = { model: this.model_proxy };
        this._destroyer = initialize(props);
    }
    destroy() {
        super.destroy();
        if (this._destroyer) {
            this._destroyer(this.model_proxy);
        }
    }
    init_module() {
        if (this.compile_error) {
            return;
        }
        this.render_module = this._render_module();
    }
    /**
     * The module whose `default.render(view)` renders a view of this model.
     */
    _render_module() {
        return ESM_RENDER_MODULE;
    }
    _cached_module(key, load) {
        let module = MODULE_CACHE.get(key);
        if (module == null) {
            module = track_module(load());
            MODULE_CACHE.set(key, module);
        }
        return module;
    }
    get resolved_render_module() {
        return this.render_module == null ? null : RESOLVED_MODULES.get(this.render_module) ?? null;
    }
    _import_source(code) {
        const url = URL.createObjectURL(new Blob([code], { type: "text/javascript" }));
        const module = resources.import_module(url, this.external_resources?.shim);
        // Fetched by the time the import settles, and otherwise held until unload.
        module.finally(() => URL.revokeObjectURL(url)).catch(() => { });
        return module;
    }
    compile() {
        if (this.bundle != null) {
            return this.esm;
        }
        let compiled;
        try {
            compiled = transform(this.esm, {
                transforms: this.sucrase_transforms,
                filePath: "render.tsx",
            }).code;
        }
        catch (e) {
            if (e instanceof SyntaxError) {
                if (this.dev) {
                    this.compile_error = e;
                    return null;
                }
                else {
                    e.message = `${e.message}. See more information with '--dev' flag.`;
                    throw e;
                }
            }
            else {
                throw e;
            }
        }
        return compiled;
    }
    get _module_cache_key() {
        if (this.bundle === "url") {
            return this.esm;
        }
        return this.bundle || `${this.class_name}-${source_id(this.esm)}`;
    }
    async recompile() {
        this.compile_error = null;
        const use_cache = (!this.dev || this.bundle);
        // Not computed in dev mode, where every edit would be interned.
        const cache_key = use_cache ? this._module_cache_key : "";
        const compile_key = `${this.type}:${cache_key}`;
        let source = use_cache ? COMPILE_CACHE.get(compile_key) ?? null : null;
        if (source === null) {
            source = this.compile();
            if (source === null) {
                this.compiled_module = Promise.resolve(null);
                return;
            }
            if (use_cache) {
                COMPILE_CACHE.set(compile_key, source);
            }
        }
        const compiled = source;
        this.compiled = compiled;
        // Awaiting the import map here would leave compiled_module holding the
        // previous module for a tick, and a view handling the same esm change
        // awaits that property, so it has to be replaced synchronously.
        const declared = this._declare_importmap();
        let esm_module;
        let resolve;
        if (use_cache && MODULE_CACHE.has(cache_key)) {
            const cached = MODULE_CACHE.get(cache_key);
            esm_module = declared.then(() => cached);
        }
        else {
            if (use_cache) {
                MODULE_CACHE.set(cache_key, new Promise((res) => { resolve = res; }));
            }
            if (this.bundle === "url") {
                esm_module = declared.then(() => resources.import_module(this.esm, this.external_resources?.shim));
            }
            else {
                esm_module = declared.then(() => this._import_source(compiled));
            }
        }
        this.compiled_module = (esm_module).then((mod) => {
            if (resolve) {
                resolve(mod);
            }
            try {
                let initialize;
                if (this.bundle != null && (mod.default || {}).hasOwnProperty(this.class_name)) {
                    mod = mod.default[this.class_name];
                }
                if (mod.initialize) {
                    initialize = mod.initialize;
                }
                else if (mod.default && mod.default.initialize) {
                    initialize = mod.default.initialize;
                }
                else if (typeof mod.default === "function") {
                    const initialized = mod.default();
                    mod = { default: initialized };
                    initialize = initialized.initialize;
                }
                if (initialize) {
                    this._run_initializer(initialize);
                }
                this.init_module();
                return mod;
            }
            catch (e) {
                if (this.dev) {
                    this.compile_error = e;
                }
                console.error(`Could not initialize module due to error: ${e}`);
                return null;
            }
        });
    }
    static __module__ = "panel.models.esm";
    static {
        this.prototype.default_view = ReactiveESMView;
        this.define(({ Any, Array, Bool, Nullable, Str }) => ({
            _defs: [Array(Any), []],
            css_bundle: [Nullable(Str), null],
            bundle: [Nullable(Str), null],
            children: [Array(Str), []],
            class_name: [Str, ""],
            data: [Any],
            dev: [Bool, false],
            esm: [Str, ""],
            events: [Array(Str), []],
            importmap: [Any, {}],
            render_policy: [RenderPolicy, "children"],
        }));
    }
}
//# sourceMappingURL=reactive_esm.js.map