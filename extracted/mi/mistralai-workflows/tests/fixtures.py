from datetime import timedelta

import temporalio.workflow
from pydantic import BaseModel
from temporalio.exceptions import ApplicationError

import mistralai.workflows as workflows
from mistralai.workflows import activity, workflow


class GreetingParams(BaseModel):
    name: str


class GreetingResult(BaseModel):
    message: str


class UpdateInput(BaseModel):
    new_value: str


class UpdateResult(BaseModel):
    old_value: str
    new_value: str
    success: bool


class ParamsModel(BaseModel):
    name: str
    count: int = 1


class ResultModel(BaseModel):
    message: str
    success: bool = True


@activity()
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"


@activity()
async def say_goodbye(name: str) -> str:
    return f"Goodbye, {name}!"


@workflow.define(name="simple_workflow")
class SimpleWorkflow:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        result = await say_hello(name)
        return result


@workflow.define(name="multi_activity_workflow")
class MultiActivityWorkflow:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        hello = await say_hello(name)
        goodbye = await say_goodbye(name)
        return f"{hello} {goodbye}"


@workflow.define(name="pure_workflow")
class PureWorkflow:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        return f"Workflow says: {name}"


@workflow.define(name="workflow_with_display_name", workflow_display_name="My Friendly Workflow")
class WorkflowWithDisplayName:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        return f"Display name workflow says: {name}"


@workflow.define(name="failing_workflow")
class FailingWorkflow:
    @workflow.entrypoint
    async def run(self, message: str) -> str:
        # Raise a non-retryable error to prevent workflow task retries.
        # This ensures the failure event is emitted exactly once.
        raise ApplicationError(
            f"Intentional failure: {message}",
            non_retryable=True,
        )


@workflow.define(name="child_workflow")
class ChildWorkflow:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        return f"Child says: {name}"


class ChildWorkflowParams(BaseModel):
    name: str


@workflow.define(name="parent_workflow")
class ParentWorkflow:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        child_result = await workflow.execute_workflow(ChildWorkflow, params=ChildWorkflowParams(name=name))
        return f"Parent got: {child_result}"


@workflow.define(name="child_workflow_custom_execute")
class ChildWorkflowCustomExecute:
    @workflow.entrypoint
    async def execute(self, name: str) -> str:
        return f"Child with custom entrypoint says: {name}"


class PersonData(BaseModel):
    first_name: str
    last_name: str
    age: int


class ProcessingResult(BaseModel):
    full_name: str
    is_adult: bool
    message: str


class MultiParamInput(BaseModel):
    name: str
    count: int


class MultiParamWithPrefixInput(BaseModel):
    name: str
    count: int
    prefix: str


@workflow.define(name="pydantic_child_workflow")
class PydanticChildWorkflow:
    @workflow.entrypoint
    async def run(self, person: PersonData) -> ProcessingResult:
        full_name = f"{person.first_name} {person.last_name}"
        is_adult = person.age >= 18
        message = f"{full_name} is {'an adult' if is_adult else 'a minor'}"
        return ProcessingResult(full_name=full_name, is_adult=is_adult, message=message)


@workflow.define(name="pydantic_parent_workflow")
class PydanticParentWorkflow:
    @workflow.entrypoint
    async def run(self, person: PersonData) -> str:
        result = await workflows.execute_workflow(PydanticChildWorkflow, params=person)
        return f"Processed: {result.message}"


@workflow.define(name="multi_arg_child_workflow")
class MultiArgChildWorkflow:
    @workflow.entrypoint
    async def run(self, name: str, count: int) -> str:
        return f"{name} repeated {count} times: " + ", ".join([name] * count)


@workflow.define(name="multi_arg_parent_workflow")
class MultiArgParentWorkflow:
    @workflow.entrypoint
    async def run(self, name: str, count: int) -> str:
        result = await workflows.execute_workflow(MultiArgChildWorkflow, params=MultiParamInput(name=name, count=count))
        return f"Parent received: {result}"


class PrimitiveWorkflowParams(BaseModel):
    message: str


@workflow.define(name="primitive_child_workflow")
class PrimitiveChildWorkflow:
    @workflow.entrypoint
    async def run(self, message: str) -> str:
        return f"Echo: {message}"


@workflow.define(name="primitive_parent_workflow")
class PrimitiveParentWorkflow:
    @workflow.entrypoint
    async def run(self, message: str) -> str:
        result = await workflows.execute_workflow(
            PrimitiveChildWorkflow, params=PrimitiveWorkflowParams(message=message)
        )
        return f"Got back: {result}"


class NestedWorkflowParams(BaseModel):
    value: str


@workflow.define(name="nested_child_level_2")
class NestedChildLevel2:
    @workflow.entrypoint
    async def run(self, value: str) -> str:
        return f"L2[{value}]"


@workflow.define(name="nested_child_level_1")
class NestedChildLevel1:
    @workflow.entrypoint
    async def run(self, value: str) -> str:
        result = await workflows.execute_workflow(NestedChildLevel2, params=NestedWorkflowParams(value=value))
        return f"L1[{result}]"


@workflow.define(name="nested_parent_workflow")
class NestedParentWorkflow:
    @workflow.entrypoint
    async def run(self, value: str) -> str:
        result = await workflows.execute_workflow(NestedChildLevel1, params=NestedWorkflowParams(value=value))
        return f"L0[{result}]"


@workflow.define(name="standalone_workflow_with_pydantic")
class StandaloneWorkflowWithPydantic:
    @workflow.entrypoint
    async def run(self, person: PersonData) -> ProcessingResult:
        full_name = f"{person.first_name} {person.last_name}"
        is_adult = person.age >= 18
        message = f"Standalone: {full_name} is {'an adult' if is_adult else 'a minor'}"
        return ProcessingResult(full_name=full_name, is_adult=is_adult, message=message)


