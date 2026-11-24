import { div } from "@bokehjs/core/dom";
import { ModelEvent } from "@bokehjs/core/bokeh_events";
import { isArray } from "@bokehjs/core/util/types";
import { LayoutDOM, LayoutDOMView } from "@bokehjs/models/layouts/layout_dom";
import { set_size } from "./layout";
import { await_resources, define_external_resources, load_resources, render_resource_error, } from "./resources";
import { debounce } from "debounce";
export class VegaEvent extends ModelEvent {
    data;
    constructor(data) {
        super();
        this.data = data;
    }
    get event_values() {
        return { model: this.origin, data: this.data };
    }
    static {
        this.prototype.event_name = "vega_event";
    }
}
export class VegaPlotView extends LayoutDOMView {
    vega_view;
    container;
    _connected = new Set();
    _listeners = new Set();
    _dirty_sources = new Set();
    _data_update = null;
    _replot;
    _replot_pending = false;
    _embed_id = 0;
    _resize_frame = null;
    _last_size = null;
    async lazy_initialize() {
        await super.lazy_initialize();
        const error = await await_resources(this.model);
        if (error != null) {
            render_resource_error(this, error, LayoutDOMView.prototype.render);
        }
    }
    connect_signals() {
        super.connect_signals();
        const { data, show_actions, theme, data_sources, events } = this.model.properties;
        this._replot = debounce(() => this._plot(), 20);
        this.on_change([data, show_actions, theme], () => {
            this._replot_pending = true;
            this._replot();
        });
        this.on_change(data_sources, () => this._connect_sources());
        this.on_change(events, () => this._add_listeners());
        this._connect_sources();
    }
    _connect_sources() {
        for (const name in this.model.data_sources) {
            const cds = this.model.data_sources[name];
            if (!this._connected.has(cds)) {
                this.connect(cds.properties.data.change, () => this._source_changed(name));
                this._connected.add(cds);
            }
        }
    }
    /**
     * Pushes changed datasets into the existing Vega View rather than
     * recompiling the spec, coalescing changes made in the same patch.
     */
    _source_changed(name) {
        this._dirty_sources.add(name);
        if (this._data_update == null) {
            this._data_update = Promise.resolve().then(() => {
                this._data_update = null;
                this._update_data();
            });
        }
    }
    _update_data() {
        if (this._dirty_sources.size === 0 || this._replot_pending) {
            this._dirty_sources.clear();
            return;
        }
        const view = this.vega_view;
        if (view == null) {
            // Applied once the embed in flight resolves, or fetched by render()
            return;
        }
        const names = [...this._dirty_sources];
        this._dirty_sources.clear();
        for (const name of names) {
            const cds = this.model.data_sources[name];
            if (cds == null) {
                continue;
            }
            const values = this._fetch_dataset(cds);
            const dataset = this._store_values(name, values);
            try {
                view.data(dataset, values);
            }
            catch {
                // The dataset is not part of the compiled dataflow (e.g. the spec
                // was restructured), so fall back to re-embedding the spec.
                this._replot_pending = true;
                this._replot();
                return;
            }
        }
        view.runAsync();
    }
    remove() {
        // Also discards the result of an embed still in flight
        this._embed_id++;
        if (this._resize_frame != null) {
            cancelAnimationFrame(this._resize_frame);
            this._resize_frame = null;
        }
        this.vega_view?.finalize();
        this.vega_view = null;
        super.remove();
    }
    _dispatch_event(name, value) {
        if ("vlPoint" in value && value.vlPoint.or != null) {
            const indexes = [];
            for (const index of value.vlPoint.or) {
                if (index._vgsid_ !== undefined) { // If "_vgsid_" property exists
                    indexes.push(index._vgsid_);
                }
                else { // If "_vgsid_" property doesn't exist
                    // Iterate through all properties in the "index" object
                    for (const key in index) {
                        if (index.hasOwnProperty(key)) { // To ensure key comes from "index" object itself, not its prototype
                            indexes.push({ [key]: index[key] }); // Push a new object with this key-value pair into the array
                        }
                    }
                }
            }
            value = indexes;
        }
        this.model.trigger_event(new VegaEvent({ type: name, value }));
    }
    _fetch_dataset(cds) {
        const data = [];
        const columns = cds.columns();
        for (let i = 0; i < cds.get_length(); i++) {
            const item = {};
            for (const column of columns) {
                item[column] = cds.data[column][i];
            }
            data.push(item);
        }
        return data;
    }
    /**
     * Writes the values of a data source into the spec, returning the name
     * of the dataset they end up in once the spec is compiled by Vega.
     */
    _store_values(name, values) {
        const { data } = this.model;
        if (name === "data" && data.data != null && !isArray(data.data)) {
            data.data.values = values;
            return data.data.name ?? "source_0";
        }
        if (data.data != null) {
            const data_objs = isArray(data.data) ? data.data : [data.data];
            for (const d of data_objs) {
                if (d.name === name) {
                    d.values = values;
                    return name;
                }
            }
        }
        data.datasets = data.datasets ?? {};
        data.datasets[name] = values;
        return name;
    }
    get child_models() {
        return [];
    }
    render() {
        super.render();
        this.container = div();
        set_size(this.container, this.model);
        this._plot();
        this.shadow_el.append(this.container);
    }
    _plot() {
        this._replot_pending = false;
        const data = this.model.data;
        if ((data == null) || !window.vegaEmbed) {
            return;
        }
        for (const name in this.model.data_sources) {
            this._store_values(name, this._fetch_dataset(this.model.data_sources[name]));
        }
        this._dirty_sources.clear();
        const config = { actions: this.model.show_actions, theme: this.model.theme };
        // vegaEmbed replaces the container contents but leaves the previous
        // View (and its timers and listeners) running, so finalize it here.
        this.vega_view?.finalize();
        this.vega_view = null;
        this._listeners.clear();
        const embed_id = ++this._embed_id;
        window.vegaEmbed(this.container, this.model.data, config).then((result) => {
            if (embed_id !== this._embed_id) {
                result.view.finalize();
                return;
            }
            this.vega_view = result.view;
            // The container may have changed size while the spec was compiling
            this._last_size = null;
            this._add_listeners();
            this._update_data();
            this._schedule_resize();
        });
    }
    _add_listeners() {
        const view = this.vega_view;
        if (view == null) {
            return;
        }
        for (const event of this.model.events) {
            if (this._listeners.has(event)) {
                continue;
            }
            this._listeners.add(event);
            const callback = (name, value) => this._dispatch_event(name, value);
            const timeout = this.model.throttle[event] || 20;
            view.addSignalListener(event, debounce(callback, timeout, false));
        }
    }
    after_layout() {
        super.after_layout();
        this._schedule_resize();
    }
    // Bokeh's ResizeObserver calls this whenever the element's box changes,
    // including CSS-driven changes (flex, splitters) that skip after_layout.
    _after_resize() {
        super._after_resize();
        this._schedule_resize();
    }
    _container_size() {
        return [this.container.clientWidth, this.container.clientHeight];
    }
    _schedule_resize() {
        if (this._resize_frame != null) {
            return;
        }
        this._resize_frame = requestAnimationFrame(() => {
            this._resize_frame = null;
            this._resize();
        });
    }
    /**
     * Container-sized specs only measure their container on window resize
     * events, so replay those whenever the container itself changes size.
     * Remembering the measured size breaks the loop where the redraw
     * resizes the container again.
     */
    _resize() {
        const view = this.vega_view;
        if (view == null) {
            return;
        }
        const [width, height] = this._container_size();
        if (width === 0 || height === 0) {
            return;
        }
        const last = this._last_size;
        if (last != null && last[0] === width && last[1] === height) {
            return;
        }
        this._last_size = [width, height];
        for (const listener of view._eventListeners) {
            if (listener.type === "resize") {
                listener.handler(new Event("resize"));
            }
        }
    }
}
export class VegaPlot extends LayoutDOM {
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "panel.models.vega";
    static {
        this.prototype.default_view = VegaPlotView;
        this.define(({ Any, List, Bool, Nullable, Str }) => ({
            data: [Any, {}],
            data_sources: [Any, {}],
            events: [List(Str), []],
            show_actions: [Bool, false],
            theme: [Nullable(Str), null],
            throttle: [Any, {}],
        }));
        define_external_resources(this);
    }
    initialize() {
        super.initialize();
        load_resources(this);
    }
}
//# sourceMappingURL=vega.js.map