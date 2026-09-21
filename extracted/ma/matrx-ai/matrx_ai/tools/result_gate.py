"""Layer 1 of the tool-result size gate — source-aware, graceful, at production.

Applied once to every result that carries real tool output, at the executor's
single convergence point. The model NEVER sees more than the soft cap from a tool
that did not self-manage; the full payload is cached for ``fetch_tool_result`` and
the firing is recorded so the gap becomes visible.

Three outcomes, three alarm tiers (see output_caps.py):
  * CANARY  — result in [CANARY, SOFT): passed, but recorded so we can replay and
              tune the cap empirically. Quiet (no console banner).
  * SOFT    — result ≥ SOFT and the tool did NOT declare ``output_self_capped``:
              truncate-with-notice + stash + alarm. For a tool we OWN this is a
              defect ("teach it to manage itself"); for an external/MCP tool it is
              expected (we cannot teach it) — the severity differs by ``tool_kind``.
  * (self-capped) — the tool managed its own size: trusted, untouched.

The ABSOLUTE ceiling (Layer 2) is enforced separately at the provider boundary
(MessageList.sanitize) so even results that bypass this executor are bounded.

The durable recording is an INJECTED sink (aidream wires an ops-triage writer in
package_integration.py) — matrx-ai must not import a host's DB layer. Absent a
sink, only the console sink runs, so the package stays standalone.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_utils import vcprint
from pydantic import BaseModel

from matrx_ai.tools.output_caps import truncate_with_notice
from matrx_ai.tools.output_overflow import stash_overflow
from matrx_ai.tools.result_gate_limits import ResultGateLimits, load_result_gate_limits
from matrx_ai.tools.sections import ResultSection, section_result

GateTier = Literal["canary", "soft_fired", "ceiling_fired"]
ToolKind = Literal["native", "external", "agent", "unknown"]


class ToolResultGateEvent(BaseModel):
    """A single gate firing — handed to every registered sink, typed end to end."""

    tier: GateTier
    tool_name: str
    tool_kind: ToolKind
    output_chars: int
    limit: int
    conversation_id: str | None = None
    call_id: str | None = None
    user_id: str | None = None


_SINKS: list[Callable[[ToolResultGateEvent], None]] = []


def register_tool_result_gate_sink(sink: Callable[[ToolResultGateEvent], None]) -> None:
    """Register a durable sink for gate firings (e.g. the ops-triage writer).

    Sinks must be best-effort and non-blocking; a sink that raises is isolated
    here so one bad sink never breaks dispatch.
    """
    _SINKS.append(sink)


def _emit(event: ToolResultGateEvent) -> None:
    for sink in _SINKS:
        try:
            sink(event)
        except Exception as exc:  # noqa: BLE001 — a sink must never break dispatch
            vcprint(f"[result_gate] sink raised, ignored: {exc}", color="yellow")


def _console_sink(event: ToolResultGateEvent) -> None:
    # Canary is informational and high-volume-ish — keep it quiet on the console
    # (the durable sink still records it for tuning). Soft/ceiling firings SCREAM.
    if event.tier == "canary":
        return
    owned = event.tool_kind in ("native", "agent")
    headline = (
        "🚨 TOOL-RESULT SIZE GATE FIRED — A TOOL DID NOT MANAGE ITS OWN OUTPUT"
        if owned
        else "⚠️ TOOL-RESULT SIZE GATE FIRED on an EXTERNAL tool (expected — cannot self-manage)"
    )
    fix = (
        "FIX THE TOOL: it must truncate its large fields itself (matrx_ai.tools."
        "output_caps.cap_text), offer the agent a way to fetch more, and set "
        "ToolResult.output_self_capped=True. The generic truncation here is BLUNT "
        "and can destroy a structured result — that is why this is an alarm."
        if owned
        else "No action needed per-firing; the result was truncated and cached for "
        "fetch_tool_result. Recorded for cost visibility."
    )
    vcprint(
        data={
            "tool": event.tool_name,
            "tool_kind": event.tool_kind,
            "output_chars": event.output_chars,
            "soft_cap": event.limit,
            "conversation_id": event.conversation_id,
            "call_id": event.call_id,
        },
        title=f"{headline}\n{fix}",
        color="red" if owned else "yellow",
        verbose=True,
    )


_SINKS.append(_console_sink)


def tool_kind_label(tool_type: Any) -> ToolKind:
    """Map a ToolType (or its string value) to the gate's coarse kind."""
    val = getattr(tool_type, "value", tool_type)
    if val in ("local",):
        return "native"
    if val in ("agent",):
        return "agent"
    if val in ("external", "external_handler"):
        return "external"
    return "unknown"


