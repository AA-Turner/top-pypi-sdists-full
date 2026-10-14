'use strict';
/*!
 * Copyright (c) Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */
(function(root, factory) {
  factory(root["Bokeh"], "3.10.1");
})(this, function(Bokeh, version) {
  let define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" ? (version != null ? Bokeh[version] : Bokeh) : null;
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh" + (version != null ? " " + version : "") + ". You have to load it prior to loading plugins.");
    }
  })
({
639: /* models/glyphs/webgl/main.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    require(640) /* ./index */;
},
640: /* models/glyphs/webgl/index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require(1) /* tslib */;
    var regl_wrap_1 = require(641) /* ./regl_wrap */;
    __esExport("get_regl", regl_wrap_1.get_regl);
    tslib_1.__exportStar(require(655) /* ./annular_wedge */, exports);
    tslib_1.__exportStar(require(662) /* ./annulus */, exports);
    tslib_1.__exportStar(require(663) /* ./base_line */, exports);
    tslib_1.__exportStar(require(658) /* ./base_marker */, exports);
    tslib_1.__exportStar(require(664) /* ./circle */, exports);
    tslib_1.__exportStar(require(666) /* ./hex_tile */, exports);
    tslib_1.__exportStar(require(667) /* ./image */, exports);
    tslib_1.__exportStar(require(668) /* ./line_gl */, exports);
    tslib_1.__exportStar(require(670) /* ./lrtb */, exports);
    tslib_1.__exportStar(require(671) /* ./multi_line */, exports);
    tslib_1.__exportStar(require(672) /* ./patch */, exports);
    tslib_1.__exportStar(require(678) /* ./patches */, exports);
    tslib_1.__exportStar(require(679) /* ./multi_marker */, exports);
    tslib_1.__exportStar(require(680) /* ./ngon */, exports);
    tslib_1.__exportStar(require(681) /* ./rect */, exports);
    tslib_1.__exportStar(require(669) /* ./single_line */, exports);
    tslib_1.__exportStar(require(657) /* ./single_marker */, exports);
    tslib_1.__exportStar(require(682) /* ./step */, exports);
    tslib_1.__exportStar(require(683) /* ./wedge */, exports);
},
641: /* models/glyphs/webgl/regl_wrap.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.get_regl = get_regl;
    const tslib_1 = require(1) /* tslib */;
    const regl_1 = tslib_1.__importDefault(require(642) /* regl */);
    const dash_cache_1 = require(643) /* ./dash_cache */;
    const accumulate_vert_1 = tslib_1.__importDefault(require(645) /* ./accumulate.vert */);
    const accumulate_frag_1 = tslib_1.__importDefault(require(646) /* ./accumulate.frag */);
    const image_vert_1 = tslib_1.__importDefault(require(647) /* ./image.vert */);
    const image_frag_1 = tslib_1.__importDefault(require(648) /* ./image.frag */);
    const regl_line_vert_1 = tslib_1.__importDefault(require(649) /* ./regl_line.vert */);
    const regl_line_frag_1 = tslib_1.__importDefault(require(650) /* ./regl_line.frag */);
    const marker_vert_1 = tslib_1.__importDefault(require(651) /* ./marker.vert */);
    const marker_frag_1 = tslib_1.__importDefault(require(652) /* ./marker.frag */);
    const polygon_vert_1 = tslib_1.__importDefault(require(653) /* ./polygon.vert */);
    const polygon_frag_1 = tslib_1.__importDefault(require(654) /* ./polygon.frag */);
    // All access to regl is performed via the get_regl() function that returns a
    // ReglWrapper object.  This ensures that regl is correctly initialised before
    // it is used, and is only initialised once.
    let regl_wrapper = null;
    function get_regl(gl) {
        if (regl_wrapper == null) {
            regl_wrapper = new ReglWrapper(gl);
        }
        return regl_wrapper;
    }
    class ReglWrapper {
        _regl;
        _regl_available;
        _dash_cache;
        // Drawing functions.
        _accumulate;
        _image;
        _solid_line;
        _dashed_line;
        _polygon;
        _polygon_hatch;
        _marker_no_hatch_map = new Map();
        _marker_hatch_map = new Map();
        // Static Buffers/Elements
        _line_geometry;
        _line_triangles;
        _rect_geometry;
        _rect_triangles;
        // WebGL state variables.
        _scissor;
        _viewport;
        _scale_x = 1;
        _scale_y = 1;
        _clear_viewport;
        // WebGL framebuffer used to accumulate glyph rendering before single blit to Canvas.
        _framebuffer;
        _framebuffer_texture;
        constructor(gl) {
            try {
                this._regl = (0, regl_1.default)({
                    gl,
                    extensions: [
                        "ANGLE_instanced_arrays",
                        "EXT_blend_minmax",
                        "OES_element_index_uint",
                    ],
                });
                this._regl_available = true;
                // Initialise static Buffers/Elements.
                this._line_geometry = this._regl.buffer({
                    usage: "static",
                    type: "float",
                    data: [[-2, 0], [-1, -1], [1, -1], [1, 1], [-1, 1]],
                });
                this._line_triangles = this._regl.elements({
                    usage: "static",
                    primitive: "triangle fan",
                    data: [0, 1, 2, 3, 4],
                });
                this._rect_geometry = this._regl.buffer({
                    usage: "static",
                    type: "float",
                    data: [[-1, -1], [1, -1], [1, 1], [-1, 1]],
                });
                this._rect_triangles = this._regl.elements({
                    usage: "static",
                    primitive: "triangle fan",
                    data: [0, 1, 2, 3],
                });
            }
            catch (err) {
                this._regl_available = false;
            }
        }
        // Create and return ReGL Buffer.
        buffer(options) {
            return this._regl.buffer(options);
        }
        // Create and return ReGL Elements.
        elements(options) {
            return this._regl.elements(options);
        }
        clear(width, height) {
            // Plots exceeding the drawing buffer are scaled down into it
            const { drawingBufferWidth, drawingBufferHeight } = this._regl._gl;
            const vp_width = Math.min(width, drawingBufferWidth);
            const vp_height = Math.min(height, drawingBufferHeight);
            this._viewport = {
                x: 0,
                y: 0,
                width: vp_width,
                height: vp_height,
            };
            this._scale_x = isFinite(width) && width > 0 ? vp_width / width : 1;
            this._scale_y = isFinite(height) && height > 0 ? vp_height / height : 1;
            // Clear only the viewport, because the shared drawing buffer may be much larger
            this._clear_viewport ??= this._regl({ scissor: { enable: true, box: this._regl.prop("box") } });
            this._clear_viewport({ box: this._viewport }, () => this._regl.clear({ color: [0, 0, 0, 0] }));
        }
        clear_framebuffer(framebuffer) {
            this._regl.clear({ color: [0, 0, 0, 0], framebuffer });
        }
        get framebuffer_and_texture() {
            const { _regl, _viewport } = this;
            const size = {
                height: _viewport.height,
                width: _viewport.width,
            };
            if (this._framebuffer_texture == null) {
                this._framebuffer_texture = _regl.texture(size);
            }
            else {
                // Resize texture, no-op if no change.
                this._framebuffer_texture(size);
            }
            if (this._framebuffer == null) {
                this._framebuffer = _regl.framebuffer({
                    // Auto-sizes to size of texture.
                    color: this._framebuffer_texture,
                    depth: false,
                    stencil: false,
                });
            }
            return [this._framebuffer, this._framebuffer_texture];
        }
        get has_webgl() {
            return this._regl_available;
        }
        get scissor() {
            return this._scissor;
        }
        set_scissor(x, y, width, height) {
            const scale_x = this._scale_x;
            const scale_y = this._scale_y;
            const x0 = Math.floor(x * scale_x);
            const y0 = Math.floor(y * scale_y);
            const x1 = Math.ceil((x + width) * scale_x);
            const y1 = Math.ceil((y + height) * scale_y);
            const vx1 = this._viewport.width ?? 0;
            const vy1 = this._viewport.height ?? 0;
            const sx0 = Math.max(0, Math.min(vx1, x0));
            const sy0 = Math.max(0, Math.min(vy1, y0));
            const sx1 = Math.max(0, Math.min(vx1, x1));
            const sy1 = Math.max(0, Math.min(vy1, y1));
            this._scissor = {
                x: sx0,
                y: sy0,
                width: Math.max(0, sx1 - sx0),
                height: Math.max(0, sy1 - sy0),
            };
        }
        /** Return a device-pixel scissor tightly enclosing screen-space points,
         * intersected with the plot frame. Screen y coordinates increase downward,
         * whereas WebGL scissor coordinates increase upward. */
        scissor_for_points(points, padding, pixel_ratio) {
            let x0 = Infinity;
            let y0 = Infinity;
            let x1 = -Infinity;
            let y1 = -Infinity;
            for (let i = 0; i + 1 < points.length; i += 2) {
                const x = points[i];
                const y = points[i + 1];
                if (isFinite(x + y)) {
                    x0 = Math.min(x0, x);
                    y0 = Math.min(y0, y);
                    x1 = Math.max(x1, x);
                    y1 = Math.max(y1, y);
                }
            }
            if (!isFinite(x0 + y0 + x1 + y1)) {
                return { ...this._scissor, width: 0, height: 0 };
            }
            const scale_x = this._scale_x;
            const scale_y = this._scale_y;
            const viewport_width = this._viewport.width ?? 0;
            const viewport_height = this._viewport.height ?? 0;
            const left = Math.floor((x0 - padding) * pixel_ratio * scale_x);
            const right = Math.ceil((x1 + padding) * pixel_ratio * scale_x);
            const bottom = Math.floor(viewport_height - (y1 + padding) * pixel_ratio * scale_y);
            const top = Math.ceil(viewport_height - (y0 - padding) * pixel_ratio * scale_y);
            const { x: clip_x = 0, y: clip_y = 0, width: clip_width = 0, height: clip_height = 0 } = this._scissor;
            const sx0 = Math.max(0, clip_x, left);
            const sy0 = Math.max(0, clip_y, bottom);
            const sx1 = Math.min(viewport_width, clip_x + clip_width, right);
            const sy1 = Math.min(viewport_height, clip_y + clip_height, top);
            return {
                x: sx0,
                y: sy0,
                width: Math.max(0, sx1 - sx0),
                height: Math.max(0, sy1 - sy0),
            };
        }
        texture(options) {
            return this._regl.texture(options);
        }
        get viewport() {
            return this._viewport;
        }
        accumulate() {
            if (this._accumulate == null) {
                this._accumulate = regl_accumulate(this._regl, this._rect_geometry, this._rect_triangles);
            }
            return this._accumulate;
        }
        dashed_line() {
            if (this._dashed_line == null) {
                this._dashed_line = regl_dashed_line(this._regl, this._line_geometry, this._line_triangles);
            }
            return this._dashed_line;
        }
        get_dash(line_dash) {
            if (this._dash_cache == null) {
                this._dash_cache = new dash_cache_1.DashCache(this._regl);
            }
            return this._dash_cache.get(line_dash);
        }
        image() {
            if (this._image == null) {
                this._image = regl_image(this._regl, this._rect_geometry, this._rect_triangles);
            }
            return this._image;
        }
        polygon() {
            if (this._polygon == null) {
                this._polygon = regl_polygon(this._regl);
            }
            return this._polygon;
        }
        polygon_hatch() {
            if (this._polygon_hatch == null) {
                this._polygon_hatch = regl_polygon_hatch(this._regl);
            }
            return this._polygon_hatch;
        }
        marker_no_hatch(marker_type) {
            let func = this._marker_no_hatch_map.get(marker_type);
            if (func == null) {
                func = regl_marker(this._regl, marker_type);
                this._marker_no_hatch_map.set(marker_type, func);
            }
            return func;
        }
        marker_hatch(marker_type) {
            let func = this._marker_hatch_map.get(marker_type);
            if (func == null) {
                func = regl_marker_hatch(this._regl, marker_type);
                this._marker_hatch_map.set(marker_type, func);
            }
            return func;
        }
        solid_line() {
            if (this._solid_line == null) {
                this._solid_line = regl_solid_line(this._regl, this._line_geometry, this._line_triangles);
            }
            return this._solid_line;
        }
    }
    exports.ReglWrapper = ReglWrapper;
    function regl_accumulate(regl, geometry, triangles) {
        const config = {
            vert: accumulate_vert_1.default,
            frag: accumulate_frag_1.default,
            attributes: {
                a_position: {
                    buffer: geometry,
                    divisor: 0,
                },
            },
            uniforms: {
                u_framebuffer_tex: regl.prop("framebuffer_tex"),
            },
            elements: triangles,
            blend: {
                enable: true,
                func: {
                    srcRGB: "one",
                    srcAlpha: "one",
                    dstRGB: "one minus src alpha",
                    dstAlpha: "one minus src alpha",
                },
            },
            depth: { enable: false },
            scissor: {
                enable: true,
                box: regl.prop("scissor"),
            },
            viewport: regl.prop("viewport"),
        };
        return regl(config);
    }
    // Regl rendering functions are here as some will be reused, e.g. lines may also
    // be used around polygons or for bezier curves.
    function regl_image(regl, geometry, triangles) {
        const config = {
            vert: image_vert_1.default,
            frag: image_frag_1.default,
            attributes: {
                a_position: {
                    buffer: geometry,
                    divisor: 0,
                },
                a_bounds(_, props) {
                    return props.bounds.to_attribute_config();
                },
            },
            uniforms: {
                u_canvas_size: regl.prop("canvas_size"),
                u_tex: regl.prop("tex"),
                u_global_alpha: regl.prop("global_alpha"),
            },
            elements: triangles,
            blend: {
                enable: true,
                func: {
                    srcRGB: "one",
                    srcAlpha: "one",
                    dstRGB: "one minus src alpha",
                    dstAlpha: "one minus src alpha",
                },
            },
            depth: { enable: false },
            scissor: {
                enable: true,
                box: regl.prop("scissor"),
            },
            viewport: regl.prop("viewport"),
        };
        return regl(config);
    }
    // Mesh for line rendering (solid and dashed).
    //
    //   1       4-----3
    //          /      |
    //         /       |
    // y 0    0        |
    //         \       |
    //          \      |
    //  -1       1-----2
    //
    //       -2  -1    1
    //              x
    function regl_solid_line(regl, line_geometry, line_triangles) {
        const config = {
            vert: regl_line_vert_1.default,
            frag: regl_line_frag_1.default,
            attributes: {
                a_position: {
                    buffer: line_geometry,
                    divisor: 0,
                },
                a_point_prev(_, props) {
                    return props.points.to_attribute_config(props.point_offset);
                },
                a_point_start(_, props) {
                    return props.points.to_attribute_config(props.point_offset + 2);
                },
                a_point_end(_, props) {
                    return props.points.to_attribute_config(props.point_offset + 4);
                },
                a_point_next(_, props) {
                    return props.points.to_attribute_config(props.point_offset + 6);
                },
                a_show_prev(_, props) {
                    return props.show.to_attribute_config(props.point_offset / 2 - props.line_offset);
                },
                a_show_curr(_, props) {
                    return props.show.to_attribute_config(props.point_offset / 2 - props.line_offset + 1);
                },
                a_show_next(_, props) {
                    return props.show.to_attribute_config(props.point_offset / 2 - props.line_offset + 2);
                },
                a_linewidth(_, props) {
                    return props.linewidth.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_line_color(_, props) {
                    return props.line_color.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_line_cap(_, props) {
                    return props.line_cap.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_line_join(_, props) {
                    return props.line_join.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
            },
            uniforms: {
                u_canvas_size: regl.prop("canvas_size"),
                u_antialias: regl.prop("antialias"),
                u_miter_limit: regl.prop("miter_limit"),
            },
            elements: line_triangles,
            instances: regl.prop("nsegments"),
            blend: {
                enable: true,
                equation: "max",
                func: {
                    srcRGB: 1,
                    srcAlpha: 1,
                    dstRGB: 1,
                    dstAlpha: 1,
                },
            },
            depth: { enable: false },
            framebuffer: regl.prop("framebuffer"),
            scissor: {
                enable: true,
                box: regl.prop("scissor"),
            },
            viewport: regl.prop("viewport"),
        };
        return regl(config);
    }
    function regl_dashed_line(regl, line_geometry, line_triangles) {
        const config = {
            vert: `\
#define DASHED
${regl_line_vert_1.default}
`,
            frag: `\
#define DASHED
${regl_line_frag_1.default}
`,
            attributes: {
                a_position: {
                    buffer: line_geometry,
                    divisor: 0,
                },
                a_point_prev(_, props) {
                    return props.points.to_attribute_config(props.point_offset);
                },
                a_point_start(_, props) {
                    return props.points.to_attribute_config(props.point_offset + 2);
                },
                a_point_end(_, props) {
                    return props.points.to_attribute_config(props.point_offset + 4);
                },
                a_point_next(_, props) {
                    return props.points.to_attribute_config(props.point_offset + 6);
                },
                a_show_prev(_, props) {
                    return props.show.to_attribute_config(props.point_offset / 2 - props.line_offset);
                },
                a_show_curr(_, props) {
                    return props.show.to_attribute_config(props.point_offset / 2 - props.line_offset + 1);
                },
                a_show_next(_, props) {
                    return props.show.to_attribute_config(props.point_offset / 2 - props.line_offset + 2);
                },
                a_linewidth(_, props) {
                    return props.linewidth.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_line_color(_, props) {
                    return props.line_color.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_line_cap(_, props) {
                    return props.line_cap.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_line_join(_, props) {
                    return props.line_join.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_length_so_far(_, props) {
                    return props.length_so_far.to_attribute_config(props.point_offset / 2 - 3 * props.line_offset);
                },
                a_dash_tex_info(_, props) {
                    return props.dash_tex_info.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_dash_scale(_, props) {
                    return props.dash_scale.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
                a_dash_offset(_, props) {
                    return props.dash_offset.to_attribute_config_nested(props.line_offset, props.nsegments + 3);
                },
            },
            uniforms: {
                u_canvas_size: regl.prop("canvas_size"),
                u_antialias: regl.prop("antialias"),
                u_miter_limit: regl.prop("miter_limit"),
                u_dash_tex: regl.prop("dash_tex"),
            },
            elements: line_triangles,
            instances: regl.prop("nsegments"),
            blend: {
                enable: true,
                equation: "max",
                func: {
                    srcRGB: 1,
                    srcAlpha: 1,
                    dstRGB: 1,
                    dstAlpha: 1,
                },
            },
            depth: { enable: false },
            framebuffer: regl.prop("framebuffer"),
            scissor: {
                enable: true,
                box: regl.prop("scissor"),
            },
            viewport: regl.prop("viewport"),
        };
        return regl(config);
    }
    function regl_polygon(regl) {
        const config = {
            vert: polygon_vert_1.default,
            frag: polygon_frag_1.default,
            attributes: {
                a_position(_, props) {
                    return props.positions.to_per_vertex_config();
                },
                a_fill_color(_, props) {
                    return props.fill_color.to_per_vertex_config();
                },
                a_edge_distance(_, props) {
                    return props.edge_distance.to_per_vertex_config();
                },
            },
            uniforms: {
                u_canvas_size: regl.prop("canvas_size"),
                u_antialias: regl.prop("antialias"),
            },
            elements: regl.prop("elements"),
            count: regl.prop("count"),
            offset: regl.prop("offset"),
            blend: {
                enable: true,
                func: {
                    srcRGB: "one",
                    srcAlpha: "one",
                    dstRGB: "one minus src alpha",
                    dstAlpha: "one minus src alpha",
                },
            },
            depth: { enable: false },
            scissor: {
                enable: true,
                box: regl.prop("scissor"),
            },
            viewport: regl.prop("viewport"),
        };
        return regl(config);
    }
    function regl_polygon_hatch(regl) {
        const config = {
            vert: `\
#define HATCH
${polygon_vert_1.default}
`,
            frag: `\
#define HATCH
${polygon_frag_1.default}
`,
            attributes: {
                a_position(_, props) {
                    return props.positions.to_per_vertex_config();
                },
                a_fill_color(_, props) {
                    return props.fill_color.to_per_vertex_config();
                },
                a_edge_distance(_, props) {
                    return props.edge_distance.to_per_vertex_config();
                },
                a_hatch_pattern(_, props) {
                    return props.hatch_pattern.to_per_vertex_config();
                },
                a_hatch_scale(_, props) {
                    return props.hatch_scale.to_per_vertex_config();
                },
                a_hatch_weight(_, props) {
                    return props.hatch_weight.to_per_vertex_config();
                },
                a_hatch_color(_, props) {
                    return props.hatch_color.to_per_vertex_config();
                },
            },
            uniforms: {
                u_canvas_size: regl.prop("canvas_size"),
                u_antialias: regl.prop("antialias"),
            },
            elements: regl.prop("elements"),
            count: regl.prop("count"),
            offset: regl.prop("offset"),
            blend: {
                enable: true,
                func: {
                    srcRGB: "one",
                    srcAlpha: "one",
                    dstRGB: "one minus src alpha",
                    dstAlpha: "one minus src alpha",
                },
            },
            depth: { enable: false },
            scissor: {
                enable: true,
                box: regl.prop("scissor"),
            },
            viewport: regl.prop("viewport"),
        };
        return regl(config);
    }
    function regl_marker(regl, marker_type, vert_defs = [], frag_defs = [], attributes) {
        const vert_prefix = vert_defs.map((def) => `#define ${def}`).join("\n");
        const frag_prefix = frag_defs.map((def) => `#define ${def}`).join("\n");
        const config = {
            vert: `\
${vert_prefix}
#define MULTI_MARKER
#define USE_${marker_type.toUpperCase()}
${marker_vert_1.default}
`,
            frag: `\
${frag_prefix}
#define USE_${marker_type.toUpperCase()}
${marker_frag_1.default}
`,
            attributes: {
                a_position: {
                    buffer: regl.buffer([[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5]]),
                    divisor: 0,
                },
                a_center(_, props) {
                    return props.center.to_attribute_config(0, props.nmarkers);
                },
                a_width(_, props) {
                    return props.width.to_attribute_config(0, props.nmarkers);
                },
                a_height(_, props) {
                    return props.height.to_attribute_config(0, props.nmarkers);
                },
                a_angle(_, props) {
                    return props.angle.to_attribute_config(0, props.nmarkers);
                },
                a_aux(_, props) {
                    return props.aux.to_attribute_config(0, props.nmarkers);
                },
                a_linewidth(_, props) {
                    return props.linewidth.to_attribute_config(0, props.nmarkers);
                },
                a_line_color(_, props) {
                    return props.line_color.to_attribute_config(0, props.nmarkers);
                },
                a_fill_color(_, props) {
                    return props.fill_color.to_attribute_config(0, props.nmarkers);
                },
                a_line_cap(_, props) {
                    return props.line_cap.to_attribute_config(0, props.nmarkers);
                },
                a_line_join(_, props) {
                    return props.line_join.to_attribute_config(0, props.nmarkers);
                },
                a_show(_, props) {
                    return props.show.to_attribute_config(0, props.nmarkers);
                },
                ...attributes,
            },
            uniforms: {
                u_canvas_size: regl.prop("canvas_size"),
                u_antialias: regl.prop("antialias"),
                u_size_hint: regl.prop("size_hint"),
                u_border_radius: regl.prop("border_radius"),
            },
            count: 4,
            primitive: "triangle fan",
            instances: regl.prop("nmarkers"),
            blend: {
                enable: true,
                func: {
                    srcRGB: "one",
                    srcAlpha: "one",
                    dstRGB: "one minus src alpha",
                    dstAlpha: "one minus src alpha",
                },
            },
            depth: { enable: false },
            scissor: {
                enable: true,
                box: regl.prop("scissor"),
            },
            viewport: regl.prop("viewport"),
        };
        return regl(config);
    }
    function regl_marker_hatch(regl, marker_type) {
        const hatch_attributes = {
            a_hatch_pattern(_, props) {
                return props.hatch_pattern.to_attribute_config(0, props.nmarkers);
            },
            a_hatch_scale(_, props) {
                return props.hatch_scale.to_attribute_config(0, props.nmarkers);
            },
            a_hatch_weight(_, props) {
                return props.hatch_weight.to_attribute_config(0, props.nmarkers);
            },
            a_hatch_color(_, props) {
                return props.hatch_color.to_attribute_config(0, props.nmarkers);
            },
        };
        return regl_marker(regl, marker_type, ["HATCH"], ["HATCH"], hatch_attributes);
    }
},
642: /* regl/dist/regl.js */ function _(require, module, exports, __esModule, __esExport) {
    (function (global, factory) {
        typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
            typeof define === 'function' && define.amd ? define(factory) :
                (global.createREGL = factory());
    }(this, (function () {
        'use strict';
        var isTypedArray = function (x) {
            return (x instanceof Uint8Array ||
                x instanceof Uint16Array ||
                x instanceof Uint32Array ||
                x instanceof Int8Array ||
                x instanceof Int16Array ||
                x instanceof Int32Array ||
                x instanceof Float32Array ||
                x instanceof Float64Array ||
                x instanceof Uint8ClampedArray);
        };
        var extend = function (base, opts) {
            var keys = Object.keys(opts);
            for (var i = 0; i < keys.length; ++i) {
                base[keys[i]] = opts[keys[i]];
            }
            return base;
        };
        // Error checking and parameter validation.
        //
        // Statements for the form `check.someProcedure(...)` get removed by
        // a browserify transform for optimized/minified bundles.
        //
        /* globals atob */
        var endl = '\n';
        // only used for extracting shader names.  if atob not present, then errors
        // will be slightly crappier
        function decodeB64(str) {
            if (typeof atob !== 'undefined') {
                return atob(str);
            }
            return 'base64:' + str;
        }
        function raise(message) {
            var error = new Error('(regl) ' + message);
            console.error(error);
            throw error;
        }
        function check(pred, message) {
            if (!pred) {
                raise(message);
            }
        }
        function encolon(message) {
            if (message) {
                return ': ' + message;
            }
            return '';
        }
        function checkParameter(param, possibilities, message) {
            if (!(param in possibilities)) {
                raise('unknown parameter (' + param + ')' + encolon(message) +
                    '. possible values: ' + Object.keys(possibilities).join());
            }
        }
        function checkIsTypedArray(data, message) {
            if (!isTypedArray(data)) {
                raise('invalid parameter type' + encolon(message) +
                    '. must be a typed array');
            }
        }
        function standardTypeEh(value, type) {
            switch (type) {
                case 'number': return typeof value === 'number';
                case 'object': return typeof value === 'object';
                case 'string': return typeof value === 'string';
                case 'boolean': return typeof value === 'boolean';
                case 'function': return typeof value === 'function';
                case 'undefined': return typeof value === 'undefined';
                case 'symbol': return typeof value === 'symbol';
            }
        }
        function checkTypeOf(value, type, message) {
            if (!standardTypeEh(value, type)) {
                raise('invalid parameter type' + encolon(message) +
                    '. expected ' + type + ', got ' + (typeof value));
            }
        }
        function checkNonNegativeInt(value, message) {
            if (!((value >= 0) &&
                ((value | 0) === value))) {
                raise('invalid parameter type, (' + value + ')' + encolon(message) +
                    '. must be a nonnegative integer');
            }
        }
        function checkOneOf(value, list, message) {
            if (list.indexOf(value) < 0) {
                raise('invalid value' + encolon(message) + '. must be one of: ' + list);
            }
        }
        var constructorKeys = [
            'gl',
            'canvas',
            'container',
            'attributes',
            'pixelRatio',
            'extensions',
            'optionalExtensions',
            'profile',
            'onDone'
        ];
        function checkConstructor(obj) {
            Object.keys(obj).forEach(function (key) {
                if (constructorKeys.indexOf(key) < 0) {
                    raise('invalid regl constructor argument "' + key + '". must be one of ' + constructorKeys);
                }
            });
        }
        function leftPad(str, n) {
            str = str + '';
            while (str.length < n) {
                str = ' ' + str;
            }
            return str;
        }
        function ShaderFile() {
            this.name = 'unknown';
            this.lines = [];
            this.index = {};
            this.hasErrors = false;
        }
        function ShaderLine(number, line) {
            this.number = number;
            this.line = line;
            this.errors = [];
        }
        function ShaderError(fileNumber, lineNumber, message) {
            this.file = fileNumber;
            this.line = lineNumber;
            this.message = message;
        }
        function guessCommand() {
            var error = new Error();
            var stack = (error.stack || error).toString();
            var pat = /compileProcedure.*\n\s*at.*\((.*)\)/.exec(stack);
            if (pat) {
                return pat[1];
            }
            var pat2 = /compileProcedure.*\n\s*at\s+(.*)(\n|$)/.exec(stack);
            if (pat2) {
                return pat2[1];
            }
            return 'unknown';
        }
        function guessCallSite() {
            var error = new Error();
            var stack = (error.stack || error).toString();
            var pat = /at REGLCommand.*\n\s+at.*\((.*)\)/.exec(stack);
            if (pat) {
                return pat[1];
            }
            var pat2 = /at REGLCommand.*\n\s+at\s+(.*)\n/.exec(stack);
            if (pat2) {
                return pat2[1];
            }
            return 'unknown';
        }
        function parseSource(source, command) {
            var lines = source.split('\n');
            var lineNumber = 1;
            var fileNumber = 0;
            var files = {
                unknown: new ShaderFile(),
                0: new ShaderFile()
            };
            files.unknown.name = files[0].name = command || guessCommand();
            files.unknown.lines.push(new ShaderLine(0, ''));
            for (var i = 0; i < lines.length; ++i) {
                var line = lines[i];
                var parts = /^\s*#\s*(\w+)\s+(.+)\s*$/.exec(line);
                if (parts) {
                    switch (parts[1]) {
                        case 'line':
                            var lineNumberInfo = /(\d+)(\s+\d+)?/.exec(parts[2]);
                            if (lineNumberInfo) {
                                lineNumber = lineNumberInfo[1] | 0;
                                if (lineNumberInfo[2]) {
                                    fileNumber = lineNumberInfo[2] | 0;
                                    if (!(fileNumber in files)) {
                                        files[fileNumber] = new ShaderFile();
                                    }
                                }
                            }
                            break;
                        case 'define':
                            var nameInfo = /SHADER_NAME(_B64)?\s+(.*)$/.exec(parts[2]);
                            if (nameInfo) {
                                files[fileNumber].name = (nameInfo[1]
                                    ? decodeB64(nameInfo[2])
                                    : nameInfo[2]);
                            }
                            break;
                    }
                }
                files[fileNumber].lines.push(new ShaderLine(lineNumber++, line));
            }
            Object.keys(files).forEach(function (fileNumber) {
                var file = files[fileNumber];
                file.lines.forEach(function (line) {
                    file.index[line.number] = line;
                });
            });
            return files;
        }
        function parseErrorLog(errLog) {
            var result = [];
            errLog.split('\n').forEach(function (errMsg) {
                if (errMsg.length < 5) {
                    return;
                }
                var parts = /^ERROR:\s+(\d+):(\d+):\s*(.*)$/.exec(errMsg);
                if (parts) {
                    result.push(new ShaderError(parts[1] | 0, parts[2] | 0, parts[3].trim()));
                }
                else if (errMsg.length > 0) {
                    result.push(new ShaderError('unknown', 0, errMsg));
                }
            });
            return result;
        }
        function annotateFiles(files, errors) {
            errors.forEach(function (error) {
                var file = files[error.file];
                if (file) {
                    var line = file.index[error.line];
                    if (line) {
                        line.errors.push(error);
                        file.hasErrors = true;
                        return;
                    }
                }
                files.unknown.hasErrors = true;
                files.unknown.lines[0].errors.push(error);
            });
        }
        function checkShaderError(gl, shader, source, type, command) {
            if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
                var errLog = gl.getShaderInfoLog(shader);
                var typeName = type === gl.FRAGMENT_SHADER ? 'fragment' : 'vertex';
                checkCommandType(source, 'string', typeName + ' shader source must be a string', command);
                var files = parseSource(source, command);
                var errors = parseErrorLog(errLog);
                annotateFiles(files, errors);
                Object.keys(files).forEach(function (fileNumber) {
                    var file = files[fileNumber];
                    if (!file.hasErrors) {
                        return;
                    }
                    var strings = [''];
                    var styles = [''];
                    function push(str, style) {
                        strings.push(str);
                        styles.push(style || '');
                    }
                    push('file number ' + fileNumber + ': ' + file.name + '\n', 'color:red;text-decoration:underline;font-weight:bold');
                    file.lines.forEach(function (line) {
                        if (line.errors.length > 0) {
                            push(leftPad(line.number, 4) + '|  ', 'background-color:yellow; font-weight:bold');
                            push(line.line + endl, 'color:red; background-color:yellow; font-weight:bold');
                            // try to guess token
                            var offset = 0;
                            line.errors.forEach(function (error) {
                                var message = error.message;
                                var token = /^\s*'(.*)'\s*:\s*(.*)$/.exec(message);
                                if (token) {
                                    var tokenPat = token[1];
                                    message = token[2];
                                    switch (tokenPat) {
                                        case 'assign':
                                            tokenPat = '=';
                                            break;
                                    }
                                    offset = Math.max(line.line.indexOf(tokenPat, offset), 0);
                                }
                                else {
                                    offset = 0;
                                }
                                push(leftPad('| ', 6));
                                push(leftPad('^^^', offset + 3) + endl, 'font-weight:bold');
                                push(leftPad('| ', 6));
                                push(message + endl, 'font-weight:bold');
                            });
                            push(leftPad('| ', 6) + endl);
                        }
                        else {
                            push(leftPad(line.number, 4) + '|  ');
                            push(line.line + endl, 'color:red');
                        }
                    });
                    if (typeof document !== 'undefined' && !window.chrome) {
                        styles[0] = strings.join('%c');
                        console.log.apply(console, styles);
                    }
                    else {
                        console.log(strings.join(''));
                    }
                });
                check.raise('Error compiling ' + typeName + ' shader, ' + files[0].name);
            }
        }
        function checkLinkError(gl, program, fragShader, vertShader, command) {
            if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
                var errLog = gl.getProgramInfoLog(program);
                var fragParse = parseSource(fragShader, command);
                var vertParse = parseSource(vertShader, command);
                var header = 'Error linking program with vertex shader, "' +
                    vertParse[0].name + '", and fragment shader "' + fragParse[0].name + '"';
                if (typeof document !== 'undefined') {
                    console.log('%c' + header + endl + '%c' + errLog, 'color:red;text-decoration:underline;font-weight:bold', 'color:red');
                }
                else {
                    console.log(header + endl + errLog);
                }
                check.raise(header);
            }
        }
        function saveCommandRef(object) {
            object._commandRef = guessCommand();
        }
        function saveDrawCommandInfo(opts, uniforms, attributes, stringStore) {
            saveCommandRef(opts);
            function id(str) {
                if (str) {
                    return stringStore.id(str);
                }
                return 0;
            }
            opts._fragId = id(opts.static.frag);
            opts._vertId = id(opts.static.vert);
            function addProps(dict, set) {
                Object.keys(set).forEach(function (u) {
                    dict[stringStore.id(u)] = true;
                });
            }
            var uniformSet = opts._uniformSet = {};
            addProps(uniformSet, uniforms.static);
            addProps(uniformSet, uniforms.dynamic);
            var attributeSet = opts._attributeSet = {};
            addProps(attributeSet, attributes.static);
            addProps(attributeSet, attributes.dynamic);
            opts._hasCount = ('count' in opts.static ||
                'count' in opts.dynamic ||
                'elements' in opts.static ||
                'elements' in opts.dynamic);
        }
        function commandRaise(message, command) {
            var callSite = guessCallSite();
            raise(message +
                ' in command ' + (command || guessCommand()) +
                (callSite === 'unknown' ? '' : ' called from ' + callSite));
        }
        function checkCommand(pred, message, command) {
            if (!pred) {
                commandRaise(message, command || guessCommand());
            }
        }
        function checkParameterCommand(param, possibilities, message, command) {
            if (!(param in possibilities)) {
                commandRaise('unknown parameter (' + param + ')' + encolon(message) +
                    '. possible values: ' + Object.keys(possibilities).join(), command || guessCommand());
            }
        }
        function checkCommandType(value, type, message, command) {
            if (!standardTypeEh(value, type)) {
                commandRaise('invalid parameter type' + encolon(message) +
                    '. expected ' + type + ', got ' + (typeof value), command || guessCommand());
            }
        }
        function checkOptional(block) {
            block();
        }
        function checkFramebufferFormat(attachment, texFormats, rbFormats) {
            if (attachment.texture) {
                checkOneOf(attachment.texture._texture.internalformat, texFormats, 'unsupported texture format for attachment');
            }
            else {
                checkOneOf(attachment.renderbuffer._renderbuffer.format, rbFormats, 'unsupported renderbuffer format for attachment');
            }
        }
        var GL_CLAMP_TO_EDGE = 0x812F;
        var GL_NEAREST = 0x2600;
        var GL_NEAREST_MIPMAP_NEAREST = 0x2700;
        var GL_LINEAR_MIPMAP_NEAREST = 0x2701;
        var GL_NEAREST_MIPMAP_LINEAR = 0x2702;
        var GL_LINEAR_MIPMAP_LINEAR = 0x2703;
        var GL_BYTE = 5120;
        var GL_UNSIGNED_BYTE = 5121;
        var GL_SHORT = 5122;
        var GL_UNSIGNED_SHORT = 5123;
        var GL_INT = 5124;
        var GL_UNSIGNED_INT = 5125;
        var GL_FLOAT = 5126;
        var GL_UNSIGNED_SHORT_4_4_4_4 = 0x8033;
        var GL_UNSIGNED_SHORT_5_5_5_1 = 0x8034;
        var GL_UNSIGNED_SHORT_5_6_5 = 0x8363;
        var GL_UNSIGNED_INT_24_8_WEBGL = 0x84FA;
        var GL_HALF_FLOAT_OES = 0x8D61;
        var TYPE_SIZE = {};
        TYPE_SIZE[GL_BYTE] =
            TYPE_SIZE[GL_UNSIGNED_BYTE] = 1;
        TYPE_SIZE[GL_SHORT] =
            TYPE_SIZE[GL_UNSIGNED_SHORT] =
                TYPE_SIZE[GL_HALF_FLOAT_OES] =
                    TYPE_SIZE[GL_UNSIGNED_SHORT_5_6_5] =
                        TYPE_SIZE[GL_UNSIGNED_SHORT_4_4_4_4] =
                            TYPE_SIZE[GL_UNSIGNED_SHORT_5_5_5_1] = 2;
        TYPE_SIZE[GL_INT] =
            TYPE_SIZE[GL_UNSIGNED_INT] =
                TYPE_SIZE[GL_FLOAT] =
                    TYPE_SIZE[GL_UNSIGNED_INT_24_8_WEBGL] = 4;
        function pixelSize(type, channels) {
            if (type === GL_UNSIGNED_SHORT_5_5_5_1 ||
                type === GL_UNSIGNED_SHORT_4_4_4_4 ||
                type === GL_UNSIGNED_SHORT_5_6_5) {
                return 2;
            }
            else if (type === GL_UNSIGNED_INT_24_8_WEBGL) {
                return 4;
            }
            else {
                return TYPE_SIZE[type] * channels;
            }
        }
        function isPow2(v) {
            return !(v & (v - 1)) && (!!v);
        }
        function checkTexture2D(info, mipData, limits) {
            var i;
            var w = mipData.width;
            var h = mipData.height;
            var c = mipData.channels;
            // Check texture shape
            check(w > 0 && w <= limits.maxTextureSize &&
                h > 0 && h <= limits.maxTextureSize, 'invalid texture shape');
            // check wrap mode
            if (info.wrapS !== GL_CLAMP_TO_EDGE || info.wrapT !== GL_CLAMP_TO_EDGE) {
                check(isPow2(w) && isPow2(h), 'incompatible wrap mode for texture, both width and height must be power of 2');
            }
            if (mipData.mipmask === 1) {
                if (w !== 1 && h !== 1) {
                    check(info.minFilter !== GL_NEAREST_MIPMAP_NEAREST &&
                        info.minFilter !== GL_NEAREST_MIPMAP_LINEAR &&
                        info.minFilter !== GL_LINEAR_MIPMAP_NEAREST &&
                        info.minFilter !== GL_LINEAR_MIPMAP_LINEAR, 'min filter requires mipmap');
                }
            }
            else {
                // texture must be power of 2
                check(isPow2(w) && isPow2(h), 'texture must be a square power of 2 to support mipmapping');
                check(mipData.mipmask === (w << 1) - 1, 'missing or incomplete mipmap data');
            }
            if (mipData.type === GL_FLOAT) {
                if (limits.extensions.indexOf('oes_texture_float_linear') < 0) {
                    check(info.minFilter === GL_NEAREST && info.magFilter === GL_NEAREST, 'filter not supported, must enable oes_texture_float_linear');
                }
                check(!info.genMipmaps, 'mipmap generation not supported with float textures');
            }
            // check image complete
            var mipimages = mipData.images;
            for (i = 0; i < 16; ++i) {
                if (mipimages[i]) {
                    var mw = w >> i;
                    var mh = h >> i;
                    check(mipData.mipmask & (1 << i), 'missing mipmap data');
                    var img = mipimages[i];
                    check(img.width === mw &&
                        img.height === mh, 'invalid shape for mip images');
                    check(img.format === mipData.format &&
                        img.internalformat === mipData.internalformat &&
                        img.type === mipData.type, 'incompatible type for mip image');
                    if (img.compressed) {
                        // TODO: check size for compressed images
                    }
                    else if (img.data) {
                        // check(img.data.byteLength === mw * mh *
                        // Math.max(pixelSize(img.type, c), img.unpackAlignment),
                        var rowSize = Math.ceil(pixelSize(img.type, c) * mw / img.unpackAlignment) * img.unpackAlignment;
                        check(img.data.byteLength === rowSize * mh, 'invalid data for image, buffer size is inconsistent with image format');
                    }
                    else if (img.element) {
                        // TODO: check element can be loaded
                    }
                    else if (img.copy) {
                        // TODO: check compatible format and type
                    }
                }
                else if (!info.genMipmaps) {
                    check((mipData.mipmask & (1 << i)) === 0, 'extra mipmap data');
                }
            }
            if (mipData.compressed) {
                check(!info.genMipmaps, 'mipmap generation for compressed images not supported');
            }
        }
        function checkTextureCube(texture, info, faces, limits) {
            var w = texture.width;
            var h = texture.height;
            var c = texture.channels;
            // Check texture shape
            check(w > 0 && w <= limits.maxTextureSize && h > 0 && h <= limits.maxTextureSize, 'invalid texture shape');
            check(w === h, 'cube map must be square');
            check(info.wrapS === GL_CLAMP_TO_EDGE && info.wrapT === GL_CLAMP_TO_EDGE, 'wrap mode not supported by cube map');
            for (var i = 0; i < faces.length; ++i) {
                var face = faces[i];
                check(face.width === w && face.height === h, 'inconsistent cube map face shape');
                if (info.genMipmaps) {
                    check(!face.compressed, 'can not generate mipmap for compressed textures');
                    check(face.mipmask === 1, 'can not specify mipmaps and generate mipmaps');
                }
                else {
                    // TODO: check mip and filter mode
                }
                var mipmaps = face.images;
                for (var j = 0; j < 16; ++j) {
                    var img = mipmaps[j];
                    if (img) {
                        var mw = w >> j;
                        var mh = h >> j;
                        check(face.mipmask & (1 << j), 'missing mipmap data');
                        check(img.width === mw &&
                            img.height === mh, 'invalid shape for mip images');
                        check(img.format === texture.format &&
                            img.internalformat === texture.internalformat &&
                            img.type === texture.type, 'incompatible type for mip image');
                        if (img.compressed) {
                            // TODO: check size for compressed images
                        }
                        else if (img.data) {
                            check(img.data.byteLength === mw * mh *
                                Math.max(pixelSize(img.type, c), img.unpackAlignment), 'invalid data for image, buffer size is inconsistent with image format');
                        }
                        else if (img.element) {
                            // TODO: check element can be loaded
                        }
                        else if (img.copy) {
                            // TODO: check compatible format and type
                        }
                    }
                }
            }
        }
        var check$1 = extend(check, {
            optional: checkOptional,
            raise: raise,
            commandRaise: commandRaise,
            command: checkCommand,
            parameter: checkParameter,
            commandParameter: checkParameterCommand,
            constructor: checkConstructor,
            type: checkTypeOf,
            commandType: checkCommandType,
            isTypedArray: checkIsTypedArray,
            nni: checkNonNegativeInt,
            oneOf: checkOneOf,
            shaderError: checkShaderError,
            linkError: checkLinkError,
            callSite: guessCallSite,
            saveCommandRef: saveCommandRef,
            saveDrawInfo: saveDrawCommandInfo,
            framebufferFormat: checkFramebufferFormat,
            guessCommand: guessCommand,
            texture2D: checkTexture2D,
            textureCube: checkTextureCube
        });
        var VARIABLE_COUNTER = 0;
        var DYN_FUNC = 0;
        var DYN_CONSTANT = 5;
        var DYN_ARRAY = 6;
        function DynamicVariable(type, data) {
            this.id = (VARIABLE_COUNTER++);
            this.type = type;
            this.data = data;
        }
        function escapeStr(str) {
            return str.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
        }
        function splitParts(str) {
            if (str.length === 0) {
                return [];
            }
            var firstChar = str.charAt(0);
            var lastChar = str.charAt(str.length - 1);
            if (str.length > 1 &&
                firstChar === lastChar &&
                (firstChar === '"' || firstChar === "'")) {
                return ['"' + escapeStr(str.substr(1, str.length - 2)) + '"'];
            }
            var parts = /\[(false|true|null|\d+|'[^']*'|"[^"]*")\]/.exec(str);
            if (parts) {
                return (splitParts(str.substr(0, parts.index))
                    .concat(splitParts(parts[1]))
                    .concat(splitParts(str.substr(parts.index + parts[0].length))));
            }
            var subparts = str.split('.');
            if (subparts.length === 1) {
                return ['"' + escapeStr(str) + '"'];
            }
            var result = [];
            for (var i = 0; i < subparts.length; ++i) {
                result = result.concat(splitParts(subparts[i]));
            }
            return result;
        }
        function toAccessorString(str) {
            return '[' + splitParts(str).join('][') + ']';
        }
        function defineDynamic(type, data) {
            return new DynamicVariable(type, toAccessorString(data + ''));
        }
        function isDynamic(x) {
            return (typeof x === 'function' && !x._reglType) || (x instanceof DynamicVariable);
        }
        function unbox(x, path) {
            if (typeof x === 'function') {
                return new DynamicVariable(DYN_FUNC, x);
            }
            else if (typeof x === 'number' || typeof x === 'boolean') {
                return new DynamicVariable(DYN_CONSTANT, x);
            }
            else if (Array.isArray(x)) {
                return new DynamicVariable(DYN_ARRAY, x.map(function (y, i) { return unbox(y, path + '[' + i + ']'); }));
            }
            else if (x instanceof DynamicVariable) {
                return x;
            }
            check$1(false, 'invalid option type in uniform ' + path);
        }
        var dynamic = {
            DynamicVariable: DynamicVariable,
            define: defineDynamic,
            isDynamic: isDynamic,
            unbox: unbox,
            accessor: toAccessorString
        };
        /* globals requestAnimationFrame, cancelAnimationFrame */
        var raf = {
            next: typeof requestAnimationFrame === 'function'
                ? function (cb) { return requestAnimationFrame(cb); }
                : function (cb) { return setTimeout(cb, 16); },
            cancel: typeof cancelAnimationFrame === 'function'
                ? function (raf) { return cancelAnimationFrame(raf); }
                : clearTimeout
        };
        /* globals performance */
        var clock = (typeof performance !== 'undefined' && performance.now)
            ? function () { return performance.now(); }
            : function () { return +(new Date()); };
        function createStringStore() {
            var stringIds = { '': 0 };
            var stringValues = [''];
            return {
                id: function (str) {
                    var result = stringIds[str];
                    if (result) {
                        return result;
                    }
                    result = stringIds[str] = stringValues.length;
                    stringValues.push(str);
                    return result;
                },
                str: function (id) {
                    return stringValues[id];
                }
            };
        }
        // Context and canvas creation helper functions
        function createCanvas(element, onDone, pixelRatio) {
            var canvas = document.createElement('canvas');
            extend(canvas.style, {
                border: 0,
                margin: 0,
                padding: 0,
                top: 0,
                left: 0,
                width: '100%',
                height: '100%'
            });
            element.appendChild(canvas);
            if (element === document.body) {
                canvas.style.position = 'absolute';
                extend(element.style, {
                    margin: 0,
                    padding: 0
                });
            }
            function resize() {
                var w = window.innerWidth;
                var h = window.innerHeight;
                if (element !== document.body) {
                    var bounds = canvas.getBoundingClientRect();
                    w = bounds.right - bounds.left;
                    h = bounds.bottom - bounds.top;
                }
                canvas.width = pixelRatio * w;
                canvas.height = pixelRatio * h;
            }
            var resizeObserver;
            if (element !== document.body && typeof ResizeObserver === 'function') {
                // ignore 'ResizeObserver' is not defined
                // eslint-disable-next-line
                resizeObserver = new ResizeObserver(function () {
                    // setTimeout to avoid flicker
                    setTimeout(resize);
                });
                resizeObserver.observe(element);
            }
            else {
                window.addEventListener('resize', resize, false);
            }
            function onDestroy() {
                if (resizeObserver) {
                    resizeObserver.disconnect();
                }
                else {
                    window.removeEventListener('resize', resize);
                }
                element.removeChild(canvas);
            }
            resize();
            return {
                canvas: canvas,
                onDestroy: onDestroy
            };
        }
        function createContext(canvas, contextAttributes) {
            function get(name) {
                try {
                    return canvas.getContext(name, contextAttributes);
                }
                catch (e) {
                    return null;
                }
            }
            return (get('webgl') ||
                get('experimental-webgl') ||
                get('webgl-experimental'));
        }
        function isHTMLElement(obj) {
            return (typeof obj.nodeName === 'string' &&
                typeof obj.appendChild === 'function' &&
                typeof obj.getBoundingClientRect === 'function');
        }
        function isWebGLContext(obj) {
            return (typeof obj.drawArrays === 'function' ||
                typeof obj.drawElements === 'function');
        }
        function parseExtensions(input) {
            if (typeof input === 'string') {
                return input.split();
            }
            check$1(Array.isArray(input), 'invalid extension array');
            return input;
        }
        function getElement(desc) {
            if (typeof desc === 'string') {
                check$1(typeof document !== 'undefined', 'not supported outside of DOM');
                return document.querySelector(desc);
            }
            return desc;
        }
        function parseArgs(args_) {
            var args = args_ || {};
            var element, container, canvas, gl;
            var contextAttributes = {};
            var extensions = [];
            var optionalExtensions = [];
            var pixelRatio = (typeof window === 'undefined' ? 1 : window.devicePixelRatio);
            var profile = false;
            var onDone = function (err) {
                if (err) {
                    check$1.raise(err);
                }
            };
            var onDestroy = function () { };
            if (typeof args === 'string') {
                check$1(typeof document !== 'undefined', 'selector queries only supported in DOM enviroments');
                element = document.querySelector(args);
                check$1(element, 'invalid query string for element');
            }
            else if (typeof args === 'object') {
                if (isHTMLElement(args)) {
                    element = args;
                }
                else if (isWebGLContext(args)) {
                    gl = args;
                    canvas = gl.canvas;
                }
                else {
                    check$1.constructor(args);
                    if ('gl' in args) {
                        gl = args.gl;
                    }
                    else if ('canvas' in args) {
                        canvas = getElement(args.canvas);
                    }
                    else if ('container' in args) {
                        container = getElement(args.container);
                    }
                    if ('attributes' in args) {
                        contextAttributes = args.attributes;
                        check$1.type(contextAttributes, 'object', 'invalid context attributes');
                    }
                    if ('extensions' in args) {
                        extensions = parseExtensions(args.extensions);
                    }
                    if ('optionalExtensions' in args) {
                        optionalExtensions = parseExtensions(args.optionalExtensions);
                    }
                    if ('onDone' in args) {
                        check$1.type(args.onDone, 'function', 'invalid or missing onDone callback');
                        onDone = args.onDone;
                    }
                    if ('profile' in args) {
                        profile = !!args.profile;
                    }
                    if ('pixelRatio' in args) {
                        pixelRatio = +args.pixelRatio;
                        check$1(pixelRatio > 0, 'invalid pixel ratio');
                    }
                }
            }
            else {
                check$1.raise('invalid arguments to regl');
            }
            if (element) {
                if (element.nodeName.toLowerCase() === 'canvas') {
                    canvas = element;
                }
                else {
                    container = element;
                }
            }
            if (!gl) {
                if (!canvas) {
                    check$1(typeof document !== 'undefined', 'must manually specify webgl context outside of DOM environments');
                    var result = createCanvas(container || document.body, onDone, pixelRatio);
                    if (!result) {
                        return null;
                    }
                    canvas = result.canvas;
                    onDestroy = result.onDestroy;
                }
                // workaround for chromium bug, premultiplied alpha value is platform dependent
                if (contextAttributes.premultipliedAlpha === undefined)
                    contextAttributes.premultipliedAlpha = true;
                gl = createContext(canvas, contextAttributes);
            }
            if (!gl) {
                onDestroy();
                onDone('webgl not supported, try upgrading your browser or graphics drivers http://get.webgl.org');
                return null;
            }
            return {
                gl: gl,
                canvas: canvas,
                container: container,
                extensions: extensions,
                optionalExtensions: optionalExtensions,
                pixelRatio: pixelRatio,
                profile: profile,
                onDone: onDone,
                onDestroy: onDestroy
            };
        }
        function createExtensionCache(gl, config) {
            var extensions = {};
            function tryLoadExtension(name_) {
                check$1.type(name_, 'string', 'extension name must be string');
                var name = name_.toLowerCase();
                var ext;
                try {
                    ext = extensions[name] = gl.getExtension(name);
                }
                catch (e) { }
                return !!ext;
            }
            for (var i = 0; i < config.extensions.length; ++i) {
                var name = config.extensions[i];
                if (!tryLoadExtension(name)) {
                    config.onDestroy();
                    config.onDone('"' + name + '" extension is not supported by the current WebGL context, try upgrading your system or a different browser');
                    return null;
                }
            }
            config.optionalExtensions.forEach(tryLoadExtension);
            return {
                extensions: extensions,
                restore: function () {
                    Object.keys(extensions).forEach(function (name) {
                        if (extensions[name] && !tryLoadExtension(name)) {
                            throw new Error('(regl): error restoring extension ' + name);
                        }
                    });
                }
            };
        }
        function loop(n, f) {
            var result = Array(n);
            for (var i = 0; i < n; ++i) {
                result[i] = f(i);
            }
            return result;
        }
        var GL_BYTE$1 = 5120;
        var GL_UNSIGNED_BYTE$2 = 5121;
        var GL_SHORT$1 = 5122;
        var GL_UNSIGNED_SHORT$1 = 5123;
        var GL_INT$1 = 5124;
        var GL_UNSIGNED_INT$1 = 5125;
        var GL_FLOAT$2 = 5126;
        function nextPow16(v) {
            for (var i = 16; i <= (1 << 28); i *= 16) {
                if (v <= i) {
                    return i;
                }
            }
            return 0;
        }
        function log2(v) {
            var r, shift;
            r = (v > 0xFFFF) << 4;
            v >>>= r;
            shift = (v > 0xFF) << 3;
            v >>>= shift;
            r |= shift;
            shift = (v > 0xF) << 2;
            v >>>= shift;
            r |= shift;
            shift = (v > 0x3) << 1;
            v >>>= shift;
            r |= shift;
            return r | (v >> 1);
        }
        function createPool() {
            var bufferPool = loop(8, function () {
                return [];
            });
            function alloc(n) {
                var sz = nextPow16(n);
                var bin = bufferPool[log2(sz) >> 2];
                if (bin.length > 0) {
                    return bin.pop();
                }
                return new ArrayBuffer(sz);
            }
            function free(buf) {
                bufferPool[log2(buf.byteLength) >> 2].push(buf);
            }
            function allocType(type, n) {
                var result = null;
                switch (type) {
                    case GL_BYTE$1:
                        result = new Int8Array(alloc(n), 0, n);
                        break;
                    case GL_UNSIGNED_BYTE$2:
                        result = new Uint8Array(alloc(n), 0, n);
                        break;
                    case GL_SHORT$1:
                        result = new Int16Array(alloc(2 * n), 0, n);
                        break;
                    case GL_UNSIGNED_SHORT$1:
                        result = new Uint16Array(alloc(2 * n), 0, n);
                        break;
                    case GL_INT$1:
                        result = new Int32Array(alloc(4 * n), 0, n);
                        break;
                    case GL_UNSIGNED_INT$1:
                        result = new Uint32Array(alloc(4 * n), 0, n);
                        break;
                    case GL_FLOAT$2:
                        result = new Float32Array(alloc(4 * n), 0, n);
                        break;
                    default:
                        return null;
                }
                if (result.length !== n) {
                    return result.subarray(0, n);
                }
                return result;
            }
            function freeType(array) {
                free(array.buffer);
            }
            return {
                alloc: alloc,
                free: free,
                allocType: allocType,
                freeType: freeType
            };
        }
        var pool = createPool();
        // zero pool for initial zero data
        pool.zero = createPool();
        var GL_SUBPIXEL_BITS = 0x0D50;
        var GL_RED_BITS = 0x0D52;
        var GL_GREEN_BITS = 0x0D53;
        var GL_BLUE_BITS = 0x0D54;
        var GL_ALPHA_BITS = 0x0D55;
        var GL_DEPTH_BITS = 0x0D56;
        var GL_STENCIL_BITS = 0x0D57;
        var GL_ALIASED_POINT_SIZE_RANGE = 0x846D;
        var GL_ALIASED_LINE_WIDTH_RANGE = 0x846E;
        var GL_MAX_TEXTURE_SIZE = 0x0D33;
        var GL_MAX_VIEWPORT_DIMS = 0x0D3A;
        var GL_MAX_VERTEX_ATTRIBS = 0x8869;
        var GL_MAX_VERTEX_UNIFORM_VECTORS = 0x8DFB;
        var GL_MAX_VARYING_VECTORS = 0x8DFC;
        var GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS = 0x8B4D;
        var GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS = 0x8B4C;
        var GL_MAX_TEXTURE_IMAGE_UNITS = 0x8872;
        var GL_MAX_FRAGMENT_UNIFORM_VECTORS = 0x8DFD;
        var GL_MAX_CUBE_MAP_TEXTURE_SIZE = 0x851C;
        var GL_MAX_RENDERBUFFER_SIZE = 0x84E8;
        var GL_VENDOR = 0x1F00;
        var GL_RENDERER = 0x1F01;
        var GL_VERSION = 0x1F02;
        var GL_SHADING_LANGUAGE_VERSION = 0x8B8C;
        var GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FF;
        var GL_MAX_COLOR_ATTACHMENTS_WEBGL = 0x8CDF;
        var GL_MAX_DRAW_BUFFERS_WEBGL = 0x8824;
        var GL_TEXTURE_2D = 0x0DE1;
        var GL_TEXTURE_CUBE_MAP = 0x8513;
        var GL_TEXTURE_CUBE_MAP_POSITIVE_X = 0x8515;
        var GL_TEXTURE0 = 0x84C0;
        var GL_RGBA = 0x1908;
        var GL_FLOAT$1 = 0x1406;
        var GL_UNSIGNED_BYTE$1 = 0x1401;
        var GL_FRAMEBUFFER = 0x8D40;
        var GL_FRAMEBUFFER_COMPLETE = 0x8CD5;
        var GL_COLOR_ATTACHMENT0 = 0x8CE0;
        var GL_COLOR_BUFFER_BIT$1 = 0x4000;
        var wrapLimits = function (gl, extensions) {
            var maxAnisotropic = 1;
            if (extensions.ext_texture_filter_anisotropic) {
                maxAnisotropic = gl.getParameter(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT);
            }
            var maxDrawbuffers = 1;
            var maxColorAttachments = 1;
            if (extensions.webgl_draw_buffers) {
                maxDrawbuffers = gl.getParameter(GL_MAX_DRAW_BUFFERS_WEBGL);
                maxColorAttachments = gl.getParameter(GL_MAX_COLOR_ATTACHMENTS_WEBGL);
            }
            // detect if reading float textures is available (Safari doesn't support)
            var readFloat = !!extensions.oes_texture_float;
            if (readFloat) {
                var readFloatTexture = gl.createTexture();
                gl.bindTexture(GL_TEXTURE_2D, readFloatTexture);
                gl.texImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_FLOAT$1, null);
                var fbo = gl.createFramebuffer();
                gl.bindFramebuffer(GL_FRAMEBUFFER, fbo);
                gl.framebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, readFloatTexture, 0);
                gl.bindTexture(GL_TEXTURE_2D, null);
                if (gl.checkFramebufferStatus(GL_FRAMEBUFFER) !== GL_FRAMEBUFFER_COMPLETE)
                    readFloat = false;
                else {
                    gl.viewport(0, 0, 1, 1);
                    gl.clearColor(1.0, 0.0, 0.0, 1.0);
                    gl.clear(GL_COLOR_BUFFER_BIT$1);
                    var pixels = pool.allocType(GL_FLOAT$1, 4);
                    gl.readPixels(0, 0, 1, 1, GL_RGBA, GL_FLOAT$1, pixels);
                    if (gl.getError())
                        readFloat = false;
                    else {
                        gl.deleteFramebuffer(fbo);
                        gl.deleteTexture(readFloatTexture);
                        readFloat = pixels[0] === 1.0;
                    }
                    pool.freeType(pixels);
                }
            }
            // detect non power of two cube textures support (IE doesn't support)
            var isIE = typeof navigator !== 'undefined' && (/MSIE/.test(navigator.userAgent) || /Trident\//.test(navigator.appVersion) || /Edge/.test(navigator.userAgent));
            var npotTextureCube = true;
            if (!isIE) {
                var cubeTexture = gl.createTexture();
                var data = pool.allocType(GL_UNSIGNED_BYTE$1, 36);
                gl.activeTexture(GL_TEXTURE0);
                gl.bindTexture(GL_TEXTURE_CUBE_MAP, cubeTexture);
                gl.texImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL_RGBA, 3, 3, 0, GL_RGBA, GL_UNSIGNED_BYTE$1, data);
                pool.freeType(data);
                gl.bindTexture(GL_TEXTURE_CUBE_MAP, null);
                gl.deleteTexture(cubeTexture);
                npotTextureCube = !gl.getError();
            }
            return {
                // drawing buffer bit depth
                colorBits: [
                    gl.getParameter(GL_RED_BITS),
                    gl.getParameter(GL_GREEN_BITS),
                    gl.getParameter(GL_BLUE_BITS),
                    gl.getParameter(GL_ALPHA_BITS)
                ],
                depthBits: gl.getParameter(GL_DEPTH_BITS),
                stencilBits: gl.getParameter(GL_STENCIL_BITS),
                subpixelBits: gl.getParameter(GL_SUBPIXEL_BITS),
                // supported extensions
                extensions: Object.keys(extensions).filter(function (ext) {
                    return !!extensions[ext];
                }),
                // max aniso samples
                maxAnisotropic: maxAnisotropic,
                // max draw buffers
                maxDrawbuffers: maxDrawbuffers,
                maxColorAttachments: maxColorAttachments,
                // point and line size ranges
                pointSizeDims: gl.getParameter(GL_ALIASED_POINT_SIZE_RANGE),
                lineWidthDims: gl.getParameter(GL_ALIASED_LINE_WIDTH_RANGE),
                maxViewportDims: gl.getParameter(GL_MAX_VIEWPORT_DIMS),
                maxCombinedTextureUnits: gl.getParameter(GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS),
                maxCubeMapSize: gl.getParameter(GL_MAX_CUBE_MAP_TEXTURE_SIZE),
                maxRenderbufferSize: gl.getParameter(GL_MAX_RENDERBUFFER_SIZE),
                maxTextureUnits: gl.getParameter(GL_MAX_TEXTURE_IMAGE_UNITS),
                maxTextureSize: gl.getParameter(GL_MAX_TEXTURE_SIZE),
                maxAttributes: gl.getParameter(GL_MAX_VERTEX_ATTRIBS),
                maxVertexUniforms: gl.getParameter(GL_MAX_VERTEX_UNIFORM_VECTORS),
                maxVertexTextureUnits: gl.getParameter(GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS),
                maxVaryingVectors: gl.getParameter(GL_MAX_VARYING_VECTORS),
                maxFragmentUniforms: gl.getParameter(GL_MAX_FRAGMENT_UNIFORM_VECTORS),
                // vendor info
                glsl: gl.getParameter(GL_SHADING_LANGUAGE_VERSION),
                renderer: gl.getParameter(GL_RENDERER),
                vendor: gl.getParameter(GL_VENDOR),
                version: gl.getParameter(GL_VERSION),
                // quirks
                readFloat: readFloat,
                npotTextureCube: npotTextureCube
            };
        };
        function isNDArrayLike(obj) {
            return (!!obj &&
                typeof obj === 'object' &&
                Array.isArray(obj.shape) &&
                Array.isArray(obj.stride) &&
                typeof obj.offset === 'number' &&
                obj.shape.length === obj.stride.length &&
                (Array.isArray(obj.data) ||
                    isTypedArray(obj.data)));
        }
        var values = function (obj) {
            return Object.keys(obj).map(function (key) { return obj[key]; });
        };
        var flattenUtils = {
            shape: arrayShape$1,
            flatten: flattenArray
        };
        function flatten1D(array, nx, out) {
            for (var i = 0; i < nx; ++i) {
                out[i] = array[i];
            }
        }
        function flatten2D(array, nx, ny, out) {
            var ptr = 0;
            for (var i = 0; i < nx; ++i) {
                var row = array[i];
                for (var j = 0; j < ny; ++j) {
                    out[ptr++] = row[j];
                }
            }
        }
        function flatten3D(array, nx, ny, nz, out, ptr_) {
            var ptr = ptr_;
            for (var i = 0; i < nx; ++i) {
                var row = array[i];
                for (var j = 0; j < ny; ++j) {
                    var col = row[j];
                    for (var k = 0; k < nz; ++k) {
                        out[ptr++] = col[k];
                    }
                }
            }
        }
        function flattenRec(array, shape, level, out, ptr) {
            var stride = 1;
            for (var i = level + 1; i < shape.length; ++i) {
                stride *= shape[i];
            }
            var n = shape[level];
            if (shape.length - level === 4) {
                var nx = shape[level + 1];
                var ny = shape[level + 2];
                var nz = shape[level + 3];
                for (i = 0; i < n; ++i) {
                    flatten3D(array[i], nx, ny, nz, out, ptr);
                    ptr += stride;
                }
            }
            else {
                for (i = 0; i < n; ++i) {
                    flattenRec(array[i], shape, level + 1, out, ptr);
                    ptr += stride;
                }
            }
        }
        function flattenArray(array, shape, type, out_) {
            var sz = 1;
            if (shape.length) {
                for (var i = 0; i < shape.length; ++i) {
                    sz *= shape[i];
                }
            }
            else {
                sz = 0;
            }
            var out = out_ || pool.allocType(type, sz);
            switch (shape.length) {
                case 0:
                    break;
                case 1:
                    flatten1D(array, shape[0], out);
                    break;
                case 2:
                    flatten2D(array, shape[0], shape[1], out);
                    break;
                case 3:
                    flatten3D(array, shape[0], shape[1], shape[2], out, 0);
                    break;
                default:
                    flattenRec(array, shape, 0, out, 0);
            }
            return out;
        }
        function arrayShape$1(array_) {
            var shape = [];
            for (var array = array_; array.length; array = array[0]) {
                shape.push(array.length);
            }
            return shape;
        }
        var arrayTypes = {
            "[object Int8Array]": 5120,
            "[object Int16Array]": 5122,
            "[object Int32Array]": 5124,
            "[object Uint8Array]": 5121,
            "[object Uint8ClampedArray]": 5121,
            "[object Uint16Array]": 5123,
            "[object Uint32Array]": 5125,
            "[object Float32Array]": 5126,
            "[object Float64Array]": 5121,
            "[object ArrayBuffer]": 5121
        };
        var int8 = 5120;
        var int16 = 5122;
        var int32 = 5124;
        var uint8 = 5121;
        var uint16 = 5123;
        var uint32 = 5125;
        var float = 5126;
        var float32 = 5126;
        var glTypes = {
            int8: int8,
            int16: int16,
            int32: int32,
            uint8: uint8,
            uint16: uint16,
            uint32: uint32,
            float: float,
            float32: float32
        };
        var dynamic$1 = 35048;
        var stream = 35040;
        var usageTypes = {
            dynamic: dynamic$1,
            stream: stream,
            "static": 35044
        };
        var arrayFlatten = flattenUtils.flatten;
        var arrayShape = flattenUtils.shape;
        var GL_STATIC_DRAW = 0x88E4;
        var GL_STREAM_DRAW = 0x88E0;
        var GL_UNSIGNED_BYTE$3 = 5121;
        var GL_FLOAT$3 = 5126;
        var DTYPES_SIZES = [];
        DTYPES_SIZES[5120] = 1; // int8
        DTYPES_SIZES[5122] = 2; // int16
        DTYPES_SIZES[5124] = 4; // int32
        DTYPES_SIZES[5121] = 1; // uint8
        DTYPES_SIZES[5123] = 2; // uint16
        DTYPES_SIZES[5125] = 4; // uint32
        DTYPES_SIZES[5126] = 4; // float32
        function typedArrayCode(data) {
            return arrayTypes[Object.prototype.toString.call(data)] | 0;
        }
        function copyArray(out, inp) {
            for (var i = 0; i < inp.length; ++i) {
                out[i] = inp[i];
            }
        }
        function transpose(result, data, shapeX, shapeY, strideX, strideY, offset) {
            var ptr = 0;
            for (var i = 0; i < shapeX; ++i) {
                for (var j = 0; j < shapeY; ++j) {
                    result[ptr++] = data[strideX * i + strideY * j + offset];
                }
            }
        }
        function wrapBufferState(gl, stats, config, destroyBuffer) {
            var bufferCount = 0;
            var bufferSet = {};
            function REGLBuffer(type) {
                this.id = bufferCount++;
                this.buffer = gl.createBuffer();
                this.type = type;
                this.usage = GL_STATIC_DRAW;
                this.byteLength = 0;
                this.dimension = 1;
                this.dtype = GL_UNSIGNED_BYTE$3;
                this.persistentData = null;
                if (config.profile) {
                    this.stats = { size: 0 };
                }
            }
            REGLBuffer.prototype.bind = function () {
                gl.bindBuffer(this.type, this.buffer);
            };
            REGLBuffer.prototype.destroy = function () {
                destroy(this);
            };
            var streamPool = [];
            function createStream(type, data) {
                var buffer = streamPool.pop();
                if (!buffer) {
                    buffer = new REGLBuffer(type);
                }
                buffer.bind();
                initBufferFromData(buffer, data, GL_STREAM_DRAW, 0, 1, false);
                return buffer;
            }
            function destroyStream(stream$$1) {
                streamPool.push(stream$$1);
            }
            function initBufferFromTypedArray(buffer, data, usage) {
                buffer.byteLength = data.byteLength;
                gl.bufferData(buffer.type, data, usage);
            }
            function initBufferFromData(buffer, data, usage, dtype, dimension, persist) {
                var shape;
                buffer.usage = usage;
                if (Array.isArray(data)) {
                    buffer.dtype = dtype || GL_FLOAT$3;
                    if (data.length > 0) {
                        var flatData;
                        if (Array.isArray(data[0])) {
                            shape = arrayShape(data);
                            var dim = 1;
                            for (var i = 1; i < shape.length; ++i) {
                                dim *= shape[i];
                            }
                            buffer.dimension = dim;
                            flatData = arrayFlatten(data, shape, buffer.dtype);
                            initBufferFromTypedArray(buffer, flatData, usage);
                            if (persist) {
                                buffer.persistentData = flatData;
                            }
                            else {
                                pool.freeType(flatData);
                            }
                        }
                        else if (typeof data[0] === 'number') {
                            buffer.dimension = dimension;
                            var typedData = pool.allocType(buffer.dtype, data.length);
                            copyArray(typedData, data);
                            initBufferFromTypedArray(buffer, typedData, usage);
                            if (persist) {
                                buffer.persistentData = typedData;
                            }
                            else {
                                pool.freeType(typedData);
                            }
                        }
                        else if (isTypedArray(data[0])) {
                            buffer.dimension = data[0].length;
                            buffer.dtype = dtype || typedArrayCode(data[0]) || GL_FLOAT$3;
                            flatData = arrayFlatten(data, [data.length, data[0].length], buffer.dtype);
                            initBufferFromTypedArray(buffer, flatData, usage);
                            if (persist) {
                                buffer.persistentData = flatData;
                            }
                            else {
                                pool.freeType(flatData);
                            }
                        }
                        else {
                            check$1.raise('invalid buffer data');
                        }
                    }
                }
                else if (isTypedArray(data)) {
                    buffer.dtype = dtype || typedArrayCode(data);
                    buffer.dimension = dimension;
                    initBufferFromTypedArray(buffer, data, usage);
                    if (persist) {
                        buffer.persistentData = new Uint8Array(new Uint8Array(data.buffer));
                    }
                }
                else if (isNDArrayLike(data)) {
                    shape = data.shape;
                    var stride = data.stride;
                    var offset = data.offset;
                    var shapeX = 0;
                    var shapeY = 0;
                    var strideX = 0;
                    var strideY = 0;
                    if (shape.length === 1) {
                        shapeX = shape[0];
                        shapeY = 1;
                        strideX = stride[0];
                        strideY = 0;
                    }
                    else if (shape.length === 2) {
                        shapeX = shape[0];
                        shapeY = shape[1];
                        strideX = stride[0];
                        strideY = stride[1];
                    }
                    else {
                        check$1.raise('invalid shape');
                    }
                    buffer.dtype = dtype || typedArrayCode(data.data) || GL_FLOAT$3;
                    buffer.dimension = shapeY;
                    var transposeData = pool.allocType(buffer.dtype, shapeX * shapeY);
                    transpose(transposeData, data.data, shapeX, shapeY, strideX, strideY, offset);
                    initBufferFromTypedArray(buffer, transposeData, usage);
                    if (persist) {
                        buffer.persistentData = transposeData;
                    }
                    else {
                        pool.freeType(transposeData);
                    }
                }
                else if (data instanceof ArrayBuffer) {
                    buffer.dtype = GL_UNSIGNED_BYTE$3;
                    buffer.dimension = dimension;
                    initBufferFromTypedArray(buffer, data, usage);
                    if (persist) {
                        buffer.persistentData = new Uint8Array(new Uint8Array(data));
                    }
                }
                else {
                    check$1.raise('invalid buffer data');
                }
            }
            function destroy(buffer) {
                stats.bufferCount--;
                // remove attribute link
                destroyBuffer(buffer);
                var handle = buffer.buffer;
                check$1(handle, 'buffer must not be deleted already');
                gl.deleteBuffer(handle);
                buffer.buffer = null;
                delete bufferSet[buffer.id];
            }
            function createBuffer(options, type, deferInit, persistent) {
                stats.bufferCount++;
                var buffer = new REGLBuffer(type);
                bufferSet[buffer.id] = buffer;
                function reglBuffer(options) {
                    var usage = GL_STATIC_DRAW;
                    var data = null;
                    var byteLength = 0;
                    var dtype = 0;
                    var dimension = 1;
                    if (Array.isArray(options) ||
                        isTypedArray(options) ||
                        isNDArrayLike(options) ||
                        options instanceof ArrayBuffer) {
                        data = options;
                    }
                    else if (typeof options === 'number') {
                        byteLength = options | 0;
                    }
                    else if (options) {
                        check$1.type(options, 'object', 'buffer arguments must be an object, a number or an array');
                        if ('data' in options) {
                            check$1(data === null ||
                                Array.isArray(data) ||
                                isTypedArray(data) ||
                                isNDArrayLike(data), 'invalid data for buffer');
                            data = options.data;
                        }
                        if ('usage' in options) {
                            check$1.parameter(options.usage, usageTypes, 'invalid buffer usage');
                            usage = usageTypes[options.usage];
                        }
                        if ('type' in options) {
                            check$1.parameter(options.type, glTypes, 'invalid buffer type');
                            dtype = glTypes[options.type];
                        }
                        if ('dimension' in options) {
                            check$1.type(options.dimension, 'number', 'invalid dimension');
                            dimension = options.dimension | 0;
                        }
                        if ('length' in options) {
                            check$1.nni(byteLength, 'buffer length must be a nonnegative integer');
                            byteLength = options.length | 0;
                        }
                    }
                    buffer.bind();
                    if (!data) {
                        // #475
                        if (byteLength)
                            gl.bufferData(buffer.type, byteLength, usage);
                        buffer.dtype = dtype || GL_UNSIGNED_BYTE$3;
                        buffer.usage = usage;
                        buffer.dimension = dimension;
                        buffer.byteLength = byteLength;
                    }
                    else {
                        initBufferFromData(buffer, data, usage, dtype, dimension, persistent);
                    }
                    if (config.profile) {
                        buffer.stats.size = buffer.byteLength * DTYPES_SIZES[buffer.dtype];
                    }
                    return reglBuffer;
                }
                function setSubData(data, offset) {
                    check$1(offset + data.byteLength <= buffer.byteLength, 'invalid buffer subdata call, buffer is too small. ' + ' Can\'t write data of size ' + data.byteLength + ' starting from offset ' + offset + ' to a buffer of size ' + buffer.byteLength);
                    gl.bufferSubData(buffer.type, offset, data);
                }
                function subdata(data, offset_) {
                    var offset = (offset_ || 0) | 0;
                    var shape;
                    buffer.bind();
                    if (isTypedArray(data) || data instanceof ArrayBuffer) {
                        setSubData(data, offset);
                    }
                    else if (Array.isArray(data)) {
                        if (data.length > 0) {
                            if (typeof data[0] === 'number') {
                                var converted = pool.allocType(buffer.dtype, data.length);
                                copyArray(converted, data);
                                setSubData(converted, offset);
                                pool.freeType(converted);
                            }
                            else if (Array.isArray(data[0]) || isTypedArray(data[0])) {
                                shape = arrayShape(data);
                                var flatData = arrayFlatten(data, shape, buffer.dtype);
                                setSubData(flatData, offset);
                                pool.freeType(flatData);
                            }
                            else {
                                check$1.raise('invalid buffer data');
                            }
                        }
                    }
                    else if (isNDArrayLike(data)) {
                        shape = data.shape;
                        var stride = data.stride;
                        var shapeX = 0;
                        var shapeY = 0;
                        var strideX = 0;
                        var strideY = 0;
                        if (shape.length === 1) {
                            shapeX = shape[0];
                            shapeY = 1;
                            strideX = stride[0];
                            strideY = 0;
                        }
                        else if (shape.length === 2) {
                            shapeX = shape[0];
                            shapeY = shape[1];
                            strideX = stride[0];
                            strideY = stride[1];
                        }
                        else {
                            check$1.raise('invalid shape');
                        }
                        var dtype = Array.isArray(data.data)
                            ? buffer.dtype
                            : typedArrayCode(data.data);
                        var transposeData = pool.allocType(dtype, shapeX * shapeY);
                        transpose(transposeData, data.data, shapeX, shapeY, strideX, strideY, data.offset);
                        setSubData(transposeData, offset);
                        pool.freeType(transposeData);
                    }
                    else {
                        check$1.raise('invalid data for buffer subdata');
                    }
                    return reglBuffer;
                }
                if (!deferInit) {
                    reglBuffer(options);
                }
                reglBuffer._reglType = 'buffer';
                reglBuffer._buffer = buffer;
                reglBuffer.subdata = subdata;
                if (config.profile) {
                    reglBuffer.stats = buffer.stats;
                }
                reglBuffer.destroy = function () { destroy(buffer); };
                return reglBuffer;
            }
            function restoreBuffers() {
                values(bufferSet).forEach(function (buffer) {
                    buffer.buffer = gl.createBuffer();
                    gl.bindBuffer(buffer.type, buffer.buffer);
                    gl.bufferData(buffer.type, buffer.persistentData || buffer.byteLength, buffer.usage);
                });
            }
            if (config.profile) {
                stats.getTotalBufferSize = function () {
                    var total = 0;
                    // TODO: Right now, the streams are not part of the total count.
                    Object.keys(bufferSet).forEach(function (key) {
                        total += bufferSet[key].stats.size;
                    });
                    return total;
                };
            }
            return {
                create: createBuffer,
                createStream: createStream,
                destroyStream: destroyStream,
                clear: function () {
                    values(bufferSet).forEach(destroy);
                    streamPool.forEach(destroy);
                },
                getBuffer: function (wrapper) {
                    if (wrapper && wrapper._buffer instanceof REGLBuffer) {
                        return wrapper._buffer;
                    }
                    return null;
                },
                restore: restoreBuffers,
                _initBuffer: initBufferFromData
            };
        }
        var points = 0;
        var point = 0;
        var lines = 1;
        var line = 1;
        var triangles = 4;
        var triangle = 4;
        var primTypes = {
            points: points,
            point: point,
            lines: lines,
            line: line,
            triangles: triangles,
            triangle: triangle,
            "line loop": 2,
            "line strip": 3,
            "triangle strip": 5,
            "triangle fan": 6
        };
        var GL_POINTS = 0;
        var GL_LINES = 1;
        var GL_TRIANGLES = 4;
        var GL_BYTE$2 = 5120;
        var GL_UNSIGNED_BYTE$4 = 5121;
        var GL_SHORT$2 = 5122;
        var GL_UNSIGNED_SHORT$2 = 5123;
        var GL_INT$2 = 5124;
        var GL_UNSIGNED_INT$2 = 5125;
        var GL_ELEMENT_ARRAY_BUFFER = 34963;
        var GL_STREAM_DRAW$1 = 0x88E0;
        var GL_STATIC_DRAW$1 = 0x88E4;
        function wrapElementsState(gl, extensions, bufferState, stats) {
            var elementSet = {};
            var elementCount = 0;
            var elementTypes = {
                'uint8': GL_UNSIGNED_BYTE$4,
                'uint16': GL_UNSIGNED_SHORT$2
            };
            if (extensions.oes_element_index_uint) {
                elementTypes.uint32 = GL_UNSIGNED_INT$2;
            }
            function REGLElementBuffer(buffer) {
                this.id = elementCount++;
                elementSet[this.id] = this;
                this.buffer = buffer;
                this.primType = GL_TRIANGLES;
                this.vertCount = 0;
                this.type = 0;
            }
            REGLElementBuffer.prototype.bind = function () {
                this.buffer.bind();
            };
            var bufferPool = [];
            function createElementStream(data) {
                var result = bufferPool.pop();
                if (!result) {
                    result = new REGLElementBuffer(bufferState.create(null, GL_ELEMENT_ARRAY_BUFFER, true, false)._buffer);
                }
                initElements(result, data, GL_STREAM_DRAW$1, -1, -1, 0, 0);
                return result;
            }
            function destroyElementStream(elements) {
                bufferPool.push(elements);
            }
            function initElements(elements, data, usage, prim, count, byteLength, type) {
                elements.buffer.bind();
                var dtype;
                if (data) {
                    var predictedType = type;
                    if (!type && (!isTypedArray(data) ||
                        (isNDArrayLike(data) && !isTypedArray(data.data)))) {
                        predictedType = extensions.oes_element_index_uint
                            ? GL_UNSIGNED_INT$2
                            : GL_UNSIGNED_SHORT$2;
                    }
                    bufferState._initBuffer(elements.buffer, data, usage, predictedType, 3);
                }
                else {
                    gl.bufferData(GL_ELEMENT_ARRAY_BUFFER, byteLength, usage);
                    elements.buffer.dtype = dtype || GL_UNSIGNED_BYTE$4;
                    elements.buffer.usage = usage;
                    elements.buffer.dimension = 3;
                    elements.buffer.byteLength = byteLength;
                }
                dtype = type;
                if (!type) {
                    switch (elements.buffer.dtype) {
                        case GL_UNSIGNED_BYTE$4:
                        case GL_BYTE$2:
                            dtype = GL_UNSIGNED_BYTE$4;
                            break;
                        case GL_UNSIGNED_SHORT$2:
                        case GL_SHORT$2:
                            dtype = GL_UNSIGNED_SHORT$2;
                            break;
                        case GL_UNSIGNED_INT$2:
                        case GL_INT$2:
                            dtype = GL_UNSIGNED_INT$2;
                            break;
                        default:
                            check$1.raise('unsupported type for element array');
                    }
                    elements.buffer.dtype = dtype;
                }
                elements.type = dtype;
                // Check oes_element_index_uint extension
                check$1(dtype !== GL_UNSIGNED_INT$2 ||
                    !!extensions.oes_element_index_uint, '32 bit element buffers not supported, enable oes_element_index_uint first');
                // try to guess default primitive type and arguments
                var vertCount = count;
                if (vertCount < 0) {
                    vertCount = elements.buffer.byteLength;
                    if (dtype === GL_UNSIGNED_SHORT$2) {
                        vertCount >>= 1;
                    }
                    else if (dtype === GL_UNSIGNED_INT$2) {
                        vertCount >>= 2;
                    }
                }
                elements.vertCount = vertCount;
                // try to guess primitive type from cell dimension
                var primType = prim;
                if (prim < 0) {
                    primType = GL_TRIANGLES;
                    var dimension = elements.buffer.dimension;
                    if (dimension === 1)
                        primType = GL_POINTS;
                    if (dimension === 2)
                        primType = GL_LINES;
                    if (dimension === 3)
                        primType = GL_TRIANGLES;
                }
                elements.primType = primType;
            }
            function destroyElements(elements) {
                stats.elementsCount--;
                check$1(elements.buffer !== null, 'must not double destroy elements');
                delete elementSet[elements.id];
                elements.buffer.destroy();
                elements.buffer = null;
            }
            function createElements(options, persistent) {
                var buffer = bufferState.create(null, GL_ELEMENT_ARRAY_BUFFER, true);
                var elements = new REGLElementBuffer(buffer._buffer);
                stats.elementsCount++;
                function reglElements(options) {
                    if (!options) {
                        buffer();
                        elements.primType = GL_TRIANGLES;
                        elements.vertCount = 0;
                        elements.type = GL_UNSIGNED_BYTE$4;
                    }
                    else if (typeof options === 'number') {
                        buffer(options);
                        elements.primType = GL_TRIANGLES;
                        elements.vertCount = options | 0;
                        elements.type = GL_UNSIGNED_BYTE$4;
                    }
                    else {
                        var data = null;
                        var usage = GL_STATIC_DRAW$1;
                        var primType = -1;
                        var vertCount = -1;
                        var byteLength = 0;
                        var dtype = 0;
                        if (Array.isArray(options) ||
                            isTypedArray(options) ||
                            isNDArrayLike(options)) {
                            data = options;
                        }
                        else {
                            check$1.type(options, 'object', 'invalid arguments for elements');
                            if ('data' in options) {
                                data = options.data;
                                check$1(Array.isArray(data) ||
                                    isTypedArray(data) ||
                                    isNDArrayLike(data), 'invalid data for element buffer');
                            }
                            if ('usage' in options) {
                                check$1.parameter(options.usage, usageTypes, 'invalid element buffer usage');
                                usage = usageTypes[options.usage];
                            }
                            if ('primitive' in options) {
                                check$1.parameter(options.primitive, primTypes, 'invalid element buffer primitive');
                                primType = primTypes[options.primitive];
                            }
                            if ('count' in options) {
                                check$1(typeof options.count === 'number' && options.count >= 0, 'invalid vertex count for elements');
                                vertCount = options.count | 0;
                            }
                            if ('type' in options) {
                                check$1.parameter(options.type, elementTypes, 'invalid buffer type');
                                dtype = elementTypes[options.type];
                            }
                            if ('length' in options) {
                                byteLength = options.length | 0;
                            }
                            else {
                                byteLength = vertCount;
                                if (dtype === GL_UNSIGNED_SHORT$2 || dtype === GL_SHORT$2) {
                                    byteLength *= 2;
                                }
                                else if (dtype === GL_UNSIGNED_INT$2 || dtype === GL_INT$2) {
                                    byteLength *= 4;
                                }
                            }
                        }
                        initElements(elements, data, usage, primType, vertCount, byteLength, dtype);
                    }
                    return reglElements;
                }
                reglElements(options);
                reglElements._reglType = 'elements';
                reglElements._elements = elements;
                reglElements.subdata = function (data, offset) {
                    buffer.subdata(data, offset);
                    return reglElements;
                };
                reglElements.destroy = function () {
                    destroyElements(elements);
                };
                return reglElements;
            }
            return {
                create: createElements,
                createStream: createElementStream,
                destroyStream: destroyElementStream,
                getElements: function (elements) {
                    if (typeof elements === 'function' &&
                        elements._elements instanceof REGLElementBuffer) {
                        return elements._elements;
                    }
                    return null;
                },
                clear: function () {
                    values(elementSet).forEach(destroyElements);
                }
            };
        }
        var FLOAT = new Float32Array(1);
        var INT = new Uint32Array(FLOAT.buffer);
        var GL_UNSIGNED_SHORT$4 = 5123;
        function convertToHalfFloat(array) {
            var ushorts = pool.allocType(GL_UNSIGNED_SHORT$4, array.length);
            for (var i = 0; i < array.length; ++i) {
                if (isNaN(array[i])) {
                    ushorts[i] = 0xffff;
                }
                else if (array[i] === Infinity) {
                    ushorts[i] = 0x7c00;
                }
                else if (array[i] === -Infinity) {
                    ushorts[i] = 0xfc00;
                }
                else {
                    FLOAT[0] = array[i];
                    var x = INT[0];
                    var sgn = (x >>> 31) << 15;
                    var exp = ((x << 1) >>> 24) - 127;
                    var frac = (x >> 13) & ((1 << 10) - 1);
                    if (exp < -24) {
                        // round non-representable denormals to 0
                        ushorts[i] = sgn;
                    }
                    else if (exp < -14) {
                        // handle denormals
                        var s = -14 - exp;
                        ushorts[i] = sgn + ((frac + (1 << 10)) >> s);
                    }
                    else if (exp > 15) {
                        // round overflow to +/- Infinity
                        ushorts[i] = sgn + 0x7c00;
                    }
                    else {
                        // otherwise convert directly
                        ushorts[i] = sgn + ((exp + 15) << 10) + frac;
                    }
                }
            }
            return ushorts;
        }
        function isArrayLike(s) {
            return Array.isArray(s) || isTypedArray(s);
        }
        var isPow2$1 = function (v) {
            return !(v & (v - 1)) && (!!v);
        };
        var GL_COMPRESSED_TEXTURE_FORMATS = 0x86A3;
        var GL_TEXTURE_2D$1 = 0x0DE1;
        var GL_TEXTURE_CUBE_MAP$1 = 0x8513;
        var GL_TEXTURE_CUBE_MAP_POSITIVE_X$1 = 0x8515;
        var GL_RGBA$1 = 0x1908;
        var GL_ALPHA = 0x1906;
        var GL_RGB = 0x1907;
        var GL_LUMINANCE = 0x1909;
        var GL_LUMINANCE_ALPHA = 0x190A;
        var GL_RGBA4 = 0x8056;
        var GL_RGB5_A1 = 0x8057;
        var GL_RGB565 = 0x8D62;
        var GL_UNSIGNED_SHORT_4_4_4_4$1 = 0x8033;
        var GL_UNSIGNED_SHORT_5_5_5_1$1 = 0x8034;
        var GL_UNSIGNED_SHORT_5_6_5$1 = 0x8363;
        var GL_UNSIGNED_INT_24_8_WEBGL$1 = 0x84FA;
        var GL_DEPTH_COMPONENT = 0x1902;
        var GL_DEPTH_STENCIL = 0x84F9;
        var GL_SRGB_EXT = 0x8C40;
        var GL_SRGB_ALPHA_EXT = 0x8C42;
        var GL_HALF_FLOAT_OES$1 = 0x8D61;
        var GL_COMPRESSED_RGB_S3TC_DXT1_EXT = 0x83F0;
        var GL_COMPRESSED_RGBA_S3TC_DXT1_EXT = 0x83F1;
        var GL_COMPRESSED_RGBA_S3TC_DXT3_EXT = 0x83F2;
        var GL_COMPRESSED_RGBA_S3TC_DXT5_EXT = 0x83F3;
        var GL_COMPRESSED_RGB_ATC_WEBGL = 0x8C92;
        var GL_COMPRESSED_RGBA_ATC_EXPLICIT_ALPHA_WEBGL = 0x8C93;
        var GL_COMPRESSED_RGBA_ATC_INTERPOLATED_ALPHA_WEBGL = 0x87EE;
        var GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG = 0x8C00;
        var GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG = 0x8C01;
        var GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG = 0x8C02;
        var GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG = 0x8C03;
        var GL_COMPRESSED_RGB_ETC1_WEBGL = 0x8D64;
        var GL_UNSIGNED_BYTE$5 = 0x1401;
        var GL_UNSIGNED_SHORT$3 = 0x1403;
        var GL_UNSIGNED_INT$3 = 0x1405;
        var GL_FLOAT$4 = 0x1406;
        var GL_TEXTURE_WRAP_S = 0x2802;
        var GL_TEXTURE_WRAP_T = 0x2803;
        var GL_REPEAT = 0x2901;
        var GL_CLAMP_TO_EDGE$1 = 0x812F;
        var GL_MIRRORED_REPEAT = 0x8370;
        var GL_TEXTURE_MAG_FILTER = 0x2800;
        var GL_TEXTURE_MIN_FILTER = 0x2801;
        var GL_NEAREST$1 = 0x2600;
        var GL_LINEAR = 0x2601;
        var GL_NEAREST_MIPMAP_NEAREST$1 = 0x2700;
        var GL_LINEAR_MIPMAP_NEAREST$1 = 0x2701;
        var GL_NEAREST_MIPMAP_LINEAR$1 = 0x2702;
        var GL_LINEAR_MIPMAP_LINEAR$1 = 0x2703;
        var GL_GENERATE_MIPMAP_HINT = 0x8192;
        var GL_DONT_CARE = 0x1100;
        var GL_FASTEST = 0x1101;
        var GL_NICEST = 0x1102;
        var GL_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE;
        var GL_UNPACK_ALIGNMENT = 0x0CF5;
        var GL_UNPACK_FLIP_Y_WEBGL = 0x9240;
        var GL_UNPACK_PREMULTIPLY_ALPHA_WEBGL = 0x9241;
        var GL_UNPACK_COLORSPACE_CONVERSION_WEBGL = 0x9243;
        var GL_BROWSER_DEFAULT_WEBGL = 0x9244;
        var GL_TEXTURE0$1 = 0x84C0;
        var MIPMAP_FILTERS = [
            GL_NEAREST_MIPMAP_NEAREST$1,
            GL_NEAREST_MIPMAP_LINEAR$1,
            GL_LINEAR_MIPMAP_NEAREST$1,
            GL_LINEAR_MIPMAP_LINEAR$1
        ];
        var CHANNELS_FORMAT = [
            0,
            GL_LUMINANCE,
            GL_LUMINANCE_ALPHA,
            GL_RGB,
            GL_RGBA$1
        ];
        var FORMAT_CHANNELS = {};
        FORMAT_CHANNELS[GL_LUMINANCE] =
            FORMAT_CHANNELS[GL_ALPHA] =
                FORMAT_CHANNELS[GL_DEPTH_COMPONENT] = 1;
        FORMAT_CHANNELS[GL_DEPTH_STENCIL] =
            FORMAT_CHANNELS[GL_LUMINANCE_ALPHA] = 2;
        FORMAT_CHANNELS[GL_RGB] =
            FORMAT_CHANNELS[GL_SRGB_EXT] = 3;
        FORMAT_CHANNELS[GL_RGBA$1] =
            FORMAT_CHANNELS[GL_SRGB_ALPHA_EXT] = 4;
        function objectName(str) {
            return '[object ' + str + ']';
        }
        var CANVAS_CLASS = objectName('HTMLCanvasElement');
        var OFFSCREENCANVAS_CLASS = objectName('OffscreenCanvas');
        var CONTEXT2D_CLASS = objectName('CanvasRenderingContext2D');
        var BITMAP_CLASS = objectName('ImageBitmap');
        var IMAGE_CLASS = objectName('HTMLImageElement');
        var VIDEO_CLASS = objectName('HTMLVideoElement');
        var PIXEL_CLASSES = Object.keys(arrayTypes).concat([
            CANVAS_CLASS,
            OFFSCREENCANVAS_CLASS,
            CONTEXT2D_CLASS,
            BITMAP_CLASS,
            IMAGE_CLASS,
            VIDEO_CLASS
        ]);
        // for every texture type, store
        // the size in bytes.
        var TYPE_SIZES = [];
        TYPE_SIZES[GL_UNSIGNED_BYTE$5] = 1;
        TYPE_SIZES[GL_FLOAT$4] = 4;
        TYPE_SIZES[GL_HALF_FLOAT_OES$1] = 2;
        TYPE_SIZES[GL_UNSIGNED_SHORT$3] = 2;
        TYPE_SIZES[GL_UNSIGNED_INT$3] = 4;
        var FORMAT_SIZES_SPECIAL = [];
        FORMAT_SIZES_SPECIAL[GL_RGBA4] = 2;
        FORMAT_SIZES_SPECIAL[GL_RGB5_A1] = 2;
        FORMAT_SIZES_SPECIAL[GL_RGB565] = 2;
        FORMAT_SIZES_SPECIAL[GL_DEPTH_STENCIL] = 4;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGB_S3TC_DXT1_EXT] = 0.5;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGBA_S3TC_DXT1_EXT] = 0.5;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGBA_S3TC_DXT3_EXT] = 1;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGBA_S3TC_DXT5_EXT] = 1;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGB_ATC_WEBGL] = 0.5;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGBA_ATC_EXPLICIT_ALPHA_WEBGL] = 1;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGBA_ATC_INTERPOLATED_ALPHA_WEBGL] = 1;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG] = 0.5;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG] = 0.25;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG] = 0.5;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG] = 0.25;
        FORMAT_SIZES_SPECIAL[GL_COMPRESSED_RGB_ETC1_WEBGL] = 0.5;
        function isNumericArray(arr) {
            return (Array.isArray(arr) &&
                (arr.length === 0 ||
                    typeof arr[0] === 'number'));
        }
        function isRectArray(arr) {
            if (!Array.isArray(arr)) {
                return false;
            }
            var width = arr.length;
            if (width === 0 || !isArrayLike(arr[0])) {
                return false;
            }
            return true;
        }
        function classString(x) {
            return Object.prototype.toString.call(x);
        }
        function isCanvasElement(object) {
            return classString(object) === CANVAS_CLASS;
        }
        function isOffscreenCanvas(object) {
            return classString(object) === OFFSCREENCANVAS_CLASS;
        }
        function isContext2D(object) {
            return classString(object) === CONTEXT2D_CLASS;
        }
        function isBitmap(object) {
            return classString(object) === BITMAP_CLASS;
        }
        function isImageElement(object) {
            return classString(object) === IMAGE_CLASS;
        }
        function isVideoElement(object) {
            return classString(object) === VIDEO_CLASS;
        }
        function isPixelData(object) {
            if (!object) {
                return false;
            }
            var className = classString(object);
            if (PIXEL_CLASSES.indexOf(className) >= 0) {
                return true;
            }
            return (isNumericArray(object) ||
                isRectArray(object) ||
                isNDArrayLike(object));
        }
        function typedArrayCode$1(data) {
            return arrayTypes[Object.prototype.toString.call(data)] | 0;
        }
        function convertData(result, data) {
            var n = data.length;
            switch (result.type) {
                case GL_UNSIGNED_BYTE$5:
                case GL_UNSIGNED_SHORT$3:
                case GL_UNSIGNED_INT$3:
                case GL_FLOAT$4:
                    var converted = pool.allocType(result.type, n);
                    converted.set(data);
                    result.data = converted;
                    break;
                case GL_HALF_FLOAT_OES$1:
                    result.data = convertToHalfFloat(data);
                    break;
                default:
                    check$1.raise('unsupported texture type, must specify a typed array');
            }
        }
        function preConvert(image, n) {
            return pool.allocType(image.type === GL_HALF_FLOAT_OES$1
                ? GL_FLOAT$4
                : image.type, n);
        }
        function postConvert(image, data) {
            if (image.type === GL_HALF_FLOAT_OES$1) {
                image.data = convertToHalfFloat(data);
                pool.freeType(data);
            }
            else {
                image.data = data;
            }
        }
        function transposeData(image, array, strideX, strideY, strideC, offset) {
            var w = image.width;
            var h = image.height;
            var c = image.channels;
            var n = w * h * c;
            var data = preConvert(image, n);
            var p = 0;
            for (var i = 0; i < h; ++i) {
                for (var j = 0; j < w; ++j) {
                    for (var k = 0; k < c; ++k) {
                        data[p++] = array[strideX * j + strideY * i + strideC * k + offset];
                    }
                }
            }
            postConvert(image, data);
        }
        function getTextureSize(format, type, width, height, isMipmap, isCube) {
            var s;
            if (typeof FORMAT_SIZES_SPECIAL[format] !== 'undefined') {
                // we have a special array for dealing with weird color formats such as RGB5A1
                s = FORMAT_SIZES_SPECIAL[format];
            }
            else {
                s = FORMAT_CHANNELS[format] * TYPE_SIZES[type];
            }
            if (isCube) {
                s *= 6;
            }
            if (isMipmap) {
                // compute the total size of all the mipmaps.
                var total = 0;
                var w = width;
                while (w >= 1) {
                    // we can only use mipmaps on a square image,
                    // so we can simply use the width and ignore the height:
                    total += s * w * w;
                    w /= 2;
                }
                return total;
            }
            else {
                return s * width * height;
            }
        }
        function createTextureSet(gl, extensions, limits, reglPoll, contextState, stats, config) {
            // -------------------------------------------------------
            // Initialize constants and parameter tables here
            // -------------------------------------------------------
            var mipmapHint = {
                "don't care": GL_DONT_CARE,
                'dont care': GL_DONT_CARE,
                'nice': GL_NICEST,
                'fast': GL_FASTEST
            };
            var wrapModes = {
                'repeat': GL_REPEAT,
                'clamp': GL_CLAMP_TO_EDGE$1,
                'mirror': GL_MIRRORED_REPEAT
            };
            var magFilters = {
                'nearest': GL_NEAREST$1,
                'linear': GL_LINEAR
            };
            var minFilters = extend({
                'mipmap': GL_LINEAR_MIPMAP_LINEAR$1,
                'nearest mipmap nearest': GL_NEAREST_MIPMAP_NEAREST$1,
                'linear mipmap nearest': GL_LINEAR_MIPMAP_NEAREST$1,
                'nearest mipmap linear': GL_NEAREST_MIPMAP_LINEAR$1,
                'linear mipmap linear': GL_LINEAR_MIPMAP_LINEAR$1
            }, magFilters);
            var colorSpace = {
                'none': 0,
                'browser': GL_BROWSER_DEFAULT_WEBGL
            };
            var textureTypes = {
                'uint8': GL_UNSIGNED_BYTE$5,
                'rgba4': GL_UNSIGNED_SHORT_4_4_4_4$1,
                'rgb565': GL_UNSIGNED_SHORT_5_6_5$1,
                'rgb5 a1': GL_UNSIGNED_SHORT_5_5_5_1$1
            };
            var textureFormats = {
                'alpha': GL_ALPHA,
                'luminance': GL_LUMINANCE,
                'luminance alpha': GL_LUMINANCE_ALPHA,
                'rgb': GL_RGB,
                'rgba': GL_RGBA$1,
                'rgba4': GL_RGBA4,
                'rgb5 a1': GL_RGB5_A1,
                'rgb565': GL_RGB565
            };
            var compressedTextureFormats = {};
            if (extensions.ext_srgb) {
                textureFormats.srgb = GL_SRGB_EXT;
                textureFormats.srgba = GL_SRGB_ALPHA_EXT;
            }
            if (extensions.oes_texture_float) {
                textureTypes.float32 = textureTypes.float = GL_FLOAT$4;
            }
            if (extensions.oes_texture_half_float) {
                textureTypes['float16'] = textureTypes['half float'] = GL_HALF_FLOAT_OES$1;
            }
            if (extensions.webgl_depth_texture) {
                extend(textureFormats, {
                    'depth': GL_DEPTH_COMPONENT,
                    'depth stencil': GL_DEPTH_STENCIL
                });
                extend(textureTypes, {
                    'uint16': GL_UNSIGNED_SHORT$3,
                    'uint32': GL_UNSIGNED_INT$3,
                    'depth stencil': GL_UNSIGNED_INT_24_8_WEBGL$1
                });
            }
            if (extensions.webgl_compressed_texture_s3tc) {
                extend(compressedTextureFormats, {
                    'rgb s3tc dxt1': GL_COMPRESSED_RGB_S3TC_DXT1_EXT,
                    'rgba s3tc dxt1': GL_COMPRESSED_RGBA_S3TC_DXT1_EXT,
                    'rgba s3tc dxt3': GL_COMPRESSED_RGBA_S3TC_DXT3_EXT,
                    'rgba s3tc dxt5': GL_COMPRESSED_RGBA_S3TC_DXT5_EXT
                });
            }
            if (extensions.webgl_compressed_texture_atc) {
                extend(compressedTextureFormats, {
                    'rgb atc': GL_COMPRESSED_RGB_ATC_WEBGL,
                    'rgba atc explicit alpha': GL_COMPRESSED_RGBA_ATC_EXPLICIT_ALPHA_WEBGL,
                    'rgba atc interpolated alpha': GL_COMPRESSED_RGBA_ATC_INTERPOLATED_ALPHA_WEBGL
                });
            }
            if (extensions.webgl_compressed_texture_pvrtc) {
                extend(compressedTextureFormats, {
                    'rgb pvrtc 4bppv1': GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG,
                    'rgb pvrtc 2bppv1': GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG,
                    'rgba pvrtc 4bppv1': GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG,
                    'rgba pvrtc 2bppv1': GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG
                });
            }
            if (extensions.webgl_compressed_texture_etc1) {
                compressedTextureFormats['rgb etc1'] = GL_COMPRESSED_RGB_ETC1_WEBGL;
            }
            // Copy over all texture formats
            var supportedCompressedFormats = Array.prototype.slice.call(gl.getParameter(GL_COMPRESSED_TEXTURE_FORMATS));
            Object.keys(compressedTextureFormats).forEach(function (name) {
                var format = compressedTextureFormats[name];
                if (supportedCompressedFormats.indexOf(format) >= 0) {
                    textureFormats[name] = format;
                }
            });
            var supportedFormats = Object.keys(textureFormats);
            limits.textureFormats = supportedFormats;
            // associate with every format string its
            // corresponding GL-value.
            var textureFormatsInvert = [];
            Object.keys(textureFormats).forEach(function (key) {
                var val = textureFormats[key];
                textureFormatsInvert[val] = key;
            });
            // associate with every type string its
            // corresponding GL-value.
            var textureTypesInvert = [];
            Object.keys(textureTypes).forEach(function (key) {
                var val = textureTypes[key];
                textureTypesInvert[val] = key;
            });
            var magFiltersInvert = [];
            Object.keys(magFilters).forEach(function (key) {
                var val = magFilters[key];
                magFiltersInvert[val] = key;
            });
            var minFiltersInvert = [];
            Object.keys(minFilters).forEach(function (key) {
                var val = minFilters[key];
                minFiltersInvert[val] = key;
            });
            var wrapModesInvert = [];
            Object.keys(wrapModes).forEach(function (key) {
                var val = wrapModes[key];
                wrapModesInvert[val] = key;
            });
            // colorFormats[] gives the format (channels) associated to an
            // internalformat
            var colorFormats = supportedFormats.reduce(function (color, key) {
                var glenum = textureFormats[key];
                if (glenum === GL_LUMINANCE ||
                    glenum === GL_ALPHA ||
                    glenum === GL_LUMINANCE ||
                    glenum === GL_LUMINANCE_ALPHA ||
                    glenum === GL_DEPTH_COMPONENT ||
                    glenum === GL_DEPTH_STENCIL ||
                    (extensions.ext_srgb &&
                        (glenum === GL_SRGB_EXT ||
                            glenum === GL_SRGB_ALPHA_EXT))) {
                    color[glenum] = glenum;
                }
                else if (glenum === GL_RGB5_A1 || key.indexOf('rgba') >= 0) {
                    color[glenum] = GL_RGBA$1;
                }
                else {
                    color[glenum] = GL_RGB;
                }
                return color;
            }, {});
            function TexFlags() {
                // format info
                this.internalformat = GL_RGBA$1;
                this.format = GL_RGBA$1;
                this.type = GL_UNSIGNED_BYTE$5;
                this.compressed = false;
                // pixel storage
                this.premultiplyAlpha = false;
                this.flipY = false;
                this.unpackAlignment = 1;
                this.colorSpace = GL_BROWSER_DEFAULT_WEBGL;
                // shape info
                this.width = 0;
                this.height = 0;
                this.channels = 0;
            }
            function copyFlags(result, other) {
                result.internalformat = other.internalformat;
                result.format = other.format;
                result.type = other.type;
                result.compressed = other.compressed;
                result.premultiplyAlpha = other.premultiplyAlpha;
                result.flipY = other.flipY;
                result.unpackAlignment = other.unpackAlignment;
                result.colorSpace = other.colorSpace;
                result.width = other.width;
                result.height = other.height;
                result.channels = other.channels;
            }
            function parseFlags(flags, options) {
                if (typeof options !== 'object' || !options) {
                    return;
                }
                if ('premultiplyAlpha' in options) {
                    check$1.type(options.premultiplyAlpha, 'boolean', 'invalid premultiplyAlpha');
                    flags.premultiplyAlpha = options.premultiplyAlpha;
                }
                if ('flipY' in options) {
                    check$1.type(options.flipY, 'boolean', 'invalid texture flip');
                    flags.flipY = options.flipY;
                }
                if ('alignment' in options) {
                    check$1.oneOf(options.alignment, [1, 2, 4, 8], 'invalid texture unpack alignment');
                    flags.unpackAlignment = options.alignment;
                }
                if ('colorSpace' in options) {
                    check$1.parameter(options.colorSpace, colorSpace, 'invalid colorSpace');
                    flags.colorSpace = colorSpace[options.colorSpace];
                }
                if ('type' in options) {
                    var type = options.type;
                    check$1(extensions.oes_texture_float ||
                        !(type === 'float' || type === 'float32'), 'you must enable the OES_texture_float extension in order to use floating point textures.');
                    check$1(extensions.oes_texture_half_float ||
                        !(type === 'half float' || type === 'float16'), 'you must enable the OES_texture_half_float extension in order to use 16-bit floating point textures.');
                    check$1(extensions.webgl_depth_texture ||
                        !(type === 'uint16' || type === 'uint32' || type === 'depth stencil'), 'you must enable the WEBGL_depth_texture extension in order to use depth/stencil textures.');
                    check$1.parameter(type, textureTypes, 'invalid texture type');
                    flags.type = textureTypes[type];
                }
                var w = flags.width;
                var h = flags.height;
                var c = flags.channels;
                var hasChannels = false;
                if ('shape' in options) {
                    check$1(Array.isArray(options.shape) && options.shape.length >= 2, 'shape must be an array');
                    w = options.shape[0];
                    h = options.shape[1];
                    if (options.shape.length === 3) {
                        c = options.shape[2];
                        check$1(c > 0 && c <= 4, 'invalid number of channels');
                        hasChannels = true;
                    }
                    check$1(w >= 0 && w <= limits.maxTextureSize, 'invalid width');
                    check$1(h >= 0 && h <= limits.maxTextureSize, 'invalid height');
                }
                else {
                    if ('radius' in options) {
                        w = h = options.radius;
                        check$1(w >= 0 && w <= limits.maxTextureSize, 'invalid radius');
                    }
                    if ('width' in options) {
                        w = options.width;
                        check$1(w >= 0 && w <= limits.maxTextureSize, 'invalid width');
                    }
                    if ('height' in options) {
                        h = options.height;
                        check$1(h >= 0 && h <= limits.maxTextureSize, 'invalid height');
                    }
                    if ('channels' in options) {
                        c = options.channels;
                        check$1(c > 0 && c <= 4, 'invalid number of channels');
                        hasChannels = true;
                    }
                }
                flags.width = w | 0;
                flags.height = h | 0;
                flags.channels = c | 0;
                var hasFormat = false;
                if ('format' in options) {
                    var formatStr = options.format;
                    check$1(extensions.webgl_depth_texture ||
                        !(formatStr === 'depth' || formatStr === 'depth stencil'), 'you must enable the WEBGL_depth_texture extension in order to use depth/stencil textures.');
                    check$1.parameter(formatStr, textureFormats, 'invalid texture format');
                    var internalformat = flags.internalformat = textureFormats[formatStr];
                    flags.format = colorFormats[internalformat];
                    if (formatStr in textureTypes) {
                        if (!('type' in options)) {
                            flags.type = textureTypes[formatStr];
                        }
                    }
                    if (formatStr in compressedTextureFormats) {
                        flags.compressed = true;
                    }
                    hasFormat = true;
                }
                // Reconcile channels and format
                if (!hasChannels && hasFormat) {
                    flags.channels = FORMAT_CHANNELS[flags.format];
                }
                else if (hasChannels && !hasFormat) {
                    if (flags.channels !== CHANNELS_FORMAT[flags.format]) {
                        flags.format = flags.internalformat = CHANNELS_FORMAT[flags.channels];
                    }
                }
                else if (hasFormat && hasChannels) {
                    check$1(flags.channels === FORMAT_CHANNELS[flags.format], 'number of channels inconsistent with specified format');
                }
            }
            function setFlags(flags) {
                gl.pixelStorei(GL_UNPACK_FLIP_Y_WEBGL, flags.flipY);
                gl.pixelStorei(GL_UNPACK_PREMULTIPLY_ALPHA_WEBGL, flags.premultiplyAlpha);
                gl.pixelStorei(GL_UNPACK_COLORSPACE_CONVERSION_WEBGL, flags.colorSpace);
                gl.pixelStorei(GL_UNPACK_ALIGNMENT, flags.unpackAlignment);
            }
            // -------------------------------------------------------
            // Tex image data
            // -------------------------------------------------------
            function TexImage() {
                TexFlags.call(this);
                this.xOffset = 0;
                this.yOffset = 0;
                // data
                this.data = null;
                this.needsFree = false;
                // html element
                this.element = null;
                // copyTexImage info
                this.needsCopy = false;
            }
            function parseImage(image, options) {
                var data = null;
                if (isPixelData(options)) {
                    data = options;
                }
                else if (options) {
                    check$1.type(options, 'object', 'invalid pixel data type');
                    parseFlags(image, options);
                    if ('x' in options) {
                        image.xOffset = options.x | 0;
                    }
                    if ('y' in options) {
                        image.yOffset = options.y | 0;
                    }
                    if (isPixelData(options.data)) {
                        data = options.data;
                    }
                }
                check$1(!image.compressed ||
                    data instanceof Uint8Array, 'compressed texture data must be stored in a uint8array');
                if (options.copy) {
                    check$1(!data, 'can not specify copy and data field for the same texture');
                    var viewW = contextState.viewportWidth;
                    var viewH = contextState.viewportHeight;
                    image.width = image.width || (viewW - image.xOffset);
                    image.height = image.height || (viewH - image.yOffset);
                    image.needsCopy = true;
                    check$1(image.xOffset >= 0 && image.xOffset < viewW &&
                        image.yOffset >= 0 && image.yOffset < viewH &&
                        image.width > 0 && image.width <= viewW &&
                        image.height > 0 && image.height <= viewH, 'copy texture read out of bounds');
                }
                else if (!data) {
                    image.width = image.width || 1;
                    image.height = image.height || 1;
                    image.channels = image.channels || 4;
                }
                else if (isTypedArray(data)) {
                    image.channels = image.channels || 4;
                    image.data = data;
                    if (!('type' in options) && image.type === GL_UNSIGNED_BYTE$5) {
                        image.type = typedArrayCode$1(data);
                    }
                }
                else if (isNumericArray(data)) {
                    image.channels = image.channels || 4;
                    convertData(image, data);
                    image.alignment = 1;
                    image.needsFree = true;
                }
                else if (isNDArrayLike(data)) {
                    var array = data.data;
                    if (!Array.isArray(array) && image.type === GL_UNSIGNED_BYTE$5) {
                        image.type = typedArrayCode$1(array);
                    }
                    var shape = data.shape;
                    var stride = data.stride;
                    var shapeX, shapeY, shapeC, strideX, strideY, strideC;
                    if (shape.length === 3) {
                        shapeC = shape[2];
                        strideC = stride[2];
                    }
                    else {
                        check$1(shape.length === 2, 'invalid ndarray pixel data, must be 2 or 3D');
                        shapeC = 1;
                        strideC = 1;
                    }
                    shapeX = shape[0];
                    shapeY = shape[1];
                    strideX = stride[0];
                    strideY = stride[1];
                    image.alignment = 1;
                    image.width = shapeX;
                    image.height = shapeY;
                    image.channels = shapeC;
                    image.format = image.internalformat = CHANNELS_FORMAT[shapeC];
                    image.needsFree = true;
                    transposeData(image, array, strideX, strideY, strideC, data.offset);
                }
                else if (isCanvasElement(data) || isOffscreenCanvas(data) || isContext2D(data)) {
                    if (isCanvasElement(data) || isOffscreenCanvas(data)) {
                        image.element = data;
                    }
                    else {
                        image.element = data.canvas;
                    }
                    image.width = image.element.width;
                    image.height = image.element.height;
                    image.channels = 4;
                }
                else if (isBitmap(data)) {
                    image.element = data;
                    image.width = data.width;
                    image.height = data.height;
                    image.channels = 4;
                }
                else if (isImageElement(data)) {
                    image.element = data;
                    image.width = data.naturalWidth;
                    image.height = data.naturalHeight;
                    image.channels = 4;
                }
                else if (isVideoElement(data)) {
                    image.element = data;
                    image.width = data.videoWidth;
                    image.height = data.videoHeight;
                    image.channels = 4;
                }
                else if (isRectArray(data)) {
                    var w = image.width || data[0].length;
                    var h = image.height || data.length;
                    var c = image.channels;
                    if (isArrayLike(data[0][0])) {
                        c = c || data[0][0].length;
                    }
                    else {
                        c = c || 1;
                    }
                    var arrayShape = flattenUtils.shape(data);
                    var n = 1;
                    for (var dd = 0; dd < arrayShape.length; ++dd) {
                        n *= arrayShape[dd];
                    }
                    var allocData = preConvert(image, n);
                    flattenUtils.flatten(data, arrayShape, '', allocData);
                    postConvert(image, allocData);
                    image.alignment = 1;
                    image.width = w;
                    image.height = h;
                    image.channels = c;
                    image.format = image.internalformat = CHANNELS_FORMAT[c];
                    image.needsFree = true;
                }
                if (image.type === GL_FLOAT$4) {
                    check$1(limits.extensions.indexOf('oes_texture_float') >= 0, 'oes_texture_float extension not enabled');
                }
                else if (image.type === GL_HALF_FLOAT_OES$1) {
                    check$1(limits.extensions.indexOf('oes_texture_half_float') >= 0, 'oes_texture_half_float extension not enabled');
                }
                // do compressed texture  validation here.
            }
            function setImage(info, target, miplevel) {
                var element = info.element;
                var data = info.data;
                var internalformat = info.internalformat;
                var format = info.format;
                var type = info.type;
                var width = info.width;
                var height = info.height;
                setFlags(info);
                if (element) {
                    gl.texImage2D(target, miplevel, format, format, type, element);
                }
                else if (info.compressed) {
                    gl.compressedTexImage2D(target, miplevel, internalformat, width, height, 0, data);
                }
                else if (info.needsCopy) {
                    reglPoll();
                    gl.copyTexImage2D(target, miplevel, format, info.xOffset, info.yOffset, width, height, 0);
                }
                else {
                    gl.texImage2D(target, miplevel, format, width, height, 0, format, type, data || null);
                }
            }
            function setSubImage(info, target, x, y, miplevel) {
                var element = info.element;
                var data = info.data;
                var internalformat = info.internalformat;
                var format = info.format;
                var type = info.type;
                var width = info.width;
                var height = info.height;
                setFlags(info);
                if (element) {
                    gl.texSubImage2D(target, miplevel, x, y, format, type, element);
                }
                else if (info.compressed) {
                    gl.compressedTexSubImage2D(target, miplevel, x, y, internalformat, width, height, data);
                }
                else if (info.needsCopy) {
                    reglPoll();
                    gl.copyTexSubImage2D(target, miplevel, x, y, info.xOffset, info.yOffset, width, height);
                }
                else {
                    gl.texSubImage2D(target, miplevel, x, y, width, height, format, type, data);
                }
            }
            // texImage pool
            var imagePool = [];
            function allocImage() {
                return imagePool.pop() || new TexImage();
            }
            function freeImage(image) {
                if (image.needsFree) {
                    pool.freeType(image.data);
                }
                TexImage.call(image);
                imagePool.push(image);
            }
            // -------------------------------------------------------
            // Mip map
            // -------------------------------------------------------
            function MipMap() {
                TexFlags.call(this);
                this.genMipmaps = false;
                this.mipmapHint = GL_DONT_CARE;
                this.mipmask = 0;
                this.images = Array(16);
            }
            function parseMipMapFromShape(mipmap, width, height) {
                var img = mipmap.images[0] = allocImage();
                mipmap.mipmask = 1;
                img.width = mipmap.width = width;
                img.height = mipmap.height = height;
                img.channels = mipmap.channels = 4;
            }
            function parseMipMapFromObject(mipmap, options) {
                var imgData = null;
                if (isPixelData(options)) {
                    imgData = mipmap.images[0] = allocImage();
                    copyFlags(imgData, mipmap);
                    parseImage(imgData, options);
                    mipmap.mipmask = 1;
                }
                else {
                    parseFlags(mipmap, options);
                    if (Array.isArray(options.mipmap)) {
                        var mipData = options.mipmap;
                        for (var i = 0; i < mipData.length; ++i) {
                            imgData = mipmap.images[i] = allocImage();
                            copyFlags(imgData, mipmap);
                            imgData.width >>= i;
                            imgData.height >>= i;
                            parseImage(imgData, mipData[i]);
                            mipmap.mipmask |= (1 << i);
                        }
                    }
                    else {
                        imgData = mipmap.images[0] = allocImage();
                        copyFlags(imgData, mipmap);
                        parseImage(imgData, options);
                        mipmap.mipmask = 1;
                    }
                }
                copyFlags(mipmap, mipmap.images[0]);
                // For textures of the compressed format WEBGL_compressed_texture_s3tc
                // we must have that
                //
                // "When level equals zero width and height must be a multiple of 4.
                // When level is greater than 0 width and height must be 0, 1, 2 or a multiple of 4. "
                //
                // but we do not yet support having multiple mipmap levels for compressed textures,
                // so we only test for level zero.
                if (mipmap.compressed &&
                    (mipmap.internalformat === GL_COMPRESSED_RGB_S3TC_DXT1_EXT ||
                        mipmap.internalformat === GL_COMPRESSED_RGBA_S3TC_DXT1_EXT ||
                        mipmap.internalformat === GL_COMPRESSED_RGBA_S3TC_DXT3_EXT ||
                        mipmap.internalformat === GL_COMPRESSED_RGBA_S3TC_DXT5_EXT)) {
                    check$1(mipmap.width % 4 === 0 && mipmap.height % 4 === 0, 'for compressed texture formats, mipmap level 0 must have width and height that are a multiple of 4');
                }
            }
            function setMipMap(mipmap, target) {
                var images = mipmap.images;
                for (var i = 0; i < images.length; ++i) {
                    if (!images[i]) {
                        return;
                    }
                    setImage(images[i], target, i);
                }
            }
            var mipPool = [];
            function allocMipMap() {
                var result = mipPool.pop() || new MipMap();
                TexFlags.call(result);
                result.mipmask = 0;
                for (var i = 0; i < 16; ++i) {
                    result.images[i] = null;
                }
                return result;
            }
            function freeMipMap(mipmap) {
                var images = mipmap.images;
                for (var i = 0; i < images.length; ++i) {
                    if (images[i]) {
                        freeImage(images[i]);
                    }
                    images[i] = null;
                }
                mipPool.push(mipmap);
            }
            // -------------------------------------------------------
            // Tex info
            // -------------------------------------------------------
            function TexInfo() {
                this.minFilter = GL_NEAREST$1;
                this.magFilter = GL_NEAREST$1;
                this.wrapS = GL_CLAMP_TO_EDGE$1;
                this.wrapT = GL_CLAMP_TO_EDGE$1;
                this.anisotropic = 1;
                this.genMipmaps = false;
                this.mipmapHint = GL_DONT_CARE;
            }
            function parseTexInfo(info, options) {
                if ('min' in options) {
                    var minFilter = options.min;
                    check$1.parameter(minFilter, minFilters);
                    info.minFilter = minFilters[minFilter];
                    if (MIPMAP_FILTERS.indexOf(info.minFilter) >= 0 && !('faces' in options)) {
                        info.genMipmaps = true;
                    }
                }
                if ('mag' in options) {
                    var magFilter = options.mag;
                    check$1.parameter(magFilter, magFilters);
                    info.magFilter = magFilters[magFilter];
                }
                var wrapS = info.wrapS;
                var wrapT = info.wrapT;
                if ('wrap' in options) {
                    var wrap = options.wrap;
                    if (typeof wrap === 'string') {
                        check$1.parameter(wrap, wrapModes);
                        wrapS = wrapT = wrapModes[wrap];
                    }
                    else if (Array.isArray(wrap)) {
                        check$1.parameter(wrap[0], wrapModes);
                        check$1.parameter(wrap[1], wrapModes);
                        wrapS = wrapModes[wrap[0]];
                        wrapT = wrapModes[wrap[1]];
                    }
                }
                else {
                    if ('wrapS' in options) {
                        var optWrapS = options.wrapS;
                        check$1.parameter(optWrapS, wrapModes);
                        wrapS = wrapModes[optWrapS];
                    }
                    if ('wrapT' in options) {
                        var optWrapT = options.wrapT;
                        check$1.parameter(optWrapT, wrapModes);
                        wrapT = wrapModes[optWrapT];
                    }
                }
                info.wrapS = wrapS;
                info.wrapT = wrapT;
                if ('anisotropic' in options) {
                    var anisotropic = options.anisotropic;
                    check$1(typeof anisotropic === 'number' &&
                        anisotropic >= 1 && anisotropic <= limits.maxAnisotropic, 'aniso samples must be between 1 and ');
                    info.anisotropic = options.anisotropic;
                }
                if ('mipmap' in options) {
                    var hasMipMap = false;
                    switch (typeof options.mipmap) {
                        case 'string':
                            check$1.parameter(options.mipmap, mipmapHint, 'invalid mipmap hint');
                            info.mipmapHint = mipmapHint[options.mipmap];
                            info.genMipmaps = true;
                            hasMipMap = true;
                            break;
                        case 'boolean':
                            hasMipMap = info.genMipmaps = options.mipmap;
                            break;
                        case 'object':
                            check$1(Array.isArray(options.mipmap), 'invalid mipmap type');
                            info.genMipmaps = false;
                            hasMipMap = true;
                            break;
                        default:
                            check$1.raise('invalid mipmap type');
                    }
                    if (hasMipMap && !('min' in options)) {
                        info.minFilter = GL_NEAREST_MIPMAP_NEAREST$1;
                    }
                }
            }
            function setTexInfo(info, target) {
                gl.texParameteri(target, GL_TEXTURE_MIN_FILTER, info.minFilter);
                gl.texParameteri(target, GL_TEXTURE_MAG_FILTER, info.magFilter);
                gl.texParameteri(target, GL_TEXTURE_WRAP_S, info.wrapS);
                gl.texParameteri(target, GL_TEXTURE_WRAP_T, info.wrapT);
                if (extensions.ext_texture_filter_anisotropic) {
                    gl.texParameteri(target, GL_TEXTURE_MAX_ANISOTROPY_EXT, info.anisotropic);
                }
                if (info.genMipmaps) {
                    gl.hint(GL_GENERATE_MIPMAP_HINT, info.mipmapHint);
                    gl.generateMipmap(target);
                }
            }
            // -------------------------------------------------------
            // Full texture object
            // -------------------------------------------------------
            var textureCount = 0;
            var textureSet = {};
            var numTexUnits = limits.maxTextureUnits;
            var textureUnits = Array(numTexUnits).map(function () {
                return null;
            });
            function REGLTexture(target) {
                TexFlags.call(this);
                this.mipmask = 0;
                this.internalformat = GL_RGBA$1;
                this.id = textureCount++;
                this.refCount = 1;
                this.target = target;
                this.texture = gl.createTexture();
                this.unit = -1;
                this.bindCount = 0;
                this.texInfo = new TexInfo();
                if (config.profile) {
                    this.stats = { size: 0 };
                }
            }
            function tempBind(texture) {
                gl.activeTexture(GL_TEXTURE0$1);
                gl.bindTexture(texture.target, texture.texture);
            }
            function tempRestore() {
                var prev = textureUnits[0];
                if (prev) {
                    gl.bindTexture(prev.target, prev.texture);
                }
                else {
                    gl.bindTexture(GL_TEXTURE_2D$1, null);
                }
            }
            function destroy(texture) {
                var handle = texture.texture;
                check$1(handle, 'must not double destroy texture');
                var unit = texture.unit;
                var target = texture.target;
                if (unit >= 0) {
                    gl.activeTexture(GL_TEXTURE0$1 + unit);
                    gl.bindTexture(target, null);
                    textureUnits[unit] = null;
                }
                gl.deleteTexture(handle);
                texture.texture = null;
                texture.params = null;
                texture.pixels = null;
                texture.refCount = 0;
                delete textureSet[texture.id];
                stats.textureCount--;
            }
            extend(REGLTexture.prototype, {
                bind: function () {
                    var texture = this;
                    texture.bindCount += 1;
                    var unit = texture.unit;
                    if (unit < 0) {
                        for (var i = 0; i < numTexUnits; ++i) {
                            var other = textureUnits[i];
                            if (other) {
                                if (other.bindCount > 0) {
                                    continue;
                                }
                                other.unit = -1;
                            }
                            textureUnits[i] = texture;
                            unit = i;
                            break;
                        }
                        if (unit >= numTexUnits) {
                            check$1.raise('insufficient number of texture units');
                        }
                        if (config.profile && stats.maxTextureUnits < (unit + 1)) {
                            stats.maxTextureUnits = unit + 1; // +1, since the units are zero-based
                        }
                        texture.unit = unit;
                        gl.activeTexture(GL_TEXTURE0$1 + unit);
                        gl.bindTexture(texture.target, texture.texture);
                    }
                    return unit;
                },
                unbind: function () {
                    this.bindCount -= 1;
                },
                decRef: function () {
                    if (--this.refCount <= 0) {
                        destroy(this);
                    }
                }
            });
            function createTexture2D(a, b) {
                var texture = new REGLTexture(GL_TEXTURE_2D$1);
                textureSet[texture.id] = texture;
                stats.textureCount++;
                function reglTexture2D(a, b) {
                    var texInfo = texture.texInfo;
                    TexInfo.call(texInfo);
                    var mipData = allocMipMap();
                    if (typeof a === 'number') {
                        if (typeof b === 'number') {
                            parseMipMapFromShape(mipData, a | 0, b | 0);
                        }
                        else {
                            parseMipMapFromShape(mipData, a | 0, a | 0);
                        }
                    }
                    else if (a) {
                        check$1.type(a, 'object', 'invalid arguments to regl.texture');
                        parseTexInfo(texInfo, a);
                        parseMipMapFromObject(mipData, a);
                    }
                    else {
                        // empty textures get assigned a default shape of 1x1
                        parseMipMapFromShape(mipData, 1, 1);
                    }
                    if (texInfo.genMipmaps) {
                        mipData.mipmask = (mipData.width << 1) - 1;
                    }
                    texture.mipmask = mipData.mipmask;
                    copyFlags(texture, mipData);
                    check$1.texture2D(texInfo, mipData, limits);
                    texture.internalformat = mipData.internalformat;
                    reglTexture2D.width = mipData.width;
                    reglTexture2D.height = mipData.height;
                    tempBind(texture);
                    setMipMap(mipData, GL_TEXTURE_2D$1);
                    setTexInfo(texInfo, GL_TEXTURE_2D$1);
                    tempRestore();
                    freeMipMap(mipData);
                    if (config.profile) {
                        texture.stats.size = getTextureSize(texture.internalformat, texture.type, mipData.width, mipData.height, texInfo.genMipmaps, false);
                    }
                    reglTexture2D.format = textureFormatsInvert[texture.internalformat];
                    reglTexture2D.type = textureTypesInvert[texture.type];
                    reglTexture2D.mag = magFiltersInvert[texInfo.magFilter];
                    reglTexture2D.min = minFiltersInvert[texInfo.minFilter];
                    reglTexture2D.wrapS = wrapModesInvert[texInfo.wrapS];
                    reglTexture2D.wrapT = wrapModesInvert[texInfo.wrapT];
                    return reglTexture2D;
                }
                function subimage(image, x_, y_, level_) {
                    check$1(!!image, 'must specify image data');
                    var x = x_ | 0;
                    var y = y_ | 0;
                    var level = level_ | 0;
                    var imageData = allocImage();
                    copyFlags(imageData, texture);
                    imageData.width = 0;
                    imageData.height = 0;
                    parseImage(imageData, image);
                    imageData.width = imageData.width || ((texture.width >> level) - x);
                    imageData.height = imageData.height || ((texture.height >> level) - y);
                    check$1(texture.type === imageData.type &&
                        texture.format === imageData.format &&
                        texture.internalformat === imageData.internalformat, 'incompatible format for texture.subimage');
                    check$1(x >= 0 && y >= 0 &&
                        x + imageData.width <= texture.width &&
                        y + imageData.height <= texture.height, 'texture.subimage write out of bounds');
                    check$1(texture.mipmask & (1 << level), 'missing mipmap data');
                    check$1(imageData.data || imageData.element || imageData.needsCopy, 'missing image data');
                    tempBind(texture);
                    setSubImage(imageData, GL_TEXTURE_2D$1, x, y, level);
                    tempRestore();
                    freeImage(imageData);
                    return reglTexture2D;
                }
                function resize(w_, h_) {
                    var w = w_ | 0;
                    var h = (h_ | 0) || w;
                    if (w === texture.width && h === texture.height) {
                        return reglTexture2D;
                    }
                    reglTexture2D.width = texture.width = w;
                    reglTexture2D.height = texture.height = h;
                    tempBind(texture);
                    for (var i = 0; texture.mipmask >> i; ++i) {
                        var _w = w >> i;
                        var _h = h >> i;
                        if (!_w || !_h)
                            break;
                        gl.texImage2D(GL_TEXTURE_2D$1, i, texture.format, _w, _h, 0, texture.format, texture.type, null);
                    }
                    tempRestore();
                    // also, recompute the texture size.
                    if (config.profile) {
                        texture.stats.size = getTextureSize(texture.internalformat, texture.type, w, h, false, false);
                    }
                    return reglTexture2D;
                }
                reglTexture2D(a, b);
                reglTexture2D.subimage = subimage;
                reglTexture2D.resize = resize;
                reglTexture2D._reglType = 'texture2d';
                reglTexture2D._texture = texture;
                if (config.profile) {
                    reglTexture2D.stats = texture.stats;
                }
                reglTexture2D.destroy = function () {
                    texture.decRef();
                };
                return reglTexture2D;
            }
            function createTextureCube(a0, a1, a2, a3, a4, a5) {
                var texture = new REGLTexture(GL_TEXTURE_CUBE_MAP$1);
                textureSet[texture.id] = texture;
                stats.cubeCount++;
                var faces = new Array(6);
                function reglTextureCube(a0, a1, a2, a3, a4, a5) {
                    var i;
                    var texInfo = texture.texInfo;
                    TexInfo.call(texInfo);
                    for (i = 0; i < 6; ++i) {
                        faces[i] = allocMipMap();
                    }
                    if (typeof a0 === 'number' || !a0) {
                        var s = (a0 | 0) || 1;
                        for (i = 0; i < 6; ++i) {
                            parseMipMapFromShape(faces[i], s, s);
                        }
                    }
                    else if (typeof a0 === 'object') {
                        if (a1) {
                            parseMipMapFromObject(faces[0], a0);
                            parseMipMapFromObject(faces[1], a1);
                            parseMipMapFromObject(faces[2], a2);
                            parseMipMapFromObject(faces[3], a3);
                            parseMipMapFromObject(faces[4], a4);
                            parseMipMapFromObject(faces[5], a5);
                        }
                        else {
                            parseTexInfo(texInfo, a0);
                            parseFlags(texture, a0);
                            if ('faces' in a0) {
                                var faceInput = a0.faces;
                                check$1(Array.isArray(faceInput) && faceInput.length === 6, 'cube faces must be a length 6 array');
                                for (i = 0; i < 6; ++i) {
                                    check$1(typeof faceInput[i] === 'object' && !!faceInput[i], 'invalid input for cube map face');
                                    copyFlags(faces[i], texture);
                                    parseMipMapFromObject(faces[i], faceInput[i]);
                                }
                            }
                            else {
                                for (i = 0; i < 6; ++i) {
                                    parseMipMapFromObject(faces[i], a0);
                                }
                            }
                        }
                    }
                    else {
                        check$1.raise('invalid arguments to cube map');
                    }
                    copyFlags(texture, faces[0]);
                    check$1.optional(function () {
                        if (!limits.npotTextureCube) {
                            check$1(isPow2$1(texture.width) && isPow2$1(texture.height), 'your browser does not support non power or two texture dimensions');
                        }
                    });
                    if (texInfo.genMipmaps) {
                        texture.mipmask = (faces[0].width << 1) - 1;
                    }
                    else {
                        texture.mipmask = faces[0].mipmask;
                    }
                    check$1.textureCube(texture, texInfo, faces, limits);
                    texture.internalformat = faces[0].internalformat;
                    reglTextureCube.width = faces[0].width;
                    reglTextureCube.height = faces[0].height;
                    tempBind(texture);
                    for (i = 0; i < 6; ++i) {
                        setMipMap(faces[i], GL_TEXTURE_CUBE_MAP_POSITIVE_X$1 + i);
                    }
                    setTexInfo(texInfo, GL_TEXTURE_CUBE_MAP$1);
                    tempRestore();
                    if (config.profile) {
                        texture.stats.size = getTextureSize(texture.internalformat, texture.type, reglTextureCube.width, reglTextureCube.height, texInfo.genMipmaps, true);
                    }
                    reglTextureCube.format = textureFormatsInvert[texture.internalformat];
                    reglTextureCube.type = textureTypesInvert[texture.type];
                    reglTextureCube.mag = magFiltersInvert[texInfo.magFilter];
                    reglTextureCube.min = minFiltersInvert[texInfo.minFilter];
                    reglTextureCube.wrapS = wrapModesInvert[texInfo.wrapS];
                    reglTextureCube.wrapT = wrapModesInvert[texInfo.wrapT];
                    for (i = 0; i < 6; ++i) {
                        freeMipMap(faces[i]);
                    }
                    return reglTextureCube;
                }
                function subimage(face, image, x_, y_, level_) {
                    check$1(!!image, 'must specify image data');
                    check$1(typeof face === 'number' && face === (face | 0) &&
                        face >= 0 && face < 6, 'invalid face');
                    var x = x_ | 0;
                    var y = y_ | 0;
                    var level = level_ | 0;
                    var imageData = allocImage();
                    copyFlags(imageData, texture);
                    imageData.width = 0;
                    imageData.height = 0;
                    parseImage(imageData, image);
                    imageData.width = imageData.width || ((texture.width >> level) - x);
                    imageData.height = imageData.height || ((texture.height >> level) - y);
                    check$1(texture.type === imageData.type &&
                        texture.format === imageData.format &&
                        texture.internalformat === imageData.internalformat, 'incompatible format for texture.subimage');
                    check$1(x >= 0 && y >= 0 &&
                        x + imageData.width <= texture.width &&
                        y + imageData.height <= texture.height, 'texture.subimage write out of bounds');
                    check$1(texture.mipmask & (1 << level), 'missing mipmap data');
                    check$1(imageData.data || imageData.element || imageData.needsCopy, 'missing image data');
                    tempBind(texture);
                    setSubImage(imageData, GL_TEXTURE_CUBE_MAP_POSITIVE_X$1 + face, x, y, level);
                    tempRestore();
                    freeImage(imageData);
                    return reglTextureCube;
                }
                function resize(radius_) {
                    var radius = radius_ | 0;
                    if (radius === texture.width) {
                        return;
                    }
                    reglTextureCube.width = texture.width = radius;
                    reglTextureCube.height = texture.height = radius;
                    tempBind(texture);
                    for (var i = 0; i < 6; ++i) {
                        for (var j = 0; texture.mipmask >> j; ++j) {
                            gl.texImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X$1 + i, j, texture.format, radius >> j, radius >> j, 0, texture.format, texture.type, null);
                        }
                    }
                    tempRestore();
                    if (config.profile) {
                        texture.stats.size = getTextureSize(texture.internalformat, texture.type, reglTextureCube.width, reglTextureCube.height, false, true);
                    }
                    return reglTextureCube;
                }
                reglTextureCube(a0, a1, a2, a3, a4, a5);
                reglTextureCube.subimage = subimage;
                reglTextureCube.resize = resize;
                reglTextureCube._reglType = 'textureCube';
                reglTextureCube._texture = texture;
                if (config.profile) {
                    reglTextureCube.stats = texture.stats;
                }
                reglTextureCube.destroy = function () {
                    texture.decRef();
                };
                return reglTextureCube;
            }
            // Called when regl is destroyed
            function destroyTextures() {
                for (var i = 0; i < numTexUnits; ++i) {
                    gl.activeTexture(GL_TEXTURE0$1 + i);
                    gl.bindTexture(GL_TEXTURE_2D$1, null);
                    textureUnits[i] = null;
                }
                values(textureSet).forEach(destroy);
                stats.cubeCount = 0;
                stats.textureCount = 0;
            }
            if (config.profile) {
                stats.getTotalTextureSize = function () {
                    var total = 0;
                    Object.keys(textureSet).forEach(function (key) {
                        total += textureSet[key].stats.size;
                    });
                    return total;
                };
            }
            function restoreTextures() {
                for (var i = 0; i < numTexUnits; ++i) {
                    var tex = textureUnits[i];
                    if (tex) {
                        tex.bindCount = 0;
                        tex.unit = -1;
                        textureUnits[i] = null;
                    }
                }
                values(textureSet).forEach(function (texture) {
                    texture.texture = gl.createTexture();
                    gl.bindTexture(texture.target, texture.texture);
                    for (var i = 0; i < 32; ++i) {
                        if ((texture.mipmask & (1 << i)) === 0) {
                            continue;
                        }
                        if (texture.target === GL_TEXTURE_2D$1) {
                            gl.texImage2D(GL_TEXTURE_2D$1, i, texture.internalformat, texture.width >> i, texture.height >> i, 0, texture.internalformat, texture.type, null);
                        }
                        else {
                            for (var j = 0; j < 6; ++j) {
                                gl.texImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X$1 + j, i, texture.internalformat, texture.width >> i, texture.height >> i, 0, texture.internalformat, texture.type, null);
                            }
                        }
                    }
                    setTexInfo(texture.texInfo, texture.target);
                });
            }
            function refreshTextures() {
                for (var i = 0; i < numTexUnits; ++i) {
                    var tex = textureUnits[i];
                    if (tex) {
                        tex.bindCount = 0;
                        tex.unit = -1;
                        textureUnits[i] = null;
                    }
                    gl.activeTexture(GL_TEXTURE0$1 + i);
                    gl.bindTexture(GL_TEXTURE_2D$1, null);
                    gl.bindTexture(GL_TEXTURE_CUBE_MAP$1, null);
                }
            }
            return {
                create2D: createTexture2D,
                createCube: createTextureCube,
                clear: destroyTextures,
                getTexture: function (wrapper) {
                    return null;
                },
                restore: restoreTextures,
                refresh: refreshTextures
            };
        }
        var GL_RENDERBUFFER = 0x8D41;
        var GL_RGBA4$1 = 0x8056;
        var GL_RGB5_A1$1 = 0x8057;
        var GL_RGB565$1 = 0x8D62;
        var GL_DEPTH_COMPONENT16 = 0x81A5;
        var GL_STENCIL_INDEX8 = 0x8D48;
        var GL_DEPTH_STENCIL$1 = 0x84F9;
        var GL_SRGB8_ALPHA8_EXT = 0x8C43;
        var GL_RGBA32F_EXT = 0x8814;
        var GL_RGBA16F_EXT = 0x881A;
        var GL_RGB16F_EXT = 0x881B;
        var FORMAT_SIZES = [];
        FORMAT_SIZES[GL_RGBA4$1] = 2;
        FORMAT_SIZES[GL_RGB5_A1$1] = 2;
        FORMAT_SIZES[GL_RGB565$1] = 2;
        FORMAT_SIZES[GL_DEPTH_COMPONENT16] = 2;
        FORMAT_SIZES[GL_STENCIL_INDEX8] = 1;
        FORMAT_SIZES[GL_DEPTH_STENCIL$1] = 4;
        FORMAT_SIZES[GL_SRGB8_ALPHA8_EXT] = 4;
        FORMAT_SIZES[GL_RGBA32F_EXT] = 16;
        FORMAT_SIZES[GL_RGBA16F_EXT] = 8;
        FORMAT_SIZES[GL_RGB16F_EXT] = 6;
        function getRenderbufferSize(format, width, height) {
            return FORMAT_SIZES[format] * width * height;
        }
        var wrapRenderbuffers = function (gl, extensions, limits, stats, config) {
            var formatTypes = {
                'rgba4': GL_RGBA4$1,
                'rgb565': GL_RGB565$1,
                'rgb5 a1': GL_RGB5_A1$1,
                'depth': GL_DEPTH_COMPONENT16,
                'stencil': GL_STENCIL_INDEX8,
                'depth stencil': GL_DEPTH_STENCIL$1
            };
            if (extensions.ext_srgb) {
                formatTypes['srgba'] = GL_SRGB8_ALPHA8_EXT;
            }
            if (extensions.ext_color_buffer_half_float) {
                formatTypes['rgba16f'] = GL_RGBA16F_EXT;
                formatTypes['rgb16f'] = GL_RGB16F_EXT;
            }
            if (extensions.webgl_color_buffer_float) {
                formatTypes['rgba32f'] = GL_RGBA32F_EXT;
            }
            var formatTypesInvert = [];
            Object.keys(formatTypes).forEach(function (key) {
                var val = formatTypes[key];
                formatTypesInvert[val] = key;
            });
            var renderbufferCount = 0;
            var renderbufferSet = {};
            function REGLRenderbuffer(renderbuffer) {
                this.id = renderbufferCount++;
                this.refCount = 1;
                this.renderbuffer = renderbuffer;
                this.format = GL_RGBA4$1;
                this.width = 0;
                this.height = 0;
                if (config.profile) {
                    this.stats = { size: 0 };
                }
            }
            REGLRenderbuffer.prototype.decRef = function () {
                if (--this.refCount <= 0) {
                    destroy(this);
                }
            };
            function destroy(rb) {
                var handle = rb.renderbuffer;
                check$1(handle, 'must not double destroy renderbuffer');
                gl.bindRenderbuffer(GL_RENDERBUFFER, null);
                gl.deleteRenderbuffer(handle);
                rb.renderbuffer = null;
                rb.refCount = 0;
                delete renderbufferSet[rb.id];
                stats.renderbufferCount--;
            }
            function createRenderbuffer(a, b) {
                var renderbuffer = new REGLRenderbuffer(gl.createRenderbuffer());
                renderbufferSet[renderbuffer.id] = renderbuffer;
                stats.renderbufferCount++;
                function reglRenderbuffer(a, b) {
                    var w = 0;
                    var h = 0;
                    var format = GL_RGBA4$1;
                    if (typeof a === 'object' && a) {
                        var options = a;
                        if ('shape' in options) {
                            var shape = options.shape;
                            check$1(Array.isArray(shape) && shape.length >= 2, 'invalid renderbuffer shape');
                            w = shape[0] | 0;
                            h = shape[1] | 0;
                        }
                        else {
                            if ('radius' in options) {
                                w = h = options.radius | 0;
                            }
                            if ('width' in options) {
                                w = options.width | 0;
                            }
                            if ('height' in options) {
                                h = options.height | 0;
                            }
                        }
                        if ('format' in options) {
                            check$1.parameter(options.format, formatTypes, 'invalid renderbuffer format');
                            format = formatTypes[options.format];
                        }
                    }
                    else if (typeof a === 'number') {
                        w = a | 0;
                        if (typeof b === 'number') {
                            h = b | 0;
                        }
                        else {
                            h = w;
                        }
                    }
                    else if (!a) {
                        w = h = 1;
                    }
                    else {
                        check$1.raise('invalid arguments to renderbuffer constructor');
                    }
                    // check shape
                    check$1(w > 0 && h > 0 &&
                        w <= limits.maxRenderbufferSize && h <= limits.maxRenderbufferSize, 'invalid renderbuffer size');
                    if (w === renderbuffer.width &&
                        h === renderbuffer.height &&
                        format === renderbuffer.format) {
                        return;
                    }
                    reglRenderbuffer.width = renderbuffer.width = w;
                    reglRenderbuffer.height = renderbuffer.height = h;
                    renderbuffer.format = format;
                    gl.bindRenderbuffer(GL_RENDERBUFFER, renderbuffer.renderbuffer);
                    gl.renderbufferStorage(GL_RENDERBUFFER, format, w, h);
                    check$1(gl.getError() === 0, 'invalid render buffer format');
                    if (config.profile) {
                        renderbuffer.stats.size = getRenderbufferSize(renderbuffer.format, renderbuffer.width, renderbuffer.height);
                    }
                    reglRenderbuffer.format = formatTypesInvert[renderbuffer.format];
                    return reglRenderbuffer;
                }
                function resize(w_, h_) {
                    var w = w_ | 0;
                    var h = (h_ | 0) || w;
                    if (w === renderbuffer.width && h === renderbuffer.height) {
                        return reglRenderbuffer;
                    }
                    // check shape
                    check$1(w > 0 && h > 0 &&
                        w <= limits.maxRenderbufferSize && h <= limits.maxRenderbufferSize, 'invalid renderbuffer size');
                    reglRenderbuffer.width = renderbuffer.width = w;
                    reglRenderbuffer.height = renderbuffer.height = h;
                    gl.bindRenderbuffer(GL_RENDERBUFFER, renderbuffer.renderbuffer);
                    gl.renderbufferStorage(GL_RENDERBUFFER, renderbuffer.format, w, h);
                    check$1(gl.getError() === 0, 'invalid render buffer format');
                    // also, recompute size.
                    if (config.profile) {
                        renderbuffer.stats.size = getRenderbufferSize(renderbuffer.format, renderbuffer.width, renderbuffer.height);
                    }
                    return reglRenderbuffer;
                }
                reglRenderbuffer(a, b);
                reglRenderbuffer.resize = resize;
                reglRenderbuffer._reglType = 'renderbuffer';
                reglRenderbuffer._renderbuffer = renderbuffer;
                if (config.profile) {
                    reglRenderbuffer.stats = renderbuffer.stats;
                }
                reglRenderbuffer.destroy = function () {
                    renderbuffer.decRef();
                };
                return reglRenderbuffer;
            }
            if (config.profile) {
                stats.getTotalRenderbufferSize = function () {
                    var total = 0;
                    Object.keys(renderbufferSet).forEach(function (key) {
                        total += renderbufferSet[key].stats.size;
                    });
                    return total;
                };
            }
            function restoreRenderbuffers() {
                values(renderbufferSet).forEach(function (rb) {
                    rb.renderbuffer = gl.createRenderbuffer();
                    gl.bindRenderbuffer(GL_RENDERBUFFER, rb.renderbuffer);
                    gl.renderbufferStorage(GL_RENDERBUFFER, rb.format, rb.width, rb.height);
                });
                gl.bindRenderbuffer(GL_RENDERBUFFER, null);
            }
            return {
                create: createRenderbuffer,
                clear: function () {
                    values(renderbufferSet).forEach(destroy);
                },
                restore: restoreRenderbuffers
            };
        };
        // We store these constants so that the minifier can inline them
        var GL_FRAMEBUFFER$1 = 0x8D40;
        var GL_RENDERBUFFER$1 = 0x8D41;
        var GL_TEXTURE_2D$2 = 0x0DE1;
        var GL_TEXTURE_CUBE_MAP_POSITIVE_X$2 = 0x8515;
        var GL_COLOR_ATTACHMENT0$1 = 0x8CE0;
        var GL_DEPTH_ATTACHMENT = 0x8D00;
        var GL_STENCIL_ATTACHMENT = 0x8D20;
        var GL_DEPTH_STENCIL_ATTACHMENT = 0x821A;
        var GL_FRAMEBUFFER_COMPLETE$1 = 0x8CD5;
        var GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT = 0x8CD6;
        var GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT = 0x8CD7;
        var GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS = 0x8CD9;
        var GL_FRAMEBUFFER_UNSUPPORTED = 0x8CDD;
        var GL_HALF_FLOAT_OES$2 = 0x8D61;
        var GL_UNSIGNED_BYTE$6 = 0x1401;
        var GL_FLOAT$5 = 0x1406;
        var GL_RGB$1 = 0x1907;
        var GL_RGBA$2 = 0x1908;
        var GL_DEPTH_COMPONENT$1 = 0x1902;
        var colorTextureFormatEnums = [
            GL_RGB$1,
            GL_RGBA$2
        ];
        // for every texture format, store
        // the number of channels
        var textureFormatChannels = [];
        textureFormatChannels[GL_RGBA$2] = 4;
        textureFormatChannels[GL_RGB$1] = 3;
        // for every texture type, store
        // the size in bytes.
        var textureTypeSizes = [];
        textureTypeSizes[GL_UNSIGNED_BYTE$6] = 1;
        textureTypeSizes[GL_FLOAT$5] = 4;
        textureTypeSizes[GL_HALF_FLOAT_OES$2] = 2;
        var GL_RGBA4$2 = 0x8056;
        var GL_RGB5_A1$2 = 0x8057;
        var GL_RGB565$2 = 0x8D62;
        var GL_DEPTH_COMPONENT16$1 = 0x81A5;
        var GL_STENCIL_INDEX8$1 = 0x8D48;
        var GL_DEPTH_STENCIL$2 = 0x84F9;
        var GL_SRGB8_ALPHA8_EXT$1 = 0x8C43;
        var GL_RGBA32F_EXT$1 = 0x8814;
        var GL_RGBA16F_EXT$1 = 0x881A;
        var GL_RGB16F_EXT$1 = 0x881B;
        var colorRenderbufferFormatEnums = [
            GL_RGBA4$2,
            GL_RGB5_A1$2,
            GL_RGB565$2,
            GL_SRGB8_ALPHA8_EXT$1,
            GL_RGBA16F_EXT$1,
            GL_RGB16F_EXT$1,
            GL_RGBA32F_EXT$1
        ];
        var statusCode = {};
        statusCode[GL_FRAMEBUFFER_COMPLETE$1] = 'complete';
        statusCode[GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT] = 'incomplete attachment';
        statusCode[GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS] = 'incomplete dimensions';
        statusCode[GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT] = 'incomplete, missing attachment';
        statusCode[GL_FRAMEBUFFER_UNSUPPORTED] = 'unsupported';
        function wrapFBOState(gl, extensions, limits, textureState, renderbufferState, stats) {
            var framebufferState = {
                cur: null,
                next: null,
                dirty: false,
                setFBO: null
            };
            var colorTextureFormats = ['rgba'];
            var colorRenderbufferFormats = ['rgba4', 'rgb565', 'rgb5 a1'];
            if (extensions.ext_srgb) {
                colorRenderbufferFormats.push('srgba');
            }
            if (extensions.ext_color_buffer_half_float) {
                colorRenderbufferFormats.push('rgba16f', 'rgb16f');
            }
            if (extensions.webgl_color_buffer_float) {
                colorRenderbufferFormats.push('rgba32f');
            }
            var colorTypes = ['uint8'];
            if (extensions.oes_texture_half_float) {
                colorTypes.push('half float', 'float16');
            }
            if (extensions.oes_texture_float) {
                colorTypes.push('float', 'float32');
            }
            function FramebufferAttachment(target, texture, renderbuffer) {
                this.target = target;
                this.texture = texture;
                this.renderbuffer = renderbuffer;
                var w = 0;
                var h = 0;
                if (texture) {
                    w = texture.width;
                    h = texture.height;
                }
                else if (renderbuffer) {
                    w = renderbuffer.width;
                    h = renderbuffer.height;
                }
                this.width = w;
                this.height = h;
            }
            function decRef(attachment) {
                if (attachment) {
                    if (attachment.texture) {
                        attachment.texture._texture.decRef();
                    }
                    if (attachment.renderbuffer) {
                        attachment.renderbuffer._renderbuffer.decRef();
                    }
                }
            }
            function incRefAndCheckShape(attachment, width, height) {
                if (!attachment) {
                    return;
                }
                if (attachment.texture) {
                    var texture = attachment.texture._texture;
                    var tw = Math.max(1, texture.width);
                    var th = Math.max(1, texture.height);
                    check$1(tw === width && th === height, 'inconsistent width/height for supplied texture');
                    texture.refCount += 1;
                }
                else {
                    var renderbuffer = attachment.renderbuffer._renderbuffer;
                    check$1(renderbuffer.width === width && renderbuffer.height === height, 'inconsistent width/height for renderbuffer');
                    renderbuffer.refCount += 1;
                }
            }
            function attach(location, attachment) {
                if (attachment) {
                    if (attachment.texture) {
                        gl.framebufferTexture2D(GL_FRAMEBUFFER$1, location, attachment.target, attachment.texture._texture.texture, 0);
                    }
                    else {
                        gl.framebufferRenderbuffer(GL_FRAMEBUFFER$1, location, GL_RENDERBUFFER$1, attachment.renderbuffer._renderbuffer.renderbuffer);
                    }
                }
            }
            function parseAttachment(attachment) {
                var target = GL_TEXTURE_2D$2;
                var texture = null;
                var renderbuffer = null;
                var data = attachment;
                if (typeof attachment === 'object') {
                    data = attachment.data;
                    if ('target' in attachment) {
                        target = attachment.target | 0;
                    }
                }
                check$1.type(data, 'function', 'invalid attachment data');
                var type = data._reglType;
                if (type === 'texture2d') {
                    texture = data;
                    check$1(target === GL_TEXTURE_2D$2);
                }
                else if (type === 'textureCube') {
                    texture = data;
                    check$1(target >= GL_TEXTURE_CUBE_MAP_POSITIVE_X$2 &&
                        target < GL_TEXTURE_CUBE_MAP_POSITIVE_X$2 + 6, 'invalid cube map target');
                }
                else if (type === 'renderbuffer') {
                    renderbuffer = data;
                    target = GL_RENDERBUFFER$1;
                }
                else {
                    check$1.raise('invalid regl object for attachment');
                }
                return new FramebufferAttachment(target, texture, renderbuffer);
            }
            function allocAttachment(width, height, isTexture, format, type) {
                if (isTexture) {
                    var texture = textureState.create2D({
                        width: width,
                        height: height,
                        format: format,
                        type: type
                    });
                    texture._texture.refCount = 0;
                    return new FramebufferAttachment(GL_TEXTURE_2D$2, texture, null);
                }
                else {
                    var rb = renderbufferState.create({
                        width: width,
                        height: height,
                        format: format
                    });
                    rb._renderbuffer.refCount = 0;
                    return new FramebufferAttachment(GL_RENDERBUFFER$1, null, rb);
                }
            }
            function unwrapAttachment(attachment) {
                return attachment && (attachment.texture || attachment.renderbuffer);
            }
            function resizeAttachment(attachment, w, h) {
                if (attachment) {
                    if (attachment.texture) {
                        attachment.texture.resize(w, h);
                    }
                    else if (attachment.renderbuffer) {
                        attachment.renderbuffer.resize(w, h);
                    }
                    attachment.width = w;
                    attachment.height = h;
                }
            }
            var framebufferCount = 0;
            var framebufferSet = {};
            function REGLFramebuffer() {
                this.id = framebufferCount++;
                framebufferSet[this.id] = this;
                this.framebuffer = gl.createFramebuffer();
                this.width = 0;
                this.height = 0;
                this.colorAttachments = [];
                this.depthAttachment = null;
                this.stencilAttachment = null;
                this.depthStencilAttachment = null;
            }
            function decFBORefs(framebuffer) {
                framebuffer.colorAttachments.forEach(decRef);
                decRef(framebuffer.depthAttachment);
                decRef(framebuffer.stencilAttachment);
                decRef(framebuffer.depthStencilAttachment);
            }
            function destroy(framebuffer) {
                var handle = framebuffer.framebuffer;
                check$1(handle, 'must not double destroy framebuffer');
                gl.deleteFramebuffer(handle);
                framebuffer.framebuffer = null;
                stats.framebufferCount--;
                delete framebufferSet[framebuffer.id];
            }
            function updateFramebuffer(framebuffer) {
                var i;
                gl.bindFramebuffer(GL_FRAMEBUFFER$1, framebuffer.framebuffer);
                var colorAttachments = framebuffer.colorAttachments;
                for (i = 0; i < colorAttachments.length; ++i) {
                    attach(GL_COLOR_ATTACHMENT0$1 + i, colorAttachments[i]);
                }
                for (i = colorAttachments.length; i < limits.maxColorAttachments; ++i) {
                    gl.framebufferTexture2D(GL_FRAMEBUFFER$1, GL_COLOR_ATTACHMENT0$1 + i, GL_TEXTURE_2D$2, null, 0);
                }
                gl.framebufferTexture2D(GL_FRAMEBUFFER$1, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D$2, null, 0);
                gl.framebufferTexture2D(GL_FRAMEBUFFER$1, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D$2, null, 0);
                gl.framebufferTexture2D(GL_FRAMEBUFFER$1, GL_STENCIL_ATTACHMENT, GL_TEXTURE_2D$2, null, 0);
                attach(GL_DEPTH_ATTACHMENT, framebuffer.depthAttachment);
                attach(GL_STENCIL_ATTACHMENT, framebuffer.stencilAttachment);
                attach(GL_DEPTH_STENCIL_ATTACHMENT, framebuffer.depthStencilAttachment);
                // Check status code
                var status = gl.checkFramebufferStatus(GL_FRAMEBUFFER$1);
                if (!gl.isContextLost() && status !== GL_FRAMEBUFFER_COMPLETE$1) {
                    check$1.raise('framebuffer configuration not supported, status = ' +
                        statusCode[status]);
                }
                gl.bindFramebuffer(GL_FRAMEBUFFER$1, framebufferState.next ? framebufferState.next.framebuffer : null);
                framebufferState.cur = framebufferState.next;
                // FIXME: Clear error code here.  This is a work around for a bug in
                // headless-gl
                gl.getError();
            }
            function createFBO(a0, a1) {
                var framebuffer = new REGLFramebuffer();
                stats.framebufferCount++;
                function reglFramebuffer(a, b) {
                    var i;
                    check$1(framebufferState.next !== framebuffer, 'can not update framebuffer which is currently in use');
                    var width = 0;
                    var height = 0;
                    var needsDepth = true;
                    var needsStencil = true;
                    var colorBuffer = null;
                    var colorTexture = true;
                    var colorFormat = 'rgba';
                    var colorType = 'uint8';
                    var colorCount = 1;
                    var depthBuffer = null;
                    var stencilBuffer = null;
                    var depthStencilBuffer = null;
                    var depthStencilTexture = false;
                    if (typeof a === 'number') {
                        width = a | 0;
                        height = (b | 0) || width;
                    }
                    else if (!a) {
                        width = height = 1;
                    }
                    else {
                        check$1.type(a, 'object', 'invalid arguments for framebuffer');
                        var options = a;
                        if ('shape' in options) {
                            var shape = options.shape;
                            check$1(Array.isArray(shape) && shape.length >= 2, 'invalid shape for framebuffer');
                            width = shape[0];
                            height = shape[1];
                        }
                        else {
                            if ('radius' in options) {
                                width = height = options.radius;
                            }
                            if ('width' in options) {
                                width = options.width;
                            }
                            if ('height' in options) {
                                height = options.height;
                            }
                        }
                        if ('color' in options ||
                            'colors' in options) {
                            colorBuffer =
                                options.color ||
                                    options.colors;
                            if (Array.isArray(colorBuffer)) {
                                check$1(colorBuffer.length === 1 || extensions.webgl_draw_buffers, 'multiple render targets not supported');
                            }
                        }
                        if (!colorBuffer) {
                            if ('colorCount' in options) {
                                colorCount = options.colorCount | 0;
                                check$1(colorCount > 0, 'invalid color buffer count');
                            }
                            if ('colorTexture' in options) {
                                colorTexture = !!options.colorTexture;
                                colorFormat = 'rgba4';
                            }
                            if ('colorType' in options) {
                                colorType = options.colorType;
                                if (!colorTexture) {
                                    if (colorType === 'half float' || colorType === 'float16') {
                                        check$1(extensions.ext_color_buffer_half_float, 'you must enable EXT_color_buffer_half_float to use 16-bit render buffers');
                                        colorFormat = 'rgba16f';
                                    }
                                    else if (colorType === 'float' || colorType === 'float32') {
                                        check$1(extensions.webgl_color_buffer_float, 'you must enable WEBGL_color_buffer_float in order to use 32-bit floating point renderbuffers');
                                        colorFormat = 'rgba32f';
                                    }
                                }
                                else {
                                    check$1(extensions.oes_texture_float ||
                                        !(colorType === 'float' || colorType === 'float32'), 'you must enable OES_texture_float in order to use floating point framebuffer objects');
                                    check$1(extensions.oes_texture_half_float ||
                                        !(colorType === 'half float' || colorType === 'float16'), 'you must enable OES_texture_half_float in order to use 16-bit floating point framebuffer objects');
                                }
                                check$1.oneOf(colorType, colorTypes, 'invalid color type');
                            }
                            if ('colorFormat' in options) {
                                colorFormat = options.colorFormat;
                                if (colorTextureFormats.indexOf(colorFormat) >= 0) {
                                    colorTexture = true;
                                }
                                else if (colorRenderbufferFormats.indexOf(colorFormat) >= 0) {
                                    colorTexture = false;
                                }
                                else {
                                    check$1.optional(function () {
                                        if (colorTexture) {
                                            check$1.oneOf(options.colorFormat, colorTextureFormats, 'invalid color format for texture');
                                        }
                                        else {
                                            check$1.oneOf(options.colorFormat, colorRenderbufferFormats, 'invalid color format for renderbuffer');
                                        }
                                    });
                                }
                            }
                        }
                        if ('depthTexture' in options || 'depthStencilTexture' in options) {
                            depthStencilTexture = !!(options.depthTexture ||
                                options.depthStencilTexture);
                            check$1(!depthStencilTexture || extensions.webgl_depth_texture, 'webgl_depth_texture extension not supported');
                        }
                        if ('depth' in options) {
                            if (typeof options.depth === 'boolean') {
                                needsDepth = options.depth;
                            }
                            else {
                                depthBuffer = options.depth;
                                needsStencil = false;
                            }
                        }
                        if ('stencil' in options) {
                            if (typeof options.stencil === 'boolean') {
                                needsStencil = options.stencil;
                            }
                            else {
                                stencilBuffer = options.stencil;
                                needsDepth = false;
                            }
                        }
                        if ('depthStencil' in options) {
                            if (typeof options.depthStencil === 'boolean') {
                                needsDepth = needsStencil = options.depthStencil;
                            }
                            else {
                                depthStencilBuffer = options.depthStencil;
                                needsDepth = false;
                                needsStencil = false;
                            }
                        }
                    }
                    // parse attachments
                    var colorAttachments = null;
                    var depthAttachment = null;
                    var stencilAttachment = null;
                    var depthStencilAttachment = null;
                    // Set up color attachments
                    if (Array.isArray(colorBuffer)) {
                        colorAttachments = colorBuffer.map(parseAttachment);
                    }
                    else if (colorBuffer) {
                        colorAttachments = [parseAttachment(colorBuffer)];
                    }
                    else {
                        colorAttachments = new Array(colorCount);
                        for (i = 0; i < colorCount; ++i) {
                            colorAttachments[i] = allocAttachment(width, height, colorTexture, colorFormat, colorType);
                        }
                    }
                    check$1(extensions.webgl_draw_buffers || colorAttachments.length <= 1, 'you must enable the WEBGL_draw_buffers extension in order to use multiple color buffers.');
                    check$1(colorAttachments.length <= limits.maxColorAttachments, 'too many color attachments, not supported');
                    width = width || colorAttachments[0].width;
                    height = height || colorAttachments[0].height;
                    if (depthBuffer) {
                        depthAttachment = parseAttachment(depthBuffer);
                    }
                    else if (needsDepth && !needsStencil) {
                        depthAttachment = allocAttachment(width, height, depthStencilTexture, 'depth', 'uint32');
                    }
                    if (stencilBuffer) {
                        stencilAttachment = parseAttachment(stencilBuffer);
                    }
                    else if (needsStencil && !needsDepth) {
                        stencilAttachment = allocAttachment(width, height, false, 'stencil', 'uint8');
                    }
                    if (depthStencilBuffer) {
                        depthStencilAttachment = parseAttachment(depthStencilBuffer);
                    }
                    else if (!depthBuffer && !stencilBuffer && needsStencil && needsDepth) {
                        depthStencilAttachment = allocAttachment(width, height, depthStencilTexture, 'depth stencil', 'depth stencil');
                    }
                    check$1((!!depthBuffer) + (!!stencilBuffer) + (!!depthStencilBuffer) <= 1, 'invalid framebuffer configuration, can specify exactly one depth/stencil attachment');
                    var commonColorAttachmentSize = null;
                    for (i = 0; i < colorAttachments.length; ++i) {
                        incRefAndCheckShape(colorAttachments[i], width, height);
                        check$1(!colorAttachments[i] ||
                            (colorAttachments[i].texture &&
                                colorTextureFormatEnums.indexOf(colorAttachments[i].texture._texture.format) >= 0) ||
                            (colorAttachments[i].renderbuffer &&
                                colorRenderbufferFormatEnums.indexOf(colorAttachments[i].renderbuffer._renderbuffer.format) >= 0), 'framebuffer color attachment ' + i + ' is invalid');
                        if (colorAttachments[i] && colorAttachments[i].texture) {
                            var colorAttachmentSize = textureFormatChannels[colorAttachments[i].texture._texture.format] *
                                textureTypeSizes[colorAttachments[i].texture._texture.type];
                            if (commonColorAttachmentSize === null) {
                                commonColorAttachmentSize = colorAttachmentSize;
                            }
                            else {
                                // We need to make sure that all color attachments have the same number of bitplanes
                                // (that is, the same numer of bits per pixel)
                                // This is required by the GLES2.0 standard. See the beginning of Chapter 4 in that document.
                                check$1(commonColorAttachmentSize === colorAttachmentSize, 'all color attachments much have the same number of bits per pixel.');
                            }
                        }
                    }
                    incRefAndCheckShape(depthAttachment, width, height);
                    check$1(!depthAttachment ||
                        (depthAttachment.texture &&
                            depthAttachment.texture._texture.format === GL_DEPTH_COMPONENT$1) ||
                        (depthAttachment.renderbuffer &&
                            depthAttachment.renderbuffer._renderbuffer.format === GL_DEPTH_COMPONENT16$1), 'invalid depth attachment for framebuffer object');
                    incRefAndCheckShape(stencilAttachment, width, height);
                    check$1(!stencilAttachment ||
                        (stencilAttachment.renderbuffer &&
                            stencilAttachment.renderbuffer._renderbuffer.format === GL_STENCIL_INDEX8$1), 'invalid stencil attachment for framebuffer object');
                    incRefAndCheckShape(depthStencilAttachment, width, height);
                    check$1(!depthStencilAttachment ||
                        (depthStencilAttachment.texture &&
                            depthStencilAttachment.texture._texture.format === GL_DEPTH_STENCIL$2) ||
                        (depthStencilAttachment.renderbuffer &&
                            depthStencilAttachment.renderbuffer._renderbuffer.format === GL_DEPTH_STENCIL$2), 'invalid depth-stencil attachment for framebuffer object');
                    // decrement references
                    decFBORefs(framebuffer);
                    framebuffer.width = width;
                    framebuffer.height = height;
                    framebuffer.colorAttachments = colorAttachments;
                    framebuffer.depthAttachment = depthAttachment;
                    framebuffer.stencilAttachment = stencilAttachment;
                    framebuffer.depthStencilAttachment = depthStencilAttachment;
                    reglFramebuffer.color = colorAttachments.map(unwrapAttachment);
                    reglFramebuffer.depth = unwrapAttachment(depthAttachment);
                    reglFramebuffer.stencil = unwrapAttachment(stencilAttachment);
                    reglFramebuffer.depthStencil = unwrapAttachment(depthStencilAttachment);
                    reglFramebuffer.width = framebuffer.width;
                    reglFramebuffer.height = framebuffer.height;
                    updateFramebuffer(framebuffer);
                    return reglFramebuffer;
                }
                function resize(w_, h_) {
                    check$1(framebufferState.next !== framebuffer, 'can not resize a framebuffer which is currently in use');
                    var w = Math.max(w_ | 0, 1);
                    var h = Math.max((h_ | 0) || w, 1);
                    if (w === framebuffer.width && h === framebuffer.height) {
                        return reglFramebuffer;
                    }
                    // resize all buffers
                    var colorAttachments = framebuffer.colorAttachments;
                    for (var i = 0; i < colorAttachments.length; ++i) {
                        resizeAttachment(colorAttachments[i], w, h);
                    }
                    resizeAttachment(framebuffer.depthAttachment, w, h);
                    resizeAttachment(framebuffer.stencilAttachment, w, h);
                    resizeAttachment(framebuffer.depthStencilAttachment, w, h);
                    framebuffer.width = reglFramebuffer.width = w;
                    framebuffer.height = reglFramebuffer.height = h;
                    updateFramebuffer(framebuffer);
                    return reglFramebuffer;
                }
                reglFramebuffer(a0, a1);
                return extend(reglFramebuffer, {
                    resize: resize,
                    _reglType: 'framebuffer',
                    _framebuffer: framebuffer,
                    destroy: function () {
                        destroy(framebuffer);
                        decFBORefs(framebuffer);
                    },
                    use: function (block) {
                        framebufferState.setFBO({
                            framebuffer: reglFramebuffer
                        }, block);
                    }
                });
            }
            function createCubeFBO(options) {
                var faces = Array(6);
                function reglFramebufferCube(a) {
                    var i;
                    check$1(faces.indexOf(framebufferState.next) < 0, 'can not update framebuffer which is currently in use');
                    var params = {
                        color: null
                    };
                    var radius = 0;
                    var colorBuffer = null;
                    var colorFormat = 'rgba';
                    var colorType = 'uint8';
                    var colorCount = 1;
                    if (typeof a === 'number') {
                        radius = a | 0;
                    }
                    else if (!a) {
                        radius = 1;
                    }
                    else {
                        check$1.type(a, 'object', 'invalid arguments for framebuffer');
                        var options = a;
                        if ('shape' in options) {
                            var shape = options.shape;
                            check$1(Array.isArray(shape) && shape.length >= 2, 'invalid shape for framebuffer');
                            check$1(shape[0] === shape[1], 'cube framebuffer must be square');
                            radius = shape[0];
                        }
                        else {
                            if ('radius' in options) {
                                radius = options.radius | 0;
                            }
                            if ('width' in options) {
                                radius = options.width | 0;
                                if ('height' in options) {
                                    check$1(options.height === radius, 'must be square');
                                }
                            }
                            else if ('height' in options) {
                                radius = options.height | 0;
                            }
                        }
                        if ('color' in options ||
                            'colors' in options) {
                            colorBuffer =
                                options.color ||
                                    options.colors;
                            if (Array.isArray(colorBuffer)) {
                                check$1(colorBuffer.length === 1 || extensions.webgl_draw_buffers, 'multiple render targets not supported');
                            }
                        }
                        if (!colorBuffer) {
                            if ('colorCount' in options) {
                                colorCount = options.colorCount | 0;
                                check$1(colorCount > 0, 'invalid color buffer count');
                            }
                            if ('colorType' in options) {
                                check$1.oneOf(options.colorType, colorTypes, 'invalid color type');
                                colorType = options.colorType;
                            }
                            if ('colorFormat' in options) {
                                colorFormat = options.colorFormat;
                                check$1.oneOf(options.colorFormat, colorTextureFormats, 'invalid color format for texture');
                            }
                        }
                        if ('depth' in options) {
                            params.depth = options.depth;
                        }
                        if ('stencil' in options) {
                            params.stencil = options.stencil;
                        }
                        if ('depthStencil' in options) {
                            params.depthStencil = options.depthStencil;
                        }
                    }
                    var colorCubes;
                    if (colorBuffer) {
                        if (Array.isArray(colorBuffer)) {
                            colorCubes = [];
                            for (i = 0; i < colorBuffer.length; ++i) {
                                colorCubes[i] = colorBuffer[i];
                            }
                        }
                        else {
                            colorCubes = [colorBuffer];
                        }
                    }
                    else {
                        colorCubes = Array(colorCount);
                        var cubeMapParams = {
                            radius: radius,
                            format: colorFormat,
                            type: colorType
                        };
                        for (i = 0; i < colorCount; ++i) {
                            colorCubes[i] = textureState.createCube(cubeMapParams);
                        }
                    }
                    // Check color cubes
                    params.color = Array(colorCubes.length);
                    for (i = 0; i < colorCubes.length; ++i) {
                        var cube = colorCubes[i];
                        check$1(typeof cube === 'function' && cube._reglType === 'textureCube', 'invalid cube map');
                        radius = radius || cube.width;
                        check$1(cube.width === radius && cube.height === radius, 'invalid cube map shape');
                        params.color[i] = {
                            target: GL_TEXTURE_CUBE_MAP_POSITIVE_X$2,
                            data: colorCubes[i]
                        };
                    }
                    for (i = 0; i < 6; ++i) {
                        for (var j = 0; j < colorCubes.length; ++j) {
                            params.color[j].target = GL_TEXTURE_CUBE_MAP_POSITIVE_X$2 + i;
                        }
                        // reuse depth-stencil attachments across all cube maps
                        if (i > 0) {
                            params.depth = faces[0].depth;
                            params.stencil = faces[0].stencil;
                            params.depthStencil = faces[0].depthStencil;
                        }
                        if (faces[i]) {
                            (faces[i])(params);
                        }
                        else {
                            faces[i] = createFBO(params);
                        }
                    }
                    return extend(reglFramebufferCube, {
                        width: radius,
                        height: radius,
                        color: colorCubes
                    });
                }
                function resize(radius_) {
                    var i;
                    var radius = radius_ | 0;
                    check$1(radius > 0 && radius <= limits.maxCubeMapSize, 'invalid radius for cube fbo');
                    if (radius === reglFramebufferCube.width) {
                        return reglFramebufferCube;
                    }
                    var colors = reglFramebufferCube.color;
                    for (i = 0; i < colors.length; ++i) {
                        colors[i].resize(radius);
                    }
                    for (i = 0; i < 6; ++i) {
                        faces[i].resize(radius);
                    }
                    reglFramebufferCube.width = reglFramebufferCube.height = radius;
                    return reglFramebufferCube;
                }
                reglFramebufferCube(options);
                return extend(reglFramebufferCube, {
                    faces: faces,
                    resize: resize,
                    _reglType: 'framebufferCube',
                    destroy: function () {
                        faces.forEach(function (f) {
                            f.destroy();
                        });
                    }
                });
            }
            function restoreFramebuffers() {
                framebufferState.cur = null;
                framebufferState.next = null;
                framebufferState.dirty = true;
                values(framebufferSet).forEach(function (fb) {
                    fb.framebuffer = gl.createFramebuffer();
                    updateFramebuffer(fb);
                });
            }
            return extend(framebufferState, {
                getFramebuffer: function (object) {
                    if (typeof object === 'function' && object._reglType === 'framebuffer') {
                        var fbo = object._framebuffer;
                        if (fbo instanceof REGLFramebuffer) {
                            return fbo;
                        }
                    }
                    return null;
                },
                create: createFBO,
                createCube: createCubeFBO,
                clear: function () {
                    values(framebufferSet).forEach(destroy);
                },
                restore: restoreFramebuffers
            });
        }
        var GL_FLOAT$6 = 5126;
        var GL_ARRAY_BUFFER$1 = 34962;
        var GL_ELEMENT_ARRAY_BUFFER$1 = 34963;
        var VAO_OPTIONS = [
            'attributes',
            'elements',
            'offset',
            'count',
            'primitive',
            'instances'
        ];
        function AttributeRecord() {
            this.state = 0;
            this.x = 0.0;
            this.y = 0.0;
            this.z = 0.0;
            this.w = 0.0;
            this.buffer = null;
            this.size = 0;
            this.normalized = false;
            this.type = GL_FLOAT$6;
            this.offset = 0;
            this.stride = 0;
            this.divisor = 0;
        }
        function wrapAttributeState(gl, extensions, limits, stats, bufferState, elementState, drawState) {
            var NUM_ATTRIBUTES = limits.maxAttributes;
            var attributeBindings = new Array(NUM_ATTRIBUTES);
            for (var i = 0; i < NUM_ATTRIBUTES; ++i) {
                attributeBindings[i] = new AttributeRecord();
            }
            var vaoCount = 0;
            var vaoSet = {};
            var state = {
                Record: AttributeRecord,
                scope: {},
                state: attributeBindings,
                currentVAO: null,
                targetVAO: null,
                restore: extVAO() ? restoreVAO : function () { },
                createVAO: createVAO,
                getVAO: getVAO,
                destroyBuffer: destroyBuffer,
                setVAO: extVAO() ? setVAOEXT : setVAOEmulated,
                clear: extVAO() ? destroyVAOEXT : function () { }
            };
            function destroyBuffer(buffer) {
                for (var i = 0; i < attributeBindings.length; ++i) {
                    var record = attributeBindings[i];
                    if (record.buffer === buffer) {
                        gl.disableVertexAttribArray(i);
                        record.buffer = null;
                    }
                }
            }
            function extVAO() {
                return extensions.oes_vertex_array_object;
            }
            function extInstanced() {
                return extensions.angle_instanced_arrays;
            }
            function getVAO(vao) {
                if (typeof vao === 'function' && vao._vao) {
                    return vao._vao;
                }
                return null;
            }
            function setVAOEXT(vao) {
                if (vao === state.currentVAO) {
                    return;
                }
                var ext = extVAO();
                if (vao) {
                    ext.bindVertexArrayOES(vao.vao);
                }
                else {
                    ext.bindVertexArrayOES(null);
                }
                state.currentVAO = vao;
            }
            function setVAOEmulated(vao) {
                if (vao === state.currentVAO) {
                    return;
                }
                if (vao) {
                    vao.bindAttrs();
                }
                else {
                    var exti = extInstanced();
                    for (var i = 0; i < attributeBindings.length; ++i) {
                        var binding = attributeBindings[i];
                        if (binding.buffer) {
                            gl.enableVertexAttribArray(i);
                            binding.buffer.bind();
                            gl.vertexAttribPointer(i, binding.size, binding.type, binding.normalized, binding.stride, binding.offfset);
                            if (exti && binding.divisor) {
                                exti.vertexAttribDivisorANGLE(i, binding.divisor);
                            }
                        }
                        else {
                            gl.disableVertexAttribArray(i);
                            gl.vertexAttrib4f(i, binding.x, binding.y, binding.z, binding.w);
                        }
                    }
                    if (drawState.elements) {
                        gl.bindBuffer(GL_ELEMENT_ARRAY_BUFFER$1, drawState.elements.buffer.buffer);
                    }
                    else {
                        gl.bindBuffer(GL_ELEMENT_ARRAY_BUFFER$1, null);
                    }
                }
                state.currentVAO = vao;
            }
            function destroyVAOEXT() {
                values(vaoSet).forEach(function (vao) {
                    vao.destroy();
                });
            }
            function REGLVAO() {
                this.id = ++vaoCount;
                this.attributes = [];
                this.elements = null;
                this.ownsElements = false;
                this.count = 0;
                this.offset = 0;
                this.instances = -1;
                this.primitive = 4;
                var extension = extVAO();
                if (extension) {
                    this.vao = extension.createVertexArrayOES();
                }
                else {
                    this.vao = null;
                }
                vaoSet[this.id] = this;
                this.buffers = [];
            }
            REGLVAO.prototype.bindAttrs = function () {
                var exti = extInstanced();
                var attributes = this.attributes;
                for (var i = 0; i < attributes.length; ++i) {
                    var attr = attributes[i];
                    if (attr.buffer) {
                        gl.enableVertexAttribArray(i);
                        gl.bindBuffer(GL_ARRAY_BUFFER$1, attr.buffer.buffer);
                        gl.vertexAttribPointer(i, attr.size, attr.type, attr.normalized, attr.stride, attr.offset);
                        if (exti && attr.divisor) {
                            exti.vertexAttribDivisorANGLE(i, attr.divisor);
                        }
                    }
                    else {
                        gl.disableVertexAttribArray(i);
                        gl.vertexAttrib4f(i, attr.x, attr.y, attr.z, attr.w);
                    }
                }
                for (var j = attributes.length; j < NUM_ATTRIBUTES; ++j) {
                    gl.disableVertexAttribArray(j);
                }
                var elements = elementState.getElements(this.elements);
                if (elements) {
                    gl.bindBuffer(GL_ELEMENT_ARRAY_BUFFER$1, elements.buffer.buffer);
                }
                else {
                    gl.bindBuffer(GL_ELEMENT_ARRAY_BUFFER$1, null);
                }
            };
            REGLVAO.prototype.refresh = function () {
                var ext = extVAO();
                if (ext) {
                    ext.bindVertexArrayOES(this.vao);
                    this.bindAttrs();
                    state.currentVAO = null;
                    ext.bindVertexArrayOES(null);
                }
            };
            REGLVAO.prototype.destroy = function () {
                if (this.vao) {
                    var extension = extVAO();
                    if (this === state.currentVAO) {
                        state.currentVAO = null;
                        extension.bindVertexArrayOES(null);
                    }
                    extension.deleteVertexArrayOES(this.vao);
                    this.vao = null;
                }
                if (this.ownsElements) {
                    this.elements.destroy();
                    this.elements = null;
                    this.ownsElements = false;
                }
                if (vaoSet[this.id]) {
                    delete vaoSet[this.id];
                    stats.vaoCount -= 1;
                }
            };
            function restoreVAO() {
                var ext = extVAO();
                if (ext) {
                    values(vaoSet).forEach(function (vao) {
                        vao.refresh();
                    });
                }
            }
            function createVAO(_attr) {
                var vao = new REGLVAO();
                stats.vaoCount += 1;
                function updateVAO(options) {
                    var attributes;
                    if (Array.isArray(options)) {
                        attributes = options;
                        if (vao.elements && vao.ownsElements) {
                            vao.elements.destroy();
                        }
                        vao.elements = null;
                        vao.ownsElements = false;
                        vao.offset = 0;
                        vao.count = 0;
                        vao.instances = -1;
                        vao.primitive = 4;
                    }
                    else {
                        check$1(typeof options === 'object', 'invalid arguments for create vao');
                        check$1('attributes' in options, 'must specify attributes for vao');
                        if (options.elements) {
                            var elements = options.elements;
                            if (vao.ownsElements) {
                                if (typeof elements === 'function' && elements._reglType === 'elements') {
                                    vao.elements.destroy();
                                    vao.ownsElements = false;
                                }
                                else {
                                    vao.elements(elements);
                                    vao.ownsElements = false;
                                }
                            }
                            else if (elementState.getElements(options.elements)) {
                                vao.elements = options.elements;
                                vao.ownsElements = false;
                            }
                            else {
                                vao.elements = elementState.create(options.elements);
                                vao.ownsElements = true;
                            }
                        }
                        else {
                            vao.elements = null;
                            vao.ownsElements = false;
                        }
                        attributes = options.attributes;
                        // set default vao
                        vao.offset = 0;
                        vao.count = -1;
                        vao.instances = -1;
                        vao.primitive = 4;
                        // copy element properties
                        if (vao.elements) {
                            vao.count = vao.elements._elements.vertCount;
                            vao.primitive = vao.elements._elements.primType;
                        }
                        if ('offset' in options) {
                            vao.offset = options.offset | 0;
                        }
                        if ('count' in options) {
                            vao.count = options.count | 0;
                        }
                        if ('instances' in options) {
                            vao.instances = options.instances | 0;
                        }
                        if ('primitive' in options) {
                            check$1(options.primitive in primTypes, 'bad primitive type: ' + options.primitive);
                            vao.primitive = primTypes[options.primitive];
                        }
                        check$1.optional(() => {
                            var keys = Object.keys(options);
                            for (var i = 0; i < keys.length; ++i) {
                                check$1(VAO_OPTIONS.indexOf(keys[i]) >= 0, 'invalid option for vao: "' + keys[i] + '" valid options are ' + VAO_OPTIONS);
                            }
                        });
                        check$1(Array.isArray(attributes), 'attributes must be an array');
                    }
                    check$1(attributes.length < NUM_ATTRIBUTES, 'too many attributes');
                    check$1(attributes.length > 0, 'must specify at least one attribute');
                    var bufUpdated = {};
                    var nattributes = vao.attributes;
                    nattributes.length = attributes.length;
                    for (var i = 0; i < attributes.length; ++i) {
                        var spec = attributes[i];
                        var rec = nattributes[i] = new AttributeRecord();
                        var data = spec.data || spec;
                        if (Array.isArray(data) || isTypedArray(data) || isNDArrayLike(data)) {
                            var buf;
                            if (vao.buffers[i]) {
                                buf = vao.buffers[i];
                                if (isTypedArray(data) && buf._buffer.byteLength >= data.byteLength) {
                                    buf.subdata(data);
                                }
                                else {
                                    buf.destroy();
                                    vao.buffers[i] = null;
                                }
                            }
                            if (!vao.buffers[i]) {
                                buf = vao.buffers[i] = bufferState.create(spec, GL_ARRAY_BUFFER$1, false, true);
                            }
                            rec.buffer = bufferState.getBuffer(buf);
                            rec.size = rec.buffer.dimension | 0;
                            rec.normalized = false;
                            rec.type = rec.buffer.dtype;
                            rec.offset = 0;
                            rec.stride = 0;
                            rec.divisor = 0;
                            rec.state = 1;
                            bufUpdated[i] = 1;
                        }
                        else if (bufferState.getBuffer(spec)) {
                            rec.buffer = bufferState.getBuffer(spec);
                            rec.size = rec.buffer.dimension | 0;
                            rec.normalized = false;
                            rec.type = rec.buffer.dtype;
                            rec.offset = 0;
                            rec.stride = 0;
                            rec.divisor = 0;
                            rec.state = 1;
                        }
                        else if (bufferState.getBuffer(spec.buffer)) {
                            rec.buffer = bufferState.getBuffer(spec.buffer);
                            rec.size = ((+spec.size) || rec.buffer.dimension) | 0;
                            rec.normalized = !!spec.normalized || false;
                            if ('type' in spec) {
                                check$1.parameter(spec.type, glTypes, 'invalid buffer type');
                                rec.type = glTypes[spec.type];
                            }
                            else {
                                rec.type = rec.buffer.dtype;
                            }
                            rec.offset = (spec.offset || 0) | 0;
                            rec.stride = (spec.stride || 0) | 0;
                            rec.divisor = (spec.divisor || 0) | 0;
                            rec.state = 1;
                            check$1(rec.size >= 1 && rec.size <= 4, 'size must be between 1 and 4');
                            check$1(rec.offset >= 0, 'invalid offset');
                            check$1(rec.stride >= 0 && rec.stride <= 255, 'stride must be between 0 and 255');
                            check$1(rec.divisor >= 0, 'divisor must be positive');
                            check$1(!rec.divisor || !!extensions.angle_instanced_arrays, 'ANGLE_instanced_arrays must be enabled to use divisor');
                        }
                        else if ('x' in spec) {
                            check$1(i > 0, 'first attribute must not be a constant');
                            rec.x = +spec.x || 0;
                            rec.y = +spec.y || 0;
                            rec.z = +spec.z || 0;
                            rec.w = +spec.w || 0;
                            rec.state = 2;
                        }
                        else {
                            check$1(false, 'invalid attribute spec for location ' + i);
                        }
                    }
                    // retire unused buffers
                    for (var j = 0; j < vao.buffers.length; ++j) {
                        if (!bufUpdated[j] && vao.buffers[j]) {
                            vao.buffers[j].destroy();
                            vao.buffers[j] = null;
                        }
                    }
                    vao.refresh();
                    return updateVAO;
                }
                updateVAO.destroy = function () {
                    for (var j = 0; j < vao.buffers.length; ++j) {
                        if (vao.buffers[j]) {
                            vao.buffers[j].destroy();
                        }
                    }
                    vao.buffers.length = 0;
                    if (vao.ownsElements) {
                        vao.elements.destroy();
                        vao.elements = null;
                        vao.ownsElements = false;
                    }
                    vao.destroy();
                };
                updateVAO._vao = vao;
                updateVAO._reglType = 'vao';
                return updateVAO(_attr);
            }
            return state;
        }
        var GL_FRAGMENT_SHADER = 35632;
        var GL_VERTEX_SHADER = 35633;
        var GL_ACTIVE_UNIFORMS = 0x8B86;
        var GL_ACTIVE_ATTRIBUTES = 0x8B89;
        function wrapShaderState(gl, stringStore, stats, config) {
            // ===================================================
            // glsl compilation and linking
            // ===================================================
            var fragShaders = {};
            var vertShaders = {};
            function ActiveInfo(name, id, location, info) {
                this.name = name;
                this.id = id;
                this.location = location;
                this.info = info;
            }
            function insertActiveInfo(list, info) {
                for (var i = 0; i < list.length; ++i) {
                    if (list[i].id === info.id) {
                        list[i].location = info.location;
                        return;
                    }
                }
                list.push(info);
            }
            function getShader(type, id, command) {
                var cache = type === GL_FRAGMENT_SHADER ? fragShaders : vertShaders;
                var shader = cache[id];
                if (!shader) {
                    var source = stringStore.str(id);
                    shader = gl.createShader(type);
                    gl.shaderSource(shader, source);
                    gl.compileShader(shader);
                    check$1.shaderError(gl, shader, source, type, command);
                    cache[id] = shader;
                }
                return shader;
            }
            // ===================================================
            // program linking
            // ===================================================
            var programCache = {};
            var programList = [];
            var PROGRAM_COUNTER = 0;
            function REGLProgram(fragId, vertId) {
                this.id = PROGRAM_COUNTER++;
                this.fragId = fragId;
                this.vertId = vertId;
                this.program = null;
                this.uniforms = [];
                this.attributes = [];
                this.refCount = 1;
                if (config.profile) {
                    this.stats = {
                        uniformsCount: 0,
                        attributesCount: 0
                    };
                }
            }
            function linkProgram(desc, command, attributeLocations) {
                var i, info;
                // -------------------------------
                // compile & link
                // -------------------------------
                var fragShader = getShader(GL_FRAGMENT_SHADER, desc.fragId);
                var vertShader = getShader(GL_VERTEX_SHADER, desc.vertId);
                var program = desc.program = gl.createProgram();
                gl.attachShader(program, fragShader);
                gl.attachShader(program, vertShader);
                if (attributeLocations) {
                    for (i = 0; i < attributeLocations.length; ++i) {
                        var binding = attributeLocations[i];
                        gl.bindAttribLocation(program, binding[0], binding[1]);
                    }
                }
                gl.linkProgram(program);
                check$1.linkError(gl, program, stringStore.str(desc.fragId), stringStore.str(desc.vertId), command);
                // -------------------------------
                // grab uniforms
                // -------------------------------
                var numUniforms = gl.getProgramParameter(program, GL_ACTIVE_UNIFORMS);
                if (config.profile) {
                    desc.stats.uniformsCount = numUniforms;
                }
                var uniforms = desc.uniforms;
                for (i = 0; i < numUniforms; ++i) {
                    info = gl.getActiveUniform(program, i);
                    if (info) {
                        if (info.size > 1) {
                            for (var j = 0; j < info.size; ++j) {
                                var name = info.name.replace('[0]', '[' + j + ']');
                                insertActiveInfo(uniforms, new ActiveInfo(name, stringStore.id(name), gl.getUniformLocation(program, name), info));
                            }
                        }
                        var uniName = info.name;
                        if (info.size > 1) {
                            uniName = uniName.replace('[0]', '');
                        }
                        insertActiveInfo(uniforms, new ActiveInfo(uniName, stringStore.id(uniName), gl.getUniformLocation(program, uniName), info));
                    }
                }
                // -------------------------------
                // grab attributes
                // -------------------------------
                var numAttributes = gl.getProgramParameter(program, GL_ACTIVE_ATTRIBUTES);
                if (config.profile) {
                    desc.stats.attributesCount = numAttributes;
                }
                var attributes = desc.attributes;
                for (i = 0; i < numAttributes; ++i) {
                    info = gl.getActiveAttrib(program, i);
                    if (info) {
                        insertActiveInfo(attributes, new ActiveInfo(info.name, stringStore.id(info.name), gl.getAttribLocation(program, info.name), info));
                    }
                }
            }
            if (config.profile) {
                stats.getMaxUniformsCount = function () {
                    var m = 0;
                    programList.forEach(function (desc) {
                        if (desc.stats.uniformsCount > m) {
                            m = desc.stats.uniformsCount;
                        }
                    });
                    return m;
                };
                stats.getMaxAttributesCount = function () {
                    var m = 0;
                    programList.forEach(function (desc) {
                        if (desc.stats.attributesCount > m) {
                            m = desc.stats.attributesCount;
                        }
                    });
                    return m;
                };
            }
            function restoreShaders() {
                fragShaders = {};
                vertShaders = {};
                for (var i = 0; i < programList.length; ++i) {
                    linkProgram(programList[i], null, programList[i].attributes.map(function (info) {
                        return [info.location, info.name];
                    }));
                }
            }
            return {
                clear: function () {
                    var deleteShader = gl.deleteShader.bind(gl);
                    values(fragShaders).forEach(deleteShader);
                    fragShaders = {};
                    values(vertShaders).forEach(deleteShader);
                    vertShaders = {};
                    programList.forEach(function (desc) {
                        gl.deleteProgram(desc.program);
                    });
                    programList.length = 0;
                    programCache = {};
                    stats.shaderCount = 0;
                },
                program: function (vertId, fragId, command, attribLocations) {
                    check$1.command(vertId >= 0, 'missing vertex shader', command);
                    check$1.command(fragId >= 0, 'missing fragment shader', command);
                    var cache = programCache[fragId];
                    if (!cache) {
                        cache = programCache[fragId] = {};
                    }
                    var prevProgram = cache[vertId];
                    if (prevProgram) {
                        prevProgram.refCount++;
                        if (!attribLocations) {
                            return prevProgram;
                        }
                    }
                    var program = new REGLProgram(fragId, vertId);
                    stats.shaderCount++;
                    linkProgram(program, command, attribLocations);
                    if (!prevProgram) {
                        cache[vertId] = program;
                    }
                    programList.push(program);
                    return extend(program, {
                        destroy: function () {
                            program.refCount--;
                            if (program.refCount <= 0) {
                                gl.deleteProgram(program.program);
                                var idx = programList.indexOf(program);
                                programList.splice(idx, 1);
                                stats.shaderCount--;
                            }
                            // no program is linked to this vert anymore
                            if (cache[program.vertId].refCount <= 0) {
                                gl.deleteShader(vertShaders[program.vertId]);
                                delete vertShaders[program.vertId];
                                delete programCache[program.fragId][program.vertId];
                            }
                            // no program is linked to this frag anymore
                            if (!Object.keys(programCache[program.fragId]).length) {
                                gl.deleteShader(fragShaders[program.fragId]);
                                delete fragShaders[program.fragId];
                                delete programCache[program.fragId];
                            }
                        }
                    });
                },
                restore: restoreShaders,
                shader: getShader,
                frag: -1,
                vert: -1
            };
        }
        var GL_RGBA$3 = 6408;
        var GL_UNSIGNED_BYTE$7 = 5121;
        var GL_PACK_ALIGNMENT = 0x0D05;
        var GL_FLOAT$7 = 0x1406; // 5126
        function wrapReadPixels(gl, framebufferState, reglPoll, context, glAttributes, extensions, limits) {
            function readPixelsImpl(input) {
                var type;
                if (framebufferState.next === null) {
                    check$1(glAttributes.preserveDrawingBuffer, 'you must create a webgl context with "preserveDrawingBuffer":true in order to read pixels from the drawing buffer');
                    type = GL_UNSIGNED_BYTE$7;
                }
                else {
                    check$1(framebufferState.next.colorAttachments[0].texture !== null, 'You cannot read from a renderbuffer');
                    type = framebufferState.next.colorAttachments[0].texture._texture.type;
                    check$1.optional(function () {
                        if (extensions.oes_texture_float) {
                            check$1(type === GL_UNSIGNED_BYTE$7 || type === GL_FLOAT$7, 'Reading from a framebuffer is only allowed for the types \'uint8\' and \'float\'');
                            if (type === GL_FLOAT$7) {
                                check$1(limits.readFloat, 'Reading \'float\' values is not permitted in your browser. For a fallback, please see: https://www.npmjs.com/package/glsl-read-float');
                            }
                        }
                        else {
                            check$1(type === GL_UNSIGNED_BYTE$7, 'Reading from a framebuffer is only allowed for the type \'uint8\'');
                        }
                    });
                }
                var x = 0;
                var y = 0;
                var width = context.framebufferWidth;
                var height = context.framebufferHeight;
                var data = null;
                if (isTypedArray(input)) {
                    data = input;
                }
                else if (input) {
                    check$1.type(input, 'object', 'invalid arguments to regl.read()');
                    x = input.x | 0;
                    y = input.y | 0;
                    check$1(x >= 0 && x < context.framebufferWidth, 'invalid x offset for regl.read');
                    check$1(y >= 0 && y < context.framebufferHeight, 'invalid y offset for regl.read');
                    width = (input.width || (context.framebufferWidth - x)) | 0;
                    height = (input.height || (context.framebufferHeight - y)) | 0;
                    data = input.data || null;
                }
                // sanity check input.data
                if (data) {
                    if (type === GL_UNSIGNED_BYTE$7) {
                        check$1(data instanceof Uint8Array, 'buffer must be \'Uint8Array\' when reading from a framebuffer of type \'uint8\'');
                    }
                    else if (type === GL_FLOAT$7) {
                        check$1(data instanceof Float32Array, 'buffer must be \'Float32Array\' when reading from a framebuffer of type \'float\'');
                    }
                }
                check$1(width > 0 && width + x <= context.framebufferWidth, 'invalid width for read pixels');
                check$1(height > 0 && height + y <= context.framebufferHeight, 'invalid height for read pixels');
                // Update WebGL state
                reglPoll();
                // Compute size
                var size = width * height * 4;
                // Allocate data
                if (!data) {
                    if (type === GL_UNSIGNED_BYTE$7) {
                        data = new Uint8Array(size);
                    }
                    else if (type === GL_FLOAT$7) {
                        data = data || new Float32Array(size);
                    }
                }
                // Type check
                check$1.isTypedArray(data, 'data buffer for regl.read() must be a typedarray');
                check$1(data.byteLength >= size, 'data buffer for regl.read() too small');
                // Run read pixels
                gl.pixelStorei(GL_PACK_ALIGNMENT, 4);
                gl.readPixels(x, y, width, height, GL_RGBA$3, type, data);
                return data;
            }
            function readPixelsFBO(options) {
                var result;
                framebufferState.setFBO({
                    framebuffer: options.framebuffer
                }, function () {
                    result = readPixelsImpl(options);
                });
                return result;
            }
            function readPixels(options) {
                if (!options || !('framebuffer' in options)) {
                    return readPixelsImpl(options);
                }
                else {
                    return readPixelsFBO(options);
                }
            }
            return readPixels;
        }
        function slice(x) {
            return Array.prototype.slice.call(x);
        }
        function join(x) {
            return slice(x).join('');
        }
        function createEnvironment() {
            // Unique variable id counter
            var varCounter = 0;
            // Linked values are passed from this scope into the generated code block
            // Calling link() passes a value into the generated scope and returns
            // the variable name which it is bound to
            var linkedNames = [];
            var linkedValues = [];
            function link(value) {
                for (var i = 0; i < linkedValues.length; ++i) {
                    if (linkedValues[i] === value) {
                        return linkedNames[i];
                    }
                }
                var name = 'g' + (varCounter++);
                linkedNames.push(name);
                linkedValues.push(value);
                return name;
            }
            // create a code block
            function block() {
                var code = [];
                function push() {
                    code.push.apply(code, slice(arguments));
                }
                var vars = [];
                function def() {
                    var name = 'v' + (varCounter++);
                    vars.push(name);
                    if (arguments.length > 0) {
                        code.push(name, '=');
                        code.push.apply(code, slice(arguments));
                        code.push(';');
                    }
                    return name;
                }
                return extend(push, {
                    def: def,
                    toString: function () {
                        return join([
                            (vars.length > 0 ? 'var ' + vars.join(',') + ';' : ''),
                            join(code)
                        ]);
                    }
                });
            }
            function scope() {
                var entry = block();
                var exit = block();
                var entryToString = entry.toString;
                var exitToString = exit.toString;
                function save(object, prop) {
                    exit(object, prop, '=', entry.def(object, prop), ';');
                }
                return extend(function () {
                    entry.apply(entry, slice(arguments));
                }, {
                    def: entry.def,
                    entry: entry,
                    exit: exit,
                    save: save,
                    set: function (object, prop, value) {
                        save(object, prop);
                        entry(object, prop, '=', value, ';');
                    },
                    toString: function () {
                        return entryToString() + exitToString();
                    }
                });
            }
            function conditional() {
                var pred = join(arguments);
                var thenBlock = scope();
                var elseBlock = scope();
                var thenToString = thenBlock.toString;
                var elseToString = elseBlock.toString;
                return extend(thenBlock, {
                    then: function () {
                        thenBlock.apply(thenBlock, slice(arguments));
                        return this;
                    },
                    else: function () {
                        elseBlock.apply(elseBlock, slice(arguments));
                        return this;
                    },
                    toString: function () {
                        var elseClause = elseToString();
                        if (elseClause) {
                            elseClause = 'else{' + elseClause + '}';
                        }
                        return join([
                            'if(', pred, '){',
                            thenToString(),
                            '}', elseClause
                        ]);
                    }
                });
            }
            // procedure list
            var globalBlock = block();
            var procedures = {};
            function proc(name, count) {
                var args = [];
                function arg() {
                    var name = 'a' + args.length;
                    args.push(name);
                    return name;
                }
                count = count || 0;
                for (var i = 0; i < count; ++i) {
                    arg();
                }
                var body = scope();
                var bodyToString = body.toString;
                var result = procedures[name] = extend(body, {
                    arg: arg,
                    toString: function () {
                        return join([
                            'function(', args.join(), '){',
                            bodyToString(),
                            '}'
                        ]);
                    }
                });
                return result;
            }
            function compile() {
                var code = ['"use strict";',
                    globalBlock,
                    'return {'];
                Object.keys(procedures).forEach(function (name) {
                    code.push('"', name, '":', procedures[name].toString(), ',');
                });
                code.push('}');
                var src = join(code)
                    .replace(/;/g, ';\n')
                    .replace(/}/g, '}\n')
                    .replace(/{/g, '{\n');
                var proc = Function.apply(null, linkedNames.concat(src));
                return proc.apply(null, linkedValues);
            }
            return {
                global: globalBlock,
                link: link,
                block: block,
                proc: proc,
                scope: scope,
                cond: conditional,
                compile: compile
            };
        }
        // "cute" names for vector components
        var CUTE_COMPONENTS = 'xyzw'.split('');
        var GL_UNSIGNED_BYTE$8 = 5121;
        var ATTRIB_STATE_POINTER = 1;
        var ATTRIB_STATE_CONSTANT = 2;
        var DYN_FUNC$1 = 0;
        var DYN_PROP$1 = 1;
        var DYN_CONTEXT$1 = 2;
        var DYN_STATE$1 = 3;
        var DYN_THUNK = 4;
        var DYN_CONSTANT$1 = 5;
        var DYN_ARRAY$1 = 6;
        var S_DITHER = 'dither';
        var S_BLEND_ENABLE = 'blend.enable';
        var S_BLEND_COLOR = 'blend.color';
        var S_BLEND_EQUATION = 'blend.equation';
        var S_BLEND_FUNC = 'blend.func';
        var S_DEPTH_ENABLE = 'depth.enable';
        var S_DEPTH_FUNC = 'depth.func';
        var S_DEPTH_RANGE = 'depth.range';
        var S_DEPTH_MASK = 'depth.mask';
        var S_COLOR_MASK = 'colorMask';
        var S_CULL_ENABLE = 'cull.enable';
        var S_CULL_FACE = 'cull.face';
        var S_FRONT_FACE = 'frontFace';
        var S_LINE_WIDTH = 'lineWidth';
        var S_POLYGON_OFFSET_ENABLE = 'polygonOffset.enable';
        var S_POLYGON_OFFSET_OFFSET = 'polygonOffset.offset';
        var S_SAMPLE_ALPHA = 'sample.alpha';
        var S_SAMPLE_ENABLE = 'sample.enable';
        var S_SAMPLE_COVERAGE = 'sample.coverage';
        var S_STENCIL_ENABLE = 'stencil.enable';
        var S_STENCIL_MASK = 'stencil.mask';
        var S_STENCIL_FUNC = 'stencil.func';
        var S_STENCIL_OPFRONT = 'stencil.opFront';
        var S_STENCIL_OPBACK = 'stencil.opBack';
        var S_SCISSOR_ENABLE = 'scissor.enable';
        var S_SCISSOR_BOX = 'scissor.box';
        var S_VIEWPORT = 'viewport';
        var S_PROFILE = 'profile';
        var S_FRAMEBUFFER = 'framebuffer';
        var S_VERT = 'vert';
        var S_FRAG = 'frag';
        var S_ELEMENTS = 'elements';
        var S_PRIMITIVE = 'primitive';
        var S_COUNT = 'count';
        var S_OFFSET = 'offset';
        var S_INSTANCES = 'instances';
        var S_VAO = 'vao';
        var SUFFIX_WIDTH = 'Width';
        var SUFFIX_HEIGHT = 'Height';
        var S_FRAMEBUFFER_WIDTH = S_FRAMEBUFFER + SUFFIX_WIDTH;
        var S_FRAMEBUFFER_HEIGHT = S_FRAMEBUFFER + SUFFIX_HEIGHT;
        var S_VIEWPORT_WIDTH = S_VIEWPORT + SUFFIX_WIDTH;
        var S_VIEWPORT_HEIGHT = S_VIEWPORT + SUFFIX_HEIGHT;
        var S_DRAWINGBUFFER = 'drawingBuffer';
        var S_DRAWINGBUFFER_WIDTH = S_DRAWINGBUFFER + SUFFIX_WIDTH;
        var S_DRAWINGBUFFER_HEIGHT = S_DRAWINGBUFFER + SUFFIX_HEIGHT;
        var NESTED_OPTIONS = [
            S_BLEND_FUNC,
            S_BLEND_EQUATION,
            S_STENCIL_FUNC,
            S_STENCIL_OPFRONT,
            S_STENCIL_OPBACK,
            S_SAMPLE_COVERAGE,
            S_VIEWPORT,
            S_SCISSOR_BOX,
            S_POLYGON_OFFSET_OFFSET
        ];
        var GL_ARRAY_BUFFER$2 = 34962;
        var GL_ELEMENT_ARRAY_BUFFER$2 = 34963;
        var GL_FRAGMENT_SHADER$1 = 35632;
        var GL_VERTEX_SHADER$1 = 35633;
        var GL_TEXTURE_2D$3 = 0x0DE1;
        var GL_TEXTURE_CUBE_MAP$2 = 0x8513;
        var GL_CULL_FACE = 0x0B44;
        var GL_BLEND = 0x0BE2;
        var GL_DITHER = 0x0BD0;
        var GL_STENCIL_TEST = 0x0B90;
        var GL_DEPTH_TEST = 0x0B71;
        var GL_SCISSOR_TEST = 0x0C11;
        var GL_POLYGON_OFFSET_FILL = 0x8037;
        var GL_SAMPLE_ALPHA_TO_COVERAGE = 0x809E;
        var GL_SAMPLE_COVERAGE = 0x80A0;
        var GL_FLOAT$8 = 5126;
        var GL_FLOAT_VEC2 = 35664;
        var GL_FLOAT_VEC3 = 35665;
        var GL_FLOAT_VEC4 = 35666;
        var GL_INT$3 = 5124;
        var GL_INT_VEC2 = 35667;
        var GL_INT_VEC3 = 35668;
        var GL_INT_VEC4 = 35669;
        var GL_BOOL = 35670;
        var GL_BOOL_VEC2 = 35671;
        var GL_BOOL_VEC3 = 35672;
        var GL_BOOL_VEC4 = 35673;
        var GL_FLOAT_MAT2 = 35674;
        var GL_FLOAT_MAT3 = 35675;
        var GL_FLOAT_MAT4 = 35676;
        var GL_SAMPLER_2D = 35678;
        var GL_SAMPLER_CUBE = 35680;
        var GL_TRIANGLES$1 = 4;
        var GL_FRONT = 1028;
        var GL_BACK = 1029;
        var GL_CW = 0x0900;
        var GL_CCW = 0x0901;
        var GL_MIN_EXT = 0x8007;
        var GL_MAX_EXT = 0x8008;
        var GL_ALWAYS = 519;
        var GL_KEEP = 7680;
        var GL_ZERO = 0;
        var GL_ONE = 1;
        var GL_FUNC_ADD = 0x8006;
        var GL_LESS = 513;
        var GL_FRAMEBUFFER$2 = 0x8D40;
        var GL_COLOR_ATTACHMENT0$2 = 0x8CE0;
        var blendFuncs = {
            '0': 0,
            '1': 1,
            'zero': 0,
            'one': 1,
            'src color': 768,
            'one minus src color': 769,
            'src alpha': 770,
            'one minus src alpha': 771,
            'dst color': 774,
            'one minus dst color': 775,
            'dst alpha': 772,
            'one minus dst alpha': 773,
            'constant color': 32769,
            'one minus constant color': 32770,
            'constant alpha': 32771,
            'one minus constant alpha': 32772,
            'src alpha saturate': 776
        };
        // There are invalid values for srcRGB and dstRGB. See:
        // https://www.khronos.org/registry/webgl/specs/1.0/#6.13
        // https://github.com/KhronosGroup/WebGL/blob/0d3201f5f7ec3c0060bc1f04077461541f1987b9/conformance-suites/1.0.3/conformance/misc/webgl-specific.html#L56
        var invalidBlendCombinations = [
            'constant color, constant alpha',
            'one minus constant color, constant alpha',
            'constant color, one minus constant alpha',
            'one minus constant color, one minus constant alpha',
            'constant alpha, constant color',
            'constant alpha, one minus constant color',
            'one minus constant alpha, constant color',
            'one minus constant alpha, one minus constant color'
        ];
        var compareFuncs = {
            'never': 512,
            'less': 513,
            '<': 513,
            'equal': 514,
            '=': 514,
            '==': 514,
            '===': 514,
            'lequal': 515,
            '<=': 515,
            'greater': 516,
            '>': 516,
            'notequal': 517,
            '!=': 517,
            '!==': 517,
            'gequal': 518,
            '>=': 518,
            'always': 519
        };
        var stencilOps = {
            '0': 0,
            'zero': 0,
            'keep': 7680,
            'replace': 7681,
            'increment': 7682,
            'decrement': 7683,
            'increment wrap': 34055,
            'decrement wrap': 34056,
            'invert': 5386
        };
        var shaderType = {
            'frag': GL_FRAGMENT_SHADER$1,
            'vert': GL_VERTEX_SHADER$1
        };
        var orientationType = {
            'cw': GL_CW,
            'ccw': GL_CCW
        };
        function isBufferArgs(x) {
            return Array.isArray(x) ||
                isTypedArray(x) ||
                isNDArrayLike(x);
        }
        // Make sure viewport is processed first
        function sortState(state) {
            return state.sort(function (a, b) {
                if (a === S_VIEWPORT) {
                    return -1;
                }
                else if (b === S_VIEWPORT) {
                    return 1;
                }
                return (a < b) ? -1 : 1;
            });
        }
        function Declaration(thisDep, contextDep, propDep, append) {
            this.thisDep = thisDep;
            this.contextDep = contextDep;
            this.propDep = propDep;
            this.append = append;
        }
        function isStatic(decl) {
            return decl && !(decl.thisDep || decl.contextDep || decl.propDep);
        }
        function createStaticDecl(append) {
            return new Declaration(false, false, false, append);
        }
        function createDynamicDecl(dyn, append) {
            var type = dyn.type;
            if (type === DYN_FUNC$1) {
                var numArgs = dyn.data.length;
                return new Declaration(true, numArgs >= 1, numArgs >= 2, append);
            }
            else if (type === DYN_THUNK) {
                var data = dyn.data;
                return new Declaration(data.thisDep, data.contextDep, data.propDep, append);
            }
            else if (type === DYN_CONSTANT$1) {
                return new Declaration(false, false, false, append);
            }
            else if (type === DYN_ARRAY$1) {
                var thisDep = false;
                var contextDep = false;
                var propDep = false;
                for (var i = 0; i < dyn.data.length; ++i) {
                    var subDyn = dyn.data[i];
                    if (subDyn.type === DYN_PROP$1) {
                        propDep = true;
                    }
                    else if (subDyn.type === DYN_CONTEXT$1) {
                        contextDep = true;
                    }
                    else if (subDyn.type === DYN_STATE$1) {
                        thisDep = true;
                    }
                    else if (subDyn.type === DYN_FUNC$1) {
                        thisDep = true;
                        var subArgs = subDyn.data;
                        if (subArgs >= 1) {
                            contextDep = true;
                        }
                        if (subArgs >= 2) {
                            propDep = true;
                        }
                    }
                    else if (subDyn.type === DYN_THUNK) {
                        thisDep = thisDep || subDyn.data.thisDep;
                        contextDep = contextDep || subDyn.data.contextDep;
                        propDep = propDep || subDyn.data.propDep;
                    }
                }
                return new Declaration(thisDep, contextDep, propDep, append);
            }
            else {
                return new Declaration(type === DYN_STATE$1, type === DYN_CONTEXT$1, type === DYN_PROP$1, append);
            }
        }
        var SCOPE_DECL = new Declaration(false, false, false, function () { });
        function reglCore(gl, stringStore, extensions, limits, bufferState, elementState, textureState, framebufferState, uniformState, attributeState, shaderState, drawState, contextState, timer, config) {
            var AttributeRecord = attributeState.Record;
            var blendEquations = {
                'add': 32774,
                'subtract': 32778,
                'reverse subtract': 32779
            };
            if (extensions.ext_blend_minmax) {
                blendEquations.min = GL_MIN_EXT;
                blendEquations.max = GL_MAX_EXT;
            }
            var extInstancing = extensions.angle_instanced_arrays;
            var extDrawBuffers = extensions.webgl_draw_buffers;
            var extVertexArrays = extensions.oes_vertex_array_object;
            // ===================================================
            // ===================================================
            // WEBGL STATE
            // ===================================================
            // ===================================================
            var currentState = {
                dirty: true,
                profile: config.profile
            };
            var nextState = {};
            var GL_STATE_NAMES = [];
            var GL_FLAGS = {};
            var GL_VARIABLES = {};
            function propName(name) {
                return name.replace('.', '_');
            }
            function stateFlag(sname, cap, init) {
                var name = propName(sname);
                GL_STATE_NAMES.push(sname);
                nextState[name] = currentState[name] = !!init;
                GL_FLAGS[name] = cap;
            }
            function stateVariable(sname, func, init) {
                var name = propName(sname);
                GL_STATE_NAMES.push(sname);
                if (Array.isArray(init)) {
                    currentState[name] = init.slice();
                    nextState[name] = init.slice();
                }
                else {
                    currentState[name] = nextState[name] = init;
                }
                GL_VARIABLES[name] = func;
            }
            // Dithering
            stateFlag(S_DITHER, GL_DITHER);
            // Blending
            stateFlag(S_BLEND_ENABLE, GL_BLEND);
            stateVariable(S_BLEND_COLOR, 'blendColor', [0, 0, 0, 0]);
            stateVariable(S_BLEND_EQUATION, 'blendEquationSeparate', [GL_FUNC_ADD, GL_FUNC_ADD]);
            stateVariable(S_BLEND_FUNC, 'blendFuncSeparate', [GL_ONE, GL_ZERO, GL_ONE, GL_ZERO]);
            // Depth
            stateFlag(S_DEPTH_ENABLE, GL_DEPTH_TEST, true);
            stateVariable(S_DEPTH_FUNC, 'depthFunc', GL_LESS);
            stateVariable(S_DEPTH_RANGE, 'depthRange', [0, 1]);
            stateVariable(S_DEPTH_MASK, 'depthMask', true);
            // Color mask
            stateVariable(S_COLOR_MASK, S_COLOR_MASK, [true, true, true, true]);
            // Face culling
            stateFlag(S_CULL_ENABLE, GL_CULL_FACE);
            stateVariable(S_CULL_FACE, 'cullFace', GL_BACK);
            // Front face orientation
            stateVariable(S_FRONT_FACE, S_FRONT_FACE, GL_CCW);
            // Line width
            stateVariable(S_LINE_WIDTH, S_LINE_WIDTH, 1);
            // Polygon offset
            stateFlag(S_POLYGON_OFFSET_ENABLE, GL_POLYGON_OFFSET_FILL);
            stateVariable(S_POLYGON_OFFSET_OFFSET, 'polygonOffset', [0, 0]);
            // Sample coverage
            stateFlag(S_SAMPLE_ALPHA, GL_SAMPLE_ALPHA_TO_COVERAGE);
            stateFlag(S_SAMPLE_ENABLE, GL_SAMPLE_COVERAGE);
            stateVariable(S_SAMPLE_COVERAGE, 'sampleCoverage', [1, false]);
            // Stencil
            stateFlag(S_STENCIL_ENABLE, GL_STENCIL_TEST);
            stateVariable(S_STENCIL_MASK, 'stencilMask', -1);
            stateVariable(S_STENCIL_FUNC, 'stencilFunc', [GL_ALWAYS, 0, -1]);
            stateVariable(S_STENCIL_OPFRONT, 'stencilOpSeparate', [GL_FRONT, GL_KEEP, GL_KEEP, GL_KEEP]);
            stateVariable(S_STENCIL_OPBACK, 'stencilOpSeparate', [GL_BACK, GL_KEEP, GL_KEEP, GL_KEEP]);
            // Scissor
            stateFlag(S_SCISSOR_ENABLE, GL_SCISSOR_TEST);
            stateVariable(S_SCISSOR_BOX, 'scissor', [0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight]);
            // Viewport
            stateVariable(S_VIEWPORT, S_VIEWPORT, [0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight]);
            // ===================================================
            // ===================================================
            // ENVIRONMENT
            // ===================================================
            // ===================================================
            var sharedState = {
                gl: gl,
                context: contextState,
                strings: stringStore,
                next: nextState,
                current: currentState,
                draw: drawState,
                elements: elementState,
                buffer: bufferState,
                shader: shaderState,
                attributes: attributeState.state,
                vao: attributeState,
                uniforms: uniformState,
                framebuffer: framebufferState,
                extensions: extensions,
                timer: timer,
                isBufferArgs: isBufferArgs
            };
            var sharedConstants = {
                primTypes: primTypes,
                compareFuncs: compareFuncs,
                blendFuncs: blendFuncs,
                blendEquations: blendEquations,
                stencilOps: stencilOps,
                glTypes: glTypes,
                orientationType: orientationType
            };
            check$1.optional(function () {
                sharedState.isArrayLike = isArrayLike;
            });
            if (extDrawBuffers) {
                sharedConstants.backBuffer = [GL_BACK];
                sharedConstants.drawBuffer = loop(limits.maxDrawbuffers, function (i) {
                    if (i === 0) {
                        return [0];
                    }
                    return loop(i, function (j) {
                        return GL_COLOR_ATTACHMENT0$2 + j;
                    });
                });
            }
            var drawCallCounter = 0;
            function createREGLEnvironment() {
                var env = createEnvironment();
                var link = env.link;
                var global = env.global;
                env.id = drawCallCounter++;
                env.batchId = '0';
                // link shared state
                var SHARED = link(sharedState);
                var shared = env.shared = {
                    props: 'a0'
                };
                Object.keys(sharedState).forEach(function (prop) {
                    shared[prop] = global.def(SHARED, '.', prop);
                });
                // Inject runtime assertion stuff for debug builds
                check$1.optional(function () {
                    env.CHECK = link(check$1);
                    env.commandStr = check$1.guessCommand();
                    env.command = link(env.commandStr);
                    env.assert = function (block, pred, message) {
                        block('if(!(', pred, '))', this.CHECK, '.commandRaise(', link(message), ',', this.command, ');');
                    };
                    sharedConstants.invalidBlendCombinations = invalidBlendCombinations;
                });
                // Copy GL state variables over
                var nextVars = env.next = {};
                var currentVars = env.current = {};
                Object.keys(GL_VARIABLES).forEach(function (variable) {
                    if (Array.isArray(currentState[variable])) {
                        nextVars[variable] = global.def(shared.next, '.', variable);
                        currentVars[variable] = global.def(shared.current, '.', variable);
                    }
                });
                // Initialize shared constants
                var constants = env.constants = {};
                Object.keys(sharedConstants).forEach(function (name) {
                    constants[name] = global.def(JSON.stringify(sharedConstants[name]));
                });
                // Helper function for calling a block
                env.invoke = function (block, x) {
                    switch (x.type) {
                        case DYN_FUNC$1:
                            var argList = [
                                'this',
                                shared.context,
                                shared.props,
                                env.batchId
                            ];
                            return block.def(link(x.data), '.call(', argList.slice(0, Math.max(x.data.length + 1, 4)), ')');
                        case DYN_PROP$1:
                            return block.def(shared.props, x.data);
                        case DYN_CONTEXT$1:
                            return block.def(shared.context, x.data);
                        case DYN_STATE$1:
                            return block.def('this', x.data);
                        case DYN_THUNK:
                            x.data.append(env, block);
                            return x.data.ref;
                        case DYN_CONSTANT$1:
                            return x.data.toString();
                        case DYN_ARRAY$1:
                            return x.data.map(function (y) {
                                return env.invoke(block, y);
                            });
                    }
                };
                env.attribCache = {};
                var scopeAttribs = {};
                env.scopeAttrib = function (name) {
                    var id = stringStore.id(name);
                    if (id in scopeAttribs) {
                        return scopeAttribs[id];
                    }
                    var binding = attributeState.scope[id];
                    if (!binding) {
                        binding = attributeState.scope[id] = new AttributeRecord();
                    }
                    var result = scopeAttribs[id] = link(binding);
                    return result;
                };
                return env;
            }
            // ===================================================
            // ===================================================
            // PARSING
            // ===================================================
            // ===================================================
            function parseProfile(options) {
                var staticOptions = options.static;
                var dynamicOptions = options.dynamic;
                var profileEnable;
                if (S_PROFILE in staticOptions) {
                    var value = !!staticOptions[S_PROFILE];
                    profileEnable = createStaticDecl(function (env, scope) {
                        return value;
                    });
                    profileEnable.enable = value;
                }
                else if (S_PROFILE in dynamicOptions) {
                    var dyn = dynamicOptions[S_PROFILE];
                    profileEnable = createDynamicDecl(dyn, function (env, scope) {
                        return env.invoke(scope, dyn);
                    });
                }
                return profileEnable;
            }
            function parseFramebuffer(options, env) {
                var staticOptions = options.static;
                var dynamicOptions = options.dynamic;
                if (S_FRAMEBUFFER in staticOptions) {
                    var framebuffer = staticOptions[S_FRAMEBUFFER];
                    if (framebuffer) {
                        framebuffer = framebufferState.getFramebuffer(framebuffer);
                        check$1.command(framebuffer, 'invalid framebuffer object');
                        return createStaticDecl(function (env, block) {
                            var FRAMEBUFFER = env.link(framebuffer);
                            var shared = env.shared;
                            block.set(shared.framebuffer, '.next', FRAMEBUFFER);
                            var CONTEXT = shared.context;
                            block.set(CONTEXT, '.' + S_FRAMEBUFFER_WIDTH, FRAMEBUFFER + '.width');
                            block.set(CONTEXT, '.' + S_FRAMEBUFFER_HEIGHT, FRAMEBUFFER + '.height');
                            return FRAMEBUFFER;
                        });
                    }
                    else {
                        return createStaticDecl(function (env, scope) {
                            var shared = env.shared;
                            scope.set(shared.framebuffer, '.next', 'null');
                            var CONTEXT = shared.context;
                            scope.set(CONTEXT, '.' + S_FRAMEBUFFER_WIDTH, CONTEXT + '.' + S_DRAWINGBUFFER_WIDTH);
                            scope.set(CONTEXT, '.' + S_FRAMEBUFFER_HEIGHT, CONTEXT + '.' + S_DRAWINGBUFFER_HEIGHT);
                            return 'null';
                        });
                    }
                }
                else if (S_FRAMEBUFFER in dynamicOptions) {
                    var dyn = dynamicOptions[S_FRAMEBUFFER];
                    return createDynamicDecl(dyn, function (env, scope) {
                        var FRAMEBUFFER_FUNC = env.invoke(scope, dyn);
                        var shared = env.shared;
                        var FRAMEBUFFER_STATE = shared.framebuffer;
                        var FRAMEBUFFER = scope.def(FRAMEBUFFER_STATE, '.getFramebuffer(', FRAMEBUFFER_FUNC, ')');
                        check$1.optional(function () {
                            env.assert(scope, '!' + FRAMEBUFFER_FUNC + '||' + FRAMEBUFFER, 'invalid framebuffer object');
                        });
                        scope.set(FRAMEBUFFER_STATE, '.next', FRAMEBUFFER);
                        var CONTEXT = shared.context;
                        scope.set(CONTEXT, '.' + S_FRAMEBUFFER_WIDTH, FRAMEBUFFER + '?' + FRAMEBUFFER + '.width:' +
                            CONTEXT + '.' + S_DRAWINGBUFFER_WIDTH);
                        scope.set(CONTEXT, '.' + S_FRAMEBUFFER_HEIGHT, FRAMEBUFFER +
                            '?' + FRAMEBUFFER + '.height:' +
                            CONTEXT + '.' + S_DRAWINGBUFFER_HEIGHT);
                        return FRAMEBUFFER;
                    });
                }
                else {
                    return null;
                }
            }
            function parseViewportScissor(options, framebuffer, env) {
                var staticOptions = options.static;
                var dynamicOptions = options.dynamic;
                function parseBox(param) {
                    if (param in staticOptions) {
                        var box = staticOptions[param];
                        check$1.commandType(box, 'object', 'invalid ' + param, env.commandStr);
                        var isStatic = true;
                        var x = box.x | 0;
                        var y = box.y | 0;
                        var w, h;
                        if ('width' in box) {
                            w = box.width | 0;
                            check$1.command(w >= 0, 'invalid ' + param, env.commandStr);
                        }
                        else {
                            isStatic = false;
                        }
                        if ('height' in box) {
                            h = box.height | 0;
                            check$1.command(h >= 0, 'invalid ' + param, env.commandStr);
                        }
                        else {
                            isStatic = false;
                        }
                        return new Declaration(!isStatic && framebuffer && framebuffer.thisDep, !isStatic && framebuffer && framebuffer.contextDep, !isStatic && framebuffer && framebuffer.propDep, function (env, scope) {
                            var CONTEXT = env.shared.context;
                            var BOX_W = w;
                            if (!('width' in box)) {
                                BOX_W = scope.def(CONTEXT, '.', S_FRAMEBUFFER_WIDTH, '-', x);
                            }
                            var BOX_H = h;
                            if (!('height' in box)) {
                                BOX_H = scope.def(CONTEXT, '.', S_FRAMEBUFFER_HEIGHT, '-', y);
                            }
                            return [x, y, BOX_W, BOX_H];
                        });
                    }
                    else if (param in dynamicOptions) {
                        var dynBox = dynamicOptions[param];
                        var result = createDynamicDecl(dynBox, function (env, scope) {
                            var BOX = env.invoke(scope, dynBox);
                            check$1.optional(function () {
                                env.assert(scope, BOX + '&&typeof ' + BOX + '==="object"', 'invalid ' + param);
                            });
                            var CONTEXT = env.shared.context;
                            var BOX_X = scope.def(BOX, '.x|0');
                            var BOX_Y = scope.def(BOX, '.y|0');
                            var BOX_W = scope.def('"width" in ', BOX, '?', BOX, '.width|0:', '(', CONTEXT, '.', S_FRAMEBUFFER_WIDTH, '-', BOX_X, ')');
                            var BOX_H = scope.def('"height" in ', BOX, '?', BOX, '.height|0:', '(', CONTEXT, '.', S_FRAMEBUFFER_HEIGHT, '-', BOX_Y, ')');
                            check$1.optional(function () {
                                env.assert(scope, BOX_W + '>=0&&' +
                                    BOX_H + '>=0', 'invalid ' + param);
                            });
                            return [BOX_X, BOX_Y, BOX_W, BOX_H];
                        });
                        if (framebuffer) {
                            result.thisDep = result.thisDep || framebuffer.thisDep;
                            result.contextDep = result.contextDep || framebuffer.contextDep;
                            result.propDep = result.propDep || framebuffer.propDep;
                        }
                        return result;
                    }
                    else if (framebuffer) {
                        return new Declaration(framebuffer.thisDep, framebuffer.contextDep, framebuffer.propDep, function (env, scope) {
                            var CONTEXT = env.shared.context;
                            return [
                                0, 0,
                                scope.def(CONTEXT, '.', S_FRAMEBUFFER_WIDTH),
                                scope.def(CONTEXT, '.', S_FRAMEBUFFER_HEIGHT)
                            ];
                        });
                    }
                    else {
                        return null;
                    }
                }
                var viewport = parseBox(S_VIEWPORT);
                if (viewport) {
                    var prevViewport = viewport;
                    viewport = new Declaration(viewport.thisDep, viewport.contextDep, viewport.propDep, function (env, scope) {
                        var VIEWPORT = prevViewport.append(env, scope);
                        var CONTEXT = env.shared.context;
                        scope.set(CONTEXT, '.' + S_VIEWPORT_WIDTH, VIEWPORT[2]);
                        scope.set(CONTEXT, '.' + S_VIEWPORT_HEIGHT, VIEWPORT[3]);
                        return VIEWPORT;
                    });
                }
                return {
                    viewport: viewport,
                    scissor_box: parseBox(S_SCISSOR_BOX)
                };
            }
            function parseAttribLocations(options, attributes) {
                var staticOptions = options.static;
                var staticProgram = typeof staticOptions[S_FRAG] === 'string' &&
                    typeof staticOptions[S_VERT] === 'string';
                if (staticProgram) {
                    if (Object.keys(attributes.dynamic).length > 0) {
                        return null;
                    }
                    var staticAttributes = attributes.static;
                    var sAttributes = Object.keys(staticAttributes);
                    if (sAttributes.length > 0 && typeof staticAttributes[sAttributes[0]] === 'number') {
                        var bindings = [];
                        for (var i = 0; i < sAttributes.length; ++i) {
                            check$1(typeof staticAttributes[sAttributes[i]] === 'number', 'must specify all vertex attribute locations when using vaos');
                            bindings.push([staticAttributes[sAttributes[i]] | 0, sAttributes[i]]);
                        }
                        return bindings;
                    }
                }
                return null;
            }
            function parseProgram(options, env, attribLocations) {
                var staticOptions = options.static;
                var dynamicOptions = options.dynamic;
                function parseShader(name) {
                    if (name in staticOptions) {
                        var id = stringStore.id(staticOptions[name]);
                        check$1.optional(function () {
                            shaderState.shader(shaderType[name], id, check$1.guessCommand());
                        });
                        var result = createStaticDecl(function () {
                            return id;
                        });
                        result.id = id;
                        return result;
                    }
                    else if (name in dynamicOptions) {
                        var dyn = dynamicOptions[name];
                        return createDynamicDecl(dyn, function (env, scope) {
                            var str = env.invoke(scope, dyn);
                            var id = scope.def(env.shared.strings, '.id(', str, ')');
                            check$1.optional(function () {
                                scope(env.shared.shader, '.shader(', shaderType[name], ',', id, ',', env.command, ');');
                            });
                            return id;
                        });
                    }
                    return null;
                }
                var frag = parseShader(S_FRAG);
                var vert = parseShader(S_VERT);
                var program = null;
                var progVar;
                if (isStatic(frag) && isStatic(vert)) {
                    program = shaderState.program(vert.id, frag.id, null, attribLocations);
                    progVar = createStaticDecl(function (env, scope) {
                        return env.link(program);
                    });
                }
                else {
                    progVar = new Declaration((frag && frag.thisDep) || (vert && vert.thisDep), (frag && frag.contextDep) || (vert && vert.contextDep), (frag && frag.propDep) || (vert && vert.propDep), function (env, scope) {
                        var SHADER_STATE = env.shared.shader;
                        var fragId;
                        if (frag) {
                            fragId = frag.append(env, scope);
                        }
                        else {
                            fragId = scope.def(SHADER_STATE, '.', S_FRAG);
                        }
                        var vertId;
                        if (vert) {
                            vertId = vert.append(env, scope);
                        }
                        else {
                            vertId = scope.def(SHADER_STATE, '.', S_VERT);
                        }
                        var progDef = SHADER_STATE + '.program(' + vertId + ',' + fragId;
                        check$1.optional(function () {
                            progDef += ',' + env.command;
                        });
                        return scope.def(progDef + ')');
                    });
                }
                return {
                    frag: frag,
                    vert: vert,
                    progVar: progVar,
                    program: program
                };
            }
            function parseDraw(options, env) {
                var staticOptions = options.static;
                var dynamicOptions = options.dynamic;
                // TODO: should use VAO to get default values for offset properties
                // should move vao parse into here and out of the old stuff
                var staticDraw = {};
                var vaoActive = false;
                function parseVAO() {
                    if (S_VAO in staticOptions) {
                        var vao = staticOptions[S_VAO];
                        if (vao !== null && attributeState.getVAO(vao) === null) {
                            vao = attributeState.createVAO(vao);
                        }
                        vaoActive = true;
                        staticDraw.vao = vao;
                        return createStaticDecl(function (env) {
                            var vaoRef = attributeState.getVAO(vao);
                            if (vaoRef) {
                                return env.link(vaoRef);
                            }
                            else {
                                return 'null';
                            }
                        });
                    }
                    else if (S_VAO in dynamicOptions) {
                        vaoActive = true;
                        var dyn = dynamicOptions[S_VAO];
                        return createDynamicDecl(dyn, function (env, scope) {
                            var vaoRef = env.invoke(scope, dyn);
                            return scope.def(env.shared.vao + '.getVAO(' + vaoRef + ')');
                        });
                    }
                    return null;
                }
                var vao = parseVAO();
                var elementsActive = false;
                function parseElements() {
                    if (S_ELEMENTS in staticOptions) {
                        var elements = staticOptions[S_ELEMENTS];
                        staticDraw.elements = elements;
                        if (isBufferArgs(elements)) {
                            var e = staticDraw.elements = elementState.create(elements, true);
                            elements = elementState.getElements(e);
                            elementsActive = true;
                        }
                        else if (elements) {
                            elements = elementState.getElements(elements);
                            elementsActive = true;
                            check$1.command(elements, 'invalid elements', env.commandStr);
                        }
                        var result = createStaticDecl(function (env, scope) {
                            if (elements) {
                                var result = env.link(elements);
                                env.ELEMENTS = result;
                                return result;
                            }
                            env.ELEMENTS = null;
                            return null;
                        });
                        result.value = elements;
                        return result;
                    }
                    else if (S_ELEMENTS in dynamicOptions) {
                        elementsActive = true;
                        var dyn = dynamicOptions[S_ELEMENTS];
                        return createDynamicDecl(dyn, function (env, scope) {
                            var shared = env.shared;
                            var IS_BUFFER_ARGS = shared.isBufferArgs;
                            var ELEMENT_STATE = shared.elements;
                            var elementDefn = env.invoke(scope, dyn);
                            var elements = scope.def('null');
                            var elementStream = scope.def(IS_BUFFER_ARGS, '(', elementDefn, ')');
                            var ifte = env.cond(elementStream)
                                .then(elements, '=', ELEMENT_STATE, '.createStream(', elementDefn, ');')
                                .else(elements, '=', ELEMENT_STATE, '.getElements(', elementDefn, ');');
                            check$1.optional(function () {
                                env.assert(ifte.else, '!' + elementDefn + '||' + elements, 'invalid elements');
                            });
                            scope.entry(ifte);
                            scope.exit(env.cond(elementStream)
                                .then(ELEMENT_STATE, '.destroyStream(', elements, ');'));
                            env.ELEMENTS = elements;
                            return elements;
                        });
                    }
                    else if (vaoActive) {
                        return new Declaration(vao.thisDep, vao.contextDep, vao.propDep, function (env, scope) {
                            return scope.def(env.shared.vao + '.currentVAO?' + env.shared.elements + '.getElements(' + env.shared.vao + '.currentVAO.elements):null');
                        });
                    }
                    return null;
                }
                var elements = parseElements();
                function parsePrimitive() {
                    if (S_PRIMITIVE in staticOptions) {
                        var primitive = staticOptions[S_PRIMITIVE];
                        staticDraw.primitive = primitive;
                        check$1.commandParameter(primitive, primTypes, 'invalid primitve', env.commandStr);
                        return createStaticDecl(function (env, scope) {
                            return primTypes[primitive];
                        });
                    }
                    else if (S_PRIMITIVE in dynamicOptions) {
                        var dynPrimitive = dynamicOptions[S_PRIMITIVE];
                        return createDynamicDecl(dynPrimitive, function (env, scope) {
                            var PRIM_TYPES = env.constants.primTypes;
                            var prim = env.invoke(scope, dynPrimitive);
                            check$1.optional(function () {
                                env.assert(scope, prim + ' in ' + PRIM_TYPES, 'invalid primitive, must be one of ' + Object.keys(primTypes));
                            });
                            return scope.def(PRIM_TYPES, '[', prim, ']');
                        });
                    }
                    else if (elementsActive) {
                        if (isStatic(elements)) {
                            if (elements.value) {
                                return createStaticDecl(function (env, scope) {
                                    return scope.def(env.ELEMENTS, '.primType');
                                });
                            }
                            else {
                                return createStaticDecl(function () {
                                    return GL_TRIANGLES$1;
                                });
                            }
                        }
                        else {
                            return new Declaration(elements.thisDep, elements.contextDep, elements.propDep, function (env, scope) {
                                var elements = env.ELEMENTS;
                                return scope.def(elements, '?', elements, '.primType:', GL_TRIANGLES$1);
                            });
                        }
                    }
                    else if (vaoActive) {
                        return new Declaration(vao.thisDep, vao.contextDep, vao.propDep, function (env, scope) {
                            return scope.def(env.shared.vao + '.currentVAO?' + env.shared.vao + '.currentVAO.primitive:' + GL_TRIANGLES$1);
                        });
                    }
                    return null;
                }
                function parseParam(param, isOffset) {
                    if (param in staticOptions) {
                        var value = staticOptions[param] | 0;
                        if (isOffset) {
                            staticDraw.offset = value;
                        }
                        else {
                            staticDraw.instances = value;
                        }
                        check$1.command(!isOffset || value >= 0, 'invalid ' + param, env.commandStr);
                        return createStaticDecl(function (env, scope) {
                            if (isOffset) {
                                env.OFFSET = value;
                            }
                            return value;
                        });
                    }
                    else if (param in dynamicOptions) {
                        var dynValue = dynamicOptions[param];
                        return createDynamicDecl(dynValue, function (env, scope) {
                            var result = env.invoke(scope, dynValue);
                            if (isOffset) {
                                env.OFFSET = result;
                                check$1.optional(function () {
                                    env.assert(scope, result + '>=0', 'invalid ' + param);
                                });
                            }
                            return result;
                        });
                    }
                    else if (isOffset) {
                        if (elementsActive) {
                            return createStaticDecl(function (env, scope) {
                                env.OFFSET = 0;
                                return 0;
                            });
                        }
                        else if (vaoActive) {
                            return new Declaration(vao.thisDep, vao.contextDep, vao.propDep, function (env, scope) {
                                return scope.def(env.shared.vao + '.currentVAO?' + env.shared.vao + '.currentVAO.offset:0');
                            });
                        }
                    }
                    else if (vaoActive) {
                        return new Declaration(vao.thisDep, vao.contextDep, vao.propDep, function (env, scope) {
                            return scope.def(env.shared.vao + '.currentVAO?' + env.shared.vao + '.currentVAO.instances:-1');
                        });
                    }
                    return null;
                }
                var OFFSET = parseParam(S_OFFSET, true);
                function parseVertCount() {
                    if (S_COUNT in staticOptions) {
                        var count = staticOptions[S_COUNT] | 0;
                        staticDraw.count = count;
                        check$1.command(typeof count === 'number' && count >= 0, 'invalid vertex count', env.commandStr);
                        return createStaticDecl(function () {
                            return count;
                        });
                    }
                    else if (S_COUNT in dynamicOptions) {
                        var dynCount = dynamicOptions[S_COUNT];
                        return createDynamicDecl(dynCount, function (env, scope) {
                            var result = env.invoke(scope, dynCount);
                            check$1.optional(function () {
                                env.assert(scope, 'typeof ' + result + '==="number"&&' +
                                    result + '>=0&&' +
                                    result + '===(' + result + '|0)', 'invalid vertex count');
                            });
                            return result;
                        });
                    }
                    else if (elementsActive) {
                        if (isStatic(elements)) {
                            if (elements) {
                                if (OFFSET) {
                                    return new Declaration(OFFSET.thisDep, OFFSET.contextDep, OFFSET.propDep, function (env, scope) {
                                        var result = scope.def(env.ELEMENTS, '.vertCount-', env.OFFSET);
                                        check$1.optional(function () {
                                            env.assert(scope, result + '>=0', 'invalid vertex offset/element buffer too small');
                                        });
                                        return result;
                                    });
                                }
                                else {
                                    return createStaticDecl(function (env, scope) {
                                        return scope.def(env.ELEMENTS, '.vertCount');
                                    });
                                }
                            }
                            else {
                                var result = createStaticDecl(function () {
                                    return -1;
                                });
                                check$1.optional(function () {
                                    result.MISSING = true;
                                });
                                return result;
                            }
                        }
                        else {
                            var variable = new Declaration(elements.thisDep || OFFSET.thisDep, elements.contextDep || OFFSET.contextDep, elements.propDep || OFFSET.propDep, function (env, scope) {
                                var elements = env.ELEMENTS;
                                if (env.OFFSET) {
                                    return scope.def(elements, '?', elements, '.vertCount-', env.OFFSET, ':-1');
                                }
                                return scope.def(elements, '?', elements, '.vertCount:-1');
                            });
                            check$1.optional(function () {
                                variable.DYNAMIC = true;
                            });
                            return variable;
                        }
                    }
                    else if (vaoActive) {
                        var countVariable = new Declaration(vao.thisDep, vao.contextDep, vao.propDep, function (env, scope) {
                            return scope.def(env.shared.vao, '.currentVAO?', env.shared.vao, '.currentVAO.count:-1');
                        });
                        return countVariable;
                    }
                    return null;
                }
                var primitive = parsePrimitive();
                var count = parseVertCount();
                var instances = parseParam(S_INSTANCES, false);
                return {
                    elements: elements,
                    primitive: primitive,
                    count: count,
                    instances: instances,
                    offset: OFFSET,
                    vao: vao,
                    vaoActive: vaoActive,
                    elementsActive: elementsActive,
                    // static draw props
                    static: staticDraw
                };
            }
            function parseGLState(options, env) {
                var staticOptions = options.static;
                var dynamicOptions = options.dynamic;
                var STATE = {};
                GL_STATE_NAMES.forEach(function (prop) {
                    var param = propName(prop);
                    function parseParam(parseStatic, parseDynamic) {
                        if (prop in staticOptions) {
                            var value = parseStatic(staticOptions[prop]);
                            STATE[param] = createStaticDecl(function () {
                                return value;
                            });
                        }
                        else if (prop in dynamicOptions) {
                            var dyn = dynamicOptions[prop];
                            STATE[param] = createDynamicDecl(dyn, function (env, scope) {
                                return parseDynamic(env, scope, env.invoke(scope, dyn));
                            });
                        }
                    }
                    switch (prop) {
                        case S_CULL_ENABLE:
                        case S_BLEND_ENABLE:
                        case S_DITHER:
                        case S_STENCIL_ENABLE:
                        case S_DEPTH_ENABLE:
                        case S_SCISSOR_ENABLE:
                        case S_POLYGON_OFFSET_ENABLE:
                        case S_SAMPLE_ALPHA:
                        case S_SAMPLE_ENABLE:
                        case S_DEPTH_MASK:
                            return parseParam(function (value) {
                                check$1.commandType(value, 'boolean', prop, env.commandStr);
                                return value;
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, 'typeof ' + value + '==="boolean"', 'invalid flag ' + prop, env.commandStr);
                                });
                                return value;
                            });
                        case S_DEPTH_FUNC:
                            return parseParam(function (value) {
                                check$1.commandParameter(value, compareFuncs, 'invalid ' + prop, env.commandStr);
                                return compareFuncs[value];
                            }, function (env, scope, value) {
                                var COMPARE_FUNCS = env.constants.compareFuncs;
                                check$1.optional(function () {
                                    env.assert(scope, value + ' in ' + COMPARE_FUNCS, 'invalid ' + prop + ', must be one of ' + Object.keys(compareFuncs));
                                });
                                return scope.def(COMPARE_FUNCS, '[', value, ']');
                            });
                        case S_DEPTH_RANGE:
                            return parseParam(function (value) {
                                check$1.command(isArrayLike(value) &&
                                    value.length === 2 &&
                                    typeof value[0] === 'number' &&
                                    typeof value[1] === 'number' &&
                                    value[0] <= value[1], 'depth range is 2d array', env.commandStr);
                                return value;
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, env.shared.isArrayLike + '(' + value + ')&&' +
                                        value + '.length===2&&' +
                                        'typeof ' + value + '[0]==="number"&&' +
                                        'typeof ' + value + '[1]==="number"&&' +
                                        value + '[0]<=' + value + '[1]', 'depth range must be a 2d array');
                                });
                                var Z_NEAR = scope.def('+', value, '[0]');
                                var Z_FAR = scope.def('+', value, '[1]');
                                return [Z_NEAR, Z_FAR];
                            });
                        case S_BLEND_FUNC:
                            return parseParam(function (value) {
                                check$1.commandType(value, 'object', 'blend.func', env.commandStr);
                                var srcRGB = ('srcRGB' in value ? value.srcRGB : value.src);
                                var srcAlpha = ('srcAlpha' in value ? value.srcAlpha : value.src);
                                var dstRGB = ('dstRGB' in value ? value.dstRGB : value.dst);
                                var dstAlpha = ('dstAlpha' in value ? value.dstAlpha : value.dst);
                                check$1.commandParameter(srcRGB, blendFuncs, param + '.srcRGB', env.commandStr);
                                check$1.commandParameter(srcAlpha, blendFuncs, param + '.srcAlpha', env.commandStr);
                                check$1.commandParameter(dstRGB, blendFuncs, param + '.dstRGB', env.commandStr);
                                check$1.commandParameter(dstAlpha, blendFuncs, param + '.dstAlpha', env.commandStr);
                                check$1.command((invalidBlendCombinations.indexOf(srcRGB + ', ' + dstRGB) === -1), 'unallowed blending combination (srcRGB, dstRGB) = (' + srcRGB + ', ' + dstRGB + ')', env.commandStr);
                                return [
                                    blendFuncs[srcRGB],
                                    blendFuncs[dstRGB],
                                    blendFuncs[srcAlpha],
                                    blendFuncs[dstAlpha]
                                ];
                            }, function (env, scope, value) {
                                var BLEND_FUNCS = env.constants.blendFuncs;
                                check$1.optional(function () {
                                    env.assert(scope, value + '&&typeof ' + value + '==="object"', 'invalid blend func, must be an object');
                                });
                                function read(prefix, suffix) {
                                    var func = scope.def('"', prefix, suffix, '" in ', value, '?', value, '.', prefix, suffix, ':', value, '.', prefix);
                                    check$1.optional(function () {
                                        env.assert(scope, func + ' in ' + BLEND_FUNCS, 'invalid ' + prop + '.' + prefix + suffix + ', must be one of ' + Object.keys(blendFuncs));
                                    });
                                    return func;
                                }
                                var srcRGB = read('src', 'RGB');
                                var dstRGB = read('dst', 'RGB');
                                check$1.optional(function () {
                                    var INVALID_BLEND_COMBINATIONS = env.constants.invalidBlendCombinations;
                                    env.assert(scope, INVALID_BLEND_COMBINATIONS +
                                        '.indexOf(' + srcRGB + '+", "+' + dstRGB + ') === -1 ', 'unallowed blending combination for (srcRGB, dstRGB)');
                                });
                                var SRC_RGB = scope.def(BLEND_FUNCS, '[', srcRGB, ']');
                                var SRC_ALPHA = scope.def(BLEND_FUNCS, '[', read('src', 'Alpha'), ']');
                                var DST_RGB = scope.def(BLEND_FUNCS, '[', dstRGB, ']');
                                var DST_ALPHA = scope.def(BLEND_FUNCS, '[', read('dst', 'Alpha'), ']');
                                return [SRC_RGB, DST_RGB, SRC_ALPHA, DST_ALPHA];
                            });
                        case S_BLEND_EQUATION:
                            return parseParam(function (value) {
                                if (typeof value === 'string') {
                                    check$1.commandParameter(value, blendEquations, 'invalid ' + prop, env.commandStr);
                                    return [
                                        blendEquations[value],
                                        blendEquations[value]
                                    ];
                                }
                                else if (typeof value === 'object') {
                                    check$1.commandParameter(value.rgb, blendEquations, prop + '.rgb', env.commandStr);
                                    check$1.commandParameter(value.alpha, blendEquations, prop + '.alpha', env.commandStr);
                                    return [
                                        blendEquations[value.rgb],
                                        blendEquations[value.alpha]
                                    ];
                                }
                                else {
                                    check$1.commandRaise('invalid blend.equation', env.commandStr);
                                }
                            }, function (env, scope, value) {
                                var BLEND_EQUATIONS = env.constants.blendEquations;
                                var RGB = scope.def();
                                var ALPHA = scope.def();
                                var ifte = env.cond('typeof ', value, '==="string"');
                                check$1.optional(function () {
                                    function checkProp(block, name, value) {
                                        env.assert(block, value + ' in ' + BLEND_EQUATIONS, 'invalid ' + name + ', must be one of ' + Object.keys(blendEquations));
                                    }
                                    checkProp(ifte.then, prop, value);
                                    env.assert(ifte.else, value + '&&typeof ' + value + '==="object"', 'invalid ' + prop);
                                    checkProp(ifte.else, prop + '.rgb', value + '.rgb');
                                    checkProp(ifte.else, prop + '.alpha', value + '.alpha');
                                });
                                ifte.then(RGB, '=', ALPHA, '=', BLEND_EQUATIONS, '[', value, '];');
                                ifte.else(RGB, '=', BLEND_EQUATIONS, '[', value, '.rgb];', ALPHA, '=', BLEND_EQUATIONS, '[', value, '.alpha];');
                                scope(ifte);
                                return [RGB, ALPHA];
                            });
                        case S_BLEND_COLOR:
                            return parseParam(function (value) {
                                check$1.command(isArrayLike(value) &&
                                    value.length === 4, 'blend.color must be a 4d array', env.commandStr);
                                return loop(4, function (i) {
                                    return +value[i];
                                });
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, env.shared.isArrayLike + '(' + value + ')&&' +
                                        value + '.length===4', 'blend.color must be a 4d array');
                                });
                                return loop(4, function (i) {
                                    return scope.def('+', value, '[', i, ']');
                                });
                            });
                        case S_STENCIL_MASK:
                            return parseParam(function (value) {
                                check$1.commandType(value, 'number', param, env.commandStr);
                                return value | 0;
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, 'typeof ' + value + '==="number"', 'invalid stencil.mask');
                                });
                                return scope.def(value, '|0');
                            });
                        case S_STENCIL_FUNC:
                            return parseParam(function (value) {
                                check$1.commandType(value, 'object', param, env.commandStr);
                                var cmp = value.cmp || 'keep';
                                var ref = value.ref || 0;
                                var mask = 'mask' in value ? value.mask : -1;
                                check$1.commandParameter(cmp, compareFuncs, prop + '.cmp', env.commandStr);
                                check$1.commandType(ref, 'number', prop + '.ref', env.commandStr);
                                check$1.commandType(mask, 'number', prop + '.mask', env.commandStr);
                                return [
                                    compareFuncs[cmp],
                                    ref,
                                    mask
                                ];
                            }, function (env, scope, value) {
                                var COMPARE_FUNCS = env.constants.compareFuncs;
                                check$1.optional(function () {
                                    function assert() {
                                        env.assert(scope, Array.prototype.join.call(arguments, ''), 'invalid stencil.func');
                                    }
                                    assert(value + '&&typeof ', value, '==="object"');
                                    assert('!("cmp" in ', value, ')||(', value, '.cmp in ', COMPARE_FUNCS, ')');
                                });
                                var cmp = scope.def('"cmp" in ', value, '?', COMPARE_FUNCS, '[', value, '.cmp]', ':', GL_KEEP);
                                var ref = scope.def(value, '.ref|0');
                                var mask = scope.def('"mask" in ', value, '?', value, '.mask|0:-1');
                                return [cmp, ref, mask];
                            });
                        case S_STENCIL_OPFRONT:
                        case S_STENCIL_OPBACK:
                            return parseParam(function (value) {
                                check$1.commandType(value, 'object', param, env.commandStr);
                                var fail = value.fail || 'keep';
                                var zfail = value.zfail || 'keep';
                                var zpass = value.zpass || 'keep';
                                check$1.commandParameter(fail, stencilOps, prop + '.fail', env.commandStr);
                                check$1.commandParameter(zfail, stencilOps, prop + '.zfail', env.commandStr);
                                check$1.commandParameter(zpass, stencilOps, prop + '.zpass', env.commandStr);
                                return [
                                    prop === S_STENCIL_OPBACK ? GL_BACK : GL_FRONT,
                                    stencilOps[fail],
                                    stencilOps[zfail],
                                    stencilOps[zpass]
                                ];
                            }, function (env, scope, value) {
                                var STENCIL_OPS = env.constants.stencilOps;
                                check$1.optional(function () {
                                    env.assert(scope, value + '&&typeof ' + value + '==="object"', 'invalid ' + prop);
                                });
                                function read(name) {
                                    check$1.optional(function () {
                                        env.assert(scope, '!("' + name + '" in ' + value + ')||' +
                                            '(' + value + '.' + name + ' in ' + STENCIL_OPS + ')', 'invalid ' + prop + '.' + name + ', must be one of ' + Object.keys(stencilOps));
                                    });
                                    return scope.def('"', name, '" in ', value, '?', STENCIL_OPS, '[', value, '.', name, ']:', GL_KEEP);
                                }
                                return [
                                    prop === S_STENCIL_OPBACK ? GL_BACK : GL_FRONT,
                                    read('fail'),
                                    read('zfail'),
                                    read('zpass')
                                ];
                            });
                        case S_POLYGON_OFFSET_OFFSET:
                            return parseParam(function (value) {
                                check$1.commandType(value, 'object', param, env.commandStr);
                                var factor = value.factor | 0;
                                var units = value.units | 0;
                                check$1.commandType(factor, 'number', param + '.factor', env.commandStr);
                                check$1.commandType(units, 'number', param + '.units', env.commandStr);
                                return [factor, units];
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, value + '&&typeof ' + value + '==="object"', 'invalid ' + prop);
                                });
                                var FACTOR = scope.def(value, '.factor|0');
                                var UNITS = scope.def(value, '.units|0');
                                return [FACTOR, UNITS];
                            });
                        case S_CULL_FACE:
                            return parseParam(function (value) {
                                var face = 0;
                                if (value === 'front') {
                                    face = GL_FRONT;
                                }
                                else if (value === 'back') {
                                    face = GL_BACK;
                                }
                                check$1.command(!!face, param, env.commandStr);
                                return face;
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, value + '==="front"||' +
                                        value + '==="back"', 'invalid cull.face');
                                });
                                return scope.def(value, '==="front"?', GL_FRONT, ':', GL_BACK);
                            });
                        case S_LINE_WIDTH:
                            return parseParam(function (value) {
                                check$1.command(typeof value === 'number' &&
                                    value >= limits.lineWidthDims[0] &&
                                    value <= limits.lineWidthDims[1], 'invalid line width, must be a positive number between ' +
                                    limits.lineWidthDims[0] + ' and ' + limits.lineWidthDims[1], env.commandStr);
                                return value;
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, 'typeof ' + value + '==="number"&&' +
                                        value + '>=' + limits.lineWidthDims[0] + '&&' +
                                        value + '<=' + limits.lineWidthDims[1], 'invalid line width');
                                });
                                return value;
                            });
                        case S_FRONT_FACE:
                            return parseParam(function (value) {
                                check$1.commandParameter(value, orientationType, param, env.commandStr);
                                return orientationType[value];
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, value + '==="cw"||' +
                                        value + '==="ccw"', 'invalid frontFace, must be one of cw,ccw');
                                });
                                return scope.def(value + '==="cw"?' + GL_CW + ':' + GL_CCW);
                            });
                        case S_COLOR_MASK:
                            return parseParam(function (value) {
                                check$1.command(isArrayLike(value) && value.length === 4, 'color.mask must be length 4 array', env.commandStr);
                                return value.map(function (v) { return !!v; });
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, env.shared.isArrayLike + '(' + value + ')&&' +
                                        value + '.length===4', 'invalid color.mask');
                                });
                                return loop(4, function (i) {
                                    return '!!' + value + '[' + i + ']';
                                });
                            });
                        case S_SAMPLE_COVERAGE:
                            return parseParam(function (value) {
                                check$1.command(typeof value === 'object' && value, param, env.commandStr);
                                var sampleValue = 'value' in value ? value.value : 1;
                                var sampleInvert = !!value.invert;
                                check$1.command(typeof sampleValue === 'number' &&
                                    sampleValue >= 0 && sampleValue <= 1, 'sample.coverage.value must be a number between 0 and 1', env.commandStr);
                                return [sampleValue, sampleInvert];
                            }, function (env, scope, value) {
                                check$1.optional(function () {
                                    env.assert(scope, value + '&&typeof ' + value + '==="object"', 'invalid sample.coverage');
                                });
                                var VALUE = scope.def('"value" in ', value, '?+', value, '.value:1');
                                var INVERT = scope.def('!!', value, '.invert');
                                return [VALUE, INVERT];
                            });
                    }
                });
                return STATE;
            }
            function parseUniforms(uniforms, env) {
                var staticUniforms = uniforms.static;
                var dynamicUniforms = uniforms.dynamic;
                var UNIFORMS = {};
                Object.keys(staticUniforms).forEach(function (name) {
                    var value = staticUniforms[name];
                    var result;
                    if (typeof value === 'number' ||
                        typeof value === 'boolean') {
                        result = createStaticDecl(function () {
                            return value;
                        });
                    }
                    else if (typeof value === 'function') {
                        var reglType = value._reglType;
                        if (reglType === 'texture2d' ||
                            reglType === 'textureCube') {
                            result = createStaticDecl(function (env) {
                                return env.link(value);
                            });
                        }
                        else if (reglType === 'framebuffer' ||
                            reglType === 'framebufferCube') {
                            check$1.command(value.color.length > 0, 'missing color attachment for framebuffer sent to uniform "' + name + '"', env.commandStr);
                            result = createStaticDecl(function (env) {
                                return env.link(value.color[0]);
                            });
                        }
                        else {
                            check$1.commandRaise('invalid data for uniform "' + name + '"', env.commandStr);
                        }
                    }
                    else if (isArrayLike(value)) {
                        result = createStaticDecl(function (env) {
                            var ITEM = env.global.def('[', loop(value.length, function (i) {
                                check$1.command(typeof value[i] === 'number' ||
                                    typeof value[i] === 'boolean', 'invalid uniform ' + name, env.commandStr);
                                return value[i];
                            }), ']');
                            return ITEM;
                        });
                    }
                    else {
                        check$1.commandRaise('invalid or missing data for uniform "' + name + '"', env.commandStr);
                    }
                    result.value = value;
                    UNIFORMS[name] = result;
                });
                Object.keys(dynamicUniforms).forEach(function (key) {
                    var dyn = dynamicUniforms[key];
                    UNIFORMS[key] = createDynamicDecl(dyn, function (env, scope) {
                        return env.invoke(scope, dyn);
                    });
                });
                return UNIFORMS;
            }
            function parseAttributes(attributes, env) {
                var staticAttributes = attributes.static;
                var dynamicAttributes = attributes.dynamic;
                var attributeDefs = {};
                Object.keys(staticAttributes).forEach(function (attribute) {
                    var value = staticAttributes[attribute];
                    var id = stringStore.id(attribute);
                    var record = new AttributeRecord();
                    if (isBufferArgs(value)) {
                        record.state = ATTRIB_STATE_POINTER;
                        record.buffer = bufferState.getBuffer(bufferState.create(value, GL_ARRAY_BUFFER$2, false, true));
                        record.type = 0;
                    }
                    else {
                        var buffer = bufferState.getBuffer(value);
                        if (buffer) {
                            record.state = ATTRIB_STATE_POINTER;
                            record.buffer = buffer;
                            record.type = 0;
                        }
                        else {
                            check$1.command(typeof value === 'object' && value, 'invalid data for attribute ' + attribute, env.commandStr);
                            if ('constant' in value) {
                                var constant = value.constant;
                                record.buffer = 'null';
                                record.state = ATTRIB_STATE_CONSTANT;
                                if (typeof constant === 'number') {
                                    record.x = constant;
                                }
                                else {
                                    check$1.command(isArrayLike(constant) &&
                                        constant.length > 0 &&
                                        constant.length <= 4, 'invalid constant for attribute ' + attribute, env.commandStr);
                                    CUTE_COMPONENTS.forEach(function (c, i) {
                                        if (i < constant.length) {
                                            record[c] = constant[i];
                                        }
                                    });
                                }
                            }
                            else {
                                if (isBufferArgs(value.buffer)) {
                                    buffer = bufferState.getBuffer(bufferState.create(value.buffer, GL_ARRAY_BUFFER$2, false, true));
                                }
                                else {
                                    buffer = bufferState.getBuffer(value.buffer);
                                }
                                check$1.command(!!buffer, 'missing buffer for attribute "' + attribute + '"', env.commandStr);
                                var offset = value.offset | 0;
                                check$1.command(offset >= 0, 'invalid offset for attribute "' + attribute + '"', env.commandStr);
                                var stride = value.stride | 0;
                                check$1.command(stride >= 0 && stride < 256, 'invalid stride for attribute "' + attribute + '", must be integer betweeen [0, 255]', env.commandStr);
                                var size = value.size | 0;
                                check$1.command(!('size' in value) || (size > 0 && size <= 4), 'invalid size for attribute "' + attribute + '", must be 1,2,3,4', env.commandStr);
                                var normalized = !!value.normalized;
                                var type = 0;
                                if ('type' in value) {
                                    check$1.commandParameter(value.type, glTypes, 'invalid type for attribute ' + attribute, env.commandStr);
                                    type = glTypes[value.type];
                                }
                                var divisor = value.divisor | 0;
                                check$1.optional(function () {
                                    if ('divisor' in value) {
                                        check$1.command(divisor === 0 || extInstancing, 'cannot specify divisor for attribute "' + attribute + '", instancing not supported', env.commandStr);
                                        check$1.command(divisor >= 0, 'invalid divisor for attribute "' + attribute + '"', env.commandStr);
                                    }
                                    var command = env.commandStr;
                                    var VALID_KEYS = [
                                        'buffer',
                                        'offset',
                                        'divisor',
                                        'normalized',
                                        'type',
                                        'size',
                                        'stride'
                                    ];
                                    Object.keys(value).forEach(function (prop) {
                                        check$1.command(VALID_KEYS.indexOf(prop) >= 0, 'unknown parameter "' + prop + '" for attribute pointer "' + attribute + '" (valid parameters are ' + VALID_KEYS + ')', command);
                                    });
                                });
                                record.buffer = buffer;
                                record.state = ATTRIB_STATE_POINTER;
                                record.size = size;
                                record.normalized = normalized;
                                record.type = type || buffer.dtype;
                                record.offset = offset;
                                record.stride = stride;
                                record.divisor = divisor;
                            }
                        }
                    }
                    attributeDefs[attribute] = createStaticDecl(function (env, scope) {
                        var cache = env.attribCache;
                        if (id in cache) {
                            return cache[id];
                        }
                        var result = {
                            isStream: false
                        };
                        Object.keys(record).forEach(function (key) {
                            result[key] = record[key];
                        });
                        if (record.buffer) {
                            result.buffer = env.link(record.buffer);
                            result.type = result.type || (result.buffer + '.dtype');
                        }
                        cache[id] = result;
                        return result;
                    });
                });
                Object.keys(dynamicAttributes).forEach(function (attribute) {
                    var dyn = dynamicAttributes[attribute];
                    function appendAttributeCode(env, block) {
                        var VALUE = env.invoke(block, dyn);
                        var shared = env.shared;
                        var constants = env.constants;
                        var IS_BUFFER_ARGS = shared.isBufferArgs;
                        var BUFFER_STATE = shared.buffer;
                        // Perform validation on attribute
                        check$1.optional(function () {
                            env.assert(block, VALUE + '&&(typeof ' + VALUE + '==="object"||typeof ' +
                                VALUE + '==="function")&&(' +
                                IS_BUFFER_ARGS + '(' + VALUE + ')||' +
                                BUFFER_STATE + '.getBuffer(' + VALUE + ')||' +
                                BUFFER_STATE + '.getBuffer(' + VALUE + '.buffer)||' +
                                IS_BUFFER_ARGS + '(' + VALUE + '.buffer)||' +
                                '("constant" in ' + VALUE +
                                '&&(typeof ' + VALUE + '.constant==="number"||' +
                                shared.isArrayLike + '(' + VALUE + '.constant))))', 'invalid dynamic attribute "' + attribute + '"');
                        });
                        // allocate names for result
                        var result = {
                            isStream: block.def(false)
                        };
                        var defaultRecord = new AttributeRecord();
                        defaultRecord.state = ATTRIB_STATE_POINTER;
                        Object.keys(defaultRecord).forEach(function (key) {
                            result[key] = block.def('' + defaultRecord[key]);
                        });
                        var BUFFER = result.buffer;
                        var TYPE = result.type;
                        block('if(', IS_BUFFER_ARGS, '(', VALUE, ')){', result.isStream, '=true;', BUFFER, '=', BUFFER_STATE, '.createStream(', GL_ARRAY_BUFFER$2, ',', VALUE, ');', TYPE, '=', BUFFER, '.dtype;', '}else{', BUFFER, '=', BUFFER_STATE, '.getBuffer(', VALUE, ');', 'if(', BUFFER, '){', TYPE, '=', BUFFER, '.dtype;', '}else if("constant" in ', VALUE, '){', result.state, '=', ATTRIB_STATE_CONSTANT, ';', 'if(typeof ' + VALUE + '.constant === "number"){', result[CUTE_COMPONENTS[0]], '=', VALUE, '.constant;', CUTE_COMPONENTS.slice(1).map(function (n) {
                            return result[n];
                        }).join('='), '=0;', '}else{', CUTE_COMPONENTS.map(function (name, i) {
                            return (result[name] + '=' + VALUE + '.constant.length>' + i +
                                '?' + VALUE + '.constant[' + i + ']:0;');
                        }).join(''), '}}else{', 'if(', IS_BUFFER_ARGS, '(', VALUE, '.buffer)){', BUFFER, '=', BUFFER_STATE, '.createStream(', GL_ARRAY_BUFFER$2, ',', VALUE, '.buffer);', '}else{', BUFFER, '=', BUFFER_STATE, '.getBuffer(', VALUE, '.buffer);', '}', TYPE, '="type" in ', VALUE, '?', constants.glTypes, '[', VALUE, '.type]:', BUFFER, '.dtype;', result.normalized, '=!!', VALUE, '.normalized;');
                        function emitReadRecord(name) {
                            block(result[name], '=', VALUE, '.', name, '|0;');
                        }
                        emitReadRecord('size');
                        emitReadRecord('offset');
                        emitReadRecord('stride');
                        emitReadRecord('divisor');
                        block('}}');
                        block.exit('if(', result.isStream, '){', BUFFER_STATE, '.destroyStream(', BUFFER, ');', '}');
                        return result;
                    }
                    attributeDefs[attribute] = createDynamicDecl(dyn, appendAttributeCode);
                });
                return attributeDefs;
            }
            function parseContext(context) {
                var staticContext = context.static;
                var dynamicContext = context.dynamic;
                var result = {};
                Object.keys(staticContext).forEach(function (name) {
                    var value = staticContext[name];
                    result[name] = createStaticDecl(function (env, scope) {
                        if (typeof value === 'number' || typeof value === 'boolean') {
                            return '' + value;
                        }
                        else {
                            return env.link(value);
                        }
                    });
                });
                Object.keys(dynamicContext).forEach(function (name) {
                    var dyn = dynamicContext[name];
                    result[name] = createDynamicDecl(dyn, function (env, scope) {
                        return env.invoke(scope, dyn);
                    });
                });
                return result;
            }
            function parseArguments(options, attributes, uniforms, context, env) {
                var staticOptions = options.static;
                var dynamicOptions = options.dynamic;
                check$1.optional(function () {
                    var KEY_NAMES = [
                        S_FRAMEBUFFER,
                        S_VERT,
                        S_FRAG,
                        S_ELEMENTS,
                        S_PRIMITIVE,
                        S_OFFSET,
                        S_COUNT,
                        S_INSTANCES,
                        S_PROFILE,
                        S_VAO
                    ].concat(GL_STATE_NAMES);
                    function checkKeys(dict) {
                        Object.keys(dict).forEach(function (key) {
                            check$1.command(KEY_NAMES.indexOf(key) >= 0, 'unknown parameter "' + key + '"', env.commandStr);
                        });
                    }
                    checkKeys(staticOptions);
                    checkKeys(dynamicOptions);
                });
                var attribLocations = parseAttribLocations(options, attributes);
                var framebuffer = parseFramebuffer(options, env);
                var viewportAndScissor = parseViewportScissor(options, framebuffer, env);
                var draw = parseDraw(options, env);
                var state = parseGLState(options, env);
                var shader = parseProgram(options, env, attribLocations);
                function copyBox(name) {
                    var defn = viewportAndScissor[name];
                    if (defn) {
                        state[name] = defn;
                    }
                }
                copyBox(S_VIEWPORT);
                copyBox(propName(S_SCISSOR_BOX));
                var dirty = Object.keys(state).length > 0;
                var result = {
                    framebuffer: framebuffer,
                    draw: draw,
                    shader: shader,
                    state: state,
                    dirty: dirty,
                    scopeVAO: null,
                    drawVAO: null,
                    useVAO: false,
                    attributes: {}
                };
                result.profile = parseProfile(options, env);
                result.uniforms = parseUniforms(uniforms, env);
                result.drawVAO = result.scopeVAO = draw.vao;
                // special case: check if we can statically allocate a vertex array object for this program
                if (!result.drawVAO &&
                    shader.program &&
                    !attribLocations &&
                    extensions.angle_instanced_arrays &&
                    draw.static.elements) {
                    var useVAO = true;
                    var staticBindings = shader.program.attributes.map(function (attr) {
                        var binding = attributes.static[attr];
                        useVAO = useVAO && !!binding;
                        return binding;
                    });
                    if (useVAO && staticBindings.length > 0) {
                        var vao = attributeState.getVAO(attributeState.createVAO({
                            attributes: staticBindings,
                            elements: draw.static.elements
                        }));
                        result.drawVAO = new Declaration(null, null, null, function (env, scope) {
                            return env.link(vao);
                        });
                        result.useVAO = true;
                    }
                }
                if (attribLocations) {
                    result.useVAO = true;
                }
                else {
                    result.attributes = parseAttributes(attributes, env);
                }
                result.context = parseContext(context, env);
                return result;
            }
            // ===================================================
            // ===================================================
            // COMMON UPDATE FUNCTIONS
            // ===================================================
            // ===================================================
            function emitContext(env, scope, context) {
                var shared = env.shared;
                var CONTEXT = shared.context;
                var contextEnter = env.scope();
                Object.keys(context).forEach(function (name) {
                    scope.save(CONTEXT, '.' + name);
                    var defn = context[name];
                    var value = defn.append(env, scope);
                    if (Array.isArray(value)) {
                        contextEnter(CONTEXT, '.', name, '=[', value.join(), '];');
                    }
                    else {
                        contextEnter(CONTEXT, '.', name, '=', value, ';');
                    }
                });
                scope(contextEnter);
            }
            // ===================================================
            // ===================================================
            // COMMON DRAWING FUNCTIONS
            // ===================================================
            // ===================================================
            function emitPollFramebuffer(env, scope, framebuffer, skipCheck) {
                var shared = env.shared;
                var GL = shared.gl;
                var FRAMEBUFFER_STATE = shared.framebuffer;
                var EXT_DRAW_BUFFERS;
                if (extDrawBuffers) {
                    EXT_DRAW_BUFFERS = scope.def(shared.extensions, '.webgl_draw_buffers');
                }
                var constants = env.constants;
                var DRAW_BUFFERS = constants.drawBuffer;
                var BACK_BUFFER = constants.backBuffer;
                var NEXT;
                if (framebuffer) {
                    NEXT = framebuffer.append(env, scope);
                }
                else {
                    NEXT = scope.def(FRAMEBUFFER_STATE, '.next');
                }
                if (!skipCheck) {
                    scope('if(', NEXT, '!==', FRAMEBUFFER_STATE, '.cur){');
                }
                scope('if(', NEXT, '){', GL, '.bindFramebuffer(', GL_FRAMEBUFFER$2, ',', NEXT, '.framebuffer);');
                if (extDrawBuffers) {
                    scope(EXT_DRAW_BUFFERS, '.drawBuffersWEBGL(', DRAW_BUFFERS, '[', NEXT, '.colorAttachments.length]);');
                }
                scope('}else{', GL, '.bindFramebuffer(', GL_FRAMEBUFFER$2, ',null);');
                if (extDrawBuffers) {
                    scope(EXT_DRAW_BUFFERS, '.drawBuffersWEBGL(', BACK_BUFFER, ');');
                }
                scope('}', FRAMEBUFFER_STATE, '.cur=', NEXT, ';');
                if (!skipCheck) {
                    scope('}');
                }
            }
            function emitPollState(env, scope, args) {
                var shared = env.shared;
                var GL = shared.gl;
                var CURRENT_VARS = env.current;
                var NEXT_VARS = env.next;
                var CURRENT_STATE = shared.current;
                var NEXT_STATE = shared.next;
                var block = env.cond(CURRENT_STATE, '.dirty');
                GL_STATE_NAMES.forEach(function (prop) {
                    var param = propName(prop);
                    if (param in args.state) {
                        return;
                    }
                    var NEXT, CURRENT;
                    if (param in NEXT_VARS) {
                        NEXT = NEXT_VARS[param];
                        CURRENT = CURRENT_VARS[param];
                        var parts = loop(currentState[param].length, function (i) {
                            return block.def(NEXT, '[', i, ']');
                        });
                        block(env.cond(parts.map(function (p, i) {
                            return p + '!==' + CURRENT + '[' + i + ']';
                        }).join('||'))
                            .then(GL, '.', GL_VARIABLES[param], '(', parts, ');', parts.map(function (p, i) {
                            return CURRENT + '[' + i + ']=' + p;
                        }).join(';'), ';'));
                    }
                    else {
                        NEXT = block.def(NEXT_STATE, '.', param);
                        var ifte = env.cond(NEXT, '!==', CURRENT_STATE, '.', param);
                        block(ifte);
                        if (param in GL_FLAGS) {
                            ifte(env.cond(NEXT)
                                .then(GL, '.enable(', GL_FLAGS[param], ');')
                                .else(GL, '.disable(', GL_FLAGS[param], ');'), CURRENT_STATE, '.', param, '=', NEXT, ';');
                        }
                        else {
                            ifte(GL, '.', GL_VARIABLES[param], '(', NEXT, ');', CURRENT_STATE, '.', param, '=', NEXT, ';');
                        }
                    }
                });
                if (Object.keys(args.state).length === 0) {
                    block(CURRENT_STATE, '.dirty=false;');
                }
                scope(block);
            }
            function emitSetOptions(env, scope, options, filter) {
                var shared = env.shared;
                var CURRENT_VARS = env.current;
                var CURRENT_STATE = shared.current;
                var GL = shared.gl;
                sortState(Object.keys(options)).forEach(function (param) {
                    var defn = options[param];
                    if (filter && !filter(defn)) {
                        return;
                    }
                    var variable = defn.append(env, scope);
                    if (GL_FLAGS[param]) {
                        var flag = GL_FLAGS[param];
                        if (isStatic(defn)) {
                            if (variable) {
                                scope(GL, '.enable(', flag, ');');
                            }
                            else {
                                scope(GL, '.disable(', flag, ');');
                            }
                        }
                        else {
                            scope(env.cond(variable)
                                .then(GL, '.enable(', flag, ');')
                                .else(GL, '.disable(', flag, ');'));
                        }
                        scope(CURRENT_STATE, '.', param, '=', variable, ';');
                    }
                    else if (isArrayLike(variable)) {
                        var CURRENT = CURRENT_VARS[param];
                        scope(GL, '.', GL_VARIABLES[param], '(', variable, ');', variable.map(function (v, i) {
                            return CURRENT + '[' + i + ']=' + v;
                        }).join(';'), ';');
                    }
                    else {
                        scope(GL, '.', GL_VARIABLES[param], '(', variable, ');', CURRENT_STATE, '.', param, '=', variable, ';');
                    }
                });
            }
            function injectExtensions(env, scope) {
                if (extInstancing) {
                    env.instancing = scope.def(env.shared.extensions, '.angle_instanced_arrays');
                }
            }
            function emitProfile(env, scope, args, useScope, incrementCounter) {
                var shared = env.shared;
                var STATS = env.stats;
                var CURRENT_STATE = shared.current;
                var TIMER = shared.timer;
                var profileArg = args.profile;
                function perfCounter() {
                    if (typeof performance === 'undefined') {
                        return 'Date.now()';
                    }
                    else {
                        return 'performance.now()';
                    }
                }
                var CPU_START, QUERY_COUNTER;
                function emitProfileStart(block) {
                    CPU_START = scope.def();
                    block(CPU_START, '=', perfCounter(), ';');
                    if (typeof incrementCounter === 'string') {
                        block(STATS, '.count+=', incrementCounter, ';');
                    }
                    else {
                        block(STATS, '.count++;');
                    }
                    if (timer) {
                        if (useScope) {
                            QUERY_COUNTER = scope.def();
                            block(QUERY_COUNTER, '=', TIMER, '.getNumPendingQueries();');
                        }
                        else {
                            block(TIMER, '.beginQuery(', STATS, ');');
                        }
                    }
                }
                function emitProfileEnd(block) {
                    block(STATS, '.cpuTime+=', perfCounter(), '-', CPU_START, ';');
                    if (timer) {
                        if (useScope) {
                            block(TIMER, '.pushScopeStats(', QUERY_COUNTER, ',', TIMER, '.getNumPendingQueries(),', STATS, ');');
                        }
                        else {
                            block(TIMER, '.endQuery();');
                        }
                    }
                }
                function scopeProfile(value) {
                    var prev = scope.def(CURRENT_STATE, '.profile');
                    scope(CURRENT_STATE, '.profile=', value, ';');
                    scope.exit(CURRENT_STATE, '.profile=', prev, ';');
                }
                var USE_PROFILE;
                if (profileArg) {
                    if (isStatic(profileArg)) {
                        if (profileArg.enable) {
                            emitProfileStart(scope);
                            emitProfileEnd(scope.exit);
                            scopeProfile('true');
                        }
                        else {
                            scopeProfile('false');
                        }
                        return;
                    }
                    USE_PROFILE = profileArg.append(env, scope);
                    scopeProfile(USE_PROFILE);
                }
                else {
                    USE_PROFILE = scope.def(CURRENT_STATE, '.profile');
                }
                var start = env.block();
                emitProfileStart(start);
                scope('if(', USE_PROFILE, '){', start, '}');
                var end = env.block();
                emitProfileEnd(end);
                scope.exit('if(', USE_PROFILE, '){', end, '}');
            }
            function emitAttributes(env, scope, args, attributes, filter) {
                var shared = env.shared;
                function typeLength(x) {
                    switch (x) {
                        case GL_FLOAT_VEC2:
                        case GL_INT_VEC2:
                        case GL_BOOL_VEC2:
                            return 2;
                        case GL_FLOAT_VEC3:
                        case GL_INT_VEC3:
                        case GL_BOOL_VEC3:
                            return 3;
                        case GL_FLOAT_VEC4:
                        case GL_INT_VEC4:
                        case GL_BOOL_VEC4:
                            return 4;
                        default:
                            return 1;
                    }
                }
                function emitBindAttribute(ATTRIBUTE, size, record) {
                    var GL = shared.gl;
                    var LOCATION = scope.def(ATTRIBUTE, '.location');
                    var BINDING = scope.def(shared.attributes, '[', LOCATION, ']');
                    var STATE = record.state;
                    var BUFFER = record.buffer;
                    var CONST_COMPONENTS = [
                        record.x,
                        record.y,
                        record.z,
                        record.w
                    ];
                    var COMMON_KEYS = [
                        'buffer',
                        'normalized',
                        'offset',
                        'stride'
                    ];
                    function emitBuffer() {
                        scope('if(!', BINDING, '.buffer){', GL, '.enableVertexAttribArray(', LOCATION, ');}');
                        var TYPE = record.type;
                        var SIZE;
                        if (!record.size) {
                            SIZE = size;
                        }
                        else {
                            SIZE = scope.def(record.size, '||', size);
                        }
                        scope('if(', BINDING, '.type!==', TYPE, '||', BINDING, '.size!==', SIZE, '||', COMMON_KEYS.map(function (key) {
                            return BINDING + '.' + key + '!==' + record[key];
                        }).join('||'), '){', GL, '.bindBuffer(', GL_ARRAY_BUFFER$2, ',', BUFFER, '.buffer);', GL, '.vertexAttribPointer(', [
                            LOCATION,
                            SIZE,
                            TYPE,
                            record.normalized,
                            record.stride,
                            record.offset
                        ], ');', BINDING, '.type=', TYPE, ';', BINDING, '.size=', SIZE, ';', COMMON_KEYS.map(function (key) {
                            return BINDING + '.' + key + '=' + record[key] + ';';
                        }).join(''), '}');
                        if (extInstancing) {
                            var DIVISOR = record.divisor;
                            scope('if(', BINDING, '.divisor!==', DIVISOR, '){', env.instancing, '.vertexAttribDivisorANGLE(', [LOCATION, DIVISOR], ');', BINDING, '.divisor=', DIVISOR, ';}');
                        }
                    }
                    function emitConstant() {
                        scope('if(', BINDING, '.buffer){', GL, '.disableVertexAttribArray(', LOCATION, ');', BINDING, '.buffer=null;', '}if(', CUTE_COMPONENTS.map(function (c, i) {
                            return BINDING + '.' + c + '!==' + CONST_COMPONENTS[i];
                        }).join('||'), '){', GL, '.vertexAttrib4f(', LOCATION, ',', CONST_COMPONENTS, ');', CUTE_COMPONENTS.map(function (c, i) {
                            return BINDING + '.' + c + '=' + CONST_COMPONENTS[i] + ';';
                        }).join(''), '}');
                    }
                    if (STATE === ATTRIB_STATE_POINTER) {
                        emitBuffer();
                    }
                    else if (STATE === ATTRIB_STATE_CONSTANT) {
                        emitConstant();
                    }
                    else {
                        scope('if(', STATE, '===', ATTRIB_STATE_POINTER, '){');
                        emitBuffer();
                        scope('}else{');
                        emitConstant();
                        scope('}');
                    }
                }
                attributes.forEach(function (attribute) {
                    var name = attribute.name;
                    var arg = args.attributes[name];
                    var record;
                    if (arg) {
                        if (!filter(arg)) {
                            return;
                        }
                        record = arg.append(env, scope);
                    }
                    else {
                        if (!filter(SCOPE_DECL)) {
                            return;
                        }
                        var scopeAttrib = env.scopeAttrib(name);
                        check$1.optional(function () {
                            env.assert(scope, scopeAttrib + '.state', 'missing attribute ' + name);
                        });
                        record = {};
                        Object.keys(new AttributeRecord()).forEach(function (key) {
                            record[key] = scope.def(scopeAttrib, '.', key);
                        });
                    }
                    emitBindAttribute(env.link(attribute), typeLength(attribute.info.type), record);
                });
            }
            function emitUniforms(env, scope, args, uniforms, filter, isBatchInnerLoop) {
                var shared = env.shared;
                var GL = shared.gl;
                var definedArrUniforms = {};
                var infix;
                for (var i = 0; i < uniforms.length; ++i) {
                    var uniform = uniforms[i];
                    var name = uniform.name;
                    var type = uniform.info.type;
                    var size = uniform.info.size;
                    var arg = args.uniforms[name];
                    if (size > 1) {
                        // either foo[n] or foos, avoid define both
                        if (!arg) {
                            continue;
                        }
                        var arrUniformName = name.replace('[0]', '');
                        if (definedArrUniforms[arrUniformName]) {
                            continue;
                        }
                        definedArrUniforms[arrUniformName] = 1;
                    }
                    var UNIFORM = env.link(uniform);
                    var LOCATION = UNIFORM + '.location';
                    var VALUE;
                    if (arg) {
                        if (!filter(arg)) {
                            continue;
                        }
                        if (isStatic(arg)) {
                            var value = arg.value;
                            check$1.command(value !== null && typeof value !== 'undefined', 'missing uniform "' + name + '"', env.commandStr);
                            if (type === GL_SAMPLER_2D || type === GL_SAMPLER_CUBE) {
                                check$1.command(typeof value === 'function' &&
                                    ((type === GL_SAMPLER_2D &&
                                        (value._reglType === 'texture2d' ||
                                            value._reglType === 'framebuffer')) ||
                                        (type === GL_SAMPLER_CUBE &&
                                            (value._reglType === 'textureCube' ||
                                                value._reglType === 'framebufferCube'))), 'invalid texture for uniform ' + name, env.commandStr);
                                var TEX_VALUE = env.link(value._texture || value.color[0]._texture);
                                scope(GL, '.uniform1i(', LOCATION, ',', TEX_VALUE + '.bind());');
                                scope.exit(TEX_VALUE, '.unbind();');
                            }
                            else if (type === GL_FLOAT_MAT2 ||
                                type === GL_FLOAT_MAT3 ||
                                type === GL_FLOAT_MAT4) {
                                check$1.optional(function () {
                                    check$1.command(isArrayLike(value), 'invalid matrix for uniform ' + name, env.commandStr);
                                    check$1.command((type === GL_FLOAT_MAT2 && value.length === 4) ||
                                        (type === GL_FLOAT_MAT3 && value.length === 9) ||
                                        (type === GL_FLOAT_MAT4 && value.length === 16), 'invalid length for matrix uniform ' + name, env.commandStr);
                                });
                                var MAT_VALUE = env.global.def('new Float32Array([' +
                                    Array.prototype.slice.call(value) + '])');
                                var dim = 2;
                                if (type === GL_FLOAT_MAT3) {
                                    dim = 3;
                                }
                                else if (type === GL_FLOAT_MAT4) {
                                    dim = 4;
                                }
                                scope(GL, '.uniformMatrix', dim, 'fv(', LOCATION, ',false,', MAT_VALUE, ');');
                            }
                            else {
                                switch (type) {
                                    case GL_FLOAT$8:
                                        if (size === 1) {
                                            check$1.commandType(value, 'number', 'uniform ' + name, env.commandStr);
                                        }
                                        else {
                                            check$1.command(isArrayLike(value) && (value.length === size), 'uniform ' + name, env.commandStr);
                                        }
                                        infix = '1f';
                                        break;
                                    case GL_FLOAT_VEC2:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 2 === 0 && value.length <= size * 2), 'uniform ' + name, env.commandStr);
                                        infix = '2f';
                                        break;
                                    case GL_FLOAT_VEC3:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 3 === 0 && value.length <= size * 3), 'uniform ' + name, env.commandStr);
                                        infix = '3f';
                                        break;
                                    case GL_FLOAT_VEC4:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 4 === 0 && value.length <= size * 4), 'uniform ' + name, env.commandStr);
                                        infix = '4f';
                                        break;
                                    case GL_BOOL:
                                        if (size === 1) {
                                            check$1.commandType(value, 'boolean', 'uniform ' + name, env.commandStr);
                                        }
                                        else {
                                            check$1.command(isArrayLike(value) && (value.length === size), 'uniform ' + name, env.commandStr);
                                        }
                                        infix = '1i';
                                        break;
                                    case GL_INT$3:
                                        if (size === 1) {
                                            check$1.commandType(value, 'number', 'uniform ' + name, env.commandStr);
                                        }
                                        else {
                                            check$1.command(isArrayLike(value) && (value.length === size), 'uniform ' + name, env.commandStr);
                                        }
                                        infix = '1i';
                                        break;
                                    case GL_BOOL_VEC2:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 2 === 0 && value.length <= size * 2), 'uniform ' + name, env.commandStr);
                                        infix = '2i';
                                        break;
                                    case GL_INT_VEC2:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 2 === 0 && value.length <= size * 2), 'uniform ' + name, env.commandStr);
                                        infix = '2i';
                                        break;
                                    case GL_BOOL_VEC3:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 3 === 0 && value.length <= size * 3), 'uniform ' + name, env.commandStr);
                                        infix = '3i';
                                        break;
                                    case GL_INT_VEC3:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 3 === 0 && value.length <= size * 3), 'uniform ' + name, env.commandStr);
                                        infix = '3i';
                                        break;
                                    case GL_BOOL_VEC4:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 4 === 0 && value.length <= size * 4), 'uniform ' + name, env.commandStr);
                                        infix = '4i';
                                        break;
                                    case GL_INT_VEC4:
                                        check$1.command(isArrayLike(value) && (value.length && value.length % 4 === 0 && value.length <= size * 4), 'uniform ' + name, env.commandStr);
                                        infix = '4i';
                                        break;
                                }
                                if (size > 1) {
                                    infix += 'v';
                                    value = env.global.def('[' +
                                        Array.prototype.slice.call(value) + ']');
                                }
                                else {
                                    value = isArrayLike(value) ? Array.prototype.slice.call(value) : value;
                                }
                                scope(GL, '.uniform', infix, '(', LOCATION, ',', value, ');');
                            }
                            continue;
                        }
                        else {
                            VALUE = arg.append(env, scope);
                        }
                    }
                    else {
                        if (!filter(SCOPE_DECL)) {
                            continue;
                        }
                        VALUE = scope.def(shared.uniforms, '[', stringStore.id(name), ']');
                    }
                    if (type === GL_SAMPLER_2D) {
                        check$1(!Array.isArray(VALUE), 'must specify a scalar prop for textures');
                        scope('if(', VALUE, '&&', VALUE, '._reglType==="framebuffer"){', VALUE, '=', VALUE, '.color[0];', '}');
                    }
                    else if (type === GL_SAMPLER_CUBE) {
                        check$1(!Array.isArray(VALUE), 'must specify a scalar prop for cube maps');
                        scope('if(', VALUE, '&&', VALUE, '._reglType==="framebufferCube"){', VALUE, '=', VALUE, '.color[0];', '}');
                    }
                    // perform type validation
                    check$1.optional(function () {
                        function emitCheck(pred, message) {
                            env.assert(scope, pred, 'bad data or missing for uniform "' + name + '".  ' + message);
                        }
                        function checkType(type, size) {
                            if (size === 1) {
                                check$1(!Array.isArray(VALUE), 'must not specify an array type for uniform');
                            }
                            emitCheck('Array.isArray(' + VALUE + ') && typeof ' + VALUE + '[0]===" ' + type + '"' +
                                ' || typeof ' + VALUE + '==="' + type + '"', 'invalid type, expected ' + type);
                        }
                        function checkVector(n, type, size) {
                            if (Array.isArray(VALUE)) {
                                check$1(VALUE.length && VALUE.length % n === 0 && VALUE.length <= n * size, 'must have length of ' + (size === 1 ? '' : 'n * ') + n);
                            }
                            else {
                                emitCheck(shared.isArrayLike + '(' + VALUE + ')&&' + VALUE + '.length && ' + VALUE + '.length % ' + n + ' === 0' +
                                    ' && ' + VALUE + '.length<=' + n * size, 'invalid vector, should have length of ' + (size === 1 ? '' : 'n * ') + n, env.commandStr);
                            }
                        }
                        function checkTexture(target) {
                            check$1(!Array.isArray(VALUE), 'must not specify a value type');
                            emitCheck('typeof ' + VALUE + '==="function"&&' +
                                VALUE + '._reglType==="texture' +
                                (target === GL_TEXTURE_2D$3 ? '2d' : 'Cube') + '"', 'invalid texture type', env.commandStr);
                        }
                        switch (type) {
                            case GL_INT$3:
                                checkType('number', size);
                                break;
                            case GL_INT_VEC2:
                                checkVector(2, 'number', size);
                                break;
                            case GL_INT_VEC3:
                                checkVector(3, 'number', size);
                                break;
                            case GL_INT_VEC4:
                                checkVector(4, 'number', size);
                                break;
                            case GL_FLOAT$8:
                                checkType('number', size);
                                break;
                            case GL_FLOAT_VEC2:
                                checkVector(2, 'number', size);
                                break;
                            case GL_FLOAT_VEC3:
                                checkVector(3, 'number', size);
                                break;
                            case GL_FLOAT_VEC4:
                                checkVector(4, 'number', size);
                                break;
                            case GL_BOOL:
                                checkType('boolean', size);
                                break;
                            case GL_BOOL_VEC2:
                                checkVector(2, 'boolean', size);
                                break;
                            case GL_BOOL_VEC3:
                                checkVector(3, 'boolean', size);
                                break;
                            case GL_BOOL_VEC4:
                                checkVector(4, 'boolean', size);
                                break;
                            case GL_FLOAT_MAT2:
                                checkVector(4, 'number', size);
                                break;
                            case GL_FLOAT_MAT3:
                                checkVector(9, 'number', size);
                                break;
                            case GL_FLOAT_MAT4:
                                checkVector(16, 'number', size);
                                break;
                            case GL_SAMPLER_2D:
                                checkTexture(GL_TEXTURE_2D$3);
                                break;
                            case GL_SAMPLER_CUBE:
                                checkTexture(GL_TEXTURE_CUBE_MAP$2);
                                break;
                        }
                    });
                    var unroll = 1;
                    switch (type) {
                        case GL_SAMPLER_2D:
                        case GL_SAMPLER_CUBE:
                            var TEX = scope.def(VALUE, '._texture');
                            scope(GL, '.uniform1i(', LOCATION, ',', TEX, '.bind());');
                            scope.exit(TEX, '.unbind();');
                            continue;
                        case GL_INT$3:
                        case GL_BOOL:
                            infix = '1i';
                            break;
                        case GL_INT_VEC2:
                        case GL_BOOL_VEC2:
                            infix = '2i';
                            unroll = 2;
                            break;
                        case GL_INT_VEC3:
                        case GL_BOOL_VEC3:
                            infix = '3i';
                            unroll = 3;
                            break;
                        case GL_INT_VEC4:
                        case GL_BOOL_VEC4:
                            infix = '4i';
                            unroll = 4;
                            break;
                        case GL_FLOAT$8:
                            infix = '1f';
                            break;
                        case GL_FLOAT_VEC2:
                            infix = '2f';
                            unroll = 2;
                            break;
                        case GL_FLOAT_VEC3:
                            infix = '3f';
                            unroll = 3;
                            break;
                        case GL_FLOAT_VEC4:
                            infix = '4f';
                            unroll = 4;
                            break;
                        case GL_FLOAT_MAT2:
                            infix = 'Matrix2fv';
                            break;
                        case GL_FLOAT_MAT3:
                            infix = 'Matrix3fv';
                            break;
                        case GL_FLOAT_MAT4:
                            infix = 'Matrix4fv';
                            break;
                    }
                    if (infix.indexOf('Matrix') === -1 && size > 1) {
                        infix += 'v';
                        unroll = 1;
                    }
                    if (infix.charAt(0) === 'M') {
                        scope(GL, '.uniform', infix, '(', LOCATION, ',');
                        var matSize = Math.pow(type - GL_FLOAT_MAT2 + 2, 2);
                        var STORAGE = env.global.def('new Float32Array(', matSize, ')');
                        if (Array.isArray(VALUE)) {
                            scope('false,(', loop(matSize, function (i) {
                                return STORAGE + '[' + i + ']=' + VALUE[i];
                            }), ',', STORAGE, ')');
                        }
                        else {
                            scope('false,(Array.isArray(', VALUE, ')||', VALUE, ' instanceof Float32Array)?', VALUE, ':(', loop(matSize, function (i) {
                                return STORAGE + '[' + i + ']=' + VALUE + '[' + i + ']';
                            }), ',', STORAGE, ')');
                        }
                        scope(');');
                    }
                    else if (unroll > 1) {
                        var prev = [];
                        var cur = [];
                        for (var j = 0; j < unroll; ++j) {
                            if (Array.isArray(VALUE)) {
                                cur.push(VALUE[j]);
                            }
                            else {
                                cur.push(scope.def(VALUE + '[' + j + ']'));
                            }
                            if (isBatchInnerLoop) {
                                prev.push(scope.def());
                            }
                        }
                        if (isBatchInnerLoop) {
                            scope('if(!', env.batchId, '||', prev.map(function (p, i) {
                                return p + '!==' + cur[i];
                            }).join('||'), '){', prev.map(function (p, i) {
                                return p + '=' + cur[i] + ';';
                            }).join(''));
                        }
                        scope(GL, '.uniform', infix, '(', LOCATION, ',', cur.join(','), ');');
                        if (isBatchInnerLoop) {
                            scope('}');
                        }
                    }
                    else {
                        check$1(!Array.isArray(VALUE), 'uniform value must not be an array');
                        if (isBatchInnerLoop) {
                            var prevS = scope.def();
                            scope('if(!', env.batchId, '||', prevS, '!==', VALUE, '){', prevS, '=', VALUE, ';');
                        }
                        scope(GL, '.uniform', infix, '(', LOCATION, ',', VALUE, ');');
                        if (isBatchInnerLoop) {
                            scope('}');
                        }
                    }
                }
            }
            function emitDraw(env, outer, inner, args) {
                var shared = env.shared;
                var GL = shared.gl;
                var DRAW_STATE = shared.draw;
                var drawOptions = args.draw;
                function emitElements() {
                    var defn = drawOptions.elements;
                    var ELEMENTS;
                    var scope = outer;
                    if (defn) {
                        if ((defn.contextDep && args.contextDynamic) || defn.propDep) {
                            scope = inner;
                        }
                        ELEMENTS = defn.append(env, scope);
                        if (drawOptions.elementsActive) {
                            scope('if(' + ELEMENTS + ')' +
                                GL + '.bindBuffer(' + GL_ELEMENT_ARRAY_BUFFER$2 + ',' + ELEMENTS + '.buffer.buffer);');
                        }
                    }
                    else {
                        ELEMENTS = scope.def();
                        scope(ELEMENTS, '=', DRAW_STATE, '.', S_ELEMENTS, ';', 'if(', ELEMENTS, '){', GL, '.bindBuffer(', GL_ELEMENT_ARRAY_BUFFER$2, ',', ELEMENTS, '.buffer.buffer);}', 'else if(', shared.vao, '.currentVAO){', ELEMENTS, '=', env.shared.elements + '.getElements(' + shared.vao, '.currentVAO.elements);', (!extVertexArrays ? 'if(' + ELEMENTS + ')' + GL + '.bindBuffer(' + GL_ELEMENT_ARRAY_BUFFER$2 + ',' + ELEMENTS + '.buffer.buffer);' : ''), '}');
                    }
                    return ELEMENTS;
                }
                function emitCount() {
                    var defn = drawOptions.count;
                    var COUNT;
                    var scope = outer;
                    if (defn) {
                        if ((defn.contextDep && args.contextDynamic) || defn.propDep) {
                            scope = inner;
                        }
                        COUNT = defn.append(env, scope);
                        check$1.optional(function () {
                            if (defn.MISSING) {
                                env.assert(outer, 'false', 'missing vertex count');
                            }
                            if (defn.DYNAMIC) {
                                env.assert(scope, COUNT + '>=0', 'missing vertex count');
                            }
                        });
                    }
                    else {
                        COUNT = scope.def(DRAW_STATE, '.', S_COUNT);
                        check$1.optional(function () {
                            env.assert(scope, COUNT + '>=0', 'missing vertex count');
                        });
                    }
                    return COUNT;
                }
                var ELEMENTS = emitElements();
                function emitValue(name) {
                    var defn = drawOptions[name];
                    if (defn) {
                        if ((defn.contextDep && args.contextDynamic) || defn.propDep) {
                            return defn.append(env, inner);
                        }
                        else {
                            return defn.append(env, outer);
                        }
                    }
                    else {
                        return outer.def(DRAW_STATE, '.', name);
                    }
                }
                var PRIMITIVE = emitValue(S_PRIMITIVE);
                var OFFSET = emitValue(S_OFFSET);
                var COUNT = emitCount();
                if (typeof COUNT === 'number') {
                    if (COUNT === 0) {
                        return;
                    }
                }
                else {
                    inner('if(', COUNT, '){');
                    inner.exit('}');
                }
                var INSTANCES, EXT_INSTANCING;
                if (extInstancing) {
                    INSTANCES = emitValue(S_INSTANCES);
                    EXT_INSTANCING = env.instancing;
                }
                var ELEMENT_TYPE = ELEMENTS + '.type';
                var elementsStatic = drawOptions.elements && isStatic(drawOptions.elements) && !drawOptions.vaoActive;
                function emitInstancing() {
                    function drawElements() {
                        inner(EXT_INSTANCING, '.drawElementsInstancedANGLE(', [
                            PRIMITIVE,
                            COUNT,
                            ELEMENT_TYPE,
                            OFFSET + '<<((' + ELEMENT_TYPE + '-' + GL_UNSIGNED_BYTE$8 + ')>>1)',
                            INSTANCES
                        ], ');');
                    }
                    function drawArrays() {
                        inner(EXT_INSTANCING, '.drawArraysInstancedANGLE(', [PRIMITIVE, OFFSET, COUNT, INSTANCES], ');');
                    }
                    if (ELEMENTS && ELEMENTS !== 'null') {
                        if (!elementsStatic) {
                            inner('if(', ELEMENTS, '){');
                            drawElements();
                            inner('}else{');
                            drawArrays();
                            inner('}');
                        }
                        else {
                            drawElements();
                        }
                    }
                    else {
                        drawArrays();
                    }
                }
                function emitRegular() {
                    function drawElements() {
                        inner(GL + '.drawElements(' + [
                            PRIMITIVE,
                            COUNT,
                            ELEMENT_TYPE,
                            OFFSET + '<<((' + ELEMENT_TYPE + '-' + GL_UNSIGNED_BYTE$8 + ')>>1)'
                        ] + ');');
                    }
                    function drawArrays() {
                        inner(GL + '.drawArrays(' + [PRIMITIVE, OFFSET, COUNT] + ');');
                    }
                    if (ELEMENTS && ELEMENTS !== 'null') {
                        if (!elementsStatic) {
                            inner('if(', ELEMENTS, '){');
                            drawElements();
                            inner('}else{');
                            drawArrays();
                            inner('}');
                        }
                        else {
                            drawElements();
                        }
                    }
                    else {
                        drawArrays();
                    }
                }
                if (extInstancing && (typeof INSTANCES !== 'number' || INSTANCES >= 0)) {
                    if (typeof INSTANCES === 'string') {
                        inner('if(', INSTANCES, '>0){');
                        emitInstancing();
                        inner('}else if(', INSTANCES, '<0){');
                        emitRegular();
                        inner('}');
                    }
                    else {
                        emitInstancing();
                    }
                }
                else {
                    emitRegular();
                }
            }
            function createBody(emitBody, parentEnv, args, program, count) {
                var env = createREGLEnvironment();
                var scope = env.proc('body', count);
                check$1.optional(function () {
                    env.commandStr = parentEnv.commandStr;
                    env.command = env.link(parentEnv.commandStr);
                });
                if (extInstancing) {
                    env.instancing = scope.def(env.shared.extensions, '.angle_instanced_arrays');
                }
                emitBody(env, scope, args, program);
                return env.compile().body;
            }
            // ===================================================
            // ===================================================
            // DRAW PROC
            // ===================================================
            // ===================================================
            function emitDrawBody(env, draw, args, program) {
                injectExtensions(env, draw);
                if (args.useVAO) {
                    if (args.drawVAO) {
                        draw(env.shared.vao, '.setVAO(', args.drawVAO.append(env, draw), ');');
                    }
                    else {
                        draw(env.shared.vao, '.setVAO(', env.shared.vao, '.targetVAO);');
                    }
                }
                else {
                    draw(env.shared.vao, '.setVAO(null);');
                    emitAttributes(env, draw, args, program.attributes, function () {
                        return true;
                    });
                }
                emitUniforms(env, draw, args, program.uniforms, function () {
                    return true;
                }, false);
                emitDraw(env, draw, draw, args);
            }
            function emitDrawProc(env, args) {
                var draw = env.proc('draw', 1);
                injectExtensions(env, draw);
                emitContext(env, draw, args.context);
                emitPollFramebuffer(env, draw, args.framebuffer);
                emitPollState(env, draw, args);
                emitSetOptions(env, draw, args.state);
                emitProfile(env, draw, args, false, true);
                var program = args.shader.progVar.append(env, draw);
                draw(env.shared.gl, '.useProgram(', program, '.program);');
                if (args.shader.program) {
                    emitDrawBody(env, draw, args, args.shader.program);
                }
                else {
                    draw(env.shared.vao, '.setVAO(null);');
                    var drawCache = env.global.def('{}');
                    var PROG_ID = draw.def(program, '.id');
                    var CACHED_PROC = draw.def(drawCache, '[', PROG_ID, ']');
                    draw(env.cond(CACHED_PROC)
                        .then(CACHED_PROC, '.call(this,a0);')
                        .else(CACHED_PROC, '=', drawCache, '[', PROG_ID, ']=', env.link(function (program) {
                        return createBody(emitDrawBody, env, args, program, 1);
                    }), '(', program, ');', CACHED_PROC, '.call(this,a0);'));
                }
                if (Object.keys(args.state).length > 0) {
                    draw(env.shared.current, '.dirty=true;');
                }
                if (env.shared.vao) {
                    draw(env.shared.vao, '.setVAO(null);');
                }
            }
            // ===================================================
            // ===================================================
            // BATCH PROC
            // ===================================================
            // ===================================================
            function emitBatchDynamicShaderBody(env, scope, args, program) {
                env.batchId = 'a1';
                injectExtensions(env, scope);
                function all() {
                    return true;
                }
                emitAttributes(env, scope, args, program.attributes, all);
                emitUniforms(env, scope, args, program.uniforms, all, false);
                emitDraw(env, scope, scope, args);
            }
            function emitBatchBody(env, scope, args, program) {
                injectExtensions(env, scope);
                var contextDynamic = args.contextDep;
                var BATCH_ID = scope.def();
                var PROP_LIST = 'a0';
                var NUM_PROPS = 'a1';
                var PROPS = scope.def();
                env.shared.props = PROPS;
                env.batchId = BATCH_ID;
                var outer = env.scope();
                var inner = env.scope();
                scope(outer.entry, 'for(', BATCH_ID, '=0;', BATCH_ID, '<', NUM_PROPS, ';++', BATCH_ID, '){', PROPS, '=', PROP_LIST, '[', BATCH_ID, '];', inner, '}', outer.exit);
                function isInnerDefn(defn) {
                    return ((defn.contextDep && contextDynamic) || defn.propDep);
                }
                function isOuterDefn(defn) {
                    return !isInnerDefn(defn);
                }
                if (args.needsContext) {
                    emitContext(env, inner, args.context);
                }
                if (args.needsFramebuffer) {
                    emitPollFramebuffer(env, inner, args.framebuffer);
                }
                emitSetOptions(env, inner, args.state, isInnerDefn);
                if (args.profile && isInnerDefn(args.profile)) {
                    emitProfile(env, inner, args, false, true);
                }
                if (!program) {
                    var progCache = env.global.def('{}');
                    var PROGRAM = args.shader.progVar.append(env, inner);
                    var PROG_ID = inner.def(PROGRAM, '.id');
                    var CACHED_PROC = inner.def(progCache, '[', PROG_ID, ']');
                    inner(env.shared.gl, '.useProgram(', PROGRAM, '.program);', 'if(!', CACHED_PROC, '){', CACHED_PROC, '=', progCache, '[', PROG_ID, ']=', env.link(function (program) {
                        return createBody(emitBatchDynamicShaderBody, env, args, program, 2);
                    }), '(', PROGRAM, ');}', CACHED_PROC, '.call(this,a0[', BATCH_ID, '],', BATCH_ID, ');');
                }
                else {
                    if (args.useVAO) {
                        if (args.drawVAO) {
                            if (isInnerDefn(args.drawVAO)) {
                                // vao is a prop
                                inner(env.shared.vao, '.setVAO(', args.drawVAO.append(env, inner), ');');
                            }
                            else {
                                // vao is invariant
                                outer(env.shared.vao, '.setVAO(', args.drawVAO.append(env, outer), ');');
                            }
                        }
                        else {
                            // scoped vao binding
                            outer(env.shared.vao, '.setVAO(', env.shared.vao, '.targetVAO);');
                        }
                    }
                    else {
                        outer(env.shared.vao, '.setVAO(null);');
                        emitAttributes(env, outer, args, program.attributes, isOuterDefn);
                        emitAttributes(env, inner, args, program.attributes, isInnerDefn);
                    }
                    emitUniforms(env, outer, args, program.uniforms, isOuterDefn, false);
                    emitUniforms(env, inner, args, program.uniforms, isInnerDefn, true);
                    emitDraw(env, outer, inner, args);
                }
            }
            function emitBatchProc(env, args) {
                var batch = env.proc('batch', 2);
                env.batchId = '0';
                injectExtensions(env, batch);
                // Check if any context variables depend on props
                var contextDynamic = false;
                var needsContext = true;
                Object.keys(args.context).forEach(function (name) {
                    contextDynamic = contextDynamic || args.context[name].propDep;
                });
                if (!contextDynamic) {
                    emitContext(env, batch, args.context);
                    needsContext = false;
                }
                // framebuffer state affects framebufferWidth/height context vars
                var framebuffer = args.framebuffer;
                var needsFramebuffer = false;
                if (framebuffer) {
                    if (framebuffer.propDep) {
                        contextDynamic = needsFramebuffer = true;
                    }
                    else if (framebuffer.contextDep && contextDynamic) {
                        needsFramebuffer = true;
                    }
                    if (!needsFramebuffer) {
                        emitPollFramebuffer(env, batch, framebuffer);
                    }
                }
                else {
                    emitPollFramebuffer(env, batch, null);
                }
                // viewport is weird because it can affect context vars
                if (args.state.viewport && args.state.viewport.propDep) {
                    contextDynamic = true;
                }
                function isInnerDefn(defn) {
                    return (defn.contextDep && contextDynamic) || defn.propDep;
                }
                // set webgl options
                emitPollState(env, batch, args);
                emitSetOptions(env, batch, args.state, function (defn) {
                    return !isInnerDefn(defn);
                });
                if (!args.profile || !isInnerDefn(args.profile)) {
                    emitProfile(env, batch, args, false, 'a1');
                }
                // Save these values to args so that the batch body routine can use them
                args.contextDep = contextDynamic;
                args.needsContext = needsContext;
                args.needsFramebuffer = needsFramebuffer;
                // determine if shader is dynamic
                var progDefn = args.shader.progVar;
                if ((progDefn.contextDep && contextDynamic) || progDefn.propDep) {
                    emitBatchBody(env, batch, args, null);
                }
                else {
                    var PROGRAM = progDefn.append(env, batch);
                    batch(env.shared.gl, '.useProgram(', PROGRAM, '.program);');
                    if (args.shader.program) {
                        emitBatchBody(env, batch, args, args.shader.program);
                    }
                    else {
                        batch(env.shared.vao, '.setVAO(null);');
                        var batchCache = env.global.def('{}');
                        var PROG_ID = batch.def(PROGRAM, '.id');
                        var CACHED_PROC = batch.def(batchCache, '[', PROG_ID, ']');
                        batch(env.cond(CACHED_PROC)
                            .then(CACHED_PROC, '.call(this,a0,a1);')
                            .else(CACHED_PROC, '=', batchCache, '[', PROG_ID, ']=', env.link(function (program) {
                            return createBody(emitBatchBody, env, args, program, 2);
                        }), '(', PROGRAM, ');', CACHED_PROC, '.call(this,a0,a1);'));
                    }
                }
                if (Object.keys(args.state).length > 0) {
                    batch(env.shared.current, '.dirty=true;');
                }
                if (env.shared.vao) {
                    batch(env.shared.vao, '.setVAO(null);');
                }
            }
            // ===================================================
            // ===================================================
            // SCOPE COMMAND
            // ===================================================
            // ===================================================
            function emitScopeProc(env, args) {
                var scope = env.proc('scope', 3);
                env.batchId = 'a2';
                var shared = env.shared;
                var CURRENT_STATE = shared.current;
                emitContext(env, scope, args.context);
                if (args.framebuffer) {
                    args.framebuffer.append(env, scope);
                }
                sortState(Object.keys(args.state)).forEach(function (name) {
                    var defn = args.state[name];
                    var value = defn.append(env, scope);
                    if (isArrayLike(value)) {
                        value.forEach(function (v, i) {
                            scope.set(env.next[name], '[' + i + ']', v);
                        });
                    }
                    else {
                        scope.set(shared.next, '.' + name, value);
                    }
                });
                emitProfile(env, scope, args, true, true);
                [S_ELEMENTS, S_OFFSET, S_COUNT, S_INSTANCES, S_PRIMITIVE].forEach(function (opt) {
                    var variable = args.draw[opt];
                    if (!variable) {
                        return;
                    }
                    scope.set(shared.draw, '.' + opt, '' + variable.append(env, scope));
                });
                Object.keys(args.uniforms).forEach(function (opt) {
                    var value = args.uniforms[opt].append(env, scope);
                    if (Array.isArray(value)) {
                        value = '[' + value.join() + ']';
                    }
                    scope.set(shared.uniforms, '[' + stringStore.id(opt) + ']', value);
                });
                Object.keys(args.attributes).forEach(function (name) {
                    var record = args.attributes[name].append(env, scope);
                    var scopeAttrib = env.scopeAttrib(name);
                    Object.keys(new AttributeRecord()).forEach(function (prop) {
                        scope.set(scopeAttrib, '.' + prop, record[prop]);
                    });
                });
                if (args.scopeVAO) {
                    scope.set(shared.vao, '.targetVAO', args.scopeVAO.append(env, scope));
                }
                function saveShader(name) {
                    var shader = args.shader[name];
                    if (shader) {
                        scope.set(shared.shader, '.' + name, shader.append(env, scope));
                    }
                }
                saveShader(S_VERT);
                saveShader(S_FRAG);
                if (Object.keys(args.state).length > 0) {
                    scope(CURRENT_STATE, '.dirty=true;');
                    scope.exit(CURRENT_STATE, '.dirty=true;');
                }
                scope('a1(', env.shared.context, ',a0,', env.batchId, ');');
            }
            function isDynamicObject(object) {
                if (typeof object !== 'object' || isArrayLike(object)) {
                    return;
                }
                var props = Object.keys(object);
                for (var i = 0; i < props.length; ++i) {
                    if (dynamic.isDynamic(object[props[i]])) {
                        return true;
                    }
                }
                return false;
            }
            function splatObject(env, options, name) {
                var object = options.static[name];
                if (!object || !isDynamicObject(object)) {
                    return;
                }
                var globals = env.global;
                var keys = Object.keys(object);
                var thisDep = false;
                var contextDep = false;
                var propDep = false;
                var objectRef = env.global.def('{}');
                keys.forEach(function (key) {
                    var value = object[key];
                    if (dynamic.isDynamic(value)) {
                        if (typeof value === 'function') {
                            value = object[key] = dynamic.unbox(value);
                        }
                        var deps = createDynamicDecl(value, null);
                        thisDep = thisDep || deps.thisDep;
                        propDep = propDep || deps.propDep;
                        contextDep = contextDep || deps.contextDep;
                    }
                    else {
                        globals(objectRef, '.', key, '=');
                        switch (typeof value) {
                            case 'number':
                                globals(value);
                                break;
                            case 'string':
                                globals('"', value, '"');
                                break;
                            case 'object':
                                if (Array.isArray(value)) {
                                    globals('[', value.join(), ']');
                                }
                                break;
                            default:
                                globals(env.link(value));
                                break;
                        }
                        globals(';');
                    }
                });
                function appendBlock(env, block) {
                    keys.forEach(function (key) {
                        var value = object[key];
                        if (!dynamic.isDynamic(value)) {
                            return;
                        }
                        var ref = env.invoke(block, value);
                        block(objectRef, '.', key, '=', ref, ';');
                    });
                }
                options.dynamic[name] = new dynamic.DynamicVariable(DYN_THUNK, {
                    thisDep: thisDep,
                    contextDep: contextDep,
                    propDep: propDep,
                    ref: objectRef,
                    append: appendBlock
                });
                delete options.static[name];
            }
            // ===========================================================================
            // ===========================================================================
            // MAIN DRAW COMMAND
            // ===========================================================================
            // ===========================================================================
            function compileCommand(options, attributes, uniforms, context, stats) {
                var env = createREGLEnvironment();
                // link stats, so that we can easily access it in the program.
                env.stats = env.link(stats);
                // splat options and attributes to allow for dynamic nested properties
                Object.keys(attributes.static).forEach(function (key) {
                    splatObject(env, attributes, key);
                });
                NESTED_OPTIONS.forEach(function (name) {
                    splatObject(env, options, name);
                });
                var args = parseArguments(options, attributes, uniforms, context, env);
                emitDrawProc(env, args);
                emitScopeProc(env, args);
                emitBatchProc(env, args);
                return extend(env.compile(), {
                    destroy: function () {
                        args.shader.program.destroy();
                    }
                });
            }
            // ===========================================================================
            // ===========================================================================
            // POLL / REFRESH
            // ===========================================================================
            // ===========================================================================
            return {
                next: nextState,
                current: currentState,
                procs: (function () {
                    var env = createREGLEnvironment();
                    var poll = env.proc('poll');
                    var refresh = env.proc('refresh');
                    var common = env.block();
                    poll(common);
                    refresh(common);
                    var shared = env.shared;
                    var GL = shared.gl;
                    var NEXT_STATE = shared.next;
                    var CURRENT_STATE = shared.current;
                    common(CURRENT_STATE, '.dirty=false;');
                    emitPollFramebuffer(env, poll);
                    emitPollFramebuffer(env, refresh, null, true);
                    // Refresh updates all attribute state changes
                    var INSTANCING;
                    if (extInstancing) {
                        INSTANCING = env.link(extInstancing);
                    }
                    // update vertex array bindings
                    if (extensions.oes_vertex_array_object) {
                        refresh(env.link(extensions.oes_vertex_array_object), '.bindVertexArrayOES(null);');
                    }
                    for (var i = 0; i < limits.maxAttributes; ++i) {
                        var BINDING = refresh.def(shared.attributes, '[', i, ']');
                        var ifte = env.cond(BINDING, '.buffer');
                        ifte.then(GL, '.enableVertexAttribArray(', i, ');', GL, '.bindBuffer(', GL_ARRAY_BUFFER$2, ',', BINDING, '.buffer.buffer);', GL, '.vertexAttribPointer(', i, ',', BINDING, '.size,', BINDING, '.type,', BINDING, '.normalized,', BINDING, '.stride,', BINDING, '.offset);').else(GL, '.disableVertexAttribArray(', i, ');', GL, '.vertexAttrib4f(', i, ',', BINDING, '.x,', BINDING, '.y,', BINDING, '.z,', BINDING, '.w);', BINDING, '.buffer=null;');
                        refresh(ifte);
                        if (extInstancing) {
                            refresh(INSTANCING, '.vertexAttribDivisorANGLE(', i, ',', BINDING, '.divisor);');
                        }
                    }
                    refresh(env.shared.vao, '.currentVAO=null;', env.shared.vao, '.setVAO(', env.shared.vao, '.targetVAO);');
                    Object.keys(GL_FLAGS).forEach(function (flag) {
                        var cap = GL_FLAGS[flag];
                        var NEXT = common.def(NEXT_STATE, '.', flag);
                        var block = env.block();
                        block('if(', NEXT, '){', GL, '.enable(', cap, ')}else{', GL, '.disable(', cap, ')}', CURRENT_STATE, '.', flag, '=', NEXT, ';');
                        refresh(block);
                        poll('if(', NEXT, '!==', CURRENT_STATE, '.', flag, '){', block, '}');
                    });
                    Object.keys(GL_VARIABLES).forEach(function (name) {
                        var func = GL_VARIABLES[name];
                        var init = currentState[name];
                        var NEXT, CURRENT;
                        var block = env.block();
                        block(GL, '.', func, '(');
                        if (isArrayLike(init)) {
                            var n = init.length;
                            NEXT = env.global.def(NEXT_STATE, '.', name);
                            CURRENT = env.global.def(CURRENT_STATE, '.', name);
                            block(loop(n, function (i) {
                                return NEXT + '[' + i + ']';
                            }), ');', loop(n, function (i) {
                                return CURRENT + '[' + i + ']=' + NEXT + '[' + i + '];';
                            }).join(''));
                            poll('if(', loop(n, function (i) {
                                return NEXT + '[' + i + ']!==' + CURRENT + '[' + i + ']';
                            }).join('||'), '){', block, '}');
                        }
                        else {
                            NEXT = common.def(NEXT_STATE, '.', name);
                            CURRENT = common.def(CURRENT_STATE, '.', name);
                            block(NEXT, ');', CURRENT_STATE, '.', name, '=', NEXT, ';');
                            poll('if(', NEXT, '!==', CURRENT, '){', block, '}');
                        }
                        refresh(block);
                    });
                    return env.compile();
                })(),
                compile: compileCommand
            };
        }
        function stats() {
            return {
                vaoCount: 0,
                bufferCount: 0,
                elementsCount: 0,
                framebufferCount: 0,
                shaderCount: 0,
                textureCount: 0,
                cubeCount: 0,
                renderbufferCount: 0,
                maxTextureUnits: 0
            };
        }
        var GL_QUERY_RESULT_EXT = 0x8866;
        var GL_QUERY_RESULT_AVAILABLE_EXT = 0x8867;
        var GL_TIME_ELAPSED_EXT = 0x88BF;
        var createTimer = function (gl, extensions) {
            if (!extensions.ext_disjoint_timer_query) {
                return null;
            }
            // QUERY POOL BEGIN
            var queryPool = [];
            function allocQuery() {
                return queryPool.pop() || extensions.ext_disjoint_timer_query.createQueryEXT();
            }
            function freeQuery(query) {
                queryPool.push(query);
            }
            // QUERY POOL END
            var pendingQueries = [];
            function beginQuery(stats) {
                var query = allocQuery();
                extensions.ext_disjoint_timer_query.beginQueryEXT(GL_TIME_ELAPSED_EXT, query);
                pendingQueries.push(query);
                pushScopeStats(pendingQueries.length - 1, pendingQueries.length, stats);
            }
            function endQuery() {
                extensions.ext_disjoint_timer_query.endQueryEXT(GL_TIME_ELAPSED_EXT);
            }
            //
            // Pending stats pool.
            //
            function PendingStats() {
                this.startQueryIndex = -1;
                this.endQueryIndex = -1;
                this.sum = 0;
                this.stats = null;
            }
            var pendingStatsPool = [];
            function allocPendingStats() {
                return pendingStatsPool.pop() || new PendingStats();
            }
            function freePendingStats(pendingStats) {
                pendingStatsPool.push(pendingStats);
            }
            // Pending stats pool end
            var pendingStats = [];
            function pushScopeStats(start, end, stats) {
                var ps = allocPendingStats();
                ps.startQueryIndex = start;
                ps.endQueryIndex = end;
                ps.sum = 0;
                ps.stats = stats;
                pendingStats.push(ps);
            }
            // we should call this at the beginning of the frame,
            // in order to update gpuTime
            var timeSum = [];
            var queryPtr = [];
            function update() {
                var ptr, i;
                var n = pendingQueries.length;
                if (n === 0) {
                    return;
                }
                // Reserve space
                queryPtr.length = Math.max(queryPtr.length, n + 1);
                timeSum.length = Math.max(timeSum.length, n + 1);
                timeSum[0] = 0;
                queryPtr[0] = 0;
                // Update all pending timer queries
                var queryTime = 0;
                ptr = 0;
                for (i = 0; i < pendingQueries.length; ++i) {
                    var query = pendingQueries[i];
                    if (extensions.ext_disjoint_timer_query.getQueryObjectEXT(query, GL_QUERY_RESULT_AVAILABLE_EXT)) {
                        queryTime += extensions.ext_disjoint_timer_query.getQueryObjectEXT(query, GL_QUERY_RESULT_EXT);
                        freeQuery(query);
                    }
                    else {
                        pendingQueries[ptr++] = query;
                    }
                    timeSum[i + 1] = queryTime;
                    queryPtr[i + 1] = ptr;
                }
                pendingQueries.length = ptr;
                // Update all pending stat queries
                ptr = 0;
                for (i = 0; i < pendingStats.length; ++i) {
                    var stats = pendingStats[i];
                    var start = stats.startQueryIndex;
                    var end = stats.endQueryIndex;
                    stats.sum += timeSum[end] - timeSum[start];
                    var startPtr = queryPtr[start];
                    var endPtr = queryPtr[end];
                    if (endPtr === startPtr) {
                        stats.stats.gpuTime += stats.sum / 1e6;
                        freePendingStats(stats);
                    }
                    else {
                        stats.startQueryIndex = startPtr;
                        stats.endQueryIndex = endPtr;
                        pendingStats[ptr++] = stats;
                    }
                }
                pendingStats.length = ptr;
            }
            return {
                beginQuery: beginQuery,
                endQuery: endQuery,
                pushScopeStats: pushScopeStats,
                update: update,
                getNumPendingQueries: function () {
                    return pendingQueries.length;
                },
                clear: function () {
                    queryPool.push.apply(queryPool, pendingQueries);
                    for (var i = 0; i < queryPool.length; i++) {
                        extensions.ext_disjoint_timer_query.deleteQueryEXT(queryPool[i]);
                    }
                    pendingQueries.length = 0;
                    queryPool.length = 0;
                },
                restore: function () {
                    pendingQueries.length = 0;
                    queryPool.length = 0;
                }
            };
        };
        var GL_COLOR_BUFFER_BIT = 16384;
        var GL_DEPTH_BUFFER_BIT = 256;
        var GL_STENCIL_BUFFER_BIT = 1024;
        var GL_ARRAY_BUFFER = 34962;
        var CONTEXT_LOST_EVENT = 'webglcontextlost';
        var CONTEXT_RESTORED_EVENT = 'webglcontextrestored';
        var DYN_PROP = 1;
        var DYN_CONTEXT = 2;
        var DYN_STATE = 3;
        function find(haystack, needle) {
            for (var i = 0; i < haystack.length; ++i) {
                if (haystack[i] === needle) {
                    return i;
                }
            }
            return -1;
        }
        function wrapREGL(args) {
            var config = parseArgs(args);
            if (!config) {
                return null;
            }
            var gl = config.gl;
            var glAttributes = gl.getContextAttributes();
            var contextLost = gl.isContextLost();
            var extensionState = createExtensionCache(gl, config);
            if (!extensionState) {
                return null;
            }
            var stringStore = createStringStore();
            var stats$$1 = stats();
            var extensions = extensionState.extensions;
            var timer = createTimer(gl, extensions);
            var START_TIME = clock();
            var WIDTH = gl.drawingBufferWidth;
            var HEIGHT = gl.drawingBufferHeight;
            var contextState = {
                tick: 0,
                time: 0,
                viewportWidth: WIDTH,
                viewportHeight: HEIGHT,
                framebufferWidth: WIDTH,
                framebufferHeight: HEIGHT,
                drawingBufferWidth: WIDTH,
                drawingBufferHeight: HEIGHT,
                pixelRatio: config.pixelRatio
            };
            var uniformState = {};
            var drawState = {
                elements: null,
                primitive: 4, // GL_TRIANGLES
                count: -1,
                offset: 0,
                instances: -1
            };
            var limits = wrapLimits(gl, extensions);
            var bufferState = wrapBufferState(gl, stats$$1, config, destroyBuffer);
            var elementState = wrapElementsState(gl, extensions, bufferState, stats$$1);
            var attributeState = wrapAttributeState(gl, extensions, limits, stats$$1, bufferState, elementState, drawState);
            function destroyBuffer(buffer) {
                return attributeState.destroyBuffer(buffer);
            }
            var shaderState = wrapShaderState(gl, stringStore, stats$$1, config);
            var textureState = createTextureSet(gl, extensions, limits, function () { core.procs.poll(); }, contextState, stats$$1, config);
            var renderbufferState = wrapRenderbuffers(gl, extensions, limits, stats$$1, config);
            var framebufferState = wrapFBOState(gl, extensions, limits, textureState, renderbufferState, stats$$1);
            var core = reglCore(gl, stringStore, extensions, limits, bufferState, elementState, textureState, framebufferState, uniformState, attributeState, shaderState, drawState, contextState, timer, config);
            var readPixels = wrapReadPixels(gl, framebufferState, core.procs.poll, contextState, glAttributes, extensions, limits);
            var nextState = core.next;
            var canvas = gl.canvas;
            var rafCallbacks = [];
            var lossCallbacks = [];
            var restoreCallbacks = [];
            var destroyCallbacks = [config.onDestroy];
            var activeRAF = null;
            function handleRAF() {
                if (rafCallbacks.length === 0) {
                    if (timer) {
                        timer.update();
                    }
                    activeRAF = null;
                    return;
                }
                // schedule next animation frame
                activeRAF = raf.next(handleRAF);
                // poll for changes
                poll();
                // fire a callback for all pending rafs
                for (var i = rafCallbacks.length - 1; i >= 0; --i) {
                    var cb = rafCallbacks[i];
                    if (cb) {
                        cb(contextState, null, 0);
                    }
                }
                // flush all pending webgl calls
                gl.flush();
                // poll GPU timers *after* gl.flush so we don't delay command dispatch
                if (timer) {
                    timer.update();
                }
            }
            function startRAF() {
                if (!activeRAF && rafCallbacks.length > 0) {
                    activeRAF = raf.next(handleRAF);
                }
            }
            function stopRAF() {
                if (activeRAF) {
                    raf.cancel(handleRAF);
                    activeRAF = null;
                }
            }
            function handleContextLoss(event) {
                event.preventDefault();
                // set context lost flag
                contextLost = true;
                // pause request animation frame
                stopRAF();
                // lose context
                lossCallbacks.forEach(function (cb) {
                    cb();
                });
            }
            function handleContextRestored(event) {
                // clear error code
                gl.getError();
                // clear context lost flag
                contextLost = false;
                // refresh state
                extensionState.restore();
                shaderState.restore();
                bufferState.restore();
                textureState.restore();
                renderbufferState.restore();
                framebufferState.restore();
                attributeState.restore();
                if (timer) {
                    timer.restore();
                }
                // refresh state
                core.procs.refresh();
                // restart RAF
                startRAF();
                // restore context
                restoreCallbacks.forEach(function (cb) {
                    cb();
                });
            }
            if (canvas) {
                canvas.addEventListener(CONTEXT_LOST_EVENT, handleContextLoss, false);
                canvas.addEventListener(CONTEXT_RESTORED_EVENT, handleContextRestored, false);
            }
            function destroy() {
                rafCallbacks.length = 0;
                stopRAF();
                if (canvas) {
                    canvas.removeEventListener(CONTEXT_LOST_EVENT, handleContextLoss);
                    canvas.removeEventListener(CONTEXT_RESTORED_EVENT, handleContextRestored);
                }
                shaderState.clear();
                framebufferState.clear();
                renderbufferState.clear();
                attributeState.clear();
                textureState.clear();
                elementState.clear();
                bufferState.clear();
                if (timer) {
                    timer.clear();
                }
                destroyCallbacks.forEach(function (cb) {
                    cb();
                });
            }
            function compileProcedure(options) {
                check$1(!!options, 'invalid args to regl({...})');
                check$1.type(options, 'object', 'invalid args to regl({...})');
                function flattenNestedOptions(options) {
                    var result = extend({}, options);
                    delete result.uniforms;
                    delete result.attributes;
                    delete result.context;
                    delete result.vao;
                    if ('stencil' in result && result.stencil.op) {
                        result.stencil.opBack = result.stencil.opFront = result.stencil.op;
                        delete result.stencil.op;
                    }
                    function merge(name) {
                        if (name in result) {
                            var child = result[name];
                            delete result[name];
                            Object.keys(child).forEach(function (prop) {
                                result[name + '.' + prop] = child[prop];
                            });
                        }
                    }
                    merge('blend');
                    merge('depth');
                    merge('cull');
                    merge('stencil');
                    merge('polygonOffset');
                    merge('scissor');
                    merge('sample');
                    if ('vao' in options) {
                        result.vao = options.vao;
                    }
                    return result;
                }
                function separateDynamic(object, useArrays) {
                    var staticItems = {};
                    var dynamicItems = {};
                    Object.keys(object).forEach(function (option) {
                        var value = object[option];
                        if (dynamic.isDynamic(value)) {
                            dynamicItems[option] = dynamic.unbox(value, option);
                            return;
                        }
                        else if (useArrays && Array.isArray(value)) {
                            for (var i = 0; i < value.length; ++i) {
                                if (dynamic.isDynamic(value[i])) {
                                    dynamicItems[option] = dynamic.unbox(value, option);
                                    return;
                                }
                            }
                        }
                        staticItems[option] = value;
                    });
                    return {
                        dynamic: dynamicItems,
                        static: staticItems
                    };
                }
                // Treat context variables separate from other dynamic variables
                var context = separateDynamic(options.context || {}, true);
                var uniforms = separateDynamic(options.uniforms || {}, true);
                var attributes = separateDynamic(options.attributes || {}, false);
                var opts = separateDynamic(flattenNestedOptions(options), false);
                var stats$$1 = {
                    gpuTime: 0.0,
                    cpuTime: 0.0,
                    count: 0
                };
                var compiled = core.compile(opts, attributes, uniforms, context, stats$$1);
                var draw = compiled.draw;
                var batch = compiled.batch;
                var scope = compiled.scope;
                // FIXME: we should modify code generation for batch commands so this
                // isn't necessary
                var EMPTY_ARRAY = [];
                function reserve(count) {
                    while (EMPTY_ARRAY.length < count) {
                        EMPTY_ARRAY.push(null);
                    }
                    return EMPTY_ARRAY;
                }
                function REGLCommand(args, body) {
                    var i;
                    if (contextLost) {
                        check$1.raise('context lost');
                    }
                    if (typeof args === 'function') {
                        return scope.call(this, null, args, 0);
                    }
                    else if (typeof body === 'function') {
                        if (typeof args === 'number') {
                            for (i = 0; i < args; ++i) {
                                scope.call(this, null, body, i);
                            }
                        }
                        else if (Array.isArray(args)) {
                            for (i = 0; i < args.length; ++i) {
                                scope.call(this, args[i], body, i);
                            }
                        }
                        else {
                            return scope.call(this, args, body, 0);
                        }
                    }
                    else if (typeof args === 'number') {
                        if (args > 0) {
                            return batch.call(this, reserve(args | 0), args | 0);
                        }
                    }
                    else if (Array.isArray(args)) {
                        if (args.length) {
                            return batch.call(this, args, args.length);
                        }
                    }
                    else {
                        return draw.call(this, args);
                    }
                }
                return extend(REGLCommand, {
                    stats: stats$$1,
                    destroy: function () {
                        compiled.destroy();
                    }
                });
            }
            var setFBO = framebufferState.setFBO = compileProcedure({
                framebuffer: dynamic.define.call(null, DYN_PROP, 'framebuffer')
            });
            function clearImpl(_, options) {
                var clearFlags = 0;
                core.procs.poll();
                var c = options.color;
                if (c) {
                    gl.clearColor(+c[0] || 0, +c[1] || 0, +c[2] || 0, +c[3] || 0);
                    clearFlags |= GL_COLOR_BUFFER_BIT;
                }
                if ('depth' in options) {
                    gl.clearDepth(+options.depth);
                    clearFlags |= GL_DEPTH_BUFFER_BIT;
                }
                if ('stencil' in options) {
                    gl.clearStencil(options.stencil | 0);
                    clearFlags |= GL_STENCIL_BUFFER_BIT;
                }
                check$1(!!clearFlags, 'called regl.clear with no buffer specified');
                gl.clear(clearFlags);
            }
            function clear(options) {
                check$1(typeof options === 'object' && options, 'regl.clear() takes an object as input');
                if ('framebuffer' in options) {
                    if (options.framebuffer &&
                        options.framebuffer_reglType === 'framebufferCube') {
                        for (var i = 0; i < 6; ++i) {
                            setFBO(extend({
                                framebuffer: options.framebuffer.faces[i]
                            }, options), clearImpl);
                        }
                    }
                    else {
                        setFBO(options, clearImpl);
                    }
                }
                else {
                    clearImpl(null, options);
                }
            }
            function frame(cb) {
                check$1.type(cb, 'function', 'regl.frame() callback must be a function');
                rafCallbacks.push(cb);
                function cancel() {
                    // FIXME:  should we check something other than equals cb here?
                    // what if a user calls frame twice with the same callback...
                    //
                    var i = find(rafCallbacks, cb);
                    check$1(i >= 0, 'cannot cancel a frame twice');
                    function pendingCancel() {
                        var index = find(rafCallbacks, pendingCancel);
                        rafCallbacks[index] = rafCallbacks[rafCallbacks.length - 1];
                        rafCallbacks.length -= 1;
                        if (rafCallbacks.length <= 0) {
                            stopRAF();
                        }
                    }
                    rafCallbacks[i] = pendingCancel;
                }
                startRAF();
                return {
                    cancel: cancel
                };
            }
            // poll viewport
            function pollViewport() {
                var viewport = nextState.viewport;
                var scissorBox = nextState.scissor_box;
                viewport[0] = viewport[1] = scissorBox[0] = scissorBox[1] = 0;
                contextState.viewportWidth =
                    contextState.framebufferWidth =
                        contextState.drawingBufferWidth =
                            viewport[2] =
                                scissorBox[2] = gl.drawingBufferWidth;
                contextState.viewportHeight =
                    contextState.framebufferHeight =
                        contextState.drawingBufferHeight =
                            viewport[3] =
                                scissorBox[3] = gl.drawingBufferHeight;
            }
            function poll() {
                contextState.tick += 1;
                contextState.time = now();
                pollViewport();
                core.procs.poll();
            }
            function refresh() {
                textureState.refresh();
                pollViewport();
                core.procs.refresh();
                if (timer) {
                    timer.update();
                }
            }
            function now() {
                return (clock() - START_TIME) / 1000.0;
            }
            refresh();
            function addListener(event, callback) {
                check$1.type(callback, 'function', 'listener callback must be a function');
                var callbacks;
                switch (event) {
                    case 'frame':
                        return frame(callback);
                    case 'lost':
                        callbacks = lossCallbacks;
                        break;
                    case 'restore':
                        callbacks = restoreCallbacks;
                        break;
                    case 'destroy':
                        callbacks = destroyCallbacks;
                        break;
                    default:
                        check$1.raise('invalid event, must be one of frame,lost,restore,destroy');
                }
                callbacks.push(callback);
                return {
                    cancel: function () {
                        for (var i = 0; i < callbacks.length; ++i) {
                            if (callbacks[i] === callback) {
                                callbacks[i] = callbacks[callbacks.length - 1];
                                callbacks.pop();
                                return;
                            }
                        }
                    }
                };
            }
            var regl = extend(compileProcedure, {
                // Clear current FBO
                clear: clear,
                // Short cuts for dynamic variables
                prop: dynamic.define.bind(null, DYN_PROP),
                context: dynamic.define.bind(null, DYN_CONTEXT),
                this: dynamic.define.bind(null, DYN_STATE),
                // executes an empty draw command
                draw: compileProcedure({}),
                // Resources
                buffer: function (options) {
                    return bufferState.create(options, GL_ARRAY_BUFFER, false, false);
                },
                elements: function (options) {
                    return elementState.create(options, false);
                },
                texture: textureState.create2D,
                cube: textureState.createCube,
                renderbuffer: renderbufferState.create,
                framebuffer: framebufferState.create,
                framebufferCube: framebufferState.createCube,
                vao: attributeState.createVAO,
                // Expose context attributes
                attributes: glAttributes,
                // Frame rendering
                frame: frame,
                on: addListener,
                // System limits
                limits: limits,
                hasExtension: function (name) {
                    return limits.extensions.indexOf(name.toLowerCase()) >= 0;
                },
                // Read pixels
                read: readPixels,
                // Destroy regl and all associated resources
                destroy: destroy,
                // Direct GL state manipulation
                _gl: gl,
                _refresh: refresh,
                poll: function () {
                    poll();
                    if (timer) {
                        timer.update();
                    }
                },
                // Current time
                now: now,
                // regl Statistics Information
                stats: stats$$1
            });
            config.onDone(null, regl);
            return regl;
        }
        return wrapREGL;
    })));
},
643: /* models/glyphs/webgl/dash_cache.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.normalize_dash_pattern = normalize_dash_pattern;
    const math_1 = require(644) /* ./utils/math */;
    const logging_1 = require(11) /* ../../../core/logging */;
    const array_1 = require(10) /* ../../../core/util/array */;
    const arrayable_1 = require(14) /* ../../../core/util/arrayable */;
    function normalize_dash_pattern(pattern) {
        for (const value of pattern) {
            if (!Number.isFinite(value) || value < 0) {
                logging_1.logger.warn(`invalid line dash pattern: ${pattern.join(",")}`);
                return [];
            }
        }
        if (pattern.length % 2 == 1) {
            pattern = (0, array_1.concat)([pattern, pattern]);
        }
        return (0, arrayable_1.sum)(pattern) == 0 ? [] : pattern;
    }
    /*
     * DashCache creates and stores webgl resources for dashes that can be reused
     * for different webgl lines. Dash is represented by a pattern containing an
     * even number of non-negative lengths.
     */
    class DashCache {
        _regl; // Needed to create textures.
        _map;
        constructor(regl) {
            this._regl = regl;
            this._map = new Map();
        }
        _create_texture(pattern) {
            /*
             * Texture used to represent dash pattern is a distance function.  Each tex
             * value is the distance to the nearest edge between a dash and a gap; +ve
             * if in a dash and -ve if in a gap.  If this was an analytical function
             * then it would be piecewise linear with turning points (local extremes)
             * in the middle of each dash and each gap.  Try to use the minimum texture
             * length that includes all these middle points.  For a single dash (hence
             * single gap) this is 2 values, one each in the middle of the dash and the
             * gap.
             * For rendering the texture is repeated.  WebGL only supports this for
             * texture lengths that are a power of 2, so if the ideal texture length is
             * not a power of 2 then increase it to be a large power of 2 and do not
             * bother to ensure that turning points in the distance function correspond
             * to texture value locations.
             * Finally, would like to use floating point textures for the distance.
             * However, these are often not available on mobile devices so instead scale
             * them to uint8 and convert back to floating point in fragment shader.
             */
            const n = pattern.length; // Number of items in pattern.
            let len = 0; // Length of pattern.
            const twice_jumps = []; // Twice the jumps between dash middles.
            let dist_min = 0.0, dist_max = 0.0; // Min and max distances.
            for (let i = 0; i < n; i++) {
                len += pattern[i];
                twice_jumps.push(pattern[i] + pattern[(i + 1) % n]);
                if (i % 2 == 0) {
                    dist_max = Math.max(dist_max, pattern[i]); // Dash.
                }
                else {
                    dist_min = Math.min(dist_min, -pattern[i]); // Gap.
                }
            }
            dist_min *= 0.5;
            dist_max *= 0.5;
            const integer_jumps = twice_jumps.every(Number.isInteger);
            const twice_jumps_gcd = integer_jumps ? (0, math_1.gcd)(twice_jumps) : 0;
            // Starts and ends of dashes and gaps.
            const starts_and_ends = [0];
            for (let i = 0; i < n; i++) {
                starts_and_ends.push(starts_and_ends[i] + pattern[i]);
            }
            // Length of texture, webgl requires a power of 2.
            const ideal_ntex = integer_jumps ? 2 * len / twice_jumps_gcd : 128;
            const length_pow_2 = integer_jumps && (0, math_1.is_pow_2)(ideal_ntex);
            const ntex = length_pow_2 ? ideal_ntex : 128;
            // Distance between texture values.
            const dtex = len / ntex;
            // xstart is the position along the texture of the first value, and offset
            // is the distance to the upstroke of the first dash.
            // When interpolating the texture each texel fills 1/ntex of the length of
            // the texture.  For a single dash the centre of the dash is 0.25 along
            // the texture, so the upstroke offset has to be determined from this.
            let xstart;
            if (length_pow_2) {
                xstart = 0.5 * pattern[0];
                if (dtex < xstart) {
                    const n_dtex = Math.floor(xstart / dtex);
                    xstart -= n_dtex * dtex;
                }
            }
            else {
                // Have lots of values so don't need to match middles of dashes/gaps.
                xstart = 0.0;
            }
            const offset = xstart - 0.5 * dtex;
            // Calculate values for texture.
            const dist = new Uint8Array(ntex);
            let dash_index = 0;
            for (let i = 0; i < ntex; i++) {
                const x = xstart + i * dtex; // Distance along texture.
                // Which dash are we in?
                while (dash_index < n - 1 && x >= starts_and_ends[dash_index + 1]) {
                    dash_index++;
                }
                const xsize = pattern[dash_index];
                const xmid = starts_and_ends[dash_index] + 0.5 * xsize;
                let dist_float = 0.5 * xsize - Math.abs(x - xmid);
                if (dash_index % 2 == 1) {
                    dist_float = -dist_float; // Change sign for gaps between dashes.
                }
                dist[i] = Math.round(255 * (dist_float - dist_min) / (dist_max - dist_min));
            }
            // Create the 1D texture.
            const tex = this._regl.texture({
                shape: [ntex, 1, 1],
                data: dist,
                wrapS: "repeat",
                format: "alpha",
                type: "uint8",
                mag: "linear",
                min: "linear",
            });
            return [[len, offset, dist_min, dist_max], tex];
        }
        _get_key(pattern) {
            return pattern.join(",");
        }
        _get_or_create(pattern) {
            const key = this._get_key(pattern);
            let cached = this._map.get(key);
            if (cached == null) {
                // GCD-based texture reuse is only meaningful for integer dash patterns.
                // BokehJS also accepts fractional Canvas-style patterns, which are kept
                // verbatim rather than being subjected to floating-point Euclid loops.
                const scale = pattern.every(Number.isInteger) ? (0, math_1.gcd)(pattern) : 1;
                if (scale > 1) {
                    // Do not modify pattern in-place, create a new one.
                    pattern = (0, arrayable_1.map)(pattern, (n) => (n / scale));
                    // Get the simple pattern that can be reused when scaled up.
                    cached = this._get_or_create(pattern);
                    // Store an entry for the requested pattern which is just the simple
                    // pattern scaled-up.
                    const [tex_info, tex, _simple_scale] = cached;
                    cached = [tex_info, tex, scale];
                    this._map.set(key, cached);
                }
                else {
                    // Simple pattern with scale of 1.
                    const [tex_info, tex] = this._create_texture(pattern);
                    // Store the simple pattern.
                    cached = [tex_info, tex, scale];
                    this._map.set(key, cached);
                }
            }
            return cached;
        }
        get(pattern) {
            pattern = normalize_dash_pattern(pattern);
            if (pattern.length == 0) {
                throw new Error("cannot create a dash texture for a solid line");
            }
            return this._get_or_create(pattern);
        }
    }
    exports.DashCache = DashCache;
},
644: /* models/glyphs/webgl/utils/math.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.gcd = gcd;
    exports.is_pow_2 = is_pow_2;
    // Greatest Common Divisor of 2+ integers using Euclid's algorithm.
    function gcd2(a, b) {
        a = Math.abs(a);
        b = Math.abs(b);
        if (a == 0) {
            return b;
        }
        if (b == 0) {
            return a;
        }
        while (b != 0) {
            const remainder = a % b;
            a = b;
            b = remainder;
        }
        return a;
    }
    function gcd(values) {
        let ret = 0;
        for (let i = 0; i < values.length; i++) {
            ret = gcd2(ret, values[i]);
        }
        return ret;
    }
    // From regl
    function is_pow_2(v) {
        return (v & (v - 1)) == 0 && v != 0;
    }
},
645: /* models/glyphs/webgl/accumulate.vert.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
precision highp float;attribute vec2 a_position;varying vec2 v_tex_coords;void main(){gl_Position=vec4(a_position.x,a_position.y,0.,1.);v_tex_coords=0.5*(1.+a_position);}`;
    exports.default = shader;
},
646: /* models/glyphs/webgl/accumulate.frag.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
uniform sampler2D u_framebuffer_tex;varying vec2 v_tex_coords;void main(){gl_FragColor=texture2D(u_framebuffer_tex,v_tex_coords);}`;
    exports.default = shader;
},
647: /* models/glyphs/webgl/image.vert.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
precision highp float;attribute vec2 a_position;attribute vec4 a_bounds;uniform vec2 u_canvas_size;varying vec2 v_tex_coords;void main(){v_tex_coords=vec2(a_position.x<0.?0.:1.,a_position.y<0.?0.:1.);float x=a_position.x<0.?a_bounds[0]:a_bounds[2];float y=a_position.y<0.?a_bounds[1]:a_bounds[3];vec2 xy=vec2(x,y);vec2 pos=xy+0.5;pos/=u_canvas_size;gl_Position=vec4(2.*pos.x-1.,1.-2.*pos.y,0.,1.);}`;
    exports.default = shader;
},
648: /* models/glyphs/webgl/image.frag.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
uniform sampler2D u_tex;uniform float u_global_alpha;varying vec2 v_tex_coords;void main(){vec4 color=texture2D(u_tex,v_tex_coords);float alpha=color.a*u_global_alpha;gl_FragColor=vec4(color.rgb*alpha,alpha);}`;
    exports.default = shader;
},
649: /* models/glyphs/webgl/regl_line.vert.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
precision highp float;const int butt_cap=0;const int round_cap=1;const int square_cap=2;const int miter_join=0;const int round_join=1;const int bevel_join=2;attribute vec2 a_position;attribute vec2 a_point_prev;attribute vec2 a_point_start;attribute vec2 a_point_end;attribute vec2 a_point_next;attribute float a_show_prev;attribute float a_show_curr;attribute float a_show_next;attribute float a_linewidth;attribute vec4 a_line_color;attribute float a_line_cap;attribute float a_line_join;
#ifdef DASHED
attribute float a_length_so_far;attribute vec4 a_dash_tex_info;attribute float a_dash_scale;attribute float a_dash_offset;
#endif
uniform vec2 u_canvas_size;uniform float u_antialias;uniform float u_miter_limit;varying float v_linewidth;varying vec4 v_line_color;varying float v_line_cap;varying float v_line_join;varying float v_segment_length;varying vec2 v_coords;varying float v_flags;varying float v_cos_turn_angle_start;varying float v_cos_turn_angle_end;
#ifdef DASHED
varying float v_length_so_far;varying vec4 v_dash_tex_info;varying float v_dash_scale;varying float v_dash_offset;
#endif
#define SMALL  1e-6
float cross_z(in vec2 v0,in vec2 v1){return v0.x*v1.y-v0.y*v1.x;}vec2 right_vector(in vec2 v){return vec2(v.y,-v.x);}float calc_turn_angle(in bool has_cap,in vec2 segment_right,in vec2 other_right,out vec2 point_right,out float sin_turn_angle){float cos_turn_angle;vec2 diff=segment_right+other_right;float len=length(diff);if(has_cap||len<SMALL){point_right=segment_right;cos_turn_angle=-1.;sin_turn_angle=0.;}else{point_right=diff/len;cos_turn_angle=dot(segment_right,other_right);sin_turn_angle=cross_z(segment_right,other_right);}return cos_turn_angle;}bool miter_too_large(in int join_type,in float cos_turn_angle){float cos_half_angle_sqr=0.5*(1.+cos_turn_angle);return join_type==miter_join&&cos_half_angle_sqr<1./(u_miter_limit*u_miter_limit);}vec2 normalize_check_len(in vec2 vec,in float len){if(abs(len)<SMALL)return vec2(1.,0.);else return vec/len;}vec2 normalize_check(in vec2 vec){return normalize_check_len(vec,length(vec));}void main(){if(a_show_curr<0.5){gl_Position=vec4(-2.,-2.,0.,1.);return;}int join_type=int(a_line_join+0.5);int cap_type=int(a_line_cap+0.5);v_linewidth=a_linewidth;v_line_color=a_line_color;if(v_linewidth<1.){v_line_color.a*=v_linewidth;v_linewidth=1.;}float halfwidth=0.5*(v_linewidth+u_antialias);vec2 segment_along=a_point_end-a_point_start;v_segment_length=length(a_point_end-a_point_start);segment_along=normalize_check_len(segment_along,v_segment_length);vec2 segment_right=right_vector(segment_along);vec2 xy;vec2 prev_along=normalize_check(a_point_start-a_point_prev);vec2 prev_right=right_vector(prev_along);vec2 next_right=right_vector(normalize_check(a_point_next-a_point_end));v_coords.y=a_position.y*halfwidth;bool has_start_cap=a_show_prev<0.5;bool has_end_cap=a_show_next<0.5;vec2 point_right_start,point_right_end;float sin_turn_angle_start,sin_turn_angle_end;v_cos_turn_angle_start=calc_turn_angle(has_start_cap,segment_right,prev_right,point_right_start,sin_turn_angle_start);v_cos_turn_angle_end=calc_turn_angle(has_end_cap,segment_right,next_right,point_right_end,sin_turn_angle_end);float sign_turn_right_start=sin_turn_angle_start>=0.?1.:-1.;bool miter_too_large_start=!has_start_cap&&miter_too_large(join_type,v_cos_turn_angle_start);bool miter_too_large_end=!has_end_cap&&miter_too_large(join_type,v_cos_turn_angle_end);float sign_at_start=-sign(a_position.x);vec2 point=sign_at_start>0.?a_point_start:a_point_end;if((has_start_cap&&sign_at_start>0.)||(has_end_cap&&sign_at_start<0.)){xy=point-segment_right*(halfwidth*a_position.y);if(cap_type==butt_cap)xy-=sign_at_start*0.5*u_antialias*segment_along;else xy-=sign_at_start*halfwidth*segment_along;}else if(sign_at_start>0.){vec2 inside_point=a_point_start+segment_right*(sign_turn_right_start*halfwidth);vec2 prev_outside_point=a_point_start-prev_right*(sign_turn_right_start*halfwidth);if(join_type==round_join||join_type==bevel_join||miter_too_large_start){if(v_cos_turn_angle_start<=0.){xy=a_point_start-segment_right*(halfwidth*a_position.y)-halfwidth*segment_along;}else{if(a_position.x<-1.5){xy=prev_outside_point;v_coords.y=-dot(xy-a_point_start,segment_right);}else if(a_position.y*sign_turn_right_start>0.){float d=halfwidth*abs(sin_turn_angle_start);xy=a_point_start-segment_right*(halfwidth*a_position.y)-d*segment_along;}else{xy=inside_point;}}}else{if(a_position.x<-1.5){xy=prev_outside_point;v_coords.y=-dot(xy-a_point_start,segment_right);}else if(a_position.y*sign_turn_right_start>0.){float tan_half_turn_angle=(1.-v_cos_turn_angle_start)/sin_turn_angle_start;float d=sign_turn_right_start*halfwidth*tan_half_turn_angle;xy=a_point_start-segment_right*(halfwidth*a_position.y)-d*segment_along;}else{xy=inside_point;}}}else{xy=point-segment_right*(halfwidth*a_position.y);}vec2 pos=xy+0.5;pos/=u_canvas_size;gl_Position=vec4(2.*pos.x-1.,1.-2.*pos.y,0.,1.);bool turn_right_start=sin_turn_angle_start>=0.;bool turn_right_end=sin_turn_angle_end>=0.;v_coords.x=dot(xy-a_point_start,segment_along);v_flags=float(int(has_start_cap)+2*int(has_end_cap)+4*int(miter_too_large_start)+8*int(miter_too_large_end)+16*int(turn_right_start)+32*int(turn_right_end));v_line_cap=a_line_cap;v_line_join=a_line_join;
#ifdef DASHED
v_length_so_far=a_length_so_far;v_dash_tex_info=a_dash_tex_info;v_dash_scale=a_dash_scale;v_dash_offset=a_dash_offset;
#endif
}`;
    exports.default = shader;
},
650: /* models/glyphs/webgl/regl_line.frag.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
const int butt_cap=0;const int round_cap=1;const int square_cap=2;const int miter_join=0;const int round_join=1;const int bevel_join=2;uniform float u_antialias;
#ifdef DASHED
uniform sampler2D u_dash_tex;
#endif
varying float v_linewidth;varying vec4 v_line_color;varying float v_line_cap;varying float v_line_join;varying float v_segment_length;varying vec2 v_coords;varying float v_flags;varying float v_cos_turn_angle_start;varying float v_cos_turn_angle_end;
#ifdef DASHED
varying float v_length_so_far;varying vec4 v_dash_tex_info;varying float v_dash_scale;varying float v_dash_offset;
#endif
#define ONE_MINUS_SMALL  (1.0 - 1e-6)
float cross_z(in vec2 v0,in vec2 v1){return v0.x*v1.y-v0.y*v1.x;}vec2 right_vector(in vec2 v){return vec2(v.y,-v.x);}float bevel_join_distance(in vec2 coords,in vec2 other_right,in float sign_turn_right){float hw=0.5*v_linewidth;if(other_right.y>=ONE_MINUS_SMALL){return abs(hw-v_coords.x);}else{const vec2 segment_right=vec2(0.,-1.);vec2 corner_right=normalize(other_right+segment_right);vec2 outside_point=(-hw*sign_turn_right)*segment_right;return hw+sign_turn_right*dot(outside_point-coords,corner_right);}}float cap(in int cap_type,in float x,in float y){if(cap_type==butt_cap)return max(0.5*v_linewidth-x,abs(y));else if(cap_type==square_cap)return max(-x,abs(y));else return distance(vec2(min(x,0.),y),vec2(0.,0.));}float distance_to_alpha(in float dist){return 1.-smoothstep(0.5*(v_linewidth-u_antialias),0.5*(v_linewidth+u_antialias),dist);}vec2 turn_angle_to_right_vector(in float cos_turn_angle,in float sign_turn_right){float sin_turn_angle=sign_turn_right*sqrt(1.-cos_turn_angle*cos_turn_angle);return vec2(sin_turn_angle,-cos_turn_angle);}
#ifdef DASHED
float dash_distance(in float x){float tex_length=v_dash_tex_info.x;float tex_offset=v_dash_tex_info.y;float tex_dist_min=v_dash_tex_info.z;float tex_dist_max=v_dash_tex_info.w;x+=v_length_so_far-v_dash_scale*tex_offset+v_dash_offset;float dist=texture2D(u_dash_tex,vec2(x/(tex_length*v_dash_scale),0.)).a;dist=tex_dist_min+dist*(tex_dist_max-tex_dist_min);return v_dash_scale*dist;}mat2 rotation_matrix(in vec2 other_right){float sin_angle=other_right.x;float cos_angle=-other_right.y;return mat2(cos_angle,-sin_angle,sin_angle,cos_angle);}
#endif
void main(){int join_type=int(v_line_join+0.5);int cap_type=int(v_line_cap+0.5);float halfwidth=0.5*(v_linewidth+u_antialias);float half_antialias=0.5*u_antialias;int flags=int(v_flags+0.5);bool turn_right_end=(flags/32>0);float sign_turn_right_end=turn_right_end?1.:-1.;flags-=32*int(turn_right_end);bool turn_right_start=(flags/16>0);float sign_turn_right_start=turn_right_start?1.:-1.;flags-=16*int(turn_right_start);bool miter_too_large_end=(flags/8>0);flags-=8*int(miter_too_large_end);bool miter_too_large_start=(flags/4>0);flags-=4*int(miter_too_large_start);bool has_end_cap=(flags/2>0);flags-=2*int(has_end_cap);bool has_start_cap=flags>0;vec2 prev_right=turn_angle_to_right_vector(v_cos_turn_angle_start,sign_turn_right_start);vec2 next_right=turn_angle_to_right_vector(v_cos_turn_angle_end,sign_turn_right_end);float dist=v_coords.y;vec2 end_coords=vec2(v_segment_length,0.)-v_coords;if(v_coords.x<=half_antialias){if(has_start_cap)dist=cap(cap_type,v_coords.x,v_coords.y);else if(join_type==round_join){if(v_coords.x<=0.)dist=distance(v_coords,vec2(0.,0.));}else{if(join_type==bevel_join||miter_too_large_start)dist=max(abs(dist),bevel_join_distance(v_coords,prev_right,sign_turn_right_start));float prev_sideways_dist=-sign_turn_right_start*dot(v_coords,prev_right);dist=max(abs(dist),prev_sideways_dist);}}if(end_coords.x<=half_antialias){if(has_end_cap){dist=max(abs(dist),cap(cap_type,end_coords.x,v_coords.y));}else if(join_type==bevel_join||miter_too_large_end){dist=max(abs(dist),bevel_join_distance(end_coords,next_right,sign_turn_right_end));}}float alpha=distance_to_alpha(abs(dist));
#ifdef DASHED
if(v_dash_tex_info.x>=0.){dist=dash_distance(v_coords.x);vec2 prev_coords=rotation_matrix(prev_right)*v_coords;float start_dash_distance=dash_distance(0.);if(!has_start_cap&&cap_type==butt_cap){bool outer_solid=start_dash_distance>=0.&&v_coords.x<half_antialias&&prev_coords.x>-half_antialias;if(outer_solid){float half_aa_dist=dash_distance(half_antialias);if(half_aa_dist>0.)dist=half_aa_dist-v_coords.x+half_antialias;else dist=start_dash_distance-v_coords.x;half_aa_dist=dash_distance(-half_antialias);if(half_aa_dist>0.)dist=min(dist,half_aa_dist+prev_coords.x+half_antialias);else dist=min(dist,start_dash_distance+prev_coords.x);}else{if(v_coords.x<half_antialias)dist=min(0.,dash_distance(half_antialias)-half_antialias)+v_coords.x;if(prev_coords.x>-half_antialias&&prev_coords.x<=half_antialias){float prev_dist=min(0.,dash_distance(-half_antialias)-half_antialias)-prev_coords.x;prev_dist=min(prev_dist,0.5*v_linewidth-abs(prev_coords.y));dist=max(dist,prev_dist);}}}if(!has_end_cap&&cap_type==butt_cap&&end_coords.x<half_antialias){float end_dash_distance=dash_distance(v_segment_length);bool increasing=end_dash_distance>=0.&&sign_turn_right_end*v_coords.y<0.;if(!increasing){float half_aa_dist=dash_distance(v_segment_length-half_antialias);dist=min(0.,half_aa_dist-half_antialias)+end_coords.x;}}dist=cap(cap_type,dist,v_coords.y);float dash_alpha=distance_to_alpha(dist);alpha=min(alpha,dash_alpha);}
#endif
alpha=v_line_color.a*alpha;gl_FragColor=vec4(v_line_color.rgb*alpha,alpha);}`;
    exports.default = shader;
},
651: /* models/glyphs/webgl/marker.vert.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
precision highp float;attribute vec2 a_position;attribute vec2 a_center;attribute float a_width;attribute float a_height;attribute float a_angle;attribute float a_aux;attribute float a_linewidth;attribute vec4 a_line_color;attribute vec4 a_fill_color;attribute float a_line_cap;attribute float a_line_join;attribute float a_show;
#ifdef HATCH
attribute float a_hatch_pattern;attribute float a_hatch_scale;attribute float a_hatch_weight;attribute vec4 a_hatch_color;
#endif
uniform vec2 u_canvas_size;uniform float u_antialias;
#ifdef MULTI_MARKER
uniform float u_size_hint;
#endif
#ifdef USE_ROUND_RECT
uniform vec4 u_border_radius;varying vec4 v_border_radius;
#endif
#ifdef USE_ANNULAR_WEDGE
varying float v_outer_radius;varying float v_inner_radius;varying float v_start_angle;varying float v_end_angle;
#endif
#ifdef USE_ANNULUS
varying float v_outer_radius;varying float v_inner_radius;
#endif
#ifdef USE_WEDGE
varying float v_radius;varying float v_start_angle;varying float v_end_angle;
#endif
#if defined(USE_CIRCLE) || defined(USE_NGON)
varying float v_radius;
#endif
#ifdef USE_NGON
varying float v_n;
#endif
varying float v_linewidth;varying vec2 v_size;varying vec4 v_line_color;varying vec4 v_fill_color;varying float v_line_cap;varying float v_line_join;varying vec2 v_coords;
#ifdef HATCH
varying float v_hatch_pattern;varying float v_hatch_scale;varying float v_hatch_weight;varying vec4 v_hatch_color;varying vec2 v_hatch_coords;
#endif
#ifdef MULTI_MARKER
#define M_DASH          1
#define M_DOT           2
#define M_DIAMOND       3
#define M_HEX           4
#define M_SQUARE_PIN    5
#define M_TRIANGLE      6
#define M_TRIANGLE_PIN  7
#define M_STAR          8
vec2 enclosing_size(){int size_hint=int(u_size_hint+0.5);if(size_hint==M_DASH)return vec2(v_size.x+v_linewidth+u_antialias,v_linewidth+u_antialias);else if(size_hint==M_DOT)return 0.25*v_size+u_antialias;else if(size_hint==M_DIAMOND)return vec2(v_size.x*(2./3.)+(v_linewidth+u_antialias)*1.20185,v_size.y+(v_linewidth+u_antialias)*1.80278);else if(size_hint==M_HEX)return v_size+(v_linewidth+u_antialias)*vec2(2./sqrt(3.),1.);else if(size_hint==M_SQUARE_PIN)return v_size+(v_linewidth+u_antialias)*3.1;else if(size_hint==M_TRIANGLE)return vec2(v_size.x+(v_linewidth+u_antialias)*sqrt(3.),v_size.y*(2./sqrt(3.))+(v_linewidth+u_antialias)*2.);else if(size_hint==M_TRIANGLE_PIN)return v_size+(v_linewidth+u_antialias)*vec2(4.8,6.);else if(size_hint==M_STAR)return vec2(v_size.x*0.95106+(v_linewidth+u_antialias)*3.,v_size.y+(v_linewidth+u_antialias)*3.2);else return v_size+v_linewidth+u_antialias;}
#else
vec2 enclosing_size(){return v_size+v_linewidth+u_antialias;}
#endif
void main(){
#if defined(USE_RECT) || defined(USE_ROUND_RECT) || defined(USE_HEX_TILE)
v_size=vec2(a_width,a_height);
#elif defined(USE_ANNULUS) || defined(USE_ANNULAR_WEDGE) || defined(USE_WEDGE)
v_size=vec2(2.*a_width,2.*a_width);
#else
v_size=vec2(a_width,a_width);
#endif
#ifdef USE_NGON
v_n=a_aux;
#endif
if(a_show<0.5||v_size.x<0.||v_size.y<0.||(v_size.x==0.&&v_size.y==0.)
#ifdef USE_NGON
||v_n<3.
#endif
){gl_Position=vec4(-2.,-2.,0.,1.);return;}
#ifdef USE_ANNULAR_WEDGE
v_outer_radius=a_width;v_inner_radius=a_height;v_start_angle=a_angle;v_end_angle=a_aux;
#endif
#ifdef USE_ANNULUS
v_outer_radius=a_width;v_inner_radius=a_height;
#endif
#ifdef USE_WEDGE
v_radius=a_width;v_start_angle=a_angle;v_end_angle=a_aux;
#endif
#if defined(USE_CIRCLE) || defined(USE_NGON)
v_radius=0.5*a_width;
#endif
#ifdef USE_ROUND_RECT
const vec2 unit2=vec2(1.,1.);float scale=min(v_size.x/max(dot(u_border_radius.xy,unit2),dot(u_border_radius.zw,unit2)),v_size.y/max(dot(u_border_radius.yz,unit2),dot(u_border_radius.wx,unit2)));v_border_radius=u_border_radius*min(scale,1.);
#endif
v_linewidth=a_linewidth;v_line_color=a_line_color;v_fill_color=a_fill_color;v_line_cap=a_line_cap;v_line_join=a_line_join;if(v_linewidth<1.){v_line_color.a*=v_linewidth;v_linewidth=1.;}
#ifdef HATCH
v_hatch_pattern=a_hatch_pattern;v_hatch_scale=a_hatch_scale;v_hatch_weight=a_hatch_weight;v_hatch_color=a_hatch_color;
#endif
v_coords=a_position*enclosing_size();
#if defined(USE_CIRCLE) || defined(USE_ANNULUS) || defined(USE_ANNULAR_WEDGE) || defined(USE_WEDGE)
vec2 pos=a_center+v_coords;
#else
float c=cos(-a_angle);float s=sin(-a_angle);mat2 rotation=mat2(c,-s,s,c);vec2 pos=a_center+rotation*v_coords;
#endif
#ifdef HATCH
v_hatch_coords=pos-0.5;
#endif
pos+=0.5;pos/=u_canvas_size;gl_Position=vec4(2.*pos.x-1.,1.-2.*pos.y,0.,1.);}`;
    exports.default = shader;
},
652: /* models/glyphs/webgl/marker.frag.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
const float SQRT2=sqrt(2.);const float SQRT3=sqrt(3.);const float PI=3.14159265358979323846;const int butt_cap=0;const int round_cap=1;const int square_cap=2;const int miter_join=0;const int round_join=1;const int bevel_join=2;
#ifdef HATCH
const int hatch_dot=1;const int hatch_ring=2;const int hatch_horizontal_line=3;const int hatch_vertical_line=4;const int hatch_cross=5;const int hatch_horizontal_dash=6;const int hatch_vertical_dash=7;const int hatch_spiral=8;const int hatch_right_diagonal_line=9;const int hatch_left_diagonal_line=10;const int hatch_diagonal_cross=11;const int hatch_right_diagonal_dash=12;const int hatch_left_diagonal_dash=13;const int hatch_horizontal_wave=14;const int hatch_vertical_wave=15;const int hatch_criss_cross=16;
#endif
uniform float u_antialias;varying vec2 v_coords;varying vec2 v_size;
#ifdef USE_ANNULAR_WEDGE
varying float v_outer_radius;varying float v_inner_radius;varying float v_start_angle;varying float v_end_angle;
#endif
#ifdef USE_ANNULUS
varying float v_outer_radius;varying float v_inner_radius;
#endif
#ifdef USE_WEDGE
varying float v_radius;varying float v_start_angle;varying float v_end_angle;
#endif
#if defined(USE_CIRCLE) || defined(USE_NGON)
varying float v_radius;
#endif
#ifdef USE_NGON
varying float v_n;
#endif
#ifdef USE_ROUND_RECT
varying vec4 v_border_radius;
#endif
varying float v_linewidth;varying vec4 v_line_color;varying vec4 v_fill_color;varying float v_line_cap;varying float v_line_join;
#ifdef HATCH
varying float v_hatch_pattern;varying float v_hatch_scale;varying float v_hatch_weight;varying vec4 v_hatch_color;varying vec2 v_hatch_coords;
#endif
#if defined(USE_CIRCLE_DOT) || defined(USE_DIAMOND_DOT) || defined(USE_DOT) || defined(USE_HEX_DOT) || defined(USE_SQUARE_DOT) || defined(USE_STAR_DOT) || defined(USE_TRIANGLE_DOT)
#define APPEND_DOT 
#endif
#if defined(USE_CIRCLE_CROSS) || defined(USE_SQUARE_CROSS)
#define APPEND_CROSS 
#endif
#ifdef USE_DIAMOND_CROSS
#define APPEND_CROSS_2 
#endif
#ifdef USE_CIRCLE_X
#define APPEND_X 
#define APPEND_X_LEN  (0.5*v_size.x)
#endif
#ifdef USE_SQUARE_X
#define APPEND_X 
#define APPEND_X_LEN  (v_size.x/SQRT2)
#endif
#ifdef USE_CIRCLE_Y
#define APPEND_Y 
#endif
#if defined(USE_ASTERISK) || defined(USE_CROSS) || defined(USE_DASH) || defined(USE_DOT) || defined(USE_X) || defined(USE_Y)
#define LINE_ONLY 
#endif
#if defined(LINE_ONLY) || defined(APPEND_CROSS) || defined(APPEND_CROSS_2) || defined(APPEND_X) || defined(APPEND_Y)
float end_cap_distance(in vec2 p,in vec2 end_point,in vec2 unit_direction,in int line_cap){vec2 offset=p-end_point;if(line_cap==butt_cap)return dot(offset,unit_direction)+0.5*v_linewidth;else if(line_cap==square_cap)return dot(offset,unit_direction);else if(line_cap==round_cap&&dot(offset,unit_direction)>0.)return length(offset);else return-v_linewidth-u_antialias;}
#endif
#if !(defined(LINE_ONLY) || defined(USE_SQUARE_PIN) || defined(USE_TRIANGLE_PIN))
float line_join_distance_no_miter(in vec2 p,in vec2 corner,in vec2 unit_normal,in float offset,in int line_join){float dist_outside=dot((p-corner),unit_normal)-offset;if(line_join==bevel_join&&dist_outside>-0.5*u_antialias)return dist_outside+0.5*v_linewidth;else if(dist_outside>0.)return distance(p,corner);else return-v_linewidth-u_antialias;}
#endif
#if defined(USE_SQUARE_PIN) || defined(USE_TRIANGLE_PIN)
float line_join_distance_incl_miter(in vec2 p,in vec2 corner,in vec2 unit_normal,in float offset,in int line_join,vec2 miter_unit_normal){float dist_outside=dot((p-corner),unit_normal)-offset;if(line_join==miter_join&&dist_outside>0.)return dot((p-corner),miter_unit_normal);else if(line_join==bevel_join&&dist_outside>-0.5*u_antialias)return dist_outside+0.5*v_linewidth;else if(dist_outside>0.)return distance(p,corner);else return-v_linewidth-u_antialias;}
#endif
#if defined(APPEND_CROSS) || defined(APPEND_X) || defined(USE_ASTERISK) || defined(USE_CROSS) || defined(USE_X)
float one_cross(in vec2 p,in int line_cap,in float len){p=abs(p);p=(p.y>p.x)?p.yx:p.xy;float dist=p.y;float end_dist=end_cap_distance(p,vec2(len,0.),vec2(1.,0.),line_cap);return max(dist,end_dist);}
#endif
#ifdef APPEND_CROSS_2
float one_cross_2(in vec2 p,in int line_cap,in vec2 lengths){p=abs(p);bool switch_xy=(p.y>p.x);p=switch_xy?p.yx:p.xy;float len=switch_xy?lengths.y:lengths.x;float dist=p.y;float end_dist=end_cap_distance(p,vec2(len,0.),vec2(1.,0.),line_cap);return max(dist,end_dist);}
#endif
#if defined(APPEND_Y) || defined(USE_Y)
float one_y(in vec2 p,in int line_cap,in float len){p=vec2(abs(p.x),-p.y);const float k=6./sqrt(13.);vec2 unit_along=vec2(0.5*k,k/3.);vec2 end_point=vec2(0.5*len*SQRT3,len*SQRT3/3.);float dist=max(abs(dot(p,vec2(-unit_along.y,unit_along.x))),end_cap_distance(p,end_point,unit_along,line_cap));if(p.y<0.){float vert_dist=max(p.x,end_cap_distance(p,vec2(0.,-len),vec2(0.,-1.),line_cap));dist=min(dist,vert_dist);}return dist;}
#endif
#ifdef USE_ASTERISK
float marker_distance(in vec2 p,in int line_cap,in int line_join){vec2 p_diag=vec2((p.x+p.y)/SQRT2,(p.x-p.y)/SQRT2);float len=0.5*v_size.x;return min(one_cross(p,line_cap,len),one_cross(p_diag,line_cap,len));}
#endif
#if defined(USE_ANNULUS) || defined(USE_WEDGE) || defined(USE_ANNULAR_WEDGE)
float merge(in float d1,in float d2){return min(d1,d2);}float intersect(in float d1,in float d2){return max(d1,d2);}float subtract(in float d1,in float d2){return max(d1,-d2);}float circle(in vec2 p,in float radius){return length(p)-radius;}float segment_square(in vec2 p,in vec2 q){vec2 v=p-q*clamp(dot(p,q)/dot(q,q),0.,1.);return dot(v,v);}vec2 xy(in float angle){return vec2(cos(angle),sin(angle));}float cross_z(in vec2 v0,in vec2 v1){return v0.x*v1.y-v0.y*v1.x;}float wedge(in vec2 p,in float r,in float start_angle,in float end_angle){vec2 a=r*xy(start_angle);vec2 b=r*xy(end_angle);float d=sqrt(merge(segment_square(p,a),segment_square(p,b)));float s;if(cross_z(a,b)<0.){s=sign(max(cross_z(a,p),cross_z(p,b)));}else{s=-sign(max(cross_z(p,a),cross_z(b,p)));}return s*d;}float annulus(in vec2 p,in float outer_radius,in float inner_radius){float outer=circle(p,outer_radius);float inner=circle(p,inner_radius);return subtract(outer,inner);}
#endif
#if defined(USE_ANNULUS)
float marker_distance(in vec2 p,in int line_cap,in int line_join){return annulus(p,v_outer_radius,v_inner_radius);}
#endif
#if defined(USE_WEDGE)
float marker_distance(in vec2 p,in int line_cap,in int line_join){return intersect(circle(p,v_radius),wedge(p,v_radius,v_start_angle,v_end_angle));}
#endif
#if defined(USE_ANNULAR_WEDGE)
float marker_distance(in vec2 p,in int line_cap,in int line_join){return intersect(annulus(p,v_outer_radius,v_inner_radius),wedge(p,v_outer_radius,v_start_angle,v_end_angle));}
#endif
#if defined(USE_CIRCLE) || defined(USE_CIRCLE_CROSS) || defined(USE_CIRCLE_DOT) || defined(USE_CIRCLE_X) || defined(USE_CIRCLE_Y)
float marker_distance(in vec2 p,in int line_cap,in int line_join){return length(p)-0.5*v_size.x;}
#endif
#ifdef USE_CROSS
float marker_distance(in vec2 p,in int line_cap,in int line_join){return one_cross(p,line_cap,0.5*v_size.x);}
#endif
#ifdef USE_DASH
float marker_distance(in vec2 p,in int line_cap,in int line_join){p=abs(p);float dist=p.y;float end_dist=end_cap_distance(p,vec2(0.5*v_size.x,0.),vec2(1.,0.),line_cap);return max(dist,end_dist);}
#endif
#if defined(USE_DIAMOND) || defined(USE_DIAMOND_CROSS) || defined(USE_DIAMOND_DOT)
float marker_distance(in vec2 p,in int line_cap,in int line_join){p=abs(p);float r=0.5*v_size.x;const float SQRT13=sqrt(13.);float dist=dot(p,vec2(3.,2.))/SQRT13-2.*r/SQRT13;if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p,vec2(0.,r),vec2(0.,1.),v_linewidth/SQRT13,line_join));dist=max(dist,line_join_distance_no_miter(p,vec2(r*2./3.,0.),vec2(1.,0.),v_linewidth*(1.5/SQRT13),line_join));}return dist;}
#endif
#ifdef USE_DOT
float marker_distance(in vec2 p,in int line_cap,in int line_join){return v_linewidth+u_antialias;}
#endif
#if defined(USE_HEX_TILE) || defined(USE_HEX) || defined(USE_HEX_DOT)
float marker_distance(in vec2 p,in int line_cap,in int line_join){p=abs(p);float rx=v_size.x/2.;float h=v_size.y*(SQRT3/4.);float len_normal=sqrt(h*h+0.25*rx*rx);vec2 unit_normal=vec2(h,0.5*rx)/len_normal;float dist=max(dot(p,unit_normal)-rx*h/len_normal,p.y-h);if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p,vec2(rx,0.),vec2(1.,0.),0.5*v_linewidth*unit_normal.x,line_join));unit_normal=normalize(unit_normal+vec2(0.,1.));dist=max(dist,line_join_distance_no_miter(p,vec2(0.5*rx,h),unit_normal,0.5*v_linewidth*unit_normal.y,line_join));}return dist;}
#endif
#ifdef USE_NGON
float marker_distance(in vec2 p,in int line_cap,in int line_join){float side_angle=2.*PI/v_n;p.y=-p.y;float angle=mod(atan(p.x,p.y),side_angle);angle=min(angle,side_angle-angle);p=length(p)*vec2(sin(angle),cos(angle));float half_angle=0.5*side_angle;float cos_half_angle=cos(half_angle);vec2 unit_normal=vec2(sin(half_angle),cos_half_angle);vec2 corner=vec2(0.,v_size.y/2.);float dist=dot(p-corner,unit_normal);if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p,corner,vec2(0.,1.),0.5*v_linewidth*cos_half_angle,line_join));}return dist;}
#endif
#ifdef USE_PLUS
float marker_distance(in vec2 p,in int line_cap,in int line_join){p=abs(p);p=(p.y>p.x)?p.yx:p.xy;float r=0.5*v_size.x;p=p-vec2(r,0.375*r);float dist=max(p.x,p.y);if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p,vec2(0.,0.),vec2(1./SQRT2,1./SQRT2),v_linewidth/(2.*SQRT2),line_join));dist=min(dist,-line_join_distance_no_miter(p,vec2(-5.*r/8.,0.),vec2(-1./SQRT2,-1./SQRT2),v_linewidth/(2.*SQRT2),line_join));}return dist;}
#endif
#if defined(USE_ROUND_RECT)
float marker_distance(in vec2 p,in int line_cap,in int line_join){vec2 halfsize=v_size/2.;vec2 p2=abs(p)-halfsize;float dist=max(p2.x,p2.y);if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p2,vec2(0.,0.),vec2(1./SQRT2,1./SQRT2),v_linewidth/(2.*SQRT2),line_join));}vec4 border_radius=v_border_radius;vec4 xsign=vec4(-1.,1.,1.,-1.);vec4 ysign=vec4(-1.,-1.,1.,1.);for(int i=0;i<4;i++){float radius=border_radius.x;p2=p*vec2(xsign.x,ysign.x);vec2 offset=p2-halfsize+radius;if(min(radius,min(offset.x,offset.y))>0.){dist=max(dist,length(offset)-radius);}border_radius.xyzw=border_radius.yzwx;xsign.xyzw=xsign.yzwx;ysign.xyzw=ysign.yzwx;}return dist;}
#endif
#if defined(USE_RECT) || defined(USE_SQUARE) || defined(USE_SQUARE_CROSS) || defined(USE_SQUARE_DOT) || defined(USE_SQUARE_X)
float marker_distance(in vec2 p,in int line_cap,in int line_join){vec2 p2=abs(p)-v_size/2.;float dist=max(p2.x,p2.y);if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p2,vec2(0.,0.),vec2(1./SQRT2,1./SQRT2),v_linewidth/(2.*SQRT2),line_join));}return dist;}
#endif
#ifdef USE_SQUARE_PIN
float marker_distance(in vec2 p,in int line_cap,in int line_join){p=abs(p);p=(p.y>p.x)?p.yx:p.xy;float r=0.5*v_size.x;float center_x=r*2.44375;float radius=r*1.75626;float dist=radius-distance(p,vec2(center_x,0.));dist=max(dist,line_join_distance_incl_miter(p,vec2(r,r),vec2(1./SQRT2,1./SQRT2),v_linewidth*0.1124297533493792,line_join,vec2(8./sqrt(89.),-5./sqrt(89.))));return dist;}
#endif
#if defined(USE_STAR) || defined(USE_STAR_DOT)
float marker_distance(in vec2 p,in int line_cap,in int line_join){const float SQRT5=sqrt(5.);const float COS72=0.25*(SQRT5-1.);const float SIN72=sqrt((5.+SQRT5)/8.);float angle=atan(p.x,p.y);angle=mod(angle,0.4*PI)-0.2*PI;p=length(p)*vec2(cos(angle),abs(sin(angle)));float r=0.5*v_size.x;float a=r*sqrt(5.-2.*SQRT5);float dist=dot(p,vec2(COS72,SIN72))-r*COS72;if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p,vec2(r,0.),vec2(1.,0.),v_linewidth*(0.5*COS72),line_join));const float COS36=sqrt(0.5+COS72/2.);const float SIN36=sqrt(0.5-COS72/2.);dist=min(dist,-line_join_distance_no_miter(p,vec2(r-a*SIN72,a*COS72),vec2(-COS36,-SIN36),v_linewidth*(0.5*COS36),line_join));}return dist;}
#endif
#if defined(USE_TRIANGLE) || defined(USE_TRIANGLE_DOT) || defined(USE_INVERTED_TRIANGLE)
float marker_distance(in vec2 p,in int line_cap,in int line_join){float r=0.5*v_size.x;float a=r*SQRT3/3.;
#ifdef USE_INVERTED_TRIANGLE
p=vec2(abs(p.x),-p.y);
#else
p=vec2(abs(p.x),p.y);
#endif
float dist=max(0.5*dot(p,vec2(SQRT3,-1.))-a,p.y-a);if(line_join!=miter_join){dist=max(dist,line_join_distance_no_miter(p,vec2(0.,-(2./SQRT3)*r),vec2(0.,-1.),v_linewidth*0.25,line_join));dist=max(dist,line_join_distance_no_miter(p,vec2(r,a),vec2(SQRT3/2.,0.5),v_linewidth*0.25,line_join));}return dist;}
#endif
#ifdef USE_TRIANGLE_PIN
float marker_distance(in vec2 p,in int line_cap,in int line_join){float angle=atan(p.x,-p.y);angle=mod(angle,PI*2./3.)-PI/3.;p=length(p)*vec2(cos(angle),abs(sin(angle)));const float a=1./SQRT3;const float b=SQRT3/8.;const float c=(a-b)/2.;const float x=(1.-c*c)/(2.*c);const float center_x=x+a;const float radius=x+c;float r=0.5*v_size.x;float dist=r*radius-distance(p,vec2(r*center_x,0.));dist=max(dist,line_join_distance_incl_miter(p,vec2(a*r,r),vec2(0.5,0.5*SQRT3),v_linewidth*0.0881844526878324,line_join,vec2(8.*SQRT3,-5.)/sqrt(217.)));return dist;}
#endif
#ifdef USE_X
float marker_distance(in vec2 p,in int line_cap,in int line_join){p=vec2((p.x+p.y)/SQRT2,(p.x-p.y)/SQRT2);return one_cross(p,line_cap,0.5*v_size.x);}
#endif
#ifdef USE_Y
float marker_distance(in vec2 p,in int line_cap,in int line_join){return one_y(p,line_cap,0.5*v_size.x);}
#endif
float distance_to_fraction(in float dist){return 1.-smoothstep(-0.5*u_antialias,0.5*u_antialias,dist);}float fill_fraction(in float dist){return distance_to_fraction(dist);}float line_fraction(in float dist){return distance_to_fraction(abs(dist)-0.5*v_linewidth);}vec4 fractional_color(in vec4 color,in float fraction){color.a*=fraction;color.rgb*=color.a;return color;}vec4 blend_colors(in vec4 src,in vec4 dest){return(1.-src.a)*dest+src;}
#ifdef APPEND_DOT
float dot_fraction(in vec2 p){float radius=0.125*v_size.x;float dot_distance=max(length(p)-radius,-0.5*u_antialias);return fill_fraction(dot_distance);}
#endif
#ifdef HATCH
float wrap(in float x){return fract(x)-0.5;}vec2 wrap(in vec2 xy){return fract(xy)-0.5;}float hatch_fraction(in vec2 coords,in int hatch_pattern){float scale=v_hatch_scale;coords=coords/scale;float halfwidth=0.5*v_hatch_weight/scale;float dist=u_antialias;if(hatch_pattern==hatch_dot){const float dot_radius=0.25;dist=length(wrap(coords))-dot_radius;}else if(hatch_pattern==hatch_ring){const float ring_radius=0.25;dist=abs(length(wrap(coords))-ring_radius)-halfwidth;}else if(hatch_pattern==hatch_horizontal_line){dist=abs(wrap(coords.y))-halfwidth;}else if(hatch_pattern==hatch_vertical_line){dist=abs(wrap(coords.x))-halfwidth;}else if(hatch_pattern==hatch_cross){dist=min(abs(wrap(coords.x)),abs(wrap(coords.y)))-halfwidth;}else if(hatch_pattern==hatch_horizontal_dash){const float halflength=0.25;dist=max(abs(wrap(coords.y)),abs(wrap(coords.x)+0.25)-halflength)-halfwidth;}else if(hatch_pattern==hatch_vertical_dash){const float halflength=0.25;dist=max(abs(wrap(coords.x)),abs(wrap(coords.y)+0.25)-halflength)-halfwidth;}else if(hatch_pattern==hatch_spiral){vec2 wrap2=wrap(coords);float angle=wrap(atan(wrap2.y,wrap2.x)/(2.*PI));const float dr=PI/15.;float radius=length(wrap2);float frac=fract((radius-dr*angle)/dr);dist=dr*(abs(frac-0.5));dist=min(dist,radius)-halfwidth;}else if(hatch_pattern==hatch_right_diagonal_line){dist=abs(wrap(2.*coords.x+coords.y))/sqrt(5.)-halfwidth;}else if(hatch_pattern==hatch_left_diagonal_line){dist=abs(wrap(2.*coords.x-coords.y))/sqrt(5.)-halfwidth;}else if(hatch_pattern==hatch_diagonal_cross){coords=vec2(coords.x+coords.y+0.5,coords.x-coords.y+0.5);dist=min(abs(wrap(coords.x)),abs(wrap(coords.y)))/SQRT2-halfwidth;}else if(hatch_pattern==hatch_right_diagonal_dash){float across=coords.x+coords.y+0.5;dist=abs(wrap(across))/SQRT2;across=floor(across);float along=wrap(0.5*(coords.x-coords.y+across));const float halflength=0.25;along=abs(along)-halflength;dist=max(dist,along)-halfwidth;}else if(hatch_pattern==hatch_left_diagonal_dash){float across=coords.x-coords.y+0.5;dist=abs(wrap(across))/SQRT2;across=floor(across);float along=wrap(0.5*(coords.x+coords.y+across));const float halflength=0.25;along=abs(along)-halflength;dist=max(dist,along)-halfwidth;}else if(hatch_pattern==hatch_horizontal_wave){float wrapx=wrap(coords.x);float wrapy=wrap(coords.y-0.25+abs(wrapx));dist=abs(wrapy)/SQRT2-halfwidth;}else if(hatch_pattern==hatch_vertical_wave){float wrapy=wrap(coords.y);float wrapx=wrap(coords.x-0.25+abs(wrapy));dist=abs(wrapx)/SQRT2-halfwidth;}else if(hatch_pattern==hatch_criss_cross){float plus=min(abs(wrap(coords.x)),abs(wrap(coords.y)));coords=vec2(coords.x+coords.y+0.5,coords.x-coords.y+0.5);float X=min(abs(wrap(coords.x)),abs(wrap(coords.y)))/SQRT2;dist=min(plus,X)-halfwidth;}return distance_to_fraction(dist*scale);}
#endif
void main(){int line_cap=int(v_line_cap+0.5);int line_join=int(v_line_join+0.5);
#ifdef HATCH
int hatch_pattern=int(v_hatch_pattern+0.5);
#endif
float dist=marker_distance(v_coords,line_cap,line_join);
#ifdef LINE_ONLY
vec4 color=vec4(0.,0.,0.,0.);
#else
float fill_frac=fill_fraction(dist);vec4 color=fractional_color(v_fill_color,fill_frac);
#endif
#if defined(HATCH) && !defined(LINE_ONLY)
if(hatch_pattern>0&&fill_frac>0.){float hatch_frac=hatch_fraction(v_hatch_coords,hatch_pattern);vec4 hatch_color=fractional_color(v_hatch_color,hatch_frac*fill_frac);color=blend_colors(hatch_color,color);}
#endif
float line_frac=line_fraction(dist);
#ifdef APPEND_DOT
line_frac=max(line_frac,dot_fraction(v_coords));
#endif
#ifdef APPEND_CROSS
line_frac=max(line_frac,line_fraction(one_cross(v_coords,line_cap,0.5*v_size.x)));
#endif
#ifdef APPEND_CROSS_2
vec2 lengths=vec2(v_size.x/3.,v_size.x/2.);line_frac=max(line_frac,line_fraction(one_cross_2(v_coords,line_cap,lengths)));
#endif
#ifdef APPEND_X
vec2 p=vec2((v_coords.x+v_coords.y)/SQRT2,(v_coords.x-v_coords.y)/SQRT2);line_frac=max(line_frac,line_fraction(one_cross(p,line_cap,APPEND_X_LEN)));
#endif
#ifdef APPEND_Y
line_frac=max(line_frac,line_fraction(one_y(v_coords,line_cap,0.5*v_size.x)));
#endif
if(line_frac>0.){vec4 line_color=fractional_color(v_line_color,line_frac);color=blend_colors(line_color,color);}gl_FragColor=color;}`;
    exports.default = shader;
},
653: /* models/glyphs/webgl/polygon.vert.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
precision highp float;attribute vec2 a_position;attribute vec4 a_fill_color;attribute float a_edge_distance;
#ifdef HATCH
attribute float a_hatch_pattern;attribute float a_hatch_scale;attribute float a_hatch_weight;attribute vec4 a_hatch_color;
#endif
uniform vec2 u_canvas_size;varying vec4 v_fill_color;varying float v_edge_distance;
#ifdef HATCH
varying float v_hatch_pattern;varying float v_hatch_scale;varying float v_hatch_weight;varying vec4 v_hatch_color;varying vec2 v_hatch_coords;
#endif
void main(){v_fill_color=a_fill_color;v_edge_distance=a_edge_distance;
#ifdef HATCH
v_hatch_pattern=a_hatch_pattern;v_hatch_scale=a_hatch_scale;v_hatch_weight=a_hatch_weight;v_hatch_color=a_hatch_color;v_hatch_coords=a_position;
#endif
vec2 pos=a_position+0.5;pos/=u_canvas_size;gl_Position=vec4(2.*pos.x-1.,1.-2.*pos.y,0.,1.);}`;
    exports.default = shader;
},
654: /* models/glyphs/webgl/polygon.frag.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const shader = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
uniform float u_antialias;varying vec4 v_fill_color;varying float v_edge_distance;
#ifdef HATCH
const float SQRT2=sqrt(2.);const float SQRT3=sqrt(3.);const float PI=3.14159265358979323846;const int hatch_dot=1;const int hatch_ring=2;const int hatch_horizontal_line=3;const int hatch_vertical_line=4;const int hatch_cross=5;const int hatch_horizontal_dash=6;const int hatch_vertical_dash=7;const int hatch_spiral=8;const int hatch_right_diagonal_line=9;const int hatch_left_diagonal_line=10;const int hatch_diagonal_cross=11;const int hatch_right_diagonal_dash=12;const int hatch_left_diagonal_dash=13;const int hatch_horizontal_wave=14;const int hatch_vertical_wave=15;const int hatch_criss_cross=16;varying float v_hatch_pattern;varying float v_hatch_scale;varying float v_hatch_weight;varying vec4 v_hatch_color;varying vec2 v_hatch_coords;float distance_to_fraction(in float dist){return 1.-smoothstep(-0.5*u_antialias,0.5*u_antialias,dist);}vec4 fractional_color(in vec4 color,in float fraction){color.a*=fraction;color.rgb*=color.a;return color;}vec4 blend_colors(in vec4 src,in vec4 dest){return(1.-src.a)*dest+src;}float wrap(in float x){return fract(x)-0.5;}vec2 wrap(in vec2 xy){return fract(xy)-0.5;}float hatch_fraction(in vec2 coords,in int hatch_pattern){float scale=v_hatch_scale;coords=coords/scale;float halfwidth=0.5*v_hatch_weight/scale;float dist=u_antialias;if(hatch_pattern==hatch_dot){const float dot_radius=0.25;dist=length(wrap(coords))-dot_radius;}else if(hatch_pattern==hatch_ring){const float ring_radius=0.25;dist=abs(length(wrap(coords))-ring_radius)-halfwidth;}else if(hatch_pattern==hatch_horizontal_line){dist=abs(wrap(coords.y))-halfwidth;}else if(hatch_pattern==hatch_vertical_line){dist=abs(wrap(coords.x))-halfwidth;}else if(hatch_pattern==hatch_cross){dist=min(abs(wrap(coords.x)),abs(wrap(coords.y)))-halfwidth;}else if(hatch_pattern==hatch_horizontal_dash){const float halflength=0.25;dist=max(abs(wrap(coords.y)),abs(wrap(coords.x)+0.25)-halflength)-halfwidth;}else if(hatch_pattern==hatch_vertical_dash){const float halflength=0.25;dist=max(abs(wrap(coords.x)),abs(wrap(coords.y)+0.25)-halflength)-halfwidth;}else if(hatch_pattern==hatch_spiral){vec2 wrap2=wrap(coords);float angle=wrap(atan(wrap2.y,wrap2.x)/(2.*PI));const float dr=PI/15.;float radius=length(wrap2);float frac=fract((radius-dr*angle)/dr);dist=dr*(abs(frac-0.5));dist=min(dist,radius)-halfwidth;}else if(hatch_pattern==hatch_right_diagonal_line){dist=abs(wrap(2.*coords.x+coords.y))/sqrt(5.)-halfwidth;}else if(hatch_pattern==hatch_left_diagonal_line){dist=abs(wrap(2.*coords.x-coords.y))/sqrt(5.)-halfwidth;}else if(hatch_pattern==hatch_diagonal_cross){coords=vec2(coords.x+coords.y+0.5,coords.x-coords.y+0.5);dist=min(abs(wrap(coords.x)),abs(wrap(coords.y)))/SQRT2-halfwidth;}else if(hatch_pattern==hatch_right_diagonal_dash){float across=coords.x+coords.y+0.5;dist=abs(wrap(across))/SQRT2;across=floor(across);float along=wrap(0.5*(coords.x-coords.y+across));const float halflength=0.25;along=abs(along)-halflength;dist=max(dist,along)-halfwidth;}else if(hatch_pattern==hatch_left_diagonal_dash){float across=coords.x-coords.y+0.5;dist=abs(wrap(across))/SQRT2;across=floor(across);float along=wrap(0.5*(coords.x+coords.y+across));const float halflength=0.25;along=abs(along)-halflength;dist=max(dist,along)-halfwidth;}else if(hatch_pattern==hatch_horizontal_wave){float wrapx=wrap(coords.x);float wrapy=wrap(coords.y-0.25+abs(wrapx));dist=abs(wrapy)/SQRT2-halfwidth;}else if(hatch_pattern==hatch_vertical_wave){float wrapy=wrap(coords.y);float wrapx=wrap(coords.x-0.25+abs(wrapy));dist=abs(wrapx)/SQRT2-halfwidth;}else if(hatch_pattern==hatch_criss_cross){float plus=min(abs(wrap(coords.x)),abs(wrap(coords.y)));coords=vec2(coords.x+coords.y+0.5,coords.x-coords.y+0.5);float X=min(abs(wrap(coords.x)),abs(wrap(coords.y)))/SQRT2;dist=min(plus,X)-halfwidth;}return distance_to_fraction(dist*scale);}
#endif
void main(){vec4 color=v_fill_color;color=vec4(color.rgb*color.a,color.a);
#ifdef HATCH
int hatch_pattern=int(v_hatch_pattern+0.5);if(hatch_pattern>0){float hatch_frac=hatch_fraction(v_hatch_coords,hatch_pattern);vec4 hatch_color=fractional_color(v_hatch_color,hatch_frac);color=blend_colors(hatch_color,color);}
#endif
float edge_alpha=smoothstep(0.,u_antialias,v_edge_distance);color*=edge_alpha;gl_FragColor=color;}`;
    exports.default = shader;
},
655: /* models/glyphs/webgl/annular_wedge.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const sxsy_1 = require(656) /* ./sxsy */;
    class AnnularWedgeGL extends sxsy_1.SXSYGlyphGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return "annular_wedge";
        }
        get outer_radius() {
            return this._widths;
        }
        get inner_radius() {
            return this._heights;
        }
        get start_angle() {
            return this._angles;
        }
        get end_angle() {
            return this._auxs;
        }
        _set_data() {
            super._set_data();
            this.outer_radius.set_from_array(this.glyph.souter_radius);
            this.inner_radius.set_from_array(this.glyph.sinner_radius);
            if (this.glyph.model.direction == "anticlock") {
                this.start_angle.set_from_prop(this.glyph.start_angle);
                this.end_angle.set_from_prop(this.glyph.end_angle);
            }
            else {
                this.start_angle.set_from_prop(this.glyph.end_angle);
                this.end_angle.set_from_prop(this.glyph.start_angle);
            }
        }
    }
    exports.AnnularWedgeGL = AnnularWedgeGL;
},
656: /* models/glyphs/webgl/sxsy.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const single_marker_1 = require(657) /* ./single_marker */;
    const webgl_utils_1 = require(661) /* ./webgl_utils */;
    class SXSYGlyphGL extends single_marker_1.SingleMarkerGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        _set_data() {
            const nmarkers = this.nvertices;
            const centers_array = this._centers.get_sized_array(2 * nmarkers);
            (0, webgl_utils_1.interleave)(this.glyph.sx, this.glyph.sy, nmarkers, single_marker_1.SingleMarkerGL.missing_point, centers_array);
            this._centers.update();
        }
    }
    exports.SXSYGlyphGL = SXSYGlyphGL;
},
657: /* models/glyphs/webgl/single_marker.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_marker_1 = require(658) /* ./base_marker */;
    const buffer_1 = require(660) /* ./buffer */;
    class SingleMarkerGL extends base_marker_1.BaseMarkerGL {
        glyph;
        _show = new buffer_1.Uint8Buffer(this.regl_wrapper);
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        _get_visuals() {
            return this.glyph.visuals;
        }
        draw(indices, main_glyph, transform) {
            this._draw_impl(indices, transform, main_glyph.glglyph);
        }
        _draw_impl(indices, transform, main_gl_glyph) {
            const main_data_changed = main_gl_glyph.data_changed;
            if (main_data_changed || main_gl_glyph.data_mapped) {
                main_gl_glyph.set_data(main_data_changed);
                main_gl_glyph.data_changed = false;
                main_gl_glyph.data_mapped = false;
            }
            // Update derived glyph data if it has overrides
            const derived_data_changed = this.data_changed;
            if (this !== main_gl_glyph && (derived_data_changed || this.data_mapped)) {
                this.set_data(derived_data_changed); // Populate derived buffers
                this.data_changed = false;
                this.data_mapped = false;
            }
            if (this.visuals_changed) {
                this._set_visuals();
                this.visuals_changed = false;
            }
            const nmarkers = main_gl_glyph.nvertices;
            const show_all = indices.length >= nmarkers;
            const has_show_indices = this._show_indices != null;
            const rebuild_show = this._show_nmarkers != nmarkers ||
                (show_all ? has_show_indices : this._have_indices_changed(indices));
            if (rebuild_show) {
                const show_array = this._show.get_sized_array(nmarkers);
                if (show_all) {
                    show_array.fill(255);
                    this._show_indices = null;
                }
                else {
                    show_array.fill(0);
                    for (let i = 0; i < indices.length; i++) {
                        show_array[indices[i]] = 255;
                    }
                    this._show_indices = indices.slice();
                }
                this._show.update();
                this._show_nmarkers = nmarkers;
            }
            this._draw_one_marker_type(this.marker_type, transform, main_gl_glyph, this._show);
        }
    }
    exports.SingleMarkerGL = SingleMarkerGL;
},
658: /* models/glyphs/webgl/base_marker.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_1 = require(659) /* ./base */;
    const buffer_1 = require(660) /* ./buffer */;
    const webgl_utils_1 = require(661) /* ./webgl_utils */;
    // Abstract base class for markers. All markers share the same GLSL, except for
    // one function in the fragment shader that defines the marker geometry and is
    // enabled through a #define.
    class BaseMarkerGL extends base_1.BaseGLGlyph {
        _antialias = 1.5;
        // data properties
        _centers = new buffer_1.Float32Buffer(this.regl_wrapper);
        _widths = new buffer_1.Float32Buffer(this.regl_wrapper);
        _heights = new buffer_1.Float32Buffer(this.regl_wrapper);
        _angles = new buffer_1.Float32Buffer(this.regl_wrapper);
        _auxs = new buffer_1.Float32Buffer(this.regl_wrapper);
        // used by RectGL
        _border_radius = [0.0, 0.0, 0.0, 0.0];
        _border_radius_nonzero = false;
        // indices properties
        _show_indices = null;
        _show_nmarkers = -1;
        // visual properties
        _linewidths = new buffer_1.Float32Buffer(this.regl_wrapper);
        _line_caps = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _line_joins = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _line_rgba = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _fill_rgba = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        // Only needed if have hatch pattern, either all or none of the buffers are set.
        _have_hatch = false;
        _hatch_patterns = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _hatch_scales = new buffer_1.Float32Buffer(this.regl_wrapper);
        _hatch_weights = new buffer_1.Float32Buffer(this.regl_wrapper);
        _hatch_rgba = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        // Avoiding use of nan or inf to represent missing data in webgl as shaders may
        // have reduced floating point precision. So here using a large-ish negative
        // value instead.
        static missing_point = -10000;
        /**
         * Selects appropriate geometry buffers for rendering a marker glyph.
         *
         * This method implements smart buffer selection to support property overrides in derived
         * glyphs (hover_glyph, selection_glyph, muted_glyph). For each geometry property, it
         * checks if the derived glyph has populated its own buffer; if so, that buffer is used,
         * otherwise it falls back to the main glyph's buffer.
         *
         * This pattern enables zero-overhead overrides: derived glyphs that don't override
         * properties simply reuse main glyph buffers, while overrides are handled via lazy
         * buffer creation detected by length checks.
         *
         * @param derived_gl - The glyph being rendered (may be main or derived glyph)
         * @param main_gl_glyph - The main glyph (used as fallback for unpopulated buffers)
         * @returns Object with buffer references for width, height, angle, aux, and border_radius
         *
         * Note: border_radius always uses main glyph buffer (overrides not supported)
         */
        marker_props(derived_gl, main_gl_glyph) {
            // Smart selection: use derived buffer if populated, else main buffer
            const use_derived_width = derived_gl !== main_gl_glyph && derived_gl._widths.length > 0;
            const use_derived_height = derived_gl !== main_gl_glyph && derived_gl._heights.length > 0;
            const use_derived_angle = derived_gl !== main_gl_glyph && derived_gl._angles.length > 0;
            const use_derived_aux = derived_gl !== main_gl_glyph && derived_gl._auxs.length > 0;
            return {
                width: use_derived_width ? derived_gl._widths : main_gl_glyph._widths,
                height: use_derived_height ? derived_gl._heights : main_gl_glyph._heights,
                angle: use_derived_angle ? derived_gl._angles : main_gl_glyph._angles,
                aux: use_derived_aux ? derived_gl._auxs : main_gl_glyph._auxs,
                border_radius: main_gl_glyph._border_radius, // Always from main (overrides not supported)
            };
        }
        get line_props() {
            return {
                linewidth: this._linewidths,
                line_color: this._line_rgba,
                line_cap: this._line_caps,
                line_join: this._line_joins,
            };
        }
        get fill_props() {
            return {
                fill_color: this._fill_rgba,
            };
        }
        get hatch_props() {
            return {
                hatch_pattern: this._hatch_patterns,
                hatch_scale: this._hatch_scales,
                hatch_weight: this._hatch_weights,
                hatch_color: this._hatch_rgba,
            };
        }
        _draw_one_marker_type(marker_type, transform, main_gl_glyph, show) {
            const props_no_hatch = {
                scissor: this.regl_wrapper.scissor,
                viewport: this.regl_wrapper.viewport,
                canvas_size: [transform.width, transform.height],
                size_hint: (0, webgl_utils_1.marker_type_to_size_hint)(marker_type),
                nmarkers: main_gl_glyph.nvertices,
                antialias: this._antialias / transform.pixel_ratio,
                show,
                center: main_gl_glyph._centers, // Always from main (position overrides not supported)
                ...this.marker_props(this, main_gl_glyph),
                ...this.line_props,
                ...this.fill_props,
            };
            if (this._have_hatch) {
                const props_hatch = { ...props_no_hatch, ...this.hatch_props };
                const draw = this.regl_wrapper.marker_hatch(marker_type);
                draw(props_hatch);
            }
            else {
                const draw = this.regl_wrapper.marker_no_hatch(marker_type);
                draw(props_no_hatch);
            }
        }
        _did_set_once = false;
        set_data(data_changed = this.data_changed) {
            if (!this._did_set_once) {
                this._did_set_once = true;
                this._set_once();
            }
            this._set_data(data_changed);
        }
        _set_once() { }
        _set_visuals() {
            const { line, fill, hatch } = this._get_visuals();
            this._linewidths.set_from_prop(line.line_width);
            this._line_caps.set_from_line_cap(line.line_cap);
            this._line_joins.set_from_line_join(line.line_join);
            this._line_rgba.set_from_color(line.line_color, line.line_alpha);
            this._fill_rgba.set_from_color(fill.fill_color, fill.fill_alpha);
            this._have_hatch = hatch.doit;
            if (this._have_hatch) {
                this._hatch_patterns.set_from_hatch_pattern(hatch.hatch_pattern);
                this._hatch_scales.set_from_prop(hatch.hatch_scale);
                this._hatch_weights.set_from_prop(hatch.hatch_weight);
                this._hatch_rgba.set_from_color(hatch.hatch_color, hatch.hatch_alpha);
            }
        }
        _have_indices_changed(indices) {
            const existing = this._show_indices;
            if (existing == null || existing.length !== indices.length) {
                return true;
            }
            const n = indices.length;
            if (n === 0) {
                return false;
            }
            // Endpoints mismatching proves inequality regardless of ordering.
            if (existing[0] !== indices[0] || existing[n - 1] !== indices[n - 1]) {
                return true;
            }
            for (let i = 1; i < n - 1; i++) {
                if (existing[i] !== indices[i]) {
                    return true;
                }
            }
            return false;
        }
    }
    exports.BaseMarkerGL = BaseMarkerGL;
},
659: /* models/glyphs/webgl/base.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    class BaseGLGlyph {
        regl_wrapper;
        glyph;
        nvertices = 0;
        size_changed = false;
        data_changed = false;
        data_mapped = false;
        visuals_changed = false;
        constructor(regl_wrapper, glyph) {
            this.regl_wrapper = regl_wrapper;
            this.glyph = glyph;
        }
        set_data_changed() {
            const { data_size } = this.glyph;
            if (data_size != this.nvertices) {
                this.nvertices = data_size;
                this.size_changed = true;
            }
            this.data_changed = true;
        }
        set_data_mapped() {
            this.data_mapped = true;
        }
        set_visuals_changed() {
            this.visuals_changed = true;
        }
        render(_ctx, indices, mainglyph) {
            if (indices.length == 0) {
                return;
            }
            const { width, height } = this.glyph.renderer.plot_view.canvas_view.primary.canvas;
            const { pixel_ratio } = this.glyph.renderer.plot_view.canvas_view;
            const trans = {
                pixel_ratio, // Needed to scale antialiasing
                width: width / pixel_ratio,
                height: height / pixel_ratio,
            };
            this.draw(indices, mainglyph, trans);
        }
    }
    exports.BaseGLGlyph = BaseGLGlyph;
},
660: /* models/glyphs/webgl/buffer.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.expand_to_per_vertex = expand_to_per_vertex;
    const webgl_utils_1 = require(661) /* ./webgl_utils */;
    const assert_1 = require(13) /* ../../../core/util/assert */;
    const color_1 = require(23) /* ../../../core/util/color */;
    // Arrays are sent to GPU using ReGL Buffer objects.  CPU-side arrays used to
    // update the Buffers are also kept for reuse to avoid unnecessary reallocation.
    class WrappedBuffer {
        regl_wrapper;
        buffer;
        array;
        is_scalar;
        // Number of buffer elements per rendered primitive, e.g. for RGBA buffers this is 4
        // as a single color is 4 x uint8 = 32-bit in total.
        elements_per_primitive;
        constructor(regl_wrapper, elements_per_primitive = 1) {
            this.regl_wrapper = regl_wrapper;
            this.is_scalar = true;
            this.elements_per_primitive = elements_per_primitive;
        }
        // Return array if already know it exists and is the correct length.
        get_array() {
            (0, assert_1.assert)(this.array != null, "WrappedBuffer not yet initialised");
            return this.array;
        }
        // Return array of correct size, creating it if necessary.
        // Must call update() when finished setting the array values.
        get_sized_array(length) {
            if (this.array == null || this.array.length != length) {
                this.array = this.new_array(length);
            }
            return this.array;
        }
        is_normalized() {
            return false;
        }
        get length() {
            return this.array != null ? this.array.length : 0;
        }
        get is_scalar_value() {
            return this.is_scalar;
        }
        set_from_array(numbers) {
            const len = numbers.length;
            const array = this.get_sized_array(len);
            for (let i = 0; i < len; i++) {
                array[i] = numbers[i];
            }
            this.update();
        }
        set_from_prop(prop) {
            const len = prop.is_Scalar() ? 1 : prop.length;
            const array = this.get_sized_array(len);
            for (let i = 0; i < len; i++) {
                array[i] = prop.get(i);
            }
            this.update(prop.is_Scalar());
        }
        set_from_scalar(scalar) {
            this.get_sized_array(1).fill(scalar);
            this.update(true);
        }
        // Return a ReGL AttributeConfig that corresponds to one value for each glyph
        // or the same value for a number of glyphs.  A buffer passed to ReGL for
        // instanced rendering can be used for multiple rendering calls and the
        // important attributes for this are the offset (in bytes) into the buffer
        // and the divisor, which is the number of instances rendered before the
        // offset is advanced to the next buffer element.
        // For non-instanced (polygon/elements) rendering where all attributes
        // must have divisor 0 and data is expanded to per-vertex.
        to_per_vertex_config() {
            return {
                buffer: this.buffer,
                divisor: 0,
                normalized: this.is_normalized(),
                offset: 0,
            };
        }
        // to_attribute_config() is used for the common case of a single render call
        // per buffer with visual properties that are either scalar or vector.
        // Visual properties of scatter markers are an good example, and scalar_divisor
        // would be the number of markers rendered.
        to_attribute_config(offset = 0, scalar_divisor = 1) {
            return {
                buffer: this.buffer,
                divisor: this.is_scalar ? scalar_divisor : 1,
                normalized: this.is_normalized(),
                offset: offset * this.bytes_per_element(),
            };
        }
        // to_attribute_config_nested() is used for the more complicated case in
        // which the vectorisation is nested, such as rendering multi_lines where
        // each visual property has a single buffer that is used multiple times, once
        // for each of the constituent lines.  Vector properties are therefore
        // constant for each constituent line (composed of multiple rendered
        // instances) but change between lines.
        to_attribute_config_nested(offset_vector = 0, divisor = 1) {
            return {
                buffer: this.buffer,
                divisor: divisor * this.elements_per_primitive,
                normalized: this.is_normalized(),
                offset: this.is_scalar ? 0 : offset_vector * this.bytes_per_element() * this.elements_per_primitive,
            };
        }
        // Extract the ith item (of `components` elements) from this buffer into `dst`,
        // marking `dst` as scalar.  If this buffer is already scalar, returns `this`
        // unchanged and `dst` is not touched.
        extract_at(i, components, dst) {
            if (this.is_scalar) {
                return this;
            }
            const src_arr = this.get_array();
            const dst_arr = dst.get_sized_array(components);
            const off = i * components;
            for (let c = 0; c < components; c++) {
                dst_arr[c] = src_arr[off + c];
            }
            dst.update(true);
            return dst;
        }
        // Update ReGL buffer with data contained in array in preparation for passing
        // it to the GPU.  This function must be called after get_sized_array().
        update(is_scalar = false) {
            // Update buffer with data contained in array.
            if (this.buffer == null) {
                // Create new buffer.
                this.buffer = this.regl_wrapper.buffer({
                    usage: "dynamic",
                    data: this.array,
                });
            }
            else {
                // Reuse existing buffer.
                this.buffer({ data: this.array });
            }
            this.is_scalar = is_scalar;
        }
    }
    class Float32Buffer extends WrappedBuffer {
        bytes_per_element() {
            return Float32Array.BYTES_PER_ELEMENT;
        }
        new_array(len) {
            return new Float32Array(len);
        }
    }
    exports.Float32Buffer = Float32Buffer;
    class Uint8Buffer extends WrappedBuffer {
        bytes_per_element() {
            return Uint8Array.BYTES_PER_ELEMENT;
        }
        new_array(len) {
            return new Uint8Array(len);
        }
        set_from_color(color_prop, alpha_prop) {
            const is_scalar_colors = color_prop.is_Scalar();
            const is_scalar = is_scalar_colors && alpha_prop.is_Scalar();
            const ncolors = is_scalar ? 1 : color_prop.length;
            if (!is_scalar_colors) {
                const color_v = color_prop;
                const array = new Uint8Array(color_v.copy_buffer());
                for (let i = 0; i < ncolors; i++) {
                    const alpha = alpha_prop.get(i);
                    array[4 * i + 3] = (0, color_1.byte)(alpha * array[4 * i + 3]);
                }
                this.array = array;
                this.update(is_scalar);
                return;
            }
            const array = this.get_sized_array(4 * ncolors);
            for (let i = 0; i < ncolors; i++) {
                const [r, g, b, a] = (0, color_1.color2rgba)(color_prop.get(i), alpha_prop.get(i));
                array[4 * i] = r;
                array[4 * i + 1] = g;
                array[4 * i + 2] = b;
                array[4 * i + 3] = a;
            }
            this.update(is_scalar);
        }
        set_from_hatch_pattern(hatch_pattern_prop) {
            const len = hatch_pattern_prop.is_Scalar() ? 1 : hatch_pattern_prop.length;
            const array = this.get_sized_array(len);
            for (let i = 0; i < len; i++) {
                array[i] = (0, webgl_utils_1.hatch_pattern_to_index)(hatch_pattern_prop.get(i));
            }
            this.update(hatch_pattern_prop.is_Scalar());
        }
        set_from_line_cap(line_cap_prop) {
            const len = line_cap_prop.is_Scalar() ? 1 : line_cap_prop.length;
            const array = this.get_sized_array(len);
            for (let i = 0; i < len; i++) {
                array[i] = webgl_utils_1.cap_lookup[line_cap_prop.get(i)];
            }
            this.update(line_cap_prop.is_Scalar());
        }
        set_from_line_join(line_join_prop) {
            const len = line_join_prop.is_Scalar() ? 1 : line_join_prop.length;
            const array = this.get_sized_array(len);
            for (let i = 0; i < len; i++) {
                array[i] = webgl_utils_1.join_lookup[line_join_prop.get(i)];
            }
            this.update(line_join_prop.is_Scalar());
        }
    }
    exports.Uint8Buffer = Uint8Buffer;
    // Normalized refers to optional WebGL behaviour of automatically converting
    // Uint8 values that are passed to shaders into floats in the range 0 to 1.
    class NormalizedUint8Buffer extends Uint8Buffer {
        is_normalized() {
            return true;
        }
    }
    exports.NormalizedUint8Buffer = NormalizedUint8Buffer;
    // Expand a scalar or per-item source buffer to per-vertex in the destination buffer.
    // Used for non-instanced polygon rendering where all attributes need divisor 0.
    // components is the number of elements per item (e.g. 4 for RGBA).
    function expand_to_per_vertex(src, dst, vertex_counts, components) {
        const src_arr = src.get_array();
        let total = 0;
        for (const c of vertex_counts) {
            total += c;
        }
        const dst_arr = dst.get_sized_array(total * components);
        let offset = 0;
        for (let i = 0; i < vertex_counts.length; i++) {
            const src_offset = src.is_scalar_value ? 0 : i * components;
            for (let j = 0; j < vertex_counts[i]; j++) {
                for (let c = 0; c < components; c++) {
                    dst_arr[offset++] = src_arr[src_offset + c];
                }
            }
        }
        dst.update();
    }
},
661: /* models/glyphs/webgl/webgl_utils.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.interleave = interleave;
    exports.hatch_pattern_to_index = hatch_pattern_to_index;
    exports.marker_type_to_size_hint = marker_type_to_size_hint;
    const patterns_1 = require(105) /* ../../../core/visuals/patterns */;
    function interleave(arr0, arr1, n, alt, out) {
        for (let i = 0; i < n; i++) {
            const v0 = arr0[i];
            const v1 = arr1[i];
            if (isFinite(v0 + v1)) {
                out[2 * i] = v0;
                out[2 * i + 1] = v1;
            }
            else {
                out[2 * i] = alt;
                out[2 * i + 1] = alt;
            }
        }
    }
    // WebGL shaders use integers for caps, joins and hatching.
    exports.cap_lookup = { butt: 0, round: 1, square: 2 };
    exports.join_lookup = { miter: 0, round: 1, bevel: 2 };
    const hatch_pattern_lookup = {
        blank: 0,
        dot: 1,
        ring: 2,
        horizontal_line: 3,
        vertical_line: 4,
        cross: 5,
        horizontal_dash: 6,
        vertical_dash: 7,
        spiral: 8,
        right_diagonal_line: 9,
        left_diagonal_line: 10,
        diagonal_cross: 11,
        right_diagonal_dash: 12,
        left_diagonal_dash: 13,
        horizontal_wave: 14,
        vertical_wave: 15,
        criss_cross: 16,
    };
    function hatch_pattern_to_index(pattern) {
        return hatch_pattern_lookup[patterns_1.hatch_aliases[pattern] ?? pattern] ?? 0;
    }
    function marker_type_to_size_hint(marker_type) {
        // Marker size hint is only used here and in the marker fragment shader.
        switch (marker_type) {
            case "dash":
                return 1;
            case "dot":
                return 2;
            case "diamond":
            case "diamond_cross":
            case "diamond_dot":
                return 3;
            case "hex":
            case "hex_tile":
                return 4;
            case "square_pin":
                return 5;
            case "inverted_triangle":
            case "ngon":
            case "triangle":
            case "triangle_dot":
                return 6;
            case "triangle_pin":
                return 7;
            case "star":
            case "star_dot":
                return 8;
            default:
                return 0;
        }
    }
},
662: /* models/glyphs/webgl/annulus.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const sxsy_1 = require(656) /* ./sxsy */;
    class AnnulusGL extends sxsy_1.SXSYGlyphGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return "annulus";
        }
        get outer_radius() {
            return this._widths;
        }
        get inner_radius() {
            return this._heights;
        }
        _set_data() {
            super._set_data();
            this.outer_radius.set_from_array(this.glyph.souter_radius);
            this.inner_radius.set_from_array(this.glyph.sinner_radius);
        }
        _set_once() {
            super._set_once();
            this._angles.set_from_scalar(0);
            this._auxs.set_from_scalar(0);
        }
    }
    exports.AnnulusGL = AnnulusGL;
},
663: /* models/glyphs/webgl/base_line.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.line_bounds_padding = line_bounds_padding;
    const base_1 = require(659) /* ./base */;
    const buffer_1 = require(660) /* ./buffer */;
    const line_1 = require(100) /* ../../../core/visuals/line */;
    const dash_cache_1 = require(643) /* ./dash_cache */;
    exports.LINE_AA_WIDTH = 1.5;
    exports.LINE_MITER_LIMIT = 10.0;
    /** Extra screen-space padding needed to enclose a rendered line. A miter join
     * can extend by half the line width times the miter limit, and antialiasing
     * adds a fringe beyond that geometry. */
    function line_bounds_padding(linewidth) {
        return exports.LINE_AA_WIDTH + exports.LINE_MITER_LIMIT * linewidth / 2;
    }
    class BaseLineGL extends base_1.BaseGLGlyph {
        glyph;
        _antialias = exports.LINE_AA_WIDTH; // Make this larger to test antialiasing at edges.
        _miter_limit = exports.LINE_MITER_LIMIT; // Threshold for miters to be replaced by bevels.
        // data properties
        _points;
        _show; // Applies to segments not points.
        // visual properties
        _linewidth = new buffer_1.Float32Buffer(this.regl_wrapper);
        _line_color = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _line_cap = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _line_join = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _is_dashed = false;
        // visual properties that are only used if line is dashed.
        _length_so_far; // Depends on both data and visuals.
        _dash_tex = [];
        _dash_tex_info;
        _dash_scale;
        _dash_offset;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        _draw_single(main_gl_glyph, transform, line_offset, point_offset, nsegments, framebuffer, show = null) {
            const linewidths = this._linewidth.get_array();
            const linewidth = linewidths[this._linewidth.is_scalar_value ? 0 : line_offset];
            const points = main_gl_glyph._points.get_array().subarray(point_offset, point_offset + 2 * (nsegments + 3));
            const padding = line_bounds_padding(linewidth);
            const scissor = this.regl_wrapper.scissor_for_points(points, padding, transform.pixel_ratio);
            const solid_props = {
                scissor,
                viewport: this.regl_wrapper.viewport,
                canvas_size: [transform.width, transform.height],
                antialias: this._antialias / transform.pixel_ratio,
                miter_limit: this._miter_limit,
                points: main_gl_glyph._points,
                show: show ?? main_gl_glyph._show,
                nsegments,
                linewidth: this._linewidth,
                line_color: this._line_color,
                line_cap: this._line_cap,
                line_join: this._line_join,
                framebuffer,
                point_offset,
                line_offset,
            };
            const dash_index = this._dash_tex.length == 1 ? 0 : line_offset;
            if (this._is_dashed && this._dash_tex[dash_index] != null) {
                const dashed_props = {
                    ...solid_props,
                    length_so_far: main_gl_glyph._length_so_far,
                    dash_tex: this._dash_tex[dash_index],
                    dash_tex_info: this._dash_tex_info,
                    dash_scale: this._dash_scale,
                    dash_offset: this._dash_offset,
                };
                this.regl_wrapper.dashed_line()(dashed_props);
            }
            else {
                this.regl_wrapper.solid_line()(solid_props);
            }
            return scissor;
        }
        _set_length_single(length_so_far, points, show) {
            // Set length so far for a single line from the points and show flags for that line.
            // Only needed if line is dashed.
            const nsegments = length_so_far.length;
            let length = 0.0;
            for (let i = 0; i < nsegments; i++) {
                length_so_far[i] = length;
                if (show[i + 1] == 1) {
                    length += Math.sqrt((points[2 * i + 4] - points[2 * i + 2]) ** 2 +
                        (points[2 * i + 5] - points[2 * i + 3]) ** 2);
                }
                else {
                    // Reset to zero at invalid point.
                    length = 0.0;
                }
            }
        }
        _set_points_single(points, sx, sy) {
            // Set points array for a single line.
            const npoints = points.length / 2 - 2;
            const is_closed = (npoints > 2 && sx[0] == sx[npoints - 1] && sy[0] == sy[npoints - 1] &&
                isFinite(sx[0] + sy[0]));
            for (let i = 1; i < npoints + 1; i++) {
                points[2 * i] = sx[i - 1];
                points[2 * i + 1] = sy[i - 1];
            }
            if (is_closed) {
                points[0] = points[2 * npoints - 2]; // Last but one point.
                points[1] = points[2 * npoints - 1];
                points[2 * npoints + 2] = points[4]; // Second point.
                points[2 * npoints + 3] = points[5];
            }
            else {
                points[0] = 0.0;
                points[1] = 0.0;
                points[2 * npoints + 2] = 0.0;
                points[2 * npoints + 3] = 0.0;
            }
        }
        _set_show_single(show, points) {
            // Set show flags for a single line from the points of that line.
            // Do not show line segments which have a NaN coordinate at either end, and
            // also take account of line being closed (start and end points identical).
            const npoints = points.length / 2 - 2;
            let start_finite = isFinite(points[2] + points[3]);
            for (let i = 1; i < npoints; i++) {
                const end_finite = isFinite(points[2 * i + 2] + points[2 * i + 3]);
                show[i] = (start_finite && end_finite) ? 1 : 0;
                start_finite = end_finite;
            }
            const is_closed = npoints > 2 && points[0] == points[2 * npoints - 2] && points[1] == points[2 * npoints - 1];
            if (is_closed) {
                show[0] = show[npoints - 1];
                show[npoints] = show[1];
            }
            else {
                show[0] = 0;
                show[npoints] = 0;
            }
        }
        _set_visuals() {
            const line_visuals = this._get_visuals();
            this._line_color.set_from_color(line_visuals.line_color, line_visuals.line_alpha);
            this._linewidth.set_from_prop(line_visuals.line_width);
            this._line_cap.set_from_line_cap(line_visuals.line_cap);
            this._line_join.set_from_line_join(line_visuals.line_join);
            const { line_dash } = line_visuals;
            const dash_count = line_dash.is_Scalar() ? 1 : line_dash.length;
            const dash_patterns = new Array(dash_count);
            this._is_dashed = false;
            for (let i = 0; i < dash_count; i++) {
                const pattern = (0, dash_cache_1.normalize_dash_pattern)((0, line_1.resolve_line_dash)(line_dash.get(i)));
                dash_patterns[i] = pattern;
                this._is_dashed ||= pattern.length != 0;
            }
            // Visual updates replace, rather than append to, the previous texture map.
            this._dash_tex = [];
            if (this._is_dashed) {
                if (this._dash_offset == null) {
                    this._dash_offset = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                this._dash_offset.set_from_prop(line_visuals.line_dash_offset);
                const n = dash_count;
                if (this._dash_tex_info == null) {
                    this._dash_tex_info = new buffer_1.Float32Buffer(this.regl_wrapper, 4);
                }
                const dash_tex_info = this._dash_tex_info.get_sized_array(4 * n);
                if (this._dash_scale == null) {
                    this._dash_scale = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                const dash_scale = this._dash_scale.get_sized_array(n);
                for (let i = 0; i < n; i++) {
                    const arr = dash_patterns[i];
                    if (arr.length > 0) {
                        // This line is dashed
                        const [tex_info, tex, scale] = this.regl_wrapper.get_dash(arr);
                        this._dash_tex.push(tex);
                        for (let j = 0; j < 4; j++) {
                            dash_tex_info[4 * i + j] = tex_info[j];
                        }
                        dash_scale[i] = scale;
                    }
                    else {
                        // This line is solid
                        this._dash_tex.push(null);
                        dash_tex_info.fill(0, 4 * i, 4 * (i + 1));
                        dash_scale[i] = 0;
                    }
                }
                this._dash_tex_info.update(line_dash.is_Scalar());
                this._dash_scale.update(line_dash.is_Scalar());
            }
        }
    }
    exports.BaseLineGL = BaseLineGL;
},
664: /* models/glyphs/webgl/circle.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const radial_1 = require(665) /* ./radial */;
    class CircleGL extends radial_1.RadialGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return "circle";
        }
        _set_once() {
            super._set_once();
            this._angles.set_from_scalar(0);
        }
    }
    exports.CircleGL = CircleGL;
},
665: /* models/glyphs/webgl/radial.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const sxsy_1 = require(656) /* ./sxsy */;
    const arrayable_1 = require(14) /* ../../../core/util/arrayable */;
    class RadialGL extends sxsy_1.SXSYGlyphGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        // TODO: should be 'radius'
        get size() {
            return this._widths;
        }
        _set_data() {
            super._set_data();
            // Ideally we wouldn't multiply here, but currently handling of
            // circle glyph and scatter with circle marker is handled with
            // a single code path.
            this.size.set_from_array((0, arrayable_1.mul)(this.glyph.sradius, 2.0));
        }
        _set_once() {
            super._set_once();
            this._heights.set_from_scalar(0);
        }
    }
    exports.RadialGL = RadialGL;
},
666: /* models/glyphs/webgl/hex_tile.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const sxsy_1 = require(656) /* ./sxsy */;
    class HexTileGL extends sxsy_1.SXSYGlyphGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return "hex_tile";
        }
        _set_data() {
            super._set_data();
            let width;
            let height;
            if (this.glyph.model.orientation == "pointytop") {
                this._angles.set_from_scalar(0.5 * Math.PI);
                width = this.glyph.svy[0] * 2;
                height = this.glyph.svx[4] * 4 / Math.sqrt(3);
            }
            else {
                this._angles.set_from_scalar(0);
                width = this.glyph.svx[0] * 2;
                height = this.glyph.svy[4] * 4 / Math.sqrt(3);
            }
            const { scale } = this.glyph;
            this._widths.set_from_prop(scale.map((scale_i) => width * scale_i));
            this._heights.set_from_prop(scale.map((scale_i) => height * scale_i));
        }
        _set_once() {
            super._set_once();
            this._auxs.set_from_scalar(0);
        }
    }
    exports.HexTileGL = HexTileGL;
},
667: /* models/glyphs/webgl/image.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_1 = require(659) /* ./base */;
    const buffer_1 = require(660) /* ./buffer */;
    const assert_1 = require(13) /* ../../../core/util/assert */;
    class ImageGL extends base_1.BaseGLGlyph {
        glyph;
        // data properties
        _tex = [];
        _bounds = [];
        // image_changed is separate from data_changed as it can occur through changed colormapping.
        _image_changed = false;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        draw(indices, main_glyph, transform) {
            const main_gl_glyph = main_glyph.glglyph;
            // The only visual property that can change is global_alpha and that is read on every render,
            // so ignore this.visuals_changed
            const data_changed_or_mapped = main_gl_glyph.data_changed || main_gl_glyph.data_mapped;
            if (data_changed_or_mapped) {
                // Handle change of location or bounds.
                main_gl_glyph._set_data();
            }
            if (main_gl_glyph._image_changed || main_gl_glyph.data_changed) {
                // Handle change of image itself. If _image_changed then image has definitely changed such as
                // from a change of colormapping. If data_changed then image may have changed so update just
                // in case. If we could identify what in the CDS has changed (e.g. image or x) then we would
                // know whether to call _set_image or not.
                main_gl_glyph._set_image();
            }
            main_gl_glyph.data_changed = false;
            main_gl_glyph.data_mapped = false;
            main_gl_glyph._image_changed = false;
            const { global_alpha } = this.glyph.visuals.image;
            for (const i of indices) {
                if (main_gl_glyph._tex[i] == null || main_gl_glyph._bounds[i] == null) {
                    continue;
                }
                const props = {
                    scissor: this.regl_wrapper.scissor,
                    viewport: this.regl_wrapper.viewport,
                    canvas_size: [transform.width, transform.height],
                    bounds: main_gl_glyph._bounds[i],
                    tex: main_gl_glyph._tex[i],
                    global_alpha: global_alpha.get(i),
                };
                this.regl_wrapper.image()(props);
            }
        }
        set_image_changed() {
            this._image_changed = true;
        }
        _set_data() {
            const { image } = this.glyph;
            const nimage = image.length;
            if (this._bounds.length != nimage) {
                this._bounds = Array(nimage).fill(null);
            }
            for (let i = 0; i < nimage; i++) {
                const { sx, sy, sdw: sw, sdh: sh, xy_anchor, xy_scale, xy_sign } = this.glyph;
                const sx_i = sx[i];
                const sy_i = sy[i];
                const sw_i = sw[i];
                const sh_i = sh[i];
                if (!isFinite(sx_i + sy_i + sw_i + sh_i)) {
                    this._bounds[i] = null;
                    continue;
                }
                if (this._bounds[i] == null) {
                    this._bounds[i] = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                const bounds_array = this._bounds[i].get_sized_array(4);
                bounds_array[0] = sx[i] + sw[i] * (0.5 * (1 - xy_scale.x) - xy_anchor.x) * xy_sign.x;
                bounds_array[1] = sy[i] + sh[i] * (0.5 * (1 - xy_scale.y) - xy_anchor.y) * xy_sign.y;
                bounds_array[2] = bounds_array[0] + sw[i] * xy_scale.x * xy_sign.x;
                bounds_array[3] = bounds_array[1] + sh[i] * xy_scale.y * xy_sign.y;
                this._bounds[i].update();
            }
        }
        _set_image() {
            const { image, image_data } = this.glyph;
            const nimage = image.length;
            (0, assert_1.assert)(image_data != null);
            if (this._tex.length != nimage) {
                this._tex = Array(nimage).fill(null);
            }
            for (let i = 0; i < nimage; i++) {
                const image_data_i = image_data[i];
                if (image_data_i == null) {
                    this._tex[i] = null;
                    continue;
                }
                const tex_options = {
                    width: image_data_i.width,
                    height: image_data_i.height,
                    data: image_data_i,
                    format: "rgba",
                    type: "uint8",
                };
                if (this._tex[i] == null) {
                    this._tex[i] = this.regl_wrapper.texture(tex_options);
                }
                else {
                    this._tex[i](tex_options); // Reuse existing WebGL texture
                }
            }
        }
    }
    exports.ImageGL = ImageGL;
},
668: /* models/glyphs/webgl/line_gl.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const buffer_1 = require(660) /* ./buffer */;
    const single_line_1 = require(669) /* ./single_line */;
    class LineGL extends single_line_1.SingleLineGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        draw(indices, main_glyph, transform) {
            this._draw_impl(indices, transform, main_glyph.glglyph);
        }
        _get_show_buffer(indices, main_gl_glyph) {
            // If displaying all indices use main glyph's _show.
            // Otherwise use this._show which is updated from the indices and uses
            // main glyph's show to identify if (x, y) are finite or not.
            const main_show = main_gl_glyph._show;
            let show = main_show;
            if (indices.length != main_show.length - 1) {
                const nonselection = this.glyph.parent.nonselection_glyph == this.glyph;
                const n = main_show.length;
                const main_show_array = main_show.get_sized_array(n);
                if (this._show == null) {
                    this._show = new buffer_1.Uint8Buffer(this.regl_wrapper);
                }
                const show_array = this._show.get_sized_array(n); // equal to npoints+1
                show_array.fill(0);
                let iprev = indices[0]; // Previous index
                if (nonselection && iprev > 0) {
                    show_array[iprev] = main_show_array[iprev]; // Start of first line
                }
                for (let k = 1; k < indices.length; k++) {
                    const i = indices[k];
                    if (i == iprev + 1) {
                        show_array[i] = main_show_array[i];
                    }
                    else if (nonselection) {
                        // Gap in indices, end previous line and start new one
                        show_array[iprev + 1] = main_show_array[iprev + 1];
                        show_array[i] = main_show_array[i];
                    }
                    iprev = i;
                }
                // iprev is now the last index
                if (nonselection && iprev != n - 2) {
                    show_array[iprev + 1] = main_show_array[iprev + 1]; // End of last line
                }
                this._show.update();
                show = this._show;
            }
            return show;
        }
        _get_visuals() {
            return this.glyph.visuals.line;
        }
        _set_data_points() {
            const sx = this.glyph.sx;
            const sy = this.glyph.sy;
            const npoints = sx.length;
            if (this._points == null) {
                this._points = new buffer_1.Float32Buffer(this.regl_wrapper);
            }
            const points_array = this._points.get_sized_array((npoints + 2) * 2);
            this._set_points_single(points_array, sx, sy);
            this._points.update();
            return points_array;
        }
    }
    exports.LineGL = LineGL;
},
669: /* models/glyphs/webgl/single_line.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_line_1 = require(663) /* ./base_line */;
    const buffer_1 = require(660) /* ./buffer */;
    class SingleLineGL extends base_line_1.BaseLineGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        _draw_impl(indices, transform, main_gl_glyph) {
            if (this.visuals_changed) {
                this._set_visuals();
                this.visuals_changed = false;
            }
            const data_changed_or_mapped = main_gl_glyph.data_changed || main_gl_glyph.data_mapped;
            if (data_changed_or_mapped) {
                main_gl_glyph._set_data(main_gl_glyph.data_changed);
            }
            if ((data_changed_or_mapped && main_gl_glyph._is_dashed) || this._is_dashed) {
                // length_so_far is a data property as it depends on point positions in canvas coordinates
                // but is only needed for dashed lines so it also depends on visual properties.
                // Care needed if base glyph is solid but e.g. nonselection glyph is dashed.
                main_gl_glyph._set_length();
            }
            if (data_changed_or_mapped) {
                main_gl_glyph.data_changed = false;
                main_gl_glyph.data_mapped = false;
            }
            // Get show buffer to account for selected indices.
            const show = this._get_show_buffer(indices, main_gl_glyph);
            const npoints = main_gl_glyph._points.length / 2 - 2;
            const nsegments = npoints - 1;
            this._draw_single(main_gl_glyph, transform, 0, 0, nsegments, null, show);
        }
        _set_data(data_changed) {
            // If data_changed is false the underlying glyph data has not changed but has been mapped to
            // different canvas coordinates e.g. via pan or zoom. If data_changed is true the data itself
            // has changed, which also implies it has been mapped.
            const points_array = this._set_data_points();
            if (data_changed) {
                // show flags for data, taking into account NaNs but not selected indices
                // Points array includes extra points at each end
                const npoints = points_array.length / 2 - 2;
                if (this._show == null) {
                    this._show = new buffer_1.Uint8Buffer(this.regl_wrapper);
                }
                const show_array = this._show.get_sized_array(npoints + 1);
                this._set_show_single(show_array, points_array);
                this._show.update();
            }
        }
        _set_length() {
            const points_array = this._points.get_array();
            const show_array = this._show.get_array();
            // Points array includes extra points at each end
            const npoints = points_array.length / 2 - 2;
            if (this._length_so_far == null) {
                this._length_so_far = new buffer_1.Float32Buffer(this.regl_wrapper);
            }
            const length_so_far = this._length_so_far.get_sized_array(npoints - 1);
            this._set_length_single(length_so_far, points_array, show_array);
            this._length_so_far.update();
        }
    }
    exports.SingleLineGL = SingleLineGL;
},
670: /* models/glyphs/webgl/lrtb.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const single_marker_1 = require(657) /* ./single_marker */;
    const { abs } = Math;
    class LRTBGL extends single_marker_1.SingleMarkerGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return this._border_radius_nonzero ? "round_rect" : "rect";
        }
        _set_data() {
            const nmarkers = this.nvertices;
            const centers_array = this._centers.get_sized_array(nmarkers * 2);
            const widths_array = this._widths.get_sized_array(nmarkers);
            const heights_array = this._heights.get_sized_array(nmarkers);
            const { sleft, sright, stop, sbottom } = this.glyph;
            const { missing_point } = single_marker_1.SingleMarkerGL;
            for (let i = 0; i < nmarkers; i++) {
                const l = sleft[i];
                const r = sright[i];
                const t = stop[i];
                const b = sbottom[i];
                if (isFinite(l + r + t + b)) {
                    centers_array[2 * i] = (l + r) / 2;
                    centers_array[2 * i + 1] = (t + b) / 2;
                    widths_array[i] = abs(r - l);
                    heights_array[i] = abs(t - b);
                }
                else {
                    centers_array[2 * i] = missing_point;
                    centers_array[2 * i + 1] = missing_point;
                    widths_array[i] = missing_point;
                    heights_array[i] = missing_point;
                }
            }
            this._centers.update();
            this._widths.update();
            this._heights.update();
            this._angles.set_from_scalar(0);
            if (this.glyph.border_radius != null) {
                const { top_left, top_right, bottom_right, bottom_left } = this.glyph.border_radius;
                this._border_radius = [top_left, top_right, bottom_right, bottom_left];
                this._border_radius_nonzero = Math.max(...this._border_radius) > 0.0;
            }
            else {
                this._border_radius = [0, 0, 0, 0];
                this._border_radius_nonzero = false;
            }
        }
        _set_once() {
            super._set_once();
            this._auxs.set_from_scalar(0);
        }
    }
    exports.LRTBGL = LRTBGL;
},
671: /* models/glyphs/webgl/multi_line.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_line_1 = require(663) /* ./base_line */;
    const buffer_1 = require(660) /* ./buffer */;
    class MultiLineGL extends base_line_1.BaseLineGL {
        glyph;
        _point_offsets = [];
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        draw(indices, main_glyph, transform) {
            // Indices refer to whole lines not line segments
            if (this.visuals_changed) {
                this._set_visuals();
                this.visuals_changed = false;
            }
            const main_gl_glyph = main_glyph.glglyph;
            const data_changed_or_mapped = main_gl_glyph.data_changed || main_gl_glyph.data_mapped;
            if (data_changed_or_mapped) {
                main_gl_glyph._set_data(main_gl_glyph.data_changed);
            }
            if ((data_changed_or_mapped && main_gl_glyph._is_dashed) || this._is_dashed) {
                // length_so_far is a data property as it depends on point positions in canvas coordinates
                // but is only needed for dashed lines so it also depends on visual properties.
                // Care needed if base glyph is solid but e.g. nonselection glyph is dashed.
                main_gl_glyph._set_length();
            }
            if (data_changed_or_mapped) {
                main_gl_glyph.data_changed = false;
                main_gl_glyph.data_mapped = false;
            }
            const { data_size } = this.glyph; // Number of lines
            let framebuffer = null;
            let tex = null;
            if (data_size > 1) {
                [framebuffer, tex] = this.regl_wrapper.framebuffer_and_texture;
            }
            for (const index of indices) {
                const npoints = main_glyph.sxs.get(index).length;
                const nsegments = npoints - 1; // Points array includes extra points at each end
                if (nsegments <= 0) {
                    continue;
                }
                const point_offset = main_gl_glyph._point_offsets[index];
                // Not necessary if just a single line
                if (framebuffer != null) {
                    this.regl_wrapper.clear_framebuffer(framebuffer);
                }
                const scissor = this._draw_single(main_gl_glyph, transform, index, point_offset, nsegments, framebuffer);
                if (framebuffer != null) {
                    // Accumulate framebuffer to WebGL canvas
                    const accumulate_props = {
                        scissor,
                        viewport: this.regl_wrapper.viewport,
                        framebuffer_tex: tex,
                    };
                    this.regl_wrapper.accumulate()(accumulate_props);
                }
            }
        }
        _get_visuals() {
            return this.glyph.visuals.line;
        }
        _set_data(data_changed) {
            // If data_changed is false the underlying glyph data has not changed but has been mapped to
            // different canvas coordinates e.g. via pan or zoom. If data_changed is true the data itself
            // has changed, which also implies it has been mapped.
            // Set data properties which are points and show flags for data
            // (taking into account NaNs but not selected indices)
            const line_count = this.glyph.data_size;
            const total_point_count = this.glyph.sxs.data.length;
            if (this._points == null) {
                this._points = new buffer_1.Float32Buffer(this.regl_wrapper);
            }
            const points_array = this._points.get_sized_array((total_point_count + 2 * line_count) * 2);
            let point_offset = 0;
            for (let i = 0; i < line_count; i++) {
                if (data_changed) {
                    this._point_offsets[i] = point_offset;
                }
                // Process a single line at a time.
                const sx = this.glyph.sxs.get(i);
                const sy = this.glyph.sys.get(i);
                const npoints = sx.length;
                const points = points_array.subarray(point_offset, point_offset + (npoints + 2) * 2);
                this._set_points_single(points, sx, sy);
                point_offset += (npoints + 2) * 2;
            }
            if (data_changed) {
                this._point_offsets.length = line_count;
            }
            this._points.update();
            if (data_changed) {
                if (this._show == null) {
                    this._show = new buffer_1.Uint8Buffer(this.regl_wrapper);
                }
                const show_array = this._show.get_sized_array(total_point_count + line_count);
                let point_offset = 0;
                let show_offset = 0;
                for (let i = 0; i < line_count; i++) {
                    // Process a single line at a time.
                    const sx = this.glyph.sxs.get(i);
                    const npoints = sx.length;
                    const points = points_array.subarray(point_offset, point_offset + (npoints + 2) * 2);
                    const show = show_array.subarray(show_offset, show_offset + npoints + 1);
                    this._set_show_single(show, points);
                    point_offset += (npoints + 2) * 2;
                    show_offset += npoints + 1;
                }
                this._show.update();
            }
        }
        _set_length() {
            const line_count = this.glyph.data_size;
            const total_point_count = this.glyph.sxs.data.length;
            const points_array = this._points.get_array();
            const show_array = this._show.get_array();
            if (this._length_so_far == null) {
                this._length_so_far = new buffer_1.Float32Buffer(this.regl_wrapper);
            }
            const length_so_far = this._length_so_far.get_sized_array(total_point_count - line_count);
            let point_offset = 0;
            let show_offset = 0;
            let length_offset = 0;
            for (let i = 0; i < line_count; i++) {
                const sx = this.glyph.sxs.get(i);
                const npoints = sx.length;
                const nsegments = npoints - 1;
                const points = points_array.subarray(point_offset, point_offset + (npoints + 2) * 2);
                const show = show_array.subarray(show_offset, show_offset + npoints + 1);
                const length = length_so_far.subarray(length_offset, length_offset + nsegments);
                this._set_length_single(length, points, show);
                point_offset += (npoints + 2) * 2;
                show_offset += npoints + 1;
                length_offset += nsegments;
            }
            this._length_so_far.update();
        }
    }
    exports.MultiLineGL = MultiLineGL;
},
672: /* models/glyphs/webgl/patch.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_1 = require(659) /* ./base */;
    const buffer_1 = require(660) /* ./buffer */;
    const line_1 = require(100) /* ../../../core/visuals/line */;
    const dash_cache_1 = require(643) /* ./dash_cache */;
    const base_line_1 = require(663) /* ./base_line */;
    const polygon_1 = require(673) /* ../../../core/util/polygon */;
    const polygon_2 = require(674) /* ./polygon */;
    class PatchGL extends base_1.BaseGLGlyph {
        glyph;
        // Fill buffers
        _positions;
        _edge_distance;
        _elements = null;
        // Per-vertex visual buffers for polygon fill (divisor 0)
        _pv_fill_color = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _pv_hatch_patterns = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _pv_hatch_scales = new buffer_1.Float32Buffer(this.regl_wrapper);
        _pv_hatch_weights = new buffer_1.Float32Buffer(this.regl_wrapper);
        _pv_hatch_rgba = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        // Source visual buffers (scalar, from _set_visuals)
        _fill_color = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _have_hatch = false;
        _hatch_patterns = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _hatch_scales = new buffer_1.Float32Buffer(this.regl_wrapper);
        _hatch_weights = new buffer_1.Float32Buffer(this.regl_wrapper);
        _hatch_rgba = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        // Stroke upload buffers (reuse line infrastructure)
        _line_points_buf;
        _line_show_buf;
        _linewidth = new buffer_1.Float32Buffer(this.regl_wrapper);
        _line_color = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _line_cap = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _line_join = new buffer_1.Uint8Buffer(this.regl_wrapper);
        // Dash state
        _is_dashed = false;
        _length_so_far_buf;
        _dash_tex = [];
        _dash_tex_info;
        _dash_scale;
        _dash_offset;
        _triangle_count = 0;
        _nvertices = 0;
        _ring_data = [];
        _pv_dirty = true;
        _pv_elements = null;
        _topology;
        _topology_scales;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        draw(_indices, main_glyph, transform) {
            const main_patch = main_glyph;
            const main_gl = main_patch.glglyph;
            const derived_data_changed = this !== main_gl && this.data_changed;
            if (this.visuals_changed) {
                this._set_visuals();
                this.visuals_changed = false;
                this._pv_dirty = true;
            }
            const data_changed = main_gl.data_changed;
            const data_changed_or_mapped = data_changed || main_gl.data_mapped;
            if (data_changed_or_mapped) {
                main_gl._set_data(data_changed);
                main_gl.data_changed = false;
                main_gl.data_mapped = false;
                this._pv_dirty ||= data_changed || derived_data_changed;
            }
            if (this !== main_gl && (this.data_changed || this.data_mapped)) {
                this.data_changed = false;
                this.data_mapped = false;
                this._pv_dirty = true;
            }
            // Remapping can change the finite contours without changing source data.
            // Each visual variant must notice the resulting vertex layout change.
            if (this._pv_elements !== main_gl._elements) {
                this._pv_elements = main_gl._elements;
                this._pv_dirty = true;
            }
            if (main_gl._triangle_count == 0 && main_gl._ring_data.length == 0) {
                return;
            }
            // Expand visual buffers to per-vertex when visuals or data changed
            if (this._pv_dirty && main_gl._nvertices > 0) {
                const vertex_counts = [main_gl._nvertices];
                (0, buffer_1.expand_to_per_vertex)(this._fill_color, this._pv_fill_color, vertex_counts, 4);
                if (this._have_hatch) {
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_patterns, this._pv_hatch_patterns, vertex_counts, 1);
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_scales, this._pv_hatch_scales, vertex_counts, 1);
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_weights, this._pv_hatch_weights, vertex_counts, 1);
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_rgba, this._pv_hatch_rgba, vertex_counts, 4);
                }
                this._pv_dirty = false;
            }
            const { width, height } = transform;
            const canvas_size = [width, height];
            // Fill pass
            if (main_gl._triangle_count > 0 && main_gl._elements != null) {
                const fill_visuals = this.glyph.visuals.fill;
                if (fill_visuals.doit) {
                    if (this._have_hatch) {
                        this.regl_wrapper.polygon_hatch()({
                            scissor: this.regl_wrapper.scissor,
                            viewport: this.regl_wrapper.viewport,
                            canvas_size,
                            positions: main_gl._positions,
                            fill_color: this._pv_fill_color,
                            edge_distance: main_gl._edge_distance,
                            elements: main_gl._elements,
                            count: main_gl._triangle_count * 3,
                            offset: 0,
                            antialias: polygon_1.POLYGON_AA_WIDTH / transform.pixel_ratio,
                            hatch_pattern: this._pv_hatch_patterns,
                            hatch_scale: this._pv_hatch_scales,
                            hatch_weight: this._pv_hatch_weights,
                            hatch_color: this._pv_hatch_rgba,
                        });
                    }
                    else {
                        this.regl_wrapper.polygon()({
                            scissor: this.regl_wrapper.scissor,
                            viewport: this.regl_wrapper.viewport,
                            canvas_size,
                            positions: main_gl._positions,
                            fill_color: this._pv_fill_color,
                            edge_distance: main_gl._edge_distance,
                            elements: main_gl._elements,
                            count: main_gl._triangle_count * 3,
                            offset: 0,
                            antialias: polygon_1.POLYGON_AA_WIDTH / transform.pixel_ratio,
                        });
                    }
                }
            }
            // Stroke pass - draw each ring outline separately
            if (main_gl._ring_data.length > 0) {
                const line_visuals = this.glyph.visuals.line;
                if (line_visuals.doit) {
                    for (const ring of main_gl._ring_data) {
                        if (ring.nline < 2) {
                            continue;
                        }
                        const nsegments = ring.nline - 1;
                        const linewidth = this._linewidth.get_array()[0];
                        const scissor = this.regl_wrapper.scissor_for_points(ring.points, (0, base_line_1.line_bounds_padding)(linewidth), transform.pixel_ratio);
                        const [framebuffer, tex] = this.regl_wrapper.framebuffer_and_texture;
                        this.regl_wrapper.clear_framebuffer(framebuffer);
                        // Upload ring data
                        if (this._line_points_buf == null) {
                            this._line_points_buf = new buffer_1.Float32Buffer(this.regl_wrapper);
                        }
                        const pts = this._line_points_buf.get_sized_array(ring.points.length);
                        pts.set(ring.points);
                        this._line_points_buf.update();
                        if (this._line_show_buf == null) {
                            this._line_show_buf = new buffer_1.Uint8Buffer(this.regl_wrapper);
                        }
                        const shw = this._line_show_buf.get_sized_array(ring.show.length);
                        shw.set(ring.show);
                        this._line_show_buf.update();
                        if (this._is_dashed) {
                            if (this._length_so_far_buf == null) {
                                this._length_so_far_buf = new buffer_1.Float32Buffer(this.regl_wrapper);
                            }
                            const lsf = this._length_so_far_buf.get_sized_array(ring.length_so_far.length);
                            lsf.set(ring.length_so_far);
                            this._length_so_far_buf.update();
                        }
                        const solid_props = {
                            scissor,
                            viewport: this.regl_wrapper.viewport,
                            canvas_size,
                            antialias: base_line_1.LINE_AA_WIDTH / transform.pixel_ratio,
                            miter_limit: base_line_1.LINE_MITER_LIMIT,
                            points: this._line_points_buf,
                            show: this._line_show_buf,
                            nsegments,
                            linewidth: this._linewidth,
                            line_color: this._line_color,
                            line_cap: this._line_cap,
                            line_join: this._line_join,
                            framebuffer,
                            point_offset: 0,
                            line_offset: 0,
                        };
                        if (this._is_dashed && this._dash_tex[0] != null) {
                            const dashed_props = {
                                ...solid_props,
                                length_so_far: this._length_so_far_buf,
                                dash_tex: this._dash_tex[0],
                                dash_tex_info: this._dash_tex_info,
                                dash_scale: this._dash_scale,
                                dash_offset: this._dash_offset,
                            };
                            this.regl_wrapper.dashed_line()(dashed_props);
                        }
                        else {
                            this.regl_wrapper.solid_line()(solid_props);
                        }
                        const accumulate_props = {
                            scissor,
                            viewport: this.regl_wrapper.viewport,
                            framebuffer_tex: tex,
                        };
                        this.regl_wrapper.accumulate()(accumulate_props);
                    }
                }
            }
        }
        _set_data(data_changed = true) {
            const { sx, sy } = this.glyph;
            const rings = (0, polygon_1.split_rings)(sx, sy);
            const { scales } = this.glyph.renderer.coordinates;
            // Changing scale types is not an affine remapping of cached intersections.
            const scales_changed = scales.some((scale, i) => scale !== this._topology_scales?.[i]);
            this._topology_scales = scales;
            if (rings.length > 0) {
                let topology = this._topology;
                let topology_changed = data_changed || scales_changed;
                if (topology_changed || topology == null || !topology.matches(rings)) {
                    topology = (0, polygon_2.try_create_polygon_topology)(rings) ?? undefined;
                    this._topology = topology;
                    topology_changed = true;
                }
                let total_nvertices = 0;
                let total_ntriangles = 0;
                let total_coords = 0;
                let total_elements = 0;
                const group_geoms = topology?.geometries(rings) ?? [];
                for (const geom of group_geoms) {
                    total_nvertices += geom.nvertices;
                    total_ntriangles += geom.ntriangles;
                    total_coords += geom.positions.length;
                    total_elements += geom.indices.length;
                }
                this._triangle_count = total_ntriangles;
                this._nvertices = total_nvertices;
                // Merge all group geometries into single buffers
                if (this._positions == null) {
                    this._positions = new buffer_1.Float32Buffer(this.regl_wrapper, 2);
                }
                const pos_array = this._positions.get_sized_array(total_coords);
                if (this._edge_distance == null) {
                    this._edge_distance = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                const ed_array = this._edge_distance.get_sized_array(total_nvertices);
                const elem_array = topology_changed || this._elements == null ? new Uint32Array(total_elements) : null;
                let pos_offset = 0;
                let ed_offset = 0;
                let elem_offset = 0;
                let vertex_offset = 0;
                for (const geom of group_geoms) {
                    pos_array.set(geom.positions, pos_offset);
                    pos_offset += geom.positions.length;
                    ed_array.set(geom.edge_distance, ed_offset);
                    ed_offset += geom.edge_distance.length;
                    if (elem_array != null) {
                        for (let j = 0; j < geom.indices.length; j++) {
                            elem_array[elem_offset + j] = geom.indices[j] + vertex_offset;
                        }
                    }
                    elem_offset += geom.indices.length;
                    vertex_offset += geom.nvertices;
                }
                this._positions.update();
                this._edge_distance.update();
                // Element topology is data-space invariant, so retain it across mapping.
                if (elem_array != null) {
                    this._elements?.destroy();
                    this._elements = total_elements == 0 ? null : this.regl_wrapper.elements({
                        usage: "static",
                        primitive: "triangles",
                        data: elem_array,
                        type: "uint32",
                    });
                }
                // Build line data for all rings (outer boundary + holes + disjoint)
                this._ring_data = [];
                for (const ring of rings) {
                    const data = (0, polygon_1.build_line_from_ring)(ring);
                    if (data.nline > 0) {
                        this._ring_data.push(data);
                    }
                }
            }
            else {
                if (data_changed || scales_changed) {
                    this._elements?.destroy();
                    this._elements = null;
                    this._topology = undefined;
                }
                this._triangle_count = 0;
                this._nvertices = 0;
                this._ring_data = [];
            }
        }
        _set_visuals() {
            const fill_visuals = this.glyph.visuals.fill;
            this._fill_color.set_from_color(fill_visuals.fill_color, fill_visuals.fill_alpha);
            const line_visuals = this.glyph.visuals.line;
            this._line_color.set_from_color(line_visuals.line_color, line_visuals.line_alpha);
            this._linewidth.set_from_prop(line_visuals.line_width);
            this._line_cap.set_from_line_cap(line_visuals.line_cap);
            this._line_join.set_from_line_join(line_visuals.line_join);
            // Dash detection
            const { line_dash } = line_visuals;
            const arr = (0, dash_cache_1.normalize_dash_pattern)((0, line_1.resolve_line_dash)(line_dash.get(0)));
            this._is_dashed = arr.length != 0;
            this._dash_tex = [];
            if (this._is_dashed) {
                if (this._dash_offset == null) {
                    this._dash_offset = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                this._dash_offset.set_from_prop(line_visuals.line_dash_offset);
                if (this._dash_tex_info == null) {
                    this._dash_tex_info = new buffer_1.Float32Buffer(this.regl_wrapper, 4);
                }
                const dash_tex_info = this._dash_tex_info.get_sized_array(4);
                if (this._dash_scale == null) {
                    this._dash_scale = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                const dash_scale = this._dash_scale.get_sized_array(1);
                const [tex_info, tex, scale] = this.regl_wrapper.get_dash(arr);
                this._dash_tex.push(tex);
                for (let j = 0; j < 4; j++) {
                    dash_tex_info[j] = tex_info[j];
                }
                dash_scale[0] = scale;
                // Patch is always scalar (single glyph).
                this._dash_tex_info.update(true);
                this._dash_scale.update(true);
            }
            const hatch_visuals = this.glyph.visuals.hatch;
            this._have_hatch = hatch_visuals.doit;
            if (this._have_hatch) {
                this._hatch_patterns.set_from_hatch_pattern(hatch_visuals.hatch_pattern);
                this._hatch_scales.set_from_prop(hatch_visuals.hatch_scale);
                this._hatch_weights.set_from_prop(hatch_visuals.hatch_weight);
                this._hatch_rgba.set_from_color(hatch_visuals.hatch_color, hatch_visuals.hatch_alpha);
            }
        }
    }
    exports.PatchGL = PatchGL;
},
673: /* core/util/polygon.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.split_rings = split_rings;
    exports.generate_skirt_geometry = generate_skirt_geometry;
    exports.build_line_from_ring = build_line_from_ring;
    // Shared utilities for polygon rendering (Patch, Patches glyphs).
    /** Width of the anti-aliasing skirt in CSS pixels. Must match the
     *  `antialias` uniform passed to the polygon shader so that the
     *  smoothstep fade range equals the skirt geometry extent. */
    exports.POLYGON_AA_WIDTH = 0.75;
    /** Split x/y coordinate arrays on non-finite values into rings (sub-paths).
     *  Each ring is a flat array of interleaved [x0, y0, x1, y1, ...] values. */
    function split_rings(sx, sy) {
        const n = Math.min(sx.length, sy.length);
        const rings = [];
        let current_ring = [];
        for (let i = 0; i < n; i++) {
            const x = sx[i];
            const y = sy[i];
            if (!isFinite(x + y)) {
                if (current_ring.length > 0) {
                    rings.push(current_ring);
                    current_ring = [];
                }
            }
            else {
                current_ring.push(x, y);
            }
        }
        if (current_ring.length > 0) {
            rings.push(current_ring);
        }
        return rings;
    }
    /** Compute the signed area of a ring (shoelace formula).
     *  Positive for counter-clockwise, negative for clockwise. */
    function signed_area_2(ring) {
        const n = ring.length / 2;
        let area = 0;
        for (let i = 0; i < n; i++) {
            const j = (i + 1) % n;
            area += ring[i * 2] * ring[j * 2 + 1] - ring[j * 2] * ring[i * 2 + 1];
        }
        return area;
    }
    /** Generate expanded geometry with an anti-aliasing skirt around polygon boundaries.
     *
     *  The skirt approach adds a thin fringe of extra triangles around each polygon
     *  boundary edge. Interior vertices get `edge_distance = antialias_width`
     *  (fully opaque). Skirt outer vertices get `edge_distance = 0.0` (fully
     *  transparent). The GPU linearly interpolates across the skirt, producing a
     *  smooth alpha gradient for anti-aliased polygon edges. Ordinarily the skirt
     *  straddles the mathematical boundary. Rings with subpixel segments instead
     *  keep their triangulated vertices fixed and place the entire fade outwards,
     *  because moving those vertices can invalidate skinny fill triangles.
     *
     *  @param flat_coords      Interleaved [x0,y0,...] screen-pixel coordinates.
     *  @param rings            Ring arrays as returned by {@link split_rings}.
     *  @param tri_indices      Fill triangle indices into flat_coords.
     *  @param antialias_width  Width of the AA skirt in CSS pixels.
     *  @param preserve_vertices Keep boundary vertices fixed when the tessellator
     *                           adds vertices shared by touching boundaries.
     *  @param canonical_orientation Every boundary has the filled region on its
     *                               left, regardless of whether it is an outer or hole.
     *  @returns SkirtGeometry with combined positions, edge distances, and indices.
     */
    function generate_skirt_geometry(flat_coords, rings, tri_indices, antialias_width, preserve_vertices = false, canonical_orientation = false) {
        const n_original = flat_coords.length / 2;
        const n_fill_tris = tri_indices.length / 3;
        if (n_original < 3 || n_fill_tris == 0) {
            return {
                positions: new Float32Array(flat_coords.length),
                edge_distance: new Float32Array(n_original).fill(antialias_width),
                indices: new Uint32Array(tri_indices),
                nvertices: n_original,
                ntriangles: n_fill_tris,
            };
        }
        // Count boundary vertices (= boundary edges) across all rings
        let n_boundary = 0;
        for (const ring of rings) {
            n_boundary += ring.length / 2;
        }
        const n_total_verts = n_original + n_boundary;
        const n_skirt_tris = 2 * n_boundary;
        const n_total_tris = n_fill_tris + n_skirt_tris;
        const positions = new Float32Array(n_total_verts * 2);
        const edge_distance = new Float32Array(n_total_verts);
        const indices = new Uint32Array(n_total_tris * 3);
        // 1. Copy original vertices, set edge_distance = antialias_width
        for (let i = 0; i < flat_coords.length; i++) {
            positions[i] = flat_coords[i];
        }
        edge_distance.fill(antialias_width, 0, n_original);
        // 2. Copy fill indices
        for (let i = 0; i < tri_indices.length; i++) {
            indices[i] = tri_indices[i];
        }
        // 3. Generate skirt vertices and triangles
        let skirt_vert_idx = n_original;
        let skirt_tri_idx = n_fill_tris * 3;
        let ring_offset = 0; // global vertex index offset for current ring
        for (let ring_idx = 0; ring_idx < rings.length; ring_idx++) {
            const ring = rings[ring_idx];
            const npts = ring.length / 2;
            if (npts < 2) {
                ring_offset += npts;
                continue;
            }
            // Determine normal direction based on ring role:
            // Ring 0 (outer): expand outward
            // Ring 1+ (holes): expand into the hole
            const area = signed_area_2(ring);
            // For CCW (positive area) outer ring, right-hand perpendicular points outward
            // For holes, we flip
            const normal_sign = canonical_orientation ? 1 : ring_idx == 0 ? Math.sign(area) : -Math.sign(area);
            // If area is zero (degenerate ring), skip skirt for this ring
            if (normal_sign == 0) {
                // Still create degenerate skirt vertices at the same position
                for (let i = 0; i < npts; i++) {
                    const vx = flat_coords[(ring_offset + i) * 2];
                    const vy = flat_coords[(ring_offset + i) * 2 + 1];
                    positions[skirt_vert_idx * 2] = vx;
                    positions[skirt_vert_idx * 2 + 1] = vy;
                    edge_distance[skirt_vert_idx] = 0;
                    // Still emit skirt triangles (they'll be degenerate/zero-area)
                    const a_inner = ring_offset + i;
                    const b_inner = ring_offset + (i + 1) % npts;
                    const skirt_base = skirt_vert_idx - i; // base of this ring's skirt vertices
                    const a_out = skirt_base + i;
                    const b_out = skirt_base + (i + 1) % npts;
                    indices[skirt_tri_idx++] = a_inner;
                    indices[skirt_tri_idx++] = b_inner;
                    indices[skirt_tri_idx++] = b_out;
                    indices[skirt_tri_idx++] = a_inner;
                    indices[skirt_tri_idx++] = b_out;
                    indices[skirt_tri_idx++] = a_out;
                    skirt_vert_idx++;
                }
                ring_offset += npts;
                continue;
            }
            // Compute per-edge outward normals
            const normals = new Float64Array(npts * 2);
            for (let i = 0; i < npts; i++) {
                const j = (i + 1) % npts;
                const ex = ring[j * 2] - ring[i * 2];
                const ey = ring[j * 2 + 1] - ring[i * 2 + 1];
                const len = Math.sqrt(ex * ex + ey * ey);
                if (len < 1e-10) {
                    // Zero-length edge: normal will be zero, handled below
                    normals[i * 2] = 0;
                    normals[i * 2 + 1] = 0;
                }
                else {
                    // Right-hand perpendicular: (ey, -ex) for CCW, then multiply by normal_sign
                    normals[i * 2] = normal_sign * ey / len;
                    normals[i * 2 + 1] = normal_sign * (-ex) / len;
                }
            }
            // Record the base index for this ring's skirt vertices
            const skirt_base = skirt_vert_idx;
            // Clamp the inward shift so that it doesn't collapse small or narrow
            // polygons. We use the approximate "inradius" (area / perimeter) to
            // estimate how far inward we can safely shift without inverting the
            // fill triangulation. Rings with subpixel boundary detail need a
            // stronger fallback: keep their triangulated vertices fixed and place the
            // entire AA fade outside. Applying that fallback only to subpixel rings
            // preserves centered AA on ordinary adjacent polygons, avoiding overlap
            // seams between their semi-transparent fills.
            let perimeter = 0;
            let min_edge_length = Infinity;
            for (let i = 0; i < npts; i++) {
                const j = (i + 1) % npts;
                const ex = ring[j * 2] - ring[i * 2];
                const ey = ring[j * 2 + 1] - ring[i * 2 + 1];
                const length = Math.sqrt(ex * ex + ey * ey);
                perimeter += length;
                min_edge_length = Math.min(min_edge_length, length);
            }
            const abs_area = Math.abs(area);
            const inradius = perimeter > 0 ? abs_area / perimeter : 0;
            const half_aa = Math.min(0.5 * antialias_width, 0.25 * inradius);
            const preserve_topology = preserve_vertices || min_edge_length < antialias_width;
            for (let i = 0; i < npts; i++) {
                const prev_edge = (i - 1 + npts) % npts;
                const curr_edge = i;
                const n0x = normals[prev_edge * 2];
                const n0y = normals[prev_edge * 2 + 1];
                const n1x = normals[curr_edge * 2];
                const n1y = normals[curr_edge * 2 + 1];
                const n0_zero = (n0x == 0 && n0y == 0);
                const n1_zero = (n1x == 0 && n1y == 0);
                // Compute unit miter direction (dx, dy) and inverse-cosine scale
                let dx, dy, inv_cos;
                if (n0_zero && n1_zero) {
                    dx = 0;
                    dy = 0;
                    inv_cos = 1;
                }
                else if (n0_zero) {
                    dx = n1x;
                    dy = n1y;
                    inv_cos = 1;
                }
                else if (n1_zero) {
                    dx = n0x;
                    dy = n0y;
                    inv_cos = 1;
                }
                else {
                    let bx = n0x + n1x;
                    let by = n0y + n1y;
                    const blen = Math.sqrt(bx * bx + by * by);
                    if (blen < 1e-10) {
                        // Normals point in opposite directions (180° turn)
                        dx = n0x;
                        dy = n0y;
                        inv_cos = 1;
                    }
                    else {
                        bx /= blen;
                        by /= blen;
                        const cos_half = bx * n0x + by * n0y;
                        const clamped_cos = Math.max(cos_half, 0.1);
                        inv_cos = 1.0 / clamped_cos;
                        dx = bx;
                        dy = by;
                    }
                }
                const inner_offset = (preserve_topology ? 0 : half_aa) * inv_cos;
                const outer_offset = (preserve_topology ? antialias_width : half_aa) * inv_cos;
                const vx = flat_coords[(ring_offset + i) * 2];
                const vy = flat_coords[(ring_offset + i) * 2 + 1];
                positions[(ring_offset + i) * 2] = vx - dx * inner_offset;
                positions[(ring_offset + i) * 2 + 1] = vy - dy * inner_offset;
                positions[skirt_vert_idx * 2] = vx + dx * outer_offset;
                positions[skirt_vert_idx * 2 + 1] = vy + dy * outer_offset;
                edge_distance[skirt_vert_idx] = 0;
                skirt_vert_idx++;
            }
            // Emit skirt triangles for each boundary edge
            for (let i = 0; i < npts; i++) {
                const j = (i + 1) % npts;
                const a_inner = ring_offset + i;
                const b_inner = ring_offset + j;
                const a_outer = skirt_base + i;
                const b_outer = skirt_base + j;
                // Two triangles per edge: (A_inner, B_inner, B_outer) and (A_inner, B_outer, A_outer)
                indices[skirt_tri_idx++] = a_inner;
                indices[skirt_tri_idx++] = b_inner;
                indices[skirt_tri_idx++] = b_outer;
                indices[skirt_tri_idx++] = a_inner;
                indices[skirt_tri_idx++] = b_outer;
                indices[skirt_tri_idx++] = a_outer;
            }
            ring_offset += npts;
        }
        return {
            positions,
            edge_distance,
            indices,
            nvertices: n_total_verts,
            ntriangles: n_total_tris,
        };
    }
    /** Build line rendering data from a flat ring [x0,y0,x1,y1,...].
     *  Produces points with guard vertices, show flags, and
     *  cumulative segment lengths (always computed so that any glyph view
     *  e.g. selection or hover can render dashed if needed). */
    function build_line_from_ring(ring) {
        const npoints = ring.length / 2;
        if (npoints < 2) {
            return {
                points: new Float32Array(0),
                show: new Uint8Array(0),
                nline: 0,
                length_so_far: new Float32Array(0),
            };
        }
        const is_closed = (npoints > 2 &&
            ring[0] == ring[(npoints - 1) * 2] &&
            ring[1] == ring[(npoints - 1) * 2 + 1]);
        // For implicitly closed polygons, add a closing point to draw the final edge
        const nline = is_closed ? npoints : npoints + 1;
        const points = new Float32Array((nline + 2) * 2);
        for (let i = 0; i < npoints; i++) {
            points[(i + 1) * 2] = ring[i * 2];
            points[(i + 1) * 2 + 1] = ring[i * 2 + 1];
        }
        if (!is_closed) {
            // Add closing point (repeat first vertex)
            points[(npoints + 1) * 2] = ring[0];
            points[(npoints + 1) * 2 + 1] = ring[1];
        }
        // Guard points for proper line joins at the closing vertex
        if (is_closed) {
            points[0] = points[(npoints - 1) * 2];
            points[1] = points[(npoints - 1) * 2 + 1];
            points[(nline + 1) * 2] = points[4];
            points[(nline + 1) * 2 + 1] = points[5];
        }
        else {
            // guard0 = last unique point (before closing vertex)
            points[0] = points[npoints * 2];
            points[1] = points[npoints * 2 + 1];
            // guard_end = second point (after closing vertex)
            points[(nline + 1) * 2] = points[4];
            points[(nline + 1) * 2 + 1] = points[5];
        }
        const show = new Uint8Array(nline + 1);
        show.fill(1);
        // Always compute length_so_far so that any glyph view (selection, hover)
        // can render dashed lines even if the main glyph is solid.
        const nsegments = nline - 1;
        const length_so_far = new Float32Array(nsegments);
        let length = 0.0;
        for (let i = 0; i < nsegments; i++) {
            length_so_far[i] = length;
            if (show[i + 1] == 1) {
                length += Math.sqrt((points[2 * i + 4] - points[2 * i + 2]) ** 2 +
                    (points[2 * i + 5] - points[2 * i + 3]) ** 2);
            }
            else {
                length = 0.0;
            }
        }
        return { points, show, nline, length_so_far };
    }
},
674: /* models/glyphs/webgl/polygon.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.coordinates = coordinates;
    exports.subdivide_contour = subdivide_contour;
    exports.simple_ring_indices = simple_ring_indices;
    exports.is_affine_remap = is_affine_remap;
    exports.try_create_polygon_topology = try_create_polygon_topology;
    const tslib_1 = require(1) /* tslib */;
    const tessellator_1 = require(675) /* ./tessellator */;
    const earcut_1 = tslib_1.__importDefault(require(677) /* earcut */);
    const polygon_1 = require(673) /* ../../../core/util/polygon */;
    const logging_1 = require(11) /* ../../../core/logging */;
    function coordinates(indices, coords) {
        const ring = new Array(2 * indices.length);
        for (let i = 0; i < indices.length; i++) {
            ring[2 * i] = coords[2 * indices[i]];
            ring[2 * i + 1] = coords[2 * indices[i] + 1];
        }
        return ring;
    }
    function* subdivide_contour(indices) {
        // Long initial faces cause quadratic relabeling in the tessellator. Split
        // them into short arcs and a contour through the arc endpoints. Every added
        // chord occurs twice in opposite directions, preserving the original winding.
        const max_vertices = 128;
        while (indices.length > max_vertices) {
            const backbone = [indices[0]];
            for (let start = 0; start < indices.length - 1; start += max_vertices - 1) {
                const end = Math.min(start + max_vertices - 1, indices.length - 1);
                const arc = indices.slice(start, end + 1);
                if (arc.length >= 3) {
                    yield arc;
                }
                backbone.push(indices[end]);
            }
            indices = backbone;
        }
        yield indices;
    }
    function orientation(a, b, c, ring) {
        const abx = ring[2 * b] - ring[2 * a];
        const aby = ring[2 * b + 1] - ring[2 * a + 1];
        const acx = ring[2 * c] - ring[2 * a];
        const acy = ring[2 * c + 1] - ring[2 * a + 1];
        const cross = abx * acy - aby * acx;
        const error = 8 * Number.EPSILON * (Math.abs(abx * acy) + Math.abs(aby * acx));
        return Math.abs(cross) <= error ? 0 : Math.sign(cross);
    }
    function on_segment(a, b, p, ring) {
        const x = ring[2 * p], y = ring[2 * p + 1];
        return x >= Math.min(ring[2 * a], ring[2 * b]) && x <= Math.max(ring[2 * a], ring[2 * b]) &&
            y >= Math.min(ring[2 * a + 1], ring[2 * b + 1]) && y <= Math.max(ring[2 * a + 1], ring[2 * b + 1]);
    }
    function segments_intersect(a, b, c, d, ring) {
        const abc = orientation(a, b, c, ring);
        const abd = orientation(a, b, d, ring);
        const cda = orientation(c, d, a, ring);
        const cdb = orientation(c, d, b, ring);
        if (abc * abd < 0 && cda * cdb < 0) {
            return true;
        }
        return abc == 0 && on_segment(a, b, c, ring) || abd == 0 && on_segment(a, b, d, ring) ||
            cda == 0 && on_segment(c, d, a, ring) || cdb == 0 && on_segment(c, d, b, ring);
    }
    /** Return source indices when a small ring is simple enough to triangulate directly. */
    function simple_ring_indices(ring) {
        const max_vertices = 4096;
        const indices = [];
        for (let i = 0; i < ring.length / 2; i++) {
            const previous = indices.at(-1);
            if (previous == null || ring[2 * i] != ring[2 * previous] || ring[2 * i + 1] != ring[2 * previous + 1]) {
                indices.push(i);
            }
        }
        if (indices.length > 1) {
            const first = indices[0], last = indices.at(-1);
            if (ring[2 * first] == ring[2 * last] && ring[2 * first + 1] == ring[2 * last + 1]) {
                indices.pop();
            }
        }
        if (indices.length < 3 || indices.length > max_vertices) {
            return null;
        }
        let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
        for (const index of indices) {
            const x = ring[2 * index], y = ring[2 * index + 1];
            if (!isFinite(x + y) || Math.abs(x) > 1e150 || Math.abs(y) > 1e150) {
                return null;
            }
            x0 = Math.min(x0, x);
            y0 = Math.min(y0, y);
            x1 = Math.max(x1, x);
            y1 = Math.max(y1, y);
        }
        if (x0 == x1 || y0 == y1) {
            return null;
        }
        for (let i = 0; i < indices.length; i++) {
            const previous = indices[(i + indices.length - 1) % indices.length];
            const current = indices[i];
            const next = indices[(i + 1) % indices.length];
            if (orientation(previous, current, next, ring) == 0) {
                const ax = ring[2 * previous] - ring[2 * current];
                const ay = ring[2 * previous + 1] - ring[2 * current + 1];
                const bx = ring[2 * next] - ring[2 * current];
                const by = ring[2 * next + 1] - ring[2 * current + 1];
                if (ax * bx + ay * by > 0) {
                    return null;
                }
            }
        }
        // A conservative uniform grid avoids comparing every pair of edges. Every
        // segment is entered into each cell touched by its bounding box, so crossing
        // segments are always tested together; false positives only select the
        // robust tessellation path.
        const grid_size = Math.ceil(Math.sqrt(indices.length));
        const cells = Array.from({ length: grid_size * grid_size }, () => new Array());
        const checked = new Int32Array(indices.length);
        const cell_index = (value, low, high) => Math.min(grid_size - 1, Math.floor(grid_size * (value - low) / (high - low)));
        for (let i = 0; i < indices.length; i++) {
            const i1 = (i + 1) % indices.length;
            const a = indices[i], b = indices[i1];
            const ix0 = cell_index(Math.min(ring[2 * a], ring[2 * b]), x0, x1);
            const ix1 = cell_index(Math.max(ring[2 * a], ring[2 * b]), x0, x1);
            const iy0 = cell_index(Math.min(ring[2 * a + 1], ring[2 * b + 1]), y0, y1);
            const iy1 = cell_index(Math.max(ring[2 * a + 1], ring[2 * b + 1]), y0, y1);
            for (let iy = iy0; iy <= iy1; iy++) {
                for (let ix = ix0; ix <= ix1; ix++) {
                    const cell = cells[iy * grid_size + ix];
                    for (const j of cell) {
                        if (checked[j] == i + 1) {
                            continue;
                        }
                        checked[j] = i + 1;
                        const j1 = (j + 1) % indices.length;
                        if (j1 != i && i1 != j && segments_intersect(a, b, indices[j], indices[j1], ring)) {
                            return null;
                        }
                    }
                    cell.push(i);
                }
            }
        }
        return indices;
    }
    function is_affine_remap(source, mapped) {
        if (source.length != mapped.length) {
            return false;
        }
        for (const offset of [0, 1]) {
            if (source.length <= offset) {
                continue;
            }
            const first = offset;
            let second = offset + 2;
            while (second < source.length && source[second] == source[first]) {
                second += 2;
            }
            if (second >= source.length) {
                for (let i = offset + 2; i < mapped.length; i += 2) {
                    if (mapped[i] != mapped[first]) {
                        return false;
                    }
                }
                continue;
            }
            const scale = (mapped[second] - mapped[first]) / (source[second] - source[first]);
            const shift = mapped[first] - scale * source[first];
            for (let i = offset; i < source.length; i += 2) {
                const expected = scale * source[i] + shift;
                // Screen coordinates are stored as float32, so an affine remap can pick
                // up rounding at both the source and destination mapping stages.
                const tolerance = 1e-6 * Math.max(1, Math.abs(expected), Math.abs(mapped[i]));
                if (Math.abs(expected - mapped[i]) > tolerance) {
                    return false;
                }
            }
        }
        return true;
    }
    /** Resolve an even-odd polygon into simple boundaries and cache its triangulation.
     *  Source vertex indices and intersection weights allow the same topology to be
     *  reused under affine screen mappings, including reversed axes. */
    class PolygonTopology {
        _ring_lengths;
        _source_coords;
        _combined = [];
        _groups;
        constructor(rings) {
            this._ring_lengths = rings.map((ring) => ring.length);
            const coords = rings.flat();
            this._source_coords = coords.slice();
            const { gluEnum, windingRule } = tessellator_1.libtess;
            const combine = ([x, y], data, weights) => {
                const sources = [];
                const source_weights = [];
                for (let i = 0; i < data.length; i++) {
                    const source = data[i];
                    if (source != null && weights[i] != 0) {
                        sources.push(source);
                        source_weights.push(weights[i]);
                    }
                }
                // A source can itself be an intersection generated earlier in the sweep.
                // Keep this dependency graph instead of recursively expanding its weights.
                this._combined.push({ sources, weights: source_weights });
                const index = coords.length / 2;
                coords.push(x, y);
                return index;
            };
            const tesselator = () => {
                const tess = new tessellator_1.libtess.GluTesselator();
                // A fixed normal handles rings whose signed area cancels, such as a
                // symmetric bow-tie, and gives resolved boundaries a known orientation.
                tess.gluTessNormal(0, 0, 1);
                tess.gluTessProperty(gluEnum.GLU_TESS_WINDING_RULE, windingRule.GLU_TESS_WINDING_ODD);
                tess.gluTessCallback(gluEnum.GLU_TESS_COMBINE, combine);
                tess.gluTessCallback(gluEnum.GLU_TESS_ERROR, (code) => {
                    throw new Error(`Polygon tessellation failed (${code})`);
                });
                return tess;
            };
            // Most Patches datasets contain many modest, non-self-intersecting rings.
            // Checking those rings directly avoids the boundary-resolution sweep while
            // retaining the robust path for crossings, overlaps, and large contours.
            if (rings.length == 1) {
                const indices = simple_ring_indices(rings[0]);
                if (indices != null) {
                    const tri_indices = (0, earcut_1.default)(coordinates(indices, coords));
                    this._groups = [{
                            rings: [indices], vertices: indices, tri_indices, canonical_orientation: false, preserve_vertices: false,
                        }];
                    return;
                }
            }
            const tess = tesselator();
            const groups = [];
            // The mesh callback runs after libtess has triangulated the interior and
            // discarded exterior faces. Read both products from that single mesh so
            // complex polygons don't need a second tessellation pass for their fill.
            tess.gluTessCallback(gluEnum.GLU_TESS_MESH, (mesh) => {
                const boundaries = [];
                const visited = new Set();
                for (let face = mesh.fHead.next; face !== mesh.fHead; face = face.next) {
                    let edge = face.anEdge;
                    do {
                        if (edge.sym.lFace == null && !visited.has(edge)) {
                            const start = edge;
                            const boundary = [];
                            let current = start;
                            do {
                                visited.add(current);
                                boundary.push(current.org.data);
                                // Cross adjacent interior triangles around the destination until
                                // the next edge with the filled region on its left is reached.
                                current = current.lNext;
                                while (current.sym.lFace != null) {
                                    current = current.sym.lNext;
                                }
                            } while (current !== start);
                            boundaries.push(boundary);
                        }
                        edge = edge.lNext;
                    } while (edge !== face.anEdge);
                }
                const vertices = boundaries.flat();
                const preserve_vertices = new Set(vertices).size < vertices.length;
                const vertex_indices = new Map(vertices.map((index, i) => [index, i]));
                const local_index = (index) => {
                    let local = vertex_indices.get(index);
                    if (local == null) {
                        local = vertices.length;
                        vertices.push(index);
                        vertex_indices.set(index, local);
                    }
                    return local;
                };
                const tri_indices = [];
                for (let face = mesh.fHead.next; face !== mesh.fHead; face = face.next) {
                    let edge = face.anEdge;
                    do {
                        tri_indices.push(local_index(edge.org.data));
                        edge = edge.lNext;
                    } while (edge !== face.anEdge);
                }
                if (tri_indices.length != 0) {
                    groups.push({ rings: boundaries, vertices, tri_indices, canonical_orientation: true, preserve_vertices });
                }
            });
            tess.gluTessBeginPolygon();
            let offset = 0;
            for (const ring of rings) {
                if (ring.length >= 6) {
                    const indices = Array.from({ length: ring.length / 2 }, (_, i) => offset + i);
                    for (const contour of subdivide_contour(indices)) {
                        tess.gluTessBeginContour();
                        for (const index of contour) {
                            tess.gluTessVertex([coords[2 * index], coords[2 * index + 1], 0], index);
                        }
                        tess.gluTessEndContour();
                    }
                }
                offset += ring.length / 2;
            }
            tess.gluTessEndPolygon();
            this._groups = groups;
        }
        // Check mapped ring structure; callers invalidate separately on data changes.
        matches(rings) {
            return rings.length == this._ring_lengths.length &&
                rings.every((ring, i) => ring.length == this._ring_lengths[i]) &&
                is_affine_remap(this._source_coords, rings.flat());
        }
        geometries(rings, antialias_width = polygon_1.POLYGON_AA_WIDTH) {
            const coords = rings.flat();
            for (const { sources, weights } of this._combined) {
                let x = 0;
                let y = 0;
                for (let i = 0; i < sources.length; i++) {
                    const source = sources[i];
                    x += weights[i] * coords[2 * source];
                    y += weights[i] * coords[2 * source + 1];
                }
                coords.push(x, y);
            }
            return this._groups.map(({ rings: boundaries, vertices, tri_indices, canonical_orientation, preserve_vertices }) => {
                const group_rings = boundaries.map((indices) => coordinates(indices, coords));
                const flat_coords = boundaries.length == 1 && vertices === boundaries[0] ?
                    group_rings[0] : coordinates(vertices, coords);
                const boundary_vertices = boundaries.reduce((count, ring) => count + ring.length, 0);
                // Shared boundary occurrences and fill-only mesh vertices must keep their
                // triangulated positions when the AA fringe is added.
                preserve_vertices ||= vertices.length > boundary_vertices;
                return (0, polygon_1.generate_skirt_geometry)(flat_coords, group_rings, tri_indices, antialias_width, preserve_vertices, canonical_orientation);
            });
        }
    }
    exports.PolygonTopology = PolygonTopology;
    let warned_tessellation_error = false;
    /** Construct polygon topology without allowing invalid geometry to abort a plot render. */
    function try_create_polygon_topology(rings) {
        try {
            return new PolygonTopology(rings);
        }
        catch (error) {
            if (!warned_tessellation_error) {
                warned_tessellation_error = true;
                logging_1.logger.warn("unable to tessellate a WebGL polygon fill; rendering its outline only", error);
            }
            return null;
        }
    }
},
675: /* models/glyphs/webgl/tessellator.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.smaller_loop = smaller_loop;
    exports.with_upstream_mesh_operations = with_upstream_mesh_operations;
    const tslib_1 = require(1) /* tslib */;
    /*!
     * Adapted from libtess.js: Copyright 2000, Silicon Graphics, Inc.
     * Copyright 2015, Google Inc. All Rights Reserved.
     * Distributed under the SGI Free Software License B, version 2.0:
     * http://oss.sgi.com/projects/FreeB/
     */
    const libtess_cat_js_1 = tslib_1.__importDefault(require(676) /* libtess/libtess.cat.js */);
    exports.libtess = libtess_cat_js_1.default;
    // Adapt libtess 1.2.2's mesh operations to relabel the smaller face loop when
    // splitting or joining faces. The upstream choice can repeatedly walk a large
    // face for small local changes. These operations preserve the edge topology,
    // vertex identities and inside flags; only the surviving face identity differs.
    // Use the unminified entry point for stable internal names and pin the version.
    // Derived from the mesh operations in libtess's libtess.cat.js distribution.
    // The 1.2.2 sweep, monotone tessellation, and rendering call sites re-read
    // half-edge face references after these operations. removeDegenerateFaces_ is
    // the exception: it caches the next face, so the adapter preserves deletion
    // identity for its one- and two-edge faces below.
    const { mesh } = libtess_cat_js_1.default;
    const upstream_mesh_operations = {
        connect: mesh.connect,
        meshSplice: mesh.meshSplice,
        killFace_: mesh.killFace_,
    };
    function smaller_loop(a, b) {
        let ea = a.lNext;
        let eb = b.lNext;
        while (ea !== a && eb !== b) {
            ea = ea.lNext;
            eb = eb.lNext;
        }
        return ea === a ? a : b;
    }
    function split_face(a, b, face) {
        const edge = smaller_loop(a, b);
        face.anEdge = edge === a ? b : a;
        mesh.makeFace_(edge, face);
    }
    const adapted_mesh_operations = {
        connect: (eOrg, eDst) => {
            const joining_loops = eDst.lFace !== eOrg.lFace;
            const eNew = mesh.makeEdgePair_(eOrg);
            const eNewSym = eNew.sym;
            if (joining_loops) {
                mesh.killFace_(eDst.lFace, eOrg.lFace);
            }
            mesh.splice_(eNew, eOrg.lNext);
            mesh.splice_(eNewSym, eDst);
            eNew.org = eOrg.dst();
            eNewSym.org = eDst.org;
            const face = eOrg.lFace;
            eNew.lFace = eNewSym.lFace = face;
            face.anEdge = eNewSym;
            if (!joining_loops) {
                split_face(eNew, eNewSym, face);
            }
            return eNew;
        },
        meshSplice: (eOrg, eDst) => {
            if (eOrg === eDst) {
                return;
            }
            const joining_vertices = eDst.org !== eOrg.org;
            const joining_loops = eDst.lFace !== eOrg.lFace;
            if (joining_vertices) {
                mesh.killVertex_(eDst.org, eOrg.org);
            }
            if (joining_loops) {
                mesh.killFace_(eDst.lFace, eOrg.lFace);
            }
            mesh.splice_(eDst, eOrg);
            if (!joining_vertices) {
                mesh.makeVertex_(eDst, eOrg.org);
                eOrg.org.anEdge = eOrg;
            }
            if (!joining_loops) {
                split_face(eDst, eOrg, eOrg.lFace);
            }
        },
        killFace_: (face, replacement) => {
            // removeDegenerateFaces_ caches face.next before deleting a one- or two-edge
            // face. Preserve the requested deletion in that case so the cached face is
            // never the replacement object that this operation unlinks.
            const degenerate = face.anEdge.lNext.lNext === face.anEdge;
            if (!degenerate && replacement != null && smaller_loop(face.anEdge, replacement.anEdge) === replacement.anEdge) {
                // Retain the target face's classification even when its object is replaced.
                face.inside = replacement.inside;
                const previous = face;
                face = replacement;
                replacement = previous;
            }
            const start = face.anEdge;
            let edge = start;
            do {
                // Null is used only when removing a face entirely, outside the sweep.
                edge.lFace = replacement;
                edge = edge.lNext;
            } while (edge !== start);
            face.next.prev = face.prev;
            face.prev.next = face.next;
        },
    };
    Object.assign(mesh, adapted_mesh_operations);
    /** Run a synchronous check against libtess's original mesh operations. */
    function with_upstream_mesh_operations(fn) {
        const current = {
            connect: mesh.connect,
            meshSplice: mesh.meshSplice,
            killFace_: mesh.killFace_,
        };
        Object.assign(mesh, upstream_mesh_operations);
        try {
            return fn();
        }
        finally {
            Object.assign(mesh, current);
        }
    }
},
676: /* libtess/libtess.cat.js */ function _(require, module, exports, __esModule, __esExport) {
    /**
     * @license
     * Copyright 2000, Silicon Graphics, Inc. All Rights Reserved.
     * Copyright 2015, Google Inc. All Rights Reserved.
     *
     * Permission is hereby granted, free of charge, to any person obtaining a copy
     * of this software and associated documentation files (the "Software"), to
     * deal in the Software without restriction, including without limitation the
     * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
     * sell copies of the Software, and to permit persons to whom the Software is
     * furnished to do so, subject to the following conditions:
     *
     * The above copyright notice including the dates of first publication and
     * either this permission notice or a reference to http://oss.sgi.com/projects/FreeB/
     * shall be included in all copies or substantial portions of the Software.
     *
     * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
     * SILICON GRAPHICS, INC. BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
     * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
     * IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
     *
     * Original Code. The Original Code is: OpenGL Sample Implementation,
     * Version 1.2.1, released January 26, 2000, developed by Silicon Graphics,
     * Inc. The Original Code is Copyright (c) 1991-2000 Silicon Graphics, Inc.
     * Copyright in any portions created by third parties is as indicated
     * elsewhere herein. All Rights Reserved.
     */
    /**
     * @author ericv@cs.stanford.edu (Eric Veach)
     * @author bckenny@google.com (Brendan Kenny)
     */
    /**
     * Base namespace.
     * @const
     */
    var libtess = {};
    /**
     * Whether to run asserts and extra debug checks.
     * @define {boolean}
     */
    libtess.DEBUG = false;
    /**
     * Checks if the condition evaluates to true if libtess.DEBUG is true.
     * @param {*} condition The condition to check.
     * @param {string=} opt_message Error message in case of failure.
     * @throws {Error} Assertion failed, the condition evaluates to false.
     */
    libtess.assert = function (condition, opt_message) {
        if (libtess.DEBUG && !condition) {
            throw new Error('Assertion failed' +
                (opt_message ? ': ' + opt_message : ''));
        }
    };
    /**
     * The maximum vertex coordinate size, 1e150. Anything larger will trigger a
     * GLU_TESS_COORD_TOO_LARGE error callback and the vertex will be clamped to
     * this value for all tessellation calculations.
     * @const {number}
     */
    libtess.GLU_TESS_MAX_COORD = 1e150;
    // NOTE(bckenny): value from glu.pl generator
    /**
     * Normally the polygon is projected to a plane perpendicular to one of the
     * three coordinate axes before tessellating in 2d. This helps numerical
     * accuracy by forgoing a transformation step by simply dropping one coordinate
     * dimension.
     *
     * However, this can affect the placement of intersection points for non-axis-
     * aligned polygons. Setting TRUE_PROJECT to true will instead project onto a
     * plane actually perpendicular to the polygon's normal.
     *
     * NOTE(bckenny): I can find no instances on the internet in which this mode has
     * been used, but it's difficult to search for. This was a compile-time setting
     * in the original, so setting this as constant. If this is exposed in the
     * public API, remove the ignore coverage directives on
     * libtess.normal.projectPolygon and libtess.normal.normalize_.
     * @const {boolean}
     */
    libtess.TRUE_PROJECT = false;
    /**
     * The default tolerance for merging features, 0, meaning vertices are only
     * merged if they are exactly coincident
     * If a higher tolerance is needed, significant rewriting will need to occur.
     * See libtess.sweep.TOLERANCE_NONZERO_ as a starting place.
     * @const {number}
     */
    libtess.GLU_TESS_DEFAULT_TOLERANCE = 0;
    /**
     * The input contours parition the plane into regions. A winding
     * rule determines which of these regions are inside the polygon.
     *
     * For a single contour C, the winding number of a point x is simply
     * the signed number of revolutions we make around x as we travel
     * once around C (where CCW is positive). When there are several
     * contours, the individual winding numbers are summed. This
     * procedure associates a signed integer value with each point x in
     * the plane. Note that the winding number is the same for all
     * points in a single region.
     *
     * The winding rule classifies a region as "inside" if its winding
     * number belongs to the chosen category (odd, nonzero, positive,
     * negative, or absolute value of at least two). The current GLU
     * tesselator implements the "odd" rule. The "nonzero" rule is another
     * common way to define the interior. The other three rules are
     * useful for polygon CSG operations.
     * @enum {number}
     */
    libtess.windingRule = {
        // NOTE(bckenny): values from enumglu.spec
        GLU_TESS_WINDING_ODD: 100130,
        GLU_TESS_WINDING_NONZERO: 100131,
        GLU_TESS_WINDING_POSITIVE: 100132,
        GLU_TESS_WINDING_NEGATIVE: 100133,
        GLU_TESS_WINDING_ABS_GEQ_TWO: 100134
    };
    /**
     * The type of primitive return from a "begin" callback. GL_LINE_LOOP is only
     * returned when GLU_TESS_BOUNDARY_ONLY is true. GL_TRIANGLE_STRIP and
     * GL_TRIANGLE_FAN are no longer returned since 1.1.0 (see release notes).
     * @enum {number}
     */
    libtess.primitiveType = {
        GL_LINE_LOOP: 2,
        GL_TRIANGLES: 4,
        GL_TRIANGLE_STRIP: 5,
        GL_TRIANGLE_FAN: 6
    };
    /**
     * The types of errors provided in the error callback.
     * @enum {number}
     */
    libtess.errorType = {
        // TODO(bckenny) doc types
        // NOTE(bckenny): values from enumglu.spec
        GLU_TESS_MISSING_BEGIN_POLYGON: 100151,
        GLU_TESS_MISSING_END_POLYGON: 100153,
        GLU_TESS_MISSING_BEGIN_CONTOUR: 100152,
        GLU_TESS_MISSING_END_CONTOUR: 100154,
        GLU_TESS_COORD_TOO_LARGE: 100155,
        GLU_TESS_NEED_COMBINE_CALLBACK: 100156
    };
    /**
     * Enum values necessary for providing settings and callbacks. See the readme
     * for details.
     * @enum {number}
     */
    libtess.gluEnum = {
        // TODO(bckenny): rename so not always typing libtess.gluEnum.*?
        // NOTE(bckenny): values from enumglu.spec
        GLU_TESS_BEGIN: 100100,
        GLU_TESS_VERTEX: 100101,
        GLU_TESS_END: 100102,
        GLU_TESS_ERROR: 100103,
        GLU_TESS_EDGE_FLAG: 100104,
        GLU_TESS_COMBINE: 100105,
        GLU_TESS_BEGIN_DATA: 100106,
        GLU_TESS_VERTEX_DATA: 100107,
        GLU_TESS_END_DATA: 100108,
        GLU_TESS_ERROR_DATA: 100109,
        GLU_TESS_EDGE_FLAG_DATA: 100110,
        GLU_TESS_COMBINE_DATA: 100111,
        GLU_TESS_MESH: 100112, //  NOTE(bckenny): from tess.c
        GLU_TESS_TOLERANCE: 100142,
        GLU_TESS_WINDING_RULE: 100140,
        GLU_TESS_BOUNDARY_ONLY: 100141,
        // TODO(bckenny): move this to libtess.errorType?
        GLU_INVALID_ENUM: 100900,
        GLU_INVALID_VALUE: 100901
    };
    /** @typedef {number} */
    libtess.PQHandle;
    /* global libtess */
    /** @const */
    libtess.geom = {};
    /**
     * Returns whether vertex u and vertex v are equal.
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @return {boolean}
     */
    libtess.geom.vertEq = function (u, v) {
        return u.s === v.s && u.t === v.t;
    };
    /**
     * Returns whether vertex u is lexicographically less than or equal to vertex v.
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @return {boolean}
     */
    libtess.geom.vertLeq = function (u, v) {
        return (u.s < v.s) || (u.s === v.s && u.t <= v.t);
    };
    /**
     * Given three vertices u,v,w such that geom.vertLeq(u,v) && geom.vertLeq(v,w),
     * evaluates the t-coord of the edge uw at the s-coord of the vertex v.
     * Returns v.t - (uw)(v.s), ie. the signed distance from uw to v.
     * If uw is vertical (and thus passes thru v), the result is zero.
     *
     * The calculation is extremely accurate and stable, even when v
     * is very close to u or w.  In particular if we set v.t = 0 and
     * let r be the negated result (this evaluates (uw)(v.s)), then
     * r is guaranteed to satisfy MIN(u.t,w.t) <= r <= MAX(u.t,w.t).
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @param {libtess.GluVertex} w
     * @return {number}
     */
    libtess.geom.edgeEval = function (u, v, w) {
        var gapL = v.s - u.s;
        var gapR = w.s - v.s;
        if (gapL + gapR > 0) {
            if (gapL < gapR) {
                return (v.t - u.t) + (u.t - w.t) * (gapL / (gapL + gapR));
            }
            else {
                return (v.t - w.t) + (w.t - u.t) * (gapR / (gapL + gapR));
            }
        }
        // vertical line
        return 0;
    };
    /**
     * Returns a number whose sign matches geom.edgeEval(u,v,w) but which
     * is cheaper to evaluate.  Returns > 0, == 0 , or < 0
     * as v is above, on, or below the edge uw.
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @param {libtess.GluVertex} w
     * @return {number}
     */
    libtess.geom.edgeSign = function (u, v, w) {
        var gapL = v.s - u.s;
        var gapR = w.s - v.s;
        if (gapL + gapR > 0) {
            return (v.t - w.t) * gapL + (v.t - u.t) * gapR;
        }
        // vertical line
        return 0;
    };
    /**
     * Version of VertLeq with s and t transposed.
     * Returns whether vertex u is lexicographically less than or equal to vertex v.
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @return {boolean}
     */
    libtess.geom.transLeq = function (u, v) {
        return (u.t < v.t) || (u.t === v.t && u.s <= v.s);
    };
    /**
     * Version of geom.edgeEval with s and t transposed.
     * Given three vertices u,v,w such that geom.transLeq(u,v) &&
     * geom.transLeq(v,w), evaluates the t-coord of the edge uw at the s-coord of
     * the vertex v. Returns v.s - (uw)(v.t), ie. the signed distance from uw to v.
     * If uw is vertical (and thus passes thru v), the result is zero.
     *
     * The calculation is extremely accurate and stable, even when v
     * is very close to u or w.  In particular if we set v.s = 0 and
     * let r be the negated result (this evaluates (uw)(v.t)), then
     * r is guaranteed to satisfy MIN(u.s,w.s) <= r <= MAX(u.s,w.s).
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @param {libtess.GluVertex} w
     * @return {number}
     */
    libtess.geom.transEval = function (u, v, w) {
        var gapL = v.t - u.t;
        var gapR = w.t - v.t;
        if (gapL + gapR > 0) {
            if (gapL < gapR) {
                return (v.s - u.s) + (u.s - w.s) * (gapL / (gapL + gapR));
            }
            else {
                return (v.s - w.s) + (w.s - u.s) * (gapR / (gapL + gapR));
            }
        }
        // vertical line
        return 0;
    };
    /**
     * Version of geom.edgeSign with s and t transposed.
     * Returns a number whose sign matches geom.transEval(u,v,w) but which
     * is cheaper to evaluate.  Returns > 0, == 0 , or < 0
     * as v is above, on, or below the edge uw.
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @param {libtess.GluVertex} w
     * @return {number}
     */
    libtess.geom.transSign = function (u, v, w) {
        var gapL = v.t - u.t;
        var gapR = w.t - v.t;
        if (gapL + gapR > 0) {
            return (v.s - w.s) * gapL + (v.s - u.s) * gapR;
        }
        // vertical line
        return 0;
    };
    /**
     * Returns whether edge is directed from right to left.
     * @param {libtess.GluHalfEdge} e
     * @return {boolean}
     */
    libtess.geom.edgeGoesLeft = function (e) {
        return libtess.geom.vertLeq(e.dst(), e.org);
    };
    /**
     * Returns whether edge is directed from left to right.
     * @param {libtess.GluHalfEdge} e
     * @return {boolean}
     */
    libtess.geom.edgeGoesRight = function (e) {
        return libtess.geom.vertLeq(e.org, e.dst());
    };
    /**
     * Calculates the L1 distance between vertices u and v.
     * @param {libtess.GluVertex} u
     * @param {libtess.GluVertex} v
     * @return {number}
     */
    libtess.geom.vertL1dist = function (u, v) {
        return Math.abs(u.s - v.s) + Math.abs(u.t - v.t);
    };
    // NOTE(bckenny): vertCCW is called nowhere in libtess and isn't part of the
    // public API.
    /* istanbul ignore next */
    /**
     * For almost-degenerate situations, the results are not reliable.
     * Unless the floating-point arithmetic can be performed without
     * rounding errors, *any* implementation will give incorrect results
     * on some degenerate inputs, so the client must have some way to
     * handle this situation.
     * @param {!libtess.GluVertex} u
     * @param {!libtess.GluVertex} v
     * @param {!libtess.GluVertex} w
     * @return {boolean}
     */
    libtess.geom.vertCCW = function (u, v, w) {
        return (u.s * (v.t - w.t) + v.s * (w.t - u.t) + w.s * (u.t - v.t)) >= 0;
    };
    /**
     * Given parameters a,x,b,y returns the value (b*x+a*y)/(a+b),
     * or (x+y)/2 if a==b==0. It requires that a,b >= 0, and enforces
     * this in the rare case that one argument is slightly negative.
     * The implementation is extremely stable numerically.
     * In particular it guarantees that the result r satisfies
     * MIN(x,y) <= r <= MAX(x,y), and the results are very accurate
     * even when a and b differ greatly in magnitude.
     * @private
     * @param {number} a
     * @param {number} x
     * @param {number} b
     * @param {number} y
     * @return {number}
     */
    libtess.geom.interpolate_ = function (a, x, b, y) {
        // from Macro RealInterpolate:
        //(a = (a < 0) ? 0 : a, b = (b < 0) ? 0 : b, ((a <= b) ? ((b == 0) ? ((x+y) / 2) : (x + (y-x) * (a/(a+b)))) : (y + (x-y) * (b/(a+b)))))
        a = (a < 0) ? 0 : a;
        b = (b < 0) ? 0 : b;
        if (a <= b) {
            if (b === 0) {
                return (x + y) / 2;
            }
            else {
                return x + (y - x) * (a / (a + b));
            }
        }
        else {
            return y + (x - y) * (b / (a + b));
        }
    };
    /**
     * Given edges (o1,d1) and (o2,d2), compute their point of intersection.
     * The computed point is guaranteed to lie in the intersection of the
     * bounding rectangles defined by each edge.
     * @param {!libtess.GluVertex} o1
     * @param {!libtess.GluVertex} d1
     * @param {!libtess.GluVertex} o2
     * @param {!libtess.GluVertex} d2
     * @param {!libtess.GluVertex} v
     */
    libtess.geom.edgeIntersect = function (o1, d1, o2, d2, v) {
        // This is certainly not the most efficient way to find the intersection
        // of two line segments, but it is very numerically stable.
        // Strategy: find the two middle vertices in the VertLeq ordering,
        // and interpolate the intersection s-value from these. Then repeat
        // using the TransLeq ordering to find the intersection t-value.
        var z1;
        var z2;
        var tmp;
        if (!libtess.geom.vertLeq(o1, d1)) {
            // Swap(o1, d1);
            tmp = o1;
            o1 = d1;
            d1 = tmp;
        }
        if (!libtess.geom.vertLeq(o2, d2)) {
            // Swap(o2, d2);
            tmp = o2;
            o2 = d2;
            d2 = tmp;
        }
        if (!libtess.geom.vertLeq(o1, o2)) {
            // Swap(o1, o2);
            tmp = o1;
            o1 = o2;
            o2 = tmp;
            // Swap(d1, d2);
            tmp = d1;
            d1 = d2;
            d2 = tmp;
        }
        if (!libtess.geom.vertLeq(o2, d1)) {
            // Technically, no intersection -- do our best
            v.s = (o2.s + d1.s) / 2;
        }
        else if (libtess.geom.vertLeq(d1, d2)) {
            // Interpolate between o2 and d1
            z1 = libtess.geom.edgeEval(o1, o2, d1);
            z2 = libtess.geom.edgeEval(o2, d1, d2);
            if (z1 + z2 < 0) {
                z1 = -z1;
                z2 = -z2;
            }
            v.s = libtess.geom.interpolate_(z1, o2.s, z2, d1.s);
        }
        else {
            // Interpolate between o2 and d2
            z1 = libtess.geom.edgeSign(o1, o2, d1);
            z2 = -libtess.geom.edgeSign(o1, d2, d1);
            if (z1 + z2 < 0) {
                z1 = -z1;
                z2 = -z2;
            }
            v.s = libtess.geom.interpolate_(z1, o2.s, z2, d2.s);
        }
        // Now repeat the process for t
        if (!libtess.geom.transLeq(o1, d1)) {
            // Swap(o1, d1);
            tmp = o1;
            o1 = d1;
            d1 = tmp;
        }
        if (!libtess.geom.transLeq(o2, d2)) {
            // Swap(o2, d2);
            tmp = o2;
            o2 = d2;
            d2 = tmp;
        }
        if (!libtess.geom.transLeq(o1, o2)) {
            // Swap(o1, o2);
            tmp = o1;
            o1 = o2;
            o2 = tmp;
            // Swap(d1, d2);
            tmp = d1;
            d1 = d2;
            d2 = tmp;
        }
        if (!libtess.geom.transLeq(o2, d1)) {
            // Technically, no intersection -- do our best
            v.t = (o2.t + d1.t) / 2;
        }
        else if (libtess.geom.transLeq(d1, d2)) {
            // Interpolate between o2 and d1
            z1 = libtess.geom.transEval(o1, o2, d1);
            z2 = libtess.geom.transEval(o2, d1, d2);
            if (z1 + z2 < 0) {
                z1 = -z1;
                z2 = -z2;
            }
            v.t = libtess.geom.interpolate_(z1, o2.t, z2, d1.t);
        }
        else {
            // Interpolate between o2 and d2
            z1 = libtess.geom.transSign(o1, o2, d1);
            z2 = -libtess.geom.transSign(o1, d2, d1);
            if (z1 + z2 < 0) {
                z1 = -z1;
                z2 = -z2;
            }
            v.t = libtess.geom.interpolate_(z1, o2.t, z2, d2.t);
        }
    };
    /* global libtess */
    // TODO(bckenny): could maybe merge GluMesh and mesh.js since these are
    // operations on the mesh
    /** @const */
    libtess.mesh = {};
    /****************** Basic Edge Operations **********************/
    /**
     * makeEdge creates one edge, two vertices, and a loop (face).
     * The loop consists of the two new half-edges.
     *
     * @param {libtess.GluMesh} mesh [description].
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.mesh.makeEdge = function (mesh) {
        // TODO(bckenny): probably move to GluMesh, but needs Make* methods with it
        var e = libtess.mesh.makeEdgePair_(mesh.eHead);
        // complete edge with vertices and face (see mesh.makeEdgePair_)
        libtess.mesh.makeVertex_(e, mesh.vHead);
        libtess.mesh.makeVertex_(e.sym, mesh.vHead);
        libtess.mesh.makeFace_(e, mesh.fHead);
        return e;
    };
    /**
     * meshSplice(eOrg, eDst) is the basic operation for changing the
     * mesh connectivity and topology. It changes the mesh so that
     *  eOrg.oNext <- OLD( eDst.oNext )
     *  eDst.oNext <- OLD( eOrg.oNext )
     * where OLD(...) means the value before the meshSplice operation.
     *
     * This can have two effects on the vertex structure:
     *  - if eOrg.org != eDst.org, the two vertices are merged together
     *  - if eOrg.org == eDst.org, the origin is split into two vertices
     * In both cases, eDst.org is changed and eOrg.org is untouched.
     *
     * Similarly (and independently) for the face structure,
     *  - if eOrg.lFace == eDst.lFace, one loop is split into two
     *  - if eOrg.lFace != eDst.lFace, two distinct loops are joined into one
     * In both cases, eDst.lFace is changed and eOrg.lFace is unaffected.
     *
     * Some special cases:
     * If eDst == eOrg, the operation has no effect.
     * If eDst == eOrg.lNext, the new face will have a single edge.
     * If eDst == eOrg.lPrev(), the old face will have a single edge.
     * If eDst == eOrg.oNext, the new vertex will have a single edge.
     * If eDst == eOrg.oPrev(), the old vertex will have a single edge.
     *
     * @param {libtess.GluHalfEdge} eOrg [description].
     * @param {libtess.GluHalfEdge} eDst [description].
     */
    libtess.mesh.meshSplice = function (eOrg, eDst) {
        // TODO: more descriptive name?
        var joiningLoops = false;
        var joiningVertices = false;
        if (eOrg === eDst) {
            return;
        }
        if (eDst.org !== eOrg.org) {
            // We are merging two disjoint vertices -- destroy eDst.org
            joiningVertices = true;
            libtess.mesh.killVertex_(eDst.org, eOrg.org);
        }
        if (eDst.lFace !== eOrg.lFace) {
            // We are connecting two disjoint loops -- destroy eDst.lFace
            joiningLoops = true;
            libtess.mesh.killFace_(eDst.lFace, eOrg.lFace);
        }
        // Change the edge structure
        libtess.mesh.splice_(eDst, eOrg);
        if (!joiningVertices) {
            // We split one vertex into two -- the new vertex is eDst.org.
            // Make sure the old vertex points to a valid half-edge.
            libtess.mesh.makeVertex_(eDst, eOrg.org);
            eOrg.org.anEdge = eOrg;
        }
        if (!joiningLoops) {
            // We split one loop into two -- the new loop is eDst.lFace.
            // Make sure the old face points to a valid half-edge.
            libtess.mesh.makeFace_(eDst, eOrg.lFace);
            eOrg.lFace.anEdge = eOrg;
        }
    };
    /**
     * deleteEdge(eDel) removes the edge eDel. There are several cases:
     * if (eDel.lFace != eDel.rFace()), we join two loops into one; the loop
     * eDel.lFace is deleted. Otherwise, we are splitting one loop into two;
     * the newly created loop will contain eDel.dst(). If the deletion of eDel
     * would create isolated vertices, those are deleted as well.
     *
     * This function could be implemented as two calls to __gl_meshSplice
     * plus a few calls to memFree, but this would allocate and delete
     * unnecessary vertices and faces.
     *
     * @param {libtess.GluHalfEdge} eDel [description].
     */
    libtess.mesh.deleteEdge = function (eDel) {
        var eDelSym = eDel.sym;
        var joiningLoops = false;
        // First step: disconnect the origin vertex eDel.org.  We make all
        // changes to get a consistent mesh in this "intermediate" state.
        if (eDel.lFace !== eDel.rFace()) {
            // We are joining two loops into one -- remove the left face
            joiningLoops = true;
            libtess.mesh.killFace_(eDel.lFace, eDel.rFace());
        }
        if (eDel.oNext === eDel) {
            libtess.mesh.killVertex_(eDel.org, null);
        }
        else {
            // Make sure that eDel.org and eDel.rFace() point to valid half-edges
            eDel.rFace().anEdge = eDel.oPrev();
            eDel.org.anEdge = eDel.oNext;
            libtess.mesh.splice_(eDel, eDel.oPrev());
            if (!joiningLoops) {
                // We are splitting one loop into two -- create a new loop for eDel.
                libtess.mesh.makeFace_(eDel, eDel.lFace);
            }
        }
        // Claim: the mesh is now in a consistent state, except that eDel.org
        // may have been deleted.  Now we disconnect eDel.dst().
        if (eDelSym.oNext === eDelSym) {
            libtess.mesh.killVertex_(eDelSym.org, null);
            libtess.mesh.killFace_(eDelSym.lFace, null);
        }
        else {
            // Make sure that eDel.dst() and eDel.lFace point to valid half-edges
            eDel.lFace.anEdge = eDelSym.oPrev();
            eDelSym.org.anEdge = eDelSym.oNext;
            libtess.mesh.splice_(eDelSym, eDelSym.oPrev());
        }
        // Any isolated vertices or faces have already been freed.
        libtess.mesh.killEdge_(eDel);
    };
    /******************** Other Edge Operations **********************/
    /* All these routines can be implemented with the basic edge
     * operations above.  They are provided for convenience and efficiency.
     */
    /**
     * addEdgeVertex(eOrg) creates a new edge eNew such that
     * eNew == eOrg.lNext, and eNew.dst() is a newly created vertex.
     * eOrg and eNew will have the same left face.
     *
     * @param {libtess.GluHalfEdge} eOrg [description].
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.mesh.addEdgeVertex = function (eOrg) {
        // TODO(bckenny): why is it named this?
        var eNew = libtess.mesh.makeEdgePair_(eOrg);
        var eNewSym = eNew.sym;
        // Connect the new edge appropriately
        libtess.mesh.splice_(eNew, eOrg.lNext);
        // Set the vertex and face information
        eNew.org = eOrg.dst();
        libtess.mesh.makeVertex_(eNewSym, eNew.org);
        eNew.lFace = eNewSym.lFace = eOrg.lFace;
        return eNew;
    };
    /**
     * splitEdge(eOrg) splits eOrg into two edges eOrg and eNew,
     * such that eNew == eOrg.lNext. The new vertex is eOrg.dst() == eNew.org.
     * eOrg and eNew will have the same left face.
     *
     * @param {libtess.GluHalfEdge} eOrg [description].
     * @return {!libtess.GluHalfEdge} [description].
     */
    libtess.mesh.splitEdge = function (eOrg) {
        var tempHalfEdge = libtess.mesh.addEdgeVertex(eOrg);
        var eNew = tempHalfEdge.sym;
        // Disconnect eOrg from eOrg.dst() and connect it to eNew.org
        libtess.mesh.splice_(eOrg.sym, eOrg.sym.oPrev());
        libtess.mesh.splice_(eOrg.sym, eNew);
        // Set the vertex and face information
        eOrg.sym.org = eNew.org; // NOTE(bckenny): assignment to dst
        eNew.dst().anEdge = eNew.sym; // may have pointed to eOrg.sym
        eNew.sym.lFace = eOrg.rFace(); // NOTE(bckenny): assignment to rFace
        eNew.winding = eOrg.winding; // copy old winding information
        eNew.sym.winding = eOrg.sym.winding;
        return eNew;
    };
    /**
     * connect(eOrg, eDst) creates a new edge from eOrg.dst()
     * to eDst.org, and returns the corresponding half-edge eNew.
     * If eOrg.lFace == eDst.lFace, this splits one loop into two,
     * and the newly created loop is eNew.lFace. Otherwise, two disjoint
     * loops are merged into one, and the loop eDst.lFace is destroyed.
     *
     * If (eOrg == eDst), the new face will have only two edges.
     * If (eOrg.lNext == eDst), the old face is reduced to a single edge.
     * If (eOrg.lNext.lNext == eDst), the old face is reduced to two edges.
     *
     * @param {libtess.GluHalfEdge} eOrg [description].
     * @param {libtess.GluHalfEdge} eDst [description].
     * @return {!libtess.GluHalfEdge} [description].
     */
    libtess.mesh.connect = function (eOrg, eDst) {
        var joiningLoops = false;
        var eNew = libtess.mesh.makeEdgePair_(eOrg);
        var eNewSym = eNew.sym;
        if (eDst.lFace !== eOrg.lFace) {
            // We are connecting two disjoint loops -- destroy eDst.lFace
            joiningLoops = true;
            libtess.mesh.killFace_(eDst.lFace, eOrg.lFace);
        }
        // Connect the new edge appropriately
        libtess.mesh.splice_(eNew, eOrg.lNext);
        libtess.mesh.splice_(eNewSym, eDst);
        // Set the vertex and face information
        eNew.org = eOrg.dst();
        eNewSym.org = eDst.org;
        eNew.lFace = eNewSym.lFace = eOrg.lFace;
        // Make sure the old face points to a valid half-edge
        eOrg.lFace.anEdge = eNewSym;
        if (!joiningLoops) {
            // We split one loop into two -- the new loop is eNew.lFace
            libtess.mesh.makeFace_(eNew, eOrg.lFace);
        }
        return eNew;
    };
    /******************** Other Operations **********************/
    /**
     * zapFace(fZap) destroys a face and removes it from the
     * global face list. All edges of fZap will have a null pointer as their
     * left face. Any edges which also have a null pointer as their right face
     * are deleted entirely (along with any isolated vertices this produces).
     * An entire mesh can be deleted by zapping its faces, one at a time,
     * in any order. Zapped faces cannot be used in further mesh operations!
     *
     * @param {libtess.GluFace} fZap [description].
     */
    libtess.mesh.zapFace = function (fZap) {
        var eStart = fZap.anEdge;
        // walk around face, deleting edges whose right face is also NULL
        var eNext = eStart.lNext;
        var e;
        do {
            e = eNext;
            eNext = e.lNext;
            e.lFace = null;
            if (e.rFace() === null) {
                // delete the edge -- see mesh.deleteEdge above
                if (e.oNext === e) {
                    libtess.mesh.killVertex_(e.org, null);
                }
                else {
                    // Make sure that e.org points to a valid half-edge
                    e.org.anEdge = e.oNext;
                    libtess.mesh.splice_(e, e.oPrev());
                }
                var eSym = e.sym;
                if (eSym.oNext === eSym) {
                    libtess.mesh.killVertex_(eSym.org, null);
                }
                else {
                    // Make sure that eSym.org points to a valid half-edge
                    eSym.org.anEdge = eSym.oNext;
                    libtess.mesh.splice_(eSym, eSym.oPrev());
                }
                libtess.mesh.killEdge_(e);
            }
        } while (e !== eStart);
        // delete from circular doubly-linked list
        var fPrev = fZap.prev;
        var fNext = fZap.next;
        fNext.prev = fPrev;
        fPrev.next = fNext;
        // TODO(bckenny): memFree( fZap );
        // TODO(bckenny): probably null at callsite
    };
    // TODO(bckenny): meshUnion isn't called within libtess and isn't part of the
    // public API. Could be useful if more mesh manipulation functions are exposed.
    /* istanbul ignore next */
    /**
     * meshUnion() forms the union of all structures in
     * both meshes, and returns the new mesh (the old meshes are destroyed).
     *
     * @param {!libtess.GluMesh} mesh1
     * @param {!libtess.GluMesh} mesh2
     * @return {!libtess.GluMesh}
     */
    libtess.mesh.meshUnion = function (mesh1, mesh2) {
        // TODO(bceknny): probably move to GluMesh method
        var f1 = mesh1.fHead;
        var v1 = mesh1.vHead;
        var e1 = mesh1.eHead;
        var f2 = mesh2.fHead;
        var v2 = mesh2.vHead;
        var e2 = mesh2.eHead;
        // Add the faces, vertices, and edges of mesh2 to those of mesh1
        if (f2.next !== f2) {
            f1.prev.next = f2.next;
            f2.next.prev = f1.prev;
            f2.prev.next = f1;
            f1.prev = f2.prev;
        }
        if (v2.next !== v2) {
            v1.prev.next = v2.next;
            v2.next.prev = v1.prev;
            v2.prev.next = v1;
            v1.prev = v2.prev;
        }
        if (e2.next !== e2) {
            e1.sym.next.sym.next = e2.next;
            e2.next.sym.next = e1.sym.next;
            e2.sym.next.sym.next = e1;
            e1.sym.next = e2.sym.next;
        }
        // TODO(bckenny): memFree(mesh2);
        // TODO(bckenny): If function is kept, remove mesh2's data to enforce.
        return mesh1;
    };
    /**
     * deleteMesh(mesh) will free all storage for any valid mesh.
     * @param {libtess.GluMesh} mesh [description].
     */
    libtess.mesh.deleteMesh = function (mesh) {
        // TODO(bckenny): unnecessary, I think.
        // TODO(bckenny): might want to explicitly null at callsite
        // lots of memFrees. see also DELETE_BY_ZAPPING
    };
    /************************ Utility Routines ************************/
    /**
     * Creates a new pair of half-edges which form their own loop.
     * No vertex or face structures are allocated, but these must be assigned
     * before the current edge operation is completed.
     *
     * TODO(bckenny): warning about eNext strictly being first of pair? (see code)
     *
     * @private
     * @param {libtess.GluHalfEdge} eNext [description].
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.mesh.makeEdgePair_ = function (eNext) {
        var e = new libtess.GluHalfEdge();
        var eSym = new libtess.GluHalfEdge();
        // TODO(bckenny): how do we ensure this? see above comment in jsdoc
        // Make sure eNext points to the first edge of the edge pair
        // if (eNext->Sym < eNext ) { eNext = eNext->Sym; }
        // NOTE(bckenny): check this for bugs in current implementation!
        // Insert in circular doubly-linked list before eNext.
        // Note that the prev pointer is stored in sym.next.
        var ePrev = eNext.sym.next;
        eSym.next = ePrev;
        ePrev.sym.next = e;
        e.next = eNext;
        eNext.sym.next = eSym;
        e.sym = eSym;
        e.oNext = e;
        e.lNext = eSym;
        eSym.sym = e;
        eSym.oNext = eSym;
        eSym.lNext = e;
        return e;
    };
    /**
     * splice_ is best described by the Guibas/Stolfi paper or the
     * CS348a notes. Basically, it modifies the mesh so that
     * a.oNext and b.oNext are exchanged. This can have various effects
     * depending on whether a and b belong to different face or vertex rings.
     * For more explanation see mesh.meshSplice below.
     *
     * @private
     * @param {libtess.GluHalfEdge} a [description].
     * @param {libtess.GluHalfEdge} b [description].
     */
    libtess.mesh.splice_ = function (a, b) {
        var aONext = a.oNext;
        var bONext = b.oNext;
        aONext.sym.lNext = b;
        bONext.sym.lNext = a;
        a.oNext = bONext;
        b.oNext = aONext;
    };
    /**
     * makeVertex_(eOrig, vNext) attaches a new vertex and makes it the
     * origin of all edges in the vertex loop to which eOrig belongs. "vNext" gives
     * a place to insert the new vertex in the global vertex list.  We insert
     * the new vertex *before* vNext so that algorithms which walk the vertex
     * list will not see the newly created vertices.
     *
     * NOTE: unlike original, acutally allocates new vertex.
     *
     * @private
     * @param {libtess.GluHalfEdge} eOrig [description].
     * @param {libtess.GluVertex} vNext [description].
     */
    libtess.mesh.makeVertex_ = function (eOrig, vNext) {
        // insert in circular doubly-linked list before vNext
        var vPrev = vNext.prev;
        var vNew = new libtess.GluVertex(vNext, vPrev);
        vPrev.next = vNew;
        vNext.prev = vNew;
        vNew.anEdge = eOrig;
        // leave coords, s, t undefined
        // TODO(bckenny): does above line mean 0 specifically, or does it matter?
        // fix other edges on this vertex loop
        var e = eOrig;
        do {
            e.org = vNew;
            e = e.oNext;
        } while (e !== eOrig);
    };
    /**
     * makeFace_(eOrig, fNext) attaches a new face and makes it the left
     * face of all edges in the face loop to which eOrig belongs. "fNext" gives
     * a place to insert the new face in the global face list.  We insert
     * the new face *before* fNext so that algorithms which walk the face
     * list will not see the newly created faces.
     *
     * NOTE: unlike original, acutally allocates new face.
     *
     * @private
     * @param {libtess.GluHalfEdge} eOrig [description].
     * @param {libtess.GluFace} fNext [description].
     */
    libtess.mesh.makeFace_ = function (eOrig, fNext) {
        // insert in circular doubly-linked list before fNext
        var fPrev = fNext.prev;
        var fNew = new libtess.GluFace(fNext, fPrev);
        fPrev.next = fNew;
        fNext.prev = fNew;
        fNew.anEdge = eOrig;
        // The new face is marked "inside" if the old one was.  This is a
        // convenience for the common case where a face has been split in two.
        fNew.inside = fNext.inside;
        // fix other edges on this face loop
        var e = eOrig;
        do {
            e.lFace = fNew;
            e = e.lNext;
        } while (e !== eOrig);
    };
    /**
     * killEdge_ destroys an edge (the half-edges eDel and eDel.sym),
     * and removes from the global edge list.
     *
     * @private
     * @param {libtess.GluHalfEdge} eDel [description].
     */
    libtess.mesh.killEdge_ = function (eDel) {
        // TODO(bckenny): in this case, no need to worry(?), but check when checking mesh.makeEdgePair_
        // Half-edges are allocated in pairs, see EdgePair above
        // if (eDel->Sym < eDel ) { eDel = eDel->Sym; }
        // delete from circular doubly-linked list
        var eNext = eDel.next;
        var ePrev = eDel.sym.next;
        eNext.sym.next = ePrev;
        ePrev.sym.next = eNext;
        // TODO(bckenny): memFree( eDel ); (which also frees eDel.sym)
        // TODO(bckenny): need to null at callsites?
    };
    /**
     * killVertex_ destroys a vertex and removes it from the global
     * vertex list. It updates the vertex loop to point to a given new vertex.
     *
     * @private
     * @param {libtess.GluVertex} vDel [description].
     * @param {libtess.GluVertex} newOrg [description].
     */
    libtess.mesh.killVertex_ = function (vDel, newOrg) {
        var eStart = vDel.anEdge;
        // change the origin of all affected edges
        var e = eStart;
        do {
            e.org = newOrg;
            e = e.oNext;
        } while (e !== eStart);
        // delete from circular doubly-linked list
        var vPrev = vDel.prev;
        var vNext = vDel.next;
        vNext.prev = vPrev;
        vPrev.next = vNext;
        // TODO(bckenny): memFree( vDel );
        // TODO(bckenny): need to null at callsites?
    };
    /**
     * killFace_ destroys a face and removes it from the global face
     * list. It updates the face loop to point to a given new face.
     *
     * @private
     * @param {libtess.GluFace} fDel [description].
     * @param {libtess.GluFace} newLFace [description].
     */
    libtess.mesh.killFace_ = function (fDel, newLFace) {
        var eStart = fDel.anEdge;
        // change the left face of all affected edges
        var e = eStart;
        do {
            e.lFace = newLFace;
            e = e.lNext;
        } while (e !== eStart);
        // delete from circular doubly-linked list
        var fPrev = fDel.prev;
        var fNext = fDel.next;
        fNext.prev = fPrev;
        fPrev.next = fNext;
        // TODO(bckenny): memFree( fDel );
        // TODO(bckenny): need to null at callsites?
    };
    /* global libtess */
    /** @const */
    libtess.normal = {};
    // TODO(bckenny): Integrate SLANTED_SWEEP somehow?
    /* The "feature merging" is not intended to be complete. There are
     * special cases where edges are nearly parallel to the sweep line
     * which are not implemented. The algorithm should still behave
     * robustly (ie. produce a reasonable tesselation) in the presence
     * of such edges, however it may miss features which could have been
     * merged. We could minimize this effect by choosing the sweep line
     * direction to be something unusual (ie. not parallel to one of the
     * coordinate axes).
     * #if defined(SLANTED_SWEEP)
     * #define S_UNIT_X  0.50941539564955385 // Pre-normalized
     * #define S_UNIT_Y  0.86052074622010633
     * #endif
     */
    /**
     * X coordinate of local basis for polygon projection.
     * @private {number}
     * @const
     */
    libtess.normal.S_UNIT_X_ = 1.0;
    /**
     * Y coordinate of local basis for polygon projection.
     * @private {number}
     * @const
     */
    libtess.normal.S_UNIT_Y_ = 0.0;
    /**
     * Determines a polygon normal and projects vertices onto the plane of the
     * polygon. A pre-computed normal for the data may be provided, or set to the
     * zero vector if one should be computed from it.
     * @param {!libtess.GluTesselator} tess
     * @param {number} normalX
     * @param {number} normalY
     * @param {number} normalZ
     */
    libtess.normal.projectPolygon = function (tess, normalX, normalY, normalZ) {
        var computedNormal = false;
        var norm = [
            normalX,
            normalY,
            normalZ
        ];
        if (normalX === 0 && normalY === 0 && normalZ === 0) {
            libtess.normal.computeNormal_(tess, norm);
            computedNormal = true;
        }
        var i = libtess.normal.longAxis_(norm);
        var vHead = tess.mesh.vHead;
        var v;
        // NOTE(bckenny): This branch is never taken. See comment on
        // libtess.TRUE_PROJECT.
        /* istanbul ignore if */
        if (libtess.TRUE_PROJECT) {
            // Choose the initial sUnit vector to be approximately perpendicular
            // to the normal.
            libtess.normal.normalize_(norm);
            var sUnit = [0, 0, 0];
            var tUnit = [0, 0, 0];
            sUnit[i] = 0;
            sUnit[(i + 1) % 3] = libtess.normal.S_UNIT_X_;
            sUnit[(i + 2) % 3] = libtess.normal.S_UNIT_Y_;
            // Now make it exactly perpendicular
            var w = libtess.normal.dot_(sUnit, norm);
            sUnit[0] -= w * norm[0];
            sUnit[1] -= w * norm[1];
            sUnit[2] -= w * norm[2];
            libtess.normal.normalize_(sUnit);
            // Choose tUnit so that (sUnit,tUnit,norm) form a right-handed frame
            tUnit[0] = norm[1] * sUnit[2] - norm[2] * sUnit[1];
            tUnit[1] = norm[2] * sUnit[0] - norm[0] * sUnit[2];
            tUnit[2] = norm[0] * sUnit[1] - norm[1] * sUnit[0];
            libtess.normal.normalize_(tUnit);
            // Project the vertices onto the sweep plane
            for (v = vHead.next; v !== vHead; v = v.next) {
                v.s = libtess.normal.dot_(v.coords, sUnit);
                v.t = libtess.normal.dot_(v.coords, tUnit);
            }
        }
        else {
            // Project perpendicular to a coordinate axis -- better numerically
            var sAxis = (i + 1) % 3;
            var tAxis = (i + 2) % 3;
            var tNegate = norm[i] > 0 ? 1 : -1;
            // Project the vertices onto the sweep plane
            for (v = vHead.next; v !== vHead; v = v.next) {
                v.s = v.coords[sAxis];
                v.t = tNegate * v.coords[tAxis];
            }
        }
        if (computedNormal) {
            libtess.normal.checkOrientation_(tess);
        }
    };
    // NOTE(bckenny): libtess.normal.dot_ is no longer called in code without
    // libtess.TRUE_PROJECT defined.
    /* istanbul ignore next */
    /**
     * Computes the dot product of vectors u and v.
     * @private
     * @param {!Array<number>} u
     * @param {!Array<number>} v
     * @return {number}
     */
    libtess.normal.dot_ = function (u, v) {
        return u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
    };
    // NOTE(bckenny): only called from within libtess.normal.projectPolygon's
    // TRUE_PROJECT branch, so ignoring for code coverage.
    /* istanbul ignore next */
    /**
     * Normalize vector v.
     * @private
     * @param {!Array<number>} v
     */
    libtess.normal.normalize_ = function (v) {
        var len = v[0] * v[0] + v[1] * v[1] + v[2] * v[2];
        len = Math.sqrt(len);
        v[0] /= len;
        v[1] /= len;
        v[2] /= len;
    };
    /**
     * Returns the index of the longest component of vector v.
     * @private
     * @param {!Array<number>} v
     * @return {number}
     */
    libtess.normal.longAxis_ = function (v) {
        var i = 0;
        if (Math.abs(v[1]) > Math.abs(v[0])) {
            i = 1;
        }
        if (Math.abs(v[2]) > Math.abs(v[i])) {
            i = 2;
        }
        return i;
    };
    /**
     * Compute an approximate normal of the polygon from the vertices themselves.
     * Result returned in norm.
     * @private
     * @param {!libtess.GluTesselator} tess
     * @param {!Array<number>} norm
     */
    libtess.normal.computeNormal_ = function (tess, norm) {
        var maxVal = [
            -2 * libtess.GLU_TESS_MAX_COORD,
            -2 * libtess.GLU_TESS_MAX_COORD,
            -2 * libtess.GLU_TESS_MAX_COORD
        ];
        var minVal = [
            2 * libtess.GLU_TESS_MAX_COORD,
            2 * libtess.GLU_TESS_MAX_COORD,
            2 * libtess.GLU_TESS_MAX_COORD
        ];
        var maxVert = [];
        var minVert = [];
        var v;
        var vHead = tess.mesh.vHead;
        for (v = vHead.next; v !== vHead; v = v.next) {
            for (var i = 0; i < 3; ++i) {
                var c = v.coords[i];
                if (c < minVal[i]) {
                    minVal[i] = c;
                    minVert[i] = v;
                }
                if (c > maxVal[i]) {
                    maxVal[i] = c;
                    maxVert[i] = v;
                }
            }
        }
        // Find two vertices separated by at least 1/sqrt(3) of the maximum
        // distance between any two vertices
        var index = 0;
        if (maxVal[1] - minVal[1] > maxVal[0] - minVal[0]) {
            index = 1;
        }
        if (maxVal[2] - minVal[2] > maxVal[index] - minVal[index]) {
            index = 2;
        }
        if (minVal[index] >= maxVal[index]) {
            // All vertices are the same -- normal doesn't matter
            norm[0] = 0;
            norm[1] = 0;
            norm[2] = 1;
            return;
        }
        // Look for a third vertex which forms the triangle with maximum area
        // (Length of normal == twice the triangle area)
        var maxLen2 = 0;
        var v1 = minVert[index];
        var v2 = maxVert[index];
        var tNorm = [0, 0, 0];
        var d1 = [
            v1.coords[0] - v2.coords[0],
            v1.coords[1] - v2.coords[1],
            v1.coords[2] - v2.coords[2]
        ];
        var d2 = [0, 0, 0];
        for (v = vHead.next; v !== vHead; v = v.next) {
            d2[0] = v.coords[0] - v2.coords[0];
            d2[1] = v.coords[1] - v2.coords[1];
            d2[2] = v.coords[2] - v2.coords[2];
            tNorm[0] = d1[1] * d2[2] - d1[2] * d2[1];
            tNorm[1] = d1[2] * d2[0] - d1[0] * d2[2];
            tNorm[2] = d1[0] * d2[1] - d1[1] * d2[0];
            var tLen2 = tNorm[0] * tNorm[0] + tNorm[1] * tNorm[1] + tNorm[2] * tNorm[2];
            if (tLen2 > maxLen2) {
                maxLen2 = tLen2;
                norm[0] = tNorm[0];
                norm[1] = tNorm[1];
                norm[2] = tNorm[2];
            }
        }
        if (maxLen2 <= 0) {
            // All points lie on a single line -- any decent normal will do
            norm[0] = norm[1] = norm[2] = 0;
            norm[libtess.normal.longAxis_(d1)] = 1;
        }
    };
    /**
     * Check that the sum of the signed area of all projected contours is
     * non-negative. If not, negate the t-coordinates to reverse the orientation and
     * make it so.
     * @private
     * @param {!libtess.GluTesselator} tess
     */
    libtess.normal.checkOrientation_ = function (tess) {
        var area = 0;
        var fHead = tess.mesh.fHead;
        for (var f = fHead.next; f !== fHead; f = f.next) {
            var e = f.anEdge;
            if (e.winding <= 0) {
                continue;
            }
            do {
                area += (e.org.s - e.dst().s) * (e.org.t + e.dst().t);
                e = e.lNext;
            } while (e !== f.anEdge);
        }
        if (area < 0) {
            // Reverse the orientation by flipping all the t-coordinates
            var vHead = tess.mesh.vHead;
            for (var v = vHead.next; v !== vHead; v = v.next) {
                v.t = -v.t;
            }
        }
    };
    /* global libtess */
    /** @const */
    libtess.render = {};
    /**
     * Takes a mesh, breaks it into separate triangles, and renders them. The
     * rendering output is provided as callbacks (see the API). Set flagEdges to
     * true to get edgeFlag callbacks (tess.flagBoundary in original libtess).
     * @param {!libtess.GluTesselator} tess
     * @param {!libtess.GluMesh} mesh
     * @param {boolean} flagEdges
     */
    libtess.render.renderMesh = function (tess, mesh, flagEdges) {
        var beginCallbackCalled = false;
        // TODO(bckenny): edgeState needs to be boolean, but !== on first call
        // force edge state output for first vertex
        var edgeState = -1;
        // We examine all faces in an arbitrary order. Whenever we find
        // an inside triangle f, we render f.
        // NOTE(bckenny): go backwards through face list to match original libtess
        // triangle order
        for (var f = mesh.fHead.prev; f !== mesh.fHead; f = f.prev) {
            if (f.inside) {
                // We're going to emit a triangle, so call begin callback once
                if (!beginCallbackCalled) {
                    tess.callBeginCallback(libtess.primitiveType.GL_TRIANGLES);
                    beginCallbackCalled = true;
                }
                // check that face has only three edges
                var e = f.anEdge;
                // Loop once for each edge (there will always be 3 edges)
                do {
                    if (flagEdges) {
                        // Set the "edge state" to true just before we output the
                        // first vertex of each edge on the polygon boundary.
                        var newState = !e.rFace().inside ? 1 : 0; // TODO(bckenny): total hack to get edgeState working. fix me.
                        if (edgeState !== newState) {
                            edgeState = newState;
                            // TODO(bckenny): edgeState should be boolean now
                            tess.callEdgeFlagCallback(!!edgeState);
                        }
                    }
                    // emit vertex
                    tess.callVertexCallback(e.org.data);
                    e = e.lNext;
                } while (e !== f.anEdge);
            }
        }
        // only call end callback if begin was called
        if (beginCallbackCalled) {
            tess.callEndCallback();
        }
    };
    /**
     * Takes a mesh, and outputs one contour for each face marked "inside". The
     * rendering output is provided as callbacks (see the API).
     * @param {!libtess.GluTesselator} tess
     * @param {!libtess.GluMesh} mesh
     */
    libtess.render.renderBoundary = function (tess, mesh) {
        for (var f = mesh.fHead.next; f !== mesh.fHead; f = f.next) {
            if (f.inside) {
                tess.callBeginCallback(libtess.primitiveType.GL_LINE_LOOP);
                var e = f.anEdge;
                do {
                    tess.callVertexCallback(e.org.data);
                    e = e.lNext;
                } while (e !== f.anEdge);
                tess.callEndCallback();
            }
        }
    };
    /* global libtess */
    // TODO(bckenny): a number of these never return null (as opposed to original) and should be typed appropriately
    /*
     * Invariants for the Edge Dictionary.
     * - each pair of adjacent edges e2=succ(e1) satisfies edgeLeq_(e1,e2)
     *   at any valid location of the sweep event
     * - if edgeLeq_(e2,e1) as well (at any valid sweep event), then e1 and e2
     *   share a common endpoint
     * - for each e, e.dst() has been processed, but not e.org
     * - each edge e satisfies vertLeq(e.dst(),event) && vertLeq(event,e.org)
     *   where "event" is the current sweep line event.
     * - no edge e has zero length
     *
     * Invariants for the Mesh (the processed portion).
     * - the portion of the mesh left of the sweep line is a planar graph,
     *   ie. there is *some* way to embed it in the plane
     * - no processed edge has zero length
     * - no two processed vertices have identical coordinates
     * - each "inside" region is monotone, ie. can be broken into two chains
     *   of monotonically increasing vertices according to VertLeq(v1,v2)
     *   - a non-invariant: these chains may intersect (very slightly)
     *
     * Invariants for the Sweep.
     * - if none of the edges incident to the event vertex have an activeRegion
     *   (ie. none of these edges are in the edge dictionary), then the vertex
     *   has only right-going edges.
     * - if an edge is marked "fixUpperEdge" (it is a temporary edge introduced
     *   by ConnectRightVertex), then it is the only right-going edge from
     *   its associated vertex.  (This says that these edges exist only
     *   when it is necessary.)
     */
    /** @const */
    libtess.sweep = {};
    /**
     * Make the sentinel coordinates big enough that they will never be
     * merged with real input features.  (Even with the largest possible
     * input contour and the maximum tolerance of 1.0, no merging will be
     * done with coordinates larger than 3 * libtess.GLU_TESS_MAX_COORD).
     * @private
     * @const
     * @type {number}
     */
    libtess.sweep.SENTINEL_COORD_ = 4 * libtess.GLU_TESS_MAX_COORD;
    /**
     * Because vertices at exactly the same location are merged together
     * before we process the sweep event, some degenerate cases can't occur.
     * However if someone eventually makes the modifications required to
     * merge features which are close together, the cases below marked
     * TOLERANCE_NONZERO will be useful.  They were debugged before the
     * code to merge identical vertices in the main loop was added.
     * @private
     * @const
     * @type {boolean}
     */
    libtess.sweep.TOLERANCE_NONZERO_ = false;
    /**
     * computeInterior(tess) computes the planar arrangement specified
     * by the given contours, and further subdivides this arrangement
     * into regions. Each region is marked "inside" if it belongs
     * to the polygon, according to the rule given by tess.windingRule.
     * Each interior region is guaranteed be monotone.
     *
     * @param {libtess.GluTesselator} tess [description].
     */
    libtess.sweep.computeInterior = function (tess) {
        tess.fatalError = false;
        // Each vertex defines an event for our sweep line. Start by inserting
        // all the vertices in a priority queue. Events are processed in
        // lexicographic order, ie.
        // e1 < e2  iff  e1.x < e2.x || (e1.x == e2.x && e1.y < e2.y)
        libtess.sweep.removeDegenerateEdges_(tess);
        libtess.sweep.initPriorityQ_(tess);
        libtess.sweep.initEdgeDict_(tess);
        var v;
        while ((v = tess.pq.extractMin()) !== null) {
            for (;;) {
                var vNext = tess.pq.minimum();
                if (vNext === null || !libtess.geom.vertEq(vNext, v)) {
                    break;
                }
                /* Merge together all vertices at exactly the same location.
                 * This is more efficient than processing them one at a time,
                 * simplifies the code (see connectLeftDegenerate), and is also
                 * important for correct handling of certain degenerate cases.
                 * For example, suppose there are two identical edges A and B
                 * that belong to different contours (so without this code they would
                 * be processed by separate sweep events).  Suppose another edge C
                 * crosses A and B from above.  When A is processed, we split it
                 * at its intersection point with C.  However this also splits C,
                 * so when we insert B we may compute a slightly different
                 * intersection point.  This might leave two edges with a small
                 * gap between them.  This kind of error is especially obvious
                 * when using boundary extraction (GLU_TESS_BOUNDARY_ONLY).
                 */
                vNext = tess.pq.extractMin();
                libtess.sweep.spliceMergeVertices_(tess, v.anEdge, vNext.anEdge);
            }
            libtess.sweep.sweepEvent_(tess, v);
        }
        // TODO(bckenny): what does the next comment mean? can we eliminate event except when debugging?
        // Set tess.event for debugging purposes
        var minRegion = tess.dict.getMin().getKey();
        tess.event = minRegion.eUp.org;
        libtess.sweep.doneEdgeDict_(tess);
        libtess.sweep.donePriorityQ_(tess);
        libtess.sweep.removeDegenerateFaces_(tess.mesh);
        tess.mesh.checkMesh();
    };
    /**
     * When we merge two edges into one, we need to compute the combined
     * winding of the new edge.
     * @private
     * @param {libtess.GluHalfEdge} eDst [description].
     * @param {libtess.GluHalfEdge} eSrc [description].
     */
    libtess.sweep.addWinding_ = function (eDst, eSrc) {
        // NOTE(bckenny): from AddWinding macro
        eDst.winding += eSrc.winding;
        eDst.sym.winding += eSrc.sym.winding;
    };
    /**
     * Both edges must be directed from right to left (this is the canonical
     * direction for the upper edge of each region).
     *
     * The strategy is to evaluate a "t" value for each edge at the
     * current sweep line position, given by tess.event.  The calculations
     * are designed to be very stable, but of course they are not perfect.
     *
     * Special case: if both edge destinations are at the sweep event,
     * we sort the edges by slope (they would otherwise compare equally).
     *
     * @private
     * @param {!libtess.GluTesselator} tess
     * @param {!libtess.ActiveRegion} reg1
     * @param {!libtess.ActiveRegion} reg2
     * @return {boolean}
     */
    libtess.sweep.edgeLeq_ = function (tess, reg1, reg2) {
        var event = tess.event;
        var e1 = reg1.eUp;
        var e2 = reg2.eUp;
        if (e1.dst() === event) {
            if (e2.dst() === event) {
                // Two edges right of the sweep line which meet at the sweep event.
                // Sort them by slope.
                if (libtess.geom.vertLeq(e1.org, e2.org)) {
                    return libtess.geom.edgeSign(e2.dst(), e1.org, e2.org) <= 0;
                }
                return libtess.geom.edgeSign(e1.dst(), e2.org, e1.org) >= 0;
            }
            return libtess.geom.edgeSign(e2.dst(), event, e2.org) <= 0;
        }
        if (e2.dst() === event) {
            return libtess.geom.edgeSign(e1.dst(), event, e1.org) >= 0;
        }
        // General case - compute signed distance *from* e1, e2 to event
        var t1 = libtess.geom.edgeEval(e1.dst(), event, e1.org);
        var t2 = libtess.geom.edgeEval(e2.dst(), event, e2.org);
        return (t1 >= t2);
    };
    /**
     * [deleteRegion_ description]
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} reg [description].
     */
    libtess.sweep.deleteRegion_ = function (tess, reg) {
        if (reg.fixUpperEdge) {
            // It was created with zero winding number, so it better be
            // deleted with zero winding number (ie. it better not get merged
            // with a real edge).
        }
        reg.eUp.activeRegion = null;
        tess.dict.deleteNode(reg.nodeUp);
        reg.nodeUp = null;
        // memFree( reg ); TODO(bckenny)
        // TODO(bckenny): may need to null at callsite
    };
    /**
     * Replace an upper edge which needs fixing (see connectRightVertex).
     * @private
     * @param {libtess.ActiveRegion} reg [description].
     * @param {libtess.GluHalfEdge} newEdge [description].
     */
    libtess.sweep.fixUpperEdge_ = function (reg, newEdge) {
        libtess.mesh.deleteEdge(reg.eUp);
        reg.fixUpperEdge = false;
        reg.eUp = newEdge;
        newEdge.activeRegion = reg;
    };
    /**
     * Find the region above the uppermost edge with the same origin.
     * @private
     * @param {libtess.ActiveRegion} reg [description].
     * @return {libtess.ActiveRegion} [description].
     */
    libtess.sweep.topLeftRegion_ = function (reg) {
        var org = reg.eUp.org;
        // Find the region above the uppermost edge with the same origin
        do {
            reg = reg.regionAbove();
        } while (reg.eUp.org === org);
        // If the edge above was a temporary edge introduced by connectRightVertex,
        // now is the time to fix it.
        if (reg.fixUpperEdge) {
            var e = libtess.mesh.connect(reg.regionBelow().eUp.sym, reg.eUp.lNext);
            libtess.sweep.fixUpperEdge_(reg, e);
            reg = reg.regionAbove();
        }
        return reg;
    };
    /**
     * Find the region above the uppermost edge with the same destination.
     * @private
     * @param {libtess.ActiveRegion} reg [description].
     * @return {libtess.ActiveRegion} [description].
     */
    libtess.sweep.topRightRegion_ = function (reg) {
        var dst = reg.eUp.dst();
        do {
            reg = reg.regionAbove();
        } while (reg.eUp.dst() === dst);
        return reg;
    };
    /**
     * Add a new active region to the sweep line, *somewhere* below "regAbove"
     * (according to where the new edge belongs in the sweep-line dictionary).
     * The upper edge of the new region will be "eNewUp".
     * Winding number and "inside" flag are not updated.
     *
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} regAbove [description].
     * @param {libtess.GluHalfEdge} eNewUp [description].
     * @return {libtess.ActiveRegion} regNew.
     */
    libtess.sweep.addRegionBelow_ = function (tess, regAbove, eNewUp) {
        var regNew = new libtess.ActiveRegion();
        regNew.eUp = eNewUp;
        regNew.nodeUp = tess.dict.insertBefore(regAbove.nodeUp, regNew);
        eNewUp.activeRegion = regNew;
        return regNew;
    };
    /**
     * [isWindingInside_ description]
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {number} n int.
     * @return {boolean} [description].
     */
    libtess.sweep.isWindingInside_ = function (tess, n) {
        switch (tess.windingRule) {
            case libtess.windingRule.GLU_TESS_WINDING_ODD:
                return ((n & 1) !== 0);
            case libtess.windingRule.GLU_TESS_WINDING_NONZERO:
                return (n !== 0);
            case libtess.windingRule.GLU_TESS_WINDING_POSITIVE:
                return (n > 0);
            case libtess.windingRule.GLU_TESS_WINDING_NEGATIVE:
                return (n < 0);
            case libtess.windingRule.GLU_TESS_WINDING_ABS_GEQ_TWO:
                return (n >= 2) || (n <= -2);
        }
        // TODO(bckenny): not reached
        return false;
    };
    /**
     * [computeWinding_ description]
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} reg [description].
     */
    libtess.sweep.computeWinding_ = function (tess, reg) {
        reg.windingNumber = reg.regionAbove().windingNumber + reg.eUp.winding;
        reg.inside = libtess.sweep.isWindingInside_(tess, reg.windingNumber);
    };
    /**
     * Delete a region from the sweep line. This happens when the upper
     * and lower chains of a region meet (at a vertex on the sweep line).
     * The "inside" flag is copied to the appropriate mesh face (we could
     * not do this before -- since the structure of the mesh is always
     * changing, this face may not have even existed until now).
     *
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} reg [description].
     */
    libtess.sweep.finishRegion_ = function (tess, reg) {
        // TODO(bckenny): may need to null reg at callsite
        var e = reg.eUp;
        var f = e.lFace;
        f.inside = reg.inside;
        f.anEdge = e; // optimization for tessmono.tessellateMonoRegion() // TODO(bckenny): how so?
        libtess.sweep.deleteRegion_(tess, reg);
    };
    /**
     * We are given a vertex with one or more left-going edges. All affected
     * edges should be in the edge dictionary. Starting at regFirst.eUp,
     * we walk down deleting all regions where both edges have the same
     * origin vOrg. At the same time we copy the "inside" flag from the
     * active region to the face, since at this point each face will belong
     * to at most one region (this was not necessarily true until this point
     * in the sweep). The walk stops at the region above regLast; if regLast
     * is null we walk as far as possible. At the same time we relink the
     * mesh if necessary, so that the ordering of edges around vOrg is the
     * same as in the dictionary.
     *
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} regFirst [description].
     * @param {libtess.ActiveRegion} regLast [description].
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.sweep.finishLeftRegions_ = function (tess, regFirst, regLast) {
        var regPrev = regFirst;
        var ePrev = regFirst.eUp;
        while (regPrev !== regLast) {
            // placement was OK
            regPrev.fixUpperEdge = false;
            var reg = regPrev.regionBelow();
            var e = reg.eUp;
            if (e.org !== ePrev.org) {
                if (!reg.fixUpperEdge) {
                    /* Remove the last left-going edge. Even though there are no further
                     * edges in the dictionary with this origin, there may be further
                     * such edges in the mesh (if we are adding left edges to a vertex
                     * that has already been processed). Thus it is important to call
                     * finishRegion rather than just deleteRegion.
                     */
                    libtess.sweep.finishRegion_(tess, regPrev);
                    break;
                }
                // If the edge below was a temporary edge introduced by
                // connectRightVertex, now is the time to fix it.
                e = libtess.mesh.connect(ePrev.lPrev(), e.sym);
                libtess.sweep.fixUpperEdge_(reg, e);
            }
            // Relink edges so that ePrev.oNext === e
            if (ePrev.oNext !== e) {
                libtess.mesh.meshSplice(e.oPrev(), e);
                libtess.mesh.meshSplice(ePrev, e);
            }
            // may change reg.eUp
            libtess.sweep.finishRegion_(tess, regPrev);
            ePrev = reg.eUp;
            regPrev = reg;
        }
        return ePrev;
    };
    /**
     * Purpose: insert right-going edges into the edge dictionary, and update
     * winding numbers and mesh connectivity appropriately. All right-going
     * edges share a common origin vOrg. Edges are inserted CCW starting at
     * eFirst; the last edge inserted is eLast.oPrev. If vOrg has any
     * left-going edges already processed, then eTopLeft must be the edge
     * such that an imaginary upward vertical segment from vOrg would be
     * contained between eTopLeft.oPrev and eTopLeft; otherwise eTopLeft
     * should be null.
     *
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} regUp [description].
     * @param {libtess.GluHalfEdge} eFirst [description].
     * @param {libtess.GluHalfEdge} eLast [description].
     * @param {libtess.GluHalfEdge} eTopLeft [description].
     * @param {boolean} cleanUp [description].
     */
    libtess.sweep.addRightEdges_ = function (tess, regUp, eFirst, eLast, eTopLeft, cleanUp) {
        var firstTime = true;
        // Insert the new right-going edges in the dictionary
        var e = eFirst;
        do {
            libtess.sweep.addRegionBelow_(tess, regUp, e.sym);
            e = e.oNext;
        } while (e !== eLast);
        // Walk *all* right-going edges from e.org, in the dictionary order,
        // updating the winding numbers of each region, and re-linking the mesh
        // edges to match the dictionary ordering (if necessary).
        if (eTopLeft === null) {
            eTopLeft = regUp.regionBelow().eUp.rPrev();
        }
        var regPrev = regUp;
        var ePrev = eTopLeft;
        var reg;
        for (;;) {
            reg = regPrev.regionBelow();
            e = reg.eUp.sym;
            if (e.org !== ePrev.org) {
                break;
            }
            if (e.oNext !== ePrev) {
                // Unlink e from its current position, and relink below ePrev
                libtess.mesh.meshSplice(e.oPrev(), e);
                libtess.mesh.meshSplice(ePrev.oPrev(), e);
            }
            // Compute the winding number and "inside" flag for the new regions
            reg.windingNumber = regPrev.windingNumber - e.winding;
            reg.inside = libtess.sweep.isWindingInside_(tess, reg.windingNumber);
            // Check for two outgoing edges with same slope -- process these
            // before any intersection tests (see example in libtess.sweep.computeInterior).
            regPrev.dirty = true;
            if (!firstTime && libtess.sweep.checkForRightSplice_(tess, regPrev)) {
                libtess.sweep.addWinding_(e, ePrev);
                libtess.sweep.deleteRegion_(tess, regPrev); // TODO(bckenny): need to null regPrev anywhere else?
                libtess.mesh.deleteEdge(ePrev);
            }
            firstTime = false;
            regPrev = reg;
            ePrev = e;
        }
        regPrev.dirty = true;
        if (cleanUp) {
            // Check for intersections between newly adjacent edges.
            libtess.sweep.walkDirtyRegions_(tess, regPrev);
        }
    };
    /**
     * Set up data for and call GLU_TESS_COMBINE callback on GluTesselator.
     * @private
     * @param {!libtess.GluTesselator} tess
     * @param {!libtess.GluVertex} isect A raw vertex at the intersection.
     * @param {!Array<Object>} data The vertices of the intersecting edges.
     * @param {!Array<number>} weights The linear combination coefficients for this intersection.
     * @param {boolean} needed Whether a returned vertex is necessary in this case.
     */
    libtess.sweep.callCombine_ = function (tess, isect, data, weights, needed) {
        // Copy coord data in case the callback changes it.
        var coords = [
            isect.coords[0],
            isect.coords[1],
            isect.coords[2]
        ];
        isect.data = null;
        isect.data = tess.callCombineCallback(coords, data, weights);
        if (isect.data === null) {
            if (!needed) {
                // not needed, so just use data from first vertex
                isect.data = data[0];
            }
            else if (!tess.fatalError) {
                // The only way fatal error is when two edges are found to intersect,
                // but the user has not provided the callback necessary to handle
                // generated intersection points.
                tess.callErrorCallback(libtess.errorType.GLU_TESS_NEED_COMBINE_CALLBACK);
                tess.fatalError = true;
            }
        }
    };
    /**
     * Two vertices with idential coordinates are combined into one.
     * e1.org is kept, while e2.org is discarded.
     * @private
     * @param {!libtess.GluTesselator} tess
     * @param {libtess.GluHalfEdge} e1 [description].
     * @param {libtess.GluHalfEdge} e2 [description].
     */
    libtess.sweep.spliceMergeVertices_ = function (tess, e1, e2) {
        // TODO(bckenny): better way to init these? save them?
        var data = [null, null, null, null];
        var weights = [0.5, 0.5, 0, 0];
        data[0] = e1.org.data;
        data[1] = e2.org.data;
        libtess.sweep.callCombine_(tess, e1.org, data, weights, false);
        libtess.mesh.meshSplice(e1, e2);
    };
    /**
     * Find some weights which describe how the intersection vertex is
     * a linear combination of org and dst. Each of the two edges
     * which generated "isect" is allocated 50% of the weight; each edge
     * splits the weight between its org and dst according to the
     * relative distance to "isect".
     *
     * @private
     * @param {libtess.GluVertex} isect [description].
     * @param {libtess.GluVertex} org [description].
     * @param {libtess.GluVertex} dst [description].
     * @param {Array.<number>} weights [description].
     * @param {number} weightIndex Index into weights for first weight to supply.
     */
    libtess.sweep.vertexWeights_ = function (isect, org, dst, weights, weightIndex) {
        // TODO(bckenny): think through how we can use L1dist here and be correct for coords
        var t1 = libtess.geom.vertL1dist(org, isect);
        var t2 = libtess.geom.vertL1dist(dst, isect);
        // TODO(bckenny): introduced weightIndex to mimic addressing in original
        // 1) document (though it is private and only used from getIntersectData)
        // 2) better way? manually inline into getIntersectData? supply two two-length tmp arrays?
        var i0 = weightIndex;
        var i1 = weightIndex + 1;
        weights[i0] = 0.5 * t2 / (t1 + t2);
        weights[i1] = 0.5 * t1 / (t1 + t2);
        isect.coords[0] += weights[i0] * org.coords[0] + weights[i1] * dst.coords[0];
        isect.coords[1] += weights[i0] * org.coords[1] + weights[i1] * dst.coords[1];
        isect.coords[2] += weights[i0] * org.coords[2] + weights[i1] * dst.coords[2];
    };
    /**
     * We've computed a new intersection point, now we need a "data" pointer
     * from the user so that we can refer to this new vertex in the
     * rendering callbacks.
     * @private
     * @param {!libtess.GluTesselator} tess
     * @param {libtess.GluVertex} isect [description].
     * @param {libtess.GluVertex} orgUp [description].
     * @param {libtess.GluVertex} dstUp [description].
     * @param {libtess.GluVertex} orgLo [description].
     * @param {libtess.GluVertex} dstLo [description].
     */
    libtess.sweep.getIntersectData_ = function (tess, isect, orgUp, dstUp, orgLo, dstLo) {
        // TODO(bckenny): called for every intersection event, should these be from a pool?
        // TODO(bckenny): better way to init these?
        var weights = [0, 0, 0, 0];
        var data = [
            orgUp.data,
            dstUp.data,
            orgLo.data,
            dstLo.data
        ];
        // TODO(bckenny): it appears isect is a reappropriated vertex, so does need to be zeroed.
        // double check this.
        isect.coords[0] = isect.coords[1] = isect.coords[2] = 0;
        // TODO(bckenny): see note in libtess.sweep.vertexWeights_ for explanation of weightIndex. fix?
        libtess.sweep.vertexWeights_(isect, orgUp, dstUp, weights, 0);
        libtess.sweep.vertexWeights_(isect, orgLo, dstLo, weights, 2);
        libtess.sweep.callCombine_(tess, isect, data, weights, true);
    };
    /**
     * Check the upper and lower edge of regUp, to make sure that the
     * eUp.org is above eLo, or eLo.org is below eUp (depending on which
     * origin is leftmost).
     *
     * The main purpose is to splice right-going edges with the same
     * dest vertex and nearly identical slopes (ie. we can't distinguish
     * the slopes numerically). However the splicing can also help us
     * to recover from numerical errors. For example, suppose at one
     * point we checked eUp and eLo, and decided that eUp.org is barely
     * above eLo. Then later, we split eLo into two edges (eg. from
     * a splice operation like this one). This can change the result of
     * our test so that now eUp.org is incident to eLo, or barely below it.
     * We must correct this condition to maintain the dictionary invariants.
     *
     * One possibility is to check these edges for intersection again
     * (i.e. checkForIntersect). This is what we do if possible. However
     * checkForIntersect requires that tess.event lies between eUp and eLo,
     * so that it has something to fall back on when the intersection
     * calculation gives us an unusable answer. So, for those cases where
     * we can't check for intersection, this routine fixes the problem
     * by just splicing the offending vertex into the other edge.
     * This is a guaranteed solution, no matter how degenerate things get.
     * Basically this is a combinatorial solution to a numerical problem.
     *
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} regUp [description].
     * @return {boolean} [description].
     */
    libtess.sweep.checkForRightSplice_ = function (tess, regUp) {
        // TODO(bckenny): fully learn how these two checks work
        var regLo = regUp.regionBelow();
        var eUp = regUp.eUp;
        var eLo = regLo.eUp;
        if (libtess.geom.vertLeq(eUp.org, eLo.org)) {
            if (libtess.geom.edgeSign(eLo.dst(), eUp.org, eLo.org) > 0) {
                return false;
            }
            // eUp.org appears to be below eLo
            if (!libtess.geom.vertEq(eUp.org, eLo.org)) {
                // Splice eUp.org into eLo
                libtess.mesh.splitEdge(eLo.sym);
                libtess.mesh.meshSplice(eUp, eLo.oPrev());
                regUp.dirty = regLo.dirty = true;
            }
            else if (eUp.org !== eLo.org) {
                // merge the two vertices, discarding eUp.org
                tess.pq.remove(eUp.org.pqHandle);
                libtess.sweep.spliceMergeVertices_(tess, eLo.oPrev(), eUp);
            }
        }
        else {
            if (libtess.geom.edgeSign(eUp.dst(), eLo.org, eUp.org) < 0) {
                return false;
            }
            // eLo.org appears to be above eUp, so splice eLo.org into eUp
            regUp.regionAbove().dirty = regUp.dirty = true;
            libtess.mesh.splitEdge(eUp.sym);
            libtess.mesh.meshSplice(eLo.oPrev(), eUp);
        }
        return true;
    };
    /**
     * Check the upper and lower edge of regUp to make sure that the
     * eUp.dst() is above eLo, or eLo.dst() is below eUp (depending on which
     * destination is rightmost).
     *
     * Theoretically, this should always be true. However, splitting an edge
     * into two pieces can change the results of previous tests. For example,
     * suppose at one point we checked eUp and eLo, and decided that eUp.dst()
     * is barely above eLo. Then later, we split eLo into two edges (eg. from
     * a splice operation like this one). This can change the result of
     * the test so that now eUp.dst() is incident to eLo, or barely below it.
     * We must correct this condition to maintain the dictionary invariants
     * (otherwise new edges might get inserted in the wrong place in the
     * dictionary, and bad stuff will happen).
     *
     * We fix the problem by just splicing the offending vertex into the
     * other edge.
     *
     * @private
     * @param {libtess.GluTesselator} tess description].
     * @param {libtess.ActiveRegion} regUp [description].
     * @return {boolean} [description].
     */
    libtess.sweep.checkForLeftSplice_ = function (tess, regUp) {
        var regLo = regUp.regionBelow();
        var eUp = regUp.eUp;
        var eLo = regLo.eUp;
        var e;
        if (libtess.geom.vertLeq(eUp.dst(), eLo.dst())) {
            if (libtess.geom.edgeSign(eUp.dst(), eLo.dst(), eUp.org) < 0) {
                return false;
            }
            // eLo.dst() is above eUp, so splice eLo.dst() into eUp
            regUp.regionAbove().dirty = regUp.dirty = true;
            e = libtess.mesh.splitEdge(eUp);
            libtess.mesh.meshSplice(eLo.sym, e);
            e.lFace.inside = regUp.inside;
        }
        else {
            if (libtess.geom.edgeSign(eLo.dst(), eUp.dst(), eLo.org) > 0) {
                return false;
            }
            // eUp.dst() is below eLo, so splice eUp.dst() into eLo
            regUp.dirty = regLo.dirty = true;
            e = libtess.mesh.splitEdge(eLo);
            libtess.mesh.meshSplice(eUp.lNext, eLo.sym);
            e.rFace().inside = regUp.inside;
        }
        return true;
    };
    /**
     * Check the upper and lower edges of the given region to see if
     * they intersect. If so, create the intersection and add it
     * to the data structures.
     *
     * Returns true if adding the new intersection resulted in a recursive
     * call to addRightEdges_(); in this case all "dirty" regions have been
     * checked for intersections, and possibly regUp has been deleted.
     *
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} regUp [description].
     * @return {boolean} [description].
     */
    libtess.sweep.checkForIntersect_ = function (tess, regUp) {
        var regLo = regUp.regionBelow();
        var eUp = regUp.eUp;
        var eLo = regLo.eUp;
        var orgUp = eUp.org;
        var orgLo = eLo.org;
        var dstUp = eUp.dst();
        var dstLo = eLo.dst();
        var isect = new libtess.GluVertex();
        if (orgUp === orgLo) {
            // right endpoints are the same
            return false;
        }
        var tMinUp = Math.min(orgUp.t, dstUp.t);
        var tMaxLo = Math.max(orgLo.t, dstLo.t);
        if (tMinUp > tMaxLo) {
            // t ranges do not overlap
            return false;
        }
        if (libtess.geom.vertLeq(orgUp, orgLo)) {
            if (libtess.geom.edgeSign(dstLo, orgUp, orgLo) > 0) {
                return false;
            }
        }
        else {
            if (libtess.geom.edgeSign(dstUp, orgLo, orgUp) < 0) {
                return false;
            }
        }
        // At this point the edges intersect, at least marginally
        libtess.geom.edgeIntersect(dstUp, orgUp, dstLo, orgLo, isect);
        // The following properties are guaranteed:
        if (libtess.geom.vertLeq(isect, tess.event)) {
            /* The intersection point lies slightly to the left of the sweep line,
             * so move it until it's slightly to the right of the sweep line.
             * (If we had perfect numerical precision, this would never happen
             * in the first place). The easiest and safest thing to do is
             * replace the intersection by tess.event.
             */
            isect.s = tess.event.s;
            isect.t = tess.event.t;
        }
        // TODO(bckenny): try to find test54.d
        /* Similarly, if the computed intersection lies to the right of the
         * rightmost origin (which should rarely happen), it can cause
         * unbelievable inefficiency on sufficiently degenerate inputs.
         * (If you have the test program, try running test54.d with the
         * "X zoom" option turned on).
         */
        var orgMin = libtess.geom.vertLeq(orgUp, orgLo) ? orgUp : orgLo;
        if (libtess.geom.vertLeq(orgMin, isect)) {
            isect.s = orgMin.s;
            isect.t = orgMin.t;
        }
        if (libtess.geom.vertEq(isect, orgUp) || libtess.geom.vertEq(isect, orgLo)) {
            // Easy case -- intersection at one of the right endpoints
            libtess.sweep.checkForRightSplice_(tess, regUp);
            return false;
        }
        // TODO(bckenny): clean this up; length is distracting
        if ((!libtess.geom.vertEq(dstUp, tess.event) &&
            libtess.geom.edgeSign(dstUp, tess.event, isect) >= 0) ||
            (!libtess.geom.vertEq(dstLo, tess.event) &&
                libtess.geom.edgeSign(dstLo, tess.event, isect) <= 0)) {
            /* Very unusual -- the new upper or lower edge would pass on the
             * wrong side of the sweep event, or through it. This can happen
             * due to very small numerical errors in the intersection calculation.
             */
            if (dstLo === tess.event) {
                // Splice dstLo into eUp, and process the new region(s)
                libtess.mesh.splitEdge(eUp.sym);
                libtess.mesh.meshSplice(eLo.sym, eUp);
                regUp = libtess.sweep.topLeftRegion_(regUp);
                eUp = regUp.regionBelow().eUp;
                libtess.sweep.finishLeftRegions_(tess, regUp.regionBelow(), regLo);
                libtess.sweep.addRightEdges_(tess, regUp, eUp.oPrev(), eUp, eUp, true);
                return true;
            }
            if (dstUp === tess.event) {
                // Splice dstUp into eLo, and process the new region(s)
                libtess.mesh.splitEdge(eLo.sym);
                libtess.mesh.meshSplice(eUp.lNext, eLo.oPrev());
                regLo = regUp;
                regUp = libtess.sweep.topRightRegion_(regUp);
                var e = regUp.regionBelow().eUp.rPrev();
                regLo.eUp = eLo.oPrev();
                eLo = libtess.sweep.finishLeftRegions_(tess, regLo, null);
                libtess.sweep.addRightEdges_(tess, regUp, eLo.oNext, eUp.rPrev(), e, true);
                return true;
            }
            /* Special case: called from connectRightVertex. If either
             * edge passes on the wrong side of tess.event, split it
             * (and wait for connectRightVertex to splice it appropriately).
             */
            if (libtess.geom.edgeSign(dstUp, tess.event, isect) >= 0) {
                regUp.regionAbove().dirty = regUp.dirty = true;
                libtess.mesh.splitEdge(eUp.sym);
                eUp.org.s = tess.event.s;
                eUp.org.t = tess.event.t;
            }
            if (libtess.geom.edgeSign(dstLo, tess.event, isect) <= 0) {
                regUp.dirty = regLo.dirty = true;
                libtess.mesh.splitEdge(eLo.sym);
                eLo.org.s = tess.event.s;
                eLo.org.t = tess.event.t;
            }
            // leave the rest for connectRightVertex
            return false;
        }
        /* General case -- split both edges, splice into new vertex.
         * When we do the splice operation, the order of the arguments is
         * arbitrary as far as correctness goes. However, when the operation
         * creates a new face, the work done is proportional to the size of
         * the new face. We expect the faces in the processed part of
         * the mesh (ie. eUp.lFace) to be smaller than the faces in the
         * unprocessed original contours (which will be eLo.oPrev.lFace).
         */
        libtess.mesh.splitEdge(eUp.sym);
        libtess.mesh.splitEdge(eLo.sym);
        libtess.mesh.meshSplice(eLo.oPrev(), eUp);
        eUp.org.s = isect.s;
        eUp.org.t = isect.t;
        eUp.org.pqHandle = tess.pq.insert(eUp.org);
        libtess.sweep.getIntersectData_(tess, eUp.org, orgUp, dstUp, orgLo, dstLo);
        regUp.regionAbove().dirty = regUp.dirty = regLo.dirty = true;
        return false;
    };
    /**
     * When the upper or lower edge of any region changes, the region is
     * marked "dirty". This routine walks through all the dirty regions
     * and makes sure that the dictionary invariants are satisfied
     * (see the comments at the beginning of this file). Of course,
     * new dirty regions can be created as we make changes to restore
     * the invariants.
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} regUp [description].
     */
    libtess.sweep.walkDirtyRegions_ = function (tess, regUp) {
        var regLo = regUp.regionBelow();
        for (;;) {
            // Find the lowest dirty region (we walk from the bottom up).
            while (regLo.dirty) {
                regUp = regLo;
                regLo = regLo.regionBelow();
            }
            if (!regUp.dirty) {
                regLo = regUp;
                regUp = regUp.regionAbove();
                if (regUp === null || !regUp.dirty) {
                    // We've walked all the dirty regions
                    return;
                }
            }
            regUp.dirty = false;
            var eUp = regUp.eUp;
            var eLo = regLo.eUp;
            if (eUp.dst() !== eLo.dst()) {
                // Check that the edge ordering is obeyed at the dst vertices.
                if (libtess.sweep.checkForLeftSplice_(tess, regUp)) {
                    // If the upper or lower edge was marked fixUpperEdge, then
                    // we no longer need it (since these edges are needed only for
                    // vertices which otherwise have no right-going edges).
                    if (regLo.fixUpperEdge) {
                        libtess.sweep.deleteRegion_(tess, regLo);
                        libtess.mesh.deleteEdge(eLo);
                        regLo = regUp.regionBelow();
                        eLo = regLo.eUp;
                    }
                    else if (regUp.fixUpperEdge) {
                        libtess.sweep.deleteRegion_(tess, regUp);
                        libtess.mesh.deleteEdge(eUp);
                        regUp = regLo.regionAbove();
                        eUp = regUp.eUp;
                    }
                }
            }
            if (eUp.org !== eLo.org) {
                if (eUp.dst() !== eLo.dst() && !regUp.fixUpperEdge &&
                    !regLo.fixUpperEdge &&
                    (eUp.dst() === tess.event || eLo.dst() === tess.event)) {
                    /* When all else fails in checkForIntersect(), it uses tess.event
                     * as the intersection location. To make this possible, it requires
                     * that tess.event lie between the upper and lower edges, and also
                     * that neither of these is marked fixUpperEdge (since in the worst
                     * case it might splice one of these edges into tess.event, and
                     * violate the invariant that fixable edges are the only right-going
                     * edge from their associated vertex).
                     */
                    if (libtess.sweep.checkForIntersect_(tess, regUp)) {
                        // walkDirtyRegions() was called recursively; we're done
                        return;
                    }
                }
                else {
                    // Even though we can't use checkForIntersect(), the org vertices
                    // may violate the dictionary edge ordering. Check and correct this.
                    libtess.sweep.checkForRightSplice_(tess, regUp);
                }
            }
            if (eUp.org === eLo.org && eUp.dst() === eLo.dst()) {
                // A degenerate loop consisting of only two edges -- delete it.
                libtess.sweep.addWinding_(eLo, eUp);
                libtess.sweep.deleteRegion_(tess, regUp);
                libtess.mesh.deleteEdge(eUp);
                regUp = regLo.regionAbove();
            }
        }
    };
    /**
     * Purpose: connect a "right" vertex vEvent (one where all edges go left)
     * to the unprocessed portion of the mesh. Since there are no right-going
     * edges, two regions (one above vEvent and one below) are being merged
     * into one. regUp is the upper of these two regions.
     *
     * There are two reasons for doing this (adding a right-going edge):
     *  - if the two regions being merged are "inside", we must add an edge
     *    to keep them separated (the combined region would not be monotone).
     *  - in any case, we must leave some record of vEvent in the dictionary,
     *    so that we can merge vEvent with features that we have not seen yet.
     *    For example, maybe there is a vertical edge which passes just to
     *    the right of vEvent; we would like to splice vEvent into this edge.
     *
     * However, we don't want to connect vEvent to just any vertex. We don't
     * want the new edge to cross any other edges; otherwise we will create
     * intersection vertices even when the input data had no self-intersections.
     * (This is a bad thing; if the user's input data has no intersections,
     * we don't want to generate any false intersections ourselves.)
     *
     * Our eventual goal is to connect vEvent to the leftmost unprocessed
     * vertex of the combined region (the union of regUp and regLo).
     * But because of unseen vertices with all right-going edges, and also
     * new vertices which may be created by edge intersections, we don't
     * know where that leftmost unprocessed vertex is. In the meantime, we
     * connect vEvent to the closest vertex of either chain, and mark the region
     * as "fixUpperEdge". This flag says to delete and reconnect this edge
     * to the next processed vertex on the boundary of the combined region.
     * Quite possibly the vertex we connected to will turn out to be the
     * closest one, in which case we won't need to make any changes.
     *
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.ActiveRegion} regUp [description].
     * @param {libtess.GluHalfEdge} eBottomLeft [description].
     */
    libtess.sweep.connectRightVertex_ = function (tess, regUp, eBottomLeft) {
        var eTopLeft = eBottomLeft.oNext;
        var regLo = regUp.regionBelow();
        var eUp = regUp.eUp;
        var eLo = regLo.eUp;
        var degenerate = false;
        if (eUp.dst() !== eLo.dst()) {
            libtess.sweep.checkForIntersect_(tess, regUp);
        }
        // Possible new degeneracies: upper or lower edge of regUp may pass
        // through vEvent, or may coincide with new intersection vertex
        if (libtess.geom.vertEq(eUp.org, tess.event)) {
            libtess.mesh.meshSplice(eTopLeft.oPrev(), eUp);
            regUp = libtess.sweep.topLeftRegion_(regUp);
            eTopLeft = regUp.regionBelow().eUp;
            libtess.sweep.finishLeftRegions_(tess, regUp.regionBelow(), regLo);
            degenerate = true;
        }
        if (libtess.geom.vertEq(eLo.org, tess.event)) {
            libtess.mesh.meshSplice(eBottomLeft, eLo.oPrev());
            eBottomLeft = libtess.sweep.finishLeftRegions_(tess, regLo, null);
            degenerate = true;
        }
        if (degenerate) {
            libtess.sweep.addRightEdges_(tess, regUp, eBottomLeft.oNext, eTopLeft, eTopLeft, true);
            return;
        }
        // Non-degenerate situation -- need to add a temporary, fixable edge.
        // Connect to the closer of eLo.org, eUp.org.
        var eNew;
        if (libtess.geom.vertLeq(eLo.org, eUp.org)) {
            eNew = eLo.oPrev();
        }
        else {
            eNew = eUp;
        }
        eNew = libtess.mesh.connect(eBottomLeft.lPrev(), eNew);
        // Prevent cleanup, otherwise eNew might disappear before we've even
        // had a chance to mark it as a temporary edge.
        libtess.sweep.addRightEdges_(tess, regUp, eNew, eNew.oNext, eNew.oNext, false);
        eNew.sym.activeRegion.fixUpperEdge = true;
        libtess.sweep.walkDirtyRegions_(tess, regUp);
    };
    /**
     * The event vertex lies exacty on an already-processed edge or vertex.
     * Adding the new vertex involves splicing it into the already-processed
     * part of the mesh.
     * @private
     * @param {!libtess.GluTesselator} tess
     * @param {libtess.ActiveRegion} regUp [description].
     * @param {libtess.GluVertex} vEvent [description].
     */
    libtess.sweep.connectLeftDegenerate_ = function (tess, regUp, vEvent) {
        var e = regUp.eUp;
        /* istanbul ignore if */
        if (libtess.geom.vertEq(e.org, vEvent)) {
            // NOTE(bckenny): this code is unreachable but remains for a hypothetical
            // future extension of libtess. See docs on libtess.sweep.TOLERANCE_NONZERO_
            // for more information. Conditional on TOLERANCE_NONZERO_ to help Closure
            // Compiler eliminate dead code.
            // e.org is an unprocessed vertex - just combine them, and wait
            // for e.org to be pulled from the queue
            if (libtess.sweep.TOLERANCE_NONZERO_) {
                libtess.sweep.spliceMergeVertices_(tess, e, vEvent.anEdge);
            }
            return;
        }
        if (!libtess.geom.vertEq(e.dst(), vEvent)) {
            // General case -- splice vEvent into edge e which passes through it
            libtess.mesh.splitEdge(e.sym);
            if (regUp.fixUpperEdge) {
                // This edge was fixable -- delete unused portion of original edge
                libtess.mesh.deleteEdge(e.oNext);
                regUp.fixUpperEdge = false;
            }
            libtess.mesh.meshSplice(vEvent.anEdge, e);
            // recurse
            libtess.sweep.sweepEvent_(tess, vEvent);
            return;
        }
        // NOTE(bckenny): this code is unreachable but remains for a hypothetical
        // future extension of libtess. See docs on libtess.sweep.TOLERANCE_NONZERO_
        // for more information. Conditional on TOLERANCE_NONZERO_ to help Closure
        // Compiler eliminate dead code.
        // vEvent coincides with e.dst(), which has already been processed.
        // Splice in the additional right-going edges.
        /* istanbul ignore next */
        /* istanbul ignore next */
        if (libtess.sweep.TOLERANCE_NONZERO_) {
            regUp = libtess.sweep.topRightRegion_(regUp);
            var reg = regUp.regionBelow();
            var eTopRight = reg.eUp.sym;
            var eTopLeft = eTopRight.oNext;
            var eLast = eTopLeft;
            if (reg.fixUpperEdge) {
                // Here e.dst() has only a single fixable edge going right.
                // We can delete it since now we have some real right-going edges.
                // there are some left edges too
                libtess.sweep.deleteRegion_(tess, reg); // TODO(bckenny): something to null?
                libtess.mesh.deleteEdge(eTopRight);
                eTopRight = eTopLeft.oPrev();
            }
            libtess.mesh.meshSplice(vEvent.anEdge, eTopRight);
            if (!libtess.geom.edgeGoesLeft(eTopLeft)) {
                // e.dst() had no left-going edges -- indicate this to addRightEdges()
                eTopLeft = null;
            }
            libtess.sweep.addRightEdges_(tess, regUp, eTopRight.oNext, eLast, eTopLeft, true);
        }
    };
    /**
     * Connect a "left" vertex (one where both edges go right)
     * to the processed portion of the mesh. Let R be the active region
     * containing vEvent, and let U and L be the upper and lower edge
     * chains of R. There are two possibilities:
     *
     * - the normal case: split R into two regions, by connecting vEvent to
     *   the rightmost vertex of U or L lying to the left of the sweep line
     *
     * - the degenerate case: if vEvent is close enough to U or L, we
     *   merge vEvent into that edge chain. The subcases are:
     *  - merging with the rightmost vertex of U or L
     *  - merging with the active edge of U or L
     *  - merging with an already-processed portion of U or L
     *
     * @private
     * @param {libtess.GluTesselator} tess   [description].
     * @param {libtess.GluVertex} vEvent [description].
     */
    libtess.sweep.connectLeftVertex_ = function (tess, vEvent) {
        // TODO(bckenny): tmp only used for sweep. better to keep tmp across calls?
        var tmp = new libtess.ActiveRegion();
        // NOTE(bckenny): this was commented out in the original
        // libtess.assert(vEvent.anEdge.oNext.oNext === vEvent.anEdge);
        // Get a pointer to the active region containing vEvent
        tmp.eUp = vEvent.anEdge.sym;
        var regUp = tess.dict.search(tmp).getKey();
        var regLo = regUp.regionBelow();
        var eUp = regUp.eUp;
        var eLo = regLo.eUp;
        // try merging with U or L first
        if (libtess.geom.edgeSign(eUp.dst(), vEvent, eUp.org) === 0) {
            libtess.sweep.connectLeftDegenerate_(tess, regUp, vEvent);
            return;
        }
        // Connect vEvent to rightmost processed vertex of either chain.
        // e.dst() is the vertex that we will connect to vEvent.
        var reg = libtess.geom.vertLeq(eLo.dst(), eUp.dst()) ? regUp : regLo;
        var eNew;
        if (regUp.inside || reg.fixUpperEdge) {
            if (reg === regUp) {
                eNew = libtess.mesh.connect(vEvent.anEdge.sym, eUp.lNext);
            }
            else {
                var tempHalfEdge = libtess.mesh.connect(eLo.dNext(), vEvent.anEdge);
                eNew = tempHalfEdge.sym;
            }
            if (reg.fixUpperEdge) {
                libtess.sweep.fixUpperEdge_(reg, eNew);
            }
            else {
                libtess.sweep.computeWinding_(tess, libtess.sweep.addRegionBelow_(tess, regUp, eNew));
            }
            libtess.sweep.sweepEvent_(tess, vEvent);
        }
        else {
            // The new vertex is in a region which does not belong to the polygon.
            // We don''t need to connect this vertex to the rest of the mesh.
            libtess.sweep.addRightEdges_(tess, regUp, vEvent.anEdge, vEvent.anEdge, null, true);
        }
    };
    /**
     * Does everything necessary when the sweep line crosses a vertex.
     * Updates the mesh and the edge dictionary.
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {libtess.GluVertex} vEvent [description].
     */
    libtess.sweep.sweepEvent_ = function (tess, vEvent) {
        tess.event = vEvent; // for access in edgeLeq_ // TODO(bckenny): wuh?
        /* Check if this vertex is the right endpoint of an edge that is
         * already in the dictionary.  In this case we don't need to waste
         * time searching for the location to insert new edges.
         */
        var e = vEvent.anEdge;
        while (e.activeRegion === null) {
            e = e.oNext;
            if (e === vEvent.anEdge) {
                // All edges go right -- not incident to any processed edges
                libtess.sweep.connectLeftVertex_(tess, vEvent);
                return;
            }
        }
        /* Processing consists of two phases: first we "finish" all the
         * active regions where both the upper and lower edges terminate
         * at vEvent (ie. vEvent is closing off these regions).
         * We mark these faces "inside" or "outside" the polygon according
         * to their winding number, and delete the edges from the dictionary.
         * This takes care of all the left-going edges from vEvent.
         */
        var regUp = libtess.sweep.topLeftRegion_(e.activeRegion);
        var reg = regUp.regionBelow();
        var eTopLeft = reg.eUp;
        var eBottomLeft = libtess.sweep.finishLeftRegions_(tess, reg, null);
        /* Next we process all the right-going edges from vEvent. This
         * involves adding the edges to the dictionary, and creating the
         * associated "active regions" which record information about the
         * regions between adjacent dictionary edges.
         */
        if (eBottomLeft.oNext === eTopLeft) {
            // No right-going edges -- add a temporary "fixable" edge
            libtess.sweep.connectRightVertex_(tess, regUp, eBottomLeft);
        }
        else {
            libtess.sweep.addRightEdges_(tess, regUp, eBottomLeft.oNext, eTopLeft, eTopLeft, true);
        }
    };
    /**
     * We add two sentinel edges above and below all other edges,
     * to avoid special cases at the top and bottom.
     * @private
     * @param {libtess.GluTesselator} tess [description].
     * @param {number} t [description].
     */
    libtess.sweep.addSentinel_ = function (tess, t) {
        var reg = new libtess.ActiveRegion();
        var e = libtess.mesh.makeEdge(tess.mesh);
        e.org.s = libtess.sweep.SENTINEL_COORD_;
        e.org.t = t;
        e.dst().s = -libtess.sweep.SENTINEL_COORD_;
        e.dst().t = t;
        tess.event = e.dst(); //initialize it
        reg.eUp = e;
        reg.windingNumber = 0;
        reg.inside = false;
        reg.fixUpperEdge = false;
        reg.sentinel = true;
        reg.dirty = false;
        reg.nodeUp = tess.dict.insert(reg);
    };
    /**
     * We maintain an ordering of edge intersections with the sweep line.
     * This order is maintained in a dynamic dictionary.
     * @private
     * @param {libtess.GluTesselator} tess [description].
     */
    libtess.sweep.initEdgeDict_ = function (tess) {
        tess.dict = new libtess.Dict(tess, libtess.sweep.edgeLeq_);
        libtess.sweep.addSentinel_(tess, -libtess.sweep.SENTINEL_COORD_);
        libtess.sweep.addSentinel_(tess, libtess.sweep.SENTINEL_COORD_);
    };
    /**
     * [doneEdgeDict_ description]
     * @private
     * @param {libtess.GluTesselator} tess [description].
     */
    libtess.sweep.doneEdgeDict_ = function (tess) {
        // NOTE(bckenny): fixedEdges is only used in the assert below, so ignore so
        // when asserts are removed jshint won't error.
        /* jshint unused:false */
        var fixedEdges = 0;
        var reg;
        while ((reg = tess.dict.getMin().getKey()) !== null) {
            // At the end of all processing, the dictionary should contain
            // only the two sentinel edges, plus at most one "fixable" edge
            // created by connectRightVertex().
            if (!reg.sentinel) {
            }
            libtess.sweep.deleteRegion_(tess, reg);
        }
        // NOTE(bckenny): see tess.dict.deleteDict_() for old delete dict function
        tess.dict = null;
    };
    /**
     * Remove zero-length edges, and contours with fewer than 3 vertices.
     * @private
     * @param {libtess.GluTesselator} tess [description].
     */
    libtess.sweep.removeDegenerateEdges_ = function (tess) {
        var eHead = tess.mesh.eHead;
        var eNext;
        for (var e = eHead.next; e !== eHead; e = eNext) {
            eNext = e.next;
            var eLNext = e.lNext;
            if (libtess.geom.vertEq(e.org, e.dst()) && e.lNext.lNext !== e) {
                // Zero-length edge, contour has at least 3 edges
                libtess.sweep.spliceMergeVertices_(tess, eLNext, e); // deletes e.org
                libtess.mesh.deleteEdge(e); // e is a self-loop TODO(bckenny): does this comment really apply here?
                e = eLNext;
                eLNext = e.lNext;
            }
            if (eLNext.lNext === e) {
                // Degenerate contour (one or two edges)
                if (eLNext !== e) {
                    if (eLNext === eNext || eLNext === eNext.sym) {
                        eNext = eNext.next;
                    }
                    libtess.mesh.deleteEdge(eLNext);
                }
                if (e === eNext || e === eNext.sym) {
                    eNext = eNext.next;
                }
                libtess.mesh.deleteEdge(e);
            }
        }
    };
    /**
     * Construct priority queue and insert all vertices into it, which determines
     * the order in which vertices cross the sweep line.
     * @private
     * @param {libtess.GluTesselator} tess [description].
     */
    libtess.sweep.initPriorityQ_ = function (tess) {
        var pq = new libtess.PriorityQ();
        tess.pq = pq;
        var vHead = tess.mesh.vHead;
        var v;
        for (v = vHead.next; v !== vHead; v = v.next) {
            v.pqHandle = pq.insert(v);
        }
        pq.init();
    };
    /**
     * [donePriorityQ_ description]
     * @private
     * @param {libtess.GluTesselator} tess [description].
     */
    libtess.sweep.donePriorityQ_ = function (tess) {
        // TODO(bckenny): probably don't need deleteQ. check that function for comment
        tess.pq.deleteQ();
        tess.pq = null;
    };
    /**
     * Delete any degenerate faces with only two edges. walkDirtyRegions()
     * will catch almost all of these, but it won't catch degenerate faces
     * produced by splice operations on already-processed edges.
     * The two places this can happen are in finishLeftRegions(), when
     * we splice in a "temporary" edge produced by connectRightVertex(),
     * and in checkForLeftSplice(), where we splice already-processed
     * edges to ensure that our dictionary invariants are not violated
     * by numerical errors.
     *
     * In both these cases it is *very* dangerous to delete the offending
     * edge at the time, since one of the routines further up the stack
     * will sometimes be keeping a pointer to that edge.
     *
     * @private
     * @param {libtess.GluMesh} mesh [description].
     */
    libtess.sweep.removeDegenerateFaces_ = function (mesh) {
        var fNext;
        for (var f = mesh.fHead.next; f !== mesh.fHead; f = fNext) {
            fNext = f.next;
            var e = f.anEdge;
            if (e.lNext.lNext === e) {
                // A face with only two edges
                libtess.sweep.addWinding_(e.oNext, e);
                libtess.mesh.deleteEdge(e);
            }
        }
    };
    /* global libtess */
    /** @const */
    libtess.tessmono = {};
    /**
     * Tessellates a monotone region (what else would it do??). The region must
     * consist of a single loop of half-edges (see mesh.js) oriented CCW. "Monotone"
     * in this case means that any vertical line intersects the interior of the
     * region in a single interval.
     *
     * Tessellation consists of adding interior edges (actually pairs of
     * half-edges), to split the region into non-overlapping triangles.
     * @private
     * @param {!libtess.GluFace} face
     */
    libtess.tessmono.tessellateMonoRegion_ = function (face) {
        /* The basic idea is explained in Preparata and Shamos (which I don't
         * have handy right now), although their implementation is more
         * complicated than this one. The are two edge chains, an upper chain
         * and a lower chain. We process all vertices from both chains in order,
         * from right to left.
         *
         * The algorithm ensures that the following invariant holds after each
         * vertex is processed: the untessellated region consists of two
         * chains, where one chain (say the upper) is a single edge, and
         * the other chain is concave. The left vertex of the single edge
         * is always to the left of all vertices in the concave chain.
         *
         * Each step consists of adding the rightmost unprocessed vertex to one
         * of the two chains, and forming a fan of triangles from the rightmost
         * of two chain endpoints. Determining whether we can add each triangle
         * to the fan is a simple orientation test. By making the fan as large
         * as possible, we restore the invariant (check it yourself).
         *
         * All edges are oriented CCW around the boundary of the region.
         * First, find the half-edge whose origin vertex is rightmost.
         * Since the sweep goes from left to right, face.anEdge should
         * be close to the edge we want.
         */
        var up = face.anEdge;
        for (; libtess.geom.vertLeq(up.dst(), up.org); up = up.lPrev()) { }
        for (; libtess.geom.vertLeq(up.org, up.dst()); up = up.lNext) { }
        var lo = up.lPrev();
        var tempHalfEdge;
        while (up.lNext !== lo) {
            if (libtess.geom.vertLeq(up.dst(), lo.org)) {
                // up.dst() is on the left. It is safe to form triangles from lo.org.
                // The edgeGoesLeft test guarantees progress even when some triangles
                // are CW, given that the upper and lower chains are truly monotone.
                while (lo.lNext !== up && (libtess.geom.edgeGoesLeft(lo.lNext) ||
                    libtess.geom.edgeSign(lo.org, lo.dst(), lo.lNext.dst()) <= 0)) {
                    tempHalfEdge = libtess.mesh.connect(lo.lNext, lo);
                    lo = tempHalfEdge.sym;
                }
                lo = lo.lPrev();
            }
            else {
                // lo.org is on the left. We can make CCW triangles from up.dst().
                while (lo.lNext !== up && (libtess.geom.edgeGoesRight(up.lPrev()) ||
                    libtess.geom.edgeSign(up.dst(), up.org, up.lPrev().org) >= 0)) {
                    tempHalfEdge = libtess.mesh.connect(up, up.lPrev());
                    up = tempHalfEdge.sym;
                }
                up = up.lNext;
            }
        }
        // Now lo.org == up.dst() == the leftmost vertex. The remaining region
        // can be tessellated in a fan from this leftmost vertex.
        while (lo.lNext.lNext !== up) {
            tempHalfEdge = libtess.mesh.connect(lo.lNext, lo);
            lo = tempHalfEdge.sym;
        }
    };
    /**
     * Tessellates each region of the mesh which is marked "inside" the polygon.
     * Each such region must be monotone.
     * @param {!libtess.GluMesh} mesh
     */
    libtess.tessmono.tessellateInterior = function (mesh) {
        var next;
        for (var f = mesh.fHead.next; f !== mesh.fHead; f = next) {
            // Make sure we don't try to tessellate the new triangles.
            next = f.next;
            if (f.inside) {
                libtess.tessmono.tessellateMonoRegion_(f);
            }
        }
    };
    /**
     * Zaps (i.e. sets to null) all faces which are not marked "inside" the polygon.
     * Since further mesh operations on null faces are not allowed, the main purpose
     * is to clean up the mesh so that exterior loops are not represented in the
     * data structure.
     * @param {!libtess.GluMesh} mesh
     */
    libtess.tessmono.discardExterior = function (mesh) {
        var next;
        for (var f = mesh.fHead.next; f !== mesh.fHead; f = next) {
            // Since f will be destroyed, save its next pointer.
            next = f.next;
            if (!f.inside) {
                libtess.mesh.zapFace(f);
            }
        }
    };
    /**
     * Resets the winding numbers on all edges so that regions marked "inside" the
     * polygon have a winding number of "value", and regions outside have a winding
     * number of 0.
     *
     * If keepOnlyBoundary is true, it also deletes all edges which do not separate
     * an interior region from an exterior one.
     *
     * @param {!libtess.GluMesh} mesh
     * @param {number} value
     * @param {boolean} keepOnlyBoundary
     */
    libtess.tessmono.setWindingNumber = function (mesh, value, keepOnlyBoundary) {
        var eNext;
        for (var e = mesh.eHead.next; e !== mesh.eHead; e = eNext) {
            eNext = e.next;
            if (e.rFace().inside !== e.lFace.inside) {
                // This is a boundary edge (one side is interior, one is exterior).
                e.winding = (e.lFace.inside) ? value : -value;
            }
            else {
                // Both regions are interior, or both are exterior.
                if (!keepOnlyBoundary) {
                    e.winding = 0;
                }
                else {
                    libtess.mesh.deleteEdge(e);
                }
            }
        }
    };
    /* global libtess */
    /**
     * A list of edges crossing the sweep line, sorted from top to bottom.
     * Implementation is a doubly-linked list, sorted by the injected edgeLeq
     * comparator function. Here it is a simple ordering, but see libtess.sweep for
     * the list of invariants on the edge dictionary this ordering creates.
     * @constructor
     * @struct
     * @param {!libtess.GluTesselator} frame
     * @param {function(!libtess.GluTesselator, !libtess.ActiveRegion, !libtess.ActiveRegion): boolean} leq
     */
    libtess.Dict = function (frame, leq) {
        /**
         * The head of the doubly-linked DictNode list. At creation time, links back
         * and forward only to itself.
         * @private {!libtess.DictNode}
         */
        this.head_ = new libtess.DictNode();
        /**
         * The GluTesselator used as the frame for edge/event comparisons.
         * @private {!libtess.GluTesselator}
         */
        this.frame_ = frame;
        /**
         * Comparison function to maintain the invariants of the Dict. See
         * libtess.sweep.edgeLeq_ for source.
         * @private
         * @type {function(!libtess.GluTesselator, !libtess.ActiveRegion, !libtess.ActiveRegion): boolean}
         */
        this.leq_ = leq;
    };
    /* istanbul ignore next */
    /**
     * Formerly used to delete the dict.
     * NOTE(bckenny): No longer called but left for memFree documentation. Nulled at
     * former callsite instead (sweep.doneEdgeDict_)
     * @private
     */
    libtess.Dict.prototype.deleteDict_ = function () {
        // for (var node = this.head_.next; node !== this.head_; node = node.next) {
        //   memFree(node);
        // }
        // memFree(dict);
    };
    /**
     * Insert the supplied key into the edge list and return its new node.
     * @param {libtess.DictNode} node
     * @param {!libtess.ActiveRegion} key
     * @return {!libtess.DictNode}
     */
    libtess.Dict.prototype.insertBefore = function (node, key) {
        do {
            node = node.prev;
        } while (node.key !== null && !this.leq_(this.frame_, node.key, key));
        // insert the new node and update the surrounding nodes to point to it
        var newNode = new libtess.DictNode(key, node.next, node);
        node.next.prev = newNode;
        node.next = newNode;
        return newNode;
    };
    /**
     * Insert key into the dict and return the new node that contains it.
     * @param {!libtess.ActiveRegion} key
     * @return {!libtess.DictNode}
     */
    libtess.Dict.prototype.insert = function (key) {
        // NOTE(bckenny): from a macro in dict.h/dict-list.h
        return this.insertBefore(this.head_, key);
    };
    /**
     * Remove node from the list.
     * @param {libtess.DictNode} node
     */
    libtess.Dict.prototype.deleteNode = function (node) {
        node.next.prev = node.prev;
        node.prev.next = node.next;
        // NOTE(bckenny): nulled at callsite (sweep.deleteRegion_)
        // memFree( node );
    };
    /**
     * Search returns the node with the smallest key greater than or equal
     * to the given key. If there is no such key, returns a node whose
     * key is null. Similarly, max(d).getSuccessor() has a null key, etc.
     * @param {!libtess.ActiveRegion} key
     * @return {!libtess.DictNode}
     */
    libtess.Dict.prototype.search = function (key) {
        var node = this.head_;
        do {
            node = node.next;
        } while (node.key !== null && !this.leq_(this.frame_, key, node.key));
        return node;
    };
    /**
     * Return the node with the smallest key.
     * @return {!libtess.DictNode}
     */
    libtess.Dict.prototype.getMin = function () {
        // NOTE(bckenny): from a macro in dict.h/dict-list.h
        return this.head_.next;
    };
    // NOTE(bckenny): libtess.Dict.getMax isn't called within libtess and isn't part
    // of the public API. For now, leaving in but ignoring for coverage.
    /* istanbul ignore next */
    /**
     * Returns the node with the greatest key.
     * @return {!libtess.DictNode}
     */
    libtess.Dict.prototype.getMax = function () {
        // NOTE(bckenny): from a macro in dict.h/dict-list.h
        return this.head_.prev;
    };
    /* global libtess */
    /**
     * A doubly-linked-list node with a libtess.ActiveRegion payload.
     * The key for this node and the next and previous nodes in the parent Dict list
     * can be provided to insert it into an existing list (or all can be omitted if
     * this is to be the founding node of the list).
     * @param {!libtess.ActiveRegion=} opt_key
     * @param {!libtess.DictNode=} opt_nextNode
     * @param {!libtess.DictNode=} opt_prevNode
     * @constructor
     * @struct
     */
    libtess.DictNode = function (opt_key, opt_nextNode, opt_prevNode) {
        /**
         * The ActiveRegion key for this node, or null if the head of the list.
         * @type {libtess.ActiveRegion}
         */
        this.key = opt_key || null;
        /**
         * Link to next DictNode in parent list or to self if this is the first node.
         * @type {!libtess.DictNode}
         */
        this.next = opt_nextNode || this;
        /**
         * Link to previous DictNode in parent list or to self if this is the first
         * node.
         * @type {!libtess.DictNode}
         */
        this.prev = opt_prevNode || this;
    };
    /**
     * Get the key from this node.
     * @return {libtess.ActiveRegion}
     */
    libtess.DictNode.prototype.getKey = function () {
        return this.key;
    };
    /**
     * Get the successor node to this one.
     * @return {!libtess.DictNode}
     */
    libtess.DictNode.prototype.getSuccessor = function () {
        return this.next;
    };
    /**
     * Get the predecessor node to this one.
     * @return {!libtess.DictNode}
     */
    libtess.DictNode.prototype.getPredecessor = function () {
        return this.prev;
    };
    /* global libtess */
    // TODO(bckenny): create more javascript-y API, e.g. make gluTessEndPolygon
    // async, don't require so many temp objects created
    /**
     * The tesselator main class, providing the public API.
     * @constructor
     * @struct
     */
    libtess.GluTesselator = function () {
        // Only initialize fields which can be changed by the api. Other fields
        // are initialized where they are used.
        /*** state needed for collecting the input data ***/
        /**
         * Tesselator state, tracking what begin/end calls have been seen.
         * @private {libtess.GluTesselator.tessState_}
         */
        this.state_ = libtess.GluTesselator.tessState_.T_DORMANT;
        /**
         * lastEdge_.org is the most recent vertex
         * @private {libtess.GluHalfEdge}
         */
        this.lastEdge_ = null;
        /**
         * stores the input contours, and eventually the tessellation itself
         * @type {libtess.GluMesh}
         */
        this.mesh = null;
        /**
         * Error callback.
         * @private {?function((libtess.errorType|libtess.gluEnum), Object=)}
         */
        this.errorCallback_ = null;
        /*** state needed for projecting onto the sweep plane ***/
        /**
         * user-specified normal (if provided)
         * @private {!Array<number>}
         */
        this.normal_ = [0, 0, 0];
        /*** state needed for the line sweep ***/
        /**
         * rule for determining polygon interior
         * @type {libtess.windingRule}
         */
        this.windingRule = libtess.windingRule.GLU_TESS_WINDING_ODD;
        /**
         * fatal error: needed combine callback
         * @type {boolean}
         */
        this.fatalError = false;
        /**
         * edge dictionary for sweep line
         * @type {libtess.Dict}
         */
        this.dict = null;
        // NOTE(bckenny): dict initialized in sweep.initEdgeDict_, removed in sweep.doneEdgeDict_
        /**
         * priority queue of vertex events
         * @type {libtess.PriorityQ}
         */
        this.pq = null;
        // NOTE(bckenny): pq initialized in sweep.initPriorityQ
        /**
         * current sweep event being processed
         * @type {libtess.GluVertex}
         */
        this.event = null;
        /**
         * Combine callback.
         * @private {?function(Array<number>, Array<Object>, Array<number>, Object=): Object}
         */
        this.combineCallback_ = null;
        /*** state needed for rendering callbacks (see render.js) ***/
        /**
         * Extract contours, not triangles
         * @private {boolean}
         */
        this.boundaryOnly_ = false;
        /**
         * Begin callback.
         * @private {?function(libtess.primitiveType, Object=)}
         */
        this.beginCallback_ = null;
        /**
         * Edge flag callback.
         * @private {?function(boolean, Object=)}
         */
        this.edgeFlagCallback_ = null;
        /**
         * Vertex callback.
         * @private {?function(Object, Object=)}
         */
        this.vertexCallback_ = null;
        /**
         * End callback.
         * @private {?function(Object=)}
         */
        this.endCallback_ = null;
        /**
         * Mesh callback.
         * @private {?function(libtess.GluMesh)}
         */
        this.meshCallback_ = null;
        /**
         * client data for current polygon
         * @private {Object}
         */
        this.polygonData_ = null;
    };
    /**
     * The begin/end calls must be properly nested. We keep track of the current
     * state to enforce the ordering.
     * @enum {number}
     * @private
     */
    libtess.GluTesselator.tessState_ = {
        T_DORMANT: 0,
        T_IN_POLYGON: 1,
        T_IN_CONTOUR: 2
    };
    /**
     * Destory the tesselator object. See README.
     */
    libtess.GluTesselator.prototype.gluDeleteTess = function () {
        // TODO(bckenny): This does nothing but assert that it isn't called while
        // building the polygon since we rely on GC to handle memory. *If* the public
        // API changes, this should go.
        this.requireState_(libtess.GluTesselator.tessState_.T_DORMANT);
        // memFree(tess); TODO(bckenny)
    };
    /**
     * Set properties for control over tesselation. See README.
     * @param {libtess.gluEnum} which [description].
     * @param {number|boolean} value [description].
     */
    libtess.GluTesselator.prototype.gluTessProperty = function (which, value) {
        // TODO(bckenny): split into more setters?
        // TODO(bckenny): in any case, we can do better than this switch statement
        switch (which) {
            case libtess.gluEnum.GLU_TESS_TOLERANCE:
                // NOTE(bckenny): libtess has never supported any tolerance but 0.
                return;
            case libtess.gluEnum.GLU_TESS_WINDING_RULE:
                var windingRule = /** @type {libtess.windingRule} */ (value);
                switch (windingRule) {
                    case libtess.windingRule.GLU_TESS_WINDING_ODD:
                    case libtess.windingRule.GLU_TESS_WINDING_NONZERO:
                    case libtess.windingRule.GLU_TESS_WINDING_POSITIVE:
                    case libtess.windingRule.GLU_TESS_WINDING_NEGATIVE:
                    case libtess.windingRule.GLU_TESS_WINDING_ABS_GEQ_TWO:
                        this.windingRule = windingRule;
                        return;
                    default:
                }
                break;
            case libtess.gluEnum.GLU_TESS_BOUNDARY_ONLY:
                this.boundaryOnly_ = !!value;
                return;
            default:
                this.callErrorCallback(libtess.gluEnum.GLU_INVALID_ENUM);
                return;
        }
        this.callErrorCallback(libtess.gluEnum.GLU_INVALID_VALUE);
    };
    /**
     * Returns tessellator property
     * @param {libtess.gluEnum} which [description].
     * @return {number|boolean} [description].
     */
    libtess.GluTesselator.prototype.gluGetTessProperty = function (which) {
        // TODO(bckenny): as above, split into more getters? and improve on switch statement
        // why are these being asserted in getter but not setter?
        switch (which) {
            case libtess.gluEnum.GLU_TESS_TOLERANCE:
                return 0;
            case libtess.gluEnum.GLU_TESS_WINDING_RULE:
                var rule = this.windingRule;
                return rule;
            case libtess.gluEnum.GLU_TESS_BOUNDARY_ONLY:
                return this.boundaryOnly_;
            default:
                this.callErrorCallback(libtess.gluEnum.GLU_INVALID_ENUM);
                break;
        }
        return false;
    };
    /**
     * Lets the user supply the polygon normal, if known. All input data is
     * projected into a plane perpendicular to the normal before tesselation. All
     * output triangles are oriented CCW with respect to the normal (CW orientation
     * can be obtained by reversing the sign of the supplied normal). For example,
     * if you know that all polygons lie in the x-y plane, call
     * `tess.gluTessNormal(0.0, 0.0, 1.0)` before rendering any polygons.
     * @param {number} x
     * @param {number} y
     * @param {number} z
     */
    libtess.GluTesselator.prototype.gluTessNormal = function (x, y, z) {
        this.normal_[0] = x;
        this.normal_[1] = y;
        this.normal_[2] = z;
    };
    /**
     * Specify callbacks. See README for callback descriptions. A null or undefined
     * opt_fn removes current callback.
     * @param {libtess.gluEnum} which The callback-type gluEnum value.
     * @param {?Function=} opt_fn
     */
    libtess.GluTesselator.prototype.gluTessCallback = function (which, opt_fn) {
        var fn = !opt_fn ? null : opt_fn;
        // TODO(bckenny): better opt_fn typing?
        // TODO(bckenny): should add documentation that references in callback are volatile (or make a copy)
        switch (which) {
            case libtess.gluEnum.GLU_TESS_BEGIN:
            case libtess.gluEnum.GLU_TESS_BEGIN_DATA:
                this.beginCallback_ = /** @type {?function(libtess.primitiveType, Object=)} */ (fn);
                return;
            case libtess.gluEnum.GLU_TESS_EDGE_FLAG:
            case libtess.gluEnum.GLU_TESS_EDGE_FLAG_DATA:
                this.edgeFlagCallback_ = /** @type {?function(boolean, Object=)} */ (fn);
                return;
            case libtess.gluEnum.GLU_TESS_VERTEX:
            case libtess.gluEnum.GLU_TESS_VERTEX_DATA:
                this.vertexCallback_ = /** @type {?function(Object, Object=)} */ (fn);
                return;
            case libtess.gluEnum.GLU_TESS_END:
            case libtess.gluEnum.GLU_TESS_END_DATA:
                this.endCallback_ = /** @type {?function(Object=)} */ (fn);
                return;
            case libtess.gluEnum.GLU_TESS_ERROR:
            case libtess.gluEnum.GLU_TESS_ERROR_DATA:
                this.errorCallback_ = /** @type {?function((libtess.errorType|libtess.gluEnum), Object=)} */ (fn);
                return;
            case libtess.gluEnum.GLU_TESS_COMBINE:
            case libtess.gluEnum.GLU_TESS_COMBINE_DATA:
                this.combineCallback_ = /** @type {?function(Array<number>, Array<Object>, Array<number>, Object=): Object} */ (fn);
                return;
            case libtess.gluEnum.GLU_TESS_MESH:
                this.meshCallback_ = /** @type {?function(libtess.GluMesh)} */ (fn);
                return;
            default:
                this.callErrorCallback(libtess.gluEnum.GLU_INVALID_ENUM);
                return;
        }
    };
    /**
     * Specify a vertex and associated data. Must be within calls to
     * beginContour/endContour. See README.
     * @param {!Array<number>} coords
     * @param {Object} data
     */
    libtess.GluTesselator.prototype.gluTessVertex = function (coords, data) {
        var tooLarge = false;
        // TODO(bckenny): pool allocation?
        var clamped = [0, 0, 0];
        this.requireState_(libtess.GluTesselator.tessState_.T_IN_CONTOUR);
        for (var i = 0; i < 3; ++i) {
            var x = coords[i];
            if (x < -libtess.GLU_TESS_MAX_COORD) {
                x = -libtess.GLU_TESS_MAX_COORD;
                tooLarge = true;
            }
            if (x > libtess.GLU_TESS_MAX_COORD) {
                x = libtess.GLU_TESS_MAX_COORD;
                tooLarge = true;
            }
            clamped[i] = x;
        }
        if (tooLarge) {
            this.callErrorCallback(libtess.errorType.GLU_TESS_COORD_TOO_LARGE);
        }
        this.addVertex_(clamped, data);
    };
    /**
     * [gluTessBeginPolygon description]
     * @param {Object} data Client data for current polygon.
     */
    libtess.GluTesselator.prototype.gluTessBeginPolygon = function (data) {
        this.requireState_(libtess.GluTesselator.tessState_.T_DORMANT);
        this.state_ = libtess.GluTesselator.tessState_.T_IN_POLYGON;
        this.mesh = new libtess.GluMesh();
        this.polygonData_ = data;
    };
    /**
     * [gluTessBeginContour description]
     */
    libtess.GluTesselator.prototype.gluTessBeginContour = function () {
        this.requireState_(libtess.GluTesselator.tessState_.T_IN_POLYGON);
        this.state_ = libtess.GluTesselator.tessState_.T_IN_CONTOUR;
        this.lastEdge_ = null;
    };
    /**
     * [gluTessEndContour description]
     */
    libtess.GluTesselator.prototype.gluTessEndContour = function () {
        this.requireState_(libtess.GluTesselator.tessState_.T_IN_CONTOUR);
        this.state_ = libtess.GluTesselator.tessState_.T_IN_POLYGON;
    };
    /**
     * [gluTessEndPolygon description]
     */
    libtess.GluTesselator.prototype.gluTessEndPolygon = function () {
        this.requireState_(libtess.GluTesselator.tessState_.T_IN_POLYGON);
        this.state_ = libtess.GluTesselator.tessState_.T_DORMANT;
        // Determine the polygon normal and project vertices onto the plane
        // of the polygon.
        libtess.normal.projectPolygon(this, this.normal_[0], this.normal_[1], this.normal_[2]);
        // computeInterior(tess) computes the planar arrangement specified
        // by the given contours, and further subdivides this arrangement
        // into regions. Each region is marked "inside" if it belongs
        // to the polygon, according to the rule given by this.windingRule.
        // Each interior region is guaranteed be monotone.
        libtess.sweep.computeInterior(this);
        if (!this.fatalError) {
            // If the user wants only the boundary contours, we throw away all edges
            // except those which separate the interior from the exterior.
            // Otherwise we tessellate all the regions marked "inside".
            // NOTE(bckenny): we know this.mesh has been initialized, so help closure out.
            var mesh = /** @type {!libtess.GluMesh} */ (this.mesh);
            if (this.boundaryOnly_) {
                libtess.tessmono.setWindingNumber(mesh, 1, true);
            }
            else {
                libtess.tessmono.tessellateInterior(mesh);
            }
            this.mesh.checkMesh();
            if (this.beginCallback_ || this.endCallback_ || this.vertexCallback_ ||
                this.edgeFlagCallback_) {
                if (this.boundaryOnly_) {
                    // output boundary contours
                    libtess.render.renderBoundary(this, this.mesh);
                }
                else {
                    // output triangles (with edge callback if one is set)
                    var flagEdges = !!this.edgeFlagCallback_;
                    libtess.render.renderMesh(this, this.mesh, flagEdges);
                }
            }
            if (this.meshCallback_) {
                // Throw away the exterior faces, so that all faces are interior.
                // This way the user doesn't have to check the "inside" flag,
                // and we don't need to even reveal its existence. It also leaves
                // the freedom for an implementation to not generate the exterior
                // faces in the first place.
                libtess.tessmono.discardExterior(this.mesh);
                // user wants the mesh itself
                this.meshCallback_(this.mesh);
                this.mesh = null;
                this.polygonData_ = null;
                return;
            }
        }
        libtess.mesh.deleteMesh(this.mesh);
        this.polygonData_ = null;
        this.mesh = null;
    };
    /**
     * Change the tesselator state.
     * @private
     * @param {libtess.GluTesselator.tessState_} state
     */
    libtess.GluTesselator.prototype.requireState_ = function (state) {
        if (this.state_ !== state) {
            this.gotoState_(state);
        }
    };
    /**
     * Change the current tesselator state one level at a time to get to the
     * desired state. Only triggered when the API is not called in the correct order
     * so an error callback is made, however the tesselator will always attempt to
     * recover afterwards (see README).
     * @private
     * @param {libtess.GluTesselator.tessState_} newState
     */
    libtess.GluTesselator.prototype.gotoState_ = function (newState) {
        while (this.state_ !== newState) {
            if (this.state_ < newState) {
                switch (this.state_) {
                    case libtess.GluTesselator.tessState_.T_DORMANT:
                        this.callErrorCallback(libtess.errorType.GLU_TESS_MISSING_BEGIN_POLYGON);
                        this.gluTessBeginPolygon(null);
                        break;
                    case libtess.GluTesselator.tessState_.T_IN_POLYGON:
                        this.callErrorCallback(libtess.errorType.GLU_TESS_MISSING_BEGIN_CONTOUR);
                        this.gluTessBeginContour();
                        break;
                }
            }
            else {
                switch (this.state_) {
                    case libtess.GluTesselator.tessState_.T_IN_CONTOUR:
                        this.callErrorCallback(libtess.errorType.GLU_TESS_MISSING_END_CONTOUR);
                        this.gluTessEndContour();
                        break;
                    case libtess.GluTesselator.tessState_.T_IN_POLYGON:
                        this.callErrorCallback(libtess.errorType.GLU_TESS_MISSING_END_POLYGON);
                        // NOTE(bckenny): libtess originally reset the tesselator, even though
                        // the README claims it should spit out the tessellated results at
                        // this point.
                        // (see http://cgit.freedesktop.org/mesa/glu/tree/src/libtess/tess.c#n180)
                        this.gluTessEndPolygon();
                        break;
                }
            }
        }
    };
    /**
     * [addVertex_ description]
     * @private
     * @param {!Array<number>} coords [description].
     * @param {Object} data [description].
     */
    libtess.GluTesselator.prototype.addVertex_ = function (coords, data) {
        var e = this.lastEdge_;
        if (e === null) {
            // Make a self-loop (one vertex, one edge).
            e = libtess.mesh.makeEdge(this.mesh);
            libtess.mesh.meshSplice(e, e.sym);
        }
        else {
            // Create a new vertex and edge which immediately follow e
            // in the ordering around the left face.
            libtess.mesh.splitEdge(e);
            e = e.lNext;
        }
        // The new vertex is now e.org.
        e.org.data = data;
        e.org.coords[0] = coords[0];
        e.org.coords[1] = coords[1];
        e.org.coords[2] = coords[2];
        // The winding of an edge says how the winding number changes as we
        // cross from the edge''s right face to its left face.  We add the
        // vertices in such an order that a CCW contour will add +1 to
        // the winding number of the region inside the contour.
        e.winding = 1;
        e.sym.winding = -1;
        this.lastEdge_ = e;
    };
    /**
     * Call callback to indicate the start of a primitive, to be followed by emitted
     * vertices, if any. In libtess.js, `type` will always be `GL_TRIANGLES`.
     * @param {libtess.primitiveType} type
     */
    libtess.GluTesselator.prototype.callBeginCallback = function (type) {
        if (this.beginCallback_) {
            this.beginCallback_(type, this.polygonData_);
        }
    };
    /**
     * Call callback to emit a vertex of the tessellated polygon.
     * @param {Object} data
     */
    libtess.GluTesselator.prototype.callVertexCallback = function (data) {
        if (this.vertexCallback_) {
            this.vertexCallback_(data, this.polygonData_);
        }
    };
    /**
     * Call callback to indicate whether the vertices to follow begin edges which
     * lie on a polygon boundary.
     * @param {boolean} flag
     */
    libtess.GluTesselator.prototype.callEdgeFlagCallback = function (flag) {
        if (this.edgeFlagCallback_) {
            this.edgeFlagCallback_(flag, this.polygonData_);
        }
    };
    /**
     * Call callback to indicate the end of tessellation.
     */
    libtess.GluTesselator.prototype.callEndCallback = function () {
        if (this.endCallback_) {
            this.endCallback_(this.polygonData_);
        }
    };
    /* jscs:disable maximumLineLength */
    /**
     * Call callback for combining vertices at edge intersection requiring the
     * creation of a new vertex.
     * @param {!Array<number>} coords Intersection coordinates.
     * @param {!Array<Object>} data Array of vertex data, one per edge vertices.
     * @param {!Array<number>} weight Coefficients used for the linear combination of vertex coordinates that gives coords.
     * @return {?Object} Interpolated vertex.
     */
    libtess.GluTesselator.prototype.callCombineCallback = function (coords, data, weight) {
        if (this.combineCallback_) {
            return this.combineCallback_(coords, data, weight, this.polygonData_) ||
                null;
        }
        return null;
    };
    /* jscs:enable maximumLineLength */
    /**
     * Call error callback, if specified, with errno.
     * @param {(libtess.errorType|libtess.gluEnum)} errno
     */
    libtess.GluTesselator.prototype.callErrorCallback = function (errno) {
        if (this.errorCallback_) {
            this.errorCallback_(errno, this.polygonData_);
        }
    };
    /* global libtess */
    /**
     * Each face has a pointer to the next and previous faces in the
     * circular list, and a pointer to a half-edge with this face as
     * the left face (null if this is the dummy header). There is also
     * a field "data" for client data.
     *
     * @param {libtess.GluFace=} opt_nextFace
     * @param {libtess.GluFace=} opt_prevFace
     * @constructor
     * @struct
     */
    libtess.GluFace = function (opt_nextFace, opt_prevFace) {
        // TODO(bckenny): reverse order of params?
        /**
         * next face (never null)
         * @type {!libtess.GluFace}
         */
        this.next = opt_nextFace || this;
        /**
         * previous face (never NULL)
         * @type {!libtess.GluFace}
         */
        this.prev = opt_prevFace || this;
        /**
         * A half edge with this left face.
         * @type {libtess.GluHalfEdge}
         */
        this.anEdge = null;
        /**
         * room for client's data
         * @type {Object}
         */
        this.data = null;
        /**
         * This face is in the polygon interior.
         * @type {boolean}
         */
        this.inside = false;
    };
    /* global libtess */
    /**
     * The fundamental data structure is the "half-edge". Two half-edges
     * go together to make an edge, but they point in opposite directions.
     * Each half-edge has a pointer to its mate (the "symmetric" half-edge sym),
     * its origin vertex (org), the face on its left side (lFace), and the
     * adjacent half-edges in the CCW direction around the origin vertex
     * (oNext) and around the left face (lNext). There is also a "next"
     * pointer for the global edge list (see below).
     *
     * The notation used for mesh navigation:
     *  sym   = the mate of a half-edge (same edge, but opposite direction)
     *  oNext = edge CCW around origin vertex (keep same origin)
     *  dNext = edge CCW around destination vertex (keep same dest)
     *  lNext = edge CCW around left face (dest becomes new origin)
     *  rNext = edge CCW around right face (origin becomes new dest)
     *
     * "prev" means to substitute CW for CCW in the definitions above.
     *
     * The circular edge list is special; since half-edges always occur
     * in pairs (e and e.sym), each half-edge stores a pointer in only
     * one direction. Starting at eHead and following the e.next pointers
     * will visit each *edge* once (ie. e or e.sym, but not both).
     * e.sym stores a pointer in the opposite direction, thus it is
     * always true that e.sym.next.sym.next === e.
     *
     * @param {libtess.GluHalfEdge=} opt_nextEdge
     * @constructor
     * @struct
     */
    libtess.GluHalfEdge = function (opt_nextEdge) {
        // TODO(bckenny): are these the right defaults? (from gl_meshNewMesh requirements)
        /**
         * doubly-linked list (prev==sym->next)
         * @type {!libtess.GluHalfEdge}
         */
        this.next = opt_nextEdge || this;
        // TODO(bckenny): how can this be required if created in pairs? move to factory creation only?
        /**
         * same edge, opposite direction
         * @type {libtess.GluHalfEdge}
         */
        this.sym = null;
        /**
         * next edge CCW around origin
         * @type {libtess.GluHalfEdge}
         */
        this.oNext = null;
        /**
         * next edge CCW around left face
         * @type {libtess.GluHalfEdge}
         */
        this.lNext = null;
        /**
         * origin vertex (oVertex too long)
         * @type {libtess.GluVertex}
         */
        this.org = null;
        /**
         * left face
         * @type {libtess.GluFace}
         */
        this.lFace = null;
        // Internal data (keep hidden)
        // NOTE(bckenny): can't be private, though...
        /**
         * a region with this upper edge (see sweep.js)
         * @type {libtess.ActiveRegion}
         */
        this.activeRegion = null;
        /**
         * change in winding number when crossing from the right face to the left face
         * @type {number}
         */
        this.winding = 0;
    };
    // NOTE(bckenny): the following came from macros in mesh
    // TODO(bckenny): using methods as aliases for sym connections for now.
    // not sure about this approach. getters? renames?
    /**
     * [rFace description]
     * @return {libtess.GluFace} [description].
     */
    libtess.GluHalfEdge.prototype.rFace = function () {
        return this.sym.lFace;
    };
    /**
     * [dst description]
     * @return {libtess.GluVertex} [description].
     */
    libtess.GluHalfEdge.prototype.dst = function () {
        return this.sym.org;
    };
    /**
     * [oPrev description]
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.GluHalfEdge.prototype.oPrev = function () {
        return this.sym.lNext;
    };
    /**
     * [lPrev description]
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.GluHalfEdge.prototype.lPrev = function () {
        return this.oNext.sym;
    };
    // NOTE(bckenny): libtess.GluHalfEdge.dPrev is called nowhere in libtess and
    // isn't part of the current public API. It could be useful for mesh traversal
    // and manipulation if made public, however.
    /* istanbul ignore next */
    /**
     * The edge clockwise around destination vertex (keep same dest).
     * @return {libtess.GluHalfEdge}
     */
    libtess.GluHalfEdge.prototype.dPrev = function () {
        return this.lNext.sym;
    };
    /**
     * [rPrev description]
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.GluHalfEdge.prototype.rPrev = function () {
        return this.sym.oNext;
    };
    /**
     * [dNext description]
     * @return {libtess.GluHalfEdge} [description].
     */
    libtess.GluHalfEdge.prototype.dNext = function () {
        return this.rPrev().sym;
    };
    // NOTE(bckenny): libtess.GluHalfEdge.rNext is called nowhere in libtess and
    // isn't part of the current public API. It could be useful for mesh traversal
    // and manipulation if made public, however.
    /* istanbul ignore next */
    /**
     * The edge CCW around the right face (origin of this becomes new dest).
     * @return {libtess.GluHalfEdge}
     */
    libtess.GluHalfEdge.prototype.rNext = function () {
        return this.oPrev().sym;
    };
    /* global libtess */
    /**
     * Creates a new mesh with no edges, no vertices,
     * and no loops (what we usually call a "face").
     *
     * @constructor
     * @struct
     */
    libtess.GluMesh = function () {
        /**
         * dummy header for vertex list
         * @type {libtess.GluVertex}
         */
        this.vHead = new libtess.GluVertex();
        /**
         * dummy header for face list
         * @type {libtess.GluFace}
         */
        this.fHead = new libtess.GluFace();
        /**
         * dummy header for edge list
         * @type {libtess.GluHalfEdge}
         */
        this.eHead = new libtess.GluHalfEdge();
        /**
         * and its symmetric counterpart
         * @type {libtess.GluHalfEdge}
         */
        this.eHeadSym = new libtess.GluHalfEdge();
        // TODO(bckenny): better way to pair these?
        this.eHead.sym = this.eHeadSym;
        this.eHeadSym.sym = this.eHead;
    };
    // TODO(bckenny): #ifndef NDEBUG
    /**
     * Checks mesh for self-consistency.
     */
    libtess.GluMesh.prototype.checkMesh = function () {
        if (!libtess.DEBUG) {
            return;
        }
        var fHead = this.fHead;
        var vHead = this.vHead;
        var eHead = this.eHead;
        var e;
        // faces
        var f;
        var fPrev = fHead;
        for (fPrev = fHead; (f = fPrev.next) !== fHead; fPrev = f) {
            e = f.anEdge;
            do {
                e = e.lNext;
            } while (e !== f.anEdge);
        }
        // vertices
        var v;
        var vPrev = vHead;
        for (vPrev = vHead; (v = vPrev.next) !== vHead; vPrev = v) {
            e = v.anEdge;
            do {
                e = e.oNext;
            } while (e !== v.anEdge);
        }
        // edges
        var ePrev = eHead;
        for (ePrev = eHead; (e = ePrev.next) !== eHead; ePrev = e) {
        }
    };
    /* global libtess */
    /**
     * Each vertex has a pointer to next and previous vertices in the
     * circular list, and a pointer to a half-edge with this vertex as
     * the origin (null if this is the dummy header). There is also a
     * field "data" for client data.
     * @param {libtess.GluVertex=} opt_nextVertex Optional reference to next vertex in the vertex list.
     * @param {libtess.GluVertex=} opt_prevVertex Optional reference to previous vertex in the vertex list.
     * @constructor
     * @struct
     */
    libtess.GluVertex = function (opt_nextVertex, opt_prevVertex) {
        /**
         * Next vertex (never null).
         * @type {!libtess.GluVertex}
         */
        this.next = opt_nextVertex || this;
        /**
         * Previous vertex (never null).
         * @type {!libtess.GluVertex}
         */
        this.prev = opt_prevVertex || this;
        /**
         * A half-edge with this origin.
         * @type {libtess.GluHalfEdge}
         */
        this.anEdge = null;
        /**
         * The client's data.
         * @type {Object}
         */
        this.data = null;
        /**
         * The vertex location in 3D.
         * @type {!Array.<number>}
         */
        this.coords = [0, 0, 0];
        // TODO(bckenny): we may want to rethink coords, either eliminate (using s
        // and t and user data) or index into contiguous storage?
        /**
         * Component of projection onto the sweep plane.
         * @type {number}
         */
        this.s = 0;
        /**
         * Component of projection onto the sweep plane.
         * @type {number}
         */
        this.t = 0;
        /**
         * Handle to allow deletion from priority queue, or 0 if not yet inserted into
         * queue.
         * @type {libtess.PQHandle}
         */
        this.pqHandle = 0;
    };
    /* global libtess */
    /**
     * A priority queue of vertices, ordered by libtess.geom.vertLeq, implemented
     * with a sorted array. Used for initial insertion of vertices (see
     * libtess.sweep.initPriorityQ_), sorted once, then it uses an internal
     * libtess.PriorityQHeap for any subsequently created vertices from
     * intersections.
     * @constructor
     * @struct
     */
    libtess.PriorityQ = function () {
        /**
         * An unordered list of vertices that have been inserted in the queue, with
         * null in empty slots.
         * @private {Array<libtess.GluVertex>}
         */
        this.verts_ = [];
        /**
         * Array of indices into this.verts_, sorted by vertLeq over the addressed
         * vertices.
         * @private {Array<number>}
         */
        this.order_ = null;
        /**
         * The size of this queue, not counting any vertices stored in heap_.
         * @private {number}
         */
        this.size_ = 0;
        /**
         * Indicates that the queue has been initialized via init. If false, inserts
         * are fast insertions at the end of the verts_ array. If true, the verts_
         * array is sorted and subsequent inserts are done in the heap.
         * @private {boolean}
         */
        this.initialized_ = false;
        /**
         * A priority queue heap, used for faster insertions of vertices after verts_
         * has been sorted.
         * @private {libtess.PriorityQHeap}
         */
        this.heap_ = new libtess.PriorityQHeap();
    };
    /**
     * Release major storage memory used by priority queue.
     */
    libtess.PriorityQ.prototype.deleteQ = function () {
        // TODO(bckenny): could instead clear most of these.
        this.heap_ = null;
        this.order_ = null;
        this.verts_ = null;
        // NOTE(bckenny): nulled at callsite (sweep.donePriorityQ_)
    };
    /**
     * Sort vertices by libtess.geom.vertLeq. Must be called before any method other
     * than insert is called to ensure correctness when removing or querying.
     */
    libtess.PriorityQ.prototype.init = function () {
        // TODO(bckenny): reuse. in theory, we don't have to empty this, as access is
        // dictated by this.size_, but array.sort doesn't know that
        this.order_ = [];
        // Create an array of indirect pointers to the verts, so that
        // the handles we have returned are still valid.
        // TODO(bckenny): valid for when? it appears we can just store indexes into
        // verts_, but what did this mean?
        for (var i = 0; i < this.size_; i++) {
            this.order_[i] = i;
        }
        // sort the indirect pointers in descending order of the verts themselves
        // TODO(bckenny): make sure it's ok that verts[a] === verts[b] returns 1
        // TODO(bckenny): unstable sort means we may get slightly different polys in
        // different browsers, but only when passing in equal points
        // TODO(bckenny): make less awkward closure?
        var comparator = (function (verts) {
            return function (a, b) {
                return libtess.geom.vertLeq(verts[a], verts[b]) ? 1 : -1;
            };
        })(this.verts_);
        this.order_.sort(comparator);
        this.initialized_ = true;
        this.heap_.init();
        // NOTE(bckenny): debug assert of ordering of the verts_ array.
        if (libtess.DEBUG) {
            var p = 0;
            var r = p + this.size_ - 1;
            for (i = p; i < r; ++i) {
            }
        }
    };
    /**
     * Insert a vertex into the priority queue. Returns a PQHandle to refer to it,
     * which will never be 0.
     * @param {libtess.GluVertex} vert
     * @return {libtess.PQHandle}
     */
    libtess.PriorityQ.prototype.insert = function (vert) {
        // NOTE(bckenny): originally returned LONG_MAX as alloc failure signal. no
        // longer does.
        if (this.initialized_) {
            return this.heap_.insert(vert);
        }
        var curr = this.size_++;
        this.verts_[curr] = vert;
        // Negative handles index the sorted array.
        return -(curr + 1);
    };
    /**
     * Removes the minimum vertex from the queue and returns it. If the queue is
     * empty, null will be returned.
     * @return {libtess.GluVertex}
     */
    libtess.PriorityQ.prototype.extractMin = function () {
        if (this.size_ === 0) {
            return this.heap_.extractMin();
        }
        var sortMin = this.verts_[this.order_[this.size_ - 1]];
        if (!this.heap_.isEmpty()) {
            var heapMin = this.heap_.minimum();
            if (libtess.geom.vertLeq(heapMin, sortMin)) {
                return this.heap_.extractMin();
            }
        }
        do {
            --this.size_;
        } while (this.size_ > 0 && this.verts_[this.order_[this.size_ - 1]] === null);
        return sortMin;
    };
    /**
     * Returns the minimum vertex in the queue. If the queue is empty, null will be
     * returned.
     * @return {libtess.GluVertex}
     */
    libtess.PriorityQ.prototype.minimum = function () {
        if (this.size_ === 0) {
            return this.heap_.minimum();
        }
        var sortMin = this.verts_[this.order_[this.size_ - 1]];
        if (!this.heap_.isEmpty()) {
            var heapMin = this.heap_.minimum();
            if (libtess.geom.vertLeq(heapMin, sortMin)) {
                return heapMin;
            }
        }
        return sortMin;
    };
    /**
     * Remove vertex with handle removeHandle from queue.
     * @param {libtess.PQHandle} removeHandle
     */
    libtess.PriorityQ.prototype.remove = function (removeHandle) {
        if (removeHandle >= 0) {
            this.heap_.remove(removeHandle);
            return;
        }
        removeHandle = -(removeHandle + 1);
        this.verts_[removeHandle] = null;
        while (this.size_ > 0 && this.verts_[this.order_[this.size_ - 1]] === null) {
            --this.size_;
        }
    };
    /* global libtess */
    /**
     * A priority queue of vertices, ordered by libtess.geom.vertLeq, implemented
     * with a binary heap. Used only within libtess.PriorityQ for prioritizing
     * vertices created by intersections (see libtess.sweep.checkForIntersect_).
     * @constructor
     * @struct
     */
    libtess.PriorityQHeap = function () {
        /**
         * The heap itself. Active nodes are stored in the range 1..size, with the
         * minimum at 1. Each node stores only an index into verts_ and handles_.
         * @private {!Array<number>}
         */
        this.heap_ = libtess.PriorityQHeap.reallocNumeric_([0], libtess.PriorityQHeap.INIT_SIZE_ + 1);
        /**
         * An unordered list of vertices in the heap, with null in empty slots.
         * @private {!Array<libtess.GluVertex>}
         */
        this.verts_ = [null, null];
        /**
         * An unordered list of indices mapping vertex handles into the heap. An entry
         * at index i will map the vertex at i in verts_ to its place in the heap
         * (i.e. heap_[handles_[i]] === i).
         * Empty slots below size_ are a free list chain starting at freeList_.
         * @private {!Array<number>}
         */
        this.handles_ = [0, 0];
        /**
         * The size of the queue.
         * @private {number}
         */
        this.size_ = 0;
        /**
         * The queue's current allocated space.
         * @private {number}
         */
        this.max_ = libtess.PriorityQHeap.INIT_SIZE_;
        /**
         * The index of the next free hole in the verts_ array. That slot in handles_
         * has the next index in the free list. If there are no holes, freeList_ === 0
         * and a new vertex must be appended to the list.
         * @private {libtess.PQHandle}
         */
        this.freeList_ = 0;
        /**
         * Indicates that the heap has been initialized via init. If false, inserts
         * are fast insertions at the end of a list. If true, all inserts will now be
         * correctly ordered in the queue before returning.
         * @private {boolean}
         */
        this.initialized_ = false;
        // Point the first index at the first (currently null) vertex.
        this.heap_[1] = 1;
    };
    /**
     * The initial allocated space for the queue.
     * @const
     * @private {number}
     */
    libtess.PriorityQHeap.INIT_SIZE_ = 32;
    /**
     * Allocate a numeric index array of size size. oldArray's contents are copied
     * to the beginning of the new array. The rest of the array is filled with
     * zeroes.
     * @private
     * @param {!Array<number>} oldArray
     * @param {number} size
     * @return {!Array<number>}
     */
    libtess.PriorityQHeap.reallocNumeric_ = function (oldArray, size) {
        var newArray = new Array(size);
        // NOTE(bckenny): V8 likes this significantly more than simply growing the
        // array element-by-element or expanding the existing array all at once, so,
        // for now, emulating realloc.
        for (var index = 0; index < oldArray.length; index++) {
            newArray[index] = oldArray[index];
        }
        for (; index < size; index++) {
            newArray[index] = 0;
        }
        return newArray;
    };
    /**
     * Initializing ordering of the heap. Must be called before any method other
     * than insert is called to ensure correctness when removing or querying.
     */
    libtess.PriorityQHeap.prototype.init = function () {
        // This method of building a heap is O(n), rather than O(n lg n).
        for (var i = this.size_; i >= 1; --i) {
            // TODO(bckenny): since init is called before anything is inserted (see
            // PriorityQ.init), this will always be empty. Better to lazily init?
            this.floatDown_(i);
        }
        this.initialized_ = true;
    };
    /**
     * Insert a new vertex into the heap.
     * @param {libtess.GluVertex} vert The vertex to insert.
     * @return {libtess.PQHandle} A handle that can be used to remove the vertex.
     */
    libtess.PriorityQHeap.prototype.insert = function (vert) {
        var endIndex = ++this.size_;
        // If the heap overflows, double its size.
        if ((endIndex * 2) > this.max_) {
            this.max_ *= 2;
            this.handles_ = libtess.PriorityQHeap.reallocNumeric_(this.handles_, this.max_ + 1);
        }
        var newVertSlot;
        if (this.freeList_ === 0) {
            // No free slots, append vertex.
            newVertSlot = endIndex;
        }
        else {
            // Put vertex in free slot, update freeList_ to next free slot.
            newVertSlot = this.freeList_;
            this.freeList_ = this.handles_[this.freeList_];
        }
        this.verts_[newVertSlot] = vert;
        this.handles_[newVertSlot] = endIndex;
        this.heap_[endIndex] = newVertSlot;
        if (this.initialized_) {
            this.floatUp_(endIndex);
        }
        return newVertSlot;
    };
    /**
     * @return {boolean} Whether the heap is empty.
     */
    libtess.PriorityQHeap.prototype.isEmpty = function () {
        return this.size_ === 0;
    };
    /**
     * Returns the minimum vertex in the heap. If the heap is empty, null will be
     * returned.
     * @return {libtess.GluVertex}
     */
    libtess.PriorityQHeap.prototype.minimum = function () {
        return this.verts_[this.heap_[1]];
    };
    /**
     * Removes the minimum vertex from the heap and returns it. If the heap is
     * empty, null will be returned.
     * @return {libtess.GluVertex}
     */
    libtess.PriorityQHeap.prototype.extractMin = function () {
        var heap = this.heap_;
        var verts = this.verts_;
        var handles = this.handles_;
        var minHandle = heap[1];
        var minVertex = verts[minHandle];
        if (this.size_ > 0) {
            // Replace min with last vertex.
            heap[1] = heap[this.size_];
            handles[heap[1]] = 1;
            // Clear min vertex and put slot at front of freeList_.
            verts[minHandle] = null;
            handles[minHandle] = this.freeList_;
            this.freeList_ = minHandle;
            // Restore heap.
            if (--this.size_ > 0) {
                this.floatDown_(1);
            }
        }
        return minVertex;
    };
    /**
     * Remove vertex with handle removeHandle from heap.
     * @param {libtess.PQHandle} removeHandle
     */
    libtess.PriorityQHeap.prototype.remove = function (removeHandle) {
        var heap = this.heap_;
        var verts = this.verts_;
        var handles = this.handles_;
        var heapIndex = handles[removeHandle];
        // Replace with last vertex.
        heap[heapIndex] = heap[this.size_];
        handles[heap[heapIndex]] = heapIndex;
        // Restore heap.
        if (heapIndex <= --this.size_) {
            if (heapIndex <= 1) {
                this.floatDown_(heapIndex);
            }
            else {
                var vert = verts[heap[heapIndex]];
                var parentVert = verts[heap[heapIndex >> 1]];
                if (libtess.geom.vertLeq(parentVert, vert)) {
                    this.floatDown_(heapIndex);
                }
                else {
                    this.floatUp_(heapIndex);
                }
            }
        }
        // Clear vertex and put slot at front of freeList_.
        verts[removeHandle] = null;
        handles[removeHandle] = this.freeList_;
        this.freeList_ = removeHandle;
    };
    /**
     * Restore heap by moving the vertex at index in the heap downwards to a valid
     * slot.
     * @private
     * @param {libtess.PQHandle} index
     */
    libtess.PriorityQHeap.prototype.floatDown_ = function (index) {
        var heap = this.heap_;
        var verts = this.verts_;
        var handles = this.handles_;
        var currIndex = index;
        var currHandle = heap[currIndex];
        for (;;) {
            // The children of node i are nodes 2i and 2i+1.
            var childIndex = currIndex << 1;
            if (childIndex < this.size_) {
                // Set child to the index of the child with the minimum vertex.
                if (libtess.geom.vertLeq(verts[heap[childIndex + 1]], verts[heap[childIndex]])) {
                    childIndex = childIndex + 1;
                }
            }
            var childHandle = heap[childIndex];
            if (childIndex > this.size_ ||
                libtess.geom.vertLeq(verts[currHandle], verts[childHandle])) {
                // Heap restored.
                heap[currIndex] = currHandle;
                handles[currHandle] = currIndex;
                return;
            }
            // Swap current node and child; repeat from childIndex.
            heap[currIndex] = childHandle;
            handles[childHandle] = currIndex;
            currIndex = childIndex;
        }
    };
    /**
     * Restore heap by moving the vertex at index in the heap upwards to a valid
     * slot.
     * @private
     * @param {libtess.PQHandle} index
     */
    libtess.PriorityQHeap.prototype.floatUp_ = function (index) {
        var heap = this.heap_;
        var verts = this.verts_;
        var handles = this.handles_;
        var currIndex = index;
        var currHandle = heap[currIndex];
        for (;;) {
            // The parent of node i is node floor(i/2).
            var parentIndex = currIndex >> 1;
            var parentHandle = heap[parentIndex];
            if (parentIndex === 0 ||
                libtess.geom.vertLeq(verts[parentHandle], verts[currHandle])) {
                // Heap restored.
                heap[currIndex] = currHandle;
                handles[currHandle] = currIndex;
                return;
            }
            // Swap current node and parent; repeat from parentIndex.
            heap[currIndex] = parentHandle;
            handles[parentHandle] = currIndex;
            currIndex = parentIndex;
        }
    };
    /* global libtess */
    // TODO(bckenny): apparently only visible outside of sweep for debugging routines.
    // find out if we can hide
    /**
     * For each pair of adjacent edges crossing the sweep line, there is
     * an ActiveRegion to represent the region between them. The active
     * regions are kept in sorted order in a dynamic dictionary. As the
     * sweep line crosses each vertex, we update the affected regions.
     * @constructor
     * @struct
     */
    libtess.ActiveRegion = function () {
        // TODO(bckenny): I *think* eUp and nodeUp could be passed in as constructor params
        /**
         * The upper edge of the region, directed right to left
         * @type {libtess.GluHalfEdge}
         */
        this.eUp = null;
        /**
         * Dictionary node corresponding to eUp edge.
         * @type {libtess.DictNode}
         */
        this.nodeUp = null;
        /**
         * Used to determine which regions are inside the polygon.
         * @type {number}
         */
        this.windingNumber = 0;
        /**
         * Whether this region is inside the polygon.
         * @type {boolean}
         */
        this.inside = false;
        /**
         * Marks fake edges at t = +/-infinity.
         * @type {boolean}
         */
        this.sentinel = false;
        /**
         * Marks regions where the upper or lower edge has changed, but we haven't
         * checked whether they intersect yet.
         * @type {boolean}
         */
        this.dirty = false;
        /**
         * marks temporary edges introduced when we process a "right vertex" (one
         * without any edges leaving to the right)
         * @type {boolean}
         */
        this.fixUpperEdge = false;
    };
    /**
     * Returns the ActiveRegion below this one.
     * @return {libtess.ActiveRegion}
     */
    libtess.ActiveRegion.prototype.regionBelow = function () {
        return this.nodeUp.getPredecessor().getKey();
    };
    /**
     * Returns the ActiveRegion above this one.
     * @return {libtess.ActiveRegion}
     */
    libtess.ActiveRegion.prototype.regionAbove = function () {
        return this.nodeUp.getSuccessor().getKey();
    };
    /* global libtess, module */
    /**
     * node.js export for non-compiled source
     */
    if (typeof module !== 'undefined') {
        module.exports = libtess;
    }
},
677: /* earcut/src/earcut.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.default = earcut;
    exports.deviation = deviation;
    exports.flatten = flatten;
    function earcut(data, holeIndices, dim = 2) {
        const hasHoles = holeIndices && holeIndices.length;
        const outerLen = hasHoles ? holeIndices[0] * dim : data.length;
        let outerNode = linkedList(data, 0, outerLen, dim, true);
        const triangles = [];
        if (!outerNode || outerNode.next === outerNode.prev)
            return triangles;
        let minX, minY, invSize;
        if (hasHoles)
            outerNode = eliminateHoles(data, holeIndices, outerNode, dim);
        // if the shape is not too simple, we'll use z-order curve hash later; calculate polygon bbox
        if (data.length > 80 * dim) {
            minX = data[0];
            minY = data[1];
            let maxX = minX;
            let maxY = minY;
            for (let i = dim; i < outerLen; i += dim) {
                const x = data[i];
                const y = data[i + 1];
                if (x < minX)
                    minX = x;
                if (y < minY)
                    minY = y;
                if (x > maxX)
                    maxX = x;
                if (y > maxY)
                    maxY = y;
            }
            // minX, minY and invSize are later used to transform coords into integers for z-order calculation
            invSize = Math.max(maxX - minX, maxY - minY);
            invSize = invSize !== 0 ? 32767 / invSize : 0;
        }
        earcutLinked(outerNode, triangles, dim, minX, minY, invSize, 0);
        return triangles;
    }
    // create a circular doubly linked list from polygon points in the specified winding order
    function linkedList(data, start, end, dim, clockwise) {
        let last;
        if (clockwise === (signedArea(data, start, end, dim) > 0)) {
            for (let i = start; i < end; i += dim)
                last = insertNode(i / dim | 0, data[i], data[i + 1], last);
        }
        else {
            for (let i = end - dim; i >= start; i -= dim)
                last = insertNode(i / dim | 0, data[i], data[i + 1], last);
        }
        if (last && equals(last, last.next)) {
            removeNode(last);
            last = last.next;
        }
        return last;
    }
    // eliminate colinear or duplicate points
    function filterPoints(start, end) {
        if (!start)
            return start;
        if (!end)
            end = start;
        let p = start, again;
        do {
            again = false;
            if (!p.steiner && (equals(p, p.next) || area(p.prev, p, p.next) === 0)) {
                removeNode(p);
                p = end = p.prev;
                if (p === p.next)
                    break;
                again = true;
            }
            else {
                p = p.next;
            }
        } while (again || p !== end);
        return end;
    }
    // main ear slicing loop which triangulates a polygon (given as a linked list)
    function earcutLinked(ear, triangles, dim, minX, minY, invSize, pass) {
        if (!ear)
            return;
        // interlink polygon nodes in z-order
        if (!pass && invSize)
            indexCurve(ear, minX, minY, invSize);
        let stop = ear;
        // iterate through ears, slicing them one by one
        while (ear.prev !== ear.next) {
            const prev = ear.prev;
            const next = ear.next;
            if (invSize ? isEarHashed(ear, minX, minY, invSize) : isEar(ear)) {
                triangles.push(prev.i, ear.i, next.i); // cut off the triangle
                removeNode(ear);
                // skipping the next vertex leads to less sliver triangles
                ear = next.next;
                stop = next.next;
                continue;
            }
            ear = next;
            // if we looped through the whole remaining polygon and can't find any more ears
            if (ear === stop) {
                // try filtering points and slicing again
                if (!pass) {
                    earcutLinked(filterPoints(ear), triangles, dim, minX, minY, invSize, 1);
                    // if this didn't work, try curing all small self-intersections locally
                }
                else if (pass === 1) {
                    ear = cureLocalIntersections(filterPoints(ear), triangles);
                    earcutLinked(ear, triangles, dim, minX, minY, invSize, 2);
                    // as a last resort, try splitting the remaining polygon into two
                }
                else if (pass === 2) {
                    splitEarcut(ear, triangles, dim, minX, minY, invSize);
                }
                break;
            }
        }
    }
    // check whether a polygon node forms a valid ear with adjacent nodes
    function isEar(ear) {
        const a = ear.prev, b = ear, c = ear.next;
        if (area(a, b, c) >= 0)
            return false; // reflex, can't be an ear
        // now make sure we don't have other points inside the potential ear
        const ax = a.x, bx = b.x, cx = c.x, ay = a.y, by = b.y, cy = c.y;
        // triangle bbox
        const x0 = Math.min(ax, bx, cx), y0 = Math.min(ay, by, cy), x1 = Math.max(ax, bx, cx), y1 = Math.max(ay, by, cy);
        let p = c.next;
        while (p !== a) {
            if (p.x >= x0 && p.x <= x1 && p.y >= y0 && p.y <= y1 &&
                pointInTriangleExceptFirst(ax, ay, bx, by, cx, cy, p.x, p.y) &&
                area(p.prev, p, p.next) >= 0)
                return false;
            p = p.next;
        }
        return true;
    }
    function isEarHashed(ear, minX, minY, invSize) {
        const a = ear.prev, b = ear, c = ear.next;
        if (area(a, b, c) >= 0)
            return false; // reflex, can't be an ear
        const ax = a.x, bx = b.x, cx = c.x, ay = a.y, by = b.y, cy = c.y;
        // triangle bbox
        const x0 = Math.min(ax, bx, cx), y0 = Math.min(ay, by, cy), x1 = Math.max(ax, bx, cx), y1 = Math.max(ay, by, cy);
        // z-order range for the current triangle bbox;
        const minZ = zOrder(x0, y0, minX, minY, invSize), maxZ = zOrder(x1, y1, minX, minY, invSize);
        let p = ear.prevZ, n = ear.nextZ;
        // look for points inside the triangle in both directions
        while (p && p.z >= minZ && n && n.z <= maxZ) {
            if (p.x >= x0 && p.x <= x1 && p.y >= y0 && p.y <= y1 && p !== a && p !== c &&
                pointInTriangleExceptFirst(ax, ay, bx, by, cx, cy, p.x, p.y) && area(p.prev, p, p.next) >= 0)
                return false;
            p = p.prevZ;
            if (n.x >= x0 && n.x <= x1 && n.y >= y0 && n.y <= y1 && n !== a && n !== c &&
                pointInTriangleExceptFirst(ax, ay, bx, by, cx, cy, n.x, n.y) && area(n.prev, n, n.next) >= 0)
                return false;
            n = n.nextZ;
        }
        // look for remaining points in decreasing z-order
        while (p && p.z >= minZ) {
            if (p.x >= x0 && p.x <= x1 && p.y >= y0 && p.y <= y1 && p !== a && p !== c &&
                pointInTriangleExceptFirst(ax, ay, bx, by, cx, cy, p.x, p.y) && area(p.prev, p, p.next) >= 0)
                return false;
            p = p.prevZ;
        }
        // look for remaining points in increasing z-order
        while (n && n.z <= maxZ) {
            if (n.x >= x0 && n.x <= x1 && n.y >= y0 && n.y <= y1 && n !== a && n !== c &&
                pointInTriangleExceptFirst(ax, ay, bx, by, cx, cy, n.x, n.y) && area(n.prev, n, n.next) >= 0)
                return false;
            n = n.nextZ;
        }
        return true;
    }
    // go through all polygon nodes and cure small local self-intersections
    function cureLocalIntersections(start, triangles) {
        let p = start;
        do {
            const a = p.prev, b = p.next.next;
            if (!equals(a, b) && intersects(a, p, p.next, b) && locallyInside(a, b) && locallyInside(b, a)) {
                triangles.push(a.i, p.i, b.i);
                // remove two nodes involved
                removeNode(p);
                removeNode(p.next);
                p = start = b;
            }
            p = p.next;
        } while (p !== start);
        return filterPoints(p);
    }
    // try splitting polygon into two and triangulate them independently
    function splitEarcut(start, triangles, dim, minX, minY, invSize) {
        // look for a valid diagonal that divides the polygon into two
        let a = start;
        do {
            let b = a.next.next;
            while (b !== a.prev) {
                if (a.i !== b.i && isValidDiagonal(a, b)) {
                    // split the polygon in two by the diagonal
                    let c = splitPolygon(a, b);
                    // filter colinear points around the cuts
                    a = filterPoints(a, a.next);
                    c = filterPoints(c, c.next);
                    // run earcut on each half
                    earcutLinked(a, triangles, dim, minX, minY, invSize, 0);
                    earcutLinked(c, triangles, dim, minX, minY, invSize, 0);
                    return;
                }
                b = b.next;
            }
            a = a.next;
        } while (a !== start);
    }
    // link every hole into the outer loop, producing a single-ring polygon without holes
    function eliminateHoles(data, holeIndices, outerNode, dim) {
        const queue = [];
        for (let i = 0, len = holeIndices.length; i < len; i++) {
            const start = holeIndices[i] * dim;
            const end = i < len - 1 ? holeIndices[i + 1] * dim : data.length;
            const list = linkedList(data, start, end, dim, false);
            if (list === list.next)
                list.steiner = true;
            queue.push(getLeftmost(list));
        }
        queue.sort(compareXYSlope);
        // process holes from left to right
        for (let i = 0; i < queue.length; i++) {
            outerNode = eliminateHole(queue[i], outerNode);
        }
        return outerNode;
    }
    function compareXYSlope(a, b) {
        let result = a.x - b.x;
        // when the left-most point of 2 holes meet at a vertex, sort the holes counterclockwise so that when we find
        // the bridge to the outer shell is always the point that they meet at.
        if (result === 0) {
            result = a.y - b.y;
            if (result === 0) {
                const aSlope = (a.next.y - a.y) / (a.next.x - a.x);
                const bSlope = (b.next.y - b.y) / (b.next.x - b.x);
                result = aSlope - bSlope;
            }
        }
        return result;
    }
    // find a bridge between vertices that connects hole with an outer ring and link it
    function eliminateHole(hole, outerNode) {
        const bridge = findHoleBridge(hole, outerNode);
        if (!bridge) {
            return outerNode;
        }
        const bridgeReverse = splitPolygon(bridge, hole);
        // filter collinear points around the cuts
        filterPoints(bridgeReverse, bridgeReverse.next);
        return filterPoints(bridge, bridge.next);
    }
    // David Eberly's algorithm for finding a bridge between hole and outer polygon
    function findHoleBridge(hole, outerNode) {
        let p = outerNode;
        const hx = hole.x;
        const hy = hole.y;
        let qx = -Infinity;
        let m;
        // find a segment intersected by a ray from the hole's leftmost point to the left;
        // segment's endpoint with lesser x will be potential connection point
        // unless they intersect at a vertex, then choose the vertex
        if (equals(hole, p))
            return p;
        do {
            if (equals(hole, p.next))
                return p.next;
            else if (hy <= p.y && hy >= p.next.y && p.next.y !== p.y) {
                const x = p.x + (hy - p.y) * (p.next.x - p.x) / (p.next.y - p.y);
                if (x <= hx && x > qx) {
                    qx = x;
                    m = p.x < p.next.x ? p : p.next;
                    if (x === hx)
                        return m; // hole touches outer segment; pick leftmost endpoint
                }
            }
            p = p.next;
        } while (p !== outerNode);
        if (!m)
            return null;
        // look for points inside the triangle of hole point, segment intersection and endpoint;
        // if there are no points found, we have a valid connection;
        // otherwise choose the point of the minimum angle with the ray as connection point
        const stop = m;
        const mx = m.x;
        const my = m.y;
        let tanMin = Infinity;
        p = m;
        do {
            if (hx >= p.x && p.x >= mx && hx !== p.x &&
                pointInTriangle(hy < my ? hx : qx, hy, mx, my, hy < my ? qx : hx, hy, p.x, p.y)) {
                const tan = Math.abs(hy - p.y) / (hx - p.x); // tangential
                if (locallyInside(p, hole) &&
                    (tan < tanMin || (tan === tanMin && (p.x > m.x || (p.x === m.x && sectorContainsSector(m, p)))))) {
                    m = p;
                    tanMin = tan;
                }
            }
            p = p.next;
        } while (p !== stop);
        return m;
    }
    // whether sector in vertex m contains sector in vertex p in the same coordinates
    function sectorContainsSector(m, p) {
        return area(m.prev, m, p.prev) < 0 && area(p.next, m, m.next) < 0;
    }
    // interlink polygon nodes in z-order
    function indexCurve(start, minX, minY, invSize) {
        let p = start;
        do {
            if (p.z === 0)
                p.z = zOrder(p.x, p.y, minX, minY, invSize);
            p.prevZ = p.prev;
            p.nextZ = p.next;
            p = p.next;
        } while (p !== start);
        p.prevZ.nextZ = null;
        p.prevZ = null;
        sortLinked(p);
    }
    // Simon Tatham's linked list merge sort algorithm
    // http://www.chiark.greenend.org.uk/~sgtatham/algorithms/listsort.html
    function sortLinked(list) {
        let numMerges;
        let inSize = 1;
        do {
            let p = list;
            let e;
            list = null;
            let tail = null;
            numMerges = 0;
            while (p) {
                numMerges++;
                let q = p;
                let pSize = 0;
                for (let i = 0; i < inSize; i++) {
                    pSize++;
                    q = q.nextZ;
                    if (!q)
                        break;
                }
                let qSize = inSize;
                while (pSize > 0 || (qSize > 0 && q)) {
                    if (pSize !== 0 && (qSize === 0 || !q || p.z <= q.z)) {
                        e = p;
                        p = p.nextZ;
                        pSize--;
                    }
                    else {
                        e = q;
                        q = q.nextZ;
                        qSize--;
                    }
                    if (tail)
                        tail.nextZ = e;
                    else
                        list = e;
                    e.prevZ = tail;
                    tail = e;
                }
                p = q;
            }
            tail.nextZ = null;
            inSize *= 2;
        } while (numMerges > 1);
        return list;
    }
    // z-order of a point given coords and inverse of the longer side of data bbox
    function zOrder(x, y, minX, minY, invSize) {
        // coords are transformed into non-negative 15-bit integer range
        x = (x - minX) * invSize | 0;
        y = (y - minY) * invSize | 0;
        x = (x | (x << 8)) & 0x00FF00FF;
        x = (x | (x << 4)) & 0x0F0F0F0F;
        x = (x | (x << 2)) & 0x33333333;
        x = (x | (x << 1)) & 0x55555555;
        y = (y | (y << 8)) & 0x00FF00FF;
        y = (y | (y << 4)) & 0x0F0F0F0F;
        y = (y | (y << 2)) & 0x33333333;
        y = (y | (y << 1)) & 0x55555555;
        return x | (y << 1);
    }
    // find the leftmost node of a polygon ring
    function getLeftmost(start) {
        let p = start, leftmost = start;
        do {
            if (p.x < leftmost.x || (p.x === leftmost.x && p.y < leftmost.y))
                leftmost = p;
            p = p.next;
        } while (p !== start);
        return leftmost;
    }
    // check if a point lies within a convex triangle
    function pointInTriangle(ax, ay, bx, by, cx, cy, px, py) {
        return (cx - px) * (ay - py) >= (ax - px) * (cy - py) &&
            (ax - px) * (by - py) >= (bx - px) * (ay - py) &&
            (bx - px) * (cy - py) >= (cx - px) * (by - py);
    }
    // check if a point lies within a convex triangle but false if its equal to the first point of the triangle
    function pointInTriangleExceptFirst(ax, ay, bx, by, cx, cy, px, py) {
        return !(ax === px && ay === py) && pointInTriangle(ax, ay, bx, by, cx, cy, px, py);
    }
    // check if a diagonal between two polygon nodes is valid (lies in polygon interior)
    function isValidDiagonal(a, b) {
        return a.next.i !== b.i && a.prev.i !== b.i && !intersectsPolygon(a, b) && // doesn't intersect other edges
            (locallyInside(a, b) && locallyInside(b, a) && middleInside(a, b) && // locally visible
                (area(a.prev, a, b.prev) || area(a, b.prev, b)) || // does not create opposite-facing sectors
                equals(a, b) && area(a.prev, a, a.next) > 0 && area(b.prev, b, b.next) > 0); // special zero-length case
    }
    // signed area of a triangle
    function area(p, q, r) {
        return (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
    }
    // check if two points are equal
    function equals(p1, p2) {
        return p1.x === p2.x && p1.y === p2.y;
    }
    // check if two segments intersect
    function intersects(p1, q1, p2, q2) {
        const o1 = sign(area(p1, q1, p2));
        const o2 = sign(area(p1, q1, q2));
        const o3 = sign(area(p2, q2, p1));
        const o4 = sign(area(p2, q2, q1));
        if (o1 !== o2 && o3 !== o4)
            return true; // general case
        if (o1 === 0 && onSegment(p1, p2, q1))
            return true; // p1, q1 and p2 are collinear and p2 lies on p1q1
        if (o2 === 0 && onSegment(p1, q2, q1))
            return true; // p1, q1 and q2 are collinear and q2 lies on p1q1
        if (o3 === 0 && onSegment(p2, p1, q2))
            return true; // p2, q2 and p1 are collinear and p1 lies on p2q2
        if (o4 === 0 && onSegment(p2, q1, q2))
            return true; // p2, q2 and q1 are collinear and q1 lies on p2q2
        return false;
    }
    // for collinear points p, q, r, check if point q lies on segment pr
    function onSegment(p, q, r) {
        return q.x <= Math.max(p.x, r.x) && q.x >= Math.min(p.x, r.x) && q.y <= Math.max(p.y, r.y) && q.y >= Math.min(p.y, r.y);
    }
    function sign(num) {
        return num > 0 ? 1 : num < 0 ? -1 : 0;
    }
    // check if a polygon diagonal intersects any polygon segments
    function intersectsPolygon(a, b) {
        let p = a;
        do {
            if (p.i !== a.i && p.next.i !== a.i && p.i !== b.i && p.next.i !== b.i &&
                intersects(p, p.next, a, b))
                return true;
            p = p.next;
        } while (p !== a);
        return false;
    }
    // check if a polygon diagonal is locally inside the polygon
    function locallyInside(a, b) {
        return area(a.prev, a, a.next) < 0 ?
            area(a, b, a.next) >= 0 && area(a, a.prev, b) >= 0 :
            area(a, b, a.prev) < 0 || area(a, a.next, b) < 0;
    }
    // check if the middle point of a polygon diagonal is inside the polygon
    function middleInside(a, b) {
        let p = a;
        let inside = false;
        const px = (a.x + b.x) / 2;
        const py = (a.y + b.y) / 2;
        do {
            if (((p.y > py) !== (p.next.y > py)) && p.next.y !== p.y &&
                (px < (p.next.x - p.x) * (py - p.y) / (p.next.y - p.y) + p.x))
                inside = !inside;
            p = p.next;
        } while (p !== a);
        return inside;
    }
    // link two polygon vertices with a bridge; if the vertices belong to the same ring, it splits polygon into two;
    // if one belongs to the outer ring and another to a hole, it merges it into a single ring
    function splitPolygon(a, b) {
        const a2 = createNode(a.i, a.x, a.y), b2 = createNode(b.i, b.x, b.y), an = a.next, bp = b.prev;
        a.next = b;
        b.prev = a;
        a2.next = an;
        an.prev = a2;
        b2.next = a2;
        a2.prev = b2;
        bp.next = b2;
        b2.prev = bp;
        return b2;
    }
    // create a node and optionally link it with previous one (in a circular doubly linked list)
    function insertNode(i, x, y, last) {
        const p = createNode(i, x, y);
        if (!last) {
            p.prev = p;
            p.next = p;
        }
        else {
            p.next = last.next;
            p.prev = last;
            last.next.prev = p;
            last.next = p;
        }
        return p;
    }
    function removeNode(p) {
        p.next.prev = p.prev;
        p.prev.next = p.next;
        if (p.prevZ)
            p.prevZ.nextZ = p.nextZ;
        if (p.nextZ)
            p.nextZ.prevZ = p.prevZ;
    }
    function createNode(i, x, y) {
        return {
            i, // vertex index in coordinates array
            x, y, // vertex coordinates
            prev: null, // previous and next vertex nodes in a polygon ring
            next: null,
            z: 0, // z-order curve value
            prevZ: null, // previous and next nodes in z-order
            nextZ: null,
            steiner: false // indicates whether this is a steiner point
        };
    }
    // return a percentage difference between the polygon area and its triangulation area;
    // used to verify correctness of triangulation
    function deviation(data, holeIndices, dim, triangles) {
        const hasHoles = holeIndices && holeIndices.length;
        const outerLen = hasHoles ? holeIndices[0] * dim : data.length;
        let polygonArea = Math.abs(signedArea(data, 0, outerLen, dim));
        if (hasHoles) {
            for (let i = 0, len = holeIndices.length; i < len; i++) {
                const start = holeIndices[i] * dim;
                const end = i < len - 1 ? holeIndices[i + 1] * dim : data.length;
                polygonArea -= Math.abs(signedArea(data, start, end, dim));
            }
        }
        let trianglesArea = 0;
        for (let i = 0; i < triangles.length; i += 3) {
            const a = triangles[i] * dim;
            const b = triangles[i + 1] * dim;
            const c = triangles[i + 2] * dim;
            trianglesArea += Math.abs((data[a] - data[c]) * (data[b + 1] - data[a + 1]) -
                (data[a] - data[b]) * (data[c + 1] - data[a + 1]));
        }
        return polygonArea === 0 && trianglesArea === 0 ? 0 :
            Math.abs((trianglesArea - polygonArea) / polygonArea);
    }
    function signedArea(data, start, end, dim) {
        let sum = 0;
        for (let i = start, j = end - dim; i < end; i += dim) {
            sum += (data[j] - data[i]) * (data[i + 1] + data[j + 1]);
            j = i;
        }
        return sum;
    }
    // turn a polygon in a multi-dimensional array form (e.g. as in GeoJSON) into a form Earcut accepts
    function flatten(data) {
        const vertices = [];
        const holes = [];
        const dimensions = data[0][0].length;
        let holeIndex = 0;
        let prevLen = 0;
        for (const ring of data) {
            for (const p of ring) {
                for (let d = 0; d < dimensions; d++)
                    vertices.push(p[d]);
            }
            if (prevLen) {
                holeIndex += prevLen;
                holes.push(holeIndex);
            }
            prevLen = ring.length;
        }
        return { vertices, holes, dimensions };
    }
},
678: /* models/glyphs/webgl/patches.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_1 = require(659) /* ./base */;
    const buffer_1 = require(660) /* ./buffer */;
    const line_1 = require(100) /* ../../../core/visuals/line */;
    const dash_cache_1 = require(643) /* ./dash_cache */;
    const base_line_1 = require(663) /* ./base_line */;
    const polygon_1 = require(673) /* ../../../core/util/polygon */;
    const polygon_2 = require(674) /* ./polygon */;
    class PatchesGL extends base_1.BaseGLGlyph {
        glyph;
        // Fill buffers
        _positions;
        _edge_distance;
        _elements = null;
        _total_element_count = 0;
        // Per-vertex visual buffers for polygon fill (divisor 0)
        _pv_fill_color = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _pv_hatch_patterns = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _pv_hatch_scales = new buffer_1.Float32Buffer(this.regl_wrapper);
        _pv_hatch_weights = new buffer_1.Float32Buffer(this.regl_wrapper);
        _pv_hatch_rgba = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        // Source visual buffers (scalar or per-polygon, from _set_visuals)
        _fill_color = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _have_hatch = false;
        _hatch_patterns = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _hatch_scales = new buffer_1.Float32Buffer(this.regl_wrapper);
        _hatch_weights = new buffer_1.Float32Buffer(this.regl_wrapper);
        _hatch_rgba = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        // Stroke buffers
        _line_points_buf;
        _line_show_buf;
        _length_so_far_buf;
        _linewidth = new buffer_1.Float32Buffer(this.regl_wrapper);
        _line_color = new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4);
        _line_cap = new buffer_1.Uint8Buffer(this.regl_wrapper);
        _line_join = new buffer_1.Uint8Buffer(this.regl_wrapper);
        // Dash state
        _is_dashed = false;
        _dash_tex = [];
        _dash_tex_info;
        _dash_scale;
        _dash_offset;
        // Per-polygon scalar draw buffers for stroke rendering.
        // Since geometry is re-uploaded per ring (line_offset = 0), per-polygon
        // vector visual properties are extracted into these scalar buffers.
        _draw_lw;
        _draw_lc;
        _draw_lcap;
        _draw_ljoin;
        _draw_dti;
        _draw_ds;
        _draw_do;
        _poly_data;
        _pv_dirty = true;
        _pv_elements = null;
        _topology;
        _topology_scales;
        _elements_signature = "";
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        // Issues one fill draw call per selected polygon and one stroke draw call
        // per ring per selected polygon. This matches the MultiLineGL pattern and
        // is necessary for correct selection/hover rendering, but may become a
        // bottleneck for plots with very many polygons.
        draw(indices, main_glyph, transform) {
            const main_patches = main_glyph;
            const main_gl = main_patches.glglyph;
            const derived_data_changed = this !== main_gl && this.data_changed;
            if (this.visuals_changed) {
                this._set_visuals();
                this.visuals_changed = false;
                this._pv_dirty = true;
            }
            const data_changed = main_gl.data_changed;
            const data_changed_or_mapped = data_changed || main_gl.data_mapped;
            if (data_changed_or_mapped) {
                main_gl._set_data(data_changed);
                main_gl.data_changed = false;
                main_gl.data_mapped = false;
                this._pv_dirty ||= data_changed || derived_data_changed;
            }
            if (this !== main_gl && (this.data_changed || this.data_mapped)) {
                this.data_changed = false;
                this.data_mapped = false;
                this._pv_dirty = true;
            }
            // Remapping can change the finite contours without changing source data.
            // Each visual variant must notice the resulting vertex layout change.
            if (this._pv_elements !== main_gl._elements) {
                this._pv_elements = main_gl._elements;
                this._pv_dirty = true;
            }
            if (main_gl._poly_data == null) {
                return;
            }
            const { width, height } = transform;
            const canvas_size = [width, height];
            const poly_data = main_gl._poly_data;
            // Expand visual buffers to per-vertex when visuals or data changed
            if (this._pv_dirty && poly_data.fill_nvertices.length > 0) {
                const vertex_counts = poly_data.fill_nvertices;
                (0, buffer_1.expand_to_per_vertex)(this._fill_color, this._pv_fill_color, vertex_counts, 4);
                if (this._have_hatch) {
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_patterns, this._pv_hatch_patterns, vertex_counts, 1);
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_scales, this._pv_hatch_scales, vertex_counts, 1);
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_weights, this._pv_hatch_weights, vertex_counts, 1);
                    (0, buffer_1.expand_to_per_vertex)(this._hatch_rgba, this._pv_hatch_rgba, vertex_counts, 4);
                }
                this._pv_dirty = false;
            }
            // Fill pass - draw each polygon separately to respect selection indices
            const fill_visuals = this.glyph.visuals.fill;
            if (fill_visuals.doit && main_gl._elements != null && main_gl._total_element_count > 0) {
                for (const i of indices) {
                    if (i >= poly_data.fill_element_counts.length) {
                        continue;
                    }
                    const count = poly_data.fill_element_counts[i];
                    if (count == 0) {
                        continue;
                    }
                    const offset = poly_data.fill_element_offsets[i];
                    if (this._have_hatch) {
                        this.regl_wrapper.polygon_hatch()({
                            scissor: this.regl_wrapper.scissor,
                            viewport: this.regl_wrapper.viewport,
                            canvas_size,
                            positions: main_gl._positions,
                            fill_color: this._pv_fill_color,
                            edge_distance: main_gl._edge_distance,
                            elements: main_gl._elements,
                            count,
                            offset,
                            antialias: polygon_1.POLYGON_AA_WIDTH / transform.pixel_ratio,
                            hatch_pattern: this._pv_hatch_patterns,
                            hatch_scale: this._pv_hatch_scales,
                            hatch_weight: this._pv_hatch_weights,
                            hatch_color: this._pv_hatch_rgba,
                        });
                    }
                    else {
                        this.regl_wrapper.polygon()({
                            scissor: this.regl_wrapper.scissor,
                            viewport: this.regl_wrapper.viewport,
                            canvas_size,
                            positions: main_gl._positions,
                            fill_color: this._pv_fill_color,
                            edge_distance: main_gl._edge_distance,
                            elements: main_gl._elements,
                            count,
                            offset,
                            antialias: polygon_1.POLYGON_AA_WIDTH / transform.pixel_ratio,
                        });
                    }
                }
            }
            // Stroke pass - draw each ring outline separately.
            // Geometry (points, show, length_so_far) is re-uploaded per ring, so
            // point_offset and line_offset are always 0. Per-polygon vector visual
            // properties are extracted into scalar draw buffers for each polygon.
            const line_visuals = this.glyph.visuals.line;
            if (line_visuals.doit) {
                for (const i of indices) {
                    if (i >= poly_data.line_rings.length) {
                        continue;
                    }
                    // Extract per-polygon visual values into scalar buffers
                    const linewidth = this._linewidth.extract_at(i, 1, this._draw_lw ??= new buffer_1.Float32Buffer(this.regl_wrapper));
                    const line_color = this._line_color.extract_at(i, 4, this._draw_lc ??= new buffer_1.NormalizedUint8Buffer(this.regl_wrapper, 4));
                    const line_cap = this._line_cap.extract_at(i, 1, this._draw_lcap ??= new buffer_1.Uint8Buffer(this.regl_wrapper));
                    const line_join = this._line_join.extract_at(i, 1, this._draw_ljoin ??= new buffer_1.Uint8Buffer(this.regl_wrapper));
                    let dash_tex_info;
                    let dash_scale;
                    let dash_offset;
                    const dash_i = Math.min(i, this._dash_tex.length - 1);
                    if (this._is_dashed && this._dash_tex[dash_i] != null) {
                        dash_tex_info = this._dash_tex_info.extract_at(i, 4, this._draw_dti ??= new buffer_1.Float32Buffer(this.regl_wrapper, 4));
                        dash_scale = this._dash_scale.extract_at(i, 1, this._draw_ds ??= new buffer_1.Float32Buffer(this.regl_wrapper));
                        dash_offset = this._dash_offset.extract_at(i, 1, this._draw_do ??= new buffer_1.Float32Buffer(this.regl_wrapper));
                    }
                    const rings = poly_data.line_rings[i];
                    for (const ring of rings) {
                        if (ring.nline < 2) {
                            continue;
                        }
                        const nsegments = ring.nline - 1;
                        const linewidth_value = linewidth.get_array()[0];
                        const scissor = this.regl_wrapper.scissor_for_points(ring.points, (0, base_line_1.line_bounds_padding)(linewidth_value), transform.pixel_ratio);
                        const [framebuffer, tex] = this.regl_wrapper.framebuffer_and_texture;
                        this.regl_wrapper.clear_framebuffer(framebuffer);
                        // Upload this ring's line data
                        if (this._line_points_buf == null) {
                            this._line_points_buf = new buffer_1.Float32Buffer(this.regl_wrapper);
                        }
                        const pts_array = this._line_points_buf.get_sized_array(ring.points.length);
                        pts_array.set(ring.points);
                        this._line_points_buf.update();
                        if (this._line_show_buf == null) {
                            this._line_show_buf = new buffer_1.Uint8Buffer(this.regl_wrapper);
                        }
                        const shw_array = this._line_show_buf.get_sized_array(ring.show.length);
                        shw_array.set(ring.show);
                        this._line_show_buf.update();
                        const solid_props = {
                            scissor,
                            viewport: this.regl_wrapper.viewport,
                            canvas_size,
                            antialias: base_line_1.LINE_AA_WIDTH / transform.pixel_ratio,
                            miter_limit: base_line_1.LINE_MITER_LIMIT,
                            points: this._line_points_buf,
                            show: this._line_show_buf,
                            nsegments,
                            linewidth,
                            line_color,
                            line_cap,
                            line_join,
                            framebuffer,
                            point_offset: 0,
                            line_offset: 0,
                        };
                        if (this._is_dashed && dash_tex_info != null) {
                            // Upload length_so_far for this ring
                            if (this._length_so_far_buf == null) {
                                this._length_so_far_buf = new buffer_1.Float32Buffer(this.regl_wrapper);
                            }
                            const lsf_array = this._length_so_far_buf.get_sized_array(ring.length_so_far.length);
                            lsf_array.set(ring.length_so_far);
                            this._length_so_far_buf.update();
                            const dashed_props = {
                                ...solid_props,
                                length_so_far: this._length_so_far_buf,
                                dash_tex: this._dash_tex[dash_i],
                                dash_tex_info,
                                dash_scale: dash_scale,
                                dash_offset: dash_offset,
                            };
                            this.regl_wrapper.dashed_line()(dashed_props);
                        }
                        else {
                            this.regl_wrapper.solid_line()(solid_props);
                        }
                        const accumulate_props = {
                            scissor,
                            viewport: this.regl_wrapper.viewport,
                            framebuffer_tex: tex,
                        };
                        this.regl_wrapper.accumulate()(accumulate_props);
                    }
                }
            }
        }
        _set_data(data_changed = true) {
            const { sxs, sys } = this.glyph;
            const npoly = this.glyph.data_size;
            const { scales } = this.glyph.renderer.coordinates;
            // Changing scale types is not an affine remapping of cached intersections.
            const scales_changed = scales.some((scale, i) => scale !== this._topology_scales?.[i]);
            this._topology_scales = scales;
            const topology_changed = data_changed || scales_changed || this._topology == null || this._topology.length != npoly;
            let elements_changed = topology_changed;
            if (topology_changed) {
                this._topology = new Array(npoly).fill(null);
            }
            const per_poly = new Array(npoly);
            const fill_nvertices = new Array(npoly);
            const fill_element_offsets = new Array(npoly);
            const fill_element_counts = new Array(npoly);
            const line_rings = new Array(npoly);
            const active_topology = [];
            let total_coords = 0;
            let total_elements = 0;
            for (let i = 0; i < npoly; i++) {
                const sx = sxs.get(i);
                const sy = sys.get(i);
                const rings = (0, polygon_1.split_rings)(sx, sy);
                line_rings[i] = [];
                if (rings.length > 0) {
                    let topology = this._topology[i];
                    if (topology_changed || topology == null || !topology.matches(rings)) {
                        elements_changed = true;
                        topology = (0, polygon_2.try_create_polygon_topology)(rings);
                        this._topology[i] = topology;
                    }
                    const group_results = topology?.geometries(rings) ?? [];
                    active_topology.push(group_results.map((geom) => `${geom.nvertices}:${geom.indices.length}`).join(","));
                    let poly_nvertices = 0;
                    let poly_elements = 0;
                    for (const geom of group_results) {
                        poly_nvertices += geom.nvertices;
                        poly_elements += geom.indices.length;
                    }
                    per_poly[i] = { groups: group_results, all_rings: rings };
                    fill_nvertices[i] = poly_nvertices;
                    fill_element_offsets[i] = total_elements;
                    fill_element_counts[i] = poly_elements;
                    total_coords += poly_nvertices * 2;
                    total_elements += poly_elements;
                }
                else {
                    active_topology.push("");
                    if (data_changed) {
                        this._topology[i] = null;
                    }
                    per_poly[i] = null;
                    fill_nvertices[i] = 0;
                    fill_element_offsets[i] = total_elements;
                    fill_element_counts[i] = 0;
                }
            }
            // Pass 2: copy per-polygon results directly into destination buffers.
            const total_vertices = total_coords / 2;
            if (this._positions == null) {
                this._positions = new buffer_1.Float32Buffer(this.regl_wrapper, 2);
            }
            const pos_array = this._positions.get_sized_array(total_coords);
            if (this._edge_distance == null) {
                this._edge_distance = new buffer_1.Float32Buffer(this.regl_wrapper);
            }
            const ed_array = this._edge_distance.get_sized_array(total_vertices);
            const elements_signature = active_topology.join(";");
            elements_changed ||= elements_signature != this._elements_signature;
            const elem_array = elements_changed || this._elements == null ? new Uint32Array(total_elements) : null;
            let pos_offset = 0;
            let ed_offset = 0;
            let elem_offset = 0;
            let vertex_offset = 0;
            for (let i = 0; i < npoly; i++) {
                const result = per_poly[i];
                if (result == null) {
                    continue;
                }
                const { groups, all_rings } = result;
                for (const geom of groups) {
                    pos_array.set(geom.positions, pos_offset);
                    pos_offset += geom.positions.length;
                    ed_array.set(geom.edge_distance, ed_offset);
                    ed_offset += geom.edge_distance.length;
                    // Offset indices by vertex_offset for merged buffer
                    if (elem_array != null) {
                        for (let j = 0; j < geom.indices.length; j++) {
                            elem_array[elem_offset + j] = geom.indices[j] + vertex_offset;
                        }
                    }
                    elem_offset += geom.indices.length;
                    vertex_offset += geom.nvertices;
                }
                // Build line data for all rings (outer boundary + holes + disjoint)
                const ring_line_data = [];
                for (const ring of all_rings) {
                    const data = (0, polygon_1.build_line_from_ring)(ring);
                    if (data.nline > 0) {
                        ring_line_data.push(data);
                    }
                }
                line_rings[i] = ring_line_data;
            }
            this._poly_data = {
                line_rings,
                fill_nvertices,
                fill_element_offsets,
                fill_element_counts,
            };
            this._positions.update();
            this._edge_distance.update();
            // Upload merged element buffer
            this._total_element_count = total_elements;
            if (elem_array != null) {
                this._elements?.destroy();
                if (total_elements > 0) {
                    this._elements = this.regl_wrapper.elements({
                        usage: "static",
                        primitive: "triangles",
                        data: elem_array,
                        type: "uint32",
                    });
                }
                else {
                    this._elements = null;
                }
            }
            this._elements_signature = elements_signature;
        }
        _set_visuals() {
            const fill_visuals = this.glyph.visuals.fill;
            this._fill_color.set_from_color(fill_visuals.fill_color, fill_visuals.fill_alpha);
            const line_visuals = this.glyph.visuals.line;
            this._line_color.set_from_color(line_visuals.line_color, line_visuals.line_alpha);
            this._linewidth.set_from_prop(line_visuals.line_width);
            this._line_cap.set_from_line_cap(line_visuals.line_cap);
            this._line_join.set_from_line_join(line_visuals.line_join);
            // Dash detection
            const { line_dash } = line_visuals;
            const n = line_dash.is_Scalar() ? 1 : line_dash.length;
            const patterns = new Array(n);
            this._is_dashed = false;
            for (let i = 0; i < n; i++) {
                const pattern = (0, dash_cache_1.normalize_dash_pattern)((0, line_1.resolve_line_dash)(line_dash.get(i)));
                patterns[i] = pattern;
                this._is_dashed ||= pattern.length != 0;
            }
            this._dash_tex = [];
            if (this._is_dashed) {
                if (this._dash_offset == null) {
                    this._dash_offset = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                this._dash_offset.set_from_prop(line_visuals.line_dash_offset);
                if (this._dash_tex_info == null) {
                    this._dash_tex_info = new buffer_1.Float32Buffer(this.regl_wrapper, 4);
                }
                const dash_tex_info = this._dash_tex_info.get_sized_array(4 * n);
                if (this._dash_scale == null) {
                    this._dash_scale = new buffer_1.Float32Buffer(this.regl_wrapper);
                }
                const dash_scale = this._dash_scale.get_sized_array(n);
                for (let i = 0; i < n; i++) {
                    const arr = patterns[i];
                    if (arr.length > 0) {
                        const [tex_info, tex, scale] = this.regl_wrapper.get_dash(arr);
                        this._dash_tex.push(tex);
                        for (let j = 0; j < 4; j++) {
                            dash_tex_info[4 * i + j] = tex_info[j];
                        }
                        dash_scale[i] = scale;
                    }
                    else {
                        this._dash_tex.push(null);
                        dash_tex_info.fill(0, 4 * i, 4 * (i + 1));
                        dash_scale[i] = 0;
                    }
                }
                // Mark scalar so that to_attribute_config_nested always uses offset 0,
                // consistent with line_offset: 0 in the draw call.
                const dash_is_scalar = line_dash.is_Scalar();
                this._dash_tex_info.update(dash_is_scalar);
                this._dash_scale.update(dash_is_scalar);
            }
            const hatch_visuals = this.glyph.visuals.hatch;
            this._have_hatch = hatch_visuals.doit;
            if (this._have_hatch) {
                this._hatch_patterns.set_from_hatch_pattern(hatch_visuals.hatch_pattern);
                this._hatch_scales.set_from_prop(hatch_visuals.hatch_scale);
                this._hatch_weights.set_from_prop(hatch_visuals.hatch_weight);
                this._hatch_rgba.set_from_color(hatch_visuals.hatch_color, hatch_visuals.hatch_alpha);
            }
        }
    }
    exports.PatchesGL = PatchesGL;
},
679: /* models/glyphs/webgl/multi_marker.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const base_marker_1 = require(658) /* ./base_marker */;
    const webgl_utils_1 = require(661) /* ./webgl_utils */;
    const enums_1 = require(21) /* ../../../core/enums */;
    const buffer_1 = require(660) /* ./buffer */;
    class MultiMarkerGL extends base_marker_1.BaseMarkerGL {
        glyph;
        // data properties, either all or none are set.
        _marker_types;
        _unique_marker_types;
        _show_by_type = new Map();
        _nshow_by_type = new Map();
        _show_marker_types;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        draw(indices, main_glyph, transform) {
            // The main glyph has the data, this glyph has the visuals.
            const main_gl_glyph = main_glyph.glglyph;
            const main_data_changed = main_gl_glyph.data_changed;
            if (main_data_changed || main_gl_glyph.data_mapped) {
                main_gl_glyph.set_data(main_data_changed);
                main_gl_glyph.data_changed = false;
                main_gl_glyph.data_mapped = false;
            }
            const derived_data_changed = this.data_changed;
            if (this !== main_gl_glyph && (derived_data_changed || this.data_mapped)) {
                this.set_data(derived_data_changed);
                this.data_changed = false;
                this.data_mapped = false;
            }
            if (this.visuals_changed) {
                this._set_visuals();
                this.visuals_changed = false;
            }
            const nmarkers = main_gl_glyph.nvertices;
            const marker_gl = this !== main_gl_glyph && this._marker_types != null ? this : main_gl_glyph;
            const marker_types = marker_gl._marker_types;
            const rebuild_show = main_data_changed || derived_data_changed || this._show_nmarkers != nmarkers ||
                this._show_marker_types !== marker_types || this._have_indices_changed(indices);
            if (rebuild_show) {
                this._nshow_by_type.clear();
                const is_single_marker_type = marker_types.is_scalar;
                if (is_single_marker_type) {
                    const single_marker_type = marker_gl._unique_marker_types[0];
                    if (single_marker_type != null) {
                        const buffer = this._show_by_type.has(single_marker_type) ? this._show_by_type.get(single_marker_type) : new buffer_1.Uint8Buffer(this.regl_wrapper);
                        const array = buffer.get_sized_array(nmarkers).fill(0);
                        for (let i = 0; i < indices.length; i++) {
                            array[indices[i]] = 255;
                        }
                        this._show_by_type.set(single_marker_type, buffer);
                        this._nshow_by_type.set(single_marker_type, indices.length);
                    }
                }
                else {
                    for (const buffer of this._show_by_type.values()) {
                        buffer.get_sized_array(nmarkers).fill(0);
                    }
                    for (const marker_type of marker_gl._unique_marker_types) {
                        if (marker_type != null && !this._show_by_type.has(marker_type)) {
                            const buffer = new buffer_1.Uint8Buffer(this.regl_wrapper);
                            buffer.get_sized_array(nmarkers).fill(0);
                            this._show_by_type.set(marker_type, buffer);
                        }
                    }
                    for (const index of indices) {
                        const marker_type = marker_types.get(index);
                        if (enums_1.MarkerType.valid(marker_type)) {
                            this._show_by_type.get(marker_type).get_sized_array(nmarkers)[index] = 255;
                            this._nshow_by_type.set(marker_type, (this._nshow_by_type.get(marker_type) ?? 0) + 1);
                        }
                    }
                }
                for (const buffer of this._show_by_type.values()) {
                    buffer.update();
                }
                this._show_indices = indices.slice();
                this._show_nmarkers = nmarkers;
                this._show_marker_types = marker_types;
            }
            for (const marker_type of marker_gl._unique_marker_types) {
                if (marker_type == null || this._nshow_by_type.get(marker_type) == null) {
                    continue;
                }
                this._draw_one_marker_type(marker_type, transform, main_gl_glyph, this._show_by_type.get(marker_type));
            }
        }
        _get_visuals() {
            return this.glyph.visuals;
        }
        _set_data(data_changed = true) {
            const nmarkers = this.nvertices;
            // Always update positions, sizes, and angles (for streaming updates)
            const centers_array = this._centers.get_sized_array(2 * nmarkers);
            (0, webgl_utils_1.interleave)(this.glyph.sx, this.glyph.sy, nmarkers, base_marker_1.BaseMarkerGL.missing_point, centers_array);
            this._centers.update();
            this._widths.set_from_prop(this.glyph.size);
            this._angles.set_from_prop(this.glyph.angle);
            if (data_changed || this._marker_types == null) {
                this._marker_types = this.glyph.marker;
                this._unique_marker_types = this._marker_types.unique().filter((marker) => enums_1.MarkerType.valid(marker));
            }
        }
        _set_once() {
            super._set_once();
            this._heights.set_from_scalar(0);
            this._auxs.set_from_scalar(0);
        }
    }
    exports.MultiMarkerGL = MultiMarkerGL;
},
680: /* models/glyphs/webgl/ngon.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const radial_1 = require(665) /* ./radial */;
    class NgonGL extends radial_1.RadialGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return "ngon";
        }
        _set_data() {
            super._set_data();
            this._angles.set_from_prop(this.glyph.angle);
            this._auxs.set_from_prop(this.glyph.n);
        }
    }
    exports.NgonGL = NgonGL;
},
681: /* models/glyphs/webgl/rect.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const sxsy_1 = require(656) /* ./sxsy */;
    class RectGL extends sxsy_1.SXSYGlyphGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return this._border_radius_nonzero ? "round_rect" : "rect";
        }
        _set_data() {
            super._set_data();
            this._widths.set_from_array(this.glyph.swidth);
            this._heights.set_from_array(this.glyph.sheight);
            this._angles.set_from_prop(this.glyph.angle);
            const { top_left, top_right, bottom_right, bottom_left } = this.glyph.border_radius;
            this._border_radius = [top_left, top_right, bottom_right, bottom_left];
            this._border_radius_nonzero = Math.max(...this._border_radius) > 0.0;
        }
        _set_once() {
            super._set_once();
            this._auxs.set_from_scalar(0);
        }
    }
    exports.RectGL = RectGL;
},
682: /* models/glyphs/webgl/step.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const buffer_1 = require(660) /* ./buffer */;
    const single_line_1 = require(669) /* ./single_line */;
    const assert_1 = require(13) /* ../../../core/util/assert */;
    class StepGL extends single_line_1.SingleLineGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        draw(indices, main_glyph, transform) {
            this._draw_impl(indices, transform, main_glyph.glglyph);
        }
        _get_show_buffer(indices, main_gl_glyph) {
            const main_show = main_gl_glyph._show;
            let show = main_show;
            const mode = this.glyph.model.mode;
            const n = main_show.length;
            const { pad_before, pad_after } = this.glyph.model;
            const num_pad_points = (pad_before != 0 ? 1 : 0) + (pad_after != 0 ? 1 : 0);
            const nstep_points = n - 1 - num_pad_points;
            const expected_full_length = mode == "center" ? (nstep_points + 2) / 3 : (nstep_points + 1) / 2;
            if (indices.length != expected_full_length) {
                const main_show_array = main_show.get_sized_array(n); // equal to npoints+1
                if (this._show == null) {
                    this._show = new buffer_1.Uint8Buffer(this.regl_wrapper);
                }
                const show_array = this._show.get_sized_array(n);
                show_array.fill(0);
                const offset = mode == "center" ? 1 : 0;
                const idx_offset = pad_before != 0 ? 1 : 0;
                if (indices.length > 1) {
                    for (let k = 0; k < indices.length; k++) {
                        const i = indices[k];
                        const inext = indices[k + 1];
                        const idx = i * (2 + offset) + 1 + idx_offset;
                        if (i == inext - 1) {
                            show_array[idx] = main_show_array[idx];
                            show_array[idx + 1] = main_show_array[idx + 1];
                            show_array[idx + 1 + offset] = main_show_array[idx + 1 + offset];
                        }
                    }
                }
                this._show.update();
                show = this._show;
            }
            return show;
        }
        _get_visuals() {
            return this.glyph.visuals.line;
        }
        _set_data_points() {
            const sx = this.glyph.sx;
            const sy = this.glyph.sy;
            const mode = this.glyph.model.mode;
            const { pad_before, pad_after } = this.glyph.model;
            const npoints = sx.length;
            const is_closed = (npoints > 2 && sx[0] == sx[npoints - 1] && sy[0] == sy[npoints - 1] &&
                isFinite(sx[0]) && isFinite(sy[0]));
            const nstep_points = mode == "center" ? 3 * npoints - 2 : 2 * npoints - 1;
            const total_points = nstep_points + (pad_before != 0 ? 1 : 0) + (pad_after != 0 ? 1 : 0);
            if (this._points == null) {
                this._points = new buffer_1.Float32Buffer(this.regl_wrapper);
            }
            const points_array = this._points.get_sized_array((total_points + 2) * 2);
            // WebGL renderer needs just one of (x, y) coordinates of inserted step points
            // to be NaN for it to be rendered correctly.
            let j = 2;
            if (pad_before != 0) {
                const pad_sx = this.glyph.renderer.xscale.s_compute(this.glyph.x[0] - pad_before);
                points_array[j++] = pad_sx;
                points_array[j++] = sy[0];
            }
            let is_finite = isFinite(sx[0] + sy[0]);
            points_array[j++] = is_finite ? sx[0] : NaN;
            points_array[j++] = sy[0];
            for (let i = 0; i < npoints - 1; i++) {
                const next_finite = isFinite(sx[i + 1] + sy[i + 1]);
                switch (mode) {
                    case "before":
                        points_array[j++] = is_finite && next_finite ? sx[i] : NaN;
                        points_array[j++] = sy[i + 1];
                        points_array[j++] = next_finite ? sx[i + 1] : NaN;
                        points_array[j++] = sy[i + 1];
                        break;
                    case "after":
                        points_array[j++] = is_finite && next_finite ? sx[i + 1] : NaN;
                        points_array[j++] = sy[i];
                        points_array[j++] = next_finite ? sx[i + 1] : NaN;
                        points_array[j++] = sy[i + 1];
                        break;
                    case "center":
                        if (is_finite && next_finite) {
                            const midx = (sx[i] + sx[i + 1]) / 2;
                            points_array[j++] = midx;
                            points_array[j++] = sy[i];
                            points_array[j++] = midx;
                            points_array[j++] = sy[i + 1];
                            points_array[j++] = sx[i + 1];
                            points_array[j++] = sy[i + 1];
                        }
                        else {
                            points_array[j++] = is_finite ? sx[i] : NaN;
                            points_array[j++] = sy[i];
                            points_array[j++] = NaN;
                            points_array[j++] = NaN;
                            points_array[j++] = next_finite ? sx[i + 1] : NaN;
                            points_array[j++] = sy[i + 1];
                        }
                        break;
                    default:
                        (0, assert_1.unreachable)();
                }
                is_finite = next_finite;
            }
            if (pad_after != 0) {
                const pad_sx = this.glyph.renderer.xscale.s_compute(this.glyph.x[npoints - 1] + pad_after);
                points_array[j++] = pad_sx;
                points_array[j++] = sy[npoints - 1];
            }
            (0, assert_1.assert)(j == total_points * 2 + 2);
            if (is_closed) {
                points_array[0] = points_array[2 * total_points - 2]; // Last but one point.
                points_array[1] = points_array[2 * total_points - 1];
                points_array[2 * total_points + 2] = points_array[4]; // Second point.
                points_array[2 * total_points + 3] = points_array[5];
            }
            else {
                // These are never used by the WebGL shaders, but setting to zero anyway.
                points_array[0] = 0.0;
                points_array[1] = 0.0;
                points_array[2 * total_points + 2] = 0.0;
                points_array[2 * total_points + 3] = 0.0;
            }
            this._points.update();
            return points_array;
        }
    }
    exports.StepGL = StepGL;
},
683: /* models/glyphs/webgl/wedge.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const sxsy_1 = require(656) /* ./sxsy */;
    class WedgeGL extends sxsy_1.SXSYGlyphGL {
        glyph;
        constructor(regl_wrapper, glyph) {
            super(regl_wrapper, glyph);
            this.glyph = glyph;
        }
        get marker_type() {
            return "wedge";
        }
        get radius() {
            return this._widths;
        }
        get start_angle() {
            return this._angles;
        }
        get end_angle() {
            return this._auxs;
        }
        _set_data() {
            super._set_data();
            this.radius.set_from_array(this.glyph.sradius);
            if (this.glyph.model.direction == "anticlock") {
                this.start_angle.set_from_prop(this.glyph.start_angle);
                this.end_angle.set_from_prop(this.glyph.end_angle);
            }
            else {
                this.start_angle.set_from_prop(this.glyph.end_angle);
                this.end_angle.set_from_prop(this.glyph.start_angle);
            }
        }
        _set_once() {
            super._set_once();
            this._heights.set_from_scalar(0);
        }
    }
    exports.WedgeGL = WedgeGL;
},
}, 639, {"models/glyphs/webgl/main":639,"models/glyphs/webgl/index":640,"models/glyphs/webgl/regl_wrap":641,"models/glyphs/webgl/dash_cache":643,"models/glyphs/webgl/utils/math":644,"models/glyphs/webgl/accumulate.vert":645,"models/glyphs/webgl/accumulate.frag":646,"models/glyphs/webgl/image.vert":647,"models/glyphs/webgl/image.frag":648,"models/glyphs/webgl/regl_line.vert":649,"models/glyphs/webgl/regl_line.frag":650,"models/glyphs/webgl/marker.vert":651,"models/glyphs/webgl/marker.frag":652,"models/glyphs/webgl/polygon.vert":653,"models/glyphs/webgl/polygon.frag":654,"models/glyphs/webgl/annular_wedge":655,"models/glyphs/webgl/sxsy":656,"models/glyphs/webgl/single_marker":657,"models/glyphs/webgl/base_marker":658,"models/glyphs/webgl/base":659,"models/glyphs/webgl/buffer":660,"models/glyphs/webgl/webgl_utils":661,"models/glyphs/webgl/annulus":662,"models/glyphs/webgl/base_line":663,"models/glyphs/webgl/circle":664,"models/glyphs/webgl/radial":665,"models/glyphs/webgl/hex_tile":666,"models/glyphs/webgl/image":667,"models/glyphs/webgl/line_gl":668,"models/glyphs/webgl/single_line":669,"models/glyphs/webgl/lrtb":670,"models/glyphs/webgl/multi_line":671,"models/glyphs/webgl/patch":672,"core/util/polygon":673,"models/glyphs/webgl/polygon":674,"models/glyphs/webgl/tessellator":675,"models/glyphs/webgl/patches":678,"models/glyphs/webgl/multi_marker":679,"models/glyphs/webgl/ngon":680,"models/glyphs/webgl/rect":681,"models/glyphs/webgl/step":682,"models/glyphs/webgl/wedge":683}, {});});
//# sourceMappingURL=bokeh-gl.js.map
