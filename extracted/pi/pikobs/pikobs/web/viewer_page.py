"""
pikobs.web.viewer_page
======================
The page of the common viewer (generate_web): the choices on the left, as
buttons grouped by what they choose, and the figure on the right.

* The groups cascade: each one shows only the values that exist with what
  is chosen above it, a group with a single value is not shown, and a
  value that is gone is replaced by the one chosen last time in the same
  family (or the first), with a short highlight so the change is seen.
* The figure has a toolbar -- flip, fit, download (PNG, and SVG when there
  is one), copy a link to the selection, open alone, help -- and a
  lightbox: fit to the screen, then full size.
* The explanation of the module sits in a collapsible "About" box, closed
  by default, and the page remembers whether it was left open.
* The selection is kept in the address (#key=value&...), so a link opens
  the same figure; arrows step through the last group, F flips, W fits,
  Esc closes, ? shows the keys. With play, the last group is animated.

Everything is in one HTML file: it works opened from disk or copied
anywhere.
"""
import html
import json

#: The order of the groups, from the general to the particular. A key that
#: is not here keeps its place among the others, before panel, mode and date.
_ORDER = {
    "comparison": -1, "metric": -0.5,
    "experiment": 0, "experience": 0, "exp_name": 0, "run": 0,
    # the projection right before the region: the map is chosen first
    "family": 1, "proj": 1.9, "projection": 1.9,
    "region": 2, "flag": 3, "criteria": 3,
    "surface": 4, "land_ocean": 4, "function": 5,
    "varno": 6, "channel": 7, "vcoord": 7, "level": 7, "layer": 7,
    "id_stn": 8, "special": 9, "panel": 10, "mode": 11, "date": 12,
}


def ordered_keys(keys, enable_play=False):
    """The keys in the order of the groups; with play, the animated key
    (the last one given) stays last."""
    keys = list(keys)
    last = keys[-1] if (enable_play and keys) else None
    rest = [k for k in keys if k != last]
    pos = {k: i for i, k in enumerate(rest)}
    rest = sorted(rest, key=lambda k: (_ORDER.get(k, 9.5), pos[k]))
    return rest + ([last] if last else [])


def _js(obj):
    """JSON safe inside a <script>."""
    return json.dumps(obj).replace("</", "<\\/")


def render_page(items, keys, captions, *, title, subtitle=None,
                image_subdir_key=None, value_labels=None, issues_url=None,
                enable_play=False, base_dir=None, value_notes=None, doc_link=None):
    """The HTML of the viewer. ``items`` are the stringified items,
    ``captions`` the (key, label) pairs of generate_web."""
    keys = ordered_keys(keys, enable_play)
    labels = dict(captions)
    about = ""
    if subtitle:
        about = ('<details class="about" id="about"><summary>About this '
                 f'diagnostic</summary><div class="body">{subtitle}</div></details>')
    footer = ""
    if issues_url:
        u = html.escape(issues_url, quote=True)
        footer = f'<footer>Issues: <a href="{u}" target="_blank">{u}</a></footer>'
    play = ""
    if enable_play:
        play = ('<button class="tb" id="btnp" onclick="togglePlay()" '
                'title="Animate the last group (space)">&#9654; Play</button>'
                '<select class="tb" id="speed" title="Frames per second">'
                '<option value="0.5">0.5 fps</option><option value="1">1 fps</option>'
                '<option value="2" selected>2 fps</option><option value="4">4 fps</option>'
                '<option value="8">8 fps</option></select>'
                '<label class="tb" title="Start again at the end">'
                '<input type="checkbox" id="loop" checked> Loop</label>')
    page = _PAGE
    for tag, val in (("__TITLE__", html.escape(title)), ("__ABOUT__", about),
                     ("__FOOTER__", footer), ("__PLAY__", play),
                     ("__ITEMS__", _js(list(items))), ("__KEYS__", _js(keys)),
                     ("__LABELS__", _js({k: labels.get(k, k) for k in keys})),
                     ("__VLABELS__", _js(dict(value_labels) if value_labels else {})),
                     ("__SUBDIR__", _js(image_subdir_key)),
                     ("__PLAY_ON__", "true" if enable_play else "false"),
                     ("__BASE__", _js(base_dir.rstrip("/") if base_dir else None)),
                     ("__NOTES__", _js(dict(value_notes) if value_notes else {})),
                     ("__DOC__", (f'<a class="doc" href="{html.escape(doc_link, quote=True)}" '
                                  'target="_blank">Documentation &#8599;</a>' if doc_link else ""))):
        page = page.replace(tag, val)
    return page