def apply_size_gate(
    content_dict: dict[str, Any],
    *,
    output_self_capped: bool,
    tool_name: str,
    tool_kind: ToolKind,
    conversation_id: str | None,
    user_id: str | None,
    limits: ResultGateLimits | None = None,
) -> tuple[dict[str, Any], bool]:
    """Gate ONE tool-result content dict (the output of ``to_tool_result_content``).

    ``limits`` are the org's effective caps. Omitted, the package defaults apply —
    which is what every non-production caller (tests, standalone matrx-ai) wants
    and what this function did before the caps became knobs. Production reaches
    this through :func:`apply_size_gate_async`, which resolves the rows first.

    Returns ``(content_dict, truncated)`` where ``truncated`` is True only when the
    soft cap fired (so the caller can inject ``fetch_tool_result`` for the next
    turn). Pure except for the best-effort overflow stash + sink emit. Cheap on the
    hot path: a single ``len`` when nothing's wrong. Never raises — a gate failure
    must not break a tool result.
    """
    caps = limits or ResultGateLimits()
    try:
        content = content_dict.get("content")
        # Media / typed-block results carry references the model needs intact —
        # never touch a non-string content (image/audio/video blocks are a list).
        if not isinstance(content, str):
            return content_dict, False
        chars = len(content)
        call_id = str(content_dict.get("call_id") or "")

        # A self-capped tool owns its size — trusted, no soft cap, no canary noise.
        if output_self_capped:
            return content_dict, False

        if chars < caps.soft_cap_chars:
            # Shadow/canary band — passed, but record for empirical tuning.
            if chars >= caps.canary_chars:
                _emit(
                    ToolResultGateEvent(
                        tier="canary",
                        tool_name=tool_name,
                        tool_kind=tool_kind,
                        output_chars=chars,
                        limit=caps.soft_cap_chars,
                        conversation_id=conversation_id,
                        call_id=call_id or None,
                        user_id=user_id,
                    )
                )
            return content_dict, False

        # Over the soft cap and NOT self-managed → gate it.
        stash_overflow(
            call_id=call_id,
            content=content,
            total_chars=chars,
            user_id=user_id,
            conversation_id=conversation_id,
            tool_name=tool_name,
        )
        new_content = truncate_with_notice(
            content,
            limit=caps.soft_cap_chars,
            total_chars=chars,
            call_id=call_id,
            tool_name=tool_name,
        )
        content_dict["content"] = new_content
        # output_chars on the CONTENT dict is "what the model now sees" (it feeds
        # the FE's total_chars_visible_to_model). Lower it to the truncated size so
        # the indicator is accurate; result.output_chars (the DB/true size) is a
        # separate field and stays untouched for persistence + canary replay.
        content_dict["output_chars"] = len(new_content)
        # Mark the preview so the UI / context-trim can tell this was gated, and
        # carry the true pre-truncation size for display.
        preview = content_dict.get("output_preview")
        if isinstance(preview, dict):
            preview["size_gated"] = True
            preview["true_output_chars"] = chars
        _emit(
            ToolResultGateEvent(
                tier="soft_fired",
                tool_name=tool_name,
                tool_kind=tool_kind,
                output_chars=chars,
                limit=caps.soft_cap_chars,
                conversation_id=conversation_id,
                call_id=call_id or None,
                user_id=user_id,
            )
        )
        return content_dict, True
    except Exception as exc:  # noqa: BLE001 — the gate must never break a result
        vcprint(f"[result_gate] apply_size_gate failed, returning ungated: {exc}", color="yellow")
        return content_dict, False


