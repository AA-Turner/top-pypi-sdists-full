"use strict";
(self["webpackChunkipysigma"] = self["webpackChunkipysigma"] || []).push([["lib_widget_js-data_image_svg_xml_base64_PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgM-6426be"],{

/***/ "./lib/custom-hover.js":
/*!*****************************!*\
  !*** ./lib/custom-hover.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const custom_label_1 = __importDefault(__webpack_require__(/*! ./custom-label */ "./lib/custom-label.js"));
/**
 * Draw an hovered node.
 * - if there is no label => display a shadow on the node
 * - if the label box is bigger than node size => display a label box that contains the node with a shadow
 * - else node with shadow and the label box
 */
function drawHover(context, data, settings) {
    const size = data.labelSize || settings.labelSize;
    const font = settings.labelFont;
    const weight = settings.labelWeight;
    data = Object.assign(Object.assign({}, data), { label: data.label || data.hoverLabel });
    context.font = `${weight} ${size}px ${font}`;
    // Then we draw the label background
    context.fillStyle = '#FFF';
    context.shadowOffsetX = 0;
    context.shadowOffsetY = 0;
    context.shadowBlur = 8;
    context.shadowColor = '#000';
    const PADDING = 2;
    if (typeof data.label === 'string') {
        const textWidth = context.measureText(data.label).width;
        const boxWidth = Math.round(textWidth + 5);
        const boxHeight = Math.round(size + 2 * PADDING);
        const radius = Math.max(data.size, size / 2) + PADDING;
        const angleRadian = Math.asin(boxHeight / 2 / radius);
        const xDeltaCoord = Math.sqrt(Math.abs(Math.pow(radius, 2) - Math.pow(boxHeight / 2, 2)));
        context.beginPath();
        context.moveTo(data.x + xDeltaCoord, data.y + boxHeight / 2);
        context.lineTo(data.x + radius + boxWidth, data.y + boxHeight / 2);
        context.lineTo(data.x + radius + boxWidth, data.y - boxHeight / 2);
        context.lineTo(data.x + xDeltaCoord, data.y - boxHeight / 2);
        context.arc(data.x, data.y, radius, angleRadian, -angleRadian);
        context.closePath();
        context.fill();
    }
    else {
        context.beginPath();
        context.arc(data.x, data.y, data.size + PADDING, 0, Math.PI * 2);
        context.closePath();
        context.fill();
    }
    context.shadowOffsetX = 0;
    context.shadowOffsetY = 0;
    context.shadowBlur = 0;
    // And finally we draw the label
    (0, custom_label_1.default)(context, data, settings);
}
exports["default"] = drawHover;


/***/ }),

/***/ "./lib/custom-label.js":
/*!*****************************!*\
  !*** ./lib/custom-label.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
function drawLabel(context, data, settings) {
    if (!data.label)
        return;
    const size = data.labelSize || settings.labelSize;
    const font = settings.labelFont;
    const weight = settings.labelWeight;
    const color = data.labelColor || settings.labelColor.color;
    context.fillStyle = color;
    context.font = `${weight} ${size}px ${font}`;
    context.fillText(data.label, data.x + data.size + 3, data.y + size / 3);
}
exports["default"] = drawLabel;


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.scatterIcon = exports.fullscreenExitIcon = exports.fullscreenEnterIcon = exports.pauseIcon = exports.playIcon = exports.resetLayoutIcon = exports.resetZoomIcon = exports.unzoomIcon = exports.zoomIcon = void 0;
exports.zoomIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path><path d="M12 10h-2v2H9v-2H7V9h2V7h1v2h2v1z"></path></svg>`;
exports.unzoomIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14zM7 9h5v1H7z"></path></svg>`;
exports.resetZoomIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M5 15H3v4c0 1.1.9 2 2 2h4v-2H5v-4zM5 5h4V3H5c-1.1 0-2 .9-2 2v4h2V5zm14-2h-4v2h4v4h2V5c0-1.1-.9-2-2-2zm0 16h-4v2h4c1.1 0 2-.9 2-2v-4h-2v4zM12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 6c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"></path></svg>`;
exports.resetLayoutIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M7.11 8.53 5.7 7.11C4.8 8.27 4.24 9.61 4.07 11h2.02c.14-.87.49-1.72 1.02-2.47zM6.09 13H4.07c.17 1.39.72 2.73 1.62 3.89l1.41-1.42c-.52-.75-.87-1.59-1.01-2.47zm1.01 5.32c1.16.9 2.51 1.44 3.9 1.61V17.9c-.87-.15-1.71-.49-2.46-1.03L7.1 18.32zM13 4.07V1L8.45 5.55 13 10V6.09c2.84.48 5 2.94 5 5.91s-2.16 5.43-5 5.91v2.02c3.95-.49 7-3.85 7-7.93s-3.05-7.44-7-7.93z"></path></svg>`;
exports.playIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>`;
exports.pauseIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"></path></svg>`;
exports.fullscreenEnterIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"></path></svg>`;
exports.fullscreenExitIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"></path></svg>`;
exports.scatterIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><circle cx="7" cy="14" r="3"></circle><circle cx="11" cy="6" r="3"></circle><circle cx="16.6" cy="17.6" r="3"></circle></svg>`;


/***/ }),

/***/ "./lib/palette.js":
/*!************************!*\
  !*** ./lib/palette.js ***!
  \************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const iwanthue_1 = __importDefault(__webpack_require__(/*! iwanthue */ "webpack/sharing/consume/default/iwanthue/iwanthue"));
const d3Chromatic = __importStar(__webpack_require__(/*! d3-scale-chromatic */ "webpack/sharing/consume/default/d3-scale-chromatic/d3-scale-chromatic"));
const shuffle_in_place_1 = __webpack_require__(/*! pandemonium/shuffle-in-place */ "./node_modules/pandemonium/shuffle-in-place.js");
const seedrandom_1 = __importDefault(__webpack_require__(/*! seedrandom */ "webpack/sharing/consume/default/seedrandom/seedrandom"));
const shapes_1 = __webpack_require__(/*! ./shapes */ "./lib/shapes.js");
function getDefaultDefaultValue(kind) {
    if (kind === 'color')
        return '#ccc';
    else
        return shapes_1.UNKNOWN_SHAPE;
}
class Palette {
    constructor(name, kind, map, defaultValue) {
        this.name = name;
        this.kind = kind;
        this.map = map;
        this.defaultValue = defaultValue;
        this.size = this.map.size;
    }
    get(key) {
        const value = this.map.get(key);
        if (value === undefined)
            return this.defaultValue;
        return value;
    }
    forEach(callback) {
        this.map.forEach(callback);
    }
    static getMacroDefault(kind) {
        if (kind === 'color')
            return '#ccc';
        else
            return shapes_1.UNKNOWN_SHAPE;
    }
    static fromScheme(name, kind, scheme, values, defaultValue) {
        const target = d3Chromatic['scheme' + scheme];
        let colors;
        if (Array.isArray(target[target.length - 1])) {
            const firstValidCount = target.findIndex((c) => Array.isArray(c));
            colors = target[Math.min(Math.max(firstValidCount, values.length), target.length)];
        }
        else {
            colors = target.slice();
            const shuffleInPlace = (0, shuffle_in_place_1.createShuffleInPlace)((0, seedrandom_1.default)(name));
            shuffleInPlace(colors);
            colors = colors.slice(0, Math.min(values.length, colors.length));
        }
        const map = new Map();
        values.slice(0, colors.length).forEach((v, i) => {
            map.set(v, colors[i]);
        });
        return new Palette(name, kind, map, defaultValue || getDefaultDefaultValue(kind));
    }
    static fromEntries(name, kind, entries, defaultValue) {
        return new Palette(name, kind, new Map(entries), defaultValue || getDefaultDefaultValue(kind));
    }
    static generateFromValues(name, kind, values, defaultValue) {
        if (kind === 'color') {
            const settings = {
                colorSpace: 'sensible',
                seed: name,
                clustering: 'force-vector',
                attempts: 5,
            };
            if (values.length === 0)
                return new Palette(name, kind, new Map(), defaultValue || getDefaultDefaultValue(kind));
            const colors = (0, iwanthue_1.default)(values.length, settings);
            const map = new Map();
            values.forEach((v, i) => {
                map.set(v, colors[i]);
            });
            return new Palette(name, kind, map, defaultValue || getDefaultDefaultValue(kind));
        }
        else {
            const map = new Map();
            shapes_1.USEFUL_SHAPES.slice(0, Math.min(values.length, shapes_1.USEFUL_SHAPES.length)).forEach((shape, i) => {
                map.set(values[i], shape.name);
            });
            return new Palette(name, kind, map, defaultValue || getDefaultDefaultValue(kind));
        }
    }
}
exports["default"] = Palette;


/***/ }),

