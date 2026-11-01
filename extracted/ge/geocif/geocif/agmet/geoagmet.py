"""Agricultural Meteorology (Agmet) Monitoring Runner.

Generates multi-panel time-series plots of climate and vegetation
indicators per region and district, with crop calendar overlays
and optional FLDAS forecast dots.

Usage::

    from geocif.agmet import geoagmet
    geoagmet.run(cfg_geocif)
"""

import ast
import os
import re
import shutil
import zipfile
import multiprocessing as mp
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import arrow as ar
import numpy as np
import pandas as pd
from heapq import nsmallest
from tqdm.rich import tqdm

from geoprepare import base
from geocif.agmet import plot, utils
from geocif.ml import stats
from geocif import utils as ut

# Show usage info on import
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console()
_table = Table(show_header=False, box=None, padding=(0, 1))
_table.add_column(style="bold cyan", no_wrap=True)
_table.add_column()
_table.add_row("Usage", "from geocif.agmet import geoagmet; geoagmet.run(cfg)")
_table.add_row("cfg", "\\[geobase.txt, countries.txt, crops.txt, geocif.txt]")
_console.print(Panel(_table, title="[bold bright_white]GeoCIF Agmet Runner[/]", border_style="bright_blue", padding=(1, 2)))


class AgmetGeo(base.BaseGeo):
    """Lightweight geo object for agmet plots. No Neptune dependency."""

    def __init__(self, path_config_file):
        super().__init__(path_config_file)
        self.parse_config()

    def _get_option(self, option, default=None, sections=("AGMET", "DEFAULT")):
        """Get a config option, checking sections in order."""
        for section in sections:
            if self.parser.has_option(section, option):
                return ast.literal_eval(self.parser.get(section, option))
        return default

    def parse_config(self, section="DEFAULT"):
        self.project_name = self.parser.get("DEFAULT", "project_name")
        super().parse_config(project_name=self.project_name, section="DEFAULT")

        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.forecast_seasons = self._get_option(
            "agmet_seasons", [ar.utcnow().year]
        )
        self.plot_seasons = self._get_option(
            "plot_seasons", self.forecast_seasons
        )
        self.models = self._get_option("models", [])
        eo_plot_raw = self._get_option(
            "eo_plot",
            ["ndvi", "chirts_era5_tmax", "chirts_era5_tmin", "chirps", "esi_4wk", "nsidc_surface", "nsidc_rootzone"],
        )
        self.plot_snow_thickness = self.parser.getboolean(
            "AGMET", "plot_snow_thickness", fallback=False
        )
        self.eo_plot = self._expand_eo_plot(eo_plot_raw, self.plot_snow_thickness)
        # Unit of the yields shown in the recent-years NDVI legend; the same
        # per-project key the ML plots read (poppy: kg/ha).
        self.yield_units = self.parser.get("ML", "yield_units", fallback="MT/ha")
        self.eo_model = self._get_option(
            "eo_model",
            ["ndvi", "chirts_era5_tmax", "chirts_era5_tmin", "chirps", "esi_4wk", "nsidc_surface", "nsidc_rootzone"],
        )
        self.logo_harvest = self.dir_metadata / "images" / self.parser.get(
            "AGMET", "logo_harvest"
        )
        self.logo_geoglam = self.dir_metadata / "images" / self.parser.get(
            "AGMET", "logo_geoglam"
        )
        # USA branding: any USA plot carries the NASA Acres logo INSTEAD of
        # the Harvest + GEOGLAM pair (standing rule, 2026-08-16). File
        # configurable via [AGMET] logo_usa; default acres.png.
        self.logo_usa = self.dir_metadata / "images" / self.parser.get(
            "AGMET", "logo_usa", fallback="acres.png"
        )
        # Logo display box in pixels (figimage draws at native size — a 3089px
        # wide asset would otherwise cover the figure). See plot.LOGO_MAX_PX.
        self.logo_max_px = (
            self.parser.getint("AGMET", "logo_max_width_px", fallback=plot.LOGO_MAX_PX[0]),
            self.parser.getint("AGMET", "logo_max_height_px", fallback=plot.LOGO_MAX_PX[1]),
        )
        # When True, county-level filenames get the admin_1 (state) appended:
        # {region}_{state}.png — needed where ADM2_NAME collides across states
        # (e.g. Kiowa in CO/KS/OK).  Default off for backward compatibility.
        self.filename_with_state = self.parser.getboolean(
            "AGMET", "filename_with_state", fallback=False
        )
        # When True, the two corner logos are drawn on the figure.  Set False
        # to suppress them entirely (e.g. for partner-branded reports).
        self.show_logos = self.parser.getboolean(
            "AGMET", "show_logos", fallback=True
        )
        # Layout for county runs such as the USA. All off by default, so other
        # projects keep their folders, file names, titles and locator map.
        #   region_folder     folder for per-unit figures (default adm1/adm2)
        #   group_by_admin_1  admin_2 figures go to <admin_1>/<id>_<name>.png,
        #                     are titled "<Name>, <Admin_1> (<district>)", and
        #                     the locator map shows the admin_1 unit
        #   id_width          zero-pad numeric ids in those names (5 = US FIPS)
        #   district_file     region -> district table (read_district_file);
        #                     district figures are drawn per district instead
        #                     of per calendar region
        #   district_folder   folder for district figures (default district)
        self.region_folder = self.parser.get("AGMET", "region_folder", fallback="").strip()
        self.group_by_admin_1 = self.parser.getboolean(
            "AGMET", "group_by_admin_1", fallback=False
        )
        self.id_width = self.parser.getint("AGMET", "id_width", fallback=0)
        self.district_folder = (
            self.parser.get("AGMET", "district_folder", fallback="").strip() or "district"
        )
        district_file = self.parser.get("AGMET", "district_file", fallback="").strip()
        self.district_table = (
            read_district_file(self.dir_boundary_files / district_file)
            if district_file else None
        )

        # Honor [ML] show_production_share (default True): suppress the
        # "% of national production" caption on crop-condition figures for
        # projects where the region share is misleading (e.g. poppy).
        from geocif.viz import diagnostics as _diag
        _diag.set_show_production_share(
            _diag.show_production_share_from_parser(self.parser)
        )

    @staticmethod
    def _expand_eo_plot(eo_plot_raw, plot_snow_thickness=False):
        """Map raw EO variable names to subplot names in GEOGLAM display order.

        Layout (3 columns):
            Row 0: ndvi            | cumulative_precip | <soil/other>
            Row 1: yearly_ndvi     | daily_precip      | <soil/other>
            Row 2: esi_4wk         | cpc_tmax          | ...

        When ``plot_snow_thickness`` is True, the sub-surface soil moisture
        subplot (``nsidc_rootzone``) is replaced in-place by AgERA5 snow
        thickness (LWE), preserving the layout slot.
        """
        # Desired order of subplot names matching GEOGLAM layout
        ordered = [
            "ndvi", "cumulative_precip", "nsidc_surface",
            "yearly_ndvi", "daily_precip", "nsidc_rootzone",
            "esi_4wk", "cpc_tmax", "chirts_era5_tmax", "daymet_tmax",
        ]

        # Which raw vars expand into which subplot names
        expansions = {
            "ndvi": ["ndvi", "yearly_ndvi"],
            "chirps": ["cumulative_precip", "daily_precip"],
            "daymet_prcp": ["cumulative_precip", "daily_precip"],
            "gcvi": ["gcvi", "yearly_gcvi"],
        }
        # These raw vars get dropped (absorbed into the avg temp plot)
        skip = {"cpc_tmin", "daymet_tmin", "chirts_era5_tmin"}

        # Build set of subplot names from raw eo_plot
        subplot_set = set()
        for var in eo_plot_raw:
            if var in skip:
                continue
            if var in expansions:
                subplot_set.update(expansions[var])
            else:
                subplot_set.add(var)

        # Return in GEOGLAM order, then any extras not in the template
        result = [s for s in ordered if s in subplot_set]
        extras = [s for s in subplot_set if s not in ordered]
        final = result + extras

        if plot_snow_thickness:
            final = [
                "agera5_snow_thickness_lwe" if s == "nsidc_rootzone" else s
                for s in final
            ]

        return final

    def logos_for_country(self, country: str) -> list:
        """Logo set for a country's plots: USA -> NASA Acres only (standing
        rule, 2026-08-16); everywhere else -> Harvest + GEOGLAM."""
        c = str(country).lower()
        if "united_states" in c or c in ("usa", "us"):
            return [self.logo_usa]
        return [self.logo_harvest, self.logo_geoglam]

    def read_statistics(self, country=None, read_countries=False, **kwargs):
        """Read zone/country info. country is optional when only reading countries."""
        if read_countries:
            path_countries = (
                self.dir_metadata / self.parser.get("DEFAULT", "zone_file")
            )
            self.df_countries = (
                pd.read_csv(path_countries)
                if path_countries.is_file()
                else pd.DataFrame()
            )
        if country is not None:
            super().read_statistics(country, read_countries=read_countries, **kwargs)

    def get_calendar_region_for_region(self, df, region):
        return df[df["region"] == region]["calendar_region"].values[0]

    def setup_country(self, country, scale, crop, growing_season):
        self.country = country
        self.scale = scale
        self.crop = crop
        self.growing_season = growing_season
        # category becomes a directory-path segment (plots/{category}/...) and
        # is matched literally by _finalize_plots against "AMIS"/"EWCM". Strip
        # stray surrounding quotes/whitespace so a quoted config value (e.g.
        # `category = 'EWCM'`) doesn't create a mismatched dir that silently
        # breaks the AMIS/EWCM ZIP finalize step.
        self.category = self.parser.get(country, "category").strip().strip("'\"")
        self.use_cropland_mask = self.parser.getboolean(country, "use_cropland_mask")

        self.get_dirname(country)
        self.get_ccs_dataframe(country, scale, crop, growing_season)
        self.add_yield_statistics(country, crop)

        self.list_regions = self.df_ccs["region"].unique()
        self.list_calendar_regions = self.df_ccs["calendar_region"].unique()

        if "chirps" in self.df_ccs.columns.values:
            self.precip_var = "chirps"
        elif "daymet_prcp" in self.df_ccs.columns.values:
            self.precip_var = "daymet_prcp"
        else:
            self.precip_var = "cpc_precip"

    def setup_region(self, region, plot_season, type_region="region"):
        self.region = region
        self.calendar_region = self.get_calendar_region_for_region(self.df_ccs, region)
        self.plot_season = plot_season
        self.type_region = type_region

        if type_region == "region":
            self.df_region = self.df_ccs[self.df_ccs["region"] == region].copy()
        elif type_region == "calendar_region":
            self.df_region = self.df_ccs[
                self.df_ccs["calendar_region"] == self.calendar_region
            ].copy()
        elif type_region == "region_year":
            self.df_region = self.df_ccs[
                (self.df_ccs["region"] == region) & (self.df_ccs["year"] == plot_season)
            ].copy()
        elif type_region == "calendar_region_year":
            self.df_region = self.df_ccs[
                (self.df_ccs["calendar_region"] == self.calendar_region)
                & (self.df_ccs["year"] == plot_season)
            ].copy()
        else:
            raise ValueError(f"Unknown type_region: {type_region}")

        self.df_region.index = pd.to_datetime(self.df_region.index)

        crop_short = utils.get_crop_abbrev(self.crop)

        # Abbreviate scale: admin_1 → adm1, admin_2 → adm2
        self.scale_short = self.scale.replace("admin_", "adm")

        folder = f"{crop_short}_s{self.growing_season}_{self.plot_season}"
        self.dir_agmet = (
            self.dir_output
            / "crop_condition"
            / ar.now().format("MMMM_DD_YYYY")
            / "plots"
            / self.category
            / self.country
            / folder
            / "condition"
        )

        (
            self.date_planting,
            self.date_greenup,
            self.date_senescence,
            self.date_harvesting,
        ) = self.get_calendar(self.region, self.plot_season)

    def create_run_combinations(self):
        all_combinations = []

        for country in self.countries:
            admin_level = self.parser.get(country, "admin_level")
            crops = ast.literal_eval(self.parser.get(country, "crops"))

            # Use configured seasons if available, otherwise auto-detect per crop
            has_seasons = self.parser.has_option(country, "seasons") or self.parser.has_option("DEFAULT", "seasons")

            for crop in crops:
                if has_seasons:
                    seasons = ast.literal_eval(self.parser.get(country, "seasons"))
                else:
                    from pathlib import Path
                    dir_calendars = Path(self.parser.get("PATHS", "dir_crop_calendars"))
                    calendar_file = self.parser.get(country, "calendar_file")
                    seasons = ut.detect_seasons_from_calendar(
                        dir_calendars / calendar_file,
                        country.replace("_", " ").title(),
                        crop,
                    )
                    self.logger.info(f"Auto-detected seasons {seasons} for {country} {crop}")

                for season in seasons:
                    all_combinations.append(
                        (country, admin_level, crop, season)
                    )

        return all_combinations

    def get_calendar(self, region, forecast_season):
        SEASON = "harvest_season"
        CAL = "crop_calendar"

        df_sub = self.df_ccs[self.df_ccs["region"] == region]
        df_sub.index = pd.to_datetime(df_sub.index)
        sr_cal = df_sub[df_sub[SEASON] == forecast_season][["doy", CAL]]

        sr_cal[CAL] = pd.to_numeric(sr_cal[CAL], errors="coerce")

        if sr_cal.empty:
            return np.nan, np.nan, np.nan, np.nan
        else:
            date_planting = (sr_cal[CAL] == 1).idxmax()
            date_greenup = (
                (sr_cal[CAL] == 2).idxmax() if len(sr_cal[sr_cal[CAL] == 2]) else None
            )
            date_senesc = (
                (sr_cal[CAL][::-1] == 2).idxmax()
                if len(sr_cal[sr_cal[CAL] == 3])
                else None
            )
            date_harvesting = (
                (sr_cal[CAL][::-1] == 3).idxmax()
                if len(sr_cal[sr_cal[CAL] == 3])
                else None
            )

            return date_planting, date_greenup, date_senesc, date_harvesting

    def get_ccs_dataframe(self, country, scale, crop, growing_season):
        dir_ccs = self.dir_output / self.dir_threshold / country

        self.df_ccs = pd.read_csv(
            dir_ccs / f"{country}_{crop}_s{growing_season}.csv", index_col=0
        ).copy()

        self.df_ccs = self.df_ccs.assign(datetime=pd.to_datetime(self.df_ccs.index))
        self.df_ccs.index.name = None

        # Advance NDVI by 8 days to match GEOGLAM convention
        # (NDVI composites represent data from ~8 days prior)
        if "ndvi" in self.df_ccs.columns:
            self.df_ccs["ndvi"] = self.df_ccs.groupby("region")["ndvi"].shift(8)

    def add_yield_statistics(self, country, crop):
        """Add yield data from FEWSNET/GEOGLAM stats to df_ccs."""
        # Add temporary columns expected by stats.add_statistics
        self.df_ccs = self.df_ccs.assign(
            Region=self.df_ccs["region"],
            **{"Harvest Year": self.df_ccs["harvest_season"]},
            Season=int(self.growing_season),
        )

        country_str = country.replace("_", " ").title()
        crop_str = utils.get_crop_name(crop)

        self.df_ccs = stats.add_statistics(
            dir_stats=self.dir_production_statistics,
            df=self.df_ccs,
            country=country_str,
            crop=crop_str,
            admin_zone=self.scale,
            stats=["Yield (tn per ha)", "Production (tn)", "Area (ha)"],
            method="",
            parser=self.parser,
        )

        # Map result back to the yield column used by agmet plotting
        if "Yield (tn per ha)" in self.df_ccs.columns:
            self.df_ccs["yield"] = self.df_ccs["Yield (tn per ha)"]

        # Compute production share (%) per region based on last 5 years
        self.df_ccs["production_share_pct"] = np.nan
        if "Production (tn)" in self.df_ccs.columns:
            prod = (
                self.df_ccs.groupby(["region", "harvest_season"])["Production (tn)"]
                .first()
                .reset_index()
                .dropna(subset=["Production (tn)"])
            )
            if not prod.empty:
                last_5_years = sorted(prod["harvest_season"].unique())[-5:]
                prod = prod[prod["harvest_season"].isin(last_5_years)]
                mean_by_region = prod.groupby("region")["Production (tn)"].mean()
                national_total = mean_by_region.sum()
                if national_total > 0:
                    share = (mean_by_region / national_total * 100)
                    self.df_ccs["production_share_pct"] = self.df_ccs["region"].map(share)

        # Drop temporary columns
        drop_cols = ["Region", "Harvest Year", "Season", "Yield (tn per ha)",
                     "Area (ha)", "Production (tn)", "Area"]
        self.df_ccs.drop(
            columns=[c for c in drop_cols if c in self.df_ccs.columns],
            inplace=True,
        )

    def get_closest_season(self, season):
        self.closest = nsmallest(
            5 + 1, range(2001, ar.utcnow().year), key=lambda x: abs(x - season)
        )

        if season in self.closest:
            self.closest.remove(season)

    def check_date(self, df, plot_season):
        try:
            last_valid_date = pd.to_datetime(df["chirps"].last_valid_index()).date()

            bool_year_check = ar.utcnow().year <= plot_season
            bool_date_check = (last_valid_date > self.date_planting.date()) & (
                last_valid_date < self.date_harvesting.date()
            )

            return bool_year_check, bool_date_check
        except Exception:
            return False, False

    def add_precip_forecast(self, plot_season):
        # Only add chirps_gefs column if not already present (don't wipe existing data)
        if "chirps_gefs" not in self.df_ccs.columns:
            self.df_ccs["chirps_gefs"] = np.nan
        if "chirps_gefs" not in self.df_region.columns:
            self.df_region["chirps_gefs"] = np.nan

        try:
            bool_year_check, bool_date_check = self.check_date(
                self.df_region, plot_season
            )
        except Exception:
            return

        if not (bool_year_check & bool_date_check):
            return

        base_dir = self.dir_output / self.dir_threshold / self.country / self.scale
        path_gefs = (
            base_dir / "cr" / "chirps_gefs"
            if self.use_cropland_mask
            else base_dir / self.crop / "chirps_gefs"
        )

        region_name = self.df_region["region"].unique()[0]

        # Try current season, fall back to previous season
        # Filenames are {region_id}_{region_name}_{year}_{var}_{crop}.csv
        gefs_files = list(path_gefs.glob(f"*{region_name}*{plot_season}*.csv"))
        if not gefs_files:
            gefs_files = list(path_gefs.glob(f"*{region_name}*{plot_season - 1}*.csv"))
        if not gefs_files:
            return

        df_gefs = pd.read_csv(gefs_files[0])

        # Remove leap year day (doy 60)
        if 60 in df_gefs["doy"].values:
            df_gefs = df_gefs[df_gefs["doy"] != 60]

        # Get forecast values, replace NaN with 0
        val_gefs = np.nan_to_num(np.asarray(df_gefs["chirps_gefs"]))

        # Assign to 15-day forecast window (today → today+14)
        now = ar.utcnow().to("America/New_York")
        start_date = now.date()
        end_date = now.shift(days=+14).date()

        try:
            self.df_region.loc[start_date:end_date, "chirps_gefs"] = val_gefs
        except Exception:
            self.df_region.loc[start_date:end_date, "chirps_gefs"] = np.nan

        # Merge back into df_ccs via combine_first using temp copies
        # to avoid destroying the DatetimeIndex with inplace set_index
        region_name = self.df_region["region"].iloc[0]

        df_forecast = self.df_region.loc[start_date:end_date].copy()
        df_forecast.index = df_forecast["datetime"].astype(str) + df_forecast["region"]

        df_ccs_tmp = self.df_ccs.copy()
        df_ccs_tmp.index = df_ccs_tmp["datetime"].astype(str) + df_ccs_tmp["region"]
        df_ccs_tmp = df_ccs_tmp.combine_first(df_forecast)

        # Restore datetime index on df_ccs
        self.df_ccs = df_ccs_tmp.set_index(
            pd.to_datetime(df_ccs_tmp["datetime"]), drop=True
        )
        self.df_ccs.index.name = None

        # Re-slice df_region from updated df_ccs
        self.df_region = self.df_ccs[self.df_ccs["region"] == region_name].copy()


