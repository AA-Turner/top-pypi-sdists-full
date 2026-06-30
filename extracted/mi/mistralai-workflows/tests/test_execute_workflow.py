from typing import Any

import pytest
from temporalio.client import WorkflowFailureError
from temporalio.exceptions import ApplicationError, ChildWorkflowError

import mistralai.workflows as workflows
from mistralai.workflows import get_workflow_definition
from mistralai.workflows.exceptions import WorkflowsException

from .fixtures import (
    ChildWorkflow,
    ChildWorkflowCustomExecute,
    ChildWorkflowParams,
    CompareWaitModesParentWorkflow,
    CompareWaitModesPydanticParentWorkflow,
    FailingChildWaitFalseParent,
    FailingChildWaitTrueParent,
    FailingWorkflow,
    FireAndForgetChildParams,
    FireAndForgetChildWorkflow,
    FireAndForgetParentWorkflow,
    MultiArgChildWorkflow,
    MultiArgParentWorkflow,
    MultiParamWithPrefixInput,
    NestedChildLevel1,
    NestedChildLevel2,
    NestedParentWorkflow,
    ParentWorkflow,
    PersonData,
    PrimitiveChildWorkflow,
    PrimitiveParentWorkflow,
    PrimitiveWorkflowParams,
    ProcessingResult,
    PydanticChildWorkflow,
    PydanticParentWorkflow,
    ReportsExecutionTimeoutChild,
    ReportsTimeoutOverrideParent,
    ReportsTimeoutParent,
    StandaloneWorkflowWithMultiArgs,
    StandaloneWorkflowWithPydantic,
    StartThenAwaitParentWorkflow,
)
from .utils import create_test_worker


class TestExecuteWorkflowBasic:
    @pytest.mark.asyncio
    async def test_simple_child_workflow(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ParentWorkflow, ChildWorkflow], activities=[]):
            workflow_def = get_workflow_definition(ParentWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Test"},
                id="test-parent-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert "Child says: Test" in result["result"]
            assert "Parent got:" in result["result"]


class TestExecuteWorkflowWithPydantic:
    @pytest.mark.asyncio
    async def test_child_workflow_with_pydantic_model(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env, workflows=[PydanticParentWorkflow, PydanticChildWorkflow], activities=[]
        ):
            workflow_def = get_workflow_definition(PydanticParentWorkflow)
            person = PersonData(first_name="John", last_name="Doe", age=25)

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                person.model_dump(),
                id="test-pydantic-parent",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert "Processed: John Doe is an adult" in result["result"]

    @pytest.mark.asyncio
    async def test_child_workflow_with_pydantic_minor(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env, workflows=[PydanticParentWorkflow, PydanticChildWorkflow], activities=[]
        ):
            workflow_def = get_workflow_definition(PydanticParentWorkflow)
            person = PersonData(first_name="Jane", last_name="Smith", age=16)

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                person.model_dump(),
                id="test-pydantic-parent-minor",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert "Processed: Jane Smith is a minor" in result["result"]


class TestExecuteWorkflowWithMultipleArgs:
    @pytest.mark.asyncio
    async def test_child_workflow_with_multiple_args(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env, workflows=[MultiArgParentWorkflow, MultiArgChildWorkflow], activities=[]
        ):
            workflow_def = get_workflow_definition(MultiArgParentWorkflow)

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Hello", "count": 3},
                id="test-multi-arg-parent",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert "Parent received: Hello repeated 3 times: Hello, Hello, Hello" in result["result"]


class TestExecuteWorkflowWithPrimitives:
    @pytest.mark.asyncio
    async def test_child_workflow_with_primitive_types(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env, workflows=[PrimitiveParentWorkflow, PrimitiveChildWorkflow], activities=[]
        ):
            workflow_def = get_workflow_definition(PrimitiveParentWorkflow)

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"message": "TestMessage"},
                id="test-primitive-parent",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert "Got back: Echo: TestMessage" in result["result"]


class TestExecuteWorkflowNested:
    @pytest.mark.asyncio
    async def test_nested_child_workflows(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[NestedParentWorkflow, NestedChildLevel1, NestedChildLevel2],
            activities=[],
        ):
            workflow_def = get_workflow_definition(NestedParentWorkflow)

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"value": "test"},
                id="test-nested-parent",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == "L0[L1[L2[test]]]"


