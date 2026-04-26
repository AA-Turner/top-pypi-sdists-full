import logging
import os
from pathlib import Path

import cartopy
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import pygeoutil.rgeo as rgeo
from cartopy.feature import ShapelyFeature
from matplotlib.lines import Line2D as Line

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

        if key:
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
                xy = (region["geometry"].centroid.x, region["geometry"].centroid.y)
                plt.annotate(
                    text=region[annotate_region_column].title(),
                    xy=xy,
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


def _set_extent(ax, name_country):
    """Set map extent and add country borders."""
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

        extent = rgeo.get_country_lat_lon_extent(_name_country, buffer=1.0)

        # Use contiguous U.S. extent (exclude Alaska/Hawaii)
        if any(c in ("united_states_of_america", "united_states") for c in _name_country):
            extent = [-130, -60, 22, 52]

        # Scale padding proportionally to country height (minimal — buffer=1.0 already adds 1°)
        lat_range = extent[3] - extent[2]
        extent[3] = extent[3] + lat_range * 0.05  # ~5% for title
        extent[2] = extent[2] - lat_range * 0.08  # ~8% for legend
        ax.set_extent(extent)
    else:
        ax.add_feature(cartopy.feature.LAND.with_scale("50m"), color="white")
        ax.add_feature(
            cartopy.feature.BORDERS.with_scale("50m"), linewidth=0.35, edgecolor="black"
        )
        ax.add_feature(
            cartopy.feature.COASTLINE.with_scale("110m"), linewidth=0.35, edgecolor="black"
        )
        ax.set_extent([-179, 180, -60, 85])


def _save(fig, dir_out, fname):
    """Save figure and close."""
    try:
        plt.savefig(Path(dir_out) / fname, dpi=350, bbox_inches="tight")
        plt.close(fig)
    except (OSError, ValueError) as e:
        logger.warning(f"Failed to save figure {fname}: {e}")


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

    # When ax is provided, draw into it (caller owns fig/save).
    # When ax is None, create our own fig and save to disk.
    external_ax = ax is not None
    if not external_ax:
        os.makedirs(dir_out, exist_ok=True)
        proj = ccrs.PlateCarree()
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
