"""
pikobs.web.viewer
=================
Generic, module-agnostic HTML viewer for collections of PNG figures
indexed by a small number of categorical keys (family, region,
surface, station, ...).
Design
------
The viewer makes no assumption about *what* the PNGs are or *how*
their filenames are built. The producing module is responsible for:
* building the list of items, one dict per PNG, where each dict
  contains every key that should drive a dropdown PLUS a
  ``"filename"`` entry,
* deciding the ORDER in which dropdowns appear (``keys``),
* providing pretty labels for selected values if needed
  (``value_labels``).
The viewer takes that, writes a self-contained HTML file with:
* cascading dropdowns,
* a flip button (toggle current vs previous image, hotkey ``F``),
* an image container with a FIXED aspect ratio so the layout never
  jumps when images of slightly different pixel sizes are swapped.
Returns the path of the generated HTML file.
Two HTML viewers can coexist in the same directory by giving them
different ``output_path`` filenames (one per producing module).
"""
import json
import os
from typing import Iterable, Mapping, Optional

# Default dropdown captions if the producer does not supply one.
_DEFAULT_KEY_LABELS = {
    "family"    : "Family",
    "region"    : "Region",
    "surface"   : "Land filter",
    "land_ocean": "Land filter",
    "special"   : "Special",
    "experience": "Experience",
    "panel"     : "Panel",
    "id_stn"    : "Station",
    "varno"     : "Varno",
    "vcoord"    : "Vcoord",
    "function"  : "Function",
    "criteria"  : "Criteria",
    "channel"   : "Channel",
    "experiment": "Experiment",
    "date"      : "Date",
    "level"     : "Level",
    "layer"     : "Layer",          # B) added
    "mode"      : "Mode",
    "flag"      : "Flag",
}


def _stringify(items, keys):
    """Coerce every key value to a plain string (JSON safe, sortable)."""
    out = []
    for it in items:
        rec = {}
        for k in keys:
            if k not in it:
                raise KeyError(f"item is missing key {k!r}: {it!r}")
            rec[k] = str(it[k]).strip()
        if "filename" not in it:
            raise KeyError(f"item is missing 'filename': {it!r}")
        rec["filename"] = str(it["filename"])
        out.append(rec)
    return out


# the web server of the home folders: https://<host>/~<user>/<entry of public_html>/...
WEB_HOST = "goc-dx-u3.science.gc.ca"

# where the Pikobs documentation lives: the one line to change the day it
# moves ($PIKOBS_DOCS_URL overrides it without touching the code)
DOCS_URL = "https://goc-dx-u3.science.gc.ca/~dlo001/Pikobs/docs/build/html"


def docs_url(page: str) -> str:
    """The address of a page of the documentation, e.g. docs_url("stats.html")."""
    return f"{(os.environ.get('PIKOBS_DOCS_URL') or DOCS_URL).rstrip('/')}/{page}"



def _doc_link(output_path, doc_page=None):
    """The documentation page of the module whose viewer this is:
    pikobs_<module>_viewer.html is documented in <module>.html, unless
    doc_page names another. None when the name says nothing."""
    import re
    if doc_page is None:
        m = re.match(r"pikobs_(\w+?)_viewer\.html$", os.path.basename(str(output_path)))
        if not m:
            return None
        doc_page = f"{m.group(1)}.html"
    return docs_url(doc_page) if doc_page else None