class TestExecuteWorkflowDirect:
    @pytest.mark.asyncio
    async def test_direct_execute_workflow_with_pydantic(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[StandaloneWorkflowWithPydantic], activities=[]):
            person = PersonData(first_name="Alice", last_name="Johnson", age=30)

            result = await workflows.execute_workflow(StandaloneWorkflowWithPydantic, params=person)

            assert isinstance(result, ProcessingResult)
            assert result.full_name == "Alice Johnson"
            assert result.is_adult is True
            assert "Standalone: Alice Johnson is an adult" in result.message

    @pytest.mark.asyncio
    async def test_direct_execute_workflow_with_multiple_args(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[StandaloneWorkflowWithMultiArgs], activities=[]):
            result = await workflows.execute_workflow(
                StandaloneWorkflowWithMultiArgs, params=MultiParamWithPrefixInput(name="Item", count=3, prefix=">> ")
            )

            assert isinstance(result, str)
            assert result == "Generated: >> Item, >> Item, >> Item"

    @pytest.mark.asyncio
    async def test_direct_execute_workflow_returns_primitive(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[PrimitiveChildWorkflow], activities=[]):
            result = await workflows.execute_workflow(
                PrimitiveChildWorkflow, params=PrimitiveWorkflowParams(message="DirectCall")
            )

            assert isinstance(result, str)
            assert result == "Echo: DirectCall"


class TestExecuteWorkflowNoWait:
    @pytest.mark.asyncio
    async def test_fire_and_forget(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[FireAndForgetParentWorkflow, FireAndForgetChildWorkflow],
            activities=[],
        ):
            workflow_def = get_workflow_definition(FireAndForgetParentWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"tag": "abc"},
                id="test-fire-and-forget-parent",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == "parent-done:abc"

    @pytest.mark.asyncio
    async def test_start_then_await(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[StartThenAwaitParentWorkflow, FireAndForgetChildWorkflow],
            activities=[],
        ):
            workflow_def = get_workflow_definition(StartThenAwaitParentWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"tag": "xyz"},
                id="test-start-then-await-parent",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == "parent-got:child-done:xyz"

    @pytest.mark.asyncio
    async def test_wait_false_outside_workflow_raises(self) -> None:
        with pytest.raises(WorkflowsException):
            await workflows.execute_workflow(
                FireAndForgetChildWorkflow,
                params=FireAndForgetChildParams(tag="test"),
                wait=False,
            )


class TestExecuteWorkflowWaitComparison:
    """Compare wait=True and wait=False return values from within a workflow."""

    @pytest.mark.asyncio
    async def test_wait_true_and_wait_false_return_same_result(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[CompareWaitModesParentWorkflow, FireAndForgetChildWorkflow],
            activities=[],
        ):
            workflow_def = get_workflow_definition(CompareWaitModesParentWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"tag": "compare"},
                id="test-compare-wait-modes",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            wait_true_result = result["result"]["wait_true"]
            wait_false_result = result["result"]["wait_false"]

            assert wait_true_result == wait_false_result, (
                f"wait=True and wait=False returned different results!\n"
                f"  wait=True:  {wait_true_result}\n"
                f"  wait=False: {wait_false_result}\n"
            )


