import logging
import os
from pathlib import Path

import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D as Line

# NOTE: cartopy / pygeoutil are imported lazily inside the matplotlib-path
# helpers (_draw_regions, _projection_for, _set_extent). The default PyGMT
# backend does not need them, so importing this module in a pygmt-only env
# (no cartopy) still works.

logger = logging.getLogger(__name__)


# =============================================================================
# Private helpers
# =============================================================================

def _resolve_cmap(cmap, series, vmax):
    """Pick a default colormap when none is provided."""
    if cmap:
        return cmap
    import palettable as pal
    if series == "diverging":
        return pal.colorbrewer.diverging.Spectral_11
    elif series == "sequential":
        return pal.colorbrewer.qualitative.Set3_7
    elif series == "qualitative":
        return pal.colorbrewer.qualitative.Set3_7
    return cmap


def _filter_countries(attribute_df, name_country, ax):
    """Filter shapefile to selected countries."""
    if name_country == "world":
        return attribute_df

    admin_col = None
    if "ADMIN0" in attribute_df.columns:
        admin_col = "ADMIN0"
    elif "ADM0_NAME" in attribute_df.columns:
        admin_col = "ADM0_NAME"

    if admin_col:
        attribute_df = attribute_df[
            attribute_df[admin_col]
            .str.lower()
            .isin(el.lower() for el in name_country)
        ]
    ax.spines["geo"].set_edgecolor("white")
    return attribute_df


def _compute_norm(df, attribute_df, merge_col, name_col, series, vmin, vmax,
                  classify_by, continuous_colorbar, cmap, fixed_range=False):
    """Merge data with shapefile, compute classification breaks and norm."""
    df_comb = gpd.GeoDataFrame(df.merge(attribute_df, on=merge_col, suffixes=("", "_y")), geometry="geometry")
    df_comb = df_comb.dropna(subset=[name_col])

    if fixed_range:
        breaks = list(np.linspace(vmin, vmax, 11))
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
        return df_comb, norm, breaks

    breaks = None
    if series != "qualitative":
        from matplotlib.colors import BoundaryNorm
        import mapclassify
        values = df_comb[name_col].dropna().values
        n_unique = len(np.unique(values))
        classifier = mapclassify.Quantiles if classify_by == "region" else mapclassify.FisherJenks
        if n_unique >= 10:
            mc = classifier(values, k=10)
            breaks = [round(values.min(), 2)] + [round(b, 2) for b in mc.bins.tolist()]
        elif n_unique >= 2:
            mc = classifier(values, k=n_unique)
            breaks = [round(values.min(), 2)] + [round(b, 2) for b in mc.bins.tolist()]
        else:
            breaks = list(np.linspace(vmin, vmax, 7))
        if continuous_colorbar:
            norm = matplotlib.colors.Normalize(vmin=breaks[0], vmax=breaks[-1])
        else:
            norm = BoundaryNorm(breaks, ncolors=cmap.mpl_colormap.N, clip=True)
    else:
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)

    return df_comb, norm, breaks


