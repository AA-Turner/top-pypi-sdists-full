from datetime import timedelta
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict
from temporalio.client import WorkflowFailureError

from mistralai.workflows import activity, get_workflow_definition, workflow
from mistralai.workflows.exceptions import WorkflowsException

from .fixtures import (
    GreetingParams,
    ParamsModel,
    UpdateInput,
    WorkflowWithPydanticHandlers,
)
from .utils import create_test_worker


class SimpleInput(BaseModel):
    message: str


class ComplexOutput(BaseModel):
    result: str
    count: int


class PromptInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str


class CountInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    count: int


@workflow.define(name="workflow_with_union_input")
class WorkflowWithUnionInput:
    @workflow.entrypoint
    async def run(self, params: PromptInput | CountInput) -> str:
        if isinstance(params, PromptInput):
            return f"prompt:{params.prompt}"
        return f"count:{params.count}"


@workflow.define(name="workflow_with_optional_union_input")
class WorkflowWithOptionalUnionInput:
    @workflow.entrypoint
    async def run(self, params: PromptInput | CountInput | None) -> str:
        if params is None:
            return "none"
        if isinstance(params, PromptInput):
            return f"prompt:{params.prompt}"
        return f"count:{params.count}"


@workflow.define(name="workflow_with_defaults")
class WorkflowWithDefaults:
    @workflow.entrypoint
    async def run(self, name: str, greeting: str = "Hello", count: int = 1) -> str:
        return f"{greeting}, {name}! (x{count})"


@workflow.define(name="workflow_all_defaults")
class WorkflowAllDefaults:
    @workflow.entrypoint
    async def run(self, name: str = "World", greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"


@workflow.define(name="workflow_mixed_params")
class WorkflowMixedParams:
    @workflow.entrypoint
    async def run(
        self,
        required_str: str,
        optional_int: int = 42,
        optional_bool: bool = False,
        optional_str: str = "default",
    ) -> str:
        return f"{required_str}: int={optional_int}, bool={optional_bool}, str={optional_str}"


@activity()
async def activity_with_defaults(name: str, prefix: str = "Mr.", suffix: str = "") -> str:
    result = f"{prefix} {name}"
    if suffix:
        result += f" {suffix}"
    return result


@activity()
async def activity_all_defaults(x: int = 10, y: int = 20) -> int:
    return x + y


@workflow.define(name="workflow_calling_activity_with_defaults")
class WorkflowCallingActivityWithDefaults:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        result1 = await activity_with_defaults(name, "Dr.", "PhD")
        result2 = await activity_with_defaults(name, "Ms.")
        result3 = await activity_with_defaults(name)
        result4 = await activity_all_defaults()
        result5 = await activity_all_defaults(5)
        result6 = await activity_all_defaults(5, 15)
        return f"{result1} | {result2} | {result3} | {result4} | {result5} | {result6}"


@workflow.define(name="workflow_with_signal_defaults")
class WorkflowWithSignalDefaults:
    def __init__(self) -> None:
        self.messages: list[str] = []

    @workflow.entrypoint
    async def run(self) -> str:
        await workflow.wait_condition(lambda: len(self.messages) >= 2)
        return " | ".join(self.messages)

    @workflow.signal(name="add_message")
    async def add_message(self, text: str, priority: int = 0, tag: str = "info") -> None:
        self.messages.append(f"[{tag}:{priority}] {text}")


@workflow.define(name="workflow_with_query_defaults")
class WorkflowWithQueryDefaults:
    def __init__(self) -> None:
        self.counter = 0

    @workflow.entrypoint
    async def run(self) -> str:
        await workflow.wait_condition(lambda: self.counter >= 10)
        return "done"

    @workflow.signal(name="increment")
    async def increment(self, amount: int = 1) -> None:
        self.counter += amount

    @workflow.query(name="get_counter")
    def get_counter(self, multiplier: int = 1, offset: int = 0) -> int:
        return (self.counter * multiplier) + offset


@workflow.define(name="workflow_with_update_defaults")
class WorkflowWithUpdateDefaults:
    def __init__(self) -> None:
        self.value = 100

    @workflow.entrypoint
    async def run(self) -> int:
        await workflow.wait_condition(lambda: self.value <= 0)
        return self.value

    @workflow.update(name="adjust_value")
    async def adjust_value(self, delta: int, min_value: int = 0, max_value: int = 200) -> dict:
        old_value = self.value
        self.value += delta
        self.value = max(min_value, min(max_value, self.value))
        return {"old": old_value, "new": self.value, "clamped": old_value + delta != self.value}


@workflow.define(name="test_signal_empty_dict_defaults")
class SignalEmptyDictDefaultsWorkflow:
    def __init__(self) -> None:
        self.counter = 0

    @workflow.entrypoint
    async def run(self) -> int:
        await workflow.wait_condition(lambda: self.counter >= 2)
        return self.counter

    @workflow.signal(name="increment")
    async def increment(self, amount: int = 1) -> None:
        self.counter += amount


class TestWorkflowDefaultParameters:
    @pytest.mark.asyncio
    async def test_workflow_with_some_defaults(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithDefaults], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithDefaults)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Alice", "greeting": "Hi", "count": 3},
                id="test-all-params",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "Hi, Alice! (x3)"

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Bob"},
                id="test-required-only",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "Hello, Bob! (x1)"

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Charlie", "count": 5},
                id="test-partial-defaults",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "Hello, Charlie! (x5)"

    @pytest.mark.asyncio
    async def test_workflow_with_all_defaults(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowAllDefaults], activities=[]):
            workflow_def = get_workflow_definition(WorkflowAllDefaults)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-no-params",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "Hello, World!"

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Python"},
                id="test-one-param",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "Hello, Python!"

    @pytest.mark.asyncio
    async def test_workflow_mixed_default_types(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowMixedParams], activities=[]):
            workflow_def = get_workflow_definition(WorkflowMixedParams)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"required_str": "test"},
                id="test-mixed-required-only",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "test: int=42, bool=False, str=default"

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"required_str": "custom", "optional_int": 99, "optional_bool": True},
                id="test-mixed-partial",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "custom: int=99, bool=True, str=default"


