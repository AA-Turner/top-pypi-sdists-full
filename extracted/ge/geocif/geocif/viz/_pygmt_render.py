#!/usr/bin/env python3
"""Self-contained PyGMT choropleth renderer.

Imports ONLY pygmt + geopandas + stdlib (no geocif), so it can run inside a
pygmt-capable env (e.g. ``conda run -n pygmt_env python _pygmt_render.py ...``)
independently of the pipeline's runtime env. ``geocif.viz.plot._plot_map_pygmt``
preps a colored GeoDataFrame + a params dict, writes them to a temp GeoJSON +
JSON, and either calls :func:`render` in-process (when pygmt is importable) or
shells out to this file as a subprocess (the uv-venv bridge).

params JSON schema:
    {
      "out_path": str,
      "region": [w, e, s, n],
      "projection": "M15c",
      "title": str, "label": str,
      "do_borders": bool,
      "annotate": bool,               # use the "_label" column
      "admin1_borders": bool,         # overlay state/province lines (admin_2 maps)
      "colorbar": {
         "type": "continuous"|"qualitative"|"none",
         "colors": [hex, ...],        # continuous: ramp stops; qualitative: per-class
         "vmin": float, "vmax": float,      # continuous only
         "cat_labels": [str, ...]           # qualitative only
      }
    }
The GeoJSON carries a "_fill" (hex color) column and optional "_label" column.
"""
import os
import sys
import json
import tempfile

import geopandas as gpd

# The shared style constants live in the stdlib-only viz/_style.py so that
# GMT-free modules can import them too. The dual import keeps THIS file
# runnable both in-package and as a standalone script in the pygmt bridge
# env (same directory on sys.path, no geocif installed there).
try:
    from geocif.viz._style import (
        ANNOT_BOX, ANNOT_FONT, ANNOT_OFFSET, ANNOT_VAL_FONT,
        ANNOT_VAL_OFFSET, AREA_THRESH, BORDER_PEN, CBAR_POS, COAST_KW,
        NODATA, POLY_PEN)
except ImportError:  # standalone: `python _pygmt_render.py ...`
    from _style import (
        ANNOT_BOX, ANNOT_FONT, ANNOT_OFFSET, ANNOT_VAL_FONT,
        ANNOT_VAL_OFFSET, AREA_THRESH, BORDER_PEN, CBAR_POS, COAST_KW,
        NODATA, POLY_PEN)


def annotate_centroids(fig, gdf, label_col, val_col=None, fmt="{}",
                       font=ANNOT_FONT, val_font=ANNOT_VAL_FONT):
    """Name above the polygon centroid, value below it.

    The one annotation loop for both map families — the two drifted copies
    disagreed on the empty-centroid guard (a geometry reduced to nothing
    by simplify() crashes fig.text) and hand-mirrored the value offset.
    A name with no drawable value sits centred, un-offset.
    """
    import pandas as pd

    for _, row in gdf.iterrows():
        c = row["geometry"].centroid
        if c.is_empty:
            continue
        lbl = str(row[label_col])
        val = row[val_col] if val_col else None
        if val is not None and pd.notna(val):
            txt = val if isinstance(val, str) else fmt.format(val)
            if str(txt).lower() not in ("", "nan"):
                fig.text(x=c.x, y=c.y, text=lbl, font=font,
                         offset=ANNOT_OFFSET, **ANNOT_BOX)
                fig.text(x=c.x, y=c.y, text=str(txt), font=val_font,
                         offset=ANNOT_VAL_OFFSET, **ANNOT_BOX)
                continue
        fig.text(x=c.x, y=c.y, text=lbl, font=font, **ANNOT_BOX)


def render(geojson_path, params):
    """Render the choropleth described by ``geojson_path`` + ``params`` dict.

    pygmt is imported HERE, not at module scope, so importing this module
    needs no GMT C library — which is what the header has always claimed
    and what lets the style constants and :func:`annotate_centroids` be
    shared with GMT-free callers (and tested off-cluster).
    """
    import pygmt

    gdf = gpd.read_file(geojson_path)
    p = params
    fig = pygmt.Figure()
    # No embedded quotes: pygmt passes frame/label strings through the API,
    # so shell-style "..." quoting is unnecessary and shows up literally in
    # the rendered title/labels.
    title = p.get("title") or ""
    frame = ["af", f"+t{title}"] if title else ["af"]
    fig.basemap(region=p["region"], projection=p.get("projection", "M15c"), frame=frame)
    fig.coast(**COAST_KW)

    pen = POLY_PEN if p.get("do_borders", True) else None
    with tempfile.TemporaryDirectory() as td:
        # one plot call per distinct fill color (fewer GMT invocations)
        for i, (color, grp) in enumerate(gdf.groupby("_fill")):
            fp = os.path.join(td, f"g{i}.gmt")
            grp[["geometry"]].to_file(fp, driver="OGR_GMT")
            fig.plot(data=fp, fill=color, pen=pen)

        # admin_1 (state/province) boundaries, drawn AFTER the choropleth so
        # they sit ON TOP of it — fig.coast above runs before the polygons, so
        # borders requested there would be painted over. GMT border level 2 is
        # state/province. Slim, but heavier than the county stroke (0.4p) so it
        # reads above the county mesh instead of vanishing into it.
        if p.get("admin1_borders"):
            fig.coast(borders=BORDER_PEN, area_thresh=5000)

        cb = p.get("colorbar", {})
        label = p.get("label") or ""
        if cb.get("type") == "qualitative" and cb.get("colors"):
            labels = [str(x).replace(",", " ") for x in cb.get("cat_labels", [])]
            cols = cb["colors"][:len(labels)]
            # N discrete categories -> N CPT nodes (0..N-1). Using [0, N, 1]
            # would make N+1 nodes for N colors and misalign swatches/labels.
            pygmt.makecpt(cmap=",".join(cols), series=[0, len(labels) - 1, 1],
                          color_model="+c" + ",".join(labels))
            fig.colorbar(position=CBAR_POS,
                         frame=(f"+L{label}" if label else "+Lclass"))
        elif cb.get("type") == "continuous" and cb.get("colors"):
            pygmt.makecpt(cmap=",".join(cb["colors"]),
                          series=[float(cb["vmin"]), float(cb["vmax"])])
            fig.colorbar(position=CBAR_POS,
                         frame=(f"x+l{label}" if label else "af"))

        if p.get("annotate") and "_label" in gdf.columns:
            annotate_centroids(
                fig, gdf, "_label",
                val_col="_label_val" if "_label_val" in gdf.columns else None,
                font=p.get("annot_font", ANNOT_FONT),
                val_font=p.get("annot_val_font", ANNOT_VAL_FONT))

        os.makedirs(os.path.dirname(p["out_path"]) or ".", exist_ok=True)
        fig.savefig(p["out_path"], dpi=p.get("dpi", 350))


if __name__ == "__main__":
    _geojson, _json = sys.argv[1], sys.argv[2]
    with open(_json) as fh:
        _params = json.load(fh)
    render(_geojson, _params)
    print(f"OK {_params.get('out_path')}")
