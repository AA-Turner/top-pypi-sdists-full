#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Push static Hive partition filters into stage listing (SNOW-3295586)."""
from __future__ import annotations

from collections.abc import Callable

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark.types import StructType
from snowflake.snowpark_connect.config import (
    global_config,
    is_hive_partition_pruning_enabled,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.read.partition_pruning import (
    HivePartitionPruningHint,
    build_pruned_clean_source_paths,
    extract_leading_partition_predicates,
    reset_hive_partition_pruning_hint,
    set_hive_partition_pruning_hint,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_PRUNING_READ_FORMATS = frozenset({"csv", "json", "parquet", "text"})


def _read_has_user_path_glob(read_rel: relation_proto.Relation) -> bool:
    options = dict(read_rel.read.data_source.options)
    lowered = {k.lower(): v for k, v in options.items()}
    return bool(lowered.get("pathglobfilter") or lowered.get("pattern"))


def _read_format_from_relation(read_rel: relation_proto.Relation) -> str | None:
    if not read_rel.read.data_source.HasField("format"):
        return None
    return read_rel.read.data_source.format.lower()


def _with_pruned_dataframe(
    read_container: DataFrameContainer,
    result_df: snowpark.DataFrame,
    schema_getter: Callable[[], StructType],
) -> DataFrameContainer:
    """Build a filtered container preserving read-side metadata from ``read_container``."""
    return DataFrameContainer(
        result_df,
        read_container.column_map,
        read_container.table_name,
        read_container.alias,
        cached_schema_getter=schema_getter,
        partition_hint=read_container.partition_hint,
        dataframe_hint=read_container._dataframe_hint,
        can_be_cached=read_container.can_be_cached,
        can_be_materialized=read_container.can_be_materialized,
        aggregate_metadata=read_container._aggregate_metadata,
        cached_local_relation_arrow_table=read_container.cached_local_relation_arrow_table,
    )


class _FilterOverHivePartitionedRead:
    name = "FilterOverHivePartitionedRead"
    rel_type = "filter"

    def applies_to(self, rel: relation_proto.Relation) -> bool:
        if not is_hive_partition_pruning_enabled():
            return False
        if rel.filter.input.WhichOneof("rel_type") != "read":
            return False
        read_rel = rel.filter.input
        if read_rel.read.WhichOneof("read_type") != "data_source":
            return False
        if not read_rel.read.data_source.paths:
            return False
        read_format = _read_format_from_relation(read_rel)
        if read_format not in _PRUNING_READ_FORMATS:
            return False
        return not _read_has_user_path_glob(read_rel)

    def apply(self, rel: relation_proto.Relation) -> DataFrameContainer | None:
        from snowflake.snowpark_connect.expression.map_expression import (
            map_single_column_expression,
        )
        from snowflake.snowpark_connect.expression.typer import ExpressionTyper
        from snowflake.snowpark_connect.relation.read.map_read import (
            _normalize_read_source_path,
            _quote_stage_path,
            _read_file_from_data_source,
        )
        from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
            _discover_partition_columns,
            use_external_table,
        )
        from snowflake.snowpark_connect.relation.read.path_anchoring import (
            classify_source_path,
        )
        from snowflake.snowpark_connect.relation.stage_locator import (
            get_paths_from_stage,
        )
        from snowflake.snowpark_connect.utils.session import (
            get_or_create_snowpark_session,
        )

        read_rel = rel.filter.input
        read_format = _read_format_from_relation(read_rel)
        if read_format is None:
            return None

        options = dict(read_rel.read.data_source.options)
        session = get_or_create_snowpark_session()
        clean_source_paths = [
            _normalize_read_source_path(path)
            for path in read_rel.read.data_source.paths
        ]
        stage_paths = get_paths_from_stage(clean_source_paths, session)
        if not stage_paths:
            return None

        discovery_path = stage_paths[0]
        classification = classify_source_path(clean_source_paths[0])
        if classification.kind == "dir" and not discovery_path.endswith("/"):
            discovery_path += "/"
        quoted_discovery_path = _quote_stage_path(discovery_path)

        if use_external_table(session, quoted_discovery_path):
            return None

        partition_columns, _ = _discover_partition_columns(
            session,
            quoted_discovery_path,
            read_format,  # type: ignore[arg-type]
        )
        if not partition_columns:
            return None

        predicates = extract_leading_partition_predicates(
            rel.filter.condition,
            partition_columns,
            case_sensitive=global_config.spark_sql_caseSensitive,
        )
        if not predicates:
            return None

        pruned_paths = build_pruned_clean_source_paths(
            clean_source_paths, partition_columns, predicates
        )
        if pruned_paths == clean_source_paths:
            return None

        logger.debug(
            "Hive partition pruning: %d path(s) -> %d path(s) for columns %s",
            len(clean_source_paths),
            len(pruned_paths),
            list(predicates),
        )

        hint = HivePartitionPruningHint(pruned_clean_source_paths=tuple(pruned_paths))
        token = set_hive_partition_pruning_hint(hint)
        try:
            read_container = _read_file_from_data_source(
                read_rel, session, clean_source_paths, options, read_format
            )
        finally:
            reset_hive_partition_pruning_hint(token)

        typer = ExpressionTyper(read_container.dataframe)
        _, condition = map_single_column_expression(
            rel.filter.condition, read_container.column_map, typer
        )
        result_df = read_container.dataframe.filter(condition.col)
        return _with_pruned_dataframe(
            read_container,
            result_df,
            lambda: read_container.dataframe.schema,
        )


filter_over_hive_partitioned_read = _FilterOverHivePartitionedRead()
