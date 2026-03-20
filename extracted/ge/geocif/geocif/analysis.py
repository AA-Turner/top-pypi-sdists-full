import ast
import os
import shutil
import sqlite3
import warnings
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import arrow as ar
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import palettable as pal
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from geocif import logger as log
from geocif import utils
from .viz import plot

warnings.simplefilter(action="ignore", category=FutureWarning)

# Show usage info on import
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console()
_table = Table(show_header=False, box=None, padding=(0, 1))
_table.add_column(style="bold cyan", no_wrap=True)
_table.add_column()
_table.add_row("Usage", "from geocif import analysis; analysis.run(cfg)")
_table.add_row("cfg", "\\[geobase.txt, countries.txt, crops.txt, geocif.txt]")
_console.print(Panel(_table, title="[bold bright_white]GeoCIF Analysis Runner[/]", border_style="bright_blue", padding=(1, 2)))


@dataclass
class Geoanalysis:
    path_config_files: List[Path] = field(default_factory=list)
    logger: log = None
    parser: ConfigParser = field(default_factory=ConfigParser)

    def __post_init__(self):
        self.country: str = None
        self.countries: list = None
        self.crop: str = None
        self.table: str = None
        self.forecast_season: int = None
        self.model_names: list = []
        self.df_analysis: pd.DataFrame = None
        self.lag_yield_as_feature: bool = None
        self.number_lag_years: int = None
        self.all_seasons_with_yield: list = None

        self.project_name = self.parser.get("DEFAULT", "project_name", fallback="geocif")
        self.dir_out = Path(self.parser.get("PATHS", "dir_output")) / self.project_name
        self._date = ar.utcnow().to("America/New_York")
        self.today = self._date.format("MMMM_DD_YYYY")

        self.dir_ml = self.dir_out / "ml"
        self.dir_db = self.dir_ml / "db"
        self.dir_analysis = self.dir_ml / "analysis" / self.today
        self.dir_plots = self.dir_analysis / "plots"
        self.dir_maps = self.dir_analysis / "maps"
        self.dir_config = self.dir_analysis / "config"
        os.makedirs(self.dir_db, exist_ok=True)
        os.makedirs(self.dir_analysis, exist_ok=True)
        os.makedirs(self.dir_plots, exist_ok=True)
        os.makedirs(self.dir_maps, exist_ok=True)
        os.makedirs(self.dir_config, exist_ok=True)

        self.db_forecasts = self.parser.get("DEFAULT", "db")
        self.db_path = self.dir_db / self.db_forecasts

        self.dir_boundary_files = Path(self.parser.get("PATHS", "dir_boundary_files"))

    def table_exists(self, db_path, table_name):
        # Create a connection to the SQLite database
        with sqlite3.connect(db_path) as con:
            # Create a cursor object using the cursor() method
            cursor = con.cursor()

            # Define the query to find the table
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?"

            # Execute the prepared query passing the table_name as a parameter
            cursor.execute(query, (table_name,))

            # Fetch the result
            result = cursor.fetchone()

            # Close the cursor
            cursor.close()

        # Return True if a result is found, False otherwise
        return result is not None

    def query(self):
        self.logger.info(f"Query {self.country} {self.crop}")
        con = sqlite3.connect(self.db_path)

        # Read from database, where country and crop match
        query = "SELECT * FROM " + self.table
        try:
            self.df_analysis = pd.read_sql_query(query, con)

            # For pooled tables, don't filter by country (results have per-row Country)
            if self.country == "pooled":
                self.df_analysis = self.df_analysis[
                    (self.df_analysis["Crop"] == self.crop)
                    & (self.df_analysis["Model"] == self.model)
                ]
            else:
                self.df_analysis = self.df_analysis[
                    (self.df_analysis["Country"] == self.country)
                    & (self.df_analysis["Crop"] == self.crop)
                    & (self.df_analysis["Model"] == self.model)
                ]
        except Exception as e:
            pass

        con.commit()
        con.close()

    def annual_metrics(self, df):
        """
        Compute metrics for a given dataframe
        :param df: dataframe containing Observed and Forecast data
        """
        import scipy.stats
        from sklearn.metrics import mean_squared_error, mean_absolute_error

        if len(df) < 3:
            return pd.Series()

        # Compute metrics
        from geocif.ml.embedding import _ccc_series

        rmse = np.sqrt(mean_squared_error(df[self.observed], df[self.predicted]))
        nse = utils.nse(df[self.observed], df[self.predicted])
        r2 = scipy.stats.pearsonr(df[self.observed], df[self.predicted])[0] ** 2
        ccc = _ccc_series(df[self.observed], df[self.predicted])
        mae = mean_absolute_error(df[self.observed], df[self.predicted])
        mape = utils.mape(df[self.observed], df[self.predicted])
        pbias = utils.pbias(df[self.observed], df[self.predicted])

        # Return as a dictionary
        dict_results = {
            "Root Mean Square Error": rmse,
            "Nash-Sutcliff Efficiency": nse,
            "$r^2$": r2,
            "CCC": ccc,
            "Mean Absolute Error": mae,
            "Mean Absolute\nPercentage Error": mape,
            "Percentage Bias": pbias,
        }

        return pd.Series(dict_results)

    def regional_metrics(self, df):
        # Compute MAPE for each region, compute within this function
        # Compute metrics

        actual, predicted = df[self.observed], df[self.predicted]
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100

        return pd.Series({"Mean Absolute Percentage Error": mape})

    def add_stage_information(self, df):
        """
        Create a new column called Dekad which contains the last dekad
        :param df: dataframe containing the column Stages for which we will compute Dekad information
        """
        for i, row in df.iterrows():
            # Get the latest stage
            stage = row["Stage Name"].split("-")[0]
            df.loc[i, "Date"] = stage

        return df

    def select_top_N_years(self, group, N=5):
        return group.nsmallest(N, "Mean Absolute Percentage Error")

    def analyze(self):
        self.logger.info(f"Analyze {self.country} {self.crop}")

        df = self._clean_data()
        if df.empty:
            return pd.DataFrame(), pd.DataFrame()

        df_metrics = self._compute_metrics(df)
        df_metrics = self._process_metrics(df_metrics)

        self._plot_metrics(df_metrics)
        df_regional_metrics_by_year = self._compute_regional_metrics(
            df, by="Harvest Year"
        )
        df_regional_metrics_by_year = self._select_top_years(
            df_regional_metrics_by_year
        )
        df_regional_metrics = self._average_mape(df_regional_metrics_by_year)

        self._store_results(
            df_metrics, df_regional_metrics, df_regional_metrics_by_year
        )
        df_national_yield = self._compute_national_yield(df)
        self._plot_national_yield(df_national_yield)
        self._plot_regional_yield_scatter(df)
        self._plot_scatter_by_region(df)
        if self.country == "pooled":
            self._plot_scatter_by_country(df)
        self._plot_mape_by_region(df_regional_metrics)

        return df_metrics, df_regional_metrics, df_national_yield

    def _clean_data(self):
        # Remove rows with missing values in Observed Yield (tn per ha)
        return self.df_analysis.dropna(subset=["Observed Yield (tn per ha)"])

    def _compute_metrics(self, df):
        # For each Harvest Year, Stages combination, compute metrics
        df_metrics = (
            df.groupby(
                ["Country", "Model", "Harvest Year", "Stage Name", "Stage Range"]
            )
            .apply(self.annual_metrics)
            .reset_index()
        )

        # return df_metrics.pivot_table(
        #    index=["Country", "Model", "Harvest Year", "Stage Name", "Stage Range"],
        #    columns="level_5",
        #    values=0,
        # ).reset_index()
        return df_metrics

    def _process_metrics(self, df_metrics):
        # Assign each unique Stage Name a unique integer identifier
        df_metrics["Stage_ID"] = pd.Categorical(df_metrics["Stage Name"]).codes

        # Order by Harvest Year and Number Stages (ascending)
        df_metrics = df_metrics.sort_values(by=["Harvest Year", "Stage_ID"])

        # Add columns with the name of the country and crop
        df_metrics["Country"] = self.country
        df_metrics["Crop"] = self.crop

        # Add stage information for plotting
        return self.add_stage_information(df_metrics)

    def _plot_metrics(self, df_metrics):
        metrics = [
            "Root Mean Square Error",
            "$r^2$",
            "CCC",
            "Mean Absolute Error",
            "Mean Absolute\nPercentage Error",
            "Percentage Bias",
        ]
        for metric in metrics:
            self.plot_metric(df_metrics, metric)

    def _compute_regional_metrics(self, df, by=None):
        cols = [
            "Country",
            "Region",
            "% of total Area (ha)",
            "Model",
            "Crop",
            "Stage Name",
            "Stage Range",
        ]

        if by:
            return df.groupby(cols + [by]).apply(self.regional_metrics).reset_index()
        else:
            return df.groupby(cols).apply(self.regional_metrics).reset_index()

    def _select_top_years(self, df_regional_metrics, top_N=-1):
        if top_N == -1:
            return df_regional_metrics
        else:
            return (
                df_regional_metrics.groupby(["Country", "Region"])
                .apply(lambda x: self.select_top_N_years(x, 10))
                .reset_index(drop=True)
            )

    def _average_mape(self, df_regional_metrics):
        cols = [
            "Country",
            "Region",
            "% of total Area (ha)",
            "Model",
            "Crop",
            "Stage Name",
            "Stage Range",
        ]
        return (
            df_regional_metrics.groupby(cols)["Mean Absolute Percentage Error"]
            .mean()
            .reset_index()
        )

    def _store_results(
        self, df_metrics, df_regional_metrics, df_regional_metrics_by_year
    ):
        # Create an index based on specific columns
        df_metrics.index = df_metrics.apply(
            lambda row: "_".join(
                [
                    str(row[col])
                    for col in [
                        "Country",
                        "Crop",
                        "Model",
                        "Harvest Year",
                        "Stage Name",
                    ]
                ]
            ),
            axis=1,
        )
        df_metrics.index.set_names(["Index"], inplace=True)

        df_regional_metrics.index = df_regional_metrics.apply(
            lambda row: "_".join(
                [
                    str(row[col])
                    for col in ["Country", "Region", "Model", "Crop", "Stage Name"]
                ]
            ),
            axis=1,
        )
        df_regional_metrics.index.set_names(["Index"], inplace=True)

        df_regional_metrics_by_year.index = df_regional_metrics_by_year.apply(
            lambda row: "_".join(
                [
                    str(row[col])
                    for col in [
                        "Country",
                        "Region",
                        "Model",
                        "Crop",
                        "Stage Name",
                        "Harvest Year",
                    ]
                ]
            ),
            axis=1,
        )
        df_regional_metrics_by_year.index.set_names(["Index"], inplace=True)

        # Format with 3 places after the decimal point
        df_metrics = df_metrics.round(3)
        df_regional_metrics = df_regional_metrics.round(3)
        df_regional_metrics_by_year = df_regional_metrics_by_year.round(3)

        # Store results in database
        with sqlite3.connect(self.db_path) as con:
            utils.to_db(self.db_path, "country_metrics", df_metrics)
            utils.to_db(self.db_path, "regional_metrics", df_regional_metrics)
            utils.to_db(
                self.db_path, "regional_metrics_by_year", df_regional_metrics_by_year
            )

            con.commit()

    def _compute_national_yield(self, df_region):
        # Define column names
        observed = "Observed Yield (tn per ha)"
        predicted = "Predicted Yield (tn per ha)"
        area_ha = "Area (ha)"

        df_tmp = df_region.copy()

        # Fill
        df_tmp[area_ha] = df_tmp.groupby("Country")[area_ha].transform(
            lambda x: x.fillna(x.median())
        )

        # Log that we are filling missing values with the median
        self.logger.info(
            f"Filling missing values in {area_ha} with the median for each country"
        )

        # Compute observed and predicted national yield by multiplying Yield (tn per ha) by Area (ha)
        df_tmp[observed] = df_tmp[observed] * df_tmp[area_ha]
        df_tmp[predicted] = df_tmp[predicted] * df_tmp[area_ha]

        # Group by Country and Harvest Year, then sum the National Yield and Area
        df_national_yield = (
            df_tmp.groupby(["Country", "Harvest Year"])
            .agg({observed: "sum", predicted: "sum", area_ha: "sum"})
            .reset_index()
        )

        # Compute observed and predicted yield per ha for each Harvest Year
        df_national_yield[observed] = (
            df_national_yield[observed] / df_national_yield[area_ha]
        )
        df_national_yield[predicted] = (
            df_national_yield[predicted] / df_national_yield[area_ha]
        )

        return df_national_yield

    def _plot_regional_yield_scatter(self, df):
        """
        Plot observed vs predicted yield for all regions and all years.
        """
        from sklearn.metrics import (
            mean_squared_error,
            r2_score,
            mean_absolute_percentage_error,
        )

        # Extract data
        y_observed = df["Observed Yield (tn per ha)"]
        y_predicted = df["Predicted Yield (tn per ha)"]
        years = pd.to_numeric(df["Harvest Year"], errors="coerce")

        # Generate colors for years
        cmap = plt.cm.viridis  # Colormap for years
        norm = plt.Normalize(
            vmin=years.min(), vmax=years.max()
        )  # Normalize years to colormap
        colors = [cmap(norm(year)) for year in years]

        # Create the plot
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(10, 6))

            # Add gridlines
            ax.grid(True, linestyle="--", alpha=0.5)

            # Scatter plot with colors representing years
            scatter = ax.scatter(y_observed, y_predicted, color=colors, s=50)

            # Add 1:1 diagonal line
            max_yield = max(y_observed.max(), y_predicted.max()) * 1.25
            ax.plot([0, max_yield], [0, max_yield], color="gray", linestyle="--")

            # Calculate and display metrics
            rmse = np.sqrt(mean_squared_error(y_observed, y_predicted))
            mape = mean_absolute_percentage_error(y_observed, y_predicted)
            r2 = r2_score(y_observed, y_predicted)
            n_points = len(y_observed)  # Number of data points

            textstr = (
                f"RMSE: {rmse:.2f} tn/ha\n"
                f"MAPE: {mape:.2%}\n"
                f"$r^2$: {r2:.2f}\n"
                f"N: {n_points}"
            )

            ax.annotate(
                textstr,
                xy=(0.05, 0.95),
                xycoords="axes fraction",
                fontsize=12,
                verticalalignment="top",
            )

            # Set axis limits and labels
            ax.set_xlabel("Observed Yield (tn/ha)")
            ax.set_ylabel("Predicted Yield (tn/ha)")
            ax.set_xlim(0, max_yield)
            ax.set_ylim(0, max_yield)

            # Add colorbar for years
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = fig.colorbar(sm, ax=ax, aspect=50, pad=0.02)
            cbar.set_label("Harvest Year")

            # Set equispaced ticks for exactly 5 points
            ticks = np.linspace(
                years.min(), years.max(), 5, dtype=int
            )  # 5 equispaced ticks
            cbar.set_ticks(ticks)
            cbar.ax.set_yticklabels([str(tick) for tick in ticks])

            plt.tight_layout()

            # Save the plot
            fname = f"scatter_all_regions_{self.country}_{self.crop}.png"
            plt.savefig(self.dir_country_plots / fname, dpi=250)
            plt.close()

    def _plot_scatter_by_region(self, df):
        """Small-multiples scatter plot: observed vs predicted yield per region."""
        import math
        from sklearn.metrics import (
            mean_squared_error,
            r2_score,
            mean_absolute_percentage_error,
        )

        regions = sorted(df["Region"].unique())
        n = len(regions)
        if n == 0:
            return

        ncols = min(4, n)
        nrows = math.ceil(n / ncols)

        fig, axes = plt.subplots(
            nrows, ncols,
            figsize=(4 * ncols, 4 * nrows),
            squeeze=False,
        )

        for idx, region in enumerate(regions):
            row, col = divmod(idx, ncols)
            ax = axes[row][col]

            sub = df[df["Region"] == region]
            obs = sub["Observed Yield (tn per ha)"]
            pred = sub["Predicted Yield (tn per ha)"]

            valid = obs.notna() & pred.notna()
            obs, pred = obs[valid], pred[valid]

            if len(obs) < 2:
                ax.set_title(region, fontsize=9)
                ax.text(0.5, 0.5, "Insufficient data", transform=ax.transAxes,
                        ha="center", va="center", fontsize=8)
                continue

            ax.scatter(obs, pred, s=20, alpha=0.7)

            max_val = max(obs.max(), pred.max()) * 1.15
            ax.plot([0, max_val], [0, max_val], color="gray", linestyle="--", linewidth=0.8)
            ax.set_xlim(0, max_val)
            ax.set_ylim(0, max_val)
            ax.set_aspect("equal", adjustable="box")

            rmse = np.sqrt(mean_squared_error(obs, pred))
            r2 = r2_score(obs, pred)
            mape = mean_absolute_percentage_error(obs, pred)

            ax.set_title(region, fontsize=9, fontweight="bold")
            ax.annotate(
                f"R²={r2:.2f}\nRMSE={rmse:.2f}\nMAPE={mape:.1%}",
                xy=(0.05, 0.95), xycoords="axes fraction",
                fontsize=7, verticalalignment="top",
            )
            ax.tick_params(labelsize=7)

        # Hide unused axes
        for idx in range(n, nrows * ncols):
            row, col = divmod(idx, ncols)
            axes[row][col].set_visible(False)

        fig.supxlabel("Observed Yield (tn/ha)", fontsize=10)
        fig.supylabel("Predicted Yield (tn/ha)", fontsize=10)
        fig.suptitle(f"{self.country} — {self.crop}", fontsize=12, fontweight="bold")
        plt.tight_layout()

        fname = f"scatter_by_region_{self.country}_{self.crop}.png"
        fig.savefig(self.dir_country_plots / fname, dpi=250)
        plt.close(fig)

    def _plot_scatter_by_country(self, df):
        """Small-multiples scatter plot: observed vs predicted yield per country (pooled mode)."""
        import math
        from sklearn.metrics import (
            mean_squared_error,
            r2_score,
            mean_absolute_percentage_error,
        )

        countries = sorted(df["Country"].unique())
        n = len(countries)
        if n == 0:
            return

        ncols = min(4, n)
        nrows = math.ceil(n / ncols)

        fig, axes = plt.subplots(
            nrows, ncols,
            figsize=(4 * ncols, 4 * nrows),
            squeeze=False,
        )

        for idx, country in enumerate(countries):
            row, col = divmod(idx, ncols)
            ax = axes[row][col]

            sub = df[df["Country"] == country]
            obs = sub["Observed Yield (tn per ha)"]
            pred = sub["Predicted Yield (tn per ha)"]

            valid = obs.notna() & pred.notna()
            obs, pred = obs[valid], pred[valid]

            if len(obs) < 2:
                ax.set_title(country, fontsize=9)
                ax.text(0.5, 0.5, "Insufficient data", transform=ax.transAxes,
                        ha="center", va="center", fontsize=8)
                continue

            ax.scatter(obs, pred, s=20, alpha=0.7)

            max_val = max(obs.max(), pred.max()) * 1.15
            ax.plot([0, max_val], [0, max_val], color="gray", linestyle="--", linewidth=0.8)
            ax.set_xlim(0, max_val)
            ax.set_ylim(0, max_val)
            ax.set_aspect("equal", adjustable="box")

            rmse = np.sqrt(mean_squared_error(obs, pred))
            r2 = r2_score(obs, pred)
            mape = mean_absolute_percentage_error(obs, pred)

            ax.set_title(country, fontsize=9, fontweight="bold")
            ax.annotate(
                f"R²={r2:.2f}\nRMSE={rmse:.2f}\nMAPE={mape:.1%}",
                xy=(0.05, 0.95), xycoords="axes fraction",
                fontsize=7, verticalalignment="top",
            )
            ax.tick_params(labelsize=7)

        for idx in range(n, nrows * ncols):
            row, col = divmod(idx, ncols)
            axes[row][col].set_visible(False)

        fig.supxlabel("Observed Yield (tn/ha)", fontsize=10)
        fig.supylabel("Predicted Yield (tn/ha)", fontsize=10)
        fig.suptitle(f"Pooled — {self.crop}", fontsize=12, fontweight="bold")
        plt.tight_layout()

        fname = f"scatter_by_country_{self.crop}.png"
        fig.savefig(self.dir_plots / fname, dpi=250)
        plt.close(fig)

    def _plot_mape_by_region(self, df_regional_metrics):
        """Horizontal bar chart of average MAPE by region."""
        if df_regional_metrics.empty or "MAPE" not in df_regional_metrics.columns:
            return

        df_plot = (
            df_regional_metrics
            .groupby("Region")["MAPE"]
            .mean()
            .sort_values(ascending=True)
        )

        if df_plot.empty:
            return

        fig, ax = plt.subplots(figsize=(8, max(4, len(df_plot) * 0.35)))
        bars = ax.barh(df_plot.index, df_plot.values, color="steelblue")

        for bar, val in zip(bars, df_plot.values):
            ax.text(
                val + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=8,
            )

        ax.set_xlabel("MAPE (%)")
        ax.set_title(
            f"Mean MAPE by Region — {self.country} {self.crop}",
            fontsize=11, fontweight="bold",
        )
        plt.tight_layout()

        fname = f"mape_by_region_{self.country}_{self.crop}.png"
        fig.savefig(self.dir_country_plots / fname, dpi=250)
        plt.close(fig)

    def _plot_national_yield(self, df_national_yield):
        from sklearn.metrics import (
            mean_squared_error,
            r2_score,
            mean_absolute_percentage_error,
        )

        # Ensure 'Harvest Year' is numeric
        df_national_yield["Harvest Year"] = pd.to_numeric(
            df_national_yield["Harvest Year"], errors="coerce"
        )

        # Extract data
        x = df_national_yield["Harvest Year"]
        y_observed = df_national_yield["Observed Yield (tn per ha)"]
        y_predicted = df_national_yield["Predicted Yield (tn per ha)"]

        # Generate colors for years
        cmap = plt.cm.viridis  # Colormap for years
        norm = plt.Normalize(vmin=x.min(), vmax=x.max())  # Normalize years to colormap
        colors = [cmap(norm(year)) for year in x]

        # Create the plot
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(10, 6))  # Explicitly define axes

            max_yield = max(y_observed.max(), y_predicted.max()) * 1.25

            # Add gridlines
            ax.grid(True, linestyle="--", alpha=0.5)

            # Scatter plot with uniform size and dynamic colors
            for year, obs, pred, color in zip(x, y_observed, y_predicted, colors):
                ax.scatter(obs, pred, color=color, s=50, label=year)

            # Add 1:1 diagonal line
            ax.plot([0, max_yield], [0, max_yield], color="gray", linestyle="--")

            # Calculate and display metrics
            rmse = np.sqrt(mean_squared_error(y_observed, y_predicted))
            mape = mean_absolute_percentage_error(y_observed, y_predicted)
            r2 = r2_score(y_observed, y_predicted)

            n_points = len(y_observed)  # Number of data points

            textstr = (
                f"RMSE: {rmse:.2f} tn/ha\n"
                f"MAPE: {mape:.2%}\n"
                f"$r^2$: {r2:.2f}\n"
                f"N: {n_points}"
            )

            ax.annotate(
                textstr,
                xy=(0.05, 0.95),
                xycoords="axes fraction",
                fontsize=12,
                verticalalignment="top",
            )

            # Set axis limits and labels
            ax.set_xlabel("Observed Yield (tn/ha)")
            ax.set_ylabel("Predicted Yield (tn/ha)")
            ax.set_xlim(0, max_yield)
            ax.set_ylim(0, max_yield)

            # Add legend for years
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = fig.colorbar(
                sm, ax=ax, aspect=50, pad=0.02
            )  # Specify the axis explicitly
            cbar.set_label("Harvest Year")

            # Set equispaced ticks for exactly 5 points
            ticks = np.linspace(x.min(), x.max(), 5, dtype=int)  # 5 equispaced ticks
            cbar.set_ticks(ticks)
            cbar.ax.set_yticklabels([str(tick) for tick in ticks])

            plt.tight_layout()

            # Save the plot
            fname = f"scatter_{self.country}_{self.crop}.png"
            plt.savefig(self.dir_country_plots / fname, dpi=250)
            plt.close()

    def get_historic_production(self):
        # Read in historic production data
        if self.country == "pooled":
            frames = []
            for c in self.countries:
                f = utils.statistics_file_path(self.dir_out, self.method, c, self.crop)
                if f.exists():
                    frames.append(pd.read_csv(f))
            df_all = pd.concat(frames, ignore_index=True)
        else:
            file = utils.statistics_file_path(self.dir_out, self.method, self.country, self.crop)
            df_all = pd.read_csv(file)

        # Keep only the relevant columns and drop NaNs
        df_all = df_all[["Region", "Harvest Year", "Yield (tn per ha)"]].dropna()

        # --- For computing the % of total production ---
        # Determine unique years and sort them (in case they aren't already)
        years = sorted(df_all["Harvest Year"].unique())
        # Subset dataframe to include only the last 5 years of the dataset
        last_five_years = years[-5:]
        df_recent = df_all[df_all["Harvest Year"].isin(last_five_years)]

        # For each region, compute the % of total production (using yield sum over the last five years)
        df_pct = (
            df_recent.groupby("Region")["Yield (tn per ha)"]
            .sum()
            .pipe(lambda x: x / x.sum() * 100)
            .to_frame(name="% of total Area (ha)")
            .reset_index()
        )

        # --- For computing median yields ---
        # Compute median yield for 2018 - 2022
        df_median_2018_2022 = (
            df_all[df_all["Harvest Year"].between(2018, 2022)]
            .groupby("Region")["Yield (tn per ha)"]
            .mean()
            .rename(f"Median Yield (tn per ha) (2018-2022)")
            .reset_index()
        )

        # Compute median yield for 2013 - 2017
        df_median_2013_2017 = (
            df_all[df_all["Harvest Year"].between(2013, 2017)]
            .groupby("Region")["Yield (tn per ha)"]
            .mean()
            .rename("Median Yield (tn per ha) (2013-2017)")
            .reset_index()
        )

        # Compute mean yield for the last 10 years
        max_year = int(df_all["Harvest Year"].max())
        df_median_10yr = (
            df_all[df_all["Harvest Year"].between(max_year - 10, max_year - 1)]
            .groupby("Region")["Yield (tn per ha)"]
            .mean()
            .rename("Median Yield (tn per ha) (10yr)")
            .reset_index()
        )

        # Merge the median yield columns with the % of total production dataframe
        df_historic = (
            df_pct.merge(df_median_2018_2022, on="Region", how="left")
            .merge(df_median_2013_2017, on="Region", how="left")
            .merge(df_median_10yr, on="Region", how="left")
        )

        return df_historic

    def preprocess(self):
        if self.df_analysis.empty:
            return

        # Add a column called N year average that contains the average of the yield of the last 10 years
        # this will be the same for each dekad in any year
        df_lag_yield = self.df_analysis.copy()

        df_lag_yield = (
            df_lag_yield.groupby("Region")["Median Yield (tn per ha)"]
            .median()
            .reset_index()
        )
        df_lag_yield.columns = ["Region", f"{self.number_lag_years} year average"]

        self.df_analysis = self.df_analysis.merge(df_lag_yield, on="Region", how="left")

        df_historic = self.get_historic_production()
        self.df_analysis = self.df_analysis.merge(df_historic, on="Region", how="left")

        # Anomaly columns: percentage departure from reference period median
        # After merge, columns may have _y suffix if they existed in both dataframes
        for col_suffix, base_col in [
            ("2013-2017", "Median Yield (tn per ha) (2013-2017)"),
            ("2018-2022", "Median Yield (tn per ha) (2018-2022)"),
            ("10yr", "Median Yield (tn per ha) (10yr)"),
        ]:
            # Find the actual column name (may have _y suffix from merge)
            if f"{base_col}_y" in self.df_analysis.columns:
                ref_col = f"{base_col}_y"
            elif base_col in self.df_analysis.columns:
                ref_col = base_col
            else:
                continue

            self.df_analysis[f"Anomaly ({col_suffix})"] = (
                (self.df_analysis[self.predicted] - self.df_analysis[ref_col])
                / self.df_analysis[ref_col]
                * 100.0
            )

        # Compute the yield from the last year
        # Add a column called Ratio Last Year that is the ratio between the predicted yield and the last year yield
        # self.df_analysis["Ratio Last Year"] = (
        #     self.df_analysis[self.predicted]
        #     * 100.0
        #     / self.df_analysis[f"Last Year Yield (tn per ha)"]
        # )

        return self.df_analysis

    def map(self, df_plot):
        # df_plot = self.df_analysis.copy()
        models = df_plot["Model"].unique()

        for model in models:
            df_model = df_plot[df_plot["Model"] == model]

            countries = df_model["Country"].unique().tolist()
            dir_maps = self.dir_analysis / "maps" / model
            countries = [country.title().replace("_", " ") for country in countries]
            df_model["Country Region"] = (
                df_model["Country"].str.lower().str.replace("_", " ")
                + " "
                + df_model["Region"].str.lower().str.replace("_", " ")
            )

            # Change Harvest year to type int
            df_model["Harvest Year"] = df_model["Harvest Year"].astype(int)
            annotate_region_column = (
                "ADM1_NAME" if self.admin_zone == "admin_1" else "ADM2_NAME"
            )
            analysis_years = df_model["Harvest Year"].unique()
            pbar = tqdm(analysis_years, leave=False)
            for idx, year in enumerate(pbar):
                pbar.set_description(f"Map {year}")
                pbar.update()

                df_harvest_year = df_model[df_model["Harvest Year"] == year]

                # Use each country's latest available time period for maps
                # (different countries may have different latest stages)
                df_time_period_parts = []
                for ckey in df_harvest_year["Country"].unique():
                    df_c = df_harvest_year[df_harvest_year["Country"] == ckey]
                    latest = df_c["Stage Name"].unique()[-1]
                    df_time_period_parts.append(
                        df_c[df_c["Stage Name"] == latest]
                    )
                df_time_period = pd.concat(df_time_period_parts, ignore_index=True)

                # Use overall latest stage label for filenames
                all_stages = df_harvest_year["Stage Name"].unique()
                time_period = all_stages[-1]
                time_period_label = time_period.split("-")[0].strip()
                if True:
                    #
                    #                 """ % of total area """
                    if idx == 0:
                        fname = f"{self.country}_{self.crop}_{model}_perc_area.png"
                        col = "% of total Area (ha)"
                        plot.plot_map(
                            self.dg,  # dataframe containing adm1 name and polygon
                            df_model,  # dataframe containing information that will be mapped
                            merge_col="Country Region",  # Column on which to merge
                            name_country=countries,  # Plot global map
                            name_col=col,  # Which column to plot
                            dir_out=dir_maps / self.country / str(year),  # Output directory
                            fname=fname,  # Output file name
                            label=f"% of Total Area (ha)\n{self.crop.title()}",
                            vmin=df_model[col].min(),
                            vmax=df_model[col].max(),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",

                            annotate_regions=self.annotate_regions,
                            annotate_region_column=annotate_region_column,
                            loc_legend="lower left",
                        )
                    #
                    """ Unique regions """
                    fname = f"{self.country}_{self.crop}_{model}_region_ID.png"
                    col = "Region_ID"
                    df_model[col] = df_model[col].astype(int) + 1
                    if df_model["Region_ID"].nunique() > 1:
                        # Create a dictionary with each region assigned a unique integer identifier and name
                        dict_region = {
                            int(key): key
                            for key in df_time_period["Region_ID"].unique()
                        }

                        plot.plot_map(
                            self.dg,  # dataframe containing adm1 name and polygon
                            df_model,  # dataframe containing information that will be mapped
                            dict_lup=dict_region,
                            merge_col="Country Region",  # Column on which to merge
                            name_country=countries,  # Plot global map
                            name_col=col,  # Which column to plot
                            dir_out=dir_maps / self.country / str(year),  # Output directory
                            fname=fname,  # Output file name
                            label=f"Region Cluster\n{self.crop.title()}",
                            vmin=df_model[col].min(),
                            vmax=df_model[col].max(),
                            cmap=pal.tableau.Tableau_20.mpl_colors,
                            series="qualitative",

                            alpha_feature=1,
                            use_key=True,
                            annotate_regions=self.annotate_regions,
                            annotate_region_column=annotate_region_column,
                            loc_legend="lower left",
                        )
                    #                     breakpoint()

                    # """ Anomaly """
                    # fname = (
                    #     f"{fname_prefix}_{self.crop}_{time_period}_{year}_anomaly.png"
                    # )
                    # plot.plot_map(
                    #     self.dg,  # dataframe containing adm1 name and polygon
                    #     df_harvest_year,  # dataframe containing information that will be mapped
                    #     merge_col="Country Region",  # Column on which to merge
                    #     name_country=countries,  # Plot global map
                    #     name_col="Anomaly",  # Which column to plot
                    #     dir_out=self.dir_plot / str(year),  # Output directory
                    #     fname=fname,  # Output file name
                    #     label=f"% of {self.number_lag_years}-year Median Yield\n{self.crop.title()}, {year}",
                    #     vmin=df_harvest_year["Anomaly"].min(),
                    #     vmax=110,  # df_harvest_year["Anomaly"].max(),
                    #     cmap=pal.cartocolors.diverging.Geyser_5_r,
                    #     series="sequential",
                    #     show_bg=False,
                    #     annotate_regions=True,
                    #     annotate_region_column=annotate_region_column,
                    #     loc_legend="lower left",
                    # )

                    # Make map of predicted yield by country
                    for country in countries:
                        country_key = country.lower().replace(" ", "_")
                        dir_country = dir_maps / country_key / str(year)

                        df_country = df_model[df_model["Country"] == country_key]
                        fname = f"perc_area_{country_key}_{self.crop}_{model}.png"
                        col = "% of total Area (ha)"
                        plot.plot_map(
                            self.dg,  # dataframe containing adm1 name and polygon
                            df_country,  # dataframe containing information that will be mapped
                            merge_col="Country Region",  # Column on which to merge
                            name_country=[country],  # Plot global map
                            name_col=col,  # Which column to plot
                            dir_out=dir_country,  # Output directory
                            fname=fname,  # Output file name
                            label=f"% of Total Area (ha)\n{self.crop.title()}",
                            vmin=df_country[col].min(),
                            vmax=df_country[col].max(),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",

                            annotate_regions=self.annotate_regions,
                            annotate_region_column=annotate_region_column,
                            loc_legend="lower left",
                        )

                        df_country = df_harvest_year[df_harvest_year["Country"] == country_key]
                        # Use this country's own latest stage for the label
                        country_latest_stage = df_country["Stage Name"].unique()[-1]
                        country_time_label = country_latest_stage.split("-")[0].strip()
                        fname = f"predicted_yield_{country_key}_{self.crop}_{model}_{country_time_label}_{year}.png"
                        plot.plot_map(
                            self.dg,  # dataframe containing adm1 name and polygon
                            df_country,  # dataframe containing information that will be mapped
                            merge_col="Country Region",  # Column on which to merge
                            name_country=[country],  # Plot global map
                            name_col="Predicted Yield (tn per ha)",  # Which column to plot
                            dir_out=dir_country,  # Output directory
                            fname=fname,  # Output file name
                            label=f"Predicted Yield (Mg/ha)\n{self.crop.title()}, {year}",
                            vmin=df_country[self.predicted].min(),
                            vmax=df_country[self.predicted].max(),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",

                            annotate_regions=self.annotate_regions,
                            annotate_region_column=annotate_region_column,
                            loc_legend="lower left",
                        )

                        # Anomaly maps for each reference period
                        # Filter to this country's latest stage only
                        df_country = df_country[
                            df_country["Stage Name"] == country_latest_stage
                        ]
                        for period_label, anomaly_col in [
                            ("2013-2017", "Anomaly (2013-2017)"),
                            ("2018-2022", "Anomaly (2018-2022)"),
                            ("10yr", "Anomaly (10yr)"),
                        ]:
                            fname = f"anomaly_{country_key}_{self.crop}_{model}_{country_time_label}_{year}.png"
                            _amin = df_country[anomaly_col].min()
                            _amax = df_country[anomaly_col].max()
                            _extend = "both" if _amin < -40 and _amax > 40 else "min" if _amin < -40 else "max" if _amax > 40 else "neither"
                            plot.plot_map(
                                self.dg,
                                df_country,
                                merge_col="Country Region",
                                name_country=[country],
                                name_col=anomaly_col,
                                dir_out=dir_country / period_label,
                                fname=fname,
                                label=f"% departure from {period_label} mean\n{self.crop.title()}, {year}",
                                vmin=-40,
                                vmax=40,
                                cmap=pal.colorbrewer.diverging.BrBG_11,
                                series="diverging",
                                annotate_regions=self.annotate_regions,
                                annotate_region_column=annotate_region_column,
                                loc_legend="lower left",
                                extend=_extend,
                            )

                    # Consolidated multi-country maps
                    # Only include countries that have data for this year
                    countries_with_data = [
                        c.title().replace("_", " ")
                        for c in df_time_period["Country"].unique()
                    ]
                    if len(countries_with_data) > 1:
                        dir_consolidated = dir_maps / str(year)
                        consolidated_prefix = f"{len(countries_with_data)}_countries"

                        fname = f"{consolidated_prefix}_{self.crop}_{model}_predicted_yield_{time_period_label}_{year}.png"
                        plot.plot_map(
                            self.dg,
                            df_time_period,
                            merge_col="Country Region",
                            name_country=countries_with_data,
                            name_col="Predicted Yield (tn per ha)",
                            dir_out=dir_consolidated,
                            fname=fname,
                            label=f"Predicted Yield (Mg/ha)\n{self.crop.title()}, {year}",
                            vmin=df_time_period[self.predicted].min(),
                            vmax=df_time_period[self.predicted].max(),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",

                            annotate_regions=self.annotate_regions,
                            annotate_region_column=annotate_region_column,
                            loc_legend="lower left",
                        )

                        for period_label, anomaly_col in [
                            ("2013-2017", "Anomaly (2013-2017)"),
                            ("2018-2022", "Anomaly (2018-2022)"),
                            ("10yr", "Anomaly (10yr)"),
                        ]:
                            fname = f"{consolidated_prefix}_{self.crop}_{model}_anomaly_{time_period_label}_{year}.png"
                            _amin = df_time_period[anomaly_col].min()
                            _amax = df_time_period[anomaly_col].max()
                            _extend = "both" if _amin < -40 and _amax > 40 else "min" if _amin < -40 else "max" if _amax > 40 else "neither"
                            plot.plot_map(
                                self.dg,
                                df_time_period,
                                merge_col="Country Region",
                                name_country=countries_with_data,
                                name_col=anomaly_col,
                                dir_out=dir_consolidated / period_label,
                                fname=fname,
                                label=f"% departure from {period_label} mean\n{self.crop.title()}, {year}",
                                vmin=-40,
                                vmax=40,
                                cmap=pal.colorbrewer.diverging.BrBG_11,
                                series="diverging",
                                annotate_regions=self.annotate_regions,
                                annotate_region_column=annotate_region_column,
                                loc_legend="lower left",
                                extend=_extend,
                            )

                    """ Ratio of Predicted to last Year Yield """
                    # fname = f"{self.country}_{self.crop}_{time_period}_{year}_ratio_last_year_yield.png"
                    # plot.plot_map(
                    #     self.dg,  # dataframe containing adm1 name and polygon
                    #     df_time_period,  # dataframe containing information that will be mapped
                    #     merge_col="Country Region",  # Column on which to merge
                    #     name_country=countries,  # Plot global map
                    #     name_col="Ratio Last Year",  # Which column to plot
                    #     dir_out=self.plot_dir / str(year),  # Output directory
                    #     fname=fname,  # Output file name
                    #     label=f"Ratio Last Year to {self.predicted}\n{self.crop.title()}, {time_period} {year}",
                    #     vmin=df_time_period["Ratio Last Year"].min(),
                    #     vmax=df_time_period["Ratio Last Year"].max(),
                    #     cmap=pal.scientific.sequential.Bamako_20_r,
                    #     series="sequential",
                    #     show_bg=False,
                    #     annotate_regions=True,
                    #     annotate_region_column=annotate_region_column,
                    #     loc_legend="lower left",
                    # )

                    # Area
                    # breakpoint()
                    if df_time_period["Area (ha)"].notna().all():
                        fname = f"{self.country}_{self.crop}_{model}_{year}_area.png"
                        plot.plot_map(
                            self.dg,  # dataframe containing adm1 name and polygon
                            df_time_period,  # dataframe containing information that will be mapped
                            merge_col="Country Region",  # Column on which to merge
                            name_country=countries,  # Plot global map
                            name_col="Area (ha)",  # Which column to plot
                            dir_out=dir_maps / self.country / str(year),  # Output directory
                            fname=fname,  # Output file name
                            label=f"Area (ha)\n{self.crop.title()}, {time_period}",
                            vmin=df_time_period["Area (ha)"].min(),
                            vmax=df_time_period["Area (ha)"].max(),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",

                            annotate_regions=self.annotate_regions,
                            loc_legend="lower left",
                        )

    def plot_metric(self, df, metric="$r^2$"):
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax = sns.lineplot(data=df, x="Date", y=metric, ax=ax)  # "$r^2$"
            ax.set_xlabel("")
            ax.set_ylabel(metric)
            plt.xticks(rotation=0)
            plt.tight_layout()

            # If metric is $r^2$ or NSE, do not plot values below 0
            if metric in ["$r^2$", "Nash-Sutcliffe Efficiency"]:
                plt.ylim(0, 1)

            # Replace \n in metric
            metric = metric.replace("\n", " ")
            fname = f"{self.country}_{self.crop}_{metric}.png"

            plt.savefig(self.dir_country_plots / fname, dpi=250)
            plt.close()

    def execute(self):
        self.dir_country_plots = self.dir_plots / self.country
        os.makedirs(self.dir_country_plots, exist_ok=True)
        self.query()
        df = self.preprocess()
        self.analyze()

        return df

    def get_config_data(self):
        try:
            with sqlite3.connect(self.db_path) as con:
                # Find names of all tables starting with 'config'
                query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'config%'"
                df = pd.read_sql_query(query, con)

                if df.empty:
                    raise ValueError("No configuration tables found")

                # Extract datetime from the table names
                re = r"(\d{4} \d{2}:\d{2})$"
                df["datetime"] = pd.to_datetime(
                    df["name"].str.extract(re)[0], format="%Y %H:%M"
                )

                # Sort the DataFrame by datetime in descending order and get the latest config file
                latest_config = df.sort_values(by="datetime", ascending=False).iloc[0][
                    "name"
                ]

                self.logger.info("=====================================")
                self.logger.info(f"\t{latest_config}")
                self.logger.info("=====================================")
                # Read the latest config file
                query = f"SELECT * FROM {latest_config}"
                self.df_config = pd.read_sql_query(query, con)
        except Exception as e:
            self.logger.error(f"Failed to get configuration data: {e}")
            self.df_config = None

    def setup(self):
        """

        Args:
            country:
            crop:
            model:

        Returns:

        """
        self.dict_config = {}

        if self.df_config is None:
            self.logger.error("No configuration data available — run the ML runner first to populate the database.")
            return

        self.observed = "Observed Yield (tn per ha)"
        self.predicted = "Predicted Yield (tn per ha)"

        # Get the ML section
        df_ml = self.df_config[self.df_config["Section"] == "ML"]

        self.countries = ast.literal_eval(
            df_ml[df_ml["Option"] == "countries"]["Value"].values[0]
        )
        all_shapefiles = []
        pool_countries = False
        pool_countries_rows = df_ml[df_ml["Option"] == "pool_countries"]
        if not pool_countries_rows.empty:
            pool_countries = pool_countries_rows["Value"].values[0].lower() in ("true", "1", "yes")

        for country in self.countries:
            df = self.df_config[self.df_config["Section"] == country]

            method = df[df["Option"] == "method"]["Value"].values[0]
            crops = ast.literal_eval(df[df["Option"] == "crops"]["Value"].values[0])
            models = ast.literal_eval(df[df["Option"] == "models"]["Value"].values[0])
            admin_zone = df[df["Option"] == "admin_level"]["Value"].values[0]
            name_shapefile = df[df["Option"] == "boundary_file"]["Value"].values[0]

            for crop in crops:
                # Does a table with the name {country}_{crop} exist in the database?
                table = f"{country}_{crop}"
                if self.table_exists(self.db_path, table):
                    self.dict_config[f"{country}_{crop}"] = {
                        "method": method,
                        "crops": crop,
                        "models": models,
                        "admin_zone": admin_zone,
                        "name_shapefile": name_shapefile,
                    }

            # Load this country's shapefile
            shp_file = self.parser.get(country, "boundary_file")
            dg_country = gpd.read_file(
                self.dir_boundary_files / shp_file,
                engine="pyogrio",
            )

            # Rename columns using config-driven mapping
            from geoprepare.georegion import get_boundary_col_mapping
            rename = get_boundary_col_mapping(self.parser, shp_file)
            # Drop columns that would create duplicates after rename
            # (e.g. shapefile has both name0 and ADM0_NAME; renaming name0→ADM0_NAME would duplicate)
            targets = set(rename.values())
            sources = set(rename.keys())
            conflicting = [c for c in dg_country.columns if c in targets and c not in sources]
            if conflicting:
                dg_country = dg_country.drop(columns=conflicting)
            dg_country = dg_country.rename(columns=rename)

            if "ADM0_NAME" not in dg_country.columns:
                dg_country.loc[:, "ADM0_NAME"] = country.title().replace("_", " ")

            all_shapefiles.append(dg_country)

        # Check for pooled tables (pooled_{crop})
        if pool_countries:
            all_crops = set()
            for country in self.countries:
                df = self.df_config[self.df_config["Section"] == country]
                crops = ast.literal_eval(df[df["Option"] == "crops"]["Value"].values[0])
                all_crops.update(crops)

            # Use first country's config for shared settings
            df_first = self.df_config[self.df_config["Section"] == self.countries[0]]
            first_method = df_first[df_first["Option"] == "method"]["Value"].values[0]
            first_models = ast.literal_eval(df_first[df_first["Option"] == "models"]["Value"].values[0])
            first_admin = df_first[df_first["Option"] == "admin_level"]["Value"].values[0]
            first_shp = df_first[df_first["Option"] == "boundary_file"]["Value"].values[0]

            for crop in all_crops:
                table = f"pooled_{crop}"
                if self.table_exists(self.db_path, table):
                    self.dict_config[f"pooled_{crop}"] = {
                        "method": first_method,
                        "crops": crop,
                        "models": first_models,
                        "admin_zone": first_admin,
                        "name_shapefile": first_shp,
                    }

        # Concatenate all country shapefiles for consolidated maps
        self.dg = pd.concat(all_shapefiles, ignore_index=True)
        self.annotate_regions = self.parser.getboolean(self.countries[-1], "annotate_regions", fallback=False)

        # Create a new column called Country Region that is the concatenation of ADM0_NAME and ADM1_NAME
        # however if ADM2_NAME is not null, then it is the concatenation of ADM0_NAME and ADM2_NAME
        self.dg["Country Region"] = self.dg["ADM0_NAME"]
        self.dg["Country Region"] = self.dg["Country Region"].str.cat(
            self.dg["ADM1_NAME"], sep=" "
        )
        if "ADM2_NAME" in self.dg.columns:
            self.dg.loc[self.dg["ADM2_NAME"].notna(), "Country Region"] = (
                self.dg["ADM0_NAME"] + " " + self.dg["ADM2_NAME"]
            )
        # Make it lower case
        self.dg["Country Region"] = (
            self.dg["Country Region"].str.lower().replace("_", " ")
        )


