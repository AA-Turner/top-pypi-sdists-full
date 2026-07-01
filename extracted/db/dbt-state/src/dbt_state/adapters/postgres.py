from __future__ import annotations

import typing as t
from datetime import datetime, timezone

try:
    from dbt_common.exceptions import DbtDatabaseError
except ImportError:
    from dbt.exceptions import DbtDatabaseError  # type: ignore

from sqlglot import exp

from dbt_state import events
from dbt_state.adapters.base import BaseAdapterExtension
from dbt_state.adapters.common import (
    ViewFetchResult,
    build_information_schema_filter,
    ViewDefinition,
)
from dbt_state.errors import AdapterExtensionError


class PostgresAdapterExtension(BaseAdapterExtension):
    DEFAULT_SCHEMA_NAME = "public"
    SHOULD_RELEASE_CONNECTION: bool = True

    @property
    def supports_view_last_modified(self) -> bool:
        return False

    def current_timestamp_utc(self) -> datetime:
        epoch_micros = self.execute(
            "SELECT CAST(EXTRACT(EPOCH FROM clock_timestamp()) * 1000000 AS BIGINT)",
            fetch=True,
        ).rows[0][0]
        return datetime.fromtimestamp(int(epoch_micros) / 1_000_000, tz=timezone.utc)

    def rollback(self) -> None:
        """Roll back the current transaction for PostgreSQL.

        PostgreSQL uses implicit transactions, so we need to rollback directly
        on the connection handle rather than checking transaction_open flag.
        """
        conn = self.adapter.connections.get_if_exists()
        if conn is not None and conn.handle:
            try:
                conn.handle.rollback()
            except Exception as e:
                events.fire_debug_event("Failed to rollback PostgreSQL connection: {}", str(e))

    def _fetch_last_modified_epochs(
        self, table_batch: t.Collection[exp.Table]
    ) -> dict[str, t.Optional[int]]:
        if not table_batch:
            return {}

        table_fqns = [self._to_fqn(t) for t in table_batch]

        last_modified_epochs: dict[str, t.Optional[int]] = {}
        for table in table_fqns:
            query = (
                exp.select(
                    "CAST(EXTRACT(EPOCH FROM pg_xact_commit_timestamp(t.xmin)) * 1000 AS BIGINT) AS last_modified_epoch"
                )
                .from_(table.as_("t"))
                .order_by("last_modified_epoch DESC NULLS LAST")
                .limit(1)
            )
            try:
                agate_table = self.execute(query, fetch=True)
                if len(agate_table) > 1:
                    raise AdapterExtensionError("Found more than one result")
                if len(agate_table) == 1:
                    last_modified_epochs[self._sql(table)] = int(
                        agate_table[0]["last_modified_epoch"]
                    )
                else:
                    # no rows indicates that the table exists but has no data in it
                    last_modified_epochs[self._sql(table)] = None
            except DbtDatabaseError as e:
                if "does not exist" in str(e):
                    self.rollback()
                    last_modified_epochs[self._sql(table)] = None
                else:
                    raise e

        return last_modified_epochs

    def _fetch_view_definitions(self, table_batch: t.Collection[exp.Table]) -> ViewFetchResult:
        if not table_batch:
            return ViewFetchResult(definitions=[])

        view_definitions = []

        filter_expr = build_information_schema_filter(table_batch, ("schemaname", "viewname"))
        query = f"""
        SELECT
            schemaname,
            viewname,
            definition
        FROM pg_views
        WHERE {self._sql(filter_expr)}
        """

        result_rows = self.execute(query, fetch=True).rows

        for schema, name, view_definition in result_rows:
            catalog = self.default_catalog

            fqn = self._build_fqn_from_row(catalog, schema, name)
            view_definitions.append(
                ViewDefinition(
                    fqn=fqn,
                    definition=view_definition,
                    dialect=self.dialect,
                    default_catalog=catalog,
                    # TODO: this is wrong, theoretically every single view dependency could have a different schema
                    # depending on how they resolved via search_path when the view was created
                    # this info can be fetched by querying `pg_depend` and friends
                    default_schema=self.DEFAULT_SCHEMA_NAME,
                )
            )

        return ViewFetchResult(definitions=view_definitions)
