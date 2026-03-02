import json
import logging
import math
from decimal import Decimal
from typing import Optional, Any

import numpy as np
import pandas as pd
from teradataml import DataFrame  # noqa
from teradataml.analytics.valib import *  # noqa # NOSONAR(python:S2208)
from teradatasql import OperationalError

from tmo.stats import store

logger = logging.getLogger(__name__)

value_for_nan = 0
CHARSET_INVALID_PARAMETER = "'charset' is an invalid parameter"


class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating) or isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(_NpEncoder, self).default(obj)


def _compute_continuous_edges(
    variables: list[str], statistics: pd.DataFrame, dtypes: dict, bins=10
) -> list[float]:
    edges = []

    # Should return what is in the feature catalog, for now calculate linspace boundaries based on min/max
    ranges = statistics.drop(
        statistics.columns.difference(["xcol", "xmin", "xmax"]), axis=1
    )
    ranges = ranges.set_index("xcol")
    ranges.index = ranges.index.map(str.lower)
    ranges = ranges.to_dict(orient="index")

    for var in variables:
        x_min, x_max = ranges[var]["xmin"], ranges[var]["xmax"]

        # if integer type and range is less than the number of bins, only use 'range' bins
        if x_max - x_min < bins and dtypes[var].startswith("int"):
            edges.append(
                np.linspace(x_min, x_max, int(x_max) - int(x_min) + 1).tolist()
            )
        elif dtypes[var].startswith("decimal") or dtypes[var].startswith("float"):
            # (min / max must be rounded up / down accordingly so easier to just use the vals from stats)
            vals = np.linspace(x_min, x_max, bins + 1).tolist()

            # Rounding all edges to the best Teradata-compatible precision
            vals = list(map(_round_to_td_float, vals))

            dedup = []
            [dedup.append(x) for x in vals if x not in dedup]

            edges.append(dedup)
        else:  # Here we compute for regular int variables
            vals = np.linspace(x_min, x_max, bins + 1).tolist()
            for i in range(1, len(vals)):
                vals[i] = round(vals[i], 1)
            edges.append(vals)

    return edges


def _convert_all_edges_to_val_str(all_edges):
    # boundaries for multiple columns follows the following format..
    # ["{10, 0, 200000}", "{5, 0, 100}"]
    boundaries = []
    for edges in all_edges:
        edges_str = ",".join(str(edge) for edge in edges)
        boundaries.append("{{ {} }}".format(edges_str))

    return boundaries


def _fill_missing_bins(
    bin_edges: list[float], bin_values: list[float], reference_edges: list[float]
) -> list[float]:
    """
    Compare the `bin_edges` returned by VAL to `reference_edges` and fill in any missing bins with `0`.
    This is required as VAL doesn't return empty bins and so if we want to ensure we always have all the bins
    represented in the `bin_values` (which we do or else indices vs reference edges mean nothing), then we must do this.

    """
    new_bin_values = list(bin_values)

    epsilon = 1e-08
    for i, edge in enumerate(reference_edges):
        is_present = False
        for curr_edge in bin_edges:
            if abs(float(curr_edge) - float(edge)) < epsilon:
                is_present = True

        if not is_present:
            new_bin_values.insert(i, 0.0)

    return new_bin_values


def _extract_null_count(var_freq: pd.DataFrame) -> tuple[pd.DataFrame, float | None]:
    """
    Extract null count from frequency DataFrame and remove null rows.

    Parameters:
        var_freq: DataFrame containing frequency data for a variable

    Returns:
        tuple: (cleaned_var_freq, null_count) - DataFrame without nulls and null count
    """
    null_count = None

    if var_freq["xval"].isnull().values.any():
        null_rows = var_freq[var_freq["xval"].isnull()]
        null_count = null_rows.xcnt.tolist()[0]
        var_freq = var_freq[var_freq["xval"].notnull()]

    return var_freq, null_count