@dataclass
class RegionalMapper(Geoanalysis):
    path_config_files: List[Path] = field(default_factory=list)
    logger: log = None
    parser: ConfigParser = field(default_factory=ConfigParser)

    def __post_init__(self):
        # Call the parent class constructor
        super().__post_init__()
        self.get_config_data()
        self.setup()

    def map_regional(self):
        """Main function to read data and generate plots."""
        self.read_data()

        self.clean_data()
        if not self.df_regional.empty and not self.df_regional_by_year.empty:
            self.crop = self.df_regional["Crop"].iloc[0].lower()
            self.plot_heatmap()
            self.plot_kde()
            self.plot_mape_map()
            self.plot_mape_by_year()

    def read_data(self):
        """Read data from the database."""
        con = sqlite3.connect(self.db_path)

        query = "SELECT * FROM regional_metrics"
        try:
            self.df_regional = pd.read_sql_query(query, con)
        except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
            self.logger.error(f"Failed to read data from regional_metrics: {e}")
            self.df_regional = pd.DataFrame()

        query = "SELECT * FROM regional_metrics_by_year"
        try:
            self.df_regional_by_year = pd.read_sql_query(query, con)
        except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
            self.logger.error(f"Failed to read data from regional_metrics_by_year: {e}")
            self.df_regional_by_year = pd.DataFrame()

        con.close()

    def clean_data(self):
        """Clean and format the data."""
        if not self.df_regional.empty:
            self.df_regional["Country"] = (
                self.df_regional["Country"].str.replace("_", " ").str.title()
            )
            self.df_regional["Model"] = self.df_regional["Model"].str.title()

    def plot_heatmap(self):
        """Generate heatmaps of MAPE bins vs. % total area bins."""
        models = self.df_regional["Model"].unique()
        for model in models:
            df_model = self.df_regional[self.df_regional["Model"] == model]

            # HACK: Drop rows where '% of total Area (ha)' is less than 1% and Mean Absolute Percentage Error is > 50%
            # or where the Mean Absolute Percentage Error is greater than 50% if the '% of total Area (ha)' is greater than 1%
            df_tmp = df_model[
                (df_model["% of total Area (ha)"] < 0.5)
                & (df_model["Mean Absolute Percentage Error"] > 100)
            ]

            df_model = df_model.drop(df_tmp.index)
            bin_edges = np.linspace(0, df_model["% of total Area (ha)"].max() + 1, 6)
            df_model["Area Bins"] = pd.cut(
                df_model["% of total Area (ha)"], bins=bin_edges, precision=0
            )
            df_model["MAPE Bins"] = pd.cut(
                df_model["Mean Absolute Percentage Error"],
                bins=5,
                right=False,
                precision=1,
            )
            area_mape_counts = (
                df_model.groupby(["Area Bins", "MAPE Bins"])
                .size()
                .unstack(fill_value=0)
            )
            self._plot_heatmap(area_mape_counts, model)

    def _plot_heatmap(self, area_mape_counts, model):
        """
        Plot heatmap helper function
        Args:
            area_mape_counts:
            model:

        Returns:

        """
        plt.figure(figsize=(10, 8))

        ax = sns.heatmap(
            area_mape_counts,
            annot=True,
            square=True,
            cmap=pal.scientific.sequential.Bamako_20_r.mpl_colormap,
            fmt="d",
        )
        for text in ax.texts:
            if text.get_text() == "0":
                text.set_text("")
                text.set_color("white")
        plt.ylabel("% of Total Area (ha) Bins")
        plt.xlabel("MAPE Bins")
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        ax.invert_yaxis()

        plt.tight_layout()
        plt.savefig(self.dir_plots / f"heatmap_{model}_{self.crop}.png", dpi=250)
        plt.close()

    def plot_kde(self):
        """Generate KDE plots of MAPE for each country."""
        models = self.df_regional["Model"].unique()

        for model in models:
            df_model = self.df_regional[self.df_regional["Model"] == model]

            # HACK: Drop rows where '% of total Area (ha)' is less than 1% and Mean Absolute Percentage Error is > 50%
            # or where the Mean Absolute Percentage Error is greater than 50% if the '% of total Area (ha)' is greater than 1%
            df_tmp = df_model[
                (df_model["% of total Area (ha)"] < 0.5)
                & (df_model["Mean Absolute Percentage Error"] > 100)
            ]

            df_model = df_model.drop(df_tmp.index)

            with plt.style.context("science"):
                plt.figure(figsize=(12, 8))
                for label, group_data in df_model.groupby("Country"):
                    sns.histplot(
                        group_data["Mean Absolute Percentage Error"],
                        label=label,
                    )

                # Plot a dashed gray line at x=20
                plt.axvline(x=20, color="gray", linestyle="--")

                plt.minorticks_on()
                plt.xlabel("Mean Absolute Percentage Error (%)")
                plt.ylabel("Frequency")
                plt.legend(title="Country", title_fontsize="16")

                # Adding the title at the top-right corner
                # plt.text(
                #     0.95, 0.95,  # Coordinates in axes fraction
                #     f"Model: {model}",
                #     transform=plt.gca().transAxes,
                #     fontsize=14,
                #     verticalalignment="top",
                #     horizontalalignment="right",
                #     bbox=dict(facecolor="white", alpha=0.6, edgecolor="none")
                # )

                plt.tight_layout()
                plt.savefig(
                    self.dir_plots / f"histogram_region_{model}_{self.crop}.png", dpi=250
                )
                plt.close()

    def plot_mape_map(self):
        """Plot the map of MAPE."""
        self.df_regional["Country Region"] = (
            self.df_regional["Country"].str.lower().str.replace("_", " ")
            + " "
            + self.df_regional["Region"].str.lower()
        )
        models = self.df_regional["Model"].unique()

        for model in models:
            df_model = self.df_regional[self.df_regional["Model"] == model]

            # HACK: Drop rows where '% of total Area (ha)' is less than 1% and Mean Absolute Percentage Error is > 50%
            # or where the Mean Absolute Percentage Error is greater than 50% if the '% of total Area (ha)' is greater than 1%
            df_tmp = df_model[
                (df_model["% of total Area (ha)"] < 0.5)
                & (df_model["Mean Absolute Percentage Error"] > 100)
            ]

            df_model = df_model.drop(df_tmp.index)

            col = "Mean Absolute Percentage Error"
            # Blank out MAPE scores above 100% so they appear empty on the map
            df_model = df_model.copy()
            df_model.loc[df_model[col] > 100, col] = np.nan
            countries = df_model["Country"].unique().tolist()
            countries = [country.title().replace("_", " ") for country in countries]
            crop = df_model["Crop"].unique()[0].title().replace("_", " ")
            df = df_model[df_model["Country"].isin(countries)]
            self.dg = self.dg[self.dg["ADM0_NAME"].isin(countries)]

            fname = f"map_{self.crop}_{df_model['Model'].iloc[0]}_mape.png"
            plot.plot_map(
                self.dg,
                df,
                merge_col="Country Region",
                name_country=countries,
                name_col=col,
                dir_out=self.dir_maps,
                fname=fname,
                label="MAPE (%)",
                vmin=df[col].min(),
                vmax=df[col].max(),
                cmap=pal.scientific.sequential.Bamako_20_r,
                series="sequential",
                annotate_regions=self.annotate_regions,
                loc_legend="lower left",
            )

    def plot_mape_by_year(self):
        """Compute MAPE by year and plot using a bar chart."""
        # Compute the Mean Absolute Percentage Error (MAPE) by year
        mape_by_year = (
            self.df_regional_by_year.groupby("Harvest Year")[
                "Mean Absolute Percentage Error"
            ]
            .mean()
            .reset_index()
        )

        # Plot MAPE by year
        with plt.style.context("science"):
            plt.figure(figsize=(10, 6))
            sns.barplot(
                x="Harvest Year", y="Mean Absolute Percentage Error", data=mape_by_year
            )
            # Draw a dashed gray line at y=20
            plt.axhline(y=20, color="gray", linestyle="--")

            plt.xlabel("")
            plt.ylabel("Mean Absolute Percentage Error (%)")
            plt.xticks(rotation=0)

            plt.tight_layout()
            plt.savefig(self.dir_plots / f"bar_mape_by_year_{self.crop}.png", dpi=250)
            plt.close()