def announce_viewer(output_path: str) -> None:
    """Where the viewer is, and its address in a browser.

    Looks in ~/public_html for a link or folder that already shows the
    viewer's folder (~/public_html/sites8 -> ~/sites8, say) and gives the
    address through it -- the most specific one when several do. Otherwise
    the one ln -s that would, and the address it would then have. Without a
    ~/public_html, the path alone. The host: $PIKOBS_WEB_HOST, or WEB_HOST.
    """
    import getpass
    path = os.path.abspath(output_path)
    print(f"Viewer: {path}", flush=True)
    pub = os.path.expanduser("~/public_html")
    if not os.path.isdir(pub):
        return
    base = (f"https://{os.environ.get('PIKOBS_WEB_HOST') or WEB_HOST}"
            f"/~{getpass.getuser()}")
    real = os.path.realpath(path)
    try:
        names = sorted(os.listdir(pub))
    except OSError:
        names = []
    best = None
    for name in [""] + names:
        root = os.path.realpath(os.path.join(pub, name))
        if real.startswith(root.rstrip(os.sep) + os.sep):
            if best is None or len(root) > len(best[1]):
                best = (name, root)
    if best is not None:
        rel = os.path.relpath(real, best[1])
        print(f"Web:    {base}/{'/'.join(p for p in (best[0], rel) if p)}", flush=True)
        return
    folder = os.path.dirname(path)
    print("Web:    to open it in a browser, link the folder under public_html once:",
          flush=True)
    print(f"          ln -s {folder} {pub}/", flush=True)
    print(f"        then: {base}/{os.path.basename(folder)}/{os.path.basename(path)}",
          flush=True)


def generate_web(
    items: Iterable[Mapping],
    keys: list,
    output_path: str,
    *,
    title: str = "Pikobs Viewer",
    subtitle: Optional[str] = None,
    image_subdir_key: Optional[str] = None,
    value_labels: Optional[Mapping[str, Mapping[str, str]]] = None,
    key_labels: Optional[Mapping[str, str]] = None,
    issues_url: Optional[str] = None,
    doc_page: Optional[str] = None,
    enable_play: bool = False,
) -> str:
    """Render a self-contained HTML viewer for a list of PNG items.

    Parameters
    ----------
    enable_play:
        If True, add Play/Pause/Speed/Loop controls that animate over
        the last dropdown axis.  Use for time-series viewers (mapobs).
        Default False (scatter, profile).
    """
    items_str = _stringify(list(items), keys)
    captions = []
    for i, k in enumerate(keys, start=1):
        if key_labels and k in key_labels:
            captions.append((k, key_labels[k]))
        elif k in _DEFAULT_KEY_LABELS:
            captions.append((k, _DEFAULT_KEY_LABELS[k]))
        else:
            captions.append((k, k.replace("_", " ").title()))

    if os.environ.get("PIKOBS_OLD_VIEWER"):
        json_items   = json.dumps(items_str)
        json_keys    = json.dumps(keys)
        json_vlabels = json.dumps(dict(value_labels) if value_labels else {})
        js_subdir    = json.dumps(image_subdir_key) if image_subdir_key else "null"

        dropdown_html = "\n".join(
            f'    <div class="cg"><label>{i}. {label}</label>'
            f'<select id="s{i-1}" onchange="render({i-1})"></select></div>'
            for i, (_, label) in enumerate(captions, start=1)
        )

        sub_html    = f'<p>{subtitle}</p>' if subtitle else ''
        footer_html = ''
        if issues_url:
            footer_html = (
                f'<div class="footer">Issues: '
                f'<a href="{issues_url}" target="_blank">{issues_url}</a></div>'
            )

        play_key_label = captions[-1][1] if captions else ""
        template = _HTML_TEMPLATE_PLAY if enable_play else _HTML_TEMPLATE
        html = template.format(
            title=title,
            sub_html=sub_html,
            dropdown_html=dropdown_html,
            footer_html=footer_html,
            json_items=json_items,
            json_keys=json_keys,
            json_vlabels=json_vlabels,
            js_subdir=js_subdir,
            play_key_label=play_key_label,
        )
    else:
        # buttons on the left, the figure on the right (viewer_page.py)
        from pikobs.web.viewer_page import render_page
        html = render_page(items_str, keys, captions, title=title,
                           subtitle=subtitle,
                           image_subdir_key=image_subdir_key,
                           value_labels=value_labels,
                           issues_url=issues_url,
                           enable_play=enable_play,
                           doc_link=_doc_link(output_path, doc_page))

    out_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(
        f"[viewer] wrote {output_path}  "
        f"({len(items_str)} items, {len(keys)} keys)"
    )
    announce_viewer(output_path)
    return output_path


