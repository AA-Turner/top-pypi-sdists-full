from __future__ import annotations

import typing as t
from concurrent.futures import Future
from datetime import datetime, timezone

from sqlglot import exp
from collections import defaultdict
from dbt.adapters.base.relation import BaseRelation
from dbt_state import events
from dbt_state.adapters.base import BaseAdapterExtension
from dbt_state.adapters.common import (
    ViewFetchResult,
    build_information_schema_filter,
    ViewDefinition,
    group_tables_by_catalog,
)
from dbt_state.utils import set_invocation_context
from query_cache_common.utils import extract_fqn_parts
import re
import time


# A broad `table_schema IN (...)` / `(...) OR (...)` INFORMATION_SCHEMA fetch taking longer than this
# triggers a one-time hint that a dedicated `snowflake_metadata_warehouse` would speed it up.
_SLOW_METADATA_QUERY_WARNING_THRESHOLD_SECONDS = 15.0


if t.TYPE_CHECKING:
    from dbt.contracts.graph.nodes import ManifestNode


class SnowflakeAdapterExtension(BaseAdapterExtension):
    DEFAULT_SCHEMA_NAME: str | None = "public"
    SYSTEM_METADATA_CATALOGS: t.List[str] = ["snowflake"]

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self._get_view_ddl_override: t.Optional[str] = kwargs.get("get_view_ddl_override")
        self._metadata_warehouse: t.Optional[str] = kwargs.get("metadata_warehouse")

        # Emit the "slow metadata query" hint at most once per run. Fired from executor threads, so a
        # rare race may surface a single duplicate, which is harmless for an informational warning.
        self._slow_metadata_query_warning_emitted: bool = False

    @property
    def use_heuristic_clock_for_last_modified(self) -> bool:
        return True

    def current_timestamp_utc(self) -> datetime:
        return self.execute("SELECT SYSDATE()", fetch=True).rows[0][0].replace(tzinfo=timezone.utc)

    def get_relation_table_type(
        self, node: ManifestNode, relation: BaseRelation
    ) -> t.Optional[str]:
        from dbt.adapters.snowflake.relation import SnowflakeRelation
        from dbt.adapters.snowflake.relation import SnowflakeRelationType

        assert isinstance(relation, SnowflakeRelation)

        if not relation.type or relation.type not in (
            SnowflakeRelationType.DynamicTable,
            SnowflakeRelationType.Table,
        ):
            # views, CTE's, external etc are unimplemented
            return None

        # note: we can't utilize relation.get_ddl_prefix_for_create() because it doesnt exist in the dbt-snowflake version that dbt 1.7 resolves
        config = node.config

        transient_explicitly_set_true: bool = config.get("transient", False)
        is_iceberg = hasattr(relation, "is_iceberg_format") and relation.is_iceberg_format

        if relation.type == SnowflakeRelationType.DynamicTable:
            if is_iceberg:
                return "DYNAMIC ICEBERG TABLE"

            # the Snowflake adapter does not create dynamic tables as transient by default, just normal ones
            # note that DYNAMIC ICEBERG TABLE'S also cannot be transient
            return (
                "DYNAMIC TABLE" if not transient_explicitly_set_true else "TRANSIENT DYNAMIC TABLE"
            )

        if is_iceberg:
            # Note: iceberg tables cannot be transient
            return "ICEBERG TABLE"
        if transient_explicitly_set_true or config.get("transient", True):
            # dbt-snowflake creates transient tables unless the user explicitly opts out
            return "TRANSIENT TABLE"

        return "TABLE"

    def prefetch_last_modified_epochs(
        self,
        table_fqns: t.Collection[str],
        table_overrides: t.Optional[t.Dict[str, t.Callable[[], int]]] = None,
    ) -> Future[None]:
        """Batch-prefetch last modified timestamps for the given table FQNs into the cache.

        Claims cache entries, then fetches *all* rows from ``INFORMATION_SCHEMA.TABLES``
        for every distinct (catalog, schema) pair derived from the input FQNs. This avoids
        per-table filtering and warms the cache for neighbouring tables that will likely be
        needed later. The query runs on a background thread via the adapter's executor.
        On error, all claimed entries are cancelled so on-demand fetches can proceed normally.

        Args:
            table_fqns: Fully qualified, quoted table name strings to prefetch.
            table_overrides: Map of fqn -> custom last_modified function. All fqns in this are present in :table_fqns

        Returns:
            A Future that completes when the prefetch is done.
        """
        if not table_fqns:
            return super().prefetch_last_modified_epochs(table_fqns)

        events.fire_info_event("Fetching freshness metadata")

        claimed_fqns_by_catalog: t.Dict[str, t.List[str]] = defaultdict(list)
        claimed_fqns_by_schema: t.Dict[t.Tuple[str, str], t.List[str]] = defaultdict(list)
        schemas_by_catalog: t.Dict[str, t.Set[str]] = defaultdict(set)
        fqns_with_custom_last_modified = (
            {
                self._sql(self._to_fqn(raw_fqn)): override_fn
                for raw_fqn, override_fn in table_overrides.items()
            }
            if table_overrides
            else {}
        )

        with self._last_modified_epoch_cache as cache:
            for raw_fqn in table_fqns:
                table = self._to_fqn(raw_fqn)
                fqn = self._sql(table)
                if cache.claim_if_available(fqn):
                    claimed_fqns_by_catalog[table.catalog].append(fqn)
                    claimed_fqns_by_schema[(table.catalog, table.db)].append(fqn)
                    schemas_by_catalog[table.catalog].add(table.db)

        if not claimed_fqns_by_catalog:
            return super().prefetch_last_modified_epochs(table_fqns)

        def _prefetch_for_catalog(
            catalog: str, schemas: t.List[str], claimed_fqns: t.List[str]
        ) -> None:
            set_invocation_context()
            try:
                self._ensure_thread_connection("prefetch_last_modified_timestamps")
                result = {
                    fqn: last_modified
                    for fqn, last_modified in self._fetch_last_modified_epochs_from_schemas_in_catalog(
                        catalog, schemas
                    ).items()
                    if fqn not in fqns_with_custom_last_modified
                }

                with self._last_modified_epoch_cache as cache:
                    cache.fulfill_many(result)
                    for fqn in claimed_fqns:
                        if fqn not in result and fqn not in fqns_with_custom_last_modified:
                            cache.fulfill(fqn, None)
            except Exception as e:
                # if a database error occured, cache None for all the fqn's that were requested
                # this assumes that the same database error will occur in the execute phase which
                # will result in None being returned anyway, so may as well cache it now
                with self._last_modified_epoch_cache as cache:
                    cache.fulfill_many({fqn: None for fqn in claimed_fqns})
                events.fire_warn_event_suboptimal(
                    "Failed to prefetch last modified timestamps: {}", str(e)
                )

        def _prefetch_for_custom(fqn: str, last_modified_fn: t.Callable[[], int]) -> None:
            set_invocation_context()

            try:
                epoch = last_modified_fn()
                with self._last_modified_epoch_cache as cache:
                    cache.fulfill(fqn, epoch)
            except Exception as e:
                with self._last_modified_epoch_cache as cache:
                    cache.fulfill(fqn, None)
                events.fire_warn_event_suboptimal(
                    "Failed to prefetch last modified timestamp for {} using custom freshness override: {}",
                    fqn,
                    str(e),
                )

        futures: t.List[Future] = []
        if self._metadata_warehouse:
            # A dedicated metadata warehouse is configured, so fan out one query per schema instead
            # of a single per-catalog `IN (...)` scan. Single-schema INFORMATION_SCHEMA queries are
            # far more selective (and faster) than a broad multi-schema scan, and the extra
            # concurrency they create is isolated to the dedicated warehouse rather than competing
            # with model execution on the main warehouse.
            for (catalog, schema), claimed in claimed_fqns_by_schema.items():
                futures.append(
                    self._executor.submit(_prefetch_for_catalog, catalog, [schema], claimed)
                )
        else:
            for catalog, schemas in schemas_by_catalog.items():
                futures.append(
                    self._executor.submit(
                        _prefetch_for_catalog,
                        catalog,
                        list(schemas),
                        claimed_fqns_by_catalog[catalog],
                    )
                )

        for fqn, override_fn in fqns_with_custom_last_modified.items():
            futures.append(self._executor.submit(_prefetch_for_custom, fqn, override_fn))

        def _wait_all() -> None:
            for f in futures:
                f.result()

        # this does occupy an extra executor slot but it's also simple to implement and results
        # in minimal bookkeeping / dealing with protecting a counter variable / dealing with
        # error handling if executor.submit() throws an exception in an interation of the loop above
        return self._executor.submit(_wait_all)

    def _maybe_warn_slow_metadata_query(self, elapsed_seconds: float) -> None:
        """Hint (once per run) that a dedicated metadata warehouse would speed up slow broad
        INFORMATION_SCHEMA fetches. Only fires when one is not already configured, since setting it
        is the fix: it routes these queries to an isolated warehouse and fans them out per schema.
        """
        if (
            self._metadata_warehouse
            or self._slow_metadata_query_warning_emitted
            or elapsed_seconds < _SLOW_METADATA_QUERY_WARNING_THRESHOLD_SECONDS
        ):
            return

        self._slow_metadata_query_warning_emitted = True
        events.fire_warn_event(
            "Fetching table metadata (e.g., last modified timestamps) from INFORMATION_SCHEMA took "
            "{}s. Set the `metadata_warehouse` config to route "
            "these introspection queries to a dedicated warehouse. This will lead to better parallelism "
            "and reduced contention, resulting in these queries being executed significantly faster.",
            round(elapsed_seconds, 1),
        )

    def _fetch_last_modified_epochs_from_schemas_in_catalog(
        self, catalog: str, schemas: t.List[str]
    ) -> dict[str, t.Optional[int]]:
        """Fetch last modified epochs for all tables in the given schemas under the given catalog.

        Builds a SELECT query with a `table_schema IN (...)` filter covering all schemas requested
        for that catalog.
        """

        schemas = sorted(schemas)
        schema_filter = (
            exp.column("table_schema").isin(*schemas, copy=False)
            if len(schemas) > 1
            else exp.column("table_schema").eq(schemas[0])
        )
        query = f"""
        SELECT
            table_catalog,
            table_schema,
            table_name,
            DATE_PART(EPOCH_MILLISECOND, last_altered) AS last_modified_epoch
        FROM "{catalog}".INFORMATION_SCHEMA.TABLES
        WHERE
            {self._sql(schema_filter)}
        """

        start = time.monotonic()
        rows = self.execute(query, fetch=True).rows
        self._maybe_warn_slow_metadata_query(time.monotonic() - start)

        result: dict[str, t.Optional[int]] = {}
        for catalog, schema, name, last_modified_epoch in rows:
            fqn = self._build_fqn_from_row(catalog, schema, name)
            result[fqn] = int(last_modified_epoch) if last_modified_epoch is not None else None

        return result

    def _batch_tables_for_last_modified(
        self, tables: t.Collection[exp.Table]
    ) -> t.Collection[t.Collection[exp.Table]]:
        if not self._metadata_warehouse:
            return super()._batch_tables_for_last_modified(tables)

        # A dedicated metadata warehouse is configured, so fan out one on-demand last-modified query
        # per schema (parallelized across the executor), mirroring prefetch_last_modified_epochs.
        tables_by_schema: t.Dict[t.Tuple[str, str], t.List[exp.Table]] = defaultdict(list)
        for table in tables:
            tables_by_schema[(table.catalog, table.db)].append(table)
        return list(tables_by_schema.values())

    def _fetch_last_modified_epochs(
        self, table_batch: t.Collection[exp.Table]
    ) -> dict[str, t.Optional[int]]:
        if not table_batch:
            return {}

        queries = []
        tables_by_catalog = group_tables_by_catalog(table_batch, self.default_catalog)

        for catalog, tables in tables_by_catalog.items():
            # Build component filter from table objects
            filter_expr = build_information_schema_filter(
                tables, ("table_catalog", "table_schema", "table_name")
            )

            # note: we must incur the penalty of hitting INFORMATION_SCHEMA.TABLES (which includes both tables and views)
            # because the significantly faster options `SHOW TABLES`, `SHOW VIEWS` and `SHOW OBJECTS`
            # do not include the LAST_ALTERED timestamp
            query = f"""
            SELECT
                table_catalog,
                table_schema,
                table_name,
                DATE_PART(EPOCH_MILLISECOND, last_altered) AS last_modified_epoch
            FROM "{catalog}".INFORMATION_SCHEMA.TABLES
            WHERE
                {self._sql(filter_expr)}
            """
            queries.append(query)

        query = "UNION ALL\n".join(queries)

        try:
            start = time.monotonic()
            rows = self.execute(query, fetch=True).rows
            self._maybe_warn_slow_metadata_query(time.monotonic() - start)

            # ensure that we have an entry for all input tables, even if some are missing from information_schema
            # (can happen if theyre views OR we try to fetch last_modified for a table that doesnt exist yet)
            result: dict[str, t.Optional[int]] = {self._sql(t): None for t in table_batch}
            for catalog, schema, name, last_modified_epoch in rows:
                fqn = self._build_fqn_from_row(catalog, schema, name)
                result[fqn] = int(last_modified_epoch) if last_modified_epoch is not None else None
            return result
        except Exception as e:
            events.fire_warn_event_suboptimal(
                "Failed to fetch table last modified timestamps for databases: '{}' {}",
                ", ".join(tables_by_catalog),
                str(e),
            )
            return {}

    def _fetch_view_definitions(self, table_batch: t.Collection[exp.Table]) -> ViewFetchResult:
        if not table_batch:
            return ViewFetchResult(definitions=[])

        fqns = [t.sql(dialect=self.dialect) for t in table_batch]

        query = _fetch_view_definition_script(fqns, get_ddl_override=self._get_view_ddl_override)

        try:
            rows = self.execute(f"EXECUTE IMMEDIATE $${query}$$", fetch=True).rows
            result = []
            unresolvable: t.Set[str] = set()
            for fqn, view_definition, error in rows:
                if view_definition is None:
                    # This message deliberately covers both tables and views as:
                    # - we don't know the object type before calling GET_DDL()
                    # - looking it up just for a nicer error message (or to avoid calling GET_DDL() for a table) has more overhead than just calling GET_DDL() on everything
                    events.fire_debug_event(
                        "Object definition is NULL for {}, skipping. This is typically caused by insufficient permissions to fetch the object's DDL. Error: {}",
                        fqn,
                        error,
                    )
                    # Collected so callers can treat these as always-stale (their last_altered does not reflect data changes)
                    unresolvable.add(fqn)
                    continue

                # skip tables, GET_DDL('VIEW', '<something>') still returns CREATE TABLE statements for tables...
                if is_table_ddl(view_definition):
                    continue

                catalog, schema, _ = extract_fqn_parts(fqn, dialect=self.dialect)

                result.append(
                    ViewDefinition(
                        fqn=fqn,
                        definition=view_definition,
                        dialect=self.dialect,
                        default_catalog=catalog,
                        default_schema=schema,
                    )
                )
            return ViewFetchResult(definitions=result, unresolvable=unresolvable)
        except Exception as e:
            events.fire_warn_event_suboptimal("Failed to fetch view definitions: {}", str(e))
            return ViewFetchResult(definitions=[])

    def _ensure_thread_connection(self, name: str, force: bool = False) -> None:
        was_acquired = self._connection_acquired
        super()._ensure_thread_connection(name, force)
        if self._metadata_warehouse and not was_acquired:
            self.execute(f"USE WAREHOUSE {self._metadata_warehouse}")