def create_title_for_plot(obj):
    """
    Args:
        obj:

    Returns:

    """
    region_name = obj.region.replace("_", " ").title()
    calendar_region_name = (
        str(obj.calendar_region).replace("_", " ").title()
        if pd.notna(obj.calendar_region)
        else region_name
    )
    country_name = obj.country.replace("_", " ").title()
    crop_name = _crop_display_name(obj)

    title_line_1 = f"{region_name} ({calendar_region_name}, {country_name})"
    title_line_2 = f"{crop_name} {obj.plot_season}"

    return f"{title_line_1}\n{title_line_2}"


def _crop_display_name(obj):
    """Crop name for figure titles: metadata/crop_per_season.csv, else the long crop name."""
    long_crop_name = utils.get_crop_name(obj.crop)
    df_crop_per_season = pd.read_csv(obj.dir_metadata / "crop_per_season.csv")
    df_crop_per_season.columns = df_crop_per_season.columns.str.lower()
    # Match crop: CSV uses abbreviations (mz, sb, ww) but obj.crop may be full name
    crop_key = utils.get_crop_abbrev(obj.crop)
    crop_name = df_crop_per_season[
        (df_crop_per_season["country"] == obj.country)
        & (df_crop_per_season["crop"] == crop_key)
        & (df_crop_per_season["season"] == int(obj.growing_season))
    ]["name"].values
    return crop_name[0] if len(crop_name) > 0 else long_crop_name.replace("_", " ").title()


