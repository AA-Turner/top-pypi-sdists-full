from typing import List
from typing import Optional
from typing import Set

from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.schema import Schema
from tecton_proto.common import schema__client_pb2 as schema_pb2


# TODO(njoung): Enforce some consistency between callable functions and instantiated objects
# in the exports of this file

_OFFLINE_QUERY_METHODS_STRING = "`get_features_for_events()` or `get_features_in_range()`"


# Generic
def INTERNAL_ERROR(message):
    return TectonInternalError(
        f"We seem to have encountered an error. Please contact support for assistance. Error details: {message}"
    )


def MDS_INACCESSIBLE(host_port):
    return TectonInternalError(
        f"Failed to connect to Tecton at {host_port}, please check your connectivity or contact support"
    )


def SERVER_GROUP_NOT_FOUND(server_group_name, feature_service_name):
    return TectonValidationError(
        f"Server group '{server_group_name}' for Feature Service '{feature_service_name}' defined in the repo.yaml file is not found in the workspace. You can find all available Server Groups in a workspace using the CLI command `tecton server-group list`"
    )


def VALIDATION_ERROR_FROM_MDS(message, trace_id: Optional[str] = None):
    suffix = f", trace ID: {trace_id}" if trace_id else ""
    return TectonValidationError(f"{message}{suffix}")


def UNSUPPORTED_OPERATION(op, reason):
    return TectonValidationError(f"Operation '{op}' is not supported: {reason}")


def INVALID_SPINE_TIME_KEY_TYPE_SPARK(t):
    return TectonValidationError(
        f"Invalid type of timestamp_key column in the input events dataframe. Expected TimestampType, got {t}"
    )


INVALID_NULL_SPINE_TIME_KEY = TectonValidationError(
    "Unable to infer the time range of the events dataframe. This typically occurs when all the timestamps in the dataframe are null."
)


def INVALID_SPINE_TIME_KEY_TYPE_PANDAS(t):
    return TectonValidationError(
        f"Invalid type of timestamp_key column in the given events dataframe. Expected datetime, got {t}"
    )


def MISSING_SPINE_COLUMN(param, col, existing_cols):
    return TectonValidationError(
        f"{param} column is missing from the events dataframe. Expected to find '{col}' among available columns: '{', '.join(existing_cols)}'."
    )


def MISSING_REQUEST_DATA_IN_SPINE(key, existing_cols):
    return TectonValidationError(
        f"Request context key '{key}' not found in the events dataframe schema. Expected to find '{key}' among available columns: '{', '.join(existing_cols)}'."
    )


def NONEXISTENT_WORKSPACE(name, workspaces):
    return TectonValidationError(f'Workspace "{name}" not found. Available workspaces: {workspaces}')


def INCORRECT_MATERIALIZATION_ENABLED_FLAG(user_set_bool, server_side_bool):
    return TectonValidationError(
        f"'is_live={user_set_bool}' argument does not match the value on the server: {server_side_bool}"
    )


def UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(op):
    return TectonValidationError(f"Operation '{op}' is not supported in a development workspace")


def INVALID_JOIN_KEYS_TYPE(t):
    return TectonValidationError(f"Invalid type for join_keys. Expected Dict[str, Union[int, str, bytes]], got {t}")


def INVALID_REQUEST_DATA_TYPE(t):
    return TectonValidationError(
        f"Invalid type for request_data. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
    )


def INVALID_REQUEST_CONTEXT_TYPE(t):
    return TectonValidationError(
        f"Invalid type for request_context_map. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
    )


def INVALID_INDIVIDUAL_JOIN_KEY_TYPE(key: str, type_str: str):
    return TectonValidationError(
        f"Invalid type for join_key '{key}'. Expected either type int, str, or bytes, got {type_str}"
    )


def EMPTY_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not be empty.")


def EMPTY_ELEMENT_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have an empty element.")


def DUPLICATED_ELEMENTS_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have duplicated elements.")


def DATA_SOURCE_HAS_NO_BATCH_CONFIG(data_source: str):
    return TectonValidationError(
        f"Cannot run get_dataframe on locally defined Data Source '{data_source}' because it does not have a batch_config"
    )


def FEATURE_VIEW_HAS_NO_STREAM_SOURCE(feature_view: str):
    return TectonValidationError(
        f"Cannot run run_stream on Feature View {feature_view} because it does not have a Stream Source"
    )


