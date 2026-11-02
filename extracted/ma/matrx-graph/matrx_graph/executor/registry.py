from __future__ import annotations

from collections.abc import Callable

from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from matrx_graph.contract_kinds import (
    ContractDefinition,
    ContractDirection,
    ContractFamily,
    contract_from_model,
)
from matrx_graph.errors import NodeRegistryError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.node_spec import NodeSpec

# ── Legacy spec_type alias ───────────────────────────────────────────────────
# Registered-node spec_types were historically minted with an "action." prefix
# ("action.ai.agent.start"). The namespace was ERADICATED (Arman's ruling,
# 2026-08-08 — docs/workflow/NOMENCLATURE.md): the canonical spec_type is the
# bare dotted name ("ai.agent.start"). Stored workflow definitions, checkpoint
# replays, and seeds still carry the old spelling, so every registry lookup
# resolves the legacy prefix as an ALIAS. Stored definitions are NEVER
# rewritten; new registrations must never mint an "action."-prefixed type
# (guarded by scripts/check_action_namespace.py in the host repo).
LEGACY_SPEC_TYPE_PREFIX = "action."


#: A step type renamed to its Action's name (``declare_action(former_step_names=...)``):
#: stored definitions keep the old spelling, and every lookup resolves it here.
_RENAMED_SPEC_TYPES: dict[str, str] = {}


def alias_spec_type(former: str, current: str) -> None:
    """Make a former step type resolve to ``current``. Idempotent; one target per name."""
    held = _RENAMED_SPEC_TYPES.get(former)
    if held is not None and held != current:
        raise NodeRegistryError(f"Step type {former!r} already resolves to {held!r}, not {current!r}.")
    _RENAMED_SPEC_TYPES[former] = current


def canonical_spec_type(spec_type: str) -> str:
    """Resolve a possibly legacy-prefixed or renamed spec_type to its canonical form."""
    if spec_type.startswith(LEGACY_SPEC_TYPE_PREFIX):
        spec_type = spec_type[len(LEGACY_SPEC_TYPE_PREFIX) :]
    return _RENAMED_SPEC_TYPES.get(spec_type, spec_type)


@runtime_checkable
class NodeExecutor(Protocol):
    """Protocol for executing a single node type.

    An executor is registered once (per process or per workflow host) and looked
    up by the scheduler via the `spec.node_type` identifier. Executors are
    stateless across invocations; per-invocation state lives in `ctx`.

    The `inputs` arg is a typed instance of `spec.input_schema`, constructed by
    the scheduler from upstream edge payloads. The `config` arg is a typed
    instance of `spec.config_schema`, resolved from the NodeDef's authored
    config at compile time. The return value is a typed instance of
    `spec.output_schema`, which the scheduler places on all DATA edges leaving
    this node.

    Side effects the executor may perform during execute():
        - ctx.channels.write(name, value) to update channel state
        - ctx.send(target_node_id, payload) to emit Send directives
        - ctx.interrupt(payload) to pause the run and surface to the UI
        - ctx.emitter.send_chunk / send_data / ... to stream progress

    Raise an exception to mark the node as failed — the scheduler routes
    failure along any outgoing ERROR edges.
    """

    spec: NodeSpec

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: BaseModel,
        config: BaseModel,
    ) -> BaseModel: ...


