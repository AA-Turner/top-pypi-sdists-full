"use strict";
(self["webpackChunkjupyterlab_autoscrollcelloutput"] = self["webpackChunkjupyterlab_autoscrollcelloutput"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);




const plugin = {
    id: 'jupyterlab_autoscrollcelloutput:plugin',
    autoStart: true,
    activate: (app) => {
        console.log('JupyterLab extension jupyterlab_autoscrollcelloutput is activated!');
        app.docRegistry.addWidgetExtension('Notebook', {
            createNew: (panel, context) => {
                return new ButtonAutoScrollCellOutput().init(panel);
            }
        });
    }
};
class ButtonAutoScrollCellOutput {
    init(panel) {
        const triggerAutoScrollCellOutput = () => {
            if (SET) {
                SET = false;
                console.log('Extension jupyterlab_autoscrollcelloutput disabled for notebook:', panel.id);
                if (button.hasClass('selected'))
                    button.removeClass('selected');
            }
            else {
                SET = true;
                console.log('Extension jupyterlab_autoscrollcelloutput enabled for notebook:', panel.id);
                button.addClass('selected');
            }
            this.notebook.model.metadata.set('autoscrollcelloutput', SET);
        };
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            className: 'buttonAutoScrollCellOuput',
            iconClass: 'wll-ScrollIcon',
            label: 'scroll',
            onClick: triggerAutoScrollCellOutput,
            tooltip: 'Auto Scroll Cell Ouput'
        });
        panel.toolbar.insertItem(10, 'AutoScrollCellOutput', button);
        this.notebook = panel.content;
        var SET = true;
        button.addClass('selected');
        this.notebook.model.cells.changed.connect(this.handlerCellsChange, this);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => { button.dispose(); });
    }
    handlerCellsChange(cells, changed_cells) {
        if (changed_cells.type == 'add') {
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(changed_cells.newValues, (cellModel, idx) => {
                if (cellModel instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCellModel) {
                    cellModel.outputs.changed.connect((output, arg) => {
                        let autoScrollSet = this.notebook.model.metadata.get('autoscrollcelloutput');
                        if (['add', 'set'].includes(arg.type) && cellModel.metadata.get("scrolled") && autoScrollSet) {
                            // Find the widget for the model.
                            for (let cell of this.notebook.widgets) {
                                if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell && cell.model == cellModel) {
                                    // Scroll to bottom
                                    cell.outputArea.node.scrollTop = cell.outputArea.node.scrollHeight;
                                }
                            }
                        }
                    });
                }
            });
        }
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.5c0ce75d28ac2c8edfe1.js.map