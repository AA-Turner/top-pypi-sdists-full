"""Lightweight DataFrame wrapper around Chalk's execution engine.

The :class:`DataFrame` class constructs query plans backed by ``libchalk`` and
can materialize them into Arrow tables.  It offers a minimal API similar to
other DataFrame libraries while delegating heavy lifting to the underlying
engine.
"""

from __future__ import annotations

import typing
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TypeAlias

import pyarrow

import chalk._gen.chalk.dataframe.v1.dataframe_pb2 as dataframe_pb2
import chalk._gen.chalk.expression.v1.expression_pb2 as expression_pb2
from chalk.features._encoding.converter import PrimitiveFeatureConverter
from chalk.features.underscore import (
    Underscore,
    UnderscoreAttr,
    UnderscoreCall,
    UnderscoreRoot,
    convert_value_to_proto_expr,
)

if TYPE_CHECKING:
    from chalk.features import Underscore


MaterializedTable: TypeAlias = pyarrow.RecordBatch | pyarrow.Table


@dataclass
class _LazyFrameConstructor:
    """
    A lazily-called function which will be used to construct a Chalk DataFrame.
    """

    self_dataframe: "Optional[LazyFramePlaceholder]"
    """If present, this is the value of 'self' to call the function on."""

    function_name: str
    """The name of the function to construct the DataFrame."""

    args: tuple[Any, ...]
    """The args to pass to the DataFrame function."""

    kwargs: dict[str, Any]
    """The kwargs to pass to the DataFrame function."""