class TestActivityDefaultParameters:
    @pytest.mark.asyncio
    async def test_activity_with_defaults(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowCallingActivityWithDefaults],
            activities=[activity_with_defaults, activity_all_defaults],
        ):
            workflow_def = get_workflow_definition(WorkflowCallingActivityWithDefaults)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Smith"},
                id="test-activity-defaults",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            expected = "Dr. Smith PhD | Ms. Smith | Mr. Smith | 30 | 25 | 20"
            assert result["result"] == expected


class TestSignalDefaultParameters:
    @pytest.mark.asyncio
    async def test_signal_with_defaults(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithSignalDefaults], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithSignalDefaults)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-signal-defaults",
                task_queue="test-task-queue",
            )

            await handle.signal("add_message", {"text": "urgent", "priority": 10, "tag": "error"})

            await handle.signal("add_message", {"text": "normal"})

            result = await handle.result()
            assert "[error:10] urgent" in result["result"]
            assert "[info:0] normal" in result["result"]

    @pytest.mark.asyncio
    async def test_signal_empty_dict_uses_all_defaults(self, temporal_env: Any) -> None:
        """
        Regression test: empty dict with all default parameters.

        Without selective @functools.wraps (excluding __annotations__), Temporal would see
        the original function signature and fail to deserialize an empty dict.
        See workflows/worker/workflow.py signal/query/update decorators.
        """
        async with create_test_worker(temporal_env, workflows=[SignalEmptyDictDefaultsWorkflow], activities=[]):
            handle = await temporal_env.client.start_workflow(
                "test_signal_empty_dict_defaults",
                {},
                id="test-signal-empty-dict",
                task_queue="test-task-queue",
            )

            await handle.signal("increment", {"amount": 1})
            await handle.signal("increment", {})

            result = await handle.result()
            assert result["result"] == 2


class TestQueryDefaultParameters:
    @pytest.mark.asyncio
    async def test_query_with_defaults(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithQueryDefaults], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithQueryDefaults)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-query-defaults",
                task_queue="test-task-queue",
            )

            await handle.signal("increment", {"amount": 5})
            await handle.signal("increment", {})  # default amount=1

            result = await handle.query("get_counter", {})
            assert result == 6  # 5 + 1, multiplier=1, offset=0

            result = await handle.query("get_counter", {"multiplier": 2})
            assert result == 12  # (5 + 1) * 2 + 0

            result = await handle.query("get_counter", {"multiplier": 3, "offset": 10})
            assert result == 28  # (5 + 1) * 3 + 10


