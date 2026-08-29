"""Workflow and activity definitions for runtime search key deletion tests.

Kept separate from the test module to avoid sandbox import issues.
"""

from __future__ import annotations

from mistralai.workflows import activity, workflow


@activity()
async def untag_from_activity() -> str:
    await workflow.delete_search_keys(["activity.key"])
    return "ok"


@workflow.define(name="test-delete-search-keys-from-workflow")
class DeleteSearchKeysWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        await workflow.delete_search_keys(["customer.tier"])
        return "ok"


@workflow.define(name="test-delete-search-keys-from-activity")
class DeleteSearchKeysFromActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await untag_from_activity()


@workflow.define(name="test-delete-search-keys-invalid-from-workflow")
class DeleteInvalidSearchKeysWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        await workflow.delete_search_keys(["bad:key"])
        return "ok"