def _create_frequencies_dict(var_freq: pd.DataFrame) -> dict:
    """
    Create a dictionary mapping category values to their frequencies.

    Parameters:
        var_freq: DataFrame containing frequency data (without nulls)

    Returns:
        dict: mapping of category -> frequency count
    """
    if var_freq.empty:
        return {}

    return var_freq[["xval", "xcnt"]].set_index("xval").T.to_dict(orient="records")[0]


def _build_monitored_frequencies(
    frequencies_dict: dict,
    reference_categories: list,
    variable_name: str,
) -> tuple[dict, dict | None]:
    """
    Build monitored and unmonitored frequency dictionaries based on reference categories.

    Parameters:
        frequencies_dict: dict of all observed frequencies
        reference_categories: list of expected categories
        variable_name: name of the variable (for logging)

    Returns:
        tuple: (monitored_frequencies, unmonitored_frequencies)
    """
    # Build monitored frequencies (based on reference categories)
    monitored = {
        cat: frequencies_dict.get(cat, 0) if cat in reference_categories else 0
        for cat in reference_categories
    }

    # Identify new categories not in reference
    unmonitored = None
    for category in frequencies_dict.keys():
        if category not in reference_categories:
            logger.warning(
                f"Categorical feature {variable_name} has a new category {category} "
                "that's not listed in reference categories"
            )
            if unmonitored is None:
                unmonitored = {}
            unmonitored[category] = frequencies_dict.get(category)

    return monitored, unmonitored


def _process_categorical_var(
    frequencies: pd.DataFrame,
    group_label: str,
    variable_name: str,
    feature_importance: float,
    reference_categories: Optional[list],
) -> dict:
    """
    Process categorical variable statistics and build data structure.

    Creates a structure containing:
    - type: "categorical"
    - group: monitoring group name
    - importance: feature importance score
    - categories: reference categories list
    - statistics: nulls, frequency, and unmonitored_frequency

    Parameters:
        frequencies: DataFrame containing frequency data from VAL
        group_label: monitoring group name
        variable_name: name of the categorical variable
        feature_importance: importance score for this feature
        reference_categories: list of expected categories (None if unmonitored)

    Returns:
        dict: structured categorical variable statistics
    """
    # Initialize base structure
    data_struct: dict[str, str | float | dict[Any, Any] | list] = {
        "type": "categorical",
        "group": group_label,
        "statistics": {},
    }

    if feature_importance:
        data_struct["importance"] = feature_importance

    # Filter to this variable's frequencies
    var_freq = frequencies[frequencies.xcol == variable_name]

    # Extract and handle null values
    var_freq, null_count = _extract_null_count(var_freq)
    if null_count is not None:
        data_struct["statistics"]["nulls"] = null_count

    # Handle case where all values are null
    if var_freq.empty:
        logger.warning(
            f"Categorical feature {variable_name} has only NULL values, "
            "not computing a frequency"
        )
        return data_struct

    # Create frequency dictionary from DataFrame
    frequencies_dict = _create_frequencies_dict(var_freq)

    # Handle unmonitored features (no reference categories)
    if reference_categories is None:
        data_struct["statistics"]["unmonitored_frequency"] = frequencies_dict
        return data_struct

    # Record reference categories for monitored features
    data_struct["categories"] = reference_categories

    # Build monitored and unmonitored frequencies
    monitored, unmonitored = _build_monitored_frequencies(
        frequencies_dict, reference_categories, variable_name
    )

    data_struct["statistics"]["frequency"] = monitored

    if unmonitored is not None:
        data_struct["statistics"]["unmonitored_frequency"] = unmonitored

    return data_struct


