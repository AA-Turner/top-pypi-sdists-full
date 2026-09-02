(function(){"use strict";try{if(typeof document<"u"){var r=document.createElement("style");r.appendChild(document.createTextNode('.driver-active .driver-overlay,.driver-active *{pointer-events:none}.driver-active .driver-active-element,.driver-active .driver-active-element *,.driver-popover,.driver-popover *{pointer-events:auto}@keyframes animate-fade-in{0%{opacity:0}to{opacity:1}}.driver-fade .driver-overlay{animation:animate-fade-in .2s ease-in-out}.driver-fade .driver-popover{animation:animate-fade-in .2s}.driver-popover{all:unset;box-sizing:border-box;color:#2d2d2d;margin:0;padding:15px;border-radius:5px;min-width:250px;max-width:300px;box-shadow:0 1px 10px #0006;z-index:1000000000;position:fixed;top:0;right:0;background-color:#fff}.driver-popover *{font-family:Helvetica Neue,Inter,ui-sans-serif,"Apple Color Emoji",Helvetica,Arial,sans-serif}.driver-popover-title{font:19px/normal sans-serif;font-weight:700;display:block;position:relative;line-height:1.5;zoom:1;margin:0}.driver-popover-close-btn{all:unset;position:absolute;top:0;right:0;width:32px;height:28px;cursor:pointer;font-size:18px;font-weight:500;color:#d2d2d2;z-index:1;text-align:center;transition:color;transition-duration:.2s}.driver-popover-close-btn:hover,.driver-popover-close-btn:focus{color:#2d2d2d}.driver-popover-title[style*=block]+.driver-popover-description{margin-top:5px}.driver-popover-description{margin-bottom:0;font:14px/normal sans-serif;line-height:1.5;font-weight:400;zoom:1}.driver-popover-footer{margin-top:15px;text-align:right;zoom:1;display:flex;align-items:center;justify-content:space-between}.driver-popover-progress-text{font-size:13px;font-weight:400;color:#727272;zoom:1}.driver-popover-footer button{all:unset;display:inline-block;box-sizing:border-box;padding:3px 7px;text-decoration:none;text-shadow:1px 1px 0 #fff;background-color:#fff;color:#2d2d2d;font:12px/normal sans-serif;cursor:pointer;outline:0;zoom:1;line-height:1.3;border:1px solid #ccc;border-radius:3px}.driver-popover-footer .driver-popover-btn-disabled{opacity:.5;pointer-events:none}:not(body):has(>.driver-active-element){overflow:hidden!important}.driver-no-interaction,.driver-no-interaction *{pointer-events:none!important}.driver-popover-footer button:hover,.driver-popover-footer button:focus{background-color:#f7f7f7}.driver-popover-navigation-btns{display:flex;flex-grow:1;justify-content:flex-end}.driver-popover-navigation-btns button+button{margin-left:4px}.driver-popover-arrow{content:"";position:absolute;border:5px solid #fff}.driver-popover-arrow-side-over{display:none}.driver-popover-arrow-side-left{left:100%;border-right-color:transparent;border-bottom-color:transparent;border-top-color:transparent}.driver-popover-arrow-side-right{right:100%;border-left-color:transparent;border-bottom-color:transparent;border-top-color:transparent}.driver-popover-arrow-side-top{top:100%;border-right-color:transparent;border-bottom-color:transparent;border-left-color:transparent}.driver-popover-arrow-side-bottom{bottom:100%;border-left-color:transparent;border-top-color:transparent;border-right-color:transparent}.driver-popover-arrow-side-center{display:none}.driver-popover-arrow-side-left.driver-popover-arrow-align-start,.driver-popover-arrow-side-right.driver-popover-arrow-align-start{top:15px}.driver-popover-arrow-side-top.driver-popover-arrow-align-start,.driver-popover-arrow-side-bottom.driver-popover-arrow-align-start{left:15px}.driver-popover-arrow-align-end.driver-popover-arrow-side-left,.driver-popover-arrow-align-end.driver-popover-arrow-side-right{bottom:15px}.driver-popover-arrow-side-top.driver-popover-arrow-align-end,.driver-popover-arrow-side-bottom.driver-popover-arrow-align-end{right:15px}.driver-popover-arrow-side-left.driver-popover-arrow-align-center,.driver-popover-arrow-side-right.driver-popover-arrow-align-center{top:50%;margin-top:-5px}.driver-popover-arrow-side-top.driver-popover-arrow-align-center,.driver-popover-arrow-side-bottom.driver-popover-arrow-align-center{left:50%;margin-left:-5px}.driver-popover-arrow-none{display:none}')),document.head.appendChild(r)}}catch(o){console.error("vite-plugin-css-injected-by-js",o)}})();
let Y = {}, U;
function F(e = {}) {
  Y = {
    animate: !0,
    allowClose: !0,
    overlayClickBehavior: "close",
    overlayOpacity: 0.7,
    smoothScroll: !1,
    disableActiveInteraction: !1,
    showProgress: !1,
    stagePadding: 10,
    stageRadius: 5,
    popoverOffset: 10,
    showButtons: ["next", "previous", "close"],
    disableButtons: [],
    overlayColor: "#000",
    ...e
  };
}
function r(e) {
  return e ? Y[e] : Y;
}
function ve(e) {
  U = e;
}
function E() {
  return U;
}
let O = {};
function R(e, t) {
  O[e] = t;
}
function $(e) {
  var t;
  (t = O[e]) == null || t.call(O);
}
function ue() {
  O = {};
}
function z(e, t, n, i) {
  return (e /= i / 2) < 1 ? n / 2 * e * e + t : -n / 2 * (--e * (e - 2) - 1) + t;
}
function V(e) {
  const t = 'a[href]:not([disabled]), button:not([disabled]), textarea:not([disabled]), input[type="text"]:not([disabled]), input[type="radio"]:not([disabled]), input[type="checkbox"]:not([disabled]), select:not([disabled])';
  return e.flatMap((n) => {
    const i = n.matches(t), o = Array.from(n.querySelectorAll(t));
    return [...i ? [n] : [], ...o];
  }).filter((n) => getComputedStyle(n).pointerEvents !== "none" && fe(n));
}
function ee(e) {
  if (!e || me(e))
    return;
  const t = r("smoothScroll"), n = e.offsetHeight > window.innerHeight;
  e.scrollIntoView({
    // Removing the smooth scrolling for elements which exist inside the scrollable parent
    // This was causing the highlight to not properly render
    behavior: !t || he(e) ? "auto" : "smooth",
    inline: "center",
    block: n ? "start" : "center"
  });
}
function he(e) {
  if (!e || !e.parentElement)
    return;
  const t = e.parentElement;
  return t.scrollHeight > t.clientHeight;
}
function me(e) {
  const t = e.getBoundingClientRect();
  return t.top >= 0 && t.left >= 0 && t.bottom <= (window.innerHeight || document.documentElement.clientHeight) && t.right <= (window.innerWidth || document.documentElement.clientWidth);
}
function fe(e) {
  return !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
}
let q = {};
function k(e, t) {
  q[e] = t;
}
function a(e) {
  return e ? q[e] : q;
}
function K() {
  q = {};
}
function we(e, t, n, i) {
  let o = a("__activeStagePosition");
  const s = o || n.getBoundingClientRect(), v = i.getBoundingClientRect(), g = z(e, s.x, v.x - s.x, t), d = z(e, s.y, v.y - s.y, t), m = z(e, s.width, v.width - s.width, t), h = z(e, s.height, v.height - s.height, t);
  o = {
    x: g,
    y: d,
    width: m,
    height: h
  }, ne(o), k("__activeStagePosition", o);
}
function te(e) {
  if (!e)
    return;
  const t = e.getBoundingClientRect(), n = {
    x: t.x,
    y: t.y,
    width: t.width,
    height: t.height
  };
  k("__activeStagePosition", n), ne(n);
}
function ge() {
  const e = a("__activeStagePosition"), t = a("__overlaySvg");
  if (!e)
    return;
  if (!t) {
    console.warn("No stage svg found.");
    return;
  }
  const n = window.innerWidth, i = window.innerHeight;
  t.setAttribute("viewBox", `0 0 ${n} ${i}`);
}
function ye(e) {
  const t = xe(e);
  document.body.appendChild(t), re(t, (n) => {
    n.target.tagName === "path" && $("overlayClick");
  }), k("__overlaySvg", t);
}
function ne(e) {
  const t = a("__overlaySvg");
  if (!t) {
    ye(e);
    return;
  }
  const n = t.firstElementChild;
  if (n?.tagName !== "path")
    throw new Error("no path element found in stage svg");
  n.setAttribute("d", oe(e));
}
function xe(e) {
  const t = window.innerWidth, n = window.innerHeight, i = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  i.classList.add("driver-overlay", "driver-overlay-animated"), i.setAttribute("viewBox", `0 0 ${t} ${n}`), i.setAttribute("xmlSpace", "preserve"), i.setAttribute("xmlnsXlink", "http://www.w3.org/1999/xlink"), i.setAttribute("version", "1.1"), i.setAttribute("preserveAspectRatio", "xMinYMin slice"), i.style.fillRule = "evenodd", i.style.clipRule = "evenodd", i.style.strokeLinejoin = "round", i.style.strokeMiterlimit = "2", i.style.zIndex = "10000", i.style.position = "fixed", i.style.top = "0", i.style.left = "0", i.style.width = "100%", i.style.height = "100%";
  const o = document.createElementNS("http://www.w3.org/2000/svg", "path");
  return o.setAttribute("d", oe(e)), o.style.fill = r("overlayColor") || "rgb(0,0,0)", o.style.opacity = `${r("overlayOpacity")}`, o.style.pointerEvents = "auto", o.style.cursor = "auto", i.appendChild(o), i;
}
function oe(e) {
  const t = window.innerWidth, n = window.innerHeight, i = r("stagePadding") || 0, o = r("stageRadius") || 0, s = e.width + i * 2, v = e.height + i * 2, g = Math.min(o, s / 2, v / 2), d = Math.floor(Math.max(g, 0)), m = e.x - i + d, h = e.y - i, x = s - d * 2, l = v - d * 2;
  return `M${t},0L0,0L0,${n}L${t},${n}L${t},0Z
    M${m},${h} h${x} a${d},${d} 0 0 1 ${d},${d} v${l} a${d},${d} 0 0 1 -${d},${d} h-${x} a${d},${d} 0 0 1 -${d},-${d} v-${l} a${d},${d} 0 0 1 ${d},-${d} z`;
}
function be() {
  const e = a("__overlaySvg");
  e && e.remove();
}
function Ce() {
  const e = document.getElementById("driver-dummy-element");
  if (e)
    return e;
  let t = document.createElement("div");
  return t.id = "driver-dummy-element", t.style.width = "0", t.style.height = "0", t.style.pointerEvents = "none", t.style.opacity = "0", t.style.position = "fixed", t.style.top = "50%", t.style.left = "50%", document.body.appendChild(t), t;
}
function Z(e) {
  const { element: t } = e;
  let n = typeof t == "function" ? t() : typeof t == "string" ? document.querySelector(t) : t;
  n || (n = Ce()), ke(n, e);
}
function _e() {
  const e = a("__activeElement"), t = a("__activeStep");
  e && (te(e), ge(), le(e, t));
}
function ke(e, t) {
  var n;
  const i = Date.now(), o = a("__activeStep"), s = a("__activeElement") || e, v = !s || s === e, g = e.id === "driver-dummy-element", d = s.id === "driver-dummy-element", m = r("animate"), h = t.onHighlightStarted || r("onHighlightStarted"), x = t?.onHighlighted || r("onHighlighted"), l = o?.onDeselected || r("onDeselected"), p = r(), u = a();
  !v && l && l(d ? void 0 : s, o, {
    config: p,
    state: u,
    driver: E()
  }), h && h(g ? void 0 : e, t, {
    config: p,
    state: u,
    driver: E()
  });
  const f = !v && m;
  let c = !1;
  Be(), k("previousStep", o), k("previousElement", s), k("activeStep", t), k("activeElement", e);
  const w = () => {
    if (a("__transitionCallback") !== w)
      return;
    const b = Date.now() - i, C = 400 - b <= 400 / 2;
    t.popover && C && !c && f && (J(e, t), c = !0), r("animate") && b < 400 ? we(b, 400, s, e) : (te(e), x && x(g ? void 0 : e, t, {
      config: r(),
      state: a(),
      driver: E()
    }), k("__transitionCallback", void 0), k("__previousStep", o), k("__previousElement", s), k("__activeStep", t), k("__activeElement", e)), window.requestAnimationFrame(w);
  };
  k("__transitionCallback", w), window.requestAnimationFrame(w), ee(e), !f && t.popover && J(e, t), s.classList.remove("driver-active-element", "driver-no-interaction"), s.removeAttribute("aria-haspopup"), s.removeAttribute("aria-expanded"), s.removeAttribute("aria-controls"), ((n = t.disableActiveInteraction) != null ? n : r("disableActiveInteraction")) && e.classList.add("driver-no-interaction"), e.classList.add("driver-active-element"), e.setAttribute("aria-haspopup", "dialog"), e.setAttribute("aria-expanded", "true"), e.setAttribute("aria-controls", "driver-popover-content");
}
function Le() {
  var e;
  (e = document.getElementById("driver-dummy-element")) == null || e.remove(), document.querySelectorAll(".driver-active-element").forEach((t) => {
    t.classList.remove("driver-active-element", "driver-no-interaction"), t.removeAttribute("aria-haspopup"), t.removeAttribute("aria-expanded"), t.removeAttribute("aria-controls");
  });
}
function T() {
  const e = a("__resizeTimeout");
  e && window.cancelAnimationFrame(e), k("__resizeTimeout", window.requestAnimationFrame(_e));
}
function Se(e) {
  var t;
  if (!a("isInitialized") || !(e.key === "Tab" || e.keyCode === 9))
    return;
  const n = a("__activeElement"), i = (t = a("popover")) == null ? void 0 : t.wrapper, o = V([
    ...i ? [i] : [],
    ...n ? [n] : []
  ]), s = o[0], v = o[o.length - 1];
  if (e.preventDefault(), e.shiftKey) {
    const g = o[o.indexOf(document.activeElement) - 1] || v;
    g?.focus();
  } else {
    const g = o[o.indexOf(document.activeElement) + 1] || s;
    g?.focus();
  }
}
function ie(e) {
  var t;
  ((t = r("allowKeyboardControl")) == null || t) && (e.key === "Escape" ? $("escapePress") : e.key === "ArrowRight" ? $("arrowRightPress") : e.key === "ArrowLeft" && $("arrowLeftPress"));
}
function re(e, t, n) {
  const i = (o, s) => {
    const v = o.target;
    e.contains(v) && ((!n || n(v)) && (o.preventDefault(), o.stopPropagation(), o.stopImmediatePropagation()), s?.(o));
  };
  document.addEventListener("pointerdown", i, !0), document.addEventListener("mousedown", i, !0), document.addEventListener("pointerup", i, !0), document.addEventListener("mouseup", i, !0), document.addEventListener(
    "click",
    (o) => {
      i(o, t);
    },
    !0
  );
}
function Ee() {
  window.addEventListener("keyup", ie, !1), window.addEventListener("keydown", Se, !1), window.addEventListener("resize", T), window.addEventListener("scroll", T);
}
function Pe() {
  window.removeEventListener("keyup", ie), window.removeEventListener("resize", T), window.removeEventListener("scroll", T);
}
function Be() {
  const e = a("popover");
  e && (e.wrapper.style.display = "none");
}
function J(e, t) {
  var n, i;
  let o = a("popover");
  o && document.body.removeChild(o.wrapper), o = Ae(), document.body.appendChild(o.wrapper);
  const {
    title: s,
    description: v,
    showButtons: g,
    disableButtons: d,
    showProgress: m,
    nextBtnText: h = r("nextBtnText") || "Next &rarr;",
    prevBtnText: x = r("prevBtnText") || "&larr; Previous",
    progressText: l = r("progressText") || "{current} of {total}"
  } = t.popover || {};
  o.nextButton.innerHTML = h, o.previousButton.innerHTML = x, o.progress.innerHTML = l, s ? (o.title.innerHTML = s, o.title.style.display = "block") : o.title.style.display = "none", v ? (o.description.innerHTML = v, o.description.style.display = "block") : o.description.style.display = "none";
  const p = g || r("showButtons"), u = m || r("showProgress") || !1, f = p?.includes("next") || p?.includes("previous") || u;
  o.closeButton.style.display = p.includes("close") ? "block" : "none", f ? (o.footer.style.display = "flex", o.progress.style.display = u ? "block" : "none", o.nextButton.style.display = p.includes("next") ? "block" : "none", o.previousButton.style.display = p.includes("previous") ? "block" : "none") : o.footer.style.display = "none";
  const c = d || r("disableButtons") || [];
  c != null && c.includes("next") && (o.nextButton.disabled = !0, o.nextButton.classList.add("driver-popover-btn-disabled")), c != null && c.includes("previous") && (o.previousButton.disabled = !0, o.previousButton.classList.add("driver-popover-btn-disabled")), c != null && c.includes("close") && (o.closeButton.disabled = !0, o.closeButton.classList.add("driver-popover-btn-disabled"));
  const w = o.wrapper;
  w.style.display = "block", w.style.left = "", w.style.top = "", w.style.bottom = "", w.style.right = "", w.id = "driver-popover-content", w.setAttribute("role", "dialog"), w.setAttribute("aria-labelledby", "driver-popover-title"), w.setAttribute("aria-describedby", "driver-popover-description");
  const b = o.arrow;
  b.className = "driver-popover-arrow";
  const C = ((n = t.popover) == null ? void 0 : n.popoverClass) || r("popoverClass") || "";
  w.className = `driver-popover ${C}`.trim(), re(
    o.wrapper,
    (P) => {
      var D, M, I;
      const H = P.target, W = ((D = t.popover) == null ? void 0 : D.onNextClick) || r("onNextClick"), A = ((M = t.popover) == null ? void 0 : M.onPrevClick) || r("onPrevClick"), N = ((I = t.popover) == null ? void 0 : I.onCloseClick) || r("onCloseClick");
      if (H.closest(".driver-popover-next-btn"))
        return W ? W(e, t, {
          config: r(),
          state: a(),
          driver: E()
        }) : $("nextClick");
      if (H.closest(".driver-popover-prev-btn"))
        return A ? A(e, t, {
          config: r(),
          state: a(),
          driver: E()
        }) : $("prevClick");
      if (H.closest(".driver-popover-close-btn"))
        return N ? N(e, t, {
          config: r(),
          state: a(),
          driver: E()
        }) : $("closeClick");
    },
    (P) => !(o != null && o.description.contains(P)) && !(o != null && o.title.contains(P)) && typeof P.className == "string" && P.className.includes("driver-popover")
  ), k("popover", o);
  const S = ((i = t.popover) == null ? void 0 : i.onPopoverRender) || r("onPopoverRender");
  S && S(o, {
    config: r(),
    state: a(),
    driver: E()
  }), le(e, t), ee(w);
  const _ = e.classList.contains("driver-dummy-element"), y = V([w, ..._ ? [] : [e]]);
  y.length > 0 && y[0].focus();
}
function se() {
  const e = a("popover");
  if (!(e != null && e.wrapper))
    return;
  const t = e.wrapper.getBoundingClientRect(), n = r("stagePadding") || 0, i = r("popoverOffset") || 0;
  return {
    width: t.width + n + i,
    height: t.height + n + i,
    realWidth: t.width,
    realHeight: t.height
  };
}
function X(e, t) {
  const { elementDimensions: n, popoverDimensions: i, popoverPadding: o, popoverArrowDimensions: s } = t;
  return e === "start" ? Math.max(
    Math.min(
      n.top - o,
      window.innerHeight - i.realHeight - s.width
    ),
    s.width
  ) : e === "end" ? Math.max(
    Math.min(
      n.top - i?.realHeight + n.height + o,
      window.innerHeight - i?.realHeight - s.width
    ),
    s.width
  ) : e === "center" ? Math.max(
    Math.min(
      n.top + n.height / 2 - i?.realHeight / 2,
      window.innerHeight - i?.realHeight - s.width
    ),
    s.width
  ) : 0;
}
function G(e, t) {
  const { elementDimensions: n, popoverDimensions: i, popoverPadding: o, popoverArrowDimensions: s } = t;
  return e === "start" ? Math.max(
    Math.min(
      n.left - o,
      window.innerWidth - i.realWidth - s.width
    ),
    s.width
  ) : e === "end" ? Math.max(
    Math.min(
      n.left - i?.realWidth + n.width + o,
      window.innerWidth - i?.realWidth - s.width
    ),
    s.width
  ) : e === "center" ? Math.max(
    Math.min(
      n.left + n.width / 2 - i?.realWidth / 2,
      window.innerWidth - i?.realWidth - s.width
    ),
    s.width
  ) : 0;
}
function le(e, t) {
  const n = a("popover");
  if (!n)
    return;
  const { align: i = "start", side: o = "left" } = t?.popover || {}, s = i, v = e.id === "driver-dummy-element" ? "over" : o, g = r("stagePadding") || 0, d = se(), m = n.arrow.getBoundingClientRect(), h = e.getBoundingClientRect(), x = h.top - d.height;
  let l = x >= 0;
  const p = window.innerHeight - (h.bottom + d.height);
  let u = p >= 0;
  const f = h.left - d.width;
  let c = f >= 0;
  const w = window.innerWidth - (h.right + d.width);
  let b = w >= 0;
  const C = !l && !u && !c && !b;
  let S = v;
  if (v === "top" && l ? b = c = u = !1 : v === "bottom" && u ? b = c = l = !1 : v === "left" && c ? b = l = u = !1 : v === "right" && b && (c = l = u = !1), v === "over") {
    const _ = window.innerWidth / 2 - d.realWidth / 2, y = window.innerHeight / 2 - d.realHeight / 2;
    n.wrapper.style.left = `${_}px`, n.wrapper.style.right = "auto", n.wrapper.style.top = `${y}px`, n.wrapper.style.bottom = "auto";
  } else if (C) {
    const _ = window.innerWidth / 2 - d?.realWidth / 2, y = 10;
    n.wrapper.style.left = `${_}px`, n.wrapper.style.right = "auto", n.wrapper.style.bottom = `${y}px`, n.wrapper.style.top = "auto";
  } else if (c) {
    const _ = Math.min(
      f,
      window.innerWidth - d?.realWidth - m.width
    ), y = X(s, {
      elementDimensions: h,
      popoverDimensions: d,
      popoverPadding: g,
      popoverArrowDimensions: m
    });
    n.wrapper.style.left = `${_}px`, n.wrapper.style.top = `${y}px`, n.wrapper.style.bottom = "auto", n.wrapper.style.right = "auto", S = "left";
  } else if (b) {
    const _ = Math.min(
      w,
      window.innerWidth - d?.realWidth - m.width
    ), y = X(s, {
      elementDimensions: h,
      popoverDimensions: d,
      popoverPadding: g,
      popoverArrowDimensions: m
    });
    n.wrapper.style.right = `${_}px`, n.wrapper.style.top = `${y}px`, n.wrapper.style.bottom = "auto", n.wrapper.style.left = "auto", S = "right";
  } else if (l) {
    const _ = Math.min(
      x,
      window.innerHeight - d.realHeight - m.width
    );
    let y = G(s, {
      elementDimensions: h,
      popoverDimensions: d,
      popoverPadding: g,
      popoverArrowDimensions: m
    });
    n.wrapper.style.top = `${_}px`, n.wrapper.style.left = `${y}px`, n.wrapper.style.bottom = "auto", n.wrapper.style.right = "auto", S = "top";
  } else if (u) {
    const _ = Math.min(
      p,
      window.innerHeight - d?.realHeight - m.width
    );
    let y = G(s, {
      elementDimensions: h,
      popoverDimensions: d,
      popoverPadding: g,
      popoverArrowDimensions: m
    });
    n.wrapper.style.left = `${y}px`, n.wrapper.style.bottom = `${_}px`, n.wrapper.style.top = "auto", n.wrapper.style.right = "auto", S = "bottom";
  }
  C ? n.arrow.classList.add("driver-popover-arrow-none") : $e(s, S, e);
}
function $e(e, t, n) {
  const i = a("popover");
  if (!i)
    return;
  const o = n.getBoundingClientRect(), s = se(), v = i.arrow, g = s.width, d = window.innerWidth, m = o.width, h = o.left, x = s.height, l = window.innerHeight, p = o.top, u = o.height;
  v.className = "driver-popover-arrow";
  let f = t, c = e;
  if (t === "top" ? (h + m <= 0 ? (f = "right", c = "end") : h + m - g <= 0 && (f = "top", c = "start"), h >= d ? (f = "left", c = "end") : h + g >= d && (f = "top", c = "end")) : t === "bottom" ? (h + m <= 0 ? (f = "right", c = "start") : h + m - g <= 0 && (f = "bottom", c = "start"), h >= d ? (f = "left", c = "start") : h + g >= d && (f = "bottom", c = "end")) : t === "left" ? (p + u <= 0 ? (f = "bottom", c = "end") : p + u - x <= 0 && (f = "left", c = "start"), p >= l ? (f = "top", c = "end") : p + x >= l && (f = "left", c = "end")) : t === "right" && (p + u <= 0 ? (f = "bottom", c = "start") : p + u - x <= 0 && (f = "right", c = "start"), p >= l ? (f = "top", c = "start") : p + x >= l && (f = "right", c = "end")), !f)
    v.classList.add("driver-popover-arrow-none");
  else {
    v.classList.add(`driver-popover-arrow-side-${f}`), v.classList.add(`driver-popover-arrow-align-${c}`);
    const w = n.getBoundingClientRect(), b = v.getBoundingClientRect(), C = r("stagePadding") || 0, S = w.left - C < window.innerWidth && w.right + C > 0 && w.top - C < window.innerHeight && w.bottom + C > 0;
    t === "bottom" && S && (b.x > w.x && b.x + b.width < w.x + w.width ? i.wrapper.style.transform = "translateY(0)" : (v.classList.remove(`driver-popover-arrow-align-${c}`), v.classList.add("driver-popover-arrow-none"), i.wrapper.style.transform = `translateY(-${C / 2}px)`));
  }
}
function Ae() {
  const e = document.createElement("div");
  e.classList.add("driver-popover");
  const t = document.createElement("div");
  t.classList.add("driver-popover-arrow");
  const n = document.createElement("header");
  n.id = "driver-popover-title", n.classList.add("driver-popover-title"), n.style.display = "none", n.innerText = "Popover Title";
  const i = document.createElement("div");
  i.id = "driver-popover-description", i.classList.add("driver-popover-description"), i.style.display = "none", i.innerText = "Popover description is here";
  const o = document.createElement("button");
  o.type = "button", o.classList.add("driver-popover-close-btn"), o.setAttribute("aria-label", "Close"), o.innerHTML = "&times;";
  const s = document.createElement("footer");
  s.classList.add("driver-popover-footer");
  const v = document.createElement("span");
  v.classList.add("driver-popover-progress-text"), v.innerText = "";
  const g = document.createElement("span");
  g.classList.add("driver-popover-navigation-btns");
  const d = document.createElement("button");
  d.type = "button", d.classList.add("driver-popover-prev-btn"), d.innerHTML = "&larr; Previous";
  const m = document.createElement("button");
  return m.type = "button", m.classList.add("driver-popover-next-btn"), m.innerHTML = "Next &rarr;", g.appendChild(d), g.appendChild(m), s.appendChild(v), s.appendChild(g), e.appendChild(o), e.appendChild(t), e.appendChild(n), e.appendChild(i), e.appendChild(s), {
    wrapper: e,
    arrow: t,
    title: n,
    description: i,
    footer: s,
    previousButton: d,
    nextButton: m,
    closeButton: o,
    footerButtons: g,
    progress: v
  };
}
function He() {
  var e;
  const t = a("popover");
  t && ((e = t.wrapper.parentElement) == null || e.removeChild(t.wrapper));
}
function Te(e = {}) {
  F(e);
  function t() {
    r("allowClose") && h();
  }
  function n() {
    const l = r("overlayClickBehavior");
    if (r("allowClose") && l === "close") {
      h();
      return;
    }
    if (typeof l == "function") {
      const p = a("__activeStep"), u = a("__activeElement");
      l(u, p, {
        config: r(),
        state: a(),
        driver: E()
      });
      return;
    }
    l === "nextStep" && i();
  }
  function i() {
    const l = a("activeIndex"), p = r("steps") || [];
    if (typeof l > "u")
      return;
    const u = l + 1;
    p[u] ? m(u) : h();
  }
  function o() {
    const l = a("activeIndex"), p = r("steps") || [];
    if (typeof l > "u")
      return;
    const u = l - 1;
    p[u] ? m(u) : h();
  }
  function s(l) {
    (r("steps") || [])[l] ? m(l) : h();
  }
  function v() {
    var l;
    if (a("__transitionCallback"))
      return;
    const p = a("activeIndex"), u = a("__activeStep"), f = a("__activeElement");
    if (typeof p > "u" || typeof u > "u" || typeof a("activeIndex") > "u")
      return;
    const c = ((l = u.popover) == null ? void 0 : l.onPrevClick) || r("onPrevClick");
    if (c)
      return c(f, u, {
        config: r(),
        state: a(),
        driver: E()
      });
    o();
  }
  function g() {
    var l;
    if (a("__transitionCallback"))
      return;
    const p = a("activeIndex"), u = a("__activeStep"), f = a("__activeElement");
    if (typeof p > "u" || typeof u > "u")
      return;
    const c = ((l = u.popover) == null ? void 0 : l.onNextClick) || r("onNextClick");
    if (c)
      return c(f, u, {
        config: r(),
        state: a(),
        driver: E()
      });
    i();
  }
  function d() {
    a("isInitialized") || (k("isInitialized", !0), document.body.classList.add("driver-active", r("animate") ? "driver-fade" : "driver-simple"), Ee(), R("overlayClick", n), R("escapePress", t), R("arrowLeftPress", v), R("arrowRightPress", g));
  }
  function m(l = 0) {
    var p, u, f, c, w, b, C, S;
    const _ = r("steps");
    if (!_) {
      console.error("No steps to drive through"), h();
      return;
    }
    if (!_[l]) {
      h();
      return;
    }
    k("__activeOnDestroyed", document.activeElement), k("activeIndex", l);
    const y = _[l], P = _[l + 1], D = _[l - 1], M = ((p = y.popover) == null ? void 0 : p.doneBtnText) || r("doneBtnText") || "Done", I = r("allowClose"), H = typeof ((u = y.popover) == null ? void 0 : u.showProgress) < "u" ? (f = y.popover) == null ? void 0 : f.showProgress : r("showProgress"), W = (((c = y.popover) == null ? void 0 : c.progressText) || r("progressText") || "{{current}} of {{total}}").replace("{{current}}", `${l + 1}`).replace("{{total}}", `${_.length}`), A = ((w = y.popover) == null ? void 0 : w.showButtons) || r("showButtons"), N = [
      "next",
      "previous",
      ...I ? ["close"] : []
    ].filter((ce) => !(A != null && A.length) || A.includes(ce)), de = ((b = y.popover) == null ? void 0 : b.onNextClick) || r("onNextClick"), ae = ((C = y.popover) == null ? void 0 : C.onPrevClick) || r("onPrevClick"), pe = ((S = y.popover) == null ? void 0 : S.onCloseClick) || r("onCloseClick");
    Z({
      ...y,
      popover: {
        showButtons: N,
        nextBtnText: P ? void 0 : M,
        disableButtons: [...D ? [] : ["previous"]],
        showProgress: H,
        progressText: W,
        onNextClick: de || (() => {
          P ? m(l + 1) : h();
        }),
        onPrevClick: ae || (() => {
          m(l - 1);
        }),
        onCloseClick: pe || (() => {
          h();
        }),
        ...y?.popover || {}
      }
    });
  }
  function h(l = !0) {
    const p = a("__activeElement"), u = a("__activeStep"), f = a("__activeOnDestroyed"), c = r("onDestroyStarted");
    if (l && c) {
      const C = !p || p?.id === "driver-dummy-element";
      c(C ? void 0 : p, u, {
        config: r(),
        state: a(),
        driver: E()
      });
      return;
    }
    const w = u?.onDeselected || r("onDeselected"), b = r("onDestroyed");
    if (document.body.classList.remove("driver-active", "driver-fade", "driver-simple"), Pe(), He(), Le(), be(), ue(), K(), p && u) {
      const C = p.id === "driver-dummy-element";
      w && w(C ? void 0 : p, u, {
        config: r(),
        state: a(),
        driver: E()
      }), b && b(C ? void 0 : p, u, {
        config: r(),
        state: a(),
        driver: E()
      });
    }
    f && f.focus();
  }
  const x = {
    isActive: () => a("isInitialized") || !1,
    refresh: T,
    drive: (l = 0) => {
      d(), m(l);
    },
    setConfig: F,
    setSteps: (l) => {
      K(), F({
        ...r(),
        steps: l
      });
    },
    getConfig: r,
    getState: a,
    getActiveIndex: () => a("activeIndex"),
    isFirstStep: () => a("activeIndex") === 0,
    isLastStep: () => {
      const l = r("steps") || [], p = a("activeIndex");
      return p !== void 0 && p === l.length - 1;
    },
    getActiveStep: () => a("activeStep"),
    getActiveElement: () => a("activeElement"),
    getPreviousElement: () => a("previousElement"),
    getPreviousStep: () => a("previousStep"),
    moveNext: i,
    movePrevious: o,
    moveTo: s,
    hasNextStep: () => {
      const l = r("steps") || [], p = a("activeIndex");
      return p !== void 0 && !!l[p + 1];
    },
    hasPreviousStep: () => {
      const l = r("steps") || [], p = a("activeIndex");
      return p !== void 0 && !!l[p - 1];
    },
    highlight: (l) => {
      d(), Z({
        ...l,
        popover: l.popover ? {
          showButtons: [],
          showProgress: !1,
          progressText: "",
          ...l.popover
        } : void 0
      });
    },
    destroy: () => {
      h(!1);
    }
  };
  return ve(x), x;
}
const Q = "streamlitTourStyle";
function De(e) {
  try {
    return localStorage.getItem(e) === "1";
  } catch {
    return !1;
  }
}
function Me(e) {
  try {
    localStorage.setItem(e, "1");
  } catch {
  }
}
function Ie() {
  if (document.getElementById(Q)) return;
  const e = document.createElement("style");
  e.id = Q, e.textContent = `
    [data-testid="stSidebarContainer"],
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
      z-index: 1 !important;
    }
    header[data-testid="stHeader"] {
      z-index: 1 !important;
    }
    .driver-overlay {
      z-index: 999999 !important;
    }
    .driver-popover {
      z-index: 1000000 !important;
    }
    .driver-active-element,
    [data-testid="stSidebar"].driver-active-element {
      z-index: 1000000 !important;
    }
  `, document.head.appendChild(e);
}
let L = null, B = 0, j = !1;
const We = ({
  data: e,
  setStateValue: t
}) => {
  if (Ie(), L?.isActive())
    return console.log("[tour] already active, bailing"), () => {
    };
  L && (L.destroy(), L = null);
  const {
    steps: n = [],
    showProgress: i = !0,
    animate: o = !0,
    overlayOpacity: s = 0.75,
    oneTimeTour: v = !1,
    key: g = "driverjs",
    tourStorageKey: d = "streamlitTour",
    reset: m = !1
  } = e;
  return m ? (localStorage.removeItem(d), () => {
  }) : v && De(d) ? (t("skipped", !0), () => {
  }) : n.length === 0 ? (console.warn("[streamlit-driverjs] No steps provided."), t("skipped", !0), () => {
  }) : (B = 0, j = n.length <= 1, L = Te({
    showProgress: i,
    animate: o,
    overlayOpacity: s,
    steps: n,
    // Can be used to rerun the tour at the same step after a refresh/page switch
    onHighlightStarted: () => {
      localStorage.setItem("currentStep", String(B));
    },
    onNextClick: () => {
      B += 1, B >= n.length - 1 && (j = !0), t("currentStep", B), L?.moveNext();
    },
    onPrevClick: () => {
      B -= 1, t("currentStep", B), L?.movePrevious();
    },
    onDestroyStarted: () => {
      const x = j || (L?.isLastStep() ?? !1);
      v && x && Me(d), t("currentStep", B), t("dismissed", !x), t("finished", x), t("skipped", !1), L?.destroy(), L = null;
    }
  }), L.drive(), () => {
    L && !L.isActive() && (L.destroy(), L = null);
  });
};
export {
  We as default
};
//# sourceMappingURL=index-bRJkqUb4.js.map
