import type { Geometry } from "../../core/geometry";
import type { HasProps } from "../../core/has_props";
import type * as p from "../../core/properties";
import { SelectionManager } from "../../core/selection_manager";
import { Signal, Signal0 } from "../../core/signaling";
import type { Arrayable, Attrs, Data, Dict } from "../../core/types";
import type { PatchSet } from "../../core/patching";
import type { GlyphRenderer } from "../renderers/glyph_renderer";
import { SelectionPolicy } from "../selections/interaction_policy";
import { Selection } from "../selections/selection";
import { DataSource } from "./data_source";
import type { Index } from "../../core/util/templating";
export declare namespace ColumnarDataSource {
    type Attrs = p.AttrsOf<Props>;
    type Props = DataSource.Props & {
        data: p.Property<Data>;
        default_values: p.Property<Dict<unknown>>;
        selection_policy: p.Property<SelectionPolicy>;
        inspected: p.Property<Selection>;
    };
}
export interface ColumnarDataSource extends ColumnarDataSource.Attrs {
}
export declare abstract class ColumnarDataSource extends DataSource {
    properties: ColumnarDataSource.Props;
    data: Data;
    private _selection_sync;
    private _with_selection_sync;
    setv<T extends Attrs>(changed_attrs: Partial<T>, options?: HasProps.SetOptions): void;
    stream_to(prop: p.Property<Data>, new_data: Data, rollover?: number, options?: {
        sync?: boolean;
    }): void;
    patch_to(prop: p.Property<Data>, patches: PatchSet<unknown>, options?: {
        sync?: boolean;
    }): void;
    get_array<T>(key: string): T[];
    readonly _select: Signal0<this>;
    readonly inspect: Signal<[GlyphRenderer, {
        geometry: Geometry;
    }], this>;
    readonly selection_manager: SelectionManager;
    constructor(attrs?: Partial<ColumnarDataSource.Attrs>);
    get inferred_defaults(): Map<string, unknown>;
    get<T = unknown>(name: string): Arrayable<T>;
    set(name: string, column: Arrayable<unknown>): void;
    connect_signals(): void;
    protected _prune_selection(): void;
    get_column(name: string): Arrayable | null;
    get_row(index: Index): {
        [key: string]: unknown;
    };
    columns(): string[];
    get_length(soft?: boolean): number | null;
    get length(): number;
    clear(): void;
    stream(new_data: Data, rollover?: number, { sync }?: {
        sync?: boolean;
    }): void;
    patch(patches: PatchSet<unknown>, { sync }?: {
        sync?: boolean;
    }): void;
}
//# sourceMappingURL=columnar_data_source.d.ts.map