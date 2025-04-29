from __future__ import annotations

import asyncio
import base64
import io
import json
import os
import typing
import uuid
import warnings
import webbrowser
from collections import OrderedDict
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import IntEnum
from sys import stderr
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Mapping, Optional, Sequence, Union, cast, overload
from urllib.parse import urlparse

import pandas as pd
import requests as requests
from typing_extensions import assert_never

from chalk.client import ChalkBaseException, Dataset, DatasetRevision
from chalk.client.models import (
    ChalkError,
    ColumnMetadata,
    DatasetFilter,
    DatasetRecomputeResponse,
    DatasetResponse,
    DatasetRevisionPreviewResponse,
    DatasetRevisionResponse,
    DatasetRevisionSummaryResponse,
    IngestDatasetRequest,
    OfflineQueryContext,
    QueryStatus,
)
from chalk.client.response import DatasetPartition
from chalk.features import DataFrame, Feature, FeatureWrapper, ResolverProtocol, deserialize_dtype, ensure_feature
from chalk.features._encoding.pyarrow import pyarrow_to_polars
from chalk.features.feature_set import FeatureSetBase
from chalk.features.filter import freeze_time
from chalk.features.pseudofeatures import CHALK_TS_FEATURE, ID_FEATURE, OBSERVED_AT_FEATURE, PSEUDONAMESPACE
from chalk.features.resolver import Resolver
from chalk.features.tag import BranchId, EnvironmentId
from chalk.integrations.catalogs.base_catalog import BaseCatalog
from chalk.utils.df_utils import read_parquet
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.threading import DEFAULT_IO_EXECUTOR

if TYPE_CHECKING:
    import polars as pl
    import pyarrow as pa

    from chalk.client.client_impl import ChalkAPIClientImpl

_logger = get_logger(__name__)


class ColNameDecoder:
    def decode_col_name(self, col_name: str) -> str:
        if col_name.startswith("__") and col_name.endswith("__"):
            return col_name
        x_split = col_name.split("_")
        if x_split[0] == "ca":
            return "_".join(x_split[1:])
        elif x_split[0] == "cb":
            root_fqn_b32 = x_split[1]
            return base64.b32decode(root_fqn_b32.replace("0", "=").upper()).decode("utf8")
        elif x_split[0] == "cc":
            # Need to implement serialization / deserialization of the state dict
            raise NotImplementedError("Decoding stateful column names are not yet supported")
        else:
            raise ValueError(f"Unexpected identifier: {x_split[0]}")


class DatasetVersion(IntEnum):
    """Format of the parquet file. Used when loading a dataset so that we know what format it is in"""

    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES = 1
    """
    This is the format that bigquery dumps to when specifying an output bucket and output format
    as part of an (async) query job
    The output contains extra columns, and all column names are b32 encoded, because
    bigquery does not support '.' in column names.
    The client will have to decode column names before loading this data
    All data, except for feature times, are json encoded
    """

    DATASET_WRITER = 2
    """This is the format returned by the dataset writer in engine. Should always be used for inputs"""

    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2 = 3
    """
    This format uses separate columns for the observed at and timestamp columns
    The observed at column is the actual timestamp from when the observation was observed,
    whereas the timestamp column is the original timestamp that the user requested
    """

    COMPUTE_RESOLVER_OUTPUT_V1 = 4

    NATIVE_DTYPES = 5
    """This format has feature values decoded with their native data types.
    It does not require json decoding client-side"""

    NATIVE_COLUMN_NAMES = 6
    """This format does not encode column names"""


def _read_parquet_pyarrow(uri: str) -> pa.Table:
    try:
        import pyarrow.parquet as pq
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    if uri.startswith("file://"):
        # local files for testing
        uri = uri[len("file://") :]
        return pq.read_table(uri)
    response = requests.get(uri)
    response.raise_for_status()  # Raise an error if the request fails

    # Load the Parquet data from the response content
    return pq.read_table(io.BytesIO(response.content))


def _parallel_download_pyarrow(
    uris: List[str],
    executor: ThreadPoolExecutor,
) -> pa.Table:
    try:
        import pyarrow as pa
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    table_futures: list[Future[pa.Table]] = []
    for uri in uris:
        table_futures.append(executor.submit(_read_parquet_pyarrow, uri))
    tables = [table.result() for table in table_futures]
    tables = [table.select(sorted(table.column_names)) for table in tables]
    return pa.concat_tables(tables)


def _parallel_download_polars_lazy(
    uris: List[str],
    executor: ThreadPoolExecutor,
) -> pl.LazyFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    df_futures: list[Future[pl.DataFrame]] = []

    # Filesystem class registration is non-threadsafe, so let's fetch the supported filesystems here
    # to pre-emptively register them.
    if len(uris) > 0 and uris[0].startswith("gs"):
        # importing here because we shouldn't assume that this is present in all cases
        from fsspec import get_filesystem_class

        get_filesystem_class("gs")

    if len(uris) > 0 and uris[0].startswith("s3"):
        # importing here because we shouldn't assume that this is present in all cases
        from fsspec import get_filesystem_class

        get_filesystem_class("s3")

    for uri in uris:
        # New versions of polars.scan_parquet don't use fsspec, and we need to pass explicit storage options here.
        # However, read_parquet still uses fsspec. In any case, we still collect here, so it doesn't really matter.
        #   https://docs.rs/object_store/0.7.0/src/object_store/gcp/mod.rs.html#963-1083
        #   https://docs.rs/object_store/0.7.0/src/object_store/aws/mod.rs.html#963-1083
        df_futures.append(executor.submit(read_parquet, uri))

    dfs = [df.result() for df in df_futures]
    dfs = [_standardize_utc_timezone_format(x.select(sorted(x.columns))) for x in dfs]
    df = pl.concat(dfs)
    return df.lazy()