def UNKNOWN_REQUEST_CONTEXT_KEY(keys, key):
    return TectonValidationError(f"Unknown request context key '{key}', expected one of: {keys}")


def FV_TIME_KEY_MISSING(fv_name):
    return TectonValidationError(f"Argument 'timestamp_key' is required for the feature definition '{fv_name}'")


def FV_NO_MATERIALIZED_DATA(fv_name):
    return TectonValidationError(
        f"Feature definition '{fv_name}' doesn't have any materialized data. Materialization jobs may not have updated the offline feature store yet. Please monitor using materialization_status() or use from_source=True to compute from source data."
    )


def FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(fd_name, workspace):
    return TectonValidationError(
        f"Feature Definition {fd_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). Please use from_source=True when getting features (not applicable for Feature Tables) or alternatively configure offline materialization for this Feature Definition in a live workspace."
    )


def FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(ft_name, workspace):
    return TectonValidationError(
        f"Feature Table {ft_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). Please apply this Feature Table to a live workspace and ingest some features before using {_OFFLINE_QUERY_METHODS_STRING}."
    )


def FEATURE_TABLE_GET_ONLINE_FEATURES_FROM_DEVELOPMENT_WORKSPACE(ft_name, workspace):
    return TectonValidationError(
        f"Feature Table {ft_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). Please apply this Feature Table to a live workspace and ingest some features before using with get_online_features()."
    )


def FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE(ft_name):
    return TectonValidationError(
        f"Feature Table {ft_name} does not have offline materialization enabled, i.e. offline=True. Cannot retrieve offline feature if offline materializaiton is not enabled."
    )


def FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(fv_name, fco_name):
    return TectonValidationError(
        f"{fco_name} {fv_name} is defined locally, i.e. it has not been applied to a Tecton workspace. In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
    )


def UNSUPPORTED_SAVE_IN_READ_API_WITH_LOCAL_OBJECT(fs_name):
    return TectonValidationError(
        f"{fs_name} is defined locally, i.e. it has not been applied to a Tecton workspace. In order to save features (i.e. save=True) this Feature Service must be applied to a workspace and have materialization enabled (i.e. offline=True)."
    )


def FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE_GFD(fv_name, workspace):
    return TectonValidationError(
        f"Feature View {fv_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
    )


def FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(fv_name, workspace):
    return TectonValidationError(
        f"Feature view {fv_name} uses incremental backfills and is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
        + "Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
        + f"Enable offline materialization for this feature view in a live workspace to use {_OFFLINE_QUERY_METHODS_STRING}. "
        + "Or use `run()` to test this feature view without materializing data."
    )


def FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_IN_LOCAL_MODE(fv_name):
    return TectonValidationError(
        f"Feature view {fv_name} uses incremental backfills and is locally defined which means materialization is not enabled."
        + "Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
        + f"Apply and enable offline materialization for this feature view in a live workspace to use {_OFFLINE_QUERY_METHODS_STRING}. "
        + "Or use `run()` to test this feature view locally in a notebook."
    )


def FD_GET_FEATURES_MATERIALIZATION_DISABLED(fd_name):
    return TectonValidationError(
        f"Feature View {fd_name} does not have offline materialization turned on. In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
    )


def FV_GET_FEATURES_MATERIALIZATION_DISABLED_GFD(fv_name):
    return TectonValidationError(
        f"Feature View {fv_name} does not have offline materialization turned on. Try calling this function with 'use_materialized_data=False' or alternatively configure offline materialization for this Feature View."
    )


# DataSources
DS_STREAM_PREVIEW_ON_NON_STREAM = TectonValidationError("'start_stream_preview' called on non-streaming data source")

DS_DATAFRAME_NO_TIMESTAMP = TectonValidationError(
    "Cannot find timestamp column for this data source. Please call 'get_dataframe' without parameters 'start_time' or 'end_time'."
)

DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER = TectonValidationError(
    "The method 'get_dataframe()' cannot filter on timestamps when 'apply_translator' is False. "
    "'start_time' and 'end_time' must be None."
)

DS_INCORRECT_SUPPORTS_TIME_FILTERING = TectonValidationError(
    "Cannot filter on timestamps when supports_time_filtering on data source is False. "
    "'start_time' and 'end_time' must be None."
)


def FS_INTERNAL_ERROR(message):
    return TectonInternalError(f"Online feature request error: {message}")


FS_GET_FEATURE_VECTOR_REQUIRED_ARGS = TectonValidationError(
    "get_feature_vector requires at least one of join_keys or request_context_map"
)

