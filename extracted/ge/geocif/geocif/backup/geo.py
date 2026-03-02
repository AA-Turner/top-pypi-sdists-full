import os
import ast
import itertools
import math

import arrow as ar
import numpy as np
import pandas as pd
import neptune
from pathlib import Path

from geoprepare import base, log


class geo(base.BaseGeo):
    def __init__(self, path_config_file):
        super().__init__(path_config_file)

        # Parse configuration files
        self.parse_config()

    def parse_config(self, section="DEFAULT"):
        """

        Args:
            section ():

        Returns:

        """
        super().parse_config(section="DEFAULT")

        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.forecast_seasons = ast.literal_eval(
            self.parser.get("DEFAULT", "forecast_seasons")
        )
        self.plot_seasons = ast.literal_eval(self.parser.get("DEFAULT", "plot_seasons"))
        self.models = ast.literal_eval(self.parser.get("DEFAULT", "models"))
        self.eo_plot = ast.literal_eval(self.parser.get("DEFAULT", "eo_plot"))
        self.eo_model = ast.literal_eval(self.parser.get("DEFAULT", "eo_model"))
        self.logo_harvest = self.dir_metadata / self.parser.get(
            "METADATA", "logo_harvest"
        )
        self.logo_geoglam = self.dir_metadata / self.parser.get(
            "METADATA", "logo_geoglam"
        )

        # self.lag_area_as_feature = self.parser.getboolean('DEFAULT', 'lag_area_as_feature')
        # self.location_as_feature = self.parser.getboolean('DEFAULT', 'location_as_feature')

        # MLOPS
        self.neptune_username = self.parser.get("MLOPS", "neptune_username")
        self.neptune_project = self.parser.get("MLOPS", "neptune_project")

        # Setup experiment logging, check results at https://app.neptune.ai/
        self.tracker = neptune.init_run(
            project=f"{self.neptune_username}/{self.neptune_project}",
            capture_hardware_metrics=False,
            source_files=[],
            capture_stderr=False,
        )

    def get_calendar_region_for_region(self, df, region):
        """

        Args:
            df ():
            region ():

        Returns:

        """
        calendar_region = df[df["region"] == region]["calendar_region"].values[0]

        return calendar_region

    def setup_country(self, country, scale, crop, growing_season):
        self.country = country
        self.scale = scale
        self.crop = crop
        self.growing_season = growing_season
        self.category = self.parser.get(country, "category")
        self.use_cropland_mask = self.parser.getboolean(country, "USE_CROPLAND_MASK")

        self.get_dirname(country)
        self.get_ccs_dataframe(country, scale, crop, growing_season)

        # Get list of regions in ccs dataframe
        self.list_regions = self.df_ccs["region"].unique()

        # Get list of calendar regions in ccs dataframe
        self.list_calendar_regions = self.df_ccs["calendar_region"].unique()

        self.precip_var = (
            "chirps" if "chirps" in self.df_ccs.columns.values else "cpc_precip"
        )

        # Append current date to the output directory
        self.dir_output = self.dir_output / ar.now().format("MMMM_DD_YYYY")

    def setup_region(self, region, plot_season, type_region="region"):
        self.region = region
        self.calendar_region = self.get_calendar_region_for_region(self.df_ccs, region)
        self.plot_season = plot_season
        self.type_region = type_region

        # get ccs dataframe for region/calendar_region
        if type_region == "region":
            self.df_region = self.df_ccs[self.df_ccs["region"] == region]
        elif type_region == "calendar_region":
            self.df_region = self.df_ccs[
                self.df_ccs["calendar_region"] == self.calendar_region
            ]
        elif type_region == "region_year":
            self.df_region = self.df_ccs[
                (self.df_ccs["region"] == region) & (self.df_ccs["year"] == plot_season)
            ]
        elif type_region == "calendar_region_year":
            self.df_region = self.df_ccs[
                (self.df_ccs["calendar_region"] == self.calendar_region)
                & (self.df_ccs["year"] == plot_season)
            ]
        else:
            raise ValueError(f"Unknown type_region: {type_region}")

        # convert df_region index to datetime
        self.df_region.index = pd.to_datetime(self.df_region.index)

        # Setup output directory for agmet graphics
        # Create output directory
        folder = f"{self.crop}_s{self.growing_season}_{self.plot_season}"
        self.dir_agmet = (
            self.dir_output
            / "crop_condition"
            / self.category
            / self.country
            / folder
            / "condition"
        )
        # dir_output = self.dir_output / 'crop_condition' / self.category / self.country / folder

        # Get phenological transition dates from crop calendar
        (
            self.date_planting,
            self.date_greenup,
            self.date_senescence,
            self.date_harvesting,
        ) = self.get_calendar(self.region, self.plot_season)

    def create_run_combinations(self):
        """
        Create combinations of run parameters.
        Returns:
        """
        all_combinations = []

        for country in self.countries:
            scales = ast.literal_eval(self.parser.get(country, "scales"))
            crops = ast.literal_eval(self.parser.get(country, "crops"))
            growing_seasons = ast.literal_eval(
                self.parser.get(country, "growing_seasons")
            )

            for scale in scales:
                for crop in crops:
                    for growing_season in growing_seasons:
                        all_combinations.extend(
                            list(
                                itertools.product(
                                    [country], [scale], [crop], [growing_season]
                                )
                            )
                        )

        return all_combinations

    def get_calendar(self, region, forecast_season):
        """
        Get calendar information for region
        Args:
            region:

        Returns:

        """
        SEASON = "harvest_season"
        CAL = "crop_calendar"

        df_sub = self.df_ccs[
            self.df_ccs["region"] == region
        ]  # region specific data frame
        df_sub.index = pd.to_datetime(df_sub.index)
        sr_cal = df_sub[df_sub[SEASON] == forecast_season][
            ["doy", CAL]
        ]  # Pandas series with calendar info

        # Change calendar column to int if it is not
        sr_cal[CAL] = pd.to_numeric(sr_cal[CAL], errors="coerce")

        # Get the crop calendar dates
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
        # Read in ccs file using geomerge object
        dir_ccs = self.dir_inputs / self.dir_threshold / country / scale

        self.df_ccs = pd.read_csv(
            dir_ccs / f"{crop}_s{growing_season}.csv", index_col=0
        )

        # convert index to datetime column with type datetime
        self.df_ccs["datetime"] = pd.to_datetime(self.df_ccs.index)
        self.df_ccs.index.name = None

    def get_closest_season(self, season):
        from heapq import nsmallest

        self.closest = nsmallest(
            5 + 1, range(2001, ar.utcnow().year), key=lambda x: abs(x - season)
        )

        if season in self.closest:
            self.closest.remove(season)

    def check_date(self, df, plot_season):
        # Check if the last date in the CHIRPS-GEFS data is within the growing season
        last_valid_date = pd.to_datetime(df["chirps"].last_valid_index()).date()

        bool_year_check = ar.utcnow().year <= plot_season
        bool_date_check = (last_valid_date > self.date_planting.date()) & (
            last_valid_date < self.date_harvesting.date()
        )

        return bool_year_check, bool_date_check

    def add_precip_forecast(self, plot_season):
        bool_year_check, bool_date_check = self.check_date(self.df_ccs, plot_season)

        if bool_year_check & bool_date_check:
            # Get CHIRPS-GEFS data for region
            base_dir = self.dir_inputs / self.dir_threshold / self.country / self.scale
            path_gefs = (
                base_dir / "cr" / "chirps_gefs"
                if self.use_cropland_mask
                else base_dir / self.crop / "chirps_gefs"
            )

            df_gefs = pd.read_csv(
                list(path_gefs.glob(self.df_region["region"].unique()[0] + "*.csv"))[0],
                header=None,
            )
            val_gefs = (
                float(df_gefs.values[1][5])
                if not math.isnan(float(df_gefs.values[1][5]))
                else 0.0
            )

            # Add CHIRPS-GEFS
            start_date = ar.utcnow().shift(days=+15).date()
            end_date = ar.utcnow().shift(days=+16).date()

            self.df_region.loc[start_date:end_date, "chirps_gefs"] = val_gefs
            self.df_ccs.loc[start_date.strftime("%Y-%m-%d"), "chirps_gefs"] = val_gefs


def run(params=None):
    import time

    time.sleep(60 * 25)


if __name__ == "__main__":
    pass
