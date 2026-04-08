import ast
import os
import shutil
import zipfile
import multiprocessing as mp
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import arrow as ar
import numpy as np
import pandas as pd
from heapq import nsmallest
from tqdm import tqdm

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
            ["ndvi", "cpc_tmax", "cpc_tmin", "chirps", "esi_4wk", "soil_moisture_as1", "soil_moisture_as2"],
        )
        self.eo_plot = self._expand_eo_plot(eo_plot_raw)
        self.eo_model = self._get_option(
            "eo_model",
            ["ndvi", "cpc_tmax", "cpc_tmin", "chirps", "esi_4wk", "soil_moisture_as1", "soil_moisture_as2"],
        )
        self.logo_harvest = self.dir_metadata / "images" / self.parser.get(
            "AGMET", "logo_harvest"
        )
        self.logo_geoglam = self.dir_metadata / "images" / self.parser.get(
            "AGMET", "logo_geoglam"
        )

    @staticmethod
    def _expand_eo_plot(eo_plot_raw):
        """Map raw EO variable names to subplot names in GEOGLAM display order.

        Layout (3 columns):
            Row 0: ndvi            | cumulative_precip | <soil/other>
            Row 1: yearly_ndvi     | daily_precip      | <soil/other>
            Row 2: esi_4wk         | cpc_tmax          | ...
        """
        # Desired order of subplot names matching GEOGLAM layout
        ordered = [
            "ndvi", "cumulative_precip", "nsidc_surface",
            "yearly_ndvi", "daily_precip", "nsidc_rootzone",
            "esi_4wk", "cpc_tmax", "daymet_tmax",
        ]

        # Which raw vars expand into which subplot names
        expansions = {
            "ndvi": ["ndvi", "yearly_ndvi"],
            "chirps": ["cumulative_precip", "daily_precip"],
            "daymet_prcp": ["cumulative_precip", "daily_precip"],
            "gcvi": ["gcvi", "yearly_gcvi"],
        }
        # These raw vars get dropped (absorbed into the avg temp plot)
        skip = {"cpc_tmin", "daymet_tmin"}

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
        return result + extras

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
        self.category = self.parser.get(country, "category")
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
            seasons = ast.literal_eval(
                self.parser.get(country, "seasons")
            )

            for crop in crops:
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
    long_crop_name = utils.get_crop_name(obj.crop)

    # Get name of crop based on metadata/crop_per_season.csv file
    df_crop_per_season = pd.read_csv(obj.dir_metadata / "crop_per_season.csv")
    df_crop_per_season.columns = df_crop_per_season.columns.str.lower()
    # Match crop: CSV uses abbreviations (mz, sb, ww) but obj.crop may be full name
    crop_key = utils.get_crop_abbrev(obj.crop)
    crop_name = df_crop_per_season[
        (df_crop_per_season["country"] == obj.country)
        & (df_crop_per_season["crop"] == crop_key)
        & (df_crop_per_season["season"] == int(obj.growing_season))
    ]["name"].values

    crop_name = crop_name[0] if len(crop_name) > 0 else long_crop_name.replace("_", " ").title()

    title_line_1 = f"{region_name} ({calendar_region_name}, {country_name})"
    title_line_2 = f"{crop_name} {obj.plot_season}"

    return f"{title_line_1}\n{title_line_2}"


