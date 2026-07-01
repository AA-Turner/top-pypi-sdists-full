from __future__ import annotations

import typing as t
from dbt.config import RuntimeConfig
from dbt.adapters.sql import SQLAdapter

from dbt_state.adapters import BaseAdapterExtension
from dbt_state import events
from dbt_state.config import CloneIncrementalInDev, RunCacheConfig
from dbt_state.relation import DeferredRelationResolver
from dbt_state.profiles import Profiles
from dbt_state.utils import is_full_refresh, is_incremental_or_snapshot


if t.TYPE_CHECKING:
    from dbt_state._typing import ModelOrSnapshotNode


class DevCloner:
    def __init__(
        self,
        config: RuntimeConfig,
        adapter_ext: BaseAdapterExtension,
        profiles: Profiles,
        deferred_relation_resolver: DeferredRelationResolver,
        run_cache_config: RunCacheConfig,
    ) -> None:
        self._config = config
        self._adapter_ext = adapter_ext
        self._profiles = profiles
        self._deferred_relation_resolver = deferred_relation_resolver
        self._run_cache_config = run_cache_config

    def get_clone_source(
        self, node: ModelOrSnapshotNode
    ) -> t.Optional[t.Tuple[str, t.Optional[str]]]:
        """Returns the clone source table name and type."""
        profiles = self._profiles
        clone_incremental_in_dev = self._run_cache_config.resolve_clone_incremental_in_dev(
            node.config
        )
        if (
            profiles.is_defer_to_profile
            or is_full_refresh(self._config, node)
            or not is_incremental_or_snapshot(node)
            or clone_incremental_in_dev == CloneIncrementalInDev.NEVER
        ):
            return None

        if not profiles.has_defer_to_profile:
            events.fire_debug_event(
                "No defer_to target configured for cloning, skipping clone for '{}'",
                node.name,
            )
            return None

        if clone_incremental_in_dev != CloneIncrementalInDev.ALWAYS:
            if self._adapter_ext.adapter.get_relation(
                database=node.database,
                schema=node.schema,
                identifier=node.identifier,
            ):
                events.fire_debug_event(
                    "Target table '{}' already exists, skipping clone",
                    node.relation_name,
                )
                return None

        defer_to_schema = self._deferred_relation_resolver.get_deferred_schema(node)
        defer_to_database = self._deferred_relation_resolver.get_deferred_database(node)
        defer_to_identifier = self._deferred_relation_resolver.get_deferred_identifier(node)

        defer_to_relation = self._adapter_ext.adapter.get_relation(
            database=defer_to_database,
            schema=defer_to_schema,
            identifier=defer_to_identifier,
        )
        if not defer_to_relation:
            events.fire_debug_event("Model '{}' has no matching table to clone from", node.name)
            return None

        try:
            defer_to_relation_sql = defer_to_relation.render()
            source_table_type = self._adapter_ext.get_relation_table_type(
                node=node, relation=defer_to_relation
            )
            return defer_to_relation_sql, source_table_type
        except Exception as e:
            events.fire_warn_event(
                "Failed to clone table {} into table {}: {}",
                defer_to_relation_sql,
                node.relation_name,
                str(e),
            )
            return None

    def clone(
        self,
        adapter: SQLAdapter,
        node: ModelOrSnapshotNode,
        clone_sqls: t.Iterable[str],
        clone_source: str,
        clone_target: str,
    ) -> None:
        with events.downgrade_adapter_error_events():
            if self._adapter_ext.IMPLEMENTS_CUSTOM_CLONE:
                self._adapter_ext.clone(clone_sqls, clone_source, clone_target)
            else:
                for sql in clone_sqls:
                    adapter.execute(sql)

        # Add the created relation to the cache
        self._adapter_ext.cache_node_relation(node)

        events.fire_debug_event(
            "Cloned table {} into table {}",
            clone_source,
            clone_target,
        )