def _standardize_utc_timezone_format(df: pl.DataFrame) -> pl.DataFrame:
    """
    Polars has a bug where it sometimes converts +00:00 timezones to UTC, but sometimes not, depending
    on whether there are rows or not. This function standardizes all timezones to UTC recursively.
    """
    try:
        import polars as pl
        from polars.datatypes import DataType, Datetime, List, Struct
        from polars.expr import Expr
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    def process_type(col_expr: Expr, dtype: DataType) -> Expr:
        """
        Recursively process a column expression based on its data type,
        converting any datetime with +00:00 timezone to UTC.

        Args:
            col_expr: Polars column expression
            dtype: Data type of the column

        Returns:
            Processed column expression
        """
        # Base case: Datetime with +00:00 timezone
        if isinstance(dtype, Datetime) and getattr(dtype, "time_zone", None) == "+00:00":
            return col_expr.dt.convert_time_zone("UTC")

        # Recursive case 1: List type
        elif isinstance(dtype, List):
            inner_type = dtype.inner

            if isinstance(inner_type, Datetime) and getattr(inner_type, "time_zone", None) == "+00:00":
                return col_expr.list.eval(pl.element().dt.convert_time_zone("UTC"))
            elif isinstance(inner_type, Struct):
                field_exprs = []
                for field in inner_type.fields:
                    if isinstance(field.dtype, Datetime) and getattr(field.dtype, "time_zone", None) == "+00:00":
                        field_exprs.append(
                            pl.element().struct.field(field.name).dt.convert_time_zone("UTC").alias(field.name)
                        )
                    elif isinstance(field.dtype, List):
                        if (
                            isinstance(field.dtype.inner, Datetime)
                            and getattr(field.dtype.inner, "time_zone", None) == "+00:00"
                        ):
                            field_exprs.append(
                                pl.element()
                                .struct.field(field.name)
                                .list.eval(pl.element().dt.convert_time_zone("UTC"))
                                .alias(field.name)
                            )
                        else:
                            field_exprs.append(pl.element().struct.field(field.name).alias(field.name))
                    else:
                        field_exprs.append(pl.element().struct.field(field.name).alias(field.name))

                return col_expr.list.eval(pl.struct(field_exprs))
            else:
                # For other inner types, no conversion needed
                return col_expr

        # Recursive case 2: Struct type
        elif isinstance(dtype, Struct):
            field_exprs = []
            for field in dtype.fields:
                if isinstance(field.dtype, Datetime) and getattr(field.dtype, "time_zone", None) == "+00:00":
                    field_exprs.append(col_expr.struct.field(field.name).dt.convert_time_zone("UTC").alias(field.name))
                elif isinstance(field.dtype, List):
                    list_field_expr = process_type(col_expr.struct.field(field.name), field.dtype)
                    field_exprs.append(list_field_expr.alias(field.name))
                else:
                    field_exprs.append(col_expr.struct.field(field.name).alias(field.name))

            return pl.struct(field_exprs)

        # Default case: Return the column expression unchanged
        else:
            return col_expr

    exprs = []
    for col_name, column_dtype in df.schema.items():
        column_expr = pl.col(col_name)
        processed_expr = process_type(column_expr, column_dtype).alias(col_name)
        exprs.append(processed_expr)

    return df.select(exprs)


def _load_dataset_from_chalk_writer(uris: List[str], executor: Optional[ThreadPoolExecutor]) -> pl.LazyFrame:
    # This should be used for v1 datasets (deprecated) and givens
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if executor is None:
        executor = DEFAULT_IO_EXECUTOR
    df_futures: list[Future[pl.DataFrame]] = []
    for uri in uris:
        df_futures.append(executor.submit(read_parquet, uri))

    dfs = [df.result() for df in df_futures]
    dfs = [x.select(sorted(x.columns)) for x in dfs]
    df = pl.concat(dfs)
    return df.lazy()


def _decode_column_names(
    column_names: List[str],
    col_name_decoder: ColNameDecoder | None,
) -> Mapping[str, str]:
    ans: Dict[str, str] = {}
    for x in column_names:
        if x.startswith("__"):
            if x in ("__id__", ID_FEATURE.fqn):
                ans[x] = ID_FEATURE.fqn
            elif x in ("__ts__", CHALK_TS_FEATURE.fqn):
                # Preserve these columns as-is to help with loading the timestamp
                ans[x] = CHALK_TS_FEATURE.fqn
            elif x in ("__observed_at__", "__oat__", OBSERVED_AT_FEATURE.fqn):
                # Preserve these columns as-is to help with loading the timestamp
                ans[x] = OBSERVED_AT_FEATURE.fqn
            elif x.startswith("__chalk_prompt_"):
                # Presere these columns for prompt evaluations
                ans[x] = x
            # Drop all the other metadata columns
            continue
        if col_name_decoder is None:
            feature_name = x
        else:
            feature_name = col_name_decoder.decode_col_name(x)
        if any(feature_name.endswith(f".__{y}__") for y in ("oat", "rat", "observed_at", "replaced_observed_at")):
            # Drop the timestamp metadata from individual features
            continue
        ans[x] = feature_name
    return ans


def _json_decode(x: Optional[str]):
    if x is None:
        return None
    return json.loads(x)


def _load_dataset_inner(
    uris: List[str],
    executor: Optional[ThreadPoolExecutor],
    output_feature_fqns: Optional[Sequence[str]],
    output_ts: Union[bool, str],
    output_id: bool,
    output_oat: bool,
    version: DatasetVersion,
    columns: Optional[Sequence[ColumnMetadata]],
    return_type: Literal["polars_dataframe", "polars_lazyframe", "pandas", "pyarrow"],
) -> Union[pl.DataFrame, pl.LazyFrame, pd.DataFrame, pa.Table]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    del pl  # unused
    # V2 datasets are in multiple files, and have column names encoded
    # due to DB limitations (e.g. bigquery does not support '.' in column names)
    # In addition, the datasets may contain extra columns (e.g. replaced observed at)
    # All values are JSON encoded
    if executor is None:
        executor = DEFAULT_IO_EXECUTOR
    if return_type == "pyarrow":
        table = _parallel_download_pyarrow(uris, executor)
        if version != DatasetVersion.NATIVE_COLUMN_NAMES:
            raise ValueError(f"'to_arrow' not supported for version {version}")
        return _extract_table_columns(table, output_feature_fqns, output_ts, output_id, output_oat, columns)

    else:
        # use polars for everything else
        df = _parallel_download_polars_lazy(uris, executor)
        final_df = _extract_df_columns(df, output_feature_fqns, output_ts, output_id, output_oat, version, columns)
        if return_type == "polars_lazyframe":
            return final_df
        elif return_type == "polars_dataframe":
            return final_df.collect()
        elif return_type == "pandas":
            return final_df.collect().to_pandas()


def to_utc(df: pl.DataFrame | pl.LazyFrame, col: str, expr: pl.Expr):
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    if col not in df.schema:
        return expr

    dtype = df.schema[col]
    if isinstance(dtype, pl.Datetime):
        if dtype.time_zone is not None:
            return expr.dt.convert_time_zone("UTC")
        else:
            return expr.dt.replace_time_zone("UTC")
    else:
        return expr


def _extract_table_columns(
    table: pa.Table,
    output_feature_fqns: Optional[Sequence[str]],
    output_ts: Union[bool, str],
    output_id: bool,
    output_oat: bool,
    columns: Optional[Sequence[ColumnMetadata]] = None,
) -> pa.Table:
    """Possibly just return the table unaltered?"""
    # decoded_col_names = _decode_column_names(table.column_names, None)
    # table = table.select(list(decoded_col_names.keys()))  # Select columns based on the keys of the decoded_col_names
    # table = table.rename_columns([decoded_col_names[col] for col in table.column_names])
    return table


