"""Client-side reconstruction of a session from its ``/events`` stream.

``/events`` is a JSON-patch stream against a rendered session, not a sequence of
whole entries: each ``history_update`` event carries ``add`` / ``replace`` /
``remove`` / ``append`` patches addressed by JSON pointer. :class:`RenderedSession`
applies them in order to maintain the same ordered entry list a product client
renders, so callers can read the live conversation (messages, tool calls, tool
results) without re-implementing the patch protocol.
"""

import copy
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID

# Callbacks whose unanswered presence means the agent is blocked on the user.
# The between-turn turn boundary is NOT a callback anymore: it is signaled by
# the ``workflow_status = waiting_for_input`` state row instead (see
# ``RenderedSession.waiting_for_input``). Only ``ask_user_question`` remains a
# waiting callback (it does not flip the workflow status; the callback itself is
# the only signal).
#
# This stays legacy-only. Session v1 has its own blocking kinds and reports them
# through ``RenderedSessionV1.blocking_callback``, so widening this set would only
# change how a legacy ``callback_call`` is read. Legacy callback names are
# free-form (a tool name reaches the wire verbatim), so widening it is not safe.
WAITING_CALLBACK_NAMES = frozenset({"ask_user_question"})

_WAITING_FOR_INPUT_STATUS = "waiting_for_input"


@dataclass(slots=True)
class Callback:
    """An actionable callback the agent is blocked on (e.g. ``ask_user_question``)."""

    id: UUID
    name: str
    prompt: str
    input: Any

    @property
    def is_waiting(self) -> bool:
        """Whether this callback represents the agent waiting for user input."""
        return self.name in WAITING_CALLBACK_NAMES


class SessionRenderer(Protocol):
    """What :class:`~mistralai.vibe_agents.sessions_client.client.SessionsClient` needs of a renderer.

    Structural, so :class:`RenderedSession` and ``RenderedSessionV1`` both satisfy
    it without a shared base: the client folds and inspects, and stays ignorant of
    which session event protocol produced the frames.
    """

    def apply_public_session_event(self, event: dict[str, Any]) -> None: ...

    def callback_from_event(self, event: dict[str, Any]) -> Callback | None: ...

    def resolve_callback(self, callback_id: UUID) -> None: ...

    @property
    def waiting_for_input(self) -> bool: ...


def callback_from_event(event: dict[str, Any]) -> Callback | None:
    """Return the actionable callback a ``callback_call`` event carries, if any."""
    if event.get("type") != "callback_call":
        return None
    payload = event.get("payload")
    if not isinstance(payload, dict):
        return None
    raw_id = payload.get("id")
    name = payload.get("name")
    if not isinstance(raw_id, str) or not isinstance(name, str):
        return None
    try:
        callback_id = UUID(raw_id)
    except ValueError:
        return None
    callback_input = payload.get("input")
    prompt = ""
    if isinstance(callback_input, dict):
        raw_prompt = callback_input.get("prompt") or callback_input.get("question")
        if isinstance(raw_prompt, str):
            prompt = raw_prompt
    return Callback(id=callback_id, name=name, prompt=prompt, input=callback_input)


def _workflow_status_from_entry_value(value: Any) -> str | None:
    """Return the ``workflow_status`` of a state-entry patch value, if it is one."""
    if not isinstance(value, dict) or value.get("type") != "state":
        return None
    payload = value.get("payload")
    if not isinstance(payload, dict) or payload.get("type") != "workflow_status":
        return None
    content = payload.get("content")
    if not isinstance(content, dict):
        return None
    status = content.get("status")
    return status if isinstance(status, str) else None


def _waiting_for_input_from_patches(patches: Sequence[Any]) -> bool | None:
    """Whether the most recent ``workflow_status`` patch parks on ``waiting_for_input``.

    The turn boundary is signaled by a ``state`` entry carrying
    ``payload.type == "workflow_status"`` with ``content.status == "waiting_for_input"``
    (from the agent loop's ``EventWorkflowStatusChanged(WAITING_FOR_INPUT)``); a later
    ``workflow_status`` row with a different status (e.g. ``running`` once the next turn
    starts) means no longer waiting. Only the last such patch in the batch matters, so this
    scans from the end and returns on the first one. Returns ``None`` when the batch carries
    no ``workflow_status`` patch, so the caller leaves the flag unchanged.
    """
    for patch in reversed(patches):
        if not isinstance(patch, dict) or patch.get("op") not in ("add", "replace"):
            continue
        status = _workflow_status_from_entry_value(patch.get("value"))
        if status is not None:
            return status == _WAITING_FOR_INPUT_STATUS
    return None


