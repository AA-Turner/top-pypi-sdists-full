import type { Transform } from "sucrase";
import { ModelEvent } from "@bokehjs/core/bokeh_events";
import type { StyleSheetLike } from "@bokehjs/core/dom";
import { DOMView } from "@bokehjs/core/dom_view";
import type * as p from "@bokehjs/core/properties";
import type { Attrs } from "@bokehjs/core/types";
import type { LayoutDOM } from "@bokehjs/models/layouts/layout_dom";
import { UIElementView } from "@bokehjs/models/ui/ui_element";
import type { UIElement } from "@bokehjs/models/ui/ui_element";
import { HTMLBox, HTMLBoxView } from "./layout";
export declare class DataEvent extends ModelEvent {
    readonly data: unknown;
    constructor(data: unknown);
    protected get event_values(): Attrs;
}
export declare class ESMEvent extends DataEvent {
    static from_values(values: object): ESMEvent;
}
export declare function model_getter(target: ReactiveESMView, name: string): any;
export declare function model_setter(target: ReactiveESMView, name: string, value: any): boolean;
export declare class ReactiveESMView extends HTMLBoxView {
    model: ReactiveESM;
    container: HTMLDivElement;
    accessed_properties: string[];
    accessed_children: string[];
    compiled_module: any;
    model_proxy: any;
    _child_callbacks: Map<string, ((new_views: UIElementView[]) => void)[]>;
    _child_rendered: Map<UIElementView, boolean>;
    _event_handlers: ((data: unknown) => void)[];
    _lifecycle_handlers: Map<string, ((...args: any[]) => void)[]>;
    _module_cache: Map<string, any>;
    _rendered: boolean;
    _stale_children: boolean;
    _mounted: Map<string, Set<string>>;
    _update_children_chain: Promise<void>;
    _layout_pending: boolean;
    _proxy_methods: Map<string, (...args: any[]) => any>;
    _last_size: [number, number] | null;
    initialize(): void;
    lazy_initialize(): Promise<void>;
    stylesheets(): StyleSheetLike[];
    connect_signals(): void;
    disconnect_signals(): void;
    _dispatch_event(data: unknown): void;
    _on_mounted(): void;
    /**
     * Bokeh walks the whole view tree from `r_after_render`, but ESM components
     * do not render their children themselves: the children are mounted later,
     * by the component, once it commits. Recursing into a child that has not
     * been mounted yet would run `after_render` (and with it style updates,
     * measurement and layout) on a view that is still detached and therefore
     * measures 0x0, which permanently poisons anything latching onto its first
     * measurement. Such children are skipped here and walked when they mount.
     */
    r_after_render(): void;
    /**
     * Whether Bokeh's render walk may descend into a child view. Views this
     * component owns are only walkable once mounted; anything else (e.g. a
     * context menu) is not ours to defer.
     */
    protected _is_mountable(child_view: DOMView): boolean;
    notify_mount(child: string, id: string, remove?: boolean): void;
    on_event(callback: (data: unknown) => void): void;
    remove_on_event(callback: (data: unknown) => void): boolean;
    get_child_view(model: UIElement): UIElementView | undefined;
    get render_fn(): ((props: any) => any) | null;
    get child_models(): LayoutDOM[];
    render_error(error: SyntaxError): void;
    render(): void;
    get is_managed(): boolean;
    /**
     * Renders a child without laying it out and schedules a single layout pass
     * instead. Children mount one at a time (e.g. once per React
     * `componentDidMount`), and a child's `compute_layout` lays out, and so
     * measures, the whole tree; doing that per child is quadratic in the
     * number of children.
     */
    render_child(view: DOMView): void;
    /**
     * Lays out once all synchronous work queued in the current task (such as
     * a React commit mounting every child) has run. A pass that happens in the
     * meantime, e.g. `_on_mounted`'s, makes the scheduled one a no-op.
     */
    schedule_layout(): void;
    compute_layout(): void;
    protected _update_bbox(): boolean;
    after_rendered(): void;
    render_esm(): void;
    render_children(): void;
    has_finished(): boolean;
    /**
     * Each notification makes the root walk the whole tree in `has_finished`,
     * and every component and child reports finishing separately, so loading
     * N components would walk the tree N times. Notifications issued in the
     * same task are coalesced into one per root.
     */
    notify_finished(): void;
    invalidate_layout(): void;
    remove(): void;
    after_resize(): void;
    after_layout(): void;
    /**
     * Maps each child model to the name of the children property holding it,
     * built once per update pass rather than searched per child view.
     */
    protected _child_names(): Map<UIElement, string>;
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
    update_children(): Promise<void>;
    /**
     * Groups newly created child views by the children property they belong to.
     */
    protected _group_new_views(created: Set<UIElementView>): Map<string, UIElementView[]>;
    protected _update_children_pass(): Promise<void>;
    on_child_render(child: string, callback: (new_views: UIElementView[]) => void): void;
    remove_on_child_render(child: string, callback?: (new_views: UIElementView[]) => void): void;
}
export declare const RenderPolicy: import("@bokehjs/core/kinds").Kinds.Enum<"children" | "manual">;
export declare namespace ReactiveESM {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        _defs: p.Property<any[]>;
        css_bundle: p.Property<string | null>;
        bundle: p.Property<string | null>;
        children: p.Property<any>;
        class_name: p.Property<string>;
        data: p.Property<any>;
        dev: p.Property<boolean>;
        esm: p.Property<string>;
        events: p.Property<string[]>;
        importmap: p.Property<any>;
        render_policy: p.Property<typeof RenderPolicy["__type__"]>;
    };
}
export interface ReactiveESM extends ReactiveESM.Attrs {
}
export declare class ReactiveESM extends HTMLBox {
    properties: ReactiveESM.Props;
    compiled: string | null;
    compiled_module: Promise<any> | null;
    compile_error: Error | null;
    model_proxy: any;
    render_module: Promise<any> | null;
    sucrase_transforms: Transform[];
    _destroyer: any | null;
    _esm_watchers: Map<string, {
        view: ReactiveESMView | null;
        orig: any;
        cb: any;
        signal: any;
    }[]>;
    _event_views: Set<ReactiveESMView>;
    constructor(attrs?: Partial<ReactiveESM.Attrs>);
    initialize(): void;
    connect_signals(): void;
    /**
     * Resolves a possibly dotted property path to the property's change
     * signal and the model owning it, falling back to the component model's
     * own properties.
     */
    protected _resolve_watch(prop: string): {
        target: any;
        name: string;
        signal: any;
    } | null;
    watch(view: ReactiveESMView | null, prop: string, cb: any, force?: boolean): void;
    unwatch(view: ReactiveESMView | null, prop: string, cb: any): boolean;
    disconnect_watchers(view: ReactiveESMView): void;
    protected _declare_importmap(): Promise<void>;
    protected _run_initializer(initialize: (props: any) => any): void;
    destroy(): void;
    init_module(): void;
    /**
     * The module whose `default.render(view)` renders a view of this model.
     */
    protected _render_module(): Promise<any>;
    protected _cached_module(key: string, load: () => Promise<any>): Promise<any>;
    get resolved_render_module(): any | null;
    protected _import_source(code: string): Promise<any>;
    compile(): string | null;
    get _module_cache_key(): string;
    recompile(): Promise<void>;
    static __module__: string;
}
//# sourceMappingURL=reactive_esm.d.ts.map