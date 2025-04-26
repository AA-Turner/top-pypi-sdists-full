import dataclasses
import logging
import re
import typing
from typing import Iterable
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
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.query.dialect import Dialect
from tecton_core.query.errors import SQLCompilationError
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError


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
    created_views: typing.List[str] = attrs.field(init=False)
    offline_store_options: Iterable[OfflineStoreOptionsProvider] = ()

    @staticmethod
    def from_context(
        offline_store_options: Iterable[OfflineStoreOptionsProvider] = (), duckdb_config: Optional[DuckDBConfig] = None
    ) -> "DuckDBCompute":
        return DuckDBCompute(
            session=duckdb_factory.create_connection(duckdb_config), offline_store_options=offline_store_options
        )

    def __attrs_post_init__(self):
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")
        self.created_views = []

    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
        checkpoint_as: Optional[str] = None,
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
        if self.is_debug:
            logging.warning(f"DUCKDB: run SQL {sql_string}")

        if monitor:
            monitor.set_query(sql_string)

        # Need to use DuckDB cursor (which creates a new connection based on the original connection)
        # to be thread-safe. It avoids a mysterious "unsuccessful or closed pending query result" error too.
        try:
            cursor = self.session.cursor()
            # Although we set timezone globally, DuckDB still needs this cursor-level config to produce
            # correct arrow result. Otherwise, timestamps in arrow table will have a local timezone.
            cursor.sql("SET TimeZone='UTC'")
            duckdb_relation = cursor.sql(sql_string)
            if checkpoint_as:
                duckdb_relation.create(checkpoint_as)
                duckdb_relation = self.session.table(checkpoint_as)

            if return_dataframe:
                res = duckdb_relation.fetch_arrow_reader(batch_size=int(conf.get_or_raise("DUCKDB_BATCH_SIZE")))
            else:
                res = None

            if self.is_debug:
                logging.warning(self.session.sql("FROM duckdb_memory()"))

            return res
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
