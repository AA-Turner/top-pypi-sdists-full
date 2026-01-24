"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const plugin = require("./index");
const base = require("@jupyter-widgets/base");
module.exports = {
    id: 'jupyter-tablewidgets',
    requires: [base.IJupyterWidgetRegistry],
    activate: (app, widgets) => {
        widgets.registerWidget({
            name: 'jupyter-tablewidgets',
            version: plugin.version,
            exports: plugin,
        });
    },
    autoStart: true,
};
//# sourceMappingURL=labplugin.js.map