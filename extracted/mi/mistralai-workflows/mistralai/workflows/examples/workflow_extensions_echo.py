from typing import Any

from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context


class ExtensionsEchoResult(BaseModel):
    workflow_extensions: dict[str, Any]
    activity_extensions: dict[str, Any]


@workflows.activity()
async def get_extensions_activity() -> dict[str, Any]:
    context = retrieve_context()
    return context.extensions if context else {}


@workflows.workflow.define(
    name="example-extensions-echo-workflow",
    workflow_description="Echo workflow that returns extensions from both workflow and activity context",
)
class ExtensionsEchoWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> ExtensionsEchoResult:
        context = retrieve_context()
        workflow_extensions = context.extensions if context else {}
        activity_extensions = await get_extensions_activity()
        return ExtensionsEchoResult(
            workflow_extensions=workflow_extensions,
            activity_extensions=activity_extensions,
        )
