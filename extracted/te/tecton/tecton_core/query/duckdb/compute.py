import dataclasses
import logging
import re
import typing
from typing import Optional
from typing import Union

import attrs
import pandas

from tecton_core.duckdb_factory import DuckDBConfig


try:
    import duckdb
except ImportError:
    msg = (
        "Couldn't initialize Rift compute. "
        "To use Rift install all Rift dependencies first by executing `pip install tecton[rift]`."
    )
    raise RuntimeError(msg)
import pyarrow.json
import sqlparse
from duckdb import DuckDBPyConnection

from tecton_core import conf
from tecton_core import duckdb_factory
from tecton_core.errors import TectonValidationError
from tecton_core.offline_store import S3Options
from tecton_core.query.dialect import Dialect
from tecton_core.query.errors import SQLCompilationError
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError
from tecton_core.schema_validation import cast_batch
from tecton_core.schema_validation import tecton_schema_to_arrow_schema


@dataclasses.dataclass
class _Cause:
    type_name: str
    message: str


_input_error_pattern = re.compile(
    r"Invalid Input Error: arrow_scan: get_next failed\(\): "
    + r"(?:Unknown error|Invalid): (.*)\. Detail: Python exception: (.*)",
    re.DOTALL,
)


def extract_input_error_cause(e: duckdb.InvalidInputException) -> Optional[_Cause]:
    m = _input_error_pattern.match(str(e))
    if m:
        return _Cause(message=m.group(1), type_name=m.group(2))
    else:
        return None


@attrs.define
class DuckDBCompute(SQLCompute):
    session: "DuckDBPyConnection"
    is_debug: bool = attrs.field(init=False)
    is_verbose_logs: bool = attrs.field(init=False)
    created_views: typing.List[str] = attrs.field(init=False)

    @staticmethod
    def from_context(
        duckdb_config: Optional[DuckDBConfig] = None,
    ) -> "DuckDBCompute":
        return DuckDBCompute(
            session=duckdb_factory.create_connection(duckdb_config),
        )

    def __attrs_post_init__(self):
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")
        self.is_verbose_logs = conf.QUERYTREE_VERBOSE.enabled()
        self.created_views = []

    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
        checkpoint_as: Optional[str] = None,
        s3_options: Optional[S3Options] = None,
    ) -> Optional[pyarrow.RecordBatchReader]:
        # Notes on case sensitivity:
        # 1. DuckDB is case insensitive when referring to column names, though preserves the
        #    underlying data casing when exporting to e.g. parquet.
        #    See https://duckdb.org/2022/05/04/friendlier-sql.html#case-insensitivity-while-maintaining-case
        #    This means that when using Snowflake for pipeline compute, the view + m13n schema is auto upper-cased
        # 2. When there is a spine provided, the original casing of that spine is used (since DuckDB separately
        #    registers the spine).
        # 3. When exporting values out of DuckDB (to user, or for ODFVs), we coerce the casing to respect the
        #    explicit schema specified. Thus ODFV definitions should reference the casing specified in the dependent
        #    FV's m13n schema.
        sql_string = sqlparse.format(sql_string, reindent=True)

        if self.is_verbose_logs:
            logging.warning(f"DUCKDB: run SQL {sql_string}")

        if monitor:
            monitor.set_query(sql_string)

        # Need to use DuckDB cursor (which creates a new connection based on the original connection)
        # to be thread-safe. It avoids a mysterious "unsuccessful or closed pending query result" error too.
        try:
            cursor = self.session.cursor()
            if s3_options:
                assert s3_options.region, "AWS Region must be specified. Consider setting CLUSTER_REGION in tecton.conf"
                cursor.execute(
                    f"""CREATE OR REPLACE secret aws_secret (
                     type s3,
                     key_id '{s3_options.access_key_id}',
                     secret '{s3_options.secret_access_key}',
                     session_token '{s3_options.session_token}',
                     endpoint 's3.{s3_options.region}.amazonaws.com',
                     region '{s3_options.region}')"""
                )

            # Although we set timezone globally, DuckDB still needs this cursor-level config to produce
            # correct arrow result. Otherwise, timestamps in arrow table will have a local timezone.
            cursor.sql("SET TimeZone='UTC'")
            duckdb_relation = cursor.sql(sql_string)
            if checkpoint_as:
                duckdb_relation.create(checkpoint_as)
                duckdb_relation = self.session.table(checkpoint_as)

            if return_dataframe:
                duckdb_reader = duckdb_relation.fetch_arrow_reader(
                    batch_size=int(conf.get_or_raise("DUCKDB_BATCH_SIZE"))
                )

                if expected_output_schema:
                    output_schema = tecton_schema_to_arrow_schema(expected_output_schema)
                else:
                    # Default to schema from reader (if needed)
                    output_schema = duckdb_reader.schema

                def batch_iterator():
                    for batch in duckdb_reader:
                        yield cast_batch(batch, output_schema)

                res = pyarrow.RecordBatchReader.from_batches(output_schema, batch_iterator())
            else:
                res = None

            if self.is_verbose_logs:
                logging.warning(self.session.sql("FROM duckdb_memory()"))

            return monitor.monitored_arrow_reader(res) if monitor and res else res
        except duckdb.InvalidInputException as e:
            # This means that the iterator we passed into DuckDB failed. If it failed due a TectonValidationError
            # we want to unwrap that to get rid of the noisy DuckDB context which is generally irrelevant to the
            # failure.
            cause = extract_input_error_cause(e)
            if not cause:
                raise
            for error_t in (CastError, TectonValidationError):
                if error_t.__name__ in cause.type_name:
                    raise error_t(cause.message) from None
            raise
        except duckdb.Error as e:
            raise SQLCompilationError(str(e), sql_string) from None

    def get_dialect(self) -> Dialect:
        return Dialect.DUCKDB

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pandas.DataFrame) -> None:
        self.session.from_df(pandas_df).create_view(table_name)
        self.created_views.append(table_name)

    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        self.session.from_arrow(table_or_reader).create_view(table_name)
        self.created_views.append(table_name)

    def unregister_temp_table(self, table_name: str) -> None:
        self.session.sql(f"DROP TABLE IF EXISTS {table_name}")

    def cleanup_temp_tables(self):
        for view in self.created_views:
            self.session.unregister(view)
        self.created_views = []
