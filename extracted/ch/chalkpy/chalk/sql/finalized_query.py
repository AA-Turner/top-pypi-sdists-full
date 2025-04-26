from __future__ import annotations

import dataclasses
import warnings
from collections import defaultdict
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    overload,
)

import pyarrow as pa

from chalk.features import DataFrame, Feature, Features
from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.query_execution_parameters import (
    QueryExecutionParameters,
    query_execution_parameters_from_env_vars,
)
from chalk.sql.protocols import BaseSQLSourceProtocol
from chalk.utils.async_helpers import async_enumerate
from chalk.utils.df_utils import pa_table_to_pl_df
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.string import normalize_string_for_matching

if TYPE_CHECKING:
    import sqlalchemy.ext.asyncio
    from sqlalchemy import Table
    from sqlalchemy.engine import Connection
    from sqlalchemy.sql import Select
    from sqlalchemy.sql.ddl import CreateTable, DropTable
    from sqlalchemy.sql.elements import TextClause


class Finalizer(str, Enum):
    ONE_OR_NONE = "OneOrNone"
    ONE = "One"
    FIRST = "First"
    ALL = "All"


def _get_matching_root_fqn(
    normalized_to_original_col: Mapping[str, str], expected_feature_root_fqns: Collection[str]
) -> dict[str, str]:
    # Returns a map from original_col to the matched columns
    candidates: List[str] = []
    lookup: defaultdict[str, list[str]] = defaultdict(list)
    for x in expected_feature_root_fqns:
        root_fqn_normalized = normalize_string_for_matching(x.lower())
        without_root_ns = normalize_string_for_matching(".".join(x.split(".")[1:]))
        lookup[root_fqn_normalized].append(x)
        lookup[without_root_ns].append(x)
        if len(x.split("@")) == 2:
            non_versioned = x.split("@")[0]
            non_versioned_normalized = normalize_string_for_matching(non_versioned.lower())
            non_versioned_without_root_ns = normalize_string_for_matching(".".join(non_versioned.split(".")[1:]))
            lookup[non_versioned_normalized].append(x)
            lookup[non_versioned_without_root_ns].append(x)

    new_mapped_cols = {}
    for normalized_col_name, original_col_name in normalized_to_original_col.items():
        if len(original_col_name.split("@")) == 2:
            version_number = original_col_name.split("@")[1]
            normalized_col_name = normalized_col_name[: -len(f"{version_number}")]
        candidates = lookup[normalized_col_name]
        if len(candidates) == 0:
            continue
        if len(candidates) > 1:
            # We really shouldn't hit this, unless if features are case-sensitive and the user is querying
            # snowflake which is case-insensitive
            raise ValueError(
                (
                    f"Column '{normalized_col_name}' was ambiguous which feature it referred to. "
                    f"Possible candidates were: {candidates}"
                )
            )
        new_mapped_cols[original_col_name] = candidates[0]
    return new_mapped_cols