FS_API_KEY_MISSING = TectonValidationError(
    "API key is required for online feature requests, but was not found in the environment. Please generate a key and set TECTON_API_KEY "
    + "using https://docs.tecton.ai/docs/reading-feature-data/reading-feature-data-for-inference"
)


def FV_INVALID_MOCK_SOURCES(mock_sources_keys: List[str], fv_params: List[str]):
    return TectonValidationError(
        f"Mock sources {mock_sources_keys} do not match the Feature View's input parameters {fv_params}"
    )


def FV_INVALID_MOCK_INPUTS(mock_inputs: List[str], inputs: List[str]):
    msg = "Mock input in input_data parameter does not match FeatureView's inputs."
    missing_inputs = sorted(set(inputs) - set(mock_inputs))
    if missing_inputs:
        msg += f" Missing inputs: {missing_inputs}"
    extra_inputs = sorted(set(mock_inputs) - set(inputs))
    if extra_inputs:
        msg += f" Extra inputs: {extra_inputs}"
    return TectonValidationError(msg)


def UNDEFINED_REQUEST_SOURCE_INPUT(undefined_inputs: List[str], expected_inputs: List[str]):
    return TectonValidationError(
        f"The provided request source data contains keys not defined in the request source schema. Extraneous keys: {undefined_inputs}. Expected keys: {expected_inputs}."
    )


def FV_INVALID_MOCK_INPUTS_NUM_ROWS(num_rows: List[int]):
    return TectonValidationError(
        f"Number of rows are not equal across all mock_inputs. Number of rows found are: {str(num_rows)}."
    )


def FV_UNSUPPORTED_ARG(invalid_arg_name: str):
    return TectonValidationError(f"Argument '{invalid_arg_name}' is not supported for this FeatureView type.")


def FV_INVALID_ARG_VALUE(arg_name: str, value: str, expected: str):
    return TectonValidationError(f"Invalid argument value '{arg_name}={value}', supported value(s): '{expected}'")


def FV_INVALID_ARG_COMBO(arg_names: List[str]):
    return TectonValidationError(f"Invalid argument combinations; {str(arg_names)} cannot be used together.")


def FT_UNABLE_TO_ACCESS_SOURCE_DATA(fv_name):
    return TectonValidationError(
        f"The source data for FeatureTable {fv_name} does not exist. Please use from_source=False when calling this function."
    )


def NO_SCHEMA_FROM_SOURCE_FALSE(fv_name, method_name):
    return TectonValidationError(
        f"Feature view {fv_name} does not have a `features` parameter, and `from_source` is set to False. When calling `{method_name}`, either the `features` param must be used or `from_source` must be set to `True`. Please use the `features` parameter, or set `from_source=True`."
    )


class InvalidTransformationMode(TectonValidationError):
    def __init__(self, name: str, got: str, allowed_modes: List[str]):
        super().__init__(f"Mode for '{name}' is '{got}', must be one of: {', '.join(allowed_modes)}")


class InvalidConstantType(TectonValidationError):
    def __init__(self, value, allowed_types):
        allowed_types = [str(allowed_type) for allowed_type in allowed_types]
        super().__init__(
            f"Tecton const value '{value}' must have one of the following types: {', '.join(allowed_types)}"
        )


class InvalidTransformInvocation(TectonValidationError):
    def __init__(self, transformation_name: str, got: str):
        super().__init__(
            f"Allowed arguments for Transformation '{transformation_name}' are: "
            f"tecton.const, tecton.materialization_context, transformations, and DataSource inputs. Got: '{got}'"
        )


# Dataset
DATASET_SPINE_COLUMNS_NOT_SET = TectonValidationError(
    "Cannot retrieve the events dataframe when Dataset was created without one."
)

UNSUPPORTED_FETCH_AS_PANDAS_AVRO = TectonValidationError(
    "Logged datasets require spark. Please use `to_spark()` to fetch."
)


def INVALID_DATASET_PATH(path: str):
    return TectonValidationError(f"Dataset storage location must be an s3 path or a local directory. path={path}")


# Feature Retrevial
def GET_HISTORICAL_FEATURES_WRONG_PARAMS(params: List[str], if_statement: str):
    return TectonValidationError("Cannot provide parameters " + ", ".join(params) + f" if {if_statement}")


GET_ONLINE_FEATURES_ODFV_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this Feature View since it has other Feature Views as inputs"
)

GET_ONLINE_FEATURES_FS_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this Feature Service"
)


