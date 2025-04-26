from __future__ import annotations

from os import PathLike
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Mapping, Optional, Protocol, Type, TypeVar, Union, overload

from chalk.features import DataFrame, Feature, Features
from chalk.sql._internal.incremental import IncrementalSettings
from chalk.utils.duration import Duration

if TYPE_CHECKING:
    import sqlalchemy
    import sqlalchemy.ext.asyncio

    from chalk.sql.finalized_query import DataframeFinalizedChalkQuery, SingletonFinalizedChalkQuery

TTableIngestProtocol = TypeVar("TTableIngestProtocol", bound="TableIngestProtocol")


class StringChalkQueryProtocol(Protocol):
    def execute(self) -> DataFrame:
        """Materialize the query.

        Chalk queries are lazy, which allows Chalk
        to perform performance optimizations like push-down filters.
        Instead of calling execute, consider returning this query from
        a resolver as an intermediate feature, and processing that
        intermediate feature in a different resolver.

        Returns
        -------
        DataFrame
            A `DataFrame` with the results of the query.
        """
        ans = self.all().execute()
        assert isinstance(ans, DataFrame)
        return ans

    def one_or_none(self) -> SingletonFinalizedChalkQuery:
        """Return at most one result or raise an exception.

        Returns `None` if the query selects no rows. Raises if
        multiple object identities are returned, or if multiple
        rows are returned for a query that returns only scalar
        values as opposed to full identity-mapped entities.

        Returns
        -------
        SingletonFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    def one(self) -> SingletonFinalizedChalkQuery:
        """Return exactly one result or raise an exception.

        Returns
        -------
        SingletonFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    def all(self) -> DataframeFinalizedChalkQuery:
        """Return the results represented by this Query as a list.

        Returns
        -------
        DataframeFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    @overload
    def incremental(
        self,
        *,
        incremental_column: str,
        lookback_period: Duration = "0s",
        mode: Literal["row", "group"] = "row",
        incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time",
    ) -> DataframeFinalizedChalkQuery:
        ...

    @overload
    def incremental(
        self,
        *,
        incremental_column: None = None,
        lookback_period: None = None,
        mode: Literal["parameter"],
        incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time",
    ) -> DataframeFinalizedChalkQuery:
        ...

    def incremental(
        self,
        *,
        incremental_column: Optional[str] = None,
        lookback_period: Optional[Duration] = "0s",
        mode: Literal["row", "group", "parameter"] = "row",
        incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time",
    ) -> DataframeFinalizedChalkQuery:
        """Operates like `.all()`, but tracks `previous_latest_row_timestamp` between query executions in
        order to limit the amount of data returned.

        `previous_latest_row_timestamp` will be set the start of the query execution, or if you return
        a `FeatureTime`-mapped column, Chalk will update `previous_latest_row_timestamp` to the maximum
        observed `FeatureTime` value.

        In `"row"` mode:
        `incremental_column` MUST be set.

        Returns the results represented by this query as a list (like `.all()`), but modifies the query to
        only return "new" results, by adding a clause that looks like:

            ```
            WHERE <incremental_column> >= <previous_latest_row_timestamp> - <lookback_period>
            ```

        In `"group"` mode:
        `incremental_column` MUST be set.

        Returns the results represented by this query as a list (like `.all()`), but modifies the query to
        only results from "groups" which have changed since the last run of the query.

        This works by (1) parsing your query, (2) finding the "group keys", (3) selecting only changed groups.
        Concretely:

            ```
            SELECT user_id, sum(amount) as sum_amount
            FROM payments
            GROUP BY user_id
            ```

        would be rewritten like this:

            ```
            SELECT user_id, sum(amount) as sum_amount
            FROM payments
            WHERE user_id in (
                SELECT DISTINCT(user_id)
                FROM payments WHERE created_at >= <previous_latest_row_timestamp> - <lookback_period>
            )
            GROUP BY user_id
            ```

        In `"parameter"` mode:
        `incremental_column` WILL BE IGNORED.

        This mode is for cases where you want full control of incrementalization. Chalk will not manipulate your query.
        Chalk will include a query parameter named `"chalk_incremental_timestamp"`. Depending on your SQL
        dialect, you can use this value to incrementalize your query with `:chalk_incremental_timestamp` or
        `%(chalk_incremental_timestamp)s`.

        Parameters
        ----------
        incremental_column
            This should reference a timestamp column in your underlying table, typically something
            like `"updated_at"`, `"created_at"`, `"event_time"`, etc.
        lookback_period
            Defaults to `0`, which means we only return rows that are strictly newer than
            the last observed row.
        mode
            Defaults to `"row"`, which indicates that only rows newer than the last observed row should be
            considered. When set to `"group"`, Chalk will only ingest features from groups which are newer
            than the last observation time. This requires that the query is grouped by a primary key.
        incremental_timestamp
            Defaults to `"feature_time"`, which means that the timestamp associated with the last feature value
            will be used as the incremental time. Alternatively, setting this parameter to `"resolver_execution_time"`
            will use last literal timestamp that the resolver ran.

        Returns
        -------
        DataframeFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...


