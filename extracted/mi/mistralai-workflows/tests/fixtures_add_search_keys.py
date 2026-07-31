"""Workflow and activity definitions for runtime search key ingestion tests.

Kept separate from the test module to avoid sandbox import issues.
"""

from __future__ import annotations

from mistralai.workflows import activity, workflow


@activity()
async def tag_from_activity() -> str:
    await workflow.add_search_keys({"activity.key": "from-activity"})
    return "ok"


@workflow.define(name="test-add-search-keys-from-workflow")
class AddSearchKeysWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        await workflow.add_search_keys({"customer.tier": "gold"})
        return "ok"


@workflow.define(name="test-add-search-keys-from-activity")
class AddSearchKeysFromActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await tag_from_activity()


@workflow.define(name="test-add-search-keys-invalid-from-workflow")
class AddInvalidSearchKeysWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        await workflow.add_search_keys({"bad:key": "v"})
        return "ok"
