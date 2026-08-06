from __future__ import annotations

import typing as t
from dataclasses import replace

from dbt.config import Profile, RuntimeConfig
from dbt.contracts.graph.manifest import Manifest, ManifestNode
from dbt.parser.base import RelationUpdate


class DeferredRelationResolver:
    def __init__(
        self, config: RuntimeConfig, manifest: Manifest, defer_to_profile: Profile
    ) -> None:
        self._config = replace(config, **defer_to_profile.to_profile_info())
        self._manifest = manifest
        self._relation_updates: t.Dict[str, RelationUpdate] = {}

    def get_deferred_schema(self, node: ManifestNode) -> t.Optional[str]:
        # runs dbt's generate_schema_name() macro
        return self._get_defer_to_component(node, "schema")

    def get_deferred_database(self, node: ManifestNode) -> t.Optional[str]:
        # runs dbt's generate_database_name() macro
        return self._get_defer_to_component(node, "database")

    def get_deferred_identifier(self, node: ManifestNode) -> t.Optional[str]:
        # runs dbt's generate_alias_name() macro
        # note that alias falls back to identifier, so node.alias will use node.identifier if no alias is configured
        return self._get_defer_to_component(node, "alias")

    def _get_defer_to_component(
        self,
        node: ManifestNode,
        component: t.Literal["schema"] | t.Literal["database"] | t.Literal["alias"],
    ) -> t.Optional[str]:
        if component not in self._relation_updates:
            self._relation_updates[component] = RelationUpdate(
                self._config, self._manifest, component
            )

        override = getattr(node.config, component, None)
        relation_update = self._relation_updates[component]
        if getattr(node, "package_name", None) in relation_update.package_updaters:
            new_value = relation_update.package_updaters[node.package_name](override, node)
        else:
            new_value = relation_update.default_updater(override, node)

        if isinstance(new_value, str):
            new_value = new_value.strip()
        return new_value