def _create_district_title(obj, cal_region):
    """Build plot title for a district (calendar region) plot."""
    cal_region_name = cal_region.replace("_", " ").title()
    country_name = obj.country.replace("_", " ").title()
    long_crop_name = utils.get_crop_name(obj.crop)

    df_crop_per_season = pd.read_csv(obj.dir_metadata / "crop_per_season.csv")
    df_crop_per_season.columns = df_crop_per_season.columns.str.lower()
    crop_key = utils.get_crop_abbrev(obj.crop)
    crop_name = df_crop_per_season[
        (df_crop_per_season["country"] == obj.country)
        & (df_crop_per_season["crop"] == crop_key)
        & (df_crop_per_season["season"] == int(obj.growing_season))
    ]["name"].values
    crop_name = crop_name[0] if len(crop_name) > 0 else long_crop_name.replace("_", " ").title()

    return f"{cal_region_name} ({country_name})\n{crop_name} {obj.plot_season}"


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
            gdf = gpd.read_file(boundary_path, engine="pyogrio")
            adm0_col = next((c for c in ["ADM0_NAME", "ADMIN0", "name0"] if c in gdf.columns), None)
            if adm0_col:
                mask = gdf[adm0_col].str.lower().str.replace("_", " ") == country_norm
                boundary_gdf = gdf[mask].copy()
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

    for plot_season in obj.plot_seasons:
        obj.get_closest_season(plot_season)

        ###############################################################
        # Loop 1: Admin-level plots (one per region)
        ###############################################################
        for region in obj.list_regions:
            obj.setup_region(region, plot_season, "region")

            if obj.precip_var == "chirps":
                obj.add_precip_forecast(plot_season)

            dates_calendar = [
                obj.date_planting,
                obj.date_greenup,
                obj.date_senescence,
                obj.date_harvesting,
            ]

            sup_title = create_title_for_plot(obj)

            # Extract production share for this region
            region_pct = None
            if "production_share_pct" in obj.df_region.columns:
                vals = obj.df_region["production_share_pct"].dropna()
                if not vals.empty:
                    region_pct = vals.iloc[0]

            plot.AgmetPlotter(
                obj.df_region,
                obj.eo_plot,
                closest=obj.closest,
                dates_cal=dates_calendar,
                frcast_yr=obj.plot_season,
                logos=[obj.logo_harvest, obj.logo_geoglam],
                dir_out=obj.dir_agmet / obj.scale_short,
                sup_title=sup_title,
                fname=f"{obj.region}.png",
                production_pct=region_pct,
                country=obj.country,
                region=obj.region,
                boundary_gdf=boundary_gdf,
                admin_level=obj.scale,
            ).plot()

        ###############################################################
        # Loop 2: District plots (one per calendar region, aggregated)
        ###############################################################
        for cal_region in obj.list_calendar_regions:
            if pd.isna(cal_region):
                continue

            # Filter full df_ccs to all regions in this calendar region
            df_district = obj.df_ccs[obj.df_ccs["calendar_region"] == cal_region].copy()
            df_district.index = pd.to_datetime(df_district.index)

            # Use first region in this calendar region for crop calendar dates
            first_region = df_district["region"].iloc[0]
            obj.setup_region(first_region, plot_season, "region")
            dates_calendar = [
                obj.date_planting,
                obj.date_greenup,
                obj.date_senescence,
                obj.date_harvesting,
            ]

            # Build column list for aggregation
            columns = [c for c in (obj.eo_model or []) + ["month", "day", "yield"]
                       if c in df_district.columns]
            if "chirps" in df_district.columns:
                try:
                    bool_year_check, bool_date_check = obj.check_date(
                        df_district, obj.plot_season
                    )
                except Exception:
                    bool_year_check, bool_date_check = False, False

                if bool_date_check and bool_year_check:
                    columns = [c for c in (obj.eo_model or []) + [
                        "month", "day", "chirps_gefs", "yield",
                    ] if c in df_district.columns]

            try:
                df_agg = (
                    df_district.groupby(
                        ["country", "calendar_region", "harvest_season", "doy", "datetime"]
                    )[columns]
                    .mean()
                    .reset_index()
                )
            except Exception:
                continue

            if "daymet_tmax" in df_agg.columns and "daymet_tmin" in df_agg.columns:
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

            sup_title = _create_district_title(obj, cal_region)

            # Sum production shares of all regions in this district
            district_pct = None
            if "production_share_pct" in df_district.columns:
                region_shares = (
                    df_district.groupby("region")["production_share_pct"]
                    .first()
                    .dropna()
                )
                if not region_shares.empty:
                    district_pct = region_shares.sum()

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
                    logos=[obj.logo_harvest, obj.logo_geoglam],
                    dir_out=obj.dir_agmet / "district",
                    sup_title=sup_title,
                    fname=f"{cal_region}.png",
                    production_pct=district_pct,
                    country=obj.country,
                    region=cal_region,
                    boundary_gdf=boundary_gdf,
                    highlight_gdf=highlight_gdf,
                    admin_level=obj.scale,
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
        params.append(("CPUs", str(cpu_count)))

    ut.display_run_summary("GeoCIF Agmet Runner", params, wait=20)

    if do_parallel:
        work_items = [
            (path_config_file, country, scale, crop, gs)
            for country, scale, crop, gs in all_combinations
        ]
        with mp.Pool(cpu_count) as pool:
            list(tqdm(
                pool.imap_unordered(_agmet_worker, work_items),
                total=len(work_items),
                desc="Agmet (parallel)",
            ))
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
