var gs = Object.defineProperty, ir = (r, t) => {
  let e = {};
  for (var i in r) gs(e, i, {
    get: r[i],
    enumerable: !0
  });
  return t || gs(e, Symbol.toStringTag, { value: "Module" }), e;
};
function Ne(r) {
  return Ne = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Ne(r);
}
function zn(r) {
  var t = (function(e, i) {
    if (Ne(e) != "object" || !e) return e;
    var s = e[Symbol.toPrimitive];
    if (s !== void 0) {
      var o = s.call(e, i || "default");
      if (Ne(o) != "object") return o;
      throw TypeError("@@toPrimitive must return a primitive value.");
    }
    return (i === "string" ? String : Number)(e);
  })(r, "string");
  return Ne(t) == "symbol" ? t : t + "";
}
function f(r, t, e) {
  return (t = zn(t)) in r ? Object.defineProperty(r, t, {
    value: e,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : r[t] = e, r;
}
var fs = class {
  constructor() {
    f(this, "browserShadowBlurConstant", 1), f(this, "DPI", 96), f(this, "devicePixelRatio", typeof window < "u" ? window.devicePixelRatio : 1), f(this, "perfLimitSizeTotal", 2097152), f(this, "maxCacheSideLimit", 4096), f(this, "minCacheSideLimit", 256), f(this, "disableStyleCopyPaste", !1), f(this, "enableGLFiltering", !0), f(this, "textureSize", 4096), f(this, "forceGLPutImageData", !1), f(this, "cachesBoundsOfCurve", !1), f(this, "fontPaths", {}), f(this, "NUM_FRACTION_DIGITS", 4);
  }
}, P = new class extends fs {
  constructor(r) {
    super(), this.configure(r);
  }
  configure(r = {}) {
    Object.assign(this, r);
  }
  addFonts(r = {}) {
    this.fontPaths = {
      ...this.fontPaths,
      ...r
    };
  }
  removeFonts(r = []) {
    r.forEach((t) => {
      delete this.fontPaths[t];
    });
  }
  clearFonts() {
    this.fontPaths = {};
  }
  restoreDefaults(r) {
    let t = new fs(), e = r?.reduce((i, s) => (i[s] = t[s], i), {}) || t;
    this.configure(e);
  }
}(), Xt = (r, ...t) => console[r]("fabric", ...t), _t = class extends Error {
  constructor(r, t) {
    super(`fabric: ${r}`, t);
  }
}, Gn = class extends _t {
  constructor(r) {
    super(`${r} 'options.signal' is in 'aborted' state`);
  }
}, Un = class {
}, Nn = class extends Un {
  testPrecision(r, t) {
    let e = `precision ${t} float;
void main(){}`, i = r.createShader(r.FRAGMENT_SHADER);
    return !!i && (r.shaderSource(i, e), r.compileShader(i), !!r.getShaderParameter(i, r.COMPILE_STATUS));
  }
  queryWebGL(r) {
    let t = r.getContext("webgl");
    t && (this.maxTextureSize = t.getParameter(t.MAX_TEXTURE_SIZE), this.GLPrecision = [
      "highp",
      "mediump",
      "lowp"
    ].find((e) => this.testPrecision(t, e)), t.getExtension("WEBGL_lose_context").loseContext(), Xt("log", `WebGL: max texture size ${this.maxTextureSize}`));
  }
  isSupported(r) {
    return !!this.maxTextureSize && this.maxTextureSize >= r;
  }
}, qn = {}, ps, Ct = () => ps || (ps = {
  document,
  window,
  isTouchSupported: "ontouchstart" in window || "ontouchstart" in document || window && window.navigator && window.navigator.maxTouchPoints > 0,
  WebGLProbe: new Nn(),
  dispose() {
  },
  copyPasteData: qn
}), _e = () => Ct().document, fe = () => Ct().window, Us = () => {
  var r;
  return Math.max((r = P.devicePixelRatio) == null ? fe().devicePixelRatio : r, 1);
}, qe = new class {
  constructor() {
    f(this, "boundsOfCurveCache", {}), this.charWidthsCache = /* @__PURE__ */ new Map();
  }
  getFontCache({ fontFamily: r, fontStyle: t, fontWeight: e }) {
    r = r.toLowerCase();
    let i = this.charWidthsCache;
    i.has(r) || i.set(r, /* @__PURE__ */ new Map());
    let s = i.get(r), o = `${t.toLowerCase()}_${(e + "").toLowerCase()}`;
    return s.has(o) || s.set(o, /* @__PURE__ */ new Map()), s.get(o);
  }
  clearFontCache(r) {
    r ? this.charWidthsCache.delete((r || "").toLowerCase()) : this.charWidthsCache = /* @__PURE__ */ new Map();
  }
  limitDimsByArea(r) {
    let { perfLimitSizeTotal: t } = P, e = Math.sqrt(t * r);
    return [Math.floor(e), Math.floor(t / e)];
  }
}(), li = "7.4.0";
function Cr() {
}
var Yt = Math.PI / 2, Kn = Math.PI / 4, pt = 2 * Math.PI, Ii = Math.PI / 180, Z = Object.freeze([
  1,
  0,
  0,
  1,
  0,
  0
]), L = "center", V = "left", Ns = "bottom", gt = "right", Lr = "none", Bi = /\r?\n/, qs = "moving", Rr = "scaling", Ks = "rotating", Js = "rotate", Qs = "skewing", Ze = "resizing", Zs = "modifyPoly", Mr = "changed", to = "scale", Wt = "scaleX", Vt = "scaleY", Se = "skewX", Ce = "skewY", tt = "fill", Mt = "stroke", eo = "modified", ms = "normal", oe = "json", w = new class {
  constructor() {
    this[oe] = /* @__PURE__ */ new Map(), this.svg = /* @__PURE__ */ new Map();
  }
  has(r) {
    return this[oe].has(r);
  }
  getClass(r) {
    let t = this[oe].get(r);
    if (!t) throw new _t(`No class registered for ${r}`);
    return t;
  }
  setClass(r, t) {
    t ? this[oe].set(t, r) : (this[oe].set(r.type, r), this[oe].set(r.type.toLowerCase(), r));
  }
  getSVGClass(r) {
    return this.svg.get(r);
  }
  setSVGClass(r, t) {
    this.svg.set(t ?? r.type.toLowerCase(), r);
  }
}(), Dr = new class extends Array {
  remove(r) {
    let t = this.indexOf(r);
    t > -1 && this.splice(t, 1);
  }
  cancelAll() {
    let r = this.splice(0);
    return r.forEach((t) => t.abort()), r;
  }
  cancelByCanvas(r) {
    if (!r) return [];
    let t = this.filter((e) => {
      var i;
      return e.target === r || typeof e.target == "object" && ((i = e.target) == null ? void 0 : i.canvas) === r;
    });
    return t.forEach((e) => e.abort()), t;
  }
  cancelByTarget(r) {
    if (!r) return [];
    let t = this.filter((e) => e.target === r);
    return t.forEach((e) => e.abort()), t;
  }
}(), Jn = class {
  constructor() {
    f(this, "__eventListeners", {});
  }
  on(r, t) {
    if (this.__eventListeners || (this.__eventListeners = {}), typeof r == "object") return Object.entries(r).forEach(([e, i]) => {
      this.on(e, i);
    }), () => this.off(r);
    if (t) {
      let e = r;
      return this.__eventListeners[e] || (this.__eventListeners[e] = []), this.__eventListeners[e].push(t), () => this.off(e, t);
    }
    return () => !1;
  }
  once(r, t) {
    if (typeof r == "object") {
      let e = [];
      return Object.entries(r).forEach(([i, s]) => {
        e.push(this.once(i, s));
      }), () => e.forEach((i) => i());
    }
    if (t) {
      let e = this.on(r, function(...i) {
        t.call(this, ...i), e();
      });
      return e;
    }
    return () => !1;
  }
  _removeEventListener(r, t) {
    if (this.__eventListeners[r]) if (t) {
      let e = this.__eventListeners[r], i = e.indexOf(t);
      i > -1 && e.splice(i, 1);
    } else this.__eventListeners[r] = [];
  }
  off(r, t) {
    if (this.__eventListeners) if (r === void 0) for (let e in this.__eventListeners) this._removeEventListener(e);
    else typeof r == "object" ? Object.entries(r).forEach(([e, i]) => {
      this._removeEventListener(e, i);
    }) : this._removeEventListener(r, t);
  }
  fire(r, t) {
    var e;
    if (!this.__eventListeners) return;
    let i = (e = this.__eventListeners[r]) == null ? void 0 : e.concat();
    if (i) for (let s = 0; s < i.length; s++) i[s].call(this, t || {});
  }
}, Gt = (r, t) => {
  let e = r.indexOf(t);
  return e !== -1 && r.splice(e, 1), r;
}, mt = (r) => {
  if (r === 0) return 1;
  switch (Math.abs(r) / Yt) {
    case 1:
    case 3:
      return 0;
    case 2:
      return -1;
  }
  return Math.cos(r);
}, vt = (r) => {
  if (r === 0) return 0;
  let t = r / Yt, e = Math.sign(r);
  switch (t) {
    case 1:
      return e;
    case 2:
      return 0;
    case 3:
      return -e;
  }
  return Math.sin(r);
}, v = class K {
  constructor(t = 0, e = 0) {
    typeof t == "object" ? (this.x = t.x, this.y = t.y) : (this.x = t, this.y = e);
  }
  add(t) {
    return new K(this.x + t.x, this.y + t.y);
  }
  addEquals(t) {
    return this.x += t.x, this.y += t.y, this;
  }
  scalarAdd(t) {
    return new K(this.x + t, this.y + t);
  }
  scalarAddEquals(t) {
    return this.x += t, this.y += t, this;
  }
  subtract(t) {
    return new K(this.x - t.x, this.y - t.y);
  }
  subtractEquals(t) {
    return this.x -= t.x, this.y -= t.y, this;
  }
  scalarSubtract(t) {
    return new K(this.x - t, this.y - t);
  }
  scalarSubtractEquals(t) {
    return this.x -= t, this.y -= t, this;
  }
  multiply(t) {
    return new K(this.x * t.x, this.y * t.y);
  }
  scalarMultiply(t) {
    return new K(this.x * t, this.y * t);
  }
  scalarMultiplyEquals(t) {
    return this.x *= t, this.y *= t, this;
  }
  divide(t) {
    return new K(this.x / t.x, this.y / t.y);
  }
  scalarDivide(t) {
    return new K(this.x / t, this.y / t);
  }
  scalarDivideEquals(t) {
    return this.x /= t, this.y /= t, this;
  }
  eq(t) {
    return this.x === t.x && this.y === t.y;
  }
  lt(t) {
    return this.x < t.x && this.y < t.y;
  }
  lte(t) {
    return this.x <= t.x && this.y <= t.y;
  }
  gt(t) {
    return this.x > t.x && this.y > t.y;
  }
  gte(t) {
    return this.x >= t.x && this.y >= t.y;
  }
  lerp(t, e = 0.5) {
    return e = Math.max(Math.min(1, e), 0), new K(this.x + (t.x - this.x) * e, this.y + (t.y - this.y) * e);
  }
  distanceFrom(t) {
    let e = this.x - t.x, i = this.y - t.y;
    return Math.sqrt(e * e + i * i);
  }
  midPointFrom(t) {
    return this.lerp(t);
  }
  min(t) {
    return new K(Math.min(this.x, t.x), Math.min(this.y, t.y));
  }
  max(t) {
    return new K(Math.max(this.x, t.x), Math.max(this.y, t.y));
  }
  toString() {
    return `${this.x},${this.y}`;
  }
  setXY(t, e) {
    return this.x = t, this.y = e, this;
  }
  setX(t) {
    return this.x = t, this;
  }
  setY(t) {
    return this.y = t, this;
  }
  setFromPoint(t) {
    return this.x = t.x, this.y = t.y, this;
  }
  swap(t) {
    let e = this.x, i = this.y;
    this.x = t.x, this.y = t.y, t.x = e, t.y = i;
  }
  clone() {
    return new K(this.x, this.y);
  }
  rotate(t, e = Xi) {
    let i = vt(t), s = mt(t), o = this.subtract(e);
    return new K(o.x * s - o.y * i, o.x * i + o.y * s).add(e);
  }
  transform(t, e = !1) {
    return new K(t[0] * this.x + t[2] * this.y + (e ? 0 : t[4]), t[1] * this.x + t[3] * this.y + (e ? 0 : t[5]));
  }
}, Xi = new v(0, 0), br = (r) => !!r && Array.isArray(r._objects);
function ro(r) {
  class t extends r {
    constructor(...i) {
      super(...i), f(this, "_objects", []);
    }
    _onObjectAdded(i) {
    }
    _onObjectRemoved(i) {
    }
    _onStackOrderChanged(i) {
    }
    add(...i) {
      let s = this._objects.push(...i);
      return i.forEach((o) => this._onObjectAdded(o)), s;
    }
    insertAt(i, ...s) {
      return this._objects.splice(i, 0, ...s), s.forEach((o) => this._onObjectAdded(o)), this._objects.length;
    }
    remove(...i) {
      let s = this._objects, o = [];
      return i.forEach((n) => {
        let a = s.indexOf(n);
        a !== -1 && (s.splice(a, 1), o.push(n), this._onObjectRemoved(n));
      }), o;
    }
    forEachObject(i) {
      this.getObjects().forEach((s, o, n) => i(s, o, n));
    }
    getObjects(...i) {
      return i.length === 0 ? [...this._objects] : this._objects.filter((s) => s.isType(...i));
    }
    item(i) {
      return this._objects[i];
    }
    isEmpty() {
      return this._objects.length === 0;
    }
    size() {
      return this._objects.length;
    }
    contains(i, s) {
      return !!this._objects.includes(i) || !!s && this._objects.some((o) => o instanceof t && o.contains(i, !0));
    }
    complexity() {
      return this._objects.reduce((i, s) => i += s.complexity ? s.complexity() : 0, 0);
    }
    sendObjectToBack(i) {
      return !(!i || i === this._objects[0]) && (Gt(this._objects, i), this._objects.unshift(i), this._onStackOrderChanged(i), !0);
    }
    bringObjectToFront(i) {
      return !(!i || i === this._objects[this._objects.length - 1]) && (Gt(this._objects, i), this._objects.push(i), this._onStackOrderChanged(i), !0);
    }
    sendObjectBackwards(i, s) {
      if (!i) return !1;
      let o = this._objects.indexOf(i);
      if (o !== 0) {
        let n = this.findNewLowerIndex(i, o, s);
        return Gt(this._objects, i), this._objects.splice(n, 0, i), this._onStackOrderChanged(i), !0;
      }
      return !1;
    }
    bringObjectForward(i, s) {
      if (!i) return !1;
      let o = this._objects.indexOf(i);
      if (o !== this._objects.length - 1) {
        let n = this.findNewUpperIndex(i, o, s);
        return Gt(this._objects, i), this._objects.splice(n, 0, i), this._onStackOrderChanged(i), !0;
      }
      return !1;
    }
    moveObjectTo(i, s) {
      return i !== this._objects[s] && (Gt(this._objects, i), this._objects.splice(s, 0, i), this._onStackOrderChanged(i), !0);
    }
    findNewLowerIndex(i, s, o) {
      let n;
      if (o) {
        n = s;
        for (let a = s - 1; a >= 0; --a) if (i.isOverlapping(this._objects[a])) {
          n = a;
          break;
        }
      } else n = s - 1;
      return n;
    }
    findNewUpperIndex(i, s, o) {
      let n;
      if (o) {
        n = s;
        for (let a = s + 1; a < this._objects.length; ++a) if (i.isOverlapping(this._objects[a])) {
          n = a;
          break;
        }
      } else n = s + 1;
      return n;
    }
    collectObjects({ left: i, top: s, width: o, height: n }, { includeIntersecting: a = !0 } = {}) {
      let l = [], h = new v(i, s), c = h.add(new v(o, n));
      for (let u = this._objects.length - 1; u >= 0; u--) {
        let d = this._objects[u];
        d.selectable && d.visible && (a && d.intersectsWithRect(h, c) || d.isContainedWithinRect(h, c) || a && d.containsPoint(h) || a && d.containsPoint(c)) && l.push(d);
      }
      return l;
    }
  }
  return t;
}
var io = class extends Jn {
  _setOptions(r = {}) {
    for (let t in r) this.set(t, r[t]);
  }
  _setObject(r) {
    for (let t in r) this._set(t, r[t]);
  }
  set(r, t) {
    return typeof r == "object" ? this._setObject(r) : this._set(r, t), this;
  }
  _set(r, t) {
    this[r] = t;
  }
  toggle(r) {
    let t = this.get(r);
    return typeof t == "boolean" && this.set(r, !t), this;
  }
  get(r) {
    return this[r];
  }
};
function Ke(r) {
  return fe().requestAnimationFrame(r);
}
function so(r) {
  return fe().cancelAnimationFrame(r);
}
var Qn = 0, $t = () => Qn++, bt = () => {
  let r = _e().createElement("canvas");
  if (!r || r.getContext === void 0) throw new _t("Failed to create `canvas` element");
  return r;
}, oo = () => _e().createElement("img"), Zn = (r) => {
  var t;
  let e = nt(r);
  return (t = e.getContext("2d")) == null || t.drawImage(r, 0, 0), e;
}, nt = (r) => {
  let t = bt();
  return t.width = r.width, t.height = r.height, t;
}, $i = (r, t, e) => r.toDataURL(`image/${t}`, e), Yi = (r, t, e) => new Promise((i, s) => {
  r.toBlob(i, `image/${t}`, e);
}), B = (r) => r * Ii, Dt = (r) => r / Ii, no = (r) => r.every((t, e) => t === Z[e]), U = (r, t, e) => new v(r).transform(t, e), ot = (r) => {
  let t = 1 / (r[0] * r[3] - r[1] * r[2]), e = [
    t * r[3],
    -t * r[1],
    -t * r[2],
    t * r[0],
    0,
    0
  ], { x: i, y: s } = new v(r[4], r[5]).transform(e, !0);
  return e[4] = -i, e[5] = -s, e;
}, $ = (r, t, e) => [
  r[0] * t[0] + r[2] * t[1],
  r[1] * t[0] + r[3] * t[1],
  r[0] * t[2] + r[2] * t[3],
  r[1] * t[2] + r[3] * t[3],
  e ? 0 : r[0] * t[4] + r[2] * t[5] + r[4],
  e ? 0 : r[1] * t[4] + r[3] * t[5] + r[5]
], Ir = (r, t) => r.reduceRight((e, i) => i && e ? $(i, e, t) : i || e, void 0) || Z.concat(), Wi = ([r, t]) => Math.atan2(t, r), Vi = ([r, t]) => Math.sqrt(r * r + t * t), ao = ([, , r, t]) => Math.sqrt(r * r + t * t), pe = (r) => {
  let t = Wi(r), e = r[0] ** 2 + r[1] ** 2, i = Math.sqrt(e), s = (r[0] * r[3] - r[2] * r[1]) / i, o = Math.atan2(r[0] * r[2] + r[1] * r[3], e);
  return {
    angle: Dt(t),
    scaleX: i,
    scaleY: s,
    skewX: Dt(o),
    skewY: 0,
    translateX: r[4] || 0,
    translateY: r[5] || 0
  };
}, be = (r, t = 0) => [
  1,
  0,
  0,
  1,
  r,
  t
];
function ee({ angle: r = 0 } = {}, { x: t = 0, y: e = 0 } = {}) {
  let i = B(r), s = mt(i), o = vt(i);
  return [
    s,
    o,
    -o,
    s,
    t ? t - (s * t - o * e) : 0,
    e ? e - (o * t + s * e) : 0
  ];
}
var Br = (r, t = r) => [
  r,
  0,
  0,
  t,
  0,
  0
], lo = (r) => Math.tan(B(r)), Hi = (r) => [
  1,
  0,
  lo(r),
  1,
  0,
  0
], zi = (r) => [
  1,
  lo(r),
  0,
  1,
  0,
  0
], sr = ({ scaleX: r = 1, scaleY: t = 1, flipX: e = !1, flipY: i = !1, skewX: s = 0, skewY: o = 0 }) => {
  let n = Br(e ? -r : r, i ? -t : t);
  return s && (n = $(n, Hi(s), !0)), o && (n = $(n, zi(o), !0)), n;
}, ho = (r) => {
  let { translateX: t = 0, translateY: e = 0, angle: i = 0 } = r, s = be(t, e);
  i && (s = $(s, ee({ angle: i })));
  let o = sr(r);
  return no(o) || (s = $(s, o)), s;
}, Je = (r, { signal: t, crossOrigin: e = null } = {}) => new Promise(function(i, s) {
  if (t && t.aborted) return s(new Gn("loadImage"));
  let o = oo(), n;
  t && (n = function(l) {
    o.src = "", s(l);
  }, t.addEventListener("abort", n, { once: !0 }));
  let a = function() {
    o.onload = o.onerror = null, n && t?.removeEventListener("abort", n), i(o);
  };
  r ? (o.onload = a, o.onerror = function() {
    n && t?.removeEventListener("abort", n), s(new _t(`Error loading ${o.src}`));
  }, e && (o.crossOrigin = e), o.src = r) : a();
}), me = (r, { signal: t, reviver: e = Cr } = {}) => new Promise((i, s) => {
  let o = [];
  t && t.addEventListener("abort", s, { once: !0 }), Promise.allSettled(r.map((n) => w.getClass(n.type).fromObject(n, { signal: t }))).then(async (n) => {
    for (let [a, l] of n.entries()) if (l.status === "fulfilled" && (await e(r[a], l.value), o.push(l.value)), l.status === "rejected") {
      let h = await e(r[a], void 0, l.reason);
      h && o.push(h);
    }
    i(o);
  }).catch((n) => {
    o.forEach((a) => {
      a.dispose && a.dispose();
    }), s(n);
  }).finally(() => {
    t && t.removeEventListener("abort", s);
  });
}), or = (r, { signal: t } = {}) => new Promise((e, i) => {
  let s = [];
  t && t.addEventListener("abort", i, { once: !0 });
  let o = Object.values(r).map((a) => a && a.type && w.has(a.type) ? me([a], { signal: t }).then(([l]) => (s.push(l), l)) : a), n = Object.keys(r);
  Promise.all(o).then((a) => a.reduce((l, h, c) => (l[n[c]] = h, l), {})).then(e).catch((a) => {
    s.forEach((l) => {
      l.dispose && l.dispose();
    }), i(a);
  }).finally(() => {
    t && t.removeEventListener("abort", i);
  });
}), re = (r, t = []) => t.reduce((e, i) => (i in r && (e[i] = r[i]), e), {}), Gi = (r, t) => Object.keys(r).reduce((e, i) => (t(r[i], i, r) && (e[i] = r[i]), e), {}), F = (r, t) => parseFloat(Number(r).toFixed(t)), ve = (r) => "matrix(" + r.map((t) => F(t, P.NUM_FRACTION_DIGITS)).join(" ") + ")", ht = (r) => !!r && r.toLive !== void 0, vs = (r) => !!r && typeof r.toObject == "function", ys = (r) => !!r && r.offsetX !== void 0 && "source" in r, Ut = (r) => !!r && "multiSelectionStacking" in r;
function co(r) {
  let t = r && ut(r), e = 0, i = 0;
  if (!r || !t) return {
    left: e,
    top: i
  };
  let s = r, o = t.documentElement, n = t.body || {
    scrollLeft: 0,
    scrollTop: 0
  };
  for (; s && (s.parentNode || s.host) && (s = s.parentNode || s.host, s === t ? (e = n.scrollLeft || o.scrollLeft || 0, i = n.scrollTop || o.scrollTop || 0) : (e += s.scrollLeft || 0, i += s.scrollTop || 0), s.nodeType !== 1 || s.style.position !== "fixed"); ) ;
  return {
    left: e,
    top: i
  };
}
var ut = (r) => r.ownerDocument || null, uo = (r) => {
  var t;
  return ((t = r.ownerDocument) == null ? void 0 : t.defaultView) || null;
}, go = (r, t, { width: e, height: i }, s = 1) => {
  r.width = e, r.height = i, s > 1 && (r.setAttribute("width", (e * s).toString()), r.setAttribute("height", (i * s).toString()), t.scale(s, s));
}, hi = (r, { width: t, height: e }) => {
  t && (r.style.width = typeof t == "number" ? `${t}px` : t), e && (r.style.height = typeof e == "number" ? `${e}px` : e);
};
function xs(r) {
  return r.onselectstart !== void 0 && (r.onselectstart = () => !1), r.style.userSelect = Lr, r;
}
var fo = class {
  constructor(r) {
    f(this, "_originalCanvasStyle", void 0), f(this, "lower", void 0);
    let t = this.createLowerCanvas(r);
    this.lower = {
      el: t,
      ctx: t.getContext("2d")
    };
  }
  createLowerCanvas(r) {
    let t = (e = r) && e.getContext !== void 0 ? r : r && _e().getElementById(r) || bt();
    var e;
    if (t.hasAttribute("data-fabric")) throw new _t("Trying to initialize a canvas that has already been initialized. Did you forget to dispose the canvas?");
    return this._originalCanvasStyle = t.style.cssText, t.setAttribute("data-fabric", "main"), t.classList.add("lower-canvas"), t;
  }
  cleanupDOM({ width: r, height: t }) {
    let { el: e } = this.lower;
    e.classList.remove("lower-canvas"), e.removeAttribute("data-fabric"), e.setAttribute("width", `${r}`), e.setAttribute("height", `${t}`), e.style.cssText = this._originalCanvasStyle || "", this._originalCanvasStyle = void 0;
  }
  setDimensions(r, t) {
    let { el: e, ctx: i } = this.lower;
    go(e, i, r, t);
  }
  setCSSDimensions(r) {
    hi(this.lower.el, r);
  }
  calcOffset() {
    return (function(r) {
      var t;
      let e = r && ut(r), i = {
        left: 0,
        top: 0
      };
      if (!e) return i;
      let s = ((t = uo(r)) == null ? void 0 : t.getComputedStyle(r, null)) || {};
      i.left += parseInt(s.borderLeftWidth, 10) || 0, i.top += parseInt(s.borderTopWidth, 10) || 0, i.left += parseInt(s.paddingLeft, 10) || 0, i.top += parseInt(s.paddingTop, 10) || 0;
      let o = {
        left: 0,
        top: 0
      }, n = e.documentElement;
      r.getBoundingClientRect !== void 0 && (o = r.getBoundingClientRect());
      let a = co(r);
      return {
        left: o.left + a.left - (n.clientLeft || 0) + i.left,
        top: o.top + a.top - (n.clientTop || 0) + i.top
      };
    })(this.lower.el);
  }
  dispose() {
    Ct().dispose(this.lower.el), delete this.lower;
  }
}, ta = {
  backgroundVpt: !0,
  backgroundColor: "",
  overlayVpt: !0,
  overlayColor: "",
  includeDefaultValues: !0,
  svgViewportTransformation: !0,
  renderOnAddRemove: !0,
  skipOffscreen: !0,
  enableRetinaScaling: !0,
  imageSmoothingEnabled: !0,
  controlsAboveOverlay: !1,
  allowTouchScrolling: !1,
  viewportTransform: [...Z],
  patternQuality: "best"
}, ea = ir({
  capitalize: () => ra,
  escapeXml: () => M,
  graphemeSplit: () => Xr
}), ra = (r, t = !1) => `${r.charAt(0).toUpperCase()}${t ? r.slice(1) : r.slice(1).toLowerCase()}`, M = (r) => r.toString().replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&apos;").replace(/</g, "&lt;").replace(/>/g, "&gt;"), Me, Xr = (r) => {
  if (Me || Me || (Me = "Intl" in fe() && "Segmenter" in Intl && new Intl.Segmenter(void 0, { granularity: "grapheme" })), Me) {
    let t = Me.segment(r);
    return Array.from(t).map(({ segment: e }) => e);
  }
  return ia(r);
}, ia = (r) => {
  let t = [];
  for (let e, i = 0; i < r.length; i++) (e = sa(r, i)) !== !1 && t.push(e);
  return t;
}, sa = (r, t) => {
  let e = r.charCodeAt(t);
  if (isNaN(e)) return "";
  if (e < 55296 || e > 57343) return r.charAt(t);
  if (55296 <= e && e <= 56319) {
    if (r.length <= t + 1) throw "High surrogate without following low surrogate";
    let s = r.charCodeAt(t + 1);
    if (56320 > s || s > 57343) throw "High surrogate without following low surrogate";
    return r.charAt(t) + r.charAt(t + 1);
  }
  if (t === 0) throw "Low surrogate without preceding high surrogate";
  let i = r.charCodeAt(t - 1);
  if (55296 > i || i > 56319) throw "Low surrogate without preceding high surrogate";
  return !1;
}, $r = class po extends ro(io) {
  get lowerCanvasEl() {
    var t;
    return (t = this.elements.lower) == null ? void 0 : t.el;
  }
  get contextContainer() {
    var t;
    return (t = this.elements.lower) == null ? void 0 : t.ctx;
  }
  static getDefaults() {
    return po.ownDefaults;
  }
  constructor(t, e = {}) {
    super(), Object.assign(this, this.constructor.getDefaults()), this.set(e), this.initElements(t), this._setDimensionsImpl({
      width: this.width || this.elements.lower.el.width || 0,
      height: this.height || this.elements.lower.el.height || 0
    }), this.skipControlsDrawing = !1, this.viewportTransform = [...this.viewportTransform], this.calcViewportBoundaries();
  }
  initElements(t) {
    this.elements = new fo(t);
  }
  add(...t) {
    let e = super.add(...t);
    return t.length > 0 && this.renderOnAddRemove && this.requestRenderAll(), e;
  }
  insertAt(t, ...e) {
    let i = super.insertAt(t, ...e);
    return e.length > 0 && this.renderOnAddRemove && this.requestRenderAll(), i;
  }
  remove(...t) {
    let e = super.remove(...t);
    return e.length > 0 && this.renderOnAddRemove && this.requestRenderAll(), e;
  }
  _onObjectAdded(t) {
    t.canvas && t.canvas !== this && (Xt("warn", `Canvas is trying to add an object that belongs to a different canvas.
Resulting to default behavior: removing object from previous canvas and adding to new canvas`), t.canvas.remove(t)), t._set("canvas", this), t.setCoords(), this.fire("object:added", { target: t }), t.fire("added", { target: this });
  }
  _onObjectRemoved(t) {
    t._set("canvas", void 0), this.fire("object:removed", { target: t }), t.fire("removed", { target: this });
  }
  _onStackOrderChanged() {
    this.renderOnAddRemove && this.requestRenderAll();
  }
  getRetinaScaling() {
    return this.enableRetinaScaling ? Us() : 1;
  }
  calcOffset() {
    return this._offset = this.elements.calcOffset();
  }
  getWidth() {
    return this.width;
  }
  getHeight() {
    return this.height;
  }
  _setDimensionsImpl(t, { cssOnly: e = !1, backstoreOnly: i = !1 } = {}) {
    if (!e) {
      let s = {
        width: this.width,
        height: this.height,
        ...t
      };
      this.elements.setDimensions(s, this.getRetinaScaling()), this.hasLostContext = !0, this.width = s.width, this.height = s.height;
    }
    i || this.elements.setCSSDimensions(t), this.calcOffset();
  }
  setDimensions(t, e) {
    this._setDimensionsImpl(t, e), e && e.cssOnly || this.requestRenderAll();
  }
  getZoom() {
    return Vi(this.viewportTransform);
  }
  setViewportTransform(t) {
    this.viewportTransform = t, this.calcViewportBoundaries(), this.renderOnAddRemove && this.requestRenderAll();
  }
  zoomToPoint(t, e) {
    let i = t, s = [...this.viewportTransform], o = U(t, ot(s));
    s[0] = e, s[3] = e;
    let n = U(o, s);
    s[4] += i.x - n.x, s[5] += i.y - n.y, this.setViewportTransform(s);
  }
  setZoom(t) {
    this.zoomToPoint(new v(0, 0), t);
  }
  absolutePan(t) {
    let e = [...this.viewportTransform];
    return e[4] = -t.x, e[5] = -t.y, this.setViewportTransform(e);
  }
  relativePan(t) {
    return this.absolutePan(new v(-t.x - this.viewportTransform[4], -t.y - this.viewportTransform[5]));
  }
  getElement() {
    return this.elements.lower.el;
  }
  clearContext(t) {
    t.clearRect(0, 0, this.width, this.height);
  }
  getContext() {
    return this.elements.lower.ctx;
  }
  clear() {
    this.remove(...this.getObjects()), this.backgroundImage = void 0, this.overlayImage = void 0, this.backgroundColor = "", this.overlayColor = "", this.clearContext(this.getContext()), this.fire("canvas:cleared"), this.renderOnAddRemove && this.requestRenderAll();
  }
  renderAll() {
    this.cancelRequestedRender(), this.destroyed || this.renderCanvas(this.getContext(), this._objects);
  }
  renderAndReset() {
    this.nextRenderHandle = 0, this.renderAll();
  }
  requestRenderAll() {
    this.nextRenderHandle || this.disposed || this.destroyed || (this.nextRenderHandle = Ke(() => this.renderAndReset()));
  }
  calcViewportBoundaries() {
    let t = this.width, e = this.height, i = ot(this.viewportTransform), s = U({
      x: 0,
      y: 0
    }, i), o = U({
      x: t,
      y: e
    }, i), n = s.min(o), a = s.max(o);
    return this.vptCoords = {
      tl: n,
      tr: new v(a.x, n.y),
      bl: new v(n.x, a.y),
      br: a
    };
  }
  cancelRequestedRender() {
    this.nextRenderHandle && (so(this.nextRenderHandle), this.nextRenderHandle = 0);
  }
  drawControls(t) {
  }
  renderCanvas(t, e) {
    if (this.destroyed) return;
    let i = this.viewportTransform, s = this.clipPath;
    this.calcViewportBoundaries(), this.clearContext(t), t.imageSmoothingEnabled = this.imageSmoothingEnabled, t.patternQuality = this.patternQuality, this.fire("before:render", { ctx: t }), this._renderBackground(t), t.save(), t.transform(i[0], i[1], i[2], i[3], i[4], i[5]), this._renderObjects(t, e), t.restore(), this.controlsAboveOverlay || this.skipControlsDrawing || this.drawControls(t), s && (s._set("canvas", this), s.shouldCache(), s._transformDone = !0, s.renderCache({ forClipping: !0 }), this.drawClipPathOnCanvas(t, s)), this._renderOverlay(t), this.controlsAboveOverlay && !this.skipControlsDrawing && this.drawControls(t), this.fire("after:render", { ctx: t }), this.__cleanupTask && (this.__cleanupTask(), this.__cleanupTask = void 0);
  }
  drawClipPathOnCanvas(t, e) {
    let i = this.viewportTransform;
    t.save(), t.transform(...i), t.globalCompositeOperation = "destination-in", e.transform(t), t.scale(1 / e.zoomX, 1 / e.zoomY), t.drawImage(e._cacheCanvas, -e.cacheTranslationX, -e.cacheTranslationY), t.restore();
  }
  _renderObjects(t, e) {
    for (let i = 0, s = e.length; i < s; ++i) e[i] && e[i].render(t);
  }
  _renderBackgroundOrOverlay(t, e) {
    let i = this[`${e}Color`], s = this[`${e}Image`], o = this.viewportTransform, n = this[`${e}Vpt`];
    if (!i && !s) return;
    let a = ht(i);
    if (i) {
      if (t.save(), t.beginPath(), t.moveTo(0, 0), t.lineTo(this.width, 0), t.lineTo(this.width, this.height), t.lineTo(0, this.height), t.closePath(), t.fillStyle = a ? i.toLive(t) : i, n && t.transform(...o), a) {
        t.transform(1, 0, 0, 1, i.offsetX || 0, i.offsetY || 0);
        let l = i.gradientTransform || i.patternTransform;
        l && t.transform(...l);
      }
      t.fill(), t.restore();
    }
    if (s) {
      t.save();
      let { skipOffscreen: l } = this;
      this.skipOffscreen = n, n && t.transform(...o), s.render(t), this.skipOffscreen = l, t.restore();
    }
  }
  _renderBackground(t) {
    this._renderBackgroundOrOverlay(t, "background");
  }
  _renderOverlay(t) {
    this._renderBackgroundOrOverlay(t, "overlay");
  }
  getCenterPoint() {
    return new v(this.width / 2, this.height / 2);
  }
  centerObjectH(t) {
    return this._centerObject(t, new v(this.getCenterPoint().x, t.getCenterPoint().y));
  }
  centerObjectV(t) {
    return this._centerObject(t, new v(t.getCenterPoint().x, this.getCenterPoint().y));
  }
  centerObject(t) {
    return this._centerObject(t, this.getCenterPoint());
  }
  viewportCenterObject(t) {
    return this._centerObject(t, this.getVpCenter());
  }
  viewportCenterObjectH(t) {
    return this._centerObject(t, new v(this.getVpCenter().x, t.getCenterPoint().y));
  }
  viewportCenterObjectV(t) {
    return this._centerObject(t, new v(t.getCenterPoint().x, this.getVpCenter().y));
  }
  getVpCenter() {
    return U(this.getCenterPoint(), ot(this.viewportTransform));
  }
  _centerObject(t, e) {
    t.setXY(e, L, L), t.setCoords(), this.renderOnAddRemove && this.requestRenderAll();
  }
  toDatalessJSON(t) {
    return this.toDatalessObject(t);
  }
  toObject(t) {
    return this._toObjectMethod("toObject", t);
  }
  toJSON() {
    return this.toObject();
  }
  toDatalessObject(t) {
    return this._toObjectMethod("toDatalessObject", t);
  }
  _toObjectMethod(t, e) {
    let i = this.clipPath, s = i && !i.excludeFromExport ? this._toObject(i, t, e) : null;
    return {
      version: li,
      ...re(this, e),
      objects: this._objects.filter((o) => !o.excludeFromExport).map((o) => this._toObject(o, t, e)),
      ...this.__serializeBgOverlay(t, e),
      ...s ? { clipPath: s } : null
    };
  }
  _toObject(t, e, i) {
    let s;
    this.includeDefaultValues || (s = t.includeDefaultValues, t.includeDefaultValues = !1);
    let o = t[e](i);
    return this.includeDefaultValues || (t.includeDefaultValues = !!s), o;
  }
  __serializeBgOverlay(t, e) {
    let i = {}, s = this.backgroundImage, o = this.overlayImage, n = this.backgroundColor, a = this.overlayColor;
    return ht(n) ? n.excludeFromExport || (i.background = n.toObject(e)) : n && (i.background = n), ht(a) ? a.excludeFromExport || (i.overlay = a.toObject(e)) : a && (i.overlay = a), s && !s.excludeFromExport && (i.backgroundImage = this._toObject(s, t, e)), o && !o.excludeFromExport && (i.overlayImage = this._toObject(o, t, e)), i;
  }
  toSVG(t = {}, e) {
    t.reviver = e;
    let i = [];
    var s;
    return this._setSVGPreamble(i, t), this._setSVGHeader(i, t), this.clipPath && i.push(`<g clip-path="url(#${M((s = this.clipPath.clipPathId) == null ? "" : s)})" >
`), this._setSVGBgOverlayColor(i, "background"), this._setSVGBgOverlayImage(i, "backgroundImage", e), this._setSVGObjects(i, e), this.clipPath && i.push(`</g>
`), this._setSVGBgOverlayColor(i, "overlay"), this._setSVGBgOverlayImage(i, "overlayImage", e), i.push("</svg>"), i.join("");
  }
  _setSVGPreamble(t, e) {
    e.suppressPreamble || t.push('<?xml version="1.0" encoding="', e.encoding || "UTF-8", `" standalone="no" ?>
`, '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" ', `"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
`);
  }
  _setSVGHeader(t, e) {
    let i = e.width || `${this.width}`, s = e.height || `${this.height}`, o = P.NUM_FRACTION_DIGITS, n = e.viewBox, a;
    if (n) a = `viewBox="${n.x} ${n.y} ${n.width} ${n.height}" `;
    else if (this.svgViewportTransformation) {
      let l = this.viewportTransform;
      a = `viewBox="${F(-l[4] / l[0], o)} ${F(-l[5] / l[3], o)} ${F(this.width / l[0], o)} ${F(this.height / l[3], o)}" `;
    } else a = `viewBox="0 0 ${this.width} ${this.height}" `;
    t.push("<svg ", 'xmlns="http://www.w3.org/2000/svg" ', 'xmlns:xlink="http://www.w3.org/1999/xlink" ', 'version="1.1" ', 'width="', i, '" ', 'height="', s, '" ', a, `xml:space="preserve">
`, "<desc>Created with Fabric.js ", li, `</desc>
`, `<defs>
`, this.createSVGFontFacesMarkup(), this.createSVGRefElementsMarkup(), this.createSVGClipPathMarkup(e), `</defs>
`);
  }
  createSVGClipPathMarkup(t) {
    let e = this.clipPath;
    return e ? (e.clipPathId = `CLIPPATH_${$t()}`, `<clipPath id="${e.clipPathId}" >
${e.toClipPathSVG(t.reviver)}</clipPath>
`) : "";
  }
  createSVGRefElementsMarkup() {
    return ["background", "overlay"].map((t) => {
      let e = this[`${t}Color`];
      if (ht(e)) {
        let i = this[`${t}Vpt`], s = this.viewportTransform, o = {
          isType: () => !1,
          width: this.width / (i ? s[0] : 1),
          height: this.height / (i ? s[3] : 1)
        };
        return e.toSVG(o, { additionalTransform: i ? ve(s) : "" });
      }
    }).join("");
  }
  createSVGFontFacesMarkup() {
    let t = [], e = {}, i = P.fontPaths;
    this._objects.forEach(function o(n) {
      t.push(n), br(n) && n._objects.forEach(o);
    }), t.forEach((o) => {
      if (!(n = o) || typeof n._renderText != "function") return;
      var n;
      let { styles: a, fontFamily: l } = o;
      !e[l] && i[l] && (e[l] = !0, a && Object.values(a).forEach((h) => {
        Object.values(h).forEach(({ fontFamily: c = "" }) => {
          !e[c] && i[c] && (e[c] = !0);
        });
      }));
    });
    let s = Object.keys(e).map((o) => `		@font-face {
			font-family: '${o}';
			src: url('${i[o]}');
		}
`).join("");
    return s ? `	<style type="text/css"><![CDATA[
${s}]]></style>
` : "";
  }
  _setSVGObjects(t, e) {
    this.forEachObject((i) => {
      i.excludeFromExport || this._setSVGObject(t, i, e);
    });
  }
  _setSVGObject(t, e, i) {
    t.push(e.toSVG(i));
  }
  _setSVGBgOverlayImage(t, e, i) {
    let s = this[e];
    s && !s.excludeFromExport && s.toSVG && t.push(s.toSVG(i));
  }
  _setSVGBgOverlayColor(t, e) {
    let i = this[`${e}Color`];
    if (i) if (ht(i)) {
      let s = i.repeat || "", o = this.width, n = this.height, a = this[`${e}Vpt`] ? ve(ot(this.viewportTransform)) : "";
      t.push(`<rect transform="${a} translate(${o / 2},${n / 2})" x="${i.offsetX - o / 2}" y="${i.offsetY - n / 2}" width="${s !== "repeat-y" && s !== "no-repeat" || !ys(i) ? o : i.source.width}" height="${s !== "repeat-x" && s !== "no-repeat" || !ys(i) ? n : i.source.height}" fill="url(#SVGID_${i.id})"></rect>
`);
    } else t.push('<rect x="0" y="0" width="100%" height="100%" ', 'fill="', i, '"', `></rect>
`);
  }
  loadFromJSON(t, e, { signal: i } = {}) {
    if (!t) return Promise.reject(new _t("`json` is undefined"));
    let { objects: s = [], ...o } = typeof t == "string" ? JSON.parse(t) : t, { backgroundImage: n, background: a, overlayImage: l, overlay: h, clipPath: c } = o, u = this.renderOnAddRemove;
    return this.renderOnAddRemove = !1, Promise.all([me(s, {
      reviver: e,
      signal: i
    }), or({
      backgroundImage: n,
      backgroundColor: a,
      overlayImage: l,
      overlayColor: h,
      clipPath: c
    }, { signal: i })]).then(([d, g]) => (this.clear(), this.add(...d), this.set(o), this.set(g), this.renderOnAddRemove = u, this));
  }
  clone(t) {
    let e = this.toObject(t);
    return this.cloneWithoutData().loadFromJSON(e);
  }
  cloneWithoutData() {
    let t = nt(this);
    return new this.constructor(t);
  }
  toDataURL(t = {}) {
    let { format: e = "png", quality: i = 1, multiplier: s = 1, enableRetinaScaling: o = !1 } = t, n = s * (o ? this.getRetinaScaling() : 1);
    return $i(this.toCanvasElement(n, t), e, i);
  }
  toBlob(t = {}) {
    let { format: e = "png", quality: i = 1, multiplier: s = 1, enableRetinaScaling: o = !1 } = t, n = s * (o ? this.getRetinaScaling() : 1);
    return Yi(this.toCanvasElement(n, t), e, i);
  }
  toCanvasElement(t = 1, { width: e, height: i, left: s, top: o, filter: n } = {}) {
    let a = (e || this.width) * t, l = (i || this.height) * t, h = this.getZoom(), c = this.width, u = this.height, d = this.skipControlsDrawing, g = h * t, p = this.viewportTransform, m = [
      g,
      0,
      0,
      g,
      (p[4] - (s || 0)) * t,
      (p[5] - (o || 0)) * t
    ], y = this.enableRetinaScaling, x = nt({
      width: a,
      height: l
    }), _ = n ? this._objects.filter((S) => n(S)) : this._objects;
    return this.enableRetinaScaling = !1, this.viewportTransform = m, this.width = a, this.height = l, this.skipControlsDrawing = !0, this.calcViewportBoundaries(), this.renderCanvas(x.getContext("2d"), _), this.viewportTransform = p, this.width = c, this.height = u, this.calcViewportBoundaries(), this.enableRetinaScaling = y, this.skipControlsDrawing = d, x;
  }
  dispose() {
    return !this.disposed && this.elements.cleanupDOM({
      width: this.width,
      height: this.height
    }), Dr.cancelByCanvas(this), this.disposed = !0, new Promise((t, e) => {
      let i = () => {
        this.destroy(), t(!0);
      };
      i.kill = e, this.__cleanupTask && this.__cleanupTask.kill("aborted"), this.destroyed ? t(!1) : this.nextRenderHandle ? this.__cleanupTask = i : i();
    });
  }
  destroy() {
    this.destroyed = !0, this.cancelRequestedRender(), this.forEachObject((t) => t.dispose()), this._objects = [], this.backgroundImage && this.backgroundImage.dispose(), this.backgroundImage = void 0, this.overlayImage && this.overlayImage.dispose(), this.overlayImage = void 0, this.elements.dispose();
  }
  toString() {
    return `#<Canvas (${this.complexity()}): { objects: ${this._objects.length} }>`;
  }
};
f($r, "ownDefaults", ta);
var oa = [
  "touchstart",
  "touchmove",
  "touchend"
], mo = (r) => {
  let t = co(r.target), e = (function(i) {
    let s = i.changedTouches;
    return s && s[0] ? s[0] : i;
  })(r);
  return new v(e.clientX + t.left, e.clientY + t.top);
}, Er = (r) => oa.includes(r.type) || r.pointerType === "touch", _s = (r) => {
  r.preventDefault(), r.stopPropagation();
}, St = (r) => {
  let t = 0, e = 0, i = 0, s = 0;
  for (let o = 0, n = r.length; o < n; o++) {
    let { x: a, y: l } = r[o];
    (a > i || !o) && (i = a), (a < t || !o) && (t = a), (l > s || !o) && (s = l), (l < e || !o) && (e = l);
  }
  return {
    left: t,
    top: e,
    width: i - t,
    height: s - e
  };
}, na = (r, t) => {
  ye(r, $(ot(t), r.calcOwnMatrix()));
}, vo = (r, t) => ye(r, $(t, r.calcOwnMatrix())), ye = (r, t) => {
  let { translateX: e, translateY: i, scaleX: s, scaleY: o, ...n } = pe(t), a = new v(e, i);
  r.flipX = !1, r.flipY = !1, Object.assign(r, n), r.set({
    scaleX: s,
    scaleY: o
  }), r.setPositionByOrigin(a, L, L);
}, yo = (r) => {
  r.scaleX = 1, r.scaleY = 1, r.skewX = 0, r.skewY = 0, r.flipX = !1, r.flipY = !1, r.rotate(0);
}, Ui = (r) => ({
  scaleX: r.scaleX,
  scaleY: r.scaleY,
  skewX: r.skewX,
  skewY: r.skewY,
  angle: r.angle,
  left: r.left,
  flipX: r.flipX,
  flipY: r.flipY,
  top: r.top
}), Yr = (r, t, e) => {
  let i = r / 2, s = t / 2, o = St([
    new v(-i, -s),
    new v(i, -s),
    new v(-i, s),
    new v(i, s)
  ].map((n) => n.transform(e)));
  return new v(o.width, o.height);
}, nr = (r = Z, t = Z) => $(ot(t), r), Et = (r, t = Z, e = Z) => r.transform(nr(t, e)), xo = (r, t = Z, e = Z) => r.transform(nr(t, e), !0), Ni = (r, t, e) => {
  let i = nr(t, e);
  return ye(r, $(i, r.calcOwnMatrix())), i;
}, aa = {
  left: -0.5,
  top: -0.5,
  center: 0,
  bottom: 0.5,
  right: 0.5
}, J = (r) => typeof r == "string" ? aa[r] : r - 0.5, la = new v(1, 0), _o = new v(), qi = (r, t) => r.rotate(t), tr = (r, t) => new v(t).subtract(r), Pr = (r) => r.distanceFrom(_o), jr = (r, t) => Math.atan2(ue(r, t), So(r, t)), Ki = (r) => jr(la, r), Wr = (r) => r.eq(_o) ? r : r.scalarDivide(Pr(r)), Ji = (r, t = !0) => Wr(new v(-r.y, r.x).scalarMultiply(t ? 1 : -1)), ue = (r, t) => r.x * t.y - r.y * t.x, So = (r, t) => r.x * t.x + r.y * t.y, ci = (r, t, e) => {
  if (r.eq(t) || r.eq(e)) return !0;
  let i = ue(t, e), s = ue(t, r), o = ue(e, r);
  return i >= 0 ? s >= 0 && o <= 0 : !(s <= 0 && o >= 0);
}, Qi = "not-allowed";
function Co(r) {
  return J(r.originX) === J("center") && J(r.originY) === J("center");
}
function Ss(r) {
  return 0.5 - J(r);
}
var ft = (r, t) => r[t], Zi = (r, t, e, i) => ({
  e: r,
  transform: t,
  pointer: new v(e, i)
});
function bo(r, t, e) {
  let i = e, s = Ki(tr(Et(r.getCenterPoint(), r.canvas.viewportTransform, void 0), i)) + pt;
  return Math.round(s % pt / Kn);
}
function Vr({ target: r, corner: t }, e, i, s, o) {
  var n;
  let a = r.controls[t], l = ((n = r.canvas) == null ? void 0 : n.getZoom()) || 1, h = r.padding / l, c = (function(u, d, g, p) {
    let m = u.getRelativeCenterPoint(), y = g !== void 0 && p !== void 0 ? u.translateToGivenOrigin(m, L, L, g, p) : new v(u.left, u.top);
    return (u.angle ? d.rotate(-B(u.angle), m) : d).subtract(y);
  })(r, new v(s, o), e, i);
  return c.x >= h && (c.x -= h), c.x <= -h && (c.x += h), c.y >= h && (c.y -= h), c.y <= h && (c.y += h), c.x -= a.offsetX, c.y -= a.offsetY, c;
}
var ha = new RegExp(String.raw`[\0-\x1F\x7F;<>\\]|\/\*|\*\/|url\s*\(|expression\s*\(|(?:java|vb)script\s*:|data\s*:|@import\b`, "iu"), Hr = (r) => typeof r == "string" && r.trim().length > 0 && !ha.test(r), qt = (r, t = "") => {
  let e = Number(r);
  return Number.isFinite(e) ? `${e}` : t;
}, Kt = (r, t = "") => typeof r == "string" && Hr(r) ? r : t, Ar = (r) => r.replace(/\s+/g, " "), Cs = {
  aliceblue: "#F0F8FF",
  antiquewhite: "#FAEBD7",
  aqua: "#0FF",
  aquamarine: "#7FFFD4",
  azure: "#F0FFFF",
  beige: "#F5F5DC",
  bisque: "#FFE4C4",
  black: "#000",
  blanchedalmond: "#FFEBCD",
  blue: "#00F",
  blueviolet: "#8A2BE2",
  brown: "#A52A2A",
  burlywood: "#DEB887",
  cadetblue: "#5F9EA0",
  chartreuse: "#7FFF00",
  chocolate: "#D2691E",
  coral: "#FF7F50",
  cornflowerblue: "#6495ED",
  cornsilk: "#FFF8DC",
  crimson: "#DC143C",
  cyan: "#0FF",
  darkblue: "#00008B",
  darkcyan: "#008B8B",
  darkgoldenrod: "#B8860B",
  darkgray: "#A9A9A9",
  darkgrey: "#A9A9A9",
  darkgreen: "#006400",
  darkkhaki: "#BDB76B",
  darkmagenta: "#8B008B",
  darkolivegreen: "#556B2F",
  darkorange: "#FF8C00",
  darkorchid: "#9932CC",
  darkred: "#8B0000",
  darksalmon: "#E9967A",
  darkseagreen: "#8FBC8F",
  darkslateblue: "#483D8B",
  darkslategray: "#2F4F4F",
  darkslategrey: "#2F4F4F",
  darkturquoise: "#00CED1",
  darkviolet: "#9400D3",
  deeppink: "#FF1493",
  deepskyblue: "#00BFFF",
  dimgray: "#696969",
  dimgrey: "#696969",
  dodgerblue: "#1E90FF",
  firebrick: "#B22222",
  floralwhite: "#FFFAF0",
  forestgreen: "#228B22",
  fuchsia: "#F0F",
  gainsboro: "#DCDCDC",
  ghostwhite: "#F8F8FF",
  gold: "#FFD700",
  goldenrod: "#DAA520",
  gray: "#808080",
  grey: "#808080",
  green: "#008000",
  greenyellow: "#ADFF2F",
  honeydew: "#F0FFF0",
  hotpink: "#FF69B4",
  indianred: "#CD5C5C",
  indigo: "#4B0082",
  ivory: "#FFFFF0",
  khaki: "#F0E68C",
  lavender: "#E6E6FA",
  lavenderblush: "#FFF0F5",
  lawngreen: "#7CFC00",
  lemonchiffon: "#FFFACD",
  lightblue: "#ADD8E6",
  lightcoral: "#F08080",
  lightcyan: "#E0FFFF",
  lightgoldenrodyellow: "#FAFAD2",
  lightgray: "#D3D3D3",
  lightgrey: "#D3D3D3",
  lightgreen: "#90EE90",
  lightpink: "#FFB6C1",
  lightsalmon: "#FFA07A",
  lightseagreen: "#20B2AA",
  lightskyblue: "#87CEFA",
  lightslategray: "#789",
  lightslategrey: "#789",
  lightsteelblue: "#B0C4DE",
  lightyellow: "#FFFFE0",
  lime: "#0F0",
  limegreen: "#32CD32",
  linen: "#FAF0E6",
  magenta: "#F0F",
  maroon: "#800000",
  mediumaquamarine: "#66CDAA",
  mediumblue: "#0000CD",
  mediumorchid: "#BA55D3",
  mediumpurple: "#9370DB",
  mediumseagreen: "#3CB371",
  mediumslateblue: "#7B68EE",
  mediumspringgreen: "#00FA9A",
  mediumturquoise: "#48D1CC",
  mediumvioletred: "#C71585",
  midnightblue: "#191970",
  mintcream: "#F5FFFA",
  mistyrose: "#FFE4E1",
  moccasin: "#FFE4B5",
  navajowhite: "#FFDEAD",
  navy: "#000080",
  oldlace: "#FDF5E6",
  olive: "#808000",
  olivedrab: "#6B8E23",
  orange: "#FFA500",
  orangered: "#FF4500",
  orchid: "#DA70D6",
  palegoldenrod: "#EEE8AA",
  palegreen: "#98FB98",
  paleturquoise: "#AFEEEE",
  palevioletred: "#DB7093",
  papayawhip: "#FFEFD5",
  peachpuff: "#FFDAB9",
  peru: "#CD853F",
  pink: "#FFC0CB",
  plum: "#DDA0DD",
  powderblue: "#B0E0E6",
  purple: "#800080",
  rebeccapurple: "#639",
  red: "#F00",
  rosybrown: "#BC8F8F",
  royalblue: "#4169E1",
  saddlebrown: "#8B4513",
  salmon: "#FA8072",
  sandybrown: "#F4A460",
  seagreen: "#2E8B57",
  seashell: "#FFF5EE",
  sienna: "#A0522D",
  silver: "#C0C0C0",
  skyblue: "#87CEEB",
  slateblue: "#6A5ACD",
  slategray: "#708090",
  slategrey: "#708090",
  snow: "#FFFAFA",
  springgreen: "#00FF7F",
  steelblue: "#4682B4",
  tan: "#D2B48C",
  teal: "#008080",
  thistle: "#D8BFD8",
  tomato: "#FF6347",
  turquoise: "#40E0D0",
  violet: "#EE82EE",
  wheat: "#F5DEB3",
  white: "#FFF",
  whitesmoke: "#F5F5F5",
  yellow: "#FF0",
  yellowgreen: "#9ACD32"
}, Qr = (r, t, e) => (e < 0 && (e += 1), e > 1 && --e, e < 1 / 6 ? r + 6 * (t - r) * e : e < 0.5 ? t : e < 2 / 3 ? r + (t - r) * (2 / 3 - e) * 6 : r), bs = (r, t, e, i) => {
  r /= 255, t /= 255, e /= 255;
  let s = Math.max(r, t, e), o = Math.min(r, t, e), n, a, l = (s + o) / 2;
  if (s === o) n = a = 0;
  else {
    let h = s - o;
    switch (a = l > 0.5 ? h / (2 - s - o) : h / (s + o), s) {
      case r:
        n = (t - e) / h + (t < e ? 6 : 0);
        break;
      case t:
        n = (e - r) / h + 2;
        break;
      case e:
        n = (r - t) / h + 4;
    }
    n /= 6;
  }
  return [
    Math.round(360 * n),
    Math.round(100 * a),
    Math.round(100 * l),
    i
  ];
}, ws = (r = "1") => parseFloat(r) / (r.endsWith("%") ? 100 : 1), lr = (r) => Math.min(Math.round(r), 255).toString(16).toUpperCase().padStart(2, "0"), Ts = ([r, t, e, i = 1]) => {
  let s = Math.round(0.3 * r + 0.59 * t + 0.11 * e);
  return [
    s,
    s,
    s,
    i
  ];
}, et = class G {
  constructor(t) {
    if (f(this, "isUnrecognised", !1), t) if (t instanceof G) this.setSource([...t._source]);
    else if (Array.isArray(t)) {
      let [e, i, s, o = 1] = t;
      this.setSource([
        e,
        i,
        s,
        o
      ]);
    } else this.setSource(this._tryParsingColor(t));
    else this.setSource([
      0,
      0,
      0,
      1
    ]);
  }
  _tryParsingColor(t) {
    return (t = t.toLowerCase()) in Cs && (t = Cs[t]), t === "transparent" ? [
      255,
      255,
      255,
      0
    ] : G.sourceFromHex(t) || G.sourceFromRgb(t) || G.sourceFromHsl(t) || (this.isUnrecognised = !0) && [
      0,
      0,
      0,
      1
    ];
  }
  getSource() {
    return this._source;
  }
  setSource(t) {
    this._source = t;
  }
  toRgb() {
    let [t, e, i] = this.getSource();
    return `rgb(${t},${e},${i})`;
  }
  toRgba() {
    return `rgba(${this.getSource().join(",")})`;
  }
  toHsl() {
    let [t, e, i] = bs(...this.getSource());
    return `hsl(${t},${e}%,${i}%)`;
  }
  toHsla() {
    let [t, e, i, s] = bs(...this.getSource());
    return `hsla(${t},${e}%,${i}%,${s})`;
  }
  toHex() {
    return this.toHexa().slice(0, 6);
  }
  toHexa() {
    let [t, e, i, s] = this.getSource();
    return `${lr(t)}${lr(e)}${lr(i)}${lr(Math.round(255 * s))}`;
  }
  getAlpha() {
    return this.getSource()[3];
  }
  setAlpha(t) {
    return this._source[3] = t, this;
  }
  toGrayscale() {
    return this.setSource(Ts(this.getSource())), this;
  }
  toBlackWhite(t) {
    let [e, , , i] = Ts(this.getSource()), s = e < (t || 127) ? 0 : 255;
    return this.setSource([
      s,
      s,
      s,
      i
    ]), this;
  }
  overlayWith(t) {
    t instanceof G || (t = new G(t));
    let e = this.getSource(), i = t.getSource(), [s, o, n] = e.map((a, l) => Math.round(0.5 * a + 0.5 * i[l]));
    return this.setSource([
      s,
      o,
      n,
      e[3]
    ]), this;
  }
  static fromRgb(t) {
    return G.fromRgba(t);
  }
  static fromRgba(t) {
    return new G(G.sourceFromRgb(t));
  }
  static sourceFromRgb(t) {
    let e = Ar(t).match(/^rgba?\(\s?(\d{0,3}(?:\.\d+)?%?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?(?:\s?[,/]\s?(\d{0,3}(?:\.\d+)?%?)\s?)?\)$/i);
    if (e) {
      let [i, s, o] = e.slice(1, 4).map((n) => {
        let a = parseFloat(n);
        return n.endsWith("%") ? Math.round(2.55 * a) : a;
      });
      return [
        i,
        s,
        o,
        ws(e[4])
      ];
    }
  }
  static fromHsl(t) {
    return G.fromHsla(t);
  }
  static fromHsla(t) {
    return new G(G.sourceFromHsl(t));
  }
  static sourceFromHsl(t) {
    let e = Ar(t).match(/^hsla?\(\s?([+-]?\d{0,3}(?:\.\d+)?(?:deg|turn|rad)?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?(?:\s?[,/]\s?(\d*(?:\.\d+)?%?)\s?)?\)$/i);
    if (!e) return;
    let i = (G.parseAngletoDegrees(e[1]) % 360 + 360) % 360 / 360, s = parseFloat(e[2]) / 100, o = parseFloat(e[3]) / 100, n, a, l;
    if (s === 0) n = a = l = o;
    else {
      let h = o <= 0.5 ? o * (s + 1) : o + s - o * s, c = 2 * o - h;
      n = Qr(c, h, i + 1 / 3), a = Qr(c, h, i), l = Qr(c, h, i - 1 / 3);
    }
    return [
      Math.round(255 * n),
      Math.round(255 * a),
      Math.round(255 * l),
      ws(e[4])
    ];
  }
  static fromHex(t) {
    return new G(G.sourceFromHex(t));
  }
  static sourceFromHex(t) {
    if (t.match(/^#?(([0-9a-f]){3,4}|([0-9a-f]{2}){3,4})$/i)) {
      let e = t.slice(t.indexOf("#") + 1), i;
      i = e.length <= 4 ? e.split("").map((l) => l + l) : e.match(/.{2}/g);
      let [s, o, n, a = 255] = i.map((l) => parseInt(l, 16));
      return [
        s,
        o,
        n,
        a / 255
      ];
    }
  }
  static parseAngletoDegrees(t) {
    let e = t.toLowerCase(), i = parseFloat(e);
    return e.includes("rad") ? Dt(i) : e.includes("turn") ? 360 * i : i;
  }
}, ca = (r) => {
  let t = [
    "instantiated_by_use",
    "style",
    "id",
    "class"
  ];
  switch (r) {
    case "linearGradient":
      return t.concat([
        "x1",
        "y1",
        "x2",
        "y2",
        "gradientUnits",
        "gradientTransform"
      ]);
    case "radialGradient":
      return t.concat([
        "gradientUnits",
        "gradientTransform",
        "cx",
        "cy",
        "r",
        "fx",
        "fy",
        "fr"
      ]);
    case "stop":
      return t.concat([
        "offset",
        "stop-color",
        "stop-opacity"
      ]);
  }
  return t;
}, Zt = (r, t = 16) => {
  let e = /\D{0,2}$/.exec(r), i = parseFloat(r), s = P.DPI;
  switch (e?.[0]) {
    case "mm":
      return i * s / 25.4;
    case "cm":
      return i * s / 2.54;
    case "in":
      return i * s;
    case "pt":
      return i * s / 72;
    case "pc":
      return i * s / 72 * 12;
    case "em":
      return i * t;
    default:
      return i;
  }
}, wo = (r) => {
  let [t, e] = r.trim().split(" "), [i, s] = (o = t) && o !== "none" ? [o.slice(1, 4), o.slice(5, 8)] : o === "none" ? [o, o] : ["Mid", "Mid"];
  var o;
  return {
    meetOrSlice: e || "meet",
    alignX: i,
    alignY: s
  };
}, er = (r, t, e = !0) => {
  let i, s;
  if (t) if (t.toLive) i = `url(#SVGID_${M(t.id)})`;
  else {
    let o = String(t);
    if (Hr(o)) {
      let n = new et(o), a = n.getAlpha();
      i = n.toRgb(), a !== 1 && (s = a.toString());
    } else i = new et("black").toRgb();
  }
  else i = "none";
  return e ? `${r}: ${i}; ${s ? `${r}-opacity: ${s}; ` : ""}` : `${r}="${i}" ${s ? `${r}-opacity="${s}" ` : ""}`;
}, To = class {
  getSvgStyles(r) {
    let t = this.fillRule == null ? "nonzero" : Kt(this.fillRule), e = this.strokeWidth == null ? "0" : qt(this.strokeWidth), i = this.strokeDashArray == null ? Lr : this.strokeDashArray.every((d) => Number.isFinite(Number(d))) ? this.strokeDashArray.join(" ") : "", s = this.strokeDashOffset == null ? "0" : qt(this.strokeDashOffset), o = this.strokeLineCap == null ? "butt" : Kt(this.strokeLineCap), n = this.strokeLineJoin == null ? "miter" : Kt(this.strokeLineJoin), a = this.strokeMiterLimit == null ? "4" : qt(this.strokeMiterLimit), l = this.opacity == null ? "1" : qt(this.opacity), h = this.visible ? "" : " visibility: hidden;", c = r ? "" : this.getSvgFilter(), u = er(tt, this.fill);
    return [
      er(Mt, this.stroke),
      e ? `stroke-width: ${e}; ` : "",
      i ? `stroke-dasharray: ${i}; ` : "",
      o ? `stroke-linecap: ${o}; ` : "",
      s ? `stroke-dashoffset: ${s}; ` : "",
      n ? `stroke-linejoin: ${n}; ` : "",
      a ? `stroke-miterlimit: ${a}; ` : "",
      u,
      t ? `fill-rule: ${t}; ` : "",
      l ? `opacity: ${l};` : "",
      c,
      h
    ].map((d) => M(d)).join("");
  }
  getSvgFilter() {
    return this.shadow ? `filter: url(#SVGID_${M(this.shadow.id)});` : "";
  }
  getSvgCommons() {
    return [this.id ? `id="${M(String(this.id))}" ` : "", this.clipPath ? `clip-path="url(#${M(this.clipPath.clipPathId)})" ` : ""].join("");
  }
  getSvgTransform(r, t = "") {
    return `transform="${ve(r ? this.calcTransformMatrix() : this.calcOwnMatrix())}${t}" `;
  }
  _toSVG(r) {
    return [""];
  }
  toSVG(r) {
    return this._createBaseSVGMarkup(this._toSVG(r), { reviver: r });
  }
  toClipPathSVG(r) {
    return "	" + this._createBaseClipPathSVGMarkup(this._toSVG(r), { reviver: r });
  }
  _createBaseClipPathSVGMarkup(r, { reviver: t, additionalTransform: e = "" } = {}) {
    let i = [this.getSvgTransform(!0, e), this.getSvgCommons()].join(""), s = r.indexOf("COMMON_PARTS");
    return r[s] = i, t ? t(r.join("")) : r.join("");
  }
  _createBaseSVGMarkup(r, { noStyle: t, reviver: e, withShadow: i, additionalTransform: s } = {}) {
    let o = t ? "" : `style="${this.getSvgStyles()}" `, n = i ? `style="${this.getSvgFilter()}" ` : "", a = this.clipPath, l = this.strokeUniform ? 'vector-effect="non-scaling-stroke" ' : "", h = a && a.absolutePositioned, c = this.stroke, u = this.fill, d = this.shadow, g = [], p = r.indexOf("COMMON_PARTS"), m;
    return a && (a.clipPathId = `CLIPPATH_${$t()}`, m = `<clipPath id="${a.clipPathId}" >
${a.toClipPathSVG(e)}</clipPath>
`), h && g.push("<g ", n, this.getSvgCommons(), ` >
`), g.push("<g ", this.getSvgTransform(!1), h ? "" : n + this.getSvgCommons(), ` >
`), r[p] = [
      o,
      l,
      t ? "" : this.addPaintOrder(),
      " ",
      s ? `transform="${s}" ` : ""
    ].join(""), ht(u) && g.push(u.toSVG(this)), ht(c) && g.push(c.toSVG(this)), d && g.push(d.toSVG(this)), a && g.push(m), g.push(r.join("")), g.push(`</g>
`), h && g.push(`</g>
`), e ? e(g.join("")) : g.join("");
  }
  addPaintOrder() {
    return this.paintFirst === "fill" ? "" : ` paint-order="${M(this.paintFirst)}" `;
  }
};
function zr(r) {
  return RegExp("^(" + r.join("|") + ")\\b", "i");
}
var xe = "textDecorationThickness", Gr = "textDecorationColor", Oo = [
  "fontSize",
  "fontWeight",
  "fontFamily",
  "fontStyle"
], ko = [
  "underline",
  "overline",
  "linethrough"
], Mo = [
  ...Oo,
  "lineHeight",
  "text",
  "charSpacing",
  "textAlign",
  "styles",
  "path",
  "pathStartOffset",
  "pathSide",
  "pathAlign"
], Do = [
  ...Mo,
  ...ko,
  "textBackgroundColor",
  "direction",
  xe,
  Gr
], ua = [
  ...Oo,
  ...ko,
  Mt,
  "strokeWidth",
  tt,
  "deltaY",
  "textBackgroundColor",
  xe,
  Gr
], da = {
  _reNewline: Bi,
  _reSpacesAndTabs: /[ \t\r]/g,
  _reSpaceAndTab: /[ \t\r]/,
  _reWords: /\S+/g,
  fontSize: 40,
  fontWeight: ms,
  fontFamily: "Times New Roman",
  underline: !1,
  overline: !1,
  linethrough: !1,
  textAlign: V,
  fontStyle: ms,
  lineHeight: 1.16,
  textBackgroundColor: "",
  stroke: null,
  shadow: null,
  path: void 0,
  pathStartOffset: 0,
  pathSide: V,
  pathAlign: "baseline",
  charSpacing: 0,
  deltaY: 0,
  direction: "ltr",
  CACHE_FONT_SIZE: 400,
  MIN_TEXT_WIDTH: 2,
  superscript: {
    size: 0.6,
    baseline: -0.35
  },
  subscript: {
    size: 0.6,
    baseline: 0.11
  },
  _fontSizeFraction: 0.222,
  offsets: {
    underline: 0.1,
    linethrough: -0.28167,
    overline: -0.81333
  },
  _fontSizeMult: 1.13,
  [xe]: 66.667
}, ts = "justify", dt = String.raw`[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?`, Zr = String.raw`(?:\s*,?\s+|\s*,\s*)`, ga = RegExp("(normal|italic)?\\s*(normal|small-caps)?\\s*(normal|bold|bolder|lighter|100|200|300|400|500|600|700|800|900)?\\s*(" + dt + "(?:px|cm|mm|em|pt|pc|in)*)(?:\\/(normal|" + dt + "))?\\s+(.*)"), fa = {
  cx: V,
  x: V,
  r: "radius",
  cy: "top",
  y: "top",
  display: "visible",
  visibility: "visible",
  transform: "transformMatrix",
  "fill-opacity": "fillOpacity",
  "fill-rule": "fillRule",
  "font-family": "fontFamily",
  "font-size": "fontSize",
  "font-style": "fontStyle",
  "font-weight": "fontWeight",
  "letter-spacing": "charSpacing",
  "paint-order": "paintFirst",
  "stroke-dasharray": "strokeDashArray",
  "stroke-dashoffset": "strokeDashOffset",
  "stroke-linecap": "strokeLineCap",
  "stroke-linejoin": "strokeLineJoin",
  "stroke-miterlimit": "strokeMiterLimit",
  "stroke-opacity": "strokeOpacity",
  "stroke-width": "strokeWidth",
  "text-decoration": "textDecoration",
  "text-anchor": "textAnchor",
  opacity: "opacity",
  "clip-path": "clipPath",
  "clip-rule": "clipRule",
  "vector-effect": "strokeUniform",
  "image-rendering": "imageSmoothing",
  "text-decoration-thickness": xe,
  "text-decoration-color": Gr
}, Os = "font-size", ks = "clip-path", Uh = zr([
  "path",
  "circle",
  "polygon",
  "polyline",
  "ellipse",
  "rect",
  "line",
  "image",
  "text"
]), Nh = zr([
  "symbol",
  "image",
  "marker",
  "pattern",
  "view",
  "svg"
]), Ms = zr([
  "symbol",
  "g",
  "a",
  "svg",
  "clipPath",
  "defs"
]), qh = new RegExp(String.raw`^\s*(${dt})${Zr}(${dt})${Zr}(${dt})${Zr}(${dt})\s*$`), Ds = "(-?\\d+(?:\\.\\d*)?(?:px)?(?:\\s?|$))?", Es = RegExp("(?:\\s|^)" + Ds + Ds + "(" + dt + "?(?:px)?)?(?:\\s?|$)(?:$|\\s)"), de = class wr {
  constructor(t = {}) {
    let e = typeof t == "string" ? wr.parseShadow(t) : t;
    Object.assign(this, wr.ownDefaults, e), this.id = $t();
  }
  static parseShadow(t) {
    let e = t.trim(), [, i = 0, s = 0, o = 0] = (Es.exec(e) || []).map((n) => parseFloat(n) || 0);
    return {
      color: (e.replace(Es, "") || "rgb(0,0,0)").trim(),
      offsetX: i,
      offsetY: s,
      blur: o
    };
  }
  toString() {
    return [
      this.offsetX,
      this.offsetY,
      this.blur,
      this.color
    ].join("px ");
  }
  toSVG(t) {
    let e = qi(new v(this.offsetX, this.offsetY), B(-t.angle)), i = P.NUM_FRACTION_DIGITS, s = new et(this.color), o = 40, n = 40;
    return t.width && t.height && (o = 100 * F((Math.abs(e.x) + this.blur) / t.width, i) + 20, n = 100 * F((Math.abs(e.y) + this.blur) / t.height, i) + 20), t.flipX && (e.x *= -1), t.flipY && (e.y *= -1), `<filter id="SVGID_${M(this.id)}" y="-${n}%" height="${100 + 2 * n}%" x="-${o}%" width="${100 + 2 * o}%" >
	<feGaussianBlur in="SourceAlpha" stdDeviation="${F(this.blur ? this.blur / 2 : 0, i)}"></feGaussianBlur>
	<feOffset dx="${F(e.x, i)}" dy="${F(e.y, i)}" result="oBlur" ></feOffset>
	<feFlood flood-color="${s.toRgb()}" flood-opacity="${s.getAlpha()}"/>
	<feComposite in2="oBlur" operator="in" />
	<feMerge>
		<feMergeNode></feMergeNode>
		<feMergeNode in="SourceGraphic"></feMergeNode>
	</feMerge>
</filter>
`;
  }
  toObject() {
    let t = {
      color: this.color,
      blur: this.blur,
      offsetX: this.offsetX,
      offsetY: this.offsetY,
      affectStroke: this.affectStroke,
      nonScaling: this.nonScaling,
      type: this.constructor.type
    }, e = wr.ownDefaults;
    return this.includeDefaultValues ? t : Gi(t, (i, s) => i !== e[s]);
  }
  static async fromObject(t) {
    return new this(t);
  }
};
f(de, "ownDefaults", {
  color: "rgb(0,0,0)",
  blur: 0,
  offsetX: 0,
  offsetY: 0,
  affectStroke: !1,
  includeDefaultValues: !0,
  nonScaling: !1
}), f(de, "type", "shadow"), w.setClass(de, "shadow");
var te = (r, t, e) => Math.max(r, Math.min(t, e)), pa = [
  "top",
  V,
  Wt,
  Vt,
  "flipX",
  "flipY",
  "originX",
  "originY",
  "angle",
  "opacity",
  "globalCompositeOperation",
  "shadow",
  "visible",
  Se,
  Ce
], Pt = [
  tt,
  Mt,
  "strokeWidth",
  "strokeDashArray",
  "width",
  "height",
  "paintFirst",
  "strokeUniform",
  "strokeLineCap",
  "strokeDashOffset",
  "strokeLineJoin",
  "strokeMiterLimit",
  "backgroundColor",
  "clipPath"
], ma = {
  top: 0,
  left: 0,
  width: 0,
  height: 0,
  angle: 0,
  flipX: !1,
  flipY: !1,
  scaleX: 1,
  scaleY: 1,
  minScaleLimit: 0,
  skewX: 0,
  skewY: 0,
  originX: L,
  originY: L,
  strokeWidth: 1,
  strokeUniform: !1,
  padding: 0,
  opacity: 1,
  paintFirst: tt,
  fill: "rgb(0,0,0)",
  fillRule: "nonzero",
  stroke: null,
  strokeDashArray: null,
  strokeDashOffset: 0,
  strokeLineCap: "butt",
  strokeLineJoin: "miter",
  strokeMiterLimit: 4,
  globalCompositeOperation: "source-over",
  backgroundColor: "",
  shadow: null,
  visible: !0,
  includeDefaultValues: !0,
  excludeFromExport: !1,
  objectCaching: !0,
  clipPath: void 0,
  inverted: !1,
  absolutePositioned: !1,
  centeredRotation: !0,
  centeredScaling: !1,
  dirty: !0
}, va = ir({
  defaultEasing: () => Po,
  easeInBack: () => Xa,
  easeInBounce: () => jo,
  easeInCirc: () => Aa,
  easeInCubic: () => ya,
  easeInElastic: () => Ra,
  easeInExpo: () => Ea,
  easeInOutBack: () => Ya,
  easeInOutBounce: () => Wa,
  easeInOutCirc: () => La,
  easeInOutCubic: () => _a,
  easeInOutElastic: () => Ba,
  easeInOutExpo: () => ja,
  easeInOutQuad: () => za,
  easeInOutQuart: () => ba,
  easeInOutQuint: () => Oa,
  easeInOutSine: () => Da,
  easeInQuad: () => Va,
  easeInQuart: () => Sa,
  easeInQuint: () => wa,
  easeInSine: () => ka,
  easeOutBack: () => $a,
  easeOutBounce: () => rs,
  easeOutCirc: () => Fa,
  easeOutCubic: () => xa,
  easeOutElastic: () => Ia,
  easeOutExpo: () => Pa,
  easeOutQuad: () => Ha,
  easeOutQuart: () => Ca,
  easeOutQuint: () => Ta,
  easeOutSine: () => Ma
}), es = (r, t, e, i) => (r < Math.abs(t) ? (r = t, i = e / 4) : i = t === 0 && r === 0 ? e / pt * Math.asin(1) : e / pt * Math.asin(t / r), {
  a: r,
  c: t,
  p: e,
  s: i
}), Eo = (r, t, e, i, s) => r * 2 ** (10 * --i) * Math.sin((i * s - t) * pt / e), Po = (r, t, e, i) => -e * Math.cos(r / i * Yt) + e + t, ya = (r, t, e, i) => e * (r / i) ** 3 + t, xa = (r, t, e, i) => e * ((r / i - 1) ** 3 + 1) + t, _a = (r, t, e, i) => (r /= i / 2) < 1 ? e / 2 * r ** 3 + t : e / 2 * ((r - 2) ** 3 + 2) + t, Sa = (r, t, e, i) => e * (r /= i) * r ** 3 + t, Ca = (r, t, e, i) => -e * ((r = r / i - 1) * r ** 3 - 1) + t, ba = (r, t, e, i) => (r /= i / 2) < 1 ? e / 2 * r ** 4 + t : -e / 2 * ((r -= 2) * r ** 3 - 2) + t, wa = (r, t, e, i) => e * (r / i) ** 5 + t, Ta = (r, t, e, i) => e * ((r / i - 1) ** 5 + 1) + t, Oa = (r, t, e, i) => (r /= i / 2) < 1 ? e / 2 * r ** 5 + t : e / 2 * ((r - 2) ** 5 + 2) + t, ka = (r, t, e, i) => -e * Math.cos(r / i * Yt) + e + t, Ma = (r, t, e, i) => e * Math.sin(r / i * Yt) + t, Da = (r, t, e, i) => -e / 2 * (Math.cos(Math.PI * r / i) - 1) + t, Ea = (r, t, e, i) => r === 0 ? t : e * 2 ** (10 * (r / i - 1)) + t, Pa = (r, t, e, i) => r === i ? t + e : e * -(2 ** (-10 * r / i) + 1) + t, ja = (r, t, e, i) => r === 0 ? t : r === i ? t + e : (r /= i / 2) < 1 ? e / 2 * 2 ** (10 * (r - 1)) + t : e / 2 * -(2 ** (-10 * (r - 1)) + 2) + t, Aa = (r, t, e, i) => -e * (Math.sqrt(1 - (r /= i) * r) - 1) + t, Fa = (r, t, e, i) => e * Math.sqrt(1 - (r = r / i - 1) * r) + t, La = (r, t, e, i) => (r /= i / 2) < 1 ? -e / 2 * (Math.sqrt(1 - r ** 2) - 1) + t : e / 2 * (Math.sqrt(1 - (r -= 2) * r) + 1) + t, Ra = (r, t, e, i) => {
  let s = e, o = 0;
  if (r === 0) return t;
  if ((r /= i) === 1) return t + e;
  o || (o = 0.3 * i);
  let { a: n, s: a, p: l } = es(s, e, o, 1.70158);
  return -Eo(n, a, l, r, i) + t;
}, Ia = (r, t, e, i) => {
  let s = e, o = 0;
  if (r === 0) return t;
  if ((r /= i) === 1) return t + e;
  o || (o = 0.3 * i);
  let { a: n, s: a, p: l, c: h } = es(s, e, o, 1.70158);
  return n * 2 ** (-10 * r) * Math.sin((r * i - a) * pt / l) + h + t;
}, Ba = (r, t, e, i) => {
  let s = e, o = 0;
  if (r === 0) return t;
  if ((r /= i / 2) == 2) return t + e;
  o || (o = 0.3 * 1.5 * i);
  let { a: n, s: a, p: l, c: h } = es(s, e, o, 1.70158);
  return r < 1 ? -0.5 * Eo(n, a, l, r, i) + t : n * 2 ** (-10 * --r) * Math.sin((r * i - a) * pt / l) * 0.5 + h + t;
}, Xa = (r, t, e, i, s = 1.70158) => e * (r /= i) * r * ((s + 1) * r - s) + t, $a = (r, t, e, i, s = 1.70158) => e * ((r = r / i - 1) * r * ((s + 1) * r + s) + 1) + t, Ya = (r, t, e, i, s = 1.70158) => (r /= i / 2) < 1 ? e / 2 * (r * r * ((1 + (s *= 1.525)) * r - s)) + t : e / 2 * ((r -= 2) * r * ((1 + (s *= 1.525)) * r + s) + 2) + t, rs = (r, t, e, i) => (r /= i) < 1 / 2.75 ? e * (7.5625 * r * r) + t : r < 2 / 2.75 ? e * (7.5625 * (r -= 1.5 / 2.75) * r + 0.75) + t : r < 2.5 / 2.75 ? e * (7.5625 * (r -= 2.25 / 2.75) * r + 0.9375) + t : e * (7.5625 * (r -= 2.625 / 2.75) * r + 0.984375) + t, jo = (r, t, e, i) => e - rs(i - r, 0, e, i) + t, Wa = (r, t, e, i) => r < i / 2 ? 0.5 * jo(2 * r, 0, e, i) + t : 0.5 * rs(2 * r - i, 0, e, i) + 0.5 * e + t, Va = (r, t, e, i) => e * (r /= i) * r + t, Ha = (r, t, e, i) => -e * (r /= i) * (r - 2) + t, za = (r, t, e, i) => (r /= i / 2) < 1 ? e / 2 * r ** 2 + t : -e / 2 * (--r * (r - 2) - 1) + t, Ga = () => !1, is = class {
  constructor({ startValue: r, byValue: t, duration: e = 500, delay: i = 0, easing: s = Po, onStart: o = Cr, onChange: n = Cr, onComplete: a = Cr, abort: l = Ga, target: h }) {
    f(this, "_state", "pending"), f(this, "durationProgress", 0), f(this, "valueProgress", 0), this.tick = this.tick.bind(this), this.duration = e, this.delay = i, this.easing = s, this._onStart = o, this._onChange = n, this._onComplete = a, this._abort = l, this.target = h, this.startValue = r, this.byValue = t, this.value = this.startValue, this.endValue = Object.freeze(this.calculate(this.duration).value);
  }
  get state() {
    return this._state;
  }
  isDone() {
    return this._state === "aborted" || this._state === "completed";
  }
  start() {
    let r = (t) => {
      this._state === "pending" && (this.startTime = t || +/* @__PURE__ */ new Date(), this._state = "running", this._onStart(), this.tick(this.startTime));
    };
    this.register(), this.delay > 0 ? this.timeout = fe().setTimeout(() => Ke(r), this.delay) : Ke(r);
  }
  tick(r) {
    let t = (r || +/* @__PURE__ */ new Date()) - this.startTime, e = Math.min(t, this.duration);
    this.durationProgress = e / this.duration;
    let { value: i, valueProgress: s } = this.calculate(e);
    this.value = Object.freeze(i), this.valueProgress = s, this._state !== "aborted" && (this._abort(this.value, this.valueProgress, this.durationProgress) ? (this._state = "aborted", this.unregister()) : t >= this.duration ? (this.durationProgress = this.valueProgress = 1, this._onChange(this.endValue, this.valueProgress, this.durationProgress), this._state = "completed", this._onComplete(this.endValue, this.valueProgress, this.durationProgress), this.unregister(), this.timeout = null) : (this._onChange(this.value, this.valueProgress, this.durationProgress), Ke(this.tick)));
  }
  register() {
    Dr.push(this);
  }
  unregister() {
    Dr.remove(this);
  }
  abort() {
    this._state = "aborted", this.unregister(), this.timeout && fe().clearTimeout(this.timeout);
  }
}, Ua = class extends is {
  constructor({ startValue: r = 0, endValue: t = 100, ...e }) {
    super({
      ...e,
      startValue: r,
      byValue: t - r
    });
  }
  calculate(r) {
    let t = this.easing(r, this.startValue, this.byValue, this.duration);
    return {
      value: t,
      valueProgress: Math.abs((t - this.startValue) / this.byValue)
    };
  }
}, Na = class extends is {
  constructor({ startValue: r = [0], endValue: t = [100], ...e }) {
    super({
      ...e,
      startValue: r,
      byValue: t.map((i, s) => i - r[s])
    });
  }
  calculate(r) {
    let t = this.startValue.map((e, i) => this.easing(r, e, this.byValue[i], this.duration, i));
    return {
      value: t,
      valueProgress: Math.abs((t[0] - this.startValue[0]) / this.byValue[0])
    };
  }
}, qa = (r, t, e, i) => t + e * (1 - Math.cos(r / i * Yt)), ti = (r) => r && ((t, e, i) => r(new et(t).toRgba(), e, i)), Ka = class extends is {
  constructor({ startValue: r, endValue: t, easing: e = qa, onChange: i, onComplete: s, abort: o, ...n }) {
    let a = new et(r).getSource(), l = new et(t).getSource();
    super({
      ...n,
      startValue: a,
      byValue: l.map((h, c) => h - a[c]),
      easing: e,
      onChange: ti(i),
      onComplete: ti(s),
      abort: ti(o)
    });
  }
  calculate(r) {
    let [t, e, i, s] = this.startValue.map((n, a) => this.easing(r, n, this.byValue[a], this.duration, a)), o = [...[
      t,
      e,
      i
    ].map(Math.round), te(0, s, 1)];
    return {
      value: o,
      valueProgress: o.map((n, a) => this.byValue[a] === 0 ? 0 : Math.abs((n - this.startValue[a]) / this.byValue[a])).find((n) => n !== 0) || 0
    };
  }
};
function ss(r) {
  let t = ((e) => Array.isArray(e.startValue) || Array.isArray(e.endValue))(r) ? new Na(r) : new Ua(r);
  return t.start(), t;
}
function Ao(r) {
  let t = new Ka(r);
  return t.start(), t;
}
var Qe = class H {
  constructor(t) {
    this.status = t, this.points = [];
  }
  includes(t) {
    return this.points.some((e) => e.eq(t));
  }
  append(...t) {
    return this.points = this.points.concat(t.filter((e) => !this.includes(e))), this;
  }
  static isPointContained(t, e, i, s = !1) {
    if (e.eq(i)) return t.eq(e);
    if (e.x === i.x) return t.x === e.x && (s || t.y >= Math.min(e.y, i.y) && t.y <= Math.max(e.y, i.y));
    if (e.y === i.y) return t.y === e.y && (s || t.x >= Math.min(e.x, i.x) && t.x <= Math.max(e.x, i.x));
    {
      let o = tr(e, i), n = tr(e, t).divide(o);
      return s ? Math.abs(n.x) === Math.abs(n.y) : n.x === n.y && n.x >= 0 && n.x <= 1;
    }
  }
  static isPointInPolygon(t, e) {
    let i = new v(t).setX(Math.min(t.x - 1, ...e.map((o) => o.x))), s = 0;
    for (let o = 0; o < e.length; o++) {
      let n = this.intersectSegmentSegment(e[o], e[(o + 1) % e.length], t, i);
      if (n.includes(t)) return !0;
      s += +(n.status === "Intersection");
    }
    return s % 2 == 1;
  }
  static intersectLineLine(t, e, i, s, o = !0, n = !0) {
    let a = e.x - t.x, l = e.y - t.y, h = s.x - i.x, c = s.y - i.y, u = t.x - i.x, d = t.y - i.y, g = h * d - c * u, p = a * d - l * u, m = c * a - h * l;
    if (m !== 0) {
      let y = g / m, x = p / m;
      return (o || 0 <= y && y <= 1) && (n || 0 <= x && x <= 1) ? new H("Intersection").append(new v(t.x + y * a, t.y + y * l)) : new H();
    }
    return new H(g === 0 || p === 0 ? o || n || H.isPointContained(t, i, s) || H.isPointContained(e, i, s) || H.isPointContained(i, t, e) || H.isPointContained(s, t, e) ? "Coincident" : void 0 : "Parallel");
  }
  static intersectSegmentLine(t, e, i, s) {
    return H.intersectLineLine(t, e, i, s, !1, !0);
  }
  static intersectSegmentSegment(t, e, i, s) {
    return H.intersectLineLine(t, e, i, s, !1, !1);
  }
  static intersectLinePolygon(t, e, i, s = !0) {
    let o = new H(), n = i.length;
    for (let a, l, h, c = 0; c < n; c++) {
      if (a = i[c], l = i[(c + 1) % n], h = H.intersectLineLine(t, e, a, l, s, !1), h.status === "Coincident") return h;
      o.append(...h.points);
    }
    return o.points.length > 0 && (o.status = "Intersection"), o;
  }
  static intersectSegmentPolygon(t, e, i) {
    return H.intersectLinePolygon(t, e, i, !1);
  }
  static intersectPolygonPolygon(t, e) {
    let i = new H(), s = t.length, o = [];
    for (let n = 0; n < s; n++) {
      let a = t[n], l = t[(n + 1) % s], h = H.intersectSegmentPolygon(a, l, e);
      h.status === "Coincident" ? (o.push(h), i.append(a, l)) : i.append(...h.points);
    }
    return o.length > 0 && o.length === t.length ? new H("Coincident") : (i.points.length > 0 && (i.status = "Intersection"), i);
  }
  static intersectPolygonRectangle(t, e, i) {
    let s = e.min(i), o = e.max(i), n = new v(o.x, s.y), a = new v(s.x, o.y);
    return H.intersectPolygonPolygon(t, [
      s,
      n,
      o,
      a
    ]);
  }
}, Ja = class extends io {
  getX() {
    return this.getXY().x;
  }
  setX(r) {
    this.setXY(this.getXY().setX(r));
  }
  getY() {
    return this.getXY().y;
  }
  setY(r) {
    this.setXY(this.getXY().setY(r));
  }
  getRelativeX() {
    return this.left;
  }
  setRelativeX(r) {
    this.left = r;
  }
  getRelativeY() {
    return this.top;
  }
  setRelativeY(r) {
    this.top = r;
  }
  getXY() {
    let r = this.getRelativeXY();
    return this.group ? U(r, this.group.calcTransformMatrix()) : r;
  }
  setXY(r, t, e) {
    this.group && (r = U(r, ot(this.group.calcTransformMatrix()))), this.setRelativeXY(r, t, e);
  }
  getRelativeXY() {
    return new v(this.left, this.top);
  }
  setRelativeXY(r, t = this.originX, e = this.originY) {
    this.setPositionByOrigin(r, t, e);
  }
  isStrokeAccountedForInDimensions() {
    return !1;
  }
  getCoords() {
    let { tl: r, tr: t, br: e, bl: i } = this.aCoords || (this.aCoords = this.calcACoords()), s = [
      r,
      t,
      e,
      i
    ];
    if (this.group) {
      let o = this.group.calcTransformMatrix();
      return s.map((n) => U(n, o));
    }
    return s;
  }
  intersectsWithRect(r, t) {
    return Qe.intersectPolygonRectangle(this.getCoords(), r, t).status === "Intersection";
  }
  intersectsWithObject(r) {
    let t = Qe.intersectPolygonPolygon(this.getCoords(), r.getCoords());
    return t.status === "Intersection" || t.status === "Coincident" || r.isContainedWithinObject(this) || this.isContainedWithinObject(r);
  }
  isContainedWithinObject(r) {
    return this.getCoords().every((t) => r.containsPoint(t));
  }
  isContainedWithinRect(r, t) {
    let { left: e, top: i, width: s, height: o } = this.getBoundingRect();
    return e >= r.x && e + s <= t.x && i >= r.y && i + o <= t.y;
  }
  isOverlapping(r) {
    return this.intersectsWithObject(r) || this.isContainedWithinObject(r) || r.isContainedWithinObject(this);
  }
  containsPoint(r) {
    return Qe.isPointInPolygon(r, this.getCoords());
  }
  isOnScreen() {
    if (!this.canvas) return !1;
    let { tl: r, br: t } = this.canvas.vptCoords;
    return !!this.getCoords().some((e) => e.x <= t.x && e.x >= r.x && e.y <= t.y && e.y >= r.y) || !!this.intersectsWithRect(r, t) || this.containsPoint(r.midPointFrom(t));
  }
  isPartiallyOnScreen() {
    if (!this.canvas) return !1;
    let { tl: r, br: t } = this.canvas.vptCoords;
    return !!this.intersectsWithRect(r, t) || this.getCoords().every((e) => (e.x >= t.x || e.x <= r.x) && (e.y >= t.y || e.y <= r.y)) && this.containsPoint(r.midPointFrom(t));
  }
  getBoundingRect() {
    return St(this.getCoords());
  }
  getScaledWidth() {
    return this._getTransformedDimensions().x;
  }
  getScaledHeight() {
    return this._getTransformedDimensions().y;
  }
  scale(r) {
    this._set(Wt, r), this._set(Vt, r), this.setCoords();
  }
  scaleToWidth(r) {
    let t = this.getBoundingRect().width / this.getScaledWidth();
    return this.scale(r / this.width / t);
  }
  scaleToHeight(r) {
    let t = this.getBoundingRect().height / this.getScaledHeight();
    return this.scale(r / this.height / t);
  }
  getCanvasRetinaScaling() {
    var r;
    return ((r = this.canvas) == null ? void 0 : r.getRetinaScaling()) || 1;
  }
  getTotalAngle() {
    return this.group ? Dt(Wi(this.calcTransformMatrix())) : this.angle;
  }
  getViewportTransform() {
    var r;
    return ((r = this.canvas) == null ? void 0 : r.viewportTransform) || Z.concat();
  }
  calcACoords() {
    let r = ee({ angle: this.angle }), { x: t, y: e } = this.getRelativeCenterPoint(), i = $(be(t, e), r), s = this._getTransformedDimensions(), o = s.x / 2, n = s.y / 2;
    return {
      tl: U({
        x: -o,
        y: -n
      }, i),
      tr: U({
        x: o,
        y: -n
      }, i),
      bl: U({
        x: -o,
        y: n
      }, i),
      br: U({
        x: o,
        y: n
      }, i)
    };
  }
  setCoords() {
    this.aCoords = this.calcACoords();
  }
  transformMatrixKey(r = !1) {
    let t = [];
    return !r && this.group && (t = this.group.transformMatrixKey(r)), t.push(this.top, this.left, this.width, this.height, this.scaleX, this.scaleY, this.angle, this.strokeWidth, this.skewX, this.skewY, +this.flipX, +this.flipY, J(this.originX), J(this.originY)), t;
  }
  calcTransformMatrix(r = !1) {
    let t = this.calcOwnMatrix();
    if (r || !this.group) return t;
    let e = this.transformMatrixKey(r), i = this.matrixCache;
    return i && i.key.every((s, o) => s === e[o]) ? i.value : (this.group && (t = $(this.group.calcTransformMatrix(!1), t)), this.matrixCache = {
      key: e,
      value: t
    }, t);
  }
  calcOwnMatrix() {
    let r = this.transformMatrixKey(!0), t = this.ownMatrixCache;
    if (t && t.key.every((s, o) => s === r[o])) return t.value;
    let e = this.getRelativeCenterPoint(), i = ho({
      angle: this.angle,
      translateX: e.x,
      translateY: e.y,
      scaleX: this.scaleX,
      scaleY: this.scaleY,
      skewX: this.skewX,
      skewY: this.skewY,
      flipX: this.flipX,
      flipY: this.flipY
    });
    return this.ownMatrixCache = {
      key: r,
      value: i
    }, i;
  }
  _getNonTransformedDimensions() {
    return new v(this.width, this.height).scalarAdd(this.strokeWidth);
  }
  _calculateCurrentDimensions(r) {
    var t;
    let e = (t = this.canvas) == null ? void 0 : t.viewportTransform, i = this._getTransformedDimensions(r);
    return e ? i.multiply(new v(Vi(e), ao(e))).scalarAdd(2 * this.padding) : i.scalarAdd(2 * this.padding);
  }
  _getTransformedDimensions(r = {}) {
    let t = {
      scaleX: this.scaleX,
      scaleY: this.scaleY,
      skewX: this.skewX,
      skewY: this.skewY,
      width: this.width,
      height: this.height,
      strokeWidth: this.strokeWidth,
      ...r
    }, e = t.strokeWidth, i = e, s = 0;
    this.strokeUniform && (i = 0, s = e);
    let o = t.width + i, n = t.height + i, a;
    return a = t.skewX === 0 && t.skewY === 0 ? new v(o * t.scaleX, n * t.scaleY) : Yr(o, n, sr(t)), a.scalarAdd(s);
  }
  translateToGivenOrigin(r, t, e, i, s) {
    let o = r.x, n = r.y, a = J(i) - J(t), l = J(s) - J(e);
    if (a || l) {
      let h = this._getTransformedDimensions();
      o += a * h.x, n += l * h.y;
    }
    return new v(o, n);
  }
  translateToCenterPoint(r, t, e) {
    if (t === "center" && e === "center") return r;
    let i = this.translateToGivenOrigin(r, t, e, L, L);
    return this.angle ? i.rotate(B(this.angle), r) : i;
  }
  translateToOriginPoint(r, t, e) {
    let i = this.translateToGivenOrigin(r, L, L, t, e);
    return this.angle ? i.rotate(B(this.angle), r) : i;
  }
  getCenterPoint() {
    let r = this.getRelativeCenterPoint();
    return this.group ? U(r, this.group.calcTransformMatrix()) : r;
  }
  getRelativeCenterPoint() {
    return this.translateToCenterPoint(new v(this.left, this.top), this.originX, this.originY);
  }
  getPointByOrigin(r, t) {
    return this.getPositionByOrigin(r, t);
  }
  getPositionByOrigin(r, t) {
    return this.translateToOriginPoint(this.getRelativeCenterPoint(), r, t);
  }
  setPositionByOrigin(r, t, e) {
    let i = this.translateToCenterPoint(r, t, e), s = this.translateToOriginPoint(i, this.originX, this.originY);
    this.set({
      left: s.x,
      top: s.y
    });
  }
  _getLeftTopCoords() {
    return this.getPositionByOrigin(V, "top");
  }
  positionByLeftTop(r) {
    return this.setPositionByOrigin(r, V, "top");
  }
}, wt = class Tr extends Ja {
  static getDefaults() {
    return Tr.ownDefaults;
  }
  get type() {
    let t = this.constructor.type;
    return t === "FabricObject" ? "object" : t.toLowerCase();
  }
  set type(t) {
    Xt("warn", "Setting type has no effect", t);
  }
  constructor(t) {
    super(), f(this, "_cacheContext", null), Object.assign(this, Tr.ownDefaults), this.setOptions(t);
  }
  _createCacheCanvas() {
    this._cacheCanvas = bt(), this._cacheContext = this._cacheCanvas.getContext("2d"), this._updateCacheCanvas(), this.dirty = !0;
  }
  _limitCacheSize(t) {
    let e = t.width, i = t.height, s = P.maxCacheSideLimit, o = P.minCacheSideLimit;
    if (e <= s && i <= s && e * i <= P.perfLimitSizeTotal) return e < o && (t.width = o), i < o && (t.height = o), t;
    let n = e / i, [a, l] = qe.limitDimsByArea(n), h = te(o, a, s), c = te(o, l, s);
    return e > h && (t.zoomX /= e / h, t.width = h, t.capped = !0), i > c && (t.zoomY /= i / c, t.height = c, t.capped = !0), t;
  }
  _getCacheCanvasDimensions() {
    let t = this.getTotalObjectScaling(), e = this._getTransformedDimensions({
      skewX: 0,
      skewY: 0
    }), i = e.x * t.x / this.scaleX, s = e.y * t.y / this.scaleY;
    return {
      width: Math.ceil(i + 2),
      height: Math.ceil(s + 2),
      zoomX: t.x,
      zoomY: t.y,
      x: i,
      y: s
    };
  }
  _updateCacheCanvas() {
    let t = this._cacheCanvas, e = this._cacheContext, { width: i, height: s, zoomX: o, zoomY: n, x: a, y: l } = this._limitCacheSize(this._getCacheCanvasDimensions()), h = i !== t.width || s !== t.height, c = this.zoomX !== o || this.zoomY !== n;
    if (!t || !e) return !1;
    if (h || c) {
      i !== t.width || s !== t.height ? (t.width = i, t.height = s) : (e.setTransform(1, 0, 0, 1, 0, 0), e.clearRect(0, 0, t.width, t.height));
      let u = a / 2, d = l / 2;
      return this.cacheTranslationX = Math.round(t.width / 2 - u) + u, this.cacheTranslationY = Math.round(t.height / 2 - d) + d, e.translate(this.cacheTranslationX, this.cacheTranslationY), e.scale(o, n), this.zoomX = o, this.zoomY = n, !0;
    }
    return !1;
  }
  setOptions(t = {}) {
    this._setOptions(t);
  }
  transform(t) {
    let e = this.group && !this.group._transformDone || this.group && this.canvas && t === this.canvas.contextTop, i = this.calcTransformMatrix(!e);
    t.transform(i[0], i[1], i[2], i[3], i[4], i[5]);
  }
  getObjectScaling() {
    if (!this.group) return new v(Math.abs(this.scaleX), Math.abs(this.scaleY));
    let t = pe(this.calcTransformMatrix());
    return new v(Math.abs(t.scaleX), Math.abs(t.scaleY));
  }
  getTotalObjectScaling() {
    let t = this.getObjectScaling();
    if (this.canvas) {
      let e = this.canvas.getZoom(), i = this.getCanvasRetinaScaling();
      return t.scalarMultiply(e * i);
    }
    return t;
  }
  getObjectOpacity() {
    let t = this.opacity;
    return this.group && (t *= this.group.getObjectOpacity()), t;
  }
  _constrainScale(t) {
    return Math.abs(t) < this.minScaleLimit ? t < 0 ? -this.minScaleLimit : this.minScaleLimit : t === 0 ? 1e-4 : t;
  }
  _set(t, e) {
    t !== "scaleX" && t !== "scaleY" || (e = this._constrainScale(e)), t === "scaleX" && e < 0 ? (this.flipX = !this.flipX, e *= -1) : t === "scaleY" && e < 0 ? (this.flipY = !this.flipY, e *= -1) : t !== "shadow" || !e || e instanceof de || (e = new de(e));
    let i = this[t] !== e;
    return this[t] = e, i && this.constructor.cacheProperties.includes(t) && (this.dirty = !0), this.parent && (this.dirty || i && this.constructor.stateProperties.includes(t)) && this.parent._set("dirty", !0), this;
  }
  isNotVisible() {
    return this.opacity === 0 || !this.width && !this.height && this.strokeWidth === 0 || !this.visible;
  }
  render(t) {
    this.isNotVisible() || this.canvas && this.canvas.skipOffscreen && !this.group && !this.isOnScreen() || (t.save(), this._setupCompositeOperation(t), this.drawSelectionBackground(t), this.transform(t), this._setOpacity(t), this._setShadow(t), this.shouldCache() ? (this.renderCache(), this.drawCacheOnCanvas(t)) : (this._removeCacheCanvas(), this.drawObject(t, !1, {}), this.dirty = !1), t.restore());
  }
  drawSelectionBackground(t) {
  }
  renderCache(t) {
    if (t = t || {}, this._cacheCanvas && this._cacheContext || this._createCacheCanvas(), this.isCacheDirty() && this._cacheContext) {
      let { zoomX: e, zoomY: i, cacheTranslationX: s, cacheTranslationY: o } = this, { width: n, height: a } = this._cacheCanvas;
      this.drawObject(this._cacheContext, t.forClipping, {
        zoomX: e,
        zoomY: i,
        cacheTranslationX: s,
        cacheTranslationY: o,
        width: n,
        height: a,
        parentClipPaths: []
      }), this.dirty = !1;
    }
  }
  _removeCacheCanvas() {
    this._cacheCanvas = void 0, this._cacheContext = null;
  }
  hasStroke() {
    return !!this.stroke && this.stroke !== "transparent" && this.strokeWidth !== 0;
  }
  hasFill() {
    return !!this.fill && this.fill !== "transparent";
  }
  needsItsOwnCache() {
    return !!(this.paintFirst === "stroke" && this.hasFill() && this.hasStroke() && this.shadow) || !!this.clipPath;
  }
  shouldCache() {
    return this.ownCaching = this.objectCaching && (!this.parent || !this.parent.isOnACache()) || this.needsItsOwnCache(), this.ownCaching;
  }
  willDrawShadow() {
    return !!this.shadow && (this.shadow.offsetX !== 0 || this.shadow.offsetY !== 0);
  }
  drawClipPathOnCache(t, e, i) {
    t.save(), e.inverted ? t.globalCompositeOperation = "destination-out" : t.globalCompositeOperation = "destination-in", t.setTransform(1, 0, 0, 1, 0, 0), t.drawImage(i, 0, 0), t.restore();
  }
  drawObject(t, e, i) {
    let s = this.fill, o = this.stroke;
    e ? (this.fill = "black", this.stroke = "", this._setClippingProperties(t)) : this._renderBackground(t), this.fire("before:render", { ctx: t }), this._render(t), this._drawClipPath(t, this.clipPath, i), this.fill = s, this.stroke = o;
  }
  createClipPathLayer(t, e) {
    let i = nt(e), s = i.getContext("2d");
    if (s.translate(e.cacheTranslationX, e.cacheTranslationY), s.scale(e.zoomX, e.zoomY), t._cacheCanvas = i, e.parentClipPaths.forEach((o) => {
      o.transform(s);
    }), e.parentClipPaths.push(t), t.absolutePositioned) {
      let o = ot(this.calcTransformMatrix());
      s.transform(o[0], o[1], o[2], o[3], o[4], o[5]);
    }
    return t.transform(s), t.drawObject(s, !0, e), i;
  }
  _drawClipPath(t, e, i) {
    if (!e) return;
    e._transformDone = !0;
    let s = this.createClipPathLayer(e, i);
    this.drawClipPathOnCache(t, e, s);
  }
  drawCacheOnCanvas(t) {
    t.scale(1 / this.zoomX, 1 / this.zoomY), t.drawImage(this._cacheCanvas, -this.cacheTranslationX, -this.cacheTranslationY);
  }
  isCacheDirty(t = !1) {
    if (this.isNotVisible()) return !1;
    let e = this._cacheCanvas, i = this._cacheContext;
    return !(!e || !i || t || !this._updateCacheCanvas()) || !!(this.dirty || this.clipPath && this.clipPath.absolutePositioned) && (e && i && !t && (i.save(), i.setTransform(1, 0, 0, 1, 0, 0), i.clearRect(0, 0, e.width, e.height), i.restore()), !0);
  }
  _renderBackground(t) {
    if (!this.backgroundColor) return;
    let e = this._getNonTransformedDimensions();
    t.fillStyle = this.backgroundColor, t.fillRect(-e.x / 2, -e.y / 2, e.x, e.y), this._removeShadow(t);
  }
  _setOpacity(t) {
    this.group && !this.group._transformDone ? t.globalAlpha = this.getObjectOpacity() : t.globalAlpha *= this.opacity;
  }
  _setStrokeStyles(t, e) {
    let i = e.stroke;
    i && (t.lineWidth = e.strokeWidth, t.lineCap = e.strokeLineCap, t.lineDashOffset = e.strokeDashOffset, t.lineJoin = e.strokeLineJoin, t.miterLimit = e.strokeMiterLimit, ht(i) ? i.gradientUnits === "percentage" || i.gradientTransform || i.patternTransform ? this._applyPatternForTransformedGradient(t, i) : (t.strokeStyle = i.toLive(t), this._applyPatternGradientTransform(t, i)) : t.strokeStyle = e.stroke);
  }
  _setFillStyles(t, { fill: e }) {
    e && (ht(e) ? (t.fillStyle = e.toLive(t), this._applyPatternGradientTransform(t, e)) : t.fillStyle = e);
  }
  _setClippingProperties(t) {
    t.globalAlpha = 1, t.strokeStyle = "transparent", t.fillStyle = "#000000";
  }
  _setLineDash(t, e) {
    e && e.length !== 0 && t.setLineDash(e);
  }
  _setShadow(t) {
    if (!this.shadow) return;
    let e = this.shadow, i = this.canvas, s = this.getCanvasRetinaScaling(), [o, , , n] = i?.viewportTransform || Z, a = o * s, l = n * s, h = e.nonScaling ? new v(1, 1) : this.getObjectScaling();
    t.shadowColor = e.color, t.shadowBlur = e.blur * P.browserShadowBlurConstant * (a + l) * (h.x + h.y) / 4, t.shadowOffsetX = e.offsetX * a * h.x, t.shadowOffsetY = e.offsetY * l * h.y;
  }
  _removeShadow(t) {
    this.shadow && (t.shadowColor = "", t.shadowBlur = t.shadowOffsetX = t.shadowOffsetY = 0);
  }
  _applyPatternGradientTransform(t, e) {
    if (!ht(e)) return {
      offsetX: 0,
      offsetY: 0
    };
    let i = e.gradientTransform || e.patternTransform, s = -this.width / 2 + e.offsetX || 0, o = -this.height / 2 + e.offsetY || 0;
    return e.gradientUnits === "percentage" ? t.transform(this.width, 0, 0, this.height, s, o) : t.transform(1, 0, 0, 1, s, o), i && t.transform(i[0], i[1], i[2], i[3], i[4], i[5]), {
      offsetX: s,
      offsetY: o
    };
  }
  _renderPaintInOrder(t) {
    this.paintFirst === "stroke" ? (this._renderStroke(t), this._renderFill(t)) : (this._renderFill(t), this._renderStroke(t));
  }
  _render(t) {
  }
  _renderFill(t) {
    this.fill && (t.save(), this._setFillStyles(t, this), this.fillRule === "evenodd" ? t.fill("evenodd") : t.fill(), t.restore());
  }
  _renderStroke(t) {
    if (this.stroke && this.strokeWidth !== 0) {
      if (this.shadow && !this.shadow.affectStroke && this._removeShadow(t), t.save(), this.strokeUniform) {
        let e = this.getObjectScaling();
        t.scale(1 / e.x, 1 / e.y);
      }
      this._setLineDash(t, this.strokeDashArray), this._setStrokeStyles(t, this), t.stroke(), t.restore();
    }
  }
  _applyPatternForTransformedGradient(t, e) {
    var i;
    let s = this._limitCacheSize(this._getCacheCanvasDimensions()), o = this.getCanvasRetinaScaling(), n = s.x / this.scaleX / o, a = s.y / this.scaleY / o, l = nt({
      width: Math.ceil(n),
      height: Math.ceil(a)
    }), h = l.getContext("2d");
    h && (h.beginPath(), h.moveTo(0, 0), h.lineTo(n, 0), h.lineTo(n, a), h.lineTo(0, a), h.closePath(), h.translate(n / 2, a / 2), h.scale(s.zoomX / this.scaleX / o, s.zoomY / this.scaleY / o), this._applyPatternGradientTransform(h, e), h.fillStyle = e.toLive(t), h.fill(), t.translate(-this.width / 2 - this.strokeWidth / 2, -this.height / 2 - this.strokeWidth / 2), t.scale(o * this.scaleX / s.zoomX, o * this.scaleY / s.zoomY), t.strokeStyle = (i = h.createPattern(l, "no-repeat")) == null ? "" : i);
  }
  _findCenterFromElement() {
    return new v(this.left + this.width / 2, this.top + this.height / 2);
  }
  clone(t) {
    let e = this.toObject(t);
    return this.constructor.fromObject(e);
  }
  cloneAsImage(t) {
    let e = this.toCanvasElement(t);
    return new (w.getClass("image"))(e);
  }
  toCanvasElement(t = {}) {
    let e = Ui(this), i = this.group, s = this.shadow, o = Math.abs, n = t.enableRetinaScaling ? Us() : 1, a = (t.multiplier || 1) * n, l = t.canvasProvider || ((_) => new $r(_, {
      enableRetinaScaling: !1,
      renderOnAddRemove: !1,
      skipOffscreen: !1
    }));
    delete this.group, t.withoutTransform && yo(this), t.withoutShadow && (this.shadow = null), t.viewportTransform && Ni(this, this.getViewportTransform()), this.setCoords();
    let h = bt(), c = this.getBoundingRect(), u = this.shadow, d = new v();
    if (u) {
      let _ = u.blur, S = u.nonScaling ? new v(1, 1) : this.getObjectScaling();
      d.x = 2 * Math.round(o(u.offsetX) + _) * o(S.x), d.y = 2 * Math.round(o(u.offsetY) + _) * o(S.y);
    }
    let g = c.width + d.x, p = c.height + d.y;
    h.width = Math.ceil(g), h.height = Math.ceil(p);
    let m = l(h);
    t.format === "jpeg" && (m.backgroundColor = "#fff"), this.setPositionByOrigin(new v(m.width / 2, m.height / 2), L, L);
    let y = this.canvas;
    m._objects = [this], this.set("canvas", m), this.setCoords();
    let x = m.toCanvasElement(a || 1, t);
    return this.set("canvas", y), this.shadow = s, i && (this.group = i), this.set(e), this.setCoords(), m._objects = [], m.destroy(), x;
  }
  toDataURL(t = {}) {
    return $i(this.toCanvasElement(t), t.format || "png", t.quality || 1);
  }
  toBlob(t = {}) {
    return Yi(this.toCanvasElement(t), t.format || "png", t.quality || 1);
  }
  isType(...t) {
    return t.includes(this.constructor.type) || t.includes(this.type);
  }
  complexity() {
    return 1;
  }
  toJSON() {
    return this.toObject();
  }
  rotate(t) {
    let { centeredRotation: e, originX: i, originY: s } = this;
    if (e) {
      let { x: o, y: n } = this.getRelativeCenterPoint();
      this.originX = L, this.originY = L, this.left = o, this.top = n;
    }
    if (this.set("angle", t), e) {
      let { x: o, y: n } = this.getPositionByOrigin(i, s);
      this.left = o, this.top = n, this.originX = i, this.originY = s;
    }
  }
  setOnGroup() {
  }
  _setupCompositeOperation(t) {
    this.globalCompositeOperation && (t.globalCompositeOperation = this.globalCompositeOperation);
  }
  dispose() {
    Dr.cancelByTarget(this), this.off(), this._set("canvas", void 0), this._cacheCanvas && Ct().dispose(this._cacheCanvas), this._cacheCanvas = void 0, this._cacheContext = null;
  }
  animate(t, e) {
    return Object.entries(t).reduce((i, [s, o]) => (i[s] = this._animate(s, o, e), i), {});
  }
  _animate(t, e, i = {}) {
    let s = t.split("."), o = this.constructor.colorProperties.includes(s[s.length - 1]), { abort: n, startValue: a, onChange: l, onComplete: h } = i, c = {
      ...i,
      target: this,
      startValue: a ?? s.reduce((u, d) => u[d], this),
      endValue: e,
      abort: n?.bind(this),
      onChange: (u, d, g) => {
        s.reduce((p, m, y) => (y === s.length - 1 && (p[m] = u), p[m]), this), l && l(u, d, g);
      },
      onComplete: (u, d, g) => {
        this.setCoords(), h && h(u, d, g);
      }
    };
    return o ? Ao(c) : ss(c);
  }
  isDescendantOf(t) {
    let { parent: e, group: i } = this;
    return e === t || i === t || !!e && e.isDescendantOf(t) || !!i && i !== e && i.isDescendantOf(t);
  }
  getAncestors() {
    let t = [], e = this;
    do
      e = e.parent, e && t.push(e);
    while (e);
    return t;
  }
  findCommonAncestors(t) {
    if (this === t) return {
      fork: [],
      otherFork: [],
      common: [this, ...this.getAncestors()]
    };
    let e = this.getAncestors(), i = t.getAncestors();
    if (e.length === 0 && i.length > 0 && this === i[i.length - 1]) return {
      fork: [],
      otherFork: [t, ...i.slice(0, i.length - 1)],
      common: [this]
    };
    for (let s, o = 0; o < e.length; o++) {
      if (s = e[o], s === t) return {
        fork: [this, ...e.slice(0, o)],
        otherFork: [],
        common: e.slice(o)
      };
      for (let n = 0; n < i.length; n++) {
        if (this === i[n]) return {
          fork: [],
          otherFork: [t, ...i.slice(0, n)],
          common: [this, ...e]
        };
        if (s === i[n]) return {
          fork: [this, ...e.slice(0, o)],
          otherFork: [t, ...i.slice(0, n)],
          common: e.slice(o)
        };
      }
    }
    return {
      fork: [this, ...e],
      otherFork: [t, ...i],
      common: []
    };
  }
  hasCommonAncestors(t) {
    let e = this.findCommonAncestors(t);
    return e && !!e.common.length;
  }
  isInFrontOf(t) {
    if (this === t) return;
    let e = this.findCommonAncestors(t);
    if (e.fork.includes(t)) return !0;
    if (e.otherFork.includes(this)) return !1;
    let i = e.common[0] || this.canvas;
    if (!i) return;
    let s = e.fork.pop(), o = e.otherFork.pop(), n = i._objects.indexOf(s), a = i._objects.indexOf(o);
    return n > -1 && n > a;
  }
  toObject(t = []) {
    let e = t.concat(Tr.customProperties, this.constructor.customProperties || []), i, s = P.NUM_FRACTION_DIGITS, { clipPath: o, fill: n, stroke: a, shadow: l, strokeDashArray: h, left: c, top: u, originX: d, originY: g, width: p, height: m, strokeWidth: y, strokeLineCap: x, strokeDashOffset: _, strokeLineJoin: S, strokeUniform: C, strokeMiterLimit: b, scaleX: O, scaleY: T, angle: k, flipX: D, flipY: I, opacity: j, visible: E, backgroundColor: R, fillRule: X, paintFirst: z, globalCompositeOperation: Y, skewX: q, skewY: rt } = this;
    o && !o.excludeFromExport && (i = o.toObject(e.concat("inverted", "absolutePositioned")));
    let A = (we) => F(we, s), yt = {
      ...re(this, e),
      type: this.constructor.type,
      version: li,
      originX: d,
      originY: g,
      left: A(c),
      top: A(u),
      width: A(p),
      height: A(m),
      fill: vs(n) ? n.toObject() : n,
      stroke: vs(a) ? a.toObject() : a,
      strokeWidth: A(y),
      strokeDashArray: h && h.concat(),
      strokeLineCap: x,
      strokeDashOffset: _,
      strokeLineJoin: S,
      strokeUniform: C,
      strokeMiterLimit: A(b),
      scaleX: A(O),
      scaleY: A(T),
      angle: A(k),
      flipX: D,
      flipY: I,
      opacity: A(j),
      shadow: l && l.toObject(),
      visible: E,
      backgroundColor: R,
      fillRule: X,
      paintFirst: z,
      globalCompositeOperation: Y,
      skewX: A(q),
      skewY: A(rt),
      ...i ? { clipPath: i } : null
    };
    return this.includeDefaultValues ? yt : this._removeDefaultValues(yt);
  }
  toDatalessObject(t) {
    return this.toObject(t);
  }
  _removeDefaultValues(t) {
    let e = this.constructor.getDefaults(), i = Object.keys(e).length > 0 ? e : Object.getPrototypeOf(this);
    return Gi(t, (s, o) => {
      if (o === "left" || o === "top" || o === "type") return !0;
      let n = i[o];
      return s !== n && !(Array.isArray(s) && Array.isArray(n) && s.length === 0 && n.length === 0);
    });
  }
  toString() {
    return `#<${this.constructor.type}>`;
  }
  static _fromObject({ type: t, ...e }, { extraParam: i, ...s } = {}) {
    return or(e, s).then((o) => i ? (delete o[i], new this(e[i], o)) : new this(o));
  }
  static fromObject(t, e) {
    return this._fromObject(t, e);
  }
};
f(wt, "stateProperties", pa), f(wt, "cacheProperties", Pt), f(wt, "ownDefaults", ma), f(wt, "type", "FabricObject"), f(wt, "colorProperties", [
  tt,
  Mt,
  "backgroundColor"
]), f(wt, "customProperties", []), w.setClass(wt), w.setClass(wt, "object");
var os = (r, t) => {
  var e;
  let { transform: { target: i } } = t;
  (e = i.canvas) == null || e.fire(`object:${r}`, {
    ...t,
    target: i
  }), i.fire(r, t);
}, jt = (r, t, e) => (i, s, o, n) => {
  let a = t(i, s, o, n);
  return a && os(r, {
    ...Zi(i, s, o, n),
    ...e
  }), a;
};
function Ht(r) {
  return (t, e, i, s) => {
    let { target: o, originX: n, originY: a } = e, l = o.getPositionByOrigin(n, a), h = r(t, e, i, s);
    return o.setPositionByOrigin(l, e.originX, e.originY), h;
  };
}
var Fo = (r, t, e, i) => (s, o, n, a) => {
  let l = Vr(o, o.originX, o.originY, n, a)[e], h = J(o[t]);
  if (h === 0 || h > 0 && l < 0 || h < 0 && l > 0) {
    let { target: c } = o, u = c.strokeWidth / (c.strokeUniform ? c[i] : 1), d = Co(o) ? 2 : 1, g = c[r], p = Math.abs(l * d / c[i]) - u;
    return c.set(r, Math.max(p, 1)), g !== c[r];
  }
  return !1;
}, Lo = Fo("width", "originX", "x", "scaleX"), Ro = Fo("height", "originY", "y", "scaleY"), ui = jt(Ze, Ht(Lo)), Qa = jt(Ze, Ht(Ro));
function Io(r, t, e, i, s) {
  r.save();
  let { stroke: o, xSize: n, ySize: a, opName: l } = this.commonRenderProps(r, t, e, s, i), h = n;
  n > a ? r.scale(1, a / n) : a > n && (h = a, r.scale(n / a, 1)), r.beginPath(), r.arc(0, 0, h / 2, 0, pt, !1), r[l](), o && r.stroke(), r.restore();
}
function Bo(r, t, e, i, s) {
  r.save();
  let { stroke: o, xSize: n, ySize: a, opName: l } = this.commonRenderProps(r, t, e, s, i), h = n / 2, c = a / 2;
  r[`${l}Rect`](-h, -c, n, a), o && r.strokeRect(-h, -c, n, a), r.restore();
}
var st = class {
  constructor(r) {
    f(this, "visible", !0), f(this, "actionName", to), f(this, "angle", 0), f(this, "x", 0), f(this, "y", 0), f(this, "offsetX", 0), f(this, "offsetY", 0), f(this, "sizeX", 0), f(this, "sizeY", 0), f(this, "touchSizeX", 0), f(this, "touchSizeY", 0), f(this, "cursorStyle", "crosshair"), f(this, "withConnection", !1), Object.assign(this, r);
  }
  getTransformAnchorPoint() {
    var r;
    return (r = this.transformAnchorPoint) == null ? new v(0.5 - this.x, 0.5 - this.y) : r;
  }
  shouldActivate(r, t, e, { tl: i, tr: s, br: o, bl: n }) {
    var a;
    return ((a = t.canvas) == null ? void 0 : a.getActiveObject()) === t && t.isControlVisible(r) && Qe.isPointInPolygon(e, [
      i,
      s,
      o,
      n
    ]);
  }
  getActionHandler(r, t, e) {
    return this.actionHandler;
  }
  getMouseDownHandler(r, t, e) {
    return this.mouseDownHandler;
  }
  getMouseUpHandler(r, t, e) {
    return this.mouseUpHandler;
  }
  cursorStyleHandler(r, t, e, i) {
    return t.cursorStyle;
  }
  getActionName(r, t, e) {
    return t.actionName;
  }
  getVisibility(r, t) {
    var e, i;
    return (e = (i = r._controlsVisibility) == null ? void 0 : i[t]) == null ? this.visible : e;
  }
  setVisibility(r, t, e) {
    this.visible = r;
  }
  positionHandler(r, t, e, i) {
    return new v(this.x * r.x + this.offsetX, this.y * r.y + this.offsetY).transform(t);
  }
  calcCornerCoords(r, t, e, i, s, o) {
    let n = Ir([
      be(e, i),
      ee({ angle: r }),
      Br((s ? this.touchSizeX : this.sizeX) || t, (s ? this.touchSizeY : this.sizeY) || t)
    ]);
    return {
      tl: new v(-0.5, -0.5).transform(n),
      tr: new v(0.5, -0.5).transform(n),
      br: new v(0.5, 0.5).transform(n),
      bl: new v(-0.5, 0.5).transform(n)
    };
  }
  commonRenderProps(r, t, e, i, s = {}) {
    let { cornerSize: o, cornerColor: n, transparentCorners: a, cornerStrokeColor: l } = s, h = o || i.cornerSize, c = this.sizeX || h, u = this.sizeY || h, d = a === void 0 ? i.transparentCorners : a, g = d ? Mt : tt, p = l || i.cornerStrokeColor, m = !d && !!p;
    return r.fillStyle = n || i.cornerColor || "", r.strokeStyle = p || "", r.translate(t, e), r.rotate(B(i.getTotalAngle())), {
      stroke: m,
      xSize: c,
      ySize: u,
      transparentCorners: d,
      opName: g
    };
  }
  render(r, t, e, i, s) {
    ((i = i || {}).cornerStyle || s.cornerStyle) === "circle" ? Io.call(this, r, t, e, i, s) : Bo.call(this, r, t, e, i, s);
  }
}, Xo = (r, t, e) => e.lockRotation ? Qi : t.cursorStyle, $o = jt(Ks, Ht((r, { target: t, ex: e, ey: i, theta: s, originX: o, originY: n }, a, l) => {
  let h = t.getPositionByOrigin(o, n);
  if (ft(t, "lockRotation")) return !1;
  let c = Math.atan2(i - h.y, e - h.x), u = Dt(Math.atan2(l - h.y, a - h.x) - c + s);
  if (t.snapAngle && t.snapAngle > 0) {
    let g = t.snapAngle, p = t.snapThreshold || g, m = Math.ceil(u / g) * g, y = Math.floor(u / g) * g;
    Math.abs(u - y) < p ? u = y : Math.abs(u - m) < p && (u = m);
  }
  u < 0 && (u = 360 + u), u %= 360;
  let d = t.angle !== u;
  return t.angle = u, d;
}));
function Yo(r, t) {
  let e = t.canvas, i = r[e.uniScaleKey];
  return e.uniformScaling && !i || !e.uniformScaling && i;
}
function Wo(r, t, e) {
  let i = ft(r, "lockScalingX"), s = ft(r, "lockScalingY");
  if (i && s || !t && (i || s) && e || i && t === "x" || s && t === "y") return !0;
  let { width: o, height: n, strokeWidth: a } = r;
  return o === 0 && a === 0 && t !== "y" || n === 0 && a === 0 && t !== "x";
}
var Za = [
  "e",
  "se",
  "s",
  "sw",
  "w",
  "nw",
  "n",
  "ne",
  "e"
], le = (r, t, e, i) => {
  let s = Yo(r, e);
  return Wo(e, t.x !== 0 && t.y === 0 ? "x" : t.x === 0 && t.y !== 0 ? "y" : "", s) ? Qi : `${Za[bo(e, 0, i)]}-resize`;
};
function ns(r, t, e, i, s = {}) {
  let o = t.target, n = s.by, a = Yo(r, o), l, h, c, u, d, g;
  if (Wo(o, n, a)) return !1;
  if (t.gestureScale) h = t.scaleX * t.gestureScale, c = t.scaleY * t.gestureScale;
  else {
    if (l = Vr(t, t.originX, t.originY, e, i), d = n === "y" ? 1 : Math.sign(l.x || t.signX || 1), g = n === "x" ? 1 : Math.sign(l.y || t.signY || 1), t.signX || (t.signX = d), t.signY || (t.signY = g), ft(o, "lockScalingFlip") && (t.signX !== d || t.signY !== g)) return !1;
    if (u = o._getTransformedDimensions(), a && !n) {
      let y = Math.abs(l.x) + Math.abs(l.y), { original: x } = t, _ = y / (Math.abs(u.x * x.scaleX / o.scaleX) + Math.abs(u.y * x.scaleY / o.scaleY));
      h = x.scaleX * _, c = x.scaleY * _;
    } else h = Math.abs(l.x * o.scaleX / u.x), c = Math.abs(l.y * o.scaleY / u.y);
    Co(t) && (h *= 2, c *= 2), t.signX !== d && n !== "y" && (t.originX = Ss(t.originX), h *= -1, t.signX = d), t.signY !== g && n !== "x" && (t.originY = Ss(t.originY), c *= -1, t.signY = g);
  }
  let p = o.scaleX, m = o.scaleY;
  return n ? (n === "x" && o.set("scaleX", h), n === "y" && o.set("scaleY", c)) : (!ft(o, "lockScalingX") && o.set("scaleX", h), !ft(o, "lockScalingY") && o.set("scaleY", c)), p !== o.scaleX || m !== o.scaleY;
}
var Ee = jt(Rr, Ht((r, t, e, i) => ns(r, t, e, i))), Vo = jt(Rr, Ht((r, t, e, i) => ns(r, t, e, i, { by: "x" }))), Ho = jt(Rr, Ht((r, t, e, i) => ns(r, t, e, i, { by: "y" }))), ei = {
  x: {
    counterAxis: "y",
    scale: Wt,
    skew: Se,
    lockSkewing: "lockSkewingX",
    origin: "originX",
    flip: "flipX"
  },
  y: {
    counterAxis: "x",
    scale: Vt,
    skew: Ce,
    lockSkewing: "lockSkewingY",
    origin: "originY",
    flip: "flipY"
  }
}, tl = [
  "ns",
  "nesw",
  "ew",
  "nwse"
], zo = (r, t, e, i) => t.x !== 0 && ft(e, "lockSkewingY") || t.y !== 0 && ft(e, "lockSkewingX") ? Qi : `${tl[bo(e, 0, i) % 4]}-resize`;
function Go(r, t, e, i, s) {
  let { target: o } = e, { counterAxis: n, origin: a, lockSkewing: l, skew: h, flip: c } = ei[r];
  if (ft(o, l)) return !1;
  let { origin: u, flip: d } = ei[n], g = J(e[u]) * (o[d] ? -1 : 1), p = -Math.sign(g) * (o[c] ? -1 : 1), m = -(o[h] === 0 && Vr(e, "center", "center", i, s)[r] > 0 || o[h] > 0 ? 1 : -1) * p * 0.5 + 0.5;
  return jt(Qs, Ht((y, x, _, S) => (function(C, { target: b, ex: O, ey: T, skewingSide: k, ...D }, I) {
    let { skew: j } = ei[C], E = I.subtract(new v(O, T)).divide(new v(b.scaleX, b.scaleY))[C], R = b[j], X = D[j], z = Math.tan(B(X)), Y = C === "y" ? b._getTransformedDimensions({
      scaleX: 1,
      scaleY: 1,
      skewX: 0
    }).x : b._getTransformedDimensions({
      scaleX: 1,
      scaleY: 1
    }).y, q = 2 * E * k / Math.max(Y, 1) + z, rt = Dt(Math.atan(q));
    b.set(j, rt);
    let A = R !== b[j];
    if (A && C === "y") {
      let { skewX: yt, scaleX: we } = b, Te = b._getTransformedDimensions({ skewY: R }), Ft = b._getTransformedDimensions(), Oe = yt === 0 ? 1 : Te.x / Ft.x;
      Oe !== 1 && b.set("scaleX", Oe * we);
    }
    return A;
  })(r, x, new v(_, S))))(t, {
    ...e,
    [a]: m,
    skewingSide: p
  }, i, s);
}
var Uo = (r, t, e, i) => Go("x", r, t, e, i), No = (r, t, e, i) => Go("y", r, t, e, i);
function Ur(r, t) {
  return r[t.canvas.altActionKey];
}
var Pe = (r, t, e) => {
  let i = Ur(r, e);
  return t.x === 0 ? i ? Se : Vt : t.y === 0 ? i ? Ce : Wt : "";
}, Jt = (r, t, e, i) => Ur(r, e) ? zo(0, t, e, i) : le(r, t, e, i), di = (r, t, e, i) => Ur(r, t.target) ? No(r, t, e, i) : Vo(r, t, e, i), gi = (r, t, e, i) => Ur(r, t.target) ? Uo(r, t, e, i) : Ho(r, t, e, i), as = () => ({
  ml: new st({
    x: -0.5,
    y: 0,
    cursorStyleHandler: Jt,
    actionHandler: di,
    getActionName: Pe
  }),
  mr: new st({
    x: 0.5,
    y: 0,
    cursorStyleHandler: Jt,
    actionHandler: di,
    getActionName: Pe
  }),
  mb: new st({
    x: 0,
    y: 0.5,
    cursorStyleHandler: Jt,
    actionHandler: gi,
    getActionName: Pe
  }),
  mt: new st({
    x: 0,
    y: -0.5,
    cursorStyleHandler: Jt,
    actionHandler: gi,
    getActionName: Pe
  }),
  tl: new st({
    x: -0.5,
    y: -0.5,
    cursorStyleHandler: le,
    actionHandler: Ee
  }),
  tr: new st({
    x: 0.5,
    y: -0.5,
    cursorStyleHandler: le,
    actionHandler: Ee
  }),
  bl: new st({
    x: -0.5,
    y: 0.5,
    cursorStyleHandler: le,
    actionHandler: Ee
  }),
  br: new st({
    x: 0.5,
    y: 0.5,
    cursorStyleHandler: le,
    actionHandler: Ee
  }),
  mtr: new st({
    x: 0,
    y: -0.5,
    actionHandler: $o,
    cursorStyleHandler: Xo,
    offsetY: -40,
    withConnection: !0,
    actionName: Js
  })
}), qo = () => ({
  mr: new st({
    x: 0.5,
    y: 0,
    actionHandler: ui,
    cursorStyleHandler: Jt,
    actionName: Ze
  }),
  ml: new st({
    x: -0.5,
    y: 0,
    actionHandler: ui,
    cursorStyleHandler: Jt,
    actionName: Ze
  })
}), Ko = () => ({
  ...as(),
  ...qo()
}), Jo = class fi extends wt {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...fi.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, this.constructor.createControls(), fi.ownDefaults), this.setOptions(t);
  }
  static createControls() {
    return { controls: as() };
  }
  _updateCacheCanvas() {
    let t = this.canvas;
    if (this.noScaleCache && t && t._currentTransform) {
      let e = t._currentTransform, i = e.target, s = e.action;
      if (this === i && s && s.startsWith("scale")) return !1;
    }
    return super._updateCacheCanvas();
  }
  getActiveControl() {
    let t = this.__corner;
    return t ? {
      key: t,
      control: this.controls[t],
      coord: this.oCoords[t]
    } : void 0;
  }
  findControl(t, e = !1) {
    if (!this.hasControls || !this.canvas) return;
    this.__corner = void 0;
    let i = Object.entries(this.oCoords);
    for (let s = i.length - 1; s >= 0; s--) {
      let [o, n] = i[s], a = this.controls[o];
      if (a.shouldActivate(o, this, t, e ? n.touchCorner : n.corner)) return this.__corner = o, {
        key: o,
        control: a,
        coord: this.oCoords[o]
      };
    }
  }
  calcOCoords() {
    let t = this.getViewportTransform(), e = Vi(t), i = ao(t), s = this.getCenterPoint(), o = $($(t, $(be(s.x, s.y), ee({ angle: this.getTotalAngle() - (this.group && this.flipX ? 180 : 0) }))), [
      1 / e,
      0,
      0,
      1 / i,
      0,
      0
    ]), n = this.group ? pe(this.calcTransformMatrix()) : void 0;
    n && (n.scaleX = Math.abs(n.scaleX), n.scaleY = Math.abs(n.scaleY));
    let a = this._calculateCurrentDimensions(n), l = {};
    return this.forEachControl((h, c) => {
      let u = h.positionHandler(a, o, this, h);
      l[c] = Object.assign(u, this._calcCornerCoords(h, u));
    }), l;
  }
  _calcCornerCoords(t, e) {
    let i = this.getTotalAngle();
    return {
      corner: t.calcCornerCoords(i, this.cornerSize, e.x, e.y, !1, this),
      touchCorner: t.calcCornerCoords(i, this.touchCornerSize, e.x, e.y, !0, this)
    };
  }
  setCoords() {
    super.setCoords(), this.canvas && (this.oCoords = this.calcOCoords());
  }
  forEachControl(t) {
    for (let e in this.controls) t(this.controls[e], e, this);
  }
  drawSelectionBackground(t) {
    if (!this.selectionBackgroundColor || this.canvas && this.canvas._activeObject !== this) return;
    t.save();
    let e = this.getRelativeCenterPoint(), i = this._calculateCurrentDimensions(), s = this.getViewportTransform();
    t.translate(e.x, e.y), t.scale(1 / s[0], 1 / s[3]), t.rotate(B(this.angle)), t.fillStyle = this.selectionBackgroundColor, t.fillRect(-i.x / 2, -i.y / 2, i.x, i.y), t.restore();
  }
  strokeBorders(t, e) {
    t.strokeRect(-e.x / 2, -e.y / 2, e.x, e.y);
  }
  _drawBorders(t, e, i = {}) {
    let s = {
      hasControls: this.hasControls,
      borderColor: this.borderColor,
      borderDashArray: this.borderDashArray,
      ...i
    };
    t.save(), t.strokeStyle = s.borderColor, this._setLineDash(t, s.borderDashArray), this.strokeBorders(t, e), s.hasControls && this.drawControlsConnectingLines(t, e), t.restore();
  }
  _renderControls(t, e = {}) {
    let { hasBorders: i, hasControls: s } = this, o = {
      hasBorders: i,
      hasControls: s,
      ...e
    }, n = this.getViewportTransform(), a = o.hasBorders, l = o.hasControls, h = pe($(n, this.calcTransformMatrix()));
    t.save(), t.translate(h.translateX, h.translateY), t.lineWidth = this.borderScaleFactor, this.group === this.parent && (t.globalAlpha = this.isMoving ? this.borderOpacityWhenMoving : 1), this.flipX && (h.angle -= 180);
    let c = Wi(n);
    t.rotate(this.group ? B(h.angle) : B(this.angle) + c), a && this.drawBorders(t, h, e), l && this.drawControls(t, e), t.restore();
  }
  drawBorders(t, e, i) {
    let s;
    if (i && i.forActiveSelection || this.group) {
      let o = Yr(this.width, this.height, sr(e)), n = this.isStrokeAccountedForInDimensions() ? Xi : (this.strokeUniform ? new v().scalarAdd(this.canvas ? this.canvas.getZoom() : 1) : new v(e.scaleX, e.scaleY)).scalarMultiply(this.strokeWidth);
      s = o.add(n).scalarAdd(this.borderScaleFactor).scalarAdd(2 * this.padding);
    } else s = this._calculateCurrentDimensions().scalarAdd(this.borderScaleFactor);
    this._drawBorders(t, s, i);
  }
  drawControlsConnectingLines(t, e) {
    let i = !1;
    t.beginPath(), this.forEachControl((s, o) => {
      s.withConnection && s.getVisibility(this, o) && (i = !0, t.moveTo(s.x * e.x, s.y * e.y), t.lineTo(s.x * e.x + s.offsetX, s.y * e.y + s.offsetY));
    }), i && t.stroke();
  }
  drawControls(t, e = {}) {
    t.save();
    let i = this.getCanvasRetinaScaling(), { cornerStrokeColor: s, cornerDashArray: o, cornerColor: n } = this, a = {
      cornerStrokeColor: s,
      cornerDashArray: o,
      cornerColor: n,
      ...e
    };
    t.setTransform(i, 0, 0, i, 0, 0), t.strokeStyle = t.fillStyle = a.cornerColor, this.transparentCorners || (t.strokeStyle = a.cornerStrokeColor), this._setLineDash(t, a.cornerDashArray), this.forEachControl((l, h) => {
      if (l.getVisibility(this, h)) {
        let c = this.oCoords[h];
        l.render(t, c.x, c.y, a, this);
      }
    }), t.restore();
  }
  isControlVisible(t) {
    return this.controls[t] && this.controls[t].getVisibility(this, t);
  }
  setControlVisible(t, e) {
    this._controlsVisibility || (this._controlsVisibility = {}), this._controlsVisibility[t] = e;
  }
  setControlsVisibility(t = {}) {
    Object.entries(t).forEach(([e, i]) => this.setControlVisible(e, i));
  }
  clearContextTop(t) {
    if (!this.canvas) return;
    let e = this.canvas.contextTop;
    if (!e) return;
    let i = this.canvas.viewportTransform;
    e.save(), e.transform(i[0], i[1], i[2], i[3], i[4], i[5]), this.transform(e);
    let s = this.width + 4, o = this.height + 4;
    return e.clearRect(-s / 2, -o / 2, s, o), t || e.restore(), e;
  }
  onDeselect(t) {
    return !1;
  }
  onSelect(t) {
    return !1;
  }
  shouldStartDragging(t) {
    return !1;
  }
  onDragStart(t) {
    return !1;
  }
  canDrop(t) {
    return !1;
  }
  renderDragSourceEffect(t) {
  }
  renderDropTargetEffect(t) {
  }
};
function Qo(r, t) {
  return t.forEach((e) => {
    Object.getOwnPropertyNames(e.prototype).forEach((i) => {
      i !== "constructor" && Object.defineProperty(r.prototype, i, Object.getOwnPropertyDescriptor(e.prototype, i) || /* @__PURE__ */ Object.create(null));
    });
  }), r;
}
f(Jo, "ownDefaults", {
  noScaleCache: !0,
  lockMovementX: !1,
  lockMovementY: !1,
  lockRotation: !1,
  lockScalingX: !1,
  lockScalingY: !1,
  lockSkewingX: !1,
  lockSkewingY: !1,
  lockScalingFlip: !1,
  cornerSize: 13,
  touchCornerSize: 24,
  transparentCorners: !0,
  cornerColor: "rgb(178,204,255)",
  cornerStrokeColor: "",
  cornerStyle: "rect",
  cornerDashArray: null,
  hasControls: !0,
  borderColor: "rgb(178,204,255)",
  borderDashArray: null,
  borderOpacityWhenMoving: 0.4,
  borderScaleFactor: 1,
  hasBorders: !0,
  selectionBackgroundColor: "",
  selectable: !0,
  evented: !0,
  perPixelTargetFind: !1,
  activeOn: "down",
  hoverCursor: null,
  moveCursor: null
});
var N = class extends Jo {
};
Qo(N, [To]), w.setClass(N), w.setClass(N, "object");
var Zo = (r, t, e, i) => {
  let s = 2 * (i = Math.round(i)) + 1, { data: o } = r.getImageData(t - i, e - i, s, s);
  for (let n = 3; n < o.length; n += 4) if (o[n] > 0) return !1;
  return !0;
}, tn = class {
  constructor(r) {
    this.options = r, this.strokeProjectionMagnitude = this.options.strokeWidth / 2, this.scale = new v(this.options.scaleX, this.options.scaleY), this.strokeUniformScalar = this.options.strokeUniform ? new v(1 / this.options.scaleX, 1 / this.options.scaleY) : new v(1, 1);
  }
  createSideVector(r, t) {
    let e = tr(r, t);
    return this.options.strokeUniform ? e.multiply(this.scale) : e;
  }
  projectOrthogonally(r, t, e) {
    return this.applySkew(r.add(this.calcOrthogonalProjection(r, t, e)));
  }
  isSkewed() {
    return this.options.skewX !== 0 || this.options.skewY !== 0;
  }
  applySkew(r) {
    let t = new v(r);
    return t.y += t.x * Math.tan(B(this.options.skewY)), t.x += t.y * Math.tan(B(this.options.skewX)), t;
  }
  scaleUnitVector(r, t) {
    return r.multiply(this.strokeUniformScalar).scalarMultiply(t);
  }
}, el = new v(), en = class Or extends tn {
  static getOrthogonalRotationFactor(t, e) {
    let i = e ? jr(t, e) : Ki(t);
    return Math.abs(i) < Yt ? -1 : 1;
  }
  constructor(t, e, i, s) {
    super(s), f(this, "AB", void 0), f(this, "AC", void 0), f(this, "alpha", void 0), f(this, "bisector", void 0), this.A = new v(t), this.B = new v(e), this.C = new v(i), this.AB = this.createSideVector(this.A, this.B), this.AC = this.createSideVector(this.A, this.C), this.alpha = jr(this.AB, this.AC), this.bisector = Wr(qi(this.AB.eq(el) ? this.AC : this.AB, this.alpha / 2));
  }
  calcOrthogonalProjection(t, e, i = this.strokeProjectionMagnitude) {
    let s = Ji(this.createSideVector(t, e)), o = Or.getOrthogonalRotationFactor(s, this.bisector);
    return this.scaleUnitVector(s, i * o);
  }
  projectBevel() {
    let t = [];
    return (this.alpha % pt === 0 ? [this.B] : [this.B, this.C]).forEach((e) => {
      t.push(this.projectOrthogonally(this.A, e)), t.push(this.projectOrthogonally(this.A, e, -this.strokeProjectionMagnitude));
    }), t;
  }
  projectMiter() {
    let t = [], e = Math.abs(this.alpha), i = 1 / Math.sin(e / 2), s = this.scaleUnitVector(this.bisector, -this.strokeProjectionMagnitude * i), o = this.options.strokeUniform ? Pr(this.scaleUnitVector(this.bisector, this.options.strokeMiterLimit)) : this.options.strokeMiterLimit;
    return Pr(s) / this.strokeProjectionMagnitude <= o && t.push(this.applySkew(this.A.add(s))), t.push(...this.projectBevel()), t;
  }
  projectRoundNoSkew(t, e) {
    let i = [], s = new v(Or.getOrthogonalRotationFactor(this.bisector), Or.getOrthogonalRotationFactor(new v(this.bisector.y, this.bisector.x)));
    return [new v(1, 0).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar).multiply(s), new v(0, 1).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar).multiply(s)].forEach((o) => {
      ci(o, t, e) && i.push(this.A.add(o));
    }), i;
  }
  projectRoundWithSkew(t, e) {
    let i = [], { skewX: s, skewY: o, scaleX: n, scaleY: a, strokeUniform: l } = this.options, h = new v(Math.tan(B(s)), Math.tan(B(o))), c = this.strokeProjectionMagnitude, u = l ? c / a / Math.sqrt(1 / a ** 2 + 1 / n ** 2 * h.y ** 2) : c / Math.sqrt(1 + h.y ** 2), d = new v(Math.sqrt(Math.max(c ** 2 - u ** 2, 0)), u), g = l ? c / Math.sqrt(1 + h.x ** 2 * (1 / a) ** 2 / (1 / n + 1 / n * h.x * h.y) ** 2) : c / Math.sqrt(1 + h.x ** 2 / (1 + h.x * h.y) ** 2), p = new v(g, Math.sqrt(Math.max(c ** 2 - g ** 2, 0)));
    return [
      p,
      p.scalarMultiply(-1),
      d,
      d.scalarMultiply(-1)
    ].map((m) => this.applySkew(l ? m.multiply(this.strokeUniformScalar) : m)).forEach((m) => {
      ci(m, t, e) && i.push(this.applySkew(this.A).add(m));
    }), i;
  }
  projectRound() {
    let t = [];
    t.push(...this.projectBevel());
    let e = this.alpha % pt === 0, i = this.applySkew(this.A), s = t[e ? 0 : 2].subtract(i), o = t[+!!e].subtract(i), n = ue(s, e ? this.applySkew(this.AB.scalarMultiply(-1)) : this.applySkew(this.bisector.multiply(this.strokeUniformScalar).scalarMultiply(-1))) > 0, a = n ? s : o, l = n ? o : s;
    return this.isSkewed() ? t.push(...this.projectRoundWithSkew(a, l)) : t.push(...this.projectRoundNoSkew(a, l)), t;
  }
  projectPoints() {
    switch (this.options.strokeLineJoin) {
      case "miter":
        return this.projectMiter();
      case "round":
        return this.projectRound();
      default:
        return this.projectBevel();
    }
  }
  project() {
    return this.projectPoints().map((t) => ({
      originPoint: this.A,
      projectedPoint: t,
      angle: this.alpha,
      bisector: this.bisector
    }));
  }
}, Ps = class extends tn {
  constructor(r, t, e) {
    super(e), this.A = new v(r), this.T = new v(t);
  }
  calcOrthogonalProjection(r, t, e = this.strokeProjectionMagnitude) {
    let i = this.createSideVector(r, t);
    return this.scaleUnitVector(Ji(i), e);
  }
  projectButt() {
    return [this.projectOrthogonally(this.A, this.T, this.strokeProjectionMagnitude), this.projectOrthogonally(this.A, this.T, -this.strokeProjectionMagnitude)];
  }
  projectRound() {
    let r = [];
    if (!this.isSkewed() && this.A.eq(this.T)) {
      let t = new v(1, 1).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar);
      r.push(this.applySkew(this.A.add(t)), this.applySkew(this.A.subtract(t)));
    } else r.push(...new en(this.A, this.T, this.T, this.options).projectRound());
    return r;
  }
  projectSquare() {
    let r = [];
    if (this.A.eq(this.T)) {
      let t = new v(1, 1).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar);
      r.push(this.A.add(t), this.A.subtract(t));
    } else {
      let t = this.calcOrthogonalProjection(this.A, this.T, this.strokeProjectionMagnitude), e = this.scaleUnitVector(Wr(this.createSideVector(this.A, this.T)), -this.strokeProjectionMagnitude), i = this.A.add(e);
      r.push(i.add(t), i.subtract(t));
    }
    return r.map((t) => this.applySkew(t));
  }
  projectPoints() {
    switch (this.options.strokeLineCap) {
      case "round":
        return this.projectRound();
      case "square":
        return this.projectSquare();
      default:
        return this.projectButt();
    }
  }
  project() {
    return this.projectPoints().map((r) => ({
      originPoint: this.A,
      projectedPoint: r
    }));
  }
}, rn = (r, t, e = !1) => {
  let i = [];
  if (r.length === 0) return i;
  let s = r.reduce((o, n) => (o[o.length - 1].eq(n) || o.push(new v(n)), o), [new v(r[0])]);
  if (s.length === 1) e = !0;
  else if (!e) {
    let o = s[0], n = ((a, l) => {
      for (let h = a.length - 1; h >= 0; h--) if (l(a[h], h, a)) return h;
      return -1;
    })(s, (a) => !a.eq(o));
    s.splice(n + 1);
  }
  return s.forEach((o, n, a) => {
    let l, h;
    n === 0 ? (h = a[1], l = e ? o : a[a.length - 1]) : n === a.length - 1 ? (l = a[n - 1], h = e ? o : a[0]) : (l = a[n - 1], h = a[n + 1]), e && a.length === 1 ? i.push(...new Ps(o, o, t).project()) : !e || n !== 0 && n !== a.length - 1 ? i.push(...new en(o, l, h, t).project()) : i.push(...new Ps(o, n === 0 ? h : l, t).project());
  }), i;
}, ls = (r) => {
  let t = {};
  return Object.keys(r).forEach((e) => {
    t[e] = {}, Object.keys(r[e]).forEach((i) => {
      t[e][i] = { ...r[e][i] };
    });
  }), t;
}, Nr = (r, t, e = !1) => r.fill !== t.fill || r.stroke !== t.stroke || r.strokeWidth !== t.strokeWidth || r.fontSize !== t.fontSize || r.fontFamily !== t.fontFamily || r.fontWeight !== t.fontWeight || r.fontStyle !== t.fontStyle || r.textDecorationThickness !== t.textDecorationThickness || r.textDecorationColor !== t.textDecorationColor || r.textBackgroundColor !== t.textBackgroundColor || r.deltaY !== t.deltaY || e && (r.overline !== t.overline || r.underline !== t.underline || r.linethrough !== t.linethrough), sn = (r, t) => {
  let e = t.split(`
`), i = [], s = -1, o = {};
  r = ls(r);
  for (let n = 0; n < e.length; n++) {
    let a = Xr(e[n]);
    if (r[n]) for (let l = 0; l < a.length; l++) {
      s++;
      let h = r[n][l];
      h && Object.keys(h).length > 0 && (Nr(o, h, !0) ? i.push({
        start: s,
        end: s + 1,
        style: h
      }) : i[i.length - 1].end++), o = h || {};
    }
    else s += a.length, o = {};
  }
  return i;
}, on = (r, t) => {
  if (!Array.isArray(r)) return ls(r);
  let e = t.split(Bi), i = {}, s = -1, o = 0;
  for (let n = 0; n < e.length; n++) {
    let a = Xr(e[n]);
    for (let l = 0; l < a.length; l++) s++, r[o] && r[o].start <= s && s < r[o].end && (i[n] = i[n] || {}, i[n][l] = { ...r[o].style }, s === r[o].end - 1 && o++);
  }
  return i;
}, zt = [
  "display",
  "transform",
  tt,
  "fill-opacity",
  "fill-rule",
  "opacity",
  Mt,
  "stroke-dasharray",
  "stroke-linecap",
  "stroke-dashoffset",
  "stroke-linejoin",
  "stroke-miterlimit",
  "stroke-opacity",
  "stroke-width",
  "id",
  "paint-order",
  "vector-effect",
  "instantiated_by_use",
  "clip-path"
];
function js(r, t) {
  let e = r.nodeName, i = r.getAttribute("class"), s = r.getAttribute("id"), o = "(?![a-zA-Z\\-]+)", n;
  if (n = RegExp("^" + e, "i"), t = t.replace(n, ""), s && t.length && (n = RegExp("#" + s + o, "i"), t = t.replace(n, "")), i && t.length) {
    let a = i.split(" ");
    for (let l = a.length; l--; ) n = RegExp("\\." + a[l] + o, "i"), t = t.replace(n, "");
  }
  return t.length === 0;
}
function rl(r, t) {
  let e = !0, i = js(r, t.pop());
  return i && t.length && (e = (function(s, o) {
    let n, a = !0;
    for (; s.parentElement && s.parentElement.nodeType === 1 && o.length; ) a && (n = o.pop()), a = js(s = s.parentElement, n);
    return o.length === 0;
  })(r, t)), i && e && t.length === 0;
}
function il(r, t = {}) {
  let e = {};
  for (let i in t) rl(r, i.split(" ")) && (e = {
    ...e,
    ...t[i]
  });
  return e;
}
var sl = (r) => {
  var t;
  return (t = fa[r]) == null ? r : t;
}, ol = RegExp(`(${dt})`, "gi"), Q = `(${dt})`, nl = String.raw`(skewX)\(${Q}\)`, al = String.raw`(skewY)\(${Q}\)`, ll = String.raw`(rotate)\(${Q}(?: ${Q} ${Q})?\)`, hl = String.raw`(scale)\(${Q}(?: ${Q})?\)`, cl = String.raw`(translate)\(${Q}(?: ${Q})?\)`, hs = `(?:${String.raw`(matrix)\(${Q} ${Q} ${Q} ${Q} ${Q} ${Q}\)`}|${cl}|${ll}|${hl}|${nl}|${al})`, ul = `(?:${hs}*)`, dl = String.raw`^\s*(?:${ul}?)\s*$`, gl = new RegExp(dl), fl = new RegExp(hs), pl = new RegExp(hs, "g");
function pi(r) {
  let t = [];
  if (!(r = ((e) => Ar(e.replace(ol, " $1 ").replace(/,/gi, " ")))(r).replace(/\s*([()])\s*/gi, "$1")) || r && !gl.test(r)) return [...Z];
  for (let e of r.matchAll(pl)) {
    let i = fl.exec(e[0]);
    if (!i) continue;
    let s = Z, [, o, ...n] = i.filter((g) => !!g), [a, l, h, c, u, d] = n.map((g) => parseFloat(g));
    switch (o) {
      case "translate":
        s = be(a, l);
        break;
      case Js:
        s = ee({ angle: a }, {
          x: l,
          y: h
        });
        break;
      case to:
        s = Br(a, l);
        break;
      case Se:
        s = Hi(a);
        break;
      case Ce:
        s = zi(a);
        break;
      case "matrix":
        s = [
          a,
          l,
          h,
          c,
          u,
          d
        ];
    }
    t.push(s);
  }
  return Ir(t);
}
function ml(r, t, e, i) {
  let s = Array.isArray(t), o, n = t;
  if (r !== "fill" && r !== "stroke" || t !== "none") {
    if (r === "strokeUniform") return t === "non-scaling-stroke";
    if (r === "strokeDashArray") n = t === "none" ? null : t.replace(/,/g, " ").split(/\s+/).map(parseFloat);
    else if (r === "transformMatrix") n = e && e.transformMatrix ? $(e.transformMatrix, pi(t)) : pi(t);
    else if (r === "visible") n = t !== "none" && t !== "hidden", e && e.visible === !1 && (n = !1);
    else if (r === "opacity") n = parseFloat(t), e && e.opacity !== void 0 && (n *= e.opacity);
    else if (r === "textAnchor") n = t === "start" ? V : t === "end" ? gt : L;
    else if (r === "charSpacing" || r === "textDecorationThickness") o = Zt(t, i) / i * 1e3;
    else if (r === "paintFirst") {
      let a = t.indexOf(tt), l = t.indexOf(Mt);
      n = tt, (a > -1 && l > -1 && l < a || a === -1 && l > -1) && (n = Mt);
    } else {
      if (r === "href" || r === "xlink:href" || r === "font" || r === "id") return t;
      if (r === "imageSmoothing") return t === "optimizeQuality";
      o = s ? t.map(Zt) : Zt(t, i);
    }
  } else n = "";
  return !s && isNaN(o) ? n : o;
}
function vl(r, t) {
  r.replace(/;\s*$/, "").split(";").forEach((e) => {
    if (!e) return;
    let [i, s] = e.split(":");
    t[i.trim().toLowerCase()] = s.trim();
  });
}
function yl(r) {
  let t = {}, e = r.getAttribute("style");
  return e && (typeof e == "string" ? vl(e, t) : (function(i, s) {
    Object.entries(i).forEach(([o, n]) => {
      n !== void 0 && (s[o.toLowerCase()] = n);
    });
  })(e, t)), t;
}
var xl = {
  stroke: "strokeOpacity",
  fill: "fillOpacity"
};
function At(r, t, e) {
  if (!r) return {};
  let i, s = {}, o = 16;
  r.parentNode && Ms.test(r.parentNode.nodeName) && (s = At(r.parentElement, t, e), s.fontSize && (i = o = Zt(s.fontSize)));
  let n = {
    ...t.reduce((h, c) => {
      let u = r.getAttribute(c);
      return u && (h[c] = u), h;
    }, {}),
    ...il(r, e),
    ...yl(r)
  };
  n["clip-path"] && r.setAttribute(ks, n[ks]), n["font-size"] && (i = Zt(n[Os], o), n[Os] = `${i}`);
  let a = {};
  for (let h in n) {
    let c = sl(h);
    a[c] = ml(c, n[h], s, i);
  }
  a && a.font && (function(h, c) {
    let u = h.match(ga);
    if (!u) return;
    let d = u[1], g = u[3], p = u[4], m = u[5], y = u[6];
    d && (c.fontStyle = d), g && (c.fontWeight = isNaN(parseFloat(g)) ? g : parseFloat(g)), p && (c.fontSize = Zt(p)), y && (c.fontFamily = y), m && (c.lineHeight = m === "normal" ? 1 : m);
  })(a.font, a);
  let l = {
    ...s,
    ...a
  };
  return Ms.test(r.nodeName) ? l : (function(h) {
    let c = N.getDefaults();
    return Object.entries(xl).forEach(([u, d]) => {
      if (h[d] === void 0 || h[u] === "") return;
      if (h[u] === void 0) {
        if (!c[u]) return;
        h[u] = c[u];
      }
      if (h[u].indexOf("url(") === 0) return;
      let g = new et(h[u]);
      h[u] = g.setAlpha(F(g.getAlpha() * h[d], 2)).toRgba();
    }), h;
  })(l);
}
var nn = ["rx", "ry"], Tt = class mi extends N {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...mi.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, mi.ownDefaults), this.setOptions(t), this._initRxRy();
  }
  _initRxRy() {
    let { rx: t, ry: e } = this;
    t && !e ? this.ry = t : e && !t && (this.rx = e);
  }
  _render(t) {
    let { width: e, height: i } = this, s = -e / 2, o = -i / 2, n = this.rx ? Math.min(this.rx, e / 2) : 0, a = this.ry ? Math.min(this.ry, i / 2) : 0, l = n !== 0 || a !== 0;
    t.beginPath(), t.moveTo(s + n, o), t.lineTo(s + e - n, o), l && t.bezierCurveTo(s + e - 0.4477152502 * n, o, s + e, o + 0.4477152502 * a, s + e, o + a), t.lineTo(s + e, o + i - a), l && t.bezierCurveTo(s + e, o + i - 0.4477152502 * a, s + e - 0.4477152502 * n, o + i, s + e - n, o + i), t.lineTo(s + n, o + i), l && t.bezierCurveTo(s + 0.4477152502 * n, o + i, s, o + i - 0.4477152502 * a, s, o + i - a), t.lineTo(s, o + a), l && t.bezierCurveTo(s, o + 0.4477152502 * a, s + 0.4477152502 * n, o, s + n, o), t.closePath(), this._renderPaintInOrder(t);
  }
  toObject(t = []) {
    return super.toObject([...nn, ...t]);
  }
  _toSVG() {
    let { width: t, height: e, rx: i, ry: s } = this;
    return [
      "<rect ",
      "COMMON_PARTS",
      `x="${-t / 2}" y="${-e / 2}" rx="${M(i)}" ry="${M(s)}" width="${M(t)}" height="${M(e)}" />
`
    ];
  }
  static async fromElement(t, e, i) {
    let { left: s = 0, top: o = 0, width: n = 0, height: a = 0, visible: l = !0, ...h } = At(t, this.ATTRIBUTE_NAMES, i);
    return new this({
      ...e,
      ...h,
      left: s,
      top: o,
      width: n,
      height: a,
      visible: !!(l && n && a)
    });
  }
};
f(Tt, "type", "Rect"), f(Tt, "cacheProperties", [...Pt, ...nn]), f(Tt, "ownDefaults", {
  rx: 0,
  ry: 0
}), f(Tt, "ATTRIBUTE_NAMES", [
  ...zt,
  "x",
  "y",
  "rx",
  "ry",
  "width",
  "height"
]), w.setClass(Tt), w.setSVGClass(Tt);
var As = "initialization", vi = "added", an = (r, t) => {
  let { strokeUniform: e, strokeWidth: i, width: s, height: o, group: n } = t, a = n && n !== r ? nr(n.calcTransformMatrix(), r.calcTransformMatrix()) : null, l = a ? t.getRelativeCenterPoint().transform(a) : t.getRelativeCenterPoint(), h = !t.isStrokeAccountedForInDimensions(), c = e && h ? xo(new v(i, i), void 0, r.calcTransformMatrix()) : Xi, u = !e && h ? i : 0, d = Yr(s + u, o + u, Ir([a, t.calcOwnMatrix()], !0)).add(c).scalarDivide(2);
  return [l.subtract(d), l.add(d)];
}, qr = class {
  calcLayoutResult(r, t) {
    if (this.shouldPerformLayout(r)) return this.calcBoundingBox(t, r);
  }
  shouldPerformLayout({ type: r, prevStrategy: t, strategy: e }) {
    return r === "initialization" || r === "imperative" || !!t && e !== t;
  }
  shouldLayoutClipPath({ type: r, target: { clipPath: t } }) {
    return r !== "initialization" && t && !t.absolutePositioned;
  }
  getInitialSize(r, t) {
    return t.size;
  }
  calcBoundingBox(r, t) {
    let { type: e, target: i } = t;
    if (e === "imperative" && t.overrides) return t.overrides;
    if (r.length === 0) return;
    let { left: s, top: o, width: n, height: a } = St(r.map((c) => an(i, c)).reduce((c, u) => c.concat(u), [])), l = new v(n, a), h = new v(s, o).add(l.scalarDivide(2));
    if (e === "initialization") {
      let c = this.getInitialSize(t, {
        size: l,
        center: h
      });
      return {
        center: h,
        relativeCorrection: new v(0, 0),
        size: c
      };
    }
    return {
      center: h.transform(i.calcOwnMatrix()),
      size: l
    };
  }
};
f(qr, "type", "strategy");
var yi = class extends qr {
  shouldPerformLayout(r) {
    return !0;
  }
};
f(yi, "type", "fit-content"), w.setClass(yi);
var ln = "layoutManager", rr = class {
  constructor(r = new yi()) {
    f(this, "strategy", void 0), this.strategy = r, this._subscriptions = /* @__PURE__ */ new Map();
  }
  performLayout(r) {
    let t = {
      bubbles: !0,
      strategy: this.strategy,
      ...r,
      prevStrategy: this._prevLayoutStrategy,
      stopPropagation() {
        this.bubbles = !1;
      }
    };
    this.onBeforeLayout(t);
    let e = this.getLayoutResult(t);
    e && this.commitLayout(t, e), this.onAfterLayout(t, e), this._prevLayoutStrategy = t.strategy;
  }
  attachHandlers(r, t) {
    let { target: e } = t;
    return [
      eo,
      qs,
      Ze,
      Ks,
      Rr,
      Qs,
      Mr,
      Zs,
      "modifyPath"
    ].map((i) => r.on(i, (s) => this.performLayout(i === "modified" ? {
      type: "object_modified",
      trigger: i,
      e: s,
      target: e
    } : {
      type: "object_modifying",
      trigger: i,
      e: s,
      target: e
    })));
  }
  subscribe(r, t) {
    this.unsubscribe(r, t);
    let e = this.attachHandlers(r, t);
    this._subscriptions.set(r, e);
  }
  unsubscribe(r, t) {
    (this._subscriptions.get(r) || []).forEach((e) => e()), this._subscriptions.delete(r);
  }
  unsubscribeTargets(r) {
    r.targets.forEach((t) => this.unsubscribe(t, r));
  }
  subscribeTargets(r) {
    r.targets.forEach((t) => this.subscribe(t, r));
  }
  onBeforeLayout(r) {
    let { target: t, type: e } = r, { canvas: i } = t;
    if (e === "initialization" || e === "added" ? this.subscribeTargets(r) : e === "removed" && this.unsubscribeTargets(r), t.fire("layout:before", { context: r }), i && i.fire("object:layout:before", {
      target: t,
      context: r
    }), e === "imperative" && r.deep) {
      let { strategy: s, ...o } = r;
      t.forEachObject((n) => n.layoutManager && n.layoutManager.performLayout({
        ...o,
        bubbles: !1,
        target: n
      }));
    }
  }
  getLayoutResult(r) {
    let { target: t, strategy: e, type: i } = r, s = e.calcLayoutResult(r, t.getObjects());
    if (!s) return;
    let o = i === "initialization" ? new v() : t.getRelativeCenterPoint(), { center: n, correction: a = new v(), relativeCorrection: l = new v() } = s;
    return {
      result: s,
      prevCenter: o,
      nextCenter: n,
      offset: o.subtract(n).add(a).transform(i === "initialization" ? Z : ot(t.calcOwnMatrix()), !0).add(l)
    };
  }
  commitLayout(r, t) {
    let { target: e } = r, { result: { size: i }, nextCenter: s } = t;
    var o, n;
    e.set({
      width: i.x,
      height: i.y
    }), this.layoutObjects(r, t), r.type === "initialization" ? e.set({
      left: (o = r.x) == null ? s.x + i.x * J(e.originX) : o,
      top: (n = r.y) == null ? s.y + i.y * J(e.originY) : n
    }) : (e.setPositionByOrigin(s, L, L), e.setCoords(), e.set("dirty", !0));
  }
  layoutObjects(r, t) {
    let { target: e } = r;
    e.forEachObject((i) => {
      i.group === e && this.layoutObject(r, t, i);
    }), r.strategy.shouldLayoutClipPath(r) && this.layoutObject(r, t, e.clipPath);
  }
  layoutObject(r, { offset: t }, e) {
    e.set({
      left: e.left + t.x,
      top: e.top + t.y
    });
  }
  onAfterLayout(r, t) {
    let { target: e, strategy: i, bubbles: s, prevStrategy: o, ...n } = r, { canvas: a } = e;
    e.fire("layout:after", {
      context: r,
      result: t
    }), a && a.fire("object:layout:after", {
      context: r,
      result: t,
      target: e
    });
    let l = e.parent;
    s && l != null && l.layoutManager && ((n.path || (n.path = [])).push(e), l.layoutManager.performLayout({
      ...n,
      target: l
    })), e.set("dirty", !0);
  }
  dispose() {
    let { _subscriptions: r } = this;
    r.forEach((t) => t.forEach((e) => e())), r.clear();
  }
  toObject() {
    return {
      type: ln,
      strategy: this.strategy.constructor.type
    };
  }
  toJSON() {
    return this.toObject();
  }
};
w.setClass(rr, ln);
var _l = class extends rr {
  performLayout() {
  }
}, ge = class xi extends ro(N) {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...xi.ownDefaults
    };
  }
  constructor(t = [], e = {}) {
    super(), f(this, "_activeObjects", []), f(this, "__objectSelectionTracker", void 0), f(this, "__objectSelectionDisposer", void 0), Object.assign(this, xi.ownDefaults), this.setOptions(e), this.groupInit(t, e);
  }
  groupInit(t, e) {
    var i;
    this._objects = [...t], this.__objectSelectionTracker = this.__objectSelectionMonitor.bind(this, !0), this.__objectSelectionDisposer = this.__objectSelectionMonitor.bind(this, !1), this.forEachObject((s) => {
      this.enterGroup(s, !1);
    }), this.layoutManager = (i = e.layoutManager) == null ? new rr() : i, this.layoutManager.performLayout({
      type: As,
      target: this,
      targets: [...t],
      x: e.left,
      y: e.top
    });
  }
  canEnterGroup(t) {
    return t === this || this.isDescendantOf(t) ? (Xt("error", "Group: circular object trees are not supported, this call has no effect"), !1) : this._objects.indexOf(t) === -1 || (Xt("error", "Group: duplicate objects are not supported inside group, this call has no effect"), !1);
  }
  _filterObjectsBeforeEnteringGroup(t) {
    return t.filter((e, i, s) => this.canEnterGroup(e) && s.indexOf(e) === i);
  }
  add(...t) {
    let e = this._filterObjectsBeforeEnteringGroup(t), i = super.add(...e);
    return this._onAfterObjectsChange(vi, e), i;
  }
  insertAt(t, ...e) {
    let i = this._filterObjectsBeforeEnteringGroup(e), s = super.insertAt(t, ...i);
    return this._onAfterObjectsChange(vi, i), s;
  }
  remove(...t) {
    let e = super.remove(...t);
    return this._onAfterObjectsChange("removed", e), e;
  }
  _onObjectAdded(t) {
    this.enterGroup(t, !0), this.fire("object:added", { target: t }), t.fire("added", { target: this });
  }
  _onObjectRemoved(t, e) {
    this.exitGroup(t, e), this.fire("object:removed", { target: t }), t.fire("removed", { target: this });
  }
  _onAfterObjectsChange(t, e) {
    this.layoutManager.performLayout({
      type: t,
      targets: e,
      target: this
    });
  }
  _onStackOrderChanged() {
    this._set("dirty", !0);
  }
  _set(t, e) {
    let i = this[t];
    return super._set(t, e), t === "canvas" && i !== e && (this._objects || []).forEach((s) => {
      s._set(t, e);
    }), this;
  }
  _shouldSetNestedCoords() {
    return this.subTargetCheck;
  }
  removeAll() {
    return this._activeObjects = [], this.remove(...this._objects);
  }
  __objectSelectionMonitor(t, { target: e }) {
    let i = this._activeObjects;
    if (t) i.push(e), this._set("dirty", !0);
    else if (i.length > 0) {
      let s = i.indexOf(e);
      s > -1 && (i.splice(s, 1), this._set("dirty", !0));
    }
  }
  _watchObject(t, e) {
    t && this._watchObject(!1, e), t ? (e.on("selected", this.__objectSelectionTracker), e.on("deselected", this.__objectSelectionDisposer)) : (e.off("selected", this.__objectSelectionTracker), e.off("deselected", this.__objectSelectionDisposer));
  }
  enterGroup(t, e) {
    t.group && t.group.remove(t), t._set("parent", this), this._enterGroup(t, e);
  }
  _enterGroup(t, e) {
    e && ye(t, $(ot(this.calcTransformMatrix()), t.calcTransformMatrix())), this._shouldSetNestedCoords() && t.setCoords(), t._set("group", this), t._set("canvas", this.canvas), this._watchObject(!0, t);
    let i = this.canvas && this.canvas.getActiveObject && this.canvas.getActiveObject();
    i && (i === t || t.isDescendantOf(i)) && this._activeObjects.push(t);
  }
  exitGroup(t, e) {
    this._exitGroup(t, e), t._set("parent", void 0), t._set("canvas", void 0);
  }
  _exitGroup(t, e) {
    t._set("group", void 0), e || (ye(t, $(this.calcTransformMatrix(), t.calcTransformMatrix())), t.setCoords()), this._watchObject(!1, t);
    let i = this._activeObjects.length > 0 ? this._activeObjects.indexOf(t) : -1;
    i > -1 && this._activeObjects.splice(i, 1);
  }
  shouldCache() {
    let t = N.prototype.shouldCache.call(this);
    if (t) {
      for (let e = 0; e < this._objects.length; e++) if (this._objects[e].willDrawShadow()) return this.ownCaching = !1, !1;
    }
    return t;
  }
  willDrawShadow() {
    if (super.willDrawShadow()) return !0;
    for (let t = 0; t < this._objects.length; t++) if (this._objects[t].willDrawShadow()) return !0;
    return !1;
  }
  isOnACache() {
    return this.ownCaching || !!this.parent && this.parent.isOnACache();
  }
  drawObject(t, e, i) {
    this._renderBackground(t);
    for (let o = 0; o < this._objects.length; o++) {
      var s;
      let n = this._objects[o];
      (s = this.canvas) != null && s.preserveObjectStacking && n.group !== this ? (t.save(), t.transform(...ot(this.calcTransformMatrix())), n.render(t), t.restore()) : n.group === this && n.render(t);
    }
    this._drawClipPath(t, this.clipPath, i);
  }
  setCoords() {
    super.setCoords(), this._shouldSetNestedCoords() && this.forEachObject((t) => t.setCoords());
  }
  triggerLayout(t = {}) {
    this.layoutManager.performLayout({
      target: this,
      type: "imperative",
      ...t
    });
  }
  render(t) {
    this._transformDone = !0, super.render(t), this._transformDone = !1;
  }
  __serializeObjects(t, e) {
    let i = this.includeDefaultValues;
    return this._objects.filter(function(s) {
      return !s.excludeFromExport;
    }).map(function(s) {
      let o = s.includeDefaultValues;
      s.includeDefaultValues = i;
      let n = s[t || "toObject"](e);
      return s.includeDefaultValues = o, n;
    });
  }
  toObject(t = []) {
    let e = this.layoutManager.toObject();
    return {
      ...super.toObject([
        "subTargetCheck",
        "interactive",
        ...t
      ]),
      ...e.strategy !== "fit-content" || this.includeDefaultValues ? { layoutManager: e } : {},
      objects: this.__serializeObjects("toObject", t)
    };
  }
  toString() {
    return `#<Group: (${this.complexity()})>`;
  }
  dispose() {
    this.layoutManager.unsubscribeTargets({
      targets: this.getObjects(),
      target: this
    }), this._activeObjects = [], this.forEachObject((t) => {
      this._watchObject(!1, t), t.dispose();
    }), super.dispose();
  }
  _createSVGBgRect(t) {
    if (!this.backgroundColor) return "";
    let e = Tt.prototype._toSVG.call(this), i = e.indexOf("COMMON_PARTS");
    e[i] = 'for="group" ';
    let s = e.join("");
    return t ? t(s) : s;
  }
  _toSVG(t) {
    let e = [
      "<g ",
      "COMMON_PARTS",
      ` >
`
    ], i = this._createSVGBgRect(t);
    i && e.push("		", i);
    for (let s = 0; s < this._objects.length; s++) e.push("		", this._objects[s].toSVG(t));
    return e.push(`</g>
`), e;
  }
  getSvgStyles() {
    let t = this.opacity !== void 0 && this.opacity !== 1 ? `opacity: ${M(this.opacity)};` : "", e = this.visible ? "" : " visibility: hidden;";
    return [
      t,
      this.getSvgFilter(),
      e
    ].join("");
  }
  toClipPathSVG(t) {
    let e = [], i = this._createSVGBgRect(t);
    i && e.push("	", i);
    for (let s = 0; s < this._objects.length; s++) e.push("	", this._objects[s].toClipPathSVG(t));
    return this._createBaseClipPathSVGMarkup(e, { reviver: t });
  }
  static fromObject({ type: t, objects: e = [], layoutManager: i, ...s }, o) {
    return Promise.all([me(e, o), or(s, o)]).then(([n, a]) => {
      let l = new this(n, {
        ...s,
        ...a,
        layoutManager: new _l()
      });
      return l.layoutManager = i ? new (w.getClass(i.type))(new (w.getClass(i.strategy))()) : new rr(), l.layoutManager.subscribeTargets({
        type: As,
        target: l,
        targets: l.getObjects()
      }), l.setCoords(), l;
    });
  }
};
f(ge, "type", "Group"), f(ge, "ownDefaults", {
  strokeWidth: 0,
  subTargetCheck: !1,
  interactive: !1
}), w.setClass(ge);
var Sl = (r, t) => r && r.length === 1 ? r[0] : new ge(r, t), hn = (r, t) => Math.min(t.width / r.width, t.height / r.height), cn = (r, t) => Math.max(t.width / r.width, t.height / r.height), _i = "\\s*,?\\s*", De = `${_i}(${dt})`, Cl = `${De}${De}${De}${_i}([01])${_i}([01])${De}${De}`, bl = {
  m: "l",
  M: "L"
}, wl = (r, t, e, i, s, o, n, a, l, h, c) => {
  let u = mt(r), d = vt(r), g = mt(t), p = vt(t), m = e * s * g - i * o * p + n, y = i * s * g + e * o * p + a;
  return [
    "C",
    h + l * (-e * s * d - i * o * u),
    c + l * (-i * s * d + e * o * u),
    m + l * (e * s * p + i * o * g),
    y + l * (i * s * p - e * o * g),
    m,
    y
  ];
}, Fs = (r, t, e, i) => {
  let s = Math.atan2(t, r), o = Math.atan2(i, e);
  return o >= s ? o - s : 2 * Math.PI - (s - o);
};
function Si(r, t, e, i, s, o, n, a) {
  let l;
  if (P.cachesBoundsOfCurve && (l = [...arguments].join(), qe.boundsOfCurveCache[l])) return qe.boundsOfCurveCache[l];
  let h = Math.sqrt, c = Math.abs, u = [], d = [[0, 0], [0, 0]], g = 6 * r - 12 * e + 6 * s, p = -3 * r + 9 * e - 9 * s + 3 * n, m = 3 * e - 3 * r;
  for (let C = 0; C < 2; ++C) {
    if (C > 0 && (g = 6 * t - 12 * i + 6 * o, p = -3 * t + 9 * i - 9 * o + 3 * a, m = 3 * i - 3 * t), c(p) < 1e-12) {
      if (c(g) < 1e-12) continue;
      let D = -m / g;
      0 < D && D < 1 && u.push(D);
      continue;
    }
    let b = g * g - 4 * m * p;
    if (b < 0) continue;
    let O = h(b), T = (-g + O) / (2 * p);
    0 < T && T < 1 && u.push(T);
    let k = (-g - O) / (2 * p);
    0 < k && k < 1 && u.push(k);
  }
  let y = u.length, x = y, _ = dn(r, t, e, i, s, o, n, a);
  for (; y--; ) {
    let { x: C, y: b } = _(u[y]);
    d[0][y] = C, d[1][y] = b;
  }
  d[0][x] = r, d[1][x] = t, d[0][x + 1] = n, d[1][x + 1] = a;
  let S = [new v(Math.min(...d[0]), Math.min(...d[1])), new v(Math.max(...d[0]), Math.max(...d[1]))];
  return P.cachesBoundsOfCurve && (qe.boundsOfCurveCache[l] = S), S;
}
var Tl = (r, t, [e, i, s, o, n, a, l, h]) => {
  let c = ((u, d, g, p, m, y, x) => {
    if (g === 0 || p === 0) return [];
    let _ = 0, S = 0, C = 0, b = Math.PI, O = x * Ii, T = vt(O), k = mt(O), D = 0.5 * (-k * u - T * d), I = 0.5 * (-k * d + T * u), j = g ** 2, E = p ** 2, R = I ** 2, X = D ** 2, z = j * E - j * R - E * X, Y = Math.abs(g), q = Math.abs(p);
    if (z < 0) {
      let Lt = Math.sqrt(1 - z / (j * E));
      Y *= Lt, q *= Lt;
    } else C = (m === y ? -1 : 1) * Math.sqrt(z / (j * R + E * X));
    let rt = C * Y * I / q, A = -C * q * D / Y, yt = k * rt - T * A + 0.5 * u, we = T * rt + k * A + 0.5 * d, Te = Fs(1, 0, (D - rt) / Y, (I - A) / q), Ft = Fs((D - rt) / Y, (I - A) / q, (-D - rt) / Y, (-I - A) / q);
    y === 0 && Ft > 0 ? Ft -= 2 * b : y === 1 && Ft < 0 && (Ft += 2 * b);
    let Oe = Math.ceil(Math.abs(Ft / b * 2)), ar = [], ke = Ft / Oe, Hn = 8 / 3 * Math.sin(ke / 4) * Math.sin(ke / 4) / Math.sin(ke / 2), Jr = Te + ke;
    for (let Lt = 0; Lt < Oe; Lt++) ar[Lt] = wl(Te, Jr, k, T, Y, q, yt, we, Hn, _, S), _ = ar[Lt][5], S = ar[Lt][6], Te = Jr, Jr += ke;
    return ar;
  })(l - r, h - t, i, s, n, a, o);
  for (let u = 0, d = c.length; u < d; u++) c[u][1] += r, c[u][2] += t, c[u][3] += r, c[u][4] += t, c[u][5] += r, c[u][6] += t;
  return c;
}, un = (r) => {
  let t = 0, e = 0, i = 0, s = 0, o = [], n, a = 0, l = 0;
  for (let h of r) {
    let c = [...h], u;
    switch (c[0]) {
      case "l":
        c[1] += t, c[2] += e;
      case "L":
        t = c[1], e = c[2], u = [
          "L",
          t,
          e
        ];
        break;
      case "h":
        c[1] += t;
      case "H":
        t = c[1], u = [
          "L",
          t,
          e
        ];
        break;
      case "v":
        c[1] += e;
      case "V":
        e = c[1], u = [
          "L",
          t,
          e
        ];
        break;
      case "m":
        c[1] += t, c[2] += e;
      case "M":
        t = c[1], e = c[2], i = c[1], s = c[2], u = [
          "M",
          t,
          e
        ];
        break;
      case "c":
        c[1] += t, c[2] += e, c[3] += t, c[4] += e, c[5] += t, c[6] += e;
      case "C":
        a = c[3], l = c[4], t = c[5], e = c[6], u = [
          "C",
          c[1],
          c[2],
          a,
          l,
          t,
          e
        ];
        break;
      case "s":
        c[1] += t, c[2] += e, c[3] += t, c[4] += e;
      case "S":
        n === "C" ? (a = 2 * t - a, l = 2 * e - l) : (a = t, l = e), t = c[3], e = c[4], u = [
          "C",
          a,
          l,
          c[1],
          c[2],
          t,
          e
        ], a = u[3], l = u[4];
        break;
      case "q":
        c[1] += t, c[2] += e, c[3] += t, c[4] += e;
      case "Q":
        a = c[1], l = c[2], t = c[3], e = c[4], u = [
          "Q",
          a,
          l,
          t,
          e
        ];
        break;
      case "t":
        c[1] += t, c[2] += e;
      case "T":
        n === "Q" ? (a = 2 * t - a, l = 2 * e - l) : (a = t, l = e), t = c[1], e = c[2], u = [
          "Q",
          a,
          l,
          t,
          e
        ];
        break;
      case "a":
        c[6] += t, c[7] += e;
      case "A":
        Tl(t, e, c).forEach((d) => o.push(d)), t = c[6], e = c[7];
        break;
      case "z":
      case "Z":
        t = i, e = s, u = ["Z"];
    }
    u ? (o.push(u), n = u[0]) : n = "";
  }
  return o;
}, Fr = (r, t, e, i) => Math.sqrt((e - r) ** 2 + (i - t) ** 2), dn = (r, t, e, i, s, o, n, a) => (l) => {
  let h = l ** 3, c = ((g) => 3 * g ** 2 * (1 - g))(l), u = ((g) => 3 * g * (1 - g) ** 2)(l), d = ((g) => (1 - g) ** 3)(l);
  return new v(n * h + s * c + e * u + r * d, a * h + o * c + i * u + t * d);
}, gn = (r) => r ** 2, fn = (r) => 2 * r * (1 - r), pn = (r) => (1 - r) ** 2, Ol = (r, t, e, i, s, o, n, a) => (l) => {
  let h = gn(l), c = fn(l), u = pn(l), d = 3 * (u * (e - r) + c * (s - e) + h * (n - s)), g = 3 * (u * (i - t) + c * (o - i) + h * (a - o));
  return Math.atan2(g, d);
}, kl = (r, t, e, i, s, o) => (n) => {
  let a = gn(n), l = fn(n), h = pn(n);
  return new v(s * a + e * l + r * h, o * a + i * l + t * h);
}, Ml = (r, t, e, i, s, o) => (n) => {
  let a = 1 - n, l = 2 * (a * (e - r) + n * (s - e)), h = 2 * (a * (i - t) + n * (o - i));
  return Math.atan2(h, l);
}, Ls = (r, t, e) => {
  let i = new v(t, e), s = 0;
  for (let o = 1; o <= 100; o += 1) {
    let n = r(o / 100);
    s += Fr(i.x, i.y, n.x, n.y), i = n;
  }
  return s;
}, Dl = (r, t) => {
  let e, i = 0, s = 0, o = {
    x: r.x,
    y: r.y
  }, n = { ...o }, a = 0.01, l = 0, h = r.iterator, c = r.angleFinder;
  for (; s < t && a > 1e-4; ) n = h(i), l = i, e = Fr(o.x, o.y, n.x, n.y), e + s > t ? (i -= a, a /= 2) : (o = n, i += a, s += e);
  return {
    ...n,
    angle: c(l)
  };
}, cs = (r) => {
  let t, e, i = 0, s = 0, o = 0, n = 0, a = 0, l = [];
  for (let h of r) {
    let c = {
      x: s,
      y: o,
      command: h[0],
      length: 0
    };
    switch (h[0]) {
      case "M":
        e = c, e.x = n = s = h[1], e.y = a = o = h[2];
        break;
      case "L":
        e = c, e.length = Fr(s, o, h[1], h[2]), s = h[1], o = h[2];
        break;
      case "C":
        t = dn(s, o, h[1], h[2], h[3], h[4], h[5], h[6]), e = c, e.iterator = t, e.angleFinder = Ol(s, o, h[1], h[2], h[3], h[4], h[5], h[6]), e.length = Ls(t, s, o), s = h[5], o = h[6];
        break;
      case "Q":
        t = kl(s, o, h[1], h[2], h[3], h[4]), e = c, e.iterator = t, e.angleFinder = Ml(s, o, h[1], h[2], h[3], h[4]), e.length = Ls(t, s, o), s = h[3], o = h[4];
        break;
      case "Z":
        e = c, e.destX = n, e.destY = a, e.length = Fr(s, o, n, a), s = n, o = a;
    }
    i += e.length, l.push(e);
  }
  return l.push({
    length: i,
    x: s,
    y: o
  }), l;
}, mn = (r, t, e = cs(r)) => {
  let i = 0;
  for (; t - e[i].length > 0 && i < e.length - 2; ) t -= e[i].length, i++;
  let s = e[i], o = t / s.length, n = r[i];
  switch (s.command) {
    case "M":
      return {
        x: s.x,
        y: s.y,
        angle: 0
      };
    case "Z":
      return {
        ...new v(s.x, s.y).lerp(new v(s.destX, s.destY), o),
        angle: Math.atan2(s.destY - s.y, s.destX - s.x)
      };
    case "L":
      return {
        ...new v(s.x, s.y).lerp(new v(n[1], n[2]), o),
        angle: Math.atan2(n[2] - s.y, n[1] - s.x)
      };
    case "C":
    case "Q":
      return Dl(s, t);
  }
}, El = RegExp("[mzlhvcsqta][^mzlhvcsqta]*", "gi"), Rs = new RegExp(Cl, "g"), Pl = new RegExp(dt, "gi"), jl = {
  m: 2,
  l: 2,
  h: 1,
  v: 1,
  c: 6,
  s: 4,
  q: 4,
  t: 2,
  a: 7
}, vn = (r) => {
  var t;
  let e = [], i = (t = r.match(El)) == null ? [] : t;
  for (let s of i) {
    let o = s[0];
    if (o === "z" || o === "Z") {
      e.push([o]);
      continue;
    }
    let n = jl[o.toLowerCase()], a = [];
    if (o === "a" || o === "A") {
      let l;
      for (Rs.lastIndex = 0; l = Rs.exec(s); ) a.push(...l.slice(1));
    } else a = s.match(Pl) || [];
    for (let l = 0; l < a.length; l += n) {
      let h = Array(n), c = bl[o];
      h[0] = l > 0 && c ? c : o;
      for (let u = 0; u < n; u++) h[u + 1] = parseFloat(a[l + u]);
      e.push(h);
    }
  }
  return e;
}, yn = (r, t = 0) => {
  let e = new v(r[0]), i = new v(r[1]), s = 1, o = 0, n = [], a = r.length, l = a > 2, h;
  for (l && (s = r[2].x < i.x ? -1 : r[2].x === i.x ? 0 : 1, o = r[2].y < i.y ? -1 : r[2].y === i.y ? 0 : 1), n.push([
    "M",
    e.x - s * t,
    e.y - o * t
  ]), h = 1; h < a; h++) {
    if (!e.eq(i)) {
      let c = e.midPointFrom(i);
      n.push([
        "Q",
        e.x,
        e.y,
        c.x,
        c.y
      ]);
    }
    e = r[h], h + 1 < r.length && (i = r[h + 1]);
  }
  return l && (s = e.x > r[h - 2].x ? 1 : e.x === r[h - 2].x ? 0 : -1, o = e.y > r[h - 2].y ? 1 : e.y === r[h - 2].y ? 0 : -1), n.push([
    "L",
    e.x + s * t,
    e.y + o * t
  ]), n;
}, Al = (r, t, e) => (e && (t = $(t, [
  1,
  0,
  0,
  1,
  -e.x,
  -e.y
])), r.map((i) => {
  let s = [...i];
  for (let o = 1; o < i.length - 1; o += 2) {
    let { x: n, y: a } = U({
      x: i[o],
      y: i[o + 1]
    }, t);
    s[o] = n, s[o + 1] = a;
  }
  return s;
})), Fl = (r, t) => {
  let e = 2 * Math.PI / r, i = -Yt;
  r % 2 == 0 && (i += e / 2);
  let s = Array(r + 1);
  for (let o = 0; o < r; o++) {
    let n = o * e + i, { x: a, y: l } = new v(mt(n), vt(n)).scalarMultiply(t);
    s[o] = [
      o === 0 ? "M" : "L",
      a,
      l
    ];
  }
  return s[r] = ["Z"], s;
}, us = (r, t) => r.map((e) => e.map((i, s) => s === 0 || t === void 0 ? i : F(i, t)).join(" ")).join(" "), Ll = (r, t) => {
  var e;
  let i = r, s = t;
  i.inverted && !s.inverted && (i = t, s = r), Ni(s, (e = s.group) == null ? void 0 : e.calcTransformMatrix(), i.calcTransformMatrix());
  let o = i.inverted && s.inverted;
  return o && (i.inverted = s.inverted = !1), new ge([i], {
    clipPath: s,
    inverted: o
  });
}, Rl = (r, t) => Math.floor(Math.random() * (t - r + 1)) + r, Il = (r, t) => {
  let e = r._findCenterFromElement();
  r.transformMatrix && (((i) => {
    if (i.transformMatrix) {
      let { scaleX: s, scaleY: o, angle: n, skewX: a } = pe(i.transformMatrix);
      i.flipX = !1, i.flipY = !1, i.set(Wt, s), i.set(Vt, o), i.angle = n, i.skewX = a, i.skewY = 0;
    }
  })(r), e = e.transform(r.transformMatrix)), delete r.transformMatrix, t && (r.scaleX *= t.scaleX, r.scaleY *= t.scaleY, r.cropX = t.cropX, r.cropY = t.cropY, e.x += t.offsetLeft, e.y += t.offsetTop, r.width = t.width, r.height = t.height), r.setPositionByOrigin(e, L, L);
}, Kh = ir({
  addTransformToObject: () => vo,
  animate: () => ss,
  animateColor: () => Ao,
  applyTransformToObject: () => ye,
  calcAngleBetweenVectors: () => jr,
  calcDimensionsMatrix: () => sr,
  calcPlaneChangeMatrix: () => nr,
  calcVectorRotation: () => Ki,
  cancelAnimFrame: () => so,
  capValue: () => te,
  composeMatrix: () => ho,
  copyCanvasElement: () => Zn,
  cos: () => mt,
  createCanvasElement: () => bt,
  createImage: () => oo,
  createRotateMatrix: () => ee,
  createScaleMatrix: () => Br,
  createSkewXMatrix: () => Hi,
  createSkewYMatrix: () => zi,
  createTranslateMatrix: () => be,
  createVector: () => tr,
  crossProduct: () => ue,
  degreesToRadians: () => B,
  dotProduct: () => So,
  ease: () => va,
  enlivenObjectEnlivables: () => or,
  enlivenObjects: () => me,
  findScaleToCover: () => cn,
  findScaleToFit: () => hn,
  getBoundsOfCurve: () => Si,
  getOrthonormalVector: () => Ji,
  getPathSegmentsInfo: () => cs,
  getPointOnPath: () => mn,
  getPointer: () => mo,
  getRandomInt: () => Rl,
  getRegularPolygonPath: () => Fl,
  getSmoothPathFromPoints: () => yn,
  getSvgAttributes: () => ca,
  getUnitVector: () => Wr,
  groupSVGElements: () => Sl,
  hasStyleChanged: () => Nr,
  invertTransform: () => ot,
  isBetweenVectors: () => ci,
  isIdentityMatrix: () => no,
  isTouchEvent: () => Er,
  isTransparent: () => Zo,
  joinPath: () => us,
  loadImage: () => Je,
  magnitude: () => Pr,
  makeBoundingBoxFromPoints: () => St,
  makePathSimpler: () => un,
  matrixToSVG: () => ve,
  mergeClipPaths: () => Ll,
  multiplyTransformMatrices: () => $,
  multiplyTransformMatrixArray: () => Ir,
  parsePath: () => vn,
  parsePreserveAspectRatioAttribute: () => wo,
  parseUnit: () => Zt,
  pick: () => re,
  projectStrokeOnPoints: () => rn,
  qrDecompose: () => pe,
  radiansToDegrees: () => Dt,
  removeFromArray: () => Gt,
  removeTransformFromObject: () => na,
  removeTransformMatrixForSvgParsing: () => Il,
  requestAnimFrame: () => Ke,
  resetObjectTransform: () => yo,
  rotateVector: () => qi,
  saveObjectTransform: () => Ui,
  sendObjectToPlane: () => Ni,
  sendPointToPlane: () => Et,
  sendVectorToPlane: () => xo,
  sin: () => vt,
  sizeAfterTransform: () => Yr,
  string: () => ea,
  stylesFromArray: () => on,
  stylesToArray: () => sn,
  toBlob: () => Yi,
  toDataURL: () => $i,
  toFixed: () => F,
  transformPath: () => Al,
  transformPoint: () => U
});
function Ci(r, t) {
  let e = r.style;
  e && Object.entries(t).forEach(([i, s]) => e.setProperty(i, s));
}
var Bl = class extends fo {
  constructor(r, { allowTouchScrolling: t = !1, containerClass: e = "" } = {}) {
    super(r), f(this, "upper", void 0), f(this, "container", void 0);
    let { el: i } = this.lower, s = this.createUpperCanvas();
    this.upper = {
      el: s,
      ctx: s.getContext("2d")
    }, this.applyCanvasStyle(i, { allowTouchScrolling: t }), this.applyCanvasStyle(s, {
      allowTouchScrolling: t,
      styles: {
        position: "absolute",
        left: "0",
        top: "0"
      }
    });
    let o = this.createContainerElement();
    o.classList.add(e), i.parentNode && i.parentNode.replaceChild(o, i), o.append(i, s), this.container = o;
  }
  createUpperCanvas() {
    let { el: r } = this.lower, t = bt();
    return t.className = r.className, t.classList.remove("lower-canvas"), t.classList.add("upper-canvas"), t.setAttribute("data-fabric", "top"), t.style.cssText = r.style.cssText, t.setAttribute("draggable", "true"), t;
  }
  createContainerElement() {
    let r = _e().createElement("div");
    return r.setAttribute("data-fabric", "wrapper"), Ci(r, { position: "relative" }), xs(r), r;
  }
  applyCanvasStyle(r, t) {
    let { styles: e, allowTouchScrolling: i } = t;
    Ci(r, {
      ...e,
      "touch-action": i ? "manipulation" : Lr
    }), xs(r);
  }
  setDimensions(r, t) {
    super.setDimensions(r, t);
    let { el: e, ctx: i } = this.upper;
    go(e, i, r, t);
  }
  setCSSDimensions(r) {
    super.setCSSDimensions(r), hi(this.upper.el, r), hi(this.container, r);
  }
  cleanupDOM(r) {
    let t = this.container, { el: e } = this.lower, { el: i } = this.upper;
    super.cleanupDOM(r), t.removeChild(i), t.removeChild(e), t.parentNode && t.parentNode.replaceChild(e, t);
  }
  dispose() {
    super.dispose(), Ct().dispose(this.upper.el), delete this.upper, delete this.container;
  }
}, xn = (r, t, e, i) => {
  let { target: s, offsetX: o, offsetY: n } = t, a = e - o, l = i - n, h = !ft(s, "lockMovementX") && s.left !== a, c = !ft(s, "lockMovementY") && s.top !== l;
  return h && s.set("left", a), c && s.set("top", l), (h || c) && os(qs, Zi(r, t, e, i)), h || c;
}, _n = Zs, Sn = (r) => function(t, e, i) {
  let { points: s, pathOffset: o } = i;
  return new v(s[r]).subtract(o).transform($(i.getViewportTransform(), i.calcTransformMatrix()));
}, Cn = (r, t, e, i) => {
  let { target: s, pointIndex: o } = t, n = s, a = Et(new v(e, i), void 0, n.calcOwnMatrix());
  return n.points[o] = a.add(n.pathOffset), n.setDimensions(), n.set("dirty", !0), !0;
}, bn = (r, t) => function(e, i, s, o) {
  let n = i.target, a = new v(n.points[(r > 0 ? r : n.points.length) - 1]), l = a.subtract(n.pathOffset).transform(n.calcOwnMatrix()), h = t(e, {
    ...i,
    pointIndex: r
  }, s, o), c = a.subtract(n.pathOffset).transform(n.calcOwnMatrix()).subtract(l);
  return n.left -= c.x, n.top -= c.y, h;
}, wn = (r) => jt(_n, bn(r, Cn));
function Xl(r, t = {}) {
  let e = {};
  for (let i = 0; i < (typeof r == "number" ? r : r.points.length); i++) e[`p${i}`] = new st({
    actionName: _n,
    positionHandler: Sn(i),
    actionHandler: wn(i),
    ...t
  });
  return e;
}
var bi = (r, t, e) => {
  let { path: i, pathOffset: s } = r, o = i[t];
  return new v(o[e] - s.x, o[e + 1] - s.y).transform($(r.getViewportTransform(), r.calcTransformMatrix()));
};
function $l(r, t, e) {
  let { commandIndex: i, pointIndex: s } = this;
  return bi(e, i, s);
}
function Yl(r, t, e, i) {
  let { target: s } = t, { commandIndex: o, pointIndex: n } = this, a = ((l, h, c, u, d) => {
    let { path: g, pathOffset: p } = l, m = g[(u > 0 ? u : g.length) - 1], y = new v(m[d], m[d + 1]), x = y.subtract(p).transform(l.calcOwnMatrix()), _ = Et(new v(h, c), void 0, l.calcOwnMatrix());
    g[u][d] = _.x + p.x, g[u][d + 1] = _.y + p.y, l.setDimensions();
    let S = y.subtract(l.pathOffset).transform(l.calcOwnMatrix()).subtract(x);
    return l.left -= S.x, l.top -= S.y, l.set("dirty", !0), !0;
  })(s, e, i, o, n);
  return a && os(this.actionName, {
    ...Zi(r, t, e, i),
    commandIndex: o,
    pointIndex: n
  }), a;
}
var Tn = class extends st {
  constructor(r) {
    super(r);
  }
  render(r, t, e, i, s) {
    let o = {
      ...i,
      cornerColor: this.controlFill,
      cornerStrokeColor: this.controlStroke,
      transparentCorners: !this.controlFill
    };
    super.render(r, t, e, o, s);
  }
}, Wl = class extends Tn {
  constructor(r) {
    super(r);
  }
  render(r, t, e, i, s) {
    let { path: o } = s, { commandIndex: n, pointIndex: a, connectToCommandIndex: l, connectToPointIndex: h } = this;
    r.save(), r.strokeStyle = this.controlStroke, this.connectionDashArray && r.setLineDash(this.connectionDashArray);
    let [c] = o[n], u = bi(s, l, h);
    if (c === "Q") {
      let d = bi(s, n, a + 2);
      r.moveTo(d.x, d.y), r.lineTo(t, e);
    } else r.moveTo(t, e);
    r.lineTo(u.x, u.y), r.stroke(), r.restore(), super.render(r, t, e, i, s);
  }
}, hr = (r, t, e, i, s, o) => new (e ? Wl : Tn)({
  commandIndex: r,
  pointIndex: t,
  actionName: "modifyPath",
  positionHandler: $l,
  actionHandler: Yl,
  connectToCommandIndex: s,
  connectToPointIndex: o,
  ...i,
  ...e ? i.controlPointStyle : i.pointStyle
});
function Vl(r, t = {}) {
  let e = {}, i = "M";
  return r.path.forEach((s, o) => {
    let n = s[0];
    switch (n !== "Z" && (e[`c_${o}_${n}`] = hr(o, s.length - 2, !1, t)), n) {
      case "C":
        e[`c_${o}_C_CP_1`] = hr(o, 1, !0, t, o - 1, /* @__PURE__ */ ((a) => a === "C" ? 5 : a === "Q" ? 3 : 1)(i)), e[`c_${o}_C_CP_2`] = hr(o, 3, !0, t, o, 5);
        break;
      case "Q":
        e[`c_${o}_Q_CP_1`] = hr(o, 1, !0, t, o, 3);
    }
    i = n;
  }), e;
}
var Jh = ir({
  changeHeight: () => Qa,
  changeObjectHeight: () => Ro,
  changeObjectWidth: () => Lo,
  changeWidth: () => ui,
  createObjectDefaultControls: () => as,
  createPathControls: () => Vl,
  createPolyActionHandler: () => wn,
  createPolyControls: () => Xl,
  createPolyPositionHandler: () => Sn,
  createResizeControls: () => qo,
  createTextboxDefaultControls: () => Ko,
  dragHandler: () => xn,
  factoryPolyActionHandler: () => bn,
  getLocalPoint: () => Vr,
  polyActionHandler: () => Cn,
  renderCircleControl: () => Io,
  renderSquareControl: () => Bo,
  rotationStyleHandler: () => Xo,
  rotationWithSnapping: () => $o,
  scaleCursorStyleHandler: () => le,
  scaleOrSkewActionName: () => Pe,
  scaleSkewCursorStyleHandler: () => Jt,
  scalingEqually: () => Ee,
  scalingX: () => Vo,
  scalingXOrSkewingY: () => di,
  scalingY: () => Ho,
  scalingYOrSkewingX: () => gi,
  skewCursorStyleHandler: () => zo,
  skewHandlerX: () => Uo,
  skewHandlerY: () => No,
  wrapWithFireEvent: () => jt,
  wrapWithFixedAnchor: () => Ht
}), On = class kn extends $r {
  constructor(...t) {
    super(...t), f(this, "_hoveredTargets", []), f(this, "_currentTransform", null), f(this, "_groupSelector", null), f(this, "contextTopDirty", !1);
  }
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...kn.ownDefaults
    };
  }
  get upperCanvasEl() {
    var t;
    return (t = this.elements.upper) == null ? void 0 : t.el;
  }
  get contextTop() {
    var t;
    return (t = this.elements.upper) == null ? void 0 : t.ctx;
  }
  get wrapperEl() {
    return this.elements.container;
  }
  initElements(t) {
    this.elements = new Bl(t, {
      allowTouchScrolling: this.allowTouchScrolling,
      containerClass: this.containerClass
    }), this._createCacheCanvas();
  }
  _onObjectAdded(t) {
    this._objectsToRender = void 0, super._onObjectAdded(t);
  }
  _onObjectRemoved(t) {
    this._objectsToRender = void 0, t === this._activeObject && (this.fire("before:selection:cleared", { deselected: [t] }), this._discardActiveObject(), this.fire("selection:cleared", { deselected: [t] }), t.fire("deselected", { target: t })), t === this._hoveredTarget && (this._hoveredTarget = void 0, this._hoveredTargets = []), super._onObjectRemoved(t);
  }
  _onStackOrderChanged() {
    this._objectsToRender = void 0, super._onStackOrderChanged();
  }
  _chooseObjectsToRender() {
    let t = this._activeObject;
    return !this.preserveObjectStacking && t ? this._objects.filter((e) => !e.group && e !== t).concat(t) : this._objects;
  }
  renderAll() {
    this.cancelRequestedRender(), this.destroyed || (!this.contextTopDirty || this._groupSelector || this.isDrawingMode || (this.clearContext(this.contextTop), this.contextTopDirty = !1), this.hasLostContext && (this.renderTopLayer(this.contextTop), this.hasLostContext = !1), !this._objectsToRender && (this._objectsToRender = this._chooseObjectsToRender()), this.renderCanvas(this.getContext(), this._objectsToRender));
  }
  renderTopLayer(t) {
    t.save(), this.isDrawingMode && this._isCurrentlyDrawing && (this.freeDrawingBrush && this.freeDrawingBrush._render(), this.contextTopDirty = !0), this.selection && this._groupSelector && (this._drawSelection(t), this.contextTopDirty = !0), t.restore();
  }
  renderTop() {
    let t = this.contextTop;
    this.clearContext(t), this.renderTopLayer(t), this.fire("after:render", { ctx: t });
  }
  setTargetFindTolerance(t) {
    t = Math.round(t), this.targetFindTolerance = t;
    let e = this.getRetinaScaling(), i = Math.ceil((2 * t + 1) * e);
    this.pixelFindCanvasEl.width = this.pixelFindCanvasEl.height = i, this.pixelFindContext.scale(e, e);
  }
  isTargetTransparent(t, e, i) {
    let s = this.targetFindTolerance, o = this.pixelFindContext;
    this.clearContext(o), o.save(), o.translate(-e + s, -i + s), o.transform(...this.viewportTransform);
    let n = t.selectionBackgroundColor;
    t.selectionBackgroundColor = "", t.render(o), t.selectionBackgroundColor = n, o.restore();
    let a = Math.round(s * this.getRetinaScaling());
    return Zo(o, a, a, a);
  }
  _isSelectionKeyPressed(t) {
    let e = this.selectionKey;
    return !!e && (Array.isArray(e) ? !!e.find((i) => !!i && t[i] === !0) : t[e]);
  }
  _shouldClearSelection(t, e) {
    let i = this.getActiveObjects(), s = this._activeObject;
    return !!(!e || e && s && i.length > 1 && i.indexOf(e) === -1 && s !== e && !this._isSelectionKeyPressed(t) || e && !e.evented || e && !e.selectable && s && s !== e);
  }
  _shouldCenterTransform(t, e, i) {
    if (!t) return;
    let s;
    return e === "scale" || e === "scaleX" || e === "scaleY" || e === "resizing" ? s = this.centeredScaling || t.centeredScaling : e === "rotate" && (s = this.centeredRotation || t.centeredRotation), s ? !i : i;
  }
  _getOriginFromCorner(t, e) {
    let i = e ? t.controls[e].getTransformAnchorPoint() : {
      x: t.originX,
      y: t.originY
    };
    return e && ([
      "ml",
      "tl",
      "bl"
    ].includes(e) ? i.x = gt : [
      "mr",
      "tr",
      "br"
    ].includes(e) && (i.x = V), [
      "tl",
      "mt",
      "tr"
    ].includes(e) ? i.y = Ns : [
      "bl",
      "mb",
      "br"
    ].includes(e) && (i.y = "top")), i;
  }
  _setupCurrentTransform(t, e, i) {
    var s;
    let o = e.group ? Et(this.getScenePoint(t), void 0, e.group.calcTransformMatrix()) : this.getScenePoint(t), { key: n = "", control: a } = e.getActiveControl() || {}, l = i && a ? (s = a.getActionHandler(t, e, a)) == null ? void 0 : s.bind(a) : xn, h = ((k, D, I, j) => {
      if (!D || !k) return "drag";
      let E = j.controls[D];
      return E.getActionName(I, E, j);
    })(i, n, t, e), c = t[this.centeredKey], u = this._shouldCenterTransform(e, h, c) ? {
      x: L,
      y: L
    } : this._getOriginFromCorner(e, n), { scaleX: d, scaleY: g, skewX: p, skewY: m, left: y, top: x, angle: _, width: S, height: C, cropX: b, cropY: O } = e, T = {
      target: e,
      action: h,
      actionHandler: l,
      actionPerformed: !1,
      corner: n,
      scaleX: d,
      scaleY: g,
      skewX: p,
      skewY: m,
      offsetX: o.x - y,
      offsetY: o.y - x,
      originX: u.x,
      originY: u.y,
      ex: o.x,
      ey: o.y,
      lastX: o.x,
      lastY: o.y,
      theta: B(_),
      width: S,
      height: C,
      shiftKey: t.shiftKey,
      altKey: c,
      original: {
        ...Ui(e),
        originX: u.x,
        originY: u.y,
        cropX: b,
        cropY: O
      }
    };
    this._currentTransform = T, this.fire("before:transform", {
      e: t,
      transform: T
    });
  }
  setCursor(t) {
    this.upperCanvasEl.style.cursor = t;
  }
  _drawSelection(t) {
    let { x: e, y: i, deltaX: s, deltaY: o } = this._groupSelector, n = new v(e, i).transform(this.viewportTransform), a = new v(e + s, i + o).transform(this.viewportTransform), l = this.selectionLineWidth / 2, h = Math.min(n.x, a.x), c = Math.min(n.y, a.y), u = Math.max(n.x, a.x), d = Math.max(n.y, a.y);
    this.selectionColor && (t.fillStyle = this.selectionColor, t.fillRect(h, c, u - h, d - c)), this.selectionLineWidth && this.selectionBorderColor && (t.lineWidth = this.selectionLineWidth, t.strokeStyle = this.selectionBorderColor, h += l, c += l, u -= l, d -= l, N.prototype._setLineDash.call(this, t, this.selectionDashArray), t.strokeRect(h, c, u - h, d - c));
  }
  findTarget(t) {
    if (this._targetInfo) return this._targetInfo;
    if (this.skipTargetFind) return {
      subTargets: [],
      currentSubTargets: []
    };
    let e = this.getScenePoint(t), i = this._activeObject, s = this.getActiveObjects(), o = this.searchPossibleTargets(this._objects, e), { subTargets: n, container: a, target: l } = o, h = {
      ...o,
      currentSubTargets: n,
      currentContainer: a,
      currentTarget: l
    };
    if (!i) return h;
    let c = {
      ...this.searchPossibleTargets([i], e),
      currentSubTargets: n,
      currentContainer: a,
      currentTarget: l
    };
    return i.findControl(this.getViewportPoint(t), Er(t)) ? {
      ...c,
      target: i
    } : c.target && (s.length > 1 || !this.preserveObjectStacking || this.preserveObjectStacking && t[this.altSelectionKey]) ? c : h;
  }
  _pointIsInObjectSelectionArea(t, e) {
    let i = t.getCoords(), s = this.getZoom(), o = t.padding / s;
    if (o) {
      let [n, a, l, h] = i, c = Math.atan2(a.y - n.y, a.x - n.x), u = mt(c) * o, d = vt(c) * o, g = u + d, p = u - d;
      i = [
        new v(n.x - p, n.y - g),
        new v(a.x + g, a.y - p),
        new v(l.x + p, l.y + g),
        new v(h.x - g, h.y + p)
      ];
    }
    return Qe.isPointInPolygon(e, i);
  }
  _checkTarget(t, e) {
    if (t && t.visible && t.evented && this._pointIsInObjectSelectionArea(t, e)) {
      if (!this.perPixelTargetFind && !t.perPixelTargetFind || t.isEditing) return !0;
      {
        let i = e.transform(this.viewportTransform);
        if (!this.isTargetTransparent(t, i.x, i.y)) return !0;
      }
    }
    return !1;
  }
  _searchPossibleTargets(t, e, i) {
    let s = t.length;
    for (; s--; ) {
      let o = t[s];
      if (this._checkTarget(o, e)) {
        if (br(o) && o.subTargetCheck) {
          let { target: n } = this._searchPossibleTargets(o._objects, e, i);
          n && i.push(n);
        }
        return {
          target: o,
          subTargets: i
        };
      }
    }
    return { subTargets: [] };
  }
  searchPossibleTargets(t, e) {
    let i = this._searchPossibleTargets(t, e, []);
    i.container = i.target;
    let { container: s, subTargets: o } = i;
    if (s && br(s) && s.interactive && o[0]) {
      for (let n = o.length - 1; n > 0; n--) {
        let a = o[n];
        if (!br(a) || !a.interactive) return i.target = a, i;
      }
      return i.target = o[0], i;
    }
    return i;
  }
  getViewportPoint(t) {
    return this._viewportPoint ? this._viewportPoint : this._getPointerImpl(t, !0);
  }
  getScenePoint(t) {
    return this._scenePoint ? this._scenePoint : this._getPointerImpl(t);
  }
  _getPointerImpl(t, e = !1) {
    let i = this.upperCanvasEl, s = i.getBoundingClientRect(), o = mo(t), n = s.width || 0, a = s.height || 0;
    n && a || ("top" in s && "bottom" in s && (a = Math.abs(s.top - s.bottom)), "right" in s && "left" in s && (n = Math.abs(s.right - s.left))), this.calcOffset(), o.x -= this._offset.left, o.y -= this._offset.top, e || (o = Et(o, void 0, this.viewportTransform));
    let l = this.getRetinaScaling();
    l !== 1 && (o.x /= l, o.y /= l);
    let h = n === 0 || a === 0 ? new v(1, 1) : new v(i.width / n, i.height / a);
    return o.multiply(h);
  }
  _setDimensionsImpl(t, e) {
    this._resetTransformEventData(), super._setDimensionsImpl(t, e), this._isCurrentlyDrawing && this.freeDrawingBrush && this.freeDrawingBrush._setBrushStyles(this.contextTop);
  }
  _createCacheCanvas() {
    this.pixelFindCanvasEl = bt(), this.pixelFindContext = this.pixelFindCanvasEl.getContext("2d", { willReadFrequently: !0 }), this.setTargetFindTolerance(this.targetFindTolerance);
  }
  getTopContext() {
    return this.elements.upper.ctx;
  }
  getSelectionContext() {
    return this.elements.upper.ctx;
  }
  getSelectionElement() {
    return this.elements.upper.el;
  }
  getActiveObject() {
    return this._activeObject;
  }
  getActiveObjects() {
    let t = this._activeObject;
    return Ut(t) ? t.getObjects() : t ? [t] : [];
  }
  _fireSelectionEvents(t, e) {
    let i = !1, s = !1, o = this.getActiveObjects(), n = [], a = [];
    t.forEach((l) => {
      o.includes(l) || (i = !0, l.fire("deselected", {
        e,
        target: l
      }), a.push(l));
    }), o.forEach((l) => {
      t.includes(l) || (i = !0, l.fire("selected", {
        e,
        target: l
      }), n.push(l));
    }), t.length > 0 && o.length > 0 ? (s = !0, i && this.fire("selection:updated", {
      e,
      selected: n,
      deselected: a
    })) : o.length > 0 ? (s = !0, this.fire("selection:created", {
      e,
      selected: n
    })) : t.length > 0 && (s = !0, this.fire("selection:cleared", {
      e,
      deselected: a
    })), s && (this._objectsToRender = void 0);
  }
  setActiveObject(t, e) {
    let i = this.getActiveObjects(), s = this._setActiveObject(t, e);
    return this._fireSelectionEvents(i, e), s;
  }
  _setActiveObject(t, e) {
    let i = this._activeObject;
    return i !== t && !(!this._discardActiveObject(e, t) && this._activeObject) && !t.onSelect({ e }) && (this._activeObject = t, Ut(t) && i !== t && t.set("canvas", this), t.setCoords(), !0);
  }
  _discardActiveObject(t, e) {
    let i = this._activeObject;
    return !!i && !i.onDeselect({
      e: t,
      object: e
    }) && (this._currentTransform && this._currentTransform.target === i && this.endCurrentTransform(t), Ut(i) && i === this._hoveredTarget && (this._hoveredTarget = void 0), this._activeObject = void 0, !0);
  }
  discardActiveObject(t) {
    let e = this.getActiveObjects(), i = this.getActiveObject();
    e.length && this.fire("before:selection:cleared", {
      e: t,
      deselected: [i]
    });
    let s = this._discardActiveObject(t);
    return this._fireSelectionEvents(e, t), s;
  }
  endCurrentTransform(t) {
    let e = this._currentTransform;
    this._finalizeCurrentTransform(t), e && e.target && (e.target.isMoving = !1), this._currentTransform = null;
  }
  _finalizeCurrentTransform(t) {
    let e = this._currentTransform, i = e.target, s = {
      e: t,
      target: i,
      transform: e,
      action: e.action
    };
    i._scaling && (i._scaling = !1), i.setCoords(), e.actionPerformed && (this.fire("object:modified", s), i.fire(eo, s));
  }
  setViewportTransform(t) {
    super.setViewportTransform(t);
    let e = this._activeObject;
    e && e.setCoords();
  }
  destroy() {
    let t = this._activeObject;
    Ut(t) && (t.removeAll(), t.dispose()), delete this._activeObject, super.destroy(), this.pixelFindContext = null, this.pixelFindCanvasEl = void 0;
  }
  clear() {
    this.discardActiveObject(), this._activeObject = void 0, this.clearContext(this.contextTop), super.clear();
  }
  drawControls(t) {
    let e = this._activeObject;
    e && e._renderControls(t);
  }
  _toObject(t, e, i) {
    let s = this._realizeGroupTransformOnObject(t), o = super._toObject(t, e, i);
    return t.set(s), o;
  }
  _realizeGroupTransformOnObject(t) {
    let { group: e } = t;
    if (e && Ut(e) && this._activeObject === e) {
      let i = re(t, [
        "angle",
        "flipX",
        "flipY",
        V,
        Wt,
        Vt,
        Se,
        Ce,
        "top"
      ]);
      return vo(t, e.calcOwnMatrix()), i;
    }
    return {};
  }
  _setSVGObject(t, e, i) {
    let s = this._realizeGroupTransformOnObject(e);
    super._setSVGObject(t, e, i), e.set(s);
  }
};
f(On, "ownDefaults", {
  uniformScaling: !0,
  uniScaleKey: "shiftKey",
  centeredScaling: !1,
  centeredRotation: !1,
  centeredKey: "altKey",
  altActionKey: "shiftKey",
  selection: !0,
  selectionKey: "shiftKey",
  selectionColor: "rgba(100, 100, 255, 0.3)",
  selectionDashArray: [],
  selectionBorderColor: "rgba(255, 255, 255, 0.3)",
  selectionLineWidth: 1,
  selectionFullyContained: !1,
  hoverCursor: "move",
  moveCursor: "move",
  defaultCursor: "default",
  freeDrawingCursor: "crosshair",
  notAllowedCursor: "not-allowed",
  perPixelTargetFind: !1,
  targetFindTolerance: 0,
  skipTargetFind: !1,
  stopContextMenu: !0,
  fireRightClick: !0,
  fireMiddleClick: !0,
  enablePointerEvents: !1,
  containerClass: "canvas-container",
  preserveObjectStacking: !0
});
var Hl = class {
  constructor(r) {
    f(this, "targets", []), f(this, "__disposer", void 0);
    let t = () => {
      let { hiddenTextarea: i } = r.getActiveObject() || {};
      i && i.focus();
    }, e = r.upperCanvasEl;
    e.addEventListener("click", t), this.__disposer = () => e.removeEventListener("click", t);
  }
  exitTextEditing() {
    this.target = void 0, this.targets.forEach((r) => {
      r.isEditing && r.exitEditing();
    });
  }
  add(r) {
    this.targets.push(r);
  }
  remove(r) {
    this.unregister(r), Gt(this.targets, r);
  }
  register(r) {
    this.target = r;
  }
  unregister(r) {
    r === this.target && (this.target = void 0);
  }
  onMouseMove(r) {
    var t;
    (t = this.target) != null && t.isEditing && this.target.updateSelectionOnMouseMove(r);
  }
  clear() {
    this.targets = [], this.target = void 0;
  }
  dispose() {
    this.clear(), this.__disposer(), delete this.__disposer;
  }
}, it = { passive: !1 }, ne = (r, t) => ({
  viewportPoint: r.getViewportPoint(t),
  scenePoint: r.getScenePoint(t)
}), Rt = (r, ...t) => r.addEventListener(...t), at = (r, ...t) => r.removeEventListener(...t), zl = {
  mouse: {
    in: "over",
    out: "out",
    targetIn: "mouseover",
    targetOut: "mouseout",
    canvasIn: "mouse:over",
    canvasOut: "mouse:out"
  },
  drag: {
    in: "enter",
    out: "leave",
    targetIn: "dragenter",
    targetOut: "dragleave",
    canvasIn: "drag:enter",
    canvasOut: "drag:leave"
  }
}, wi = class extends On {
  constructor(r, t = {}) {
    super(r, t), f(this, "_isClick", void 0), f(this, "textEditingManager", new Hl(this)), [
      "_onMouseDown",
      "_onTouchStart",
      "_onMouseMove",
      "_onMouseUp",
      "_onTouchEnd",
      "_onResize",
      "_onMouseWheel",
      "_onMouseOut",
      "_onMouseEnter",
      "_onContextMenu",
      "_onClick",
      "_onDragStart",
      "_onDragEnd",
      "_onDragProgress",
      "_onDragOver",
      "_onDragEnter",
      "_onDragLeave",
      "_onDrop"
    ].forEach((e) => {
      this[e] = this[e].bind(this);
    }), this.addOrRemove(Rt);
  }
  _getEventPrefix() {
    return this.enablePointerEvents ? "pointer" : "mouse";
  }
  addOrRemove(r, t = !1) {
    let e = this.upperCanvasEl, i = this._getEventPrefix();
    r(uo(e), "resize", this._onResize), r(e, i + "down", this._onMouseDown), r(e, `${i}move`, this._onMouseMove, it), r(e, `${i}out`, this._onMouseOut), r(e, `${i}enter`, this._onMouseEnter), r(e, "wheel", this._onMouseWheel, { passive: !1 }), r(e, "contextmenu", this._onContextMenu), t || (r(e, "click", this._onClick), r(e, "dblclick", this._onClick)), r(e, "dragstart", this._onDragStart), r(e, "dragend", this._onDragEnd), r(e, "dragover", this._onDragOver), r(e, "dragenter", this._onDragEnter), r(e, "dragleave", this._onDragLeave), r(e, "drop", this._onDrop), this.enablePointerEvents || r(e, "touchstart", this._onTouchStart, it);
  }
  removeListeners() {
    this.addOrRemove(at);
    let r = this._getEventPrefix(), t = ut(this.upperCanvasEl);
    at(t, `${r}up`, this._onMouseUp), at(t, "touchend", this._onTouchEnd, it), at(t, `${r}move`, this._onMouseMove, it), at(t, "touchmove", this._onMouseMove, it), clearTimeout(this._willAddMouseDown);
  }
  _onMouseWheel(r) {
    this._cacheTransformEventData(r), this._handleEvent(r, "wheel"), this._resetTransformEventData();
  }
  _onMouseOut(r) {
    let t = this._hoveredTarget, e = {
      e: r,
      ...ne(this, r)
    };
    this.fire("mouse:out", {
      ...e,
      target: t
    }), this._hoveredTarget = void 0, t && t.fire("mouseout", { ...e }), this._hoveredTargets.forEach((i) => {
      this.fire("mouse:out", {
        ...e,
        target: i
      }), i && i.fire("mouseout", { ...e });
    }), this._hoveredTargets = [];
  }
  _onMouseEnter(r) {
    let { target: t } = this.findTarget(r);
    this._currentTransform || t || (this.fire("mouse:over", {
      e: r,
      ...ne(this, r)
    }), this._hoveredTarget = void 0, this._hoveredTargets = []);
  }
  _onDragStart(r) {
    this._isClick = !1;
    let t = this.getActiveObject();
    if (t && t.onDragStart(r)) {
      this._dragSource = t;
      let e = {
        e: r,
        target: t
      };
      this.fire("dragstart", e), t.fire("dragstart", e), Rt(this.upperCanvasEl, "drag", this._onDragProgress);
      return;
    }
    _s(r);
  }
  _renderDragEffects(r, t, e) {
    let i = !1, s = this._dropTarget;
    s && s !== t && s !== e && (s.clearContextTop(), i = !0), t?.clearContextTop(), e !== t && e?.clearContextTop();
    let o = this.contextTop;
    o.save(), o.transform(...this.viewportTransform), t && (o.save(), t.transform(o), t.renderDragSourceEffect(r), o.restore(), i = !0), e && (o.save(), e.transform(o), e.renderDropTargetEffect(r), o.restore(), i = !0), o.restore(), i && (this.contextTopDirty = !0);
  }
  _onDragEnd(r) {
    let { currentSubTargets: t } = this.findTarget(r), e = !!r.dataTransfer && r.dataTransfer.dropEffect !== "none", i = e ? this._activeObject : void 0, s = {
      e: r,
      target: this._dragSource,
      subTargets: t,
      dragSource: this._dragSource,
      didDrop: e,
      dropTarget: i
    };
    at(this.upperCanvasEl, "drag", this._onDragProgress), this.fire("dragend", s), this._dragSource && this._dragSource.fire("dragend", s), delete this._dragSource, this._onMouseUp(r);
  }
  _onDragProgress(r) {
    let t = {
      e: r,
      target: this._dragSource,
      dragSource: this._dragSource,
      dropTarget: this._draggedoverTarget
    };
    this.fire("drag", t), this._dragSource && this._dragSource.fire("drag", t);
  }
  _onDragOver(r) {
    let t = "dragover", { currentContainer: e, currentSubTargets: i } = this.findTarget(r), s = this._dragSource, o = {
      e: r,
      target: e,
      subTargets: i,
      dragSource: s,
      canDrop: !1,
      dropTarget: void 0
    }, n;
    this.fire(t, o), this._fireEnterLeaveEvents(r, e, o), e && (e.canDrop(r) && (n = e), e.fire(t, o));
    for (let a = 0; a < i.length; a++) {
      let l = i[a];
      l.canDrop(r) && (n = l), l.fire(t, o);
    }
    this._renderDragEffects(r, s, n), this._dropTarget = n;
  }
  _onDragEnter(r) {
    let { currentContainer: t, currentSubTargets: e } = this.findTarget(r), i = {
      e: r,
      target: t,
      subTargets: e,
      dragSource: this._dragSource
    };
    this.fire("dragenter", i), this._fireEnterLeaveEvents(r, t, i);
  }
  _onDragLeave(r) {
    let { currentSubTargets: t } = this.findTarget(r), e = {
      e: r,
      target: this._draggedoverTarget,
      subTargets: t,
      dragSource: this._dragSource
    };
    this.fire("dragleave", e), this._fireEnterLeaveEvents(r, void 0, e), this._renderDragEffects(r, this._dragSource), this._dropTarget = void 0, this._hoveredTargets = [];
  }
  _onDrop(r) {
    let { currentContainer: t, currentSubTargets: e } = this.findTarget(r), i = this._basicEventHandler("drop:before", {
      e: r,
      target: t,
      subTargets: e,
      dragSource: this._dragSource,
      ...ne(this, r)
    });
    i.didDrop = !1, i.dropTarget = void 0, this._basicEventHandler("drop", i), this.fire("drop:after", i);
  }
  _onContextMenu(r) {
    let { target: t, subTargets: e } = this.findTarget(r), i = this._basicEventHandler("contextmenu:before", {
      e: r,
      target: t,
      subTargets: e
    });
    return this.stopContextMenu && _s(r), this._basicEventHandler("contextmenu", i), !1;
  }
  _onClick(r) {
    let t = r.detail;
    t > 3 || t < 2 || (this._cacheTransformEventData(r), t == 2 && r.type === "dblclick" && this._handleEvent(r, "dblclick"), t == 3 && this._handleEvent(r, "tripleclick"), this._resetTransformEventData());
  }
  fireEventFromPointerEvent(r, t, e, i = {}) {
    this._cacheTransformEventData(r);
    let { target: s, subTargets: o } = this.findTarget(r), n = {
      e: r,
      target: s,
      subTargets: o,
      ...ne(this, r),
      transform: this._currentTransform,
      ...i
    };
    this.fire(t, n), s && s.fire(e, n);
    for (let a = 0; a < o.length; a++) o[a] !== s && o[a].fire(e, n);
    this._resetTransformEventData();
  }
  getPointerId(r) {
    let t = r.changedTouches;
    return t ? t[0] && t[0].identifier : this.enablePointerEvents ? r.pointerId : -1;
  }
  _isMainEvent(r) {
    return r.isPrimary === !0 || r.isPrimary !== !1 && (r.type === "touchend" && r.touches.length === 0 || !r.changedTouches || r.changedTouches[0].identifier === this.mainTouchId);
  }
  _onTouchStart(r) {
    this._cacheTransformEventData(r);
    let t = !this.allowTouchScrolling, e = this._activeObject;
    this.mainTouchId === void 0 && (this.mainTouchId = this.getPointerId(r)), this.__onMouseDown(r);
    let { target: i } = this.findTarget(r);
    (this.isDrawingMode || e && i === e) && (t = !0), t && r.preventDefault();
    let s = this.upperCanvasEl, o = this._getEventPrefix(), n = ut(s);
    Rt(n, "touchend", this._onTouchEnd, it), t && Rt(n, "touchmove", this._onMouseMove, it), at(s, `${o}down`, this._onMouseDown), this._resetTransformEventData();
  }
  _onMouseDown(r) {
    this._cacheTransformEventData(r), this.__onMouseDown(r);
    let t = this.upperCanvasEl, e = this._getEventPrefix();
    at(t, `${e}move`, this._onMouseMove, it);
    let i = ut(t);
    Rt(i, `${e}up`, this._onMouseUp), Rt(i, `${e}move`, this._onMouseMove, it), this._resetTransformEventData();
  }
  _onTouchEnd(r) {
    if (r.touches.length > 0) return;
    this._cacheTransformEventData(r), this.__onMouseUp(r), this._resetTransformEventData(), delete this.mainTouchId;
    let t = this._getEventPrefix(), e = ut(this.upperCanvasEl);
    at(e, "touchend", this._onTouchEnd, it), at(e, "touchmove", this._onMouseMove, it), this._willAddMouseDown && clearTimeout(this._willAddMouseDown), this._willAddMouseDown = setTimeout(() => {
      Rt(this.upperCanvasEl, `${t}down`, this._onMouseDown), this._willAddMouseDown = 0;
    }, 400);
  }
  _onMouseUp(r) {
    this._cacheTransformEventData(r), this.__onMouseUp(r);
    let t = this.upperCanvasEl, e = this._getEventPrefix();
    if (this._isMainEvent(r)) {
      let i = ut(this.upperCanvasEl);
      at(i, `${e}up`, this._onMouseUp), at(i, `${e}move`, this._onMouseMove, it), Rt(t, `${e}move`, this._onMouseMove, it);
    }
    this._resetTransformEventData();
  }
  _onMouseMove(r) {
    this._cacheTransformEventData(r);
    let t = this.getActiveObject();
    !this.allowTouchScrolling && (!t || !t.shouldStartDragging(r)) && r.preventDefault && r.preventDefault(), this.__onMouseMove(r), this._resetTransformEventData();
  }
  _onResize() {
    this.calcOffset(), this._resetTransformEventData();
  }
  _shouldRender(r) {
    let t = this.getActiveObject();
    return !!t != !!r || t && r && t !== r;
  }
  __onMouseUp(r) {
    var t;
    this._handleEvent(r, "up:before");
    let e = this._currentTransform, i = this._isClick, { target: s } = this.findTarget(r), { button: o } = r;
    if (o) return void ((this.fireMiddleClick && o === 1 || this.fireRightClick && o === 2) && this._handleEvent(r, "up"));
    if (this.isDrawingMode && this._isCurrentlyDrawing) return void this._onMouseUpInDrawingMode(r);
    if (!this._isMainEvent(r)) return;
    let n, a, l = !1;
    if (e && (this._finalizeCurrentTransform(r), l = e.actionPerformed), !i) {
      let h = s === this._activeObject;
      this.handleSelection(r), l || (l = this._shouldRender(s) || !h && s === this._activeObject);
    }
    if (s) {
      let { key: h, control: c } = s.findControl(this.getViewportPoint(r), Er(r)) || {};
      if (a = h, s.selectable && s !== this._activeObject && s.activeOn === "up") this.setActiveObject(s, r), l = !0;
      else if (c) {
        let u = c.getMouseUpHandler(r, s, c);
        u && (n = this.getScenePoint(r), u.call(c, r, e, n.x, n.y));
      }
      s.isMoving = !1;
    }
    if (e && (e.target !== s || e.corner !== a)) {
      let h = e.target && e.target.controls[e.corner], c = h && h.getMouseUpHandler(r, e.target, h);
      n = n || this.getScenePoint(r), c && c.call(h, r, e, n.x, n.y);
    }
    this._setCursorFromEvent(r, s), this._handleEvent(r, "up"), this._groupSelector = null, this._currentTransform = null, s && (s.__corner = void 0), l ? this.requestRenderAll() : i || (t = this._activeObject) != null && t.isEditing || this.renderTop();
  }
  _basicEventHandler(r, t) {
    let { target: e, subTargets: i = [] } = t;
    this.fire(r, t), e && e.fire(r, t);
    for (let s = 0; s < i.length; s++) i[s] !== e && i[s].fire(r, t);
    return t;
  }
  _handleEvent(r, t, e) {
    let { target: i, subTargets: s } = this.findTarget(r), o = {
      e: r,
      target: i,
      subTargets: s,
      ...ne(this, r),
      transform: this._currentTransform,
      ...t === "down:before" || t === "down" ? e : {}
    };
    t !== "up:before" && t !== "up" || (o.isClick = this._isClick), this.fire(`mouse:${t}`, o), i && i.fire(`mouse${t}`, o);
    for (let n = 0; n < s.length; n++) s[n] !== i && s[n].fire(`mouse${t}`, o);
  }
  _onMouseDownInDrawingMode(r) {
    this._isCurrentlyDrawing = !0, this.getActiveObject() && (this.discardActiveObject(r), this.requestRenderAll());
    let t = this.getScenePoint(r);
    this.freeDrawingBrush && this.freeDrawingBrush.onMouseDown(t, {
      e: r,
      pointer: t
    }), this._handleEvent(r, "down", { alreadySelected: !1 });
  }
  _onMouseMoveInDrawingMode(r) {
    if (this._isCurrentlyDrawing) {
      let t = this.getScenePoint(r);
      this.freeDrawingBrush && this.freeDrawingBrush.onMouseMove(t, {
        e: r,
        pointer: t
      });
    }
    this.setCursor(this.freeDrawingCursor), this._handleEvent(r, "move");
  }
  _onMouseUpInDrawingMode(r) {
    let t = this.getScenePoint(r);
    this.freeDrawingBrush ? this._isCurrentlyDrawing = !!this.freeDrawingBrush.onMouseUp({
      e: r,
      pointer: t
    }) : this._isCurrentlyDrawing = !1, this._handleEvent(r, "up");
  }
  __onMouseDown(r) {
    this._isClick = !0, this._handleEvent(r, "down:before");
    let { target: t } = this.findTarget(r), e = !!t && t === this._activeObject, { button: i } = r;
    if (i) return void ((this.fireMiddleClick && i === 1 || this.fireRightClick && i === 2) && this._handleEvent(r, "down", { alreadySelected: e }));
    if (this.isDrawingMode) return void this._onMouseDownInDrawingMode(r);
    if (!this._isMainEvent(r) || this._currentTransform) return;
    let s = this._shouldRender(t), o = !1;
    if (this.handleMultiSelection(r, t) ? (t = this._activeObject, o = !0, s = !0) : this._shouldClearSelection(r, t) && this.discardActiveObject(r), this.selection && (!t || !t.selectable && !t.isEditing && t !== this._activeObject)) {
      let n = this.getScenePoint(r);
      this._groupSelector = {
        x: n.x,
        y: n.y,
        deltaY: 0,
        deltaX: 0
      };
    }
    if (e = !!t && t === this._activeObject, t) {
      t.selectable && t.activeOn === "down" && this.setActiveObject(t, r);
      let n = t.findControl(this.getViewportPoint(r), Er(r));
      if (t === this._activeObject && (n || !o)) {
        this._setupCurrentTransform(r, t, e);
        let a = n ? n.control : void 0, l = this.getScenePoint(r), h = a && a.getMouseDownHandler(r, t, a);
        h && h.call(a, r, this._currentTransform, l.x, l.y);
      }
    }
    s && (this._objectsToRender = void 0), this._handleEvent(r, "down", { alreadySelected: e }), s && this.requestRenderAll();
  }
  _resetTransformEventData() {
    this._targetInfo = this._viewportPoint = this._scenePoint = void 0;
  }
  _cacheTransformEventData(r) {
    this._resetTransformEventData(), this._viewportPoint = this.getViewportPoint(r), this._scenePoint = Et(this._viewportPoint, void 0, this.viewportTransform), this._targetInfo = this.findTarget(r), this._currentTransform && (this._targetInfo.target = this._currentTransform.target);
  }
  __onMouseMove(r) {
    if (this._isClick = !1, this._handleEvent(r, "move:before"), this.isDrawingMode) return void this._onMouseMoveInDrawingMode(r);
    if (!this._isMainEvent(r)) return;
    let t = this._groupSelector;
    if (t) {
      let e = this.getScenePoint(r);
      t.deltaX = e.x - t.x, t.deltaY = e.y - t.y, this.renderTop();
    } else if (this._currentTransform) this._transformObject(r);
    else {
      let { target: e } = this.findTarget(r);
      this._setCursorFromEvent(r, e), this._fireOverOutEvents(r, e);
    }
    this.textEditingManager.onMouseMove(r), this._handleEvent(r, "move");
  }
  _fireOverOutEvents(r, t) {
    let { _hoveredTarget: e, _hoveredTargets: i } = this, { subTargets: s, currentTarget: o } = this.findTarget(r), n = Math.max(i.length, s.length);
    this.fireSyntheticInOutEvents("mouse", {
      e: r,
      target: t,
      oldTarget: e,
      actualTarget: o,
      oldActualTarget: this._hoveredActualTarget,
      fireCanvas: !0
    });
    for (let a = 0; a < n; a++) s[a] === t || i[a] && i[a] === e || this.fireSyntheticInOutEvents("mouse", {
      e: r,
      target: s[a],
      oldTarget: i[a]
    });
    this._hoveredActualTarget = o, this._hoveredTarget = t, this._hoveredTargets = s;
  }
  _fireEnterLeaveEvents(r, t, e) {
    let i = this._draggedoverTarget, s = this._hoveredTargets, { subTargets: o } = this.findTarget(r), n = Math.max(s.length, o.length);
    this.fireSyntheticInOutEvents("drag", {
      ...e,
      target: t,
      oldTarget: i,
      fireCanvas: !0
    });
    for (let a = 0; a < n; a++) this.fireSyntheticInOutEvents("drag", {
      ...e,
      target: o[a],
      oldTarget: s[a]
    });
    this._draggedoverTarget = t;
  }
  fireSyntheticInOutEvents(r, { target: t, oldTarget: e, actualTarget: i, oldActualTarget: s, fireCanvas: o, e: n, ...a }) {
    let { targetIn: l, targetOut: h, canvasIn: c, canvasOut: u } = zl[r], d = e !== t, g = s !== i, p = t && d, m = i && g, y = e && d, x = s && g, _ = {
      ...a,
      e: n,
      ...ne(this, n)
    }, S = {
      ..._,
      target: e,
      nextTarget: t,
      actualTarget: s,
      nextActualTarget: i
    };
    (y || x) && o && this.fire(u, S), y && e.fire(h, S), x && e !== s && s.fire(h, S);
    let C = {
      ..._,
      target: t,
      previousTarget: e,
      actualTarget: i,
      previousActualTarget: s
    };
    (p || m) && o && this.fire(c, C), p && t.fire(l, C), m && i !== t && i.fire(l, C);
  }
  _transformObject(r) {
    let t = this.getScenePoint(r), e = this._currentTransform, i = e.target, s = i.group ? Et(t, void 0, i.group.calcTransformMatrix()) : t;
    e.shiftKey = r.shiftKey, e.altKey = !!this.centeredKey && r[this.centeredKey], this._performTransformAction(r, e, s), e.actionPerformed && this.requestRenderAll();
  }
  _performTransformAction(r, t, e) {
    let { action: i, actionHandler: s, target: o } = t, n = !!s && s(r, t, e.x, e.y);
    n && o.setCoords(), i === "drag" && n && (t.target.isMoving = !0, this.setCursor(t.target.moveCursor || this.moveCursor)), t.actionPerformed = t.actionPerformed || n;
  }
  _setCursorFromEvent(r, t) {
    if (!t) return void this.setCursor(this.defaultCursor);
    let e = t.hoverCursor || this.hoverCursor, i = Ut(this._activeObject) ? this._activeObject : null, s = (!i || t.group !== i) && t.findControl(this.getViewportPoint(r));
    if (s) {
      let { control: o, coord: n } = s;
      this.setCursor(o.cursorStyleHandler(r, o, t, n));
    } else {
      if (t.subTargetCheck) {
        let { subTargets: o } = this.findTarget(r);
        o.concat().reverse().forEach((n) => {
          e = n.hoverCursor || e;
        });
      }
      this.setCursor(e);
    }
  }
  handleMultiSelection(r, t) {
    let e = this._activeObject, i = Ut(e);
    if (e && this._isSelectionKeyPressed(r) && this.selection && t && t.selectable && (e !== t || i) && (i || !t.isDescendantOf(e) && !e.isDescendantOf(t)) && !t.onSelect({ e: r }) && !e.getActiveControl()) {
      if (i) {
        let s = e.getObjects(), o = [];
        if (t === e) {
          let n = this.getScenePoint(r), a = this.searchPossibleTargets(s, n);
          if (a.target ? (t = a.target, o = a.subTargets) : (a = this.searchPossibleTargets(this._objects, n), t = a.target, o = a.subTargets), !t || !t.selectable) return !1;
        }
        t.group === e ? (e.remove(t), this._hoveredTarget = t, this._hoveredTargets = o, e.size() === 1 && this._setActiveObject(e.item(0), r)) : (e.multiSelectAdd(t), this._hoveredTarget = e, this._hoveredTargets = o), this._fireSelectionEvents(s, r);
      } else {
        e.isEditing && e.exitEditing();
        let s = new (w.getClass("ActiveSelection"))([], { canvas: this });
        s.multiSelectAdd(e, t), this._hoveredTarget = s, this._setActiveObject(s, r), this._fireSelectionEvents([e], r);
      }
      return !0;
    }
    return !1;
  }
  handleSelection(r) {
    if (!this.selection || !this._groupSelector) return !1;
    let { x: t, y: e, deltaX: i, deltaY: s } = this._groupSelector, o = new v(t, e), n = o.add(new v(i, s)), a = o.min(n), l = o.max(n).subtract(a), h = this.collectObjects({
      left: a.x,
      top: a.y,
      width: l.x,
      height: l.y
    }, { includeIntersecting: !this.selectionFullyContained }), c = o.eq(n) ? h[0] ? [h[0]] : [] : h.length > 1 ? h.filter((u) => !u.onSelect({ e: r })).reverse() : h;
    if (c.length === 1) this.setActiveObject(c[0], r);
    else if (c.length > 1) {
      let u = w.getClass("ActiveSelection");
      this.setActiveObject(new u(c, { canvas: this }), r);
    }
    return this._groupSelector = null, !0;
  }
  toCanvasElement(r = 1, t) {
    let { upper: e } = this.elements;
    e.ctx = void 0;
    let i = super.toCanvasElement(r, t);
    return e.ctx = e.el.getContext("2d"), i;
  }
  clear() {
    this.textEditingManager.clear(), super.clear();
  }
  destroy() {
    this.removeListeners(), this.textEditingManager.dispose(), super.destroy();
  }
}, Mn = {
  x1: 0,
  y1: 0,
  x2: 0,
  y2: 0
}, Gl = {
  ...Mn,
  r1: 0,
  r2: 0
}, he = (r, t) => isNaN(r) && typeof t == "number" ? t : r;
function Dn(r) {
  return r && /%$/.test(r) && Number.isFinite(parseFloat(r));
}
function En(r, t) {
  return te(0, he(typeof r == "number" ? r : typeof r == "string" ? parseFloat(r) / (Dn(r) ? 100 : 1) : NaN, t), 1);
}
var Ul = /\s*;\s*/, Nl = /\s*:\s*/;
function ql(r, t) {
  let e, i, s = r.getAttribute("style");
  if (s) {
    let n = s.split(Ul);
    n[n.length - 1] === "" && n.pop();
    for (let a = n.length; a--; ) {
      let [l, h] = n[a].split(Nl).map((c) => c.trim());
      l === "stop-color" ? e = h : l === "stop-opacity" && (i = h);
    }
  }
  e = e || r.getAttribute("stop-color") || "rgb(0,0,0)", i = he(parseFloat(i || r.getAttribute("stop-opacity") || ""), 1);
  let o = new et(e);
  return o.setAlpha(o.getAlpha() * i * t), {
    offset: En(r.getAttribute("offset"), 0),
    color: o.toRgba()
  };
}
function Kl(r, t) {
  let e = [], i = r.getElementsByTagName("stop"), s = En(t, 1);
  for (let o = i.length; o--; ) e.push(ql(i[o], s));
  return e;
}
function Pn(r) {
  return r.nodeName === "linearGradient" || r.nodeName === "LINEARGRADIENT" ? "linear" : "radial";
}
function jn(r) {
  return r.getAttribute("gradientUnits") === "userSpaceOnUse" ? "pixels" : "percentage";
}
function ct(r, t) {
  return r.getAttribute(t);
}
function Jl(r, t) {
  return (function(e, { width: i, height: s, gradientUnits: o }) {
    let n;
    return Object.entries(e).reduce((a, [l, h]) => {
      if (h === "Infinity") n = 1;
      else if (h === "-Infinity") n = 0;
      else {
        let c = typeof h == "string";
        n = c ? parseFloat(h) : h, c && Dn(h) && (n *= 0.01, o === "pixels" && (l !== "x1" && l !== "x2" && l !== "r2" || (n *= i), l !== "y1" && l !== "y2" || (n *= s)));
      }
      return a[l] = n, a;
    }, {});
  })(Pn(r) === "linear" ? (function(e) {
    return {
      x1: ct(e, "x1") || 0,
      y1: ct(e, "y1") || 0,
      x2: ct(e, "x2") || "100%",
      y2: ct(e, "y2") || 0
    };
  })(r) : (function(e) {
    return {
      x1: ct(e, "fx") || ct(e, "cx") || "50%",
      y1: ct(e, "fy") || ct(e, "cy") || "50%",
      r1: 0,
      x2: ct(e, "cx") || "50%",
      y2: ct(e, "cy") || "50%",
      r2: ct(e, "r") || "50%"
    };
  })(r), {
    ...t,
    gradientUnits: jn(r)
  });
}
var cr = class {
  constructor(r) {
    let { type: t = "linear", gradientUnits: e = "pixels", coords: i = {}, colorStops: s = [], offsetX: o = 0, offsetY: n = 0, gradientTransform: a, id: l } = r || {};
    Object.assign(this, {
      type: t,
      gradientUnits: e,
      coords: {
        ...t === "radial" ? Gl : Mn,
        ...i
      },
      colorStops: s,
      offsetX: o,
      offsetY: n,
      gradientTransform: a,
      id: l ? `${l}_${$t()}` : $t()
    });
  }
  addColorStop(r) {
    for (let t in r) this.colorStops.push({
      offset: parseFloat(t),
      color: r[t]
    });
    return this;
  }
  toObject(r) {
    return {
      ...re(this, r),
      type: this.type,
      coords: { ...this.coords },
      colorStops: this.colorStops.map((t) => ({ ...t })),
      offsetX: this.offsetX,
      offsetY: this.offsetY,
      gradientUnits: this.gradientUnits,
      gradientTransform: this.gradientTransform ? [...this.gradientTransform] : void 0
    };
  }
  toSVG(r, { additionalTransform: t } = {}) {
    let e = [], i = this.gradientTransform ? this.gradientTransform.concat() : Z.concat(), s = this.gradientUnits === "pixels" ? "userSpaceOnUse" : "objectBoundingBox", o = this.colorStops.map((u) => ({ ...u })).sort((u, d) => u.offset - d.offset), n = -this.offsetX, a = -this.offsetY;
    var l;
    s === "objectBoundingBox" ? (n /= r.width, a /= r.height) : (n += r.width / 2, a += r.height / 2), (l = r) && typeof l._renderPathCommands == "function" && this.gradientUnits !== "percentage" && (n -= r.pathOffset.x, a -= r.pathOffset.y), i[4] -= n, i[5] -= a;
    let h = [
      `id="SVGID_${M(String(this.id))}"`,
      `gradientUnits="${s}"`,
      `gradientTransform="${t ? t + " " : ""}${ve(i)}"`,
      ""
    ].join(" "), c = (u) => parseFloat(String(u));
    if (this.type === "linear") {
      let { x1: u, y1: d, x2: g, y2: p } = this.coords, m = c(u), y = c(d), x = c(g), _ = c(p);
      e.push("<linearGradient ", h, ' x1="', m, '" y1="', y, '" x2="', x, '" y2="', _, `">
`);
    } else if (this.type === "radial") {
      let { x1: u, y1: d, x2: g, y2: p, r1: m, r2: y } = this.coords, x = c(u), _ = c(d), S = c(g), C = c(p), b = c(m), O = c(y), T = b > O;
      e.push("<radialGradient ", h, ' cx="', T ? x : S, '" cy="', T ? _ : C, '" r="', T ? b : O, '" fx="', T ? S : x, '" fy="', T ? C : _, `">
`), T && (o.reverse(), o.forEach((D) => {
        D.offset = 1 - D.offset;
      }));
      let k = Math.min(b, O);
      if (k > 0) {
        let D = k / Math.max(b, O);
        o.forEach((I) => {
          I.offset += D * (1 - I.offset);
        });
      }
    }
    return o.forEach(({ color: u, offset: d }) => {
      let g = String(u), p = Hr(g) ? g : new et(g).toRgba();
      e.push(`<stop offset="${100 * d}%" style="stop-color:${M(p)};"/>
`);
    }), e.push(this.type === "linear" ? "</linearGradient>" : "</radialGradient>", `
`), e.join("");
  }
  toLive(r) {
    let { x1: t, y1: e, x2: i, y2: s, r1: o, r2: n } = this.coords, a = this.type === "linear" ? r.createLinearGradient(t, e, i, s) : r.createRadialGradient(t, e, o, i, s, n);
    return this.colorStops.forEach(({ color: l, offset: h }) => {
      a.addColorStop(h, l);
    }), a;
  }
  static async fromObject(r) {
    let { colorStops: t, gradientTransform: e } = r;
    return new this({
      ...r,
      colorStops: t ? t.map((i) => ({ ...i })) : void 0,
      gradientTransform: e ? [...e] : void 0
    });
  }
  static fromElement(r, t, e) {
    let i = jn(r), s = t._findCenterFromElement();
    return new this({
      id: r.getAttribute("id") || void 0,
      type: Pn(r),
      coords: Jl(r, {
        width: e.viewBoxWidth || e.width,
        height: e.viewBoxHeight || e.height
      }),
      colorStops: Kl(r, e.opacity),
      gradientUnits: i,
      gradientTransform: pi(r.getAttribute("gradientTransform") || ""),
      ...i === "pixels" ? {
        offsetX: t.width / 2 - s.x,
        offsetY: t.height / 2 - s.y
      } : {
        offsetX: 0,
        offsetY: 0
      }
    });
  }
};
f(cr, "type", "Gradient"), w.setClass(cr, "gradient"), w.setClass(cr, "linear"), w.setClass(cr, "radial");
var ri = class {
  get type() {
    return "pattern";
  }
  set type(r) {
    Xt("warn", "Setting type has no effect", r);
  }
  constructor(r) {
    f(this, "repeat", "repeat"), f(this, "offsetX", 0), f(this, "offsetY", 0), f(this, "crossOrigin", ""), this.id = $t(), Object.assign(this, r);
  }
  isImageSource() {
    return !!this.source && typeof this.source.src == "string";
  }
  isCanvasSource() {
    return !!this.source && !!this.source.toDataURL;
  }
  sourceToString() {
    return this.isImageSource() ? this.source.src : this.isCanvasSource() ? this.source.toDataURL() : "";
  }
  toLive(r) {
    return this.source && (!this.isImageSource() || this.source.complete && this.source.naturalWidth !== 0 && this.source.naturalHeight !== 0) ? r.createPattern(this.source, this.repeat) : null;
  }
  toObject(r = []) {
    let { repeat: t, crossOrigin: e } = this;
    return {
      ...re(this, r),
      type: "pattern",
      source: this.sourceToString(),
      repeat: t,
      crossOrigin: e,
      offsetX: F(this.offsetX, P.NUM_FRACTION_DIGITS),
      offsetY: F(this.offsetY, P.NUM_FRACTION_DIGITS),
      patternTransform: this.patternTransform ? [...this.patternTransform] : null
    };
  }
  toSVG({ width: r, height: t }) {
    let { source: e, repeat: i, id: s } = this, o = he(this.offsetX / r, 0), n = he(this.offsetY / t, 0), a = i === "repeat-y" || i === "no-repeat" ? 1 + Math.abs(o || 0) : he(e.width / r, 0), l = i === "repeat-x" || i === "no-repeat" ? 1 + Math.abs(n || 0) : he(e.height / t, 0);
    return [
      `<pattern id="SVGID_${M(s)}" x="${o}" y="${n}" width="${a}" height="${l}">`,
      `<image x="0" y="0" width="${e.width}" height="${e.height}" xlink:href="${M(this.sourceToString())}"></image>`,
      "</pattern>",
      ""
    ].join(`
`);
  }
  static async fromObject({ type: r, source: t, patternTransform: e, ...i }, s) {
    let o = await Je(t, {
      ...s,
      crossOrigin: i.crossOrigin
    });
    return new this({
      ...i,
      patternTransform: e && e.slice(0),
      source: o
    });
  }
};
f(ri, "type", "Pattern"), w.setClass(ri), w.setClass(ri, "pattern");
var Ql = class {
  constructor(r) {
    f(this, "color", "rgb(0, 0, 0)"), f(this, "width", 1), f(this, "shadow", null), f(this, "strokeLineCap", "round"), f(this, "strokeLineJoin", "round"), f(this, "strokeMiterLimit", 10), f(this, "strokeDashArray", null), f(this, "limitedToCanvasSize", !1), this.canvas = r;
  }
  _setBrushStyles(r) {
    r.strokeStyle = this.color, r.lineWidth = this.width, r.lineCap = this.strokeLineCap, r.miterLimit = this.strokeMiterLimit, r.lineJoin = this.strokeLineJoin, r.setLineDash(this.strokeDashArray || []);
  }
  _saveAndTransform(r) {
    let t = this.canvas.viewportTransform;
    r.save(), r.transform(t[0], t[1], t[2], t[3], t[4], t[5]);
  }
  needsFullRender() {
    return new et(this.color).getAlpha() < 1 || !!this.shadow;
  }
  _setShadow() {
    if (!this.shadow || !this.canvas) return;
    let r = this.canvas, t = this.shadow, e = r.contextTop, i = r.getZoom() * r.getRetinaScaling();
    e.shadowColor = t.color, e.shadowBlur = t.blur * i, e.shadowOffsetX = t.offsetX * i, e.shadowOffsetY = t.offsetY * i;
  }
  _resetShadow() {
    let r = this.canvas.contextTop;
    r.shadowColor = "", r.shadowBlur = r.shadowOffsetX = r.shadowOffsetY = 0;
  }
  _isOutSideCanvas(r) {
    return r.x < 0 || r.x > this.canvas.getWidth() || r.y < 0 || r.y > this.canvas.getHeight();
  }
}, Ot = class An extends N {
  constructor(t, { path: e, left: i, top: s, ...o } = {}) {
    super(), Object.assign(this, An.ownDefaults), this.setOptions(o), this._setPath(t || [], !0), typeof i == "number" && this.set("left", i), typeof s == "number" && this.set("top", s);
  }
  _setPath(t, e) {
    this.path = un(Array.isArray(t) ? t : vn(t)), this.setBoundingBox(e);
  }
  _findCenterFromElement() {
    let t = this._calcBoundsFromPath();
    return new v(t.left + t.width / 2, t.top + t.height / 2);
  }
  _renderPathCommands(t) {
    let e = -this.pathOffset.x, i = -this.pathOffset.y;
    t.beginPath();
    for (let s of this.path) switch (s[0]) {
      case "L":
        t.lineTo(s[1] + e, s[2] + i);
        break;
      case "M":
        t.moveTo(s[1] + e, s[2] + i);
        break;
      case "C":
        t.bezierCurveTo(s[1] + e, s[2] + i, s[3] + e, s[4] + i, s[5] + e, s[6] + i);
        break;
      case "Q":
        t.quadraticCurveTo(s[1] + e, s[2] + i, s[3] + e, s[4] + i);
        break;
      case "Z":
        t.closePath();
    }
  }
  _render(t) {
    this._renderPathCommands(t), this._renderPaintInOrder(t);
  }
  toString() {
    return `#<Path (${this.complexity()}): { "top": ${this.top}, "left": ${this.left} }>`;
  }
  toObject(t = []) {
    return {
      ...super.toObject(t),
      path: this.path.map((e) => e.slice())
    };
  }
  toDatalessObject(t = []) {
    let e = this.toObject(t);
    return this.sourcePath && (delete e.path, e.sourcePath = this.sourcePath), e;
  }
  _toSVG() {
    return [
      "<path ",
      "COMMON_PARTS",
      `d="${us(this.path, P.NUM_FRACTION_DIGITS)}" stroke-linecap="round" />
`
    ];
  }
  _getOffsetTransform() {
    let t = P.NUM_FRACTION_DIGITS;
    return ` translate(${F(-this.pathOffset.x, t)}, ${F(-this.pathOffset.y, t)})`;
  }
  toClipPathSVG(t) {
    let e = this._getOffsetTransform();
    return "	" + this._createBaseClipPathSVGMarkup(this._toSVG(), {
      reviver: t,
      additionalTransform: e
    });
  }
  toSVG(t) {
    let e = this._getOffsetTransform();
    return this._createBaseSVGMarkup(this._toSVG(), {
      reviver: t,
      additionalTransform: e
    });
  }
  complexity() {
    return this.path.length;
  }
  setDimensions() {
    this.setBoundingBox();
  }
  setBoundingBox(t) {
    let { width: e, height: i, pathOffset: s } = this._calcDimensions();
    this.set({
      width: e,
      height: i,
      pathOffset: s
    }), t && this.setPositionByOrigin(s, "center", "center");
  }
  _calcBoundsFromPath() {
    let t = [], e = 0, i = 0, s = 0, o = 0;
    for (let n of this.path) switch (n[0]) {
      case "L":
        s = n[1], o = n[2], t.push({
          x: e,
          y: i
        }, {
          x: s,
          y: o
        });
        break;
      case "M":
        s = n[1], o = n[2], e = s, i = o;
        break;
      case "C":
        t.push(...Si(s, o, n[1], n[2], n[3], n[4], n[5], n[6])), s = n[5], o = n[6];
        break;
      case "Q":
        t.push(...Si(s, o, n[1], n[2], n[1], n[2], n[3], n[4])), s = n[3], o = n[4];
        break;
      case "Z":
        s = e, o = i;
    }
    return St(t);
  }
  _calcDimensions() {
    let t = this._calcBoundsFromPath();
    return {
      ...t,
      pathOffset: new v(t.left + t.width / 2, t.top + t.height / 2)
    };
  }
  static fromObject(t) {
    return this._fromObject(t, { extraParam: "path" });
  }
  static async fromElement(t, e, i) {
    let { d: s, ...o } = At(t, this.ATTRIBUTE_NAMES, i);
    return new this(s, {
      ...o,
      ...e,
      left: void 0,
      top: void 0
    });
  }
};
f(Ot, "type", "Path"), f(Ot, "cacheProperties", [
  ...Pt,
  "path",
  "fillRule"
]), f(Ot, "ATTRIBUTE_NAMES", [...zt, "d"]), w.setClass(Ot), w.setSVGClass(Ot);
var Zl = class Ti extends Ql {
  constructor(t) {
    super(t), f(this, "decimate", 0.4), f(this, "drawStraightLine", !1), f(this, "straightLineKey", "shiftKey"), this._points = [], this._hasStraightLine = !1;
  }
  needsFullRender() {
    return super.needsFullRender() || this._hasStraightLine;
  }
  static drawSegment(t, e, i) {
    let s = e.midPointFrom(i);
    return t.quadraticCurveTo(e.x, e.y, s.x, s.y), s;
  }
  onMouseDown(t, { e }) {
    this.canvas._isMainEvent(e) && (this.drawStraightLine = !!this.straightLineKey && e[this.straightLineKey], this._prepareForDrawing(t), this._addPoint(t), this._render());
  }
  onMouseMove(t, { e }) {
    if (this.canvas._isMainEvent(e) && (this.drawStraightLine = !!this.straightLineKey && e[this.straightLineKey], (this.limitedToCanvasSize !== !0 || !this._isOutSideCanvas(t)) && this._addPoint(t) && this._points.length > 1)) if (this.needsFullRender()) this.canvas.clearContext(this.canvas.contextTop), this._render();
    else {
      let i = this._points, s = i.length, o = this.canvas.contextTop;
      this._saveAndTransform(o), this.oldEnd && (o.beginPath(), o.moveTo(this.oldEnd.x, this.oldEnd.y)), this.oldEnd = Ti.drawSegment(o, i[s - 2], i[s - 1]), o.stroke(), o.restore();
    }
  }
  onMouseUp({ e: t }) {
    return !this.canvas._isMainEvent(t) || (this.drawStraightLine = !1, this.oldEnd = void 0, this._finalizeAndAddPath(), !1);
  }
  _prepareForDrawing(t) {
    this._reset(), this._addPoint(t), this.canvas.contextTop.moveTo(t.x, t.y);
  }
  _addPoint(t) {
    return !(this._points.length > 1 && t.eq(this._points[this._points.length - 1])) && (this.drawStraightLine && this._points.length > 1 && (this._hasStraightLine = !0, this._points.pop()), this._points.push(t), !0);
  }
  _reset() {
    this._points = [], this._setBrushStyles(this.canvas.contextTop), this._setShadow(), this._hasStraightLine = !1;
  }
  _render(t = this.canvas.contextTop) {
    let e = this._points[0], i = this._points[1];
    if (this._saveAndTransform(t), t.beginPath(), this._points.length === 2 && e.x === i.x && e.y === i.y) {
      let s = this.width / 1e3;
      e.x -= s, i.x += s;
    }
    t.moveTo(e.x, e.y);
    for (let s = 1; s < this._points.length; s++) Ti.drawSegment(t, e, i), e = this._points[s], i = this._points[s + 1];
    t.lineTo(e.x, e.y), t.stroke(), t.restore();
  }
  convertPointsToSVGPath(t) {
    return yn(t, this.width / 1e3);
  }
  createPath(t) {
    let e = new Ot(t, {
      fill: null,
      stroke: this.color,
      strokeWidth: this.width,
      strokeLineCap: this.strokeLineCap,
      strokeMiterLimit: this.strokeMiterLimit,
      strokeLineJoin: this.strokeLineJoin,
      strokeDashArray: this.strokeDashArray
    });
    return this.shadow && (this.shadow.affectStroke = !0, e.shadow = new de(this.shadow)), e;
  }
  decimatePoints(t, e) {
    if (t.length <= 2) return t;
    let i, s = t[0], o = (e / this.canvas.getZoom()) ** 2, n = t.length - 1, a = [s];
    for (let l = 1; l < n - 1; l++) i = (s.x - t[l].x) ** 2 + (s.y - t[l].y) ** 2, i >= o && (s = t[l], a.push(s));
    return a.push(t[n]), a;
  }
  _finalizeAndAddPath() {
    this.canvas.contextTop.closePath(), this.decimate && (this._points = this.decimatePoints(this._points, this.decimate));
    let t = this.convertPointsToSVGPath(this._points);
    if ((function(i) {
      return us(i) === "M 0 0 Q 0 0 0 0 L 0 0";
    })(t)) return void this.canvas.requestRenderAll();
    let e = this.createPath(t);
    this.canvas.clearContext(this.canvas.contextTop), this.canvas.fire("before:path:created", { path: e }), this.canvas.add(e), this.canvas.requestRenderAll(), e.setCoords(), this._resetShadow(), this.canvas.fire("path:created", { path: e });
  }
}, Fn = [
  "radius",
  "startAngle",
  "endAngle",
  "counterClockwise"
], lt = class Oi extends N {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Oi.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, Oi.ownDefaults), this.setOptions(t);
  }
  _set(t, e) {
    return super._set(t, e), t === "radius" && this.setRadius(e), this;
  }
  _render(t) {
    t.beginPath(), t.arc(0, 0, this.radius, B(this.startAngle), B(this.endAngle), this.counterClockwise), this._renderPaintInOrder(t);
  }
  getRadiusX() {
    return this.get("radius") * this.get(Wt);
  }
  getRadiusY() {
    return this.get("radius") * this.get(Vt);
  }
  setRadius(t) {
    this.radius = t, this.set({
      width: 2 * t,
      height: 2 * t
    });
  }
  toObject(t = []) {
    return super.toObject([...Fn, ...t]);
  }
  _toSVG() {
    let { radius: t, startAngle: e, endAngle: i } = this, s = (i - e) % 360;
    if (s === 0) return [
      "<circle ",
      "COMMON_PARTS",
      'cx="0" cy="0" ',
      'r="',
      `${M(t)}`,
      `" />
`
    ];
    {
      let o = B(e), n = B(i), a = mt(o) * t, l = vt(o) * t, h = mt(n) * t, c = vt(n) * t;
      return [
        `<path d="M ${a} ${l} A ${t} ${t} 0 ${+(s > 180)} ${+!this.counterClockwise} ${h} ${c}" `,
        "COMMON_PARTS",
        ` />
`
      ];
    }
  }
  static async fromElement(t, e, i) {
    let { left: s = 0, top: o = 0, radius: n = 0, ...a } = At(t, this.ATTRIBUTE_NAMES, i);
    return new this({
      ...a,
      radius: n,
      left: s - n,
      top: o - n
    });
  }
  static fromObject(t) {
    return super._fromObject(t);
  }
};
f(lt, "type", "Circle"), f(lt, "cacheProperties", [...Pt, ...Fn]), f(lt, "ownDefaults", {
  radius: 0,
  startAngle: 0,
  endAngle: 360,
  counterClockwise: !1
}), f(lt, "ATTRIBUTE_NAMES", [
  "cx",
  "cy",
  "r",
  ...zt
]), w.setClass(lt), w.setSVGClass(lt);
var ki = [
  "x1",
  "x2",
  "y1",
  "y2"
], kt = class Ln extends N {
  constructor([t, e, i, s] = [
    0,
    0,
    0,
    0
  ], o = {}) {
    super(), Object.assign(this, Ln.ownDefaults), this.setOptions(o), this.x1 = t, this.x2 = i, this.y1 = e, this.y2 = s, this._setWidthHeight();
    let { left: n, top: a } = o;
    typeof n == "number" && this.set("left", n), typeof a == "number" && this.set("top", a);
  }
  _setWidthHeight() {
    let { x1: t, y1: e, x2: i, y2: s } = this;
    this.width = Math.abs(i - t), this.height = Math.abs(s - e);
    let { left: o, top: n, width: a, height: l } = St([{
      x: t,
      y: e
    }, {
      x: i,
      y: s
    }]), h = new v(o + a / 2, n + l / 2);
    this.setPositionByOrigin(h, L, L);
  }
  _set(t, e) {
    return super._set(t, e), ki.includes(t) && this._setWidthHeight(), this;
  }
  _render(t) {
    t.beginPath();
    let e = this.calcLinePoints();
    t.moveTo(e.x1, e.y1), t.lineTo(e.x2, e.y2), t.lineWidth = this.strokeWidth;
    let i = t.strokeStyle;
    var s;
    ht(this.stroke) ? t.strokeStyle = this.stroke.toLive(t) : t.strokeStyle = (s = this.stroke) == null ? t.fillStyle : s, this.stroke && this._renderStroke(t), t.strokeStyle = i;
  }
  _findCenterFromElement() {
    return new v((this.x1 + this.x2) / 2, (this.y1 + this.y2) / 2);
  }
  toObject(t = []) {
    return {
      ...super.toObject(t),
      ...this.calcLinePoints()
    };
  }
  _getNonTransformedDimensions() {
    let t = super._getNonTransformedDimensions();
    return this.strokeLineCap === "butt" && (this.width === 0 && (t.y -= this.strokeWidth), this.height === 0 && (t.x -= this.strokeWidth)), t;
  }
  calcLinePoints() {
    let { x1: t, x2: e, y1: i, y2: s, width: o, height: n } = this, a = t <= e ? -0.5 : 0.5, l = i <= s ? -0.5 : 0.5;
    return {
      x1: a * o,
      x2: a * -o,
      y1: l * n,
      y2: l * -n
    };
  }
  _toSVG() {
    let { x1: t, x2: e, y1: i, y2: s } = this.calcLinePoints();
    return [
      "<line ",
      "COMMON_PARTS",
      `x1="${t}" y1="${i}" x2="${e}" y2="${s}" />
`
    ];
  }
  static async fromElement(t, e, i) {
    let { x1: s = 0, y1: o = 0, x2: n = 0, y2: a = 0, ...l } = At(t, this.ATTRIBUTE_NAMES, i);
    return new this([
      s,
      o,
      n,
      a
    ], l);
  }
  static fromObject({ x1: t, y1: e, x2: i, y2: s, ...o }) {
    return this._fromObject({
      ...o,
      points: [
        t,
        e,
        i,
        s
      ]
    }, { extraParam: "points" });
  }
};
f(kt, "type", "Line"), f(kt, "cacheProperties", [...Pt, ...ki]), f(kt, "ATTRIBUTE_NAMES", zt.concat(ki)), w.setClass(kt), w.setSVGClass(kt);
var ur = class Mi extends N {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Mi.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, Mi.ownDefaults), this.setOptions(t);
  }
  _render(t) {
    let e = this.width / 2, i = this.height / 2;
    t.beginPath(), t.moveTo(-e, i), t.lineTo(0, -i), t.lineTo(e, i), t.closePath(), this._renderPaintInOrder(t);
  }
  _toSVG() {
    let t = this.width / 2, e = this.height / 2;
    return [
      "<polygon ",
      "COMMON_PARTS",
      'points="',
      `${-t} ${e},0 ${-e},${t} ${e}`,
      '" />'
    ];
  }
};
f(ur, "type", "Triangle"), f(ur, "ownDefaults", {
  width: 100,
  height: 100
}), w.setClass(ur), w.setSVGClass(ur);
var Rn = ["rx", "ry"], ae = class Di extends N {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Di.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, Di.ownDefaults), this.setOptions(t);
  }
  _set(t, e) {
    switch (super._set(t, e), t) {
      case "rx":
        this.rx = e, this.set("width", 2 * e);
        break;
      case "ry":
        this.ry = e, this.set("height", 2 * e);
    }
    return this;
  }
  getRx() {
    return this.get("rx") * this.get(Wt);
  }
  getRy() {
    return this.get("ry") * this.get(Vt);
  }
  toObject(t = []) {
    return super.toObject([...Rn, ...t]);
  }
  _toSVG() {
    return [
      "<ellipse ",
      "COMMON_PARTS",
      `cx="0" cy="0" rx="${M(this.rx)}" ry="${M(this.ry)}" />
`
    ];
  }
  _render(t) {
    t.beginPath(), t.save(), t.transform(1, 0, 0, this.ry / this.rx, 0, 0), t.arc(0, 0, this.rx, 0, pt, !1), t.restore(), this._renderPaintInOrder(t);
  }
  static async fromElement(t, e, i) {
    let s = At(t, this.ATTRIBUTE_NAMES, i);
    return s.left = (s.left || 0) - s.rx, s.top = (s.top || 0) - s.ry, new this(s);
  }
};
f(ae, "type", "Ellipse"), f(ae, "cacheProperties", [...Pt, ...Rn]), f(ae, "ownDefaults", {
  rx: 0,
  ry: 0
}), f(ae, "ATTRIBUTE_NAMES", [
  ...zt,
  "cx",
  "cy",
  "rx",
  "ry"
]), w.setClass(ae), w.setSVGClass(ae);
var In = { exactBoundingBox: !1 }, It = class Ei extends N {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Ei.ownDefaults
    };
  }
  constructor(t = [], e = {}) {
    super(), f(this, "strokeDiff", void 0), Object.assign(this, Ei.ownDefaults), this.setOptions(e), this.points = t;
    let { left: i, top: s } = e;
    this.initialized = !0, this.setBoundingBox(!0), typeof i == "number" && this.set("left", i), typeof s == "number" && this.set("top", s);
  }
  isOpen() {
    return !0;
  }
  _projectStrokeOnPoints(t) {
    return rn(this.points, t, this.isOpen());
  }
  _calcDimensions(t) {
    t = {
      scaleX: this.scaleX,
      scaleY: this.scaleY,
      skewX: this.skewX,
      skewY: this.skewY,
      strokeLineCap: this.strokeLineCap,
      strokeLineJoin: this.strokeLineJoin,
      strokeMiterLimit: this.strokeMiterLimit,
      strokeUniform: this.strokeUniform,
      strokeWidth: this.strokeWidth,
      ...t || {}
    };
    let e = this.exactBoundingBox ? this._projectStrokeOnPoints(t).map((h) => h.projectedPoint) : this.points;
    if (e.length === 0) return {
      left: 0,
      top: 0,
      width: 0,
      height: 0,
      pathOffset: new v(),
      strokeOffset: new v(),
      strokeDiff: new v()
    };
    let i = St(e), s = sr({
      ...t,
      scaleX: 1,
      scaleY: 1
    }), o = St(this.points.map((h) => U(h, s, !0))), n = new v(this.scaleX, this.scaleY), a = i.left + i.width / 2, l = i.top + i.height / 2;
    return this.exactBoundingBox && (a -= l * Math.tan(B(this.skewX)), l -= a * Math.tan(B(this.skewY))), {
      ...i,
      pathOffset: new v(a, l),
      strokeOffset: new v(o.left, o.top).subtract(new v(i.left, i.top)).multiply(n),
      strokeDiff: new v(i.width, i.height).subtract(new v(o.width, o.height)).multiply(n)
    };
  }
  _findCenterFromElement() {
    let t = St(this.points);
    return new v(t.left + t.width / 2, t.top + t.height / 2);
  }
  setDimensions() {
    this.setBoundingBox();
  }
  setBoundingBox(t) {
    let { left: e, top: i, width: s, height: o, pathOffset: n, strokeOffset: a, strokeDiff: l } = this._calcDimensions();
    this.set({
      width: s,
      height: o,
      pathOffset: n,
      strokeOffset: a,
      strokeDiff: l
    }), t && this.setPositionByOrigin(new v(e + s / 2, i + o / 2), "center", "center");
  }
  isStrokeAccountedForInDimensions() {
    return this.exactBoundingBox;
  }
  _getNonTransformedDimensions() {
    return this.exactBoundingBox ? new v(this.width, this.height) : super._getNonTransformedDimensions();
  }
  _getTransformedDimensions(t = {}) {
    if (this.exactBoundingBox) {
      let n;
      if (Object.keys(t).some((a) => this.strokeUniform || this.constructor.layoutProperties.includes(a))) {
        var e, i;
        let { width: a, height: l } = this._calcDimensions(t);
        n = new v((e = t.width) == null ? a : e, (i = t.height) == null ? l : i);
      } else {
        var s, o;
        n = new v((s = t.width) == null ? this.width : s, (o = t.height) == null ? this.height : o);
      }
      return n.multiply(new v(t.scaleX || this.scaleX, t.scaleY || this.scaleY));
    }
    return super._getTransformedDimensions(t);
  }
  _set(t, e) {
    let i = this.initialized && this[t] !== e, s = super._set(t, e);
    return this.exactBoundingBox && i && ((t === "scaleX" || t === "scaleY") && this.strokeUniform && this.constructor.layoutProperties.includes("strokeUniform") || this.constructor.layoutProperties.includes(t)) && this.setDimensions(), s;
  }
  toObject(t = []) {
    return {
      ...super.toObject(t),
      points: this.points.map(({ x: e, y: i }) => ({
        x: e,
        y: i
      }))
    };
  }
  _toSVG() {
    let t = this.pathOffset.x, e = this.pathOffset.y, i = P.NUM_FRACTION_DIGITS, s = this.points.map(({ x: o, y: n }) => `${F(o - t, i)},${F(n - e, i)}`).join(" ");
    return [
      `<${M(this.constructor.type).toLowerCase()} `,
      "COMMON_PARTS",
      `points="${s}" />
`
    ];
  }
  _render(t) {
    let e = this.points.length, i = this.pathOffset.x, s = this.pathOffset.y;
    if (e && !isNaN(this.points[e - 1].y)) {
      t.beginPath(), t.moveTo(this.points[0].x - i, this.points[0].y - s);
      for (let o = 0; o < e; o++) {
        let n = this.points[o];
        t.lineTo(n.x - i, n.y - s);
      }
      !this.isOpen() && t.closePath(), this._renderPaintInOrder(t);
    }
  }
  complexity() {
    return this.points.length;
  }
  static async fromElement(t, e, i) {
    let s = (function(l) {
      if (!l) return [];
      let h = l.replace(/,/g, " ").trim().split(/\s+/), c = [];
      for (let u = 0; u < h.length; u += 2) c.push({
        x: parseFloat(h[u]),
        y: parseFloat(h[u + 1])
      });
      return c;
    })(t.getAttribute("points")), { left: o, top: n, ...a } = At(t, this.ATTRIBUTE_NAMES, i);
    return new this(s, {
      ...a,
      ...e
    });
  }
  static fromObject(t) {
    return this._fromObject(t, { extraParam: "points" });
  }
};
f(It, "ownDefaults", In), f(It, "type", "Polyline"), f(It, "layoutProperties", [
  Se,
  Ce,
  "strokeLineCap",
  "strokeLineJoin",
  "strokeMiterLimit",
  "strokeWidth",
  "strokeUniform",
  "points"
]), f(It, "cacheProperties", [...Pt, "points"]), f(It, "ATTRIBUTE_NAMES", [...zt]), w.setClass(It), w.setSVGClass(It);
var dr = class extends It {
  isOpen() {
    return !1;
  }
};
f(dr, "ownDefaults", In), f(dr, "type", "Polygon"), w.setClass(dr), w.setSVGClass(dr);
var Bn = class extends N {
  isEmptyStyles(r) {
    if (!this.styles || r !== void 0 && !this.styles[r]) return !0;
    let t = r === void 0 ? this.styles : { line: this.styles[r] };
    for (let e in t) for (let i in t[e]) for (let s in t[e][i]) return !1;
    return !0;
  }
  styleHas(r, t) {
    if (!this.styles || t !== void 0 && !this.styles[t]) return !1;
    let e = t === void 0 ? this.styles : { 0: this.styles[t] };
    for (let i in e) for (let s in e[i]) if (e[i][s][r] !== void 0) return !0;
    return !1;
  }
  cleanStyle(r) {
    if (!this.styles) return !1;
    let t = this.styles, e, i, s = 0, o = !0, n = 0;
    for (let a in t) {
      e = 0;
      for (let l in t[a]) {
        let h = t[a][l] || {};
        s++, h[r] === void 0 ? o = !1 : (i ? h[r] !== i && (o = !1) : i = h[r], h[r] === this[r] && delete h[r]), Object.keys(h).length === 0 ? delete t[a][l] : e++;
      }
      e === 0 && delete t[a];
    }
    for (let a = 0; a < this._textLines.length; a++) n += this._textLines[a].length;
    o && s === n && (this[r] = i, this.removeStyle(r));
  }
  removeStyle(r) {
    if (!this.styles) return;
    let t = this.styles, e, i, s;
    for (i in t) {
      for (s in e = t[i], e) delete e[s][r], Object.keys(e[s]).length === 0 && delete e[s];
      Object.keys(e).length === 0 && delete t[i];
    }
  }
  _extendStyles(r, t) {
    let { lineIndex: e, charIndex: i } = this.get2DCursorLocation(r);
    this._getLineStyle(e) || this._setLineStyle(e);
    let s = Gi({
      ...this._getStyleDeclaration(e, i),
      ...t
    }, (o) => o !== void 0);
    this._setStyleDeclaration(e, i, s);
  }
  getSelectionStyles(r, t, e) {
    let i = [];
    for (let s = r; s < (t || r); s++) i.push(this.getStyleAtPosition(s, e));
    return i;
  }
  getStyleAtPosition(r, t) {
    let { lineIndex: e, charIndex: i } = this.get2DCursorLocation(r);
    return t ? this.getCompleteStyleDeclaration(e, i) : this._getStyleDeclaration(e, i);
  }
  setSelectionStyles(r, t, e) {
    for (let i = t; i < (e || t); i++) this._extendStyles(i, r);
    this._forceClearCache = !0;
  }
  _getStyleDeclaration(r, t) {
    var e;
    let i = this.styles && this.styles[r];
    return i && (e = i[t]) != null ? e : {};
  }
  getCompleteStyleDeclaration(r, t) {
    return {
      ...re(this, this.constructor._styleProperties),
      ...this._getStyleDeclaration(r, t)
    };
  }
  _setStyleDeclaration(r, t, e) {
    this.styles[r][t] = e;
  }
  _deleteStyleDeclaration(r, t) {
    delete this.styles[r][t];
  }
  _getLineStyle(r) {
    return !!this.styles[r];
  }
  _setLineStyle(r) {
    this.styles[r] = {};
  }
  _deleteLineStyle(r) {
    delete this.styles[r];
  }
};
f(Bn, "_styleProperties", ua);
var th = /  +/g, eh = /"/g;
function ii(r, t, e, i, s) {
  return `		${((o, { left: n, top: a, width: l, height: h }, c = P.NUM_FRACTION_DIGITS) => {
    let u = er(tt, o, !1), [d, g, p, m] = [
      n,
      a,
      l,
      h
    ].map((y) => F(y, c));
    return `<rect ${u} x="${d}" y="${g}" width="${p}" height="${m}"></rect>`;
  })(r, {
    left: t,
    top: e,
    width: i,
    height: s
  })}
`;
}
var si, xt = class je extends Bn {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...je.ownDefaults
    };
  }
  constructor(t, e) {
    super(), f(this, "__charBounds", []), Object.assign(this, je.ownDefaults), this.setOptions(e), this.styles || (this.styles = {}), this.text = t, this.initialized = !0, this.path && this.setPathInfo(), this.initDimensions(), this.setCoords();
  }
  setPathInfo() {
    let t = this.path;
    t && (t.segmentsInfo = cs(t.path));
  }
  _splitText() {
    let t = this._splitTextIntoLines(this.text);
    return this.textLines = t.lines, this._textLines = t.graphemeLines, this._unwrappedTextLines = t._unwrappedLines, this._text = t.graphemeText, t;
  }
  initDimensions() {
    this._splitText(), this._clearCache(), this.dirty = !0, this.path ? (this.width = this.path.width, this.height = this.path.height) : (this.width = this.calcTextWidth() || this.cursorWidth || this.MIN_TEXT_WIDTH, this.height = this.calcTextHeight()), this.textAlign.includes("justify") && this.enlargeSpaces();
  }
  enlargeSpaces() {
    let t, e, i, s, o, n, a;
    for (let l = 0, h = this._textLines.length; l < h; l++) if ((this.textAlign === "justify" || l !== h - 1 && !this.isEndOfWrapping(l)) && (s = 0, o = this._textLines[l], e = this.getLineWidth(l), e < this.width && (a = this.textLines[l].match(this._reSpacesAndTabs)))) {
      i = a.length, t = (this.width - e) / i;
      for (let c = 0; c <= o.length; c++) n = this.__charBounds[l][c], this._reSpaceAndTab.test(o[c]) ? (n.width += t, n.kernedWidth += t, n.left += s, s += t) : n.left += s;
    }
  }
  isEndOfWrapping(t) {
    return t === this._textLines.length - 1;
  }
  missingNewlineOffset(t) {
    return 1;
  }
  get2DCursorLocation(t, e) {
    let i = e ? this._unwrappedTextLines : this._textLines, s;
    for (s = 0; s < i.length; s++) {
      if (t <= i[s].length) return {
        lineIndex: s,
        charIndex: t
      };
      t -= i[s].length + this.missingNewlineOffset(s, e);
    }
    return {
      lineIndex: s - 1,
      charIndex: i[s - 1].length < t ? i[s - 1].length : t
    };
  }
  toString() {
    return `#<Text (${this.complexity()}): { "text": "${this.text}", "fontFamily": "${this.fontFamily}" }>`;
  }
  _getCacheCanvasDimensions() {
    let t = super._getCacheCanvasDimensions(), e = this.fontSize;
    return t.width += e * t.zoomX, t.height += e * t.zoomY, t;
  }
  _render(t) {
    let e = this.path;
    e && !e.isNotVisible() && e._render(t), this._setTextStyles(t), this._renderTextLinesBackground(t), this._renderTextDecoration(t, "underline"), this._renderText(t), this._renderTextDecoration(t, "overline"), this._renderTextDecoration(t, "linethrough");
  }
  _renderText(t) {
    this.paintFirst === "stroke" ? (this._renderTextStroke(t), this._renderTextFill(t)) : (this._renderTextFill(t), this._renderTextStroke(t));
  }
  _setTextStyles(t, e, i) {
    if (t.textBaseline = "alphabetic", this.path) switch (this.pathAlign) {
      case L:
        t.textBaseline = "middle";
        break;
      case "ascender":
        t.textBaseline = "top";
        break;
      case "descender":
        t.textBaseline = Ns;
    }
    t.font = this._getFontDeclaration(e, i);
  }
  calcTextWidth() {
    let t = this.getLineWidth(0);
    for (let e = 1, i = this._textLines.length; e < i; e++) {
      let s = this.getLineWidth(e);
      s > t && (t = s);
    }
    return t;
  }
  _renderTextLine(t, e, i, s, o, n) {
    this._renderChars(t, e, i, s, o, n);
  }
  _renderTextLinesBackground(t) {
    if (!this.textBackgroundColor && !this.styleHas("textBackgroundColor")) return;
    let e = t.fillStyle, i = this._getLeftOffset(), s = this._getTopOffset();
    for (let o = 0, n = this._textLines.length; o < n; o++) {
      let a = this.getHeightOfLine(o);
      if (!this.textBackgroundColor && !this.styleHas("textBackgroundColor", o)) {
        s += a;
        continue;
      }
      let l = this._textLines[o].length, h = this._getLineLeftOffset(o), c, u, d = 0, g = 0, p = this.getValueOfPropertyAt(o, 0, "textBackgroundColor"), m = this.getHeightOfLineImpl(o);
      for (let y = 0; y < l; y++) {
        let x = this.__charBounds[o][y];
        u = this.getValueOfPropertyAt(o, y, "textBackgroundColor"), this.path ? (t.save(), t.translate(x.renderLeft, x.renderTop), t.rotate(x.angle), t.fillStyle = u, u && t.fillRect(-x.width / 2, -m * (1 - this._fontSizeFraction), x.width, m), t.restore()) : u === p ? d += x.kernedWidth : (c = i + h + g, this.direction === "rtl" && (c = this.width - c - d), t.fillStyle = p, p && t.fillRect(c, s, d, m), g = x.left, d = x.width, p = u);
      }
      u && !this.path && (c = i + h + g, this.direction === "rtl" && (c = this.width - c - d), t.fillStyle = u, t.fillRect(c, s, d, m)), s += a;
    }
    t.fillStyle = e, this._removeShadow(t);
  }
  _measureChar(t, e, i, s) {
    let o = qe.getFontCache(e), n = this._getFontDeclaration(e), a = i ? i + t : t, l = i && n === this._getFontDeclaration(s), h = e.fontSize / this.CACHE_FONT_SIZE, c, u, d, g;
    if (i && o.has(i) && (d = o.get(i)), o.has(t) && (g = c = o.get(t)), l && o.has(a) && (u = o.get(a), g = u - d), c === void 0 || d === void 0 || u === void 0) {
      let p = (si || (si = nt({
        width: 0,
        height: 0
      }).getContext("2d")), si);
      this._setTextStyles(p, e, !0), c === void 0 && (g = c = p.measureText(t).width, o.set(t, c)), d === void 0 && l && i && (d = p.measureText(i).width, o.set(i, d)), l && u === void 0 && (u = p.measureText(a).width, o.set(a, u), g = u - d);
    }
    return {
      width: c * h,
      kernedWidth: g * h
    };
  }
  getHeightOfChar(t, e) {
    return this.getValueOfPropertyAt(t, e, "fontSize");
  }
  measureLine(t) {
    let e = this._measureLine(t);
    return this.charSpacing !== 0 && (e.width -= this._getWidthOfCharSpacing()), e.width < 0 && (e.width = 0), e;
  }
  _measureLine(t) {
    let e, i, s = 0, o = this.pathSide === gt, n = this.path, a = this._textLines[t], l = a.length, h = Array(l);
    this.__charBounds[t] = h;
    for (let c = 0; c < l; c++) {
      let u = a[c];
      i = this._getGraphemeBox(u, t, c, e), h[c] = i, s += i.kernedWidth, e = u;
    }
    if (h[l] = {
      left: i ? i.left + i.width : 0,
      width: 0,
      kernedWidth: 0,
      height: this.fontSize,
      deltaY: 0
    }, n && n.segmentsInfo) {
      let c = 0, u = n.segmentsInfo[n.segmentsInfo.length - 1].length;
      switch (this.textAlign) {
        case V:
          c = o ? u - s : 0;
          break;
        case L:
          c = (u - s) / 2;
          break;
        case gt:
          c = o ? 0 : u - s;
      }
      c += this.pathStartOffset * (o ? -1 : 1);
      for (let d = o ? l - 1 : 0; o ? d >= 0 : d < l; o ? d-- : d++) i = h[d], c > u ? c %= u : c < 0 && (c += u), this._setGraphemeOnPath(c, i), c += i.kernedWidth;
    }
    return {
      width: s,
      numOfSpaces: 0
    };
  }
  _setGraphemeOnPath(t, e) {
    let i = t + e.kernedWidth / 2, s = this.path, o = mn(s.path, i, s.segmentsInfo);
    e.renderLeft = o.x - s.pathOffset.x, e.renderTop = o.y - s.pathOffset.y, e.angle = o.angle + (this.pathSide === "right" ? Math.PI : 0);
  }
  _getGraphemeBox(t, e, i, s, o) {
    let n = this.getCompleteStyleDeclaration(e, i), a = s ? this.getCompleteStyleDeclaration(e, i - 1) : {}, l = this._measureChar(t, n, s, a), h, c = l.kernedWidth, u = l.width;
    this.charSpacing !== 0 && (h = this._getWidthOfCharSpacing(), u += h, c += h);
    let d = {
      width: u,
      left: 0,
      height: n.fontSize,
      kernedWidth: c,
      deltaY: n.deltaY
    };
    if (i > 0 && !o) {
      let g = this.__charBounds[e][i - 1];
      d.left = g.left + g.width + l.kernedWidth - l.width;
    }
    return d;
  }
  getHeightOfLineImpl(t) {
    let e = this.__lineHeights;
    if (e[t]) return e[t];
    let i = this.getHeightOfChar(t, 0);
    for (let s = 1, o = this._textLines[t].length; s < o; s++) i = Math.max(this.getHeightOfChar(t, s), i);
    return e[t] = i * this._fontSizeMult;
  }
  getHeightOfLine(t) {
    return this.getHeightOfLineImpl(t) * this.lineHeight;
  }
  calcTextHeight() {
    let t = 0;
    for (let e = 0, i = this._textLines.length; e < i; e++) t += e === i - 1 ? this.getHeightOfLineImpl(e) : this.getHeightOfLine(e);
    return t;
  }
  _getLeftOffset() {
    return this.direction === "ltr" ? -this.width / 2 : this.width / 2;
  }
  _getTopOffset() {
    return -this.height / 2;
  }
  _renderTextCommon(t, e) {
    t.save();
    let i = 0, s = this._getLeftOffset(), o = this._getTopOffset();
    for (let n = 0, a = this._textLines.length; n < a; n++) this._renderTextLine(e, t, this._textLines[n], s + this._getLineLeftOffset(n), o + i + this.getHeightOfLineImpl(n), n), i += this.getHeightOfLine(n);
    t.restore();
  }
  _renderTextFill(t) {
    (this.fill || this.styleHas("fill")) && this._renderTextCommon(t, "fillText");
  }
  _renderTextStroke(t) {
    (this.stroke && this.strokeWidth !== 0 || !this.isEmptyStyles()) && (this.shadow && !this.shadow.affectStroke && this._removeShadow(t), t.save(), this._setLineDash(t, this.strokeDashArray), t.beginPath(), this._renderTextCommon(t, "strokeText"), t.closePath(), t.restore());
  }
  _renderChars(t, e, i, s, o, n) {
    let a = this.textAlign.includes(ts), l = this.path, h = !a && this.charSpacing === 0 && this.isEmptyStyles(n) && !l, c = this.direction === "ltr", u = this.direction === "ltr" ? 1 : -1, d = e.direction, g, p, m, y, x, _ = "", S = 0;
    if (e.save(), d !== this.direction && (e.canvas.setAttribute("dir", c ? "ltr" : "rtl"), e.direction = c ? "ltr" : "rtl", e.textAlign = c ? V : gt), o -= this.getHeightOfLineImpl(n) * this._fontSizeFraction, h) return this._renderChar(t, e, n, 0, i.join(""), s, o), void e.restore();
    for (let C = 0, b = i.length - 1; C <= b; C++) y = C === b || this.charSpacing || l, _ += i[C], m = this.__charBounds[n][C], S === 0 ? (s += u * (m.kernedWidth - m.width), S += m.width) : S += m.kernedWidth, a && !y && this._reSpaceAndTab.test(i[C]) && (y = !0), y || (g = g || this.getCompleteStyleDeclaration(n, C), p = this.getCompleteStyleDeclaration(n, C + 1), y = Nr(g, p, !1)), y && (l ? (e.save(), e.translate(m.renderLeft, m.renderTop), e.rotate(m.angle), this._renderChar(t, e, n, C, _, -S / 2, 0), e.restore()) : (x = s, this._renderChar(t, e, n, C, _, x, o)), _ = "", g = p, s += u * S, S = 0);
    e.restore();
  }
  _applyPatternGradientTransformText(t) {
    let e = this.width + this.strokeWidth, i = this.height + this.strokeWidth, s = nt({
      width: e,
      height: i
    }), o = s.getContext("2d");
    return s.width = e, s.height = i, o.beginPath(), o.moveTo(0, 0), o.lineTo(e, 0), o.lineTo(e, i), o.lineTo(0, i), o.closePath(), o.translate(e / 2, i / 2), o.fillStyle = t.toLive(o), this._applyPatternGradientTransform(o, t), o.fill(), o.createPattern(s, "no-repeat");
  }
  handleFiller(t, e, i) {
    let s, o;
    return ht(i) ? i.gradientUnits === "percentage" || i.gradientTransform || i.patternTransform ? (s = -this.width / 2, o = -this.height / 2, t.translate(s, o), t[e] = this._applyPatternGradientTransformText(i), {
      offsetX: s,
      offsetY: o
    }) : (t[e] = i.toLive(t), this._applyPatternGradientTransform(t, i)) : (t[e] = i, {
      offsetX: 0,
      offsetY: 0
    });
  }
  _setStrokeStyles(t, { stroke: e, strokeWidth: i }) {
    return t.lineWidth = i, t.lineCap = this.strokeLineCap, t.lineDashOffset = this.strokeDashOffset, t.lineJoin = this.strokeLineJoin, t.miterLimit = this.strokeMiterLimit, this.handleFiller(t, "strokeStyle", e);
  }
  _setFillStyles(t, { fill: e }) {
    return this.handleFiller(t, "fillStyle", e);
  }
  _renderChar(t, e, i, s, o, n, a) {
    let l = this._getStyleDeclaration(i, s), h = this.getCompleteStyleDeclaration(i, s), c = t === "fillText" && h.fill, u = t === "strokeText" && h.stroke && h.strokeWidth;
    if (u || c) {
      if (e.save(), e.font = this._getFontDeclaration(h), l.textBackgroundColor && this._removeShadow(e), l.deltaY && (a += l.deltaY), c) {
        let d = this._setFillStyles(e, h);
        e.fillText(o, n - d.offsetX, a - d.offsetY);
      }
      if (u) {
        let d = this._setStrokeStyles(e, h);
        e.strokeText(o, n - d.offsetX, a - d.offsetY);
      }
      e.restore();
    }
  }
  setSuperscript(t, e) {
    this._setScript(t, e, this.superscript);
  }
  setSubscript(t, e) {
    this._setScript(t, e, this.subscript);
  }
  _setScript(t, e, i) {
    let s = this.get2DCursorLocation(t, !0), o = this.getValueOfPropertyAt(s.lineIndex, s.charIndex, "fontSize"), n = this.getValueOfPropertyAt(s.lineIndex, s.charIndex, "deltaY"), a = {
      fontSize: o * i.size,
      deltaY: n + o * i.baseline
    };
    this.setSelectionStyles(a, t, e);
  }
  _getLineLeftOffset(t) {
    let e = this.getLineWidth(t), i = this.width - e, s = this.textAlign, o = this.direction, n = this.isEndOfWrapping(t), a = 0;
    return s === "justify" || s === "justify-center" && !n || s === "justify-right" && !n || s === "justify-left" && !n ? 0 : (s === "center" && (a = i / 2), s === "right" && (a = i), s === "justify-center" && (a = i / 2), s === "justify-right" && (a = i), o === "rtl" && (s === "right" || s === "justify-right" ? a = 0 : s === "left" || s === "justify-left" ? a = -i : s !== "center" && s !== "justify-center" || (a = -i / 2)), a);
  }
  _clearCache() {
    this._forceClearCache = !1, this.__lineWidths = [], this.__lineHeights = [], this.__charBounds = [];
  }
  getLineWidth(t) {
    if (this.__lineWidths[t] !== void 0) return this.__lineWidths[t];
    let { width: e } = this.measureLine(t);
    return this.__lineWidths[t] = e, e;
  }
  _getWidthOfCharSpacing() {
    return this.charSpacing === 0 ? 0 : this.fontSize * this.charSpacing / 1e3;
  }
  getValueOfPropertyAt(t, e, i) {
    var s;
    return (s = this._getStyleDeclaration(t, e)[i]) == null ? this[i] : s;
  }
  _renderTextDecoration(t, e) {
    if (!this[e] && !this.styleHas(e)) return;
    let i = this._getTopOffset(), s = this._getLeftOffset(), o = this.path, n = this._getWidthOfCharSpacing(), a = e === "linethrough" ? 0.5 : +(e === "overline"), l = this.offsets[e];
    for (let h = 0, c = this._textLines.length; h < c; h++) {
      let u = this.getHeightOfLine(h);
      if (!this[e] && !this.styleHas(e, h)) {
        i += u;
        continue;
      }
      let d = this._textLines[h], g = u / this.lineHeight, p = this._getLineLeftOffset(h), m, y = 0, x = 0, _ = this.getValueOfPropertyAt(h, 0, e), S = this.getValueOfPropertyAt(h, 0, tt), C = this.getValueOfPropertyAt(h, 0, "textDecorationColor") || S, b = this.getValueOfPropertyAt(h, 0, xe), O = _, T = C, k = b, D = i + g * (1 - this._fontSizeFraction), I = this.getHeightOfChar(h, 0), j = this.getValueOfPropertyAt(h, 0, "deltaY");
      for (let X = 0, z = d.length; X < z; X++) {
        let Y = this.__charBounds[h][X];
        O = this.getValueOfPropertyAt(h, X, e), m = this.getValueOfPropertyAt(h, X, tt), T = this.getValueOfPropertyAt(h, X, "textDecorationColor") || m, k = this.getValueOfPropertyAt(h, X, xe);
        let q = this.getHeightOfChar(h, X), rt = this.getValueOfPropertyAt(h, X, "deltaY");
        if (o && O && m) {
          let A = this.fontSize * k / 1e3;
          t.save(), t.fillStyle = T, t.translate(Y.renderLeft, Y.renderTop), t.rotate(Y.angle), t.fillRect(-Y.kernedWidth / 2, l * q + rt - a * A, Y.kernedWidth, A), t.restore();
        } else if ((O !== _ || m !== S || T !== C || q !== I || k !== b || rt !== j) && x > 0) {
          let A = this.fontSize * b / 1e3, yt = s + p + y;
          this.direction === "rtl" && (yt = this.width - yt - x), _ && C && b && (t.fillStyle = C, t.fillRect(yt, D + l * I + j - a * A, x, A)), y = Y.left, x = Y.width, _ = O, C = T, b = k, S = m, I = q, j = rt;
        } else x += Y.kernedWidth;
      }
      let E = s + p + y;
      this.direction === "rtl" && (E = this.width - E - x), t.fillStyle = T;
      let R = this.fontSize * k / 1e3;
      O && T && k && t.fillRect(E, D + l * I + j - a * R, x - n, R), i += u;
    }
    this._removeShadow(t);
  }
  _getFontDeclaration({ fontFamily: t = this.fontFamily, fontStyle: e = this.fontStyle, fontWeight: i = this.fontWeight, fontSize: s = this.fontSize } = {}, o) {
    let n = t.includes("'") || t.includes('"') || t.includes(",") || je.genericFonts.includes(t.toLowerCase()) ? t : `"${t}"`;
    return [
      e,
      i,
      `${o ? this.CACHE_FONT_SIZE : s}px`,
      n
    ].join(" ");
  }
  render(t) {
    this.visible && (this.canvas && this.canvas.skipOffscreen && !this.group && !this.isOnScreen() || (this._forceClearCache && this.initDimensions(), super.render(t)));
  }
  graphemeSplit(t) {
    return Xr(t);
  }
  _splitTextIntoLines(t) {
    let e = t.split(this._reNewline), i = Array(e.length), s = [`
`], o = [];
    for (let n = 0; n < e.length; n++) i[n] = this.graphemeSplit(e[n]), o = o.concat(i[n], s);
    return o.pop(), {
      _unwrappedLines: i,
      lines: e,
      graphemeText: o,
      graphemeLines: i
    };
  }
  toObject(t = []) {
    return {
      ...super.toObject([...Do, ...t]),
      styles: sn(this.styles, this.text),
      ...this.path ? { path: this.path.toObject() } : {}
    };
  }
  set(t, e) {
    let { textLayoutProperties: i } = this.constructor;
    super.set(t, e);
    let s = !1, o = !1;
    if (typeof t == "object") for (let n in t) n === "path" && this.setPathInfo(), s = s || i.includes(n), o = o || n === "path";
    else s = i.includes(t), o = t === "path";
    return o && this.setPathInfo(), s && this.initialized && (this.initDimensions(), this.setCoords()), this;
  }
  complexity() {
    return 1;
  }
  static async fromElement(t, e, i) {
    let s = At(t, je.ATTRIBUTE_NAMES, i), { textAnchor: o = V, textDecoration: n = "", dx: a = 0, dy: l = 0, top: h = 0, left: c = 0, fontSize: u = 16, strokeWidth: d = 1, ...g } = {
      ...e,
      ...s
    }, p = new this(Ar(t.textContent || "").trim(), {
      left: c + a,
      top: h + l,
      underline: n.includes("underline"),
      overline: n.includes("overline"),
      linethrough: n.includes("line-through"),
      strokeWidth: 0,
      fontSize: u,
      ...g
    }), m = p.getScaledHeight() / p.height, y = ((p.height + p.strokeWidth) * p.lineHeight - p.height) * m, x = p.getScaledHeight() + y, _ = 0;
    return o === "center" && (_ = p.getScaledWidth() / 2), o === "right" && (_ = p.getScaledWidth()), p.set({
      left: p.left - _,
      top: p.top - (x - p.fontSize * (0.07 + p._fontSizeFraction)) / p.lineHeight,
      strokeWidth: d
    }), p;
  }
  static fromObject(t) {
    return this._fromObject({
      ...t,
      styles: on(t.styles || {}, t.text)
    }, { extraParam: "text" });
  }
};
f(xt, "textLayoutProperties", Mo), f(xt, "cacheProperties", [...Pt, ...Do]), f(xt, "ownDefaults", da), f(xt, "type", "Text"), f(xt, "genericFonts", [
  "serif",
  "sans-serif",
  "monospace",
  "cursive",
  "fantasy",
  "system-ui",
  "ui-serif",
  "ui-sans-serif",
  "ui-monospace",
  "ui-rounded",
  "math",
  "emoji",
  "fangsong"
]), f(xt, "ATTRIBUTE_NAMES", zt.concat("x", "y", "dx", "dy", "font-family", "font-style", "font-weight", "font-size", "letter-spacing", "text-decoration", "text-decoration-thickness", "text-decoration-color", "text-anchor")), Qo(xt, [class extends To {
  _toSVG() {
    let r = this._getSVGLeftTopOffsets(), t = this._getSVGTextAndBg(r.textTop, r.textLeft);
    return this._wrapSVGTextAndBg(t);
  }
  toSVG(r) {
    let t = this._createBaseSVGMarkup(this._toSVG(), {
      reviver: r,
      noStyle: !0,
      withShadow: !0
    }), e = this.path;
    return e ? t + e._createBaseSVGMarkup(e._toSVG(), {
      reviver: r,
      withShadow: !0,
      additionalTransform: ve(this.calcOwnMatrix())
    }) : t;
  }
  _getSVGLeftTopOffsets() {
    return {
      textLeft: -this.width / 2,
      textTop: -this.height / 2,
      lineTop: this.getHeightOfLine(0)
    };
  }
  _wrapSVGTextAndBg({ textBgRects: r, textSpans: t }) {
    let e = this.getSvgTextDecoration(this);
    return [
      r.join(""),
      '		<text xml:space="preserve" ',
      `font-family="${M(this.fontFamily.replace(eh, "'"))}" `,
      `font-size="${M(this.fontSize)}" `,
      this.fontStyle ? `font-style="${M(this.fontStyle)}" ` : "",
      this.fontWeight ? `font-weight="${M(this.fontWeight)}" ` : "",
      e ? `text-decoration="${e}" ` : "",
      this.direction === "rtl" ? 'direction="rtl" ' : "",
      'style="',
      this.getSvgStyles(!0),
      '"',
      this.addPaintOrder(),
      " >",
      t.join(""),
      `</text>
`
    ];
  }
  _getSVGTextAndBg(r, t) {
    let e = [], i = [], s, o = r;
    this.backgroundColor && i.push(ii(this.backgroundColor, -this.width / 2, -this.height / 2, this.width, this.height));
    for (let n = 0, a = this._textLines.length; n < a; n++) s = this._getLineLeftOffset(n), this.direction === "rtl" && (s += this.width), (this.textBackgroundColor || this.styleHas("textBackgroundColor", n)) && this._setSVGTextLineBg(i, n, t + s, o), this._setSVGTextLineText(e, n, t + s, o), o += this.getHeightOfLine(n);
    return {
      textSpans: e,
      textBgRects: i
    };
  }
  _createTextCharSpan(r, t, e, i, s) {
    let o = P.NUM_FRACTION_DIGITS, n = this.getSvgSpanStyles(t, r !== r.trim() || !!r.match(th)), a = n ? `style="${n}"` : "", l = t.deltaY, h = l ? ` dy="${F(l, o)}" ` : "", { angle: c, renderLeft: u, renderTop: d, width: g } = s, p = "";
    if (u !== void 0) {
      let m = g / 2;
      c && (p = ` rotate="${F(Dt(c), o)}"`);
      let y = ee({ angle: Dt(c) });
      y[4] = u, y[5] = d;
      let x = new v(-m, 0).transform(y);
      e = x.x, i = x.y;
    }
    return `<tspan x="${F(e, o)}" y="${F(i, o)}" ${h}${p}${a}>${M(r)}</tspan>`;
  }
  _setSVGTextLineText(r, t, e, i) {
    let s = this.getHeightOfLine(t), o = this.textAlign.includes(ts), n = this._textLines[t], a, l, h, c, u, d = "", g = 0;
    i += s * (1 - this._fontSizeFraction) / this.lineHeight;
    for (let p = 0, m = n.length - 1; p <= m; p++) u = p === m || this.charSpacing || this.path, d += n[p], h = this.__charBounds[t][p], g === 0 ? (e += h.kernedWidth - h.width, g += h.width) : g += h.kernedWidth, o && !u && this._reSpaceAndTab.test(n[p]) && (u = !0), u || (a = a || this.getCompleteStyleDeclaration(t, p), l = this.getCompleteStyleDeclaration(t, p + 1), u = Nr(a, l, !0)), u && (c = this._getStyleDeclaration(t, p), r.push(this._createTextCharSpan(d, c, e, i, h)), d = "", a = l, this.direction === "rtl" ? e -= g : e += g, g = 0);
  }
  _setSVGTextLineBg(r, t, e, i) {
    let s = this._textLines[t], o = this.getHeightOfLine(t) / this.lineHeight, n, a = 0, l = 0, h = this.getValueOfPropertyAt(t, 0, "textBackgroundColor");
    for (let c = 0; c < s.length; c++) {
      let { left: u, width: d, kernedWidth: g } = this.__charBounds[t][c];
      n = this.getValueOfPropertyAt(t, c, "textBackgroundColor"), n === h ? a += g : (h && r.push(ii(h, e + l, i, a, o)), l = u, a = d, h = n);
    }
    n && r.push(ii(h, e + l, i, a, o));
  }
  getSvgStyles(r) {
    let t = Hr(this.textDecorationColor) ? ` text-decoration-color: ${M(this[Gr])};` : "";
    return `${super.getSvgStyles(r)} text-decoration-thickness: ${F(this.textDecorationThickness * this.getObjectScaling().y / 10, P.NUM_FRACTION_DIGITS)}%;${t} white-space: pre;`;
  }
  getSvgSpanStyles(r, t) {
    let { fontFamily: e, strokeWidth: i, stroke: s, fill: o, fontSize: n, fontStyle: a, fontWeight: l, textDecorationThickness: h, textDecorationColor: c, linethrough: u, overline: d, underline: g } = r, p = this.getSvgTextDecoration({
      underline: g ?? this.underline,
      overline: d ?? this.overline,
      linethrough: u ?? this.linethrough
    }), m = h || this.textDecorationThickness, y = c || this.textDecorationColor, x = qt(i), _ = Kt(e), S = qt(n), C = Kt(a), b = qt(l) || Kt(l), O = Kt(y);
    return [
      s ? er(Mt, s) : "",
      x ? `stroke-width: ${M(x)}; ` : "",
      _ ? `font-family: ${_.includes("'") || _.includes('"') ? M(_) : `'${M(_)}'`}; ` : "",
      S ? `font-size: ${M(S)}px; ` : "",
      C ? `font-style: ${M(C)}; ` : "",
      b ? `font-weight: ${M(b)}; ` : "",
      p ? `text-decoration: ${p}; text-decoration-thickness: ${F(m * this.getObjectScaling().y / 10, P.NUM_FRACTION_DIGITS)}%;${O ? ` text-decoration-color: ${M(O)};` : ""} ` : "",
      o ? er(tt, o) : "",
      t ? "white-space: pre; " : ""
    ].join("");
  }
  getSvgTextDecoration(r) {
    return [
      "overline",
      "underline",
      "line-through"
    ].filter((t) => r[t.replace("-", "")]).join(" ");
  }
}]), w.setClass(xt), w.setSVGClass(xt);
var rh = class {
  constructor(r) {
    f(this, "target", void 0), f(this, "__mouseDownInPlace", !1), f(this, "__dragStartFired", !1), f(this, "__isDraggingOver", !1), f(this, "__dragStartSelection", void 0), f(this, "__dragImageDisposer", void 0), f(this, "_dispose", void 0), this.target = r;
    let t = [
      this.target.on("dragenter", this.dragEnterHandler.bind(this)),
      this.target.on("dragover", this.dragOverHandler.bind(this)),
      this.target.on("dragleave", this.dragLeaveHandler.bind(this)),
      this.target.on("dragend", this.dragEndHandler.bind(this)),
      this.target.on("drop", this.dropHandler.bind(this))
    ];
    this._dispose = () => {
      t.forEach((e) => e()), this._dispose = void 0;
    };
  }
  isPointerOverSelection(r) {
    let t = this.target, e = t.getSelectionStartFromPointer(r);
    return t.isEditing && e >= t.selectionStart && e <= t.selectionEnd && t.selectionStart < t.selectionEnd;
  }
  start(r) {
    return this.__mouseDownInPlace = this.isPointerOverSelection(r);
  }
  isActive() {
    return this.__mouseDownInPlace;
  }
  end(r) {
    let t = this.isActive();
    return t && !this.__dragStartFired && (this.target.setCursorByClick(r), this.target.initDelayedCursor(!0)), this.__mouseDownInPlace = !1, this.__dragStartFired = !1, this.__isDraggingOver = !1, t;
  }
  getDragStartSelection() {
    return this.__dragStartSelection;
  }
  setDragImage(r, { selectionStart: t, selectionEnd: e }) {
    var i;
    let s = this.target, o = s.canvas, n = new v(s.flipX ? -1 : 1, s.flipY ? -1 : 1), a = s._getCursorBoundaries(t), l = new v(a.left + a.leftOffset, a.top + a.topOffset).multiply(n).transform(s.calcTransformMatrix()), h = o.getScenePoint(r).subtract(l), c = s.getCanvasRetinaScaling(), u = s.getBoundingRect(), d = l.subtract(new v(u.left, u.top)), g = o.viewportTransform, p = d.add(h).transform(g, !0), m = s.backgroundColor, y = ls(s.styles);
    s.backgroundColor = "";
    let x = {
      stroke: "transparent",
      fill: "transparent",
      textBackgroundColor: "transparent"
    };
    s.setSelectionStyles(x, 0, t), s.setSelectionStyles(x, e, s.text.length), s.dirty = !0;
    let _ = s.toCanvasElement({
      enableRetinaScaling: o.enableRetinaScaling,
      viewportTransform: !0
    });
    s.backgroundColor = m, s.styles = y, s.dirty = !0, Ci(_, {
      position: "fixed",
      left: -_.width + "px",
      border: Lr,
      width: _.width / c + "px",
      height: _.height / c + "px"
    }), this.__dragImageDisposer && this.__dragImageDisposer(), this.__dragImageDisposer = () => {
      _.remove();
    }, ut(r.target || this.target.hiddenTextarea).body.appendChild(_), (i = r.dataTransfer) == null || i.setDragImage(_, p.x, p.y);
  }
  onDragStart(r) {
    this.__dragStartFired = !0;
    let t = this.target, e = this.isActive();
    if (e && r.dataTransfer) {
      let i = this.__dragStartSelection = {
        selectionStart: t.selectionStart,
        selectionEnd: t.selectionEnd
      }, s = t._text.slice(i.selectionStart, i.selectionEnd).join(""), o = {
        text: t.text,
        value: s,
        ...i
      };
      r.dataTransfer.setData("text/plain", s), r.dataTransfer.setData("application/fabric", JSON.stringify({
        value: s,
        styles: t.getSelectionStyles(i.selectionStart, i.selectionEnd, !0)
      })), r.dataTransfer.effectAllowed = "copyMove", this.setDragImage(r, o);
    }
    return t.abortCursorAnimation(), e;
  }
  canDrop(r) {
    if (this.target.editable && !this.target.getActiveControl() && !r.defaultPrevented) {
      if (this.isActive() && this.__dragStartSelection) {
        let t = this.target.getSelectionStartFromPointer(r), e = this.__dragStartSelection;
        return t < e.selectionStart || t > e.selectionEnd;
      }
      return !0;
    }
    return !1;
  }
  targetCanDrop(r) {
    return this.target.canDrop(r);
  }
  dragEnterHandler({ e: r }) {
    let t = this.targetCanDrop(r);
    !this.__isDraggingOver && t && (this.__isDraggingOver = !0);
  }
  dragOverHandler(r) {
    let { e: t } = r, e = this.targetCanDrop(t);
    !this.__isDraggingOver && e ? this.__isDraggingOver = !0 : this.__isDraggingOver && !e && (this.__isDraggingOver = !1), this.__isDraggingOver && (t.preventDefault(), r.canDrop = !0, r.dropTarget = this.target);
  }
  dragLeaveHandler() {
    (this.__isDraggingOver || this.isActive()) && (this.__isDraggingOver = !1);
  }
  dropHandler(r) {
    var t;
    let { e } = r, i = e.defaultPrevented;
    this.__isDraggingOver = !1, e.preventDefault();
    let s = (t = e.dataTransfer) == null ? void 0 : t.getData("text/plain");
    if (s && !i) {
      let o = this.target, n = o.canvas, a = o.getSelectionStartFromPointer(e), { styles: l } = e.dataTransfer.types.includes("application/fabric") ? JSON.parse(e.dataTransfer.getData("application/fabric")) : {}, h = s[Math.max(0, s.length - 1)];
      if (this.__dragStartSelection) {
        let c = this.__dragStartSelection.selectionStart, u = this.__dragStartSelection.selectionEnd;
        a > c && a <= u ? a = c : a > u && (a -= u - c), o.removeChars(c, u), delete this.__dragStartSelection;
      }
      o._reNewline.test(h) && (o._reNewline.test(o._text[a]) || a === o._text.length) && (s = s.trimEnd()), r.didDrop = !0, r.dropTarget = o, o.insertChars(s, l, a), n.setActiveObject(o), o.enterEditing(e), o.selectionStart = Math.min(a + 0, o._text.length), o.selectionEnd = Math.min(o.selectionStart + s.length, o._text.length), o.hiddenTextarea.value = o.text, o._updateTextarea(), o.hiddenTextarea.focus(), o.fire(Mr, {
        index: a + 0,
        action: "drop"
      }), n.fire("text:changed", { target: o }), n.contextTopDirty = !0, n.requestRenderAll();
    }
  }
  dragEndHandler({ e: r }) {
    if (this.isActive() && this.__dragStartFired && this.__dragStartSelection) {
      var t;
      let e = this.target, i = this.target.canvas, { selectionStart: s, selectionEnd: o } = this.__dragStartSelection, n = ((t = r.dataTransfer) == null ? void 0 : t.dropEffect) || "none";
      n === "none" ? (e.selectionStart = s, e.selectionEnd = o, e._updateTextarea(), e.hiddenTextarea.focus()) : (e.clearContextTop(), n === "move" && (e.removeChars(s, o), e.selectionStart = e.selectionEnd = s, e.hiddenTextarea && (e.hiddenTextarea.value = e.text), e._updateTextarea(), e.fire(Mr, {
        index: s,
        action: "dragend"
      }), i.fire("text:changed", { target: e }), i.requestRenderAll()), e.exitEditing());
    }
    this.__dragImageDisposer && this.__dragImageDisposer(), delete this.__dragImageDisposer, delete this.__dragStartSelection, this.__isDraggingOver = !1;
  }
  dispose() {
    this._dispose && this._dispose();
  }
}, Is = /[ \n\.,;!\?\-]/, ih = class extends xt {
  constructor(...r) {
    super(...r), f(this, "_currentCursorOpacity", 1);
  }
  initBehavior() {
    this._tick = this._tick.bind(this), this._onTickComplete = this._onTickComplete.bind(this), this.updateSelectionOnMouseMove = this.updateSelectionOnMouseMove.bind(this);
  }
  onDeselect(r) {
    return this.isEditing && this.exitEditing(), this.selected = !1, super.onDeselect(r);
  }
  _animateCursor({ toValue: r, duration: t, delay: e, onComplete: i }) {
    return ss({
      startValue: this._currentCursorOpacity,
      endValue: r,
      duration: t,
      delay: e,
      onComplete: i,
      abort: () => !this.canvas || this.selectionStart !== this.selectionEnd,
      onChange: (s) => {
        this._currentCursorOpacity = s, this.renderCursorOrSelection();
      }
    });
  }
  _tick(r) {
    this._currentTickState = this._animateCursor({
      toValue: 0,
      duration: this.cursorDuration / 2,
      delay: Math.max(r || 0, 100),
      onComplete: this._onTickComplete
    });
  }
  _onTickComplete() {
    var r;
    (r = this._currentTickCompleteState) == null || r.abort(), this._currentTickCompleteState = this._animateCursor({
      toValue: 1,
      duration: this.cursorDuration,
      onComplete: this._tick
    });
  }
  initDelayedCursor(r) {
    this.abortCursorAnimation(), this._tick(r ? 0 : this.cursorDelay);
  }
  abortCursorAnimation() {
    let r = !1;
    [this._currentTickState, this._currentTickCompleteState].forEach((t) => {
      t && !t.isDone() && (r = !0, t.abort());
    }), this._currentCursorOpacity = 1, r && this.clearContextTop();
  }
  restartCursorIfNeeded() {
    [this._currentTickState, this._currentTickCompleteState].some((r) => !r || r.isDone()) && this.initDelayedCursor();
  }
  selectAll() {
    return this.selectionStart = 0, this.selectionEnd = this._text.length, this._fireSelectionChanged(), this._updateTextarea(), this;
  }
  cmdAll() {
    this.selectAll(), this.renderCursorOrSelection();
  }
  getSelectedText() {
    return this._text.slice(this.selectionStart, this.selectionEnd).join("");
  }
  findWordBoundaryLeft(r) {
    let t = 0, e = r - 1;
    if (this._reSpace.test(this._text[e])) for (; this._reSpace.test(this._text[e]); ) t++, e--;
    for (; /\S/.test(this._text[e]) && e > -1; ) t++, e--;
    return r - t;
  }
  findWordBoundaryRight(r) {
    let t = 0, e = r;
    if (this._reSpace.test(this._text[e])) for (; this._reSpace.test(this._text[e]); ) t++, e++;
    for (; /\S/.test(this._text[e]) && e < this._text.length; ) t++, e++;
    return r + t;
  }
  findLineBoundaryLeft(r) {
    let t = 0, e = r - 1;
    for (; !/\n/.test(this._text[e]) && e > -1; ) t++, e--;
    return r - t;
  }
  findLineBoundaryRight(r) {
    let t = 0, e = r;
    for (; !/\n/.test(this._text[e]) && e < this._text.length; ) t++, e++;
    return r + t;
  }
  searchWordBoundary(r, t) {
    let e = this._text, i = r > 0 && this._reSpace.test(e[r]) && (t === -1 || !Bi.test(e[r - 1])) ? r - 1 : r, s = e[i];
    for (; i > 0 && i < e.length && !Is.test(s); ) i += t, s = e[i];
    return t === -1 && Is.test(s) && i++, i;
  }
  selectWord(r) {
    var t;
    r = (t = r) == null ? this.selectionStart : t;
    let e = this.searchWordBoundary(r, -1), i = Math.max(e, this.searchWordBoundary(r, 1));
    this.selectionStart = e, this.selectionEnd = i, this._fireSelectionChanged(), this._updateTextarea(), this.renderCursorOrSelection();
  }
  selectLine(r) {
    var t;
    r = (t = r) == null ? this.selectionStart : t;
    let e = this.findLineBoundaryLeft(r), i = this.findLineBoundaryRight(r);
    this.selectionStart = e, this.selectionEnd = i, this._fireSelectionChanged(), this._updateTextarea();
  }
  enterEditing(r) {
    !this.isEditing && this.editable && (this.enterEditingImpl(), this.fire("editing:entered", r ? { e: r } : void 0), this._fireSelectionChanged(), this.canvas && (this.canvas.fire("text:editing:entered", {
      target: this,
      e: r
    }), this.canvas.requestRenderAll()));
  }
  enterEditingImpl() {
    this.canvas && (this.canvas.calcOffset(), this.canvas.textEditingManager.exitTextEditing()), this.isEditing = !0, this.initHiddenTextarea(), this.hiddenTextarea.focus(), this.hiddenTextarea.value = this.text, this._updateTextarea(), this._saveEditingProps(), this._setEditingProps(), this._textBeforeEdit = this.text, this._tick();
  }
  updateSelectionOnMouseMove(r) {
    if (this.getActiveControl()) return;
    let t = this.hiddenTextarea;
    ut(t).activeElement !== t && t.focus();
    let e = this.getSelectionStartFromPointer(r), i = this.selectionStart, s = this.selectionEnd;
    (e === this.__selectionStartOnMouseDown && i !== s || i !== e && s !== e) && (e > this.__selectionStartOnMouseDown ? (this.selectionStart = this.__selectionStartOnMouseDown, this.selectionEnd = e) : (this.selectionStart = e, this.selectionEnd = this.__selectionStartOnMouseDown), this.selectionStart === i && this.selectionEnd === s || (this._fireSelectionChanged(), this._updateTextarea(), this.renderCursorOrSelection()));
  }
  _setEditingProps() {
    this.hoverCursor = "text", this.canvas && (this.canvas.defaultCursor = this.canvas.moveCursor = "text"), this.borderColor = this.editingBorderColor, this.hasControls = this.selectable = !1, this.lockMovementX = this.lockMovementY = !0;
  }
  fromStringToGraphemeSelection(r, t, e) {
    let i = e.slice(0, r), s = this.graphemeSplit(i).length;
    if (r === t) return {
      selectionStart: s,
      selectionEnd: s
    };
    let o = e.slice(r, t);
    return {
      selectionStart: s,
      selectionEnd: s + this.graphemeSplit(o).length
    };
  }
  fromGraphemeToStringSelection(r, t, e) {
    let i = e.slice(0, r).join("").length;
    return r === t ? {
      selectionStart: i,
      selectionEnd: i
    } : {
      selectionStart: i,
      selectionEnd: i + e.slice(r, t).join("").length
    };
  }
  _updateTextarea() {
    if (this.cursorOffsetCache = {}, this.hiddenTextarea) {
      if (!this.inCompositionMode) {
        let r = this.fromGraphemeToStringSelection(this.selectionStart, this.selectionEnd, this._text);
        this.hiddenTextarea.selectionStart = r.selectionStart, this.hiddenTextarea.selectionEnd = r.selectionEnd;
      }
      this.updateTextareaPosition();
    }
  }
  updateFromTextArea() {
    let { hiddenTextarea: r, direction: t, textAlign: e, inCompositionMode: i } = this;
    if (!r) return;
    let s = e === "justify" ? t === "ltr" ? V : gt : e.replace("justify-", ""), o = this.getPositionByOrigin(s, "top");
    this.cursorOffsetCache = {}, this.text = r.value, this.set("dirty", !0), this.initDimensions(), this.setPositionByOrigin(o, s, "top"), this.setCoords();
    let n = this.fromStringToGraphemeSelection(r.selectionStart, r.selectionEnd, r.value);
    this.selectionEnd = this.selectionStart = n.selectionEnd, i || (this.selectionStart = n.selectionStart), this.updateTextareaPosition();
  }
  updateTextareaPosition() {
    if (this.selectionStart === this.selectionEnd) {
      let r = this._calcTextareaPosition();
      this.hiddenTextarea.style.left = r.left, this.hiddenTextarea.style.top = r.top;
    }
  }
  _calcTextareaPosition() {
    if (!this.canvas) return {
      left: "1px",
      top: "1px"
    };
    let r = this.inCompositionMode ? this.compositionStart : this.selectionStart, t = this._getCursorBoundaries(r), e = this.get2DCursorLocation(r), i = e.lineIndex, s = e.charIndex, o = this.getValueOfPropertyAt(i, s, "fontSize") * this.lineHeight, n = t.leftOffset, a = this.getCanvasRetinaScaling(), l = this.canvas.upperCanvasEl, h = l.width / a, c = l.height / a, u = h - o, d = c - o, g = new v(t.left + n, t.top + t.topOffset + o).transform(this.calcTransformMatrix()).transform(this.canvas.viewportTransform).multiply(new v(l.clientWidth / h, l.clientHeight / c));
    return g.x < 0 && (g.x = 0), g.x > u && (g.x = u), g.y < 0 && (g.y = 0), g.y > d && (g.y = d), g.x += this.canvas._offset.left, g.y += this.canvas._offset.top, {
      left: `${g.x}px`,
      top: `${g.y}px`,
      fontSize: `${o}px`,
      charHeight: o
    };
  }
  _saveEditingProps() {
    this._savedProps = {
      hasControls: this.hasControls,
      borderColor: this.borderColor,
      lockMovementX: this.lockMovementX,
      lockMovementY: this.lockMovementY,
      hoverCursor: this.hoverCursor,
      selectable: this.selectable,
      defaultCursor: this.canvas && this.canvas.defaultCursor,
      moveCursor: this.canvas && this.canvas.moveCursor
    };
  }
  _restoreEditingProps() {
    this._savedProps && (this.hoverCursor = this._savedProps.hoverCursor, this.hasControls = this._savedProps.hasControls, this.borderColor = this._savedProps.borderColor, this.selectable = this._savedProps.selectable, this.lockMovementX = this._savedProps.lockMovementX, this.lockMovementY = this._savedProps.lockMovementY, this.canvas && (this.canvas.defaultCursor = this._savedProps.defaultCursor || this.canvas.defaultCursor, this.canvas.moveCursor = this._savedProps.moveCursor || this.canvas.moveCursor), delete this._savedProps);
  }
  exitEditingImpl() {
    let r = this.hiddenTextarea;
    this.selected = !1, this.isEditing = !1, r && (r.blur && r.blur(), r.parentNode && r.parentNode.removeChild(r)), this.hiddenTextarea = null, this.abortCursorAnimation(), this.selectionStart !== this.selectionEnd && this.clearContextTop(), this.selectionEnd = this.selectionStart, this._restoreEditingProps(), this._forceClearCache && (this.initDimensions(), this.setCoords());
  }
  exitEditing() {
    let r = this._textBeforeEdit !== this.text;
    return this.exitEditingImpl(), this.fire("editing:exited"), r && this.fire("modified"), this.canvas && (this.canvas.fire("text:editing:exited", { target: this }), r && this.canvas.fire("object:modified", { target: this })), this;
  }
  _removeExtraneousStyles() {
    for (let r in this.styles) this._textLines[r] || delete this.styles[r];
  }
  removeStyleFromTo(r, t) {
    let { lineIndex: e, charIndex: i } = this.get2DCursorLocation(r, !0), { lineIndex: s, charIndex: o } = this.get2DCursorLocation(t, !0);
    if (e !== s) {
      if (this.styles[e]) for (let n = i; n < this._unwrappedTextLines[e].length; n++) delete this.styles[e][n];
      if (this.styles[s]) for (let n = o; n < this._unwrappedTextLines[s].length; n++) {
        let a = this.styles[s][n];
        a && (this.styles[e] || (this.styles[e] = {}), this.styles[e][i + n - o] = a);
      }
      for (let n = e + 1; n <= s; n++) delete this.styles[n];
      this.shiftLineStyles(s, e - s);
    } else if (this.styles[e]) {
      let n = this.styles[e], a = o - i;
      for (let l = i; l < o; l++) delete n[l];
      for (let l in this.styles[e]) {
        let h = parseInt(l, 10);
        h >= o && (n[h - a] = n[l], delete n[l]);
      }
    }
  }
  shiftLineStyles(r, t) {
    let e = Object.assign({}, this.styles);
    for (let i in this.styles) {
      let s = parseInt(i, 10);
      s > r && (this.styles[s + t] = e[s], e[s - t] || delete this.styles[s]);
    }
  }
  insertNewlineStyleObject(r, t, e, i) {
    let s = {}, o = this._unwrappedTextLines[r].length, n = o === t, a = !1;
    e || (e = 1), this.shiftLineStyles(r, e);
    let l = this.styles[r] ? this.styles[r][t === 0 ? t : t - 1] : void 0;
    for (let c in this.styles[r]) {
      let u = parseInt(c, 10);
      u >= t && (a = !0, s[u - t] = this.styles[r][c], n && t === 0 || delete this.styles[r][c]);
    }
    let h = !1;
    for (a && !n && (this.styles[r + e] = s, h = !0), (h || o > t) && e--; e > 0; ) i && i[e - 1] ? this.styles[r + e] = { 0: { ...i[e - 1] } } : l ? this.styles[r + e] = { 0: { ...l } } : delete this.styles[r + e], e--;
    this._forceClearCache = !0;
  }
  insertCharStyleObject(r, t, e, i) {
    this.styles || (this.styles = {});
    let s = this.styles[r], o = s ? { ...s } : {};
    e || (e = 1);
    for (let a in o) {
      let l = parseInt(a, 10);
      l >= t && (s[l + e] = o[l], o[l - e] || delete s[l]);
    }
    if (this._forceClearCache = !0, i) {
      for (; e--; ) Object.keys(i[e]).length && (this.styles[r] || (this.styles[r] = {}), this.styles[r][t + e] = { ...i[e] });
      return;
    }
    if (!s) return;
    let n = s[t ? t - 1 : 1];
    for (; n && e--; ) this.styles[r][t + e] = { ...n };
  }
  insertNewStyleBlock(r, t, e) {
    let i = this.get2DCursorLocation(t, !0), s = [0], o, n = 0;
    for (let a = 0; a < r.length; a++) r[a] === `
` ? (n++, s[n] = 0) : s[n]++;
    for (s[0] > 0 && (this.insertCharStyleObject(i.lineIndex, i.charIndex, s[0], e), e = e && e.slice(s[0] + 1)), n && this.insertNewlineStyleObject(i.lineIndex, i.charIndex + s[0], n), o = 1; o < n; o++) s[o] > 0 ? this.insertCharStyleObject(i.lineIndex + o, 0, s[o], e) : e && this.styles[i.lineIndex + o] && e[0] && (this.styles[i.lineIndex + o][0] = e[0]), e = e && e.slice(s[o] + 1);
    s[o] > 0 && this.insertCharStyleObject(i.lineIndex + o, 0, s[o], e);
  }
  removeChars(r, t = r + 1) {
    this.removeStyleFromTo(r, t), this._text.splice(r, t - r), this.text = this._text.join(""), this.set("dirty", !0), this.initDimensions(), this.setCoords(), this._removeExtraneousStyles();
  }
  insertChars(r, t, e, i = e) {
    i > e && this.removeStyleFromTo(e, i);
    let s = this.graphemeSplit(r);
    this.insertNewStyleBlock(s, e, t), this._text = [
      ...this._text.slice(0, e),
      ...s,
      ...this._text.slice(i)
    ], this.text = this._text.join(""), this.set("dirty", !0), this.initDimensions(), this.setCoords(), this._removeExtraneousStyles();
  }
  setSelectionStartEndWithShift(r, t, e) {
    e <= r ? (t === r ? this._selectionDirection = V : this._selectionDirection === "right" && (this._selectionDirection = V, this.selectionEnd = r), this.selectionStart = e) : e > r && e < t ? this._selectionDirection === "right" ? this.selectionEnd = e : this.selectionStart = e : (t === r ? this._selectionDirection = gt : this._selectionDirection === "left" && (this._selectionDirection = gt, this.selectionStart = t), this.selectionEnd = e);
  }
}, sh = class extends ih {
  initHiddenTextarea() {
    let r = this.canvas && ut(this.canvas.getElement()) || _e(), t = r.createElement("textarea");
    Object.entries({
      autocapitalize: "off",
      autocorrect: "off",
      autocomplete: "off",
      spellcheck: "false",
      "data-fabric": "textarea",
      wrap: "off",
      name: "fabricTextarea"
    }).map(([o, n]) => t.setAttribute(o, n));
    let { top: e, left: i, fontSize: s } = this._calcTextareaPosition();
    t.style.cssText = `position: absolute; top: ${e}; left: ${i}; z-index: -999; opacity: 0; width: 1px; height: 1px; font-size: 1px; padding-top: ${s};`, (this.hiddenTextareaContainer || r.body).appendChild(t), Object.entries({
      blur: "blur",
      keydown: "onKeyDown",
      keyup: "onKeyUp",
      input: "onInput",
      copy: "copy",
      cut: "copy",
      paste: "paste",
      compositionstart: "onCompositionStart",
      compositionupdate: "onCompositionUpdate",
      compositionend: "onCompositionEnd"
    }).map(([o, n]) => t.addEventListener(o, this[n].bind(this))), this.hiddenTextarea = t;
  }
  blur() {
    this.abortCursorAnimation();
  }
  onKeyDown(r) {
    if (!this.isEditing) return;
    let t = this.direction === "rtl" ? this.keysMapRtl : this.keysMap;
    if (r.keyCode in t) this[t[r.keyCode]](r);
    else {
      if (!(r.keyCode in this.ctrlKeysMapDown) || !r.ctrlKey && !r.metaKey) return;
      this[this.ctrlKeysMapDown[r.keyCode]](r);
    }
    r.stopImmediatePropagation(), r.preventDefault(), r.keyCode >= 33 && r.keyCode <= 40 ? (this.inCompositionMode = !1, this.clearContextTop(), this.renderCursorOrSelection()) : this.canvas && this.canvas.requestRenderAll();
  }
  onKeyUp(r) {
    !this.isEditing || this._copyDone || this.inCompositionMode ? this._copyDone = !1 : r.keyCode in this.ctrlKeysMapUp && (r.ctrlKey || r.metaKey) && (this[this.ctrlKeysMapUp[r.keyCode]](r), r.stopImmediatePropagation(), r.preventDefault(), this.canvas && this.canvas.requestRenderAll());
  }
  onInput(r) {
    let t = this.fromPaste, { value: e, selectionStart: i, selectionEnd: s } = this.hiddenTextarea;
    if (this.fromPaste = !1, r && r.stopPropagation(), !this.isEditing) return;
    let o = () => {
      this.updateFromTextArea(), this.fire(Mr), this.canvas && (this.canvas.fire("text:changed", { target: this }), this.canvas.requestRenderAll());
    };
    if (this.hiddenTextarea.value === "") return this.styles = {}, void o();
    let n = this._splitTextIntoLines(e).graphemeText, a = this._text.length, l = n.length, h = this.selectionStart, c = this.selectionEnd, u = h !== c, d, g, p, m, y = l - a, x = this.fromStringToGraphemeSelection(i, s, e), _ = h > x.selectionStart;
    u ? (g = this._text.slice(h, c), y += c - h) : l < a && (g = _ ? this._text.slice(c + y, c) : this._text.slice(h, h - y));
    let S = n.slice(x.selectionEnd - y, x.selectionEnd);
    if (g && g.length && (S.length && (d = this.getSelectionStyles(h, h + 1, !1), d = S.map(() => d[0])), u ? (p = h, m = c) : _ ? (p = c - g.length, m = c) : (p = c, m = c + g.length), this.removeStyleFromTo(p, m)), S.length) {
      let { copyPasteData: C } = Ct();
      t && S.join("") === C.copiedText && !P.disableStyleCopyPaste && (d = C.copiedTextStyle), this.insertNewStyleBlock(S, h, d);
    }
    o();
  }
  onCompositionStart() {
    this.inCompositionMode = !0;
  }
  onCompositionEnd() {
    this.inCompositionMode = !1;
  }
  onCompositionUpdate({ target: r }) {
    let { selectionStart: t, selectionEnd: e } = r;
    this.compositionStart = t, this.compositionEnd = e, this.updateTextareaPosition();
  }
  copy() {
    if (this.selectionStart === this.selectionEnd) return;
    let { copyPasteData: r } = Ct();
    r.copiedText = this.getSelectedText(), P.disableStyleCopyPaste ? r.copiedTextStyle = void 0 : r.copiedTextStyle = this.getSelectionStyles(this.selectionStart, this.selectionEnd, !0), this._copyDone = !0;
  }
  paste() {
    this.fromPaste = !0;
  }
  _getWidthBeforeCursor(r, t) {
    let e, i = this._getLineLeftOffset(r);
    return t > 0 && (e = this.__charBounds[r][t - 1], i += e.left + e.width), i;
  }
  getDownCursorOffset(r, t) {
    let e = this._getSelectionForOffset(r, t), i = this.get2DCursorLocation(e), s = i.lineIndex;
    if (s === this._textLines.length - 1 || r.metaKey || r.keyCode === 34) return this._text.length - e;
    let o = i.charIndex, n = this._getWidthBeforeCursor(s, o), a = this._getIndexOnLine(s + 1, n);
    return this._textLines[s].slice(o).length + a + 1 + this.missingNewlineOffset(s);
  }
  _getSelectionForOffset(r, t) {
    return r.shiftKey && this.selectionStart !== this.selectionEnd && t ? this.selectionEnd : this.selectionStart;
  }
  getUpCursorOffset(r, t) {
    let e = this._getSelectionForOffset(r, t), i = this.get2DCursorLocation(e), s = i.lineIndex;
    if (s === 0 || r.metaKey || r.keyCode === 33) return -e;
    let o = i.charIndex, n = this._getWidthBeforeCursor(s, o), a = this._getIndexOnLine(s - 1, n), l = this._textLines[s].slice(0, o), h = this.missingNewlineOffset(s - 1);
    return -this._textLines[s - 1].length + a - l.length + (1 - h);
  }
  _getIndexOnLine(r, t) {
    let e = this._textLines[r], i, s, o = this._getLineLeftOffset(r), n = 0;
    for (let a = 0, l = e.length; a < l; a++) if (i = this.__charBounds[r][a].width, o += i, o > t) {
      s = !0;
      let h = o - i, c = o, u = Math.abs(h - t);
      n = Math.abs(c - t) < u ? a : a - 1;
      break;
    }
    return s || (n = e.length - 1), n;
  }
  moveCursorDown(r) {
    this.selectionStart >= this._text.length && this.selectionEnd >= this._text.length || this._moveCursorUpOrDown("Down", r);
  }
  moveCursorUp(r) {
    this.selectionStart === 0 && this.selectionEnd === 0 || this._moveCursorUpOrDown("Up", r);
  }
  _moveCursorUpOrDown(r, t) {
    let e = this[`get${r}CursorOffset`](t, this._selectionDirection === gt);
    if (t.shiftKey ? this.moveCursorWithShift(e) : this.moveCursorWithoutShift(e), e !== 0) {
      let i = this.text.length;
      this.selectionStart = te(0, this.selectionStart, i), this.selectionEnd = te(0, this.selectionEnd, i), this.abortCursorAnimation(), this.initDelayedCursor(), this._fireSelectionChanged(), this._updateTextarea();
    }
  }
  moveCursorWithShift(r) {
    let t = this._selectionDirection === "left" ? this.selectionStart + r : this.selectionEnd + r;
    return this.setSelectionStartEndWithShift(this.selectionStart, this.selectionEnd, t), r !== 0;
  }
  moveCursorWithoutShift(r) {
    return r < 0 ? (this.selectionStart += r, this.selectionEnd = this.selectionStart) : (this.selectionEnd += r, this.selectionStart = this.selectionEnd), r !== 0;
  }
  moveCursorLeft(r) {
    this.selectionStart === 0 && this.selectionEnd === 0 || this._moveCursorLeftOrRight("Left", r);
  }
  _move(r, t, e) {
    let i;
    if (r.altKey) i = this[`findWordBoundary${e}`](this[t]);
    else {
      if (!r.metaKey && r.keyCode !== 35 && r.keyCode !== 36) return this[t] += e === "Left" ? -1 : 1, !0;
      i = this[`findLineBoundary${e}`](this[t]);
    }
    return i !== void 0 && this[t] !== i && (this[t] = i, !0);
  }
  _moveLeft(r, t) {
    return this._move(r, t, "Left");
  }
  _moveRight(r, t) {
    return this._move(r, t, "Right");
  }
  moveCursorLeftWithoutShift(r) {
    let t = !0;
    return this._selectionDirection = V, this.selectionEnd === this.selectionStart && this.selectionStart !== 0 && (t = this._moveLeft(r, "selectionStart")), this.selectionEnd = this.selectionStart, t;
  }
  moveCursorLeftWithShift(r) {
    return this._selectionDirection === "right" && this.selectionStart !== this.selectionEnd ? this._moveLeft(r, "selectionEnd") : this.selectionStart === 0 ? void 0 : (this._selectionDirection = V, this._moveLeft(r, "selectionStart"));
  }
  moveCursorRight(r) {
    this.selectionStart >= this._text.length && this.selectionEnd >= this._text.length || this._moveCursorLeftOrRight("Right", r);
  }
  _moveCursorLeftOrRight(r, t) {
    let e = `moveCursor${r}${t.shiftKey ? "WithShift" : "WithoutShift"}`;
    this._currentCursorOpacity = 1, this[e](t) && (this.abortCursorAnimation(), this.initDelayedCursor(), this._fireSelectionChanged(), this._updateTextarea());
  }
  moveCursorRightWithShift(r) {
    return this._selectionDirection === "left" && this.selectionStart !== this.selectionEnd ? this._moveRight(r, "selectionStart") : this.selectionEnd === this._text.length ? void 0 : (this._selectionDirection = gt, this._moveRight(r, "selectionEnd"));
  }
  moveCursorRightWithoutShift(r) {
    let t = !0;
    return this._selectionDirection = gt, this.selectionStart === this.selectionEnd ? (t = this._moveRight(r, "selectionStart"), this.selectionEnd = this.selectionStart) : this.selectionStart = this.selectionEnd, t;
  }
}, Bs = (r) => !!r.button, oh = class extends sh {
  constructor(...r) {
    super(...r), f(this, "draggableTextDelegate", void 0);
  }
  initBehavior() {
    this.on("mousedown", this._mouseDownHandler), this.on("mouseup", this.mouseUpHandler), this.on("mousedblclick", this.doubleClickHandler), this.on("mousetripleclick", this.tripleClickHandler), this.draggableTextDelegate = new rh(this), super.initBehavior();
  }
  shouldStartDragging() {
    return this.draggableTextDelegate.isActive();
  }
  onDragStart(r) {
    return this.draggableTextDelegate.onDragStart(r);
  }
  canDrop(r) {
    return this.draggableTextDelegate.canDrop(r);
  }
  doubleClickHandler(r) {
    this.isEditing && (this.selectWord(this.getSelectionStartFromPointer(r.e)), this.renderCursorOrSelection());
  }
  tripleClickHandler(r) {
    this.isEditing && (this.selectLine(this.getSelectionStartFromPointer(r.e)), this.renderCursorOrSelection());
  }
  _mouseDownHandler({ e: r, alreadySelected: t }) {
    this.canvas && this.editable && !Bs(r) && !this.getActiveControl() && (this.draggableTextDelegate.start(r) || (this.canvas.textEditingManager.register(this), t && (this.inCompositionMode = !1, this.setCursorByClick(r)), this.isEditing && (this.__selectionStartOnMouseDown = this.selectionStart, this.selectionStart === this.selectionEnd && this.abortCursorAnimation(), this.renderCursorOrSelection()), this.selected || (this.selected = t || this.isEditing)));
  }
  mouseUpHandler({ e: r, transform: t }) {
    let e = this.draggableTextDelegate.end(r);
    if (this.canvas) {
      this.canvas.textEditingManager.unregister(this);
      let i = this.canvas._activeObject;
      if (i && i !== this) return;
    }
    !this.editable || this.group && !this.group.interactive || t && t.actionPerformed || Bs(r) || e || this.selected && !this.getActiveControl() && (this.enterEditing(r), this.selectionStart === this.selectionEnd ? this.initDelayedCursor(!0) : this.renderCursorOrSelection());
  }
  setCursorByClick(r) {
    let t = this.getSelectionStartFromPointer(r), e = this.selectionStart, i = this.selectionEnd;
    r.shiftKey ? this.setSelectionStartEndWithShift(e, i, t) : (this.selectionStart = t, this.selectionEnd = t), this.isEditing && (this._fireSelectionChanged(), this._updateTextarea());
  }
  getSelectionStartFromPointer(r) {
    let t = this.canvas.getScenePoint(r).transform(ot(this.calcTransformMatrix())).add(new v(-this._getLeftOffset(), -this._getTopOffset())), e = 0, i = 0, s = 0;
    for (let l = 0; l < this._textLines.length && e <= t.y; l++) e += this.getHeightOfLine(l), s = l, l > 0 && (i += this._textLines[l - 1].length + this.missingNewlineOffset(l - 1));
    let o = Math.abs(this._getLineLeftOffset(s)), n = this._textLines[s].length, a = this.__charBounds[s];
    for (let l = 0; l < n; l++) {
      let h = o + a[l].kernedWidth;
      if (t.x <= h) {
        Math.abs(t.x - h) <= Math.abs(t.x - o) && i++;
        break;
      }
      o = h, i++;
    }
    return Math.min(this.flipX ? n - i : i, this._text.length);
  }
}, gr = "moveCursorUp", fr = "moveCursorDown", pr = "moveCursorLeft", mr = "moveCursorRight", vr = "exitEditing", Xs = (r, t) => {
  let e = t.getRetinaScaling();
  r.setTransform(e, 0, 0, e, 0, 0);
  let i = t.viewportTransform;
  r.transform(i[0], i[1], i[2], i[3], i[4], i[5]);
}, nh = {
  selectionStart: 0,
  selectionEnd: 0,
  selectionColor: "rgba(17,119,255,0.3)",
  isEditing: !1,
  editable: !0,
  editingBorderColor: "rgba(102,153,255,0.25)",
  cursorWidth: 2,
  cursorColor: "",
  cursorDelay: 1e3,
  cursorDuration: 600,
  caching: !0,
  hiddenTextareaContainer: null,
  keysMap: {
    9: vr,
    27: vr,
    33: gr,
    34: fr,
    35: mr,
    36: pr,
    37: pr,
    38: gr,
    39: mr,
    40: fr
  },
  keysMapRtl: {
    9: vr,
    27: vr,
    33: gr,
    34: fr,
    35: pr,
    36: mr,
    37: mr,
    38: gr,
    39: pr,
    40: fr
  },
  ctrlKeysMapDown: { 65: "cmdAll" },
  ctrlKeysMapUp: {
    67: "copy",
    88: "cut"
  },
  _selectionDirection: null,
  _reSpace: /\s|\r?\n/,
  inCompositionMode: !1
}, ce = class Pi extends oh {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Pi.ownDefaults
    };
  }
  get type() {
    let t = super.type;
    return t === "itext" ? "i-text" : t;
  }
  constructor(t, e) {
    super(t, {
      ...Pi.ownDefaults,
      ...e
    }), this.initBehavior();
  }
  _set(t, e) {
    return this.isEditing && this._savedProps && t in this._savedProps ? (this._savedProps[t] = e, this) : (t === "canvas" && (this.canvas instanceof wi && this.canvas.textEditingManager.remove(this), e instanceof wi && e.textEditingManager.add(this)), super._set(t, e));
  }
  setSelectionStart(t) {
    t = Math.max(t, 0), this._updateAndFire("selectionStart", t);
  }
  setSelectionEnd(t) {
    t = Math.min(t, this.text.length), this._updateAndFire("selectionEnd", t);
  }
  _updateAndFire(t, e) {
    this[t] !== e && (this._fireSelectionChanged(), this[t] = e), this._updateTextarea();
  }
  _fireSelectionChanged() {
    this.fire("selection:changed"), this.canvas && this.canvas.fire("text:selection:changed", { target: this });
  }
  initDimensions() {
    this.isEditing && this.initDelayedCursor(), super.initDimensions();
  }
  getSelectionStyles(t = this.selectionStart || 0, e = this.selectionEnd, i) {
    return super.getSelectionStyles(t, e, i);
  }
  setSelectionStyles(t, e = this.selectionStart || 0, i = this.selectionEnd) {
    return super.setSelectionStyles(t, e, i);
  }
  get2DCursorLocation(t = this.selectionStart, e) {
    return super.get2DCursorLocation(t, e);
  }
  render(t) {
    super.render(t), this.cursorOffsetCache = {}, this.renderCursorOrSelection();
  }
  toCanvasElement(t) {
    let e = this.isEditing;
    this.isEditing = !1;
    let i = super.toCanvasElement(t);
    return this.isEditing = e, i;
  }
  renderCursorOrSelection() {
    if (!this.isEditing || !this.canvas) return;
    let t = this.clearContextTop(!0);
    if (!t) return;
    let e = this._getCursorBoundaries(), i = this.findAncestorsWithClipPath(), s = i.length > 0, o, n = t;
    if (s) {
      o = nt(t.canvas), n = o.getContext("2d"), Xs(n, this.canvas);
      let a = this.calcTransformMatrix();
      n.transform(a[0], a[1], a[2], a[3], a[4], a[5]);
    }
    if (this.selectionStart !== this.selectionEnd || this.inCompositionMode ? this.renderSelection(n, e) : this.renderCursor(n, e), s) for (let a of i) {
      let l = a.clipPath, h = nt(t.canvas), c = h.getContext("2d");
      if (Xs(c, this.canvas), !l.absolutePositioned) {
        let u = a.calcTransformMatrix();
        c.transform(u[0], u[1], u[2], u[3], u[4], u[5]);
      }
      l.transform(c), l.drawObject(c, !0, {}), this.drawClipPathOnCache(n, l, h);
    }
    s && (t.setTransform(1, 0, 0, 1, 0, 0), t.drawImage(o, 0, 0)), this.canvas.contextTopDirty = !0, t.restore();
  }
  findAncestorsWithClipPath() {
    let t = [], e = this;
    for (; e; ) e.clipPath && t.push(e), e = e.parent;
    return t;
  }
  _getCursorBoundaries(t = this.selectionStart, e) {
    let i = this._getLeftOffset(), s = this._getTopOffset(), o = this._getCursorBoundariesOffsets(t, e);
    return {
      left: i,
      top: s,
      leftOffset: o.left,
      topOffset: o.top
    };
  }
  _getCursorBoundariesOffsets(t, e) {
    return e ? this.__getCursorBoundariesOffsets(t) : this.cursorOffsetCache && "top" in this.cursorOffsetCache ? this.cursorOffsetCache : this.cursorOffsetCache = this.__getCursorBoundariesOffsets(t);
  }
  __getCursorBoundariesOffsets(t) {
    let e = 0, i = 0, { charIndex: s, lineIndex: o } = this.get2DCursorLocation(t), { textAlign: n, direction: a } = this;
    for (let u = 0; u < o; u++) e += this.getHeightOfLine(u);
    let l = this._getLineLeftOffset(o), h = this.__charBounds[o][s];
    h && (i = h.left), this.charSpacing !== 0 && s === this._textLines[o].length && (i -= this._getWidthOfCharSpacing());
    let c = l + (i > 0 ? i : 0);
    return a === "rtl" && (n === "right" || n === "justify" || n === "justify-right" ? c *= -1 : n === "left" || n === "justify-left" ? c = l - (i > 0 ? i : 0) : n !== "center" && n !== "justify-center" || (c = l - (i > 0 ? i : 0))), {
      top: e,
      left: c
    };
  }
  renderCursorAt(t) {
    this._renderCursor(this.canvas.contextTop, this._getCursorBoundaries(t, !0), t);
  }
  renderCursor(t, e) {
    this._renderCursor(t, e, this.selectionStart);
  }
  getCursorRenderingData(t = this.selectionStart, e = this._getCursorBoundaries(t)) {
    let i = this.get2DCursorLocation(t), s = i.lineIndex, o = i.charIndex > 0 ? i.charIndex - 1 : 0, n = this.getValueOfPropertyAt(s, o, "fontSize"), a = this.getObjectScaling().x * this.canvas.getZoom(), l = this.cursorWidth / a, h = this.getValueOfPropertyAt(s, o, "deltaY"), c = e.topOffset + (1 - this._fontSizeFraction) * this.getHeightOfLine(s) / this.lineHeight - n * (1 - this._fontSizeFraction);
    return {
      color: this.cursorColor || this.getValueOfPropertyAt(s, o, "fill"),
      opacity: this._currentCursorOpacity,
      left: e.left + e.leftOffset - l / 2,
      top: c + e.top + h,
      width: l,
      height: n
    };
  }
  _renderCursor(t, e, i) {
    let { color: s, opacity: o, left: n, top: a, width: l, height: h } = this.getCursorRenderingData(i, e);
    t.fillStyle = s, t.globalAlpha = o, t.fillRect(n, a, l, h);
  }
  renderSelection(t, e) {
    let i = {
      selectionStart: this.inCompositionMode ? this.hiddenTextarea.selectionStart : this.selectionStart,
      selectionEnd: this.inCompositionMode ? this.hiddenTextarea.selectionEnd : this.selectionEnd
    };
    this._renderSelection(t, i, e);
  }
  renderDragSourceEffect() {
    let t = this.draggableTextDelegate.getDragStartSelection();
    this._renderSelection(this.canvas.contextTop, t, this._getCursorBoundaries(t.selectionStart, !0));
  }
  renderDropTargetEffect(t) {
    let e = this.getSelectionStartFromPointer(t);
    this.renderCursorAt(e);
  }
  _renderSelection(t, e, i) {
    let { textAlign: s, direction: o } = this, n = e.selectionStart, a = e.selectionEnd, l = s.includes(ts), h = this.get2DCursorLocation(n), c = this.get2DCursorLocation(a), u = h.lineIndex, d = c.lineIndex, g = h.charIndex < 0 ? 0 : h.charIndex, p = c.charIndex < 0 ? 0 : c.charIndex;
    for (let m = u; m <= d; m++) {
      let y = this._getLineLeftOffset(m) || 0, x = this.getHeightOfLine(m), _ = 0, S = 0;
      if (m === u && (_ = this.__charBounds[u][g].left), m >= u && m < d) S = l && !this.isEndOfWrapping(m) ? this.width : this.getLineWidth(m) || 5;
      else if (m === d) if (p === 0) S = this.__charBounds[d][p].left;
      else {
        let D = this._getWidthOfCharSpacing();
        S = this.__charBounds[d][p - 1].left + this.__charBounds[d][p - 1].width - D;
      }
      let C = x;
      (this.lineHeight < 1 || m === d && this.lineHeight > 1) && (x /= this.lineHeight);
      let b = i.left + y + _, O = x, T = 0, k = S - _;
      this.inCompositionMode ? (t.fillStyle = this.compositionColor || "black", O = 1, T = x) : t.fillStyle = this.selectionColor, o === "rtl" && (s === "right" || s === "justify" || s === "justify-right" ? b = this.width - b - k : s === "left" || s === "justify-left" ? b = i.left + y - S : s !== "center" && s !== "justify-center" || (b = i.left + y - S)), t.fillRect(b, i.top + i.topOffset + T, k, O), i.topOffset += C;
    }
  }
  getCurrentCharFontSize() {
    let t = this._getCurrentCharIndex();
    return this.getValueOfPropertyAt(t.l, t.c, "fontSize");
  }
  getCurrentCharColor() {
    let t = this._getCurrentCharIndex();
    return this.getValueOfPropertyAt(t.l, t.c, tt);
  }
  _getCurrentCharIndex() {
    let t = this.get2DCursorLocation(this.selectionStart, !0), e = t.charIndex > 0 ? t.charIndex - 1 : 0;
    return {
      l: t.lineIndex,
      c: e
    };
  }
  dispose() {
    this.exitEditingImpl(), this.draggableTextDelegate.dispose(), super.dispose();
  }
};
f(ce, "ownDefaults", nh), f(ce, "type", "IText"), w.setClass(ce), w.setClass(ce, "i-text");
var yr = class ji extends ce {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...ji.ownDefaults
    };
  }
  constructor(t, e) {
    super(t, {
      ...ji.ownDefaults,
      ...e
    });
  }
  static createControls() {
    return { controls: Ko() };
  }
  initDimensions() {
    this.initialized && (this.isEditing && this.initDelayedCursor(), this._clearCache(), this.dynamicMinWidth = 0, this._styleMap = this._generateStyleMap(this._splitText()), this.dynamicMinWidth > this.width && this._set("width", this.dynamicMinWidth), this.textAlign.includes("justify") && this.enlargeSpaces(), this.height = this.calcTextHeight());
  }
  _generateStyleMap(t) {
    let e = 0, i = 0, s = 0, o = {};
    for (let n = 0; n < t.graphemeLines.length; n++) t.graphemeText[s] === `
` && n > 0 ? (i = 0, s++, e++) : !this.splitByGrapheme && this._reSpaceAndTab.test(t.graphemeText[s]) && n > 0 && (i++, s++), o[n] = {
      line: e,
      offset: i
    }, s += t.graphemeLines[n].length, i += t.graphemeLines[n].length;
    return o;
  }
  styleHas(t, e) {
    if (this._styleMap && !this.isWrapping) {
      let i = this._styleMap[e];
      i && (e = i.line);
    }
    return super.styleHas(t, e);
  }
  isEmptyStyles(t) {
    if (!this.styles) return !0;
    let e, i, s = 0, o = !1, n = this._styleMap[t], a = this._styleMap[t + 1];
    n && (t = n.line, s = n.offset), a && (e = a.line, o = e === t, i = a.offset);
    let l = t === void 0 ? this.styles : { line: this.styles[t] };
    for (let h in l) for (let c in l[h]) {
      let u = parseInt(c, 10);
      if (u >= s && (!o || u < i)) for (let d in l[h][c]) return !1;
    }
    return !0;
  }
  _getStyleDeclaration(t, e) {
    if (this._styleMap && !this.isWrapping) {
      let i = this._styleMap[t];
      if (!i) return {};
      t = i.line, e = i.offset + e;
    }
    return super._getStyleDeclaration(t, e);
  }
  _setStyleDeclaration(t, e, i) {
    let s = this._styleMap[t];
    super._setStyleDeclaration(s.line, s.offset + e, i);
  }
  _deleteStyleDeclaration(t, e) {
    let i = this._styleMap[t];
    super._deleteStyleDeclaration(i.line, i.offset + e);
  }
  _getLineStyle(t) {
    let e = this._styleMap[t];
    return !!this.styles[e.line];
  }
  _setLineStyle(t) {
    let e = this._styleMap[t];
    super._setLineStyle(e.line);
  }
  _wrapText(t, e) {
    this.isWrapping = !0;
    let i = this.getGraphemeDataForRender(t), s = [];
    for (let o = 0; o < i.wordsData.length; o++) s.push(...this._wrapLine(o, e, i));
    return this.isWrapping = !1, s;
  }
  getGraphemeDataForRender(t) {
    let e = this.splitByGrapheme, i = e ? "" : " ", s = 0;
    return {
      wordsData: t.map((o, n) => {
        let a = 0, l = e ? this.graphemeSplit(o) : this.wordSplit(o);
        return l.length === 0 ? [{
          word: [],
          width: 0
        }] : l.map((h) => {
          let c = e ? [h] : this.graphemeSplit(h), u = this._measureWord(c, n, a);
          return s = Math.max(u, s), a += c.length + i.length, {
            word: c,
            width: u
          };
        });
      }),
      largestWordWidth: s
    };
  }
  _measureWord(t, e, i = 0) {
    let s, o = 0;
    for (let n = 0, a = t.length; n < a; n++) o += this._getGraphemeBox(t[n], e, n + i, s, !0).kernedWidth, s = t[n];
    return o;
  }
  wordSplit(t) {
    return t.split(this._wordJoiners);
  }
  _wrapLine(t, e, { largestWordWidth: i, wordsData: s }, o = 0) {
    let n = this._getWidthOfCharSpacing(), a = this.splitByGrapheme, l = [], h = a ? "" : " ", c = 0, u = [], d = 0, g = 0, p = !0;
    e -= o;
    let m = Math.max(e, i, this.dynamicMinWidth), y = s[t], x;
    for (x = 0; x < y.length; x++) {
      let { word: _, width: S } = y[x];
      d += _.length, c += g + S - n, c > m && !p ? (l.push(u), u = [], c = S, p = !0) : c += n, p || a || u.push(h), u = u.concat(_), g = a ? 0 : this._measureWord([h], t, d), d++, p = !1;
    }
    return x && l.push(u), i + o > this.dynamicMinWidth && (this.dynamicMinWidth = i - n + o), l;
  }
  isEndOfWrapping(t) {
    return !this._styleMap[t + 1] || this._styleMap[t + 1].line !== this._styleMap[t].line;
  }
  missingNewlineOffset(t, e) {
    return this.splitByGrapheme && !e ? +!!this.isEndOfWrapping(t) : 1;
  }
  _splitTextIntoLines(t) {
    let e = super._splitTextIntoLines(t), i = this._wrapText(e.lines, this.width), s = Array(i.length);
    for (let o = 0; o < i.length; o++) s[o] = i[o].join("");
    return e.lines = s, e.graphemeLines = i, e;
  }
  getMinWidth() {
    return Math.max(this.minWidth, this.dynamicMinWidth);
  }
  _removeExtraneousStyles() {
    let t = /* @__PURE__ */ new Map();
    for (let e in this._styleMap) {
      let i = parseInt(e, 10);
      if (this._textLines[i]) {
        let s = this._styleMap[e].line;
        t.set(`${s}`, !0);
      }
    }
    for (let e in this.styles) t.has(e) || delete this.styles[e];
  }
  toObject(t = []) {
    return super.toObject([
      "minWidth",
      "splitByGrapheme",
      ...t
    ]);
  }
};
f(yr, "type", "Textbox"), f(yr, "textLayoutProperties", [...ce.textLayoutProperties, "width"]), f(yr, "ownDefaults", {
  minWidth: 20,
  dynamicMinWidth: 2,
  lockScalingFlip: !0,
  noScaleCache: !1,
  _wordJoiners: /[ \t\r]/,
  splitByGrapheme: !1
}), w.setClass(yr);
var $s = class extends qr {
  shouldPerformLayout(r) {
    return !!r.target.clipPath && super.shouldPerformLayout(r);
  }
  shouldLayoutClipPath() {
    return !1;
  }
  calcLayoutResult(r, t) {
    let { target: e } = r, { clipPath: i, group: s } = e;
    if (!i || !this.shouldPerformLayout(r)) return;
    let { width: o, height: n } = St(an(e, i)), a = new v(o, n);
    if (i.absolutePositioned) return {
      center: Et(i.getRelativeCenterPoint(), void 0, s ? s.calcTransformMatrix() : void 0),
      size: a
    };
    {
      let l = i.getRelativeCenterPoint().transform(e.calcOwnMatrix(), !0);
      if (this.shouldPerformLayout(r)) {
        let { center: h = new v(), correction: c = new v() } = this.calcBoundingBox(t, r) || {};
        return {
          center: h.add(l),
          correction: c.subtract(l),
          size: a
        };
      }
      return {
        center: e.getRelativeCenterPoint().add(l),
        size: a
      };
    }
  }
};
f($s, "type", "clip-path"), w.setClass($s);
var Ys = class extends qr {
  getInitialSize({ target: r }, { size: t }) {
    return new v(r.width || t.x, r.height || t.y);
  }
};
f(Ys, "type", "fixed"), w.setClass(Ys);
var ah = class extends rr {
  subscribeTargets(r) {
    let t = r.target;
    r.targets.reduce((e, i) => (i.parent && e.add(i.parent), e), /* @__PURE__ */ new Set()).forEach((e) => {
      e.layoutManager.subscribeTargets({
        target: e,
        targets: [t]
      });
    });
  }
  unsubscribeTargets(r) {
    let t = r.target, e = t.getObjects();
    r.targets.reduce((i, s) => (s.parent && i.add(s.parent), i), /* @__PURE__ */ new Set()).forEach((i) => {
      !e.some((s) => s.parent === i) && i.layoutManager.unsubscribeTargets({
        target: i,
        targets: [t]
      });
    });
  }
}, xr = class Ai extends ge {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Ai.ownDefaults
    };
  }
  constructor(t = [], e = {}) {
    super(), Object.assign(this, Ai.ownDefaults), this.setOptions(e);
    let { left: i, top: s, layoutManager: o } = e;
    this.groupInit(t, {
      left: i,
      top: s,
      layoutManager: o ?? new ah()
    });
  }
  _shouldSetNestedCoords() {
    return !0;
  }
  __objectSelectionMonitor() {
  }
  multiSelectAdd(...t) {
    this.multiSelectionStacking === "selection-order" ? this.add(...t) : t.forEach((e) => {
      let i = this._objects.findIndex((o) => o.isInFrontOf(e)), s = i === -1 ? this.size() : i;
      this.insertAt(s, e);
    });
  }
  canEnterGroup(t) {
    return this.getObjects().some((e) => e.isDescendantOf(t) || t.isDescendantOf(e)) ? (Xt("error", "ActiveSelection: circular object trees are not supported, this call has no effect"), !1) : super.canEnterGroup(t);
  }
  enterGroup(t, e) {
    t.parent && t.parent === t.group ? t.parent._exitGroup(t) : t.group && t.parent !== t.group && t.group.remove(t), this._enterGroup(t, e);
  }
  exitGroup(t, e) {
    this._exitGroup(t, e), t.parent && t.parent._enterGroup(t, !0);
  }
  _onAfterObjectsChange(t, e) {
    super._onAfterObjectsChange(t, e);
    let i = /* @__PURE__ */ new Set();
    e.forEach((s) => {
      let { parent: o } = s;
      o && i.add(o);
    }), t === "removed" ? i.forEach((s) => {
      s._onAfterObjectsChange(vi, e);
    }) : i.forEach((s) => {
      s._set("dirty", !0);
    });
  }
  onDeselect() {
    return this.removeAll(), !1;
  }
  toString() {
    return `#<ActiveSelection: (${this.complexity()})>`;
  }
  shouldCache() {
    return !1;
  }
  isOnACache() {
    return !1;
  }
  _renderControls(t, e, i) {
    t.save(), t.globalAlpha = this.isMoving ? this.borderOpacityWhenMoving : 1;
    let s = {
      hasControls: !1,
      ...i,
      forActiveSelection: !0
    };
    for (let o = 0; o < this._objects.length; o++) this._objects[o]._renderControls(t, s);
    super._renderControls(t, e), t.restore();
  }
};
f(xr, "type", "ActiveSelection"), f(xr, "ownDefaults", { multiSelectionStacking: "canvas-stacking" }), w.setClass(xr), w.setClass(xr, "activeSelection");
var lh = class {
  constructor() {
    f(this, "resources", {});
  }
  applyFilters(r, t, e, i, s) {
    let o = s.getContext("2d", {
      willReadFrequently: !0,
      desynchronized: !0
    });
    if (!o) return;
    o.drawImage(t, 0, 0, e, i);
    let n = {
      sourceWidth: e,
      sourceHeight: i,
      imageData: o.getImageData(0, 0, e, i),
      originalEl: t,
      originalImageData: o.getImageData(0, 0, e, i),
      canvasEl: s,
      ctx: o,
      filterBackend: this
    };
    r.forEach((l) => {
      l.applyTo(n);
    });
    let { imageData: a } = n;
    return a.width === e && a.height === i || (s.width = a.width, s.height = a.height), o.putImageData(a, 0, 0), n;
  }
}, Xn = class {
  constructor({ tileSize: r = P.textureSize } = {}) {
    f(this, "aPosition", new Float32Array([
      0,
      0,
      0,
      1,
      1,
      0,
      1,
      1
    ])), f(this, "resources", {}), this.tileSize = r, this.setupGLContext(r, r), this.captureGPUInfo();
  }
  setupGLContext(r, t) {
    this.dispose(), this.createWebGLCanvas(r, t);
  }
  createWebGLCanvas(r, t) {
    let e = nt({
      width: r,
      height: t
    }), i = e.getContext("webgl", {
      alpha: !0,
      premultipliedAlpha: !1,
      depth: !1,
      stencil: !1,
      antialias: !1
    });
    i && (i.clearColor(0, 0, 0, 0), this.canvas = e, this.gl = i);
  }
  applyFilters(r, t, e, i, s, o) {
    let n = this.gl, a = s.getContext("2d");
    if (!n || !a) return;
    let l;
    o && (l = this.getCachedTexture(o, t));
    let h = {
      originalWidth: t.width || t.naturalWidth || 0,
      originalHeight: t.height || t.naturalHeight || 0,
      sourceWidth: e,
      sourceHeight: i,
      destinationWidth: e,
      destinationHeight: i,
      context: n,
      sourceTexture: this.createTexture(n, e, i, l ? void 0 : t),
      targetTexture: this.createTexture(n, e, i),
      originalTexture: l || this.createTexture(n, e, i, l ? void 0 : t),
      passes: r.length,
      webgl: !0,
      aPosition: this.aPosition,
      programCache: this.programCache,
      pass: 0,
      filterBackend: this,
      targetCanvas: s
    }, c = n.createFramebuffer();
    return n.bindFramebuffer(n.FRAMEBUFFER, c), r.forEach((u) => {
      u && u.applyTo(h);
    }), (function(u) {
      let d = u.targetCanvas, g = d.width, p = d.height, m = u.destinationWidth, y = u.destinationHeight;
      g === m && p === y || (d.width = m, d.height = y);
    })(h), this.copyGLTo2D(n, h), n.bindTexture(n.TEXTURE_2D, null), n.deleteTexture(h.sourceTexture), n.deleteTexture(h.targetTexture), n.deleteFramebuffer(c), a.setTransform(1, 0, 0, 1, 0, 0), h;
  }
  dispose() {
    this.canvas && (this.canvas = null, this.gl = null), this.clearWebGLCaches();
  }
  clearWebGLCaches() {
    this.programCache = {}, this.textureCache = {};
  }
  createTexture(r, t, e, i, s) {
    let { NEAREST: o, TEXTURE_2D: n, RGBA: a, UNSIGNED_BYTE: l, CLAMP_TO_EDGE: h, TEXTURE_MAG_FILTER: c, TEXTURE_MIN_FILTER: u, TEXTURE_WRAP_S: d, TEXTURE_WRAP_T: g } = r, p = r.createTexture();
    return r.bindTexture(n, p), r.texParameteri(n, c, s || o), r.texParameteri(n, u, s || o), r.texParameteri(n, d, h), r.texParameteri(n, g, h), i ? r.texImage2D(n, 0, a, a, l, i) : r.texImage2D(n, 0, a, t, e, 0, a, l, null), p;
  }
  getCachedTexture(r, t, e) {
    let { textureCache: i } = this;
    if (i[r]) return i[r];
    {
      let s = this.createTexture(this.gl, t.width, t.height, t, e);
      return s && (i[r] = s), s;
    }
  }
  evictCachesForKey(r) {
    this.textureCache[r] && (this.gl.deleteTexture(this.textureCache[r]), delete this.textureCache[r]);
  }
  copyGLTo2D(r, t) {
    let e = r.canvas, i = t.targetCanvas, s = i.getContext("2d");
    if (!s) return;
    s.translate(0, i.height), s.scale(1, -1);
    let o = e.height - i.height;
    s.drawImage(e, 0, o, i.width, i.height, 0, 0, i.width, i.height);
  }
  copyGLTo2DPutImageData(r, t) {
    let e = t.targetCanvas.getContext("2d"), i = t.destinationWidth, s = t.destinationHeight, o = i * s * 4;
    if (!e) return;
    let n = new Uint8Array(this.imageBuffer, 0, o), a = new Uint8ClampedArray(this.imageBuffer, 0, o);
    r.readPixels(0, 0, i, s, r.RGBA, r.UNSIGNED_BYTE, n);
    let l = new ImageData(a, i, s);
    e.putImageData(l, 0, 0);
  }
  captureGPUInfo() {
    if (this.gpuInfo) return this.gpuInfo;
    let r = this.gl, t = {
      renderer: "",
      vendor: ""
    };
    if (!r) return t;
    let e = r.getExtension("WEBGL_debug_renderer_info");
    if (e) {
      let i = r.getParameter(e.UNMASKED_RENDERER_WEBGL), s = r.getParameter(e.UNMASKED_VENDOR_WEBGL);
      i && (t.renderer = i.toLowerCase()), s && (t.vendor = s.toLowerCase());
    }
    return this.gpuInfo = t, t;
  }
}, oi;
function hh() {
  let { WebGLProbe: r } = Ct();
  return r.queryWebGL(bt()), P.enableGLFiltering && r.isSupported(P.textureSize) ? new Xn({ tileSize: P.textureSize }) : new lh();
}
function ni(r = !0) {
  return !oi && r && (oi = hh()), oi;
}
var $n = ["cropX", "cropY"], Bt = class Fi extends N {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Fi.ownDefaults
    };
  }
  constructor(t, e) {
    super(), f(this, "_lastScaleX", 1), f(this, "_lastScaleY", 1), f(this, "_filterScalingX", 1), f(this, "_filterScalingY", 1), this.filters = [], Object.assign(this, Fi.ownDefaults), this.setOptions(e), this.cacheKey = `texture${$t()}`, this.setElement(typeof t == "string" ? (this.canvas && ut(this.canvas.getElement()) || _e()).getElementById(t) : t, e);
  }
  getElement() {
    return this._element;
  }
  setElement(t, e = {}) {
    this.removeTexture(this.cacheKey), this.removeTexture(`${this.cacheKey}_filtered`), this._element = t, this._originalElement = t, this._setWidthHeight(e), this.filters.length !== 0 && this.applyFilters(), this.resizeFilter && this.applyResizeFilters();
  }
  removeTexture(t) {
    let e = ni(!1);
    e instanceof Xn && e.evictCachesForKey(t);
  }
  dispose() {
    super.dispose(), this.removeTexture(this.cacheKey), this.removeTexture(`${this.cacheKey}_filtered`), this._cacheContext = null, [
      "_originalElement",
      "_element",
      "_filteredEl",
      "_cacheCanvas"
    ].forEach((t) => {
      let e = this[t];
      e && Ct().dispose(e), this[t] = void 0;
    });
  }
  getCrossOrigin() {
    return this._originalElement && (this._originalElement.crossOrigin || null);
  }
  getOriginalSize() {
    let t = this.getElement();
    return t ? {
      width: t.naturalWidth || t.width,
      height: t.naturalHeight || t.height
    } : {
      width: 0,
      height: 0
    };
  }
  _stroke(t) {
    if (!this.stroke || this.strokeWidth === 0) return;
    let e = this.width / 2, i = this.height / 2;
    t.beginPath(), t.moveTo(-e, -i), t.lineTo(e, -i), t.lineTo(e, i), t.lineTo(-e, i), t.lineTo(-e, -i), t.closePath();
  }
  toObject(t = []) {
    let e = [];
    return this.filters.forEach((i) => {
      i && e.push(i.toObject());
    }), {
      ...super.toObject([...$n, ...t]),
      src: this.getSrc(),
      crossOrigin: this.getCrossOrigin(),
      filters: e,
      ...this.resizeFilter ? { resizeFilter: this.resizeFilter.toObject() } : {}
    };
  }
  hasCrop() {
    return !!this.cropX || !!this.cropY || this.width < this._element.width || this.height < this._element.height;
  }
  _toSVG() {
    let t = [], e = this._element, i = -this.width / 2, s = -this.height / 2, o = [], n = [], a = "", l = "";
    if (!e) return [];
    if (this.hasCrop()) {
      let h = $t();
      o.push('<clipPath id="imageCrop_' + h + `">
`, '	<rect x="' + i + '" y="' + s + '" width="' + M(this.width) + '" height="' + M(this.height) + `" />
`, `</clipPath>
`), a = ' clip-path="url(#imageCrop_' + h + ')" ';
    }
    if (this.imageSmoothing || (l = ' image-rendering="optimizeSpeed"'), t.push("	<image ", "COMMON_PARTS", `xlink:href="${M(this.getSrc(!0))}" x="${i - this.cropX}" y="${s - this.cropY}" width="${e.width || e.naturalWidth}" height="${e.height || e.naturalHeight}"${l}${a}></image>
`), this.stroke || this.strokeDashArray) {
      let h = this.fill;
      this.fill = null, n = [`	<rect x="${i}" y="${s}" width="${M(this.width)}" height="${M(this.height)}" style="${this.getSvgStyles()}" />
`], this.fill = h;
    }
    return o = this.paintFirst === "fill" ? o.concat(t, n) : o.concat(n, t), o;
  }
  getSrc(t) {
    let e = t ? this._element : this._originalElement;
    return e ? e.toDataURL ? e.toDataURL() : this.srcFromAttribute ? e.getAttribute("src") || "" : e.src : this.src || "";
  }
  getSvgSrc(t) {
    return this.getSrc(t);
  }
  setSrc(t, { crossOrigin: e, signal: i } = {}) {
    return Je(t, {
      crossOrigin: e,
      signal: i
    }).then((s) => {
      e !== void 0 && this.set({ crossOrigin: e }), this.setElement(s);
    });
  }
  toString() {
    return `#<Image: { src: "${this.getSrc()}" }>`;
  }
  applyResizeFilters() {
    let t = this.resizeFilter, e = this.minimumScaleTrigger, i = this.getTotalObjectScaling(), s = i.x, o = i.y, n = this._filteredEl || this._originalElement;
    if (this.group && this.set("dirty", !0), !t || s > e && o > e) return this._element = n, this._filterScalingX = 1, this._filterScalingY = 1, this._lastScaleX = s, void (this._lastScaleY = o);
    let a = nt(n), { width: l, height: h } = n;
    this._element = a, this._lastScaleX = t.scaleX = s, this._lastScaleY = t.scaleY = o, ni().applyFilters([t], n, l, h, this._element), this._filterScalingX = a.width / this._originalElement.width, this._filterScalingY = a.height / this._originalElement.height;
  }
  applyFilters(t = this.filters || []) {
    if (t = t.filter((o) => o && !o.isNeutralState()), this.set("dirty", !0), this.removeTexture(`${this.cacheKey}_filtered`), t.length === 0) return this._element = this._originalElement, this._filteredEl = void 0, this._filterScalingX = 1, void (this._filterScalingY = 1);
    let e = this._originalElement, i = e.naturalWidth || e.width, s = e.naturalHeight || e.height;
    if (this._element === this._originalElement) {
      let o = nt({
        width: i,
        height: s
      });
      this._element = o, this._filteredEl = o;
    } else this._filteredEl && (this._element = this._filteredEl, this._filteredEl.getContext("2d").clearRect(0, 0, i, s), this._lastScaleX = 1, this._lastScaleY = 1);
    ni().applyFilters(t, this._originalElement, i, s, this._element, this.cacheKey), this._originalElement.width === this._element.width && this._originalElement.height === this._element.height || (this._filterScalingX = this._element.width / this._originalElement.width, this._filterScalingY = this._element.height / this._originalElement.height);
  }
  _render(t) {
    t.imageSmoothingEnabled = this.imageSmoothing, this.isMoving !== !0 && this.resizeFilter && this._needsResize() && this.applyResizeFilters(), this._stroke(t), this._renderPaintInOrder(t);
  }
  drawCacheOnCanvas(t) {
    t.imageSmoothingEnabled = this.imageSmoothing, super.drawCacheOnCanvas(t);
  }
  shouldCache() {
    return this.needsItsOwnCache();
  }
  _renderFill(t) {
    let e = this._element;
    if (!e) return;
    let i = this._filterScalingX, s = this._filterScalingY, o = this.width, n = this.height, a = Math.max(this.cropX, 0), l = Math.max(this.cropY, 0), h = e.naturalWidth || e.width, c = e.naturalHeight || e.height, u = a * i, d = l * s, g = Math.min(o * i, h - u), p = Math.min(n * s, c - d), m = -o / 2, y = -n / 2, x = Math.min(o, h / i - a), _ = Math.min(n, c / s - l);
    e && t.drawImage(e, u, d, g, p, m, y, x, _);
  }
  _needsResize() {
    let t = this.getTotalObjectScaling();
    return t.x !== this._lastScaleX || t.y !== this._lastScaleY;
  }
  _resetWidthHeight() {
    this.set(this.getOriginalSize());
  }
  _setWidthHeight({ width: t, height: e } = {}) {
    let i = this.getOriginalSize();
    this.width = t || i.width, this.height = e || i.height;
  }
  parsePreserveAspectRatioAttribute() {
    let t = wo(this.preserveAspectRatio || ""), e = this.width, i = this.height, s = {
      width: e,
      height: i
    }, o, n = this._element.width, a = this._element.height, l = 1, h = 1, c = 0, u = 0, d = 0, g = 0;
    return !t || t.alignX === "none" && t.alignY === "none" ? (l = e / n, h = i / a) : (t.meetOrSlice === "meet" && (l = h = hn(this._element, s), o = (e - n * l) / 2, t.alignX === "Min" && (c = -o), t.alignX === "Max" && (c = o), o = (i - a * h) / 2, t.alignY === "Min" && (u = -o), t.alignY === "Max" && (u = o)), t.meetOrSlice === "slice" && (l = h = cn(this._element, s), o = n - e / l, t.alignX === "Mid" && (d = o / 2), t.alignX === "Max" && (d = o), o = a - i / h, t.alignY === "Mid" && (g = o / 2), t.alignY === "Max" && (g = o), n = e / l, a = i / h)), {
      width: n,
      height: a,
      scaleX: l,
      scaleY: h,
      offsetLeft: c,
      offsetTop: u,
      cropX: d,
      cropY: g
    };
  }
  static fromObject({ filters: t, resizeFilter: e, src: i, crossOrigin: s, type: o, ...n }, a) {
    return Promise.all([
      Je(i, {
        ...a,
        crossOrigin: s
      }),
      t && me(t, a),
      e ? me([e], a) : [],
      or(n, a)
    ]).then(([l, h = [], [c], u = {}]) => new this(l, {
      ...n,
      src: i,
      filters: h,
      resizeFilter: c,
      ...u
    }));
  }
  static fromURL(t, { crossOrigin: e = null, signal: i } = {}, s) {
    return Je(t, {
      crossOrigin: e,
      signal: i
    }).then((o) => new this(o, s));
  }
  static async fromElement(t, e = {}, i) {
    let s = At(t, this.ATTRIBUTE_NAMES, i);
    return this.fromURL(s["xlink:href"] || s.href, e, s).catch((o) => (Xt("log", "Unable to parse Image", o), null));
  }
};
f(Bt, "type", "Image"), f(Bt, "cacheProperties", [...Pt, ...$n]), f(Bt, "ownDefaults", {
  strokeWidth: 0,
  srcFromAttribute: !1,
  minimumScaleTrigger: 0.5,
  cropX: 0,
  cropY: 0,
  imageSmoothing: !0
}), f(Bt, "ATTRIBUTE_NAMES", [
  ...zt,
  "x",
  "y",
  "width",
  "height",
  "preserveAspectRatio",
  "xlink:href",
  "href",
  "crossOrigin",
  "image-rendering"
]), w.setClass(Bt), w.setSVGClass(Bt);
var Qh = zr([
  "pattern",
  "defs",
  "symbol",
  "metadata",
  "clipPath",
  "mask",
  "desc"
]), Kr = (r) => r.webgl !== void 0, ds = "precision highp float", ch = `
    ${ds};
    varying vec2 vTexCoord;
    uniform sampler2D uTexture;
    void main() {
      gl_FragColor = texture2D(uTexture, vTexCoord);
    }`, uh = new RegExp(ds, "g"), W = class {
  get type() {
    return this.constructor.type;
  }
  constructor({ type: r, ...t } = {}) {
    Object.assign(this, this.constructor.defaults, t);
  }
  getFragmentSource() {
    return ch;
  }
  getVertexSource() {
    return `
    attribute vec2 aPosition;
    varying vec2 vTexCoord;
    void main() {
      vTexCoord = aPosition;
      gl_Position = vec4(aPosition * 2.0 - 1.0, 0.0, 1.0);
    }`;
  }
  createProgram(r, t = this.getFragmentSource(), e = this.getVertexSource()) {
    let { WebGLProbe: { GLPrecision: i = "highp" } } = Ct();
    i !== "highp" && (t = t.replace(uh, ds.replace("highp", i)));
    let s = r.createShader(r.VERTEX_SHADER), o = r.createShader(r.FRAGMENT_SHADER), n = r.createProgram();
    if (!s || !o || !n) throw new _t("Vertex, fragment shader or program creation error");
    if (r.shaderSource(s, e), r.compileShader(s), !r.getShaderParameter(s, r.COMPILE_STATUS)) throw new _t(`Vertex shader compile error for ${this.type}: ${r.getShaderInfoLog(s)}`);
    if (r.shaderSource(o, t), r.compileShader(o), !r.getShaderParameter(o, r.COMPILE_STATUS)) throw new _t(`Fragment shader compile error for ${this.type}: ${r.getShaderInfoLog(o)}`);
    if (r.attachShader(n, s), r.attachShader(n, o), r.linkProgram(n), !r.getProgramParameter(n, r.LINK_STATUS)) throw new _t(`Shader link error for "${this.type}" ${r.getProgramInfoLog(n)}`);
    let a = this.getUniformLocations(r, n) || {};
    return a.uStepW = r.getUniformLocation(n, "uStepW"), a.uStepH = r.getUniformLocation(n, "uStepH"), {
      program: n,
      attributeLocations: this.getAttributeLocations(r, n),
      uniformLocations: a
    };
  }
  getAttributeLocations(r, t) {
    return { aPosition: r.getAttribLocation(t, "aPosition") };
  }
  getUniformLocations(r, t) {
    let e = this.constructor.uniformLocations, i = {};
    for (let s = 0; s < e.length; s++) i[e[s]] = r.getUniformLocation(t, e[s]);
    return i;
  }
  sendAttributeData(r, t, e) {
    let i = t.aPosition, s = r.createBuffer();
    r.bindBuffer(r.ARRAY_BUFFER, s), r.enableVertexAttribArray(i), r.vertexAttribPointer(i, 2, r.FLOAT, !1, 0, 0), r.bufferData(r.ARRAY_BUFFER, e, r.STATIC_DRAW);
  }
  _setupFrameBuffer(r) {
    let t = r.context;
    if (r.passes > 1) {
      let e = r.destinationWidth, i = r.destinationHeight;
      r.sourceWidth === e && r.sourceHeight === i || (t.deleteTexture(r.targetTexture), r.targetTexture = r.filterBackend.createTexture(t, e, i)), t.framebufferTexture2D(t.FRAMEBUFFER, t.COLOR_ATTACHMENT0, t.TEXTURE_2D, r.targetTexture, 0);
    } else t.bindFramebuffer(t.FRAMEBUFFER, null), t.finish();
  }
  _swapTextures(r) {
    r.passes--, r.pass++;
    let t = r.targetTexture;
    r.targetTexture = r.sourceTexture, r.sourceTexture = t;
  }
  isNeutralState(r) {
    return !1;
  }
  applyTo(r) {
    Kr(r) ? (this._setupFrameBuffer(r), this.applyToWebGL(r), this._swapTextures(r)) : this.applyTo2d(r);
  }
  applyTo2d(r) {
  }
  getCacheKey() {
    return this.type;
  }
  retrieveShader(r) {
    let t = this.getCacheKey();
    return r.programCache[t] || (r.programCache[t] = this.createProgram(r.context)), r.programCache[t];
  }
  applyToWebGL(r) {
    let t = r.context, e = this.retrieveShader(r);
    r.pass === 0 && r.originalTexture ? t.bindTexture(t.TEXTURE_2D, r.originalTexture) : t.bindTexture(t.TEXTURE_2D, r.sourceTexture), t.useProgram(e.program), this.sendAttributeData(t, e.attributeLocations, r.aPosition), t.uniform1f(e.uniformLocations.uStepW, 1 / r.sourceWidth), t.uniform1f(e.uniformLocations.uStepH, 1 / r.sourceHeight), this.sendUniformData(t, e.uniformLocations), t.viewport(0, 0, r.destinationWidth, r.destinationHeight), t.drawArrays(t.TRIANGLE_STRIP, 0, 4);
  }
  bindAdditionalTexture(r, t, e) {
    r.activeTexture(e), r.bindTexture(r.TEXTURE_2D, t), r.activeTexture(r.TEXTURE0);
  }
  unbindAdditionalTexture(r, t) {
    r.activeTexture(t), r.bindTexture(r.TEXTURE_2D, null), r.activeTexture(r.TEXTURE0);
  }
  sendUniformData(r, t) {
  }
  createHelpLayer(r) {
    if (!r.helpLayer) {
      let { sourceWidth: t, sourceHeight: e } = r;
      r.helpLayer = nt({
        width: t,
        height: e
      });
    }
  }
  toObject() {
    let r = Object.keys(this.constructor.defaults || {});
    return {
      type: this.type,
      ...r.reduce((t, e) => (t[e] = this[e], t), {})
    };
  }
  toJSON() {
    return this.toObject();
  }
  static async fromObject({ type: r, ...t }, e) {
    return new this(t);
  }
};
f(W, "type", "BaseFilter"), f(W, "uniformLocations", []);
var dh = {
  multiply: `gl_FragColor.rgb *= uColor.rgb;
`,
  screen: `gl_FragColor.rgb = 1.0 - (1.0 - gl_FragColor.rgb) * (1.0 - uColor.rgb);
`,
  add: `gl_FragColor.rgb += uColor.rgb;
`,
  difference: `gl_FragColor.rgb = abs(gl_FragColor.rgb - uColor.rgb);
`,
  subtract: `gl_FragColor.rgb -= uColor.rgb;
`,
  lighten: `gl_FragColor.rgb = max(gl_FragColor.rgb, uColor.rgb);
`,
  darken: `gl_FragColor.rgb = min(gl_FragColor.rgb, uColor.rgb);
`,
  exclusion: `gl_FragColor.rgb += uColor.rgb - 2.0 * (uColor.rgb * gl_FragColor.rgb);
`,
  overlay: `
    if (uColor.r < 0.5) {
      gl_FragColor.r *= 2.0 * uColor.r;
    } else {
      gl_FragColor.r = 1.0 - 2.0 * (1.0 - gl_FragColor.r) * (1.0 - uColor.r);
    }
    if (uColor.g < 0.5) {
      gl_FragColor.g *= 2.0 * uColor.g;
    } else {
      gl_FragColor.g = 1.0 - 2.0 * (1.0 - gl_FragColor.g) * (1.0 - uColor.g);
    }
    if (uColor.b < 0.5) {
      gl_FragColor.b *= 2.0 * uColor.b;
    } else {
      gl_FragColor.b = 1.0 - 2.0 * (1.0 - gl_FragColor.b) * (1.0 - uColor.b);
    }
    `,
  tint: `
    gl_FragColor.rgb *= (1.0 - uColor.a);
    gl_FragColor.rgb += uColor.rgb;
    `
}, Ae = class extends W {
  getCacheKey() {
    return `${this.type}_${this.mode}`;
  }
  getFragmentSource() {
    return `
      precision highp float;
      uniform sampler2D uTexture;
      uniform vec4 uColor;
      varying vec2 vTexCoord;
      void main() {
        vec4 color = texture2D(uTexture, vTexCoord);
        gl_FragColor = color;
        if (color.a > 0.0) {
          ${dh[this.mode]}
        }
      }
      `;
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = new et(this.color).getSource(), e = this.alpha, i = t[0] * e, s = t[1] * e, o = t[2] * e, n = 1 - e;
    for (let a = 0; a < r.length; a += 4) {
      let l = r[a], h = r[a + 1], c = r[a + 2], u, d, g;
      switch (this.mode) {
        case "multiply":
          u = l * i / 255, d = h * s / 255, g = c * o / 255;
          break;
        case "screen":
          u = 255 - (255 - l) * (255 - i) / 255, d = 255 - (255 - h) * (255 - s) / 255, g = 255 - (255 - c) * (255 - o) / 255;
          break;
        case "add":
          u = l + i, d = h + s, g = c + o;
          break;
        case "difference":
          u = Math.abs(l - i), d = Math.abs(h - s), g = Math.abs(c - o);
          break;
        case "subtract":
          u = l - i, d = h - s, g = c - o;
          break;
        case "darken":
          u = Math.min(l, i), d = Math.min(h, s), g = Math.min(c, o);
          break;
        case "lighten":
          u = Math.max(l, i), d = Math.max(h, s), g = Math.max(c, o);
          break;
        case "overlay":
          u = i < 128 ? 2 * l * i / 255 : 255 - 2 * (255 - l) * (255 - i) / 255, d = s < 128 ? 2 * h * s / 255 : 255 - 2 * (255 - h) * (255 - s) / 255, g = o < 128 ? 2 * c * o / 255 : 255 - 2 * (255 - c) * (255 - o) / 255;
          break;
        case "exclusion":
          u = i + l - 2 * i * l / 255, d = s + h - 2 * s * h / 255, g = o + c - 2 * o * c / 255;
          break;
        case "tint":
          u = i + l * n, d = s + h * n, g = o + c * n;
      }
      r[a] = u, r[a + 1] = d, r[a + 2] = g;
    }
  }
  sendUniformData(r, t) {
    let e = new et(this.color).getSource();
    e[0] = this.alpha * e[0] / 255, e[1] = this.alpha * e[1] / 255, e[2] = this.alpha * e[2] / 255, e[3] = this.alpha, r.uniform4fv(t.uColor, e);
  }
};
f(Ae, "defaults", {
  color: "#F95C63",
  mode: "multiply",
  alpha: 1
}), f(Ae, "type", "BlendColor"), f(Ae, "uniformLocations", ["uColor"]), w.setClass(Ae);
var gh = {
  multiply: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform sampler2D uImage;
    uniform vec4 uColor;
    varying vec2 vTexCoord;
    varying vec2 vTexCoord2;
    void main() {
      vec4 color = texture2D(uTexture, vTexCoord);
      vec4 color2 = texture2D(uImage, vTexCoord2);
      color.rgba *= color2.rgba;
      gl_FragColor = color;
    }
    `,
  mask: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform sampler2D uImage;
    uniform vec4 uColor;
    varying vec2 vTexCoord;
    varying vec2 vTexCoord2;
    void main() {
      vec4 color = texture2D(uTexture, vTexCoord);
      vec4 color2 = texture2D(uImage, vTexCoord2);
      color.a = color2.a;
      gl_FragColor = color;
    }
    `
}, Fe = class extends W {
  getCacheKey() {
    return `${this.type}_${this.mode}`;
  }
  getFragmentSource() {
    return gh[this.mode];
  }
  getVertexSource() {
    return `
    attribute vec2 aPosition;
    varying vec2 vTexCoord;
    varying vec2 vTexCoord2;
    uniform mat3 uTransformMatrix;
    void main() {
      vTexCoord = aPosition;
      vTexCoord2 = (uTransformMatrix * vec3(aPosition, 1.0)).xy;
      gl_Position = vec4(aPosition * 2.0 - 1.0, 0.0, 1.0);
    }
    `;
  }
  applyToWebGL(r) {
    let t = r.context, e = this.createTexture(r.filterBackend, this.image);
    this.bindAdditionalTexture(t, e, t.TEXTURE1), super.applyToWebGL(r), this.unbindAdditionalTexture(t, t.TEXTURE1);
  }
  createTexture(r, t) {
    return r.getCachedTexture(t.cacheKey, t.getElement());
  }
  calculateMatrix() {
    let r = this.image, { width: t, height: e } = r.getElement();
    return [
      1 / r.scaleX,
      0,
      0,
      0,
      1 / r.scaleY,
      0,
      -r.left / t,
      -r.top / e,
      1
    ];
  }
  applyTo2d({ imageData: { data: r, width: t, height: e }, filterBackend: { resources: i } }) {
    let s = this.image;
    i.blendImage || (i.blendImage = bt());
    let o = i.blendImage, n = o.getContext("2d");
    o.width !== t || o.height !== e ? (o.width = t, o.height = e) : n.clearRect(0, 0, t, e), n.setTransform(s.scaleX, 0, 0, s.scaleY, s.left, s.top), n.drawImage(s.getElement(), 0, 0, t, e);
    let a = n.getImageData(0, 0, t, e).data;
    for (let l = 0; l < r.length; l += 4) {
      let h = r[l], c = r[l + 1], u = r[l + 2], d = r[l + 3], g = a[l], p = a[l + 1], m = a[l + 2], y = a[l + 3];
      switch (this.mode) {
        case "multiply":
          r[l] = h * g / 255, r[l + 1] = c * p / 255, r[l + 2] = u * m / 255, r[l + 3] = d * y / 255;
          break;
        case "mask":
          r[l + 3] = y;
      }
    }
  }
  sendUniformData(r, t) {
    let e = this.calculateMatrix();
    r.uniform1i(t.uImage, 1), r.uniformMatrix3fv(t.uTransformMatrix, !1, e);
  }
  toObject() {
    return {
      ...super.toObject(),
      image: this.image && this.image.toObject()
    };
  }
  static async fromObject({ type: r, image: t, ...e }, i) {
    return Bt.fromObject(t, i).then((s) => new this({
      ...e,
      image: s
    }));
  }
};
f(Fe, "type", "BlendImage"), f(Fe, "defaults", {
  mode: "multiply",
  alpha: 1
}), f(Fe, "uniformLocations", ["uTransformMatrix", "uImage"]), w.setClass(Fe);
var Le = class extends W {
  getFragmentSource() {
    return `
    precision highp float;
    uniform sampler2D uTexture;
    uniform vec2 uDelta;
    varying vec2 vTexCoord;
    const float nSamples = 15.0;
    vec3 v3offset = vec3(12.9898, 78.233, 151.7182);
    float random(vec3 scale) {
      /* use the fragment position for a different seed per-pixel */
      return fract(sin(dot(gl_FragCoord.xyz, scale)) * 43758.5453);
    }
    void main() {
      vec4 color = vec4(0.0);
      float totalC = 0.0;
      float totalA = 0.0;
      float offset = random(v3offset);
      for (float t = -nSamples; t <= nSamples; t++) {
        float percent = (t + offset - 0.5) / nSamples;
        vec4 sample = texture2D(uTexture, vTexCoord + uDelta * percent);
        float weight = 1.0 - abs(percent);
        float alpha = weight * sample.a;
        color.rgb += sample.rgb * alpha;
        color.a += alpha;
        totalA += weight;
        totalC += alpha;
      }
      gl_FragColor.rgb = color.rgb / totalC;
      gl_FragColor.a = color.a / totalA;
    }
  `;
  }
  applyTo(r) {
    Kr(r) ? (this.aspectRatio = r.sourceWidth / r.sourceHeight, r.passes++, this._setupFrameBuffer(r), this.horizontal = !0, this.applyToWebGL(r), this._swapTextures(r), this._setupFrameBuffer(r), this.horizontal = !1, this.applyToWebGL(r), this._swapTextures(r)) : this.applyTo2d(r);
  }
  applyTo2d({ imageData: { data: r, width: t, height: e } }) {
    this.aspectRatio = t / e, this.horizontal = !0;
    let i = this.getBlurValue() * t, s = new Uint8ClampedArray(r), o = 4 * t;
    for (let n = 0; n < r.length; n += 4) {
      let a = 0, l = 0, h = 0, c = 0, u = 0, d = n - n % o, g = d + o;
      for (let p = -14; p < 15; p++) {
        let m = p / 15, y = 4 * Math.floor(i * m), x = 1 - Math.abs(m), _ = n + y;
        _ < d ? _ = d : _ > g && (_ = g);
        let S = r[_ + 3] * x;
        a += r[_] * S, l += r[_ + 1] * S, h += r[_ + 2] * S, c += S, u += x;
      }
      s[n] = a / c, s[n + 1] = l / c, s[n + 2] = h / c, s[n + 3] = c / u;
    }
    this.horizontal = !1, i = this.getBlurValue() * e;
    for (let n = 0; n < s.length; n += 4) {
      let a = 0, l = 0, h = 0, c = 0, u = 0, d = n % o, g = s.length - o + d;
      for (let p = -14; p < 15; p++) {
        let m = p / 15, y = Math.floor(i * m) * o, x = 1 - Math.abs(m), _ = n + y;
        _ < d ? _ = d : _ > g && (_ = g);
        let S = s[_ + 3] * x;
        a += s[_] * S, l += s[_ + 1] * S, h += s[_ + 2] * S, c += S, u += x;
      }
      r[n] = a / c, r[n + 1] = l / c, r[n + 2] = h / c, r[n + 3] = c / u;
    }
  }
  sendUniformData(r, t) {
    let e = this.chooseRightDelta();
    r.uniform2fv(t.uDelta, e);
  }
  isNeutralState() {
    return this.blur === 0;
  }
  getBlurValue() {
    let r = 1, { horizontal: t, aspectRatio: e } = this;
    return t ? e > 1 && (r = 1 / e) : e < 1 && (r = e), r * this.blur * 0.12;
  }
  chooseRightDelta() {
    let r = this.getBlurValue();
    return this.horizontal ? [r, 0] : [0, r];
  }
};
f(Le, "type", "Blur"), f(Le, "defaults", { blur: 0 }), f(Le, "uniformLocations", ["uDelta"]), w.setClass(Le);
var Re = class extends W {
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform float uBrightness;
  varying vec2 vTexCoord;
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    color.rgb += uBrightness;
    gl_FragColor = color;
  }
`;
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = Math.round(255 * this.brightness);
    for (let e = 0; e < r.length; e += 4) r[e] += t, r[e + 1] += t, r[e + 2] += t;
  }
  isNeutralState() {
    return this.brightness === 0;
  }
  sendUniformData(r, t) {
    r.uniform1f(t.uBrightness, this.brightness);
  }
};
f(Re, "type", "Brightness"), f(Re, "defaults", { brightness: 0 }), f(Re, "uniformLocations", ["uBrightness"]), w.setClass(Re);
var Yn = {
  matrix: [
    1,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    1,
    0
  ],
  colorsOnly: !0
}, Qt = class extends W {
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  varying vec2 vTexCoord;
  uniform mat4 uColorMatrix;
  uniform vec4 uConstants;
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    color *= uColorMatrix;
    color += uConstants;
    gl_FragColor = color;
  }`;
  }
  applyTo2d(r) {
    let t = r.imageData.data, e = this.matrix, i = this.colorsOnly;
    for (let s = 0; s < t.length; s += 4) {
      let o = t[s], n = t[s + 1], a = t[s + 2];
      if (t[s] = o * e[0] + n * e[1] + a * e[2] + 255 * e[4], t[s + 1] = o * e[5] + n * e[6] + a * e[7] + 255 * e[9], t[s + 2] = o * e[10] + n * e[11] + a * e[12] + 255 * e[14], !i) {
        let l = t[s + 3];
        t[s] += l * e[3], t[s + 1] += l * e[8], t[s + 2] += l * e[13], t[s + 3] = o * e[15] + n * e[16] + a * e[17] + l * e[18] + 255 * e[19];
      }
    }
  }
  sendUniformData(r, t) {
    let e = this.matrix, i = [
      e[0],
      e[1],
      e[2],
      e[3],
      e[5],
      e[6],
      e[7],
      e[8],
      e[10],
      e[11],
      e[12],
      e[13],
      e[15],
      e[16],
      e[17],
      e[18]
    ], s = [
      e[4],
      e[9],
      e[14],
      e[19]
    ];
    r.uniformMatrix4fv(t.uColorMatrix, !1, i), r.uniform4fv(t.uConstants, s);
  }
  toObject() {
    return {
      ...super.toObject(),
      matrix: [...this.matrix]
    };
  }
};
function ie(r, t) {
  var e;
  let i = (f(e = class extends Qt {
    toObject() {
      return {
        type: this.type,
        colorsOnly: this.colorsOnly
      };
    }
  }, "type", r), f(e, "defaults", {
    colorsOnly: !1,
    matrix: t
  }), e);
  return w.setClass(i, r), i;
}
f(Qt, "type", "ColorMatrix"), f(Qt, "defaults", Yn), f(Qt, "uniformLocations", ["uColorMatrix", "uConstants"]), w.setClass(Qt);
var fh = ie("Brownie", [
  0.5997,
  0.34553,
  -0.27082,
  0,
  0.186,
  -0.0377,
  0.86095,
  0.15059,
  0,
  -0.1449,
  0.24113,
  -0.07441,
  0.44972,
  0,
  -0.02965,
  0,
  0,
  0,
  1,
  0
]), ph = ie("Vintage", [
  0.62793,
  0.32021,
  -0.03965,
  0,
  0.03784,
  0.02578,
  0.64411,
  0.03259,
  0,
  0.02926,
  0.0466,
  -0.08512,
  0.52416,
  0,
  0.02023,
  0,
  0,
  0,
  1,
  0
]), mh = ie("Kodachrome", [
  1.12855,
  -0.39673,
  -0.03992,
  0,
  0.24991,
  -0.16404,
  1.08352,
  -0.05498,
  0,
  0.09698,
  -0.16786,
  -0.56034,
  1.60148,
  0,
  0.13972,
  0,
  0,
  0,
  1,
  0
]), vh = ie("Technicolor", [
  1.91252,
  -0.85453,
  -0.09155,
  0,
  0.04624,
  -0.30878,
  1.76589,
  -0.10601,
  0,
  -0.27589,
  -0.2311,
  -0.75018,
  1.84759,
  0,
  0.12137,
  0,
  0,
  0,
  1,
  0
]), yh = ie("Polaroid", [
  1.438,
  -0.062,
  -0.062,
  0,
  0,
  -0.122,
  1.378,
  -0.122,
  0,
  0,
  -0.016,
  -0.016,
  1.483,
  0,
  0,
  0,
  0,
  0,
  1,
  0
]), xh = ie("Sepia", [
  0.393,
  0.769,
  0.189,
  0,
  0,
  0.349,
  0.686,
  0.168,
  0,
  0,
  0.272,
  0.534,
  0.131,
  0,
  0,
  0,
  0,
  0,
  1,
  0
]), _h = ie("BlackWhite", [
  1.5,
  1.5,
  1.5,
  0,
  -1,
  1.5,
  1.5,
  1.5,
  0,
  -1,
  1.5,
  1.5,
  1.5,
  0,
  -1,
  0,
  0,
  0,
  1,
  0
]), Li = class extends W {
  constructor(r = {}) {
    super(r), this.subFilters = r.subFilters || [];
  }
  applyTo(r) {
    Kr(r) && (r.passes += this.subFilters.length - 1), this.subFilters.forEach((t) => {
      t.applyTo(r);
    });
  }
  toObject() {
    return {
      type: this.type,
      subFilters: this.subFilters.map((r) => r.toObject())
    };
  }
  isNeutralState() {
    return !this.subFilters.some((r) => !r.isNeutralState());
  }
  static fromObject(r, t) {
    return Promise.all((r.subFilters || []).map((e) => w.getClass(e.type).fromObject(e, t))).then((e) => new this({ subFilters: e }));
  }
};
f(Li, "type", "Composed"), w.setClass(Li);
var Ie = class extends W {
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform float uContrast;
  varying vec2 vTexCoord;
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    float contrastF = 1.015 * (uContrast + 1.0) / (1.0 * (1.015 - uContrast));
    color.rgb = contrastF * (color.rgb - 0.5) + 0.5;
    gl_FragColor = color;
  }`;
  }
  isNeutralState() {
    return this.contrast === 0;
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = Math.floor(255 * this.contrast), e = 259 * (t + 255) / (255 * (259 - t));
    for (let i = 0; i < r.length; i += 4) r[i] = e * (r[i] - 128) + 128, r[i + 1] = e * (r[i + 1] - 128) + 128, r[i + 2] = e * (r[i + 2] - 128) + 128;
  }
  sendUniformData(r, t) {
    r.uniform1f(t.uContrast, this.contrast);
  }
};
f(Ie, "type", "Contrast"), f(Ie, "defaults", { contrast: 0 }), f(Ie, "uniformLocations", ["uContrast"]), w.setClass(Ie);
var Sh = {
  Convolute_3_1: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[9];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 0);
      for (float h = 0.0; h < 3.0; h+=1.0) {
        for (float w = 0.0; w < 3.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 1), uStepH * (h - 1));
          color += texture2D(uTexture, vTexCoord + matrixPos) * uMatrix[int(h * 3.0 + w)];
        }
      }
      gl_FragColor = color;
    }
    `,
  Convolute_3_0: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[9];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 1);
      for (float h = 0.0; h < 3.0; h+=1.0) {
        for (float w = 0.0; w < 3.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 1.0), uStepH * (h - 1.0));
          color.rgb += texture2D(uTexture, vTexCoord + matrixPos).rgb * uMatrix[int(h * 3.0 + w)];
        }
      }
      float alpha = texture2D(uTexture, vTexCoord).a;
      gl_FragColor = color;
      gl_FragColor.a = alpha;
    }
    `,
  Convolute_5_1: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[25];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 0);
      for (float h = 0.0; h < 5.0; h+=1.0) {
        for (float w = 0.0; w < 5.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 2.0), uStepH * (h - 2.0));
          color += texture2D(uTexture, vTexCoord + matrixPos) * uMatrix[int(h * 5.0 + w)];
        }
      }
      gl_FragColor = color;
    }
    `,
  Convolute_5_0: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[25];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 1);
      for (float h = 0.0; h < 5.0; h+=1.0) {
        for (float w = 0.0; w < 5.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 2.0), uStepH * (h - 2.0));
          color.rgb += texture2D(uTexture, vTexCoord + matrixPos).rgb * uMatrix[int(h * 5.0 + w)];
        }
      }
      float alpha = texture2D(uTexture, vTexCoord).a;
      gl_FragColor = color;
      gl_FragColor.a = alpha;
    }
    `,
  Convolute_7_1: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[49];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 0);
      for (float h = 0.0; h < 7.0; h+=1.0) {
        for (float w = 0.0; w < 7.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 3.0), uStepH * (h - 3.0));
          color += texture2D(uTexture, vTexCoord + matrixPos) * uMatrix[int(h * 7.0 + w)];
        }
      }
      gl_FragColor = color;
    }
    `,
  Convolute_7_0: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[49];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 1);
      for (float h = 0.0; h < 7.0; h+=1.0) {
        for (float w = 0.0; w < 7.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 3.0), uStepH * (h - 3.0));
          color.rgb += texture2D(uTexture, vTexCoord + matrixPos).rgb * uMatrix[int(h * 7.0 + w)];
        }
      }
      float alpha = texture2D(uTexture, vTexCoord).a;
      gl_FragColor = color;
      gl_FragColor.a = alpha;
    }
    `,
  Convolute_9_1: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[81];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 0);
      for (float h = 0.0; h < 9.0; h+=1.0) {
        for (float w = 0.0; w < 9.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 4.0), uStepH * (h - 4.0));
          color += texture2D(uTexture, vTexCoord + matrixPos) * uMatrix[int(h * 9.0 + w)];
        }
      }
      gl_FragColor = color;
    }
    `,
  Convolute_9_0: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform float uMatrix[81];
    uniform float uStepW;
    uniform float uStepH;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = vec4(0, 0, 0, 1);
      for (float h = 0.0; h < 9.0; h+=1.0) {
        for (float w = 0.0; w < 9.0; w+=1.0) {
          vec2 matrixPos = vec2(uStepW * (w - 4.0), uStepH * (h - 4.0));
          color.rgb += texture2D(uTexture, vTexCoord + matrixPos).rgb * uMatrix[int(h * 9.0 + w)];
        }
      }
      float alpha = texture2D(uTexture, vTexCoord).a;
      gl_FragColor = color;
      gl_FragColor.a = alpha;
    }
    `
}, Be = class extends W {
  getCacheKey() {
    return `${this.type}_${Math.sqrt(this.matrix.length)}_${+!!this.opaque}`;
  }
  getFragmentSource() {
    return Sh[this.getCacheKey()];
  }
  applyTo2d(r) {
    let t = r.imageData, e = t.data, i = this.matrix, s = Math.round(Math.sqrt(i.length)), o = Math.floor(s / 2), n = t.width, a = t.height, l = r.ctx.createImageData(n, a), h = l.data, c = +!!this.opaque, u, d, g, p, m, y, x, _, S, C, b, O, T;
    for (b = 0; b < a; b++) for (C = 0; C < n; C++) {
      for (m = 4 * (b * n + C), u = 0, d = 0, g = 0, p = 0, T = 0; T < s; T++) for (O = 0; O < s; O++) x = b + T - o, y = C + O - o, x < 0 || x >= a || y < 0 || y >= n || (_ = 4 * (x * n + y), S = i[T * s + O], u += e[_] * S, d += e[_ + 1] * S, g += e[_ + 2] * S, c || (p += e[_ + 3] * S));
      h[m] = u, h[m + 1] = d, h[m + 2] = g, h[m + 3] = c ? e[m + 3] : p;
    }
    r.imageData = l;
  }
  sendUniformData(r, t) {
    r.uniform1fv(t.uMatrix, this.matrix);
  }
  toObject() {
    return {
      ...super.toObject(),
      opaque: this.opaque,
      matrix: [...this.matrix]
    };
  }
};
f(Be, "type", "Convolute"), f(Be, "defaults", {
  opaque: !1,
  matrix: [
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0
  ]
}), f(Be, "uniformLocations", [
  "uMatrix",
  "uOpaque",
  "uHalfSize",
  "uSize"
]), w.setClass(Be);
var Wn = "Gamma", Xe = class extends W {
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform vec3 uGamma;
  varying vec2 vTexCoord;
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    vec3 correction = (1.0 / uGamma);
    color.r = pow(color.r, correction.r);
    color.g = pow(color.g, correction.g);
    color.b = pow(color.b, correction.b);
    gl_FragColor = color;
    gl_FragColor.rgb *= color.a;
  }
`;
  }
  constructor(r = {}) {
    super(r), this.gamma = r.gamma || this.constructor.defaults.gamma.concat();
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = this.gamma, e = 1 / t[0], i = 1 / t[1], s = 1 / t[2];
    this.rgbValues || (this.rgbValues = {
      r: /* @__PURE__ */ new Uint8Array(256),
      g: /* @__PURE__ */ new Uint8Array(256),
      b: /* @__PURE__ */ new Uint8Array(256)
    });
    let o = this.rgbValues;
    for (let n = 0; n < 256; n++) o.r[n] = 255 * (n / 255) ** e, o.g[n] = 255 * (n / 255) ** i, o.b[n] = 255 * (n / 255) ** s;
    for (let n = 0; n < r.length; n += 4) r[n] = o.r[r[n]], r[n + 1] = o.g[r[n + 1]], r[n + 2] = o.b[r[n + 2]];
  }
  sendUniformData(r, t) {
    r.uniform3fv(t.uGamma, this.gamma);
  }
  isNeutralState() {
    let { gamma: r } = this;
    return r[0] === 1 && r[1] === 1 && r[2] === 1;
  }
  toObject() {
    return {
      type: Wn,
      gamma: this.gamma.concat()
    };
  }
};
f(Xe, "type", Wn), f(Xe, "defaults", { gamma: [
  1,
  1,
  1
] }), f(Xe, "uniformLocations", ["uGamma"]), w.setClass(Xe);
var Ch = {
  average: `
    precision highp float;
    uniform sampler2D uTexture;
    varying vec2 vTexCoord;
    void main() {
      vec4 color = texture2D(uTexture, vTexCoord);
      float average = (color.r + color.b + color.g) / 3.0;
      gl_FragColor = vec4(average, average, average, color.a);
    }
    `,
  lightness: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform int uMode;
    varying vec2 vTexCoord;
    void main() {
      vec4 col = texture2D(uTexture, vTexCoord);
      float average = (max(max(col.r, col.g),col.b) + min(min(col.r, col.g),col.b)) / 2.0;
      gl_FragColor = vec4(average, average, average, col.a);
    }
    `,
  luminosity: `
    precision highp float;
    uniform sampler2D uTexture;
    uniform int uMode;
    varying vec2 vTexCoord;
    void main() {
      vec4 col = texture2D(uTexture, vTexCoord);
      float average = 0.21 * col.r + 0.72 * col.g + 0.07 * col.b;
      gl_FragColor = vec4(average, average, average, col.a);
    }
    `
}, $e = class extends W {
  applyTo2d({ imageData: { data: r } }) {
    for (let t, e = 0; e < r.length; e += 4) {
      let i = r[e], s = r[e + 1], o = r[e + 2];
      switch (this.mode) {
        case "average":
          t = (i + s + o) / 3;
          break;
        case "lightness":
          t = (Math.min(i, s, o) + Math.max(i, s, o)) / 2;
          break;
        case "luminosity":
          t = 0.21 * i + 0.72 * s + 0.07 * o;
      }
      r[e + 2] = r[e + 1] = r[e] = t;
    }
  }
  getCacheKey() {
    return `${this.type}_${this.mode}`;
  }
  getFragmentSource() {
    return Ch[this.mode];
  }
  sendUniformData(r, t) {
    r.uniform1i(t.uMode, 1);
  }
  isNeutralState() {
    return !1;
  }
};
f($e, "type", "Grayscale"), f($e, "defaults", { mode: "average" }), f($e, "uniformLocations", ["uMode"]), w.setClass($e);
var bh = {
  ...Yn,
  rotation: 0
}, kr = class extends Qt {
  calculateMatrix() {
    let r = this.rotation * Math.PI, t = mt(r), e = vt(r), i = 1 / 3, s = Math.sqrt(i) * e, o = 1 - t;
    this.matrix = [
      t + o / 3,
      i * o - s,
      i * o + s,
      0,
      0,
      i * o + s,
      t + i * o,
      i * o - s,
      0,
      0,
      i * o - s,
      i * o + s,
      t + i * o,
      0,
      0,
      0,
      0,
      0,
      1,
      0
    ];
  }
  isNeutralState() {
    return this.rotation === 0;
  }
  applyTo(r) {
    this.calculateMatrix(), super.applyTo(r);
  }
  toObject() {
    return {
      type: this.type,
      rotation: this.rotation
    };
  }
};
f(kr, "type", "HueRotation"), f(kr, "defaults", bh), w.setClass(kr);
var Ye = class extends W {
  applyTo2d({ imageData: { data: r } }) {
    for (let t = 0; t < r.length; t += 4) r[t] = 255 - r[t], r[t + 1] = 255 - r[t + 1], r[t + 2] = 255 - r[t + 2], this.alpha && (r[t + 3] = 255 - r[t + 3]);
  }
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform int uInvert;
  uniform int uAlpha;
  varying vec2 vTexCoord;
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    if (uInvert == 1) {
      if (uAlpha == 1) {
        gl_FragColor = vec4(1.0 - color.r,1.0 -color.g,1.0 -color.b,1.0 -color.a);
      } else {
        gl_FragColor = vec4(1.0 - color.r,1.0 -color.g,1.0 -color.b,color.a);
      }
    } else {
      gl_FragColor = color;
    }
  }
`;
  }
  isNeutralState() {
    return !this.invert;
  }
  sendUniformData(r, t) {
    r.uniform1i(t.uInvert, Number(this.invert)), r.uniform1i(t.uAlpha, Number(this.alpha));
  }
};
f(Ye, "type", "Invert"), f(Ye, "defaults", {
  alpha: !1,
  invert: !0
}), f(Ye, "uniformLocations", ["uInvert", "uAlpha"]), w.setClass(Ye);
var We = class extends W {
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform float uStepH;
  uniform float uNoise;
  uniform float uSeed;
  varying vec2 vTexCoord;
  float rand(vec2 co, float seed, float vScale) {
    return fract(sin(dot(co.xy * vScale ,vec2(12.9898 , 78.233))) * 43758.5453 * (seed + 0.01) / 2.0);
  }
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    color.rgb += (0.5 - rand(vTexCoord, uSeed, 0.1 / uStepH)) * uNoise;
    gl_FragColor = color;
  }
`;
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = this.noise;
    for (let e = 0; e < r.length; e += 4) {
      let i = (0.5 - Math.random()) * t;
      r[e] += i, r[e + 1] += i, r[e + 2] += i;
    }
  }
  sendUniformData(r, t) {
    r.uniform1f(t.uNoise, this.noise / 255), r.uniform1f(t.uSeed, Math.random());
  }
  isNeutralState() {
    return this.noise === 0;
  }
};
f(We, "type", "Noise"), f(We, "defaults", { noise: 0 }), f(We, "uniformLocations", ["uNoise", "uSeed"]), w.setClass(We);
var Ve = class extends W {
  applyTo2d({ imageData: { data: r, width: t, height: e } }) {
    for (let i = 0; i < e; i += this.blocksize) for (let s = 0; s < t; s += this.blocksize) {
      let o = 4 * i * t + 4 * s, n = r[o], a = r[o + 1], l = r[o + 2], h = r[o + 3];
      for (let c = i; c < Math.min(i + this.blocksize, e); c++) for (let u = s; u < Math.min(s + this.blocksize, t); u++) {
        let d = 4 * c * t + 4 * u;
        r[d] = n, r[d + 1] = a, r[d + 2] = l, r[d + 3] = h;
      }
    }
  }
  isNeutralState() {
    return this.blocksize === 1;
  }
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform float uBlocksize;
  uniform float uStepW;
  uniform float uStepH;
  varying vec2 vTexCoord;
  void main() {
    float blockW = uBlocksize * uStepW;
    float blockH = uBlocksize * uStepH;
    int posX = int(vTexCoord.x / blockW);
    int posY = int(vTexCoord.y / blockH);
    float fposX = float(posX);
    float fposY = float(posY);
    vec2 squareCoords = vec2(fposX * blockW, fposY * blockH);
    vec4 color = texture2D(uTexture, squareCoords);
    gl_FragColor = color;
  }
`;
  }
  sendUniformData(r, t) {
    r.uniform1f(t.uBlocksize, this.blocksize);
  }
};
f(Ve, "type", "Pixelate"), f(Ve, "defaults", { blocksize: 4 }), f(Ve, "uniformLocations", ["uBlocksize"]), w.setClass(Ve);
var He = class extends W {
  getFragmentSource() {
    return `
precision highp float;
uniform sampler2D uTexture;
uniform vec4 uLow;
uniform vec4 uHigh;
varying vec2 vTexCoord;
void main() {
  gl_FragColor = texture2D(uTexture, vTexCoord);
  if(all(greaterThan(gl_FragColor.rgb,uLow.rgb)) && all(greaterThan(uHigh.rgb,gl_FragColor.rgb))) {
    gl_FragColor.a = 0.0;
  }
}
`;
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = 255 * this.distance, e = new et(this.color).getSource(), i = [
      e[0] - t,
      e[1] - t,
      e[2] - t
    ], s = [
      e[0] + t,
      e[1] + t,
      e[2] + t
    ];
    for (let o = 0; o < r.length; o += 4) {
      let n = r[o], a = r[o + 1], l = r[o + 2];
      n > i[0] && a > i[1] && l > i[2] && n < s[0] && a < s[1] && l < s[2] && (r[o + 3] = 0);
    }
  }
  sendUniformData(r, t) {
    let e = new et(this.color).getSource(), i = this.distance, s = [
      0 + e[0] / 255 - i,
      0 + e[1] / 255 - i,
      0 + e[2] / 255 - i,
      1
    ], o = [
      e[0] / 255 + i,
      e[1] / 255 + i,
      e[2] / 255 + i,
      1
    ];
    r.uniform4fv(t.uLow, s), r.uniform4fv(t.uHigh, o);
  }
};
f(He, "type", "RemoveColor"), f(He, "defaults", {
  color: "#FFFFFF",
  distance: 0.02,
  useAlpha: !1
}), f(He, "uniformLocations", ["uLow", "uHigh"]), w.setClass(He);
var ze = class extends W {
  sendUniformData(r, t) {
    r.uniform2fv(t.uDelta, this.horizontal ? [1 / this.width, 0] : [0, 1 / this.height]), r.uniform1fv(t.uTaps, this.taps);
  }
  getFilterWindow() {
    let r = this.tempScale;
    return Math.ceil(this.lanczosLobes / r);
  }
  getCacheKey() {
    let r = this.getFilterWindow();
    return `${this.type}_${r}`;
  }
  getFragmentSource() {
    let r = this.getFilterWindow();
    return this.generateShader(r);
  }
  getTaps() {
    let r = this.lanczosCreate(this.lanczosLobes), t = this.tempScale, e = this.getFilterWindow(), i = Array(e);
    for (let s = 1; s <= e; s++) i[s - 1] = r(s * t);
    return i;
  }
  generateShader(r) {
    let t = Array(r);
    for (let e = 1; e <= r; e++) t[e - 1] = `${e}.0 * uDelta`;
    return `
      precision highp float;
      uniform sampler2D uTexture;
      uniform vec2 uDelta;
      varying vec2 vTexCoord;
      uniform float uTaps[${r}];
      void main() {
        vec4 color = texture2D(uTexture, vTexCoord);
        float sum = 1.0;
        ${t.map((e, i) => `
              color += texture2D(uTexture, vTexCoord + ${e}) * uTaps[${i}] + texture2D(uTexture, vTexCoord - ${e}) * uTaps[${i}];
              sum += 2.0 * uTaps[${i}];
            `).join(`
`)}
        gl_FragColor = color / sum;
      }
    `;
  }
  applyToForWebgl(r) {
    r.passes++, this.width = r.sourceWidth, this.horizontal = !0, this.dW = Math.round(this.width * this.scaleX), this.dH = r.sourceHeight, this.tempScale = this.dW / this.width, this.taps = this.getTaps(), r.destinationWidth = this.dW, super.applyTo(r), r.sourceWidth = r.destinationWidth, this.height = r.sourceHeight, this.horizontal = !1, this.dH = Math.round(this.height * this.scaleY), this.tempScale = this.dH / this.height, this.taps = this.getTaps(), r.destinationHeight = this.dH, super.applyTo(r), r.sourceHeight = r.destinationHeight;
  }
  applyTo(r) {
    Kr(r) ? this.applyToForWebgl(r) : this.applyTo2d(r);
  }
  isNeutralState() {
    return this.scaleX === 1 && this.scaleY === 1;
  }
  lanczosCreate(r) {
    return (t) => {
      if (t >= r || t <= -r) return 0;
      if (t < 11920929e-14 && t > -11920929e-14) return 1;
      let e = (t *= Math.PI) / r;
      return Math.sin(t) / t * Math.sin(e) / e;
    };
  }
  applyTo2d(r) {
    let t = r.imageData, e = this.scaleX, i = this.scaleY;
    this.rcpScaleX = 1 / e, this.rcpScaleY = 1 / i;
    let s = t.width, o = t.height, n = Math.round(s * e), a = Math.round(o * i), l;
    l = this.resizeType === "sliceHack" ? this.sliceByTwo(r, s, o, n, a) : this.resizeType === "hermite" ? this.hermiteFastResize(r, s, o, n, a) : this.resizeType === "bilinear" ? this.bilinearFiltering(r, s, o, n, a) : this.resizeType === "lanczos" ? this.lanczosResize(r, s, o, n, a) : new ImageData(n, a), r.imageData = l;
  }
  sliceByTwo(r, t, e, i, s) {
    let o = r.imageData, n = 0.5, a = !1, l = !1, h = t * n, c = e * n, u = r.filterBackend.resources, d = 0, g = 0, p = t, m = 0;
    u.sliceByTwo || (u.sliceByTwo = bt());
    let y = u.sliceByTwo;
    (y.width < 1.5 * t || y.height < e) && (y.width = 1.5 * t, y.height = e);
    let x = y.getContext("2d");
    for (x.clearRect(0, 0, 1.5 * t, e), x.putImageData(o, 0, 0), i = Math.floor(i), s = Math.floor(s); !a || !l; ) t = h, e = c, i < Math.floor(h * n) ? h = Math.floor(h * n) : (h = i, a = !0), s < Math.floor(c * n) ? c = Math.floor(c * n) : (c = s, l = !0), x.drawImage(y, d, g, t, e, p, m, h, c), d = p, g = m, m += c;
    return x.getImageData(d, g, i, s);
  }
  lanczosResize(r, t, e, i, s) {
    let o = r.imageData.data, n = r.ctx.createImageData(i, s), a = n.data, l = this.lanczosCreate(this.lanczosLobes), h = this.rcpScaleX, c = this.rcpScaleY, u = 2 / this.rcpScaleX, d = 2 / this.rcpScaleY, g = Math.ceil(h * this.lanczosLobes / 2), p = Math.ceil(c * this.lanczosLobes / 2), m = {}, y = {
      x: 0,
      y: 0
    }, x = {
      x: 0,
      y: 0
    };
    return (function _(S) {
      let C, b, O, T, k, D, I, j, E, R, X;
      for (y.x = (S + 0.5) * h, x.x = Math.floor(y.x), C = 0; C < s; C++) {
        for (y.y = (C + 0.5) * c, x.y = Math.floor(y.y), k = 0, D = 0, I = 0, j = 0, E = 0, b = x.x - g; b <= x.x + g; b++) if (!(b < 0 || b >= t)) {
          R = Math.floor(1e3 * Math.abs(b - y.x)), m[R] || (m[R] = {});
          for (let z = x.y - p; z <= x.y + p; z++) z < 0 || z >= e || (X = Math.floor(1e3 * Math.abs(z - y.y)), m[R][X] || (m[R][X] = l(Math.sqrt((R * u) ** 2 + (X * d) ** 2) / 1e3)), O = m[R][X], O > 0 && (T = 4 * (z * t + b), k += O, D += O * o[T], I += O * o[T + 1], j += O * o[T + 2], E += O * o[T + 3]));
        }
        T = 4 * (C * i + S), a[T] = D / k, a[T + 1] = I / k, a[T + 2] = j / k, a[T + 3] = E / k;
      }
      return ++S < i ? _(S) : n;
    })(0);
  }
  bilinearFiltering(r, t, e, i, s) {
    let o, n, a, l, h, c, u, d, g, p, m, y, x, _ = 0, S = this.rcpScaleX, C = this.rcpScaleY, b = 4 * (t - 1), O = r.imageData.data, T = r.ctx.createImageData(i, s), k = T.data;
    for (u = 0; u < s; u++) for (d = 0; d < i; d++) for (h = Math.floor(S * d), c = Math.floor(C * u), g = S * d - h, p = C * u - c, x = 4 * (c * t + h), m = 0; m < 4; m++) o = O[x + m], n = O[x + 4 + m], a = O[x + b + m], l = O[x + b + 4 + m], y = o * (1 - g) * (1 - p) + n * g * (1 - p) + a * p * (1 - g) + l * g * p, k[_++] = y;
    return T;
  }
  hermiteFastResize(r, t, e, i, s) {
    let o = this.rcpScaleX, n = this.rcpScaleY, a = Math.ceil(o / 2), l = Math.ceil(n / 2), h = r.imageData.data, c = r.ctx.createImageData(i, s), u = c.data;
    for (let d = 0; d < s; d++) for (let g = 0; g < i; g++) {
      let p = 4 * (g + d * i), m, y = 0, x = 0, _ = 0, S = 0, C = 0, b = 0, O = (d + 0.5) * n;
      for (let T = Math.floor(d * n); T < (d + 1) * n; T++) {
        let k = Math.abs(O - (T + 0.5)) / l, D = (g + 0.5) * o, I = k * k;
        for (let j = Math.floor(g * o); j < (g + 1) * o; j++) {
          let E = Math.abs(D - (j + 0.5)) / a, R = Math.sqrt(I + E * E);
          R > 1 && R < -1 || (m = 2 * R * R * R - 3 * R * R + 1, m > 0 && (E = 4 * (j + T * t), b += m * h[E + 3], x += m, h[E + 3] < 255 && (m = m * h[E + 3] / 250), _ += m * h[E], S += m * h[E + 1], C += m * h[E + 2], y += m));
        }
      }
      u[p] = _ / y, u[p + 1] = S / y, u[p + 2] = C / y, u[p + 3] = b / x;
    }
    return c;
  }
};
f(ze, "type", "Resize"), f(ze, "defaults", {
  resizeType: "hermite",
  scaleX: 1,
  scaleY: 1,
  lanczosLobes: 3
}), f(ze, "uniformLocations", ["uDelta", "uTaps"]), w.setClass(ze);
var Ge = class extends W {
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform float uSaturation;
  varying vec2 vTexCoord;
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    float rgMax = max(color.r, color.g);
    float rgbMax = max(rgMax, color.b);
    color.r += rgbMax != color.r ? (rgbMax - color.r) * uSaturation : 0.00;
    color.g += rgbMax != color.g ? (rgbMax - color.g) * uSaturation : 0.00;
    color.b += rgbMax != color.b ? (rgbMax - color.b) * uSaturation : 0.00;
    gl_FragColor = color;
  }
`;
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = -this.saturation;
    for (let e = 0; e < r.length; e += 4) {
      let i = r[e], s = r[e + 1], o = r[e + 2], n = Math.max(i, s, o);
      r[e] += n === i ? 0 : (n - i) * t, r[e + 1] += n === s ? 0 : (n - s) * t, r[e + 2] += n === o ? 0 : (n - o) * t;
    }
  }
  sendUniformData(r, t) {
    r.uniform1f(t.uSaturation, -this.saturation);
  }
  isNeutralState() {
    return this.saturation === 0;
  }
};
f(Ge, "type", "Saturation"), f(Ge, "defaults", { saturation: 0 }), f(Ge, "uniformLocations", ["uSaturation"]), w.setClass(Ge);
var Ue = class extends W {
  getFragmentSource() {
    return `
  precision highp float;
  uniform sampler2D uTexture;
  uniform float uVibrance;
  varying vec2 vTexCoord;
  void main() {
    vec4 color = texture2D(uTexture, vTexCoord);
    float max = max(color.r, max(color.g, color.b));
    float avg = (color.r + color.g + color.b) / 3.0;
    float amt = (abs(max - avg) * 2.0) * uVibrance;
    color.r += max != color.r ? (max - color.r) * amt : 0.00;
    color.g += max != color.g ? (max - color.g) * amt : 0.00;
    color.b += max != color.b ? (max - color.b) * amt : 0.00;
    gl_FragColor = color;
  }
`;
  }
  applyTo2d({ imageData: { data: r } }) {
    let t = -this.vibrance;
    for (let e = 0; e < r.length; e += 4) {
      let i = r[e], s = r[e + 1], o = r[e + 2], n = Math.max(i, s, o), a = (i + s + o) / 3, l = 2 * Math.abs(n - a) / 255 * t;
      r[e] += n === i ? 0 : (n - i) * l, r[e + 1] += n === s ? 0 : (n - s) * l, r[e + 2] += n === o ? 0 : (n - o) * l;
    }
  }
  sendUniformData(r, t) {
    r.uniform1f(t.uVibrance, -this.vibrance);
  }
  isNeutralState() {
    return this.vibrance === 0;
  }
};
f(Ue, "type", "Vibrance"), f(Ue, "defaults", { vibrance: 0 }), f(Ue, "uniformLocations", ["uVibrance"]), w.setClass(Ue);
var Zh = ir({
  BaseFilter: () => W,
  BlackWhite: () => _h,
  BlendColor: () => Ae,
  BlendImage: () => Fe,
  Blur: () => Le,
  Brightness: () => Re,
  Brownie: () => fh,
  ColorMatrix: () => Qt,
  Composed: () => Li,
  Contrast: () => Ie,
  Convolute: () => Be,
  Gamma: () => Xe,
  Grayscale: () => $e,
  HueRotation: () => kr,
  Invert: () => Ye,
  Kodachrome: () => mh,
  Noise: () => We,
  Pixelate: () => Ve,
  Polaroid: () => yh,
  RemoveColor: () => He,
  Resize: () => ze,
  Saturation: () => Ge,
  Sepia: () => xh,
  Technicolor: () => vh,
  Vibrance: () => Ue,
  Vintage: () => ph
}), Vn = (r, t, e) => {
  const i = r.width ?? t.width, s = r.height ?? t.height;
  if (e === "contain") {
    const o = Math.min(i / t.width, s / t.height);
    t.set({
      left: (i - t.width * o) / 2,
      top: (s - t.height * o) / 2,
      originX: "left",
      originY: "top",
      scaleX: o,
      scaleY: o
    });
    return;
  }
  t.set({
    left: 0,
    top: 0,
    originX: "left",
    originY: "top",
    scaleX: i / t.width,
    scaleY: s / t.height
  });
}, wh = async (r, t, e, i) => {
  if (!t) {
    r.backgroundImage = void 0, r.renderAll();
    return;
  }
  const s = await Bt.fromURL(t);
  e() && (Vn(r, s, i), r.backgroundImage = s, r.renderAll());
}, Th = (r, t) => {
  const e = r.backgroundImage;
  e && (Vn(r, e, t), r.renderAll());
}, Oh = (r, t) => {
  let e = null, i = null;
  const s = (o) => {
    i = { value: o }, e !== null && clearTimeout(e), e = setTimeout(() => {
      e = null;
      const n = i;
      i = null, r(n.value);
    }, t);
  };
  return s.cancel = () => {
    e !== null && (clearTimeout(e), e = null), i = null;
  }, s;
}, kh = (r, t) => {
  const e = Oh(r, t);
  return {
    schedule: (i) => e(i),
    now: (i) => {
      e.cancel(), r(i);
    },
    cancel: () => e.cancel()
  };
}, Mh = 100, Ws = (r) => r == null ? !0 : typeof r != "object" ? !1 : Object.keys(r).length === 0, Vs = (r, t) => JSON.stringify(r) === JSON.stringify(t), Dh = class {
  undoStack = [];
  redoStack = [];
  initialState = null;
  currentState = null;
  get current() {
    return this.currentState;
  }
  get initial() {
    return this.initialState;
  }
  canUndo() {
    return this.undoStack.length !== 0;
  }
  canRedo() {
    return this.redoStack.length !== 0;
  }
  save(r) {
    if (Ws(this.currentState))
      return this.undoStack = [], this.redoStack = [], this.initialState = r, this.currentState = r, !1;
    if (Vs(r, this.currentState)) return !1;
    const t = this.undoStack.length >= Mh;
    return this.undoStack = [...this.undoStack.slice(t ? 1 : 0), this.currentState], this.redoStack = [], this.initialState == null && (this.initialState = this.currentState), this.currentState = r, !0;
  }
  undo() {
    if (Ws(this.currentState) || Vs(this.initialState, this.currentState)) return !1;
    const r = this.undoStack.length === 0;
    return this.redoStack = [...this.redoStack, this.currentState], r || (this.currentState = this.undoStack[this.undoStack.length - 1]), this.undoStack = this.undoStack.slice(0, -1), !0;
  }
  redo() {
    return this.redoStack.length === 0 ? !1 : (this.undoStack = [...this.undoStack, this.currentState], this.currentState = this.redoStack[this.redoStack.length - 1], this.redoStack = this.redoStack.slice(0, -1), !0);
  }
  reset(r) {
    this.undoStack = [], this.redoStack = [], this.initialState = r, this.currentState = r;
  }
}, Eh = {
  upload: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 18V6"/><path d="M7 11l5-5 5 5"/><path d="M5 21h14"/></svg>',
  undo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-2"/></svg>',
  redo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14l5-5-5-5"/><path d="M20 9H10a6 6 0 0 0 0 12h2"/></svg>',
  bin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13h10l1-13"/></svg>'
}, _r = (r, t, e) => {
  const i = document.createElement("button");
  return i.type = "button", i.className = "dc-icon-button", i.title = t, i.setAttribute("aria-label", t), i.innerHTML = Eh[r], i.addEventListener("click", e), i;
}, Ph = (r, t) => {
  r.innerHTML = "";
  const e = document.createElement("div");
  e.className = "dc-toolbar-card", r.appendChild(e);
  const i = _r("upload", "Update the app with this drawing", t.onSend), s = _r("undo", "Undo", t.onUndo), o = _r("redo", "Redo", t.onRedo), n = _r("bin", "Reset canvas & history", t.onReset);
  return e.append(i, s, o, n), {
    undoButton: s,
    redoButton: o
  };
}, jh = (r, t, e) => {
  r.undoButton.disabled = !t, r.redoButton.disabled = !e;
}, se = class {
  canvas;
  constructor(r) {
    this.canvas = r;
  }
}, Ah = (r, t) => {
  const e = t.x - r.x, i = t.y - r.y;
  return Math.sqrt(e * e + i * i);
}, Fh = class extends se {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentCircle = new lt();
  currentStartX = 0;
  currentStartY = 0;
  minRadius = 10;
  configureCanvas({ strokeWidth: r, strokeColor: t, fillColor: e }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((a) => a.selectable = a.evented = !1), this.strokeWidth = r, this.strokeColor = t, this.fillColor = e, this.minRadius = r;
    const i = (a) => this.onMouseDown(a), s = (a) => this.onMouseMove(a), o = () => this.onMouseUp(), n = () => this.onMouseOut();
    return this.canvas.on("mouse:down", i), this.canvas.on("mouse:move", s), this.canvas.on("mouse:up", o), this.canvas.on("mouse:out", n), () => {
      this.canvas.off("mouse:down", i), this.canvas.off("mouse:move", s), this.canvas.off("mouse:up", o), this.canvas.off("mouse:out", n);
    };
  }
  onMouseDown(r) {
    const t = this.canvas, e = r.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(r.e);
    this.currentStartX = i.x, this.currentStartY = i.y, this.currentCircle = new lt({
      left: this.currentStartX,
      top: this.currentStartY,
      originX: "left",
      originY: "center",
      strokeWidth: this.strokeWidth,
      stroke: this.strokeColor,
      fill: this.fillColor,
      selectable: !1,
      evented: !1,
      radius: this.minRadius
    }), e === 0 && t.add(this.currentCircle);
  }
  onMouseMove(r) {
    if (!this.isMouseDown) return;
    const t = this.canvas, e = t.getScenePoint(r.e), i = Ah({
      x: this.currentStartX,
      y: this.currentStartY
    }, {
      x: e.x,
      y: e.y
    }) / 2;
    this.currentCircle.set({
      radius: Math.max(i, this.minRadius),
      angle: Math.atan2(e.y - this.currentStartY, e.x - this.currentStartX) * 180 / Math.PI
    }), this.currentCircle.setCoords(), t.renderAll();
  }
  onMouseUp() {
    this.isMouseDown = !1;
  }
  onMouseOut() {
    this.isMouseDown = !1;
  }
}, Lh = class extends se {
  configureCanvas({ strokeWidth: r, strokeColor: t }) {
    return this.canvas.isDrawingMode = !0, this.canvas.freeDrawingBrush = new Zl(this.canvas), this.canvas.freeDrawingBrush.width = r, this.canvas.freeDrawingBrush.color = t, () => {
    };
  }
}, Rh = class extends se {
  isMouseDown = !1;
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentLine = new kt();
  configureCanvas({ strokeWidth: r, strokeColor: t }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((n) => n.selectable = n.evented = !1), this.strokeWidth = r, this.strokeColor = t;
    const e = (n) => this.onMouseDown(n), i = (n) => this.onMouseMove(n), s = () => this.onMouseUp(), o = () => this.onMouseOut();
    return this.canvas.on("mouse:down", e), this.canvas.on("mouse:move", i), this.canvas.on("mouse:up", s), this.canvas.on("mouse:out", o), () => {
      this.canvas.off("mouse:down", e), this.canvas.off("mouse:move", i), this.canvas.off("mouse:up", s), this.canvas.off("mouse:out", o);
    };
  }
  onMouseDown(r) {
    const t = this.canvas, e = r.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(r.e);
    this.currentLine = new kt([
      i.x,
      i.y,
      i.x,
      i.y
    ], {
      strokeWidth: this.strokeWidth,
      fill: this.strokeColor,
      stroke: this.strokeColor,
      originX: "center",
      originY: "center",
      selectable: !1,
      evented: !1
    }), e === 0 && t.add(this.currentLine);
  }
  onMouseMove(r) {
    if (!this.isMouseDown) return;
    const t = this.canvas, e = t.getScenePoint(r.e);
    this.currentLine.set({
      x2: e.x,
      y2: e.y
    }), this.currentLine.setCoords(), t.renderAll();
  }
  onMouseUp() {
    this.isMouseDown = !1;
    const r = this.canvas;
    this.currentLine.width === 0 && this.currentLine.height === 0 && r.remove(this.currentLine);
  }
  onMouseOut() {
    this.isMouseDown = !1;
  }
}, Ih = class extends se {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  startCircle = new lt();
  currentLine = new kt();
  currentPath = new Ot("M 0 0");
  pathString = "M ";
  configureCanvas({ strokeWidth: r, strokeColor: t, fillColor: e }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((l) => l.selectable = l.evented = !1), this.strokeWidth = r, this.strokeColor = t, this.fillColor = e;
    const i = (l) => this.onMouseDown(l), s = (l) => this.onMouseMove(l), o = () => this.onMouseUp(), n = () => this.onMouseOut(), a = () => this.onMouseDoubleClick();
    return this.canvas.on("mouse:down", i), this.canvas.on("mouse:move", s), this.canvas.on("mouse:up", o), this.canvas.on("mouse:out", n), this.canvas.on("mouse:dblclick", a), () => {
      this.canvas.off("mouse:down", i), this.canvas.off("mouse:move", s), this.canvas.off("mouse:up", o), this.canvas.off("mouse:out", n), this.canvas.off("mouse:dblclick", a);
    };
  }
  onMouseDown(r) {
    const t = this.canvas, e = r.e.button;
    let i = this.pathString === "M ";
    this.isMouseDown = !0;
    const s = t.getScenePoint(r.e);
    t.remove(this.currentLine), this.currentLine = new kt([
      s.x,
      s.y,
      s.x,
      s.y
    ], {
      strokeWidth: this.strokeWidth,
      fill: this.strokeColor,
      stroke: this.strokeColor,
      originX: "center",
      originY: "center",
      selectable: !1,
      evented: !1
    }), e === 0 && t.add(this.currentLine), i && e === 0 ? (this.pathString += `${s.x} ${s.y} `, this.startCircle = new lt({
      left: s.x,
      top: s.y,
      originX: "center",
      originY: "center",
      strokeWidth: this.strokeWidth,
      stroke: this.strokeColor,
      fill: this.strokeColor,
      selectable: !1,
      evented: !1,
      radius: this.strokeWidth
    }), t.add(this.startCircle), i = !1) : (t.remove(this.currentPath), e === 0 && (this.pathString += `L ${s.x} ${s.y} `), e === 2 && (this.pathString += "z", t.remove(this.startCircle))), this.currentPath = new Ot(this.pathString, {
      strokeWidth: this.strokeWidth,
      fill: this.fillColor,
      stroke: this.strokeColor,
      originX: "center",
      originY: "center",
      selectable: !1,
      evented: !1
    }), this.currentPath.width !== 0 && this.currentPath.height !== 0 && t.add(this.currentPath), e === 2 && (this.pathString = "M ");
  }
  onMouseMove(r) {
    if (!this.isMouseDown) return;
    const t = this.canvas, e = t.getScenePoint(r.e);
    this.currentLine.set({
      x2: e.x,
      y2: e.y
    }), this.currentLine.setCoords(), t.renderAll();
  }
  onMouseUp() {
    this.isMouseDown = !0;
  }
  onMouseOut() {
    this.isMouseDown = !1;
  }
  onMouseDoubleClick() {
    const r = this.canvas;
    for (let t = 0; t < 3; t++) {
      const e = this.pathString.lastIndexOf("L");
      e === -1 ? (this.pathString = "M ", r.remove(this.startCircle)) : this.pathString = this.pathString.slice(0, e);
    }
    r.remove(this.currentLine), r.remove(this.currentPath), this.currentPath = new Ot(this.pathString, {
      strokeWidth: this.strokeWidth,
      fill: this.fillColor,
      stroke: this.strokeColor,
      originX: "center",
      originY: "center",
      selectable: !1,
      evented: !1
    }), r.add(this.currentPath);
  }
}, Bh = class extends se {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentRect = new Tt();
  currentStartX = 0;
  currentStartY = 0;
  minLength = 10;
  configureCanvas({ strokeWidth: r, strokeColor: t, fillColor: e }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((a) => a.selectable = a.evented = !1), this.strokeWidth = r, this.strokeColor = t, this.fillColor = e, this.minLength = r;
    const i = (a) => this.onMouseDown(a), s = (a) => this.onMouseMove(a), o = () => this.onMouseUp(), n = () => this.onMouseOut();
    return this.canvas.on("mouse:down", i), this.canvas.on("mouse:move", s), this.canvas.on("mouse:up", o), this.canvas.on("mouse:out", n), () => {
      this.canvas.off("mouse:down", i), this.canvas.off("mouse:move", s), this.canvas.off("mouse:up", o), this.canvas.off("mouse:out", n);
    };
  }
  onMouseDown(r) {
    const t = this.canvas, e = r.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(r.e);
    this.currentStartX = i.x, this.currentStartY = i.y, this.currentRect = new Tt({
      left: this.currentStartX,
      top: this.currentStartY,
      originX: "left",
      originY: "top",
      width: this.minLength,
      height: this.minLength,
      stroke: this.strokeColor,
      strokeWidth: this.strokeWidth,
      fill: this.fillColor,
      transparentCorners: !1,
      selectable: !1,
      evented: !1,
      strokeUniform: !0,
      noScaleCache: !1,
      angle: 0
    }), e === 0 && t.add(this.currentRect);
  }
  onMouseMove(r) {
    if (!this.isMouseDown) return;
    const t = this.canvas, e = t.getScenePoint(r.e);
    this.currentStartX > e.x && this.currentRect.set({ left: Math.abs(e.x) }), this.currentStartY > e.y && this.currentRect.set({ top: Math.abs(e.y) });
    const i = Math.abs(this.currentStartX - e.x), s = Math.abs(this.currentStartY - e.y);
    this.currentRect.set({
      width: Math.max(i, this.minLength * 2),
      height: Math.max(s, this.minLength * 2)
    }), this.currentRect.setCoords(), t.renderAll();
  }
  onMouseUp() {
    this.isMouseDown = !1;
  }
  onMouseOut() {
    this.isMouseDown = !1;
  }
}, Xh = class extends se {
  configureCanvas(r) {
    const t = this.canvas;
    t.isDrawingMode = !1, t.selection = !0, t.forEachObject((i) => i.selectable = i.evented = !0);
    const e = () => {
      const i = t.getActiveObject();
      i && t.remove(i);
    };
    return t.on("mouse:dblclick", e), () => {
      t.off("mouse:dblclick", e);
    };
  }
}, $h = class extends se {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentCircle = new lt();
  currentStartX = 0;
  currentStartY = 0;
  displayRadius = 1;
  configureCanvas({ strokeWidth: r, strokeColor: t, fillColor: e, displayRadius: i }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((l) => l.selectable = l.evented = !1), this.strokeWidth = r, this.strokeColor = t, this.fillColor = e, this.displayRadius = i;
    const s = (l) => this.onMouseDown(l), o = () => this.onMouseMove(), n = () => this.onMouseUp(), a = () => this.onMouseOut();
    return this.canvas.on("mouse:down", s), this.canvas.on("mouse:move", o), this.canvas.on("mouse:up", n), this.canvas.on("mouse:out", a), () => {
      this.canvas.off("mouse:down", s), this.canvas.off("mouse:move", o), this.canvas.off("mouse:up", n), this.canvas.off("mouse:out", a);
    };
  }
  onMouseDown(r) {
    const t = this.canvas, e = r.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(r.e);
    this.currentStartX = i.x - (this.displayRadius + this.strokeWidth / 2), this.currentStartY = i.y, this.currentCircle = new lt({
      left: this.currentStartX,
      top: this.currentStartY,
      originX: "left",
      originY: "center",
      strokeWidth: this.strokeWidth,
      stroke: this.strokeColor,
      fill: this.fillColor,
      selectable: !1,
      evented: !1,
      radius: this.displayRadius
    }), e === 0 && t.add(this.currentCircle);
  }
  onMouseMove() {
    this.isMouseDown && (this.currentCircle.setCoords(), this.canvas.renderAll());
  }
  onMouseUp() {
    this.isMouseDown = !1;
  }
  onMouseOut() {
    this.isMouseDown = !1;
  }
}, Hs = {
  circle: Fh,
  freedraw: Lh,
  line: Rh,
  polygon: Ih,
  rect: Bh,
  transform: Xh,
  point: $h
}, Yh = 200, zs = (r) => {
  const t = r.canvas.toObject();
  return r.history.save(t) && r.latest.realtimeUpdateStreamlit && r.sender.schedule(t), t;
}, Wh = (r, t) => {
  const e = r.latest.returnImageData ? r.canvas.toDataURL({
    format: "png",
    multiplier: 1
  }) : null;
  r.latest.setStateValue("drawing", {
    raw: t,
    data: e
  });
}, ai = async (r) => {
  const t = r.history.current;
  if (t == null) return !1;
  const e = ++r.loadGeneration;
  return await r.canvas.loadFromJSON(t), e !== r.loadGeneration ? !1 : (r.canvas.renderAll(), r.latest.data && Ri(r, r.latest.data), !0);
}, Vh = (r) => {
  r.isDrawingMode = !1, r.selection = !1, r.discardActiveObject(), r.forEachObject((t) => {
    t.selectable = !1, t.evented = !1;
  }), r.renderAll();
}, Ri = (r, t) => {
  if (r.activeToolCleanup?.(), r.activeToolCleanup = null, t.disabled) {
    Vh(r.canvas);
    return;
  }
  r.activeToolCleanup = new (Hs[t.drawingMode] ?? Hs.freedraw)(r.canvas).configureCanvas({
    fillColor: t.fillColor,
    strokeWidth: t.strokeWidth,
    strokeColor: t.strokeColor,
    displayRadius: t.displayRadius
  });
}, Nt = (r) => {
  jh(r.toolbarHandles, r.history.canUndo(), r.history.canRedo());
}, Gs = (r) => JSON.stringify([
  r.drawingMode,
  r.fillColor,
  r.strokeWidth,
  r.strokeColor,
  r.displayRadius,
  r.disabled
]), Hh = (r) => {
  const t = document.createElement("div");
  t.className = "dc-container";
  const e = document.createElement("canvas");
  e.className = "dc-background-canvas";
  const i = document.createElement("canvas");
  i.className = "dc-canvas";
  const s = document.createElement("div");
  s.className = "dc-toolbar", t.append(e, i, s), r.appendChild(t);
  const o = new wi(i, { enableRetinaScaling: !1 });
  o.stopContextMenu = !0, o.fireRightClick = !0;
  const n = {
    container: t,
    canvas: o,
    backgroundCanvas: new $r(e, { enableRetinaScaling: !1 }),
    toolbarEl: s,
    toolbarHandles: null,
    history: new Dh(),
    sender: null,
    activeToolCleanup: null,
    lastToolKey: null,
    lastInitialDrawingKey: null,
    lastBackgroundImageURL: null,
    lastBackgroundImageFit: null,
    width: 0,
    height: 0,
    loadGeneration: 0,
    backgroundGeneration: 0,
    latest: {
      realtimeUpdateStreamlit: !0,
      returnImageData: !1,
      setStateValue: () => {
      },
      data: null
    }
  };
  return n.sender = kh((a) => Wh(n, a), Yh), n.toolbarHandles = Ph(s, {
    onSend: () => {
      n.sender.now(o.toObject());
    },
    onUndo: () => {
      n.history.undo() && (ai(n).then((a) => {
        a && n.latest.realtimeUpdateStreamlit && n.sender.now(o.toObject());
      }), Nt(n));
    },
    onRedo: () => {
      n.history.redo() && (ai(n).then((a) => {
        a && n.latest.realtimeUpdateStreamlit && n.sender.now(o.toObject());
      }), Nt(n));
    },
    onReset: () => {
      const a = n.history.initial ?? {};
      n.history.reset(a), ai(n).then((l) => {
        l && n.sender.now(o.toObject());
      }), Nt(n);
    }
  }), o.on("mouse:up", (a) => {
    if (n.latest.data?.disabled) return;
    const l = a.e, h = l != null && l.button === 2;
    queueMicrotask(() => {
      const c = zs(n);
      h && n.sender.now(c), Nt(n);
    });
  }), o.on("mouse:dblclick", () => {
    n.latest.data?.disabled || queueMicrotask(() => {
      zs(n), Nt(n);
    });
  }), n;
}, zh = (r, t, e) => {
  r.latest.realtimeUpdateStreamlit = t.realtimeUpdateStreamlit, r.latest.returnImageData = t.returnImageData, r.latest.setStateValue = e, r.latest.data = t;
  const i = r.width !== t.canvasWidth || r.height !== t.canvasHeight;
  i && (r.width = t.canvasWidth, r.height = t.canvasHeight, r.canvas.setDimensions({
    width: t.canvasWidth,
    height: t.canvasHeight
  }), r.backgroundCanvas.setDimensions({
    width: t.canvasWidth,
    height: t.canvasHeight
  }));
  const s = t.displayToolbar && !t.disabled;
  r.container.style.width = `${t.canvasWidth}px`, r.container.style.height = `${t.canvasHeight}px`, r.toolbarEl.style.display = s ? "flex" : "none", r.toolbarEl.dataset.pinned = String(!t.realtimeUpdateStreamlit);
  const o = t.backgroundImageFit !== r.lastBackgroundImageFit;
  if (r.lastBackgroundImageFit = t.backgroundImageFit, t.backgroundImageURL !== r.lastBackgroundImageURL) {
    r.lastBackgroundImageURL = t.backgroundImageURL;
    const a = ++r.backgroundGeneration;
    wh(r.backgroundCanvas, t.backgroundImageURL, () => a === r.backgroundGeneration, t.backgroundImageFit).catch((l) => {
      console.error("streamlit-drawable-canvas: failed to load background image", l), a === r.backgroundGeneration && (r.lastBackgroundImageURL = null);
    });
  } else (i || o) && Th(r.backgroundCanvas, t.backgroundImageFit);
  const n = JSON.stringify(t.initialDrawing);
  if (n !== r.lastInitialDrawingKey) {
    r.lastInitialDrawingKey = n, r.sender.cancel();
    const a = ++r.loadGeneration;
    r.canvas.loadFromJSON(t.initialDrawing).then(() => {
      if (a !== r.loadGeneration) return;
      r.canvas.renderAll(), r.history.reset(t.initialDrawing);
      const l = r.latest.data ?? t;
      Ri(r, l), r.lastToolKey = Gs(l), Nt(r);
    });
  } else {
    const a = Gs(t);
    a !== r.lastToolKey && (r.lastToolKey = a, Ri(r, t));
  }
  Nt(r);
}, Gh = (r) => {
  r.sender.cancel(), r.activeToolCleanup?.(), r.canvas.dispose(), r.backgroundCanvas.dispose(), r.container.remove();
}, Sr = /* @__PURE__ */ new WeakMap(), tc = (r) => {
  const { data: t, parentElement: e, setStateValue: i } = r, s = e.querySelector(".canvas-root");
  if (!s) throw new Error("Unexpected: .canvas-root element not found");
  let o = Sr.get(e);
  return o ? s.contains(o.container) || s.appendChild(o.container) : (o = Hh(s), Sr.set(e, o)), zh(o, t, i), () => {
    const n = Sr.get(e);
    n && (Gh(n), Sr.delete(e));
  };
};
export {
  tc as default
};
