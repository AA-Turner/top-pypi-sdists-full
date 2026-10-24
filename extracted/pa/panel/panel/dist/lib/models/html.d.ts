import { ModelEvent } from "@bokehjs/core/bokeh_events";
import { Signal } from "@bokehjs/core/signaling";
import type { StyleSheetLike } from "@bokehjs/core/dom";
import type * as p from "@bokehjs/core/properties";
import type { Attrs, Dict } from "@bokehjs/core/types";
import { Markup } from "@bokehjs/models/widgets/markup";
import { PanelMarkupView } from "./layout";
/**
 * Replaces the characters between `start` and `end` of the unescaped
 * text with the escaped `patch`, producing `version` of the text.
 */
export declare class HTMLStreamEvent extends ModelEvent {
    readonly model: HTML;
    readonly patch: string;
    readonly start: number;
    readonly end: number | null;
    readonly version: number | null;
    constructor(model: HTML, patch: string, start: number, end?: number | null, version?: number | null);
    protected get event_values(): Attrs;
    static from_values(values: object): HTMLStreamEvent;
}
export declare function escape_html(text: string): string;
export declare function unescape_html(text: string): string;
/**
 * Splits HTML into top-level blocks, i.e. ranges ending where all
 * opened elements are closed again, starting the scan at `from`. HTML
 * that never closes an element (or ends mid-tag) yields one block for
 * the remainder, so malformed input degrades to a full re-render.
 */
export declare function split_blocks(html: string, from?: number): [number, number][];
type Block = {
    end: number;
    nodes: ChildNode[];
};
export declare class DOMEvent extends ModelEvent {
    readonly node: string;
    readonly data: unknown;
    constructor(node: string, data: unknown);
    protected get event_values(): Attrs;
}
export declare function html_decode(input: string): string | null;
export declare function run_scripts(node: Element): void;
export declare class HTMLView extends PanelMarkupView {
    model: HTML;
    protected _blocks: Block[] | null;
    protected _dirty: number | null;
    protected _frame: number | null;
    protected readonly _event_listeners: Map<string, Map<string, (event: Event) => void>>;
    connect_signals(): void;
    remove(): void;
    stylesheets(): StyleSheetLike[];
    protected _flush_stream(): void;
    /**
     * Re-renders only the top-level blocks at or after the first
     * modified offset, keeping the DOM (and any text selection) of the
     * preceding blocks intact.
     */
    protected _update_blocks(html: string, dirty: number): void;
    set_html(html: string | null): void;
    protected _decorate(nodes: Iterable<Node>): void;
    render(): void;
    style_redraw(): void;
    process_tex(): string;
    private contains_tex;
    private _remove_event_listeners;
    private _setup_event_listeners;
}
export declare namespace HTML {
    type Attrs = p.AttrsOf<Props>;
    type Props = Markup.Props & {
        events: p.Property<Dict<string[]>>;
        run_scripts: p.Property<boolean>;
        stream_version: p.Property<number>;
    };
}
export interface HTML extends HTML.Attrs {
}
export declare class HTML extends Markup {
    properties: HTML.Props;
    protected _stream_text: string | null;
    protected _stream_queue: Map<number, HTMLStreamEvent>;
    readonly streamed: Signal<number, this>;
    constructor(attrs?: Partial<HTML.Attrs>);
    get stream_text(): string;
    apply_stream(event: HTMLStreamEvent): void;
    protected _apply_stream(event: HTMLStreamEvent): void;
    reset_stream(): void;
    static __module__: string;
}
export {};
//# sourceMappingURL=html.d.ts.map