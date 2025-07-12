from datetime import datetime
from datetime import timezone
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas
from pyspark.sql import DataFrame as pysparkDF
from pyspark.sql.types import TimestampType

from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton_core import data_processing_utils
from tecton_core import specs
from tecton_core.errors import TectonValidationError
from tecton_core.fco_container import FcoContainer
from tecton_core.id_helper import IdHelper
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query_consts import MOCK_COLUMN_SEPARATOR
from tecton_core.query_consts import udf_internal
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_proto.data.freshness_status__client_pb2 import FreshnessStatus
from tecton_proto.data.materialization_status__client_pb2 import DataSourceType
from tecton_proto.data.materialization_status__client_pb2 import MaterializationAttemptStatus
from tecton_proto.data.materialization_status__client_pb2 import MaterializationStatusState
from tecton_proto.metadataservice.metadata_service__client_pb2 import GetFeatureFreshnessRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import GetWorkspaceRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import QueryFeatureViewsRequest


_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


def validate_join_keys(join_keys: List[str]):
    """
    Validates that `join_keys` is not empty and has non-empty distinct values.

    :raises TectonValidationError: if `join_keys` is invalid.
    """
    if not join_keys:
        msg = "join_keys"
        raise errors.EMPTY_ARGUMENT(msg)

    if "" in join_keys:
        msg = "join_keys"
        raise errors.EMPTY_ELEMENT_IN_ARGUMENT(msg)

    if len(join_keys) > len(set(join_keys)):
        msg = "join_keys"
        raise errors.DUPLICATED_ELEMENTS_IN_ARGUMENT(msg)


def validate_spine_dataframe(
    spine: DataframeWrapper, timestamp_key: Optional[str], request_context_keys: Optional[List[str]] = None
):
    spine_df = spine._dataframe
    if not hasattr(spine_df, "columns"):
        return

    if timestamp_key:
        if timestamp_key not in spine_df.columns:
            msg = "timestamp_key"
            raise errors.MISSING_SPINE_COLUMN(msg, timestamp_key, spine_df.columns)
        if is_pyspark_df(spine_df):
            data_type = spine_df.schema[timestamp_key].dataType
            if not isinstance(data_type, TimestampType):
                raise errors.INVALID_SPINE_TIME_KEY_TYPE_SPARK(data_type)
        elif isinstance(spine_df, pandas.DataFrame):
            dtypes = dict(spine_df.dtypes)
            data_type = dtypes[timestamp_key]
            if not pandas.api.types.is_datetime64_any_dtype(data_type):
                raise errors.INVALID_SPINE_TIME_KEY_TYPE_PANDAS(data_type)
        else:
            raise errors.UNRECOGNIZED_EVENTS_DATAFRAME_TYPE(type(spine_df))
    if request_context_keys:
        for key in request_context_keys:
            if key not in spine_df.columns:
                raise errors.MISSING_REQUEST_DATA_IN_SPINE(key, spine_df.columns)


def get_mocked_feature_view_columns(columns: List[str]) -> Dict[str, List[str]]:
    feature_view_to_features = {}

    for column in columns:
        if MOCK_COLUMN_SEPARATOR in column:
            feature_view_name, feature_name = column.split(MOCK_COLUMN_SEPARATOR, 1)
            if feature_view_name not in feature_view_to_features:
                feature_view_to_features[feature_view_name] = []
            feature_view_to_features[feature_view_name].append(feature_name)

    return feature_view_to_features


def format_seconds_into_highest_unit(total_seconds):
    intervals = [("wk", 60 * 60 * 24 * 7), ("d", 60 * 60 * 24), ("h", 60 * 60), ("m", 60), ("s", 1)]

    units = []
    for abbreviation, size in intervals:
        count = total_seconds // size
        total_seconds %= size
        if count != 0:
            units.append(f"{count}{abbreviation}")

    return " ".join(units[:2] if len(units) > 2 else units)


def snake_to_capitalized(snake_str):
    return "".join(x.title() for x in snake_str.split("_"))


