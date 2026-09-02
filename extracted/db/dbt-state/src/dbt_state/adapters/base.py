from __future__ import annotations

import abc
import functools
import os
import threading
import time
import typing as t
from collections import deque
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from datetime import datetime

import agate
from dbt.adapters.base import BaseRelation
from dbt.adapters.sql import SQLAdapter
from sqlglot import exp, parse_one
from sqlglot.dialects.dialect import Dialect
from sqlglot.optimizer.normalize_identifiers import normalize_identifiers
from sqlglot.optimizer.qualify_columns import quote_identifiers

from dbt_state.utils import set_invocation_context

try:
    from dbt.adapters.contracts.relation import RelationType
except ImportError:
    # dbt 1.7
    from dbt.adapters.base.relation import RelationType


from dbt_state import events
from dbt_state.adapters.common import (
    EventualCache,
    ViewDefinition,
    ViewFetchResult,
    ViewTraversalResult,
    map_future_payload,
)
from dbt_state.errors import AdapterExtensionError
from dbt_state.utils import find_tables

if t.TYPE_CHECKING:
    from dbt.contracts.graph.manifest import SourceDefinition
    from dbt.contracts.graph.nodes import ManifestNode


class BaseAdapterExtension(abc.ABC):
    DEFAULT_SCHEMA_NAME: str | None = None
    """Whether this adapter extension requires acquiring connections on worker threads (one per thread)."""
    REQUIRES_NAMED_CONNECTION: bool = True
    """Whether connections acquired on worker threads should be released after each use, or held
    for the duration of the thread's lifetime (until close() is called)."""
    SHOULD_RELEASE_CONNECTION: bool = False

    SYSTEM_METADATA_CATALOGS: t.ClassVar[t.List[str]] = []
    """Catalogs that should not have their last modified / view definition tracked"""
    SYSTEM_METADATA_SCHEMAS: t.ClassVar[t.List[str]] = ["information_schema"]
    """Schemas that should not have their last modified / view definition tracked"""
    IMPLEMENTS_CUSTOM_CLONE: bool = False
    """When True, the adapter extension handles clone execution via clone() rather than
    the caller executing the server-provided clone_sqls directly."""

    CLONE_CHAIN_DEPTH_LIMIT: t.Optional[int] = None
    """How many clones of clones can be created before the database throws a "Cannot have more than N chained clones"-style error.
    0 = cloning effectively disabled
    None = no limit imposed
    """

    _CONNECTION_BARRIER_TIMEOUT_SECONDS: float = 2.0

    def __init__(
        self,
        adapter: SQLAdapter,
        max_worker_threads: t.Optional[int] = None,
        worker_thread_timeout_seconds: t.Optional[int] = None,
        cache_ttl_seconds: t.Optional[int] = None,
        **kwargs: t.Any,
    ) -> None:
        self.adapter = adapter
        self._max_worker_threads = max_worker_threads
        self._view_definition_cache: EventualCache[str, t.Optional[ViewDefinition]] = EventualCache(
            ttl_seconds=cache_ttl_seconds, cache_name="view_definition_cache"
        )
        self._last_modified_epoch_cache: EventualCache[str, t.Optional[int]] = EventualCache(
            ttl_seconds=cache_ttl_seconds, cache_name="last_modified_epoch_cache"
        )
        self._max_workers = max_worker_threads or min(32, (os.cpu_count() or 1) + 4)
        self._executor = ThreadPoolExecutor(thread_name_prefix="drc", max_workers=self._max_workers)
        self._timeout = worker_thread_timeout_seconds
        self._thread_local = threading.local()
        self._known_unresolvable_fqns: t.Set[str] = set()

    @property
    def use_heuristic_clock_for_last_modified(self) -> bool:
        """Whether or not run-cache should use the "heuristic" clock to guess last_modified timestamps after execution,
        rather than reading the actual values from the database metadata.

        Guessing timestamps can be faster for some engines but has implications later when comparing timestamps
        (as dependency freshness lookups use real timestamps but an execution may have been stamped with a heuristic timestamp)

        So this should only be enabled for engines that really need it for performance reasons
        """
        return False

    @property
    def supports_view_last_modified(self) -> bool:
        return True

    @property
    def dialect(self) -> str:
        return self.adapter.type()

    @property
    def default_catalog(self) -> str:
        return self.adapter.config.credentials.database

    def execute(
        self, sql: str | exp.Expression, fetch: bool = False, **kwargs: t.Any
    ) -> agate.Table:
        if isinstance(sql, exp.Expression):
            sql = sql.sql(dialect=self.dialect)
        _, agate_table = self.adapter.execute(sql, fetch=fetch, **kwargs)
        return agate_table

    def clone(
        self,
        clone_sqls: t.Iterable[str],
        clone_source: str,
        clone_target: str,
    ) -> None:
        """Execute a dialect-specific clone of clone_source into clone_target.

        Only called when IMPLEMENTS_CUSTOM_CLONE is True. Subclasses that set
        IMPLEMENTS_CUSTOM_CLONE = True must override this method.

        Args:
            clone_sqls: Server-provided fallback SQL (may be used if custom logic fails).
            clone_source: Fully-qualified quoted source table name.
            clone_target: Fully-qualified quoted target table name.
        """
        raise NotImplementedError(
            f"{type(self).__name__} sets IMPLEMENTS_CUSTOM_CLONE=True but does not implement clone()"
        )

    @abc.abstractmethod
    def current_timestamp_utc(self) -> datetime:
        """Get the current UTC time from the database."""

    def prewarm_connections(self) -> None:
        """Eagerly acquire a connection on every executor thread.

        Doing this as early as possible is useful since establishing a new connection
        has a considerable overhead. This method is non-blocking and ensures connections
        are available by the time the actual work starts.
        """
        if not self.REQUIRES_NAMED_CONNECTION or self.SHOULD_RELEASE_CONNECTION:
            return

        num_workers = self._max_workers
        barrier = threading.Barrier(num_workers)

        def _prewarm_connection(name: str) -> None:
            prewarm_start_time = time.perf_counter()
            try:
                self._ensure_thread_connection(name)
                # Force execution of a query in case if the connection is established lazily
                self.execute("SELECT 1")
            finally:
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

    def close(self) -> None:
        self._release_all_connections()
        self._executor.shutdown(wait=True)

    def rollback(self) -> None:
        self.adapter.connections.rollback_if_open()

    @staticmethod
    def _release_orphaned_claims(
        cache: EventualCache[str, t.Any], claimed_fqns: t.Set[str]
    ) -> None:
        """Cancel any keys claimed in ``cache`` that were never fulfilled.

        Workers waiting on a claimed key block on its Future, and the wait loops have
        no overall deadline -- so a claim left unfulfilled (e.g. because an exception
        aborted the lookup) would deadlock every other worker that needs it, cascading
        across the run. Cancelling lets those waiters fail fast and fall back to a
        cache miss. Callers discard fulfilled keys as they go, so only genuine orphans
        remain here; ``cancel_inflight`` is a no-op on already-fulfilled keys anyway.
        """
        for fqn in claimed_fqns:
            cache.cancel_inflight(fqn)

    def get_last_modified_epoch(
        self,
        tables: t.Iterable[str | exp.Table],
        table_overrides: t.Optional[t.Dict[str, t.Callable[[], int]]] = None,
    ) -> dict[str, t.Optional[int]]:
        """Get the last modified epoch for the given tables.

        Tracks the keys this call claims in the shared cache and releases any it does
        not fulfill on exit (see :meth:`_release_orphaned_claims`).
        """
        claimed_fqns: t.Set[str] = set()
        try:
            return self._get_last_modified_epoch(tables, table_overrides, claimed_fqns)
        finally:
            self._release_orphaned_claims(self._last_modified_epoch_cache, claimed_fqns)

    def _get_last_modified_epoch(
        self,
        tables: t.Iterable[str | exp.Table],
        table_overrides: t.Optional[t.Dict[str, t.Callable[[], int]]],
        claimed_fqns: t.Set[str],
    ) -> dict[str, t.Optional[int]]:
        """Get the last modified epoch for the given tables.

        Args:
            tables: A list of table names
            table_overrides: A mapping of table names -> custom last_modified_epoch() functions
                Every table name present in :table_overrides is also present in :tables.
                Implementations should check for overrides and call them instead of the default behaviour.

        Returns:
            A dictionary mapping table names to their last modified timestamps in epoch millis or None if not available.
            Table names in the mapping are fully qualified and quoted.
        """
        if not tables:
            return {}

        table_overrides = table_overrides or {}

        table_map = {self._sql(fqn): fqn for fqn in [self._to_fqn(t) for t in tables]}
        override_map = {self._to_fqn(fqn): override for fqn, override in table_overrides.items()}
        futures: t.Dict[Future[t.Dict[str, t.Optional[int]]], t.Sequence[exp.Table]] = {}
        uncached_table_names: t.List[exp.Table] = []

        # we dont need to incur a db hit for system metadata tables since they arent tables that we can track modifications to
        system_metadata_table_fqns = {
            fqn for fqn, t in table_map.items() if self._is_system_metadata_table(t)
        }

        # Check cache first and see which tables need to be fetched
        with self._last_modified_epoch_cache as cache:
            for fqn, table in table_map.items():
                if fqn in system_metadata_table_fqns:
                    continue

                if cache.claim_if_available(fqn):
                    uncached_table_names.append(table)
                    claimed_fqns.add(fqn)
                else:
                    events.fire_debug_event(f"{fqn}: last_modified local cache hit")

                    future: Future[t.Dict[str, t.Optional[int]]] = map_future_payload(
                        cache.resolve_or_raise(fqn),
                        # use functools.partial to capture 'fqn' by value, otherwise
                        # when the lambda is eventually evaluated, `fqn` will point to the last
                        # value in the loop, not the value of this iteration of the loop
                        functools.partial(lambda fqn, ts: {fqn: ts}, fqn),
                    )
                    futures[future] = [table]

        # Query database only for uncached tables
        if uncached_table_names:

            def _fetch_last_modified_epochs_with_connection(
                index: int,
                table_batch_or_override: t.List[exp.Table]
                | t.Tuple[exp.Table, t.Callable[[], int]],
            ) -> dict[str, t.Optional[int]]:
                if not table_batch_or_override:
                    return {}

                # table_name
                table_batch = (
                    table_batch_or_override if isinstance(table_batch_or_override, list) else None
                )

                # table_name, override_fn
                table_override = (
                    table_batch_or_override if isinstance(table_batch_or_override, tuple) else None
                )

                set_invocation_context()

                table_names = table_batch or []
                if table_override:
                    table_name, _ = table_override
                    table_names.append(table_name)

                events.fire_debug_event(
                    f"Fetching last_modified for tables: {', '.join(self._sql(table) for table in table_names)}"
                )

                force_thread_connection = False
                if table_override:
                    # adapters like BigQuery usually dont need a thread connection to fetch last_modified because
                    # they use API calls. However a freshness override with a custom query needs to hit the database,
                    # so we need to force a connection to be present or it will fail with a "connection never acquired for thread" error
                    force_thread_connection = True

                self._ensure_thread_connection(
                    f"fetch_last_modified_timestamps_{index}", force=force_thread_connection
                )
                try:
                    if table_override:
                        table_name, override = table_override
                        return {self._sql(table_name): override()}

                    assert table_batch is not None
                    return self._fetch_last_modified_epochs(table_batch)
                finally:
                    if self.SHOULD_RELEASE_CONNECTION:
                        self._release_thread_connection()

            for index, batch in enumerate(
                self._batch_tables_for_last_modified(uncached_table_names)
            ):
                with_overrides, without_overrides = (
                    [tbl for tbl in batch if tbl in override_map],
                    [tbl for tbl in batch if tbl not in override_map],
                )

                # one future per override because they all may have different logic and cant be fetched in bulk
                for tbl in with_overrides:
                    future = self._executor.submit(
                        _fetch_last_modified_epochs_with_connection,
                        index,
                        (tbl, override_map[tbl]),
                    )
                    futures[future] = [tbl]

                # one future to batch fetch tables without overrides (default)
                future = self._executor.submit(
                    _fetch_last_modified_epochs_with_connection, index, without_overrides
                )
                futures[future] = without_overrides

        all_results: t.Dict[str, t.Optional[int]] = {
            fqn: None for fqn in system_metadata_table_fqns
        }

        while futures:
            done, _ = wait(futures, timeout=self._timeout, return_when=FIRST_COMPLETED)

            for future in done:
                tables = futures.pop(future)

                try:
                    result = future.result()

                    with self._last_modified_epoch_cache as cache:
                        cache.fulfill_many(result)

                    all_results.update(result)
                    claimed_fqns.difference_update(result)
                except Exception:
                    # We need to remove any keys in the cache we failed to fetch in order to:
                    #  - cancel any in-flight futures that other threads may be waiting on
                    #  - make the keys available for claiming again
                    for table in tables:
                        fqn = self._sql(table)
                        self._last_modified_epoch_cache.cancel_inflight(fqn)
                        claimed_fqns.discard(fqn)
                    raise

        missing_fqns: t.Dict[str, t.Optional[int]] = {
            fqn: None for fqn in table_map.keys() - all_results.keys()
        }

        # Record missing tables in cache so we don't try to fetch them again
        with self._last_modified_epoch_cache as cache:
            cache.fulfill_many(missing_fqns)

        all_results.update(missing_fqns)
        claimed_fqns.difference_update(missing_fqns)

        if missing_fqns:
            events.fire_debug_event(
                "Table(s) {} not found or access denied", ", ".join(missing_fqns)
            )

        return all_results

    def get_available_last_modified_epochs(
        self, tables: t.Iterable[str | exp.Table]
    ) -> dict[str, t.Optional[int]]:
        """Return already-resolved last-modified epochs for the given tables without
        claiming, fetching, or blocking.

        For each requested table the returned mapping contains its fully-qualified,
        quoted FQN string (same key format as get_last_modified_epoch) mapped to:
        the cached epoch if the cache entry is already resolved (may be None for a
        known-missing table), or None if the entry is still in flight or was never
        fetched. Every requested table is present in the result.
        """
        table_map = {self._sql(fqn): fqn for fqn in [self._to_fqn(table) for table in tables]}

        results: t.Dict[str, t.Optional[int]] = {}
        with self._last_modified_epoch_cache as cache:
            for fqn, table in table_map.items():
                if self._is_system_metadata_table(table):
                    results[fqn] = None
                    continue

                future = cache.resolve(fqn)
                if future is not None and future.done() and not future.exception():
                    results[fqn] = future.result()
                else:
                    results[fqn] = None

        return results

    @staticmethod
    def prefetch_last_modified_epochs(
        table_fqns: t.Collection[str],
        table_overrides: t.Optional[t.Dict[str, t.Callable[[], int]]] = None,
    ) -> Future[None]:
        """Batch-prefetch last modified timestamps into the cache for the given table FQNs.

        The default implementation is a no-op. Subclasses may override this to
        issue a single batch query that warms the cache so that subsequent
        ``get_last_modified_epoch()`` calls are pure cache hits.

        Args:
            table_fqns: Fully qualified, quoted table name strings to prefetch.
            table_overrides: Map of fqn -> custom last_modified function. All fqns in this are present in :table_fqns

        Returns:
            A Future that completes when the prefetch is done.
        """
        future: Future[None] = Future()
        future.set_result(None)
        return future

    def clear_cache(self, tables: t.Iterable[str | exp.Table]) -> None:
        """Clears any caches for the given tables.

        Args:
            tables: A list of table names.
        """
        fqns = [self._sql(self._to_fqn(t)) for t in tables]

        with self._last_modified_epoch_cache as cache:
            cache.remove(fqns)

        with self._view_definition_cache as cache:
            cache.remove(fqns)

        events.fire_debug_event(f"Cleared {', '.join(fqns)} from cache")

    def clear_last_modified_cache(self, tables: t.Iterable[str | exp.Table]) -> None:
        """Clears the last modified epoch cache for the given tables."""
        fqns = [self._sql(self._to_fqn(t)) for t in tables]
        with self._last_modified_epoch_cache as cache:
            cache.remove(fqns)

    def traverse_view_definitions(
        self, sql_or_tables: exp.Expr | str | t.Collection[exp.Table]
    ) -> ViewTraversalResult:
        """Recursively traverse view definitions for references in the given SQL or table names.

        Tracks the views this call claims in the shared cache and releases any it does
        not fulfill on exit (see :meth:`_release_orphaned_claims`).
        """
        claimed_fqns: t.Set[str] = set()
        try:
            return self._traverse_view_definitions(sql_or_tables, claimed_fqns)
        finally:
            self._release_orphaned_claims(self._view_definition_cache, claimed_fqns)

    def _traverse_view_definitions(
        self,
        sql_or_tables: exp.Expr | str | t.Collection[exp.Table],
        claimed_fqns: t.Set[str],
    ) -> ViewTraversalResult:
        """Recursively traverses view definitions for references extracted from the given SQL expression or table names.

        Args:
            sql_or_tables: A parsed or raw SQL expression to extract view references from, or a collection of table names
                representing the views to fetch definitions for.

        Returns:
            A ViewTraversalResult containing a mapping of view names to their SQL definitions. View names in the mapping
            are fully qualified and quoted.

        """
        if isinstance(sql_or_tables, str):
            sql_or_tables = parse_one(sql_or_tables, dialect=self.dialect)
        tables = (
            find_tables(sql_or_tables)
            if isinstance(sql_or_tables, exp.Expression)
            else sql_or_tables
        )

        if not tables:
            return ViewTraversalResult(
                view_definitions={}, seen_tables=set(), unresolvable_tables=set()
            )

        queue = deque(set(tables))
        visited: t.Set[str] = set()
        futures: t.Dict[Future[ViewFetchResult], t.Collection[exp.Table]] = {}
        view_definitions: t.Dict[str, ViewDefinition] = {}
        unresolvable: t.Set[str] = set()

        def _fetch_view_definitions_with_connection(
            index: int, table_batch: t.Collection[exp.Table]
        ) -> ViewFetchResult:
            if not table_batch:
                return ViewFetchResult(definitions=[])
            set_invocation_context()
            events.fire_debug_event(
                f"Fetching definition for views: {', '.join(self._sql(table) for table in table_batch)}"
            )

            self._ensure_thread_connection(f"fetch_views_{index}")
            try:
                return self._fetch_view_definitions(table_batch)
            finally:
                if self.SHOULD_RELEASE_CONNECTION:
                    self._release_thread_connection()

        while True:
            if queue:
                tables_to_query: dict[str, exp.Table] = {}
                while queue:
                    # We can't assume any of the tables in the queue are fully qualified, so we fully qualify them
                    # before doing anything
                    try:
                        next_table = self._to_fqn(queue.popleft())
                    except AdapterExtensionError:
                        continue

                    fqn = self._sql(next_table)
                    if self._is_system_metadata_table(next_table):
                        # we should not attempt to fetch view definitions for system metadata tables
                        # we should still record the dependency as a "seen_table" though, so we add it to the visited set
                        visited.add(fqn)
                        continue

                    if fqn in visited:
                        continue

                    visited.add(fqn)

                    with self._view_definition_cache as cache:
                        if cache.claim_if_available(fqn):
                            # we are now responsible for fetching this
                            tables_to_query[fqn] = next_table
                            claimed_fqns.add(fqn)
                        else:
                            # another thread is already fetching this. add it to our list of futures to wait
                            future: Future[ViewFetchResult] = map_future_payload(
                                cache.resolve_or_raise(fqn),
                                lambda vd, f=fqn: ViewFetchResult(
                                    definitions=[vd] if vd else [],
                                    unresolvable={f}
                                    if f in self._known_unresolvable_fqns
                                    else set(),
                                ),
                            )
                            futures[future] = [next_table]

                # The remaining items in tables_to_query are cache misses and need to be fetched from the db
                for idx, batch in enumerate(self._batch_table_names(tables_to_query.values())):
                    new_future = self._executor.submit(
                        _fetch_view_definitions_with_connection, idx, batch
                    )
                    futures[new_future] = batch

            elif futures:
                done, _ = wait(futures, timeout=self._timeout, return_when=FIRST_COMPLETED)
                for future in done:
                    queried_tables = futures.pop(future)

                    # Track which tables we queried for
                    queried_fqns = {self._sql(t) for t in queried_tables}

                    try:
                        raw_result = future.result()
                        unresolvable.update(raw_result.unresolvable)
                        self._known_unresolvable_fqns.update(raw_result.unresolvable)
                        fetched_definitions = {d.fqn: d for d in raw_result.definitions}

                        # Add found views to cache
                        with self._view_definition_cache as cache:
                            cache.fulfill_many(fetched_definitions)
                        claimed_fqns.difference_update(fetched_definitions)
                    except Exception:
                        # We need to remove any keys in the cache we failed to fetch in order to:
                        #  - cancel any in-flight futures that other threads may be waiting on
                        #  - make the keys available for claiming again
                        for fqn in queried_fqns:
                            self._view_definition_cache.cancel_inflight(fqn)
                        claimed_fqns.difference_update(queried_fqns)
                        raise

                    # Add found views to our overall list of definitions to return
                    view_definitions.update(fetched_definitions)

                    # Add any new tables referenced within the found views to the processing queue
                    queue.extend(
                        [
                            t
                            for d in fetched_definitions.values()
                            for t in d.extract_referenced_tables()
                        ]
                    )

                    # Cache None for tables that were queried but not found (not views)
                    if table_fqns := queried_fqns - set(fetched_definitions):
                        with self._view_definition_cache as cache:
                            cache.fulfill_many({fqn: None for fqn in table_fqns})
                        claimed_fqns.difference_update(table_fqns)

            else:
                return ViewTraversalResult(
                    view_definitions=view_definitions,
                    seen_tables=visited - set(view_definitions),
                    unresolvable_tables=unresolvable,
                )

    def cache_last_modified_epoch(self, table: exp.Table, last_modified_epoch: int) -> None:
        """Pre-populate the last modified epoch cache for a table.

        Args:
            table: The table expression identifying the table.
            last_modified_epoch: The last modified timestamp in epoch milliseconds.
        """
        fqn = self._sql(self._to_fqn(table))
        with self._last_modified_epoch_cache as cache:
            if cache.claim_if_available(fqn):
                cache.fulfill(fqn, last_modified_epoch)

    def cache_view_definition(self, table: exp.Table, definition: str, default_schema: str) -> None:
        """Pre-populate the view definition cache with a known view SQL definition.

        Uses claim_if_available so it won't overwrite an existing cache entry.

        Args:
            table: The table expression identifying the view.
            definition: The SQL definition of the view.
            default_schema: The schema used to qualify unqualified references within the definition.
        """
        fqn = self._sql(self._to_fqn(table))
        view_def = ViewDefinition(
            fqn=fqn,
            definition=definition,
            dialect=self.dialect,
            default_catalog=self.default_catalog,
            default_schema=default_schema,
        )
        with self._view_definition_cache as cache:
            if cache.claim_if_available(fqn):
                cache.fulfill(fqn, view_def, no_expire=True)

    def cache_node_relation(self, node: ManifestNode) -> None:
        """Add an entry to the model cache based on the supplied ModelNode.

        This is for when the plugin creates new database objects after dbt has populated its relation cache, to ensure those
        objects are reflected / available to the remainder of the dbt invocation.
        """
        relation = self._node_to_relation(node)
        self.adapter.cache_added(relation)

    def relation_exists(self, relation: BaseRelation) -> bool:
        """Check if the given relation exists in the database.

        Args:
            relation: The relation to check.

        Returns:
            True if the relation exists, False otherwise.
        """
        return (
            self.adapter.get_relation(
                database=relation.database,
                schema=relation.schema,
                identifier=relation.identifier,
            )
            is not None
        )

    def relation_to_fqn(self, relation: BaseRelation) -> str:
        """Convert a relation to its fully qualified name in SQL.

        Args:
            relation: The relation to convert.

        Returns:
            The fully qualified name of the relation, properly quoted.
        """
        return self._sql(self._to_fqn(relation.render()))

    def fqn_to_cached_relation(self, fqn: t.Union[str, exp.Table]) -> t.Optional[BaseRelation]:
        """Convert a fqn to a dbt relation, fetching it from the dbt relation cache"""
        fqn = self._to_fqn(fqn)

        return self.adapter.get_relation(
            database=fqn.catalog,
            schema=fqn.db,
            identifier=fqn.name,
        )

    def report(self) -> t.Dict[str, t.Any]:
        """Report any information that has been gathered during adapter execution

        Returns:
            A dictionary containing report data. An empty dict means there is nothing
            that should be reported.
        """
        data = {}

        if self._last_modified_epoch_cache.stats.contains_lock_timeouts:
            data["last_modified_epoch_cache_stats"] = self._last_modified_epoch_cache.stats.report()

        if self._view_definition_cache.stats.contains_lock_timeouts:
            data["view_definition_cache_stats"] = self._view_definition_cache.stats.report()

        return data

    def _node_to_normalized_identifiers(
        self,
        node: ManifestNode | SourceDefinition,
        override_database: t.Optional[str] = None,
        override_schema: t.Optional[str] = None,
        override_identifier: t.Optional[str] = None,
    ) -> t.Tuple[str, str, str, t.Dict[str, bool]]:
        """Break a dbt manifest node into parts that can be force-quoted without first normalizing.

        dbt supports quoting the catalog, schema and identifier portions independently whereas SQLGlot
        tends to be all-or-none.

        The output of this method can be used to construct both dbt Relation objects and SQLGlot exp.Table objects
        that are consistent with each other.

        :override_database, :override_schema and :override_identifier can be used to override the values without changing the input node object

        Returns a tuple of (database, schema, identifier, quote_policy). These are deliberately strings so that they can be used to construct
        a Relation object, but they have been normalized according to the quote policy
        """
        quote_policy = {
            **self.adapter.Relation.get_default_quote_policy().to_dict(omit_none=True),
            **self.adapter.config.quoting,
            **node.config.get("quoting", {}),
        }

        database = override_database or node.database or self.default_catalog
        schema = override_schema or node.schema
        identifier = override_identifier or str(
            node.alias if hasattr(node, "alias") else node.identifier
        )

        # normalize any unquoted identifiers
        if not quote_policy["database"] and database:
            database = self._sql(self._normalize_identifier(database))

        if not quote_policy["schema"] and schema:
            schema = self._sql(self._normalize_identifier(schema))

        if not quote_policy["identifier"] and identifier:
            identifier = self._sql(self._normalize_identifier(identifier))

        return database, schema, identifier, quote_policy

    def _node_to_relation(self, node: ManifestNode | SourceDefinition) -> BaseRelation:
        """Turn a dbt manifest node into an adapter-specific Relation object suitable for putting
        into the Relation cache, while respecting the configured quote policy"""

        database, schema, identifier, dbt_quote_policy = self._node_to_normalized_identifiers(node)

        return self.adapter.Relation.create(
            database=database,
            schema=schema,
            identifier=identifier,
            type=RelationType.Table,
            quote_policy=dbt_quote_policy,
        )

    def _node_to_table(
        self,
        node: ManifestNode | SourceDefinition,
        override_database: t.Optional[str] = None,
        override_schema: t.Optional[str] = None,
        override_identifier: t.Optional[str] = None,
    ) -> exp.Table:
        """Given a dbt node, convert it to a SQLGlot exp.Table object while applying correct quoting
        and normalization per the dbt quote policy for this node.

        Note that since dbt allows a mixture of quoted and unquoted parts and SQLGlot prefers all or nothing,
        the produced SQLGlot exp.Table is semantically equivalent but not identical to the dbt Node.
        This is achieved by normalizing any identifiers that are unquoted on the dbt side and then force-quoting everything
        """
        database, schema, identifier, _ = self._node_to_normalized_identifiers(
            node,
            override_database=override_database,
            override_schema=override_schema,
            override_identifier=override_identifier,
        )
        return exp.table_(catalog=database, db=schema, table=identifier, quoted=True)

    @staticmethod
    def get_relation_table_type(node: ManifestNode, relation: BaseRelation) -> t.Optional[str]:
        """Given a dbt model node and its corresponding relation, identify if it is a special / non-standard table type.

        This is intended for when the user specifies things like `transient=True` on the model.
        We need this to be communicated server-side so we can generate correct clone statements
        (eg cloning a transient table has different syntax than cloning a normal table).

        Note that special table types tend to be database-specific which is why this method
        returns a string
        """
        return None

    @staticmethod
    def _batch_table_names(
        tables: t.Collection[exp.Table],
    ) -> t.Collection[t.Collection[exp.Table]]:
        """Given a list of tables, decide the best way of chunking them up to fetch table information (such as last modified or view definitions) *in parallel*.

        For example, some databases might batch by catalog and submit a query per catalog, while others might create a batch per table because all they
        have available is a synchronous API to fetch table-by-table.

        The default implementation just returns a single batch containing all the tables.

        Args:
            tables: A list of tables to break up into multiple batches

        Returns:
            A list of lists. Each entry is a batch of tables to process at once via self._fetch_view_definitions()
        """
        return [tables]

    def _batch_tables_for_last_modified(
        self, tables: t.Collection[exp.Table]
    ) -> t.Collection[t.Collection[exp.Table]]:
        """Batching strategy for last-modified fetches specifically.

        Defaults to `_batch_table_names`. Adapters can override this to choose a different
        parallelism strategy for on-demand last-modified queries without affecting view-definition
        batching.
        """
        return self._batch_table_names(tables)

    @abc.abstractmethod
    def _fetch_view_definitions(self, table_batch: t.Collection[exp.Table]) -> ViewFetchResult:
        """Given a batch of table references, fetch all the corresponding view definitions.

        Note that this method needs to be thread-safe as it is called concurrently

        Args:
            table_batch: A single batch of table references to fetch view definitions for.
                Note that the batch is created by self._batch_table_names

        Returns:
            A ViewFetchResult containing
            - definitions: A list of ViewDefinition objects containing the SQL that defines the view.
              Note that if some of the references in :table_batch turned out to be tables
              and not views, they are expected to not be present in the return list.
            - unresolvable: FQNs whose definition could not be fetched. These remain as
            dependencies but their last-modified metadata may not reflect data changes.

        """

    @abc.abstractmethod
    def _fetch_last_modified_epochs(
        self, table_batch: t.Collection[exp.Table]
    ) -> dict[str, t.Optional[int]]:
        """Given a batch of table references, fetch all the last modified epochs for those tables.
        The last modified epochs should be in *milliseconds*. Also, only tables should be checked as views always
        fetch the latest data by their nature.

        Args:
            table_batch: A single batch of table references to fetch view definitions for.
                Note that the batch is created by self._batch_table_names

        Returns:
            A mapping of fqn -> last modified epoch.
            If the fqn points to a view, then the fqn should map to None.
            If the fqn could not be fetched, then it should be omitted from the result entirely
        """

    @property
    def _connection_acquired(self) -> bool:
        return getattr(self._thread_local, "connection_acquired", False)

    def _ensure_thread_connection(self, name: str, force: bool = False) -> None:
        """Acquire a named dbt connection for the current thread if one hasn't been acquired yet.

        Connections are cached per-thread and only released when close() is called.
        This avoids the overhead of opening/closing a connection for every batch.
        """
        if not force and not self.REQUIRES_NAMED_CONNECTION:
            return
        if self._connection_acquired:
            return
        self.adapter.acquire_connection(name)
        self._thread_local.connection_acquired = True

    def _release_thread_connection(self) -> None:
        """Releases the current thread's connection, if it has one."""
        if not self._connection_acquired:
            return
        self.adapter.release_connection()
        self._thread_local.connection_acquired = False

    def _release_all_connections(self) -> None:
        """Release all connections that were acquired on executor threads.

        Uses a barrier to ensure every thread in the pool participates exactly once,
        preventing the race where one thread picks up multiple release tasks while
        another thread (with a connection) gets none.
        """
        if not self.REQUIRES_NAMED_CONNECTION:
            return

        num_workers = self._max_workers
        barrier = threading.Barrier(num_workers)

        def _release_on_thread() -> None:
            try:
                self._release_thread_connection()
            finally:
                try:
                    barrier.wait(timeout=self._CONNECTION_BARRIER_TIMEOUT_SECONDS)
                except threading.BrokenBarrierError:
                    pass

        futures = [self._executor.submit(_release_on_thread) for _ in range(num_workers)]
        for f in futures:
            f.result()

    def _build_fqn_from_row(self, catalog: str, schema: str, name: str) -> str:
        """Build FQN string from individual components.

        Args:
            catalog: Database/catalog name
            schema: Schema name
            name: Table/view name

        Returns:
            Fully qualified quoted name: '"CATALOG"."SCHEMA"."NAME"'
        """
        table = exp.table_(name, db=schema, catalog=catalog, quoted=True)
        return self._sql(table)

    def _to_fqn(
        self, table: str | exp.Table, normalization_dialect: t.Optional[str | Dialect] = None
    ) -> exp.Table:
        if isinstance(table, str):
            table = exp.to_table(table, dialect=self.dialect)

        # we need to use the underlying exp.Identifier objects to preserve any quoting information
        table_catalog = table.args.get("catalog")
        table_schema = table.args.get("db")
        table_name = table.args.get("this")

        if not table_schema:
            if self.DEFAULT_SCHEMA_NAME:
                table_schema = self.DEFAULT_SCHEMA_NAME
            else:
                raise AdapterExtensionError(
                    f"Missing schema in the table expression: {table.sql(dialect=self.dialect)}"
                )
        if not table_name:
            raise AdapterExtensionError(
                f"Missing table name in the table expression: {table.sql(dialect=self.dialect)}"
            )
        if not table_catalog:
            table_catalog = self.default_catalog

        # strip comments to prevent the fqn's from being generated with comments in between the parts
        for part in (table_catalog, table_schema, table_name):
            if isinstance(part, exp.Expression):
                part.comments = None

        # since _to_fqn() returns the table parts quoted, we have to normalize unquoted identifiers first
        # if we force-quote without normalizing then on engines like Snowflake we end up with identifiers
        # that should be uppercase stuck as lowercase because they were force-quoted
        return quote_identifiers(
            normalize_identifiers(
                exp.table_(
                    table_name,
                    db=table_schema,
                    catalog=table_catalog,
                ),
                dialect=normalization_dialect
                if normalization_dialect is not None
                else self.dialect,
            ),
            dialect=self.dialect,
        )

    def _sql(self, expression: exp.Expr, copy: bool = False) -> str:
        """Converts an expression to sql in the adapter dialect.

        By default sql() copies the expression for safety but if the
        expression is not shared and is created just to generate sql,
        it's faster to just generate the sql without copying it
        """
        return expression.sql(dialect=self.dialect, copy=copy)

    def _normalize_identifier(self, expr: t.Union[str, exp.Identifier]) -> exp.Identifier:
        if isinstance(expr, str):
            expr = exp.parse_identifier(expr, dialect=self.dialect)
        return normalize_identifiers(expr, dialect=self.dialect)

    def _is_system_metadata_table(self, table: exp.Table) -> bool:
        """Is the specified table a known system metadata table/view?

        These are typically virtual objects exposed by the database that dont have a last modified / view definition,
        so should be short-circuited
        """
        return (
            table.catalog.lower() in self.SYSTEM_METADATA_CATALOGS
            or table.db.lower() in self.SYSTEM_METADATA_SCHEMAS
        )
