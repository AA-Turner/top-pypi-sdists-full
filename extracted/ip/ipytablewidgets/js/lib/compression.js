"use strict";
// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021
Object.defineProperty(exports, "__esModule", { value: true });
exports.decompress = void 0;
const pako = require("pako");
const lz4 = require("lz4js");
exports.decompress = {
    zlib: (input) => {
        return pako.inflate(new Uint8Array(input)).buffer;
    },
    lz4: (input) => {
        return lz4.decompress(new Uint8Array(input)).buffer;
    },
};
//# sourceMappingURL=compression.js.map