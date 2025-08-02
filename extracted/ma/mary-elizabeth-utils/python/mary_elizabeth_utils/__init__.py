# Config
# Version
from ._version import VERSION
from .analysis.cohort import (
    create_cohorts,
    create_exposed_group,
    create_unexposed_group,
    identify_severe_chronic_cases,
    match_cohorts,
)

# Analysis
from .analysis.statistics import (
    generate_summary_statistics,
    plot_categorical_comparisons,
    plot_numeric_comparisons,
)
from .config.config import Config, load_config
from .data.loading import load_icd10_codes, load_register_data
from .data.processing import DataProcessor

# Data
from .data.table_creation import (
    create_child_table,
    create_diagnosis_table,
    create_education_table,
    create_employment_table,
    create_healthcare_table,
    create_person_child_table,
    create_person_family_table,
    create_person_table,
    create_person_year_income_table,
    create_socioeconomic_status_table,
    create_time_table,
    create_treatment_period_table,
)
from .data.transformation import impute_missing_values, transform_data
from .data.validation import check_logical_consistency, check_missing_values, check_outliers

# Main entry point
from .main import main as run_analysis
from .utils.caching import cache_result

# Utils
from .utils.logger import setup_colored_logger
from .utils.pipeline import Pipeline
from .utils.reports import (
    generate_demographic_report,
    generate_economic_report,
    generate_health_report,
    generate_integrated_analysis_report,
)

__version__ = VERSION

__all__ = [
    # Config
    "Config",
    "load_config",
    # Data
    "load_icd10_codes",
    "load_register_data",
    "create_person_table",
    "create_child_table",
    "create_diagnosis_table",
    "create_employment_table",
    "create_education_table",
    "create_healthcare_table",
    "create_time_table",
    "create_socioeconomic_status_table",
    "create_treatment_period_table",
    "create_person_child_table",
    "create_person_family_table",
    "create_person_year_income_table",
    "DataProcessor",
    "transform_data",
    "impute_missing_values",
    "check_logical_consistency",
    "check_missing_values",
    "check_outliers",
    # Analysis
    "generate_summary_statistics",
    "plot_categorical_comparisons",
    "plot_numeric_comparisons",
    "create_cohorts",
    "identify_severe_chronic_cases",
    "create_exposed_group",
    "create_unexposed_group",
    "match_cohorts",
    # Utils
    "setup_colored_logger",
    "cache_result",
    "Pipeline",
    "generate_health_report",
    "generate_economic_report",
    "generate_demographic_report",
    "generate_integrated_analysis_report",
    # Main entry point
    "run_analysis",
    # Version
    "__version__",
]
