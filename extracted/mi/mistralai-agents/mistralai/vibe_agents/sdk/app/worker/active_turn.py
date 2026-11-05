"""Translate product message content before Runtime-owned command buffering."""

from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.content import to_core_image_content, to_model_json_text
from mistralai.vibe.harness.runtime.session.commands import (
    ContextMessage,
)
from mistralai.vibe_agents import session_workflow as wire

type ActiveTurnWireCommand = wire.MessageCommand | wire.SystemCommand


def command_content(command: wire.MessageCommand) -> list[core_protocol.ContentBlock]:
    """Translate one product message into portable Harness content blocks."""

    content: list[core_protocol.ContentBlock] = []
    for part in command.message.parts:
        if isinstance(part, wire.MessagePartText):
            content.append(core_protocol.TextContentBlock(text=part.text))
        elif isinstance(part, wire.MessagePartImage):
            content.append(to_core_image_content(part.image_url))
        elif isinstance(part, wire.MessagePartResourceLink):
            content.append(
                core_protocol.ResourceLinkContentBlock(
                    uri=part.uri,
                    name=part.name or "resource",
                    mime_type=part.mime_type,
                    # Products put their own keys on links; Harness content carries only what it models.
                    annotations=None
                    if part.annotations is None
                    else core_protocol.ContentAnnotations.model_validate(part.annotations, extra="ignore"),
                )
            )
        elif isinstance(part, wire.MessagePartForm):
            values = to_model_json_text(part.values)
            content.append(
                core_protocol.TextContentBlock(
                    text=f"[form: {part.form_id}]\n{values}",
                )
            )
    if not content:
        content.append(core_protocol.TextContentBlock(text=""))
    return content


def context_messages(command: wire.MessageCommand) -> list[ContextMessage]:
    """Translate private product context into Harness context messages."""

    if command.context is None:
        return []
    return [ContextMessage(content=[core_protocol.TextContentBlock(text=command.context.summary)])]


__all__ = [
    "ActiveTurnWireCommand",
    "command_content",
    "context_messages",
]
