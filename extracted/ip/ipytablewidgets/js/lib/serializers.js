"use strict";
// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021
Object.defineProperty(exports, "__esModule", { value: true });
exports.table_serialization = exports.tableToJSON = exports.rowProxy = exports.JSONToTable = void 0;
const ndarray = require("ndarray");
const compression_1 = require("./compression");
const dtypeToArray = {
    "bool": Uint8Array,
    int8: Int8Array,
    int16: Int16Array,
    int32: Int32Array,
    uint8: Uint8Array,
    uint16: Uint16Array,
    uint32: Uint32Array,
    float32: Float32Array,
    float64: Float64Array,
    str: Array
};
const RowIndex = Symbol('rowIndex');
function JSONToTable(obj, manager) {
    if (obj === null) {
        return null;
    }
    var data = {};
    var size = Infinity;
    let decoder = new TextDecoder("utf-8");
    let buffer;
    for (const [col, val] of Object.entries(obj.data)) {
        // console.log(col, val);
        if (val.compression !== undefined) {
            let valBuffer = val.buffer;
            buffer = compression_1.decompress[val.compression](valBuffer.buffer);
            if (val.dtype === "str") {
                let u8buf = buffer;
                let strcol = decoder.decode(u8buf);
                let lstr = JSON.parse(strcol);
                data[col] = lstr;
            }
            else { //numeric
                data[col] = ndarray(new dtypeToArray[val.dtype](buffer), val.shape);
                size = Math.min(size, val.shape[0]);
            }
        }
        else { // no compression
            if (val.dtype === "str") {
                let lstr = val.buffer;
                data[col] = lstr;
                size = Math.min(size, lstr.length);
            }
            else { //numeric
                let valBuffer = val.buffer;
                data[col] = ndarray(new dtypeToArray[val.dtype](valBuffer.buffer), val.shape);
                size = Math.min(size, val.shape[0]);
            }
        }
    }
    var result = { columns: obj.columns, data: data, size: size };
    // console.log("result", result);
    //let objFoo = obj.data.foo;
    return result;
}
exports.JSONToTable = JSONToTable;
function rowProxy(table) {
    if (table === null) {
        return null;
    }
    var fields = table.columns;
    var proto = {};
    fields.forEach((name) => {
        const column = table.data[name];
        const arraycolumn = column;
        const stringcolumn = column;
        // skip columns with duplicate names
        if (proto.hasOwnProperty(name))
            return;
        if (arraycolumn.shape === undefined) {
            Object.defineProperty(proto, name, {
                get: function () {
                    const i = this[RowIndex];
                    return stringcolumn[i];
                },
                set: function () {
                    throw Error('Arrow field values can not be overwritten.');
                },
                enumerable: true
            });
        }
        else {
            Object.defineProperty(proto, name, {
                get: function () {
                    const i = this[RowIndex];
                    const v = arraycolumn.get(i);
                    return isNaN(v) ? null : v;
                },
                set: function () {
                    throw Error('Arrow field values can not be overwritten.');
                },
                enumerable: true
            });
        }
    });
    return (i) => {
        var r = Object.create(proto);
        r[RowIndex] = i;
        return r;
    };
}
exports.rowProxy = rowProxy;
function tableToJSON(obj, widget) {
    return null; // TODO: implement or remove ...
}
exports.tableToJSON = tableToJSON;
/**
 * Serializers for to/from tables/dataframes
 */
exports.table_serialization = { deserialize: JSONToTable, serialize: tableToJSON };
//# sourceMappingURL=serializers.js.map