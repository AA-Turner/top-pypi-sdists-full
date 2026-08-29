"""Workflow and activity definitions for execution-registration tests.

Kept separate from the test module to avoid sandbox import issues.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

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


class SearchKeyCustomer(BaseModel):
    name: str
    tier: int


class SearchKeyInput(BaseModel):
    id: str
    customer: SearchKeyCustomer
    note: str | None = None


@workflow.define(
    name="test-registration-search-keys",
    search_keys=["id", "customer.name", "customer.tier", "note"],
)
class SearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, payload: SearchKeyInput) -> str:
        return await capture_token()


class SearchKeyContext(BaseModel):
    tenant_name: str
    region: str | None = None


@workflow.define(
    name="test-registration-search-keys-multi",
    search_keys=["payload.id", "payload.customer.name", "context.tenant_name", "context.region"],
)
class MultiParamSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, payload: SearchKeyInput, context: SearchKeyContext) -> str:
        return await capture_token()


@workflow.define(
    name="test-registration-search-keys-scalar",
    search_keys=["city"],
)
class ScalarParamSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, city: str) -> str:
        return await capture_token()


class Tier(str, Enum):
    free = "free"
    paid = "paid"


@workflow.define(
    name="test-registration-search-keys-scalar-int",
    search_keys=["count"],
)
class ScalarIntSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, count: int) -> str:
        return await capture_token()


@workflow.define(
    name="test-registration-search-keys-scalar-enum",
    search_keys=["tier"],
)
class ScalarEnumSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, tier: Tier) -> str:
        return await capture_token()


@workflow.define(
    name="test-registration-search-keys-multi-scalar",
    search_keys=["city", "count"],
)
class MultiScalarSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, city: str, count: int) -> str:
        return await capture_token()


@workflow.define(
    name="test-registration-search-keys-mixed",
    search_keys=["city", "payload.id", "payload.customer.name"],
)
class MixedScalarModelSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, city: str, payload: SearchKeyInput) -> str:
        return await capture_token()


@workflow.define(
    name="test-registration-search-keys-single-basemodel",
    search_keys=["id", "customer.name", "customer.tier"],
)
class SingleBaseModelSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, payload: SearchKeyInput) -> str:
        return await capture_token()


class DefaultPayload(BaseModel):
    id: str = "hey"


class DefaultPayloadWithNote(BaseModel):
    id: str = "hey"
    note: str | None = "default-note"


@workflow.define(
    name="test-registration-search-keys-defaults-multi",
    search_keys=["id", "payload.id"],
)
class DefaultMultiParamSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, payload: DefaultPayload = DefaultPayload(), id: str = "hi") -> str:
        return await capture_token()


@workflow.define(
    name="test-registration-search-keys-defaults-single",
    search_keys=["id", "note"],
)
class DefaultSingleParamSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, payload: DefaultPayloadWithNote = DefaultPayloadWithNote()) -> str:
        return await capture_token()


@workflow.define(
    name="test-registration-search-keys-defaults-scalar",
    search_keys=["city"],
)
class DefaultScalarSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, city: str = "paris") -> str:
        return await capture_token()


class CoercedPayload(BaseModel):
    ratio: float = 1.0
    when: datetime | None = None


@workflow.define(
    name="test-registration-search-keys-coercion",
    search_keys=["ratio", "when"],
)
class CoercedSearchKeyWorkflow:
    @workflow.entrypoint
    async def run(self, payload: CoercedPayload) -> str:
        return await capture_token()
