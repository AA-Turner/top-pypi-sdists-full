"""The held-run seam — a refused run is kept, so a person can watch it run once (Arman, 2026-10-11:
"If we are not saving the exact run so that I can go and watch it run one time and see what
happens, then it's not helping me").

Every gate at ``UnifiedAIClient._dispatch_with_billing_net`` (usage, run approval / protected
account, readiness, top-tier model, automation guardrails) refuses by raising a CALLER refusal
(``is_caller_refusal``). At that moment this seam hands the HOST:

* the refusal itself;
* the ambient ``AppContext`` (actor, organization, request, conversation, agent, metadata);
* the request ``config`` about to be sent (model, messages, tools) and the call ``profile``;
* the agent facts :func:`note_agent_run` recorded in ``Agent.execute`` — agent id, version flag,
  the exact variable values and user input — or None for a run that did not come through it.

The host decides what to keep and where (aidream: ``billing.held_run``). THE ONE RULE: recording
can never change, slow or fail the refusal. The recorder must be synchronous and cheap (it copies
references and schedules its own background write); every exception is logged red and swallowed.
"""

from __future__ import annotations

import contextvars
import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

Recorder = Callable[[BaseException, Any, Any, Any, "dict[str, Any] | None"], None]

_recorder: Recorder | None = None
_AGENT_RUN: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar(
    "matrx_ai_held_run_agent_facts", default=None
)


def set_held_run_recorder(recorder: Recorder | None) -> None:
    """Host wiring: ``(refusal, ctx, config, profile, agent_facts) -> None``, synchronous."""
    global _recorder
    _recorder = recorder


def note_agent_run(
    *,
    agent_id: str | None,
    is_version: bool,
    variables: dict[str, Any] | None,
    user_input: Any,
    name: str | None,
    context: dict[str, Any] | None = None,
) -> contextvars.Token:
    """Called by ``Agent.execute`` right before the request: what this agent run was handed."""
    return _AGENT_RUN.set(
        {
            "agent_id": str(agent_id) if agent_id else None,
            "is_version": bool(is_version),
            "variables": dict(variables or {}),
            "user_input": user_input,
            "name": name,
            "context": dict(context or {}),
        }
    )


def reset_agent_run(token: contextvars.Token) -> None:
    try:
        _AGENT_RUN.reset(token)
    except ValueError:  # reset from another context (a forked task) — fall back to clearing
        _AGENT_RUN.set(None)


def current_agent_run() -> dict[str, Any] | None:
    return _AGENT_RUN.get()


def record_refusal(exc: BaseException, *, config: Any = None, profile: Any = None) -> None:
    """Hand one gate refusal to the host. Never raises; ignores anything that is not a refusal."""
    recorder = _recorder
    if recorder is None or not getattr(exc, "is_caller_refusal", False):
        return
    try:
        from matrx_connect.context.app_context import try_get_app_context

        recorder(exc, try_get_app_context(), config, profile, _AGENT_RUN.get())
    except Exception:  # noqa: BLE001 — a held-run recorder never touches the refusal
        logger.exception(
            "[held run] the host recorder failed; the refusal (%s) stands but the run was NOT kept",
            type(exc).__name__,
        )


__all__ = [
    "current_agent_run",
    "note_agent_run",
    "record_refusal",
    "reset_agent_run",
    "set_held_run_recorder",
]
