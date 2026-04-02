"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.load_ipython_extension = void 0;
if (window.require !== undefined) {
    window.require.config({
        map: {
            "*": {
                "jupyter-tablewidgets": "nbextensions/jupyter-tablewidgets/index",
            }
        }
    });
}
function load_ipython_extension() { }
exports.load_ipython_extension = load_ipython_extension;
//# sourceMappingURL=extension.js.map