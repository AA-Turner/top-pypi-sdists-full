from __future__ import annotations

import threading
import time
import typing as t
from collections import defaultdict
from concurrent.futures import Future
from dataclasses import replace
from datetime import datetime, timezone
from functools import cached_property
from multiprocessing import get_context

from dbt.adapters.sql import SQLAdapter
from sqlglot import TokenType, exp, tokenize
from sqlglot.dialects.dialect import Dialect
from typing_extensions import override

from dbt_state import events
from dbt_state.adapters.base import BaseAdapterExtension
from dbt_state.adapters.common import (
    ViewDefinition,
    ViewFetchResult,
    build_information_schema_filter,
    group_tables_by_catalog,
)
from dbt_state.utils import set_invocation_context


class RedshiftAdapterExtension(BaseAdapterExtension):
    DEFAULT_SCHEMA_NAME = "public"
    SHOULD_RELEASE_CONNECTION: bool = True
    SYSTEM_METADATA_SCHEMAS: t.ClassVar[t.List[str]] = ["information_schema", "pg_catalog"]
    IMPLEMENTS_CUSTOM_CLONE: bool = True

    _SYS_QUERY_DETAIL_LOOKBACK_MINUTES = 30
    _CASE_SENSITIVE_NORMALIZATION_DIALECT: t.ClassVar[Dialect] = Dialect.get_or_raise(
        "redshift, normalization_strategy = case_sensitive"
    )

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self._catalog_adapters: t.Dict[str, SQLAdapter] = {}

    @property
    def supports_view_last_modified(self) -> bool:
        return False

    @property
    def use_heuristic_clock_for_last_modified(self) -> bool:
        return True

    @cached_property
    def case_sensitivity_enabled(self) -> bool:
        try:
            result = self.execute(
                "SELECT CURRENT_SETTING('enable_case_sensitive_identifier')", fetch=True
            )
            return result.rows[0][0].strip().lower() == "on"
        except Exception as e:
            events.fire_debug_event(
                "Failed to retrieve enable_case_sensitive_identifier",
                str(e),
            )
            return False

    @cached_property
    def _datashare_catalogs(self) -> t.Set[str]:
        try:
            result = self.execute("SHOW DATABASES", fetch=True)
            return set(
                row["database_name"].lower()
                for row in result
                if row["database_type"].lower() == "shared"
            )
        except Exception as e:
            events.fire_debug_event("Failed to identify datashare catalogs. Error: {}", str(e))
            return set()

    def current_timestamp_utc(self) -> datetime:
        return (
            self.execute(
                "SELECT (SYSDATE AT TIME ZONE CURRENT_SETTING('timezone')) AT TIME ZONE 'UTC'",
                fetch=True,
            )
            .rows[0][0]
            .replace(tzinfo=timezone.utc)
        )

    def rollback(self) -> None:
        """Roll back the current transaction for Redshift.

        Redshift uses implicit transactions, so we need to rollback directly
        on the connection handle rather than checking transaction_open flag.
        """
        conn = self.adapter.connections.get_if_exists()
        if conn is not None and conn.handle:
            try:
                conn.handle.rollback()
            except Exception as e:
                events.fire_debug_event("Failed to rollback Redshift connection: {}", str(e))

    def prewarm_connections(self) -> None:
        """Eagerly acquire connections on every executor thread.

        The base class skips pre-warming when SHOULD_RELEASE_CONNECTION=True, but Redshift
        benefits from it: connections are acquired and then released back to dbt's pool.
        Subsequent connection_named() calls reuse pool connections regardless of name, so both
        SHOW TABLES and sys_query_detail threads benefit from pre-established connections.

        Only warms the default catalog. Non-default catalog adapters
        are created lazily and cannot be pre-warmed at this stage.
        """
        num_workers = self._max_workers
        barrier = threading.Barrier(num_workers)

        def _prewarm_connection(name: str) -> None:
            prewarm_start_time = time.perf_counter()
            try:
                self._ensure_thread_connection(name)
                self.execute("SELECT 1")
            finally:
                self._release_thread_connection()
                prewarm_end_time = time.perf_counter()
                try:
                    barrier.wait(timeout=self._CONNECTION_BARRIER_TIMEOUT_SECONDS)
                except threading.BrokenBarrierError:
                    pass
                events.fire_debug_event(
                    "Prewarming connection {} took {} seconds, waiting on other threads took {} seconds",
                    name,
                    prewarm_end_time - prewarm_start_time,
                    time.perf_counter() - prewarm_end_time,
                )

        for i in range(num_workers):
            self._executor.submit(_prewarm_connection, f"run_cache_prewarm_{i}")

    def clone(
        self,
        clone_sqls: t.Iterable[str],
        clone_source: str,
        clone_target: str,
    ) -> None:
        """Clone clone_source into clone_target preserving PRIMARY KEY and FOREIGN KEY.

        Uses SHOW TABLE to obtain the full DDL (including PK/FK constraints) then
        executes DROP + CREATE + INSERT in a single transaction. Falls back to the
        server-provided LIKE-based clone_sqls when SHOW TABLE is unavailable.
        """
        raw_ddl = self._show_table_ddl(clone_source)
        if raw_ddl is None:
            events.fire_debug_event(
                "SHOW TABLE unavailable for {}; falling back to server-provided clone SQL",
                clone_source,
            )
            for sql in clone_sqls:
                self.adapter.execute(sql)
            return

        target_ddl = self._normalize_ddl_for_clone(raw_ddl, clone_target)
        for sql in [
            f"DROP TABLE IF EXISTS {clone_target}",
            target_ddl,
            f"INSERT INTO {clone_target} SELECT * FROM {clone_source}",
        ]:
            self.adapter.execute(sql)

    def close(self) -> None:
        for adapter in self._catalog_adapters.values():
            adapter.cleanup_connections()
        super().close()

    def _to_fqn(
        self, table: str | exp.Table, normalization_dialect: t.Optional[str | Dialect] = None
    ) -> exp.Table:
        if self.case_sensitivity_enabled:
            return super()._to_fqn(
                table, normalization_dialect=self._CASE_SENSITIVE_NORMALIZATION_DIALECT
            )
        return super()._to_fqn(table)

    def _show_table_ddl(self, table_fqn: str) -> t.Optional[str]:
        """Run SHOW TABLE and return the DDL string, or None if unavailable."""
        try:
            result = self.execute(f"SHOW TABLE {table_fqn}", fetch=True)
            if not result.rows:
                return None
            return result.rows[0][0]
        except Exception as exc:
            events.fire_debug_event("SHOW TABLE failed for {}: {}", table_fqn, str(exc))
            return None

    def _normalize_ddl_for_clone(self, ddl: str, clone_target: str) -> str:
        """Normalize the SHOW TABLE DDL that is used for cloning.

        Replace the table name in a SHOW TABLE DDL string with clone_target.
        If DISTSTYLE_AUTO is set, but column-level distkey is present, remove
        the distkey attribute.
        """

        _TABLE_MODIFIER_STRINGS = {"LOCAL", "TEMPORARY", "TEMP"}
        _NAME_TYPES = {TokenType.VAR, TokenType.IDENTIFIER}

        tokens = tokenize(ddl, dialect=self.dialect)
        len_tokens = len(tokens)
        i = 0

        while i < len_tokens and tokens[i].token_type != TokenType.CREATE:
            i += 1
        if i >= len_tokens:
            return ddl
        i += 1

        while i < len_tokens and tokens[i].text.upper() in _TABLE_MODIFIER_STRINGS:
            i += 1

        if i >= len_tokens or tokens[i].token_type != TokenType.TABLE:
            return ddl
        i += 1

        if (
            i + 2 < len_tokens
            and tokens[i].text.upper() == "IF"
            and tokens[i + 1].text.upper() == "NOT"
            and tokens[i + 2].text.upper() == "EXISTS"
        ):
            i += 3

        if i >= len_tokens or tokens[i].token_type not in _NAME_TYPES:
            return ddl

        name_start = tokens[i].start
        name_end = tokens[i].end
        i += 1

        while (
            i + 1 < len_tokens
            and tokens[i].token_type == TokenType.DOT
            and tokens[i + 1].token_type in _NAME_TYPES
        ):
            name_end = tokens[i + 1].end
            i += 2

        distkey_start = None
        distkey_end = None
        has_diststyle_auto = False

        while i + 1 < len_tokens:
            curr = tokens[i]
            nxt = tokens[i + 1]

            if (
                curr.token_type == TokenType.VAR
                and curr.text.upper() == "DISTSTYLE"
                and nxt.token_type == TokenType.VAR
                and nxt.text.upper() == "AUTO"
            ):
                has_diststyle_auto = True
                break

            if curr.token_type == TokenType.VAR and curr.text.upper() == "DISTKEY":
                prev = tokens[i - 1]
                if prev.token_type not in {
                    TokenType.L_PAREN,
                    TokenType.COMMA,
                } and prev.text.upper() not in {"REFERENCES", "CONSTRAINT", "LIKE"}:
                    distkey_start = (
                        prev.end + 1
                    )  # start after the token before distkey, so any whitespace is removed
                    distkey_end = curr.end
            i += 1

        if has_diststyle_auto and distkey_start is not None and distkey_end is not None:
            ddl = ddl[:distkey_start] + ddl[distkey_end + 1 :]

        normalized_ddl = ddl[:name_start] + clone_target + ddl[name_end + 1 :]
        return normalized_ddl

    def prefetch_last_modified_epochs(
        self,
        table_fqns: t.Collection[str],
        table_overrides: t.Optional[t.Dict[str, t.Callable[[], int]]] = None,
    ) -> Future[None]:
        """Batch-prefetch last modified timestamps for the given FQNs into the cache.

        Runs SHOW TABLES per schema and the sys_query_detail join in parallel background
        threads. Results are merged (sys_query_detail overrides SHOW TABLES) then stored
        in the cache, so subsequent get_last_modified_epoch calls are cache hits.

        Args:
            table_fqns: Fully qualified, quoted table name strings to prefetch.

        Returns:
            A Future that completes when the cache has been populated.
        """
        if not table_fqns:
            return super().prefetch_last_modified_epochs(table_fqns, table_overrides)

        events.fire_info_event("Fetching freshness metadata")

        claimed_fqns: t.List[str] = []
        tables_by_schema: t.Dict[t.Tuple[str, str], t.List[exp.Table]] = defaultdict(list)

        with self._last_modified_epoch_cache as cache:
            for raw_fqn in table_fqns:
                table = self._to_fqn(raw_fqn)
                fqn = self._sql(table)
                if cache.claim_if_available(fqn):
                    claimed_fqns.append(fqn)
                    tables_by_schema[table.catalog, table.db].append(table)

        if not claimed_fqns:
            return super().prefetch_last_modified_epochs(table_fqns, table_overrides)

        table_overrides = {
            self._sql(self._to_fqn(raw_fqn)): override
            for raw_fqn, override in (table_overrides or {}).items()
        }

        tables_by_catalog: t.Dict[str, t.List[exp.Table]] = defaultdict(list)
        for (catalog, _), tables in tables_by_schema.items():
            tables_by_catalog[catalog].extend(tables)

        def _fetch_show_tables_thread(
            catalog: str, schema: str, tables: t.List[exp.Table]
        ) -> t.Dict[str, t.Optional[int]]:
            set_invocation_context()
            self._ensure_thread_connection("prefetch_last_modified_timestamps")
            return self._query_show_tables_for_schema(catalog, schema, tables)

        def _fetch_sys_query_detail_thread(
            catalog: str, catalog_tables: t.List[exp.Table]
        ) -> t.Dict[str, t.Optional[int]]:
            set_invocation_context()

            catalog_adapter = self._get_or_create_catalog_adapter(catalog)
            try:
                with catalog_adapter.connection_named(catalog):
                    return self._query_sys_query_detail(catalog_tables, adapter=catalog_adapter)
            finally:
                self._thread_local.connection_acquired = False

        def _fetch_custom_thread(
            table_fqn: str, custom_fn: t.Callable[[], int]
        ) -> t.Dict[str, t.Optional[int]]:
            self._ensure_thread_connection("prefetch_custom_last_modified")
            return {table_fqn: custom_fn()}

        show_futures = [
            self._executor.submit(_fetch_show_tables_thread, catalog, schema, tables)
            for (catalog, schema), tables in tables_by_schema.items()
        ]
        sys_futures = [
            self._executor.submit(_fetch_sys_query_detail_thread, catalog, catalog_tables)
            for catalog, catalog_tables in tables_by_catalog.items()
        ]
        custom_futures = [
            self._executor.submit(_fetch_custom_thread, fqn, override)
            for fqn, override in table_overrides.items()
        ]

        def _wait_all() -> None:
            merged: t.Dict[str, t.Optional[int]] = {}
            for f in show_futures:
                try:
                    merged.update(f.result())
                except Exception as exc:
                    events.fire_warn_event_suboptimal(
                        "Failed to prefetch SHOW TABLES for Redshift: {}", str(exc)
                    )
            for f in sys_futures:
                try:
                    merged.update(f.result())
                except Exception as exc:
                    events.fire_warn_event_suboptimal(
                        "Failed to prefetch sys_query_detail for Redshift: {}", str(exc)
                    )
            for f in custom_futures:
                try:
                    merged.update(f.result())
                except Exception as exc:
                    events.fire_warn_event_suboptimal(
                        "Failed to prefetch custom freshness queries for Redshift: {}", str(exc)
                    )

            for fqn in claimed_fqns:
                if fqn not in merged:
                    merged[fqn] = None
            with self._last_modified_epoch_cache as cache:
                cache.fulfill_many(merged)

        return self._executor.submit(_wait_all)

    def _fetch_last_modified_epochs(
        self, table_batch: t.Collection[exp.Table]
    ) -> dict[str, t.Optional[int]]:
        if not table_batch:
            return {}

        table_fqns = [self._to_fqn(t) for t in table_batch]
        last_modified_epochs: dict[str, t.Optional[int]] = {
            self._sql(fqn): None for fqn in table_fqns
        }

        tables_by_schema: dict[tuple[str, str], list[exp.Table]] = defaultdict(list)
        tables_by_catalog: dict[str, list[exp.Table]] = defaultdict(list)
        for fqn in table_fqns:
            tables_by_schema[fqn.catalog, fqn.db].append(fqn)
            tables_by_catalog[fqn.catalog].append(fqn)

        for (catalog, schema), schema_tables in tables_by_schema.items():
            # SHOW TABLES timestamps have a lag of approximately 20 minutes.
            # Normally, we use _query_sys_query_detail to supplement the lag time, but metadata views and system catalogs
            # are not shared to datashare consumers:
            # https://docs.aws.amazon.com/redshift/latest/dg/considerations-datashare-reads-writes.html
            # For datashare consumers, we return None so there is no false cache hit, which can occur when
            # timestamps have changed but those timestamps have not yet propagated to SHOW TABLES.
            if catalog.lower() in self._datashare_catalogs:
                continue

            last_modified_epochs.update(
                self._query_show_tables_for_schema(catalog, schema, schema_tables)
            )

        for catalog, catalog_tables in tables_by_catalog.items():
            catalog_adapter = self._get_or_create_catalog_adapter(catalog)
            with catalog_adapter.connection_named(catalog):
                sys_results = self._query_sys_query_detail(catalog_tables, adapter=catalog_adapter)

            for fqn_key, epoch in sys_results.items():
                if fqn_key in last_modified_epochs:
                    last_modified_epochs[fqn_key] = epoch

        return last_modified_epochs

    def _query_show_tables_for_schema(
        self,
        catalog: str,
        schema: str,
        tables: t.Collection[exp.Table],
    ) -> t.Dict[str, t.Optional[int]]:
        """Run SHOW TABLES for one schema and return an FQN→epoch dict for the given tables."""
        result: t.Dict[str, t.Optional[int]] = {}
        if self.case_sensitivity_enabled:
            table_names = {tbl.name for tbl in tables}
        else:
            table_names = {tbl.name.lower() for tbl in tables}
        show_result = self.execute(f"SHOW TABLES FROM SCHEMA {catalog}.{schema}", fetch=True)

        for row in show_result:
            row_table_name = (
                row["table_name"] if self.case_sensitivity_enabled else row["table_name"].lower()
            )
            if row_table_name not in table_names:
                continue
            fqn_key = self._build_fqn_from_row(
                row["database_name"], row["schema_name"], row["table_name"]
            )
            candidates = [
                ts for ts in (row["last_modified_time"], row["last_altered_time"]) if ts is not None
            ]
            if candidates:
                result[fqn_key] = int(
                    max(candidates).replace(tzinfo=timezone.utc).timestamp() * 1000
                )
        return result

    def _query_sys_query_detail(
        self, tables: t.Collection[exp.Table], adapter: SQLAdapter
    ) -> t.Dict[str, t.Optional[int]]:
        """Query Redshift table creation/recent write metadata and return an FQN→epoch dict."""
        if not tables:
            return {}

        catalog = next(iter(tables)).catalog or self.default_catalog

        tables_by_schema: dict[str, list[exp.Table]] = defaultdict(list)
        for tbl in tables:
            tables_by_schema[tbl.db].append(tbl)

        or_conditions = []
        for schema_value, schema_tables in tables_by_schema.items():
            if self.case_sensitivity_enabled:
                schema_condition = f"ns.nspname = '{schema_value}'"
                in_list = ", ".join(f"'{tbl.name}'" for tbl in schema_tables)
                table_name_condition = f"c.relname IN ({in_list})"
            else:
                schema_condition = f"upper(ns.nspname) = upper('{schema_value}')"
                in_list = ", ".join(f"'{tbl.name.upper()}'" for tbl in schema_tables)
                table_name_condition = f"upper(c.relname) IN ({in_list})"
            or_conditions.append(f"({schema_condition} AND {table_name_condition})")

        schema_table_filter = " OR ".join(or_conditions)

        # note: we deliberately don't join to sys_transaction_history via sys_query_history to only consider timestamps
        # on committed transactions because it slows things down too much. so if a table is modified in a transaction,
        # and that transaction gets rolled back, that will show an updated last_modified
        sys_rows_sql = f"""
            SELECT
                ns.nspname AS schema_name,
                c.relname AS table_name,
                MAX(events.event_time) AS last_updated
            FROM pg_class c
            JOIN pg_namespace ns ON ns.oid = c.relnamespace
            JOIN (
                SELECT
                    pci.reloid AS table_id,
                    pci.relcreationtime AS event_time
                FROM pg_class_info pci
                WHERE pci.relcreationtime IS NOT NULL
                AND pci.relcreationtime >= DATEADD(minute, -{self._SYS_QUERY_DETAIL_LOOKBACK_MINUTES}, (SYSDATE at time zone CURRENT_SETTING('timezone')) at time zone 'UTC')

                UNION ALL

                SELECT
                    qd.table_id,
                    qd.end_time AS event_time
                FROM sys_query_detail qd
                WHERE qd.step_name IN ('insert', 'delete')
                AND qd.end_time >= DATEADD(minute, -{self._SYS_QUERY_DETAIL_LOOKBACK_MINUTES}, (SYSDATE at time zone CURRENT_SETTING('timezone')) at time zone 'UTC')
            ) events ON events.table_id = c.oid
            WHERE ({schema_table_filter})
            GROUP BY 1, 2
            """

        _, agate_result = adapter.execute(sys_rows_sql, fetch=True)
        sys_rows = agate_result.rows

        result: t.Dict[str, t.Optional[int]] = {}
        for schema_name, table_name, last_updated in sys_rows:
            if last_updated is None:
                continue
            fqn_key = self._build_fqn_from_row(catalog, schema_name.strip(), table_name.strip())
            result[fqn_key] = int(last_updated.replace(tzinfo=timezone.utc).timestamp() * 1000)
        return result

    def _fetch_view_definitions(self, table_batch: t.Collection[exp.Table]) -> ViewFetchResult:
        if not table_batch:
            return ViewFetchResult(definitions=[])

        queries = []
        # redshift supports cross-database queries, need to group/query by catalog
        for catalog, tables in group_tables_by_catalog(table_batch, self.default_catalog).items():
            filter_expr = build_information_schema_filter(tables, ("table_schema", "table_name"))
            query = f"""
            SELECT
                table_catalog,
                table_schema,
                table_name,
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
            # information_schema.views only populates view_defintions for the owner.
            # For non-owners, the row will still populate, but with view_defintion as NULL.
            if view_definition is None:
                events.fire_debug_event(
                    "Object definition is NULL for {}, skipping. This is typically caused by insufficient permissions to fetch the object's DDL.",
                    fqn,
                )
                continue

            view_definitions.append(
                ViewDefinition(
                    fqn=fqn,
                    definition=view_definition,
                    dialect=self.dialect,
                    default_catalog=catalog,
                    default_schema=schema,
                )
            )

        return ViewFetchResult(definitions=view_definitions)

    @override
    def cache_view_definition(self, table: exp.Table, definition: str, default_schema: str) -> None:
        # Redshift uses early-binding views by default: at CREATE VIEW time it
        # fully resolves the view body and stores the resolved form. Reading the
        # view back from information_schema.views therefore returns the resolved
        # SQL, not the original — e.g. `select id from upstream as up` becomes
        # `SELECT up.id FROM upstream up`.
        # https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html

        # dbt's compiled_code is the unresolved form. If we cache compiled_code
        # in run 1 and fall through to information_schema.views in run 2 (because
        # the view isn't in the selected set), the two runs produce different
        # `stable_sql` for the view dependency, which breaks candidate matching on
        # the server.

        # Skip the cache write so every run sources view definitions from the
        # warehouse via `_fetch_view_definitions`, ensuring identical
        # canonicalization across runs.
        return

    def _get_or_create_catalog_adapter(self, catalog: str) -> SQLAdapter:
        catalog = catalog.lower()
        if catalog == self.default_catalog.lower():
            return self.adapter

        if catalog not in self._catalog_adapters:
            creds = self.adapter.config.credentials.replace(database=catalog)
            config = replace(self.adapter.config, credentials=creds)
            self._catalog_adapters[catalog] = type(self.adapter)(config, get_context("spawn"))
        return self._catalog_adapters[catalog]
