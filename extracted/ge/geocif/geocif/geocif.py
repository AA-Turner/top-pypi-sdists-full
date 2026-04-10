"""
geocif.py - REFACTORED VERSION

Main class for agricultural yield forecasting using climate and environmental indicators.
Refactored to improve readability, maintainability, and debuggability.
"""

import ast
import os
import traceback
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import arrow as ar
import geopandas as gp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from statsmodels.tools.tools import add_constant
from tqdm import tqdm

from geocif import logger as log
from geocif import utils
from .cid import definitions as di
from .ml import correlations, feature_engineering as fe, feature_selection as fs
from .ml import output, spatial_neighbors as sn, stages, stats, trainers, trend, xai

plt.style.use("default")

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


@dataclass
class Geocif:
    """Main class for crop yield forecasting using ML and climate data."""
    
    method: str = "dekad_r"
    group_by: List[str] = field(
        default_factory=lambda: ["Index", "Country", "Region", "Crop", "Season"]
    )
    metrics: List[str] = field(default_factory=lambda: ["$r^2$", "RMSE", "MAE", "MAPE"])
    logger: log = None
    parser: ConfigParser = field(default_factory=ConfigParser)
    project_name: str = "geocif"

    def __post_init__(self):
        """Initialize paths, dates, and configuration."""
        self._initialize_directories()
        self._initialize_dates()
        self._initialize_country_data()
        self._load_configuration()
        self._initialize_ml_configuration()
        self._setup_feature_dictionaries()

    # ============================================================================
    # INITIALIZATION METHODS
    # ============================================================================

    def _initialize_directories(self):
        """Setup directory paths."""
        self.dir_output = Path(self.parser.get("PATHS", "dir_output")) / self.project_name
        self.dir_boundary_files = Path(self.parser.get("PATHS", "dir_boundary_files"))
        self.dir_production_statistics = Path(self.parser.get("PATHS", "dir_production_statistics"))

        self.dir_ml = self.dir_output / "ml"
        self.dir_db = self.dir_ml / "db"

        os.makedirs(self.dir_ml, exist_ok=True)
        os.makedirs(self.dir_db, exist_ok=True)

    def _initialize_dates(self):
        """Setup date-related attributes."""
        self._date = ar.utcnow().to("America/New_York")
        self.today = self._date.format("MMMM_DD_YYYY")
        self.today_year = self._date.year
        self.today_doy = int(self._date.format("DDD"))
        self.today_full = self._date.format("MMMM_DD_YYYY_HH_mm")

    def _initialize_country_data(self):
        """Initialize country/crop specific attributes."""
        self.country: Optional[str] = None
        self.crop: Optional[str] = None
        self.forecast_season: Optional[int] = None
        self.all_stages: list = []
        self.all_seasons: list = []
        self.all_seasons_with_yield: list = []
        self.model_names: list = []
        self.feature_names: list = []
        self.selected_features: list = []
        self.df_forecast = pd.DataFrame()

    def _load_configuration(self):
        """Load configuration from config file."""
        # Logging
        self.log_level = self.parser.get("LOGGING", "log_level")
        
        # Default settings
        self.method = self.parser.get("DEFAULT", "method")
        self.db_forecasts = self.parser.get("DEFAULT", "db")
        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        if self.parser.has_option("DEFAULT", "do_parallel_ml"):
            self.do_parallel = self.parser.getboolean("DEFAULT", "do_parallel_ml")
        else:
            self.do_parallel = False
        self.update_input_file = self.parser.getboolean("DEFAULT", "update_input_file")
        self.correlation_plots = self.parser.getboolean("DEFAULT", "correlation_plots")
        self.national_correlation = self.parser.getboolean("DEFAULT", "national_correlation")
        self.plot_map_for_correlation_plot = self.parser.getboolean(
            "DEFAULT", "plot_map_for_correlation_plot"
        )
        self.correlation_plot_groupby = self.parser.get("DEFAULT", "correlation_plot_groupby")
        self.run_ml = self.parser.getboolean("DEFAULT", "run_ml")
        self.use_cumulative_features = self.parser.getboolean("DEFAULT", "use_cumulative_features")

    def _initialize_ml_configuration(self):
        """Load ML-specific configuration."""
        self.model_type = self.parser.get("ML", "model_type")
        self.classify_target = self.parser.getboolean("ML", "classify_target")
        self.number_classes = self.parser.getint("ML", "number_classes")
        self.target = self.parser.get("ML", "target")
        self.rename_target = self.parser.getboolean("ML", "rename_target")
        self.new_name_target = self.parser.get("ML", "new_name_target")
        self.fraction_simulate = self.parser.getint("ML", "fraction_simulate")
        
        self.analogous_year_yield_as_feature = self.parser.getboolean(
            "ML", "analogous_year_yield_as_feature"
        )
        self.correlation_threshold = self.parser.getfloat("ML", "correlation_threshold")
        self.correlation_metric = self.parser.get("ML", "correlation_metric", fallback="both")
        self.include_lat_lon_as_feature = self.parser.getboolean("ML", "include_lat_lon_as_feature")
        self.spatial_autocorrelation = self.parser.getboolean("ML", "spatial_autocorrelation")
        self.sa_method = self.parser.get("ML", "sa_method")
        self.last_year_yield_as_feature = self.parser.getboolean("ML", "last_year_yield_as_feature")
        self.panel_model = self.parser.getboolean("ML", "panel_model")
        self.panel_model_region = self.parser.get("ML", "panel_model_region")
        self.use_outlook_as_feature = self.parser.getboolean("ML", "use_outlook_as_feature")
        self.use_single_time_period_as_feature = self.parser.getboolean(
            "ML", "use_single_time_period_as_feature"
        )
        self.lag_yield_as_feature = self.parser.getboolean("ML", "lag_yield_as_feature")
        self.number_median_years = self.parser.getint("ML", "median_years")
        self.median_yield_as_feature = self.parser.getboolean("ML", "median_yield_as_feature")
        self.median_area_as_feature = self.parser.getboolean("ML", "median_area_as_feature")
        self.number_lag_years = self.parser.getint("ML", "lag_years")
        self.cluster_strategy = self.parser.get("ML", "cluster_strategy")
        self.feature_selection = self.parser.get("ML", "feature_selection")
        # Valid values: none, SHAP, stabl, feature_engine, mrmr, RFECV, lasso,
        #   BorutaPy, Leshy, PowerShap, BorutaShap, Genetic, RFE, multi, gOMP
        self.check_yield_trend = self.parser.getboolean("ML", "check_yield_trend")
        self.detrend_method = self.parser.get("ML", "detrend_method") if self.parser.has_option("ML", "detrend_method") else "gaussian"
        self.run_latest_time_period = self.parser.getboolean("ML", "run_latest_time_period")
        self.run_every_time_period = self.parser.get("ML", "run_every_time_period")
        self.cat_features: list = ast.literal_eval(self.parser.get("ML", "cat_features"))
        self.use_spatial_neighbors = (
            self.parser.getboolean("ML", "use_spatial_neighbors")
            if self.parser.has_option("ML", "use_spatial_neighbors") else False
        )
        self.spatial_neighbor_method = (
            self.parser.get("ML", "spatial_neighbor_method")
            if self.parser.has_option("ML", "spatial_neighbor_method") else "knn"
        )
        self.spatial_neighbor_k = (
            self.parser.getint("ML", "spatial_neighbor_k")
            if self.parser.has_option("ML", "spatial_neighbor_k") else 5
        )
        self.remove_last_month = (
            self.parser.getboolean("ML", "remove_last_month")
            if self.parser.has_option("ML", "remove_last_month") else False
        )

    def _setup_feature_dictionaries(self):
        """Setup feature dictionaries and database paths."""
        self.target_bins = {}
        
        self.fixed_columns: list = [
            "Country", "Region", "Crop", "Area", "Season", "Harvest Year",
        ]
        
        self.target: str = "Yield (tn per ha)"
        self.statistics_columns: list = ["Area (ha)", "Production (tn)"]
        
        if self.model_type == "REGRESSION":
            self.target_column = (
                f"Detrended {self.target}" if self.check_yield_trend else self.target
            )
        elif self.model_type == "CLASSIFICATION":
            self.target_column = self.target_class
        
        self.combined_dict = {
            **di.dict_indices,
            **di.dict_ndvi,
            **di.dict_gcvi,
            **di.dict_esi4wk,
            **di.dict_hindex,
            **di.dict_aef,
            **di.dict_fldas,
        }
        
        self.combined_keys = list(self.combined_dict.keys())
        
        # Update paths
        self.dir_analysis = self.dir_ml / "analysis" / self.today
        
        os.makedirs(self.dir_analysis, exist_ok=True)
        
        self.db_path = self.dir_db / self.db_forecasts

    # ============================================================================
    # SETUP METHODS
    # ============================================================================

    def setup(self, forecast_season: int, model: str):
        """
        Setup for a specific country/crop/season/model combination.

        Args:
            forecast_season: Year to forecast
            model: Model name to use
        """
        self._setup_basic_parameters(forecast_season, model)
        self._validate_model_configuration()
        self._setup_model_specific_flags()
        self._setup_seasons_and_stages()
        self._setup_geodata()

    def setup_pooled(self, countries: list, forecast_season: int, model: str):
        """Setup for pooled cross-country execution.

        Args:
            countries: List of country names being pooled
            forecast_season: Year to forecast
            model: Model name to use
        """
        self.countries_pooled = countries
        self._config_country = countries[0]
        self._setup_basic_parameters(forecast_season, model)
        self._validate_model_configuration()
        self._setup_model_specific_flags()
        self._setup_seasons_and_stages()
        self._setup_geodata_pooled(countries)

    def _setup_basic_parameters(self, forecast_season: int, model: str):
        """Setup basic parameters for the run."""
        _str = f"{self.country} {self.crop} {model} {forecast_season}"
        self.logger.info(f"Setup {_str}")

        self.forecast_season = forecast_season
        self.model_name = model
        self.experiment_name = self.parser.get("ML", "experiment_name")
        self.ml_model = self.parser.getboolean(self.model_name, "ML_model")
        self.select_cei_by = self.parser.get(self.model_name, "select_cei_by")
        self.use_ceis = ast.literal_eval(self.parser.get(self.model_name, "use_ceis"))
        # In pooled mode, use _config_country for per-country config lookups
        _cc = getattr(self, '_config_country', self.country)
        self.model_names = ast.literal_eval(self.parser.get(_cc, "models"))
        self.optimize = self.parser.getboolean(_cc, "optimize")
        self.fraction_loocv = self.parser.getfloat(_cc, "fraction_loocv")
        self.all_seasons = self.df_inputs["Harvest Year"].unique()

    def _validate_model_configuration(self):
        """Validate model type and classification settings."""
        if self.model_type == "REGRESSION" and self.classify_target:
            raise ValueError("Model type is regression but classify_target is True")
        elif self.model_type == "CLASSIFICATION" and not self.classify_target:
            raise ValueError("Model type is classification but classify_target is False")

    def _setup_model_specific_flags(self):
        """Setup model-specific flags based on model type and name."""
        if self.model_type == "CLASSIFICATION":
            self._setup_classification_flags()
        elif self.model_type == "REGRESSION":
            self._setup_regression_flags()

    def _setup_classification_flags(self):
        """Setup flags for classification models."""
        self.do_xai = False
        self.alpha = self.parser.getfloat("ML", "alpha")
        self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
        self.estimate_ci_for_all = self.parser.getboolean("ML", "estimate_ci_for_all")
        self.ci_method = self.parser.get("ML", "ci_method", fallback="crepes")
        self.check_yield_trend = False

        if self.model_name == "ngboost":
            self.cat_features = [col for col in self.cat_features if col != "Region"]

    def _setup_regression_flags(self):
        """Setup flags for regression models."""
        if not self.ml_model or self.model_name in ["linear", "gam", "merf", "cubist"]:
            self._setup_simple_regression_flags()
        elif self.model_name.startswith("cumulative_"):
            self._setup_cumulative_flags()
        elif self.model_name in ["tabpfn", "desreg", "tabicl"]:
            self._setup_tabular_flags()
        elif self.model_name in ["oblique", "ydf"]:
            self._setup_tree_flags()
        elif self.model_name == "ngboost":
            self._setup_ngboost_flags()
        else:
            self._setup_standard_ml_flags()

    def _setup_simple_regression_flags(self):
        """Flags for simple regression models."""
        self.do_xai = False
        self.estimate_ci = False
        self.check_yield_trend = False
        self.estimate_ci_for_all = False

    def _setup_cumulative_flags(self):
        """Flags for cumulative models."""
        self.correlation_plots = False
        self.lag_yield_as_feature = False
        self.median_yield_as_feature = False
        self.median_area_as_feature = False
        self.analogous_year_yield_as_feature = False
        self.last_year_yield_as_feature = False
        self.include_lat_lon_as_feature = False
        self.do_xai = False
        self.estimate_ci = False
        self.estimate_ci_for_all = False
        self.check_yield_trend = True
        self.cluster_strategy = "single"
        self.use_spatial_neighbors = False
        self.select_cei_by = "Index"
        self.use_cumulative_features = True

    def _setup_tabular_flags(self):
        """Flags for tabular models."""
        self.do_xai = self.parser.getboolean("ML", "do_xai", fallback=False)
        self.alpha = self.parser.getfloat("ML", "alpha")
        self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
        self.estimate_ci_for_all = self.parser.getboolean("ML", "estimate_ci_for_all")
        self.ci_method = self.parser.get("ML", "ci_method", fallback="crepes")
        self.cat_features = [col for col in self.cat_features if col != "Region"]

    def _setup_tree_flags(self):
        """Flags for tree-based models."""
        self.do_xai = False
        self.estimate_ci = False
        self.cat_features = [col for col in self.cat_features if col != "Region"]

    def _setup_ngboost_flags(self):
        """Flags for NGBoost."""
        self.do_xai = False
        self.alpha = self.parser.getfloat("ML", "alpha")
        self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
        self.estimate_ci_for_all = self.parser.getboolean("ML", "estimate_ci_for_all")
        self.ci_method = self.parser.get("ML", "ci_method", fallback="crepes")
        self.cat_features = [col for col in self.cat_features if col != "Region"]

    def _setup_standard_ml_flags(self):
        """Flags for standard ML models with full features."""
        self.do_xai = self.parser.getboolean("ML", "do_xai")
        self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
        self.estimate_ci_for_all = self.parser.getboolean("ML", "estimate_ci_for_all")
        self.alpha = self.parser.getfloat("ML", "alpha")
        self.ci_method = self.parser.get("ML", "ci_method", fallback="crepes")
        self.check_yield_trend = self.parser.getboolean("ML", "check_yield_trend")

    def _setup_seasons_and_stages(self):
        """Setup seasons and simulation stages."""
        self.all_seasons_with_yield = self.df_inputs[
            self.df_inputs[self.target].notna()
        ]["Harvest Year"].unique()
        
        if self.method.endswith("_r"):
            self._setup_reverse_stages()
        else:
            raise NotImplementedError(f"Method {self.method} not implemented")
        
        self._filter_current_month_stages()
        self._create_simulation_stages()

    def _setup_reverse_stages(self):
        """Setup stages for reverse methods."""
        if self.forecast_season == self.today_year:
            mask = self.df_inputs["Harvest Year"] == self.forecast_season
            self.all_stages = self.df_inputs[mask]["Stage_ID"].unique()
        else:
            self.all_stages = self.df_inputs["Stage_ID"].unique()

    def _filter_current_month_stages(self):
        """Filter out current month stages for real-time forecasting."""
        if self.forecast_season == self.today_year:
            current_month = ar.utcnow().month
            self.all_stages = [
                elem for elem in self.all_stages
                if not elem.startswith(str(current_month))
            ]

    def _create_simulation_stages(self):
        """Create simulation stages from stage IDs."""
        self.simulation_stages = [
            np.array([int(stage) for stage in s.split("_")]) 
            for s in self.all_stages
        ]

    def _setup_geodata(self):
        """Setup geodata (shapefiles) for the country."""
        self.name_shapefile = self.parser.get(self.country, "boundary_file")
        self.admin_zone = self.parser.get(self.country, "admin_level")
        
        self.dg = gp.read_file(
            self.dir_boundary_files / self.name_shapefile,
            engine="pyogrio",
        )
        
        self._standardize_geodata_columns()
        self._add_country_region_column()
        self._filter_to_country()

    def _standardize_geodata_columns(self):
        """Standardize column names in geodata using config-driven mapping."""
        from geoprepare.georegion import get_boundary_col_mapping

        rename = get_boundary_col_mapping(self.parser, self.name_shapefile)
        # Fix Tanzania naming before rename
        adm0_src = next((k for k, v in rename.items() if v == "ADM0_NAME"), "ADM0_NAME")
        if adm0_src in self.dg.columns:
            self.dg[adm0_src] = self.dg[adm0_src].replace(
                "Tanzania", "United Republic of Tanzania"
            )

        # Drop columns that would create duplicates after rename
        # (e.g. shapefile has both name0 and ADM0_NAME; renaming name0→ADM0_NAME would duplicate)
        targets = set(rename.values())
        sources = set(rename.keys())
        conflicting = [c for c in self.dg.columns if c in targets and c not in sources]
        if conflicting:
            self.dg = self.dg.drop(columns=conflicting)

        self.dg = self.dg.rename(columns=rename)

    def _add_country_region_column(self):
        """Add Country Region column for merging."""
        if self.admin_zone == "admin_2" and "ADM2_NAME" in self.dg.columns:
            self.dg["Country Region"] = self.dg["ADM0_NAME"] + " " + self.dg["ADM2_NAME"]
        else:
            self.dg["Country Region"] = self.dg["ADM0_NAME"] + " " + self.dg["ADM1_NAME"]

        self.dg["Country Region"] = self.dg["Country Region"].str.lower()

    def _filter_to_country(self):
        """Filter geodata to current country."""
        self.dg_country = self.dg[
            self.dg["ADM0_NAME"].str.lower().str.replace(" ", "_") == self.country
        ]
        self.dg_country = self.dg_country.drop_duplicates(subset=["Country Region"])

    def _setup_geodata_pooled(self, countries: list):
        """Load and concatenate shapefiles for multiple countries."""
        from geoprepare.georegion import get_boundary_col_mapping

        all_gdf = []
        for country in countries:
            shp_file = self.parser.get(country, "boundary_file")
            dg = gp.read_file(
                self.dir_boundary_files / shp_file, engine="pyogrio"
            )
            rename = get_boundary_col_mapping(self.parser, shp_file)
            adm0_src = next(
                (k for k, v in rename.items() if v == "ADM0_NAME"), "ADM0_NAME"
            )
            if adm0_src in dg.columns:
                dg[adm0_src] = dg[adm0_src].replace(
                    "Tanzania", "United Republic of Tanzania"
                )
            targets = set(rename.values())
            sources = set(rename.keys())
            conflicting = [
                c for c in dg.columns if c in targets and c not in sources
            ]
            if conflicting:
                dg = dg.drop(columns=conflicting)
            dg = dg.rename(columns=rename)
            all_gdf.append(dg)

        self.dg = pd.concat(all_gdf, ignore_index=True)
        self.admin_zone = self.parser.get(countries[0], "admin_level")
        self._add_country_region_column()
        # Keep all countries (don't filter to single country)
        self.dg_country = self.dg.drop_duplicates(subset=["Country Region"])

    # ============================================================================
    # DATA READING AND PREPARATION
    # ============================================================================

    def read_data(self, country: str, crop: str, season: int):
        """
        Read and prepare input data for a country/crop/season.
        
        Args:
            country: Country name
            crop: Crop name
            season: Season/year
        """
        self.logger.info(f"Reading data for {country} {crop} {season}")
        
        self.country = country
        self.crop = crop
        
        file_path = self._get_statistics_file_path(country, crop)
        
        if not file_path.exists() or self.update_input_file:
            try:
                self._create_statistics_file(country, crop, file_path)
            except FileNotFoundError as e:
                self.logger.warning(f"Skipping {country} {crop}: {e}")
                return
        else:
            self.df_inputs = pd.read_csv(file_path)
        
        if self.rename_target:
            self._rename_target_column()

    def _get_statistics_file_path(self, country: str, crop: str) -> Path:
        """Get path to statistics file."""
        path = utils.statistics_file_path(self.dir_output, self.method, country, crop)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _create_statistics_file(self, country: str, crop: str, file_path: Path):
        """Create statistics file by combining CEI data with yield statistics."""
        admin_zone = self.parser.get(country, "admin_level")
        country_str = country.title().replace("_", " ")
        crop_str = crop.title().replace("_", " ")
        
        _dir_country = (
            self.dir_output / "cid" / "indices" / self.method /
            admin_zone / country / crop
        )
        
        file_name = f"{country}_{crop}_s*.csv"
        all_files = list(_dir_country.glob(file_name))
        all_files = [f for f in all_files if "_2000" not in f.name]
        
        if not all_files:
            raise FileNotFoundError(
                f"No files found in {_dir_country} with pattern {file_name}"
            )
        
        self.df_inputs = pd.concat(
            (pd.read_csv(f, engine="pyarrow") 
             for f in tqdm(all_files, desc="Reading CSVs", leave=False)),
            ignore_index=True
        )
        
        self.df_inputs = stats.add_statistics(
            self.dir_production_statistics,
            self.df_inputs,
            country_str,
            crop_str,
            admin_zone,
            [self.target] + self.statistics_columns,
            self.method,
            parser=self.parser,
            label=f"{country} {crop}",
        )
        
        self.logger.info("Adding starting and ending time period for each stage")
        self.df_inputs = stages.add_stage_information(
            self.df_inputs, self.method,
            label=f"{country} {crop}",
        )
        
        self.logger.info("Writing input file to disk")
        self.df_inputs.to_csv(file_path, index=False)

    def read_data_pooled(self, countries: list, crop: str, season: int):
        """Read and concatenate data from multiple countries for the same crop.

        Args:
            countries: List of country names to pool
            crop: Crop name
            season: Season/year (unused here, kept for API symmetry)
        """
        self.logger.info(f"Reading pooled data for {countries} {crop}")
        self.crop = crop
        self.country = "pooled"
        self.countries_pooled = countries

        frames = []
        for country in countries:
            file_path = self._get_statistics_file_path(country, crop)
            if not file_path.exists() or self.update_input_file:
                try:
                    self._create_statistics_file(country, crop, file_path)
                    frames.append(self.df_inputs)
                except FileNotFoundError as e:
                    self.logger.warning(f"Skipping {country} {crop}: {e}")
                    continue
            else:
                frames.append(pd.read_csv(file_path))

        if not frames:
            self.df_inputs = None
            return

        self.df_inputs = pd.concat(frames, ignore_index=True)

        # Add disambiguated region column for use as cat feature
        self.df_inputs["Country__Region"] = (
            self.df_inputs["Country"].str.strip()
            + "__"
            + self.df_inputs["Region"].str.strip()
        )

        # Ensure Country__Region survives the pivot
        if "Country__Region" not in self.fixed_columns:
            self.fixed_columns.append("Country__Region")

        if self.rename_target:
            self._rename_target_column()

    def _rename_target_column(self):
        """Rename target column if configured."""
        self.df_inputs.rename(
            columns={self.target: self.new_name_target},
            inplace=True
        )
        self.target = self.new_name_target
        self.target_column = self.new_name_target

    # ============================================================================
    # MAIN EXECUTION PIPELINE
    # ============================================================================

    def execute(self):
        """
        Main execution pipeline - orchestrates the entire workflow.
        """
        df = self._prepare_ml_dataframe()
        df = self._add_lat_lon_to_data(df)
        
        self._run_spatial_autocorrelation_if_enabled()
        
        dict_selected_features, dict_best_cei = self._generate_correlation_plots(df)
        
        self._prepare_train_test_split(df)
        self._compute_detrended_yield()
        self._add_spatial_neighbor_features()

        if self.run_ml:
            self._execute_ml_pipeline(dict_selected_features, dict_best_cei)

    def _filter_low_production_regions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Exclude bottom-5th-pct production regions and regions with ≤3 data points."""
        if "Area (ha)" not in df.columns or self.target not in df.columns:
            return df
        counts = df.groupby("Region")[self.target].count()
        prod = df.groupby("Region").apply(
            lambda g: (g["Area (ha)"] * g[self.target]).mean()
        )
        threshold = prod.quantile(0.05)
        keep = prod.index[(prod >= threshold) & (counts > 3)]
        n_excluded = len(prod) - len(keep)
        if n_excluded:
            self.logger.info(
                f"  Region filter: excluding {n_excluded} of {len(prod)} regions "
                f"(bottom-5%-production or ≤3 observations)"
            )
        return df[df["Region"].isin(keep)].copy()

    def _prepare_ml_dataframe(self) -> pd.DataFrame:
        """Convert raw data into ML-ready format."""
        df = self._filter_by_simulation_stages()
        df = self._filter_by_cei_categories(df)
        df = self.create_ml_dataframe(df)

        if self.parser.getboolean("DEFAULT", "filter_low_production_regions", fallback=False):
            df = self._filter_low_production_regions(df)

        self._save_ml_dataframe(df)
        df[self.cat_features] = df[self.cat_features].astype("category")
        
        return df

    def _filter_by_simulation_stages(self) -> pd.DataFrame:
        """Filter data to include only simulation stages."""
        stages_list = [
            stages.convert_stage_string(s, to_array=False) 
            for s in self.simulation_stages
        ]
        mask = self.df_inputs["Stage_ID"].isin(stages_list)
        return self.df_inputs[mask]

    def _filter_by_cei_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter by selected CEI categories."""
        if "all" in self.use_ceis:
            return df
        
        if self.select_cei_by == "Type":
            return df[df["Type"].isin(self.use_ceis)]
        elif self.select_cei_by == "Index":
            return df[df["Index"].isin(self.use_ceis)]
        
        return df

    def _save_ml_dataframe(self, df: pd.DataFrame):
        """Save ML-ready dataframe to disk."""
        base = self.dir_analysis
        if self.experiment_name != "default":
            base = base / self.experiment_name / "runs"
        dir_output = (
            base / self.country / self.crop /
            self.model_name / str(self.forecast_season)
        )
        dir_output.mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.country}_{self.crop}_{self.forecast_season}.csv"
        df.to_csv(dir_output / filename, index=False)

    def _add_lat_lon_to_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add latitude/longitude columns by merging with geodata.

        If lat/lon already exist in the data (from geoprepare extraction),
        use those directly. Otherwise fall back to computing centroids from
        the admin boundary shapefile.
        """
        # If geoprepare already provided non-zero lat/lon, use them as-is
        if "lat" in df.columns and "lon" in df.columns and (df["lat"] != 0).any():
            df["Country Region"] = (
                df["Country"].astype(str) + " " + df["Region"].astype(str)
            ).str.lower()
            return df

        df["Country Region"] = (
            df["Country"].astype(str) + " " + df["Region"].astype(str)
        ).str.lower()

        cols = self._get_geodata_columns()
        self.dg_country = self.dg_country[cols].merge(
            df[["Country Region", self.correlation_plot_groupby]],
            on="Country Region",
            how="outer",
        )

        centroids = self.dg_country.to_crs(epsg=6933).centroid.to_crs(epsg=4326)
        self.dg_country["lat"] = centroids.y
        self.dg_country["lon"] = centroids.x

        df = df.merge(
            self.dg_country[["Country Region", "lat", "lon"]].drop_duplicates(),
            on="Country Region",
            how="left",
        )

        return df

    def _get_geodata_columns(self) -> List[str]:
        """Get appropriate columns based on admin zone."""
        base_cols = ["Country Region", "geometry"]

        if self.admin_zone == "admin_2" and "ADM2_NAME" in self.dg.columns:
            return base_cols + ["ADM2_NAME"]
        else:
            return base_cols + ["ADM1_NAME"]

    def _run_spatial_autocorrelation_if_enabled(self):
        """Compute spatial autocorrelation if configured."""
        if not self.spatial_autocorrelation:
            return
        
        from .ml import spatial_autocorrelation as sa
        
        kwargs = self._build_correlation_kwargs()
        sa.compute_spatial_autocorrelation(self.df_inputs, **kwargs)

    def _generate_correlation_plots(self, df: pd.DataFrame) -> Tuple[Dict, Dict]:
        """Generate correlation plots and return selected features."""
        if not self.correlation_plots:
            return {}, {}
        
        self.logger.info(f"Correlation plot for {self.country} {self.crop}")
        kwargs = self._build_correlation_kwargs()
        
        return correlations.all_correlated_feature_by_time(df, **kwargs)

    def _build_correlation_kwargs(self) -> Dict:
        """Build keyword arguments for correlation analysis."""
        return {
            "all_stages": self.all_stages,
            "target_col": self.target,
            "country": self.country,
            "crop": self.crop,
            "dir_output": (
                self.dir_analysis / self.country / self.crop / 
                self.model_name / str(self.forecast_season)
            ),
            "forecast_season": self.forecast_season,
            "method": self.method,
            "national_correlation": self.national_correlation,
            "groupby": self.correlation_plot_groupby,
            "cluster_strategy": self.cluster_strategy,
            "dg_country": self.dg_country,
            "combined_dict": self.combined_dict,
            "plot_map": self.plot_map_for_correlation_plot,
            "correlation_threshold": self.correlation_threshold,
            "correlation_metric": self.correlation_metric,
        }

    def _prepare_train_test_split(self, df: pd.DataFrame):
        """Separate data into training and testing sets."""
        df[f"{self.target}_class"] = np.nan
        
        mask = df["Harvest Year"] == self.forecast_season
        self.df_train = df[~mask].copy()
        self.df_test = df[mask].copy()
        
        self.df_train = self.df_train.dropna(subset=[self.target])

    def _compute_detrended_yield(self):
        """Compute detrended yield for each region."""
        self.df_train[f"Detrended {self.target}"] = np.nan
        self.df_train["Detrended Model"] = np.nan
        self.df_train["Detrended Model Type"] = pd.Series(np.nan, index=self.df_train.index, dtype="object")
        self.df_test[f"Detrended {self.target}"] = np.nan
        self.df_test["Detrended Model"] = np.nan
        self.df_test["Detrended Model Type"] = pd.Series(np.nan, index=self.df_test.index, dtype="object")
        self.detrend_models = {}

        groups = self.df_train.groupby("Region")

        for region_name, group in groups:
            if group.empty or not group[self.target].any():
                continue

            self._process_region_detrending(group, region_name)

    def _process_region_detrending(self, group: pd.DataFrame, region_name: str):
        """Process detrending and classification for a single region."""
        if self.check_yield_trend:
            detrended_data = trend.detrend_dataframe(
                group, column_name=self.target, model_type=self.detrend_method
            )
            self.df_train.loc[group.index, f"Detrended {self.target}"] = (
                detrended_data.detrended_series
            )
            self.df_train.loc[group.index, "Detrended Model Type"] = (
                detrended_data.model_type
            )
            if self.detrend_method == "gaussian":
                # Dicts can't be stored per-row in a DataFrame; keep in separate dict
                self.detrend_models[region_name] = detrended_data.trend_model
            else:
                self.df_train.loc[group.index, "Detrended Model"] = (
                    detrended_data.trend_model
                )
        
        # Create categorical classes
        group, new_target_column, bins = fe.classify_target(
            group, self.target, self.number_classes
        )
        self.target_bins[region_name] = bins
        self.target_class = new_target_column
        self.df_train.loc[group.index, new_target_column] = group[new_target_column]

    def _add_spatial_neighbor_features(self):
        """Build spatial neighbor graph from training data and add nbr_ features."""
        if not self.use_spatial_neighbors:
            return

        # In pooled mode, use Country__Region to avoid name collisions
        admin_col = "Country__Region" if getattr(self, 'countries_pooled', None) else "Region"

        # Prefer detrended yield for correlation if available
        detrended_col = f"Detrended {self.target}"
        yield_col_for_corr = (
            detrended_col
            if self.check_yield_trend and detrended_col in self.df_train.columns
               and self.df_train[detrended_col].notna().any()
            else self.target
        )

        self.neighbor_graph = sn.build_neighbor_graph(
            self.df_train,
            admin_col=admin_col,
            lat_col="lat",
            lon_col="lon",
            yield_col=yield_col_for_corr,
            method=self.spatial_neighbor_method,
            k=self.spatial_neighbor_k,
        )

        # Feature columns = everything except fixed, target, stats, meta
        exclude_cols = set(
            self.fixed_columns
            + self.statistics_columns
            + [
                self.target, f"{self.target}_class",
                "Region_ID", "lat", "lon", "Country Region",
                f"Detrended {self.target}", "Detrended Model",
                "Detrended Model Type",
            ]
        )
        feature_cols = [
            c for c in self.df_train.columns
            if c not in exclude_cols and not c.startswith("nbr_")
        ]

        self.df_train = sn.add_neighbor_features(
            self.df_train, self.neighbor_graph, feature_cols,
            admin_col=admin_col, year_col="Harvest Year",
            yield_col=self.target, prefix="nbr_",
        )
        self.df_test = sn.add_neighbor_features(
            self.df_test, self.neighbor_graph, feature_cols,
            admin_col=admin_col, year_col="Harvest Year",
            yield_col=self.target, prefix="nbr_",
        )

        self.logger.info(
            f"Added {len(feature_cols)} neighbor features "
            f"({self.spatial_neighbor_method}, k={self.spatial_neighbor_k})"
        )

    def _execute_ml_pipeline(self, dict_selected_features: Dict, dict_best_cei: Dict):
        """Execute the machine learning training pipeline."""
        self.logger.info(f"Running ML for {self.country} {self.crop}")
        
        setup_stages = self._get_setup_stages()
        num_regions = len(self.df_train["Region_ID"].unique())
        
        pbar = tqdm(setup_stages)
        for stage in pbar:
            pbar.set_description(f"[{self.experiment_name}] ML {self.country} {self.crop} {self.forecast_season} ({num_regions} regions, {len(setup_stages)} stages) fs={self.feature_selection} detrend={self.check_yield_trend}")
            
            try:
                self.loop_ml(stage, dict_selected_features, dict_best_cei)
            except Exception as e:
                self.logger.error(f"Error in ML loop for stage {stage}: {e}")

    def _get_setup_stages(self) -> List:
        """Determine which stages to use for ML training."""
        setup_stages = [self.simulation_stages]
        
        if self.run_latest_time_period:
            return [setup_stages[-1]]
        
        return setup_stages

    # ============================================================================
    # ML DATAFRAME CREATION
    # ============================================================================

    def create_ml_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create ML-ready dataframe from long format CEI data.
        
        Args:
            df: Input dataframe with CEI data
            
        Returns:
            Wide-format dataframe ready for ML
        """
        _str = f"{self.country} {self.crop}"
        self.logger.info(f"Creating ML dataframe {_str}")
        
        df = self._pivot_to_wide_format(df)
        df = self._apply_cumulative_or_stage_selection(df)
        df = self._filter_single_time_period_features(df)
        df = self._filter_current_month_partial_data(df)
        df = self._remove_last_month_data(df)
        df = self._update_column_names(df)
        df = self._add_engineered_features(df)
        df = self._add_region_clusters(df)
        
        return df

    def _pivot_to_wide_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert from long to wide format."""
        df = df[
            ["Index", "Stage_ID", "CEI"]
            + self.fixed_columns
            + [self.target]
            + self.statistics_columns
        ]
        
        # Fill NaN temporarily for pivot
        df.loc[:, [self.target] + self.statistics_columns] = df[
            [self.target] + self.statistics_columns
        ].fillna(-1)
        df.loc[:, "Area"] = df["Area"].fillna(-1)
        
        df = df.pivot_table(
            index=self.fixed_columns + [self.target] + self.statistics_columns,
            columns=["Index", "Stage_ID"],
            values="CEI",
        ).reset_index()
        
        # Restore NaN
        df[[self.target] + self.statistics_columns] = df[
            [self.target] + self.statistics_columns
        ].replace(-1, np.nan)
        
        df.columns = [f"{i}_{j}" if j != "" else f"{i}" for i, j in df.columns]
        
        return df

    def _apply_cumulative_or_stage_selection(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply cumulative features or select specific stage."""
        if not self.use_cumulative_features:
            return self._select_latest_stage(df)
        
        return self._create_cumulative_features(df)

    def _select_latest_stage(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select features from the latest stage only."""
        all_cei_columns = self.get_cei_column_names(df)

        if not all_cei_columns:
            return df

        parts = all_cei_columns[-1].split("_")
        skip = 2 if parts[0] == "AEF" else 1
        first_stage_idx = next(
            (i for i in range(skip, len(parts)) if parts[i].isdigit()),
            len(parts),
        )
        cei = "_".join(parts[:first_stage_idx])
        
        cei_column = df[df.columns[df.columns.str.contains(cei)]].columns
        max_cei_col = max(cei_column, key=len)
        
        self.stage_info = stages.get_stage_information_dict(max_cei_col, self.method)
        
        return df

    def _create_cumulative_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create cumulative features for each region."""
        all_cei_columns = self.get_cei_column_names(df)

        if not all_cei_columns:
            return df

        parts = all_cei_columns[-1].split("_")
        skip = 2 if parts[0] == "AEF" else 1
        first_stage_idx = next(
            (i for i in range(skip, len(parts)) if parts[i].isdigit()),
            len(parts),
        )
        cei = "_".join(parts[:first_stage_idx])
        
        frames = []
        groups = df.groupby(["Region"])
        
        for name, group in groups:
            group = group.dropna(axis=1, how="all")
            
            cei_column = group[group.columns[group.columns.str.contains(cei)]].columns
            
            if not len(cei_column):
                continue
            
            max_cei_col = max(cei_column, key=len)
            self.stage_info = stages.get_stage_information_dict(max_cei_col, self.method)
            
            all_columns = group.columns[
                group.columns.str.contains(self.stage_info["Stage_ID"])
            ].tolist()
            
            try:
                group = group[
                    self.fixed_columns
                    + [self.target]
                    + self.statistics_columns
                    + all_columns
                ]
            except KeyError:
                continue
            
            group.rename(
                columns={
                    col: stages.get_stage_information_dict(col, self.method)["CEI"]
                    for col in all_columns
                },
                inplace=True,
            )
            
            frames.append(group)
        
        if frames:
            return pd.concat(frames)
        
        return df

    def _filter_single_time_period_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter to keep only single time period features if configured."""
        if self.use_single_time_period_as_feature:
            df = stages.select_single_time_period_features(df)
        
        return df

    def _filter_current_month_partial_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove current month data if forecasting current year."""
        if self.forecast_season != self.today_year:
            return df
        
        current_month = ar.utcnow().month
        current_day = ar.utcnow().day
        
        cols_to_drop = []
        for col in df.columns:
            if "_" not in col:
                continue

            try:
                mon = stages.get_stage_information_dict(col, self.method).get("Starting Stage")
            except (ValueError, IndexError, KeyError):
                continue

            if mon == current_month and current_day < 25:
                cols_to_drop.append(col)
        
        return df.drop(columns=cols_to_drop)

    def _remove_last_month_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop feature columns from the last available time period."""
        if not self.remove_last_month:
            return df

        if self.forecast_season != self.today_year:
            return df

        current_month = ar.utcnow().month
        current_day = ar.utcnow().day

        # After _filter_current_month_partial_data:
        # day < 25 → current month already dropped → last available = current_month - 1
        # day >= 25 → current month kept → last available = current_month
        last_month = (current_month - 1 if current_month > 1 else 12) if current_day < 25 else current_month

        cols_to_drop = []
        for col in df.columns:
            if "_" not in col:
                continue
            try:
                mon = stages.get_stage_information_dict(col, self.method).get("Starting Stage")
            except (ValueError, IndexError, KeyError):
                continue
            if mon == last_month:
                cols_to_drop.append(col)

        if cols_to_drop:
            self.logger.info(f"  remove_last_month: dropping {len(cols_to_drop)} columns from stage {last_month}")

        return df.drop(columns=cols_to_drop)

    def _update_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Update column names to be human-readable."""
        df = stages.update_feature_names(df, self.method)
        
        all_cei_columns = self.get_cei_column_names(df)
        df.loc[:, all_cei_columns] = df.loc[:, all_cei_columns].fillna(0)
        
        return df

    def _add_engineered_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add engineered features (lag, median, analogous year, etc.)."""
        df = fe.compute_last_year_yield(df, self.target)
        
        df = fe.compute_median_statistics(
            df, self.all_seasons_with_yield, self.number_median_years, self.target
        )
        
        df = fe.compute_user_median_statistics(df, range(2018, 2023), self.target)
        df = fe.compute_user_median_statistics(df, range(2013, 2018), self.target)
        
        if self.median_area_as_feature:
            df = fe.compute_median_statistics(
                df, self.all_seasons_with_yield, self.number_median_years, "Area (ha)"
            )
        
        if self.lag_yield_as_feature:
            df = fe.compute_lag_yield(
                df, self.all_seasons_with_yield, self.forecast_season,
                self.number_lag_years, self.target
            )
        
        if self.analogous_year_yield_as_feature:
            df = fe.compute_analogous_yield(
                df, self.all_seasons_with_yield, self.number_median_years, self.target
            )
        
        return df

    def _add_region_clusters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add Region_ID column based on clustering strategy."""
        df["Region"] = df["Region"].astype("category")

        if getattr(self, 'countries_pooled', None):
            # Pooled mode: true pooling — one model on all data
            df["Region_ID"] = 1
        elif self.cluster_strategy == "single":
            df["Region_ID"] = 1
        elif self.cluster_strategy == "individual":
            df["Region_ID"] = df["Region"].cat.codes
        elif self.cluster_strategy == "auto_detect":
            clusters_assigned = fe.detect_clusters(df, self.target)
            df = df.merge(clusters_assigned, on="Region")
            df["Region_ID"] = df["Region_ID"].astype("category")
        else:
            raise ValueError(f"Unsupported cluster strategy {self.cluster_strategy}")

        return df

    def get_cei_column_names(self, df: pd.DataFrame) -> List[str]:
        """Get list of CEI column names (excluding fixed/target/meta/engineered columns)."""
        exclude = set(
            self.fixed_columns
            + [self.target]
            + self.statistics_columns
            + [
                f"{self.target}_class",
                "Region_ID", "lat", "lon", "Country Region", "Country__Region",
                f"Detrended {self.target}", "Detrended Model", "Detrended Model Type",
                "Stage Names", "Stage_ID", "Stage Range", "Starting Stage", "Ending Stage",
                "Percentage Season",
                "Analogous Year", "Analogous Year Yield",
            ]
        )
        skip_prefixes = (
            f"Median {self.target}",
            f"Last Year {self.target}",
            "t - ",
            "nbr_",
        )
        return [
            col for col in df.columns
            if col not in exclude and not col.startswith(skip_prefixes)
        ]

    # ============================================================================
    # FEATURE CREATION METHODS
    # ============================================================================

    def create_feature_names(self, stages_features: list, selected_features: dict):
        """
        Create feature names for machine learning stages.
        
        Args:
            stages_features: List of features for different stages
            selected_features: Dictionary of selected features
        """
        if not isinstance(stages_features, list):
            raise TypeError("stages_features should be a list")
        
        self.feature_names = []
        
        method = "latest" if self.model_name.startswith("cumulative_") else "fraction"
        
        #stages_features = stages.select_stages_for_ml(
        #    stages_features, method=method, n=60
        #)
        
        for stage in stages_features:
            _stage = "_".join(map(str, stage))
            _tmp = [f"{col}_{_stage}" for col in self.combined_keys]
            
            for _t in _tmp:
                parts = _t.split("_")
                # Find where numeric stage numbers begin (AEF_N band is part of name)
                _skip = 2 if parts[0] == "AEF" else 1
                _idx = next(
                    (i for i in range(_skip, len(parts)) if parts[i].isdigit()),
                    len(parts),
                )
                cei = "_".join(parts[:_idx])
                
                try:
                    if self.model_name.startswith("cumulative_"):
                        dict_fn = stages.get_stage_information_dict(_t, self.method)
                        tmp_col = f"{dict_fn['CEI']}"
                        
                        if tmp_col in self.df_train.columns:
                            self.feature_names.append(tmp_col)
                    else:
                        if selected_features["CEI"].any():
                            for x in selected_features["CEI"].values:
                                if x not in cei:
                                    continue
                                
                                dict_fn = stages.get_stage_information_dict(_t, self.method)
                                tmp_col = f"{dict_fn['CEI']} {dict_fn['Stage Name']}"
                                
                                if tmp_col in self.df_train.columns:
                                    self.feature_names.append(tmp_col)
                except Exception as e:
                    self.logger.error(f"Error creating feature name for {_t}: {e}")
        
        self.feature_names = list(set(self.feature_names))
        
        if self.median_yield_as_feature:
            self.feature_names.append(f"Median {self.target}")
        
        if self.lag_yield_as_feature:
            for i in range(1, self.number_lag_years + 1):
                self.feature_names.append(f"t -{i} {self.target}")
        
        if self.analogous_year_yield_as_feature:
            self.feature_names.extend(["Analogous Year", "Analogous Year Yield"])
        
        if self.use_outlook_as_feature:
            self.feature_names.append("FCST")
        
        if self.include_lat_lon_as_feature:
            self.feature_names.extend(["lat", "lon"])

        if self.use_spatial_neighbors:
            nbr_cols = [c for c in self.df_train.columns if c.startswith("nbr_")]
            self.feature_names.extend(nbr_cols)

        self.selected_features = []

    # ============================================================================
    # FEATURE SELECTION
    # ============================================================================

    def apply_feature_selector(self, region: int, dir_output: Path):
        """
        Apply feature selection for a specific region.
        
        Args:
            region: Region ID
            dir_output: Directory for output files
        """
        if self.model_name.startswith("cumulative_"):
            all_features = self.X_train.columns
            self.selected_features = [
                column for column in all_features
                if any(cei in column for cei in self.use_ceis)
            ]
        elif self.feature_selection.lower() == "none":
            self.logger.info(f"Skipping feature selection for {self.country} {self.crop}")
            X_for_selection = self.X_train.drop(columns=["Region"], errors="ignore")
            self.selected_features = X_for_selection.columns.tolist()
            self.logger.info(f"Using all {len(self.selected_features)} features")
        else:
            self.logger.info(f"Selecting features for {self.country} {self.crop}")
            X_for_selection = self.X_train.drop(columns=["Region"], errors="ignore")
            _, _, self.selected_features = fs.select_features(
                X_for_selection,
                self.y_train,
                method=self.feature_selection,
                dir_output=dir_output,
                region=region
            )
            # fallback: if selector returned no features, use all
            if not self.selected_features:
                self.logger.warning(
                    f"Feature selection ({self.feature_selection}) returned 0 "
                    f"features for {self.country} {self.crop}; using all features"
                )
                self.selected_features = X_for_selection.columns.tolist()
            self.logger.info(f"Selected features: {self.selected_features}")
        
        # Ensure lat/lon are included if configured
        if "lat" not in self.selected_features and self.include_lat_lon_as_feature:
            self.selected_features.append("lat")
        if "lon" not in self.selected_features and self.include_lat_lon_as_feature:
            self.selected_features.append("lon")

    # ============================================================================
    # MODEL TRAINING (Delegated to ModelTrainer)
    # ============================================================================

    def train_model(self, df_region: pd.DataFrame, dir_output: Path, scaler=None):
        """
        Train ML model - delegates to ModelTrainer for actual training logic.
        
        Args:
            df_region: Regional training data
            dir_output: Output directory
            scaler: Optional scaler for preprocessing
        """
        trainer = ModelTrainer(self)
        trainer.train(df_region, dir_output, scaler)

    # ============================================================================
    # PREDICTION (Refactored with helper methods)
    # ============================================================================

    def predict(
        self, 
        df_region: pd.DataFrame, 
        scaler=None
    ) -> Tuple[str, pd.DataFrame]:
        """
        Predict yield for the current stage.
        
        Args:
            df_region: Regional test data
            scaler: Optional scaler
            
        Returns:
            Tuple of (experiment_id, results_dataframe)
        """
        X_test = df_region[self.selected_features + self.cat_features]
        y_test = df_region[self.target].values
        
        y_pred, y_pred_ci, best_hyperparameters = self._run_prediction(
            X_test, df_region, scaler
        )
        
        if self.check_yield_trend:
            y_pred = self._retrend_predictions(y_pred, df_region)

        if getattr(self, 'countries_pooled', None):
            experiment_id = f"pooled_{self.crop}"
        else:
            experiment_id = f"{self.country}_{self.crop}"
        df_result = self._build_results_dataframe(
            df_region, X_test, y_test, y_pred, y_pred_ci, 
            best_hyperparameters, experiment_id
        )
        
        return experiment_id, df_result

    def _run_prediction(
        self, 
        X_test: pd.DataFrame, 
        df_region: pd.DataFrame, 
        scaler
    ) -> Tuple:
        """Execute prediction based on model type."""
        if not self.ml_model:
            return self._predict_baseline(X_test, df_region)
        
        X_test_processed = self._preprocess_test_data(X_test, scaler)
        
        if self.estimate_ci:
            return self._predict_with_confidence_intervals(X_test_processed, df_region)
        else:
            return self._predict_point_estimates(X_test_processed, df_region)

    def _predict_baseline(
        self, 
        X_test: pd.DataFrame, 
        df_region: pd.DataFrame
    ) -> Tuple:
        """Non-ML baseline predictions."""
        if self.model_name == "analog":
            y_pred = np.full(len(X_test), df_region["Analogous Year Yield"].values)
        elif self.model_name == "median":
            y_pred = np.full(len(X_test), df_region[f"Median {self.target}"].values)
        elif self.model_name == "last_year":
            y_pred = np.full(len(X_test), df_region[f"Last Year {self.target}"].values)
        else:
            raise ValueError(f"Unknown baseline model: {self.model_name}")
        
        return y_pred, None, np.nan

    def _preprocess_test_data(self, X_test: pd.DataFrame, scaler) -> pd.DataFrame:
        """Preprocess test data based on model requirements."""
        if self.model_name in ["linear", "gam"]:
            X_test = X_test.drop(
                columns=[item for item in self.cat_features if item != "Harvest Year"]
            )
            return scaler.transform(X_test)
        
        if self.model_name.startswith("cumulative_"):
            return self._scale_cumulative_features(X_test)
        
        return X_test

    def _scale_cumulative_features(self, X_test: pd.DataFrame) -> pd.DataFrame:
        """Special scaling for cumulative models."""
        num_columns = int(self.model_name.split("_")[1])
        
        scaler = StandardScaler()
        X_numeric = X_test.iloc[:, :num_columns]
        X_scaled_numeric = pd.DataFrame(
            scaler.fit_transform(X_numeric),
            columns=X_numeric.columns,
            index=X_test.index,
        )
        
        le = LabelEncoder()
        X_region = pd.Series(
            le.fit_transform(X_test["Region"]),
            name="Region",
            index=X_test.index,
        )
        
        return pd.concat([X_scaled_numeric, X_region], axis=1)

    def _predict_with_confidence_intervals(
        self, 
        X_test: pd.DataFrame,
        df_region: pd.DataFrame
    ) -> Tuple:
        """Predict with confidence intervals."""
        if not (self.estimate_ci_for_all or self.forecast_season == self.today_year):
            return self._predict_point_estimates(X_test, df_region)
        
        if self.model_name == "ngboost":
            return self._predict_ngboost_with_ci(X_test)
        elif self.model_name == "tabpfn":
            return self._predict_tabpfn_with_quantiles(X_test)
        elif self.model_name == "tabicl":
            return self._predict_tabicl_with_quantiles(X_test)
        elif self.model_name in ["logistic", "catboost"] and self.model_type == "CLASSIFICATION":
            return self._predict_classification_with_proba(X_test)
        else:
            return self._predict_with_conformal(X_test)

    def _predict_ngboost_with_ci(self, X_test: pd.DataFrame) -> Tuple:
        """NGBoost-specific prediction with confidence intervals."""
        y_pred = self.model.predict(X_test)
        
        if self.model_type == "REGRESSION":
            y_dists = self.model.pred_dist(X_test)
            z_value = utils.get_z_value(self.alpha)
            
            means = y_dists.loc
            std_devs = y_dists.scale
            
            lower_bounds = means - z_value * std_devs
            upper_bounds = means + z_value * std_devs
            
            y_pred_ci = np.vstack([lower_bounds, means, upper_bounds]).T
        else:
            y_pred_proba = self.model.predict_proba(X_test)
            y_pred_ci = np.vstack([y_pred_proba[:, 0], y_pred, y_pred_proba[:, 1]]).T
        
        return y_pred, y_pred_ci, {}

    def _predict_tabpfn_with_quantiles(self, X_test: pd.DataFrame) -> Tuple:
        """TabPFN native quantile regression for prediction intervals."""
        lower_q = self.alpha / 2
        upper_q = 1.0 - self.alpha / 2

        y_pred = self.model.predict(X_test)
        q_preds = self.model.predict(
            X_test, output_type="quantiles", quantiles=[lower_q, upper_q]
        )

        # Handle both list-of-arrays and 2D-array returns
        q_arr = np.asarray(q_preds)
        self.logger.debug(f"  TabPFN quantile raw type={type(q_preds)}, array shape={q_arr.shape}")
        if q_arr.ndim == 2 and q_arr.shape[1] >= 2:
            # Shape (n_samples, n_quantiles)
            lower = q_arr[:, 0]
            upper = q_arr[:, -1]
        else:
            # List of arrays: [lower_array, upper_array]
            lower = np.asarray(q_preds[0])
            upper = np.asarray(q_preds[-1])

        # Match expected shape: (n_samples, 2, 1) → flattens to [lower, upper] per sample
        y_pred_ci = np.stack([lower, upper], axis=1)[:, :, np.newaxis]
        self.logger.debug(f"  TabPFN CI shape={y_pred_ci.shape}, sample[0]: [{lower[0]:.3f}, {upper[0]:.3f}]")

        return y_pred, y_pred_ci, {}

    def _predict_tabicl_with_quantiles(self, X_test: pd.DataFrame) -> Tuple:
        """TabICL native quantile regression for prediction intervals."""
        lower_q = self.alpha / 2
        upper_q = 1.0 - self.alpha / 2

        y_pred = self.model.predict(X_test)
        q_preds = self.model.predict(
            X_test, output_type="quantiles", alphas=[lower_q, upper_q]
        )

        # Handle both list-of-arrays and 2D-array returns
        q_arr = np.asarray(q_preds)
        self.logger.debug(f"  TabICL quantile raw type={type(q_preds)}, array shape={q_arr.shape}")
        if q_arr.ndim == 2 and q_arr.shape[1] >= 2:
            # Shape (n_samples, n_quantiles)
            lower = q_arr[:, 0]
            upper = q_arr[:, -1]
        else:
            # List of arrays: [lower_array, upper_array]
            lower = np.asarray(q_preds[0])
            upper = np.asarray(q_preds[-1])

        # Match expected shape: (n_samples, 2, 1) → flattens to [lower, upper] per sample
        y_pred_ci = np.stack([lower, upper], axis=1)[:, :, np.newaxis]
        self.logger.debug(f"  TabICL CI shape={y_pred_ci.shape}, sample[0]: [{lower[0]:.3f}, {upper[0]:.3f}]")

        return y_pred, y_pred_ci, {}

    def _predict_classification_with_proba(self, X_test: pd.DataFrame) -> Tuple:
        """Classification with probabilities."""
        y_pred = self.model.predict(X_test)
        y_pred_ci = self.model.predict_proba(X_test)
        return y_pred, y_pred_ci, {}

    def _predict_with_conformal(self, X_test: pd.DataFrame) -> Tuple:
        """Predict using conformal prediction (crepes or MAPIE)."""
        if hasattr(self.model, 'predict_int'):
            # crepes WrapRegressor
            y_pred = self.model.predict(X_test)
            intervals = self.model.predict_int(X_test, confidence=1 - self.alpha)
            y_pred_ci = intervals[:, :, np.newaxis]  # (n, 2) → (n, 2, 1)
        else:
            # MAPIE SplitConformalRegressor
            y_pred, y_pred_ci = self.model.predict_interval(X_test)

        best_hyperparameters = {}
        try:
            inner = getattr(self.model, 'learner', None) or getattr(self.model, 'estimator', self.model)
            best_hyperparameters = inner.get_params().copy()
        except AttributeError:
            pass

        return y_pred, y_pred_ci, best_hyperparameters

    def _predict_point_estimates(
        self, 
        X_test: pd.DataFrame,
        df_region: pd.DataFrame
    ) -> Tuple:
        """Standard point predictions."""
        if self.model_name == "merf":
            return self._predict_merf(X_test, df_region)
        
        y_pred = np.asarray(self.model.predict(X_test)).ravel()

        try:
            best_hyperparameters = self.model.get_params().copy()
        except AttributeError:
            best_hyperparameters = {}

        return y_pred, None, best_hyperparameters

    def _predict_merf(self, X_test: pd.DataFrame, df_region: pd.DataFrame) -> Tuple:
        """MERF-specific prediction."""
        Z_test = np.ones((len(X_test), 1))
        clusters_test = df_region["Region"].reset_index(drop=True).astype("object")
        
        y_pred = self.model.predict(X_test, Z_test, clusters_test)
        best_hyperparameters = self.model.fe_model.get_params().copy()
        
        return y_pred, None, best_hyperparameters

    def _retrend_predictions(
        self,
        y_pred: np.ndarray,
        df_region: pd.DataFrame
    ) -> np.ndarray:
        """Add trend back to detrended predictions."""
        y_pred_retrended = y_pred.copy()

        for region in df_region["Region"].unique():
            mask_test = df_region["Region"].values == region
            row_indices = np.where(mask_test)[0]

            mask_train = self.df_train["Region"] == region
            df_tmp = self.df_train[mask_train]

            if df_tmp.empty:
                continue

            model_type = df_tmp["Detrended Model Type"].iloc[0]

            for ri in row_indices:
                if model_type == "gaussian":
                    gaussian_model = self.detrend_models[region]
                    year = df_region.iloc[ri]["Harvest Year"]
                    X = add_constant(np.array([year]), has_constant="add")
                    yei = gaussian_model["extrap_model"].predict(X)[0]
                    # Detrended values are percent anomalies: Yai = 100*(Yi-Yei)/Yei
                    # Retrend: Yi = Yei * (1 + Yai/100)
                    y_pred_retrended[ri] = yei * (1 + y_pred[ri] / 100.0)
                else:
                    obj_trend = trend.DetrendedData(
                        df_tmp[f"Detrended {self.target}"],
                        df_tmp["Detrended Model"],
                        df_tmp["Detrended Model Type"],
                    )
                    trend_value = trend.compute_trend(
                        obj_trend, df_region.iloc[ri][["Harvest Year"]]
                    )[0]
                    y_pred_retrended[ri] += trend_value

                df_region.iloc[ri, df_region.columns.get_loc("Detrended Model Type")] = model_type

        return y_pred_retrended

    def _build_results_dataframe(
        self,
        df_region: pd.DataFrame,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        y_pred_ci: Optional[np.ndarray],
        best_hyperparameters: dict,
        experiment_id: str
    ) -> pd.DataFrame:
        """Build comprehensive results dataframe."""
        shp = len(X_test)
        
        df = self._create_base_results(
            df_region, X_test, y_test, y_pred, 
            best_hyperparameters, experiment_id, shp
        )
        
        self._add_median_yield_columns(df, df_region)
        self._add_confidence_intervals(df, y_pred_ci)
        self._add_trend_info(df, df_region)
        self._add_feature_columns(df, df_region)
        
        df.index = self._create_result_index(df)
        df.index.set_names(["Index"], inplace=True)
        
        return df

    def _create_base_results(
        self,
        df_region: pd.DataFrame,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        best_hyperparameters: dict,
        experiment_id: str,
        shp: int
    ) -> pd.DataFrame:
        """Create base results dataframe."""
        now = ar.utcnow().to("America/New_York").format("MMMM-DD-YYYY HH:mm:ss")
        selected_features = self.selected_features + self.cat_features
        
        ape = self._compute_ape(y_pred, y_test, shp)
        
        # In pooled mode, pull Country from data (per-row); otherwise use self.country
        if getattr(self, 'countries_pooled', None):
            country_vals = df_region["Country"].values
        else:
            country_vals = np.full(shp, self.country)

        return pd.DataFrame({
            "Experiment_ID": np.full(shp, experiment_id),
            "Experiment Name": np.full(shp, self.experiment_name),
            "Date": np.full(shp, self.today),
            "Time": np.full(shp, now),
            "Country": country_vals,
            "Crop": np.full(shp, self.crop),
            "Cluster Strategy": np.full(shp, self.cluster_strategy),
            "Frequency": np.full(shp, self.method),
            "Selected Features": [selected_features.copy() for _ in range(shp)],
            "Best Hyperparameters": np.full(shp, best_hyperparameters),
            "Stage_ID": np.full(shp, self.stage_info["Stage_ID"]),
            "Stage Range": np.full(shp, self.stage_info["Stage Range"]),
            "Stage Name": np.full(shp, self.stage_info["Stage Name"]),
            "Starting Stage": np.full(shp, self.stage_info["Starting Stage"]),
            "Ending Stage": np.full(shp, self.stage_info["Ending Stage"]),
            "Model": np.full(shp, self.model_name),
            "Region_ID": df_region["Region_ID"].values,
            "Region": df_region["Region"].values,
            "Season": df_region["Season"].values,
            "Harvest Year": df_region["Harvest Year"].values,
            "Area (ha)": df_region["Area (ha)"].values,
            f"Observed {self.target}": np.around(y_test, 3).ravel(),
            f"Predicted {self.target}": np.around(y_pred, 3).ravel(),
            "APE": np.around(ape, 3).ravel(),
        })

    def _compute_ape(
        self, 
        y_pred: np.ndarray, 
        y_test: np.ndarray, 
        shp: int
    ) -> np.ndarray:
        """Compute absolute percentage error."""
        if self.model_type == "REGRESSION":
            return np.abs((y_pred - y_test) / y_test) * 100
        else:
            return np.full(shp, np.nan)

    def _add_median_yield_columns(self, df: pd.DataFrame, df_region: pd.DataFrame):
        """Add median yield reference columns."""
        df.loc[:, f"Median {self.target}"] = np.around(
            df_region[f"Median {self.target}"].values, 3
        )
        
        for period in ["(2018-2022)", "(2013-2017)"]:
            col_name = f"Median {self.target} {period}"
            if col_name in df_region.columns:
                df.loc[:, col_name] = np.around(df_region[col_name].values, 3)

    def _add_confidence_intervals(self, df: pd.DataFrame, y_pred_ci: Optional[np.ndarray]):
        """Add confidence interval columns if applicable."""
        if not self.estimate_ci:
            return
        
        if not (self.estimate_ci_for_all or self.forecast_season == self.today_year):
            return
        
        if y_pred_ci is None:
            return
        
        for idx, ci in enumerate(y_pred_ci):
            df.loc[idx, "alpha"] = self.alpha
            
            if self.model_type == "REGRESSION":
                y_pred_ci_ = [item for sublist in ci for item in sublist]
                df.loc[idx, "lower CI"] = np.around(y_pred_ci_[0], 3)
                df.loc[idx, "upper CI"] = np.around(y_pred_ci_[1], 3)
            else:
                df.loc[idx, "CI"] = ", ".join(map(str, np.asarray(ci).flatten()))

    def _add_trend_info(self, df: pd.DataFrame, df_region: pd.DataFrame):
        """Add detrending information if applicable."""
        if self.check_yield_trend:
            df.loc[:, "Detrended Model Type"] = df_region["Detrended Model Type"].values

    def _add_feature_columns(self, df: pd.DataFrame, df_region: pd.DataFrame):
        """Add feature-related columns."""
        if self.last_year_yield_as_feature:
            df.loc[:, f"Last Year {self.target}"] = np.around(
                df_region[f"Last Year {self.target}"].values, 3
            )
        
        if self.analogous_year_yield_as_feature:
            df.loc[:, "Analogous Year"] = df_region["Analogous Year"].values
            df.loc[:, "Analogous Year Yield"] = np.around(
                df_region["Analogous Year Yield"].values, 3
            )
        
        for col in [
            f"Median {self.target}",
            "Analogous Year",
            "Analogous Year Yield",
            "Detrended Model Type",
            "Detrended Model",
        ]:
            if col not in df.columns:
                df.loc[:, col] = np.nan

        # Last observed year and yield per region
        obs_map = getattr(self, 'last_observed_map', {})
        regions = df_region["Region"].values
        df.loc[:, "Last Observed Year"] = [
            obs_map[r][0] if r in obs_map else np.nan for r in regions
        ]
        last_yields = [
            obs_map[r][1] if r in obs_map else np.nan for r in regions
        ]
        df.loc[:, f"Last Observed {self.target}"] = [
            np.around(v, 3) if not np.isnan(v) else np.nan for v in last_yields
        ]

    def _create_result_index(self, df: pd.DataFrame) -> pd.Series:
        """Create unique index for results."""
        index_columns = [
            "Experiment Name", "Model", "Cluster Strategy", "Country",
            "Region", "Crop", "Season", "Harvest Year", "Stage Name", "Time",
        ]
        
        return df.apply(
            lambda row: "_".join([str(row[col]) for col in index_columns]), 
            axis=1
        )

    # ============================================================================
    # ML LOOP - Training and prediction for all regions
    # ============================================================================

    def loop_ml(
        self, 
        stages: list, 
        dict_selected_features: Dict, 
        dict_best_cei: Dict
    ):
        """
        Main ML loop - orchestrates training and prediction for all regions.
        
        Args:
            stages: List of stages to use
            dict_selected_features: Selected features per region
            dict_best_cei: Best CEI features per region
        """
        dir_output = self._get_output_directory()
        scaler = self._initialize_scaler()
        
        region_ids = self.df_train["Region_ID"].unique()
        pbar = tqdm(region_ids, leave=False)
        
        for idx, region_id in enumerate(pbar):
            try:
                self._process_single_region(
                    region_id, idx, stages, dict_selected_features, 
                    dict_best_cei, dir_output, scaler, pbar
                )
            except Exception as e:
                self.logger.error(f"Error processing region {region_id}: {e}\n{traceback.format_exc()}")

    def _get_output_directory(self) -> Path:
        """Get output directory for current model/season."""
        base = self.dir_analysis
        if self.experiment_name != "default":
            base = base / self.experiment_name / "runs"
        dir_output = (
            base / self.country / self.crop /
            self.model_name / str(self.forecast_season)
        )
        dir_output.mkdir(parents=True, exist_ok=True)
        return dir_output

    def _initialize_scaler(self):
        """Initialize scaler if needed."""
        if self.model_name in ["linear", "gam"]:
            return StandardScaler()
        return None

    def _process_single_region(
        self,
        region_id: int,
        idx: int,
        stages: list,
        dict_selected_features: Dict,
        dict_best_cei: Dict,
        dir_output: Path,
        scaler,
        pbar
    ):
        """Process training and prediction for a single region."""
        self._create_feature_names_for_region(
            region_id, stages, dict_selected_features, dict_best_cei
        )

        df_region_train, df_region_test = self._prepare_region_data(region_id)
        
        if df_region_train.empty:
            self.logger.warning(f"No training data for region {region_id}")
            return
        
        self._setup_training_data(df_region_train)
        self._select_features(region_id, dir_output)
        
        self._update_progress_bar(pbar, idx)
        
        if self.ml_model:
            self.train_model(df_region_train, dir_output, scaler)
        
        experiment_id, df_results = self.predict(df_region_test, scaler)
        
        self._run_xai_if_enabled(df_region_train, df_region_test)
        self._store_results(experiment_id, df_results)

    def _create_feature_names_for_region(
        self,
        region_id: int,
        stages: list,
        dict_selected_features: Dict,
        dict_best_cei: Dict
    ):
        """Create feature names based on model type and region."""
        if self.model_name == "linear":
            selected = dict_best_cei[region_id][0:3].tolist()
            self.create_feature_names(stages, selected)
        elif self.model_name.startswith("cumulative_"):
            self.create_feature_names(stages, {})
        elif self.ml_model:
            selected = dict_selected_features.get(region_id)
            if selected is not None and not selected.empty:
                self.create_feature_names(stages, selected)
            else:
                # No correlation-based selection — use all CEI features
                self.feature_names = self.get_cei_column_names(self.df_train)
        elif self.model_name == "median":
            self.feature_names = [f"Median {self.target}"]
            self.last_year_yield_as_feature = False
            self.analogous_year_yield_as_feature = False
        elif self.model_name == "analog":
            self.feature_names = ["Analogous Year", "Analogous Year Yield"]
            self.last_year_yield_as_feature = False
            self.median_yield_as_feature = False

    def _prepare_region_data(self, region_id: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Prepare training and test data for a specific region."""
        mask_train = self.df_train["Region_ID"] == region_id
        mask_test = self.df_test["Region_ID"] == region_id

        common_columns = self._get_common_columns()
        
        df_region_train = self._extract_region_subset(
            self.df_train[mask_train], common_columns
        )
        
        df_region_test = self._extract_region_subset(
            self.df_test[mask_test], common_columns
        )
        
        return df_region_train, df_region_test

    def _get_common_columns(self) -> List[str]:
        """Get list of common columns needed for training/testing."""
        common_columns = (
            [self.target, self.target_class]
            + self.statistics_columns
            + self.feature_names
            + [f"Median {self.target}"]
            + [f"Median {self.target} (2018-2022)"]
            + [f"Median {self.target} (2013-2017)"]
            + ["Region_ID"]
        )
        
        if self.check_yield_trend:
            common_columns.extend([
                f"Detrended {self.target}",
                "Detrended Model Type",
                "Detrended Model",
            ])
        
        if self.last_year_yield_as_feature:
            common_columns.append(f"Last Year {self.target}")

        if self.use_spatial_neighbors:
            nbr_cols = [c for c in self.df_train.columns if c.startswith("nbr_")]
            common_columns.extend(nbr_cols)

        return common_columns

    def _extract_region_subset(
        self, 
        df: pd.DataFrame, 
        common_columns: List[str]
    ) -> pd.DataFrame:
        """Extract region subset with proper column filtering."""
        df_subset = df[self.fixed_columns + common_columns].copy()
        df_subset.reset_index(drop=True, inplace=True)
        return df_subset

    def _setup_training_data(self, df_region_train: pd.DataFrame):
        """Setup X_train and y_train, handling NaN values."""
        df_region_train = df_region_train.dropna(subset=[self.target_column])
        
        self.X_train = df_region_train[self.feature_names + ["Region"]]
        
        self.X_train = self._clean_training_features(self.X_train)
        
        if self.model_name in ["gam", "linear"]:
            self._fill_missing_values()
        
        self.y_train = df_region_train[self.target_column]

        # Compute last available observed year and yield PER REGION
        df_valid = df_region_train.dropna(subset=[self.target_column])
        self.last_observed_map = {}  # {region_name: (year, yield)}
        if not df_valid.empty:
            for region, grp in df_valid.groupby("Region"):
                last_row = grp.loc[grp["Harvest Year"].idxmax()]
                self.last_observed_map[region] = (
                    int(last_row["Harvest Year"]),
                    float(last_row[self.target_column]),
                )

    # Add debug logging in _clean_training_features
    def _clean_training_features(self, X_train: pd.DataFrame) -> pd.DataFrame:
        """Drop columns with NaNs except lag yield and neighbor columns."""
        preserve_cols = [
            c for c in X_train.columns
            if c.startswith("t -") or c.startswith("nbr_")
        ]

        X_train = (
            X_train
            .drop(columns=preserve_cols)
            .dropna(axis=1, how="any")
            .join(X_train[preserve_cols])
        )

        return X_train

    def _fill_missing_values(self):
        """Fill missing values with median (for models that can't handle NaN)."""
        for col in self.X_train.columns:
            median = self.X_train[col].median()
            self.X_train[col].fillna(median, inplace=True)

    def _select_features(self, region_id: int, dir_output: Path):
        """Apply feature selection for the region."""
        self.apply_feature_selector(region_id, dir_output)

    def _update_progress_bar(self, pbar, idx: int):
        """Update progress bar with region information."""
        if self.cluster_strategy == "individual":
            region_name = self.df_train["Region"].unique()[idx]
            pbar.set_description(f"Fit/Predict {self.country} {self.crop} {region_name}")
        else:
            pbar.set_description(f"Fit/Predict {self.country} {self.crop} group {idx + 1}")
        
        pbar.update()

    def _run_xai_if_enabled(
        self, 
        df_region_train: pd.DataFrame, 
        df_region_test: pd.DataFrame
    ):
        """Run XAI (explainable AI) analysis if configured."""
        if not self.do_xai:
            return

        # TabPFN/TabICL use native quantile prediction (no conformal wrapper),
        # so SHAP can still introspect the underlying model when estimate_ci
        # is True. The guard only matters for tree models wrapped by crepes/MAPIE.
        if self.estimate_ci and self.model_name not in ("tabpfn", "tabicl"):
            self.logger.warning("Cannot perform XAI if estimate_ci is True")
            return
        
        kwargs = {
            "cluster_strategy": self.cluster_strategy,
            "model": self.model,
            "model_name": self.model_name,
            "forecast_season": self.forecast_season,
            "crop": self.crop,
            "country": self.country,
            "analysis_dir": self.dir_analysis,
            "db_path": self.db_path,
        }
        
        try:
            xai.explain(df_region_train, df_region_test, **kwargs)
        except Exception as e:
            self.logger.error(f"Error in XAI: {e}")

    def _store_results(self, experiment_id: str, df: pd.DataFrame):
        """Store results to database."""
        if not self.ml_model:
            model = self.model_name
        elif self.estimate_ci:
            try:
                model = self.model.estimator_
            except AttributeError:
                model = getattr(self.model, 'learner',
                        getattr(self.model, 'estimator', self.model))
        else:
            model = self.model
        
        try:
            output.store(self.db_path, experiment_id, df, model, self.model_name)
        except Exception as e:
            self.logger.error(f"Error storing results for {experiment_id}: {e}")


# ============================================================================
# MODEL TRAINER CLASS - Strategy Pattern for Different Model Types
# ============================================================================

class ModelTrainer:
    """Strategy pattern for different model training approaches."""
    
    def __init__(self, geocif_obj: Geocif):
        self.obj = geocif_obj
        
    def train(self, df_region: pd.DataFrame, dir_output: Path, scaler=None):
        """Main training orchestrator."""
        X_train = self._prepare_training_data(df_region)
        self._save_training_data(X_train, df_region, dir_output)

        X_train_scaled = self._scale_if_needed(X_train, scaler)

        self._train_base_model(df_region, X_train_scaled)
        self._fit_final_model(X_train, X_train_scaled, df_region)
        self._add_confidence_intervals_if_needed(X_train)
    
    def _prepare_training_data(self, df_region: pd.DataFrame) -> pd.DataFrame:
        """Extract and prepare features for training."""
        return df_region[self.obj.selected_features + self.obj.cat_features]
    
    def _save_training_data(
        self, 
        X_train: pd.DataFrame, 
        df_region: pd.DataFrame, 
        dir_output: Path
    ):
        """Save training data for debugging/analysis."""
        region_id = df_region["Region_ID"].unique()[0]
        X_train.to_csv(dir_output / f"X_train_{region_id}.csv", index=False)
    
    def _scale_if_needed(self, X_train: pd.DataFrame, scaler):
        """Scale features if scaler is provided."""
        if not scaler:
            return X_train
        
        X_train_nocat = X_train.drop(
            columns=[item for item in self.obj.cat_features 
                    if item != "Harvest Year"]
        )
        return scaler.fit_transform(X_train_nocat)
    
    def _train_base_model(self, df_region: pd.DataFrame, X_train_scaled):
        """Train the base model with hyperparameter optimization."""
        self.obj.best_hyperparams, self.obj.model = trainers.auto_train(
            self.obj.cluster_strategy,
            self.obj.model_name,
            self.obj.model_type,
            False,
            "Harvest Year",
            df_region[
                self.obj.selected_features + 
                self.obj.cat_features + 
                [self.obj.target]
            ],
            X_train_scaled,
            self.obj.y_train,
            feature_names=self.obj.selected_features,
            target_col=self.obj.target_column,
            optimize=self.obj.optimize,
            fraction_loocv=self.obj.fraction_loocv,
            cat_features=self.obj.cat_features,
        )
    
    def _add_confidence_intervals_if_needed(self, X_train=None):
        """Wrap model with confidence interval estimator."""
        if not self.obj.estimate_ci:
            return

        if not (self.obj.estimate_ci_for_all or
                self.obj.forecast_season == self.obj.today_year):
            return

        self.obj.model = trainers.estimate_ci(
            self.obj.model_type,
            self.obj.model_name,
            self.obj.model,
            self.obj.alpha,
            self.obj.ci_method,
        )
        # Calibrate/conformalize with training data
        if X_train is not None:
            if hasattr(self.obj.model, 'calibrate'):
                self.obj.model.calibrate(X_train, self.obj.y_train.values)
            elif hasattr(self.obj.model, 'conformalize'):
                self.obj.model.conformalize(X_train, self.obj.y_train)
    
    def _fit_final_model(
        self, 
        X_train: pd.DataFrame, 
        X_train_scaled, 
        df_region: pd.DataFrame
    ):
        """Fit the final model using model-specific logic."""
        fitter = self._get_model_fitter()
        fitter.fit(X_train, X_train_scaled, df_region)
    
    def _get_model_fitter(self):
        """Factory method to get appropriate model fitter."""
        fitters = {
            "catboost": CatBoostFitter(self.obj),
            "tabpfn": TabPFNFitter(self.obj),
            "tabicl": TabICLFitter(self.obj),
            "ngboost": NGBoostFitter(self.obj),
            "oblique": ObliqueFitter(self.obj),
            "ydf": YDFFitter(self.obj),
            "geospaNN": GeospaNNFitter(self.obj),
            "merf": MERFFitter(self.obj),
            "linear": LinearFitter(self.obj),
            "gam": GAMFitter(self.obj),
            "cubist": CubistFitter(self.obj),
        }
        
        if self.obj.model_name.startswith("cumulative_"):
            return CumulativeFitter(self.obj)
        
        if self.obj.model_name == "desreg":
            return DesregFitter(self.obj)
        
        return fitters.get(self.obj.model_name, DefaultFitter(self.obj))


# ============================================================================
# MODEL FITTERS - One class per model type
# ============================================================================

class BaseFitter:
    """Base class for model-specific fitting logic."""
    
    def __init__(self, geocif_obj: Geocif):
        self.obj = geocif_obj
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        raise NotImplementedError


class CatBoostFitter(BaseFitter):
    """CatBoost-specific fitting."""

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        self.obj.model.fit(
            X_train,
            self.obj.y_train,
            cat_features=self.obj.cat_features,
            verbose=False,
        )


class TabPFNFitter(BaseFitter):
    """TabPFN-specific fitting with categorical feature handling."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        cat_feature_indices = self._get_categorical_indices(X_train)
        self.obj.model.fit(
            X_train,
            np.asarray(self.obj.y_train).ravel(),
            # categorical_feature_indices=cat_feature_indices
        )
    
    def _get_categorical_indices(self, X_train: pd.DataFrame) -> List[int]:
        """Get indices of categorical features."""
        if not self.obj.cat_features:
            return []
        
        return [
            X_train.columns.get_loc(col) 
            for col in self.obj.cat_features 
            if col in X_train.columns
        ]


class TabICLFitter(BaseFitter):
    """TabICL-specific fitting."""

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        import sklearn
        prev = sklearn.get_config()["transform_output"]
        sklearn.set_config(transform_output="default")
        try:
            self.obj.model.fit(X_train, np.asarray(self.obj.y_train).ravel())
        finally:
            sklearn.set_config(transform_output=prev)


class NGBoostFitter(BaseFitter):
    """NGBoost-specific fitting (no categorical features)."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        X_train_no_cat = X_train.drop(
            columns=[item for item in self.obj.cat_features 
                    if item != "Harvest Year"]
        )
        self.obj.model.fit(X_train_no_cat, self.obj.y_train)


class ObliqueFitter(NGBoostFitter):
    """Oblique tree fitter (same as NGBoost)."""
    pass


class YDFFitter(BaseFitter):
    """Yggdrasil Decision Forests fitter."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        df_train = pd.concat([X_train, self.obj.y_train], axis=1)
        self.obj.model = self.obj.model.train(df_train)


class GeospaNNFitter(BaseFitter):
    """Geospatial Neural Network fitter."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        self.obj.model.fit(X_train, self.obj.y_train)


class MERFFitter(BaseFitter):
    """Mixed Effects Random Forest fitter."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        Z_train = np.ones((len(X_train), 1))
        clusters_train = df_region["Region"].reset_index(drop=True).astype("object")
        
        self.obj.model.fit(
            X_train,
            Z_train,
            clusters_train,
            self.obj.y_train.values,
        )


class LinearFitter(BaseFitter):
    """Linear model fitter (uses scaled data)."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        self.obj.model.fit(X_train_scaled, self.obj.y_train)


class GAMFitter(BaseFitter):
    """Generalized Additive Model fitter."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        self.obj.model.fit(X_train_scaled, self.obj.y_train.values)
        self.obj.best_hyperparams = {}


class CubistFitter(BaseFitter):
    """Cubist rule-based model fitter."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        self.obj.model.fit(X_train, self.obj.y_train)


class CumulativeFitter(BaseFitter):
    """Cumulative model fitter with special preprocessing."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        num_columns = self._get_num_columns()
        X_train_scaled = self._scale_cumulative_features(X_train, num_columns)
        
        self.obj.model.fit(X_train_scaled, self.obj.y_train)
    
    def _get_num_columns(self) -> int:
        """Extract number of columns from model name."""
        return int(self.obj.model_name.split("_")[1])
    
    def _scale_cumulative_features(
        self, 
        X_train: pd.DataFrame, 
        num_columns: int
    ) -> pd.DataFrame:
        """Scale numeric features and encode region."""
        scaler = StandardScaler()
        X_numeric = X_train.iloc[:, :num_columns]
        X_scaled_numeric = pd.DataFrame(
            scaler.fit_transform(X_numeric),
            columns=X_numeric.columns,
            index=X_train.index,
        )
        
        le = LabelEncoder()
        X_region = pd.Series(
            le.fit_transform(X_train["Region"]),
            name="Region",
            index=X_train.index,
        )
        
        return pd.concat([X_scaled_numeric, X_region], axis=1)


class DesregFitter(BaseFitter):
    """Desreg (Distributional regression) fitter."""
    
    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        self.obj.model.fit(X_train, self.obj.y_train)


class DefaultFitter(BaseFitter):
    """Default fitter for standard sklearn-like models."""

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        try:
            self.obj.model.fit(X_train, self.obj.y_train)
        except Exception as e:
            self.obj.logger.exception(
                f"Error fitting {self.obj.model_name} for "
                f"{self.obj.country} {self.obj.crop}: {e}"
            )
            raise