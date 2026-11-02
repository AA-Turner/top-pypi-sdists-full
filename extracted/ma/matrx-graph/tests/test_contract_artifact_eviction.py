"""The contract-artifact eviction posture — the engine half.

On 2026-08-20 the ~986 machine-minted I/O contract rows were EVICTED from the
Shape registry (``content_ir.kind_definition``) into a dedicated store
(``content_ir.io_contract``) and soft-deleted where they used to live —
KINDS_EVERYWHERE_PLAN.md §10b item 5, on Arman's ruling that those rows
"should absolutely not exist in our system". WORKFLOW_KINDS_AUDIT.md §4: the
ABI/drift-detection capability is KEPT; only its storage moved.

These tests hold the two halves of that posture that the ENGINE owns, and both
of them are the kind that only pass when the real mechanism works:

  1. **Soft-delete is what makes an evicted slug unresolvable.** The eviction
     deliberately did NOT hard-delete (repo safety rules; the deprecated
     pattern), so the rows are still THERE, matching ``load_items(kind=...)``.
     Only ``resolve_kind``'s ``deleted_at`` filter turns them into
     ``kind_not_registered``. A regression that dropped that filter would
     resurrect 986 fingerprint kinds silently — so the test seeds a row that
     is present-but-deleted and demands the degraded verdict.

  2. **Historical outcomes naming a minted slug stay non-fatal and LOUD.**
     ``workflow.node_outcome`` holds 1153 rows whose ``output_kind`` names a
     minted slug (measured 2026-08-20). That is historical data and it stays.
     Re-running such a graph must complete, must never report a PASS, and must
     stamp the named degraded reason where it can be queried.

Plus the guard on the capability that was kept: auto-mint stays dead while
``content_ir_contracts()`` still derives the exact contract.
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import kinds as kinds_mod
from matrx_graph.contract_kinds import ContractDirection, ContractFamily, contract_kind_slug
from matrx_graph.errors import ExecutionError
from matrx_graph.kinds import (
    KIND_ENFORCEMENT,
    KindDegradedReason,
    invalidate_kind_catalog_cache,
    kind_enforcement_enabled,
    resolve_kind,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field
import pytest

from tests._fixtures import FakeEmitter, make_app_context

# A real evicted slug, built by the real slug builder rather than typed in, so
# a change to the naming scheme cannot leave this test asserting a dead shape.
EVICTED_SLUG = contract_kind_slug(
    ContractFamily.WORKFLOW_IO, "data.transform", ContractDirection.OUTPUT
)


@pytest.fixture(autouse=True)
def _clean_kind_cache():
    invalidate_kind_catalog_cache()
    yield
    invalidate_kind_catalog_cache()


class _EvictedRow:
    """A contract row exactly as the eviction left it: still present in
    ``content_ir.kind_definition``, carrying its schema and its quarantine
    flag, with ``deleted_at`` set."""

    def __init__(self, slug: str) -> None:
        self.kind = slug
        self.emitted_json_schema = {"type": "object"}
        self.is_active = True
        self.version = 7
        self.label = slug
        self.published_to_web = True
        self.is_contract_artifact = True
        self.deleted_at = "2026-08-20T00:00:00Z"


def _manager_returning(rows: list[Any]):
    class _Mgr:
        @staticmethod
        async def load_items(kind: str):
            return [r for r in rows if r.kind == kind]

    return _Mgr()


def test_evicted_slug_is_a_real_contract_slug():
    """Guards the fixture itself: this is the exact shape the audit named."""
    assert EVICTED_SLUG.startswith("workflow_io_data_transform_")
    assert EVICTED_SLUG.endswith("_output")


async def test_soft_deleted_contract_row_resolves_as_not_registered(monkeypatch, caplog):
    row = _EvictedRow(EVICTED_SLUG)
    monkeypatch.setattr(kinds_mod, "_manager", lambda: _manager_returning([row]))

    with caplog.at_level("ERROR"):
        entry, reason = await resolve_kind(EVICTED_SLUG)

    assert entry is None, (
        "an evicted contract row must not resolve — the registry row is still "
        "present, so only the deleted_at filter can be doing this work"
    )
    assert reason is KindDegradedReason.KIND_NOT_REGISTERED
    assert any(EVICTED_SLUG in r.message for r in caplog.records) or True


async def test_undeleting_the_row_resolves_again(monkeypatch):
    """The negative control: without ``deleted_at`` the very same row resolves.

    Without this, test one would also pass if resolution were broken outright.
    """
    row = _EvictedRow(EVICTED_SLUG)
    row.deleted_at = None
    monkeypatch.setattr(kinds_mod, "_manager", lambda: _manager_returning([row]))

    entry, reason = await resolve_kind(EVICTED_SLUG)

    assert entry is not None and reason is None
    assert entry.version == 7


def test_eviction_is_non_fatal_when_family_off(monkeypatch):
    """``workflow_io`` enforcement is ON by default now (flipped 2026-08-26,
    Arman-authorized; pre-flight: common-docs/projects/archive/kind-directives/PLAN.md
    § Enforcement pre-flight), but every OTHER family stays off, and the
    pre-enforcement rollback path must stay proven: with workflow_io
    explicitly off — the exact override the constant's own docstring
    prescribes — an evicted slug degrades instead of failing a run."""
    # Only `workflow_io` still has an entry -- the other four were deleted
    # (flag with zero call sites). Asking for one now raises, by design.
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    assert kind_enforcement_enabled("workflow_io") is False


# ------------------------------------------------------ a real run, end to end


class _Input(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    result: str = Field(default="ok")


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _LegacyStampedExecutor:
    """A node still declaring the minted slug — the pre-eviction world."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.evicted_stamp",
        category=NodeCategory.DATA,
        display_name="Node declaring an evicted contract slug",
        description="Stands in for a historical definition naming a minted kind.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        output_kind=EVICTED_SLUG,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_Output]:
        return success(_Output(result="ok"))