@dataclass(slots=True)
class RenderedSession:
    """Accumulates ``/events`` history patches into an ordered entry list."""

    entries: list[dict[str, Any]] = field(default_factory=list)
    session_result: dict[str, Any] | None = None
    invalid_patch_count: int = 0
    waiting_for_input: bool = False

    def callback_from_event(self, event: dict[str, Any]) -> Callback | None:
        """Return the actionable callback a ``callback_call`` event carries, if any."""
        return callback_from_event(event)

    def resolve_callback(self, callback_id: UUID) -> None:
        """No-op: the legacy renderer holds no open-callback state to clear.

        ``waiting_for_input`` comes from the ``workflow_status`` row, not from the
        callbacks seen so far, so an answered callback cannot keep it true.
        """

    def apply_public_session_event(self, event: dict[str, Any]) -> None:
        """Fold one public session event (the inner ``event`` of an /events frame)."""
        event_type = event.get("type")
        payload = event.get("payload")
        if event_type == "history_update" and isinstance(payload, dict):
            patches = payload.get("patches")
            if isinstance(patches, list):
                self.invalid_patch_count += _apply_history_patches(self.entries, patches)
                waiting = _waiting_for_input_from_patches(patches)
                if waiting is not None:
                    self.waiting_for_input = waiting
            return

        if event_type == "task_result" and isinstance(payload, dict):
            self.session_result = payload


def _apply_history_patches(entries: list[dict[str, Any]], patches: Sequence[Any]) -> int:
    invalid_count = 0
    for patch in patches:
        if not isinstance(patch, dict):
            invalid_count += 1
            continue
        tokens = _json_pointer_tokens(patch.get("path"))
        if tokens is None:
            invalid_count += 1
            continue

        op = patch.get("op")
        if op == "add":
            invalid_count += 0 if _apply_add_patch(entries, tokens, patch.get("value")) else 1
        elif op == "replace":
            invalid_count += 0 if _apply_replace_patch(entries, tokens, patch.get("value")) else 1
        elif op == "remove":
            invalid_count += 0 if _apply_remove_patch(entries, tokens) else 1
        elif op == "append":
            invalid_count += 0 if _apply_string_append_patch(entries, tokens, patch.get("value")) else 1
        else:
            invalid_count += 1
    return invalid_count


def _json_pointer_tokens(path: Any) -> list[str] | None:
    if not isinstance(path, str) or not path.startswith("/"):
        return None
    return [part.replace("~1", "/").replace("~0", "~") for part in path.removeprefix("/").split("/")]


def _list_index(token: str, length: int, *, allow_end: bool) -> int | None:
    if token == "-" and allow_end:  # noqa: S105 — JSON-pointer token, not a secret
        return length
    try:
        index = int(token)
    except ValueError:
        return None
    if index < 0:
        return None
    if index == length and allow_end:
        return index
    if index >= length:
        return None
    return index


def _resolve_patch_parent(root: list[dict[str, Any]], tokens: list[str]) -> tuple[Any, str] | None:
    if not tokens:
        return None
    current: Any = root
    for token in tokens[:-1]:
        if isinstance(current, list):
            index = _list_index(token, len(current), allow_end=False)
            if index is None:
                return None
            current = current[index]
            continue
        if isinstance(current, dict):
            if token not in current:
                return None
            current = current[token]
            continue
        return None
    return current, tokens[-1]


def _apply_add_patch(entries: list[dict[str, Any]], tokens: list[str], value: Any) -> bool:
    resolved = _resolve_patch_parent(entries, tokens)
    if resolved is None:
        return False
    parent, token = resolved
    copied_value = copy.deepcopy(value)
    if isinstance(parent, list):
        index = _list_index(token, len(parent), allow_end=True)
        if index is None:
            return False
        parent.insert(index, copied_value)
        return True
    if isinstance(parent, dict):
        parent[token] = copied_value
        return True
    return False


def _apply_replace_patch(entries: list[dict[str, Any]], tokens: list[str], value: Any) -> bool:
    resolved = _resolve_patch_parent(entries, tokens)
    if resolved is None:
        return False
    parent, token = resolved
    copied_value = copy.deepcopy(value)
    if isinstance(parent, list):
        index = _list_index(token, len(parent), allow_end=False)
        if index is None:
            return False
        parent[index] = copied_value
        return True
    if isinstance(parent, dict):
        if token not in parent:
            return False
        parent[token] = copied_value
        return True
    return False


def _apply_remove_patch(entries: list[dict[str, Any]], tokens: list[str]) -> bool:
    resolved = _resolve_patch_parent(entries, tokens)
    if resolved is None:
        return False
    parent, token = resolved
    if isinstance(parent, list):
        index = _list_index(token, len(parent), allow_end=False)
        if index is None:
            return False
        parent.pop(index)
        return True
    if isinstance(parent, dict):
        if token not in parent:
            return False
        del parent[token]
        return True
    return False


def _apply_string_append_patch(entries: list[dict[str, Any]], tokens: list[str], value: Any) -> bool:
    if not isinstance(value, str):
        return False
    resolved = _resolve_patch_parent(entries, tokens)
    if resolved is None:
        return False
    parent, token = resolved
    if isinstance(parent, list):
        index = _list_index(token, len(parent), allow_end=False)
        if index is None or not isinstance(parent[index], str):
            return False
        parent[index] += value
        return True
    if isinstance(parent, dict):
        if not isinstance(parent.get(token), str):
            return False
        parent[token] += value
        return True
    return False