def _create_district_title(obj, cal_region):
    """Build plot title for a district (calendar region) plot."""
    cal_region_name = cal_region.replace("_", " ").title()
    country_name = obj.country.replace("_", " ").title()
    crop_name = _crop_display_name(obj)

    return f"{cal_region_name} ({country_name})\n{crop_name} {obj.plot_season}"


def _title_within_admin_1(obj, name, admin_1, group):
    """'<Name>, <Admin_1> (<group>)' over '<crop> <season>' (group_by_admin_1 titles)."""
    line_1 = f"{name}, {admin_1}" if admin_1 else name
    if group:
        line_1 += f" ({group})"
    return f"{line_1}\n{_crop_display_name(obj)} {obj.plot_season}"


def _lookup_state_for_region(region, region_id, boundary_gdf):
    """Return admin_1 (state) name for a county, or None if not resolvable.

    Prefers ADM_ID match; falls back to ADM2_NAME match only when unambiguous.
    """
    if boundary_gdf is None or boundary_gdf.empty:
        return None
    adm1_col = next(
        (c for c in ["ADM1_NAME", "ADMIN1", "name1"] if c in boundary_gdf.columns),
        None,
    )
    if adm1_col is None:
        return None
    if region_id is not None and "ADM_ID" in boundary_gdf.columns:
        m = boundary_gdf[boundary_gdf["ADM_ID"].astype(str) == str(region_id)]
        if not m.empty:
            return str(m[adm1_col].iloc[0])
    adm2_col = next(
        (c for c in ["ADM2_NAME", "ADMIN2"] if c in boundary_gdf.columns),
        None,
    )
    if adm2_col is None:
        return None
    m = boundary_gdf[
        boundary_gdf[adm2_col].astype(str).str.lower().str.replace("_", " ")
        == str(region).replace("_", " ").lower()
    ]
    if len(m) >= 1:
        # When multiple rows match by name (e.g. counties sharing ADM2_NAME
        # across states), pick the first deterministically and warn. Returning
        # None here would silently collapse filenames — the very collision the
        # filename_with_state feature exists to prevent.
        if len(m) > 1:
            import logging
            logging.getLogger(__name__).warning(
                f"Ambiguous county name {region!r} matches {len(m)} rows in "
                f"boundary file; picking {m[adm1_col].iloc[0]!r} for filename. "
                f"Add an id_col to geobase.txt for this shapefile to disambiguate."
            )
        return str(m[adm1_col].iloc[0])
    return None