def _draw_regions(ax, df_comb, merge_col, name_col, series, dict_lup, use_key,
                  cmap, norm, alpha_feature, do_borders, annotate_regions,
                  annotate_region_column):
    """Color each region polygon and optionally annotate."""
    import cartopy.crs as ccrs
    from cartopy.feature import ShapelyFeature
    for i, region in df_comb.iterrows():
        if merge_col in df_comb and df_comb[merge_col][i] == "region":
            continue

        key = None
        if series == "qualitative":
            for key, val_cc in dict_lup.items():
                if use_key:
                    if key == df_comb[name_col][i]:
                        break
                else:
                    if val_cc == df_comb[name_col][i]:
                        break
        else:
            key = df_comb[name_col][i]

        # NaN in the value column means "region excluded from analysis"
        # (e.g. yield_outlook's minimal-crop-area filter). Draw as
        # lightgray silhouette with the normal black border so the
        # country outline stays complete.
        if key is not None and series != "qualitative" and pd.isna(key):
            key = "__excluded__"
            fc = (0.85, 0.85, 0.85, 1.0)
        elif key:
            if series == "qualitative":
                if isinstance(cmap, list):
                    fc = _normalize_color(cmap[(key - 1) % len(cmap)])
                else:
                    fc = _normalize_color(cmap.colors[(key - 1) % len(cmap.colors)])
            else:
                fc = cmap.mpl_colormap(norm(key))

            from shapely.ops import unary_union
            raw_geom = df_comb["geometry"][i]
            # Merge sub-polygons to remove internal edges
            merged = unary_union(raw_geom)
            geom = [merged] if merged.geom_type == "Polygon" else merged

            region_feature = ShapelyFeature(
                geom,
                ccrs.PlateCarree(),
                facecolor=fc,
                edgecolor="black" if do_borders else "none",
                linestyle="-",
                linewidth=0.5 if do_borders else 0.0,
                alpha=alpha_feature,
            )

            lw = 0.5 if do_borders else 0.0
            ax.add_feature(region_feature, linewidth=lw)

            if annotate_regions:
                lon, lat = region["geometry"].centroid.x, region["geometry"].centroid.y
                # Transform lat/lon centroid into the axes projection so labels
                # land correctly under any projection (identity for PlateCarree,
                # reprojected for Albers/USA).
                try:
                    xt, yt = ax.projection.transform_point(lon, lat, ccrs.PlateCarree())
                except Exception:
                    xt, yt = lon, lat
                if np.isfinite(xt) and np.isfinite(yt):
                    plt.annotate(
                        text=region[annotate_region_column].title(),
                        xy=(xt, yt),
                        ha="center",
                        va="center",
                        fontsize=3,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.5, ec="b", lw=0),
                    )



def _normalize_color(raw):
    """Normalize a color tuple from 0-255 ints to 0-1 floats if needed."""
    if isinstance(raw, (list, tuple)) and any(isinstance(c, int) and c > 1 for c in raw):
        return tuple(c / 255.0 for c in raw)
    return raw


def _add_qualitative_legend(ax, cmap, dict_lup, alpha_feature, loc_legend, label):
    """Add a qualitative (categorical) legend."""
    if isinstance(cmap, list):
        colors = [_normalize_color(c) for c in cmap]
    else:
        colors = [_normalize_color(c) for c in cmap.colors]
    legend_artists = [
        Line([0], [0], color=c, linewidth=2, alpha=alpha_feature)
        for c in colors
    ]
    legend_texts = list(dict_lup.values())

    legend = plt.legend(
        legend_artists,
        legend_texts,
        frameon=False,
        fancybox=False,
        loc=loc_legend,
        title=label,
        title_fontsize="xx-small",
        ncol=3 if len(legend_texts) > 9 else 2 if len(legend_texts) > 6 else 1,
        prop={"size": 5},
    )
    plt.setp(legend.get_title(), fontsize="xx-small", fontweight="semibold")


def _add_colorbar(ax, cmap, norm, breaks, loc_legend, label,
                  legend_dividers, continuous_colorbar, series="sequential",
                  extend="neither"):
    """Add a continuous or discrete colorbar."""
    from matplotlib.ticker import FormatStrFormatter
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    if continuous_colorbar:
        ticks = list(np.linspace(breaks[0], breaks[-1], len(breaks)))
    else:
        ticks = list(breaks)

    # Ensure 0.5 is included for sequential colorbars
    if series == "sequential" and ticks[0] <= 0.5 <= ticks[-1]:
        if not any(abs(t - 0.5) < 1e-9 for t in ticks):
            ticks.append(0.5)
            ticks.sort()

    # Adjust format based on the smallest step size
    step_size = min(b - a for a, b in zip(ticks, ticks[1:]))
    if step_size > 10:
        fmt = "%d"
        ticks = [int(tick) for tick in ticks]
    elif step_size > 2:
        fmt = "%.1f"
        ticks = [round(tick, 1) for tick in ticks]
    else:
        fmt = "%.2f"
        ticks = [round(tick, 2) for tick in ticks]

    # Limit ticks to avoid overlapping labels
    max_ticks = 6
    if len(ticks) > max_ticks:
        indices = np.linspace(0, len(ticks) - 1, max_ticks, dtype=int)
        ticks = [ticks[i] for i in indices]

    cbaxes = inset_axes(
        ax, width="75%", height="3%", loc=loc_legend, borderpad=0.5
    )
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap.mpl_colormap)
    cb = plt.colorbar(
        mappable=sm,
        cax=cbaxes,
        ticks=ticks,
        ticklocation="bottom",
        orientation="horizontal",
        format=FormatStrFormatter(fmt),
        extend=extend,
    )

    if legend_dividers:
        cb.solids.set(edgecolor="white", linewidth=3)
    cb.outline.set_visible(False)

    if legend_dividers:
        cb.ax.tick_params(width=0, pad=0.1)
        for idx, bound in enumerate(ticks):
            if idx == 0 or idx == len(ticks) - 1:
                continue
            cb.ax.axvline(bound, c="k", linewidth=0.75, ymin=0.3, ymax=2, alpha=0.6)
    else:
        cb.ax.tick_params(width=0.5, length=3, color='k', pad=2)

    # Hide first tick label and its tick mark
    ticks[0] = ""
    cb.ax.set_xlabel(label, fontsize=6, fontweight="semibold", fontfamily="sans-serif", labelpad=2)
    cb.ax.set_xticklabels(ticks, fontsize=5, fontfamily="sans-serif", rotation=45, ha="right")
    major_ticks = cb.ax.xaxis.get_major_ticks()
    if major_ticks:
        major_ticks[0].tick1line.set_visible(False)
        major_ticks[0].tick2line.set_visible(False)


