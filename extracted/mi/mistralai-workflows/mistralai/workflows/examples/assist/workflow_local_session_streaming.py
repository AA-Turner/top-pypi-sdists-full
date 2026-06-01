"""
Local Session Streaming Workflow Example

Demonstrates using the `LocalSession` with the new streaming-aware activity.
Tokens are emitted via the Task/SSE pipeline while the activity is running,
so the workflow only needs to gather the final result.
"""

import asyncio

from mistralai.client.models import TextChunk
from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflow_mistralai
from mistralai.workflows import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger()


class WorkflowParams(BaseModel):
    prompt: str = Field(description="User prompt to send to the agent")
    model: str = Field(default="mistral-medium-latest", description="Model identifier to use for completion")


class WorkflowOutput(BaseModel):
    response: str


class CityFactsParams(BaseModel):
    city: str = Field(description="City to look up")


class CityFactsResult(BaseModel):
    summary: str


@workflows.activity()
async def lookup_city_facts(params: CityFactsParams) -> CityFactsResult:
    """Simple activity to showcase tool usage."""
    city = params.city
    summary = f"{city} is renowned for its history and culture."
    return CityFactsResult(summary=summary)


@workflows.workflow.define(name="local-session-streaming-workflow")
class LocalSessionStreamingWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowOutput:
        logger.info("Workflow: starting local session streaming run", model=params.model)

        session = workflow_mistralai.LocalSession(stream=True)

        agent = workflow_mistralai.Agent(
            model=params.model,
            description="Helpful assistant that answers questions succinctly.",
            instructions=(
                "When asked about a city, call the `lookup_city_facts` tool to gather facts before responding. "
                "After receiving tool output, summarize it for the user."
            ),
            name="local-session-agent",
            tools=[lookup_city_facts],
        )

        outputs = await workflow_mistralai.Runner.run(
            agent=agent,
            inputs=params.prompt,
            session=session,
        )

        text = "".join(chunk.text for chunk in outputs if isinstance(chunk, TextChunk))
        logger.info("Workflow: completed agent run", length=len(text))
        return WorkflowOutput(response=text)


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([LocalSessionStreamingWorkflow]))
