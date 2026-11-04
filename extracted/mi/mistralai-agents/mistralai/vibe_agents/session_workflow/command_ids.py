"""Command ids the Workflow and its clients derive for the same message or command."""

from typing import Literal
from uuid import NAMESPACE_URL, UUID, uuid5

_SDK_COMMAND_ID_NAMESPACE = uuid5(NAMESPACE_URL, "mistral-agents-sdk-vibe-agents-commands")


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


__all__ = ["message_command_id", "sdk_command_id"]
