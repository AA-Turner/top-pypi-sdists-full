import json
from typing import Any, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel, Field
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.plugins.mistralai.tool import execute_activity_tool
from mistralai.workflows.testing import create_test_worker


class _SimpleResult(BaseModel):
    name: str
    score: float


class _Address(BaseModel):
    city: str
    zip_code: str


class _User(BaseModel):
    name: str
    addresses: list[_Address]


_NESTED_USER = _User(
    name="alice",
    addresses=[_Address(city="Paris", zip_code="75001"), _Address(city="Lyon", zip_code="69001")],
)

_NESTED_DICT = {
    "users": [
        {"id": 1, "tags": ["admin", "active"], "meta": {"login_count": 42}},
        {"id": 2, "tags": [], "meta": {"login_count": 0}},
    ],
    "pagination": {"page": 1, "total": 2, "has_next": False},
}

_LIST_OF_DICTS = [
    {"type": "text", "content": "hello"},
    {"type": "image", "url": "https://example.com/img.png", "dimensions": [800, 600]},
    {"type": "code", "language": "python", "lines": 42},
]


@pytest.fixture
def mock_tool_execution() -> Generator[tuple[MagicMock | AsyncMock, MagicMock | AsyncMock], Any, None]:
    """Mock tool execution dependencies to isolate execute_activity_tool testing."""
    with (
        patch("mistralai.workflows.plugins.mistralai.tool.get_wrapped_activity") as mock_activity,
        patch("mistralai.workflows.plugins.mistralai.tool.get_function_signature_type_hints") as mock_hints,
    ):
        yield mock_activity, mock_hints


