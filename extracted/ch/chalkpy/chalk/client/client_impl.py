from __future__ import annotations

import base64
import collections.abc
import inspect
import itertools
import json
import os
import pathlib
import random
import re
import string
import subprocess
import time
import traceback
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
from urllib.parse import urljoin

import pandas as pd
import pyarrow.feather
import requests
import requests.structures
from dateutil import parser
from requests import HTTPError
from requests.adapters import DEFAULT_POOLBLOCK, DEFAULT_POOLSIZE, DEFAULT_RETRIES, HTTPAdapter
from typing_extensions import NoReturn, override
from urllib3 import Retry

import chalk._repr.utils as repr_utils
from chalk._reporting.models import BatchReport, BatchReportResponse
from chalk._reporting.progress import ProgressService
from chalk._upload_features.utils import to_multi_upload_inputs
from chalk._version import __version__ as chalkpy_version
from chalk.client._internal_models.models import INDEX_COL_NAME, TS_COL_NAME, OfflineQueryGivensVersion
from chalk.client.client import ChalkClient
from chalk.client.dataset import (
    DatasetImpl,
    DatasetRevisionImpl,
    DatasetVersion,
    dataset_from_response,
    load_dataset,
    load_schema,
)
from chalk.client.exc import CHALK_TRACE_ID_KEY, ChalkAuthException, ChalkBaseException, ChalkCustomException
from chalk.client.models import (
    TIMEDELTA_PREFIX,
    BranchDeployRequest,
    BranchDeployResponse,
    BranchIdParam,
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    ChalkError,
    ChalkException,
    ComputeResolverOutputRequest,
    ComputeResolverOutputResponse,
    CreateOfflineQueryJobRequest,
    CreateOfflineQueryJobResponse,
    CreatePromptEvaluationRequest,
    DatasetJobStatusRequest,
    DatasetResponse,
    DatasetRevisionPreviewResponse,
    DatasetRevisionSummaryResponse,
    ErrorCode,
    ExchangeCredentialsRequest,
    ExchangeCredentialsResponse,
    FeatureDropRequest,
    FeatureDropResponse,
    FeatureObservationDeletionRequest,
    FeatureObservationDeletionResponse,
    FeatureResult,
    FeatureStatisticsResponse,
    GetIncrementalProgressResponse,
    GetOfflineQueryJobResponse,
    IngestDatasetRequest,
    MultiUploadFeaturesRequest,
    MultiUploadFeaturesResponse,
    OfflineQueryContext,
    OfflineQueryInput,
    OfflineQueryInputUri,
    OfflineQueryParquetUploadURLResponse,
    OnlineQuery,
    OnlineQueryContext,
    OnlineQueryManyRequest,
    OnlineQueryRequest,
    OnlineQueryResponse,
    OnlineQueryResponseFeather,
    OnlineQueryResultFeather,
    OutputExpression,
    PersistenceSettings,
    PingRequest,
    PingResponse,
    PlanQueryRequest,
    PlanQueryResponse,
    QueryMeta,
    ResolverReplayResponse,
    ResolverRunResponse,
    ResourceRequests,
    SetDatasetRevisionMetadataRequest,
    SetDatasetRevisionMetadataResponse,
    SetIncrementalProgressRequest,
    StreamResolverTestMessagePayload,
    StreamResolverTestRequest,
    StreamResolverTestResponse,
    TriggerResolverRunRequest,
    UploadedParquetShardedOfflineQueryInput,
    UploadFeaturesRequest,
    UploadFeaturesResponse,
    WhoAmIResponse,
)
from chalk.client.response import Dataset, FeatureReference, OnlineQueryResult
from chalk.client.serialization.query_serialization import MULTI_QUERY_MAGIC_STR, write_query_to_buffer
from chalk.config.auth_config import load_token
from chalk.config.project_config import load_project_config
from chalk.features import (
    DataFrame,
    Feature,
    FeatureNotFoundException,
    FeatureWrapper,
    ensure_feature,
    live_updates,
    unwrap_feature,
)
from chalk.features._encoding.inputs import recursive_encode_inputs, validate_iterable_values_in_mapping
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import Features, is_feature_set_class
from chalk.features.pseudofeatures import CHALK_TS_FEATURE
from chalk.features.resolver import Resolver
from chalk.features.tag import BranchId, DeploymentId, EnvironmentId
from chalk.importer import CHALK_IMPORT_FLAG
from chalk.parsed._proto.utils import encode_proto_to_b64
from chalk.parsed.branch_state import BranchGraphSummary
from chalk.prompts import Prompt
from chalk.queries.query_context import ContextJsonDict, JsonValue
from chalk.utils import notebook
from chalk.utils.collections import FrozenOrderedSet
from chalk.utils.df_utils import chunk_table, pa_table_to_pl_df
from chalk.utils.duration import parse_chalk_duration, timedelta_to_duration
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.string import s

if TYPE_CHECKING:
    import ssl

    import polars as pl
    import pyarrow as pa
    from pydantic import BaseModel, ValidationError

    from chalk.client._internal_models.check import Result

    QueryInput = Union[Mapping[FeatureReference, Any], pd.DataFrame, pl.DataFrame, DataFrame]
    QueryInputTime = Union[Sequence[datetime], datetime, None]
else:
    try:
        from pydantic.v1 import BaseModel, ValidationError
    except ImportError:
        from pydantic import BaseModel, ValidationError


_logger = get_logger(__name__)

T = TypeVar("T")


class _ChalkHTTPException(BaseModel):
    detail: str
    trace: Optional[str] = None
    errors: Optional[List[ChalkError]] = None


class _BranchDeploymentInfo(BaseModel):
    deployment_id: str
    created_at: datetime


class _BranchInfo(BaseModel):
    name: str
    latest_deployment: Optional[str]
    latest_deployment_time: Optional[datetime]
    deployments: List[_BranchDeploymentInfo]


class _BranchMetadataResponse(BaseModel):
    branches: List[_BranchInfo]

    def __str__(self):
        def _make_line(info: _BranchInfo) -> str:
            latest_str = ""
            if info.latest_deployment_time and info.latest_deployment_time:
                latest_str = f" -- latest: {info.latest_deployment_time.isoformat()} ({info.latest_deployment})"
            return f"* `{info.name}`:\t{len(info.deployments)} deployments" + latest_str

        return "\n".join(_make_line(bi) for bi in self.branches)


def _do_query_errors_match(
    actual: FrozenOrderedSet[ChalkError],
    expected: FrozenOrderedSet[ChalkError],
) -> bool:
    return actual == expected


def _do_resultsets_match(
    actual: Sequence[Any],
    expected: Sequence[Any],
) -> bool:
    if len(actual) != len(expected):
        return False
    for a in actual:
        matched = False
        for i, e in enumerate(expected):
            if _does_result_match(a, e):
                matched = True
                expected = [x for j, x in enumerate(expected) if j != i]
                break
        if not matched:
            return False
    return True


def _get_caller(frames: int = 1) -> Optional[str]:
    frames += 1
    frame = inspect.currentframe()
    for _ in range(frames):
        if frame:
            frame = frame.f_back
    if frame:
        return f"{frame.f_code.co_filename}:{frame.f_lineno}"
    return "<unknown>"


def _fail_test(message: str, frames: int = 1) -> NoReturn:
    caller = _get_caller(frames=frames + 1)
    try:
        import pytest
    except ImportError:
        pytest = None

    if pytest and caller:
        pytest.fail(f"{caller}: {message}", pytrace=False)
    elif pytest:
        pytest.fail(message)

    raise AssertionError(f"{caller}: {message}")


def _does_result_match(
    a: Result,
    e: Result,
    float_rel_tolerance: float = 1e-6,
    float_abs_tolerance: float = 1e-12,
) -> bool:
    try:
        import polars as pl
        import polars.testing as pl_test
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    if a.fqn != e.fqn:
        return False
    elif a.pkey != e.pkey:
        return False
    elif a.cache_hit != e.cache_hit:
        return False
    elif isinstance(e.error, ErrorCode):
        # If all we expect is an error code, then match the error code
        return isinstance(a.error, ChalkError) and a.error.code == e.error
    elif e.error is not None:
        assert isinstance(e.error, ChalkError), f"Failed to validate result: the error {e.error} must be a ChalkError!"
        return a.error == e.error
    elif a.error is not None:
        # If no error is expected, then there must not have been an error, and the values must match
        return False

    expected_value = e.value
    if isinstance(expected_value, DataFrame):
        expected_value = expected_value.to_polars().collect()
    if isinstance(a.value, pl.DataFrame) and isinstance(expected_value, pl.DataFrame):
        try:
            pl_test.assert_frame_equal(
                a.value,
                expected_value,
                check_column_order=False,
                check_row_order=False,
            )
        except AssertionError as exc:
            print(exc)
            return False
        else:
            return True
    elif not isinstance(a.value, pl.DataFrame) and not isinstance(expected_value, pl.DataFrame):
        maybe_feature = Feature.from_root_fqn(a.fqn)
        if maybe_feature.is_feature_time or maybe_feature.is_scalar:
            converter = maybe_feature.converter
            if maybe_feature.is_has_many_subfeature:
                try:
                    expected_value = sorted(converter.from_rich_to_json(v) for v in expected_value)  # type: ignore

                except TypeError:
                    expected_value = sorted(
                        [converter.from_rich_to_json(v) for v in expected_value],  # type: ignore
                        key=json.dumps,
                    )
            else:
                expected_value = converter.from_rich_to_json(expected_value, missing_value_strategy="allow")
        if isinstance(a.value, float) and isinstance(expected_value, (float, int)):
            return (
                # short circuit for float comparison
                (a.value == expected_value)
                # If you specify both `float_rel_tolerance` and `float_abs_tolerance`,
                # the numbers will be considered equal if either tolerance is met.
                or (abs(a.value - expected_value) <= float_abs_tolerance)
                or (abs(a.value - expected_value) <= float_rel_tolerance * max(abs(a.value), abs(expected_value)))
            )
        return a.value == expected_value
    return False


def _validate_offline_query_inputs(
    inputs: Mapping[Union[str, Feature, Any], Any],
) -> Mapping[Union[str, Feature, Any], Any]:
    if len(inputs) == 0:
        return inputs

    def _is_scalar(v: Any):
        return not isinstance(v, collections.abc.Iterable) or isinstance(v, str)

    scalar_values = {k: v for (k, v) in inputs.items() if _is_scalar(v)}
    if len(scalar_values) == len(inputs):
        return {str(k): [v] for (k, v) in inputs.items()}
    elif len(scalar_values) > 0:
        first_key = next(iter(scalar_values.keys()))
        error_msg = (
            f"Failed to parse query inputs: offline_query() expects multiple input values for each feature. "
            f"Found a single value of type {type(inputs[first_key])} for key '{str(first_key)}'."
        )
        raise ValueError(error_msg)
    else:
        validated_inputs = {str(k): v for (k, v) in inputs.items()}
        length = None
        for k, v in validated_inputs.items():
            if length is None:
                length = len(list(v))
            elif length != len(list(v)):
                raise ChalkBaseException(
                    errors=[
                        ChalkError.create(
                            code=ErrorCode.VALIDATION_FAILED,
                            message=(
                                f"This query specified {length} output row{s(length)}, "
                                + f"but the `{k}` argument contains {len(list(v))} value{s(len(list(v)))}."
                            ),
                        )
                    ],
                )
        return validated_inputs


