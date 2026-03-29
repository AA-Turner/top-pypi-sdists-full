"""Tests for mission_compiler — deterministic and LLM-assisted plan compilation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.db import init_db
from anteroom.services.mission_compiler import (
    AdapterDefaults,
    CompiledItem,
    CompiledPatch,
    CompiledPlan,
    PatchOperation,
    apply_adapter_defaults,
    apply_patch,
    apply_plan,
    compile_from_prompt,
    compile_from_spec,
    compile_patch,
)
from anteroom.services.mission_storage import (
    get_dependencies,
    get_session,
    list_items_by_session,
    list_revisions,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SPEC_YAML = """\
requirements: |
  Build the thing.
design: |
  Use modules.
tasks:
  - id: t1
    summary: Set up project
  - id: t2
    summary: Implement core
    depends_on: [t1]
  - id: t3
    summary: Write tests
    depends_on: [t1, t2]
"""


def _make_artifact(
    fqn: str = "test/spec/myspec",
    content: str = SPEC_YAML,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": "art-001",
        "fqn": fqn,
        "type": "spec",
        "namespace": "test",
        "name": "myspec",
        "content": content,
        "content_hash": "abc123",
        "source": "local",
        "metadata": metadata if metadata is not None else {"phases": {"tasks": {"status": "approved"}}},
        "version": 3,
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


# ---------------------------------------------------------------------------
# compile_from_spec
# ---------------------------------------------------------------------------


@patch("anteroom.services.mission_compiler.artifact_storage.get_artifact_by_fqn")
def test_compile_from_spec_basic(mock_get: Any) -> None:
    mock_get.return_value = _make_artifact()
    plan = compile_from_spec(None, "test/spec/myspec")  # type: ignore[arg-type]

    assert len(plan.items) == 3
    assert plan.items[0].temp_id == "t1"
    assert plan.items[0].summary == "Set up project"
    assert plan.items[1].depends_on == ["t1"]
    assert plan.items[2].depends_on == ["t1", "t2"]
    assert plan.title == "myspec"
    assert plan.referenced_artifacts == [{"fqn": "test/spec/myspec", "version": 3}]


@patch("anteroom.services.mission_compiler.artifact_storage.get_artifact_by_fqn")
def test_compile_from_spec_with_adapter_defaults(mock_get: Any) -> None:
    mock_get.return_value = _make_artifact()
    defaults = AdapterDefaults(adapter_type="agent", adapter_config={"model": "gpt-4"})
    plan = compile_from_spec(None, "test/spec/myspec", adapter_defaults=defaults)  # type: ignore[arg-type]

    for item in plan.items:
        assert item.adapter_type == "agent"
        assert item.adapter_config["model"] == "gpt-4"
        assert item.adapter_config["spec_fqn"] == "test/spec/myspec"
        assert "task_id" in item.adapter_config


@patch("anteroom.services.mission_compiler.artifact_storage.get_artifact_by_fqn")
def test_compile_from_spec_not_found(mock_get: Any) -> None:
    mock_get.return_value = None
    with pytest.raises(ValueError, match="not found"):
        compile_from_spec(None, "test/spec/missing")  # type: ignore[arg-type]


@patch("anteroom.services.mission_compiler.artifact_storage.get_artifact_by_fqn")
def test_compile_from_spec_no_tasks(mock_get: Any) -> None:
    yaml_no_tasks = "requirements: |\n  Req.\ndesign: |\n  Des.\ntasks: []\n"
    mock_get.return_value = _make_artifact(content=yaml_no_tasks)
    with pytest.raises(ValueError, match="no tasks"):
        compile_from_spec(None, "test/spec/empty")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# apply_adapter_defaults
# ---------------------------------------------------------------------------


def test_apply_adapter_defaults_overrides_noop() -> None:
    plan = CompiledPlan(
        items=[
            CompiledItem(summary="a", temp_id="t1", adapter_type="noop"),
            CompiledItem(summary="b", temp_id="t2", adapter_type="custom"),
        ]
    )
    defaults = AdapterDefaults(adapter_type="agent", adapter_config={"key": "val"})
    result = apply_adapter_defaults(plan, defaults)

    assert result.items[0].adapter_type == "agent"
    assert result.items[0].adapter_config["key"] == "val"
    assert result.items[1].adapter_type == "custom"
    assert result.items[1].adapter_config == {}


# ---------------------------------------------------------------------------
# compile_from_prompt
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_compile_from_prompt_valid_json() -> None:
    ai = AsyncMock()
    ai.complete.return_value = json.dumps(
        {
            "title": "Test Plan",
            "description": "A test",
            "items": [
                {"summary": "Task 1", "temp_id": "t1", "priority": 10},
                {"summary": "Task 2", "temp_id": "t2", "depends_on": ["t1"]},
            ],
        }
    )
    plan = await compile_from_prompt("build something", ai)

    assert plan.title == "Test Plan"
    assert len(plan.items) == 2
    assert plan.items[0].priority == 10
    assert plan.items[1].depends_on == ["t1"]


@pytest.mark.asyncio
async def test_compile_from_prompt_bad_json_fallback() -> None:
    ai = AsyncMock()
    ai.complete.return_value = "this is not json at all"
    plan = await compile_from_prompt("do the thing", ai)

    assert len(plan.items) == 1
    assert plan.items[0].summary == "do the thing"
    assert plan.items[0].temp_id == "item_0"


@pytest.mark.asyncio
async def test_compile_from_prompt_none_response_fallback() -> None:
    ai = AsyncMock()
    ai.complete.return_value = None
    plan = await compile_from_prompt("do the thing", ai)

    assert len(plan.items) == 1
    assert plan.items[0].summary == "do the thing"


@pytest.mark.asyncio
async def test_compile_from_prompt_with_adapter_defaults() -> None:
    ai = AsyncMock()
    ai.complete.return_value = json.dumps(
        {
            "title": "Plan",
            "items": [{"summary": "Task", "temp_id": "t1"}],
        }
    )
    defaults = AdapterDefaults(adapter_type="agent")
    plan = await compile_from_prompt("build", ai, adapter_defaults=defaults)

    assert plan.items[0].adapter_type == "agent"


@pytest.mark.asyncio
async def test_compile_from_prompt_markdown_fences() -> None:
    ai = AsyncMock()
    ai.complete.return_value = '```json\n{"title":"P","items":[{"summary":"A","temp_id":"t1"}]}\n```'
    plan = await compile_from_prompt("test", ai)

    assert len(plan.items) == 1
    assert plan.items[0].summary == "A"


# ---------------------------------------------------------------------------
# compile_patch
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_compile_patch_basic() -> None:
    ai = AsyncMock()
    ai.complete.return_value = json.dumps(
        {
            "operations": [
                {"op": "add_item", "payload": {"summary": "New", "temp_id": "n1"}},
                {"op": "drop_item", "target_item_id": "item-1"},
                {"op": "change_priority", "target_item_id": "item-2", "payload": {"priority": 10}},
            ]
        }
    )
    current = [
        {"id": "item-1", "status": "pending"},
        {"id": "item-2", "status": "pending"},
    ]
    result = await compile_patch("drop item-1, reprioritize item-2", current, ai)

    assert len(result.operations) == 3
    assert result.operations[0].op == "add_item"
    assert result.operations[1].op == "drop_item"
    assert result.operations[2].op == "change_priority"


@pytest.mark.asyncio
async def test_compile_patch_restricted_detection() -> None:
    ai = AsyncMock()
    ai.complete.return_value = json.dumps(
        {
            "operations": [
                {"op": "drop_item", "target_item_id": "item-active"},
            ]
        }
    )
    current = [
        {"id": "item-active", "status": "active"},
    ]
    result = await compile_patch("drop it", current, ai)

    assert result.operations[0].restricted is True


@pytest.mark.asyncio
async def test_compile_patch_invalid_json() -> None:
    ai = AsyncMock()
    ai.complete.return_value = "not json"
    result = await compile_patch("edit", [], ai)

    assert len(result.operations) == 0


@pytest.mark.asyncio
async def test_compile_patch_invalid_ops_filtered() -> None:
    ai = AsyncMock()
    ai.complete.return_value = json.dumps(
        {
            "operations": [
                {"op": "add_item", "payload": {"summary": "OK", "temp_id": "n1"}},
                {"op": "invalid_op", "target_item_id": "x"},
            ]
        }
    )
    result = await compile_patch("edit", [], ai)

    assert len(result.operations) == 1
    assert result.operations[0].op == "add_item"


# ---------------------------------------------------------------------------
# apply_plan (real DB)
# ---------------------------------------------------------------------------


def test_apply_plan_creates_session_and_items(db: Any) -> None:
    plan = CompiledPlan(
        items=[
            CompiledItem(summary="First", temp_id="t1", priority=10),
            CompiledItem(summary="Second", temp_id="t2", depends_on=["t1"]),
            CompiledItem(summary="Third", temp_id="t3", depends_on=["t1", "t2"]),
        ],
        title="Test Plan",
        referenced_artifacts=[{"fqn": "test/spec/x", "version": 1}],
    )
    session = apply_plan(db, plan, source_type="spec", source_fqn="test/spec/x", source_version=1)

    assert session["title"] == "Test Plan"
    items = list_items_by_session(db, session["id"])
    assert len(items) == 3
    assert items[0]["summary"] == "First"
    assert items[0]["priority"] == 10


def test_apply_plan_temp_id_mapping(db: Any) -> None:
    plan = CompiledPlan(
        items=[
            CompiledItem(summary="A", temp_id="t1"),
            CompiledItem(summary="B", temp_id="t2", depends_on=["t1"]),
        ],
    )
    session = apply_plan(db, plan)
    items = list_items_by_session(db, session["id"])

    item_map = {i["summary"]: i["id"] for i in items}
    deps_b = get_dependencies(db, item_map["B"])
    assert item_map["A"] in deps_b


def test_apply_plan_creates_revision(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="Solo", temp_id="t1")])
    session = apply_plan(db, plan)
    revisions = list_revisions(db, session["id"])

    assert len(revisions) == 1
    assert revisions[0]["revision_number"] == 1
    assert revisions[0]["reason"] == "initial plan"


def test_apply_plan_defaults_session_to_pending(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="Solo", temp_id="t1")])
    session = apply_plan(db, plan)

    persisted = get_session(db, session["id"])
    assert persisted is not None
    assert persisted["status"] == "pending"


def test_apply_plan_persists_active_session_when_requested(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="Solo", temp_id="t1")])
    session = apply_plan(db, plan, session_status="active")

    persisted = get_session(db, session["id"])
    assert persisted is not None
    assert persisted["status"] == "active"


# ---------------------------------------------------------------------------
# apply_patch (real DB)
# ---------------------------------------------------------------------------


def test_apply_patch_add_and_drop(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="Original", temp_id="t1")])
    session = apply_plan(db, plan)
    items_before = list_items_by_session(db, session["id"])
    original_id = items_before[0]["id"]

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(op="add_item", payload={"summary": "Added", "temp_id": "n1", "priority": 20}),
            PatchOperation(op="drop_item", target_item_id=original_id),
        ]
    )
    apply_patch(db, session["id"], patch_ops)

    items_after = list_items_by_session(db, session["id"])
    statuses = {i["summary"]: i["status"] for i in items_after}
    assert statuses["Added"] == "pending"
    assert statuses["Original"] == "dropped"


def test_apply_patch_restricted_raises(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="X", temp_id="t1")])
    session = apply_plan(db, plan)

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(op="drop_item", target_item_id="fake-id", restricted=True),
        ]
    )
    with pytest.raises(ValueError, match="active items"):
        apply_patch(db, session["id"], patch_ops)


def test_apply_patch_creates_revision(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="X", temp_id="t1")])
    session = apply_plan(db, plan)

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(op="add_item", payload={"summary": "New", "temp_id": "n1"}),
        ]
    )
    apply_patch(db, session["id"], patch_ops)

    revisions = list_revisions(db, session["id"])
    assert len(revisions) == 2
    assert revisions[1]["revision_number"] == 2
    assert revisions[1]["reason"] == "patch applied"


def test_apply_patch_session_not_found(db: Any) -> None:
    patch_ops = CompiledPatch(operations=[])
    with pytest.raises(ValueError, match="Session not found"):
        apply_patch(db, "nonexistent-id", patch_ops)


# ---------------------------------------------------------------------------
# Blocker fix: tasks phase approval gate
# ---------------------------------------------------------------------------


@patch("anteroom.services.mission_compiler.artifact_storage.get_artifact_by_fqn")
def test_compile_from_spec_rejects_unapproved_tasks(mock_get: Any) -> None:
    mock_get.return_value = _make_artifact(metadata={"phases": {"tasks": {"status": "draft"}}})
    with pytest.raises(ValueError, match="must be approved"):
        compile_from_spec(None, "test/spec/myspec")  # type: ignore[arg-type]


@patch("anteroom.services.mission_compiler.artifact_storage.get_artifact_by_fqn")
def test_compile_from_spec_rejects_stale_tasks(mock_get: Any) -> None:
    mock_get.return_value = _make_artifact(metadata={"phases": {"tasks": {"status": "stale"}}})
    with pytest.raises(ValueError, match="must be approved"):
        compile_from_spec(None, "test/spec/myspec")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Blocker fix: artifact_context carried into referenced_artifacts
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_compile_from_prompt_carries_artifact_context() -> None:
    ai = AsyncMock()
    ai.complete.return_value = json.dumps({"title": "Plan", "items": [{"summary": "A", "temp_id": "t1"}]})
    ctx = [{"fqn": "@ns/rule/sec", "version": 1}]
    plan = await compile_from_prompt("build", ai, artifact_context=ctx)

    assert {"fqn": "@ns/rule/sec", "version": 1} in plan.referenced_artifacts


@pytest.mark.asyncio
async def test_compile_patch_carries_artifact_context() -> None:
    ai = AsyncMock()
    ai.complete.return_value = json.dumps(
        {"operations": [{"op": "add_item", "payload": {"summary": "New", "temp_id": "n1"}}]}
    )
    ctx = [{"fqn": "@ns/rule/sec", "version": 2}]
    result = await compile_patch("add stuff", [], ai, artifact_context=ctx)

    assert {"fqn": "@ns/rule/sec", "version": 2} in result.referenced_artifacts


# ---------------------------------------------------------------------------
# Blocker fix: apply_patch two-pass and prevalidation
# ---------------------------------------------------------------------------


def test_apply_patch_two_new_items_with_interdep(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="Base", temp_id="t1")])
    session = apply_plan(db, plan)

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(op="add_item", payload={"summary": "New A", "temp_id": "na"}),
            PatchOperation(op="add_item", payload={"summary": "New B", "temp_id": "nb", "depends_on": ["na"]}),
        ]
    )
    apply_patch(db, session["id"], patch_ops)

    items = list_items_by_session(db, session["id"])
    item_map = {i["summary"]: i["id"] for i in items}
    deps_b = get_dependencies(db, item_map["New B"])
    assert item_map["New A"] in deps_b


def test_apply_patch_nonexistent_target_raises(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="X", temp_id="t1")])
    session = apply_plan(db, plan)

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(op="drop_item", target_item_id="nonexistent-item-id"),
        ]
    )
    with pytest.raises(ValueError, match="nonexistent item"):
        apply_patch(db, session["id"], patch_ops)


def test_apply_patch_add_item_bad_dep_prevalidated(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="X", temp_id="t1")])
    session = apply_plan(db, plan)

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(
                op="add_item",
                payload={"summary": "New", "temp_id": "n1", "depends_on": ["bogus-id"]},
            ),
        ]
    )
    with pytest.raises(ValueError, match="unknown item"):
        apply_patch(db, session["id"], patch_ops)

    # No items should have been created (prevalidation before mutation)
    items = list_items_by_session(db, session["id"])
    assert len(items) == 1  # only original


def test_apply_plan_rejects_cycle(db: Any) -> None:
    plan = CompiledPlan(
        items=[
            CompiledItem(summary="A", temp_id="t1", depends_on=["t2"]),
            CompiledItem(summary="B", temp_id="t2", depends_on=["t1"]),
        ]
    )
    with pytest.raises(ValueError, match="Circular dependency"):
        apply_plan(db, plan)


def test_apply_plan_rejects_self_dep(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="A", temp_id="t1", depends_on=["t1"])])
    with pytest.raises(ValueError, match="self-dependency"):
        apply_plan(db, plan)


def test_apply_patch_rejects_cycle(db: Any) -> None:
    plan = CompiledPlan(
        items=[
            CompiledItem(summary="A", temp_id="t1"),
            CompiledItem(summary="B", temp_id="t2"),
        ]
    )
    session = apply_plan(db, plan)
    items = list_items_by_session(db, session["id"])
    id_a = next(i["id"] for i in items if i["summary"] == "A")
    id_b = next(i["id"] for i in items if i["summary"] == "B")

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(op="change_dependencies", target_item_id=id_a, payload={"depends_on": [id_b]}),
            PatchOperation(op="change_dependencies", target_item_id=id_b, payload={"depends_on": [id_a]}),
        ]
    )
    with pytest.raises(ValueError, match="Circular dependency"):
        apply_patch(db, session["id"], patch_ops)


def test_apply_patch_change_deps_bad_ref_prevalidated(db: Any) -> None:
    plan = CompiledPlan(items=[CompiledItem(summary="X", temp_id="t1")])
    session = apply_plan(db, plan)
    items = list_items_by_session(db, session["id"])
    item_id = items[0]["id"]

    patch_ops = CompiledPatch(
        operations=[
            PatchOperation(
                op="change_dependencies",
                target_item_id=item_id,
                payload={"depends_on": ["bogus-id"]},
            ),
        ]
    )
    with pytest.raises(ValueError, match="unknown item"):
        apply_patch(db, session["id"], patch_ops)


# ---------------------------------------------------------------------------
# execution_profile integration
# ---------------------------------------------------------------------------


@patch("anteroom.services.mission_compiler.artifact_storage.get_artifact_by_fqn")
def test_compile_from_spec_with_execution_profile(mock_get: Any) -> None:
    from anteroom.services.mission_profiles import ExecutionProfile

    mock_get.return_value = _make_artifact()
    profile = ExecutionProfile(name="test", plan_first=True)

    with patch("anteroom.services.mission_profiles.discover_workflows", return_value=[]):
        plan = compile_from_spec(None, "test/spec/myspec", execution_profile=profile)  # type: ignore[arg-type]

    assert plan.execution_profile == "test"
    ids = [i.temp_id for i in plan.items]
    assert "_planning" in ids


@pytest.mark.asyncio
async def test_compile_from_prompt_with_execution_profile() -> None:
    from anteroom.services.mission_profiles import ExecutionProfile

    mock_ai = AsyncMock()
    mock_ai.complete.return_value = json.dumps(
        {
            "title": "Test",
            "items": [
                {"summary": "A", "temp_id": "a"},
                {"summary": "B", "temp_id": "b"},
            ],
        }
    )
    profile = ExecutionProfile(name="parallel", parallel_lanes=True, lane_limits={"default": 2})

    with patch("anteroom.services.mission_profiles.discover_workflows", return_value=[]):
        plan = await compile_from_prompt("do stuff", mock_ai, execution_profile=profile)

    assert plan.execution_profile == "parallel"
    lanes = [i.lane for i in plan.items if i.lane]
    assert len(lanes) >= 2


def test_compiled_item_binding_reason() -> None:
    item = CompiledItem(summary="test", temp_id="t1", binding_reason="test reason")
    assert item.binding_reason == "test reason"


def test_compiled_item_binding_reason_default() -> None:
    item = CompiledItem(summary="test", temp_id="t1")
    assert item.binding_reason == ""


def test_compiled_plan_execution_profile_default() -> None:
    plan = CompiledPlan(items=[])
    assert plan.execution_profile is None


def test_compiled_plan_execution_profile_set() -> None:
    plan = CompiledPlan(items=[], execution_profile="hands-off")
    assert plan.execution_profile == "hands-off"


def test_apply_plan_with_lane_limits(db: Any) -> None:
    plan = CompiledPlan(
        items=[CompiledItem(summary="A", temp_id="a")],
        title="Test",
        execution_profile="parallel-review",
    )
    session = apply_plan(db, plan, lane_limits={"default": 3})
    assert session["id"]
    # Verify session was created with lane_limits and metadata
    from anteroom.services.mission_storage import get_session

    s = get_session(db, session["id"])
    assert s is not None
    assert s.get("lane_limits") == {"default": 3}
    assert s.get("metadata", {}).get("execution_profile") == "parallel-review"


def test_apply_plan_hold_on_create(db: Any) -> None:
    """Items with _hold_on_create in adapter_config get hold_requested=True."""
    plan = CompiledPlan(
        items=[
            CompiledItem(summary="Work", temp_id="w1"),
            CompiledItem(
                summary="Review: Work",
                temp_id="r1",
                adapter_config={"_hold_on_create": True, "_binding_reason": "review gate"},
                depends_on=["w1"],
            ),
        ],
        title="Test",
    )
    session = apply_plan(db, plan)
    items = list_items_by_session(db, session["id"])
    review = [i for i in items if i["summary"] == "Review: Work"][0]
    assert review["hold_requested"] == 1  # SQLite stores bool as int
