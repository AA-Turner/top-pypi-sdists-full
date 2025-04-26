from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from chalk.utils.environment_parsing import env_var_bool


@dataclass(frozen=True)
class PostgresQueryExecutionParameters:
    attempt_efficient_postgres_execution: bool
    """
    Overrides QueryExecutionParameters.attempt_efficient_parameters if True
    """

    polars_read_csv: bool
    """
    When `attempt_postgres_efficient_execution` is True, this flag decides whether to use polars'
    read_csv or pyarrow's read_csv.
    """

    skip_datetime_timezone_cast: bool
    """
    skip datetime timezone casting, only under efficient execution. This happens BEFORE the sql query.
    """

    csv_read_then_cast: bool = True
    """DEPRECATED"""


@dataclass(frozen=True)
class SnowflakeQueryExecutionParameters:
    snowflake_unload_stage: Optional[str]
    """
    The name of the Snowflake stage to use for unloading data. If None, the default stage will be used.
    I.e. '@CHALK_UNLOAD_STAGE/test_1'
    """


@dataclass(frozen=True)
class BigqueryQueryExecutionParameters:
    bigquery_unload_path: Optional[str]
    """
    The name of the GCS or S3 bucket to use for unloading data. If None, queries will be executed to a temp table.
    """


@dataclass(frozen=True)
class QueryExecutionParameters:
    attempt_efficient_execution: bool
    """
    This will be overriden at query time if the source is a postgres source and
    PostgresQueryExecutionParameters.attempt_efficient_postgres_execution is True in the invoker
    """

    postgres: PostgresQueryExecutionParameters

    snowflake: SnowflakeQueryExecutionParameters

    bigquery: BigqueryQueryExecutionParameters

    yield_empty_batches: bool = False
    """Whether to yield empty batches. This can be useful to capture the schema of an otherwise-empty results set"""

    fallback_to_inefficient_execution: bool = True
    """Whether to fallback to inefficient execution if efficient execution fails for an unexpected error"""

    max_prefetch_size_bytes: int = 1024 * 1024 * 1024
    """If nonnegative, the maximum number of bytes to prefetched when executing a query. If zero or negative,
    then there is no limit to the number of bytes that can be prefetched."""

    num_client_prefetch_threads: int = 4
    """Number of threads to use when downloading query results."""

    tags: frozenset[str] = field(default_factory=frozenset)
    """Tags that can be used to select a source. These tags are proxied from the overlying Chalk query context."""


def query_execution_parameters_from_env_vars():
    """
    For when called in user resolver code.
    If you do not want to do efficient execution, set CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION_WITHOUT_EXCEPTION to True
    """
    return QueryExecutionParameters(
        attempt_efficient_execution=not env_var_bool("CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION"),
        max_prefetch_size_bytes=int(os.getenv("CHALK_MAX_PREFETCH_SIZE_BYTES", "1073741824")),
        num_client_prefetch_threads=int(os.getenv("CHALK_NUM_CLIENT_PREFETCH_THREADS", "4")),
        postgres=PostgresQueryExecutionParameters(
            attempt_efficient_postgres_execution=True,
            polars_read_csv=env_var_bool("CHALK_FORCE_POLARS_READ_CSV"),
            skip_datetime_timezone_cast=env_var_bool("CHALK_SKIP_PG_DATETIME_ZONE_CAST"),
        ),
        snowflake=SnowflakeQueryExecutionParameters(
            snowflake_unload_stage=os.getenv("CHALK_SNOWFLAKE_UNLOAD_STAGE", None),
        ),
        bigquery=BigqueryQueryExecutionParameters(
            bigquery_unload_path=os.getenv("CHALK_BIGQUERY_UNLOAD_PATH", None),
        ),
    )
