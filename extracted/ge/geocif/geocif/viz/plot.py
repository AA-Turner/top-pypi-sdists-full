import logging
import os

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


def plot_df_shpfile(
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
    annotation_text=None,
    show_bg=True,
    loc_legend="lower center",
    do_borders=True,
    series="sequential",
    alpha_feature=1.0,
    use_key=False,
    annotate_regions=False,
    annotate_region_column="ADM1_NAME",
    include_first_tick=True,
    include_last_tick=True,
):
    """

    Args:
        attribute_df:
        df:
        dict_lup:
        merge_col:
        name_country:
        name_col:
        dir_out:
        fname:
        title:
        label:
        vmin:
        vmax:
        cmap:
        annotation_text:
        show_bg:
        loc_legend:
        do_borders:
        series:
        alpha_feature:
        use_key:
        annotate_regions:
        annotate_region_column:
        include_first_tick:
        include_last_tick:

    Returns:

    """
    os.makedirs(dir_out, exist_ok=True)

    proj = ccrs.PlateCarree()
    fig, ax = plt.subplots(subplot_kw={"projection": proj})

    # First subplot contains the map
    # ax.set_global()
    # Do not annotate regions if plotting a world map
    if name_country == "world":
        annotate_regions = False

    # Show background image of oceans (or not)
    if show_bg:
        ax.stock_img()
        from PIL import Image

        Image.MAX_IMAGE_PIXELS = 1000000000000
        # C:\Users\ritvik\anaconda3\envs\UMD\Lib\site-packages\cartopy\data\raster\natural_earth
        ax.background_img(name="ne_shaded", resolution="vhigh")

    # Annotate
    if annotation_text:
        t = ax.text(
            0.97,
            0.9,
            annotation_text,
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
        )
        t.set_bbox(dict(color="white", alpha=0.25, edgecolor="white"))

    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    if not cmap:
        import palettable as pal

        if series == "diverging":
            # prev colormap: palettable.colorbrewer.diverging.RdYlGn_9.mpl_colormap
            cmap = pal.colorbrewer.diverging.Spectral_11  # plt.get_cmap('viridis')
        elif series == "sequential":
            cmap = pal.colorbrewer.qualitative.Set3_7
        elif series == "qualitative":
            if int(vmax) <= 3:
                cmap = pal.colorbrewer.qualitative.Set3_7  # Green, Blue, Red
            else:
                cmap = pal.colorbrewer.qualitative.Set3_7

    if name_country != "world":
        try:
            if "ADMIN0" in attribute_df.columns:
                attribute_df = attribute_df[
                    attribute_df["ADMIN0"]
                    .str.lower()
                    .isin(el.lower() for el in name_country)
                ]
            elif "ADM0_NAME" in attribute_df.columns:
                attribute_df = attribute_df[
                    attribute_df["ADM0_NAME"]
                    .str.lower()
                    .isin(el.lower() for el in name_country)
                ]
        except:
            breakpoint()
        ax.spines["geo"].set_edgecolor("white")

    df_comb = df.merge(attribute_df, on=merge_col, suffixes=("", "_y"))
    # drop rows in df_comb where name_col is NaN
    df_comb = df_comb.dropna(subset=[name_col])

    for i, region in df_comb.iterrows():
        key = None
        # Ignore predicted yields for 'region'. Only plot actual adm1's
        # TODO: This is project specific thing, should not be here
        if merge_col in df_comb and df_comb[merge_col][i] == "region":
            continue

        if series == "qualitative":
            for key, val_cc in dict_lup.items():  # Get qualitative class
                if use_key:
                    if key == df_comb[name_col][i]:
                        break
                else:
                    if val_cc == df_comb[name_col][i]:
                        break
        else:
            key = df_comb[name_col][i]  # Get numeric value

        if key:
            if series == "qualitative":
                if isinstance(cmap, list):
                    fc = cmap[(key - 1) % len(cmap)]
                else:
                    fc = cmap.colors[(key - 1) % len(cmap.colors)]
            else:
                fc = cmap.mpl_colormap(norm(key))

            if df_comb["geometry"][i].geom_type == "MultiPolygon":
                geom = df_comb["geometry"][i]
            elif df_comb["geometry"][i].geom_type == "Polygon":
                geom = [df_comb["geometry"][i]]

            # geom = gp.GeoSeries(region.geometry).to_json()
            # clipped = xds.rio.clip(geom,  attribute_df.crs.name, drop=False)
            region_feature = ShapelyFeature(
                geom,
                ccrs.PlateCarree(),
                facecolor=fc,
                edgecolor="black",
                linestyle=":",
                linewidth=0.2,
                alpha=alpha_feature,
            )

            lw = 0.2 if do_borders else 0.0
            ax.add_feature(region_feature, linewidth=lw)
            # https://gis.stackexchange.com/questions/402314/plot-shapely-polygon-on-top-of-rasterio
            # xs, ys = geom[0].exterior.xy
            # ax.fill(xs, ys, alpha=0.5, fc=fc, ec='none')

            # tif_path = r'D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\cropland_v9.tif'
            # import rasterio as rio

            # with rio.open(tif_path, "r") as src:
            #     band_num = 1
            #     src_image = src.read(band_num, out_dtype=rio.float64)
            #
            #     # out_image, out_transform = rio.mask.mask(src, geom, crop=False, filled=False, indexes=band_num)
            #     # # pdb.set_trace()
            #     # src_image[out_image.mask] = key
            #     ## https://stackoverflow.com/questions/57031480/plotting-a-rasterio-raster-on-a-cartopy-geoaxes
            #     ax.imshow(src_image, transform=ccrs.Mercator())##, transform=ccrs.PlateCarree())

            # Annotate each region
            if annotate_regions:
                xy = (region["geometry"].centroid.x, region["geometry"].centroid.y)
                plt.annotate(
                    text=region[
                        annotate_region_column
                    ].title(),  # The annotation text, capitalized
                    xy=xy,  # Position tuple (x, y)
                    ha="center",  # Horizontal alignment (alias for horizontalalignment)
                    va="center",  # Vertical alignment (alias for verticalalignment)
                    fontsize=3,  # Text font size
                    bbox=dict(
                        boxstyle="round,pad=0.3", fc="white", alpha=0.5, ec="b", lw=0
                    )
                    # Optional: text box styling
                )

    ################################################
    # Plot scalebar
    ################################################
    if name_country != "world":
        from matplotlib_scalebar.scalebar import ScaleBar
        from shapely.geometry.point import Point
        import geopandas as gp

        points = gp.GeoSeries(
            [Point(-73.5, 40.5), Point(-74.5, 40.5)], crs=4326
        )  # Geographic WGS 84 - degrees
        points = points.to_crs(32619)  # Projected WGS 84 - meters
        distance_meters = points[0].distance(points[1])
        ax.add_artist(
            ScaleBar(
                distance_meters,
                box_alpha=0.75,
                frameon=False,
                location="lower right",
                font_properties={"family": "serif", "size": "xx-small"},
            )
        )

    # Add title to map plot
    if title:
        plt.title(title, fontsize=4, fontweight="semibold")

    if series == "qualitative":
        # cbar = custom_colorbar(cmap, len(dict_lup) + 1, labels=dict_lup.values(), shrink=0.75, orientation='horizontal')
        # cbar.outline.set_visible(False)
        # Nicer ArcGIS style legend
        if isinstance(cmap, list):
            legend_artists = [
                Line([0], [0], color=color, linewidth=2, alpha=alpha_feature)
                for color in cmap
            ]
        else:
            legend_artists = [
                Line([0], [0], color=color, linewidth=2, alpha=alpha_feature)
                for color in cmap.colors
            ]
        legend_texts = list(dict_lup.values())

        legend = plt.legend(
            legend_artists,
            legend_texts,
            # bbox_to_anchor=(1.0, -0.01),
            frameon=False,
            fancybox=False,
            loc=loc_legend,
            title=label,
            title_fontsize="xx-small",
            ncol=3 if len(legend_texts) > 9 else 2 if len(legend_texts) > 6 else 1,
            prop={"size": 5},
        )
        # for label in legend.get_texts():
        #     label.set_fontsize('xx-small')
        plt.setp(legend.get_title(), fontsize="xx-small", fontweight="semibold")
        if show_bg:
            legend.legendPatch.set_facecolor("wheat")
    else:
        if not np.isnan(vmin) and not np.isnan(vmax):
            from matplotlib.colors import BoundaryNorm
            from matplotlib.ticker import FormatStrFormatter
            from mpl_toolkits.axes_grid1.inset_locator import inset_axes

            # Get 5 values equidistant from vmin to vmax (for 4 intervals, we need 5 boundaries)
            number_of_intervals = 6
            ticks = np.linspace(vmin, vmax, number_of_intervals + 1)

            # Adjust format based on the step size
            step_size = (vmax - vmin) / number_of_intervals
            if step_size > 10:
                format = "%d"
                ticks = [int(tick) for tick in ticks]
            elif step_size > 2 and step_size <= 10:
                format = "%.1f"
                ticks = [round(tick, 1) for tick in ticks]
            else:
                format = "%.2f"
                ticks = [round(tick, 2) for tick in ticks]

            norm = BoundaryNorm(ticks, ncolors=cmap.mpl_colormap.N, clip=True)
            cbaxes = inset_axes(
                ax, width="75%", height="3%", loc=loc_legend, borderpad=0.25
            )
            sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap.mpl_colormap)
            # sm._A = []
            cb = plt.colorbar(
                mappable=sm,
                cax=cbaxes,
                ticks=ticks,
                ticklocation="top",
                orientation="horizontal",
                # drawedges=True,
                format=FormatStrFormatter(format),
            )

            cb.solids.set(edgecolor="white", linewidth=3)
            cb.outline.set_visible(False)
            # remove ticks
            cb.ax.tick_params(width=0, pad=0.1)
            # cb.ax.tick_params(width=1, length=10, color='k')
            for idx, bound in enumerate(ticks):
                # ignore first and last ticks
                if idx == 0 or idx == len(ticks) - 1:
                    continue
                cb.ax.axvline(bound, c="k", linewidth=0.75, ymin=0.3, ymax=2, alpha=0.6)
            # plt.setp(cb.ax.xaxis.get_ticklines(), alpha=0.6)
            # Do not show first and last tick label
            ticks[0] = ""
            # ticks[-1] = ""
            cb.ax.set_title(
                label, fontsize=8, fontweight="semibold", fontfamily="sans-serif"
            )
            cb.ax.set_xticklabels(ticks, fontsize=5, fontfamily="sans-serif")

            # Use BoundaryNorm to create discrete levels
            # sm = plt.cm.ScalarMappable(cmap=cmap.mpl_colormap, norm=norm)
            # sm._A = []  # This is a hack to make sure the ScalarMappable is aware of the colormap

            # Adjust format based on the step size
            # step_size = (vmax - vmin) / number_of_intervals
            # if step_size > 10:
            #     format = "%d"
            # elif step_size > 2 and step_size <= 10:
            #     format = "%.1f"
            # else:
            #     format = "%.2f"
            #
            # cbaxes = inset_axes(ax, width="50%", height="2%", loc=loc_legend, borderpad=0.25)
            # try:
            #
            #     cbar = plt.colorbar(sm, cax=cbaxes, orientation='horizontal', format=FormatStrFormatter(format))
            # except:
            #     breakpoint()
            # cbar.ax.set_title(label, fontsize=8, fontweight='semibold')
            #
            # # Update the ticks to the ones defined for the discrete intervals
            # cbar.set_ticks(ticks)
            #
            # cbar.ax.xaxis.set_ticks_position('none')  # Hide the tick marks (optional)
            # cbar.outline.set_visible(False)  # Hide the border of the colorbar
            # cbar.ax.tick_params(labelsize=6, pad=1)  # Adjust tick label font size and padding
            #
            # # Optionally rotate the tick labels if needed
            # cbar.ax.set_xticklabels([format % tick for tick in ticks], rotation=30, fontsize=6)

    # Set extent to match country or world
    if name_country:
        if name_country != "world":
            from cartopy.io import shapereader

            shpfilename = shapereader.natural_earth(
                "50m", "cultural", "admin_0_countries"
            )

            df_country = gpd.read_file(shpfilename, engine="pyogrio")
            # Hack
            # Rename Russia to Russian Federation, in the ADMIN column
            df_country.loc[
                df_country["ADMIN"].str.lower() == "russia", "ADMIN"
            ] = "Russian Federation"
            # read the country borders
            _name_country = []
            for cntr in name_country:
                cntr = cntr.replace("_", " ").lower()
                try:
                    poly = df_country.loc[df_country["ADMIN"].str.lower() == cntr][
                        "geometry"
                    ].values[0]
                except:
                    breakpoint()
                ax.add_geometries(
                    poly, crs=ccrs.PlateCarree(), facecolor="none", edgecolor="black"
                )
                _name_country.append(cntr.replace(" ", "_").lower())

            extent = rgeo.get_country_lat_lon_extent(
                _name_country, buffer=1.0
            )  # left, right, bottom, top

            # Hack: Add space to the top for adding title
            extent[3] = extent[3] + 2
            # Add some space to the bottom for adding legend and colorbar
            extent[2] = extent[2] - 3

            ax.set_extent(extent)
        elif name_country == "world":
            ax.add_feature(
                cartopy.feature.LAND.with_scale("50m"), color="white"
            )  # colors the land area white
            # ax.add_feature(cartopy.feature.OCEAN.with_scale('10m'))  # ocean with color blue
            ax.add_feature(
                cartopy.feature.BORDERS.with_scale("50m"),
                linewidth=0.35,
                edgecolor="black",
            )  # state borders
            ax.add_feature(
                cartopy.feature.COASTLINE.with_scale("110m"),
                linewidth=0.35,
                edgecolor="black",
            )  # only coastline, not land-land borders
            ax.set_extent([-179, 180, -60, 85])

    # for ax in fig.get_axes():
    #     ax.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
    #     ax.axis("off")

    # cbar.ax.tick_params(labelsize=8)
    # if series == "sequential":
    #     cbar.ax.tick_params(size=2, width=0.5, which="both")
    #     cbar.outline.set_visible(False)
    # plt.tight_layout()
    try:
        plt.savefig(dir_out / fname, dpi=350, bbox_inches="tight")
        plt.close(fig)
    except (OSError, ValueError) as e:
        logger.warning("Failed to save figure %s: %s", fname, e)
        return
