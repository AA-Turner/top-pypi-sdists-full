from typing import Any

import pytest
from temporalio.testing import WorkflowEnvironment

import mistralai.workflows  # noqa: F401  # imports every SDK module that registers an activity
from mistralai.workflows import get_workflow_definition
from mistralai.workflows.core.activity import get_all_temporal_activities
from mistralai.workflows.core.config.config import INTERNAL_ACTIVITY_PREFIX
from mistralai.workflows.testing import create_test_worker, get_internal_activities

from .fixtures import SimpleWorkflow, say_hello


def _name(activity_fn: Any) -> str:
    return str(activity_fn.__temporal_activity_definition.name)


def test_internal_activities_include_every_sdk_activity_with_a_reserved_name() -> None:
    sdk_internal = {
        _name(a)
        for a in get_all_temporal_activities()
        if a.__module__.startswith("mistralai.workflows.core.") and _name(a).startswith("__")
    }

    assert sdk_internal
    assert sdk_internal <= {_name(a) for a in get_internal_activities()}


def test_internal_activities_use_internal_names() -> None:
    names = [_name(a) for a in get_internal_activities()]

    assert len(names) == len(set(names))
    assert all(name.startswith("__") for name in names), names
    assert any(name.startswith(INTERNAL_ACTIVITY_PREFIX) for name in names)


@pytest.mark.asyncio
async def test_test_worker_accepts_internal_activities_it_already_registers(temporal_env: WorkflowEnvironment) -> None:
    activities = [say_hello, *get_internal_activities()]

    async with create_test_worker(temporal_env, workflows=[SimpleWorkflow], activities=activities):
        workflow_def = get_workflow_definition(SimpleWorkflow)
        assert workflow_def is not None
        result = await temporal_env.client.execute_workflow(
            workflow_def.name, {"name": "Alice"}, id="test-internal-activities", task_queue="test-task-queue"
        )

    assert result
