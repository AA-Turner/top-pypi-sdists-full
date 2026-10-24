import { Column, ColumnView } from "./column";
import { ModelEvent } from "@bokehjs/core/bokeh_events";
import type * as p from "@bokehjs/core/properties";
import type { Attrs } from "@bokehjs/core/types";
import type { UIElementView } from "@bokehjs/models/ui/ui_element";
export declare class ScrollLatestEvent extends ModelEvent {
    readonly model: Feed;
    readonly rerender: boolean;
    readonly scroll_limit?: number | null | undefined;
    constructor(model: Feed, rerender: boolean, scroll_limit?: number | null | undefined);
    protected get event_values(): Attrs;
    static from_values(values: object): ScrollLatestEvent;
}
export declare class FeedView extends ColumnView {
    model: Feed;
    _intersection_observer: IntersectionObserver;
    protected _visibility_pending: boolean;
    protected _visibility_listener: boolean;
    protected _latest_pending: boolean;
    _last_visible: UIElementView | null;
    _rendered: boolean;
    _sync: boolean;
    _reference: number | null;
    _reference_view: UIElementView | null;
    protected _children_update: Promise<void> | null;
    protected _latest_scroll_pending: boolean;
    protected _latest_last: string | null;
    initialize(): void;
    connect_signals(): void;
    get node_map(): any;
    update_children(): Promise<void>;
    _scroll_to_latest_children(): void;
    protected _rebuild_children(): Promise<void>;
    build_child_views(): Promise<UIElementView[]>;
    _update_layout(): void;
    render(): void;
    _reobserve_children(): void;
    trigger_auto_scroll(): void;
    _land_latest_scroll(): boolean;
    after_render(): void;
}
export declare namespace Feed {
    type Attrs = p.AttrsOf<Props>;
    type Props = Column.Props & {
        visible_children: p.Property<string[]>;
    };
}
export interface Feed extends Feed.Attrs {
}
export declare class Feed extends Column {
    properties: Feed.Props;
    constructor(attrs?: Partial<Feed.Attrs>);
    static __module__: string;
}
//# sourceMappingURL=feed.d.ts.map