def _projection_for(name_country):
    """Axes map projection for ``name_country``.

    The contiguous U.S. is badly stretched under plate-carree, so USA maps use
    Albers Equal Area (standard CONUS parameters). Every other country keeps
    ``PlateCarree`` (unchanged). Data is always added with a PlateCarree
    ``transform`` (lat/lon), so cartopy reprojects correctly either way.
    """
    import cartopy.crs as ccrs
    names = name_country if isinstance(name_country, (list, tuple)) else [name_country]
    norm = {str(n).replace("_", " ").lower() for n in names if n}
    if norm & {"united states of america", "united states", "usa"}:
        return ccrs.AlbersEqualArea(
            central_longitude=-96.0, central_latitude=37.5,
            standard_parallels=(29.5, 45.5),
        )
    return ccrs.PlateCarree()


def _set_extent(ax, name_country):
    """Set map extent and add country borders."""
    import cartopy
    import cartopy.crs as ccrs
    import pygeoutil.rgeo as rgeo
    if not name_country:
        return

    if name_country != "world":
        from cartopy.io import shapereader

        shpfilename = shapereader.natural_earth("50m", "cultural", "admin_0_countries")
        df_country = gpd.read_file(shpfilename, engine="pyogrio")
        df_country.loc[
            df_country["ADMIN"].str.lower() == "russia", "ADMIN"
        ] = "Russian Federation"

        _name_country = []
        for cntr in name_country:
            cntr_lower = cntr.replace("_", " ").lower()
            matches = df_country.loc[df_country["ADMIN"].str.lower() == cntr_lower]
            if matches.empty:
                logger.error(f"Country not found in Natural Earth: {cntr}")
                continue
            poly = matches["geometry"].values[0]
            # Dissolve to single exterior boundary (avoids internal admin lines)
            from shapely.ops import unary_union
            poly = unary_union(poly)
            ax.add_geometries(
                [poly], crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black"
            )
            _name_country.append(cntr_lower.replace(" ", "_"))

        # Skip extent-setting when no countries matched Natural Earth.
        # Happens when name_country contains a sub-country zone (e.g. a
        # zone like Wolayita that lives inside Ethiopia) or a misspelled
        # country. Without this guard the empty-list path used to hit
        # pygeoutil's UnboundLocalError; with the pygeoutil fix in place
        # this would return the global bbox, which is also wrong here —
        # let cartopy auto-fit from the geometries already added via
        # ax.add_geometries above.
        if not _name_country:
            logger.warning(
                "  Skipping country-extent setting; no countries matched "
                "Natural Earth. Cartopy will auto-fit from the shapefile."
            )
            return

        try:
            extent = rgeo.get_country_lat_lon_extent(_name_country, buffer=1.0)
        except Exception as exc:  # noqa: BLE001
            # Defense-in-depth — any unexpected pygeoutil failure
            # shouldn't crash the whole plotting pass. Auto-fit instead.
            logger.warning(
                f"  get_country_lat_lon_extent failed ({type(exc).__name__}: "
                f"{exc}); falling back to cartopy auto-extent."
            )
            return

        # Use contiguous U.S. extent (exclude Alaska/Hawaii)
        if any(c in ("united_states_of_america", "united_states") for c in _name_country):
            extent = [-130, -60, 22, 52]

        # Scale padding proportionally to country height (minimal — buffer=1.0 already adds 1°)
        lat_range = extent[3] - extent[2]
        extent[3] = extent[3] + lat_range * 0.05  # ~5% for title
        extent[2] = extent[2] - lat_range * 0.08  # ~8% for legend
        # extent is lat/lon; pass crs so it's correct under any axes projection
        # (identity for PlateCarree, reprojected for Albers/USA).
        ax.set_extent(extent, crs=ccrs.PlateCarree())
    else:
        ax.add_feature(cartopy.feature.LAND.with_scale("50m"), color="white")
        ax.add_feature(
            cartopy.feature.BORDERS.with_scale("50m"), linewidth=0.35, edgecolor="black"
        )
        ax.add_feature(
            cartopy.feature.COASTLINE.with_scale("110m"), linewidth=0.35, edgecolor="black"
        )
        ax.set_extent([-179, 180, -60, 85], crs=ccrs.PlateCarree())


