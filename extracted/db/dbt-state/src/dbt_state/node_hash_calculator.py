from abc import ABC, abstractmethod

import typing as t
import json
import hashlib
from collections import deque
from functools import cached_property

from dbt.contracts.graph.manifest import Manifest

from dbt_state._typing import ModelOrSnapshotOrTestNode

from dbt.contracts.graph.nodes import (
    GenericTestNode,
    ModelNode,
)

# Keys to exclude from the node config when calculating the hash.
# ref: https://docs.getdbt.com/reference/node-selection/methods?version=2.0&name=Fusion#state
_CONFIG_HASH_EXCLUDED_KEYS = frozenset({"alias", "schema", "database", "tags", "group"})


class NodeHashCalculator(ABC):
    """Base calculator with shared hash component methods."""

    def __init__(self, node: ModelOrSnapshotOrTestNode, manifest: Manifest):
        self.node = node
        self.manifest = manifest

    @abstractmethod
    def calculate_node_hash(self) -> str:
        """Subclasses define how to combine the components."""

    def _calculate_hash(self, *args: object) -> str:
        return hashlib.md5("".join(str(x) for x in args).encode()).hexdigest()

    @cached_property
    def node_body_hash(self) -> t.Optional[str]:
        raw_code = getattr(self.node, "raw_code", None)
        if not raw_code:
            return None
        return self._calculate_hash(raw_code)

    @cached_property
    def node_configs_hash(self) -> t.Optional[str]:
        unrendered_config = getattr(self.node, "unrendered_config", None)
        if not unrendered_config:
            return None
        filtered = {
            k: v for k, v in unrendered_config.items() if k not in _CONFIG_HASH_EXCLUDED_KEYS
        }
        return self._calculate_hash(json.dumps(filtered, sort_keys=True))

    @cached_property
    def node_persisted_docs_hash(self) -> t.Optional[str]:
        persist_docs = getattr(self.node.config, "persist_docs", None)
        if not persist_docs:
            return None

        parts: t.Dict[str, t.Any] = {}
        if persist_docs.get("relation"):
            parts["description"] = getattr(self.node, "description", "") or ""
        if persist_docs.get("columns"):
            columns = getattr(self.node, "columns", None) or {}
            parts["columns"] = {
                name: (col.description or "") for name, col in sorted(columns.items())
            }
        if not parts:
            return None
        return self._calculate_hash(json.dumps(parts, sort_keys=True))

    @cached_property
    def node_macros_hash(self) -> t.Optional[str]:
        depends_on_macros = getattr(self.node.depends_on, "macros", None)
        if not depends_on_macros:
            return None

        all_macros = self._get_all_macros()
        # Sort macro IDs to ensure deterministic ordering
        sorted_macro_ids = sorted(all_macros)
        macro_sqls = list()
        for macro_id in sorted_macro_ids:
            macro = self.manifest.macros.get(macro_id)
            if macro:
                macro_sqls.append(macro.macro_sql)

        return self._calculate_hash("".join(macro_sqls))

    def _get_all_macros(self) -> t.Set[str]:
        """
        Collect all macros that affect this node's rendering.

        This includes:
        1. Macros directly referenced by this node
        2. Macros referenced by those macros (recursively)

        This does NOT include macros from upstream nodes - each node's macro hash
        should only reflect the macros used to render that specific node.
        """
        visited_macros: t.Set[str] = set()
        all_macros: t.Set[str] = set(self.node.depends_on.macros)

        macro_queue: deque[str] = deque(all_macros)
        while macro_queue:
            macro_id = macro_queue.popleft()

            if macro_id in visited_macros:
                continue
            visited_macros.add(macro_id)

            macro = self.manifest.macros.get(macro_id)
            if macro:
                # Add all macros this macro depends on
                for dep_macro_id in macro.depends_on.macros:
                    all_macros.add(dep_macro_id)
                    if dep_macro_id not in visited_macros:
                        macro_queue.append(dep_macro_id)

        return all_macros


class DefaultNodeHashCalculator(NodeHashCalculator):
    """Default: SnapshotNode, SingularTestNode"""

    def calculate_node_hash(self) -> str:
        parts = [
            self.node_body_hash,
            self.node_configs_hash,
            self.node_persisted_docs_hash,
            self.node_macros_hash,
        ]
        return self._calculate_hash(*(p for p in parts if p is not None))


class ModelNodeHashCalculator(NodeHashCalculator):
    @cached_property
    def node_contract_hash(self) -> str:
        contract = getattr(self.node, "contract", None)
        enforced = bool(getattr(contract, "enforced", False))
        if enforced:
            build_contract_checksum = getattr(self.node, "build_contract_checksum", None)
            if callable(build_contract_checksum):
                build_contract_checksum()
            checksum = getattr(contract, "checksum", None)
            if checksum:
                contract_state = f"enforced:true|checksum:{checksum}"
            else:
                contract_state = "enforced:false"
        else:
            contract_state = "enforced:false"

        return self._calculate_hash(contract_state)

    @cached_property
    def node_ref_representation_hash(self) -> t.Optional[str]:
        if not hasattr(self.node, "latest_version"):
            return None
        parts = {
            "latest_version": getattr(self.node, "latest_version", None),
            "access": str(getattr(self.node, "access", None)),
            "deprecation_date": str(getattr(self.node, "deprecation_date", None)),
        }
        return self._calculate_hash(json.dumps(parts, sort_keys=True))

    def calculate_node_hash(self) -> str:
        parts = [
            self.node_body_hash,
            self.node_configs_hash,
            self.node_persisted_docs_hash,
            self.node_macros_hash,
            self.node_contract_hash,
            self.node_ref_representation_hash,
        ]
        return self._calculate_hash(*(p for p in parts if p is not None))


class GenericTestNodeCalculator(NodeHashCalculator):
    def calculate_node_hash(self) -> str:
        parts = [
            self.node_configs_hash,
        ]
        return self._calculate_hash(*(p for p in parts if p is not None))


def create_node_hash_calculator(
    node: ModelOrSnapshotOrTestNode, manifest: Manifest
) -> NodeHashCalculator:
    """Factory function to create the appropriate calculator for a node type."""
    if isinstance(node, ModelNode):
        return ModelNodeHashCalculator(node, manifest)
    if isinstance(node, GenericTestNode):
        return GenericTestNodeCalculator(node, manifest)
    return DefaultNodeHashCalculator(node, manifest)
