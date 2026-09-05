var Cs = Object.defineProperty, hr = (e, t) => {
  let r = {};
  for (var i in e) Cs(r, i, {
    get: e[i],
    enumerable: !0
  });
  return t || Cs(r, Symbol.toStringTag, { value: "Module" }), r;
};
function Qe(e) {
  return Qe = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Qe(e);
}
function ua(e) {
  var t = (function(r, i) {
    if (Qe(r) != "object" || !r) return r;
    var s = r[Symbol.toPrimitive];
    if (s !== void 0) {
      var o = s.call(r, i || "default");
      if (Qe(o) != "object") return o;
      throw TypeError("@@toPrimitive must return a primitive value.");
    }
    return (i === "string" ? String : Number)(r);
  })(e, "string");
  return Qe(t) == "symbol" ? t : t + "";
}
function f(e, t, r) {
  return (t = ua(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
var bs = class {
  constructor() {
    f(this, "browserShadowBlurConstant", 1), f(this, "DPI", 96), f(this, "devicePixelRatio", typeof window < "u" ? window.devicePixelRatio : 1), f(this, "perfLimitSizeTotal", 2097152), f(this, "maxCacheSideLimit", 4096), f(this, "minCacheSideLimit", 256), f(this, "disableStyleCopyPaste", !1), f(this, "enableGLFiltering", !0), f(this, "textureSize", 4096), f(this, "forceGLPutImageData", !1), f(this, "cachesBoundsOfCurve", !1), f(this, "fontPaths", {}), f(this, "NUM_FRACTION_DIGITS", 4);
  }
}, P = new class extends bs {
  constructor(e) {
    super(), this.configure(e);
  }
  configure(e = {}) {
    Object.assign(this, e);
  }
  addFonts(e = {}) {
    this.fontPaths = {
      ...this.fontPaths,
      ...e
    };
  }
  removeFonts(e = []) {
    e.forEach((t) => {
      delete this.fontPaths[t];
    });
  }
  clearFonts() {
    this.fontPaths = {};
  }
  restoreDefaults(e) {
    let t = new bs(), r = e?.reduce((i, s) => (i[s] = t[s], i), {}) || t;
    this.configure(r);
  }
}(), zt = (e, ...t) => console[e]("fabric", ...t), Ct = class extends Error {
  constructor(e, t) {
    super(`fabric: ${e}`, t);
  }
}, da = class extends Ct {
  constructor(e) {
    super(`${e} 'options.signal' is in 'aborted' state`);
  }
}, ga = class {
}, fa = class extends ga {
  testPrecision(e, t) {
    let r = `precision ${t} float;
void main(){}`, i = e.createShader(e.FRAGMENT_SHADER);
    return !!i && (e.shaderSource(i, r), e.compileShader(i), !!e.getShaderParameter(i, e.COMPILE_STATUS));
  }
  queryWebGL(e) {
    let t = e.getContext("webgl");
    t && (this.maxTextureSize = t.getParameter(t.MAX_TEXTURE_SIZE), this.GLPrecision = [
      "highp",
      "mediump",
      "lowp"
    ].find((r) => this.testPrecision(t, r)), t.getExtension("WEBGL_lose_context").loseContext(), zt("log", `WebGL: max texture size ${this.maxTextureSize}`));
  }
  isSupported(e) {
    return !!this.maxTextureSize && this.maxTextureSize >= e;
  }
}, pa = {}, ws, wt = () => ws || (ws = {
  document,
  window,
  isTouchSupported: "ontouchstart" in window || "ontouchstart" in document || window && window.navigator && window.navigator.maxTouchPoints > 0,
  WebGLProbe: new fa(),
  dispose() {
  },
  copyPasteData: pa
}), we = () => wt().document, ye = () => wt().window, io = () => {
  var e;
  return Math.max((e = P.devicePixelRatio) == null ? ye().devicePixelRatio : e, 1);
}, Ze = new class {
  constructor() {
    f(this, "boundsOfCurveCache", {}), this.charWidthsCache = /* @__PURE__ */ new Map();
  }
  getFontCache({ fontFamily: e, fontStyle: t, fontWeight: r }) {
    e = e.toLowerCase();
    let i = this.charWidthsCache;
    i.has(e) || i.set(e, /* @__PURE__ */ new Map());
    let s = i.get(e), o = `${t.toLowerCase()}_${(r + "").toLowerCase()}`;
    return s.has(o) || s.set(o, /* @__PURE__ */ new Map()), s.get(o);
  }
  clearFontCache(e) {
    e ? this.charWidthsCache.delete((e || "").toLowerCase()) : this.charWidthsCache = /* @__PURE__ */ new Map();
  }
  limitDimsByArea(e) {
    let { perfLimitSizeTotal: t } = P, r = Math.sqrt(t * e);
    return [Math.floor(r), Math.floor(t / r)];
  }
}(), mi = "7.4.0";
function Or() {
}
var Ut = Math.PI / 2, ma = Math.PI / 4, vt = 2 * Math.PI, Gi = Math.PI / 180, et = Object.freeze([
  1,
  0,
  0,
  1,
  0,
  0
]), L = "center", H = "left", so = "bottom", pt = "right", $r = "none", Ui = /\r?\n/, oo = "moving", Wr = "scaling", no = "rotating", ao = "rotate", lo = "skewing", ir = "resizing", ho = "modifyPoly", jr = "changed", co = "scale", Nt = "scaleX", qt = "scaleY", Te = "skewX", Oe = "skewY", st = "fill", Dt = "stroke", uo = "modified", Ts = "normal", he = "json", w = new class {
  constructor() {
    this[he] = /* @__PURE__ */ new Map(), this.svg = /* @__PURE__ */ new Map();
  }
  has(e) {
    return this[he].has(e);
  }
  getClass(e) {
    let t = this[he].get(e);
    if (!t) throw new Ct(`No class registered for ${e}`);
    return t;
  }
  setClass(e, t) {
    t ? this[he].set(t, e) : (this[he].set(e.type, e), this[he].set(e.type.toLowerCase(), e));
  }
  getSVGClass(e) {
    return this.svg.get(e);
  }
  setSVGClass(e, t) {
    this.svg.set(t ?? e.type.toLowerCase(), e);
  }
}(), Fr = new class extends Array {
  remove(e) {
    let t = this.indexOf(e);
    t > -1 && this.splice(t, 1);
  }
  cancelAll() {
    let e = this.splice(0);
    return e.forEach((t) => t.abort()), e;
  }
  cancelByCanvas(e) {
    if (!e) return [];
    let t = this.filter((r) => {
      var i;
      return r.target === e || typeof r.target == "object" && ((i = r.target) == null ? void 0 : i.canvas) === e;
    });
    return t.forEach((r) => r.abort()), t;
  }
  cancelByTarget(e) {
    if (!e) return [];
    let t = this.filter((r) => r.target === e);
    return t.forEach((r) => r.abort()), t;
  }
}(), va = class {
  constructor() {
    f(this, "__eventListeners", {});
  }
  on(e, t) {
    if (this.__eventListeners || (this.__eventListeners = {}), typeof e == "object") return Object.entries(e).forEach(([r, i]) => {
      this.on(r, i);
    }), () => this.off(e);
    if (t) {
      let r = e;
      return this.__eventListeners[r] || (this.__eventListeners[r] = []), this.__eventListeners[r].push(t), () => this.off(r, t);
    }
    return () => !1;
  }
  once(e, t) {
    if (typeof e == "object") {
      let r = [];
      return Object.entries(e).forEach(([i, s]) => {
        r.push(this.once(i, s));
      }), () => r.forEach((i) => i());
    }
    if (t) {
      let r = this.on(e, function(...i) {
        t.call(this, ...i), r();
      });
      return r;
    }
    return () => !1;
  }
  _removeEventListener(e, t) {
    if (this.__eventListeners[e]) if (t) {
      let r = this.__eventListeners[e], i = r.indexOf(t);
      i > -1 && r.splice(i, 1);
    } else this.__eventListeners[e] = [];
  }
  off(e, t) {
    if (this.__eventListeners) if (e === void 0) for (let r in this.__eventListeners) this._removeEventListener(r);
    else typeof e == "object" ? Object.entries(e).forEach(([r, i]) => {
      this._removeEventListener(r, i);
    }) : this._removeEventListener(e, t);
  }
  fire(e, t) {
    var r;
    if (!this.__eventListeners) return;
    let i = (r = this.__eventListeners[e]) == null ? void 0 : r.concat();
    if (i) for (let s = 0; s < i.length; s++) i[s].call(this, t || {});
  }
}, Qt = (e, t) => {
  let r = e.indexOf(t);
  return r !== -1 && e.splice(r, 1), e;
}, yt = (e) => {
  if (e === 0) return 1;
  switch (Math.abs(e) / Ut) {
    case 1:
    case 3:
      return 0;
    case 2:
      return -1;
  }
  return Math.cos(e);
}, xt = (e) => {
  if (e === 0) return 0;
  let t = e / Ut, r = Math.sign(e);
  switch (t) {
    case 1:
      return r;
    case 2:
      return 0;
    case 3:
      return -r;
  }
  return Math.sin(e);
}, v = class Q {
  constructor(t = 0, r = 0) {
    typeof t == "object" ? (this.x = t.x, this.y = t.y) : (this.x = t, this.y = r);
  }
  add(t) {
    return new Q(this.x + t.x, this.y + t.y);
  }
  addEquals(t) {
    return this.x += t.x, this.y += t.y, this;
  }
  scalarAdd(t) {
    return new Q(this.x + t, this.y + t);
  }
  scalarAddEquals(t) {
    return this.x += t, this.y += t, this;
  }
  subtract(t) {
    return new Q(this.x - t.x, this.y - t.y);
  }
  subtractEquals(t) {
    return this.x -= t.x, this.y -= t.y, this;
  }
  scalarSubtract(t) {
    return new Q(this.x - t, this.y - t);
  }
  scalarSubtractEquals(t) {
    return this.x -= t, this.y -= t, this;
  }
  multiply(t) {
    return new Q(this.x * t.x, this.y * t.y);
  }
  scalarMultiply(t) {
    return new Q(this.x * t, this.y * t);
  }
  scalarMultiplyEquals(t) {
    return this.x *= t, this.y *= t, this;
  }
  divide(t) {
    return new Q(this.x / t.x, this.y / t.y);
  }
  scalarDivide(t) {
    return new Q(this.x / t, this.y / t);
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
  lerp(t, r = 0.5) {
    return r = Math.max(Math.min(1, r), 0), new Q(this.x + (t.x - this.x) * r, this.y + (t.y - this.y) * r);
  }
  distanceFrom(t) {
    let r = this.x - t.x, i = this.y - t.y;
    return Math.sqrt(r * r + i * i);
  }
  midPointFrom(t) {
    return this.lerp(t);
  }
  min(t) {
    return new Q(Math.min(this.x, t.x), Math.min(this.y, t.y));
  }
  max(t) {
    return new Q(Math.max(this.x, t.x), Math.max(this.y, t.y));
  }
  toString() {
    return `${this.x},${this.y}`;
  }
  setXY(t, r) {
    return this.x = t, this.y = r, this;
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
    let r = this.x, i = this.y;
    this.x = t.x, this.y = t.y, t.x = r, t.y = i;
  }
  clone() {
    return new Q(this.x, this.y);
  }
  rotate(t, r = Ni) {
    let i = xt(t), s = yt(t), o = this.subtract(r);
    return new Q(o.x * s - o.y * i, o.x * i + o.y * s).add(r);
  }
  transform(t, r = !1) {
    return new Q(t[0] * this.x + t[2] * this.y + (r ? 0 : t[4]), t[1] * this.x + t[3] * this.y + (r ? 0 : t[5]));
  }
}, Ni = new v(0, 0), kr = (e) => !!e && Array.isArray(e._objects);
function go(e) {
  class t extends e {
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
      return !(!i || i === this._objects[0]) && (Qt(this._objects, i), this._objects.unshift(i), this._onStackOrderChanged(i), !0);
    }
    bringObjectToFront(i) {
      return !(!i || i === this._objects[this._objects.length - 1]) && (Qt(this._objects, i), this._objects.push(i), this._onStackOrderChanged(i), !0);
    }
    sendObjectBackwards(i, s) {
      if (!i) return !1;
      let o = this._objects.indexOf(i);
      if (o !== 0) {
        let n = this.findNewLowerIndex(i, o, s);
        return Qt(this._objects, i), this._objects.splice(n, 0, i), this._onStackOrderChanged(i), !0;
      }
      return !1;
    }
    bringObjectForward(i, s) {
      if (!i) return !1;
      let o = this._objects.indexOf(i);
      if (o !== this._objects.length - 1) {
        let n = this.findNewUpperIndex(i, o, s);
        return Qt(this._objects, i), this._objects.splice(n, 0, i), this._onStackOrderChanged(i), !0;
      }
      return !1;
    }
    moveObjectTo(i, s) {
      return i !== this._objects[s] && (Qt(this._objects, i), this._objects.splice(s, 0, i), this._onStackOrderChanged(i), !0);
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
var fo = class extends va {
  _setOptions(e = {}) {
    for (let t in e) this.set(t, e[t]);
  }
  _setObject(e) {
    for (let t in e) this._set(t, e[t]);
  }
  set(e, t) {
    return typeof e == "object" ? this._setObject(e) : this._set(e, t), this;
  }
  _set(e, t) {
    this[e] = t;
  }
  toggle(e) {
    let t = this.get(e);
    return typeof t == "boolean" && this.set(e, !t), this;
  }
  get(e) {
    return this[e];
  }
};
function tr(e) {
  return ye().requestAnimationFrame(e);
}
function po(e) {
  return ye().cancelAnimationFrame(e);
}
var ya = 0, Gt = () => ya++, Tt = () => {
  let e = we().createElement("canvas");
  if (!e || e.getContext === void 0) throw new Ct("Failed to create `canvas` element");
  return e;
}, mo = () => we().createElement("img"), xa = (e) => {
  var t;
  let r = ht(e);
  return (t = r.getContext("2d")) == null || t.drawImage(e, 0, 0), r;
}, ht = (e) => {
  let t = Tt();
  return t.width = e.width, t.height = e.height, t;
}, qi = (e, t, r) => e.toDataURL(`image/${t}`, r), Ki = (e, t, r) => new Promise((i, s) => {
  e.toBlob(i, `image/${t}`, r);
}), I = (e) => e * Gi, Et = (e) => e / Gi, vo = (e) => e.every((t, r) => t === et[r]), N = (e, t, r) => new v(e).transform(t, r), lt = (e) => {
  let t = 1 / (e[0] * e[3] - e[1] * e[2]), r = [
    t * e[3],
    -t * e[1],
    -t * e[2],
    t * e[0],
    0,
    0
  ], { x: i, y: s } = new v(e[4], e[5]).transform(r, !0);
  return r[4] = -i, r[5] = -s, r;
}, Y = (e, t, r) => [
  e[0] * t[0] + e[2] * t[1],
  e[1] * t[0] + e[3] * t[1],
  e[0] * t[2] + e[2] * t[3],
  e[1] * t[2] + e[3] * t[3],
  r ? 0 : e[0] * t[4] + e[2] * t[5] + e[4],
  r ? 0 : e[1] * t[4] + e[3] * t[5] + e[5]
], Vr = (e, t) => e.reduceRight((r, i) => i && r ? Y(i, r, t) : i || r, void 0) || et.concat(), Ji = ([e, t]) => Math.atan2(t, e), Qi = ([e, t]) => Math.sqrt(e * e + t * t), yo = ([, , e, t]) => Math.sqrt(e * e + t * t), xe = (e) => {
  let t = Ji(e), r = e[0] ** 2 + e[1] ** 2, i = Math.sqrt(r), s = (e[0] * e[3] - e[2] * e[1]) / i, o = Math.atan2(e[0] * e[2] + e[1] * e[3], r);
  return {
    angle: Et(t),
    scaleX: i,
    scaleY: s,
    skewX: Et(o),
    skewY: 0,
    translateX: e[4] || 0,
    translateY: e[5] || 0
  };
}, ke = (e, t = 0) => [
  1,
  0,
  0,
  1,
  e,
  t
];
function ne({ angle: e = 0 } = {}, { x: t = 0, y: r = 0 } = {}) {
  let i = I(e), s = yt(i), o = xt(i);
  return [
    s,
    o,
    -o,
    s,
    t ? t - (s * t - o * r) : 0,
    r ? r - (o * t + s * r) : 0
  ];
}
var Hr = (e, t = e) => [
  e,
  0,
  0,
  t,
  0,
  0
], xo = (e) => Math.tan(I(e)), Zi = (e) => [
  1,
  0,
  xo(e),
  1,
  0,
  0
], ts = (e) => [
  1,
  xo(e),
  0,
  1,
  0,
  0
], cr = ({ scaleX: e = 1, scaleY: t = 1, flipX: r = !1, flipY: i = !1, skewX: s = 0, skewY: o = 0 }) => {
  let n = Hr(r ? -e : e, i ? -t : t);
  return s && (n = Y(n, Zi(s), !0)), o && (n = Y(n, ts(o), !0)), n;
}, _o = (e) => {
  let { translateX: t = 0, translateY: r = 0, angle: i = 0 } = e, s = ke(t, r);
  i && (s = Y(s, ne({ angle: i })));
  let o = cr(e);
  return vo(o) || (s = Y(s, o)), s;
}, er = (e, { signal: t, crossOrigin: r = null } = {}) => new Promise(function(i, s) {
  if (t && t.aborted) return s(new da("loadImage"));
  let o = mo(), n;
  t && (n = function(l) {
    o.src = "", s(l);
  }, t.addEventListener("abort", n, { once: !0 }));
  let a = function() {
    o.onload = o.onerror = null, n && t?.removeEventListener("abort", n), i(o);
  };
  e ? (o.onload = a, o.onerror = function() {
    n && t?.removeEventListener("abort", n), s(new Ct(`Error loading ${o.src}`));
  }, r && (o.crossOrigin = r), o.src = e) : a();
}), _e = (e, { signal: t, reviver: r = Or } = {}) => new Promise((i, s) => {
  let o = [];
  t && t.addEventListener("abort", s, { once: !0 }), Promise.allSettled(e.map((n) => w.getClass(n.type).fromObject(n, { signal: t }))).then(async (n) => {
    for (let [a, l] of n.entries()) if (l.status === "fulfilled" && (await r(e[a], l.value), o.push(l.value)), l.status === "rejected") {
      let h = await r(e[a], void 0, l.reason);
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
}), ur = (e, { signal: t } = {}) => new Promise((r, i) => {
  let s = [];
  t && t.addEventListener("abort", i, { once: !0 });
  let o = Object.values(e).map((a) => a && a.type && w.has(a.type) ? _e([a], { signal: t }).then(([l]) => (s.push(l), l)) : a), n = Object.keys(e);
  Promise.all(o).then((a) => a.reduce((l, h, c) => (l[n[c]] = h, l), {})).then(r).catch((a) => {
    s.forEach((l) => {
      l.dispose && l.dispose();
    }), i(a);
  }).finally(() => {
    t && t.removeEventListener("abort", i);
  });
}), ae = (e, t = []) => t.reduce((r, i) => (i in e && (r[i] = e[i]), r), {}), es = (e, t) => Object.keys(e).reduce((r, i) => (t(e[i], i, e) && (r[i] = e[i]), r), {}), F = (e, t) => parseFloat(Number(e).toFixed(t)), Se = (e) => "matrix(" + e.map((t) => F(t, P.NUM_FRACTION_DIGITS)).join(" ") + ")", ut = (e) => !!e && e.toLive !== void 0, Os = (e) => !!e && typeof e.toObject == "function", ks = (e) => !!e && e.offsetX !== void 0 && "source" in e, Zt = (e) => !!e && "multiSelectionStacking" in e;
function So(e) {
  let t = e && gt(e), r = 0, i = 0;
  if (!e || !t) return {
    left: r,
    top: i
  };
  let s = e, o = t.documentElement, n = t.body || {
    scrollLeft: 0,
    scrollTop: 0
  };
  for (; s && (s.parentNode || s.host) && (s = s.parentNode || s.host, s === t ? (r = n.scrollLeft || o.scrollLeft || 0, i = n.scrollTop || o.scrollTop || 0) : (r += s.scrollLeft || 0, i += s.scrollTop || 0), s.nodeType !== 1 || s.style.position !== "fixed"); ) ;
  return {
    left: r,
    top: i
  };
}
var gt = (e) => e.ownerDocument || null, Co = (e) => {
  var t;
  return ((t = e.ownerDocument) == null ? void 0 : t.defaultView) || null;
}, bo = (e, t, { width: r, height: i }, s = 1) => {
  e.width = r, e.height = i, s > 1 && (e.setAttribute("width", (r * s).toString()), e.setAttribute("height", (i * s).toString()), t.scale(s, s));
}, vi = (e, { width: t, height: r }) => {
  t && (e.style.width = typeof t == "number" ? `${t}px` : t), r && (e.style.height = typeof r == "number" ? `${r}px` : r);
};
function Ms(e) {
  return e.onselectstart !== void 0 && (e.onselectstart = () => !1), e.style.userSelect = $r, e;
}
var wo = class {
  constructor(e) {
    f(this, "_originalCanvasStyle", void 0), f(this, "lower", void 0);
    let t = this.createLowerCanvas(e);
    this.lower = {
      el: t,
      ctx: t.getContext("2d")
    };
  }
  createLowerCanvas(e) {
    let t = (r = e) && r.getContext !== void 0 ? e : e && we().getElementById(e) || Tt();
    var r;
    if (t.hasAttribute("data-fabric")) throw new Ct("Trying to initialize a canvas that has already been initialized. Did you forget to dispose the canvas?");
    return this._originalCanvasStyle = t.style.cssText, t.setAttribute("data-fabric", "main"), t.classList.add("lower-canvas"), t;
  }
  cleanupDOM({ width: e, height: t }) {
    let { el: r } = this.lower;
    r.classList.remove("lower-canvas"), r.removeAttribute("data-fabric"), r.setAttribute("width", `${e}`), r.setAttribute("height", `${t}`), r.style.cssText = this._originalCanvasStyle || "", this._originalCanvasStyle = void 0;
  }
  setDimensions(e, t) {
    let { el: r, ctx: i } = this.lower;
    bo(r, i, e, t);
  }
  setCSSDimensions(e) {
    vi(this.lower.el, e);
  }
  calcOffset() {
    return (function(e) {
      var t;
      let r = e && gt(e), i = {
        left: 0,
        top: 0
      };
      if (!r) return i;
      let s = ((t = Co(e)) == null ? void 0 : t.getComputedStyle(e, null)) || {};
      i.left += parseInt(s.borderLeftWidth, 10) || 0, i.top += parseInt(s.borderTopWidth, 10) || 0, i.left += parseInt(s.paddingLeft, 10) || 0, i.top += parseInt(s.paddingTop, 10) || 0;
      let o = {
        left: 0,
        top: 0
      }, n = r.documentElement;
      e.getBoundingClientRect !== void 0 && (o = e.getBoundingClientRect());
      let a = So(e);
      return {
        left: o.left + a.left - (n.clientLeft || 0) + i.left,
        top: o.top + a.top - (n.clientTop || 0) + i.top
      };
    })(this.lower.el);
  }
  dispose() {
    wt().dispose(this.lower.el), delete this.lower;
  }
}, _a = {
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
  viewportTransform: [...et],
  patternQuality: "best"
}, Sa = hr({
  capitalize: () => Ca,
  escapeXml: () => M,
  graphemeSplit: () => zr
}), Ca = (e, t = !1) => `${e.charAt(0).toUpperCase()}${t ? e.slice(1) : e.slice(1).toLowerCase()}`, M = (e) => e.toString().replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&apos;").replace(/</g, "&lt;").replace(/>/g, "&gt;"), Ae, zr = (e) => {
  if (Ae || Ae || (Ae = "Intl" in ye() && "Segmenter" in Intl && new Intl.Segmenter(void 0, { granularity: "grapheme" })), Ae) {
    let t = Ae.segment(e);
    return Array.from(t).map(({ segment: r }) => r);
  }
  return ba(e);
}, ba = (e) => {
  let t = [];
  for (let r, i = 0; i < e.length; i++) (r = wa(e, i)) !== !1 && t.push(r);
  return t;
}, wa = (e, t) => {
  let r = e.charCodeAt(t);
  if (isNaN(r)) return "";
  if (r < 55296 || r > 57343) return e.charAt(t);
  if (55296 <= r && r <= 56319) {
    if (e.length <= t + 1) throw "High surrogate without following low surrogate";
    let s = e.charCodeAt(t + 1);
    if (56320 > s || s > 57343) throw "High surrogate without following low surrogate";
    return e.charAt(t) + e.charAt(t + 1);
  }
  if (t === 0) throw "Low surrogate without preceding high surrogate";
  let i = e.charCodeAt(t - 1);
  if (55296 > i || i > 56319) throw "Low surrogate without preceding high surrogate";
  return !1;
}, Gr = class To extends go(fo) {
  get lowerCanvasEl() {
    var t;
    return (t = this.elements.lower) == null ? void 0 : t.el;
  }
  get contextContainer() {
    var t;
    return (t = this.elements.lower) == null ? void 0 : t.ctx;
  }
  static getDefaults() {
    return To.ownDefaults;
  }
  constructor(t, r = {}) {
    super(), Object.assign(this, this.constructor.getDefaults()), this.set(r), this.initElements(t), this._setDimensionsImpl({
      width: this.width || this.elements.lower.el.width || 0,
      height: this.height || this.elements.lower.el.height || 0
    }), this.skipControlsDrawing = !1, this.viewportTransform = [...this.viewportTransform], this.calcViewportBoundaries();
  }
  initElements(t) {
    this.elements = new wo(t);
  }
  add(...t) {
    let r = super.add(...t);
    return t.length > 0 && this.renderOnAddRemove && this.requestRenderAll(), r;
  }
  insertAt(t, ...r) {
    let i = super.insertAt(t, ...r);
    return r.length > 0 && this.renderOnAddRemove && this.requestRenderAll(), i;
  }
  remove(...t) {
    let r = super.remove(...t);
    return r.length > 0 && this.renderOnAddRemove && this.requestRenderAll(), r;
  }
  _onObjectAdded(t) {
    t.canvas && t.canvas !== this && (zt("warn", `Canvas is trying to add an object that belongs to a different canvas.
Resulting to default behavior: removing object from previous canvas and adding to new canvas`), t.canvas.remove(t)), t._set("canvas", this), t.setCoords(), this.fire("object:added", { target: t }), t.fire("added", { target: this });
  }
  _onObjectRemoved(t) {
    t._set("canvas", void 0), this.fire("object:removed", { target: t }), t.fire("removed", { target: this });
  }
  _onStackOrderChanged() {
    this.renderOnAddRemove && this.requestRenderAll();
  }
  getRetinaScaling() {
    return this.enableRetinaScaling ? io() : 1;
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
  _setDimensionsImpl(t, { cssOnly: r = !1, backstoreOnly: i = !1 } = {}) {
    if (!r) {
      let s = {
        width: this.width,
        height: this.height,
        ...t
      };
      this.elements.setDimensions(s, this.getRetinaScaling()), this.hasLostContext = !0, this.width = s.width, this.height = s.height;
    }
    i || this.elements.setCSSDimensions(t), this.calcOffset();
  }
  setDimensions(t, r) {
    this._setDimensionsImpl(t, r), r && r.cssOnly || this.requestRenderAll();
  }
  getZoom() {
    return Qi(this.viewportTransform);
  }
  setViewportTransform(t) {
    this.viewportTransform = t, this.calcViewportBoundaries(), this.renderOnAddRemove && this.requestRenderAll();
  }
  zoomToPoint(t, r) {
    let i = t, s = [...this.viewportTransform], o = N(t, lt(s));
    s[0] = r, s[3] = r;
    let n = N(o, s);
    s[4] += i.x - n.x, s[5] += i.y - n.y, this.setViewportTransform(s);
  }
  setZoom(t) {
    this.zoomToPoint(new v(0, 0), t);
  }
  absolutePan(t) {
    let r = [...this.viewportTransform];
    return r[4] = -t.x, r[5] = -t.y, this.setViewportTransform(r);
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
    this.nextRenderHandle || this.disposed || this.destroyed || (this.nextRenderHandle = tr(() => this.renderAndReset()));
  }
  calcViewportBoundaries() {
    let t = this.width, r = this.height, i = lt(this.viewportTransform), s = N({
      x: 0,
      y: 0
    }, i), o = N({
      x: t,
      y: r
    }, i), n = s.min(o), a = s.max(o);
    return this.vptCoords = {
      tl: n,
      tr: new v(a.x, n.y),
      bl: new v(n.x, a.y),
      br: a
    };
  }
  cancelRequestedRender() {
    this.nextRenderHandle && (po(this.nextRenderHandle), this.nextRenderHandle = 0);
  }
  drawControls(t) {
  }
  renderCanvas(t, r) {
    if (this.destroyed) return;
    let i = this.viewportTransform, s = this.clipPath;
    this.calcViewportBoundaries(), this.clearContext(t), t.imageSmoothingEnabled = this.imageSmoothingEnabled, t.patternQuality = this.patternQuality, this.fire("before:render", { ctx: t }), this._renderBackground(t), t.save(), t.transform(i[0], i[1], i[2], i[3], i[4], i[5]), this._renderObjects(t, r), t.restore(), this.controlsAboveOverlay || this.skipControlsDrawing || this.drawControls(t), s && (s._set("canvas", this), s.shouldCache(), s._transformDone = !0, s.renderCache({ forClipping: !0 }), this.drawClipPathOnCanvas(t, s)), this._renderOverlay(t), this.controlsAboveOverlay && !this.skipControlsDrawing && this.drawControls(t), this.fire("after:render", { ctx: t }), this.__cleanupTask && (this.__cleanupTask(), this.__cleanupTask = void 0);
  }
  drawClipPathOnCanvas(t, r) {
    let i = this.viewportTransform;
    t.save(), t.transform(...i), t.globalCompositeOperation = "destination-in", r.transform(t), t.scale(1 / r.zoomX, 1 / r.zoomY), t.drawImage(r._cacheCanvas, -r.cacheTranslationX, -r.cacheTranslationY), t.restore();
  }
  _renderObjects(t, r) {
    for (let i = 0, s = r.length; i < s; ++i) r[i] && r[i].render(t);
  }
  _renderBackgroundOrOverlay(t, r) {
    let i = this[`${r}Color`], s = this[`${r}Image`], o = this.viewportTransform, n = this[`${r}Vpt`];
    if (!i && !s) return;
    let a = ut(i);
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
    return N(this.getCenterPoint(), lt(this.viewportTransform));
  }
  _centerObject(t, r) {
    t.setXY(r, L, L), t.setCoords(), this.renderOnAddRemove && this.requestRenderAll();
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
  _toObjectMethod(t, r) {
    let i = this.clipPath, s = i && !i.excludeFromExport ? this._toObject(i, t, r) : null;
    return {
      version: mi,
      ...ae(this, r),
      objects: this._objects.filter((o) => !o.excludeFromExport).map((o) => this._toObject(o, t, r)),
      ...this.__serializeBgOverlay(t, r),
      ...s ? { clipPath: s } : null
    };
  }
  _toObject(t, r, i) {
    let s;
    this.includeDefaultValues || (s = t.includeDefaultValues, t.includeDefaultValues = !1);
    let o = t[r](i);
    return this.includeDefaultValues || (t.includeDefaultValues = !!s), o;
  }
  __serializeBgOverlay(t, r) {
    let i = {}, s = this.backgroundImage, o = this.overlayImage, n = this.backgroundColor, a = this.overlayColor;
    return ut(n) ? n.excludeFromExport || (i.background = n.toObject(r)) : n && (i.background = n), ut(a) ? a.excludeFromExport || (i.overlay = a.toObject(r)) : a && (i.overlay = a), s && !s.excludeFromExport && (i.backgroundImage = this._toObject(s, t, r)), o && !o.excludeFromExport && (i.overlayImage = this._toObject(o, t, r)), i;
  }
  toSVG(t = {}, r) {
    t.reviver = r;
    let i = [];
    var s;
    return this._setSVGPreamble(i, t), this._setSVGHeader(i, t), this.clipPath && i.push(`<g clip-path="url(#${M((s = this.clipPath.clipPathId) == null ? "" : s)})" >
`), this._setSVGBgOverlayColor(i, "background"), this._setSVGBgOverlayImage(i, "backgroundImage", r), this._setSVGObjects(i, r), this.clipPath && i.push(`</g>
`), this._setSVGBgOverlayColor(i, "overlay"), this._setSVGBgOverlayImage(i, "overlayImage", r), i.push("</svg>"), i.join("");
  }
  _setSVGPreamble(t, r) {
    r.suppressPreamble || t.push('<?xml version="1.0" encoding="', r.encoding || "UTF-8", `" standalone="no" ?>
`, '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" ', `"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
`);
  }
  _setSVGHeader(t, r) {
    let i = r.width || `${this.width}`, s = r.height || `${this.height}`, o = P.NUM_FRACTION_DIGITS, n = r.viewBox, a;
    if (n) a = `viewBox="${n.x} ${n.y} ${n.width} ${n.height}" `;
    else if (this.svgViewportTransformation) {
      let l = this.viewportTransform;
      a = `viewBox="${F(-l[4] / l[0], o)} ${F(-l[5] / l[3], o)} ${F(this.width / l[0], o)} ${F(this.height / l[3], o)}" `;
    } else a = `viewBox="0 0 ${this.width} ${this.height}" `;
    t.push("<svg ", 'xmlns="http://www.w3.org/2000/svg" ', 'xmlns:xlink="http://www.w3.org/1999/xlink" ', 'version="1.1" ', 'width="', i, '" ', 'height="', s, '" ', a, `xml:space="preserve">
`, "<desc>Created with Fabric.js ", mi, `</desc>
`, `<defs>
`, this.createSVGFontFacesMarkup(), this.createSVGRefElementsMarkup(), this.createSVGClipPathMarkup(r), `</defs>
`);
  }
  createSVGClipPathMarkup(t) {
    let r = this.clipPath;
    return r ? (r.clipPathId = `CLIPPATH_${Gt()}`, `<clipPath id="${r.clipPathId}" >
${r.toClipPathSVG(t.reviver)}</clipPath>
`) : "";
  }
  createSVGRefElementsMarkup() {
    return ["background", "overlay"].map((t) => {
      let r = this[`${t}Color`];
      if (ut(r)) {
        let i = this[`${t}Vpt`], s = this.viewportTransform, o = {
          isType: () => !1,
          width: this.width / (i ? s[0] : 1),
          height: this.height / (i ? s[3] : 1)
        };
        return r.toSVG(o, { additionalTransform: i ? Se(s) : "" });
      }
    }).join("");
  }
  createSVGFontFacesMarkup() {
    let t = [], r = {}, i = P.fontPaths;
    this._objects.forEach(function o(n) {
      t.push(n), kr(n) && n._objects.forEach(o);
    }), t.forEach((o) => {
      if (!(n = o) || typeof n._renderText != "function") return;
      var n;
      let { styles: a, fontFamily: l } = o;
      !r[l] && i[l] && (r[l] = !0, a && Object.values(a).forEach((h) => {
        Object.values(h).forEach(({ fontFamily: c = "" }) => {
          !r[c] && i[c] && (r[c] = !0);
        });
      }));
    });
    let s = Object.keys(r).map((o) => `		@font-face {
			font-family: '${o}';
			src: url('${i[o]}');
		}
`).join("");
    return s ? `	<style type="text/css"><![CDATA[
${s}]]></style>
` : "";
  }
  _setSVGObjects(t, r) {
    this.forEachObject((i) => {
      i.excludeFromExport || this._setSVGObject(t, i, r);
    });
  }
  _setSVGObject(t, r, i) {
    t.push(r.toSVG(i));
  }
  _setSVGBgOverlayImage(t, r, i) {
    let s = this[r];
    s && !s.excludeFromExport && s.toSVG && t.push(s.toSVG(i));
  }
  _setSVGBgOverlayColor(t, r) {
    let i = this[`${r}Color`];
    if (i) if (ut(i)) {
      let s = i.repeat || "", o = this.width, n = this.height, a = this[`${r}Vpt`] ? Se(lt(this.viewportTransform)) : "";
      t.push(`<rect transform="${a} translate(${o / 2},${n / 2})" x="${i.offsetX - o / 2}" y="${i.offsetY - n / 2}" width="${s !== "repeat-y" && s !== "no-repeat" || !ks(i) ? o : i.source.width}" height="${s !== "repeat-x" && s !== "no-repeat" || !ks(i) ? n : i.source.height}" fill="url(#SVGID_${i.id})"></rect>
`);
    } else t.push('<rect x="0" y="0" width="100%" height="100%" ', 'fill="', i, '"', `></rect>
`);
  }
  loadFromJSON(t, r, { signal: i } = {}) {
    if (!t) return Promise.reject(new Ct("`json` is undefined"));
    let { objects: s = [], ...o } = typeof t == "string" ? JSON.parse(t) : t, { backgroundImage: n, background: a, overlayImage: l, overlay: h, clipPath: c } = o, u = this.renderOnAddRemove;
    return this.renderOnAddRemove = !1, Promise.all([_e(s, {
      reviver: r,
      signal: i
    }), ur({
      backgroundImage: n,
      backgroundColor: a,
      overlayImage: l,
      overlayColor: h,
      clipPath: c
    }, { signal: i })]).then(([d, g]) => (this.clear(), this.add(...d), this.set(o), this.set(g), this.renderOnAddRemove = u, this));
  }
  clone(t) {
    let r = this.toObject(t);
    return this.cloneWithoutData().loadFromJSON(r);
  }
  cloneWithoutData() {
    let t = ht(this);
    return new this.constructor(t);
  }
  toDataURL(t = {}) {
    let { format: r = "png", quality: i = 1, multiplier: s = 1, enableRetinaScaling: o = !1 } = t, n = s * (o ? this.getRetinaScaling() : 1);
    return qi(this.toCanvasElement(n, t), r, i);
  }
  toBlob(t = {}) {
    let { format: r = "png", quality: i = 1, multiplier: s = 1, enableRetinaScaling: o = !1 } = t, n = s * (o ? this.getRetinaScaling() : 1);
    return Ki(this.toCanvasElement(n, t), r, i);
  }
  toCanvasElement(t = 1, { width: r, height: i, left: s, top: o, filter: n } = {}) {
    let a = (r || this.width) * t, l = (i || this.height) * t, h = this.getZoom(), c = this.width, u = this.height, d = this.skipControlsDrawing, g = h * t, p = this.viewportTransform, m = [
      g,
      0,
      0,
      g,
      (p[4] - (s || 0)) * t,
      (p[5] - (o || 0)) * t
    ], x = this.enableRetinaScaling, _ = ht({
      width: a,
      height: l
    }), y = n ? this._objects.filter((S) => n(S)) : this._objects;
    return this.enableRetinaScaling = !1, this.viewportTransform = m, this.width = a, this.height = l, this.skipControlsDrawing = !0, this.calcViewportBoundaries(), this.renderCanvas(_.getContext("2d"), y), this.viewportTransform = p, this.width = c, this.height = u, this.calcViewportBoundaries(), this.enableRetinaScaling = x, this.skipControlsDrawing = d, _;
  }
  dispose() {
    return !this.disposed && this.elements.cleanupDOM({
      width: this.width,
      height: this.height
    }), Fr.cancelByCanvas(this), this.disposed = !0, new Promise((t, r) => {
      let i = () => {
        this.destroy(), t(!0);
      };
      i.kill = r, this.__cleanupTask && this.__cleanupTask.kill("aborted"), this.destroyed ? t(!1) : this.nextRenderHandle ? this.__cleanupTask = i : i();
    });
  }
  destroy() {
    this.destroyed = !0, this.cancelRequestedRender(), this.forEachObject((t) => t.dispose()), this._objects = [], this.backgroundImage && this.backgroundImage.dispose(), this.backgroundImage = void 0, this.overlayImage && this.overlayImage.dispose(), this.overlayImage = void 0, this.elements.dispose();
  }
  toString() {
    return `#<Canvas (${this.complexity()}): { objects: ${this._objects.length} }>`;
  }
};
f(Gr, "ownDefaults", _a);
var Ta = [
  "touchstart",
  "touchmove",
  "touchend"
], Oo = (e) => {
  let t = So(e.target), r = (function(i) {
    let s = i.changedTouches;
    return s && s[0] ? s[0] : i;
  })(e);
  return new v(r.clientX + t.left, r.clientY + t.top);
}, Lr = (e) => Ta.includes(e.type) || e.pointerType === "touch", Ds = (e) => {
  e.preventDefault(), e.stopPropagation();
}, bt = (e) => {
  let t = 0, r = 0, i = 0, s = 0;
  for (let o = 0, n = e.length; o < n; o++) {
    let { x: a, y: l } = e[o];
    (a > i || !o) && (i = a), (a < t || !o) && (t = a), (l > s || !o) && (s = l), (l < r || !o) && (r = l);
  }
  return {
    left: t,
    top: r,
    width: i - t,
    height: s - r
  };
}, Oa = (e, t) => {
  Ce(e, Y(lt(t), e.calcOwnMatrix()));
}, ko = (e, t) => Ce(e, Y(t, e.calcOwnMatrix())), Ce = (e, t) => {
  let { translateX: r, translateY: i, scaleX: s, scaleY: o, ...n } = xe(t), a = new v(r, i);
  e.flipX = !1, e.flipY = !1, Object.assign(e, n), e.set({
    scaleX: s,
    scaleY: o
  }), e.setPositionByOrigin(a, L, L);
}, Mo = (e) => {
  e.scaleX = 1, e.scaleY = 1, e.skewX = 0, e.skewY = 0, e.flipX = !1, e.flipY = !1, e.rotate(0);
}, rs = (e) => ({
  scaleX: e.scaleX,
  scaleY: e.scaleY,
  skewX: e.skewX,
  skewY: e.skewY,
  angle: e.angle,
  left: e.left,
  flipX: e.flipX,
  flipY: e.flipY,
  top: e.top
}), Ur = (e, t, r) => {
  let i = e / 2, s = t / 2, o = bt([
    new v(-i, -s),
    new v(i, -s),
    new v(-i, s),
    new v(i, s)
  ].map((n) => n.transform(r)));
  return new v(o.width, o.height);
}, dr = (e = et, t = et) => Y(lt(t), e), Pt = (e, t = et, r = et) => e.transform(dr(t, r)), Do = (e, t = et, r = et) => e.transform(dr(t, r), !0), is = (e, t, r) => {
  let i = dr(t, r);
  return Ce(e, Y(i, e.calcOwnMatrix())), i;
}, ka = {
  left: -0.5,
  top: -0.5,
  center: 0,
  bottom: 0.5,
  right: 0.5
}, Z = (e) => typeof e == "string" ? ka[e] : e - 0.5, Ma = new v(1, 0), Eo = new v(), ss = (e, t) => e.rotate(t), sr = (e, t) => new v(t).subtract(e), Rr = (e) => e.distanceFrom(Eo), Br = (e, t) => Math.atan2(fe(e, t), Po(e, t)), os = (e) => Br(Ma, e), Nr = (e) => e.eq(Eo) ? e : e.scalarDivide(Rr(e)), ns = (e, t = !0) => Nr(new v(-e.y, e.x).scalarMultiply(t ? 1 : -1)), fe = (e, t) => e.x * t.y - e.y * t.x, Po = (e, t) => e.x * t.x + e.y * t.y, yi = (e, t, r) => {
  if (e.eq(t) || e.eq(r)) return !0;
  let i = fe(t, r), s = fe(t, e), o = fe(r, e);
  return i >= 0 ? s >= 0 && o <= 0 : !(s <= 0 && o >= 0);
}, as = "not-allowed";
function Ao(e) {
  return Z(e.originX) === Z("center") && Z(e.originY) === Z("center");
}
function Es(e) {
  return 0.5 - Z(e);
}
var mt = (e, t) => e[t], ls = (e, t, r, i) => ({
  e,
  transform: t,
  pointer: new v(r, i)
});
function jo(e, t, r) {
  let i = r, s = os(sr(Pt(e.getCenterPoint(), e.canvas.viewportTransform, void 0), i)) + vt;
  return Math.round(s % vt / ma);
}
function qr({ target: e, corner: t }, r, i, s, o) {
  var n;
  let a = e.controls[t], l = ((n = e.canvas) == null ? void 0 : n.getZoom()) || 1, h = e.padding / l, c = (function(u, d, g, p) {
    let m = u.getRelativeCenterPoint(), x = g !== void 0 && p !== void 0 ? u.translateToGivenOrigin(m, L, L, g, p) : new v(u.left, u.top);
    return (u.angle ? d.rotate(-I(u.angle), m) : d).subtract(x);
  })(e, new v(s, o), r, i);
  return c.x >= h && (c.x -= h), c.x <= -h && (c.x += h), c.y >= h && (c.y -= h), c.y <= h && (c.y += h), c.x -= a.offsetX, c.y -= a.offsetY, c;
}
var Da = new RegExp(String.raw`[\0-\x1F\x7F;<>\\]|\/\*|\*\/|url\s*\(|expression\s*\(|(?:java|vb)script\s*:|data\s*:|@import\b`, "iu"), Kr = (e) => typeof e == "string" && e.trim().length > 0 && !Da.test(e), te = (e, t = "") => {
  let r = Number(e);
  return Number.isFinite(r) ? `${r}` : t;
}, ee = (e, t = "") => typeof e == "string" && Kr(e) ? e : t, Ir = (e) => e.replace(/\s+/g, " "), Ps = {
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
}, si = (e, t, r) => (r < 0 && (r += 1), r > 1 && --r, r < 1 / 6 ? e + 6 * (t - e) * r : r < 0.5 ? t : r < 2 / 3 ? e + (t - e) * (2 / 3 - r) * 6 : e), As = (e, t, r, i) => {
  e /= 255, t /= 255, r /= 255;
  let s = Math.max(e, t, r), o = Math.min(e, t, r), n, a, l = (s + o) / 2;
  if (s === o) n = a = 0;
  else {
    let h = s - o;
    switch (a = l > 0.5 ? h / (2 - s - o) : h / (s + o), s) {
      case e:
        n = (t - r) / h + (t < r ? 6 : 0);
        break;
      case t:
        n = (r - e) / h + 2;
        break;
      case r:
        n = (e - t) / h + 4;
    }
    n /= 6;
  }
  return [
    Math.round(360 * n),
    Math.round(100 * a),
    Math.round(100 * l),
    i
  ];
}, js = (e = "1") => parseFloat(e) / (e.endsWith("%") ? 100 : 1), fr = (e) => Math.min(Math.round(e), 255).toString(16).toUpperCase().padStart(2, "0"), Fs = ([e, t, r, i = 1]) => {
  let s = Math.round(0.3 * e + 0.59 * t + 0.11 * r);
  return [
    s,
    s,
    s,
    i
  ];
}, K = class U {
  constructor(t) {
    if (f(this, "isUnrecognised", !1), t) if (t instanceof U) this.setSource([...t._source]);
    else if (Array.isArray(t)) {
      let [r, i, s, o = 1] = t;
      this.setSource([
        r,
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
    return (t = t.toLowerCase()) in Ps && (t = Ps[t]), t === "transparent" ? [
      255,
      255,
      255,
      0
    ] : U.sourceFromHex(t) || U.sourceFromRgb(t) || U.sourceFromHsl(t) || (this.isUnrecognised = !0) && [
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
    let [t, r, i] = this.getSource();
    return `rgb(${t},${r},${i})`;
  }
  toRgba() {
    return `rgba(${this.getSource().join(",")})`;
  }
  toHsl() {
    let [t, r, i] = As(...this.getSource());
    return `hsl(${t},${r}%,${i}%)`;
  }
  toHsla() {
    let [t, r, i, s] = As(...this.getSource());
    return `hsla(${t},${r}%,${i}%,${s})`;
  }
  toHex() {
    return this.toHexa().slice(0, 6);
  }
  toHexa() {
    let [t, r, i, s] = this.getSource();
    return `${fr(t)}${fr(r)}${fr(i)}${fr(Math.round(255 * s))}`;
  }
  getAlpha() {
    return this.getSource()[3];
  }
  setAlpha(t) {
    return this._source[3] = t, this;
  }
  toGrayscale() {
    return this.setSource(Fs(this.getSource())), this;
  }
  toBlackWhite(t) {
    let [r, , , i] = Fs(this.getSource()), s = r < (t || 127) ? 0 : 255;
    return this.setSource([
      s,
      s,
      s,
      i
    ]), this;
  }
  overlayWith(t) {
    t instanceof U || (t = new U(t));
    let r = this.getSource(), i = t.getSource(), [s, o, n] = r.map((a, l) => Math.round(0.5 * a + 0.5 * i[l]));
    return this.setSource([
      s,
      o,
      n,
      r[3]
    ]), this;
  }
  static fromRgb(t) {
    return U.fromRgba(t);
  }
  static fromRgba(t) {
    return new U(U.sourceFromRgb(t));
  }
  static sourceFromRgb(t) {
    let r = Ir(t).match(/^rgba?\(\s?(\d{0,3}(?:\.\d+)?%?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?(?:\s?[,/]\s?(\d{0,3}(?:\.\d+)?%?)\s?)?\)$/i);
    if (r) {
      let [i, s, o] = r.slice(1, 4).map((n) => {
        let a = parseFloat(n);
        return n.endsWith("%") ? Math.round(2.55 * a) : a;
      });
      return [
        i,
        s,
        o,
        js(r[4])
      ];
    }
  }
  static fromHsl(t) {
    return U.fromHsla(t);
  }
  static fromHsla(t) {
    return new U(U.sourceFromHsl(t));
  }
  static sourceFromHsl(t) {
    let r = Ir(t).match(/^hsla?\(\s?([+-]?\d{0,3}(?:\.\d+)?(?:deg|turn|rad)?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?[\s|,]\s?(\d{0,3}(?:\.\d+)?%?)\s?(?:\s?[,/]\s?(\d*(?:\.\d+)?%?)\s?)?\)$/i);
    if (!r) return;
    let i = (U.parseAngletoDegrees(r[1]) % 360 + 360) % 360 / 360, s = parseFloat(r[2]) / 100, o = parseFloat(r[3]) / 100, n, a, l;
    if (s === 0) n = a = l = o;
    else {
      let h = o <= 0.5 ? o * (s + 1) : o + s - o * s, c = 2 * o - h;
      n = si(c, h, i + 1 / 3), a = si(c, h, i), l = si(c, h, i - 1 / 3);
    }
    return [
      Math.round(255 * n),
      Math.round(255 * a),
      Math.round(255 * l),
      js(r[4])
    ];
  }
  static fromHex(t) {
    return new U(U.sourceFromHex(t));
  }
  static sourceFromHex(t) {
    if (t.match(/^#?(([0-9a-f]){3,4}|([0-9a-f]{2}){3,4})$/i)) {
      let r = t.slice(t.indexOf("#") + 1), i;
      i = r.length <= 4 ? r.split("").map((l) => l + l) : r.match(/.{2}/g);
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
    let r = t.toLowerCase(), i = parseFloat(r);
    return r.includes("rad") ? Et(i) : r.includes("turn") ? 360 * i : i;
  }
}, Ea = (e) => {
  let t = [
    "instantiated_by_use",
    "style",
    "id",
    "class"
  ];
  switch (e) {
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
}, se = (e, t = 16) => {
  let r = /\D{0,2}$/.exec(e), i = parseFloat(e), s = P.DPI;
  switch (r?.[0]) {
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
}, Fo = (e) => {
  let [t, r] = e.trim().split(" "), [i, s] = (o = t) && o !== "none" ? [o.slice(1, 4), o.slice(5, 8)] : o === "none" ? [o, o] : ["Mid", "Mid"];
  var o;
  return {
    meetOrSlice: r || "meet",
    alignX: i,
    alignY: s
  };
}, or = (e, t, r = !0) => {
  let i, s;
  if (t) if (t.toLive) i = `url(#SVGID_${M(t.id)})`;
  else {
    let o = String(t);
    if (Kr(o)) {
      let n = new K(o), a = n.getAlpha();
      i = n.toRgb(), a !== 1 && (s = a.toString());
    } else i = new K("black").toRgb();
  }
  else i = "none";
  return r ? `${e}: ${i}; ${s ? `${e}-opacity: ${s}; ` : ""}` : `${e}="${i}" ${s ? `${e}-opacity="${s}" ` : ""}`;
}, Lo = class {
  getSvgStyles(e) {
    let t = this.fillRule == null ? "nonzero" : ee(this.fillRule), r = this.strokeWidth == null ? "0" : te(this.strokeWidth), i = this.strokeDashArray == null ? $r : this.strokeDashArray.every((d) => Number.isFinite(Number(d))) ? this.strokeDashArray.join(" ") : "", s = this.strokeDashOffset == null ? "0" : te(this.strokeDashOffset), o = this.strokeLineCap == null ? "butt" : ee(this.strokeLineCap), n = this.strokeLineJoin == null ? "miter" : ee(this.strokeLineJoin), a = this.strokeMiterLimit == null ? "4" : te(this.strokeMiterLimit), l = this.opacity == null ? "1" : te(this.opacity), h = this.visible ? "" : " visibility: hidden;", c = e ? "" : this.getSvgFilter(), u = or(st, this.fill);
    return [
      or(Dt, this.stroke),
      r ? `stroke-width: ${r}; ` : "",
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
  getSvgTransform(e, t = "") {
    return `transform="${Se(e ? this.calcTransformMatrix() : this.calcOwnMatrix())}${t}" `;
  }
  _toSVG(e) {
    return [""];
  }
  toSVG(e) {
    return this._createBaseSVGMarkup(this._toSVG(e), { reviver: e });
  }
  toClipPathSVG(e) {
    return "	" + this._createBaseClipPathSVGMarkup(this._toSVG(e), { reviver: e });
  }
  _createBaseClipPathSVGMarkup(e, { reviver: t, additionalTransform: r = "" } = {}) {
    let i = [this.getSvgTransform(!0, r), this.getSvgCommons()].join(""), s = e.indexOf("COMMON_PARTS");
    return e[s] = i, t ? t(e.join("")) : e.join("");
  }
  _createBaseSVGMarkup(e, { noStyle: t, reviver: r, withShadow: i, additionalTransform: s } = {}) {
    let o = t ? "" : `style="${this.getSvgStyles()}" `, n = i ? `style="${this.getSvgFilter()}" ` : "", a = this.clipPath, l = this.strokeUniform ? 'vector-effect="non-scaling-stroke" ' : "", h = a && a.absolutePositioned, c = this.stroke, u = this.fill, d = this.shadow, g = [], p = e.indexOf("COMMON_PARTS"), m;
    return a && (a.clipPathId = `CLIPPATH_${Gt()}`, m = `<clipPath id="${a.clipPathId}" >
${a.toClipPathSVG(r)}</clipPath>
`), h && g.push("<g ", n, this.getSvgCommons(), ` >
`), g.push("<g ", this.getSvgTransform(!1), h ? "" : n + this.getSvgCommons(), ` >
`), e[p] = [
      o,
      l,
      t ? "" : this.addPaintOrder(),
      " ",
      s ? `transform="${s}" ` : ""
    ].join(""), ut(u) && g.push(u.toSVG(this)), ut(c) && g.push(c.toSVG(this)), d && g.push(d.toSVG(this)), a && g.push(m), g.push(e.join("")), g.push(`</g>
`), h && g.push(`</g>
`), r ? r(g.join("")) : g.join("");
  }
  addPaintOrder() {
    return this.paintFirst === "fill" ? "" : ` paint-order="${M(this.paintFirst)}" `;
  }
};
function Jr(e) {
  return RegExp("^(" + e.join("|") + ")\\b", "i");
}
var be = "textDecorationThickness", Qr = "textDecorationColor", Ro = [
  "fontSize",
  "fontWeight",
  "fontFamily",
  "fontStyle"
], Bo = [
  "underline",
  "overline",
  "linethrough"
], Io = [
  ...Ro,
  "lineHeight",
  "text",
  "charSpacing",
  "textAlign",
  "styles",
  "path",
  "pathStartOffset",
  "pathSide",
  "pathAlign"
], Xo = [
  ...Io,
  ...Bo,
  "textBackgroundColor",
  "direction",
  be,
  Qr
], Pa = [
  ...Ro,
  ...Bo,
  Dt,
  "strokeWidth",
  st,
  "deltaY",
  "textBackgroundColor",
  be,
  Qr
], Aa = {
  _reNewline: Ui,
  _reSpacesAndTabs: /[ \t\r]/g,
  _reSpaceAndTab: /[ \t\r]/,
  _reWords: /\S+/g,
  fontSize: 40,
  fontWeight: Ts,
  fontFamily: "Times New Roman",
  underline: !1,
  overline: !1,
  linethrough: !1,
  textAlign: H,
  fontStyle: Ts,
  lineHeight: 1.16,
  textBackgroundColor: "",
  stroke: null,
  shadow: null,
  path: void 0,
  pathStartOffset: 0,
  pathSide: H,
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
  [be]: 66.667
}, hs = "justify", ft = String.raw`[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?`, oi = String.raw`(?:\s*,?\s+|\s*,\s*)`, ja = RegExp("(normal|italic)?\\s*(normal|small-caps)?\\s*(normal|bold|bolder|lighter|100|200|300|400|500|600|700|800|900)?\\s*(" + ft + "(?:px|cm|mm|em|pt|pc|in)*)(?:\\/(normal|" + ft + "))?\\s+(.*)"), Fa = {
  cx: H,
  x: H,
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
  "text-decoration-thickness": be,
  "text-decoration-color": Qr
}, Ls = "font-size", Rs = "clip-path", zc = Jr([
  "path",
  "circle",
  "polygon",
  "polyline",
  "ellipse",
  "rect",
  "line",
  "image",
  "text"
]), Gc = Jr([
  "symbol",
  "image",
  "marker",
  "pattern",
  "view",
  "svg"
]), Bs = Jr([
  "symbol",
  "g",
  "a",
  "svg",
  "clipPath",
  "defs"
]), Uc = new RegExp(String.raw`^\s*(${ft})${oi}(${ft})${oi}(${ft})${oi}(${ft})\s*$`), Is = "(-?\\d+(?:\\.\\d*)?(?:px)?(?:\\s?|$))?", Xs = RegExp("(?:\\s|^)" + Is + Is + "(" + ft + "?(?:px)?)?(?:\\s?|$)(?:$|\\s)"), pe = class Mr {
  constructor(t = {}) {
    let r = typeof t == "string" ? Mr.parseShadow(t) : t;
    Object.assign(this, Mr.ownDefaults, r), this.id = Gt();
  }
  static parseShadow(t) {
    let r = t.trim(), [, i = 0, s = 0, o = 0] = (Xs.exec(r) || []).map((n) => parseFloat(n) || 0);
    return {
      color: (r.replace(Xs, "") || "rgb(0,0,0)").trim(),
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
    let r = ss(new v(this.offsetX, this.offsetY), I(-t.angle)), i = P.NUM_FRACTION_DIGITS, s = new K(this.color), o = 40, n = 40;
    return t.width && t.height && (o = 100 * F((Math.abs(r.x) + this.blur) / t.width, i) + 20, n = 100 * F((Math.abs(r.y) + this.blur) / t.height, i) + 20), t.flipX && (r.x *= -1), t.flipY && (r.y *= -1), `<filter id="SVGID_${M(this.id)}" y="-${n}%" height="${100 + 2 * n}%" x="-${o}%" width="${100 + 2 * o}%" >
	<feGaussianBlur in="SourceAlpha" stdDeviation="${F(this.blur ? this.blur / 2 : 0, i)}"></feGaussianBlur>
	<feOffset dx="${F(r.x, i)}" dy="${F(r.y, i)}" result="oBlur" ></feOffset>
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
    }, r = Mr.ownDefaults;
    return this.includeDefaultValues ? t : es(t, (i, s) => i !== r[s]);
  }
  static async fromObject(t) {
    return new this(t);
  }
};
f(pe, "ownDefaults", {
  color: "rgb(0,0,0)",
  blur: 0,
  offsetX: 0,
  offsetY: 0,
  affectStroke: !1,
  includeDefaultValues: !0,
  nonScaling: !1
}), f(pe, "type", "shadow"), w.setClass(pe, "shadow");
var oe = (e, t, r) => Math.max(e, Math.min(t, r)), La = [
  "top",
  H,
  Nt,
  qt,
  "flipX",
  "flipY",
  "originX",
  "originY",
  "angle",
  "opacity",
  "globalCompositeOperation",
  "shadow",
  "visible",
  Te,
  Oe
], At = [
  st,
  Dt,
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
], Ra = {
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
  paintFirst: st,
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
}, Ba = hr({
  defaultEasing: () => $o,
  easeInBack: () => ol,
  easeInBounce: () => Wo,
  easeInCirc: () => Za,
  easeInCubic: () => Ia,
  easeInElastic: () => rl,
  easeInExpo: () => Ka,
  easeInOutBack: () => al,
  easeInOutBounce: () => ll,
  easeInOutCirc: () => el,
  easeInOutCubic: () => Ya,
  easeInOutElastic: () => sl,
  easeInOutExpo: () => Qa,
  easeInOutQuad: () => ul,
  easeInOutQuart: () => Va,
  easeInOutQuint: () => Ga,
  easeInOutSine: () => qa,
  easeInQuad: () => hl,
  easeInQuart: () => $a,
  easeInQuint: () => Ha,
  easeInSine: () => Ua,
  easeOutBack: () => nl,
  easeOutBounce: () => us,
  easeOutCirc: () => tl,
  easeOutCubic: () => Xa,
  easeOutElastic: () => il,
  easeOutExpo: () => Ja,
  easeOutQuad: () => cl,
  easeOutQuart: () => Wa,
  easeOutQuint: () => za,
  easeOutSine: () => Na
}), cs = (e, t, r, i) => (e < Math.abs(t) ? (e = t, i = r / 4) : i = t === 0 && e === 0 ? r / vt * Math.asin(1) : r / vt * Math.asin(t / e), {
  a: e,
  c: t,
  p: r,
  s: i
}), Yo = (e, t, r, i, s) => e * 2 ** (10 * --i) * Math.sin((i * s - t) * vt / r), $o = (e, t, r, i) => -r * Math.cos(e / i * Ut) + r + t, Ia = (e, t, r, i) => r * (e / i) ** 3 + t, Xa = (e, t, r, i) => r * ((e / i - 1) ** 3 + 1) + t, Ya = (e, t, r, i) => (e /= i / 2) < 1 ? r / 2 * e ** 3 + t : r / 2 * ((e - 2) ** 3 + 2) + t, $a = (e, t, r, i) => r * (e /= i) * e ** 3 + t, Wa = (e, t, r, i) => -r * ((e = e / i - 1) * e ** 3 - 1) + t, Va = (e, t, r, i) => (e /= i / 2) < 1 ? r / 2 * e ** 4 + t : -r / 2 * ((e -= 2) * e ** 3 - 2) + t, Ha = (e, t, r, i) => r * (e / i) ** 5 + t, za = (e, t, r, i) => r * ((e / i - 1) ** 5 + 1) + t, Ga = (e, t, r, i) => (e /= i / 2) < 1 ? r / 2 * e ** 5 + t : r / 2 * ((e - 2) ** 5 + 2) + t, Ua = (e, t, r, i) => -r * Math.cos(e / i * Ut) + r + t, Na = (e, t, r, i) => r * Math.sin(e / i * Ut) + t, qa = (e, t, r, i) => -r / 2 * (Math.cos(Math.PI * e / i) - 1) + t, Ka = (e, t, r, i) => e === 0 ? t : r * 2 ** (10 * (e / i - 1)) + t, Ja = (e, t, r, i) => e === i ? t + r : r * -(2 ** (-10 * e / i) + 1) + t, Qa = (e, t, r, i) => e === 0 ? t : e === i ? t + r : (e /= i / 2) < 1 ? r / 2 * 2 ** (10 * (e - 1)) + t : r / 2 * -(2 ** (-10 * (e - 1)) + 2) + t, Za = (e, t, r, i) => -r * (Math.sqrt(1 - (e /= i) * e) - 1) + t, tl = (e, t, r, i) => r * Math.sqrt(1 - (e = e / i - 1) * e) + t, el = (e, t, r, i) => (e /= i / 2) < 1 ? -r / 2 * (Math.sqrt(1 - e ** 2) - 1) + t : r / 2 * (Math.sqrt(1 - (e -= 2) * e) + 1) + t, rl = (e, t, r, i) => {
  let s = r, o = 0;
  if (e === 0) return t;
  if ((e /= i) === 1) return t + r;
  o || (o = 0.3 * i);
  let { a: n, s: a, p: l } = cs(s, r, o, 1.70158);
  return -Yo(n, a, l, e, i) + t;
}, il = (e, t, r, i) => {
  let s = r, o = 0;
  if (e === 0) return t;
  if ((e /= i) === 1) return t + r;
  o || (o = 0.3 * i);
  let { a: n, s: a, p: l, c: h } = cs(s, r, o, 1.70158);
  return n * 2 ** (-10 * e) * Math.sin((e * i - a) * vt / l) + h + t;
}, sl = (e, t, r, i) => {
  let s = r, o = 0;
  if (e === 0) return t;
  if ((e /= i / 2) == 2) return t + r;
  o || (o = 0.3 * 1.5 * i);
  let { a: n, s: a, p: l, c: h } = cs(s, r, o, 1.70158);
  return e < 1 ? -0.5 * Yo(n, a, l, e, i) + t : n * 2 ** (-10 * --e) * Math.sin((e * i - a) * vt / l) * 0.5 + h + t;
}, ol = (e, t, r, i, s = 1.70158) => r * (e /= i) * e * ((s + 1) * e - s) + t, nl = (e, t, r, i, s = 1.70158) => r * ((e = e / i - 1) * e * ((s + 1) * e + s) + 1) + t, al = (e, t, r, i, s = 1.70158) => (e /= i / 2) < 1 ? r / 2 * (e * e * ((1 + (s *= 1.525)) * e - s)) + t : r / 2 * ((e -= 2) * e * ((1 + (s *= 1.525)) * e + s) + 2) + t, us = (e, t, r, i) => (e /= i) < 1 / 2.75 ? r * (7.5625 * e * e) + t : e < 2 / 2.75 ? r * (7.5625 * (e -= 1.5 / 2.75) * e + 0.75) + t : e < 2.5 / 2.75 ? r * (7.5625 * (e -= 2.25 / 2.75) * e + 0.9375) + t : r * (7.5625 * (e -= 2.625 / 2.75) * e + 0.984375) + t, Wo = (e, t, r, i) => r - us(i - e, 0, r, i) + t, ll = (e, t, r, i) => e < i / 2 ? 0.5 * Wo(2 * e, 0, r, i) + t : 0.5 * us(2 * e - i, 0, r, i) + 0.5 * r + t, hl = (e, t, r, i) => r * (e /= i) * e + t, cl = (e, t, r, i) => -r * (e /= i) * (e - 2) + t, ul = (e, t, r, i) => (e /= i / 2) < 1 ? r / 2 * e ** 2 + t : -r / 2 * (--e * (e - 2) - 1) + t, dl = () => !1, ds = class {
  constructor({ startValue: e, byValue: t, duration: r = 500, delay: i = 0, easing: s = $o, onStart: o = Or, onChange: n = Or, onComplete: a = Or, abort: l = dl, target: h }) {
    f(this, "_state", "pending"), f(this, "durationProgress", 0), f(this, "valueProgress", 0), this.tick = this.tick.bind(this), this.duration = r, this.delay = i, this.easing = s, this._onStart = o, this._onChange = n, this._onComplete = a, this._abort = l, this.target = h, this.startValue = e, this.byValue = t, this.value = this.startValue, this.endValue = Object.freeze(this.calculate(this.duration).value);
  }
  get state() {
    return this._state;
  }
  isDone() {
    return this._state === "aborted" || this._state === "completed";
  }
  start() {
    let e = (t) => {
      this._state === "pending" && (this.startTime = t || +/* @__PURE__ */ new Date(), this._state = "running", this._onStart(), this.tick(this.startTime));
    };
    this.register(), this.delay > 0 ? this.timeout = ye().setTimeout(() => tr(e), this.delay) : tr(e);
  }
  tick(e) {
    let t = (e || +/* @__PURE__ */ new Date()) - this.startTime, r = Math.min(t, this.duration);
    this.durationProgress = r / this.duration;
    let { value: i, valueProgress: s } = this.calculate(r);
    this.value = Object.freeze(i), this.valueProgress = s, this._state !== "aborted" && (this._abort(this.value, this.valueProgress, this.durationProgress) ? (this._state = "aborted", this.unregister()) : t >= this.duration ? (this.durationProgress = this.valueProgress = 1, this._onChange(this.endValue, this.valueProgress, this.durationProgress), this._state = "completed", this._onComplete(this.endValue, this.valueProgress, this.durationProgress), this.unregister(), this.timeout = null) : (this._onChange(this.value, this.valueProgress, this.durationProgress), tr(this.tick)));
  }
  register() {
    Fr.push(this);
  }
  unregister() {
    Fr.remove(this);
  }
  abort() {
    this._state = "aborted", this.unregister(), this.timeout && ye().clearTimeout(this.timeout);
  }
}, gl = class extends ds {
  constructor({ startValue: e = 0, endValue: t = 100, ...r }) {
    super({
      ...r,
      startValue: e,
      byValue: t - e
    });
  }
  calculate(e) {
    let t = this.easing(e, this.startValue, this.byValue, this.duration);
    return {
      value: t,
      valueProgress: Math.abs((t - this.startValue) / this.byValue)
    };
  }
}, fl = class extends ds {
  constructor({ startValue: e = [0], endValue: t = [100], ...r }) {
    super({
      ...r,
      startValue: e,
      byValue: t.map((i, s) => i - e[s])
    });
  }
  calculate(e) {
    let t = this.startValue.map((r, i) => this.easing(e, r, this.byValue[i], this.duration, i));
    return {
      value: t,
      valueProgress: Math.abs((t[0] - this.startValue[0]) / this.byValue[0])
    };
  }
}, pl = (e, t, r, i) => t + r * (1 - Math.cos(e / i * Ut)), ni = (e) => e && ((t, r, i) => e(new K(t).toRgba(), r, i)), ml = class extends ds {
  constructor({ startValue: e, endValue: t, easing: r = pl, onChange: i, onComplete: s, abort: o, ...n }) {
    let a = new K(e).getSource(), l = new K(t).getSource();
    super({
      ...n,
      startValue: a,
      byValue: l.map((h, c) => h - a[c]),
      easing: r,
      onChange: ni(i),
      onComplete: ni(s),
      abort: ni(o)
    });
  }
  calculate(e) {
    let [t, r, i, s] = this.startValue.map((n, a) => this.easing(e, n, this.byValue[a], this.duration, a)), o = [...[
      t,
      r,
      i
    ].map(Math.round), oe(0, s, 1)];
    return {
      value: o,
      valueProgress: o.map((n, a) => this.byValue[a] === 0 ? 0 : Math.abs((n - this.startValue[a]) / this.byValue[a])).find((n) => n !== 0) || 0
    };
  }
};
function gs(e) {
  let t = ((r) => Array.isArray(r.startValue) || Array.isArray(r.endValue))(e) ? new fl(e) : new gl(e);
  return t.start(), t;
}
function Vo(e) {
  let t = new ml(e);
  return t.start(), t;
}
var rr = class z {
  constructor(t) {
    this.status = t, this.points = [];
  }
  includes(t) {
    return this.points.some((r) => r.eq(t));
  }
  append(...t) {
    return this.points = this.points.concat(t.filter((r) => !this.includes(r))), this;
  }
  static isPointContained(t, r, i, s = !1) {
    if (r.eq(i)) return t.eq(r);
    if (r.x === i.x) return t.x === r.x && (s || t.y >= Math.min(r.y, i.y) && t.y <= Math.max(r.y, i.y));
    if (r.y === i.y) return t.y === r.y && (s || t.x >= Math.min(r.x, i.x) && t.x <= Math.max(r.x, i.x));
    {
      let o = sr(r, i), n = sr(r, t).divide(o);
      return s ? Math.abs(n.x) === Math.abs(n.y) : n.x === n.y && n.x >= 0 && n.x <= 1;
    }
  }
  static isPointInPolygon(t, r) {
    let i = new v(t).setX(Math.min(t.x - 1, ...r.map((o) => o.x))), s = 0;
    for (let o = 0; o < r.length; o++) {
      let n = this.intersectSegmentSegment(r[o], r[(o + 1) % r.length], t, i);
      if (n.includes(t)) return !0;
      s += +(n.status === "Intersection");
    }
    return s % 2 == 1;
  }
  static intersectLineLine(t, r, i, s, o = !0, n = !0) {
    let a = r.x - t.x, l = r.y - t.y, h = s.x - i.x, c = s.y - i.y, u = t.x - i.x, d = t.y - i.y, g = h * d - c * u, p = a * d - l * u, m = c * a - h * l;
    if (m !== 0) {
      let x = g / m, _ = p / m;
      return (o || 0 <= x && x <= 1) && (n || 0 <= _ && _ <= 1) ? new z("Intersection").append(new v(t.x + x * a, t.y + x * l)) : new z();
    }
    return new z(g === 0 || p === 0 ? o || n || z.isPointContained(t, i, s) || z.isPointContained(r, i, s) || z.isPointContained(i, t, r) || z.isPointContained(s, t, r) ? "Coincident" : void 0 : "Parallel");
  }
  static intersectSegmentLine(t, r, i, s) {
    return z.intersectLineLine(t, r, i, s, !1, !0);
  }
  static intersectSegmentSegment(t, r, i, s) {
    return z.intersectLineLine(t, r, i, s, !1, !1);
  }
  static intersectLinePolygon(t, r, i, s = !0) {
    let o = new z(), n = i.length;
    for (let a, l, h, c = 0; c < n; c++) {
      if (a = i[c], l = i[(c + 1) % n], h = z.intersectLineLine(t, r, a, l, s, !1), h.status === "Coincident") return h;
      o.append(...h.points);
    }
    return o.points.length > 0 && (o.status = "Intersection"), o;
  }
  static intersectSegmentPolygon(t, r, i) {
    return z.intersectLinePolygon(t, r, i, !1);
  }
  static intersectPolygonPolygon(t, r) {
    let i = new z(), s = t.length, o = [];
    for (let n = 0; n < s; n++) {
      let a = t[n], l = t[(n + 1) % s], h = z.intersectSegmentPolygon(a, l, r);
      h.status === "Coincident" ? (o.push(h), i.append(a, l)) : i.append(...h.points);
    }
    return o.length > 0 && o.length === t.length ? new z("Coincident") : (i.points.length > 0 && (i.status = "Intersection"), i);
  }
  static intersectPolygonRectangle(t, r, i) {
    let s = r.min(i), o = r.max(i), n = new v(o.x, s.y), a = new v(s.x, o.y);
    return z.intersectPolygonPolygon(t, [
      s,
      n,
      o,
      a
    ]);
  }
}, vl = class extends fo {
  getX() {
    return this.getXY().x;
  }
  setX(e) {
    this.setXY(this.getXY().setX(e));
  }
  getY() {
    return this.getXY().y;
  }
  setY(e) {
    this.setXY(this.getXY().setY(e));
  }
  getRelativeX() {
    return this.left;
  }
  setRelativeX(e) {
    this.left = e;
  }
  getRelativeY() {
    return this.top;
  }
  setRelativeY(e) {
    this.top = e;
  }
  getXY() {
    let e = this.getRelativeXY();
    return this.group ? N(e, this.group.calcTransformMatrix()) : e;
  }
  setXY(e, t, r) {
    this.group && (e = N(e, lt(this.group.calcTransformMatrix()))), this.setRelativeXY(e, t, r);
  }
  getRelativeXY() {
    return new v(this.left, this.top);
  }
  setRelativeXY(e, t = this.originX, r = this.originY) {
    this.setPositionByOrigin(e, t, r);
  }
  isStrokeAccountedForInDimensions() {
    return !1;
  }
  getCoords() {
    let { tl: e, tr: t, br: r, bl: i } = this.aCoords || (this.aCoords = this.calcACoords()), s = [
      e,
      t,
      r,
      i
    ];
    if (this.group) {
      let o = this.group.calcTransformMatrix();
      return s.map((n) => N(n, o));
    }
    return s;
  }
  intersectsWithRect(e, t) {
    return rr.intersectPolygonRectangle(this.getCoords(), e, t).status === "Intersection";
  }
  intersectsWithObject(e) {
    let t = rr.intersectPolygonPolygon(this.getCoords(), e.getCoords());
    return t.status === "Intersection" || t.status === "Coincident" || e.isContainedWithinObject(this) || this.isContainedWithinObject(e);
  }
  isContainedWithinObject(e) {
    return this.getCoords().every((t) => e.containsPoint(t));
  }
  isContainedWithinRect(e, t) {
    let { left: r, top: i, width: s, height: o } = this.getBoundingRect();
    return r >= e.x && r + s <= t.x && i >= e.y && i + o <= t.y;
  }
  isOverlapping(e) {
    return this.intersectsWithObject(e) || this.isContainedWithinObject(e) || e.isContainedWithinObject(this);
  }
  containsPoint(e) {
    return rr.isPointInPolygon(e, this.getCoords());
  }
  isOnScreen() {
    if (!this.canvas) return !1;
    let { tl: e, br: t } = this.canvas.vptCoords;
    return !!this.getCoords().some((r) => r.x <= t.x && r.x >= e.x && r.y <= t.y && r.y >= e.y) || !!this.intersectsWithRect(e, t) || this.containsPoint(e.midPointFrom(t));
  }
  isPartiallyOnScreen() {
    if (!this.canvas) return !1;
    let { tl: e, br: t } = this.canvas.vptCoords;
    return !!this.intersectsWithRect(e, t) || this.getCoords().every((r) => (r.x >= t.x || r.x <= e.x) && (r.y >= t.y || r.y <= e.y)) && this.containsPoint(e.midPointFrom(t));
  }
  getBoundingRect() {
    return bt(this.getCoords());
  }
  getScaledWidth() {
    return this._getTransformedDimensions().x;
  }
  getScaledHeight() {
    return this._getTransformedDimensions().y;
  }
  scale(e) {
    this._set(Nt, e), this._set(qt, e), this.setCoords();
  }
  scaleToWidth(e) {
    let t = this.getBoundingRect().width / this.getScaledWidth();
    return this.scale(e / this.width / t);
  }
  scaleToHeight(e) {
    let t = this.getBoundingRect().height / this.getScaledHeight();
    return this.scale(e / this.height / t);
  }
  getCanvasRetinaScaling() {
    var e;
    return ((e = this.canvas) == null ? void 0 : e.getRetinaScaling()) || 1;
  }
  getTotalAngle() {
    return this.group ? Et(Ji(this.calcTransformMatrix())) : this.angle;
  }
  getViewportTransform() {
    var e;
    return ((e = this.canvas) == null ? void 0 : e.viewportTransform) || et.concat();
  }
  calcACoords() {
    let e = ne({ angle: this.angle }), { x: t, y: r } = this.getRelativeCenterPoint(), i = Y(ke(t, r), e), s = this._getTransformedDimensions(), o = s.x / 2, n = s.y / 2;
    return {
      tl: N({
        x: -o,
        y: -n
      }, i),
      tr: N({
        x: o,
        y: -n
      }, i),
      bl: N({
        x: -o,
        y: n
      }, i),
      br: N({
        x: o,
        y: n
      }, i)
    };
  }
  setCoords() {
    this.aCoords = this.calcACoords();
  }
  transformMatrixKey(e = !1) {
    let t = [];
    return !e && this.group && (t = this.group.transformMatrixKey(e)), t.push(this.top, this.left, this.width, this.height, this.scaleX, this.scaleY, this.angle, this.strokeWidth, this.skewX, this.skewY, +this.flipX, +this.flipY, Z(this.originX), Z(this.originY)), t;
  }
  calcTransformMatrix(e = !1) {
    let t = this.calcOwnMatrix();
    if (e || !this.group) return t;
    let r = this.transformMatrixKey(e), i = this.matrixCache;
    return i && i.key.every((s, o) => s === r[o]) ? i.value : (this.group && (t = Y(this.group.calcTransformMatrix(!1), t)), this.matrixCache = {
      key: r,
      value: t
    }, t);
  }
  calcOwnMatrix() {
    let e = this.transformMatrixKey(!0), t = this.ownMatrixCache;
    if (t && t.key.every((s, o) => s === e[o])) return t.value;
    let r = this.getRelativeCenterPoint(), i = _o({
      angle: this.angle,
      translateX: r.x,
      translateY: r.y,
      scaleX: this.scaleX,
      scaleY: this.scaleY,
      skewX: this.skewX,
      skewY: this.skewY,
      flipX: this.flipX,
      flipY: this.flipY
    });
    return this.ownMatrixCache = {
      key: e,
      value: i
    }, i;
  }
  _getNonTransformedDimensions() {
    return new v(this.width, this.height).scalarAdd(this.strokeWidth);
  }
  _calculateCurrentDimensions(e) {
    var t;
    let r = (t = this.canvas) == null ? void 0 : t.viewportTransform, i = this._getTransformedDimensions(e);
    return r ? i.multiply(new v(Qi(r), yo(r))).scalarAdd(2 * this.padding) : i.scalarAdd(2 * this.padding);
  }
  _getTransformedDimensions(e = {}) {
    let t = {
      scaleX: this.scaleX,
      scaleY: this.scaleY,
      skewX: this.skewX,
      skewY: this.skewY,
      width: this.width,
      height: this.height,
      strokeWidth: this.strokeWidth,
      ...e
    }, r = t.strokeWidth, i = r, s = 0;
    this.strokeUniform && (i = 0, s = r);
    let o = t.width + i, n = t.height + i, a;
    return a = t.skewX === 0 && t.skewY === 0 ? new v(o * t.scaleX, n * t.scaleY) : Ur(o, n, cr(t)), a.scalarAdd(s);
  }
  translateToGivenOrigin(e, t, r, i, s) {
    let o = e.x, n = e.y, a = Z(i) - Z(t), l = Z(s) - Z(r);
    if (a || l) {
      let h = this._getTransformedDimensions();
      o += a * h.x, n += l * h.y;
    }
    return new v(o, n);
  }
  translateToCenterPoint(e, t, r) {
    if (t === "center" && r === "center") return e;
    let i = this.translateToGivenOrigin(e, t, r, L, L);
    return this.angle ? i.rotate(I(this.angle), e) : i;
  }
  translateToOriginPoint(e, t, r) {
    let i = this.translateToGivenOrigin(e, L, L, t, r);
    return this.angle ? i.rotate(I(this.angle), e) : i;
  }
  getCenterPoint() {
    let e = this.getRelativeCenterPoint();
    return this.group ? N(e, this.group.calcTransformMatrix()) : e;
  }
  getRelativeCenterPoint() {
    return this.translateToCenterPoint(new v(this.left, this.top), this.originX, this.originY);
  }
  getPointByOrigin(e, t) {
    return this.getPositionByOrigin(e, t);
  }
  getPositionByOrigin(e, t) {
    return this.translateToOriginPoint(this.getRelativeCenterPoint(), e, t);
  }
  setPositionByOrigin(e, t, r) {
    let i = this.translateToCenterPoint(e, t, r), s = this.translateToOriginPoint(i, this.originX, this.originY);
    this.set({
      left: s.x,
      top: s.y
    });
  }
  _getLeftTopCoords() {
    return this.getPositionByOrigin(H, "top");
  }
  positionByLeftTop(e) {
    return this.setPositionByOrigin(e, H, "top");
  }
}, Ot = class Dr extends vl {
  static getDefaults() {
    return Dr.ownDefaults;
  }
  get type() {
    let t = this.constructor.type;
    return t === "FabricObject" ? "object" : t.toLowerCase();
  }
  set type(t) {
    zt("warn", "Setting type has no effect", t);
  }
  constructor(t) {
    super(), f(this, "_cacheContext", null), Object.assign(this, Dr.ownDefaults), this.setOptions(t);
  }
  _createCacheCanvas() {
    this._cacheCanvas = Tt(), this._cacheContext = this._cacheCanvas.getContext("2d"), this._updateCacheCanvas(), this.dirty = !0;
  }
  _limitCacheSize(t) {
    let r = t.width, i = t.height, s = P.maxCacheSideLimit, o = P.minCacheSideLimit;
    if (r <= s && i <= s && r * i <= P.perfLimitSizeTotal) return r < o && (t.width = o), i < o && (t.height = o), t;
    let n = r / i, [a, l] = Ze.limitDimsByArea(n), h = oe(o, a, s), c = oe(o, l, s);
    return r > h && (t.zoomX /= r / h, t.width = h, t.capped = !0), i > c && (t.zoomY /= i / c, t.height = c, t.capped = !0), t;
  }
  _getCacheCanvasDimensions() {
    let t = this.getTotalObjectScaling(), r = this._getTransformedDimensions({
      skewX: 0,
      skewY: 0
    }), i = r.x * t.x / this.scaleX, s = r.y * t.y / this.scaleY;
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
    let t = this._cacheCanvas, r = this._cacheContext, { width: i, height: s, zoomX: o, zoomY: n, x: a, y: l } = this._limitCacheSize(this._getCacheCanvasDimensions()), h = i !== t.width || s !== t.height, c = this.zoomX !== o || this.zoomY !== n;
    if (!t || !r) return !1;
    if (h || c) {
      i !== t.width || s !== t.height ? (t.width = i, t.height = s) : (r.setTransform(1, 0, 0, 1, 0, 0), r.clearRect(0, 0, t.width, t.height));
      let u = a / 2, d = l / 2;
      return this.cacheTranslationX = Math.round(t.width / 2 - u) + u, this.cacheTranslationY = Math.round(t.height / 2 - d) + d, r.translate(this.cacheTranslationX, this.cacheTranslationY), r.scale(o, n), this.zoomX = o, this.zoomY = n, !0;
    }
    return !1;
  }
  setOptions(t = {}) {
    this._setOptions(t);
  }
  transform(t) {
    let r = this.group && !this.group._transformDone || this.group && this.canvas && t === this.canvas.contextTop, i = this.calcTransformMatrix(!r);
    t.transform(i[0], i[1], i[2], i[3], i[4], i[5]);
  }
  getObjectScaling() {
    if (!this.group) return new v(Math.abs(this.scaleX), Math.abs(this.scaleY));
    let t = xe(this.calcTransformMatrix());
    return new v(Math.abs(t.scaleX), Math.abs(t.scaleY));
  }
  getTotalObjectScaling() {
    let t = this.getObjectScaling();
    if (this.canvas) {
      let r = this.canvas.getZoom(), i = this.getCanvasRetinaScaling();
      return t.scalarMultiply(r * i);
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
  _set(t, r) {
    t !== "scaleX" && t !== "scaleY" || (r = this._constrainScale(r)), t === "scaleX" && r < 0 ? (this.flipX = !this.flipX, r *= -1) : t === "scaleY" && r < 0 ? (this.flipY = !this.flipY, r *= -1) : t !== "shadow" || !r || r instanceof pe || (r = new pe(r));
    let i = this[t] !== r;
    return this[t] = r, i && this.constructor.cacheProperties.includes(t) && (this.dirty = !0), this.parent && (this.dirty || i && this.constructor.stateProperties.includes(t)) && this.parent._set("dirty", !0), this;
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
      let { zoomX: r, zoomY: i, cacheTranslationX: s, cacheTranslationY: o } = this, { width: n, height: a } = this._cacheCanvas;
      this.drawObject(this._cacheContext, t.forClipping, {
        zoomX: r,
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
  drawClipPathOnCache(t, r, i) {
    t.save(), r.inverted ? t.globalCompositeOperation = "destination-out" : t.globalCompositeOperation = "destination-in", t.setTransform(1, 0, 0, 1, 0, 0), t.drawImage(i, 0, 0), t.restore();
  }
  drawObject(t, r, i) {
    let s = this.fill, o = this.stroke;
    r ? (this.fill = "black", this.stroke = "", this._setClippingProperties(t)) : this._renderBackground(t), this.fire("before:render", { ctx: t }), this._render(t), this._drawClipPath(t, this.clipPath, i), this.fill = s, this.stroke = o;
  }
  createClipPathLayer(t, r) {
    let i = ht(r), s = i.getContext("2d");
    if (s.translate(r.cacheTranslationX, r.cacheTranslationY), s.scale(r.zoomX, r.zoomY), t._cacheCanvas = i, r.parentClipPaths.forEach((o) => {
      o.transform(s);
    }), r.parentClipPaths.push(t), t.absolutePositioned) {
      let o = lt(this.calcTransformMatrix());
      s.transform(o[0], o[1], o[2], o[3], o[4], o[5]);
    }
    return t.transform(s), t.drawObject(s, !0, r), i;
  }
  _drawClipPath(t, r, i) {
    if (!r) return;
    r._transformDone = !0;
    let s = this.createClipPathLayer(r, i);
    this.drawClipPathOnCache(t, r, s);
  }
  drawCacheOnCanvas(t) {
    t.scale(1 / this.zoomX, 1 / this.zoomY), t.drawImage(this._cacheCanvas, -this.cacheTranslationX, -this.cacheTranslationY);
  }
  isCacheDirty(t = !1) {
    if (this.isNotVisible()) return !1;
    let r = this._cacheCanvas, i = this._cacheContext;
    return !(!r || !i || t || !this._updateCacheCanvas()) || !!(this.dirty || this.clipPath && this.clipPath.absolutePositioned) && (r && i && !t && (i.save(), i.setTransform(1, 0, 0, 1, 0, 0), i.clearRect(0, 0, r.width, r.height), i.restore()), !0);
  }
  _renderBackground(t) {
    if (!this.backgroundColor) return;
    let r = this._getNonTransformedDimensions();
    t.fillStyle = this.backgroundColor, t.fillRect(-r.x / 2, -r.y / 2, r.x, r.y), this._removeShadow(t);
  }
  _setOpacity(t) {
    this.group && !this.group._transformDone ? t.globalAlpha = this.getObjectOpacity() : t.globalAlpha *= this.opacity;
  }
  _setStrokeStyles(t, r) {
    let i = r.stroke;
    i && (t.lineWidth = r.strokeWidth, t.lineCap = r.strokeLineCap, t.lineDashOffset = r.strokeDashOffset, t.lineJoin = r.strokeLineJoin, t.miterLimit = r.strokeMiterLimit, ut(i) ? i.gradientUnits === "percentage" || i.gradientTransform || i.patternTransform ? this._applyPatternForTransformedGradient(t, i) : (t.strokeStyle = i.toLive(t), this._applyPatternGradientTransform(t, i)) : t.strokeStyle = r.stroke);
  }
  _setFillStyles(t, { fill: r }) {
    r && (ut(r) ? (t.fillStyle = r.toLive(t), this._applyPatternGradientTransform(t, r)) : t.fillStyle = r);
  }
  _setClippingProperties(t) {
    t.globalAlpha = 1, t.strokeStyle = "transparent", t.fillStyle = "#000000";
  }
  _setLineDash(t, r) {
    r && r.length !== 0 && t.setLineDash(r);
  }
  _setShadow(t) {
    if (!this.shadow) return;
    let r = this.shadow, i = this.canvas, s = this.getCanvasRetinaScaling(), [o, , , n] = i?.viewportTransform || et, a = o * s, l = n * s, h = r.nonScaling ? new v(1, 1) : this.getObjectScaling();
    t.shadowColor = r.color, t.shadowBlur = r.blur * P.browserShadowBlurConstant * (a + l) * (h.x + h.y) / 4, t.shadowOffsetX = r.offsetX * a * h.x, t.shadowOffsetY = r.offsetY * l * h.y;
  }
  _removeShadow(t) {
    this.shadow && (t.shadowColor = "", t.shadowBlur = t.shadowOffsetX = t.shadowOffsetY = 0);
  }
  _applyPatternGradientTransform(t, r) {
    if (!ut(r)) return {
      offsetX: 0,
      offsetY: 0
    };
    let i = r.gradientTransform || r.patternTransform, s = -this.width / 2 + r.offsetX || 0, o = -this.height / 2 + r.offsetY || 0;
    return r.gradientUnits === "percentage" ? t.transform(this.width, 0, 0, this.height, s, o) : t.transform(1, 0, 0, 1, s, o), i && t.transform(i[0], i[1], i[2], i[3], i[4], i[5]), {
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
        let r = this.getObjectScaling();
        t.scale(1 / r.x, 1 / r.y);
      }
      this._setLineDash(t, this.strokeDashArray), this._setStrokeStyles(t, this), t.stroke(), t.restore();
    }
  }
  _applyPatternForTransformedGradient(t, r) {
    var i;
    let s = this._limitCacheSize(this._getCacheCanvasDimensions()), o = this.getCanvasRetinaScaling(), n = s.x / this.scaleX / o, a = s.y / this.scaleY / o, l = ht({
      width: Math.ceil(n),
      height: Math.ceil(a)
    }), h = l.getContext("2d");
    h && (h.beginPath(), h.moveTo(0, 0), h.lineTo(n, 0), h.lineTo(n, a), h.lineTo(0, a), h.closePath(), h.translate(n / 2, a / 2), h.scale(s.zoomX / this.scaleX / o, s.zoomY / this.scaleY / o), this._applyPatternGradientTransform(h, r), h.fillStyle = r.toLive(t), h.fill(), t.translate(-this.width / 2 - this.strokeWidth / 2, -this.height / 2 - this.strokeWidth / 2), t.scale(o * this.scaleX / s.zoomX, o * this.scaleY / s.zoomY), t.strokeStyle = (i = h.createPattern(l, "no-repeat")) == null ? "" : i);
  }
  _findCenterFromElement() {
    return new v(this.left + this.width / 2, this.top + this.height / 2);
  }
  clone(t) {
    let r = this.toObject(t);
    return this.constructor.fromObject(r);
  }
  cloneAsImage(t) {
    let r = this.toCanvasElement(t);
    return new (w.getClass("image"))(r);
  }
  toCanvasElement(t = {}) {
    let r = rs(this), i = this.group, s = this.shadow, o = Math.abs, n = t.enableRetinaScaling ? io() : 1, a = (t.multiplier || 1) * n, l = t.canvasProvider || ((y) => new Gr(y, {
      enableRetinaScaling: !1,
      renderOnAddRemove: !1,
      skipOffscreen: !1
    }));
    delete this.group, t.withoutTransform && Mo(this), t.withoutShadow && (this.shadow = null), t.viewportTransform && is(this, this.getViewportTransform()), this.setCoords();
    let h = Tt(), c = this.getBoundingRect(), u = this.shadow, d = new v();
    if (u) {
      let y = u.blur, S = u.nonScaling ? new v(1, 1) : this.getObjectScaling();
      d.x = 2 * Math.round(o(u.offsetX) + y) * o(S.x), d.y = 2 * Math.round(o(u.offsetY) + y) * o(S.y);
    }
    let g = c.width + d.x, p = c.height + d.y;
    h.width = Math.ceil(g), h.height = Math.ceil(p);
    let m = l(h);
    t.format === "jpeg" && (m.backgroundColor = "#fff"), this.setPositionByOrigin(new v(m.width / 2, m.height / 2), L, L);
    let x = this.canvas;
    m._objects = [this], this.set("canvas", m), this.setCoords();
    let _ = m.toCanvasElement(a || 1, t);
    return this.set("canvas", x), this.shadow = s, i && (this.group = i), this.set(r), this.setCoords(), m._objects = [], m.destroy(), _;
  }
  toDataURL(t = {}) {
    return qi(this.toCanvasElement(t), t.format || "png", t.quality || 1);
  }
  toBlob(t = {}) {
    return Ki(this.toCanvasElement(t), t.format || "png", t.quality || 1);
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
    let { centeredRotation: r, originX: i, originY: s } = this;
    if (r) {
      let { x: o, y: n } = this.getRelativeCenterPoint();
      this.originX = L, this.originY = L, this.left = o, this.top = n;
    }
    if (this.set("angle", t), r) {
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
    Fr.cancelByTarget(this), this.off(), this._set("canvas", void 0), this._cacheCanvas && wt().dispose(this._cacheCanvas), this._cacheCanvas = void 0, this._cacheContext = null;
  }
  animate(t, r) {
    return Object.entries(t).reduce((i, [s, o]) => (i[s] = this._animate(s, o, r), i), {});
  }
  _animate(t, r, i = {}) {
    let s = t.split("."), o = this.constructor.colorProperties.includes(s[s.length - 1]), { abort: n, startValue: a, onChange: l, onComplete: h } = i, c = {
      ...i,
      target: this,
      startValue: a ?? s.reduce((u, d) => u[d], this),
      endValue: r,
      abort: n?.bind(this),
      onChange: (u, d, g) => {
        s.reduce((p, m, x) => (x === s.length - 1 && (p[m] = u), p[m]), this), l && l(u, d, g);
      },
      onComplete: (u, d, g) => {
        this.setCoords(), h && h(u, d, g);
      }
    };
    return o ? Vo(c) : gs(c);
  }
  isDescendantOf(t) {
    let { parent: r, group: i } = this;
    return r === t || i === t || !!r && r.isDescendantOf(t) || !!i && i !== r && i.isDescendantOf(t);
  }
  getAncestors() {
    let t = [], r = this;
    do
      r = r.parent, r && t.push(r);
    while (r);
    return t;
  }
  findCommonAncestors(t) {
    if (this === t) return {
      fork: [],
      otherFork: [],
      common: [this, ...this.getAncestors()]
    };
    let r = this.getAncestors(), i = t.getAncestors();
    if (r.length === 0 && i.length > 0 && this === i[i.length - 1]) return {
      fork: [],
      otherFork: [t, ...i.slice(0, i.length - 1)],
      common: [this]
    };
    for (let s, o = 0; o < r.length; o++) {
      if (s = r[o], s === t) return {
        fork: [this, ...r.slice(0, o)],
        otherFork: [],
        common: r.slice(o)
      };
      for (let n = 0; n < i.length; n++) {
        if (this === i[n]) return {
          fork: [],
          otherFork: [t, ...i.slice(0, n)],
          common: [this, ...r]
        };
        if (s === i[n]) return {
          fork: [this, ...r.slice(0, o)],
          otherFork: [t, ...i.slice(0, n)],
          common: r.slice(o)
        };
      }
    }
    return {
      fork: [this, ...r],
      otherFork: [t, ...i],
      common: []
    };
  }
  hasCommonAncestors(t) {
    let r = this.findCommonAncestors(t);
    return r && !!r.common.length;
  }
  isInFrontOf(t) {
    if (this === t) return;
    let r = this.findCommonAncestors(t);
    if (r.fork.includes(t)) return !0;
    if (r.otherFork.includes(this)) return !1;
    let i = r.common[0] || this.canvas;
    if (!i) return;
    let s = r.fork.pop(), o = r.otherFork.pop(), n = i._objects.indexOf(s), a = i._objects.indexOf(o);
    return n > -1 && n > a;
  }
  toObject(t = []) {
    let r = t.concat(Dr.customProperties, this.constructor.customProperties || []), i, s = P.NUM_FRACTION_DIGITS, { clipPath: o, fill: n, stroke: a, shadow: l, strokeDashArray: h, left: c, top: u, originX: d, originY: g, width: p, height: m, strokeWidth: x, strokeLineCap: _, strokeDashOffset: y, strokeLineJoin: S, strokeUniform: C, strokeMiterLimit: b, scaleX: O, scaleY: T, angle: k, flipX: D, flipY: B, opacity: A, visible: E, backgroundColor: R, fillRule: X, paintFirst: G, globalCompositeOperation: $, skewX: J, skewY: ot } = this;
    o && !o.excludeFromExport && (i = o.toObject(r.concat("inverted", "absolutePositioned")));
    let j = (Me) => F(Me, s), _t = {
      ...ae(this, r),
      type: this.constructor.type,
      version: mi,
      originX: d,
      originY: g,
      left: j(c),
      top: j(u),
      width: j(p),
      height: j(m),
      fill: Os(n) ? n.toObject() : n,
      stroke: Os(a) ? a.toObject() : a,
      strokeWidth: j(x),
      strokeDashArray: h && h.concat(),
      strokeLineCap: _,
      strokeDashOffset: y,
      strokeLineJoin: S,
      strokeUniform: C,
      strokeMiterLimit: j(b),
      scaleX: j(O),
      scaleY: j(T),
      angle: j(k),
      flipX: D,
      flipY: B,
      opacity: j(A),
      shadow: l && l.toObject(),
      visible: E,
      backgroundColor: R,
      fillRule: X,
      paintFirst: G,
      globalCompositeOperation: $,
      skewX: j(J),
      skewY: j(ot),
      ...i ? { clipPath: i } : null
    };
    return this.includeDefaultValues ? _t : this._removeDefaultValues(_t);
  }
  toDatalessObject(t) {
    return this.toObject(t);
  }
  _removeDefaultValues(t) {
    let r = this.constructor.getDefaults(), i = Object.keys(r).length > 0 ? r : Object.getPrototypeOf(this);
    return es(t, (s, o) => {
      if (o === "left" || o === "top" || o === "type") return !0;
      let n = i[o];
      return s !== n && !(Array.isArray(s) && Array.isArray(n) && s.length === 0 && n.length === 0);
    });
  }
  toString() {
    return `#<${this.constructor.type}>`;
  }
  static _fromObject({ type: t, ...r }, { extraParam: i, ...s } = {}) {
    return ur(r, s).then((o) => i ? (delete o[i], new this(r[i], o)) : new this(o));
  }
  static fromObject(t, r) {
    return this._fromObject(t, r);
  }
};
f(Ot, "stateProperties", La), f(Ot, "cacheProperties", At), f(Ot, "ownDefaults", Ra), f(Ot, "type", "FabricObject"), f(Ot, "colorProperties", [
  st,
  Dt,
  "backgroundColor"
]), f(Ot, "customProperties", []), w.setClass(Ot), w.setClass(Ot, "object");
var fs = (e, t) => {
  var r;
  let { transform: { target: i } } = t;
  (r = i.canvas) == null || r.fire(`object:${e}`, {
    ...t,
    target: i
  }), i.fire(e, t);
}, jt = (e, t, r) => (i, s, o, n) => {
  let a = t(i, s, o, n);
  return a && fs(e, {
    ...ls(i, s, o, n),
    ...r
  }), a;
};
function Kt(e) {
  return (t, r, i, s) => {
    let { target: o, originX: n, originY: a } = r, l = o.getPositionByOrigin(n, a), h = e(t, r, i, s);
    return o.setPositionByOrigin(l, r.originX, r.originY), h;
  };
}
var Ho = (e, t, r, i) => (s, o, n, a) => {
  let l = qr(o, o.originX, o.originY, n, a)[r], h = Z(o[t]);
  if (h === 0 || h > 0 && l < 0 || h < 0 && l > 0) {
    let { target: c } = o, u = c.strokeWidth / (c.strokeUniform ? c[i] : 1), d = Ao(o) ? 2 : 1, g = c[e], p = Math.abs(l * d / c[i]) - u;
    return c.set(e, Math.max(p, 1)), g !== c[e];
  }
  return !1;
}, zo = Ho("width", "originX", "x", "scaleX"), Go = Ho("height", "originY", "y", "scaleY"), xi = jt(ir, Kt(zo)), yl = jt(ir, Kt(Go));
function Uo(e, t, r, i, s) {
  e.save();
  let { stroke: o, xSize: n, ySize: a, opName: l } = this.commonRenderProps(e, t, r, s, i), h = n;
  n > a ? e.scale(1, a / n) : a > n && (h = a, e.scale(n / a, 1)), e.beginPath(), e.arc(0, 0, h / 2, 0, vt, !1), e[l](), o && e.stroke(), e.restore();
}
function No(e, t, r, i, s) {
  e.save();
  let { stroke: o, xSize: n, ySize: a, opName: l } = this.commonRenderProps(e, t, r, s, i), h = n / 2, c = a / 2;
  e[`${l}Rect`](-h, -c, n, a), o && e.strokeRect(-h, -c, n, a), e.restore();
}
var V = class {
  constructor(e) {
    f(this, "visible", !0), f(this, "actionName", co), f(this, "angle", 0), f(this, "x", 0), f(this, "y", 0), f(this, "offsetX", 0), f(this, "offsetY", 0), f(this, "sizeX", 0), f(this, "sizeY", 0), f(this, "touchSizeX", 0), f(this, "touchSizeY", 0), f(this, "cursorStyle", "crosshair"), f(this, "withConnection", !1), Object.assign(this, e);
  }
  getTransformAnchorPoint() {
    var e;
    return (e = this.transformAnchorPoint) == null ? new v(0.5 - this.x, 0.5 - this.y) : e;
  }
  shouldActivate(e, t, r, { tl: i, tr: s, br: o, bl: n }) {
    var a;
    return ((a = t.canvas) == null ? void 0 : a.getActiveObject()) === t && t.isControlVisible(e) && rr.isPointInPolygon(r, [
      i,
      s,
      o,
      n
    ]);
  }
  getActionHandler(e, t, r) {
    return this.actionHandler;
  }
  getMouseDownHandler(e, t, r) {
    return this.mouseDownHandler;
  }
  getMouseUpHandler(e, t, r) {
    return this.mouseUpHandler;
  }
  cursorStyleHandler(e, t, r, i) {
    return t.cursorStyle;
  }
  getActionName(e, t, r) {
    return t.actionName;
  }
  getVisibility(e, t) {
    var r, i;
    return (r = (i = e._controlsVisibility) == null ? void 0 : i[t]) == null ? this.visible : r;
  }
  setVisibility(e, t, r) {
    this.visible = e;
  }
  positionHandler(e, t, r, i) {
    return new v(this.x * e.x + this.offsetX, this.y * e.y + this.offsetY).transform(t);
  }
  calcCornerCoords(e, t, r, i, s, o) {
    let n = Vr([
      ke(r, i),
      ne({ angle: e }),
      Hr((s ? this.touchSizeX : this.sizeX) || t, (s ? this.touchSizeY : this.sizeY) || t)
    ]);
    return {
      tl: new v(-0.5, -0.5).transform(n),
      tr: new v(0.5, -0.5).transform(n),
      br: new v(0.5, 0.5).transform(n),
      bl: new v(-0.5, 0.5).transform(n)
    };
  }
  commonRenderProps(e, t, r, i, s = {}) {
    let { cornerSize: o, cornerColor: n, transparentCorners: a, cornerStrokeColor: l } = s, h = o || i.cornerSize, c = this.sizeX || h, u = this.sizeY || h, d = a === void 0 ? i.transparentCorners : a, g = d ? Dt : st, p = l || i.cornerStrokeColor, m = !d && !!p;
    return e.fillStyle = n || i.cornerColor || "", e.strokeStyle = p || "", e.translate(t, r), e.rotate(I(i.getTotalAngle())), {
      stroke: m,
      xSize: c,
      ySize: u,
      transparentCorners: d,
      opName: g
    };
  }
  render(e, t, r, i, s) {
    ((i = i || {}).cornerStyle || s.cornerStyle) === "circle" ? Uo.call(this, e, t, r, i, s) : No.call(this, e, t, r, i, s);
  }
}, qo = (e, t, r) => r.lockRotation ? as : t.cursorStyle, Ko = jt(no, Kt((e, { target: t, ex: r, ey: i, theta: s, originX: o, originY: n }, a, l) => {
  let h = t.getPositionByOrigin(o, n);
  if (mt(t, "lockRotation")) return !1;
  let c = Math.atan2(i - h.y, r - h.x), u = Et(Math.atan2(l - h.y, a - h.x) - c + s);
  if (t.snapAngle && t.snapAngle > 0) {
    let g = t.snapAngle, p = t.snapThreshold || g, m = Math.ceil(u / g) * g, x = Math.floor(u / g) * g;
    Math.abs(u - x) < p ? u = x : Math.abs(u - m) < p && (u = m);
  }
  u < 0 && (u = 360 + u), u %= 360;
  let d = t.angle !== u;
  return t.angle = u, d;
}));
function Jo(e, t) {
  let r = t.canvas, i = e[r.uniScaleKey];
  return r.uniformScaling && !i || !r.uniformScaling && i;
}
function Qo(e, t, r) {
  let i = mt(e, "lockScalingX"), s = mt(e, "lockScalingY");
  if (i && s || !t && (i || s) && r || i && t === "x" || s && t === "y") return !0;
  let { width: o, height: n, strokeWidth: a } = e;
  return o === 0 && a === 0 && t !== "y" || n === 0 && a === 0 && t !== "x";
}
var xl = [
  "e",
  "se",
  "s",
  "sw",
  "w",
  "nw",
  "n",
  "ne",
  "e"
], de = (e, t, r, i) => {
  let s = Jo(e, r);
  return Qo(r, t.x !== 0 && t.y === 0 ? "x" : t.x === 0 && t.y !== 0 ? "y" : "", s) ? as : `${xl[jo(r, 0, i)]}-resize`;
};
function ps(e, t, r, i, s = {}) {
  let o = t.target, n = s.by, a = Jo(e, o), l, h, c, u, d, g;
  if (Qo(o, n, a)) return !1;
  if (t.gestureScale) h = t.scaleX * t.gestureScale, c = t.scaleY * t.gestureScale;
  else {
    if (l = qr(t, t.originX, t.originY, r, i), d = n === "y" ? 1 : Math.sign(l.x || t.signX || 1), g = n === "x" ? 1 : Math.sign(l.y || t.signY || 1), t.signX || (t.signX = d), t.signY || (t.signY = g), mt(o, "lockScalingFlip") && (t.signX !== d || t.signY !== g)) return !1;
    if (u = o._getTransformedDimensions(), a && !n) {
      let x = Math.abs(l.x) + Math.abs(l.y), { original: _ } = t, y = x / (Math.abs(u.x * _.scaleX / o.scaleX) + Math.abs(u.y * _.scaleY / o.scaleY));
      h = _.scaleX * y, c = _.scaleY * y;
    } else h = Math.abs(l.x * o.scaleX / u.x), c = Math.abs(l.y * o.scaleY / u.y);
    Ao(t) && (h *= 2, c *= 2), t.signX !== d && n !== "y" && (t.originX = Es(t.originX), h *= -1, t.signX = d), t.signY !== g && n !== "x" && (t.originY = Es(t.originY), c *= -1, t.signY = g);
  }
  let p = o.scaleX, m = o.scaleY;
  return n ? (n === "x" && o.set("scaleX", h), n === "y" && o.set("scaleY", c)) : (!mt(o, "lockScalingX") && o.set("scaleX", h), !mt(o, "lockScalingY") && o.set("scaleY", c)), p !== o.scaleX || m !== o.scaleY;
}
var Fe = jt(Wr, Kt((e, t, r, i) => ps(e, t, r, i))), Zo = jt(Wr, Kt((e, t, r, i) => ps(e, t, r, i, { by: "x" }))), tn = jt(Wr, Kt((e, t, r, i) => ps(e, t, r, i, { by: "y" }))), ai = {
  x: {
    counterAxis: "y",
    scale: Nt,
    skew: Te,
    lockSkewing: "lockSkewingX",
    origin: "originX",
    flip: "flipX"
  },
  y: {
    counterAxis: "x",
    scale: qt,
    skew: Oe,
    lockSkewing: "lockSkewingY",
    origin: "originY",
    flip: "flipY"
  }
}, _l = [
  "ns",
  "nesw",
  "ew",
  "nwse"
], en = (e, t, r, i) => t.x !== 0 && mt(r, "lockSkewingY") || t.y !== 0 && mt(r, "lockSkewingX") ? as : `${_l[jo(r, 0, i) % 4]}-resize`;
function rn(e, t, r, i, s) {
  let { target: o } = r, { counterAxis: n, origin: a, lockSkewing: l, skew: h, flip: c } = ai[e];
  if (mt(o, l)) return !1;
  let { origin: u, flip: d } = ai[n], g = Z(r[u]) * (o[d] ? -1 : 1), p = -Math.sign(g) * (o[c] ? -1 : 1), m = -(o[h] === 0 && qr(r, "center", "center", i, s)[e] > 0 || o[h] > 0 ? 1 : -1) * p * 0.5 + 0.5;
  return jt(lo, Kt((x, _, y, S) => (function(C, { target: b, ex: O, ey: T, skewingSide: k, ...D }, B) {
    let { skew: A } = ai[C], E = B.subtract(new v(O, T)).divide(new v(b.scaleX, b.scaleY))[C], R = b[A], X = D[A], G = Math.tan(I(X)), $ = C === "y" ? b._getTransformedDimensions({
      scaleX: 1,
      scaleY: 1,
      skewX: 0
    }).x : b._getTransformedDimensions({
      scaleX: 1,
      scaleY: 1
    }).y, J = 2 * E * k / Math.max($, 1) + G, ot = Et(Math.atan(J));
    b.set(A, ot);
    let j = R !== b[A];
    if (j && C === "y") {
      let { skewX: _t, scaleX: Me } = b, De = b._getTransformedDimensions({ skewY: R }), Rt = b._getTransformedDimensions(), Ee = _t === 0 ? 1 : De.x / Rt.x;
      Ee !== 1 && b.set("scaleX", Ee * Me);
    }
    return j;
  })(e, _, new v(y, S))))(t, {
    ...r,
    [a]: m,
    skewingSide: p
  }, i, s);
}
var sn = (e, t, r, i) => rn("x", e, t, r, i), on = (e, t, r, i) => rn("y", e, t, r, i);
function Zr(e, t) {
  return e[t.canvas.altActionKey];
}
var Le = (e, t, r) => {
  let i = Zr(e, r);
  return t.x === 0 ? i ? Te : qt : t.y === 0 ? i ? Oe : Nt : "";
}, re = (e, t, r, i) => Zr(e, r) ? en(0, t, r, i) : de(e, t, r, i), _i = (e, t, r, i) => Zr(e, t.target) ? on(e, t, r, i) : Zo(e, t, r, i), Si = (e, t, r, i) => Zr(e, t.target) ? sn(e, t, r, i) : tn(e, t, r, i), ms = () => ({
  ml: new V({
    x: -0.5,
    y: 0,
    cursorStyleHandler: re,
    actionHandler: _i,
    getActionName: Le
  }),
  mr: new V({
    x: 0.5,
    y: 0,
    cursorStyleHandler: re,
    actionHandler: _i,
    getActionName: Le
  }),
  mb: new V({
    x: 0,
    y: 0.5,
    cursorStyleHandler: re,
    actionHandler: Si,
    getActionName: Le
  }),
  mt: new V({
    x: 0,
    y: -0.5,
    cursorStyleHandler: re,
    actionHandler: Si,
    getActionName: Le
  }),
  tl: new V({
    x: -0.5,
    y: -0.5,
    cursorStyleHandler: de,
    actionHandler: Fe
  }),
  tr: new V({
    x: 0.5,
    y: -0.5,
    cursorStyleHandler: de,
    actionHandler: Fe
  }),
  bl: new V({
    x: -0.5,
    y: 0.5,
    cursorStyleHandler: de,
    actionHandler: Fe
  }),
  br: new V({
    x: 0.5,
    y: 0.5,
    cursorStyleHandler: de,
    actionHandler: Fe
  }),
  mtr: new V({
    x: 0,
    y: -0.5,
    actionHandler: Ko,
    cursorStyleHandler: qo,
    offsetY: -40,
    withConnection: !0,
    actionName: ao
  })
}), nn = () => ({
  mr: new V({
    x: 0.5,
    y: 0,
    actionHandler: xi,
    cursorStyleHandler: re,
    actionName: ir
  }),
  ml: new V({
    x: -0.5,
    y: 0,
    actionHandler: xi,
    cursorStyleHandler: re,
    actionName: ir
  })
}), an = () => ({
  ...ms(),
  ...nn()
}), ln = class Ci extends Ot {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Ci.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, this.constructor.createControls(), Ci.ownDefaults), this.setOptions(t);
  }
  static createControls() {
    return { controls: ms() };
  }
  _updateCacheCanvas() {
    let t = this.canvas;
    if (this.noScaleCache && t && t._currentTransform) {
      let r = t._currentTransform, i = r.target, s = r.action;
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
  findControl(t, r = !1) {
    if (!this.hasControls || !this.canvas) return;
    this.__corner = void 0;
    let i = Object.entries(this.oCoords);
    for (let s = i.length - 1; s >= 0; s--) {
      let [o, n] = i[s], a = this.controls[o];
      if (a.shouldActivate(o, this, t, r ? n.touchCorner : n.corner)) return this.__corner = o, {
        key: o,
        control: a,
        coord: this.oCoords[o]
      };
    }
  }
  calcOCoords() {
    let t = this.getViewportTransform(), r = Qi(t), i = yo(t), s = this.getCenterPoint(), o = Y(Y(t, Y(ke(s.x, s.y), ne({ angle: this.getTotalAngle() - (this.group && this.flipX ? 180 : 0) }))), [
      1 / r,
      0,
      0,
      1 / i,
      0,
      0
    ]), n = this.group ? xe(this.calcTransformMatrix()) : void 0;
    n && (n.scaleX = Math.abs(n.scaleX), n.scaleY = Math.abs(n.scaleY));
    let a = this._calculateCurrentDimensions(n), l = {};
    return this.forEachControl((h, c) => {
      let u = h.positionHandler(a, o, this, h);
      l[c] = Object.assign(u, this._calcCornerCoords(h, u));
    }), l;
  }
  _calcCornerCoords(t, r) {
    let i = this.getTotalAngle();
    return {
      corner: t.calcCornerCoords(i, this.cornerSize, r.x, r.y, !1, this),
      touchCorner: t.calcCornerCoords(i, this.touchCornerSize, r.x, r.y, !0, this)
    };
  }
  setCoords() {
    super.setCoords(), this.canvas && (this.oCoords = this.calcOCoords());
  }
  forEachControl(t) {
    for (let r in this.controls) t(this.controls[r], r, this);
  }
  drawSelectionBackground(t) {
    if (!this.selectionBackgroundColor || this.canvas && this.canvas._activeObject !== this) return;
    t.save();
    let r = this.getRelativeCenterPoint(), i = this._calculateCurrentDimensions(), s = this.getViewportTransform();
    t.translate(r.x, r.y), t.scale(1 / s[0], 1 / s[3]), t.rotate(I(this.angle)), t.fillStyle = this.selectionBackgroundColor, t.fillRect(-i.x / 2, -i.y / 2, i.x, i.y), t.restore();
  }
  strokeBorders(t, r) {
    t.strokeRect(-r.x / 2, -r.y / 2, r.x, r.y);
  }
  _drawBorders(t, r, i = {}) {
    let s = {
      hasControls: this.hasControls,
      borderColor: this.borderColor,
      borderDashArray: this.borderDashArray,
      ...i
    };
    t.save(), t.strokeStyle = s.borderColor, this._setLineDash(t, s.borderDashArray), this.strokeBorders(t, r), s.hasControls && this.drawControlsConnectingLines(t, r), t.restore();
  }
  _renderControls(t, r = {}) {
    let { hasBorders: i, hasControls: s } = this, o = {
      hasBorders: i,
      hasControls: s,
      ...r
    }, n = this.getViewportTransform(), a = o.hasBorders, l = o.hasControls, h = xe(Y(n, this.calcTransformMatrix()));
    t.save(), t.translate(h.translateX, h.translateY), t.lineWidth = this.borderScaleFactor, this.group === this.parent && (t.globalAlpha = this.isMoving ? this.borderOpacityWhenMoving : 1), this.flipX && (h.angle -= 180);
    let c = Ji(n);
    t.rotate(this.group ? I(h.angle) : I(this.angle) + c), a && this.drawBorders(t, h, r), l && this.drawControls(t, r), t.restore();
  }
  drawBorders(t, r, i) {
    let s;
    if (i && i.forActiveSelection || this.group) {
      let o = Ur(this.width, this.height, cr(r)), n = this.isStrokeAccountedForInDimensions() ? Ni : (this.strokeUniform ? new v().scalarAdd(this.canvas ? this.canvas.getZoom() : 1) : new v(r.scaleX, r.scaleY)).scalarMultiply(this.strokeWidth);
      s = o.add(n).scalarAdd(this.borderScaleFactor).scalarAdd(2 * this.padding);
    } else s = this._calculateCurrentDimensions().scalarAdd(this.borderScaleFactor);
    this._drawBorders(t, s, i);
  }
  drawControlsConnectingLines(t, r) {
    let i = !1;
    t.beginPath(), this.forEachControl((s, o) => {
      s.withConnection && s.getVisibility(this, o) && (i = !0, t.moveTo(s.x * r.x, s.y * r.y), t.lineTo(s.x * r.x + s.offsetX, s.y * r.y + s.offsetY));
    }), i && t.stroke();
  }
  drawControls(t, r = {}) {
    t.save();
    let i = this.getCanvasRetinaScaling(), { cornerStrokeColor: s, cornerDashArray: o, cornerColor: n } = this, a = {
      cornerStrokeColor: s,
      cornerDashArray: o,
      cornerColor: n,
      ...r
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
  setControlVisible(t, r) {
    this._controlsVisibility || (this._controlsVisibility = {}), this._controlsVisibility[t] = r;
  }
  setControlsVisibility(t = {}) {
    Object.entries(t).forEach(([r, i]) => this.setControlVisible(r, i));
  }
  clearContextTop(t) {
    if (!this.canvas) return;
    let r = this.canvas.contextTop;
    if (!r) return;
    let i = this.canvas.viewportTransform;
    r.save(), r.transform(i[0], i[1], i[2], i[3], i[4], i[5]), this.transform(r);
    let s = this.width + 4, o = this.height + 4;
    return r.clearRect(-s / 2, -o / 2, s, o), t || r.restore(), r;
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
function hn(e, t) {
  return t.forEach((r) => {
    Object.getOwnPropertyNames(r.prototype).forEach((i) => {
      i !== "constructor" && Object.defineProperty(e.prototype, i, Object.getOwnPropertyDescriptor(r.prototype, i) || /* @__PURE__ */ Object.create(null));
    });
  }), e;
}
f(ln, "ownDefaults", {
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
var q = class extends ln {
};
hn(q, [Lo]), w.setClass(q), w.setClass(q, "object");
var cn = (e, t, r, i) => {
  let s = 2 * (i = Math.round(i)) + 1, { data: o } = e.getImageData(t - i, r - i, s, s);
  for (let n = 3; n < o.length; n += 4) if (o[n] > 0) return !1;
  return !0;
}, un = class {
  constructor(e) {
    this.options = e, this.strokeProjectionMagnitude = this.options.strokeWidth / 2, this.scale = new v(this.options.scaleX, this.options.scaleY), this.strokeUniformScalar = this.options.strokeUniform ? new v(1 / this.options.scaleX, 1 / this.options.scaleY) : new v(1, 1);
  }
  createSideVector(e, t) {
    let r = sr(e, t);
    return this.options.strokeUniform ? r.multiply(this.scale) : r;
  }
  projectOrthogonally(e, t, r) {
    return this.applySkew(e.add(this.calcOrthogonalProjection(e, t, r)));
  }
  isSkewed() {
    return this.options.skewX !== 0 || this.options.skewY !== 0;
  }
  applySkew(e) {
    let t = new v(e);
    return t.y += t.x * Math.tan(I(this.options.skewY)), t.x += t.y * Math.tan(I(this.options.skewX)), t;
  }
  scaleUnitVector(e, t) {
    return e.multiply(this.strokeUniformScalar).scalarMultiply(t);
  }
}, Sl = new v(), dn = class Er extends un {
  static getOrthogonalRotationFactor(t, r) {
    let i = r ? Br(t, r) : os(t);
    return Math.abs(i) < Ut ? -1 : 1;
  }
  constructor(t, r, i, s) {
    super(s), f(this, "AB", void 0), f(this, "AC", void 0), f(this, "alpha", void 0), f(this, "bisector", void 0), this.A = new v(t), this.B = new v(r), this.C = new v(i), this.AB = this.createSideVector(this.A, this.B), this.AC = this.createSideVector(this.A, this.C), this.alpha = Br(this.AB, this.AC), this.bisector = Nr(ss(this.AB.eq(Sl) ? this.AC : this.AB, this.alpha / 2));
  }
  calcOrthogonalProjection(t, r, i = this.strokeProjectionMagnitude) {
    let s = ns(this.createSideVector(t, r)), o = Er.getOrthogonalRotationFactor(s, this.bisector);
    return this.scaleUnitVector(s, i * o);
  }
  projectBevel() {
    let t = [];
    return (this.alpha % vt === 0 ? [this.B] : [this.B, this.C]).forEach((r) => {
      t.push(this.projectOrthogonally(this.A, r)), t.push(this.projectOrthogonally(this.A, r, -this.strokeProjectionMagnitude));
    }), t;
  }
  projectMiter() {
    let t = [], r = Math.abs(this.alpha), i = 1 / Math.sin(r / 2), s = this.scaleUnitVector(this.bisector, -this.strokeProjectionMagnitude * i), o = this.options.strokeUniform ? Rr(this.scaleUnitVector(this.bisector, this.options.strokeMiterLimit)) : this.options.strokeMiterLimit;
    return Rr(s) / this.strokeProjectionMagnitude <= o && t.push(this.applySkew(this.A.add(s))), t.push(...this.projectBevel()), t;
  }
  projectRoundNoSkew(t, r) {
    let i = [], s = new v(Er.getOrthogonalRotationFactor(this.bisector), Er.getOrthogonalRotationFactor(new v(this.bisector.y, this.bisector.x)));
    return [new v(1, 0).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar).multiply(s), new v(0, 1).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar).multiply(s)].forEach((o) => {
      yi(o, t, r) && i.push(this.A.add(o));
    }), i;
  }
  projectRoundWithSkew(t, r) {
    let i = [], { skewX: s, skewY: o, scaleX: n, scaleY: a, strokeUniform: l } = this.options, h = new v(Math.tan(I(s)), Math.tan(I(o))), c = this.strokeProjectionMagnitude, u = l ? c / a / Math.sqrt(1 / a ** 2 + 1 / n ** 2 * h.y ** 2) : c / Math.sqrt(1 + h.y ** 2), d = new v(Math.sqrt(Math.max(c ** 2 - u ** 2, 0)), u), g = l ? c / Math.sqrt(1 + h.x ** 2 * (1 / a) ** 2 / (1 / n + 1 / n * h.x * h.y) ** 2) : c / Math.sqrt(1 + h.x ** 2 / (1 + h.x * h.y) ** 2), p = new v(g, Math.sqrt(Math.max(c ** 2 - g ** 2, 0)));
    return [
      p,
      p.scalarMultiply(-1),
      d,
      d.scalarMultiply(-1)
    ].map((m) => this.applySkew(l ? m.multiply(this.strokeUniformScalar) : m)).forEach((m) => {
      yi(m, t, r) && i.push(this.applySkew(this.A).add(m));
    }), i;
  }
  projectRound() {
    let t = [];
    t.push(...this.projectBevel());
    let r = this.alpha % vt === 0, i = this.applySkew(this.A), s = t[r ? 0 : 2].subtract(i), o = t[+!!r].subtract(i), n = fe(s, r ? this.applySkew(this.AB.scalarMultiply(-1)) : this.applySkew(this.bisector.multiply(this.strokeUniformScalar).scalarMultiply(-1))) > 0, a = n ? s : o, l = n ? o : s;
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
}, Ys = class extends un {
  constructor(e, t, r) {
    super(r), this.A = new v(e), this.T = new v(t);
  }
  calcOrthogonalProjection(e, t, r = this.strokeProjectionMagnitude) {
    let i = this.createSideVector(e, t);
    return this.scaleUnitVector(ns(i), r);
  }
  projectButt() {
    return [this.projectOrthogonally(this.A, this.T, this.strokeProjectionMagnitude), this.projectOrthogonally(this.A, this.T, -this.strokeProjectionMagnitude)];
  }
  projectRound() {
    let e = [];
    if (!this.isSkewed() && this.A.eq(this.T)) {
      let t = new v(1, 1).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar);
      e.push(this.applySkew(this.A.add(t)), this.applySkew(this.A.subtract(t)));
    } else e.push(...new dn(this.A, this.T, this.T, this.options).projectRound());
    return e;
  }
  projectSquare() {
    let e = [];
    if (this.A.eq(this.T)) {
      let t = new v(1, 1).scalarMultiply(this.strokeProjectionMagnitude).multiply(this.strokeUniformScalar);
      e.push(this.A.add(t), this.A.subtract(t));
    } else {
      let t = this.calcOrthogonalProjection(this.A, this.T, this.strokeProjectionMagnitude), r = this.scaleUnitVector(Nr(this.createSideVector(this.A, this.T)), -this.strokeProjectionMagnitude), i = this.A.add(r);
      e.push(i.add(t), i.subtract(t));
    }
    return e.map((t) => this.applySkew(t));
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
    return this.projectPoints().map((e) => ({
      originPoint: this.A,
      projectedPoint: e
    }));
  }
}, gn = (e, t, r = !1) => {
  let i = [];
  if (e.length === 0) return i;
  let s = e.reduce((o, n) => (o[o.length - 1].eq(n) || o.push(new v(n)), o), [new v(e[0])]);
  if (s.length === 1) r = !0;
  else if (!r) {
    let o = s[0], n = ((a, l) => {
      for (let h = a.length - 1; h >= 0; h--) if (l(a[h], h, a)) return h;
      return -1;
    })(s, (a) => !a.eq(o));
    s.splice(n + 1);
  }
  return s.forEach((o, n, a) => {
    let l, h;
    n === 0 ? (h = a[1], l = r ? o : a[a.length - 1]) : n === a.length - 1 ? (l = a[n - 1], h = r ? o : a[0]) : (l = a[n - 1], h = a[n + 1]), r && a.length === 1 ? i.push(...new Ys(o, o, t).project()) : !r || n !== 0 && n !== a.length - 1 ? i.push(...new dn(o, l, h, t).project()) : i.push(...new Ys(o, n === 0 ? h : l, t).project());
  }), i;
}, vs = (e) => {
  let t = {};
  return Object.keys(e).forEach((r) => {
    t[r] = {}, Object.keys(e[r]).forEach((i) => {
      t[r][i] = { ...e[r][i] };
    });
  }), t;
}, ti = (e, t, r = !1) => e.fill !== t.fill || e.stroke !== t.stroke || e.strokeWidth !== t.strokeWidth || e.fontSize !== t.fontSize || e.fontFamily !== t.fontFamily || e.fontWeight !== t.fontWeight || e.fontStyle !== t.fontStyle || e.textDecorationThickness !== t.textDecorationThickness || e.textDecorationColor !== t.textDecorationColor || e.textBackgroundColor !== t.textBackgroundColor || e.deltaY !== t.deltaY || r && (e.overline !== t.overline || e.underline !== t.underline || e.linethrough !== t.linethrough), fn = (e, t) => {
  let r = t.split(`
`), i = [], s = -1, o = {};
  e = vs(e);
  for (let n = 0; n < r.length; n++) {
    let a = zr(r[n]);
    if (e[n]) for (let l = 0; l < a.length; l++) {
      s++;
      let h = e[n][l];
      h && Object.keys(h).length > 0 && (ti(o, h, !0) ? i.push({
        start: s,
        end: s + 1,
        style: h
      }) : i[i.length - 1].end++), o = h || {};
    }
    else s += a.length, o = {};
  }
  return i;
}, pn = (e, t) => {
  if (!Array.isArray(e)) return vs(e);
  let r = t.split(Ui), i = {}, s = -1, o = 0;
  for (let n = 0; n < r.length; n++) {
    let a = zr(r[n]);
    for (let l = 0; l < a.length; l++) s++, e[o] && e[o].start <= s && s < e[o].end && (i[n] = i[n] || {}, i[n][l] = { ...e[o].style }, s === e[o].end - 1 && o++);
  }
  return i;
}, Jt = [
  "display",
  "transform",
  st,
  "fill-opacity",
  "fill-rule",
  "opacity",
  Dt,
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
function $s(e, t) {
  let r = e.nodeName, i = e.getAttribute("class"), s = e.getAttribute("id"), o = "(?![a-zA-Z\\-]+)", n;
  if (n = RegExp("^" + r, "i"), t = t.replace(n, ""), s && t.length && (n = RegExp("#" + s + o, "i"), t = t.replace(n, "")), i && t.length) {
    let a = i.split(" ");
    for (let l = a.length; l--; ) n = RegExp("\\." + a[l] + o, "i"), t = t.replace(n, "");
  }
  return t.length === 0;
}
function Cl(e, t) {
  let r = !0, i = $s(e, t.pop());
  return i && t.length && (r = (function(s, o) {
    let n, a = !0;
    for (; s.parentElement && s.parentElement.nodeType === 1 && o.length; ) a && (n = o.pop()), a = $s(s = s.parentElement, n);
    return o.length === 0;
  })(e, t)), i && r && t.length === 0;
}
function bl(e, t = {}) {
  let r = {};
  for (let i in t) Cl(e, i.split(" ")) && (r = {
    ...r,
    ...t[i]
  });
  return r;
}
var wl = (e) => {
  var t;
  return (t = Fa[e]) == null ? e : t;
}, Tl = RegExp(`(${ft})`, "gi"), tt = `(${ft})`, Ol = String.raw`(skewX)\(${tt}\)`, kl = String.raw`(skewY)\(${tt}\)`, Ml = String.raw`(rotate)\(${tt}(?: ${tt} ${tt})?\)`, Dl = String.raw`(scale)\(${tt}(?: ${tt})?\)`, El = String.raw`(translate)\(${tt}(?: ${tt})?\)`, ys = `(?:${String.raw`(matrix)\(${tt} ${tt} ${tt} ${tt} ${tt} ${tt}\)`}|${El}|${Ml}|${Dl}|${Ol}|${kl})`, Pl = `(?:${ys}*)`, Al = String.raw`^\s*(?:${Pl}?)\s*$`, jl = new RegExp(Al), Fl = new RegExp(ys), Ll = new RegExp(ys, "g");
function bi(e) {
  let t = [];
  if (!(e = ((r) => Ir(r.replace(Tl, " $1 ").replace(/,/gi, " ")))(e).replace(/\s*([()])\s*/gi, "$1")) || e && !jl.test(e)) return [...et];
  for (let r of e.matchAll(Ll)) {
    let i = Fl.exec(r[0]);
    if (!i) continue;
    let s = et, [, o, ...n] = i.filter((g) => !!g), [a, l, h, c, u, d] = n.map((g) => parseFloat(g));
    switch (o) {
      case "translate":
        s = ke(a, l);
        break;
      case ao:
        s = ne({ angle: a }, {
          x: l,
          y: h
        });
        break;
      case co:
        s = Hr(a, l);
        break;
      case Te:
        s = Zi(a);
        break;
      case Oe:
        s = ts(a);
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
  return Vr(t);
}
function Rl(e, t, r, i) {
  let s = Array.isArray(t), o, n = t;
  if (e !== "fill" && e !== "stroke" || t !== "none") {
    if (e === "strokeUniform") return t === "non-scaling-stroke";
    if (e === "strokeDashArray") n = t === "none" ? null : t.replace(/,/g, " ").split(/\s+/).map(parseFloat);
    else if (e === "transformMatrix") n = r && r.transformMatrix ? Y(r.transformMatrix, bi(t)) : bi(t);
    else if (e === "visible") n = t !== "none" && t !== "hidden", r && r.visible === !1 && (n = !1);
    else if (e === "opacity") n = parseFloat(t), r && r.opacity !== void 0 && (n *= r.opacity);
    else if (e === "textAnchor") n = t === "start" ? H : t === "end" ? pt : L;
    else if (e === "charSpacing" || e === "textDecorationThickness") o = se(t, i) / i * 1e3;
    else if (e === "paintFirst") {
      let a = t.indexOf(st), l = t.indexOf(Dt);
      n = st, (a > -1 && l > -1 && l < a || a === -1 && l > -1) && (n = Dt);
    } else {
      if (e === "href" || e === "xlink:href" || e === "font" || e === "id") return t;
      if (e === "imageSmoothing") return t === "optimizeQuality";
      o = s ? t.map(se) : se(t, i);
    }
  } else n = "";
  return !s && isNaN(o) ? n : o;
}
function Bl(e, t) {
  e.replace(/;\s*$/, "").split(";").forEach((r) => {
    if (!r) return;
    let [i, s] = r.split(":");
    t[i.trim().toLowerCase()] = s.trim();
  });
}
function Il(e) {
  let t = {}, r = e.getAttribute("style");
  return r && (typeof r == "string" ? Bl(r, t) : (function(i, s) {
    Object.entries(i).forEach(([o, n]) => {
      n !== void 0 && (s[o.toLowerCase()] = n);
    });
  })(r, t)), t;
}
var Xl = {
  stroke: "strokeOpacity",
  fill: "fillOpacity"
};
function Ft(e, t, r) {
  if (!e) return {};
  let i, s = {}, o = 16;
  e.parentNode && Bs.test(e.parentNode.nodeName) && (s = Ft(e.parentElement, t, r), s.fontSize && (i = o = se(s.fontSize)));
  let n = {
    ...t.reduce((h, c) => {
      let u = e.getAttribute(c);
      return u && (h[c] = u), h;
    }, {}),
    ...bl(e, r),
    ...Il(e)
  };
  n["clip-path"] && e.setAttribute(Rs, n[Rs]), n["font-size"] && (i = se(n[Ls], o), n[Ls] = `${i}`);
  let a = {};
  for (let h in n) {
    let c = wl(h);
    a[c] = Rl(c, n[h], s, i);
  }
  a && a.font && (function(h, c) {
    let u = h.match(ja);
    if (!u) return;
    let d = u[1], g = u[3], p = u[4], m = u[5], x = u[6];
    d && (c.fontStyle = d), g && (c.fontWeight = isNaN(parseFloat(g)) ? g : parseFloat(g)), p && (c.fontSize = se(p)), x && (c.fontFamily = x), m && (c.lineHeight = m === "normal" ? 1 : m);
  })(a.font, a);
  let l = {
    ...s,
    ...a
  };
  return Bs.test(e.nodeName) ? l : (function(h) {
    let c = q.getDefaults();
    return Object.entries(Xl).forEach(([u, d]) => {
      if (h[d] === void 0 || h[u] === "") return;
      if (h[u] === void 0) {
        if (!c[u]) return;
        h[u] = c[u];
      }
      if (h[u].indexOf("url(") === 0) return;
      let g = new K(h[u]);
      h[u] = g.setAlpha(F(g.getAlpha() * h[d], 2)).toRgba();
    }), h;
  })(l);
}
var mn = ["rx", "ry"], rt = class wi extends q {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...wi.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, wi.ownDefaults), this.setOptions(t), this._initRxRy();
  }
  _initRxRy() {
    let { rx: t, ry: r } = this;
    t && !r ? this.ry = t : r && !t && (this.rx = r);
  }
  _render(t) {
    let { width: r, height: i } = this, s = -r / 2, o = -i / 2, n = this.rx ? Math.min(this.rx, r / 2) : 0, a = this.ry ? Math.min(this.ry, i / 2) : 0, l = n !== 0 || a !== 0;
    t.beginPath(), t.moveTo(s + n, o), t.lineTo(s + r - n, o), l && t.bezierCurveTo(s + r - 0.4477152502 * n, o, s + r, o + 0.4477152502 * a, s + r, o + a), t.lineTo(s + r, o + i - a), l && t.bezierCurveTo(s + r, o + i - 0.4477152502 * a, s + r - 0.4477152502 * n, o + i, s + r - n, o + i), t.lineTo(s + n, o + i), l && t.bezierCurveTo(s + 0.4477152502 * n, o + i, s, o + i - 0.4477152502 * a, s, o + i - a), t.lineTo(s, o + a), l && t.bezierCurveTo(s, o + 0.4477152502 * a, s + 0.4477152502 * n, o, s + n, o), t.closePath(), this._renderPaintInOrder(t);
  }
  toObject(t = []) {
    return super.toObject([...mn, ...t]);
  }
  _toSVG() {
    let { width: t, height: r, rx: i, ry: s } = this;
    return [
      "<rect ",
      "COMMON_PARTS",
      `x="${-t / 2}" y="${-r / 2}" rx="${M(i)}" ry="${M(s)}" width="${M(t)}" height="${M(r)}" />
`
    ];
  }
  static async fromElement(t, r, i) {
    let { left: s = 0, top: o = 0, width: n = 0, height: a = 0, visible: l = !0, ...h } = Ft(t, this.ATTRIBUTE_NAMES, i);
    return new this({
      ...r,
      ...h,
      left: s,
      top: o,
      width: n,
      height: a,
      visible: !!(l && n && a)
    });
  }
};
f(rt, "type", "Rect"), f(rt, "cacheProperties", [...At, ...mn]), f(rt, "ownDefaults", {
  rx: 0,
  ry: 0
}), f(rt, "ATTRIBUTE_NAMES", [
  ...Jt,
  "x",
  "y",
  "rx",
  "ry",
  "width",
  "height"
]), w.setClass(rt), w.setSVGClass(rt);
var Ws = "initialization", Ti = "added", vn = (e, t) => {
  let { strokeUniform: r, strokeWidth: i, width: s, height: o, group: n } = t, a = n && n !== e ? dr(n.calcTransformMatrix(), e.calcTransformMatrix()) : null, l = a ? t.getRelativeCenterPoint().transform(a) : t.getRelativeCenterPoint(), h = !t.isStrokeAccountedForInDimensions(), c = r && h ? Do(new v(i, i), void 0, e.calcTransformMatrix()) : Ni, u = !r && h ? i : 0, d = Ur(s + u, o + u, Vr([a, t.calcOwnMatrix()], !0)).add(c).scalarDivide(2);
  return [l.subtract(d), l.add(d)];
}, ei = class {
  calcLayoutResult(e, t) {
    if (this.shouldPerformLayout(e)) return this.calcBoundingBox(t, e);
  }
  shouldPerformLayout({ type: e, prevStrategy: t, strategy: r }) {
    return e === "initialization" || e === "imperative" || !!t && r !== t;
  }
  shouldLayoutClipPath({ type: e, target: { clipPath: t } }) {
    return e !== "initialization" && t && !t.absolutePositioned;
  }
  getInitialSize(e, t) {
    return t.size;
  }
  calcBoundingBox(e, t) {
    let { type: r, target: i } = t;
    if (r === "imperative" && t.overrides) return t.overrides;
    if (e.length === 0) return;
    let { left: s, top: o, width: n, height: a } = bt(e.map((c) => vn(i, c)).reduce((c, u) => c.concat(u), [])), l = new v(n, a), h = new v(s, o).add(l.scalarDivide(2));
    if (r === "initialization") {
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
f(ei, "type", "strategy");
var Oi = class extends ei {
  shouldPerformLayout(e) {
    return !0;
  }
};
f(Oi, "type", "fit-content"), w.setClass(Oi);
var yn = "layoutManager", nr = class {
  constructor(e = new Oi()) {
    f(this, "strategy", void 0), this.strategy = e, this._subscriptions = /* @__PURE__ */ new Map();
  }
  performLayout(e) {
    let t = {
      bubbles: !0,
      strategy: this.strategy,
      ...e,
      prevStrategy: this._prevLayoutStrategy,
      stopPropagation() {
        this.bubbles = !1;
      }
    };
    this.onBeforeLayout(t);
    let r = this.getLayoutResult(t);
    r && this.commitLayout(t, r), this.onAfterLayout(t, r), this._prevLayoutStrategy = t.strategy;
  }
  attachHandlers(e, t) {
    let { target: r } = t;
    return [
      uo,
      oo,
      ir,
      no,
      Wr,
      lo,
      jr,
      ho,
      "modifyPath"
    ].map((i) => e.on(i, (s) => this.performLayout(i === "modified" ? {
      type: "object_modified",
      trigger: i,
      e: s,
      target: r
    } : {
      type: "object_modifying",
      trigger: i,
      e: s,
      target: r
    })));
  }
  subscribe(e, t) {
    this.unsubscribe(e, t);
    let r = this.attachHandlers(e, t);
    this._subscriptions.set(e, r);
  }
  unsubscribe(e, t) {
    (this._subscriptions.get(e) || []).forEach((r) => r()), this._subscriptions.delete(e);
  }
  unsubscribeTargets(e) {
    e.targets.forEach((t) => this.unsubscribe(t, e));
  }
  subscribeTargets(e) {
    e.targets.forEach((t) => this.subscribe(t, e));
  }
  onBeforeLayout(e) {
    let { target: t, type: r } = e, { canvas: i } = t;
    if (r === "initialization" || r === "added" ? this.subscribeTargets(e) : r === "removed" && this.unsubscribeTargets(e), t.fire("layout:before", { context: e }), i && i.fire("object:layout:before", {
      target: t,
      context: e
    }), r === "imperative" && e.deep) {
      let { strategy: s, ...o } = e;
      t.forEachObject((n) => n.layoutManager && n.layoutManager.performLayout({
        ...o,
        bubbles: !1,
        target: n
      }));
    }
  }
  getLayoutResult(e) {
    let { target: t, strategy: r, type: i } = e, s = r.calcLayoutResult(e, t.getObjects());
    if (!s) return;
    let o = i === "initialization" ? new v() : t.getRelativeCenterPoint(), { center: n, correction: a = new v(), relativeCorrection: l = new v() } = s;
    return {
      result: s,
      prevCenter: o,
      nextCenter: n,
      offset: o.subtract(n).add(a).transform(i === "initialization" ? et : lt(t.calcOwnMatrix()), !0).add(l)
    };
  }
  commitLayout(e, t) {
    let { target: r } = e, { result: { size: i }, nextCenter: s } = t;
    var o, n;
    r.set({
      width: i.x,
      height: i.y
    }), this.layoutObjects(e, t), e.type === "initialization" ? r.set({
      left: (o = e.x) == null ? s.x + i.x * Z(r.originX) : o,
      top: (n = e.y) == null ? s.y + i.y * Z(r.originY) : n
    }) : (r.setPositionByOrigin(s, L, L), r.setCoords(), r.set("dirty", !0));
  }
  layoutObjects(e, t) {
    let { target: r } = e;
    r.forEachObject((i) => {
      i.group === r && this.layoutObject(e, t, i);
    }), e.strategy.shouldLayoutClipPath(e) && this.layoutObject(e, t, r.clipPath);
  }
  layoutObject(e, { offset: t }, r) {
    r.set({
      left: r.left + t.x,
      top: r.top + t.y
    });
  }
  onAfterLayout(e, t) {
    let { target: r, strategy: i, bubbles: s, prevStrategy: o, ...n } = e, { canvas: a } = r;
    r.fire("layout:after", {
      context: e,
      result: t
    }), a && a.fire("object:layout:after", {
      context: e,
      result: t,
      target: r
    });
    let l = r.parent;
    s && l != null && l.layoutManager && ((n.path || (n.path = [])).push(r), l.layoutManager.performLayout({
      ...n,
      target: l
    })), r.set("dirty", !0);
  }
  dispose() {
    let { _subscriptions: e } = this;
    e.forEach((t) => t.forEach((r) => r())), e.clear();
  }
  toObject() {
    return {
      type: yn,
      strategy: this.strategy.constructor.type
    };
  }
  toJSON() {
    return this.toObject();
  }
};
w.setClass(nr, yn);
var Yl = class extends nr {
  performLayout() {
  }
}, me = class ki extends go(q) {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...ki.ownDefaults
    };
  }
  constructor(t = [], r = {}) {
    super(), f(this, "_activeObjects", []), f(this, "__objectSelectionTracker", void 0), f(this, "__objectSelectionDisposer", void 0), Object.assign(this, ki.ownDefaults), this.setOptions(r), this.groupInit(t, r);
  }
  groupInit(t, r) {
    var i;
    this._objects = [...t], this.__objectSelectionTracker = this.__objectSelectionMonitor.bind(this, !0), this.__objectSelectionDisposer = this.__objectSelectionMonitor.bind(this, !1), this.forEachObject((s) => {
      this.enterGroup(s, !1);
    }), this.layoutManager = (i = r.layoutManager) == null ? new nr() : i, this.layoutManager.performLayout({
      type: Ws,
      target: this,
      targets: [...t],
      x: r.left,
      y: r.top
    });
  }
  canEnterGroup(t) {
    return t === this || this.isDescendantOf(t) ? (zt("error", "Group: circular object trees are not supported, this call has no effect"), !1) : this._objects.indexOf(t) === -1 || (zt("error", "Group: duplicate objects are not supported inside group, this call has no effect"), !1);
  }
  _filterObjectsBeforeEnteringGroup(t) {
    return t.filter((r, i, s) => this.canEnterGroup(r) && s.indexOf(r) === i);
  }
  add(...t) {
    let r = this._filterObjectsBeforeEnteringGroup(t), i = super.add(...r);
    return this._onAfterObjectsChange(Ti, r), i;
  }
  insertAt(t, ...r) {
    let i = this._filterObjectsBeforeEnteringGroup(r), s = super.insertAt(t, ...i);
    return this._onAfterObjectsChange(Ti, i), s;
  }
  remove(...t) {
    let r = super.remove(...t);
    return this._onAfterObjectsChange("removed", r), r;
  }
  _onObjectAdded(t) {
    this.enterGroup(t, !0), this.fire("object:added", { target: t }), t.fire("added", { target: this });
  }
  _onObjectRemoved(t, r) {
    this.exitGroup(t, r), this.fire("object:removed", { target: t }), t.fire("removed", { target: this });
  }
  _onAfterObjectsChange(t, r) {
    this.layoutManager.performLayout({
      type: t,
      targets: r,
      target: this
    });
  }
  _onStackOrderChanged() {
    this._set("dirty", !0);
  }
  _set(t, r) {
    let i = this[t];
    return super._set(t, r), t === "canvas" && i !== r && (this._objects || []).forEach((s) => {
      s._set(t, r);
    }), this;
  }
  _shouldSetNestedCoords() {
    return this.subTargetCheck;
  }
  removeAll() {
    return this._activeObjects = [], this.remove(...this._objects);
  }
  __objectSelectionMonitor(t, { target: r }) {
    let i = this._activeObjects;
    if (t) i.push(r), this._set("dirty", !0);
    else if (i.length > 0) {
      let s = i.indexOf(r);
      s > -1 && (i.splice(s, 1), this._set("dirty", !0));
    }
  }
  _watchObject(t, r) {
    t && this._watchObject(!1, r), t ? (r.on("selected", this.__objectSelectionTracker), r.on("deselected", this.__objectSelectionDisposer)) : (r.off("selected", this.__objectSelectionTracker), r.off("deselected", this.__objectSelectionDisposer));
  }
  enterGroup(t, r) {
    t.group && t.group.remove(t), t._set("parent", this), this._enterGroup(t, r);
  }
  _enterGroup(t, r) {
    r && Ce(t, Y(lt(this.calcTransformMatrix()), t.calcTransformMatrix())), this._shouldSetNestedCoords() && t.setCoords(), t._set("group", this), t._set("canvas", this.canvas), this._watchObject(!0, t);
    let i = this.canvas && this.canvas.getActiveObject && this.canvas.getActiveObject();
    i && (i === t || t.isDescendantOf(i)) && this._activeObjects.push(t);
  }
  exitGroup(t, r) {
    this._exitGroup(t, r), t._set("parent", void 0), t._set("canvas", void 0);
  }
  _exitGroup(t, r) {
    t._set("group", void 0), r || (Ce(t, Y(this.calcTransformMatrix(), t.calcTransformMatrix())), t.setCoords()), this._watchObject(!1, t);
    let i = this._activeObjects.length > 0 ? this._activeObjects.indexOf(t) : -1;
    i > -1 && this._activeObjects.splice(i, 1);
  }
  shouldCache() {
    let t = q.prototype.shouldCache.call(this);
    if (t) {
      for (let r = 0; r < this._objects.length; r++) if (this._objects[r].willDrawShadow()) return this.ownCaching = !1, !1;
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
  drawObject(t, r, i) {
    this._renderBackground(t);
    for (let o = 0; o < this._objects.length; o++) {
      var s;
      let n = this._objects[o];
      (s = this.canvas) != null && s.preserveObjectStacking && n.group !== this ? (t.save(), t.transform(...lt(this.calcTransformMatrix())), n.render(t), t.restore()) : n.group === this && n.render(t);
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
  __serializeObjects(t, r) {
    let i = this.includeDefaultValues;
    return this._objects.filter(function(s) {
      return !s.excludeFromExport;
    }).map(function(s) {
      let o = s.includeDefaultValues;
      s.includeDefaultValues = i;
      let n = s[t || "toObject"](r);
      return s.includeDefaultValues = o, n;
    });
  }
  toObject(t = []) {
    let r = this.layoutManager.toObject();
    return {
      ...super.toObject([
        "subTargetCheck",
        "interactive",
        ...t
      ]),
      ...r.strategy !== "fit-content" || this.includeDefaultValues ? { layoutManager: r } : {},
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
    let r = rt.prototype._toSVG.call(this), i = r.indexOf("COMMON_PARTS");
    r[i] = 'for="group" ';
    let s = r.join("");
    return t ? t(s) : s;
  }
  _toSVG(t) {
    let r = [
      "<g ",
      "COMMON_PARTS",
      ` >
`
    ], i = this._createSVGBgRect(t);
    i && r.push("		", i);
    for (let s = 0; s < this._objects.length; s++) r.push("		", this._objects[s].toSVG(t));
    return r.push(`</g>
`), r;
  }
  getSvgStyles() {
    let t = this.opacity !== void 0 && this.opacity !== 1 ? `opacity: ${M(this.opacity)};` : "", r = this.visible ? "" : " visibility: hidden;";
    return [
      t,
      this.getSvgFilter(),
      r
    ].join("");
  }
  toClipPathSVG(t) {
    let r = [], i = this._createSVGBgRect(t);
    i && r.push("	", i);
    for (let s = 0; s < this._objects.length; s++) r.push("	", this._objects[s].toClipPathSVG(t));
    return this._createBaseClipPathSVGMarkup(r, { reviver: t });
  }
  static fromObject({ type: t, objects: r = [], layoutManager: i, ...s }, o) {
    return Promise.all([_e(r, o), ur(s, o)]).then(([n, a]) => {
      let l = new this(n, {
        ...s,
        ...a,
        layoutManager: new Yl()
      });
      return l.layoutManager = i ? new (w.getClass(i.type))(new (w.getClass(i.strategy))()) : new nr(), l.layoutManager.subscribeTargets({
        type: Ws,
        target: l,
        targets: l.getObjects()
      }), l.setCoords(), l;
    });
  }
};
f(me, "type", "Group"), f(me, "ownDefaults", {
  strokeWidth: 0,
  subTargetCheck: !1,
  interactive: !1
}), w.setClass(me);
var $l = (e, t) => e && e.length === 1 ? e[0] : new me(e, t), xn = (e, t) => Math.min(t.width / e.width, t.height / e.height), _n = (e, t) => Math.max(t.width / e.width, t.height / e.height), Mi = "\\s*,?\\s*", je = `${Mi}(${ft})`, Wl = `${je}${je}${je}${Mi}([01])${Mi}([01])${je}${je}`, Vl = {
  m: "l",
  M: "L"
}, Hl = (e, t, r, i, s, o, n, a, l, h, c) => {
  let u = yt(e), d = xt(e), g = yt(t), p = xt(t), m = r * s * g - i * o * p + n, x = i * s * g + r * o * p + a;
  return [
    "C",
    h + l * (-r * s * d - i * o * u),
    c + l * (-i * s * d + r * o * u),
    m + l * (r * s * p + i * o * g),
    x + l * (i * s * p - r * o * g),
    m,
    x
  ];
}, Vs = (e, t, r, i) => {
  let s = Math.atan2(t, e), o = Math.atan2(i, r);
  return o >= s ? o - s : 2 * Math.PI - (s - o);
};
function Di(e, t, r, i, s, o, n, a) {
  let l;
  if (P.cachesBoundsOfCurve && (l = [...arguments].join(), Ze.boundsOfCurveCache[l])) return Ze.boundsOfCurveCache[l];
  let h = Math.sqrt, c = Math.abs, u = [], d = [[0, 0], [0, 0]], g = 6 * e - 12 * r + 6 * s, p = -3 * e + 9 * r - 9 * s + 3 * n, m = 3 * r - 3 * e;
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
  let x = u.length, _ = x, y = Cn(e, t, r, i, s, o, n, a);
  for (; x--; ) {
    let { x: C, y: b } = y(u[x]);
    d[0][x] = C, d[1][x] = b;
  }
  d[0][_] = e, d[1][_] = t, d[0][_ + 1] = n, d[1][_ + 1] = a;
  let S = [new v(Math.min(...d[0]), Math.min(...d[1])), new v(Math.max(...d[0]), Math.max(...d[1]))];
  return P.cachesBoundsOfCurve && (Ze.boundsOfCurveCache[l] = S), S;
}
var zl = (e, t, [r, i, s, o, n, a, l, h]) => {
  let c = ((u, d, g, p, m, x, _) => {
    if (g === 0 || p === 0) return [];
    let y = 0, S = 0, C = 0, b = Math.PI, O = _ * Gi, T = xt(O), k = yt(O), D = 0.5 * (-k * u - T * d), B = 0.5 * (-k * d + T * u), A = g ** 2, E = p ** 2, R = B ** 2, X = D ** 2, G = A * E - A * R - E * X, $ = Math.abs(g), J = Math.abs(p);
    if (G < 0) {
      let Bt = Math.sqrt(1 - G / (A * E));
      $ *= Bt, J *= Bt;
    } else C = (m === x ? -1 : 1) * Math.sqrt(G / (A * R + E * X));
    let ot = C * $ * B / J, j = -C * J * D / $, _t = k * ot - T * j + 0.5 * u, Me = T * ot + k * j + 0.5 * d, De = Vs(1, 0, (D - ot) / $, (B - j) / J), Rt = Vs((D - ot) / $, (B - j) / J, (-D - ot) / $, (-B - j) / J);
    x === 0 && Rt > 0 ? Rt -= 2 * b : x === 1 && Rt < 0 && (Rt += 2 * b);
    let Ee = Math.ceil(Math.abs(Rt / b * 2)), gr = [], Pe = Rt / Ee, ca = 8 / 3 * Math.sin(Pe / 4) * Math.sin(Pe / 4) / Math.sin(Pe / 2), ii = De + Pe;
    for (let Bt = 0; Bt < Ee; Bt++) gr[Bt] = Hl(De, ii, k, T, $, J, _t, Me, ca, y, S), y = gr[Bt][5], S = gr[Bt][6], De = ii, ii += Pe;
    return gr;
  })(l - e, h - t, i, s, n, a, o);
  for (let u = 0, d = c.length; u < d; u++) c[u][1] += e, c[u][2] += t, c[u][3] += e, c[u][4] += t, c[u][5] += e, c[u][6] += t;
  return c;
}, Sn = (e) => {
  let t = 0, r = 0, i = 0, s = 0, o = [], n, a = 0, l = 0;
  for (let h of e) {
    let c = [...h], u;
    switch (c[0]) {
      case "l":
        c[1] += t, c[2] += r;
      case "L":
        t = c[1], r = c[2], u = [
          "L",
          t,
          r
        ];
        break;
      case "h":
        c[1] += t;
      case "H":
        t = c[1], u = [
          "L",
          t,
          r
        ];
        break;
      case "v":
        c[1] += r;
      case "V":
        r = c[1], u = [
          "L",
          t,
          r
        ];
        break;
      case "m":
        c[1] += t, c[2] += r;
      case "M":
        t = c[1], r = c[2], i = c[1], s = c[2], u = [
          "M",
          t,
          r
        ];
        break;
      case "c":
        c[1] += t, c[2] += r, c[3] += t, c[4] += r, c[5] += t, c[6] += r;
      case "C":
        a = c[3], l = c[4], t = c[5], r = c[6], u = [
          "C",
          c[1],
          c[2],
          a,
          l,
          t,
          r
        ];
        break;
      case "s":
        c[1] += t, c[2] += r, c[3] += t, c[4] += r;
      case "S":
        n === "C" ? (a = 2 * t - a, l = 2 * r - l) : (a = t, l = r), t = c[3], r = c[4], u = [
          "C",
          a,
          l,
          c[1],
          c[2],
          t,
          r
        ], a = u[3], l = u[4];
        break;
      case "q":
        c[1] += t, c[2] += r, c[3] += t, c[4] += r;
      case "Q":
        a = c[1], l = c[2], t = c[3], r = c[4], u = [
          "Q",
          a,
          l,
          t,
          r
        ];
        break;
      case "t":
        c[1] += t, c[2] += r;
      case "T":
        n === "Q" ? (a = 2 * t - a, l = 2 * r - l) : (a = t, l = r), t = c[1], r = c[2], u = [
          "Q",
          a,
          l,
          t,
          r
        ];
        break;
      case "a":
        c[6] += t, c[7] += r;
      case "A":
        zl(t, r, c).forEach((d) => o.push(d)), t = c[6], r = c[7];
        break;
      case "z":
      case "Z":
        t = i, r = s, u = ["Z"];
    }
    u ? (o.push(u), n = u[0]) : n = "";
  }
  return o;
}, Xr = (e, t, r, i) => Math.sqrt((r - e) ** 2 + (i - t) ** 2), Cn = (e, t, r, i, s, o, n, a) => (l) => {
  let h = l ** 3, c = ((g) => 3 * g ** 2 * (1 - g))(l), u = ((g) => 3 * g * (1 - g) ** 2)(l), d = ((g) => (1 - g) ** 3)(l);
  return new v(n * h + s * c + r * u + e * d, a * h + o * c + i * u + t * d);
}, bn = (e) => e ** 2, wn = (e) => 2 * e * (1 - e), Tn = (e) => (1 - e) ** 2, Gl = (e, t, r, i, s, o, n, a) => (l) => {
  let h = bn(l), c = wn(l), u = Tn(l), d = 3 * (u * (r - e) + c * (s - r) + h * (n - s)), g = 3 * (u * (i - t) + c * (o - i) + h * (a - o));
  return Math.atan2(g, d);
}, Ul = (e, t, r, i, s, o) => (n) => {
  let a = bn(n), l = wn(n), h = Tn(n);
  return new v(s * a + r * l + e * h, o * a + i * l + t * h);
}, Nl = (e, t, r, i, s, o) => (n) => {
  let a = 1 - n, l = 2 * (a * (r - e) + n * (s - r)), h = 2 * (a * (i - t) + n * (o - i));
  return Math.atan2(h, l);
}, Hs = (e, t, r) => {
  let i = new v(t, r), s = 0;
  for (let o = 1; o <= 100; o += 1) {
    let n = e(o / 100);
    s += Xr(i.x, i.y, n.x, n.y), i = n;
  }
  return s;
}, ql = (e, t) => {
  let r, i = 0, s = 0, o = {
    x: e.x,
    y: e.y
  }, n = { ...o }, a = 0.01, l = 0, h = e.iterator, c = e.angleFinder;
  for (; s < t && a > 1e-4; ) n = h(i), l = i, r = Xr(o.x, o.y, n.x, n.y), r + s > t ? (i -= a, a /= 2) : (o = n, i += a, s += r);
  return {
    ...n,
    angle: c(l)
  };
}, xs = (e) => {
  let t, r, i = 0, s = 0, o = 0, n = 0, a = 0, l = [];
  for (let h of e) {
    let c = {
      x: s,
      y: o,
      command: h[0],
      length: 0
    };
    switch (h[0]) {
      case "M":
        r = c, r.x = n = s = h[1], r.y = a = o = h[2];
        break;
      case "L":
        r = c, r.length = Xr(s, o, h[1], h[2]), s = h[1], o = h[2];
        break;
      case "C":
        t = Cn(s, o, h[1], h[2], h[3], h[4], h[5], h[6]), r = c, r.iterator = t, r.angleFinder = Gl(s, o, h[1], h[2], h[3], h[4], h[5], h[6]), r.length = Hs(t, s, o), s = h[5], o = h[6];
        break;
      case "Q":
        t = Ul(s, o, h[1], h[2], h[3], h[4]), r = c, r.iterator = t, r.angleFinder = Nl(s, o, h[1], h[2], h[3], h[4]), r.length = Hs(t, s, o), s = h[3], o = h[4];
        break;
      case "Z":
        r = c, r.destX = n, r.destY = a, r.length = Xr(s, o, n, a), s = n, o = a;
    }
    i += r.length, l.push(r);
  }
  return l.push({
    length: i,
    x: s,
    y: o
  }), l;
}, On = (e, t, r = xs(e)) => {
  let i = 0;
  for (; t - r[i].length > 0 && i < r.length - 2; ) t -= r[i].length, i++;
  let s = r[i], o = t / s.length, n = e[i];
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
      return ql(s, t);
  }
}, Kl = RegExp("[mzlhvcsqta][^mzlhvcsqta]*", "gi"), zs = new RegExp(Wl, "g"), Jl = new RegExp(ft, "gi"), Ql = {
  m: 2,
  l: 2,
  h: 1,
  v: 1,
  c: 6,
  s: 4,
  q: 4,
  t: 2,
  a: 7
}, kn = (e) => {
  var t;
  let r = [], i = (t = e.match(Kl)) == null ? [] : t;
  for (let s of i) {
    let o = s[0];
    if (o === "z" || o === "Z") {
      r.push([o]);
      continue;
    }
    let n = Ql[o.toLowerCase()], a = [];
    if (o === "a" || o === "A") {
      let l;
      for (zs.lastIndex = 0; l = zs.exec(s); ) a.push(...l.slice(1));
    } else a = s.match(Jl) || [];
    for (let l = 0; l < a.length; l += n) {
      let h = Array(n), c = Vl[o];
      h[0] = l > 0 && c ? c : o;
      for (let u = 0; u < n; u++) h[u + 1] = parseFloat(a[l + u]);
      r.push(h);
    }
  }
  return r;
}, Mn = (e, t = 0) => {
  let r = new v(e[0]), i = new v(e[1]), s = 1, o = 0, n = [], a = e.length, l = a > 2, h;
  for (l && (s = e[2].x < i.x ? -1 : e[2].x === i.x ? 0 : 1, o = e[2].y < i.y ? -1 : e[2].y === i.y ? 0 : 1), n.push([
    "M",
    r.x - s * t,
    r.y - o * t
  ]), h = 1; h < a; h++) {
    if (!r.eq(i)) {
      let c = r.midPointFrom(i);
      n.push([
        "Q",
        r.x,
        r.y,
        c.x,
        c.y
      ]);
    }
    r = e[h], h + 1 < e.length && (i = e[h + 1]);
  }
  return l && (s = r.x > e[h - 2].x ? 1 : r.x === e[h - 2].x ? 0 : -1, o = r.y > e[h - 2].y ? 1 : r.y === e[h - 2].y ? 0 : -1), n.push([
    "L",
    r.x + s * t,
    r.y + o * t
  ]), n;
}, Zl = (e, t, r) => (r && (t = Y(t, [
  1,
  0,
  0,
  1,
  -r.x,
  -r.y
])), e.map((i) => {
  let s = [...i];
  for (let o = 1; o < i.length - 1; o += 2) {
    let { x: n, y: a } = N({
      x: i[o],
      y: i[o + 1]
    }, t);
    s[o] = n, s[o + 1] = a;
  }
  return s;
})), th = (e, t) => {
  let r = 2 * Math.PI / e, i = -Ut;
  e % 2 == 0 && (i += r / 2);
  let s = Array(e + 1);
  for (let o = 0; o < e; o++) {
    let n = o * r + i, { x: a, y: l } = new v(yt(n), xt(n)).scalarMultiply(t);
    s[o] = [
      o === 0 ? "M" : "L",
      a,
      l
    ];
  }
  return s[e] = ["Z"], s;
}, _s = (e, t) => e.map((r) => r.map((i, s) => s === 0 || t === void 0 ? i : F(i, t)).join(" ")).join(" "), eh = (e, t) => {
  var r;
  let i = e, s = t;
  i.inverted && !s.inverted && (i = t, s = e), is(s, (r = s.group) == null ? void 0 : r.calcTransformMatrix(), i.calcTransformMatrix());
  let o = i.inverted && s.inverted;
  return o && (i.inverted = s.inverted = !1), new me([i], {
    clipPath: s,
    inverted: o
  });
}, rh = (e, t) => Math.floor(Math.random() * (t - e + 1)) + e, ih = (e, t) => {
  let r = e._findCenterFromElement();
  e.transformMatrix && (((i) => {
    if (i.transformMatrix) {
      let { scaleX: s, scaleY: o, angle: n, skewX: a } = xe(i.transformMatrix);
      i.flipX = !1, i.flipY = !1, i.set(Nt, s), i.set(qt, o), i.angle = n, i.skewX = a, i.skewY = 0;
    }
  })(e), r = r.transform(e.transformMatrix)), delete e.transformMatrix, t && (e.scaleX *= t.scaleX, e.scaleY *= t.scaleY, e.cropX = t.cropX, e.cropY = t.cropY, r.x += t.offsetLeft, r.y += t.offsetTop, e.width = t.width, e.height = t.height), e.setPositionByOrigin(r, L, L);
}, ar = hr({
  addTransformToObject: () => ko,
  animate: () => gs,
  animateColor: () => Vo,
  applyTransformToObject: () => Ce,
  calcAngleBetweenVectors: () => Br,
  calcDimensionsMatrix: () => cr,
  calcPlaneChangeMatrix: () => dr,
  calcVectorRotation: () => os,
  cancelAnimFrame: () => po,
  capValue: () => oe,
  composeMatrix: () => _o,
  copyCanvasElement: () => xa,
  cos: () => yt,
  createCanvasElement: () => Tt,
  createImage: () => mo,
  createRotateMatrix: () => ne,
  createScaleMatrix: () => Hr,
  createSkewXMatrix: () => Zi,
  createSkewYMatrix: () => ts,
  createTranslateMatrix: () => ke,
  createVector: () => sr,
  crossProduct: () => fe,
  degreesToRadians: () => I,
  dotProduct: () => Po,
  ease: () => Ba,
  enlivenObjectEnlivables: () => ur,
  enlivenObjects: () => _e,
  findScaleToCover: () => _n,
  findScaleToFit: () => xn,
  getBoundsOfCurve: () => Di,
  getOrthonormalVector: () => ns,
  getPathSegmentsInfo: () => xs,
  getPointOnPath: () => On,
  getPointer: () => Oo,
  getRandomInt: () => rh,
  getRegularPolygonPath: () => th,
  getSmoothPathFromPoints: () => Mn,
  getSvgAttributes: () => Ea,
  getUnitVector: () => Nr,
  groupSVGElements: () => $l,
  hasStyleChanged: () => ti,
  invertTransform: () => lt,
  isBetweenVectors: () => yi,
  isIdentityMatrix: () => vo,
  isTouchEvent: () => Lr,
  isTransparent: () => cn,
  joinPath: () => _s,
  loadImage: () => er,
  magnitude: () => Rr,
  makeBoundingBoxFromPoints: () => bt,
  makePathSimpler: () => Sn,
  matrixToSVG: () => Se,
  mergeClipPaths: () => eh,
  multiplyTransformMatrices: () => Y,
  multiplyTransformMatrixArray: () => Vr,
  parsePath: () => kn,
  parsePreserveAspectRatioAttribute: () => Fo,
  parseUnit: () => se,
  pick: () => ae,
  projectStrokeOnPoints: () => gn,
  qrDecompose: () => xe,
  radiansToDegrees: () => Et,
  removeFromArray: () => Qt,
  removeTransformFromObject: () => Oa,
  removeTransformMatrixForSvgParsing: () => ih,
  requestAnimFrame: () => tr,
  resetObjectTransform: () => Mo,
  rotateVector: () => ss,
  saveObjectTransform: () => rs,
  sendObjectToPlane: () => is,
  sendPointToPlane: () => Pt,
  sendVectorToPlane: () => Do,
  sin: () => xt,
  sizeAfterTransform: () => Ur,
  string: () => Sa,
  stylesFromArray: () => pn,
  stylesToArray: () => fn,
  toBlob: () => Ki,
  toDataURL: () => qi,
  toFixed: () => F,
  transformPath: () => Zl,
  transformPoint: () => N
});
function Ei(e, t) {
  let r = e.style;
  r && Object.entries(t).forEach(([i, s]) => r.setProperty(i, s));
}
var sh = class extends wo {
  constructor(e, { allowTouchScrolling: t = !1, containerClass: r = "" } = {}) {
    super(e), f(this, "upper", void 0), f(this, "container", void 0);
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
    o.classList.add(r), i.parentNode && i.parentNode.replaceChild(o, i), o.append(i, s), this.container = o;
  }
  createUpperCanvas() {
    let { el: e } = this.lower, t = Tt();
    return t.className = e.className, t.classList.remove("lower-canvas"), t.classList.add("upper-canvas"), t.setAttribute("data-fabric", "top"), t.style.cssText = e.style.cssText, t.setAttribute("draggable", "true"), t;
  }
  createContainerElement() {
    let e = we().createElement("div");
    return e.setAttribute("data-fabric", "wrapper"), Ei(e, { position: "relative" }), Ms(e), e;
  }
  applyCanvasStyle(e, t) {
    let { styles: r, allowTouchScrolling: i } = t;
    Ei(e, {
      ...r,
      "touch-action": i ? "manipulation" : $r
    }), Ms(e);
  }
  setDimensions(e, t) {
    super.setDimensions(e, t);
    let { el: r, ctx: i } = this.upper;
    bo(r, i, e, t);
  }
  setCSSDimensions(e) {
    super.setCSSDimensions(e), vi(this.upper.el, e), vi(this.container, e);
  }
  cleanupDOM(e) {
    let t = this.container, { el: r } = this.lower, { el: i } = this.upper;
    super.cleanupDOM(e), t.removeChild(i), t.removeChild(r), t.parentNode && t.parentNode.replaceChild(r, t);
  }
  dispose() {
    super.dispose(), wt().dispose(this.upper.el), delete this.upper, delete this.container;
  }
}, Dn = (e, t, r, i) => {
  let { target: s, offsetX: o, offsetY: n } = t, a = r - o, l = i - n, h = !mt(s, "lockMovementX") && s.left !== a, c = !mt(s, "lockMovementY") && s.top !== l;
  return h && s.set("left", a), c && s.set("top", l), (h || c) && fs(oo, ls(e, t, r, i)), h || c;
}, En = ho, Pn = (e) => function(t, r, i) {
  let { points: s, pathOffset: o } = i;
  return new v(s[e]).subtract(o).transform(Y(i.getViewportTransform(), i.calcTransformMatrix()));
}, An = (e, t, r, i) => {
  let { target: s, pointIndex: o } = t, n = s, a = Pt(new v(r, i), void 0, n.calcOwnMatrix());
  return n.points[o] = a.add(n.pathOffset), n.setDimensions(), n.set("dirty", !0), !0;
}, jn = (e, t) => function(r, i, s, o) {
  let n = i.target, a = new v(n.points[(e > 0 ? e : n.points.length) - 1]), l = a.subtract(n.pathOffset).transform(n.calcOwnMatrix()), h = t(r, {
    ...i,
    pointIndex: e
  }, s, o), c = a.subtract(n.pathOffset).transform(n.calcOwnMatrix()).subtract(l);
  return n.left -= c.x, n.top -= c.y, h;
}, Fn = (e) => jt(En, jn(e, An));
function oh(e, t = {}) {
  let r = {};
  for (let i = 0; i < (typeof e == "number" ? e : e.points.length); i++) r[`p${i}`] = new V({
    actionName: En,
    positionHandler: Pn(i),
    actionHandler: Fn(i),
    ...t
  });
  return r;
}
var Pi = (e, t, r) => {
  let { path: i, pathOffset: s } = e, o = i[t];
  return new v(o[r] - s.x, o[r + 1] - s.y).transform(Y(e.getViewportTransform(), e.calcTransformMatrix()));
};
function nh(e, t, r) {
  let { commandIndex: i, pointIndex: s } = this;
  return Pi(r, i, s);
}
function ah(e, t, r, i) {
  let { target: s } = t, { commandIndex: o, pointIndex: n } = this, a = ((l, h, c, u, d) => {
    let { path: g, pathOffset: p } = l, m = g[(u > 0 ? u : g.length) - 1], x = new v(m[d], m[d + 1]), _ = x.subtract(p).transform(l.calcOwnMatrix()), y = Pt(new v(h, c), void 0, l.calcOwnMatrix());
    g[u][d] = y.x + p.x, g[u][d + 1] = y.y + p.y, l.setDimensions();
    let S = x.subtract(l.pathOffset).transform(l.calcOwnMatrix()).subtract(_);
    return l.left -= S.x, l.top -= S.y, l.set("dirty", !0), !0;
  })(s, r, i, o, n);
  return a && fs(this.actionName, {
    ...ls(e, t, r, i),
    commandIndex: o,
    pointIndex: n
  }), a;
}
var Ln = class extends V {
  constructor(e) {
    super(e);
  }
  render(e, t, r, i, s) {
    let o = {
      ...i,
      cornerColor: this.controlFill,
      cornerStrokeColor: this.controlStroke,
      transparentCorners: !this.controlFill
    };
    super.render(e, t, r, o, s);
  }
}, lh = class extends Ln {
  constructor(e) {
    super(e);
  }
  render(e, t, r, i, s) {
    let { path: o } = s, { commandIndex: n, pointIndex: a, connectToCommandIndex: l, connectToPointIndex: h } = this;
    e.save(), e.strokeStyle = this.controlStroke, this.connectionDashArray && e.setLineDash(this.connectionDashArray);
    let [c] = o[n], u = Pi(s, l, h);
    if (c === "Q") {
      let d = Pi(s, n, a + 2);
      e.moveTo(d.x, d.y), e.lineTo(t, r);
    } else e.moveTo(t, r);
    e.lineTo(u.x, u.y), e.stroke(), e.restore(), super.render(e, t, r, i, s);
  }
}, pr = (e, t, r, i, s, o) => new (r ? lh : Ln)({
  commandIndex: e,
  pointIndex: t,
  actionName: "modifyPath",
  positionHandler: nh,
  actionHandler: ah,
  connectToCommandIndex: s,
  connectToPointIndex: o,
  ...i,
  ...r ? i.controlPointStyle : i.pointStyle
});
function hh(e, t = {}) {
  let r = {}, i = "M";
  return e.path.forEach((s, o) => {
    let n = s[0];
    switch (n !== "Z" && (r[`c_${o}_${n}`] = pr(o, s.length - 2, !1, t)), n) {
      case "C":
        r[`c_${o}_C_CP_1`] = pr(o, 1, !0, t, o - 1, /* @__PURE__ */ ((a) => a === "C" ? 5 : a === "Q" ? 3 : 1)(i)), r[`c_${o}_C_CP_2`] = pr(o, 3, !0, t, o, 5);
        break;
      case "Q":
        r[`c_${o}_Q_CP_1`] = pr(o, 1, !0, t, o, 3);
    }
    i = n;
  }), r;
}
var ch = hr({
  changeHeight: () => yl,
  changeObjectHeight: () => Go,
  changeObjectWidth: () => zo,
  changeWidth: () => xi,
  createObjectDefaultControls: () => ms,
  createPathControls: () => hh,
  createPolyActionHandler: () => Fn,
  createPolyControls: () => oh,
  createPolyPositionHandler: () => Pn,
  createResizeControls: () => nn,
  createTextboxDefaultControls: () => an,
  dragHandler: () => Dn,
  factoryPolyActionHandler: () => jn,
  getLocalPoint: () => qr,
  polyActionHandler: () => An,
  renderCircleControl: () => Uo,
  renderSquareControl: () => No,
  rotationStyleHandler: () => qo,
  rotationWithSnapping: () => Ko,
  scaleCursorStyleHandler: () => de,
  scaleOrSkewActionName: () => Le,
  scaleSkewCursorStyleHandler: () => re,
  scalingEqually: () => Fe,
  scalingX: () => Zo,
  scalingXOrSkewingY: () => _i,
  scalingY: () => tn,
  scalingYOrSkewingX: () => Si,
  skewCursorStyleHandler: () => en,
  skewHandlerX: () => sn,
  skewHandlerY: () => on,
  wrapWithFireEvent: () => jt,
  wrapWithFixedAnchor: () => Kt
}), Rn = class Bn extends Gr {
  constructor(...t) {
    super(...t), f(this, "_hoveredTargets", []), f(this, "_currentTransform", null), f(this, "_groupSelector", null), f(this, "contextTopDirty", !1);
  }
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Bn.ownDefaults
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
    this.elements = new sh(t, {
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
    return !this.preserveObjectStacking && t ? this._objects.filter((r) => !r.group && r !== t).concat(t) : this._objects;
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
    let r = this.getRetinaScaling(), i = Math.ceil((2 * t + 1) * r);
    this.pixelFindCanvasEl.width = this.pixelFindCanvasEl.height = i, this.pixelFindContext.scale(r, r);
  }
  isTargetTransparent(t, r, i) {
    let s = this.targetFindTolerance, o = this.pixelFindContext;
    this.clearContext(o), o.save(), o.translate(-r + s, -i + s), o.transform(...this.viewportTransform);
    let n = t.selectionBackgroundColor;
    t.selectionBackgroundColor = "", t.render(o), t.selectionBackgroundColor = n, o.restore();
    let a = Math.round(s * this.getRetinaScaling());
    return cn(o, a, a, a);
  }
  _isSelectionKeyPressed(t) {
    let r = this.selectionKey;
    return !!r && (Array.isArray(r) ? !!r.find((i) => !!i && t[i] === !0) : t[r]);
  }
  _shouldClearSelection(t, r) {
    let i = this.getActiveObjects(), s = this._activeObject;
    return !!(!r || r && s && i.length > 1 && i.indexOf(r) === -1 && s !== r && !this._isSelectionKeyPressed(t) || r && !r.evented || r && !r.selectable && s && s !== r);
  }
  _shouldCenterTransform(t, r, i) {
    if (!t) return;
    let s;
    return r === "scale" || r === "scaleX" || r === "scaleY" || r === "resizing" ? s = this.centeredScaling || t.centeredScaling : r === "rotate" && (s = this.centeredRotation || t.centeredRotation), s ? !i : i;
  }
  _getOriginFromCorner(t, r) {
    let i = r ? t.controls[r].getTransformAnchorPoint() : {
      x: t.originX,
      y: t.originY
    };
    return r && ([
      "ml",
      "tl",
      "bl"
    ].includes(r) ? i.x = pt : [
      "mr",
      "tr",
      "br"
    ].includes(r) && (i.x = H), [
      "tl",
      "mt",
      "tr"
    ].includes(r) ? i.y = so : [
      "bl",
      "mb",
      "br"
    ].includes(r) && (i.y = "top")), i;
  }
  _setupCurrentTransform(t, r, i) {
    var s;
    let o = r.group ? Pt(this.getScenePoint(t), void 0, r.group.calcTransformMatrix()) : this.getScenePoint(t), { key: n = "", control: a } = r.getActiveControl() || {}, l = i && a ? (s = a.getActionHandler(t, r, a)) == null ? void 0 : s.bind(a) : Dn, h = ((k, D, B, A) => {
      if (!D || !k) return "drag";
      let E = A.controls[D];
      return E.getActionName(B, E, A);
    })(i, n, t, r), c = t[this.centeredKey], u = this._shouldCenterTransform(r, h, c) ? {
      x: L,
      y: L
    } : this._getOriginFromCorner(r, n), { scaleX: d, scaleY: g, skewX: p, skewY: m, left: x, top: _, angle: y, width: S, height: C, cropX: b, cropY: O } = r, T = {
      target: r,
      action: h,
      actionHandler: l,
      actionPerformed: !1,
      corner: n,
      scaleX: d,
      scaleY: g,
      skewX: p,
      skewY: m,
      offsetX: o.x - x,
      offsetY: o.y - _,
      originX: u.x,
      originY: u.y,
      ex: o.x,
      ey: o.y,
      lastX: o.x,
      lastY: o.y,
      theta: I(y),
      width: S,
      height: C,
      shiftKey: t.shiftKey,
      altKey: c,
      original: {
        ...rs(r),
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
    let { x: r, y: i, deltaX: s, deltaY: o } = this._groupSelector, n = new v(r, i).transform(this.viewportTransform), a = new v(r + s, i + o).transform(this.viewportTransform), l = this.selectionLineWidth / 2, h = Math.min(n.x, a.x), c = Math.min(n.y, a.y), u = Math.max(n.x, a.x), d = Math.max(n.y, a.y);
    this.selectionColor && (t.fillStyle = this.selectionColor, t.fillRect(h, c, u - h, d - c)), this.selectionLineWidth && this.selectionBorderColor && (t.lineWidth = this.selectionLineWidth, t.strokeStyle = this.selectionBorderColor, h += l, c += l, u -= l, d -= l, q.prototype._setLineDash.call(this, t, this.selectionDashArray), t.strokeRect(h, c, u - h, d - c));
  }
  findTarget(t) {
    if (this._targetInfo) return this._targetInfo;
    if (this.skipTargetFind) return {
      subTargets: [],
      currentSubTargets: []
    };
    let r = this.getScenePoint(t), i = this._activeObject, s = this.getActiveObjects(), o = this.searchPossibleTargets(this._objects, r), { subTargets: n, container: a, target: l } = o, h = {
      ...o,
      currentSubTargets: n,
      currentContainer: a,
      currentTarget: l
    };
    if (!i) return h;
    let c = {
      ...this.searchPossibleTargets([i], r),
      currentSubTargets: n,
      currentContainer: a,
      currentTarget: l
    };
    return i.findControl(this.getViewportPoint(t), Lr(t)) ? {
      ...c,
      target: i
    } : c.target && (s.length > 1 || !this.preserveObjectStacking || this.preserveObjectStacking && t[this.altSelectionKey]) ? c : h;
  }
  _pointIsInObjectSelectionArea(t, r) {
    let i = t.getCoords(), s = this.getZoom(), o = t.padding / s;
    if (o) {
      let [n, a, l, h] = i, c = Math.atan2(a.y - n.y, a.x - n.x), u = yt(c) * o, d = xt(c) * o, g = u + d, p = u - d;
      i = [
        new v(n.x - p, n.y - g),
        new v(a.x + g, a.y - p),
        new v(l.x + p, l.y + g),
        new v(h.x - g, h.y + p)
      ];
    }
    return rr.isPointInPolygon(r, i);
  }
  _checkTarget(t, r) {
    if (t && t.visible && t.evented && this._pointIsInObjectSelectionArea(t, r)) {
      if (!this.perPixelTargetFind && !t.perPixelTargetFind || t.isEditing) return !0;
      {
        let i = r.transform(this.viewportTransform);
        if (!this.isTargetTransparent(t, i.x, i.y)) return !0;
      }
    }
    return !1;
  }
  _searchPossibleTargets(t, r, i) {
    let s = t.length;
    for (; s--; ) {
      let o = t[s];
      if (this._checkTarget(o, r)) {
        if (kr(o) && o.subTargetCheck) {
          let { target: n } = this._searchPossibleTargets(o._objects, r, i);
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
  searchPossibleTargets(t, r) {
    let i = this._searchPossibleTargets(t, r, []);
    i.container = i.target;
    let { container: s, subTargets: o } = i;
    if (s && kr(s) && s.interactive && o[0]) {
      for (let n = o.length - 1; n > 0; n--) {
        let a = o[n];
        if (!kr(a) || !a.interactive) return i.target = a, i;
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
  _getPointerImpl(t, r = !1) {
    let i = this.upperCanvasEl, s = i.getBoundingClientRect(), o = Oo(t), n = s.width || 0, a = s.height || 0;
    n && a || ("top" in s && "bottom" in s && (a = Math.abs(s.top - s.bottom)), "right" in s && "left" in s && (n = Math.abs(s.right - s.left))), this.calcOffset(), o.x -= this._offset.left, o.y -= this._offset.top, r || (o = Pt(o, void 0, this.viewportTransform));
    let l = this.getRetinaScaling();
    l !== 1 && (o.x /= l, o.y /= l);
    let h = n === 0 || a === 0 ? new v(1, 1) : new v(i.width / n, i.height / a);
    return o.multiply(h);
  }
  _setDimensionsImpl(t, r) {
    this._resetTransformEventData(), super._setDimensionsImpl(t, r), this._isCurrentlyDrawing && this.freeDrawingBrush && this.freeDrawingBrush._setBrushStyles(this.contextTop);
  }
  _createCacheCanvas() {
    this.pixelFindCanvasEl = Tt(), this.pixelFindContext = this.pixelFindCanvasEl.getContext("2d", { willReadFrequently: !0 }), this.setTargetFindTolerance(this.targetFindTolerance);
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
    return Zt(t) ? t.getObjects() : t ? [t] : [];
  }
  _fireSelectionEvents(t, r) {
    let i = !1, s = !1, o = this.getActiveObjects(), n = [], a = [];
    t.forEach((l) => {
      o.includes(l) || (i = !0, l.fire("deselected", {
        e: r,
        target: l
      }), a.push(l));
    }), o.forEach((l) => {
      t.includes(l) || (i = !0, l.fire("selected", {
        e: r,
        target: l
      }), n.push(l));
    }), t.length > 0 && o.length > 0 ? (s = !0, i && this.fire("selection:updated", {
      e: r,
      selected: n,
      deselected: a
    })) : o.length > 0 ? (s = !0, this.fire("selection:created", {
      e: r,
      selected: n
    })) : t.length > 0 && (s = !0, this.fire("selection:cleared", {
      e: r,
      deselected: a
    })), s && (this._objectsToRender = void 0);
  }
  setActiveObject(t, r) {
    let i = this.getActiveObjects(), s = this._setActiveObject(t, r);
    return this._fireSelectionEvents(i, r), s;
  }
  _setActiveObject(t, r) {
    let i = this._activeObject;
    return i !== t && !(!this._discardActiveObject(r, t) && this._activeObject) && !t.onSelect({ e: r }) && (this._activeObject = t, Zt(t) && i !== t && t.set("canvas", this), t.setCoords(), !0);
  }
  _discardActiveObject(t, r) {
    let i = this._activeObject;
    return !!i && !i.onDeselect({
      e: t,
      object: r
    }) && (this._currentTransform && this._currentTransform.target === i && this.endCurrentTransform(t), Zt(i) && i === this._hoveredTarget && (this._hoveredTarget = void 0), this._activeObject = void 0, !0);
  }
  discardActiveObject(t) {
    let r = this.getActiveObjects(), i = this.getActiveObject();
    r.length && this.fire("before:selection:cleared", {
      e: t,
      deselected: [i]
    });
    let s = this._discardActiveObject(t);
    return this._fireSelectionEvents(r, t), s;
  }
  endCurrentTransform(t) {
    let r = this._currentTransform;
    this._finalizeCurrentTransform(t), r && r.target && (r.target.isMoving = !1), this._currentTransform = null;
  }
  _finalizeCurrentTransform(t) {
    let r = this._currentTransform, i = r.target, s = {
      e: t,
      target: i,
      transform: r,
      action: r.action
    };
    i._scaling && (i._scaling = !1), i.setCoords(), r.actionPerformed && (this.fire("object:modified", s), i.fire(uo, s));
  }
  setViewportTransform(t) {
    super.setViewportTransform(t);
    let r = this._activeObject;
    r && r.setCoords();
  }
  destroy() {
    let t = this._activeObject;
    Zt(t) && (t.removeAll(), t.dispose()), delete this._activeObject, super.destroy(), this.pixelFindContext = null, this.pixelFindCanvasEl = void 0;
  }
  clear() {
    this.discardActiveObject(), this._activeObject = void 0, this.clearContext(this.contextTop), super.clear();
  }
  drawControls(t) {
    let r = this._activeObject;
    r && r._renderControls(t);
  }
  _toObject(t, r, i) {
    let s = this._realizeGroupTransformOnObject(t), o = super._toObject(t, r, i);
    return t.set(s), o;
  }
  _realizeGroupTransformOnObject(t) {
    let { group: r } = t;
    if (r && Zt(r) && this._activeObject === r) {
      let i = ae(t, [
        "angle",
        "flipX",
        "flipY",
        H,
        Nt,
        qt,
        Te,
        Oe,
        "top"
      ]);
      return ko(t, r.calcOwnMatrix()), i;
    }
    return {};
  }
  _setSVGObject(t, r, i) {
    let s = this._realizeGroupTransformOnObject(r);
    super._setSVGObject(t, r, i), r.set(s);
  }
};
f(Rn, "ownDefaults", {
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
var uh = class {
  constructor(e) {
    f(this, "targets", []), f(this, "__disposer", void 0);
    let t = () => {
      let { hiddenTextarea: i } = e.getActiveObject() || {};
      i && i.focus();
    }, r = e.upperCanvasEl;
    r.addEventListener("click", t), this.__disposer = () => r.removeEventListener("click", t);
  }
  exitTextEditing() {
    this.target = void 0, this.targets.forEach((e) => {
      e.isEditing && e.exitEditing();
    });
  }
  add(e) {
    this.targets.push(e);
  }
  remove(e) {
    this.unregister(e), Qt(this.targets, e);
  }
  register(e) {
    this.target = e;
  }
  unregister(e) {
    e === this.target && (this.target = void 0);
  }
  onMouseMove(e) {
    var t;
    (t = this.target) != null && t.isEditing && this.target.updateSelectionOnMouseMove(e);
  }
  clear() {
    this.targets = [], this.target = void 0;
  }
  dispose() {
    this.clear(), this.__disposer(), delete this.__disposer;
  }
}, nt = { passive: !1 }, ce = (e, t) => ({
  viewportPoint: e.getViewportPoint(t),
  scenePoint: e.getScenePoint(t)
}), It = (e, ...t) => e.addEventListener(...t), ct = (e, ...t) => e.removeEventListener(...t), dh = {
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
}, Ai = class extends Rn {
  constructor(e, t = {}) {
    super(e, t), f(this, "_isClick", void 0), f(this, "textEditingManager", new uh(this)), [
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
    ].forEach((r) => {
      this[r] = this[r].bind(this);
    }), this.addOrRemove(It);
  }
  _getEventPrefix() {
    return this.enablePointerEvents ? "pointer" : "mouse";
  }
  addOrRemove(e, t = !1) {
    let r = this.upperCanvasEl, i = this._getEventPrefix();
    e(Co(r), "resize", this._onResize), e(r, i + "down", this._onMouseDown), e(r, `${i}move`, this._onMouseMove, nt), e(r, `${i}out`, this._onMouseOut), e(r, `${i}enter`, this._onMouseEnter), e(r, "wheel", this._onMouseWheel, { passive: !1 }), e(r, "contextmenu", this._onContextMenu), t || (e(r, "click", this._onClick), e(r, "dblclick", this._onClick)), e(r, "dragstart", this._onDragStart), e(r, "dragend", this._onDragEnd), e(r, "dragover", this._onDragOver), e(r, "dragenter", this._onDragEnter), e(r, "dragleave", this._onDragLeave), e(r, "drop", this._onDrop), this.enablePointerEvents || e(r, "touchstart", this._onTouchStart, nt);
  }
  removeListeners() {
    this.addOrRemove(ct);
    let e = this._getEventPrefix(), t = gt(this.upperCanvasEl);
    ct(t, `${e}up`, this._onMouseUp), ct(t, "touchend", this._onTouchEnd, nt), ct(t, `${e}move`, this._onMouseMove, nt), ct(t, "touchmove", this._onMouseMove, nt), clearTimeout(this._willAddMouseDown);
  }
  _onMouseWheel(e) {
    this._cacheTransformEventData(e), this._handleEvent(e, "wheel"), this._resetTransformEventData();
  }
  _onMouseOut(e) {
    let t = this._hoveredTarget, r = {
      e,
      ...ce(this, e)
    };
    this.fire("mouse:out", {
      ...r,
      target: t
    }), this._hoveredTarget = void 0, t && t.fire("mouseout", { ...r }), this._hoveredTargets.forEach((i) => {
      this.fire("mouse:out", {
        ...r,
        target: i
      }), i && i.fire("mouseout", { ...r });
    }), this._hoveredTargets = [];
  }
  _onMouseEnter(e) {
    let { target: t } = this.findTarget(e);
    this._currentTransform || t || (this.fire("mouse:over", {
      e,
      ...ce(this, e)
    }), this._hoveredTarget = void 0, this._hoveredTargets = []);
  }
  _onDragStart(e) {
    this._isClick = !1;
    let t = this.getActiveObject();
    if (t && t.onDragStart(e)) {
      this._dragSource = t;
      let r = {
        e,
        target: t
      };
      this.fire("dragstart", r), t.fire("dragstart", r), It(this.upperCanvasEl, "drag", this._onDragProgress);
      return;
    }
    Ds(e);
  }
  _renderDragEffects(e, t, r) {
    let i = !1, s = this._dropTarget;
    s && s !== t && s !== r && (s.clearContextTop(), i = !0), t?.clearContextTop(), r !== t && r?.clearContextTop();
    let o = this.contextTop;
    o.save(), o.transform(...this.viewportTransform), t && (o.save(), t.transform(o), t.renderDragSourceEffect(e), o.restore(), i = !0), r && (o.save(), r.transform(o), r.renderDropTargetEffect(e), o.restore(), i = !0), o.restore(), i && (this.contextTopDirty = !0);
  }
  _onDragEnd(e) {
    let { currentSubTargets: t } = this.findTarget(e), r = !!e.dataTransfer && e.dataTransfer.dropEffect !== "none", i = r ? this._activeObject : void 0, s = {
      e,
      target: this._dragSource,
      subTargets: t,
      dragSource: this._dragSource,
      didDrop: r,
      dropTarget: i
    };
    ct(this.upperCanvasEl, "drag", this._onDragProgress), this.fire("dragend", s), this._dragSource && this._dragSource.fire("dragend", s), delete this._dragSource, this._onMouseUp(e);
  }
  _onDragProgress(e) {
    let t = {
      e,
      target: this._dragSource,
      dragSource: this._dragSource,
      dropTarget: this._draggedoverTarget
    };
    this.fire("drag", t), this._dragSource && this._dragSource.fire("drag", t);
  }
  _onDragOver(e) {
    let t = "dragover", { currentContainer: r, currentSubTargets: i } = this.findTarget(e), s = this._dragSource, o = {
      e,
      target: r,
      subTargets: i,
      dragSource: s,
      canDrop: !1,
      dropTarget: void 0
    }, n;
    this.fire(t, o), this._fireEnterLeaveEvents(e, r, o), r && (r.canDrop(e) && (n = r), r.fire(t, o));
    for (let a = 0; a < i.length; a++) {
      let l = i[a];
      l.canDrop(e) && (n = l), l.fire(t, o);
    }
    this._renderDragEffects(e, s, n), this._dropTarget = n;
  }
  _onDragEnter(e) {
    let { currentContainer: t, currentSubTargets: r } = this.findTarget(e), i = {
      e,
      target: t,
      subTargets: r,
      dragSource: this._dragSource
    };
    this.fire("dragenter", i), this._fireEnterLeaveEvents(e, t, i);
  }
  _onDragLeave(e) {
    let { currentSubTargets: t } = this.findTarget(e), r = {
      e,
      target: this._draggedoverTarget,
      subTargets: t,
      dragSource: this._dragSource
    };
    this.fire("dragleave", r), this._fireEnterLeaveEvents(e, void 0, r), this._renderDragEffects(e, this._dragSource), this._dropTarget = void 0, this._hoveredTargets = [];
  }
  _onDrop(e) {
    let { currentContainer: t, currentSubTargets: r } = this.findTarget(e), i = this._basicEventHandler("drop:before", {
      e,
      target: t,
      subTargets: r,
      dragSource: this._dragSource,
      ...ce(this, e)
    });
    i.didDrop = !1, i.dropTarget = void 0, this._basicEventHandler("drop", i), this.fire("drop:after", i);
  }
  _onContextMenu(e) {
    let { target: t, subTargets: r } = this.findTarget(e), i = this._basicEventHandler("contextmenu:before", {
      e,
      target: t,
      subTargets: r
    });
    return this.stopContextMenu && Ds(e), this._basicEventHandler("contextmenu", i), !1;
  }
  _onClick(e) {
    let t = e.detail;
    t > 3 || t < 2 || (this._cacheTransformEventData(e), t == 2 && e.type === "dblclick" && this._handleEvent(e, "dblclick"), t == 3 && this._handleEvent(e, "tripleclick"), this._resetTransformEventData());
  }
  fireEventFromPointerEvent(e, t, r, i = {}) {
    this._cacheTransformEventData(e);
    let { target: s, subTargets: o } = this.findTarget(e), n = {
      e,
      target: s,
      subTargets: o,
      ...ce(this, e),
      transform: this._currentTransform,
      ...i
    };
    this.fire(t, n), s && s.fire(r, n);
    for (let a = 0; a < o.length; a++) o[a] !== s && o[a].fire(r, n);
    this._resetTransformEventData();
  }
  getPointerId(e) {
    let t = e.changedTouches;
    return t ? t[0] && t[0].identifier : this.enablePointerEvents ? e.pointerId : -1;
  }
  _isMainEvent(e) {
    return e.isPrimary === !0 || e.isPrimary !== !1 && (e.type === "touchend" && e.touches.length === 0 || !e.changedTouches || e.changedTouches[0].identifier === this.mainTouchId);
  }
  _onTouchStart(e) {
    this._cacheTransformEventData(e);
    let t = !this.allowTouchScrolling, r = this._activeObject;
    this.mainTouchId === void 0 && (this.mainTouchId = this.getPointerId(e)), this.__onMouseDown(e);
    let { target: i } = this.findTarget(e);
    (this.isDrawingMode || r && i === r) && (t = !0), t && e.preventDefault();
    let s = this.upperCanvasEl, o = this._getEventPrefix(), n = gt(s);
    It(n, "touchend", this._onTouchEnd, nt), t && It(n, "touchmove", this._onMouseMove, nt), ct(s, `${o}down`, this._onMouseDown), this._resetTransformEventData();
  }
  _onMouseDown(e) {
    this._cacheTransformEventData(e), this.__onMouseDown(e);
    let t = this.upperCanvasEl, r = this._getEventPrefix();
    ct(t, `${r}move`, this._onMouseMove, nt);
    let i = gt(t);
    It(i, `${r}up`, this._onMouseUp), It(i, `${r}move`, this._onMouseMove, nt), this._resetTransformEventData();
  }
  _onTouchEnd(e) {
    if (e.touches.length > 0) return;
    this._cacheTransformEventData(e), this.__onMouseUp(e), this._resetTransformEventData(), delete this.mainTouchId;
    let t = this._getEventPrefix(), r = gt(this.upperCanvasEl);
    ct(r, "touchend", this._onTouchEnd, nt), ct(r, "touchmove", this._onMouseMove, nt), this._willAddMouseDown && clearTimeout(this._willAddMouseDown), this._willAddMouseDown = setTimeout(() => {
      It(this.upperCanvasEl, `${t}down`, this._onMouseDown), this._willAddMouseDown = 0;
    }, 400);
  }
  _onMouseUp(e) {
    this._cacheTransformEventData(e), this.__onMouseUp(e);
    let t = this.upperCanvasEl, r = this._getEventPrefix();
    if (this._isMainEvent(e)) {
      let i = gt(this.upperCanvasEl);
      ct(i, `${r}up`, this._onMouseUp), ct(i, `${r}move`, this._onMouseMove, nt), It(t, `${r}move`, this._onMouseMove, nt);
    }
    this._resetTransformEventData();
  }
  _onMouseMove(e) {
    this._cacheTransformEventData(e);
    let t = this.getActiveObject();
    !this.allowTouchScrolling && (!t || !t.shouldStartDragging(e)) && e.preventDefault && e.preventDefault(), this.__onMouseMove(e), this._resetTransformEventData();
  }
  _onResize() {
    this.calcOffset(), this._resetTransformEventData();
  }
  _shouldRender(e) {
    let t = this.getActiveObject();
    return !!t != !!e || t && e && t !== e;
  }
  __onMouseUp(e) {
    var t;
    this._handleEvent(e, "up:before");
    let r = this._currentTransform, i = this._isClick, { target: s } = this.findTarget(e), { button: o } = e;
    if (o) return void ((this.fireMiddleClick && o === 1 || this.fireRightClick && o === 2) && this._handleEvent(e, "up"));
    if (this.isDrawingMode && this._isCurrentlyDrawing) return void this._onMouseUpInDrawingMode(e);
    if (!this._isMainEvent(e)) return;
    let n, a, l = !1;
    if (r && (this._finalizeCurrentTransform(e), l = r.actionPerformed), !i) {
      let h = s === this._activeObject;
      this.handleSelection(e), l || (l = this._shouldRender(s) || !h && s === this._activeObject);
    }
    if (s) {
      let { key: h, control: c } = s.findControl(this.getViewportPoint(e), Lr(e)) || {};
      if (a = h, s.selectable && s !== this._activeObject && s.activeOn === "up") this.setActiveObject(s, e), l = !0;
      else if (c) {
        let u = c.getMouseUpHandler(e, s, c);
        u && (n = this.getScenePoint(e), u.call(c, e, r, n.x, n.y));
      }
      s.isMoving = !1;
    }
    if (r && (r.target !== s || r.corner !== a)) {
      let h = r.target && r.target.controls[r.corner], c = h && h.getMouseUpHandler(e, r.target, h);
      n = n || this.getScenePoint(e), c && c.call(h, e, r, n.x, n.y);
    }
    this._setCursorFromEvent(e, s), this._handleEvent(e, "up"), this._groupSelector = null, this._currentTransform = null, s && (s.__corner = void 0), l ? this.requestRenderAll() : i || (t = this._activeObject) != null && t.isEditing || this.renderTop();
  }
  _basicEventHandler(e, t) {
    let { target: r, subTargets: i = [] } = t;
    this.fire(e, t), r && r.fire(e, t);
    for (let s = 0; s < i.length; s++) i[s] !== r && i[s].fire(e, t);
    return t;
  }
  _handleEvent(e, t, r) {
    let { target: i, subTargets: s } = this.findTarget(e), o = {
      e,
      target: i,
      subTargets: s,
      ...ce(this, e),
      transform: this._currentTransform,
      ...t === "down:before" || t === "down" ? r : {}
    };
    t !== "up:before" && t !== "up" || (o.isClick = this._isClick), this.fire(`mouse:${t}`, o), i && i.fire(`mouse${t}`, o);
    for (let n = 0; n < s.length; n++) s[n] !== i && s[n].fire(`mouse${t}`, o);
  }
  _onMouseDownInDrawingMode(e) {
    this._isCurrentlyDrawing = !0, this.getActiveObject() && (this.discardActiveObject(e), this.requestRenderAll());
    let t = this.getScenePoint(e);
    this.freeDrawingBrush && this.freeDrawingBrush.onMouseDown(t, {
      e,
      pointer: t
    }), this._handleEvent(e, "down", { alreadySelected: !1 });
  }
  _onMouseMoveInDrawingMode(e) {
    if (this._isCurrentlyDrawing) {
      let t = this.getScenePoint(e);
      this.freeDrawingBrush && this.freeDrawingBrush.onMouseMove(t, {
        e,
        pointer: t
      });
    }
    this.setCursor(this.freeDrawingCursor), this._handleEvent(e, "move");
  }
  _onMouseUpInDrawingMode(e) {
    let t = this.getScenePoint(e);
    this.freeDrawingBrush ? this._isCurrentlyDrawing = !!this.freeDrawingBrush.onMouseUp({
      e,
      pointer: t
    }) : this._isCurrentlyDrawing = !1, this._handleEvent(e, "up");
  }
  __onMouseDown(e) {
    this._isClick = !0, this._handleEvent(e, "down:before");
    let { target: t } = this.findTarget(e), r = !!t && t === this._activeObject, { button: i } = e;
    if (i) return void ((this.fireMiddleClick && i === 1 || this.fireRightClick && i === 2) && this._handleEvent(e, "down", { alreadySelected: r }));
    if (this.isDrawingMode) return void this._onMouseDownInDrawingMode(e);
    if (!this._isMainEvent(e) || this._currentTransform) return;
    let s = this._shouldRender(t), o = !1;
    if (this.handleMultiSelection(e, t) ? (t = this._activeObject, o = !0, s = !0) : this._shouldClearSelection(e, t) && this.discardActiveObject(e), this.selection && (!t || !t.selectable && !t.isEditing && t !== this._activeObject)) {
      let n = this.getScenePoint(e);
      this._groupSelector = {
        x: n.x,
        y: n.y,
        deltaY: 0,
        deltaX: 0
      };
    }
    if (r = !!t && t === this._activeObject, t) {
      t.selectable && t.activeOn === "down" && this.setActiveObject(t, e);
      let n = t.findControl(this.getViewportPoint(e), Lr(e));
      if (t === this._activeObject && (n || !o)) {
        this._setupCurrentTransform(e, t, r);
        let a = n ? n.control : void 0, l = this.getScenePoint(e), h = a && a.getMouseDownHandler(e, t, a);
        h && h.call(a, e, this._currentTransform, l.x, l.y);
      }
    }
    s && (this._objectsToRender = void 0), this._handleEvent(e, "down", { alreadySelected: r }), s && this.requestRenderAll();
  }
  _resetTransformEventData() {
    this._targetInfo = this._viewportPoint = this._scenePoint = void 0;
  }
  _cacheTransformEventData(e) {
    this._resetTransformEventData(), this._viewportPoint = this.getViewportPoint(e), this._scenePoint = Pt(this._viewportPoint, void 0, this.viewportTransform), this._targetInfo = this.findTarget(e), this._currentTransform && (this._targetInfo.target = this._currentTransform.target);
  }
  __onMouseMove(e) {
    if (this._isClick = !1, this._handleEvent(e, "move:before"), this.isDrawingMode) return void this._onMouseMoveInDrawingMode(e);
    if (!this._isMainEvent(e)) return;
    let t = this._groupSelector;
    if (t) {
      let r = this.getScenePoint(e);
      t.deltaX = r.x - t.x, t.deltaY = r.y - t.y, this.renderTop();
    } else if (this._currentTransform) this._transformObject(e);
    else {
      let { target: r } = this.findTarget(e);
      this._setCursorFromEvent(e, r), this._fireOverOutEvents(e, r);
    }
    this.textEditingManager.onMouseMove(e), this._handleEvent(e, "move");
  }
  _fireOverOutEvents(e, t) {
    let { _hoveredTarget: r, _hoveredTargets: i } = this, { subTargets: s, currentTarget: o } = this.findTarget(e), n = Math.max(i.length, s.length);
    this.fireSyntheticInOutEvents("mouse", {
      e,
      target: t,
      oldTarget: r,
      actualTarget: o,
      oldActualTarget: this._hoveredActualTarget,
      fireCanvas: !0
    });
    for (let a = 0; a < n; a++) s[a] === t || i[a] && i[a] === r || this.fireSyntheticInOutEvents("mouse", {
      e,
      target: s[a],
      oldTarget: i[a]
    });
    this._hoveredActualTarget = o, this._hoveredTarget = t, this._hoveredTargets = s;
  }
  _fireEnterLeaveEvents(e, t, r) {
    let i = this._draggedoverTarget, s = this._hoveredTargets, { subTargets: o } = this.findTarget(e), n = Math.max(s.length, o.length);
    this.fireSyntheticInOutEvents("drag", {
      ...r,
      target: t,
      oldTarget: i,
      fireCanvas: !0
    });
    for (let a = 0; a < n; a++) this.fireSyntheticInOutEvents("drag", {
      ...r,
      target: o[a],
      oldTarget: s[a]
    });
    this._draggedoverTarget = t;
  }
  fireSyntheticInOutEvents(e, { target: t, oldTarget: r, actualTarget: i, oldActualTarget: s, fireCanvas: o, e: n, ...a }) {
    let { targetIn: l, targetOut: h, canvasIn: c, canvasOut: u } = dh[e], d = r !== t, g = s !== i, p = t && d, m = i && g, x = r && d, _ = s && g, y = {
      ...a,
      e: n,
      ...ce(this, n)
    }, S = {
      ...y,
      target: r,
      nextTarget: t,
      actualTarget: s,
      nextActualTarget: i
    };
    (x || _) && o && this.fire(u, S), x && r.fire(h, S), _ && r !== s && s.fire(h, S);
    let C = {
      ...y,
      target: t,
      previousTarget: r,
      actualTarget: i,
      previousActualTarget: s
    };
    (p || m) && o && this.fire(c, C), p && t.fire(l, C), m && i !== t && i.fire(l, C);
  }
  _transformObject(e) {
    let t = this.getScenePoint(e), r = this._currentTransform, i = r.target, s = i.group ? Pt(t, void 0, i.group.calcTransformMatrix()) : t;
    r.shiftKey = e.shiftKey, r.altKey = !!this.centeredKey && e[this.centeredKey], this._performTransformAction(e, r, s), r.actionPerformed && this.requestRenderAll();
  }
  _performTransformAction(e, t, r) {
    let { action: i, actionHandler: s, target: o } = t, n = !!s && s(e, t, r.x, r.y);
    n && o.setCoords(), i === "drag" && n && (t.target.isMoving = !0, this.setCursor(t.target.moveCursor || this.moveCursor)), t.actionPerformed = t.actionPerformed || n;
  }
  _setCursorFromEvent(e, t) {
    if (!t) return void this.setCursor(this.defaultCursor);
    let r = t.hoverCursor || this.hoverCursor, i = Zt(this._activeObject) ? this._activeObject : null, s = (!i || t.group !== i) && t.findControl(this.getViewportPoint(e));
    if (s) {
      let { control: o, coord: n } = s;
      this.setCursor(o.cursorStyleHandler(e, o, t, n));
    } else {
      if (t.subTargetCheck) {
        let { subTargets: o } = this.findTarget(e);
        o.concat().reverse().forEach((n) => {
          r = n.hoverCursor || r;
        });
      }
      this.setCursor(r);
    }
  }
  handleMultiSelection(e, t) {
    let r = this._activeObject, i = Zt(r);
    if (r && this._isSelectionKeyPressed(e) && this.selection && t && t.selectable && (r !== t || i) && (i || !t.isDescendantOf(r) && !r.isDescendantOf(t)) && !t.onSelect({ e }) && !r.getActiveControl()) {
      if (i) {
        let s = r.getObjects(), o = [];
        if (t === r) {
          let n = this.getScenePoint(e), a = this.searchPossibleTargets(s, n);
          if (a.target ? (t = a.target, o = a.subTargets) : (a = this.searchPossibleTargets(this._objects, n), t = a.target, o = a.subTargets), !t || !t.selectable) return !1;
        }
        t.group === r ? (r.remove(t), this._hoveredTarget = t, this._hoveredTargets = o, r.size() === 1 && this._setActiveObject(r.item(0), e)) : (r.multiSelectAdd(t), this._hoveredTarget = r, this._hoveredTargets = o), this._fireSelectionEvents(s, e);
      } else {
        r.isEditing && r.exitEditing();
        let s = new (w.getClass("ActiveSelection"))([], { canvas: this });
        s.multiSelectAdd(r, t), this._hoveredTarget = s, this._setActiveObject(s, e), this._fireSelectionEvents([r], e);
      }
      return !0;
    }
    return !1;
  }
  handleSelection(e) {
    if (!this.selection || !this._groupSelector) return !1;
    let { x: t, y: r, deltaX: i, deltaY: s } = this._groupSelector, o = new v(t, r), n = o.add(new v(i, s)), a = o.min(n), l = o.max(n).subtract(a), h = this.collectObjects({
      left: a.x,
      top: a.y,
      width: l.x,
      height: l.y
    }, { includeIntersecting: !this.selectionFullyContained }), c = o.eq(n) ? h[0] ? [h[0]] : [] : h.length > 1 ? h.filter((u) => !u.onSelect({ e })).reverse() : h;
    if (c.length === 1) this.setActiveObject(c[0], e);
    else if (c.length > 1) {
      let u = w.getClass("ActiveSelection");
      this.setActiveObject(new u(c, { canvas: this }), e);
    }
    return this._groupSelector = null, !0;
  }
  toCanvasElement(e = 1, t) {
    let { upper: r } = this.elements;
    r.ctx = void 0;
    let i = super.toCanvasElement(e, t);
    return r.ctx = r.el.getContext("2d"), i;
  }
  clear() {
    this.textEditingManager.clear(), super.clear();
  }
  destroy() {
    this.removeListeners(), this.textEditingManager.dispose(), super.destroy();
  }
}, In = {
  x1: 0,
  y1: 0,
  x2: 0,
  y2: 0
}, gh = {
  ...In,
  r1: 0,
  r2: 0
}, ge = (e, t) => isNaN(e) && typeof t == "number" ? t : e;
function Xn(e) {
  return e && /%$/.test(e) && Number.isFinite(parseFloat(e));
}
function Yn(e, t) {
  return oe(0, ge(typeof e == "number" ? e : typeof e == "string" ? parseFloat(e) / (Xn(e) ? 100 : 1) : NaN, t), 1);
}
var fh = /\s*;\s*/, ph = /\s*:\s*/;
function mh(e, t) {
  let r, i, s = e.getAttribute("style");
  if (s) {
    let n = s.split(fh);
    n[n.length - 1] === "" && n.pop();
    for (let a = n.length; a--; ) {
      let [l, h] = n[a].split(ph).map((c) => c.trim());
      l === "stop-color" ? r = h : l === "stop-opacity" && (i = h);
    }
  }
  r = r || e.getAttribute("stop-color") || "rgb(0,0,0)", i = ge(parseFloat(i || e.getAttribute("stop-opacity") || ""), 1);
  let o = new K(r);
  return o.setAlpha(o.getAlpha() * i * t), {
    offset: Yn(e.getAttribute("offset"), 0),
    color: o.toRgba()
  };
}
function vh(e, t) {
  let r = [], i = e.getElementsByTagName("stop"), s = Yn(t, 1);
  for (let o = i.length; o--; ) r.push(mh(i[o], s));
  return r;
}
function $n(e) {
  return e.nodeName === "linearGradient" || e.nodeName === "LINEARGRADIENT" ? "linear" : "radial";
}
function Wn(e) {
  return e.getAttribute("gradientUnits") === "userSpaceOnUse" ? "pixels" : "percentage";
}
function dt(e, t) {
  return e.getAttribute(t);
}
function yh(e, t) {
  return (function(r, { width: i, height: s, gradientUnits: o }) {
    let n;
    return Object.entries(r).reduce((a, [l, h]) => {
      if (h === "Infinity") n = 1;
      else if (h === "-Infinity") n = 0;
      else {
        let c = typeof h == "string";
        n = c ? parseFloat(h) : h, c && Xn(h) && (n *= 0.01, o === "pixels" && (l !== "x1" && l !== "x2" && l !== "r2" || (n *= i), l !== "y1" && l !== "y2" || (n *= s)));
      }
      return a[l] = n, a;
    }, {});
  })($n(e) === "linear" ? (function(r) {
    return {
      x1: dt(r, "x1") || 0,
      y1: dt(r, "y1") || 0,
      x2: dt(r, "x2") || "100%",
      y2: dt(r, "y2") || 0
    };
  })(e) : (function(r) {
    return {
      x1: dt(r, "fx") || dt(r, "cx") || "50%",
      y1: dt(r, "fy") || dt(r, "cy") || "50%",
      r1: 0,
      x2: dt(r, "cx") || "50%",
      y2: dt(r, "cy") || "50%",
      r2: dt(r, "r") || "50%"
    };
  })(e), {
    ...t,
    gradientUnits: Wn(e)
  });
}
var mr = class {
  constructor(e) {
    let { type: t = "linear", gradientUnits: r = "pixels", coords: i = {}, colorStops: s = [], offsetX: o = 0, offsetY: n = 0, gradientTransform: a, id: l } = e || {};
    Object.assign(this, {
      type: t,
      gradientUnits: r,
      coords: {
        ...t === "radial" ? gh : In,
        ...i
      },
      colorStops: s,
      offsetX: o,
      offsetY: n,
      gradientTransform: a,
      id: l ? `${l}_${Gt()}` : Gt()
    });
  }
  addColorStop(e) {
    for (let t in e) this.colorStops.push({
      offset: parseFloat(t),
      color: e[t]
    });
    return this;
  }
  toObject(e) {
    return {
      ...ae(this, e),
      type: this.type,
      coords: { ...this.coords },
      colorStops: this.colorStops.map((t) => ({ ...t })),
      offsetX: this.offsetX,
      offsetY: this.offsetY,
      gradientUnits: this.gradientUnits,
      gradientTransform: this.gradientTransform ? [...this.gradientTransform] : void 0
    };
  }
  toSVG(e, { additionalTransform: t } = {}) {
    let r = [], i = this.gradientTransform ? this.gradientTransform.concat() : et.concat(), s = this.gradientUnits === "pixels" ? "userSpaceOnUse" : "objectBoundingBox", o = this.colorStops.map((u) => ({ ...u })).sort((u, d) => u.offset - d.offset), n = -this.offsetX, a = -this.offsetY;
    var l;
    s === "objectBoundingBox" ? (n /= e.width, a /= e.height) : (n += e.width / 2, a += e.height / 2), (l = e) && typeof l._renderPathCommands == "function" && this.gradientUnits !== "percentage" && (n -= e.pathOffset.x, a -= e.pathOffset.y), i[4] -= n, i[5] -= a;
    let h = [
      `id="SVGID_${M(String(this.id))}"`,
      `gradientUnits="${s}"`,
      `gradientTransform="${t ? t + " " : ""}${Se(i)}"`,
      ""
    ].join(" "), c = (u) => parseFloat(String(u));
    if (this.type === "linear") {
      let { x1: u, y1: d, x2: g, y2: p } = this.coords, m = c(u), x = c(d), _ = c(g), y = c(p);
      r.push("<linearGradient ", h, ' x1="', m, '" y1="', x, '" x2="', _, '" y2="', y, `">
`);
    } else if (this.type === "radial") {
      let { x1: u, y1: d, x2: g, y2: p, r1: m, r2: x } = this.coords, _ = c(u), y = c(d), S = c(g), C = c(p), b = c(m), O = c(x), T = b > O;
      r.push("<radialGradient ", h, ' cx="', T ? _ : S, '" cy="', T ? y : C, '" r="', T ? b : O, '" fx="', T ? S : _, '" fy="', T ? C : y, `">
`), T && (o.reverse(), o.forEach((D) => {
        D.offset = 1 - D.offset;
      }));
      let k = Math.min(b, O);
      if (k > 0) {
        let D = k / Math.max(b, O);
        o.forEach((B) => {
          B.offset += D * (1 - B.offset);
        });
      }
    }
    return o.forEach(({ color: u, offset: d }) => {
      let g = String(u), p = Kr(g) ? g : new K(g).toRgba();
      r.push(`<stop offset="${100 * d}%" style="stop-color:${M(p)};"/>
`);
    }), r.push(this.type === "linear" ? "</linearGradient>" : "</radialGradient>", `
`), r.join("");
  }
  toLive(e) {
    let { x1: t, y1: r, x2: i, y2: s, r1: o, r2: n } = this.coords, a = this.type === "linear" ? e.createLinearGradient(t, r, i, s) : e.createRadialGradient(t, r, o, i, s, n);
    return this.colorStops.forEach(({ color: l, offset: h }) => {
      a.addColorStop(h, l);
    }), a;
  }
  static async fromObject(e) {
    let { colorStops: t, gradientTransform: r } = e;
    return new this({
      ...e,
      colorStops: t ? t.map((i) => ({ ...i })) : void 0,
      gradientTransform: r ? [...r] : void 0
    });
  }
  static fromElement(e, t, r) {
    let i = Wn(e), s = t._findCenterFromElement();
    return new this({
      id: e.getAttribute("id") || void 0,
      type: $n(e),
      coords: yh(e, {
        width: r.viewBoxWidth || r.width,
        height: r.viewBoxHeight || r.height
      }),
      colorStops: vh(e, r.opacity),
      gradientUnits: i,
      gradientTransform: bi(e.getAttribute("gradientTransform") || ""),
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
f(mr, "type", "Gradient"), w.setClass(mr, "gradient"), w.setClass(mr, "linear"), w.setClass(mr, "radial");
var li = class {
  get type() {
    return "pattern";
  }
  set type(e) {
    zt("warn", "Setting type has no effect", e);
  }
  constructor(e) {
    f(this, "repeat", "repeat"), f(this, "offsetX", 0), f(this, "offsetY", 0), f(this, "crossOrigin", ""), this.id = Gt(), Object.assign(this, e);
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
  toLive(e) {
    return this.source && (!this.isImageSource() || this.source.complete && this.source.naturalWidth !== 0 && this.source.naturalHeight !== 0) ? e.createPattern(this.source, this.repeat) : null;
  }
  toObject(e = []) {
    let { repeat: t, crossOrigin: r } = this;
    return {
      ...ae(this, e),
      type: "pattern",
      source: this.sourceToString(),
      repeat: t,
      crossOrigin: r,
      offsetX: F(this.offsetX, P.NUM_FRACTION_DIGITS),
      offsetY: F(this.offsetY, P.NUM_FRACTION_DIGITS),
      patternTransform: this.patternTransform ? [...this.patternTransform] : null
    };
  }
  toSVG({ width: e, height: t }) {
    let { source: r, repeat: i, id: s } = this, o = ge(this.offsetX / e, 0), n = ge(this.offsetY / t, 0), a = i === "repeat-y" || i === "no-repeat" ? 1 + Math.abs(o || 0) : ge(r.width / e, 0), l = i === "repeat-x" || i === "no-repeat" ? 1 + Math.abs(n || 0) : ge(r.height / t, 0);
    return [
      `<pattern id="SVGID_${M(s)}" x="${o}" y="${n}" width="${a}" height="${l}">`,
      `<image x="0" y="0" width="${r.width}" height="${r.height}" xlink:href="${M(this.sourceToString())}"></image>`,
      "</pattern>",
      ""
    ].join(`
`);
  }
  static async fromObject({ type: e, source: t, patternTransform: r, ...i }, s) {
    let o = await er(t, {
      ...s,
      crossOrigin: i.crossOrigin
    });
    return new this({
      ...i,
      patternTransform: r && r.slice(0),
      source: o
    });
  }
};
f(li, "type", "Pattern"), w.setClass(li), w.setClass(li, "pattern");
var xh = class {
  constructor(e) {
    f(this, "color", "rgb(0, 0, 0)"), f(this, "width", 1), f(this, "shadow", null), f(this, "strokeLineCap", "round"), f(this, "strokeLineJoin", "round"), f(this, "strokeMiterLimit", 10), f(this, "strokeDashArray", null), f(this, "limitedToCanvasSize", !1), this.canvas = e;
  }
  _setBrushStyles(e) {
    e.strokeStyle = this.color, e.lineWidth = this.width, e.lineCap = this.strokeLineCap, e.miterLimit = this.strokeMiterLimit, e.lineJoin = this.strokeLineJoin, e.setLineDash(this.strokeDashArray || []);
  }
  _saveAndTransform(e) {
    let t = this.canvas.viewportTransform;
    e.save(), e.transform(t[0], t[1], t[2], t[3], t[4], t[5]);
  }
  needsFullRender() {
    return new K(this.color).getAlpha() < 1 || !!this.shadow;
  }
  _setShadow() {
    if (!this.shadow || !this.canvas) return;
    let e = this.canvas, t = this.shadow, r = e.contextTop, i = e.getZoom() * e.getRetinaScaling();
    r.shadowColor = t.color, r.shadowBlur = t.blur * i, r.shadowOffsetX = t.offsetX * i, r.shadowOffsetY = t.offsetY * i;
  }
  _resetShadow() {
    let e = this.canvas.contextTop;
    e.shadowColor = "", e.shadowBlur = e.shadowOffsetX = e.shadowOffsetY = 0;
  }
  _isOutSideCanvas(e) {
    return e.x < 0 || e.x > this.canvas.getWidth() || e.y < 0 || e.y > this.canvas.getHeight();
  }
}, Wt = class Vn extends q {
  constructor(t, { path: r, left: i, top: s, ...o } = {}) {
    super(), Object.assign(this, Vn.ownDefaults), this.setOptions(o), this._setPath(t || [], !0), typeof i == "number" && this.set("left", i), typeof s == "number" && this.set("top", s);
  }
  _setPath(t, r) {
    this.path = Sn(Array.isArray(t) ? t : kn(t)), this.setBoundingBox(r);
  }
  _findCenterFromElement() {
    let t = this._calcBoundsFromPath();
    return new v(t.left + t.width / 2, t.top + t.height / 2);
  }
  _renderPathCommands(t) {
    let r = -this.pathOffset.x, i = -this.pathOffset.y;
    t.beginPath();
    for (let s of this.path) switch (s[0]) {
      case "L":
        t.lineTo(s[1] + r, s[2] + i);
        break;
      case "M":
        t.moveTo(s[1] + r, s[2] + i);
        break;
      case "C":
        t.bezierCurveTo(s[1] + r, s[2] + i, s[3] + r, s[4] + i, s[5] + r, s[6] + i);
        break;
      case "Q":
        t.quadraticCurveTo(s[1] + r, s[2] + i, s[3] + r, s[4] + i);
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
      path: this.path.map((r) => r.slice())
    };
  }
  toDatalessObject(t = []) {
    let r = this.toObject(t);
    return this.sourcePath && (delete r.path, r.sourcePath = this.sourcePath), r;
  }
  _toSVG() {
    return [
      "<path ",
      "COMMON_PARTS",
      `d="${_s(this.path, P.NUM_FRACTION_DIGITS)}" stroke-linecap="round" />
`
    ];
  }
  _getOffsetTransform() {
    let t = P.NUM_FRACTION_DIGITS;
    return ` translate(${F(-this.pathOffset.x, t)}, ${F(-this.pathOffset.y, t)})`;
  }
  toClipPathSVG(t) {
    let r = this._getOffsetTransform();
    return "	" + this._createBaseClipPathSVGMarkup(this._toSVG(), {
      reviver: t,
      additionalTransform: r
    });
  }
  toSVG(t) {
    let r = this._getOffsetTransform();
    return this._createBaseSVGMarkup(this._toSVG(), {
      reviver: t,
      additionalTransform: r
    });
  }
  complexity() {
    return this.path.length;
  }
  setDimensions() {
    this.setBoundingBox();
  }
  setBoundingBox(t) {
    let { width: r, height: i, pathOffset: s } = this._calcDimensions();
    this.set({
      width: r,
      height: i,
      pathOffset: s
    }), t && this.setPositionByOrigin(s, "center", "center");
  }
  _calcBoundsFromPath() {
    let t = [], r = 0, i = 0, s = 0, o = 0;
    for (let n of this.path) switch (n[0]) {
      case "L":
        s = n[1], o = n[2], t.push({
          x: r,
          y: i
        }, {
          x: s,
          y: o
        });
        break;
      case "M":
        s = n[1], o = n[2], r = s, i = o;
        break;
      case "C":
        t.push(...Di(s, o, n[1], n[2], n[3], n[4], n[5], n[6])), s = n[5], o = n[6];
        break;
      case "Q":
        t.push(...Di(s, o, n[1], n[2], n[1], n[2], n[3], n[4])), s = n[3], o = n[4];
        break;
      case "Z":
        s = r, o = i;
    }
    return bt(t);
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
  static async fromElement(t, r, i) {
    let { d: s, ...o } = Ft(t, this.ATTRIBUTE_NAMES, i);
    return new this(s, {
      ...o,
      ...r,
      left: void 0,
      top: void 0
    });
  }
};
f(Wt, "type", "Path"), f(Wt, "cacheProperties", [
  ...At,
  "path",
  "fillRule"
]), f(Wt, "ATTRIBUTE_NAMES", [...Jt, "d"]), w.setClass(Wt), w.setSVGClass(Wt);
var _h = class ji extends xh {
  constructor(t) {
    super(t), f(this, "decimate", 0.4), f(this, "drawStraightLine", !1), f(this, "straightLineKey", "shiftKey"), this._points = [], this._hasStraightLine = !1;
  }
  needsFullRender() {
    return super.needsFullRender() || this._hasStraightLine;
  }
  static drawSegment(t, r, i) {
    let s = r.midPointFrom(i);
    return t.quadraticCurveTo(r.x, r.y, s.x, s.y), s;
  }
  onMouseDown(t, { e: r }) {
    this.canvas._isMainEvent(r) && (this.drawStraightLine = !!this.straightLineKey && r[this.straightLineKey], this._prepareForDrawing(t), this._addPoint(t), this._render());
  }
  onMouseMove(t, { e: r }) {
    if (this.canvas._isMainEvent(r) && (this.drawStraightLine = !!this.straightLineKey && r[this.straightLineKey], (this.limitedToCanvasSize !== !0 || !this._isOutSideCanvas(t)) && this._addPoint(t) && this._points.length > 1)) if (this.needsFullRender()) this.canvas.clearContext(this.canvas.contextTop), this._render();
    else {
      let i = this._points, s = i.length, o = this.canvas.contextTop;
      this._saveAndTransform(o), this.oldEnd && (o.beginPath(), o.moveTo(this.oldEnd.x, this.oldEnd.y)), this.oldEnd = ji.drawSegment(o, i[s - 2], i[s - 1]), o.stroke(), o.restore();
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
    let r = this._points[0], i = this._points[1];
    if (this._saveAndTransform(t), t.beginPath(), this._points.length === 2 && r.x === i.x && r.y === i.y) {
      let s = this.width / 1e3;
      r.x -= s, i.x += s;
    }
    t.moveTo(r.x, r.y);
    for (let s = 1; s < this._points.length; s++) ji.drawSegment(t, r, i), r = this._points[s], i = this._points[s + 1];
    t.lineTo(r.x, r.y), t.stroke(), t.restore();
  }
  convertPointsToSVGPath(t) {
    return Mn(t, this.width / 1e3);
  }
  createPath(t) {
    let r = new Wt(t, {
      fill: null,
      stroke: this.color,
      strokeWidth: this.width,
      strokeLineCap: this.strokeLineCap,
      strokeMiterLimit: this.strokeMiterLimit,
      strokeLineJoin: this.strokeLineJoin,
      strokeDashArray: this.strokeDashArray
    });
    return this.shadow && (this.shadow.affectStroke = !0, r.shadow = new pe(this.shadow)), r;
  }
  decimatePoints(t, r) {
    if (t.length <= 2) return t;
    let i, s = t[0], o = (r / this.canvas.getZoom()) ** 2, n = t.length - 1, a = [s];
    for (let l = 1; l < n - 1; l++) i = (s.x - t[l].x) ** 2 + (s.y - t[l].y) ** 2, i >= o && (s = t[l], a.push(s));
    return a.push(t[n]), a;
  }
  _finalizeAndAddPath() {
    this.canvas.contextTop.closePath(), this.decimate && (this._points = this.decimatePoints(this._points, this.decimate));
    let t = this.convertPointsToSVGPath(this._points);
    if ((function(i) {
      return _s(i) === "M 0 0 Q 0 0 0 0 L 0 0";
    })(t)) return void this.canvas.requestRenderAll();
    let r = this.createPath(t);
    this.canvas.clearContext(this.canvas.contextTop), this.canvas.fire("before:path:created", { path: r }), this.canvas.add(r), this.canvas.requestRenderAll(), r.setCoords(), this._resetShadow(), this.canvas.fire("path:created", { path: r });
  }
}, Hn = [
  "radius",
  "startAngle",
  "endAngle",
  "counterClockwise"
], it = class Fi extends q {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Fi.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, Fi.ownDefaults), this.setOptions(t);
  }
  _set(t, r) {
    return super._set(t, r), t === "radius" && this.setRadius(r), this;
  }
  _render(t) {
    t.beginPath(), t.arc(0, 0, this.radius, I(this.startAngle), I(this.endAngle), this.counterClockwise), this._renderPaintInOrder(t);
  }
  getRadiusX() {
    return this.get("radius") * this.get(Nt);
  }
  getRadiusY() {
    return this.get("radius") * this.get(qt);
  }
  setRadius(t) {
    this.radius = t, this.set({
      width: 2 * t,
      height: 2 * t
    });
  }
  toObject(t = []) {
    return super.toObject([...Hn, ...t]);
  }
  _toSVG() {
    let { radius: t, startAngle: r, endAngle: i } = this, s = (i - r) % 360;
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
      let o = I(r), n = I(i), a = yt(o) * t, l = xt(o) * t, h = yt(n) * t, c = xt(n) * t;
      return [
        `<path d="M ${a} ${l} A ${t} ${t} 0 ${+(s > 180)} ${+!this.counterClockwise} ${h} ${c}" `,
        "COMMON_PARTS",
        ` />
`
      ];
    }
  }
  static async fromElement(t, r, i) {
    let { left: s = 0, top: o = 0, radius: n = 0, ...a } = Ft(t, this.ATTRIBUTE_NAMES, i);
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
f(it, "type", "Circle"), f(it, "cacheProperties", [...At, ...Hn]), f(it, "ownDefaults", {
  radius: 0,
  startAngle: 0,
  endAngle: 360,
  counterClockwise: !1
}), f(it, "ATTRIBUTE_NAMES", [
  "cx",
  "cy",
  "r",
  ...Jt
]), w.setClass(it), w.setSVGClass(it);
var Li = [
  "x1",
  "x2",
  "y1",
  "y2"
], kt = class zn extends q {
  constructor([t, r, i, s] = [
    0,
    0,
    0,
    0
  ], o = {}) {
    super(), Object.assign(this, zn.ownDefaults), this.setOptions(o), this.x1 = t, this.x2 = i, this.y1 = r, this.y2 = s, this._setWidthHeight();
    let { left: n, top: a } = o;
    typeof n == "number" && this.set("left", n), typeof a == "number" && this.set("top", a);
  }
  _setWidthHeight() {
    let { x1: t, y1: r, x2: i, y2: s } = this;
    this.width = Math.abs(i - t), this.height = Math.abs(s - r);
    let { left: o, top: n, width: a, height: l } = bt([{
      x: t,
      y: r
    }, {
      x: i,
      y: s
    }]), h = new v(o + a / 2, n + l / 2);
    this.setPositionByOrigin(h, L, L);
  }
  _set(t, r) {
    return super._set(t, r), Li.includes(t) && this._setWidthHeight(), this;
  }
  _render(t) {
    t.beginPath();
    let r = this.calcLinePoints();
    t.moveTo(r.x1, r.y1), t.lineTo(r.x2, r.y2), t.lineWidth = this.strokeWidth;
    let i = t.strokeStyle;
    var s;
    ut(this.stroke) ? t.strokeStyle = this.stroke.toLive(t) : t.strokeStyle = (s = this.stroke) == null ? t.fillStyle : s, this.stroke && this._renderStroke(t), t.strokeStyle = i;
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
    let { x1: t, x2: r, y1: i, y2: s, width: o, height: n } = this, a = t <= r ? -0.5 : 0.5, l = i <= s ? -0.5 : 0.5;
    return {
      x1: a * o,
      x2: a * -o,
      y1: l * n,
      y2: l * -n
    };
  }
  _toSVG() {
    let { x1: t, x2: r, y1: i, y2: s } = this.calcLinePoints();
    return [
      "<line ",
      "COMMON_PARTS",
      `x1="${t}" y1="${i}" x2="${r}" y2="${s}" />
`
    ];
  }
  static async fromElement(t, r, i) {
    let { x1: s = 0, y1: o = 0, x2: n = 0, y2: a = 0, ...l } = Ft(t, this.ATTRIBUTE_NAMES, i);
    return new this([
      s,
      o,
      n,
      a
    ], l);
  }
  static fromObject({ x1: t, y1: r, x2: i, y2: s, ...o }) {
    return this._fromObject({
      ...o,
      points: [
        t,
        r,
        i,
        s
      ]
    }, { extraParam: "points" });
  }
};
f(kt, "type", "Line"), f(kt, "cacheProperties", [...At, ...Li]), f(kt, "ATTRIBUTE_NAMES", Jt.concat(Li)), w.setClass(kt), w.setSVGClass(kt);
var vr = class Ri extends q {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Ri.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, Ri.ownDefaults), this.setOptions(t);
  }
  _render(t) {
    let r = this.width / 2, i = this.height / 2;
    t.beginPath(), t.moveTo(-r, i), t.lineTo(0, -i), t.lineTo(r, i), t.closePath(), this._renderPaintInOrder(t);
  }
  _toSVG() {
    let t = this.width / 2, r = this.height / 2;
    return [
      "<polygon ",
      "COMMON_PARTS",
      'points="',
      `${-t} ${r},0 ${-r},${t} ${r}`,
      '" />'
    ];
  }
};
f(vr, "type", "Triangle"), f(vr, "ownDefaults", {
  width: 100,
  height: 100
}), w.setClass(vr), w.setSVGClass(vr);
var Gn = ["rx", "ry"], ue = class Bi extends q {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Bi.ownDefaults
    };
  }
  constructor(t) {
    super(), Object.assign(this, Bi.ownDefaults), this.setOptions(t);
  }
  _set(t, r) {
    switch (super._set(t, r), t) {
      case "rx":
        this.rx = r, this.set("width", 2 * r);
        break;
      case "ry":
        this.ry = r, this.set("height", 2 * r);
    }
    return this;
  }
  getRx() {
    return this.get("rx") * this.get(Nt);
  }
  getRy() {
    return this.get("ry") * this.get(qt);
  }
  toObject(t = []) {
    return super.toObject([...Gn, ...t]);
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
    t.beginPath(), t.save(), t.transform(1, 0, 0, this.ry / this.rx, 0, 0), t.arc(0, 0, this.rx, 0, vt, !1), t.restore(), this._renderPaintInOrder(t);
  }
  static async fromElement(t, r, i) {
    let s = Ft(t, this.ATTRIBUTE_NAMES, i);
    return s.left = (s.left || 0) - s.rx, s.top = (s.top || 0) - s.ry, new this(s);
  }
};
f(ue, "type", "Ellipse"), f(ue, "cacheProperties", [...At, ...Gn]), f(ue, "ownDefaults", {
  rx: 0,
  ry: 0
}), f(ue, "ATTRIBUTE_NAMES", [
  ...Jt,
  "cx",
  "cy",
  "rx",
  "ry"
]), w.setClass(ue), w.setSVGClass(ue);
var Un = { exactBoundingBox: !1 }, Yt = class Ii extends q {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Ii.ownDefaults
    };
  }
  constructor(t = [], r = {}) {
    super(), f(this, "strokeDiff", void 0), Object.assign(this, Ii.ownDefaults), this.setOptions(r), this.points = t;
    let { left: i, top: s } = r;
    this.initialized = !0, this.setBoundingBox(!0), typeof i == "number" && this.set("left", i), typeof s == "number" && this.set("top", s);
  }
  isOpen() {
    return !0;
  }
  _projectStrokeOnPoints(t) {
    return gn(this.points, t, this.isOpen());
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
    let r = this.exactBoundingBox ? this._projectStrokeOnPoints(t).map((h) => h.projectedPoint) : this.points;
    if (r.length === 0) return {
      left: 0,
      top: 0,
      width: 0,
      height: 0,
      pathOffset: new v(),
      strokeOffset: new v(),
      strokeDiff: new v()
    };
    let i = bt(r), s = cr({
      ...t,
      scaleX: 1,
      scaleY: 1
    }), o = bt(this.points.map((h) => N(h, s, !0))), n = new v(this.scaleX, this.scaleY), a = i.left + i.width / 2, l = i.top + i.height / 2;
    return this.exactBoundingBox && (a -= l * Math.tan(I(this.skewX)), l -= a * Math.tan(I(this.skewY))), {
      ...i,
      pathOffset: new v(a, l),
      strokeOffset: new v(o.left, o.top).subtract(new v(i.left, i.top)).multiply(n),
      strokeDiff: new v(i.width, i.height).subtract(new v(o.width, o.height)).multiply(n)
    };
  }
  _findCenterFromElement() {
    let t = bt(this.points);
    return new v(t.left + t.width / 2, t.top + t.height / 2);
  }
  setDimensions() {
    this.setBoundingBox();
  }
  setBoundingBox(t) {
    let { left: r, top: i, width: s, height: o, pathOffset: n, strokeOffset: a, strokeDiff: l } = this._calcDimensions();
    this.set({
      width: s,
      height: o,
      pathOffset: n,
      strokeOffset: a,
      strokeDiff: l
    }), t && this.setPositionByOrigin(new v(r + s / 2, i + o / 2), "center", "center");
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
        var r, i;
        let { width: a, height: l } = this._calcDimensions(t);
        n = new v((r = t.width) == null ? a : r, (i = t.height) == null ? l : i);
      } else {
        var s, o;
        n = new v((s = t.width) == null ? this.width : s, (o = t.height) == null ? this.height : o);
      }
      return n.multiply(new v(t.scaleX || this.scaleX, t.scaleY || this.scaleY));
    }
    return super._getTransformedDimensions(t);
  }
  _set(t, r) {
    let i = this.initialized && this[t] !== r, s = super._set(t, r);
    return this.exactBoundingBox && i && ((t === "scaleX" || t === "scaleY") && this.strokeUniform && this.constructor.layoutProperties.includes("strokeUniform") || this.constructor.layoutProperties.includes(t)) && this.setDimensions(), s;
  }
  toObject(t = []) {
    return {
      ...super.toObject(t),
      points: this.points.map(({ x: r, y: i }) => ({
        x: r,
        y: i
      }))
    };
  }
  _toSVG() {
    let t = this.pathOffset.x, r = this.pathOffset.y, i = P.NUM_FRACTION_DIGITS, s = this.points.map(({ x: o, y: n }) => `${F(o - t, i)},${F(n - r, i)}`).join(" ");
    return [
      `<${M(this.constructor.type).toLowerCase()} `,
      "COMMON_PARTS",
      `points="${s}" />
`
    ];
  }
  _render(t) {
    let r = this.points.length, i = this.pathOffset.x, s = this.pathOffset.y;
    if (r && !isNaN(this.points[r - 1].y)) {
      t.beginPath(), t.moveTo(this.points[0].x - i, this.points[0].y - s);
      for (let o = 0; o < r; o++) {
        let n = this.points[o];
        t.lineTo(n.x - i, n.y - s);
      }
      !this.isOpen() && t.closePath(), this._renderPaintInOrder(t);
    }
  }
  complexity() {
    return this.points.length;
  }
  static async fromElement(t, r, i) {
    let s = (function(l) {
      if (!l) return [];
      let h = l.replace(/,/g, " ").trim().split(/\s+/), c = [];
      for (let u = 0; u < h.length; u += 2) c.push({
        x: parseFloat(h[u]),
        y: parseFloat(h[u + 1])
      });
      return c;
    })(t.getAttribute("points")), { left: o, top: n, ...a } = Ft(t, this.ATTRIBUTE_NAMES, i);
    return new this(s, {
      ...a,
      ...r
    });
  }
  static fromObject(t) {
    return this._fromObject(t, { extraParam: "points" });
  }
};
f(Yt, "ownDefaults", Un), f(Yt, "type", "Polyline"), f(Yt, "layoutProperties", [
  Te,
  Oe,
  "strokeLineCap",
  "strokeLineJoin",
  "strokeMiterLimit",
  "strokeWidth",
  "strokeUniform",
  "points"
]), f(Yt, "cacheProperties", [...At, "points"]), f(Yt, "ATTRIBUTE_NAMES", [...Jt]), w.setClass(Yt), w.setSVGClass(Yt);
var Vt = class extends Yt {
  isOpen() {
    return !1;
  }
};
f(Vt, "ownDefaults", Un), f(Vt, "type", "Polygon"), w.setClass(Vt), w.setSVGClass(Vt);
var Nn = class extends q {
  isEmptyStyles(e) {
    if (!this.styles || e !== void 0 && !this.styles[e]) return !0;
    let t = e === void 0 ? this.styles : { line: this.styles[e] };
    for (let r in t) for (let i in t[r]) for (let s in t[r][i]) return !1;
    return !0;
  }
  styleHas(e, t) {
    if (!this.styles || t !== void 0 && !this.styles[t]) return !1;
    let r = t === void 0 ? this.styles : { 0: this.styles[t] };
    for (let i in r) for (let s in r[i]) if (r[i][s][e] !== void 0) return !0;
    return !1;
  }
  cleanStyle(e) {
    if (!this.styles) return !1;
    let t = this.styles, r, i, s = 0, o = !0, n = 0;
    for (let a in t) {
      r = 0;
      for (let l in t[a]) {
        let h = t[a][l] || {};
        s++, h[e] === void 0 ? o = !1 : (i ? h[e] !== i && (o = !1) : i = h[e], h[e] === this[e] && delete h[e]), Object.keys(h).length === 0 ? delete t[a][l] : r++;
      }
      r === 0 && delete t[a];
    }
    for (let a = 0; a < this._textLines.length; a++) n += this._textLines[a].length;
    o && s === n && (this[e] = i, this.removeStyle(e));
  }
  removeStyle(e) {
    if (!this.styles) return;
    let t = this.styles, r, i, s;
    for (i in t) {
      for (s in r = t[i], r) delete r[s][e], Object.keys(r[s]).length === 0 && delete r[s];
      Object.keys(r).length === 0 && delete t[i];
    }
  }
  _extendStyles(e, t) {
    let { lineIndex: r, charIndex: i } = this.get2DCursorLocation(e);
    this._getLineStyle(r) || this._setLineStyle(r);
    let s = es({
      ...this._getStyleDeclaration(r, i),
      ...t
    }, (o) => o !== void 0);
    this._setStyleDeclaration(r, i, s);
  }
  getSelectionStyles(e, t, r) {
    let i = [];
    for (let s = e; s < (t || e); s++) i.push(this.getStyleAtPosition(s, r));
    return i;
  }
  getStyleAtPosition(e, t) {
    let { lineIndex: r, charIndex: i } = this.get2DCursorLocation(e);
    return t ? this.getCompleteStyleDeclaration(r, i) : this._getStyleDeclaration(r, i);
  }
  setSelectionStyles(e, t, r) {
    for (let i = t; i < (r || t); i++) this._extendStyles(i, e);
    this._forceClearCache = !0;
  }
  _getStyleDeclaration(e, t) {
    var r;
    let i = this.styles && this.styles[e];
    return i && (r = i[t]) != null ? r : {};
  }
  getCompleteStyleDeclaration(e, t) {
    return {
      ...ae(this, this.constructor._styleProperties),
      ...this._getStyleDeclaration(e, t)
    };
  }
  _setStyleDeclaration(e, t, r) {
    this.styles[e][t] = r;
  }
  _deleteStyleDeclaration(e, t) {
    delete this.styles[e][t];
  }
  _getLineStyle(e) {
    return !!this.styles[e];
  }
  _setLineStyle(e) {
    this.styles[e] = {};
  }
  _deleteLineStyle(e) {
    delete this.styles[e];
  }
};
f(Nn, "_styleProperties", Pa);
var Sh = /  +/g, Ch = /"/g;
function hi(e, t, r, i, s) {
  return `		${((o, { left: n, top: a, width: l, height: h }, c = P.NUM_FRACTION_DIGITS) => {
    let u = or(st, o, !1), [d, g, p, m] = [
      n,
      a,
      l,
      h
    ].map((x) => F(x, c));
    return `<rect ${u} x="${d}" y="${g}" width="${p}" height="${m}"></rect>`;
  })(e, {
    left: t,
    top: r,
    width: i,
    height: s
  })}
`;
}
var ci, St = class Re extends Nn {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Re.ownDefaults
    };
  }
  constructor(t, r) {
    super(), f(this, "__charBounds", []), Object.assign(this, Re.ownDefaults), this.setOptions(r), this.styles || (this.styles = {}), this.text = t, this.initialized = !0, this.path && this.setPathInfo(), this.initDimensions(), this.setCoords();
  }
  setPathInfo() {
    let t = this.path;
    t && (t.segmentsInfo = xs(t.path));
  }
  _splitText() {
    let t = this._splitTextIntoLines(this.text);
    return this.textLines = t.lines, this._textLines = t.graphemeLines, this._unwrappedTextLines = t._unwrappedLines, this._text = t.graphemeText, t;
  }
  initDimensions() {
    this._splitText(), this._clearCache(), this.dirty = !0, this.path ? (this.width = this.path.width, this.height = this.path.height) : (this.width = this.calcTextWidth() || this.cursorWidth || this.MIN_TEXT_WIDTH, this.height = this.calcTextHeight()), this.textAlign.includes("justify") && this.enlargeSpaces();
  }
  enlargeSpaces() {
    let t, r, i, s, o, n, a;
    for (let l = 0, h = this._textLines.length; l < h; l++) if ((this.textAlign === "justify" || l !== h - 1 && !this.isEndOfWrapping(l)) && (s = 0, o = this._textLines[l], r = this.getLineWidth(l), r < this.width && (a = this.textLines[l].match(this._reSpacesAndTabs)))) {
      i = a.length, t = (this.width - r) / i;
      for (let c = 0; c <= o.length; c++) n = this.__charBounds[l][c], this._reSpaceAndTab.test(o[c]) ? (n.width += t, n.kernedWidth += t, n.left += s, s += t) : n.left += s;
    }
  }
  isEndOfWrapping(t) {
    return t === this._textLines.length - 1;
  }
  missingNewlineOffset(t) {
    return 1;
  }
  get2DCursorLocation(t, r) {
    let i = r ? this._unwrappedTextLines : this._textLines, s;
    for (s = 0; s < i.length; s++) {
      if (t <= i[s].length) return {
        lineIndex: s,
        charIndex: t
      };
      t -= i[s].length + this.missingNewlineOffset(s, r);
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
    let t = super._getCacheCanvasDimensions(), r = this.fontSize;
    return t.width += r * t.zoomX, t.height += r * t.zoomY, t;
  }
  _render(t) {
    let r = this.path;
    r && !r.isNotVisible() && r._render(t), this._setTextStyles(t), this._renderTextLinesBackground(t), this._renderTextDecoration(t, "underline"), this._renderText(t), this._renderTextDecoration(t, "overline"), this._renderTextDecoration(t, "linethrough");
  }
  _renderText(t) {
    this.paintFirst === "stroke" ? (this._renderTextStroke(t), this._renderTextFill(t)) : (this._renderTextFill(t), this._renderTextStroke(t));
  }
  _setTextStyles(t, r, i) {
    if (t.textBaseline = "alphabetic", this.path) switch (this.pathAlign) {
      case L:
        t.textBaseline = "middle";
        break;
      case "ascender":
        t.textBaseline = "top";
        break;
      case "descender":
        t.textBaseline = so;
    }
    t.font = this._getFontDeclaration(r, i);
  }
  calcTextWidth() {
    let t = this.getLineWidth(0);
    for (let r = 1, i = this._textLines.length; r < i; r++) {
      let s = this.getLineWidth(r);
      s > t && (t = s);
    }
    return t;
  }
  _renderTextLine(t, r, i, s, o, n) {
    this._renderChars(t, r, i, s, o, n);
  }
  _renderTextLinesBackground(t) {
    if (!this.textBackgroundColor && !this.styleHas("textBackgroundColor")) return;
    let r = t.fillStyle, i = this._getLeftOffset(), s = this._getTopOffset();
    for (let o = 0, n = this._textLines.length; o < n; o++) {
      let a = this.getHeightOfLine(o);
      if (!this.textBackgroundColor && !this.styleHas("textBackgroundColor", o)) {
        s += a;
        continue;
      }
      let l = this._textLines[o].length, h = this._getLineLeftOffset(o), c, u, d = 0, g = 0, p = this.getValueOfPropertyAt(o, 0, "textBackgroundColor"), m = this.getHeightOfLineImpl(o);
      for (let x = 0; x < l; x++) {
        let _ = this.__charBounds[o][x];
        u = this.getValueOfPropertyAt(o, x, "textBackgroundColor"), this.path ? (t.save(), t.translate(_.renderLeft, _.renderTop), t.rotate(_.angle), t.fillStyle = u, u && t.fillRect(-_.width / 2, -m * (1 - this._fontSizeFraction), _.width, m), t.restore()) : u === p ? d += _.kernedWidth : (c = i + h + g, this.direction === "rtl" && (c = this.width - c - d), t.fillStyle = p, p && t.fillRect(c, s, d, m), g = _.left, d = _.width, p = u);
      }
      u && !this.path && (c = i + h + g, this.direction === "rtl" && (c = this.width - c - d), t.fillStyle = u, t.fillRect(c, s, d, m)), s += a;
    }
    t.fillStyle = r, this._removeShadow(t);
  }
  _measureChar(t, r, i, s) {
    let o = Ze.getFontCache(r), n = this._getFontDeclaration(r), a = i ? i + t : t, l = i && n === this._getFontDeclaration(s), h = r.fontSize / this.CACHE_FONT_SIZE, c, u, d, g;
    if (i && o.has(i) && (d = o.get(i)), o.has(t) && (g = c = o.get(t)), l && o.has(a) && (u = o.get(a), g = u - d), c === void 0 || d === void 0 || u === void 0) {
      let p = (ci || (ci = ht({
        width: 0,
        height: 0
      }).getContext("2d")), ci);
      this._setTextStyles(p, r, !0), c === void 0 && (g = c = p.measureText(t).width, o.set(t, c)), d === void 0 && l && i && (d = p.measureText(i).width, o.set(i, d)), l && u === void 0 && (u = p.measureText(a).width, o.set(a, u), g = u - d);
    }
    return {
      width: c * h,
      kernedWidth: g * h
    };
  }
  getHeightOfChar(t, r) {
    return this.getValueOfPropertyAt(t, r, "fontSize");
  }
  measureLine(t) {
    let r = this._measureLine(t);
    return this.charSpacing !== 0 && (r.width -= this._getWidthOfCharSpacing()), r.width < 0 && (r.width = 0), r;
  }
  _measureLine(t) {
    let r, i, s = 0, o = this.pathSide === pt, n = this.path, a = this._textLines[t], l = a.length, h = Array(l);
    this.__charBounds[t] = h;
    for (let c = 0; c < l; c++) {
      let u = a[c];
      i = this._getGraphemeBox(u, t, c, r), h[c] = i, s += i.kernedWidth, r = u;
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
        case H:
          c = o ? u - s : 0;
          break;
        case L:
          c = (u - s) / 2;
          break;
        case pt:
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
  _setGraphemeOnPath(t, r) {
    let i = t + r.kernedWidth / 2, s = this.path, o = On(s.path, i, s.segmentsInfo);
    r.renderLeft = o.x - s.pathOffset.x, r.renderTop = o.y - s.pathOffset.y, r.angle = o.angle + (this.pathSide === "right" ? Math.PI : 0);
  }
  _getGraphemeBox(t, r, i, s, o) {
    let n = this.getCompleteStyleDeclaration(r, i), a = s ? this.getCompleteStyleDeclaration(r, i - 1) : {}, l = this._measureChar(t, n, s, a), h, c = l.kernedWidth, u = l.width;
    this.charSpacing !== 0 && (h = this._getWidthOfCharSpacing(), u += h, c += h);
    let d = {
      width: u,
      left: 0,
      height: n.fontSize,
      kernedWidth: c,
      deltaY: n.deltaY
    };
    if (i > 0 && !o) {
      let g = this.__charBounds[r][i - 1];
      d.left = g.left + g.width + l.kernedWidth - l.width;
    }
    return d;
  }
  getHeightOfLineImpl(t) {
    let r = this.__lineHeights;
    if (r[t]) return r[t];
    let i = this.getHeightOfChar(t, 0);
    for (let s = 1, o = this._textLines[t].length; s < o; s++) i = Math.max(this.getHeightOfChar(t, s), i);
    return r[t] = i * this._fontSizeMult;
  }
  getHeightOfLine(t) {
    return this.getHeightOfLineImpl(t) * this.lineHeight;
  }
  calcTextHeight() {
    let t = 0;
    for (let r = 0, i = this._textLines.length; r < i; r++) t += r === i - 1 ? this.getHeightOfLineImpl(r) : this.getHeightOfLine(r);
    return t;
  }
  _getLeftOffset() {
    return this.direction === "ltr" ? -this.width / 2 : this.width / 2;
  }
  _getTopOffset() {
    return -this.height / 2;
  }
  _renderTextCommon(t, r) {
    t.save();
    let i = 0, s = this._getLeftOffset(), o = this._getTopOffset();
    for (let n = 0, a = this._textLines.length; n < a; n++) this._renderTextLine(r, t, this._textLines[n], s + this._getLineLeftOffset(n), o + i + this.getHeightOfLineImpl(n), n), i += this.getHeightOfLine(n);
    t.restore();
  }
  _renderTextFill(t) {
    (this.fill || this.styleHas("fill")) && this._renderTextCommon(t, "fillText");
  }
  _renderTextStroke(t) {
    (this.stroke && this.strokeWidth !== 0 || !this.isEmptyStyles()) && (this.shadow && !this.shadow.affectStroke && this._removeShadow(t), t.save(), this._setLineDash(t, this.strokeDashArray), t.beginPath(), this._renderTextCommon(t, "strokeText"), t.closePath(), t.restore());
  }
  _renderChars(t, r, i, s, o, n) {
    let a = this.textAlign.includes(hs), l = this.path, h = !a && this.charSpacing === 0 && this.isEmptyStyles(n) && !l, c = this.direction === "ltr", u = this.direction === "ltr" ? 1 : -1, d = r.direction, g, p, m, x, _, y = "", S = 0;
    if (r.save(), d !== this.direction && (r.canvas.setAttribute("dir", c ? "ltr" : "rtl"), r.direction = c ? "ltr" : "rtl", r.textAlign = c ? H : pt), o -= this.getHeightOfLineImpl(n) * this._fontSizeFraction, h) return this._renderChar(t, r, n, 0, i.join(""), s, o), void r.restore();
    for (let C = 0, b = i.length - 1; C <= b; C++) x = C === b || this.charSpacing || l, y += i[C], m = this.__charBounds[n][C], S === 0 ? (s += u * (m.kernedWidth - m.width), S += m.width) : S += m.kernedWidth, a && !x && this._reSpaceAndTab.test(i[C]) && (x = !0), x || (g = g || this.getCompleteStyleDeclaration(n, C), p = this.getCompleteStyleDeclaration(n, C + 1), x = ti(g, p, !1)), x && (l ? (r.save(), r.translate(m.renderLeft, m.renderTop), r.rotate(m.angle), this._renderChar(t, r, n, C, y, -S / 2, 0), r.restore()) : (_ = s, this._renderChar(t, r, n, C, y, _, o)), y = "", g = p, s += u * S, S = 0);
    r.restore();
  }
  _applyPatternGradientTransformText(t) {
    let r = this.width + this.strokeWidth, i = this.height + this.strokeWidth, s = ht({
      width: r,
      height: i
    }), o = s.getContext("2d");
    return s.width = r, s.height = i, o.beginPath(), o.moveTo(0, 0), o.lineTo(r, 0), o.lineTo(r, i), o.lineTo(0, i), o.closePath(), o.translate(r / 2, i / 2), o.fillStyle = t.toLive(o), this._applyPatternGradientTransform(o, t), o.fill(), o.createPattern(s, "no-repeat");
  }
  handleFiller(t, r, i) {
    let s, o;
    return ut(i) ? i.gradientUnits === "percentage" || i.gradientTransform || i.patternTransform ? (s = -this.width / 2, o = -this.height / 2, t.translate(s, o), t[r] = this._applyPatternGradientTransformText(i), {
      offsetX: s,
      offsetY: o
    }) : (t[r] = i.toLive(t), this._applyPatternGradientTransform(t, i)) : (t[r] = i, {
      offsetX: 0,
      offsetY: 0
    });
  }
  _setStrokeStyles(t, { stroke: r, strokeWidth: i }) {
    return t.lineWidth = i, t.lineCap = this.strokeLineCap, t.lineDashOffset = this.strokeDashOffset, t.lineJoin = this.strokeLineJoin, t.miterLimit = this.strokeMiterLimit, this.handleFiller(t, "strokeStyle", r);
  }
  _setFillStyles(t, { fill: r }) {
    return this.handleFiller(t, "fillStyle", r);
  }
  _renderChar(t, r, i, s, o, n, a) {
    let l = this._getStyleDeclaration(i, s), h = this.getCompleteStyleDeclaration(i, s), c = t === "fillText" && h.fill, u = t === "strokeText" && h.stroke && h.strokeWidth;
    if (u || c) {
      if (r.save(), r.font = this._getFontDeclaration(h), l.textBackgroundColor && this._removeShadow(r), l.deltaY && (a += l.deltaY), c) {
        let d = this._setFillStyles(r, h);
        r.fillText(o, n - d.offsetX, a - d.offsetY);
      }
      if (u) {
        let d = this._setStrokeStyles(r, h);
        r.strokeText(o, n - d.offsetX, a - d.offsetY);
      }
      r.restore();
    }
  }
  setSuperscript(t, r) {
    this._setScript(t, r, this.superscript);
  }
  setSubscript(t, r) {
    this._setScript(t, r, this.subscript);
  }
  _setScript(t, r, i) {
    let s = this.get2DCursorLocation(t, !0), o = this.getValueOfPropertyAt(s.lineIndex, s.charIndex, "fontSize"), n = this.getValueOfPropertyAt(s.lineIndex, s.charIndex, "deltaY"), a = {
      fontSize: o * i.size,
      deltaY: n + o * i.baseline
    };
    this.setSelectionStyles(a, t, r);
  }
  _getLineLeftOffset(t) {
    let r = this.getLineWidth(t), i = this.width - r, s = this.textAlign, o = this.direction, n = this.isEndOfWrapping(t), a = 0;
    return s === "justify" || s === "justify-center" && !n || s === "justify-right" && !n || s === "justify-left" && !n ? 0 : (s === "center" && (a = i / 2), s === "right" && (a = i), s === "justify-center" && (a = i / 2), s === "justify-right" && (a = i), o === "rtl" && (s === "right" || s === "justify-right" ? a = 0 : s === "left" || s === "justify-left" ? a = -i : s !== "center" && s !== "justify-center" || (a = -i / 2)), a);
  }
  _clearCache() {
    this._forceClearCache = !1, this.__lineWidths = [], this.__lineHeights = [], this.__charBounds = [];
  }
  getLineWidth(t) {
    if (this.__lineWidths[t] !== void 0) return this.__lineWidths[t];
    let { width: r } = this.measureLine(t);
    return this.__lineWidths[t] = r, r;
  }
  _getWidthOfCharSpacing() {
    return this.charSpacing === 0 ? 0 : this.fontSize * this.charSpacing / 1e3;
  }
  getValueOfPropertyAt(t, r, i) {
    var s;
    return (s = this._getStyleDeclaration(t, r)[i]) == null ? this[i] : s;
  }
  _renderTextDecoration(t, r) {
    if (!this[r] && !this.styleHas(r)) return;
    let i = this._getTopOffset(), s = this._getLeftOffset(), o = this.path, n = this._getWidthOfCharSpacing(), a = r === "linethrough" ? 0.5 : +(r === "overline"), l = this.offsets[r];
    for (let h = 0, c = this._textLines.length; h < c; h++) {
      let u = this.getHeightOfLine(h);
      if (!this[r] && !this.styleHas(r, h)) {
        i += u;
        continue;
      }
      let d = this._textLines[h], g = u / this.lineHeight, p = this._getLineLeftOffset(h), m, x = 0, _ = 0, y = this.getValueOfPropertyAt(h, 0, r), S = this.getValueOfPropertyAt(h, 0, st), C = this.getValueOfPropertyAt(h, 0, "textDecorationColor") || S, b = this.getValueOfPropertyAt(h, 0, be), O = y, T = C, k = b, D = i + g * (1 - this._fontSizeFraction), B = this.getHeightOfChar(h, 0), A = this.getValueOfPropertyAt(h, 0, "deltaY");
      for (let X = 0, G = d.length; X < G; X++) {
        let $ = this.__charBounds[h][X];
        O = this.getValueOfPropertyAt(h, X, r), m = this.getValueOfPropertyAt(h, X, st), T = this.getValueOfPropertyAt(h, X, "textDecorationColor") || m, k = this.getValueOfPropertyAt(h, X, be);
        let J = this.getHeightOfChar(h, X), ot = this.getValueOfPropertyAt(h, X, "deltaY");
        if (o && O && m) {
          let j = this.fontSize * k / 1e3;
          t.save(), t.fillStyle = T, t.translate($.renderLeft, $.renderTop), t.rotate($.angle), t.fillRect(-$.kernedWidth / 2, l * J + ot - a * j, $.kernedWidth, j), t.restore();
        } else if ((O !== y || m !== S || T !== C || J !== B || k !== b || ot !== A) && _ > 0) {
          let j = this.fontSize * b / 1e3, _t = s + p + x;
          this.direction === "rtl" && (_t = this.width - _t - _), y && C && b && (t.fillStyle = C, t.fillRect(_t, D + l * B + A - a * j, _, j)), x = $.left, _ = $.width, y = O, C = T, b = k, S = m, B = J, A = ot;
        } else _ += $.kernedWidth;
      }
      let E = s + p + x;
      this.direction === "rtl" && (E = this.width - E - _), t.fillStyle = T;
      let R = this.fontSize * k / 1e3;
      O && T && k && t.fillRect(E, D + l * B + A - a * R, _ - n, R), i += u;
    }
    this._removeShadow(t);
  }
  _getFontDeclaration({ fontFamily: t = this.fontFamily, fontStyle: r = this.fontStyle, fontWeight: i = this.fontWeight, fontSize: s = this.fontSize } = {}, o) {
    let n = t.includes("'") || t.includes('"') || t.includes(",") || Re.genericFonts.includes(t.toLowerCase()) ? t : `"${t}"`;
    return [
      r,
      i,
      `${o ? this.CACHE_FONT_SIZE : s}px`,
      n
    ].join(" ");
  }
  render(t) {
    this.visible && (this.canvas && this.canvas.skipOffscreen && !this.group && !this.isOnScreen() || (this._forceClearCache && this.initDimensions(), super.render(t)));
  }
  graphemeSplit(t) {
    return zr(t);
  }
  _splitTextIntoLines(t) {
    let r = t.split(this._reNewline), i = Array(r.length), s = [`
`], o = [];
    for (let n = 0; n < r.length; n++) i[n] = this.graphemeSplit(r[n]), o = o.concat(i[n], s);
    return o.pop(), {
      _unwrappedLines: i,
      lines: r,
      graphemeText: o,
      graphemeLines: i
    };
  }
  toObject(t = []) {
    return {
      ...super.toObject([...Xo, ...t]),
      styles: fn(this.styles, this.text),
      ...this.path ? { path: this.path.toObject() } : {}
    };
  }
  set(t, r) {
    let { textLayoutProperties: i } = this.constructor;
    super.set(t, r);
    let s = !1, o = !1;
    if (typeof t == "object") for (let n in t) n === "path" && this.setPathInfo(), s = s || i.includes(n), o = o || n === "path";
    else s = i.includes(t), o = t === "path";
    return o && this.setPathInfo(), s && this.initialized && (this.initDimensions(), this.setCoords()), this;
  }
  complexity() {
    return 1;
  }
  static async fromElement(t, r, i) {
    let s = Ft(t, Re.ATTRIBUTE_NAMES, i), { textAnchor: o = H, textDecoration: n = "", dx: a = 0, dy: l = 0, top: h = 0, left: c = 0, fontSize: u = 16, strokeWidth: d = 1, ...g } = {
      ...r,
      ...s
    }, p = new this(Ir(t.textContent || "").trim(), {
      left: c + a,
      top: h + l,
      underline: n.includes("underline"),
      overline: n.includes("overline"),
      linethrough: n.includes("line-through"),
      strokeWidth: 0,
      fontSize: u,
      ...g
    }), m = p.getScaledHeight() / p.height, x = ((p.height + p.strokeWidth) * p.lineHeight - p.height) * m, _ = p.getScaledHeight() + x, y = 0;
    return o === "center" && (y = p.getScaledWidth() / 2), o === "right" && (y = p.getScaledWidth()), p.set({
      left: p.left - y,
      top: p.top - (_ - p.fontSize * (0.07 + p._fontSizeFraction)) / p.lineHeight,
      strokeWidth: d
    }), p;
  }
  static fromObject(t) {
    return this._fromObject({
      ...t,
      styles: pn(t.styles || {}, t.text)
    }, { extraParam: "text" });
  }
};
f(St, "textLayoutProperties", Io), f(St, "cacheProperties", [...At, ...Xo]), f(St, "ownDefaults", Aa), f(St, "type", "Text"), f(St, "genericFonts", [
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
]), f(St, "ATTRIBUTE_NAMES", Jt.concat("x", "y", "dx", "dy", "font-family", "font-style", "font-weight", "font-size", "letter-spacing", "text-decoration", "text-decoration-thickness", "text-decoration-color", "text-anchor")), hn(St, [class extends Lo {
  _toSVG() {
    let e = this._getSVGLeftTopOffsets(), t = this._getSVGTextAndBg(e.textTop, e.textLeft);
    return this._wrapSVGTextAndBg(t);
  }
  toSVG(e) {
    let t = this._createBaseSVGMarkup(this._toSVG(), {
      reviver: e,
      noStyle: !0,
      withShadow: !0
    }), r = this.path;
    return r ? t + r._createBaseSVGMarkup(r._toSVG(), {
      reviver: e,
      withShadow: !0,
      additionalTransform: Se(this.calcOwnMatrix())
    }) : t;
  }
  _getSVGLeftTopOffsets() {
    return {
      textLeft: -this.width / 2,
      textTop: -this.height / 2,
      lineTop: this.getHeightOfLine(0)
    };
  }
  _wrapSVGTextAndBg({ textBgRects: e, textSpans: t }) {
    let r = this.getSvgTextDecoration(this);
    return [
      e.join(""),
      '		<text xml:space="preserve" ',
      `font-family="${M(this.fontFamily.replace(Ch, "'"))}" `,
      `font-size="${M(this.fontSize)}" `,
      this.fontStyle ? `font-style="${M(this.fontStyle)}" ` : "",
      this.fontWeight ? `font-weight="${M(this.fontWeight)}" ` : "",
      r ? `text-decoration="${r}" ` : "",
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
  _getSVGTextAndBg(e, t) {
    let r = [], i = [], s, o = e;
    this.backgroundColor && i.push(hi(this.backgroundColor, -this.width / 2, -this.height / 2, this.width, this.height));
    for (let n = 0, a = this._textLines.length; n < a; n++) s = this._getLineLeftOffset(n), this.direction === "rtl" && (s += this.width), (this.textBackgroundColor || this.styleHas("textBackgroundColor", n)) && this._setSVGTextLineBg(i, n, t + s, o), this._setSVGTextLineText(r, n, t + s, o), o += this.getHeightOfLine(n);
    return {
      textSpans: r,
      textBgRects: i
    };
  }
  _createTextCharSpan(e, t, r, i, s) {
    let o = P.NUM_FRACTION_DIGITS, n = this.getSvgSpanStyles(t, e !== e.trim() || !!e.match(Sh)), a = n ? `style="${n}"` : "", l = t.deltaY, h = l ? ` dy="${F(l, o)}" ` : "", { angle: c, renderLeft: u, renderTop: d, width: g } = s, p = "";
    if (u !== void 0) {
      let m = g / 2;
      c && (p = ` rotate="${F(Et(c), o)}"`);
      let x = ne({ angle: Et(c) });
      x[4] = u, x[5] = d;
      let _ = new v(-m, 0).transform(x);
      r = _.x, i = _.y;
    }
    return `<tspan x="${F(r, o)}" y="${F(i, o)}" ${h}${p}${a}>${M(e)}</tspan>`;
  }
  _setSVGTextLineText(e, t, r, i) {
    let s = this.getHeightOfLine(t), o = this.textAlign.includes(hs), n = this._textLines[t], a, l, h, c, u, d = "", g = 0;
    i += s * (1 - this._fontSizeFraction) / this.lineHeight;
    for (let p = 0, m = n.length - 1; p <= m; p++) u = p === m || this.charSpacing || this.path, d += n[p], h = this.__charBounds[t][p], g === 0 ? (r += h.kernedWidth - h.width, g += h.width) : g += h.kernedWidth, o && !u && this._reSpaceAndTab.test(n[p]) && (u = !0), u || (a = a || this.getCompleteStyleDeclaration(t, p), l = this.getCompleteStyleDeclaration(t, p + 1), u = ti(a, l, !0)), u && (c = this._getStyleDeclaration(t, p), e.push(this._createTextCharSpan(d, c, r, i, h)), d = "", a = l, this.direction === "rtl" ? r -= g : r += g, g = 0);
  }
  _setSVGTextLineBg(e, t, r, i) {
    let s = this._textLines[t], o = this.getHeightOfLine(t) / this.lineHeight, n, a = 0, l = 0, h = this.getValueOfPropertyAt(t, 0, "textBackgroundColor");
    for (let c = 0; c < s.length; c++) {
      let { left: u, width: d, kernedWidth: g } = this.__charBounds[t][c];
      n = this.getValueOfPropertyAt(t, c, "textBackgroundColor"), n === h ? a += g : (h && e.push(hi(h, r + l, i, a, o)), l = u, a = d, h = n);
    }
    n && e.push(hi(h, r + l, i, a, o));
  }
  getSvgStyles(e) {
    let t = Kr(this.textDecorationColor) ? ` text-decoration-color: ${M(this[Qr])};` : "";
    return `${super.getSvgStyles(e)} text-decoration-thickness: ${F(this.textDecorationThickness * this.getObjectScaling().y / 10, P.NUM_FRACTION_DIGITS)}%;${t} white-space: pre;`;
  }
  getSvgSpanStyles(e, t) {
    let { fontFamily: r, strokeWidth: i, stroke: s, fill: o, fontSize: n, fontStyle: a, fontWeight: l, textDecorationThickness: h, textDecorationColor: c, linethrough: u, overline: d, underline: g } = e, p = this.getSvgTextDecoration({
      underline: g ?? this.underline,
      overline: d ?? this.overline,
      linethrough: u ?? this.linethrough
    }), m = h || this.textDecorationThickness, x = c || this.textDecorationColor, _ = te(i), y = ee(r), S = te(n), C = ee(a), b = te(l) || ee(l), O = ee(x);
    return [
      s ? or(Dt, s) : "",
      _ ? `stroke-width: ${M(_)}; ` : "",
      y ? `font-family: ${y.includes("'") || y.includes('"') ? M(y) : `'${M(y)}'`}; ` : "",
      S ? `font-size: ${M(S)}px; ` : "",
      C ? `font-style: ${M(C)}; ` : "",
      b ? `font-weight: ${M(b)}; ` : "",
      p ? `text-decoration: ${p}; text-decoration-thickness: ${F(m * this.getObjectScaling().y / 10, P.NUM_FRACTION_DIGITS)}%;${O ? ` text-decoration-color: ${M(O)};` : ""} ` : "",
      o ? or(st, o) : "",
      t ? "white-space: pre; " : ""
    ].join("");
  }
  getSvgTextDecoration(e) {
    return [
      "overline",
      "underline",
      "line-through"
    ].filter((t) => e[t.replace("-", "")]).join(" ");
  }
}]), w.setClass(St), w.setSVGClass(St);
var bh = class {
  constructor(e) {
    f(this, "target", void 0), f(this, "__mouseDownInPlace", !1), f(this, "__dragStartFired", !1), f(this, "__isDraggingOver", !1), f(this, "__dragStartSelection", void 0), f(this, "__dragImageDisposer", void 0), f(this, "_dispose", void 0), this.target = e;
    let t = [
      this.target.on("dragenter", this.dragEnterHandler.bind(this)),
      this.target.on("dragover", this.dragOverHandler.bind(this)),
      this.target.on("dragleave", this.dragLeaveHandler.bind(this)),
      this.target.on("dragend", this.dragEndHandler.bind(this)),
      this.target.on("drop", this.dropHandler.bind(this))
    ];
    this._dispose = () => {
      t.forEach((r) => r()), this._dispose = void 0;
    };
  }
  isPointerOverSelection(e) {
    let t = this.target, r = t.getSelectionStartFromPointer(e);
    return t.isEditing && r >= t.selectionStart && r <= t.selectionEnd && t.selectionStart < t.selectionEnd;
  }
  start(e) {
    return this.__mouseDownInPlace = this.isPointerOverSelection(e);
  }
  isActive() {
    return this.__mouseDownInPlace;
  }
  end(e) {
    let t = this.isActive();
    return t && !this.__dragStartFired && (this.target.setCursorByClick(e), this.target.initDelayedCursor(!0)), this.__mouseDownInPlace = !1, this.__dragStartFired = !1, this.__isDraggingOver = !1, t;
  }
  getDragStartSelection() {
    return this.__dragStartSelection;
  }
  setDragImage(e, { selectionStart: t, selectionEnd: r }) {
    var i;
    let s = this.target, o = s.canvas, n = new v(s.flipX ? -1 : 1, s.flipY ? -1 : 1), a = s._getCursorBoundaries(t), l = new v(a.left + a.leftOffset, a.top + a.topOffset).multiply(n).transform(s.calcTransformMatrix()), h = o.getScenePoint(e).subtract(l), c = s.getCanvasRetinaScaling(), u = s.getBoundingRect(), d = l.subtract(new v(u.left, u.top)), g = o.viewportTransform, p = d.add(h).transform(g, !0), m = s.backgroundColor, x = vs(s.styles);
    s.backgroundColor = "";
    let _ = {
      stroke: "transparent",
      fill: "transparent",
      textBackgroundColor: "transparent"
    };
    s.setSelectionStyles(_, 0, t), s.setSelectionStyles(_, r, s.text.length), s.dirty = !0;
    let y = s.toCanvasElement({
      enableRetinaScaling: o.enableRetinaScaling,
      viewportTransform: !0
    });
    s.backgroundColor = m, s.styles = x, s.dirty = !0, Ei(y, {
      position: "fixed",
      left: -y.width + "px",
      border: $r,
      width: y.width / c + "px",
      height: y.height / c + "px"
    }), this.__dragImageDisposer && this.__dragImageDisposer(), this.__dragImageDisposer = () => {
      y.remove();
    }, gt(e.target || this.target.hiddenTextarea).body.appendChild(y), (i = e.dataTransfer) == null || i.setDragImage(y, p.x, p.y);
  }
  onDragStart(e) {
    this.__dragStartFired = !0;
    let t = this.target, r = this.isActive();
    if (r && e.dataTransfer) {
      let i = this.__dragStartSelection = {
        selectionStart: t.selectionStart,
        selectionEnd: t.selectionEnd
      }, s = t._text.slice(i.selectionStart, i.selectionEnd).join(""), o = {
        text: t.text,
        value: s,
        ...i
      };
      e.dataTransfer.setData("text/plain", s), e.dataTransfer.setData("application/fabric", JSON.stringify({
        value: s,
        styles: t.getSelectionStyles(i.selectionStart, i.selectionEnd, !0)
      })), e.dataTransfer.effectAllowed = "copyMove", this.setDragImage(e, o);
    }
    return t.abortCursorAnimation(), r;
  }
  canDrop(e) {
    if (this.target.editable && !this.target.getActiveControl() && !e.defaultPrevented) {
      if (this.isActive() && this.__dragStartSelection) {
        let t = this.target.getSelectionStartFromPointer(e), r = this.__dragStartSelection;
        return t < r.selectionStart || t > r.selectionEnd;
      }
      return !0;
    }
    return !1;
  }
  targetCanDrop(e) {
    return this.target.canDrop(e);
  }
  dragEnterHandler({ e }) {
    let t = this.targetCanDrop(e);
    !this.__isDraggingOver && t && (this.__isDraggingOver = !0);
  }
  dragOverHandler(e) {
    let { e: t } = e, r = this.targetCanDrop(t);
    !this.__isDraggingOver && r ? this.__isDraggingOver = !0 : this.__isDraggingOver && !r && (this.__isDraggingOver = !1), this.__isDraggingOver && (t.preventDefault(), e.canDrop = !0, e.dropTarget = this.target);
  }
  dragLeaveHandler() {
    (this.__isDraggingOver || this.isActive()) && (this.__isDraggingOver = !1);
  }
  dropHandler(e) {
    var t;
    let { e: r } = e, i = r.defaultPrevented;
    this.__isDraggingOver = !1, r.preventDefault();
    let s = (t = r.dataTransfer) == null ? void 0 : t.getData("text/plain");
    if (s && !i) {
      let o = this.target, n = o.canvas, a = o.getSelectionStartFromPointer(r), { styles: l } = r.dataTransfer.types.includes("application/fabric") ? JSON.parse(r.dataTransfer.getData("application/fabric")) : {}, h = s[Math.max(0, s.length - 1)];
      if (this.__dragStartSelection) {
        let c = this.__dragStartSelection.selectionStart, u = this.__dragStartSelection.selectionEnd;
        a > c && a <= u ? a = c : a > u && (a -= u - c), o.removeChars(c, u), delete this.__dragStartSelection;
      }
      o._reNewline.test(h) && (o._reNewline.test(o._text[a]) || a === o._text.length) && (s = s.trimEnd()), e.didDrop = !0, e.dropTarget = o, o.insertChars(s, l, a), n.setActiveObject(o), o.enterEditing(r), o.selectionStart = Math.min(a + 0, o._text.length), o.selectionEnd = Math.min(o.selectionStart + s.length, o._text.length), o.hiddenTextarea.value = o.text, o._updateTextarea(), o.hiddenTextarea.focus(), o.fire(jr, {
        index: a + 0,
        action: "drop"
      }), n.fire("text:changed", { target: o }), n.contextTopDirty = !0, n.requestRenderAll();
    }
  }
  dragEndHandler({ e }) {
    if (this.isActive() && this.__dragStartFired && this.__dragStartSelection) {
      var t;
      let r = this.target, i = this.target.canvas, { selectionStart: s, selectionEnd: o } = this.__dragStartSelection, n = ((t = e.dataTransfer) == null ? void 0 : t.dropEffect) || "none";
      n === "none" ? (r.selectionStart = s, r.selectionEnd = o, r._updateTextarea(), r.hiddenTextarea.focus()) : (r.clearContextTop(), n === "move" && (r.removeChars(s, o), r.selectionStart = r.selectionEnd = s, r.hiddenTextarea && (r.hiddenTextarea.value = r.text), r._updateTextarea(), r.fire(jr, {
        index: s,
        action: "dragend"
      }), i.fire("text:changed", { target: r }), i.requestRenderAll()), r.exitEditing());
    }
    this.__dragImageDisposer && this.__dragImageDisposer(), delete this.__dragImageDisposer, delete this.__dragStartSelection, this.__isDraggingOver = !1;
  }
  dispose() {
    this._dispose && this._dispose();
  }
}, Gs = /[ \n\.,;!\?\-]/, wh = class extends St {
  constructor(...e) {
    super(...e), f(this, "_currentCursorOpacity", 1);
  }
  initBehavior() {
    this._tick = this._tick.bind(this), this._onTickComplete = this._onTickComplete.bind(this), this.updateSelectionOnMouseMove = this.updateSelectionOnMouseMove.bind(this);
  }
  onDeselect(e) {
    return this.isEditing && this.exitEditing(), this.selected = !1, super.onDeselect(e);
  }
  _animateCursor({ toValue: e, duration: t, delay: r, onComplete: i }) {
    return gs({
      startValue: this._currentCursorOpacity,
      endValue: e,
      duration: t,
      delay: r,
      onComplete: i,
      abort: () => !this.canvas || this.selectionStart !== this.selectionEnd,
      onChange: (s) => {
        this._currentCursorOpacity = s, this.renderCursorOrSelection();
      }
    });
  }
  _tick(e) {
    this._currentTickState = this._animateCursor({
      toValue: 0,
      duration: this.cursorDuration / 2,
      delay: Math.max(e || 0, 100),
      onComplete: this._onTickComplete
    });
  }
  _onTickComplete() {
    var e;
    (e = this._currentTickCompleteState) == null || e.abort(), this._currentTickCompleteState = this._animateCursor({
      toValue: 1,
      duration: this.cursorDuration,
      onComplete: this._tick
    });
  }
  initDelayedCursor(e) {
    this.abortCursorAnimation(), this._tick(e ? 0 : this.cursorDelay);
  }
  abortCursorAnimation() {
    let e = !1;
    [this._currentTickState, this._currentTickCompleteState].forEach((t) => {
      t && !t.isDone() && (e = !0, t.abort());
    }), this._currentCursorOpacity = 1, e && this.clearContextTop();
  }
  restartCursorIfNeeded() {
    [this._currentTickState, this._currentTickCompleteState].some((e) => !e || e.isDone()) && this.initDelayedCursor();
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
  findWordBoundaryLeft(e) {
    let t = 0, r = e - 1;
    if (this._reSpace.test(this._text[r])) for (; this._reSpace.test(this._text[r]); ) t++, r--;
    for (; /\S/.test(this._text[r]) && r > -1; ) t++, r--;
    return e - t;
  }
  findWordBoundaryRight(e) {
    let t = 0, r = e;
    if (this._reSpace.test(this._text[r])) for (; this._reSpace.test(this._text[r]); ) t++, r++;
    for (; /\S/.test(this._text[r]) && r < this._text.length; ) t++, r++;
    return e + t;
  }
  findLineBoundaryLeft(e) {
    let t = 0, r = e - 1;
    for (; !/\n/.test(this._text[r]) && r > -1; ) t++, r--;
    return e - t;
  }
  findLineBoundaryRight(e) {
    let t = 0, r = e;
    for (; !/\n/.test(this._text[r]) && r < this._text.length; ) t++, r++;
    return e + t;
  }
  searchWordBoundary(e, t) {
    let r = this._text, i = e > 0 && this._reSpace.test(r[e]) && (t === -1 || !Ui.test(r[e - 1])) ? e - 1 : e, s = r[i];
    for (; i > 0 && i < r.length && !Gs.test(s); ) i += t, s = r[i];
    return t === -1 && Gs.test(s) && i++, i;
  }
  selectWord(e) {
    var t;
    e = (t = e) == null ? this.selectionStart : t;
    let r = this.searchWordBoundary(e, -1), i = Math.max(r, this.searchWordBoundary(e, 1));
    this.selectionStart = r, this.selectionEnd = i, this._fireSelectionChanged(), this._updateTextarea(), this.renderCursorOrSelection();
  }
  selectLine(e) {
    var t;
    e = (t = e) == null ? this.selectionStart : t;
    let r = this.findLineBoundaryLeft(e), i = this.findLineBoundaryRight(e);
    this.selectionStart = r, this.selectionEnd = i, this._fireSelectionChanged(), this._updateTextarea();
  }
  enterEditing(e) {
    !this.isEditing && this.editable && (this.enterEditingImpl(), this.fire("editing:entered", e ? { e } : void 0), this._fireSelectionChanged(), this.canvas && (this.canvas.fire("text:editing:entered", {
      target: this,
      e
    }), this.canvas.requestRenderAll()));
  }
  enterEditingImpl() {
    this.canvas && (this.canvas.calcOffset(), this.canvas.textEditingManager.exitTextEditing()), this.isEditing = !0, this.initHiddenTextarea(), this.hiddenTextarea.focus(), this.hiddenTextarea.value = this.text, this._updateTextarea(), this._saveEditingProps(), this._setEditingProps(), this._textBeforeEdit = this.text, this._tick();
  }
  updateSelectionOnMouseMove(e) {
    if (this.getActiveControl()) return;
    let t = this.hiddenTextarea;
    gt(t).activeElement !== t && t.focus();
    let r = this.getSelectionStartFromPointer(e), i = this.selectionStart, s = this.selectionEnd;
    (r === this.__selectionStartOnMouseDown && i !== s || i !== r && s !== r) && (r > this.__selectionStartOnMouseDown ? (this.selectionStart = this.__selectionStartOnMouseDown, this.selectionEnd = r) : (this.selectionStart = r, this.selectionEnd = this.__selectionStartOnMouseDown), this.selectionStart === i && this.selectionEnd === s || (this._fireSelectionChanged(), this._updateTextarea(), this.renderCursorOrSelection()));
  }
  _setEditingProps() {
    this.hoverCursor = "text", this.canvas && (this.canvas.defaultCursor = this.canvas.moveCursor = "text"), this.borderColor = this.editingBorderColor, this.hasControls = this.selectable = !1, this.lockMovementX = this.lockMovementY = !0;
  }
  fromStringToGraphemeSelection(e, t, r) {
    let i = r.slice(0, e), s = this.graphemeSplit(i).length;
    if (e === t) return {
      selectionStart: s,
      selectionEnd: s
    };
    let o = r.slice(e, t);
    return {
      selectionStart: s,
      selectionEnd: s + this.graphemeSplit(o).length
    };
  }
  fromGraphemeToStringSelection(e, t, r) {
    let i = r.slice(0, e).join("").length;
    return e === t ? {
      selectionStart: i,
      selectionEnd: i
    } : {
      selectionStart: i,
      selectionEnd: i + r.slice(e, t).join("").length
    };
  }
  _updateTextarea() {
    if (this.cursorOffsetCache = {}, this.hiddenTextarea) {
      if (!this.inCompositionMode) {
        let e = this.fromGraphemeToStringSelection(this.selectionStart, this.selectionEnd, this._text);
        this.hiddenTextarea.selectionStart = e.selectionStart, this.hiddenTextarea.selectionEnd = e.selectionEnd;
      }
      this.updateTextareaPosition();
    }
  }
  updateFromTextArea() {
    let { hiddenTextarea: e, direction: t, textAlign: r, inCompositionMode: i } = this;
    if (!e) return;
    let s = r === "justify" ? t === "ltr" ? H : pt : r.replace("justify-", ""), o = this.getPositionByOrigin(s, "top");
    this.cursorOffsetCache = {}, this.text = e.value, this.set("dirty", !0), this.initDimensions(), this.setPositionByOrigin(o, s, "top"), this.setCoords();
    let n = this.fromStringToGraphemeSelection(e.selectionStart, e.selectionEnd, e.value);
    this.selectionEnd = this.selectionStart = n.selectionEnd, i || (this.selectionStart = n.selectionStart), this.updateTextareaPosition();
  }
  updateTextareaPosition() {
    if (this.selectionStart === this.selectionEnd) {
      let e = this._calcTextareaPosition();
      this.hiddenTextarea.style.left = e.left, this.hiddenTextarea.style.top = e.top;
    }
  }
  _calcTextareaPosition() {
    if (!this.canvas) return {
      left: "1px",
      top: "1px"
    };
    let e = this.inCompositionMode ? this.compositionStart : this.selectionStart, t = this._getCursorBoundaries(e), r = this.get2DCursorLocation(e), i = r.lineIndex, s = r.charIndex, o = this.getValueOfPropertyAt(i, s, "fontSize") * this.lineHeight, n = t.leftOffset, a = this.getCanvasRetinaScaling(), l = this.canvas.upperCanvasEl, h = l.width / a, c = l.height / a, u = h - o, d = c - o, g = new v(t.left + n, t.top + t.topOffset + o).transform(this.calcTransformMatrix()).transform(this.canvas.viewportTransform).multiply(new v(l.clientWidth / h, l.clientHeight / c));
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
    let e = this.hiddenTextarea;
    this.selected = !1, this.isEditing = !1, e && (e.blur && e.blur(), e.parentNode && e.parentNode.removeChild(e)), this.hiddenTextarea = null, this.abortCursorAnimation(), this.selectionStart !== this.selectionEnd && this.clearContextTop(), this.selectionEnd = this.selectionStart, this._restoreEditingProps(), this._forceClearCache && (this.initDimensions(), this.setCoords());
  }
  exitEditing() {
    let e = this._textBeforeEdit !== this.text;
    return this.exitEditingImpl(), this.fire("editing:exited"), e && this.fire("modified"), this.canvas && (this.canvas.fire("text:editing:exited", { target: this }), e && this.canvas.fire("object:modified", { target: this })), this;
  }
  _removeExtraneousStyles() {
    for (let e in this.styles) this._textLines[e] || delete this.styles[e];
  }
  removeStyleFromTo(e, t) {
    let { lineIndex: r, charIndex: i } = this.get2DCursorLocation(e, !0), { lineIndex: s, charIndex: o } = this.get2DCursorLocation(t, !0);
    if (r !== s) {
      if (this.styles[r]) for (let n = i; n < this._unwrappedTextLines[r].length; n++) delete this.styles[r][n];
      if (this.styles[s]) for (let n = o; n < this._unwrappedTextLines[s].length; n++) {
        let a = this.styles[s][n];
        a && (this.styles[r] || (this.styles[r] = {}), this.styles[r][i + n - o] = a);
      }
      for (let n = r + 1; n <= s; n++) delete this.styles[n];
      this.shiftLineStyles(s, r - s);
    } else if (this.styles[r]) {
      let n = this.styles[r], a = o - i;
      for (let l = i; l < o; l++) delete n[l];
      for (let l in this.styles[r]) {
        let h = parseInt(l, 10);
        h >= o && (n[h - a] = n[l], delete n[l]);
      }
    }
  }
  shiftLineStyles(e, t) {
    let r = Object.assign({}, this.styles);
    for (let i in this.styles) {
      let s = parseInt(i, 10);
      s > e && (this.styles[s + t] = r[s], r[s - t] || delete this.styles[s]);
    }
  }
  insertNewlineStyleObject(e, t, r, i) {
    let s = {}, o = this._unwrappedTextLines[e].length, n = o === t, a = !1;
    r || (r = 1), this.shiftLineStyles(e, r);
    let l = this.styles[e] ? this.styles[e][t === 0 ? t : t - 1] : void 0;
    for (let c in this.styles[e]) {
      let u = parseInt(c, 10);
      u >= t && (a = !0, s[u - t] = this.styles[e][c], n && t === 0 || delete this.styles[e][c]);
    }
    let h = !1;
    for (a && !n && (this.styles[e + r] = s, h = !0), (h || o > t) && r--; r > 0; ) i && i[r - 1] ? this.styles[e + r] = { 0: { ...i[r - 1] } } : l ? this.styles[e + r] = { 0: { ...l } } : delete this.styles[e + r], r--;
    this._forceClearCache = !0;
  }
  insertCharStyleObject(e, t, r, i) {
    this.styles || (this.styles = {});
    let s = this.styles[e], o = s ? { ...s } : {};
    r || (r = 1);
    for (let a in o) {
      let l = parseInt(a, 10);
      l >= t && (s[l + r] = o[l], o[l - r] || delete s[l]);
    }
    if (this._forceClearCache = !0, i) {
      for (; r--; ) Object.keys(i[r]).length && (this.styles[e] || (this.styles[e] = {}), this.styles[e][t + r] = { ...i[r] });
      return;
    }
    if (!s) return;
    let n = s[t ? t - 1 : 1];
    for (; n && r--; ) this.styles[e][t + r] = { ...n };
  }
  insertNewStyleBlock(e, t, r) {
    let i = this.get2DCursorLocation(t, !0), s = [0], o, n = 0;
    for (let a = 0; a < e.length; a++) e[a] === `
` ? (n++, s[n] = 0) : s[n]++;
    for (s[0] > 0 && (this.insertCharStyleObject(i.lineIndex, i.charIndex, s[0], r), r = r && r.slice(s[0] + 1)), n && this.insertNewlineStyleObject(i.lineIndex, i.charIndex + s[0], n), o = 1; o < n; o++) s[o] > 0 ? this.insertCharStyleObject(i.lineIndex + o, 0, s[o], r) : r && this.styles[i.lineIndex + o] && r[0] && (this.styles[i.lineIndex + o][0] = r[0]), r = r && r.slice(s[o] + 1);
    s[o] > 0 && this.insertCharStyleObject(i.lineIndex + o, 0, s[o], r);
  }
  removeChars(e, t = e + 1) {
    this.removeStyleFromTo(e, t), this._text.splice(e, t - e), this.text = this._text.join(""), this.set("dirty", !0), this.initDimensions(), this.setCoords(), this._removeExtraneousStyles();
  }
  insertChars(e, t, r, i = r) {
    i > r && this.removeStyleFromTo(r, i);
    let s = this.graphemeSplit(e);
    this.insertNewStyleBlock(s, r, t), this._text = [
      ...this._text.slice(0, r),
      ...s,
      ...this._text.slice(i)
    ], this.text = this._text.join(""), this.set("dirty", !0), this.initDimensions(), this.setCoords(), this._removeExtraneousStyles();
  }
  setSelectionStartEndWithShift(e, t, r) {
    r <= e ? (t === e ? this._selectionDirection = H : this._selectionDirection === "right" && (this._selectionDirection = H, this.selectionEnd = e), this.selectionStart = r) : r > e && r < t ? this._selectionDirection === "right" ? this.selectionEnd = r : this.selectionStart = r : (t === e ? this._selectionDirection = pt : this._selectionDirection === "left" && (this._selectionDirection = pt, this.selectionStart = t), this.selectionEnd = r);
  }
}, Th = class extends wh {
  initHiddenTextarea() {
    let e = this.canvas && gt(this.canvas.getElement()) || we(), t = e.createElement("textarea");
    Object.entries({
      autocapitalize: "off",
      autocorrect: "off",
      autocomplete: "off",
      spellcheck: "false",
      "data-fabric": "textarea",
      wrap: "off",
      name: "fabricTextarea"
    }).map(([o, n]) => t.setAttribute(o, n));
    let { top: r, left: i, fontSize: s } = this._calcTextareaPosition();
    t.style.cssText = `position: absolute; top: ${r}; left: ${i}; z-index: -999; opacity: 0; width: 1px; height: 1px; font-size: 1px; padding-top: ${s};`, (this.hiddenTextareaContainer || e.body).appendChild(t), Object.entries({
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
  onKeyDown(e) {
    if (!this.isEditing) return;
    let t = this.direction === "rtl" ? this.keysMapRtl : this.keysMap;
    if (e.keyCode in t) this[t[e.keyCode]](e);
    else {
      if (!(e.keyCode in this.ctrlKeysMapDown) || !e.ctrlKey && !e.metaKey) return;
      this[this.ctrlKeysMapDown[e.keyCode]](e);
    }
    e.stopImmediatePropagation(), e.preventDefault(), e.keyCode >= 33 && e.keyCode <= 40 ? (this.inCompositionMode = !1, this.clearContextTop(), this.renderCursorOrSelection()) : this.canvas && this.canvas.requestRenderAll();
  }
  onKeyUp(e) {
    !this.isEditing || this._copyDone || this.inCompositionMode ? this._copyDone = !1 : e.keyCode in this.ctrlKeysMapUp && (e.ctrlKey || e.metaKey) && (this[this.ctrlKeysMapUp[e.keyCode]](e), e.stopImmediatePropagation(), e.preventDefault(), this.canvas && this.canvas.requestRenderAll());
  }
  onInput(e) {
    let t = this.fromPaste, { value: r, selectionStart: i, selectionEnd: s } = this.hiddenTextarea;
    if (this.fromPaste = !1, e && e.stopPropagation(), !this.isEditing) return;
    let o = () => {
      this.updateFromTextArea(), this.fire(jr), this.canvas && (this.canvas.fire("text:changed", { target: this }), this.canvas.requestRenderAll());
    };
    if (this.hiddenTextarea.value === "") return this.styles = {}, void o();
    let n = this._splitTextIntoLines(r).graphemeText, a = this._text.length, l = n.length, h = this.selectionStart, c = this.selectionEnd, u = h !== c, d, g, p, m, x = l - a, _ = this.fromStringToGraphemeSelection(i, s, r), y = h > _.selectionStart;
    u ? (g = this._text.slice(h, c), x += c - h) : l < a && (g = y ? this._text.slice(c + x, c) : this._text.slice(h, h - x));
    let S = n.slice(_.selectionEnd - x, _.selectionEnd);
    if (g && g.length && (S.length && (d = this.getSelectionStyles(h, h + 1, !1), d = S.map(() => d[0])), u ? (p = h, m = c) : y ? (p = c - g.length, m = c) : (p = c, m = c + g.length), this.removeStyleFromTo(p, m)), S.length) {
      let { copyPasteData: C } = wt();
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
  onCompositionUpdate({ target: e }) {
    let { selectionStart: t, selectionEnd: r } = e;
    this.compositionStart = t, this.compositionEnd = r, this.updateTextareaPosition();
  }
  copy() {
    if (this.selectionStart === this.selectionEnd) return;
    let { copyPasteData: e } = wt();
    e.copiedText = this.getSelectedText(), P.disableStyleCopyPaste ? e.copiedTextStyle = void 0 : e.copiedTextStyle = this.getSelectionStyles(this.selectionStart, this.selectionEnd, !0), this._copyDone = !0;
  }
  paste() {
    this.fromPaste = !0;
  }
  _getWidthBeforeCursor(e, t) {
    let r, i = this._getLineLeftOffset(e);
    return t > 0 && (r = this.__charBounds[e][t - 1], i += r.left + r.width), i;
  }
  getDownCursorOffset(e, t) {
    let r = this._getSelectionForOffset(e, t), i = this.get2DCursorLocation(r), s = i.lineIndex;
    if (s === this._textLines.length - 1 || e.metaKey || e.keyCode === 34) return this._text.length - r;
    let o = i.charIndex, n = this._getWidthBeforeCursor(s, o), a = this._getIndexOnLine(s + 1, n);
    return this._textLines[s].slice(o).length + a + 1 + this.missingNewlineOffset(s);
  }
  _getSelectionForOffset(e, t) {
    return e.shiftKey && this.selectionStart !== this.selectionEnd && t ? this.selectionEnd : this.selectionStart;
  }
  getUpCursorOffset(e, t) {
    let r = this._getSelectionForOffset(e, t), i = this.get2DCursorLocation(r), s = i.lineIndex;
    if (s === 0 || e.metaKey || e.keyCode === 33) return -r;
    let o = i.charIndex, n = this._getWidthBeforeCursor(s, o), a = this._getIndexOnLine(s - 1, n), l = this._textLines[s].slice(0, o), h = this.missingNewlineOffset(s - 1);
    return -this._textLines[s - 1].length + a - l.length + (1 - h);
  }
  _getIndexOnLine(e, t) {
    let r = this._textLines[e], i, s, o = this._getLineLeftOffset(e), n = 0;
    for (let a = 0, l = r.length; a < l; a++) if (i = this.__charBounds[e][a].width, o += i, o > t) {
      s = !0;
      let h = o - i, c = o, u = Math.abs(h - t);
      n = Math.abs(c - t) < u ? a : a - 1;
      break;
    }
    return s || (n = r.length - 1), n;
  }
  moveCursorDown(e) {
    this.selectionStart >= this._text.length && this.selectionEnd >= this._text.length || this._moveCursorUpOrDown("Down", e);
  }
  moveCursorUp(e) {
    this.selectionStart === 0 && this.selectionEnd === 0 || this._moveCursorUpOrDown("Up", e);
  }
  _moveCursorUpOrDown(e, t) {
    let r = this[`get${e}CursorOffset`](t, this._selectionDirection === pt);
    if (t.shiftKey ? this.moveCursorWithShift(r) : this.moveCursorWithoutShift(r), r !== 0) {
      let i = this.text.length;
      this.selectionStart = oe(0, this.selectionStart, i), this.selectionEnd = oe(0, this.selectionEnd, i), this.abortCursorAnimation(), this.initDelayedCursor(), this._fireSelectionChanged(), this._updateTextarea();
    }
  }
  moveCursorWithShift(e) {
    let t = this._selectionDirection === "left" ? this.selectionStart + e : this.selectionEnd + e;
    return this.setSelectionStartEndWithShift(this.selectionStart, this.selectionEnd, t), e !== 0;
  }
  moveCursorWithoutShift(e) {
    return e < 0 ? (this.selectionStart += e, this.selectionEnd = this.selectionStart) : (this.selectionEnd += e, this.selectionStart = this.selectionEnd), e !== 0;
  }
  moveCursorLeft(e) {
    this.selectionStart === 0 && this.selectionEnd === 0 || this._moveCursorLeftOrRight("Left", e);
  }
  _move(e, t, r) {
    let i;
    if (e.altKey) i = this[`findWordBoundary${r}`](this[t]);
    else {
      if (!e.metaKey && e.keyCode !== 35 && e.keyCode !== 36) return this[t] += r === "Left" ? -1 : 1, !0;
      i = this[`findLineBoundary${r}`](this[t]);
    }
    return i !== void 0 && this[t] !== i && (this[t] = i, !0);
  }
  _moveLeft(e, t) {
    return this._move(e, t, "Left");
  }
  _moveRight(e, t) {
    return this._move(e, t, "Right");
  }
  moveCursorLeftWithoutShift(e) {
    let t = !0;
    return this._selectionDirection = H, this.selectionEnd === this.selectionStart && this.selectionStart !== 0 && (t = this._moveLeft(e, "selectionStart")), this.selectionEnd = this.selectionStart, t;
  }
  moveCursorLeftWithShift(e) {
    return this._selectionDirection === "right" && this.selectionStart !== this.selectionEnd ? this._moveLeft(e, "selectionEnd") : this.selectionStart === 0 ? void 0 : (this._selectionDirection = H, this._moveLeft(e, "selectionStart"));
  }
  moveCursorRight(e) {
    this.selectionStart >= this._text.length && this.selectionEnd >= this._text.length || this._moveCursorLeftOrRight("Right", e);
  }
  _moveCursorLeftOrRight(e, t) {
    let r = `moveCursor${e}${t.shiftKey ? "WithShift" : "WithoutShift"}`;
    this._currentCursorOpacity = 1, this[r](t) && (this.abortCursorAnimation(), this.initDelayedCursor(), this._fireSelectionChanged(), this._updateTextarea());
  }
  moveCursorRightWithShift(e) {
    return this._selectionDirection === "left" && this.selectionStart !== this.selectionEnd ? this._moveRight(e, "selectionStart") : this.selectionEnd === this._text.length ? void 0 : (this._selectionDirection = pt, this._moveRight(e, "selectionEnd"));
  }
  moveCursorRightWithoutShift(e) {
    let t = !0;
    return this._selectionDirection = pt, this.selectionStart === this.selectionEnd ? (t = this._moveRight(e, "selectionStart"), this.selectionEnd = this.selectionStart) : this.selectionStart = this.selectionEnd, t;
  }
}, Us = (e) => !!e.button, Oh = class extends Th {
  constructor(...e) {
    super(...e), f(this, "draggableTextDelegate", void 0);
  }
  initBehavior() {
    this.on("mousedown", this._mouseDownHandler), this.on("mouseup", this.mouseUpHandler), this.on("mousedblclick", this.doubleClickHandler), this.on("mousetripleclick", this.tripleClickHandler), this.draggableTextDelegate = new bh(this), super.initBehavior();
  }
  shouldStartDragging() {
    return this.draggableTextDelegate.isActive();
  }
  onDragStart(e) {
    return this.draggableTextDelegate.onDragStart(e);
  }
  canDrop(e) {
    return this.draggableTextDelegate.canDrop(e);
  }
  doubleClickHandler(e) {
    this.isEditing && (this.selectWord(this.getSelectionStartFromPointer(e.e)), this.renderCursorOrSelection());
  }
  tripleClickHandler(e) {
    this.isEditing && (this.selectLine(this.getSelectionStartFromPointer(e.e)), this.renderCursorOrSelection());
  }
  _mouseDownHandler({ e, alreadySelected: t }) {
    this.canvas && this.editable && !Us(e) && !this.getActiveControl() && (this.draggableTextDelegate.start(e) || (this.canvas.textEditingManager.register(this), t && (this.inCompositionMode = !1, this.setCursorByClick(e)), this.isEditing && (this.__selectionStartOnMouseDown = this.selectionStart, this.selectionStart === this.selectionEnd && this.abortCursorAnimation(), this.renderCursorOrSelection()), this.selected || (this.selected = t || this.isEditing)));
  }
  mouseUpHandler({ e, transform: t }) {
    let r = this.draggableTextDelegate.end(e);
    if (this.canvas) {
      this.canvas.textEditingManager.unregister(this);
      let i = this.canvas._activeObject;
      if (i && i !== this) return;
    }
    !this.editable || this.group && !this.group.interactive || t && t.actionPerformed || Us(e) || r || this.selected && !this.getActiveControl() && (this.enterEditing(e), this.selectionStart === this.selectionEnd ? this.initDelayedCursor(!0) : this.renderCursorOrSelection());
  }
  setCursorByClick(e) {
    let t = this.getSelectionStartFromPointer(e), r = this.selectionStart, i = this.selectionEnd;
    e.shiftKey ? this.setSelectionStartEndWithShift(r, i, t) : (this.selectionStart = t, this.selectionEnd = t), this.isEditing && (this._fireSelectionChanged(), this._updateTextarea());
  }
  getSelectionStartFromPointer(e) {
    let t = this.canvas.getScenePoint(e).transform(lt(this.calcTransformMatrix())).add(new v(-this._getLeftOffset(), -this._getTopOffset())), r = 0, i = 0, s = 0;
    for (let l = 0; l < this._textLines.length && r <= t.y; l++) r += this.getHeightOfLine(l), s = l, l > 0 && (i += this._textLines[l - 1].length + this.missingNewlineOffset(l - 1));
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
}, yr = "moveCursorUp", xr = "moveCursorDown", _r = "moveCursorLeft", Sr = "moveCursorRight", Cr = "exitEditing", Ns = (e, t) => {
  let r = t.getRetinaScaling();
  e.setTransform(r, 0, 0, r, 0, 0);
  let i = t.viewportTransform;
  e.transform(i[0], i[1], i[2], i[3], i[4], i[5]);
}, kh = {
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
    9: Cr,
    27: Cr,
    33: yr,
    34: xr,
    35: Sr,
    36: _r,
    37: _r,
    38: yr,
    39: Sr,
    40: xr
  },
  keysMapRtl: {
    9: Cr,
    27: Cr,
    33: yr,
    34: xr,
    35: _r,
    36: Sr,
    37: Sr,
    38: yr,
    39: _r,
    40: xr
  },
  ctrlKeysMapDown: { 65: "cmdAll" },
  ctrlKeysMapUp: {
    67: "copy",
    88: "cut"
  },
  _selectionDirection: null,
  _reSpace: /\s|\r?\n/,
  inCompositionMode: !1
}, Mt = class Xi extends Oh {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Xi.ownDefaults
    };
  }
  get type() {
    let t = super.type;
    return t === "itext" ? "i-text" : t;
  }
  constructor(t, r) {
    super(t, {
      ...Xi.ownDefaults,
      ...r
    }), this.initBehavior();
  }
  _set(t, r) {
    return this.isEditing && this._savedProps && t in this._savedProps ? (this._savedProps[t] = r, this) : (t === "canvas" && (this.canvas instanceof Ai && this.canvas.textEditingManager.remove(this), r instanceof Ai && r.textEditingManager.add(this)), super._set(t, r));
  }
  setSelectionStart(t) {
    t = Math.max(t, 0), this._updateAndFire("selectionStart", t);
  }
  setSelectionEnd(t) {
    t = Math.min(t, this.text.length), this._updateAndFire("selectionEnd", t);
  }
  _updateAndFire(t, r) {
    this[t] !== r && (this._fireSelectionChanged(), this[t] = r), this._updateTextarea();
  }
  _fireSelectionChanged() {
    this.fire("selection:changed"), this.canvas && this.canvas.fire("text:selection:changed", { target: this });
  }
  initDimensions() {
    this.isEditing && this.initDelayedCursor(), super.initDimensions();
  }
  getSelectionStyles(t = this.selectionStart || 0, r = this.selectionEnd, i) {
    return super.getSelectionStyles(t, r, i);
  }
  setSelectionStyles(t, r = this.selectionStart || 0, i = this.selectionEnd) {
    return super.setSelectionStyles(t, r, i);
  }
  get2DCursorLocation(t = this.selectionStart, r) {
    return super.get2DCursorLocation(t, r);
  }
  render(t) {
    super.render(t), this.cursorOffsetCache = {}, this.renderCursorOrSelection();
  }
  toCanvasElement(t) {
    let r = this.isEditing;
    this.isEditing = !1;
    let i = super.toCanvasElement(t);
    return this.isEditing = r, i;
  }
  renderCursorOrSelection() {
    if (!this.isEditing || !this.canvas) return;
    let t = this.clearContextTop(!0);
    if (!t) return;
    let r = this._getCursorBoundaries(), i = this.findAncestorsWithClipPath(), s = i.length > 0, o, n = t;
    if (s) {
      o = ht(t.canvas), n = o.getContext("2d"), Ns(n, this.canvas);
      let a = this.calcTransformMatrix();
      n.transform(a[0], a[1], a[2], a[3], a[4], a[5]);
    }
    if (this.selectionStart !== this.selectionEnd || this.inCompositionMode ? this.renderSelection(n, r) : this.renderCursor(n, r), s) for (let a of i) {
      let l = a.clipPath, h = ht(t.canvas), c = h.getContext("2d");
      if (Ns(c, this.canvas), !l.absolutePositioned) {
        let u = a.calcTransformMatrix();
        c.transform(u[0], u[1], u[2], u[3], u[4], u[5]);
      }
      l.transform(c), l.drawObject(c, !0, {}), this.drawClipPathOnCache(n, l, h);
    }
    s && (t.setTransform(1, 0, 0, 1, 0, 0), t.drawImage(o, 0, 0)), this.canvas.contextTopDirty = !0, t.restore();
  }
  findAncestorsWithClipPath() {
    let t = [], r = this;
    for (; r; ) r.clipPath && t.push(r), r = r.parent;
    return t;
  }
  _getCursorBoundaries(t = this.selectionStart, r) {
    let i = this._getLeftOffset(), s = this._getTopOffset(), o = this._getCursorBoundariesOffsets(t, r);
    return {
      left: i,
      top: s,
      leftOffset: o.left,
      topOffset: o.top
    };
  }
  _getCursorBoundariesOffsets(t, r) {
    return r ? this.__getCursorBoundariesOffsets(t) : this.cursorOffsetCache && "top" in this.cursorOffsetCache ? this.cursorOffsetCache : this.cursorOffsetCache = this.__getCursorBoundariesOffsets(t);
  }
  __getCursorBoundariesOffsets(t) {
    let r = 0, i = 0, { charIndex: s, lineIndex: o } = this.get2DCursorLocation(t), { textAlign: n, direction: a } = this;
    for (let u = 0; u < o; u++) r += this.getHeightOfLine(u);
    let l = this._getLineLeftOffset(o), h = this.__charBounds[o][s];
    h && (i = h.left), this.charSpacing !== 0 && s === this._textLines[o].length && (i -= this._getWidthOfCharSpacing());
    let c = l + (i > 0 ? i : 0);
    return a === "rtl" && (n === "right" || n === "justify" || n === "justify-right" ? c *= -1 : n === "left" || n === "justify-left" ? c = l - (i > 0 ? i : 0) : n !== "center" && n !== "justify-center" || (c = l - (i > 0 ? i : 0))), {
      top: r,
      left: c
    };
  }
  renderCursorAt(t) {
    this._renderCursor(this.canvas.contextTop, this._getCursorBoundaries(t, !0), t);
  }
  renderCursor(t, r) {
    this._renderCursor(t, r, this.selectionStart);
  }
  getCursorRenderingData(t = this.selectionStart, r = this._getCursorBoundaries(t)) {
    let i = this.get2DCursorLocation(t), s = i.lineIndex, o = i.charIndex > 0 ? i.charIndex - 1 : 0, n = this.getValueOfPropertyAt(s, o, "fontSize"), a = this.getObjectScaling().x * this.canvas.getZoom(), l = this.cursorWidth / a, h = this.getValueOfPropertyAt(s, o, "deltaY"), c = r.topOffset + (1 - this._fontSizeFraction) * this.getHeightOfLine(s) / this.lineHeight - n * (1 - this._fontSizeFraction);
    return {
      color: this.cursorColor || this.getValueOfPropertyAt(s, o, "fill"),
      opacity: this._currentCursorOpacity,
      left: r.left + r.leftOffset - l / 2,
      top: c + r.top + h,
      width: l,
      height: n
    };
  }
  _renderCursor(t, r, i) {
    let { color: s, opacity: o, left: n, top: a, width: l, height: h } = this.getCursorRenderingData(i, r);
    t.fillStyle = s, t.globalAlpha = o, t.fillRect(n, a, l, h);
  }
  renderSelection(t, r) {
    let i = {
      selectionStart: this.inCompositionMode ? this.hiddenTextarea.selectionStart : this.selectionStart,
      selectionEnd: this.inCompositionMode ? this.hiddenTextarea.selectionEnd : this.selectionEnd
    };
    this._renderSelection(t, i, r);
  }
  renderDragSourceEffect() {
    let t = this.draggableTextDelegate.getDragStartSelection();
    this._renderSelection(this.canvas.contextTop, t, this._getCursorBoundaries(t.selectionStart, !0));
  }
  renderDropTargetEffect(t) {
    let r = this.getSelectionStartFromPointer(t);
    this.renderCursorAt(r);
  }
  _renderSelection(t, r, i) {
    let { textAlign: s, direction: o } = this, n = r.selectionStart, a = r.selectionEnd, l = s.includes(hs), h = this.get2DCursorLocation(n), c = this.get2DCursorLocation(a), u = h.lineIndex, d = c.lineIndex, g = h.charIndex < 0 ? 0 : h.charIndex, p = c.charIndex < 0 ? 0 : c.charIndex;
    for (let m = u; m <= d; m++) {
      let x = this._getLineLeftOffset(m) || 0, _ = this.getHeightOfLine(m), y = 0, S = 0;
      if (m === u && (y = this.__charBounds[u][g].left), m >= u && m < d) S = l && !this.isEndOfWrapping(m) ? this.width : this.getLineWidth(m) || 5;
      else if (m === d) if (p === 0) S = this.__charBounds[d][p].left;
      else {
        let D = this._getWidthOfCharSpacing();
        S = this.__charBounds[d][p - 1].left + this.__charBounds[d][p - 1].width - D;
      }
      let C = _;
      (this.lineHeight < 1 || m === d && this.lineHeight > 1) && (_ /= this.lineHeight);
      let b = i.left + x + y, O = _, T = 0, k = S - y;
      this.inCompositionMode ? (t.fillStyle = this.compositionColor || "black", O = 1, T = _) : t.fillStyle = this.selectionColor, o === "rtl" && (s === "right" || s === "justify" || s === "justify-right" ? b = this.width - b - k : s === "left" || s === "justify-left" ? b = i.left + x - S : s !== "center" && s !== "justify-center" || (b = i.left + x - S)), t.fillRect(b, i.top + i.topOffset + T, k, O), i.topOffset += C;
    }
  }
  getCurrentCharFontSize() {
    let t = this._getCurrentCharIndex();
    return this.getValueOfPropertyAt(t.l, t.c, "fontSize");
  }
  getCurrentCharColor() {
    let t = this._getCurrentCharIndex();
    return this.getValueOfPropertyAt(t.l, t.c, st);
  }
  _getCurrentCharIndex() {
    let t = this.get2DCursorLocation(this.selectionStart, !0), r = t.charIndex > 0 ? t.charIndex - 1 : 0;
    return {
      l: t.lineIndex,
      c: r
    };
  }
  dispose() {
    this.exitEditingImpl(), this.draggableTextDelegate.dispose(), super.dispose();
  }
};
f(Mt, "ownDefaults", kh), f(Mt, "type", "IText"), w.setClass(Mt), w.setClass(Mt, "i-text");
var br = class Yi extends Mt {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Yi.ownDefaults
    };
  }
  constructor(t, r) {
    super(t, {
      ...Yi.ownDefaults,
      ...r
    });
  }
  static createControls() {
    return { controls: an() };
  }
  initDimensions() {
    this.initialized && (this.isEditing && this.initDelayedCursor(), this._clearCache(), this.dynamicMinWidth = 0, this._styleMap = this._generateStyleMap(this._splitText()), this.dynamicMinWidth > this.width && this._set("width", this.dynamicMinWidth), this.textAlign.includes("justify") && this.enlargeSpaces(), this.height = this.calcTextHeight());
  }
  _generateStyleMap(t) {
    let r = 0, i = 0, s = 0, o = {};
    for (let n = 0; n < t.graphemeLines.length; n++) t.graphemeText[s] === `
` && n > 0 ? (i = 0, s++, r++) : !this.splitByGrapheme && this._reSpaceAndTab.test(t.graphemeText[s]) && n > 0 && (i++, s++), o[n] = {
      line: r,
      offset: i
    }, s += t.graphemeLines[n].length, i += t.graphemeLines[n].length;
    return o;
  }
  styleHas(t, r) {
    if (this._styleMap && !this.isWrapping) {
      let i = this._styleMap[r];
      i && (r = i.line);
    }
    return super.styleHas(t, r);
  }
  isEmptyStyles(t) {
    if (!this.styles) return !0;
    let r, i, s = 0, o = !1, n = this._styleMap[t], a = this._styleMap[t + 1];
    n && (t = n.line, s = n.offset), a && (r = a.line, o = r === t, i = a.offset);
    let l = t === void 0 ? this.styles : { line: this.styles[t] };
    for (let h in l) for (let c in l[h]) {
      let u = parseInt(c, 10);
      if (u >= s && (!o || u < i)) for (let d in l[h][c]) return !1;
    }
    return !0;
  }
  _getStyleDeclaration(t, r) {
    if (this._styleMap && !this.isWrapping) {
      let i = this._styleMap[t];
      if (!i) return {};
      t = i.line, r = i.offset + r;
    }
    return super._getStyleDeclaration(t, r);
  }
  _setStyleDeclaration(t, r, i) {
    let s = this._styleMap[t];
    super._setStyleDeclaration(s.line, s.offset + r, i);
  }
  _deleteStyleDeclaration(t, r) {
    let i = this._styleMap[t];
    super._deleteStyleDeclaration(i.line, i.offset + r);
  }
  _getLineStyle(t) {
    let r = this._styleMap[t];
    return !!this.styles[r.line];
  }
  _setLineStyle(t) {
    let r = this._styleMap[t];
    super._setLineStyle(r.line);
  }
  _wrapText(t, r) {
    this.isWrapping = !0;
    let i = this.getGraphemeDataForRender(t), s = [];
    for (let o = 0; o < i.wordsData.length; o++) s.push(...this._wrapLine(o, r, i));
    return this.isWrapping = !1, s;
  }
  getGraphemeDataForRender(t) {
    let r = this.splitByGrapheme, i = r ? "" : " ", s = 0;
    return {
      wordsData: t.map((o, n) => {
        let a = 0, l = r ? this.graphemeSplit(o) : this.wordSplit(o);
        return l.length === 0 ? [{
          word: [],
          width: 0
        }] : l.map((h) => {
          let c = r ? [h] : this.graphemeSplit(h), u = this._measureWord(c, n, a);
          return s = Math.max(u, s), a += c.length + i.length, {
            word: c,
            width: u
          };
        });
      }),
      largestWordWidth: s
    };
  }
  _measureWord(t, r, i = 0) {
    let s, o = 0;
    for (let n = 0, a = t.length; n < a; n++) o += this._getGraphemeBox(t[n], r, n + i, s, !0).kernedWidth, s = t[n];
    return o;
  }
  wordSplit(t) {
    return t.split(this._wordJoiners);
  }
  _wrapLine(t, r, { largestWordWidth: i, wordsData: s }, o = 0) {
    let n = this._getWidthOfCharSpacing(), a = this.splitByGrapheme, l = [], h = a ? "" : " ", c = 0, u = [], d = 0, g = 0, p = !0;
    r -= o;
    let m = Math.max(r, i, this.dynamicMinWidth), x = s[t], _;
    for (_ = 0; _ < x.length; _++) {
      let { word: y, width: S } = x[_];
      d += y.length, c += g + S - n, c > m && !p ? (l.push(u), u = [], c = S, p = !0) : c += n, p || a || u.push(h), u = u.concat(y), g = a ? 0 : this._measureWord([h], t, d), d++, p = !1;
    }
    return _ && l.push(u), i + o > this.dynamicMinWidth && (this.dynamicMinWidth = i - n + o), l;
  }
  isEndOfWrapping(t) {
    return !this._styleMap[t + 1] || this._styleMap[t + 1].line !== this._styleMap[t].line;
  }
  missingNewlineOffset(t, r) {
    return this.splitByGrapheme && !r ? +!!this.isEndOfWrapping(t) : 1;
  }
  _splitTextIntoLines(t) {
    let r = super._splitTextIntoLines(t), i = this._wrapText(r.lines, this.width), s = Array(i.length);
    for (let o = 0; o < i.length; o++) s[o] = i[o].join("");
    return r.lines = s, r.graphemeLines = i, r;
  }
  getMinWidth() {
    return Math.max(this.minWidth, this.dynamicMinWidth);
  }
  _removeExtraneousStyles() {
    let t = /* @__PURE__ */ new Map();
    for (let r in this._styleMap) {
      let i = parseInt(r, 10);
      if (this._textLines[i]) {
        let s = this._styleMap[r].line;
        t.set(`${s}`, !0);
      }
    }
    for (let r in this.styles) t.has(r) || delete this.styles[r];
  }
  toObject(t = []) {
    return super.toObject([
      "minWidth",
      "splitByGrapheme",
      ...t
    ]);
  }
};
f(br, "type", "Textbox"), f(br, "textLayoutProperties", [...Mt.textLayoutProperties, "width"]), f(br, "ownDefaults", {
  minWidth: 20,
  dynamicMinWidth: 2,
  lockScalingFlip: !0,
  noScaleCache: !1,
  _wordJoiners: /[ \t\r]/,
  splitByGrapheme: !1
}), w.setClass(br);
var qs = class extends ei {
  shouldPerformLayout(e) {
    return !!e.target.clipPath && super.shouldPerformLayout(e);
  }
  shouldLayoutClipPath() {
    return !1;
  }
  calcLayoutResult(e, t) {
    let { target: r } = e, { clipPath: i, group: s } = r;
    if (!i || !this.shouldPerformLayout(e)) return;
    let { width: o, height: n } = bt(vn(r, i)), a = new v(o, n);
    if (i.absolutePositioned) return {
      center: Pt(i.getRelativeCenterPoint(), void 0, s ? s.calcTransformMatrix() : void 0),
      size: a
    };
    {
      let l = i.getRelativeCenterPoint().transform(r.calcOwnMatrix(), !0);
      if (this.shouldPerformLayout(e)) {
        let { center: h = new v(), correction: c = new v() } = this.calcBoundingBox(t, e) || {};
        return {
          center: h.add(l),
          correction: c.subtract(l),
          size: a
        };
      }
      return {
        center: r.getRelativeCenterPoint().add(l),
        size: a
      };
    }
  }
};
f(qs, "type", "clip-path"), w.setClass(qs);
var Ks = class extends ei {
  getInitialSize({ target: e }, { size: t }) {
    return new v(e.width || t.x, e.height || t.y);
  }
};
f(Ks, "type", "fixed"), w.setClass(Ks);
var Mh = class extends nr {
  subscribeTargets(e) {
    let t = e.target;
    e.targets.reduce((r, i) => (i.parent && r.add(i.parent), r), /* @__PURE__ */ new Set()).forEach((r) => {
      r.layoutManager.subscribeTargets({
        target: r,
        targets: [t]
      });
    });
  }
  unsubscribeTargets(e) {
    let t = e.target, r = t.getObjects();
    e.targets.reduce((i, s) => (s.parent && i.add(s.parent), i), /* @__PURE__ */ new Set()).forEach((i) => {
      !r.some((s) => s.parent === i) && i.layoutManager.unsubscribeTargets({
        target: i,
        targets: [t]
      });
    });
  }
}, wr = class $i extends me {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...$i.ownDefaults
    };
  }
  constructor(t = [], r = {}) {
    super(), Object.assign(this, $i.ownDefaults), this.setOptions(r);
    let { left: i, top: s, layoutManager: o } = r;
    this.groupInit(t, {
      left: i,
      top: s,
      layoutManager: o ?? new Mh()
    });
  }
  _shouldSetNestedCoords() {
    return !0;
  }
  __objectSelectionMonitor() {
  }
  multiSelectAdd(...t) {
    this.multiSelectionStacking === "selection-order" ? this.add(...t) : t.forEach((r) => {
      let i = this._objects.findIndex((o) => o.isInFrontOf(r)), s = i === -1 ? this.size() : i;
      this.insertAt(s, r);
    });
  }
  canEnterGroup(t) {
    return this.getObjects().some((r) => r.isDescendantOf(t) || t.isDescendantOf(r)) ? (zt("error", "ActiveSelection: circular object trees are not supported, this call has no effect"), !1) : super.canEnterGroup(t);
  }
  enterGroup(t, r) {
    t.parent && t.parent === t.group ? t.parent._exitGroup(t) : t.group && t.parent !== t.group && t.group.remove(t), this._enterGroup(t, r);
  }
  exitGroup(t, r) {
    this._exitGroup(t, r), t.parent && t.parent._enterGroup(t, !0);
  }
  _onAfterObjectsChange(t, r) {
    super._onAfterObjectsChange(t, r);
    let i = /* @__PURE__ */ new Set();
    r.forEach((s) => {
      let { parent: o } = s;
      o && i.add(o);
    }), t === "removed" ? i.forEach((s) => {
      s._onAfterObjectsChange(Ti, r);
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
  _renderControls(t, r, i) {
    t.save(), t.globalAlpha = this.isMoving ? this.borderOpacityWhenMoving : 1;
    let s = {
      hasControls: !1,
      ...i,
      forActiveSelection: !0
    };
    for (let o = 0; o < this._objects.length; o++) this._objects[o]._renderControls(t, s);
    super._renderControls(t, r), t.restore();
  }
};
f(wr, "type", "ActiveSelection"), f(wr, "ownDefaults", { multiSelectionStacking: "canvas-stacking" }), w.setClass(wr), w.setClass(wr, "activeSelection");
var Dh = class {
  constructor() {
    f(this, "resources", {});
  }
  applyFilters(e, t, r, i, s) {
    let o = s.getContext("2d", {
      willReadFrequently: !0,
      desynchronized: !0
    });
    if (!o) return;
    o.drawImage(t, 0, 0, r, i);
    let n = {
      sourceWidth: r,
      sourceHeight: i,
      imageData: o.getImageData(0, 0, r, i),
      originalEl: t,
      originalImageData: o.getImageData(0, 0, r, i),
      canvasEl: s,
      ctx: o,
      filterBackend: this
    };
    e.forEach((l) => {
      l.applyTo(n);
    });
    let { imageData: a } = n;
    return a.width === r && a.height === i || (s.width = a.width, s.height = a.height), o.putImageData(a, 0, 0), n;
  }
}, qn = class {
  constructor({ tileSize: e = P.textureSize } = {}) {
    f(this, "aPosition", new Float32Array([
      0,
      0,
      0,
      1,
      1,
      0,
      1,
      1
    ])), f(this, "resources", {}), this.tileSize = e, this.setupGLContext(e, e), this.captureGPUInfo();
  }
  setupGLContext(e, t) {
    this.dispose(), this.createWebGLCanvas(e, t);
  }
  createWebGLCanvas(e, t) {
    let r = ht({
      width: e,
      height: t
    }), i = r.getContext("webgl", {
      alpha: !0,
      premultipliedAlpha: !1,
      depth: !1,
      stencil: !1,
      antialias: !1
    });
    i && (i.clearColor(0, 0, 0, 0), this.canvas = r, this.gl = i);
  }
  applyFilters(e, t, r, i, s, o) {
    let n = this.gl, a = s.getContext("2d");
    if (!n || !a) return;
    let l;
    o && (l = this.getCachedTexture(o, t));
    let h = {
      originalWidth: t.width || t.naturalWidth || 0,
      originalHeight: t.height || t.naturalHeight || 0,
      sourceWidth: r,
      sourceHeight: i,
      destinationWidth: r,
      destinationHeight: i,
      context: n,
      sourceTexture: this.createTexture(n, r, i, l ? void 0 : t),
      targetTexture: this.createTexture(n, r, i),
      originalTexture: l || this.createTexture(n, r, i, l ? void 0 : t),
      passes: e.length,
      webgl: !0,
      aPosition: this.aPosition,
      programCache: this.programCache,
      pass: 0,
      filterBackend: this,
      targetCanvas: s
    }, c = n.createFramebuffer();
    return n.bindFramebuffer(n.FRAMEBUFFER, c), e.forEach((u) => {
      u && u.applyTo(h);
    }), (function(u) {
      let d = u.targetCanvas, g = d.width, p = d.height, m = u.destinationWidth, x = u.destinationHeight;
      g === m && p === x || (d.width = m, d.height = x);
    })(h), this.copyGLTo2D(n, h), n.bindTexture(n.TEXTURE_2D, null), n.deleteTexture(h.sourceTexture), n.deleteTexture(h.targetTexture), n.deleteFramebuffer(c), a.setTransform(1, 0, 0, 1, 0, 0), h;
  }
  dispose() {
    this.canvas && (this.canvas = null, this.gl = null), this.clearWebGLCaches();
  }
  clearWebGLCaches() {
    this.programCache = {}, this.textureCache = {};
  }
  createTexture(e, t, r, i, s) {
    let { NEAREST: o, TEXTURE_2D: n, RGBA: a, UNSIGNED_BYTE: l, CLAMP_TO_EDGE: h, TEXTURE_MAG_FILTER: c, TEXTURE_MIN_FILTER: u, TEXTURE_WRAP_S: d, TEXTURE_WRAP_T: g } = e, p = e.createTexture();
    return e.bindTexture(n, p), e.texParameteri(n, c, s || o), e.texParameteri(n, u, s || o), e.texParameteri(n, d, h), e.texParameteri(n, g, h), i ? e.texImage2D(n, 0, a, a, l, i) : e.texImage2D(n, 0, a, t, r, 0, a, l, null), p;
  }
  getCachedTexture(e, t, r) {
    let { textureCache: i } = this;
    if (i[e]) return i[e];
    {
      let s = this.createTexture(this.gl, t.width, t.height, t, r);
      return s && (i[e] = s), s;
    }
  }
  evictCachesForKey(e) {
    this.textureCache[e] && (this.gl.deleteTexture(this.textureCache[e]), delete this.textureCache[e]);
  }
  copyGLTo2D(e, t) {
    let r = e.canvas, i = t.targetCanvas, s = i.getContext("2d");
    if (!s) return;
    s.translate(0, i.height), s.scale(1, -1);
    let o = r.height - i.height;
    s.drawImage(r, 0, o, i.width, i.height, 0, 0, i.width, i.height);
  }
  copyGLTo2DPutImageData(e, t) {
    let r = t.targetCanvas.getContext("2d"), i = t.destinationWidth, s = t.destinationHeight, o = i * s * 4;
    if (!r) return;
    let n = new Uint8Array(this.imageBuffer, 0, o), a = new Uint8ClampedArray(this.imageBuffer, 0, o);
    e.readPixels(0, 0, i, s, e.RGBA, e.UNSIGNED_BYTE, n);
    let l = new ImageData(a, i, s);
    r.putImageData(l, 0, 0);
  }
  captureGPUInfo() {
    if (this.gpuInfo) return this.gpuInfo;
    let e = this.gl, t = {
      renderer: "",
      vendor: ""
    };
    if (!e) return t;
    let r = e.getExtension("WEBGL_debug_renderer_info");
    if (r) {
      let i = e.getParameter(r.UNMASKED_RENDERER_WEBGL), s = e.getParameter(r.UNMASKED_VENDOR_WEBGL);
      i && (t.renderer = i.toLowerCase()), s && (t.vendor = s.toLowerCase());
    }
    return this.gpuInfo = t, t;
  }
}, ui;
function Eh() {
  let { WebGLProbe: e } = wt();
  return e.queryWebGL(Tt()), P.enableGLFiltering && e.isSupported(P.textureSize) ? new qn({ tileSize: P.textureSize }) : new Dh();
}
function di(e = !0) {
  return !ui && e && (ui = Eh()), ui;
}
var Kn = ["cropX", "cropY"], $t = class Wi extends q {
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Wi.ownDefaults
    };
  }
  constructor(t, r) {
    super(), f(this, "_lastScaleX", 1), f(this, "_lastScaleY", 1), f(this, "_filterScalingX", 1), f(this, "_filterScalingY", 1), this.filters = [], Object.assign(this, Wi.ownDefaults), this.setOptions(r), this.cacheKey = `texture${Gt()}`, this.setElement(typeof t == "string" ? (this.canvas && gt(this.canvas.getElement()) || we()).getElementById(t) : t, r);
  }
  getElement() {
    return this._element;
  }
  setElement(t, r = {}) {
    this.removeTexture(this.cacheKey), this.removeTexture(`${this.cacheKey}_filtered`), this._element = t, this._originalElement = t, this._setWidthHeight(r), this.filters.length !== 0 && this.applyFilters(), this.resizeFilter && this.applyResizeFilters();
  }
  removeTexture(t) {
    let r = di(!1);
    r instanceof qn && r.evictCachesForKey(t);
  }
  dispose() {
    super.dispose(), this.removeTexture(this.cacheKey), this.removeTexture(`${this.cacheKey}_filtered`), this._cacheContext = null, [
      "_originalElement",
      "_element",
      "_filteredEl",
      "_cacheCanvas"
    ].forEach((t) => {
      let r = this[t];
      r && wt().dispose(r), this[t] = void 0;
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
    let r = this.width / 2, i = this.height / 2;
    t.beginPath(), t.moveTo(-r, -i), t.lineTo(r, -i), t.lineTo(r, i), t.lineTo(-r, i), t.lineTo(-r, -i), t.closePath();
  }
  toObject(t = []) {
    let r = [];
    return this.filters.forEach((i) => {
      i && r.push(i.toObject());
    }), {
      ...super.toObject([...Kn, ...t]),
      src: this.getSrc(),
      crossOrigin: this.getCrossOrigin(),
      filters: r,
      ...this.resizeFilter ? { resizeFilter: this.resizeFilter.toObject() } : {}
    };
  }
  hasCrop() {
    return !!this.cropX || !!this.cropY || this.width < this._element.width || this.height < this._element.height;
  }
  _toSVG() {
    let t = [], r = this._element, i = -this.width / 2, s = -this.height / 2, o = [], n = [], a = "", l = "";
    if (!r) return [];
    if (this.hasCrop()) {
      let h = Gt();
      o.push('<clipPath id="imageCrop_' + h + `">
`, '	<rect x="' + i + '" y="' + s + '" width="' + M(this.width) + '" height="' + M(this.height) + `" />
`, `</clipPath>
`), a = ' clip-path="url(#imageCrop_' + h + ')" ';
    }
    if (this.imageSmoothing || (l = ' image-rendering="optimizeSpeed"'), t.push("	<image ", "COMMON_PARTS", `xlink:href="${M(this.getSrc(!0))}" x="${i - this.cropX}" y="${s - this.cropY}" width="${r.width || r.naturalWidth}" height="${r.height || r.naturalHeight}"${l}${a}></image>
`), this.stroke || this.strokeDashArray) {
      let h = this.fill;
      this.fill = null, n = [`	<rect x="${i}" y="${s}" width="${M(this.width)}" height="${M(this.height)}" style="${this.getSvgStyles()}" />
`], this.fill = h;
    }
    return o = this.paintFirst === "fill" ? o.concat(t, n) : o.concat(n, t), o;
  }
  getSrc(t) {
    let r = t ? this._element : this._originalElement;
    return r ? r.toDataURL ? r.toDataURL() : this.srcFromAttribute ? r.getAttribute("src") || "" : r.src : this.src || "";
  }
  getSvgSrc(t) {
    return this.getSrc(t);
  }
  setSrc(t, { crossOrigin: r, signal: i } = {}) {
    return er(t, {
      crossOrigin: r,
      signal: i
    }).then((s) => {
      r !== void 0 && this.set({ crossOrigin: r }), this.setElement(s);
    });
  }
  toString() {
    return `#<Image: { src: "${this.getSrc()}" }>`;
  }
  applyResizeFilters() {
    let t = this.resizeFilter, r = this.minimumScaleTrigger, i = this.getTotalObjectScaling(), s = i.x, o = i.y, n = this._filteredEl || this._originalElement;
    if (this.group && this.set("dirty", !0), !t || s > r && o > r) return this._element = n, this._filterScalingX = 1, this._filterScalingY = 1, this._lastScaleX = s, void (this._lastScaleY = o);
    let a = ht(n), { width: l, height: h } = n;
    this._element = a, this._lastScaleX = t.scaleX = s, this._lastScaleY = t.scaleY = o, di().applyFilters([t], n, l, h, this._element), this._filterScalingX = a.width / this._originalElement.width, this._filterScalingY = a.height / this._originalElement.height;
  }
  applyFilters(t = this.filters || []) {
    if (t = t.filter((o) => o && !o.isNeutralState()), this.set("dirty", !0), this.removeTexture(`${this.cacheKey}_filtered`), t.length === 0) return this._element = this._originalElement, this._filteredEl = void 0, this._filterScalingX = 1, void (this._filterScalingY = 1);
    let r = this._originalElement, i = r.naturalWidth || r.width, s = r.naturalHeight || r.height;
    if (this._element === this._originalElement) {
      let o = ht({
        width: i,
        height: s
      });
      this._element = o, this._filteredEl = o;
    } else this._filteredEl && (this._element = this._filteredEl, this._filteredEl.getContext("2d").clearRect(0, 0, i, s), this._lastScaleX = 1, this._lastScaleY = 1);
    di().applyFilters(t, this._originalElement, i, s, this._element, this.cacheKey), this._originalElement.width === this._element.width && this._originalElement.height === this._element.height || (this._filterScalingX = this._element.width / this._originalElement.width, this._filterScalingY = this._element.height / this._originalElement.height);
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
    let r = this._element;
    if (!r) return;
    let i = this._filterScalingX, s = this._filterScalingY, o = this.width, n = this.height, a = Math.max(this.cropX, 0), l = Math.max(this.cropY, 0), h = r.naturalWidth || r.width, c = r.naturalHeight || r.height, u = a * i, d = l * s, g = Math.min(o * i, h - u), p = Math.min(n * s, c - d), m = -o / 2, x = -n / 2, _ = Math.min(o, h / i - a), y = Math.min(n, c / s - l);
    r && t.drawImage(r, u, d, g, p, m, x, _, y);
  }
  _needsResize() {
    let t = this.getTotalObjectScaling();
    return t.x !== this._lastScaleX || t.y !== this._lastScaleY;
  }
  _resetWidthHeight() {
    this.set(this.getOriginalSize());
  }
  _setWidthHeight({ width: t, height: r } = {}) {
    let i = this.getOriginalSize();
    this.width = t || i.width, this.height = r || i.height;
  }
  parsePreserveAspectRatioAttribute() {
    let t = Fo(this.preserveAspectRatio || ""), r = this.width, i = this.height, s = {
      width: r,
      height: i
    }, o, n = this._element.width, a = this._element.height, l = 1, h = 1, c = 0, u = 0, d = 0, g = 0;
    return !t || t.alignX === "none" && t.alignY === "none" ? (l = r / n, h = i / a) : (t.meetOrSlice === "meet" && (l = h = xn(this._element, s), o = (r - n * l) / 2, t.alignX === "Min" && (c = -o), t.alignX === "Max" && (c = o), o = (i - a * h) / 2, t.alignY === "Min" && (u = -o), t.alignY === "Max" && (u = o)), t.meetOrSlice === "slice" && (l = h = _n(this._element, s), o = n - r / l, t.alignX === "Mid" && (d = o / 2), t.alignX === "Max" && (d = o), o = a - i / h, t.alignY === "Mid" && (g = o / 2), t.alignY === "Max" && (g = o), n = r / l, a = i / h)), {
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
  static fromObject({ filters: t, resizeFilter: r, src: i, crossOrigin: s, type: o, ...n }, a) {
    return Promise.all([
      er(i, {
        ...a,
        crossOrigin: s
      }),
      t && _e(t, a),
      r ? _e([r], a) : [],
      ur(n, a)
    ]).then(([l, h = [], [c], u = {}]) => new this(l, {
      ...n,
      src: i,
      filters: h,
      resizeFilter: c,
      ...u
    }));
  }
  static fromURL(t, { crossOrigin: r = null, signal: i } = {}, s) {
    return er(t, {
      crossOrigin: r,
      signal: i
    }).then((o) => new this(o, s));
  }
  static async fromElement(t, r = {}, i) {
    let s = Ft(t, this.ATTRIBUTE_NAMES, i);
    return this.fromURL(s["xlink:href"] || s.href, r, s).catch((o) => (zt("log", "Unable to parse Image", o), null));
  }
};
f($t, "type", "Image"), f($t, "cacheProperties", [...At, ...Kn]), f($t, "ownDefaults", {
  strokeWidth: 0,
  srcFromAttribute: !1,
  minimumScaleTrigger: 0.5,
  cropX: 0,
  cropY: 0,
  imageSmoothing: !0
}), f($t, "ATTRIBUTE_NAMES", [
  ...Jt,
  "x",
  "y",
  "width",
  "height",
  "preserveAspectRatio",
  "xlink:href",
  "href",
  "crossOrigin",
  "image-rendering"
]), w.setClass($t), w.setSVGClass($t);
var Nc = Jr([
  "pattern",
  "defs",
  "symbol",
  "metadata",
  "clipPath",
  "mask",
  "desc"
]), ri = (e) => e.webgl !== void 0, Ss = "precision highp float", Ph = `
    ${Ss};
    varying vec2 vTexCoord;
    uniform sampler2D uTexture;
    void main() {
      gl_FragColor = texture2D(uTexture, vTexCoord);
    }`, Ah = new RegExp(Ss, "g"), W = class {
  get type() {
    return this.constructor.type;
  }
  constructor({ type: e, ...t } = {}) {
    Object.assign(this, this.constructor.defaults, t);
  }
  getFragmentSource() {
    return Ph;
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
  createProgram(e, t = this.getFragmentSource(), r = this.getVertexSource()) {
    let { WebGLProbe: { GLPrecision: i = "highp" } } = wt();
    i !== "highp" && (t = t.replace(Ah, Ss.replace("highp", i)));
    let s = e.createShader(e.VERTEX_SHADER), o = e.createShader(e.FRAGMENT_SHADER), n = e.createProgram();
    if (!s || !o || !n) throw new Ct("Vertex, fragment shader or program creation error");
    if (e.shaderSource(s, r), e.compileShader(s), !e.getShaderParameter(s, e.COMPILE_STATUS)) throw new Ct(`Vertex shader compile error for ${this.type}: ${e.getShaderInfoLog(s)}`);
    if (e.shaderSource(o, t), e.compileShader(o), !e.getShaderParameter(o, e.COMPILE_STATUS)) throw new Ct(`Fragment shader compile error for ${this.type}: ${e.getShaderInfoLog(o)}`);
    if (e.attachShader(n, s), e.attachShader(n, o), e.linkProgram(n), !e.getProgramParameter(n, e.LINK_STATUS)) throw new Ct(`Shader link error for "${this.type}" ${e.getProgramInfoLog(n)}`);
    let a = this.getUniformLocations(e, n) || {};
    return a.uStepW = e.getUniformLocation(n, "uStepW"), a.uStepH = e.getUniformLocation(n, "uStepH"), {
      program: n,
      attributeLocations: this.getAttributeLocations(e, n),
      uniformLocations: a
    };
  }
  getAttributeLocations(e, t) {
    return { aPosition: e.getAttribLocation(t, "aPosition") };
  }
  getUniformLocations(e, t) {
    let r = this.constructor.uniformLocations, i = {};
    for (let s = 0; s < r.length; s++) i[r[s]] = e.getUniformLocation(t, r[s]);
    return i;
  }
  sendAttributeData(e, t, r) {
    let i = t.aPosition, s = e.createBuffer();
    e.bindBuffer(e.ARRAY_BUFFER, s), e.enableVertexAttribArray(i), e.vertexAttribPointer(i, 2, e.FLOAT, !1, 0, 0), e.bufferData(e.ARRAY_BUFFER, r, e.STATIC_DRAW);
  }
  _setupFrameBuffer(e) {
    let t = e.context;
    if (e.passes > 1) {
      let r = e.destinationWidth, i = e.destinationHeight;
      e.sourceWidth === r && e.sourceHeight === i || (t.deleteTexture(e.targetTexture), e.targetTexture = e.filterBackend.createTexture(t, r, i)), t.framebufferTexture2D(t.FRAMEBUFFER, t.COLOR_ATTACHMENT0, t.TEXTURE_2D, e.targetTexture, 0);
    } else t.bindFramebuffer(t.FRAMEBUFFER, null), t.finish();
  }
  _swapTextures(e) {
    e.passes--, e.pass++;
    let t = e.targetTexture;
    e.targetTexture = e.sourceTexture, e.sourceTexture = t;
  }
  isNeutralState(e) {
    return !1;
  }
  applyTo(e) {
    ri(e) ? (this._setupFrameBuffer(e), this.applyToWebGL(e), this._swapTextures(e)) : this.applyTo2d(e);
  }
  applyTo2d(e) {
  }
  getCacheKey() {
    return this.type;
  }
  retrieveShader(e) {
    let t = this.getCacheKey();
    return e.programCache[t] || (e.programCache[t] = this.createProgram(e.context)), e.programCache[t];
  }
  applyToWebGL(e) {
    let t = e.context, r = this.retrieveShader(e);
    e.pass === 0 && e.originalTexture ? t.bindTexture(t.TEXTURE_2D, e.originalTexture) : t.bindTexture(t.TEXTURE_2D, e.sourceTexture), t.useProgram(r.program), this.sendAttributeData(t, r.attributeLocations, e.aPosition), t.uniform1f(r.uniformLocations.uStepW, 1 / e.sourceWidth), t.uniform1f(r.uniformLocations.uStepH, 1 / e.sourceHeight), this.sendUniformData(t, r.uniformLocations), t.viewport(0, 0, e.destinationWidth, e.destinationHeight), t.drawArrays(t.TRIANGLE_STRIP, 0, 4);
  }
  bindAdditionalTexture(e, t, r) {
    e.activeTexture(r), e.bindTexture(e.TEXTURE_2D, t), e.activeTexture(e.TEXTURE0);
  }
  unbindAdditionalTexture(e, t) {
    e.activeTexture(t), e.bindTexture(e.TEXTURE_2D, null), e.activeTexture(e.TEXTURE0);
  }
  sendUniformData(e, t) {
  }
  createHelpLayer(e) {
    if (!e.helpLayer) {
      let { sourceWidth: t, sourceHeight: r } = e;
      e.helpLayer = ht({
        width: t,
        height: r
      });
    }
  }
  toObject() {
    let e = Object.keys(this.constructor.defaults || {});
    return {
      type: this.type,
      ...e.reduce((t, r) => (t[r] = this[r], t), {})
    };
  }
  toJSON() {
    return this.toObject();
  }
  static async fromObject({ type: e, ...t }, r) {
    return new this(t);
  }
};
f(W, "type", "BaseFilter"), f(W, "uniformLocations", []);
var jh = {
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
}, Be = class extends W {
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
          ${jh[this.mode]}
        }
      }
      `;
  }
  applyTo2d({ imageData: { data: e } }) {
    let t = new K(this.color).getSource(), r = this.alpha, i = t[0] * r, s = t[1] * r, o = t[2] * r, n = 1 - r;
    for (let a = 0; a < e.length; a += 4) {
      let l = e[a], h = e[a + 1], c = e[a + 2], u, d, g;
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
      e[a] = u, e[a + 1] = d, e[a + 2] = g;
    }
  }
  sendUniformData(e, t) {
    let r = new K(this.color).getSource();
    r[0] = this.alpha * r[0] / 255, r[1] = this.alpha * r[1] / 255, r[2] = this.alpha * r[2] / 255, r[3] = this.alpha, e.uniform4fv(t.uColor, r);
  }
};
f(Be, "defaults", {
  color: "#F95C63",
  mode: "multiply",
  alpha: 1
}), f(Be, "type", "BlendColor"), f(Be, "uniformLocations", ["uColor"]), w.setClass(Be);
var Fh = {
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
}, Ie = class extends W {
  getCacheKey() {
    return `${this.type}_${this.mode}`;
  }
  getFragmentSource() {
    return Fh[this.mode];
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
  applyToWebGL(e) {
    let t = e.context, r = this.createTexture(e.filterBackend, this.image);
    this.bindAdditionalTexture(t, r, t.TEXTURE1), super.applyToWebGL(e), this.unbindAdditionalTexture(t, t.TEXTURE1);
  }
  createTexture(e, t) {
    return e.getCachedTexture(t.cacheKey, t.getElement());
  }
  calculateMatrix() {
    let e = this.image, { width: t, height: r } = e.getElement();
    return [
      1 / e.scaleX,
      0,
      0,
      0,
      1 / e.scaleY,
      0,
      -e.left / t,
      -e.top / r,
      1
    ];
  }
  applyTo2d({ imageData: { data: e, width: t, height: r }, filterBackend: { resources: i } }) {
    let s = this.image;
    i.blendImage || (i.blendImage = Tt());
    let o = i.blendImage, n = o.getContext("2d");
    o.width !== t || o.height !== r ? (o.width = t, o.height = r) : n.clearRect(0, 0, t, r), n.setTransform(s.scaleX, 0, 0, s.scaleY, s.left, s.top), n.drawImage(s.getElement(), 0, 0, t, r);
    let a = n.getImageData(0, 0, t, r).data;
    for (let l = 0; l < e.length; l += 4) {
      let h = e[l], c = e[l + 1], u = e[l + 2], d = e[l + 3], g = a[l], p = a[l + 1], m = a[l + 2], x = a[l + 3];
      switch (this.mode) {
        case "multiply":
          e[l] = h * g / 255, e[l + 1] = c * p / 255, e[l + 2] = u * m / 255, e[l + 3] = d * x / 255;
          break;
        case "mask":
          e[l + 3] = x;
      }
    }
  }
  sendUniformData(e, t) {
    let r = this.calculateMatrix();
    e.uniform1i(t.uImage, 1), e.uniformMatrix3fv(t.uTransformMatrix, !1, r);
  }
  toObject() {
    return {
      ...super.toObject(),
      image: this.image && this.image.toObject()
    };
  }
  static async fromObject({ type: e, image: t, ...r }, i) {
    return $t.fromObject(t, i).then((s) => new this({
      ...r,
      image: s
    }));
  }
};
f(Ie, "type", "BlendImage"), f(Ie, "defaults", {
  mode: "multiply",
  alpha: 1
}), f(Ie, "uniformLocations", ["uTransformMatrix", "uImage"]), w.setClass(Ie);
var Xe = class extends W {
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
  applyTo(e) {
    ri(e) ? (this.aspectRatio = e.sourceWidth / e.sourceHeight, e.passes++, this._setupFrameBuffer(e), this.horizontal = !0, this.applyToWebGL(e), this._swapTextures(e), this._setupFrameBuffer(e), this.horizontal = !1, this.applyToWebGL(e), this._swapTextures(e)) : this.applyTo2d(e);
  }
  applyTo2d({ imageData: { data: e, width: t, height: r } }) {
    this.aspectRatio = t / r, this.horizontal = !0;
    let i = this.getBlurValue() * t, s = new Uint8ClampedArray(e), o = 4 * t;
    for (let n = 0; n < e.length; n += 4) {
      let a = 0, l = 0, h = 0, c = 0, u = 0, d = n - n % o, g = d + o;
      for (let p = -14; p < 15; p++) {
        let m = p / 15, x = 4 * Math.floor(i * m), _ = 1 - Math.abs(m), y = n + x;
        y < d ? y = d : y > g && (y = g);
        let S = e[y + 3] * _;
        a += e[y] * S, l += e[y + 1] * S, h += e[y + 2] * S, c += S, u += _;
      }
      s[n] = a / c, s[n + 1] = l / c, s[n + 2] = h / c, s[n + 3] = c / u;
    }
    this.horizontal = !1, i = this.getBlurValue() * r;
    for (let n = 0; n < s.length; n += 4) {
      let a = 0, l = 0, h = 0, c = 0, u = 0, d = n % o, g = s.length - o + d;
      for (let p = -14; p < 15; p++) {
        let m = p / 15, x = Math.floor(i * m) * o, _ = 1 - Math.abs(m), y = n + x;
        y < d ? y = d : y > g && (y = g);
        let S = s[y + 3] * _;
        a += s[y] * S, l += s[y + 1] * S, h += s[y + 2] * S, c += S, u += _;
      }
      e[n] = a / c, e[n + 1] = l / c, e[n + 2] = h / c, e[n + 3] = c / u;
    }
  }
  sendUniformData(e, t) {
    let r = this.chooseRightDelta();
    e.uniform2fv(t.uDelta, r);
  }
  isNeutralState() {
    return this.blur === 0;
  }
  getBlurValue() {
    let e = 1, { horizontal: t, aspectRatio: r } = this;
    return t ? r > 1 && (e = 1 / r) : r < 1 && (e = r), e * this.blur * 0.12;
  }
  chooseRightDelta() {
    let e = this.getBlurValue();
    return this.horizontal ? [e, 0] : [0, e];
  }
};
f(Xe, "type", "Blur"), f(Xe, "defaults", { blur: 0 }), f(Xe, "uniformLocations", ["uDelta"]), w.setClass(Xe);
var Ye = class extends W {
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
  applyTo2d({ imageData: { data: e } }) {
    let t = Math.round(255 * this.brightness);
    for (let r = 0; r < e.length; r += 4) e[r] += t, e[r + 1] += t, e[r + 2] += t;
  }
  isNeutralState() {
    return this.brightness === 0;
  }
  sendUniformData(e, t) {
    e.uniform1f(t.uBrightness, this.brightness);
  }
};
f(Ye, "type", "Brightness"), f(Ye, "defaults", { brightness: 0 }), f(Ye, "uniformLocations", ["uBrightness"]), w.setClass(Ye);
var Jn = {
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
}, ie = class extends W {
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
  applyTo2d(e) {
    let t = e.imageData.data, r = this.matrix, i = this.colorsOnly;
    for (let s = 0; s < t.length; s += 4) {
      let o = t[s], n = t[s + 1], a = t[s + 2];
      if (t[s] = o * r[0] + n * r[1] + a * r[2] + 255 * r[4], t[s + 1] = o * r[5] + n * r[6] + a * r[7] + 255 * r[9], t[s + 2] = o * r[10] + n * r[11] + a * r[12] + 255 * r[14], !i) {
        let l = t[s + 3];
        t[s] += l * r[3], t[s + 1] += l * r[8], t[s + 2] += l * r[13], t[s + 3] = o * r[15] + n * r[16] + a * r[17] + l * r[18] + 255 * r[19];
      }
    }
  }
  sendUniformData(e, t) {
    let r = this.matrix, i = [
      r[0],
      r[1],
      r[2],
      r[3],
      r[5],
      r[6],
      r[7],
      r[8],
      r[10],
      r[11],
      r[12],
      r[13],
      r[15],
      r[16],
      r[17],
      r[18]
    ], s = [
      r[4],
      r[9],
      r[14],
      r[19]
    ];
    e.uniformMatrix4fv(t.uColorMatrix, !1, i), e.uniform4fv(t.uConstants, s);
  }
  toObject() {
    return {
      ...super.toObject(),
      matrix: [...this.matrix]
    };
  }
};
function le(e, t) {
  var r;
  let i = (f(r = class extends ie {
    toObject() {
      return {
        type: this.type,
        colorsOnly: this.colorsOnly
      };
    }
  }, "type", e), f(r, "defaults", {
    colorsOnly: !1,
    matrix: t
  }), r);
  return w.setClass(i, e), i;
}
f(ie, "type", "ColorMatrix"), f(ie, "defaults", Jn), f(ie, "uniformLocations", ["uColorMatrix", "uConstants"]), w.setClass(ie);
var Lh = le("Brownie", [
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
]), Rh = le("Vintage", [
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
]), Bh = le("Kodachrome", [
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
]), Ih = le("Technicolor", [
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
]), Xh = le("Polaroid", [
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
]), Yh = le("Sepia", [
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
]), $h = le("BlackWhite", [
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
]), Vi = class extends W {
  constructor(e = {}) {
    super(e), this.subFilters = e.subFilters || [];
  }
  applyTo(e) {
    ri(e) && (e.passes += this.subFilters.length - 1), this.subFilters.forEach((t) => {
      t.applyTo(e);
    });
  }
  toObject() {
    return {
      type: this.type,
      subFilters: this.subFilters.map((e) => e.toObject())
    };
  }
  isNeutralState() {
    return !this.subFilters.some((e) => !e.isNeutralState());
  }
  static fromObject(e, t) {
    return Promise.all((e.subFilters || []).map((r) => w.getClass(r.type).fromObject(r, t))).then((r) => new this({ subFilters: r }));
  }
};
f(Vi, "type", "Composed"), w.setClass(Vi);
var $e = class extends W {
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
  applyTo2d({ imageData: { data: e } }) {
    let t = Math.floor(255 * this.contrast), r = 259 * (t + 255) / (255 * (259 - t));
    for (let i = 0; i < e.length; i += 4) e[i] = r * (e[i] - 128) + 128, e[i + 1] = r * (e[i + 1] - 128) + 128, e[i + 2] = r * (e[i + 2] - 128) + 128;
  }
  sendUniformData(e, t) {
    e.uniform1f(t.uContrast, this.contrast);
  }
};
f($e, "type", "Contrast"), f($e, "defaults", { contrast: 0 }), f($e, "uniformLocations", ["uContrast"]), w.setClass($e);
var Wh = {
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
}, We = class extends W {
  getCacheKey() {
    return `${this.type}_${Math.sqrt(this.matrix.length)}_${+!!this.opaque}`;
  }
  getFragmentSource() {
    return Wh[this.getCacheKey()];
  }
  applyTo2d(e) {
    let t = e.imageData, r = t.data, i = this.matrix, s = Math.round(Math.sqrt(i.length)), o = Math.floor(s / 2), n = t.width, a = t.height, l = e.ctx.createImageData(n, a), h = l.data, c = +!!this.opaque, u, d, g, p, m, x, _, y, S, C, b, O, T;
    for (b = 0; b < a; b++) for (C = 0; C < n; C++) {
      for (m = 4 * (b * n + C), u = 0, d = 0, g = 0, p = 0, T = 0; T < s; T++) for (O = 0; O < s; O++) _ = b + T - o, x = C + O - o, _ < 0 || _ >= a || x < 0 || x >= n || (y = 4 * (_ * n + x), S = i[T * s + O], u += r[y] * S, d += r[y + 1] * S, g += r[y + 2] * S, c || (p += r[y + 3] * S));
      h[m] = u, h[m + 1] = d, h[m + 2] = g, h[m + 3] = c ? r[m + 3] : p;
    }
    e.imageData = l;
  }
  sendUniformData(e, t) {
    e.uniform1fv(t.uMatrix, this.matrix);
  }
  toObject() {
    return {
      ...super.toObject(),
      opaque: this.opaque,
      matrix: [...this.matrix]
    };
  }
};
f(We, "type", "Convolute"), f(We, "defaults", {
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
}), f(We, "uniformLocations", [
  "uMatrix",
  "uOpaque",
  "uHalfSize",
  "uSize"
]), w.setClass(We);
var Qn = "Gamma", Ve = class extends W {
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
  constructor(e = {}) {
    super(e), this.gamma = e.gamma || this.constructor.defaults.gamma.concat();
  }
  applyTo2d({ imageData: { data: e } }) {
    let t = this.gamma, r = 1 / t[0], i = 1 / t[1], s = 1 / t[2];
    this.rgbValues || (this.rgbValues = {
      r: /* @__PURE__ */ new Uint8Array(256),
      g: /* @__PURE__ */ new Uint8Array(256),
      b: /* @__PURE__ */ new Uint8Array(256)
    });
    let o = this.rgbValues;
    for (let n = 0; n < 256; n++) o.r[n] = 255 * (n / 255) ** r, o.g[n] = 255 * (n / 255) ** i, o.b[n] = 255 * (n / 255) ** s;
    for (let n = 0; n < e.length; n += 4) e[n] = o.r[e[n]], e[n + 1] = o.g[e[n + 1]], e[n + 2] = o.b[e[n + 2]];
  }
  sendUniformData(e, t) {
    e.uniform3fv(t.uGamma, this.gamma);
  }
  isNeutralState() {
    let { gamma: e } = this;
    return e[0] === 1 && e[1] === 1 && e[2] === 1;
  }
  toObject() {
    return {
      type: Qn,
      gamma: this.gamma.concat()
    };
  }
};
f(Ve, "type", Qn), f(Ve, "defaults", { gamma: [
  1,
  1,
  1
] }), f(Ve, "uniformLocations", ["uGamma"]), w.setClass(Ve);
var Vh = {
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
}, He = class extends W {
  applyTo2d({ imageData: { data: e } }) {
    for (let t, r = 0; r < e.length; r += 4) {
      let i = e[r], s = e[r + 1], o = e[r + 2];
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
      e[r + 2] = e[r + 1] = e[r] = t;
    }
  }
  getCacheKey() {
    return `${this.type}_${this.mode}`;
  }
  getFragmentSource() {
    return Vh[this.mode];
  }
  sendUniformData(e, t) {
    e.uniform1i(t.uMode, 1);
  }
  isNeutralState() {
    return !1;
  }
};
f(He, "type", "Grayscale"), f(He, "defaults", { mode: "average" }), f(He, "uniformLocations", ["uMode"]), w.setClass(He);
var Hh = {
  ...Jn,
  rotation: 0
}, Pr = class extends ie {
  calculateMatrix() {
    let e = this.rotation * Math.PI, t = yt(e), r = xt(e), i = 1 / 3, s = Math.sqrt(i) * r, o = 1 - t;
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
  applyTo(e) {
    this.calculateMatrix(), super.applyTo(e);
  }
  toObject() {
    return {
      type: this.type,
      rotation: this.rotation
    };
  }
};
f(Pr, "type", "HueRotation"), f(Pr, "defaults", Hh), w.setClass(Pr);
var ze = class extends W {
  applyTo2d({ imageData: { data: e } }) {
    for (let t = 0; t < e.length; t += 4) e[t] = 255 - e[t], e[t + 1] = 255 - e[t + 1], e[t + 2] = 255 - e[t + 2], this.alpha && (e[t + 3] = 255 - e[t + 3]);
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
  sendUniformData(e, t) {
    e.uniform1i(t.uInvert, Number(this.invert)), e.uniform1i(t.uAlpha, Number(this.alpha));
  }
};
f(ze, "type", "Invert"), f(ze, "defaults", {
  alpha: !1,
  invert: !0
}), f(ze, "uniformLocations", ["uInvert", "uAlpha"]), w.setClass(ze);
var Ge = class extends W {
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
  applyTo2d({ imageData: { data: e } }) {
    let t = this.noise;
    for (let r = 0; r < e.length; r += 4) {
      let i = (0.5 - Math.random()) * t;
      e[r] += i, e[r + 1] += i, e[r + 2] += i;
    }
  }
  sendUniformData(e, t) {
    e.uniform1f(t.uNoise, this.noise / 255), e.uniform1f(t.uSeed, Math.random());
  }
  isNeutralState() {
    return this.noise === 0;
  }
};
f(Ge, "type", "Noise"), f(Ge, "defaults", { noise: 0 }), f(Ge, "uniformLocations", ["uNoise", "uSeed"]), w.setClass(Ge);
var Ue = class extends W {
  applyTo2d({ imageData: { data: e, width: t, height: r } }) {
    for (let i = 0; i < r; i += this.blocksize) for (let s = 0; s < t; s += this.blocksize) {
      let o = 4 * i * t + 4 * s, n = e[o], a = e[o + 1], l = e[o + 2], h = e[o + 3];
      for (let c = i; c < Math.min(i + this.blocksize, r); c++) for (let u = s; u < Math.min(s + this.blocksize, t); u++) {
        let d = 4 * c * t + 4 * u;
        e[d] = n, e[d + 1] = a, e[d + 2] = l, e[d + 3] = h;
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
  sendUniformData(e, t) {
    e.uniform1f(t.uBlocksize, this.blocksize);
  }
};
f(Ue, "type", "Pixelate"), f(Ue, "defaults", { blocksize: 4 }), f(Ue, "uniformLocations", ["uBlocksize"]), w.setClass(Ue);
var Ne = class extends W {
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
  applyTo2d({ imageData: { data: e } }) {
    let t = 255 * this.distance, r = new K(this.color).getSource(), i = [
      r[0] - t,
      r[1] - t,
      r[2] - t
    ], s = [
      r[0] + t,
      r[1] + t,
      r[2] + t
    ];
    for (let o = 0; o < e.length; o += 4) {
      let n = e[o], a = e[o + 1], l = e[o + 2];
      n > i[0] && a > i[1] && l > i[2] && n < s[0] && a < s[1] && l < s[2] && (e[o + 3] = 0);
    }
  }
  sendUniformData(e, t) {
    let r = new K(this.color).getSource(), i = this.distance, s = [
      0 + r[0] / 255 - i,
      0 + r[1] / 255 - i,
      0 + r[2] / 255 - i,
      1
    ], o = [
      r[0] / 255 + i,
      r[1] / 255 + i,
      r[2] / 255 + i,
      1
    ];
    e.uniform4fv(t.uLow, s), e.uniform4fv(t.uHigh, o);
  }
};
f(Ne, "type", "RemoveColor"), f(Ne, "defaults", {
  color: "#FFFFFF",
  distance: 0.02,
  useAlpha: !1
}), f(Ne, "uniformLocations", ["uLow", "uHigh"]), w.setClass(Ne);
var qe = class extends W {
  sendUniformData(e, t) {
    e.uniform2fv(t.uDelta, this.horizontal ? [1 / this.width, 0] : [0, 1 / this.height]), e.uniform1fv(t.uTaps, this.taps);
  }
  getFilterWindow() {
    let e = this.tempScale;
    return Math.ceil(this.lanczosLobes / e);
  }
  getCacheKey() {
    let e = this.getFilterWindow();
    return `${this.type}_${e}`;
  }
  getFragmentSource() {
    let e = this.getFilterWindow();
    return this.generateShader(e);
  }
  getTaps() {
    let e = this.lanczosCreate(this.lanczosLobes), t = this.tempScale, r = this.getFilterWindow(), i = Array(r);
    for (let s = 1; s <= r; s++) i[s - 1] = e(s * t);
    return i;
  }
  generateShader(e) {
    let t = Array(e);
    for (let r = 1; r <= e; r++) t[r - 1] = `${r}.0 * uDelta`;
    return `
      precision highp float;
      uniform sampler2D uTexture;
      uniform vec2 uDelta;
      varying vec2 vTexCoord;
      uniform float uTaps[${e}];
      void main() {
        vec4 color = texture2D(uTexture, vTexCoord);
        float sum = 1.0;
        ${t.map((r, i) => `
              color += texture2D(uTexture, vTexCoord + ${r}) * uTaps[${i}] + texture2D(uTexture, vTexCoord - ${r}) * uTaps[${i}];
              sum += 2.0 * uTaps[${i}];
            `).join(`
`)}
        gl_FragColor = color / sum;
      }
    `;
  }
  applyToForWebgl(e) {
    e.passes++, this.width = e.sourceWidth, this.horizontal = !0, this.dW = Math.round(this.width * this.scaleX), this.dH = e.sourceHeight, this.tempScale = this.dW / this.width, this.taps = this.getTaps(), e.destinationWidth = this.dW, super.applyTo(e), e.sourceWidth = e.destinationWidth, this.height = e.sourceHeight, this.horizontal = !1, this.dH = Math.round(this.height * this.scaleY), this.tempScale = this.dH / this.height, this.taps = this.getTaps(), e.destinationHeight = this.dH, super.applyTo(e), e.sourceHeight = e.destinationHeight;
  }
  applyTo(e) {
    ri(e) ? this.applyToForWebgl(e) : this.applyTo2d(e);
  }
  isNeutralState() {
    return this.scaleX === 1 && this.scaleY === 1;
  }
  lanczosCreate(e) {
    return (t) => {
      if (t >= e || t <= -e) return 0;
      if (t < 11920929e-14 && t > -11920929e-14) return 1;
      let r = (t *= Math.PI) / e;
      return Math.sin(t) / t * Math.sin(r) / r;
    };
  }
  applyTo2d(e) {
    let t = e.imageData, r = this.scaleX, i = this.scaleY;
    this.rcpScaleX = 1 / r, this.rcpScaleY = 1 / i;
    let s = t.width, o = t.height, n = Math.round(s * r), a = Math.round(o * i), l;
    l = this.resizeType === "sliceHack" ? this.sliceByTwo(e, s, o, n, a) : this.resizeType === "hermite" ? this.hermiteFastResize(e, s, o, n, a) : this.resizeType === "bilinear" ? this.bilinearFiltering(e, s, o, n, a) : this.resizeType === "lanczos" ? this.lanczosResize(e, s, o, n, a) : new ImageData(n, a), e.imageData = l;
  }
  sliceByTwo(e, t, r, i, s) {
    let o = e.imageData, n = 0.5, a = !1, l = !1, h = t * n, c = r * n, u = e.filterBackend.resources, d = 0, g = 0, p = t, m = 0;
    u.sliceByTwo || (u.sliceByTwo = Tt());
    let x = u.sliceByTwo;
    (x.width < 1.5 * t || x.height < r) && (x.width = 1.5 * t, x.height = r);
    let _ = x.getContext("2d");
    for (_.clearRect(0, 0, 1.5 * t, r), _.putImageData(o, 0, 0), i = Math.floor(i), s = Math.floor(s); !a || !l; ) t = h, r = c, i < Math.floor(h * n) ? h = Math.floor(h * n) : (h = i, a = !0), s < Math.floor(c * n) ? c = Math.floor(c * n) : (c = s, l = !0), _.drawImage(x, d, g, t, r, p, m, h, c), d = p, g = m, m += c;
    return _.getImageData(d, g, i, s);
  }
  lanczosResize(e, t, r, i, s) {
    let o = e.imageData.data, n = e.ctx.createImageData(i, s), a = n.data, l = this.lanczosCreate(this.lanczosLobes), h = this.rcpScaleX, c = this.rcpScaleY, u = 2 / this.rcpScaleX, d = 2 / this.rcpScaleY, g = Math.ceil(h * this.lanczosLobes / 2), p = Math.ceil(c * this.lanczosLobes / 2), m = {}, x = {
      x: 0,
      y: 0
    }, _ = {
      x: 0,
      y: 0
    };
    return (function y(S) {
      let C, b, O, T, k, D, B, A, E, R, X;
      for (x.x = (S + 0.5) * h, _.x = Math.floor(x.x), C = 0; C < s; C++) {
        for (x.y = (C + 0.5) * c, _.y = Math.floor(x.y), k = 0, D = 0, B = 0, A = 0, E = 0, b = _.x - g; b <= _.x + g; b++) if (!(b < 0 || b >= t)) {
          R = Math.floor(1e3 * Math.abs(b - x.x)), m[R] || (m[R] = {});
          for (let G = _.y - p; G <= _.y + p; G++) G < 0 || G >= r || (X = Math.floor(1e3 * Math.abs(G - x.y)), m[R][X] || (m[R][X] = l(Math.sqrt((R * u) ** 2 + (X * d) ** 2) / 1e3)), O = m[R][X], O > 0 && (T = 4 * (G * t + b), k += O, D += O * o[T], B += O * o[T + 1], A += O * o[T + 2], E += O * o[T + 3]));
        }
        T = 4 * (C * i + S), a[T] = D / k, a[T + 1] = B / k, a[T + 2] = A / k, a[T + 3] = E / k;
      }
      return ++S < i ? y(S) : n;
    })(0);
  }
  bilinearFiltering(e, t, r, i, s) {
    let o, n, a, l, h, c, u, d, g, p, m, x, _, y = 0, S = this.rcpScaleX, C = this.rcpScaleY, b = 4 * (t - 1), O = e.imageData.data, T = e.ctx.createImageData(i, s), k = T.data;
    for (u = 0; u < s; u++) for (d = 0; d < i; d++) for (h = Math.floor(S * d), c = Math.floor(C * u), g = S * d - h, p = C * u - c, _ = 4 * (c * t + h), m = 0; m < 4; m++) o = O[_ + m], n = O[_ + 4 + m], a = O[_ + b + m], l = O[_ + b + 4 + m], x = o * (1 - g) * (1 - p) + n * g * (1 - p) + a * p * (1 - g) + l * g * p, k[y++] = x;
    return T;
  }
  hermiteFastResize(e, t, r, i, s) {
    let o = this.rcpScaleX, n = this.rcpScaleY, a = Math.ceil(o / 2), l = Math.ceil(n / 2), h = e.imageData.data, c = e.ctx.createImageData(i, s), u = c.data;
    for (let d = 0; d < s; d++) for (let g = 0; g < i; g++) {
      let p = 4 * (g + d * i), m, x = 0, _ = 0, y = 0, S = 0, C = 0, b = 0, O = (d + 0.5) * n;
      for (let T = Math.floor(d * n); T < (d + 1) * n; T++) {
        let k = Math.abs(O - (T + 0.5)) / l, D = (g + 0.5) * o, B = k * k;
        for (let A = Math.floor(g * o); A < (g + 1) * o; A++) {
          let E = Math.abs(D - (A + 0.5)) / a, R = Math.sqrt(B + E * E);
          R > 1 && R < -1 || (m = 2 * R * R * R - 3 * R * R + 1, m > 0 && (E = 4 * (A + T * t), b += m * h[E + 3], _ += m, h[E + 3] < 255 && (m = m * h[E + 3] / 250), y += m * h[E], S += m * h[E + 1], C += m * h[E + 2], x += m));
        }
      }
      u[p] = y / x, u[p + 1] = S / x, u[p + 2] = C / x, u[p + 3] = b / _;
    }
    return c;
  }
};
f(qe, "type", "Resize"), f(qe, "defaults", {
  resizeType: "hermite",
  scaleX: 1,
  scaleY: 1,
  lanczosLobes: 3
}), f(qe, "uniformLocations", ["uDelta", "uTaps"]), w.setClass(qe);
var Ke = class extends W {
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
  applyTo2d({ imageData: { data: e } }) {
    let t = -this.saturation;
    for (let r = 0; r < e.length; r += 4) {
      let i = e[r], s = e[r + 1], o = e[r + 2], n = Math.max(i, s, o);
      e[r] += n === i ? 0 : (n - i) * t, e[r + 1] += n === s ? 0 : (n - s) * t, e[r + 2] += n === o ? 0 : (n - o) * t;
    }
  }
  sendUniformData(e, t) {
    e.uniform1f(t.uSaturation, -this.saturation);
  }
  isNeutralState() {
    return this.saturation === 0;
  }
};
f(Ke, "type", "Saturation"), f(Ke, "defaults", { saturation: 0 }), f(Ke, "uniformLocations", ["uSaturation"]), w.setClass(Ke);
var Je = class extends W {
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
  applyTo2d({ imageData: { data: e } }) {
    let t = -this.vibrance;
    for (let r = 0; r < e.length; r += 4) {
      let i = e[r], s = e[r + 1], o = e[r + 2], n = Math.max(i, s, o), a = (i + s + o) / 3, l = 2 * Math.abs(n - a) / 255 * t;
      e[r] += n === i ? 0 : (n - i) * l, e[r + 1] += n === s ? 0 : (n - s) * l, e[r + 2] += n === o ? 0 : (n - o) * l;
    }
  }
  sendUniformData(e, t) {
    e.uniform1f(t.uVibrance, -this.vibrance);
  }
  isNeutralState() {
    return this.vibrance === 0;
  }
};
f(Je, "type", "Vibrance"), f(Je, "defaults", { vibrance: 0 }), f(Je, "uniformLocations", ["uVibrance"]), w.setClass(Je);
var qc = hr({
  BaseFilter: () => W,
  BlackWhite: () => $h,
  BlendColor: () => Be,
  BlendImage: () => Ie,
  Blur: () => Xe,
  Brightness: () => Ye,
  Brownie: () => Lh,
  ColorMatrix: () => ie,
  Composed: () => Vi,
  Contrast: () => $e,
  Convolute: () => We,
  Gamma: () => Ve,
  Grayscale: () => He,
  HueRotation: () => Pr,
  Invert: () => ze,
  Kodachrome: () => Bh,
  Noise: () => Ge,
  Pixelate: () => Ue,
  Polaroid: () => Xh,
  RemoveColor: () => Ne,
  Resize: () => qe,
  Saturation: () => Ke,
  Sepia: () => Yh,
  Technicolor: () => Ih,
  Vibrance: () => Je,
  Vintage: () => Rh
}), Zn = (e, t, r) => {
  const i = e.width ?? t.width, s = e.height ?? t.height;
  if (r === "contain") {
    const a = Math.min(i / t.width, s / t.height), l = (i - t.width * a) / 2, h = (s - t.height * a) / 2;
    return t.set({
      left: l,
      top: h,
      originX: "left",
      originY: "top",
      scaleX: a,
      scaleY: a
    }), {
      naturalWidth: t.width,
      naturalHeight: t.height,
      scaleX: a,
      scaleY: a,
      offsetX: l,
      offsetY: h
    };
  }
  const o = i / t.width, n = s / t.height;
  return t.set({
    left: 0,
    top: 0,
    originX: "left",
    originY: "top",
    scaleX: o,
    scaleY: n
  }), {
    naturalWidth: t.width,
    naturalHeight: t.height,
    scaleX: o,
    scaleY: n,
    offsetX: 0,
    offsetY: 0
  };
}, zh = async (e, t, r, i) => {
  if (!t)
    return e.backgroundImage = void 0, e.renderAll(), null;
  const s = await $t.fromURL(t);
  if (!r()) return null;
  const o = Zn(e, s, i);
  return e.backgroundImage = s, e.renderAll(), o;
}, Gh = (e, t) => {
  const r = e.backgroundImage;
  if (!r) return null;
  const i = Zn(e, r, t);
  return e.renderAll(), i;
}, Uh = (e, t) => {
  let r = null, i = null;
  const s = (o) => {
    i = { value: o }, r !== null && clearTimeout(r), r = setTimeout(() => {
      r = null;
      const n = i;
      i = null, e(n.value);
    }, t);
  };
  return s.cancel = () => {
    r !== null && (clearTimeout(r), r = null), i = null;
  }, s;
}, Nh = (e, t) => {
  const r = Uh(e, t);
  return {
    schedule: (i) => r(i),
    now: (i) => {
      r.cancel(), e(i);
    },
    cancel: () => r.cancel()
  };
}, qh = 100, Js = (e) => e == null ? !0 : typeof e != "object" ? !1 : Object.keys(e).length === 0, Qs = (e, t) => JSON.stringify(e) === JSON.stringify(t), Kh = class {
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
  save(e) {
    if (Js(this.currentState))
      return this.undoStack = [], this.redoStack = [], this.initialState = e, this.currentState = e, !1;
    if (Qs(e, this.currentState)) return !1;
    const t = this.undoStack.length >= qh;
    return this.undoStack = [...this.undoStack.slice(t ? 1 : 0), this.currentState], this.redoStack = [], this.initialState == null && (this.initialState = this.currentState), this.currentState = e, !0;
  }
  undo() {
    if (Js(this.currentState) || Qs(this.initialState, this.currentState)) return !1;
    const e = this.undoStack.length === 0;
    return this.redoStack = [...this.redoStack, this.currentState], e || (this.currentState = this.undoStack[this.undoStack.length - 1]), this.undoStack = this.undoStack.slice(0, -1), !0;
  }
  redo() {
    return this.redoStack.length === 0 ? !1 : (this.undoStack = [...this.undoStack, this.currentState], this.currentState = this.redoStack[this.redoStack.length - 1], this.redoStack = this.redoStack.slice(0, -1), !0);
  }
  reset(e) {
    this.undoStack = [], this.redoStack = [], this.initialState = e, this.currentState = e;
  }
}, Jh = {
  upload: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 18V6"/><path d="M7 11l5-5 5 5"/><path d="M5 21h14"/></svg>',
  undo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-2"/></svg>',
  redo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14l5-5-5-5"/><path d="M20 9H10a6 6 0 0 0 0 12h2"/></svg>',
  bin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13h10l1-13"/></svg>',
  forward: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M12 16V8"/><path d="M8 12l4-4 4 4"/></svg>',
  backward: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M12 8v8"/><path d="M8 12l4 4 4-4"/></svg>',
  deleteSelected: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="M6 6l12 12"/></svg>',
  edit: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>'
}, Xt = (e, t, r) => {
  const i = document.createElement("button");
  return i.type = "button", i.className = "dc-icon-button", i.title = t, i.setAttribute("aria-label", t), i.innerHTML = Jh[e], i.addEventListener("click", r), i;
}, Qh = (e, t) => {
  e.innerHTML = "";
  const r = document.createElement("div");
  r.className = "dc-toolbar-card", e.appendChild(r);
  const i = Xt("upload", "Update the app with this drawing", t.onSend), s = Xt("undo", "Undo", t.onUndo), o = Xt("redo", "Redo", t.onRedo), n = document.createElement("div");
  n.className = "dc-toolbar-separator";
  const a = Xt("edit", "Edit", t.onEditToggle);
  a.setAttribute("aria-pressed", "false");
  const l = Xt("forward", "Bring forward", t.onBringForward), h = Xt("backward", "Send backward", t.onSendBackward), c = Xt("deleteSelected", "Delete selected", t.onDeleteSelected), u = document.createElement("div");
  u.className = "dc-toolbar-contextual", u.append(l, h, c);
  const d = Xt("bin", "Reset canvas & history", t.onReset);
  return r.append(i, s, o, n, a, u, d), {
    undoButton: s,
    redoButton: o,
    editButton: a,
    contextualGroup: u,
    bringForwardButton: l,
    sendBackwardButton: h,
    deleteSelectedButton: c
  };
}, Zh = (e, t, r, i, s) => {
  e.undoButton.disabled = !t, e.redoButton.disabled = !r, e.editButton.setAttribute("aria-pressed", String(i)), e.contextualGroup.style.display = i ? "flex" : "none", e.bringForwardButton.disabled = !s, e.sendBackwardButton.disabled = !s, e.deleteSelectedButton.disabled = !s;
}, Lt = class {
  canvas;
  constructor(e) {
    this.canvas = e;
  }
}, tc = (e, t) => {
  const r = t.x - e.x, i = t.y - e.y;
  return Math.sqrt(r * r + i * i);
}, ec = class extends Lt {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentCircle = new it();
  currentStartX = 0;
  currentStartY = 0;
  minRadius = 10;
  configureCanvas({ strokeWidth: e, strokeColor: t, fillColor: r }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((a) => a.selectable = a.evented = !1), this.strokeWidth = e, this.strokeColor = t, this.fillColor = r, this.minRadius = e;
    const i = (a) => this.onMouseDown(a), s = (a) => this.onMouseMove(a), o = () => this.onMouseUp(), n = () => this.onMouseOut();
    return this.canvas.on("mouse:down", i), this.canvas.on("mouse:move", s), this.canvas.on("mouse:up", o), this.canvas.on("mouse:out", n), () => {
      this.canvas.off("mouse:down", i), this.canvas.off("mouse:move", s), this.canvas.off("mouse:up", o), this.canvas.off("mouse:out", n);
    };
  }
  onMouseDown(e) {
    const t = this.canvas, r = e.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(e.e);
    this.currentStartX = i.x, this.currentStartY = i.y, this.currentCircle = new it({
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
    }), r === 0 && t.add(this.currentCircle);
  }
  onMouseMove(e) {
    if (!this.isMouseDown) return;
    const t = this.canvas, r = t.getScenePoint(e.e), i = tc({
      x: this.currentStartX,
      y: this.currentStartY
    }, {
      x: r.x,
      y: r.y
    }) / 2;
    this.currentCircle.set({
      radius: Math.max(i, this.minRadius),
      angle: Math.atan2(r.y - this.currentStartY, r.x - this.currentStartX) * 180 / Math.PI
    }), this.currentCircle.setCoords(), t.renderAll();
  }
  onMouseUp() {
    this.isMouseDown = !1;
  }
  onMouseOut() {
    this.isMouseDown = !1;
  }
}, rc = class extends Lt {
  configureCanvas({ strokeWidth: e, strokeColor: t }) {
    return this.canvas.isDrawingMode = !0, this.canvas.freeDrawingBrush = new _h(this.canvas), this.canvas.freeDrawingBrush.width = e, this.canvas.freeDrawingBrush.color = t, () => {
    };
  }
}, ic = class extends Lt {
  isMouseDown = !1;
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentLine = new kt();
  configureCanvas({ strokeWidth: e, strokeColor: t }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((n) => n.selectable = n.evented = !1), this.strokeWidth = e, this.strokeColor = t;
    const r = (n) => this.onMouseDown(n), i = (n) => this.onMouseMove(n), s = () => this.onMouseUp(), o = () => this.onMouseOut();
    return this.canvas.on("mouse:down", r), this.canvas.on("mouse:move", i), this.canvas.on("mouse:up", s), this.canvas.on("mouse:out", o), () => {
      this.canvas.off("mouse:down", r), this.canvas.off("mouse:move", i), this.canvas.off("mouse:up", s), this.canvas.off("mouse:out", o);
    };
  }
  onMouseDown(e) {
    const t = this.canvas, r = e.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(e.e);
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
    }), r === 0 && t.add(this.currentLine);
  }
  onMouseMove(e) {
    if (!this.isMouseDown) return;
    const t = this.canvas, r = t.getScenePoint(e.e);
    this.currentLine.set({
      x2: r.x,
      y2: r.y
    }), this.currentLine.setCoords(), t.renderAll();
  }
  onMouseUp() {
    this.isMouseDown = !1;
    const e = this.canvas;
    this.currentLine.width === 0 && this.currentLine.height === 0 && e.remove(this.currentLine);
  }
  onMouseOut() {
    this.isMouseDown = !1;
  }
}, sc = (e, t) => {
  if (e.length === 0) return "M 0 0";
  const [r, ...i] = e, s = [`M ${r.x} ${r.y}`, ...i.map((o) => `L ${o.x} ${o.y}`)];
  return t && s.push("z"), s.join(" ");
}, oc = 3, nc = 10, ac = class extends Lt {
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  handleColor = "#31333f";
  handleStrokeColor = "#fff";
  points = [];
  handles = [];
  currentPath = null;
  onPolygonClosed = () => {
  };
  configureCanvas({ strokeWidth: e, strokeColor: t, fillColor: r, onPolygonClosed: i, pointEditCornerColor: s, pointEditCornerStrokeColor: o }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((a) => a.selectable = a.evented = !1), this.strokeWidth = e, this.strokeColor = t, this.fillColor = r, this.onPolygonClosed = i, this.handleColor = s, this.handleStrokeColor = o, this.points = [], this.handles = [], this.currentPath = null;
    const n = (a) => this.onMouseDown(a);
    return this.canvas.on("mouse:down", n), () => {
      this.canvas.off("mouse:down", n), this.removeHandles(), this.currentPath && (this.canvas.remove(this.currentPath), this.currentPath = null);
    };
  }
  onMouseDown(e) {
    if (e.e.button !== 0) return;
    const t = this.handles.indexOf(e.target);
    if (t === 0) {
      this.points.length >= oc && this.close();
      return;
    }
    if (t > 0) {
      this.removeVertex(t);
      return;
    }
    const r = this.canvas.getScenePoint(e.e);
    this.addVertex(r);
  }
  addVertex(e) {
    const t = new it({
      left: e.x,
      top: e.y,
      originX: "center",
      originY: "center",
      radius: nc,
      fill: this.handleColor,
      stroke: this.handleStrokeColor,
      strokeWidth: 2,
      selectable: !1,
      evented: !0,
      hoverCursor: "pointer",
      excludeFromExport: !0
    });
    this.points.push(e), this.handles.push(t), this.canvas.add(t), this.render();
  }
  removeVertex(e) {
    this.canvas.remove(this.handles[e]), this.handles.splice(e, 1), this.points.splice(e, 1), this.render();
  }
  close() {
    this.currentPath && this.canvas.remove(this.currentPath), this.removeHandles();
    const e = new Vt(this.points, {
      strokeWidth: this.strokeWidth,
      fill: this.fillColor,
      stroke: this.strokeColor,
      selectable: !1,
      evented: !1
    });
    this.canvas.add(e), this.points = [], this.currentPath = null, this.onPolygonClosed();
  }
  removeHandles() {
    this.handles.forEach((e) => this.canvas.remove(e)), this.handles = [];
  }
  render(e = !1) {
    const t = this.canvas;
    this.currentPath && t.remove(this.currentPath), this.currentPath = this.points.length >= 2 ? new Wt(sc(this.points, e), {
      strokeWidth: this.strokeWidth,
      fill: this.fillColor,
      stroke: this.strokeColor,
      originX: "center",
      originY: "center",
      selectable: !1,
      evented: !1
    }) : null, this.currentPath && t.add(this.currentPath), this.handles.forEach((r) => t.bringObjectToFront(r)), t.renderAll();
  }
}, lc = class extends Lt {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentRect = new rt();
  currentStartX = 0;
  currentStartY = 0;
  minLength = 10;
  configureCanvas({ strokeWidth: e, strokeColor: t, fillColor: r }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((a) => a.selectable = a.evented = !1), this.strokeWidth = e, this.strokeColor = t, this.fillColor = r, this.minLength = e;
    const i = (a) => this.onMouseDown(a), s = (a) => this.onMouseMove(a), o = () => this.onMouseUp(), n = () => this.onMouseOut();
    return this.canvas.on("mouse:down", i), this.canvas.on("mouse:move", s), this.canvas.on("mouse:up", o), this.canvas.on("mouse:out", n), () => {
      this.canvas.off("mouse:down", i), this.canvas.off("mouse:move", s), this.canvas.off("mouse:up", o), this.canvas.off("mouse:out", n);
    };
  }
  onMouseDown(e) {
    const t = this.canvas, r = e.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(e.e);
    this.currentStartX = i.x, this.currentStartY = i.y, this.currentRect = new rt({
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
    }), r === 0 && t.add(this.currentRect);
  }
  onMouseMove(e) {
    if (!this.isMouseDown) return;
    const t = this.canvas, r = t.getScenePoint(e.e);
    this.currentStartX > r.x && this.currentRect.set({ left: Math.abs(r.x) }), this.currentStartY > r.y && this.currentRect.set({ top: Math.abs(r.y) });
    const i = Math.abs(this.currentStartX - r.x), s = Math.abs(this.currentStartY - r.y);
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
}, Ht = [
  "lockMovementX",
  "lockMovementY",
  "lockRotation",
  "lockScalingX",
  "lockScalingY",
  "lockSkewingX",
  "lockSkewingY",
  "lockScalingFlip"
], hc = (e) => typeof e == "string" && e.toLowerCase() === "z", cc = (e) => {
  const t = [];
  let r = !1;
  for (const i of e) {
    if (!Array.isArray(i) || i.length === 0) return null;
    const [s, ...o] = i;
    if (typeof s != "string") return null;
    const n = s.toUpperCase();
    if (n === "M" || n === "L") {
      if (o.length !== 2) return null;
      t.push({
        x: o[0],
        y: o[1]
      });
    } else if (hc(s)) r = !0;
    else return null;
  }
  return !r || t.length < 3 ? null : t;
}, uc = (e, t) => {
  const r = e / 2, i = t / 2;
  return [
    {
      x: -r,
      y: -i
    },
    {
      x: r,
      y: -i
    },
    {
      x: r,
      y: i
    },
    {
      x: -r,
      y: i
    }
  ];
}, dc = (e, t) => e.map((r) => ({
  x: t[0] * r.x + t[2] * r.y,
  y: t[1] * r.x + t[3] * r.y
})), gc = (e, t) => e.length <= 3 ? null : e.filter((r, i) => i !== t), fc = (e, t) => Math.hypot(t.x - e.x, t.y - e.y), pc = [
  "fill",
  "stroke",
  "strokeWidth",
  "strokeUniform",
  "strokeDashArray",
  "opacity",
  "flipX",
  "flipY",
  "visible",
  "globalCompositeOperation",
  "shadow",
  "selectable",
  "evented"
], mc = (e) => {
  if (e instanceof rt) return uc(e.width, e.height);
  const t = cc(e.path);
  if (!t) return null;
  const { x: r, y: i } = e.pathOffset;
  return t.map((s) => ({
    x: s.x - r,
    y: s.y - i
  }));
}, ta = (e, t) => {
  const r = mc(t);
  if (!r) return null;
  const { angle: i, scaleX: s, scaleY: o, skewX: n, skewY: a } = ar.qrDecompose(t.calcOwnMatrix()), l = ar.composeMatrix({
    angle: 0,
    scaleX: s,
    scaleY: o,
    skewX: n,
    skewY: a
  }), h = dc(r, [
    l[0],
    l[1],
    l[2],
    l[3]
  ]), c = {
    angle: i,
    scaleX: 1,
    scaleY: 1,
    skewX: 0,
    skewY: 0
  }, u = t;
  for (const p of pc) c[p] = u[p];
  for (const p of Ht) c[p] = u[p];
  const d = new Vt(h, c);
  d.setPositionByOrigin(t.getCenterPoint(), "center", "center");
  const g = e.getObjects().indexOf(t);
  return e.remove(t), e.insertAt(g, d), d;
}, ea = (e) => {
  let t = !1;
  for (const r of e.getObjects()) r instanceof Wt && ta(e, r) && (t = !0);
  return t;
}, vc = 3, yc = (e, t) => {
  let r = null;
  return {
    mouseDownHandler: (i, s, o, n) => (r = {
      x: o,
      y: n
    }, !0),
    mouseUpHandler: (i, s, o, n) => {
      const a = !!r && fc(r, {
        x: o,
        y: n
      }) < vc;
      return r = null, a && t(e), !0;
    }
  };
}, ra = (e) => {
  const t = ch.createPolyControls(e, { cursorStyle: "pointer" });
  for (const [r, i] of Object.entries(t)) {
    const s = Number(r.slice(1));
    Object.assign(i, yc(s, (o) => {
      const n = o === 0 ? 1 : 0, a = e.points[n], l = new v(a.x, a.y).subtract(e.pathOffset).transform(e.calcOwnMatrix()), h = gc(e.points, o);
      if (!h) return;
      e.points = h, e.setDimensions();
      const c = new v(a.x, a.y).subtract(e.pathOffset).transform(e.calcOwnMatrix());
      e.left -= c.x - l.x, e.top -= c.y - l.y, ra(e), e.setCoords(), e.canvas?.requestRenderAll();
    }));
  }
  e.controls = t;
}, xc = (e) => {
  const t = (r) => new V({
    cursorStyle: "pointer",
    positionHandler: (i, s, o) => {
      const n = o, a = n.calcLinePoints();
      return new v(r === 1 ? a.x1 : a.x2, r === 1 ? a.y1 : a.y2).transform(ar.multiplyTransformMatrices(n.getViewportTransform(), n.calcTransformMatrix()));
    },
    actionHandler: (i, s, o, n) => {
      const a = s.target, l = a.calcLinePoints(), h = r === 1 ? {
        x: l.x2,
        y: l.y2
      } : {
        x: l.x1,
        y: l.y1
      }, c = new v(h.x, h.y).transform(a.calcTransformMatrix()), u = ar.sendPointToPlane(new v(o, n), void 0, a.calcOwnMatrix()), d = (a.x1 + a.x2) / 2, g = (a.y1 + a.y2) / 2;
      a.set(r === 1 ? {
        x1: d + u.x,
        y1: g + u.y
      } : {
        x2: d + u.x,
        y2: g + u.y
      });
      const p = new v(o, n), m = c.add(p).scalarDivide(2);
      return a.set({
        left: m.x,
        top: m.y
      }), a.setCoords(), !0;
    }
  });
  e.controls = {
    p1: t(1),
    p2: t(2)
  };
}, _c = (e) => {
  const t = (r, i) => new V({
    x: r,
    y: i,
    cursorStyle: "pointer",
    actionHandler: (s, o, n, a) => {
      const l = o.target, h = l.getCenterPoint(), c = new v(n, a).distanceFrom(h) / (l.scaleX || 1);
      return l.set({
        radius: c,
        scaleX: 1,
        scaleY: 1
      }), l.setPositionByOrigin(h, "center", "center"), l.setCoords(), !0;
    }
  });
  e.controls = {
    r0: t(0.5, 0),
    r1: t(-0.5, 0),
    r2: t(0, 0.5),
    r3: t(0, -0.5)
  };
}, Sc = (e) => {
  e.controls = {
    tl: new V({
      x: -0.5,
      y: -0.5,
      actionHandler: () => !1
    }),
    tr: new V({
      x: 0.5,
      y: -0.5,
      actionHandler: () => !1
    }),
    br: new V({
      x: 0.5,
      y: 0.5,
      actionHandler: () => !1
    }),
    bl: new V({
      x: -0.5,
      y: 0.5,
      actionHandler: () => !1
    })
  };
}, Cc = (e, t, r) => {
  const i = (s) => {
    const o = t();
    if (!(o instanceof rt) || !o.findControl(e.getViewportPoint(s.e), ar.isTouchEvent(s.e))) return;
    const n = ta(e, o);
    n && (e.setActiveObject(n), r(n), e._resetTransformEventData());
  };
  return e.on("mouse:down:before", i), () => e.off("mouse:down:before", i);
}, ia = (e, t) => e + 2 * t, sa = (e, t, r) => e - t - r < 0, oa = (e) => {
  const [t, r, i] = e;
  return (0.299 * t + 0.587 * r + 0.114 * i) / 255 > 0.5 ? "#000" : "#fff";
}, bc = 6, na = 4, ve = 4, wc = "system-ui, -apple-system, 'Segoe UI', sans-serif", Zs = "#31333f", aa = (e) => {
  if (typeof e == "string") {
    const s = new K(e);
    if (!s.isUnrecognised) {
      const [o, n, a] = s.getSource();
      return {
        fillStyle: e,
        rgb: [
          o,
          n,
          a
        ]
      };
    }
  }
  const [t, r, i] = new K(Zs).getSource();
  return {
    fillStyle: Zs,
    rgb: [
      t,
      r,
      i
    ]
  };
}, Tc = (e, t) => {
  if (!t.label || t.chipSuppressed) return;
  const { rgb: r, fillStyle: i } = aa(t.stroke), s = oa(r), o = t.getLabelAnchorLocal(), n = t.scaleX || 1, a = t.scaleY || 1;
  e.save(), e.scale(1 / n, 1 / a);
  const l = o.x * n, h = o.y * a;
  e.font = `${t.fontSize}px ${wc}`;
  const c = e.measureText(t.label).width, u = ia(t.fontSize, na), d = c + 12, g = t.getBoundingRect().top, p = sa(g, u, ve) ? h + ve : h - ve - u;
  e.fillStyle = i, e.fillRect(l, p, d, u), e.fillStyle = s, e.textBaseline = "middle", e.textAlign = "left", e.fillText(t.label, l + bc, p + u / 2), e.restore();
}, Oc = (e) => {
  class t extends e {
    static customProperties = [
      ...e.customProperties ?? [],
      "label",
      "fontSize"
    ];
    chipSuppressed = !1;
    _render(i) {
      super._render(i), Tc(i, this);
    }
  }
  return t;
}, kc = (e) => {
  const t = e.getLabelAnchorLocal(), r = new v(t.x, t.y).transform(e.calcTransformMatrix()), i = ia(e.fontSize, na), s = e.getBoundingRect().top, o = sa(s, i, ve), { fillStyle: n, rgb: a } = aa(e.stroke);
  return {
    left: r.x,
    top: o ? r.y + ve : r.y - ve - i,
    fillStyle: n,
    textColor: oa(a)
  };
}, lr = class Hi extends Oc(rt) {
  static type = "LabeledRect";
  static ownDefaults = {
    label: "",
    fontSize: 20,
    lockRotation: !0,
    objectCaching: !1
  };
  static getDefaults() {
    return {
      ...super.getDefaults(),
      ...Hi.ownDefaults
    };
  }
  constructor(t = {}) {
    super(t), Object.assign(this, Hi.ownDefaults), this.setOptions(t), this.setControlVisible("mtr", !1);
  }
  getLabelAnchorLocal() {
    return {
      x: -this.width / 2,
      y: -this.height / 2
    };
  }
};
w.setClass(lr);
var Mc = 3, Dc = 10, Ec = 24, to = (e) => {
  if (!e || !(e instanceof Vt || e instanceof kt || e instanceof rt || e instanceof it)) return !1;
  const t = e;
  return !(Ht.some((r) => t[r]) || e instanceof it && e.scaleX !== e.scaleY);
}, Pc = (e) => {
  e instanceof Vt ? ra(e) : e instanceof kt ? xc(e) : e instanceof it ? _c(e) : e instanceof rt && Sc(e);
}, Ac = (e) => ({
  controls: e.controls,
  hasBorders: e.hasBorders,
  cornerStyle: e.cornerStyle,
  cornerColor: e.cornerColor,
  cornerStrokeColor: e.cornerStrokeColor,
  transparentCorners: e.transparentCorners,
  cornerSize: e.cornerSize,
  touchCornerSize: e.touchCornerSize
}), jc = class extends Lt {
  configureCanvas({ pointEdit: e, pointEditCornerColor: t, pointEditCornerStrokeColor: r, hiddenTextareaContainer: i }) {
    const s = this.canvas;
    s.isDrawingMode = !1, s.selection = !0, s.forEachObject((y) => y.selectable = y.evented = !0), e.get() && (s.selection = !1);
    let o = null;
    const n = (y) => {
      const S = kc(y);
      y.chipSuppressed = !0, y.dirty = !0;
      const C = new Mt(y.label, {
        left: S.left,
        top: S.top,
        originX: "left",
        originY: "top",
        fontSize: y.fontSize,
        fill: S.textColor,
        backgroundColor: S.fillStyle,
        hiddenTextareaContainer: i,
        excludeFromExport: !0
      });
      s.add(C), s.setActiveObject(C), C.enterEditing(), C.selectAll(), s.selection = !1, o = {
        rect: y,
        itext: C
      }, s.requestRenderAll();
    }, a = (y) => {
      if (!o || y.target !== o.itext) return;
      const { rect: S, itext: C } = o;
      S.label = C.text ?? "", s.remove(C), S.chipSuppressed = !1, S.dirty = !0, s.selection = !0, o = null, s.setActiveObject(S), s.requestRenderAll();
    };
    s.on("text:editing:exited", a);
    let l = null, h = null;
    const c = () => {
      h && (h.object.hoverCursor = h.original), h = null;
    }, u = () => {
      const y = s.getActiveObject();
      c(), !e.get() && y && (to(y) || y instanceof lr) && (h = {
        object: y,
        original: y.hoverCursor
      }, y.hoverCursor = "pointer");
    }, d = (y) => {
      e.set({
        object: y,
        saved: Ac(y)
      }), s.selection = !1, y.set({
        hasBorders: !1,
        cornerStyle: "circle",
        cornerColor: t,
        cornerStrokeColor: r,
        transparentCorners: !1,
        cornerSize: Dc,
        touchCornerSize: Ec
      }), Pc(y), y.setCoords(), s.requestRenderAll();
    }, g = (y) => {
      c(), d(y);
    }, p = () => {
      const y = e.get();
      y && (e.set(null), s.selection = !0, y.object.set({ ...y.saved }), y.object.setCoords(), s.requestRenderAll());
    }, m = (y) => {
      const S = y.target ?? null, C = s.getScenePoint(y.e);
      l = {
        target: S,
        alreadySelected: y.alreadySelected,
        x: C.x,
        y: C.y
      };
    }, x = (y) => {
      const S = l;
      if (l = null, !S) return;
      const C = y.target ?? null, b = e.get();
      if (!S.target) {
        b && p(), u();
        return;
      }
      if (C !== S.target) return;
      if (b) {
        b.object !== S.target && p(), u();
        return;
      }
      const O = s.getScenePoint(y.e);
      if (Math.hypot(O.x - S.x, O.y - S.y) < Mc && S.alreadySelected) {
        if (C instanceof lr) {
          n(C), u();
          return;
        }
        to(C) && g(C);
      }
      u();
    };
    s.on("mouse:down", m), s.on("mouse:up", x), s.on("selection:created", u), s.on("selection:updated", u);
    const _ = Cc(s, () => e.get()?.object ?? null, (y) => d(y));
    return () => {
      o && o.itext.exitEditing(), s.off("mouse:down", m), s.off("mouse:up", x), s.off("selection:created", u), s.off("selection:updated", u), s.off("text:editing:exited", a), _(), c(), p();
    };
  }
}, Fc = class extends Lt {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  currentCircle = new it();
  currentStartX = 0;
  currentStartY = 0;
  displayRadius = 1;
  configureCanvas({ strokeWidth: e, strokeColor: t, fillColor: r, displayRadius: i }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((l) => l.selectable = l.evented = !1), this.strokeWidth = e, this.strokeColor = t, this.fillColor = r, this.displayRadius = i;
    const s = (l) => this.onMouseDown(l), o = () => this.onMouseMove(), n = () => this.onMouseUp(), a = () => this.onMouseOut();
    return this.canvas.on("mouse:down", s), this.canvas.on("mouse:move", o), this.canvas.on("mouse:up", n), this.canvas.on("mouse:out", a), () => {
      this.canvas.off("mouse:down", s), this.canvas.off("mouse:move", o), this.canvas.off("mouse:up", n), this.canvas.off("mouse:out", a);
    };
  }
  onMouseDown(e) {
    const t = this.canvas, r = e.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(e.e);
    this.currentStartX = i.x - (this.displayRadius + this.strokeWidth / 2), this.currentStartY = i.y, this.currentCircle = new it({
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
    }), r === 0 && t.add(this.currentCircle);
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
}, Lc = class extends Lt {
  fillColor = "#000000";
  fontSize = 20;
  hiddenTextareaContainer = null;
  configureCanvas({ fillColor: e, fontSize: t, hiddenTextareaContainer: r }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((s) => s.selectable = s.evented = !1), this.fillColor = e, this.fontSize = t, this.hiddenTextareaContainer = r;
    const i = (s) => this.onMouseDown(s);
    return this.canvas.on("mouse:down", i), () => {
      this.canvas.off("mouse:down", i);
    };
  }
  onMouseDown(e) {
    if (e.e.button !== 0) return;
    const t = this.canvas, r = t.getScenePoint(e.e), i = new Mt("", {
      left: r.x,
      top: r.y,
      fill: this.fillColor,
      fontSize: this.fontSize,
      hiddenTextareaContainer: this.hiddenTextareaContainer
    });
    t.add(i), t.setActiveObject(i), i.enterEditing();
  }
}, Rc = class extends Lt {
  isMouseDown = !1;
  fillColor = "#ffffff";
  strokeWidth = 10;
  strokeColor = "#ffffff";
  label = "";
  fontSize = 20;
  currentRect = new lr();
  currentStartX = 0;
  currentStartY = 0;
  minLength = 10;
  configureCanvas({ strokeWidth: e, strokeColor: t, fillColor: r, label: i, fontSize: s }) {
    this.canvas.isDrawingMode = !1, this.canvas.selection = !1, this.canvas.forEachObject((h) => h.selectable = h.evented = !1), this.strokeWidth = e, this.strokeColor = t, this.fillColor = r, this.label = i, this.fontSize = s, this.minLength = e;
    const o = (h) => this.onMouseDown(h), n = (h) => this.onMouseMove(h), a = () => this.onMouseUp(), l = () => this.onMouseOut();
    return this.canvas.on("mouse:down", o), this.canvas.on("mouse:move", n), this.canvas.on("mouse:up", a), this.canvas.on("mouse:out", l), () => {
      this.canvas.off("mouse:down", o), this.canvas.off("mouse:move", n), this.canvas.off("mouse:up", a), this.canvas.off("mouse:out", l);
    };
  }
  onMouseDown(e) {
    const t = this.canvas, r = e.e.button;
    this.isMouseDown = !0;
    const i = t.getScenePoint(e.e);
    this.currentStartX = i.x, this.currentStartY = i.y, this.currentRect = new lr({
      left: this.currentStartX,
      top: this.currentStartY,
      originX: "left",
      originY: "top",
      width: this.minLength,
      height: this.minLength,
      stroke: this.strokeColor,
      strokeWidth: this.strokeWidth,
      fill: this.fillColor,
      label: this.label,
      fontSize: this.fontSize,
      transparentCorners: !1,
      selectable: !1,
      evented: !1,
      strokeUniform: !0,
      noScaleCache: !1,
      angle: 0
    }), r === 0 && t.add(this.currentRect);
  }
  onMouseMove(e) {
    if (!this.isMouseDown) return;
    const t = this.canvas, r = t.getScenePoint(e.e);
    this.currentStartX > r.x && this.currentRect.set({ left: Math.abs(r.x) }), this.currentStartY > r.y && this.currentRect.set({ top: Math.abs(r.y) });
    const i = Math.abs(this.currentStartX - r.x), s = Math.abs(this.currentStartY - r.y);
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
}, gi = {
  circle: ec,
  freedraw: rc,
  line: ic,
  polygon: ac,
  rect: lc,
  edit: jc,
  point: Fc,
  text: Lc,
  labeled_rect: Rc
}, Bc = 200, Ar = (e) => {
  const t = e.canvas.toObject(Ht);
  return e.history.save(t) && e.latest.realtimeUpdateStreamlit && e.sender.schedule(t), t;
}, Ic = (e, t) => {
  const r = e.latest.returnImageData ? e.canvas.toDataURL({
    format: "png",
    multiplier: 1
  }) : null;
  e.latest.setStateValue("drawing", {
    raw: t,
    data: r
  });
}, la = (e, t) => {
  e.forEachObject((r) => {
    r instanceof Mt && (r.hiddenTextareaContainer = t);
  });
}, fi = async (e) => {
  const t = e.history.current;
  if (t == null) return !1;
  const r = ++e.loadGeneration;
  return await e.canvas.loadFromJSON(t), r !== e.loadGeneration ? !1 : (la(e.canvas, e.textareaHostEl), ea(e.canvas), e.canvas.renderAll(), e.pointEdit = null, e.latest.data && Yr(e, e.latest.data), !0);
}, Xc = (e) => {
  e.isDrawingMode = !1, e.selection = !1, e.discardActiveObject(), e.forEachObject((t) => {
    t.selectable = !1, t.evented = !1;
  }), e.renderAll();
}, Yc = (e, t) => e === t ? !0 : e === null || t === null ? !1 : e.naturalWidth === t.naturalWidth && e.naturalHeight === t.naturalHeight && e.scaleX === t.scaleX && e.scaleY === t.scaleY && e.offsetX === t.offsetX && e.offsetY === t.offsetY, eo = (e, t) => {
  Yc(t, e.lastBackgroundFit) || (e.lastBackgroundFit = t, e.latest.setStateValue("backgroundFit", t));
}, ro = (e, t, r) => getComputedStyle(e).getPropertyValue(t).trim() || r, Yr = (e, t) => {
  if (e.activeToolCleanup?.(), e.activeToolCleanup = null, t.disabled) {
    Xc(e.canvas);
    return;
  }
  e.activeToolCleanup = new (e.editActive ? gi.edit : gi[t.drawingMode] ?? gi.freedraw)(e.canvas).configureCanvas({
    fillColor: t.fillColor,
    strokeWidth: t.strokeWidth,
    strokeColor: t.strokeColor,
    displayRadius: t.displayRadius,
    fontSize: t.fontSize,
    label: t.label,
    hiddenTextareaContainer: e.textareaHostEl,
    onPolygonClosed: () => {
      e.polygonJustClosed = !0;
    },
    pointEdit: {
      get: () => e.pointEdit,
      set: (r) => {
        e.pointEdit = r;
      }
    },
    pointEditCornerColor: ro(e.container, "--st-text-color", "#31333f"),
    pointEditCornerStrokeColor: ro(e.container, "--st-background-color", "#fff")
  });
}, ha = (e, t) => {
  e.toolbarEl.dataset.pinned = String(!t || e.editActive);
}, at = (e) => {
  Zh(e.toolbarHandles, e.history.canUndo(), e.history.canRedo(), e.editActive, e.canvas.getActiveObject() != null);
}, pi = (e) => {
  const t = Ar(e);
  e.latest.realtimeUpdateStreamlit && e.sender.now(t), at(e);
}, $c = (e) => !e.disabled, zi = (e, t) => JSON.stringify([
  e.drawingMode,
  t,
  e.fillColor,
  e.strokeWidth,
  e.strokeColor,
  e.displayRadius,
  e.disabled,
  e.fontSize,
  e.label
]), Wc = (e) => {
  const t = document.createElement("div");
  t.className = "dc-root";
  const r = document.createElement("div");
  r.className = "dc-scroll";
  const i = document.createElement("div");
  i.className = "dc-container";
  const s = document.createElement("canvas");
  s.className = "dc-background-canvas";
  const o = document.createElement("canvas");
  o.className = "dc-canvas";
  const n = document.createElement("div");
  n.className = "dc-toolbar";
  const a = document.createElement("div");
  a.className = "dc-textarea-host", i.append(s, o), r.appendChild(i), t.append(r, n, a), e.appendChild(t);
  const l = new Ai(o, { enableRetinaScaling: !1 });
  l.stopContextMenu = !1;
  const h = {
    container: t,
    scrollEl: r,
    canvasBox: i,
    textareaHostEl: a,
    canvas: l,
    backgroundCanvas: new Gr(s, { enableRetinaScaling: !1 }),
    toolbarEl: n,
    toolbarHandles: null,
    history: new Kh(),
    sender: null,
    activeToolCleanup: null,
    lastToolKey: null,
    lastInitialDrawingKey: null,
    lastBackgroundImageURL: null,
    lastBackgroundImageFit: null,
    lastBackgroundFit: null,
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
    },
    isTextEditing: !1,
    polygonJustClosed: !1,
    pointEdit: null,
    editActive: !1,
    lastDrawingMode: null
  };
  return h.sender = Nh((c) => Ic(h, c), Bc), h.toolbarHandles = Qh(n, {
    onSend: () => {
      h.sender.now(l.toObject(Ht));
    },
    onEditToggle: () => {
      h.isTextEditing && l.discardActiveObject(), h.editActive = !h.editActive;
      const c = h.latest.data;
      c && (Yr(h, c), h.lastToolKey = zi(c, h.editActive)), ha(h, h.latest.realtimeUpdateStreamlit), at(h);
    },
    onUndo: () => {
      h.history.undo() && (fi(h).then((c) => {
        c && h.latest.realtimeUpdateStreamlit && h.sender.now(l.toObject(Ht));
      }), at(h));
    },
    onRedo: () => {
      h.history.redo() && (fi(h).then((c) => {
        c && h.latest.realtimeUpdateStreamlit && h.sender.now(l.toObject(Ht));
      }), at(h));
    },
    onBringForward: () => {
      const c = l.getActiveObject();
      c && (l.bringObjectForward(c), l.renderAll(), pi(h));
    },
    onSendBackward: () => {
      const c = l.getActiveObject();
      c && (l.sendObjectBackwards(c), l.renderAll(), pi(h));
    },
    onDeleteSelected: () => {
      const c = l.getActiveObject();
      c && (l.discardActiveObject(), l.remove(c), l.renderAll(), pi(h));
    },
    onReset: () => {
      const c = h.history.initial ?? {};
      h.history.reset(c), fi(h).then((u) => {
        u && h.sender.now(l.toObject(Ht));
      }), at(h);
    }
  }), l.on("mouse:up", () => {
    if (h.latest.data?.disabled || h.isTextEditing) return;
    const c = h.polygonJustClosed;
    h.polygonJustClosed = !1, queueMicrotask(() => {
      const u = Ar(h);
      c && h.sender.now(u), at(h);
    });
  }), l.on("mouse:dblclick", () => {
    h.latest.data?.disabled || h.isTextEditing || queueMicrotask(() => {
      Ar(h), at(h);
    });
  }), l.on("text:editing:entered", () => {
    h.isTextEditing = !0;
  }), l.on("text:editing:exited", () => {
    h.isTextEditing = !1, queueMicrotask(() => {
      Ar(h), at(h);
    });
  }), l.on("selection:created", () => at(h)), l.on("selection:updated", () => at(h)), l.on("selection:cleared", () => at(h)), h;
}, Vc = (e, t, r) => {
  e.latest.realtimeUpdateStreamlit = t.realtimeUpdateStreamlit, e.latest.returnImageData = t.returnImageData, e.latest.setStateValue = r, e.latest.data = t, t.drawingMode !== e.lastDrawingMode && (e.editActive = !1), e.lastDrawingMode = t.drawingMode;
  const i = e.width !== t.canvasWidth || e.height !== t.canvasHeight;
  i && (e.width = t.canvasWidth, e.height = t.canvasHeight, e.canvas.setDimensions({
    width: t.canvasWidth,
    height: t.canvasHeight
  }), e.backgroundCanvas.setDimensions({
    width: t.canvasWidth,
    height: t.canvasHeight
  })), e.canvasBox.style.width = `${t.canvasWidth}px`, e.canvasBox.style.height = `${t.canvasHeight}px`, t.maxDisplayHeight != null ? (e.scrollEl.style.maxHeight = `${t.maxDisplayHeight}px`, e.scrollEl.style.overflowY = "auto") : (e.scrollEl.style.maxHeight = "", e.scrollEl.style.overflowY = "hidden"), e.toolbarEl.style.display = $c(t) ? "flex" : "none", ha(e, t.realtimeUpdateStreamlit);
  const s = t.backgroundImageFit !== e.lastBackgroundImageFit;
  if (e.lastBackgroundImageFit = t.backgroundImageFit, t.backgroundImageURL !== e.lastBackgroundImageURL) {
    e.lastBackgroundImageURL = t.backgroundImageURL;
    const a = ++e.backgroundGeneration;
    zh(e.backgroundCanvas, t.backgroundImageURL, () => a === e.backgroundGeneration, t.backgroundImageFit).then((l) => {
      a === e.backgroundGeneration && eo(e, l);
    }).catch((l) => {
      console.error("streamlit-drawable-canvas: failed to load background image", l), a === e.backgroundGeneration && (e.lastBackgroundImageURL = null);
    });
  } else (i || s) && eo(e, Gh(e.backgroundCanvas, t.backgroundImageFit));
  const o = JSON.stringify(t.initialDrawing), n = e.lastInitialDrawingKey === null;
  if (o !== e.lastInitialDrawingKey) {
    e.lastInitialDrawingKey = o, e.sender.cancel();
    const a = ++e.loadGeneration;
    e.canvas.loadFromJSON(t.initialDrawing).then(() => {
      if (a !== e.loadGeneration) return;
      la(e.canvas, e.textareaHostEl);
      const l = ea(e.canvas);
      e.canvas.renderAll();
      const h = e.canvas.toObject(Ht);
      e.history.reset(h), e.pointEdit = null;
      const c = e.latest.data ?? t;
      Yr(e, c), e.lastToolKey = zi(c, e.editActive), at(e), (!n && e.latest.realtimeUpdateStreamlit || l) && e.sender.now(h);
    });
  } else {
    const a = zi(t, e.editActive);
    a !== e.lastToolKey && (e.lastToolKey = a, Yr(e, t));
  }
  at(e);
}, Hc = (e) => {
  e.sender.cancel(), e.activeToolCleanup?.(), e.canvas.dispose(), e.backgroundCanvas.dispose(), e.container.remove();
}, Tr = /* @__PURE__ */ new WeakMap(), Kc = (e) => {
  const { data: t, parentElement: r, setStateValue: i } = e, s = r.querySelector(".canvas-root");
  if (!s) throw new Error("Unexpected: .canvas-root element not found");
  let o = Tr.get(r);
  return o ? s.contains(o.container) || s.appendChild(o.container) : (o = Wc(s), Tr.set(r, o)), Vc(o, t, i), () => {
    const n = Tr.get(r);
    n && (Hc(n), Tr.delete(r));
  };
};
export {
  Kc as default
};