def _build_county_fname(region, region_id, with_state, boundary_gdf):
    """Compose the per-region plot filename.

    Returns ``{region}_{state}.png`` when ``with_state`` is True and a state can
    be resolved; otherwise the legacy ``{region}.png``.
    """
    if not with_state:
        return f"{region}.png"
    state = _lookup_state_for_region(region, region_id, boundary_gdf)
    if not state:
        return f"{region}.png"
    state_slug = state.lower().replace(" ", "_")
    return f"{region}_{state_slug}.png"


def _district_columns(eo_model, available, with_forecast):
    """Columns averaged into a district plot, each listed once.

    eo_model usually already contains chirps_gefs. Appending it again for an
    in-season forecast gave the aggregate two chirps_gefs columns, the plotter
    read a 2-D forecast and dropped it, so district plots never showed the
    CHIRPS-GEFS forecast (found 2026-10-02 on the Indiana district plots).
    """
    extra = ["month", "day", "chirps_gefs", "yield"] if with_forecast else ["month", "day", "yield"]
    return [c for c in dict.fromkeys(list(eo_model or []) + extra) if c in available]


def read_district_file(path):
    """Read a region -> district table for district figures ([AGMET] district_file).

    CSV with one row per region: ``region_id`` (the boundary file's ADM_ID,
    e.g. a US county FIPS code), ``admin_1``, ``district_id`` (kept as text,
    so '0140' keeps its zero) and ``district_name``. Raises when a column is
    missing or a region is listed twice.
    """
    df = pd.read_csv(path, dtype={"district_id": str})
    missing = {"region_id", "admin_1", "district_id", "district_name"} - set(df.columns)
    if missing:
        raise ValueError(f"{path}: district file lacks columns {sorted(missing)}")
    df["region_key"] = df["region_id"].map(_id_key)
    dup = df.loc[df["region_key"].duplicated(), "region_key"].unique()
    if len(dup):
        raise ValueError(f"{path}: regions listed more than once: {list(dup)[:10]}")
    return df


