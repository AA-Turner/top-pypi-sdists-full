import asyncio

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows import workflow
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.logging import setup_logging
from mistralai.workflows.examples.assist.workflow_insurance_claims import InsuranceClaimsWorkflow
from mistralai.workflows.examples.assist.workflow_multi_turn_chat import MultiTurnChatWorkflow
from mistralai.workflows.examples.assist.workflow_pokemon_personality import PokemonPersonalityWorkflow
from mistralai.workflows.examples.assist.workflow_rfc_builder import RFCBuilderWorkflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


@workflows.activity()
async def assist_activity(query: str) -> workflows_mistralai.ChatAssistantWorkflowOutput:
    async with workflows.task("activity.processing", {"query": query}):
        await asyncio.sleep(1)

    return workflows_mistralai.ChatAssistantWorkflowOutput(
        content=[workflows_mistralai.TextOutput(text="result1"), workflows_mistralai.TextOutput(text="result2")]
    )


@workflows.workflow.define(
    name="assist-workflow-hello-world",
    workflow_display_name="Hello World assist",
    workflow_description="Example workflow",
)
class Workflow:
    @workflows.workflow.entrypoint
    async def run(self, document_title: str) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        results = await assist_activity(document_title)
        return results


if __name__ == "__main__":
    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )
    asyncio.run(
        workflows.run_worker(
            [Workflow, PokemonPersonalityWorkflow, MultiTurnChatWorkflow, InsuranceClaimsWorkflow, RFCBuilderWorkflow]
        )
    )
