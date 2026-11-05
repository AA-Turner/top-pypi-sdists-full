"""Sign-ins: a turn that waits for the user to connect a source, and the answer that says which ones they did.

A host opens a sign-in as a callback of its own kind, ``auth``. The SDK reads it as an
``OpenSignIn`` and sends a ``SignInAnswer`` as its ``AuthResult``; ``on_client_tool`` never gets it.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass

from pydantic import JsonValue

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe_agents.sdk.authoring.errors import SdkError
from mistralai.vibe_agents.sdk.client.records import OpenSignIn, SignInRequest
from mistralai.vibe_agents.sdk.client.unknown_values import read_value

__all__ = [
    "SignInAnswer",
    "SignInHandler",
    "check_sign_in_answer",
    "is_sign_in_tool",
    "open_sign_in",
    "sign_in_output",
    "sign_in_requests",
]


# The client tool names a connector sign-in had before its own kind, ``auth``. A call of one, with no
# connector or from an older host, is neither a sign-in nor the caller's own client tool call.
_SIGN_IN_TOOLS = frozenset({"connectors.ask_enable_connector", "ask_enable_connector"})


def is_sign_in_tool(name: str) -> bool:
    """Whether ``name`` is the client tool name of a connector sign-in, under either host's name."""
    return name in _SIGN_IN_TOOLS


@dataclass(frozen=True, slots=True, init=False)
class SignInAnswer:
    """The answer to an ``OpenSignIn``: the ids of the sources the user connected, and of those they
    refused to connect.

    Name each source the sign-in asks for in one list: an answer that leaves one out raises
    ``SdkError`` and sends nothing, and the sign-in stays open. An SDK agent, run locally or
    deployed, checks each source said to be connected, and tells the agent one that is not is still
    not connected. The Agent Controller's default runtime, which serves Le Chat's
    ``ask_enable_connector``, marks each one connected without a check.
    """

    connected: tuple[str, ...]
    denied: tuple[str, ...]

    def __init__(self, *, connected: Iterable[str] = (), denied: Iterable[str] = ()) -> None:
        connected_ids = _ids(connected, "connected")
        denied_ids = _ids(denied, "denied")
        if both := sorted(set(connected_ids) & set(denied_ids)):
            raise ValueError(f"A sign-in answer has each source in one list at most, not {both} in both")
        object.__setattr__(self, "connected", connected_ids)
        object.__setattr__(self, "denied", denied_ids)


# TODO(sign-in-callback): accept ``agents.KeepCallbackOpen()``, the "keep it open" answer that
# approval and client tool handlers share, once #71815 is on main.
type SignInHandler = Callable[[OpenSignIn], SignInAnswer | Awaitable[SignInAnswer]]
"""A plain or async function that answers a sign-in with a ``SignInAnswer``."""


def _ids(ids: Iterable[str], label: str) -> tuple[str, ...]:
    if isinstance(ids, str):
        raise TypeError(f"SignInAnswer({label}=...) takes a list of source ids, not the string {ids!r}")
    listed = tuple(ids)
    if not all(isinstance(source_id, str) for source_id in listed):
        raise TypeError(f"SignInAnswer({label}=...) takes source ids, which are strings")
    return listed


def sign_in_requests(callback: harness_session.SessionCallback) -> tuple[SignInRequest, ...] | None:
    """The sources a sign-in callback asks for, or ``None`` when ``callback`` is not a sign-in."""
    if not isinstance(callback, harness_session.AuthCallback):
        return None
    return tuple(
        SignInRequest(
            source=read_value(request.source, "SignInRequest.source"),
            id=request.id,
            name=request.name,
            mode=read_value(request.mode, "SignInRequest.mode"),
        )
        for request in callback.requests
    )


def open_sign_in(
    callback: harness_session.SessionCallback, requests: tuple[SignInRequest, ...], session_id: str, turn_id: str
) -> OpenSignIn:
    """The record of a sign-in ``callback`` of ``session_id``, which asks for ``requests``."""
    return OpenSignIn(
        id=callback.id,
        session_id=session_id,
        turn_id=callback.turn_id or turn_id,
        kind="sign_in",
        title=None,
        requests=requests,
    )


def check_sign_in_answer(callback_id: str, requests: Iterable[SignInRequest], answer: SignInAnswer) -> None:
    """Raise ``SdkError`` when ``answer`` names a source that the sign-in did not ask for, or leaves
    out one that it asks for."""
    asked = {request.id for request in requests}
    answered = {*answer.connected, *answer.denied}
    if unknown := sorted(answered - asked):
        raise SdkError(
            f"Sign-in {callback_id} asks for {sorted(asked)}: the answer names {unknown}, which it does not ask for"
        )
    if left_out := sorted(asked - answered):
        raise SdkError(
            f"Sign-in {callback_id} asks for {sorted(asked)}: the answer leaves out {left_out}; "
            "name each source in connected or denied"
        )


def sign_in_output(answer: SignInAnswer) -> dict[str, JsonValue]:
    """The ``AuthResult`` that a host takes for a sign-in."""
    result = harness_session.AuthResult(connected=list(answer.connected), denied=list(answer.denied))
    return result.model_dump(mode="json", by_alias=True)