class TestUpdateDefaultParameters:
    @pytest.mark.asyncio
    async def test_update_with_defaults(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithUpdateDefaults], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithUpdateDefaults)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-update-defaults",
                task_queue="test-task-queue",
            )

            result = await handle.execute_update("adjust_value", {"delta": -30})
            assert result["old"] == 100
            assert result["new"] == 70
            assert result["clamped"] is False

            result = await handle.execute_update("adjust_value", {"delta": 150, "max_value": 150})
            assert result["old"] == 70
            assert result["new"] == 150
            assert result["clamped"] is True

            result = await handle.execute_update("adjust_value", {"delta": -200, "min_value": -10})
            assert result["old"] == 150
            assert result["new"] == -10
            assert result["clamped"] is True


class TestPydanticParameters:
    @pytest.mark.asyncio
    async def test_pydantic_signal_query_update_handlers(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithPydanticHandlers], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithPydanticHandlers)
            assert workflow_def is not None

            params = ParamsModel(name="TestWorkflow", count=2)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                params.model_dump(),
                id="test-pydantic-handlers",
                task_queue="test-task-queue",
            )

            query_result = await handle.query("get_status")
            assert isinstance(query_result, dict)
            assert "message" in query_result
            assert "TestWorkflow" in query_result["message"]

            update_input = UpdateInput(new_value="updated_value")
            update_result = await handle.execute_update("update_value", update_input.model_dump())
            assert isinstance(update_result, dict)
            assert update_result["old_value"] == "TestWorkflow"
            assert update_result["new_value"] == "updated_value"
            assert update_result["success"] is True

            await handle.signal("add_greeting", GreetingParams(name="Alice").model_dump())
            await handle.signal("add_greeting", GreetingParams(name="Bob").model_dump())

            result = await handle.result()
            assert isinstance(result, dict)
            assert result["success"] is True
            assert "2 greetings" in result["message"]


class TestUnionInputWorkflow:
    @pytest.mark.asyncio
    async def test_prompt_input(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithUnionInput], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"prompt": "hello"},
                id="test-union-prompt",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "prompt:hello"

    @pytest.mark.asyncio
    async def test_count_input(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithUnionInput], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"count": 42},
                id="test-union-count",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "count:42"

    @pytest.mark.asyncio
    async def test_wrong_input(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithUnionInput], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"count": 42, "wrong": "key"},
                id="test-union-wrong-input",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=1),
            )
            with pytest.raises(WorkflowFailureError):
                await handle.result()


