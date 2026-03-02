import typing
from datetime import datetime
import calendar as cal
import pandas as pd
from tqdm import tqdm
import numpy as np

from geocif.backup import geo, features
from geocif.agmet import utils


class geocif(geo.geo):
    def __init__(self, path_config_file):
        # Create geo object
        super().__init__(path_config_file)

        self.model: str = None  # Name of the model to run e.g. MERF
        self.iteration: int = None
        self.fraction_of_season: float = None
        self.forecast_year: int = None
        self.forecast_month: int = None
        self.forecast_start_month: str = None
        self.forecast_end_month: str = None
        self.forecast_month_names: str = None
        self.doys: typing.List = []

        self.df_season: pd.DataFrame = pd.DataFrame()
        self.df_now_train: pd.DataFrame = pd.DataFrame()
        self.df_now: pd.DataFrame = pd.DataFrame()

        self.date_peak_season: pd.Timestamp = None
        self.full_season: typing.List = []
        self.current: typing.List = []
        self.region_season: typing.List = []

        self.forecast_season: int = None
        self.peak_season: typing.List = []

        # Figure out how often to execute the ML model, e.g. interval_length = daily implies a daily model run
        self.interval_length = self.parser.get("DEFAULT", "interval_length")
        # Translate interval_length to number of days e.g. dekad = 10, daily = 1 ...
        self.run_model_N_days = utils.get_model_frequency(self.interval_length)

        # Should the model only be run at peak growing season?
        self.run_model_at_peak = self.parser.getboolean("DEFAULT", "run_model_at_peak")

        # Which peak to use? First, median, or last?
        self.peak_to_use = self.parser.get("DEFAULT", "peak_to_use")

    def generate_feature_names(self):
        """
        Generate feature names for the current iteration
        """
        # percentiles = list(range(0, self.fraction_of_season, 10))
        # percentiles = ['t' + str(p) for p in percentiles]
        percentiles = ["t10", "t20", "t30", "t50", "t60", "t70", "t80", "t90", "t100"]

        for var in self.eo_model:
            for idx, f in enumerate(percentiles):
                # pass
                # cumulative feature
                # if f'cum_{f}_var' not in self.feature_names:
                #     self.feature_names.append(f'cum_{f}_{var}')

                if f"{f}_{var}" not in self.feature_names:
                    self.feature_names.extend([f"{f}_{var}"])

            # percentile values for entire season: min, 25th, 50th, 75, 90th, max
            self.feature_names.append(f"min_{var}")
            self.feature_names.append(f"p25_{var}")
            self.feature_names.append(f"p50_{var}")
            self.feature_names.append(f"p75_{var}")
            self.feature_names.append(f"p90_{var}")
            self.feature_names.append(f"max_{var}")
            # cumulative feature
            self.feature_names.append(f"cum_{var}")

            for threshold in [25, 50, 75, 90]:
                self.feature_names.append(f"count_above_{threshold}p_{var}")
                self.feature_names.append(f"count_below_{threshold}p_{var}")
                self.feature_names.append(f"consecutive_above_{threshold}p_{var}")
                self.feature_names.append(f"consecutive_below_{threshold}p_{var}")

                #
                # # difference in consecutive features
                # if f'diff_{f}_var' not in self.feature_names:
                #     if idx < len(percentiles) - 1:
                #         self.feature_names.append(f'diff_{f}_{var}')
            # self.feature_names.extend([f'count_above_mean_{var}'])
            # self.feature_names.extend([f'mean_abs_change_{var}'])

        self.feature_names.extend(
            ["zero_precip", "doy_peak_ndvi", "harvest_season"]
        )  # f'average_{'yield'}',

    def create_features(self):
        pass

    def train(self):
        pass

    def predict(self):
        pass

    def setup_season_ml(self, drop_forecast_season=True):
        """

        Args:
            drop_forecast_season ():

        Returns:

        """
        #              Season      region   yield
        # 2000-01-01     NaN       idaho    NaN
        # 2000-03-15   2000.0      idaho    2.4
        # Drop any lines with NaN in them
        df_pre_ml = (
            self.df_now_train[["harvest_season", "region", "yield"]]
            .drop_duplicates()
            .dropna(how="any")
        )

        # Drop forecast_season row since prediction data cannot be used for training
        if drop_forecast_season:
            df_pre_ml.drop(
                df_pre_ml[df_pre_ml["harvest_season"] == self.forecast_season].index,
                inplace=True,
            )

        df_pre_ml.loc[:, "original_yield"] = df_pre_ml["yield"]

        return df_pre_ml

    def setup_region_closest_years_ml(self, year, region):
        """

        Args:
            year ():
            region ():

        Returns:

        """
        df = self.df_now_train[
            (self.df_now_train["harvest_season"] == year)
            & (self.df_now_train["region"] == region)
        ]

        # Excluding forecast year and current year from the closest years
        self.get_closest_season(year)

        closest = self.closest
        if year in closest:
            closest.remove(year)

        df_rc = self.df_now_train[
            (self.df_now_train["region"] == region)
            & (  # only for region in consideration
                self.df_now_train["harvest_season"].isin(closest)
            )
        ]  # only include years closest to forecast year

        # Current year should not be in dataframe
        assert year not in df_rc["harvest_season"].unique()

        # Drop rows for which season is NaN i.e. out of season
        df_rc = df_rc[np.isfinite(df_rc["harvest_season"])]

        return df, df_rc

    def train(self, drop_forecast_season=True):
        """

        Args:
            drop_forecast_season ():

        Returns:

        """
        # Create train dataframe based on forecast season
        self.df_now_train = self.df_now[
            self.df_now["harvest_season"] != self.forecast_season
        ]
        # self.df_now_test = self.df_now[self.df_now['harvest_season'] == self.forecast_season]

        #####################################################
        # Create training dataframe with year and region as index
        #####################################################
        df_ml = self.setup_season_ml(drop_forecast_season=drop_forecast_season)

        for idx, row in df_ml.iterrows():
            year, region = row[["harvest_season", "region"]]  # e.g. 2000.0, 'alabama'

            # Create mask for machine learning dataframe specific to year, region
            mask_year_region = (df_ml["harvest_season"] == year) & (
                df_ml["region"] == region
            )

            # Create dataframe for current year and region (df);
            # Create dataframe for closest years to current year and current region (df_region_closest)
            df, df_region_closest = self.setup_region_closest_years_ml(year, region)

            # Compute ML variables i.e. max and agg etc. over each crop growth stage
            # df_ml contains seasonal average values for multiple variables
            #               season      region      yield      1_max_ndvi      2_max_ndvi      3_max_ndvi
            # 2000-03-15    2000.0       idaho         5.04375      132.698          171.043        156.016
            df_ml = features.loop_fe(df, df_ml, mask_year_region)
            df_ml.loc[mask_year_region, "median_yield"] = np.nanmedian(
                df_region_closest.groupby(["region", "harvest_season"])["yield"]
                .mean()
                .values
            )

        # self.feature_names.extend([f'average_{'yield'}', 'harvest_season'])

        features.detrend(df_ml, self.closest)

        if df_ml.empty:
            return pd.DataFrame()
        elif df_ml.isnull().values.any():
            # For the rest, just fill with median values since ML cannot operate on NaN values
            df_ml.fillna(df_ml.median(), inplace=True)

        # convert index to datetime object
        df_ml.index = pd.to_datetime(df_ml.index)

        return df_ml

    def current_season_df(self, end_doy):
        """
        Create a dataframe for the current season fraction across all regions
        Args:
            end_doy ():

        Returns:

        """
        # Loop through each admin1, subset it based on current doys
        frame = []
        for region in self.list_regions:
            # Fill in values from starting doy to the currently last doy
            select_doys = utils.year_range(self.doys[0], end_doy + 1)

            df = self.df_ccs[
                (self.df_ccs["doy"].isin(select_doys))
                & (self.df_ccs["region"] == region)
            ]
            frame.append(df)

        return pd.concat(frame)

    def run_model(self):
        # Generate ML feature names
        # self.generate_feature_names()

        # Get day of years (doys) for which to train and test model
        self.doys_to_model()

        # Loop through each day of year (doy) and train and test model
        for idx, end_doy in enumerate(tqdm(self.doys[1:], desc="Running GEOCIF model")):
            self.track_model(idx)

            # Create dataframe combining all regions for the doys for which we are running the model
            self.df_now = self.current_season_df(end_doy)

            # Create training dataframe
            self.train()

    def track_model(self, idx):
        """
        Track the current iteration of the model
        Args:
            idx ():

        Returns:

        """
        # What is the current iteration?
        # i.e. if we are going to train the model 10 times this season, are we on the first, second, etc. iteration?
        self.iteration = idx + 1

        # What is the fraction of season that has elapsed based on which doy out of the list of doy's we are currently on?
        self.fraction_of_season = int(self.iteration * 10 / len(self.doys))

        # Get the year and month for which we will be testing the model
        if self.run_model_at_peak:
            self.forecast_year, self.forecast_month = (
                self.peak_season[0],
                self.peak_season[1],
            )
        else:
            i = (idx + 2) * self.run_model_N_days
            self.forecast_year, self.forecast_month = (
                self.full_season[i][0],
                self.full_season[i][1],
            )

        self.forecast_start_month = cal.month_name[self.full_season[0][1]]  # e.g. April
        self.forecast_end_month = cal.month_name[self.forecast_month]  # e.g. October
        self.forecast_month_names = f"{self.forecast_start_month}_{self.forecast_end_month}"  # e.g. April_October

    def doys_to_model(self):
        """
        Get day of year (doys) for which to train and test model
        """
        if self.run_model_at_peak and self.forecast_season <= datetime.now().year:
            self.doys = utils.get_doys(
                [self.full_season[0], self.peak_season], interval="peak_season"
            )
        else:
            # interval_length can be daily, dekad, weekly, monthly etc.
            self.doys = utils.get_doys(self.full_season, interval=self.interval_length)

    def sanity_check_pre_model(self):
        # If dataframe is empty then bail
        if self.df_ccs.empty:
            return False

        # If dataframe does not have yield information then bail
        if self.df_ccs["yield"].isnull().all():
            return False

        # If dataframe does not have area information then bail
        if self.df_ccs["area"].isnull().all():
            return False

        return True

    def peak_growing_season(self):
        peak_season = []

        for region in self.list_regions:
            self.setup_region(region, self.forecast_season, type_region="region_year")

            end_of_greenup = self.df_region[
                self.df_region["crop_calendar"] == 1.0
            ].last_valid_index()
            end_of_senescence = self.df_region[
                self.df_region["crop_calendar"] == 2.0
            ].last_valid_index()

            if not end_of_greenup:
                end_of_greenup = self.df_region[
                    self.df_region["crop_cal"] == 2.0
                ].first_valid_index()

            mid_point = end_of_greenup + (end_of_senescence - end_of_greenup) / 2
            peak_season.append(mid_point)

        # Different adm1s have different peak dates, therefore determine median peak date
        sr = pd.Series(peak_season)
        sr = sr[~sr.isnull()]

        if self.peak_to_use == "first":
            self.date_peak_season = pd.Timestamp.fromordinal(
                int(sr.apply(lambda x: x.toordinal()).min())
            )
        elif self.peak_to_use == "last":
            self.date_peak_season = pd.Timestamp.fromordinal(
                int(sr.apply(lambda x: x.toordinal()).max())
            )
        elif self.peak_to_use == "median":
            self.date_peak_season = pd.Timestamp.fromordinal(
                int(sr.apply(lambda x: x.toordinal()).median())
            )

        # if peak season date > current date then use current date as peak season date
        if self.date_peak_season > datetime.today():
            time_tuple = datetime.today().timetuple()
        else:
            time_tuple = self.date_peak_season.timetuple()

        self.peak_season = [time_tuple.tm_year, time_tuple.tm_mon, time_tuple.tm_yday]

    def get_season_information(self):
        """
        Create three class members that are used throughout the model:
        1. full_season: superset of all the months in a season for a country x crop. format: [(year1, month1, doy1), ...]
        2. current: subset of full_season that is used to train the model. format: [(month1, doy1), ...]
        3. region_season: dictionary {region: (year, month, doy)} in season for each region
        Returns:

        """
        time_col = ["year", "month", "doy"]

        prev = (
            self.df_season.groupby(["region", "crop_calendar"] + time_col)
            .size()
            .reset_index()
            .rename(columns={0: "count"})
            .drop("count", 1)
        )

        # superset of all the months in a season for a country x crop. format: [(year1, month1, doy1), ...]
        # e.g. [[2016, 1, 1], [2016, 1, 2], ..., [2016, 2, 1], [2016, 2, 2], [2016, 2, 3], ...
        self.full_season = (
            prev[time_col]
            .sort_values(time_col)
            .drop_duplicates()
            .values.astype(int)
            .tolist()
        )

        # superset of all the months in a season for a country x crop. format: [(month1, doy1), ...]
        self.current = [
            [x[1], x[2]] for x in self.full_season
        ]  # get list of doy's to plot

        # Dictionary (key: region) and values (list of year, month) in season for each region
        # alabama[(2016.0, 1.0), (2016.0, 2.0), (2016.0, 3.0), ...
        self.region_season = prev.groupby("region").apply(
            lambda x: list(
                zip(
                    x[time_col[0]].astype(int),
                    x[time_col[1]].astype(int),
                    x[time_col[2]].astype(int),
                )
            )
        )

    def setup_model(self, model, forecast_season):
        """
        Initialize for GEOCIF run the following:
        1. Select current season dataframe: df_season
        2. Set variables for season information
        3. Determine when peak growing season happens
        Args:
            model ():
            forecast_season ():

        Returns:

        """
        self.model = model
        self.forecast_season = forecast_season

        # Subset dataframe to forecast season
        self.df_season = self.df_ccs[
            self.df_ccs["harvest_season"] == self.forecast_season
        ]

        # Get information on season: year, month, day
        self.get_season_information()

        # Determine when peak growing season happens
        self.peak_growing_season()


def loop_geocif(path_config_file=None):
    """

    Args:
        path_config_file ():

    Returns:

    """
    obj = geocif(path_config_file)

    # Create combinations of run parameters
    all_combinations = obj.create_run_combinations()

    pbar = tqdm(all_combinations, total=len(all_combinations))
    for country, scale, crop, growing_season in pbar:
        # Setup country information, includes crop, growing season
        obj.setup_country(country, scale, crop, growing_season)

        # Check if dataframe is not empty, yield and area information is available
        check = obj.sanity_check_pre_model()
        if not check:
            continue

        # Loop through seasons and plot for each admin_1 region and calendar region
        for forecast_season in obj.forecast_seasons:
            # Run ML model(s)
            for model in obj.models:
                # Initialize model
                obj.setup_model(model, forecast_season)

                # Execute model
                obj.run_model()


def run():
    loop_geocif(
        [
            "D:/Users/ritvik/projects/geoprepare/geoprepare/geoprepare.txt",
            "D:/Users/ritvik/projects/geoprepare/geoprepare/geoextract.txt",
            "D:/Users/ritvik/projects/geocif/geocif/config/geocif.txt",
        ]
    )


if __name__ == "__main__":
    run()