class TestFailingChildWorkflow:
    """Verify that failing child workflows surface the same error regardless of wait mode."""

    @staticmethod
    def _get_cause_chain(exc: BaseException) -> list[type]:
        """Return the list of exception types in the __cause__ chain."""
        chain: list[type] = [type(exc)]
        while exc.__cause__ is not None:
            exc = exc.__cause__
            chain.append(type(exc))
        return chain

    @pytest.mark.asyncio
    async def test_failing_child_same_error_both_modes(self, temporal_env: Any) -> None:
        """Ensure the full error chain and message are identical for wait=True and wait=False."""
        errors: dict[str, WorkflowFailureError] = {}

        for label, parent_cls, wf_id in [
            ("wait_true", FailingChildWaitTrueParent, "test-fail-cmp-wait-true"),
            ("wait_false", FailingChildWaitFalseParent, "test-fail-cmp-wait-false"),
        ]:
            async with create_test_worker(
                temporal_env,
                workflows=[parent_cls, FailingWorkflow],
                activities=[],
            ):
                workflow_def = get_workflow_definition(parent_cls)
                h = await temporal_env.client.start_workflow(
                    workflow_def.name,
                    {"message": "same-error"},
                    id=wf_id,
                    task_queue="test-task-queue",
                )
                with pytest.raises(WorkflowFailureError) as exc_info:
                    await h.result()
                errors[label] = exc_info.value

        chain_true = self._get_cause_chain(errors["wait_true"])
        chain_false = self._get_cause_chain(errors["wait_false"])

        assert chain_true == chain_false, (
            f"Different exception chains:\n  wait=True:  {chain_true}\n  wait=False: {chain_false}"
        )
        assert chain_true == [WorkflowFailureError, ChildWorkflowError, ApplicationError]

        root_true = errors["wait_true"]
        root_false = errors["wait_false"]
        while root_true.__cause__ is not None:
            root_true = root_true.__cause__
        while root_false.__cause__ is not None:
            root_false = root_false.__cause__

        assert str(root_true) == str(root_false), (
            f"Different root error messages:\n  wait=True:  {root_true}\n  wait=False: {root_false}"
        )


class TestChildWorkflowWithPydanticParams:
    """Test child workflows that receive a pydantic model return the same result with wait=True and wait=False."""

    @pytest.mark.asyncio
    async def test_pydantic_child_same_result_both_modes(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[CompareWaitModesPydanticParentWorkflow, PydanticChildWorkflow],
            activities=[],
        ):
            workflow_def = get_workflow_definition(CompareWaitModesPydanticParentWorkflow)
            person = PersonData(first_name="Alice", last_name="Johnson", age=30)

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                person.model_dump(),
                id="test-pydantic-child-wait-modes",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            wait_true_result = result["result"]["wait_true"]
            wait_false_result = result["result"]["wait_false"]

            assert wait_true_result == wait_false_result, (
                f"wait=True and wait=False returned different results!\n"
                f"  wait=True:  {wait_true_result}\n"
                f"  wait=False: {wait_false_result}\n"
            )
            assert wait_true_result["full_name"] == "Alice Johnson"
            assert wait_true_result["is_adult"] is True


class TestChildWorkflowCustomEntrypoint:
    def test_child_workflow_with_custom_entrypoint_name_has_correct_method(self) -> None:
        assert hasattr(ChildWorkflowCustomExecute, "execute")
        assert callable(ChildWorkflowCustomExecute.execute)

    @pytest.mark.asyncio
    async def test_execute_workflow_works_with_custom_entrypoint_name(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ChildWorkflowCustomExecute], activities=[]):
            result = await workflows.execute_workflow(
                ChildWorkflowCustomExecute, params=ChildWorkflowParams(name="Test")
            )

            assert result == "Child with custom entrypoint says: Test"


class TestExecuteWorkflowDeclaredTimeout:
    """execute_workflow honours the child's declared @define(execution_timeout=...) unless overridden."""

    @pytest.mark.asyncio
    async def test_uses_declared_execution_timeout_when_not_overridden(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ReportsTimeoutParent, ReportsExecutionTimeoutChild],
            activities=[],
        ):
            workflow_def = get_workflow_definition(ReportsTimeoutParent)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"tag": "abc"},
                id="test-declared-timeout-honoured",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == 2.0, (
                "child dispatched without an explicit execution_timeout should inherit its declared "
                f"2s; before the fix execute_workflow forced the 1h (3600s) default, got {result['result']}s"
            )

    @pytest.mark.asyncio
    async def test_explicit_execution_timeout_overrides_declared(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ReportsTimeoutOverrideParent, ReportsExecutionTimeoutChild],
            activities=[],
        ):
            workflow_def = get_workflow_definition(ReportsTimeoutOverrideParent)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"tag": "abc"},
                id="test-declared-timeout-overridden",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == 30 * 60, (
                "explicit execution_timeout (30 min) passed to execute_workflow should override the "
                f"child's declared 2s, got {result['result']}s"
            )
