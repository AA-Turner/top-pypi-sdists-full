from __future__ import annotations

import pytest
from temporalio.converter import DataConverter

from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs
from mistralai.workflows.testing import create_test_worker

_captured_run_as: list[ConnectorRunAs] = []


@activity(name="test-echo-run-as", _skip_registering=True)
async def _echo_run_as(run_as: ConnectorRunAs = ConnectorRunAs.AUTO) -> str:
    _captured_run_as.append(run_as)
    return run_as.value


@workflow.define(name="test-run-as-boundary")
class _RunAsBoundaryWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await _echo_run_as(run_as=ConnectorRunAs.DEPLOYMENT)


class TestConnectorRunAsSurvivesActivityBoundary:
    @pytest.mark.asyncio
    async def test_run_as_survives_payload_converter_round_trip(self, temporal_env) -> None:
        _captured_run_as.clear()
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        original_client = temporal_env.client
        temporal_env._client = custom_client  # type: ignore[attr-defined]
        try:
            async with create_test_worker(
                temporal_env,
                workflows=[_RunAsBoundaryWorkflow],
                activities=[_echo_run_as],
            ):
                handle = await custom_client.start_workflow(
                    "test-run-as-boundary",
                    id="test-run-as-boundary",
                    task_queue="test-task-queue",
                )
                await handle.result()
        finally:
            temporal_env._client = original_client  # type: ignore[attr-defined]

        assert _captured_run_as == [ConnectorRunAs.DEPLOYMENT]
        assert isinstance(_captured_run_as[0], ConnectorRunAs)
