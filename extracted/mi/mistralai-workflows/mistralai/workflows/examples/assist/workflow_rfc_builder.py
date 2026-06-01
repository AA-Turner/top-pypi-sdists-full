"""
Example: RFC Builder Workflow

Demonstrates an interactive workflow for building RFC documents with:
- Todo list for tracking progress
- Form inputs for collecting structured feedback
- Working steps for showing processing status
- Canvas output with human-in-the-loop editing via CanvasInput
"""

import asyncio

from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows.conversational import (
    CanvasInput,
    ChatInput,
    FileField,
    FormInput,
    MultiChoice,
    NumberField,
    SingleChoice,
    TextField,
)


class RFCWorkflowParams(BaseModel):
    query: str = Field(
        default="Create an RFC document about the best way to build a new feature",
        description="The initial request for the RFC document",
    )


class RFCFeedbackForm(FormInput):
    title: str = TextField(description="RFC title suggestion", pattern=r"^RFC.*")
    summary: str = TextField(description="Brief summary of the proposed changes.")
    priority: str = SingleChoice(
        options=[
            ("low", "Low Priority"),
            ("medium", "Medium Priority"),
            ("high", "High Priority"),
            ("critical", "Critical Priority"),
        ],
        description="Priority level for this RFC",
    )
    estimated_effort: float = NumberField(
        description="Estimated effort in person-days",
        minimum=1,
        maximum=365,
    )
    category: str = SingleChoice(
        options=[
            ("feature", "New Feature"),
            ("improvement", "Improvement"),
            ("refactor", "Refactoring"),
            ("bugfix", "Bug Fix"),
            ("docs", "Documentation"),
            ("rfception", "République Fried Chicken"),
        ],
        description="Category of this RFC",
    )
    requires_migration: str = SingleChoice(
        options=[("yes", "Yes"), ("no", "No")],
        description="Does this require data migration?",
    )
    impacted_teams: list[str] = MultiChoice(
        options=[
            ("frontend", "Frontend"),
            ("backend", "Backend"),
            ("infra", "Infrastructure"),
            ("data", "Data"),
            ("science", "Science"),
        ],
        description="Teams impacted by this RFC",
    )
    supporting_documents: list[str] = FileField(description="Upload supporting documents", multiple=True)
    additional_notes: str = TextField(description="Any additional notes or context")


class RFCApprovalInput(FormInput):
    approved: str = SingleChoice(
        options=[
            ("approved", "Approve RFC"),
            ("needs_changes", "Needs Changes"),
            ("rejected", "Reject RFC"),
        ],
        description="Your decision",
    )
    comments: str = TextField(description="Comments on your decision")


