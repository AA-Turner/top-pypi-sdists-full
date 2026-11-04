"""The answer that keeps a callback open: a handler returns it to answer later."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KeepCallbackOpen:
    """What a callback handler returns to keep the callback open, for someone to answer later.

    Return ``agents.KeepCallbackOpen()`` from ``on_approval``, ``on_client_tool``, a client tool's
    answer or a raw ``provide_callbacks`` handler: nothing is sent, the callback stays open, and the
    waiting call returns ``Blocked`` on it, unless it was given ``after=`` a ``Blocked`` that already
    lists the callback: that wait returns only on a later change. Answer it later with
    ``turn.answer``, an approval with ``AllowApproval`` or ``DenyApproval`` and a client tool call
    with the tool's result, or answer it from another client.

    It is a handler's return only, never an answer: ``turn.answer`` refuses it. ``None`` is not
    this either: an approval handler that returns ``None`` raises ``agents.SdkError``, and a client
    tool that returns ``None`` sends the ``null`` result.
    """


__all__ = ["KeepCallbackOpen"]
