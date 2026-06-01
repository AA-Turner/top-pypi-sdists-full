import asyncio

from mistralai.client.models import DocumentURLChunk, OCRRequest
from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai


class WorkflowParams(BaseModel):
    model: str = Field(default="mistral-ocr-latest", description="The OCR model to use")
    document_url: str = Field(
        default="https://arxiv.org/pdf/2201.04234",
        description="URL of the document to process",
    )


@workflows.workflow.define(
    name="extract-markdown-workflow",
    workflow_display_name="extract-markdown-workflow",
    workflow_description="Workflow example using Mistral OCR to extract markdown from documents",
)
class OCRWorkflow(workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        document_url = params.document_url
        model = params.model

        async with workflows.task_from(
            state=workflows_mistralai.ChatAssistantWorkingTask(title="Processing document with OCR", content="")
        ) as task:
            ocr_request = OCRRequest(
                model=model,
                document=DocumentURLChunk(document_url=document_url),
                include_image_base64=False,
            )
            ocr_response = await workflows_mistralai.mistralai_ocr(ocr_request)

            # Extract markdown from all pages
            markdown_pages = [page.markdown for page in ocr_response.pages]
            combined_markdown = "\n\n---\n\n".join(markdown_pages)

            await task.update_state(
                updates={
                    "title": f"OCR completed ({len(ocr_response.pages)} pages)",
                    "content": f"Extracted text from {len(ocr_response.pages)} pages",
                }
            )

        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[workflows_mistralai.TextOutput(text=combined_markdown)]
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([OCRWorkflow]))