# =============================================================================
# HTML template  — Play/Speed/Loop removed (C)
# =============================================================================
_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{font-family:'Segoe UI',sans-serif;background:#f4f7f6;margin:0;padding:0;}}
  .header {{background:#2c3e50;color:white;padding:18px;text-align:center;}}
  .header p {{margin:4px 0;font-size:13px;color:#bdc3c7;}}
  .container {{max-width:1400px;margin:18px auto;padding:0 18px;}}
  .controls {{display:flex;flex-wrap:wrap;gap:12px;background:white;padding:16px;
              border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.1);
              margin-bottom:18px;justify-content:center;align-items:flex-end;}}
  .cg {{display:flex;flex-direction:column;}}
  label {{font-weight:bold;margin-bottom:4px;font-size:12px;color:#34495e;
          text-transform:uppercase;letter-spacing:.4px;}}
  select {{padding:8px;font-size:13px;border:1px solid #bdc3c7;border-radius:4px;
           min-width:140px;cursor:pointer;}}
  select:focus {{outline:none;border-color:#3498db;}}
  .btn {{color:white;border:none;padding:9px 16px;
         font-size:13px;font-weight:bold;border-radius:4px;cursor:pointer;
         height:38px;white-space:nowrap;}}
  .btn-flip {{background:#3498db;}}
  .btn-flip:hover {{background:#2980b9;}}
  .btn-flip.active {{background:#e67e22;}}
  .btn:disabled {{background:#95a5a6;cursor:not-allowed;}}
  .imgbox {{background:white;padding:18px;border-radius:8px;
            box-shadow:0 2px 6px rgba(0,0,0,.1);
            display:flex;flex-direction:column;align-items:center;}}
  .imgwrap {{position:relative;width:100%;max-height:85vh;
             aspect-ratio:1 / 1;
             display:flex;align-items:center;justify-content:center;
             background:#fafbfc;border-radius:4px;overflow:hidden;}}
  .imgwrap img {{position:absolute;top:0;left:0;width:100%;height:100%;
                 object-fit:contain;
                 opacity:0;pointer-events:none;
                 transition:opacity 0.15s ease-in-out;
                 cursor:zoom-in;}}
  .imgwrap img.show {{opacity:1;pointer-events:auto;}}
  .imgwrap.fitwidth {{max-height:none;}}
  .err {{color:#e74c3c;font-weight:bold;font-size:16px;
         position:absolute;display:none;background:white;padding:14px 22px;
         border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15);z-index:5;}}
  .pathbar {{margin-top:12px;font-family:monospace;color:#7f8c8d;font-size:12px;
             background:#ecf0f1;padding:8px 12px;border-radius:4px;
             width:100%;box-sizing:border-box;word-break:break-all;}}
  .footer {{text-align:center;padding:16px;color:#7f8c8d;font-size:13px;
            background:#ecf0f1;margin-top:auto;}}
  .footer a {{color:#3498db;text-decoration:none;font-weight:bold;}}
  .hint {{text-align:center;color:#95a5a6;font-size:11px;margin-top:8px;
          font-style:italic;}}
  .lightbox {{display:none;position:fixed;top:0;left:0;width:100%;height:100%;
              background:rgba(20,20,20,.92);z-index:1000;
              overflow:auto;text-align:center;cursor:zoom-out;}}
  .lightbox.open {{display:block;}}
  .lightbox img {{max-width:none;margin:40px auto;display:block;
                   box-shadow:0 4px 24px rgba(0,0,0,.5);}}
  .lightbox-hint {{position:fixed;top:14px;right:18px;color:#ecf0f1;
                    font-size:13px;font-family:monospace;z-index:1001;}}
</style>
</head>
<body>
<div class="header">
  <h2 style="margin:0">{title}</h2>
  {sub_html}
</div>
<div class="container">
  <div class="controls">
{dropdown_html}
    <button id="btnf" class="btn btn-flip" onclick="flip()" disabled
            title="Flip current vs previous (hotkey: F)">&#8644; Flip</button>
    <button id="btnw" class="btn btn-flip" onclick="toggleFit()"
            title="Fit to the screen or to the width (hotkey: W)">&#10530; Fit</button>
  </div>
  <div class="imgbox">
    <div id="wrap" class="imgwrap">
      <div id="err" class="err">&#9888; Image not found on disk.</div>
      <img id="imgA" onerror="onErr()" onload="onLoad(this)" onclick="openLightbox()">
      <img id="imgB" onerror="onErr()" onload="onLoad(this)" onclick="openLightbox()">
    </div>
    <div id="path" class="pathbar">Initializing...</div>
    <div class="hint">Hotkey: <b>F</b> flip &nbsp; <b>W</b> fit &nbsp; Click image to zoom</div>
  </div>
</div>
{footer_html}
<div id="lightbox" class="lightbox" onclick="closeLightbox()">
  <div class="lightbox-hint">Click anywhere or press Esc to close</div>
  <img id="lightboxImg">
</div>
<script>
const DB         = {json_items};
const KEYS       = {json_keys};
const VAL_LABELS = {json_vlabels};
const SUBDIR_KEY = {js_subdir};

let state    = Object.fromEntries(KEYS.map(k => [k, null]));
let curSrc   = '';
let prevSrc  = '';
let showPrev = false;
let curImg   = 'imgA';
let prevImg  = 'imgB';
let aspectLocked = false;

function natsort(a, b) {{
  return String(a).localeCompare(String(b), undefined,
                                 {{numeric: true, sensitivity: 'base'}});
}}
function uniq(data, key) {{
  return [...new Set(data.map(d => d[key]))].sort(natsort);
}}
function pretty(key, val) {{
  return (VAL_LABELS[key] && VAL_LABELS[key][val]) ? VAL_LABELS[key][val] : val;
}}
function fill(selId, vals, prev, key) {{
  const sel = document.getElementById(selId); sel.innerHTML = '';
  vals.forEach(v => sel.add(new Option(pretty(key, v), v)));
  sel.value = (prev && vals.includes(prev)) ? prev : (vals[0] ?? '');
}}
function render(level) {{
  if (level === -1) fill('s0', uniq(DB, KEYS[0]), null, KEYS[0]);
  state[KEYS[0]] = document.getElementById('s0').value;
  let sub = DB;
  for (let idx = 1; idx < KEYS.length; idx++) {{
    if (level <= idx - 1) {{
      sub = DB.filter(d =>
          KEYS.slice(0, idx).every(k => d[k] === state[k]));
      fill('s' + idx, uniq(sub, KEYS[idx]), state[KEYS[idx]], KEYS[idx]);
    }}
    state[KEYS[idx]] = document.getElementById('s' + idx).value;
  }}
  showImage();
}}
function buildSrc(item) {{
  return SUBDIR_KEY ? item[SUBDIR_KEY] + '/' + item.filename : item.filename;
}}
function showImage() {{
  const m = DB.find(d => KEYS.every(k => d[k] === state[k]));
  if (!m) return;
  const src = buildSrc(m);
  if (src !== curSrc) {{
    if (curSrc) {{ prevSrc = curSrc; document.getElementById('btnf').disabled = false; }}
    curSrc = src; showPrev = false;
    document.getElementById('btnf').classList.remove('active');
  }}
  apply(curSrc);
}}
function apply(src) {{
  document.getElementById('err').style.display = 'none';
  document.getElementById('path').textContent = src;
  const next = document.getElementById(prevImg);
  next.onload = () => {{
    setAspect(next);
    document.getElementById(curImg).classList.remove('show');
    next.classList.add('show');
    const swap = curImg; curImg = prevImg; prevImg = swap;
    document.getElementById('err').style.display = 'none';
  }};
  next.onerror = onErr;
  next.src = src;
}}
let fitMode = 'auto';      // auto | width | screen
let lockedRatio = 0;
function setAspect(img) {{
  if (!img.naturalWidth || !img.naturalHeight) return;
  const r = img.naturalHeight / img.naturalWidth;
  // follow the figure, but only when its shape really changes: two
  // figures of nearly the same size keep the frame, so Flip does not jump
  if (!lockedRatio || Math.abs(r - lockedRatio) / lockedRatio > 0.10) {{
    lockedRatio = r;
    document.getElementById('wrap').style.aspectRatio =
      img.naturalWidth + ' / ' + img.naturalHeight;
  }}
  applyFit();
}}
function applyFit() {{
  // a figure taller than wide goes to the full width and the page
  // scrolls: squeezed into the screen height its labels are unreadable
  const tall  = lockedRatio > 1.15;
  const width = fitMode === 'width' || (fitMode === 'auto' && tall);
  document.getElementById('wrap').classList.toggle('fitwidth', width);
  const b = document.getElementById('btnw');
  if (b) b.innerHTML = width ? '&#10530; Fit: width' : '&#10530; Fit: screen';
}}
function toggleFit() {{
  const width = document.getElementById('wrap').classList.contains('fitwidth');
  fitMode = width ? 'screen' : 'width';
  applyFit();
}}
function flip() {{
  if (!prevSrc) return;
  showPrev = !showPrev;
  document.getElementById('btnf').classList.toggle('active', showPrev);
  apply(showPrev ? prevSrc : curSrc);
}}
function onErr() {{
  document.getElementById('err').style.display = 'block';
}}
function onLoad(img) {{
  setAspect(img);
  img.classList.add('show');
}}
function openLightbox() {{
  if (!curSrc) return;
  const shown = showPrev ? prevSrc : curSrc;
  document.getElementById('lightboxImg').src = shown;
  document.getElementById('lightbox').classList.add('open');
}}
function closeLightbox() {{
  document.getElementById('lightbox').classList.remove('open');
}}
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') {{ closeLightbox(); return; }}
  if (e.target.tagName === 'SELECT') return;
  if (e.key === 'f' || e.key === 'F') {{ flip(); e.preventDefault(); }}
  else if (e.key === 'w' || e.key === 'W') {{ toggleFit(); e.preventDefault(); }}
}});
if (DB.length > 0) render(-1);
else document.getElementById('path').textContent = 'ERROR: items list is empty.';
</script>
</body>
</html>
"""



# =============================================================================
# HTML template WITH play controls (enable_play=True, e.g. mapobs)
# =============================================================================
_HTML_TEMPLATE_PLAY = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{font-family:'Segoe UI',sans-serif;background:#f4f7f6;margin:0;padding:0;}}
  .header {{background:#2c3e50;color:white;padding:18px;text-align:center;}}
  .header p {{margin:4px 0;font-size:13px;color:#bdc3c7;}}
  .container {{max-width:1400px;margin:18px auto;padding:0 18px;}}
  .controls {{display:flex;flex-wrap:wrap;gap:12px;background:white;padding:16px;
              border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.1);
              margin-bottom:18px;justify-content:center;align-items:flex-end;}}
  .cg {{display:flex;flex-direction:column;}}
  label {{font-weight:bold;margin-bottom:4px;font-size:12px;color:#34495e;
          text-transform:uppercase;letter-spacing:.4px;}}
  select {{padding:8px;font-size:13px;border:1px solid #bdc3c7;border-radius:4px;
           min-width:140px;cursor:pointer;}}
  select:focus {{outline:none;border-color:#3498db;}}
  .btn {{color:white;border:none;padding:9px 16px;
         font-size:13px;font-weight:bold;border-radius:4px;cursor:pointer;
         height:38px;white-space:nowrap;}}
  .btn-flip {{background:#3498db;}}
  .btn-flip:hover {{background:#2980b9;}}
  .btn-flip.active {{background:#e67e22;}}
  .btn-play {{background:#27ae60;min-width:90px;}}
  .btn-play:hover {{background:#1f8c4d;}}
  .btn-play.playing {{background:#c0392b;}}
  .btn-loop {{background:#7f8c8d;min-width:38px;padding:9px 10px;}}
  .btn-loop.on {{background:#16a085;}}
  .btn:disabled {{background:#95a5a6;cursor:not-allowed;}}
  .imgbox {{background:white;padding:18px;border-radius:8px;
            box-shadow:0 2px 6px rgba(0,0,0,.1);
            display:flex;flex-direction:column;align-items:center;}}
  .imgwrap {{position:relative;width:100%;max-height:85vh;
             aspect-ratio:1 / 1;
             display:flex;align-items:center;justify-content:center;
             background:#fafbfc;border-radius:4px;overflow:hidden;}}
  .imgwrap img {{position:absolute;top:0;left:0;width:100%;height:100%;
                 object-fit:contain;
                 opacity:0;pointer-events:none;
                 transition:opacity 0.15s ease-in-out;
                 cursor:zoom-in;}}
  .imgwrap img.show {{opacity:1;pointer-events:auto;}}
  .imgwrap.fitwidth {{max-height:none;}}
  .err {{color:#e74c3c;font-weight:bold;font-size:16px;
         position:absolute;display:none;background:white;padding:14px 22px;
         border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15);z-index:5;}}
  .pathbar {{margin-top:12px;font-family:monospace;color:#7f8c8d;font-size:12px;
             background:#ecf0f1;padding:8px 12px;border-radius:4px;
             width:100%;box-sizing:border-box;word-break:break-all;}}
  .footer {{text-align:center;padding:16px;color:#7f8c8d;font-size:13px;
            background:#ecf0f1;margin-top:auto;}}
  .footer a {{color:#3498db;text-decoration:none;font-weight:bold;}}
  .hint {{text-align:center;color:#95a5a6;font-size:11px;margin-top:8px;
          font-style:italic;}}
  .lightbox {{display:none;position:fixed;top:0;left:0;width:100%;height:100%;
              background:rgba(20,20,20,.92);z-index:1000;
              overflow:auto;text-align:center;cursor:zoom-out;}}
  .lightbox.open {{display:block;}}
  .lightbox img {{max-width:none;margin:40px auto;display:block;
                   box-shadow:0 4px 24px rgba(0,0,0,.5);}}
  .lightbox-hint {{position:fixed;top:14px;right:18px;color:#ecf0f1;
                    font-size:13px;font-family:monospace;z-index:1001;}}
</style>
</head>
<body>
<div class="header">
  <h2 style="margin:0">{title}</h2>
  {sub_html}
</div>
<div class="container">
  <div class="controls">
{dropdown_html}
    <button id="btnf" class="btn btn-flip" onclick="flip()" disabled
            title="Flip current vs previous (hotkey: F)">&#8644; Flip</button>
    <button id="btnw" class="btn btn-flip" onclick="toggleFit()"
            title="Fit to the screen or to the width (hotkey: W)">&#10530; Fit</button>
    <div class="cg">
      <label>Speed</label>
      <select id="speed">
        <option value="250">0.25 s</option>
        <option value="500">0.5 s</option>
        <option value="1000" selected>1 s</option>
        <option value="2000">2 s</option>
      </select>
    </div>
    <button id="btnp" class="btn btn-play" onclick="togglePlay()"
            title="Play / pause animation over {play_key_label} (hotkey: Space)">
      &#9654; Play
    </button>
    <button id="btnl" class="btn btn-loop on" onclick="toggleLoop()"
            title="Loop at end of sequence">&#x1F501;</button>
  </div>
  <div class="imgbox">
    <div id="wrap" class="imgwrap">
      <div id="err" class="err">&#9888; Image not found on disk.</div>
      <img id="imgA" onerror="onErr()" onload="onLoad(this)" onclick="openLightbox()">
      <img id="imgB" onerror="onErr()" onload="onLoad(this)" onclick="openLightbox()">
    </div>
    <div id="path" class="pathbar">Initializing...</div>
    <div class="hint">Hotkeys: <b>F</b> flip &nbsp; <b>Space</b> play/pause &nbsp; <b>W</b> fit &nbsp; Click image to zoom</div>
  </div>
</div>
{footer_html}
<div id="lightbox" class="lightbox" onclick="closeLightbox()">
  <div class="lightbox-hint">Click anywhere or press Esc to close</div>
  <img id="lightboxImg">
</div>
<script>
const DB         = {json_items};
const KEYS       = {json_keys};
const VAL_LABELS = {json_vlabels};
const SUBDIR_KEY = {js_subdir};
const PLAY_KEY   = KEYS[KEYS.length - 1];

let state    = Object.fromEntries(KEYS.map(k => [k, null]));
let curSrc   = '';
let prevSrc  = '';
let showPrev = false;
let curImg   = 'imgA';
let prevImg  = 'imgB';
let aspectLocked = false;
let playing   = false;
let playTimer = null;
let loopOn    = true;
const PRELOAD_AHEAD = 3;

function natsort(a, b) {{
  return String(a).localeCompare(String(b), undefined,
                                 {{numeric: true, sensitivity: 'base'}});
}}
function uniq(data, key) {{
  return [...new Set(data.map(d => d[key]))].sort(natsort);
}}
function pretty(key, val) {{
  return (VAL_LABELS[key] && VAL_LABELS[key][val]) ? VAL_LABELS[key][val] : val;
}}
function fill(selId, vals, prev, key) {{
  const sel = document.getElementById(selId); sel.innerHTML = '';
  vals.forEach(v => sel.add(new Option(pretty(key, v), v)));
  sel.value = (prev && vals.includes(prev)) ? prev : (vals[0] ?? '');
}}
function render(level) {{
  if (level === -1) fill('s0', uniq(DB, KEYS[0]), null, KEYS[0]);
  state[KEYS[0]] = document.getElementById('s0').value;
  let sub = DB;
  for (let idx = 1; idx < KEYS.length; idx++) {{
    if (level <= idx - 1) {{
      sub = DB.filter(d =>
          KEYS.slice(0, idx).every(k => d[k] === state[k]));
      fill('s' + idx, uniq(sub, KEYS[idx]), state[KEYS[idx]], KEYS[idx]);
    }}
    state[KEYS[idx]] = document.getElementById('s' + idx).value;
  }}
  showImage();
}}
function buildSrc(item) {{
  return SUBDIR_KEY ? item[SUBDIR_KEY] + '/' + item.filename : item.filename;
}}
function showImage() {{
  const m = DB.find(d => KEYS.every(k => d[k] === state[k]));
  if (!m) return;
  const src = buildSrc(m);
  if (src !== curSrc) {{
    if (curSrc) {{ prevSrc = curSrc; document.getElementById('btnf').disabled = false; }}
    curSrc = src; showPrev = false;
    document.getElementById('btnf').classList.remove('active');
  }}
  apply(curSrc);
  preloadAhead();
}}
function apply(src) {{
  document.getElementById('err').style.display = 'none';
  document.getElementById('path').textContent = src;
  const next = document.getElementById(prevImg);
  next.onload = () => {{
    setAspect(next);
    document.getElementById(curImg).classList.remove('show');
    next.classList.add('show');
    const swap = curImg; curImg = prevImg; prevImg = swap;
    document.getElementById('err').style.display = 'none';
  }};
  next.onerror = onErr;
  next.src = src;
}}
let fitMode = 'auto';      // auto | width | screen
let lockedRatio = 0;
function setAspect(img) {{
  if (!img.naturalWidth || !img.naturalHeight) return;
  const r = img.naturalHeight / img.naturalWidth;
  // follow the figure, but only when its shape really changes: two
  // figures of nearly the same size keep the frame, so Flip does not jump
  if (!lockedRatio || Math.abs(r - lockedRatio) / lockedRatio > 0.10) {{
    lockedRatio = r;
    document.getElementById('wrap').style.aspectRatio =
      img.naturalWidth + ' / ' + img.naturalHeight;
  }}
  applyFit();
}}
function applyFit() {{
  // a figure taller than wide goes to the full width and the page
  // scrolls: squeezed into the screen height its labels are unreadable
  const tall  = lockedRatio > 1.15;
  const width = fitMode === 'width' || (fitMode === 'auto' && tall);
  document.getElementById('wrap').classList.toggle('fitwidth', width);
  const b = document.getElementById('btnw');
  if (b) b.innerHTML = width ? '&#10530; Fit: width' : '&#10530; Fit: screen';
}}
function toggleFit() {{
  const width = document.getElementById('wrap').classList.contains('fitwidth');
  fitMode = width ? 'screen' : 'width';
  applyFit();
}}
function flip() {{
  if (!prevSrc) return;
  showPrev = !showPrev;
  document.getElementById('btnf').classList.toggle('active', showPrev);
  apply(showPrev ? prevSrc : curSrc);
}}
function onErr() {{ document.getElementById('err').style.display = 'block'; }}
function onLoad(img) {{
  setAspect(img);
  img.classList.add('show');
}}
function preloadAhead() {{
  const sel = document.getElementById('s' + (KEYS.length - 1));
  if (!sel) return;
  const opts = Array.from(sel.options).map(o => o.value);
  const idx  = opts.indexOf(sel.value);
  if (idx < 0) return;
  for (let k = 1; k <= PRELOAD_AHEAD; k++) {{
    const nextIdx = idx + k;
    if (nextIdx >= opts.length) break;
    const probeState = {{...state, [PLAY_KEY]: opts[nextIdx]}};
    const m = DB.find(d => KEYS.every(k => d[k] === probeState[k]));
    if (m) {{ const img = new Image(); img.src = buildSrc(m); }}
  }}
}}
function togglePlay() {{ playing ? stopPlay() : startPlay(); }}
function startPlay() {{
  const sel = document.getElementById('s' + (KEYS.length - 1));
  if (!sel || sel.options.length <= 1) return;
  playing = true;
  document.getElementById('btnp').classList.add('playing');
  document.getElementById('btnp').innerHTML = '&#10073;&#10073; Pause';
  scheduleNext();
}}
function stopPlay() {{
  playing = false;
  if (playTimer) {{ clearTimeout(playTimer); playTimer = null; }}
  document.getElementById('btnp').classList.remove('playing');
  document.getElementById('btnp').innerHTML = '&#9654; Play';
}}
function scheduleNext() {{
  if (!playing) return;
  const speed = parseInt(document.getElementById('speed').value, 10);
  playTimer = setTimeout(advancePlay, speed);
}}
function advancePlay() {{
  if (!playing) return;
  const sel  = document.getElementById('s' + (KEYS.length - 1));
  const opts = Array.from(sel.options).map(o => o.value);
  const idx  = opts.indexOf(sel.value);
  let next   = idx + 1;
  if (next >= opts.length) {{
    if (loopOn) {{ next = 0; }} else {{ stopPlay(); return; }}
  }}
  sel.value = opts[next];
  render(KEYS.length - 1);
  scheduleNext();
}}
function toggleLoop() {{
  loopOn = !loopOn;
  document.getElementById('btnl').classList.toggle('on', loopOn);
}}
function openLightbox() {{
  if (!curSrc) return;
  const shown = showPrev ? prevSrc : curSrc;
  document.getElementById('lightboxImg').src = shown;
  document.getElementById('lightbox').classList.add('open');
}}
function closeLightbox() {{
  document.getElementById('lightbox').classList.remove('open');
}}
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') {{ closeLightbox(); return; }}
  if (e.target.tagName === 'SELECT') return;
  if (e.key === 'f' || e.key === 'F') {{ flip(); e.preventDefault(); }}
  else if (e.key === 'w' || e.key === 'W') {{ toggleFit(); e.preventDefault(); }}
  else if (e.key === ' ' || e.code === 'Space') {{ togglePlay(); e.preventDefault(); }}
}});
if (DB.length > 0) render(-1);
else document.getElementById('path').textContent = 'ERROR: items list is empty.';
</script>
</body>
</html>
"""

# =============================================================================
# CLI - useful for quick standalone testing
# =============================================================================
def _cli():
    """
    Tiny CLI for standalone testing::
        python -m pikobs.web.viewer items.json keys.json output.html
    """
    import argparse
    p = argparse.ArgumentParser(
        description="Generate the generic Pikobs HTML viewer.",
    )
    p.add_argument("items_json", help="path to items list (JSON array)")
    p.add_argument("keys_json",  help="path to keys list (JSON array)")
    p.add_argument("output",     help="output .html path")
    p.add_argument("--title",    default="Pikobs Viewer")
    p.add_argument("--subtitle", default=None)
    p.add_argument("--image_subdir_key", default=None)
    p.add_argument("--value_labels_json", default=None,
                   help="optional JSON file of {key: {value: label}}")
    p.add_argument("--issues_url", default=None)
    a = p.parse_args()
    with open(a.items_json) as fh: items = json.load(fh)
    with open(a.keys_json)  as fh: keys  = json.load(fh)
    vlabels = None
    if a.value_labels_json:
        with open(a.value_labels_json) as fh: vlabels = json.load(fh)
    generate_web(
        items=items, keys=keys, output_path=a.output,
        title=a.title, subtitle=a.subtitle,
        image_subdir_key=a.image_subdir_key,
        value_labels=vlabels,
        issues_url=a.issues_url,
    )

if __name__ == "__main__":
    _cli()


