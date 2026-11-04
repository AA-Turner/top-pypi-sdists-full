from __future__ import annotations

import typing as t

from dbt.adapters.base.relation import BaseRelation
from dbt.clients.jinja import get_rendered
from dbt.config.runtime import RuntimeConfig
from dbt.context.providers import RuntimeProvider
from dbt.contracts.graph.manifest import Manifest, SourceDefinition
from dbt.contracts.graph.nodes import ModelNode
from sqlglot import exp

from dbt_state import events
from dbt_state.adapters import BaseAdapterExtension
from dbt_state.adapters.clock import EngineHeuristicsClock
from dbt_state.node_resolution import NodeResolution

if t.TYPE_CHECKING:
    from dbt_state._typing import ModelOrSnapshotOrTestOrSeedNode


class Freshness:
    """Determines last-modified epochs and table types for target and source tables.

    Owns the engine heuristic clock state, and applies any user-configured dbt source freshness
    overrides on top of the adapter's default last-modified lookup.
    """

    def __init__(
        self,
        adapter_ext: BaseAdapterExtension,
        node_resolution: NodeResolution,
        manifest: Manifest,
        config: RuntimeConfig,
    ) -> None:
        self._adapter_ext = adapter_ext
        self._node_resolution = node_resolution
        self._manifest = manifest
        self._config = config
        self._engine_heuristics_clock = EngineHeuristicsClock(adapter_ext)
        self._engine_heuristics_clock_disabled = False
        self._use_heuristic_clock_for_last_modified: bool = (
            adapter_ext.use_heuristic_clock_for_last_modified
        )

    def get_target_table_type_and_last_modified_epoch(
        self, node: ModelOrSnapshotOrTestOrSeedNode
    ) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        target_table = self._node_resolution.node_to_table(node)
        self._adapter_ext.clear_cache([target_table])
        last_modified_epoch = self.get_heuristic_last_modified_epoch(target_table)
        target_table_type = self.node_table_type(node)

        return target_table_type, last_modified_epoch

    def node_table_type(self, node: ModelOrSnapshotOrTestOrSeedNode) -> t.Optional[str]:
        # note: get_relation() only returns a relation for relations that exist
        # it's intended that the table type is determined *after* dbt has created the tables, not before
        if (
            relation := self._adapter_ext.adapter.get_relation(
                database=node.database, schema=node.schema, identifier=node.identifier
            )
        ) and isinstance(relation, BaseRelation):
            return self._adapter_ext.get_relation_table_type(node=node, relation=relation)

        return None

    def get_heuristic_now_epoch(self) -> t.Optional[int]:
        if self._engine_heuristics_clock_disabled:
            return None

        try:
            return self._engine_heuristics_clock.now_utc_epoch()
        except Exception as e:
            events.fire_debug_event(
                "Failed to get heuristic epoch: {}; disabling heuristic clock",
                str(e),
            )
            self._engine_heuristics_clock_disabled = True

    def get_heuristic_last_modified_epoch(self, table: exp.Table) -> t.Optional[int]:
        if not self._use_heuristic_clock_for_last_modified:
            return self.get_last_modified_epoch(table)

        if heuristic_now_millis := self.get_heuristic_now_epoch():
            self._adapter_ext.cache_last_modified_epoch(table, heuristic_now_millis)
            return heuristic_now_millis
        events.fire_debug_event(
            "Failed to get heuristic last modified for table '{}', falling back to warehouse query",
            table.sql(dialect=self._node_resolution.dialect),
        )
        self._use_heuristic_clock_for_last_modified = False
        return self.get_last_modified_epoch(table)

    def get_last_modified_epoch(self, table: exp.Table) -> t.Optional[int]:
        last_modified_epochs = self._adapter_ext.get_last_modified_epoch([table])
        if len(last_modified_epochs) != 1:
            raise RuntimeError("Expected exactly one table info")
        last_modified_epoch = next(iter(last_modified_epochs.values()))
        if last_modified_epoch is None:
            events.fire_debug_event(
                "Failed to get last modified for table: '{}'",
                table.sql(dialect=self._node_resolution.dialect),
            )
        return last_modified_epoch

    def resolve_dbt_source_freshness_overrides(
        self, node: ModelNode | SourceDefinition
    ) -> t.Dict[str, t.Callable[[], int]]:
        """Users can configure source freshness in their project by adding a `freshness:` block to the source
        definitions. They can either specify a timestamp column to use or a custom query to run.

        In normal dbt, these only get invoked if the user runs `dbt source freshness`.
        However in run-cache we want to treat this logic as an override to our default method of determining source freshness.

        So, given a model node, this function packages up any freshness overrides on its sources into functions that,
        when executed, return a run-cache compatible last_modified_epoch.

        Docs: https://docs.getdbt.com/reference/resource-properties/freshness?version=1.12

        params:
            node: a ModelNode that may or may not have {{ source() }} blocks in it

        returns:
            A dict of source fqn -> function to call that will run dbt freshness and return a run-cache compatible last_modified_epoch.
            Only sources with freshness overrides specified in user config are returned.
        """

        if isinstance(node, ModelNode):
            _, source_ids = self._node_resolution.resolve_deps(node)
            source_definitions = list(
                filter(None, [self._manifest.sources.get(source_id) for source_id in source_ids])
            )
        else:
            source_definitions = [node]

        overrides = {}
        for defn in source_definitions:
            if hasattr(defn, "loaded_at_query"):
                # loaded_at_query doesnt exist until dbt 1.10 and takes precedence over loaded_at_field
                if defn.loaded_at_query is None and defn.loaded_at_field is None:
                    continue
            elif defn.loaded_at_field is None:
                continue

            relation = self._adapter_ext._node_to_relation(defn)  # noqa: SLF001

            # note: these are deliberately bound as defaults so that the correct value is captured in each _run_freshness() function
            def _run_freshness(
                defn: SourceDefinition = defn, relation: BaseRelation = relation
            ) -> int:
                # logic adapted from: https://github.com/dbt-labs/dbt-core/blob/c02340d4c14df1459c00cf91b9ab738e1c4c9507/core/dbt/task/freshness.py#L120
                if hasattr(defn, "loaded_at_query") and defn.loaded_at_query:
                    # only present if loaded_at_query is present, dbt >= 1.10
                    from dbt.context.providers import SourceContext

                    compiled_code = get_rendered(
                        defn.loaded_at_query,
                        SourceContext(
                            defn, self._config, self._manifest, RuntimeProvider(), None
                        ).to_dict(),
                        defn,
                    )
                    _, freshness = self._adapter_ext.adapter.calculate_freshness_from_custom_sql(
                        relation,
                        compiled_code,
                        macro_resolver=self._manifest,
                    )
                elif defn.loaded_at_field:
                    _, freshness = self._adapter_ext.adapter.calculate_freshness(
                        relation,
                        defn.loaded_at_field,
                        defn.freshness.filter if defn.freshness else None,
                        self._manifest,
                    )
                else:
                    raise ValueError(
                        f"No custom freshness metadata defined for {relation.render()}; execution should not have reached here"
                    )

                # the returned datetimes are not naive so this works
                user_last_modified_epoch = int(freshness["max_loaded_at"].timestamp() * 1000)

                # note: we use the heuristic clock instead of adapter_ext.current_timestamp_utc() to avoid the overhead of another db query
                if now_epoch := self.get_heuristic_now_epoch():
                    # verify the value isnt far in the future. if a far future value gets cached,
                    # and then the user fixes their freshness query to return a reasonable value,
                    # run-cache will keep returning Skip responses because the new value will always
                    # be older than the original value
                    if user_last_modified_epoch > now_epoch:
                        events.fire_warn_event(
                            "Custom last_modified query for {} returned a timestamp in the future: {}. "
                            "This indicates a bug in the query. Trimming it to the current timestamp: {}.",
                            relation.render(),
                            user_last_modified_epoch,
                            now_epoch,
                        )
                        user_last_modified_epoch = now_epoch

                return user_last_modified_epoch

            source_fqn = self._node_resolution.sql(self._node_resolution.node_to_table(defn))
            overrides[source_fqn] = _run_freshness

        return overrides
