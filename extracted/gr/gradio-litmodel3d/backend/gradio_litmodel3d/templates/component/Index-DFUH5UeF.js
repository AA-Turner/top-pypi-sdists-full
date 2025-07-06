const {
  SvelteComponent: Bi,
  assign: Oi,
  create_slot: Ti,
  detach: Wi,
  element: Pi,
  get_all_dirty_from_scope: Zi,
  get_slot_changes: Gi,
  get_spread_update: Hi,
  init: Xi,
  insert: Yi,
  safe_not_equal: Ki,
  set_dynamic_element_data: Gn,
  set_style: te,
  toggle_class: ye,
  transition_in: Wl,
  transition_out: Pl,
  update_slot_base: Ji
} = window.__gradio__svelte__internal;
function Qi(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), a = Ti(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let o = 0; o < s.length; o += 1)
    r = Oi(r, s[o]);
  return {
    c() {
      e = Pi(
        /*tag*/
        l[14]
      ), a && a.c(), Gn(
        /*tag*/
        l[14]
      )(e, r), ye(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), ye(
        e,
        "padded",
        /*padding*/
        l[6]
      ), ye(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), ye(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), ye(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), te(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), te(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), te(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), te(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), te(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), te(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), te(e, "border-width", "var(--block-border-width)");
    },
    m(o, f) {
      Yi(o, e, f), a && a.m(e, null), n = !0;
    },
    p(o, f) {
      a && a.p && (!n || f & /*$$scope*/
      131072) && Ji(
        a,
        i,
        o,
        /*$$scope*/
        o[17],
        n ? Gi(
          i,
          /*$$scope*/
          o[17],
          f,
          null
        ) : Zi(
          /*$$scope*/
          o[17]
        ),
        null
      ), Gn(
        /*tag*/
        o[14]
      )(e, r = Hi(s, [
        (!n || f & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!n || f & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!n || f & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), ye(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), ye(
        e,
        "padded",
        /*padding*/
        o[6]
      ), ye(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), ye(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), ye(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), f & /*height*/
      1 && te(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), f & /*width*/
      2 && te(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), f & /*variant*/
      16 && te(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), f & /*allow_overflow*/
      2048 && te(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), f & /*scale*/
      4096 && te(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), f & /*min_width*/
      8192 && te(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      n || (Wl(a, o), n = !0);
    },
    o(o) {
      Pl(a, o), n = !1;
    },
    d(o) {
      o && Wi(e), a && a.d(o);
    }
  };
}
function xi(l) {
  let e, t = (
    /*tag*/
    l[14] && Qi(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Wl(t, n), e = !0);
    },
    o(n) {
      Pl(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function $i(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: a = void 0 } = e, { width: s = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: o = [] } = e, { variant: f = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: d = "normal" } = e, { test_id: c = void 0 } = e, { explicit_call: m = !1 } = e, { container: h = !0 } = e, { visible: p = !0 } = e, { allow_overflow: y = !0 } = e, { scale: b = null } = e, { min_width: g = 0 } = e, q = d === "fieldset" ? "fieldset" : "div";
  const I = (v) => {
    if (v !== void 0) {
      if (typeof v == "number")
        return v + "px";
      if (typeof v == "string")
        return v;
    }
  };
  return l.$$set = (v) => {
    "height" in v && t(0, a = v.height), "width" in v && t(1, s = v.width), "elem_id" in v && t(2, r = v.elem_id), "elem_classes" in v && t(3, o = v.elem_classes), "variant" in v && t(4, f = v.variant), "border_mode" in v && t(5, _ = v.border_mode), "padding" in v && t(6, u = v.padding), "type" in v && t(16, d = v.type), "test_id" in v && t(7, c = v.test_id), "explicit_call" in v && t(8, m = v.explicit_call), "container" in v && t(9, h = v.container), "visible" in v && t(10, p = v.visible), "allow_overflow" in v && t(11, y = v.allow_overflow), "scale" in v && t(12, b = v.scale), "min_width" in v && t(13, g = v.min_width), "$$scope" in v && t(17, i = v.$$scope);
  }, [
    a,
    s,
    r,
    o,
    f,
    _,
    u,
    c,
    m,
    h,
    p,
    y,
    b,
    g,
    q,
    I,
    d,
    i,
    n
  ];
}
class Zl extends Bi {
  constructor(e) {
    super(), Xi(this, e, $i, xi, Ki, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: eo,
  append: ln,
  attr: Ft,
  create_component: to,
  destroy_component: no,
  detach: lo,
  element: Hn,
  init: io,
  insert: oo,
  mount_component: so,
  safe_not_equal: ao,
  set_data: ro,
  space: fo,
  text: _o,
  toggle_class: Ne,
  transition_in: uo,
  transition_out: co
} = window.__gradio__svelte__internal;
function mo(l) {
  let e, t, n, i, a, s;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = Hn("label"), t = Hn("span"), to(n.$$.fragment), i = fo(), a = _o(
        /*label*/
        l[0]
      ), Ft(t, "class", "svelte-9gxdi0"), Ft(e, "for", ""), Ft(e, "data-testid", "block-label"), Ft(e, "class", "svelte-9gxdi0"), Ne(e, "hide", !/*show_label*/
      l[2]), Ne(e, "sr-only", !/*show_label*/
      l[2]), Ne(
        e,
        "float",
        /*float*/
        l[4]
      ), Ne(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(r, o) {
      oo(r, e, o), ln(e, t), so(n, t, null), ln(e, i), ln(e, a), s = !0;
    },
    p(r, [o]) {
      (!s || o & /*label*/
      1) && ro(
        a,
        /*label*/
        r[0]
      ), (!s || o & /*show_label*/
      4) && Ne(e, "hide", !/*show_label*/
      r[2]), (!s || o & /*show_label*/
      4) && Ne(e, "sr-only", !/*show_label*/
      r[2]), (!s || o & /*float*/
      16) && Ne(
        e,
        "float",
        /*float*/
        r[4]
      ), (!s || o & /*disable*/
      8) && Ne(
        e,
        "hide-label",
        /*disable*/
        r[3]
      );
    },
    i(r) {
      s || (uo(n.$$.fragment, r), s = !0);
    },
    o(r) {
      co(n.$$.fragment, r), s = !1;
    },
    d(r) {
      r && lo(e), no(n);
    }
  };
}
function ho(l, e, t) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: a = !0 } = e, { disable: s = !1 } = e, { float: r = !0 } = e;
  return l.$$set = (o) => {
    "label" in o && t(0, n = o.label), "Icon" in o && t(1, i = o.Icon), "show_label" in o && t(2, a = o.show_label), "disable" in o && t(3, s = o.disable), "float" in o && t(4, r = o.float);
  }, [n, i, a, s, r];
}
class An extends eo {
  constructor(e) {
    super(), io(this, e, ho, mo, ao, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: go,
  append: Cn,
  attr: je,
  bubble: bo,
  create_component: po,
  destroy_component: wo,
  detach: Gl,
  element: qn,
  init: vo,
  insert: Hl,
  listen: ko,
  mount_component: yo,
  safe_not_equal: zo,
  set_data: Co,
  set_style: st,
  space: qo,
  text: So,
  toggle_class: J,
  transition_in: Lo,
  transition_out: Do
} = window.__gradio__svelte__internal;
function Xn(l) {
  let e, t;
  return {
    c() {
      e = qn("span"), t = So(
        /*label*/
        l[1]
      ), je(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Hl(n, e, i), Cn(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Co(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && Gl(e);
    }
  };
}
function Eo(l) {
  let e, t, n, i, a, s, r, o = (
    /*show_label*/
    l[2] && Xn(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = qn("button"), o && o.c(), t = qo(), n = qn("div"), po(i.$$.fragment), je(n, "class", "svelte-1lrphxw"), J(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), J(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), J(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], je(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), je(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), je(
        e,
        "title",
        /*label*/
        l[1]
      ), je(e, "class", "svelte-1lrphxw"), J(
        e,
        "pending",
        /*pending*/
        l[3]
      ), J(
        e,
        "padded",
        /*padded*/
        l[5]
      ), J(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), J(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), st(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), st(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), st(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(f, _) {
      Hl(f, e, _), o && o.m(e, null), Cn(e, t), Cn(e, n), yo(i, n, null), a = !0, s || (r = ko(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), s = !0);
    },
    p(f, [_]) {
      /*show_label*/
      f[2] ? o ? o.p(f, _) : (o = Xn(f), o.c(), o.m(e, t)) : o && (o.d(1), o = null), (!a || _ & /*size*/
      16) && J(
        n,
        "small",
        /*size*/
        f[4] === "small"
      ), (!a || _ & /*size*/
      16) && J(
        n,
        "large",
        /*size*/
        f[4] === "large"
      ), (!a || _ & /*size*/
      16) && J(
        n,
        "medium",
        /*size*/
        f[4] === "medium"
      ), (!a || _ & /*disabled*/
      128) && (e.disabled = /*disabled*/
      f[7]), (!a || _ & /*label*/
      2) && je(
        e,
        "aria-label",
        /*label*/
        f[1]
      ), (!a || _ & /*hasPopup*/
      256) && je(
        e,
        "aria-haspopup",
        /*hasPopup*/
        f[8]
      ), (!a || _ & /*label*/
      2) && je(
        e,
        "title",
        /*label*/
        f[1]
      ), (!a || _ & /*pending*/
      8) && J(
        e,
        "pending",
        /*pending*/
        f[3]
      ), (!a || _ & /*padded*/
      32) && J(
        e,
        "padded",
        /*padded*/
        f[5]
      ), (!a || _ & /*highlight*/
      64) && J(
        e,
        "highlight",
        /*highlight*/
        f[6]
      ), (!a || _ & /*transparent*/
      512) && J(
        e,
        "transparent",
        /*transparent*/
        f[9]
      ), _ & /*disabled, _color*/
      4224 && st(e, "color", !/*disabled*/
      f[7] && /*_color*/
      f[12] ? (
        /*_color*/
        f[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && st(e, "--bg-color", /*disabled*/
      f[7] ? "auto" : (
        /*background*/
        f[10]
      )), _ & /*offset*/
      2048 && st(
        e,
        "margin-left",
        /*offset*/
        f[11] + "px"
      );
    },
    i(f) {
      a || (Lo(i.$$.fragment, f), a = !0);
    },
    o(f) {
      Do(i.$$.fragment, f), a = !1;
    },
    d(f) {
      f && Gl(e), o && o.d(), wo(i), s = !1, r();
    }
  };
}
function Fo(l, e, t) {
  let n, { Icon: i } = e, { label: a = "" } = e, { show_label: s = !1 } = e, { pending: r = !1 } = e, { size: o = "small" } = e, { padded: f = !0 } = e, { highlight: _ = !1 } = e, { disabled: u = !1 } = e, { hasPopup: d = !1 } = e, { color: c = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: h = "var(--background-fill-primary)" } = e, { offset: p = 0 } = e;
  function y(b) {
    bo.call(this, l, b);
  }
  return l.$$set = (b) => {
    "Icon" in b && t(0, i = b.Icon), "label" in b && t(1, a = b.label), "show_label" in b && t(2, s = b.show_label), "pending" in b && t(3, r = b.pending), "size" in b && t(4, o = b.size), "padded" in b && t(5, f = b.padded), "highlight" in b && t(6, _ = b.highlight), "disabled" in b && t(7, u = b.disabled), "hasPopup" in b && t(8, d = b.hasPopup), "color" in b && t(13, c = b.color), "transparent" in b && t(9, m = b.transparent), "background" in b && t(10, h = b.background), "offset" in b && t(11, p = b.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = _ ? "var(--color-accent)" : c);
  }, [
    i,
    a,
    s,
    r,
    o,
    f,
    _,
    u,
    d,
    m,
    h,
    p,
    n,
    c,
    y
  ];
}
class it extends go {
  constructor(e) {
    super(), vo(this, e, Fo, Eo, zo, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: Mo,
  append: jo,
  attr: on,
  binding_callbacks: Io,
  create_slot: No,
  detach: Uo,
  element: Yn,
  get_all_dirty_from_scope: Vo,
  get_slot_changes: Ao,
  init: Ro,
  insert: Bo,
  safe_not_equal: Oo,
  toggle_class: Ue,
  transition_in: To,
  transition_out: Wo,
  update_slot_base: Po
} = window.__gradio__svelte__internal;
function Zo(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[5].default
  ), a = No(
    i,
    l,
    /*$$scope*/
    l[4],
    null
  );
  return {
    c() {
      e = Yn("div"), t = Yn("div"), a && a.c(), on(t, "class", "icon svelte-3w3rth"), on(e, "class", "empty svelte-3w3rth"), on(e, "aria-label", "Empty value"), Ue(
        e,
        "small",
        /*size*/
        l[0] === "small"
      ), Ue(
        e,
        "large",
        /*size*/
        l[0] === "large"
      ), Ue(
        e,
        "unpadded_box",
        /*unpadded_box*/
        l[1]
      ), Ue(
        e,
        "small_parent",
        /*parent_height*/
        l[3]
      );
    },
    m(s, r) {
      Bo(s, e, r), jo(e, t), a && a.m(t, null), l[6](e), n = !0;
    },
    p(s, [r]) {
      a && a.p && (!n || r & /*$$scope*/
      16) && Po(
        a,
        i,
        s,
        /*$$scope*/
        s[4],
        n ? Ao(
          i,
          /*$$scope*/
          s[4],
          r,
          null
        ) : Vo(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!n || r & /*size*/
      1) && Ue(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!n || r & /*size*/
      1) && Ue(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!n || r & /*unpadded_box*/
      2) && Ue(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!n || r & /*parent_height*/
      8) && Ue(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      n || (To(a, s), n = !0);
    },
    o(s) {
      Wo(a, s), n = !1;
    },
    d(s) {
      s && Uo(e), a && a.d(s), l[6](null);
    }
  };
}
function Go(l, e, t) {
  let n, { $$slots: i = {}, $$scope: a } = e, { size: s = "small" } = e, { unpadded_box: r = !1 } = e, o;
  function f(u) {
    var d;
    if (!u)
      return !1;
    const { height: c } = u.getBoundingClientRect(), { height: m } = ((d = u.parentElement) === null || d === void 0 ? void 0 : d.getBoundingClientRect()) || { height: c };
    return c > m + 2;
  }
  function _(u) {
    Io[u ? "unshift" : "push"](() => {
      o = u, t(2, o);
    });
  }
  return l.$$set = (u) => {
    "size" in u && t(0, s = u.size), "unpadded_box" in u && t(1, r = u.unpadded_box), "$$scope" in u && t(4, a = u.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*el*/
    4 && t(3, n = f(o));
  }, [s, r, o, n, a, i, _];
}
class Ho extends Mo {
  constructor(e) {
    super(), Ro(this, e, Go, Zo, Oo, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: Xo,
  append: sn,
  attr: he,
  detach: Yo,
  init: Ko,
  insert: Jo,
  noop: an,
  safe_not_equal: Qo,
  set_style: ze,
  svg_element: Mt
} = window.__gradio__svelte__internal;
function xo(l) {
  let e, t, n, i;
  return {
    c() {
      e = Mt("svg"), t = Mt("g"), n = Mt("path"), i = Mt("path"), he(n, "d", "M18,6L6.087,17.913"), ze(n, "fill", "none"), ze(n, "fill-rule", "nonzero"), ze(n, "stroke-width", "2px"), he(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), he(i, "d", "M4.364,4.364L19.636,19.636"), ze(i, "fill", "none"), ze(i, "fill-rule", "nonzero"), ze(i, "stroke-width", "2px"), he(e, "width", "100%"), he(e, "height", "100%"), he(e, "viewBox", "0 0 24 24"), he(e, "version", "1.1"), he(e, "xmlns", "http://www.w3.org/2000/svg"), he(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), he(e, "xml:space", "preserve"), he(e, "stroke", "currentColor"), ze(e, "fill-rule", "evenodd"), ze(e, "clip-rule", "evenodd"), ze(e, "stroke-linecap", "round"), ze(e, "stroke-linejoin", "round");
    },
    m(a, s) {
      Jo(a, e, s), sn(e, t), sn(t, n), sn(e, i);
    },
    p: an,
    i: an,
    o: an,
    d(a) {
      a && Yo(e);
    }
  };
}
class Xl extends Xo {
  constructor(e) {
    super(), Ko(this, e, null, xo, Qo, {});
  }
}
const {
  SvelteComponent: $o,
  append: es,
  attr: at,
  detach: ts,
  init: ns,
  insert: ls,
  noop: rn,
  safe_not_equal: is,
  svg_element: Kn
} = window.__gradio__svelte__internal;
function os(l) {
  let e, t;
  return {
    c() {
      e = Kn("svg"), t = Kn("path"), at(t, "fill", "currentColor"), at(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), at(e, "xmlns", "http://www.w3.org/2000/svg"), at(e, "width", "100%"), at(e, "height", "100%"), at(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      ls(n, e, i), es(e, t);
    },
    p: rn,
    i: rn,
    o: rn,
    d(n) {
      n && ts(e);
    }
  };
}
class Yl extends $o {
  constructor(e) {
    super(), ns(this, e, null, os, is, {});
  }
}
const {
  SvelteComponent: ss,
  append: as,
  attr: ge,
  detach: rs,
  init: fs,
  insert: _s,
  noop: fn,
  safe_not_equal: us,
  svg_element: Jn
} = window.__gradio__svelte__internal;
function cs(l) {
  let e, t;
  return {
    c() {
      e = Jn("svg"), t = Jn("path"), ge(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), ge(e, "xmlns", "http://www.w3.org/2000/svg"), ge(e, "width", "100%"), ge(e, "height", "100%"), ge(e, "viewBox", "0 0 24 24"), ge(e, "fill", "none"), ge(e, "stroke", "currentColor"), ge(e, "stroke-width", "1.5"), ge(e, "stroke-linecap", "round"), ge(e, "stroke-linejoin", "round"), ge(e, "class", "feather feather-edit-2");
    },
    m(n, i) {
      _s(n, e, i), as(e, t);
    },
    p: fn,
    i: fn,
    o: fn,
    d(n) {
      n && rs(e);
    }
  };
}
class ds extends ss {
  constructor(e) {
    super(), fs(this, e, null, cs, us, {});
  }
}
const {
  SvelteComponent: ms,
  append: Qn,
  attr: se,
  detach: hs,
  init: gs,
  insert: bs,
  noop: _n,
  safe_not_equal: ps,
  svg_element: un
} = window.__gradio__svelte__internal;
function ws(l) {
  let e, t, n;
  return {
    c() {
      e = un("svg"), t = un("path"), n = un("polyline"), se(t, "d", "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"), se(n, "points", "13 2 13 9 20 9"), se(e, "xmlns", "http://www.w3.org/2000/svg"), se(e, "width", "100%"), se(e, "height", "100%"), se(e, "viewBox", "0 0 24 24"), se(e, "fill", "none"), se(e, "stroke", "currentColor"), se(e, "stroke-width", "1.5"), se(e, "stroke-linecap", "round"), se(e, "stroke-linejoin", "round"), se(e, "class", "feather feather-file");
    },
    m(i, a) {
      bs(i, e, a), Qn(e, t), Qn(e, n);
    },
    p: _n,
    i: _n,
    o: _n,
    d(i) {
      i && hs(e);
    }
  };
}
let Kt = class extends ms {
  constructor(e) {
    super(), gs(this, e, null, ws, ps, {});
  }
};
const {
  SvelteComponent: vs,
  append: ks,
  attr: jt,
  detach: ys,
  init: zs,
  insert: Cs,
  noop: cn,
  safe_not_equal: qs,
  svg_element: xn
} = window.__gradio__svelte__internal;
function Ss(l) {
  let e, t;
  return {
    c() {
      e = xn("svg"), t = xn("path"), jt(t, "fill", "currentColor"), jt(t, "d", "M13.75 2a2.25 2.25 0 0 1 2.236 2.002V4h1.764A2.25 2.25 0 0 1 20 6.25V11h-1.5V6.25a.75.75 0 0 0-.75-.75h-2.129c-.404.603-1.091 1-1.871 1h-3.5c-.78 0-1.467-.397-1.871-1H6.25a.75.75 0 0 0-.75.75v13.5c0 .414.336.75.75.75h4.78a4 4 0 0 0 .505 1.5H6.25A2.25 2.25 0 0 1 4 19.75V6.25A2.25 2.25 0 0 1 6.25 4h1.764a2.25 2.25 0 0 1 2.236-2zm2.245 2.096L16 4.25q0-.078-.005-.154M13.75 3.5h-3.5a.75.75 0 0 0 0 1.5h3.5a.75.75 0 0 0 0-1.5M15 12a3 3 0 0 0-3 3v5c0 .556.151 1.077.415 1.524l3.494-3.494a2.25 2.25 0 0 1 3.182 0l3.494 3.494c.264-.447.415-.968.415-1.524v-5a3 3 0 0 0-3-3zm0 11a3 3 0 0 1-1.524-.415l3.494-3.494a.75.75 0 0 1 1.06 0l3.494 3.494A3 3 0 0 1 20 23zm5-7a1 1 0 1 1 0-2 1 1 0 0 1 0 2"), jt(e, "xmlns", "http://www.w3.org/2000/svg"), jt(e, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      Cs(n, e, i), ks(e, t);
    },
    p: cn,
    i: cn,
    o: cn,
    d(n) {
      n && ys(e);
    }
  };
}
class Ls extends vs {
  constructor(e) {
    super(), zs(this, e, null, Ss, qs, {});
  }
}
const {
  SvelteComponent: Ds,
  append: $n,
  attr: ae,
  detach: Es,
  init: Fs,
  insert: Ms,
  noop: dn,
  safe_not_equal: js,
  svg_element: mn
} = window.__gradio__svelte__internal;
function Is(l) {
  let e, t, n;
  return {
    c() {
      e = mn("svg"), t = mn("polyline"), n = mn("path"), ae(t, "points", "1 4 1 10 7 10"), ae(n, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), ae(e, "xmlns", "http://www.w3.org/2000/svg"), ae(e, "width", "100%"), ae(e, "height", "100%"), ae(e, "viewBox", "0 0 24 24"), ae(e, "fill", "none"), ae(e, "stroke", "currentColor"), ae(e, "stroke-width", "2"), ae(e, "stroke-linecap", "round"), ae(e, "stroke-linejoin", "round"), ae(e, "class", "feather feather-rotate-ccw");
    },
    m(i, a) {
      Ms(i, e, a), $n(e, t), $n(e, n);
    },
    p: dn,
    i: dn,
    o: dn,
    d(i) {
      i && Es(e);
    }
  };
}
class Kl extends Ds {
  constructor(e) {
    super(), Fs(this, e, null, Is, js, {});
  }
}
const {
  SvelteComponent: Ns,
  append: hn,
  attr: Z,
  detach: Us,
  init: Vs,
  insert: As,
  noop: gn,
  safe_not_equal: Rs,
  svg_element: It
} = window.__gradio__svelte__internal;
function Bs(l) {
  let e, t, n, i;
  return {
    c() {
      e = It("svg"), t = It("path"), n = It("polyline"), i = It("line"), Z(t, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), Z(n, "points", "17 8 12 3 7 8"), Z(i, "x1", "12"), Z(i, "y1", "3"), Z(i, "x2", "12"), Z(i, "y2", "15"), Z(e, "xmlns", "http://www.w3.org/2000/svg"), Z(e, "width", "90%"), Z(e, "height", "90%"), Z(e, "viewBox", "0 0 24 24"), Z(e, "fill", "none"), Z(e, "stroke", "currentColor"), Z(e, "stroke-width", "2"), Z(e, "stroke-linecap", "round"), Z(e, "stroke-linejoin", "round"), Z(e, "class", "feather feather-upload");
    },
    m(a, s) {
      As(a, e, s), hn(e, t), hn(e, n), hn(e, i);
    },
    p: gn,
    i: gn,
    o: gn,
    d(a) {
      a && Us(e);
    }
  };
}
let Os = class extends Ns {
  constructor(e) {
    super(), Vs(this, e, null, Bs, Rs, {});
  }
};
const Ts = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], el = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Ts.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: el[e][t],
      secondary: el[e][n]
    }
  }),
  {}
);
const {
  SvelteComponent: Ws,
  append: Xe,
  attr: Sn,
  check_outros: Ps,
  create_component: Jl,
  destroy_component: Ql,
  detach: At,
  element: Ln,
  group_outros: Zs,
  init: Gs,
  insert: Rt,
  mount_component: xl,
  safe_not_equal: Hs,
  set_data: Dn,
  space: En,
  text: ht,
  toggle_class: tl,
  transition_in: Ot,
  transition_out: Tt
} = window.__gradio__svelte__internal;
function Xs(l) {
  let e, t;
  return e = new Os({}), {
    c() {
      Jl(e.$$.fragment);
    },
    m(n, i) {
      xl(e, n, i), t = !0;
    },
    i(n) {
      t || (Ot(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Tt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ql(e, n);
    }
  };
}
function Ys(l) {
  let e, t;
  return e = new Ls({}), {
    c() {
      Jl(e.$$.fragment);
    },
    m(n, i) {
      xl(e, n, i), t = !0;
    },
    i(n) {
      t || (Ot(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Tt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ql(e, n);
    }
  };
}
function nl(l) {
  let e, t, n = (
    /*i18n*/
    l[1]("common.or") + ""
  ), i, a, s, r = (
    /*message*/
    (l[2] || /*i18n*/
    l[1]("upload_text.click_to_upload")) + ""
  ), o;
  return {
    c() {
      e = Ln("span"), t = ht("- "), i = ht(n), a = ht(" -"), s = En(), o = ht(r), Sn(e, "class", "or svelte-kzcjhc");
    },
    m(f, _) {
      Rt(f, e, _), Xe(e, t), Xe(e, i), Xe(e, a), Rt(f, s, _), Rt(f, o, _);
    },
    p(f, _) {
      _ & /*i18n*/
      2 && n !== (n = /*i18n*/
      f[1]("common.or") + "") && Dn(i, n), _ & /*message, i18n*/
      6 && r !== (r = /*message*/
      (f[2] || /*i18n*/
      f[1]("upload_text.click_to_upload")) + "") && Dn(o, r);
    },
    d(f) {
      f && (At(e), At(s), At(o));
    }
  };
}
function Ks(l) {
  let e, t, n, i, a, s = (
    /*i18n*/
    l[1](
      /*defs*/
      l[5][
        /*type*/
        l[0]
      ] || /*defs*/
      l[5].file
    ) + ""
  ), r, o, f;
  const _ = [Ys, Xs], u = [];
  function d(m, h) {
    return (
      /*type*/
      m[0] === "clipboard" ? 0 : 1
    );
  }
  n = d(l), i = u[n] = _[n](l);
  let c = (
    /*mode*/
    l[3] !== "short" && nl(l)
  );
  return {
    c() {
      e = Ln("div"), t = Ln("span"), i.c(), a = En(), r = ht(s), o = En(), c && c.c(), Sn(t, "class", "icon-wrap svelte-kzcjhc"), tl(
        t,
        "hovered",
        /*hovered*/
        l[4]
      ), Sn(e, "class", "wrap svelte-kzcjhc");
    },
    m(m, h) {
      Rt(m, e, h), Xe(e, t), u[n].m(t, null), Xe(e, a), Xe(e, r), Xe(e, o), c && c.m(e, null), f = !0;
    },
    p(m, [h]) {
      let p = n;
      n = d(m), n !== p && (Zs(), Tt(u[p], 1, 1, () => {
        u[p] = null;
      }), Ps(), i = u[n], i || (i = u[n] = _[n](m), i.c()), Ot(i, 1), i.m(t, null)), (!f || h & /*hovered*/
      16) && tl(
        t,
        "hovered",
        /*hovered*/
        m[4]
      ), (!f || h & /*i18n, type*/
      3) && s !== (s = /*i18n*/
      m[1](
        /*defs*/
        m[5][
          /*type*/
          m[0]
        ] || /*defs*/
        m[5].file
      ) + "") && Dn(r, s), /*mode*/
      m[3] !== "short" ? c ? c.p(m, h) : (c = nl(m), c.c(), c.m(e, null)) : c && (c.d(1), c = null);
    },
    i(m) {
      f || (Ot(i), f = !0);
    },
    o(m) {
      Tt(i), f = !1;
    },
    d(m) {
      m && At(e), u[n].d(), c && c.d();
    }
  };
}
function Js(l, e, t) {
  let { type: n = "file" } = e, { i18n: i } = e, { message: a = void 0 } = e, { mode: s = "full" } = e, { hovered: r = !1 } = e;
  const o = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv",
    gallery: "upload_text.drop_gallery",
    clipboard: "upload_text.paste_clipboard"
  };
  return l.$$set = (f) => {
    "type" in f && t(0, n = f.type), "i18n" in f && t(1, i = f.i18n), "message" in f && t(2, a = f.message), "mode" in f && t(3, s = f.mode), "hovered" in f && t(4, r = f.hovered);
  }, [n, i, a, s, r, o];
}
class Qs extends Ws {
  constructor(e) {
    super(), Gs(this, e, Js, Ks, Hs, {
      type: 0,
      i18n: 1,
      message: 2,
      mode: 3,
      hovered: 4
    });
  }
}
var ll = Object.prototype.hasOwnProperty;
function il(l, e, t) {
  for (t of l.keys())
    if (bt(t, e))
      return t;
}
function bt(l, e) {
  var t, n, i;
  if (l === e)
    return !0;
  if (l && e && (t = l.constructor) === e.constructor) {
    if (t === Date)
      return l.getTime() === e.getTime();
    if (t === RegExp)
      return l.toString() === e.toString();
    if (t === Array) {
      if ((n = l.length) === e.length)
        for (; n-- && bt(l[n], e[n]); )
          ;
      return n === -1;
    }
    if (t === Set) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n, i && typeof i == "object" && (i = il(e, i), !i) || !e.has(i))
          return !1;
      return !0;
    }
    if (t === Map) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n[0], i && typeof i == "object" && (i = il(e, i), !i) || !bt(n[1], e.get(i)))
          return !1;
      return !0;
    }
    if (t === ArrayBuffer)
      l = new Uint8Array(l), e = new Uint8Array(e);
    else if (t === DataView) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l.getInt8(n) === e.getInt8(n); )
          ;
      return n === -1;
    }
    if (ArrayBuffer.isView(l)) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l[n] === e[n]; )
          ;
      return n === -1;
    }
    if (!t || typeof l == "object") {
      n = 0;
      for (t in l)
        if (ll.call(l, t) && ++n && !ll.call(e, t) || !(t in e) || !bt(l[t], e[t]))
          return !1;
      return Object.keys(e).length === n;
    }
  }
  return l !== l && e !== e;
}
const {
  SvelteComponent: xs,
  add_flush_callback: $l,
  append: Nt,
  attr: Te,
  bind: Wt,
  binding_callbacks: pt,
  check_outros: wt,
  construct_svelte_component: Pt,
  create_component: Ke,
  destroy_component: Je,
  detach: vt,
  element: bn,
  empty: Rn,
  group_outros: kt,
  init: $s,
  insert: yt,
  mount_component: Qe,
  noop: ea,
  safe_not_equal: ta,
  space: Fn,
  transition_in: Y,
  transition_out: le
} = window.__gradio__svelte__internal;
function ol(l) {
  let e, t, n, i, a, s, r, o, f, _, u = !/*use_3dgs*/
  l[12] && sl(l);
  a = new it({
    props: {
      Icon: Yl,
      label: (
        /*i18n*/
        l[8]("common.download")
      )
    }
  });
  const d = [la, na], c = [];
  function m(h, p) {
    return (
      /*use_3dgs*/
      h[12] ? 0 : 1
    );
  }
  return o = m(l), f = c[o] = d[o](l), {
    c() {
      e = bn("div"), t = bn("div"), u && u.c(), n = Fn(), i = bn("a"), Ke(a.$$.fragment), r = Fn(), f.c(), Te(
        i,
        "href",
        /*resolved_url*/
        l[16]
      ), Te(i, "target", window.__is_colab__ ? "_blank" : null), Te(i, "download", s = window.__is_colab__ ? null : (
        /*value*/
        l[0].orig_name || /*value*/
        l[0].path
      )), Te(t, "class", "buttons svelte-14rtuon"), Te(e, "class", "model3D svelte-14rtuon");
    },
    m(h, p) {
      yt(h, e, p), Nt(e, t), u && u.m(t, null), Nt(t, n), Nt(t, i), Qe(a, i, null), Nt(e, r), c[o].m(e, null), _ = !0;
    },
    p(h, p) {
      /*use_3dgs*/
      h[12] ? u && (kt(), le(u, 1, 1, () => {
        u = null;
      }), wt()) : u ? (u.p(h, p), p & /*use_3dgs*/
      4096 && Y(u, 1)) : (u = sl(h), u.c(), Y(u, 1), u.m(t, n));
      const y = {};
      p & /*i18n*/
      256 && (y.label = /*i18n*/
      h[8]("common.download")), a.$set(y), (!_ || p & /*resolved_url*/
      65536) && Te(
        i,
        "href",
        /*resolved_url*/
        h[16]
      ), (!_ || p & /*value*/
      1 && s !== (s = window.__is_colab__ ? null : (
        /*value*/
        h[0].orig_name || /*value*/
        h[0].path
      ))) && Te(i, "download", s);
      let b = o;
      o = m(h), o === b ? c[o].p(h, p) : (kt(), le(c[b], 1, 1, () => {
        c[b] = null;
      }), wt(), f = c[o], f ? f.p(h, p) : (f = c[o] = d[o](h), f.c()), Y(f, 1), f.m(e, null));
    },
    i(h) {
      _ || (Y(u), Y(a.$$.fragment, h), Y(f), _ = !0);
    },
    o(h) {
      le(u), le(a.$$.fragment, h), le(f), _ = !1;
    },
    d(h) {
      h && vt(e), u && u.d(), Je(a), c[o].d();
    }
  };
}
function sl(l) {
  let e, t;
  return e = new it({ props: { Icon: Kl, label: "Undo" } }), e.$on(
    "click",
    /*click_handler*/
    l[19]
  ), {
    c() {
      Ke(e.$$.fragment);
    },
    m(n, i) {
      Qe(e, n, i), t = !0;
    },
    p: ea,
    i(n) {
      t || (Y(e.$$.fragment, n), t = !0);
    },
    o(n) {
      le(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Je(e, n);
    }
  };
}
function na(l) {
  let e, t, n, i;
  function a(o) {
    l[22](o);
  }
  var s = (
    /*Canvas3DComponent*/
    l[15]
  );
  function r(o, f) {
    let _ = {
      value: (
        /*value*/
        o[0]
      ),
      env_map: (
        /*env_map*/
        o[1]
      ),
      tonemapping: (
        /*tonemapping*/
        o[2]
      ),
      exposure: (
        /*exposure*/
        o[3]
      ),
      contrast: (
        /*contrast*/
        o[4]
      ),
      clear_color: (
        /*clear_color*/
        o[5]
      ),
      camera_position: (
        /*camera_position*/
        o[11]
      ),
      zoom_speed: (
        /*zoom_speed*/
        o[9]
      ),
      pan_speed: (
        /*pan_speed*/
        o[10]
      )
    };
    return (
      /*resolved_url*/
      o[16] !== void 0 && (_.resolved_url = /*resolved_url*/
      o[16]), { props: _ }
    );
  }
  return s && (e = Pt(s, r(l)), l[21](e), pt.push(() => Wt(e, "resolved_url", a))), {
    c() {
      e && Ke(e.$$.fragment), n = Rn();
    },
    m(o, f) {
      e && Qe(e, o, f), yt(o, n, f), i = !0;
    },
    p(o, f) {
      if (f & /*Canvas3DComponent*/
      32768 && s !== (s = /*Canvas3DComponent*/
      o[15])) {
        if (e) {
          kt();
          const _ = e;
          le(_.$$.fragment, 1, 0, () => {
            Je(_, 1);
          }), wt();
        }
        s ? (e = Pt(s, r(o)), o[21](e), pt.push(() => Wt(e, "resolved_url", a)), Ke(e.$$.fragment), Y(e.$$.fragment, 1), Qe(e, n.parentNode, n)) : e = null;
      } else if (s) {
        const _ = {};
        f & /*value*/
        1 && (_.value = /*value*/
        o[0]), f & /*env_map*/
        2 && (_.env_map = /*env_map*/
        o[1]), f & /*tonemapping*/
        4 && (_.tonemapping = /*tonemapping*/
        o[2]), f & /*exposure*/
        8 && (_.exposure = /*exposure*/
        o[3]), f & /*contrast*/
        16 && (_.contrast = /*contrast*/
        o[4]), f & /*clear_color*/
        32 && (_.clear_color = /*clear_color*/
        o[5]), f & /*camera_position*/
        2048 && (_.camera_position = /*camera_position*/
        o[11]), f & /*zoom_speed*/
        512 && (_.zoom_speed = /*zoom_speed*/
        o[9]), f & /*pan_speed*/
        1024 && (_.pan_speed = /*pan_speed*/
        o[10]), !t && f & /*resolved_url*/
        65536 && (t = !0, _.resolved_url = /*resolved_url*/
        o[16], $l(() => t = !1)), e.$set(_);
      }
    },
    i(o) {
      i || (e && Y(e.$$.fragment, o), i = !0);
    },
    o(o) {
      e && le(e.$$.fragment, o), i = !1;
    },
    d(o) {
      o && vt(n), l[21](null), e && Je(e, o);
    }
  };
}
function la(l) {
  let e, t, n, i;
  function a(o) {
    l[20](o);
  }
  var s = (
    /*Canvas3DGSComponent*/
    l[14]
  );
  function r(o, f) {
    let _ = {
      value: (
        /*value*/
        o[0]
      ),
      zoom_speed: (
        /*zoom_speed*/
        o[9]
      ),
      pan_speed: (
        /*pan_speed*/
        o[10]
      )
    };
    return (
      /*resolved_url*/
      o[16] !== void 0 && (_.resolved_url = /*resolved_url*/
      o[16]), { props: _ }
    );
  }
  return s && (e = Pt(s, r(l)), pt.push(() => Wt(e, "resolved_url", a))), {
    c() {
      e && Ke(e.$$.fragment), n = Rn();
    },
    m(o, f) {
      e && Qe(e, o, f), yt(o, n, f), i = !0;
    },
    p(o, f) {
      if (f & /*Canvas3DGSComponent*/
      16384 && s !== (s = /*Canvas3DGSComponent*/
      o[14])) {
        if (e) {
          kt();
          const _ = e;
          le(_.$$.fragment, 1, 0, () => {
            Je(_, 1);
          }), wt();
        }
        s ? (e = Pt(s, r(o)), pt.push(() => Wt(e, "resolved_url", a)), Ke(e.$$.fragment), Y(e.$$.fragment, 1), Qe(e, n.parentNode, n)) : e = null;
      } else if (s) {
        const _ = {};
        f & /*value*/
        1 && (_.value = /*value*/
        o[0]), f & /*zoom_speed*/
        512 && (_.zoom_speed = /*zoom_speed*/
        o[9]), f & /*pan_speed*/
        1024 && (_.pan_speed = /*pan_speed*/
        o[10]), !t && f & /*resolved_url*/
        65536 && (t = !0, _.resolved_url = /*resolved_url*/
        o[16], $l(() => t = !1)), e.$set(_);
      }
    },
    i(o) {
      i || (e && Y(e.$$.fragment, o), i = !0);
    },
    o(o) {
      e && le(e.$$.fragment, o), i = !1;
    },
    d(o) {
      o && vt(n), e && Je(e, o);
    }
  };
}
function ia(l) {
  let e, t, n, i;
  e = new An({
    props: {
      show_label: (
        /*show_label*/
        l[7]
      ),
      Icon: Kt,
      label: (
        /*label*/
        l[6] || /*i18n*/
        l[8]("3D_model.3d_model")
      )
    }
  });
  let a = (
    /*value*/
    l[0] && ol(l)
  );
  return {
    c() {
      Ke(e.$$.fragment), t = Fn(), a && a.c(), n = Rn();
    },
    m(s, r) {
      Qe(e, s, r), yt(s, t, r), a && a.m(s, r), yt(s, n, r), i = !0;
    },
    p(s, [r]) {
      const o = {};
      r & /*show_label*/
      128 && (o.show_label = /*show_label*/
      s[7]), r & /*label, i18n*/
      320 && (o.label = /*label*/
      s[6] || /*i18n*/
      s[8]("3D_model.3d_model")), e.$set(o), /*value*/
      s[0] ? a ? (a.p(s, r), r & /*value*/
      1 && Y(a, 1)) : (a = ol(s), a.c(), Y(a, 1), a.m(n.parentNode, n)) : a && (kt(), le(a, 1, 1, () => {
        a = null;
      }), wt());
    },
    i(s) {
      i || (Y(e.$$.fragment, s), Y(a), i = !0);
    },
    o(s) {
      le(e.$$.fragment, s), le(a), i = !1;
    },
    d(s) {
      s && (vt(t), vt(n)), Je(e, s), a && a.d(s);
    }
  };
}
function oa(l, e, t) {
  var n = this && this.__awaiter || function(S, X, O, U) {
    function k(de) {
      return de instanceof O ? de : new O(function(me) {
        me(de);
      });
    }
    return new (O || (O = Promise))(function(de, me) {
      function z(P) {
        try {
          oe(U.next(P));
        } catch (Ee) {
          me(Ee);
        }
      }
      function ie(P) {
        try {
          oe(U.throw(P));
        } catch (Ee) {
          me(Ee);
        }
      }
      function oe(P) {
        P.done ? de(P.value) : k(P.value).then(z, ie);
      }
      oe((U = U.apply(S, X || [])).next());
    });
  };
  let { value: i } = e, { env_map: a = null } = e, { tonemapping: s = null } = e, { exposure: r = 1 } = e, { contrast: o = 1 } = e, { clear_color: f = [0, 0, 0, 0] } = e, { label: _ = "" } = e, { show_label: u } = e, { i18n: d } = e, { zoom_speed: c = 1 } = e, { pan_speed: m = 1 } = e, { camera_position: h = [null, null, null] } = e, p = { camera_position: h, zoom_speed: c, pan_speed: m }, y = !1, b, g;
  function q() {
    return n(this, void 0, void 0, function* () {
      return (yield import("./Canvas3D-Cduz95bA.js")).default;
    });
  }
  function I() {
    return n(this, void 0, void 0, function* () {
      return (yield import("./Canvas3DGS-BNgp41cs.js")).default;
    });
  }
  let v;
  function j() {
    v == null || v.reset_camera_position(h, c, m);
  }
  let E;
  const N = () => j();
  function B(S) {
    E = S, t(16, E);
  }
  function H(S) {
    pt[S ? "unshift" : "push"](() => {
      v = S, t(13, v);
    });
  }
  function K(S) {
    E = S, t(16, E);
  }
  return l.$$set = (S) => {
    "value" in S && t(0, i = S.value), "env_map" in S && t(1, a = S.env_map), "tonemapping" in S && t(2, s = S.tonemapping), "exposure" in S && t(3, r = S.exposure), "contrast" in S && t(4, o = S.contrast), "clear_color" in S && t(5, f = S.clear_color), "label" in S && t(6, _ = S.label), "show_label" in S && t(7, u = S.show_label), "i18n" in S && t(8, d = S.i18n), "zoom_speed" in S && t(9, c = S.zoom_speed), "pan_speed" in S && t(10, m = S.pan_speed), "camera_position" in S && t(11, h = S.camera_position);
  }, l.$$.update = () => {
    l.$$.dirty & /*value, use_3dgs*/
    4097 && i && (t(12, y = i.path.endsWith(".splat") || i.path.endsWith(".ply")), y ? I().then((S) => {
      t(14, b = S);
    }) : q().then((S) => {
      t(15, g = S);
    })), l.$$.dirty & /*env_map, use_3dgs*/
    4098 && (a ? y && console.log("Env map is ignored for 3DGS models") : console.log("Env map is not provided", a)), l.$$.dirty & /*current_settings, camera_position, zoom_speed, pan_speed, canvas3d*/
    273920 && (!bt(p.camera_position, h) || p.zoom_speed !== c || p.pan_speed !== m) && (v == null || v.reset_camera_position(h, c, m), t(18, p = { camera_position: h, zoom_speed: c, pan_speed: m }));
  }, [
    i,
    a,
    s,
    r,
    o,
    f,
    _,
    u,
    d,
    c,
    m,
    h,
    y,
    v,
    b,
    g,
    E,
    j,
    p,
    N,
    B,
    H,
    K
  ];
}
class sa extends xs {
  constructor(e) {
    super(), $s(this, e, oa, ia, ta, {
      value: 0,
      env_map: 1,
      tonemapping: 2,
      exposure: 3,
      contrast: 4,
      clear_color: 5,
      label: 6,
      show_label: 7,
      i18n: 8,
      zoom_speed: 9,
      pan_speed: 10,
      camera_position: 11
    });
  }
}
var aa = Object.defineProperty, ra = (l, e, t) => e in l ? aa(l, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : l[e] = t, Me = (l, e, t) => (ra(l, typeof e != "symbol" ? e + "" : e, t), t);
new Intl.Collator(0, { numeric: 1 }).compare;
async function fa(l, e) {
  return l.map(
    (t) => new _a({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class _a {
  constructor({
    path: e,
    url: t,
    orig_name: n,
    size: i,
    blob: a,
    is_stream: s,
    mime_type: r,
    alt_text: o
  }) {
    Me(this, "path"), Me(this, "url"), Me(this, "orig_name"), Me(this, "size"), Me(this, "blob"), Me(this, "is_stream"), Me(this, "mime_type"), Me(this, "alt_text"), Me(this, "meta", { _type: "gradio.FileData" }), this.path = e, this.url = t, this.orig_name = n, this.size = i, this.blob = t ? void 0 : a, this.is_stream = s, this.mime_type = r, this.alt_text = o;
  }
}
const {
  SvelteComponent: ua,
  append: x,
  attr: Ge,
  detach: ei,
  element: He,
  init: ca,
  insert: ti,
  noop: al,
  safe_not_equal: da,
  set_data: Zt,
  set_style: pn,
  space: Mn,
  text: _t,
  toggle_class: rl
} = window.__gradio__svelte__internal, { onMount: ma, createEventDispatcher: ha, onDestroy: ga } = window.__gradio__svelte__internal;
function fl(l) {
  let e, t, n, i, a = gt(
    /*file_to_display*/
    l[2]
  ) + "", s, r, o, f, _ = (
    /*file_to_display*/
    l[2].orig_name + ""
  ), u;
  return {
    c() {
      e = He("div"), t = He("span"), n = He("div"), i = He("progress"), s = _t(a), o = Mn(), f = He("span"), u = _t(_), pn(i, "visibility", "hidden"), pn(i, "height", "0"), pn(i, "width", "0"), i.value = r = gt(
        /*file_to_display*/
        l[2]
      ), Ge(i, "max", "100"), Ge(i, "class", "svelte-cr2edf"), Ge(n, "class", "progress-bar svelte-cr2edf"), Ge(f, "class", "file-name svelte-cr2edf"), Ge(e, "class", "file svelte-cr2edf");
    },
    m(d, c) {
      ti(d, e, c), x(e, t), x(t, n), x(n, i), x(i, s), x(e, o), x(e, f), x(f, u);
    },
    p(d, c) {
      c & /*file_to_display*/
      4 && a !== (a = gt(
        /*file_to_display*/
        d[2]
      ) + "") && Zt(s, a), c & /*file_to_display*/
      4 && r !== (r = gt(
        /*file_to_display*/
        d[2]
      )) && (i.value = r), c & /*file_to_display*/
      4 && _ !== (_ = /*file_to_display*/
      d[2].orig_name + "") && Zt(u, _);
    },
    d(d) {
      d && ei(e);
    }
  };
}
function ba(l) {
  let e, t, n, i = (
    /*files_with_progress*/
    l[0].length + ""
  ), a, s, r = (
    /*files_with_progress*/
    l[0].length > 1 ? "files" : "file"
  ), o, f, _, u = (
    /*file_to_display*/
    l[2] && fl(l)
  );
  return {
    c() {
      e = He("div"), t = He("span"), n = _t("Uploading "), a = _t(i), s = Mn(), o = _t(r), f = _t("..."), _ = Mn(), u && u.c(), Ge(t, "class", "uploading svelte-cr2edf"), Ge(e, "class", "wrap svelte-cr2edf"), rl(
        e,
        "progress",
        /*progress*/
        l[1]
      );
    },
    m(d, c) {
      ti(d, e, c), x(e, t), x(t, n), x(t, a), x(t, s), x(t, o), x(t, f), x(e, _), u && u.m(e, null);
    },
    p(d, [c]) {
      c & /*files_with_progress*/
      1 && i !== (i = /*files_with_progress*/
      d[0].length + "") && Zt(a, i), c & /*files_with_progress*/
      1 && r !== (r = /*files_with_progress*/
      d[0].length > 1 ? "files" : "file") && Zt(o, r), /*file_to_display*/
      d[2] ? u ? u.p(d, c) : (u = fl(d), u.c(), u.m(e, null)) : u && (u.d(1), u = null), c & /*progress*/
      2 && rl(
        e,
        "progress",
        /*progress*/
        d[1]
      );
    },
    i: al,
    o: al,
    d(d) {
      d && ei(e), u && u.d();
    }
  };
}
function gt(l) {
  return l.progress * 100 / (l.size || 0) || 0;
}
function pa(l) {
  let e = 0;
  return l.forEach((t) => {
    e += gt(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / l.length).toFixed(2) + "%"), e / l.length;
}
function wa(l, e, t) {
  var n = this && this.__awaiter || function(h, p, y, b) {
    function g(q) {
      return q instanceof y ? q : new y(function(I) {
        I(q);
      });
    }
    return new (y || (y = Promise))(function(q, I) {
      function v(N) {
        try {
          E(b.next(N));
        } catch (B) {
          I(B);
        }
      }
      function j(N) {
        try {
          E(b.throw(N));
        } catch (B) {
          I(B);
        }
      }
      function E(N) {
        N.done ? q(N.value) : g(N.value).then(v, j);
      }
      E((b = b.apply(h, p || [])).next());
    });
  };
  let { upload_id: i } = e, { root: a } = e, { files: s } = e, { stream_handler: r } = e, o, f = !1, _, u, d = s.map((h) => Object.assign(Object.assign({}, h), { progress: 0 }));
  const c = ha();
  function m(h, p) {
    t(0, d = d.map((y) => (y.orig_name === h && (y.progress += p), y)));
  }
  return ma(() => n(void 0, void 0, void 0, function* () {
    if (o = yield r(new URL(`${a}/upload_progress?upload_id=${i}`)), o == null)
      throw new Error("Event source is not defined");
    o.onmessage = function(h) {
      return n(this, void 0, void 0, function* () {
        const p = JSON.parse(h.data);
        f || t(1, f = !0), p.msg === "done" ? (o == null || o.close(), c("done")) : (t(7, _ = p), m(p.orig_name, p.chunk_size));
      });
    };
  })), ga(() => {
    (o != null || o != null) && o.close();
  }), l.$$set = (h) => {
    "upload_id" in h && t(3, i = h.upload_id), "root" in h && t(4, a = h.root), "files" in h && t(5, s = h.files), "stream_handler" in h && t(6, r = h.stream_handler);
  }, l.$$.update = () => {
    l.$$.dirty & /*files_with_progress*/
    1 && pa(d), l.$$.dirty & /*current_file_upload, files_with_progress*/
    129 && t(2, u = _ || d[0]);
  }, [
    d,
    f,
    u,
    i,
    a,
    s,
    r,
    _
  ];
}
class va extends ua {
  constructor(e) {
    super(), ca(this, e, wa, ba, da, {
      upload_id: 3,
      root: 4,
      files: 5,
      stream_handler: 6
    });
  }
}
const {
  SvelteComponent: ka,
  append: _l,
  attr: G,
  binding_callbacks: ya,
  bubble: We,
  check_outros: ni,
  create_component: za,
  create_slot: li,
  destroy_component: Ca,
  detach: Jt,
  element: jn,
  empty: ii,
  get_all_dirty_from_scope: oi,
  get_slot_changes: si,
  group_outros: ai,
  init: qa,
  insert: Qt,
  listen: ne,
  mount_component: Sa,
  prevent_default: Pe,
  run_all: La,
  safe_not_equal: Da,
  set_style: ri,
  space: Ea,
  stop_propagation: Ze,
  toggle_class: W,
  transition_in: Ae,
  transition_out: xe,
  update_slot_base: fi
} = window.__gradio__svelte__internal, { createEventDispatcher: Fa, tick: Ma } = window.__gradio__svelte__internal;
function ja(l) {
  let e, t, n, i, a, s, r, o, f, _, u;
  const d = (
    /*#slots*/
    l[26].default
  ), c = li(
    d,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = jn("button"), c && c.c(), t = Ea(), n = jn("input"), G(n, "aria-label", "file upload"), G(n, "data-testid", "file-upload"), G(n, "type", "file"), G(n, "accept", i = /*accept_file_types*/
      l[16] || void 0), n.multiple = a = /*file_count*/
      l[6] === "multiple" || void 0, G(n, "webkitdirectory", s = /*file_count*/
      l[6] === "directory" || void 0), G(n, "mozdirectory", r = /*file_count*/
      l[6] === "directory" || void 0), G(n, "class", "svelte-1s26xmt"), G(e, "tabindex", o = /*hidden*/
      l[9] ? -1 : 0), G(e, "class", "svelte-1s26xmt"), W(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), W(
        e,
        "center",
        /*center*/
        l[4]
      ), W(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), W(
        e,
        "flex",
        /*flex*/
        l[5]
      ), W(
        e,
        "disable_click",
        /*disable_click*/
        l[7]
      ), ri(e, "height", "100%");
    },
    m(m, h) {
      Qt(m, e, h), c && c.m(e, null), _l(e, t), _l(e, n), l[34](n), f = !0, _ || (u = [
        ne(
          n,
          "change",
          /*load_files_from_upload*/
          l[18]
        ),
        ne(e, "drag", Ze(Pe(
          /*drag_handler*/
          l[27]
        ))),
        ne(e, "dragstart", Ze(Pe(
          /*dragstart_handler*/
          l[28]
        ))),
        ne(e, "dragend", Ze(Pe(
          /*dragend_handler*/
          l[29]
        ))),
        ne(e, "dragover", Ze(Pe(
          /*dragover_handler*/
          l[30]
        ))),
        ne(e, "dragenter", Ze(Pe(
          /*dragenter_handler*/
          l[31]
        ))),
        ne(e, "dragleave", Ze(Pe(
          /*dragleave_handler*/
          l[32]
        ))),
        ne(e, "drop", Ze(Pe(
          /*drop_handler*/
          l[33]
        ))),
        ne(
          e,
          "click",
          /*open_file_upload*/
          l[13]
        ),
        ne(
          e,
          "drop",
          /*loadFilesFromDrop*/
          l[19]
        ),
        ne(
          e,
          "dragenter",
          /*updateDragging*/
          l[17]
        ),
        ne(
          e,
          "dragleave",
          /*updateDragging*/
          l[17]
        )
      ], _ = !0);
    },
    p(m, h) {
      c && c.p && (!f || h[0] & /*$$scope*/
      33554432) && fi(
        c,
        d,
        m,
        /*$$scope*/
        m[25],
        f ? si(
          d,
          /*$$scope*/
          m[25],
          h,
          null
        ) : oi(
          /*$$scope*/
          m[25]
        ),
        null
      ), (!f || h[0] & /*accept_file_types*/
      65536 && i !== (i = /*accept_file_types*/
      m[16] || void 0)) && G(n, "accept", i), (!f || h[0] & /*file_count*/
      64 && a !== (a = /*file_count*/
      m[6] === "multiple" || void 0)) && (n.multiple = a), (!f || h[0] & /*file_count*/
      64 && s !== (s = /*file_count*/
      m[6] === "directory" || void 0)) && G(n, "webkitdirectory", s), (!f || h[0] & /*file_count*/
      64 && r !== (r = /*file_count*/
      m[6] === "directory" || void 0)) && G(n, "mozdirectory", r), (!f || h[0] & /*hidden*/
      512 && o !== (o = /*hidden*/
      m[9] ? -1 : 0)) && G(e, "tabindex", o), (!f || h[0] & /*hidden*/
      512) && W(
        e,
        "hidden",
        /*hidden*/
        m[9]
      ), (!f || h[0] & /*center*/
      16) && W(
        e,
        "center",
        /*center*/
        m[4]
      ), (!f || h[0] & /*boundedheight*/
      8) && W(
        e,
        "boundedheight",
        /*boundedheight*/
        m[3]
      ), (!f || h[0] & /*flex*/
      32) && W(
        e,
        "flex",
        /*flex*/
        m[5]
      ), (!f || h[0] & /*disable_click*/
      128) && W(
        e,
        "disable_click",
        /*disable_click*/
        m[7]
      );
    },
    i(m) {
      f || (Ae(c, m), f = !0);
    },
    o(m) {
      xe(c, m), f = !1;
    },
    d(m) {
      m && Jt(e), c && c.d(m), l[34](null), _ = !1, La(u);
    }
  };
}
function Ia(l) {
  let e, t, n = !/*hidden*/
  l[9] && ul(l);
  return {
    c() {
      n && n.c(), e = ii();
    },
    m(i, a) {
      n && n.m(i, a), Qt(i, e, a), t = !0;
    },
    p(i, a) {
      /*hidden*/
      i[9] ? n && (ai(), xe(n, 1, 1, () => {
        n = null;
      }), ni()) : n ? (n.p(i, a), a[0] & /*hidden*/
      512 && Ae(n, 1)) : (n = ul(i), n.c(), Ae(n, 1), n.m(e.parentNode, e));
    },
    i(i) {
      t || (Ae(n), t = !0);
    },
    o(i) {
      xe(n), t = !1;
    },
    d(i) {
      i && Jt(e), n && n.d(i);
    }
  };
}
function Na(l) {
  let e, t, n, i, a;
  const s = (
    /*#slots*/
    l[26].default
  ), r = li(
    s,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = jn("button"), r && r.c(), G(e, "tabindex", t = /*hidden*/
      l[9] ? -1 : 0), G(e, "class", "svelte-1s26xmt"), W(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), W(
        e,
        "center",
        /*center*/
        l[4]
      ), W(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), W(
        e,
        "flex",
        /*flex*/
        l[5]
      ), ri(e, "height", "100%");
    },
    m(o, f) {
      Qt(o, e, f), r && r.m(e, null), n = !0, i || (a = ne(
        e,
        "click",
        /*paste_clipboard*/
        l[12]
      ), i = !0);
    },
    p(o, f) {
      r && r.p && (!n || f[0] & /*$$scope*/
      33554432) && fi(
        r,
        s,
        o,
        /*$$scope*/
        o[25],
        n ? si(
          s,
          /*$$scope*/
          o[25],
          f,
          null
        ) : oi(
          /*$$scope*/
          o[25]
        ),
        null
      ), (!n || f[0] & /*hidden*/
      512 && t !== (t = /*hidden*/
      o[9] ? -1 : 0)) && G(e, "tabindex", t), (!n || f[0] & /*hidden*/
      512) && W(
        e,
        "hidden",
        /*hidden*/
        o[9]
      ), (!n || f[0] & /*center*/
      16) && W(
        e,
        "center",
        /*center*/
        o[4]
      ), (!n || f[0] & /*boundedheight*/
      8) && W(
        e,
        "boundedheight",
        /*boundedheight*/
        o[3]
      ), (!n || f[0] & /*flex*/
      32) && W(
        e,
        "flex",
        /*flex*/
        o[5]
      );
    },
    i(o) {
      n || (Ae(r, o), n = !0);
    },
    o(o) {
      xe(r, o), n = !1;
    },
    d(o) {
      o && Jt(e), r && r.d(o), i = !1, a();
    }
  };
}
function ul(l) {
  let e, t;
  return e = new va({
    props: {
      root: (
        /*root*/
        l[8]
      ),
      upload_id: (
        /*upload_id*/
        l[14]
      ),
      files: (
        /*file_data*/
        l[15]
      ),
      stream_handler: (
        /*stream_handler*/
        l[11]
      )
    }
  }), {
    c() {
      za(e.$$.fragment);
    },
    m(n, i) {
      Sa(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i[0] & /*root*/
      256 && (a.root = /*root*/
      n[8]), i[0] & /*upload_id*/
      16384 && (a.upload_id = /*upload_id*/
      n[14]), i[0] & /*file_data*/
      32768 && (a.files = /*file_data*/
      n[15]), i[0] & /*stream_handler*/
      2048 && (a.stream_handler = /*stream_handler*/
      n[11]), e.$set(a);
    },
    i(n) {
      t || (Ae(e.$$.fragment, n), t = !0);
    },
    o(n) {
      xe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ca(e, n);
    }
  };
}
function Ua(l) {
  let e, t, n, i;
  const a = [Na, Ia, ja], s = [];
  function r(o, f) {
    return (
      /*filetype*/
      o[0] === "clipboard" ? 0 : (
        /*uploading*/
        o[1] && /*show_progress*/
        o[10] ? 1 : 2
      )
    );
  }
  return e = r(l), t = s[e] = a[e](l), {
    c() {
      t.c(), n = ii();
    },
    m(o, f) {
      s[e].m(o, f), Qt(o, n, f), i = !0;
    },
    p(o, f) {
      let _ = e;
      e = r(o), e === _ ? s[e].p(o, f) : (ai(), xe(s[_], 1, 1, () => {
        s[_] = null;
      }), ni(), t = s[e], t ? t.p(o, f) : (t = s[e] = a[e](o), t.c()), Ae(t, 1), t.m(n.parentNode, n));
    },
    i(o) {
      i || (Ae(t), i = !0);
    },
    o(o) {
      xe(t), i = !1;
    },
    d(o) {
      o && Jt(n), s[e].d(o);
    }
  };
}
function Va(l, e, t) {
  if (!l || l === "*" || l === "file/*" || Array.isArray(l) && l.some((i) => i === "*" || i === "file/*"))
    return !0;
  let n;
  if (typeof l == "string")
    n = l.split(",").map((i) => i.trim());
  else if (Array.isArray(l))
    n = l;
  else
    return !1;
  return n.includes(e) || n.some((i) => {
    const [a] = i.split("/").map((s) => s.trim());
    return i.endsWith("/*") && t.startsWith(a + "/");
  });
}
function Aa(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  var a = this && this.__awaiter || function(w, M, R, V) {
    function T(Re) {
      return Re instanceof R ? Re : new R(function(ot) {
        ot(Re);
      });
    }
    return new (R || (R = Promise))(function(Re, ot) {
      function mt(Oe) {
        try {
          Be(V.next(Oe));
        } catch (nn) {
          ot(nn);
        }
      }
      function Fe(Oe) {
        try {
          Be(V.throw(Oe));
        } catch (nn) {
          ot(nn);
        }
      }
      function Be(Oe) {
        Oe.done ? Re(Oe.value) : T(Oe.value).then(mt, Fe);
      }
      Be((V = V.apply(w, M || [])).next());
    });
  };
  let { filetype: s = null } = e, { dragging: r = !1 } = e, { boundedheight: o = !0 } = e, { center: f = !0 } = e, { flex: _ = !0 } = e, { file_count: u = "single" } = e, { disable_click: d = !1 } = e, { root: c } = e, { hidden: m = !1 } = e, { format: h = "file" } = e, { uploading: p = !1 } = e, { hidden_upload: y = null } = e, { show_progress: b = !0 } = e, { max_file_size: g = null } = e, { upload: q } = e, { stream_handler: I } = e, v, j, E;
  const N = Fa(), B = ["image", "video", "audio", "text", "file"], H = (w) => w.startsWith(".") || w.endsWith("/*") ? w : B.includes(w) ? w + "/*" : "." + w;
  function K() {
    t(20, r = !r);
  }
  function S() {
    navigator.clipboard.read().then((w) => a(this, void 0, void 0, function* () {
      for (let M = 0; M < w.length; M++) {
        const R = w[M].types.find((V) => V.startsWith("image/"));
        if (R) {
          w[M].getType(R).then((V) => a(this, void 0, void 0, function* () {
            const T = new File([V], `clipboard.${R.replace("image/", "")}`);
            yield U([T]);
          }));
          break;
        }
      }
    }));
  }
  function X() {
    d || y && (t(2, y.value = "", y), y.click());
  }
  function O(w) {
    return a(this, void 0, void 0, function* () {
      yield Ma(), t(14, v = Math.random().toString(36).substring(2, 15)), t(1, p = !0);
      try {
        const M = yield q(w, c, v, g ?? 1 / 0);
        return N("load", u === "single" ? M == null ? void 0 : M[0] : M), t(1, p = !1), M || [];
      } catch (M) {
        return N("error", M.message), t(1, p = !1), [];
      }
    });
  }
  function U(w) {
    return a(this, void 0, void 0, function* () {
      if (!w.length)
        return;
      let M = w.map((R) => new File([R], R instanceof File ? R.name : "file", { type: R.type }));
      return t(15, j = yield fa(M)), yield O(j);
    });
  }
  function k(w) {
    return a(this, void 0, void 0, function* () {
      const M = w.target;
      if (M.files)
        if (h != "blob")
          yield U(Array.from(M.files));
        else {
          if (u === "single") {
            N("load", M.files[0]);
            return;
          }
          N("load", M.files);
        }
    });
  }
  function de(w) {
    return a(this, void 0, void 0, function* () {
      var M;
      if (t(20, r = !1), !(!((M = w.dataTransfer) === null || M === void 0) && M.files))
        return;
      const R = Array.from(w.dataTransfer.files).filter((V) => {
        const T = "." + V.name.split(".").pop();
        return T && Va(E, T, V.type) || (T && Array.isArray(s) ? s.includes(T) : T === s) ? !0 : (N("error", `Invalid file type only ${s} allowed.`), !1);
      });
      yield U(R);
    });
  }
  function me(w) {
    We.call(this, l, w);
  }
  function z(w) {
    We.call(this, l, w);
  }
  function ie(w) {
    We.call(this, l, w);
  }
  function oe(w) {
    We.call(this, l, w);
  }
  function P(w) {
    We.call(this, l, w);
  }
  function Ee(w) {
    We.call(this, l, w);
  }
  function C(w) {
    We.call(this, l, w);
  }
  function Ie(w) {
    ya[w ? "unshift" : "push"](() => {
      y = w, t(2, y);
    });
  }
  return l.$$set = (w) => {
    "filetype" in w && t(0, s = w.filetype), "dragging" in w && t(20, r = w.dragging), "boundedheight" in w && t(3, o = w.boundedheight), "center" in w && t(4, f = w.center), "flex" in w && t(5, _ = w.flex), "file_count" in w && t(6, u = w.file_count), "disable_click" in w && t(7, d = w.disable_click), "root" in w && t(8, c = w.root), "hidden" in w && t(9, m = w.hidden), "format" in w && t(21, h = w.format), "uploading" in w && t(1, p = w.uploading), "hidden_upload" in w && t(2, y = w.hidden_upload), "show_progress" in w && t(10, b = w.show_progress), "max_file_size" in w && t(22, g = w.max_file_size), "upload" in w && t(23, q = w.upload), "stream_handler" in w && t(11, I = w.stream_handler), "$$scope" in w && t(25, i = w.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*filetype*/
    1 && (s == null ? t(16, E = null) : typeof s == "string" ? t(16, E = H(s)) : (t(0, s = s.map(H)), t(16, E = s.join(", "))));
  }, [
    s,
    p,
    y,
    o,
    f,
    _,
    u,
    d,
    c,
    m,
    b,
    I,
    S,
    X,
    v,
    j,
    E,
    K,
    k,
    de,
    r,
    h,
    g,
    q,
    U,
    i,
    n,
    me,
    z,
    ie,
    oe,
    P,
    Ee,
    C,
    Ie
  ];
}
class Ra extends ka {
  constructor(e) {
    super(), qa(
      this,
      e,
      Aa,
      Ua,
      Da,
      {
        filetype: 0,
        dragging: 20,
        boundedheight: 3,
        center: 4,
        flex: 5,
        file_count: 6,
        disable_click: 7,
        root: 8,
        hidden: 9,
        format: 21,
        uploading: 1,
        hidden_upload: 2,
        show_progress: 10,
        max_file_size: 22,
        upload: 23,
        stream_handler: 11,
        paste_clipboard: 12,
        open_file_upload: 13,
        load_files: 24
      },
      null,
      [-1, -1]
    );
  }
  get paste_clipboard() {
    return this.$$.ctx[12];
  }
  get open_file_upload() {
    return this.$$.ctx[13];
  }
  get load_files() {
    return this.$$.ctx[24];
  }
}
const { setContext: Zf, getContext: Ba } = window.__gradio__svelte__internal, Oa = "WORKER_PROXY_CONTEXT_KEY";
function _i() {
  return Ba(Oa);
}
function Ta(l) {
  return l.host === window.location.host || l.host === "localhost:7860" || l.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  l.host === "lite.local";
}
function ui(l, e) {
  const t = e.toLowerCase();
  for (const [n, i] of Object.entries(l))
    if (n.toLowerCase() === t)
      return i;
}
function ci(l) {
  if (l == null)
    return !1;
  const e = new URL(l, window.location.href);
  return !(!Ta(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
async function Gf(l) {
  if (l == null || !ci(l))
    return l;
  const e = _i();
  if (e == null)
    return l;
  const n = new URL(l, window.location.href).pathname;
  return e.httpRequest({
    method: "GET",
    path: n,
    headers: {},
    query_string: ""
  }).then((i) => {
    if (i.status !== 200)
      throw new Error(`Failed to get file ${n} from the Wasm worker.`);
    const a = new Blob([i.body], {
      type: ui(i.headers, "content-type")
    });
    return URL.createObjectURL(a);
  });
}
const {
  SvelteComponent: Wa,
  assign: Gt,
  check_outros: di,
  compute_rest_props: cl,
  create_slot: Bn,
  detach: xt,
  element: mi,
  empty: hi,
  exclude_internal_props: Pa,
  get_all_dirty_from_scope: On,
  get_slot_changes: Tn,
  get_spread_update: gi,
  group_outros: bi,
  init: Za,
  insert: $t,
  listen: pi,
  prevent_default: Ga,
  safe_not_equal: Ha,
  set_attributes: Ht,
  transition_in: $e,
  transition_out: et,
  update_slot_base: Wn
} = window.__gradio__svelte__internal, { createEventDispatcher: Xa } = window.__gradio__svelte__internal;
function Ya(l) {
  let e, t, n, i, a;
  const s = (
    /*#slots*/
    l[8].default
  ), r = Bn(
    s,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let o = [
    { href: (
      /*href*/
      l[0]
    ) },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    { rel: "noopener noreferrer" },
    { download: (
      /*download*/
      l[1]
    ) },
    /*$$restProps*/
    l[6]
  ], f = {};
  for (let _ = 0; _ < o.length; _ += 1)
    f = Gt(f, o[_]);
  return {
    c() {
      e = mi("a"), r && r.c(), Ht(e, f);
    },
    m(_, u) {
      $t(_, e, u), r && r.m(e, null), n = !0, i || (a = pi(
        e,
        "click",
        /*dispatch*/
        l[3].bind(null, "click")
      ), i = !0);
    },
    p(_, u) {
      r && r.p && (!n || u & /*$$scope*/
      128) && Wn(
        r,
        s,
        _,
        /*$$scope*/
        _[7],
        n ? Tn(
          s,
          /*$$scope*/
          _[7],
          u,
          null
        ) : On(
          /*$$scope*/
          _[7]
        ),
        null
      ), Ht(e, f = gi(o, [
        (!n || u & /*href*/
        1) && { href: (
          /*href*/
          _[0]
        ) },
        { target: t },
        { rel: "noopener noreferrer" },
        (!n || u & /*download*/
        2) && { download: (
          /*download*/
          _[1]
        ) },
        u & /*$$restProps*/
        64 && /*$$restProps*/
        _[6]
      ]));
    },
    i(_) {
      n || ($e(r, _), n = !0);
    },
    o(_) {
      et(r, _), n = !1;
    },
    d(_) {
      _ && xt(e), r && r.d(_), i = !1, a();
    }
  };
}
function Ka(l) {
  let e, t, n, i;
  const a = [Qa, Ja], s = [];
  function r(o, f) {
    return (
      /*is_downloading*/
      o[2] ? 0 : 1
    );
  }
  return e = r(l), t = s[e] = a[e](l), {
    c() {
      t.c(), n = hi();
    },
    m(o, f) {
      s[e].m(o, f), $t(o, n, f), i = !0;
    },
    p(o, f) {
      let _ = e;
      e = r(o), e === _ ? s[e].p(o, f) : (bi(), et(s[_], 1, 1, () => {
        s[_] = null;
      }), di(), t = s[e], t ? t.p(o, f) : (t = s[e] = a[e](o), t.c()), $e(t, 1), t.m(n.parentNode, n));
    },
    i(o) {
      i || ($e(t), i = !0);
    },
    o(o) {
      et(t), i = !1;
    },
    d(o) {
      o && xt(n), s[e].d(o);
    }
  };
}
function Ja(l) {
  let e, t, n, i;
  const a = (
    /*#slots*/
    l[8].default
  ), s = Bn(
    a,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let r = [
    /*$$restProps*/
    l[6],
    { href: (
      /*href*/
      l[0]
    ) }
  ], o = {};
  for (let f = 0; f < r.length; f += 1)
    o = Gt(o, r[f]);
  return {
    c() {
      e = mi("a"), s && s.c(), Ht(e, o);
    },
    m(f, _) {
      $t(f, e, _), s && s.m(e, null), t = !0, n || (i = pi(e, "click", Ga(
        /*wasm_click_handler*/
        l[5]
      )), n = !0);
    },
    p(f, _) {
      s && s.p && (!t || _ & /*$$scope*/
      128) && Wn(
        s,
        a,
        f,
        /*$$scope*/
        f[7],
        t ? Tn(
          a,
          /*$$scope*/
          f[7],
          _,
          null
        ) : On(
          /*$$scope*/
          f[7]
        ),
        null
      ), Ht(e, o = gi(r, [
        _ & /*$$restProps*/
        64 && /*$$restProps*/
        f[6],
        (!t || _ & /*href*/
        1) && { href: (
          /*href*/
          f[0]
        ) }
      ]));
    },
    i(f) {
      t || ($e(s, f), t = !0);
    },
    o(f) {
      et(s, f), t = !1;
    },
    d(f) {
      f && xt(e), s && s.d(f), n = !1, i();
    }
  };
}
function Qa(l) {
  let e;
  const t = (
    /*#slots*/
    l[8].default
  ), n = Bn(
    t,
    l,
    /*$$scope*/
    l[7],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, a) {
      n && n.m(i, a), e = !0;
    },
    p(i, a) {
      n && n.p && (!e || a & /*$$scope*/
      128) && Wn(
        n,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? Tn(
          t,
          /*$$scope*/
          i[7],
          a,
          null
        ) : On(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || ($e(n, i), e = !0);
    },
    o(i) {
      et(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function xa(l) {
  let e, t, n, i, a;
  const s = [Ka, Ya], r = [];
  function o(f, _) {
    return _ & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (f[4] && ci(
      /*href*/
      f[0]
    ))), e ? 0 : 1;
  }
  return t = o(l, -1), n = r[t] = s[t](l), {
    c() {
      n.c(), i = hi();
    },
    m(f, _) {
      r[t].m(f, _), $t(f, i, _), a = !0;
    },
    p(f, [_]) {
      let u = t;
      t = o(f, _), t === u ? r[t].p(f, _) : (bi(), et(r[u], 1, 1, () => {
        r[u] = null;
      }), di(), n = r[t], n ? n.p(f, _) : (n = r[t] = s[t](f), n.c()), $e(n, 1), n.m(i.parentNode, i));
    },
    i(f) {
      a || ($e(n), a = !0);
    },
    o(f) {
      et(n), a = !1;
    },
    d(f) {
      f && xt(i), r[t].d(f);
    }
  };
}
function $a(l, e, t) {
  const n = ["href", "download"];
  let i = cl(e, n), { $$slots: a = {}, $$scope: s } = e;
  var r = this && this.__awaiter || function(m, h, p, y) {
    function b(g) {
      return g instanceof p ? g : new p(function(q) {
        q(g);
      });
    }
    return new (p || (p = Promise))(function(g, q) {
      function I(E) {
        try {
          j(y.next(E));
        } catch (N) {
          q(N);
        }
      }
      function v(E) {
        try {
          j(y.throw(E));
        } catch (N) {
          q(N);
        }
      }
      function j(E) {
        E.done ? g(E.value) : b(E.value).then(I, v);
      }
      j((y = y.apply(m, h || [])).next());
    });
  };
  let { href: o = void 0 } = e, { download: f } = e;
  const _ = Xa();
  let u = !1;
  const d = _i();
  function c() {
    return r(this, void 0, void 0, function* () {
      if (u)
        return;
      if (_("click"), o == null)
        throw new Error("href is not defined.");
      if (d == null)
        throw new Error("Wasm worker proxy is not available.");
      const h = new URL(o, window.location.href).pathname;
      t(2, u = !0), d.httpRequest({
        method: "GET",
        path: h,
        headers: {},
        query_string: ""
      }).then((p) => {
        if (p.status !== 200)
          throw new Error(`Failed to get file ${h} from the Wasm worker.`);
        const y = new Blob(
          [p.body],
          {
            type: ui(p.headers, "content-type")
          }
        ), b = URL.createObjectURL(y), g = document.createElement("a");
        g.href = b, g.download = f, g.click(), URL.revokeObjectURL(b);
      }).finally(() => {
        t(2, u = !1);
      });
    });
  }
  return l.$$set = (m) => {
    e = Gt(Gt({}, e), Pa(m)), t(6, i = cl(e, n)), "href" in m && t(0, o = m.href), "download" in m && t(1, f = m.download), "$$scope" in m && t(7, s = m.$$scope);
  }, [
    o,
    f,
    u,
    _,
    d,
    c,
    i,
    s,
    a
  ];
}
class er extends Wa {
  constructor(e) {
    super(), Za(this, e, $a, xa, Ha, { href: 0, download: 1 });
  }
}
const {
  SvelteComponent: tr,
  append: wn,
  attr: nr,
  check_outros: vn,
  create_component: Lt,
  destroy_component: Dt,
  detach: lr,
  element: ir,
  group_outros: kn,
  init: or,
  insert: sr,
  mount_component: Et,
  safe_not_equal: ar,
  set_style: dl,
  space: yn,
  toggle_class: ml,
  transition_in: Q,
  transition_out: we
} = window.__gradio__svelte__internal, { createEventDispatcher: rr } = window.__gradio__svelte__internal;
function hl(l) {
  let e, t;
  return e = new it({
    props: {
      Icon: ds,
      label: (
        /*i18n*/
        l[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[6]
  ), {
    c() {
      Lt(e.$$.fragment);
    },
    m(n, i) {
      Et(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*i18n*/
      16 && (a.label = /*i18n*/
      n[4]("common.edit")), e.$set(a);
    },
    i(n) {
      t || (Q(e.$$.fragment, n), t = !0);
    },
    o(n) {
      we(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Dt(e, n);
    }
  };
}
function gl(l) {
  let e, t;
  return e = new it({
    props: {
      Icon: Kl,
      label: (
        /*i18n*/
        l[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    l[7]
  ), {
    c() {
      Lt(e.$$.fragment);
    },
    m(n, i) {
      Et(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*i18n*/
      16 && (a.label = /*i18n*/
      n[4]("common.undo")), e.$set(a);
    },
    i(n) {
      t || (Q(e.$$.fragment, n), t = !0);
    },
    o(n) {
      we(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Dt(e, n);
    }
  };
}
function bl(l) {
  let e, t;
  return e = new er({
    props: {
      href: (
        /*download*/
        l[2]
      ),
      download: !0,
      $$slots: { default: [fr] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Lt(e.$$.fragment);
    },
    m(n, i) {
      Et(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*download*/
      4 && (a.href = /*download*/
      n[2]), i & /*$$scope, i18n*/
      528 && (a.$$scope = { dirty: i, ctx: n }), e.$set(a);
    },
    i(n) {
      t || (Q(e.$$.fragment, n), t = !0);
    },
    o(n) {
      we(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Dt(e, n);
    }
  };
}
function fr(l) {
  let e, t;
  return e = new it({
    props: {
      Icon: Yl,
      label: (
        /*i18n*/
        l[4]("common.download")
      )
    }
  }), {
    c() {
      Lt(e.$$.fragment);
    },
    m(n, i) {
      Et(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*i18n*/
      16 && (a.label = /*i18n*/
      n[4]("common.download")), e.$set(a);
    },
    i(n) {
      t || (Q(e.$$.fragment, n), t = !0);
    },
    o(n) {
      we(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Dt(e, n);
    }
  };
}
function _r(l) {
  let e, t, n, i, a, s, r = (
    /*editable*/
    l[0] && hl(l)
  ), o = (
    /*undoable*/
    l[1] && gl(l)
  ), f = (
    /*download*/
    l[2] && bl(l)
  );
  return a = new it({
    props: {
      Icon: Xl,
      label: (
        /*i18n*/
        l[4]("common.clear")
      )
    }
  }), a.$on(
    "click",
    /*click_handler_2*/
    l[8]
  ), {
    c() {
      e = ir("div"), r && r.c(), t = yn(), o && o.c(), n = yn(), f && f.c(), i = yn(), Lt(a.$$.fragment), nr(e, "class", "svelte-1wj0ocy"), ml(e, "not-absolute", !/*absolute*/
      l[3]), dl(
        e,
        "position",
        /*absolute*/
        l[3] ? "absolute" : "static"
      );
    },
    m(_, u) {
      sr(_, e, u), r && r.m(e, null), wn(e, t), o && o.m(e, null), wn(e, n), f && f.m(e, null), wn(e, i), Et(a, e, null), s = !0;
    },
    p(_, [u]) {
      /*editable*/
      _[0] ? r ? (r.p(_, u), u & /*editable*/
      1 && Q(r, 1)) : (r = hl(_), r.c(), Q(r, 1), r.m(e, t)) : r && (kn(), we(r, 1, 1, () => {
        r = null;
      }), vn()), /*undoable*/
      _[1] ? o ? (o.p(_, u), u & /*undoable*/
      2 && Q(o, 1)) : (o = gl(_), o.c(), Q(o, 1), o.m(e, n)) : o && (kn(), we(o, 1, 1, () => {
        o = null;
      }), vn()), /*download*/
      _[2] ? f ? (f.p(_, u), u & /*download*/
      4 && Q(f, 1)) : (f = bl(_), f.c(), Q(f, 1), f.m(e, i)) : f && (kn(), we(f, 1, 1, () => {
        f = null;
      }), vn());
      const d = {};
      u & /*i18n*/
      16 && (d.label = /*i18n*/
      _[4]("common.clear")), a.$set(d), (!s || u & /*absolute*/
      8) && ml(e, "not-absolute", !/*absolute*/
      _[3]), u & /*absolute*/
      8 && dl(
        e,
        "position",
        /*absolute*/
        _[3] ? "absolute" : "static"
      );
    },
    i(_) {
      s || (Q(r), Q(o), Q(f), Q(a.$$.fragment, _), s = !0);
    },
    o(_) {
      we(r), we(o), we(f), we(a.$$.fragment, _), s = !1;
    },
    d(_) {
      _ && lr(e), r && r.d(), o && o.d(), f && f.d(), Dt(a);
    }
  };
}
function ur(l, e, t) {
  let { editable: n = !1 } = e, { undoable: i = !1 } = e, { download: a = null } = e, { absolute: s = !0 } = e, { i18n: r } = e;
  const o = rr(), f = () => o("edit"), _ = () => o("undo"), u = (d) => {
    o("clear"), d.stopPropagation();
  };
  return l.$$set = (d) => {
    "editable" in d && t(0, n = d.editable), "undoable" in d && t(1, i = d.undoable), "download" in d && t(2, a = d.download), "absolute" in d && t(3, s = d.absolute), "i18n" in d && t(4, r = d.i18n);
  }, [
    n,
    i,
    a,
    s,
    r,
    o,
    f,
    _,
    u
  ];
}
class cr extends tr {
  constructor(e) {
    super(), or(this, e, ur, _r, ar, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
}
const {
  SvelteComponent: dr,
  add_flush_callback: mr,
  append: hr,
  attr: gr,
  bind: br,
  binding_callbacks: wi,
  bubble: pr,
  check_outros: en,
  construct_svelte_component: Xt,
  create_component: tt,
  create_slot: wr,
  destroy_component: nt,
  detach: zt,
  element: vr,
  empty: Pn,
  get_all_dirty_from_scope: kr,
  get_slot_changes: yr,
  group_outros: tn,
  init: zr,
  insert: Ct,
  mount_component: lt,
  safe_not_equal: Cr,
  space: vi,
  transition_in: _e,
  transition_out: ue,
  update_slot_base: qr
} = window.__gradio__svelte__internal, { createEventDispatcher: Sr, tick: pl } = window.__gradio__svelte__internal;
function Lr(l) {
  let e, t, n, i, a, s;
  t = new cr({
    props: {
      undoable: !/*use_3dgs*/
      l[16],
      i18n: (
        /*i18n*/
        l[9]
      ),
      absolute: !0
    }
  }), t.$on(
    "clear",
    /*handle_clear*/
    l[22]
  ), t.$on(
    "undo",
    /*handle_undo*/
    l[23]
  );
  const r = [Fr, Er], o = [];
  function f(_, u) {
    return (
      /*use_3dgs*/
      _[16] ? 0 : 1
    );
  }
  return i = f(l), a = o[i] = r[i](l), {
    c() {
      e = vr("div"), tt(t.$$.fragment), n = vi(), a.c(), gr(e, "class", "input-model svelte-1oz8ks8");
    },
    m(_, u) {
      Ct(_, e, u), lt(t, e, null), hr(e, n), o[i].m(e, null), s = !0;
    },
    p(_, u) {
      const d = {};
      u[0] & /*use_3dgs*/
      65536 && (d.undoable = !/*use_3dgs*/
      _[16]), u[0] & /*i18n*/
      512 && (d.i18n = /*i18n*/
      _[9]), t.$set(d);
      let c = i;
      i = f(_), i === c ? o[i].p(_, u) : (tn(), ue(o[c], 1, 1, () => {
        o[c] = null;
      }), en(), a = o[i], a ? a.p(_, u) : (a = o[i] = r[i](_), a.c()), _e(a, 1), a.m(e, null));
    },
    i(_) {
      s || (_e(t.$$.fragment, _), _e(a), s = !0);
    },
    o(_) {
      ue(t.$$.fragment, _), ue(a), s = !1;
    },
    d(_) {
      _ && zt(e), nt(t), o[i].d();
    }
  };
}
function Dr(l) {
  let e, t, n;
  function i(s) {
    l[25](s);
  }
  let a = {
    upload: (
      /*upload*/
      l[14]
    ),
    stream_handler: (
      /*stream_handler*/
      l[15]
    ),
    root: (
      /*root*/
      l[8]
    ),
    max_file_size: (
      /*max_file_size*/
      l[12]
    ),
    filetype: [".stl", ".obj", ".gltf", ".glb", "model/obj", ".splat", ".ply"],
    $$slots: { default: [Mr] },
    $$scope: { ctx: l }
  };
  return (
    /*dragging*/
    l[17] !== void 0 && (a.dragging = /*dragging*/
    l[17]), e = new Ra({ props: a }), wi.push(() => br(e, "dragging", i)), e.$on(
      "load",
      /*handle_upload*/
      l[21]
    ), e.$on(
      "error",
      /*error_handler*/
      l[26]
    ), {
      c() {
        tt(e.$$.fragment);
      },
      m(s, r) {
        lt(e, s, r), n = !0;
      },
      p(s, r) {
        const o = {};
        r[0] & /*upload*/
        16384 && (o.upload = /*upload*/
        s[14]), r[0] & /*stream_handler*/
        32768 && (o.stream_handler = /*stream_handler*/
        s[15]), r[0] & /*root*/
        256 && (o.root = /*root*/
        s[8]), r[0] & /*max_file_size*/
        4096 && (o.max_file_size = /*max_file_size*/
        s[12]), r[0] & /*$$scope*/
        268435456 && (o.$$scope = { dirty: r, ctx: s }), !t && r[0] & /*dragging*/
        131072 && (t = !0, o.dragging = /*dragging*/
        s[17], mr(() => t = !1)), e.$set(o);
      },
      i(s) {
        n || (_e(e.$$.fragment, s), n = !0);
      },
      o(s) {
        ue(e.$$.fragment, s), n = !1;
      },
      d(s) {
        nt(e, s);
      }
    }
  );
}
function Er(l) {
  let e, t, n;
  var i = (
    /*Canvas3DComponent*/
    l[19]
  );
  function a(s, r) {
    return { props: {
      value: (
        /*value*/
        s[0]
      ),
      env_map: (
        /*env_map*/
        s[1]
      ),
      tonemapping: (
        /*tonemapping*/
        s[2]
      ),
      exposure: (
        /*exposure*/
        s[3]
      ),
      contrast: (
        /*contrast*/
        s[4]
      ),
      clear_color: (
        /*clear_color*/
        s[5]
      ),
      camera_position: (
        /*camera_position*/
        s[13]
      ),
      zoom_speed: (
        /*zoom_speed*/
        s[10]
      ),
      pan_speed: (
        /*pan_speed*/
        s[11]
      )
    } };
  }
  return i && (e = Xt(i, a(l)), l[27](e)), {
    c() {
      e && tt(e.$$.fragment), t = Pn();
    },
    m(s, r) {
      e && lt(e, s, r), Ct(s, t, r), n = !0;
    },
    p(s, r) {
      if (r[0] & /*Canvas3DComponent*/
      524288 && i !== (i = /*Canvas3DComponent*/
      s[19])) {
        if (e) {
          tn();
          const o = e;
          ue(o.$$.fragment, 1, 0, () => {
            nt(o, 1);
          }), en();
        }
        i ? (e = Xt(i, a(s)), s[27](e), tt(e.$$.fragment), _e(e.$$.fragment, 1), lt(e, t.parentNode, t)) : e = null;
      } else if (i) {
        const o = {};
        r[0] & /*value*/
        1 && (o.value = /*value*/
        s[0]), r[0] & /*env_map*/
        2 && (o.env_map = /*env_map*/
        s[1]), r[0] & /*tonemapping*/
        4 && (o.tonemapping = /*tonemapping*/
        s[2]), r[0] & /*exposure*/
        8 && (o.exposure = /*exposure*/
        s[3]), r[0] & /*contrast*/
        16 && (o.contrast = /*contrast*/
        s[4]), r[0] & /*clear_color*/
        32 && (o.clear_color = /*clear_color*/
        s[5]), r[0] & /*camera_position*/
        8192 && (o.camera_position = /*camera_position*/
        s[13]), r[0] & /*zoom_speed*/
        1024 && (o.zoom_speed = /*zoom_speed*/
        s[10]), r[0] & /*pan_speed*/
        2048 && (o.pan_speed = /*pan_speed*/
        s[11]), e.$set(o);
      }
    },
    i(s) {
      n || (e && _e(e.$$.fragment, s), n = !0);
    },
    o(s) {
      e && ue(e.$$.fragment, s), n = !1;
    },
    d(s) {
      s && zt(t), l[27](null), e && nt(e, s);
    }
  };
}
function Fr(l) {
  let e, t, n;
  var i = (
    /*Canvas3DGSComponent*/
    l[18]
  );
  function a(s, r) {
    return {
      props: {
        value: (
          /*value*/
          s[0]
        ),
        zoom_speed: (
          /*zoom_speed*/
          s[10]
        ),
        pan_speed: (
          /*pan_speed*/
          s[11]
        )
      }
    };
  }
  return i && (e = Xt(i, a(l))), {
    c() {
      e && tt(e.$$.fragment), t = Pn();
    },
    m(s, r) {
      e && lt(e, s, r), Ct(s, t, r), n = !0;
    },
    p(s, r) {
      if (r[0] & /*Canvas3DGSComponent*/
      262144 && i !== (i = /*Canvas3DGSComponent*/
      s[18])) {
        if (e) {
          tn();
          const o = e;
          ue(o.$$.fragment, 1, 0, () => {
            nt(o, 1);
          }), en();
        }
        i ? (e = Xt(i, a(s)), tt(e.$$.fragment), _e(e.$$.fragment, 1), lt(e, t.parentNode, t)) : e = null;
      } else if (i) {
        const o = {};
        r[0] & /*value*/
        1 && (o.value = /*value*/
        s[0]), r[0] & /*zoom_speed*/
        1024 && (o.zoom_speed = /*zoom_speed*/
        s[10]), r[0] & /*pan_speed*/
        2048 && (o.pan_speed = /*pan_speed*/
        s[11]), e.$set(o);
      }
    },
    i(s) {
      n || (e && _e(e.$$.fragment, s), n = !0);
    },
    o(s) {
      e && ue(e.$$.fragment, s), n = !1;
    },
    d(s) {
      s && zt(t), e && nt(e, s);
    }
  };
}
function Mr(l) {
  let e;
  const t = (
    /*#slots*/
    l[24].default
  ), n = wr(
    t,
    l,
    /*$$scope*/
    l[28],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, a) {
      n && n.m(i, a), e = !0;
    },
    p(i, a) {
      n && n.p && (!e || a[0] & /*$$scope*/
      268435456) && qr(
        n,
        t,
        i,
        /*$$scope*/
        i[28],
        e ? yr(
          t,
          /*$$scope*/
          i[28],
          a,
          null
        ) : kr(
          /*$$scope*/
          i[28]
        ),
        null
      );
    },
    i(i) {
      e || (_e(n, i), e = !0);
    },
    o(i) {
      ue(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function jr(l) {
  let e, t, n, i, a, s;
  e = new An({
    props: {
      show_label: (
        /*show_label*/
        l[7]
      ),
      Icon: Kt,
      label: (
        /*label*/
        l[6] || "3D Model"
      )
    }
  });
  const r = [Dr, Lr], o = [];
  function f(_, u) {
    return (
      /*value*/
      _[0] === null ? 0 : 1
    );
  }
  return n = f(l), i = o[n] = r[n](l), {
    c() {
      tt(e.$$.fragment), t = vi(), i.c(), a = Pn();
    },
    m(_, u) {
      lt(e, _, u), Ct(_, t, u), o[n].m(_, u), Ct(_, a, u), s = !0;
    },
    p(_, u) {
      const d = {};
      u[0] & /*show_label*/
      128 && (d.show_label = /*show_label*/
      _[7]), u[0] & /*label*/
      64 && (d.label = /*label*/
      _[6] || "3D Model"), e.$set(d);
      let c = n;
      n = f(_), n === c ? o[n].p(_, u) : (tn(), ue(o[c], 1, 1, () => {
        o[c] = null;
      }), en(), i = o[n], i ? i.p(_, u) : (i = o[n] = r[n](_), i.c()), _e(i, 1), i.m(a.parentNode, a));
    },
    i(_) {
      s || (_e(e.$$.fragment, _), _e(i), s = !0);
    },
    o(_) {
      ue(e.$$.fragment, _), ue(i), s = !1;
    },
    d(_) {
      _ && (zt(t), zt(a)), nt(e, _), o[n].d(_);
    }
  };
}
function Ir(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  var a = this && this.__awaiter || function(z, ie, oe, P) {
    function Ee(C) {
      return C instanceof oe ? C : new oe(function(Ie) {
        Ie(C);
      });
    }
    return new (oe || (oe = Promise))(function(C, Ie) {
      function w(V) {
        try {
          R(P.next(V));
        } catch (T) {
          Ie(T);
        }
      }
      function M(V) {
        try {
          R(P.throw(V));
        } catch (T) {
          Ie(T);
        }
      }
      function R(V) {
        V.done ? C(V.value) : Ee(V.value).then(w, M);
      }
      R((P = P.apply(z, ie || [])).next());
    });
  };
  let { value: s } = e, { env_map: r } = e, { tonemapping: o = null } = e, { exposure: f = 1 } = e, { contrast: _ = 1 } = e, { clear_color: u = [0, 0, 0, 0] } = e, { label: d = "" } = e, { show_label: c } = e, { root: m } = e, { i18n: h } = e, { zoom_speed: p = 1 } = e, { pan_speed: y = 1 } = e, { max_file_size: b = null } = e, { camera_position: g = [null, null, null] } = e, { upload: q } = e, { stream_handler: I } = e;
  function v(z) {
    return a(this, arguments, void 0, function* ({ detail: ie }) {
      t(0, s = ie), yield pl(), O("change", s), O("load", s);
    });
  }
  function j() {
    return a(this, void 0, void 0, function* () {
      t(0, s = null), yield pl(), O("clear"), O("change");
    });
  }
  let E = !1, N, B;
  function H() {
    return a(this, void 0, void 0, function* () {
      return (yield import("./Canvas3D-Cduz95bA.js")).default;
    });
  }
  function K() {
    return a(this, void 0, void 0, function* () {
      return (yield import("./Canvas3DGS-BNgp41cs.js")).default;
    });
  }
  let S;
  function X() {
    return a(this, void 0, void 0, function* () {
      S == null || S.reset_camera_position(g, p, y);
    });
  }
  const O = Sr();
  let U = !1;
  function k(z) {
    U = z, t(17, U);
  }
  function de(z) {
    pr.call(this, l, z);
  }
  function me(z) {
    wi[z ? "unshift" : "push"](() => {
      S = z, t(20, S);
    });
  }
  return l.$$set = (z) => {
    "value" in z && t(0, s = z.value), "env_map" in z && t(1, r = z.env_map), "tonemapping" in z && t(2, o = z.tonemapping), "exposure" in z && t(3, f = z.exposure), "contrast" in z && t(4, _ = z.contrast), "clear_color" in z && t(5, u = z.clear_color), "label" in z && t(6, d = z.label), "show_label" in z && t(7, c = z.show_label), "root" in z && t(8, m = z.root), "i18n" in z && t(9, h = z.i18n), "zoom_speed" in z && t(10, p = z.zoom_speed), "pan_speed" in z && t(11, y = z.pan_speed), "max_file_size" in z && t(12, b = z.max_file_size), "camera_position" in z && t(13, g = z.camera_position), "upload" in z && t(14, q = z.upload), "stream_handler" in z && t(15, I = z.stream_handler), "$$scope" in z && t(28, i = z.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value, use_3dgs*/
    65537 && s && (t(16, E = s.path.endsWith(".splat") || s.path.endsWith(".ply")), E ? K().then((z) => {
      t(18, N = z);
    }) : H().then((z) => {
      t(19, B = z);
    })), l.$$.dirty[0] & /*dragging*/
    131072 && O("drag", U);
  }, [
    s,
    r,
    o,
    f,
    _,
    u,
    d,
    c,
    m,
    h,
    p,
    y,
    b,
    g,
    q,
    I,
    E,
    U,
    N,
    B,
    S,
    v,
    j,
    X,
    n,
    k,
    de,
    me,
    i
  ];
}
class Nr extends dr {
  constructor(e) {
    super(), zr(
      this,
      e,
      Ir,
      jr,
      Cr,
      {
        value: 0,
        env_map: 1,
        tonemapping: 2,
        exposure: 3,
        contrast: 4,
        clear_color: 5,
        label: 6,
        show_label: 7,
        root: 8,
        i18n: 9,
        zoom_speed: 10,
        pan_speed: 11,
        max_file_size: 12,
        camera_position: 13,
        upload: 14,
        stream_handler: 15
      },
      null,
      [-1, -1]
    );
  }
}
function ut(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Bt() {
}
function Ur(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const ki = typeof window < "u";
let wl = ki ? () => window.performance.now() : () => Date.now(), yi = ki ? (l) => requestAnimationFrame(l) : Bt;
const ct = /* @__PURE__ */ new Set();
function zi(l) {
  ct.forEach((e) => {
    e.c(l) || (ct.delete(e), e.f());
  }), ct.size !== 0 && yi(zi);
}
function Vr(l) {
  let e;
  return ct.size === 0 && yi(zi), {
    promise: new Promise((t) => {
      ct.add(e = { c: l, f: t });
    }),
    abort() {
      ct.delete(e);
    }
  };
}
const rt = [];
function Ar(l, e = Bt) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(r) {
    if (Ur(l, r) && (l = r, t)) {
      const o = !rt.length;
      for (const f of n)
        f[1](), rt.push(f, l);
      if (o) {
        for (let f = 0; f < rt.length; f += 2)
          rt[f][0](rt[f + 1]);
        rt.length = 0;
      }
    }
  }
  function a(r) {
    i(r(l));
  }
  function s(r, o = Bt) {
    const f = [r, o];
    return n.add(f), n.size === 1 && (t = e(i, a) || Bt), r(l), () => {
      n.delete(f), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: a, subscribe: s };
}
function vl(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function In(l, e, t, n) {
  if (typeof t == "number" || vl(t)) {
    const i = n - t, a = (t - e) / (l.dt || 1 / 60), s = l.opts.stiffness * i, r = l.opts.damping * a, o = (s - r) * l.inv_mass, f = (a + o) * l.dt;
    return Math.abs(f) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, vl(t) ? new Date(t.getTime() + f) : t + f);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, a) => In(l, e[a], t[a], n[a])
      );
    if (typeof t == "object") {
      const i = {};
      for (const a in t)
        i[a] = In(l, e[a], t[a], n[a]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function kl(l, e = {}) {
  const t = Ar(l), { stiffness: n = 0.15, damping: i = 0.8, precision: a = 0.01 } = e;
  let s, r, o, f = l, _ = l, u = 1, d = 0, c = !1;
  function m(p, y = {}) {
    _ = p;
    const b = o = {};
    return l == null || y.hard || h.stiffness >= 1 && h.damping >= 1 ? (c = !0, s = wl(), f = p, t.set(l = _), Promise.resolve()) : (y.soft && (d = 1 / ((y.soft === !0 ? 0.5 : +y.soft) * 60), u = 0), r || (s = wl(), c = !1, r = Vr((g) => {
      if (c)
        return c = !1, r = null, !1;
      u = Math.min(u + d, 1);
      const q = {
        inv_mass: u,
        opts: h,
        settled: !0,
        dt: (g - s) * 60 / 1e3
      }, I = In(q, f, l, _);
      return s = g, f = l, t.set(l = I), q.settled && (r = null), !q.settled;
    })), new Promise((g) => {
      r.promise.then(() => {
        b === o && g();
      });
    }));
  }
  const h = {
    set: m,
    update: (p, y) => m(p(_, l), y),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: a
  };
  return h;
}
const {
  SvelteComponent: Rr,
  append: be,
  attr: F,
  component_subscribe: yl,
  detach: Br,
  element: Or,
  init: Tr,
  insert: Wr,
  noop: zl,
  safe_not_equal: Pr,
  set_style: Ut,
  svg_element: pe,
  toggle_class: Cl
} = window.__gradio__svelte__internal, { onMount: Zr } = window.__gradio__svelte__internal;
function Gr(l) {
  let e, t, n, i, a, s, r, o, f, _, u, d;
  return {
    c() {
      e = Or("div"), t = pe("svg"), n = pe("g"), i = pe("path"), a = pe("path"), s = pe("path"), r = pe("path"), o = pe("g"), f = pe("path"), _ = pe("path"), u = pe("path"), d = pe("path"), F(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), F(i, "fill", "#FF7C00"), F(i, "fill-opacity", "0.4"), F(i, "class", "svelte-43sxxs"), F(a, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), F(a, "fill", "#FF7C00"), F(a, "class", "svelte-43sxxs"), F(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), F(s, "fill", "#FF7C00"), F(s, "fill-opacity", "0.4"), F(s, "class", "svelte-43sxxs"), F(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), F(r, "fill", "#FF7C00"), F(r, "class", "svelte-43sxxs"), Ut(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), F(f, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), F(f, "fill", "#FF7C00"), F(f, "fill-opacity", "0.4"), F(f, "class", "svelte-43sxxs"), F(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), F(_, "fill", "#FF7C00"), F(_, "class", "svelte-43sxxs"), F(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), F(u, "fill", "#FF7C00"), F(u, "fill-opacity", "0.4"), F(u, "class", "svelte-43sxxs"), F(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), F(d, "fill", "#FF7C00"), F(d, "class", "svelte-43sxxs"), Ut(o, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), F(t, "viewBox", "-1200 -1200 3000 3000"), F(t, "fill", "none"), F(t, "xmlns", "http://www.w3.org/2000/svg"), F(t, "class", "svelte-43sxxs"), F(e, "class", "svelte-43sxxs"), Cl(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(c, m) {
      Wr(c, e, m), be(e, t), be(t, n), be(n, i), be(n, a), be(n, s), be(n, r), be(t, o), be(o, f), be(o, _), be(o, u), be(o, d);
    },
    p(c, [m]) {
      m & /*$top*/
      2 && Ut(n, "transform", "translate(" + /*$top*/
      c[1][0] + "px, " + /*$top*/
      c[1][1] + "px)"), m & /*$bottom*/
      4 && Ut(o, "transform", "translate(" + /*$bottom*/
      c[2][0] + "px, " + /*$bottom*/
      c[2][1] + "px)"), m & /*margin*/
      1 && Cl(
        e,
        "margin",
        /*margin*/
        c[0]
      );
    },
    i: zl,
    o: zl,
    d(c) {
      c && Br(e);
    }
  };
}
function Hr(l, e, t) {
  let n, i;
  var a = this && this.__awaiter || function(c, m, h, p) {
    function y(b) {
      return b instanceof h ? b : new h(function(g) {
        g(b);
      });
    }
    return new (h || (h = Promise))(function(b, g) {
      function q(j) {
        try {
          v(p.next(j));
        } catch (E) {
          g(E);
        }
      }
      function I(j) {
        try {
          v(p.throw(j));
        } catch (E) {
          g(E);
        }
      }
      function v(j) {
        j.done ? b(j.value) : y(j.value).then(q, I);
      }
      v((p = p.apply(c, m || [])).next());
    });
  };
  let { margin: s = !0 } = e;
  const r = kl([0, 0]);
  yl(l, r, (c) => t(1, n = c));
  const o = kl([0, 0]);
  yl(l, o, (c) => t(2, i = c));
  let f;
  function _() {
    return a(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), o.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), o.set([125, -140])]), yield Promise.all([r.set([-125, 0]), o.set([125, -0])]), yield Promise.all([r.set([125, 0]), o.set([-125, 0])]);
    });
  }
  function u() {
    return a(this, void 0, void 0, function* () {
      yield _(), f || u();
    });
  }
  function d() {
    return a(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), o.set([-125, 0])]), u();
    });
  }
  return Zr(() => (d(), () => f = !0)), l.$$set = (c) => {
    "margin" in c && t(0, s = c.margin);
  }, [s, n, i, r, o];
}
class Xr extends Rr {
  constructor(e) {
    super(), Tr(this, e, Hr, Gr, Pr, { margin: 0 });
  }
}
const {
  SvelteComponent: Yr,
  append: Ye,
  attr: ke,
  binding_callbacks: ql,
  check_outros: Nn,
  create_component: Ci,
  create_slot: qi,
  destroy_component: Si,
  destroy_each: Li,
  detach: L,
  element: Ce,
  empty: dt,
  ensure_array_like: Yt,
  get_all_dirty_from_scope: Di,
  get_slot_changes: Ei,
  group_outros: Un,
  init: Kr,
  insert: D,
  mount_component: Fi,
  noop: Vn,
  safe_not_equal: Jr,
  set_data: ce,
  set_style: Ve,
  space: fe,
  text: A,
  toggle_class: re,
  transition_in: ve,
  transition_out: qe,
  update_slot_base: Mi
} = window.__gradio__svelte__internal, { tick: Qr } = window.__gradio__svelte__internal, { onDestroy: xr } = window.__gradio__svelte__internal, { createEventDispatcher: $r } = window.__gradio__svelte__internal, ef = (l) => ({}), Sl = (l) => ({}), tf = (l) => ({}), Ll = (l) => ({});
function Dl(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function El(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function nf(l) {
  let e, t, n, i, a = (
    /*i18n*/
    l[1]("common.error") + ""
  ), s, r, o;
  t = new it({
    props: {
      Icon: Xl,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const f = (
    /*#slots*/
    l[30].error
  ), _ = qi(
    f,
    l,
    /*$$scope*/
    l[29],
    Sl
  );
  return {
    c() {
      e = Ce("div"), Ci(t.$$.fragment), n = fe(), i = Ce("span"), s = A(a), r = fe(), _ && _.c(), ke(e, "class", "clear-status svelte-vopvsi"), ke(i, "class", "error svelte-vopvsi");
    },
    m(u, d) {
      D(u, e, d), Fi(t, e, null), D(u, n, d), D(u, i, d), Ye(i, s), D(u, r, d), _ && _.m(u, d), o = !0;
    },
    p(u, d) {
      const c = {};
      d[0] & /*i18n*/
      2 && (c.label = /*i18n*/
      u[1]("common.clear")), t.$set(c), (!o || d[0] & /*i18n*/
      2) && a !== (a = /*i18n*/
      u[1]("common.error") + "") && ce(s, a), _ && _.p && (!o || d[0] & /*$$scope*/
      536870912) && Mi(
        _,
        f,
        u,
        /*$$scope*/
        u[29],
        o ? Ei(
          f,
          /*$$scope*/
          u[29],
          d,
          ef
        ) : Di(
          /*$$scope*/
          u[29]
        ),
        Sl
      );
    },
    i(u) {
      o || (ve(t.$$.fragment, u), ve(_, u), o = !0);
    },
    o(u) {
      qe(t.$$.fragment, u), qe(_, u), o = !1;
    },
    d(u) {
      u && (L(e), L(n), L(i), L(r)), Si(t), _ && _.d(u);
    }
  };
}
function lf(l) {
  let e, t, n, i, a, s, r, o, f, _ = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Fl(l)
  );
  function u(g, q) {
    if (
      /*progress*/
      g[7]
    )
      return af;
    if (
      /*queue_position*/
      g[2] !== null && /*queue_size*/
      g[3] !== void 0 && /*queue_position*/
      g[2] >= 0
    )
      return sf;
    if (
      /*queue_position*/
      g[2] === 0
    )
      return of;
  }
  let d = u(l), c = d && d(l), m = (
    /*timer*/
    l[5] && Il(l)
  );
  const h = [uf, _f], p = [];
  function y(g, q) {
    return (
      /*last_progress_level*/
      g[15] != null ? 0 : (
        /*show_progress*/
        g[6] === "full" ? 1 : -1
      )
    );
  }
  ~(a = y(l)) && (s = p[a] = h[a](l));
  let b = !/*timer*/
  l[5] && Ol(l);
  return {
    c() {
      _ && _.c(), e = fe(), t = Ce("div"), c && c.c(), n = fe(), m && m.c(), i = fe(), s && s.c(), r = fe(), b && b.c(), o = dt(), ke(t, "class", "progress-text svelte-vopvsi"), re(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), re(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(g, q) {
      _ && _.m(g, q), D(g, e, q), D(g, t, q), c && c.m(t, null), Ye(t, n), m && m.m(t, null), D(g, i, q), ~a && p[a].m(g, q), D(g, r, q), b && b.m(g, q), D(g, o, q), f = !0;
    },
    p(g, q) {
      /*variant*/
      g[8] === "default" && /*show_eta_bar*/
      g[18] && /*show_progress*/
      g[6] === "full" ? _ ? _.p(g, q) : (_ = Fl(g), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), d === (d = u(g)) && c ? c.p(g, q) : (c && c.d(1), c = d && d(g), c && (c.c(), c.m(t, n))), /*timer*/
      g[5] ? m ? m.p(g, q) : (m = Il(g), m.c(), m.m(t, null)) : m && (m.d(1), m = null), (!f || q[0] & /*variant*/
      256) && re(
        t,
        "meta-text-center",
        /*variant*/
        g[8] === "center"
      ), (!f || q[0] & /*variant*/
      256) && re(
        t,
        "meta-text",
        /*variant*/
        g[8] === "default"
      );
      let I = a;
      a = y(g), a === I ? ~a && p[a].p(g, q) : (s && (Un(), qe(p[I], 1, 1, () => {
        p[I] = null;
      }), Nn()), ~a ? (s = p[a], s ? s.p(g, q) : (s = p[a] = h[a](g), s.c()), ve(s, 1), s.m(r.parentNode, r)) : s = null), /*timer*/
      g[5] ? b && (Un(), qe(b, 1, 1, () => {
        b = null;
      }), Nn()) : b ? (b.p(g, q), q[0] & /*timer*/
      32 && ve(b, 1)) : (b = Ol(g), b.c(), ve(b, 1), b.m(o.parentNode, o));
    },
    i(g) {
      f || (ve(s), ve(b), f = !0);
    },
    o(g) {
      qe(s), qe(b), f = !1;
    },
    d(g) {
      g && (L(e), L(t), L(i), L(r), L(o)), _ && _.d(g), c && c.d(), m && m.d(), ~a && p[a].d(g), b && b.d(g);
    }
  };
}
function Fl(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Ce("div"), ke(e, "class", "eta-bar svelte-vopvsi"), Ve(e, "transform", t);
    },
    m(n, i) {
      D(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && Ve(e, "transform", t);
    },
    d(n) {
      n && L(e);
    }
  };
}
function of(l) {
  let e;
  return {
    c() {
      e = A("processing |");
    },
    m(t, n) {
      D(t, e, n);
    },
    p: Vn,
    d(t) {
      t && L(e);
    }
  };
}
function sf(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, a, s;
  return {
    c() {
      e = A("queue: "), n = A(t), i = A("/"), a = A(
        /*queue_size*/
        l[3]
      ), s = A(" |");
    },
    m(r, o) {
      D(r, e, o), D(r, n, o), D(r, i, o), D(r, a, o), D(r, s, o);
    },
    p(r, o) {
      o[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && ce(n, t), o[0] & /*queue_size*/
      8 && ce(
        a,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (L(e), L(n), L(i), L(a), L(s));
    }
  };
}
function af(l) {
  let e, t = Yt(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = jl(El(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = dt();
    },
    m(i, a) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, a);
      D(i, e, a);
    },
    p(i, a) {
      if (a[0] & /*progress*/
      128) {
        t = Yt(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = El(i, t, s);
          n[s] ? n[s].p(r, a) : (n[s] = jl(r), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && L(e), Li(n, i);
    }
  };
}
function Ml(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, a = " ", s;
  function r(_, u) {
    return (
      /*p*/
      _[41].length != null ? ff : rf
    );
  }
  let o = r(l), f = o(l);
  return {
    c() {
      f.c(), e = fe(), n = A(t), i = A(" | "), s = A(a);
    },
    m(_, u) {
      f.m(_, u), D(_, e, u), D(_, n, u), D(_, i, u), D(_, s, u);
    },
    p(_, u) {
      o === (o = r(_)) && f ? f.p(_, u) : (f.d(1), f = o(_), f && (f.c(), f.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && ce(n, t);
    },
    d(_) {
      _ && (L(e), L(n), L(i), L(s)), f.d(_);
    }
  };
}
function rf(l) {
  let e = ut(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = A(e);
    },
    m(n, i) {
      D(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = ut(
        /*p*/
        n[41].index || 0
      ) + "") && ce(t, e);
    },
    d(n) {
      n && L(t);
    }
  };
}
function ff(l) {
  let e = ut(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = ut(
    /*p*/
    l[41].length
  ) + "", a;
  return {
    c() {
      t = A(e), n = A("/"), a = A(i);
    },
    m(s, r) {
      D(s, t, r), D(s, n, r), D(s, a, r);
    },
    p(s, r) {
      r[0] & /*progress*/
      128 && e !== (e = ut(
        /*p*/
        s[41].index || 0
      ) + "") && ce(t, e), r[0] & /*progress*/
      128 && i !== (i = ut(
        /*p*/
        s[41].length
      ) + "") && ce(a, i);
    },
    d(s) {
      s && (L(t), L(n), L(a));
    }
  };
}
function jl(l) {
  let e, t = (
    /*p*/
    l[41].index != null && Ml(l)
  );
  return {
    c() {
      t && t.c(), e = dt();
    },
    m(n, i) {
      t && t.m(n, i), D(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = Ml(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && L(e), t && t.d(n);
    }
  };
}
function Il(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = A(
        /*formatted_timer*/
        l[20]
      ), n = A(t), i = A("s");
    },
    m(a, s) {
      D(a, e, s), D(a, n, s), D(a, i, s);
    },
    p(a, s) {
      s[0] & /*formatted_timer*/
      1048576 && ce(
        e,
        /*formatted_timer*/
        a[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      a[0] ? `/${/*formatted_eta*/
      a[19]}` : "") && ce(n, t);
    },
    d(a) {
      a && (L(e), L(n), L(i));
    }
  };
}
function _f(l) {
  let e, t;
  return e = new Xr({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Ci(e.$$.fragment);
    },
    m(n, i) {
      Fi(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i[0] & /*variant*/
      256 && (a.margin = /*variant*/
      n[8] === "default"), e.$set(a);
    },
    i(n) {
      t || (ve(e.$$.fragment, n), t = !0);
    },
    o(n) {
      qe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Si(e, n);
    }
  };
}
function uf(l) {
  let e, t, n, i, a, s = `${/*last_progress_level*/
  l[15] * 100}%`, r = (
    /*progress*/
    l[7] != null && Nl(l)
  );
  return {
    c() {
      e = Ce("div"), t = Ce("div"), r && r.c(), n = fe(), i = Ce("div"), a = Ce("div"), ke(t, "class", "progress-level-inner svelte-vopvsi"), ke(a, "class", "progress-bar svelte-vopvsi"), Ve(a, "width", s), ke(i, "class", "progress-bar-wrap svelte-vopvsi"), ke(e, "class", "progress-level svelte-vopvsi");
    },
    m(o, f) {
      D(o, e, f), Ye(e, t), r && r.m(t, null), Ye(e, n), Ye(e, i), Ye(i, a), l[31](a);
    },
    p(o, f) {
      /*progress*/
      o[7] != null ? r ? r.p(o, f) : (r = Nl(o), r.c(), r.m(t, null)) : r && (r.d(1), r = null), f[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      o[15] * 100}%`) && Ve(a, "width", s);
    },
    i: Vn,
    o: Vn,
    d(o) {
      o && L(e), r && r.d(), l[31](null);
    }
  };
}
function Nl(l) {
  let e, t = Yt(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Bl(Dl(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = dt();
    },
    m(i, a) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, a);
      D(i, e, a);
    },
    p(i, a) {
      if (a[0] & /*progress_level, progress*/
      16512) {
        t = Yt(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = Dl(i, t, s);
          n[s] ? n[s].p(r, a) : (n[s] = Bl(r), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && L(e), Li(n, i);
    }
  };
}
function Ul(l) {
  let e, t, n, i, a = (
    /*i*/
    l[43] !== 0 && cf()
  ), s = (
    /*p*/
    l[41].desc != null && Vl(l)
  ), r = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && Al()
  ), o = (
    /*progress_level*/
    l[14] != null && Rl(l)
  );
  return {
    c() {
      a && a.c(), e = fe(), s && s.c(), t = fe(), r && r.c(), n = fe(), o && o.c(), i = dt();
    },
    m(f, _) {
      a && a.m(f, _), D(f, e, _), s && s.m(f, _), D(f, t, _), r && r.m(f, _), D(f, n, _), o && o.m(f, _), D(f, i, _);
    },
    p(f, _) {
      /*p*/
      f[41].desc != null ? s ? s.p(f, _) : (s = Vl(f), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      f[41].desc != null && /*progress_level*/
      f[14] && /*progress_level*/
      f[14][
        /*i*/
        f[43]
      ] != null ? r || (r = Al(), r.c(), r.m(n.parentNode, n)) : r && (r.d(1), r = null), /*progress_level*/
      f[14] != null ? o ? o.p(f, _) : (o = Rl(f), o.c(), o.m(i.parentNode, i)) : o && (o.d(1), o = null);
    },
    d(f) {
      f && (L(e), L(t), L(n), L(i)), a && a.d(f), s && s.d(f), r && r.d(f), o && o.d(f);
    }
  };
}
function cf(l) {
  let e;
  return {
    c() {
      e = A(" /");
    },
    m(t, n) {
      D(t, e, n);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Vl(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = A(e);
    },
    m(n, i) {
      D(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && ce(t, e);
    },
    d(n) {
      n && L(t);
    }
  };
}
function Al(l) {
  let e;
  return {
    c() {
      e = A("-");
    },
    m(t, n) {
      D(t, e, n);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Rl(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = A(e), n = A("%");
    },
    m(i, a) {
      D(i, t, a), D(i, n, a);
    },
    p(i, a) {
      a[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && ce(t, e);
    },
    d(i) {
      i && (L(t), L(n));
    }
  };
}
function Bl(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && Ul(l)
  );
  return {
    c() {
      t && t.c(), e = dt();
    },
    m(n, i) {
      t && t.m(n, i), D(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = Ul(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && L(e), t && t.d(n);
    }
  };
}
function Ol(l) {
  let e, t, n, i;
  const a = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), s = qi(
    a,
    l,
    /*$$scope*/
    l[29],
    Ll
  );
  return {
    c() {
      e = Ce("p"), t = A(
        /*loading_text*/
        l[9]
      ), n = fe(), s && s.c(), ke(e, "class", "loading svelte-vopvsi");
    },
    m(r, o) {
      D(r, e, o), Ye(e, t), D(r, n, o), s && s.m(r, o), i = !0;
    },
    p(r, o) {
      (!i || o[0] & /*loading_text*/
      512) && ce(
        t,
        /*loading_text*/
        r[9]
      ), s && s.p && (!i || o[0] & /*$$scope*/
      536870912) && Mi(
        s,
        a,
        r,
        /*$$scope*/
        r[29],
        i ? Ei(
          a,
          /*$$scope*/
          r[29],
          o,
          tf
        ) : Di(
          /*$$scope*/
          r[29]
        ),
        Ll
      );
    },
    i(r) {
      i || (ve(s, r), i = !0);
    },
    o(r) {
      qe(s, r), i = !1;
    },
    d(r) {
      r && (L(e), L(n)), s && s.d(r);
    }
  };
}
function df(l) {
  let e, t, n, i, a;
  const s = [lf, nf], r = [];
  function o(f, _) {
    return (
      /*status*/
      f[4] === "pending" ? 0 : (
        /*status*/
        f[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = o(l)) && (n = r[t] = s[t](l)), {
    c() {
      e = Ce("div"), n && n.c(), ke(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-vopvsi"), re(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), re(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), re(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), re(
        e,
        "border",
        /*border*/
        l[12]
      ), Ve(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), Ve(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(f, _) {
      D(f, e, _), ~t && r[t].m(e, null), l[33](e), a = !0;
    },
    p(f, _) {
      let u = t;
      t = o(f), t === u ? ~t && r[t].p(f, _) : (n && (Un(), qe(r[u], 1, 1, () => {
        r[u] = null;
      }), Nn()), ~t ? (n = r[t], n ? n.p(f, _) : (n = r[t] = s[t](f), n.c()), ve(n, 1), n.m(e, null)) : n = null), (!a || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      f[8] + " " + /*show_progress*/
      f[6] + " svelte-vopvsi")) && ke(e, "class", i), (!a || _[0] & /*variant, show_progress, status, show_progress*/
      336) && re(e, "hide", !/*status*/
      f[4] || /*status*/
      f[4] === "complete" || /*show_progress*/
      f[6] === "hidden"), (!a || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && re(
        e,
        "translucent",
        /*variant*/
        f[8] === "center" && /*status*/
        (f[4] === "pending" || /*status*/
        f[4] === "error") || /*translucent*/
        f[11] || /*show_progress*/
        f[6] === "minimal"
      ), (!a || _[0] & /*variant, show_progress, status*/
      336) && re(
        e,
        "generating",
        /*status*/
        f[4] === "generating"
      ), (!a || _[0] & /*variant, show_progress, border*/
      4416) && re(
        e,
        "border",
        /*border*/
        f[12]
      ), _[0] & /*absolute*/
      1024 && Ve(
        e,
        "position",
        /*absolute*/
        f[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && Ve(
        e,
        "padding",
        /*absolute*/
        f[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(f) {
      a || (ve(n), a = !0);
    },
    o(f) {
      qe(n), a = !1;
    },
    d(f) {
      f && L(e), ~t && r[t].d(), l[33](null);
    }
  };
}
var mf = function(l, e, t, n) {
  function i(a) {
    return a instanceof t ? a : new t(function(s) {
      s(a);
    });
  }
  return new (t || (t = Promise))(function(a, s) {
    function r(_) {
      try {
        f(n.next(_));
      } catch (u) {
        s(u);
      }
    }
    function o(_) {
      try {
        f(n.throw(_));
      } catch (u) {
        s(u);
      }
    }
    function f(_) {
      _.done ? a(_.value) : i(_.value).then(r, o);
    }
    f((n = n.apply(l, e || [])).next());
  });
};
let Vt = [], zn = !1;
function hf(l) {
  return mf(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Vt.push(e), !zn)
        zn = !0;
      else
        return;
      yield Qr(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < Vt.length; i++) {
          const s = Vt[i].getBoundingClientRect();
          (i === 0 || s.top + window.scrollY <= n[0]) && (n[0] = s.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), zn = !1, Vt = [];
      });
    }
  });
}
function gf(l, e, t) {
  let n, { $$slots: i = {}, $$scope: a } = e;
  this && this.__awaiter;
  const s = $r();
  let { i18n: r } = e, { eta: o = null } = e, { queue_position: f } = e, { queue_size: _ } = e, { status: u } = e, { scroll_to_output: d = !1 } = e, { timer: c = !0 } = e, { show_progress: m = "full" } = e, { message: h = null } = e, { progress: p = null } = e, { variant: y = "default" } = e, { loading_text: b = "Loading..." } = e, { absolute: g = !0 } = e, { translucent: q = !1 } = e, { border: I = !1 } = e, { autoscroll: v } = e, j, E = !1, N = 0, B = 0, H = null, K = null, S = 0, X = null, O, U = null, k = !0;
  const de = () => {
    t(0, o = t(27, H = t(19, ie = null))), t(25, N = performance.now()), t(26, B = 0), E = !0, me();
  };
  function me() {
    requestAnimationFrame(() => {
      t(26, B = (performance.now() - N) / 1e3), E && me();
    });
  }
  function z() {
    t(26, B = 0), t(0, o = t(27, H = t(19, ie = null))), E && (E = !1);
  }
  xr(() => {
    E && z();
  });
  let ie = null;
  function oe(C) {
    ql[C ? "unshift" : "push"](() => {
      U = C, t(16, U), t(7, p), t(14, X), t(15, O);
    });
  }
  const P = () => {
    s("clear_status");
  };
  function Ee(C) {
    ql[C ? "unshift" : "push"](() => {
      j = C, t(13, j);
    });
  }
  return l.$$set = (C) => {
    "i18n" in C && t(1, r = C.i18n), "eta" in C && t(0, o = C.eta), "queue_position" in C && t(2, f = C.queue_position), "queue_size" in C && t(3, _ = C.queue_size), "status" in C && t(4, u = C.status), "scroll_to_output" in C && t(22, d = C.scroll_to_output), "timer" in C && t(5, c = C.timer), "show_progress" in C && t(6, m = C.show_progress), "message" in C && t(23, h = C.message), "progress" in C && t(7, p = C.progress), "variant" in C && t(8, y = C.variant), "loading_text" in C && t(9, b = C.loading_text), "absolute" in C && t(10, g = C.absolute), "translucent" in C && t(11, q = C.translucent), "border" in C && t(12, I = C.border), "autoscroll" in C && t(24, v = C.autoscroll), "$$scope" in C && t(29, a = C.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (o === null && t(0, o = H), o != null && H !== o && (t(28, K = (performance.now() - N) / 1e3 + o), t(19, ie = K.toFixed(1)), t(27, H = o))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, S = K === null || K <= 0 || !B ? null : Math.min(B / K, 1)), l.$$.dirty[0] & /*progress*/
    128 && p != null && t(18, k = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (p != null ? t(14, X = p.map((C) => {
      if (C.index != null && C.length != null)
        return C.index / C.length;
      if (C.progress != null)
        return C.progress;
    })) : t(14, X = null), X ? (t(15, O = X[X.length - 1]), U && (O === 0 ? t(16, U.style.transition = "0", U) : t(16, U.style.transition = "150ms", U))) : t(15, O = void 0)), l.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? de() : z()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && j && d && (u === "pending" || u === "complete") && hf(j, v), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = B.toFixed(1));
  }, [
    o,
    r,
    f,
    _,
    u,
    c,
    m,
    p,
    y,
    b,
    g,
    q,
    I,
    j,
    X,
    O,
    U,
    S,
    k,
    ie,
    n,
    s,
    d,
    h,
    v,
    N,
    B,
    H,
    K,
    a,
    i,
    oe,
    P,
    Ee
  ];
}
class ji extends Yr {
  constructor(e) {
    super(), Kr(
      this,
      e,
      gf,
      df,
      Jr,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: bf,
  append: pf,
  attr: wf,
  detach: vf,
  element: kf,
  init: yf,
  insert: zf,
  noop: Tl,
  safe_not_equal: Cf,
  set_data: qf,
  text: Sf,
  toggle_class: ft
} = window.__gradio__svelte__internal;
function Lf(l) {
  let e, t = (
    /*value*/
    (l[0] ? (
      /*value*/
      l[0]
    ) : "") + ""
  ), n;
  return {
    c() {
      e = kf("div"), n = Sf(t), wf(e, "class", "svelte-1gecy8w"), ft(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), ft(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), ft(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    m(i, a) {
      zf(i, e, a), pf(e, n);
    },
    p(i, [a]) {
      a & /*value*/
      1 && t !== (t = /*value*/
      (i[0] ? (
        /*value*/
        i[0]
      ) : "") + "") && qf(n, t), a & /*type*/
      2 && ft(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), a & /*type*/
      2 && ft(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), a & /*selected*/
      4 && ft(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    i: Tl,
    o: Tl,
    d(i) {
      i && vf(e);
    }
  };
}
function Df(l, e, t) {
  let { value: n } = e, { type: i } = e, { selected: a = !1 } = e;
  return l.$$set = (s) => {
    "value" in s && t(0, n = s.value), "type" in s && t(1, i = s.type), "selected" in s && t(2, a = s.selected);
  }, [n, i, a];
}
class Hf extends bf {
  constructor(e) {
    super(), yf(this, e, Df, Lf, Cf, { value: 0, type: 1, selected: 2 });
  }
}
const {
  SvelteComponent: Ef,
  assign: Ii,
  check_outros: Ni,
  create_component: Se,
  destroy_component: Le,
  detach: qt,
  empty: Ui,
  get_spread_object: Vi,
  get_spread_update: Ai,
  group_outros: Ri,
  init: Ff,
  insert: St,
  mount_component: De,
  safe_not_equal: Mf,
  space: Zn,
  transition_in: $,
  transition_out: ee
} = window.__gradio__svelte__internal;
function jf(l) {
  let e, t;
  return e = new Zl({
    props: {
      visible: (
        /*visible*/
        l[4]
      ),
      variant: (
        /*value*/
        l[0] === null ? "dashed" : "solid"
      ),
      border_mode: (
        /*dragging*/
        l[21] ? "focus" : "base"
      ),
      padding: !1,
      elem_id: (
        /*elem_id*/
        l[2]
      ),
      elem_classes: (
        /*elem_classes*/
        l[3]
      ),
      container: (
        /*container*/
        l[13]
      ),
      scale: (
        /*scale*/
        l[14]
      ),
      min_width: (
        /*min_width*/
        l[15]
      ),
      height: (
        /*height*/
        l[17]
      ),
      $$slots: { default: [Uf] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Se(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*visible*/
      16 && (a.visible = /*visible*/
      n[4]), i & /*value*/
      1 && (a.variant = /*value*/
      n[0] === null ? "dashed" : "solid"), i & /*dragging*/
      2097152 && (a.border_mode = /*dragging*/
      n[21] ? "focus" : "base"), i & /*elem_id*/
      4 && (a.elem_id = /*elem_id*/
      n[2]), i & /*elem_classes*/
      8 && (a.elem_classes = /*elem_classes*/
      n[3]), i & /*container*/
      8192 && (a.container = /*container*/
      n[13]), i & /*scale*/
      16384 && (a.scale = /*scale*/
      n[14]), i & /*min_width*/
      32768 && (a.min_width = /*min_width*/
      n[15]), i & /*height*/
      131072 && (a.height = /*height*/
      n[17]), i & /*$$scope, label, show_label, root, env_map, tonemapping, exposure, contrast, clear_color, value, camera_position, zoom_speed, gradio, dragging, loading_status*/
      1076699107 && (a.$$scope = { dirty: i, ctx: n }), e.$set(a);
    },
    i(n) {
      t || ($(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Le(e, n);
    }
  };
}
function If(l) {
  let e, t;
  return e = new Zl({
    props: {
      visible: (
        /*visible*/
        l[4]
      ),
      variant: (
        /*value*/
        l[0] === null ? "dashed" : "solid"
      ),
      border_mode: (
        /*dragging*/
        l[21] ? "focus" : "base"
      ),
      padding: !1,
      elem_id: (
        /*elem_id*/
        l[2]
      ),
      elem_classes: (
        /*elem_classes*/
        l[3]
      ),
      container: (
        /*container*/
        l[13]
      ),
      scale: (
        /*scale*/
        l[14]
      ),
      min_width: (
        /*min_width*/
        l[15]
      ),
      height: (
        /*height*/
        l[17]
      ),
      $$slots: { default: [Bf] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Se(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*visible*/
      16 && (a.visible = /*visible*/
      n[4]), i & /*value*/
      1 && (a.variant = /*value*/
      n[0] === null ? "dashed" : "solid"), i & /*dragging*/
      2097152 && (a.border_mode = /*dragging*/
      n[21] ? "focus" : "base"), i & /*elem_id*/
      4 && (a.elem_id = /*elem_id*/
      n[2]), i & /*elem_classes*/
      8 && (a.elem_classes = /*elem_classes*/
      n[3]), i & /*container*/
      8192 && (a.container = /*container*/
      n[13]), i & /*scale*/
      16384 && (a.scale = /*scale*/
      n[14]), i & /*min_width*/
      32768 && (a.min_width = /*min_width*/
      n[15]), i & /*height*/
      131072 && (a.height = /*height*/
      n[17]), i & /*$$scope, value, gradio, env_map, tonemapping, exposure, contrast, clear_color, label, show_label, camera_position, zoom_speed, loading_status*/
      1074601923 && (a.$$scope = { dirty: i, ctx: n }), e.$set(a);
    },
    i(n) {
      t || ($(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Le(e, n);
    }
  };
}
function Nf(l) {
  let e, t;
  return e = new Qs({
    props: {
      i18n: (
        /*gradio*/
        l[16].i18n
      ),
      type: "file"
    }
  }), {
    c() {
      Se(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*gradio*/
      65536 && (a.i18n = /*gradio*/
      n[16].i18n), e.$set(a);
    },
    i(n) {
      t || ($(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Le(e, n);
    }
  };
}
function Uf(l) {
  let e, t, n, i;
  const a = [
    {
      autoscroll: (
        /*gradio*/
        l[16].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[16].i18n
    ) },
    /*loading_status*/
    l[1]
  ];
  let s = {};
  for (let r = 0; r < a.length; r += 1)
    s = Ii(s, a[r]);
  return e = new ji({ props: s }), e.$on(
    "clear_status",
    /*clear_status_handler_1*/
    l[23]
  ), n = new Nr({
    props: {
      label: (
        /*label*/
        l[11]
      ),
      show_label: (
        /*show_label*/
        l[12]
      ),
      root: (
        /*root*/
        l[5]
      ),
      env_map: (
        /*env_map*/
        l[6]
      ),
      tonemapping: (
        /*tonemapping*/
        l[7]
      ),
      exposure: (
        /*exposure*/
        l[8]
      ),
      contrast: (
        /*contrast*/
        l[9]
      ),
      clear_color: (
        /*clear_color*/
        l[10]
      ),
      value: (
        /*value*/
        l[0]
      ),
      camera_position: (
        /*camera_position*/
        l[19]
      ),
      zoom_speed: (
        /*zoom_speed*/
        l[18]
      ),
      i18n: (
        /*gradio*/
        l[16].i18n
      ),
      max_file_size: (
        /*gradio*/
        l[16].max_file_size
      ),
      upload: (
        /*gradio*/
        l[16].client.upload
      ),
      stream_handler: (
        /*gradio*/
        l[16].client.stream
      ),
      $$slots: { default: [Nf] },
      $$scope: { ctx: l }
    }
  }), n.$on(
    "change",
    /*change_handler*/
    l[24]
  ), n.$on(
    "drag",
    /*drag_handler*/
    l[25]
  ), n.$on(
    "change",
    /*change_handler_1*/
    l[26]
  ), n.$on(
    "clear",
    /*clear_handler*/
    l[27]
  ), n.$on(
    "load",
    /*load_handler*/
    l[28]
  ), n.$on(
    "error",
    /*error_handler*/
    l[29]
  ), {
    c() {
      Se(e.$$.fragment), t = Zn(), Se(n.$$.fragment);
    },
    m(r, o) {
      De(e, r, o), St(r, t, o), De(n, r, o), i = !0;
    },
    p(r, o) {
      const f = o & /*gradio, loading_status*/
      65538 ? Ai(a, [
        o & /*gradio*/
        65536 && {
          autoscroll: (
            /*gradio*/
            r[16].autoscroll
          )
        },
        o & /*gradio*/
        65536 && { i18n: (
          /*gradio*/
          r[16].i18n
        ) },
        o & /*loading_status*/
        2 && Vi(
          /*loading_status*/
          r[1]
        )
      ]) : {};
      e.$set(f);
      const _ = {};
      o & /*label*/
      2048 && (_.label = /*label*/
      r[11]), o & /*show_label*/
      4096 && (_.show_label = /*show_label*/
      r[12]), o & /*root*/
      32 && (_.root = /*root*/
      r[5]), o & /*env_map*/
      64 && (_.env_map = /*env_map*/
      r[6]), o & /*tonemapping*/
      128 && (_.tonemapping = /*tonemapping*/
      r[7]), o & /*exposure*/
      256 && (_.exposure = /*exposure*/
      r[8]), o & /*contrast*/
      512 && (_.contrast = /*contrast*/
      r[9]), o & /*clear_color*/
      1024 && (_.clear_color = /*clear_color*/
      r[10]), o & /*value*/
      1 && (_.value = /*value*/
      r[0]), o & /*camera_position*/
      524288 && (_.camera_position = /*camera_position*/
      r[19]), o & /*zoom_speed*/
      262144 && (_.zoom_speed = /*zoom_speed*/
      r[18]), o & /*gradio*/
      65536 && (_.i18n = /*gradio*/
      r[16].i18n), o & /*gradio*/
      65536 && (_.max_file_size = /*gradio*/
      r[16].max_file_size), o & /*gradio*/
      65536 && (_.upload = /*gradio*/
      r[16].client.upload), o & /*gradio*/
      65536 && (_.stream_handler = /*gradio*/
      r[16].client.stream), o & /*$$scope, gradio*/
      1073807360 && (_.$$scope = { dirty: o, ctx: r }), n.$set(_);
    },
    i(r) {
      i || ($(e.$$.fragment, r), $(n.$$.fragment, r), i = !0);
    },
    o(r) {
      ee(e.$$.fragment, r), ee(n.$$.fragment, r), i = !1;
    },
    d(r) {
      r && qt(t), Le(e, r), Le(n, r);
    }
  };
}
function Vf(l) {
  let e, t, n, i;
  return e = new An({
    props: {
      show_label: (
        /*show_label*/
        l[12]
      ),
      Icon: Kt,
      label: (
        /*label*/
        l[11] || "3D Model"
      )
    }
  }), n = new Ho({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [Rf] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Se(e.$$.fragment), t = Zn(), Se(n.$$.fragment);
    },
    m(a, s) {
      De(e, a, s), St(a, t, s), De(n, a, s), i = !0;
    },
    p(a, s) {
      const r = {};
      s & /*show_label*/
      4096 && (r.show_label = /*show_label*/
      a[12]), s & /*label*/
      2048 && (r.label = /*label*/
      a[11] || "3D Model"), e.$set(r);
      const o = {};
      s & /*$$scope*/
      1073741824 && (o.$$scope = { dirty: s, ctx: a }), n.$set(o);
    },
    i(a) {
      i || ($(e.$$.fragment, a), $(n.$$.fragment, a), i = !0);
    },
    o(a) {
      ee(e.$$.fragment, a), ee(n.$$.fragment, a), i = !1;
    },
    d(a) {
      a && qt(t), Le(e, a), Le(n, a);
    }
  };
}
function Af(l) {
  let e, t;
  return e = new sa({
    props: {
      value: (
        /*value*/
        l[0]
      ),
      i18n: (
        /*gradio*/
        l[16].i18n
      ),
      env_map: (
        /*env_map*/
        l[6]
      ),
      tonemapping: (
        /*tonemapping*/
        l[7]
      ),
      exposure: (
        /*exposure*/
        l[8]
      ),
      contrast: (
        /*contrast*/
        l[9]
      ),
      clear_color: (
        /*clear_color*/
        l[10]
      ),
      label: (
        /*label*/
        l[11]
      ),
      show_label: (
        /*show_label*/
        l[12]
      ),
      camera_position: (
        /*camera_position*/
        l[19]
      ),
      zoom_speed: (
        /*zoom_speed*/
        l[18]
      )
    }
  }), {
    c() {
      Se(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), t = !0;
    },
    p(n, i) {
      const a = {};
      i & /*value*/
      1 && (a.value = /*value*/
      n[0]), i & /*gradio*/
      65536 && (a.i18n = /*gradio*/
      n[16].i18n), i & /*env_map*/
      64 && (a.env_map = /*env_map*/
      n[6]), i & /*tonemapping*/
      128 && (a.tonemapping = /*tonemapping*/
      n[7]), i & /*exposure*/
      256 && (a.exposure = /*exposure*/
      n[8]), i & /*contrast*/
      512 && (a.contrast = /*contrast*/
      n[9]), i & /*clear_color*/
      1024 && (a.clear_color = /*clear_color*/
      n[10]), i & /*label*/
      2048 && (a.label = /*label*/
      n[11]), i & /*show_label*/
      4096 && (a.show_label = /*show_label*/
      n[12]), i & /*camera_position*/
      524288 && (a.camera_position = /*camera_position*/
      n[19]), i & /*zoom_speed*/
      262144 && (a.zoom_speed = /*zoom_speed*/
      n[18]), e.$set(a);
    },
    i(n) {
      t || ($(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Le(e, n);
    }
  };
}
function Rf(l) {
  let e, t;
  return e = new Kt({}), {
    c() {
      Se(e.$$.fragment);
    },
    m(n, i) {
      De(e, n, i), t = !0;
    },
    i(n) {
      t || ($(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Le(e, n);
    }
  };
}
function Bf(l) {
  let e, t, n, i, a, s;
  const r = [
    {
      autoscroll: (
        /*gradio*/
        l[16].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[16].i18n
    ) },
    /*loading_status*/
    l[1]
  ];
  let o = {};
  for (let d = 0; d < r.length; d += 1)
    o = Ii(o, r[d]);
  e = new ji({ props: o }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[22]
  );
  const f = [Af, Vf], _ = [];
  function u(d, c) {
    return (
      /*value*/
      d[0] ? 0 : 1
    );
  }
  return n = u(l), i = _[n] = f[n](l), {
    c() {
      Se(e.$$.fragment), t = Zn(), i.c(), a = Ui();
    },
    m(d, c) {
      De(e, d, c), St(d, t, c), _[n].m(d, c), St(d, a, c), s = !0;
    },
    p(d, c) {
      const m = c & /*gradio, loading_status*/
      65538 ? Ai(r, [
        c & /*gradio*/
        65536 && {
          autoscroll: (
            /*gradio*/
            d[16].autoscroll
          )
        },
        c & /*gradio*/
        65536 && { i18n: (
          /*gradio*/
          d[16].i18n
        ) },
        c & /*loading_status*/
        2 && Vi(
          /*loading_status*/
          d[1]
        )
      ]) : {};
      e.$set(m);
      let h = n;
      n = u(d), n === h ? _[n].p(d, c) : (Ri(), ee(_[h], 1, 1, () => {
        _[h] = null;
      }), Ni(), i = _[n], i ? i.p(d, c) : (i = _[n] = f[n](d), i.c()), $(i, 1), i.m(a.parentNode, a));
    },
    i(d) {
      s || ($(e.$$.fragment, d), $(i), s = !0);
    },
    o(d) {
      ee(e.$$.fragment, d), ee(i), s = !1;
    },
    d(d) {
      d && (qt(t), qt(a)), Le(e, d), _[n].d(d);
    }
  };
}
function Of(l) {
  let e, t, n, i;
  const a = [If, jf], s = [];
  function r(o, f) {
    return (
      /*interactive*/
      o[20] ? 1 : 0
    );
  }
  return e = r(l), t = s[e] = a[e](l), {
    c() {
      t.c(), n = Ui();
    },
    m(o, f) {
      s[e].m(o, f), St(o, n, f), i = !0;
    },
    p(o, [f]) {
      let _ = e;
      e = r(o), e === _ ? s[e].p(o, f) : (Ri(), ee(s[_], 1, 1, () => {
        s[_] = null;
      }), Ni(), t = s[e], t ? t.p(o, f) : (t = s[e] = a[e](o), t.c()), $(t, 1), t.m(n.parentNode, n));
    },
    i(o) {
      i || ($(t), i = !0);
    },
    o(o) {
      ee(t), i = !1;
    },
    d(o) {
      o && qt(n), s[e].d(o);
    }
  };
}
function Tf(l, e, t) {
  let { elem_id: n = "" } = e, { elem_classes: i = [] } = e, { visible: a = !0 } = e, { value: s = null } = e, { root: r } = e, { env_map: o = null } = e, { tonemapping: f = null } = e, { exposure: _ = 1 } = e, { contrast: u = 1 } = e, { clear_color: d } = e, { loading_status: c } = e, { label: m } = e, { show_label: h } = e, { container: p = !0 } = e, { scale: y = null } = e, { min_width: b = void 0 } = e, { gradio: g } = e, { height: q = void 0 } = e, { zoom_speed: I = 1 } = e, { camera_position: v = [null, null, null] } = e, { interactive: j } = e, E = !1;
  const N = () => g.dispatch("clear_status", c), B = () => g.dispatch("clear_status", c), H = ({ detail: k }) => t(0, s = k), K = ({ detail: k }) => t(21, E = k), S = ({ detail: k }) => g.dispatch("change", k), X = () => {
    t(0, s = null), g.dispatch("clear");
  }, O = ({ detail: k }) => {
    t(0, s = k), g.dispatch("upload");
  }, U = ({ detail: k }) => {
    t(1, c = c || {}), t(1, c.status = "error", c), g.dispatch("error", k);
  };
  return l.$$set = (k) => {
    "elem_id" in k && t(2, n = k.elem_id), "elem_classes" in k && t(3, i = k.elem_classes), "visible" in k && t(4, a = k.visible), "value" in k && t(0, s = k.value), "root" in k && t(5, r = k.root), "env_map" in k && t(6, o = k.env_map), "tonemapping" in k && t(7, f = k.tonemapping), "exposure" in k && t(8, _ = k.exposure), "contrast" in k && t(9, u = k.contrast), "clear_color" in k && t(10, d = k.clear_color), "loading_status" in k && t(1, c = k.loading_status), "label" in k && t(11, m = k.label), "show_label" in k && t(12, h = k.show_label), "container" in k && t(13, p = k.container), "scale" in k && t(14, y = k.scale), "min_width" in k && t(15, b = k.min_width), "gradio" in k && t(16, g = k.gradio), "height" in k && t(17, q = k.height), "zoom_speed" in k && t(18, I = k.zoom_speed), "camera_position" in k && t(19, v = k.camera_position), "interactive" in k && t(20, j = k.interactive);
  }, [
    s,
    c,
    n,
    i,
    a,
    r,
    o,
    f,
    _,
    u,
    d,
    m,
    h,
    p,
    y,
    b,
    g,
    q,
    I,
    v,
    j,
    E,
    N,
    B,
    H,
    K,
    S,
    X,
    O,
    U
  ];
}
class Xf extends Ef {
  constructor(e) {
    super(), Ff(this, e, Tf, Of, Mf, {
      elem_id: 2,
      elem_classes: 3,
      visible: 4,
      value: 0,
      root: 5,
      env_map: 6,
      tonemapping: 7,
      exposure: 8,
      contrast: 9,
      clear_color: 10,
      loading_status: 1,
      label: 11,
      show_label: 12,
      container: 13,
      scale: 14,
      min_width: 15,
      gradio: 16,
      height: 17,
      zoom_speed: 18,
      camera_position: 19,
      interactive: 20
    });
  }
}
export {
  Hf as E,
  Xf as I,
  Nr as M,
  sa as a,
  Gf as r
};
