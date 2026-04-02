"use strict";
// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.EchoTableWidgetView = exports.EchoTableWidgetModel = exports.TableWidgetModel = void 0;
const base_1 = require("@jupyter-widgets/base");
const ndarray = require("ndarray");
const ndarray_unpack = require("ndarray-unpack");
const serializers_1 = require("./serializers");
let version = require('../package.json').version;
class TableWidgetModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, base_1.DOMWidgetModel.prototype.defaults()), { _model_name: "TableWidgetModel", _view_name: null, _model_module: 'jupyter-tablewidgets', _view_module: null, _model_module_version: version, _view_module_version: '', _table: ndarray([]), _columns: [] });
    }
    ;
}
exports.TableWidgetModel = TableWidgetModel;
TableWidgetModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { _table: serializers_1.table_serialization });
// https://gist.github.com/pbugnion/63cf43b41ec0eed2d0b7e7426d1c67d2
class EchoTableWidgetModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, base_1.DOMWidgetModel.prototype.defaults()), { _model_name: "EchoTableWidgetModel", _view_name: "EchoTableWidgetView", _model_module: 'jupyter-tablewidgets', _view_module: 'jupyter-tablewidgets', _model_module_version: version, _view_module_version: version, data: [], echo: [] });
    }
    ;
}
exports.EchoTableWidgetModel = EchoTableWidgetModel;
EchoTableWidgetModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { data: { deserialize: base_1.unpack_models } });
class EchoTableWidgetView extends base_1.DOMWidgetView {
    render() {
        return __awaiter(this, void 0, void 0, function* () {
            let that = this.model;
            let subwg = that.get("data");
            let table = subwg.get("_table");
            let res = { 'columns': table.columns, 'data': {} };
            for (const [col, v] of Object.entries(table.data)) {
                let val = v;
                if (val.dtype !== undefined) {
                    res.data[col] = ndarray_unpack(val);
                }
                else {
                    res.data[col] = val;
                }
            }
            that.set("echo", res);
            this.touch();
        });
    }
    ;
}
exports.EchoTableWidgetView = EchoTableWidgetView;
//# sourceMappingURL=widgets.js.map