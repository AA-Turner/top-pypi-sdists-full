"""Lightweight DataFrame wrapper around Chalk's execution engine.

The :class:`DataFrame` class constructs query plans backed by ``libchalk`` and
can materialize them into Arrow tables.  It offers a minimal API similar to
other DataFrame libraries while delegating heavy lifting to the underlying
engine.
"""

from __future__ import annotations

import typing
import uuid
from collections.abc import Mapping
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
class _LazyFrameGroupBy:
    """
    A lazy representation of the chalkdf GroupBy class
    """

    _lf: LazyFramePlaceholder
    _by: typing.Sequence[str | Underscore]

    def _construct(self, *, function_name: str, args: tuple[Any, ...] = (), **kwargs: Any):
        return self._lf._construct(  # pyright:ignore[reportPrivateUsage]
            self_dataframe=self._lf._construct(  # pyright:ignore[reportPrivateUsage]
                self_dataframe=self._lf,
                function_name="group_by",
                args=tuple(self._by),
            ),
            function_name=function_name,
            args=args,
            **kwargs,
        )

    def agg(self, *aggregations: Underscore, pre_grouped_keys: typing.Sequence[str] = ()):
        """Apply the specified aggregation expressions to the group"""
        return self._construct(function_name="agg", args=aggregations, pre_grouped_keys=list(pre_grouped_keys))

    def all(self):
        """Apply ``array_agg``"""
        return self._construct(function_name="all")

    def count(self):
        """Apply ``count``"""
        return self._construct(function_name="count")

    def count_distinct(self):
        """Apply ``count_distinct``"""
        return self._construct(function_name="count_distinct")

    def max(self):
        """Apply ``max``"""
        return self._construct(function_name="max")

    def mean(self):
        """Apply ``mean``"""
        return self._construct(function_name="mean")

    def min(self):
        """Apply ``min``"""
        return self._construct(function_name="min")

    def sum(self):
        """Apply ``sum``"""
        return self._construct(function_name="sum")

    def head(
        self,
        n: int,
        order_by: typing.Sequence = (),
        rank_function: typing.Literal["row_number", "rank", "dense_rank"] = "row_number",
        rank_column: str | None = None,
    ) -> "LazyFramePlaceholder":
        """Return the first ``n`` rows per group, optionally ordered within each group."""
        # Only record the rank kwargs when they differ from the defaults. The
        # recorded call is replayed against whatever chalkdf the engine ships,
        # which may predate these parameters; emitting them unconditionally
        # would break every `group_by().head()` on such an engine.
        rank_kwargs: dict[str, Any] = {}
        if rank_function != "row_number":
            rank_kwargs["rank_function"] = rank_function
        if rank_column is not None:
            rank_kwargs["rank_column"] = rank_column
        return self._construct(
            function_name="head",
            n=n,
            order_by=list(order_by),
            **rank_kwargs,
        )


@dataclass
class _LazyFrameGroupingSetsGroupBy:
    """
    A lazy representation of the chalkdf GroupingSetsGroupBy class
    (returned by ``DataFrame.rollup`` / ``.cube`` / ``.grouping_sets``).
    The construction call is stored verbatim so it can be replayed
    against the real DataFrame — only at that point does the chosen
    multi-set form (rollup vs cube vs explicit grouping_sets) and the
    optional ``grouping_id_col`` kwarg take effect.
    """

    _lf: LazyFramePlaceholder
    _function_name: str
    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]

    def _construct(self, *, function_name: str, args: tuple[Any, ...] = (), **kwargs: Any):
        return self._lf._construct(  # pyright:ignore[reportPrivateUsage]
            self_dataframe=self._lf._construct(  # pyright:ignore[reportPrivateUsage]
                self_dataframe=self._lf,
                function_name=self._function_name,
                args=self._args,
                **self._kwargs,
            ),
            function_name=function_name,
            args=args,
            **kwargs,
        )

    def agg(self, *aggregations: Underscore):
        """Apply the specified aggregation expressions to each (grouping
        set, key-combo) cell."""
        return self._construct(function_name="agg", args=aggregations)

    def count(self):
        """Apply ``count`` per (grouping set, key-combo) cell."""
        return self._construct(function_name="count")

    def max(self):
        """Apply ``max`` to every non-by column."""
        return self._construct(function_name="max")

    def mean(self):
        """Apply ``mean`` to every non-by column."""
        return self._construct(function_name="mean")

    def min(self):
        """Apply ``min`` to every non-by column."""
        return self._construct(function_name="min")

    def sum(self):
        """Apply ``sum`` to every non-by column."""
        return self._construct(function_name="sum")


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