def run(path_config_files=[Path("../config/geocif.txt")]):
    logger, parser = log.setup_logger_parser(path_config_files)

    obj = Geoanalysis(path_config_files, logger, parser)
    obj.get_config_data()
    obj.setup()

    # Build and display run summary
    country_details = {}
    for key, value in obj.dict_config.items():
        crop = value["crops"]
        country = key.replace(f"_{crop}", "")
        info = country_details.setdefault(country, {"crops": set(), "models": set(), "method": value["method"]})
        info["crops"].add(crop)
        info["models"].update(value["models"])

    # Extract forecast_seasons from stored config
    # ConfigParser.sections() excludes DEFAULT, so DEFAULT options are stored
    # under each section — search across all sections for forecast_seasons
    forecast_seasons = None
    if obj.df_config is not None:
        fs_rows = obj.df_config[obj.df_config["Option"] == "forecast_seasons"]
        if not fs_rows.empty:
            try:
                forecast_seasons = ast.literal_eval(fs_rows["Value"].values[0])
            except Exception:
                pass

    params = [("Countries", obj.countries)]
    for country, info in country_details.items():
        params.append((f"  {country} crops", sorted(info["crops"])))
        params.append((f"  {country} models", sorted(info["models"])))
        params.append((f"  {country} method", info["method"]))
    if forecast_seasons:
        params.append(("Forecast seasons", f"{forecast_seasons[0]}-{forecast_seasons[-1]} ({len(forecast_seasons)} years)"))
    for cfg in path_config_files:
        params.append(("Config file", str(Path(cfg).resolve())))
    params.append(("Database", str(obj.db_path)))
    params.append(("Output dir", str(obj.dir_analysis)))
    params.append(("Total combinations", str(len(obj.dict_config))))
    utils.display_run_summary("GeoCIF Analysis Runner", params, wait=20)

    # Copy config files to analysis directory for reproducibility
    for cfg in path_config_files:
        cfg = Path(cfg)
        if cfg.is_file():
            shutil.copy2(cfg, obj.dir_config / cfg.name)

    """ Loop over each country, crop, model combination in dict_config """
    frames = []
    for country_crop, value in obj.dict_config.items():
        obj.crop = value["crops"]
        # to get country, remove obj.crops from country_crop
        obj.country = country_crop.replace(f"_{obj.crop}", "")

        obj.admin_zone = value["admin_zone"]
        obj.boundary_file = value["name_shapefile"]
        obj.method = value["method"]
        obj.number_lag_years = 5

        obj.table = f"{obj.country}_{obj.crop}"
        models = value["models"]
        for model in models:
            obj.model = model

            df_tmp = obj.execute()
            if df_tmp is not None and not df_tmp.empty:
                frames.append(df_tmp)

    if not frames:
        logger.warning("No data to analyze — check that the ML runner has been executed first.")
        return

    df = pd.concat(frames)

    """ For each country, plot yields, conditions, anomalies, etc. """
    obj.map(df)

    """ Map regional error metrics """
    mapper = RegionalMapper(path_config_files, logger, parser)
    mapper.map_regional()


if __name__ == "__main__":
    run()