def _process_continuous_var(
    histogram: pd.DataFrame,
    stats: pd.DataFrame,
    group_label: str,
    variable_name: str,
    feature_importance: float,
    reference_edges: Optional[list[float]],
) -> dict:
    """
    Adds the following struct
    {
        "type": "continuous",
        "group": "<group-name>",
        "importance": "<feature-importance>",
        "statistics": {
            "nulls": <missing-values>,
            "cnt": 614.0,
            "min": 21.0,
            "max": 81.0,
            ...
            "histogram": {
              "edges": [21.0,27.0,33.0,39.0,45.0,51.0,57.0,63.0,69.0,75.0,81.0],
              "values": [248.0,122.0,77.0,62.0,45.0,23.0,20.0,13.0,3.0,1.0]
            }
        }
    }
    """

    data_struct: dict[str, str | float | dict[Any, Any] | list] = {
        "type": "continuous",
        "group": group_label,
        "statistics": {},
    }

    if feature_importance:
        data_struct["importance"] = feature_importance

    def _strip_key_x(d: dict):
        return {k[1:]: v for k, v in d.items()}

    stats_values = (
        stats[stats.xcol == variable_name]
        .drop(["xdb", "xtbl", "xcol"], axis=1)
        .to_dict(orient="records")[0]
    )
    data_struct["statistics"].update(_strip_key_x(stats_values))

    if histogram.empty:
        # No histogram available - we stop here, not reporting histogram
        return data_struct

    var_hist = histogram[histogram.xcol == variable_name].sort_values(by=["xbin"])

    # if first row is nan then it is the null values in the dataset. remove from histogram
    if var_hist["xbin"].isnull().values.any():
        n = var_hist[var_hist["xbin"].isnull()]
        data_struct["statistics"]["nulls"] = n.xcnt.tolist()[0]

        var_hist = var_hist[var_hist["xbin"].notnull()]

    if var_hist.empty:
        # We should probably generate all-zero histogram here?
        logger.warning(
            f"Continuous feature {variable_name} has only NULL values, not computing a"
            " histogram"
        )
        return data_struct

    bin_edges = [var_hist.xbeg.tolist()[0]] + var_hist.xend.tolist()
    bin_values = var_hist.xcnt.tolist()

    # (issue #123) VAL docs originally stated that:
    # VAL histograms will add values lower than the first bin to the first bin, but values greater than the
    # largest bin are added to a new bin. Therefore, we did the same on both sides. However, it turns out this doc is
    # incorrect.

    is_right_outlier_bin = math.isnan(bin_edges[-1])
    is_left_outlier_bin = math.isnan(bin_edges[0])
    if is_right_outlier_bin:
        bin_edges = bin_edges[:-1]
    if is_left_outlier_bin:
        bin_edges = bin_edges[1:]

    # Add missing bin_values based on the bin_edges vs reference_edges.
    # VAL doesn't return empty bins
    if len(bin_edges) < len(reference_edges):
        bin_values = _fill_missing_bins(
            bin_edges=bin_edges, bin_values=bin_values, reference_edges=reference_edges
        )

    right_outliers = 0
    left_outliers = 0
    if is_right_outlier_bin:
        right_outliers = int(bin_values[-1])
        logger.warning(
            f"Continuous feature {variable_name} has values larger than the rightmost"
            f" bin, identified {right_outliers} values"
        )
        bin_values[-2] += bin_values[
            -1
        ]  # Probably should consider removing as some point, when outliers are properly reported and visible to the user
        bin_values = bin_values[:-1]
    if is_left_outlier_bin:
        left_outliers = int(bin_values[0])
        logger.warning(
            f"Continuous feature {variable_name} has values smaller than the leftmost"
            f" bin, identified {left_outliers} values"
        )
        bin_values[1] += bin_values[
            0
        ]  # Probably should consider removing as some point, when outliers are properly reported and visible to the user
        bin_values = bin_values[1:]

    data_struct["statistics"]["histogram"] = {
        "edges": reference_edges,
        "values": bin_values,
    }

    if is_right_outlier_bin:
        data_struct["statistics"]["histogram"]["right_outliers"] = right_outliers
    if is_left_outlier_bin:
        data_struct["statistics"]["histogram"]["left_outliers"] = left_outliers

    return data_struct


