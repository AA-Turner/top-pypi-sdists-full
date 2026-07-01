from __future__ import annotations

import typing as t
from collections import defaultdict
from datetime import datetime, timezone
from sqlglot import exp
from dbt_state.adapters.base import BaseAdapterExtension
from dbt_state import events
from dbt_state.adapters.common import (
    ViewFetchResult,
    build_information_schema_filter,
    ViewDefinition,
    group_tables_by_catalog,
)
from dbt_state.utils import find_tables
from query_cache_common.utils import extract_fqn_parts

try:
    from dbt.adapters.contracts.relation import RelationType
except ImportError:
    from dbt.adapters.base.relation import RelationType


def contains_unqualified_table_references(query: exp.Expr) -> bool:
    """Test if the input query contains unqualified table references

    For example, a direct reference to "foo" with no context vs a reference to "catalog"."schema"."foo"
    """
    for table in find_tables(query):
        if not table.catalog or not table.db:
            return True

    return False


class DatabricksAdapterExtension(BaseAdapterExtension):
    CLONE_CHAIN_DEPTH_LIMIT = 1

    def current_timestamp_utc(self) -> datetime:
        epoch_micros = self.execute(
            "SELECT unix_micros(current_timestamp())",
            fetch=True,
        ).rows[0][0]
        return datetime.fromtimestamp(int(epoch_micros) / 1_000_000, tz=timezone.utc)

    def _fetch_last_modified_epochs(
        self, table_batch: t.Collection[exp.Table]
    ) -> t.Dict[str, t.Optional[int]]:
        if not table_batch:
            return {}

        # _batch_table_names produces homogeneous batches: either a single table
        # (for DESCRIBE DETAIL) or a group of views (for information_schema).
        # We detect which kind of batch this is by checking the first relation.
        table_exprs = [self._to_fqn(t) for t in table_batch]
        fqns_to_exprs = {t.sql(dialect=self.dialect): t for t in table_exprs}
        first_relation = self.adapter.get_relation(
            database=table_exprs[0].catalog,
            schema=table_exprs[0].db,
            identifier=table_exprs[0].name,
        )

        if first_relation is None:
            return {fqn: None for fqn in fqns_to_exprs}

        if first_relation.type == RelationType.View:
            return self._fetch_view_last_modified_epochs(fqns_to_exprs)

        # DESCRIBE DETAIL is a standalone statement (can't be used as a subquery),
        # so we execute it directly. Each table arrives in its own batch from
        # _batch_table_names, so this runs once per table in parallel.
        # note: we can't use the last_altered column from information_schema.tables for tables because
        # it only shows when the table *schema* was last altered, not the data in the table
        # ref: https://kb.databricks.com/unity-catalog/last_altered-column-in-information_schema-not-reflecting-data-modifications
        assert len(fqns_to_exprs) == 1, "Expected exactly one table in batch for DESCRIBE DETAIL"
        return self._fetch_table_last_modified_epoch(next(iter(fqns_to_exprs)))

    def _fetch_table_last_modified_epoch(self, fqn: str) -> t.Dict[str, t.Optional[int]]:
        detail_result = self.execute(f"DESCRIBE DETAIL {fqn}", fetch=True)
        if detail_result.rows:
            col_index = {name: i for i, name in enumerate(detail_result.column_names)}
            last_modified = detail_result.rows[0][col_index["lastModified"]]
            if last_modified is not None:
                return {fqn: int(last_modified.replace(tzinfo=timezone.utc).timestamp() * 1000)}
        return {fqn: None}

    def _fetch_view_last_modified_epochs(
        self, fqns_to_exprs: t.Dict[str, exp.Table]
    ) -> t.Dict[str, t.Optional[int]]:
        if not fqns_to_exprs:
            return {}
        # last_altered from information_schema.tables reflects schema changes,
        # which is exactly what matters for views
        subqueries = []
        for catalog, tables in group_tables_by_catalog(
            fqns_to_exprs.values(), self.default_catalog
        ).items():
            filter_expr = build_information_schema_filter(
                tables, ("table_catalog", "table_schema", "table_name")
            )
            subqueries.append(
                f"""
                SELECT
                  concat('`', table_catalog, '`.`', table_schema, '`.`', table_name, '`') as fqn,
                  last_altered as last_updated
                FROM {catalog}.information_schema.tables
                WHERE {self._sql(filter_expr)}"""
            )

        main_cte = "union all\n".join(subqueries)
        rows = self.execute(
            f"""
        with tables as (
            {main_cte}
        )
        select fqn, unix_millis(last_updated) as last_modified_epoch
        from tables
        order by fqn
        """,
            fetch=True,
        ).rows
        timestamps = {fqn: epoch for fqn, epoch in rows}
        return {fqn: timestamps.get(fqn) for fqn in fqns_to_exprs}

    def _batch_table_names(
        self, tables: t.Collection[exp.Table]
    ) -> t.Collection[t.Collection[exp.Table]]:
        # Tables and views require different fetching strategies for last modified timestamps:
        #  - Tables use DESCRIBE DETAIL, a standalone statement that only works on one table
        #    at a time, so each table gets its own batch to be parallelized by the executor.
        #  - Views use information_schema.tables (last_altered), which supports efficient
        #    batch queries, so all views in the same catalog are grouped into a single batch.
        batches: t.List[t.List[exp.Table]] = []
        views_by_catalog: t.Dict[str, t.List[exp.Table]] = defaultdict(list)

        for table in tables:
            fqn = self._to_fqn(table)
            relation = self.adapter.get_relation(
                database=fqn.catalog, schema=fqn.db, identifier=fqn.name
            )
            if relation is not None and relation.type == RelationType.View:
                catalog = fqn.catalog or self.default_catalog
                views_by_catalog[catalog].append(table)
            else:
                batches.append([table])

        for catalog_views in views_by_catalog.values():
            batches.append(catalog_views)

        return batches

    def _fetch_view_definitions(self, table_batch: t.Collection[exp.Table]) -> ViewFetchResult:
        if not table_batch:
            return ViewFetchResult(definitions=[])

        queries = []
        for catalog, tables in group_tables_by_catalog(table_batch, self.default_catalog).items():
            filter_expr = build_information_schema_filter(
                tables, ("table_catalog", "table_schema", "table_name")
            )
            query = f"""
            SELECT
            table_catalog,
            table_schema,
            table_name as view_name,
            view_definition
            FROM {catalog}.information_schema.views
            WHERE {self._sql(filter_expr)}
            """

            queries.append(query)

        query = "UNION ALL\n".join(queries)

        view_definitions = []
        result_rows = self.execute(query, fetch=True).rows

        for catalog, schema, name, view_definition in result_rows:
            fqn = self._build_fqn_from_row(catalog, schema, name)
            catalog, schema, _ = extract_fqn_parts(fqn, dialect=self.dialect)
            view_definition = ViewDefinition(
                fqn=fqn,
                definition=view_definition,
                dialect=self.dialect,
                default_catalog=catalog,
                default_schema=schema,
            )

            # note: by default, dbt-databricks injects fully qualified references
            # so this extra fetch will only occur when encountering view definitions created outside dbt-databricks
            # that dont contain fully qualified references
            if contains_unqualified_table_references(view_definition.parsed()):
                catalog, schema = self._fetch_view_catalog_and_namespace(fqn)
                view_definition.default_catalog = catalog
                view_definition.default_schema = schema

            view_definitions.append(view_definition)

        return ViewFetchResult(definitions=view_definitions)

    def _fetch_view_catalog_and_namespace(self, fqn: str) -> t.Tuple[str, str]:
        try:
            result = self.execute(f"describe extended {fqn}", fetch=True)
            for col_name, data_type, _ in result.rows:
                if col_name == "View Catalog and Namespace":
                    tbl = exp.to_table(data_type, dialect=self.dialect)
                    return self._sql(tbl.args["db"]), self._sql(tbl.args["this"])
        except Exception as e:
            events.fire_debug_event(
                "Unable to fetch view catalog and namespace for {}: {}", fqn, str(e)
            )

        # fall back to using the catalog / schema on the view fqn itself which is more likely to be correct
        # than the default catalog / schema configured on the connection
        catalog, schema, _ = extract_fqn_parts(fqn, dialect=self.dialect)
        return catalog, schema