@workflow.define(name="standalone_workflow_with_multi_args")
class StandaloneWorkflowWithMultiArgs:
    @workflow.entrypoint
    async def run(self, name: str, count: int, prefix: str) -> str:
        items = ", ".join([f"{prefix}{name}" for _ in range(count)])
        return f"Generated: {items}"


class FireAndForgetChildParams(BaseModel):
    tag: str


@workflow.define(name="fire_and_forget_child")
class FireAndForgetChildWorkflow:
    @workflow.entrypoint
    async def run(self, tag: str) -> str:
        return f"child-done:{tag}"


@workflow.define(name="fire_and_forget_parent")
class FireAndForgetParentWorkflow:
    @workflow.entrypoint
    async def run(self, tag: str) -> str:
        await workflow.execute_workflow(
            FireAndForgetChildWorkflow,
            params=FireAndForgetChildParams(tag=tag),
            wait=False,
        )
        return f"parent-done:{tag}"


@workflow.define(name="start_then_await_parent")
class StartThenAwaitParentWorkflow:
    @workflow.entrypoint
    async def run(self, tag: str) -> str:
        handle = await workflow.execute_workflow(
            FireAndForgetChildWorkflow,
            params=FireAndForgetChildParams(tag=tag),
            wait=False,
        )
        child_result = await handle
        return f"parent-got:{child_result}"


@workflow.define(name="compare_wait_modes_parent")
class CompareWaitModesParentWorkflow:
    """Parent that calls the same child with wait=True and wait=False, returning both results for comparison."""

    @workflow.entrypoint
    async def run(self, tag: str) -> dict:
        wait_true_result = await workflow.execute_workflow(
            FireAndForgetChildWorkflow,
            params=FireAndForgetChildParams(tag=tag),
            wait=True,
        )

        handle = await workflow.execute_workflow(
            FireAndForgetChildWorkflow,
            params=FireAndForgetChildParams(tag=tag),
            wait=False,
        )
        wait_false_result = await handle

        return {
            "wait_true": wait_true_result,
            "wait_false": wait_false_result,
        }


@workflow.define(name="compare_wait_modes_pydantic_parent")
class CompareWaitModesPydanticParentWorkflow:
    """Parent that calls PydanticChildWorkflow with wait=True and wait=False, returning both for comparison."""

    @workflow.entrypoint
    async def run(self, person: PersonData) -> dict:
        wait_true_result = await workflow.execute_workflow(
            PydanticChildWorkflow,
            params=person,
            wait=True,
        )

        handle = await workflow.execute_workflow(
            PydanticChildWorkflow,
            params=person,
            wait=False,
        )
        wait_false_result = await handle

        return {
            "wait_true": wait_true_result.model_dump(),
            "wait_false": wait_false_result.model_dump(),
        }


@workflow.define(name="failing_child_wait_true_parent")
class FailingChildWaitTrueParent:
    @workflow.entrypoint
    async def run(self, message: str) -> str:
        result = await workflow.execute_workflow(
            FailingWorkflow,
            params=PrimitiveWorkflowParams(message=message),
            wait=True,
        )
        return f"Should not reach: {result}"


@workflow.define(name="failing_child_wait_false_parent")
class FailingChildWaitFalseParent:
    @workflow.entrypoint
    async def run(self, message: str) -> str:
        handle = await workflow.execute_workflow(
            FailingWorkflow,
            params=PrimitiveWorkflowParams(message=message),
            wait=False,
        )
        result = await handle
        return f"Should not reach: {result}"


@workflow.define(name="workflow_with_pydantic_handlers")
class WorkflowWithPydanticHandlers:
    def __init__(self) -> None:
        self.current_value = "initial"
        self.greetings: list[str] = []

    @workflow.entrypoint
    async def run(self, params: ParamsModel) -> ResultModel:
        self.current_value = params.name
        await workflow.wait_condition(lambda: len(self.greetings) >= params.count)
        return ResultModel(message=f"Processed {params.name} with {len(self.greetings)} greetings", success=True)

    @workflow.signal()
    async def add_greeting(self, params: GreetingParams) -> None:
        self.greetings.append(params.name)

    @workflow.query()
    def get_status(self) -> GreetingResult:
        return GreetingResult(message=f"Current: {self.current_value}, greetings: {len(self.greetings)}")

    @workflow.update()
    async def update_value(self, input_data: UpdateInput) -> UpdateResult:
        old = self.current_value
        self.current_value = input_data.new_value
        return UpdateResult(old_value=old, new_value=self.current_value, success=True)


class DeclaredTimeoutChildParams(BaseModel):
    tag: str


@workflow.define(name="reports_execution_timeout_child", execution_timeout=timedelta(seconds=2))
class ReportsExecutionTimeoutChild:
    @workflow.entrypoint
    async def run(self, tag: str) -> float:
        timeout = temporalio.workflow.info().execution_timeout
        return timeout.total_seconds() if timeout is not None else -1.0


@workflow.define(name="reports_timeout_parent")
class ReportsTimeoutParent:
    @workflow.entrypoint
    async def run(self, tag: str) -> float:
        return await workflow.execute_workflow(
            ReportsExecutionTimeoutChild,
            params=DeclaredTimeoutChildParams(tag=tag),
            wait=True,
        )


@workflow.define(name="reports_timeout_override_parent")
class ReportsTimeoutOverrideParent:
    @workflow.entrypoint
    async def run(self, tag: str) -> float:
        return await workflow.execute_workflow(
            ReportsExecutionTimeoutChild,
            params=DeclaredTimeoutChildParams(tag=tag),
            execution_timeout=timedelta(minutes=30),
            wait=True,
        )