def _id_key(value):
    """Region id as comparable text: 1001, 1001.0 and '1001' all give '1001'."""
    text = str(value).strip()
    try:
        number = float(text)
    except ValueError:
        return text.lower()
    return str(int(number)) if number.is_integer() else text


def _slug(text):
    """File-name part: lower case, '.' and "'" dropped, other runs of characters
    outside a-z, 0-9 and '-' turned into one '_' (st_clair, miami-dade)."""
    text = str(text).strip().lower().replace(".", "").replace("'", "")
    return re.sub(r"[^a-z0-9-]+", "_", text).strip("_")


def _format_id(region_id, width):
    """Region id for a file name; whole numbers are zero-padded to ``width``."""
    text = str(region_id).strip()
    try:
        number = float(text)
    except ValueError:
        return text
    if not number.is_integer():
        return text
    text = str(int(number))
    return text.zfill(width) if width else text


def _unit_name(region, region_id, admin_1, boundary_gdf):
    """Name of an admin_2 unit without its admin_1 prefix.

    Taken from the boundary file's ADM2_NAME (matched on ADM_ID), else from the
    region name. usa_counties_fips stores 'minnesota kandiyohi', so the state
    prefix is dropped.
    """
    name = None
    if boundary_gdf is not None and region_id is not None and "ADM_ID" in boundary_gdf.columns:
        adm2_col = next((c for c in ["ADM2_NAME", "ADMIN2"] if c in boundary_gdf.columns), None)
        if adm2_col:
            m = boundary_gdf[boundary_gdf["ADM_ID"].astype(str) == str(region_id)]
            if not m.empty:
                name = str(m[adm2_col].iloc[0])
    name = (name or str(region)).replace("_", " ").strip()
    if admin_1 and name.lower().startswith(admin_1.lower() + " "):
        name = name[len(admin_1) + 1:]
    return name


def _group_name(obj, region_id):
    """District of a region from district_file, else its calendar region, else None."""
    if obj.district_table is not None:
        row = obj.district_table[obj.district_table["region_key"] == _id_key(region_id)]
        if not row.empty:
            return str(row["district_name"].iloc[0])
    if pd.notna(obj.calendar_region):
        return str(obj.calendar_region).replace("_", " ").title()
    return None


def _admin1_gdf(boundary_gdf, admin_1, cache):
    """Units of one admin_1 (e.g. a state's counties) for the locator map, or None."""
    if boundary_gdf is None or not admin_1:
        return None
    key = str(admin_1).lower()
    if key not in cache:
        adm1_col = next(
            (c for c in ["ADM1_NAME", "ADMIN1", "name1"] if c in boundary_gdf.columns), None
        )
        sub = (
            boundary_gdf[boundary_gdf[adm1_col].astype(str).str.lower() == key]
            if adm1_col else None
        )
        cache[key] = sub if sub is not None and not sub.empty else None
    return cache[key]


def _region_figure_spec(obj, boundary_gdf, admin1_cache):
    """Folder, file name, title, locator boundary and outline flag of a region figure.

    Default: <region_folder or adm<N>>/<region>.png (or _build_county_fname's
    name), the legacy title and the whole country as locator. With
    group_by_admin_1: <folder>/<admin_1>/<id>_<name>.png, titled
    "<Name>, <Admin_1> (<district>)", with the admin_1 unit as locator.
    """
    folder = obj.dir_agmet / (obj.region_folder or obj.scale_short)
    if not obj.group_by_admin_1:
        fname = _build_county_fname(
            obj.region, obj.region_id, obj.filename_with_state, boundary_gdf
        )
        return folder, fname, create_title_for_plot(obj), boundary_gdf, False

    admin_1 = _lookup_state_for_region(obj.region, obj.region_id, boundary_gdf)
    name = _unit_name(obj.region, obj.region_id, admin_1, boundary_gdf)
    fname = f"{_format_id(obj.region_id, obj.id_width)}_{_slug(name)}.png"
    sup_title = _title_within_admin_1(obj, name.title(), admin_1, _group_name(obj, obj.region_id))
    locator = _admin1_gdf(boundary_gdf, admin_1, admin1_cache)
    if locator is None:
        return folder, fname, sup_title, boundary_gdf, False
    return folder / _slug(admin_1), fname, sup_title, locator, True