class TestOptionalUnionInputWorkflow:
    @pytest.mark.asyncio
    async def test_prompt_input(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithOptionalUnionInput], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithOptionalUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"prompt": "hello"},
                id="test-optional-union-prompt",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "prompt:hello"

    @pytest.mark.asyncio
    async def test_count_input(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithOptionalUnionInput], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithOptionalUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"count": 7},
                id="test-optional-union-count",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "count:7"

    @pytest.mark.asyncio
    async def test_wrong_input(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowWithOptionalUnionInput], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithOptionalUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"count": 7, "wrong": "key"},
                id="test-optional-union-wrong-input",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=1),
            )
            with pytest.raises(WorkflowFailureError):
                await handle.result()

    @pytest.mark.asyncio
    async def test_none_input(self, temporal_env: Any) -> None:
        """Passing None (null payload) should resolve to params=None in the handler."""
        async with create_test_worker(temporal_env, workflows=[WorkflowWithOptionalUnionInput], activities=[]):
            workflow_def = get_workflow_definition(WorkflowWithOptionalUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                None,
                id="test-optional-union-none",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "none"


# -- Workflows for input variety tests --


@workflow.define(name="workflow_no_params")
class WorkflowNoParams:
    @workflow.entrypoint
    async def run(self) -> str:
        return "no_params"


@workflow.define(name="workflow_single_int_default")
class WorkflowSingleIntDefault:
    @workflow.entrypoint
    async def run(self, value: int = 0) -> str:
        return f"value:{value}"


@workflow.define(name="workflow_single_str_default")
class WorkflowSingleStrDefault:
    @workflow.entrypoint
    async def run(self, text: str = "") -> str:
        return f"text:{text}"


@workflow.define(name="workflow_single_bool_default")
class WorkflowSingleBoolDefault:
    @workflow.entrypoint
    async def run(self, flag: bool = False) -> str:
        return f"flag:{flag}"


@workflow.define(name="workflow_single_required_str")
class WorkflowSingleRequiredStr:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        return f"name:{name}"


@workflow.define(name="workflow_single_basemodel")
class WorkflowSingleBaseModel:
    @workflow.entrypoint
    async def run(self, params: SimpleInput) -> str:
        return f"msg:{params.message}"


class TestNoParamWorkflow:
    @pytest.mark.asyncio
    async def test_no_params_no_arg(self, temporal_env: Any) -> None:
        """Workflow with no params, started with no arg."""
        async with create_test_worker(temporal_env, workflows=[WorkflowNoParams], activities=[]):
            workflow_def = get_workflow_definition(WorkflowNoParams)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                id="test-no-params-no-arg",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "no_params"

    @pytest.mark.asyncio
    async def test_no_params_empty_dict(self, temporal_env: Any) -> None:
        """Workflow with no params, started with {}."""
        async with create_test_worker(temporal_env, workflows=[WorkflowNoParams], activities=[]):
            workflow_def = get_workflow_definition(WorkflowNoParams)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-no-params-empty-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "no_params"

    @pytest.mark.asyncio
    async def test_no_params_none(self, temporal_env: Any) -> None:
        """Workflow with no params, started with None."""
        async with create_test_worker(temporal_env, workflows=[WorkflowNoParams], activities=[]):
            workflow_def = get_workflow_definition(WorkflowNoParams)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                None,
                id="test-no-params-none",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "no_params"


class TestFalsyDefaultInputs:
    """Test workflows where the default parameter value is falsy (0, '', False).

    These are started with the falsy value explicitly to verify it is not
    accidentally coerced to {}.
    """

    @pytest.mark.asyncio
    async def test_int_zero_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleIntDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleIntDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"value": 0},
                id="test-int-zero-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "value:0"

    @pytest.mark.asyncio
    async def test_int_nonzero_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleIntDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleIntDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"value": 42},
                id="test-int-nonzero-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "value:42"

    @pytest.mark.asyncio
    async def test_int_default_via_empty_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleIntDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleIntDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-int-default-empty-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "value:0"

    @pytest.mark.asyncio
    async def test_empty_string_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleStrDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleStrDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"text": ""},
                id="test-empty-str-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "text:"

    @pytest.mark.asyncio
    async def test_nonempty_string_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleStrDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleStrDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"text": "hello"},
                id="test-nonempty-str-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "text:hello"

    @pytest.mark.asyncio
    async def test_false_bool_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleBoolDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleBoolDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"flag": False},
                id="test-false-bool-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "flag:False"

    @pytest.mark.asyncio
    async def test_true_bool_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleBoolDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleBoolDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"flag": True},
                id="test-true-bool-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "flag:True"


