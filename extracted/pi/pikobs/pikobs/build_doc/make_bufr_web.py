#!/usr/bin/env python
"""The BUFR code search of the Varno page, on a page of its own in sites8.

The Varno page of the documentation searches the CMC table B with two files
of docs/source/_static: varno_search.js, the data (make_varno_search.py),
and varno_search_widget.js, the search itself. This page uses the same two
files, copied next to it, with the same box and the same references, so it
behaves as the page does -- a code (12163), a word in English or in French
(brightness, humidité) or a family (ro, iasi), and index.html?varno=12163 --
and follows it when it changes:

    python pikobs/build_doc/make_bufr_web.py [--out ~/sites8/pikobs_bufr]

Run it again after make_varno_search.py.
"""
import argparse
import datetime
import os
import shutil
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
STATIC = os.path.join(REPO, "docs", "source", "_static")
FILES = ("varno_search.js", "varno_search_widget.js")

PAGE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pikobs -- BUFR codes</title>
<style>
  body { margin:0; font:15px/1.55 -apple-system, "Segoe UI", Roboto, sans-serif;
         color:#1F2933; background:#F7F8FA; }
  header { background:#1F2933; color:#fff; padding:14px 22px; display:flex;
           align-items:baseline; gap:18px; flex-wrap:wrap; }
  header h1 { margin:0; font-size:20px; }
  header .sub { color:#C7CDD4; font-size:13px; }
  header a { color:#fff; margin-left:auto; font-size:13px; text-decoration:none;
             border:1px solid rgba(255,255,255,.45); border-radius:4px; padding:4px 10px; }
  main { max-width:1100px; margin:0 auto; padding:18px 22px 40px; }
  p { margin:0 0 12px; }
  a { color:#2166AC; }
  code { background:#EEF0F3; padding:0 4px; border-radius:3px; font-size:.92em; }
  .varno-search { background:#fff; border:1px solid #E5E7EB; border-radius:6px;
                  padding:14px 16px; margin:16px 0; }
  #varno-search-input { width:100%; max-width:42em; padding:.5em .7em; font-size:1.05em;
                        border:1px solid #CBD2D9; border-radius:6px; }
  #varno-search-results table { border-collapse:collapse; width:100%; margin-top:12px;
                                font-size:14px; }
  #varno-search-results th, #varno-search-results td { border-bottom:1px solid #E5E7EB;
                                text-align:left; padding:6px 8px; vertical-align:top; }
  #varno-search-results th { background:#F3F4F6; color:#6B7280; font-size:12px;
                             text-transform:uppercase; letter-spacing:.04em; }
  .note { color:#6B7280; font-size:13px; }
</style></head>
<body>
<header><h1>BUFR codes</h1>
  <span class="sub">CMC table B, and where the Pikobs families carry each code &middot; __DATE__</span>
  __DOC__
</header>
<main>
<p>Type a BUFR code (<code>12163</code>), a word in English or in French
(<code>brightness</code>, <code>humidité</code>) or a family (<code>ro</code>,
<code>iasi</code>). The search gives the name in both languages from the CMC
table B, the unit, and the families that assimilate the code or only carry it.</p>

<div class="varno-search">
  <input id="varno-search-input" type="search" autocomplete="off" autofocus
         placeholder="A BUFR code (12163), a word (brightness, humidité) or a family (iasi)">
  <div id="varno-search-results"></div>
</div>

<p>The families are read in two places of the chain. The postalt files, the
ones the modules read, say what is left at the end and what is assimilated.
The cutoff files say what arrives, and some of it is dropped on the way: the
bending angle of <code>ro</code> (<code>15037</code>) is in the cutoff files
and gone by derialt, where only the refractivity is kept. Such a code shows
under <i>Only in cutoff</i>.</p>

<p class="refs">References: <a href="https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes" target="_blank">WMO Manual on Codes, Volume I.2 (WMO-No. 306)</a> &middot; <a href="https://wmo.int/latest-version" target="_blank">WMO current tables</a></p>

</main>
<script src="varno_search.js"></script>
<script src="varno_search_widget.js"></script>
</body></html>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=os.path.expanduser("~/sites8/pikobs_bufr"))
    ap.add_argument("--static", default=STATIC,
                    help="the _static folder of the documentation")
    args = ap.parse_args(argv)
    missing = [f for f in FILES if not os.path.isfile(os.path.join(args.static, f))]
    if missing:
        print(f"[bufr] not in {args.static}: {', '.join(missing)} -- run "
              f"make_varno_search.py, or build the documentation, first",
              file=sys.stderr)
        return 1
    os.makedirs(args.out, exist_ok=True)
    for f in FILES:
        shutil.copy2(os.path.join(args.static, f), os.path.join(args.out, f))
    data = os.path.join(args.static, FILES[0])
    n = open(data, encoding="utf-8").read().count('"code":')
    # the documentation is moving: a label, no link, until it has its place
    doc = ('<span style="margin-left:auto;font-size:13px;color:#C7CDD4;'
           'border:1px dashed rgba(255,255,255,.35);border-radius:4px;'
           'padding:4px 10px">Documentation: coming soon</span>')
    date = datetime.datetime.fromtimestamp(os.path.getmtime(data)).strftime("%Y-%m-%d")
    page = PAGE.replace("__DATE__", f"{n:,} codes, data of {date}").replace("__DOC__", doc)
    index = os.path.join(args.out, "index.html")
    with open(index, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"[bufr] {n:,} codes -> {index}")
    try:
        from pikobs.web.viewer import announce_viewer
        announce_viewer(index)
    except Exception:
        print(f"Viewer: {index}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