def _aggregate_district(obj, df_district, key):
    """Daily mean over a district's regions, as the district figure plots it.

    ``key`` is the column naming the district (calendar_region, district_id).
    Returns None when the groupby fails, so the caller skips the district.
    """
    with_forecast = False
    if "chirps" in df_district.columns:
        try:
            bool_year_check, bool_date_check = obj.check_date(
                df_district, obj.plot_season
            )
        except Exception:
            bool_year_check, bool_date_check = False, False
        with_forecast = bool_date_check and bool_year_check
    columns = _district_columns(obj.eo_model, df_district.columns, with_forecast)

    try:
        df_agg = (
            df_district.groupby(
                ["country", key, "harvest_season", "doy", "datetime"]
            )[columns]
            .mean()
            .reset_index()
        )
    except Exception:
        return None

    if "chirts_era5_tmax" in df_agg.columns and "chirts_era5_tmin" in df_agg.columns:
        df_agg.loc[:, "average_temperature"] = (
            df_agg["chirts_era5_tmax"] + df_agg["chirts_era5_tmin"]
        ) / 2.0
    elif "daymet_tmax" in df_agg.columns and "daymet_tmin" in df_agg.columns:
        df_agg.loc[:, "average_temperature"] = (
            df_agg["daymet_tmax"] + df_agg["daymet_tmin"]
        ) / 2.0
    else:
        df_agg.loc[:, "average_temperature"] = (
            df_agg["cpc_tmax"] + df_agg["cpc_tmin"]
        ) / 2.0
    df_agg.set_index(
        pd.DatetimeIndex(df_agg["datetime"]), inplace=True, drop=True
    )
    df_agg.index.name = None
    df_agg.sort_values(by="datetime", inplace=True)
    return df_agg


def _district_share(df_district):
    """Sum of the production shares of a district's regions, or None."""
    if "production_share_pct" in df_district.columns:
        region_shares = (
            df_district.groupby("region")["production_share_pct"]
            .first()
            .dropna()
        )
        if not region_shares.empty:
            return region_shares.sum()
    return None


def _district_figure_spec(obj, district_id, region_ids, boundary_gdf, admin1_cache):
    """Folder, file name, title, locator, outline flag and highlight of a
    district_file figure: <district_folder>[/<admin_1>]/<district_id>_<name>.png."""
    info = obj.district_table[obj.district_table["district_id"] == district_id].iloc[0]
    name, admin_1 = str(info["district_name"]), str(info["admin_1"])
    folder = obj.dir_agmet / obj.district_folder
    fname = f"{district_id}_{_slug(name)}.png"

    highlight_gdf = None
    if boundary_gdf is not None and "ADM_ID" in boundary_gdf.columns:
        keys = {_id_key(r) for r in region_ids}
        members = boundary_gdf[boundary_gdf["ADM_ID"].map(_id_key).isin(keys)]
        if not members.empty:
            highlight_gdf = members.dissolve()

    if not obj.group_by_admin_1:
        return (folder, fname, _create_district_title(obj, name), boundary_gdf, False,
                highlight_gdf)
    sup_title = _title_within_admin_1(obj, name, admin_1, None)
    locator = _admin1_gdf(boundary_gdf, admin_1, admin1_cache)
    if locator is None:
        return folder, fname, sup_title, boundary_gdf, False, highlight_gdf
    return folder / _slug(admin_1), fname, sup_title, locator, True, highlight_gdf


def _plot_table_districts(obj, plot_season, boundary_gdf, admin1_cache):
    """Loop 2 with a district_file: one figure per district with regions in this run."""
    table = obj.district_table.set_index("region_key")
    district_regions = {}
    for region_id in obj.df_ccs["region_id"].dropna().unique():
        key = _id_key(region_id)
        if key in table.index:
            district_regions.setdefault(table.at[key, "district_id"], []).append(region_id)

    for district_id in sorted(district_regions):
        region_ids = district_regions[district_id]
        df_district = obj.df_ccs[obj.df_ccs["region_id"].isin(region_ids)].copy()
        df_district.index = pd.to_datetime(df_district.index)

        # All regions of a district share its crop calendar; take the first
        obj.setup_region(df_district["region"].iloc[0], plot_season, "region")
        if pd.isna(obj.date_planting):
            obj.logger.warning(f"Skipping plot for district {district_id} — no crop calendar data")
            continue

        dates_calendar = [
            obj.date_planting,
            obj.date_greenup,
            obj.date_senescence,
            obj.date_harvesting,
        ]
        df_agg = _aggregate_district(
            obj, df_district.assign(district_id=district_id), "district_id"
        )
        if df_agg is None or df_agg.empty:
            continue

        folder, fname, sup_title, locator, outlines, highlight_gdf = _district_figure_spec(
            obj, district_id, region_ids, boundary_gdf, admin1_cache
        )
        plot.AgmetPlotter(
            df_agg,
            obj.eo_plot,
            closest=obj.closest,
            dates_cal=dates_calendar,
            frcast_yr=obj.plot_season,
            logos=obj.logos_for_country(obj.country),
            dir_out=folder,
            sup_title=sup_title,
            fname=fname,
            production_pct=_district_share(df_district),
            country=obj.country,
            region=str(district_id),
            boundary_gdf=locator,
            highlight_gdf=highlight_gdf,
            admin_level=obj.scale,
            show_logos=obj.show_logos,
            logo_max_px=obj.logo_max_px,
            yield_units=obj.yield_units,
            inset_outlines=outlines,
        ).plot()


