from __future__ import annotations

import threading
import typing as t
from concurrent.futures import Future

from dbt.config.runtime import RuntimeConfig
from dbt.contracts.graph.manifest import Manifest, SourceDefinition
from dbt.contracts.graph.nodes import ManifestNode

from dbt_state import events
from dbt_state.adapters import BaseAdapterExtension
from dbt_state.freshness import Freshness
from dbt_state.node_resolution import NodeResolution


class MetadataPrefetcher:
    """Kicks off and awaits the async last-modified and schema metadata prefetches.

    Owns the lock, flag and future state of both prefetches. They are independent of each other.
    """

    def __init__(
        self,
        adapter_ext: BaseAdapterExtension,
        node_resolution: NodeResolution,
        freshness: Freshness,
        manifest: Manifest,
        config: RuntimeConfig,
    ) -> None:
        self._adapter_ext = adapter_ext
        self._node_resolution = node_resolution
        self._freshness = freshness
        self._manifest = manifest
        self._config = config

        self._prefetch_tables_lock = threading.Lock()
        self._prefetch_started: bool = False
        self._prefetch_future: t.Optional[Future[None]] = None
        self._prefetch_done: bool = False

        self._prefetch_schemas_lock = threading.Lock()
        self._prefetch_schemas_started: bool = False
        self._prefetch_schemas_future: t.Optional[Future[None]] = None
        self._prefetch_schemas_done: bool = False

    def collect_all_prefetch_tables(
        self, selected_ids: t.Set[str]
    ) -> t.Dict[str, ManifestNode | SourceDefinition]:
        """Collect tables from selected model/snapshot nodes and their dependencies for batch prefetching.

        Args:
            selected_ids: The set of unique IDs for models/snapshots selected for this run.
                When non-empty, only tables relevant to these nodes are collected.
                When empty, all model/snapshot tables are collected (full-project run).
        """
        tables: t.Dict[str, ManifestNode | SourceDefinition] = {}
        unselected_model_dep_ids, source_ids = self._node_resolution.collect_unselected_node_deps(
            selected_ids
        )

        for node in self._node_resolution.iter_selected_nodes(selected_ids):
            tables[
                self._node_resolution.node_to_table(node).sql(dialect=self._node_resolution.dialect)
            ] = node

        for source_id in source_ids:
            source = self._manifest.sources.get(source_id)
            if source is not None:
                tables[
                    self._node_resolution.node_to_table(source).sql(
                        dialect=self._node_resolution.dialect
                    )
                ] = source

        for dep_id in unselected_model_dep_ids:
            dep_node = self._manifest.nodes.get(dep_id)
            if dep_node is None:
                continue
            table = (
                self._node_resolution.node_to_deferred_table(dep_node)
                if self._node_resolution.defer_enabled
                else self._node_resolution.node_to_table(dep_node)
            )
            tables[table.sql(dialect=self._node_resolution.dialect)] = dep_node

        return tables

    def collect_edge_prefetch_fqns(self, selected_ids: t.Set[str]) -> t.Set[str]:
        """FQNs of the statically known edge tables of the selected models/snapshots.

        An edge is a relation a selected node reads that this invocation does not build: sources,
        seeds, and unselected upstream nodes. Unselected nodes may be deferred, so their candidate
        FQNs depend on the defer settings:
        - defer disabled: the local relation
        - defer enabled with `--favor-state`: the deferred relation only
        - defer enabled otherwise: both, since dbt only defers when the local relation is missing,
            and we dont know for sure if it's missing or not without an expensive metadata check

        Args:
            selected_ids: Unique IDs selected for this run. Empty means a full-project run.
        """
        favor_state = bool(getattr(self._config.args, "favor_state", False))
        built_ids = {n.unique_id for n in self._node_resolution.iter_selected_nodes(selected_ids)}
        fqns: t.Set[str] = set()

        def add(node: ManifestNode | SourceDefinition, deferred: bool = False) -> None:
            table = (
                self._node_resolution.node_to_deferred_table(node)  # ty: ignore[invalid-argument-type]
                if deferred
                else self._node_resolution.node_to_table(node)
            )
            fqns.add(table.sql(dialect=self._node_resolution.dialect))

        for node in self._node_resolution.iter_selected_nodes(selected_ids):
            dep_ids, source_ids = self._node_resolution.resolve_deps(node)

            # sources are always edge nodes
            for source_id in source_ids:
                if (source := self._manifest.sources.get(source_id)) is not None:
                    add(source)

            for dep_id in dep_ids:
                dep = self._manifest.nodes.get(dep_id)
                if dep is None or dep_id in built_ids:
                    # built by this run, so isnt an edge
                    continue

                if self._node_resolution.defer_enabled and dep_id not in selected_ids:
                    # there is a dependency on a deferred relation, add it as an edge
                    add(dep, deferred=True)

                    if not favor_state:
                        # if --favor-state is not set, a local version of a deferred relation is used over the
                        # remote one, if it exists. Since the "if it exists" check is expensive, we add it to
                        # the list of schemas to prefetch, and if it doesnt exist the schema prefetch will
                        # return no information for it
                        add(dep)
                else:
                    add(dep)
        return fqns

    def start_prefetch_last_modified(self) -> None:
        """Kick off the async last-modified prefetch if not already started.

        Reads the globally selected resources and collects relevant model/snapshot/source
        FQNs, then triggers an async prefetch. Does not block on the result; use
        `await_prefetch_last_modified` to wait for it. Idempotent: subsequent calls
        are no-ops.
        """
        with self._prefetch_tables_lock:
            if self._prefetch_started:
                return
            self._prefetch_started = True
            tables = self.collect_all_prefetch_tables(self._node_resolution.selected_resource_ids)
            if not tables:
                self._prefetch_done = True
                return
            events.fire_debug_event(
                "Prefetching last modified timestamps for {} tables",
                len(tables),
            )
            freshness_overrides = {
                fqn: override
                for fqn, node in tables.items()
                if isinstance(node, SourceDefinition)
                for _, override in self._freshness.resolve_dbt_source_freshness_overrides(
                    node
                ).items()
            }
            self._prefetch_future = self._adapter_ext.prefetch_last_modified_epochs(
                tables.keys(), table_overrides=freshness_overrides
            )

    def await_prefetch_last_modified(self) -> None:
        """Ensure the prefetch has started, then block until it completes.

        Idempotent: once the prefetch has completed, subsequent calls are no-ops.
        """
        if self._prefetch_done:
            return
        self.start_prefetch_last_modified()
        with self._prefetch_tables_lock:
            future = self._prefetch_future
        if future is not None:
            future.result()
        self._prefetch_done = True

    def is_prefetch_ready(self) -> bool:
        """Whether the prefetch has completed, or there is nothing to prefetch.

        Returns False when the prefetch has not been started yet: callers decide whether
        to speculate only after starting it (see ``start_prefetch_last_modified``), so an
        unstarted prefetch is not "ready".
        """
        with self._prefetch_tables_lock:
            if not self._prefetch_started:
                return False
            future = self._prefetch_future
            return self._prefetch_done or future is None or future.done()

    def start_prefetch_schemas(self) -> None:
        """Kick off the async schema prefetch if not already started.

        Mirrors `start_prefetch_last_modified` but for schemas, and is fully decoupled from
        it (its own lock, future and done flag).

        Collects the statically known edge FQNs of the  selected models (via `collect_edge_prefetch_fqns`),
        then triggers an async prefetch. This is only a warm-up: edges discovered later
        (e.g. tables reachable only through view definitions) are fetched on demand by `get_schemas`.

        Does not block on the result; use `await_prefetch_schemas` to wait for it.
        Idempotent: subsequent calls are no-ops.
        """
        with self._prefetch_schemas_lock:
            if self._prefetch_schemas_started:
                return
            self._prefetch_schemas_started = True
            edge_fqns = sorted(
                self.collect_edge_prefetch_fqns(self._node_resolution.selected_resource_ids)
            )
            if not edge_fqns:
                self._prefetch_schemas_done = True
                return

            events.fire_debug_event("Prefetching schemas for {} edge tables", len(edge_fqns))
            self._prefetch_schemas_future = self._adapter_ext.prefetch_schemas(edge_fqns)

    def await_prefetch_schemas(self) -> None:
        """Ensure the schema prefetch has started, then block until it completes.

        Idempotent: once the prefetch has completed, subsequent calls are no-ops.
        """
        if self._prefetch_schemas_done:
            return
        self.start_prefetch_schemas()
        with self._prefetch_schemas_lock:
            future = self._prefetch_schemas_future
        if future is not None:
            future.result()
        self._prefetch_schemas_done = True