def _save(fig, dir_out, fname):
    """Save figure and close."""
    try:
        plt.savefig(Path(dir_out) / fname, dpi=350, bbox_inches="tight")
        plt.close(fig)
    except (OSError, ValueError) as e:
        logger.warning(f"Failed to save figure {fname}: {e}")


# =============================================================================
# PyGMT rendering backend (default). Same title / labels / categories / colors
# as the matplotlib path — only the rendering engine differs, for nicer
# cartography. Standalone only: when ``plot_map`` is given an ``ax`` (embedded
# multi-panel figure) or when pygmt/GMT is unavailable, it falls back to
# matplotlib automatically.
# =============================================================================

def _gmt_projection_for(name_country, width="15c"):
    """GMT projection string mirroring ``_projection_for`` (Albers for CONUS,
    Mercator otherwise)."""
    names = name_country if isinstance(name_country, (list, tuple)) else [name_country]
    norm = {str(n).replace("_", " ").lower() for n in names if n}
    if norm & {"united states of america", "united states", "usa"}:
        return f"B-96/37.5/29.5/45.5/{width}"  # Albers Equal Area (CONUS)
    return f"M{width}"  # Mercator


_GMT_OK = None


def _gmt_available():
    """True iff PyGMT can load the GMT C library in THIS process (cached).

    ``import pygmt`` succeeds without GMT (it loads libgmt lazily), so we
    actually open a session. False -> use the subprocess bridge to a
    pygmt-capable env.
    """
    global _GMT_OK
    if _GMT_OK is None:
        try:
            from pygmt.clib import Session
            with Session():
                pass
            _GMT_OK = True
        except Exception:  # noqa: BLE001
            _GMT_OK = False
    return _GMT_OK