@workflows.workflow.define(
    name="rfc_builder_workflow",
    workflow_description="Interactive workflow for building RFC documents",
)
class RFCBuilderWorkflow(workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self, params: RFCWorkflowParams) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        todo_items = [
            workflows_mistralai.TodoListItem(title="Create RFC document", description="Draft initial RFC structure"),
            workflows_mistralai.TodoListItem(title="Gather feedback", description="Collect user input on the draft"),
            workflows_mistralai.TodoListItem(title="Incorporate feedback", description="Update RFC based on feedback"),
            workflows_mistralai.TodoListItem(title="Review & edit draft", description="Review and edit the RFC canvas"),
            workflows_mistralai.TodoListItem(title="Final review", description="Complete final review and approval"),
        ]

        async with workflows_mistralai.TodoList(items=todo_items):
            async with todo_items[0]:
                async with workflows.task_from(
                    state=workflows_mistralai.ChatAssistantWorkingTask(
                        type="thinking",
                        title="Planning steps",
                        content="Analyzing the request and planning the RFC structure...",
                    )
                ):
                    await asyncio.sleep(0.5)

                await self.wait_for_input(ChatInput(prompt="Initial feedback"))

                async with workflows.task_from(
                    state=workflows_mistralai.ChatAssistantWorkingTask(
                        type="tool",
                        title="Looking at the database",
                        content="Searching for existing RFC patterns and templates...",
                    )
                ):
                    await asyncio.sleep(0.3)

                async with workflows.task_from(
                    state=workflows_mistralai.ChatAssistantWorkingTask(
                        type="thinking",
                        title="Crunching numbers",
                        content="Analyzing requirements and estimating complexity...",
                    )
                ):
                    await asyncio.sleep(0.3)

            async with todo_items[1]:
                feedback = await self.wait_for_input(
                    RFCFeedbackForm,
                    label="RFC Details - Please provide your feedback",
                )

            async with todo_items[2]:
                async with workflows.task_from(
                    state=workflows_mistralai.ChatAssistantWorkingTask(
                        type="thinking",
                        title="Taking your feedback into account",
                        content=f"Incorporating feedback: {feedback.title} with {feedback.priority} priority...",
                    )
                ):
                    await asyncio.sleep(0.5)

                rfc_content = self._generate_rfc_content(params, feedback)

                canvas_resource = workflows_mistralai.CanvasResource(
                    canvas=workflows_mistralai.CanvasPayload(
                        type="text/markdown",
                        title=feedback.title,
                        content=rfc_content,
                    ),
                )
                await workflows_mistralai.send_assistant_message(
                    "Here is your RFC draft. You can review and edit it below.",
                    canvas=canvas_resource,
                )

            async with todo_items[3]:
                edited = await self.wait_for_input(
                    CanvasInput(canvas_uri=canvas_resource.uri, prompt="Any changes or feedback?"),
                    label="Review & Edit RFC",
                )

            async with todo_items[4]:
                approval = await self.wait_for_input(
                    RFCApprovalInput,
                    label="Final Approval",
                )

                async with workflows.task_from(
                    state=workflows_mistralai.ChatAssistantWorkingTask(
                        type="thinking",
                        title="Finalizing document",
                        content="Preparing final RFC document...",
                    )
                ):
                    await asyncio.sleep(0.3)

                final_content = self._append_review(edited.canvas.content, approval)

                await workflows_mistralai.send_assistant_message("Your RFC document has been finalized.")

        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[
                workflows_mistralai.TextOutput(text="Here is your finalized **RFC document**"),
                workflows_mistralai.ResourceOutput(
                    resource=workflows_mistralai.CanvasResource(
                        canvas=workflows_mistralai.CanvasPayload(
                            type="text/markdown",
                            title=edited.canvas.title,
                            content=final_content,
                        ),
                    )
                ),
            ]
        )

    def _generate_rfc_content(
        self,
        params: RFCWorkflowParams,
        feedback: RFCFeedbackForm,
    ) -> str:
        """Generate the initial RFC document content."""
        migration_text = "Yes" if feedback.requires_migration == "yes" else "No"

        return f"""# {feedback.title}

## Metadata

| Field | Value |
|-------|-------|
| Priority | {feedback.priority.title()} |
| Category | {feedback.category.title()} |
| Estimated Effort | {feedback.estimated_effort} person-days |
| Requires Migration | {migration_text} |
| Impacted Teams | {", ".join(feedback.impacted_teams)} |

## Problem Statement

{params.query}

## Summary

{feedback.summary}

## Supporting Documents

{self._format_documents(feedback.supporting_documents)}

## Additional Notes

{feedback.additional_notes}
"""

    def _append_review(self, content: str, approval: RFCApprovalInput) -> str:
        """Append review status and comments to the RFC content."""
        status = approval.approved.replace("_", " ").title()
        return f"""{content}
## Review

| Field | Value |
|-------|-------|
| Status | {status} |

## Review Comments

{approval.comments}
"""

    def _format_documents(self, urls: list[str]) -> str:
        if not urls:
            return "None provided."
        return "\n".join(f"- [{url}]({url})" for url in urls)


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([RFCBuilderWorkflow]))
