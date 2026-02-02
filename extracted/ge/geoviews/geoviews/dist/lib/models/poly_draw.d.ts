import type * as p from "@bokehjs/core/properties";
import type { Dict } from "@bokehjs/core/types";
import type { UIEvent } from "@bokehjs/core/ui_events";
import { PolyDrawTool, PolyDrawToolView } from "@bokehjs/models/tools/edit/poly_draw_tool";
import type { MultiLine } from "@bokehjs/models/glyphs/multi_line";
import type { Patches } from "@bokehjs/models/glyphs/patches";
export declare class PolyVertexDrawToolView extends PolyDrawToolView {
    model: PolyVertexDrawTool;
    _split_path(x: number, y: number): void;
    _snap_to_vertex(ev: UIEvent, x: number, y: number): [number, number];
    _set_vertices(xs: number[] | number, ys: number[] | number, styles?: any): void;
    _show_vertices(): void;
    _remove(): void;
}
export declare namespace PolyVertexDrawTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = PolyDrawTool.Props & {
        node_style: p.Property<Dict<unknown>>;
        end_style: p.Property<Dict<unknown>>;
    };
}
export interface PolyVertexDrawTool extends PolyVertexDrawTool.Attrs {
}
export interface HasPolyGlyph {
    glyph: MultiLine | Patches;
}
export declare class PolyVertexDrawTool extends PolyDrawTool {
    properties: PolyVertexDrawTool.Props;
    constructor(attrs?: Partial<PolyVertexDrawTool.Attrs>);
    static __module__: string;
}
//# sourceMappingURL=poly_draw.d.ts.map