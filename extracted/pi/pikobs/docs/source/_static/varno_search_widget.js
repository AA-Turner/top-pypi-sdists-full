// The BUFR element search of the Varno page. Its data, window.PIKOBS_VARNOS,
// is written by pikobs/build_doc/make_varno_search.py (varno_search.js).
(function () {
  "use strict";
  var MAX = 60;
  function fold(s) {                 // case and accents out: "Humidité" = "HUMIDITE"
    return (s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase();
  }
  function families(rows) {
    var f = {};
    rows.forEach(function (r) { r.used.concat(r.carried, r.cutoff || []).forEach(function (x) { f[x] = 1; }); });
    return f;
  }
  function find(rows, q, fams) {
    q = q.trim();
    if (!q) return [];
    var digits = q.replace(/^0+/, "");
    if (/^\d+$/.test(q)) {                               // a code, or the start of one
      return rows.filter(function (r) {
        return r.code.indexOf(q) === 0 || String(r.varno).indexOf(digits) === 0;
      });
    }
    if (fams[q.toLowerCase()]) {                          // a family
      var f = q.toLowerCase();
      return rows.filter(function (r) {
        return r.used.indexOf(f) >= 0 || r.carried.indexOf(f) >= 0 ||
               (r.cutoff || []).indexOf(f) >= 0;
      });
    }
    var words = fold(q).split(/\s+/);                     // words, every one of them
    return rows.filter(function (r) {
      var text = fold(r.en + " " + r.fr + " " + r.wmo);
      return words.every(function (w) { return text.indexOf(w) >= 0; });
    });
  }
  function cell(tag, text) {
    var c = document.createElement(tag); c.textContent = text; return c;
  }
  function show(box, rows, q) {
    box.innerHTML = "";
    if (!q.trim()) return;
    var info = document.createElement("p");
    info.className = "varno-search-info";
    info.textContent = rows.length === 0 ? "No BUFR code matches." :
      rows.length + " BUFR code" + (rows.length > 1 ? "s" : "") +
      (rows.length > MAX ? " -- the first " + MAX + " below, narrow the search" : "") +
      (rows.length ? " -- assimilated first, in bold" : "");
    box.appendChild(info);
    if (!rows.length) return;
    // assimilated first: by the family searched, or by any family
    var f = q.trim().toLowerCase();
    var fam = !/^\d/.test(f) && rows.every(function (r) {
      return r.used.concat(r.carried, r.cutoff || []).indexOf(f) >= 0; });
    var rank = function (r) {
      if (fam) return r.used.indexOf(f) >= 0 ? 0 : r.carried.indexOf(f) >= 0 ? 1 : 2;
      return r.used.length ? 0 : r.carried.length ? 1 : 2;
    };
    rows = rows.slice().sort(function (a, b) {
      return rank(a) - rank(b) || a.code.localeCompare(b.code); });
    var t = document.createElement("table");
    t.className = "docutils varno-search-table";
    var h = document.createElement("tr");
    ["BUFR code", "English", "Français", "Unit", "Assimilated in", "In postalt, not assimilated", "Only in cutoff"]
      .forEach(function (x) { h.appendChild(cell("th", x)); });
    t.appendChild(h);
    rows.slice(0, MAX).forEach(function (r) {
      var tr = document.createElement("tr");
      if (rank(r) === 0) tr.style.fontWeight = "600";      // assimilated
      var en = r.en + (r.wmo && fold(r.wmo) !== fold(r.en) ? "  (WMO: " + r.wmo + ")" : "");
      [r.code, en, r.fr, r.unit, r.used.join(", ") || "--", r.carried.join(", ") || "--",
       (r.cutoff || []).join(", ") || "--"]
        .forEach(function (x) { tr.appendChild(cell("td", x)); });
      t.appendChild(tr);
    });
    box.appendChild(t);
  }
  function start() {
    var input = document.getElementById("varno-search-input");
    var box = document.getElementById("varno-search-results");
    if (!input || !box || !window.PIKOBS_VARNOS) return;
    var rows = window.PIKOBS_VARNOS, fams = families(rows);
    var run = function () { show(box, find(rows, input.value, fams), input.value); };
    input.addEventListener("input", run);
    var q = new URLSearchParams(window.location.search).get("varno");
    if (q) { input.value = q; run(); }                    // ...varno.html?varno=12163
  }
  if (typeof module !== "undefined") { module.exports = { find: find, fold: fold, families: families }; }
  else if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", start); }
  else { start(); }
})();