def _validate_dataframe_type(df, df_name: str):
    """
    Validate that the provided dataframe is a teradataml DataFrame.

    Parameters:
        df: dataframe to validate
        df_name (str): name of the dataframe for error message

    Raises:
        TypeError: if df is not a teradataml DataFrame
    """
    if not isinstance(df, DataFrame):
        raise TypeError(f"We only support teradataml DataFrame for {df_name}")


def _ensure_backward_compatibility(data_stats: dict) -> dict:
    """
    Ensure backward compatibility by renaming 'predictors' to 'targets' if present.

    Parameters:
        data_stats (dict): data statistics dictionary

    Returns:
        dict: updated data statistics
    """
    # Ensure backward compatible (when we had targets incorrectly named as predictors)
    if "predictors" in data_stats:
        data_stats["targets"] = data_stats.pop("predictors")
    return data_stats


def _extract_variable_lists(data_stats: dict) -> tuple[list[str], list[str], list[str]]:
    """
    Extract and categorize variables from data statistics.

    Parameters:
        data_stats (dict): data statistics dictionary containing features and targets

    Returns:
        tuple: (features, targets, categorical) - three lists of variable names
    """
    features = []
    targets = []
    categorical = []

    for var_type in ["features", "targets"]:
        if var_type not in data_stats:
            continue

        for name, value in data_stats[var_type].items():
            # For backward compatibility with data stats created before we lower-case
            name = name.lower()

            if var_type == "features":
                features.append(name)
            elif var_type == "targets":
                targets.append(name)

            if "type" in value and value["type"] == "categorical":
                categorical.append(name)

    return features, targets, categorical


def _validate_matching_row_counts(predicted_df: DataFrame, features_df: DataFrame):
    """
    Validate that prediction and feature dataframes have matching row counts.

    Parameters:
        predicted_df: predictions dataframe
        features_df: features dataframe

    Raises:
        ValueError: if row counts don't match
    """
    if predicted_df.shape[0] != features_df.shape[0]:
        raise ValueError(
            "The number of prediction rows do not match the number of features rows!"
        )


