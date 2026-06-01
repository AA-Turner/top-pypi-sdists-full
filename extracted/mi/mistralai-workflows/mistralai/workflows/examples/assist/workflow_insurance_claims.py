import asyncio
import os
from textwrap import dedent
from typing import List, Literal

from mistralai.workflows.core.workflow import workflow

with workflow.unsafe.imports_passed_through():
    from mistralai.client import Mistral
from mistralai.client.models import (
    AssistantMessage,
    ChatCompletionRequest,
    DocumentURLChunk,
    OCRResponse,
    SystemMessage,
    TextChunk,
    ToolMessage,
    UserMessage,
)
from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai


class ClaimType(BaseModel):
    claim_type: Literal["medical", "auto_accident", "other"] = "other"


class ClaimStatus(BaseModel):
    status: Literal["approved", "rejected", "pending"] = "pending"


class ClaimResponseSignalParams(BaseModel):
    is_approved: bool = Field(description="Whether the claim is approved or rejected", default=False)


class WorkflowParams(BaseModel):
    attachement_urls: List[str] = Field(
        default_factory=lambda: [
            "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
        ]
    )
    email_content: str = Field(
        default=(
            "Hello, I'm John Doe. I'm calling about my medical claim for my surgery on December 10, 2025. "
            "I had a surgery on my knee and I'm not sure if I'll be able to work after that."
        )
    )


default_attachments = ["https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"]


class WorkflowOutput(BaseModel):
    final_email: str


@workflows.workflow.define(
    name="insurance_claims_workflow",
    workflow_description="Workflow to process insurance claims",
)
class InsuranceClaimsWorkflow(workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(
        self, email_content: str, attachement_urls: List[str] | None = default_attachments
    ) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        # Extract attachments content (OCR)
        attachements_content: dict[str, str] = {}
        if attachement_urls:
            async with workflows.task_from(
                state=workflows_mistralai.ChatAssistantWorkingTask(title="OCR attachments", content="")
            ) as task:
                ocr_tasks = [llm_ocr_from_url(MistralOCRParams(url=url)) for url in attachement_urls]
                responses = await asyncio.gather(*ocr_tasks)
                await task.update_state(
                    updates={"title": "OCR attachments", "content": f"Processed {len(responses)} documents"}
                )
            attachements_content = {
                url: "\n\n".join([page.markdown for page in response.pages])
                for url, response in zip(attachement_urls, responses, strict=True)
            }

        # Build full email with attachments
        documents = "\n\n".join(f"--- Document: {url}\n\n{markdown}" for url, markdown in attachements_content.items())
        full_email = dedent(
            f"""
            <received_email>
            {email_content}
            </received_email>

            <received_attachments>
            {documents}
            </received_attachments>
            """
        )

        # Classify claim type
        async with workflows.task_from(
            state=workflows_mistralai.ChatAssistantWorkingTask(title="Categorizing claim", content="")
        ) as task:
            try:
                claim_type = await llm_classify_claim_type(LLMClassifyClaimTypeParams(full_email=full_email))
            except Exception:
                await task.update_state(updates={"content": "Failed to classify claim type"})
                claim_type = await self.wait_for_input(ClaimType)
            await task.update_state(updates={"title": "Categorizing claim", "content": claim_type.claim_type})

        # Predict claim status
        async with workflows.task_from(
            state=workflows_mistralai.ChatAssistantWorkingTask(title="Predicting claim status", content="")
        ) as task:
            if claim_type.claim_type == "auto_accident":
                # Auto-approve auto accident claims
                claim_status = ClaimStatus(status="approved")
            elif claim_type.claim_type == "medical":
                # Ask for human feedback for medical claims
                claim_status = await self.wait_for_input(ClaimStatus)
            elif claim_type.claim_type == "other":
                # Reject other claims
                claim_status = ClaimStatus(status="rejected")
            else:
                raise ValueError("Invalid claim category")
            await task.update_state(updates={"content": claim_status.status})

        # Generate final email
        final_email = await llm_generate_final_email(
            GenerateEmailParams(full_email=full_email, claim_status=claim_status)
        )
        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[workflows_mistralai.TextOutput(text=final_email.content)]
        )


def get_mistral_client() -> Mistral:
    return Mistral(api_key=os.getenv("PROD_MISTRAL_API_KEY") or os.getenv("MISTRAL_API_KEY"))


class LLMClassifyClaimTypeParams(BaseModel):
    full_email: str


@workflows.activity()
async def llm_classify_claim_type(
    params: LLMClassifyClaimTypeParams,
    mistral_client: Mistral = workflows.Depends(get_mistral_client),
) -> ClaimType:
    result = await mistral_client.chat.parse_async(
        model="mistral-medium-latest",
        messages=[
            SystemMessage(content="Given the following claim, extract the category of the claim."),
            UserMessage(content=params.full_email),
        ],
        response_format=ClaimType,
    )
    if not result.choices or not result.choices[0].message or not result.choices[0].message.parsed:
        raise ValueError("No response from Mistral")
    parsed: ClaimType = result.choices[0].message.parsed
    return parsed


class GenerateEmailParams(BaseModel):
    full_email: str
    claim_status: ClaimStatus


class GenerateEmailResult(BaseModel):
    content: str


@workflows.activity()
async def llm_generate_final_email(
    params: GenerateEmailParams,
) -> GenerateEmailResult:
    messages: list[AssistantMessage | SystemMessage | ToolMessage | UserMessage] = [
        SystemMessage(content="Generate a short email to the customer with the claim conclusion."),
        UserMessage(
            content=dedent(
                f"""
                    The claim has been {params.claim_status.status}.
                    Sign the email with 'Best regards, Insurance Company'.
                    Here is the original claim information:

                    {params.full_email}
                    """
            )
        ),
    ]
    result = await workflows_mistralai.mistralai_chat_stream(
        ChatCompletionRequest(model="mistral-medium-latest", messages=messages)
    )
    if isinstance(result.content, str):
        return GenerateEmailResult(content=result.content)
    if isinstance(result.content, TextChunk):
        return GenerateEmailResult(content=result.content.text)

    raise ValueError("Expected text response")


class MistralOCRParams(BaseModel):
    mistral_model: str = "mistral-ocr-latest"
    url: str


@workflows.activity()
async def llm_ocr_from_url(
    params: MistralOCRParams,
    mistral_client: Mistral = workflows.Depends(get_mistral_client),
) -> OCRResponse:
    """Perform OCR on a document using Mistral's OCR API."""
    document = DocumentURLChunk(document_url=params.url)
    response = await mistral_client.ocr.process_async(
        model=params.mistral_model,
        document=document,
        include_image_base64=True,
    )
    return response


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([InsuranceClaimsWorkflow]))
