import { XYGlyph, XYGlyphView } from "@bokehjs/models/glyphs/xy_glyph";
import type { PointGeometry } from "@bokehjs/core/geometry";
import type { Context2d } from "@bokehjs/core/util/canvas";
import type * as visuals from "@bokehjs/core/visuals";
import * as p from "@bokehjs/core/properties";
import { Selection } from "@bokehjs/models/selections/selection";
export interface WindBarbView extends WindBarb.Data {
}
export declare class WindBarbView extends XYGlyphView {
    model: WindBarb;
    visuals: WindBarb.Visuals;
    protected _paint(ctx: Context2d, indices: number[], data?: WindBarb.Data): void;
    protected _draw_wind_barb(ctx: Context2d, cx: number, cy: number, angle: number, magnitude: number, scale: number, idx?: number): void;
    protected _hit_point(geometry: PointGeometry): Selection;
    draw_legend_for_index(ctx: Context2d, { x0, x1, y0, y1 }: {
        x0: number;
        y0: number;
        x1: number;
        y1: number;
    }, _index: number): void;
}
export declare namespace WindBarb {
    type Attrs = p.AttrsOf<Props>;
    type Props = XYGlyph.Props & {
        angle: p.AngleSpec;
        magnitude: p.NumberSpec;
        scale: p.Property<number>;
        barb_length: p.Property<number>;
        barb_width: p.Property<number>;
        flag_width: p.Property<number>;
        spacing: p.Property<number>;
        calm_circle_radius: p.Property<number>;
    };
    type Visuals = XYGlyph.Visuals & {
        line: visuals.LineVector;
    };
    type Data = p.GlyphDataOf<Props>;
}
export interface WindBarb extends WindBarb.Attrs {
}
export declare class WindBarb extends XYGlyph {
    properties: WindBarb.Props;
    __view_type__: WindBarbView;
    constructor(attrs?: Partial<WindBarb.Attrs>);
    static __module__: string;
}
//# sourceMappingURL=wind_barb.d.ts.map