def format_materialization_attempts(
    materialization_attempts,
    verbose=False,
    limit=1000,
    sort_columns=None,
    errors_only=False,
    override_columns: Optional[str] = None,
) -> Tuple[List, List[List]]:
    """
    Formats a list of materialization attempts for use in Displayable.from_table
    Returns (column_names, materialization_status_rows).
    """
    if not override_columns:
        column_names = ["TYPE", "WINDOW_START_TIME", "WINDOW_END_TIME", "STATUS", "ATTEMPT"]
        if verbose:
            column_names.extend(
                ["MATERIALIZATION_TASK", "ENV_VERSION", "TERMINATION_REASON", "STATE_MESSAGE", "TASK_SCHEDULED_AT"]
            )
        column_names.extend(["JOB_CREATED_AT", "JOB_LOGS"])
    else:
        column_names = override_columns

    materialization_attempts = materialization_attempts[:limit]
    if errors_only:
        materialization_attempts = [
            attempt
            for attempt in materialization_attempts
            if _materialization_status_state_name(attempt.materialization_state) == "ERROR"
        ]

    materialization_status_rows = []
    for attempt_status in materialization_attempts:
        data = _get_materialization_status_row_data(attempt_status)
        materialization_status_rows.append([data[c] for c in column_names])

    if sort_columns:
        keys = [k.upper() for k in sort_columns.split(",")]
        indices = []
        for key in keys:
            try:
                indices.append(column_names.index(key))
            except ValueError:
                msg = f"Unknown sort key {key}, should be one of: {','.join(column_names)}"
                raise ValueError(msg)
        materialization_status_rows.sort(key=lambda r: [r[i] for i in indices])

    return column_names, materialization_status_rows


def _materialization_status_state_name(state: MaterializationStatusState) -> str:
    state_name = MaterializationStatusState.Name(state)
    return state_name.replace("MATERIALIZATION_STATUS_STATE_", "")


def _get_materialization_status_row_data(attempt_status: MaterializationAttemptStatus) -> Dict[str, str]:
    status_dict = {}
    status_dict["TYPE"] = (
        "STREAM"
        if attempt_status.data_source_type == DataSourceType.DATA_SOURCE_TYPE_STREAM
        else "BATCH"
        if attempt_status.data_source_type == DataSourceType.DATA_SOURCE_TYPE_BATCH
        else "INGEST"
        if attempt_status.data_source_type == DataSourceType.DATA_SOURCE_TYPE_INGEST
        else "DELETION"
        if attempt_status.data_source_type == DataSourceType.DATA_SOURCE_TYPE_DELETION
        else "FEATURE PUBLISH"
        if attempt_status.data_source_type == DataSourceType.DATA_SOURCE_TYPE_FEATURE_EXPORT
        else "DATASET GENERATION"
        if attempt_status.data_source_type == DataSourceType.DATA_SOURCE_TYPE_DATASET_GENERATION
        else "UNKNOWN"
    )
    status_dict["WINDOW_START_TIME"] = (
        "N/A"
        if not attempt_status.HasField("window_start_time")
        else attempt_status.window_start_time.ToDatetime().replace(tzinfo=timezone.utc).strftime(_TIME_FORMAT)
    )
    status_dict["WINDOW_END_TIME"] = (
        "N/A"
        if not attempt_status.HasField("window_end_time")
        else attempt_status.window_end_time.ToDatetime().replace(tzinfo=timezone.utc).strftime(_TIME_FORMAT)
    )
    status_dict["STATUS"] = _materialization_status_state_name(attempt_status.materialization_state)
    status_dict["ATTEMPT"] = "N/A" if not attempt_status.HasField("attempt_number") else attempt_status.attempt_number
    status_dict["MATERIALIZATION_TASK"] = IdHelper.to_string(attempt_status.materialization_task_id)
    status_dict["ENV_VERSION"] = attempt_status.spark_cluster_environment_version
    status_dict["TERMINATION_REASON"] = (
        "N/A"
        if not attempt_status.HasField("termination_reason")
        or len(attempt_status.termination_reason) == 0
        or attempt_status.termination_reason == "UNKNOWN_TERMINATION_REASON"
        else attempt_status.termination_reason
    )
    status_dict["STATE_MESSAGE"] = (
        "N/A"
        if not attempt_status.HasField("state_message") or len(attempt_status.state_message) == 0
        else attempt_status.state_message
    )
    status_dict["TASK_SCHEDULED_AT"] = (
        "N/A"
        if not attempt_status.HasField("materialization_task_created_at")
        else attempt_status.materialization_task_created_at.ToDatetime()
        .replace(tzinfo=timezone.utc)
        .strftime(_TIME_FORMAT)
    )
    status_dict["JOB_CREATED_AT"] = (
        "N/A"
        if not attempt_status.HasField("attempt_created_at")
        else attempt_status.attempt_created_at.ToDatetime().replace(tzinfo=timezone.utc).strftime(_TIME_FORMAT)
    )
    status_dict["JOB_LOGS"] = "N/A" if not attempt_status.HasField("run_page_url") else attempt_status.run_page_url

    return status_dict