def _extract_df_columns(
    df: pl.LazyFrame,
    output_feature_fqns: Optional[Sequence[str]],
    output_ts: Union[bool, str],
    output_id: bool,
    output_oat: bool,
    version: DatasetVersion,
    column_metadata: Optional[Sequence[ColumnMetadata]] = None,
) -> pl.LazyFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if version in (
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        DatasetVersion.NATIVE_DTYPES,
        DatasetVersion.NATIVE_COLUMN_NAMES,
    ):
        if version == DatasetVersion.NATIVE_COLUMN_NAMES:
            col_name_decoder = None
        else:
            col_name_decoder = ColNameDecoder()
        decoded_col_names = _decode_column_names(df.columns, col_name_decoder)
        # Select only the columns in decoded_col_names
        df = df.select(list(decoded_col_names.keys()))
        df = df.rename(dict(decoded_col_names))
        if column_metadata is not None:
            col_name_set = {x.feature_fqn for x in column_metadata}
            ordered_cols: list[str] = []
            for c in df.columns:
                if c not in col_name_set:
                    ordered_cols.append(c)
            for x in column_metadata:
                if x.feature_fqn not in ordered_cols and x.feature_fqn in df.columns:
                    ordered_cols.append(x.feature_fqn)
            df = df.select(ordered_cols)
        elif version == DatasetVersion.NATIVE_COLUMN_NAMES:
            assert output_feature_fqns is not None, f"output_feature_fqns must be supplied with {version=}"
            ordered_cols: list[str] = []
            for c in df.columns:
                if c not in output_feature_fqns:
                    ordered_cols.append(c)
            for x in output_feature_fqns:
                if x not in ordered_cols and x in df.columns:
                    ordered_cols.append(x)
            df = df.select(ordered_cols)

        # Using an OrderedDict so the order will match the order the user set in the
        # output argument
        expected_cols: Dict[str, pl.Expr] = OrderedDict()
        id_col = pl.col(str(ID_FEATURE))
        if output_id:
            # All dataframes have an ID_FEATURE column if they don't have a pkey column
            if str(ID_FEATURE) in df.columns:
                expected_cols[str(ID_FEATURE)] = id_col.alias(str(ID_FEATURE))

        if output_ts:
            ts_col_name = str(CHALK_TS_FEATURE) if output_ts is True else output_ts
            input_ts_col = to_utc(df, str(CHALK_TS_FEATURE), pl.col(str(CHALK_TS_FEATURE)))
            expected_cols[ts_col_name] = input_ts_col.alias(ts_col_name)

        if output_feature_fqns is None:
            # If not provided, return all columns, except for the OBSERVED_AT_FEATURE
            # (the REPLACED_OBSERVED_AT was already dropped in _decode_col_names)
            for x in df.columns:
                if x not in expected_cols and not x.startswith(f"{PSEUDONAMESPACE}.") and "chalk_observed_at" not in x:
                    expected_cols[x] = pl.col(x)

        else:
            # Make a best-effort attempt to determine the pkey and ts column fqn from the root namespace
            # of the other features

            root_namespaces: "set[str]" = set()
            for x in df.columns:
                if not x.startswith(f"{PSEUDONAMESPACE}.") and "." in x:
                    root_namespaces.add(x.split(".")[0])

            if len(root_namespaces) == 1:
                # There is a unique root namespace.
                root_ns = root_namespaces.pop()
            else:
                # There are zero or multiple root namespaces, so none is best to choose.
                root_ns = None

            ts_feature = None
            pkey_feature = None
            features_cls = None
            if (
                root_ns is not None
                and root_ns in FeatureSetBase.registry
                and version != DatasetVersion.NATIVE_COLUMN_NAMES
            ):
                """For native column names, we don't need to decipher column names at all"""
                features_cls = FeatureSetBase.registry[root_ns]
                ts_feature = features_cls.__chalk_ts__
                pkey_feature = features_cls.__chalk_primary__
            ts_col = to_utc(
                df, str(OBSERVED_AT_FEATURE), pl.col(str(OBSERVED_AT_FEATURE)).fill_null(pl.col(str(CHALK_TS_FEATURE)))
            )
            if output_oat:
                expected_cols[str(OBSERVED_AT_FEATURE)] = ts_col.alias(str(OBSERVED_AT_FEATURE))
            for x in output_feature_fqns:
                if features_cls is not None and x in [f.fqn for f in features_cls.features if f.is_has_one]:
                    for col in df.columns:
                        if col.startswith(f"{x}.") and not col.startswith("__"):
                            expected_cols[col] = pl.col(col)
                    continue
                if x == root_ns:
                    for col in df.columns:
                        if root_ns is not None and col.startswith(root_ns) and not col.startswith("__"):
                            expected_cols[col] = pl.col(col)
                    continue
                if x in expected_cols:
                    continue
                if x in df.columns:
                    if x == str(CHALK_TS_FEATURE):
                        expected_cols[x] = ts_col.alias(x)
                    else:
                        expected_cols[x] = pl.col(x)
                    continue
                if x == str(CHALK_TS_FEATURE) or (ts_feature is not None and x == str(ts_feature)):
                    # The ts feature wasn't returned as the ts feature, but we are able to figure it out from the graph
                    # Alias the ts_col as the ts fqn (or CHALK_TS_FEATURE fqn if that's what was passed in)
                    expected_cols[x] = ts_col.alias(x)
                    continue
                if pkey_feature is not None and x == str(pkey_feature):
                    expected_cols[x] = id_col.alias(x)
                    continue
                else:
                    # We should _never_ hit this as the query should have failed before results are returned
                    # if an invalid feature was requested
                    raise ValueError(f"Feature '{x}' was not found in the results.")

        df = df.select(list(expected_cols.values()))

    elif version == DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1:
        unique_features = set(df.select(pl.col("feature_name").unique()).lazy().collect()["feature_name"].to_list())
        cols = [
            pl.col("value").filter(pl.col("feature_name").eq(fqn)).first().alias(cast(str, fqn))
            for fqn in unique_features
        ]

        df = df.groupby("pkey").agg(cols)
        decoded_stmts = []
        for col in df.columns:
            if col == "pkey":
                continue
            else:
                decoded_stmts.append(
                    pl.col(col).apply(_json_decode, return_dtype=Feature.from_root_fqn(col).converter.polars_dtype)
                )
        df = df.select(decoded_stmts)
        # it might be a good idea to remember that we used to rename this __id__ column to the primary key
        # We also need to remove columns like feature.__oat__ and feature.__rat__
        df = df.select([col for col in df.columns if not col.endswith("__")])
        return df.select(sorted(df.columns))
    elif version != DatasetVersion.DATASET_WRITER:
        raise ValueError(f"Unsupported version: {version}")

    decoded_stmts = []
    feature_name_to_metadata = None if column_metadata is None else {x.feature_fqn: x for x in column_metadata}
    for col, dtype in zip(df.columns, df.dtypes):
        if version in (
            DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
            DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        ):
            # The parquet file is all JSON-encoded except for the ts column. That is, the only datetime column is for the timestamp,
            # and all other columns are strings
            if isinstance(dtype, pl.Datetime):
                # Assuming that the only datetime column is for timestamps
                decoded_stmts.append(to_utc(df, col, pl.col(col)))
            else:
                decoded_stmts.append(pl.col(col).apply(_json_decode, return_dtype=dtype))
        elif version in (DatasetVersion.NATIVE_DTYPES, DatasetVersion.NATIVE_COLUMN_NAMES):
            # We already decoded the column names so matching against the fqn
            if col == CHALK_TS_FEATURE or col == OBSERVED_AT_FEATURE:
                decoded_stmts.append(to_utc(df, col, pl.col(col)))
            elif col == ID_FEATURE:
                # The pkey is already decoded properly -- it's always an int or str
                decoded_stmts.append(pl.col(col))
            else:
                if feature_name_to_metadata is None or col not in feature_name_to_metadata:
                    if isinstance(dtype, pl.Datetime):
                        decoded_stmts.append(to_utc(df, col, pl.col(col)))
                    else:
                        decoded_stmts.append(pl.col(col))
                else:
                    col_metadata = feature_name_to_metadata[col]
                    polars_dtype = pyarrow_to_polars(deserialize_dtype(col_metadata.dtype), col)
                    # Don't attempt to cast list and struct types -- it probably won't work
                    # Instead, we should load the dataset via pyarrow, rather than via polars
                    col_expr = pl.col(col)
                    if dtype != polars_dtype and not isinstance(polars_dtype, (pl.Struct, pl.List)):
                        col_expr = col_expr.cast(polars_dtype, strict=True)
                    decoded_stmts.append(col_expr)
        else:
            raise ValueError(f"Unsupported version: {version}")
    return df.select(decoded_stmts)