/***/ "./lib/shapes.js":
/*!***********************!*\
  !*** ./lib/shapes.js ***!
  \***********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.shapeToPicto = exports.UNKNOWN_SHAPE = exports.USEFUL_SHAPES = void 0;
exports.USEFUL_SHAPES = [
    { name: 'circle', pictogram: 'circle' },
    { name: 'triangle', pictogram: 'change_history' },
    { name: 'square', pictogram: 'square' },
    { name: 'pentagon', pictogram: 'pentagon' },
    { name: 'star', pictogram: 'star' },
    { name: 'hexagon', pictogram: 'hexagon' },
    { name: 'heart', pictogram: 'favorite' },
    { name: 'cloud', pictogram: 'cloudy' },
];
exports.UNKNOWN_SHAPE = 'help';
const SHAPES_MAP = new Map();
exports.USEFUL_SHAPES.forEach(({ name, pictogram }) => {
    SHAPES_MAP.set(name, pictogram);
});
function shapeToPicto(shape) {
    return SHAPES_MAP.get(shape) || shape;
}
exports.shapeToPicto = shapeToPicto;


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.pictogramToUrl = exports.saveAsSVG = exports.saveAsGEXF = exports.saveAsJSON = exports.saveAsPNG = exports.renderAsDataURL = void 0;
const sigma_1 = __importDefault(__webpack_require__(/*! sigma */ "webpack/sharing/consume/default/sigma/sigma"));
const file_saver_1 = __importDefault(__webpack_require__(/*! file-saver */ "webpack/sharing/consume/default/file-saver/file-saver"));
const gexf = __importStar(__webpack_require__(/*! graphology-gexf/browser */ "./node_modules/graphology-gexf/browser/index.js"));
// @ts-ignore
const renderer_1 = __importDefault(__webpack_require__(/*! graphology-svg/renderer */ "./node_modules/graphology-svg/renderer.js"));
// @ts-ignore
const defaults_1 = __webpack_require__(/*! graphology-svg/defaults */ "./node_modules/graphology-svg/defaults.js");
// Taken and adapted from: https://github.com/jacomyal/sigma.js/blob/main/examples/png-snapshot/saveAsPNG.ts
function renderToAuxiliaryCanvas(renderer, inputLayers) {
    const { width, height } = renderer.getDimensions();
    // This pixel ratio is here to deal with retina displays.
    // Indeed, for dimensions W and H, on a retina display, the canvases
    // dimensions actually are 2 * W and 2 * H. Sigma properly deals with it, but
    // we need to readapt here:
    const pixelRatio = window.devicePixelRatio || 1;
    const tmpRoot = document.createElement('DIV');
    tmpRoot.style.width = `${width}px`;
    tmpRoot.style.height = `${height}px`;
    tmpRoot.style.position = 'absolute';
    tmpRoot.style.right = '101%';
    tmpRoot.style.bottom = '101%';
    document.body.appendChild(tmpRoot);
    // Instantiate sigma:
    const tmpRenderer = new sigma_1.default(renderer.getGraph(), tmpRoot, renderer.getSettings());
    // Copy camera and force to render now, to avoid having to wait the schedule /
    // debounce frame:
    tmpRenderer.getCamera().setState(renderer.getCamera().getState());
    tmpRenderer.refresh();
    // Create a new canvas, on which the different layers will be drawn:
    const canvas = document.createElement('CANVAS');
    canvas.setAttribute('width', width * pixelRatio + '');
    canvas.setAttribute('height', height * pixelRatio + '');
    const ctx = canvas.getContext('2d');
    // Draw a white background first:
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, width * pixelRatio, height * pixelRatio);
    // For each layer, draw it on our canvas:
    const canvases = tmpRenderer.getCanvases();
    const layers = inputLayers
        ? inputLayers.filter((id) => !!canvases[id])
        : Object.keys(canvases);
    layers.forEach((id) => {
        ctx.drawImage(canvases[id], 0, 0, width * pixelRatio, height * pixelRatio, 0, 0, width * pixelRatio, height * pixelRatio);
    });
    return [
        canvas,
        () => {
            // Cleanup:
            tmpRenderer.kill();
            tmpRoot.remove();
        },
    ];
}
function copyGraphForGexf(renderer) {
    const original = renderer.getGraph();
    const copy = original.copy();
    copy.updateEachNodeAttributes((node, attr) => {
        const displayData = renderer.getNodeDisplayData(node);
        const { x, y } = renderer.graphToViewport(displayData);
        return Object.assign(Object.assign({}, attr), { color: displayData.color, size: displayData.size, x,
            y });
    });
    copy.updateEachEdgeAttributes((edge, attr) => {
        const displayData = renderer.getEdgeDisplayData(edge);
        return Object.assign(Object.assign({}, attr), { color: displayData.color, size: displayData.size });
    });
    return copy;
}
function renderAsDataURL(renderer) {
    const [canvas, cleanup] = renderToAuxiliaryCanvas(renderer);
    const dataURL = canvas.toDataURL();
    cleanup();
    return dataURL;
}
exports.renderAsDataURL = renderAsDataURL;
function saveAsPNG(renderer) {
    const [canvas, cleanup] = renderToAuxiliaryCanvas(renderer);
    // Save the canvas as a PNG image:
    canvas.toBlob((blob) => {
        if (blob)
            file_saver_1.default.saveAs(blob, 'graph.png');
        cleanup();
    }, 'image/png');
}
exports.saveAsPNG = saveAsPNG;
function saveAsJSON(renderer) {
    const data = JSON.stringify(renderer.getGraph(), null, 2);
    file_saver_1.default.saveAs(new Blob([data], { type: 'application/json' }), 'graph.json');
}
exports.saveAsJSON = saveAsJSON;
function saveAsGEXF(renderer) {
    const data = gexf.write(copyGraphForGexf(renderer));
    file_saver_1.default.saveAs(new Blob([data], { type: 'application/xml' }), 'graph.gexf');
}
exports.saveAsGEXF = saveAsGEXF;
function saveAsSVG(renderer) {
    const rendererSettings = renderer.getSettings();
    const settings = Object.assign({}, defaults_1.DEFAULTS);
    settings.nodes = {
        // @ts-ignore
        reducer: (_, n, a) => rendererSettings.nodeReducer(n, a),
        defaultColor: rendererSettings.defaultNodeColor,
    };
    settings.edges = {
        // @ts-ignore
        reducer: (_, e, a) => rendererSettings.edgeReducer(e, a),
        defaultColor: rendererSettings.defaultEdgeColor,
    };
    const data = (0, renderer_1.default)(renderer.getGraph(), settings);
    file_saver_1.default.saveAs(new Blob([data], { type: 'image/svg+xml' }), 'graph.svg');
}
exports.saveAsSVG = saveAsSVG;
function pictogramToUrl(picto, qualifier = 'default') {
    if (picto.startsWith('http'))
        return picto;
    return `https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/${picto}/${qualifier}/48px.svg`;
}
exports.pictogramToUrl = pictogramToUrl;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/visual-variables.js":
/*!*********************************!*\
  !*** ./lib/visual-variables.js ***!
  \*********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.VisualVariableScalesBuilder = exports.CategorySummary = exports.AttributeCategories = exports.AttributeExtents = exports.Extent = void 0;
const multi_set_1 = __importDefault(__webpack_require__(/*! mnemonist/multi-set */ "./node_modules/mnemonist/multi-set.js"));
const palette_1 = __importDefault(__webpack_require__(/*! ./palette */ "./lib/palette.js"));
const d3_scale_1 = __webpack_require__(/*! d3-scale */ "webpack/sharing/consume/default/d3-scale/d3-scale");
const d3Chromatic = __importStar(__webpack_require__(/*! d3-scale-chromatic */ "webpack/sharing/consume/default/d3-scale-chromatic/d3-scale-chromatic"));
/**
 * Constants.
 */
const MAX_CATEGORICAL_COLORS = 10;
const DEFAULT_DEFAULT_CONTINUOUS_NUMERICAL_VALUE = 1;
const DEFAULT_DEFAULT_CONTINUOUS_COLOR_VALUE = 'black';
const ESPILON = 1e-8;
/**
 * Helper functions.
 */
function isValidNumber(value) {
    return (typeof value === 'number' &&
        !Number.isNaN(value) &&
        value !== Infinity &&
        value !== -Infinity);
}
function rangeIsConstant(range) {
    if (!Array.isArray(range))
        return false;
    if (typeof range[0] === 'string')
        return range[0] === range[1];
    return Math.abs(range[0] - range[1]) <= ESPILON;
}
function getContinuousDefaultValue(variable) {
    if (typeof variable.range === 'string' ||
        typeof variable.range[0] === 'string') {
        // Color
        if (typeof variable.default === 'string')
            return variable.default;
        if (Array.isArray(variable.range) && typeof variable.range[0] === 'string')
            return variable.range[0];
        return DEFAULT_DEFAULT_CONTINUOUS_COLOR_VALUE;
    }
    else {
        // Size
        if (isValidNumber(variable.default))
            return variable.default;
        if (Array.isArray(variable.range) && isValidNumber(variable.range[0]))
            return variable.range[0];
        return DEFAULT_DEFAULT_CONTINUOUS_NUMERICAL_VALUE;
    }
}
function createContinuousScale(variable, extent) {
    const defaultValue = getContinuousDefaultValue(variable);
    if (rangeIsConstant(variable.range) || extent.isConstant()) {
        return () => defaultValue;
    }
    let scale;
    const definition = variable.scale;
    let isLogPlusOne = false;
    if (!definition)
        scale = (0, d3_scale_1.scaleLinear)();
    else {
        const [type, param] = definition;
        if (type === 'lin')
            scale = (0, d3_scale_1.scaleLinear)();
        else if (type === 'log' || type === 'log+1') {
            isLogPlusOne = type === 'log+1';
            scale = (0, d3_scale_1.scaleLog)();
            if (param)
                scale.base(param);
        }
        else if (type === 'pow') {
            scale = (0, d3_scale_1.scalePow)();
            scale.exponent(param ? param : 2);
        }
        else if (type === 'sqrt') {
            scale = (0, d3_scale_1.scaleSqrt)();
            if (param)
                scale.exponent(1 / param);
        }
        else
            throw new Error('unknown scale type');
    }
    const offset = isLogPlusOne ? 1 : 0;
    scale.domain([extent.min + offset, extent.max + offset]);
    if (typeof variable.range === 'string') {
        const chromatic = d3Chromatic['interpolate' + variable.range];
        return (attr) => {
            let value = attr[variable.attribute];
            if (!isValidNumber(value))
                return defaultValue;
            value += offset;
            return chromatic(scale(value));
        };
    }
    else if (variable.range) {
        scale.range(variable.range);
        return (attr) => {
            let value = attr[variable.attribute];
            if (!isValidNumber(value))
                return defaultValue;
            value += offset;
            return scale(value);
        };
    }
    throw new Error('could not create valid continuous scale');
}
/**
 * Helper classes.
 */