# ===========================================================================
# THE CONTENT GATE — which PART of an oversized result reaches the agent
# ===========================================================================
#
# Everything above cuts by POSITION: keep the first N characters, stash the rest.
# Position is not relevance — the answer is as likely to be at character 300,000
# as at character 300. The gate below cuts by RELEVANCE instead, and it can only
# do that if it knows what the agent is currently pursuing.
#
# That need is NOT at this seam today. ToolContext carries call_id / tool_name /
# iteration / budget and nothing about the request; AppContext is auth + org +
# routing. The user's question, the last assistant turn and the tool's own
# arguments all exist ONE FRAME UP (orchestrator/executor.py, tools/executor.py)
# and were dropped before the gate. GateContext is that missing frame, passed
# explicitly — so nothing here ever GUESSES the need, and when none of the three
# shapes is present, relevance is unanswerable and the positional cut stays.


@dataclass(frozen=True)
class GateContext:
    """What the agent is currently pursuing, carried down to the size gate.

    Every field is optional and NONE of them is invented here. Measured
    2026-09-20: 872 of the 903 conversations that hit this seam (96.6%) have a
    persisted user message, so ``user_question`` is usually present — but a
    worker or scheduled run has no human turn at all, and the gate must behave
    honestly when it has nothing to judge against.
    """

    user_question: str | None = None
    """The user's current question, verbatim."""

    last_assistant_turn: str | None = None
    """What the agent said it was about to do — often a sharper statement of the
    need than the user's question on iteration 5 of a loop."""

    mandate_goal: str | None = None
    """The declared goal of the mandate this run serves. Present only for a
    mandated run; never inferred for free chat."""

    tool_input: dict[str, Any] = field(default_factory=dict)
    """The arguments the agent called the tool with (url, query, path, sql)."""

    iteration: int = 0
    organization_id: str | None = None

    @property
    def has_need(self) -> bool:
        """True when SOMETHING states what the agent is after.

        With all three empty, a relevance question is unanswerable. Asking it
        anyway would buy a fluent yes/no about nothing and drop whichever half
        the model liked less.
        """
        return bool(
            (self.user_question or "").strip()
            or (self.last_assistant_turn or "").strip()
            or (self.mandate_goal or "").strip()
        )

    @property
    def tool_input_summary(self) -> str:
        """One line naming what was asked for — the cheap shape of tool_input."""
        if not self.tool_input:
            return ""
        parts = []
        for key in ("url", "query", "q", "path", "sql", "question", "search", "name"):
            val = self.tool_input.get(key)
            if isinstance(val, str) and val.strip():
                parts.append(f"{key}={val.strip()[:200]}")
        if not parts:
            parts = [f"{k}={str(v)[:80]}" for k, v in list(self.tool_input.items())[:3]]
        return "; ".join(parts)


#: How much of a section's text the cheap decision shape carries. A ~32k-token
#: judging state holds many sections at this size; the full text is offered too,
#: so a richer Holder can reach for it.
SECTION_EXCERPT_CHARS = 1_200

#: Section headings that are chrome on every page rather than content. Matched
#: case-insensitively as whole headings. Deliberately SHORT: a longer list is a
#: guess, and the boilerplate judgement belongs to the mandate, not to this
#: constant. These are only the ones no judgement is needed for.
_OBVIOUS_BOILERPLATE = frozenset(
    {
        "navigation",
        "nav",
        "footer",
        "header",
        "cookie notice",
        "cookies",
        "privacy policy",
        "terms of service",
        "skip to content",
        "skip to main content",
    }
)


