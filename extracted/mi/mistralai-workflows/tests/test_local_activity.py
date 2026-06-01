from typing import Any

import pytest
import temporalio.activity
from pydantic import BaseModel

from mistralai.workflows import activity, get_workflow_definition, workflow
from mistralai.workflows.core.execution.local_activity import run_activities_locally

from .utils import create_test_worker


class SimpleParams(BaseModel):
    value: str


class ActivityResult(BaseModel):
    is_local_activity: bool


def check_is_activity_running_locally():
    info = temporalio.activity.info()
    return info.is_local


@activity()
async def activity_1(params: SimpleParams) -> ActivityResult:
    return ActivityResult(is_local_activity=check_is_activity_running_locally())


@activity()
async def activity_2(params: SimpleParams) -> ActivityResult:
    return ActivityResult(is_local_activity=check_is_activity_running_locally())


@activity()
async def activity_3(params: SimpleParams) -> ActivityResult:
    return ActivityResult(is_local_activity=check_is_activity_running_locally())


@activity()
async def activity_4(params: SimpleParams) -> ActivityResult:
    return ActivityResult(is_local_activity=check_is_activity_running_locally())


@workflow.define(name="test-full-remote-workflow")
class FullRemoteWorkflow:
    @workflow.entrypoint
    async def run(self, params: SimpleParams) -> list[ActivityResult]:
        results = [
            await activity_1(params),
            await activity_2(params),
            await activity_3(params),
        ]
        return results


@workflow.define(name="test-full-local-workflow")
class FullLocalWorkflow:
    @workflow.entrypoint
    async def run(self, params: SimpleParams) -> list[ActivityResult]:
        with run_activities_locally():
            results = [
                await activity_1(params),
                await activity_2(params),
                await activity_3(params),
            ]
        return results


@workflow.define(name="test-mixed-execution-workflow")
class MixedExecutionWorkflow:
    @workflow.entrypoint
    async def run(self, params: SimpleParams) -> list[ActivityResult]:
        results = [
            await activity_1(params)  # Remote
        ]

        with run_activities_locally():
            results.extend(
                [
                    await activity_2(params),  # Local
                    await activity_3(params),  # Local
                ]
            )

        results.append(await activity_1(params))  # Remote
        return results


class TestLocalActivities:
    @pytest.mark.asyncio
    async def test_full_remote_execution(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[FullRemoteWorkflow],
            activities=[activity_1, activity_2, activity_3],
        ):
            workflow_def = get_workflow_definition(FullRemoteWorkflow)
            assert workflow_def is not None

            params = SimpleParams(value="test-remote")

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                params.model_dump(),
                id="test-full-remote",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            results = result["result"]
            assert len(results) == 3
            for activity_result in results:
                assert activity_result["is_local_activity"] is False

    @pytest.mark.asyncio
    async def test_full_local_execution(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[FullLocalWorkflow],
            activities=[activity_1, activity_2, activity_3],
        ):
            workflow_def = get_workflow_definition(FullLocalWorkflow)
            assert workflow_def is not None

            params = SimpleParams(value="test-local")

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                params.model_dump(),
                id="test-full-local",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            results = result["result"]
            assert len(results) == 3
            for activity_result in results:
                assert activity_result["is_local_activity"] is True

    @pytest.mark.asyncio
    async def test_mixed_execution(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[MixedExecutionWorkflow],
            activities=[activity_1, activity_2, activity_3],
        ):
            workflow_def = get_workflow_definition(MixedExecutionWorkflow)
            assert workflow_def is not None

            params = SimpleParams(value="test-mixed")

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                params.model_dump(),
                id="test-mixed-execution",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            results = result["result"]
            assert len(results) == 4

            expected_is_local = [False, True, True, False]
            for i, (activity_result, expected) in enumerate(zip(results, expected_is_local)):
                assert activity_result["is_local_activity"] == expected, (
                    f"Activity {i} local={activity_result['is_local_activity']}, expected={expected}"
                )