class NodeRegistry:
    """Holds the executor for each node type the engine can run.

    The engine exposes a module-level default registry via
    `matrx_graph.executor.registry.default_registry()`. Sibling packages
    (`matrx-ai`, `matrx-scraper`) register their node executors against this
    default registry at import time via their own `register_with_graph()`
    helpers — this is the runtime-inversion seam that keeps matrx-graph free
    of hard dependencies on AI or scraper packages.

    Tests construct their own registry instances to avoid global mutation.
    """

    def __init__(self) -> None:
        self._executors: dict[str, NodeExecutor] = {}
        self._bootstrap: Callable[[], None] | None = None
        self._bootstrapping = False

    def set_bootstrap(self, fn: Callable[[], None] | None) -> None:
        """Install the host's one-shot "register every node type" call.

        ``compile_graph`` runs it (via :meth:`ensure_bootstrapped`) before
        validating, so a process that never imported the host's app boot
        still resolves every node type instead of failing with ``Unknown
        node type``. The host's call must be idempotent.
        """
        self._bootstrap = fn

    def ensure_bootstrapped(self) -> None:
        fn = self._bootstrap
        if fn is None or self._bootstrapping:
            return
        self._bootstrapping = True  # re-entrancy guard: the bootstrap may compile
        try:
            fn()
        finally:
            self._bootstrapping = False

    @staticmethod
    def _contract_family(executor: NodeExecutor) -> ContractFamily:
        # Nodes registered through the @register_node decorator carry a
        # `contract_family` attribute ("action_io" — the contract-slug family
        # name is a separate, untouched namespace; see contract_kinds.py).
        # Everything else (builtins) is WORKFLOW_IO.
        family = getattr(executor, "contract_family", None)
        if family is None:
            return ContractFamily.WORKFLOW_IO
        try:
            return ContractFamily(family)
        except ValueError:
            return ContractFamily.WORKFLOW_IO

    def register(self, executor: NodeExecutor, *, overwrite: bool = False) -> None:
        # AUTO-MINT IS DEAD (Arman, 2026-08-20 — plan of record
        # KINDS_EVERYWHERE_PLAN.md §2, §12; the audit's break #2). This method
        # used to rewrite an undeclared (or "json") spec with a machine-minted
        # fingerprint slug, so every node READ as kind-compliant while holding
        # only a type signature — "we invent one that reads as compliant and
        # can never render". Now a spec's declaration is exactly what its
        # author wrote: None stays None (and settlement's runtime propagation
        # reads the payload's own __kind instead — the honest answer for
        # pass-throughs), a real slug stays a real slug. The fingerprint ABI
        # capture is NOT lost: ``content_ir_contracts()`` still derives the
        # exact I/O contracts for the drift-detection publisher — contracts
        # simply no longer masquerade as declarations.
        node_type = executor.spec.node_type
        if not overwrite and node_type in self._executors:
            existing = type(self._executors[node_type]).__name__
            new = type(executor).__name__
            raise NodeRegistryError(
                f"Node type '{node_type}' is already registered by "
                f"{existing}; pass overwrite=True to replace (was: {new})."
            )
        self._executors[node_type] = executor

    def unregister(self, node_type: str) -> None:
        self._executors.pop(canonical_spec_type(node_type), None)

    def get(self, node_type: str) -> NodeExecutor:
        # Exact match first; then the legacy "action." alias so stored
        # definitions / checkpoints keep resolving byte-identically.
        executor = self._executors.get(node_type) or self._executors.get(
            canonical_spec_type(node_type)
        )
        if executor is None:
            known = sorted(self._executors)
            raise NodeRegistryError(
                f"No executor registered for node type '{node_type}'. Known types: {known!r}."
            )
        return executor

    def has(self, node_type: str) -> bool:
        return node_type in self._executors or canonical_spec_type(node_type) in self._executors

    def all_specs(self) -> list[NodeSpec]:
        return [e.spec for e in self._executors.values()]

    def all_types(self) -> list[str]:
        return list(self._executors)

    def palette(self) -> list[dict[str, object]]:
        return [s.to_palette_descriptor() for s in self.all_specs()]

    def content_ir_contracts(self) -> list[ContractDefinition]:
        """Return publisher-ready exact I/O contracts for every node."""
        contracts = []
        for executor in self._executors.values():
            spec = executor.spec
            family = self._contract_family(executor)
            contracts.append(
                contract_from_model(
                    family=family,
                    source_name=spec.node_type,
                    direction=ContractDirection.INPUT,
                    model=spec.input_schema,
                    source_id=spec.node_type,
                )
            )
            if not spec.dynamic_output:
                contracts.append(
                    contract_from_model(
                        family=family,
                        source_name=spec.node_type,
                        direction=ContractDirection.OUTPUT,
                        model=spec.output_schema,
                        source_id=spec.node_type,
                    )
                )
        return contracts

    def clear(self) -> None:
        self._executors.clear()

    def assert_types_present(self, expected: set[str] | list[str] | tuple[str, ...]) -> None:
        """Raise if any expected node type isn't registered.

        Host applications call this at startup with the union of node
        types their product uses (built-ins + matrx-ai's graph_nodes +
        any local action packs). A missing type means an upstream
        ``register_with_graph()`` call failed — likely a transient
        import error during boot — and the host's first workflow run
        would die mid-flight with a confusing "no executor for X"
        message. Failing fast here surfaces the issue at boot instead.

        Wraps :class:`NodeRegistryError` so callers can catch the same
        exception class they get from ``get()``.
        """
        missing = sorted(t for t in expected if not self.has(t))
        if missing:
            known = sorted(self._executors)
            raise NodeRegistryError(
                f"Required node types are not registered: {missing!r}. "
                f"Registered types: {known!r}. Check that the package's "
                f"register_with_graph() ran successfully at startup."
            )


_default_registry = NodeRegistry()


def default_registry() -> NodeRegistry:
    return _default_registry


def register(executor: NodeExecutor, *, overwrite: bool = False) -> None:
    _default_registry.register(executor, overwrite=overwrite)


def assert_node_types_present(
    expected: set[str] | list[str] | tuple[str, ...],
) -> None:
    """Module-level convenience for the default registry. See
    :meth:`NodeRegistry.assert_types_present`."""
    _default_registry.assert_types_present(expected)