def _section_provision(
    section: ResultSection,
    *,
    sectioned: Any,
    tool_name: str,
    gate_context: GateContext,
    threshold: float,
) -> dict[str, Any]:
    """One section's provision, shaped by ``content_gate.tool_result_section``."""
    return {
        "section_text": section.text,
        "section_excerpt": section.text[:SECTION_EXCERPT_CHARS],
        "section_index": section.index,
        "section_heading": section.heading,
        "section_chars": section.chars,
        "section_source": section.section_source,
        "result_section_count": len(sectioned.sections),
        "result_total_chars": sectioned.total_chars,
        "result_format": sectioned.result_format,
        "sibling_headings": [h for h in sectioned.headings if h],
        "user_question": gate_context.user_question,
        "last_assistant_turn": gate_context.last_assistant_turn,
        "mandate_goal": gate_context.mandate_goal,
        "tool_name": tool_name,
        "tool_input": gate_context.tool_input or None,
        "tool_input_summary": gate_context.tool_input_summary or None,
        "iteration": gate_context.iteration,
        "threshold_hint": threshold,
    }


def _probability(raw: Any) -> float | None:
    """Read a ``relevant`` answer as a probability the gate can threshold.

    Accepts a number in [0, 1] or an explicit boolean. Anything else — a word, a
    1-4 score, None — is UNREADABLE and returns None, which the caller treats as
    "this section was not judged", never as "not relevant". A misread answer
    silently withholding content is the failure this gate exists to prevent.
    """
    if isinstance(raw, bool):
        return 1.0 if raw else 0.0
    if isinstance(raw, (int, float)):
        val = float(raw)
        return val if 0.0 <= val <= 1.0 else None
    return None


def _withheld_note(
    *,
    withheld: list[ResultSection],
    kept_chars: int,
    total_chars: int,
    call_id: str,
    tool_name: str,
) -> str:
    """Name every section that did not reach the agent, and how to get it.

    Counted, grouped by how it was cut, and pointed at ``fetch_tool_result`` —
    because a gate that silently drops the half that mattered is exactly the
    failure mode a positional cut already has.
    """
    by_source: dict[str, int] = {}
    for sec in withheld:
        by_source[sec.section_source] = by_source.get(sec.section_source, 0) + 1
    breakdown = ", ".join(f"{count} by {source}" for source, count in sorted(by_source.items()))
    named = "; ".join(
        f"#{sec.index}"
        + (f" {sec.heading!r}" if sec.heading else "")
        + f" ({sec.chars:,} chars)"
        for sec in withheld[:20]
    )
    more = f" …and {len(withheld) - 20} more" if len(withheld) > 20 else ""
    return (
        f"\n\n[⚠️ TOOL RESULT FILTERED BY THE PLATFORM CONTENT GATE"
        + (f" — tool {tool_name!r}" if tool_name else "")
        + f". {len(withheld):,} of the result's sections were judged not relevant to "
        f"what you are currently doing and were held back ({breakdown}); you are "
        f"seeing {kept_chars:,} of {total_chars:,} characters, in the result's own "
        f"order. NOTHING WAS DELETED — held back: {named}{more}. To read any of it, "
        f'call the `fetch_tool_result` tool with call_id="{call_id}", the offset you '
        f"want, and max_chars=<how many characters you want>.]"
    )


def _unjudged_note(*, mandate_key: str) -> str:
    """Appended to today's positional cut when nothing could judge relevance.

    Nothing fails silently: the agent is told that the cut it is looking at was
    made by POSITION, and which mandate would have made it by relevance.
    """
    return (
        f"\n\n[NOTE: this cut was made by POSITION, not by relevance — the first "
        f"characters were kept and the rest held back, so the part you need may be "
        f"in the part you cannot see. Deciding by relevance is the job of the "
        f"`{mandate_key}` mandate, which has no Holder bound, so nobody could answer "
        f"for this result. Use `fetch_tool_result` to read further.]"
    )


#: The mandate that decides this. Named in the notice when it cannot answer, so
#: "nobody is deciding this" is never silent.
SECTION_RELEVANCE_MANDATE_KEY = "content_gate.section_relevance_decision"


