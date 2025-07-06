"use strict";
(self["webpackChunkjupyterlab_autoscrollcelloutput"] = self["webpackChunkjupyterlab_autoscrollcelloutput"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ButtonAutoScrollCellOutput": () => (/* binding */ ButtonAutoScrollCellOutput),
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




// function JupyterLabAutoScroll() {
//   let divs = document.querySelectorAll('.lm-Widget.p-Widget.jp-OutputArea.jp-Cell-outputArea');
//   for (let i = 0; i < divs.length; i++) {
//     let div = divs[i];
//     if (div.scrollHeight > 0 &&
//       div.scrollTop != div.scrollHeight &&
//       div.parentElement != null &&
//       div.parentElement.parentElement != null &&
//       div.parentElement.parentElement.childNodes[1].childNodes[1].childNodes[0].childNodes[0].textContent == "[*]:") {
//       if (div.childNodes.length == 1) {
//         div.scrollTop = div.scrollHeight;
//       }
//     }
//   }
// }
/**
 * Initialization data for the jupyterlab_autoscrollcelloutput extension.
 */
const plugin = {
    id: 'jupyterlab_autoscrollcelloutput:plugin',
    autoStart: true,
    activate: (app) => {
        console.log('JupyterLab extension jupyterlab_autoscrollcelloutput is activated!');
        app.docRegistry.addWidgetExtension('Notebook', new ButtonAutoScrollCellOutput());
    }
};
class ButtonAutoScrollCellOutput {
    createNew(panel, context) {
        const triggerAutoScrollCellOutput = () => {
            if (SET) {
                SET = false;
                console.log('Extension jupyterlab_autoscrollcelloutput disabled');
                // clearInterval(t);
                if (button.hasClass('selected'))
                    button.removeClass('selected');
            }
            else {
                SET = true;
                console.log('Extension jupyterlab_autoscrollcelloutput enabled');
                // t = setInterval(JupyterLabAutoScroll, 10);
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
        this.notebook.model.cells.changed.connect(this.onCellsChanged, this);
        var SET = true;
        // var t = setInterval(JupyterLabAutoScroll, 10);
        button.addClass('selected');
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => { button.dispose(); });
    }
    onCellsChanged(cells, changed_cells) {
        // If new cells added
        if (changed_cells.type == 'add') {
            // Go through all cells
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.each)(changed_cells.newValues, (cellModel, idx) => {
                if (cellModel instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCellModel) {
                    // Detect output changes
                    cellModel.outputs.changed.connect((output, arg) => {
                        let autoScrollEnabled = this.notebook.model.metadata.get('autoscrollcelloutput');
                        // If the change type is 'set', the output has changed.
                        // Check if scroll and auto scroll is enabled in metadata
                        if (['add', 'set'].includes(arg.type) &&
                            cellModel.metadata.get("scrolled") && autoScrollEnabled) {
                            // Find the widget for the model.
                            //TODO: is there any other method then iteration
                            for (let cell of this.notebook.widgets) {
                                if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell && cell.model == cellModel) {
                                    // Scroll to bottom
                                    cell.outputArea.node.scrollTop = cell.outputArea.node.scrollHeight;
                                    // Place resize observer for output widgets
                                    // for (let widget of (cell as CodeCell).outputArea.widgets) {
                                    //     this.resizeObserver.unobserve(widget.node);
                                    //     (widget => {
                                    //         setTimeout(() => {
                                    //             this.resizeObserver.observe(widget.node);
                                    //         });
                                    //     })(widget);
                                    // }
                                    // Find output view widgets
                                    // this.scrollOutputViews(cell)
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
//# sourceMappingURL=lib_index_js.8b69d37af69b20b4237e.js.map