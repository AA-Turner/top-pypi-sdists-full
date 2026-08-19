from __future__ import annotations

import typing as t
from collections import defaultdict, deque
from pathlib import Path

from dbt.graph import UniqueId
from dbt.graph.selector_methods import SelectorMethod, StateSelectorMethod

from dbt_state.git import GitClient

try:
    from dbt_common.exceptions import DbtRuntimeError
except ImportError:
    # dbt 1.7
    from dbt.exceptions import DbtRuntimeError

from query_cache_common.models.services import selector_service_models

from dbt_state._typing import MODEL_OR_SNAPSHOT_OR_TEST_OR_SEED_NODE
from dbt_state.config import RunCacheConfig
from dbt_state.grpc.client import QueryCacheGrpcClient
from dbt_state.node_hash_calculator import (
    ModelNodeHashCalculator,
    create_node_hash_calculator,
)

if t.TYPE_CHECKING:
    from dbt.config.runtime import RuntimeConfig

# Mapping from selector string to SelectorCriteria enum
_SELECTOR_CRITERIA_MAP: t.Dict[str, selector_service_models.SelectorCriteria] = {
    "new": selector_service_models.SelectorCriteria.NEW,
    "old": selector_service_models.SelectorCriteria.OLD,
    "modified": selector_service_models.SelectorCriteria.MODIFIED,
    "unmodified": selector_service_models.SelectorCriteria.UNMODIFIED,
    "modified.body": selector_service_models.SelectorCriteria.BODY,
    "modified.configs": selector_service_models.SelectorCriteria.CONFIGS,
    "modified.persisted_descriptions": selector_service_models.SelectorCriteria.PERSISTED_DESCRIPTIONS,
    "modified.relation": selector_service_models.SelectorCriteria.RELATION,
    "modified.macros": selector_service_models.SelectorCriteria.MACROS,
    "modified.contract": selector_service_models.SelectorCriteria.CONTRACT,
}


class GitSelectorMethod(SelectorMethod):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        git_client = kwargs.pop("git_client", None)
        super().__init__(*args, **kwargs)
        self._git_client = git_client or GitClient(".")

    def search(self, included_nodes: set[UniqueId], selector: str) -> t.Iterator[UniqueId]:
        modified_files = self._all_modified_files(selector)

        affected_macros = self._compute_affected_macros(modified_files)

        for unique_id, node in self.all_nodes(included_nodes):
            if self._is_source_node(node):
                continue

            if hasattr(node, "original_file_path"):
                node_path = Path(node.original_file_path).absolute()
                if node_path in modified_files:
                    yield unique_id
                    continue

            if self._node_depends_on_changed_macro(node, affected_macros):
                yield unique_id

    def _all_modified_files(self, target_branch: str) -> set[Path]:
        return {
            *self._git_client.list_untracked_files(),
            *self._git_client.list_uncommitted_changed_files(),
            *self._git_client.list_committed_changed_files(target_branch=target_branch),
        }

    def _compute_affected_macros(self, modified_files: set[Path]) -> set[str]:
        directly_modified, reverse_deps = self._analyze_macros(modified_files)
        affected_macros = set(directly_modified)
        queue = deque(directly_modified)

        while queue:
            macro_id = queue.popleft()
            for dependent_macro_id in reverse_deps.get(macro_id, set()):
                if dependent_macro_id not in affected_macros:
                    affected_macros.add(dependent_macro_id)
                    queue.append(dependent_macro_id)

        return affected_macros

    def _analyze_macros(self, modified_files: set[Path]) -> tuple[set[str], dict[str, set[str]]]:
        modified_macro_ids = set()
        reverse_deps: dict[str, set[str]] = defaultdict(set)

        for macro_id, macro in self.manifest.macros.items():
            if hasattr(macro, "original_file_path"):
                macro_path = Path(macro.original_file_path).absolute()
                if macro_path in modified_files:
                    modified_macro_ids.add(macro_id)

            if hasattr(macro, "depends_on"):
                for dep_macro_id in macro.depends_on.macros:
                    reverse_deps[dep_macro_id].add(macro_id)

        return modified_macro_ids, reverse_deps

    @staticmethod
    def _node_depends_on_changed_macro(node: t.Any, affected_macros: set[str]) -> bool:
        if not hasattr(node, "depends_on"):
            return False
        node_macro_deps = set(node.depends_on.macros)
        return bool(node_macro_deps & affected_macros)

    @staticmethod
    def _is_source_node(node: t.Any) -> bool:
        return hasattr(node, "resource_type") and node.resource_type == "source"


