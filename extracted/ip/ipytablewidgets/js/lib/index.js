"use strict";
// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021
Object.defineProperty(exports, "__esModule", { value: true });
exports.version = exports.decompress = exports.rowProxy = exports.table_serialization = exports.EchoTableWidgetView = exports.EchoTableWidgetModel = exports.TableWidgetModel = void 0;
var widgets_1 = require("./widgets");
Object.defineProperty(exports, "TableWidgetModel", { enumerable: true, get: function () { return widgets_1.TableWidgetModel; } });
Object.defineProperty(exports, "EchoTableWidgetModel", { enumerable: true, get: function () { return widgets_1.EchoTableWidgetModel; } });
Object.defineProperty(exports, "EchoTableWidgetView", { enumerable: true, get: function () { return widgets_1.EchoTableWidgetView; } });
var serializers_1 = require("./serializers");
Object.defineProperty(exports, "table_serialization", { enumerable: true, get: function () { return serializers_1.table_serialization; } });
Object.defineProperty(exports, "rowProxy", { enumerable: true, get: function () { return serializers_1.rowProxy; } });
var compression_1 = require("./compression");
Object.defineProperty(exports, "decompress", { enumerable: true, get: function () { return compression_1.decompress; } });
exports.version = require('../package.json').version;
//# sourceMappingURL=index.js.map