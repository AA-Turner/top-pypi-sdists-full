import asyncio

from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows.plugins.mistralai import ChatCompletionRequest, UserMessage


class Person(BaseModel):
    """Example schema for structured output parsing."""

    name: str = Field(..., description="Person's full name")
    age: int = Field(..., description="Person's age")
    occupation: str = Field(..., description="Person's occupation")


class WorkflowParams(BaseModel):
    model: str = Field(default="mistral-small-latest", description="The chat model to use")
    prompt: str = Field(
        default="Extract information about a person from this text: John Doe is a 35-year-old software"
        " engineer who loves Python.",
        description="Prompt for extracting structured information",
    )


@workflows.workflow.define(
    name="chat-parse-workflow",
    workflow_display_name="chat-parse-workflow",
    workflow_description="Workflow example using Mistral chat parsing to extract structured data",
)
class ChatParseWorkflow(workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        model = params.model
        prompt = params.prompt

        async with workflows.task_from(
            state=workflows_mistralai.ChatAssistantWorkingTask(
                title="Extracting structured data", content="Processing text to extract structured information..."
            )
        ) as task:
            request = ChatCompletionRequest(model=model, messages=[UserMessage(content=prompt)])
            person_data = await workflows_mistralai.chat_parse_to_model(Person, request)

            await task.update_state(
                updates={
                    "title": "Extraction completed",
                    "content": f"Successfully extracted data for {person_data.name}",
                }
            )

        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[workflows_mistralai.TextOutput(text=f"Extracted person data: {person_data.model_dump_json()}")]
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([ChatParseWorkflow]))