class WriteConfigLike(typing.Protocol):
    """Structural type for a chalkdf ``WriteConfig`` (``KeyValueOnlineStoreConfig``,
    ``VectorStoreConfig``, ``SnowflakeWarehouseConfig``, ...).

    chalkpy cannot import the concrete config types -- they live in chalkdf, which
    depends on chalkpy, not the reverse -- so ``write_to`` accepts anything that can
    serialize itself to a proto-friendly wire mapping via ``to_wire``.
    """

    def to_wire(self) -> dict[str, Any]: ...


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
    def named_table(cls, name: str, schema: pyarrow.Schema, sorted_by: list[str] | None = None) -> LazyFramePlaceholder:
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
            sorted_by=sorted_by,
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
        mode: typing.Literal["auto", "hive", "delta"] = "auto",
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
        mode
            Scan schema inference mode:
            - ``"auto"``: infer file type from URI/path suffix (CSV/Parquet).
            - ``"hive"``: expand Hive/glob paths without Delta inference fallback.
            - ``"delta"``: treat the input as a Delta table root (requires exactly one URI).
            - ``"iceberg"``: treat the input as an Iceberg table root (requires exactly one URI).
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
            input_uris = [input_uris]

        if mode not in ("auto", "hive", "delta"):
            raise ValueErorr(f"Mode must be one of(auto, hive, delta) got, {str(mode)}")

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
            mode=mode,
        )

    @classmethod
    def scan_iceberg(
        cls,
        table: str,
        *,
        schema: typing.Optional[pyarrow.Schema] = None,
        storage_options: typing.Optional[typing.Mapping[str, str]] = None,
        snapshot_id: typing.Optional[int] = None,
    ) -> "LazyFramePlaceholder":
        """Scan an Iceberg table that is registered in a catalog.

        Parameters
        ----------
        table
            Catalog-qualified table identifier. For Glue, ``database.table``.
            Also used as the plan-node name.
        schema
            Optional Arrow schema. If omitted, inferred from the Iceberg catalog.
        storage_options
            Apache Iceberg catalog + FileIO properties. ``None`` uses the
            ambient catalog configuration from the host engine's environment.
        snapshot_id
            Pin the scan to a specific snapshot id. ``None`` selects the
            current snapshot at plan time.

        Returns
        -------
        DataFrame backed by the catalog-resolved Iceberg table.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="scan_iceberg",
            table=table,
            schema=schema,
            storage_options=storage_options,
            snapshot_id=snapshot_id,
        )

    @classmethod
    def scan_delta(
        cls,
        table: str,
        *,
        storage_options: typing.Optional[typing.Mapping[str, str]] = None,
        schema: typing.Optional[pyarrow.Schema] = None,
        row_sample: typing.Optional[float] = None,
    ) -> "LazyFramePlaceholder":
        """Scan a Delta Lake table by URI or Unity Catalog three-part name.

        Parameters
        ----------
        table
            Delta table URI or Unity Catalog three-part name. Also used as the
            plan-node name.
        storage_options
            Object-store, Unity Catalog, and/or cross-account role configuration
            forwarded to the engine. ``None`` falls back to ambient credentials.

            To assume an IAM role for cross-account S3 access, pass:

            - ``client.assume-role.arn='arn:aws:iam::<account>:role/<role>'``
            - ``client.assume-role.external-id='<id>'`` (optional, for trust
              policies with an ``sts:ExternalId`` condition)
            - ``client.assume-role.session-name='<name>'`` (optional)
            - ``region_name`` or ``aws_region``

            See :meth:`chalkdf.DataFrame.scan_delta` for the Unity Catalog keys.
        schema
            Optional pyarrow schema. If omitted, inferred from Delta metadata,
            which reads the table at plan time. Passing one explicitly skips that
            read -- useful to speed up deploys, to keep a deploy from depending on
            the table being reachable, or to pin the schema against upstream
            changes.
        row_sample
            Bernoulli row-level sample rate in ``(0, 1]``. ``None`` disables.

        Returns
        -------
        DataFrame backed by the Delta table.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="scan_delta",
            table=table,
            storage_options=storage_options,
            schema=schema,
            row_sample=row_sample,
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
        filter_predicate: typing.Optional[typing.Any] = None,
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
            glue_table_name=glue_table_name,
            schema=schema,
            batch_row_count=batch_row_count,
            aws_catalog_account_id=aws_catalog_account_id,
            aws_catalog_region=aws_catalog_region,
            aws_role_arn=aws_role_arn,
            filter_predicate=filter_predicate,
            parquet_scan_range_column=parquet_scan_range_column,
            custom_partitions=custom_partitions,
            partition_column=partition_column,
        )

    def write_iceberg(
        self,
        table: str,
        *,
        storage_options: typing.Optional[typing.Mapping[str, str]] = None,
        shard_id: int = 0,
        num_retries: int = 3,
        num_internal_retries: int = 3,
        partition_spec: typing.Optional[typing.List[typing.Tuple[str, str]]] = None,
    ) -> "LazyFramePlaceholder":
        """Write this DataFrame to an Iceberg table.

        Parameters
        ----------
        table
            Either a catalog-qualified identifier (``"namespace.name"``) or a
            direct URI (``s3://…``, ``file://…``).
        storage_options
            Iceberg catalog + FileIO properties. See :meth:`scan_iceberg`. For
            catalog-mode writes ``"warehouse"`` is the storage prefix under
            which new tables are materialized at ``<warehouse>/<namespace>/<name>``.
            ``None`` uses ambient configuration from the host engine's environment.
        shard_id
            Shard identifier for the write (used for partitioned writes).
        num_retries
            Number of end-to-end retries for the write operation.
        num_internal_retries
            Number of retries for the catalog commit step.
        partition_spec
            List of ``(column_name, transform)`` pairs defining how the table is partitioned.
            Supported transforms: ``"identity"``, ``"year"``, ``"month"``, ``"day"``, ``"hour"``,
            ``"bucket[N]"``, ``"truncate[N]"``. If omitted, new tables are created unpartitioned
            and existing tables reuse their current partition spec.

        Returns
        -------
        DataFrame
            A passthrough DataFrame (same data as input); run it to execute the write.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=self,
            function_name="write_iceberg",
            table=table,
            storage_options=storage_options,
            shard_id=shard_id,
            num_retries=num_retries,
            num_internal_retries=num_internal_retries,
            partition_spec=partition_spec,
        )

    def write_glue_iceberg(
        self,
        glue_table_name: str,
        uri: str,
        *,
        shard_id: int = 0,
        num_retries: int = 3,
        num_internal_retries: int = 3,
        aws_catalog_account_id: typing.Optional[str] = None,
        aws_catalog_region: typing.Optional[str] = None,
        aws_role_arn: typing.Optional[str] = None,
        partition_spec: typing.Optional[typing.List[typing.Tuple[str, str]]] = None,
    ) -> "LazyFramePlaceholder":
        """Write this DataFrame to an AWS Glue Iceberg table.

        Parameters
        ----------
        glue_table_name
            Fully qualified ``database.table`` name.
        uri
            S3 URI where Iceberg data files are stored (e.g. ``s3://bucket/prefix``).
        shard_id
            Shard identifier for the write (used for partitioned writes).
        num_retries
            Number of end-to-end retries for the write operation.
        num_internal_retries
            Number of retries for the catalog commit step.
        aws_catalog_account_id
            AWS account hosting the Glue catalog.
        aws_catalog_region
            Region of the Glue catalog.
        aws_role_arn
            IAM role to assume for access.
        partition_spec
            List of ``(column_name, transform)`` pairs defining how the table is partitioned.
            Supported transforms: ``"identity"``, ``"year"``, ``"month"``, ``"day"``, ``"hour"``,
            ``"bucket[N]"``, ``"truncate[N]"``. If omitted, new tables are created unpartitioned
            and existing tables reuse their current partition spec.

        Returns
        -------
        DataFrame
            A passthrough DataFrame (same data as input); run it to execute the write.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=self,
            function_name="write_glue_iceberg",
            glue_table_name=glue_table_name,
            uri=uri,
            shard_id=shard_id,
            num_retries=num_retries,
            num_internal_retries=num_internal_retries,
            aws_catalog_account_id=aws_catalog_account_id,
            aws_catalog_region=aws_catalog_region,
            aws_role_arn=aws_role_arn,
            partition_spec=partition_spec,
        )

    @classmethod
    def from_sql(
        cls,
        query: str,
        **tables: typing.Any,
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
            **tables,
        )

    @classmethod
    def from_stream_source(
        cls,
        source: typing.Any,
        n: int,
        *,
        timeout_ms: int = 15000,
        include_metadata: bool = False,
    ) -> LazyFramePlaceholder:
        """Create a DataFrame by pulling messages from a streaming source.

        This method connects to a Kafka, Kinesis, or PubSub source and pulls up to `n`
        messages, returning them as a DataFrame.

        Parameters
        ----------
        source
            A streaming source configuration. Can be one of:
            - ``KafkaSource``: Kafka topic configuration
            - ``KinesisSource``: Kinesis stream configuration
            - ``PubSubSource``: Google PubSub subscription configuration
        n
            Maximum number of messages to pull from the stream.
        timeout_ms
            Timeout in milliseconds for pulling messages. Default is 15000ms.
        include_metadata
            If False (default), returns a DataFrame with a single "value" column
            containing the raw message bytes.
            If True, returns a DataFrame with columns for topic, partition, offset,
            timestamp, key, and value.

        Returns
        -------
        DataFrame containing the messages from the stream.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.streams import KafkaSource
        >>> source = KafkaSource(
        ...     name="my_kafka",
        ...     bootstrap_server="localhost:9092",
        ...     topic="my_topic",
        ... )
        >>> # Pull 100 messages, just the raw bytes
        >>> df = DataFrame.from_stream_source(source, n=100)
        >>> # Pull with full metadata
        >>> df = DataFrame.from_stream_source(source, n=100, include_metadata=True)
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="from_stream_source",
            source=source,
            n=n,
            timeout_ms=timeout_ms,
            include_metadata=include_metadata,
        )

    @classmethod
    def from_pandas(cls, data: typing.Any) -> "LazyFramePlaceholder":
        """Construct a DataFrame from a pandas DataFrame.

        Parameters
        ----------
        data
            pandas DataFrame to convert.

        Returns
        -------
        LazyFramePlaceholder backed by the provided pandas data.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="from_pandas",
            data=data,
        )

    @classmethod
    def from_python_udf(
        cls,
        udf: typing.Any,
        schema: pyarrow.Schema,
        *,
        output_timeout: float = 300.0,
    ) -> "LazyFramePlaceholder":
        """Create a DataFrame from a Python async generator function.

        Parameters
        ----------
        udf
            An async generator function that yields data batches.
        schema
            The expected PyArrow schema for the output data.
        output_timeout
            Maximum time in seconds to wait for the output handler. Default is 300 seconds.

        Returns
        -------
        LazyFramePlaceholder representing the UDF source.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="from_python_udf",
            udf=udf,
            schema=schema,
            output_timeout=output_timeout,
        )

    @classmethod
    def from_catalog_table(
        cls,
        table_name: str,
        *,
        catalog: typing.Any,
    ) -> "LazyFramePlaceholder":
        """Create a DataFrame from a Chalk SQL catalog table.

        Parameters
        ----------
        table_name
            Name of the table in the catalog.
        catalog
            ChalkSqlCatalog instance containing the table.

        Returns
        -------
        LazyFramePlaceholder referencing the catalog table.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="from_catalog_table",
            table_name=table_name,
            catalog=catalog,
        )

    @classmethod
    def from_datasource(
        cls, source: typing.Any, query: str, expected_output_schema: pyarrow.Schema
    ) -> "LazyFramePlaceholder":
        """Create a DataFrame from the result of querying a SQL data source.

        Parameters
        ----------
        source
            SQL source to query (e.g., PostgreSQL, Snowflake, BigQuery).
        query
            SQL query to execute against the data source.
        expected_output_schema
            Output schema of the query result.

        Returns
        -------
        LazyFramePlaceholder containing the query results from the data source.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="from_datasource",
            source=source,
            query=query,
            expected_output_schema=expected_output_schema,
        )

    @classmethod
    def scan_from_sql(
        cls,
        query: str,
        *,
        pool: typing.Any,
        output_uri_prefix: str,
        schema: pyarrow.Schema,
        dialect: str = "bigquery",
        external_location_prefix: str | None = None,
    ) -> "LazyFramePlaceholder":
        """Create a DataFrame by executing a SQL SELECT and scanning the resulting parquet files.

        Parameters
        ----------
        query
            A SELECT statement to execute against the data warehouse.
        pool
            A connection pool for the data warehouse.
        output_uri_prefix
            URI prefix where the exported parquet output will be written
            (e.g., ``gs://bucket/path/`` or ``s3://bucket/prefix/``). Alternatively, can be something that
            the SQL operation can unload to, such as a stage in Snowflake defined via CREATE STAGE.
        schema
            Arrow schema of the parquet files produced by the export.
        dialect
            SQL dialect for query rewriting (default ``"bigquery"``).
        external_location_prefix
            If `output_uri_prefix` is not an external location (ex: set to a Snowflake stage), this should specify the
            URI prefix where the exported parquet output will be written (e.g., ``gs://bucket/path/`` or
            ``s3://bucket/prefix/``). If None, will assume that output_uri_prefix is the URI prefix. Defaults to None.

        Returns
        -------
        LazyFramePlaceholder that reads the exported parquet files.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="scan_from_sql",
            query=query,
            pool=pool,
            output_uri_prefix=output_uri_prefix,
            schema=schema,
            dialect=dialect,
            external_location_prefix=external_location_prefix,
        )

    @classmethod
    def deserialize(cls, source: bytes, *, format: str = "binary") -> "LazyFramePlaceholder":
        """Deserialize bytes into a LazyFramePlaceholder.

        Parameters
        ----------
        source
            The serialized data.
        format
            Serialization format. Currently only ``"binary"`` is supported.

        Returns
        -------
        LazyFramePlaceholder backed by the deserialized data.
        """
        return LazyFramePlaceholder._construct(
            self_dataframe=None,
            function_name="deserialize",
            source=source,
            format=format,
        )

    def with_columns(
        self, *columns: typing.Mapping[str, Underscore | typing.Any] | Underscore | tuple[str, Underscore | typing.Any]
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

    def onnx_inference_udf(self, onnx_model_path: str) -> LazyFramePlaceholder:
        """Run ONNX model inference on this DataFrame.

        The DataFrame must contain a column for each model input (matching
        the names from :meth:`get_onnx_model_metadata`) plus a ``__cidx__``
        column. The returned DataFrame contains the model's output columns
        along with ``__cidx__`` and ``__valid__`` columns.

        Requires the ``chalkdf-onnx-runtime`` package to be installed.

        Parameters
        ----------
        onnx_model_path
            Filesystem path to a ``.onnx`` model file.

        Returns
        -------
        DataFrame
            A new DataFrame with the model's output columns, ``__cidx__``,
            and ``__valid__``.

        Raises
        ------
        RuntimeError
            If the ONNX module is not available or the model cannot be loaded.

        Examples
        --------
        >>> meta = DataFrame.get_onnx_model_metadata("model.onnx")
        >>> df = DataFrame.from_arrow(
        ...     pa.table({
        ...         meta["input_names"][0]: pa.array([[1.0] * 10], type=pa.list_(pa.float32())),
        ...         "__cidx__": [0],
        ...     })
        ... )
        >>> result = df.onnx_inference_udf(onnx_model_path="model.onnx").to_arrow()
        >>> result.column_names
        ['output', '__valid__', '__cidx__']
        """

        return LazyFramePlaceholder._construct(
            self_dataframe=self,
            function_name="onnx_inference_udf",
            onnx_model_path=onnx_model_path,
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
            Number of rows to include. If `None`, includes all remaining rows.

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

    def union_all(self, *others: "LazyFramePlaceholder") -> "LazyFramePlaceholder":
        """Combine this DataFrame with one or more others by stacking rows.

        All DataFrames must have the same schema (different column order is
         allowed - the output will have the same column order as ``self``).
        Duplicates **are** retained. Row order **is not** preserved.

        Parameters
        ----------
        *others
            One or more DataFrames to union with this DataFrame.

        Returns
        -------
        DataFrame with all rows from all input DataFrames.

        Raises
        ------
        ValueError
            If no other DataFrames are provided, or if schemas don't match.

        Examples
        --------
        >>> df1 = DataFrame({"x": [1, 2], "y": [10, 20]})
        >>> df2 = DataFrame({"x": [3, 4], "y": [30, 40]})
        >>> df3 = DataFrame({"x": [5], "y": [50]})
        >>> result = df1.union_all(df2, df3)
        >>> # result contains all 5 rows from df1, df2, and df3, in any order
        """

        return self._construct(self_dataframe=self, function_name="union_all", args=others)

    def union(self, other: "LazyFramePlaceholder") -> "LazyFramePlaceholder":
        """Combine this DataFrame with another by stacking rows.

        Convenience method for unioning with a single DataFrame.
        Equivalent to ``union_all(other)``.

        Both DataFrames must have the same schema (different column order is
        allowed - the output will have the same column order as ``self``).
        Duplicates **are** retained. Row order **is not** preserved.

        Parameters
        ----------
        other
            DataFrame to union with this DataFrame.

        Returns
        -------
        DataFrame with all rows from both input DataFrames.

        Raises
        ------
        ValueError
            If schemas don't match.

        Examples
        --------
        >>> df1 = DataFrame({"x": [1, 2], "y": [10, 20]})
        >>> df2 = DataFrame({"x": [3, 4], "y": [30, 40]})
        >>> result = df1.union(df2)
        >>> # result contains all 4 rows from df1 and df2, in any order

        See Also
        --------
        union_all : Union with multiple DataFrames at once.
        """

        return self._construct(self_dataframe=self, function_name="union", args=(other,))

    def project(self, columns: typing.Mapping[str, Underscore | typing.Any]) -> "LazyFramePlaceholder":
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
            If `True`, raise an error if any column doesn't exist. If `False`,
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
            If `True`, raise an error if any column doesn't exist. If `False`,
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
        probe_with_right_side: bool = False,
        where: Underscore | None = None,
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
            - If `None`, must specify ``left_on`` and ``right_on`` separately.
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
        probe_with_right_side
            If True, the probe side of the join will be the right and the build will be the left.
            Default is False (left is probe, right is build)

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
            - If `None`, can specify ``left_by`` and ``right_by`` separately.
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

    def window(
        self,
        by: typing.Sequence[str | Underscore],
        order_by: typing.Sequence[str | Underscore | tuple[str | Underscore, str]],
        *expressions: typing.Any,
    ) -> "LazyFramePlaceholder":
        """Compute window (analytic) expressions partitioned by ``by`` and ordered by ``order_by``.

        Parameters
        ----------
        by
            Column names that define the partition boundaries.
        order_by
            Column names (or ``(name, direction)`` tuples) that define the sort
            order within each partition.
        *expressions
            One or more WindowExpr objects that specify the analytic computation.

        Returns
        -------
        LazyFramePlaceholder with the window-expression output columns added.
        """
        return self._construct(
            self_dataframe=self,
            function_name="window",
            by=by,
            order_by=order_by,
            args=expressions,
        )

    def group_by(self, *by: str | Underscore):
        """Create a GroupBy object for chained aggregation operations.

        This method returns a GroupBy object that can be used to apply
        aggregation expressions via the `.agg()` method. This provides
        an alternative syntax to `df.agg(by, *aggregations)`.

        Parameters
        ----------
        *by
            Column names to group by. Can be strings or underscore expressions.

        Returns
        -------
        GroupBy object that can be used to apply aggregations via `.agg()`.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> from chalk.features import _
        >>> df = DataFrame.from_dict({"group": ["A", "A", "B"], "value": [1, 2, 3]})
        >>> grouped = df.group_by("group").agg(_.value.sum().alias("total"))

        Multiple grouping columns:
        >>> df2 = DataFrame.from_dict({"g1": ["A", "A", "B"], "g2": ["X", "Y", "X"], "val": [1, 2, 3]})
        >>> result = df2.group_by("g1", "g2").agg(_.val.sum().alias("sum"))

        Using underscore expressions:
        >>> result = df.group_by(_.group).agg(_.value.mean().alias("avg"))
        """
        return _LazyFrameGroupBy(_lf=self, _by=by)

    def rollup(
        self,
        *by: str | Underscore,
        grouping_id_col: str | None = None,
    ) -> _LazyFrameGroupingSetsGroupBy:
        """Multi-set aggregation matching SQL ``GROUP BY ROLLUP(b1, b2, ...)``.

        Expands to every prefix of ``by`` plus the empty (grand-total) set.

        Parameters
        ----------
        *by
            Columns to roll up. Must be non-empty.
        grouping_id_col
            Name for the discriminator column identifying which grouping
            set produced each row. Defaults to ``__chalk_grouping_set_id__``.

        Returns
        -------
        A handle whose ``.agg(...)`` materializes the rollup.
        """
        return _LazyFrameGroupingSetsGroupBy(
            _lf=self,
            _function_name="rollup",
            _args=by,
            _kwargs={"grouping_id_col": grouping_id_col},
        )

    def cube(
        self,
        *by: str | Underscore,
        grouping_id_col: str | None = None,
    ) -> _LazyFrameGroupingSetsGroupBy:
        """Multi-set aggregation matching SQL ``GROUP BY CUBE(b1, b2, ...)``.

        Expands to all ``2^N`` subsets of ``by``.

        Parameters
        ----------
        *by
            Columns to cube. Must be non-empty.
        grouping_id_col
            Name for the discriminator column identifying which grouping
            set produced each row. Defaults to ``__chalk_grouping_set_id__``.

        Returns
        -------
        A handle whose ``.agg(...)`` materializes the cube.
        """
        return _LazyFrameGroupingSetsGroupBy(
            _lf=self,
            _function_name="cube",
            _args=by,
            _kwargs={"grouping_id_col": grouping_id_col},
        )

    def grouping_sets(
        self,
        sets: typing.Sequence[typing.Sequence[str | Underscore]],
        grouping_id_col: str | None = None,
    ) -> _LazyFrameGroupingSetsGroupBy:
        """Multi-set aggregation matching SQL ``GROUP BY GROUPING SETS (...)``.

        Each inner sequence is a grouping set; the empty inner sequence
        denotes the grand-total ``()`` set.

        Parameters
        ----------
        sets
            Sequence of grouping sets.
        grouping_id_col
            Name for the discriminator column identifying which grouping
            set produced each row. Defaults to ``__chalk_grouping_set_id__``.

        Returns
        -------
        A handle whose ``.agg(...)`` materializes the multi-set aggregation.
        """
        return _LazyFrameGroupingSetsGroupBy(
            _lf=self,
            _function_name="grouping_sets",
            _args=(sets,),
            _kwargs={"grouping_id_col": grouping_id_col},
        )

    def agg(
        self,
        by: typing.Sequence[str | Underscore],
        *aggregations: Underscore,
        pre_grouped_keys: typing.Sequence[str] = (),
    ) -> "LazyFramePlaceholder":
        """Group by columns and apply aggregation expressions.

        Parameters
        ----------
        by
            Column names to group by.
        *aggregations
            Aggregation expressions to apply to each group (e.g., sum, count, mean).
        pre_grouped_keys
            Optional caller assertion that the input is already grouped by these
            keys. Mirrors ``DataFrame.agg``; recorded so it round-trips to the
            real ``DataFrame.agg`` on replay. ``DataFrame.group_by(...).agg(...)``
            always forwards this kwarg, so it must be accepted here for the
            ``run(remote=True)`` lazy recording to serialize the plan.

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
            pre_grouped_keys=list(pre_grouped_keys),
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

    def fill_null(self, value: object | dict[str, object]) -> "LazyFramePlaceholder":
        """Replace null values with a fill value.

        Parameters
        ----------
        value
            Either a scalar value to fill all nulls across every column,
            or a dict mapping column names to per-column fill values.

        Returns
        -------
        LazyFramePlaceholder with nulls replaced by the specified fill value(s).
        """
        return self._construct(
            self_dataframe=self,
            function_name="fill_null",
            value=value,
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
        return_table_write_result: bool = False,
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
        return_table_write_result
            If True, return the raw TableWrite result (default False).

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
            return_table_write_result=return_table_write_result,
        )

    def write_lazy(
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
            function_name="write_lazy",
            target_path=target_path,
            target_file_name=target_file_name,
            file_format=file_format,
            serde_parameters=serde_parameters,
            compression=compression,
            ensure_files=ensure_files,
            connector_id=connector_id,
        )

    def write_parquet(
        self,
        output_uri_prefix: str,
        skip_planning_time_validation: bool = False,
        return_table_write_result: bool = False,
    ) -> "LazyFramePlaceholder":
        """Write the DataFrame as Parquet files using an auto-configured connector.

        This is a convenience method that simplifies writing Parquet files compared
        to the more general ``write()`` method. It automatically configures the
        appropriate connector based on the URI prefix.

        Parameters
        ----------
        output_uri_prefix
            URI prefix where Parquet files will be written. Examples:
            - ``"file:///path/to/dir/"`` for local filesystem
            - ``"s3://bucket/prefix/"`` for S3
            - ``"gs://bucket/prefix/"`` for Google Cloud Storage
        skip_planning_time_validation
            Whether to skip validation at planning time (default: False).
        return_table_write_result
            If True, return the raw TableWrite result (default False).

        Returns
        -------
        DataFrame representing the TableWrite operator.

        Examples
        --------
        >>> from chalkdf import DataFrame
        >>> df = DataFrame.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        >>> # Write to local filesystem
        >>> write_df = df.write_parquet("file:///tmp/output/")
        """

        return self._construct(
            self_dataframe=self,
            function_name="write_parquet",
            output_uri_prefix=output_uri_prefix,
            skip_planning_time_validation=skip_planning_time_validation,
            return_table_write_result=return_table_write_result,
        )

    def write_parquet_and_load(
        self,
        output_uri_prefix: str,
        destination: typing.Any,
        loader: typing.Any,
        skip_planning_time_validation: bool = False,
        return_table_write_result: bool = False,
    ) -> "LazyFramePlaceholder":
        """Write the DataFrame as Parquet files and load into a data warehouse.

        Parameters
        ----------
        output_uri_prefix
            URI prefix where Parquet files will be written.
        destination
            Target data warehouse destination (database, schema, table).
        loader
            A DataWarehouseLoader implementation that performs the load.
        skip_planning_time_validation
            Whether to skip validation at planning time (default: False).
        return_table_write_result
            If True, return the raw TableWrite result (default False).

        Returns
        -------
        LazyFramePlaceholder representing the TableWriteAndLoad operator.
        """
        return self._construct(
            self_dataframe=self,
            function_name="write_parquet_and_load",
            output_uri_prefix=output_uri_prefix,
            destination=destination,
            loader=loader,
            skip_planning_time_validation=skip_planning_time_validation,
            return_table_write_result=return_table_write_result,
        )

    def write_to(self, config: "Mapping[str, Any] | WriteConfigLike") -> "LazyFramePlaceholder":
        """Record a write to a typed destination config on this lazy plan.

        The chalkdf-side ``DataFrame.write_to`` records a recording-only entry
        on the lazy frame so the resulting ``DataFramePlan`` proto carries the
        intent (destination + per-call config) across the wire. Runtime
        resolution of the destination — looking up the live writer against the
        active ``BindingRegistry`` — happens later, at libchalk plan compile
        time, via the ``BindNodeResources`` rewriter.

        ``config`` is a chalkdf ``WriteConfig`` (e.g. ``KeyValueOnlineStoreConfig``,
        ``VectorStoreConfig``, ``SnowflakeWarehouseConfig``). It owns its serialized
        form: ``config.to_wire()`` returns a ``kind``-tagged mapping of
        proto-friendly primitives, which is what gets recorded. On replay the
        recorder hands the mapping back (as a plain ``dict``) and
        ``DataFrame.write_to`` rebuilds the typed config. Runtime handles must not
        appear in the wire mapping; they cannot be encoded as proto operands.

        ``config`` is typed structurally -- a ``Mapping`` (the replay wire form) or
        any object exposing ``to_wire`` -- because the concrete ``WriteConfig`` types
        live in chalkdf, which chalkpy does not depend on.

        Parameters
        ----------
        config
            A chalkdf ``WriteConfig`` on the recording path, or its ``to_wire``
            mapping (a ``dict``) on the replay path.

        Returns
        -------
        LazyFramePlaceholder with the ``write_to`` op appended.
        """
        # ``config`` is a WriteConfig when recording and the wire mapping itself
        # when replaying (the recorder round-trips primitives, not objects);
        # normalize to the wire form either way.
        wire = config if isinstance(config, Mapping) else config.to_wire()
        return self._construct(
            self_dataframe=self,
            function_name="write_to",
            config=wire,
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

    def head(self, n: int = 5) -> "LazyFramePlaceholder":
        """Return the first *n* rows.

        Parameters
        ----------
        n
            Number of rows to return. Defaults to ``5``.
        """
        return self._construct(
            self_dataframe=self,
            function_name="head",
            n=n,
        )

    def tail(self, n: int = 5) -> "LazyFramePlaceholder":
        """Return the last *n* rows.

        Parameters
        ----------
        n
            Number of rows to return. Defaults to ``5``.
        """
        return self._construct(
            self_dataframe=self,
            function_name="tail",
            n=n,
        )

    def iter_rows(self, *, named: bool = False) -> typing.Any:
        """Iterate over rows, yielding tuples or dicts.

        Parameters
        ----------
        named
            If ``True``, yield ``dict`` objects; otherwise tuples.
        """
        return self._construct(
            self_dataframe=self,
            function_name="iter_rows",
            named=named,
        )

    def iter_columns(self) -> typing.Any:
        """Iterate over columns, yielding Series objects."""
        return self._construct(
            self_dataframe=self,
            function_name="iter_columns",
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

    def _serialize_sql_source_reference(value: Any) -> dataframe_pb2.DataFrameDataSource:
        from chalk.parsed.to_proto import ToProtoConverter
        from chalk.sql._internal.sql_source import BaseSQLSource  # pyright: ignore[reportPrivateUsage]

        if not isinstance(value, BaseSQLSource):
            raise ValueError(f"LazyFramePlaceholder.from_datasource source must be a SQL datasource, got {type(value)}")

        return dataframe_pb2.DataFrameDataSource(
            database_source=ToProtoConverter.convert_sql_source(value),
        )

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

        args = list(df_constructor.args)
        kwargs = dict(df_constructor.kwargs)
        if df_constructor.function_name == "from_datasource":
            if "source" in kwargs:
                kwargs["source"] = _serialize_sql_source_reference(kwargs["source"])
            elif args:
                args[0] = _serialize_sql_source_reference(args[0])

        proto_args = dataframe_pb2.PyList(
            list_items=[_convert_arg(arg_value) for arg_value in args],
        )
        proto_kwargs = dataframe_pb2.PyDict(
            dict_entries=[
                dataframe_pb2.PyDictEntry(
                    entry_key=_convert_arg(kwarg_name),
                    entry_value=_convert_arg(kwarg_value),
                )
                for kwarg_name, kwarg_value in kwargs.items()
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
        if isinstance(value, bool):
            return dataframe_pb2.DataFrameOperand(
                value_bool=value,
            )
        if isinstance(value, int):
            return dataframe_pb2.DataFrameOperand(
                value_int=value,
            )
        if isinstance(value, str):
            return dataframe_pb2.DataFrameOperand(
                value_string=value,
            )
        if isinstance(value, dataframe_pb2.DataFrameDataSource):
            return dataframe_pb2.DataFrameOperand(
                data_source=value,
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

    def _construct_sql_source(kind: str, kwargs: dict[str, Any]) -> Any:
        import chalk.sql as chalk_sql

        constructors = {
            "athena": chalk_sql.AthenaSource,
            "bigquery": chalk_sql.BigQuerySource,
            "clickhouse": chalk_sql.ClickhouseSource,
            "cloudsql": chalk_sql.CloudSQLSource,
            "databricks": chalk_sql.DatabricksSource,
            "dynamodb": chalk_sql.DynamoDBSource,
            "mssql": chalk_sql.MSSQLSource,
            "mysql": chalk_sql.MySQLSource,
            "postgres": chalk_sql.PostgreSQLSource,
            "postgresql": chalk_sql.PostgreSQLSource,
            "redshift": chalk_sql.RedshiftSource,
            "snowflake": chalk_sql.SnowflakeSource,
            "spanner": chalk_sql.SpannerSource,
            "trino": chalk_sql.TrinoSource,
        }
        kwargs = dict(kwargs)
        if kind == "sqlite":
            filename = kwargs.pop("filename", None)
            constructor = chalk_sql.SQLiteFileSource if filename is not None else chalk_sql.SQLiteInMemorySource
            if filename is not None:
                kwargs = {"filename": filename, **kwargs}
        else:
            constructor = constructors.get(kind)
        if constructor is None:
            raise ValueError(f"Unsupported serialized SQL datasource kind: {kind}")

        return constructor(**kwargs)

    def _deserialize_sql_source_reference(value: Any) -> Any:
        kind = value.database_source.source_type
        if not kind:
            raise ValueError(f"Serialized SQL datasource is missing a valid source type: {value!r}")
        kwargs = {}
        if value.database_source.name:
            kwargs["name"] = value.database_source.name
        return _construct_sql_source(kind, kwargs)

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
        if value.HasField("data_source"):
            return _deserialize_sql_source_reference(value.data_source)

        raise ValueError(f"DataFrame operand expression {value} does not have any value set")

    for df in proto_plan.constructors:
        df_values.append(_convert_dataframe(df))

    if len(df_values) == 0:
        raise ValueError(
            "Could not parse LazyFramePlaceholder from proto expression; no dataframe constructors were present in the provided proto message"
        )

    return df_values[-1]