def _get_column_names(query_input: QueryInput) -> List[str]:
    """
    Get a list of output column names from a QueryInput object
    """
    try:
        import polars as pl
        import pyarrow as pa
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    input_table: pa.Table | pa.RecordBatch
    if isinstance(query_input, DataFrame):
        input_table = query_input.to_pyarrow()
    elif isinstance(query_input, pl.DataFrame):
        input_table = query_input.to_arrow()
    elif isinstance(query_input, pd.DataFrame):
        input_table = pl.from_pandas(query_input).to_arrow()
    elif isinstance(query_input, pa.Table):
        input_table = query_input
    elif isinstance(query_input, collections.abc.Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
        input_table = pl.DataFrame(_validate_offline_query_inputs(query_input)).to_arrow()
    else:
        input_table = pl.from_pandas(pd.DataFrame(query_input)).to_arrow()
    return input_table.column_names


def _offline_query_inputs_to_parquet(
    offline_query_inputs: Sequence[tuple[QueryInput, QueryInputTime]],
) -> List[pa.Table]:
    """
    Convert a list of OfflineQueryInput objects to a list of pyarrow Tables in the format
    OfflineQueryGivensVersion.SINGLE_TS_COL_NAME_WITH_URI_PREFIX
    """
    try:
        import polars as pl
        import pyarrow as pa
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    offset = 0
    tables: List[pa.Table] = []
    for single_input, single_input_times in offline_query_inputs:
        input_table: pa.Table | pa.RecordBatch
        if isinstance(single_input, DataFrame):
            input_table = single_input.to_pyarrow()
        elif isinstance(single_input, pl.DataFrame):
            input_table = single_input.to_arrow()
        elif isinstance(single_input, pd.DataFrame):
            input_table = pl.from_pandas(single_input).to_arrow()
        elif isinstance(single_input, pa.Table):
            input_table = single_input
        elif isinstance(single_input, collections.abc.Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
            input_table = pl.DataFrame(_validate_offline_query_inputs(single_input)).to_arrow()
        else:
            input_table = pl.from_pandas(pd.DataFrame(single_input)).to_arrow()
        fields: List[pa.Field] = []
        for i, column_fqn in enumerate(input_table.column_names):
            try:
                f = Feature.from_root_fqn(column_fqn)
            except FeatureNotFoundException:
                field = input_table.schema.field(i)
            else:
                field = pa.field(column_fqn, f.converter.pyarrow_dtype)
            try:
                input_table.column(i).cast(field.type)
            except Exception as e:
                raise ValueError(
                    f"Could not cast column '{column_fqn}' of original type '{input_table.schema.field(i).type}' to feature type '{field.type}': {e}"
                )
            fields.append(field)
        schema = pa.schema(fields)
        input_table = input_table.cast(schema)

        if single_input_times is None:
            single_input_times = datetime.now(timezone.utc)
        if isinstance(single_input_times, datetime):
            single_input_times = [single_input_times for _ in range(len(input_table))]
        local_tz = datetime.now(timezone.utc).astimezone().tzinfo

        single_input_times = [x.replace(tzinfo=local_tz) if x.tzinfo is None else x for x in single_input_times]
        single_input_times = [x.astimezone(timezone.utc) for x in single_input_times]

        if TS_COL_NAME not in input_table.column_names:
            if len(single_input_times) != len(input_table):
                raise ChalkBaseException(
                    errors=[
                        ChalkError.create(
                            code=ErrorCode.VALIDATION_FAILED,
                            message=(
                                f"This query specified {len(input_table)} output row{s(len(input_table))}, "
                                + f"but the `input_times` argument contains {len(single_input_times)} value{s(len(single_input_times))}."
                            ),
                        )
                    ],
                )
            input_table = input_table.append_column(
                TS_COL_NAME, pa.array(single_input_times, pa.timestamp("us", "UTC"))
            )
        input_table = input_table.append_column(
            INDEX_COL_NAME, pa.array(range(offset, offset + len(input_table)), type=pa.int64())
        )

        offset += len(input_table)
        tables.append(input_table if isinstance(input_table, pa.Table) else pa.Table.from_batches([input_table]))
    return tables


def _to_offline_query_input(
    input: QueryInput,
    input_times: QueryInputTime,
) -> OfflineQueryInput:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(input, (DataFrame, pl.DataFrame)):
        input = input.to_pandas()
    if isinstance(input, collections.abc.Mapping):
        input = _validate_offline_query_inputs(input)
    pd_dataframe: pd.DataFrame
    if isinstance(input, pd.DataFrame):
        pd_dataframe = input
    else:
        pd_dataframe = pd.DataFrame(cast(Any, input))

    columns = pd_dataframe.columns
    matrix: List[List[Any]] = pd_dataframe.T.values.tolist()

    columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]
    if input_times is None:
        input_times = datetime.now(timezone.utc)
    if isinstance(input_times, datetime):
        input_times = [input_times for _ in range(len(pd_dataframe))]
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo

    matrix.append(
        [(x.replace(tzinfo=local_tz) if x.tzinfo is None else x).astimezone(timezone.utc) for x in input_times]
    )

    for col_index, column in enumerate(matrix):
        for row_index, value in enumerate(column):
            try:
                f = Feature.from_root_fqn(columns_fqn[col_index])
            except FeatureNotFoundException:
                # The feature is not in the graph, so passing the value as-is and hoping it's possible
                # to json-serialize it
                encoded_feature = value
            else:
                encoded_feature = f.converter.from_rich_to_json(
                    value,
                    missing_value_strategy="error",
                )

            matrix[col_index][row_index] = encoded_feature

    return OfflineQueryInput(
        columns=columns_fqn,
        values=matrix,
    )


def _upload_table_parquet(
    table: pa.Table,
    url: str,
) -> None:
    try:
        import pyarrow.parquet as pq
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    written_bytes = BytesIO()
    pq.write_table(table, written_bytes)
    written_bytes.seek(0)
    if url.startswith("file://"):
        # for locally uploaded input parquet files to work
        full_path = pathlib.Path(url[len("file://") :])
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(written_bytes.getvalue())
            return
    resp = requests.put(url, data=written_bytes)
    resp.raise_for_status()


def _convert_datetime_param(
    param_name: Literal["lower_bound", "upper_bound"], param: datetime | str | None
) -> datetime | None:
    """Takes an API parameter representing an optional datetime value and converts it into a datetime object."""
    if param is None:
        return None

    if isinstance(param, str):
        # Note: If the ISO 8601 string doesn't contain a timezone, we assume the timezone is UTC.
        # This is different behavior from the original datetime param, which tries to infer the caller's local timezone.
        # Going forward, we want to always assume UTC when no timezone is provided.
        # However, to maintain backwards compatibility, datetime-type params will continue to infer local timezone.
        try:
            param = datetime.fromisoformat(param)
        except ValueError:
            raise ValueError(
                f'Passed {param_name}="{param}", but {param_name} expects a datetime string in ISO 8601 format.'
            )

        if param.tzinfo is None:
            # Don't convert the datetime object with "astimezone", just slap on UTC timezone without changing the numbers
            return param.replace(tzinfo=timezone.utc)
        return param
    elif param.tzinfo is None:
        # Infer local timezone when the parameter is passed as a datetime object with no timezone
        return param.astimezone()

    return param


def _convert_datetime_or_timedelta_param(
    param_name: Literal["lower_bound", "upper_bound"], param: datetime | timedelta | str | None
):
    if isinstance(param, timedelta):
        return param
    try:
        return _convert_datetime_param(param_name, param)
    except ValueError:
        try:
            return parse_chalk_duration(cast(str, param))
        except ValueError:
            raise ValueError(
                f'Passed {param_name}="{param}", but {param_name} should be a datetime string or duration.'
            )


def _validate_context_dict(data: Any) -> ContextJsonDict | None:
    if data is None:
        return None
    if isinstance(data, str):
        data = json.loads(data)
    if not isinstance(data, collections.abc.Mapping):
        raise TypeError(f"Query context must be a mapping, got {type(data)}")
    for key, value in data.items():
        if not isinstance(key, str):
            raise TypeError(f"Context keys must be strings, got {type(key)}")
        if not isinstance(value, (str, int, float, bool, type(None))):
            raise TypeError(
                f"Invalid type for value at key '{key}': {type(value)}. Must be str, int, float, bool, or None."
            )
    return dict(data)


class _ChalkHTTPAdapter(HTTPAdapter):
    """
    Allows for customization such as specifying an SSLContext for all requests.
    """

    def __init__(
        self,
        pool_connections: int = DEFAULT_POOLSIZE,
        pool_maxsize: int = DEFAULT_POOLSIZE,
        max_retries: int | Retry = DEFAULT_RETRIES,
        pool_block: bool = DEFAULT_POOLBLOCK,
        ssl_context: ssl.SSLContext | None = None,
    ):
        self.ssl_context = ssl_context
        super().__init__(
            pool_connections=pool_connections, pool_maxsize=pool_maxsize, max_retries=max_retries, pool_block=pool_block
        )

    def init_poolmanager(self, connections: int, maxsize: int, block: bool = DEFAULT_POOLBLOCK, **pool_kwargs: Any):
        if self.ssl_context is not None:
            pool_kwargs["ssl_context"] = self.ssl_context
        return super().init_poolmanager(connections, maxsize, block, **pool_kwargs)


window_function_regex = re.compile(r"^(.*)__(\d+)__$")


def render_fqn(name: str) -> str:
    if name.endswith("__all__"):
        return f"{name[:-7]}[all]"

    window_match = window_function_regex.match(name)

    if window_match:
        base_name, seconds_str = window_match.groups()
        seconds = int(seconds_str)

        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        time_parts: List[str] = []
        if days > 0:
            time_parts.append(f"{days}d")
        if hours > 0:
            time_parts.append(f"{hours}h")
        if minutes > 0:
            time_parts.append(f"{minutes}m")
        if seconds > 0:
            time_parts.append(f"{seconds}s")

        time_str = "".join(time_parts)
        name = f"{base_name}[{time_str}]"

    return name


class OnlineQueryResponseImpl(OnlineQueryResult):
    data: List[FeatureResult]
    warnings: List[str]
    meta: Optional[QueryMeta]

    def __init__(
        self,
        data: List[FeatureResult],
        errors: List[ChalkError],
        warnings: List[str],
        meta: Optional[QueryMeta] = None,
    ):
        super().__init__()
        self.data = data
        self.errors = errors
        self.warnings = warnings
        self.meta = meta

        for d in self.data:
            if d.value is not None:
                try:
                    f = Feature.from_root_fqn(d.field)
                except FeatureNotFoundException:
                    self.warnings.append(
                        f"Return data {d.field}:{d.value} cannot be decoded. Attempting to JSON decode"
                    )
                else:
                    if f.is_has_many:
                        if isinstance(d.value, dict):
                            # Has-manys are returned by the HTTP server in a columnar format, i.e.:
                            # {"columns": ["book.id", "book.title"], "values": [[1, 2], ["Dune", "Children of Dune"]]}
                            # FeatureConverter expects a list of structs, i.e.:
                            # [{"book.id": 1, "book.title": "Dune"}, {"book.id": 2, "book.title": "Children of Dune"}]
                            cols = d.value["columns"]
                            vals = d.value["values"]
                            vals_flattened = list(zip(*vals))
                            d.value = f.converter.from_json_to_rich(
                                [{k: v for k, v in zip(cols, row)} for row in vals_flattened]
                            )
                        elif isinstance(d.value, list):
                            d.value = f.converter.from_json_to_rich(d.value)
                        else:
                            raise ValueError(f"Unexpected value format for has-many feature {f}: {d.value}")

                    elif f.is_has_many_subfeature:
                        # TODO we might need mulitple levels of nesting for has-many-has-many's
                        assert isinstance(d.value, collections.abc.Iterable)
                        d.value = [f.converter.from_json_to_rich(v) for v in d.value]
                    else:
                        d.value = f.converter.from_json_to_rich(d.value)

        self._values = {d.field: d for d in self.data}

    def _df_repr(self) -> List[Dict[str, Any]]:
        return [{"Feature": x.field, "Value": repr_utils.get_repr_value(x.value)} for x in self.data]

    def _repr_html_(self):
        values = self.to_dict(prefix=False)
        df_html = (
            pd.DataFrame(
                {
                    "Feature": [render_fqn(k) for k in values.keys()],
                    "Value": [v for v in values.values()],
                }
            )._repr_html_()  # pyright: ignore[reportPrivateUsage]
            or ""
        )

        errors_html = ""
        if self.errors:
            errors_html = (
                "<br />"
                + "<h4>Errors</h4>"
                + "<ul>"
                + "\n".join([f"<li>{e.code.value}: {e.message}</li>" for e in self.errors])
                + "</ul>"
            )
        return f"{df_html}{errors_html}"

    def __repr__(self) -> str:
        lines: List[str] = []
        for e in self.errors or []:
            nice_code = str(e.code.value).replace("_", " ").capitalize()
            # {str(e.category.value).capitalize()}
            lines.append(
                f"### {nice_code}{e.feature and f' ({e.feature})' or ''}{e.resolver and f' ({e.resolver})' or ''}"
            )
            lines.append(e.message)
            lines.append("")

            metadata = {
                "Exception Kind": e.exception and e.exception.kind,
                "Exception Message": e.exception and e.exception.message,
                "Stacktrace": e.exception and e.exception.stacktrace,
            }
            metadata = {k: v for k, v in metadata.items() if v is not None}
            for k, v in metadata.items():
                lines.append(f"*{k}*")
                lines.append("")
                lines.append(v)
        errs = "\n".join(lines)

        try:
            return repr(pd.DataFrame(self._df_repr())) + "\n" + errs
        except:
            return f"{json.dumps(self.to_dict(), sort_keys=True, indent=4)}\n{errs}"

    def __str__(self):
        lines: List[str] = []
        for e in self.errors or []:
            nice_code = str(e.code.value).replace("_", " ").capitalize()
            # {str(e.category.value).capitalize()}
            lines.append(
                f"### {nice_code}{e.feature and f' ({e.feature})' or ''}{e.resolver and f' ({e.resolver})' or ''}"
            )
            lines.append(e.message)
            lines.append("")

            metadata = {
                "Exception Kind": e.exception and e.exception.kind,
                "Exception Message": e.exception and e.exception.message,
                "Stacktrace": e.exception and e.exception.stacktrace,
            }
            metadata = {k: v for k, v in metadata.items() if v is not None}
            for k, v in metadata.items():
                lines.append(f"*{k}*")
                lines.append("")
                lines.append(v)
        errs = "\n".join(lines)
        try:
            return str(pd.DataFrame(self._df_repr())) + "\n" + errs
        except:
            return f"{json.dumps(self.to_dict(), sort_keys=True, indent=4)}\n{errs}"

    def _repr_markdown_(self):
        lines: List[str] = []
        if self.errors is not None and len(self.errors) > 0:
            lines.append(f"## {len(self.errors)} Errors")
            lines.append("")
            for e in self.errors:
                nice_code = str(e.code.value).replace("_", " ").capitalize()
                # {str(e.category.value).capitalize()}
                lines.append(
                    f"### {nice_code}{e.feature and f' ({e.feature})' or ''}{e.resolver and f' ({e.resolver})' or ''}"
                )
                lines.append(e.message)
                lines.append("")

                metadata = {
                    "Exception Kind": e.exception and e.exception.kind,
                    "Exception Message": e.exception and e.exception.message,
                    "Stacktrace": e.exception and e.exception.stacktrace,
                }
                metadata = {k: v for k, v in metadata.items() if v is not None}
                for k, v in metadata.items():
                    lines.append(f"*{k}*")
                    lines.append("")
                    lines.append(v)
        main = "\n"
        if len(self.data) > 0:
            import polars as pl

            lines.append("")
            try:
                content = str(pl.DataFrame(self._df_repr()))
                split = content.split("\n")
                main = "\n".join(itertools.chain(split[1:3], split[5:]))
            except:
                try:
                    import pandas as pd

                    content = str(pd.DataFrame(self._df_repr()))
                    split = content.split("\n")
                    main = "\n".join(itertools.chain(split[1:3], split[5:]))
                except:
                    main = json.dumps(self.to_dict(), sort_keys=True, indent=4)
        lines.append("## Features")
        lines.append("```")
        lines.append(main)
        lines.append("```")
        return "\n".join(lines)

    def get_feature(self, feature: Any) -> Optional[FeatureResult]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        return self._values.get(str(feature))

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        v = self.get_feature(feature)
        return v and v.value

    def to_dict(self, prefix: bool = True) -> Dict[str, Any]:
        if prefix:
            return {f.field: f.value for f in self.data}
        return {f.field.split(".", maxsplit=2)[-1]: f.value for f in self.data}


def _get_overlay_graph_b64() -> str | None:
    overlay_graph = live_updates.build_overlay_graph()
    overlay_graph_b64: str | None = None
    if overlay_graph is not None:
        overlay_graph_b64 = encode_proto_to_b64(overlay_graph, deterministic=True)
    return overlay_graph_b64


class ChalkAPIClientImpl(ChalkClient):
    __name__ = "ChalkClient"
    __qualname__ = "chalk.client.ChalkClient"

    latest_client: Optional[ChalkAPIClientImpl] = None

    def __repr__(self):
        branch_text = ""
        if self._branch is not None:
            branch_text = f", branch='{self._branch}'"
        return f"chalk.client.ChalkClient<{branch_text}>"

    def __new__(cls, *args: Any, **kwargs: Any) -> ChalkAPIClientImpl:
        return object.__new__(ChalkAPIClientImpl)

    def __init__(  # pyright: ignore[reportMissingSuperCall]
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        api_server: Optional[str] = None,
        query_server: Optional[str] = None,
        branch: Optional[BranchId] | Literal[True] = None,
        deployment_tag: Optional[str] = None,
        preview_deployment_id: Optional[DeploymentId] = None,
        _skip_cache: bool = False,
        session: Optional[requests.Session] = None,
        additional_headers: Optional[Mapping[str, str]] = None,
        default_job_timeout: float | timedelta | None = None,
        default_request_timeout: float | timedelta | None = None,
        default_connect_timeout: float | timedelta | None = None,
        local: bool = False,
        ssl_context: ssl.SSLContext | None = None,
    ):
        if CHALK_IMPORT_FLAG.get() is True:
            raise RuntimeError(
                "Attempting to instantiate a Chalk client while importing source modules is forbidden. "
                + "Please exclude this file from import using your `.chalkignore` file "
                + "(see https://docs.chalk.ai/cli/apply), or wrap this query in a function that is not called upon import."
            )

        self.default_status_report_timeout = timedelta(minutes=10)

        if default_job_timeout is not None and isinstance(default_job_timeout, timedelta):
            default_job_timeout = default_job_timeout.total_seconds()
        self.default_job_timeout = default_job_timeout

        if default_request_timeout is not None and isinstance(default_request_timeout, timedelta):
            default_request_timeout = default_request_timeout.total_seconds()
        self.default_request_timeout = default_request_timeout

        if default_connect_timeout is not None and isinstance(default_connect_timeout, timedelta):
            default_connect_timeout = default_connect_timeout.total_seconds()
        self.default_connect_timeout = default_connect_timeout

        if session is None:
            session = requests.Session()
            retries = Retry(connect=3, read=3)
            session.mount("https://", _ChalkHTTPAdapter(max_retries=retries, ssl_context=ssl_context))
            session.mount("http://", HTTPAdapter(max_retries=retries))

        self.session = session

        if local and branch is None:
            branch = "chalk_local_" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        if branch is not None and deployment_tag is not None:
            raise ValueError("Cannot specify both `branch` and `deployment_tag`.")

        if branch is True:
            # pick up the local git branch
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    stdout=subprocess.PIPE,
                    text=True,
                    check=True,
                )
                branch = result.stdout.strip().replace("/", "-")
            except subprocess.CalledProcessError as e:
                raise ValueError(
                    "Could not find the current git branch from the working directory. "
                    + "Try running this script from your git repository. "
                    + e.stderr
                )

        self._preview_deployment_id: str | None = preview_deployment_id
        self._client_id: str | None = client_id
        self._deployment_tag: str | None = deployment_tag
        self._client_secret: str | None = client_secret
        self._query_server: str | None = query_server
        self._branch: str | None = branch
        self._skip_token_cache: bool = _skip_cache
        self._api_server: str | None = api_server

        self._default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"chalkpy-{chalkpy_version}",
            "X-Chalk-Features-Versioned": "true",
        }
        if additional_headers:
            self._default_headers.update(additional_headers)

        self._primary_environment = environment

        self.__class__.latest_client = self
        if notebook.is_notebook():
            if local:
                raise ValueError("Cannot use local mode in a notebook")

            # Register Cell Magics
            self._register_cell_magics()

            if branch is None:
                self.whoami()

            else:
                self._load_branches(timeout=...)

        if local:
            if branch is None:
                raise ValueError("Cannot use local mode without a branch")

            chalklocal = os.path.expanduser("~/.chalk/bin/chalk")
            if not os.path.exists(chalklocal):
                raise FileNotFoundError("Chalk CLI not found in ~/.chalk/bin/chalk, so cannot local apply")

            result = subprocess.run(
                [chalklocal, "apply", "--branch", branch],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Failed to apply branch '{branch}' using local source. Underlying error:\n {result.stderr}\n{result.stdout}"
                )

    def _exchange_credentials(self):
        _logger.debug("Performing a credentials exchange")
        if self._client_id is None or self._client_secret is None or self._api_server is None:
            token = load_token(
                client_id=self._client_id,
                client_secret=self._client_secret,
                active_environment=self._primary_environment,
                api_server=self._api_server,
                skip_cache=self._skip_token_cache,
            )
            if token is None:
                raise ChalkAuthException()
            self._client_id = token.clientId
            self._client_secret = token.clientSecret
            assert token.apiServer is not None, "load_token always provides a valid apiServer"
            self._api_server = token.apiServer
            self._primary_environment = token.activeEnvironment

        resp = self.session.request(
            method="post",
            url=urljoin(self._api_server, "v1/oauth/token"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=ExchangeCredentialsRequest(
                client_id=self._client_id,
                client_secret=self._client_secret,
                grant_type="client_credentials",
            ).dict(),
            timeout=self.default_request_timeout,
        )
        resp.raise_for_status()
        response_json = resp.json()
        try:
            creds = ExchangeCredentialsResponse(**response_json)
        except ValidationError:
            raise HTTPError(response=resp)
        self._default_headers["Authorization"] = f"Bearer {creds.access_token}"
        # FIXME: We should NOT be using the X-Chalk-Client-Id for anything, as it is NOT authenticated
        self._default_headers["X-Chalk-Client-Id"] = self._client_id
        if self._primary_environment is None:
            self._primary_environment = creds.primary_environment

    def _get_headers(
        self,
        environment_override: Optional[str],
        preview_deployment_id: str | None | ellipsis,
        branch: str | None | ellipsis,
    ) -> MutableMapping[str, str]:
        x_chalk_env_id = environment_override or self._primary_environment
        headers: MutableMapping[str, str] = requests.structures.CaseInsensitiveDict()
        headers.update(self._default_headers)  # shallow copy
        if x_chalk_env_id is not None:
            headers["X-Chalk-Env-Id"] = x_chalk_env_id
        if self._deployment_tag is not None:
            headers["X-Chalk-Deployment-Tag"] = self._deployment_tag
        if preview_deployment_id is ...:
            if self._preview_deployment_id is not None:
                headers["X-Chalk-Preview-Deployment"] = self._preview_deployment_id
        elif preview_deployment_id is not None:
            headers["X-Chalk-Preview-Deployment"] = preview_deployment_id
        if branch is ...:
            if self._branch is not None:
                headers["X-Chalk-Branch-Id"] = self._branch
        elif branch is not None:
            headers["X-Chalk-Branch-Id"] = branch
        return headers

    @staticmethod
    def _raise_if_200_with_errors(response: BaseModel):
        errors = getattr(response, "errors", None)
        if errors and isinstance(errors, list) and all(isinstance(e, ChalkError) for e in errors):
            errors = cast(List[ChalkError], errors)
            raise ChalkBaseException(errors=errors)

    @staticmethod
    def _raise_if_200_with_non_resolver_errors(response: BaseModel):
        errors = getattr(response, "errors", None)
        if errors and isinstance(errors, list) and all(isinstance(e, ChalkError) for e in errors):
            if any(not e.is_resolver_runtime_error() for e in errors):
                errors = cast(List[ChalkError], errors)
                raise ChalkBaseException(errors=errors)
            else:
                # Do nothing: we want to maintain the dataset with the resolver errors, but we should inform the user!
                message = """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: One or more resolvers failed to run. This
is very likely not a problem with Chalk, but rather
your resolvers. You can debug your resolvers through
use of the 'resolver_replay' functionality:
https://docs.chalk.ai/docs/debugging-queries#resolver-replay
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
                if notebook.is_notebook():
                    print(message)
                else:
                    _logger.info(message)

    @staticmethod
    def _raise_if_http_error(response: requests.Response, environment_override_warning: bool = False):
        if response.status_code < 400:
            return

        if response.status_code == 403 and environment_override_warning:
            raise ChalkBaseException(
                errors=None, detail="403: Cannot override environment when `client_id` and `client_secret` are set."
            )

        def _standardized_raise():
            try:
                standardized_exception = _ChalkHTTPException.parse_obj(response.json())
            except Exception:
                pass
            else:
                raise ChalkBaseException(
                    errors=standardized_exception.errors,
                    trace_id=standardized_exception.trace,
                    detail=standardized_exception.detail,
                )

        def _fallback_raise():
            trace_id = None
            if hasattr(response, "headers"):
                trace_id = response.headers.get(CHALK_TRACE_ID_KEY)

            detail = response.text
            try:
                response_json = response.json()
                if isinstance(response_json, Mapping):
                    detail = response_json.get("detail", detail)
            except requests.exceptions.JSONDecodeError:
                pass

            status_code = response.status_code
            known_error_code = None
            if status_code == 401:
                known_error_code = ErrorCode.UNAUTHENTICATED
            elif status_code == 403:
                known_error_code = ErrorCode.UNAUTHORIZED

            chalk_error = ChalkError.create(
                code=known_error_code or ErrorCode.INTERNAL_SERVER_ERROR,
                message=f"{status_code} {detail}",
            )
            raise ChalkBaseException(errors=[chalk_error], trace_id=trace_id)

        _standardized_raise()
        _fallback_raise()

    @overload
    def _request(
        self,
        method: str,
        uri: str,
        response: None,
        json: Optional[BaseModel],
        *,
        environment_override: Optional[str],
        preview_deployment_id: Optional[str],
        branch: Optional[Union[BranchId, ellipsis]],
        data: Optional[bytes] = None,
        metadata_request: bool = True,
        extra_headers: Mapping[str, str] | None = None,
        timeout: float | None | ellipsis = ...,
        connect_timeout: float | None | ellipsis = ...,
    ) -> requests.Response:
        ...

    @overload
    def _request(
        self,
        method: str,
        uri: str,
        response: Type[T],
        json: Optional[BaseModel],
        *,
        environment_override: Optional[str],
        preview_deployment_id: str | None | ellipsis,
        branch: str | None | ellipsis,
        data: Optional[bytes] = None,
        metadata_request: bool = True,
        extra_headers: Mapping[str, str] | None = None,
        timeout: float | None | ellipsis = ...,
        connect_timeout: float | None | ellipsis = ...,
    ) -> T:
        ...

    def _do_request_inner(
        self,
        method: str,
        uri: str,
        json: Optional[BaseModel],
        *,
        host: str,
        environment_override: str | None,
        preview_deployment_id: str | None | ellipsis,
        extra_headers: Mapping[str, str] | None,
        metadata_request: bool,
        branch: str | None | ellipsis,
        data: Optional[bytes] = None,
        timeout: float | None | ellipsis,
        connect_timeout: float | None | ellipsis,
    ):
        json_body = json and json.dict()
        headers = self._get_headers(
            environment_override=environment_override,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        if extra_headers:
            headers.update(extra_headers)
        if (
            "X-Chalk-Branch-Id" in headers
            and isinstance(json, CreateOfflineQueryJobRequest)
            and json.use_multiple_computers
        ):
            del headers["X-Chalk-Branch-Id"]

        url = urljoin(host, uri)
        if (
            not env_var_bool("CHALK_SKIP_BRANCH_SERVER_STATUS_CHECK")
            and headers.get("X-Chalk-Branch-Id")
            and headers.get("X-Chalk-Env-Id")
            and self._api_server is not None
        ):
            status_url = urljoin(self._api_server, "/v1/branches/start")
            status_headers = dict(self._default_headers)
            status_headers["X-Chalk-Env-Id"] = headers["X-Chalk-Env-Id"]
            # Use the same timeout logic for branch server checks
            if timeout is ...:
                branch_timeout = self.default_request_timeout
            else:
                branch_timeout = timeout
            if connect_timeout is ...:
                branch_connect_timeout = self.default_connect_timeout
            else:
                branch_connect_timeout = connect_timeout

            if branch_connect_timeout is not None and branch_timeout is not None:
                branch_timeout_value = (branch_connect_timeout, branch_timeout)
            elif branch_timeout is not None:
                branch_timeout_value = branch_timeout
            elif branch_connect_timeout is not None:
                branch_timeout_value = (branch_connect_timeout, branch_connect_timeout)
            else:
                branch_timeout_value = None

            r = self.session.request(
                method="POST", headers=status_headers, url=status_url, timeout=branch_timeout_value
            )
            # Only loop if the branch server needs to be started
            try:
                resp_json = r.json()
            except requests.exceptions.JSONDecodeError as e:
                r.raise_for_status()
                raise ValueError(f"Unexpected response when starting branch server: {r.text}") from e
            if resp_json.get("status") == "error":
                print(
                    "The branch server is offline. Starting the server is expected to take 2 minutes but could take longer.\n"
                )
                from tqdm import tqdm

                with tqdm(total=0, desc="Starting branch server") as pbar:
                    for _ in range(90):
                        r = self.session.request(
                            method="POST", headers=status_headers, url=status_url, timeout=branch_timeout_value
                        )
                        try:
                            resp_json = r.json()
                        except requests.exceptions.ConnectionError:
                            resp_json = {}
                        except requests.exceptions.JSONDecodeError as e:
                            r.raise_for_status()
                            raise ValueError(f"Unexpected response when starting branch server: {r.text}") from e
                        if resp_json.get("status") == "ok":
                            break
                        else:
                            time.sleep(4)
                            pbar.update()
                print()
                if resp_json.get("status") != "ok":
                    raise ChalkCustomException("The branch server did not start. Retry your query.")

                print("The branch server is online.\n")

        if timeout is ...:
            timeout = self.default_request_timeout
        if connect_timeout is ...:
            connect_timeout = self.default_connect_timeout

        # If both connect_timeout and timeout are specified, use a tuple
        if connect_timeout is not None and timeout is not None:
            timeout_value = (connect_timeout, timeout)
        elif timeout is not None:
            timeout_value = timeout
        elif connect_timeout is not None:
            # If only connect_timeout is specified, use it for both connect and read
            timeout_value = (connect_timeout, connect_timeout)
        else:
            timeout_value = None

        return self.session.request(
            method=method, headers=headers, url=url, json=json_body, data=data, timeout=timeout_value
        )

    def _request(
        self,
        method: str,
        uri: str,
        response: Optional[Type[T]],
        json: Optional[BaseModel],
        *,
        environment_override: Optional[str],
        preview_deployment_id: str | None | ellipsis,
        branch: str | None | ellipsis,
        data: Optional[bytes] = None,
        metadata_request: bool = True,
        extra_headers: Mapping[str, str] | None = None,
        timeout: float | None | ellipsis = ...,
        connect_timeout: float | None | ellipsis = ...,
    ) -> T | requests.Response:
        allow_credential_exchange: bool = True

        if metadata_request or self._query_server is None:
            host = self._api_server
        else:
            host = self._query_server

        if host is None:
            # We definitively need to exchange credentials to get a host
            self._exchange_credentials()
            allow_credential_exchange = False

            # After exchanging credentials, the api server is never none
            assert self._api_server is not None

            if metadata_request or self._query_server is None:
                host = self._api_server
            else:
                host = self._query_server

        r = self._do_request_inner(
            method=method,
            host=host,
            uri=uri,
            json=json,
            environment_override=environment_override,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            data=data,
            metadata_request=metadata_request,
            extra_headers=extra_headers,
            timeout=timeout,
            connect_timeout=connect_timeout,
        )

        if r.status_code in (401, 403) and allow_credential_exchange:
            # It is possible that credentials expired, or that we changed permissions since we last
            # got a token. Exchange them and try again
            self._exchange_credentials()

            # After exchanging credentials, the api server is never null
            assert self._api_server is not None

            if metadata_request or self._query_server is None:
                host = self._api_server
            else:
                host = self._query_server

            r = self._do_request_inner(
                method=method,
                host=host,
                uri=uri,
                json=json,
                environment_override=environment_override,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
                data=data,
                metadata_request=metadata_request,
                extra_headers=extra_headers,
                timeout=timeout,
                connect_timeout=connect_timeout,
            )
        if r.status_code in (401, 403):
            # Consider filtering sensitive headers
            sensitive_headers = {"set-cookie", "cookie", "authorization", "x-api-key", "x-auth-token"}
            safe_headers = {k: v for k, v in r.headers.items() if k.lower() not in sensitive_headers}
            formatted_headers = "\n".join([f"  {k}: {v}" for k, v in safe_headers.items()])
            # If still authenticated, raise a nice exception
            raise ChalkCustomException(
                f"""\
We weren't able to authenticate you with the Chalk API. Authentication was attempted with the following credentials:

    Client ID:     {self._client_id or "<missing>"}
    Client Secret: {"*" * len(self._client_secret or "<missing>")}
    Branch:        {self._branch or "<none>"}
    Environment:   {self._primary_environment or "<none>"}
    API Server:    {self._api_server or "<none>"}
    chalkpy:       v{chalkpy_version}

If these credentials look incorrect to you, try running

>>> chalk login

from the command line from '{os.getcwd()}'. If you are still having trouble, please contact Chalk support.

Additional Details:
Response Status Code: {r.status_code}
{f'Reason for Failure: {r.reason}' if r.reason else ''}
Response Headers: {formatted_headers}
""",
            )
        environment_override_warning = False
        is_service_account = self._client_id is not None and self._client_id.startswith("token-")
        if (
            is_service_account
            and environment_override is not None
            and self._primary_environment is not None
            and environment_override != self._primary_environment
        ):
            environment_override_warning = True

        self._raise_if_http_error(response=r, environment_override_warning=environment_override_warning)
        if response is None:
            return r
        try:
            resp_json = r.json()
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(f"Unexpected response: {r.status_code} {r.text}") from e
        return response(**resp_json)

    def _load_branches(self, timeout: float | None | ellipsis):
        result = self._request(
            method="GET",
            uri="/v1/branches",
            response=_BranchMetadataResponse,
            json=None,
            environment_override=None,
            preview_deployment_id=None,
            branch=self._branch,
            timeout=timeout,
        )
        our_branch = next((b for b in result.branches if b.name == self._branch), None)
        if our_branch is None:
            project_config = load_project_config()
            if project_config:
                project_path = Path(project_config.local_path).parent
            else:
                project_path = "<Your Chalk project directory>"
            branch_names = list(reversed(sorted(result.branches, key=lambda b: str(b.latest_deployment_time))))
            limit = 10
            available_branches = "\n".join(f"  - {b.name}" for b in branch_names[:limit])
            if len(branch_names) > limit:
                available_text = f"The {limit} most recently used branches are:"
            else:
                available_text = "Available branches are:"
            raise ChalkCustomException(
                f"""Your client is set up to use a branch '{self._branch}' that does not exist. {available_text}

{available_branches}

To deploy new features and resolvers in a Jupyter notebook, you must first create a branch from the Chalk CLI.

>>> cd "{project_path}" && chalk apply --branch "{self._branch}"

Then, you can run this cell again and see your new work! For more docs on applying changes to branches, see:

https://docs.chalk.ai/cli/apply
"""
            )

    def whoami(self) -> WhoAmIResponse:
        return self._request(
            method="GET",
            uri="/v1/who-am-i",
            response=WhoAmIResponse,
            json=None,
            environment_override=None,
            preview_deployment_id=None,
            metadata_request=True,
            branch=None,
        )

    # TODO can we go ahead and expose this model to clients? Seems useful
    def _get_branch_info(self) -> _BranchMetadataResponse:
        result = self._request(
            method="GET",
            uri="/v1/branches",
            response=_BranchMetadataResponse,
            json=None,
            environment_override=None,
            preview_deployment_id=None,
            branch=None,
        )
        return result

    def get_branches(self) -> List[str]:
        branches = self._get_branch_info().branches
        return sorted([b.name for b in branches])

    def get_branch(self) -> Optional[str]:
        return self._branch

    def set_branch(self, branch_name: Optional[str]):
        if branch_name is not None:
            branches = self._get_branch_info().branches
            if not any(x.name == branch_name for x in branches):
                raise ValueError(
                    (
                        f"A branch with the name '{branch_name}' does not exist in this environment. Run ChalkClient.create_branch(branch_name) to create a new branch. "
                        f"To see a list of available branches, use ChalkClient.get_branches()."
                    )
                )
        self._branch = branch_name

        message = f"Branch set to '{branch_name}'"
        if not notebook.is_notebook():
            _logger.info(message)
        else:
            print(message)

    def upload_features(
        self,
        input: Mapping[FeatureReference, Any],
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> List[ChalkError]:
        encoded_inputs, _ = recursive_encode_inputs(input)

        # Convert to a bulk style request
        for k, v in encoded_inputs.items():
            encoded_inputs[k] = [v]

        request = UploadFeaturesRequest(
            input=cast(Mapping[str, List[Any]], encoded_inputs),
            preview_deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        )

        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name

        resp = self._request(
            method="POST",
            uri="/v1/upload_features",
            json=request,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            response=UploadFeaturesResponse,
            extra_headers=extra_headers,
        )
        return resp.errors

    def multi_upload_features(
        self,
        input: Union[
            List[Mapping[Union[str, Feature, Any], Any]],
            Mapping[Union[str, Feature, Any], List[Any]],
            pd.DataFrame,
            pl.DataFrame,
            DataFrame,
        ],
        branch: Union[BranchId, ellipsis, None] = ...,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        table_compression = "uncompressed"
        try:
            tables = to_multi_upload_inputs(input)
        except ChalkBaseException as e:
            return e.errors
        except Exception as e:
            return [
                ChalkError.create(
                    code=ErrorCode.INVALID_QUERY,
                    message="Client failed to convert inputs to a multi-upload request",
                    exception=ChalkException.create(
                        kind=type(e).__name__,
                        message=str(e),
                        stacktrace=traceback.format_exc(),
                    ),
                )
            ]

        import pyarrow.feather

        errors: List[ChalkError] = []
        for table in tables:
            features: List[str] = [field.name for field in table.schema]
            table_buffer = BytesIO()
            pyarrow.feather.write_feather(table, dest=table_buffer, compression=table_compression)
            table_buffer.seek(0)
            request = MultiUploadFeaturesRequest(
                features=features, table_compression=table_compression, table_bytes=table_buffer.getvalue()
            )
            resp = self._request(
                method="POST",
                uri="/v1/upload_features/multi",
                data=request.serialize(),
                json=None,
                response=MultiUploadFeaturesResponse,
                environment_override=environment,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
                metadata_request=True,
            )
            errors.extend(resp.errors)

        return errors

    def _display_feature_search(self, features: dict[str, Any]):
        if not notebook.is_notebook():
            return
        from IPython.core.display_functions import display
        from ipywidgets import widgets

        layout = widgets.Layout(width="auto")
        search = widgets.Combobox(
            placeholder="Select A Feature",
            options=list(features.keys()),
            ensure_option=True,
            disabled=False,
            continuous_update=False,
            layout=layout,
        )
        output0 = widgets.Output()
        display(search, output0)

        def on_feature_select(_):
            with output0:
                output0.clear_output()
                table = features[search.value]
                display(table)

        search.observe(on_feature_select, names="value")

    def _register_cell_magics(self):
        try:
            from IPython.core.magic import register_cell_magic
        except ImportError:
            _logger.warning("Failed to register cell magics, IPython not found")
            return

        from chalk.utils.notebook import register_resolver_from_cell_magic

        def sql_resolver(line: str, cell: str | None):
            """Parses the cell as a SQL string resolver and uploads it to the branch"""
            from chalk.sql._internal.sql_file_resolver import SQLStringResult

            register_resolver_from_cell_magic(
                sql_string_result=SQLStringResult(
                    path=re.sub(r"[^A-Za-z_\-0-9]+", "_", line.strip()),
                    sql_string=cell,
                    error=None,
                )
            )

        register_cell_magic(sql_resolver)

    def load_features(
        self,
        branch: BranchIdParam = ...,
    ):
        if not notebook.is_notebook():
            raise ValueError("'ChalkClient().load_features()' must be called in a notebook.")

        if notebook.notebook_features_loaded.get() is True:
            print("Notebook features already loaded. To reload features, first restart the kernel.")
            return

        if branch is ...:
            branch = self._branch

        from rich.console import Console
        from rich.markup import escape
        from rich.style import Style
        from rich.table import Table

        from chalk._reporting.rich.color import SHADOWY_LAVENDER, UNDERLYING_CYAN
        from chalk.client.client_grpc import ChalkGRPCClient

        grpc_client = ChalkGRPCClient(
            client_id=self._client_id,
            client_secret=self._client_secret,
            environment=self._primary_environment,
            api_server=self._api_server,
        )

        console = Console()

        with console.status(f"Loading features from `{branch or self._branch}`", spinner="dots"):
            result = grpc_client._get_python_codegen(branch=branch)  # type: ignore

        if result.errors:
            raise ChalkBaseException(detail="Failed to generate features")

        # access the calling frame so that globals can be loaded into the notebook

        features_raw = {}

        exec(result.codegen, features_raw)

        frame = inspect.currentframe()
        assert frame is not None
        caller_frame = frame.f_back
        assert caller_frame is not None

        feature_sets = {k: v for k, v in features_raw.items() if hasattr(v, "__is_features__")}

        max_name_len = 0
        max_type_len = 0
        has_descriptions = False
        for fs in feature_sets.values():
            for f in fs.__chalk_features_raw__:
                max_name_len = max(max_name_len, len(f.name))
                max_type_len = max(max_type_len, len(str(f.typ).strip("'")))

                if has_descriptions or f.description:
                    has_descriptions = True

        features_processed: dict[str, Table] = {}

        for k, v in feature_sets.items():
            seen = set()
            table = Table(title=k, title_justify="left", width=max_name_len + max_type_len + 10)
            table.add_column("Feature", justify="left", style=Style(color=UNDERLYING_CYAN), no_wrap=True)
            table.add_column("Type", style=Style(color=SHADOWY_LAVENDER))
            if has_descriptions:
                table.add_column("Description", style=Style(color=SHADOWY_LAVENDER), overflow="fold")

            for f in v.__chalk_features_raw__:
                feature_type = str(f.typ).strip("'")

                name = f.name
                if name in seen:
                    continue
                seen.add(name)

                if f.is_windowed_pseudofeature:
                    name = render_fqn(f.name)

                if f.is_windowed:
                    feature_type = f"Windowed[{f.typ.parsed_annotation.__name__}]"

                if f.primary:
                    name = f"{name} [blue]★[/blue]"
                if f.is_has_many:
                    name = f"{name} [blue]⇶[/blue]"
                if f.is_has_one:
                    name = f"{name} [blue]→[/blue]"
                if has_descriptions:
                    table.add_row(name, escape(feature_type).strip("'"), f.description)
                table.add_row(name, escape(feature_type).strip("'"))

            features_processed[k] = table

        caller_frame.f_globals.update(features_raw)
        notebook.notebook_features_loaded.set(True)
        try:
            self._display_feature_search(features_processed)
        except Exception:
            for _, table in features_processed.items():
                console.print(table)

    def query(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Union[BranchId, None, ellipsis] = ...,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: float | ellipsis | None = ...,
        connect_timeout: float | ellipsis | None = ...,
        headers: Mapping[str, str] | None = None,
        query_context: Mapping[str, JsonValue] | str | None = None,
        value_metrics_tag_by_features: Sequence[FeatureReference] = (),
    ) -> OnlineQueryResponseImpl:
        encoded_inputs, all_warnings = recursive_encode_inputs(input)
        encoded_outputs = encode_outputs(output)
        outputs = encoded_outputs.string_outputs
        encoded_value_metrics_tag_by_features = encode_outputs(value_metrics_tag_by_features).string_outputs
        if branch is ...:
            branch = self._branch
        now_str = None
        if now is not None:
            if now.tzinfo is None:
                now = now.astimezone(tz=timezone.utc)
            now_str = now.isoformat()

        staleness_encoded = {}
        if staleness is not None:
            for k, v in staleness.items():
                if isinstance(k, str):
                    # It's a feature set
                    staleness_encoded[k] = v
                elif is_feature_set_class(k):
                    staleness_encoded[k.namespace] = v
                else:
                    staleness_encoded[ensure_feature(k).root_fqn] = v

        request = OnlineQueryRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            expression_outputs=encoded_outputs.feature_expressions_base64,
            now=now_str,
            staleness=staleness_encoded,
            context=OnlineQueryContext(
                environment=environment,
                tags=tags,
                required_resolver_tags=required_resolver_tags,
            ),
            deployment_id=preview_deployment_id,
            branch_id=branch,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            meta=meta,
            explain=explain,
            include_meta=bool(include_meta or explain),
            store_plan_stages=store_plan_stages,
            encoding_options=encoding_options or FeatureEncodingOptions(),
            planner_options=planner_options,
            value_metrics_tag_by_features=tuple(encoded_value_metrics_tag_by_features),
            query_context=_validate_context_dict(query_context),
            overlay_graph=_get_overlay_graph_b64(),
        )

        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name
        if headers:
            extra_headers.update(headers)

        resp = self._request(
            method="POST",
            uri="/v1/query/online",
            json=request,
            response=OnlineQueryResponse,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            metadata_request=False,
            extra_headers=extra_headers,
            timeout=request_timeout,
            connect_timeout=connect_timeout,
        )
        return OnlineQueryResponseImpl(data=resp.data, errors=resp.errors or [], warnings=all_warnings, meta=resp.meta)

    def multi_query(
        self,
        queries: list[OnlineQuery],
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        query_context: Mapping[str, JsonValue] | str | None = None,
        meta: Optional[Mapping[str, str]] = None,
        use_feather: Optional[bool] = True,  # deprecated
        compression: Optional[str] = "uncompressed",
    ) -> BulkOnlineQueryResponse:
        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name
        buffer = BytesIO()
        buffer.write(MULTI_QUERY_MAGIC_STR)
        if branch is ...:
            branch = self._branch
        for query in queries:
            tags = query.tags
            encoded_inputs = {str(k): v for k, v in query.input.items()}
            outputs = encode_outputs(query.output).string_outputs
            encoded_value_metrics_tag_by_features = encode_outputs(query.value_metrics_tag_by_features).string_outputs
            request = OnlineQueryManyRequest(
                inputs=cast(Mapping[str, List[Any]], encoded_inputs),
                outputs=outputs,
                staleness=(
                    {}
                    if query.staleness is None
                    else {ensure_feature(k).root_fqn: v for k, v in query.staleness.items()}
                ),
                context=OnlineQueryContext(
                    environment=environment,
                    tags=None if tags is None else list(tags),
                ),
                deployment_id=preview_deployment_id,
                branch_id=branch,
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                meta=meta,
                query_context=_validate_context_dict(query_context),
                value_metrics_tag_by_features=tuple(encoded_value_metrics_tag_by_features),
                overlay_graph=_get_overlay_graph_b64(),
            )

            write_query_to_buffer(buffer, request, compression=compression)

        buffer.seek(0)
        resp = self._request(
            method="POST",
            uri="/v1/query/feather",
            data=buffer.getvalue(),
            json=None,
            response=None,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            metadata_request=False,
            extra_headers=extra_headers,
        )

        if resp.headers.get("Content-Type") == "application/octet-stream":
            all_responses = OnlineQueryResponseFeather.deserialize(resp.content)

            bulk_results = []
            for query_name, serialized_single_result in all_responses.query_results_bytes.items():
                single_feather_result = OnlineQueryResultFeather.deserialize(serialized_single_result)
                scalars_df = None
                groups_dfs = None
                query_meta = QueryMeta(**json.loads(single_feather_result.meta)) if single_feather_result.meta else None
                errors = (
                    [ChalkError.create(**json.loads(error_json_str)) for error_json_str in single_feather_result.errors]
                    if single_feather_result.errors
                    else None
                )
                if single_feather_result.has_data:
                    scalars_pa = pyarrow.feather.read_table(BytesIO(single_feather_result.scalar_data))
                    scalars_pl = pa_table_to_pl_df(scalars_pa)
                    scalars_df = scalars_pl

                    groups_dfs = {}
                    for feature_name, feature_results_bytes in single_feather_result.groups_data.items():
                        feature_pa = pyarrow.feather.read_table(BytesIO(feature_results_bytes))
                        feature_pl = pa_table_to_pl_df(feature_pa)
                        groups_dfs[feature_name] = feature_pl

                bulk_result = BulkOnlineQueryResult(
                    scalars_df=scalars_df, groups_dfs=groups_dfs, errors=errors, meta=query_meta
                )
                bulk_results.append(bulk_result)
            return BulkOnlineQueryResponse(results=bulk_results)
        else:
            raise ChalkBaseException(
                errors=None, detail="Unexpected response from server -- failed to receive Feather encoded data."
            )

    def query_bulk(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        context: Optional[OnlineQueryContext] = None,  # Deprecated.
        environment: Optional[EnvironmentId] = None,
        store_plan_stages: bool = False,
        tags: Optional[List[str]] = None,
        required_resolver_tags: Optional[List[str]] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        query_context: Mapping[str, JsonValue] | str | None = None,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        request_timeout: float | ellipsis | None = ...,
        headers: Mapping[str, str] | None = None,
        value_metrics_tag_by_features: Sequence[FeatureReference] = (),
    ) -> BulkOnlineQueryResponse:
        extra_headers = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name
        if headers:
            extra_headers.update(headers)
        if branch is ...:
            branch = self._branch

        now_str = None
        if now is not None:
            now_str = []
            for ts in now:
                if ts.tzinfo is None:
                    ts = ts.astimezone(tz=timezone.utc)
                now_str.append(ts.isoformat())

        staleness_encoded = {}
        if staleness is not None:
            for k, v in staleness.items():
                if is_feature_set_class(k):
                    for f in k.features:
                        staleness_encoded[f.root_fqn] = v
                else:
                    staleness_encoded[ensure_feature(k).root_fqn] = v

        environment = environment or (context and context.environment)
        tags = tags or (context and context.tags)
        # TODO: We're doing a lame encoding here b/c recursive_encode will treat our lists
        #       as json to serialize.
        # encoded_inputs, encoding_warnings = recursive_encode(input)
        validate_iterable_values_in_mapping(input, method_name="ChalkClient.query_bulk(...)")
        encoded_inputs = {str(k): v for k, v in input.items()}
        encoded_outputs = encode_outputs(output)
        encoded_value_metrics_tag_by_features = encode_outputs(value_metrics_tag_by_features).string_outputs
        request = OnlineQueryManyRequest(
            inputs=cast(Mapping[str, List[Any]], encoded_inputs),
            outputs=encoded_outputs.string_outputs,
            expression_outputs=encoded_outputs.feature_expressions_base64,
            now=now_str,
            staleness=staleness_encoded,
            context=OnlineQueryContext(
                environment=environment,
                tags=tags,
                required_resolver_tags=required_resolver_tags,
            ),
            deployment_id=preview_deployment_id,
            branch_id=branch,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            query_context=_validate_context_dict(query_context),
            meta=meta,
            store_plan_stages=store_plan_stages,
            explain=explain,
            value_metrics_tag_by_features=tuple(encoded_value_metrics_tag_by_features),
            overlay_graph=_get_overlay_graph_b64(),
        )

        buffer = BytesIO()

        buffer.write(MULTI_QUERY_MAGIC_STR)
        write_query_to_buffer(buffer, request, compression="uncompressed")

        buffer.seek(0)

        resp = self._request(
            method="POST",
            uri="/v1/query/feather",
            data=buffer.getvalue(),
            json=None,
            response=None,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            metadata_request=False,
            extra_headers=extra_headers,
            timeout=request_timeout,
        )

        import polars as pl
        import pyarrow.feather

        assert (
            resp.headers.get("Content-Type") == "application/octet-stream"
        ), "The response wasn't in the expected byte format!"
        all_responses = OnlineQueryResponseFeather.deserialize(resp.content)

        bulk_results = []
        for query_name, serialized_single_result in all_responses.query_results_bytes.items():
            single_feather_result = OnlineQueryResultFeather.deserialize(serialized_single_result)
            scalars_df = None
            groups_dfs = None
            query_meta = QueryMeta(**json.loads(single_feather_result.meta)) if single_feather_result.meta else None
            errors = (
                [ChalkError.create(**json.loads(error_json_str)) for error_json_str in single_feather_result.errors]
                if single_feather_result.errors
                else None
            )
            if single_feather_result.has_data:
                scalars_pa = pyarrow.feather.read_table(BytesIO(single_feather_result.scalar_data))
                scalars_pl = pa_table_to_pl_df(scalars_pa)
                assert isinstance(scalars_pl, pl.DataFrame)
                scalars_df = scalars_pl

                groups_dfs = {}
                for feature_name, feature_results_bytes in single_feather_result.groups_data.items():
                    feature_pa = pyarrow.feather.read_table(BytesIO(feature_results_bytes))
                    feature_pl = pa_table_to_pl_df(feature_pa)
                    groups_dfs[feature_name] = feature_pl

            bulk_result = BulkOnlineQueryResult(
                scalars_df=scalars_df, groups_dfs=groups_dfs, errors=errors, meta=query_meta
            )
            bulk_results.append(bulk_result)
        return BulkOnlineQueryResponse(results=bulk_results)

    def offline_query(
        self,
        input: Union[QueryInput, OfflineQueryInputUri, Tuple[QueryInput, ...], List[QueryInput], str, None] = None,
        input_times: Union[Sequence[datetime], datetime, Sequence[Sequence[datetime]], None] = None,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        environment: Optional[EnvironmentId] = None,
        dataset_name: Optional[str] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        # distinguished from user explicitly specifying branch=None
        correlation_id: str | None = None,
        query_context: Mapping[str, JsonValue] | str | None = None,
        max_samples: Optional[int] = None,
        wait: bool = False,
        show_progress: bool | ellipsis = ...,
        timeout: float | timedelta | ellipsis | None = ...,
        recompute_features: Union[bool, List[FeatureReference]] = False,
        sample_features: Optional[List[FeatureReference]] = None,
        lower_bound: datetime | timedelta | str | None = None,
        upper_bound: datetime | timedelta | str | None = None,
        store_plan_stages: bool = False,
        explain: bool = False,
        tags: Optional[List[str]] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        spine_sql_query: str | None = None,
        resources: ResourceRequests | None = None,
        run_asynchronously: bool = False,
        store_online: bool = False,
        store_offline: bool = False,
        num_shards: int | None = None,
        num_workers: int | None = None,
        completion_deadline: timedelta | None = None,
        max_retries: int | None = None,
        include_meta: Optional[
            bool
        ] = None,  # unused, undocumented. provided to make switching online_query -> offline_query easier.
        use_multiple_computers: bool = False,
        upload_input_as_table: bool = False,
        env_overrides: dict[str, str] | None = None,
        enable_profiling: bool = False,
        override_target_image_tag: Optional[str] = None,
        feature_for_lower_upper_bound: Optional[FeatureReference] = None,
        use_job_queue: bool = False,
    ) -> DatasetImpl:
        run_asynchronously = (
            use_multiple_computers
            or use_job_queue
            or run_asynchronously
            or num_shards is not None
            or num_workers is not None
        )

        lower_bound = _convert_datetime_or_timedelta_param("lower_bound", lower_bound)
        upper_bound = _convert_datetime_or_timedelta_param("upper_bound", upper_bound)
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        del pl  # unused

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        if isinstance(num_shards, int) and num_shards < 1:
            raise ValueError("num_shards must be greater than 0")
        if isinstance(num_workers, int) and num_workers < 1:
            raise ValueError("num_workers must be greater than 0")
        if num_shards is not None and num_workers is None:
            num_workers = num_shards
        if num_workers is not None and num_shards is None:
            num_shards = num_workers
        if num_workers is not None and num_shards is not None and num_workers > num_shards:
            num_workers = num_shards

        optional_encoded_outputs = encode_outputs(output)
        optional_output_root_fqns = optional_encoded_outputs.string_outputs
        optional_output_expressions = optional_encoded_outputs.feature_expressions_base64
        required_encoded_outputs = encode_outputs(required_output)
        required_output_root_fqns = required_encoded_outputs.string_outputs
        required_output_expressions = required_encoded_outputs.feature_expressions_base64

        context = OfflineQueryContext(environment=environment)

        if input is None:
            query_input = None
        elif isinstance(input, OfflineQueryInputUri):
            query_input = input
        elif isinstance(input, str):
            query_input = OfflineQueryInputUri(
                parquet_uri=input,
                start_row=None,
                end_row=None,
            )
        else:
            if isinstance(input, (list, tuple)):
                input_times_tuple: Sequence[QueryInputTime] = (
                    [None] * len(input)
                    if input_times is None
                    else [input_times for _ in input]
                    if isinstance(input_times, datetime)
                    else input_times
                )
                run_asynchronously = True
                multi_input = list(zip(input, input_times_tuple))
            else:
                multi_input = [(input, cast(None, input_times))]

            # defaulting to uploading input as table if inputs are large
            if upload_input_as_table or (len(multi_input) > 0 and len(multi_input[0][0]) > 100) or num_shards:
                with ThreadPoolExecutor(thread_name_prefix="offline_query_upload_input") as upload_input_executor:
                    query_input = self._upload_offline_query_input(
                        multi_input,
                        context=context,
                        branch=branch,
                        executor=upload_input_executor,
                        num_shards=num_shards,
                    )
            elif run_asynchronously:
                query_input = tuple(_to_offline_query_input(x, t) for x, t in multi_input)
            else:
                assert len(multi_input) == 1, "We should default to running asynchronously if inputs is partitioned"
                query_input = _to_offline_query_input(*multi_input[0])

        response = self._create_dataset_job(
            optional_output=optional_output_root_fqns,
            required_output=required_output_root_fqns,
            query_input=query_input,
            spine_sql_query=spine_sql_query,
            dataset_name=dataset_name,
            branch=branch,
            correlation_id=correlation_id,
            query_context=_validate_context_dict(query_context),
            context=context,
            max_samples=max_samples,
            recompute_features=recompute_features,
            sample_features=sample_features,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            store_plan_stages=store_plan_stages,
            tags=tags,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            run_asynchronously=run_asynchronously,
            explain=explain,
            resources=resources,
            env_overrides=env_overrides,
            enable_profiling=enable_profiling,
            store_online=store_online,
            store_offline=store_offline,
            override_target_image_tag=override_target_image_tag,
            num_shards=num_shards,
            num_workers=num_workers,
            feature_for_lower_upper_bound=str(feature_for_lower_upper_bound)
            if feature_for_lower_upper_bound is not None
            else None,
            completion_deadline=completion_deadline,
            max_retries=max_retries,
            optional_output_expressions=optional_output_expressions,
            required_output_expressions=required_output_expressions,
            use_job_queue=use_job_queue,
        )

        initialized_dataset = dataset_from_response(response, self)

        revision = initialized_dataset.revisions[-1]
        assert isinstance(revision, DatasetRevisionImpl)
        # Storing timeout for when we call dataset revision methods that
        # require polling
        revision.timeout = timeout
        revision.show_progress = show_progress

        if not wait:
            return initialized_dataset

        revision.wait_for_completion(
            show_progress=show_progress if isinstance(show_progress, bool) else True,
            timeout=timeout,
            caller_method="offline_query",
        )
        initialized_dataset.is_finished = True
        return initialized_dataset

    def prompt_evaluation(
        self,
        prompts: list[Prompt | str],
        dataset_name: str | None = None,
        dataset_id: str | None = None,
        revision_id: str | None = None,
        reference_output: str | FeatureReference | None = None,
        evaluators: list[str] | None = None,
        meta: Mapping[str, str] | None = None,
        input: Union[QueryInput, Tuple[QueryInput, ...], List[QueryInput], str, None] = None,
        input_times: Union[Sequence[datetime], datetime, Sequence[Sequence[datetime]], None] = None,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        environment: Optional[EnvironmentId] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        # distinguished from user explicitly specifying branch=None
        correlation_id: str | None = None,
        query_context: Mapping[str, JsonValue] | str | None = None,
        max_samples: Optional[int] = None,
        wait: bool = False,
        show_progress: bool | ellipsis = ...,
        timeout: float | timedelta | ellipsis | None = ...,
        recompute_features: Union[bool, List[FeatureReference]] = False,
        sample_features: Optional[List[FeatureReference]] = None,
        lower_bound: datetime | timedelta | str | None = None,
        upper_bound: datetime | timedelta | str | None = None,
        store_plan_stages: bool = False,
        explain: bool = False,
        tags: Optional[List[str]] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        spine_sql_query: str | None = None,
        resources: ResourceRequests | None = None,
        run_asynchronously: bool = False,
        store_online: bool = False,
        store_offline: bool = False,
        num_shards: int | None = None,
        num_workers: int | None = None,
        completion_deadline: timedelta | None = None,
        max_retries: int | None = None,
        include_meta: Optional[
            bool
        ] = None,  # unused, undocumented. provided to make switching online_query -> offline_query easier.
        use_multiple_computers: bool = False,
        upload_input_as_table: bool = False,
        env_overrides: dict[str, str] | None = None,
        enable_profiling: bool = False,
        override_target_image_tag: Optional[str] = None,
        feature_for_lower_upper_bound: Optional[FeatureReference] = None,
        use_job_queue: bool = False,
    ) -> Dataset:
        if sum([dataset_name is not None, dataset_id is not None, revision_id is not None, input is not None]) != 1:
            if input is None or dataset_name is None:
                raise ValueError(
                    "'ChalkClient.prompt_evaluation' must be called with exactly one of 'dataset_name', 'dataset_id', 'revision_id' or 'input'"
                )
        if input is None:
            dataset = self.get_dataset(
                dataset_name=dataset_name,
                dataset_id=dataset_id,
                revision_id=revision_id,
                environment=environment,
            )
        else:
            dataset = None

        run_asynchronously = (
            use_multiple_computers
            or use_job_queue
            or run_asynchronously
            or num_shards is not None
            or num_workers is not None
        )

        lower_bound = _convert_datetime_or_timedelta_param("lower_bound", lower_bound)
        upper_bound = _convert_datetime_or_timedelta_param("upper_bound", upper_bound)
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        del pl  # unused

        if isinstance(num_shards, int) and num_shards < 1:
            raise ValueError("num_shards must be greater than 0")
        if isinstance(num_workers, int) and num_workers < 1:
            raise ValueError("num_workers must be greater than 0")
        if num_shards is not None and num_workers is None:
            num_workers = num_shards
        if num_workers is not None and num_shards is None:
            num_shards = num_workers
        if num_workers is not None and num_shards is not None and num_workers > num_shards:
            num_workers = num_shards

        if input is not None:
            # add the input columns to the output columns
            output = list(output)
            if isinstance(input, str):
                pass
            elif isinstance(input, (list, tuple)):
                for inp in input:
                    output += _get_column_names(inp)
            else:
                output += _get_column_names(input)

        optional_encoded_outputs = encode_outputs(output)
        optional_output_root_fqns = optional_encoded_outputs.string_outputs
        optional_output_expressions = optional_encoded_outputs.feature_expressions_base64
        required_encoded_outputs = encode_outputs(required_output)
        required_output_root_fqns = required_encoded_outputs.string_outputs
        required_output_expressions = required_encoded_outputs.feature_expressions_base64

        context = OfflineQueryContext(environment=environment)

        if input is None:
            query_input = None
        elif isinstance(input, str):
            query_input = OfflineQueryInputUri(
                parquet_uri=input,
                start_row=None,
                end_row=None,
            )
        else:
            if isinstance(input, (list, tuple)):
                input_times_tuple: Sequence[QueryInputTime] = (
                    [None] * len(input)
                    if input_times is None
                    else [input_times for _ in input]
                    if isinstance(input_times, datetime)
                    else input_times
                )
                run_asynchronously = True
                multi_input = list(zip(input, input_times_tuple))
            else:
                multi_input = [(input, cast(None, input_times))]

            # defaulting to uploading input as table if inputs are large
            if upload_input_as_table or (len(multi_input) > 0 and len(multi_input[0][0]) > 100) or num_shards:
                with ThreadPoolExecutor(thread_name_prefix="offline_query_upload_input") as upload_input_executor:
                    query_input = self._upload_offline_query_input(
                        multi_input,
                        context=context,
                        branch=branch,
                        executor=upload_input_executor,
                        num_shards=num_shards,
                    )
            elif run_asynchronously:
                query_input = tuple(_to_offline_query_input(x, t) for x, t in multi_input)
            else:
                assert len(multi_input) == 1, "We should default to running asynchronously if inputs is partitioned"
                query_input = _to_offline_query_input(*multi_input[0])

        if not (
            isinstance(recompute_features, list)
            or isinstance(recompute_features, bool)  # pyright: ignore[reportUnnecessaryIsInstance]
        ):
            raise ValueError("The value for 'recompute_features' must be either a bool for a list of features.")
        if sample_features is not None and not isinstance(
            sample_features, list
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("The value for 'sample_features' must be a list of features.")
        if isinstance(recompute_features, list):
            recompute_features = [
                unwrap_feature(f).fqn if isinstance(f, FeatureWrapper) else f for f in recompute_features
            ]
        if isinstance(sample_features, list):
            sample_features = [unwrap_feature(f).fqn if isinstance(f, FeatureWrapper) else f for f in sample_features]
        if isinstance(recompute_features, list) and isinstance(sample_features, list):
            intersection = set(recompute_features) & set(sample_features)
            if len(intersection) > 0:
                raise ValueError(
                    "Features in 'recompute_features' and 'sample_features' arguments must not overlap. "
                    + f"Intersection as specified is {sorted(list(intersection))}"
                )

        def process_bound(bound: datetime | timedelta | None) -> str | None:
            if isinstance(bound, datetime):
                if bound.tzinfo is None:
                    bound = bound.astimezone()
                return bound.isoformat()
            if isinstance(bound, timedelta):
                return TIMEDELTA_PREFIX + timedelta_to_duration(bound)
            return None

        lower_bound_str = process_bound(lower_bound)
        upper_bound_str = process_bound(upper_bound)
        if branch is ...:
            branch = self._branch
        if reference_output is not None:
            reference_output_encoded = encode_outputs([reference_output])
            if (
                len(reference_output_encoded.feature_expressions_proto) == 1
                and len(reference_output_encoded.feature_expressions_base64) == 1
            ):
                encoded_reference_output = OutputExpression(
                    base64_proto=reference_output_encoded.feature_expressions_base64[0],
                    python_repr=repr(reference_output),
                    output_column_name=reference_output_encoded.feature_expressions_proto[0].output_column_name,
                )
            elif len(reference_output_encoded.string_outputs) == 1:
                encoded_reference_output = reference_output_encoded.string_outputs[0]
            else:
                raise ValueError(f"Could not parse reference output: {reference_output}")
        else:
            encoded_reference_output = None

        request = CreatePromptEvaluationRequest(
            prompts=prompts,
            dataset_id=str(dataset.dataset_id) if dataset is not None else None,
            dataset_revision_id=str(dataset.revisions[-1].revision_id) if dataset is not None else None,
            reference_output=encoded_reference_output,
            evaluators=evaluators,
            meta=meta,
            output=optional_output_root_fqns,
            output_expressions=optional_output_expressions or [],
            required_output=required_output_root_fqns,
            required_output_expressions=required_output_expressions or [],
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            branch=branch,
            recompute_features=recompute_features,
            sample_features=sample_features,
            observed_at_lower_bound=lower_bound_str,
            observed_at_upper_bound=upper_bound_str,
            store_plan_stages=store_plan_stages,
            correlation_id=correlation_id,
            query_context=_validate_context_dict(query_context),
            explain=explain,
            tags=tags,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            use_multiple_computers=run_asynchronously,
            spine_sql_query=spine_sql_query,
            resources=resources,
            env_overrides=env_overrides,
            enable_profiling=enable_profiling,
            store_online=store_online,
            store_offline=store_offline,
            override_target_image_tag=override_target_image_tag,
            num_shards=num_shards,
            num_workers=num_workers,
            feature_for_lower_upper_bound=feature_for_lower_upper_bound,
            completion_deadline=timedelta_to_duration(completion_deadline) if completion_deadline is not None else None,
            max_retries=max_retries,
            use_job_queue=use_job_queue,
            overlay_graph=_get_overlay_graph_b64(),
        )

        response = self._request(
            method="POST",
            uri="/v1/prompt/evaluate",
            response=DatasetResponse,
            json=request,
            environment_override=environment,
            preview_deployment_id=None,
            branch=branch,
        )

        self._raise_if_200_with_non_resolver_errors(response=response)
        initialized_dataset = dataset_from_response(response, self)  # pyright: ignore[reportArgumentType]

        revision = initialized_dataset.revisions[-1]
        assert isinstance(revision, DatasetRevisionImpl)
        # Storing timeout for when we call dataset revision methods that
        # require polling
        revision.timeout = timeout
        revision.show_progress = show_progress

        if not wait:
            return initialized_dataset

        revision.wait_for_completion(
            show_progress=show_progress if isinstance(show_progress, bool) else True,
            timeout=timeout,
            caller_method="prompt_evaluation",
        )
        initialized_dataset.is_finished = True
        return initialized_dataset

    def get_operation_feature_statistics(self, operation_id: uuid.UUID) -> FeatureStatisticsResponse:
        """
        Fetches statistics for an operation's outputs.
        """
        return self._request(
            "GET",
            f"/v1/operations/{operation_id}/feature_statistics",
            FeatureStatisticsResponse,
            json=None,
            environment_override=None,
            preview_deployment_id=None,
            branch=None,
        )

    def ingest_dataset(
        self,
        request: IngestDatasetRequest,
        context: OfflineQueryContext,
    ) -> DatasetImpl:
        response = self._request(
            method="POST",
            uri="/v4/ingest_dataset",
            json=request,
            response=DatasetResponse,
            environment_override=context.environment,
            preview_deployment_id=None,
            branch=None,
            metadata_request=True,
        )
        ingestion_dataset = dataset_from_response(response, self)
        self._raise_if_200_with_errors(response=response)
        return ingestion_dataset.wait(show_progress=False, caller_name="ingest_dataset")

    def sample(
        self,
        output: Sequence[FeatureReference] = (),
        required_output: Sequence[FeatureReference] = (),
        output_id: bool = False,
        output_ts: Union[bool, str] = False,
        max_samples: Optional[int] = None,
        dataset: Optional[str] = None,
        branch: BranchId | None | ellipsis = ...,
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> pd.DataFrame:
        context = OfflineQueryContext(environment=environment)
        outputs_encoded = encode_outputs(output)
        required_outputs_encoded = encode_outputs(required_output)

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        return self._create_and_await_offline_query_job(
            query_input=None,
            optional_output=outputs_encoded.string_outputs,
            required_output=required_outputs_encoded.string_outputs,
            optional_output_expressions=outputs_encoded.feature_expressions_base64,
            required_output_expressions=required_outputs_encoded.feature_expressions_base64,
            max_samples=max_samples,
            context=context,
            output_id=output_id,
            output_ts=output_ts,
            dataset_name=dataset,
            branch=branch,
            preview_deployment_id=None,
            timeout=timeout,
            tags=tags,
        )

    @overload
    def get_dataset(
        self,
        dataset_name: str,
        environment: EnvironmentId | None = None,
    ) -> Dataset:
        ...

    @overload
    def get_dataset(
        self,
        *,
        revision_id: str | uuid.UUID,
        environment: EnvironmentId | None = None,
    ) -> Dataset:
        ...

    @overload
    def get_dataset(
        self,
        *,
        job_id: str | uuid.UUID,
        environment: EnvironmentId | None = None,
    ) -> Dataset:
        ...

    @overload
    def get_dataset(
        self,
        *,
        dataset_id: str | uuid.UUID,
        environment: EnvironmentId | None = None,
    ) -> Dataset:
        ...

    @overload
    def get_dataset(
        self,
        *,
        dataset_name: str | None = None,
        dataset_id: str | uuid.UUID | None = None,
        revision_id: str | uuid.UUID | None = None,
        job_id: str | uuid.UUID | None = None,
        environment: EnvironmentId | None = None,
    ) -> Dataset:
        ...

    def get_dataset(
        self,
        dataset_name: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        *,
        dataset_id: str | uuid.UUID | None = None,
        revision_id: str | uuid.UUID | None = None,
        job_id: str | uuid.UUID | None = None,
    ) -> Dataset:
        if sum([dataset_name is not None, dataset_id is not None, revision_id is not None, job_id is not None]) != 1:
            raise ValueError(
                "'ChalkClient.get_dataset' must be called with exactly one of 'dataset_name', 'dataset_id' or 'job_id'"
            )

        if revision_id is not None:
            response: DatasetResponse = self._get_dataset_from_job_id(
                job_id=revision_id,
                environment=environment,
                branch=None,
            )
        elif job_id is not None:
            response: DatasetResponse = self._get_dataset_from_job_id(
                job_id=job_id,
                environment=environment,
                branch=None,
            )
        elif dataset_id is not None:
            response: DatasetResponse = self._get_dataset_from_name_or_id(
                dataset_name_or_id=str(dataset_id), environment=environment, branch=None
            )
        elif dataset_name is not None:
            response: DatasetResponse = self._get_dataset_from_name_or_id(
                dataset_name_or_id=dataset_name, environment=environment, branch=None
            )
        else:
            raise ValueError(
                "'ChalkClient.get_dataset' must be called with exactly one of 'dataset_name', 'dataset_id' or 'job_id'"
            )
        if response.errors:
            raise ChalkCustomException(
                message=f"Failed to download dataset `{dataset_name or dataset_id or job_id}`",
                errors=response.errors,
            )
        return dataset_from_response(response, self)

    def create_dataset(
        self,
        input: QueryInput,
        dataset_name: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        wait: bool = False,
        show_progress: bool | ellipsis = ...,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> DatasetImpl:
        output = _get_column_names(input)
        if len(output) == 0:
            raise ValueError("'input' must be specified.")

        optional_encoded_outputs = encode_outputs(output)
        optional_output_root_fqns = optional_encoded_outputs.string_outputs
        optional_output_expressions = optional_encoded_outputs.feature_expressions_base64

        context = OfflineQueryContext(environment=environment)

        if isinstance(input, str):
            query_input = OfflineQueryInputUri(
                parquet_uri=input,
                start_row=None,
                end_row=None,
            )
        else:
            # defaulting to uploading input as table if inputs are large
            if len(input) > 100:
                with ThreadPoolExecutor(thread_name_prefix="offline_query_upload_input") as upload_input_executor:
                    query_input = self._upload_offline_query_input(
                        [(input, None)],
                        context=context,
                        branch=branch,
                        executor=upload_input_executor,
                        num_shards=None,
                    )
            else:
                query_input = _to_offline_query_input(input, None)

        response = self._create_dataset_job(
            query_input=query_input,
            dataset_name=dataset_name,
            optional_output=optional_output_root_fqns,
            optional_output_expressions=optional_output_expressions,
            branch=branch,
            required_output=[],
            spine_sql_query=None,
            correlation_id=None,
            query_context=None,
            context=context,
            max_samples=None,
            recompute_features=True,  # always recompute
            sample_features=None,
            lower_bound=None,
            upper_bound=None,
            store_plan_stages=False,
            tags=None,
            required_resolver_tags=None,
            planner_options=None,
            run_asynchronously=False,
            explain=False,
            resources=None,
            env_overrides=None,
            enable_profiling=False,
            store_online=False,
            store_offline=False,
            override_target_image_tag=None,
            num_shards=None,
            num_workers=None,
            feature_for_lower_upper_bound=None,
            completion_deadline=None,
            max_retries=None,
            required_output_expressions=None,
        )

        initialized_dataset = dataset_from_response(response, self)

        revision = initialized_dataset.revisions[-1]
        assert isinstance(revision, DatasetRevisionImpl)
        # Storing timeout for when we call dataset revision methods that
        # require polling
        revision.timeout = timeout
        revision.show_progress = show_progress

        if not wait:
            return initialized_dataset

        revision.wait_for_completion(
            show_progress=show_progress if isinstance(show_progress, bool) else True,
            timeout=timeout,
            caller_method="offline_query",
        )
        initialized_dataset.is_finished = True
        return initialized_dataset

    def set_dataset_revision_metadata(
        self, environment: EnvironmentId, revision_id: str | uuid.UUID, metadata: Mapping[str, Any]
    ):
        response = self._request(
            method="POST",
            uri=f"/dataset/{revision_id}/metadata",
            response=SetDatasetRevisionMetadataResponse,
            environment_override=environment,
            json=SetDatasetRevisionMetadataRequest(metadata=metadata),
            preview_deployment_id=None,
            branch=None,
            metadata_request=False,
        )

        if response.errors:
            raise ChalkCustomException(
                message=f"Failed to set metadata '{metadata}' for dataset revision: `{revision_id}`",
                errors=response.errors,
            )

    def delete_features(
        self,
        namespace: str,
        features: Optional[List[str]],
        tags: Optional[List[str]],
        primary_keys: List[str],
        environment: Optional[EnvironmentId] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        retain_offline: bool = False,
        retain_online: bool = False,
    ) -> FeatureObservationDeletionResponse:
        if branch is ...:
            branch = self._branch
        if branch is not None:
            raise NotImplementedError(
                (
                    f"Feature deletion is not currently supported for branch deployments. Client is currently connected to the branch '{branch}'."
                    f"Please specify `branch=None`."
                )
            )
        _logger.debug(
            (
                f"Performing deletion in environment {environment if environment else 'default'} and namespace "
                f"{namespace} with targets that match the following criteria: features={features}, tags={tags}, "
                f"and primary_keys={primary_keys}"
            )
        )

        return self._request(
            method="DELETE",
            uri="/v1/features/rows",
            json=FeatureObservationDeletionRequest(
                namespace=namespace,
                features=features,
                tags=tags,
                primary_keys=primary_keys,
                retain_offline=retain_offline,
                retain_online=retain_online,
            ),
            response=FeatureObservationDeletionResponse,
            environment_override=environment,
            preview_deployment_id=None,
            branch=branch,
        )

    def drop_features(
        self,
        namespace: str,
        features: List[str],
        environment: Optional[EnvironmentId] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        retain_offline: bool = False,
        retain_online: bool = False,
    ) -> FeatureDropResponse:
        if branch is ...:
            branch = self._branch
        if branch is not None:
            raise NotImplementedError(
                (
                    f"Feature dropping is not currently supported for branch deployments. Client is currently connected to the branch '{branch}'."
                    f"Please specify `branch=None`."
                )
            )
        _logger.debug(
            (
                f"Performing feature drop in environment {environment if environment else 'default'} and namespace "
                f"{namespace} for the following features:{features}."
            )
        )
        return self._request(
            method="DELETE",
            uri="/v1/features/columns",
            json=FeatureDropRequest(
                namespace=namespace, features=features, retain_offline=retain_offline, retain_online=retain_online
            ),
            response=FeatureDropResponse,
            environment_override=environment,
            preview_deployment_id=None,
            branch=branch,
        )

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
        upper_bound: datetime | str | None = None,
        lower_bound: datetime | str | None = None,
        store_online: bool = True,
        store_offline: bool = True,
        timestamping_mode: Literal["feature_time", "online_store_write_time"] = "feature_time",
        idempotency_key: Optional[str] = None,
        override_target_image_tag: str | None = None,
    ) -> ResolverRunResponse:
        if branch is ...:
            branch = self._branch

        if branch is not None:
            raise NotImplementedError(
                (
                    f"Triggering resolver runs is not currently supported for branch deployments."
                    f"Client is currently connected to the branch '{branch}'. Please specify `branch=None`."
                )
            )
        if preview_deployment_id is None:
            preview_deployment_id = self._preview_deployment_id
        _logger.debug(f"Triggering resolver {resolver_fqn} to run")

        lower_bound = _convert_datetime_param("lower_bound", lower_bound)
        upper_bound = _convert_datetime_param("upper_bound", upper_bound)

        return self._request(
            method="POST",
            uri="/v1/runs/trigger",
            json=TriggerResolverRunRequest(
                resolver_fqn=resolver_fqn,
                lower_bound=lower_bound and lower_bound.isoformat(),
                upper_bound=upper_bound and upper_bound.isoformat(),
                timestamping_mode=timestamping_mode,
                persistence_settings=PersistenceSettings(
                    persist_online_storage=store_online, persist_offline_storage=store_offline
                ),
                override_target_image_tag=override_target_image_tag,
                idempotency_key=idempotency_key,
            ),
            response=ResolverRunResponse,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

    def get_run_status(
        self,
        run_id: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[Union[BranchId, ellipsis]] = ...,
    ) -> ResolverRunResponse:
        if branch is ...:
            branch = self._branch
        if branch is not None:
            raise NotImplementedError(
                (
                    f"Triggering resolver runs is not currently supported for branch deployments."
                    f"Client is currently connected to the branch '{branch}'. Please specify `branch=None`."
                )
            )
        response = self._request(
            method="GET",
            uri=f"/v1/runs/{run_id}",
            response=ResolverRunResponse,
            json=None,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

        return response

    def _create_and_await_offline_query_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        optional_output_expressions: List[str],
        required_output_expressions: List[str],
        query_input: Optional[OfflineQueryInput],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: BranchId | None | ellipsis,
        context: OfflineQueryContext,
        output_id: bool,
        output_ts: Union[bool, str],
        preview_deployment_id: Optional[str],
        tags: Optional[List[str]],
        timeout: float | timedelta | ellipsis | None,
    ) -> pd.DataFrame:
        if branch is ...:
            branch = self._branch
        req = CreateOfflineQueryJobRequest(
            output=optional_output,
            output_expressions=optional_output_expressions,
            required_output=required_output,
            required_output_expressions=required_output_expressions,
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
            recompute_features=True,
            tags=tags,
        )
        response = self._create_offline_query_job(
            request=req,
            context=context,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response)
        if timeout is None:
            deadline = None
        else:
            if timeout is ...:
                timeout = self.default_status_report_timeout
            if not isinstance(timeout, timedelta):
                timeout = timedelta(seconds=timeout)
            deadline = datetime.now() + timeout
        while deadline is None or datetime.now() < deadline:
            status = self.get_job_status_v4(
                request=DatasetJobStatusRequest(
                    job_id=str(response.job_id),
                    ignore_errors=False,
                    query_inputs=False,
                ),
                environment=context and context.environment,
                branch=branch,
            )
            if status.is_finished:
                break
            time.sleep(0.5)
        else:
            raise TimeoutError(
                "Offline query job did not complete before timeout. The job may have failed or may still be running."
            )
        if status.errors:
            raise ChalkBaseException(errors=status.errors)
        return load_dataset(
            uris=status.urls,
            output_features=[*optional_output, *required_output],
            version=DatasetVersion(status.version),
            output_id=output_id,
            output_ts=output_ts,
            columns=status.columns,
            return_type="pandas",
        )

    @overload
    def load_dataset(
        self,
        job_id: uuid.UUID,
        outputs: Sequence[str] | None,
        output_id: bool,
        output_ts: bool | str,
        context: Optional[OfflineQueryContext],
        branch: Optional[BranchId],
        ignore_errors: bool,
        query_inputs: bool,
        return_type: Literal["polars_dataframe"],
    ) -> pl.DataFrame:
        ...

    @overload
    def load_dataset(
        self,
        job_id: uuid.UUID,
        outputs: Sequence[str] | None,
        output_id: bool,
        output_ts: bool | str,
        context: Optional[OfflineQueryContext],
        branch: Optional[BranchId],
        ignore_errors: bool,
        query_inputs: bool,
        return_type: Literal["polars_lazyframe"],
    ) -> pl.LazyFrame:
        ...

    @overload
    def load_dataset(
        self,
        job_id: uuid.UUID,
        outputs: Sequence[str] | None,
        output_id: bool,
        output_ts: bool | str,
        context: Optional[OfflineQueryContext],
        branch: Optional[BranchId],
        ignore_errors: bool,
        query_inputs: bool,
        return_type: Literal["pandas"],
    ) -> pd.DataFrame:
        ...

    @overload
    def load_dataset(
        self,
        job_id: uuid.UUID,
        outputs: Sequence[str] | None,
        output_id: bool,
        output_ts: bool | str,
        context: Optional[OfflineQueryContext],
        branch: Optional[BranchId],
        ignore_errors: bool,
        query_inputs: bool,
        return_type: Literal["pyarrow"],
    ) -> pa.Table:
        ...

    def load_dataset(
        self,
        job_id: uuid.UUID,
        outputs: Sequence[str] | None,
        output_id: bool,
        output_ts: bool | str,
        context: Optional[OfflineQueryContext],
        branch: Optional[BranchId],
        ignore_errors: bool,
        query_inputs: bool,
        return_type: Literal["polars_dataframe", "polars_lazyframe", "pandas", "pyarrow"],
    ) -> pa.Table | pl.LazyFrame | pl.DataFrame | pd.DataFrame:
        status = self.get_job_status_v4(
            request=DatasetJobStatusRequest(
                job_id=str(job_id),
                ignore_errors=ignore_errors,
                query_inputs=query_inputs,
            ),
            environment=context and context.environment,
            branch=branch,
        )
        return load_dataset(
            uris=status.urls,
            output_features=outputs,
            return_type=return_type,
            version=DatasetVersion(status.version),
            columns=status.columns,
            output_id=output_id,
            output_ts=output_ts,
        )

    def load_schema(
        self,
        job_id: uuid.UUID,
        context: OfflineQueryContext,
        branch: Optional[BranchId],
        ignore_errors: bool,
    ) -> pa.Schema:
        status = self.get_job_status_v4(
            request=DatasetJobStatusRequest(
                job_id=str(job_id),
                ignore_errors=ignore_errors,
                query_inputs=False,
            ),
            environment=context and context.environment,
            branch=branch,
        )
        return load_schema(status.urls)

    def recompute_dataset(
        self,
        dataset_name: Optional[str],
        revision_id: uuid.UUID,
        features: List[Union[str, Any]] | None,
        branch: BranchId | None,
        environment: Optional[EnvironmentId],
        num_shards: int,
        correlation_id: str | None = None,
        wait: bool = False,
        show_progress: bool | ellipsis = ...,
        store_plan_stages: bool = False,
        explain: bool = False,
        tags: Optional[List[str]] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        run_asynchronously: bool = False,
        timeout: float | timedelta | ellipsis | None = ...,
    ) -> DatasetImpl:
        encoded_outputs = encode_outputs((features or []))
        output_root_fqns = encoded_outputs.string_outputs
        output_expressions = encoded_outputs.feature_expressions_base64
        req = CreateOfflineQueryJobRequest(
            output=output_root_fqns,
            output_expressions=output_expressions,
            required_output=[],
            destination_format="PARQUET",
            # server will understand that we have num_shards
            input=(
                UploadedParquetShardedOfflineQueryInput(
                    filenames=tuple("" for _ in range(num_shards)),
                    version=OfflineQueryGivensVersion.SINGLE_TS_COL_NAME_WITH_URI_PREFIX,
                )
                if run_asynchronously
                else None
            ),
            dataset_name=dataset_name,
            branch=branch,
            recompute_features=output_root_fqns if len(output_root_fqns) > 0 else True,
            store_plan_stages=store_plan_stages,
            correlation_id=correlation_id,
            explain=explain,
            tags=tags,
            required_resolver_tags=required_resolver_tags,
            use_multiple_computers=run_asynchronously,
            planner_options=planner_options,
            recompute_request_revision_id=str(revision_id),
        )
        response = self._create_dataset_request(
            request=req,
            context=OfflineQueryContext(environment=environment),
            preview_deployment_id=None,
            branch=branch,
        )
        self._raise_if_200_with_non_resolver_errors(response=response)

        initialized_dataset = dataset_from_response(response, self)

        revision = initialized_dataset.revisions[-1]
        assert isinstance(revision, DatasetRevisionImpl)
        # Storing timeout for when we call dataset revision methods that
        # require polling
        revision.timeout = timeout
        revision.show_progress = show_progress

        if not wait:
            return initialized_dataset

        revision.wait_for_completion(
            show_progress=show_progress if isinstance(show_progress, bool) else True,
            timeout=timeout,
            caller_method="recompute",
        )
        initialized_dataset.is_finished = True
        return initialized_dataset

    def _upload_offline_query_input(
        self,
        offline_query_inputs: Sequence[tuple[QueryInput, QueryInputTime]],
        context: OfflineQueryContext,
        branch: BranchId | ellipsis | None,
        executor: ThreadPoolExecutor,
        num_shards: int | None = None,
    ) -> UploadedParquetShardedOfflineQueryInput:
        tables = _offline_query_inputs_to_parquet(offline_query_inputs)
        if num_shards is not None:
            if len(tables) != 1:
                raise ValueError(
                    f"The inputs for this query have already been partitioned into {len(tables)} shards. "
                    + f"The number of shards explicitly specified ({num_shards}) will be ignored."
                )
            elif num_shards > tables[0].num_rows:
                raise ValueError(
                    f"The number of shards ({num_shards}) is greater than the number of rows in the input data ({tables[0].num_rows}). "
                    + "Please specify a smaller number of shards."
                )
            else:
                tables = chunk_table(tables[0], num_shards)
        num_partitions = num_shards or len(offline_query_inputs)
        url_response = self._get_offline_query_input_upload_url(
            num_partitions=num_partitions,
            context=context,
            branch=branch,
        )
        if len(tables) != len(url_response.urls):
            raise ValueError(
                f"The number of signed upload URLs is {len(url_response.urls)}; the number of input partitions ({num_partitions}) must be equal. "
            )

        futs: List[Future[None]] = []
        for annotated_url, table in zip(url_response.urls, tables):
            futs.append(
                executor.submit(
                    _upload_table_parquet,
                    table,
                    annotated_url.signed_url,
                )
            )
        for fut in futs:
            fut.result()
        return UploadedParquetShardedOfflineQueryInput(
            filenames=tuple(annotated_url.filename for annotated_url in url_response.urls),
            version=OfflineQueryGivensVersion.SINGLE_TS_COL_NAME_WITH_URI_PREFIX,
        )

    def _get_offline_query_input_upload_url(
        self,
        num_partitions: int,
        context: OfflineQueryContext,
        branch: BranchId | ellipsis | None,
    ) -> OfflineQueryParquetUploadURLResponse:
        response = self._request(
            method="GET",
            uri=f"/v1/offline_query_parquet_upload_url/{num_partitions}",
            json=None,
            response=OfflineQueryParquetUploadURLResponse,
            environment_override=context.environment,
            preview_deployment_id=None,
            branch=branch,
            metadata_request=False,
        )
        self._raise_if_200_with_errors(response=response)
        return response

    def _create_dataset_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        query_input: Union[
            Tuple[OfflineQueryInput, ...],
            Optional[OfflineQueryInput],
            UploadedParquetShardedOfflineQueryInput,
            OfflineQueryInputUri,
        ],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: BranchId | ellipsis | None,
        context: OfflineQueryContext,
        correlation_id: Optional[str] = None,
        query_context: ContextJsonDict | None = None,
        recompute_features: Union[bool, List[FeatureReference]] = False,
        sample_features: Optional[List[FeatureReference]] = None,
        lower_bound: datetime | timedelta | None = None,
        upper_bound: datetime | timedelta | None = None,
        store_plan_stages: bool = False,
        explain: bool = False,
        tags: Optional[List[str]] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        run_asynchronously: bool = False,
        spine_sql_query: str | None = None,
        resources: ResourceRequests | None = None,
        env_overrides: Optional[Dict[str, str]] = None,
        enable_profiling: bool = False,
        store_online: bool = False,
        store_offline: bool = False,
        override_target_image_tag: Optional[str] = None,
        num_shards: int | None = None,
        num_workers: int | None = None,
        feature_for_lower_upper_bound: Optional[str] = None,
        completion_deadline: timedelta | None = None,
        max_retries: int | None = None,
        optional_output_expressions: Optional[List[str]] = None,
        required_output_expressions: Optional[List[str]] = None,
        use_job_queue: bool = False,
    ) -> DatasetResponse:
        if not (
            isinstance(recompute_features, list)
            or isinstance(recompute_features, bool)  # pyright: ignore[reportUnnecessaryIsInstance]
        ):
            raise ValueError("The value for 'recompute_features' must be either a bool for a list of features.")
        if sample_features is not None and not isinstance(
            sample_features, list
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("The value for 'sample_features' must be a list of features.")
        if isinstance(recompute_features, list):
            recompute_features = [
                unwrap_feature(f).fqn if isinstance(f, FeatureWrapper) else f for f in recompute_features
            ]
        if isinstance(sample_features, list):
            sample_features = [unwrap_feature(f).fqn if isinstance(f, FeatureWrapper) else f for f in sample_features]
        if isinstance(recompute_features, list) and isinstance(sample_features, list):
            intersection = set(recompute_features) & set(sample_features)
            if len(intersection) > 0:
                raise ValueError(
                    "Features in 'recompute_features' and 'sample_features' arguments must not overlap. "
                    + f"Intersection as specified is {sorted(list(intersection))}"
                )

        def process_bound(bound: datetime | timedelta | None) -> str | None:
            if isinstance(bound, datetime):
                if bound.tzinfo is None:
                    bound = bound.astimezone()
                return bound.isoformat()
            if isinstance(bound, timedelta):
                return TIMEDELTA_PREFIX + timedelta_to_duration(bound)
            return None

        lower_bound_str = process_bound(lower_bound)
        upper_bound_str = process_bound(upper_bound)
        if branch is ...:
            branch = self._branch
        req = CreateOfflineQueryJobRequest(
            output=optional_output,
            output_expressions=optional_output_expressions or [],
            required_output=required_output,
            required_output_expressions=required_output_expressions or [],
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
            recompute_features=recompute_features,
            sample_features=sample_features,
            observed_at_lower_bound=lower_bound_str,
            observed_at_upper_bound=upper_bound_str,
            store_plan_stages=store_plan_stages,
            correlation_id=correlation_id,
            query_context=query_context,
            explain=explain,
            tags=tags,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            use_multiple_computers=run_asynchronously,
            spine_sql_query=spine_sql_query,
            resources=resources,
            env_overrides=env_overrides,
            enable_profiling=enable_profiling,
            store_online=store_online,
            store_offline=store_offline,
            override_target_image_tag=override_target_image_tag,
            num_shards=num_shards,
            num_workers=num_workers,
            feature_for_lower_upper_bound=feature_for_lower_upper_bound,
            completion_deadline=timedelta_to_duration(completion_deadline) if completion_deadline is not None else None,
            max_retries=max_retries,
            use_job_queue=use_job_queue,
            overlay_graph=_get_overlay_graph_b64(),
        )

        response = self._create_dataset_request(
            request=req,
            context=context,
            preview_deployment_id=None,
            branch=branch,
        )
        self._raise_if_200_with_non_resolver_errors(response=response)
        return response

    def compute_resolver_output(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pl.DataFrame, pd.DataFrame, DataFrame],
        input_times: List[datetime],
        resolver: str,
        context: Optional[OfflineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        branch: BranchId | None | ellipsis = ...,
        timeout: timedelta | float | ellipsis | None = ...,
    ) -> pl.DataFrame:
        if context is None:
            context = OfflineQueryContext()
        query_input = _to_offline_query_input(input, input_times)
        request = ComputeResolverOutputRequest(input=query_input, resolver_fqn=resolver)
        response = self._request(
            method="POST",
            uri="/v1/compute_resolver_output",
            json=request,
            response=ComputeResolverOutputResponse,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response)

        if timeout is None:
            deadline = None
        else:
            if timeout is ...:
                timeout = self.default_status_report_timeout
            if not isinstance(timeout, timedelta):
                timeout = timedelta(seconds=timeout)
            deadline = datetime.now() + timeout
        while deadline is None or datetime.now() < deadline:
            status = self._get_compute_job_status(
                job_id=response.job_id,
                context=context,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
                timeout=None if timeout is None else timeout.total_seconds(),
            )
            if status.is_finished:
                break
            time.sleep(0.5)
        else:
            raise TimeoutError(
                f"Computing outputs for resolver {resolver} did not finish before the timeout. The job may still be running or may have failed."
            )

        return load_dataset(
            uris=status.urls,
            version=status.version,
            executor=None,
            columns=status.columns,
            return_type="polars_dataframe",
        )

    def create_branch(
        self,
        branch_name: str,
        create_only: bool = False,
        switch: bool = True,
        source_deployment_id: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
    ) -> BranchDeployResponse:
        available_branches = self.get_branches()
        if branch_name in available_branches and create_only:
            raise RuntimeError(
                (
                    f"The branch `{branch_name}` already exists."
                    f" To connect your client to an existing branch, specify the 'branch' parameter when "
                    f"creating a ChalkClient. Available branches are: {available_branches}"
                )
            )

        request = BranchDeployRequest(
            branch_name=branch_name,
            create_only=create_only,
            source_deployment_id=source_deployment_id,
        )
        try:
            resp = self._request(
                method="POST",
                uri=f"/v1/branches/{branch_name}/source",
                response=BranchDeployResponse,
                json=request,
                branch=...,
                environment_override=environment,
                preview_deployment_id=None,
            )
        except ChalkBaseException as e:
            raise ChalkCustomException.from_base(e, f"Failed to deploy branch `{branch_name}`.")

        if notebook.is_notebook():
            self._display_branch_creation_response(resp)

            if switch:
                self.set_branch(branch_name)
            else:
                self._display_button_to_change_branch(branch_name)
        return resp

    def _display_branch_creation_response(self, resp: BranchDeployResponse):
        from IPython.display import display_markdown

        if resp.new_branch_created:
            prefix = "Created new "
        else:
            prefix = "Deployed "
        text = f"{prefix} branch `{resp.branch_name}` with source from deployment `{resp.source_deployment_id}`."
        display_markdown(text, raw=True)

    def _display_button_to_change_branch(self, branch_name: str):
        if not notebook.is_notebook():
            return
        try:
            from IPython.core.display_functions import display
            from ipywidgets import widgets

            layout = widgets.Layout(width="auto")
            button0 = widgets.Button(
                description=f"Set current branch to '{branch_name}'",
                tooltip=f'Equivalent to client.set_branch("{branch_name}")',
                layout=layout,
            )
            output0 = widgets.Output()
            display(button0, output0)

            def on_button_clicked0(_):
                with output0:
                    old_branch = self._branch
                    self._branch = branch_name
                    old_branch_text = ""
                    if old_branch is not None:
                        old_branch_text = f" from `{old_branch}`"
                    from IPython.display import display_markdown

                    display_markdown(f"Set branch for Chalk client{old_branch_text} to `{branch_name}`.", raw=True)

            button0.on_click(on_button_clicked0)
        except Exception:
            pass

    def get_or_create_branch(
        self,
        branch_name: str,
        source_branch_name: Optional[str] = None,
        source_deployment_id: Optional[str] = None,
    ):
        available_branches = self.get_branches()

        if source_branch_name is not None and source_deployment_id is not None:
            raise RuntimeError(
                "Both 'source_branch_name' and 'source_deployment_id' cannot be specified at the same time."
            )

        if branch_name in available_branches:
            print(
                (
                    f"Branch {branch_name} already exists. Client is being updated to point to that branch, "
                    "but a new deployment is not being created."
                )
            )

        else:
            try:
                from rich.console import Console

                from chalk.client.client_grpc import ChalkGRPCClient

                client_grpc = ChalkGRPCClient(
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                    environment=self._primary_environment,
                    api_server=self._api_server,
                )

                console = Console()
                with console.status(f"Creating branch `{branch_name}`", spinner="dots"):
                    resp = client_grpc._create_branch(  # type: ignore
                        branch_name=branch_name,
                        source_branch_name=source_branch_name,
                        source_deployment_id=source_deployment_id,
                    )
                if resp.branch_already_exists:
                    print(
                        (
                            f"Created a new branch deployment on `{branch_name}`, but `{branch_name}` already existed. "
                            "It is possible someone recently created this branch."
                        )
                    )

                if resp.errors:
                    raise ChalkBaseException(errors=resp.errors)

            except ChalkBaseException as e:
                raise ChalkCustomException.from_base(e, f"Failed to deploy branch `{branch_name}`.")

        self.set_branch(branch_name)

    def _get_compute_job_status(
        self,
        job_id: str,
        context: OfflineQueryContext,
        preview_deployment_id: str | None | ellipsis,
        branch: BranchId | None | ellipsis,
        timeout: float | None | ellipsis,
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v1/compute_resolver_output/{job_id}",
            response=GetOfflineQueryJobResponse,
            json=None,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            timeout=timeout,
        )

    def _create_dataset_request(
        self,
        request: CreateOfflineQueryJobRequest,
        context: OfflineQueryContext,
        preview_deployment_id: str | None,
        branch: BranchId | None | ellipsis,
    ) -> DatasetResponse:
        response = self._request(
            method="POST",
            uri="/v4/offline_query",
            json=request,
            response=DatasetResponse,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            # If using multiple computers, then we must route through the metadata server
            # So we can actually spin up multiple pods
            metadata_request=request.use_multiple_computers,
        )
        return response

    def _create_offline_query_job(
        self,
        request: CreateOfflineQueryJobRequest,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId] = None,
    ):
        response = self._request(
            method="POST",
            uri="/v2/offline_query",
            json=request,
            response=CreateOfflineQueryJobResponse,
            environment_override=context.environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        return response

    def get_job_status_v4(
        self, request: DatasetJobStatusRequest, environment: Optional[EnvironmentId], branch: Optional[BranchId]
    ) -> GetOfflineQueryJobResponse:
        from tenacity import Retrying, retry_if_exception_message, stop_after_attempt
        from tenacity.wait import wait_exponential_jitter

        for attempt in Retrying(
            stop=stop_after_attempt(5),
            wait=wait_exponential_jitter(),
            reraise=True,
            retry=retry_if_exception_message(match="504"),
        ):
            with attempt:
                return self._request(
                    method="POST",
                    uri="/v4/offline_query/status",
                    response=GetOfflineQueryJobResponse,
                    environment_override=environment,
                    json=request,
                    preview_deployment_id=None,
                    branch=branch,
                )
        raise ValueError("Unreachable code path reached")

    def get_revision_summary(
        self,
        revision_id: str,
        environment: Optional[EnvironmentId],
    ) -> DatasetRevisionSummaryResponse:
        return self._request(
            method="GET",
            uri=f"/v4/offline_query/{revision_id}/summary",
            response=DatasetRevisionSummaryResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=None,
        )

    def get_revision_preview(
        self,
        revision_id: str,
        environment: Optional[EnvironmentId],
    ) -> DatasetRevisionPreviewResponse:
        return self._request(
            method="GET",
            uri=f"/v4/offline_query/{revision_id}/preview",
            response=DatasetRevisionPreviewResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=None,
        )

    def _get_query_inputs(
        self, job_id: uuid.UUID, environment: Optional[EnvironmentId], branch: Optional[BranchId]
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v2/offline_query_inputs/{job_id}",
            response=GetOfflineQueryJobResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=branch,
        )

    def _get_dataset_from_name_or_id(
        self,
        *,
        dataset_name_or_id: str,
        environment: Optional[EnvironmentId],
        branch: Optional[BranchId],
    ) -> DatasetResponse:
        return self._request(
            method="GET",
            uri=f"/v3/offline_query/{dataset_name_or_id}",
            response=DatasetResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=branch,
        )

    def _get_dataset_from_job_id(
        self,
        *,
        job_id: str | uuid.UUID,
        environment: Optional[EnvironmentId],
        branch: Optional[BranchId],
    ) -> DatasetResponse:
        return self._request(
            method="GET",
            uri=f"/v4/offline_query/{job_id}",
            response=DatasetResponse,
            environment_override=environment,
            json=None,
            preview_deployment_id=None,
            branch=branch,
        )

    def get_anonymous_dataset(
        self, revision_id: str, environment: Optional[EnvironmentId], branch: Optional[BranchId]
    ) -> DatasetImpl:
        try:
            response = self._get_dataset_from_job_id(
                job_id=revision_id,
                environment=environment,
                branch=branch,
            )
        except ChalkBaseException as e:
            raise ChalkCustomException.from_base(
                e,
                message=f"Failed to get dataset for revision id '{revision_id}'.",
            )

        return dataset_from_response(response, self)

    def get_batch_report(
        self, operation_id: uuid.UUID, environment_id: EnvironmentId, computer_id: int
    ) -> Optional[BatchReport]:
        if computer_id == 0:
            uri = f"/v4/offline_query/{operation_id}/status"
        else:
            uri = f"/v4/offline_query/{operation_id}/status/{computer_id}"
        try:
            response = self._request(
                method="GET",
                uri=uri,
                response=BatchReportResponse,
                json=None,
                metadata_request=True,
                environment_override=environment_id,
                preview_deployment_id=None,
                branch=None,  # request should always go to api server
            )
        except Exception:
            return None

        return response.report

    def get_resolver_replay(
        self,
        environment_id: EnvironmentId,
        revision_id: uuid.UUID,
        resolver_fqn: str,
        branch: Optional[BranchId],
        timeout: float | timedelta | ellipsis | None,
    ) -> ResolverReplayResponse:
        if timeout is None:
            deadline = None
        else:
            if timeout is ...:
                timeout = self.default_status_report_timeout
            if not isinstance(timeout, timedelta):
                timeout = timedelta(seconds=timeout)
            deadline = datetime.now() + timeout
        while deadline is None or datetime.now() < deadline:
            status = self.get_job_status_v4(
                request=DatasetJobStatusRequest(
                    job_id=str(revision_id),
                    ignore_errors=False,
                    query_inputs=False,
                ),
                environment=environment_id,
                branch=branch,
            )
            if status.is_finished:
                break
            time.sleep(0.5)
        else:
            raise TimeoutError("Resolver replay timed out. The job may still be running or may have failed.")
        return self._request(
            method="GET",
            uri=f"/v4/resolver_replay/{revision_id}/{resolver_fqn}",
            response=ResolverReplayResponse,
            json=None,
            preview_deployment_id=None,
            environment_override=environment_id,
            branch=branch,
        )

    def await_operation_completion(
        self,
        operation_id: uuid.UUID,
        environment_id: EnvironmentId,
        show_progress: bool,
        caller_method: Optional[str],
        num_computers: int,
        timeout: float | timedelta | ellipsis | None,
        raise_on_dataset_failure: bool,
    ):
        if timeout is ...:
            timeout = self.default_status_report_timeout

        ProgressService(
            operation_id=operation_id,
            client=self,
            caller_method=caller_method,
            environment_id=environment_id,
            num_computers=num_computers,
            show_progress=show_progress,
        ).await_operation(
            must_fail_on_resolver_error=raise_on_dataset_failure,
            timeout=timeout,
        )

    def _get_upsert_graph_gql_from_branch(
        self,
        branch: Union[BranchId, ellipsis, None] = ...,
        environment: Optional[EnvironmentId] = None,
    ) -> dict:
        if branch is ...:
            branch = self._branch
        if branch is None:
            raise RuntimeError(
                "No branch specified or set in client. This method only works for branch deployments. Please specify `branch=<branch_name>`"
            )
        available_branches = self.get_branches()
        if branch not in available_branches:
            raise RuntimeError(
                (
                    f"The branch `{branch}` does not exist. "
                    f"Available branches are: {available_branches}. "
                    f"To create a branch, use `ChalkClient.create_branch(...)`"
                )
            )
        result = self._request(
            method="GET",
            uri=f"/v1/branch/{branch}/graph_gql",
            environment_override=environment,
            branch=branch,
            response=None,  # get the JSON
            preview_deployment_id=None,
            json=None,
        )
        try:
            return result.json()
        except requests.exceptions.JSONDecodeError as e:
            result.raise_for_status()
            raise ValueError(f"Unexpected response when getting branch: {result.status_code} {result.text}") from e

    def reset_branch(self, branch: BranchIdParam = ..., environment: Optional[EnvironmentId] = None):
        if branch is ...:
            branch = self._branch
        if branch is None:
            raise RuntimeError(
                "No branch specified or set in client. This method only works for branch deployments. Please specify `branch=<branch_name>`"
            )
        available_branches = self.get_branches()
        if branch not in available_branches:
            raise RuntimeError(
                (
                    f"The branch `{branch}` does not exist. "
                    f"Available branches are: {available_branches}. "
                    f"To create a branch, use `ChalkClient.create_branch(...)`"
                )
            )
        self._request(
            method="POST",
            uri=f"/v1/branch/{branch}/reset",
            environment_override=environment,
            branch=branch,
            response=None,
            preview_deployment_id=None,
            json=None,
        )

    def branch_state(
        self,
        branch: Union[BranchId, ellipsis, None] = ...,
        environment: Optional[EnvironmentId] = None,
    ) -> BranchGraphSummary:
        if branch is ...:
            branch = self._branch
        if branch is None:
            raise RuntimeError(
                "No branch specified or set in client. This method only works for branch deployments. Please specify `branch=<branch_name>`"
            )
        available_branches = self.get_branches()
        if branch not in available_branches:
            raise RuntimeError(
                (
                    f"The branch `{branch}` does not exist. "
                    f"Available branches are: {available_branches}. "
                    f"To create a branch, use `ChalkClient.create_branch(...)`"
                )
            )
        result = self._request(
            method="GET",
            uri=f"/v1/branch/{branch}/graph_state",
            environment_override=environment,
            branch=branch,
            response=None,  # get the JSON
            preview_deployment_id=None,
            json=None,
        )
        try:
            resp_json = result.json()
        except requests.exceptions.JSONDecodeError as e:
            result.raise_for_status()
            raise RuntimeError(
                f"Unexpected result when getting branch state: {result.status_code} {result.text}"
            ) from e
        return BranchGraphSummary.from_dict(resp_json)  # type: ignore

    def test_streaming_resolver(
        self,
        resolver: Union[str, Resolver],
        num_messages: Optional[int] = None,
        message_filepath: Optional[str] = None,
        message_keys: Optional[List[Optional[str]]] = None,
        message_bodies: Optional[List[Union[str, bytes, BaseModel]]] = None,
        message_timestamps: Optional[List[Union[str, datetime]]] = None,
        branch: Union[BranchId, ellipsis, None] = ...,
        environment: Optional[EnvironmentId] = None,
        kafka_auto_offset_reset: Optional[Literal["earliest", "latest"]] = "earliest",
    ) -> StreamResolverTestResponse:
        resolver_fqn = resolver.fqn if isinstance(resolver, Resolver) else resolver
        if num_messages is None and message_filepath is None and message_bodies is None:
            raise ValueError("One of 'num_messages', 'message_filepath', or 'message_bodies' must be provided.")
        payloads = (
            self._validate_test_stream_resolver_inputs(
                message_filepath=message_filepath,
                message_keys=message_keys,
                message_bodies=message_bodies,
                message_timestamps=message_timestamps,
            )
            if message_bodies is not None or message_filepath is not None
            else None
        )
        request = StreamResolverTestRequest(
            resolver_fqn=resolver_fqn,
            num_messages=num_messages,
            test_messages=payloads,
            kafka_auto_offset_reset=kafka_auto_offset_reset,
        )
        result = self._request(
            method="POST",
            uri="/v1/test_stream_resolver",
            environment_override=environment,
            json=request,
            branch=branch,
            response=StreamResolverTestResponse,
            preview_deployment_id=None,
        )
        return result

    def _validate_test_stream_resolver_inputs(
        self,
        message_filepath: Optional[str] = None,
        message_keys: Optional[List[Optional[str]]] = None,
        message_bodies: Optional[List[Union[str, bytes, BaseModel]]] = None,
        message_timestamps: Optional[List[Union[str, datetime]]] = None,
    ) -> List[StreamResolverTestMessagePayload]:
        if message_filepath and (message_keys or message_bodies):
            raise ValueError("Only one of 'message_filepath' or ('message_keys' and 'message_bodies') can be provided.")
        if message_filepath:
            message_keys = []
            message_bodies = []
            message_timestamps = []
            with open(message_filepath) as file:
                for i, line in enumerate(file):
                    try:
                        json_message = json.loads(line.rstrip())
                        if "message_body" not in json_message:
                            raise ValueError(f"Key 'message_body' missing from line {i + 1}")
                        message_keys.append(json_message.get("message_key"))
                        message_body = json_message["message_body"]
                        if isinstance(message_body, str):
                            message_bodies.append(message_body)  # Already a JSON string
                        else:
                            message_bodies.append(json.dumps(message_body))  # Convert object to JSON string
                        if "message_timestamp" in json_message:
                            timestamp_string = json_message["message_timestamp"]
                            message_timestamps.append(timestamp_string)
                    except Exception as e:
                        raise ValueError(f"Could not parse line {line} from file {message_filepath}: error {e}")

        if message_bodies is None or len(message_bodies) == 0:
            raise ValueError("No message bodies provided")
        if message_keys is None:
            message_keys_list = [None] * len(message_bodies)
        else:
            message_keys_list = message_keys
        if len(message_keys_list) != len(message_bodies):
            raise ValueError(
                (
                    "The length of 'message_keys' and the length of 'message_bodies' must be equal and nonzero. "
                    + f"{len(message_keys_list)} != {len(message_bodies)}"
                )
            )
        if message_timestamps and len(message_bodies) != len(message_timestamps):
            raise ValueError(
                (
                    "The length of 'message_keys' and the length of 'message_timestamps' must be equal and nonzero. "
                    + f"{len(message_bodies)} != {len(message_bodies)}"
                )
            )
        if message_timestamps:
            timestamp_datetimes = []
            for timestamp in message_timestamps:
                try:
                    if isinstance(timestamp, str):
                        timestamp = parser.parse(timestamp)
                    if not isinstance(timestamp, datetime):  # pyright: ignore[reportUnnecessaryIsInstance]
                        raise ValueError(f"value '{timestamp}' must be a datetime")
                    if timestamp.tzinfo is None:
                        raise ValueError(f"value '{timestamp}' must be timezone aware")
                    timestamp_datetimes.append(timestamp)
                except Exception as e:
                    raise ValueError(f"Could not parse value '{timestamp}' as timezone-aware timestamp, {e}")
        else:
            timestamp_datetimes = [None] * len(message_bodies)

        payloads: List[StreamResolverTestMessagePayload] = []
        first_type = type(message_bodies[0])
        for i, (message, key, timestamp) in enumerate(
            zip(message_bodies, message_keys_list, timestamp_datetimes, strict=True)
        ):
            if not isinstance(message, first_type):
                raise ValueError(
                    f"All messages must be of the same type. Found {type(message)} for message at index {i},"
                    + f" while the first message (index 0) has type {first_type}"
                )
            if isinstance(message, bytes):
                payloads.append(
                    StreamResolverTestMessagePayload(
                        key=key,
                        message_str=None,
                        message_bytes=base64.b64encode(message).decode("utf-8"),
                        timestamp=timestamp,
                    )
                )
            elif isinstance(message, BaseModel):
                payloads.append(
                    StreamResolverTestMessagePayload(
                        key=key,
                        message_str=message.json(),
                        message_bytes=None,
                        timestamp=timestamp,
                    )
                )
            else:  # str
                payloads.append(
                    StreamResolverTestMessagePayload(
                        key=key,
                        message_str=str(message),
                        message_bytes=None,
                        timestamp=timestamp,
                    )
                )

        return payloads

    @override
    def plan_query(
        self,
        input: Sequence[FeatureReference],
        output: Sequence[FeatureReference],
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
        preview_deployment_id: str | None | ellipsis = ...,
        branch: str | None | ellipsis = ...,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
        store_plan_stages: bool = False,
        explain: bool = False,
        num_input_rows: Optional[int] = None,
        headers: Mapping[str, str] | None = None,
    ) -> PlanQueryResponse:
        encoded_inputs = encode_outputs(input).string_outputs
        outputs = encode_outputs(output).string_outputs
        if branch is ...:
            branch = self._branch

        if preview_deployment_id is ...:
            preview_deployment_id = self._preview_deployment_id

        staleness_encoded = {}
        if staleness is not None:
            for k, v in staleness.items():
                if is_feature_set_class(k):
                    for f in k.features:
                        staleness_encoded[f.root_fqn] = v
                else:
                    staleness_encoded[ensure_feature(k).root_fqn] = v

        request = PlanQueryRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            staleness=staleness_encoded,
            context=OnlineQueryContext(
                environment=environment,
                tags=tags,
            ),
            deployment_id=preview_deployment_id,
            branch_id=branch,
            query_name=query_name,
            query_name_version=query_name_version,
            meta=meta,
            store_plan_stages=store_plan_stages,
            explain=explain,
            num_input_rows=num_input_rows,
        )

        extra_headers: dict[str, str] = {}
        if query_name is not None:
            extra_headers["X-Chalk-Query-Name"] = query_name
        if headers:
            extra_headers.update(headers)

        resp = self._request(
            method="POST",
            uri="/v1/query/plan",
            json=request,
            response=PlanQueryResponse,
            environment_override=environment,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
            metadata_request=False,
            extra_headers=extra_headers,
        )
        return resp

    def _to_value(self, x: FeatureResult):
        f: Feature = Feature.from_root_fqn(x.field)

        if f.is_has_many_subfeature:
            schema: dict[str, pl.PolarsDataType] = {}
            if isinstance(x.value, DataFrame):
                df = x.value.to_polars().collect()
            elif isinstance(x.value, pl.DataFrame):
                df = x.value
            else:
                for col in x.value["columns"]:
                    if col == INDEX_COL_NAME:
                        continue
                    sub_f: Feature = Feature.from_root_fqn(col)
                    assert sub_f.is_has_one or sub_f.is_feature_time or sub_f.is_has_one or sub_f.is_has_many
                    schema[col] = sub_f.converter.polars_dtype
                df = pl.DataFrame(
                    {col: x.value["values"][i] for (i, col) in enumerate(x.value["columns"]) if col != INDEX_COL_NAME},
                    schema=schema,
                )
            return df
        elif f.is_scalar or f.is_feature_time:
            return f.converter.from_rich_to_json(x.value)
        else:
            return x.value

    def check(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        assertions: Union[Mapping[FeatureReference, Any], Any],
        cache_hits: Iterable[str | Any] | None = None,
        feature_errors: Mapping[str | Any, Any] | None = None,
        query_errors: Optional[Collection[ChalkError]] = None,
        now: Optional[datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: float | ellipsis | None = ...,
        headers: Mapping[str, str] | None = None,
        query_context: Mapping[str, JsonValue] | str | None = None,
        value_metrics_tag_by_features: Sequence[FeatureReference] = (),
        show_table: bool = False,
        float_rel_tolerance: float = 1e-6,
        float_abs_tolerance: float = 1e-12,
        prefix: bool = True,
        show_matches: bool = True,
    ):
        from rich.console import Console
        from rich.table import Table

        from chalk.client._internal_models.check import Color, ManyQueryInputsCheckerWrapper, Result

        try:
            import polars as pl
            import polars.testing as pl_test
        except:
            raise missing_dependency_exception("chalkpy[runtime]")

        console = Console()

        if isinstance(input, ManyQueryInputsCheckerWrapper):
            is_many_query = True
            parsed_inputs = input.inputs
        else:
            is_many_query = False
            if isinstance(input, Features):
                input = {
                    k: getattr(input, k.attribute_name) for k in input.features if hasattr(input, k.attribute_name)
                }
            parsed_inputs = dict(input)
        del input

        feature_errors = {str(k): v for k, v in feature_errors.items()} if feature_errors else {}
        cache_hits = {str(v) for v in cache_hits} if cache_hits else set()

        if is_many_query and isinstance(assertions, DataFrame):
            outputs = list(assertions.to_polars().columns)
        elif is_many_query and isinstance(assertions, pl.DataFrame):
            outputs = list(assertions.columns)
        else:
            values = {
                str(k): (ensure_feature(k).converter.from_rich_to_json(val, missing_value_strategy="allow"))
                for (k, val) in (
                    dict(assertions.items()).items()
                    if not is_many_query or not isinstance(assertions, list)
                    else (
                        {
                            k: [dict(feat.items())[k] for feat in assertions]
                            for k in dict(next(iter(assertions))).keys()
                        }.items()
                        if assertions
                        else {}
                    )
                )
            } or {}
            outputs = list(values.keys())

        staleness = None if staleness is None else {str(k): v for k, v in staleness.items()}
        all_keys = set(outputs)

        expected: list[Result] = []
        if not is_many_query:
            assert isinstance(values, dict)
            for key in all_keys:
                if is_many_query:
                    values_for_key = values.get(key)
                    assert (
                        values_for_key is not None
                    ), f"The feature {repr(key)} does not appear in the expected outputs {values}"
                else:
                    values_for_key = [values.get(key)]
                expected.extend(
                    [
                        Result(fqn=key, value=v, error=feature_errors.get(key, None), cache_hit=key in cache_hits)
                        for v in values_for_key  # type: ignore
                        if v is not ...
                    ]
                )

        if headers is None:
            headers = {}

        headers = dict(headers)

        if is_many_query:
            if isinstance(now, (str, datetime)):
                nows = [now] * len(next(iter(parsed_inputs.values())))
            else:
                nows = now
            if nows is not None:
                nows = [datetime.fromisoformat(now) if isinstance(now, str) else now for now in nows]
            assert not planner_options, "Planner options are not supported with query_bulk"

            resp = self.query_bulk(
                input=parsed_inputs,
                output=outputs,
                query_name=query_name,
                query_name_version=query_name_version,
                query_context=query_context,
                now=nows,
                staleness=staleness,
                tags=tags,
                headers=headers,
            )
            resp_errors = list(resp.global_errors)
            for x in resp.results:
                if x.errors:
                    resp_errors.extend(x.errors)
            resp_df = resp.results[0].scalars_df
            resp_data = None
            meta = resp.results[0].meta
            assert isinstance(meta, QueryMeta)
        else:
            assert isinstance(now, (str, datetime)) or now is None

            resp = self.query(
                input=parsed_inputs,
                output=outputs,
                query_name=query_name,
                query_name_version=query_name_version,
                query_context=query_context,
                now=datetime.fromisoformat(now) if isinstance(now, str) else now,
                staleness=staleness,
                tags=tags,
                planner_options=planner_options,
                include_meta=True,
                headers=headers,
            )
            resp_errors = list(resp.errors or ())
            resp_data = resp.data
            resp_df = None
            meta = resp.meta
            assert isinstance(meta, QueryMeta)

        def _canonicalize_error(x: ChalkError):
            return x.copy(
                update={
                    "exception": (
                        None
                        if x.exception is None
                        else x.exception.copy(update={"stacktrace": "", "internal_stacktrace": None})
                    ),
                    "feature": None,
                }
            )

        query_errors = FrozenOrderedSet(_canonicalize_error(x) for x in (query_errors or []))
        actual_errors = FrozenOrderedSet(_canonicalize_error(x) for x in (resp_errors or []))

        if not _do_query_errors_match(actual_errors, query_errors):
            errors_expected = len(query_errors) > 0

            safe = actual_errors & query_errors
            errors_table = Table(title="Chalk Query Error Check Table", title_justify="left")

            if errors_expected:
                errors_table.add_column("Kind", max_width=7)

            include_code = any(q.code for q in query_errors) or any(q.code for q in actual_errors)
            if include_code:
                errors_table.add_column("Code", max_width=32, overflow="fold")

            include_feature = any(q.feature for q in query_errors) or any(q.feature for q in actual_errors)
            if include_feature:
                errors_table.add_column("Feat", max_width=20, justify="left")

            include_resolver = any(q.resolver for q in query_errors) or any(q.resolver for q in actual_errors)
            if include_resolver:
                errors_table.add_column("Res", max_width=20, justify="left")

            errors_table.add_column("Message", justify="left", overflow="fold")

            include_exception = any(q.exception for q in query_errors) or any(q.exception for q in actual_errors)
            if include_exception:
                errors_table.add_column("Exc", max_width=30)

            table_errors = []
            for e in query_errors:
                if errors_expected:
                    row = [Color.render("Match", Color.G) if e in safe else Color.render("Expect", Color.R)]

                if include_code:
                    row.append(str(e.code))

                if include_feature:
                    row.append(e.feature and render_fqn(e.feature))

                if include_resolver:
                    row.append(e.resolver)

                row.append(e.message)

                if include_exception:
                    row.append(str(e.exception))

            for e in actual_errors:
                row = []
                if errors_expected and e not in safe:
                    row.append(Color.render("Expect", Color.R))

                if include_code:
                    row.append(str(e.code))

                if include_feature:
                    row.append(e.feature and render_fqn(e.feature))

                if include_resolver:
                    row.append(e.resolver)

                row.append(e.message)

                if include_exception:
                    row.append(str(e.exception))
                table_errors.append(row)

            # sorting by message, which is either the last or before last value in the row
            for row in sorted(table_errors, key=lambda k: k[(-1 - include_exception)]):
                errors_table.add_row(*row)

            print("\n")
            console.print(errors_table)
            _fail_test("errors differed -- see output table above")

        if resp_data is not None:
            actuals = [
                Result(
                    x.field,
                    self._to_value(x),
                    False if x.meta is None else x.meta.cache_hit,
                    x.error,
                )
                for x in resp_data
            ]

            feature_mismatch = not _do_resultsets_match(actuals, expected)
            if feature_mismatch or show_table:
                no_expectations = len(expected) == 0

                result_table = Table(title="Chalk Feature Value Check Table", title_justify="left")
                result_table.add_column("Kind", max_width=10)
                result_table.add_column("Name", overflow="fold", max_width=100)
                result_table.add_column("Value", max_width=60)
                safe = []

                for x in actuals:
                    if any(_does_result_match(x, e) for e in expected):
                        safe.append(x.fqn)  # use fqns, since __eq__ might behave weirdly for feature values

                include_errors = any(k.error for k in expected) or any(k.error for k in actuals)
                if include_errors:
                    result_table.add_column("Err", max_width=60)

                include_cache = any(k.cache_hit for k in expected) or any(k.cache_hit for k in actuals)
                if include_cache:
                    result_table.add_column("Cache Hit", max_width=5, justify="center")

                table_results = []
                for k in expected:
                    fqn = k.fqn and render_fqn(k.fqn)
                    is_safe = k.fqn in safe
                    if is_safe and not show_matches:
                        continue
                    row = [
                        Color.render("Match", Color.G) if is_safe else Color.render("Expect", Color.R),
                        fqn if prefix else fqn.split(".")[-1],
                        str(k.value),
                    ]
                    if include_errors:
                        row.append(str(k.error))
                    if include_cache:
                        row.append("✓" if k.cache_hit else "")
                    table_results.append(row)

                for k in actuals:
                    if k.fqn in safe:
                        continue
                    fqn = k.fqn and render_fqn(k.fqn)
                    row = [
                        Color.render("Actual", Color.G if k.fqn in safe or no_expectations else Color.R),
                        fqn if prefix else fqn.split(".")[-1],
                        str(k.value),
                    ]
                    if include_errors:
                        row.append(str(k.error))
                    if include_cache:
                        row.append("✓" if k.cache_hit else "")
                    table_results.append(row)

                for row in sorted(table_results, key=lambda k: k[1]):
                    result_table.add_row(*row)

                print("\n")
                console.print(result_table)
                if feature_mismatch and not no_expectations:
                    print({a.fqn: a.value for a in actuals})
                    _fail_test("results differed -- see output table above")
        else:
            if isinstance(values, pl.DataFrame):
                expected_df = values
            else:
                expected_df = DataFrame(values).to_polars().collect()
            if resp_df is None:
                if not actual_errors:
                    _fail_test("there were no errors and no results")
            else:
                resp_df = resp_df.select(expected_df.columns)
                pl_test.assert_frame_equal(
                    resp_df,
                    expected_df,
                    check_column_order=False,
                    check_row_order=False,
                )
        return None

    def set_incremental_cursor(
        self,
        *,
        resolver: str | Resolver | None = None,
        scheduled_query: str | None = None,
        max_ingested_timestamp: datetime | None = None,
        last_execution_timestamp: datetime | None = None,
    ) -> None:
        if scheduled_query is None and resolver is None:
            raise ValueError("Either scheduled_query or resolver must be provided")
        if scheduled_query is not None and resolver is not None:
            raise ValueError("Exactly one of scheduled_query or resolver must be provided")

        if scheduled_query is not None:
            url = f"/v1/incremental_progress/named_query/{scheduled_query}"
        else:
            url = f"/v1/resolvers/{str(resolver)}/incremental_progress"

        result = self._request(
            method="POST",
            uri=url,
            data=SetIncrementalProgressRequest(
                max_ingested_timestamp=(
                    max_ingested_timestamp.astimezone(tz=timezone.utc) if max_ingested_timestamp else None
                ),
                last_execution_timestamp=(
                    last_execution_timestamp.astimezone(tz=timezone.utc) if last_execution_timestamp else None
                ),
            )
            .json()
            .encode("utf-8"),
            json=None,
            response=None,
            branch=None,
            preview_deployment_id=None,
            environment_override=None,
        )
        result.raise_for_status()

        return None

    def get_incremental_cursor(
        self, *, resolver: str | Resolver | None = None, scheduled_query: str | None = None
    ) -> GetIncrementalProgressResponse:
        if scheduled_query is None and resolver is None:
            raise ValueError("Either scheduled_query or resolver must be provided")
        if scheduled_query is not None and resolver is not None:
            raise ValueError("Exactly one of scheduled_query or resolver must be provided")

        if scheduled_query is not None:
            url = f"/v1/incremental_progress/named_query/{scheduled_query}"
        else:
            url = f"/v1/resolvers/{str(resolver)}/incremental_progress"

        return self._request(
            method="GET",
            uri=url,
            json=None,
            response=GetIncrementalProgressResponse,
            branch=None,
            preview_deployment_id=None,
            environment_override=None,
        )

    def ping_engine(self, num: Optional[int] = None) -> int:
        return self._request(
            method="POST",
            uri="/ping",
            json=PingRequest(num=num),
            response=PingResponse,
            branch=None,
            preview_deployment_id=None,
            environment_override=None,
            metadata_request=False,
            extra_headers={"x-chalk-server": "go-api"},
        ).num