async def apply_size_gate_async(
    content_dict: dict[str, Any],
    *,
    output_self_capped: bool,
    tool_name: str,
    tool_kind: ToolKind,
    conversation_id: str | None,
    user_id: str | None,
    gate_context: GateContext | None = None,
) -> tuple[dict[str, Any], bool]:
    """The production door to the gate: org caps, then relevance, then position.

    Order of decision, and why each step is where it is:

    1. Resolve the org's caps. Everything below thresholds on THEIR numbers, not
       on this file's constants.
    2. Everything the sync gate already handles (non-string content, a tool that
       capped itself, a result under the cap) is handled there, unchanged.
    3. Over the cap: stash the full payload FIRST, so whatever the gate decides,
       ``fetch_tool_result`` can serve the rest.
    4. Ask the mandate which sections the agent needs. Kept sections are returned
       IN THE RESULT'S OWN ORDER with a note naming everything withheld.
    5. Nothing bound, nothing to judge against, or an unreadable answer → today's
       positional cut, with a note naming the mandate that would have decided it.

    Never raises: a gate failure must not cost a tool its result.
    """
    limits = await load_result_gate_limits(
        organization_id=(gate_context.organization_id if gate_context else None),
        user_id=user_id,
    )
    content = content_dict.get("content")
    if (
        not isinstance(content, str)
        or output_self_capped
        or len(content) < limits.soft_cap_chars
    ):
        return apply_size_gate(
            content_dict,
            output_self_capped=output_self_capped,
            tool_name=tool_name,
            tool_kind=tool_kind,
            conversation_id=conversation_id,
            user_id=user_id,
            limits=limits,
        )

    try:
        decided = await _apply_relevance_gate(
            content_dict,
            content=content,
            tool_name=tool_name,
            tool_kind=tool_kind,
            conversation_id=conversation_id,
            user_id=user_id,
            gate_context=gate_context,
            limits=limits,
        )
    except Exception as exc:  # noqa: BLE001 — the gate must never break a result
        vcprint(
            f"[result_gate] relevance gate failed ({type(exc).__name__}: {exc}); "
            f"falling back to the positional cut.",
            color="yellow",
        )
        decided = None
    if decided is not None:
        return decided

    gated, truncated = apply_size_gate(
        content_dict,
        output_self_capped=output_self_capped,
        tool_name=tool_name,
        tool_kind=tool_kind,
        conversation_id=conversation_id,
        user_id=user_id,
        limits=limits,
    )
    if truncated and isinstance(gated.get("content"), str):
        gated["content"] = gated["content"] + _unjudged_note(
            mandate_key=SECTION_RELEVANCE_MANDATE_KEY
        )
        gated["output_chars"] = len(gated["content"])
        _record_verdict(
            call_id=str(content_dict.get("call_id") or ""),
            conversation_id=conversation_id,
            verdict={
                "decided_by": "position",
                "reason": "no_holder_bound",
                "mandate_key": SECTION_RELEVANCE_MANDATE_KEY,
                "soft_cap_chars": limits.soft_cap_chars,
                "limits_source": limits.source,
                "total_chars": len(content),
                "shown_chars": gated["output_chars"],
            },
        )
    return gated, truncated


