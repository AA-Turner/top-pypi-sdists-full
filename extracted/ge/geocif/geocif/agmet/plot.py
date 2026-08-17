import os
import math
import datetime
import matplotlib
import numpy as np
import pandas as pd
import bottleneck as bn
import arrow as ar
import matplotlib.pyplot as plt
import palettable as pal
from cycler import cycler
from matplotlib import rcParams

from skmisc.loess import loess as _loess

from geocif.backup import constants
from geocif.agmet import utils

# Logo display box in figure pixels. fig.figimage draws at NATIVE pixel size,
# so a high-resolution asset renders enormous: acres.png is 3089x973 and
# spanned the whole figure (swallowing the title) until it was scaled here,
# while harvest.png (221x235) and geoglam.png (466x143) always fit. Logos are
# scaled DOWN to this box preserving aspect ratio and are never upscaled. The
# 240px height is deliberate: harvest.png is 235px tall, so a tighter bound
# would silently shrink every existing non-USA figure. acres.png binds on
# width instead -> 500x157.
LOGO_MAX_PX = (500, 240)

# "Data Sources" caption block (figure fractions). The body is bottom-anchored
# here and grows upward; the bold header is placed just above its top line.
DATA_SOURCES_BODY_Y = 0.13
DATA_SOURCES_LINESPACING = 1.5


def data_sources_header_y(n_lines, fig_height_in, fontsize,
                          body_y=DATA_SOURCES_BODY_Y,
                          linespacing=DATA_SOURCES_LINESPACING, pad_lines=0.5):
    """Figure-fraction y for the 'Data Sources' header, given the body size.

    Keeps the header exactly ``pad_lines`` above the body's top line whatever
    the line count, so conditional source lines can never overlap it.
    """
    line_h = (fontsize * linespacing) / (float(fig_height_in) * 72.0)
    return body_y + (n_lines + pad_lines) * line_h


def load_scaled_logo(path, max_w=LOGO_MAX_PX[0], max_h=LOGO_MAX_PX[1]):
    """Read a logo image, downscaled to fit within (max_w, max_h) pixels."""
    from PIL import Image

    img = Image.open(str(path))
    w, h = img.size
    scale = min(max_w / w, max_h / h, 1.0)
    if scale < 1.0:
        # Pillow 10 moved the filters to Image.Resampling; keep both working.
        resample = getattr(Image, "Resampling", Image).LANCZOS
        img = img.resize(
            (max(1, round(w * scale)), max(1, round(h * scale))), resample
        )
    return np.asarray(img)


