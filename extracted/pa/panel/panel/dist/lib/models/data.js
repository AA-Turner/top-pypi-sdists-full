import { isNumber } from "@bokehjs/core/util/types";
function cds_record_builder(cds, addId) {
    const columns = cds.columns();
    const cdsLength = cds.get_length();
    if (columns.length === 0 || cdsLength === null) {
        return null;
    }
    const accessors = [];
    for (const column of columns) {
        const array = cds.get_array(column);
        const shape = (array[0] == null || array[0].shape == null) ? null : array[0].shape;
        if (shape != null && shape.length > 1 && isNumber(shape[0])) {
            const width = shape[1];
            accessors.push([column, (i) => array.slice(i * width, i * width + width)]);
        }
        else if (array.length != cdsLength && (array.length % cdsLength === 0)) {
            const offset = array.length / cdsLength;
            accessors.push([column, (i) => array.slice(i * offset, i * offset + offset)]);
        }
        else {
            accessors.push([column, (i) => array[i]]);
        }
    }
    return (i) => {
        const item = {};
        for (const [column, get] of accessors) {
            item[column] = get(i);
        }
        if (addId) {
            item._index = i;
        }
        return item;
    };
}
export function transform_cds_to_records(cds, addId = false, start = 0) {
    const build = cds_record_builder(cds, addId);
    if (build === null) {
        return [];
    }
    const data = [];
    const cdsLength = cds.get_length() ?? 0;
    for (let i = start; i < cdsLength; i++) {
        data.push(build(i));
    }
    return data;
}
export function transform_cds_rows_to_records(cds, indices, addId = false) {
    const build = cds_record_builder(cds, addId);
    if (build === null) {
        return [];
    }
    const cdsLength = cds.get_length() ?? 0;
    const data = [];
    for (const i of indices) {
        if (i >= 0 && i < cdsLength) {
            data.push(build(i));
        }
    }
    return data;
}
export function dict_to_records(data, index = true) {
    const records = [];
    for (let i = 0; i < data.index.length; i++) {
        const record = {};
        for (const col of data) {
            if (index || col !== "index") {
                record[col] = data[col][i];
            }
        }
    }
    return records;
}
//# sourceMappingURL=data.js.map