def _process_combination(obj, country, scale, crop, growing_season):
    """Process a single (country, scale, crop, growing_season) combination.

    Handles setup, season loop, region loop, and all plotting.
    """
    try:
        obj.setup_country(country, scale, crop, growing_season)
    except FileNotFoundError as e:
        tqdm.write(f"  Skipping {country} {crop} s{growing_season}: {e}")
        return

    # Read boundary shapefile ONCE, filter to current country
    boundary_gdf = None
    region_gdf = None
    try:
        import geopandas as gpd
        country_norm = obj.country.replace("_", " ").lower()

        boundary_path = obj.dir_boundary_files / obj.parser.get(obj.country, "boundary_file")
        if boundary_path.exists():
            # Shared loader: applies config-driven rename (FIPS→ADM_ID etc.),
            # Tanzania short-name fix, drops would-be-duplicate columns.
            from geocif.utils import load_country_boundary_gdf
            gdf = load_country_boundary_gdf(obj.parser, boundary_path)
            adm0_col = next((c for c in ["ADM0_NAME", "ADMIN0", "name0"] if c in gdf.columns), None)
            if adm0_col:
                mask = gdf[adm0_col].str.lower().str.replace("_", " ") == country_norm
                boundary_gdf = gdf[mask].copy()

                # Exclude non-contiguous territories for U.S. (Alaska, Hawaii)
                if country_norm == "united states of america":
                    adm1_col = next(
                        (c for c in ["ADM1_NAME", "ADMIN1", "name1"] if c in boundary_gdf.columns),
                        None,
                    )
                    if adm1_col:
                        boundary_gdf = boundary_gdf[
                            ~boundary_gdf[adm1_col].str.lower().isin(["alaska", "hawaii"])
                        ]

                # Clip antimeridian wraparound (e.g., Russia/USA spanning dateline)
                b = boundary_gdf.total_bounds
                if b[2] - b[0] > 300:
                    from shapely.geometry import box
                    cx = boundary_gdf.geometry.centroid.x
                    if (cx >= 0).sum() > (cx < 0).sum():
                        clip_box = box(0, b[1], 180, b[3])
                    else:
                        clip_box = box(-180, b[1], 0, b[3])
                    boundary_gdf = gpd.clip(boundary_gdf, clip_box)

        # Read calendar-region shapefile for district highlighting
        region_path = obj.dir_boundary_files / obj.parser.get(obj.country, "shp_region")
        if region_path.exists():
            rgdf = gpd.read_file(region_path, engine="pyogrio")
            radm0 = next((c for c in ["ADM0_NAME", "ADMIN0", "name0"] if c in rgdf.columns), None)
            if radm0:
                rmask = rgdf[radm0].str.lower().str.replace("_", " ") == country_norm
                region_gdf = rgdf[rmask].copy()
    except Exception:
        pass

    admin1_cache = {}  # admin_1 name -> its units, for group_by_admin_1 locator maps
    for plot_season in obj.plot_seasons:
        obj.get_closest_season(plot_season)

        ###############################################################
        # Loop 1: Admin-level plots (one per region)
        ###############################################################
        # Iterate by (region, region_id) so counties that share a name across
        # states (e.g. Kiowa in CO/KS/OK) get one plot per FIPS, not merged.
        region_pairs = (
            obj.df_ccs[["region", "region_id"]]
            .drop_duplicates()
            .itertuples(index=False, name=None)
        )
        for region, region_id in region_pairs:
            obj.setup_region(region, plot_season, "region")
            # Narrow further by region_id (df_region currently holds all
            # rows for the name, which is wrong when names collide).
            obj.df_region = obj.df_region[
                obj.df_region["region_id"] == region_id
            ].copy()
            obj.region_id = region_id

            # Skip regions with no crop calendar data
            if pd.isna(obj.date_planting):
                obj.logger.warning(f"Skipping plot for {region} — no crop calendar data")
                continue

            if obj.precip_var == "chirps":
                obj.add_precip_forecast(plot_season)

            dates_calendar = [
                obj.date_planting,
                obj.date_greenup,
                obj.date_senescence,
                obj.date_harvesting,
            ]

            # Extract production share for this region
            region_pct = None
            if "production_share_pct" in obj.df_region.columns:
                vals = obj.df_region["production_share_pct"].dropna()
                if not vals.empty:
                    region_pct = vals.iloc[0]

            folder, fname, sup_title, locator, outlines = _region_figure_spec(
                obj, boundary_gdf, admin1_cache
            )

            plot.AgmetPlotter(
                obj.df_region,
                obj.eo_plot,
                closest=obj.closest,
                dates_cal=dates_calendar,
                frcast_yr=obj.plot_season,
                logos=obj.logos_for_country(obj.country),
                dir_out=folder,
                sup_title=sup_title,
                fname=fname,
                production_pct=region_pct,
                country=obj.country,
                region=obj.region,
                region_id=obj.region_id,
                boundary_gdf=locator,
                admin_level=obj.scale,
                show_logos=obj.show_logos,
                logo_max_px=obj.logo_max_px,
                yield_units=obj.yield_units,
                inset_outlines=outlines,
            ).plot()

        ###############################################################
        # Loop 2: District plots (one per calendar region, aggregated;
        # one per district of [AGMET] district_file when it is set)
        ###############################################################
        if obj.district_table is not None:
            _plot_table_districts(obj, plot_season, boundary_gdf, admin1_cache)
            continue

        for cal_region in obj.list_calendar_regions:
            if pd.isna(cal_region):
                continue

            # Filter full df_ccs to all regions in this calendar region
            df_district = obj.df_ccs[obj.df_ccs["calendar_region"] == cal_region].copy()
            df_district.index = pd.to_datetime(df_district.index)

            # Use first region in this calendar region for crop calendar dates
            first_region = df_district["region"].iloc[0]
            obj.setup_region(first_region, plot_season, "region")

            # Skip calendar regions with no crop calendar data
            if pd.isna(obj.date_planting):
                obj.logger.warning(f"Skipping plot for calendar region {cal_region} — no crop calendar data")
                continue

            dates_calendar = [
                obj.date_planting,
                obj.date_greenup,
                obj.date_senescence,
                obj.date_harvesting,
            ]

            df_agg = _aggregate_district(obj, df_district, "calendar_region")
            if df_agg is None:
                continue

            sup_title = _create_district_title(obj, cal_region)

            # Sum production shares of all regions in this district
            district_pct = _district_share(df_district)

            if not df_agg.empty:
                # Extract calendar-region geometry for district highlighting
                highlight_gdf = None
                if region_gdf is not None:
                    rname_col = next(
                        (c for c in ["Name", "name", "NAME"] if c in region_gdf.columns), None
                    )
                    if rname_col:
                        cal_norm = cal_region.replace("_", " ").lower()
                        hmask = region_gdf[rname_col].str.lower().str.replace("_", " ") == cal_norm
                        highlight_gdf = region_gdf[hmask]

                plot.AgmetPlotter(
                    df_agg,
                    obj.eo_plot,
                    closest=obj.closest,
                    dates_cal=dates_calendar,
                    frcast_yr=obj.plot_season,
                    logos=obj.logos_for_country(obj.country),
                    dir_out=obj.dir_agmet / obj.district_folder,
                    sup_title=sup_title,
                    fname=f"{cal_region}.png",
                    production_pct=district_pct,
                    country=obj.country,
                    region=cal_region,
                    boundary_gdf=boundary_gdf,
                    highlight_gdf=highlight_gdf,
                    admin_level=obj.scale,
                    show_logos=obj.show_logos,
                    logo_max_px=obj.logo_max_px,
                    yield_units=obj.yield_units,
                ).plot()


