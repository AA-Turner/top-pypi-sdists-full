from typing import Any

import pytest

from mistralai.workflows import get_workflow_definition, workflow

from .fixtures import (
    GreetingResult,
    MultiActivityWorkflow,
    PureWorkflow,
    SimpleWorkflow,
    say_goodbye,
    say_hello,
)
from .utils import create_test_worker


@workflow.define(name="spec_workflow")
class SpecWorkflow:
    @workflow.entrypoint
    async def run(self, name: str) -> GreetingResult:
        return GreetingResult(message="test")


class TestBasicWorkflowExecution:
    @pytest.mark.asyncio
    async def test_workflow_with_activity_call(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[SimpleWorkflow], activities=[say_hello]):
            workflow_def = get_workflow_definition(SimpleWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Alice"},
                id="test-simple-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert result["result"] == "Hello, Alice!"

    @pytest.mark.asyncio
    async def test_workflow_with_multiple_activities(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env, workflows=[MultiActivityWorkflow], activities=[say_hello, say_goodbye]
        ):
            workflow_def = get_workflow_definition(MultiActivityWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Bob"},
                id="test-multi-activity",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert "Hello, Bob!" in result["result"]
            assert "Goodbye, Bob!" in result["result"]

    @pytest.mark.asyncio
    async def test_workflow_without_activities(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[PureWorkflow], activities=[]):
            workflow_def = get_workflow_definition(PureWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Charlie"},
                id="test-pure-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == "Workflow says: Charlie"


class TestWorkflowDefinition:
    @pytest.mark.asyncio
    async def test_workflow_definition_structure(self, temporal_env: Any) -> None:
        workflow_def = get_workflow_definition(SpecWorkflow)

        assert workflow_def is not None
        assert workflow_def.name == "spec_workflow"
        assert workflow_def.input_schema is not None
        assert workflow_def.output_schema is not None
        assert len(workflow_def.signals) == 0
        assert len(workflow_def.queries) == 0

    @pytest.mark.asyncio
    async def test_workflow_with_pydantic_result(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[SpecWorkflow], activities=[]):
            workflow_def = get_workflow_definition(SpecWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "TestUser"},
                id="test-pydantic-result",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert "message" in result
            assert result["message"] == "test"
