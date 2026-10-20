import hashlib
import json
import os
import typing as t
from abc import ABC, abstractmethod
from collections import deque
from functools import cached_property
from pathlib import Path

import jinja2
from dbt.config.runtime import RuntimeConfig
from dbt.context.providers import RuntimeVar
from dbt.contracts.files import SourceFile
from dbt.contracts.graph.manifest import Manifest
from dbt.contracts.graph.nodes import (
    GenericTestNode,
    ModelNode,
    SeedNode,
)
from jinja2 import nodes as jinja_nodes

from dbt_state._typing import ModelOrSnapshotOrTestOrSeedNode

try:
    from dbt_common.clients.jinja import get_environment
    from dbt_common.context import get_invocation_context
except ImportError:
    # dbt 1.7: no dbt_common; jinja lives in dbt and env vars come from os.environ
    from dbt.clients.jinja import get_environment  # type: ignore[no-redef]

    get_invocation_context = None  # type: ignore[assignment]

_HASH_READ_CHUNK_SIZE = 64 * 1024

# Keys to exclude from the node config when calculating the hash.
# ref: https://docs.getdbt.com/reference/node-selection/methods?version=2.0&name=Fusion#state
_CONFIG_HASH_EXCLUDED_KEYS = frozenset({"alias", "schema", "database", "tags", "group"})


def _calculate_hash(*args: object) -> str:
    return hashlib.md5("".join(str(x) for x in args).encode()).hexdigest()


# Reserved key; cannot clash with a real dbt config key.
_RUNTIME_VARS_KEY = "__runtime_vars__"
_VAR_FUNCTIONS = frozenset({"var", "env_var"})


def _extract_var_calls(sources: t.Iterable[str]) -> t.Tuple[t.Set[str], t.Set[str]]:
    """Return the literal names passed to `var()` and `env_var()` in the Jinja sources.

    Sources that fail to parse are skipped, and calls with a dynamic name are ignored.
    """
    var_names: t.Set[str] = set()
    env_var_names: t.Set[str] = set()
    env = get_environment()
    for source in sources:
        try:
            ast = env.parse(source)
        except jinja2.TemplateSyntaxError:
            continue
        for call in ast.find_all(jinja_nodes.Call):
            func = call.node
            if not isinstance(func, jinja_nodes.Name) or func.name not in _VAR_FUNCTIONS:
                continue
            if not call.args or not isinstance(call.args[0], jinja_nodes.Const):
                continue
            name = call.args[0].value
            if not isinstance(name, str):
                continue
            (var_names if func.name == "var" else env_var_names).add(name)
    return var_names, env_var_names


