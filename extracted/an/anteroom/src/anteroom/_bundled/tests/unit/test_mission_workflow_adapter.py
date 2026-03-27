"""Tests for WorkflowAdapter in mission_adapters (#1046)."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.mission_adapters import (
    _WORKFLOW_STATUS_MAP,
    WorkflowAdapter,
    create_default_adapter_registry,
)


@pytest.fixture()
def mock_db() -> MagicMock:
    return MagicMock()


@pytest.fixture()
def mock_engine() -> AsyncMock:
    engine = AsyncMock()
    engine.enqueue_run = AsyncMock(return_value={"id": "run-123"})
    return engine


@pytest.fixture()
def adapter(mock_db: MagicMock, mock_engine: AsyncMock) -> WorkflowAdapter:
    return WorkflowAdapter(db=mock_db, engine=mock_engine)


def _make_item(
    *,
    item_id: str = "item-1",
    workflow_path: str | None = "workflows/deploy.yaml",
    extra_inputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    adapter_config: dict[str, Any] = {}
    if workflow_path is not None:
        adapter_config["workflow_path"] = workflow_path
    if extra_inputs is not None:
        adapter_config["extra_inputs"] = extra_inputs
    return {"id": item_id, "adapter_config": adapter_config}


def _make_context(**kwargs: Any) -> dict[str, Any]:
    return kwargs


# ---------------------------------------------------------------------------
# create() tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("anteroom.services.workflow_engine.load_definition")
async def test_create_happy_path(
    mock_load: MagicMock,
    adapter: WorkflowAdapter,
    mock_engine: AsyncMock,
) -> None:
    mock_load.return_value = MagicMock(name="definition")
    item = _make_item()
    context = _make_context(spec_fqn="spec/foo", task_id="t-1", task_summary="do stuff")

    result = await adapter.create(item=item, context=context)

    assert result.state == "pending"
    assert result.adapter_ref == "run-123"
    mock_load.assert_called_once_with("workflows/deploy.yaml")
    mock_engine.enqueue_run.assert_awaited_once()
    call_kwargs = mock_engine.enqueue_run.call_args
    assert call_kwargs.kwargs["target_kind"] == "mission"
    assert call_kwargs.kwargs["target_ref"] == "item-1"
    assert call_kwargs.kwargs["inputs"]["spec_fqn"] == "spec/foo"
    assert call_kwargs.kwargs["inputs"]["task_id"] == "t-1"
    assert call_kwargs.kwargs["inputs"]["task_summary"] == "do stuff"


@pytest.mark.asyncio
async def test_create_missing_workflow_path(adapter: WorkflowAdapter) -> None:
    item = _make_item(workflow_path=None)
    result = await adapter.create(item=item, context={})

    assert result.state == "failed"
    assert "Missing workflow_path" in result.summary


@pytest.mark.asyncio
@patch("anteroom.services.workflow_engine.load_definition")
async def test_create_with_artifact_refs(
    mock_load: MagicMock,
    adapter: WorkflowAdapter,
    mock_engine: AsyncMock,
) -> None:
    mock_load.return_value = MagicMock()
    item = _make_item()
    context = _make_context(artifact_refs=["art-1", "art-2"])

    await adapter.create(item=item, context=context)

    inputs = mock_engine.enqueue_run.call_args.kwargs["inputs"]
    assert inputs["artifact_refs"] == ["art-1", "art-2"]


@pytest.mark.asyncio
@patch("anteroom.services.workflow_engine.load_definition")
async def test_create_with_full_scheduler_context(
    mock_load: MagicMock,
    adapter: WorkflowAdapter,
    mock_engine: AsyncMock,
) -> None:
    """Verify adapter correctly extracts all provenance fields from the context
    that the scheduler provides (spec_fqn, task_id, task_summary, artifact_refs)."""
    mock_load.return_value = MagicMock()
    item = _make_item()
    context = _make_context(
        session_id="sess-1",
        session={"id": "sess-1", "source_fqn": "@ns/spec/auth"},
        spec_fqn="@ns/spec/auth",
        task_id="t1",
        task_summary="Implement auth module",
        artifact_refs=[{"fqn": "@ns/spec/auth", "version": 2}],
    )

    result = await adapter.create(item=item, context=context)

    assert result.state == "pending"
    inputs = mock_engine.enqueue_run.call_args.kwargs["inputs"]
    assert inputs["spec_fqn"] == "@ns/spec/auth"
    assert inputs["task_id"] == "t1"
    assert inputs["task_summary"] == "Implement auth module"
    assert inputs["artifact_refs"] == [{"fqn": "@ns/spec/auth", "version": 2}]


@pytest.mark.asyncio
@patch("anteroom.services.workflow_engine.load_definition")
async def test_create_with_extra_inputs(
    mock_load: MagicMock,
    adapter: WorkflowAdapter,
    mock_engine: AsyncMock,
) -> None:
    mock_load.return_value = MagicMock()
    item = _make_item(extra_inputs={"region": "us-east-1"})

    await adapter.create(item=item, context={})

    inputs = mock_engine.enqueue_run.call_args.kwargs["inputs"]
    assert inputs["region"] == "us-east-1"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_engine.load_definition")
async def test_create_engine_raises(
    mock_load: MagicMock,
    adapter: WorkflowAdapter,
    mock_engine: AsyncMock,
) -> None:
    mock_load.return_value = MagicMock()
    mock_engine.enqueue_run.side_effect = RuntimeError("engine exploded")

    result = await adapter.create(item=_make_item(), context={})

    assert result.state == "failed"
    assert "engine exploded" in result.summary


# ---------------------------------------------------------------------------
# status() tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_pending(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = {"status": "pending", "stop_reason": None}
    result = await adapter.status(adapter_ref="run-1")
    assert result.state == "pending"
    assert result.adapter_ref == "run-1"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_running(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = {"status": "running", "stop_reason": None}
    result = await adapter.status(adapter_ref="run-1")
    assert result.state == "running"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_completed_with_stop_reason(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = {"status": "completed", "stop_reason": "all steps done"}
    result = await adapter.status(adapter_ref="run-1")
    assert result.state == "completed"
    assert result.summary == "all steps done"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_failed(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = {"status": "failed", "stop_reason": "step crashed"}
    result = await adapter.status(adapter_ref="run-1")
    assert result.state == "failed"
    assert result.summary == "step crashed"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_waiting_maps_to_running(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = {"status": "waiting_for_approval", "stop_reason": None}
    result = await adapter.status(adapter_ref="run-1")
    assert result.state == "running"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_claimed_maps_to_pending(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = {"status": "claimed", "stop_reason": None}
    result = await adapter.status(adapter_ref="run-1")
    assert result.state == "pending"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_unknown_defaults_to_running(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = {"status": "some_future_state", "stop_reason": None}
    result = await adapter.status(adapter_ref="run-1")
    assert result.state == "running"


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_status_run_not_found(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = None
    result = await adapter.status(adapter_ref="run-missing")
    assert result.state == "failed"
    assert "not found" in result.summary


# ---------------------------------------------------------------------------
# cancel() tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.create_workflow_event")
@patch("anteroom.services.workflow_storage.release_lock")
@patch("anteroom.services.workflow_storage.update_workflow_run")
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_cancel_from_pending(
    mock_get: MagicMock,
    mock_update: MagicMock,
    mock_release: MagicMock,
    mock_event: MagicMock,
    adapter: WorkflowAdapter,
) -> None:
    mock_get.return_value = {"status": "pending"}
    result = await adapter.cancel(adapter_ref="run-1")

    assert result.state == "cancelled"
    assert result.adapter_ref == "run-1"
    mock_update.assert_called_once_with(adapter._db, "run-1", status="cancelled")
    mock_release.assert_called_once_with(adapter._db, run_id="run-1")
    mock_event.assert_called_once_with(
        adapter._db,
        run_id="run-1",
        event_type="run_cancelled",
        payload={"source": "mission_adapter"},
    )


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.update_workflow_run")
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_cancel_from_non_cancellable_state(
    mock_get: MagicMock,
    mock_update: MagicMock,
    adapter: WorkflowAdapter,
) -> None:
    mock_get.return_value = {"status": "running"}
    result = await adapter.cancel(adapter_ref="run-1")

    assert result.state == "running"
    assert "Cannot cancel" in result.summary
    mock_update.assert_not_called()


@pytest.mark.asyncio
@patch("anteroom.services.workflow_storage.get_workflow_run")
async def test_cancel_run_not_found(mock_get: MagicMock, adapter: WorkflowAdapter) -> None:
    mock_get.return_value = None
    result = await adapter.cancel(adapter_ref="run-missing")
    assert result.state == "failed"
    assert "not found" in result.summary


# ---------------------------------------------------------------------------
# Registry factory tests
# ---------------------------------------------------------------------------


def test_registry_with_db_and_engine() -> None:
    registry = create_default_adapter_registry(db=MagicMock(), engine=AsyncMock())
    types = registry.list_types()
    assert "noop" in types
    assert "workflow" in types


def test_registry_without_db_engine() -> None:
    registry = create_default_adapter_registry()
    types = registry.list_types()
    assert "noop" in types
    assert "workflow" not in types


def test_workflow_status_map_covers_known_states() -> None:
    expected = {
        "pending",
        "claimed",
        "running",
        "paused",
        "completed",
        "failed",
        "cancelled",
        "blocked",
        "waiting_for_approval",
        "waiting_for_input",
    }
    assert set(_WORKFLOW_STATUS_MAP.keys()) == expected
