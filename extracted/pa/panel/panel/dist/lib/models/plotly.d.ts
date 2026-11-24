import { ModelEvent } from "@bokehjs/core/bokeh_events";
import type { StyleSheetLike } from "@bokehjs/core/dom";
import type * as p from "@bokehjs/core/properties";
import type { Attrs } from "@bokehjs/core/types";
import { HTMLBox, HTMLBoxView } from "./layout";
export declare class PlotlyEvent extends ModelEvent {
    readonly data: any;
    constructor(data: any);
    protected get event_values(): Attrs;
}
interface PlotlyHTMLElement extends HTMLDivElement {
    _fullLayout: any;
    _hoverdata: any;
    layout: any;
    on(event: "plotly_relayout", callback: (eventData: any) => void): void;
    on(event: "plotly_relayouting", callback: (eventData: any) => void): void;
    on(event: "plotly_restyle", callback: (eventData: any) => void): void;
    on(event: "plotly_click", callback: (eventData: any) => void): void;
    on(event: "plotly_doubleclick", callback: (eventData: any) => void): void;
    on(event: "plotly_hover", callback: (eventData: any) => void): void;
    on(event: "plotly_clickannotation", callback: (eventData: any) => void): void;
    on(event: "plotly_selected", callback: (eventData: any) => void): void;
    on(event: "plotly_deselect", callback: () => void): void;
    on(event: "plotly_unhover", callback: () => void): void;
}
type PlotlyUpdate = {
    [key: string]: unknown;
};
/**
 * A relayout, or a restyle of a single trace, sent before the plot rendered.
 * Applied in order once plotted, they leave the plot as it would be had they
 * been applied as they arrived.
 */
type PendingUpdate = {
    kind: "relayout";
    data: PlotlyUpdate;
} | {
    kind: "restyle";
    trace: number;
    data: PlotlyUpdate;
};
/**
 * Adds an update to the queue, dropping earlier writes it supersedes (the
 * same key or a descendant, up to an item-level write that shifted them)
 * and merging it into the last entry when that entry is of the same kind
 * and target and none of its keys conflict. Apart from item-level writes,
 * every key is then pending at most once, which bounds the queue.
 */
export declare function queue_update(queue: PendingUpdate[], update: PendingUpdate): PendingUpdate[];
export declare class PlotlyPlotView extends HTMLBoxView {
    model: PlotlyPlot;
    _setViewport: Function;
    _settingViewport: boolean;
    _plotInitialized: boolean;
    _rendered: boolean;
    _reacting: boolean;
    _relayouting: boolean;
    _model_restyles: number;
    _pending_updates: PendingUpdate[];
    _hoverdata: any;
    container: PlotlyHTMLElement;
    _end_relayouting: (() => void) & {
        clear(): void;
    } & {
        flush(): void;
    };
    _throttled_resize: any;
    _frames: any[] | null;
    _plot_promise: Promise<void> | null;
    _plot_scheduled: boolean;
    _new_plot: boolean;
    initialize(): void;
    connect_signals(): void;
    /**
     * Plots once all changes applied in the current task have been
     * processed, waiting for a plot in progress to finish first.
     */
    _schedule_plot(new_plot?: boolean): void;
    stylesheets(): StyleSheetLike[];
    remove(): void;
    render(): void;
    _restyle(data: PlotlyUpdate, traces: number | number[] | null): Promise<unknown>;
    /**
     * Splits a restyle into one update per trace, resolving values the way
     * Plotly does: arrays are indexed (and wrapped) by position in `traces`,
     * and undefined values leave the trace unchanged.
     */
    _queue_restyle(data: PlotlyUpdate, traces: number | number[] | null): void;
    _apply_pending_updates(): Promise<void>;
    /**
     * The plot size derived from the model and the element, or null while
     * the element is not laid out.
     */
    _plot_size(): [number, number] | null;
    style_redraw(): void;
    resize_layout(): void;
    after_layout(): void;
    _trace_data(): any;
    _layout_data(): any;
    _install_callbacks(): void;
    plot(new_plot?: boolean): Promise<void>;
    _get_trace(index: number, update: boolean): any;
    _updateViewportFromProperty(): void;
    _updateViewportProperty(): void;
    _updateSetViewportFunction(): void;
}
export declare namespace PlotlyPlot {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        data: p.Property<any[]>;
        frames: p.Property<any[] | null>;
        layout: p.Property<any>;
        config: p.Property<any>;
        data_sources: p.Property<any[]>;
        relayout: p.Property<any>;
        restyle: p.Property<any>;
        relayout_data: p.Property<any>;
        restyle_data: p.Property<any>;
        viewport: p.Property<any>;
        viewport_update_policy: p.Property<string>;
        viewport_update_throttle: p.Property<number>;
        _render_count: p.Property<number>;
    };
}
export interface PlotlyPlot extends PlotlyPlot.Attrs {
}
export declare class PlotlyPlot extends HTMLBox {
    properties: PlotlyPlot.Props;
    constructor(attrs?: Partial<PlotlyPlot.Attrs>);
    static __module__: string;
}
export {};
//# sourceMappingURL=plotly.d.ts.map