class TestExecuteActivityTool:
    @pytest.mark.asyncio
    async def test_execute_activity_tool_invalid_json(
        self, mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock]
    ) -> None:
        async def mock_activity() -> None:
            return None

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({}, None, False)

        with pytest.raises(WorkflowsException, match="Invalid arguments for tool"):
            await execute_activity_tool("mock_activity", "{invalid json}", raise_on_tool_fail=True)

        result = await execute_activity_tool("mock_activity", "{invalid json}", raise_on_tool_fail=False)
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["success"] is False
        assert "Could not parse JSON" in parsed["error"]

    @pytest.mark.asyncio
    async def test_execute_activity_tool_validation_error(
        self, mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock]
    ) -> None:
        class ValidParams(BaseModel):
            name: str
            age: int = Field(gt=0)

        async def mock_activity(params: ValidParams) -> None:
            return None

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({"params": ValidParams}, None, False)

        invalid_args = json.dumps({"name": "test", "age": -5})

        with pytest.raises(WorkflowsException, match="Invalid arguments for tool"):
            await execute_activity_tool("mock_activity", invalid_args, raise_on_tool_fail=True)

        result = await execute_activity_tool("mock_activity", invalid_args, raise_on_tool_fail=False)
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["success"] is False
        assert "Invalid arguments for tool" in parsed["error"]
        assert "age" in parsed["error"]

    @pytest.mark.asyncio
    async def test_execute_activity_tool_missing_required_field(
        self, mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock]
    ) -> None:
        class ValidParams(BaseModel):
            required_field: str
            optional_field: str = "default"

        async def mock_activity(params: ValidParams) -> None:
            return None

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({"params": ValidParams}, None, False)

        incomplete_args = json.dumps({"params": {"optional_field": "test"}})

        result = await execute_activity_tool("mock_activity", incomplete_args, raise_on_tool_fail=False)
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["success"] is False
        assert "required_field" in parsed["error"]
        assert "Invalid arguments for tool mock_activity" in parsed["error"]

    @pytest.mark.asyncio
    async def test_execute_activity_tool_successful_execution(
        self, mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock]
    ) -> None:
        class ValidParams(BaseModel):
            message: str

        class ValidResult(BaseModel):
            result: str

        async def mock_activity(params: ValidParams) -> ValidResult:
            return ValidResult(result=f"Processed: {params.message}")

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({"params": ValidParams}, ValidResult, False)

        valid_args = json.dumps({"params": {"message": "test"}})

        result2 = await execute_activity_tool("mock_activity", valid_args, raise_on_tool_fail=False)
        result1 = await execute_activity_tool("mock_activity", valid_args, raise_on_tool_fail=True)

        assert result1 == result2
        parsed = json.loads(result1)
        assert parsed["result"] == "Processed: test"

    @pytest.mark.asyncio
    async def test_execute_activity_tool_invalid_tool_name(
        self, mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock]
    ) -> None:
        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = None

        with pytest.raises(WorkflowsException) as exc_info:
            await execute_activity_tool("nonexistent_tool", "{}", raise_on_tool_fail=True)
        assert exc_info.value.code == ErrorCode.ACTIVITY_NOT_FOUND_ERROR

        result = await execute_activity_tool("nonexistent_tool", "{}", raise_on_tool_fail=False)
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["success"] is False
        assert "Invalid tool name nonexistent_tool" in parsed["error"]
        assert "Could not find it in the declared agent tools" in parsed["error"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "return_value, expected_output",
        [
            pytest.param(None, "None", id="none"),
            pytest.param("hello world", "hello world", id="string"),
            pytest.param(42, "42", id="int"),
            pytest.param({"key": "value", "num": 123}, json.dumps({"key": "value", "num": 123}), id="flat_dict"),
            pytest.param([1, "two", 3.0], json.dumps([1, "two", 3.0]), id="flat_list"),
            pytest.param(
                _SimpleResult(name="test", score=0.95),
                _SimpleResult(name="test", score=0.95).model_dump_json(),
                id="basemodel",
            ),
            pytest.param(_NESTED_USER, _NESTED_USER.model_dump_json(), id="nested_basemodel"),
            pytest.param(_NESTED_DICT, json.dumps(_NESTED_DICT), id="nested_dict"),
            pytest.param(_LIST_OF_DICTS, json.dumps(_LIST_OF_DICTS), id="list_of_dicts"),
        ],
    )
    async def test_return_type_serialization(
        self,
        mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock],
        return_value: Any,
        expected_output: str,
    ) -> None:
        async def mock_activity() -> Any:
            return return_value

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({}, type(return_value), False)

        result = await execute_activity_tool("mock_activity", "{}", raise_on_tool_fail=True)
        assert result == expected_output

    @pytest.mark.asyncio
    async def test_execute_activity_tool_runtime_error_reraises_when_raise_on_fail(
        self, mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock]
    ) -> None:
        async def mock_activity() -> None:
            raise RuntimeError("database connection failed")

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({}, None, False)

        with pytest.raises(WorkflowsException, match="database connection failed") as exc_info:
            await execute_activity_tool("mock_activity", "{}", raise_on_tool_fail=True)
        assert exc_info.value.code == ErrorCode.EXECUTION_ERROR
        assert isinstance(exc_info.value.__cause__, RuntimeError)

    @pytest.mark.asyncio
    async def test_execute_activity_tool_runtime_error_returns_error_json_when_not_raise_on_fail(
        self, mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock]
    ) -> None:
        async def mock_activity() -> None:
            raise RuntimeError("database connection failed")

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({}, None, False)

        result = await execute_activity_tool("mock_activity", "{}", raise_on_tool_fail=False)
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["success"] is False
        assert parsed["error"] == "Tool mock_activity raised an error during execution: database connection failed"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("raise_on_tool_fail", [True, False])
    async def test_execute_activity_tool_preserves_framework_exception_code(
        self,
        mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock],
        raise_on_tool_fail: bool,
    ) -> None:
        """A WorkflowsException raised by the activity wrapper itself (e.g. a missing
        sticky worker session) must propagate unchanged, keeping its original code
        rather than being re-wrapped as EXECUTION_ERROR."""

        async def mock_activity() -> None:
            raise WorkflowsException(
                message="Activity is sticky to worker but no task queue is set.",
                code=ErrorCode.STICKY_WORKER_SESSION_MISSING,
            )

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({}, None, False)

        with pytest.raises(WorkflowsException) as exc_info:
            await execute_activity_tool("mock_activity", "{}", raise_on_tool_fail=raise_on_tool_fail)
        assert exc_info.value.code == ErrorCode.STICKY_WORKER_SESSION_MISSING
        assert "sticky to worker" in exc_info.value.message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("raise_on_tool_fail", [True, False])
    async def test_return_non_jsonable(
        self,
        mock_tool_execution: tuple[MagicMock | AsyncMock, MagicMock | AsyncMock],
        raise_on_tool_fail: bool,
    ) -> None:
        async def mock_activity() -> object:
            return object()

        mock_activity_fn, mock_hints = mock_tool_execution
        mock_activity_fn.return_value = mock_activity
        mock_hints.return_value = ({}, object, False)

        if raise_on_tool_fail:
            with pytest.raises(WorkflowsException, match="non-serializable result") as exc_info:
                await execute_activity_tool("mock_activity", "{}", raise_on_tool_fail=True)
            assert exc_info.value.code == ErrorCode.TOOL_ARGUMENT_ERROR
            assert exc_info.value.__cause__ is not None
            assert isinstance(exc_info.value.__cause__, TypeError)
        else:
            result = await execute_activity_tool("mock_activity", "{}", raise_on_tool_fail=False)
            assert isinstance(result, str)
            parsed = json.loads(result)
            assert parsed["success"] is False
            assert "non-serializable result" in parsed["error"]


@activity(retry_policy_max_attempts=1)
async def _failing_tool_activity() -> str:
    raise RuntimeError("database connection failed")


@workflow.define(name="tool_error_surfacing_workflow")
class _ToolErrorSurfacingWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        try:
            await execute_activity_tool("_failing_tool_activity", "{}", raise_on_tool_fail=True)
        except WorkflowsException as e:
            return e.message
        return "no error raised"


class TestExecuteActivityToolInWorkflow:
    @pytest.mark.asyncio
    async def test_runtime_error_surfaces_real_message_through_activity_error(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        """The underlying error must survive Temporal's ActivityError wrapping.

        Unlike the unit tests above (which mock the activity as a plain async
        function), running inside a real workflow means ``await activity(...)``
        raises a Temporal ``ActivityError`` whose ``str()`` is a generic wrapper.
        The real message lives in ``__cause__`` and must be unwrapped.
        """
        async with create_test_worker(
            temporal_env,
            workflows=[_ToolErrorSurfacingWorkflow],
            activities=[_failing_tool_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "tool_error_surfacing_workflow",
                id="test-tool-error-surfacing",
                task_queue="test-task-queue",
            )
            result = await handle.result()

        message = result["result"] if isinstance(result, dict) else result
        assert "database connection failed" in message
        assert "Activity task failed" not in message