class TestRawPositionalArg:
    """Test workflows started with a raw positional arg (not a dict).

    Temporal's start_workflow(name, arg, ...) passes `arg` directly to the
    workflow wrapper. The conversion layer must handle non-dict values.
    """

    @pytest.mark.asyncio
    async def test_int_zero_as_raw_arg(self, temporal_env: Any) -> None:
        """Falsy int 0 passed as raw arg must not break the workflow."""
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleIntDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleIntDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                0,
                id="test-raw-int-zero",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "value:0"

    @pytest.mark.asyncio
    async def test_int_nonzero_as_raw_arg(self, temporal_env: Any) -> None:
        """Truthy int passed as raw arg."""
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleIntDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleIntDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                42,
                id="test-raw-int-nonzero",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "value:42"

    @pytest.mark.asyncio
    async def test_empty_string_as_raw_arg(self, temporal_env: Any) -> None:
        """Falsy empty string passed as raw arg."""
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleStrDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleStrDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                "",
                id="test-raw-empty-str",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "text:"

    @pytest.mark.asyncio
    async def test_nonempty_string_as_raw_arg(self, temporal_env: Any) -> None:
        """Truthy string passed as raw arg."""
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleStrDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleStrDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                "hello",
                id="test-raw-nonempty-str",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "text:hello"

    @pytest.mark.asyncio
    async def test_false_as_raw_arg(self, temporal_env: Any) -> None:
        """Falsy False passed as raw arg."""
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleBoolDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleBoolDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                False,
                id="test-raw-false",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "flag:False"

    @pytest.mark.asyncio
    async def test_true_as_raw_arg(self, temporal_env: Any) -> None:
        """Truthy True passed as raw arg."""
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleBoolDefault], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleBoolDefault)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                True,
                id="test-raw-true",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "flag:True"

    @pytest.mark.asyncio
    async def test_string_as_raw_arg_for_required_param(self, temporal_env: Any) -> None:
        """Required string param passed as raw arg."""
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleRequiredStr], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleRequiredStr)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                "Alice",
                id="test-raw-required-str",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "name:Alice"


class TestSingleRequiredParam:
    @pytest.mark.asyncio
    async def test_string_param_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleRequiredStr], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleRequiredStr)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"name": "Alice"},
                id="test-required-str-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "name:Alice"


class TestBaseModelParam:
    @pytest.mark.asyncio
    async def test_basemodel_via_dict(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleBaseModel], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleBaseModel)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"message": "hello"},
                id="test-basemodel-dict",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "msg:hello"

    @pytest.mark.asyncio
    async def test_basemodel_via_model_dump(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[WorkflowSingleBaseModel], activities=[]):
            workflow_def = get_workflow_definition(WorkflowSingleBaseModel)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                SimpleInput(message="world").model_dump(),
                id="test-basemodel-model-dump",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"] == "msg:world"


class PageState(BaseModel):
    offset: int = 0
    total: int = 0


class PageResult(BaseModel):
    total: int
    done: bool = True


@activity()
async def fetch_page(offset: int) -> list[str]:
    if offset >= 200:
        return []
    return [f"item_{i}" for i in range(offset, min(offset + 100, 200))]


@workflow.define(name="workflow_continue_as_new_recursive")
class WorkflowContinueAsNewRecursive:
    @workflow.entrypoint
    async def run(self, state: PageState) -> PageResult:
        items = await fetch_page(state.offset)
        if not items:
            return PageResult(total=state.total)
        next_state = PageState(offset=state.offset + 100, total=state.total + len(items))
        workflow.continue_as_new(next_state)


class TestContinueAsNewBaseModelInstance:
    @pytest.mark.asyncio
    async def test_continue_as_new_with_basemodel(self, temporal_env: Any) -> None:
        """workflow.continue_as_new(PageState(...)) restarts the workflow with fresh history.
        The conversion layer must handle BaseModel params correctly."""
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowContinueAsNewRecursive],
            activities=[fetch_page],
        ):
            workflow_def = get_workflow_definition(WorkflowContinueAsNewRecursive)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                PageState(offset=100, total=100).model_dump(),
                id="test-continue-as-new-basemodel",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["total"] == 200
            assert result["done"] is True


# -- continue-as-new workflows for various parameter shapes --


class IntCounterState(BaseModel):
    count: int = 0


@workflow.define(name="can_int_counter")
class ContinueAsNewIntCounter:
    """Single int param with default, carried via BaseModel state."""

    @workflow.entrypoint
    async def run(self, state: IntCounterState) -> int:
        if state.count >= 3:
            return state.count
        workflow.continue_as_new(IntCounterState(count=state.count + 1))


class StrAccumulatorState(BaseModel):
    text: str


@workflow.define(name="can_str_accumulator")
class ContinueAsNewStrAccumulator:
    """Single required str param."""

    @workflow.entrypoint
    async def run(self, state: StrAccumulatorState) -> str:
        if len(state.text) >= 5:
            return state.text
        workflow.continue_as_new(StrAccumulatorState(text=state.text + "x"))


class BoolFlipperState(BaseModel):
    flag: bool = False


