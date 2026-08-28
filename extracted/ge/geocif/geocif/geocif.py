"""Geocif Dataclass — ML Pipeline Orchestrator.

Central class that reads CID data, engineers features, trains LOOCV
models, and stores predictions to SQLite. Instantiated and driven
by ``geocif_runner.run(cfg)``.
"""

import ast
import os
import re
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
from .ml import correlations, feature_engineering as fe, feature_selection as fs, fs_cache
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
        # Diagnostic: when True, write per-cell (feature, yield) scatter
        # grids alongside the ccc/r2 heatmaps so the data behind each
        # correlation value is inspectable. Default False (gated to avoid
        # producing many extra files per region × model × year).
        self.plot_correlation_scatter = self.parser.getboolean(
            "DEFAULT", "plot_correlation_scatter", fallback=False
        )
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
        self.correlation_metric = self.parser.get("ML", "correlation_metric", fallback="r2")
        self.include_lat_lon_as_feature = self.parser.getboolean("ML", "include_lat_lon_as_feature")
        self.spatial_autocorrelation = self.parser.getboolean("ML", "spatial_autocorrelation")
        self.sa_method = self.parser.get("ML", "sa_method")
        self.last_year_yield_as_feature = self.parser.getboolean("ML", "last_year_yield_as_feature")
        # Tri-state: "all" = full training set, "past" = past years only
        # (Harvest Year < forecast_season), None = disabled.
        _tyf_raw = self.parser.get(
            "ML", "use_yield_trend_as_feature", fallback="False"
        ).strip().lower()
        if _tyf_raw in ("true", "1", "yes", "all"):
            self.use_yield_trend_as_feature = "all"
        elif _tyf_raw in ("past", "causal"):
            self.use_yield_trend_as_feature = "past"
        else:
            self.use_yield_trend_as_feature = None
        # Per-admin Theil-Sen trend on ALL training years (mirrors the
        # [trend_all] baseline model).  Default ON — cheap, leak-safe
        # (df_train excludes the forecast year), and gives the model a
        # strong long-horizon yield-trend signal that complements raw
        # CIDs.  Set False in [ML] to disable.
        self.use_trend_all_as_feature = self.parser.getboolean(
            "ML", "use_trend_all_as_feature", fallback=True
        )
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
        # Within-year neighbor-yield leakage (0.4.774+). Default OFF.
        # When True, _prepare_train_test_split injects forecast-year rows
        # from each test region's k nearest centroid neighbors back into
        # df_train. Hindcast-only — no-ops cleanly when forecast year
        # has no known yields (real-time forecast). See
        # geocif/ml/neighbor_leakage.py for the algorithm.
        self.use_neighbor_leakage = self.parser.getboolean(
            "ML", "use_neighbor_leakage", fallback=False,
        )
        self.n_leaked_neighbors = self.parser.getint(
            "ML", "n_leaked_neighbors", fallback=3,
        )
        self.feature_selection = self.parser.get("ML", "feature_selection")
        # Valid values: none, SHAP, stabl, feature_engine, mrmr, RFECV, lasso,
        #   BorutaPy, Leshy, PowerShap, BorutaShap, Genetic, RFE, multi, gOMP
        self.check_yield_trend = self.parser.getboolean("ML", "check_yield_trend")
        # Diag-STFN-style trend gate (Zhuang et al. 2026, Ecological Informatics
        # doi:10.1016/j.ecoinf.2026.103860). When True, the ``check_yield_trend``
        # flag above is OVERRIDDEN per LOOCV fold by an auto-diagnosis that
        # checks (a) statistical significance of the (year, yield) Pearson
        # correlation on pooled training rows (p <= 0.05) AND (b) that a
        # linear trend fit beats the region-mean baseline on an inner
        # validation year (Imp = 1 - MSE_trend/MSE_naive >= 0). Only if BOTH
        # gates pass does detrending get activated for that (crop, country,
        # forecast_season). Motivated by the rice-vs-maize gap in this
        # session's Brazil metrics: rice trend baseline hit R2=0.939 (trend
        # clearly useful) while maize trend baseline hit R2=0.10 (trend
        # barely helps). Default False keeps prior behavior.
        self.check_yield_trend_diagnostic = self.parser.getboolean(
            "ML", "check_yield_trend_diagnostic", fallback=False,
        )
        # Per-region anomaly target: when set, training fits on
        # (y - region_mean_train_years); predictions add the region mean back
        # at inference time so the DB / plots / FDW stay in absolute yield
        # units. Empirical Lasso probe on Somalia maize showed CV R² jump
        # from ~0.05 → ~0.21 just from this transform — most yield variance
        # is regional baseline, not seasonal anomaly.
        # No-op when check_yield_trend=True (detrending handles baseline
        # removal differently) or when use_yield_trend_as_feature is set.
        self.target_mode = self.parser.get(
            "ML", "target_mode", fallback="absolute"
        ).strip().lower()
        if self.target_mode not in ("absolute", "region_anomaly"):
            self.target_mode = "absolute"
        self.region_anomaly_min_years = self.parser.getint(
            "ML", "region_anomaly_min_years", fallback=5
        )
        # General per-region coverage filter — drops regions with fewer than
        # this many training-year rows from both df_train and df_test in
        # _prepare_train_test_split, regardless of target_mode. 0 = off.
        # Default 5 matches the kebele-coverage threshold below which neither
        # absolute nor region_anomaly mode can learn a reliable per-region
        # signal (only 2-4 LOOCV training rows after holding out the forecast
        # year). Composes with region_anomaly_min_years (effective threshold
        # is the max of the two when target_mode = region_anomaly).
        self.min_years_per_region = self.parser.getint(
            "ML", "min_years_per_region", fallback=5
        )
        # Percent-of-national-production share filter — drops regions whose
        # mean training-year share of national production is below this
        # threshold (units: percent, so 0.5 = 0.5%). 0.0 = off. Applied in
        # _prepare_train_test_split AFTER min_years_per_region so year-sparse
        # regions are dropped first. Production = Area (ha) x Yield (tn/ha),
        # summed within region-year, share computed vs national annual total
        # then averaged across training years for stability. Reason: tiny
        # states like Distrito Federal or Roraima can dominate aggregate
        # rrmsep with high per-region MAPE despite contributing < 1% of the
        # national maize crop; excluding them focuses the model on regions
        # that actually move the national forecast. NOTE: dropping regions
        # mechanically improves the average-of-regional-rrmsep metric even
        # if remaining-region skill is unchanged, so compare fairly.
        self.min_production_share = self.parser.getfloat(
            "ML", "min_production_share", fallback=0.0
        )

        # Per-region [min_year, max_year] filter applied ONLY to df_train seen by
        # ML models (catboost, tabpfn, cubist, etc.). Baseline models (null, trend,
        # trend_all) always see the full self.df_train — they need historical
        # context to compute means/slopes. Useful when a region has a structural
        # regime shift (e.g., UNODC Afghan-poppy Southern/South-Western split in
        # 2019) and you want ML to fit on the recent regime while baselines keep
        # full history. Config format (INI, but Python literal): a dict-string,
        # e.g.  ml_year_range_per_region = {"Southern": [2019, 2100]}
        # Empty / missing → no filter.
        import ast as _ast
        _raw_yr_range = self.parser.get(
            "ML", "ml_year_range_per_region", fallback=""
        ).strip()
        try:
            self.ml_year_range_per_region = (
                _ast.literal_eval(_raw_yr_range) if _raw_yr_range else {}
            )
        except Exception as _e:  # noqa: BLE001
            self.logger.warning(
                f"Failed to parse [ML] ml_year_range_per_region "
                f"({_raw_yr_range!r}): {_e}. Defaulting to empty (no filter)."
            )
            self.ml_year_range_per_region = {}

        # Populated by _prepare_train_test_split when target_mode == region_anomaly.
        self._region_target_means: dict = {}
        # Cache for region_anomaly "skipping ..." warning dedup — only log
        # when the (country, crop, dropped-regions-set) changes.
        self._last_region_anomaly_drop = None
        # Same dedup pattern for the general min_years_per_region filter.
        self._last_min_years_drop = None
        # Per-region z-scored CID sibling features. Empty list = disabled.
        # For each base name, every wide-format column "<base> <stage>" gets
        # a companion "<base>_zreg <stage>" computed leak-safe per LOOCV fold.
        # Closes the encoding gap when target_mode = region_anomaly puts y in
        # anomaly space but X is still raw: the model now sees relative
        # anomalies directly. Motivated by Somalia drought-year audit (May 2026)
        # — see plan file replicated-sniffing-candle.md.
        try:
            import ast as _ast
            _zreg_raw = self.parser.get(
                "ML", "region_zscore_cids", fallback="[]"
            )
            self.region_zscore_cids = _ast.literal_eval(_zreg_raw)
            if not isinstance(self.region_zscore_cids, list):
                self.region_zscore_cids = []
        except (ValueError, SyntaxError):
            self.region_zscore_cids = []
        # z-score-ONLY mode: when True, drop each raw "<base> <stage>" column
        # after adding its "_zreg" sibling. Default False keeps both (raw =
        # cross-region level, _zreg = within-region anomaly; complementary).
        self.region_zscore_replace_raw = self.parser.getboolean(
            "ML", "region_zscore_replace_raw", fallback=False
        )
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
        # Optional per-project Cubist hyperparameter overrides. Absent keys
        # fall back to the trainers.py defaults (n_committees=10,
        # extrapolation=0.10, unbiased=True, auto=True), so crops that don't
        # set them are unaffected. Small-n crops (e.g. poppy, ~56 region-years)
        # do materially better with n_committees=1 + extrapolation=0.0 — the
        # 10-committee/0.10-extrapolation defaults over-boost and over-clip a
        # tiny sample (surrogate LOOCV R^2 0.468 -> 0.611 on MIN_ESI4WK).
        self.cubist_params: dict = {}
        for _opt, _cast in (
            ("cubist_n_committees", self.parser.getint),
            ("cubist_n_rules", self.parser.getint),
            ("cubist_neighbors", self.parser.getint),
            ("cubist_extrapolation", self.parser.getfloat),
            ("cubist_sample", self.parser.getfloat),
            ("cubist_unbiased", self.parser.getboolean),
            ("cubist_auto", self.parser.getboolean),
        ):
            if self.parser.has_option("ML", _opt):
                self.cubist_params[_opt.replace("cubist_", "")] = _cast("ML", _opt)
        # Optional BASS (Bayesian MARS, model='bass') hyperparameters. Absent
        # keys keep the trainers.BassRegressor defaults (max_int=1 additive,
        # npart=15) tuned for poppy. Config keys map bass_<x> -> <x>.
        self.bass_params: dict = {}
        for _opt, _cast in (
            ("bass_max_int", self.parser.getint),
            ("bass_npart", self.parser.getint),
            ("bass_max_basis", self.parser.getint),
            ("bass_nmcmc", self.parser.getint),
            ("bass_nburn", self.parser.getint),
            ("bass_thin", self.parser.getint),
        ):
            if self.parser.has_option("ML", _opt):
                self.bass_params[_opt.replace("bass_", "")] = _cast("ML", _opt)
        # Optional george (GP regression, model='george') overrides. Absent
        # keys keep trainers.GeorgeGPRegressor defaults (isotropic
        # expsquared kernel, jitter=1e-3). Config keys map george_<x> -> <x>;
        # george_kernel ∈ {expsquared, matern32, matern52}.
        self.george_params: dict = {}
        for _opt, _cast in (
            ("george_kernel", self.parser.get),
            ("george_jitter", self.parser.getfloat),
        ):
            if self.parser.has_option("ML", _opt):
                self.george_params[_opt.replace("george_", "")] = _cast("ML", _opt)
        # Optional PyGRF (Geographical RF, model='pygrf') overrides. Absent
        # keys keep trainers.PyGRFRegressor defaults (band_width heuristic,
        # local_weight = Moran's I of y). Config keys map pygrf_<x> -> <x>.
        # band_width is a float: a neighbor COUNT for kernel=adaptive but a
        # RADIUS in km for kernel=fixed. max_features follows sklearn RF
        # semantics: 'sqrt'/'log2'/None, int = count, float = fraction.
        def _cast_max_features(section, opt):
            raw = self.parser.get(section, opt).strip()
            if raw.lower() in ("sqrt", "log2"):
                return raw.lower()
            if raw.lower() in ("none", ""):
                return None
            try:
                return int(raw)
            except ValueError:
                return float(raw)

        self.pygrf_params: dict = {}
        for _opt, _cast in (
            ("pygrf_band_width", self.parser.getfloat),
            ("pygrf_local_weight", self.parser.getfloat),
            ("pygrf_n_estimators", self.parser.getint),
            ("pygrf_max_features", _cast_max_features),
            ("pygrf_kernel", self.parser.get),
            ("pygrf_resampled", self.parser.getboolean),
        ):
            if self.parser.has_option("ML", _opt):
                self.pygrf_params[_opt.replace("pygrf_", "")] = _cast("ML", _opt)
        # Optional TabPFN-GSA (model='tabpfn_gsa') overrides: K = grid cells
        # (perfect square), s = distant-sampling rate in [0,1]. Keys map
        # tabpfn_gsa_<x> -> <x>.
        self.gsa_params: dict = {}
        for _opt, _cast in (
            ("tabpfn_gsa_K", self.parser.getint),
            ("tabpfn_gsa_s", self.parser.getfloat),
        ):
            if self.parser.has_option("ML", _opt):
                self.gsa_params[_opt.replace("tabpfn_gsa_", "")] = _cast("ML", _opt)

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
            **di.dict_etref,
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
        # Per-model flag: when True, the curated_<algo> wrappers restrict
        # the feature frame to single-calendar-period (monthly) features
        # only — dropping cumulative spans + Pre-Season / In-Season
        # aggregates. Off by default for backward compatibility.
        self.monthly_only_features = self.parser.getboolean(
            self.model_name, "monthly_only_features", fallback=False,
        )
        # Trailing-window width. Taken from the last<N>m_ prefix when present,
        # overridable by an explicit key so a plain [catboost] section can use
        # the window without being renamed. -1 = off; any value < 1 disables,
        # so 0 can never be misread as "keep zero months".
        _last_m = re.match(r"^last(\d+)m_(.+)$", self.model_name)
        self.last_n_months = self._get_model_int(
            "last_n_months", int(_last_m.group(1)) if _last_m else -1
        )
        # Middle ground: single months + the one full-season window, dropping
        # intermediate cumulative spans. Restores season-integrated signal that
        # monthly_only strips, while avoiding the full cumulative set's dilution.
        self.monthly_plus_fullseason_features = self.parser.getboolean(
            self.model_name, "monthly_plus_fullseason_features", fallback=False,
        )
        # Per-model flag: include Region as a penalized factor term (pygam
        # f()) in the GAM — per-region intercepts inside one pooled model
        # (the "factor GAM"). Only meaningful under pooled cluster
        # strategies where Region varies within a training frame; in
        # per-region training Region is single-level and the factor is
        # skipped. Off by default: the plain GAM stays region-blind.
        self.gam_region_factor = self.parser.getboolean(
            self.model_name, "gam_region_factor", fallback=False,
        )
        # curated_<algo> wrappers train on a hand-picked CID list — the
        # whole point is to bypass gOMP / Boruta selection and use every
        # surviving column. Force feature_selection = none for them,
        # overriding the global [ML] feature_selection setting.
        # top<N>_<algo> wrappers: same idea but the CID list is sourced
        # at runtime from the deduplicated pearson_summary.csv emitted
        # by a broad-feature model run (must execute earlier in the
        # `models` list). N = the number after "top". Falls back to
        # whatever use_cids says when the summary file is missing.
        # auto_<algo> wrappers: like top<N>_, but the CID set is sized
        # by the at-least-X-above-Y schema in utils.auto_select_cids
        # (dedup-first relaxation). Per-model knobs override defaults.
        _top_match = re.match(r"^top(\d+)_(.+)$", self.model_name)
        _auto_match = self.model_name.startswith("auto_")
        # last<N>m_<algo> wrappers (e.g. last2m_catboost): restrict the feature
        # frame to the TRAILING N calendar periods of the season, then dispatch
        # to <algo>. N lives in the section name so last2m_catboost, plain
        # catboost and null can share one `models` list -- same folds, same
        # data prep, same baseline, hence a controlled comparison.
        # Deliberately does NOT force feature_selection = "none" (unlike
        # top<N>_ / curated_): this is a feature-SPACE restriction, and the
        # selector should still run over what survives.
        _last_match = re.match(r"^last(\d+)m_(.+)$", self.model_name)
        self.top_n_pearson: int | None = None
        self.auto_select_cids_flag = False
        if self.model_name.startswith("curated_"):
            self.feature_selection = "none"
        if _top_match:
            self.top_n_pearson = int(_top_match.group(1))
            self.feature_selection = "none"
        if _auto_match:
            self.auto_select_cids_flag = True
            self.feature_selection = "none"
            self.auto_min_count = self._get_model_int("auto_min_count", 8)
            self.auto_min_abs_r = self._get_model_float("auto_min_abs_r", 0.30)
            self.auto_dedup_threshold = self._get_model_float("auto_dedup_threshold", 0.90)
            self.auto_dedup_max = self._get_model_float("auto_dedup_max", 0.99)
            self.auto_abs_r_floor = self._get_model_float("auto_abs_r_floor", 0.10)
            self.auto_abs_r_step = self._get_model_float("auto_abs_r_step", 0.05)
        # dispatch_name = the underlying algorithm to dispatch to (e.g.
        # "gam" for "curated_gam", "tabpfn" for "top10_tabpfn" /
        # "auto_tabpfn"). EVERY model_name == "..." check that matters
        # for algorithm-specific code paths (fitter factory, GAM column
        # alignment, NaN fill, etc) should use self.dispatch_name
        # instead of self.model_name. self.model_name stays as the
        # original section name so DB rows / plots stay disambiguated.
        if self.model_name.startswith("curated_"):
            self.dispatch_name = self.model_name.split("_", 1)[1]
        elif _top_match:
            self.dispatch_name = _top_match.group(2)
        elif _auto_match:
            self.dispatch_name = self.model_name.split("_", 1)[1]
        elif _last_match:
            self.dispatch_name = _last_match.group(2)
        else:
            self.dispatch_name = self.model_name
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
        # pygrf / tabpfn_gsa consume region centroids from the lat/lon
        # feature columns. Without the flag, every region's fit raises
        # inside loop_ml's per-region catch and the run "succeeds" with
        # zero stored predictions — fail here instead, at setup time.
        # dispatch_name (not model_name) so curated_/top<N>_/auto_
        # wrappers of these algos are covered too.
        if (
            self.dispatch_name in ("pygrf", "tabpfn_gsa")
            and not self.include_lat_lon_as_feature
        ):
            raise ValueError(
                f"model = '{self.model_name}' (dispatch '{self.dispatch_name}') "
                "requires [ML] include_lat_lon_as_feature = True — region "
                "centroid lat/lon are its spatial coordinates. Set it in the "
                "config before running."
            )

    def _refresh_target_column(self):
        """Refresh ``self.target_column`` after ``self.check_yield_trend`` was
        toggled. The initial ``target_column`` is set in ``__init__`` before
        model-type-specific ``_setup_*_flags`` methods override the trend
        flag, so per-model toggles need to call this to keep the two in
        sync. Regression only; classification uses ``self.target_class``.
        """
        if getattr(self, "model_type", None) == "REGRESSION":
            self.target_column = (
                f"Detrended {self.target}" if self.check_yield_trend else self.target
            )

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
        self._refresh_target_column()

        if self.model_name == "ngboost":
            self.cat_features = [col for col in self.cat_features if col not in ("Region", "State")]

    def _setup_regression_flags(self):
        """Setup flags for regression models. Uses dispatch_name so the
        curated_<algo> wrappers pick the same flag set as their underlying
        algo (e.g. curated_gam → 'gam' → _setup_simple_regression_flags)."""
        # NB: cubist was previously in this simple-regression group, which
        # hard-disables estimate_ci — so cubist forecasts never got conformal
        # CIs despite estimate_ci=True in config. Cubist is a full ML model
        # (fits on features, supports crepes/mapie conformal wrapping), so it
        # routes to _setup_standard_ml_flags and honours the config CI flags.
        if not self.ml_model or self.dispatch_name in ["linear", "gam", "merf", "gpr", "george"]:
            self._setup_simple_regression_flags()
        elif self.model_name.startswith("cumulative_"):
            self._setup_cumulative_flags()
        elif self.dispatch_name in ["tabpfn", "tabpfn_ft", "desreg", "tabicl", "tabicl_ft", "tabfm", "exaone", "tabpfn_gsa"]:
            self._setup_tabular_flags()
        elif self.dispatch_name in ["oblique", "ydf", "pygrf"]:
            self._setup_tree_flags()
        elif self.dispatch_name == "ngboost":
            self._setup_ngboost_flags()
        else:
            self._setup_standard_ml_flags()

    def _setup_simple_regression_flags(self):
        """Flags for simple regression models."""
        self.do_xai = False
        self.estimate_ci = False
        # Every baseline fits on ABSOLUTE yield.
        #
        # `null` briefly detrended (0.4.942) so it would sit on the same target
        # as the ML models. Reverted in 0.4.944: detrended residuals are
        # zero-mean by construction, so "average the residuals, then retrend"
        # collapses to "return the trend value at the forecast year" — i.e. it
        # duplicates `trend` and destroys the climatological-mean bar. Keeping
        # them distinct is what lets you say "beats the county mean but not the
        # trend". It also never addressed the concern that motivated it: the
        # detrending is fit on the same LOOCV training set, future years
        # included. Metrics are computed in absolute space for every model
        # anyway (ML predictions are retrended in predict()), so the comparison
        # is already like-for-like.
        self.check_yield_trend = False
        self.estimate_ci_for_all = False
        # Baseline (non-ML) models and simple regressors always fit on
        # absolute yield -- refresh target_column so it tracks the flag
        # toggle above. Without this, target_column stays at "Detrended
        # Yield (tn per ha)" (set in __init__ before this flag override
        # runs) and _setup_training_data's dropna(subset=[target_column])
        # raises KeyError because _get_common_columns excludes the
        # Detrended column when check_yield_trend is False. That was
        # the "No predictions found for brazil maize null/trend" bug --
        # every baseline region crashed and got skipped, but the outer
        # loop still reported "N/110 done" from the model iteration.
        self._refresh_target_column()

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
        self._refresh_target_column()
        self.cluster_strategy = "single"
        self.use_spatial_neighbors = False
        self.select_cid_by = "Index"
        self.use_cumulative_features = True

    def _setup_tabular_flags(self):
        """Flags for tabular models."""
        self.do_xai = self.parser.getboolean("ML", "do_xai", fallback=False)
        # XAI is unsupported for tabpfn_gsa: xai.explain has no explainer
        # path for it — TreeExplainer rejects the non-tree wrapper, and the
        # permutation path would refit local TabPFN ensembles per grid cell
        # per permutation (prohibitively slow) while dropping the Region
        # column GSAModel requires at predict.
        if self.do_xai and self.dispatch_name == "tabpfn_gsa":
            self.logger.warning(
                f"[ML] do_xai = True is not supported for {self.model_name}; "
                f"disabling XAI for this model (no SHAP explainer path for GSAModel)"
            )
            self.do_xai = False
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
        self.cat_features = [col for col in self.cat_features if col not in ("Region", "State")]

    def _setup_standard_ml_flags(self):
        """Flags for standard ML models with full features."""
        self.do_xai = self.parser.getboolean("ML", "do_xai")
        self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
        self.estimate_ci_for_all = self.parser.getboolean("ML", "estimate_ci_for_all")
        self.alpha = self.parser.getfloat("ML", "alpha")
        self.ci_method = self.parser.get("ML", "ci_method", fallback="crepes")
        self.check_yield_trend = self.parser.getboolean("ML", "check_yield_trend")
        self._refresh_target_column()

    def _setup_seasons_and_stages(self):
        """Setup seasons and simulation stages."""
        self.all_seasons_with_yield = self.df_inputs[
            self.df_inputs[self.target].notna()
        ]["Harvest Year"].unique()

        if self.is_pre_season:
            self.all_stages = ["PS"]
            self.simulation_stages = [np.array([0])]
            return

        # _setup_reverse_stages is data-driven (it reads the Stage_ID values
        # already present in df_inputs), so despite the name it also serves the
        # season-normalized methods whose Stage_IDs encode a single full-season
        # window: fraction_season (deciles "10_20_..._100") and
        # phenological_stages / full_season ("1_2_3"). _filter_current_month_stages
        # is a no-op for these (their tokens are not calendar-month numbers).
        if (
            self.method.endswith("_r")
            or self.method in ("fraction_season", "phenological_stages", "full_season")
        ):
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

        # Read ONLY the seasons declared for this country/crop (config wins;
        # else calendar-detected). A bare ``_s*`` glob would also pull in
        # stray index files for seasons the country doesn't actually grow —
        # e.g. Nigeria (seasons=[1]) had leftover ``nigeria_maize_s2_*`` files
        # that injected a spurious, yield-less Season 2 into every output.
        from geocif.indices_runner import get_seasons
        seasons = get_seasons(country, self.parser, crop=crop)
        all_files = []
        for s in seasons:
            all_files.extend(sorted(_dir_country.glob(f"{country}_{crop}_s{s}_*.csv")))

        if not all_files:
            raise FileNotFoundError(
                f"No files found in {_dir_country} for seasons {seasons} "
                f"(pattern {country}_{crop}_s{{season}}_*.csv)"
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

    def _merge_season_features_if_missing(
        self, df: pd.DataFrame, country: str, crop: str
    ) -> pd.DataFrame:
        """Attach region-static phenology features to a wide ML dataframe.

        Reads ``season_length_dekads`` + ``season_start_month`` per region
        from the raw geoprepare crop_t0 CSV
        (``{dir_output}/crop_t{floor}/{country}/{country}_{crop}_s{N}.csv``)
        and joins them onto the wide ML dataframe by Region (case- and
        underscore-normalized).

        Called from ``_execute_single_pass`` / ``_execute_multi_step``
        AFTER the pivot in ``_prepare_ml_dataframe``. An earlier attempt
        in ``read_data`` operating on the long-format ``self.df_inputs``
        (0.4.793/0.4.794) was silently dropped by the pivot, since the
        CID pivot only preserves indicator × stage columns.

        No-op paths:
        1. Columns already present on ``df`` — indices_runner in a
           future release may preserve these during CID aggregation, at
           which point this method becomes a passthrough.
        2. Source CSV missing (crop_t0 not populated) — logs a warning,
           does not fail. Downstream ML runs without the two features.
        3. Source CSV lacks the columns (pre-geoprepare-0.6.282) — same
           behavior as (2). Fix: re-run geomerge to regenerate.

        The features are region-STATIC (do not vary year-to-year), so a
        deduplicated per-region lookup is joined onto every row of the
        wide dataframe. Groups A/B in Kenya emit ``(20, 4)`` vs
        ``(12, 3)`` — a continuous encoding of phenology group identity
        that TabPFN / CatBoost / etc. can split on without seeing the
        raw region name.
        """
        if "season_length_dekads" in df.columns:
            return df

        try:
            from geocif.indices_runner import get_input_file_path, get_seasons
            input_dir = get_input_file_path(
                country, self.parser, data_source="harvest"
            )
            growing_seasons = get_seasons(country, self.parser, crop=crop)
        except Exception as e:
            self.logger.warning(
                f"season-feature merge: could not resolve crop_t0 dir/seasons "
                f"for {country}: {e}. Skipping."
            )
            return df

        country_lower = country.lower().replace(" ", "_")
        crop_lower = crop.lower().replace(" ", "_")

        # Try each configured growing-season CSV; the features can differ
        # between seasons (e.g. long-rains vs short-rains phenology) but
        # for single-season configs (like Kenya current) there's just one.
        src = None
        for gs in growing_seasons:
            candidate = input_dir / f"{country_lower}_{crop_lower}_s{gs}.csv"
            if candidate.exists():
                src = candidate
                break

        if src is None:
            self.logger.warning(
                f"season-feature merge: no crop_t0 CSV found for {country} "
                f"{crop} at growing_seasons={growing_seasons} in {input_dir}; "
                f"skipping."
            )
            return df

        try:
            df_src = pd.read_csv(
                src,
                engine="pyarrow",
                usecols=["region", "season_length_dekads", "season_start_month"],
            )
        except (ValueError, KeyError) as e:
            # Pre-0.6.282 crop_t0 CSV — the two columns don't exist yet.
            self.logger.warning(
                f"season-feature merge: {src.name} lacks the new columns "
                f"({e}); re-run geomerge to populate. Skipping."
            )
            return df

        # Dedup per region — features are region-static.
        df_src = (
            df_src.dropna(subset=["season_length_dekads"])
                  .drop_duplicates(subset=["region"])
        )
        if df_src.empty:
            self.logger.warning(
                f"season-feature merge: no non-NaN season rows in {src.name}; "
                f"skipping."
            )
            return df

        def _norm(s):
            return str(s).lower().replace(" ", "_").replace("-", "_")

        df_src["_join_key"] = df_src["region"].map(_norm)
        df["_join_key"] = df["Region"].map(_norm)

        before = len(df)
        df = df.merge(
            df_src[["_join_key", "season_length_dekads", "season_start_month"]],
            on="_join_key",
            how="left",
        )
        df = df.drop(columns=["_join_key"])

        n_matched = int(df["season_length_dekads"].notna().sum())
        n_unmatched_regions = int(
            df.loc[
                df["season_length_dekads"].isna(), "Region"
            ].nunique()
        )
        self.logger.info(
            f"season-feature merge: attached to {n_matched}/{before} rows "
            f"for {country} {crop} "
            f"({df_src['region'].nunique()} source regions; "
            f"{n_unmatched_regions} unmatched region name(s))"
        )
        return df

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

        # Attach region-static phenology features onto the wide df AFTER
        # the CID pivot (long → wide) in _prepare_ml_dataframe. Doing
        # this in read_data operates on the long-format df_inputs and
        # gets silently dropped by the pivot. No-op if already present
        # or if the source crop_t0 CSV can't be read.
        df = self._merge_season_features_if_missing(df, self.country, self.crop)

        self._run_spatial_autocorrelation_if_enabled()
        self._run_cluster_analysis(df)

        dict_selected_features, dict_best_cid = self._generate_correlation_plots(df)

        self._prepare_train_test_split(df)
        self._compute_detrended_yield()
        self._compute_yield_trend_feature()
        self._compute_trend_all_feature()
        self._compute_region_zscore_features()
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

    def _get_season_months(self) -> list:
        """Return chronological season months from the longest in-season Stage_ID.

        For ``_r`` methods Stage_ID arrays are harvest→planting, so reverse
        to get planting→harvest. Returns ``[]`` if no in-season stages exist.
        Used by ``_execute_pre_season`` to enumerate valid forecast targets
        when iterating in-season init months.
        """
        stage_ids = [
            s for s in self.df_inputs["Stage_ID"].dropna().unique()
            if not s.startswith(("PS", "IS"))
        ]
        if not stage_ids:
            return []
        longest = max(stage_ids, key=lambda s: len(s.split("_")))
        months = [int(x) for x in longest.split("_")]
        if self.method.endswith("_r"):
            months = list(reversed(months))
        return months


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
                # Pre/In-season labels are already calendar-order human
                # readable ("Pre-Season (init Feb)") — display == raw.
                "Stage Window Display": stage_name,
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

            if is_before_planting:
                # Pre-season init: data tagged with PS_<init>
                df = self.df_inputs[
                    (self.df_inputs["Type"].isin(forecast_types)) &
                    (self.df_inputs["Stage"] == stage_pattern)
                ]
                debug_filter_kind = "ps_init"
            else:
                # In-season init: data is tagged by numeric target-month
                # Stage_ID, not PS_<init>. For init M and target T, the
                # freshest forecast is the row whose LEAD == (T - M) mod 12;
                # all other LEAD values for that target are stale older-init
                # forecasts. Valid targets are season months reachable from
                # M within max_lead = 6 (matches FLDAS LEAD0..5 / S2S LEAD1..6).
                max_lead = 6
                season_months = self._get_season_months()
                sid = pd.to_numeric(self.df_inputs["Stage_ID"], errors="coerce")
                lead = (
                    self.df_inputs["Index"].astype(str)
                    .str.extract(r"_LEAD(\d+)", expand=False)
                    .astype("Int64")
                )
                matches = pd.Series(False, index=self.df_inputs.index)
                target_log = []
                for tgt in season_months:
                    exp_lead = (tgt - init_month) % 12
                    if exp_lead >= max_lead:
                        continue  # outside lead horizon
                    sub = (sid == tgt) & (lead == exp_lead)
                    if sub.any():
                        target_log.append((int(tgt), int(exp_lead), int(sub.sum())))
                        matches = matches | sub
                df = self.df_inputs[
                    self.df_inputs["Type"].isin(forecast_types) & matches
                ]
                debug_filter_kind = "is_init_fresh"
                if not df.empty:
                    self.logger.info(
                        f"  In-season init {month_name}: admitted "
                        f"{len(target_log)} (target, lead) pairs: "
                        + ", ".join(
                            f"tgt={t}/LEAD{l}({n})" for t, l, n in target_log
                        )
                    )

            debug_row = {
                "step": init_month,
                "month_name": month_name,
                "filter_kind": debug_filter_kind,
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
            self._compute_trend_all_feature()
            self._compute_region_zscore_features()
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

        # Per-SEASON chronology (planting→harvest), reused here to know the
        # "publish date" (latest covered month) and remaining-season months at
        # each step. Feeds _filter_by_simulation_stages so it can admit
        # forward-looking FLDAS/S2S leads from the freshest init only. Grouped
        # by season so a two-season country uses the right season's window per
        # step (single-season => one group, unchanged).
        group_info = []
        if all_simulation_stages:
            for g in self._group_stages_by_season(all_simulation_stages):
                gmonths = {int(x) for s in g for x in s}
                glongest = max(g, key=lambda s: len(s))
                gchrono = list(reversed([int(x) for x in glongest]))
                group_info.append((gmonths, gchrono))

        df_inputs_orig = self.df_inputs.copy()
        cached_latlon = None

        for step_idx, stage_subset in enumerate(step_subsets):
            self.simulation_stages = stage_subset
            self.df_inputs = df_inputs_orig.copy()
            self._current_step_label = f"[{step_idx + 1}/{len(step_subsets)}]"

            # Per-step publish date + remaining season — read by
            # _filter_by_simulation_stages when use_cids contains forecast
            # types. Pick this subset's season group (max month overlap).
            covered = {int(x) for s in stage_subset for x in s}
            chronological = []
            if covered and group_info:
                _, chronological = max(
                    group_info, key=lambda gi: len(gi[0] & covered)
                )
            if chronological:
                chronological_covered = [m for m in chronological if m in covered]
                self._latest_covered_month = (
                    chronological_covered[-1] if chronological_covered else None
                )
                self._remaining_season_months = [
                    m for m in chronological if m not in covered
                ]
            else:
                self._latest_covered_month = None
                self._remaining_season_months = []

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

            # Attach region-static phenology features onto the wide df.
            # No-op if already present or if the source crop_t0 CSV can't
            # be read. See _merge_season_features_if_missing docstring.
            df = self._merge_season_features_if_missing(df, self.country, self.crop)

            if step_idx == 0:
                self._run_spatial_autocorrelation_if_enabled()
                self._run_cluster_analysis(df)

            dict_selected_features, dict_best_cid = self._generate_correlation_plots(df)

            self._prepare_train_test_split(df)
            self._compute_detrended_yield()
            self._compute_yield_trend_feature()
            self._compute_trend_all_feature()
            self._compute_region_zscore_features()
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

    def _filter_by_min_production_share(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop regions whose 5-year mean share of country production is below
        ``min_production_share_pct`` (config knob, percent). Per-country
        override wins over ``[DEFAULT]``; missing or ``<=0`` disables the
        filter. Share is computed by ``diagnostics.compute_production_pct``
        (mean of area*yield over the last 5 available years, normalized to
        the country total).
        """
        threshold = 0.0
        for section in (self.country, "DEFAULT"):
            if section and self.parser.has_option(section, "min_production_share_pct"):
                try:
                    threshold = self.parser.getfloat(section, "min_production_share_pct")
                    break
                except (ValueError, TypeError):
                    threshold = 0.0
        if threshold <= 0.0:
            return df

        # df["Country"] is Title Case (e.g. "Kenya") but self.country is the
        # config-section key ("kenya"). Match by normalized comparison.
        if "Country" not in df.columns:
            return df
        country_val = next(
            (c for c in df["Country"].unique()
             if str(c).lower().replace(" ", "_") == self.country),
            None,
        )
        if country_val is None:
            return df

        from .viz import diagnostics as diag
        # self.target is the post-rename yield column (config: new_name_target,
        # typically 'Yield'). compute_production_pct defaults to a different
        # obs_col name ('Observed Yield (tn per ha)') that doesn't exist here,
        # so pass self.target explicitly.
        prod_pct = diag.compute_production_pct(df, country_val, obs_col=self.target)
        if not prod_pct:
            self.logger.warning(
                f"min_production_share_pct={threshold}: production_pct empty "
                f"(check Area (ha)/{self.target} availability) — filter skipped "
                f"for {self.country}/{self.crop}"
            )
            return df

        kept = {r for r, p in prod_pct.items() if p >= threshold}
        dropped = {r: p for r, p in prod_pct.items() if p < threshold}
        if dropped:
            dropped_str = ", ".join(
                f"{r}={p:.3f}%"
                for r, p in sorted(dropped.items(), key=lambda kv: kv[1])
            )
            self.logger.warning(
                f"min_production_share_pct={threshold}: dropped "
                f"{len(dropped)} regions below threshold "
                f"({self.country}/{self.crop}): {dropped_str}"
            )
        return df[df["Region"].isin(kept)].copy()

    def _config_option(self, option: str, fallback: str = "") -> str:
        """Read a config option from the per-country section, then [DEFAULT].

        Same lookup order as ``_filter_by_min_production_share``. Returns
        ``fallback`` when neither section defines it (or the value is blank).
        """
        for section in (getattr(self, "country", None), "DEFAULT"):
            if section and self.parser.has_option(section, option):
                value = self.parser.get(section, option)
                if value is not None and str(value).strip():
                    return str(value).strip()
        return fallback

    @staticmethod
    def _normalize_admin_level(level: str) -> str:
        """Canonicalize an admin-level string: 'Admin1'/'admin 1' -> 'admin_1'."""
        norm = str(level).strip().lower().replace(" ", "_").replace("-", "_")
        match = re.fullmatch(r"admin_?(\d)", norm)
        return f"admin_{match.group(1)}" if match else norm

    def _get_run_region_selection(self) -> Optional[list]:
        """Region names the user asked to restrict this run to, or None.

        Config (per-country section, falling back to [DEFAULT])::

            run_regions = ["illinois", "iowa"]                 ; all crops
            run_regions = {"maize": ["illinois"], "soybean": [...]}

        Parsed with ``ast.literal_eval``. Returns None — meaning "no
        filtering", today's default behaviour — when the option is unset,
        unparseable, not a list/dict, or a dict that has no entry for the
        crop currently being run. A malformed value never raises: it is
        logged and treated as unset.
        """
        return stats.parse_run_regions(
            self._config_option("run_regions"),
            crop=getattr(self, "crop", None),
            log=self.logger,
        )

    def _filter_to_selected_regions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Restrict the ML frame to the user-selected regions (``run_regions``).

        The selection may be given at a DIFFERENT admin level than the run
        itself, declared by ``run_regions_level`` (default: the run's own
        ``admin_level``):

        * selection level == run level — direct name match.
        * admin_1 selection, admin_2 run — each county Region is mapped to
          its parent state via ``ml.stats.admin1_lookup`` and kept when that
          state was selected. This is the headline case: "run every county in
          Illinois and Iowa".
        * admin_2 selection, admin_1 run — the selected county names are
          mapped UP to their parent states and those states are kept.
        * anything else — logged as a warning and left untouched.

        Name matching reuses ``ml.stats._norm_region_*`` (the yield-join
        normalization), so "South Dakota", "south_dakota" and "SOUTH DAKOTA"
        are the same name. Selected names that match nothing are listed in a
        warning (typo protection). A selection that matches NO rows raises
        ValueError — a silently empty run is worse than a loud failure.
        """
        selection = self._get_run_region_selection()
        if not selection or df.empty or "Region" not in df.columns:
            return df

        from geocif.ml import stats as ml_stats

        run_level = self._normalize_admin_level(getattr(self, "admin_zone", "") or "")
        sel_level = self._normalize_admin_level(
            self._config_option("run_regions_level", fallback=run_level)
        )

        region_norm = ml_stats._norm_region_series(df["Region"])
        wanted = {ml_stats._norm_region_name(name) for name in selection}
        n_regions_before = region_norm.nunique()

        def _lookup():
            dir_stats = Path(self.parser.get("PATHS", "dir_production_statistics"))
            country_str = str(self.country).title().replace("_", " ")
            return ml_stats.admin1_lookup(dir_stats, country_str, parser=self.parser)

        if sel_level == run_level:
            keys = region_norm
            unmatched = [
                name for name in selection
                if ml_stats._norm_region_name(name) not in set(keys)
            ]
        elif sel_level == "admin_1" and run_level == "admin_2":
            mapping = _lookup()
            if not mapping:
                self.logger.error(
                    f"run_regions given at admin_1 for an admin_2 run but no "
                    f"admin_2->admin_1 mapping is available for {self.country} "
                    f"(check production_statistics_file) — running all regions."
                )
                return df
            parent_norm = {
                k: ml_stats._norm_region_name(v) for k, v in mapping.items()
            }
            keys = region_norm.map(parent_norm)
            present = set(keys.dropna())
            unmatched = [
                name for name in selection
                if ml_stats._norm_region_name(name) not in present
            ]
        elif sel_level == "admin_2" and run_level == "admin_1":
            mapping = _lookup()
            if not mapping:
                self.logger.error(
                    f"run_regions given at admin_2 for an admin_1 run but no "
                    f"admin_2->admin_1 mapping is available for {self.country} "
                    f"(check production_statistics_file) — running all regions."
                )
                return df
            parent_of = {}
            for name in selection:
                norm_name = ml_stats._norm_region_name(name)
                if norm_name in mapping:
                    parent_of[name] = ml_stats._norm_region_name(mapping[norm_name])
            wanted = set(parent_of.values())
            keys = region_norm
            present = set(keys)
            unmatched = [
                name for name in selection
                if parent_of.get(name) is None or parent_of[name] not in present
            ]
            self.logger.info(
                f"run_regions given at admin_2 for an admin_1 run — mapped "
                f"{len(parent_of)} selected region(s) up to "
                f"{len(wanted)} parent admin_1 region(s): "
                f"{', '.join(sorted(wanted))}"
            )
        else:
            self.logger.warning(
                f"run_regions_level='{sel_level}' cannot be reconciled with "
                f"admin_level='{run_level}' for {self.country}/{self.crop} — "
                f"ignoring run_regions, running all regions."
            )
            return df

        if unmatched:
            self.logger.warning(
                f"run_regions: {len(unmatched)} selected name(s) matched no "
                f"region in {self.country}/{self.crop} (check spelling): "
                f"{', '.join(unmatched)}"
            )

        mask = keys.isin(wanted).fillna(False).astype(bool)
        if not mask.any():
            examples = sorted({str(r) for r in df["Region"].unique()})[:5]
            raise ValueError(
                f"run_regions selected 0 regions for {self.country}/{self.crop}: "
                f"none of the {len(selection)} name(s) given at "
                f"'{sel_level}' (e.g. {', '.join(selection[:5])}) match any "
                f"Region in the '{run_level}' frame "
                f"(e.g. {', '.join(examples)}). Fix run_regions / "
                f"run_regions_level, or unset run_regions to run all regions."
            )

        out = df[mask].copy()
        n_kept = ml_stats._norm_region_series(out["Region"]).nunique()
        self.logger.info(
            f"run_regions filter ({self.country}/{self.crop}, selection at "
            f"'{sel_level}', run at '{run_level}'): kept {n_kept} of "
            f"{n_regions_before} regions ({len(out)} of {len(df)} rows), "
            f"dropped {n_regions_before - n_kept}"
        )
        return out

    def _add_state_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Populate the 'State' categorical (parent admin_1) for admin_2 runs.

        Opt-in purely via [ML] cat_features containing "State" — no separate
        flag, nothing country-specific. The county->state mapping comes from
        the production-statistics file (admin_2 -> admin_1) via
        ml.stats.admin1_lookup, which shares file resolution and name
        normalization with the yield join, so the two can never disagree.
        Unmapped regions get the explicit level "unknown" rather than NaN.
        """
        if "State" not in self.cat_features or "State" in df.columns or df.empty:
            return df
        from geocif.ml import stats as ml_stats

        dir_stats = Path(self.parser.get("PATHS", "dir_production_statistics"))
        country_str = self.country.title().replace("_", " ")
        mapping = ml_stats.admin1_lookup(dir_stats, country_str, parser=self.parser)
        if not mapping:
            self.logger.warning(
                "'State' in cat_features but no admin_2->admin_1 mapping "
                f"available for {country_str}; filling 'unknown'"
            )
        df["State"] = (
            ml_stats._norm_region_series(df["Region"]).map(mapping).fillna("unknown")
        )
        n_states = df["State"].nunique()
        self.logger.info(
            f"State categorical added: {n_states} states across "
            f"{df['Region'].nunique()} regions"
        )
        return df

    def _prepare_ml_dataframe(self) -> pd.DataFrame:
        """Convert raw data into ML-ready format."""
        df = self._filter_by_simulation_stages()
        if self.top_n_pearson:
            self._apply_top_n_pearson_filter(df)     # mutates self.use_cids
        elif self.auto_select_cids_flag:
            self._apply_auto_pearson_filter(df)      # mutates self.use_cids
        df = self._filter_by_cid_categories(df)
        df = self._prune_stale_forecast_rows(df)
        df = self.create_ml_dataframe(df)

        if self.parser.getboolean("DEFAULT", "filter_low_production_regions", fallback=False):
            df = self._filter_low_production_regions(df)

        # Absolute production-share filter (percent). Reads
        # [<country>] min_production_share_pct then [DEFAULT]. Ignored if
        # <=0 or unset. Complements the fixed-5%-quantile filter above.
        df = self._filter_by_min_production_share(df)

        # Explicit user region selection ([<country>] run_regions, optionally
        # given at a coarser/finer level via run_regions_level). Applied AFTER
        # the production filters so their country-wide statistics keep their
        # meaning, and before _save_ml_dataframe so training, LOOCV, the DB,
        # plots and parent aggregations all see only the selected regions.
        df = self._filter_to_selected_regions(df)

        df = self._add_state_column(df)

        self._save_ml_dataframe(df)
        df[self.cat_features] = df[self.cat_features].astype("category")

        # EDA scatters: one PNG per CID, x = full-season cumulative column,
        # y = observed yield, colour by Harvest Year. Idempotent across
        # model runs — populated by whichever (country, crop) model runs
        # first (typically the one with use_cids=['all'] giving the widest
        # CID coverage). Skipped when the per-(country, crop) output dir
        # already contains PNGs.
        try:
            self._plot_cid_vs_yield_scatters(df)
        except Exception as exc:  # noqa: BLE001 — diagnostic plot, never block training
            self.logger.warning(f"cid_vs_yield_scatters failed: {exc}")

        return df

    def _plot_cid_vs_yield_scatters(self, df: pd.DataFrame) -> None:
        """One-time CID-vs-yield EDA scatter set per (country, crop).

        Gated to fire only from models that train on the *broad* feature
        set — i.e. use_cids == ['all'], monthly_only_features = False,
        use_single_time_period_as_feature = False. Curated wrappers
        (curated_tabpfn / curated_catboost / curated_gam) and cumulative
        models always skip, because their per-model df has cumulative
        multi-month spans dropped — the plot would then show e.g. a
        31-day "full-season" MAX_ETREF instead of the actual planting-to-
        harvest cumulative. The first broad model (typically catboost or
        tabpfn) populates; subsequent broad models hit the dir-exists
        idempotency check inside cid_vs_yield_scatters and skip too.
        """
        if self.top_n_pearson:
            self.logger.debug(
                f"cid_vs_yield_scatters: skipping top-N model {self.model_name}"
            )
            return
        if self.auto_select_cids_flag:
            self.logger.debug(
                f"cid_vs_yield_scatters: skipping auto-select model {self.model_name}"
            )
            return
        if self.monthly_only_features:
            self.logger.debug(
                "cid_vs_yield_scatters: skipping monthly-only model"
            )
            return
        if self.use_single_time_period_as_feature:
            self.logger.debug(
                "cid_vs_yield_scatters: skipping single-time-period model"
            )
            return
        if "all" not in self.use_cids:
            self.logger.debug(
                f"cid_vs_yield_scatters: skipping model with use_cids != ['all'] "
                f"(got {self.use_cids})"
            )
            return

        from .viz.diagnostics import cid_vs_yield_scatters

        out_root = self.dir_analysis / "explore" / "cid_vs_yield"

        season_stages = None
        sim = getattr(self, "simulation_stages", None)
        if sim and isinstance(sim[0], (list, tuple)):
            season_stages = max((len(s) for s in sim), default=None)

        cid_vs_yield_scatters(
            df, target_col=self.target, dir_out=out_root,
            country=self.country, crop=self.crop, year_col="Harvest Year",
            method=getattr(self, "method", "monthly"),
            season_stages=season_stages,
        )

    def _filter_by_simulation_stages(self) -> pd.DataFrame:
        """Filter data to include only simulation stages.

        Augmented for forward-looking forecast leads: when
        ``self._remaining_season_months`` is set (multi-step in-season
        mode with forecast types in ``use_cids``), additionally admit
        FLDAS/S2S rows whose target ``Stage_ID`` is a future-season month
        AND whose ``Index`` carries the freshest-init LEAD number
        ``(target - latest_covered) mod 12``. This brings forward-looking
        forecasts into ``X_train`` so "All CIDs" gets the same forecast
        signal as "FLDAS Only" / "S2S Only" — without ever admitting a
        stale older-init lead for the same target.
        """
        stages_list = [
            stages.convert_stage_string(s, to_array=False)
            for s in self.simulation_stages
        ]
        mask = self.df_inputs["Stage_ID"].isin(stages_list)

        remaining = getattr(self, "_remaining_season_months", None) or []
        latest_covered = getattr(self, "_latest_covered_month", None)
        keep_forecast = (
            "all" in self.use_cids
            or any(t in self.use_cids for t in ("FLDAS", "S2S"))
        )
        if (
            keep_forecast
            and remaining
            and latest_covered is not None
            and "Type" in self.df_inputs.columns
            and "Index" in self.df_inputs.columns
        ):
            sid = pd.to_numeric(self.df_inputs["Stage_ID"], errors="coerce")
            lead = (
                self.df_inputs["Index"].astype(str)
                .str.extract(r"_LEAD(\d+)", expand=False)
                .astype("Int64")
            )
            future_set = {int(m) for m in remaining}
            # Freshest init for target M at this step = LEAD (M - L) mod 12
            expected_lead = (sid - int(latest_covered)) % 12
            fresh_future_mask = (
                self.df_inputs["Type"].isin(("FLDAS", "S2S"))
                & sid.isin(future_set)
                & (lead == expected_lead)
            )
            n_admitted = int(fresh_future_mask.sum())
            if n_admitted:
                self.logger.info(
                    f"Admitting {n_admitted} fresh-init forward-looking "
                    f"FLDAS/S2S rows (latest_covered={latest_covered}, "
                    f"future_targets={sorted(future_set)})"
                )
                mask = mask | fresh_future_mask

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

    def _get_model_int(self, key: str, default: int) -> int:
        """Read int key from [model_name] section, fall back to [ML] then default."""
        for section in (self.model_name, "ML"):
            if self.parser.has_option(section, key):
                try:
                    return self.parser.getint(section, key)
                except (ValueError, TypeError):
                    pass
        return default

    def _get_model_float(self, key: str, default: float) -> float:
        """Read float key from [model_name] section, fall back to [ML] then default."""
        for section in (self.model_name, "ML"):
            if self.parser.has_option(section, key):
                try:
                    return self.parser.getfloat(section, key)
                except (ValueError, TypeError):
                    pass
        return default

    def _record_fallback(self, category: str, **details) -> None:
        """Append a fallback event to ``<dir_analysis>/fallbacks/fallback_<pid>.csv``.

        Diagnostic-only; best-effort write (silently swallows IO errors
        because failure-to-log a fallback shouldn't crash a training
        fold). Per-PID file avoids cross-worker CSV append races under
        do_parallel_ml=True. End-of-run summary merges all PID files.

        Categories:
        - ``pearson_summary_missing``  auto_/top10_ filter couldn't load
            the pre-computed pearson_summary.csv AND inline compute failed.
        - ``pearson_summary_empty``  loaded/computed but produced 0 rows.
        - ``auto_select_zero``  schema returned 0 CIDs at the |r| floor.
        - ``top_n_empty_survivors``  top10_ filter found no kept rows.
        - ``correlation_selection_empty``  per-region correlation filter
            returned no features; model trains on all CID columns.
        """
        try:
            import csv
            row = {
                "timestamp": ar.utcnow().to("America/New_York").isoformat(),
                "pid": os.getpid(),
                "category": category,
                "model": getattr(self, "model_name", ""),
                "country": getattr(self, "country", ""),
                "crop": getattr(self, "crop", ""),
                "forecast_season": getattr(self, "forecast_season", ""),
                "stage_name": (
                    getattr(self, "stage_info", {}).get("Stage Name", "")
                    if hasattr(self, "stage_info") else ""
                ),
            }
            row.update({k: str(v) for k, v in details.items()})
            fall_dir = self.dir_analysis / "fallbacks"
            fall_dir.mkdir(parents=True, exist_ok=True)
            fpath = fall_dir / f"fallback_{os.getpid()}.csv"
            file_exists = fpath.exists()
            with open(fpath, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(row.keys()))
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        except Exception:  # noqa: BLE001
            pass

    def _load_or_compute_pearson_summary(self, df_long=None):
        """Load (pearson_df, corr) from the EDA dir if present; otherwise
        compute inline from ``df_long`` and persist for siblings.

        Needed because top<N>_ / auto_ models can fire (via parallel ML
        scheduling) BEFORE the broad-feature model has populated
        ``pearson_summary.csv``. The inline fallback computes the same
        pearson summary on demand using this fold's long-format CID df
        (best-effort persist so sibling folds skip the recompute).

        Returns ``(pearson_df, corr)`` where ``pearson_df`` is indexed
        by CID name. Returns ``(None, None)`` if no usable data exists.
        """
        explore_dir = (
            self.dir_analysis / "explore" / "cid_vs_yield"
            / self.country / self.crop / "csvs"
        )
        summary_path = explore_dir / "pearson_summary.csv"
        corr_path = explore_dir / "pearson_corr_matrix.csv"

        if summary_path.exists() and corr_path.exists():
            try:
                pearson_df = pd.read_csv(summary_path).set_index("cid")
                corr = pd.read_csv(corr_path, index_col=0)
                return pearson_df, corr
            except Exception as exc:  # noqa: BLE001
                self.logger.warning(
                    f"  {self.model_name}: pearson summary read failed "
                    f"({exc}); will recompute inline."
                )

        if df_long is None or df_long.empty:
            self.logger.warning(
                f"  [{self.country} {self.crop} {self.model_name} "
                f"forecast_season={getattr(self, 'forecast_season', '?')}] "
                f"no df available for inline pearson compute; "
                f"falling back to existing use_cids."
            )
            self._record_fallback(
                "pearson_summary_missing",
                reason="no df available for inline compute",
            )
            return None, None

        self.logger.info(
            f"  {self.model_name}: pearson_summary.csv missing — computing "
            f"inline from {len(df_long)} long rows (parallel-race fallback)."
        )
        try:
            wide = utils.pivot_long_for_pearson(df_long, self.target)
            method = getattr(self, "method", "monthly")
            season_stages = None
            sim = getattr(self, "simulation_stages", None)
            if sim and isinstance(sim[0], (list, tuple)):
                season_stages = max((len(s) for s in sim), default=None)
            pearson_df, corr = utils.compute_pearson_summary(
                wide, target_col=self.target,
                method=method, season_stages=season_stages,
            )
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                f"  {self.model_name}: inline pearson compute failed: {exc}"
            )
            return None, None

        if pearson_df is None or pearson_df.empty:
            return None, None

        # Best-effort persist so sibling folds in the same run skip the
        # recompute. Failure to write is non-fatal (siblings just retry).
        try:
            explore_dir.mkdir(parents=True, exist_ok=True)
            pearson_df.reset_index().to_csv(summary_path, index=False)
            if not corr.empty:
                corr.to_csv(corr_path)
        except Exception:  # noqa: BLE001
            pass

        return pearson_df, corr

    def _apply_top_n_pearson_filter(self, df_long=None) -> None:
        """Override self.use_cids with the top-N deduplicated CIDs.

        Loads pearson_summary.csv if present, otherwise computes inline
        from ``df_long`` (parallel-race fallback). Keeps the first N
        rows where ``kept == True`` (survivors of the mutual-correlation
        dedup at 0.9). Falls back to existing use_cids only when neither
        source is usable.
        """
        _tag = (
            f"[{self.country} {self.crop} {self.model_name} "
            f"forecast_season={getattr(self, 'forecast_season', '?')}]"
        )
        pearson_df, _corr = self._load_or_compute_pearson_summary(df_long)
        if pearson_df is None or pearson_df.empty:
            self.logger.warning(
                f"  {_tag} no pearson summary available — "
                f"falling back to existing use_cids "
                f"(use_cids={self.use_cids})."
            )
            self._record_fallback("pearson_summary_missing",
                                  fallback_use_cids=self.use_cids)
            return
        if "kept" not in pearson_df.columns:
            self.logger.warning(
                f"  {_tag} pearson summary missing 'kept' column "
                f"(stale schema); falling back to existing use_cids "
                f"(use_cids={self.use_cids})."
            )
            self._record_fallback("pearson_summary_stale_schema",
                                  fallback_use_cids=self.use_cids)
            return
        survivors = pearson_df[pearson_df["kept"]].head(self.top_n_pearson)
        top_cids = survivors.index.tolist()
        if not top_cids:
            self.logger.warning(
                f"  {_tag} no surviving CIDs in pearson summary; "
                f"falling back to existing use_cids "
                f"(use_cids={self.use_cids})."
            )
            self._record_fallback("top_n_empty_survivors",
                                  fallback_use_cids=self.use_cids,
                                  n_pearson_rows=len(pearson_df))
            return
        self.use_cids = top_cids
        self.select_cid_by = "Index"
        self.logger.info(
            f"  {self.model_name}: restricted to top {len(top_cids)} CIDs: "
            f"{top_cids}"
        )

    def _apply_auto_pearson_filter(self, df_long=None) -> None:
        """Override self.use_cids using the at-least-X-above-Y schema.

        Loads pearson_summary + corr matrix from the EDA dir if present,
        otherwise computes inline from ``df_long`` (parallel-race
        fallback). Applies the dedup-first relaxation policy in
        utils.auto_select_cids. Logs the relaxation trail and persists
        it as a per-model CSV for audit.
        """
        _tag = (
            f"[{self.country} {self.crop} {self.model_name} "
            f"forecast_season={getattr(self, 'forecast_season', '?')}]"
        )
        explore_dir = (
            self.dir_analysis / "explore" / "cid_vs_yield"
            / self.country / self.crop / "csvs"
        )
        pearson_df, corr = self._load_or_compute_pearson_summary(df_long)
        if pearson_df is None or pearson_df.empty:
            self.logger.warning(
                f"  {_tag} no pearson summary available — "
                f"falling back to existing use_cids (use_cids={self.use_cids})."
            )
            self._record_fallback("pearson_summary_missing",
                                  fallback_use_cids=self.use_cids)
            return
        if corr is None or corr.empty:
            self.logger.warning(
                f"  {_tag} corr matrix unavailable — schema requires it "
                f"for dedup; falling back to existing use_cids "
                f"(use_cids={self.use_cids})."
            )
            self._record_fallback("auto_corr_matrix_missing",
                                  fallback_use_cids=self.use_cids)
            return
        selected, relax_log = utils.auto_select_cids(
            pearson_df, corr,
            self.auto_min_count, self.auto_min_abs_r,
            self.auto_dedup_threshold, self.auto_dedup_max,
            self.auto_abs_r_floor, self.auto_abs_r_step,
        )
        report_path = explore_dir / f"auto_select_{self.model_name}.csv"
        try:
            pd.DataFrame(
                relax_log,
                columns=["step", "dedup_threshold", "abs_r_floor", "n_selected"],
            ).to_csv(report_path, index=False)
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                f"  {_tag} failed to persist relaxation report: {exc}"
            )
        if not selected:
            self.logger.warning(
                f"  {_tag} auto-select returned 0 CIDs at floor — "
                f"falling back to existing use_cids (use_cids={self.use_cids})."
            )
            self._record_fallback("auto_select_zero",
                                  fallback_use_cids=self.use_cids,
                                  relax_steps=len(relax_log),
                                  final_step=relax_log[-1][0] if relax_log else "")
            return
        self.use_cids = selected
        self.select_cid_by = "Index"
        final = relax_log[-1]
        self.logger.info(
            f"  {self.model_name}: auto-selected {len(selected)} CIDs "
            f"(final dedup={final[1]:.2f}, |r| floor={final[2]:.2f}, "
            f"steps={len(relax_log)}, report={report_path.name}): {selected}"
        )

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

        # Repair invalid rings before reprojecting. A single malformed polygon
        # in the boundary file makes GEOS abort the WHOLE to_crs with
        # "Points of LinearRing do not form a closed linestring", killing the
        # run — seen on usa_admin2 with the full 10-state county set (the
        # 3-state subset happened to miss the bad county). Only the offending
        # geometries should degrade, not the entire country.
        _g = self.dg_country.geometry
        _bad = ~_g.is_valid & _g.notna()
        if _bad.any():
            self.logger.warning(
                f"boundary geometry: repairing {int(_bad.sum())} invalid "
                f"polygon(s) before centroid reprojection "
                f"(make_valid; e.g. unclosed LinearRing)"
            )
            try:
                self.dg_country = self.dg_country.assign(
                    geometry=_g.make_valid()
                )
            except AttributeError:  # shapely < 2.1 / older geopandas
                self.dg_country = self.dg_country.assign(geometry=_g.buffer(0))
        try:
            centroids = self.dg_country.to_crs(epsg=6933).centroid.to_crs(epsg=4326)
        except Exception as exc:
            # Last resort: per-geometry so one unfixable polygon costs its own
            # region's centroid (NaN -> handled downstream) instead of the run.
            self.logger.warning(
                f"centroid reprojection failed wholesale ({type(exc).__name__}: "
                f"{exc}); falling back to per-geometry centroids"
            )
            import geopandas as _gpd
            _rows = []
            for _geom in self.dg_country.geometry:
                try:
                    _c = _gpd.GeoSeries([_geom], crs=self.dg_country.crs)                         .to_crs(epsg=6933).centroid.to_crs(epsg=4326).iloc[0]
                except Exception:
                    _c = None
                _rows.append(_c)
            centroids = _gpd.GeoSeries(_rows, crs="EPSG:4326")
        self.dg_country["lat"] = centroids.y.to_numpy()
        self.dg_country["lon"] = centroids.x.to_numpy()

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
        """Generate correlation plots and return selected features.

        Model-agnostic step: (dict_selected_features, dict_best_cid) depend
        only on df (features + observed yield), never on self.model_name. To
        avoid recomputing + rewriting identical PNGs for every model in the
        (country, crop, season) loop, cache the result to disk keyed by
        (country, crop, forecast_season, simulation_stages) and short-circuit
        subsequent workers. First worker computes + plots + writes cache;
        peers hit the cache and skip plot rendering entirely.

        Two workers may race the first compute (both cache-miss); atomic
        rename below ensures the on-disk file is never partial.
        """
        if not self.correlation_plots:
            return {}, {}

        kwargs = self._build_correlation_kwargs()

        cache_path = self._correlation_cache_path(kwargs["dir_output"])
        cached = self._load_correlation_cache(cache_path)
        if cached is not None:
            self.logger.info(
                f"Correlation plot cache HIT for {self.country} {self.crop} "
                f"({self.model_name} — skipping recompute+replot)"
            )
            return cached

        self.logger.info(f"Correlation plot for {self.country} {self.crop}")
        result = correlations.all_correlated_feature_by_time(df, **kwargs)
        self._save_correlation_cache(cache_path, result)
        return result

    def _correlation_cache_path(self, dir_output: Path) -> Path:
        """Cache pickle path keyed on everything that determines the cached
        (dict_selected_features, dict_best_cid).

        The cached result depends not only on the stage subset but on WHICH
        CIDs are available and how they are selected. Keying on
        simulation_stages alone meant two runs that differed only in use_cids /
        select_cid_by / feature_selection / correlation_threshold (e.g. an
        index sweep, or simply editing use_cids and re-running the same day)
        collided on the date-scoped cache and silently reused stale features.
        Include those knobs in the signature. forecast_season/year are already
        in dir_output.
        """
        import hashlib
        sim = getattr(self, "simulation_stages", None)
        sim_src = str(sorted(str(s) for s in sim)) if sim is not None else "default"
        uc = getattr(self, "use_cids", None)
        uc_src = str(sorted(map(str, uc))) if isinstance(uc, (list, tuple, set)) else str(uc)
        parts = [
            sim_src,
            uc_src,
            str(getattr(self, "select_cid_by", "")),
            str(getattr(self, "feature_selection", "")),
            str(getattr(self, "correlation_threshold", "")),
            str(getattr(self, "correlation_metric", "")),
        ]
        sig = hashlib.md5("|".join(parts).encode()).hexdigest()[:12]
        return dir_output / "_corr_cache" / f"step_{sig}.pkl"

    def _load_correlation_cache(self, cache_path: Path):
        """Return cached (dict_selected_features, dict_best_cid) or None."""
        if not cache_path.exists():
            return None
        try:
            import pickle
            with open(cache_path, "rb") as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError, OSError) as e:
            self.logger.warning(
                f"Correlation cache at {cache_path} unreadable ({e}); recomputing"
            )
            return None

    def _save_correlation_cache(self, cache_path: Path, result) -> None:
        """Atomically persist correlation result via tmp + rename."""
        import pickle
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = cache_path.with_suffix(cache_path.suffix + ".tmp")
        try:
            with open(tmp, "wb") as f:
                pickle.dump(result, f)
            os.replace(tmp, cache_path)
        except OSError as e:
            self.logger.warning(f"Failed to write correlation cache {cache_path}: {e}")
            if tmp.exists():
                try:
                    tmp.unlink()
                except OSError:
                    pass

    def _build_correlation_kwargs(self) -> Dict:
        """Build keyword arguments for correlation analysis."""
        return {
            "all_stages": self.all_stages,
            "target_col": self.target,
            "country": self.country,
            "crop": self.crop,
            "dir_output": (
                self.dir_analysis / self.country / self.crop /
                str(self.forecast_season)
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
            "plot_correlation_scatter": self.plot_correlation_scatter,
        }

    def _prepare_train_test_split(self, df: pd.DataFrame):
        """Separate data into training and testing sets.

        When ``target_mode == "region_anomaly"`` (and not detrending), subtract
        each region's training-year mean from the target column so the model
        fits on per-region yield anomalies. Region means are stored in
        ``self._region_target_means`` for re-addition at prediction time.
        Regions with fewer than ``region_anomaly_min_years`` training rows are
        dropped from both df_train and df_test (we can't compute a stable mean
        for them and predictions wouldn't be retrievable without one).
        """
        df[f"{self.target}_class"] = np.nan

        mask = df["Harvest Year"] == self.forecast_season
        self.df_train = df[~mask].copy()
        self.df_test = df[mask].copy()

        self.df_train = self.df_train.dropna(subset=[self.target])

        # Per-country training-year floor: [<country>] training_year_start in
        # countries.txt. If set, drops df_train rows with Harvest Year < this
        # value BEFORE ML / baseline computations see them. Affects ALL models
        # (ML + null + trend + trend_all) — use when a country's yield history
        # has a genuine regime break AND you want every model to only train on
        # the recent regime. Example: Kenya Long-rains has data 1991-2001 then
        # a 13-year gap then 2015-2024; setting training_year_start = 2015
        # excludes the pre-gap chunk from every model's training set.
        # df_test is left untouched (LOOCV forecasts still span the full
        # outlook_since_year..current_year range).
        country_key = self.country.lower().replace(" ", "_") if getattr(self, "country", None) else None
        if country_key and self.parser.has_option(country_key, "training_year_start"):
            try:
                yr_floor = self.parser.getint(country_key, "training_year_start")
                before = len(self.df_train)
                self.df_train = self.df_train[
                    self.df_train["Harvest Year"].astype(int) >= yr_floor
                ].copy()
                dropped = before - len(self.df_train)
                if dropped > 0:
                    cache_key = (self.country, self.crop, yr_floor, dropped)
                    if getattr(self, "_last_year_floor_drop", None) != cache_key:
                        self.logger.warning(
                            f"training_year_start={yr_floor}: dropped {dropped} "
                            f"df_train rows with Harvest Year < {yr_floor} "
                            f"({self.country}/{self.crop})"
                        )
                        self._last_year_floor_drop = cache_key
            except (ValueError, TypeError):
                pass

        # General min-years-per-region filter. Drops regions whose training-row
        # count is below [ML] min_years_per_region from both df_train and
        # df_test. Applied here so it composes with region_anomaly_min_years
        # below (region_anomaly will then operate on the surviving regions
        # only) and so every downstream consumer of df_train (CCC filter,
        # feature engineering, model fit) sees the same filtered set.
        if (
            self.min_years_per_region > 0
            and "Region" in self.df_train.columns
            and self.target in self.df_train.columns
        ):
            admin_col = (
                "Country__Region"
                if getattr(self, "countries_pooled", None)
                and "Country__Region" in self.df_train.columns
                else "Region"
            )
            counts = self.df_train.groupby(admin_col)[self.target].count()
            keep = counts[counts >= self.min_years_per_region].index.tolist()
            dropped = sorted(set(counts.index) - set(keep))
            if dropped:
                # Dedup the warning across LOOCV folds — log once per
                # (country, crop, threshold, dropped-set).
                cache_key = (
                    self.country,
                    self.crop,
                    self.min_years_per_region,
                    frozenset(dropped),
                )
                if getattr(self, "_last_min_years_drop", None) != cache_key:
                    self.logger.warning(
                        f"  min_years_per_region={self.min_years_per_region}: "
                        f"dropping {len(dropped)} region(s) with < "
                        f"{self.min_years_per_region} training rows: "
                        f"{dropped[:10]}{'...' if len(dropped) > 10 else ''}"
                    )
                    self._last_min_years_drop = cache_key
                self.df_train = self.df_train[
                    self.df_train[admin_col].isin(keep)
                ].copy()
                self.df_test = self.df_test[
                    self.df_test[admin_col].isin(keep)
                ].copy()

        # Min-production-share filter — drops regions whose mean training-year
        # share of national production is below [ML] min_production_share
        # (units: percent). Applied AFTER min_years_per_region so year-sparse
        # regions are dropped first. Production = Area (ha) x Yield (tn/ha)
        # summed within (region, year), share = region_prod / national_prod
        # per year, then averaged across training years for stability
        # (leak-safe: uses df_train only, computed post-LOOCV split).
        if (
            self.min_production_share > 0.0
            and "Region" in self.df_train.columns
            and "Area (ha)" in self.df_train.columns
            and self.target in self.df_train.columns
        ):
            admin_col = (
                "Country__Region"
                if getattr(self, "countries_pooled", None)
                and "Country__Region" in self.df_train.columns
                else "Region"
            )
            prod = (
                self.df_train[[admin_col, "Harvest Year", "Area (ha)", self.target]]
                .assign(
                    _prod_tn=lambda d: d["Area (ha)"].astype(float)
                    * d[self.target].astype(float)
                )
                .groupby([admin_col, "Harvest Year"], as_index=False)["_prod_tn"].sum()
            )
            national_annual = prod.groupby("Harvest Year")["_prod_tn"].sum()
            prod["_share_pct"] = 100.0 * prod["_prod_tn"] / prod["Harvest Year"].map(national_annual)
            mean_share = prod.groupby(admin_col)["_share_pct"].mean()
            keep_ps = mean_share[mean_share >= self.min_production_share].index.tolist()
            dropped_ps = sorted(set(mean_share.index) - set(keep_ps))
            if dropped_ps:
                cache_key = (
                    self.country,
                    self.crop,
                    self.min_production_share,
                    frozenset(dropped_ps),
                )
                if getattr(self, "_last_min_share_drop", None) != cache_key:
                    dropped_shares = {
                        r: round(mean_share[r], 3) for r in dropped_ps[:10]
                    }
                    self.logger.warning(
                        f"  min_production_share={self.min_production_share}%: "
                        f"dropping {len(dropped_ps)} region(s) below threshold: "
                        f"{dropped_shares}{'...' if len(dropped_ps) > 10 else ''}"
                    )
                    self._last_min_share_drop = cache_key
                self.df_train = self.df_train[
                    self.df_train[admin_col].isin(keep_ps)
                ].copy()
                self.df_test = self.df_test[
                    self.df_test[admin_col].isin(keep_ps)
                ].copy()

        # Within-year neighbor-yield leakage (0.4.774+, opt-in via
        # [ML] use_neighbor_leakage=True). Injects k nearest centroid
        # neighbors' forecast-year rows back into df_train. Default
        # OFF — when off this branch is a no-op. Done AFTER min-years
        # filtering so leaked rows aren't dropped by the region-presence
        # check, and BEFORE region-anomaly demean so the demean stats
        # see the augmented training set.
        if self.use_neighbor_leakage and self.n_leaked_neighbors > 0:
            from geocif.ml.neighbor_leakage import (
                build_centroid_lookup_from_gdf, inject_leaked_rows,
            )
            # Cache the centroid lookup on self — same (country, crop,
            # season) hits this code path for every forecast year, no
            # need to rebuild the gdf-derived lookup each call.
            if not hasattr(self, "_neighbor_centroids"):
                self._neighbor_centroids = build_centroid_lookup_from_gdf(
                    self.dg, region_col="ADM1_NAME",
                )
            self.df_train = inject_leaked_rows(
                df_train=self.df_train,
                df_full=df,
                test_regions=list(self.df_test["Region"].astype(str).unique())
                if "Region" in self.df_test.columns else [],
                target_year=int(self.forecast_season),
                centroids=self._neighbor_centroids,
                k=int(self.n_leaked_neighbors),
                target_col=self.target,
                region_col="Region",
                year_col="Harvest Year",
                logger=self.logger,
            )

        # Region-anomaly target transform (leak-safe: uses train years only).
        # Only computes the per-region mean lookup + prunes regions with too
        # few training rows. The actual demean of y_train happens later in
        # _setup_training_data so that df_train[self.target] stays absolute
        # (used by _compute_yield_trend_feature, last_observed_map, plots).
        self._region_target_means = {}
        if (
            self.target_mode == "region_anomaly"
            and not self.check_yield_trend
            and self.target in self.df_train.columns
            and "Region" in self.df_train.columns
        ):
            admin_col = (
                "Country__Region"
                if getattr(self, "countries_pooled", None)
                and "Country__Region" in self.df_train.columns
                else "Region"
            )
            counts = self.df_train.groupby(admin_col)[self.target].count()
            keep = counts[counts >= self.region_anomaly_min_years].index.tolist()
            dropped = sorted(set(counts.index) - set(keep))
            if dropped:
                # Dedup: only emit when the (country, crop, dropped-set)
                # changes. Same skipped regions across all LOOCV folds for
                # one crop → log once, not per fold.
                cache_key = (self.country, self.crop, frozenset(dropped))
                if getattr(self, "_last_region_anomaly_drop", None) != cache_key:
                    self.logger.warning(
                        f"  region_anomaly: skipping {len(dropped)} region(s) "
                        f"with < {self.region_anomaly_min_years} training rows: "
                        f"{dropped[:10]}{'...' if len(dropped) > 10 else ''}"
                    )
                    self._last_region_anomaly_drop = cache_key
            self._region_target_means = (
                self.df_train[self.df_train[admin_col].isin(keep)]
                .groupby(admin_col)[self.target]
                .mean()
                .to_dict()
            )
            # Drop skipped regions from train + test (no usable mean to re-add)
            self.df_train = self.df_train[
                self.df_train[admin_col].isin(keep)
            ].copy()
            self.df_test = self.df_test[
                self.df_test[admin_col].isin(keep)
            ].copy()
            if self._region_target_means:
                self.logger.info(
                    f"  region_anomaly: stored means for {len(self._region_target_means)} "
                    f"region(s) (mean-of-means="
                    f"{np.mean(list(self._region_target_means.values())):.3f}); "
                    f"y_train will be demeaned in _setup_training_data"
                )

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
            # "past" mode: restrict to years strictly before the forecast
            # year so the trend used for predicting Y(forecast) is fit only
            # on data that would be available at deployment time (no leak
            # from LOOCV's future training years).
            if self.use_yield_trend_as_feature == "past":
                group = group[
                    group["Harvest Year"].astype(float) < float(self.forecast_season)
                ]
                if len(group) < 5:
                    self.logger.warning(
                        f"  Yield Trend [{region_name}]: only {len(group)} "
                        f"past training rows for forecast_season="
                        f"{self.forecast_season}; skipping (need >= 5 for OLS)"
                    )
                    continue

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

    def _compute_trend_all_feature(self):
        """Compute per-admin Theil-Sen trend on ALL training years and
        write to ``Trend All`` column on both df_train and df_test.

        Mirrors the [trend_all] baseline model: simple linear Theil-Sen
        on every training row for the admin (no past-only filter, no
        12-year cap, no BEAST changepoint detection).  Coexists with
        ``Yield Trend`` (BEAST-segmented) when both flags are on — the
        two columns are independent features and the model can choose.

        LOOCV-safe: forecast year is already excluded from df_train by
        _prepare_train_test_split, so the slope fit never sees the held-
        out year.  Skipped when ``check_yield_trend`` is on (target
        detrending already absorbs the trend).
        """
        if not self.use_trend_all_as_feature:
            return
        if self.check_yield_trend:
            self.logger.warning(
                "  use_trend_all_as_feature is incompatible with "
                "check_yield_trend (target detrending). "
                "Skipping Trend All feature."
            )
            return

        from scipy.stats import theilslopes

        self.df_train["Trend All"] = np.nan
        self.df_test["Trend All"] = np.nan

        for region_name, group in self.df_train.groupby("Region", observed=True):
            x = group["Harvest Year"].astype(float).values
            y = group[self.target].astype(float).values
            valid = ~np.isnan(x) & ~np.isnan(y)
            if valid.sum() < 3:
                continue
            xv, yv = x[valid], y[valid]
            if len(np.unique(xv)) < 2:
                # theilslopes requires >= 2 distinct x-values.
                continue
            slope, intercept, _lo, _hi = theilslopes(yv, xv)

            train_mask = self.df_train["Region"] == region_name
            test_mask = self.df_test["Region"] == region_name
            tr_yrs = self.df_train.loc[train_mask, "Harvest Year"].astype(float).values
            te_yrs = self.df_test.loc[test_mask, "Harvest Year"].astype(float).values
            self.df_train.loc[train_mask, "Trend All"] = intercept + slope * tr_yrs
            self.df_test.loc[test_mask, "Trend All"] = intercept + slope * te_yrs

            self.logger.info(
                f"  Trend All [{region_name}]: "
                f"slope={slope:.4f} t/ha/yr, n_used={int(valid.sum())}"
            )

    def _compute_region_zscore_features(self):
        """Per-region z-scored sibling features for configured CID bases.

        For each base in ``self.region_zscore_cids``, finds every wide-format
        column starting with ``"<base> "`` (one per stage after the pivot
        appends the stage suffix) and writes a companion
        ``"<base>_zreg <stage>"`` column:

            zreg = (raw − region_train_mean) / region_train_std    (clipped ±5)

        Per-region stats use ``df_train`` rows only (leak-safe per LOOCV
        fold). Regions / columns with std < 1e-9 or < 3 valid training rows
        produce NaN (CatBoost / TabPFN handle NaN natively).

        Closes the encoding gap when ``target_mode = region_anomaly`` puts y
        in anomaly space while X stays raw: the model now sees relative
        anomalies directly instead of trying to recover them via Region
        interactions on raw values.
        """
        if not self.region_zscore_cids:
            return
        admin_col = (
            "Country__Region"
            if getattr(self, "countries_pooled", None)
            and "Country__Region" in self.df_train.columns
            else "Region"
        )
        # Resolve the ['all'] sentinel to every time-varying CID base present,
        # excluding static embeddings (AEF/soilgrids), categorical columns and
        # yield-derived features. Country-agnostic: no hand-curated list, so it
        # works for countries/crops where the informative CIDs are unknown —
        # gOMP selects the useful anomalies per (country, crop) fold.
        bases = self.region_zscore_cids
        if len(bases) == 1 and str(bases[0]).strip().lower() == "all":
            bases = self._all_zscore_bases()
            self.logger.info(
                f"  region_zscore: 'all' mode -> {len(bases)} time-varying CID base(s)"
            )
        std_floor = 1e-9
        n_added = 0
        dropped_raw = 0
        for base in bases:
            matching = [
                c for c in self.df_train.columns
                if (c == base or str(c).startswith(f"{base} "))
                and pd.api.types.is_numeric_dtype(self.df_train[c])
            ]
            for col in matching:
                stats = self.df_train.groupby(admin_col)[col].agg(
                    ["mean", "std", "count"]
                )
                stats.loc[stats["count"] < 3, "std"] = np.nan
                stats.loc[stats["std"].fillna(0) < std_floor, "std"] = np.nan
                mu_lookup = stats["mean"].to_dict()
                sd_lookup = stats["std"].to_dict()
                # Insert "_zreg" right after the base name so the stage
                # suffix is preserved (e.g. "STD_ETREF Jul 1-Apr 30" →
                # "STD_ETREF_zreg Jul 1-Apr 30"). For bare-base columns
                # without a stage suffix, just append "_zreg".
                zname = (
                    col.replace(base, f"{base}_zreg", 1)
                    if " " in str(col) else f"{col}_zreg"
                )
                for df in (self.df_train, self.df_test):
                    if df.empty or col not in df.columns:
                        continue
                    mu = df[admin_col].map(mu_lookup).astype(float)
                    sd = df[admin_col].map(sd_lookup).astype(float)
                    df[zname] = (
                        (df[col].astype(float) - mu) / sd
                    ).clip(-5, 5)
                n_added += 1
                # z-score-only mode: drop the raw sibling now that _zreg exists.
                if self.region_zscore_replace_raw:
                    for df in (self.df_train, self.df_test):
                        if col in df.columns:
                            df.drop(columns=[col], inplace=True)
                            dropped_raw += 1
        if n_added:
            self.logger.info(
                f"  region_zscore: added {n_added} sibling z-scored "
                f"column(s) for {len(bases)} base CID(s)"
                + (f"; dropped {dropped_raw} raw column(s) [replace_raw]"
                   if self.region_zscore_replace_raw else "")
            )

    def _all_zscore_bases(self):
        """Resolve region_zscore_cids=['all'] to every time-varying CID base in
        df_train, excluding NON-CID columns: static embeddings (AEF/soilgrids),
        categorical, geo, and — critically — the yield / Production / Area /
        Season bookkeeping columns from geocif's harvest schema.

        LEAKAGE GUARD: ``Production`` (= yield x area) and any ``Yield`` column
        are target proxies; z-scoring them per region reproduces the yield
        anomaly (the target), so gOMP would select them and inflate skill. They
        are hard-excluded here. (This was a real bug: an earlier version
        z-scored ``Production (tn)`` and it was selected in 20/20 folds for
        brazil rice/soybean/winter_wheat.) Country-agnostic — geocif's id/meta
        schema is stable — so it still generalizes to unknown-driver crops."""
        import re as _re
        stage_re = _re.compile(r" [A-Z][a-z]{2} \d+-[A-Z][a-z]{2} \d+$")
        cat = set(getattr(self, "cat_features", []) or []) | {"Country__Region"}
        soil_kw = ("sand", "clay", "silt", "bdod", "cfvo", "soc", "ocd",
                   "nitrogen", "phh2o", "soil")
        # geocif id/meta + geo + engineered non-CID columns (stable schema).
        skip_exact = {"Country", "Region", "Region_ID", "Harvest Year", "Season",
                      "Area (ha)", "Area", "Latitude", "Longitude", "lat", "lon",
                      "Trend All", "Yield Trend", "AI", getattr(self, "target", "")}
        bases = set()
        for c in self.df_train.columns:
            if not pd.api.types.is_numeric_dtype(self.df_train[c]):
                continue
            b = stage_re.sub("", str(c)).strip()
            if not b or b in cat or b in skip_exact:
                continue
            if b.startswith("AEF") or b.startswith("Detrended"):
                continue
            # Target proxies — NEVER z-score (leakage): the Yield target, any
            # lag/median/analog/last-year Yield, and Production (= yield x area).
            if "Yield" in b or "Production" in b:
                continue
            if any(k in b.lower() for k in soil_kw):
                continue
            bases.add(b)
        return sorted(bases)

    def _diagnose_yield_trend(self):
        """Diag-STFN-style trend-gate diagnostic. Returns (activate: bool,
        message: str). Runs on ``self.df_train`` so it's leak-safe per
        LOOCV fold. Gates:
          1. Pearson r on pooled (Harvest Year, target) with p <= 0.05
          2. Improvement skill score ``Imp = 1 - MSE_trend/MSE_naive >= 0``
             on the latest training year (inner held-out validation),
             using per-region linear trend fit on earlier training years.
        Both must pass; otherwise skip detrending for this (crop, country,
        forecast_season) fold.
        """
        try:
            from scipy.stats import pearsonr as _pearsonr
        except Exception as _e:
            return False, f"scipy unavailable: {_e}"
        df = self.df_train.dropna(subset=[self.target]).copy()
        if df.empty:
            return False, "no training rows"
        # Harvest Year can arrive as an unordered Categorical (set by
        # _add_region_clusters / classify_target machinery); .max() on
        # that raises "Categorical is not ordered for operation max".
        # Coerce to numeric once and reuse throughout the diagnostic.
        years_num = pd.to_numeric(df["Harvest Year"], errors="coerce")
        df = df.assign(_hy_num=years_num).dropna(subset=["_hy_num"])
        if df.empty or df["_hy_num"].nunique() < 5:
            return False, f"too few training years ({df['_hy_num'].nunique() if not df.empty else 0})"
        try:
            r, p = _pearsonr(
                df["_hy_num"].astype(float).values,
                df[self.target].astype(float).values,
            )
        except Exception as _e:
            return False, f"pearsonr failed: {_e}"
        if not np.isfinite(p) or p > 0.05:
            return False, f"r={r:.2f}, p={p:.3g} (not significant)"
        # Inner held-out: latest training year for Imp check
        max_yr = int(df["_hy_num"].max())
        inner_val = df[df["_hy_num"] == max_yr]
        inner_train = df[df["_hy_num"] < max_yr]
        if inner_val.empty or inner_train["_hy_num"].nunique() < 3:
            return False, f"insufficient inner-val history (r={r:.2f}, p={p:.3g})"
        mse_trend = 0.0
        mse_naive = 0.0
        n_val = 0
        for region_name, sub_val in inner_val.groupby("Region", observed=True):
            trn = inner_train[inner_train["Region"] == region_name]
            if trn["_hy_num"].nunique() < 2:
                continue
            years = trn["_hy_num"].astype(float).values
            vals = trn[self.target].astype(float).values
            slope, intercept = np.polyfit(years, vals, 1)
            naive_mean = float(vals.mean())
            for _, row_v in sub_val.iterrows():
                y_true = float(row_v[self.target])
                y_hat_trend = intercept + slope * float(row_v["_hy_num"])
                mse_trend += (y_true - y_hat_trend) ** 2
                mse_naive += (y_true - naive_mean) ** 2
                n_val += 1
        if n_val == 0 or mse_naive <= 0:
            return False, f"no usable inner-val obs (r={r:.2f}, p={p:.3g})"
        imp = 1.0 - (mse_trend / mse_naive)
        if imp < 0:
            return False, f"r={r:.2f}, p={p:.3g}, Imp={imp:.3f} < 0 (trend hurts inner-val)"
        return True, f"r={r:.2f}, p={p:.3g}, Imp={imp:.3f}"

    def _compute_detrended_yield(self):
        """Compute detrended yield for each region."""
        # Diag-STFN-style auto-gate: when [ML] check_yield_trend_diagnostic
        # is True, override self.check_yield_trend for THIS fold based on
        # a statistical test of trend significance + practical gain.
        if self.check_yield_trend_diagnostic:
            activate, msg = self._diagnose_yield_trend()
            prev = self.check_yield_trend
            self.check_yield_trend = bool(activate)
            self._refresh_target_column()
            self.logger.info(
                f"  trend_diagnostic [{self.country}/{self.crop}/"
                f"season={self.forecast_season}]: {msg} -> "
                f"check_yield_trend={self.check_yield_trend} (was {prev})"
            )

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

        # Feature columns = everything except fixed, target, stats, meta.
        #
        # The fixed-window medians from compute_user_median_statistics are
        # REFERENCE columns for post-run anomaly mapping, not features: each is
        # a region-constant mean over a hard-coded window (2013-2017 /
        # 2018-2022) that CONTAINS the fold's own forecast year, so a 2020 fold
        # would see 1/5 of its own target. They are already kept out of
        # `feature_names` (they only ride along in `_get_common_columns` so
        # `_add_median_yield_columns` can write them to the DB) — but without
        # this exclusion the nbr_ wrapper below would manufacture
        # `nbr_Median ... (2018-2022)` and hand it straight to the selector.
        exclude_cols = set(
            self.fixed_columns
            + self.statistics_columns
            + [
                self.target, f"{self.target}_class",
                "Region_ID", "lat", "lon", "Country Region",
                f"Detrended {self.target}", "Detrended Model",
                "Detrended Model Type",
                f"Median {self.target} (2018-2022)",
                f"Median {self.target} (2013-2017)",
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
        # df_source=df_train: the test frame is the held-out year WITH its
        # observed yields, so letting add_neighbor_features derive its
        # per-region yield medians from df_test itself made
        # nbr_mean_yield_hist a weighted mean of the neighbors' observed
        # test-year yields — test-target leakage.
        self.df_test = sn.add_neighbor_features(
            self.df_test, self.neighbor_graph, feature_cols,
            admin_col=admin_col, year_col="Harvest Year",
            yield_col=self.target, prefix="nbr_",
            df_source=self.df_train,
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

    def _group_stages_by_season(self, stages) -> List[list]:
        """Partition simulation stages into growing seasons.

        Two stages belong to the same season when their month sets overlap
        (share >=1 month); disjoint month sets mean different seasons -- e.g.
        Somalia Gu ``{4,5,6,7}`` vs Deyr ``{10,11,12,1}``. Single-season
        countries collapse to one group, so their behavior is unchanged.

        Union-find over the month sets (stage count is tiny, so O(n^2) is
        fine). Avoids ``list.remove`` on numpy arrays (ambiguous truth value).
        """
        stages = [np.asarray(s) for s in stages]
        month_sets = [set(int(x) for x in s) for s in stages]
        n = len(stages)
        parent = list(range(n))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for i in range(n):
            for j in range(i + 1, n):
                if month_sets[i] & month_sets[j]:
                    parent[find(i)] = find(j)

        comps = {}
        for i in range(n):
            comps.setdefault(find(i), []).append(stages[i])
        return list(comps.values())

    def _get_setup_stages(self) -> List[List]:
        """Build per-time-step stage subsets for multi-step execution.

        For ``run_time_steps = all`` or ``N``, returns cumulative prefixes from
        planting forward, built SEPARATELY per growing season (see
        ``_group_stages_by_season``) so multi-season countries emit every
        season instead of collapsing to whichever season owns the single
        longest stage (the Somalia Gu+Deyr bug). Per-season chronological order
        comes from that season's longest Stage_ID; ``_r`` methods store
        harvest→planting, so reversing gives planting-forward — handling
        cross-year seasons (e.g. Oct→Apr = ``[10, 11, 12, 1, 2, 3, 4]``)
        without assuming contiguous ranges.

        Returns:
            List of stage subsets (each a list of numpy arrays).
        """
        if not self.simulation_stages:
            return [self.simulation_stages]

        step = 1
        if self.run_time_steps != "all":
            try:
                step = int(self.run_time_steps)
            except ValueError:
                return [self.simulation_stages]

        all_subsets = []
        for group in self._group_stages_by_season(self.simulation_stages):
            longest = max(group, key=lambda s: len(s))
            chronological = list(reversed([int(x) for x in longest]))
            if len(chronological) <= 1:
                all_subsets.append(group)
                continue

            subsets = []
            for i in range(step, len(chronological) + 1, step):
                allowed = set(chronological[:i])
                subset = [s for s in group if all(int(x) in allowed for x in s)]
                if subset:
                    subsets.append(subset)

            all_periods = set(chronological)
            full_subset = [s for s in group if all(int(x) in all_periods for x in s)]
            if not subsets or len(subsets[-1]) < len(full_subset):
                subsets.append(full_subset)

            all_subsets.extend(subsets)

        return all_subsets if all_subsets else [self.simulation_stages]

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
        df = self._filter_monthly_only_features(df)
        df = self._filter_monthly_plus_fullseason(df)
        df = self._filter_last_n_months(df)
        df = self._filter_current_month_partial_data(df)
        df = self._remove_last_month_data(df)
        df = self._update_column_names(df)
        df = self._add_engineered_features(df)
        df = self._add_project_static_features(df)
        df = self._add_static_eo_features(df)
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
        
        # observed=True is REQUIRED, not cosmetic. pivot_table is an
        # aggregation: with any categorical grouper and observed=False (the
        # pandas default) it materialises the full cartesian product of every
        # grouper's levels. Measured on pandas 2.3.3 with this exact index /
        # columns / values on a real-shaped frame: object dtype -> (2200, 489)
        # in 0.8 s; categorical + observed=False -> MemoryError trying to
        # allocate 8.79 PiB; categorical + observed=True -> identical (2200,
        # 489), bit-identical values, same runtime. The continuous index levels
        # (yield/area/production) crossed with 1,004 Region categories are what
        # explode. Under object dtype this flag is a verified no-op, so it is
        # safe on its own and is a prerequisite for reading these columns as
        # category. Leave dropna at its default — that is what prunes unused
        # Index levels so they cannot become phantom columns.
        df = df.pivot_table(
            index=self.fixed_columns + [self.target] + self.statistics_columns,
            columns=["Index", "Stage_ID"],
            values="CID",
            observed=True,
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

    def _is_season_normalized_method(self) -> bool:
        """True for methods whose stages are season fractions / phenological
        codes rather than calendar periods. The single-calendar-period feature
        filters (monthly_only / single_time_period / monthly_plus_fullseason)
        are calendar-specific and must be skipped for these — their sole CID
        window is the full season, which those filters would wrongly drop.
        """
        return self.method in ("fraction_season", "phenological_stages", "full_season")

    def _filter_single_time_period_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter to keep only single time period features if configured."""
        if self.use_single_time_period_as_feature and not self._is_season_normalized_method():
            df = stages.select_single_time_period_features(df)

        return df

    def _filter_monthly_only_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Keep only single-calendar-period (monthly) features when the
        per-model ``monthly_only_features`` flag is set.

        Stricter than ``_filter_single_time_period_features``: drops 2-stage
        cumulative spans (Jun+Jul) and Pre-Season / In-Season aggregates.
        Used by the ``curated_<algo>`` wrapper sections. Ignored for
        season-normalized methods (fraction_season/phenological_stages/
        full_season), whose calendar-agnostic full-season window would
        otherwise be dropped, leaving zero features.
        """
        if self.monthly_only_features and not self._is_season_normalized_method():
            n_before = df.shape[1]
            df = stages.select_single_calendar_period_features(df)
            self.logger.info(
                f"  monthly_only_features: {n_before} → {df.shape[1]} columns"
            )
        return df

    def _filter_last_n_months(self, df: pd.DataFrame) -> pd.DataFrame:
        """Restrict the feature frame to the TRAILING ``last_n_months`` calendar
        periods of the season (``last<N>m_<algo>`` models, or an explicit
        ``last_n_months`` key).

        Distinct from the cumulative windows the CID stage set already holds:
        this keeps ONLY the most recent N-period span, dropping single months,
        longer spans and earlier N-spans alike. Ignored for season-normalized
        methods, whose calendar-agnostic window has no trailing month to take.

        Takes precedence over ``monthly_only_features`` /
        ``monthly_plus_fullseason_features``: those keep single months, which a
        trailing N-span excludes, so intersecting them would leave zero stage
        features. Warn rather than silently emptying the frame.
        """
        if self.last_n_months is None or self.last_n_months < 1:
            return df
        if self._is_season_normalized_method():
            return df
        if self.monthly_only_features or self.monthly_plus_fullseason_features:
            self.logger.warning(
                f"  last_n_months={self.last_n_months} overrides "
                f"monthly_only_features/monthly_plus_fullseason for "
                f"{self.model_name} — they select single months, which a "
                f"trailing {self.last_n_months}-month span excludes"
            )
        n_before = df.shape[1]
        df = stages.select_last_n_months_features(df, self.last_n_months)
        self.logger.info(
            f"  last_n_months={self.last_n_months}: {n_before} → {df.shape[1]} columns"
        )
        return df

    def _filter_monthly_plus_fullseason(self, df: pd.DataFrame) -> pd.DataFrame:
        """Keep single-month + full-season features when the per-model
        ``monthly_plus_fullseason_features`` flag is set — drops intermediate
        cumulative spans only. Middle ground between monthly-only and the full
        cumulative feature set.
        """
        if self.monthly_plus_fullseason_features and not self._is_season_normalized_method():
            n_before = df.shape[1]
            df = stages.select_monthly_plus_fullseason_features(df)
            self.logger.info(
                f"  monthly_plus_fullseason: {n_before} → {df.shape[1]} columns"
            )
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

    def _add_project_static_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Project-specific static per-region features (one static value per region, invariant over year/DOY).

        Gated by ``[ML] use_irrigation_feature`` (default False). When True,
        injects a categorical ``irrigation_status`` column
        ({irrigated, mixed, rainfed, unknown}) from
        ``{dir_metadata}/poppy_irrigation.csv``, left-joined on Region.

        Currently only wired for the ``poppy`` project (its geocif.txt sets
        the flag True and ships the accompanying CSV), but the flag is generic —
        any project that provides a matching CSV can opt in.
        """
        if not self.parser.getboolean("ML", "use_irrigation_feature", fallback=False):
            return df

        irrig_path = Path(self.parser.get("PATHS", "dir_metadata")) / "poppy_irrigation.csv"
        if not irrig_path.exists():
            self.logger.warning(f"poppy irrigation CSV not found at {irrig_path}; skipping static feature join")
            return df

        irrig = pd.read_csv(irrig_path)[["ADM1_NAME", "irrigation_status"]].rename(
            columns={"ADM1_NAME": "Region"}
        )
        before = len(df)
        df = df.merge(irrig, on="Region", how="left")
        n_missing = df["irrigation_status"].isna().sum()
        if n_missing:
            missing_regs = sorted(df.loc[df["irrigation_status"].isna(), "Region"].dropna().unique().tolist())
            self.logger.warning(
                f"irrigation_status is NaN for {n_missing}/{before} rows "
                f"(regions with no CSV match: {missing_regs}); filling with 'unknown'"
            )
            df["irrigation_status"] = df["irrigation_status"].fillna("unknown")
        self.logger.info(
            f"poppy: joined irrigation_status onto {before} rows "
            f"(unique values: {sorted(df['irrigation_status'].unique().tolist())})"
        )
        return df

    def _add_static_eo_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Join static per-region EO features (Aridity ``AI``, SoilGrids
        ``SOIL_*``) onto the wide ML frame by Region.

        These variables are constant per region (no time/stage dimension),
        so the CID stage does NOT emit them per stage window — that would
        only duplicate one value across every window. Instead the raw
        geomerge columns (``aridity``, ``soil_sand``, ...) are read from the
        crop_t0 CSV and left-joined here, giving ONE bare stage-less column
        per variable. ``create_feature_names`` force-includes whichever of
        these columns exist (gated by ``use_cids``); per-fold selection
        (gOMP etc.) decides their fate.

        Presence-driven: variables missing from the crop_t0 CSV (country
        didn't extract them) are skipped silently.
        """
        countries = (
            list(df["Country"].unique())
            if getattr(self, "countries_pooled", None) and "Country" in df.columns
            else [self.country]
        )
        _norm = lambda s: str(s).lower().replace(" ", "_").replace("-", "_")
        for cid_name, raw_col in di.STATIC_EO_COL_MAP.items():
            per_country = {
                c: self._read_region_static_from_crop_t0(c, self.crop, raw_col)
                for c in countries
            }
            if not any(per_country.values()):
                continue
            if len(countries) > 1:
                df[cid_name] = [
                    per_country.get(c, {}).get(_norm(r))
                    for c, r in zip(df["Country"], df["Region"])
                ]
            else:
                mapping = per_country[countries[0]]
                df[cid_name] = df["Region"].map(lambda r: mapping.get(_norm(r)))
            df[cid_name] = pd.to_numeric(df[cid_name], errors="coerce")
            n = int(df[cid_name].notna().sum())
            self.logger.info(
                f"static EO feature {cid_name} (<- {raw_col}): "
                f"{n}/{len(df)} rows matched"
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
        elif self.cluster_strategy == "crop_calendar_region":
            clusters_assigned = self._cluster_by_calendar_region(df)
            df = df.merge(clusters_assigned, on="Region")
            df["Region_ID"] = df["Region_ID"].astype("category")
        elif self.cluster_strategy == "admin_1":
            clusters_assigned = self._cluster_by_admin1(df)
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

    def _read_region_static_from_crop_t0(self, country: str, crop: str, column: str) -> dict:
        """Return ``{normalized_region: value}`` for a region-static column read
        from the raw geoprepare crop_t0 CSV (e.g. ``calendar_region``,
        ``season_start_month``). Region keys are normalized (lower / spaces and
        hyphens -> underscores) to match the wide-df ``Region`` values.

        Returns ``{}`` (never raises) if the crop_t0 dir/season/CSV/column can't
        be resolved, so callers can fall back gracefully.
        """
        try:
            from geocif.indices_runner import get_input_file_path, get_seasons
            input_dir = get_input_file_path(country, self.parser, data_source="harvest")
            growing_seasons = get_seasons(country, self.parser, crop=crop)
        except Exception as e:
            self.logger.warning(
                f"crop_t0 static read: cannot resolve dir/seasons for {country}: {e}"
            )
            return {}

        country_lower = country.lower().replace(" ", "_")
        crop_lower = crop.lower().replace(" ", "_")
        src = None
        for gs in growing_seasons:
            candidate = input_dir / f"{country_lower}_{crop_lower}_s{gs}.csv"
            if candidate.exists():
                src = candidate
                break
        if src is None:
            self.logger.warning(
                f"crop_t0 static read: no CSV for {country} {crop} at "
                f"growing_seasons={growing_seasons} in {input_dir}"
            )
            return {}

        try:
            df_src = pd.read_csv(src, engine="pyarrow", usecols=["region", column])
        except (ValueError, KeyError) as e:
            # Do NOT just say "re-run geomerge": geoextract/geomerge read
            # countries.txt, never geocif.txt, so a dataset listed only in
            # geocif.txt's eo_model is never extracted and no amount of
            # re-merging will produce its columns. Diagnose that case, since
            # the old wording sent a ~9h extract+merge chain after data that
            # could not appear (usa_admin2 soilgrids, 2026-08-18).
            source = di.STATIC_COLUMN_SOURCE.get(column)
            if source:
                # geocif's own parser includes geocif.txt, so it cannot see what
                # the extract side was configured with — name the trap instead
                # of guessing.
                hint = (
                    f"It comes from the '{source}' dataset. Re-running geomerge "
                    f"alone will NOT add it unless '{source}' is in eo_model in "
                    f"countries.txt — geoextract/geomerge read countries.txt, "
                    f"NOT geocif.txt, so a dataset listed only in geocif.txt is "
                    f"never extracted. Check countries.txt, then re-run "
                    f"geoextract + geomerge."
                )
            else:
                hint = "re-run geomerge to populate."
            self.logger.warning(
                f"crop_t0 static read: {src.name} lacks '{column}' ({e}). {hint}"
            )
            return {}

        df_src = df_src.dropna(subset=[column]).drop_duplicates(subset=["region"])
        _norm = lambda s: str(s).lower().replace(" ", "_").replace("-", "_")
        return {_norm(r): v for r, v in zip(df_src["region"], df_src[column])}

    def _cluster_by_calendar_region(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pool regions by their EXPLICIT crop-calendar zone.

        Reads the region-static ``calendar_region`` column (the AMISCM /
        GlobalCM_Regions zone each admin region belongs to, e.g.
        ``north_region`` / ``central-west_region`` for Brazil) from the raw
        geoprepare crop_t0 CSV and assigns one ``Region_ID`` per distinct zone,
        so each zone trains a SEPARATE pooled model.

        Unlike ``crop_calendar`` (which *infers* groups from CID null-patterns),
        this uses the actual crop-calendar assignment — the correct signal, since
        the whole point is that zones with different planting months should not
        share a pooled model. Regions whose zone can't be resolved fall back to
        their own singleton cluster (never silently merged into a wrong pool).

        Returns:
            DataFrame with columns ["Region", "Region_ID"].
        """
        regions = list(df["Region"].astype(str).unique())
        zone_map = self._read_region_static_from_crop_t0(
            self.country, self.crop, "calendar_region"
        )
        _norm = lambda s: str(s).lower().replace(" ", "_").replace("-", "_")
        region_ids = utils.group_ids_by_key(regions, zone_map, norm=_norm)

        n_zones = len(set(region_ids))
        n_unmatched = sum(1 for r in regions if _norm(r) not in zone_map)
        self.logger.info(
            f"Crop-calendar-region clustering: {len(regions)} regions "
            f"→ {n_zones} zone-pool(s) ({n_unmatched} unmatched region name(s))"
        )
        return pd.DataFrame({"Region": regions, "Region_ID": region_ids})

    def _cluster_by_admin1(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pool regions by their PARENT admin_1 unit (one model per state).

        The admin_2 counterpart to ``crop_calendar_region``: instead of pooling
        every county into one national model (``single``) or splitting to one
        model per county (``individual``), each admin_1 unit trains its own
        pooled model over its counties. Parent lookup is
        ``ml.stats.admin1_lookup`` — the same county->state map used by the
        ``State`` categorical and the ``run_regions`` filter, so all three
        agree by construction. Counties whose parent can't be resolved get
        their own singleton cluster rather than being merged into a wrong pool
        (same rule as the calendar-zone clusterer).

        Returns:
            DataFrame with columns ["Region", "Region_ID"].
        """
        from geocif.ml import stats as ml_stats

        regions = list(df["Region"].astype(str).unique())
        dir_stats = Path(self.parser.get("PATHS", "dir_production_statistics"))
        country_str = self.country.title().replace("_", " ")
        # admin1_lookup keys are normalized with spaces ("iowa adair"); the
        # grouping helper normalizes with underscores — restate the map in the
        # helper's key space so the two never disagree.
        _norm = lambda s: str(s).lower().replace(" ", "_").replace("-", "_")
        parent_map = {
            _norm(k): v
            for k, v in ml_stats.admin1_lookup(
                dir_stats, country_str, parser=self.parser
            ).items()
        }
        if not parent_map:
            self.logger.error(
                f"cluster_strategy=admin_1: no admin_2 -> admin_1 mapping for "
                f"{country_str}; every region becomes its own cluster"
            )
        region_ids = utils.group_ids_by_key(regions, parent_map, norm=_norm)

        n_groups = len(set(region_ids))
        n_unmatched = sum(1 for r in regions if _norm(r) not in parent_map)
        self.logger.info(
            f"admin_1 clustering: {len(regions)} regions → {n_groups} "
            f"state-pool(s) ({n_unmatched} unmatched region name(s))"
        )
        return pd.DataFrame({"Region": regions, "Region_ID": region_ids})

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

        # Normalize selected_features: the CID loop below indexes it as a
        # DataFrame (selected_features["CID"]), but the linear top-3 branch
        # hands over a plain list of CID names. That mismatch raised
        # TypeError("list indices must be integers...") PER CANDIDATE COLUMN
        # (~212k log lines in one run), was swallowed by the per-feature
        # try/except, and silently produced a CID-less model (lags + lat/lon
        # only). Accept list-likes by wrapping them in the expected shape.
        if isinstance(selected_features, (list, tuple, set)) or (
            hasattr(selected_features, "ndim")
            and getattr(selected_features, "ndim", 0) == 1
        ):
            selected_features = pd.DataFrame({"CID": list(selected_features)})

        self.feature_names = []

        if not stages_features or self.is_pre_season:
            # Forecast-only mode (pre-season / in-season init month) — df_train
            # carries unstaged FLDAS/S2S CID columns named like
            # MEAN_FLDAS_*_LEAD{0..5} / MEAN_S2S_*_LEAD{1..6}.  Skip the stage-
            # suffixed loop and use all CID columns directly.  Engineered
            # features below are appended as usual.
            # NOTE: is_pre_season check is load-bearing — _setup_seasons_and_stages
            # sets simulation_stages = [np.array([0])] (a truthy sentinel) for
            # pre-season runs, so `not stages_features` alone misses this branch
            # and the else loop produces feature_names = [] (root-caused via
            # flat-MAPE-across-init-months bug, 2026-05).
            self.feature_names = list(self.get_cid_column_names(self.df_train))
        else:
            method = "latest" if self.model_name.startswith("cumulative_") else "fraction"

            #stages_features = stages.select_stages_for_ml(
            #    stages_features, method=method, n=60
            #)

            cid_cols_in_df = self.get_cid_column_names(self.df_train)
            self.logger.debug(
                f"[create_feature_names] starting loop ({self.country} {self.crop} "
                f"forecast_season={getattr(self, 'forecast_season', '?')}): "
                f"len(stages_features)={len(stages_features)}, "
                f"len(combined_keys)={len(self.combined_keys)}, "
                f"df_train.shape={self.df_train.shape}, "
                f"cid_cols_in_df={len(cid_cols_in_df)}, "
                f"selected_features.shape="
                f"{getattr(selected_features, 'shape', '?')}"
            )

            candidates_seen = 0
            candidates_matched = 0
            sample_attempts = []  # collects up to 5 (_t, tmp_col) pairs for empty-match dump
            for stage in stages_features:
                _stage = "_".join(map(str, stage))
                _tmp = [f"{col}_{_stage}" for col in self.combined_keys]

                for _t in _tmp:
                    candidates_seen += 1
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

                            if len(sample_attempts) < 5:
                                sample_attempts.append((_t, tmp_col))
                            if tmp_col in self.df_train.columns:
                                self.feature_names.append(tmp_col)
                                candidates_matched += 1
                        else:
                            if selected_features["CID"].any():
                                for x in selected_features["CID"].values:
                                    if x not in cid:
                                        continue

                                    dict_fn = stages.get_stage_information_dict(_t, self.method)
                                    tmp_col = f"{dict_fn['CID']} {dict_fn['Stage Name']}"

                                    if len(sample_attempts) < 5:
                                        sample_attempts.append((_t, tmp_col))
                                    if tmp_col in self.df_train.columns:
                                        self.feature_names.append(tmp_col)
                                        candidates_matched += 1
                    except Exception:
                        import traceback as _tb
                        self.logger.error(
                            f"Error creating feature name for {_t}\n"
                            f"{_tb.format_exc()}"
                        )

            # Order-preserving dedup, NOT list(set(...)): set iteration order
            # is PYTHONHASHSEED-randomized, so the same run repeated gave a
            # different column order, which changes gOMP tie-breaking and
            # makes the feature-selection cache key differ across runs.
            self.feature_names = list(dict.fromkeys(self.feature_names))
            self.logger.debug(
                f"[create_feature_names] loop done ({self.country} {self.crop} "
                f"forecast_season={getattr(self, 'forecast_season', '?')}): "
                f"candidates_seen={candidates_seen}, "
                f"candidates_matched={candidates_matched}, "
                f"feature_names={len(self.feature_names)}"
            )

            # Mismatch dump: side-by-side sample of attempted tmp_col vs actual
            # df_train CID columns. Fires only when the loop matched nothing
            # despite df_train having CID-shaped columns — that's the bug
            # we're hunting (producer/consumer naming divergence for multi-
            # stage cumulative spans). Cheap to log, gated to failure case.
            if candidates_matched == 0 and len(cid_cols_in_df) > 0:
                sel_cids_sample = []
                try:
                    if hasattr(selected_features, "columns") and "CID" in selected_features.columns:
                        sel_cids_sample = selected_features["CID"].head(5).tolist()
                except Exception:
                    sel_cids_sample = ["<unreadable>"]
                self.logger.warning(
                    f"[create_feature_names] MISMATCH DUMP ({self.country} {self.crop} "
                    f"forecast_season={getattr(self, 'forecast_season', '?')}): "
                    f"df_train CID cols (first 5)={list(cid_cols_in_df)[:5]} | "
                    f"selected_features['CID'] (first 5)={sel_cids_sample} | "
                    f"attempted (_t -> tmp_col) (first 5)={sample_attempts}"
                )
        
        # Static per-region EO features (bare stage-less columns joined by
        # _add_static_eo_features). The correlation screen only sees staged
        # columns, so include these directly — gated by use_cids ('all', the
        # CID name, or its Type e.g. 'Soil'/'Aridity'); gOMP still decides
        # per fold whether they survive.
        for _name, _meta in di.dict_static_eo.items():
            if _name not in self.df_train.columns:
                continue
            if ("all" in self.use_cids or _name in self.use_cids
                    or _meta[0] in self.use_cids):
                self.feature_names.append(_name)

        if self.median_yield_as_feature:
            self.feature_names.append(f"Median {self.target}")

        if self.use_yield_trend_as_feature and "Yield Trend" in self.df_train.columns:
            self.feature_names.append("Yield Trend")

        if self.use_trend_all_as_feature and "Trend All" in self.df_train.columns:
            self.feature_names.append("Trend All")

        # Always include any "_zreg" sibling columns produced by
        # _compute_region_zscore_features — they're force-included so the
        # encoding-gap fix isn't silently dropped by feature selection.
        if self.region_zscore_cids:
            zreg_cols = [
                c for c in self.df_train.columns if "_zreg" in str(c)
            ]
            self.feature_names.extend(zreg_cols)

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

        # Final dedup: the empty-stages branch above can pick up engineered
        # features (e.g. "Yield Trend") via get_cid_column_names, and then the
        # appends here would duplicate them.  Preserve insertion order.
        seen = set()
        self.feature_names = [c for c in self.feature_names if not (c in seen or seen.add(c))]

        self.selected_features = []

    # ============================================================================
    # FEATURE SELECTION
    # ============================================================================

    def _string_cat_columns(self, X: pd.DataFrame) -> list:
        """cat_features present in X whose values are non-numeric (e.g.
        Region, State). These must be excluded from numeric feature
        selection; they re-enter the model via cat_features at train time.
        Numeric categoricals (Region_ID, Harvest Year) stay in selection,
        preserving pre-State behavior."""
        out = []
        for c in self.cat_features:
            if c not in X.columns:
                continue
            s = X[c]
            vals = pd.Series(
                s.cat.categories if isinstance(s.dtype, pd.CategoricalDtype) else s.unique()
            )
            if pd.to_numeric(vals, errors="coerce").isna().any():
                out.append(c)
        return out

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
            X_for_selection = self.X_train.drop(columns=self._string_cat_columns(self.X_train), errors="ignore")
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
            X_for_selection = self.X_train.drop(columns=self._string_cat_columns(self.X_train), errors="ignore")
            self.selected_features = X_for_selection.columns.tolist()
            self.logger.info(f"Using all {len(self.selected_features)} features")
        else:
            X_for_selection = self.X_train.drop(columns=self._string_cat_columns(self.X_train), errors="ignore")
            stage_id_dbg = str(getattr(self, "stage_info", {}).get("Stage_ID", ""))
            self.logger.debug(
                f"[apply_feature_selector] selecting features for "
                f"{self.country} {self.crop} "
                f"forecast_season={getattr(self, 'forecast_season', '?')} "
                f"region_id={region} stage_id={stage_id_dbg!r}: "
                f"X_for_selection.shape={X_for_selection.shape}, "
                f"feature_names={len(self.feature_names)}, "
                f"df_train.shape={getattr(self.df_train, 'shape', '?')}"
            )
            if X_for_selection.shape[1] == 0:
                raise RuntimeError(
                    f"[apply_feature_selector] X_for_selection has 0 columns — "
                    f"upstream pipeline produced no CID features. "
                    f"country={self.country} crop={self.crop} "
                    f"forecast_season={getattr(self, 'forecast_season', '?')} "
                    f"region_id={region} stage_id={stage_id_dbg!r} "
                    f"X_train.columns={list(self.X_train.columns)[:12]} "
                    f"feature_names[:12]={list(self.feature_names)[:12]} "
                    f"df_train.shape={getattr(self.df_train, 'shape', '?')}"
                )
            # Feature selection is model-independent: catboost, cubist and
            # tabpfn each recompute an identical selection for the same
            # fold/stage/region. Reuse it via a content-addressed disk cache
            # (fold-model tasks are separate processes, so it must be on
            # disk). Key = hash(X, y, method), so any change to the data is a
            # miss rather than a stale hit. Disable with
            # [ML] cache_feature_selection = False.
            fs_cache_dir = None
            if self.parser.getboolean("ML", "cache_feature_selection", fallback=True):
                fs_cache_dir = fs_cache.cache_dir_for(self.dir_ml)

            # A 'multi' run whose sub-selector died still returns a plausible
            # partial union. Caching that would re-serve it to every later
            # model and every re-run (the key is content-addressed, so
            # re-running reproduces it), so such a result is used but never
            # persisted.
            fs_status = {}

            def _compute_selection():
                _, _, feats = fs.select_features(
                    X_for_selection,
                    self.y_train,
                    method=self.feature_selection,
                    dir_output=dir_output,
                    region=region,
                    status=fs_status
                )
                return feats

            self.selected_features, _ = fs_cache.cached_select(
                X_for_selection,
                self.y_train,
                method=self.feature_selection,
                cache_dir=fs_cache_dir,
                compute_fn=_compute_selection,
                log=self.logger,
                should_cache=lambda: not fs_status.get("degraded", False),
                meta={
                    "country": str(self.country),
                    "crop": str(self.crop),
                    "forecast_season": str(getattr(self, "forecast_season", "")),
                    "stage_id": stage_id_dbg,
                    "region_id": str(region),
                },
            )
            # fallback: if selector returned no features, use all
            if not self.selected_features:
                self.logger.warning(
                    f"Feature selection ({self.feature_selection}) returned 0 "
                    f"features for {self.country} {self.crop}; using all features"
                )
                self.selected_features = X_for_selection.columns.tolist()
            self.logger.info(f"Selected features: {self.selected_features}")
        
        # Ensure lat/lon are included if configured. Guarded on actual
        # presence in df_train (same idiom as the static-EO append in
        # create_feature_names): appending a column the frame doesn't carry
        # made _prepare_training_data raise KeyError "['lat','lon'] not in
        # index" for EVERY region — 2555 failed folds and zero stored
        # predictions on the first usa_admin1 pygrf/tabpfn_gsa run.
        if self.include_lat_lon_as_feature:
            for _c in ("lat", "lon"):
                if _c not in self.selected_features and _c in self.df_train.columns:
                    self.selected_features.append(_c)

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
            "ML", "force_include_forecast_cids", fallback=False
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

        # Force-include ETref CIDs (MEAN/MAX/MIN/STD/AUC/SUM_ETREF * stage)
        # for the same reason as FLDAS/S2S above. Motivated by the Somalia
        # drought-year audit (May 2026): residual-vs-CID coupling for
        # STD_ETREF and MIN_ETREF jumps from r ~0.02-0.10 in normal years
        # to r ~0.37-0.43 in drought years (2011, 2017, 2019-21), so the
        # model has the signal in X_train but feature selection drops it
        # because the normal-year correlation is too weak. Force-including
        # protects it. Gated by [ML] force_include_etref (default False —
        # opt in per country).
        keep_etref = (
            self.parser.getboolean("ML", "force_include_etref", fallback=False)
            and ("all" in self.use_cids or "ETREF" in self.use_cids)
        )
        if keep_etref and hasattr(self, "X_train") and self.X_train is not None:
            existing = set(self.selected_features)
            forced_etref = [
                col for col in self.X_train.columns
                if "_ETREF" in str(col)
                and col not in existing
                and col != "Region"
            ]
            if forced_etref:
                self.selected_features = self.selected_features + forced_etref
                self.logger.info(
                    f"Force-included {len(forced_etref)} ETref CIDs "
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
        
        # Baselines (ML_model = False: null / trend / trend_all / median /
        # analog / last_year) predict on the RAW self.target scale — the same
        # scale as y_test and the stored Observed Yield. Only ML models fit on
        # the transformed target (detrended residual, or region anomaly) and
        # therefore need the inverse transform. Applying retrend / re-add to a
        # raw-scale baseline double-counts the level (raw_yield + trend_value
        # ~= 2x yield), which is what inflated null/trend to ~90-107% MAPE.
        # Gate on self.ml_model so baselines stay on their native scale.
        if self.ml_model:
            if self.check_yield_trend:
                y_pred, y_pred_ci = self._retrend_predictions(y_pred, df_region, y_pred_ci)
            elif self.target_mode == "region_anomaly" and self._region_target_means:
                y_pred, y_pred_ci = self._re_add_region_mean_to_predictions(
                    y_pred, df_region, y_pred_ci
                )

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
        elif self.model_name == "null":
            # Per-unit leave-one-out mean. For each held-out forecast year,
            # predict the mean of that spatial unit's yields over the TRAINING
            # years only. df_train already excludes the held-out year via LOOCV
            # (_prepare_train_test_split), so "all of this unit's training rows"
            # IS the leave-one-out set — no past-only window and no recent-N
            # cap (both biased the baseline whenever a unit's yield level
            # drifted over time).
            #
            # Computed strictly WITHIN each spatial unit, never pooled across
            # units: a null that predicts a global mean is trivially weak and
            # would flatter the ML models. df_region is a CLUSTER subset (rows
            # for every admin sharing the cluster's Region_ID), so iterate per
            # admin and give each row ITS OWN unit's mean rather than
            # broadcasting one admin's mean across the whole cluster.
            y_pred = np.full(len(X_test), np.nan, dtype=float)
            for region_name, sub in df_region.groupby("Region", observed=True):
                past = (
                    self.df_train.loc[
                        self.df_train["Region"] == region_name,
                        ["Harvest Year", self.target],
                    ]
                    .dropna()
                )
                mean_obs = (
                    float(past[self.target].mean())
                    if not past.empty else np.nan
                )
                y_pred[sub.index.to_numpy()] = mean_obs
        elif self.model_name in ("trend", "trend_all"):
            # Per-unit Theil–Sen trend fit on the TRAINING years, extrapolated
            # to the forecast season. df_train already drops the held-out year
            # via LOOCV, so the fit uses all of the unit's other years (both
            # pre- and post-forecast). The old past-only / recent-12 window was
            # removed: it anchored the slope on stale years and biased it
            # whenever a unit's yield level drifted.
            #
            # Two guards, because a naive per-unit OLS trend is weak and
            # endpoint-sensitive on short smallholder series:
            #   * Robust slope (Theil–Sen, not OLS) — one anomalous year swings
            #     an OLS slope badly when there are only ~15–25 points.
            #   * Minimum training length. Below it, fall back to the per-unit
            #     mean instead of fitting a slope at all.
            #   Both `trend` and `trend_all` use >= 5 training years.
            #   `trend` was 10 until 0.4.943, which silently degraded it into
            #   `null` on smallholder panels: Kenya admin_2 has ~10 observed
            #   years per region, so after LOOCV drops one only 148/268
            #   regions cleared the bar and just 162/2845 rows differed from
            #   the per-unit mean. `trend_all` was 3, low enough that a
            #   2-3 point "slope" was mostly noise. 5 for both: enough points
            #   for Theil-Sen to be meaningful, low enough to fit short series.
            #
            # df_region is a CLUSTER subset (one row per admin × forecast year);
            # iterate per admin so each row gets ITS OWN per-unit fit instead of
            # broadcasting the first admin's fit across the whole cluster (which
            # produced year-banded predictions in the togo soybean cid_vs_yield
            # diagnostic when cluster_strategy=auto_detect).
            from scipy.stats import theilslopes
            min_years = 5
            y_pred = np.full(len(X_test), np.nan, dtype=float)
            for region_name, sub in df_region.groupby("Region", observed=True):
                past = (
                    self.df_train.loc[
                        self.df_train["Region"] == region_name,
                        ["Harvest Year", self.target],
                    ]
                    .dropna()
                    .sort_values("Harvest Year")
                )
                positions = sub.index.to_numpy()

                # Guard: below the minimum training length, a fitted slope is
                # unreliable — fall back to the per-unit mean.
                if int(past["Harvest Year"].nunique()) < min_years:
                    y_pred[positions] = (
                        float(past[self.target].mean())
                        if not past.empty else np.nan
                    )
                    continue

                slope, intercept, _lo, _hi = theilslopes(
                    past[self.target].astype(float).values,
                    past["Harvest Year"].astype(float).values,
                )
                y_pred[positions] = float(
                    intercept + slope * float(self.forecast_season)
                )
        else:
            raise ValueError(f"Unknown baseline model: {self.model_name}")
        
        return y_pred, None, np.nan

    def _preprocess_test_data(self, X_test: pd.DataFrame, scaler) -> pd.DataFrame:
        """Preprocess test data based on model requirements."""
        if self.dispatch_name in ("linear", "gpr", "george"):
            X_test = X_test.drop(
                columns=[item for item in self.cat_features if item != "Harvest Year"]
            )
            # Same train-median fill as _scale_if_needed: LassoCV/GPR refuse
            # NaN, and test rows must be filled with TRAIN statistics.
            _fill = getattr(self, "_scaled_model_fill", None)
            if _fill is not None:
                X_test = X_test.fillna(_fill)
            return scaler.transform(X_test)

        if self.dispatch_name == "gam":
            # Align to GAMFitter's surviving fit columns (Harvest Year /
            # Region_ID / Region dropped).  No rescaling — pygam splines
            # handle raw numeric ranges. dispatch_name keeps curated_gam
            # routed through the same path as plain gam.
            # When the model was fit with a Region factor term, rebuild the
            # integer-coded column with the SAME fit-time level ordering.
            # Unseen regions code to NaN and fall through to the median
            # fill below — a seen level, degrading gracefully instead of
            # tripping pygam's f() domain check.
            _levels = getattr(self, "_gam_region_levels", None)
            if _levels:
                X_test = GAMFitter.encode_region_factor(X_test, _levels)
            fit_cols = getattr(self, "_gam_fit_cols", None)
            if fit_cols is not None:
                X_aligned = X_test.reindex(columns=fit_cols)
            else:
                X_aligned = X_test.drop(
                    columns=list(GAMFitter._DROP_COLS), errors="ignore",
                )
            # pygam.predict requires no Inf/NaN. Fill with fit-time medians
            # so the imputation matches what the model saw at fit (cached
            # by GAMFitter.fit). Last-resort fallback = 0 for columns that
            # had no training median (e.g. fully-NaN at fit, which
            # _fill_missing_values would also have left at 0).
            medians = getattr(self, "_gam_fit_medians", None)
            if medians is not None:
                X_aligned = X_aligned.fillna(medians)
            X_aligned = X_aligned.replace([np.inf, -np.inf], np.nan).fillna(0)
            # Factor codes must be exact fit-time levels: a median fill over
            # an even level count yields x.5, which is not a level pygam's
            # f() term ever saw. Round-and-clip restores a valid code.
            if _levels and GAMFitter._REGION_COL in X_aligned.columns:
                X_aligned[GAMFitter._REGION_COL] = (
                    X_aligned[GAMFitter._REGION_COL].round().clip(0, len(_levels) - 1)
                )
            return X_aligned

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
        
        # Use self.dispatch_name so curated_<algo> wrappers route through
        # their underlying algo's CI path (e.g. curated_tabpfn uses TabPFN's
        # native quantile path, not the conformal fallback).
        if self.dispatch_name == "ngboost":
            return self._predict_ngboost_with_ci(X_test)
        elif self.dispatch_name == "tabpfn":
            return self._predict_tabpfn_with_quantiles(X_test)
        elif self.dispatch_name == "tabicl":
            return self._predict_tabicl_with_quantiles(X_test)
        elif self.dispatch_name in ["logistic", "catboost"] and self.model_type == "CLASSIFICATION":
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

    def _re_add_region_mean_to_predictions(
        self,
        y_pred: np.ndarray,
        df_region: pd.DataFrame,
        y_pred_ci: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Inverse of the region-anomaly training transform.

        Training subtracted ``region_mean_train_years`` from ``self.target``
        in ``df_train``; ``y_pred`` (and CI bounds) come out in the same
        anomaly space. Add the stored per-region mean back so the DB /
        plots / FDW exports stay in absolute yield units.

        Rows for regions missing from ``self._region_target_means`` are left
        unchanged — those regions were dropped at training time so the test
        slice should already be empty for them, but the lookup defensively
        returns the value as-is rather than NaN-ing the prediction.
        """
        y_pred_out = y_pred.copy()
        y_pred_ci_out = y_pred_ci.copy() if y_pred_ci is not None else None

        admin_col = (
            "Country__Region"
            if getattr(self, "countries_pooled", None)
            and "Country__Region" in df_region.columns
            else "Region"
        )
        means_series = (
            df_region[admin_col].map(self._region_target_means).astype(float)
        )
        # Treat missing region (unseen at train time) as 0 shift so the raw
        # anomaly prediction is preserved rather than NaN-poisoning the row.
        offsets = means_series.fillna(0.0).to_numpy()

        y_pred_out = y_pred_out + offsets
        if y_pred_ci_out is not None:
            # CI shape: (n_samples, 2, 1) — [:, 0, 0] = lower, [:, 1, 0] = upper.
            # Shift both bounds by the same per-row offset to preserve width.
            y_pred_ci_out[:, 0, 0] = y_pred_ci_out[:, 0, 0] + offsets
            y_pred_ci_out[:, 1, 0] = y_pred_ci_out[:, 1, 0] + offsets

        n_shifted = int((offsets != 0).sum())
        if n_shifted:
            self.logger.info(
                f"  region_anomaly: re-added region mean to {n_shifted}/"
                f"{len(offsets)} test predictions"
            )

        return y_pred_out, y_pred_ci_out

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
            # Calendar-order human-readable label emitted alongside the
            # (load-bearing) reverse-cumulative Stage Name. See
            # stages.get_stage_information_dict for details.
            "Stage Window Display": np.full(
                shp,
                self.stage_info.get(
                    "Stage Window Display",
                    self.stage_info["Stage Name"],
                ),
            ),
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
        # dispatch_name, not model_name: curated_/top<N>_/auto_ variants of
        # the scaled models must get the scaler too — the fitter map is
        # keyed by dispatch_name and would otherwise fit on raw magnitudes.
        if self.dispatch_name in ("linear", "gpr", "george"):
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

        # For ML models only, apply per-region [min_year, max_year] restriction
        # (config: [ML] ml_year_range_per_region). Baseline models (null, trend,
        # trend_all) skip this — they read self.df_train unfiltered inside
        # predict() so they retain full historical context for their statistics.
        if self.ml_model and self.ml_year_range_per_region:
            df_region_train = self._apply_ml_year_range_filter(df_region_train)

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
        if self.ml_model:
            self._select_features(region_id, dir_output)
        else:
            # Non-ML baselines (null, trend, median, analog) have predetermined
            # feature lists set in _create_feature_names_for_region. Feature
            # selection (gOMP etc.) is meaningless for them — skip to avoid
            # dispatching gOMP on an empty X_for_selection.
            self.selected_features = list(self.feature_names)
        
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
        # dispatch_name, not model_name: last<N>m_linear / curated_linear must
        # take the same top-3-CID path as plain linear. Every other
        # linear-specific site (scaler, fitter map, NaN fill, test preprocess)
        # already keys on dispatch_name.
        #
        # The top-3 dict comes from _generate_correlation_plots, which returns
        # ({}, {}) whenever correlation_plots = False — so this branch used to
        # crash with KeyError on a PLOTTING flag. Fall back to the standard
        # selection path instead, loudly.
        if self.dispatch_name == "linear" and region_id in dict_best_cid                 and len(dict_best_cid[region_id]):
            selected = dict_best_cid[region_id][0:3].tolist()
            self.create_feature_names(stages, selected)
        elif self.dispatch_name == "linear":
            self.logger.warning(
                f"  linear top-3-CID selection needs correlation_plots = True "
                f"(dict_best_cid empty for region {region_id}); falling back "
                f"to standard feature selection"
            )
            selected = dict_selected_features.get(region_id)
            self.create_feature_names(stages, selected)
        elif self.model_name.startswith("cumulative_"):
            self.create_feature_names(stages, {})
        elif self.ml_model:
            selected = dict_selected_features.get(region_id)
            if selected is not None and not selected.empty:
                self.create_feature_names(stages, selected)
            else:
                # No correlation-based selection — use all CID features.
                # NOTE: this branch bypasses create_feature_names, so the
                # engineered-feature appends at the end of it (lat/lon, lag
                # yield, medians, _zreg, nbr_) never run. lat/lon must still
                # be added here: apply_feature_selector force-includes them
                # in selected_features, and without them in feature_names
                # they never reach df_region via _get_common_columns — which
                # is exactly how the first usa_admin1 pygrf/tabpfn_gsa run
                # lost all 2555 folds to KeyError. Configs with
                # include_lat_lon_as_feature = False are unaffected.
                self.feature_names = self.get_cid_column_names(self.df_train)
                if self.include_lat_lon_as_feature:
                    self.feature_names.extend(
                        c for c in ("lat", "lon") if c in self.df_train.columns
                    )
                self.logger.warning(
                    f"  [{self.country} {self.crop} {self.model_name} "
                    f"forecast_season={getattr(self, 'forecast_season', '?')} "
                    f"region_id={region_id}] correlation-selection empty; "
                    f"falling back to all CID columns: "
                    f"df_train.shape={self.df_train.shape}, "
                    f"feature_names={len(self.feature_names)}"
                )
                self._record_fallback(
                    "correlation_selection_empty",
                    region_id=region_id,
                    df_train_rows=self.df_train.shape[0],
                    df_train_cols=self.df_train.shape[1],
                    feature_names_fallback_count=len(self.feature_names),
                )
        elif self.model_name == "median":
            self.feature_names = [f"Median {self.target}"]
            self.last_year_yield_as_feature = False
            self.analogous_year_yield_as_feature = False
        elif self.model_name in ("null", "trend", "trend_all"):
            self.feature_names = []
            self.last_year_yield_as_feature = False
            self.median_yield_as_feature = False
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

        self._warn_if_coords_degenerate()

    def _warn_if_coords_degenerate(self):
        """Loudly flag unusable region centroids for the coordinate-driven
        models (pygrf / tabpfn_gsa).

        Both degrade SILENTLY rather than crash when centroids are absent or
        constant: PyGRFRegressor falls back to the train-mean location and
        TabPFNGSARegressor mean-fills, after which every row shares one
        coordinate — PyGRF's local forests become clones of each other and
        GSA's grid collapses to a single cell (i.e. plain TabPFN wearing a
        spatial-model name). The usual cause is a boundary-file join miss
        (``_add_lat_lon_to_data`` merges on ``"<Country> <Region>"``
        lowercased, so an underscored Country or renamed admin never
        matches) and it is invisible in the metrics.
        """
        if self.dispatch_name not in ("pygrf", "tabpfn_gsa"):
            return
        # Once per (country, crop, model) — the check is per-region-per-fold
        # but the geodata join is not, so repeating it would spam the log.
        _key = (self.country, self.crop, self.model_name)
        if getattr(self, "_coord_check_done", None) == _key:
            return
        self._coord_check_done = _key
        missing = [c for c in ("lat", "lon") if c not in self.df_train.columns]
        if missing:
            self.logger.warning(
                f"  [{self.country} {self.crop} {self.model_name}] "
                f"region centroids {missing} absent from df_train — the "
                f"spatial component is inert (predictions come from the "
                f"non-spatial part only). Check the boundary_file join."
            )
            return
        coords = self.df_train[["lat", "lon"]]
        n_finite = coords.notna().all(axis=1).sum()
        n_unique = coords.dropna().drop_duplicates().shape[0]
        n_regions = self.df_train["Region"].nunique() if "Region" in self.df_train else 0
        if n_finite == 0:
            self.logger.warning(
                f"  [{self.country} {self.crop} {self.model_name}] region "
                f"centroids are ALL NaN — boundary_file join produced no "
                f"matches, so the spatial component is inert. Check that "
                f"Country/Region names match the shapefile's "
                f"ADM0_NAME/ADM1_NAME."
            )
        elif n_unique <= 1 and n_regions > 1:
            self.logger.warning(
                f"  [{self.country} {self.crop} {self.model_name}] all "
                f"{n_regions} regions share ONE centroid — the spatial "
                f"component is degenerate (PyGRF local models collapse / "
                f"GSA grid becomes 1 cell)."
            )
        else:
            self.logger.info(
                f"  [{self.country} {self.crop} {self.model_name}] centroids "
                f"OK: {n_unique} unique location(s) over {n_regions} region(s), "
                f"{n_finite}/{len(coords)} rows with finite coords"
            )

    def _apply_ml_year_range_filter(self, df_region_train: pd.DataFrame) -> pd.DataFrame:
        """Drop training rows outside [min_year, max_year] per region.

        Applied ONLY to df_region_train used by ML models (catboost, tabpfn,
        cubist). Baseline models (null, trend, trend_all) skip this because
        they read ``self.df_train`` directly inside ``predict()`` and need the
        full history to compute means / theil-sen slopes.

        Config: ``[ML] ml_year_range_per_region = {"Region1": [2019, 2100], ...}``
        Empty dict / missing key → no filter (returns df unchanged).
        """
        if not self.ml_year_range_per_region:
            return df_region_train
        if "Region" not in df_region_train.columns or "Harvest Year" not in df_region_train.columns:
            return df_region_train

        df = df_region_train
        drop_mask_total = pd.Series(False, index=df.index)
        summary = []
        for region, yr_range in self.ml_year_range_per_region.items():
            try:
                y_min, y_max = int(yr_range[0]), int(yr_range[1])
            except (TypeError, ValueError, IndexError):
                continue
            years = df["Harvest Year"].astype("Int64")
            drop_mask = (
                (df["Region"] == region)
                & ((years < y_min) | (years > y_max))
            )
            n_drop = int(drop_mask.sum())
            if n_drop > 0:
                drop_mask_total = drop_mask_total | drop_mask
                summary.append(f"{region}: -{n_drop} rows (kept [{y_min},{y_max}])")
        if not drop_mask_total.any():
            return df

        # Dedup log across regions/folds within a run.
        cache_key = (
            self.country,
            self.crop,
            frozenset(summary),
        )
        if getattr(self, "_last_year_range_drop", None) != cache_key:
            self.logger.info(
                f"ml_year_range_per_region: {'; '.join(summary)}"
            )
            self._last_year_range_drop = cache_key
        return df[~drop_mask_total].copy()

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
        # cat_features that are NOT already in fixed_columns and ARE present
        # on df_train survive here. fixed_columns already carries Region /
        # Harvest Year / Country / ... — adding them again would produce
        # duplicate columns in _extract_region_subset (df[fixed + common])
        # and break downstream groupby('Region') with "not 1-dimensional".
        # Purpose: keep project-static categorical features (e.g.
        # `irrigation_status` from _add_project_static_features) alive
        # through the per-region column-whitelist so predict()'s slicing on
        # selected_features + cat_features doesn't KeyError.
        fixed_set = set(getattr(self, "fixed_columns", []))
        cat_cols_present = [
            c for c in getattr(self, "cat_features", [])
            if c in self.df_train.columns and c not in fixed_set
        ]
        common_columns = (
            [self.target, self.target_class]
            + self.statistics_columns
            + self.feature_names
            + cat_cols_present
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

        if self.dispatch_name in ["gam", "linear", "gpr"]:
            self._fill_missing_values()

        self.y_train = df_region_train[self.target_column]

        # Region-anomaly target transform — subtract per-region training-mean
        # ONLY from y_train so the model fits on yield deviations from each
        # region's baseline. df_region_train[self.target_column] is left
        # absolute, so last_observed_map and any other downstream readers
        # keep seeing physical units. Re-added at prediction time via
        # _re_add_region_mean_to_predictions.
        if (
            self.target_mode == "region_anomaly"
            and not self.check_yield_trend
            and getattr(self, "_region_target_means", None)
            and self.target_column == self.target
        ):
            admin_col = (
                "Country__Region"
                if getattr(self, "countries_pooled", None)
                and "Country__Region" in df_region_train.columns
                else "Region"
            )
            means = (
                df_region_train[admin_col]
                .map(self._region_target_means)
                .astype(float)
                .fillna(0.0)
            )
            # Keep Series type so downstream .loc / .iloc on y_train still works
            self.y_train = (self.y_train.astype(float) - means.values)

        # Compute last available observed year and yield PER REGION.
        #
        # Three guards keep this loop safe when df_region_train carries a
        # Categorical "Region" column with some levels having no valid
        # target rows — the failure mode that crashed the Wolayita maize
        # run with "attempt to get argmax of an empty sequence":
        #   1. observed=True drops empty Categorical levels at the
        #      groupby layer (the root cause — _add_region_clusters at
        #      geocif.py:2498 sets Region as Categorical, and the
        #      default observed=False keeps empty levels as 0-row groups).
        #   2. years.dropna() + years.empty guards the second-order case
        #      where a group has rows but Harvest Year is entirely NaN.
        #   3. idxmax() runs on the pre-dropna'd Series so it's never
        #      called on an empty sequence.
        # Regions skipped here don't appear in last_observed_map; all
        # downstream readers use .get(region) so missing keys degrade
        # gracefully.
        df_valid = df_region_train.dropna(subset=[self.target_column])
        self.last_observed_map = {}  # {region_name: (year, yield)}
        if df_valid.empty:
            return
        for region, grp in df_valid.groupby("Region", observed=True):
            years = grp["Harvest Year"].dropna()
            if years.empty:
                continue
            last_row = grp.loc[years.idxmax()]
            self.last_observed_map[region] = (
                int(last_row["Harvest Year"]),
                float(last_row[self.target_column]),
            )

    # Add debug logging in _clean_training_features
    def _clean_training_features(self, X_train: pd.DataFrame) -> pd.DataFrame:
        """Replace ±inf with NaN, drop columns that are ENTIRELY NaN, preserve lag/neighbor cols.

        Inf can leak in from feature paths that bypass the per-feature
        ``np.isfinite`` guard in ``cid/indices.py`` (REV/MAR division on
        repeated forecasts, neighbor-correlation features on constant series,
        etc.).  Sanitizing at this boundary catches all sources at once and
        lets the existing NaN-handling decide whether to drop or impute.

        Only fully all-NaN columns are dropped here; partial-NaN columns
        survive and are handled downstream:
        - gam/linear/gpr → ``_fill_missing_values`` median/mode imputes.
        - tabpfn/catboost → handle NaN natively.
        - feature_selection (gOMP etc.) → drops cols with > threshold_nan
          proportion of NaN and median-fills the rest.
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

        non_preserve_before = [c for c in X_train.columns if c not in preserve_cols]

        X_train = (
            X_train
            .drop(columns=preserve_cols)
            .dropna(axis=1, how="all")
            .join(X_train[preserve_cols])
        )

        non_preserve_after = [c for c in X_train.columns if c not in preserve_cols]
        dropped = sorted(set(non_preserve_before) - set(non_preserve_after))
        if dropped:
            self.logger.warning(
                f"[_clean_training_features] dropna(all) removed {len(dropped)}/"
                f"{len(non_preserve_before)} all-NaN non-preserve cols "
                f"(forecast_season={getattr(self, 'forecast_season', '?')}); "
                f"first 10: {dropped[:10]}"
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
        """Scale features if scaler is provided.

        Median-imputes BEFORE fitting the scaler. The per-split
        ``_fill_missing_values`` only mutates ``self.X_train``, while this
        matrix is re-sliced fresh from ``df_region`` — so its fill never
        reaches the fit. Lag features (``t -1/-2/-3 Yield``) are NaN for the
        earliest training years by construction, StandardScaler passes NaN
        through, and LassoCV refuses it — which killed all 44 folds of the
        first ``last9m_linear`` run with "Input X contains NaN". The train
        medians are stored on the Geocif object so predict-time test rows are
        filled with TRAIN statistics, never their own.
        """
        if not scaler:
            return X_train

        X_train_nocat = X_train.drop(
            columns=[item for item in self.obj.cat_features 
                    if item != "Harvest Year"]
        )
        self.obj._scaled_model_fill = X_train_nocat.median(numeric_only=True)
        X_train_nocat = X_train_nocat.fillna(self.obj._scaled_model_fill)
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
            cubist_params=getattr(self.obj, "cubist_params", None),
            bass_params=getattr(self.obj, "bass_params", None),
            george_params=getattr(self.obj, "george_params", None),
            pygrf_params=getattr(self.obj, "pygrf_params", None),
            gsa_params=getattr(self.obj, "gsa_params", None),
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
        # Calibrate/conformalize with training data. Cubist was fit on a
        # zero-variance-pruned + NaN-filled column set (CubistFitter), and its
        # sklearn feature-name check rejects the raw full-width frame. The
        # point path aligns via _preprocess_test_data; the conformal
        # calibrate must do the same or crepes' internal learner.predict trips
        # "feature names should match those passed during fit". (Cubist has no
        # scaler, so scaler=None routes straight to the cubist-align branch.)
        if X_train is not None:
            cal_X = X_train
            if self.obj.model_name == "cubist":
                cal_X = self.obj._preprocess_test_data(X_train, None)
            if hasattr(self.obj.model, 'calibrate'):
                self.obj.model.calibrate(cal_X, self.obj.y_train.values)
            elif hasattr(self.obj.model, 'conformalize'):
                self.obj.model.conformalize(cal_X, self.obj.y_train)
    
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
            # catboost_quantile: same CatBoostFitter path — the loss switch
            # (Quantile:alpha=0.25) lives in trainers.get_model(), and the
            # Pool wiring/predict path is identical to plain catboost.
            "catboost_quantile": CatBoostFitter(self.obj),
            "tabpfn": TabPFNFitter(self.obj),
            # tabpfn_phe is a Post-Hoc Ensembling wrapper around TabPFN
            # (AutoTabPFNRegressor from tabpfn_extensions) — same sklearn
            # .fit(X, y) API, so it can safely route through TabPFNFitter
            # without a dedicated fitter class. NOT named "auto_tabpfn"
            # because the wrapper-prefix regex in trainers.py strips
            # "auto_" and would route that name to the plain tabpfn branch.
            "tabpfn_phe": TabPFNFitter(self.obj),
            # tabpfn_gsa wraps GSAModel behind a plain .fit(X, y) — the
            # TabPFNFitter path (DataFrame in, y ravel) is exactly right.
            "tabpfn_gsa": TabPFNFitter(self.obj),
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
            "gpr": GPRFitter(self.obj),
            # george routes through GPRFitter: same scaled-numpy fit path as
            # sklearn's GaussianProcessRegressor (StandardScaler upstream).
            "george": GPRFitter(self.obj),
        }
        
        if self.obj.model_name.startswith("cumulative_"):
            return CumulativeFitter(self.obj)

        if self.obj.dispatch_name == "desreg":
            return DesregFitter(self.obj)

        # dispatch_name strips the curated_ prefix so curated_<algo>
        # routes to <algo>'s specific fitter (GAMFitter's term-construction,
        # CatBoostFitter's Pool wiring, etc.). Without this the curated
        # variants silently fall back to DefaultFitter and train degenerate
        # models (LinearGAM() with no spline terms, etc.).
        return fitters.get(self.obj.dispatch_name, DefaultFitter(self.obj))


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


class GPRFitter(LinearFitter):
    """Gaussian Process Regressor fitter — same as linear (scaled, no cats)."""
    pass


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
    # Region CAN come back in as a factor term via gam_region_factor —
    # unlike Harvest Year, every Region level seen at forecast time also
    # exists in training under pooled strategies, so f() is safe there.
    _DROP_COLS = ("Harvest Year", "Region_ID", "Region")

    # Name of the synthetic integer-coded column the factor term uses.
    _REGION_COL = "Region_factor"

    @staticmethod
    def encode_region_factor(X: pd.DataFrame, levels) -> pd.DataFrame:
        """Return a copy of ``X`` with ``Region_factor`` = the integer code
        of ``Region`` under the fit-time ``levels`` ordering. Regions not in
        ``levels`` map to NaN — downstream median-fill turns them into a
        seen level rather than crashing pygam's f() domain check."""
        codes = {r: float(i) for i, r in enumerate(levels)}
        out = X.copy()
        out[GAMFitter._REGION_COL] = (
            out["Region"].astype(str).map(codes) if "Region" in out.columns else np.nan
        )
        return out

    def fit(self, X_train: pd.DataFrame, X_train_scaled, df_region: pd.DataFrame):
        from pygam import LinearGAM, LogisticGAM, s, f

        # Fit-time layout must match what _preprocess_test_data produces.
        X_fit = X_train.drop(columns=list(self._DROP_COLS), errors="ignore")

        # Optional per-region intercepts: encode Region to integer codes and
        # add a penalized factor term. Skipped when Region is absent or
        # single-level (per-region training), where it carries no signal.
        self.obj._gam_region_levels = None
        if getattr(self.obj, "gam_region_factor", False) and "Region" in X_train.columns:
            levels = sorted(pd.Series(X_train["Region"]).astype(str).unique())
            if len(levels) >= 2:
                self.obj._gam_region_levels = levels
                X_fit = self.encode_region_factor(
                    X_fit.assign(Region=X_train["Region"]), levels
                ).drop(columns=["Region"])

        # Adaptive spline count.  Cap low so we don't overfit small regions
        # (a country/crop often has < 100 training rows); splines are cubic
        # (spline_order=3) which is the field-standard choice for yield
        # response curves.
        n_splines = max(4, min(10, len(X_fit) // 20))

        terms = None
        for i, col in enumerate(X_fit.columns):
            term = (
                f(i) if col == self._REGION_COL
                else s(i, n_splines=n_splines, spline_order=3)
            )
            terms = term if terms is None else terms + term

        gam_cls = LogisticGAM if self.obj.model_type == "CLASSIFICATION" else LinearGAM
        self.obj.model = gam_cls(terms=terms)
        self.obj._gam_fit_cols = list(X_fit.columns)
        # Cache fit-time medians so _align_test_features can fill predict-time
        # NaN with the same imputation pygam saw at fit (otherwise reindex on
        # a test set with missing CIDs produces NaN columns and pygam.predict
        # raises "X data must not contain Inf nor NaN").
        self.obj._gam_fit_medians = X_fit.median(numeric_only=True)

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
            import traceback as _tb
            self.obj.logger.error(
                f"Error fitting {self.obj.model_name} for "
                f"{self.obj.country} {self.obj.crop}: {e}\n"
                f"{_tb.format_exc()}"
            )
            raise