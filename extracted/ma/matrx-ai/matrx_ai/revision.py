"""``revise_until_passing`` — check an answer, revise it IN THE SAME CONVERSATION.

THE ONE revision function (design: common-docs/systems/workflows/projects/
response-checks-and-revisions/DESIGN.md §5). The workflow step
``ai.conversation.revise`` ("Check and Revise") and the podcast code path call
this; neither keeps its own loop.

The algorithm:

1. Attempt 0 is free — check the answer already paid for. Pass → ``passed``.
2. Only ``revise``-severity misses are revised; ``warn`` misses are recorded.
3. A revision is ONE host-authored turn on the conversation (``host_turn`` on
   the continue contract — never ``user_input``: THE USER-INPUT LAW). Its text
   is the agent's OWN ``revision_request`` variable default; the check report
   rides as a per-turn context entry (``response_check``), facts only.
   An agent that declares no ``revision_request`` is ``not_revisable`` — there
   is no fallback prompt text anywhere (owner ruling 2026-10-07).
4. Re-check; stop at pass or ``max_revisions``. Exhausted → the CLOSEST attempt
   flows on as ``off_target``, unless a failing check is ``on_exhausted: fail``.

Crash safety (no double pay). Every revision turn carries a deterministic
``revision_key`` = uuid5(run, node, dispatch, item, n). Before sending turn n the
conversation's persisted turns are read: a host turn with that key that already
has an answer is REUSED (no new turn, no new spend); a host turn with that key
and no answer (the worker died mid-turn) is finished with ``retry`` — the
persisted state re-runs, no second host turn is appended.

Per-run budget: the caller passes ``turns_already_paid`` read from DURABLE rows
(``workflow.run_log`` via ``matrx_graph.run_log.run_revision_turns``) — never a
process counter.
"""

from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_graph.checks import ResponseCheckResult, ResponseCheckSpec, run_checks
from matrx_utils import vcprint

#: The namespace every revision key is minted under. Changing it orphans the
#: keys of in-flight revisions — never change it.
REVISION_KEY_NAMESPACE = uuid.UUID("6f1d2c9e-4b0a-4d8e-9a57-2f3c8e1b7d40")

#: The agent variable whose DEFAULT is the revision turn's activation line.
REVISION_REQUEST_VARIABLE = "revision_request"

#: The context-entry key the check report rides under.
CHECK_CONTEXT_KEY = "response_check"

HOST_TURN_REASON = "response_check_revision"

#: Inline the report rather than leaving a ``ctx_get`` stub the agent may never fetch.
REPORT_MAX_INLINE_CHARS = 4000

Outcome = Literal["passed", "revised", "off_target", "not_revisable", "failed"]


def revision_key(base: str, n: int) -> str:
    """Deterministic id for revision turn ``n`` of one invocation."""
    return str(uuid.uuid5(REVISION_KEY_NAMESPACE, f"{base}:{n}"))


@dataclass
class RevisionAttempt:
    n: int
    text: str
    check: ResponseCheckResult
    request_id: str | None = None
    revision_key: str | None = None
    cost_usd: float = 0.0
    reused: bool = False

    def summary(self) -> dict[str, Any]:
        return {
            "n": self.n,
            "request_id": self.request_id,
            "revision_key": self.revision_key,
            "verdict": self.check.verdict,
            "measures": [m.model_dump(mode="json") for m in self.check.checks],
            "cost_usd": self.cost_usd,
            "reused": self.reused,
        }


@dataclass
class RevisionOutcome:
    outcome: Outcome
    final: RevisionAttempt
    attempts: list[RevisionAttempt] = field(default_factory=list)
    reason: str = ""
    final_result: Any = None  # the continue turn's normalized result, when revised

    @property
    def revision_turns(self) -> int:
        return sum(1 for a in self.attempts if a.n > 0 and not a.reused)

    @property
    def revision_cost_usd(self) -> float:
        return round(sum(a.cost_usd for a in self.attempts if a.n > 0), 6)

    def warning_label(self) -> str | None:
        if self.outcome == "passed" and not self.final.check.misses():
            return None
        return {
            "revised": "response_check.revised",
            "off_target": "response_check.off_target",
            "not_revisable": "response_check.not_revisable",
            "failed": "response_check.failed",
            "passed": "response_check.missed",  # warn-severity misses only
        }[self.outcome]

    def payload(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome,
            "reason": self.reason,
            "revision_turns": self.revision_turns,
            "revision_cost_usd": self.revision_cost_usd,
            "final": self.final.check.model_dump(mode="json"),
            "attempts": [a.summary() for a in self.attempts],
        }


