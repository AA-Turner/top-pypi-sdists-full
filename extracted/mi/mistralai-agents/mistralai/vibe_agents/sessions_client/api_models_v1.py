"""Pydantic boundary models for the Session v1 endpoints of the vibe_agents sessions HTTP API.

The Session v1 counterpart of ``api_models``: these endpoints speak the Harness wire models. The
client imports this module on first use, so importing ``sessions_client`` (as Workflow code does)
does not load the Harness.
"""

from typing import Annotated, get_args

from pydantic import AfterValidator, BeforeValidator, ConfigDict, Field

from mistralai.vibe.harness.app_server.session import (
    CallbackResult,
    CallbacksTreeResponse,
    MessageSendResponse,
    SessionModel,
    TreeCallback,
    UserMessageInput,
)
from mistralai.vibe.harness.app_server.session.models.callbacks import CallbackKind
from mistralai.vibe.harness.app_server.session.models.common import (
    DEFAULT_INTERRUPT_REASON,
    HistoryEntryId,
    TurnId,
)
from mistralai.vibe_agents.session_workflow.commands import require_canonical_source

_KNOWN_CALLBACK_KINDS = frozenset(get_args(CallbackKind.__value__))


# The surface that sent the command, such as ``vibe_code_web`` or ``slack``. The Harness params have
# no such field.
type CommandSource = Annotated[str, AfterValidator(require_canonical_source)]


# Used as sent, never stripped: the Session derives the command id from it, as the SDK's
# ``/commands`` fallback does.
type ProcedureIdempotencyKey = Annotated[str, Field(min_length=1, max_length=256, pattern=r"\S")]


# The bodies of the Session protocol routes, ``POST /sessions/{id}/<procedure>``: the Harness
# params without ``session_id``, which the path carries. The controller takes them as its request
# bodies, so client and server cannot drift. Each sets ``extra="forbid"`` as a server-side request.


class UserMessageRequest(UserMessageInput):
    """The fields every user-message procedure takes: Harness ``message``, ``context_messages``,
    ``idempotency_key`` and ``message_entry_id``, plus ``source``."""

    model_config = ConfigDict(extra="forbid")

    idempotency_key: ProcedureIdempotencyKey = Field(
        description=(
            "An exact retry with the same key returns the original receipt. Use a UUID or a similar "
            "random value. Reusing it with another message, entry id or context messages returns "
            "409 idempotency_conflict."
        ),
    )
    message_entry_id: HistoryEntryId | None = None
    # Required although Session v1 history does not store it yet: requiring it later would break
    # callers.
    source: CommandSource


class MessageSendRequest(UserMessageRequest):
    """Body of ``message/send``. The command id is ``message_command_id(session_id, idempotency_key)``."""


class TurnStartRequest(UserMessageRequest):
    """Body of ``turn/start``. The Turn id is ``sdk_command_id("turn", idempotency_key)``."""


class TurnSteerRequest(UserMessageRequest):
    """Body of ``turn/steer``. The command id is ``sdk_command_id("steer", idempotency_key)``."""

    expected_turn_id: TurnId


class TurnInterruptRequest(SessionModel):
    """Body of ``turn/interrupt``. The command id is ``sdk_command_id("interrupt", expected_turn_id)``."""

    model_config = ConfigDict(extra="forbid")

    expected_turn_id: TurnId
    reason: str = DEFAULT_INTERRUPT_REASON
    source: CommandSource


class SessionCancelRequest(SessionModel):
    """Body of ``cancel``. The command id is ``sdk_command_id("cancel", idempotency_key)``."""

    model_config = ConfigDict(extra="forbid")

    idempotency_key: ProcedureIdempotencyKey
    reason: str = "cancel requested"
    source: CommandSource


class CallbackResultRequest(SessionModel):
    """Body of ``callback/result``. The callback id is the command id."""

    model_config = ConfigDict(extra="forbid")

    result: CallbackResult


def _drop_unknown_callback_kinds(items: object) -> object:
    """Leave out callbacks of a kind newer than this SDK, which no handler here can answer."""

    if not isinstance(items, list):
        return items
    return [
        item
        for item in items
        if not (
            isinstance(item, dict)
            and isinstance(callback := item.get("callback"), dict)
            and isinstance(kind := callback.get("kind"), str)
            and kind not in _KNOWN_CALLBACK_KINDS
        )
    ]


class _SessionCallbacksResponse(CallbacksTreeResponse):
    """Body of ``GET /sessions/{id}/callbacks`` and data of each ``/callbacks/stream`` frame:
    Harness ``CallbacksTreeResponse``, without the callbacks of kinds this SDK does not know."""

    callbacks: Annotated[list[TreeCallback], BeforeValidator(_drop_unknown_callback_kinds)]


__all__ = [
    "CallbackResultRequest",
    "MessageSendRequest",
    "MessageSendResponse",
    "SessionCancelRequest",
    "TurnInterruptRequest",
    "TurnStartRequest",
    "TurnSteerRequest",
]