def _plot_map_pygmt(
    attribute_df, df, dict_lup, merge_col, name_country, name_col,
    dir_out, fname, title, label, vmin, vmax, cmap, series,
    do_borders, annotate_regions, annotate_region_column,
    continuous_colorbar, classify_by, fixed_range, use_key,
):
    """Render the same choropleth as ``plot_map`` using PyGMT.

    Reuses ``_compute_norm`` and computes each region's fill with the SAME
    colormap logic as ``_draw_regions`` (exact color parity). Then renders via
    :func:`geocif.viz._pygmt_render.render` — in-process when GMT is usable
    here, otherwise via a subprocess bridge to a pygmt-capable conda env
    (``GEOCIF_PYGMT_CONDA_ENV``, default ``pygmt_env``). The heavy prep runs in
    the caller's env (no pygmt needed).
    """
    import json
    import tempfile
    import subprocess
    from matplotlib.colors import to_hex

    # --- country filter (ax-free port of _filter_countries) ---
    adf = attribute_df
    if name_country and name_country != "world":
        admin_col = ("ADMIN0" if "ADMIN0" in adf.columns
                     else ("ADM0_NAME" if "ADM0_NAME" in adf.columns else None))
        if admin_col:
            adf = adf[adf[admin_col].str.lower().isin(el.lower() for el in name_country)]

    # --- merge + classification (identical to the matplotlib path) ---
    df_comb, norm, breaks = _compute_norm(
        df, adf, merge_col, name_col, series, vmin, vmax,
        classify_by, continuous_colorbar, cmap, fixed_range,
    )
    gdf = gpd.GeoDataFrame(df_comb, geometry="geometry")
    if gdf.empty:
        logger.warning(f"pygmt map: no data after merge for {fname}; skipping.")
        return

    # --- per-region fill color, matching _draw_regions ---
    def _fill_for(val):
        if series == "qualitative":
            key = None
            for k, v in dict_lup.items():
                if (use_key and k == val) or (not use_key and v == val):
                    key = k
                    break
            if key is None:
                return None
            raw = (cmap[(key - 1) % len(cmap)] if isinstance(cmap, list)
                   else cmap.colors[(key - 1) % len(cmap.colors)])
            return to_hex(_normalize_color(raw))
        if pd.isna(val):
            return "#d9d9d9"  # region excluded from analysis -> lightgray
        return to_hex(cmap.mpl_colormap(norm(val)))

    gdf["_fill"] = gdf[name_col].map(_fill_for)
    gdf = gdf[gdf["_fill"].notna()].copy()
    if gdf.empty:
        return
    gdf["geometry"] = gdf.geometry.simplify(0.01)

    cols_keep = ["_fill", "geometry"]
    if annotate_regions and annotate_region_column in gdf.columns:
        gdf["_label"] = gdf[annotate_region_column].astype(str).str.title()
        cols_keep.insert(1, "_label")

    # --- extent + colorbar spec (same colors + label as the mpl path) ---
    minx, miny, maxx, maxy = gdf.total_bounds
    padx = max(0.5, (maxx - minx) * 0.05)
    pady = max(0.5, (maxy - miny) * 0.05)

    if series == "qualitative":
        allcols = cmap if isinstance(cmap, list) else list(cmap.colors)
        cat_labels = [str(x) for x in dict_lup.values()]
        cbar = {
            "type": "qualitative",
            "colors": [to_hex(_normalize_color(c)) for c in allcols][:len(cat_labels)],
            "cat_labels": cat_labels,
        }
    elif not (np.isnan(vmin) or np.isnan(vmax)) and breaks is not None:
        cbar = {
            "type": "continuous",
            "colors": [to_hex(cmap.mpl_colormap(x)) for x in np.linspace(0, 1, 11)],
            "vmin": float(breaks[0]), "vmax": float(breaks[-1]),
        }
    else:
        cbar = {"type": "none"}

    params = {
        "out_path": str(Path(dir_out) / fname),
        "region": [float(minx - padx), float(maxx + padx),
                   float(miny - pady), float(maxy + pady)],
        "projection": _gmt_projection_for(name_country),
        "title": title or "", "label": label or "",
        "do_borders": bool(do_borders),
        "annotate": bool(annotate_regions and "_label" in gdf.columns),
        "colorbar": cbar,
    }

    os.makedirs(dir_out, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="pygmt_map_")
    gj = os.path.join(tmpdir, "data.geojson")
    pj = os.path.join(tmpdir, "params.json")
    gdf[cols_keep].to_file(gj, driver="GeoJSON")
    with open(pj, "w") as fh:
        json.dump(params, fh)

    if _gmt_available():
        from . import _pygmt_render
        # render() takes the params DICT (the subprocess __main__ path loads
        # the JSON itself) — passing the path here was latent until an env
        # could actually load GMT in-process (pixi-managed gmt, 0.4.886+).
        _pygmt_render.render(gj, params)
    else:
        # Bridge: render in a pygmt-capable conda env.
        env = os.environ.get("GEOCIF_PYGMT_CONDA_ENV", "pygmt_env")
        helper = str(Path(__file__).with_name("_pygmt_render.py"))
        cmd = f'conda run -n {env} python "{helper}" "{gj}" "{pj}"'
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if proc.returncode != 0:
            logger.warning(
                "pygmt bridge failed (rc=%s) for %s; stderr: %s",
                proc.returncode, fname, (proc.stderr or "")[-600:],
            )
            raise RuntimeError(f"pygmt bridge failed for {fname}")


# =============================================================================
# Public API
# =============================================================================

