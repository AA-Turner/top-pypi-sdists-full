from typing import Any

import pytest
from pydantic import BaseModel, Field

from mistralai.workflows import activity, workflow
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition

from .utils import create_test_worker


class GreetingParams(BaseModel):
    name: str = Field(description="Name to greet")


class GreetingResult(BaseModel):
    message: str = Field(description="Greeting message")


@activity()
async def say_hello_pydantic(params: GreetingParams) -> GreetingResult:
    return GreetingResult(message=f"Hello, {params.name}!")


@activity()
async def say_goodbye_pydantic(params: GreetingParams) -> GreetingResult:
    return GreetingResult(message=f"Goodbye, {params.name}!")


@workflow.define(name="test-simple-workflow")
class SimpleWorkflow:
    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        result = await say_hello_pydantic(params)
        return result


@workflow.define(name="test-multi-activity")
class MultiActivityWorkflow:
    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        hello = await say_hello_pydantic(params)
        goodbye = await say_goodbye_pydantic(params)
        return GreetingResult(message=f"{hello.message} {goodbye.message}")


@workflow.define(name="test-pure-workflow")
class PureWorkflow:
    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        return GreetingResult(message=f"Workflow says: {params.name}")


@workflow.define(name="test-signal-workflow")
class SignalWorkflow:
    def __init__(self) -> None:
        self.messages: list[str] = []

    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        await workflow.wait_condition(lambda: len(self.messages) > 0, timeout=5.0)
        return GreetingResult(message=", ".join(self.messages))

    @workflow.signal()
    async def add_message(self, msg: GreetingParams) -> None:
        self.messages.append(msg.name)


@workflow.define(name="test-query-workflow")
class QueryWorkflow:
    def __init__(self) -> None:
        self.value = "initial"

    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        self.value = params.name
        await workflow.wait_condition(lambda: False, timeout=1.0)
        return GreetingResult(message=f"Done with {self.value}")

    @workflow.query()
    def get_value(self) -> GreetingResult:
        return GreetingResult(message=self.value)


@workflow.define(name="test-child-workflow")
class ChildWorkflow:
    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        return GreetingResult(message=f"Child says: {params.name}")


@workflow.define(name="test-parent-workflow")
class ParentWorkflow:
    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        child_result = await workflow.execute_workflow(
            ChildWorkflow,
            params=params,
        )
        return GreetingResult(message=f"Parent received: {child_result.message}")


@workflow.define(
    name="test-spec-workflow",
    workflow_description="A test workflow for verifying spec generation",
)
class SpecWorkflow:
    @workflow.entrypoint
    async def run(self, params: GreetingParams) -> GreetingResult:
        return GreetingResult(message="test")

    @workflow.signal()
    async def test_signal(self, msg: GreetingParams) -> None:
        pass

    @workflow.query()
    def test_query(self) -> GreetingResult:
        return GreetingResult(message="query")


class TestBasicWorkflowExecution:
    @pytest.mark.asyncio
    async def test_workflow_with_activity_call(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[SimpleWorkflow], activities=[say_hello_pydantic]):
            workflow_def = get_workflow_definition(SimpleWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                GreetingParams(name="Alice").model_dump(),
                id="test-simple-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            # Temporal returns dict, our wrapper handles Pydantic
            assert isinstance(result, dict)
            assert result["message"] == "Hello, Alice!"

    @pytest.mark.asyncio
    async def test_workflow_with_multiple_activities(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env, workflows=[MultiActivityWorkflow], activities=[say_hello_pydantic, say_goodbye_pydantic]
        ):
            workflow_def = get_workflow_definition(MultiActivityWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                GreetingParams(name="Bob").model_dump(),
                id="test-multi-activity",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert "Hello, Bob!" in result["message"]
            assert "Goodbye, Bob!" in result["message"]

    @pytest.mark.asyncio
    async def test_workflow_without_activities(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[PureWorkflow], activities=[]):
            workflow_def = get_workflow_definition(PureWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                GreetingParams(name="Charlie").model_dump(),
                id="test-pure-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["message"] == "Workflow says: Charlie"


class TestWorkflowSignals:
    @pytest.mark.asyncio
    async def test_signal_decorator(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[SignalWorkflow], activities=[]):
            workflow_def = get_workflow_definition(SignalWorkflow)
            assert workflow_def is not None

            assert len(workflow_def.signals) == 1
            assert workflow_def.signals[0].name == "add_message"

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                GreetingParams(name="Initial").model_dump(),
                id="test-signal-workflow",
                task_queue="test-task-queue",
            )

            await handle.signal("add_message", GreetingParams(name="TestMessage").model_dump())

            result = await handle.result()
            assert "TestMessage" in result["message"]


class TestWorkflowQueries:
    @pytest.mark.asyncio
    async def test_query_decorator(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[QueryWorkflow], activities=[]):
            workflow_def = get_workflow_definition(QueryWorkflow)
            assert workflow_def is not None

            # Verify query is registered
            assert len(workflow_def.queries) == 1
            assert workflow_def.queries[0].name == "get_value"

            # Note: Queries on completed workflows aren't well supported in test env
            # Just verify the decorator registration works


class TestChildWorkflows:
    @pytest.mark.asyncio
    async def test_execute_workflow_helper(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ParentWorkflow, ChildWorkflow], activities=[]):
            workflow_def = get_workflow_definition(ParentWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                GreetingParams(name="Test").model_dump(),
                id="test-parent-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert "Child says: Test" in result["message"]
            assert "Parent received:" in result["message"]


class TestWorkflowDefinition:
    @pytest.mark.asyncio
    async def test_workflow_definition_structure(self, temporal_env: Any) -> None:
        workflow_def = get_workflow_definition(SpecWorkflow)

        assert workflow_def is not None
        assert workflow_def.name == "test-spec-workflow"
        assert workflow_def.description == "A test workflow for verifying spec generation"
        assert workflow_def.input_schema is not None
        assert workflow_def.output_schema is not None
        assert len(workflow_def.signals) == 1
        assert workflow_def.signals[0].name == "test_signal"
        assert len(workflow_def.queries) == 1
        assert workflow_def.queries[0].name == "test_query"
