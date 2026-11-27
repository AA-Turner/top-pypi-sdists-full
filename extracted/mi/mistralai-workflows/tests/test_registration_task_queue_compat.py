from unittest.mock import AsyncMock

import pytest

from mistralai.workflows.core.worker import _get_workflow_definitions, _register_workflow_specs
from mistralai.workflows.worker_client import models as wc_models

from .fixtures import PureWorkflow, SimpleWorkflow


@pytest.mark.asyncio
async def test_registration_sends_the_deployment_name_as_task_queue_on_every_definition() -> None:
    client = AsyncMock()
    client.register_workflow_definitions_async.return_value = wc_models.WorkflowSpecsRegisterResponse(
        has_conflicts=False
    )
    definitions = _get_workflow_definitions([SimpleWorkflow, PureWorkflow], "dep-1")

    await _register_workflow_specs(client, definitions, "dep-1", "worker", None)

    request = client.register_workflow_definitions_async.call_args.kwargs
    assert request["deployment_name"] == "dep-1"
    sent = request["definitions"]
    assert [d.model_dump(by_alias=True)["task_queue"] for d in sent] == ["dep-1", "dep-1"]


@pytest.mark.asyncio
async def test_registration_omits_schedules() -> None:
    client = AsyncMock()
    client.register_workflow_definitions_async.return_value = wc_models.WorkflowSpecsRegisterResponse(
        has_conflicts=False
    )
    definitions = _get_workflow_definitions([SimpleWorkflow], "dep-1")

    await _register_workflow_specs(client, definitions, "dep-1", "worker", None)

    (sent,) = client.register_workflow_definitions_async.call_args.kwargs["definitions"]
    assert "schedules" not in sent.model_dump(by_alias=True)