@overload
def load_dataset(
    uris: List[str],
    version: Union[int, "DatasetVersion"],
    return_type: Literal["polars_dataframe"],
    output_features: Optional[Sequence[Union[str, "Feature", "FeatureWrapper", Any]]] = None,
    output_id: bool = True,
    output_ts: Union[bool, str] = True,
    executor: Optional[ThreadPoolExecutor] = None,
    columns: Optional[Sequence["ColumnMetadata"]] = None,
    output_oat: bool = False,
) -> pl.DataFrame:
    ...


@overload
def load_dataset(
    uris: List[str],
    version: Union[int, "DatasetVersion"],
    return_type: Literal["polars_lazyframe"],
    output_features: Optional[Sequence[Union[str, "Feature", "FeatureWrapper", Any]]] = None,
    output_id: bool = True,
    output_ts: Union[bool, str] = True,
    executor: Optional[ThreadPoolExecutor] = None,
    columns: Optional[Sequence["ColumnMetadata"]] = None,
    output_oat: bool = False,
) -> pl.LazyFrame:
    ...


@overload
def load_dataset(
    uris: List[str],
    version: Union[int, "DatasetVersion"],
    return_type: Literal["pandas"],
    output_features: Optional[Sequence[Union[str, "Feature", "FeatureWrapper", Any]]] = None,
    output_id: bool = True,
    output_ts: Union[bool, str] = True,
    executor: Optional[ThreadPoolExecutor] = None,
    columns: Optional[Sequence["ColumnMetadata"]] = None,
    output_oat: bool = False,
) -> pd.DataFrame:
    ...


@overload
def load_dataset(
    uris: List[str],
    version: Union[int, "DatasetVersion"],
    return_type: Literal["pyarrow"],
    output_features: Optional[Sequence[Union[str, "Feature", "FeatureWrapper", Any]]] = None,
    output_id: bool = True,
    output_ts: Union[bool, str] = True,
    executor: Optional[ThreadPoolExecutor] = None,
    columns: Optional[Sequence["ColumnMetadata"]] = None,
    output_oat: bool = False,
) -> pa.Table:
    ...


def load_dataset(
    uris: List[str],
    version: Union[DatasetVersion, int],
    return_type: Literal["polars_dataframe", "polars_lazyframe", "pandas", "pyarrow"],
    output_features: Optional[Sequence[Union[str, Feature, FeatureWrapper, Any]]] = None,
    output_id: bool = True,
    output_ts: Union[bool, str] = True,
    executor: Optional[ThreadPoolExecutor] = None,
    columns: Optional[Sequence[ColumnMetadata]] = None,
    output_oat: bool = False,
) -> pl.DataFrame | pl.LazyFrame | pd.DataFrame | pa.Table:
    if len(uris) == 0:
        raise ValueError(
            "No outputs found. Check `dataset.status` to see if query is still running, and "
            + "'dataset.errors' for any query errors that may have occurred."
        )
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    del pl  # Unused
    if not isinstance(version, DatasetVersion):
        try:
            version = DatasetVersion(version)
        except ValueError:
            raise ValueError(
                (
                    f"The dataset version ({version}) is not supported by this installed version of the Chalk client. "
                    "Please upgrade your chalk client and try again."
                )
            )
    if version == DatasetVersion.DATASET_WRITER:
        assert return_type == "polars_lazyframe", "givens table only fetchable as lazyframe "
        return _load_dataset_from_chalk_writer(uris, executor)
    output_feature_fqns = (
        None
        if output_features is None
        else [x if isinstance(x, str) else ensure_feature(x).root_fqn for x in output_features]
    )
    if version in (
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1,
        DatasetVersion.NATIVE_DTYPES,
        DatasetVersion.NATIVE_COLUMN_NAMES,
    ):
        return _load_dataset_inner(
            uris,
            executor,
            version=version,
            output_feature_fqns=output_feature_fqns,
            output_id=output_id,
            output_ts=output_ts,
            output_oat=output_oat,
            columns=columns,
            return_type=return_type,
        )
    assert_never(version)


def load_schema(uris: List[str]) -> pa.Schema:
    if len(uris) == 0:
        raise ValueError(
            "No outputs found. Check `dataset.status` to see if query is still running, and "
            + "'dataset.errors' for any query errors that may have occurred."
        )
    uri = uris[0]  # schema should be the same for all uris

    try:
        import pyarrow.parquet as pq
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    if uri.startswith("file://"):
        # local files for testing
        uri = uri[len("file://") :]
        return pq.read_table(uri).schema

    try:
        return _try_reading_metadata_from_parquet_uri(uri)
    except Exception as e:
        # If we can't read the metadata, try to read the file as a whole
        _logger.warning(
            f"Failed to read metadata from parquet file {uri}. Trying to read the file as a whole", exc_info=e
        )
        response = requests.get(uri)
        response.raise_for_status()
        parquet_file = pq.ParquetFile(io.BytesIO(response.content))
        return parquet_file.schema.to_arrow_schema()


class _MaybeIntDFColumn:
    column: int | str

    def __init__(self, x: str):
        super().__init__()
        self.column = int(x) if x.isnumeric() else x

    def __lt__(self, other: _MaybeIntDFColumn):
        if isinstance(self.column, int) and isinstance(other.column, int):
            return self.column < other.column
        return str(self.column) < str(other.column)


@dataclass(frozen=True)
class DatasetPartitionImpl(DatasetPartition):
    performance_summary: str | None


