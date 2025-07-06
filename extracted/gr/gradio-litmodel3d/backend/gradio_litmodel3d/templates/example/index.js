const {
  SvelteComponent: _,
  append: c,
  attr: d,
  detach: g,
  element: o,
  init: r,
  insert: v,
  noop: u,
  safe_not_equal: y,
  set_data: m,
  text: b,
  toggle_class: f
} = window.__gradio__svelte__internal;
function w(a) {
  let e, n = (
    /*value*/
    (a[0] ? (
      /*value*/
      a[0]
    ) : "") + ""
  ), s;
  return {
    c() {
      e = o("div"), s = b(n), d(e, "class", "svelte-1gecy8w"), f(
        e,
        "table",
        /*type*/
        a[1] === "table"
      ), f(
        e,
        "gallery",
        /*type*/
        a[1] === "gallery"
      ), f(
        e,
        "selected",
        /*selected*/
        a[2]
      );
    },
    m(t, l) {
      v(t, e, l), c(e, s);
    },
    p(t, [l]) {
      l & /*value*/
      1 && n !== (n = /*value*/
      (t[0] ? (
        /*value*/
        t[0]
      ) : "") + "") && m(s, n), l & /*type*/
      2 && f(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), l & /*type*/
      2 && f(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), l & /*selected*/
      4 && f(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    i: u,
    o: u,
    d(t) {
      t && g(e);
    }
  };
}
function h(a, e, n) {
  let { value: s } = e, { type: t } = e, { selected: l = !1 } = e;
  return a.$$set = (i) => {
    "value" in i && n(0, s = i.value), "type" in i && n(1, t = i.type), "selected" in i && n(2, l = i.selected);
  }, [s, t, l];
}
class q extends _ {
  constructor(e) {
    super(), r(this, e, h, w, y, { value: 0, type: 1, selected: 2 });
  }
}
export {
  q as default
};