def _lowess(y, x, frac=0.2, it=3):
    """LOWESS smoothing via skmisc, fitted only on non-NaN values."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    valid = ~np.isnan(y)
    if not valid.any():
        return y
    result = np.full_like(y, np.nan)
    try:
        l = _loess(x[valid], y[valid], span=frac)
        l.control.iterations = it
        l.fit()
        result[valid] = l.outputs.fitted_values
    except ValueError:
        result[valid] = y[valid]  # fall back to unsmoothed
    return result


def set_matplotlib_params():
    """Set matplotlib defaults to nicer values."""
    rcParams["mathtext.default"] = "regular"
    rcParams["axes.labelsize"] = 12
    rcParams["xtick.labelsize"] = 12
    rcParams["ytick.labelsize"] = 12
    rcParams["legend.fontsize"] = 12
    rcParams["font.family"] = "sans-serif"
    rcParams["font.serif"] = ["Helvetica"]
    rcParams["legend.numpoints"] = 1


def get_colors(palette="colorbrewer", cmap=False, only_colors=False):
    """Get palettable colors, which are nicer."""
    if palette == "colorbrewer":
        bmap = pal.colorbrewer.diverging.PRGn_11.mpl_colors
        if cmap:
            bmap = pal.colorbrewer.diverging.PRGn_11.mpl_colormap
    elif palette == "tableau":
        bmap = pal.tableau.Tableau_20.mpl_colors
        if cmap:
            bmap = pal.tableau.Tableau_20.mpl_colormap
    elif palette == "cubehelix":
        bmap = pal.cubehelix.cubehelix2_16.mpl_colors
        if cmap:
            bmap = pal.cubehelix.cubehelix2_16.mpl_colormap
    elif palette == "qualitative":
        bmap = pal.tableau.GreenOrange_12.mpl_colors
        if cmap:
            bmap = pal.tableau.GreenOrange_12.mpl_colormap

    if cmap:
        return bmap

    if only_colors:
        color_cycle = cycler("color", bmap)
    else:
        color_cycle = (cycler(marker=["*", "o"]) * cycler("ls", ["-", "--"])) * cycler(
            "color", bmap
        )
    plt.rc("axes", prop_cycle=color_cycle)

    return bmap


class AgmetPlotter:
    """Object-oriented plotter for agmet time-series figures."""

    def __init__(
        self,
        df,
        names_cols,
        closest=None,
        dates_cal=None,
        frcast_yr=None,
        logos=None,
        window=5,
        dir_out="",
        sup_title="",
        fname="",
        production_pct=None,
        country=None,
        region=None,
        region_id=None,
        boundary_gdf=None,
        highlight_gdf=None,
        admin_level=None,
        show_logos=True,
        logo_max_px=LOGO_MAX_PX,
    ):
        self.df = df.copy()
        self.names_cols = names_cols
        self.closest = closest
        self.dates_cal = dates_cal
        self.frcast_yr = frcast_yr
        self.logos = logos
        self.window = window
        self.dir_out = dir_out
        self.sup_title = sup_title
        self.fname = fname
        self.production_pct = production_pct
        self.country = country
        self.region = region
        self.region_id = region_id
        self.boundary_gdf = boundary_gdf
        self.highlight_gdf = highlight_gdf
        self.admin_level = admin_level
        self.show_logos = show_logos
        self.logo_max_px = logo_max_px

        self.use_forecast = False
        self.color_list = get_colors("tableau", only_colors=True)

        # Determine precipitation source
        if "chirps" in self.df.columns.values:
            self.precip_var = "chirps"
        elif "daymet_prcp" in self.df.columns.values:
            self.precip_var = "daymet_prcp"
        else:
            self.precip_var = "cpc_precip"

        # Preprocess data
        if "nsidc_rootzone" in self.df:
            self.df["nsidc_rootzone"] = self.df["nsidc_rootzone"].clip(0, 1)
        if "esi_4wk" in self.df:
            self.df["esi_4wk"] = self.df["esi_4wk"] / 10.0 - 4.0
        if "chirts_era5_tmax" in self.df and "chirts_era5_tmin" in self.df:
            self.df["average_temperature"] = (
                self.df["chirts_era5_tmax"] + self.df["chirts_era5_tmin"]
            ) / 2.0
        elif "daymet_tmax" in self.df and "daymet_tmin" in self.df:
            self.df["average_temperature"] = (
                self.df["daymet_tmax"] + self.df["daymet_tmin"]
            ) / 2.0
        else:
            self.df["average_temperature"] = (
                self.df["cpc_tmax"] + self.df["cpc_tmin"]
            ) / 2.0

        # Determine available columns
        self.available_cols = [
            col for col in names_cols + [self.precip_var] if col in self.df.columns.values
        ]

        # Split by season
        self.df_current = self.df[self.df["harvest_season"] == frcast_yr]
        self.df_last = self.df[self.df["harvest_season"] == frcast_yr - 1]

        # Remove leap year day
        if 60 in self.df_current.doy.values:
            self.df_current = self.df_current[self.df_current.doy != 60]

    def _compute_historical_stats(self, var):
        """Compute mean/min/max from historical data with moving window averages."""
        df_mean_vals = self.df_previous.groupby(self.df_previous["doy"])[var].mean()
        df_mean_vals = df_mean_vals.reindex(index=self.df_current["doy"])

        df_min_vals = self.df_previous.groupby(self.df_previous["doy"])[var].min()
        df_min_vals = df_min_vals.reindex(index=self.df_current["doy"])

        df_max_vals = self.df_previous.groupby(self.df_previous["doy"])[var].max()
        df_max_vals = df_max_vals.reindex(index=self.df_current["doy"])

        df_last_vals = self.df_last.groupby("doy")[var].mean().reindex(index=self.df_current["doy"])

        curr_vals = bn.move_mean(self.df_current[var].values, window=self.window, min_count=1)
        last_vals = bn.move_mean(df_last_vals.values, window=self.window, min_count=1)
        past_vals = bn.move_mean(df_mean_vals.values, window=self.window, min_count=1)

        min_vals = bn.move_mean(
            np.minimum(df_min_vals.values, df_mean_vals.values), window=self.window, min_count=1
        )
        max_vals = bn.move_mean(
            np.maximum(df_max_vals.values, df_mean_vals.values), window=self.window, min_count=1
        )

        return df_mean_vals, curr_vals, last_vals, past_vals, min_vals, max_vals

    @staticmethod
    def _draw_trimmed(cur_ax, index, vals, **kwargs):
        """Plot vals against index; if lengths mismatch, truncate vals to match."""
        try:
            cur_ax.plot(index, vals, **kwargs)
        except Exception:
            cur_ax.plot(index, vals[:len(index)], **kwargs)

    @staticmethod
    def _build_gefs_dataframe(date1, date2, gefs_values):
        """Build a GEFS forecast DataFrame from date range and values, or return None."""
        date_range = [
            date1 + datetime.timedelta(days=i)
            for i in range((date2 - date1).days + 1)
        ]
        date_range = [x for x in date_range if x.month != 2 or x.day != 29]
        df_tmp = pd.DataFrame(date_range, columns=["date"])
        try:
            df_tmp.loc[:, "val"] = gefs_values
        except (ValueError, KeyError):
            return None
        df_tmp = df_tmp.set_index("date")
        df_tmp.index = pd.to_datetime(df_tmp.index)
        df_tmp = df_tmp[~((df_tmp.index.month == 2) & (df_tmp.index.day == 29))]
        df_tmp = df_tmp.fillna(0)
        return df_tmp

    def _draw_yearly_vi(self, cur_ax, vi_var):
        """Plot yearly VI comparison for either NDVI or GCVI."""
        from heapq import nsmallest
        is_ndvi = vi_var == "ndvi"

        yr_bound = (
            min(ar.utcnow().year, self.frcast_yr)
            if is_ndvi
            else max(ar.utcnow().year, self.frcast_yr)
        )
        closest = nsmallest(
            6, range(2001, yr_bound), key=lambda x: abs(x - self.frcast_yr)
        )
        closest.extend([self.frcast_yr])
        closest = sorted(set(closest))
        if len(closest) > 6:
            closest = closest[-6:]

        for y in closest:
            _cur = self.df[self.df["harvest_season"] == y]
            if "yield" in _cur.columns:
                _tmp = _cur["yield"]
                _yld = (
                    np.unique(_tmp[~np.isnan(_tmp)])[0]
                    if not _tmp.isnull().all()
                    else np.nan
                )
            else:
                _yld = np.nan
            if is_ndvi and y == self.frcast_yr:
                _yld = np.nan

            vals = _cur.groupby("doy")[vi_var].mean().reindex(index=self.df_current["doy"])
            vals = bn.move_mean(vals.values, window=self.window, min_count=1)
            vals = _lowess(vals, range(len(vals)), frac=1.0 / 5.0, it=3)

            label = str(y)
            if not np.isnan(_yld):
                label += f", {_yld:.2f} MT/ha"

            if y == self.frcast_yr:
                kwargs = dict(lw=1.5, color="b", label=label)
            elif y == self.frcast_yr - 1:
                kwargs = dict(lw=1.0, alpha=0.75, color=self.color_list[8], label=label)
            else:
                kwargs = dict(lw=1.0, alpha=0.75, label=label)

            self._draw_trimmed(cur_ax, self.df_current.index, vals, **kwargs)

        vi_name = "NDVI" if is_ndvi else "GCVI"
        plt.title(f"Recent 5 Years {vi_name} Comparison", fontsize=14)
        cur_ax.legend(loc="upper left", fontsize="small")

    def _draw_standard_lines(self, cur_ax, curr_vals, last_vals, past_vals,
                             min_vals, max_vals, idx):
        """Plot the standard current/last/mean/min-max lines used by multiple subplot types."""
        (a1,) = cur_ax.plot(
            self.df_current.index, curr_vals, color="b", lw=1.5,
            label=self.frcast_yr if idx == 0 else "",
        )
        (a2,) = cur_ax.plot(
            self.df_current.index, last_vals, color=self.color_list[8], lw=1.25,
            label=self.frcast_yr - 1 if idx == 0 else "",
        )
        (a3,) = cur_ax.plot(
            self.df_current.index, past_vals, color="k", lw=1.25,
            label="Mean" if idx == 0 else "",
        )
        a4 = cur_ax.fill_between(
            self.df_current.index, min_vals, max_vals, color="lightgray",
            label="Min/Max" if idx == 0 else "", alpha=0.7, lw=0,
        )
        return a1, a2, a3, a4

    def _draw_daily_precip(self, cur_ax, idx):
        """Draw daily precipitation bar chart with optional GEFS forecast."""
        plt.title("Precipitation (Daily)", fontsize=14)

        df_c = self.df_current[self.precip_var].resample("D").sum()
        cur_ax.bar(
            df_c.index, df_c.values, color="b",
            label=self.frcast_yr if idx == 0 else "", width=1.0,
        )

        if (
            df_c.index[-1].date() > ar.utcnow().date()
            and self.precip_var == "chirps"
            and "chirps_gefs" in self.df_current.columns
            and not self.df_current["chirps_gefs"].isnull().values.all()
        ):
            self.use_forecast = True
            date1 = ar.utcnow().date()
            date2 = ar.utcnow().shift(days=+15).date()
            val_gefs = self.df_current.loc[date1:date2]["chirps_gefs"].values
            df_tmp = self._build_gefs_dataframe(date1, date2, val_gefs)
            if df_tmp is not None:
                cur_ax.bar(
                    df_tmp.index, df_tmp.val.values,
                    color="tab:cyan", width=1.0, alpha=0.5,
                )

    def _draw_cumulative_precip(self, cur_ax, idx, df_mean_vals):
        """Draw cumulative precipitation line chart vs 5 year mean."""
        plt.title("Cumulative Precipitation (vs 5 year mean)", fontsize=14)

        df_c = self.df_current[self.precip_var].cumsum()
        df_m = df_mean_vals.cumsum()
        y1 = df_c.values
        y2 = df_m.values
        (a1,) = cur_ax.plot(df_c.index, y1, color="b")
        (a9,) = cur_ax.plot(df_c.index, y2, color="k")

        # Plot CHIRPS_GEFS if last date exceeds current date
        if (
            df_c.index[-1].date() > ar.utcnow().to("America/New_York").date()
            and self.precip_var == "chirps"
            and "chirps_gefs" in self.df_current.columns
            and not self.df_current["chirps_gefs"].isnull().values.all()
        ):
            self.use_forecast = True

            date1 = ar.utcnow().to("America/New_York").date()
            date2 = ar.utcnow().to("America/New_York").shift(days=+15).date()
            val_gefs = self.df_current.loc[date1:date2]["chirps_gefs"].values
            df_tmp = self._build_gefs_dataframe(date1, date2, val_gefs)

            if df_tmp is not None:
                cur_ax.plot(
                    np.nan, np.nan, "--",
                    color="tab:cyan", alpha=0.5, label="Forecast (16 day)",
                )

                try:
                    y2_gefs = df_m.loc[df_tmp.index.dayofyear]
                except (KeyError, IndexError):
                    y2_gefs = None

                val_gefs_cum = val_gefs.cumsum() + np.nanmax(df_c.values)

                if y2_gefs is not None:
                    try:
                        cur_ax.plot(
                            df_tmp.index, val_gefs_cum,
                            color="tab:cyan", linestyle="--", alpha=0.5,
                        )
                    except (ValueError, IndexError):
                        pass
                    try:
                        cur_ax.fill_between(
                            df_tmp.index, val_gefs_cum, y2_gefs,
                            where=y2_gefs >= val_gefs_cum,
                            lw=1.0, facecolor="red", alpha=0.2,
                        )
                        cur_ax.fill_between(
                            df_tmp.index, val_gefs_cum, y2_gefs,
                            where=y2_gefs <= val_gefs_cum,
                            lw=1.0, facecolor="green", alpha=0.2,
                        )
                    except (ValueError, IndexError):
                        pass

        cur_ax.fill_between(
            df_c.index, y1, y2, where=y2 >= y1, lw=1.0, facecolor="red", alpha=0.2
        )
        cur_ax.fill_between(
            df_c.index, y1, y2, where=y2 <= y1, lw=1.0, facecolor="green", alpha=0.2
        )

        cur_ax.fill(np.nan, np.nan, "red", alpha=0.2, label="< 5 year mean")
        cur_ax.fill(np.nan, np.nan, "green", alpha=0.2, label="> 5 year mean")
        cur_ax.legend(loc="upper left", fontsize="small")

    def _draw_temperature(self, cur_ax, idx):
        """Draw temperature plot with extreme markers."""
        plt.title("Temperature (daily mean)", fontsize=14)

        (
            df_mean_vals,
            curr_vals,
            last_vals,
            past_vals,
            min_vals,
            max_vals,
        ) = self._compute_historical_stats("average_temperature")

        a1, a2, a3, a4 = self._draw_standard_lines(
            cur_ax, curr_vals, last_vals, past_vals, min_vals, max_vals, idx,
        )

        tmax_col = next(
            (c for c in ["chirts_era5_tmax", "daymet_tmax", "cpc_tmax"]
             if c in self.df_current.columns), "cpc_tmax"
        )
        tmin_col = next(
            (c for c in ["chirts_era5_tmin", "daymet_tmin", "cpc_tmin"]
             if c in self.df_current.columns), "cpc_tmin"
        )

        mask_max = self.df_current[tmax_col] > 30
        mask_min = self.df_current[tmin_col] < 5

        cur_ax.plot(
            self.df_current.index[mask_max],
            self.df_current[mask_max][tmax_col],
            "ro", markersize=2, label="Max temp > 30°C",
        )
        cur_ax.plot(
            self.df_current.index[mask_min],
            self.df_current[mask_min][tmin_col],
            "co", markersize=2, label="Min temp < 5°C",
        )

        cur_ax.legend(loc="upper left", fontsize="small")
        return a1, a2, a3, a4

    # -- FLDAS panel-type → base variable mapping --
    _FLDAS_PANEL_MAP = {
        "temperature": "tair_tavg",
        "precip": "totalprecip_tavg",
        "soil_moisture": "soilmoist_tavg",
    }

    def _overlay_fldas_dots(self, cur_ax, panel_type):
        """Overlay FLDAS forecast dots on an existing subplot.

        Uses the most recent initialization month's data and plots each
        lead at its target month (init + lead).  Only future months
        (after today) up to the harvest date are shown.
        """
        fldas_var = self._FLDAS_PANEL_MAP.get(panel_type)
        if fldas_var is None:
            return

        lead0_col = f"fldas_{fldas_var}_lead0"
        if lead0_col not in self.df_current.columns:
            return

        harvest_date = self.dates_cal[3] if self.dates_cal and self.dates_cal[3] else None
        today = pd.Timestamp.now().normalize()

        # Find the last month with non-null FLDAS data (most recent init)
        monthly = self.df_current.groupby(self.df_current.index.month)
        init_month_grp = None
        for _, grp in monthly:
            if grp[lead0_col].notna().any():
                init_month_grp = grp

        if init_month_grp is None:
            return

        # Determine initialization month from the group
        init_date = init_month_grp.index[0]
        init_year, init_mo = init_date.year, init_date.month

        added_legend = False
        for lead in range(1, 6):  # skip lead 0 (init month, not a forecast)
            col = f"fldas_{fldas_var}_lead{lead}"
            if col not in init_month_grp.columns:
                continue
            val = init_month_grp[col].dropna()
            if val.empty:
                continue

            # Place dot at 15th of the target month (monthly average data)
            tgt_mo = init_mo + lead
            tgt_yr = init_year + (tgt_mo - 1) // 12
            tgt_mo = ((tgt_mo - 1) % 12) + 1
            target_date = pd.Timestamp(tgt_yr, tgt_mo, 15)

            if target_date < today:
                continue
            if harvest_date and target_date > harvest_date:
                continue

            y = val.iloc[0]
            label = "FLDAS forecast" if not added_legend else ""
            cur_ax.plot(
                target_date, y, marker="D", color="tab:orange",
                markersize=5, alpha=0.8, linestyle="none",
                label=label, zorder=5,
            )
            if label:
                added_legend = True

    def _add_annotations(self, fig, leg):
        """Add logos, data sources, production share, and footer text."""
        if self.show_logos and self.logos:
            # Any number of logos, laid out left-to-right at the fixed corner
            # anchors (single-logo lists — e.g. the USA NASA-Acres branding —
            # draw just one image).
            _positions = [(150, 2250), (450, 2300), (750, 2300)]
            _max_w, _max_h = self.logo_max_px
            for _logo, (_x, _y) in zip(self.logos, _positions):
                im = load_scaled_logo(_logo, _max_w, _max_h)
                fig.figimage(im, _x, _y, zorder=3)

        # Configure legend FIRST so its title position can be measured
        leg.get_frame().set_facecolor("none")
        leg.set_title("Legend", prop={"size": 14, "weight": "heavy"})
        leg.get_frame().set_linewidth(0.0)
        leg._legend_box.align = "left"

        # Data Sources — fixed y, well above the body (which is anchored
        # at 0.13). Previously computed dynamically from the Legend
        # title's rendered bbox so the two headers would visually align;
        # that calculation depended on the legend's handle count (FLDAS
        # forecast handle and per-year history items aren't always
        # present), which made it land below 0.13 on some country plots
        # and overlap the first line of the body. A constant keeps
        # every plot in the gallery looking the same.
        if self.precip_var == "chirps":
            precip_str = "Precipitation: CHIRPS\n"
        elif self.precip_var == "daymet_prcp":
            precip_str = "Precipitation: Daymet V4\n"
        else:
            precip_str = "Precipitation: NOAA CPC\n"
        if self.use_forecast:
            precip_str += "Precipitation Forecast: CHIRPS-GEFS\n"
        if "chirts_era5_tmax" in self.df.columns:
            temp_str = "Temperature: CHIRTS-ERA5\n"
        elif "daymet_tmax" in self.df.columns:
            temp_str = "Temperature: Daymet V4\n"
        else:
            temp_str = "Temperature: NOAA CPC\n"
        fldas_str = ""
        if any(c.startswith("fldas_") for c in self.df.columns):
            fldas_str = "Forecast: FLDAS NMME\n"
        body = (
            "NDVI: UMD GLAM system\n"
            + temp_str
            + precip_str
            + "Evaporative Stress Index: NASA ESI\n"
            + "Soil Moisture: NASA-USDA Global Soil Moisture\n"
            + fldas_str
        )
        # The body is anchored at DATA_SOURCES_BODY_Y and grows UPWARD, and its
        # line count varies per run (the forecast and FLDAS lines appear
        # conditionally), so a constant header y eventually collides with the
        # top body line — as it did on the 6-line USA agmet figures. Derive the
        # header position from the actual line count instead: deterministic and
        # render-free, unlike the old legend-bbox measurement this replaced.
        fs = plt.rcParams["font.size"]
        fig.text(
            0.83, DATA_SOURCES_BODY_Y, body,
            linespacing=DATA_SOURCES_LINESPACING, va="bottom", fontsize=fs,
        )
        ds_y = data_sources_header_y(
            n_lines=len([ln for ln in body.split("\n") if ln.strip()]),
            fig_height_in=fig.get_figheight(),
            fontsize=fs,
        )
        fig.text(
            0.83, ds_y, "Data Sources",
            fontsize=14, fontweight="bold", va="bottom",
        )

        from geocif.viz import diagnostics as _diag
        if (_diag.is_production_share_shown()
                and self.production_pct is not None
                and not np.isnan(self.production_pct)):
            fig.text(
                0.83, 0.09,
                f"{self.production_pct:.1f}% of national production (5 yr avg)",
                fontsize=9, fontstyle="italic",
            )

        fig.text(
            0.67, 0.04,
            r"$\blacktriangleright$ Crop growth stage dates are based on the 5 year average GEOGLAM best available crop calendars",
            fontsize=9,
        )
        fig.text(
            0.91, 0.02,
            f"Produced on: {ar.utcnow().to('America/New_York').format('MMM DD YYYY')}",
            fontsize=9,
        )

    def _add_inset_map(self, fig):
        """Draw a small country map with the current region highlighted in black."""
        if self.boundary_gdf is None or self.boundary_gdf.empty:
            return
        try:
            gdf = self.boundary_gdf
            # Derive column name from config admin_level (e.g. "admin_2" → "ADMIN2")
            level_num = self.admin_level.replace("admin_", "") if self.admin_level else "1"
            name_col = next(
                (c for c in [f"ADM{level_num}_NAME", f"ADMIN{level_num}"] if c in gdf.columns),
                None,
            )
            if name_col is None:
                return

            # Derive available space from subplot layout and title position
            all_axes = fig.get_axes()
            subplot_top = max(a.get_position().y1 for a in all_axes)

            renderer = fig.canvas.get_renderer()
            title_bbox = fig._suptitle.get_window_extent(renderer)
            title_right = title_bbox.transformed(fig.transFigure.inverted()).x1
            x_left = title_right
            max_w = 0.99 - x_left

            available_h = 0.98 - subplot_top
            h = available_h * 0.95

            bounds = gdf.total_bounds
            dx, dy = bounds[2] - bounds[0], bounds[3] - bounds[1]
            if dx == 0 or dy == 0:
                return
            geo_aspect = dx / dy
            w = h * geo_aspect

            if w > max_w:
                w = max_w
                h = w / geo_aspect

            ax_map = fig.add_axes([x_left, 0.99 - h, w, h])
            ax_map.set_axis_off()

            # Keep only polygon geometries (drop stray points/lines)
            gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()

            # Draw country as single dissolved polygon (avoids tiny admin_2 dots)
            dissolved = gdf.dissolve()
            dissolved.plot(ax=ax_map, color="lightgray", edgecolor="black", linewidth=1.0)

            # Highlight region: use highlight_gdf (district) or match by name (adm1).
            # When region_id is given AND boundary_gdf carries ADM_ID, prefer ID-based
            # match so counties sharing a name across states (e.g. Kiowa in CO/KS/OK)
            # don't all light up together.
            if self.highlight_gdf is not None and not self.highlight_gdf.empty:
                hgdf = self.highlight_gdf[
                    self.highlight_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])
                ]
                if not hgdf.empty:
                    # Clip highlight to the dissolved boundary so the blue
                    # never spills past the gray outline (e.g. a state polygon
                    # from shp_region extends beyond the sorghum counties).
                    try:
                        import geopandas as gpd
                        if hgdf.crs != dissolved.crs:
                            hgdf = hgdf.to_crs(dissolved.crs)
                        hgdf = gpd.clip(hgdf, dissolved)
                    except Exception:
                        pass
                    if not hgdf.empty:
                        hgdf.plot(ax=ax_map, color="royalblue", edgecolor="royalblue")
            elif self.region_id is not None and "ADM_ID" in gdf.columns:
                mask = gdf["ADM_ID"].astype(str) == str(self.region_id)
                gdf[mask].plot(ax=ax_map, color="royalblue", edgecolor="royalblue")
            elif self.region:
                region_clean = self.region.replace("_", " ").lower()
                mask = gdf[name_col].str.lower().str.replace("_", " ") == region_clean
                gdf[mask].plot(ax=ax_map, color="royalblue", edgecolor="royalblue")
        except Exception:
            pass

    def plot(self):
        """Create and save the multi-panel agmet figure."""
        os.makedirs(self.dir_out, exist_ok=True)

        # Check if current season has any non-NaN data
        _num_nans = 0
        for col in self.available_cols:
            if np.all(np.isnan(utils.sliding_mean(self.df_current[col].values, window=self.window))):
                _num_nans += 1

        if _num_nans == len(self.available_cols):
            return pd.DataFrame()

        # Build previous-years DataFrame
        self.df_previous = self.df[
            np.isin(self.df["month"], self.df_current.index.month)
            & np.isin(self.df["day"], self.df_current.index.day)
            & (self.df["harvest_season"].isin(self.closest))
        ]
        self.df_previous = self.df_previous[np.isfinite(self.df_previous["harvest_season"])]
        self.df_previous = self.df_previous[
            self.df_previous["harvest_season"] < datetime.datetime.now().year
        ]

        _tmax_col = next(
            (c for c in ["chirts_era5_tmax", "daymet_tmax", "cpc_tmax"]
             if c in self.df_current.columns), None
        )
        if (
            self.df_current.empty
            or self.df_previous.empty
            or _tmax_col is None
            or self.df_current[_tmax_col].isnull().values.all()
        ):
            return pd.DataFrame()

        # Create figure
        ncols = 3 if int(len(self.names_cols) / 2.0) >= 2 else int(math.floor(len(self.names_cols) / 2.0))
        nrows = int(math.ceil(len(self.names_cols) / 3.0))

        fig, ax = plt.subplots(nrows, ncols, squeeze=False, figsize=(20, 10))
        for i in range(len(self.names_cols), nrows * ncols):
            fig.delaxes(ax.flatten()[i])

        fig.suptitle(self.sup_title, fontsize=16, fontweight="bold")
        rcParams["xtick.labelsize"] = 12
        rcParams["ytick.labelsize"] = 12
        rcParams["axes.labelsize"] = 12

        # Legend handles
        a1 = a2 = a3 = a4 = a5 = a6 = a7 = a8 = None

        # Draw each subplot
        for idx in range(len(self.names_cols)):
            subplot_name = self.names_cols[idx]

            if subplot_name in ["cumulative_precip", "daily_precip"]:
                cur_var = self.precip_var
            elif subplot_name in ["ndvi", "yearly_ndvi"]:
                cur_var = "ndvi"
            elif subplot_name in ["gcvi", "yearly_gcvi"]:
                cur_var = "gcvi"
            else:
                cur_var = subplot_name

            cur_ax = plt.subplot(nrows, ncols, idx + 1)
            ax[idx // 3, idx % 3] = cur_ax

            # X-axis date formatting
            cur_ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
            cur_ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator(range(1, 13)))
            cur_ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("\n%Y"))
            cur_ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter("%b"))

            plt.title(utils.dict_vars.get(cur_var)[0], fontsize=14)
            plt.ylabel(utils.dict_vars.get(cur_var)[1], fontsize=10)
            try:
                if np.all(np.isnan(self.df_current[cur_var].values)):
                    cur_ax.text(0.3, 0.5, "No within season data available yet")
                    continue
            except Exception:
                continue

            (
                df_mean_vals,
                curr_vals,
                last_vals,
                past_vals,
                min_vals,
                max_vals,
            ) = self._compute_historical_stats(cur_var)

            if cur_var in ["ndvi", "gcvi"]:
                curr_vals, last_vals, min_vals, max_vals = [
                    _lowess(v, range(len(v)), frac=1.0 / 5.0, it=3)
                    for v in [curr_vals, last_vals, min_vals, max_vals]
                ]

            if np.isnan(curr_vals).all():
                cur_ax.text(0.3, 0.5, "No within season data available yet")
                continue

            cur_ax.grid(which="major", alpha=0.5, linestyle="--")
            cur_ax.grid(which="minor", alpha=0.5, linestyle="--")

            if subplot_name == "daily_precip":
                self._draw_daily_precip(cur_ax, idx)
                self._overlay_fldas_dots(cur_ax, "precip")
            elif subplot_name == "cumulative_precip":
                self._draw_cumulative_precip(cur_ax, idx, df_mean_vals)
            elif subplot_name == "yearly_ndvi":
                self._draw_yearly_vi(cur_ax, "ndvi")
            elif subplot_name == "yearly_gcvi":
                self._draw_yearly_vi(cur_ax, "gcvi")
            elif subplot_name in ("cpc_tmax", "chirts_era5_tmax", "daymet_tmax"):
                a1, a2, a3, a4 = self._draw_temperature(cur_ax, idx)
                self._overlay_fldas_dots(cur_ax, "temperature")
            else:
                a1, a2, a3, a4 = self._draw_standard_lines(
                    cur_ax, curr_vals, last_vals, past_vals, min_vals, max_vals, idx,
                )
                if subplot_name in ("nsidc_surface", "soil_moisture_as1"):
                    self._overlay_fldas_dots(cur_ax, "soil_moisture")

            # Crop calendar vertical lines
            if self.dates_cal:
                if self.dates_cal[0]:
                    a5 = cur_ax.axvline(
                        self.dates_cal[0], color=self.color_list[10],
                        label="Planting", lw=1.5, linestyle="--",
                    )
                if self.dates_cal[1]:
                    a6 = cur_ax.axvline(
                        self.dates_cal[1], color=self.color_list[4],
                        label="Greenup", lw=1.5,
                    )
                if self.dates_cal[2]:
                    a7 = cur_ax.axvline(
                        self.dates_cal[2], color="darkgoldenrod",
                        label="Senescence", lw=1.5,
                    )
                if self.dates_cal[3]:
                    a8 = cur_ax.axvline(
                        self.dates_cal[3], color=self.color_list[6],
                        label="Harvest", lw=1.5, linestyle="--",
                    )

        # Build figure legend
        if self.dates_cal:
            handles_labels = [
                (a1, str(self.frcast_yr)),
                (a2, str(self.frcast_yr - 1)),
                (a3, "5 year Mean"),
                (a4, "10 year Min/Max"),
                (a5, "Planting"),
                (a6, "Greenup"),
                (a7, "Senescence"),
                (a8, "Harvest"),
            ]
        else:
            handles_labels = [
                (a1, str(self.frcast_yr)),
                (a3, "5 year Mean"),
                (a4, "5 year Min/Max"),
            ]

        handles_labels = [(h, l) for h, l in handles_labels if h is not None]
        if handles_labels:
            handles, all_labels = zip(*handles_labels)
            leg = plt.figlegend(
                handles, all_labels, loc="lower center", bbox_to_anchor=[0.76, 0.06]
            )

        self._add_annotations(fig, leg)

        # Final layout and save
        plt.tight_layout()
        plt.subplots_adjust(top=0.88)
        self._add_inset_map(fig)
        plt.savefig(self.dir_out / self.fname, dpi=constants.DPI)
        plt.close()

        set_matplotlib_params()