def GET_ONLINE_FEATURES_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError("The following required keys are missing in request_data: " + ", ".join(keys))


def GET_FEATURE_VECTOR_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError("The following required keys are missing in request_context_map: " + ", ".join(keys))


def GET_ONLINE_FEATURES_FS_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for this Feature Service since it contains a Feature View "
        + "with the following request data keys: "
        + ", ".join(keys)
    )


def GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for this Feature View with the following request data keys: "
        + ", ".join(keys)
    )


FROM_SOURCE_WITH_FT = TectonValidationError(
    "Computing features from source is not supported for Feature Tables. Try calling this method with from_source=False."
)

USE_MATERIALIZED_DATA_WITH_FT = TectonValidationError(
    "Computing features from source is not supported for Feature Tables. Try calling this method with use_materialized_data=True."
)

FS_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    "This Feature Service contains a Feature Table and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)

FV_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    "This Feature View has a Feature Table input and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)

# Backfill Config Validation
BFC_MODE_SINGLE_REQUIRED_FEATURE_END_TIME_WHEN_START_TIME_SET = TectonValidationError(
    "feature_end_time is required when feature_start_time is set, for a FeatureView with "
    + "single_batch_schedule_interval_per_job backfill mode."
)

BFC_MODE_SINGLE_INVALID_FEATURE_TIME_RANGE = TectonValidationError(
    "Run with single_batch_schedule_interval_per_job backfill mode only supports time range equal to batch_schedule"
)


def INCORRECT_KEYS(keys, join_keys):
    return TectonValidationError(
        f"Requested keys to be deleted ({keys}) do not match the expected join keys ({join_keys})."
    )


NO_STORE_SELECTED = TectonValidationError("One of online or offline store must be selected.")


def TOO_MANY_KEYS(max_keys: int):
    return TectonValidationError(f"Max number of keys to be deleted is {max_keys}.")


OFFLINE_STORE_NOT_SUPPORTED = TectonValidationError(
    "Only DeltaLake is supported for entity deletion in offline feature stores."
)

FV_UNSUPPORTED_AGGREGATION = TectonValidationError(
    "Argument 'aggregation_level' is not supported for Feature Views with `aggregations` not specified."
)

RUN_API_PARTIAL_LEVEL_UNSUPPORTED_FOR_COMPACTION = TectonValidationError(
    "aggregation_level='partial' is only supported for Aggregate Feature Views with Compaction Disabled. Use aggregation_level='full' or aggregation_level='disabled' instead."
)


def INVALID_JOIN_KEY_TYPE(t):
    return TectonValidationError(
        f"Invalid type of join keys '{t}'. Keys must be an instance of [pyspark.sql.dataframe.DataFrame, pandas.DataFrame]."
    )


def DUPLICATED_COLS_IN_KEYS(t):
    return TectonValidationError(f"Argument keys {t} have duplicated column names. ")


ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE = TectonValidationError(
    "Athena compute can only be used in live workspaces. Current workspace is not live. Please use a different compute mode or switch to a live workspace."
)

ATHENA_COMPUTE_NOT_SUPPORTED_IN_LOCAL_MODE = TectonValidationError(
    "Athena compute can only be used in on applied Tecton objects in live workspaces. Using a locally defined Tecton object is not currently supported with Athena."
)

ATHENA_COMPUTE_MOCK_SOURCES_UNSUPPORTED = TectonValidationError(
    "Athena compute can only be used with materialized data in live workspaces. Using mock data is not supported with Athena."
)

SNOWFLAKE_COMPUTE_MOCK_SOURCES_UNSUPPORTED = TectonValidationError(
    "Using mock data in `get_historical_features` is not supported with Snowflake."
)


def INVALID_USAGE_FOR_LOCAL_TECTON_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Tecton objects that have been applied to a Tecton workspace. This object was defined locally."
    )


def INVALID_USAGE_FOR_REMOTE_TECTON_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Tecton objects that have been defined locally. This object was retrieved from a Tecton workspace."
    )


def INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Feature Tables that have been applied to a Tecton workspace. This object was defined locally, which means this Feature Table cannot be materialized. Feature Tables require materialization in order to ingest features and perform feature retrieval."
    )


def CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on locally defined Tecton objects. This object was retrieved from a Tecton workpace. Please use `run()` instead."
    )