def _agmet_worker(args):
    """Top-level worker for parallel agmet execution.

    Each worker creates its own AgmetGeo from config files — fully independent,
    no shared state. Required as a top-level function for multiprocessing pickle.
    """
    path_config_file, country, scale, crop, growing_season = args
    obj = AgmetGeo(path_config_file)
    obj.read_statistics(read_countries=True)
    _process_combination(obj, country, scale, crop, growing_season)


_COUNTRIES_AMIS_TO_EWCM = [
    "vietnam", "thailand", "south_africa", "indonesia",
    "kazakhstan", "philippines",
]


def _finalize_plots(plots_root):
    """Cross-copy EWCM/AMIS country folders and create ZIP archives.

    1. Copy EWCM/egypt → AMIS/egypt
    2. Copy AMIS/{country} → EWCM/{country} for selected countries
    3. Zip AMIS/ and EWCM/ into the parent date directory
    """
    tz = ZoneInfo("America/New_York")
    today = datetime.now(tz).date()

    # Find today's or yesterday's plots directory
    plots_dir = None
    for offset in (0, 1):
        candidate = plots_root / (today - timedelta(days=offset)).strftime("%B_%d_%Y") / "plots"
        if candidate.exists():
            plots_dir = candidate
            break

    if plots_dir is None:
        return

    date_dir = plots_dir.parent
    amis_dir = plots_dir / "AMIS"
    ewcm_dir = plots_dir / "EWCM"

    # 1. Copy egypt EWCM → AMIS
    src_egypt = ewcm_dir / "egypt"
    if src_egypt.exists():
        shutil.copytree(src_egypt, amis_dir / "egypt", dirs_exist_ok=True)

    # 2. Copy selected countries AMIS → EWCM
    if amis_dir.exists():
        for country in _COUNTRIES_AMIS_TO_EWCM:
            src = amis_dir / country
            if src.exists():
                shutil.copytree(src, ewcm_dir / country, dirs_exist_ok=True)

    # 3. Zip the final directories
    for folder in (amis_dir, ewcm_dir):
        if not folder.exists():
            continue
        zip_path = date_dir / f"{folder.name}.zip"
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in folder.rglob("*"):
                zf.write(f, f.relative_to(folder))


def loop_agmet(path_config_file=None):
    """
    Args:
    """
    # Create geo object
    obj = AgmetGeo(path_config_file)

    from geocif.data import ensure_metadata
    ensure_metadata(obj.parser)

    # Read in data on crop names in each country
    obj.read_statistics(read_countries=True)

    # Create combinations of run parameters
    all_combinations = obj.create_run_combinations()

    # Build and display run summary
    country_combos = {}
    for country, scale, crop, growing_season in all_combinations:
        country_combos.setdefault(country, []).append(
            f"{crop}, {scale}, s{growing_season}"
        )

    params = [("Countries", obj.countries)]
    for country, combos in country_combos.items():
        params.append((f"  {country}", "; ".join(dict.fromkeys(combos))))
    params.append(("Plot seasons", [str(s) for s in (obj.plot_seasons or [])]))
    params.append(("EO plot vars", obj.eo_plot))
    params.append(("EO model vars", obj.eo_model))
    params.append(("Total combinations", str(len(all_combinations))))

    do_parallel = (
        obj.parser.getboolean("DEFAULT", "do_parallel_agmet")
        if obj.parser.has_option("DEFAULT", "do_parallel_agmet")
        else False
    )
    params.append(("Parallel", str(do_parallel)))
    if do_parallel:
        fraction_cpus = obj.parser.getfloat("DEFAULT", "fraction_cpus")
        cpu_count = int(mp.cpu_count() * fraction_cpus)
        # Cap concurrent workers. Each combo loads a full boundary GeoDataFrame
        # + multi-year condition data and copies frames per region, so 64+
        # workers OOM-kill on large admin_2 countries (France etc.). A killed
        # worker made the old imap_unordered hang the whole run for hours.
        # Override via [DEFAULT] agmet_max_workers (default 16).
        cpu_count = max(1, min(
            cpu_count,
            obj.parser.getint("DEFAULT", "agmet_max_workers", fallback=16),
        ))
        params.append(("CPUs", str(cpu_count)))

    ut.display_run_summary("GeoCIF Agmet Runner", params, wait=20)

    if do_parallel:
        work_items = [
            (path_config_file, country, scale, crop, gs)
            for country, scale, crop, gs in all_combinations
        ]
        # Consume results with a per-result timeout so a worker that dies
        # (OOM/segfault) can NOT hang the whole run. imap_unordered loses a
        # dead worker's task result; a plain list() then blocks on it forever
        # (the 15h-hang bug). A TimeoutError means no worker produced a result
        # within the window, so the remaining results are lost and we stop
        # waiting. Override via [DEFAULT] agmet_task_timeout (seconds).
        task_timeout = obj.parser.getint("DEFAULT", "agmet_task_timeout", fallback=1800)
        n_items = len(work_items)
        done = 0
        with mp.Pool(cpu_count) as pool:
            result_iter = pool.imap_unordered(_agmet_worker, work_items)
            with tqdm(total=n_items, desc="Agmet (parallel)") as pbar:
                for _ in range(n_items):
                    try:
                        result_iter.next(timeout=task_timeout)
                        done += 1
                    except mp.TimeoutError:
                        obj.logger.error(
                            f"Agmet: no worker result within {task_timeout}s "
                            f"(a worker likely died/hung); {n_items - done} "
                            f"combo(s) unfinished — stopping the wait."
                        )
                        break
                    finally:
                        pbar.update(1)
        obj.logger.info(f"Agmet parallel plotting: {done}/{n_items} combos completed")
    else:
        pbar = tqdm(all_combinations, total=len(all_combinations))
        for country, scale, crop, growing_season in pbar:
            pbar.set_description(f"{country} ({crop} s{growing_season})")
            _process_combination(obj, country, scale, crop, growing_season)

    # Clean up empty output directories
    plots_root = obj.dir_output / "crop_condition"
    if plots_root.exists():
        for dirpath, dirnames, filenames in os.walk(str(plots_root), topdown=False):
            if not filenames and not os.listdir(dirpath):
                os.rmdir(dirpath)

    # Finalize: cross-copy EWCM/AMIS countries and create ZIP archives
    _finalize_plots(plots_root)


def run(path_config_files=[]):
    loop_agmet(path_config_files)


if __name__ == "__main__":
    run()
