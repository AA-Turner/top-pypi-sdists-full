"""Geocif Dataclass — ML Pipeline Orchestrator.

Central class that reads CID data, engineers features, trains LOOCV
models, and stores predictions to SQLite. Instantiated and driven
by ``geocif_runner.run(cfg)``.
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
from tqdm.rich import tqdm

from geocif import logger as log
from geocif import utils
from geocif.progress import pbar as _pbar
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
        # Optional explicit training-window cutoff. None => fall back to
        # the default "drop the earliest year" behavior.
        _tsy_raw = self.parser.get("ML", "training_start_year", fallback="").strip()
        self.training_start_year = int(_tsy_raw) if _tsy_raw else None

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
        self.use_yield_trend_as_feature = self.parser.getboolean(
            "ML", "use_yield_trend_as_feature", fallback=False
        )
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
        self.run_time_steps = self.parser.get("ML", "run_time_steps", fallback="latest")
        # "current" means use today's partial-season stage window for ALL
        # years (operationally faithful hindcasts). Replaces the old
        # align_hindcast_stage flag.
        self.align_hindcast_stage = (self.run_time_steps == "current")
        # "pre_season" runs the model BEFORE the season starts using only
        # FLDAS/S2S forecast lead data. Init month is derived dynamically
        # from the current date at execution time.
        self.is_pre_season = (self.run_time_steps == "pre_season")
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
        self.run_cluster_analysis = (
            self.parser.getboolean("ML", "run_cluster_analysis")
            if self.parser.has_option("ML", "run_cluster_analysis") else False
        )
        self.cluster_analysis_proxy = (
            self.parser.get("ML", "cluster_analysis_proxy")
            if self.parser.has_option("ML", "cluster_analysis_proxy") else "AUC_NDVI"
        )
        self.cluster_analysis_max_k = (
            self.parser.getint("ML", "cluster_analysis_max_k")
            if self.parser.has_option("ML", "cluster_analysis_max_k") else 8
        )
        self.cluster_analysis_top_n = (
            self.parser.getint("ML", "cluster_analysis_top_n")
            if self.parser.has_option("ML", "cluster_analysis_top_n") else 20
        )
        self.cluster_analysis_variance = (
            self.parser.getfloat("ML", "cluster_analysis_variance")
            if self.parser.has_option("ML", "cluster_analysis_variance") else 0.85
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
            **di.dict_s2s,
            **di.dict_fldas_engineered,
            **di.dict_s2s_engineered,
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
        self.select_cid_by = self.parser.get(self.model_name, "select_cid_by")
        self.use_cids = ast.literal_eval(self.parser.get(self.model_name, "use_cids"))
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
        elif self.model_name in ["tabpfn", "tabpfn_ft", "desreg", "tabicl", "tabicl_ft"]:
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
        self.select_cid_by = "Index"
        self.use_cumulative_features = True

    def _setup_tabular_flags(self):
        """Flags for tabular models."""
        self.do_xai = self.parser.getboolean("ML", "do_xai", fallback=False)
        self.alpha = self.parser.getfloat("ML", "alpha")
        self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
        self.estimate_ci_for_all = self.parser.getboolean("ML", "estimate_ci_for_all")
        self.ci_method = self.parser.get("ML", "ci_method", fallback="crepes")
        self.cat_features = [col for col in self.cat_features]

    def _setup_tree_flags(self):
        """Flags for tree-based models."""
        self.do_xai = False
        self.estimate_ci = False
        self.cat_features = [col for col in self.cat_features]

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

        if self.is_pre_season:
            self.all_stages = ["PS"]
            self.simulation_stages = [np.array([0])]
            return

        if self.method.endswith("_r"):
            self._setup_reverse_stages()
        else:
            raise NotImplementedError(f"Method {self.method} not implemented")

        self._filter_current_month_stages()
        self._create_simulation_stages()

    def _setup_reverse_stages(self):
        """Setup stages for reverse methods.

        When ``align_hindcast_stage`` is True (yield_outlook's default),
        every hindcast forecast_season uses the same stage set as today's
        partial-season window — making stored predictions time-aligned
        across years instead of each year picking its own full-season
        latest stage.
        """
        use_today_stages = (
            self.align_hindcast_stage or self.forecast_season == self.today_year
        )
        if use_today_stages:
            mask = self.df_inputs["Harvest Year"] == self.today_year
            self.all_stages = self.df_inputs[mask]["Stage_ID"].unique()
        else:
            self.all_stages = self.df_inputs["Stage_ID"].unique()

    def _filter_current_month_stages(self):
        """Filter out current month stages for real-time forecasting.

        Applied whenever we're aligning to today's window — either because
        this IS today's forecast_season or because ``align_hindcast_stage``
        is forcing every hindcast year onto today's stage list.
        """
        if self.align_hindcast_stage or self.forecast_season == self.today_year:
            current_month = ar.utcnow().month
            self.all_stages = [
                elem for elem in self.all_stages
                if not elem.startswith(str(current_month))
            ]

    def _create_simulation_stages(self):
        """Create simulation stages from stage IDs (skip PS_ pre-season stages)."""
        self.simulation_stages = [
            np.array([int(stage) for stage in s.split("_")])
            for s in self.all_stages
            if not s.startswith(("PS", "IS"))
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
        """Standardize column names in geodata using config-driven mapping.

        Delegates to :func:`geocif.utils.load_country_boundary_gdf` for the
        rename / conflict-drop / Tanzania-fix block — except this method
        operates on an already-loaded GeoDataFrame (``self.dg``), so it
        inlines the same steps without re-reading the file.
        """
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
        """Add Country Region column for merging.

        When running at admin_1 but the shapefile contains admin_2 polygons,
        dissolve admin_2 geometries into admin_1 so each region has a single
        merged polygon rather than keeping one arbitrary admin_2 sliver.
        """
        if self.admin_zone == "admin_2" and "ADM2_NAME" in self.dg.columns:
            self.dg["Country Region"] = self.dg["ADM0_NAME"] + " " + self.dg["ADM2_NAME"]
        else:
            # Dissolve admin_2 → admin_1 if shapefile is finer than requested
            self.dg = utils.dissolve_to_admin1(self.dg)
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
        from geocif.utils import load_country_boundary_gdf

        all_gdf = []
        for country in countries:
            shp_file = self.parser.get(country, "boundary_file")
            dg = load_country_boundary_gdf(
                self.parser, self.dir_boundary_files / shp_file
            )
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

        self._apply_training_year_filter()

    def _get_statistics_file_path(self, country: str, crop: str) -> Path:
        """Get path to statistics file."""
        path = utils.statistics_file_path(self.dir_output, self.method, country, crop)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _create_statistics_file(self, country: str, crop: str, file_path: Path):
        """Create statistics file by combining CID data with yield statistics."""
        admin_zone = self.parser.get(country, "admin_level")
        country_str = country.title().replace("_", " ")
        crop_str = crop.title().replace("_", " ")
        
        _dir_country = (
            self.dir_output / "cid" / "indices" / self.method /
            admin_zone / country / crop
        )
        
        file_name = f"{country}_{crop}_s*.csv"
        all_files = list(_dir_country.glob(file_name))

        if not all_files:
            raise FileNotFoundError(
                f"No files found in {_dir_country} with pattern {file_name}"
            )
        
        self.df_inputs = pd.concat(
            (pd.read_csv(f, engine="pyarrow") 
             for f in _pbar(all_files, desc="Reading CSVs", leave=False)),
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

        self._apply_training_year_filter()

    def _rename_target_column(self):
        """Rename target column if configured."""
        self.df_inputs.rename(
            columns={self.target: self.new_name_target},
            inplace=True
        )
        self.target = self.new_name_target
        self.target_column = self.new_name_target

    def _apply_training_year_filter(self):
        """Trim df_inputs to the configured training window.

        Behavior:
          * ``self.training_start_year is None`` (default): drop the
            single earliest Harvest Year (boundary CID coverage is often
            partial when start_year predates an EO source's start date).
          * ``self.training_start_year = <int>``: filter to
            ``Harvest Year >= training_start_year``; an explicit value
            overrides the first-year drop.
        """
        if self.df_inputs is None or self.df_inputs.empty:
            return
        if "Harvest Year" not in self.df_inputs.columns:
            return

        before = len(self.df_inputs)
        if self.training_start_year is not None:
            cutoff = int(self.training_start_year)
            self.df_inputs = self.df_inputs[
                self.df_inputs["Harvest Year"] >= cutoff
            ].reset_index(drop=True)
            mode_msg = f"training_start_year={cutoff}"
        else:
            first_year = int(self.df_inputs["Harvest Year"].min())
            self.df_inputs = self.df_inputs[
                self.df_inputs["Harvest Year"] > first_year
            ].reset_index(drop=True)
            mode_msg = f"drop earliest year ({first_year})"

        dropped = before - len(self.df_inputs)
        if dropped:
            self.logger.info(
                f"  Training-year filter ({mode_msg}): dropped {dropped} rows"
            )

    # ============================================================================
    # MAIN EXECUTION PIPELINE
    # ============================================================================

    def execute(self):
        """
        Main execution pipeline - orchestrates the entire workflow.

        When ``run_time_steps`` is ``"all"`` or an integer N, the pipeline
        runs one model per time-step through the season.  Each step includes
        all Stage_IDs whose period numbers fall within [planting..current],
        so the feature set grows as the season progresses.

        For ``"latest"`` or ``"current"``, the original single-pass flow
        is used (all stages become feature columns in one model).
        """
        if self.is_pre_season or self._is_forecast_only():
            # Forecast-only CIDs (FLDAS/S2S) iterate init months across both
            # pre-season and in-season, since cumulative stage windows don't
            # produce distinct FLDAS features. Mixed/observational pre-season
            # runs stop at planting-1.
            self._execute_pre_season(include_in_season=self._is_forecast_only())
        elif self.run_time_steps in ("latest", "current"):
            self._execute_single_pass()
        else:
            self._execute_multi_step()

    def _execute_single_pass(self):
        """Original single-run pipeline — all stages as features."""
        df = self._prepare_ml_dataframe()
        df = self._add_lat_lon_to_data(df)

        self._run_spatial_autocorrelation_if_enabled()
        self._run_cluster_analysis(df)

        dict_selected_features, dict_best_cid = self._generate_correlation_plots(df)

        self._prepare_train_test_split(df)
        self._compute_detrended_yield()
        self._compute_yield_trend_feature()
        self._add_spatial_neighbor_features()

        if self.run_ml:
            self._execute_ml_pipeline(dict_selected_features, dict_best_cid)

    # ------------------------------------------------------------------
    # PRE-SEASON MODE
    # ------------------------------------------------------------------

    def _get_season_start_month(self) -> int:
        """Return the first month of the crop season from the loaded data.

        For reverse methods (monthly_r), the longest Stage_ID contains all
        season months in harvest→planting order, so reversed gives planting
        first.  For forward methods, the shortest single-stage ID is the
        planting month.
        """
        stage_ids = [
            s for s in self.df_inputs["Stage_ID"].dropna().unique()
            if not s.startswith(("PS", "IS"))
        ]
        if not stage_ids:
            return ar.utcnow().month

        # Longest stage contains the full season sequence
        longest = max(stage_ids, key=lambda s: len(s.split("_")))
        months = [int(x) for x in longest.split("_")]
        if self.method.endswith("_r"):
            months = list(reversed(months))
        return months[0]


    def _is_forecast_only(self) -> bool:
        """Check if use_cids contains only forecast types (FLDAS/S2S)."""
        from geocif.utils import is_forecast_only
        return is_forecast_only(self.use_cids)

    def _get_pre_season_init_months(self, include_in_season: bool = False) -> list[int]:
        """Pre-season init months for the ML stage.

        Thin wrapper around :func:`geocif.utils.get_pre_season_init_months` —
        single source of truth shared with the CID stage to avoid drift.
        """
        from geocif.utils import get_pre_season_init_months

        extend = ar.utcnow().month if include_in_season else None
        return get_pre_season_init_months(
            self._get_season_start_month(),
            extend_to_month=extend,
        )

    def _execute_pre_season(self, include_in_season: bool = False):
        """Pre-season pipeline — one model per init month, multi-step.

        Args:
            include_in_season: If True, extend month range through current
                month (for forecast-only mode).
        """
        init_months = self._get_pre_season_init_months(include_in_season=include_in_season)
        season_start = self._get_season_start_month()

        self.logger.info(
            f"Pre-season mode: {len(init_months)} time steps "
            f"(months {init_months[0]}→{init_months[-1]}, "
            f"season starts {season_start})"
        )

        df_inputs_orig = self.df_inputs.copy()
        cached_latlon = None

        # Debug file for pre-season diagnostics
        debug_dir = Path(self.parser.get("PATHS", "dir_output")) / self.parser.get("DEFAULT", "project_name", fallback="geocif") / "ml" / "debug"
        debug_dir.mkdir(parents=True, exist_ok=True)
        debug_rows = []

        # Log initial state
        unique_stages = sorted(df_inputs_orig["Stage"].dropna().unique())[:30]
        unique_stage_ids = sorted(df_inputs_orig["Stage_ID"].dropna().unique())[:30] if "Stage_ID" in df_inputs_orig.columns else []
        self.logger.info(
            f"Pre-season debug: df_inputs has {len(df_inputs_orig)} rows, "
            f"Stage dtype={df_inputs_orig['Stage'].dtype}, "
            f"unique Stages (first 30)={unique_stages}"
        )

        for step_idx, init_month in enumerate(init_months):
            month_name = ar.get(f"2000-{init_month:02d}-01").format("MMM")

            # Determine if this month is pre-season or in-season
            months_until_planting = (season_start - init_month) % 12
            is_before_planting = months_until_planting > 0 and months_until_planting <= 6

            if is_before_planting:
                stage_id = f"PS_{init_month}"
                stage_name = f"Pre-Season (init {month_name})"
                label_prefix = "PS"
            else:
                stage_id = f"IS_{init_month}"
                stage_name = f"In-Season (init {month_name})"
                label_prefix = "IS"

            self.stage_info = {
                "Stage_ID": stage_id,
                "CID": "PRE_SEASON" if is_before_planting else "IN_SEASON",
                "Stage Range": stage_id,
                "Starting Stage": 0,
                "Ending Stage": 0,
                "Stage Name": stage_name,
            }
            self._current_step_label = f"[{label_prefix} {step_idx + 1}/{len(init_months)}]"
            self.logger.info(
                f"Forecast step {self._current_step_label}: init {month_name}"
            )

            # Filter to this init month's features
            self.df_inputs = df_inputs_orig.copy()
            stage_pattern = f"PS_{init_month}"

            n_stage = int((self.df_inputs["Stage"] == stage_pattern).sum())
            n_stage_id = int((self.df_inputs["Stage_ID"] == stage_pattern).sum()) if "Stage_ID" in self.df_inputs.columns else -1
            n_fldas = int((self.df_inputs["Type"] == "FLDAS").sum())
            n_s2s = int((self.df_inputs["Type"] == "S2S").sum())

            # Respect use_cids: only include forecast types that are in use_cids
            if "all" in self.use_cids:
                forecast_types = ["FLDAS", "S2S"]
            else:
                forecast_types = [c for c in self.use_cids if c in ("FLDAS", "S2S")]
            df = self.df_inputs[
                (self.df_inputs["Type"].isin(forecast_types)) &
                (self.df_inputs["Stage"] == stage_pattern)
            ]

            debug_row = {
                "step": init_month,
                "month_name": month_name,
                "n_rows_stage_match": n_stage,
                "n_rows_stage_id_match": n_stage_id,
                "n_rows_type_fldas": n_fldas,
                "n_rows_type_s2s": n_s2s,
                "n_rows_after_filter": len(df),
                "stage_dtype": str(self.df_inputs["Stage"].dtype),
                "unique_stages_sample": str(unique_stages[:10]),
                "result": "",
            }

            if df.empty:
                debug_row["result"] = "empty_filter"
                debug_rows.append(debug_row)
                self.logger.warning(
                    f"No features for init month {month_name} "
                    f"(stage_match={n_stage}, stage_id_match={n_stage_id}), skipping"
                )
                continue

            df = self.create_ml_dataframe(df)
            debug_row["n_rows_after_ml"] = len(df)
            if df.empty:
                debug_row["result"] = "empty_ml"
                debug_rows.append(debug_row)
                continue

            debug_row["result"] = "success"
            debug_rows.append(debug_row)

            if cached_latlon is None:
                df = self._add_lat_lon_to_data(df)
                if "lat" in df.columns:
                    cached_latlon = df[["Country Region", "lat", "lon"]].drop_duplicates()
            else:
                df["Country Region"] = (
                    df["Country"].astype(str) + " " + df["Region"].astype(str)
                ).str.lower()
                df = df.merge(cached_latlon, on="Country Region", how="left")

            if step_idx == 0:
                self._run_cluster_analysis(df)

            dict_selected_features, dict_best_cid = self._generate_correlation_plots(df)

            self._prepare_train_test_split(df)
            self._compute_detrended_yield()
            self._compute_yield_trend_feature()
            self._add_spatial_neighbor_features()

            if self.run_ml:
                self._execute_ml_pipeline(dict_selected_features, dict_best_cid)

        self.df_inputs = df_inputs_orig

        # Write debug CSV
        if debug_rows:
            debug_df = pd.DataFrame(debug_rows)
            debug_path = debug_dir / f"pre_season_debug_{self.country}_{self.crop}.csv"
            debug_df.to_csv(debug_path, index=False)
            self.logger.info(f"Pre-season debug written to {debug_path}")

    def _execute_multi_step(self):
        """Multi-step pipeline — one model per time-step from planting forward."""
        all_simulation_stages = list(self.simulation_stages)
        step_subsets = self._get_setup_stages()

        df_inputs_orig = self.df_inputs.copy()
        cached_latlon = None

        for step_idx, stage_subset in enumerate(step_subsets):
            self.simulation_stages = stage_subset
            self.df_inputs = df_inputs_orig.copy()
            self._current_step_label = f"[{step_idx + 1}/{len(step_subsets)}]"

            self.logger.info(
                f"Time step {self._current_step_label}: "
                f"{len(stage_subset)} stages for {self.country} {self.crop}"
            )

            df = self._prepare_ml_dataframe()

            if cached_latlon is None:
                df = self._add_lat_lon_to_data(df)
                cached_latlon = df[["Country Region", "lat", "lon"]].drop_duplicates()
            else:
                df["Country Region"] = (
                    df["Country"].astype(str) + " " + df["Region"].astype(str)
                ).str.lower()
                df = df.merge(cached_latlon, on="Country Region", how="left")

            if step_idx == 0:
                self._run_spatial_autocorrelation_if_enabled()
                self._run_cluster_analysis(df)

            dict_selected_features, dict_best_cid = self._generate_correlation_plots(df)

            self._prepare_train_test_split(df)
            self._compute_detrended_yield()
            self._compute_yield_trend_feature()
            self._add_spatial_neighbor_features()

            if self.run_ml:
                self._execute_ml_pipeline(dict_selected_features, dict_best_cid)

        self.simulation_stages = all_simulation_stages

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
        df = self._filter_by_cid_categories(df)
        df = self._prune_stale_forecast_rows(df)
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

    def _prune_stale_forecast_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop FLDAS / S2S LEAD rows whose target month already has
        observed-climate rows in the same (Region, Harvest Year) slice.

        A FLDAS or S2S forecast row's ``Stage Name`` encodes its target
        month (e.g. ``"Feb 1-Feb 28"`` = LEAD targeting February). The
        dedup at CID extraction time keeps each ``(col, lead, init_month)``
        emitted once, with the Stage Name from the emitting cumulative
        stage. Once cumulative stages advance past that target month,
        observed-climate features (ICCLIM/AgERA5/ESI/NDVI) for the same
        Stage Name also exist in the slice — making the forecast stale.

        Rule: if any non-forecast row shares a row's
        ``(Region, Harvest Year, Stage Name)``, drop that forecast row.
        Forecasts whose target month has no observed counterpart yet
        (the Gauteng pre-season fallback case at 0.4.578) survive
        because no ICCLIM row carries their Stage Name yet.
        """
        if df.empty:
            return df
        needed = {"Type", "Stage Name", "Index", "Region", "Harvest Year"}
        if not needed.issubset(df.columns):
            return df

        forecast_mask = (
            df["Type"].isin(["FLDAS", "S2S"]) &
            df["Index"].fillna("").str.contains("_LEAD", regex=False)
        )
        if not forecast_mask.any():
            return df

        observed_keys = pd.MultiIndex.from_frame(
            df.loc[~forecast_mask, ["Region", "Harvest Year", "Stage Name"]]
            .drop_duplicates()
        )
        forecast_keys = pd.MultiIndex.from_frame(
            df.loc[forecast_mask, ["Region", "Harvest Year", "Stage Name"]]
        )
        stale_within_forecast = forecast_keys.isin(observed_keys)
        stale_idx = df.index[forecast_mask][stale_within_forecast]

        n_pruned = len(stale_idx)
        if n_pruned:
            self.logger.info(
                f"Pruning {n_pruned} stale FLDAS/S2S LEAD rows from "
                f"{self.country} {self.crop} (target month already observed)"
            )
        return df.drop(stale_idx)

    def _filter_by_cid_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter by selected CID categories."""
        if "all" in self.use_cids:
            return df

        if self.select_cid_by == "Type":
            return df[df["Type"].isin(self.use_cids)]
        elif self.select_cid_by == "Index":
            return df[df["Index"].isin(self.use_cids)]
        
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
        if self.run_time_steps not in ("latest", "current") and hasattr(self, "stage_info"):
            stage_name = self.stage_info.get("Stage Name", "")
            if stage_name:
                dir_output = dir_output / utils.friendly_stage_label(stage_name).replace(" - ", "-").replace(" ", "_")
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

    def _run_cluster_analysis(self, df: pd.DataFrame):
        """Run cluster analysis on region CID profiles."""
        if not self.run_cluster_analysis:
            return

        from .ml import cluster_analysis as ca

        dir_out = (
            self.dir_analysis / self.country / self.crop
            / self.model_name / str(self.forecast_season)
        )

        self.cluster_results = ca.run_cluster_analysis(
            df=df,
            dir_output=dir_out,
            target_col=self.target,
            proxy_prefix=self.cluster_analysis_proxy,
            gdf=getattr(self, "dg_country", None),
            countries=[self.country.title().replace("_", " ")] if self.country else None,
            max_clusters=self.cluster_analysis_max_k,
            top_n_cids=self.cluster_analysis_top_n,
            variance_threshold=self.cluster_analysis_variance,
            logger=self.logger,
        )

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

    def _compute_yield_trend_feature(self):
        """Compute per-region BEAST-segmented linear trend, write to
        ``Yield Trend`` column on both df_train and df_test.

        LOOCV-safe: only training data is used to fit BEAST + OLS; the
        forecast year is already excluded by ``_prepare_train_test_split``.
        """
        if not self.use_yield_trend_as_feature:
            return
        if self.check_yield_trend:
            self.logger.warning(
                "  use_yield_trend_as_feature is incompatible with "
                "check_yield_trend (target detrending). Skipping trend feature."
            )
            return

        import ast as _ast
        cp_threshold = self.parser.getfloat(
            "BEAST", "strong_cp_threshold", fallback=0.5
        )
        tcp_minmax = _ast.literal_eval(
            self.parser.get("BEAST", "tcp_minmax", fallback="[0, 8]")
        )
        tseg_minlength = self.parser.getint(
            "BEAST", "tseg_minlength", fallback=5
        )
        mcmc_seed = self.parser.getint(
            "BEAST", "mcmc_seed", fallback=42
        )

        self.df_train["Yield Trend"] = np.nan
        self.df_test["Yield Trend"] = np.nan

        for region_name, group in self.df_train.groupby("Region"):
            # .astype(float) is required: Harvest Year may be a pandas
            # Categorical (used by tree models that treat it as a cat
            # feature), and ``slope * Categorical`` raises TypeError.
            years = group["Harvest Year"].astype(float).values
            yields = group[self.target].astype(float).values
            intercept, slope, cp_used, n_used = trend.segment_aware_trend(
                years, yields,
                cp_threshold=cp_threshold,
                tcp_minmax=tcp_minmax,
                tseg_minlength=tseg_minlength,
                mcmc_seed=mcmc_seed,
            )
            if np.isnan(intercept):
                continue

            train_mask = self.df_train["Region"] == region_name
            test_mask = self.df_test["Region"] == region_name
            tr_yrs = self.df_train.loc[train_mask, "Harvest Year"].astype(float).values
            te_yrs = self.df_test.loc[test_mask, "Harvest Year"].astype(float).values
            self.df_train.loc[train_mask, "Yield Trend"] = intercept + slope * tr_yrs
            self.df_test.loc[test_mask, "Yield Trend"] = intercept + slope * te_yrs

            self.logger.info(
                f"  Yield Trend [{region_name}]: "
                f"slope={slope:.4f} t/ha/yr, n_used={n_used}, "
                f"cp_used={cp_used}"
            )

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

    def _execute_ml_pipeline(self, dict_selected_features: Dict, dict_best_cid: Dict):
        """Execute the machine learning training pipeline.

        Uses ``self.simulation_stages`` as-is — a single model run using
        all stages in the list as feature columns.  When called from
        ``_execute_multi_step``, the stages have already been set to the
        subset for the current time step.
        """
        self.logger.info(f"Running ML for {self.country} {self.crop}")

        num_regions = len(self.df_train["Region_ID"].unique())
        step_label = getattr(self, "_current_step_label", "")
        stage_name = getattr(self, "stage_info", {}).get("Stage Name", "")

        pbar = _pbar([self.simulation_stages])
        for stages in pbar:
            pbar.set_description(
                f"{step_label} {self.country} {self.crop} {self.forecast_season} "
                f"({num_regions} reg, {len(stages)} stg) "
                f"{stage_name} {self.model_name}"
            )

            try:
                self.loop_ml(stages, dict_selected_features, dict_best_cid)
            except Exception as e:
                self.logger.error(f"Error in ML loop: {e}")

    def _get_setup_stages(self) -> List[List]:
        """Build per-time-step stage subsets for multi-step execution.

        For ``run_time_steps = all`` or ``N``, returns a list of stage
        subsets.  Each subset contains ALL Stage_IDs whose period numbers
        fall within a growing window from planting forward.

        The chronological order is derived from the longest Stage_ID
        (which contains the full season sequence).  For ``_r`` methods,
        Stage_ID arrays are ordered harvest→planting, so reversing gives
        the planting-forward order.  This handles cross-year seasons
        (e.g., Oct→Apr = ``[10, 11, 12, 1, 2, 3, 4]``) without assuming
        contiguous integer ranges.

        Returns:
            List of stage subsets (each a list of numpy arrays).
        """
        if not self.simulation_stages:
            return [self.simulation_stages]

        # Find the longest stage — it contains the full season sequence
        longest = max(self.simulation_stages, key=lambda s: len(s))
        # Reverse: harvest→planting becomes planting→harvest
        chronological = list(reversed([int(x) for x in longest]))

        if len(chronological) <= 1:
            return [self.simulation_stages]

        step = 1
        if self.run_time_steps != "all":
            try:
                step = int(self.run_time_steps)
            except ValueError:
                return [self.simulation_stages]

        # Build progression: cumulative prefixes of chronological order
        subsets = []
        for i in range(step, len(chronological) + 1, step):
            allowed = set(chronological[:i])
            subset = [
                s for s in self.simulation_stages
                if all(int(x) in allowed for x in s)
            ]
            if subset:
                subsets.append(subset)

        # Ensure the last step includes the full season
        all_periods = set(chronological)
        full_subset = [
            s for s in self.simulation_stages
            if all(int(x) in all_periods for x in s)
        ]
        if not subsets or len(subsets[-1]) < len(full_subset):
            subsets.append(full_subset)

        return subsets

    # ============================================================================
    # ML DATAFRAME CREATION
    # ============================================================================

    def create_ml_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create ML-ready dataframe from long format CID data.

        Args:
            df: Input dataframe with CID data
            
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
            ["Index", "Stage_ID", "CID"]
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
            values="CID",
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
        all_cid_columns = self.get_cid_column_names(df)

        if not all_cid_columns:
            return df

        parts = all_cid_columns[-1].split("_")
        skip = 2 if parts[0] == "AEF" else 1
        first_stage_idx = next(
            (i for i in range(skip, len(parts)) if parts[i].isdigit()),
            len(parts),
        )
        cid = "_".join(parts[:first_stage_idx])

        cid_column = df[df.columns[df.columns.str.contains(cid)]].columns
        max_cid_col = max(cid_column, key=len)

        # Don't overwrite pre-season stage_info (which carries the init month)
        if not self.is_pre_season:
            self.stage_info = stages.get_stage_information_dict(max_cid_col, self.method)

        return df

    def _create_cumulative_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create cumulative features for each region."""
        all_cid_columns = self.get_cid_column_names(df)

        if not all_cid_columns:
            return df

        parts = all_cid_columns[-1].split("_")
        skip = 2 if parts[0] == "AEF" else 1
        first_stage_idx = next(
            (i for i in range(skip, len(parts)) if parts[i].isdigit()),
            len(parts),
        )
        cid = "_".join(parts[:first_stage_idx])
        
        frames = []
        groups = df.groupby(["Region"])
        
        for name, group in groups:
            group = group.dropna(axis=1, how="all")
            
            cid_column = group[group.columns[group.columns.str.contains(cid)]].columns

            if not len(cid_column):
                continue

            max_cid_col = max(cid_column, key=len)
            if not self.is_pre_season:
                self.stage_info = stages.get_stage_information_dict(max_cid_col, self.method)

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
                    col: stages.get_stage_information_dict(col, self.method)["CID"]
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

        # update_feature_names can collapse distinct raw columns to the same
        # label (different stage numbers mapping to the same stage name).
        # pandas forbids .loc[:, cols] assignment when columns are non-unique,
        # so drop duplicates keeping the first occurrence.
        if df.columns.duplicated().any():
            dupes = df.columns[df.columns.duplicated()].unique().tolist()
            self.logger.warning(
                f"  Duplicate columns after rename: {dupes} — keeping first occurrence"
            )
            df = df.loc[:, ~df.columns.duplicated()]

        all_cid_columns = self.get_cid_column_names(df)
        df.loc[:, all_cid_columns] = df.loc[:, all_cid_columns].fillna(0)

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
        elif self.cluster_strategy == "crop_calendar":
            clusters_assigned = self._cluster_by_crop_calendar(df)
            df = df.merge(clusters_assigned, on="Region")
            df["Region_ID"] = df["Region_ID"].astype("category")
        elif self.cluster_strategy == "crop_calendar_yield":
            clusters_assigned = self._cluster_by_calendar_then_yield(df)
            df = df.merge(clusters_assigned, on="Region")
            df["Region_ID"] = df["Region_ID"].astype("category")
        else:
            raise ValueError(f"Unsupported cluster strategy {self.cluster_strategy}")

        return df

    def _cluster_by_crop_calendar(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cluster regions by their crop calendar — regions with the same
        set of non-NaN CID feature columns get the same Region_ID.

        This ensures regions sharing a model have comparable CID feature
        coverage (same growing season months), unlike yield-based clustering
        which can group regions with different calendars.

        Returns:
            DataFrame with columns ["Region", "Region_ID"].
        """
        cid_cols = self.get_cid_column_names(df)
        if not cid_cols:
            return pd.DataFrame({"Region": df["Region"].unique(), "Region_ID": 0})

        # For each region, compute which CID columns have data
        region_profiles = {}
        for region in df["Region"].unique():
            mask = df["Region"] == region
            non_null = frozenset(
                col for col in cid_cols
                if df.loc[mask, col].notna().any()
            )
            region_profiles[region] = non_null

        # Assign cluster IDs: regions with identical non-null column sets
        # share the same cluster
        unique_profiles = {}
        cluster_id = 0
        region_to_cluster = {}

        for region, profile in region_profiles.items():
            if profile not in unique_profiles:
                unique_profiles[profile] = cluster_id
                cluster_id += 1
            region_to_cluster[region] = unique_profiles[profile]

        self.logger.info(
            f"Crop calendar clustering: {len(region_to_cluster)} regions "
            f"→ {cluster_id} clusters"
        )

        return pd.DataFrame({
            "Region": list(region_to_cluster.keys()),
            "Region_ID": list(region_to_cluster.values()),
        })

    def _cluster_by_calendar_then_yield(self, df: pd.DataFrame) -> pd.DataFrame:
        """Two-stage clustering: first by crop calendar, then by yield within
        each calendar group.

        1. Partition regions by CID feature coverage (crop calendar).
           Regions with different calendars can never share a cluster.
        2. Within each calendar group, sub-cluster by yield patterns
           using K-Means (same as auto_detect).

        Returns:
            DataFrame with columns ["Region", "Region_ID"].
        """
        # Stage 1: calendar partitions
        cal_clusters = self._cluster_by_crop_calendar(df)
        cal_groups = cal_clusters.groupby("Region_ID")["Region"].apply(list).to_dict()

        region_to_final = {}
        final_id = 0

        for cal_id, regions in cal_groups.items():
            if len(regions) <= 1:
                # Single region in this calendar group — its own cluster
                for r in regions:
                    region_to_final[r] = final_id
                final_id += 1
                continue

            # Stage 2: yield-based sub-clustering within this calendar group
            df_group = df[df["Region"].isin(regions)]
            try:
                sub_clusters = fe.detect_clusters(df_group, self.target)
                for _, row in sub_clusters.iterrows():
                    region_to_final[row["Region"]] = final_id + row["Region_ID"]
                final_id += sub_clusters["Region_ID"].nunique()
            except Exception:
                # Fallback: all regions in this calendar group share one cluster
                for r in regions:
                    region_to_final[r] = final_id
                final_id += 1

        self.logger.info(
            f"Calendar+yield clustering: {len(region_to_final)} regions "
            f"→ {final_id} clusters "
            f"({len(cal_groups)} calendar groups)"
        )

        return pd.DataFrame({
            "Region": list(region_to_final.keys()),
            "Region_ID": list(region_to_final.values()),
        })

    def get_cid_column_names(self, df: pd.DataFrame) -> List[str]:
        """Get list of CID column names (excluding fixed/target/meta/engineered columns)."""
        return utils.filter_cid_columns(df, self.fixed_columns, self.target, self.statistics_columns)

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
                cid = "_".join(parts[:_idx])

                try:
                    if self.model_name.startswith("cumulative_"):
                        dict_fn = stages.get_stage_information_dict(_t, self.method)
                        tmp_col = f"{dict_fn['CID']}"

                        if tmp_col in self.df_train.columns:
                            self.feature_names.append(tmp_col)
                    else:
                        if selected_features["CID"].any():
                            for x in selected_features["CID"].values:
                                if x not in cid:
                                    continue

                                dict_fn = stages.get_stage_information_dict(_t, self.method)
                                tmp_col = f"{dict_fn['CID']} {dict_fn['Stage Name']}"
                                
                                if tmp_col in self.df_train.columns:
                                    self.feature_names.append(tmp_col)
                except Exception as e:
                    self.logger.error(f"Error creating feature name for {_t}: {e}")
        
        self.feature_names = list(set(self.feature_names))
        
        if self.median_yield_as_feature:
            self.feature_names.append(f"Median {self.target}")

        if self.use_yield_trend_as_feature and "Yield Trend" in self.df_train.columns:
            self.feature_names.append("Yield Trend")
        
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
        # Lag-only mode: ignore CID features entirely, keep just the
        # lag-yield columns plus cat_features. Set by yield_outlook.run()
        # when run_time_steps == "lag_only". Baseline mode that strips
        # every CID feature so we can measure pure lag-yield baseline.
        if self.parser.getboolean("ML", "lag_only_features", fallback=False):
            X_for = self.X_train.drop(columns=["Region"], errors="ignore")
            lag_cols = [
                c for c in X_for.columns
                if c.startswith("t -") and "Yield" in c
            ]
            cat_extras = [
                c for c in self.cat_features
                if c != "Region" and c in X_for.columns
            ]
            self.selected_features = lag_cols + cat_extras
            self.logger.info(
                f"Lag-only mode for {self.country} {self.crop}: "
                f"using {len(self.selected_features)} features "
                f"({len(lag_cols)} lag + {len(cat_extras)} cat)"
            )
            return

        # Pre-season and in-season-init stages have a tiny, mostly
        # region-constant feature pool (lag yields + MAR_FLDAS_*).
        # Feature selection adds overhead with no signal — bypass and
        # use every column, regardless of the configured method.
        stage_id = str(getattr(self, "stage_info", {}).get("Stage_ID", ""))
        if getattr(self, "is_pre_season", False) or stage_id.startswith(("PS_", "IS_")):
            X_for_selection = self.X_train.drop(columns=["Region"], errors="ignore")
            self.selected_features = X_for_selection.columns.tolist()
            self.logger.info(
                f"Skipping feature selection for {self.country} {self.crop} "
                f"(pre-season stage {stage_id or 'PS'}); using all "
                f"{len(self.selected_features)} features"
            )
            return

        if self.model_name.startswith("cumulative_"):
            all_features = self.X_train.columns
            self.selected_features = [
                column for column in all_features
                if any(cid in column for cid in self.use_cids)
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

        # Force-include FLDAS / S2S forecast CIDs back into the selected set
        # even if the feature-selection method (gOMP/Boruta/etc.) dropped
        # them. Gated by:
        #   1. [ML] force_include_forecast_cids (default True) — master
        #      switch. When False, forecast CIDs are subject to the
        #      configured feature-selection method like any other feature.
        #   2. [DEFAULT] use_cids — only forecast types the user opted
        #      into are protected.
        # End-of-season cap is applied at CID extraction time
        # (geocif/cid/indices.py:1396-1417), so anything present in
        # X_train.columns has already been bounded to the growing season
        # for this region. Stale forecasts (target month already observed)
        # are pruned in _prune_stale_forecast_rows before pivot.
        force_include = self.parser.getboolean(
            "ML", "force_include_forecast_cids", fallback=True
        )
        keep_fldas = force_include and ("all" in self.use_cids or "FLDAS" in self.use_cids)
        keep_s2s = force_include and ("all" in self.use_cids or "S2S" in self.use_cids)
        if (keep_fldas or keep_s2s) and hasattr(self, "X_train") and self.X_train is not None:
            existing = set(self.selected_features)
            forced = []
            for col in self.X_train.columns:
                if col in existing or col == "Region":
                    continue
                is_fldas = "_FLDAS_" in col
                is_s2s = "_S2S_" in col
                if (is_fldas and keep_fldas) or (is_s2s and keep_s2s):
                    forced.append(col)
            if forced:
                self.selected_features = self.selected_features + forced
                self.logger.info(
                    f"Force-included {len(forced)} FLDAS/S2S forecast CIDs "
                    f"for {self.country} {self.crop} after selection "
                    f"(use_cids={self.use_cids})"
                )

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
        X_test = df_region[self.selected_features + self.cat_features].copy()
        num_cols = X_test.select_dtypes(include=[np.number]).columns
        if len(num_cols):
            inf_mask = ~np.isfinite(X_test[num_cols].to_numpy())
            if inf_mask.any():
                bad = list(num_cols[inf_mask.any(axis=0)])
                self.logger.info(
                    f"Replacing ±inf with NaN in {len(bad)} test column(s): "
                    f"{bad[:10]}{'...' if len(bad) > 10 else ''}"
                )
                X_test[num_cols] = X_test[num_cols].replace([np.inf, -np.inf], np.nan)
        y_test = df_region[self.target].values

        y_pred, y_pred_ci, best_hyperparameters = self._run_prediction(
            X_test, df_region, scaler
        )
        
        if self.check_yield_trend:
            y_pred, y_pred_ci = self._retrend_predictions(y_pred, df_region, y_pred_ci)

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
        if self.model_name == "linear":
            X_test = X_test.drop(
                columns=[item for item in self.cat_features if item != "Harvest Year"]
            )
            return scaler.transform(X_test)

        if self.model_name == "gam":
            # Align to GAMFitter's surviving fit columns (Harvest Year /
            # Region_ID / Region dropped).  No rescaling — pygam splines
            # handle raw numeric ranges.
            fit_cols = getattr(self, "_gam_fit_cols", None)
            if fit_cols is not None:
                return X_test.reindex(columns=fit_cols)
            return X_test.drop(columns=list(GAMFitter._DROP_COLS), errors="ignore")

        if self.model_name == "cubist":
            # Align to the surviving fit-time columns (zero-variance cols
            # were dropped in CubistFitter.fit to avoid "attribute X has
            # only one value Y" errors from Cubist's .names spec).  Also
            # fill NaNs — Cubist's C wrapper barfs on float-NaN in
            # string-coerced columns at predict time.
            fit_cols = getattr(self, "_cubist_fit_cols", None)
            X = X_test.reindex(columns=fit_cols) if fit_cols is not None else X_test.copy()

            num_medians = getattr(self, "_cubist_num_medians", None)
            num_cols = X.select_dtypes(include=["number"]).columns
            obj_cols = X.select_dtypes(exclude=["number"]).columns
            if len(num_cols):
                fill = num_medians.reindex(num_cols) if num_medians is not None else X[num_cols].median()
                X[num_cols] = X[num_cols].fillna(fill).fillna(0)
            if len(obj_cols):
                X[obj_cols] = X[obj_cols].astype("object").fillna("__missing__")
            return X

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
        """TabPFN native quantile regression for prediction intervals.

        Returns the median (q=0.5) as the point estimate so it is always
        consistent with the [lower_q, upper_q] interval bounds drawn from
        the same posterior.  Using the mean would allow predicted to fall
        outside the interval for skewed posteriors.
        """
        lower_q = self.alpha / 2
        upper_q = 1.0 - self.alpha / 2

        q_preds = self.model.predict(
            X_test, output_type="quantiles", quantiles=[lower_q, 0.5, upper_q]
        )

        n_samples = len(X_test)
        q_arr = np.asarray(q_preds)
        self.logger.debug(f"  TabPFN quantile raw type={type(q_preds)}, array shape={q_arr.shape}")
        if q_arr.ndim == 2 and q_arr.shape == (n_samples, 3):
            lower, median, upper = q_arr[:, 0], q_arr[:, 1], q_arr[:, 2]
        elif q_arr.ndim == 2 and q_arr.shape == (3, n_samples):
            lower, median, upper = q_arr[0], q_arr[1], q_arr[2]
        else:
            lower = np.asarray(q_preds[0]).reshape(-1)
            median = np.asarray(q_preds[1]).reshape(-1)
            upper = np.asarray(q_preds[-1]).reshape(-1)

        assert median.shape == (n_samples,), (
            f"TabPFN median shape {median.shape} != expected ({n_samples},)"
        )

        # Enforce F^-1 monotonicity — TabPFN's bar-distribution quantile
        # estimation can produce numerically non-monotone output for skewed
        # posteriors.  Sorting per-row restores the invariant without
        # changing any of the returned values.
        stacked = np.stack([lower, median, upper], axis=1)
        violations = int(
            (stacked[:, 0] > stacked[:, 1]).sum()
            + (stacked[:, 1] > stacked[:, 2]).sum()
        )
        if violations:
            self.logger.warning(
                f"TabPFN non-monotone quantiles in {violations} sample(s); "
                "sorting to restore F^-1 monotonicity invariant."
            )
            stacked.sort(axis=1)
        lower, median, upper = stacked[:, 0], stacked[:, 1], stacked[:, 2]

        y_pred = median
        y_pred_ci = np.stack([lower, upper], axis=1)[:, :, np.newaxis]
        self.logger.debug(f"  TabPFN CI shape={y_pred_ci.shape}, sample[0]: [{lower[0]:.3f}, {median[0]:.3f}, {upper[0]:.3f}]")

        return y_pred, y_pred_ci, {}

    def _predict_tabicl_with_quantiles(self, X_test: pd.DataFrame) -> Tuple:
        """TabICL native quantile regression for prediction intervals.

        Returns the median (q=0.5) as the point estimate so it is always
        consistent with the [lower_q, upper_q] interval bounds drawn from
        the same posterior.
        """
        lower_q = self.alpha / 2
        upper_q = 1.0 - self.alpha / 2

        q_preds = self.model.predict(
            X_test, output_type="quantiles", alphas=[lower_q, 0.5, upper_q]
        )

        n_samples = len(X_test)
        q_arr = np.asarray(q_preds)
        self.logger.debug(f"  TabICL quantile raw type={type(q_preds)}, array shape={q_arr.shape}")
        if q_arr.ndim == 2 and q_arr.shape == (n_samples, 3):
            lower, median, upper = q_arr[:, 0], q_arr[:, 1], q_arr[:, 2]
        elif q_arr.ndim == 2 and q_arr.shape == (3, n_samples):
            lower, median, upper = q_arr[0], q_arr[1], q_arr[2]
        else:
            lower = np.asarray(q_preds[0]).reshape(-1)
            median = np.asarray(q_preds[1]).reshape(-1)
            upper = np.asarray(q_preds[-1]).reshape(-1)

        assert median.shape == (n_samples,), (
            f"TabICL median shape {median.shape} != expected ({n_samples},)"
        )

        # Enforce F^-1 monotonicity — see comment in TabPFN branch.
        stacked = np.stack([lower, median, upper], axis=1)
        violations = int(
            (stacked[:, 0] > stacked[:, 1]).sum()
            + (stacked[:, 1] > stacked[:, 2]).sum()
        )
        if violations:
            self.logger.warning(
                f"TabICL non-monotone quantiles in {violations} sample(s); "
                "sorting to restore F^-1 monotonicity invariant."
            )
            stacked.sort(axis=1)
        lower, median, upper = stacked[:, 0], stacked[:, 1], stacked[:, 2]

        y_pred = median
        y_pred_ci = np.stack([lower, upper], axis=1)[:, :, np.newaxis]
        self.logger.debug(f"  TabICL CI shape={y_pred_ci.shape}, sample[0]: [{lower[0]:.3f}, {median[0]:.3f}, {upper[0]:.3f}]")

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
        df_region: pd.DataFrame,
        y_pred_ci: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Add trend back to detrended predictions and CI bounds.

        Both the point estimate and (if provided) the lower/upper CI bounds
        live in detrended space.  Retrending them with the same per-region
        transform keeps the invariant ``lower ≤ y_pred ≤ upper`` — without
        this, the point estimate moves to trend-space while the CI stays in
        anomaly-space, which breaks downstream error-bar plots with
        ``xerr must not contain negative values``.
        """
        y_pred_retrended = y_pred.copy()
        y_pred_ci_retrended = y_pred_ci.copy() if y_pred_ci is not None else None

        def _apply(val_scalar, yei=None, trend_value=None, model_type="gaussian"):
            if model_type == "gaussian":
                return yei * (1 + val_scalar / 100.0)
            return val_scalar + trend_value

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
                    y_pred_retrended[ri] = _apply(y_pred[ri], yei=yei, model_type="gaussian")
                    if y_pred_ci_retrended is not None:
                        y_pred_ci_retrended[ri, 0, 0] = _apply(y_pred_ci[ri, 0, 0], yei=yei, model_type="gaussian")
                        y_pred_ci_retrended[ri, 1, 0] = _apply(y_pred_ci[ri, 1, 0], yei=yei, model_type="gaussian")
                else:
                    obj_trend = trend.DetrendedData(
                        df_tmp[f"Detrended {self.target}"],
                        df_tmp["Detrended Model"],
                        df_tmp["Detrended Model Type"],
                    )
                    trend_value = trend.compute_trend(
                        obj_trend, df_region.iloc[ri][["Harvest Year"]]
                    )[0]
                    y_pred_retrended[ri] = _apply(y_pred[ri], trend_value=trend_value, model_type="other")
                    if y_pred_ci_retrended is not None:
                        y_pred_ci_retrended[ri, 0, 0] = _apply(y_pred_ci[ri, 0, 0], trend_value=trend_value, model_type="other")
                        y_pred_ci_retrended[ri, 1, 0] = _apply(y_pred_ci[ri, 1, 0], trend_value=trend_value, model_type="other")

                df_region.iloc[ri, df_region.columns.get_loc("Detrended Model Type")] = model_type

        return y_pred_retrended, y_pred_ci_retrended

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
        # Always materialize CI columns (as NaN when skipped) so the DB
        # schema is stable across iterations.  Without this, the first
        # row written can create a table without these columns and a
        # later iteration with real CI values fails with
        # "no column named alpha".
        if self.model_type == "REGRESSION":
            for col in ("alpha", "lower CI", "upper CI"):
                if col not in df.columns:
                    df.loc[:, col] = np.nan
        else:
            if "alpha" not in df.columns:
                df.loc[:, "alpha"] = np.nan
            if "CI" not in df.columns:
                df.loc[:, "CI"] = np.nan

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
        dict_best_cid: Dict
    ):
        """
        Main ML loop - orchestrates training and prediction for all regions.

        Args:
            stages: List of stages to use
            dict_selected_features: Selected features per region
            dict_best_cid: Best CID features per region
        """
        dir_output = self._get_output_directory()
        scaler = self._initialize_scaler()
        
        region_ids = self.df_train["Region_ID"].unique()
        pbar = _pbar(region_ids, leave=False)
        
        for idx, region_id in enumerate(pbar):
            try:
                self._process_single_region(
                    region_id, idx, stages, dict_selected_features,
                    dict_best_cid, dir_output, scaler, pbar
                )
            except Exception as e:
                self.logger.error(f"Error processing region {region_id}: {e}\n{traceback.format_exc()}")

    def _get_output_directory(self) -> Path:
        """Get output directory for current model/season/stage."""
        base = self.dir_analysis
        if self.experiment_name != "default":
            base = base / self.experiment_name / "runs"
        dir_output = (
            base / self.country / self.crop /
            self.model_name / str(self.forecast_season)
        )
        # Add stage subdirectory when running multi-step
        if self.run_time_steps not in ("latest", "current") and hasattr(self, "stage_info"):
            stage_name = self.stage_info.get("Stage Name", "")
            if stage_name:
                dir_output = dir_output / utils.friendly_stage_label(stage_name).replace(" - ", "-").replace(" ", "_")
        dir_output.mkdir(parents=True, exist_ok=True)
        return dir_output

    def _initialize_scaler(self):
        """Initialize scaler if needed.

        GAM does not need pre-scaling — pygam's splines are scale-invariant
        (knots adapt to data range) and ``f()`` factor terms require raw
        integer levels, not standard-scaled values.  Handling scaling
        outside the model would break ``f()`` on Harvest Year.
        """
        if self.model_name == "linear":
            return StandardScaler()
        return None

    def _process_single_region(
        self,
        region_id: int,
        idx: int,
        stages: list,
        dict_selected_features: Dict,
        dict_best_cid: Dict,
        dir_output: Path,
        scaler,
        pbar
    ):
        """Process training and prediction for a single region."""
        self._create_feature_names_for_region(
            region_id, stages, dict_selected_features, dict_best_cid
        )

        df_region_train, df_region_test = self._prepare_region_data(region_id)
        
        if df_region_train.empty:
            self.logger.warning(f"No training data for region {region_id}")
            return

        if df_region_test.empty:
            self.logger.warning(
                f"No test data for region {region_id} "
                f"forecast_season={self.forecast_season}; skipping predict()"
            )
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
        dict_best_cid: Dict
    ):
        """Create feature names based on model type and region."""
        if self.model_name == "linear":
            selected = dict_best_cid[region_id][0:3].tolist()
            self.create_feature_names(stages, selected)
        elif self.model_name.startswith("cumulative_"):
            self.create_feature_names(stages, {})
        elif self.ml_model:
            selected = dict_selected_features.get(region_id)
            if selected is not None and not selected.empty:
                self.create_feature_names(stages, selected)
            else:
                # No correlation-based selection — use all CID features
                self.feature_names = self.get_cid_column_names(self.df_train)
        elif self.model_name == "median":
            self.feature_names = [f"Median {self.target}"]
            self.last_year_yield_as_feature = False
            self.analogous_year_yield_as_feature = False
        elif self.model_name == "analog":
            self.feature_names = ["Analogous Year", "Analogous Year Yield"]
            self.last_year_yield_as_feature = False
            self.median_yield_as_feature = False
            # Lazy-compute the analogous columns if the config didn't
            # request them up-front.  Required for the analog baseline to
            # work out of the box — otherwise df_train / df_test would be
            # missing "Analogous Year Yield" and _extract_region_subset
            # would KeyError on per-region extraction.
            if "Analogous Year Yield" not in self.df_train.columns:
                self.df_train = fe.compute_analogous_yield(
                    self.df_train, self.all_seasons_with_yield,
                    self.number_median_years, self.target,
                )
                self.df_test = fe.compute_analogous_yield(
                    self.df_test, self.all_seasons_with_yield,
                    self.number_median_years, self.target,
                )
            self.analogous_year_yield_as_feature = True

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

        # Several paths can add the same column: `Median {target}` is appended
        # unconditionally above AND also ends up in self.feature_names when
        # median_yield_as_feature=True (geocif.py:1308).  Selecting both copies
        # from df produces a DataFrame with duplicate column names which breaks
        # downstream `X[num_cols] = X[num_cols].fillna(...)` in feature
        # selection with "Columns must be same length as key".
        return list(dict.fromkeys(common_columns))

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
        """Replace ±inf with NaN, drop columns with NaN, preserve lag/neighbor cols.

        Inf can leak in from feature paths that bypass the per-feature
        ``np.isfinite`` guard in ``cid/indices.py`` (REV/MAR division on
        repeated forecasts, neighbor-correlation features on constant series,
        etc.).  Sanitizing at this boundary catches all sources at once and
        lets the existing NaN-handling decide whether to drop or impute.
        """
        inf_mask = ~np.isfinite(X_train.select_dtypes(include=[np.number]).to_numpy())
        if inf_mask.any():
            num_cols = X_train.select_dtypes(include=[np.number]).columns
            bad = list(num_cols[inf_mask.any(axis=0)])
            self.logger.info(
                f"Replacing ±inf with NaN in {len(bad)} train column(s): "
                f"{bad[:10]}{'...' if len(bad) > 10 else ''}"
            )
            X_train = X_train.replace([np.inf, -np.inf], np.nan)

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
        """Fill missing values for models that can't handle NaN.

        Median for numerics (undefined on Categorical).  Mode (most common
        level) for categoricals/objects — same behavior as sklearn
        ``SimpleImputer(strategy='most_frequent')``.
        """
        for col in self.X_train.columns:
            s = self.X_train[col]
            if s.isna().sum() == 0:
                continue
            if pd.api.types.is_numeric_dtype(s):
                fill = s.median()
            else:
                mode = s.mode(dropna=True)
                if not mode.empty:
                    fill = mode.iloc[0]
                elif hasattr(s, "cat") and len(s.cat.categories):
                    fill = s.cat.categories[0]
                else:
                    fill = ""
            self.X_train[col] = s.fillna(fill)

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
            save_model_blobs = self.parser.getboolean(
                "ML", "save_model_blobs", fallback=False
            )
            output.store(
                self.db_path, experiment_id, df, model, self.model_name,
                save_model_blobs=save_model_blobs,
            )
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

        # Conformal calibrate/conformalize expects the same input space
        # the inner model was trained on.  For scaled models (``linear``)
        # that's ``X_train_scaled`` — a numpy array with cat_features
        # (except Harvest Year) dropped.  Passing raw ``X_train`` would
        # feed an unscaled, wrong-width DataFrame into LassoCV.predict
        # during calibration, producing either a dimension error or
        # silently meaningless prediction intervals.
        X_for_cal = X_train_scaled if scaler is not None else X_train
        self._add_confidence_intervals_if_needed(X_for_cal)
    
    def _prepare_training_data(self, df_region: pd.DataFrame) -> pd.DataFrame:
        """Extract and prepare features for training."""
        return df_region[self.obj.selected_features + self.obj.cat_features]
    
    def _save_training_data(
        self,
        X_train: pd.DataFrame,
        df_region: pd.DataFrame,
        dir_output: Path
    ):
        """Save training data for debugging/analysis.

        Adds a ``Region`` column to the saved CSV for human inspection —
        models like tabpfn/tabicl strip Region from cat_features, so without
        this the CSV has no way to identify which admin each row belongs to.
        The X_train matrix passed to model.fit() is untouched.
        """
        region_id = df_region["Region_ID"].unique()[0]
        df_save = X_train.copy()
        if "Region" in df_region.columns and "Region" not in df_save.columns:
            df_save.insert(0, "Region", df_region["Region"].values)
        df_save.to_csv(dir_output / f"X_train_{region_id}.csv", index=False)
    
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
            self.obj.optimize,
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
            "tabicl_ft": TabICLFTFitter(self.obj),
            "tabpfn_ft": TabPFNFTFitter(self.obj),
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
        from catboost import Pool
        from sklearn.model_selection import train_test_split

        train_X, val_X, train_y, val_y = train_test_split(
            X_train, self.obj.y_train, test_size=0.2, random_state=42,
        )
        train_pool = Pool(train_X, train_y, cat_features=self.obj.cat_features)
        val_pool = Pool(val_X, val_y, cat_features=self.obj.cat_features)

        self.obj.model.fit(
            train_pool,
            eval_set=val_pool,
            use_best_model=True,
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


class TabPFNFTFitter(BaseFitter):
    """FinetunedTabPFNRegressor — needs X_val/y_val for early stopping.

    Holds out a fraction of X_train as the validation set passed to
    ``model.fit(X, y, X_val=, y_val=)``.  Fraction is configurable via
    ``[ML] tabpfn_ft_val_frac`` (default 0.2).

    Best used when training set has > 1000 rows; below that the fine-
    tuning overhead doesn't pay off and zero-shot ``tabpfn`` will be
    both faster and competitive.  Warns if n_train < 1000.
    """

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        import sklearn
        import warnings as _warnings
        from sklearn.model_selection import train_test_split

        y = np.asarray(self.obj.y_train).ravel()
        try:
            val_frac = self.obj.parser.getfloat(
                "ML", "tabpfn_ft_val_frac", fallback=0.2
            )
        except Exception:
            val_frac = 0.2

        if len(X_train) < 1000:
            self.obj.logger.warning(
                f"tabpfn_ft: only {len(X_train)} training rows - "
                f"fine-tuning overhead may not pay off below ~1000 rows; "
                f"consider zero-shot 'tabpfn' for small training sets"
            )

        prev = sklearn.get_config()["transform_output"]
        sklearn.set_config(transform_output="default")
        try:
            with _warnings.catch_warnings():
                # We intentionally don't pass output_dir; tabpfn warns about
                # missing checkpointing on every fit. Silence it.
                _warnings.filterwarnings(
                    "ignore",
                    message=r".*output_dir.*",
                    category=UserWarning,
                )
                if len(X_train) < 5:
                    self.obj.logger.warning(
                        f"tabpfn_ft: only {len(X_train)} training rows - "
                        f"too few for a holdout; fitting without validation"
                    )
                    self.obj.model.fit(X_train, y)
                else:
                    X_tr, X_val, y_tr, y_val = train_test_split(
                        X_train, y, test_size=val_frac,
                        random_state=42, shuffle=True,
                    )
                    self.obj.model.fit(X_tr, y_tr, X_val=X_val, y_val=y_val)
        finally:
            sklearn.set_config(transform_output=prev)


class TabICLFTFitter(BaseFitter):
    """FinetunedTabICLRegressor — needs X_val/y_val for early stopping.

    Holds out a fraction of X_train as the validation set passed to
    ``model.fit(X, y, X_val=, y_val=)``. Fraction is configurable via
    ``[ML] tabicl_ft_val_frac`` (default 0.2). On CPU-only nodes this
    will fall back to CPU automatically and take ~5-10x longer per
    task than the zero-shot ``tabicl`` baseline.
    """

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        import sklearn
        from sklearn.model_selection import train_test_split

        y = np.asarray(self.obj.y_train).ravel()
        try:
            val_frac = self.obj.parser.getfloat(
                "ML", "tabicl_ft_val_frac", fallback=0.2
            )
        except Exception:
            val_frac = 0.2
        # Need at least 2 train rows and 1 val row for split.
        if len(X_train) < 5:
            self.obj.logger.warning(
                f"tabicl_ft: only {len(X_train)} training rows — too few "
                f"for a holdout; falling back to fit without validation"
            )
            prev = sklearn.get_config()["transform_output"]
            sklearn.set_config(transform_output="default")
            try:
                self.obj.model.fit(X_train, y)
            finally:
                sklearn.set_config(transform_output=prev)
            return

        X_tr, X_val, y_tr, y_val = train_test_split(
            X_train, y, test_size=val_frac, random_state=42, shuffle=True
        )

        prev = sklearn.get_config()["transform_output"]
        sklearn.set_config(transform_output="default")
        try:
            self.obj.model.fit(X_tr, y_tr, X_val=X_val, y_val=y_val)
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
    """Yggdrasil Decision Forests fitter.

    YDF's learner is configured with ``label=target_col`` at construction
    time (trainers.py), so the training DataFrame must expose a column
    with that exact name.  We assign the label column explicitly rather
    than relying on ``pd.concat([X, y_series])`` — a concat only produces
    the target name when the Series ``.name`` is already set to it, which
    silently breaks if anything upstream resets the Series or converts it
    to an unnamed array.
    """

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        df_train = X_train.copy()
        df_train[self.obj.target_column] = np.asarray(self.obj.y_train).ravel()
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
    """Generalized Additive Model fitter.

    Builds a cubic B-spline ``s(i, n_splines=k)`` for every numeric feature
    and does the single model fit via gridsearch over a shared smoothing-
    parameter range.  pygam's penalized-likelihood optimizer reweights
    effective degrees of freedom per term around the chosen ``lam``.

    **Harvest Year is dropped from the GAM feature set.**  pygam's ``f()``
    factor term cannot extrapolate beyond train-time levels (forecasting
    2026 when train ends in 2023 → domain error), and as ``s()`` it
    extrapolates fragilely while adding no signal the CIDs don't already
    carry.  Published yield-GAM work (Lobell, Sakamoto) treats year
    exclusively via detrending, not as a feature.
    """

    # Columns that should never enter the GAM — either uninformative
    # (Region_ID is an arbitrary integer ID), zero-variance per region
    # (Region is constant in per-region training), or inextrapolable
    # (Harvest Year would cause domain errors at forecast time).
    _DROP_COLS = ("Harvest Year", "Region_ID", "Region")

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        from pygam import LinearGAM, LogisticGAM, s

        # Fit-time layout must match what _preprocess_test_data produces.
        X_fit = X_train.drop(columns=list(self._DROP_COLS), errors="ignore")

        # Adaptive spline count.  Cap low so we don't overfit small regions
        # (a country/crop often has < 100 training rows); splines are cubic
        # (spline_order=3) which is the field-standard choice for yield
        # response curves.
        n_splines = max(4, min(10, len(X_fit) // 20))

        terms = None
        for i, _ in enumerate(X_fit.columns):
            term = s(i, n_splines=n_splines, spline_order=3)
            terms = term if terms is None else terms + term

        gam_cls = LogisticGAM if self.obj.model_type == "CLASSIFICATION" else LinearGAM
        self.obj.model = gam_cls(terms=terms)
        self.obj._gam_fit_cols = list(X_fit.columns)

        y = np.asarray(self.obj.y_train).ravel()
        X_arr = X_fit.values

        # Single fit via gridsearch over shared lam range.  pygam samples
        # each value and returns the model minimizing cross-validated GCV.
        # Per-term lam tuning would be a cross-product over terms — grows
        # exponentially with n_terms and rarely helps more than the shared
        # grid given how penalized GAMs redistribute effective DoF.
        lam_grid = np.logspace(-3, 3, 11)
        self.obj.model.gridsearch(X_arr, y, lam=lam_grid, progress=False)

        self.obj.best_hyperparams = {
            "lam": [float(v) for v in np.asarray(self.obj.model.lam).ravel()],
            "n_splines": n_splines,
            "n_terms": len(X_fit.columns),
        }


class CubistFitter(BaseFitter):
    """Cubist rule-based model fitter.

    Cubist's ``.names`` spec rejects attributes with a single level
    (`"attribute X has only one value Y"`).  In per-region training
    every row has the same ``Region`` / ``Region_ID`` (and sometimes
    ``Country``), so we drop any zero-variance column before fit.
    The same columns are dropped at predict time by aligning on the
    surviving feature set.

    Cubist's internal C wrapper also chokes on NaN — ``y.astype(str)``
    leaves float NaNs as ``nan`` (not ``"nan"``) in some pandas
    versions, and ``_escapes`` then tries ``.replace`` on a float.
    We fill numerics with the train median and objects with a sentinel
    string both at fit and at predict time.
    """

    _SENTINEL = "__missing__"

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        zero_var = [c for c in X_train.columns if X_train[c].nunique(dropna=False) <= 1]
        X_fit = X_train.drop(columns=zero_var) if zero_var else X_train.copy()

        # Train-median for numerics (stored for reuse at predict time),
        # sentinel string for objects.
        num_cols = X_fit.select_dtypes(include=["number"]).columns
        obj_cols = X_fit.select_dtypes(exclude=["number"]).columns
        num_medians = X_fit[num_cols].median()
        if len(num_cols):
            X_fit[num_cols] = X_fit[num_cols].fillna(num_medians)
        if len(obj_cols):
            X_fit[obj_cols] = X_fit[obj_cols].astype("object").fillna(self._SENTINEL)

        self.obj._cubist_fit_cols = list(X_fit.columns)
        self.obj._cubist_num_medians = num_medians
        self.obj.model.fit(X_fit, self.obj.y_train)


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