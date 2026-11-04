"""Harness-typed inputs of the message Workflow Updates.

Their Update names and verdicts are in ``commands``. Kept out of the package ``__init__``, which
imports no Harness module.
"""

from uuid import UUID

from pydantic import Field

from mistralai.vibe.harness.app_server.session.models.common import HistoryEntryId
from mistralai.vibe_agents.session_workflow.inputs import WorkflowUserMessage


class _UserMessageUpdateInput(WorkflowUserMessage):
    """A message Update's user message: the Harness user-message procedure params without
    ``session_id`` and ``idempotency_key``, plus ``source`` and ``metadata``."""

    message_entry_id: HistoryEntryId | None = None
    # The surface that sent the message.
    source: str


class SendMessageInput(_UserMessageUpdateInput):
    """Input of ``send_message``: start a Turn, or steer the running one.

    The Workflow derives the command id and any new Turn id from the Session and
    ``idempotency_key``, so a retry with the same key names the same message. The Workflow names
    the user message entry the same way, unless ``message_entry_id`` is set.
    """

    idempotency_key: str = Field(min_length=1)


class StartTurnInput(_UserMessageUpdateInput):
    """Input of ``start_turn``: start a Turn, only while none runs.

    ``command_id`` names the Turn, and the message entry unless ``message_entry_id`` is set. The
    caller derives it with ``sdk_command_id``, so the route and the ``/commands`` fallback name
    one command.
    """

    command_id: UUID


class SteerTurnInput(_UserMessageUpdateInput):
    """Input of ``steer_turn``: steer ``expected_turn_id``, only while it is the active Turn.

    ``command_id`` names the message entry unless ``message_entry_id`` is set, derived as for
    ``StartTurnInput``.
    """

    command_id: UUID
    expected_turn_id: str = Field(min_length=1)


type MessageUpdateInput = SendMessageInput | StartTurnInput | SteerTurnInput


__all__ = ["MessageUpdateInput", "SendMessageInput", "StartTurnInput", "SteerTurnInput"]
