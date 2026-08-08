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
import pygmt


def render(geojson_path, params):
    """Render the choropleth described by ``geojson_path`` + ``params`` dict."""
    gdf = gpd.read_file(geojson_path)
    p = params
    fig = pygmt.Figure()
    # No embedded quotes: pygmt passes frame/label strings through the API,
    # so shell-style "..." quoting is unnecessary and shows up literally in
    # the rendered title/labels.
    title = p.get("title") or ""
    frame = ["af", f"+t{title}"] if title else ["af"]
    fig.basemap(region=p["region"], projection=p.get("projection", "M15c"), frame=frame)
    fig.coast(shorelines="0.3p,gray60", borders="1/0.2p,gray70", area_thresh=5000)

    pen = "0.4p,black" if p.get("do_borders", True) else None
    with tempfile.TemporaryDirectory() as td:
        # one plot call per distinct fill color (fewer GMT invocations)
        for i, (color, grp) in enumerate(gdf.groupby("_fill")):
            fp = os.path.join(td, f"g{i}.gmt")
            grp[["geometry"]].to_file(fp, driver="OGR_GMT")
            fig.plot(data=fp, fill=color, pen=pen)

        cb = p.get("colorbar", {})
        label = p.get("label") or ""
        if cb.get("type") == "qualitative" and cb.get("colors"):
            labels = [str(x).replace(",", " ") for x in cb.get("cat_labels", [])]
            cols = cb["colors"][:len(labels)]
            # N discrete categories -> N CPT nodes (0..N-1). Using [0, N, 1]
            # would make N+1 nodes for N colors and misalign swatches/labels.
            pygmt.makecpt(cmap=",".join(cols), series=[0, len(labels) - 1, 1],
                          color_model="+c" + ",".join(labels))
            fig.colorbar(position="JBC+w12c/0.35c+h",
                         frame=(f"+L{label}" if label else "+Lclass"))
        elif cb.get("type") == "continuous" and cb.get("colors"):
            pygmt.makecpt(cmap=",".join(cb["colors"]),
                          series=[float(cb["vmin"]), float(cb["vmax"])])
            fig.colorbar(position="JBC+w12c/0.35c+h",
                         frame=(f"x+l{label}" if label else "af"))

        if p.get("annotate") and "_label" in gdf.columns:
            font = p.get("annot_font", "8p,Helvetica,black")
            val_font = p.get("annot_val_font", "7p,Helvetica-Oblique,black")
            has_val = "_label_val" in gdf.columns
            for _, row in gdf.iterrows():
                c = row["geometry"].centroid
                if c.is_empty:
                    continue
                lbl = str(row["_label"])
                val = str(row["_label_val"]) if has_val else ""
                if val and val.lower() != "nan":
                    # Region name on top, metric value below the centroid
                    # (GMT text has no reliable newline, so two offset calls).
                    fig.text(x=c.x, y=c.y, text=lbl, font=font,
                             offset="0c/0.16c", fill="white@30", pen="0.2p,gray40")
                    fig.text(x=c.x, y=c.y, text=val, font=val_font,
                             offset="0c/-0.16c", fill="white@30", pen="0.2p,gray40")
                else:
                    fig.text(x=c.x, y=c.y, text=lbl,
                             font=font, fill="white@30", pen="0.2p,gray40")

        os.makedirs(os.path.dirname(p["out_path"]) or ".", exist_ok=True)
        fig.savefig(p["out_path"], dpi=p.get("dpi", 350))


if __name__ == "__main__":
    _geojson, _json = sys.argv[1], sys.argv[2]
    with open(_json) as fh:
        _params = json.load(fh)
    render(_geojson, _params)
    print(f"OK {_params.get('out_path')}")