TABLE_REGEX = re.compile(
    r"""
    ^\s*create\b
    (?:\s+(?!table\b)\w+)*
    \s+table\b
    """,
    re.IGNORECASE | re.VERBOSE,
)


def is_table_ddl(ddl_str: str) -> bool:
    if not ddl_str or not ddl_str.strip():
        return False

    return bool(TABLE_REGEX.match(ddl_str))


def _fetch_view_definition_script(
    fqns: t.Collection[str], get_ddl_override: t.Optional[str] = None
) -> str:
    # Implementation notes:
    #
    # tl;dr we use GET_DDL() because we can determine what we need to with a single call and it's faster than alternatives
    #
    # "why not INFORMATION_SCHEMA" / "why not SHOW VIEWS"?
    # - view definitions are not reliably available from INFORMATION_SCHEMA, depending on what permissions have been granted
    #   > eg a user may have USAGE and can SELECT from a view, but if they are not the OWNER, INFORMATION_SCHEMA.VIEWS wont show the definition
    # - INFORMATION_SCHEMA is also incredibly slow, even when filtering by TABLE_CATALOG / TABLE_SCHEMA / TABLE_NAME
    # - SHOW VIEWS is much faster than INFORMATION_SCHEMA but is still slightly slower than GET_DDL() and is more complex to use with an arbitrary FQN list
    #
    # GET_DDL() isnt perfect, it does have some usage quirks:
    # - it throws errors rather than returning NULL if there is a problem fetching the definition (eg doesnt exist / access denied)
    # - it operates on a single object at a time
    # - it fails when called on objects in shared databases, because they exist in other Snowflake accounts
    #
    # So, we wrap its usage in an anonymous script block that:
    # - takes a simple list of FQN strings as input
    # - calls GET_DDL() on each one (or a user-specified lookup function for more advanced use cases)
    # - captures and returns errors as part of the resultset, so it doesnt fail for objects that dont exist or otherwise cant be fetched
    #
    # We can get away with a single GET_DDL() call for each object because it will return either CREATE TABLE for tables and CREATE VIEW for views, so we
    # know if the object is a table or a view due to that
    #
    # If it returns an error, the object will be treated as a table, which is fine in terms of tracking upstream dependencies, because get_last_modified_epoch()
    # still works regardless of the object type

    if get_ddl_override:
        get_ddl_call = f"{get_ddl_override}(:obj_name)"
    else:
        get_ddl_call = "get_ddl('VIEW', :obj_name)"

    fqn_literals = [exp.Literal.string(fqn) for fqn in fqns]

    return f"""
begin
    let objects array := array_construct(
        {", ".join(lit.sql(dialect="snowflake") for lit in fqn_literals)}
    );

    let i integer := 0;
    let results array := array_construct();

    while (i < array_size(objects)) do
        let obj_name string := objects[i]::string;

        begin
            let ddl_text string := (select {get_ddl_call});

            results := array_append(results, object_construct(
                'OBJECT_NAME', :obj_name,
                'DEFINITION', :ddl_text,
                'ERROR', null
            ));

        exception
            when other then
                results := array_append(results, object_construct(
                    'OBJECT_NAME', :obj_name,
                    'DEFINITION', null,
                    'ERROR', :sqlerrm
                ));
        end;

        i := i + 1;
    end while;

    let rs resultset := (
        select
            f.value['OBJECT_NAME']::string as fqn,
            f.value['DEFINITION']::string as view_definition,
            f.value['ERROR']::string as error
        from table(flatten(input => :results)) f
        order by 1
    );

    return table(rs);
end;"""