def INVALID_NUMBER_OF_FEATURE_VIEW_INPUTS(num_sources: int, num_inputs: int):
    return TectonValidationError(
        f"Number of Feature View Inputs ({num_inputs}) should match the number of Data Sources ({num_sources}) in the definition."
    )


def SCHEMAS_DO_NOT_MATCH(schema: schema_pb2.Schema, derived_schema: schema_pb2.Schema):
    return TectonValidationError(
        f"The provided schema does not match the derived schema.\nProvided schema: {Schema(schema)}\nDerived schema: {Schema(derived_schema)}"
    )


def INGESTAPI_USER_ERROR(status_code: int, reason: str, error_message: str):
    if (
        isinstance(error_message, dict)
        and "requestError" in error_message
        and "errorMessage" in error_message["requestError"]
    ):
        error_message = error_message["requestError"]["errorMessage"]
    return TectonValidationError(
        f"Received {status_code} {reason} from Stream IngestAPI. Error Message: \n {error_message}"
    )


def AGGREGATION_INTERVAL_SET_COMPACTION():
    return TectonValidationError("Feature views with stream compaction enabled cannot have `aggregation_interval` set.")


def COMPACTION_TIME_WINDOW_SERIES_UNSUPPORTED():
    return TectonValidationError(
        "Aggregations using a TimeWindowSeries window are not supported when `compaction_enabled=True`."
    )


def TOO_MANY_TRANSFORMATION_CONTEXTS(func_name: str):
    return TectonValidationError(f"Only 1 Context Parameter can be passed into transformation {func_name}.")


def INVALID_INPUTS_RESOURCE_PROVIDER(resource_provider_name: str):
    return TectonValidationError(
        f"Resource provider {resource_provider_name} can only have at most 1 context input parameter."
    )


TRANSFORMATION_CONTEXT_NOT_SUPPORTED = TectonValidationError(
    "Transformation Contexts are only supported on Batch, Stream and Realtime Feature Views."
)


def TRANSFORMATION_CONTEXT_NAME_NOT_FOUND(context_parameter_name: str, user_function: str):
    return TectonValidationError(
        f'Could not find context parameter "{context_parameter_name}" for function {user_function}.'
    )


def COMPUTE_MODE_UNSUPPORTED_FOR_METHOD(method_name):
    return TectonValidationError(f"{method_name}() is only supported for SPARK or RIFT Compute Modes.")


class ModeUnsupportedForFeatureView(TectonValidationError):
    def __init__(self, mode: str, has_transformation: bool):
        if has_transformation:
            msg = f"Mode {mode} does not support transformation."
        else:
            msg = f"Mode {mode} requires transformation."
        super().__init__(msg)


class ExpressionParsingError(TectonValidationError):
    """
    Exception that indicates a problem parsing the Calculation Expression defined in a Calculation Feature.
    """

    def __init__(self, message, calculation_name, can_drop_traceback=False):
        """Initialize an instance of the exception.

        The traceback for this exception may be dropped by SDK decorators if the
        `can_drop_traceback` flag is set.

        Args:
            message (str): A description of the error.
            calculation_name (str): The name of the calculation associated with the error.
            can_drop_traceback (bool, optional): Indicates whether the traceback can be dropped.
                Defaults to False.
        """
        msg = f"In Calculation {calculation_name}: {message}"
        super().__init__(msg, can_drop_traceback)
        self.can_drop_traceback = can_drop_traceback


def CONTEXT_PARAMETER_NAME_UNSUPPORTED_FOR_NO_TRANSFORMATION_MODE(context_parameter_name):
    return TectonValidationError(
        f'Overriding `context_parameter_name` to "{context_parameter_name}" is not supported for Realtime Feature Views without '
        'a transformation. Please access RealtimeContext using "context". For example, '
        '`Attribute("context__request_timestamp", Timestamp)`'
    )


GET_FEATURES_FOR_EVENTS_UNSUPPORTED = COMPUTE_MODE_UNSUPPORTED_FOR_METHOD("get_features_for_events")

GET_FEATURES_IN_RANGE_UNSUPPORTED = COMPUTE_MODE_UNSUPPORTED_FOR_METHOD("get_features_in_range")

GET_PROMPTS_FOR_EVENTS_UNSUPPORTED = COMPUTE_MODE_UNSUPPORTED_FOR_METHOD("get_prompts_for_events")

GET_PARTIAL_AGGREGATES_UNSUPPORTED_NON_AGGREGATE = TectonValidationError(
    "get_partial_aggregates() is only supported for Feature Views with Tecton Managed Aggregations."
)

