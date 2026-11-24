import type * as p from "@bokehjs/core/properties";
import { ModelEvent } from "@bokehjs/core/bokeh_events";
import { LayoutDOM, LayoutDOMView } from "@bokehjs/models/layouts/layout_dom";
import type { Attrs } from "@bokehjs/core/types";
import type { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
import type { ResourceSpec } from "./resources";
export declare class VegaEvent extends ModelEvent {
    readonly data: any;
    constructor(data: any);
    protected get event_values(): Attrs;
}
export declare class VegaPlotView extends LayoutDOMView {
    model: VegaPlot;
    vega_view: any;
    container: HTMLDivElement;
    _connected: Set<ColumnDataSource>;
    _listeners: Set<string>;
    _dirty_sources: Set<string>;
    _data_update: Promise<void> | null;
    _replot: any;
    _replot_pending: boolean;
    _embed_id: number;
    _resize_frame: number | null;
    _last_size: [number, number] | null;
    lazy_initialize(): Promise<void>;
    connect_signals(): void;
    _connect_sources(): void;
    /**
     * Pushes changed datasets into the existing Vega View rather than
     * recompiling the spec, coalescing changes made in the same patch.
     */
    _source_changed(name: string): void;
    _update_data(): void;
    remove(): void;
    _dispatch_event(name: string, value: any): void;
    _fetch_dataset(cds: any): any[];
    /**
     * Writes the values of a data source into the spec, returning the name
     * of the dataset they end up in once the spec is compiled by Vega.
     */
    _store_values(name: string, values: any[]): string;
    get child_models(): LayoutDOM[];
    render(): void;
    _plot(): void;
    _add_listeners(): void;
    after_layout(): void;
    protected _after_resize(): void;
    _container_size(): [number, number];
    _schedule_resize(): void;
    /**
     * Container-sized specs only measure their container on window resize
     * events, so replay those whenever the container itself changes size.
     * Remembering the measured size breaks the loop where the redraw
     * resizes the container again.
     */
    _resize(): void;
}
export declare namespace VegaPlot {
    type Attrs = p.AttrsOf<Props>;
    type Props = LayoutDOM.Props & {
        data: p.Property<any>;
        data_sources: p.Property<any>;
        events: p.Property<string[]>;
        show_actions: p.Property<boolean>;
        theme: p.Property<string | null>;
        throttle: p.Property<any>;
        external_resources: p.Property<ResourceSpec | null>;
    };
}
export interface VegaPlot extends VegaPlot.Attrs {
}
export declare class VegaPlot extends LayoutDOM {
    properties: VegaPlot.Props;
    constructor(attrs?: Partial<VegaPlot.Attrs>);
    static __module__: string;
    initialize(): void;
}
//# sourceMappingURL=vega.d.ts.map