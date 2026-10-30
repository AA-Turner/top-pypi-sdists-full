from typing import Any, NoReturn, Type

import pytest
import temporalio.worker
from pydantic import BaseModel
from temporalio.workflow import ContinueAsNewVersioningBehavior

from mistralai.workflows import workflow
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition

from .utils import create_test_worker

# The server only uses the behavior to place the next run and does not record it in history,
# so the tests capture what the SDK hands to Temporal. The workflow runs unsandboxed so the
# interceptor shares this module's list.
captured_behaviors: list[ContinueAsNewVersioningBehavior | None] = []


class _CaptureOutboundInterceptor(temporalio.worker.WorkflowOutboundInterceptor):
    def continue_as_new(self, input: temporalio.worker.ContinueAsNewInput) -> NoReturn:
        captured_behaviors.append(input.initial_versioning_behavior)
        self.next.continue_as_new(input)


class _CaptureInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    def init(self, outbound: temporalio.worker.WorkflowOutboundInterceptor) -> None:
        super().init(_CaptureOutboundInterceptor(outbound))


class CaptureContinueAsNewInterceptor(temporalio.worker.Interceptor):
    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> Type[temporalio.worker.WorkflowInboundInterceptor]:
        return _CaptureInboundInterceptor


class AutoUpgradeState(BaseModel):
    auto_upgrade: bool | None = None
    continued: bool = False


class AutoUpgradeResult(BaseModel):
    target_version_changed: bool


@workflow.define(name="test-continue-as-new-auto-upgrade", enforce_determinism=False)
class AutoUpgradeContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, state: AutoUpgradeState) -> AutoUpgradeResult:
        if state.continued:
            return AutoUpgradeResult(target_version_changed=workflow.is_target_version_changed())
        next_state = AutoUpgradeState(auto_upgrade=state.auto_upgrade, continued=True)
        if state.auto_upgrade is None:
            workflow.continue_as_new(next_state)
        workflow.continue_as_new(next_state, auto_upgrade=state.auto_upgrade)


class TestContinueAsNewAutoUpgrade:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("auto_upgrade", "expected_behavior"),
        [
            (None, None),
            (False, None),
            (True, ContinueAsNewVersioningBehavior.AUTO_UPGRADE),
        ],
        ids=["omitted", "false", "true"],
    )
    async def test_auto_upgrade_sets_versioning_behavior(
        self,
        temporal_env: Any,
        auto_upgrade: bool | None,
        expected_behavior: ContinueAsNewVersioningBehavior | None,
    ) -> None:
        captured_behaviors.clear()
        async with create_test_worker(
            temporal_env,
            workflows=[AutoUpgradeContinueAsNewWorkflow],
            interceptors=[CaptureContinueAsNewInterceptor()],
        ):
            workflow_def = get_workflow_definition(AutoUpgradeContinueAsNewWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                AutoUpgradeState(auto_upgrade=auto_upgrade).model_dump(),
                id=f"test-continue-as-new-auto-upgrade-{auto_upgrade}",
                task_queue="test-task-queue",
            )

            result = await handle.result()

        assert captured_behaviors == [expected_behavior]
        assert result == {"target_version_changed": False}

    def test_is_target_version_changed_outside_workflow(self) -> None:
        assert workflow.is_target_version_changed() is False
