import { XYGlyph, XYGlyphView } from "@bokehjs/models/glyphs/xy_glyph";
import { LineVector } from "@bokehjs/core/property_mixins";
import * as p from "@bokehjs/core/properties";
import { Selection } from "@bokehjs/models/selections/selection";
export class WindBarbView extends XYGlyphView {
    static __name__ = "WindBarbView";
    _paint(ctx, indices, data) {
        const { sx, sy, angle, magnitude } = data ?? this;
        const y = this.y;
        const scale = this.model.scale;
        for (const i of indices) {
            const screen_x = sx[i];
            const screen_y = sy[i];
            const a = angle.get(i);
            const mag = magnitude.get(i);
            const lat = y[i];
            if (!isFinite(screen_x + screen_y + a + mag + lat))
                continue;
            this._draw_wind_barb(ctx, screen_x, screen_y, a, mag, scale, i);
        }
    }
    _draw_wind_barb(ctx, cx, cy, angle, magnitude, scale, idx = 0) {
        // Wind barb drawing using meteorological convention
        // magnitude is in knots (or appropriate units)
        // angle is in meteorological convention (direction wind comes FROM)
        // barbs point in the direction the wind is coming FROM
        const barb_length = this.model.barb_length * scale;
        const barb_width = this.model.barb_width * scale;
        const flag_width = this.model.flag_width * scale;
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(-angle);
        ctx.beginPath();
        this.visuals.line.apply(ctx, idx);
        ctx.strokeStyle = ctx.strokeStyle || "black";
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        // Determine barbs/flags based on magnitude
        // Standard increments: 50 knots = flag (triangle), 10 knots = full barb, 5 knots = half barb
        const mag_rounded = Math.round(magnitude / 5) * 5;
        if (mag_rounded >= 5) {
            // Draw the main staff (pointing in direction wind is coming from)
            ctx.moveTo(0, 0);
            ctx.lineTo(0, -barb_length);
            ctx.stroke();
            let remaining = mag_rounded;
            let y_offset = -barb_length;
            const spacing = this.model.spacing * scale;
            // Draw 50-knot flags (filled triangles)
            while (remaining >= 50) {
                ctx.fillStyle = ctx.strokeStyle || "black";
                ctx.beginPath();
                ctx.moveTo(0, y_offset);
                ctx.lineTo(flag_width, y_offset + spacing);
                ctx.lineTo(0, y_offset + spacing * 2);
                ctx.closePath();
                ctx.fill();
                y_offset += spacing * 2.5;
                remaining -= 50;
            }
            // Draw 10-knot barbs (full lines)
            while (remaining >= 10) {
                ctx.beginPath();
                ctx.moveTo(0, y_offset);
                ctx.lineTo(barb_width, y_offset + barb_width * 0.2);
                ctx.stroke();
                y_offset += spacing;
                remaining -= 10;
            }
            // Draw 5-knot half-barb
            if (remaining >= 5) {
                ctx.beginPath();
                ctx.moveTo(0, y_offset);
                ctx.lineTo(barb_width / 2, y_offset + barb_width * 0.1);
                ctx.stroke();
            }
        }
        else {
            // For calm winds (< 5 knots), draw only a circle (no staff line)
            ctx.beginPath();
            ctx.arc(0, 0, this.model.calm_circle_radius * scale, 0, 2 * Math.PI);
            ctx.stroke();
        }
        ctx.restore();
    }
    _hit_point(geometry) {
        const { sx, sy } = geometry;
        const candidates = [];
        for (let i = 0; i < this.data_size; i++) {
            const dx = this.sx[i] - sx;
            const dy = this.sy[i] - sy;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 10 * this.model.scale) { // Hit radius
                candidates.push(i);
            }
        }
        return new Selection({ indices: candidates });
    }
    draw_legend_for_index(ctx, { x0, x1, y0, y1 }, _index) {
        const cx = (x0 + x1) / 2;
        const cy = (y0 + y1) / 2;
        // Draw a representative wind barb in the legend
        this._draw_wind_barb(ctx, cx, cy, Math.PI / 4, 25, 0.5);
    }
}
export class WindBarb extends XYGlyph {
    static __name__ = "WindBarb";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "geoviews.models.wind_barb";
    static {
        this.prototype.default_view = WindBarbView;
        this.define(({ Float }) => ({
            angle: [p.AngleSpec, { value: 0 }],
            magnitude: [p.NumberSpec, { value: 0 }],
            scale: [Float, 1.0],
            barb_length: [Float, 30.0],
            barb_width: [Float, 15.0],
            flag_width: [Float, 15.0],
            spacing: [Float, 6.0],
            calm_circle_radius: [Float, 3.0],
        }));
        this.mixins(LineVector);
    }
}
//# sourceMappingURL=wind_barb.js.map