class ChalkQueryProtocol(Protocol):
    def first(self) -> SingletonFinalizedChalkQuery:
        """Return the first result of this Query or None if the result doesn't contain any row.

        Returns
        -------
        SingletonFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    def one_or_none(self) -> SingletonFinalizedChalkQuery:
        """Return at most one result or raise an exception.

        Returns `None` if the query selects no rows. Raises if
        multiple object identities are returned, or if multiple
        rows are returned for a query that returns only scalar
        values as opposed to full identity-mapped entities.

        Returns
        -------
        SingletonFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    def one(self) -> SingletonFinalizedChalkQuery:
        """Return exactly one result or raise an exception.

        Returns
        -------
        SingletonFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    def all(self) -> DataframeFinalizedChalkQuery:
        """Return the results represented by this Query as a `DataFrame`.

        Returns
        -------
        DataframeFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    def incremental(
        self,
        lookback_period: Duration = "0s",
        mode: Literal["row", "group", "parameter"] = "row",
        incremental_column: Optional[Union[str, Feature]] = None,
        incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time",
        params: Optional[Mapping[str, Any]] = None,
    ) -> DataframeFinalizedChalkQuery:
        """Operates like `.all()`, but tracks `previous_latest_row_timestamp` between query executions in
        order to limit the amount of data returned.

        `previous_latest_row_timestamp` will be set the start of the query execution, or if you return
        a `FeatureTime`-mapped column, Chalk will update `previous_latest_row_timestamp` to the maximum
        observed `FeatureTime` value.

        In `"row"` mode:
        `incremental_column` MUST be set.

        Returns the results represented by this query as a list (like `.all()`), but modifies the query to
        only return "new" results, by adding a clause that looks like:

            ```
            WHERE <incremental_column> >= <previous_latest_row_timestamp> - <lookback_period>
            ```

        In `"group"` mode:
        `incremental_column` MUST be set.

        Returns the results represented by this query as a list (like `.all()`), but modifies the query to
        only results from "groups" which have changed since the last run of the query.

        This works by (1) parsing your query, (2) finding the "group keys", (3) selecting only changed groups.
        Concretely:

            ```
            SELECT user_id, sum(amount) as sum_amount
            FROM payments
            GROUP BY user_id
            ```

        would be rewritten like this:

            ```
            SELECT user_id, sum(amount) as sum_amount
            FROM payments
            WHERE user_id in (
                SELECT DISTINCT(user_id)
                FROM payments WHERE created_at >= <previous_latest_row_timestamp> - <lookback_period>
            )
            GROUP BY user_id
            ```

        In `"parameter"` mode:
        `incremental_column` WILL BE IGNORED.

        This mode is for cases where you want full control of incrementalization. Chalk will not manipulate your query.
        Chalk will include a query parameter named `"chalk_incremental_timestamp"`. Depending on your SQL
        dialect, you can use this value to incrementalize your query with `:chalk_incremental_timestamp` or
        `%(chalk_incremental_timestamp)s`.

        Parameters
        ----------
        incremental_column
            This should reference a timestamp column in your underlying table, typically something
            like `"updated_at"`, `"created_at"`, `"event_time"`, etc.
        lookback_period
            Defaults to `0`, which means we only return rows that are strictly newer than
            the last observed row.
        mode
            Defaults to `"row"`, which indicates that only rows newer than the last observed row should be
            considered. When set to `"group"`, Chalk will only ingest features from groups which are newer
            than the last observation time. This requires that the query is grouped by a primary key.
        incremental_timestamp
            Defaults to `"feature_time"`, which means that the timestamp associated with the last feature value
            will be used as the incremental time. Alternatively, setting this parameter to `"resolver_execution_time"`
            will use last literal timestamp that the resolver ran.

        Returns
        -------
        DataframeFinalizedChalkQuery
            A query that can be returned from a resolver.
        """
        ...

    def filter_by(self, **kwargs: Any) -> "ChalkQueryProtocol":
        """Apply the given filtering criterion to a copy of this Query,
        using keyword expressions.

        Parameters
        ----------
        kwargs
            The column names assigned to the desired values (i.e. `name="Maria"`).

        Returns
        -------
        ChalkQueryProtocol
            A query that can be returned from a resolver or further filtered.

        Examples
        --------
        >>> from chalk.sql import PostgreSQLSource
        >>> session = PostgreSQLSource()
        >>> session.query(UserFeatures(id=UserSQL.id)).filter_by(name="Maria")
        """

        ...

    def filter(self, *criterion: Any) -> "ChalkQueryProtocol":
        """Apply the given filtering criterion to a copy of this Query, using SQL expressions.

        Parameters
        ----------
        criterion
            SQLAlchemy filter criterion

        Returns
        -------
        ChalkQueryProtocol
            A query that can be returned from a resolver or further filtered.
        """
        ...

    def order_by(self, *clauses: Any) -> "ChalkQueryProtocol":
        """Apply one or more ORDER BY criteria to the query and return the newly resulting Query.

        Parameters
        ----------
        clauses
            SQLAlchemy columns.

        Returns
        -------
        ChalkQueryProtocol
            A query that can be returned from a resolver or further filtered.
        """
        ...

    def group_by(self, *clauses: Any) -> "ChalkQueryProtocol":
        ...

    def having(self, criterion: Any) -> "ChalkQueryProtocol":
        ...

    def union(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def union_all(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def intersect(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def intersect_all(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def join(self, target: Any, *props: Any, **kwargs: Any) -> "ChalkQueryProtocol":
        ...

    def outerjoin(self, target: Any, *props: Any, **kwargs: Any) -> "ChalkQueryProtocol":
        ...

    def select_from(self, *from_obj: Any) -> "ChalkQueryProtocol":
        ...

    def execute(self):
        """Materialize the query.

        Chalk queries are lazy, which allows Chalk to perform
        performance optimizations like push-down filters.
        Instead of calling execute, consider returning this query from
        a resolver as an intermediate feature, and processing that
        intermediate feature in a different resolver.

        Note: this requires the usage of the `fields={...}` argument when used in conjunction with `query_string`
        or `query_sql_file`.

        Returns
        -------
        Any
            The raw result of executing the query. For `.all()`, returns a `DataFrame`. For `.one()` or `.one_or_none()`,
            returns a `Features` instance corresponding to the relevant feature class.
        """
        return self.all().execute()


class BaseSQLSourceProtocol(Protocol):
    name: Optional[str]

    def query_string(
        self,
        query: str,
        fields: Optional[Mapping[str, Union[Feature, str, Any]]] = None,
        args: Optional[Mapping[str, object]] = None,
    ) -> StringChalkQueryProtocol:
        """Run a query from a SQL string.

        Parameters
        ----------
        query
            The query that you'd like to run.
        fields
            A mapping from the column names selected to features.
        args
            Any args in the sql string specified by `query` need
            to have corresponding value assignments in `args`.

        Returns
        -------
        StringChalkQueryProtocol
            A query that can be returned from a `@online` or `@offline` resolver.
        """
        ...

    def query_sql_file(
        self,
        path: Union[str, bytes, PathLike],
        fields: Optional[Mapping[str, Union[Feature, str, Any]]] = None,
        args: Optional[Mapping[str, object]] = None,
    ) -> StringChalkQueryProtocol:
        """Run a query from a SQL file.

        This method allows you to query the SQL file within a Python
        resolver. However, Chalk can also infer resolvers from SQL files.
        See https://docs.chalk.ai/docs/sql#sql-file-resolvers
        for more information.

        Parameters
        ----------
        path
            The path to the file with the sql file,
            relative to the caller's file, or to the
            directory that your `chalk.yaml` file lives in.
        fields
            A mapping from the column names selected to features.
        args
            Any args in the sql file specified by `path` need
            to have corresponding value assignments in `args`.

        Returns
        -------
        StringChalkQueryProtocol
            A query that can be returned from a `@online` or `@offline` resolver.
        """
        ...

    def query(self, *entities: Any) -> ChalkQueryProtocol:
        """Query using a `SQLAlchemy` model.

        Parameters
        ----------
        entities
            Arguments as would normally be passed to a `SQLAlchemy`.

        Returns
        -------
        ChalkQueryProtocol
            A query that can be returned from a resolver.
        """
        ...

    def get_engine(self) -> sqlalchemy.engine.Engine:
        """Get an SQLAlchemy Engine. The engine will be created and cached on the first call of this method.

        Returns
        -------
        sqlalchemy.engine.Engine
            A SQLAlchemy engine.
        """
        ...


class TableIngestProtocol(Protocol):
    def with_table(
        self: Type[TTableIngestProtocol],
        *,
        name: str,
        features: Type[Union[Features, Any]],
        ignore_columns: Optional[List[str]] = None,
        ignore_features: Optional[List[Union[str, Any]]] = None,
        require_columns: Optional[List[str]] = None,
        require_features: Optional[List[Union[str, Any]]] = None,
        column_to_feature: Optional[Dict[str, Any]] = None,
        cdc: Optional[Union[bool, IncrementalSettings]] = None,
    ) -> TTableIngestProtocol:
        """Automatically ingest a table.

        Parameters
        ----------
        name
            The name of the table to ingest.
        features
            The feature class that this table should be mapping to, e.g. `User`.
        ignore_columns
            Columns in the table that should be ignored, and not mapped to features,
            even if there is a matching name.
        ignore_features
            Features on the feature class that should be ignored, and not mapped to columns,
            even if there is a matching name.
        require_columns
            Columns that must exist in the mapping.
        require_features
            Features that must exist in the mapping.
        column_to_feature
            Explicit mapping of columns to features for names that do not match.
        cdc
            Settings for incrementally ingesting the table.

        Examples
        --------
        >>> from chalk.sql import PostgreSQLSource
        >>> from chalk.features import features
        >>> PostgreSQLSource().with_table(
        ...     name="users",
        ...     features=User,
        ... ).with_table(
        ...     name="accounts",
        ...     features=Account,
        ...     # Override one of the column mappings.
        ...     column_to_feature={
        ...         "acct_id": Account.id,
        ...     },
        ... )
        """
        ...


class SQLSourceWithTableIngestProtocol(TableIngestProtocol, BaseSQLSourceProtocol, Protocol):
    ...


__all__ = [
    "StringChalkQueryProtocol",
    "ChalkQueryProtocol",
    "BaseSQLSourceProtocol",
    "TableIngestProtocol",
    "SQLSourceWithTableIngestProtocol",
]