class Extent {
    constructor() {
        this.min = Infinity;
        this.max = -Infinity;
    }
    add(value) {
        if (value < this.min)
            this.min = value;
        if (value > this.max)
            this.max = value;
    }
    isConstant() {
        return this.min === Infinity || this.min === this.max;
    }
}
exports.Extent = Extent;
class AttributeExtents {
    constructor(names) {
        this.attributes = {};
        // NOTE: this naturally deduplicates names
        names.forEach((name) => (this.attributes[name] = new Extent()));
    }
    add(attributes) {
        for (const name in this.attributes) {
            const value = attributes[name];
            if (!isValidNumber(value))
                continue;
            this.attributes[name].add(value);
        }
    }
}
exports.AttributeExtents = AttributeExtents;
class AttributeCategories {
    constructor(names) {
        this.attributes = {};
        // NOTE: this naturally deduplicates names
        names.forEach((name) => (this.attributes[name] = new multi_set_1.default()));
    }
    add(attributes) {
        for (const name in this.attributes) {
            this.attributes[name].add(attributes[name]);
        }
    }
}
exports.AttributeCategories = AttributeCategories;
class CategorySummary {
    constructor(name, kind, palette, overflowing = false) {
        this.name = name;
        this.kind = kind;
        this.palette = palette;
        this.overflowing = overflowing;
    }
    static fromTopValues(name, kind, frequencies, defaultValue, scheme, maxCount = MAX_CATEGORICAL_COLORS) {
        const count = Math.min(maxCount, frequencies.dimension);
        const topValues = frequencies.top(count);
        const overflowing = count < frequencies.dimension;
        const values = topValues.map((item) => item[0]);
        const palette = !scheme || scheme === 'IWantHue'
            ? palette_1.default.generateFromValues(name, kind, values, defaultValue)
            : palette_1.default.fromScheme(name, kind, scheme, values, defaultValue);
        return new CategorySummary(name, kind, palette, overflowing);
    }
    static fromEntries(name, kind, entries, defaultValue) {
        const palette = palette_1.default.fromEntries(name, kind, entries, defaultValue);
        return new CategorySummary(name, kind, palette);
    }
}
exports.CategorySummary = CategorySummary;
class VisualVariableScalesBuilder {
    constructor(visualVariables, maxCategories = MAX_CATEGORICAL_COLORS) {
        this.variables = visualVariables;
        this.maxCategories = maxCategories;
        const nodeExtentAttributes = [];
        const nodeCategoryAttributes = [];
        const edgeExtentAttributes = [];
        const edgeCategoryAttributes = [];
        for (const variableName in visualVariables) {
            const variable = visualVariables[variableName];
            if (variableName.startsWith('node')) {
                if (variable.type === 'category') {
                    if (!variable.palette || typeof variable.palette === 'string')
                        nodeCategoryAttributes.push(variable.attribute);
                }
                else if (variable.type === 'continuous' ||
                    variableName === 'nodeSize') {
                    nodeExtentAttributes.push(variable.attribute);
                }
            }
            else if (variableName.startsWith('edge')) {
                if (variable.type === 'category') {
                    if (!variable.palette || typeof variable.palette === 'string')
                        edgeCategoryAttributes.push(variable.attribute);
                }
                else if (variable.type === 'continuous') {
                    edgeExtentAttributes.push(variable.attribute);
                }
            }
        }
        this.nodeExtents = new AttributeExtents(nodeExtentAttributes);
        this.edgeExtents = new AttributeExtents(edgeExtentAttributes);
        this.nodeCategories = new AttributeCategories(nodeCategoryAttributes);
        this.edgeCategories = new AttributeCategories(edgeCategoryAttributes);
    }
    readGraph(graph) {
        graph.forEachNode((node, attr) => {
            this.nodeExtents.add(attr);
            this.nodeCategories.add(attr);
        });
        graph.forEachEdge((edge, attr) => {
            this.edgeExtents.add(attr);
            this.edgeCategories.add(attr);
        });
    }
    build() {
        const scales = {};
        for (const variableName in this.variables) {
            const variable = this.variables[variableName];
            let scale = null;
            // Raw variables
            if (variable.type === 'raw') {
                scale = (attr) => attr[variable.attribute] || variable.default;
            }
            // Constant variables
            else if (variable.type === 'constant') {
                scale = () => variable.default;
            }
            // Category variables
            else if (variable.type === 'category') {
                const categories = variableName.startsWith('node')
                    ? this.nodeCategories
                    : this.edgeCategories;
                const summary = variable.palette && typeof variable.palette !== 'string'
                    ? CategorySummary.fromEntries(variable.attribute, variable.kind || 'color', variable.palette, variable.default)
                    : CategorySummary.fromTopValues(variable.attribute, variable.kind || 'color', categories.attributes[variable.attribute], variable.default, variable.palette, this.maxCategories);
                const palette = summary.palette;
                scale = (attr) => palette.get(attr[variable.attribute]);
                scale.summary = summary;
            }
            // Continuous variables
            else if (variable.type === 'continuous') {
                const extents = variableName.startsWith('node')
                    ? this.nodeExtents
                    : this.edgeExtents;
                const extent = extents.attributes[variable.attribute];
                scale = createContinuousScale(variable, extent);
            }
            if (scale)
                scales[variableName] = scale;
        }
        return scales;
    }
    inferLabelRenderedSizeThreshold() {
        const variable = this.variables.nodeSize;
        if (variable.type === 'continuous') {
            const range = variable.range;
            return Math.min(6, range[0]);
        }
        return 6;
    }
}
exports.VisualVariableScalesBuilder = VisualVariableScalesBuilder;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SigmaView = exports.SigmaModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const graphology_1 = __importDefault(__webpack_require__(/*! graphology */ "webpack/sharing/consume/default/graphology/graphology"));
const worker_1 = __importDefault(__webpack_require__(/*! graphology-layout-forceatlas2/worker */ "./node_modules/graphology-layout-forceatlas2/worker.js"));
const worker_2 = __importDefault(__webpack_require__(/*! graphology-layout-noverlap/worker */ "./node_modules/graphology-layout-noverlap/worker.js"));
const graphology_layout_forceatlas2_1 = __importDefault(__webpack_require__(/*! graphology-layout-forceatlas2 */ "webpack/sharing/consume/default/graphology-layout-forceatlas2/graphology-layout-forceatlas2"));
const graphology_communities_louvain_1 = __importDefault(__webpack_require__(/*! graphology-communities-louvain */ "webpack/sharing/consume/default/graphology-communities-louvain/graphology-communities-louvain"));
const utils_1 = __webpack_require__(/*! graphology-layout/utils */ "./node_modules/graphology-layout/utils.js");
const chroma_js_1 = __importDefault(__webpack_require__(/*! chroma-js */ "webpack/sharing/consume/default/chroma-js/chroma-js"));
const sigma_1 = __importDefault(__webpack_require__(/*! sigma */ "webpack/sharing/consume/default/sigma/sigma"));
const animate_1 = __webpack_require__(/*! sigma/utils/animate */ "./node_modules/sigma/utils/animate.js");
const node_1 = __webpack_require__(/*! sigma/rendering/webgl/programs/common/node */ "./node_modules/sigma/rendering/webgl/programs/common/node.js");
const node_point_1 = __importDefault(__webpack_require__(/*! sigma/rendering/webgl/programs/node.point */ "./node_modules/sigma/rendering/webgl/programs/node.point.js"));
const node_point_border_1 = __importDefault(__webpack_require__(/*! @yomguithereal/sigma-experiments-renderers/node/node.point.border */ "./node_modules/@yomguithereal/sigma-experiments-renderers/node/node.point.border.js"));
const node_halo_1 = __importDefault(__webpack_require__(/*! @yomguithereal/sigma-experiments-renderers/node/node.halo */ "./node_modules/@yomguithereal/sigma-experiments-renderers/node/node.halo.js"));
const node_pictogram_1 = __importDefault(__webpack_require__(/*! @yomguithereal/sigma-experiments-renderers/node/node.pictogram */ "./node_modules/@yomguithereal/sigma-experiments-renderers/node/node.pictogram.js"));
const edge_line_1 = __importDefault(__webpack_require__(/*! sigma/rendering/webgl/programs/edge.line */ "./node_modules/sigma/rendering/webgl/programs/edge.line.js"));
const edge_rectangle_1 = __importDefault(__webpack_require__(/*! sigma/rendering/webgl/programs/edge.rectangle */ "./node_modules/sigma/rendering/webgl/programs/edge.rectangle.js"));
const edge_triangle_1 = __importDefault(__webpack_require__(/*! sigma/rendering/webgl/programs/edge.triangle */ "./node_modules/sigma/rendering/webgl/programs/edge.triangle.js"));
const edge_curve_1 = __importDefault(__webpack_require__(/*! @yomguithereal/sigma-experiments-renderers/edge/edge.curve */ "./node_modules/@yomguithereal/sigma-experiments-renderers/edge/edge.curve.js"));
const events_1 = __importDefault(__webpack_require__(/*! events */ "./node_modules/events/events.js"));
const seedrandom_1 = __importDefault(__webpack_require__(/*! seedrandom */ "webpack/sharing/consume/default/seedrandom/seedrandom"));
const comma_number_1 = __importDefault(__webpack_require__(/*! comma-number */ "webpack/sharing/consume/default/comma-number/comma-number"));
const choices_js_1 = __importDefault(__webpack_require__(/*! choices.js */ "webpack/sharing/consume/default/choices.js/choices.js"));
const screenfull_1 = __importDefault(__webpack_require__(/*! screenfull */ "webpack/sharing/consume/default/screenfull/screenfull"));
const debounce_1 = __importDefault(__webpack_require__(/*! debounce */ "webpack/sharing/consume/default/debounce/debounce"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const custom_hover_1 = __importDefault(__webpack_require__(/*! ./custom-hover */ "./lib/custom-hover.js"));
const custom_label_1 = __importDefault(__webpack_require__(/*! ./custom-label */ "./lib/custom-label.js"));
const visual_variables_1 = __webpack_require__(/*! ./visual-variables */ "./lib/visual-variables.js");
const utils_2 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const shapes_1 = __webpack_require__(/*! ./shapes */ "./lib/shapes.js");
const icons_1 = __webpack_require__(/*! ./icons */ "./lib/icons.js");
__webpack_require__(/*! choices.js/public/assets/styles/choices.min.css */ "./node_modules/choices.js/public/assets/styles/choices.min.css");
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
/**
 * Constants.
 */
const NODE_VIZ_ATTRIBUTES = new Set(['label', 'size', 'color', 'x', 'y']);
const EDGE_VIZ_ATTRIBUTES = new Set(['label', 'size', 'color']);
const MUTED_NODE_COLOR = '#ccc';
const IPYSIGMA_KWARG_PREFIX = 'ipysigma_kwarg_';
/**
 * Template.
 */
const TEMPLATE = `
<div class="ipysigma-container"></div>
<div class="ipysigma-left-panel">
  <div class="ipysigma-graph-description"></div>
  <div>
    <button class="ipysigma-zoom-button ipysigma-button ipysigma-svg-icon" title="zoom">
      ${icons_1.zoomIcon}
    </button>
    <button class="ipysigma-unzoom-button ipysigma-button ipysigma-svg-icon" title="unzoom">
      ${icons_1.unzoomIcon}
    </button>
    <button class="ipysigma-reset-zoom-button ipysigma-button ipysigma-svg-icon" title="reset zoom">
      ${icons_1.resetZoomIcon}
    </button>
  </div>
  <div>
    <button class="ipysigma-fullscreen-button ipysigma-button ipysigma-svg-icon" title="enter fullscreen">
      ${icons_1.fullscreenEnterIcon}
    </button>
  </div>
  <div class="ipysigma-layout-controls">
    <button class="ipysigma-layout-button ipysigma-button ipysigma-svg-icon" title="start layout">
      ${icons_1.playIcon}
    </button>
    <button class="ipysigma-noverlap-button ipysigma-button ipysigma-svg-icon" title="spread nodes">
      ${icons_1.scatterIcon}
    </button>
    <button class="ipysigma-reset-layout-button ipysigma-button ipysigma-svg-icon" title="reset layout">
      ${icons_1.resetLayoutIcon}
    </button>
  </div>
</div>
<div class="ipysigma-right-panel">
  <select class="ipysigma-search">
    <option value="">Search a node...</option>
  </select>
  <div class="ipysigma-information-shadow-display" style="display: none;">
    <span class="ipysigma-information-show-button">show info</span>
  </div>
  <div class="ipysigma-information-display">
    <div class="ipysigma-information-display-tabs">
      <span class="ipysigma-information-legend-button ipysigma-tab-button">legend</span>
      &middot;
      <span class="ipysigma-information-info-button ipysigma-tab-button">info</span>
      <span class="ipysigma-information-hide-button">hide</span>
    </div>
    <hr>
    <div class="ipysigma-legend"></div>
    <div class="ipysigma-information-contents"></div>
  </div>
  <div class="ipysigma-download-controls">
    <button class="ipysigma-download-png-button ipysigma-button">
      png
    </button>
    <button class="ipysigma-download-svg-button ipysigma-button">
      svg
    </button>
    <button class="ipysigma-download-gexf-button ipysigma-button">
      gexf
    </button>
    <button class="ipysigma-download-json-button ipysigma-button">
      json
    </button>
  </div>
</div>
`;
/**
 * Model declaration.
 */
class SigmaModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: SigmaModel.model_name, _model_module: SigmaModel.model_module, _model_module_version: SigmaModel.model_module_version, _view_name: SigmaModel.view_name, _view_module: SigmaModel.view_module, _view_module_version: SigmaModel.view_module_version, data: { nodes: [], edges: [] }, height: 500, start_layout: false, snapshot: null, layout: null, clickableEdges: false, visual_variables: {} });
    }
}
exports.SigmaModel = SigmaModel;
SigmaModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
SigmaModel.model_name = 'SigmaModel';
SigmaModel.model_module = version_1.MODULE_NAME;
SigmaModel.model_module_version = version_1.MODULE_VERSION;
SigmaModel.view_name = 'SigmaView'; // Set to null if no view
SigmaModel.view_module = version_1.MODULE_NAME; // Set to null if no view
SigmaModel.view_module_version = version_1.MODULE_VERSION;
/**
 * Helper functions.
 */
