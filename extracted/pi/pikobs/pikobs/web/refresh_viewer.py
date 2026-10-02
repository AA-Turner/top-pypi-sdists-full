#!/usr/bin/env python
"""Rewrite a viewer already written, with the current page of the viewer.

A module writes its viewer at the end of a run; after a change of the page
(pikobs/web/viewer_page.py) this rewrites an existing one from the data it
holds -- the figures, the choices, the labels, the About text -- without
running the module again.

    python pikobs/web/refresh_viewer.py ~/sites8/pikobs_vdedr_cont_exp/pikobs_vdedr_viewer.html
    python pikobs/web/refresh_viewer.py ~/sites8/*/pikobs_*_viewer.html
"""
import html
import json
import os
import re
import sys


def _const(page, name):
    m = re.search(r"const " + name + r" = (.*?);\n", page, re.S)
    return json.loads(m.group(1).replace("<\\/", "</")) if m else None


def refresh(path):
    from pikobs.web.viewer_page import render_page
    page = open(path, encoding="utf-8").read()
    items, keys = _const(page, "DB"), _const(page, "KEYS")
    if items is None or keys is None or _const(page, "LABELS") is None:
        return f"skipped (not a viewer of the new page): {path}"
    labels = _const(page, "LABELS") or {}
    title = html.unescape(re.search(r"<title>(.*?)</title>", page, re.S).group(1))
    about = re.search(r'<div class="body">(.*?)</div></details>', page, re.S)
    issues = re.search(r'<footer>Issues: <a href="([^"]+)"', page)
    new = render_page(items, keys, [(k, labels.get(k, k)) for k in keys], title=title,
                      subtitle=about.group(1) if about else None,
                      image_subdir_key=_const(page, "SUBDIR_KEY"),
                      value_labels=_const(page, "VAL_LABELS") or None,
                      issues_url=html.unescape(issues.group(1)) if issues else None,
                      enable_play=_const(page, "PLAY") is True,
                      base_dir=_const(page, "BASE") or os.path.dirname(os.path.abspath(path)))
    open(path + ".new", "w", encoding="utf-8").write(new)
    os.replace(path + ".new", path)
    return f"refreshed: {path} ({len(items)} figures)"


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print("[viewer]", refresh(p))
