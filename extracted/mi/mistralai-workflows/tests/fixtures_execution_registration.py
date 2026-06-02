"""Workflow and activity definitions for execution-registration tests.

Kept separate from the test module to avoid sandbox import issues.
"""

from __future__ import annotations

from pydantic import BaseModel

from mistralai.workflows import activity, workflow
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

# Side-channel for capturing tokens seen by activities
_observed_tokens: list[str | None] = []


@activity()
async def capture_token() -> str:
    ctx = retrieve_context()
    token = ctx.execution_token if ctx else None
    _observed_tokens.append(token)
    return "ok"


@workflow.define(name="test-registration-single-activity")
class SingleActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await capture_token()


@workflow.define(name="test-registration-two-activities")
class TwoActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        await capture_token()
        await capture_token()
        return "ok"


class IterationInput(BaseModel):
    iteration: int = 0


@workflow.define(name="test-registration-continue-as-new")
class ContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: IterationInput) -> str:
        await capture_token()
        if params.iteration < 1:
            workflow.continue_as_new(IterationInput(iteration=params.iteration + 1))
        return "ok"


class ChildParams(BaseModel):
    tag: str = "child"


@workflow.define(name="test-registration-child-parent")
class ParentWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        await capture_token()
        await workflow.execute_workflow(ChildWorkflow, params=ChildParams())
        return "ok"


@workflow.define(name="test-registration-child")
class ChildWorkflow:
    @workflow.entrypoint
    async def run(self, params: ChildParams) -> str:
        return await capture_token()