#: ``(conversation_id, host_turn | None, context, retry) -> (text, request_id, cost_usd, result)``
TurnSender = Callable[
    [str, "dict[str, Any] | None", "dict[str, Any]", bool], Awaitable[tuple[str, str | None, float, Any]]
]
#: ``(conversation_id) -> list of persisted messages`` (UnifiedMessage-like)
TurnReader = Callable[[str], Awaitable[list[Any]]]
#: ``(conversation_id) -> activation text | None``
RequestResolver = Callable[[str], Awaitable["str | None"]]


def _text_of(message: Any) -> str:
    """The reply text of a message: its text blocks only. A ``thinking`` block keeps the model's
    reasoning under ``text``; it is never the answer a revision is judged on or handed back."""
    from matrx_ai.config.message_config import content_text

    return content_text(getattr(message, "content", None), sep="")


def find_revision_turn(messages: list[Any], key: str) -> tuple[bool, str | None]:
    """(host turn with ``key`` exists, the assistant answer after it or None)."""
    for i, msg in enumerate(messages):
        role = getattr(getattr(msg, "role", None), "value", getattr(msg, "role", None))
        meta = getattr(msg, "metadata", None) or {}
        if role == "user" and meta.get("revision_key") == key:
            for later in messages[i + 1 :]:
                lrole = getattr(getattr(later, "role", None), "value", getattr(later, "role", None))
                if lrole == "user":
                    break
                if lrole == "assistant" and getattr(later, "status", "active") != "failed":
                    text = _text_of(later)
                    if text.strip():
                        return True, text
            return True, None
    return False, None


def _closest(attempts: list[RevisionAttempt]) -> RevisionAttempt:
    # Smallest distance wins; a tie goes to the LATER attempt (it saw more feedback).
    return min(reversed(attempts), key=lambda a: a.check.distance())


async def revise_until_passing(
    *,
    conversation_id: str | None,
    answer: str,
    checks: list[ResponseCheckSpec],
    values: Mapping[str, Any] | None,
    max_revisions: int,
    key_base: str,
    send_turn: TurnSender,
    read_turns: TurnReader,
    resolve_request: RequestResolver,
    tolerance_pct: float,
    revisable: bool = True,
    not_revisable_reason: str = "",
    run_budget_left: int | None = None,
    request_id: str | None = None,
    on_attempt: Callable[[int, int], Awaitable[None]] | None = None,
) -> RevisionOutcome:
    """Check ``answer``; revise in the same conversation until it passes or the bound is hit."""
    values = dict(values or {})

    def check(text: str) -> ResponseCheckResult:
        return run_checks(text, checks, values, default_tolerance_pct=tolerance_pct)

    first = RevisionAttempt(n=0, text=answer, check=check(answer), request_id=request_id)
    attempts = [first]
    if not first.check.revise_misses():
        return RevisionOutcome(outcome="passed", final=first, attempts=attempts)
    if max_revisions <= 0:
        return _exhausted(attempts, "check only (max_revisions is 0)")

    def refuse(reason: str) -> RevisionOutcome:
        return _finish(RevisionOutcome(outcome="not_revisable", final=first, attempts=attempts, reason=reason))

    if not revisable or not conversation_id:
        return refuse(not_revisable_reason or "the step that wrote this answer left no conversation to continue")
    activation = await resolve_request(conversation_id)
    if not (activation or "").strip():
        return refuse(
            f"the agent that wrote this answer declares no '{REVISION_REQUEST_VARIABLE}' "
            "variable, so there is no revision request to send"
        )

    budget = max_revisions if run_budget_left is None else min(max_revisions, run_budget_left)
    if budget <= 0:
        return _exhausted(attempts, "this run's revision budget is spent", budget_reached=True)

    last_result: Any = None
    for n in range(1, budget + 1):
        latest = attempts[-1]
        key = revision_key(key_base, n)
        if on_attempt is not None:
            await on_attempt(n, budget)
        report = latest.check
        context = {
            CHECK_CONTEXT_KEY: {
                "content": report.rendered,
                "type": "response_check_result",
                "label": "Response check",
                "max_inline_chars": REPORT_MAX_INLINE_CHARS,
            }
        }
        exists, prior_answer = find_revision_turn(await read_turns(conversation_id), key)
        if exists and prior_answer is not None:
            # Already paid for on an earlier (crashed) attempt — reuse, never re-ask.
            attempts.append(RevisionAttempt(n=n, text=prior_answer, check=check(prior_answer),
                                            revision_key=key, reused=True))
        else:
            host_turn = None if exists else {
                "text": activation,
                "reason": HOST_TURN_REASON,
                "metadata": {"revision_key": key, "revision": n},
            }
            text, req_id, cost, result = await send_turn(conversation_id, host_turn, context, exists)
            last_result = result
            attempts.append(RevisionAttempt(n=n, text=text, check=check(text), request_id=req_id,
                                            revision_key=key, cost_usd=float(cost or 0.0)))
        if not attempts[-1].check.revise_misses():
            out = RevisionOutcome(outcome="revised", final=attempts[-1], attempts=attempts,
                                  final_result=last_result)
            return _finish(out)

    out = _exhausted(attempts, f"still missing after {budget} revision(s)",
                     budget_reached=run_budget_left is not None and budget < max_revisions)
    if out.final is attempts[-1]:
        out.final_result = last_result
    return out


