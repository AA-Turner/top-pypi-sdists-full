"""Workflow and activity definitions for executor credentials lifecycle tests.

This file is kept separate from the test module because Temporal's sandbox
re-imports the module where workflow classes are defined. The test module
imports httpx at the top level, which is restricted in the sandbox.
"""

from __future__ import annotations

import asyncio

from pydantic import BaseModel

from mistralai.workflows import Depends, activity, workflow

_interleave_events: dict[str, asyncio.Event] | None = None
_activity_log: list[tuple[str, str]] = []


def _get_hooked_client():
    # Deferred import: the Temporal sandbox re-imports this module to validate
    # workflow definitions and httpx is restricted inside the sandbox.
    import httpx

    from mistralai.workflows.core.auth import StaticTokenProvider
    from mistralai.workflows.hooks.executor_credentials_hook import AsyncExecutorCredentialsHook

    hook = AsyncExecutorCredentialsHook(server_url="http://mint-server", token_provider=StaticTokenProvider("test-key"))
    return httpx.AsyncClient(
        event_hooks={"request": [hook]},
        transport=httpx.MockTransport(lambda req: httpx.Response(200, json={"ok": True})),
    )


@activity()
async def api_call(client=Depends(_get_hooked_client)) -> dict:
    response = await client.get("http://api/data")
    return response.json()


@activity()
async def api_call_own_client() -> dict:
    import httpx

    from mistralai.workflows.core.auth import StaticTokenProvider
    from mistralai.workflows.hooks.executor_credentials_hook import AsyncExecutorCredentialsHook

    hook = AsyncExecutorCredentialsHook(server_url="http://mint-server", token_provider=StaticTokenProvider("test-key"))
    async with httpx.AsyncClient(
        event_hooks={"request": [hook]},
        transport=httpx.MockTransport(lambda req: httpx.Response(200, json={"ok": True})),
    ) as client:
        response = await client.get("http://api/data")
        return response.json()


class _RetryCounter:
    def __init__(self) -> None:
        self.count = 0


def _get_retry_counter() -> _RetryCounter:
    return _RetryCounter()


@activity()
async def api_call_fail_once(
    client=Depends(_get_hooked_client),
    counter=Depends(_get_retry_counter),
) -> dict:
    from temporalio.exceptions import ApplicationError

    counter.count += 1
    response = await client.get("http://api/data")
    if counter.count == 1:
        raise ApplicationError("transient failure")
    return response.json()


@workflow.define(name="test-lifecycle-single-activity", on_behalf_of=True)
class SingleActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict:
        return await api_call()


@workflow.define(name="test-lifecycle-two-activities", on_behalf_of=True)
class TwoActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict:
        await api_call()
        return await api_call()


@workflow.define(name="test-lifecycle-two-own-clients", on_behalf_of=True)
class TwoOwnClientWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict:
        await api_call_own_client()
        return await api_call_own_client()


@workflow.define(name="test-lifecycle-retry", on_behalf_of=True)
class RetryWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict:
        return await api_call_fail_once()


@activity()
async def api_call_sync_point(client=Depends(_get_hooked_client)) -> dict:
    from temporalio import activity as temporal_activity

    wf_id = temporal_activity.info().workflow_id
    _activity_log.append((wf_id, "api_call_sync_point"))
    response = await client.get("http://api/data")
    if _interleave_events is not None:
        my_event = _interleave_events[wf_id]
        other_events = [e for k, e in _interleave_events.items() if k != wf_id]
        my_event.set()
        for e in other_events:
            await e.wait()
    return response.json()


@activity()
async def api_call_logged(client=Depends(_get_hooked_client)) -> dict:
    from temporalio import activity as temporal_activity

    wf_id = temporal_activity.info().workflow_id
    _activity_log.append((wf_id, "api_call_logged"))
    response = await client.get("http://api/data")
    return response.json()


@workflow.define(name="test-lifecycle-interleaved", on_behalf_of=True)
class InterleavedWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict:
        await api_call_sync_point()
        return await api_call_logged()


class IterationInput(BaseModel):
    iteration: int = 0


@workflow.define(name="test-lifecycle-continue-as-new", on_behalf_of=True)
class ContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: IterationInput) -> dict:
        await api_call()
        if params.iteration < 2:
            workflow.continue_as_new(IterationInput(iteration=params.iteration + 1))
        return {"done": True}