class NodeHashCalculator(ABC):
    """Base calculator with shared hash component methods."""

    def __init__(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        manifest: Manifest,
        config: RuntimeConfig,
        *,
        include_runtime_vars: bool = False,
    ) -> None:
        self.node = node
        self.manifest = manifest
        self._config = config
        self._include_runtime_vars = include_runtime_vars

    def get_base_hash_parts(self) -> t.List[t.Any]:
        """Return the common hash parts used by most node types."""
        return [
            self.node_body_hash,
            self.node_configs_hash,
            self.node_persisted_docs_hash,
            self.node_macros_hash,
            ".".join(self.node.fqn),
        ]

    @abstractmethod
    def calculate_node_hash(self) -> str:
        """Subclasses define how to combine the components."""

    @cached_property
    def node_body_hash(self) -> t.Optional[str]:
        raw_code = getattr(self.node, "raw_code", None)
        if not raw_code:
            return None
        return _calculate_hash(raw_code)

    @cached_property
    def node_configs_hash(self) -> t.Optional[str]:
        unrendered_config = getattr(self.node, "unrendered_config", None)
        runtime_vars = self.node_runtime_vars if self._include_runtime_vars else None
        if not unrendered_config and runtime_vars is None:
            return None
        filtered: t.Dict[str, t.Any] = {
            k: v
            for k, v in (unrendered_config or {}).items()
            if k not in _CONFIG_HASH_EXCLUDED_KEYS
        }
        if runtime_vars is not None:
            filtered[_RUNTIME_VARS_KEY] = runtime_vars
        return _calculate_hash(json.dumps(filtered, sort_keys=True, default=str))

    @cached_property
    def node_runtime_vars(self) -> t.Optional[t.Dict[str, t.Dict[str, t.Any]]]:
        """Values of the `var()` / `env_var()` calls used by the node's code, configs and macros.

        Returns None when the node uses none. Only folded into `node_configs_hash` when
        `include_runtime_vars` is set.
        """
        sources: t.List[str] = []
        raw_code = getattr(self.node, "raw_code", None)
        if isinstance(raw_code, str) and raw_code:
            sources.append(raw_code)
        unrendered_config = getattr(self.node, "unrendered_config", None)
        if unrendered_config:
            pending: t.List[t.Any] = list(unrendered_config.values())
            while pending:
                value = pending.pop()
                if isinstance(value, str):
                    sources.append(value)
                elif isinstance(value, dict):
                    pending.extend(value.values())
                elif isinstance(value, (list, tuple)):
                    pending.extend(value)
        for macro_id in self._get_all_macros():
            macro = self.manifest.macros.get(macro_id)
            if macro:
                sources.append(macro.macro_sql)

        var_names, env_var_names = _extract_var_calls(sources)

        file_id = getattr(self.node, "file_id", None)
        source_file = self.manifest.files.get(file_id) if file_id else None
        if isinstance(source_file, SourceFile):
            env_var_names.update(source_file.env_vars)

        if not var_names and not env_var_names:
            return None

        run_var = RuntimeVar(context={}, config=self._config, node=self.node)
        vars_values = {
            name: run_var._merged[name]  # noqa: SLF001
            for name in sorted(var_names)
            if run_var.has_var(name)
        }
        env = get_invocation_context().env if get_invocation_context else os.environ
        env_values = {name: env.get(name) for name in sorted(env_var_names)}
        return {"vars": vars_values, "env_vars": env_values}

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
        return _calculate_hash(json.dumps(parts, sort_keys=True))

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

        return _calculate_hash("".join(macro_sqls))

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
        parts = self.get_base_hash_parts()
        return _calculate_hash(*(p for p in parts if p is not None))


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

        return _calculate_hash(contract_state)

    @cached_property
    def node_ref_representation_hash(self) -> t.Optional[str]:
        if not hasattr(self.node, "latest_version"):
            return None
        parts = {
            "latest_version": getattr(self.node, "latest_version", None),
            "access": str(getattr(self.node, "access", None)),
            "deprecation_date": str(getattr(self.node, "deprecation_date", None)),
        }
        return _calculate_hash(json.dumps(parts, sort_keys=True))

    def calculate_node_hash(self) -> str:
        parts = self.get_base_hash_parts()
        # Extend with model-specific parts
        parts.extend(
            [
                self.node_contract_hash,
                self.node_ref_representation_hash,
            ]
        )
        return _calculate_hash(*(p for p in parts if p is not None))


class GenericTestNodeCalculator(NodeHashCalculator):
    def calculate_node_hash(self) -> str:
        parts = [
            self.node_configs_hash,
            ".".join(self.node.fqn),
        ]
        return _calculate_hash(*(p for p in parts if p is not None))


class SeedNodeHashCalculator(NodeHashCalculator):
    @cached_property
    def node_body_hash(self) -> t.Optional[str]:
        seed_node = t.cast(SeedNode, self.node)
        if seed_node.root_path:
            seed_path = Path(seed_node.root_path) / seed_node.original_file_path
        else:
            seed_path = Path(self._config.project_root) / seed_node.original_file_path

        md5 = hashlib.md5(usedforsecurity=False)
        with open(seed_path, "rb") as f:
            for chunk in iter(lambda: f.read(_HASH_READ_CHUNK_SIZE), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def calculate_node_hash(self) -> str:
        return self.node_body_hash if self.node_body_hash is not None else ""


def create_node_hash_calculator(
    node: ModelOrSnapshotOrTestOrSeedNode,
    manifest: Manifest,
    config: RuntimeConfig,
    *,
    include_runtime_vars: bool = False,
) -> NodeHashCalculator:
    """Factory function to create the appropriate calculator for a node type."""
    kwargs = {"include_runtime_vars": include_runtime_vars}
    if isinstance(node, ModelNode):
        return ModelNodeHashCalculator(node, manifest, config, **kwargs)
    if isinstance(node, GenericTestNode):
        return GenericTestNodeCalculator(node, manifest, config, **kwargs)
    if isinstance(node, SeedNode):
        return SeedNodeHashCalculator(node, manifest, config, **kwargs)
    return DefaultNodeHashCalculator(node, manifest, config, **kwargs)
