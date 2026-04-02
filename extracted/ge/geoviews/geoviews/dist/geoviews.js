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
  factory(root["Bokeh"], undefined);
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
"c764d38756": /* index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const GeoViews = tslib_1.__importStar(require("2e3df39bba") /* ./models */);
    exports.GeoViews = GeoViews;
    const base_1 = require("@bokehjs/base");
    (0, base_1.register_models)(GeoViews);
},
"2e3df39bba": /* models/index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    var checkpoint_tool_1 = require("49636d3eef") /* ./checkpoint_tool */;
    __esExport("CheckpointTool", checkpoint_tool_1.CheckpointTool);
    var clear_tool_1 = require("356402dee7") /* ./clear_tool */;
    __esExport("ClearTool", clear_tool_1.ClearTool);
    var poly_draw_1 = require("c03d81e6d5") /* ./poly_draw */;
    __esExport("PolyVertexDrawTool", poly_draw_1.PolyVertexDrawTool);
    var poly_edit_1 = require("238deef1f5") /* ./poly_edit */;
    __esExport("PolyVertexEditTool", poly_edit_1.PolyVertexEditTool);
    var restore_tool_1 = require("1a96add9eb") /* ./restore_tool */;
    __esExport("RestoreTool", restore_tool_1.RestoreTool);
    var wind_barb_1 = require("028985dc77") /* ./wind_barb */;
    __esExport("WindBarb", wind_barb_1.WindBarb);
},
"49636d3eef": /* models/checkpoint_tool.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const object_1 = require("@bokehjs/core/util/object");
    const array_1 = require("@bokehjs/core/util/array");
    const action_tool_1 = require("@bokehjs/models/tools/actions/action_tool");
    const column_data_source_1 = require("@bokehjs/models/sources/column_data_source");
    const icons_css_1 = require("@bokehjs/styles/icons.css");
    class CheckpointToolView extends action_tool_1.ActionToolView {
        doit() {
            const sources = this.model.sources;
            for (const source of sources) {
                if (source.buffer == null) {
                    source.buffer = [];
                }
                const data_copy = {};
                for (const [key, column] of (0, object_1.entries)(source.data)) {
                    const new_column = [];
                    for (const arr of column) {
                        if (Array.isArray(arr) || ArrayBuffer.isView(arr)) {
                            new_column.push((0, array_1.copy)(arr));
                        }
                        else {
                            new_column.push(arr);
                        }
                    }
                    data_copy[key] = new_column;
                }
                source.buffer.push(data_copy);
            }
        }
    }
    exports.CheckpointToolView = CheckpointToolView;
    CheckpointToolView.__name__ = "CheckpointToolView";
    class CheckpointTool extends action_tool_1.ActionTool {
        constructor(attrs) {
            super(attrs);
            this.tool_name = "Checkpoint";
            this.tool_icon = icons_css_1.tool_icon_save;
        }
    }
    exports.CheckpointTool = CheckpointTool;
    _a = CheckpointTool;
    CheckpointTool.__name__ = "CheckpointTool";
    CheckpointTool.__module__ = "geoviews.models.custom_tools";
    (() => {
        _a.prototype.default_view = CheckpointToolView;
        _a.define(({ List, Ref }) => ({
            sources: [List(Ref(column_data_source_1.ColumnDataSource)), []],
        }));
    })();
},
"356402dee7": /* models/clear_tool.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const action_tool_1 = require("@bokehjs/models/tools/actions/action_tool");
    const column_data_source_1 = require("@bokehjs/models/sources/column_data_source");
    const icons_css_1 = require("@bokehjs/styles/icons.css");
    class ClearToolView extends action_tool_1.ActionToolView {
        doit() {
            for (const source of this.model.sources) {
                source.clear();
            }
        }
    }
    exports.ClearToolView = ClearToolView;
    ClearToolView.__name__ = "ClearToolView";
    class ClearTool extends action_tool_1.ActionTool {
        constructor(attrs) {
            super(attrs);
            this.tool_name = "Clear data";
            this.tool_icon = icons_css_1.tool_icon_reset;
        }
    }
    exports.ClearTool = ClearTool;
    _a = ClearTool;
    ClearTool.__name__ = "ClearTool";
    ClearTool.__module__ = "geoviews.models.custom_tools";
    (() => {
        _a.prototype.default_view = ClearToolView;
        _a.define(({ List, Ref }) => ({
            sources: [List(Ref(column_data_source_1.ColumnDataSource)), []],
        }));
    })();
},
"c03d81e6d5": /* models/poly_draw.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const vectorization_1 = require("@bokehjs/core/vectorization");
    const object_1 = require("@bokehjs/core/util/object");
    const types_1 = require("@bokehjs/core/util/types");
    const assert_1 = require("@bokehjs/core/util/assert");
    const poly_draw_tool_1 = require("@bokehjs/models/tools/edit/poly_draw_tool");
    class PolyVertexDrawToolView extends poly_draw_tool_1.PolyDrawToolView {
        _split_path(x, y) {
            for (const renderer of this.model.renderers) {
                const glyph = renderer.glyph;
                const cds = renderer.data_source;
                const [xkey, ykey] = [glyph.xs.field, glyph.ys.field];
                const xpaths = cds.data[xkey];
                const ypaths = cds.data[ykey];
                for (let index = 0; index < xpaths.length; index++) {
                    let xs = xpaths[index];
                    if (!(0, types_1.isArray)(xs)) {
                        xs = Array.from(xs);
                        cds.data[xkey][index] = xs;
                    }
                    let ys = ypaths[index];
                    if (!(0, types_1.isArray)(ys)) {
                        ys = Array.from(ys);
                        cds.data[ykey][index] = ys;
                    }
                    for (let i = 0; i < xs.length; i++) {
                        if ((xs[i] == x) && (ys[i] == y) && (i != 0) && (i != (xs.length - 1))) {
                            xpaths.splice(index + 1, 0, xs.slice(i));
                            ypaths.splice(index + 1, 0, ys.slice(i));
                            xs.splice(i + 1);
                            ys.splice(i + 1);
                            for (const column of cds.columns()) {
                                if ((column !== xkey) && (column != ykey)) {
                                    cds.data[column].splice(index + 1, 0, cds.data[column][index]);
                                }
                            }
                            return;
                        }
                    }
                }
            }
        }
        _snap_to_vertex(ev, x, y) {
            const { vertex_renderer } = this.model;
            if (vertex_renderer != null) {
                // If an existing vertex is hit snap to it
                const vertex_selected = this._select_event(ev, "replace", [vertex_renderer]);
                const point_ds = vertex_renderer.data_source;
                // Type once dataspecs are typed
                const point_glyph = vertex_renderer.glyph;
                const [pxkey, pykey] = [point_glyph.x.field, point_glyph.y.field];
                if (vertex_selected.length > 0) {
                    // If existing vertex is hit split path at that location
                    // converting to feature vertex
                    const index = point_ds.selected.indices[0];
                    if (pxkey) {
                        x = point_ds.get(pxkey)[index];
                    }
                    if (pykey) {
                        y = point_ds.get(pykey)[index];
                    }
                    if (ev.type != "move") {
                        this._split_path(x, y);
                    }
                    point_ds.selection_manager.clear();
                }
            }
            return [x, y];
        }
        _set_vertices(xs, ys, styles) {
            const { vertex_renderer } = this.model;
            if (vertex_renderer == null) {
                return;
            }
            const point_glyph = vertex_renderer.glyph;
            const point_cds = vertex_renderer.data_source;
            const [pxkey, pykey] = [point_glyph.x.field, point_glyph.y.field];
            if (pxkey) {
                if ((0, types_1.isArray)(xs)) {
                    point_cds.set(pxkey, xs);
                }
                else {
                    point_glyph.x = { value: xs };
                }
            }
            if (pykey) {
                if ((0, types_1.isArray)(ys)) {
                    point_cds.set(pykey, ys);
                }
                else {
                    point_glyph.y = { value: ys };
                }
            }
            if (styles != null) {
                for (const key of (0, object_1.keys)(styles)) {
                    point_cds.set(key, styles[key]);
                    point_glyph[key] = { field: key };
                }
            }
            else {
                for (const col of point_cds.columns()) {
                    point_cds.set(col, []);
                }
            }
            this._emit_cds_changes(point_cds, true, true, false);
        }
        _show_vertices() {
            if (!this.model.active) {
                return;
            }
            const { renderers, node_style, end_style } = this.model;
            const xs = [];
            const ys = [];
            const styles = {};
            for (const key of (0, object_1.keys)(end_style)) {
                styles[key] = [];
            }
            for (let i = 0; i < renderers.length; i++) {
                const renderer = renderers[i];
                const cds = renderer.data_source;
                const glyph = renderer.glyph;
                const [xkey, ykey] = [glyph.xs.field, glyph.ys.field];
                for (const array of cds.get_array(xkey)) {
                    (0, assert_1.assert)((0, types_1.isArray)(array));
                    xs.push(...array);
                    for (const [key, val] of (0, object_1.entries)(end_style)) {
                        styles[key].push(val);
                    }
                    for (const [key, val] of (0, object_1.entries)(node_style)) {
                        for (let index = 0; index < array.length - 2; index++) {
                            styles[key].push(val);
                        }
                    }
                    for (const [key, val] of (0, object_1.entries)(end_style)) {
                        styles[key].push(val);
                    }
                }
                for (const array of cds.get_array(ykey)) {
                    (0, assert_1.assert)((0, types_1.isArray)(array));
                    ys.push(...array);
                }
                if (this._drawing && i == renderers.length - 1) {
                    // Skip currently drawn vertex
                    xs.splice(xs.length - 1, 1);
                    ys.splice(ys.length - 1, 1);
                    for (const [_, array] of (0, object_1.entries)(styles)) {
                        array.splice(array.length - 1, 1);
                    }
                }
            }
            this._set_vertices(xs, ys, styles);
        }
        _remove() {
            const renderer = this.model.renderers[0];
            const cds = renderer.data_source;
            const glyph = renderer.glyph;
            if ((0, vectorization_1.isField)(glyph.xs)) {
                const xkey = glyph.xs.field;
                const array = cds.get_array(xkey);
                const xidx = array.length - 1;
                const xs = array[xidx];
                xs.splice(xs.length - 1, 1);
                if (xs.length == 1) {
                    array.splice(xidx, 1);
                }
            }
            if ((0, vectorization_1.isField)(glyph.ys)) {
                const ykey = glyph.ys.field;
                const array = cds.get_array(ykey);
                const yidx = array.length - 1;
                const ys = array[yidx];
                ys.splice(ys.length - 1, 1);
                if (ys.length == 1) {
                    array.splice(yidx, 1);
                }
            }
            this._emit_cds_changes(cds);
            this._drawing = false;
            this._show_vertices();
        }
    }
    exports.PolyVertexDrawToolView = PolyVertexDrawToolView;
    PolyVertexDrawToolView.__name__ = "PolyVertexDrawToolView";
    class PolyVertexDrawTool extends poly_draw_tool_1.PolyDrawTool {
        constructor(attrs) {
            super(attrs);
        }
    }
    exports.PolyVertexDrawTool = PolyVertexDrawTool;
    _a = PolyVertexDrawTool;
    PolyVertexDrawTool.__name__ = "PolyVertexDrawTool";
    PolyVertexDrawTool.__module__ = "geoviews.models.custom_tools";
    (() => {
        _a.prototype.default_view = PolyVertexDrawToolView;
        _a.define(({ Dict, Unknown }) => ({
            end_style: [Dict(Unknown), {}],
            node_style: [Dict(Unknown), {}],
        }));
    })();
},
"238deef1f5": /* models/poly_edit.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const object_1 = require("@bokehjs/core/util/object");
    const types_1 = require("@bokehjs/core/util/types");
    const poly_edit_tool_1 = require("@bokehjs/models/tools/edit/poly_edit_tool");
    class PolyVertexEditToolView extends poly_edit_tool_1.PolyEditToolView {
        deactivate() {
            this._hide_vertices();
            if (this._selected_renderer == null) {
                return;
            }
            else if (this._drawing) {
                this._remove_vertex();
                this._drawing = false;
            }
            this._emit_cds_changes(this._selected_renderer.data_source, false, true, false);
        }
        _pan(ev) {
            if (this._basepoint == null || this.model.vertex_renderer == null) {
                return;
            }
            const points = this._drag_points(ev, [this.model.vertex_renderer]);
            if (!ev.modifiers.shift) {
                this._move_linked(points);
            }
            if (this._selected_renderer != null) {
                this._selected_renderer.data_source.change.emit();
            }
        }
        _pan_end(ev) {
            if (this._basepoint == null || this.model.vertex_renderer == null) {
                return;
            }
            const points = this._drag_points(ev, [this.model.vertex_renderer]);
            if (!ev.modifiers.shift) {
                this._move_linked(points);
            }
            this._emit_cds_changes(this.model.vertex_renderer.data_source, false, true, true);
            if (this._selected_renderer != null) {
                this._emit_cds_changes(this._selected_renderer.data_source);
            }
            this._basepoint = null;
        }
        _drag_points(ev, renderers) {
            if (this._basepoint == null) {
                return [];
            }
            const [bx, by] = this._basepoint;
            const points = [];
            for (const renderer of renderers) {
                const basepoint = this._map_drag(bx, by, renderer);
                const point = this._map_drag(ev.sx, ev.sy, renderer);
                if (point == null || basepoint == null) {
                    continue;
                }
                const [x, y] = point;
                const [px, py] = basepoint;
                const [dx, dy] = [x - px, y - py];
                // Type once dataspecs are typed
                const glyph = renderer.glyph;
                const cds = renderer.data_source;
                const [xkey, ykey] = [glyph.x.field, glyph.y.field];
                for (const index of cds.selected.indices) {
                    const point = [];
                    if (xkey) {
                        const xs = cds.get(xkey);
                        point.push(xs[index]);
                        xs[index] += dx;
                    }
                    if (ykey) {
                        const ys = cds.get(ykey);
                        point.push(ys[index]);
                        ys[index] += dy;
                    }
                    point.push(dx);
                    point.push(dy);
                    points.push(point);
                }
                cds.change.emit();
            }
            this._basepoint = [ev.sx, ev.sy];
            return points;
        }
        _set_vertices(xs, ys, styles) {
            if (this.model.vertex_renderer == null) {
                return;
            }
            const point_glyph = this.model.vertex_renderer.glyph;
            const point_cds = this.model.vertex_renderer.data_source;
            const [pxkey, pykey] = [point_glyph.x.field, point_glyph.y.field];
            if (pxkey) {
                if ((0, types_1.isArray)(xs)) {
                    point_cds.set(pxkey, xs);
                }
                else {
                    point_glyph.x = { value: xs };
                }
            }
            if (pykey) {
                if ((0, types_1.isArray)(ys)) {
                    point_cds.set(pykey, ys);
                }
                else {
                    point_glyph.y = { value: ys };
                }
            }
            if (styles != null) {
                for (const [key, array] of (0, object_1.entries)(styles)) {
                    point_cds.set(key, array);
                    point_glyph[key] = { field: key };
                }
            }
            else {
                for (const col of point_cds.columns()) {
                    point_cds.set(col, []);
                }
            }
            this._emit_cds_changes(point_cds, true, true, false);
        }
        _move_linked(points) {
            if (this._selected_renderer == null) {
                return;
            }
            const renderer = this._selected_renderer;
            const glyph = renderer.glyph;
            const cds = renderer.data_source;
            const [xkey, ykey] = [glyph.xs.field, glyph.ys.field];
            const xpaths = cds.data[xkey];
            const ypaths = cds.data[ykey];
            for (const point of points) {
                const [x, y, dx, dy] = point;
                for (let index = 0; index < xpaths.length; index++) {
                    const xs = xpaths[index];
                    const ys = ypaths[index];
                    for (let i = 0; i < xs.length; i++) {
                        if ((xs[i] == x) && (ys[i] == y)) {
                            xs[i] += dx;
                            ys[i] += dy;
                        }
                    }
                }
            }
        }
        _tap(ev) {
            if (this.model.vertex_renderer == null) {
                return;
            }
            const renderer = this.model.vertex_renderer;
            const point = this._map_drag(ev.sx, ev.sy, renderer);
            if (point == null) {
                return;
            }
            else if (this._drawing && this._selected_renderer != null) {
                let [x, y] = point;
                const cds = renderer.data_source;
                // Type once dataspecs are typed
                const glyph = renderer.glyph;
                const [xkey, ykey] = [glyph.x.field, glyph.y.field];
                const indices = cds.selected.indices;
                [x, y] = this._snap_to_vertex(ev, x, y);
                const index = indices[0];
                cds.selected.indices = [index + 1];
                if (xkey) {
                    const xs = cds.get_array(xkey);
                    const nx = xs[index];
                    xs[index] = x;
                    xs.splice(index + 1, 0, nx);
                }
                if (ykey) {
                    const ys = cds.get_array(ykey);
                    const ny = ys[index];
                    ys[index] = y;
                    ys.splice(index + 1, 0, ny);
                }
                cds.change.emit();
                this._emit_cds_changes(this._selected_renderer.data_source, true, false, true);
                return;
            }
            this._select_event(ev, this._select_mode(ev), [renderer]);
        }
        _show_vertices(ev) {
            if (!this.model.active) {
                return;
            }
            const renderers = this._select_event(ev, "replace", this.model.renderers);
            if (renderers.length === 0) {
                this._hide_vertices();
                this._selected_renderer = null;
                this._drawing = false;
                return;
            }
            const renderer = renderers[0];
            const glyph = renderer.glyph;
            const cds = renderer.data_source;
            const index = cds.selected.indices[0];
            const [xkey, ykey] = [glyph.xs.field, glyph.ys.field];
            let xs;
            let ys;
            if (xkey) {
                xs = cds.get(xkey)[index];
                if (!(0, types_1.isArray)(xs)) {
                    cds.get(xkey)[index] = xs = Array.from(xs);
                }
            }
            else {
                xs = glyph.xs.value;
            }
            if (ykey) {
                ys = cds.get(ykey)[index];
                if (!(0, types_1.isArray)(ys)) {
                    cds.get(ykey)[index] = ys = Array.from(ys);
                }
            }
            else {
                ys = glyph.ys.value;
            }
            const { end_style, node_style } = this.model;
            const styles = {};
            for (const [key, val] of (0, object_1.entries)(end_style)) {
                styles[key] = [val];
            }
            for (const [key, val] of (0, object_1.entries)(node_style)) {
                for (let index = 0; index < xs.length - 2; index++) {
                    styles[key].push(val);
                }
            }
            for (const [key, val] of (0, object_1.entries)(end_style)) {
                styles[key].push(val);
            }
            this._selected_renderer = renderer;
            this._set_vertices(xs, ys, styles);
        }
    }
    exports.PolyVertexEditToolView = PolyVertexEditToolView;
    PolyVertexEditToolView.__name__ = "PolyVertexEditToolView";
    class PolyVertexEditTool extends poly_edit_tool_1.PolyEditTool {
        constructor(attrs) {
            super(attrs);
        }
    }
    exports.PolyVertexEditTool = PolyVertexEditTool;
    _a = PolyVertexEditTool;
    PolyVertexEditTool.__name__ = "PolyVertexEditTool";
    PolyVertexEditTool.__module__ = "geoviews.models.custom_tools";
    (() => {
        _a.prototype.default_view = PolyVertexEditToolView;
        _a.define(({ Dict, Unknown }) => ({
            end_style: [Dict(Unknown), {}],
            node_style: [Dict(Unknown), {}],
        }));
    })();
},
"1a96add9eb": /* models/restore_tool.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const action_tool_1 = require("@bokehjs/models/tools/actions/action_tool");
    const column_data_source_1 = require("@bokehjs/models/sources/column_data_source");
    const icons_css_1 = require("@bokehjs/styles/icons.css");
    class RestoreToolView extends action_tool_1.ActionToolView {
        doit() {
            const sources = this.model.sources;
            for (const source of sources) {
                const new_data = source.buffer?.pop();
                if (new_data == null) {
                    continue;
                }
                source.data = new_data;
                source.change.emit();
                source.properties.data.change.emit();
            }
        }
    }
    exports.RestoreToolView = RestoreToolView;
    RestoreToolView.__name__ = "RestoreToolView";
    class RestoreTool extends action_tool_1.ActionTool {
        constructor(attrs) {
            super(attrs);
            this.tool_name = "Restore";
            this.tool_icon = icons_css_1.tool_icon_undo;
        }
    }
    exports.RestoreTool = RestoreTool;
    _a = RestoreTool;
    RestoreTool.__name__ = "RestoreTool";
    RestoreTool.__module__ = "geoviews.models.custom_tools";
    (() => {
        _a.prototype.default_view = RestoreToolView;
        _a.define(({ List, Ref }) => ({
            sources: [List(Ref(column_data_source_1.ColumnDataSource)), []],
        }));
    })();
},
"028985dc77": /* models/wind_barb.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const tslib_1 = require("tslib");
    const xy_glyph_1 = require("@bokehjs/models/glyphs/xy_glyph");
    const property_mixins_1 = require("@bokehjs/core/property_mixins");
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    const selection_1 = require("@bokehjs/models/selections/selection");
    class WindBarbView extends xy_glyph_1.XYGlyphView {
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
            return new selection_1.Selection({ indices: candidates });
        }
        draw_legend_for_index(ctx, { x0, x1, y0, y1 }, _index) {
            const cx = (x0 + x1) / 2;
            const cy = (y0 + y1) / 2;
            // Draw a representative wind barb in the legend
            this._draw_wind_barb(ctx, cx, cy, Math.PI / 4, 25, 0.5);
        }
    }
    exports.WindBarbView = WindBarbView;
    WindBarbView.__name__ = "WindBarbView";
    class WindBarb extends xy_glyph_1.XYGlyph {
        constructor(attrs) {
            super(attrs);
        }
    }
    exports.WindBarb = WindBarb;
    _a = WindBarb;
    WindBarb.__name__ = "WindBarb";
    WindBarb.__module__ = "geoviews.models.wind_barb";
    (() => {
        _a.prototype.default_view = WindBarbView;
        _a.define(({ Float }) => ({
            angle: [p.AngleSpec, { value: 0 }],
            magnitude: [p.NumberSpec, { value: 0 }],
            scale: [Float, 1.0],
            barb_length: [Float, 30.0],
            barb_width: [Float, 15.0],
            flag_width: [Float, 15.0],
            spacing: [Float, 6.0],
            calm_circle_radius: [Float, 3.0],
        }));
        _a.mixins(property_mixins_1.LineVector);
    })();
},
}, "c764d38756", {"index":"c764d38756","models/index":"2e3df39bba","models/checkpoint_tool":"49636d3eef","models/clear_tool":"356402dee7","models/poly_draw":"c03d81e6d5","models/poly_edit":"238deef1f5","models/restore_tool":"1a96add9eb","models/wind_barb":"028985dc77"}, {});});
//# sourceMappingURL=geoviews.js.map