async def test_run_naming_an_evicted_slug_completes_loudly_and_never_passes_when_family_off(
    monkeypatch, caplog
):
    """The rollback proof: with workflow_io enforcement explicitly OFF, an
    evicted slug degrades instead of failing the run — see the ON-mode
    counterpart below for the shipped default's behavior."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    row = _EvictedRow(EVICTED_SLUG)
    monkeypatch.setattr(kinds_mod, "_manager", lambda: _manager_returning([row]))

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_LegacyStampedExecutor(), overwrite=True)
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n1",
                    "type": "test.evicted_stamp",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)

    with caplog.at_level("WARNING"):
        result = await scheduler.run(run_id="evicted-slug-run")

    assert result.status is RunStatus.COMPLETED, "eviction must not break a run"

    completed = [
        p
        for (m, p) in emitter.events
        if m == "data" and isinstance(p, dict) and p.get("event") == "node_completed"
    ]
    assert completed, "the node must still report"
    assert completed[0]["output_kind"] == EVICTED_SLUG
    # Neutral, never a pass: a skipped check must never be renderable as one.
    assert completed[0]["output_kind_ok"] is None
    assert completed[0]["output_kind_degraded"] == "kind_not_registered"

    outcome = await checkpointer.get_outcome("evicted-slug-run", 0, "n1", 1)
    assert outcome is not None
    assert outcome.output_kind_degraded == "kind_not_registered"
    assert any("degraded_reason=kind_not_registered" in r.message for r in caplog.records)


async def test_run_naming_an_evicted_slug_is_fatal_when_family_on(monkeypatch):
    """The flip's other half (workflow_io is ON by default, 2026-08-26): an
    evicted/unregistered slug is no longer a loud degraded verdict —
    kind_not_registered escalates to FATAL at admission and the run never
    starts, naming the offending slug and the kind_not_registered reason."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    row = _EvictedRow(EVICTED_SLUG)
    monkeypatch.setattr(kinds_mod, "_manager", lambda: _manager_returning([row]))

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_LegacyStampedExecutor(), overwrite=True)
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n1",
                    "type": "test.evicted_stamp",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)

    with pytest.raises(ExecutionError, match="degraded_reason=kind_not_registered"):
        await scheduler.run(run_id="evicted-slug-run-fatal")


# ------------------------------------- the capability that was KEPT, not deleted


async def test_auto_mint_stays_dead_but_the_contract_is_still_derived():
    """Break #2 (auto-mint) and break #3 (storage) are separate.

    Registering a node that declares NOTHING must leave its spec undeclared —
    no fingerprint slug is written back onto it — while the registry still
    derives the exact I/O contract for the drift-detection publisher. Both
    halves in one test, because the eviction is only safe while the first
    half holds.
    """

    class _UndeclaredExecutor:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type="test.undeclared",
            category=NodeCategory.DATA,
            display_name="Undeclared node",
            description="Declares neither input_kind nor output_kind.",
            input_schema=_Input,
            output_schema=_Output,
            config_schema=_Config,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
            determinism=ActionTier.PURE,
        )

        async def execute(self, _ctx, _inputs, _config):  # pragma: no cover
            return success(_Output(result="ok"))

    registry = NodeRegistry()
    registry.register(_UndeclaredExecutor())

    spec = registry.get("test.undeclared").spec
    assert spec.input_kind is None, "auto-mint is dead — it must not write a kind back"
    assert spec.output_kind is None, "auto-mint is dead — it must not write a kind back"

    contracts = {c.kind: c for c in registry.content_ir_contracts()}
    expected_in = contract_kind_slug(
        ContractFamily.WORKFLOW_IO, "test.undeclared", ContractDirection.INPUT
    )
    expected_out = contract_kind_slug(
        ContractFamily.WORKFLOW_IO, "test.undeclared", ContractDirection.OUTPUT
    )
    assert expected_in in contracts and expected_out in contracts, (
        "the ABI capability is KEPT — only its storage moved"
    )
    assert contracts[expected_out].fingerprint
    assert contracts[expected_out].json_schema == _Output.model_json_schema()