def _parse_scoring_stats(
    features_df: DataFrame,
    predicted_df: DataFrame,
    data_stats: dict,
    feature_importance: dict[str, float] = None,
    feature_metadata_fqtn: str = None,
    feature_metadata_group: str = None,
) -> dict:
    """
    Parse scoring statistics from features and predictions dataframes.

    Parameters:
        features_df: teradataml DataFrame containing features
        predicted_df: teradataml DataFrame containing predictions
        data_stats (dict): existing data statistics
        feature_importance (dict): feature importance scores
        feature_metadata_fqtn (str): fully qualified table name for feature metadata
        feature_metadata_group (str): monitoring group name

    Returns:
        dict: combined statistics for features and targets
    """
    feature_importance = feature_importance or {}

    # Validate input dataframes
    _validate_dataframe_type(features_df, "features")
    _validate_dataframe_type(predicted_df, "predictions")

    # Ensure backward compatibility
    data_stats = _ensure_backward_compatibility(data_stats)

    # Extract variable lists
    features, targets, categorical = _extract_variable_lists(data_stats)

    # Validate matching row counts
    _validate_matching_row_counts(predicted_df, features_df)

    # Capture statistics for features
    data_stats = _capture_stats(
        df=features_df,
        features=features,
        targets=[],
        categorical=categorical,
        feature_importance=feature_importance,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    # Capture statistics for targets
    targets_struct = _capture_stats(
        df=predicted_df,
        features=[],
        targets=targets,
        categorical=categorical,
        feature_importance=feature_importance,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    # Combine features and targets statistics
    data_stats["targets"] = targets_struct["targets"]

    return data_stats


def _normalize_variable_names(
    features: list,
    targets: list,
    categorical: list,
    feature_importance: dict,
) -> tuple[list, list, list, dict]:
    """
    Normalize all variable names to lowercase for case-insensitive matching.

    Parameters:
        features: list of feature names
        targets: list of target names
        categorical: list of categorical variable names
        feature_importance: dict of feature importance scores

    Returns:
        tuple: (normalized_features, normalized_targets, normalized_categorical, normalized_importance)
    """
    features = [f.lower() for f in features]
    targets = [t.lower() for t in targets]
    categorical = [c.lower() for c in categorical]
    feature_importance = {k.lower(): v for k, v in feature_importance.items()}

    return features, targets, categorical, feature_importance


def _validate_variables_in_dataframe(
    features: list, targets: list, df_columns: list, original_columns: list
):
    """
    Validate that features and targets exist in the DataFrame.

    Parameters:
        features: list of feature names (lowercase)
        targets: list of target names (lowercase)
        df_columns: list of DataFrame column names (lowercase)
        original_columns: original DataFrame columns for error message

    Raises:
        ValueError: if features or targets are not in DataFrame
    """
    if features and not set(features).issubset(df_columns):
        raise ValueError(
            f"features dataframe with columns ({original_columns}) does not contain"
            f" features: {features}"
        )

    if targets and not set(targets).issubset(df_columns):
        raise ValueError(
            f"targets dataframe with columns ({original_columns}) does not contain"
            f" targets: {targets}"
        )


def _categorize_variables(
    features: list, targets: list, categorical: list
) -> tuple[list, list]:
    """
    Categorize variables into continuous and categorical types.

    Parameters:
        features: list of feature names
        targets: list of target names
        categorical: list of categorical variable names

    Returns:
        tuple: (continuous_vars, categorical_vars)
    """
    continuous_vars = list((set(features) | set(targets)) - set(categorical))
    categorical_vars = list((set(features) | set(targets)) - set(continuous_vars))

    return continuous_vars, categorical_vars


def _process_continuous_variables(
    df: DataFrame,
    continuous_vars: list,
    feature_metadata_fqtn: str,
) -> tuple[pd.DataFrame | None, pd.DataFrame | None, list, list]:
    """
    Process continuous variables and retrieve statistics and histograms.

    Parameters:
        df: teradataml DataFrame
        continuous_vars: list of continuous variable names
        feature_metadata_fqtn: fully qualified table name for feature metadata

    Returns:
        tuple: (stats, histogram, reference_edges, available_continuous_vars)
    """
    if len(continuous_vars) == 0:
        return None, None, [], []

    stats = _safe_compute_valib_statistics(df, continuous_vars)
    stats = stats.result.to_pandas().fillna(value_for_nan).reset_index()
    stats["xcol"] = stats["xcol"].str.lower()

    stats_metadata = store.get_feature_stats(feature_metadata_fqtn, "continuous")

    reference_edges = []
    available_continuous_vars = []

    for v in continuous_vars:
        if v.lower() in stats_metadata.keys():
            reference_edges.append(stats_metadata[v.lower()]["edges"])
            available_continuous_vars.append(v)
        else:
            logger.warning(
                f"Feature {v} doesn't have statistics metadata defined, and will not be"
                " monitored.\nIn order to enable monitoring for this feature, make"
                " sure that statistics metadata is available in"
                f" {feature_metadata_fqtn}"
            )

    histogram = None
    if len(available_continuous_vars) > 0:
        hist_boundaries = _convert_all_edges_to_val_str(reference_edges)
        histogram = _histogram_wrapper(
            data=df, columns=available_continuous_vars, boundaries=hist_boundaries
        )
        histogram["xcol"] = histogram["xcol"].str.lower()

    return stats, histogram, reference_edges, available_continuous_vars


def _process_categorical_variables(
    df: DataFrame,
    categorical_vars: list,
    feature_metadata_fqtn: str,
) -> tuple[pd.DataFrame | None, list, list]:
    """
    Process categorical variables and retrieve frequencies.

    Parameters:
        df: teradataml DataFrame
        categorical_vars: list of categorical variable names
        feature_metadata_fqtn: fully qualified table name for feature metadata

    Returns:
        tuple: (frequencies, reference_categories, available_categorical_vars)
    """
    if len(categorical_vars) == 0:
        return None, [], []

    stats_metadata = store.get_feature_stats(feature_metadata_fqtn, "categorical")

    reference_categories = []
    available_categorical_vars = []

    for v in categorical_vars:
        if v.lower() in stats_metadata.keys():
            reference_categories.append(stats_metadata[v.lower()]["categories"])
            available_categorical_vars.append(v)
        else:
            logger.warning(
                f"Feature {v} doesn't have statistics metadata defined, and will not be"
                " monitored.\nIn order to enable monitoring for this feature, make"
                " sure that statistics metadata is available in"
                f" {feature_metadata_fqtn}"
            )

    # Compute frequencies for all categorical features
    frequencies = _safe_compute_valib_frequency(df, categorical_vars)
    frequencies = frequencies.result.to_pandas(all_rows=True).reset_index()
    frequencies["xcol"] = frequencies["xcol"].str.lower()

    return frequencies, reference_categories, available_categorical_vars


def _build_variable_metadata(
    variable_name: str,
    continuous_vars: list,
    available_continuous_vars: list,
    available_categorical_vars: list,
    stats: pd.DataFrame | None,
    histogram: pd.DataFrame | None,
    frequencies: pd.DataFrame | None,
    reference_edges: list,
    reference_categories: list,
    group_label: str,
    feature_importance: dict,
) -> dict:
    """
    Build metadata structure for a single variable.

    Parameters:
        variable_name: name of the variable
        continuous_vars: list of continuous variables
        available_continuous_vars: list of continuous vars with metadata
        available_categorical_vars: list of categorical vars with metadata
        stats: statistics DataFrame for continuous variables
        histogram: histogram DataFrame for continuous variables
        frequencies: frequencies DataFrame for categorical variables
        reference_edges: list of reference edges for continuous variables
        reference_categories: list of reference categories for categorical variables
        group_label: monitoring group name
        feature_importance: dict of feature importance scores

    Returns:
        dict: variable metadata structure
    """
    if variable_name in continuous_vars:
        if variable_name in available_continuous_vars:
            return _process_continuous_var(
                histogram=histogram,
                stats=stats,
                reference_edges=reference_edges[
                    available_continuous_vars.index(variable_name)
                ],
                group_label=group_label,
                variable_name=variable_name,
                feature_importance=feature_importance.get(variable_name, 0.0),
            )
        else:
            return _process_continuous_var(
                histogram=pd.DataFrame(),
                stats=stats,
                reference_edges=None,
                group_label=group_label,
                variable_name=variable_name,
                feature_importance=feature_importance.get(variable_name, 0.0),
            )
    else:  # categorical variable
        if variable_name in available_categorical_vars:
            return _process_categorical_var(
                frequencies=frequencies,
                group_label=group_label,
                variable_name=variable_name,
                feature_importance=feature_importance.get(variable_name, 0.0),
                reference_categories=reference_categories[
                    available_categorical_vars.index(variable_name)
                ],
            )
        else:
            return _process_categorical_var(
                frequencies=frequencies,
                group_label=group_label,
                variable_name=variable_name,
                feature_importance=feature_importance.get(variable_name, 0.0),
                reference_categories=None,
            )


def _capture_stats(
    df: DataFrame,
    features: list,
    targets: list,
    categorical: list,
    feature_importance: dict[str, float] = None,
    feature_metadata_fqtn: str = None,
    feature_metadata_group: str = "default",
) -> dict:
    """
    Capture statistics for features and targets from a DataFrame.

    Parameters:
        df: teradataml DataFrame containing data
        features: list of feature names
        targets: list of target names
        categorical: list of categorical variable names
        feature_importance: dict of feature importance scores
        feature_metadata_fqtn: fully qualified table name for feature metadata
        feature_metadata_group: monitoring group name

    Returns:
        dict: statistics structure containing features and targets metadata
    """
    feature_importance = feature_importance or {}

    if not isinstance(df, DataFrame):
        raise TypeError("We only support teradataml DataFrame")

    if not feature_metadata_fqtn:
        raise ValueError("feature_metadata_fqtn must be defined")

    # Normalize all variable names to lowercase
    original_columns = df.columns
    df_columns = [c.lower() for c in df.columns]
    features, targets, categorical, feature_importance = _normalize_variable_names(
        features, targets, categorical, feature_importance
    )

    # Validate that variables exist in DataFrame
    _validate_variables_in_dataframe(features, targets, df_columns, original_columns)

    # Categorize variables into continuous and categorical
    continuous_vars, categorical_vars = _categorize_variables(
        features, targets, categorical
    )

    # Process continuous variables
    stats, histogram, reference_edges, available_continuous_vars = (
        _process_continuous_variables(df, continuous_vars, feature_metadata_fqtn)
    )

    # Process categorical variables
    frequencies, reference_categories, available_categorical_vars = (
        _process_categorical_variables(df, categorical_vars, feature_metadata_fqtn)
    )

    # Build data structure
    total_rows = df.shape[0]
    data_struct = {"num_rows": total_rows, "features": {}, "targets": {}}

    # Add metadata for each feature
    for variable_name in features:
        data_struct["features"][variable_name] = _build_variable_metadata(
            variable_name=variable_name,
            continuous_vars=continuous_vars,
            available_continuous_vars=available_continuous_vars,
            available_categorical_vars=available_categorical_vars,
            stats=stats,
            histogram=histogram,
            frequencies=frequencies,
            reference_edges=reference_edges,
            reference_categories=reference_categories,
            group_label=feature_metadata_group,
            feature_importance=feature_importance,
        )

    # Add metadata for each target
    for variable_name in targets:
        data_struct["targets"][variable_name] = _build_variable_metadata(
            variable_name=variable_name,
            continuous_vars=continuous_vars,
            available_continuous_vars=available_continuous_vars,
            available_categorical_vars=available_categorical_vars,
            stats=stats,
            histogram=histogram,
            frequencies=frequencies,
            reference_edges=reference_edges,
            reference_categories=reference_categories,
            group_label=feature_metadata_group,
            feature_importance=feature_importance,
        )

    # Track missing metadata
    missing_continuous = [
        c for c in continuous_vars if c.lower() not in available_continuous_vars
    ]
    missing_categorical = [
        c for c in categorical_vars if c.lower() not in available_categorical_vars
    ]

    if len(missing_categorical) > 0 or len(missing_continuous) > 0:
        data_struct["missing_metadata"] = {}
        if len(missing_continuous) > 0:
            data_struct["missing_metadata"]["continuous"] = missing_continuous
        if len(missing_categorical) > 0:
            data_struct["missing_metadata"]["categorical"] = missing_categorical

    return data_struct


def _safe_compute_valib_frequency(features_df: DataFrame, features: list[str]):
    try:
        logger.debug(
            "Executing this VAL"
            f" {valib.Frequency(data=features_df, columns=features, charset='UTF8').show_query()}"
        )
        frequencies = valib.Frequency(
            data=features_df, columns=features, charset="UTF8"
        )
    except OperationalError as opError:
        if CHARSET_INVALID_PARAMETER in str(opError):
            logger.debug(
                "Executing this VAL"
                f" {valib.Frequency(data=features_df, columns=features).show_query()}"
            )
            frequencies = valib.Frequency(data=features_df, columns=features)
        else:
            raise

    return frequencies


def _safe_compute_valib_statistics(features_df: DataFrame, features: list[str]):
    try:
        logger.debug(
            "Executing this VAL"
            f" {valib.Statistics(data=features_df, columns=features, stats_options='all', charset='UTF8').show_query()}"
        )
        statistics = valib.Statistics(
            data=features_df, columns=features, stats_options="all", charset="UTF8"
        )
    except OperationalError as opError:
        if CHARSET_INVALID_PARAMETER in str(opError):
            logger.debug(
                "Executing this VAL"
                f" {valib.Statistics(data=features_df, columns=features, stats_options='all').show_query()}"
            )
            statistics = valib.Statistics(
                data=features_df, columns=features, stats_options="all"
            )
        else:
            raise

    return statistics


def _safe_compute_valib_histogram(
    features_df: DataFrame, features: list[str], boundaries: list[str | float | int]
):
    try:
        logger.debug(
            "Executing this VAL"
            f" {valib.Histogram(data=features_df,columns=features,boundaries=boundaries, charset='UTF8').show_query()}"
        )
        histogram = valib.Histogram(
            data=features_df, columns=features, boundaries=boundaries, charset="UTF8"
        )
    except OperationalError as opError:
        if CHARSET_INVALID_PARAMETER in str(opError):
            logger.debug(
                "Executing this VAL"
                f" {valib.Histogram(data=features_df,columns=features,boundaries=boundaries).show_query()}"
            )
            histogram = valib.Histogram(
                data=features_df, columns=features, boundaries=boundaries
            )
        else:
            raise

    return histogram


def _histogram_wrapper(data, columns, boundaries):
    working_columns = list(columns)
    working_boundaries = list(boundaries)
    result = []

    # Iterate over an updated list of columns while it's not empty
    while working_columns:
        tc = list(working_columns)
        tb = list(working_boundaries)
        # If the size of td_analyze parameter is bigger than the limit
        # then reduce the list of columns until it fits
        while _val_parameter_length_too_long(tc, tb):
            if len(tc) == 1:
                raise ValueError(
                    "VAL histogram parameters are too long even for single column"
                    f" {tc[0]}"
                )
            tc.pop()
            tb.pop()

        # compute a histogram on the longest possible list of columns
        histogram = _safe_compute_valib_histogram(data, tc, tb)
        result.append(histogram.result.to_pandas(all_rows=True).reset_index())

        # removing columns thats already computed
        working_columns = working_columns[len(tc) :]
        working_boundaries = working_boundaries[len(tb) :]

    return pd.concat(result)


def _val_parameter_length_too_long(columns, boundaries, limit=31000):
    db_tbl_string = "database=;tablename=;outputdatabase=;outputtablename=;"
    column_string = f"columns={','.join(columns)};boundaries={','.join(boundaries)};"
    # assuming maximum length for database and table names at 128
    final_length = len(db_tbl_string) + len(column_string) + 128 * 4
    if final_length > limit:
        logger.debug(
            "VAL histogram parameters are too long for these columns, trying to"
            f" compute sequentially: {','.join(columns)}"
        )
    return final_length > limit


def _round_to_td_float(x, max_digits=15):
    # This function is needed to cast/round decimal and float number to the maximum precision allowed by Teradata database.
    # Teradata floats allow maximum 15 digits for mantissa, so this strange logic below does exactly that.
    # Possibly at some point we may need to add a round to exponent as well.
    (sign, digits, exponent) = Decimal(x).as_tuple()
    e = len(digits) + exponent
    (_, m, _) = (
        Decimal(x)
        .scaleb(-e)
        .quantize(Decimal(f"1E-{max_digits}"))
        .normalize()
        .as_tuple()
    )
    return np.float64(Decimal((sign, m, e - len(m))))


def infer_columns_type(
    df=None, query=None, feature_columns=None, cardinality_threshold=10
):

    if query:
        df = DataFrame.from_query(query)
        df = df.to_pandas()

    categorical_features = []
    continuous_features = []

    for col in feature_columns:
        try:
            unique_values = df[col].dropna().unique()
            num_unique = len(unique_values)

            if df[col].dtype == "object" or df[col].dtype.name == "category":
                categorical_features.append(col)

            elif num_unique == 2 and all(val in [0, 1] for val in unique_values):
                categorical_features.append(col)

            elif (
                pd.api.types.is_numeric_dtype(df[col])
                and num_unique <= cardinality_threshold
            ):
                categorical_features.append(col)

            elif pd.api.types.is_numeric_dtype(df[col]):
                continuous_features.append(col)
            else:
                continuous_features.append(col)

        except Exception as e:
            print(f"Error processing column '{col}': {e}. Skipping.")
            continue

    return categorical_features, continuous_features