function createRng() {
    return (0, seedrandom_1.default)('ipysigma');
}
function isValidNumber(value) {
    return typeof value === 'number' && !isNaN(value);
}
function escapeHtml(unsafe) {
    return ('' + unsafe)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
function renderTypedValue(value) {
    let safe = escapeHtml('' + value);
    let type = 'unknown';
    if (typeof value === 'number') {
        type = 'number';
    }
    else if (typeof value === 'string') {
        type = 'string';
    }
    else if (typeof value === 'boolean') {
        type = 'boolean';
        safe = value ? 'True' : 'False';
    }
    else if (value === null) {
        type = 'keyword';
        safe = 'null';
    }
    return `<span class="ipysigma-${type}" title="${type}">${safe}</span>`;
}
function buildGraph(data, rng) {
    const graph = graphology_1.default.from(data);
    // Rectifications
    graph.updateEachNodeAttributes((key, attr) => {
        // Random position for nodes without positions
        if (!isValidNumber(attr.x))
            attr.x = rng();
        if (!isValidNumber(attr.y))
            attr.y = rng();
        return attr;
    });
    return graph;
}
function createElement(tag, options) {
    const element = document.createElement(tag);
    const { className, style, innerHTML, title } = options || {};
    if (className)
        element.setAttribute('class', className);
    for (const prop in style) {
        element.style[prop] = style[prop];
    }
    if (innerHTML)
        element.innerHTML = innerHTML;
    if (title)
        element.setAttribute('title', title);
    return element;
}
function hide(el) {
    el.style.display = 'none';
}
function show(el) {
    el.style.display = 'block';
}
function disable(el) {
    el.classList.add('disabled');
    el.disabled = true;
}
function enable(el) {
    el.classList.remove('disabled');
    el.disabled = false;
}
const SPINNER_STATES = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'];
function createSpinner() {
    const span = createElement('span', {
        className: 'ipysigma-spinner',
        innerHTML: SPINNER_STATES[0],
    });
    let state = -1;
    let frame = null;
    const update = () => {
        state++;
        state %= SPINNER_STATES.length;
        span.innerHTML = SPINNER_STATES[state];
        frame = setTimeout(update, 80);
    };
    update();
    return [span, () => frame !== null && clearTimeout(frame)];
}
function getGraphDescription(name, graph) {
    let html = '';
    if (name) {
        html += `<u>${escapeHtml(name)}</u><br>`;
    }
    const graphTitle = `${graph.multi ? 'Multi ' : ''}${graph.type === 'undirected' ? 'Undirected' : 'Directed'} Graph`;
    html += `${graphTitle}<br><b>${(0, comma_number_1.default)(graph.order)}</b> nodes<br><b>${(0, comma_number_1.default)(graph.size)}</b> edges`;
    return html;
}
const SYNC_REGISTRY = new Map();
/**
 * View declaration.
 */
class SigmaView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.emitter = new events_1.default();
        this.edgeWeightAttribute = null;
        this.syncHoveredNode = null;
        this.syncListeners = {};
        this.layoutSpinner = null;
        this.currentTab = 'legend';
        this.isInformationShown = true;
        this.selectedNode = null;
        this.selectedEdge = null;
        this.focusedNodes = null;
        this.selectedNodeCategoryValues = null;
        this.selectedEdgeCategoryValues = null;
    }
    render() {
        super.render();
        this.el.classList.add('ipysigma-widget');
        const height = this.model.get('height');
        let backgroundColor = this.model.get('background_color');
        // NOTE: ipywidget is performing shitty white magic in static embeds...
        if (backgroundColor === "white") {
            backgroundColor = "rgb(255, 255, 255)";
        }
        const name = this.model.get('name');
        const data = this.model.get('data');
        this.el.style.backgroundColor = backgroundColor;
        this.backgroundColor = backgroundColor;
        const graph = buildGraph(data, createRng());
        this.graph = graph;
        // Preexisting layout?
        const preexistingLayout = this.model.get('layout');
        if (preexistingLayout) {
            (0, utils_1.assignLayout)(graph, preexistingLayout);
        }
        else {
            this.saveLayout();
        }
        this.originalLayoutPositions = (0, utils_1.collectLayout)(graph);
        // Selection state
        const selectedNodeCategoryValues = this.model.get('selected_node_category_values');
        const selectedEdgeCategoryValues = this.model.get('selected_edge_category_values');
        if (selectedNodeCategoryValues)
            this.selectedNodeCategoryValues = new Set(selectedNodeCategoryValues);
        if (selectedEdgeCategoryValues)
            this.selectedEdgeCategoryValues = new Set(selectedEdgeCategoryValues);
        // Widget-side metrics
        this.edgeWeightAttribute = this.model.get('edge_weight');
        let nodeMetrics = this.model.get('node_metrics') || {};
        // NOTE: for some untractable reason, I need a completly new deep object
        nodeMetrics = JSON.parse(JSON.stringify(nodeMetrics));
        for (const attrName in nodeMetrics) {
            const metricSpec = nodeMetrics[attrName];
            const metric = metricSpec.name;
            if (metric === 'louvain') {
                const communities = (0, graphology_communities_louvain_1.default)(graph, {
                    getEdgeWeight: this.edgeWeightAttribute,
                    rng: createRng(),
                    resolution: metricSpec.resolution || 1,
                });
                metricSpec.result = communities;
                graph.updateEachNodeAttributes((node, attr) => {
                    attr[attrName] = communities[node];
                    return attr;
                }, { attributes: [attrName] });
            }
            else {
                throw new Error(`unkown metric "${metric}"` + metric);
            }
        }
        this.model.set('node_metrics', nodeMetrics);
        this.touch();
        this.el.insertAdjacentHTML('beforeend', TEMPLATE);
        this.el.style.width = '100%';
        this.el.style.height = height;
        this.container = this.el.querySelector('.ipysigma-container');
        this.container.style.width = '100%';
        this.container.style.height = height;
        // Description
        const description = this.el.querySelector('.ipysigma-graph-description');
        description.innerHTML = getGraphDescription(name, graph);
        // Camera controls
        this.zoomButton = this.el.querySelector('.ipysigma-zoom-button');
        this.unzoomButton = this.el.querySelector('.ipysigma-unzoom-button');
        this.resetZoomButton = this.el.querySelector('.ipysigma-reset-zoom-button');
        // Fullscreen controls
        this.fullscreenButton = this.el.querySelector('.ipysigma-fullscreen-button');
        // Layout controls
        this.layoutControls = this.el.querySelector('.ipysigma-layout-controls');
        this.layoutButton = this.el.querySelector('.ipysigma-layout-button');
        this.noverlapButton = this.el.querySelector('.ipysigma-noverlap-button');
        this.resetLayoutButton = this.el.querySelector('.ipysigma-reset-layout-button');
        // Search
        var searchContainer = this.el.querySelector('.ipysigma-search');
        const nodeLabelAttribute = this.model.get('visual_variables').nodeLabel.attribute;
        const options = graph.mapNodes((key, attr) => {
            let labelParts = [escapeHtml(key)];
            const label = attr[nodeLabelAttribute];
            if (label && label !== key) {
                labelParts.push(` <small style="font-size: 75%;">${escapeHtml(label)}</small>`);
            }
            return { value: key, label: labelParts.join(' ') };
        });
        this.choices = new choices_js_1.default(searchContainer, {
            allowHTML: true,
            removeItemButton: true,
            renderChoiceLimit: 10,
            choices: options,
            itemSelectText: '',
            position: 'bottom',
        });
        this.informationDisplayElement = this.el.querySelector('.ipysigma-information-display');
        this.informationShadowDisplayElement = this.el.querySelector('.ipysigma-information-shadow-display');
        this.itemInfoElement = this.el.querySelector('.ipysigma-information-contents');
        this.legendElement = this.el.querySelector('.ipysigma-legend');
        this.nodeInfoButton = this.el.querySelector('.ipysigma-information-info-button');
        this.legendButton = this.el.querySelector('.ipysigma-information-legend-button');
        this.hideInformationButton = this.el.querySelector('.ipysigma-information-hide-button');
        this.showInformationButton = this.el.querySelector('.ipysigma-information-show-button');
        this.changeInformationDisplayTab('legend');
        // Download controls
        this.downloadPNGButton = this.el.querySelector('.ipysigma-download-png-button');
        this.downloadGEXFButton = this.el.querySelector('.ipysigma-download-gexf-button');
        this.downloadSVGButton = this.el.querySelector('.ipysigma-download-svg-button');
        this.downloadJSONButton = this.el.querySelector('.ipysigma-download-json-button');
        // Waiting for widget to be mounted to register events
        this.displayed.then(() => {
            // const programSettings = this.model.get(
            //   'program_settings'
            // ) as IPysigmaProgramSettings;
            var _a, _b, _c;
            const visualVariables = this.model.get('visual_variables');
            const nodeColorSaturationEnabled = visualVariables.nodeColorSaturation.type !== 'disabled';
            const nodeBordersEnabled = visualVariables.nodeBorderColor.type !== 'disabled' &&
                (visualVariables.nodeBorderSize.type !== 'disabled' ||
                    visualVariables.nodeBorderRatio.type !== 'disabled');
            const nodePictogramsEnabled = visualVariables.nodePictogram.type !== 'disabled';
            const nodeShapeEnabled = visualVariables.nodeShape.type !== 'disabled';
            const nodeHaloEnabled = visualVariables.nodeHaloSize.type !== 'disabled' &&
                visualVariables.nodeHaloColor.type !== 'disabled';
            const edgeProgramClasses = {
                rectangle: edge_rectangle_1.default,
                line: edge_line_1.default,
                triangle: edge_triangle_1.default,
                curve: edge_curve_1.default,
            };
            const NodePictogramProgram = (0, node_pictogram_1.default)({
                correctCentering: true,
                forcedSvgSize: 384,
                keepWithinCircle: true,
            });
            const NodeShapeProgram = (0, node_pictogram_1.default)({
                correctCentering: true,
                forcedSvgSize: 384,
                keepWithinCircle: false,
            });
            const nodeProgramClasses = {
                point: node_point_1.default,
                halo: (0, node_1.createNodeCompoundProgram)([node_halo_1.default, node_point_1.default]),
                border: node_point_border_1.default,
                picto: (0, node_1.createNodeCompoundProgram)([
                    node_point_1.default,
                    NodePictogramProgram,
                ]),
                shape: NodeShapeProgram,
                'border+picto': (0, node_1.createNodeCompoundProgram)([
                    node_point_border_1.default,
                    NodePictogramProgram,
                ]),
                'border+halo': (0, node_1.createNodeCompoundProgram)([
                    node_halo_1.default,
                    node_point_border_1.default,
                ]),
                'border+halo+picto': (0, node_1.createNodeCompoundProgram)([
                    node_halo_1.default,
                    node_point_border_1.default,
                    NodePictogramProgram,
                ]),
                'halo+picto': (0, node_1.createNodeCompoundProgram)([
                    node_halo_1.default,
                    node_point_1.default,
                    NodePictogramProgram,
                ]),
            };
            const nodeHoverProgramClasses = {
                halo: node_point_1.default,
                'border+halo': node_point_border_1.default,
                'border+halo+picto': (0, node_1.createNodeCompoundProgram)([
                    node_point_border_1.default,
                    NodePictogramProgram,
                ]),
                'halo+picto': (0, node_1.createNodeCompoundProgram)([
                    node_point_1.default,
                    NodePictogramProgram,
                ]),
            };
            let rendererSettings = this.model.get('renderer_settings');
            rendererSettings = Object.assign({ hoverRenderer: custom_hover_1.default, labelRenderer: custom_label_1.default, edgeProgramClasses,
                nodeProgramClasses,
                nodeHoverProgramClasses, defaultNodeType: 'point', defaultEdgeType: 'rectangle' }, rendererSettings);
            // Gathering info about the graph to build reducers correctly
            const maxCategoricalColors = this.model.get('max_categorical_colors');
            const scaleBuilder = new visual_variables_1.VisualVariableScalesBuilder(visualVariables, maxCategoricalColors);
            scaleBuilder.readGraph(graph);
            if (!('labelRenderedSizeThreshold' in rendererSettings))
                rendererSettings.labelRenderedSizeThreshold =
                    scaleBuilder.inferLabelRenderedSizeThreshold();
            const scales = scaleBuilder.build();
            this.updateLegend(visualVariables, {
                nodeColor: (_a = scales.nodeColor) === null || _a === void 0 ? void 0 : _a.summary,
                nodeBorderColor: (_b = scales.nodeBorderColor) === null || _b === void 0 ? void 0 : _b.summary,
                edgeColor: (_c = scales.edgeColor) === null || _c === void 0 ? void 0 : _c.summary,
            });
            const nodeDisplayDataRegister = {};
            const nodeCategoryAttribute = visualVariables.nodeColor.type === 'category'
                ? visualVariables.nodeColor.attribute
                : null;
            const edgeCategoryAttribute = visualVariables.edgeColor.type === 'category'
                ? visualVariables.edgeColor.attribute
                : null;
            const edgeColorFrom = visualVariables.edgeColor.type === 'dependent'
                ? visualVariables.edgeColor.value
                : null;
            const nodeBorderColorFrom = visualVariables.nodeBorderColor.type === 'dependent'
                ? visualVariables.nodeBorderColor.value
                : undefined;
            // Node reducer
            rendererSettings.nodeReducer = (node, data) => {
                const displayData = {
                    x: data.x,
                    y: data.y,
                };
                // Visual variables
                const categoryValue = nodeCategoryAttribute
                    ? data[nodeCategoryAttribute]
                    : undefined;
                if (categoryValue !== undefined) {
                    displayData.categoryValue = categoryValue;
                }
                displayData.color = scales.nodeColor(data);
                displayData.size = scales.nodeSize(data);
                displayData.label = (scales.nodeLabel(data) || node);
                displayData.labelSize = scales.nodeLabelSize(data);
                displayData.labelColor = scales.nodeLabelColor(data);
                if (nodeColorSaturationEnabled) {
                    const color = (0, chroma_js_1.default)(displayData.color);
                    displayData.color = color
                        .set('lch.c', color.get('lch.c') * scales.nodeColorSaturation(data))
                        .hex();
                }
                if (nodeBordersEnabled) {
                    if (visualVariables.nodeBorderRatio.type !== 'disabled')
                        displayData.borderRatio = scales.nodeBorderRatio(data);
                    else {
                        displayData.borderSize = scales.nodeBorderSize(data);
                        displayData.size += displayData.borderSize;
                    }
                    if (nodeBorderColorFrom) {
                        displayData.borderColor = (0, chroma_js_1.default)(displayData.color).darken().hex();
                    }
                    else {
                        displayData.borderColor = scales.nodeBorderColor(data);
                    }
                }
                if (nodePictogramsEnabled) {
                    displayData.pictogram = (0, utils_2.pictogramToUrl)((0, shapes_1.shapeToPicto)(scales.nodePictogram(data)) || 'circle');
                    displayData.pictogramColor = scales.nodePictogramColor(data);
                }
                if (nodeShapeEnabled) {
                    displayData.pictogram = (0, utils_2.pictogramToUrl)((0, shapes_1.shapeToPicto)(scales.nodeShape(data)) || 'circle', 'wght700fill1');
                    displayData.pictogramColor = displayData.color;
                }
                if (nodeHaloEnabled) {
                    const haloSize = scales.nodeHaloSize(data);
                    if (haloSize !== 0) {
                        displayData.haloSize = displayData.size + haloSize;
                    }
                    else {
                        displayData.haloSize = 0;
                    }
                    displayData.haloColor = scales.nodeHaloColor(data);
                }
                // Transient state
                if (node === this.selectedNode || node === this.syncHoveredNode) {
                    displayData.highlighted = true;
                }
                if ((this.focusedNodes && !this.focusedNodes.has(node)) ||
                    (this.selectedNodeCategoryValues &&
                        !this.selectedNodeCategoryValues.has(categoryValue))) {
                    if (!nodeShapeEnabled) {
                        displayData.type = 'point';
                        displayData.color = MUTED_NODE_COLOR;
                    }
                    else {
                        displayData.pictogramColor = MUTED_NODE_COLOR;
                    }
                    displayData.zIndex = 0;
                    displayData.size = displayData.size ? displayData.size / 2 : 1;
                    displayData.hoverLabel = displayData.label;
                    displayData.label = '';
                }
                else {
                    displayData.zIndex = 1;
                }
                nodeDisplayDataRegister[node] = displayData;
                return displayData;
            };
            // Edge reducer
            rendererSettings.edgeReducer = (edge, data) => {
                var _a, _b;
                const displayData = {};
                const [source, target] = graph.extremities(edge);
                // Visual variables
                const categoryValue = edgeCategoryAttribute
                    ? data[edgeCategoryAttribute]
                    : null;
                if (edgeColorFrom) {
                    displayData.color =
                        nodeDisplayDataRegister[edgeColorFrom === 'source' ? source : target].color;
                }
                else {
                    displayData.color = scales.edgeColor(data);
                }
                displayData.size = scales.edgeSize(data);
                if (scales.edgeLabel)
                    displayData.label = scales.edgeLabel(data);
                if (rendererSettings.defaultEdgeType === 'curve') {
                    displayData.curveness = scales.edgeCurveness(data);
                }
                // Transient state
                if (this.selectedNode && this.focusedNodes) {
                    if (source !== this.selectedNode && target !== this.selectedNode) {
                        displayData.hidden = true;
                    }
                }
                if (this.selectedNodeCategoryValues) {
                    if (!this.selectedNodeCategoryValues.has((_a = nodeDisplayDataRegister[source]) === null || _a === void 0 ? void 0 : _a.categoryValue) &&
                        !this.selectedNodeCategoryValues.has((_b = nodeDisplayDataRegister[target]) === null || _b === void 0 ? void 0 : _b.categoryValue)) {
                        displayData.hidden = true;
                    }
                }
                if (this.selectedEdgeCategoryValues) {
                    if (!this.selectedEdgeCategoryValues.has(categoryValue)) {
                        displayData.hidden = true;
                    }
                }
                if (this.selectedEdge) {
                    displayData.hidden = edge !== this.selectedEdge;
                }
                return displayData;
            };
            this.renderer = new sigma_1.default(graph, this.container, rendererSettings);
            const uiSettings = this.model.get('ui_settings');
            const initialCameraState = this.model.get('camera_state');
            this.renderer.getCamera().setState(initialCameraState);
            const selectedNode = this.model.get('selected_node');
            const selectedEdge = this.model.get('selected_edge');
            if (selectedNode)
                this.selectItem('node', selectedNode);
            else if (selectedEdge)
                this.selectItem('edge', graph.edge(selectedEdge[0], selectedEdge[1]));
            else
                this.clearSelectedItem();
            if (uiSettings.hideInfoPanel)
                this.toggleInformationDisplay();
            if (uiSettings.hideSearch) {
                this.choices.destroy();
                hide(searchContainer);
                this.informationDisplayElement.classList.add('full');
            }
            this.bindMessageHandlers();
            this.bindRendererHandlers();
            this.bindChoicesHandlers();
            this.bindInformationDisplayHandlers();
            this.bindDownloadHandlers();
            this.bindCameraHandlers();
            this.bindFullscreenHandlers();
            this.bindLayoutHandlers();
            this.syncKey = this.model.get('sync_key');
            if (this.syncKey) {
                const currentSyncEntry = SYNC_REGISTRY.get(this.syncKey);
                if (!currentSyncEntry) {
                    const emitter = new events_1.default();
                    SYNC_REGISTRY.set(this.syncKey, {
                        emitter,
                        renderers: new Set([this.renderer]),
                    });
                    this.bindSyncEvents(emitter);
                }
                else {
                    currentSyncEntry.renderers.add(this.renderer);
                    this.bindSyncEvents(currentSyncEntry.emitter);
                }
            }
        });
    }
    renderSnapshot() {
        this.model.set('snapshot', (0, utils_2.renderAsDataURL)(this.renderer));
        this.touch();
    }
    saveCameraState(state) {
        this.model.set('camera_state', state);
        this.touch();
    }
    saveLayout() {
        const mapping = (0, utils_1.collectLayout)(this.graph);
        this.model.set('layout', mapping);
        this.touch();
    }
    resetLayout() {
        this.model.set('layout', this.originalLayoutPositions);
        this.touch();
    }
    changeInformationDisplayTab(tab) {
        if (tab === 'legend') {
            hide(this.itemInfoElement);
            show(this.legendElement);
            this.legendButton.classList.remove('selectable');
            this.nodeInfoButton.classList.add('selectable');
        }
        else {
            hide(this.legendElement);
            show(this.itemInfoElement);
            this.legendButton.classList.add('selectable');
            this.nodeInfoButton.classList.remove('selectable');
        }
    }
    toggleInformationDisplay() {
        var _a, _b;
        if (this.isInformationShown) {
            // Hiding
            hide(this.informationDisplayElement);
            show(this.informationShadowDisplayElement);
            (_a = this.el.querySelector('.ipysigma-right-panel')) === null || _a === void 0 ? void 0 : _a.classList.add('hidden');
            this.isInformationShown = false;
        }
        else {
            // Showing
            show(this.informationDisplayElement);
            hide(this.informationShadowDisplayElement);
            (_b = this.el
                .querySelector('.ipysigma-right-panel')) === null || _b === void 0 ? void 0 : _b.classList.remove('hidden');
            this.isInformationShown = true;
        }
    }
    updateLegend(variables, summaries) {
        const categoryMap = new Map();
        let dataId = 0;
        function renderLegend(type, title, variable, summary, defaultColor) {
            if (variable.type === 'disabled' || variable.type === 'constant')
                return null;
            let html = `<b>${title}</b><br>`;
            if (variable.type === 'dependent') {
                html += `based on <span class="ipysigma-keyword">${variable.value}</span> color`;
            }
            else {
                const source = variable.attribute.startsWith(IPYSIGMA_KWARG_PREFIX)
                    ? 'kwarg'
                    : 'attribute';
                const name = variable.attribute.startsWith(IPYSIGMA_KWARG_PREFIX)
                    ? variable.attribute.slice(IPYSIGMA_KWARG_PREFIX.length)
                    : variable.attribute;
                if (variable.type === 'raw') {
                    html += `<span class="ipysigma-keyword">${escapeHtml(name)}</span> ${source}`;
                }
                else if (variable.type === 'continuous') {
                    html += `<span class="ipysigma-keyword">${escapeHtml(name)}</span> ${source} `;
                    if (typeof variable.range === 'string') {
                        html += `(using the <span class="ipysigma-keyword">${variable.range}</span> color scheme)`;
                    }
                    else if (typeof variable.range[0] === 'number') {
                        html += `(scaled to <span class="ipysigma-number">${variable.range[0]}</span>-<span class="ipysigma-number">${variable.range[1]}</span> px)`;
                    }
                    else {
                        html += `(from <span style="color: ${variable.range[0]}">■</span> ${variable.range[0]} to <span style="color: ${variable.range[1]}">■</span> ${variable.range[1]})`;
                    }
                }
                else {
                    html += `<span class="ipysigma-keyword">${escapeHtml(name)}</span> ${source} as a category:`;
                    const paletteItems = [];
                    if (summary && summary.kind === 'color') {
                        const values = [];
                        categoryMap.set(dataId, { type, values });
                        let i = 0;
                        summary.palette.forEach((color, value) => {
                            values.push(value);
                            paletteItems.push(`<span title="click to filter" class="category" data-key="${dataId}" data-index="${i++}"><span style="color: ${color}">■</span> <span class="category-value">${value}</span></span>`);
                        });
                        dataId++;
                        if (summary.overflowing) {
                            paletteItems.push(`<span style="color: ${summary.palette.defaultValue}">■</span> ...`);
                        }
                    }
                    else {
                        paletteItems.push(`<span style="color: ${defaultColor}">■</span> default`);
                    }
                    html += '<br>' + paletteItems.join('<br>');
                }
            }
            return html;
        }
        const items = [
            renderLegend('node', 'Node labels', variables.nodeLabel),
            renderLegend('node', 'Node colors', variables.nodeColor, summaries.nodeColor),
            renderLegend('node', 'Node border colors', variables.nodeBorderColor, summaries.nodeBorderColor),
            renderLegend('node', 'Node sizes', variables.nodeSize),
            renderLegend('edge', 'Edge colors', variables.edgeColor, summaries.edgeColor),
            renderLegend('edge', 'Edge sizes', variables.edgeSize),
            renderLegend('edge', 'Edge labels', variables.edgeLabel),
        ];
        this.legendElement.innerHTML = items.filter((l) => l).join('<hr>');
        // Binding category span events
        function getSpanInfo(span) {
            const key = +span.getAttribute('data-key');
            const index = +span.getAttribute('data-index');
            const record = categoryMap.get(key);
            if (!record)
                throw new Error('error registering category span click event handlers');
            return { type: record.type, value: record.values[index] };
        }
        const categorySpans = this.legendElement.querySelectorAll('.category');
        const updateSpans = () => {
            categorySpans.forEach((span) => {
                const { type, value } = getSpanInfo(span);
                if (type === 'node') {
                    if (!this.selectedNodeCategoryValues ||
                        this.selectedNodeCategoryValues.has(value)) {
                        span.classList.remove('evicted');
                    }
                    else {
                        span.classList.add('evicted');
                    }
                }
                else if (type === 'edge') {
                    if (!this.selectedEdgeCategoryValues ||
                        this.selectedEdgeCategoryValues.has(value)) {
                        span.classList.remove('evicted');
                    }
                    else {
                        span.classList.add('evicted');
                    }
                }
            });
        };
        categorySpans.forEach((span) => {
            span.onclick = () => {
                const { type, value } = getSpanInfo(span);
                const relatedPaletteCount = (type === 'node' ? summaries.nodeColor : summaries.edgeColor);
                this.toggleCategoryValue(type, relatedPaletteCount.palette.size, value);
                updateSpans();
                this.renderer.refresh();
            };
        });
        updateSpans();
    }
    clearSelectedItem() {
        this.selectedEdge = null;
        this.selectedNode = null;
        this.focusedNodes = null;
        this.syncHoveredNode = null;
        this.choices.setChoiceByValue('');
        if (this.model.get('clickable_edges')) {
            this.itemInfoElement.innerHTML =
                '<i>Click on a node/edge or search a node to display information about it...</i>';
        }
        else {
            this.itemInfoElement.innerHTML =
                '<i>Click on a node or search a node to display information about it...</i>';
        }
        this.changeInformationDisplayTab('legend');
        this.model.set('selected_node', null);
        this.model.set('selected_edge', null);
        this.touch();
        this.renderer.refresh();
        this.emitter.emit('clearSelectedItem');
    }
    toggleCategoryValue(type, max, value) {
        let target = type === 'node'
            ? this.selectedNodeCategoryValues
            : this.selectedEdgeCategoryValues;
        if (!target) {
            target = new Set([value]);
        }
        else if (target.size === max - 1) {
            target = null;
        }
        else if (target.has(value)) {
            if (target.size === 1) {
                target = null;
            }
            else {
                target.delete(value);
            }
        }
        else {
            target.add(value);
        }
        const update = target ? Array.from(target) : null;
        if (type === 'node') {
            this.selectedNodeCategoryValues = target;
            this.model.set('selected_node_category_values', update);
        }
        else {
            this.selectedEdgeCategoryValues = target;
            this.model.set('selected_edge_category_values', update);
        }
        this.touch();
    }
    selectItem(type, key) {
        const graph = this.graph;
        if (type === 'node') {
            this.selectedEdge = null;
            this.selectedNode = key;
            const focusedNodes = new Set();
            focusedNodes.add(this.selectedNode);
            graph.forEachNeighbor(key, (neighbor) => {
                focusedNodes.add(neighbor);
            });
            this.focusedNodes = focusedNodes;
            this.choices.setChoiceByValue(key);
            this.model.set('selected_node', key);
            this.model.set('selected_edge', null);
        }
        else {
            const extremities = graph.extremities(key);
            this.selectedEdge = key;
            this.selectedNode = null;
            this.focusedNodes = new Set(extremities);
            this.choices.setChoiceByValue('');
            this.model.set('selected_edge', extremities);
            this.model.set('selected_node', null);
        }
        this.touch();
        const attr = type === 'node'
            ? graph.getNodeAttributes(key)
            : graph.getEdgeAttributes(key);
        let innerHTML = '';
        if (type === 'node') {
            innerHTML += `<b>Node</b> <i>${renderTypedValue(key)}</i>`;
        }
        else {
            const [source, target] = this.graph.extremities(key);
            innerHTML += '<b>Edge</b>';
            if (!key.startsWith('geid_'))
                innerHTML += ` <i>${renderTypedValue(key)}</i>`;
            innerHTML += `<br>from ${renderTypedValue(source)} to ${renderTypedValue(target)}`;
        }
        const kwargInfo = [];
        const vizInfo = [];
        const info = [];
        const vizAttributes = type === 'node' ? NODE_VIZ_ATTRIBUTES : EDGE_VIZ_ATTRIBUTES;
        for (let k in attr) {
            let target = info;
            if (vizAttributes.has(k))
                target = vizInfo;
            else if (k.startsWith(IPYSIGMA_KWARG_PREFIX))
                target = kwargInfo;
            target.push(`<b>${k.startsWith(IPYSIGMA_KWARG_PREFIX)
                ? k.slice(IPYSIGMA_KWARG_PREFIX.length)
                : k}</b> ${renderTypedValue(attr[k])}`);
        }
        if (kwargInfo.length !== 0)
            innerHTML += '<hr>From kwargs:<br>' + kwargInfo.join('<br>');
        if (info.length !== 0)
            innerHTML += `<hr>Attributes:<br>` + info.join('<br>');
        if (vizInfo.length !== 0)
            innerHTML += '<hr>Known viz data:<br>' + vizInfo.join('<br>');
        if (type === 'node') {
            innerHTML += '<hr>Computed metrics:<br>';
            innerHTML += `<b>degree</b> ${renderTypedValue(graph.degree(key))}<br>`;
            if (graph.directedSize !== 0) {
                innerHTML += `<b>indegree</b> ${renderTypedValue(graph.inDegree(key))}<br>`;
                innerHTML += `<b>outdegree</b> ${renderTypedValue(graph.outDegree(key))}<br>`;
            }
        }
        this.itemInfoElement.innerHTML = innerHTML;
        this.changeInformationDisplayTab('info');
        this.renderer.refresh();
        this.emitter.emit('selectItem', { type, key });
    }
    moveCameraToNode(node) {
        const pos = this.renderer.getNodeDisplayData(node);
        if (!pos)
            return;
        this.renderer.getCamera().animate(pos, { duration: 500 });
    }
    bindMessageHandlers() {
        this.model.on('msg:custom', (content) => {
            if (content.msg === 'render_snapshot') {
                this.renderSnapshot();
            }
        });
    }
    bindRendererHandlers() {
        const debouncedSaveCameraState = (0, debounce_1.default)(this.saveCameraState.bind(this), 500);
        this.renderer.getCamera().on('updated', (state) => {
            debouncedSaveCameraState(state);
        });
        let hoveredCount = 0;
        this.renderer.on('enterNode', () => {
            hoveredCount++;
            this.container.style.cursor = 'pointer';
        });
        this.renderer.on('leaveNode', () => {
            hoveredCount--;
            if (hoveredCount === 0)
                this.container.style.cursor = 'default';
        });
        this.renderer.on('clickNode', ({ node }) => {
            if (node === this.selectedNode)
                return;
            this.selectItem('node', node);
        });
        this.renderer.on('clickStage', () => {
            if (!this.selectedNode && !this.selectedEdge)
                return;
            this.clearSelectedItem();
        });
        if (this.model.get('clickable_edges')) {
            this.renderer.on('enterEdge', () => {
                hoveredCount++;
                this.container.style.cursor = 'pointer';
            });
            this.renderer.on('leaveEdge', () => {
                hoveredCount--;
                if (hoveredCount === 0)
                    this.container.style.cursor = 'default';
            });
            this.renderer.on('clickEdge', ({ edge }) => {
                if (edge === this.selectedEdge)
                    return;
                this.selectItem('edge', edge);
            });
        }
    }
    bindChoicesHandlers() {
        this.choices.passedElement.element.addEventListener('change', (event) => {
            const node = event.detail.value;
            if (node === this.selectedNode)
                return;
            if (!node)
                return this.clearSelectedItem();
            this.selectItem('node', node);
            // We don't need to move the camera if we are fully unzoomed
            if (this.renderer.getCamera().getState().ratio >= 1)
                return;
            this.moveCameraToNode(node);
        });
    }
    bindInformationDisplayHandlers() {
        this.legendButton.onclick = () => {
            if (!this.legendButton.classList.contains('selectable'))
                return;
            this.changeInformationDisplayTab('legend');
        };
        this.nodeInfoButton.onclick = () => {
            if (!this.nodeInfoButton.classList.contains('selectable'))
                return;
            this.changeInformationDisplayTab('info');
        };
        this.hideInformationButton.onclick = () => {
            this.toggleInformationDisplay();
        };
        this.showInformationButton.onclick = () => {
            this.toggleInformationDisplay();
        };
    }
    bindDownloadHandlers() {
        this.downloadPNGButton.onclick = () => {
            (0, utils_2.saveAsPNG)(this.renderer);
        };
        this.downloadGEXFButton.onclick = () => {
            (0, utils_2.saveAsGEXF)(this.renderer);
        };
        this.downloadSVGButton.onclick = () => {
            (0, utils_2.saveAsSVG)(this.renderer);
        };
        this.downloadJSONButton.onclick = () => {
            (0, utils_2.saveAsJSON)(this.renderer);
        };
    }
    bindCameraHandlers() {
        this.zoomButton.onclick = () => {
            this.renderer.getCamera().animatedZoom();
        };
        this.unzoomButton.onclick = () => {
            this.renderer.getCamera().animatedUnzoom();
        };
        this.resetZoomButton.onclick = () => {
            this.renderer.getCamera().animatedReset();
        };
    }
    bindFullscreenHandlers() {
        const enter = () => {
            this.el.style.height = '100%';
            this.el.style.backgroundColor = this.backgroundColor;
            this.container.style.height = '100%';
            this.container.style.backgroundColor = this.backgroundColor;
            this.fullscreenButton.innerHTML = icons_1.fullscreenExitIcon;
            this.fullscreenButton.setAttribute('title', 'exit fullscreen');
            this.renderer.scheduleRefresh();
        };
        const exit = () => {
            const targetHeight = this.model.get('height');
            this.el.style.backgroundColor = this.backgroundColor;
            this.el.style.height = targetHeight;
            this.container.style.height = targetHeight;
            this.container.style.backgroundColor = this.backgroundColor;
            this.fullscreenButton.innerHTML = icons_1.fullscreenEnterIcon;
            this.fullscreenButton.setAttribute('title', 'enter fullscreen');
            this.renderer.scheduleRefresh();
        };
        screenfull_1.default.onchange(() => {
            if (screenfull_1.default.isFullscreen)
                enter();
            else
                exit();
        });
        this.fullscreenButton.onclick = () => {
            if (screenfull_1.default.isFullscreen) {
                screenfull_1.default.exit();
            }
            else {
                screenfull_1.default.request(this.el);
            }
        };
    }
    bindLayoutHandlers() {
        const graph = this.graph;
        const renderer = this.renderer;
        let settings = (this.model.get('layout_settings') ||
            {});
        const inferredSettings = graphology_layout_forceatlas2_1.default.inferSettings(graph);
        settings = Object.assign(inferredSettings, settings);
        this.layout = new worker_1.default(graph, {
            settings,
            getEdgeWeight: this.edgeWeightAttribute,
        });
        this.noverlap = new worker_2.default(graph, {
            inputReducer(key, attr) {
                var _a;
                const pos = renderer.graphToViewport(attr);
                return {
                    x: pos.x,
                    y: pos.y,
                    size: (_a = renderer.getNodeDisplayData(key)) === null || _a === void 0 ? void 0 : _a.size,
                };
            },
            outputReducer(key, attr) {
                return renderer.viewportToGraph(attr);
            },
            onConverged() {
                stopNoverlap(true);
            },
            settings: { ratio: 1, margin: 3 },
        });
        hide(this.resetLayoutButton);
        let layoutStoppingTimeout = null;
        const stopLayout = () => {
            if (layoutStoppingTimeout)
                clearTimeout(layoutStoppingTimeout);
            layoutStoppingTimeout = null;
            if (this.layoutSpinner) {
                this.layoutControls.removeChild(this.layoutSpinner[0]);
                this.layoutSpinner[1]();
                this.layoutSpinner = null;
            }
            this.layoutButton.innerHTML = icons_1.playIcon;
            this.layoutButton.setAttribute('title', 'start layout');
            this.layout.stop();
            this.saveLayout();
            enable(this.noverlapButton);
            show(this.resetLayoutButton);
        };
        const startLayout = () => {
            this.layoutSpinner = createSpinner();
            this.layoutButton.innerHTML = icons_1.pauseIcon;
            this.layoutControls.appendChild(this.layoutSpinner[0]);
            this.layoutButton.setAttribute('title', 'stop layout');
            this.layout.start();
            disable(this.noverlapButton);
            hide(this.resetLayoutButton);
        };
        const stopNoverlap = (disableButton = false) => {
            if (this.layoutSpinner) {
                this.layoutControls.removeChild(this.layoutSpinner[0]);
                this.layoutSpinner[1]();
                this.layoutSpinner = null;
            }
            this.noverlapButton.innerHTML = icons_1.scatterIcon;
            this.noverlapButton.setAttribute('title', 'spread nodes');
            this.noverlap.stop();
            this.saveLayout();
            enable(this.layoutButton);
            show(this.resetLayoutButton);
            if (disableButton)
                disable(this.noverlapButton);
        };
        const startNoverlap = () => {
            this.layoutSpinner = createSpinner();
            this.noverlapButton.innerHTML = icons_1.pauseIcon;
            this.layoutControls.appendChild(this.layoutSpinner[0]);
            this.noverlapButton.setAttribute('title', 'stop');
            this.noverlap.start();
            disable(this.layoutButton);
            hide(this.resetLayoutButton);
        };
        const resetLayout = () => {
            enable(this.noverlapButton);
            hide(this.resetLayoutButton);
            this.resetLayout();
            (0, animate_1.animateNodes)(graph, this.originalLayoutPositions, { duration: 250 });
        };
        if (this.model.get('start_layout')) {
            const seconds = this.model.get('start_layout_for_seconds');
            if (seconds) {
                layoutStoppingTimeout = setTimeout(() => {
                    stopLayout();
                }, seconds * 1000);
            }
            startLayout();
        }
        this.layoutButton.onclick = () => {
            if (this.layout.isRunning()) {
                stopLayout();
            }
            else {
                startLayout();
            }
        };
        this.noverlapButton.onclick = () => {
            if (this.noverlap.isRunning()) {
                stopNoverlap();
            }
            else {
                startNoverlap();
            }
        };
        this.resetLayoutButton.onclick = () => {
            resetLayout();
        };
    }
    bindSyncEvents(syncEmitter) {
        let locks = {
            camera: false,
            nodeAttributesUpdated: false,
            eachNodeAttributesUpdated: false,
            selectItem: false,
            clearSelectedItem: false,
        };
        const syncTargets = new Set(this.model.get('sync_targets'));
        // NOTE: all of this is very sketchy. This is here to make suuuure we
        // don't encounter a dead lock.
        const resetLocks = () => {
            for (const k in locks)
                locks[k] = false;
        };
        let resetLockFrame = null;
        const scheduleResetLocks = () => {
            if (resetLockFrame)
                return;
            resetLockFrame = setTimeout(() => {
                resetLockFrame = null;
                resetLocks();
            }, 0);
        };
        const lock = (name) => {
            locks[name] = true;
            scheduleResetLocks();
        };
        const camera = this.renderer.getCamera();
        const graph = this.renderer.getGraph();
        // Camera
        if (syncTargets.has('camera')) {
            camera.on('updated', (state) => {
                if (locks.camera) {
                    locks.camera = false;
                    return;
                }
                syncEmitter.emit('camera', { state, renderer: this.renderer });
            });
            this.syncListeners.camera = ({ state, renderer }) => {
                if (renderer === this.renderer)
                    return;
                lock('camera');
                camera.setState(state);
            };
        }
        // Layout
        if (syncTargets.has('layout')) {
            graph.on('nodeAttributesUpdated', ({ key, attributes }) => {
                if (locks.nodeAttributesUpdated) {
                    locks.nodeAttributesUpdated = false;
                    return;
                }
                syncEmitter.emit('nodePosition', {
                    node: key,
                    position: { x: attributes.x, y: attributes.y },
                    renderer: this.renderer,
                });
            });
            graph.on('eachNodeAttributesUpdated', () => {
                if (locks.eachNodeAttributesUpdated) {
                    locks.eachNodeAttributesUpdated = false;
                    return;
                }
                syncEmitter.emit('layout', {
                    layout: (0, utils_1.collectLayout)(graph),
                    renderer: this.renderer,
                });
            });
            this.syncListeners.layout = ({ layout, renderer }) => {
                if (renderer === this.renderer)
                    return;
                lock('eachNodeAttributesUpdated');
                (0, utils_1.assignLayout)(graph, layout);
            };
            this.syncListeners.nodePosition = ({ node, position, renderer }) => {
                if (renderer === this.renderer)
                    return;
                lock('nodeAttributesUpdated');
                graph.mergeNodeAttributes(node, position);
            };
        }
        // Selection
        if (syncTargets.has('selection')) {
            this.emitter.on('selectItem', (payload) => {
                if (locks.selectItem) {
                    locks.selectItem = false;
                    return;
                }
                const type = payload.type;
                let key = payload.key;
                if (type === 'edge') {
                    key = this.graph.extremities(key);
                }
                syncEmitter.emit('selectItem', { type, key, renderer: this.renderer });
            });
            this.emitter.on('clearSelectedItem', () => {
                if (locks.clearSelectedItem) {
                    locks.clearSelectedItem = false;
                    return;
                }
                syncEmitter.emit('clearSelectedItem', { renderer: this.renderer });
            });
            this.syncListeners.selectItem = ({ renderer, key, type }) => {
                if (renderer === this.renderer)
                    return;
                lock('selectItem');
                if (type === 'edge')
                    key = this.graph.edge(key[0], key[1]);
                this.selectItem(type, key);
            };
            this.syncListeners.clearSelectedItem = ({ renderer }) => {
                if (renderer === this.renderer)
                    return;
                lock('clearSelectedItem');
                this.clearSelectedItem();
            };
        }
        // Hover
        if (syncTargets.has('hover')) {
            this.renderer.on('enterNode', ({ node }) => {
                syncEmitter.emit('enterNode', { node, renderer: this.renderer });
            });
            this.renderer.on('leaveNode', ({ node }) => {
                syncEmitter.emit('leaveNode', { node, renderer: this.renderer });
            });
            this.syncListeners.enterNode = ({ node, renderer }) => {
                if (renderer === this.renderer)
                    return;
                this.syncHoveredNode = node;
                this.renderer.scheduleRefresh();
            };
            this.syncListeners.leaveNode = ({ renderer }) => {
                if (renderer === this.renderer)
                    return;
                this.syncHoveredNode = null;
                this.renderer.scheduleRefresh();
            };
        }
        // Registering events
        for (const eventName in this.syncListeners) {
            syncEmitter.on(eventName, this.syncListeners[eventName]);
        }
    }
    remove() {
        // Cleanup to avoid leaks and free GPU slots
        if (this.renderer)
            this.renderer.kill();
        if (this.layout)
            this.layout.kill();
        if (this.noverlap)
            this.noverlap.kill();
        if (this.syncKey) {
            const syncEntry = SYNC_REGISTRY.get(this.syncKey);
            if (!syncEntry) {
                throw new Error('sync entry not found on remove. this should not happen!');
            }
            if (syncEntry.renderers.size > 1) {
                syncEntry.renderers.delete(this.renderer);
                for (const eventName in this.syncListeners) {
                    syncEntry.emitter.removeListener(eventName, this.syncListeners[eventName]);
                }
            }
            else {
                syncEntry.emitter.removeAllListeners();
                SYNC_REGISTRY.delete(this.syncKey);
            }
        }
        this.emitter.removeAllListeners();
        super.remove();
    }
}
exports.SigmaView = SigmaView;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/* Choices.js overrides */
.ipysigma-widget .choices {
  margin-bottom: 5px;
}