def _exhausted(attempts: list[RevisionAttempt], reason: str, *, budget_reached: bool = False) -> RevisionOutcome:
    best = _closest(attempts)
    strict = [m for m in best.check.misses() if m.on_exhausted == "fail"]
    if budget_reached:
        reason = f"{reason}; the run's revision budget was reached"
    outcome: Outcome = "failed" if strict else "off_target"
    return _finish(RevisionOutcome(outcome=outcome, final=best, attempts=attempts, reason=reason))


def _finish(out: RevisionOutcome) -> RevisionOutcome:
    vcprint(
        f"[revision] outcome={out.outcome} turns={out.revision_turns} "
        f"distance={out.final.check.distance():.3f} {out.reason}",
        color="yellow" if out.outcome != "passed" else "green",
    )
    return out


async def agent_revision_request(conversation_id: str) -> str | None:
    """The activation line: the conversation's agent's ``revision_request`` default.

    Reads the agent that supplies this conversation's structure (the live
    mandate Holder when the conversation follows one, else the agent named on
    the row). ``None`` when that agent declares no such variable — the caller
    reports ``not_revisable``; nothing here ever invents a prompt.
    """
    from matrx_ai.agents.live_structure import read_structure_source, resolve_live_structure_agent
    from matrx_ai.db.agx_manager import agx

    source = await read_structure_source(conversation_id)
    if source is None:
        return None
    agent_id, is_version = source.named_agent_id, source.named_is_version
    if source.is_live:
        live_id, live_is_version = await resolve_live_structure_agent(source)
        if live_id:
            agent_id, is_version = live_id, live_is_version
    if not agent_id:
        return None
    agent = await agx.load_for_execution(agent_id, is_version=is_version)
    variable = (getattr(agent, "variable_defaults", None) or {}).get(REVISION_REQUEST_VARIABLE)
    text = getattr(variable, "default_value", None) if variable is not None else None
    return str(text) if text is not None and str(text).strip() else None


async def persisted_turns(conversation_id: str) -> list[Any]:
    """The conversation's persisted turns (the ONE rebuild funnel)."""
    from matrx_ai.agents.resolver import _load_persisted_messages

    return await _load_persisted_messages(conversation_id)


def host_continue_sender(
    *, build_request: Callable[[dict[str, Any]], Any], run: Callable[[str, Any], Awaitable[Any]]
) -> TurnSender:
    """A ``TurnSender`` over the host ``conversation_continuer`` (the canonical continue path).

    ``build_request`` turns a payload dict into the host ``ConversationContinueRequest``;
    ``run(conversation_id, request)`` runs it and returns a ``CompletedRequest``.
    """

    async def send(conversation_id: str, host_turn: dict[str, Any] | None,
                   context: dict[str, Any], retry: bool) -> tuple[str, str | None, float, Any]:
        import asyncio

        from matrx_ai.graph_nodes.shared import normalize_completed

        payload: dict[str, Any] = {"context": context, "store": True}
        if retry:
            payload["retry"] = True
        else:
            payload["host_turn"] = host_turn
        completed = await run(conversation_id, build_request(payload))
        result = await asyncio.to_thread(normalize_completed, completed)
        return result.final_text, result.request_id, float(result.usage.cost_usd or 0.0), result

    return send


__all__ = [
    "CHECK_CONTEXT_KEY",
    "HOST_TURN_REASON",
    "REVISION_REQUEST_VARIABLE",
    "RevisionAttempt",
    "RevisionOutcome",
    "agent_revision_request",
    "find_revision_turn",
    "host_continue_sender",
    "persisted_turns",
    "revise_until_passing",
    "revision_key",
]
