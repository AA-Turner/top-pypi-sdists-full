"""Le Chat conversational utilities for Mistral Workflows.

Generic conversational UI primitives (forms, chat inputs, todo lists,
confirmations, canvas inputs) live in ``mistralai.workflows.conversational``
and are re-exported here for backward compatibility.

Mistral-specific components that are tightly coupled to the Le Chat UI
(canvas resources, UI components, assistant messages, structured output)
are defined directly in this module.
"""

import uuid
from typing import Any, Literal, Sequence, TypeVar, overload

from pydantic import BaseModel, ConfigDict, Field

from mistralai.workflows.conversational import (  # noqa: F401
    ACCEPT_OPTION_VALUE,
    DECLINE_OPTION_VALUE,
    AcceptChoice,
    AcceptDeclineChoice,
    AcceptDeclineConfirmation,
    CanvasInput,
    CanvasInputData,
    CanvasInputModel,
    ChatAssistantWorkingTask,
    ChatInput,
    ChatInputMessageContent,
    ChatInputModel,
    CommandResult,
    CommandResultFailed,
    CommandResultRunning,
    CommandResultSuccess,
    CommandToolUIState,
    ConfirmationInput,
    ConfirmationInputModel,
    CreateFileOperation,
    DateField,
    DateTimeField,
    DeclineChoice,
    DeleteFileOperation,
    FileField,
    FileOperation,
    FileToolUIState,
    FileWithMetadataValue,
    FormInput,
    GenericToolUIState,
    MultiChoice,
    NumberField,
    ReplaceFileOperation,
    SearchReplaceBlock,
    SingleChoice,
    TextChunk,
    TextField,
    TextOutput,
    TodoList,
    TodoListItem,
    TodoListItemState,
    TodoListItemStatus,
    TodoListState,
    ToolResult,
    ToolResultFailed,
    ToolResultPending,
    ToolResultRunning,
    ToolResultSuccess,
    ToolUIState,
    input_tag,
    is_accepted,
)
from mistralai.workflows.core.task.task import Task

from .conversational_ui_components import LLM_UI_VERSION, UIComponent

LE_CHAT_INPUT_TAG = "le-chat-input"


_ModelT = TypeVar("_ModelT", bound=BaseModel)


def le_chat_input(cls: type[_ModelT]) -> type[_ModelT]:
    """Mark a Pydantic model as the Le Chat conversational input.

    Shorthand for ``@input_tag("le-chat-input")``.

    Example::

        @conversational_input
        class MyWorkflowInput(BaseModel):
            message: ChatInputMessageContent
    """
    return input_tag(LE_CHAT_INPUT_TAG)(cls)


class CanvasPayload(BaseModel):
    type: Literal[
        "text/markdown",
        "text/html",
        "image/svg+xml",
        "slides",
        "react",
        "code",
        "mermaid",
    ]
    title: str
    content: str
    language: str | None = None


class CanvasResource(BaseModel):
    uri: str = Field(default_factory=lambda: f"file://canvas/{uuid.uuid4()}")
    mimeType: Literal["application/vnd.mistral.canvas"] = "application/vnd.mistral.canvas"
    canvas: CanvasPayload
    readonly: bool = False


class UIComponentResource(BaseModel):
    mimeType: Literal["application/vnd.mistral.ui-component"] = "application/vnd.mistral.ui-component"
    component: UIComponent
    version: str = LLM_UI_VERSION
    display: Literal["inline", "block"] = "block"


class ResourceOutput(BaseModel):
    type: Literal["resource"] = "resource"
    resource: CanvasResource | UIComponentResource


ContentChunk = TextOutput | ResourceOutput


class _AssistantMessageState(BaseModel):
    """Internal state for assistant message custom task events."""

    model_config = ConfigDict(title="assistant_message")
    contentChunks: list[ContentChunk] = Field(default_factory=list)


@overload
async def send_assistant_message(
    text: str,
    *,
    canvas: CanvasResource | None = None,
) -> None: ...


@overload
async def send_assistant_message(
    text: Sequence[ContentChunk],
) -> None: ...


async def send_assistant_message(
    text: str | Sequence[ContentChunk],
    *,
    canvas: CanvasResource | None = None,
) -> None:
    """Send an assistant message to the user.

    This function allows workflows to send messages to users before requesting input,
    improving the conversational experience. The message appears in the chat as if
    sent by an assistant.

    Args:
        text: Either a text string or a sequence of content chunks.
        canvas: Optional canvas resource to include alongside the text (only when passing a string).

    Example:
        ```python
        await send_assistant_message("Please provide your favorite Pokemon:")

        await send_assistant_message(
            "Here is your document draft:",
            canvas=CanvasResource(
                canvas=CanvasPayload(type="text/markdown", title="Draft", content="# Hello"),
            ),
        )

        await send_assistant_message([
            TextOutput(text="Here is the report:"),
            ResourceOutput(resource=CanvasResource(
                canvas=CanvasPayload(type="text/markdown", title="Draft", content="# Hello"),
            )),
        ])
        ```
    """
    if isinstance(text, str):
        chunks: list[ContentChunk] = [TextOutput(text=text)]
        if canvas is not None:
            chunks.append(ResourceOutput(resource=canvas))
    else:
        chunks = list(text)
    async with Task[_AssistantMessageState](
        type="assistant_message",
        state=_AssistantMessageState(contentChunks=chunks),
    ):
        pass


class ChatAssistantWorkflowOutput(BaseModel):
    content: list[ContentChunk] = Field(default_factory=list)
    structuredContent: dict[str, Any] | None = None
    isError: bool | None = None