.ipysigma-widget .choices__inner {
  border-radius: 0;
  background-color: white;
  border: 1px solid #e0e0e0;
  box-sizing: border-box;
  padding-right: 50px;
}

.ipysigma-widget .choices__item--selectable {
  padding-right: 0px !important;
}

.ipysigma-widget .choices__item {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

/* Ipysigma own styles */
.ipysigma-widget {
  /* Background color is now set by widget directly! */
  /* background-color: white; */
  margin: 0;
  padding: 0;
  border: 1px solid #e0e0e0;
  font-family: sans-serif;
  color: black;
}

.ipysigma-widget ~ .ipysigma-widget {
  border-left: none;
}

.widget-hbox ~ .widget-hbox .ipysigma-widget {
  border-top: none;
}

.ipysigma-widget hr {
  height: 1px;
  border: none;
  background-color: #e0e0e0;
  margin-top: 6px;
  margin-bottom: 6px;
}

.ipysigma-widget .ipysigma-left-panel {
  position: absolute;
  top: 10px;
  left: 10px;
}

.ipysigma-widget .ipysigma-right-panel {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 250px;
  height: 100%;
}

.ipysigma-widget .ipysigma-right-panel.hidden {
  pointer-events: none;
}

.ipysigma-widget .ipysigma-graph-description {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 5px 10px;
  font-size: 12px;
  /* font-style: italic; */
  line-height: 16px;
}

.ipysigma-widget .ipysigma-button {
  cursor: pointer;
  text-align: center;
  background-color: white;
  border: 1px solid #e0e0e0;
  user-select: none;
}

.ipysigma-widget .ipysigma-button.disabled {
  border: none;
  cursor: default;
}

.ipysigma-widget .ipysigma-button.disabled svg {
  fill: #efefef;
}

.ipysigma-widget .ipysigma-button:hover {
  border-color: grey;
}

.ipysigma-widget .ipysigma-svg-icon {
  width: 32px;
  height: 32px;
  font-size: 24px;
  line-height: 30px;
  box-sizing: border-box;
}

.ipysigma-widget .ipysigma-zoom-button {
  margin-top: 10px;
}

.ipysigma-widget .ipysigma-unzoom-button {
  margin-top: 10px;
}

.ipysigma-widget .ipysigma-reset-zoom-button {
  margin-top: 10px;
}

.ipysigma-widget .ipysigma-fullscreen-button {
  margin-top: 10px;
}

.ipysigma-widget .ipysigma-layout-controls {
  width: 100%;
  margin-top: 10px;
  display: flex;
}

.ipysigma-widget .ipysigma-reset-layout-button,
.ipysigma-widget .ipysigma-noverlap-button {
  margin-left: 4px;
}

.ipysigma-widget .ipysigma-spinner {
  font-size: 20px;
  padding-left: 5px;
  line-height: 26px;
}

.ipysigma-widget .ipysigma-tab-button.selectable {
  color: cornflowerblue;
  text-decoration: underline;
  cursor: pointer;
}

.ipysigma-widget .ipysigma-information-display {
  width: 100%;
  height: calc(100% - 45px - 5px - 20px - 25px);
  overflow-y: auto;
  background-color: white;
  border: 1px solid #e0e0e0;
  box-sizing: border-box;
  font-size: 12px;
  line-height: 16px;
  padding: 10px;
}

.ipysigma-widget .ipysigma-information-display.full {
  height: calc(100% - 20px - 25px);
}

.ipysigma-widget .ipysigma-information-shadow-display {
  width: 100%;
  overflow-y: auto;
  box-sizing: border-box;
  font-size: 12px;
  line-height: 16px;
  padding: 10px;
}

.ipysigma-widget .ipysigma-information-hide-button,
.ipysigma-widget .ipysigma-information-show-button {
  float: right;
  cursor: pointer;
}

.ipysigma-widget .ipysigma-information-contents,
.ipysigma-widget .ipysigma-legend {
  font-family: monospace;
}

.ipysigma-widget .ipysigma-string {
  color: #bc2828;
}

.ipysigma-widget .ipysigma-number {
  color: #008800;
}

.ipysigma-widget .ipysigma-boolean,
.ipysigma-widget .ipysigma-keyword {
  color: #0457ab;
}

.ipysigma-widget .ipysigma-download-controls {
  margin-top: 5px;
  display: flex;
  text-align: right;
  position: absolute;
  bottom: 20px;
  right: 0px;
}

.ipysigma-widget .ipysigma-download-png-button,
.ipysigma-widget .ipysigma-download-svg-button,
.ipysigma-widget .ipysigma-download-gexf-button {
  margin-right: 3px;
}

.ipysigma-widget .category {
  cursor: pointer;
}
.ipysigma-widget .category.evicted .category-value {
  color: gray;
  text-decoration: line-through;
}

.ipysigma-widget .ipysigma-search,
.ipysigma-widget .ipysigma-download-controls,
.ipysigma-widget .ipysigma-information-shadow-display,
.ipysigma-widget .choices {
  pointer-events: auto;
}
`, "",{"version":3,"sources":["webpack://./css/widget.css"],"names":[],"mappings":"AAAA,yBAAyB;AACzB;EACE,kBAAkB;AACpB;;AAEA;EACE,gBAAgB;EAChB,uBAAuB;EACvB,yBAAyB;EACzB,sBAAsB;EACtB,mBAAmB;AACrB;;AAEA;EACE,6BAA6B;AAC/B;;AAEA;EACE,uBAAuB;EACvB,gBAAgB;EAChB,mBAAmB;AACrB;;AAEA,wBAAwB;AACxB;EACE,oDAAoD;EACpD,6BAA6B;EAC7B,SAAS;EACT,UAAU;EACV,yBAAyB;EACzB,uBAAuB;EACvB,YAAY;AACd;;AAEA;EACE,iBAAiB;AACnB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,WAAW;EACX,YAAY;EACZ,yBAAyB;EACzB,eAAe;EACf,kBAAkB;AACpB;;AAEA;EACE,kBAAkB;EAClB,SAAS;EACT,UAAU;AACZ;;AAEA;EACE,kBAAkB;EAClB,SAAS;EACT,WAAW;EACX,YAAY;EACZ,YAAY;AACd;;AAEA;EACE,oBAAoB;AACtB;;AAEA;EACE,uBAAuB;EACvB,yBAAyB;EACzB,iBAAiB;EACjB,eAAe;EACf,wBAAwB;EACxB,iBAAiB;AACnB;;AAEA;EACE,eAAe;EACf,kBAAkB;EAClB,uBAAuB;EACvB,yBAAyB;EACzB,iBAAiB;AACnB;;AAEA;EACE,YAAY;EACZ,eAAe;AACjB;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,WAAW;EACX,YAAY;EACZ,eAAe;EACf,iBAAiB;EACjB,sBAAsB;AACxB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,WAAW;EACX,gBAAgB;EAChB,aAAa;AACf;;AAEA;;EAEE,gBAAgB;AAClB;;AAEA;EACE,eAAe;EACf,iBAAiB;EACjB,iBAAiB;AACnB;;AAEA;EACE,qBAAqB;EACrB,0BAA0B;EAC1B,eAAe;AACjB;;AAEA;EACE,WAAW;EACX,6CAA6C;EAC7C,gBAAgB;EAChB,uBAAuB;EACvB,yBAAyB;EACzB,sBAAsB;EACtB,eAAe;EACf,iBAAiB;EACjB,aAAa;AACf;;AAEA;EACE,gCAAgC;AAClC;;AAEA;EACE,WAAW;EACX,gBAAgB;EAChB,sBAAsB;EACtB,eAAe;EACf,iBAAiB;EACjB,aAAa;AACf;;AAEA;;EAEE,YAAY;EACZ,eAAe;AACjB;;AAEA;;EAEE,sBAAsB;AACxB;;AAEA;EACE,cAAc;AAChB;;AAEA;EACE,cAAc;AAChB;;AAEA;;EAEE,cAAc;AAChB;;AAEA;EACE,eAAe;EACf,aAAa;EACb,iBAAiB;EACjB,kBAAkB;EAClB,YAAY;EACZ,UAAU;AACZ;;AAEA;;;EAGE,iBAAiB;AACnB;;AAEA;EACE,eAAe;AACjB;AACA;EACE,WAAW;EACX,6BAA6B;AAC/B;;AAEA;;;;EAIE,oBAAoB;AACtB","sourcesContent":["/* Choices.js overrides */\n.ipysigma-widget .choices {\n  margin-bottom: 5px;\n}\n\n.ipysigma-widget .choices__inner {\n  border-radius: 0;\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  box-sizing: border-box;\n  padding-right: 50px;\n}\n\n.ipysigma-widget .choices__item--selectable {\n  padding-right: 0px !important;\n}\n\n.ipysigma-widget .choices__item {\n  text-overflow: ellipsis;\n  overflow: hidden;\n  white-space: nowrap;\n}\n\n/* Ipysigma own styles */\n.ipysigma-widget {\n  /* Background color is now set by widget directly! */\n  /* background-color: white; */\n  margin: 0;\n  padding: 0;\n  border: 1px solid #e0e0e0;\n  font-family: sans-serif;\n  color: black;\n}\n\n.ipysigma-widget ~ .ipysigma-widget {\n  border-left: none;\n}\n\n.widget-hbox ~ .widget-hbox .ipysigma-widget {\n  border-top: none;\n}\n\n.ipysigma-widget hr {\n  height: 1px;\n  border: none;\n  background-color: #e0e0e0;\n  margin-top: 6px;\n  margin-bottom: 6px;\n}\n\n.ipysigma-widget .ipysigma-left-panel {\n  position: absolute;\n  top: 10px;\n  left: 10px;\n}\n\n.ipysigma-widget .ipysigma-right-panel {\n  position: absolute;\n  top: 10px;\n  right: 10px;\n  width: 250px;\n  height: 100%;\n}\n\n.ipysigma-widget .ipysigma-right-panel.hidden {\n  pointer-events: none;\n}\n\n.ipysigma-widget .ipysigma-graph-description {\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  padding: 5px 10px;\n  font-size: 12px;\n  /* font-style: italic; */\n  line-height: 16px;\n}\n\n.ipysigma-widget .ipysigma-button {\n  cursor: pointer;\n  text-align: center;\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  user-select: none;\n}\n\n.ipysigma-widget .ipysigma-button.disabled {\n  border: none;\n  cursor: default;\n}\n\n.ipysigma-widget .ipysigma-button.disabled svg {\n  fill: #efefef;\n}\n\n.ipysigma-widget .ipysigma-button:hover {\n  border-color: grey;\n}\n\n.ipysigma-widget .ipysigma-svg-icon {\n  width: 32px;\n  height: 32px;\n  font-size: 24px;\n  line-height: 30px;\n  box-sizing: border-box;\n}\n\n.ipysigma-widget .ipysigma-zoom-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-unzoom-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-reset-zoom-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-fullscreen-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-layout-controls {\n  width: 100%;\n  margin-top: 10px;\n  display: flex;\n}\n\n.ipysigma-widget .ipysigma-reset-layout-button,\n.ipysigma-widget .ipysigma-noverlap-button {\n  margin-left: 4px;\n}\n\n.ipysigma-widget .ipysigma-spinner {\n  font-size: 20px;\n  padding-left: 5px;\n  line-height: 26px;\n}\n\n.ipysigma-widget .ipysigma-tab-button.selectable {\n  color: cornflowerblue;\n  text-decoration: underline;\n  cursor: pointer;\n}\n\n.ipysigma-widget .ipysigma-information-display {\n  width: 100%;\n  height: calc(100% - 45px - 5px - 20px - 25px);\n  overflow-y: auto;\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  box-sizing: border-box;\n  font-size: 12px;\n  line-height: 16px;\n  padding: 10px;\n}\n\n.ipysigma-widget .ipysigma-information-display.full {\n  height: calc(100% - 20px - 25px);\n}\n\n.ipysigma-widget .ipysigma-information-shadow-display {\n  width: 100%;\n  overflow-y: auto;\n  box-sizing: border-box;\n  font-size: 12px;\n  line-height: 16px;\n  padding: 10px;\n}\n\n.ipysigma-widget .ipysigma-information-hide-button,\n.ipysigma-widget .ipysigma-information-show-button {\n  float: right;\n  cursor: pointer;\n}\n\n.ipysigma-widget .ipysigma-information-contents,\n.ipysigma-widget .ipysigma-legend {\n  font-family: monospace;\n}\n\n.ipysigma-widget .ipysigma-string {\n  color: #bc2828;\n}\n\n.ipysigma-widget .ipysigma-number {\n  color: #008800;\n}\n\n.ipysigma-widget .ipysigma-boolean,\n.ipysigma-widget .ipysigma-keyword {\n  color: #0457ab;\n}\n\n.ipysigma-widget .ipysigma-download-controls {\n  margin-top: 5px;\n  display: flex;\n  text-align: right;\n  position: absolute;\n  bottom: 20px;\n  right: 0px;\n}\n\n.ipysigma-widget .ipysigma-download-png-button,\n.ipysigma-widget .ipysigma-download-svg-button,\n.ipysigma-widget .ipysigma-download-gexf-button {\n  margin-right: 3px;\n}\n\n.ipysigma-widget .category {\n  cursor: pointer;\n}\n.ipysigma-widget .category.evicted .category-value {\n  color: gray;\n  text-decoration: line-through;\n}\n\n.ipysigma-widget .ipysigma-search,\n.ipysigma-widget .ipysigma-download-controls,\n.ipysigma-widget .ipysigma-information-shadow-display,\n.ipysigma-widget .choices {\n  pointer-events: auto;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjMDAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==":
/*!**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjMDAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg== ***!
  \**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjMDAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==";

/***/ }),

/***/ "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjRkZGIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==":
/*!**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjRkZGIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg== ***!
  \**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjRkZGIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==";

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = /*#__PURE__*/JSON.parse('{"name":"ipysigma","version":"0.24.6","description":"A Jupyter widget using sigma.js to render interactive networks.","keywords":["sigma","graph","jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/medialab/ipysigma","bugs":{"url":"https://github.com/medialab/ipysigma/issues"},"license":"MIT","author":{"name":"Yomguithereal","email":"guillaume.plique@sciencespo.fr"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/medialab/ipysigma"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","build:gh-pages":"./scripts/build-gh-pages.sh","build:pdf":"cd presentations && bs pdf","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipysigma/labextension","clean:nbextension":"rimraf ipysigma/nbextension/static/index.js","decks":"cd presentations && bs serve","deploy":"npm run build:gh-pages && gh-pages -d ./presentations/gh-pages","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","@yomguithereal/sigma-experiments-renderers":"0.2.2","choices.js":"^10.1.0","chroma-js":"^2.4.2","comma-number":"^2.1.0","d3-scale":"^4.0.2","d3-scale-chromatic":"^3.0.0","debounce":"^1.2.1","file-saver":"^2.0.5","graphology":"^0.25.1","graphology-communities-louvain":"^2.0.0","graphology-gexf":"^0.10.1","graphology-layout":"^0.6.0","graphology-layout-forceatlas2":"0.10.1","graphology-layout-noverlap":"^0.4.2","graphology-svg":"^0.1.3","iwanthue":"^2.0.0","mnemonist":"^0.39.1","pandemonium":"^2.4.1","screenfull":"^6.0.1","seedrandom":"^3.0.5","sigma":"3.0.0-alpha2"},"devDependencies":{"@babel/core":"^7.23.7","@babel/preset-env":"^7.23.8","@jupyter-widgets/base-manager":"^1.0.7","@jupyterlab/builder":"^4.0.11","@lumino/application":"^2.3.0","@lumino/widgets":"^2.3.1","@types/chroma-js":"^2.1.3","@types/comma-number":"^2.1.0","@types/d3-scale":"^4.0.2","@types/d3-scale-chromatic":"^3.0.0","@types/debounce":"^1.2.1","@types/file-saver":"^2.0.5","@types/jest":"^26.0.0","@types/seedrandom":"^3.0.2","@types/webpack-env":"^1.18.4","@typescript-eslint/eslint-plugin":"^6.19.1","@typescript-eslint/parser":"^6.19.1","acorn":"^8.11.3","backslide":"^3.1.0","css-loader":"^6.9.1","csstype":"^3.0.10","eslint":"^8.56.0","eslint-config-prettier":"^9.1.0","eslint-plugin-prettier":"^5.1.3","fs-extra":"^11.2.0","gh-pages":"^4.0.0","graphology-types":"0.24.5","identity-obj-proxy":"^3.0.0","jest":"^29.7.0","mkdirp":"^3.0.1","npm-run-all":"^4.1.5","prettier":"^3.2.4","rimraf":"^5.0.5","source-map-loader":"^5.0.0","style-loader":"^3.3.4","ts-jest":"^29.1.2","ts-loader":"^9.5.1","typescript":"~5.3.3","webpack":"^5.90.0","webpack-cli":"^5.1.4"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipysigma/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js-data_image_svg_xml_base64_PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgM-6426be.5b65d24a08c8c56860a5.js.map