def infer_timestamp(spine: Union[pandas.DataFrame, pysparkDF, DataframeWrapper]) -> Optional[str]:
    if not isinstance(spine, (pandas.DataFrame, pysparkDF, DataframeWrapper)):
        msg = "`timestamp_key` must be provided when spine is not a data frame"
        raise TectonValidationError(msg)

    if isinstance(spine, DataframeWrapper):
        spine = spine._dataframe
    dtypes = dict(spine.dtypes)

    if isinstance(spine, pandas.DataFrame):
        return data_processing_utils.infer_pandas_timestamp(spine)
    elif is_pyspark_df(spine):
        timestamp_cols = [(k, v) for (k, v) in dtypes.items() if v == "timestamp"]
    else:
        msg = f"Unexpected data type for spine: {type(spine)}"
        raise TectonValidationError(msg)

    if len(timestamp_cols) > 1 or len(timestamp_cols) == 0:
        msg = f"Could not infer timestamp keys from {dtypes}; please specify explicitly"
        raise TectonValidationError(msg)
    return timestamp_cols[0][0]


def can_be_stale(ff_proto: FreshnessStatus) -> bool:
    return (
        ff_proto.expected_freshness.seconds > 0 and ff_proto.freshness.seconds > 0 and ff_proto.materialization_enabled
    )


def format_freshness_table(freshness_statuses: List[FreshnessStatus]) -> Displayable:
    timestamp_format = "%x %H:%M"
    headers = [
        "Feature View",
        "Materialized?",
        "Stale?",
        "Freshness",
        "Expected Freshness",
        "Created",
        "Stream?",
    ]

    freshness_data = [
        [
            ff_proto.feature_view_name,
            str(ff_proto.materialization_enabled),
            str(ff_proto.is_stale) if can_be_stale(ff_proto) else "-",
            format_seconds_into_highest_unit(ff_proto.freshness.seconds) if can_be_stale(ff_proto) else "-",
            format_seconds_into_highest_unit(ff_proto.expected_freshness.seconds) if can_be_stale(ff_proto) else "-",
            datetime.fromtimestamp(ff_proto.created_at.seconds).strftime(timestamp_format),
            str(ff_proto.is_stream),
        ]
        for ff_proto in freshness_statuses
    ]

    sort_order = {"True": 0, "False": 1, "-": 2}
    freshness_data = sorted(freshness_data, key=lambda row: sort_order[row[2]])
    table = Displayable.from_table(headings=headers, rows=freshness_data, max_width=0)
    table._text_table.set_cols_align(["c" for _ in range(len(headers))])
    return table


def get_all_freshness(workspace: str):
    request = QueryFeatureViewsRequest()
    request.workspace = workspace
    response = metadata_service.instance().QueryFeatureViews(request)
    fco_container = FcoContainer.from_proto(response.fco_container)
    fv_ids = []
    for spec in fco_container.get_root_fcos():
        if isinstance(spec, specs.MaterializedFeatureViewSpec):
            fv_ids.append(IdHelper.from_string(spec.id))

    freshness_statuses = []

    for fv_id in fv_ids:
        fresh_request = GetFeatureFreshnessRequest()
        fresh_request.fco_locator.id.CopyFrom(fv_id)
        fresh_request.fco_locator.workspace = workspace
        fresh_response = metadata_service.instance().GetFeatureFreshness(fresh_request)
        freshness_statuses.append(fresh_response.freshness_status)

    return freshness_statuses


def is_live_workspace(workspace_name: str) -> bool:
    request = GetWorkspaceRequest()
    request.workspace_name = workspace_name
    response = metadata_service.instance().GetWorkspace(request)
    return response.workspace.capabilities.materializable


def filter_internal_columns(df: pysparkDF) -> pysparkDF:
    output_columns = [f"`{c.name}`" for c in df.schema if udf_internal() not in c.name]
    return df.select(*output_columns)


def validate_request_data(
    request_data: Optional[dict],
    required_request_context_keys: List[str],
    is_read_api_v3=True,
):
    missing_keys = set(required_request_context_keys) - set(request_data.keys()) if request_data else None
    if missing_keys:
        # TODO:(read-api) remove this check and old error message once get_feature_vector is deleted
        if is_read_api_v3:
            raise errors.GET_ONLINE_FEATURES_MISSING_REQUEST_KEY(missing_keys)
        raise errors.GET_FEATURE_VECTOR_MISSING_REQUEST_KEY(missing_keys)


def plural(x: int, singular: str, plural: str):
    """
    Returns the `singular` string if `x` is equal to 1 and `plural` if not.
    """
    if x == 1:
        return singular
    else:
        return plural


def cluster_url() -> Optional[str]:
    import sys

    from tecton_core import conf

    api_service = conf.get_or_none("API_SERVICE")
    if api_service:
        # API_SERVICE URLs of the form <subdomain>.tecton.ai/api are expected so this check
        # ensures an internal DNS address isn't being used or an invalid path is specified.
        if api_service.endswith("/api") and "ingress" not in api_service:
            return api_service[: -len("/api")]
        else:
            print(f"Warning: CLI is configured with non-standard URL: {api_service}", file=sys.stderr)
            return api_service
    else:
        return None