class FinalizedChalkQuery:
    """A query that cannot be further filtered."""

    def __init__(
        self,
        query: Union[Select, TextClause],
        params: Mapping[str, Any],
        finalizer: Finalizer,
        incremental_settings: Optional[IncrementalSettings],
        source: BaseSQLSourceProtocol,
        fields: Mapping[str, Feature],
        temp_tables: (
            Mapping[str, Tuple[Mapping[str, sqlalchemy.types.TypeEngine], pa.Table, CreateTable, Table, DropTable]]
            | None
        ) = None,
        is_empty: bool = False,
    ) -> None:
        """
        :param fields: may be set to None, in which case it can be inferred from the output type of the resolver which returned this query using infer_fields_from_resolver_output
        """
        super().__init__()
        self._query = query
        self._params = dict(params)
        self._finalizer = finalizer
        self._incremental_settings = incremental_settings
        self._source = source
        self._fields = fields
        self._temp_tables = dict(temp_tables) if temp_tables is not None else {}
        self._is_empty = is_empty

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        raise RuntimeError(
            "FinalizedChalkQuery should not be subclassed. The Chalk runtime assumes that this class is final."
        )

    @property
    def incremental_settings(self):
        return self._incremental_settings

    @property
    def finalizer(self):
        return self._finalizer

    @property
    def query(self):
        return self._query

    @property
    def source(self):
        return self._source

    @property
    def fields(self):
        return self._fields

    @property
    def params(self):
        return self._params

    @property
    def temp_tables(self):
        return self._temp_tables

    @property
    def is_empty(self):
        return self._is_empty

    def infer_fields_from_resolver_outputs(self, expected_features: Sequence[Feature[Any, Any]] | None):
        if len(self._fields) > 0:
            return self
        if expected_features is None:
            return self
        new_fields = {f.name: f for f in expected_features}
        return FinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=self._finalizer,
            incremental_settings=self._incremental_settings,
            source=self._source,
            fields=new_fields,
            temp_tables=self._temp_tables,
            is_empty=self._is_empty,
        )

    def execute(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[Any] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> Union[Features, DataFrame, None]:
        """Actually execute the query to a `DataFrame` or set of features.

        If the finalizer was ONE, ONE_OR_NONE, or FIRST, then a `Features` instance
        is returned. Otherwise, if the `finalizer` is ALL, then a `DataFrame` instance
        is returned.

        Parameters
        ----------
        expected_features
            The list of expected features for the output, as provided by the resovler in which this query is executed.
            If not specified, the column names as returned by the query will be used to determine the output features.
        connection
            Execute the query using the supplied connection. If `None` (default), a new connection will be acquired
            from the underlying source for the query
        query_execution_parameters
            Parameters to decide method of efficient/inefficient execution

        Returns
        -------
        DataFrame
            A `DataFrame`, if the `.finalizer` is ALL; otherwise, `Features` set.
            If the finalizer is ONE_OR_NONE or FIRST, then the result may be
            `None` if no row was found
        """
        return self._pa_table_to_res(
            self.execute_to_pyarrow(expected_features, connection, query_execution_parameters),
            expected_features,
        )

    async def async_execute(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[Any] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> Union[Features, DataFrame, None]:
        """Actually execute the query to a `DataFrame` or set of features.

        If the finalizer was ONE, ONE_OR_NONE, or FIRST, then a `Features` instance
        is returned. Otherwise, if the `finalizer` is ALL, then a `DataFrame` instance
        is returned.

        Parameters
        ----------
        expected_features
            The list of expected features for the output, as provided by the resovler in which this query is executed.
            If not specified, the column names as returned by the query will be used to determine the output features.
        connection
            Execute the query using the supplied connection. If `None` (default), a new connection will be acquired
            from the underlying source for the query
        query_execution_parameters
            Parameters to decide method of efficient/inefficient execution

        Returns
        -------
        DataFrame
            A `DataFrame`, if the `.finalizer` is ALL; otherwise, `Features` set.
            If the finalizer is ONE_OR_NONE or FIRST, then the result may be
            `None` if no row was found
        """
        return self._pa_table_to_res(
            await self.async_execute_to_pyarrow(expected_features, connection, query_execution_parameters),
            expected_features,
        )

    def _pa_table_to_res(self, pa_table: pa.RecordBatch | pa.Table, expected_features: Optional[Sequence[Feature]]):
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        pa_table = self._postprocess_table(0, pa_table)
        if isinstance(pa_table, pa.RecordBatch):
            pa_table = pa.Table.from_batches([pa_table])
        df = pa_table_to_pl_df(pa_table)
        assert isinstance(df, pl.DataFrame)
        if self._finalizer in (Finalizer.ONE_OR_NONE, Finalizer.FIRST) and len(df) == 0:
            return None
        res = DataFrame(df)
        if self._finalizer in (Finalizer.ONE, Finalizer.ONE_OR_NONE, Finalizer.FIRST):
            return res.slice(0, 1).to_features()[0]
        return res

    def _get_col_to_feature(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
    ):
        expected_feature_root_fqns = (
            None if expected_features is None else frozenset(x.root_fqn for x in expected_features)
        )

        def col_to_features(column_names: Sequence[str]) -> Mapping[str, Feature]:
            # First map the column names to determine the feature fqns
            col_name_mapping = self.get_col_name_mapping(tuple(column_names), expected_feature_root_fqns)
            return {k: Feature.from_root_fqn(v) for (k, v) in col_name_mapping.items()}

        return col_to_features

    def _check_incremental_settings(self):
        if self.incremental_settings is not None:
            # FIXME: Move the incrementalization logic here, so then the `execute` and `execute_to_dataframe`
            # methods can take the hwm timestamp as a parameter, to allow for direct execution
            warnings.warn(
                (
                    "This query specified an incremental configuration, which has not been applied. "
                    "This is likely because the resolver is being executed directly. "
                    "The query will be attempted without any high-water-mark timestamp. "
                    "This will attempt to select all data, "
                    "or if the filters depend on the incremental timestamp, "
                    "will result in a query execution error. "
                )
            )

    def execute_to_pyarrow(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[Connection] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> pa.Table:
        """Actually execute the query, and return a PyArrow table. Unlike :meth:`.execute`, this method will always keep the
        results as a PyArrow table, even if the finalizer implies a singleton results (e.g. ONE, ONE_OR_NONE, or FIRST).

        Parameters
        ----------
        expected_features
            The list of expected features for the output, as provided by the resolver in which this query is executed.
            If not specified, the column names as returned by the query will be used to determine the output features.
        connection
            Execute the query using the supplied connection. If None (the default), then a new connection will be acquired
            from the underlying source for the query
        query_execution_parameters
            Optional, but should be set if called from the engine. Contains options that decide the query execution
            codepath.

        Returns
        -------
        Table
            A `pa.Table`, even if the result contains 0 or 1 rows.
        """
        if query_execution_parameters is None:
            query_execution_parameters = query_execution_parameters_from_env_vars()
        query_execution_parameters = dataclasses.replace(query_execution_parameters, yield_empty_batches=True)
        batches = list(self.execute_to_pyarrow_batches(expected_features, connection, query_execution_parameters))
        if len(batches) == 0:
            # This should be impossible to reach because we specify yield_empty_batches=True, so batches should generally contain at least one element
            if expected_features is None:
                # We have no idea what the expected schema is. This should
                return pa.Table.from_pydict({})
            else:
                return pa.Table.from_pydict(
                    {k.root_fqn: [] for k in expected_features},
                    pa.schema({k.root_fqn: k.converter.pyarrow_dtype for k in expected_features}),
                )
        return pa.Table.from_batches(batches)

    def execute_to_pyarrow_batches(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[Connection] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> Iterable[pa.RecordBatch]:
        """Actually execute the query, and return a stream of `pa.RecordBatch`.

        Parameters
        ----------
        expected_features
            The list of expected features for the output, as provided by the resolver in which this query is executed.
            If not specified, the column names as returned by the query will be used to determine the output features.
        connection
            Execute the query using the supplied connection. If None (the default), then a new connection will be acquired
            from the underlying source for the query
        query_execution_parameters
            Optional, but should be set if called from the engine. Contains options that decide the query execution
            codepath.

        Yields
        ------
        A stream of `pa.RecordBatch`
        """
        from chalk.sql._internal.sql_source import BaseSQLSource
        from chalk.sql._internal.sql_source_group import SQLSourceGroup

        self._check_incremental_settings()
        col_to_features = self._get_col_to_feature(expected_features)
        assert isinstance(self.source, (BaseSQLSource, SQLSourceGroup)), f"Expected BaseSQLSource, got {self.source}"

        if query_execution_parameters is None:
            query_execution_parameters = query_execution_parameters_from_env_vars()

        total_row_count = 0

        for i, pa_table in enumerate(
            self.source.execute_query(
                finalized_query=self,
                columns_to_features=col_to_features,
                connection=connection,
                query_execution_parameters=query_execution_parameters,
            )
        ):
            assert (
                len(pa_table) > 0 or query_execution_parameters.yield_empty_batches
            ), "Should never yield empty batches"
            pa_table = self._postprocess_table(i, pa_table)
            total_row_count += len(pa_table)
            yield pa_table
            if self.finalizer == Finalizer.FIRST and total_row_count > 0:
                break
        if total_row_count == 0 and self.finalizer == Finalizer.ONE:
            raise ValueError("Expected exactly one row; got 0 rows")

    async def async_execute_to_pyarrow(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[sqlalchemy.ext.asyncio.AsyncConnection] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> pa.Table:
        """Actually execute the query, and return a PyArrow table. Unlike :meth:`.execute`, this method will always keep the
        results as a PyArrow table, even if the finalizer implies a singleton results (e.g. ONE, ONE_OR_NONE, or FIRST).

        Parameters
        ----------
        expected_features
            The list of expected features for the output, as provided by the resolver in which this query is executed.
            If not specified, the column names as returned by the query will be used to determine the output features.
        connection
            Execute the query using the supplied connection. If None (the default), then a new connection will be acquired
            from the underlying source for the query
        query_execution_parameters
            Optional, but should be set if called from the engine. Contains options that decide the query execution
            codepath.

        Returns
        -------
        Table
            A `pa.Table`, even if the result contains 0 or 1 rows.
        """
        if query_execution_parameters is None:
            query_execution_parameters = query_execution_parameters_from_env_vars()
        query_execution_parameters = dataclasses.replace(query_execution_parameters, yield_empty_batches=True)
        batches: list[pa.RecordBatch] = []
        async for batch in self.async_execute_to_pyarrow_batches(
            expected_features, connection, query_execution_parameters
        ):
            batches.append(batch)
        if len(batches) == 0:
            # This should be impossible to reach because we specify yield_empty_batches=True, so batches should generally contain at least one element
            if expected_features is None:
                # We have no idea what the expected schema is
                return pa.Table.from_pydict({})
            else:
                return pa.Table.from_pydict(
                    {k.root_fqn: [] for k in expected_features},
                    pa.schema({k.root_fqn: k.converter.pyarrow_dtype for k in expected_features}),
                )
        return pa.Table.from_batches(batches)

    async def async_execute_to_pyarrow_batches(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[sqlalchemy.ext.asyncio.AsyncConnection] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> AsyncIterable[pa.RecordBatch]:
        """Actually execute the query, and return a stream of pa.RecordBatches.

        Parameters
        ----------
        expected_features
            The list of expected features for the output, as provided by the resolver in which this query is executed.
            If not specified, the column names as returned by the query will be used to determine the output features.
        connection
            Execute the query using the supplied connection. If None (the default), then a new connection will be acquired
            from the underlying source for the query
        query_execution_parameters
            Optional, but should be set if called from the engine. Contains options that decide the query execution
            codepath.

        Yields
        ------
        A stream of `pa.RecordBatch`
        """
        from chalk.sql._internal.sql_source import BaseSQLSource

        if query_execution_parameters is None:
            query_execution_parameters = query_execution_parameters_from_env_vars()

        self._check_incremental_settings()
        col_to_features = self._get_col_to_feature(expected_features)
        assert isinstance(self.source, BaseSQLSource)

        total_row_count = 0

        async for i, pa_table in async_enumerate(
            self.source.async_execute_query(self, col_to_features, connection, query_execution_parameters)
        ):
            assert (
                len(pa_table) > 0 or query_execution_parameters.yield_empty_batches
            ), "Should never yield empty batches"
            pa_table = self._postprocess_table(i, pa_table)
            total_row_count += len(pa_table)
            yield pa_table
            if self.finalizer == Finalizer.FIRST and total_row_count > 0:
                break

        if total_row_count == 0 and self.finalizer == Finalizer.ONE:
            raise ValueError("Expected exactly one row; got 0 rows")

    @overload
    def _postprocess_table(self, i: int, pa_table: pa.RecordBatch) -> pa.RecordBatch:
        ...

    @overload
    def _postprocess_table(self, i: int, pa_table: pa.Table) -> pa.Table:  # pyright: ignore[reportOverlappingOverload]
        ...

    def _postprocess_table(self, i: int, pa_table: pa.RecordBatch | pa.Table) -> pa.RecordBatch | pa.Table:
        if len(pa_table) == 0:
            return pa_table
        if i > 0:
            if self.finalizer == Finalizer.ONE_OR_NONE:
                raise ValueError(f"Expected zero or one rows, but got multiple batches")
            if self.finalizer == Finalizer.ONE:
                raise ValueError(f"Expected one row, but got multiple batches")
            assert self.finalizer != Finalizer.FIRST
        if self._finalizer == Finalizer.ONE:
            if len(pa_table) != 1:
                raise ValueError(f"Expected exactly one row; got {len(pa_table)} rows")

        if self._finalizer == Finalizer.ONE_OR_NONE:
            if len(pa_table) > 1:
                raise ValueError(f"Expected zero or one rows; got {len(pa_table)} rows")

        if self._finalizer in (Finalizer.ONE, Finalizer.ONE_OR_NONE, Finalizer.FIRST):
            pa_table = pa_table.slice(0, 1)
        return pa_table

    def execute_to_dataframe(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[Connection] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ):
        # DEPRECATED -- will be removed soon. Only used internally
        """Actually execute the query, and return a DataFrame. Unlike :meth:`.execute`, this method will always keep the
        results as a DataFrame, even if the finalizer implies a singleton results (e.g. ONE, ONE_OR_NONE, or FIRST).

        Parameters
        ----------
        expected_features
            The list of expected features for the output, as provided by the resovler in which this query is executed.
            If not specified, the column names as returned by the query will be used to determine the output features.
        connection
            Execute the query using the supplied connection. If None (the default), then a new connection will be acquired
            from the underlying source for the query
        query_execution_parameters
            Parameters to decide method of efficient/inefficient execution

        Returns
        -------
        DataFrame
            A `DataFrame`, even if the result contains 0 or 1 rows.
        """
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        pa_table = self.execute_to_pyarrow(expected_features, connection, query_execution_parameters)
        df = pa_table_to_pl_df(pa_table)
        assert isinstance(df, pl.DataFrame)
        return DataFrame(df)

    def get_col_name_mapping(
        self,
        result_columns: Tuple[str, ...],
        expected_features: Optional[Collection[str]],
    ) -> Dict[str, str]:
        """Map the output columns to the expected feature names.

        Parameters
        ----------
        result_columns
            A list of the columns, in order, returned by the query.
        expected_features
            The expected feature root fqns for the query, as provided by the resolver signature.
            If a column name that is not in `fields` corresponds to a column in `expected_features`,
            then it will be mapped automatically.
            If a feature in `expected_features` does not have a corresponding output column,
            an error is raised.

        Returns
        -------
        dict[str, str]
            A mapping from output column names to root names.
        """
        ans: Dict[str, str] = {}
        normalized_to_original_col = {normalize_string_for_matching(x): x for x in result_columns}
        for k, v in self._fields.items():
            original_col_name = normalized_to_original_col.get(normalize_string_for_matching(k))
            if original_col_name is None:
                received_columns = ", ".join(result_columns)
                raise ValueError(
                    f"Required column '{k}' was not returned by the query. Got columns: {received_columns}"
                )
            ans[original_col_name] = v.root_fqn
        if expected_features is not None:
            unexpected_fields = [x for x in self._fields.values() if x.root_fqn not in expected_features]
            for x in unexpected_fields:
                del ans[normalized_to_original_col[normalize_string_for_matching(x.root_fqn)]]
            unsolved_normalized_to_original_col = {
                normalized_col: original_col
                for normalized_col, original_col in normalized_to_original_col.items()
                if original_col not in ans
            }
            ans.update(_get_matching_root_fqn(unsolved_normalized_to_original_col, expected_features))
        return ans


if TYPE_CHECKING:

    class SingletonFinalizedChalkQuery(FinalizedChalkQuery, Features):
        """A FinalizedChalkQuery that returns a single row when executed"""

        # Subclassing from Features so it can does not cause type errors when used in a resolver
        # that is annotated to return a Features instance
        ...

    class DataframeFinalizedChalkQuery(FinalizedChalkQuery, DataFrame):
        """A FinalizedChalkQuery that returns a DataFrame when executed"""

        # Subclassing from DataFrame so it can does not cause type errors when used in a resolver
        # that is annotated to return a DataFrame
        ...

else:
    SingletonFinalizedChalkQuery = FinalizedChalkQuery
    DataframeFinalizedChalkQuery = FinalizedChalkQuery
