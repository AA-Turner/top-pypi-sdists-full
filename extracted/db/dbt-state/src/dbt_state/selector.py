from __future__ import annotations

import typing as t
from collections import defaultdict, deque
from pathlib import Path

from dbt.graph import UniqueId
from dbt.graph.selector_methods import SelectorMethod

from dbt_state.git import GitClient


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