def plot_map(
    attribute_df,
    df,
    dict_lup=None,
    merge_col="adm1_name",
    name_country=None,
    name_col="",
    dir_out="",
    fname="",
    title="",
    label="",
    vmin=0.0,
    vmax=180.0,
    cmap=None,
    loc_legend="lower center",
    do_borders=True,
    series="sequential",
    alpha_feature=1.0,
    use_key=False,
    annotate_regions=False,
    annotate_region_column="ADM1_NAME",
    legend_dividers=False,
    continuous_colorbar=True,
    classify_by="region",
    extend="neither",
    fixed_range=None,
    ax=None,
    backend="pygmt",
):
    """Plot a choropleth map of regions colored by a data variable.

    Args:
        attribute_df: GeoDataFrame with region geometries.
        df: DataFrame with data to plot (merged via merge_col).
        dict_lup: Lookup dict for qualitative series (key -> label).
        merge_col: Column name to merge df with attribute_df.
        name_country: List of country names to plot, or "world".
        name_col: Column in df to color regions by.
        dir_out: Output directory for saved figure.
        fname: Output filename.
        title: Map title.
        label: Colorbar/legend label.
        vmin: Minimum value for color scale.
        vmax: Maximum value for color scale.
        cmap: Palettable colormap (or list of colors for qualitative).
        loc_legend: Legend location string.
        do_borders: Draw region border lines.
        series: One of "sequential", "diverging", "qualitative".
        alpha_feature: Opacity of region fills.
        use_key: Match qualitative values by key (not value).
        annotate_regions: Label each region on the map.
        annotate_region_column: Column for region annotation text.
        legend_dividers: Show divider lines between colorbar segments.
        continuous_colorbar: Smooth gradient (True) or discrete bins (False).
        classify_by: "region" (quantiles) or "value" (Fisher-Jenks).
        extend: Colorbar extend arrows ("neither", "both", "min", "max").
        fixed_range: Force colorbar to use exact vmin/vmax range. Default True for diverging.
    """
    if fixed_range is None:
        fixed_range = (series == "diverging")

    # PyGMT backend (default) for STANDALONE maps. Falls back to matplotlib
    # when embedding into a caller-owned axes (pygmt can't render into a
    # matplotlib ax) or when pygmt/GMT is unavailable at runtime.
    if backend == "pygmt" and ax is None:
        try:
            _plot_map_pygmt(
                attribute_df, df, dict_lup, merge_col, name_country, name_col,
                dir_out, fname, title, label, vmin, vmax,
                _resolve_cmap(cmap, series, vmax), series, do_borders,
                annotate_regions, annotate_region_column, continuous_colorbar,
                classify_by, fixed_range, use_key,
            )
            return
        except Exception as e:  # noqa: BLE001
            logger.warning(
                "pygmt backend failed (%s: %s); using matplotlib for %s",
                type(e).__name__, e, fname,
            )

    # When ax is provided, draw into it (caller owns fig/save).
    # When ax is None, create our own fig and save to disk.
    external_ax = ax is not None
    if not external_ax:
        os.makedirs(dir_out, exist_ok=True)
        proj = _projection_for(name_country)
        fig, ax = plt.subplots(subplot_kw={"projection": proj})

    if name_country == "world":
        annotate_regions = False

    cmap = _resolve_cmap(cmap, series, vmax)
    attribute_df = _filter_countries(attribute_df, name_country, ax)
    df_comb, norm, breaks = _compute_norm(
        df, attribute_df, merge_col, name_col, series, vmin, vmax,
        classify_by, continuous_colorbar, cmap, fixed_range,
    )
    _draw_regions(
        ax, df_comb, merge_col, name_col, series, dict_lup, use_key,
        cmap, norm, alpha_feature, do_borders, annotate_regions,
        annotate_region_column,
    )

    if title:
        ax.set_title(title, fontsize=4, fontweight="semibold")

    if series == "qualitative":
        _add_qualitative_legend(ax, cmap, dict_lup, alpha_feature, loc_legend, label)
    else:
        if not np.isnan(vmin) and not np.isnan(vmax) and breaks is not None:
            _add_colorbar(
                ax, cmap, norm, breaks, loc_legend, label,
                legend_dividers, continuous_colorbar, series, extend,
            )

    _set_extent(ax, name_country)

    if not external_ax:
        _save(fig, dir_out, fname)

    return ax