GET_PARTIAL_AGGREGATES_UNSUPPORTED_COMPACTED = TectonValidationError(
    "get_partial_aggregates() is only supported for Aggregate Feature Views with Compaction Disabled."
)

GET_PARTIAL_AGGREGATES_UNSUPPORTED_CONTINUOUS = TectonValidationError(
    'Tecton does not create partial aggregates for Feature Views with "Continuous" Stream Processing Mode.'
)

RUN_TRANSFORMATION_UNSUPPORTED = TectonValidationError(
    "run_transformation() for Batch and Stream Feature Views is only supported for SPARK and RIFT Compute Modes."
)

RUN_TRANSFORMATION_UNSUPPORTED_FOR_NO_TRANSFORMATION_MODE = TectonValidationError(
    "run_transformation() is not supported for Realtime Feature Views without a transformation function."
)


def READ_API_DEPRECATION_TEMPLATE(old_method, new_method):
    return f"{old_method}() has been deprecated in Tecton 0.9 and will be fully removed in the next major SDK release. Please use {new_method}() instead. See https://docs.tecton.ai/docs/reading-feature-data/reading-feature-data-for-training/offline-retrieval-methods for more information."


GET_HISTORICAL_FEATURES_DEPRECATED_SPINE = READ_API_DEPRECATION_TEMPLATE(
    "get_historical_features", "get_features_for_events"
)

GET_HISTORICAL_FEATURES_DEPRECATED_TIME_RANGE = READ_API_DEPRECATION_TEMPLATE(
    "get_historical_features", "get_features_in_range"
)

RUN_DEPRECATED_TRANSFORMATION = READ_API_DEPRECATION_TEMPLATE("run", "run_transformation")

RUN_DEPRECATED_PARTIAL_AGGS = READ_API_DEPRECATION_TEMPLATE("run", "get_partial_aggregates")

RUN_DEPRECATED_FULL_AGG = READ_API_DEPRECATION_TEMPLATE("run", "get_features_in_range")

GET_SPINE_DF_DEPRECATED = READ_API_DEPRECATION_TEMPLATE("get_spine_dataframe", "get_events_dataframe")


class FeaturesRequired(TectonValidationError):
    def __init__(self, feature_view_name: str):
        super().__init__(f"The 'features' parameter for {feature_view_name} must be set and be non-empty.")


BUILD_ARGS_INTERNAL_ERROR = TectonInternalError(
    "_build_args() is for internal use only and can only be called on local objects"
)

UNSUPPORTED_FRAMEWORK_VERSION = RuntimeError(
    "The existing feature definitions have been applied with an older SDK. Please downgrade the Tecton SDK or upgrade the feature definitions."
)

ON_DEMAND_ENVIRONMENT_RENAMED = "'on_demand_environment' has been renamed to 'realtime_environment' and will be removed in a future version. Please use 'realtime_environment'"


def ON_DEMAND_ENVIRONMENT_DEPRECATED():
    return TectonValidationError(
        "Cannot specify both 'realtime_environment' and 'on_demand_environment' for a Feature Service. "
        + ON_DEMAND_ENVIRONMENT_RENAMED
    )


def ON_DEMAND_ENVIRONMENT_DEPRECATED_REPO():
    return TectonValidationError(
        "Found default values for both 'realtime_environment' and 'on_demand_environment' in repo.yaml. "
        + ON_DEMAND_ENVIRONMENT_RENAMED
    )


def FV_FEATURES_PARAM_HAS_DUPLICATE_NAMES(fv_name: str, duplicate_names: List[str]):
    return TectonValidationError(
        f"Feature View {fv_name} has duplicate Feature names in the `features` parameter: {', '.join(duplicate_names)}"
    )


VALIDATION_UPON_OBJECT_CREATION_VALIDATE_DEPRECATED = (
    "The validate() method is deprecated and will be removed in a "
    "future version. As of Tecton version 1.0 objects are "
    "validated upon object creation, so validate() is unnecessary."
)

REALTIME_FEATURE_VIEW_RUN_DEPRECATED = "run() is deprecated. Please use run_transformation() instead."


GET_HISTORICAL_FEATURES_DEPRECATION_REASON = "`get_historical_features()` is replaced by `get_features_for_events()` and `get_features_in_range()`. See [Offline Retrieval Methods](https://docs.tecton.ai/docs/reading-feature-data/reading-feature-data-for-training/offline-retrieval-methods) for details."
