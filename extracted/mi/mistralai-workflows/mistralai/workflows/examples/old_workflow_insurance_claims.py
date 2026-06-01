"""
OLD Insurance Claims Workflow Example

This file contains the OLD implementation using workflows.streaming.stream() API.
It is kept for reference to show the old way of coding things.

The new approach uses the Task API from workflows.worker.task instead.

DO NOT USE THIS CODE - it relies on deprecated streaming APIs.

---

OLD CODE (kept for reference):

```python
# 10,153 characters
# we keep it for later comparison with the new implementation
import asyncio
import os
from textwrap import dedent
from typing import Any, List, Literal

import mistralai

# Import actual mistralai types for proper type checking
from mistralai import SystemMessage, UserMessage
from pydantic import BaseModel, Field

import mistralai.workflows as workflows


class LeChatPayloadWorking(BaseModel):
    type: Literal["working"] = "working"
    name: str
    results: str | None = None


class LeChatPayloadAssistantMessage(mistralai.AssistantMessage):
    type: Literal["assistant_message"] = "assistant_message"


class LeChatPayloadHumanFeedback(BaseModel):
    type: Literal["human_feedback"] = "human_feedback"
    input_schema: dict
    input: Any | None = None


class WaitUserInputUpdateParams(BaseModel):
    custom_task_id: str
    input: Any


class WaitUserInputUpdateResult(BaseModel):
    error: str | None = None


class UserInputRequest(BaseModel):
    custom_task_id: str
    input_schema: type[BaseModel]
    received: bool = False
    input: Any | None = None


class ClaimType(BaseModel):
    claim_type: Literal["medical", "auto_accident", "other"] = "other"


class ClaimStatus(BaseModel):
    status: Literal["approved", "rejected", "pending"] = "pending"


class ClaimResponseSignalParams(BaseModel):
    is_approved: bool = Field(description="Whether the claim is approved or rejected", default=False)


class WorkflowParams(BaseModel):
    attachement_urls: List[str]
    email_content: str


class WorkflowOutput(BaseModel):
    final_email: str


@workflows.workflow.define(
    name="insurance_claims_workflow",
    workflow_description="Workflow to process insurance claims",
)
class InsuranceClaimsWorkflow:
    def __init__(self) -> None:
        self._user_input_requests: dict[str, UserInputRequest] = {}

    async def _wait_for_input(self, input_schema: type[BaseModel]) -> Any:
        \"\"\"Helper method to wait for user input with the old-style pattern.\"\"\"
        with workflows.streaming.stream("human_feedback") as feedback_stream:
            feedback_stream.publish(LeChatPayloadHumanFeedback(input_schema=input_schema.model_json_schema()))
            self._user_input_requests[feedback_stream.custom_task_id] = UserInputRequest(
                custom_task_id=feedback_stream.custom_task_id,
                input_schema=input_schema,
            )
            await workflows.workflow.wait_condition(
                lambda task_id=feedback_stream.custom_task_id: bool(
                    self._user_input_requests[task_id].received
                )  # type: ignore[misc]
            )
            user_input = input_schema.model_validate(
                self._user_input_requests[feedback_stream.custom_task_id].input
            )
            feedback_stream.publish(
                LeChatPayloadHumanFeedback(
                    input_schema=input_schema.model_json_schema(),
                    input=user_input,
                )
            )
            return user_input

    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowOutput:
        # Extract attachments content (OCR)
        attachements_content: dict[str, str] = {}
        if params.attachement_urls:
            with workflows.streaming.stream("working") as stream:
                stream.publish(LeChatPayloadWorking(name="OCR attachments"))
                ocr_tasks = [llm_ocr_from_url(MistralOCRParams(url=url)) for url in params.attachement_urls]
                responses = await asyncio.gather(*ocr_tasks)
                stream.publish(
                    LeChatPayloadWorking(name="OCR attachments", results=f"Processed {len(responses)} documents")
                )
            attachements_content = {
                url: "\\n\\n".join([page.markdown for page in response.pages])
                for url, response in zip(params.attachement_urls, responses, strict=True)
            }

        # Build full email with attachments
        documents = "\\n\\n".join(
            f"--- Document: {url}\\n\\n{markdown}" for url, markdown in attachements_content.items()
        )
        full_email = dedent(
            f\"\"\"
            <received_email>
            {params.email_content}
            </received_email>

            <received_attachments>
            {documents}
            </received_attachments>
            \"\"\"
        )

        # Classify claim type
        with workflows.streaming.stream("working") as stream:
            stream.publish(LeChatPayloadWorking(name="Categorizing claim"))
            try:
                claim_type = await llm_classify_claim_type(LLMClassifyClaimTypeParams(full_email=full_email))
            except Exception:
                claim_type = await self._wait_for_input(ClaimType)
            stream.publish(LeChatPayloadWorking(name="Categorizing claim", results=claim_type.claim_type))

        # Predict claim status
        with workflows.streaming.stream("working") as stream:
            stream.publish(LeChatPayloadWorking(name="Predicting claim status"))
            if claim_type.claim_type == "auto_accident":
                # Auto-approve auto accident claims
                claim_status = ClaimStatus(status="approved")
            elif claim_type.claim_type == "medical":
                # Ask for human feedback for medical claims
                claim_status = await self._wait_for_input(ClaimStatus)
            elif claim_type.claim_type == "other":
                # Reject other claims
                claim_status = ClaimStatus(status="rejected")
            else:
                raise ValueError("Invalid claim category")
            stream.publish(LeChatPayloadWorking(name="Predicting claim status", results=claim_status.status))

        # Generate final email
        final_email = await llm_generate_final_email(
            GenerateEmailParams(full_email=full_email, claim_status=claim_status)
        )
        return WorkflowOutput(final_email=final_email.content)

    @workflows.workflow.update(name="human_feedback")
    async def human_feedback(self, message: WaitUserInputUpdateParams) -> WaitUserInputUpdateResult:
        user_input_request = self._user_input_requests.get(message.custom_task_id)
        if not user_input_request:
            return WaitUserInputUpdateResult(error=f"Custom task {message.custom_task_id} not found")

        try:
            user_input_request.input_schema.model_validate(message.input)
        except Exception as e:
            return WaitUserInputUpdateResult(error=f"Invalid input: {e}")

        user_input_request.input = message.input
        user_input_request.received = True
        return WaitUserInputUpdateResult()


def get_mistral_client() -> mistralai.Mistral:
    return mistralai.Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


class LLMClassifyClaimTypeParams(BaseModel):
    full_email: str


@workflows.activity()
async def llm_classify_claim_type(
    params: LLMClassifyClaimTypeParams,
    mistral_client: mistralai.Mistral = workflows.Depends(get_mistral_client),
) -> ClaimType:
    with workflows.streaming.stream("assistant_message") as stream:
        stream.publish(LeChatPayloadAssistantMessage(content="Classifying claim type..."))
        result = await mistral_client.chat.parse_async(
            model="mistral-medium-latest",
            messages=[
                mistralai.SystemMessage(content="Given the following claim, extract the category of the claim."),
                mistralai.UserMessage(content=params.full_email),
            ],
            response_format=ClaimType,
        )
        if not result.choices or not result.choices[0].message or not result.choices[0].message.parsed:
            stream.publish(LeChatPayloadAssistantMessage(content="Failed to classify claim type"))
            raise ValueError("No response from Mistral")
        else:
            parsed = result.choices[0].message.parsed
            stream.publish(LeChatPayloadAssistantMessage(content=parsed.model_dump_json(indent=2)))
            return parsed


class GenerateEmailParams(BaseModel):
    full_email: str
    claim_status: ClaimStatus


class GenerateEmailResult(BaseModel):
    content: str


@workflows.activity()
async def llm_generate_final_email(
    params: GenerateEmailParams,
    mistral_client: mistralai.Mistral = workflows.Depends(get_mistral_client),
) -> GenerateEmailResult:
    with workflows.streaming.stream("assistant_message") as stream:
        assistant_message_content = ""
        stream.publish(LeChatPayloadAssistantMessage(content=assistant_message_content))
        from mistralai import AssistantMessage, ToolMessage

        messages: list[SystemMessage | UserMessage | AssistantMessage | ToolMessage] = [
            SystemMessage(content="Generate a short email to the customer with the claim conclusion."),
            UserMessage(
                content=dedent(
                    f\"\"\"
                    The claim has been {params.claim_status.status}.
                    Sign the email with 'Best regards, Insurance Company'.
                    Here is the original claim information:

                    {params.full_email}
                    \"\"\"
                )
            ),
        ]
        mistral_stream = await mistral_client.chat.stream_async(
            model="mistral-medium-latest",
            messages=messages,
        )
        async for chunk in mistral_stream.generator:
            if chunk.data.choices[0].delta.content:
                assert isinstance(chunk.data.choices[0].delta.content, str), "Non string content is not supported"
                assistant_message_content += chunk.data.choices[0].delta.content
                stream.publish(LeChatPayloadAssistantMessage(content=assistant_message_content))

        return GenerateEmailResult(content=assistant_message_content)


class MistralOCRParams(BaseModel):
    mistral_model: str = "mistral-ocr-latest"
    url: str


@workflows.activity()
async def llm_ocr_from_url(
    params: MistralOCRParams,
    mistral_client: mistralai.Mistral = workflows.Depends(get_mistral_client),
) -> mistralai.OCRResponse:
    \"\"\"Perform OCR on a document using Mistral's OCR API.\"\"\"
    document = mistralai.DocumentURLChunk(document_url=params.url)
    response = await mistral_client.ocr.process_async(
        model=params.mistral_model,
        document=document,
        include_image_base64=True,
    )
    return response


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([InsuranceClaimsWorkflow]))
```
"""
