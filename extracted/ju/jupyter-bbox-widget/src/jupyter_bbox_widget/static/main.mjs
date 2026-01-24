var Lt = Object.defineProperty;
var Wt = (e, t, n) => t in e ? Lt(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var tt = (e, t, n) => Wt(e, typeof t != "symbol" ? t + "" : t, n);
function $() {
}
const At = (e) => e;
function Bt(e) {
  return e();
}
function ht() {
  return /* @__PURE__ */ Object.create(null);
}
function ne(e) {
  e.forEach(Bt);
}
function rt(e) {
  return typeof e == "function";
}
function et(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
let Fe;
function dt(e, t) {
  return e === t ? !0 : (Fe || (Fe = document.createElement("a")), Fe.href = t, e === Fe.href);
}
function Ut(e) {
  return Object.keys(e).length === 0;
}
function jt(e, ...t) {
  if (e == null) {
    for (const l of t)
      l(void 0);
    return $;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function fe(e, t, n) {
  e.$$.on_destroy.push(jt(t, n));
}
function gt(e) {
  return e ?? "";
}
function I(e, t, n) {
  return e.set(n), t;
}
const zt = typeof window < "u";
let It = zt ? () => window.performance.now() : () => Date.now(), at = zt ? (e) => requestAnimationFrame(e) : $;
const ze = /* @__PURE__ */ new Set();
function Dt(e) {
  ze.forEach((t) => {
    t.c(e) || (ze.delete(t), t.f());
  }), ze.size !== 0 && at(Dt);
}
function Ft(e) {
  let t;
  return ze.size === 0 && at(Dt), {
    promise: new Promise((n) => {
      ze.add(t = { c: e, f: n });
    }),
    abort() {
      ze.delete(t);
    }
  };
}
const Vt = typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : (
  // @ts-ignore Node typings have this
  global
);
function P(e, t) {
  e.appendChild(t);
}
function Rt(e) {
  if (!e) return document;
  const t = e.getRootNode ? e.getRootNode() : e.ownerDocument;
  return t && /** @type {ShadowRoot} */
  t.host ? (
    /** @type {ShadowRoot} */
    t
  ) : e.ownerDocument;
}
function Tt(e) {
  const t = ee("style");
  return t.textContent = "/* empty */", Ht(Rt(e), t), t.sheet;
}
function Ht(e, t) {
  return P(
    /** @type {Document} */
    e.head || e,
    t
  ), t.sheet;
}
function B(e, t, n) {
  e.insertBefore(t, n || null);
}
function A(e) {
  e.parentNode && e.parentNode.removeChild(e);
}
function Gt(e, t) {
  for (let n = 0; n < e.length; n += 1)
    e[n] && e[n].d(t);
}
function ee(e) {
  return document.createElement(e);
}
function U(e) {
  return document.createElementNS("http://www.w3.org/2000/svg", e);
}
function Re(e) {
  return document.createTextNode(e);
}
function L() {
  return Re(" ");
}
function Qt() {
  return Re("");
}
function X(e, t, n, l) {
  return e.addEventListener(t, n, l), () => e.removeEventListener(t, n, l);
}
function o(e, t, n) {
  n == null ? e.removeAttribute(t) : e.getAttribute(t) !== n && e.setAttribute(t, n);
}
function Jt(e) {
  return Array.from(e.childNodes);
}
function Ge(e, t) {
  t = "" + t, e.data !== t && (e.data = /** @type {string} */
  t);
}
function R(e, t, n, l) {
  n == null ? e.style.removeProperty(t) : e.style.setProperty(t, n, "");
}
let Ve;
function Zt() {
  if (Ve === void 0) {
    Ve = !1;
    try {
      typeof window < "u" && window.parent && window.parent.document;
    } catch {
      Ve = !0;
    }
  }
  return Ve;
}
function $t(e, t) {
  getComputedStyle(e).position === "static" && (e.style.position = "relative");
  const l = ee("iframe");
  l.setAttribute(
    "style",
    "display: block; position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; border: 0; opacity: 0; pointer-events: none; z-index: -1;"
  ), l.setAttribute("aria-hidden", "true"), l.tabIndex = -1;
  const c = Zt();
  let s;
  return c ? (l.src = "data:text/html,<script>onresize=function(){parent.postMessage(0,'*')}<\/script>", s = X(
    window,
    "message",
    /** @param {MessageEvent} event */
    (i) => {
      i.source === l.contentWindow && t();
    }
  )) : (l.src = "about:blank", l.onload = () => {
    s = X(l.contentWindow, "resize", t), t();
  }), P(e, l), () => {
    (c || s && l.contentWindow) && s(), A(l);
  };
}
function Te(e, t, n) {
  e.classList.toggle(t, !!n);
}
function Kt(e, t, { bubbles: n = !1, cancelable: l = !1 } = {}) {
  return new CustomEvent(e, { detail: t, bubbles: n, cancelable: l });
}
const Qe = /* @__PURE__ */ new Map();
let Je = 0;
function xt(e) {
  let t = 5381, n = e.length;
  for (; n--; ) t = (t << 5) - t ^ e.charCodeAt(n);
  return t >>> 0;
}
function en(e, t) {
  const n = { stylesheet: Tt(t), rules: {} };
  return Qe.set(e, n), n;
}
function mt(e, t, n, l, c, s, i, u = 0) {
  const a = 16.666 / l;
  let g = `{
`;
  for (let v = 0; v <= 1; v += a) {
    const C = t + (n - t) * s(v);
    g += v * 100 + `%{${i(C, 1 - C)}}
`;
  }
  const E = g + `100% {${i(n, 1 - n)}}
}`, w = `__svelte_${xt(E)}_${u}`, M = Rt(e), { stylesheet: m, rules: d } = Qe.get(M) || en(M, e);
  d[w] || (d[w] = !0, m.insertRule(`@keyframes ${w} ${E}`, m.cssRules.length));
  const q = e.style.animation || "";
  return e.style.animation = `${q ? `${q}, ` : ""}${w} ${l}ms linear ${c}ms 1 both`, Je += 1, w;
}
function tn(e, t) {
  const n = (e.style.animation || "").split(", "), l = n.filter(
    t ? (s) => s.indexOf(t) < 0 : (s) => s.indexOf("__svelte") === -1
    // remove all Svelte animations
  ), c = n.length - l.length;
  c && (e.style.animation = l.join(", "), Je -= c, Je || nn());
}
function nn() {
  at(() => {
    Je || (Qe.forEach((e) => {
      const { ownerNode: t } = e.stylesheet;
      t && A(t);
    }), Qe.clear());
  });
}
let We;
function Le(e) {
  We = e;
}
function Pt() {
  if (!We) throw new Error("Function called outside component initialization");
  return We;
}
function ln(e) {
  Pt().$$.on_mount.push(e);
}
function on() {
  const e = Pt();
  return (t, n, { cancelable: l = !1 } = {}) => {
    const c = e.$$.callbacks[t];
    if (c) {
      const s = Kt(
        /** @type {string} */
        t,
        n,
        { cancelable: l }
      );
      return c.slice().forEach((i) => {
        i.call(e, s);
      }), !s.defaultPrevented;
    }
    return !0;
  };
}
function sn(e, t) {
  const n = e.$$.callbacks[t.type];
  n && n.slice().forEach((l) => l.call(this, t));
}
const Be = [], re = [];
let De = [];
const it = [], fn = /* @__PURE__ */ Promise.resolve();
let ot = !1;
function un() {
  ot || (ot = !0, fn.then(Nt));
}
function Ke(e) {
  De.push(e);
}
function Oe(e) {
  it.push(e);
}
const nt = /* @__PURE__ */ new Set();
let Se = 0;
function Nt() {
  if (Se !== 0)
    return;
  const e = We;
  do {
    try {
      for (; Se < Be.length; ) {
        const t = Be[Se];
        Se++, Le(t), rn(t.$$);
      }
    } catch (t) {
      throw Be.length = 0, Se = 0, t;
    }
    for (Le(null), Be.length = 0, Se = 0; re.length; ) re.pop()();
    for (let t = 0; t < De.length; t += 1) {
      const n = De[t];
      nt.has(n) || (nt.add(n), n());
    }
    De.length = 0;
  } while (Be.length);
  for (; it.length; )
    it.pop()();
  ot = !1, nt.clear(), Le(e);
}
function rn(e) {
  if (e.fragment !== null) {
    e.update(), ne(e.before_update);
    const t = e.dirty;
    e.dirty = [-1], e.fragment && e.fragment.p(e.ctx, t), e.after_update.forEach(Ke);
  }
}
function an(e) {
  const t = [], n = [];
  De.forEach((l) => e.indexOf(l) === -1 ? t.push(l) : n.push(l)), n.forEach((l) => l()), De = t;
}
let Xe;
function _n() {
  return Xe || (Xe = Promise.resolve(), Xe.then(() => {
    Xe = null;
  })), Xe;
}
function lt(e, t, n) {
  e.dispatchEvent(Kt(`${t ? "intro" : "outro"}${n}`));
}
const He = /* @__PURE__ */ new Set();
let ae;
function st() {
  ae = {
    r: 0,
    c: [],
    p: ae
    // parent group
  };
}
function ft() {
  ae.r || ne(ae.c), ae = ae.p;
}
function te(e, t) {
  e && e.i && (He.delete(e), e.i(t));
}
function _e(e, t, n, l) {
  if (e && e.o) {
    if (He.has(e)) return;
    He.add(e), ae.c.push(() => {
      He.delete(e), l && (n && e.d(1), l());
    }), e.o(t);
  } else l && l();
}
const cn = { duration: 0 };
function bt(e, t, n, l) {
  let s = t(e, n, { direction: "both" }), i = l ? 0 : 1, u = null, a = null, g = null, E;
  function w() {
    g && tn(e, g);
  }
  function M(d, q) {
    const v = (
      /** @type {Program['d']} */
      d.b - i
    );
    return q *= Math.abs(v), {
      a: i,
      b: d.b,
      d: v,
      duration: q,
      start: d.start,
      end: d.start + q,
      group: d.group
    };
  }
  function m(d) {
    const {
      delay: q = 0,
      duration: v = 300,
      easing: C = At,
      tick: D = $,
      css: y
    } = s || cn, _ = {
      start: It() + q,
      b: d
    };
    d || (_.group = ae, ae.r += 1), "inert" in e && (d ? E !== void 0 && (e.inert = E) : (E = /** @type {HTMLElement} */
    e.inert, e.inert = !0)), u || a ? a = _ : (y && (w(), g = mt(e, i, d, v, q, C, y)), d && D(0, 1), u = M(_, v), Ke(() => lt(e, d, "start")), Ft((h) => {
      if (a && h > a.start && (u = M(a, v), a = null, lt(e, u.b, "start"), y && (w(), g = mt(
        e,
        i,
        u.b,
        u.duration,
        0,
        C,
        s.css
      ))), u) {
        if (h >= u.end)
          D(i = u.b, 1 - i), lt(e, u.b, "end"), a || (u.b ? w() : --u.group.r || ne(u.group.c)), u = null;
        else if (h >= u.start) {
          const b = h - u.start;
          i = u.a + u.d * C(b / u.duration), D(i, 1 - i);
        }
      }
      return !!(u || a);
    }));
  }
  return {
    run(d) {
      rt(s) ? _n().then(() => {
        s = s({ direction: d ? "in" : "out" }), m(d);
      }) : m(d);
    },
    end() {
      w(), u = a = null;
    }
  };
}
function Ze(e) {
  return (e == null ? void 0 : e.length) !== void 0 ? e : Array.from(e);
}
function hn(e, t) {
  _e(e, 1, 1, () => {
    t.delete(e.key);
  });
}
function dn(e, t, n, l, c, s, i, u, a, g, E, w) {
  let M = e.length, m = s.length, d = M;
  const q = {};
  for (; d--; ) q[e[d].key] = d;
  const v = [], C = /* @__PURE__ */ new Map(), D = /* @__PURE__ */ new Map(), y = [];
  for (d = m; d--; ) {
    const z = w(c, s, d), N = n(z);
    let K = i.get(N);
    K ? y.push(() => K.p(z, t)) : (K = g(N, z), K.c()), C.set(N, v[d] = K), N in q && D.set(N, Math.abs(d - q[N]));
  }
  const _ = /* @__PURE__ */ new Set(), h = /* @__PURE__ */ new Set();
  function b(z) {
    te(z, 1), z.m(u, E), i.set(z.key, z), E = z.first, m--;
  }
  for (; M && m; ) {
    const z = v[m - 1], N = e[M - 1], K = z.key, O = N.key;
    z === N ? (E = z.first, M--, m--) : C.has(O) ? !i.has(K) || _.has(K) ? b(z) : h.has(O) ? M-- : D.get(K) > D.get(O) ? (h.add(K), b(z)) : (_.add(O), M--) : (a(N, i), M--);
  }
  for (; M--; ) {
    const z = e[M];
    C.has(z.key) || a(z, i);
  }
  for (; m; ) b(v[m - 1]);
  return ne(y), v;
}
function Ye(e, t, n) {
  const l = e.$$.props[t];
  l !== void 0 && (e.$$.bound[l] = n, n(e.$$.ctx[l]));
}
function ut(e) {
  e && e.c();
}
function $e(e, t, n) {
  const { fragment: l, after_update: c } = e.$$;
  l && l.m(t, n), Ke(() => {
    const s = e.$$.on_mount.map(Bt).filter(rt);
    e.$$.on_destroy ? e.$$.on_destroy.push(...s) : ne(s), e.$$.on_mount = [];
  }), c.forEach(Ke);
}
function xe(e, t) {
  const n = e.$$;
  n.fragment !== null && (an(n.after_update), ne(n.on_destroy), n.fragment && n.fragment.d(t), n.on_destroy = n.fragment = null, n.ctx = []);
}
function gn(e, t) {
  e.$$.dirty[0] === -1 && (Be.push(e), un(), e.$$.dirty.fill(0)), e.$$.dirty[t / 31 | 0] |= 1 << t % 31;
}
function _t(e, t, n, l, c, s, i = null, u = [-1]) {
  const a = We;
  Le(e);
  const g = e.$$ = {
    fragment: null,
    ctx: [],
    // state
    props: s,
    update: $,
    not_equal: c,
    bound: ht(),
    // lifecycle
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(t.context || (a ? a.$$.context : [])),
    // everything else
    callbacks: ht(),
    dirty: u,
    skip_bound: !1,
    root: t.target || a.$$.root
  };
  i && i(g.root);
  let E = !1;
  if (g.ctx = n ? n(e, t.props || {}, (w, M, ...m) => {
    const d = m.length ? m[0] : M;
    return g.ctx && c(g.ctx[w], g.ctx[w] = d) && (!g.skip_bound && g.bound[w] && g.bound[w](d), E && gn(e, w)), M;
  }) : [], g.update(), E = !0, ne(g.before_update), g.fragment = l ? l(g.ctx) : !1, t.target) {
    if (t.hydrate) {
      const w = Jt(t.target);
      g.fragment && g.fragment.l(w), w.forEach(A);
    } else
      g.fragment && g.fragment.c();
    t.intro && te(e.$$.fragment), $e(e, t.target, t.anchor), Nt();
  }
  Le(a);
}
class ct {
  constructor() {
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    tt(this, "$$");
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    tt(this, "$$set");
  }
  /** @returns {void} */
  $destroy() {
    xe(this, 1), this.$destroy = $;
  }
  /**
   * @template {Extract<keyof Events, string>} K
   * @param {K} type
   * @param {((e: Events[K]) => void) | null | undefined} callback
   * @returns {() => void}
   */
  $on(t, n) {
    if (!rt(n))
      return $;
    const l = this.$$.callbacks[t] || (this.$$.callbacks[t] = []);
    return l.push(n), () => {
      const c = l.indexOf(n);
      c !== -1 && l.splice(c, 1);
    };
  }
  /**
   * @param {Partial<Props>} props
   * @returns {void}
   */
  $set(t) {
    this.$$set && !Ut(t) && (this.$$.skip_bound = !0, this.$$set(t), this.$$.skip_bound = !1);
  }
}
const mn = "4";
typeof window < "u" && (window.__svelte || (window.__svelte = { v: /* @__PURE__ */ new Set() })).v.add(mn);
function wt(e) {
  let t, n, l, c, s, i, u, a, g, E, w, M, m, d, q, v, C, D, y, _, h, b, z, N, K, O, x, ce, j, ie, V, F, T, oe, se, ge, Q, p, H, Z, Y, we, he, me, be, pe, G, ye, ke, ve, Me, Pe, J, Ee, Ce, Ne, Ue;
  return {
    c() {
      t = U("line"), i = L(), u = U("line"), M = L(), m = U("line"), D = L(), y = U("line"), N = L(), K = U("circle"), ce = L(), j = U("circle"), F = L(), T = U("circle"), ge = L(), Q = U("circle"), Z = L(), Y = U("line"), pe = L(), G = U("line"), Pe = L(), J = U("rect"), o(t, "x1", n = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(t, "y1", l = /*y*/
      e[3] * /*scaleY*/
      e[7]), o(t, "x2", c = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(t, "y2", s = /*y*/
      e[3] * /*scaleY*/
      e[7]), R(t, "stroke-width", "10px"), R(t, "stroke", "black"), R(t, "stroke-opacity", "0"), o(t, "class", "top svelte-qvidok"), o(u, "x1", a = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(u, "y1", g = /*y*/
      (e[3] + /*height*/
      e[1]) * /*scaleY*/
      e[7]), o(u, "x2", E = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(u, "y2", w = /*y*/
      (e[3] + /*height*/
      e[1]) * /*scaleY*/
      e[7]), R(u, "stroke-width", "10px"), R(u, "stroke", "black"), R(u, "stroke-opacity", "0"), o(u, "class", "bottom svelte-qvidok"), o(m, "x1", d = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(m, "y1", q = /*y*/
      e[3] * /*scaleY*/
      e[7]), o(m, "x2", v = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(m, "y2", C = /*y*/
      (e[3] + /*height*/
      e[1]) * /*scaleY*/
      e[7]), R(m, "stroke-width", "10px"), R(m, "stroke", "black"), R(m, "stroke-opacity", "0"), o(m, "class", "left svelte-qvidok"), o(y, "x1", _ = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(y, "y1", h = /*y*/
      e[3] * /*scaleY*/
      e[7]), o(y, "x2", b = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(y, "y2", z = /*y*/
      (e[3] + /*height*/
      e[1]) * /*scaleY*/
      e[7]), R(y, "stroke-width", "10px"), R(y, "stroke", "black"), R(y, "stroke-opacity", "0"), o(y, "class", "right svelte-qvidok"), o(K, "cx", O = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(K, "cy", x = /*y*/
      e[3] * /*scaleY*/
      e[7]), o(K, "r", 6), o(K, "fill-opacity", "0"), o(K, "class", "top-left svelte-qvidok"), o(j, "cx", ie = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(j, "cy", V = /*y*/
      e[3] * /*scaleY*/
      e[7]), o(j, "r", 6), o(j, "fill-opacity", "0"), o(j, "class", "top-right svelte-qvidok"), o(T, "cx", oe = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(T, "cy", se = /*y*/
      (e[3] + /*height*/
      e[1]) * /*scaleY*/
      e[7]), o(T, "r", 6), o(T, "fill-opacity", "0"), o(T, "class", "bottom-left svelte-qvidok"), o(Q, "cx", p = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(Q, "cy", H = /*y*/
      (e[3] + /*height*/
      e[1]) * /*scaleY*/
      e[7]), o(Q, "r", 6), o(Q, "fill-opacity", "0"), o(Q, "class", "bottom-right svelte-qvidok"), o(Y, "x1", we = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6] - 10), o(Y, "x2", he = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(Y, "y1", me = /*y*/
      e[3] * /*scaleY*/
      e[7] - 13), o(Y, "y2", be = /*y*/
      e[3] * /*scaleY*/
      e[7] - 3), R(Y, "stroke-width", "2"), R(
        Y,
        "stroke",
        /*color*/
        e[10]
      ), o(G, "x1", ye = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6] - 10), o(G, "x2", ke = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6]), o(G, "y1", ve = /*y*/
      e[3] * /*scaleY*/
      e[7] - 3), o(G, "y2", Me = /*y*/
      e[3] * /*scaleY*/
      e[7] - 13), R(G, "stroke-width", "2"), R(
        G,
        "stroke",
        /*color*/
        e[10]
      ), o(J, "width", "12"), o(J, "height", "12"), o(J, "class", "clickable svelte-qvidok"), R(J, "stroke-width", "0"), R(J, "fill-opacity", "0"), o(J, "x", Ee = /*x*/
      (e[2] + /*width*/
      e[0]) * /*scaleX*/
      e[6] - 11), o(J, "y", Ce = /*y*/
      e[3] * /*scaleY*/
      e[7] - 14);
    },
    m(f, k) {
      B(f, t, k), B(f, i, k), B(f, u, k), B(f, M, k), B(f, m, k), B(f, D, k), B(f, y, k), B(f, N, k), B(f, K, k), B(f, ce, k), B(f, j, k), B(f, F, k), B(f, T, k), B(f, ge, k), B(f, Q, k), B(f, Z, k), B(f, Y, k), B(f, pe, k), B(f, G, k), B(f, Pe, k), B(f, J, k), Ne || (Ue = [
        X(
          t,
          "mousedown",
          /*mousedown_handler*/
          e[18]
        ),
        X(
          u,
          "mousedown",
          /*mousedown_handler_1*/
          e[19]
        ),
        X(
          m,
          "mousedown",
          /*mousedown_handler_2*/
          e[20]
        ),
        X(
          y,
          "mousedown",
          /*mousedown_handler_3*/
          e[21]
        ),
        X(
          K,
          "mousedown",
          /*mousedown_handler_4*/
          e[22]
        ),
        X(
          j,
          "mousedown",
          /*mousedown_handler_5*/
          e[23]
        ),
        X(
          T,
          "mousedown",
          /*mousedown_handler_6*/
          e[24]
        ),
        X(
          Q,
          "mousedown",
          /*mousedown_handler_7*/
          e[25]
        ),
        X(
          J,
          "mousedown",
          /*remove*/
          e[13]
        )
      ], Ne = !0);
    },
    p(f, k) {
      k[0] & /*x, scaleX*/
      68 && n !== (n = /*x*/
      f[2] * /*scaleX*/
      f[6]) && o(t, "x1", n), k[0] & /*y, scaleY*/
      136 && l !== (l = /*y*/
      f[3] * /*scaleY*/
      f[7]) && o(t, "y1", l), k[0] & /*x, width, scaleX*/
      69 && c !== (c = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(t, "x2", c), k[0] & /*y, scaleY*/
      136 && s !== (s = /*y*/
      f[3] * /*scaleY*/
      f[7]) && o(t, "y2", s), k[0] & /*x, scaleX*/
      68 && a !== (a = /*x*/
      f[2] * /*scaleX*/
      f[6]) && o(u, "x1", a), k[0] & /*y, height, scaleY*/
      138 && g !== (g = /*y*/
      (f[3] + /*height*/
      f[1]) * /*scaleY*/
      f[7]) && o(u, "y1", g), k[0] & /*x, width, scaleX*/
      69 && E !== (E = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(u, "x2", E), k[0] & /*y, height, scaleY*/
      138 && w !== (w = /*y*/
      (f[3] + /*height*/
      f[1]) * /*scaleY*/
      f[7]) && o(u, "y2", w), k[0] & /*x, scaleX*/
      68 && d !== (d = /*x*/
      f[2] * /*scaleX*/
      f[6]) && o(m, "x1", d), k[0] & /*y, scaleY*/
      136 && q !== (q = /*y*/
      f[3] * /*scaleY*/
      f[7]) && o(m, "y1", q), k[0] & /*x, scaleX*/
      68 && v !== (v = /*x*/
      f[2] * /*scaleX*/
      f[6]) && o(m, "x2", v), k[0] & /*y, height, scaleY*/
      138 && C !== (C = /*y*/
      (f[3] + /*height*/
      f[1]) * /*scaleY*/
      f[7]) && o(m, "y2", C), k[0] & /*x, width, scaleX*/
      69 && _ !== (_ = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(y, "x1", _), k[0] & /*y, scaleY*/
      136 && h !== (h = /*y*/
      f[3] * /*scaleY*/
      f[7]) && o(y, "y1", h), k[0] & /*x, width, scaleX*/
      69 && b !== (b = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(y, "x2", b), k[0] & /*y, height, scaleY*/
      138 && z !== (z = /*y*/
      (f[3] + /*height*/
      f[1]) * /*scaleY*/
      f[7]) && o(y, "y2", z), k[0] & /*x, scaleX*/
      68 && O !== (O = /*x*/
      f[2] * /*scaleX*/
      f[6]) && o(K, "cx", O), k[0] & /*y, scaleY*/
      136 && x !== (x = /*y*/
      f[3] * /*scaleY*/
      f[7]) && o(K, "cy", x), k[0] & /*x, width, scaleX*/
      69 && ie !== (ie = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(j, "cx", ie), k[0] & /*y, scaleY*/
      136 && V !== (V = /*y*/
      f[3] * /*scaleY*/
      f[7]) && o(j, "cy", V), k[0] & /*x, scaleX*/
      68 && oe !== (oe = /*x*/
      f[2] * /*scaleX*/
      f[6]) && o(T, "cx", oe), k[0] & /*y, height, scaleY*/
      138 && se !== (se = /*y*/
      (f[3] + /*height*/
      f[1]) * /*scaleY*/
      f[7]) && o(T, "cy", se), k[0] & /*x, width, scaleX*/
      69 && p !== (p = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(Q, "cx", p), k[0] & /*y, height, scaleY*/
      138 && H !== (H = /*y*/
      (f[3] + /*height*/
      f[1]) * /*scaleY*/
      f[7]) && o(Q, "cy", H), k[0] & /*x, width, scaleX*/
      69 && we !== (we = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6] - 10) && o(Y, "x1", we), k[0] & /*x, width, scaleX*/
      69 && he !== (he = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(Y, "x2", he), k[0] & /*y, scaleY*/
      136 && me !== (me = /*y*/
      f[3] * /*scaleY*/
      f[7] - 13) && o(Y, "y1", me), k[0] & /*y, scaleY*/
      136 && be !== (be = /*y*/
      f[3] * /*scaleY*/
      f[7] - 3) && o(Y, "y2", be), k[0] & /*color*/
      1024 && R(
        Y,
        "stroke",
        /*color*/
        f[10]
      ), k[0] & /*x, width, scaleX*/
      69 && ye !== (ye = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6] - 10) && o(G, "x1", ye), k[0] & /*x, width, scaleX*/
      69 && ke !== (ke = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6]) && o(G, "x2", ke), k[0] & /*y, scaleY*/
      136 && ve !== (ve = /*y*/
      f[3] * /*scaleY*/
      f[7] - 3) && o(G, "y1", ve), k[0] & /*y, scaleY*/
      136 && Me !== (Me = /*y*/
      f[3] * /*scaleY*/
      f[7] - 13) && o(G, "y2", Me), k[0] & /*color*/
      1024 && R(
        G,
        "stroke",
        /*color*/
        f[10]
      ), k[0] & /*x, width, scaleX*/
      69 && Ee !== (Ee = /*x*/
      (f[2] + /*width*/
      f[0]) * /*scaleX*/
      f[6] - 11) && o(J, "x", Ee), k[0] & /*y, scaleY*/
      136 && Ce !== (Ce = /*y*/
      f[3] * /*scaleY*/
      f[7] - 14) && o(J, "y", Ce);
    },
    d(f) {
      f && (A(t), A(i), A(u), A(M), A(m), A(D), A(y), A(N), A(K), A(ce), A(j), A(F), A(T), A(ge), A(Q), A(Z), A(Y), A(pe), A(G), A(Pe), A(J)), Ne = !1, ne(Ue);
    }
  };
}
function bn(e) {
  let t, n, l, c, s, i, u, a, g, E, w, M, m, d, q, v, C, D, y, _ = !/*view_only*/
  e[9] && wt(e);
  return {
    c() {
      t = U("text"), n = Re(
        /*label*/
        e[4]
      ), s = L(), i = U("text"), u = Re(
        /*label*/
        e[4]
      ), E = L(), w = U("rect"), v = L(), _ && _.c(), C = Qt(), o(t, "filter", "url(#bg-text)"), o(t, "fill", "black"), o(t, "x", l = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(t, "y", c = /*y*/
      e[3] * /*scaleY*/
      e[7] - 4), o(i, "x", a = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(i, "y", g = /*y*/
      e[3] * /*scaleY*/
      e[7] - 4), o(i, "fill", "#333"), o(i, "class", "svelte-qvidok"), Te(i, "clickable", !/*view_only*/
      e[9]), o(w, "width", M = /*width*/
      e[0] * /*scaleX*/
      e[6]), o(w, "height", m = /*height*/
      e[1] * /*scaleY*/
      e[7]), R(
        w,
        "fill-opacity",
        /*opacity*/
        e[5]
      ), R(
        w,
        "stroke-width",
        /*isActive*/
        e[8] ? 3 : 2
      ), R(
        w,
        "stroke",
        /*color*/
        e[10]
      ), o(w, "shape-rendering", "crispEdges"), o(w, "x", d = /*x*/
      e[2] * /*scaleX*/
      e[6]), o(w, "y", q = /*y*/
      e[3] * /*scaleY*/
      e[7]), o(w, "class", "svelte-qvidok"), Te(w, "movable", !/*view_only*/
      e[9]);
    },
    m(h, b) {
      B(h, t, b), P(t, n), B(h, s, b), B(h, i, b), P(i, u), B(h, E, b), B(h, w, b), B(h, v, b), _ && _.m(h, b), B(h, C, b), D || (y = [
        X(
          i,
          "mousedown",
          /*relabel*/
          e[14]
        ),
        X(
          w,
          "mousedown",
          /*startMoving*/
          e[11]
        )
      ], D = !0);
    },
    p(h, b) {
      b[0] & /*label*/
      16 && Ge(
        n,
        /*label*/
        h[4]
      ), b[0] & /*x, scaleX*/
      68 && l !== (l = /*x*/
      h[2] * /*scaleX*/
      h[6]) && o(t, "x", l), b[0] & /*y, scaleY*/
      136 && c !== (c = /*y*/
      h[3] * /*scaleY*/
      h[7] - 4) && o(t, "y", c), b[0] & /*label*/
      16 && Ge(
        u,
        /*label*/
        h[4]
      ), b[0] & /*x, scaleX*/
      68 && a !== (a = /*x*/
      h[2] * /*scaleX*/
      h[6]) && o(i, "x", a), b[0] & /*y, scaleY*/
      136 && g !== (g = /*y*/
      h[3] * /*scaleY*/
      h[7] - 4) && o(i, "y", g), b[0] & /*view_only*/
      512 && Te(i, "clickable", !/*view_only*/
      h[9]), b[0] & /*width, scaleX*/
      65 && M !== (M = /*width*/
      h[0] * /*scaleX*/
      h[6]) && o(w, "width", M), b[0] & /*height, scaleY*/
      130 && m !== (m = /*height*/
      h[1] * /*scaleY*/
      h[7]) && o(w, "height", m), b[0] & /*opacity*/
      32 && R(
        w,
        "fill-opacity",
        /*opacity*/
        h[5]
      ), b[0] & /*isActive*/
      256 && R(
        w,
        "stroke-width",
        /*isActive*/
        h[8] ? 3 : 2
      ), b[0] & /*color*/
      1024 && R(
        w,
        "stroke",
        /*color*/
        h[10]
      ), b[0] & /*x, scaleX*/
      68 && d !== (d = /*x*/
      h[2] * /*scaleX*/
      h[6]) && o(w, "x", d), b[0] & /*y, scaleY*/
      136 && q !== (q = /*y*/
      h[3] * /*scaleY*/
      h[7]) && o(w, "y", q), b[0] & /*view_only*/
      512 && Te(w, "movable", !/*view_only*/
      h[9]), /*view_only*/
      h[9] ? _ && (_.d(1), _ = null) : _ ? _.p(h, b) : (_ = wt(h), _.c(), _.m(C.parentNode, C));
    },
    i: $,
    o: $,
    d(h) {
      h && (A(t), A(s), A(i), A(E), A(w), A(v), A(C)), _ && _.d(h), D = !1, ne(y);
    }
  };
}
function wn(e, t, n) {
  let { width: l = 0 } = t, { height: c = 0 } = t, { x: s = 0 } = t, { y: i = 0 } = t, { label: u = "" } = t, { colors: a = ["red"] } = t, { classes: g = [] } = t, { opacity: E = 0 } = t, { toImageCoordinates: w } = t, { scaleX: M = 1 } = t, { scaleY: m = 1 } = t, { isActive: d = !1 } = t, { view_only: q = !1 } = t;
  const v = on();
  let C = 0, D = 0, y = 0, _ = 0, h = !1, b = !1, z = "rgb(255,64,64)";
  function N(p) {
    p.button === 0 && (p.stopPropagation(), C = p.clientX, D = p.clientY, y = s, _ = i, v("move", q ? null : K));
  }
  function K(p) {
    p.stopPropagation(), p.preventDefault();
    const H = (p.clientX - C) / M, Z = (p.clientY - D) / m;
    n(2, s = Math.round(y + H)), n(3, i = Math.round(_ + Z));
  }
  function O(p, H) {
    p.button === 0 && (p.stopPropagation(), h = !1, b = !1, H.includes("top") ? (b = !0, _ = i + c) : H.includes("bottom") && (b = !0, _ = i), H.includes("left") ? (h = !0, y = s + l) : H.includes("right") && (h = !0, y = s), v("move", x));
  }
  function x(p) {
    p.stopPropagation(), p.preventDefault();
    const H = w(p), Z = Math.round(H.x), Y = Math.round(H.y);
    h && (n(2, s = Math.min(y, Z)), n(0, l = Math.max(y, Z) - s)), b && (n(3, i = Math.min(_, Y)), n(1, c = Math.max(_, Y) - i));
  }
  function ce(p) {
    p.button === 0 && (p.stopPropagation(), v("remove"));
  }
  function j(p) {
    q || p.button === 0 && (p.stopPropagation(), v("label"));
  }
  ln(() => {
    y = s, _ = i, C = s, D = i, h = !0, b = !0, v("create", x);
  });
  const ie = (p) => O(p, "top"), V = (p) => O(p, "bottom"), F = (p) => O(p, "left"), T = (p) => O(p, "right"), oe = (p) => O(p, "top-left"), se = (p) => O(p, "top-right"), ge = (p) => O(p, "bottom-left"), Q = (p) => O(p, "bottom-right");
  return e.$$set = (p) => {
    "width" in p && n(0, l = p.width), "height" in p && n(1, c = p.height), "x" in p && n(2, s = p.x), "y" in p && n(3, i = p.y), "label" in p && n(4, u = p.label), "colors" in p && n(15, a = p.colors), "classes" in p && n(16, g = p.classes), "opacity" in p && n(5, E = p.opacity), "toImageCoordinates" in p && n(17, w = p.toImageCoordinates), "scaleX" in p && n(6, M = p.scaleX), "scaleY" in p && n(7, m = p.scaleY), "isActive" in p && n(8, d = p.isActive), "view_only" in p && n(9, q = p.view_only);
  }, e.$$.update = () => {
    e.$$.dirty[0] & /*colors, classes, label*/
    98320 && n(10, z = a[Math.max(0, g.indexOf(u) % a.length)]);
  }, [
    l,
    c,
    s,
    i,
    u,
    E,
    M,
    m,
    d,
    q,
    z,
    N,
    O,
    ce,
    j,
    a,
    g,
    w,
    ie,
    V,
    F,
    T,
    oe,
    se,
    ge,
    Q
  ];
}
class pn extends ct {
  constructor(t) {
    super(), _t(
      this,
      t,
      wn,
      bn,
      et,
      {
        width: 0,
        height: 1,
        x: 2,
        y: 3,
        label: 4,
        colors: 15,
        classes: 16,
        opacity: 5,
        toImageCoordinates: 17,
        scaleX: 6,
        scaleY: 7,
        isActive: 8,
        view_only: 9
      },
      null,
      [-1, -1]
    );
  }
}
function pt(e) {
  let t, n;
  return {
    c() {
      t = ee("i"), o(t, "class", n = "fa fa-" + /*icon*/
      e[1]);
    },
    m(l, c) {
      B(l, t, c);
    },
    p(l, c) {
      c & /*icon*/
      2 && n !== (n = "fa fa-" + /*icon*/
      l[1]) && o(t, "class", n);
    },
    d(l) {
      l && A(t);
    }
  };
}
function yn(e) {
  let t, n, l, c, s, i, u = (
    /*icon*/
    e[1] !== "" && pt(e)
  );
  return {
    c() {
      t = ee("button"), u && u.c(), n = L(), l = Re(
        /*text*/
        e[0]
      ), o(t, "class", c = gt(
        /*style*/
        e[2]
      ) + " svelte-s4c08i"), o(
        t,
        "title",
        /*tooltip*/
        e[3]
      );
    },
    m(a, g) {
      B(a, t, g), u && u.m(t, null), P(t, n), P(t, l), s || (i = X(
        t,
        "click",
        /*click_handler*/
        e[4]
      ), s = !0);
    },
    p(a, [g]) {
      /*icon*/
      a[1] !== "" ? u ? u.p(a, g) : (u = pt(a), u.c(), u.m(t, n)) : u && (u.d(1), u = null), g & /*text*/
      1 && Ge(
        l,
        /*text*/
        a[0]
      ), g & /*style*/
      4 && c !== (c = gt(
        /*style*/
        a[2]
      ) + " svelte-s4c08i") && o(t, "class", c), g & /*tooltip*/
      8 && o(
        t,
        "title",
        /*tooltip*/
        a[3]
      );
    },
    i: $,
    o: $,
    d(a) {
      a && A(t), u && u.d(), s = !1, i();
    }
  };
}
function kn(e, t, n) {
  let { text: l = "" } = t, { icon: c = "" } = t, { style: s = "" } = t, { tooltip: i = "" } = t;
  function u(a) {
    sn.call(this, e, a);
  }
  return e.$$set = (a) => {
    "text" in a && n(0, l = a.text), "icon" in a && n(1, c = a.icon), "style" in a && n(2, s = a.style), "tooltip" in a && n(3, i = a.tooltip);
  }, [l, c, s, i, u];
}
class yt extends ct {
  constructor(t) {
    super(), _t(this, t, kn, yn, et, { text: 0, icon: 1, style: 2, tooltip: 3 });
  }
}
const Ae = [];
function vn(e, t = $) {
  let n;
  const l = /* @__PURE__ */ new Set();
  function c(u) {
    if (et(e, u) && (e = u, n)) {
      const a = !Ae.length;
      for (const g of l)
        g[1](), Ae.push(g, e);
      if (a) {
        for (let g = 0; g < Ae.length; g += 2)
          Ae[g][0](Ae[g + 1]);
        Ae.length = 0;
      }
    }
  }
  function s(u) {
    c(u(e));
  }
  function i(u, a = $) {
    const g = [u, a];
    return l.add(g), l.size === 1 && (n = t(c, s) || $), u(e), () => {
      l.delete(g), l.size === 0 && n && (n(), n = null);
    };
  }
  return { set: c, update: s, subscribe: i };
}
function ue(e, t, n) {
  const l = t, c = e.get(l), s = vn(c === void 0 ? n : c);
  return e.on("change:" + l, () => s.set(e.get(l)), null), {
    set: (i) => {
      s.set(i), e.set(l, i), e.save_changes();
    },
    subscribe: s.subscribe,
    update: (i) => {
      s.update((u) => {
        let a = i(u);
        return e.set(l, a), e.save_changes(), a;
      });
    }
  };
}
function kt(e, { delay: t = 0, duration: n = 400, easing: l = At } = {}) {
  const c = +getComputedStyle(e).opacity;
  return {
    delay: t,
    duration: n,
    easing: l,
    css: (s) => `opacity: ${s * c}`
  };
}
const { Map: Mn } = Vt;
function vt(e, t, n) {
  const l = e.slice();
  return l[60] = t[n], l[62] = n, l;
}
function Mt(e, t, n) {
  const l = e.slice();
  return l[63] = t[n], l[64] = t, l[62] = n, l;
}
function Et(e) {
  let t, n, l, c, s;
  return n = new yt({
    props: {
      text: "Skip",
      icon: "arrow-right",
      tooltip: "Keyboard shortcut: Space"
    }
  }), n.$on(
    "click",
    /*skip*/
    e[37]
  ), c = new yt({
    props: {
      text: "Submit",
      icon: "check",
      style: "success",
      tooltip: "Keyboard shortcut: Enter"
    }
  }), c.$on(
    "click",
    /*submit*/
    e[38]
  ), {
    c() {
      t = ee("div"), ut(n.$$.fragment), l = L(), ut(c.$$.fragment), o(t, "class", "buttons svelte-n5k047");
    },
    m(i, u) {
      B(i, t, u), $e(n, t, null), P(t, l), $e(c, t, null), s = !0;
    },
    p: $,
    i(i) {
      s || (te(n.$$.fragment, i), te(c.$$.fragment, i), s = !0);
    },
    o(i) {
      _e(n.$$.fragment, i), _e(c.$$.fragment, i), s = !1;
    },
    d(i) {
      i && A(t), xe(n), xe(c);
    }
  };
}
function Ct(e) {
  let t, n, l, c, s, i = [], u = new Mn(), a, g, E, w = Ze(
    /*sortedBBoxes*/
    e[1]
  );
  const M = (m) => (
    /*sortedIndexToOriginal*/
    m[11][
      /*i*/
      m[62]
    ]
  );
  for (let m = 0; m < w.length; m += 1) {
    let d = Mt(e, w, m), q = M(d);
    u.set(q, i[m] = qt(q, d));
  }
  return {
    c() {
      t = U("svg"), n = U("defs"), l = U("filter"), c = U("feFlood"), s = U("feComposite");
      for (let m = 0; m < i.length; m += 1)
        i[m].c();
      o(c, "flood-color", "rgba(255,255,255,0.5)"), o(s, "in", "SourceGraphic"), o(s, "operator", "xor"), o(l, "x", "0"), o(l, "y", "0"), o(l, "width", "1"), o(l, "height", "1"), o(l, "id", "bg-text"), o(
        t,
        "width",
        /*imgWidth*/
        e[7]
      ), o(
        t,
        "height",
        /*imgHeight*/
        e[6]
      ), o(t, "class", "svelte-n5k047");
    },
    m(m, d) {
      B(m, t, d), P(t, n), P(n, l), P(l, c), P(l, s);
      for (let q = 0; q < i.length; q += 1)
        i[q] && i[q].m(t, null);
      a = !0, g || (E = [
        X(
          t,
          "mousedown",
          /*handleMouseDown*/
          e[29]
        ),
        X(
          t,
          "mousemove",
          /*handleMouseMove*/
          e[31]
        ),
        X(
          t,
          "mouseup",
          /*handleMouseUp*/
          e[30]
        )
      ], g = !0);
    },
    p(m, d) {
      d[0] & /*getImageCoordinates, $classes, $colors, imgWidth, naturalWidth, imgHeight, naturalHeight, sortedIndexToOriginal, sortedBBoxes, $selected_index, $view_only, moveFn, $label*/
      134314970 | d[1] & /*remove, onCreateBBox, updateBBoxes*/
      14 && (w = Ze(
        /*sortedBBoxes*/
        m[1]
      ), st(), i = dn(i, d, M, 1, m, w, u, t, hn, qt, null, Mt), ft()), (!a || d[0] & /*imgWidth*/
      128) && o(
        t,
        "width",
        /*imgWidth*/
        m[7]
      ), (!a || d[0] & /*imgHeight*/
      64) && o(
        t,
        "height",
        /*imgHeight*/
        m[6]
      );
    },
    i(m) {
      if (!a) {
        for (let d = 0; d < w.length; d += 1)
          te(i[d]);
        a = !0;
      }
    },
    o(m) {
      for (let d = 0; d < i.length; d += 1)
        _e(i[d]);
      a = !1;
    },
    d(m) {
      m && A(t);
      for (let d = 0; d < i.length; d += 1)
        i[d].d();
      g = !1, ne(E);
    }
  };
}
function qt(e, t) {
  let n, l, c, s, i, u, a, g, E;
  function w(_) {
    t[45](
      _,
      /*bbox*/
      t[63]
    );
  }
  function M(_) {
    t[46](
      _,
      /*bbox*/
      t[63]
    );
  }
  function m(_) {
    t[47](
      _,
      /*bbox*/
      t[63]
    );
  }
  function d(_) {
    t[48](
      _,
      /*bbox*/
      t[63]
    );
  }
  function q(_) {
    t[49](
      _,
      /*bbox*/
      t[63]
    );
  }
  function v() {
    return (
      /*remove_handler*/
      t[50](
        /*bbox*/
        t[63]
      )
    );
  }
  function C(..._) {
    return (
      /*move_handler*/
      t[51](
        /*i*/
        t[62],
        ..._
      )
    );
  }
  function D() {
    return (
      /*label_handler*/
      t[52](
        /*bbox*/
        t[63],
        /*each_value_1*/
        t[64],
        /*i*/
        t[62]
      )
    );
  }
  let y = {
    toImageCoordinates: (
      /*getImageCoordinates*/
      t[27]
    ),
    classes: (
      /*$classes*/
      t[4]
    ),
    colors: (
      /*$colors*/
      t[16]
    ),
    scaleX: (
      /*imgWidth*/
      t[7] / /*naturalWidth*/
      t[9]
    ),
    scaleY: (
      /*imgHeight*/
      t[6] / /*naturalHeight*/
      t[8]
    ),
    isActive: (
      /*sortedIndexToOriginal*/
      t[11][
        /*i*/
        t[62]
      ] === /*$selected_index*/
      t[3]
    ),
    view_only: (
      /*$view_only*/
      t[14]
    )
  };
  return (
    /*bbox*/
    t[63].x !== void 0 && (y.x = /*bbox*/
    t[63].x), /*bbox*/
    t[63].y !== void 0 && (y.y = /*bbox*/
    t[63].y), /*bbox*/
    t[63].width !== void 0 && (y.width = /*bbox*/
    t[63].width), /*bbox*/
    t[63].height !== void 0 && (y.height = /*bbox*/
    t[63].height), /*bbox*/
    t[63].label !== void 0 && (y.label = /*bbox*/
    t[63].label), l = new pn({ props: y }), re.push(() => Ye(l, "x", w)), re.push(() => Ye(l, "y", M)), re.push(() => Ye(l, "width", m)), re.push(() => Ye(l, "height", d)), re.push(() => Ye(l, "label", q)), l.$on("remove", v), l.$on("move", C), l.$on(
      "create",
      /*onCreateBBox*/
      t[34]
    ), l.$on("label", D), {
      key: e,
      first: null,
      c() {
        n = U("g"), ut(l.$$.fragment), this.first = n;
      },
      m(_, h) {
        B(_, n, h), $e(l, n, null), E = !0;
      },
      p(_, h) {
        t = _;
        const b = {};
        h[0] & /*$classes*/
        16 && (b.classes = /*$classes*/
        t[4]), h[0] & /*$colors*/
        65536 && (b.colors = /*$colors*/
        t[16]), h[0] & /*imgWidth, naturalWidth*/
        640 && (b.scaleX = /*imgWidth*/
        t[7] / /*naturalWidth*/
        t[9]), h[0] & /*imgHeight, naturalHeight*/
        320 && (b.scaleY = /*imgHeight*/
        t[6] / /*naturalHeight*/
        t[8]), h[0] & /*sortedIndexToOriginal, sortedBBoxes, $selected_index*/
        2058 && (b.isActive = /*sortedIndexToOriginal*/
        t[11][
          /*i*/
          t[62]
        ] === /*$selected_index*/
        t[3]), h[0] & /*$view_only*/
        16384 && (b.view_only = /*$view_only*/
        t[14]), !c && h[0] & /*sortedBBoxes*/
        2 && (c = !0, b.x = /*bbox*/
        t[63].x, Oe(() => c = !1)), !s && h[0] & /*sortedBBoxes*/
        2 && (s = !0, b.y = /*bbox*/
        t[63].y, Oe(() => s = !1)), !i && h[0] & /*sortedBBoxes*/
        2 && (i = !0, b.width = /*bbox*/
        t[63].width, Oe(() => i = !1)), !u && h[0] & /*sortedBBoxes*/
        2 && (u = !0, b.height = /*bbox*/
        t[63].height, Oe(() => u = !1)), !a && h[0] & /*sortedBBoxes*/
        2 && (a = !0, b.label = /*bbox*/
        t[63].label, Oe(() => a = !1)), l.$set(b);
      },
      i(_) {
        E || (te(l.$$.fragment, _), _ && Ke(() => {
          E && (g || (g = bt(n, kt, { duration: 100 }, !0)), g.run(1));
        }), E = !0);
      },
      o(_) {
        _e(l.$$.fragment, _), _ && (g || (g = bt(n, kt, { duration: 100 }, !1)), g.run(0)), E = !1;
      },
      d(_) {
        _ && A(n), xe(l), _ && g && g.end();
      }
    }
  );
}
function En(e) {
  let t;
  return {
    c() {
      t = ee("span"), t.textContent = `${/*i*/
      (e[62] + 1) % 10}`, o(t, "class", "key svelte-n5k047");
    },
    m(n, l) {
      B(n, t, l);
    },
    d(n) {
      n && A(t);
    }
  };
}
function St(e) {
  let t, n = (
    /*_class*/
    e[60] + ""
  ), l, c, s, i, u, a = (
    /*i*/
    e[62] <= 9 && En(e)
  );
  function g() {
    return (
      /*click_handler*/
      e[53](
        /*_class*/
        e[60]
      )
    );
  }
  return {
    c() {
      t = ee("div"), l = Re(n), c = L(), a && a.c(), s = L(), o(t, "class", "class-label svelte-n5k047"), R(
        t,
        "color",
        /*$colors*/
        e[16][
          /*i*/
          e[62] % /*$colors*/
          e[16].length
        ]
      ), R(
        t,
        "border",
        /*_class*/
        (e[60] === /*$label*/
        e[13] ? 1 : 0) + "px solid " + /*$colors*/
        e[16][
          /*i*/
          e[62] % /*$colors*/
          e[16].length
        ]
      );
    },
    m(E, w) {
      B(E, t, w), P(t, l), P(t, c), a && a.m(t, null), P(t, s), i || (u = X(t, "click", g), i = !0);
    },
    p(E, w) {
      e = E, w[0] & /*$classes*/
      16 && n !== (n = /*_class*/
      e[60] + "") && Ge(l, n), w[0] & /*$colors*/
      65536 && R(
        t,
        "color",
        /*$colors*/
        e[16][
          /*i*/
          e[62] % /*$colors*/
          e[16].length
        ]
      ), w[0] & /*$classes, $label, $colors*/
      73744 && R(
        t,
        "border",
        /*_class*/
        (e[60] === /*$label*/
        e[13] ? 1 : 0) + "px solid " + /*$colors*/
        e[16][
          /*i*/
          e[62] % /*$colors*/
          e[16].length
        ]
      );
    },
    d(E) {
      E && A(t), a && a.d(), i = !1, u();
    }
  };
}
function Cn(e) {
  let t, n, l, c, s, i, u, a, g, E, w, M, m, d, q, v = !/*$hide_buttons*/
  e[15] && Et(e), C = (
    /*showSVG*/
    e[10] && Ct(e)
  ), D = Ze(
    /*$classes*/
    e[4]
  ), y = [];
  for (let _ = 0; _ < D.length; _ += 1)
    y[_] = St(vt(e, D, _));
  return {
    c() {
      t = ee("div"), v && v.c(), n = L(), l = ee("div"), c = ee("div"), s = ee("img"), a = L(), C && C.c(), g = L(), E = ee("div"), w = ee("p"), w.textContent = "Classes:", M = L();
      for (let _ = 0; _ < y.length; _ += 1)
        y[_].c();
      dt(s.src, i = /*image_src*/
      e[2]) || o(s, "src", i), o(s, "alt", "annotate me"), o(s, "class", "svelte-n5k047"), o(c, "class", "image-measure svelte-n5k047"), Ke(() => (
        /*div0_elementresize_handler*/
        e[44].call(c)
      )), o(l, "class", "image svelte-n5k047"), o(E, "class", "classes svelte-n5k047"), o(t, "class", "wrapper svelte-n5k047"), o(t, "tabindex", "0");
    },
    m(_, h) {
      B(_, t, h), v && v.m(t, null), P(t, n), P(t, l), P(l, c), P(c, s), e[43](s), u = $t(
        c,
        /*div0_elementresize_handler*/
        e[44].bind(c)
      ), P(l, a), C && C.m(l, null), P(t, g), P(t, E), P(E, w), P(E, M);
      for (let b = 0; b < y.length; b += 1)
        y[b] && y[b].m(E, null);
      e[54](t), m = !0, d || (q = [
        X(
          s,
          "load",
          /*initSVG*/
          e[28]
        ),
        X(
          t,
          "keydown",
          /*keydown_handler*/
          e[55]
        ),
        X(
          t,
          "keyup",
          /*keyup_handler*/
          e[56]
        ),
        X(
          t,
          "blur",
          /*blur_handler*/
          e[57]
        )
      ], d = !0);
    },
    p(_, h) {
      if (/*$hide_buttons*/
      _[15] ? v && (st(), _e(v, 1, 1, () => {
        v = null;
      }), ft()) : v ? (v.p(_, h), h[0] & /*$hide_buttons*/
      32768 && te(v, 1)) : (v = Et(_), v.c(), te(v, 1), v.m(t, n)), (!m || h[0] & /*image_src*/
      4 && !dt(s.src, i = /*image_src*/
      _[2])) && o(s, "src", i), /*showSVG*/
      _[10] ? C ? (C.p(_, h), h[0] & /*showSVG*/
      1024 && te(C, 1)) : (C = Ct(_), C.c(), te(C, 1), C.m(l, null)) : C && (st(), _e(C, 1, 1, () => {
        C = null;
      }), ft()), h[0] & /*$colors, $classes, $label*/
      73744) {
        D = Ze(
          /*$classes*/
          _[4]
        );
        let b;
        for (b = 0; b < D.length; b += 1) {
          const z = vt(_, D, b);
          y[b] ? y[b].p(z, h) : (y[b] = St(z), y[b].c(), y[b].m(E, null));
        }
        for (; b < y.length; b += 1)
          y[b].d(1);
        y.length = D.length;
      }
    },
    i(_) {
      m || (te(v), te(C), m = !0);
    },
    o(_) {
      _e(v), _e(C), m = !1;
    },
    d(_) {
      _ && A(t), v && v.d(), e[43](null), u(), C && C.d(), Gt(y, _), e[54](null), d = !1, ne(q);
    }
  };
}
function qn(e, t, n) {
  let l, c, s, i, u, a, g, E, w, { model: M } = t, m, d, q = 0, v = 0, C = 0, D = 0, y = !1, _ = [], h = [], b = null, z = !1, N = /* @__PURE__ */ new Set(), K = ue(M, "image_url");
  fe(e, K, (r) => n(40, l = r));
  let O = ue(M, "image_bytes");
  fe(e, O, (r) => n(41, c = r));
  let x = null, ce = ue(M, "classes", [""]);
  fe(e, ce, (r) => n(4, u = r));
  let j = ue(M, "label", "");
  fe(e, j, (r) => n(13, a = r));
  let ie = ue(M, "colors", [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf"
  ]);
  fe(e, ie, (r) => n(16, w = r));
  let V = ue(M, "bboxes", []);
  fe(e, V, (r) => n(42, i = r));
  let F = ue(M, "selected_index", -1);
  fe(e, F, (r) => n(3, s = r));
  let T = ue(M, "view_only", !1);
  fe(e, T, (r) => n(14, g = r));
  let oe = ue(M, "hide_buttons", !1);
  fe(e, oe, (r) => n(15, E = r));
  function se(r) {
    const S = d.getBoundingClientRect(), W = (r.clientX - S.left) * D / v, le = (r.clientY - S.top) * C / q;
    return { x: W, y: le };
  }
  function ge() {
    n(10, y = !0), n(9, D = d.naturalWidth), n(8, C = d.naturalHeight);
    const r = d.getBoundingClientRect();
    n(6, q = r.height), n(7, v = r.width);
  }
  function Q(r) {
    if (r.button !== 0)
      return;
    if (g) {
      I(F, s = -1, s);
      return;
    }
    const { x: S, y: W } = se(r), le = {
      x: Math.round(S),
      y: Math.round(W),
      width: 0,
      height: 0,
      label: a
    };
    z = !0, I(V, i = [...i, le], i), I(F, s = i.length - 1, s);
  }
  function p(r) {
    r.button === 0 && (r.preventDefault(), n(12, b = null), Z());
  }
  function H(r) {
    b !== null && b(r);
  }
  function Z() {
    M.set("bboxes", [], { silent: !0 }), M.set("bboxes", [...i]), M.save_changes();
  }
  function Y(r) {
    const S = i.indexOf(r);
    s > S && I(F, s -= 1, s), s == i.length - 1 && I(F, s = -1, s), I(V, i = i.filter((W) => W !== r), i);
  }
  function we(r) {
    z && (n(12, b = r.detail), z = !1);
  }
  const he = /* @__PURE__ */ new Map([
    ["KeyW", "up"],
    ["KeyA", "left"],
    ["KeyS", "down"],
    ["KeyD", "right"],
    ["KeyQ", "shrink-width"],
    ["KeyE", "grow-width"],
    ["KeyR", "grow-height"],
    ["KeyF", "shrink-height"]
  ]);
  function me(r) {
    if (r.stopPropagation(), r.preventDefault(), r.code.startsWith("Digit") || /Numpad\d/.test(r.code)) {
      let S = Number(r.code.slice(-1));
      S === 0 && (S = 10), S -= 1, S < u.length && I(j, a = u[S], a);
    } else if (r.code === "Escape")
      m.blur();
    else if (r.code === "Tab") {
      const S = r.shiftKey ? -1 : 1;
      I(F, s += S, s), s >= i.length ? I(F, s = -1, s) : s === -2 && I(F, s = i.length - 1, s);
    } else r.code === "Space" && !E ? be() : (r.code === "Enter" || r.code === "NumpadEnter") && !E && pe();
    if (s >= 0 && !g) {
      let S = he.get(r.code);
      S && N.add(S), r.code === "Delete" && Y(i[s]), r.code === "KeyC" && (I(V, i[s].label = a, i), Z());
      let W = r.shiftKey ? 10 : 1, le = 0, qe = 0, je = 0, Ie = 0;
      for (let de of N)
        de === "up" ? qe -= W : de === "down" ? qe += W : de === "right" ? le += W : de === "left" ? le -= W : de === "shrink-width" ? (je -= 2 * W, le += W) : de === "grow-width" ? (je += 2 * W, le -= W) : de === "shrink-height" ? (Ie -= 2 * W, qe += W) : de === "grow-height" && (Ie += 2 * W, qe -= W);
      (le !== 0 || qe !== 0 || je !== 0 || Ie !== 0) && (I(V, i[s].x += le, i), I(V, i[s].y += qe, i), I(V, i[s].width += je, i), I(V, i[s].height += Ie, i), Z());
    }
  }
  function be() {
    M.send({ type: "skip" }, {}), m.focus();
  }
  function pe() {
    M.send({ type: "submit" }, {}), m.focus();
  }
  function G(r) {
    return s === -1 ? r : r === i.length - 1 ? s : r < s ? r : r + 1;
  }
  function ye(r) {
    re[r ? "unshift" : "push"](() => {
      d = r, n(0, d);
    });
  }
  function ke() {
    q = this.clientHeight, v = this.clientWidth, n(6, q), n(7, v);
  }
  function ve(r, S) {
    e.$$.not_equal(S.x, r) && (S.x = r, n(1, _), n(3, s), n(42, i));
  }
  function Me(r, S) {
    e.$$.not_equal(S.y, r) && (S.y = r, n(1, _), n(3, s), n(42, i));
  }
  function Pe(r, S) {
    e.$$.not_equal(S.width, r) && (S.width = r, n(1, _), n(3, s), n(42, i));
  }
  function J(r, S) {
    e.$$.not_equal(S.height, r) && (S.height = r, n(1, _), n(3, s), n(42, i));
  }
  function Ee(r, S) {
    e.$$.not_equal(S.label, r) && (S.label = r, n(1, _), n(3, s), n(42, i));
  }
  const Ce = (r) => Y(r), Ne = (r, S) => {
    n(12, b = S.detail), I(F, s = h[r], s);
  }, Ue = (r, S, W) => {
    n(1, S[W].label = a, _), Z();
  }, f = (r) => I(j, a = r, a);
  function k(r) {
    re[r ? "unshift" : "push"](() => {
      m = r, n(5, m);
    });
  }
  const Ot = (r) => me(r), Xt = (r) => N.delete(he.get(r.code)), Yt = () => N.clear();
  return e.$$set = (r) => {
    "model" in r && n(39, M = r.model);
  }, e.$$.update = () => {
    if (e.$$.dirty[0] & /*$classes*/
    16 && I(j, a = u.length > 0 ? u[0] : "", a), e.$$.dirty[0] & /*$selected_index*/
    8 | e.$$.dirty[1] & /*$bboxes*/
    2048 && s >= i.length && I(F, s = -1, s), e.$$.dirty[0] & /*$selected_index*/
    8 | e.$$.dirty[1] & /*$bboxes*/
    2048 && n(1, _ = s === -1 ? i : [
      ...i.filter((r, S) => S !== s),
      i[s]
    ]), e.$$.dirty[0] & /*sortedBBoxes*/
    2 && n(11, h = _.map((r, S) => G(S))), e.$$.dirty[0] & /*img, image_src*/
    5 | e.$$.dirty[1] & /*$image_bytes*/
    1024 && d && c) {
      URL.revokeObjectURL(x);
      const r = new Blob([c]);
      n(2, x = URL.createObjectURL(r));
    }
    e.$$.dirty[0] & /*img, image_src*/
    5 | e.$$.dirty[1] & /*$image_url*/
    512 && d && l && (URL.revokeObjectURL(x), n(2, x = l));
  }, [
    d,
    _,
    x,
    s,
    u,
    m,
    q,
    v,
    C,
    D,
    y,
    h,
    b,
    a,
    g,
    E,
    w,
    N,
    K,
    O,
    ce,
    j,
    ie,
    V,
    F,
    T,
    oe,
    se,
    ge,
    Q,
    p,
    H,
    Z,
    Y,
    we,
    he,
    me,
    be,
    pe,
    M,
    l,
    c,
    i,
    ye,
    ke,
    ve,
    Me,
    Pe,
    J,
    Ee,
    Ce,
    Ne,
    Ue,
    f,
    k,
    Ot,
    Xt,
    Yt
  ];
}
class Sn extends ct {
  constructor(t) {
    super(), _t(this, t, qn, Cn, et, { model: 39 }, null, [-1, -1, -1]);
  }
}
function An({ model: e, el: t }) {
  let n = new Sn({ target: t, props: { model: e } });
  return () => n.$destroy();
}
const zn = { render: An };
export {
  zn as default
};