async def _apply_relevance_gate(
    content_dict: dict[str, Any],
    *,
    content: str,
    tool_name: str,
    tool_kind: ToolKind,
    conversation_id: str | None,
    user_id: str | None,
    gate_context: GateContext | None,
    limits: ResultGateLimits,
) -> tuple[dict[str, Any], bool] | None:
    """Keep the sections the agent needs, or return None to fall back."""
    from matrx_ai._ext import get_section_relevance_decider

    decider = get_section_relevance_decider()
    if decider is None or gate_context is None or not gate_context.has_need:
        return None

    chars = len(content)
    call_id = str(content_dict.get("call_id") or "")
    stash_overflow(
        call_id=call_id,
        content=content,
        total_chars=chars,
        user_id=user_id,
        conversation_id=conversation_id,
        tool_name=tool_name,
        max_chars=limits.overflow_stash_max_chars,
    )

    sectioned = section_result(content, max_sections=limits.max_sections_per_result)
    if len(sectioned.sections) < 2:
        # One section is the whole result — there is nothing to choose between,
        # so relevance has no work to do and the positional cut is the honest
        # answer rather than an all-or-nothing verdict on the entire payload.
        return None

    threshold = limits.section_relevance_threshold
    provisions = [
        _section_provision(
            sec,
            sectioned=sectioned,
            tool_name=tool_name,
            gate_context=gate_context,
            threshold=threshold,
        )
        for sec in sectioned.sections
    ]
    verdicts = await decider(provisions)
    if not verdicts:
        return None

    # Match by section_index, never by list position: a Holder that reorders or
    # invents sections must not be able to silently drop the one that mattered.
    by_index: dict[int, dict[str, Any]] = {}
    for verdict in verdicts:
        idx = verdict.get("section_index")
        if isinstance(idx, int) and 0 <= idx < len(sectioned.sections):
            by_index[idx] = verdict

    kept: list[ResultSection] = []
    withheld: list[ResultSection] = []
    unjudged = 0
    for sec in sectioned.sections:
        verdict = by_index.get(sec.index)
        if verdict is None:
            # Never judged → KEPT. Silence is not a "no": withholding on an
            # answer nobody gave is the exact failure this gate must not add.
            unjudged += 1
            kept.append(sec)
            continue
        probability = _probability(verdict.get("relevant"))
        if probability is None:
            unjudged += 1
            kept.append(sec)
            continue
        boilerplate = verdict.get("is_boilerplate") is True or (
            (sec.heading or "").strip().lower() in _OBVIOUS_BOILERPLATE
        )
        if probability >= threshold and not boilerplate:
            kept.append(sec)
        else:
            withheld.append(sec)

    if not withheld:
        # Every section earned its place; the result is still over the cap, so
        # the positional cut still applies. Claiming a saving we did not make
        # would be a lie in the note.
        return None
    if not kept:
        # Nothing survived. Handing the agent an empty result is worse than
        # handing it the head of the payload, so fall back rather than invent a
        # confidence we do not have.
        vcprint(
            f"[result_gate] relevance gate would have withheld EVERY section of "
            f"{tool_name!r}'s result ({len(withheld)} sections). Falling back to the "
            f"positional cut — an empty tool result is never the right answer.",
            color="yellow",
        )
        return None

    body = "".join(sec.text for sec in kept)
    note = _withheld_note(
        withheld=withheld,
        kept_chars=len(body),
        total_chars=chars,
        call_id=call_id,
        tool_name=tool_name,
    )
    content_dict["content"] = body + note
    content_dict["output_chars"] = len(content_dict["content"])
    preview = content_dict.get("output_preview")
    if isinstance(preview, dict):
        preview["size_gated"] = True
        preview["content_gated"] = True
        preview["true_output_chars"] = chars
    _emit(
        ToolResultGateEvent(
            tier="soft_fired",
            tool_name=tool_name,
            tool_kind=tool_kind,
            output_chars=chars,
            limit=limits.soft_cap_chars,
            conversation_id=conversation_id,
            call_id=call_id or None,
            user_id=user_id,
        )
    )
    _record_verdict(
        call_id=call_id,
        conversation_id=conversation_id,
        verdict={
            "decided_by": "relevance",
            "mandate_key": SECTION_RELEVANCE_MANDATE_KEY,
            "threshold": threshold,
            "limits_source": limits.source,
            "result_format": sectioned.result_format,
            "section_count": len(sectioned.sections),
            "kept": len(kept),
            "withheld": len(withheld),
            "unjudged_kept": unjudged,
            "total_chars": chars,
            "shown_chars": content_dict["output_chars"],
            "withheld_sections": [
                {
                    "index": sec.index,
                    "heading": sec.heading,
                    "section_source": sec.section_source,
                    "chars": sec.chars,
                    "start": sec.start,
                    "end": sec.end,
                }
                for sec in withheld[:200]
            ],
        },
    )
    return content_dict, True


def _record_verdict(
    *, call_id: str, conversation_id: str | None, verdict: dict[str, Any]
) -> None:
    """Stamp the decision on the tool-call row. Best-effort by contract."""
    if not call_id:
        return
    try:
        from matrx_ai._ext import get_gate_verdict_recorder

        recorder = get_gate_verdict_recorder()
        if recorder is None:
            return
        recorder(call_id, conversation_id, verdict)
    except Exception as exc:  # noqa: BLE001 — an audit write never breaks a result
        vcprint(f"[result_gate] gate verdict not recorded: {exc}", color="yellow")