@workflow.define(name="can_bool_flipper")
class ContinueAsNewBoolFlipper:
    """Single bool param with default. Continues-as-new once with negated value."""

    @workflow.entrypoint
    async def run(self, state: BoolFlipperState) -> bool:
        if state.flag:
            return state.flag
        workflow.continue_as_new(BoolFlipperState(flag=not state.flag))


class MultiParamState(BaseModel):
    x: int = 0
    y: int = 0
    label: str = "start"


@workflow.define(name="can_multi_param")
class ContinueAsNewMultiParam:
    """Multiple params with defaults."""

    @workflow.entrypoint
    async def run(self, state: MultiParamState) -> str:
        if state.x >= 2:
            return f"{state.label}:{state.x}:{state.y}"
        workflow.continue_as_new(MultiParamState(x=state.x + 1, y=state.y + 10, label=f"{state.label}+"))


@workflow.define(name="can_union_input")
class ContinueAsNewUnionInput:
    """Union param. Continues-as-new with a different variant."""

    @workflow.entrypoint
    async def run(self, params: PromptInput | CountInput) -> str:
        if isinstance(params, CountInput):
            return f"count:{params.count}"
        workflow.continue_as_new(CountInput(count=len(params.prompt)))


class TestContinueAsNewParameterVariety:
    """Test that workflow.continue_as_new works with various parameter shapes.

    Each workflow uses the proper continue-as-new API (not recursive self.run)
    to restart with fresh history and new parameters.
    """

    @pytest.mark.asyncio
    async def test_int_with_initial_value(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ContinueAsNewIntCounter], activities=[]):
            workflow_def = get_workflow_definition(ContinueAsNewIntCounter)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                IntCounterState(count=1).model_dump(),
                id="test-can-int",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == 3

    @pytest.mark.asyncio
    async def test_int_with_default(self, temporal_env: Any) -> None:
        """Start with default count=0."""
        async with create_test_worker(temporal_env, workflows=[ContinueAsNewIntCounter], activities=[]):
            workflow_def = get_workflow_definition(ContinueAsNewIntCounter)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                IntCounterState().model_dump(),
                id="test-can-int-default",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == 3

    @pytest.mark.asyncio
    async def test_str_required(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ContinueAsNewStrAccumulator], activities=[]):
            workflow_def = get_workflow_definition(ContinueAsNewStrAccumulator)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                StrAccumulatorState(text="ab").model_dump(),
                id="test-can-str",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "abxxx"

    @pytest.mark.asyncio
    async def test_bool_with_default(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ContinueAsNewBoolFlipper], activities=[]):
            workflow_def = get_workflow_definition(ContinueAsNewBoolFlipper)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                BoolFlipperState(flag=False).model_dump(),
                id="test-can-bool",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] is True

    @pytest.mark.asyncio
    async def test_multi_param(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ContinueAsNewMultiParam], activities=[]):
            workflow_def = get_workflow_definition(ContinueAsNewMultiParam)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                MultiParamState(x=0, y=0, label="go").model_dump(),
                id="test-can-multi",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "go++:2:20"

    @pytest.mark.asyncio
    async def test_basemodel(self, temporal_env: Any) -> None:
        """BaseModel with activity calls between continue-as-new iterations."""
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowContinueAsNewRecursive],
            activities=[fetch_page],
        ):
            workflow_def = get_workflow_definition(WorkflowContinueAsNewRecursive)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                PageState(offset=100, total=100).model_dump(),
                id="test-can-basemodel",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["total"] == 200

    @pytest.mark.asyncio
    async def test_union(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[ContinueAsNewUnionInput], activities=[]):
            workflow_def = get_workflow_definition(ContinueAsNewUnionInput)
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                PromptInput(prompt="hello").model_dump(),
                id="test-can-union",
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=5),
            )
            result = await handle.result()
            assert result["result"] == "count:5"


class TestInvalidUnionDefinition:
    def test_mixed_union_raises_at_definition_time(self) -> None:
        with pytest.raises(WorkflowsException, match="unsupported union members: str"):

            @workflow.define(name="workflow_with_invalid_union")
            class _WorkflowWithInvalidUnion:
                @workflow.entrypoint
                async def run(self, params: PromptInput | str) -> str:
                    return ""