class DatasetRevisionImpl(DatasetRevision):
    _hydrated: bool

    def __init__(
        self,
        revision_id: uuid.UUID,
        environment: EnvironmentId,
        creator_id: str,
        outputs: List[str],
        givens_uri: Optional[str],
        status: QueryStatus,
        filters: DatasetFilter,
        partitions: Sequence[DatasetPartitionImpl],
        output_uris: str,
        output_version: int,
        client: ChalkAPIClientImpl,
        num_bytes: Optional[int] = None,
        created_at: Optional[datetime] = None,
        started_at: Optional[datetime] = None,
        terminated_at: Optional[datetime] = None,
        dataset_name: Optional[str] = None,
        dataset_id: Optional[uuid.UUID] = None,
        branch: Optional[BranchId] = None,
        dashboard_url: str | None = None,
        num_computers: int = 1,
        errors: list[ChalkError] | None = None,
        timeout: float | timedelta | ellipsis | None = ...,
        metadata: Mapping[str, Any] | None = None,
    ):
        super().__init__()
        self.revision_id = revision_id
        self.environment = environment
        self.creator_id = creator_id
        self.outputs = outputs
        self.givens_uri = givens_uri
        self.status = status
        self.filters = filters
        self.num_partitions = len(partitions)
        self.partitions = list(partitions)
        self.output_uris = output_uris
        self.output_version = output_version
        self.num_bytes = num_bytes
        self.created_at = created_at
        self.started_at = started_at
        self.terminated_at = terminated_at
        self.dataset_name = dataset_name
        self.dataset_id = dataset_id
        self.dashboard_url = dashboard_url
        self._client = client
        self.branch = BranchId(branch) if branch is not None else None
        self._hydrated = self.status == QueryStatus.SUCCESSFUL
        self.num_computers = num_computers
        self.errors = errors
        # Threading `timeout` through because sometimes we don't await
        # the dataset at the initial `offline_query` call, but await
        # it when calling methods on the dataset like `to_polars()`.
        self.timeout = timeout
        self.metadata = metadata

    def __getattr__(self, name: str):
        # Using `_getattr__` instead of @property b/c VSCode eagerly loads @property, which crashes the debugger with a large dataset download
        if name == "data_as_polars":
            warnings.warn(
                DeprecationWarning(
                    "The property `DatasetRevision.data_as_polars` is deprecated. Please use the method `DatasetRevision.get_data_as_polars()` instead."
                )
            )
            return self.get_data_as_polars()
        if name == "data_as_pandas":
            warnings.warn(
                DeprecationWarning(
                    "The property `DatasetRevision.data_as_pandas` is deprecated. Please use the method `DatasetRevision.get_data_as_pandas()` instead."
                )
            )
            return self.get_data_as_pandas()

        if name == "data_as_dataframe":
            warnings.warn(
                DeprecationWarning(
                    "The property `DatasetRevision.data_as_dataframe` is deprecated. Please use the method `DatasetRevision.get_data_as_dataframe()` instead."
                )
            )
            return self.get_data_as_dataframe()
        return super().__getattribute__(name)

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_data_as_polars",
    ) -> pl.LazyFrame:
        context = OfflineQueryContext(environment=self.environment)
        if not ignore_errors:
            self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        return self._client.load_dataset(
            job_id=self.revision_id,
            context=context,
            output_id=output_id,
            outputs=self.outputs,
            output_ts=output_ts,
            branch=self.branch,
            ignore_errors=ignore_errors,
            query_inputs=False,
            return_type="polars_lazyframe",
        )

    def arrow_schema(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "arrow_schema",
    ) -> pa.Schema:
        context = OfflineQueryContext(environment=self.environment)
        if not ignore_errors:
            self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        return self._client.load_schema(
            job_id=self.revision_id,
            context=context,
            branch=self.branch,
            ignore_errors=ignore_errors,
        )

    def to_arrow(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_arrow",
    ) -> pa.Table:
        context = OfflineQueryContext(environment=self.environment)
        if not ignore_errors:
            self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        return self._client.load_dataset(
            job_id=self.revision_id,
            context=context,
            output_id=False,  # unused
            outputs=self.outputs,
            output_ts=False,  # unused
            branch=self.branch,
            ignore_errors=ignore_errors,
            query_inputs=False,
            return_type="pyarrow",
        )

    def to_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_polars",
    ) -> pl.DataFrame:
        return self.get_data_as_polars(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            timeout=timeout,
            show_progress=show_progress,
            caller_name=caller_name,
        ).collect()

    async def to_polars_async(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_polars_async",
    ) -> pl.DataFrame:
        ret = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: self.to_polars(
                output_id=output_id,
                output_ts=output_ts,
                ignore_errors=ignore_errors,
                show_progress=show_progress,
                timeout=timeout,
                caller_name=caller_name,
            ),
        )
        return ret

    def to_polars_lazyframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_polars_lazyframe",
    ) -> pl.LazyFrame:
        return self.get_data_as_polars(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_data_as_pandas",
    ) -> pd.DataFrame:
        context = OfflineQueryContext(environment=self.environment)
        _logger.info(f"loading pandas DataFrame for DatasetRevision {self.revision_id}")
        if not ignore_errors:
            self._hydrate(caller_method=caller_name, show_progress=show_progress, timeout=timeout)
        return self._client.load_dataset(
            output_id=output_id,
            output_ts=output_ts,
            job_id=self.revision_id,
            outputs=self.outputs,
            context=context,
            branch=self.branch,
            ignore_errors=ignore_errors,
            query_inputs=False,
            return_type="pandas",
        )

    def to_pandas(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        timeout: float | timedelta | ellipsis | None = ...,
        show_progress: bool = True,
        caller_name: str = "to_pandas",
    ) -> pd.DataFrame:
        return self.get_data_as_pandas(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            timeout=timeout,
            show_progress=show_progress,
            caller_name=caller_name,
        )

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_data_as_dataframe",
    ) -> DataFrame:
        context = OfflineQueryContext(environment=self.environment)
        _logger.info(f"loading Chalk DataFrame for DatasetRevision {self.revision_id}")
        if not ignore_errors:
            self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        return DataFrame(
            data=self._client.load_dataset(
                job_id=self.revision_id,
                output_id=output_id,
                output_ts=output_ts,
                outputs=self.outputs,
                context=context,
                branch=self.branch,
                ignore_errors=ignore_errors,
                query_inputs=False,
                return_type="polars_dataframe",
            )
        )

    def download_uris(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "download_uris",
    ) -> list[str]:
        from chalk.client.client_impl import DatasetJobStatusRequest

        if not ignore_errors:
            self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        status = self._client.get_job_status_v4(
            request=DatasetJobStatusRequest(
                job_id=str(self.revision_id),
                ignore_errors=ignore_errors,
                query_inputs=False,
            ),
            environment=self.environment,
            branch=self.branch,
        )
        return status.urls

    def summary(self) -> DatasetRevisionSummaryResponse:
        self.wait_for_completion(caller_method="summary")
        return self._client.get_revision_summary(
            str(self.revision_id),
            environment=self.environment,
        )

    def preview(self) -> DatasetRevisionPreviewResponse:
        self.wait_for_completion(caller_method="preview")
        return self._client.get_revision_preview(
            str(self.revision_id),
            environment=self.environment,
        )

    def wait(
        self,
        timeout: float | timedelta | ellipsis | None = ...,
        show_progress: bool = True,
        caller_name: str = "wait",
    ) -> None:
        from chalk.client.client_impl import DatasetJobStatusRequest

        self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        status = self._client.get_job_status_v4(
            request=DatasetJobStatusRequest(
                job_id=str(self.revision_id),
                query_inputs=False,
            ),
            environment=self.environment,
            branch=self.branch,
        )
        if status.errors is not None and len(status.errors) > 0:
            raise ChalkBaseException(errors=status.errors)

    def download_data(
        self,
        path: str,
        output_id: bool = False,
        output_ts: Union[bool, str] = False,
        ignore_errors: bool = False,
        executor: ThreadPoolExecutor | None = None,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "download_data",
    ) -> None:
        self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        urls = self.download_uris(
            output_id=output_id,
            output_ts=output_ts,
            timeout=timeout,
            show_progress=show_progress,
            ignore_errors=ignore_errors,
            caller_name=caller_name,
        )

        def _download_data(url: str, directory_path: str):
            r = requests.get(url)
            parse = urlparse(url)
            destination_filepath = "/".join(parse.path.split("/")[4:])
            destination_directory = os.path.join(directory_path, os.path.dirname(destination_filepath))
            os.makedirs(destination_directory, exist_ok=True)
            with open(f"{directory_path}/{destination_filepath}", "wb") as f:
                f.write(r.content)

        futures = ((executor or DEFAULT_IO_EXECUTOR).submit(_download_data, url, path) for url in urls)
        for f in futures:
            f.result()

    def get_input_dataframe(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_input_dataframe",
    ) -> pl.LazyFrame:
        if not ignore_errors:
            self._hydrate(caller_method=caller_name, timeout=timeout, show_progress=show_progress)
        context = OfflineQueryContext(environment=self.environment)
        _logger.info(f"loading input DataFrame for DatasetRevision {self.revision_id}")
        return self._client.load_dataset(
            job_id=self.revision_id,
            context=context,
            output_id=False,
            outputs=None,
            output_ts=False,
            branch=self.branch,
            query_inputs=True,
            ignore_errors=ignore_errors,
            return_type="polars_lazyframe",
        )

    def open_in_browser(self, return_url_only: bool = False) -> str:
        url = self.dashboard_url
        if url is None:
            raise ValueError(f"No url for offline query {self.revision_id} found.")
        if not return_url_only:
            webbrowser.open_new_tab(url)
        return url

    def ingest(
        self,
        store_online: bool = False,
        store_offline: bool = True,
        planner_options: Optional[Mapping[str, Any]] = None,
        online_timestamping_mode: typing.Literal["feature_time", "start_of_ingestion_job"] = "feature_time",
    ) -> DatasetImpl:
        if not self._hydrated:
            print("Waiting for dataset to complete before ingesting...")
            self.wait(show_progress=False, caller_name="ingest")
        context = OfflineQueryContext(environment=self.environment)
        wire_online_timestamping_mode = (
            "START_OF_INGESTION_JOB" if online_timestamping_mode == "start_of_ingestion_job" else "FEATURE_TIME"
        )
        request = IngestDatasetRequest(
            revision_id=str(self.revision_id),
            branch=self.branch,
            outputs=self.outputs,
            store_online=store_online,
            store_offline=store_offline,
            planner_options=planner_options,
            online_timestamping_mode=wire_online_timestamping_mode,
        )
        return self._client.ingest_dataset(request, context)

    def resolver_replay(
        self,
        resolver: ResolverProtocol,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_method: str = "resolver_replay",
    ) -> Union[pl.DataFrame, pl.LazyFrame, Mapping[str, pl.DataFrame], Mapping[str, pl.LazyFrame]]:
        revision_id = self.revision_id
        if isinstance(resolver, Resolver):
            resolver_fqn = resolver.fqn
        else:
            raise TypeError(f"resolver_replay expected a Resolver type, got {type(resolver)}")

        # Await dataset job completion
        _logger.info(f"loading Chalk DataFrame for DatasetRevision {self.revision_id}")

        if not self._hydrated:
            # If the initial `offline_query` call has a timeout set, use that.
            timeout = timeout if timeout is not ... else self.timeout
            self._client.await_operation_completion(
                operation_id=self.revision_id,
                show_progress=show_progress,
                caller_method=caller_method,
                environment_id=self.environment,
                num_computers=self.num_computers,
                timeout=timeout,
                raise_on_dataset_failure=False,
            )

        response = self._client.get_resolver_replay(
            environment_id=self.environment,
            revision_id=revision_id,
            resolver_fqn=resolver_fqn,
            branch=self.branch,
            timeout=timeout,
        )

        if response.error:
            raise IndexError(response.error)

        assert response.urls is not None
        assert len(response.urls) > 0

        # In the future, we may want a means to filter if we know there will be multiple instances of the resolver
        filtered_urls = response.urls

        if len(filtered_urls) == 1:
            no_input_df = _parallel_download_polars_lazy(filtered_urls, DEFAULT_IO_EXECUTOR).collect()
            df = self._resolver_replay(
                resolver,
                no_input_df.select(
                    [str(df_column.column) for df_column in sorted([_MaybeIntDFColumn(c) for c in no_input_df.columns])]
                ),
            )
            return df

        # We want to display dataframes separately!!

        dfs: dict[str, pl.DataFrame] = {}
        for url in filtered_urls:
            operator_id = None
            for part in url.split("/"):
                if part.startswith("operator_"):
                    operator_id = "_".join(part.split("_")[1:])
                    break

            if operator_id is not None:
                no_input_df = _parallel_download_polars_lazy([url], DEFAULT_IO_EXECUTOR).collect()
                no_input_df = no_input_df.select(
                    [str(df_column.column) for df_column in sorted([_MaybeIntDFColumn(c) for c in no_input_df.columns])]
                )
                df = self._resolver_replay(resolver, no_input_df)
                dfs[operator_id] = df
            else:
                warnings.warn(
                    f"Could not find operator id for url {url} when attempting to replay resolver {resolver_fqn}."
                )
        return dfs

    def write_to(self, destination: str, catalog: BaseCatalog | None) -> None:
        if catalog is None:
            raise ValueError("A catalog must be provided to write a dataset revision to a destination.")

        return catalog.write_to_catalog(revision=self, destination=destination)

    def set_metadata(
        self,
        metadata: Mapping[str, Any],
    ):
        self._client.set_dataset_revision_metadata(
            metadata=metadata,
            revision_id=str(self.revision_id),
            environment=self.environment,
        )

    def _resolver_replay(self, resolver: Resolver, raw_input_df: pl.DataFrame):
        def truncate_output(output: str, prefix: int = 50, suffix: int = 10) -> str:
            if len(output) <= prefix + suffix:
                return output
            return output[:prefix] + "....." + output[-suffix:]

        import polars as pl

        from chalk.features.feature_wrapper import unwrap_feature

        # We choose to run the resolver fn on the rows one at a time here for devx purposes: Running a df.with_column
        # would reduce visibility on any bad rows in the dataframe, making it harder to debug (which is the whole point
        # of resolver replay)

        output_col = []
        __ts_series = raw_input_df["__ts__"]
        no_ts_input_df = raw_input_df.drop(["__ts__"])
        for (row_i, args), __ts in zip(enumerate(no_ts_input_df.rows()), __ts_series):
            print(
                f"resolver_replay: Running resolver {resolver.fqn} on args {truncate_output(str(args))} at time {str(__ts)}"
            )
            actual_args = []
            for i, input in enumerate(resolver.inputs):
                contains_packed_df_name = f"{i}_packed_df" in no_ts_input_df.columns
                if unwrap_feature(input).is_has_many or contains_packed_df_name:
                    # bogus indexing scheme
                    col_name = (
                        f"{i}_packed_df" if contains_packed_df_name else f"{i}"
                    )  # maintain compat with older resolver replay format
                    has_many_input_df = raw_input_df[row_i].select(pl.col(col_name))
                    if len(has_many_input_df[col_name][0]) == 0:
                        # Explode's default behavior empty lists is to return NaN
                        # Explode on {'a': [[]]} becomes {'a': [NaN]}
                        # Explode on {'a': []} becomes {'a': []}
                        actual_args.append(
                            DataFrame(
                                pl.DataFrame([pl.Series(col_name, [], dtype=raw_input_df.schema[col_name])])
                                .explode(pl.all())
                                .unnest(col_name)
                            )
                        )
                    else:
                        actual_args.append(DataFrame(has_many_input_df.explode(pl.all()).unnest(col_name)))
                else:
                    value = args[i]
                    if isinstance(input, Feature):
                        value = input.converter.from_primitive_to_rich(value)
                    actual_args.append(value)
            with freeze_time(__ts.replace(tzinfo=timezone.utc)):
                try:
                    output = resolver.fn(*actual_args)
                except Exception as e:
                    print(
                        f"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Resolver {resolver.fqn} raised an uncaught exception.
Args: {truncate_output(str(args))}
This occurred during the actual execution of resolver {resolver.fqn}.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!""",
                        file=stderr,
                    )
                    raise e
            print(f"resolver_replay: {resolver.fqn} returned {output}")
            output_col.append(output)
        return raw_input_df.with_columns(pl.Series(name="__resolver_replay_output__", values=output_col))

    def __repr__(self) -> str:
        if self.dataset_name:
            return f"DatasetRevision(dataset_name='{self.dataset_name}', revision_id='{self.revision_id}', status='{self.status.value}')"
        return f"DatasetRevision(revision_id='{self.revision_id}')"

    def wait_for_completion(
        self,
        show_progress: bool = False,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_method: str | None = None,
    ) -> None:
        self._hydrate(show_progress=show_progress, timeout=timeout, caller_method=caller_method)

    def _hydrate(
        self, show_progress: bool, caller_method: Optional[str], timeout: float | timedelta | ellipsis | None
    ) -> None:
        """
        :param show_progress: Pass `True` to show a progress bar while waiting for the operation to complete.
        :param caller_method: Caller method name. This will be used to display a user-facing message explaining
        the implicit showing of computation progress.
        """
        if self._hydrated:
            return

        # If the initial `offline_query` call has a timeout set, use that.
        timeout = timeout if timeout is not ... else self.timeout
        self._client.await_operation_completion(
            operation_id=self.revision_id,
            show_progress=show_progress,
            caller_method=caller_method,
            environment_id=self.environment,
            num_computers=self.num_computers,
            timeout=timeout,
            raise_on_dataset_failure=True,
        )
        dataset = self._client.get_anonymous_dataset(
            revision_id=str(self.revision_id),
            environment=self.environment,
            branch=self.branch,
        )
        completed_revision = dataset.revisions[-1]
        assert isinstance(completed_revision, DatasetRevisionImpl)

        self.outputs = completed_revision.outputs
        self.environment = completed_revision.environment
        self.revision_id = completed_revision.revision_id
        self.branch = completed_revision.branch
        self.terminated_at = completed_revision.terminated_at
        self.started_at = completed_revision.started_at
        self.created_at = completed_revision.created_at
        self.num_bytes = completed_revision.num_bytes
        self.output_version = completed_revision.output_version
        self.output_uris = completed_revision.output_uris
        self.num_partitions = completed_revision.num_partitions
        self.filters = completed_revision.filters
        self.status = completed_revision.status
        self.givens_uri = completed_revision.givens_uri

        self._hydrated = True


class DatasetImpl(Dataset):
    revisions: list[DatasetRevisionImpl]

    def __init__(
        self,
        is_finished: bool,
        version: int,
        revisions: Sequence[DatasetRevisionImpl],
        client: ChalkAPIClientImpl,
        environment: EnvironmentId,
        dataset_id: Optional[uuid.UUID] = None,
        dataset_name: Optional[str] = None,
        errors: Optional[List[ChalkError]] = None,
    ):
        super().__init__()
        self.is_finished = is_finished
        self.version = version
        self.revisions = list(revisions)  # pyright: ignore[reportIncompatibleVariableOverride]
        self.environment = environment
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.errors = errors
        self._client = client

    def __getattr__(self, name: str):
        # Using `_getattr__` instead of @property b/c VSCode eagerly loads @property, which crashes the debugger with a large dataset download
        if name == "data_as_polars":
            warnings.warn(
                DeprecationWarning(
                    "The property `Dataset.data_as_polars` is deprecated. Please use the method `Dataset.get_data_as_polars()` instead."
                )
            )
            return self.get_data_as_polars()
        if name == "data_as_pandas":
            warnings.warn(
                DeprecationWarning(
                    "The property `Dataset.data_as_pandas` is deprecated. Please use the method `Dataset.get_data_as_pandas()` instead."
                )
            )
            return self.get_data_as_pandas()

        if name == "data_as_dataframe":
            warnings.warn(
                DeprecationWarning(
                    "The property `Dataset.data_as_dataframe` is deprecated. Please use the method `Dataset.get_data_as_dataframe()` instead."
                )
            )
            return self.get_data_as_dataframe()
        return super().__getattribute__(name)

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_data_as_polars",
    ) -> pl.LazyFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_data_as_polars(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def to_polars(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_polars",
    ) -> pl.DataFrame:
        return self.get_data_as_polars(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            timeout=timeout,
            show_progress=show_progress,
            caller_name=caller_name,
        ).collect()

    async def to_polars_async(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_polars_async",
    ) -> pl.DataFrame:
        ret = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: self.to_polars(
                output_id=output_id,
                output_ts=output_ts,
                ignore_errors=ignore_errors,
                show_progress=show_progress,
                timeout=timeout,
                caller_name=caller_name,
            ),
        )
        return ret

    def to_polars_lazyframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_polars_lazyframe",
    ) -> pl.LazyFrame:
        return self.get_data_as_polars(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def to_arrow(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_arrow",
    ) -> pa.Table:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].to_arrow(
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def arrow_schema(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "arrow_schema",
    ) -> pa.Schema:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].arrow_schema(
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_data_as_pandas",
    ) -> pd.DataFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_data_as_pandas(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            timeout=timeout,
            show_progress=show_progress,
            caller_name=caller_name,
        )

    def to_pandas(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "to_pandas",
    ) -> pd.DataFrame:
        return self.get_data_as_pandas(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            timeout=timeout,
            show_progress=show_progress,
            caller_name=caller_name,
        )

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_data_as_dataframe",
    ) -> DataFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_data_as_dataframe(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def download_uris(
        self,
        output_id: bool = False,
        output_ts: bool | str = False,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "download_uris",
    ) -> list[str]:
        return self.revisions[-1].download_uris(
            output_id=output_id,
            output_ts=output_ts,
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def wait(
        self,
        timeout: float | timedelta | ellipsis | None = ...,
        show_progress: bool = True,
        caller_name: str = "wait",
    ) -> DatasetImpl:
        self.revisions[-1].wait(timeout=timeout, show_progress=show_progress, caller_name=caller_name)
        return self

    def download_data(
        self,
        path: str,
        executor: ThreadPoolExecutor | None = None,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "download_data",
    ) -> None:
        return self.revisions[-1].download_data(
            path=path,
            ignore_errors=ignore_errors,
            executor=executor,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def summary(self) -> DatasetRevisionSummaryResponse:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].summary()

    def preview(self) -> DatasetRevisionPreviewResponse:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].preview()

    def get_input_dataframe(
        self,
        ignore_errors: bool = False,
        show_progress: bool = True,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_name: str = "get_input_dataframe",
    ) -> pl.LazyFrame:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].get_input_dataframe(
            ignore_errors=ignore_errors,
            show_progress=show_progress,
            timeout=timeout,
            caller_name=caller_name,
        )

    def open_in_browser(self, return_url_only: bool = False) -> str:
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].open_in_browser(return_url_only=return_url_only)

    def recompute(
        self,
        features: Optional[List[Union[Feature, Any]]] = None,
        branch: Optional[str] = None,
        wait: bool = False,
        show_progress: bool = False,
        store_plan_stages: bool = False,
        correlation_id: str | None = None,
        explain: bool = False,
        tags: Optional[List[str]] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        run_asynchronously: bool = False,
        timeout: float | timedelta | ellipsis | None = ...,
        use_multiple_computers: bool = False,
    ) -> Dataset:
        run_asynchronously = run_asynchronously or use_multiple_computers
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        revision = self.revisions[-1]
        branch = branch or self._client.get_branch() or revision.branch
        revision.wait_for_completion(show_progress=show_progress, timeout=timeout, caller_method="recompute")

        recompute_response = self._client.recompute_dataset(
            dataset_name=self.dataset_name,
            revision_id=revision.revision_id,
            features=features,
            branch=branch,
            environment=self.environment,
            wait=wait,
            show_progress=show_progress,
            correlation_id=correlation_id,
            store_plan_stages=store_plan_stages,
            explain=explain,
            tags=tags,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            run_asynchronously=run_asynchronously,
            num_shards=revision.num_partitions,
        )
        self.revisions.append(recompute_response.revisions[-1])
        return self

    def write_to(self, destination: str, catalog: BaseCatalog | None = None) -> None:
        return self.revisions[-1].write_to(catalog=catalog, destination=destination)

    def set_metadata(self, metadata: Mapping[str, Any]):
        return self.revisions[-1].set_metadata(metadata)

    def ingest(
        self,
        store_online: bool = False,
        store_offline: bool = True,
        planner_options: Optional[Mapping[str, Any]] = None,
        online_timestamping_mode: typing.Literal["feature_time", "start_of_ingestion_job"] = "feature_time",
    ) -> DatasetImpl:
        return self.revisions[-1].ingest(
            store_online=store_online,
            store_offline=store_offline,
            planner_options=planner_options,
            online_timestamping_mode=online_timestamping_mode,
        )

    def resolver_replay(
        self,
        resolver: ResolverProtocol,
        show_progress: bool = False,
        timeout: float | timedelta | ellipsis | None = ...,
        caller_method: str = "resolver_replay",
    ):
        if len(self.revisions) == 0:
            raise IndexError("No revisions exist for dataset")
        return self.revisions[-1].resolver_replay(
            resolver=resolver,
            show_progress=show_progress,
            timeout=timeout,
            caller_method=caller_method,
        )

    def __repr__(self) -> str:
        if self.errors and self.dataset_name:
            return f"Dataset(name='{self.dataset_name}', version='{self.version}', errors='{self.errors}')"
        if self.dataset_name:
            return f"Dataset(name='{self.dataset_name}', version='{self.version}')"
        return "Dataset(name=<unnamed>)"

    @property
    def url(self) -> str | None:
        return self.revisions[-1].dashboard_url

    @property
    def dashboard_url(self) -> str | None:
        return self.revisions[-1].dashboard_url


def dataset_revision_from_response(
    revision: Union[DatasetRevisionResponse, DatasetRecomputeResponse], client: ChalkAPIClientImpl
) -> DatasetRevisionImpl:
    assert revision.revision_id is not None
    if revision.partitions is not None:
        partitions = [DatasetPartitionImpl(x.performance_summary) for x in revision.partitions]
    elif revision.num_partitions is not None:
        partitions = [DatasetPartitionImpl(performance_summary=None) for _ in range(revision.num_partitions)]
    else:
        raise ValueError("Either the `partitions` or `num_partitions` must be provided by the server")

    return DatasetRevisionImpl(
        revision_id=revision.revision_id,
        environment=revision.environment_id,
        creator_id=revision.creator_id,
        outputs=revision.outputs,
        givens_uri=revision.givens_uri,
        status=revision.status,
        filters=revision.filters,
        partitions=partitions,
        output_uris=revision.output_uris,
        output_version=revision.output_version,
        num_bytes=revision.num_bytes,
        client=client,
        created_at=revision.created_at,
        started_at=revision.started_at,
        terminated_at=revision.terminated_at,
        dataset_name=revision.dataset_name,
        dataset_id=revision.dataset_id,
        branch=revision.branch,
        dashboard_url=revision.dashboard_url,
        num_computers=revision.num_computers,
        errors=revision.errors,
        metadata=revision.metadata,
    )


def dataset_from_response(response: DatasetResponse, client: ChalkAPIClientImpl) -> DatasetImpl:
    revisions = [dataset_revision_from_response(revision, client) for revision in response.revisions]
    return DatasetImpl(
        is_finished=response.is_finished,
        version=response.version,
        revisions=revisions,
        environment=response.environment_id,
        client=client,
        dataset_id=response.dataset_id,
        dataset_name=response.dataset_name,
        errors=response.errors,
    )


def _try_reading_metadata_from_parquet_uri(uri: str) -> pa.Schema:
    try:
        import pyarrow.parquet as pq
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    import struct

    # First, make a HEAD request to get the file size
    head_response = requests.head(uri)
    file_size = int(head_response.headers.get("Content-Length", 0))

    # Parquet files store the metadata size in the last 4 bytes
    # and have an 8-byte magic number at the end
    # So first get the last 8 bytes to read the metadata size
    footer_range = f"bytes={file_size - 8}-{file_size - 1}"
    footer_response = requests.get(uri, headers={"Range": footer_range})

    if not 200 <= footer_response.status_code < 300:  # 206 Partial Content
        raise ValueError(f"Range request failed with status {footer_response.status_code}")

    # The last 4 bytes contain the metadata size
    metadata_size = struct.unpack("<I", footer_response.content[:4])[0]

    # Now get just the metadata section plus the footer
    metadata_start = file_size - 8 - metadata_size
    metadata_range = f"bytes={metadata_start}-{file_size - 1}"
    metadata_response = requests.get(uri, headers={"Range": metadata_range})

    if not 200 <= metadata_response.status_code < 300:
        raise ValueError(f"Metadata range request failed with status {metadata_response.status_code}")

    # Create a BytesIO object with the metadata
    metadata_io = io.BytesIO(metadata_response.content)

    # PyArrow can parse this to get the schema
    try:
        # This is a bit of a hack - we're creating a fake Parquet file with just the metadata
        parquet_file = pq.ParquetFile(metadata_io)
        return parquet_file.schema.to_arrow_schema()
    except Exception as e:
        raise ValueError(f"Failed to parse Parquet metadata: {e}")