class StateSelector(StateSelectorMethod):
    def __init__(
        self,
        manifest: t.Any,
        previous_state: t.Any,
        arguments: t.List[str],
        runtime_config: RuntimeConfig,
        run_cache_config: RunCacheConfig,
        query_cache_client: QueryCacheGrpcClient,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(manifest, previous_state, arguments, **kwargs)
        self.runtime_config = runtime_config
        self.run_cache_config = run_cache_config
        self.query_cache_client = query_cache_client

    def _ensure_dependencies(self) -> None:
        """Ensure the selector was created with all required dependencies."""
        if self.run_cache_config is None:
            raise DbtRuntimeError(
                "State selector is not properly configured. "
                "Please ensure dbt-state plugin is enabled."
            )
        if self.query_cache_client is None:
            raise DbtRuntimeError(
                "State selector API client is not available. "
                "Please ensure dbt-state plugin is enabled and configured."
            )

    def search(self, included_nodes: set[UniqueId], selector: str) -> t.Iterator[UniqueId]:
        """Search for nodes matching the state selector criteria.

        Args:
            included_nodes: Set of node unique IDs to consider for selection.
            selector: The state selector criteria (e.g., "new", "modified", "modified.body").

        Yields:
            UniqueIds of nodes matching the selector criteria.

        Raises:
            DbtRuntimeError: If the project-id is not configured or selector is invalid.
        """
        # if the previous state is defined then fallback to old behavior
        if self.previous_state and self.previous_state.manifest:
            return super().search(included_nodes, selector)

        self._ensure_dependencies()

        if self.run_cache_config and self.run_cache_config.dbt_project_id is None:
            raise DbtRuntimeError(
                "To use the state:* selector, please define the 'project-id' field in your dbt_project.yml:\n\n"
                "dbt-cloud:\n"
                '  project-id: "your-project-id"\n\n'
            )

        if self.runtime_config and self.run_cache_config and self.query_cache_client:
            return self._execute_select(
                self.run_cache_config,
                self.runtime_config,
                self.query_cache_client,
                selector,
                included_nodes,
            )

        raise DbtRuntimeError(f"Context for state selector '{selector}' not set")

    def _execute_select(
        self,
        run_cache_config: RunCacheConfig,
        runtime_config: RuntimeConfig,
        query_cache_client: QueryCacheGrpcClient,
        selector: str,
        included_nodes: set[UniqueId],
    ) -> t.Iterator[UniqueId]:
        dbt_project_id = run_cache_config.dbt_project_id

        selector_criteria = _SELECTOR_CRITERIA_MAP.get(selector)
        if selector_criteria is None:
            raise DbtRuntimeError(
                f"Invalid state selector '{selector}'. "
                f"Valid selectors are: {', '.join(_SELECTOR_CRITERIA_MAP.keys())}"
            )

        target_name = run_cache_config.defer_to

        nodes = []
        for unique_id, node in self.all_nodes(included_nodes):
            if not isinstance(node, MODEL_OR_SNAPSHOT_OR_TEST_OR_SEED_NODE):
                continue

            calculator = create_node_hash_calculator(node, self.manifest, runtime_config)

            node_hash = calculator.calculate_node_hash()
            node_contract_hash = (
                calculator.node_contract_hash
                if isinstance(calculator, ModelNodeHashCalculator)
                else None
            )
            node_data = selector_service_models.DbtNodeData(
                node_unique_id=unique_id,
                node_hash=node_hash,
                node_body_hash=calculator.node_body_hash,
                node_configs_hash=calculator.node_configs_hash,
                node_persisted_descriptions_hash=calculator.node_persisted_docs_hash,
                node_macros_hash=calculator.node_macros_hash,
                node_contract_hash=node_contract_hash,
                node_database_representation=(
                    f"{node.database}.{node.schema}.{node.alias}"
                    if node.database and node.schema and node.alias
                    else None
                ),
            )
            nodes.append(node_data)

        request = selector_service_models.SelectorRequest(
            target=target_name,
            project_id=dbt_project_id,  # ty:ignore[invalid-argument-type]
            nodes=nodes,
            selector_criteria=selector_criteria,
        )
        response = query_cache_client.get_selection(request=request)

        for unique_id in response.node_unique_ids:
            yield UniqueId(unique_id)
