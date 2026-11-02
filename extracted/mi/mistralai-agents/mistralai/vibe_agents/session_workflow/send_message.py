"""Input of the ``send_message`` Workflow Update, and the command ids clients derive.

Like ``session_v1_wire``, kept out of the package ``__init__``, which imports no Harness module.
"""

from typing import Literal
from uuid import NAMESPACE_URL, UUID, uuid5

from pydantic import Field

from mistralai.vibe.harness.app_server.session.models.common import HistoryEntryId
from mistralai.vibe_agents.session_workflow.inputs import WorkflowUserMessage

_SDK_COMMAND_ID_NAMESPACE = uuid5(NAMESPACE_URL, "mistral-agents-sdk-vibe-agents-commands")


class SendMessageInput(WorkflowUserMessage):
    """One user message for the ``send_message`` Update: Harness ``MessageSendParams`` without
    ``session_id``, plus ``source`` and ``metadata``.

    The Workflow derives the command id and any new Turn id from the Session and
    ``idempotency_key``, so a retry with the same key names the same message. The Workflow names
    the user message entry the same way, unless ``message_entry_id`` is set.
    """

    idempotency_key: str = Field(min_length=1)
    message_entry_id: HistoryEntryId | None = None
    # The surface that sent the message.
    source: str


def message_command_id(session_id: str, idempotency_key: str) -> str:
    """Name the message an idempotency key sends: its command, any new Turn, and its history entry
    unless the message names one.

    The Workflow names the message with it, and a client that sent the message can name it too.
    """

    # Retries of one key must name the same message, and two Sessions may use the same key.
    # Changing this derivation would make an in-flight retry send its message twice.
    return str(uuid5(UUID(session_id), f"message/send:{idempotency_key}"))


def sdk_command_id(kind: Literal["turn", "steer", "interrupt", "cancel"], value: str) -> UUID:
    """Name the command an SDK Turn or Session command sends, from its key or expected Turn.

    A procedure route and the ``/commands`` fallback derive the same id, so a retry that moves
    between them names one command, and the Worker applies it once. A started Turn carries it.
    """

    # Frozen: changing it would make an in-flight retry apply its command twice. The namespace is
    # not per Session because the Worker deduplicates within its own Session.
    return uuid5(_SDK_COMMAND_ID_NAMESPACE, f"{kind}:{value}")


__all__ = ["SendMessageInput", "message_command_id", "sdk_command_id"]