class LazyFramePlaceholder:
    """
    A lazy representation of a DataFrame operation.

    Examples
    --------
    >>> from chalk.df import LazyFramePlaceholder
    >>> from chalk.features import _
    >>> # Create from a dictionary
    >>> df = LazyFramePlaceholder.named_table('input', pa.schema({"id": pa.int64(), "name": pa.string()}))
    >>> # Apply operations
    >>> filtered = df.filter(_.x > 1)
    """

    @staticmethod
    def _construct(
        *,
        self_dataframe: "Optional[LazyFramePlaceholder]",
        function_name: str,
        args: tuple[Any, ...] = (),
        **kwargs: Any,
    ):
        return LazyFramePlaceholder(
            _internal_constructor=_LazyFrameConstructor(
                self_dataframe=self_dataframe,
                function_name=function_name,
                args=tuple(args),
                kwargs=kwargs,
            )
        )

    def __init__(
        self,
        *,
        _internal_constructor: _LazyFrameConstructor,
    ):
        """
        An internal construct that creates a `LazyFramePlaceholder` from its underlying operation.
        """

        super().__init__()
        self._lazy_frame_constructor = _internal_constructor

    def __repr__(self) -> str:
        return "LazyFramePlaceholder(...)"

    __str__ = __repr__

    def _is_equal(self, other: LazyFramePlaceholder) -> bool:
        # proto equality is janky but it's hard to write a good eq method here given
        # we have dicts and the proto round trip is slightly lossy on tuples vs lists
        return self._to_proto() == other._to_proto()

    def _to_proto(self) -> dataframe_pb2.DataFramePlan:
        """
        Convert this proto plan to a dataframe.
        """
        return _convert_to_dataframe_proto(self)

    @staticmethod
    def _from_proto(proto: dataframe_pb2.DataFramePlan) -> "LazyFramePlaceholder":
        """
        Parse a `LazyFramePlaceholder` from the specified proto plan.
        """
        return _convert_from_dataframe_proto(proto, dataframe_class=LazyFramePlaceholder)

    @classmethod
    def named_table(cls, name: str, schema: pyarrow.Schema) -> LazyFramePlaceholder:
        """Create a ``DataFrame`` for a named table.

        Parameters
        ----------
        name
            Table identifier.
        schema
            Arrow schema describing the table.

        Returns
        -------
        DataFrame referencing the named table.
        """

        if not isinstance(name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError(
                f"LazyFramePlaceholder.named_table expected `name` to have type 'str' but it was passed as a '{type(name)}'"
            )
        if not isinstance(schema, pyarrow.Schema):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError(
                f"LazyFramePlaceholder.named_table expected `schema` to have type 'pyarrow.Schema' but it was passed as a '{type(schema)}'"
            )

        return LazyFramePlaceholder._construct(
            function_name="named_table",
            self_dataframe=None,
            name=name,
            schema=schema,
        )

    @classmethod
    def from_arrow(cls, data: MaterializedTable):
        """Construct a DataFrame from an in-memory Arrow object.

        Parameters
        ----------
        data
            PyArrow Table or RecordBatch to convert into a DataFrame.

        Returns
        -------
        DataFrame backed by the provided Arrow data.

        Examples
        --------
        >>> import pyarrow as pa
        >>> from chalkdf import DataFrame
        >>> table = pa.table({"x": [1, 2, 3], "y": ["a", "b", "c"]})
        >>> df = DataFrame.from_arrow(table)
        """

        assert isinstance(data, (pyarrow.Table, pyarrow.RecordBatch))

        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="from_arrow",
            data=data,
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Construct a DataFrame from a Python dictionary.

        Parameters
        ----------
        data
            Dictionary mapping column names to lists of values.

        Returns
        -------
        DataFrame backed by the provided dictionary data.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": ["a", "b", "c"]})
        """

        return LazyFramePlaceholder.from_arrow(pyarrow.table(data))

    @classmethod
    def scan(
        cls,
        input_uris: typing.Sequence[str | Path],
        *,
        name: typing.Optional[str] = None,
        schema: pyarrow.Schema | None = None,
    ) -> "LazyFramePlaceholder":
        """Scan files and return a DataFrame.

        Currently supports CSV (with headers) and Parquet file formats.

        Parameters
        ----------
        input_uris
            List of file paths or URIs to scan. Supports local paths and file:// URIs.
        name
            Optional name to assign to the table being scanned.
        schema
            Schema of the data. Required for CSV files, optional for Parquet.

        Returns
        -------
        DataFrame that reads data from the specified files.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> # Scan Parquet files
        >>> df = DataFrame.scan(["data/sales_2024.parquet"], name="sales_data")
        >>> # Scan CSV with explicit schema
        >>> import pyarrow as pa
        >>> schema = pa.schema([("id", pa.int64()), ("name", pa.string())])
        >>> df = DataFrame.scan(["data/users.csv"], name="users", schema=schema)
        """
        # Accept filesystem paths or URIs; construct file:// URIs manually for
        # local paths to avoid percent-encoding partition tokens like '='.

        if isinstance(input_uris, str):
            raise ValueError(
                "The LazyFramePlaceholder.scan() function must be called with a list of input_uris, not a single str URI"
            )

        if name is None:
            name = str(uuid.uuid4())

        normalized_input_uris: list[str] = []
        for p in input_uris:
            s = p if isinstance(p, str) else str(p)
            if "://" in s:
                normalized_input_uris.append(s)
            else:
                abs_path = str(Path(s).resolve())
                if not abs_path.startswith("/"):
                    normalized_input_uris.append(Path(s).resolve().as_uri())
                else:
                    normalized_input_uris.append("file://" + abs_path)

        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="scan",
            name=name,
            input_uris=normalized_input_uris,
            schema=schema,
        )

    @classmethod
    def scan_glue_iceberg(
        cls,
        glue_table_name: str,
        schema: typing.Mapping[str, pyarrow.DataType],
        *,
        batch_row_count: int = 1_000,
        aws_catalog_account_id: typing.Optional[str] = None,
        aws_catalog_region: typing.Optional[str] = None,
        aws_role_arn: typing.Optional[str] = None,
        parquet_scan_range_column: typing.Optional[str] = None,
        custom_partitions: typing.Optional[dict[str, tuple[typing.Literal["date_trunc(day)"], str]]] = None,
        partition_column: typing.Optional[str] = None,
    ) -> "LazyFramePlaceholder":
        """Load data from an AWS Glue Iceberg table.

        Parameters
        ----------
        glue_table_name
            Fully qualified ``database.table`` name.
        schema
            Mapping of column names to Arrow types.
        batch_row_count
            Number of rows per batch.
        aws_catalog_account_id
            AWS account hosting the Glue catalog.
        aws_catalog_region
            Region of the Glue catalog.
        aws_role_arn
            IAM role to assume for access.
        parquet_scan_range_column
            Column used for range-based reads.
        custom_partitions
            Additional partition definitions.
        partition_column
            Column name representing partitions.

        Returns
        -------
        DataFrame backed by the Glue table.
        """

        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="scan_glue_iceberg",
            schema=schema,
            batch_row_count=batch_row_count,
            aws_catalog_account_id=aws_catalog_account_id,
            aws_catalog_region=aws_catalog_region,
            aws_role_arn=aws_role_arn,
            filter_predicate=None,
            parquet_scan_range_column=parquet_scan_range_column,
            custom_partitions=custom_partitions,
            partition_column=partition_column,
        )

    @classmethod
    def from_sql(
        cls,
        query: str,
    ) -> LazyFramePlaceholder:
        """Create a ``DataFrame`` from the result of executing a SQL query (DuckDB dialect).

        Parameters
        ----------
        query
            SQL query string (DuckDB dialect).
        **tables
            Named tables to use in the query. Can be Arrow Table, RecordBatch, or DataFrame.

        Returns
        -------
        DataFrame containing the query results.
        """

        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="from_sql",
            query=query,
        )

    def with_columns(
        self,
        *columns: typing.Mapping[str, Underscore] | Underscore | tuple[str, Underscore],
    ) -> LazyFramePlaceholder:
        """Add or replace columns.

        Accepts multiple forms:
        - A mapping of column names to expressions
        - Positional tuples of (name, expression)
        - Bare positional expressions that must include ``.alias(<name>)``

        Parameters
        ----------
        *columns
            Column definitions as mappings, tuples, or aliased expressions.

        Returns
        -------
        DataFrame with the specified columns added or replaced.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.features import _
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        >>> # Add a new column using a dict with _ syntax
        >>> df2 = df.with_columns({"z": _.x + _.y})
        >>> # Add a new column using alias
        >>> df3 = df.with_columns((_.x + _.y).alias("z"))
        """
        entries: list[tuple[str, Underscore]] = []
        if len(columns) == 0:
            raise ValueError("with_columns requires at least one column expression")

        for col in columns:
            if isinstance(col, (list, tuple)):
                if len(col) != 2:
                    raise ValueError(
                        f"LazyFramePlaceholder.with_column(...) cannot be called with tuple having {len(col)} members - expect (name, expression) pairs only."
                    )
                entries.append(col)
            elif isinstance(col, Underscore):
                attempted_alias = _extract_alias_from_underscore(col)
                if attempted_alias:
                    entries.append(attempted_alias)
                else:
                    raise ValueError(
                        f"Positional with_columns expressions must use `.alias(...)` to set the column name, got expression '{col}' without any alias specified"
                    )
            elif isinstance(col, typing.Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
                entries.extend((k, v) for k, v in col.items())  # pyright: ignore
            else:
                raise ValueError(
                    f"LazyFramePlaceholder.with_columns cannot be called with column argument `{repr(col)}`"
                )

        return LazyFramePlaceholder._construct(
            self_dataframe=self,
            function_name="with_columns",
            args=tuple(entries),
        )

    def with_unique_id(self, name: str) -> LazyFramePlaceholder:
        """Add a monotonically increasing unique identifier column.

        Parameters
        ----------
        name
            Name of the new ID column.

        Returns
        -------
        DataFrame with a new column containing unique, incrementing IDs.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [10, 20, 30]})
        >>> df_with_id = df.with_unique_id("row_id")
        """

        return LazyFramePlaceholder._construct(
            self_dataframe=self,
            function_name="with_unique_id",
            name=name,
        )

    def filter(self, expr: Underscore) -> LazyFramePlaceholder:
        """Filter rows based on a boolean expression.

        Parameters
        ----------
        expr
            Boolean expression to filter rows. Only rows where the expression
            evaluates to True are kept.

        Returns
        -------
        DataFrame containing only the rows that match the filter condition.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.features import _
        >>> df = DataFrame.from_dict({"x": [1, 2, 3, 4], "y": [10, 20, 30, 40]})
        >>> filtered = df.filter(_.x > 2)
        """

        return LazyFramePlaceholder._construct(
            self_dataframe=self,
            function_name="filter",
            expr=expr,
        )

    def slice(self, start: int, length: int | None = None) -> LazyFramePlaceholder:
        """Return a subset of rows starting at a specific position.

        Parameters
        ----------
        start
            Zero-based index where the slice begins.
        length
            Number of rows to include. If None, includes all remaining rows.

        Returns
        -------
        DataFrame containing the sliced rows.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [1, 2, 3, 4, 5]})
        >>> # Get rows 1-3 (indices 1, 2, 3)
        >>> sliced = df.slice(1, 3)
        """

        # Can't actually express "no limit" with velox limit/offset, but this'll do.
        return self._construct(
            self_dataframe=self,
            function_name="slice",
            start=start,
            length=length,
        )

    def col(self, column: str) -> Underscore:
        """Get a column expression from the DataFrame.

        Parameters
        ----------
        column
            Name of the column to retrieve.

        Returns
        -------
        Column expression (as Underscore) that can be used in operations.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.features import _
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        >>> # Use col to reference columns in expressions
        >>> df_filtered = df.filter(_.x > 1)
        """
        return self.column(column)

    def column(self, column: str) -> Underscore:
        """Get a column expression from the DataFrame.

        Alias for col() method.

        Parameters
        ----------
        column
            Name of the column to retrieve.

        Returns
        -------
        Column expression (as Underscore) that can be used in operations.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.features import _
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        >>> df_sum = df.with_columns({"sum": _.x + _.y})
        """

        # The LazyFramePlaceholder does not currently track schema, so it cannot detect
        # errors about missing columns.
        return UnderscoreAttr(UnderscoreRoot(), column)

    def project(self, columns: typing.Mapping[str, Underscore]) -> "LazyFramePlaceholder":
        """Project to a new set of columns using expressions.

        Parameters
        ----------
        columns
            Mapping of output column names to expressions that define them.

        Returns
        -------
        DataFrame with only the specified columns.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.features import _
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        >>> projected = df.project({"sum": _.x + _.y, "x": _.x})
        """

        return self._construct(
            self_dataframe=self,
            function_name="project",
            columns=columns,
        )

    def select(self, *columns: str | Underscore, strict: bool = True) -> "LazyFramePlaceholder":
        """Select existing columns by name.

        Parameters
        ----------
        *columns
            Names of columns to select.
        strict
            If True, raise an error if any column doesn't exist. If False,
            silently ignore missing columns.

        Returns
        -------
        DataFrame with only the selected columns.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6], "z": [7, 8, 9]})
        >>> selected = df.select("x", "y")
        """

        return self._construct(
            self_dataframe=self,
            function_name="select",
            args=columns,
            strict=strict,
        )

    def drop(self, *columns: str | Underscore, strict: bool = True) -> LazyFramePlaceholder:
        """Drop specified columns from the DataFrame.

        Parameters
        ----------
        *columns
            Names of columns to drop.
        strict
            If True, raise an error if any column doesn't exist. If False,
            silently ignore missing columns.

        Returns
        -------
        DataFrame without the dropped columns.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6], "z": [7, 8, 9]})
        >>> df_dropped = df.drop("z")
        """

        return self._construct(
            self_dataframe=self,
            function_name="drop",
            args=columns,
            strict=strict,
        )

    def explode(self, column: str | Underscore) -> "LazyFramePlaceholder":
        """Explode a list or array column into multiple rows.

        Each element in the list becomes a separate row, with other column
        values duplicated.

        Parameters
        ----------
        column
            Name of the list/array column to explode.

        Returns
        -------
        DataFrame with the list column expanded into multiple rows.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"id": [1, 2], "items": [[10, 20], [30]]})
        >>> exploded = df.explode("items")
        """
        return self._construct(
            self_dataframe=self,
            function_name="explode",
            column=column,
        )

    def join(
        self,
        other: "LazyFramePlaceholder",
        *,
        on: typing.Mapping[str | Underscore, str | Underscore] | typing.Sequence[str | Underscore] | None = None,
        left_on: typing.Sequence[str | Underscore] | None = None,
        right_on: typing.Sequence[str | Underscore] | None = None,
        how: str = "inner",
        right_suffix: str | None = None,
    ) -> "LazyFramePlaceholder":
        """Join this ``DataFrame`` with another.

        Parameters
        ----------
        other
            Right-hand ``DataFrame``.
        on
            Join keys. Can be specified in multiple ways:
            - A sequence of column names (same names on both sides): ``on=["col1", "col2"]``
            - A mapping of left->right column names: ``on={"left_col": "right_col"}``
            - If None, must specify ``left_on`` and ``right_on`` separately.
        left_on
            Column names for left DataFrame join keys. Only used when ``on`` is None.
            Must be paired with ``right_on``.
        right_on
            Column names for right DataFrame join keys. Only used when ``on`` is None.
            Must be paired with ``left_on``.
        how
            Join type. Supported values:
            - ``"inner"``: Keep only rows that match in both DataFrames (default)
            - ``"left"``: Keep all rows from left DataFrame
            - ``"right"``: Keep all rows from right DataFrame
            - ``"outer"`` or ``"full"``: Keep all rows from both DataFrames
            - ``"semi"``: Return rows from left that have matches in right (no right columns)
            - ``"anti"``: Return rows from left that have no matches in right
            - ``"cross"``: Cartesian product (do not pass in ``on``)
        right_suffix
            Optional suffix applied to right-hand columns when names collide.
            For example, if both DataFrames have a column ``"value"`` and ``right_suffix="_right"``,
            the result will have ``"value"`` and ``"value_right"``.

        Returns
        -------
        Resulting ``DataFrame`` after the join.
        """

        return self._construct(
            self_dataframe=self,
            function_name="join",
            other=other,
            on=on,
            left_on=left_on,
            right_on=right_on,
            how=how,
            right_suffix=right_suffix,
        )

    def join_asof(
        self,
        other: "LazyFramePlaceholder",
        *,
        on: str | Underscore | None = None,
        left_on: str | Underscore | None = None,
        right_on: str | Underscore | None = None,
        by: typing.Mapping[str | Underscore, str | Underscore] | typing.Sequence[str | Underscore] | None = None,
        left_by: typing.Sequence[str | Underscore] | None = None,
        right_by: typing.Sequence[str | Underscore] | None = None,
        strategy: typing.Literal["forward", "backward"] = "backward",
        right_suffix: str | None = None,
        coalesce: bool = True,
    ) -> LazyFramePlaceholder:
        """Perform an as-of join with another DataFrame.

        An as-of join is similar to a left join, but instead of matching on equality,
        it matches on the nearest key from the right DataFrame. This is commonly used
        for time-series data where you want to join with the most recent observation.

        **Important**: Both DataFrames must be sorted by the ``on`` (or ``left_on/right_on``)
        column before calling this method. Use ``.order_by(on)`` to sort if needed.

        Parameters
        ----------
        other
            Right-hand DataFrame to join with.
        on
            Column name to use as the as-of join key (must be sorted).
            This column is used for both left and right DataFrames.
            The join finds the nearest match according to the ``strategy``.
            Either ``on`` or both ``left_on`` and ``right_on`` must be specified.
        left_on
            Column name in left DataFrame for the as-of join key. Only used when ``on``
            is None. Must be paired with ``right_on``.
        right_on
            Column name in right DataFrame for the as-of join key. Can be used with ``on``
            (to specify a different right column name) or with ``left_on`` (when ``on`` is None).
        by
            Additional exact-match columns (optional). These columns must match exactly
            before performing the as-of match on the ``on`` column. Can be specified as:
            - A sequence of column names (same names on both sides): ``by=["col1", "col2"]``
            - A mapping of left->right column names: ``by={"left_col": "right_col"}``
            - If None, can specify ``left_by`` and ``right_by`` separately.
        left_by
            Column names in left DataFrame for exact-match conditions. Only used when
            ``by`` is None. Must be paired with ``right_by``.
        right_by
            Column names in right DataFrame for exact-match conditions. Only used when
            ``by`` is None. Must be paired with ``left_by``.
        strategy
            Join strategy controlling which match to select:
            - ``"backward"`` (default): Match with the most recent past value
            - ``"forward"``: Match with the nearest future value
            Can also pass ``AsOfJoinStrategy.BACKWARD`` or ``AsOfJoinStrategy.FORWARD``.
        right_suffix
            Suffix to add to overlapping column names from the right DataFrame.
        coalesce
            Whether to coalesce the join keys (default True).

        Returns
        -------
        Resulting DataFrame after the as-of join.
        """
        # Convert string strategy to enum if needed

        return self._construct(
            self_dataframe=self,
            function_name="join_asof",
            other=other,
            on=on,
            left_on=left_on,
            right_on=right_on,
            by=by,
            left_by=left_by,
            right_by=right_by,
            strategy=strategy,
            right_suffix=right_suffix,
            coalesce=coalesce,
        )

    # # Window is not yet supported in LazyFramePlaceholder:
    # def window(
    #     self,
    #     by: typing.Sequence[str | Underscore],
    #     order_by: typing.Sequence[str | Underscore | tuple[str | Underscore, str]],
    #     *expressions: WindowExpr,
    # ) -> LazyFramePlaceholder:
    #     ...

    def agg(self, by: typing.Sequence[str | Underscore], *aggregations: Underscore) -> "LazyFramePlaceholder":
        """Group by columns and apply aggregation expressions.

        Parameters
        ----------
        by
            Column names to group by.
        *aggregations
            Aggregation expressions to apply to each group (e.g., sum, count, mean).

        Returns
        -------
        DataFrame with one row per group containing the aggregated values.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.features import _
        >>> df = DataFrame.from_dict({"group": ["A", "A", "B"], "value": [1, 2, 3]})
        >>> agg_df = df.agg(["group"], _.value.sum().alias("total"))
        """

        if isinstance(by, str):
            raise ValueError(f".agg(...) must be called with a list of group-by columns, not a single str {repr(by)}")

        return self._construct(
            self_dataframe=self,
            function_name="agg",
            args=(by, *aggregations),
        )

    def distinct_on(self, *columns: str | Underscore) -> "LazyFramePlaceholder":
        """Remove duplicate rows based on specified columns.

        For rows with identical values in the specified columns, only one
        row is kept (chosen arbitrarily).

        Parameters
        ----------
        *columns
            Column names to check for duplicates.

        Returns
        -------
        DataFrame with duplicate rows removed.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [1, 1, 2], "y": [10, 20, 30]})
        >>> unique = df.distinct_on("x")
        """

        return self._construct(
            self_dataframe=self,
            function_name="distinct_on",
            args=columns,
        )

    def order_by(self, *columns: str | Underscore | tuple[str | Underscore, str]) -> LazyFramePlaceholder:
        """Sort the DataFrame by one or more columns.

        Parameters
        ----------
        *columns
            Column names to sort by. Can be strings (for ascending order) or
            tuples of (column_name, direction) where direction is "asc" or "desc".

        Returns
        -------
        DataFrame sorted by the specified columns.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [3, 1, 2], "y": [30, 10, 20]})
        >>> # Sort by x ascending
        >>> sorted_df = df.order_by("x")
        >>> # Sort by x descending, then y ascending
        >>> sorted_df = df.order_by(("x", "desc"), "y")
        """

        return self._construct(
            self_dataframe=self,
            function_name="order_by",
            args=columns,
        )

    def write(
        self,
        target_path: str,
        target_file_name: str | None = None,
        *,
        file_format: str = "parquet",
        serde_parameters: typing.Mapping[str, str] | None = None,
        compression: str | None = None,
        ensure_files: bool = False,
        connector_id: str | None = None,
    ) -> "LazyFramePlaceholder":
        """Persist the DataFrame plan using Velox's Hive connector.

        Parameters
        ----------
        target_path
            Directory to write output files.
        target_file_name
            Optional explicit file name.
        file_format
            Output format (default ``parquet``).
        serde_parameters
            Optional SerDe options for text formats.
        compression
            Optional compression codec.
        ensure_files
            Ensure writers emit files even if no rows were produced.
        connector_id
            Optional connector id override.

        Returns
        -------
        DataFrame representing the TableWrite operator.
        """

        return self._construct(
            self_dataframe=self,
            function_name="write",
            target_path=target_path,
            target_file_name=target_file_name,
            file_format=file_format,
            serde_parameters=serde_parameters,
            compression=compression,
            ensure_files=ensure_files,
            connector_id=connector_id,
        )

    def rename(self, new_names: typing.Mapping[str | Underscore, str]) -> LazyFramePlaceholder:
        """Rename columns in the DataFrame.

        Parameters
        ----------
        new_names
            Dictionary mapping old column names to new column names.

        Returns
        -------
        DataFrame with renamed columns.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        >>> renamed = df.rename({"x": "id", "y": "value"})
        """

        return self._construct(
            self_dataframe=self,
            function_name="rename",
            new_names=new_names,
        )

    @staticmethod
    def from_proto(
        proto: bytes | dataframe_pb2.DataFramePlan,
    ) -> "LazyFramePlaceholder":
        if isinstance(proto, bytes):
            proto_bytes = proto
            proto = dataframe_pb2.DataFramePlan()
            proto.ParseFromString(proto_bytes)
        return _convert_from_dataframe_proto(proto, dataframe_class=LazyFramePlaceholder)


def _extract_alias_from_underscore(u: Underscore) -> tuple[str, Underscore] | None:
    """
    Given an underscore expression like `_.something.alias("name")` splits the expression
    into the alias `"name"` and the underscore expression `_.something`.

    If this expression does not have an alias, returns `None` instead.
    """
    if not isinstance(u, UnderscoreCall):
        return None
    parent = u._chalk__parent  # pyright: ignore[reportPrivateUsage]
    if not isinstance(parent, UnderscoreAttr) or parent._chalk__attr != "alias":  # pyright: ignore[reportPrivateUsage]
        return None
    if len(u._chalk__args) != 1:  # pyright: ignore[reportPrivateUsage]
        raise ValueError("alias() must be called with one argument")
    alias = u._chalk__args[0]  # pyright: ignore[reportPrivateUsage]
    if not isinstance(alias, str):
        raise ValueError("argument to alias() must be a string")
    return (
        alias,
        parent._chalk__parent,  # pyright: ignore[reportPrivateUsage]
    )


def _convert_to_dataframe_proto(
    lazy_frame: LazyFramePlaceholder,
) -> dataframe_pb2.DataFramePlan:
    """
    Converts a `LazyFramePlaceholder` into a proto value, allowing it to be round-tripped
    or converted into a Chalk DataFrame for execution.
    """
    df_constructors: list[dataframe_pb2.DataFrameConstructor] = []

    # This map will memoize the constructor for a specified `LazyFramePlaceholder`.
    lazy_frame_placeholder_cache: dict[LazyFramePlaceholder, dataframe_pb2.DataFrameIndex] = {}

    def _convert_dataframe(df: LazyFramePlaceholder) -> dataframe_pb2.DataFrameIndex:
        """
        Recursively converts a `LazyFramePlaceholder` into a proto message.
        If this `df` instance has been seen before, returns an index into the `df_constructors`
        list pointing to the previous construction.

        This allows plans that re-use operators to be efficiently encoded.
        """
        if df in lazy_frame_placeholder_cache:
            return lazy_frame_placeholder_cache[df]

        df_constructor = df._lazy_frame_constructor  # pyright: ignore[reportPrivateUsage]
        if df_constructor.self_dataframe is None:
            self_proto = None
        else:
            self_proto = _convert_dataframe(df_constructor.self_dataframe)

        proto_args = dataframe_pb2.PyList(
            list_items=[_convert_arg(arg_value) for arg_value in df_constructor.args],
        )
        proto_kwargs = dataframe_pb2.PyDict(
            dict_entries=[
                dataframe_pb2.PyDictEntry(
                    entry_key=_convert_arg(kwarg_name),
                    entry_value=_convert_arg(kwarg_value),
                )
                for kwarg_name, kwarg_value in df_constructor.kwargs.items()
            ],
        )

        new_constructor_index = len(df_constructors)
        df_constructors.append(
            dataframe_pb2.DataFrameConstructor(
                self_operand=self_proto,
                function_name=df_constructor.function_name,
                args=proto_args,
                kwargs=proto_kwargs,
            )
        )
        lazy_frame_placeholder_cache[df] = dataframe_pb2.DataFrameIndex(
            dataframe_op_index=new_constructor_index,
        )
        return lazy_frame_placeholder_cache[df]

    def _convert_arg(value: Any) -> dataframe_pb2.DataFrameOperand:
        if value is None:
            return dataframe_pb2.DataFrameOperand(
                value_none=dataframe_pb2.PyNone(),
            )
        if isinstance(value, int):
            return dataframe_pb2.DataFrameOperand(
                value_int=value,
            )
        if isinstance(value, str):
            return dataframe_pb2.DataFrameOperand(
                value_string=value,
            )
        if isinstance(value, bool):
            return dataframe_pb2.DataFrameOperand(
                value_bool=value,
            )
        if isinstance(value, (list, tuple)):
            return dataframe_pb2.DataFrameOperand(
                value_list=dataframe_pb2.PyList(
                    list_items=[_convert_arg(item) for item in value],
                )
            )
        if isinstance(value, typing.Mapping):
            return dataframe_pb2.DataFrameOperand(
                value_dict=dataframe_pb2.PyDict(
                    dict_entries=[
                        dataframe_pb2.PyDictEntry(
                            entry_key=_convert_arg(key),
                            entry_value=_convert_arg(value),
                        )
                        for key, value in value.items()
                    ]
                )
            )
        if isinstance(value, LazyFramePlaceholder):
            # Use the dataframe-specific helper function for this logic.
            return dataframe_pb2.DataFrameOperand(
                value_dataframe_index=_convert_dataframe(value),
            )
        if isinstance(value, Underscore):
            return dataframe_pb2.DataFrameOperand(
                underscore_expr=convert_value_to_proto_expr(value),
            )
        if isinstance(value, pyarrow.Schema):
            return dataframe_pb2.DataFrameOperand(
                arrow_schema=PrimitiveFeatureConverter.convert_pa_schema_to_proto_schema(value),
            )
        if isinstance(value, (pyarrow.Table, pyarrow.RecordBatch)):
            return dataframe_pb2.DataFrameOperand(
                arrow_table=PrimitiveFeatureConverter.convert_arrow_table_to_proto(value),
            )

        # If libchalk.chalktable is available in the current environment, then we might encounter
        # a libchalk.chalktable.Expr value which needs to be proto-serialized.
        LibchalkExpr = None
        try:
            from libchalk.chalktable import Expr as LibchalkExpr  # pyright: ignore
        except ImportError:
            pass
        if LibchalkExpr and isinstance(value, LibchalkExpr):
            value_expr_encoded = value.to_proto_bytes()
            return dataframe_pb2.DataFrameOperand(
                libchalk_expr=expression_pb2.LogicalExprNode.FromString(value_expr_encoded),
            )

        raise ValueError(f"LazyFramePlaceholder function operand is of unsupported type {type(value)}")

    _convert_arg(lazy_frame)

    return dataframe_pb2.DataFramePlan(
        constructors=df_constructors,
    )


def _convert_from_dataframe_proto(
    proto_plan: dataframe_pb2.DataFramePlan,
    dataframe_class: type,
) -> LazyFramePlaceholder:
    """
    Converts a proto into a lazy frame.
    """
    df_values: list[LazyFramePlaceholder] = []

    def _convert_dataframe_index(df: dataframe_pb2.DataFrameIndex) -> LazyFramePlaceholder:
        if df.dataframe_op_index < 0 or df.dataframe_op_index >= len(df_values):
            raise ValueError(
                f"DataFrame proto message value is invalid - a DataFrame constructor references operator index {df.dataframe_op_index} but only {len(df_values)} dataframe(s) intermediate values have been defined so far."
            )
        return df_values[df.dataframe_op_index]

    def _convert_dataframe(df: dataframe_pb2.DataFrameConstructor) -> LazyFramePlaceholder:
        if df.HasField("self_operand"):
            self_operand = _convert_dataframe_index(df.self_operand)
        else:
            self_operand = None

        # TODO: validate that function_name is legal.
        if self_operand is None:
            method = getattr(dataframe_class, df.function_name)
        else:
            method = getattr(self_operand, df.function_name)

        args = [_convert_arg(arg) for arg in df.args.list_items]
        kwargs = {_convert_arg(entry.entry_key): _convert_arg(entry.entry_value) for entry in df.kwargs.dict_entries}

        return method(*args, **kwargs)

    def _convert_arg(value: dataframe_pb2.DataFrameOperand) -> Any:
        if value.HasField("value_string"):
            return value.value_string
        if value.HasField("value_int"):
            return value.value_int
        if value.HasField("value_bool"):
            return value.value_bool
        if value.HasField("value_none"):
            return None
        if value.HasField("value_list"):
            return [_convert_arg(item) for item in value.value_list.list_items]
        if value.HasField("value_dict"):
            return {
                _convert_arg(entry.entry_key): _convert_arg(entry.entry_value)
                for entry in value.value_dict.dict_entries
            }
        if value.HasField("value_dataframe_index"):
            return _convert_dataframe_index(value.value_dataframe_index)
        if value.HasField("arrow_schema"):
            return PrimitiveFeatureConverter.convert_proto_schema_to_pa_schema(value.arrow_schema)
        if value.HasField("arrow_table"):
            return PrimitiveFeatureConverter.convert_arrow_table_from_proto(value.arrow_table)
        if value.HasField("underscore_expr"):
            return Underscore._from_proto(value.underscore_expr)  # pyright: ignore[reportPrivateUsage]
        if value.HasField("libchalk_expr"):
            # In order to decode `libchalk_expr` vlaues, `libchalk` must be available as a module.
            try:
                from libchalk.chalktable import Expr as LibchalkExpr  # pyright: ignore
            except ImportError:
                raise ValueError(
                    "A dataframe parameter was encoded holding a libchalk.chalktable.Expr value, but the `libchalk` module is not available in the current environment. To decode this dataframe expression, import libchalk."
                )
            return LibchalkExpr.from_proto_bytes(value.libchalk_expr.SerializeToString())

        raise ValueError(f"DataFrame operand expression {value} does not have any value set")

    for df in proto_plan.constructors:
        df_values.append(_convert_dataframe(df))

    if len(df_values) == 0:
        raise ValueError(
            "Could not parse LazyFramePlaceholder from proto expression; no dataframe constructors were present in the provided proto message"
        )

    return df_values[-1]
