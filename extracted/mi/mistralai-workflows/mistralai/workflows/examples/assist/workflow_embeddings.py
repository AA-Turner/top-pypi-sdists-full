import asyncio

from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai


class WorkflowParams(BaseModel):
    model: str = Field(default="mistral-embed", description="The embedding model to use")
    texts: list[str] = Field(
        default=["Hello, world!", "How are you?"],
        description="List of texts to embed",
    )


@workflows.workflow.define(
    name="workflow-embeddings",
    workflow_display_name="workflow-embeddings",
    workflow_description="Workflow example using Mistral Embeddings to generate text embeddings",
)
class EmbeddingsWorkflow(workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        texts = params.texts
        model = params.model

        async with workflows.task_from(
            state=workflows_mistralai.ChatAssistantWorkingTask(title="Generating embeddings", content="")
        ) as task:
            embeddings_request = workflows_mistralai.MistralEmbeddingsParams(
                model=model,
                inputs=texts,
            )
            embeddings_response = await workflows_mistralai.mistralai_embeddings(embeddings_request)

            embeddings = [data.embedding for data in embeddings_response.data if data.embedding is not None]
            total_tokens = embeddings_response.usage.total_tokens if embeddings_response.usage else 0

            await task.update_state(
                updates={
                    "title": f"Embeddings generated ({len(texts)} texts)",
                    "content": f"Generated {len(embeddings)} embeddings",
                }
            )

        result_text = f"Generated {len(embeddings)} embeddings\nModel: {model}\nTotal tokens: {total_tokens}"

        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[workflows_mistralai.TextOutput(text=result_text)]
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([EmbeddingsWorkflow]))
