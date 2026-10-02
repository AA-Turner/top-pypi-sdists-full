import json
import logging
import math
import numbers
import os

from teradatasql import OperationalError
from teradataml import DataFrame, configure
from teradataml.analytics.valib import *  # noqa # NOSONAR(python:S2208)

from tmo.context.model_context import ModelContext
from tmo.stats.stats_util import (
    _capture_stats,
    _NpEncoder,
    _parse_scoring_stats,
    _compute_continuous_edges,
    _safe_compute_valib_statistics,
    _safe_compute_valib_frequency,
    infer_columns_type,
)
from tmo.stats.store import save_feature_stats

DATA_STATS_FILENAME = "data_stats.json"
DATA_STATS_INPUT_FILEPATH = f"artifacts/input/{DATA_STATS_FILENAME}"
DATA_STATS_OUTPUT_FILEPATH = f"artifacts/output/{DATA_STATS_FILENAME}"

logger = logging.getLogger(__name__)


def record_training_stats(
    df: DataFrame,
    features: list[str],
    targets: list[str] = None,
    categorical: list[str] = None,
    context: ModelContext = None,
    feature_importance: dict[str, float] = None,
    **kwargs,
) -> dict:
    """
    Compute and record the dataset statistics used for training. This information provides ModelOps with a snapshot
    of the dataset at this point in time (i.e. at the point of training). ModelOps uses this information for data and
    prediction drift monitoring. It can also be used for data quality monitoring as all the information which is
    captured here is available to configure an alert on (e.g. max > some_threshold).

    Depending on the type of variable (categorical or continuous), different statistics and distributions are computed.
    All of this is computed in Vantage via the Vantage Analytics Library (VAL).

    Continuous Variable:
        Distribution: Histogram
        Statistics: Min, Max, Average, Skew, etc., nulls

    Categorical Variable:
        Distribution: Frequency
        Statistics: nulls

    The following example shows how you would use this function for a binary classification problem where the there
    are 3 features and 1 target. As it is classification, the target must be categorical and in this case, the features
    are all continuous.
    example usage:
        training_df = DataFrame.from_query("SELECT * from my_table")

        record_training_stats(training_df,
                              features=["feat1", "feat2", "feat3"],
                              targets=["targ1"],
                              categorical=["targ1"],
                              context=context)

    :param df: teradataml dataframe used for training with the feature and target variables
    :type df: teradataml.DataFrame
    :param features: feature variable(s) used in this training
    :type features: list[str]
    :param targets: target variable(s) used in this training
    :type targets: list[str]
    :param categorical: variable(s) (feature or target) that is categorical
    :type categorical: list[str]
    :param context: ModelContext which is associated with that training invocation
    :type context: ModelContext
    :param feature_importance: (Optional) feature importance
    :type feature_importance: dict[str, float]
    :return: the computed data statistics
    :rtype: dict
    :raise ValueError: if features or targets are not provided
    :raise TypeError: if df is not of type teradataml.DataFrame
    """

    logger.info("Computing training dataset statistics")

    targets = targets or []
    categorical = categorical or []
    context = context or {}
    feature_importance = feature_importance or {}

    if not features:
        raise ValueError("One or more features must be provided")

    # backward compatibility for when we had targets incorrectly named predictors. remove in future version
    if "predictors" in kwargs:
        logger.warning(
            "Usage of `predictors` as argument to `record_training_stats` is"
            " deprecated. "
        )
        targets = kwargs.pop("predictors")

    if not targets:
        logger.warning(
            "One or more targets are not provided to collect training statistics, make"
            " sure this is what you want."
        )

    feature_metadata_fqtn = None
    feature_metadata_group = None
    data_stats_filename = DATA_STATS_OUTPUT_FILEPATH

    if context:
        feature_metadata_fqtn = context.dataset_info.get_feature_metadata_fqtn()
        feature_metadata_group = context.dataset_info.feature_metadata_monitoring_group
        data_stats_filename = os.path.join(
            context.artifact_output_path, DATA_STATS_FILENAME
        )

    data_stats = _capture_stats(
        df=df,
        features=features,
        targets=targets,
        categorical=categorical,
        feature_importance=feature_importance,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    with open(data_stats_filename, "w+") as f:
        json.dump(data_stats, f, indent=2, cls=_NpEncoder)

    return data_stats


def record_evaluation_stats(
    features_df: DataFrame,
    predicted_df: DataFrame,
    feature_importance: dict[str, float] = None,
    context: ModelContext = None,
    **kwargs,  # noqa # NOSONAR(python:S1172)
) -> dict:
    """
    Compute and record the dataset statistics used for evaluation. This information provides ModelOps with a snapshot
    of the dataset at this point in time (i.e. at the point of evaluation). ModelOps uses this information for data
    and prediction drift monitoring. It can also be used for data quality monitoring as all the information which
    is captured here is available to configure an alert on (e.g. max > some_threshold).

    Depending on the type of variable (categorical or continuous), different statistics and distributions are computed.
    All of this is computed in Vantage via the Vantage Analytics Library (VAL).

    Continuous Variable:
        Distribution: Histogram
        Statistics: Min, Max, Average, Skew, etc., nulls

    Categorical Variable:
        Distribution: Frequency
        Statistics: nulls

    example usage:
        features_df = DataFrame.from_query("SELECT * from my_features_table")

        predicted_df = model.predict(features_df)

        record_evaluation_stats(features_df=features_df,
                                predicted_df=predicted_df,
                                context=context)

    :param features_df: dataframe containing feature variable(s) from evaluation
    :type features_df: teradataml.DataFrame
    :param predicted_df: dataframe containing predicted target variable(s) from evaluation
    :type predicted_df: teradataml.DataFrame
    :param context: ModelContext which is associated with that training invocation
    :type context: ModelContext
    :param feature_importance: (Optional) feature importance
    :type feature_importance: dict[str, float]
    :return: the computed data statistics
    :rtype: dict
    :raise ValueError: if the number of predictions (rows) do not match the number of features (rows)
    :raise TypeError: if features_df or predicted_df is not of type teradataml.DataFrame
    """

    logger.info("Computing evaluation dataset statistics")

    feature_importance = feature_importance or {}
    feature_metadata_fqtn = None  # noqa
    feature_metadata_group = None
    output_data_stats_filename = DATA_STATS_OUTPUT_FILEPATH
    input_data_stats_filename = DATA_STATS_INPUT_FILEPATH

    if context:
        feature_metadata_fqtn = context.dataset_info.get_feature_metadata_fqtn()
        feature_metadata_group = context.dataset_info.feature_metadata_monitoring_group
        output_data_stats_filename = os.path.join(
            context.artifact_output_path, DATA_STATS_FILENAME
        )
        input_data_stats_filename = os.path.join(
            context.artifact_input_path, DATA_STATS_FILENAME
        )

    with open(input_data_stats_filename, "r") as f:
        training_data_stats = json.load(f)

    data_stats = _parse_scoring_stats(
        features_df=features_df,
        predicted_df=predicted_df,
        data_stats=training_data_stats,
        feature_importance=feature_importance,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    # for evaluation, the core will do it (we may change this later to unify).
    with open(output_data_stats_filename, "w+") as f:
        json.dump(data_stats, f, indent=2, cls=_NpEncoder)

    return data_stats


def record_scoring_stats(
    features_df: DataFrame, predicted_df: DataFrame, context: ModelContext = None
) -> dict:
    """
    Compute and record the dataset statistics used for scoring. This information provides ModelOps with a snapshot
    of the dataset at this point in time (i.e. at the point of scoring). ModelOps uses this information for data
    and prediction drift monitoring. It can also be used for data quality monitoring as all the information which
    is captured here is available to configure an alert on (e.g. max > some_threshold).

    Depending on the type of variable (categorical or continuous), different statistics and distributions are computed.
    All of this is computed in Vantage via the Vantage Analytics Library (VAL).

    Continuous Variable:
        Distribution: Histogram
        Statistics: Min, Max, Average, Skew, etc., nulls

    Categorical Variable:
        Distribution: Frequency
        Statistics: nulls

    example usage:
        features_df = DataFrame.from_query("SELECT * from my_features_table")

        predicted_df = model.predict(features_df)

        record_scoring_stats(features_df=features_df,
                            predicted_df=predicted_df,
                            context=context)

    :param features_df: dataframe containing feature variable(s) from evaluation
    :type features_df: teradataml.DataFrame
    :param predicted_df: dataframe containing predicted target variable(s) from evaluation
    :type predicted_df: teradataml.DataFrame
    :param context: ModelContext which is associated with that training invocation
    :type context: ModelContext
    :return: the computed data statistics
    :rtype: dict
    :raise ValueError: if the number of predictions (rows) do not match the number of features (rows)
    :raise TypeError: if features_df or predicted_df is not of type teradataml.DataFrame
    """

    logger.info("Computing scoring dataset statistics")

    feature_metadata_fqtn = None  # noqa
    feature_metadata_group = None
    input_data_stats_filename = DATA_STATS_INPUT_FILEPATH
    output_data_stats_filename = DATA_STATS_OUTPUT_FILEPATH

    if context:
        feature_metadata_fqtn = context.dataset_info.get_feature_metadata_fqtn()
        feature_metadata_group = context.dataset_info.feature_metadata_monitoring_group
        input_data_stats_filename = os.path.join(
            context.artifact_input_path, DATA_STATS_FILENAME
        )
        output_data_stats_filename = os.path.join(
            context.artifact_output_path, DATA_STATS_FILENAME
        )

    with open(input_data_stats_filename, "r") as f:
        training_data_stats = json.load(f)

    data_stats = _parse_scoring_stats(
        features_df=features_df,
        predicted_df=predicted_df,
        data_stats=training_data_stats,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    # for evaluation, the core will do it (we may change this later to unify).
    with open(output_data_stats_filename, "w+") as f:
        json.dump(data_stats, f, indent=2, cls=_NpEncoder)

    return data_stats


def _is_numeric_type(dtype_str: str) -> bool:
    return (
        dtype_str.startswith("decimal")
        or dtype_str.startswith("float")
        or dtype_str.startswith("int")
    )


def _filter_numeric_features(features: list[str], dtypes: dict) -> list[str]:
    numeric_features = []
    for feature in features:
        if _is_numeric_type(dtypes[feature]):
            numeric_features.append(feature)
        else:
            logger.warning(
                f"Column {feature} has a type {dtypes[feature]} which is not compatible"
                " with continuous feature types. This column will be ignored."
            )
    return numeric_features


def _compute_valib_statistics(features_df: DataFrame, features: list[str]):
    return _safe_compute_valib_statistics(features_df, features)


def _filter_trivial_features(features: list[str], statistics) -> list[str]:
    non_trivial_features = []
    for feature in features:
        if statistics.loc[feature].loc["xcnt"] == 0:
            logger.warning(f"Feature {feature} has only NULL values, ignored")
        elif statistics.loc[feature].loc["xmin"] == statistics.loc[feature].loc["xmax"]:
            logger.warning(
                f"Feature {feature} doesn't have enough unique values to be considered"
                " continuous feature (needs at least two distinct not null values),"
                " ignored"
            )
        else:
            non_trivial_features.append(feature)
    return non_trivial_features


def _validate_bin_counts(edges_dict: dict, expected_bins: int) -> None:
    for variable_name, edges in edges_dict.items():
        if len(edges) < expected_bins:
            logger.warning(
                f"Variable {variable_name} has only {len(edges)} bins computed when"
                f" {expected_bins} should have been computed {edges}.\nPlease ensure"
                " the variable is not categorical (use -t categorical)."
            )


def compute_continuous_stats(
    features_df: DataFrame,
    continuous_features: list[str],
    temp_view_database: str = None,
):
    """This function computes bin edges for continuous features. Only numeric columns are used,
    others are ignored with warning. For each column it computes maximum and minimum values, and
    attempts to split the difference into 10 bins. If only smaller number is possible - it generates
    the maximum number (e.g. integer column with minimum 5 and maximum 10 generates only 5 bins).
    The column has to have at least two distinct values, otherwise the column is ignored.

    Args:
        features_df (DataFrame): Teradata DataFrame used to compute statistics metadata
        continuous_features (list): list of columns representing continuous features
        temp_view_database (str, optional): The database for creating temporary views

    Returns:
        dict: Dictionary with keys corresponding to requested features, and values containing edges
    """
    if temp_view_database:
        configure.temp_view_database = temp_view_database

    dtypes = {r[0].lower(): r[1] for r in features_df.dtypes._column_names_and_types}

    lowered_features = list(map(str.lower, continuous_features))
    numeric_features = _filter_numeric_features(lowered_features, dtypes)

    if len(numeric_features) == 0:
        raise ValueError(
            "No columns with computable statistics metadata were found, please see"
            " warning messages above"
        )

    statistics = _compute_valib_statistics(features_df, numeric_features)

    statistics_df = statistics.result.to_pandas(all_rows=True).reset_index()
    statistics_df["xcol"] = statistics_df["xcol"].str.lower()
    statistics_df = statistics_df.set_index("xcol", drop=False)

    non_trivial_features = _filter_trivial_features(numeric_features, statistics_df)

    bins = 10
    reference_edges = _compute_continuous_edges(
        non_trivial_features, statistics_df, dtypes, bins=bins
    )
    edges_dict = dict(zip(non_trivial_features, reference_edges))

    _validate_bin_counts(edges_dict, bins)

    column_stats = {f.lower(): {"edges": edges_dict[f]} for f in edges_dict.keys()}

    if len(column_stats) == 0:
        raise ValueError(
            "No columns with computable statistics metadata were found, please see"
            " warning messages above"
        )

    return column_stats


def compute_categorical_stats(
    features_df: DataFrame,
    categorical_features: list[str],
    temp_view_database: str = None,
):
    """This function computes frequencies for categorical features. Each column must have at least one non-NULL value,
    all NULL columns are ignored. NULL value is ignored in frequencies (number of NULLs is reported for every
    training/evaluation/scoring jobs).

    Args:
        features_df (DataFrame): Teradata DataFrame used to compute statistics metadata
        categorical_features (list): list of columns representing categorical features
        temp_view_database (str, optional): The database for creating temporary views

    Returns:
        dict: Dictionary with keys corresponding to requested features, and values containing frequencies
    """
    if temp_view_database:
        configure.temp_view_database = temp_view_database

    statistics = _safe_compute_valib_frequency(features_df, categorical_features)
    statistics = statistics.result.to_pandas(all_rows=True).reset_index()
    statistics = statistics.drop(
        statistics.columns.difference(["xcol", "xval", "xpct"]), axis=1
    )
    statistics["xcol"] = statistics["xcol"].str.lower()
    statistics = (
        statistics.groupby("xcol", group_keys=False)
        .apply(lambda x: dict(zip(x["xval"], x["xpct"])), include_groups=False)
        .to_dict()
    )

    lowered_features = list(map(str.lower, categorical_features))  # noqa
    features = list(lowered_features)
    for f in features:
        values_list = list(statistics[f].keys())
        for k in values_list:
            if isinstance(k, numbers.Number) and math.isnan(k):  # noqa
                logger.warning(
                    f"Categorical feature {f} has NULL values in reference table,"
                    " NULLs will be ignored"
                )
                del statistics[f][k]
        if not statistics[f]:
            logger.warning(
                f"Categorical feature {f} has only NULL values in reference table, no"
                " statistics metadata generated"
            )
            lowered_features.remove(f)

    column_stats = {
        f: {"categories": list(statistics[f].keys())} for f in lowered_features
    }

    return column_stats


def compute_stats(
    metadata_table: str,
    entity_target_columns: dict,
    database: str = None,
    features_table: str = None,
    feature_types: dict = None,
    dataframe: DataFrame = None,
    temp_view_database: str = None,
) -> None:
    """
    Computes statistics for the specified dataset and inserts them into the desired table.

    Parameters:
        metadata_table (str): The metadata table to store the computed stats.
        entity_target_columns (dict): A dictionary with keys "entityColumns" and "targetColumns", each containing a list of column names.
        database (str): The database name.
        features_table (str, optional): The table containing the features. If not provided, the function will use the provided dataframe to get the data.
        feature_types (dict, optional): A dictionary with keys "categorical" and "continuous", each containing a list of feature names.
        dataframe (DataFrame, optional): A DataFrame containing the data. If not provided, the function will query the provided table and database to get the data.
        temp_view_database (str, optional): The database for creating temporary views.

    Returns:
        None

    Example:
        ```python
        from tmo import TmoClient
        from teradataml import DataFrame

        con = create_context(host="10.15.126.184",username="admin",password="admin",database="td_modelops")

        data = DataFrame.from_table("my_data_table")

        vmoClient = TmoClient()

        vmoClient
        .dataset_templates()
        .compute_stats(
            database="td_modelops",
            features_table="pima_patient_data",
            entity_target_columns={
                "entityColumns": ["PatientId"],
                "targetColumns": ["HasDiabetes"],
            },
            metadata_table="pima_feature_metadata",
            dataframe=data,
            temp_view_database="view_db"
        )
        ```
    """
    if temp_view_database:
        configure.temp_view_database = temp_view_database

    if not features_table and not dataframe:
        raise ValueError(
            "At least one of 'features_table' or 'dataframe' must be provided."
        )

    if features_table and not database:
        raise ValueError(
            "If 'features_table' is provided, 'database' must also be provided."
        )

    if not dataframe:
        tdf = DataFrame.from_query(f"SELECT * FROM {database}.{features_table}")  # noqa
        df = tdf.to_pandas()
    else:
        tdf = dataframe
        df = tdf.to_pandas()

    if df.empty:
        print(
            "Warning: The query returned an empty DataFrame. No statistics will"
            " be computed."
        )
        return

    if not feature_types:
        entity_columns = entity_target_columns["entityColumns"]
        target_columns = entity_target_columns["targetColumns"]

        feature_columns = [
            col for col in df.columns if col not in entity_columns + target_columns
        ]

        categorical_features, continuous_features = infer_columns_type(
            df=df, feature_columns=feature_columns
        )

    else:
        categorical_features = feature_types.get("categorical", [])
        continuous_features = feature_types.get("continuous", [])

    try:
        if categorical_features:
            categorical_stats = compute_categorical_stats(tdf, categorical_features)
            save_feature_stats(
                features_table=metadata_table,
                feature_type="categorical",
                stats=categorical_stats,
            )
        if continuous_features:
            continuous_stats = compute_continuous_stats(tdf, continuous_features)
            save_feature_stats(
                features_table=metadata_table,
                feature_type="continuous",
                stats=continuous_stats,
            )

    except Exception as ex:
        raise RuntimeError(f"Could not compute feature stats: {ex}") from ex