_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root { --accent:#4C72B0; --accent-l:#eef4ff; --ink:#2c3e50; --muted:#7f8c8d;
          --bg:#f6f7f9; --card:#fff; --line:#e2e5ea; }
  * { box-sizing:border-box; }
  body { font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif; margin:0;
         background:var(--bg); color:var(--ink); }
  header { background:var(--ink); color:#fff; padding:14px 22px; }
  header h1 { margin:0; font-size:20px; font-weight:600; }
  .page { max-width:1680px; margin:0 auto; padding:16px 22px 24px; }
  details.about { background:#fff; border:1px solid var(--line);
                  border-left:4px solid var(--accent); border-radius:6px;
                  margin-bottom:16px; }
  details.about summary { cursor:pointer; padding:10px 14px; font-weight:600;
                          list-style:none; user-select:none; }
  details.about summary::-webkit-details-marker { display:none; }
  details.about summary::before { content:'\25B8'; display:inline-block; margin-right:8px;
                                  transition:transform .15s; }
  details.about[open] summary::before { transform:rotate(90deg); }
  details.about .body { padding:0 16px 14px; font-size:14px; line-height:1.55;
                        color:var(--ink); }
  /* the runs block of older viewers carried a pale grey for a dark header */
  details.about .body span[style] { color:var(--ink) !important;
                                     margin-left:0 !important; text-align:left !important; }
  details.about .runs { margin-top:12px; font-size:13px; }
  details.about .runs-title { margin:0 0 4px; font-size:11.5px; font-weight:700;
                              text-transform:uppercase; letter-spacing:.5px; color:#34495e; }
  details.about .runs table { border-collapse:collapse; }
  details.about .runs td { padding:3px 14px 3px 0; vertical-align:top; }
  details.about .runs td.role { color:var(--muted); font-size:12px;
                                text-transform:uppercase; letter-spacing:.4px; }
  details.about .runs td.name { font-weight:600; }
  details.about code { font-family:monospace; font-size:12.5px; background:#f3f5f8;
                       border:1px solid #e3e7ec; border-radius:4px; padding:1px 6px;
                       word-break:break-all; }
  details.about .period { margin:8px 0 0; }
  .layout { display:grid; grid-template-columns:minmax(240px,330px) minmax(0,1fr);
            gap:18px; align-items:stretch; }
  @media (max-width:900px) { .layout { grid-template-columns:1fr; }
                             .figure { position:static !important; } }
  .controls { background:var(--card); border:1px solid var(--line); border-radius:8px;
              padding:8px 10px; }
  .group { padding:9px 6px; border-radius:6px; transition:background .8s; }
  .group + .group { border-top:1px solid #f0f1f4; }
  .group.changed { background:#fff1c9; transition:none; }
  .group .lab { font-size:11.5px; text-transform:uppercase; letter-spacing:.5px;
                color:#34495e; font-weight:700; margin-bottom:7px; }
  .group .btns { display:flex; flex-wrap:wrap; gap:6px; }
  .group button { background:#fff; color:var(--accent); border:1px solid var(--accent);
                  border-radius:4px; padding:5px 11px; font-size:13px; cursor:pointer; }
  .group button:hover { background:var(--accent-l); }
  .group button.active { background:var(--accent); color:#fff; font-weight:600; }
  .group button.fixed { background:#2f4a73; border-color:#2f4a73; cursor:default; }
  .group button.every, .group button.every:disabled { background:#1f3b63;
     border-color:#1f3b63; color:#fff; opacity:1; cursor:default; }
  .notes { display:none; margin-top:10px; padding:10px 14px; background:#f7f9fc;
           border-left:3px solid var(--accent); border-radius:4px; font-size:13.5px;
           line-height:1.5; }
  .notes p { margin:0 0 6px; } .notes p:last-child { margin:0; }
  .notes a { color:var(--accent); font-weight:600; }
  header { display:flex; align-items:center; gap:16px; }
  header h1 { flex:1; }
  header a.doc { color:#fff; text-decoration:none; font-size:13px; border:1px solid rgba(255,255,255,.45);
                 border-radius:4px; padding:5px 11px; white-space:nowrap; }
  header a.doc:hover { background:rgba(255,255,255,.12); }
  .group .btns.many { max-height:230px; overflow-y:auto; gap:5px; padding:3px;
                      border:1px solid #eef0f3; border-radius:4px; }
  .group .btns.many button { padding:4px 9px; font-size:13.5px; min-width:52px;
                             color:#1f3b63; border-color:#8aa4c8; }
  .group .btns.many button.active { color:#fff; background:var(--accent);
                                    border-color:var(--accent); }
  .group .filter { width:100%; margin:0 0 6px; padding:5px 9px; font-size:13.5px;
                   border:1px solid #cfd4da; border-radius:4px; font-family:inherit; }
  .group .count { font-weight:400; color:var(--muted); text-transform:none;
                  letter-spacing:0; margin-left:4px; }
  .group .lab .stepb { margin-left:6px; padding:0 7px; font-size:11px;
                       line-height:18px; border-radius:3px; }
  .group.nav .lab::after { content:'  \2190 \2192'; color:var(--muted);
                          font-weight:400; letter-spacing:0; }
  .figure { align-self:start; position:sticky; top:12px; background:var(--card); border:1px solid var(--line);
            border-radius:8px; padding:12px 14px; }
  .toolbar { display:flex; flex-wrap:wrap; gap:6px; align-items:center; margin-bottom:10px; }
  .toolbar .sp { flex:1; }
  .tb { background:#fff; color:var(--ink); border:1px solid #cfd4da; border-radius:4px;
        padding:5px 10px; font-size:12.5px; cursor:pointer; text-decoration:none;
        display:inline-flex; align-items:center; gap:5px; font-family:inherit; }
  .tb:hover { background:#f2f4f7; }
  .tb.on { background:#e67e22; color:#fff; border-color:#e67e22; }
  .tb[disabled] { opacity:.45; cursor:not-allowed; }
  .imgwrap { position:relative; width:100%; max-height:82vh; aspect-ratio:1 / 1;
             display:flex; align-items:center; justify-content:center;
             background:#fafbfc; border-radius:4px; overflow:hidden; }
  .imgwrap.fitwidth { max-height:none; }
  .imgwrap.zoomed { overflow:auto; cursor:grab; }
  .imgwrap.zoomed img { width:calc(var(--z) * 100%); height:calc(var(--z) * 100%);
                        cursor:grab; }
  .imgwrap.zoomed .zoomhint { display:none; }
  .imgwrap.dragging, .imgwrap.dragging img { cursor:grabbing; }
  .zlevel { min-width:46px; justify-content:center; }
  .imgwrap img { position:absolute; top:0; left:0; width:100%; height:100%;
                 object-fit:contain; opacity:0; pointer-events:none;
                 transition:opacity .15s ease-in-out; cursor:zoom-in; }
  .imgwrap img.show { opacity:1; pointer-events:auto; }
  .zoomhint { position:absolute; right:10px; top:10px; background:rgba(44,62,80,.78);
              color:#fff; font-size:12px; padding:4px 9px; border-radius:4px; opacity:0;
              transition:opacity .15s; pointer-events:none; z-index:3; }
  .imgwrap:hover .zoomhint { opacity:1; }
  .badge { position:absolute; left:10px; top:10px; background:#e67e22; color:#fff;
           font-size:12px; font-weight:700; letter-spacing:.6px; padding:4px 9px;
           border-radius:4px; z-index:3; display:none; }
  .badge.on { display:block; }
  .caption .path { cursor:copy; }
  .err { color:#c0392b; font-weight:600; font-size:15px; position:absolute; display:none;
         background:#fff; padding:14px 22px; border-radius:6px;
         box-shadow:0 2px 8px rgba(0,0,0,.15); z-index:5; }
  .caption { margin-top:10px; font-size:13.5px; }
  .caption .path { display:block; margin-top:4px; font-family:monospace; font-size:11.5px;
                   color:var(--muted); word-break:break-all; }
  footer { text-align:center; color:var(--muted); font-size:12.5px; padding:14px; }
  footer a { color:var(--accent); font-weight:600; text-decoration:none; }
  .lightbox { display:none; position:fixed; inset:0; background:rgba(20,20,20,.94);
              z-index:1000; overflow:auto; text-align:center; }
  .lightbox.open { display:block; }
  .lightbox img { max-width:96vw; max-height:92vh; margin:4vh auto 0; display:block;
                  cursor:zoom-in; box-shadow:0 4px 24px rgba(0,0,0,.5); background:#fff; }
  .lightbox.actual img { max-width:none; max-height:none; margin:20px; cursor:zoom-out;
                         display:inline-block; }
  .lbhint { position:fixed; top:12px; right:16px; color:#ecf0f1; font-size:12.5px;
            font-family:monospace; z-index:1001; }
  .help { display:none; position:fixed; inset:0; background:rgba(0,0,0,.35); z-index:900; }
  .help.open { display:flex; align-items:center; justify-content:center; }
  .help .card { background:#fff; border-radius:8px; padding:18px 24px; min-width:300px;
                box-shadow:0 6px 30px rgba(0,0,0,.25); font-size:14px; }
  .help kbd { display:inline-block; min-width:22px; text-align:center; border:1px solid #cfd4da;
              border-bottom-width:2px; border-radius:4px; padding:1px 6px; margin-right:8px;
              font-family:monospace; background:#f7f8fa; }
  .help td { padding:4px 0; }
  .toast { position:fixed; bottom:18px; left:50%; transform:translateX(-50%);
           background:var(--ink); color:#fff; padding:8px 14px; border-radius:6px;
           font-size:13px; opacity:0; transition:opacity .2s; pointer-events:none; z-index:1100; }
  .toast.show { opacity:1; }
</style>
</head>
<body>
<header><h1>__TITLE__</h1>__DOC__</header>
<div class="page">
__ABOUT__
<div class="layout">
  <aside class="controls" id="controls"></aside>
  <main class="figure">
    <div class="toolbar">
      <button class="tb" id="btnf" onclick="flip()" disabled
              title="Show the previous figure again (F)">&#8644; Flip</button>
      <button class="tb" id="btnff" onclick="flipFlop()" disabled
              title="Alternate the two figures by itself (B)">&#8644;&#8644; Flip-flop</button>
      <button class="tb" id="btnw" onclick="toggleFit()"
              title="Fit to the screen or to the width (W)">&#10530; Fit</button>
      <button class="tb" onclick="zoomBy(-1)" title="Smaller, down to 50 %, or back from a zoom (-)">&minus;</button>
      <button class="tb zlevel" id="zlevel" onclick="zoomTo(1)"
              title="Back to the whole figure (0)">100%</button>
      <button class="tb" onclick="zoomBy(+1)"
              title="Zoom in the box; Ctrl + wheel works too (+)">+</button>
      __PLAY__
      <span class="sp"></span>
      <a class="tb" id="dl" download title="Download the figure">&#11015; PNG</a>
      <a class="tb" id="dlsvg" download style="display:none"
         title="Download the figure as SVG">&#11015; SVG</a>
      <button class="tb" onclick="copyLink()"
              title="Copy a link that opens this very figure">&#128279; Copy link</button>
      <a class="tb" id="open" target="_blank" title="Open the figure alone">&#8599; Open</a>
      <button class="tb" onclick="toggleHelp()" title="Keyboard shortcuts (?)">?</button>
    </div>
    <div id="wrap" class="imgwrap">
      <div id="err" class="err">&#9888; No figure for this selection.</div>
      <img id="imgA" alt="" onclick="openLightbox()">
      <img id="imgB" alt="" onclick="openLightbox()">
      <div class="zoomhint">&#128269; Click to zoom</div>
      <div class="badge" id="badge">PREVIOUS</div>
    </div>
    <div class="caption"><span id="cap"></span><span class="path" id="path" title="Click to copy" onclick="copyPath()"></span></div>
    <div class="notes" id="notes"></div>
  </main>
</div>
</div>
__FOOTER__
<div id="lightbox" class="lightbox" onclick="lbClick(event)">
  <div class="lbhint">Click the figure: full size &middot; outside or Esc: close</div>
  <img id="lightboxImg" alt="">
</div>
<div id="help" class="help" onclick="toggleHelp()"><div class="card">
  <b>Keyboard</b>
  <table>
    <tr><td><kbd>&larr;</kbd><kbd>&rarr;</kbd></td><td>previous / next value of the group last clicked (marked &larr; &rarr;), the last group until then</td></tr>
    <tr><td><kbd>Enter</kbd></td><td>in a filter box: go to the value typed</td></tr>
    <tr><td><kbd>F</kbd></td><td>flip to the previous figure and back</td></tr>
    <tr><td><kbd>B</kbd></td><td>flip-flop: alternate the two by itself</td></tr>
    <tr><td><kbd>W</kbd></td><td>fit to the screen or to the width</td></tr>
    <tr><td><kbd>+</kbd><kbd>-</kbd><kbd>0</kbd></td><td>zoom in the box, out, back to the whole figure (or Ctrl + wheel; drag to move)</td></tr>
    <tr><td><kbd>Z</kbd></td><td>full screen</td></tr>
    <tr><td><kbd>Esc</kbd></td><td>close the zoom</td></tr>
    <tr><td><kbd>?</kbd></td><td>this help</td></tr>
  </table>
</div></div>
<div id="toast" class="toast"></div>
<script>
const DB = __ITEMS__;
const KEYS = __KEYS__;
const LABELS = __LABELS__;
const VAL_LABELS = __VLABELS__;
const SUBDIR_KEY = __SUBDIR__;
const PLAY = __PLAY_ON__;
const BASE = __BASE__;
const NOTES = __NOTES__;   // key -> value -> what the figure shows; filled module by module
const STORE = 'pikobs_viewer:' + document.title;
const FAMKEY = KEYS.includes('family') ? 'family' : null;

const state = {};  KEYS.forEach(k => state[k] = null);
const memory = {};          // memory[key][family]: the value chosen last time
const MANY = 24;            // a group with more values is compact, with a filter
const filters = {};
let navKey = null;          // the group the arrows step: the last one clicked
function applyFilter(g, text) {
  const t = text.trim().toLowerCase();
  g.querySelectorAll('.btns button').forEach(b => {
    b.style.display = (!t || b.textContent.toLowerCase().includes(t)
                       || b.title.toLowerCase().includes(t)) ? '' : 'none';
  });
}
let curSrc = '', prevSrc = '', showPrev = false, curImg = 'imgA', prevImg = 'imgB';

function natsort(a, b) {
  return String(a).localeCompare(String(b), undefined, {numeric: true, sensitivity: 'base'});
}
function pretty(k, v) {
  if (v === '*') return 'all';                 // a figure that holds every one
  if (k === 'layer' && v === 'layer_all') return 'whole column';
  return (VAL_LABELS[k] && VAL_LABELS[k][v]) ? VAL_LABELS[k][v] : v;
}
function upTo(i) { return DB.filter(d => KEYS.slice(0, i).every(k => d[k] === state[k])); }
function uniq(rows, k) { return [...new Set(rows.map(d => d[k]))].sort(natsort); }

// every key from `from` on takes a value among those that exist with the
// keys above it: the one asked for, else the one it had, else the one
// chosen last time in this family, else the first
function cascade(from, picks) {
  const changed = [];
  for (let i = from; i < KEYS.length; i++) {
    const k = KEYS[i], vals = uniq(upTo(i), k), before = state[k];
    const fam = FAMKEY && FAMKEY !== k ? state[FAMKEY] : '';
    const mem = memory[k] ? memory[k][fam] : undefined;
    let v = vals[0];
    if (picks && picks[k] !== undefined && vals.includes(picks[k])) v = picks[k];
    else if (vals.includes(before)) v = before;
    else if (mem !== undefined && vals.includes(mem)) v = mem;
    state[k] = v;
    if (before !== null && before !== v && !(picks && picks[k] !== undefined)) changed.push(k);
  }
  return changed;
}
function remember(k) {
  const fam = FAMKEY && FAMKEY !== k ? state[FAMKEY] : '';
  (memory[k] = memory[k] || {})[fam] = state[k];
}
function choose(i, v) {
  const changed = cascade(i, {[KEYS[i]]: v});
  remember(KEYS[i]);
  draw(changed); showImage(); saveHash();
}

// a section whose only choice is its neutral value says nothing: the
// vertical of a layer is 'join', the layer of a channel is 'layer_all'
const NEUTRAL = {layer: ['layer_all'], channel: ['join'], vcoord: ['join']};
// only when the viewer holds layers; without them only Layer goes
const LAYERS_ON = DB.some(d => d.layer !== undefined &&
                               !['layer_all', '*', ''].includes(String(d.layer)));
function draw(changed) {
  const box = document.getElementById('controls'); box.innerHTML = '';
  KEYS.forEach((k, i) => {
    let vals = uniq(upTo(i), k);
    // a figure that holds every value of the key ("*"): every button,
    // all of them on, none to press
    const every = vals.length === 1 && vals[0] === '*';
    if (every) vals = uniq(DB, k).filter(v => v !== '*');
    const fixed = vals.length < 2;                  // shown, but nothing to choose
    if (fixed && vals.length === 1 && (NEUTRAL[k] || []).includes(vals[0])
        && (LAYERS_ON || k === 'layer')) return;
    const g = document.createElement('div'); g.className = 'group'; g.dataset.key = k;
    if (i === arrowIndex()) g.classList.add('nav');
    const lab = document.createElement('div'); lab.className = 'lab';
    lab.textContent = LABELS[k] || k; g.appendChild(lab);
    const many = vals.length > MANY;
    if (many) {                     // a long list: count, filter, own scroll
      const c = document.createElement('span'); c.className = 'count';
      c.textContent = '(' + vals.length + ')'; lab.appendChild(c);
      [['\u25C0', -1, 'previous'], ['\u25B6', +1, 'next']].forEach(([t, d, tip]) => {
        const s = document.createElement('button'); s.className = 'stepb';
        s.textContent = t; s.title = tip;
        s.onclick = () => { navKey = k; stepKey(i, d); };
        lab.appendChild(s);
      });
      const f = document.createElement('input'); f.className = 'filter';
      f.placeholder = 'filter\u2026  (Enter goes there)'; f.value = filters[k] || '';
      f.oninput = () => { filters[k] = f.value; applyFilter(g, f.value); };
      f.onkeydown = e => {          // the exact value typed, else the first match
        if (e.key !== 'Enter') return;
        const t = f.value.trim().toLowerCase();
        const txt = v => [String(v).toLowerCase(), String(pretty(k, v)).toLowerCase()];
        const exact = vals.find(v => txt(v).includes(t));
        const first = vals.find(v => txt(v).some(s => s.includes(t)));
        const v = exact !== undefined ? exact : first;
        if (v !== undefined) { navKey = k; choose(i, v); }
      };
      g.appendChild(f);
    }
    const btns = document.createElement('div'); btns.className = many ? 'btns many' : 'btns';
    vals.forEach(v => {
      const b = document.createElement('button');
      b.textContent = pretty(k, v); b.title = v;
      if (every) { b.className = 'active every'; b.disabled = true;
                   b.title = v + ' (the figure holds every one)'; }
      else {
        if (v === state[k]) b.className = 'active';
        if (fixed) { b.className = 'active fixed'; b.disabled = true;
                     b.title = v + ' (the only value)'; }
        else b.onclick = () => { navKey = k; choose(i, v); };
      }
      btns.appendChild(b);
    });
    g.appendChild(btns); box.appendChild(g);
    if (many) {
      applyFilter(g, filters[k] || '');
      const a = btns.querySelector('.active');
      if (a && a.scrollIntoView) a.scrollIntoView({block: 'nearest'});
    }
    if (changed && changed.includes(k)) {
      g.classList.add('changed');
      setTimeout(() => g.classList.remove('changed'), 50);
    }
  });
}

// the keys whose value is the same for every figure say nothing: not in the caption
const CONSTANT = KEYS.filter(k => uniq(DB, k).length < 2);
function buildSrc(m) { return SUBDIR_KEY ? m[SUBDIR_KEY] + '/' + m.filename : m.filename; }
// a figure may come with a map of what is under the mouse: <png>.map.json,
// rectangles in pixels of the PNG and a text for each
const MAPS = {};
const TIP = document.createElement('div');
TIP.style.cssText = 'position:fixed;display:none;pointer-events:none;z-index:1000;' +
  'background:#1f2933;color:#fff;font-size:12px;line-height:1.35;padding:6px 9px;' +
  'border-radius:5px;max-width:460px;white-space:pre-line;box-shadow:0 2px 6px rgba(0,0,0,.25)';
document.body.appendChild(TIP);
function mapOf(src) {
  if (!src) return null;
  if (!(src in MAPS)) {
    MAPS[src] = null;
    fetch(src + '.map.json').then(r => r.ok ? r.json() : null)
      .then(m => { MAPS[src] = m; }).catch(() => {});
  }
  return MAPS[src];
}
function hover(e) {
  const img = e.currentTarget, m = mapOf(img.getAttribute('src'));
  if (!m || !img.clientWidth) { TIP.style.display = 'none'; return; }
  const x = e.offsetX * m.w / img.clientWidth, y = e.offsetY * m.h / img.clientHeight;
  const r = m.rects.find(q => x >= q[0] && x < q[2] && y >= q[1] && y < q[3]);
  if (!r) { TIP.style.display = 'none'; return; }
  TIP.textContent = m.texts[r[4]];
  TIP.style.display = 'block';
  TIP.style.left = Math.min(e.clientX + 14, window.innerWidth - TIP.offsetWidth - 8) + 'px';
  TIP.style.top = Math.min(e.clientY + 14, window.innerHeight - TIP.offsetHeight - 8) + 'px';
}
['imgA', 'imgB'].forEach(id => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('mousemove', hover);
  el.addEventListener('mouseleave', () => { TIP.style.display = 'none'; });
});
function showImage() {
  const m = DB.find(d => KEYS.every(k => d[k] === state[k]));
  const err = document.getElementById('err');
  if (!m) { err.style.display = 'block'; return; }
  const src = buildSrc(m);
  if (src !== curSrc) {
    if (curSrc) { prevSrc = curSrc; document.getElementById('btnf').disabled = false;
                  document.getElementById('btnff').disabled = false; }
    curSrc = src; showPrev = false; stopFlipFlop();
    document.getElementById('btnf').classList.remove('on');
    document.getElementById('badge').classList.remove('on');
  }
  const notes = KEYS.filter(k => NOTES[k] && NOTES[k][state[k]])
                    .map(k => '<p>' + NOTES[k][state[k]] + '</p>').join('');
  const nb = document.getElementById('notes');
  nb.innerHTML = notes; nb.style.display = notes ? '' : 'none';
  document.getElementById('cap').textContent =
    KEYS.filter(k => !CONSTANT.includes(k)).map(k => pretty(k, state[k])).join(' \u00b7 ');
  apply(curSrc);
  mapOf(curSrc);                        // ask for its map, if it has one
  preloadNext();
}
function apply(src) {
  document.getElementById('err').style.display = 'none';
  document.getElementById('path').textContent = fullPath(src);
  const dl = document.getElementById('dl');
  dl.href = src; dl.download = src.split('/').pop();
  document.getElementById('open').href = src;
  const svg = src.replace(/\.png$/i, '.svg'), s = document.getElementById('dlsvg');
  s.style.display = 'none';
  if (svg !== src) {
    const probe = new Image();
    probe.onload = () => { s.href = svg; s.download = svg.split('/').pop(); s.style.display = ''; };
    probe.src = svg;
  }
  const next = document.getElementById(prevImg);
  next.onload = () => {
    setAspect(next);
    document.getElementById(curImg).classList.remove('show');
    next.classList.add('show');
    const t = curImg; curImg = prevImg; prevImg = t;
  };
  next.onerror = () => { document.getElementById('err').style.display = 'block'; };
  next.src = src;
}

let fitMode = 'auto', lockedRatio = 0;
function setAspect(img) {
  if (!img.naturalWidth || !img.naturalHeight) return;
  const r = img.naturalHeight / img.naturalWidth;
  // follow the figure only when its shape really changes, so Flip does not jump
  if (!lockedRatio || Math.abs(r - lockedRatio) / lockedRatio > 0.10) {
    lockedRatio = r;
    document.getElementById('wrap').style.aspectRatio = img.naturalWidth + ' / ' + img.naturalHeight;
  }
  applyFit();
}
function applyFit() {
  // a figure taller than wide goes to the full width and the page scrolls
  const width = fitMode === 'width' || (fitMode === 'auto' && lockedRatio > 1.15);
  document.getElementById('wrap').classList.toggle('fitwidth', width);
  document.getElementById('btnw').innerHTML = width ? '&#10530; Fit: width' : '&#10530; Fit: screen';
  if (typeof zoom !== 'undefined' && zoom < 1) zoomTo(zoom);   // the height follows the fit
}
function toggleFit() {
  fitMode = document.getElementById('wrap').classList.contains('fitwidth') ? 'screen' : 'width';
  applyFit();
}
const ZOOMS = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.25, 1.5, 2, 3, 4, 6];
let zoom = 1;
function zoomTo(z) {
  const w = document.getElementById('wrap');
  const cx = (w.scrollLeft + w.clientWidth / 2) / (w.scrollWidth || 1);
  const cy = (w.scrollTop + w.clientHeight / 2) / (w.scrollHeight || 1);
  zoom = z;
  w.style.setProperty('--z', z);
  w.classList.toggle('zoomed', z > 1);
  // below 100 % the whole box gets smaller, centred, its shape kept, so a
  // tall figure fits the screen; the buttons on the left never move
  const small = z < 1;
  w.style.width = small ? (z * 100) + '%' : '';
  w.style.marginLeft = w.style.marginRight = small ? 'auto' : '';
  w.style.maxHeight = small && !w.classList.contains('fitwidth') ? 'calc(82vh * ' + z + ')' : '';
  document.getElementById('zlevel').textContent = Math.round(z * 100) + '%';
  if (z > 1) {                    // keep the same point in the middle
    w.scrollLeft = cx * w.scrollWidth - w.clientWidth / 2;
    w.scrollTop = cy * w.scrollHeight - w.clientHeight / 2;
  }
}
function zoomBy(dir) {
  let i = ZOOMS.indexOf(zoom); if (i < 0) i = ZOOMS.indexOf(1);
  zoomTo(ZOOMS[Math.max(0, Math.min(ZOOMS.length - 1, i + dir))]);
}
(function () {                    // Ctrl + wheel zooms, a drag moves the figure
  const w = document.getElementById('wrap');
  w.addEventListener('wheel', e => {
    if (!e.ctrlKey) return;
    e.preventDefault(); zoomBy(e.deltaY < 0 ? +1 : -1);
  }, {passive: false});
  let drag = null;
  w.addEventListener('mousedown', e => {
    if (zoom <= 1) return;
    drag = {x: e.clientX, y: e.clientY, l: w.scrollLeft, t: w.scrollTop, moved: false};
    w.classList.add('dragging'); e.preventDefault();
  });
  window.addEventListener('mousemove', e => {
    if (!drag) return;
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
    w.scrollLeft = drag.l - dx; w.scrollTop = drag.t - dy;
  });
  window.addEventListener('mouseup', () => {
    if (drag) { w.dataset.dragged = drag.moved ? '1' : ''; drag = null;
                w.classList.remove('dragging'); }
  });
})();
function flip() {
  if (!prevSrc) return;
  showPrev = !showPrev;
  document.getElementById('btnf').classList.toggle('on', showPrev);
  document.getElementById('badge').classList.toggle('on', showPrev);
  apply(showPrev ? prevSrc : curSrc);
}
let ffTimer = null;
function flipFlop() {
  if (ffTimer) { stopFlipFlop(); if (showPrev) flip(); return; }
  if (!prevSrc) return;
  ffTimer = setInterval(flip, 700);
  document.getElementById('btnff').classList.add('on');
}
function stopFlipFlop() {
  if (ffTimer) { clearInterval(ffTimer); ffTimer = null; }
  document.getElementById('btnff').classList.remove('on');
}
function fullPath(src) { return BASE ? BASE + '/' + src : new URL(src, location.href).href; }
function copyPath() {
  const p = document.getElementById('path').textContent;
  const fallback = () => window.prompt('Copy this path:', p);
  if (navigator.clipboard && navigator.clipboard.writeText)
    navigator.clipboard.writeText(p).then(() => toast('Path copied'), fallback);
  else fallback();
}

function openLightbox() {
  const w = document.getElementById('wrap');
  if (w.dataset.dragged) { w.dataset.dragged = ''; return; }
  if (!curSrc) return;
  const lb = document.getElementById('lightbox');
  document.getElementById('lightboxImg').src = showPrev ? prevSrc : curSrc;
  lb.classList.remove('actual'); lb.classList.add('open');
}
function lbClick(e) {
  const lb = document.getElementById('lightbox');
  if (e.target.id === 'lightboxImg') lb.classList.toggle('actual');
  else lb.classList.remove('open');
}
function toggleHelp() { document.getElementById('help').classList.toggle('open'); }
function toast(text) {
  const t = document.getElementById('toast'); t.textContent = text; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1600);
}

// the selection in the address, so a link opens the same figure
function saveHash() {
  const h = KEYS.map(k => encodeURIComponent(k) + '=' + encodeURIComponent(state[k])).join('&');
  try { history.replaceState(null, '', '#' + h); } catch (e) { location.hash = h; }
}
function readHash() {
  const out = {};
  (location.hash || '').replace(/^#/, '').split('&').forEach(p => {
    const i = p.indexOf('=');
    if (i > 0) out[decodeURIComponent(p.slice(0, i))] = decodeURIComponent(p.slice(i + 1));
  });
  return out;
}
function copyLink() {
  saveHash();
  const url = location.href;
  const fallback = () => window.prompt('Copy this link:', url);
  if (navigator.clipboard && navigator.clipboard.writeText)
    navigator.clipboard.writeText(url).then(() => toast('Link copied'), fallback);
  else fallback();
}

// the last group with something to choose: arrows and play step through it
function navIndex() {
  for (let i = KEYS.length - 1; i >= 0; i--)
    if (uniq(upTo(i), KEYS[i]).length > 1) return i;
  return -1;
}
// the arrows step the group last clicked while it still has a choice,
// otherwise the last group with one; Play keeps the last group
function arrowIndex() {
  const i = navKey ? KEYS.indexOf(navKey) : -1;
  return (i >= 0 && uniq(upTo(i), KEYS[i]).length > 1) ? i : navIndex();
}
function stepKey(i, dir) {
  if (i < 0) return false;
  const k = KEYS[i], vals = uniq(upTo(i), k), j = vals.indexOf(state[k]) + dir;
  if (j < 0 || j >= vals.length) return false;
  choose(i, vals[j]); return true;
}
function step(dir) { return stepKey(navIndex(), dir); }
function preloadNext() {
  const i = navIndex(); if (i < 0) return;
  const k = KEYS[i], vals = uniq(upTo(i), k), j = vals.indexOf(state[k]) + 1;
  if (j >= vals.length) return;
  const m = DB.find(d => KEYS.every(x => d[x] === (x === k ? vals[j] : state[x])));
  if (m) (new Image()).src = buildSrc(m);
}
let timer = null;
function togglePlay() {
  const b = document.getElementById('btnp');
  if (timer) { clearInterval(timer); timer = null; b.innerHTML = '&#9654; Play'; b.classList.remove('on'); return; }
  const fps = parseFloat(document.getElementById('speed').value) || 2;
  timer = setInterval(() => {
    if (step(+1)) return;
    if (document.getElementById('loop').checked) {
      const i = navIndex(); if (i >= 0) choose(i, uniq(upTo(i), KEYS[i])[0]);
    } else togglePlay();
  }, 1000 / fps);
  b.innerHTML = '&#10074;&#10074; Pause'; b.classList.add('on');
}

document.addEventListener('keydown', e => {
  if (e.target.tagName === 'SELECT' || e.target.tagName === 'INPUT') return;
  const lbOpen = document.getElementById('lightbox').classList.contains('open');
  if (e.key === 'Escape') { document.getElementById('lightbox').classList.remove('open');
                            document.getElementById('help').classList.remove('open'); return; }
  if ((e.key === 'ArrowRight' || e.key === 'ArrowLeft') && !lbOpen) {
    stepKey(arrowIndex(), e.key === 'ArrowRight' ? +1 : -1); e.preventDefault();
  }
  else if (e.key === 'f' || e.key === 'F') flip();
  else if (e.key === 'b' || e.key === 'B') flipFlop();
  else if (e.key === 'w' || e.key === 'W') toggleFit();
  else if (e.key === 'z' || e.key === 'Z') { lbOpen ? document.getElementById('lightbox').classList.remove('open') : openLightbox(); }
  else if (e.key === '?') toggleHelp();
  else if (e.key === '+' || e.key === '=') zoomBy(+1);
  else if (e.key === '-' || e.key === '_') zoomBy(-1);
  else if (e.key === '0') zoomTo(1);
  else if (e.key === ' ' && PLAY) { togglePlay(); e.preventDefault(); }
});

// the About box stays as it was left
const about = document.getElementById('about');
if (about) {
  try { if (localStorage.getItem(STORE + ':about') === '1') about.open = true; } catch (e) {}
  about.addEventListener('toggle', () => {
    try { localStorage.setItem(STORE + ':about', about.open ? '1' : '0'); } catch (e) {}
  });
}

cascade(0, readHash());
KEYS.forEach(remember);
draw(); showImage(); saveHash();
</script>
</body>
</html>
"""
