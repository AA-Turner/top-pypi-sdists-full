"""Trajectory -> span-tree expansion (Phase 2 of the Harbor ownership plan).

Capture (``harbor.capture_trial``) is lossless and format-blind: the raw
``trajectory.json`` bytes are always stored. This module is the pluggable
*interpretation* layer on top — it reads a trajectory document and expands it
into child spans under the trial's rollout span, using a small normalized
vocabulary so trees are comparable across forks:

  rollout (root, created at capture)
    turn        one per trajectory step
      tool_call  one per tool invocation, result joined via source_call_id
    marker      explicit truncation marker when an eager cap was hit

Every turn and tool_call also carries an OPERATIONAL OUTCOME
(``attributes.outcome``: succeeded / failed / unknown) with its provenance.
That is a different axis from ``status``, which stays lifecycle: a span can be
``completed`` and have failed, and most ATIF producers state no outcome at all,
so ``unknown`` is the honest and common answer. Outcomes come only from
structured producer fields whose meaning is proven — never from result prose,
a result's presence, an exit code, or the trial's reward.

Span IDs are deterministic (uuid5 of run/trial/path), so expansion is
idempotent — re-running it upserts the same rows — and *retroactive*: a trial
captured before its format had a parser can be expanded later from the stored
bytes (``probe trial expand``) without re-running anything.

Formats vary per fork, so parsers live in a registry keyed by format prefix.
``ATIF`` (Harbor upstream's Agent Trajectory Interchange Format, the
``schema_version: "ATIF-v1.x"`` documents) ships built in; private forks
register their own with :func:`register_trajectory_parser`. An unknown format
is never an error — expansion just reports ``expanded: false`` and the raw
bytes stay queryable.

Heavy content (full prompts, tool output) is excerpted in span attributes;
the complete text lives in the stored trajectory artifact.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable

from ..models import SpanBatch, SpanCreate
from ..sdk import unit_context

if TYPE_CHECKING:
    from ..sdk.run import Run

#: Eager-expansion window. A cap here is a lazy-loading concern, never a data
#: limit — raw bytes are always stored and ``max_spans=0`` expands everything.
DEFAULT_MAX_SPANS = 500

_EXCERPT_LIMIT = 700
_SPAN_POST_CHUNK = 200

_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "probe.harbor.trajectory")


def detect_trajectory_format(doc: Any) -> str | None:
    """Sniff a trajectory document's format. ATIF declares itself via
    ``schema_version``; other forks use ``schema``/``format``; anything
    else is ``"unknown"`` (still captured, just not expanded)."""
    if not isinstance(doc, dict):
        return "unknown" if doc is not None else None
    fmt = doc.get("schema_version") or doc.get("schema") or doc.get("format")
    return str(fmt) if fmt else "unknown"


@dataclass
class PlannedSpan:
    """One node a parser wants in the tree. ``path`` is the stable identity
    (uuid5 input) and ``parent_path`` links within the plan; ``None`` means
    the trial's rollout span. Parents must precede children in the plan so a
    prefix cut can never orphan a kept child."""

    path: str
    span_type: str
    name: str
    parent_path: str | None = None
    started_at: str | None = None
    ended_at: str | None = None
    status: str = "completed"
    attributes: dict = field(default_factory=dict)


Parser = Callable[[dict], list[PlannedSpan]]

_PARSERS: dict[str, Parser] = {}


def register_trajectory_parser(format_prefix: str, parser: Parser) -> None:
    """Register a parser for trajectory documents whose detected format starts
    with ``format_prefix`` (case-insensitive). Longest prefix wins."""
    _PARSERS[format_prefix.lower()] = parser


def parser_for(fmt: str | None) -> Parser | None:
    if not fmt:
        return None
    low = fmt.lower()
    best = None
    for prefix in _PARSERS:
        if low.startswith(prefix) and (best is None or len(prefix) > len(best)):
            best = prefix
    return _PARSERS[best] if best else None


def _excerpt(value: Any, limit: int = _EXCERPT_LIMIT) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        try:
            value = json.dumps(value, default=str)
        except (TypeError, ValueError):
            value = str(value)
    if len(value) > limit:
        return value[:limit] + f"… [{len(value) - limit} more chars in stored trajectory]"
    return value


def _flatten_message(message: Any) -> tuple[str | None, int]:
    """ATIF messages are a string or a list of content parts; return the
    joined text excerpt and how many image parts were present."""
    if isinstance(message, str):
        return _excerpt(message), 0
    if isinstance(message, list):
        texts, images = [], 0
        for part in message:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "image":
                images += 1
            elif part.get("text"):
                texts.append(str(part["text"]))
        return _excerpt("\n".join(texts)) if texts else None, images
    return None, 0


def _prune(mapping: dict) -> dict:
    return {k: v for k, v in mapping.items() if v is not None}


def _aware(ts: Any) -> str | None:
    """SpanCreate.started_at requires a tz-aware datetime; ATIF timestamps may
    be naive. Pass through only aware ones — naive stays in attributes."""
    if not isinstance(ts, str):
        return None
    try:
        return ts if datetime.fromisoformat(ts.replace("Z", "+00:00")).tzinfo else None
    except ValueError:
        return None


# Timing provenance, surfaced as ``attributes.elapsed_source``.
#
# ATIF carries a per-step START and nothing else — no end time, no duration
# anywhere in the format. A step's extent can therefore only be INFERRED from
# when the next sibling step began, and that number silently includes tool
# execution and any idle gap. It is not a duration, so it never lands in
# ``ended_at``: the run-activity computation reads
# ``GREATEST(created_at, started_at, ended_at)`` over spans, and every future
# consumer will read ``ended_at`` as a measured end. Inferred values stay in
# attributes, tagged with where they came from.
ELAPSED_SOURCE_NEXT_STEP = "inferred_next_step"
ELAPSED_SOURCE_SUBAGENT_SPAN = "inferred_subagent_span"


def _elapsed_ms(start: str | None, end: str | None) -> int | None:
    """Milliseconds between two tz-aware ISO timestamps.

    ``None`` when either side is missing or naive (``_aware`` already refused
    it), and ``None`` when the clock ran backwards — a negative extent is a
    corrupt input, not a short step. Equal stamps give ``0``, which is a real
    sub-millisecond step rather than an absence.
    """
    if start is None or end is None:
        return None
    try:
        began = datetime.fromisoformat(start.replace("Z", "+00:00"))
        ended = datetime.fromisoformat(end.replace("Z", "+00:00"))
    except ValueError:
        return None
    # Integer microseconds, not total_seconds() * 1000: the float round-trip
    # can truncate an exact millisecond interval one low.
    delta = ended - began
    if delta.days < 0:
        return None
    micros = (delta.days * 86_400 + delta.seconds) * 1_000_000 + delta.microseconds
    return micros // 1000


def _roll_up_subagent(
    wrapper: PlannedSpan,
    descendants: list[PlannedSpan],
    *,
    boundary: str | None,
) -> None:
    """Give a synthetic subagent wrapper the extent of the work it contains.

    The START is real — the first descendant's own measured timestamp. The
    EXTENT runs to where the LAST descendant ends, and that terminal step is the
    subtle case: being last, it has no next sibling INSIDE the subagent, so its
    own elapsed is absent. Its bound comes from one level up instead. The
    subagent runs within a tool call under turn N, so it demonstrably finished
    before turn N+1 began — ``boundary`` is that measured start, which makes the
    tail an upper bound of the same provenance class as every other inference
    here rather than a different kind of guess.

    With no boundary either (the parent turn is itself last), the extent is
    genuinely unknown and stays absent. Falling back to the newest extent we
    happen to have would render the wrapper as FINISHED before the work inside
    it ran — a confidently wrong number rather than a missing one.

    Descendants arrive in parser order, so first/last are positional and never
    depend on comparing timestamp strings across differing UTC offsets.
    """
    timed = [plan for plan in descendants if plan.started_at]
    if not timed:
        return
    wrapper.started_at = timed[0].started_at
    tail = timed[-1]
    tail_elapsed = tail.attributes.get("elapsed_ms")
    if not isinstance(tail_elapsed, int):
        tail_elapsed = _elapsed_ms(tail.started_at, boundary)
    if tail_elapsed is None:
        return
    to_tail = _elapsed_ms(wrapper.started_at, tail.started_at)
    if to_tail is None:
        return
    wrapper.attributes["elapsed_ms"] = to_tail + tail_elapsed
    wrapper.attributes["elapsed_source"] = ELAPSED_SOURCE_SUBAGENT_SPAN


# Operational outcome, surfaced as ``attributes.outcome`` with its provenance.
#
# ``status`` answers "is this over?"; this answers "did it work?", and the two
# are not the same question. ATIF has no outcome field in ANY version Harbor
# 0.21 accepts (v1.0..v1.7) — every model is ``extra: "forbid"``, so the only
# place a producer can state one is an open ``extra`` dict. An outcome is
# therefore producer-specific by construction: there is nothing universal to
# normalize against, only a few fields whose meaning can be PROVEN and an open
# set that cannot. Anything unproven stays ``unknown``, which renders neutral.
#
# Never derived from: result prose, the presence or absence of a result, an
# exit code, a lifecycle ``status`` value, whether the trajectory continued, or
# the trial's reward. See docs/2026-08-24-atif-operational-outcomes.md for the
# evidence behind each exclusion.
OUTCOME_SUCCEEDED = "succeeded"
OUTCOME_FAILED = "failed"
OUTCOME_UNKNOWN = "unknown"

# Derivation rules, recorded as ``attributes.outcome_rule`` so a reader can
# tell an observed outcome from an aggregated one without guessing.
RULE_EXPLICIT_RESULT = "explicit_result_flag"
RULE_EXPLICIT_CALL = "explicit_call_flag"
RULE_EXPLICIT_TURN = "explicit_turn_flag"
RULE_CHILD_FAILED = "child_failed"
RULE_CHILDREN_ALL_SUCCEEDED = "children_all_succeeded"
RULE_MIXED_CHILDREN = "mixed_child_outcomes"
RULE_CONFLICT = "conflicting_signals"
RULE_NO_SIGNAL = "no_authoritative_signal"
# Trial scope only (harbor.capture_trial) — never spread onto a child span.
RULE_TRIAL_EXCEPTION = "trial_exception"

#: The ONLY keys read as an outcome, in the ATIF/Anthropic sense of
#: ``is_error``: True means the invocation FAILED, False means it SUCCEEDED.
#:
#: Keyed BY CONTAINER, not one flat set, because a name carries its own scope.
#: Harbor's ``claude_code`` converter writes ``tool_result_is_error`` onto an
#: observation result and ``tool_use_is_error`` onto the call (its own names
#: for Anthropic's ``is_error`` on a ``tool_result`` and a ``tool_use`` block);
#: plain ``is_error`` is the raw name that reaches ``extra`` when a converter
#: passes a producer event through unmapped, which Copilot CLI's flat schema
#: does. Reading ``tool_result_is_error`` off a STEP would be reading a
#: result-scoped name at turn scope and calling the meaning proven when it is
#: not, so each container reads only the names that belong to it.
#:
#: Notably absent everywhere: ``status``. Codex writes the Responses API item
#: status, and ``"completed"`` there means ARGUMENT GENERATION finished — the
#: tool may not have run at all.
_SOURCE_RESULT_EXTRA = "observation.results[].extra"
_SOURCE_CALL_EXTRA = "tool_calls[].extra"
_SOURCE_STEP_EXTRA = "steps[].extra"

_ERROR_FLAG_KEYS: dict[str, tuple[str, ...]] = {
    _SOURCE_RESULT_EXTRA: ("tool_result_is_error", "is_error"),
    _SOURCE_CALL_EXTRA: ("tool_use_is_error", "is_error"),
    _SOURCE_STEP_EXTRA: ("is_error",),
}

#: Producer identity is untrusted open text copied onto EVERY span in the
#: trajectory, so it is clipped. Long enough for a real agent name and semver,
#: short enough that a hostile or broken producer cannot multiply one document
#: into a far larger set of jsonb writes.
_PRODUCER_LIMIT = 120
#: Aggregated, not read: the turn itself stated nothing and its outcome came
#: from the calls it issued. Saying "observation.results[].extra" here would
#: claim the turn read a field it never looked at.
_SOURCE_CHILD_CALLS = "tool_call children"


def _error_flags(extra: Any, where: str) -> list[tuple[str, str]]:
    """Every outcome a producer explicitly STATED in one ``extra`` dict.

    A flag counts only when it is a real ``bool``. ``isinstance(v, bool)``
    rejects ``1``/``0`` on purpose: a producer writing an int, a string, or
    ``None`` has not stated an outcome in a vocabulary we can prove, and
    coercing it would invent one. Explicit ``False`` is a POSITIVE success
    signal and must survive — hence membership and identity tests throughout,
    never truthiness.

    Returns one ``(outcome, source)`` pair per key found, so the caller can see
    a disagreement instead of silently taking whichever it looked at first.
    """
    if not isinstance(extra, dict):
        return []
    found = []
    for key in _ERROR_FLAG_KEYS[where]:
        value = extra.get(key)
        if isinstance(value, bool):
            found.append(
                (OUTCOME_FAILED if value else OUTCOME_SUCCEEDED, f"{where}.{key}")
            )
    return found


def _reduce_flags(
    flags: list[tuple[str, str]], rule: str
) -> tuple[str, str | None, str]:
    """Collapse stated flags into ``(outcome, source, rule)``.

    Disagreement is refused rather than resolved: two producer fields claiming
    opposite things is exactly the case where picking a winner would be a
    guess. The disagreeing sources are still named, so the refusal is auditable.
    """
    if not flags:
        return OUTCOME_UNKNOWN, None, RULE_NO_SIGNAL
    outcomes = {outcome for outcome, _ in flags}
    if len(outcomes) > 1:
        detail = ", ".join(f"{source}={outcome}" for outcome, source in flags)
        return OUTCOME_UNKNOWN, detail, RULE_CONFLICT
    return flags[0][0], flags[0][1], rule


def _tool_call_outcome(
    call: dict, results: list[dict]
) -> tuple[str, str | None, str]:
    """One invocation's outcome.

    The RESULT's flag outranks the CALL's: the result is what observed the
    execution, while the call is only the request. They are reduced together
    when both exist so a genuine disagreement still surfaces as a conflict
    rather than being hidden by precedence.

    ``results`` is every result that named this call, because a call may have
    more than one. Collapsing them to one before the reduce would resolve a
    disagreement by arrival order instead of reporting it.
    """
    result_flags = [
        flag
        for result in results
        for flag in _error_flags(result.get("extra"), _SOURCE_RESULT_EXTRA)
    ]
    call_flags = _error_flags(call.get("extra"), _SOURCE_CALL_EXTRA)
    if result_flags and call_flags:
        return _reduce_flags(result_flags + call_flags, RULE_EXPLICIT_RESULT)
    if result_flags:
        return _reduce_flags(result_flags, RULE_EXPLICIT_RESULT)
    return _reduce_flags(call_flags, RULE_EXPLICIT_CALL)


def _turn_outcome(
    step: dict, child_outcomes: list[str]
) -> tuple[str, str | None, str]:
    """A turn's outcome: an explicit statement, else its tool calls.

    ``child_outcomes`` is this step's OWN tool calls, correlated by
    ``source_call_id`` upstream — never a positional zip, and never anything
    from a nested subagent, whose spans keep their own outcomes.

    Success demands unanimity and failure does not, and the asymmetry is the
    point. One proven failure is positive evidence that something in this turn
    failed, whatever its unknown siblings did. One unknown sibling, by
    contrast, means we cannot say the turn succeeded — so it does not.

    A turn with no tool calls stays unknown however cleanly it generated:
    "the model finished talking" is not an operational outcome.
    """
    stated = _error_flags(step.get("extra"), _SOURCE_STEP_EXTRA)
    if stated:
        outcome, source, rule = _reduce_flags(stated, RULE_EXPLICIT_TURN)
        # An explicit turn FAILURE outranks the children: a turn can fail for a
        # reason that is not one of its tools, and that is the producer's call
        # to make. An explicit turn SUCCESS does NOT get to overrule a child
        # that explicitly failed — that is precisely the false-green this whole
        # attribute exists to prevent, so the disagreement is reported instead.
        if outcome == OUTCOME_SUCCEEDED and OUTCOME_FAILED in child_outcomes:
            return (
                OUTCOME_UNKNOWN,
                f"{source}=succeeded, {_SOURCE_CHILD_CALLS}=failed",
                RULE_CONFLICT,
            )
        return outcome, source, rule
    if not child_outcomes:
        return OUTCOME_UNKNOWN, None, RULE_NO_SIGNAL
    if OUTCOME_FAILED in child_outcomes:
        return OUTCOME_FAILED, _SOURCE_CHILD_CALLS, RULE_CHILD_FAILED
    if all(outcome == OUTCOME_SUCCEEDED for outcome in child_outcomes):
        return OUTCOME_SUCCEEDED, _SOURCE_CHILD_CALLS, RULE_CHILDREN_ALL_SUCCEEDED
    if all(outcome == OUTCOME_UNKNOWN for outcome in child_outcomes):
        # Nothing was stated anywhere under this turn. Reported as absence
        # rather than as a mixture so a fleet report can tell "this producer
        # says nothing" apart from "this producer says something, sometimes".
        return OUTCOME_UNKNOWN, None, RULE_NO_SIGNAL
    return OUTCOME_UNKNOWN, None, RULE_MIXED_CHILDREN


def _clip(value: Any) -> str | None:
    """Producer identity as a bounded string, or None. Not ``_excerpt``: this
    rides on every span and wants a hard cap, not a "N more chars" suffix."""
    if not isinstance(value, str) or not value:
        return None
    return value[:_PRODUCER_LIMIT]


def outcome_attributes(
    outcome: str, source: str | None, rule: str, agent: dict
) -> dict:
    """The outcome plus enough provenance to audit or re-derive it: which rule
    fired, which producer field it read, and which producer/version wrote the
    document. The producer rides on every span so a fleet report groups by it
    in SQL instead of re-reading blobs from storage.

    Pruned here rather than by the caller so no span ever carries an explicit
    ``outcome_source: null`` — ``attributes ? 'outcome_source'`` would then be
    true for a span that read nothing, which is exactly the confusion these
    keys exist to remove."""
    return _prune(
        {
            "outcome": outcome,
            "outcome_rule": rule,
            "outcome_source": source,
            "outcome_producer": _clip(agent.get("name")),
            "outcome_producer_version": _clip(agent.get("version")),
        }
    )


def parse_atif(doc: dict, *, boundary: str | None = None) -> list[PlannedSpan]:
    """Map an ATIF trajectory (any v1.x) into the normalized vocabulary.

    ``boundary`` is the measured instant the whole trajectory demonstrably
    finished before — Harbor's ``agent_execution.finished_at``. It bounds the
    terminal step, which has no next sibling of its own. Optional and keyword
    only, so the registry's plain ``Callable[[dict], list[PlannedSpan]]``
    contract still holds for fork parsers that do not want it.

    Structural mapping only — every step becomes a ``turn``, every tool call a
    ``tool_call`` child with its observation result joined via
    ``source_call_id``; unmatched observation results attach to the turn.
    Embedded subagent trajectories (v1.7) recurse under the tool_call/turn
    whose observation referenced them. Fork-specific ``extra`` fields pass
    through untouched in attributes.
    """
    return _parse_atif_inner(doc, prefix="", parent_path=None, boundary=boundary)


def _parse_atif_inner(
    doc: dict, *, prefix: str, parent_path: str | None, boundary: str | None = None
) -> list[PlannedSpan]:
    plans: list[PlannedSpan] = []
    subagents = {
        sub.get("trajectory_id"): sub
        for sub in doc.get("subagent_trajectories") or []
        if isinstance(sub, dict)
    }
    agent = doc.get("agent") if isinstance(doc.get("agent"), dict) else {}

    # Materialized because a step's extent is inferred from the NEXT sibling's
    # start. One doc's steps ARE the sibling set — a subagent trajectory recurses
    # through its own _parse_atif_inner call with its own steps — so sibling
    # scoping falls out of the loop and never needs parent_path grouping.
    steps = [step for step in doc.get("steps") or [] if isinstance(step, dict)]

    for index, step in enumerate(steps):
        step_id = step.get("step_id")
        source = step.get("source") or "agent"
        turn_path = f"{prefix}turn/{step_id}"
        message, image_parts = _flatten_message(step.get("message"))

        calls = [c for c in step.get("tool_calls") or [] if isinstance(c, dict)]
        results = []
        if isinstance(step.get("observation"), dict):
            results = [r for r in step["observation"].get("results") or [] if isinstance(r, dict)]
        # A LIST per call, not one result. ATIF places no uniqueness constraint
        # on `source_call_id` (its validator only checks the id EXISTS in
        # tool_calls), and Harbor's copilot_cli converter APPENDS each arriving
        # result onto the issuing step, so one call can accumulate several. A
        # dict comprehension silently kept the last, which for an OUTCOME means
        # two results disagreeing would resolve to whichever arrived last
        # instead of being reported as the conflict it is.
        by_call: dict[str, list[dict]] = {}
        for result in results:
            result_call_id = result.get("source_call_id")
            if result_call_id:
                by_call.setdefault(result_call_id, []).append(result)
        seen_call_ids: set[str] = set()
        ambiguous_call_ids: set[str] = set()
        for candidate in calls:
            candidate_id = candidate.get("tool_call_id")
            if candidate_id in seen_call_ids:
                ambiguous_call_ids.add(candidate_id)
            elif candidate_id is not None:
                seen_call_ids.add(candidate_id)
        unmatched = [r for r in results if not r.get("source_call_id")]

        metrics = step.get("metrics") if isinstance(step.get("metrics"), dict) else None
        started_at = _aware(step.get("timestamp"))
        # The immediate next sibling is the boundary. If ITS timestamp is absent
        # or naive we stop rather than scanning further — skipping ahead would
        # silently fold an untimed step's work into this one's extent. The LAST
        # step has no successor, so it falls back to ``boundary`` — one level up.
        # At the top level that is the agent_execution phase's measured end; in
        # a subagent it is the parent turn's next sibling. Same provenance class
        # as every other inference here (an upper bound the work fits inside),
        # which is why the terminal step no longer renders as a point forever.
        next_started_at = (
            _aware(steps[index + 1].get("timestamp"))
            if index + 1 < len(steps)
            else boundary
        )
        elapsed_ms = _elapsed_ms(started_at, next_started_at)
        # Built now, appended before its children (PlannedSpan requires parents
        # to precede children), but its outcome is filled in AFTER the tool
        # calls below: a turn's outcome aggregates the calls it issued.
        turn_plan = PlannedSpan(
            path=turn_path,
            span_type="turn",
            name=f"{source} turn {step_id}",
            parent_path=parent_path,
            started_at=started_at,
            attributes=_prune(
                {
                    "source": source,
                    "timestamp": step.get("timestamp"),
                    # System/user setup turns are not model generations.
                    # Only inherit the trajectory-level model for agent
                    # turns; otherwise preserve absence honestly.
                    "model_name": step.get("model_name")
                    or (agent.get("model_name") if source == "agent" else None),
                    "message": message,
                    "image_parts": image_parts or None,
                    "reasoning": _excerpt(step.get("reasoning_content")),
                    "observation": _excerpt(
                        "\n".join(str(r.get("content") or "") for r in unmatched)
                    )
                    if unmatched
                    else None,
                    "prompt_tokens": (metrics or {}).get("prompt_tokens"),
                    "completion_tokens": (metrics or {}).get("completion_tokens"),
                    "cached_tokens": (metrics or {}).get("cached_tokens"),
                    "cost_usd": (metrics or {}).get("cost_usd"),
                    "llm_call_count": step.get("llm_call_count"),
                    "is_copied_context": step.get("is_copied_context"),
                    "elapsed_ms": elapsed_ms,
                    "elapsed_source": (
                        ELAPSED_SOURCE_NEXT_STEP if elapsed_ms is not None else None
                    ),
                    "extra": step.get("extra"),
                    # Results with no ``source_call_id`` come from actions
                    # outside the tool-calling format. Their content already
                    # lands in ``observation``; their metadata was being
                    # dropped entirely. Preserved here, never derived from —
                    # an unmatched result must not be able to speak for a
                    # sibling call.
                    "observation_extra": _excerpt(
                        [r.get("extra") for r in unmatched]
                    )
                    if any(r.get("extra") is not None for r in unmatched)
                    else None,
                }
            ),
        )
        plans.append(turn_plan)

        child_outcomes: list[str] = []
        for i, call in enumerate(calls):
            call_path = f"{turn_path}/call/{i}"
            # Correlated by id, never by position: a turn may issue several
            # calls in parallel and ATIF makes no promise that its results come
            # back in the order they were requested. An unmatched call gets no
            # result and therefore no outcome.
            call_id = call.get("tool_call_id")
            # A tool_call_id repeated inside one step makes correlation
            # ambiguous: ATIF does not require call ids to be unique within a
            # step, and handing both calls the same result would let one
            # success mark two invocations — and then their turn — successful.
            # Ambiguous correlation is not evidence, so neither call gets any.
            matched = [] if call_id in ambiguous_call_ids else by_call.get(call_id) or []
            # Content keeps the LAST result, which is what the dict
            # comprehension did before and what a streamed tool's final chunk
            # should be. The OUTCOME reads every one of them.
            result = matched[-1] if matched else None
            call_outcome = outcome_attributes(
                *_tool_call_outcome(call, matched), agent
            )
            plans.append(
                PlannedSpan(
                    path=call_path,
                    span_type="tool_call",
                    name=str(call.get("function_name") or "tool"),
                    parent_path=turn_path,
                    # ATIF gives a call no timestamp of its own. Sending none let
                    # the server stamp INGEST time, which put every tool call
                    # after the rollout that contained it had already ended. Its
                    # turn's start is the honest lower bound: the call cannot
                    # have run before the turn it belongs to began.
                    started_at=started_at,
                    attributes=_prune(
                        {
                            "tool_call_id": call.get("tool_call_id"),
                            "function_name": call.get("function_name"),
                            "arguments": _excerpt(call.get("arguments")),
                            "result": _excerpt(result.get("content")) if result else None,
                            "extra": call.get("extra"),
                            # The matched result's own metadata — the ONLY place
                            # any pinned producer states a tool outcome, and
                            # previously discarded wholesale. Excerpted like
                            # every other heavy field: Claude Code's
                            # ``tool_result_metadata`` echoes the full tool
                            # output, and SQL is not where that belongs.
                            "result_extra": _excerpt((result or {}).get("extra")),
                            **call_outcome,
                        }
                    ),
                )
            )
            child_outcomes.append(call_outcome["outcome"])
            plans.extend(
                _expand_subagent_refs(
                    result, subagents, parent_path=call_path, boundary=next_started_at
                )
            )
        turn_plan.attributes.update(
            outcome_attributes(*_turn_outcome(step, child_outcomes), agent)
        )
        for result in unmatched:
            plans.extend(
                _expand_subagent_refs(
                    result, subagents, parent_path=turn_path, boundary=next_started_at
                )
            )
    return plans


def _expand_subagent_refs(
    result: dict | None,
    subagents: dict[str | None, dict],
    *,
    parent_path: str,
    boundary: str | None = None,
) -> list[PlannedSpan]:
    plans: list[PlannedSpan] = []
    if not isinstance(result, dict):
        return plans
    for ref in result.get("subagent_trajectory_ref") or []:
        if not isinstance(ref, dict):
            continue
        traj_id = ref.get("trajectory_id")
        sub = subagents.get(traj_id)
        if not isinstance(sub, dict):
            continue  # external trajectory_path file — bytes captured, not expanded here
        sub_agent = sub.get("agent") if isinstance(sub.get("agent"), dict) else {}
        sub_path = f"{parent_path}/sub/{traj_id}"
        wrapper = PlannedSpan(
            path=sub_path,
            span_type="turn",
            name=f"subagent {sub_agent.get('name') or traj_id}",
            parent_path=parent_path,
            attributes=_prune(
                {
                    "subagent": True,
                    "trajectory_id": traj_id,
                    "agent": sub_agent or None,
                    # The wrapper is a container, not work: it issues no tool
                    # calls of its own, and the nested trajectory's outcomes
                    # belong to the nested spans. Rolling them up here would
                    # let a subagent's failure recolor the delegating turn.
                    **outcome_attributes(
                        OUTCOME_UNKNOWN, None, RULE_NO_SIGNAL, sub_agent
                    ),
                }
            ),
        )
        # Children first so the wrapper can take its extent from them, but
        # APPENDED parent-first: PlannedSpan requires parents to precede
        # children so a prefix cut cannot orphan a kept child.
        # The boundary rides INTO the recursion, not just into the roll-up:
        # a subagent nested under another subagent's terminal step was
        # previously untimed purely because of nesting depth (TODOS.md
        # "Inferred span timing: provenance gaps", case 3).
        sub_plans = _parse_atif_inner(
            sub, prefix=f"{sub_path}/", parent_path=sub_path, boundary=boundary
        )
        _roll_up_subagent(wrapper, sub_plans, boundary=boundary)
        plans.append(wrapper)
        plans.extend(sub_plans)
    return plans


register_trajectory_parser("atif", parse_atif)


def tool_call_ids(doc: Any) -> list[str]:
    """Every ``tool_call_id`` a trajectory document declares.

    Used to score how much of a trial's tool timing a recovery actually
    reached. Deliberately reads the DOCUMENT rather than the recovered mapping:
    coverage is a fraction of what the trajectory has, and a transcript from a
    resumed session can mention calls this document never contained.
    """
    if not isinstance(doc, dict):
        return []
    out: list[str] = []
    stack = [doc]
    seen = 0
    while stack and seen < 100_000:
        node = stack.pop()
        if not isinstance(node, dict):
            continue
        for step in node.get("steps") or []:
            if not isinstance(step, dict):
                continue
            for call in step.get("tool_calls") or []:
                if isinstance(call, dict) and isinstance(call.get("tool_call_id"), str):
                    out.append(call["tool_call_id"])
                    seen += 1
        for sub in node.get("subagent_trajectories") or []:
            stack.append(sub)
    return out


def span_id_for(run_id: str, trial: str, path: str) -> str:
    """Deterministic span id — same run/trial/path always maps to the same
    UUID, which is what makes expansion idempotent and re-runnable."""
    return str(uuid.uuid5(_NAMESPACE, f"{run_id}:{trial}:{path}"))


#: Stamped on a turn whose recorded start fell outside the phase it belongs to.
CONTAINMENT_CLAMPED = "clamped_to_phase"


def _apply_tool_call_timing(
    plans: list[PlannedSpan],
    timing: dict[str, tuple[str, str, dict[str, Any]]],
) -> None:
    """Close tool-call spans that a caller measured elsewhere, in place.

    Joined on ``tool_call_id``, which is the producer's own opaque id -- never
    on name, index or position. A call the mapping does not cover keeps the
    inherited start and no end, exactly as before: partial recovery leaves a
    trial with a mix of measured and inferred calls, and each says which it is.
    """
    for plan in plans:
        if plan.span_type != "tool_call":
            continue
        call_id = plan.attributes.get("tool_call_id")
        found = timing.get(call_id) if isinstance(call_id, str) else None
        if found is None:
            continue
        started_at, ended_at, attributes = found
        plan.started_at = started_at
        plan.ended_at = ended_at
        # A measured window replaces an inferred one outright. Leaving both
        # would hand a consumer two durations and two provenance claims for the
        # same span and no rule for which wins.
        plan.attributes.pop("elapsed_ms", None)
        plan.attributes.pop("elapsed_source", None)
        plan.attributes.update(attributes)


def _reparent_root_turns(
    plans: list[PlannedSpan],
    target_path: str,
    *,
    phase_start: str | None,
    phase_end: str | None,
) -> None:
    """Hang root-level turns off the agent_execution phase, in place.

    Depth-first rendering equals chronological order only when a child really
    does sit inside its parent, so a turn that starts outside the phase is
    clamped to the nearer boundary. The recorded stamp is kept verbatim in
    ``raw_started_at``: the clamp exists to keep the TREE coherent, and throwing
    away the number that proved the incoherence would hide the only evidence
    that a producer's clocks disagreed.

    Ordering uses ``_elapsed_ms``, which already refuses a negative delta, so
    "before" and "after" are decided by parsed instants rather than by comparing
    ISO strings that may carry different UTC offsets.
    """
    for plan in plans:
        if plan.parent_path is not None or plan.span_type != "turn":
            continue
        plan.parent_path = target_path
        started = plan.started_at
        if started is None or phase_start is None or phase_end is None:
            continue
        if _elapsed_ms(phase_start, started) is None:
            clamped = phase_start
        elif _elapsed_ms(started, phase_end) is None:
            clamped = phase_end
        else:
            continue
        plan.attributes["raw_started_at"] = started
        plan.attributes["containment"] = CONTAINMENT_CLAMPED
        plan.started_at = clamped
        # `elapsed_ms` was measured from the stamp we just replaced, so it no
        # longer describes an interval starting where this span now starts.
        # Dropping it leaves a bounded span with no duration claim, which is
        # honest; keeping it would let a clamped turn render as running past
        # the phase that supposedly contains it.
        plan.attributes.pop("elapsed_ms", None)
        plan.attributes.pop("elapsed_source", None)


def expand_trajectory(
    run: "Run",
    doc: Any,
    *,
    root_span_id: str,
    trial: str,
    step_index: int | None = None,
    fmt: str | None = None,
    max_spans: int | None = None,
    coords: dict[str, Any] | None = None,
    strict: bool | None = None,
    extra_plans: list[PlannedSpan] | None = None,
    reparent_root_turns_to: str | None = None,
    containment: tuple[str | None, str | None] = (None, None),
    tool_call_timing: dict[str, tuple[str, str, dict[str, Any]]] | None = None,
) -> dict:
    """Expand one trajectory document into spans under ``root_span_id``.

    ``max_spans`` is the eager window (``None`` -> :data:`DEFAULT_MAX_SPANS`,
    ``0`` -> unlimited). When the cap cuts the plan, an explicit ``marker``
    span records how many spans remain so truncation is visible, and a full
    re-expand later (idempotent ids) fills in the rest.

    ``extra_plans`` are spans some OTHER artifact produced — today, the phase
    and gap spans ``harbor_phases`` derives from ``result.json``. They ride
    through this one writer so they get the same deterministic ids, the same
    ``step_index`` and the same resolved coordinate as everything else. Getting
    ``step_index`` for free is not cosmetic: the spans API orders
    ``step_index NULLS LAST, started_at``, so a phase span created without one
    sorts after every trial in the run.

    ``reparent_root_turns_to`` is a plan path (the ``agent_execution`` phase)
    that root-level turns become children of, which is what makes the timeline's
    depth-first walk read chronologically. ``containment`` is that phase's
    measured ``(start, end)``; a turn falling outside it is clamped to the
    boundary and stamped, with its recorded stamp preserved verbatim in
    ``raw_started_at`` so the clamp adds a rendering hint without destroying
    the evidence that it was needed.

    ``tool_call_timing`` maps a ``tool_call_id`` to a measured
    ``(started_at, ended_at, attributes)`` recovered from somewhere other than
    the trajectory -- today the agent's own transcript. Deliberately a plain
    mapping rather than a typed import: this module stays format-neutral, and
    where a caller found real timing is the caller's business. Measured values
    are the one thing allowed to reach ``ended_at``.

    ``coords`` is the below-run coordinate stamped on every expanded span,
    merged over the ambient :meth:`Run.unit` context (call site wins per key)
    and resolved ONCE — the whole batch, truncation marker included, lands at
    the coordinate that was ambient when expansion was requested.

    Returns ``{format, expanded, spans, truncated, remaining, final_metrics}``.
    """
    fmt = fmt or detect_trajectory_format(doc)
    parser = parser_for(fmt)
    if parser is None or not isinstance(doc, dict):
        return {"format": fmt, "expanded": False, "spans": 0, "truncated": False}

    # A trajectory parser's plan order is the producer's authoritative
    # execution order. Persist it explicitly because timestamps are optional
    # (ATIF system/user setup turns commonly omit them) and the spans API is
    # otherwise free to return equal/missing-timestamp siblings in a different
    # order. Use one global, zero-based index across the flattened plan: sorting
    # siblings by it restores parser order at every level of the tree.
    phase_start, phase_end = containment
    # Only the built-in parser is offered the boundary; the registry contract
    # for fork parsers stays the plain one-argument callable.
    all_plans = (
        parse_atif(doc, boundary=phase_end) if parser is parse_atif else parser(doc)
    )
    if tool_call_timing:
        _apply_tool_call_timing(all_plans, tool_call_timing)
    if reparent_root_turns_to is not None:
        _reparent_root_turns(
            all_plans, reparent_root_turns_to, phase_start=phase_start, phase_end=phase_end
        )
    # Phase spans lead: PlannedSpan requires a parent to precede its children,
    # and the turns were just reparented onto one of them.
    all_plans = [*(extra_plans or []), *all_plans]
    indexed_plans = list(enumerate(all_plans))
    limit = DEFAULT_MAX_SPANS if max_spans is None else max_spans
    remaining = 0
    if limit and len(all_plans) > limit:
        remaining = len(all_plans) - limit
        indexed_plans = indexed_plans[:limit]
        indexed_plans.append(
            (
                len(all_plans),
                PlannedSpan(
                    path="truncation-marker",
                    span_type="marker",
                    name=f"{remaining} more spans not yet expanded",
                    attributes={
                        "truncated": True,
                        "remaining": remaining,
                        "hint": "probe trial expand <run> <manifest-id> --max-spans 0",
                    },
                ),
            )
        )

    # Always a dict, never None: the span body serializes without
    # exclude_none, and the server's coords field is non-nullable with
    # {} meaning "no coordinate stated" (keeps any existing one). Resolved
    # ONCE, so every span in the batch carries the same coordinate.
    resolved_coords = unit_context.merged_coords(coords)
    spans = []
    for trajectory_index, plan in indexed_plans:
        parent = (
            span_id_for(run.id, trial, plan.parent_path) if plan.parent_path else root_span_id
        )
        spans.append(
            SpanCreate(
                id=span_id_for(run.id, trial, plan.path),
                span_type=plan.span_type,
                parent_span_id=parent,
                name=plan.name,
                step_index=step_index,
                external_key=f"{trial}:{plan.path}",
                status=plan.status,
                started_at=plan.started_at,
                ended_at=plan.ended_at,
                attributes={
                    **plan.attributes,
                    # Connector-owned presentation metadata. This intentionally
                    # overrides a parser-supplied key so every format shares one
                    # trustworthy ordering contract.
                    "trajectory_index": trajectory_index,
                },
                # `summary_metrics` since the rename -- see
                # `probe.sdk.run.Run.span` for what passing the old name here
                # costs: the kwarg lands nowhere and the span ships a null into
                # a server field that is a plain dict.
                summary_metrics={},
                coords=resolved_coords,
            )
        )
    for start in range(0, len(spans), _SPAN_POST_CHUNK):
        batch = SpanBatch(spans=spans[start : start + _SPAN_POST_CHUNK])
        run._client.write(
            "POST",
            f"/v1/runs/{run.id}/spans",
            batch.model_dump(mode="json"),
            strict=strict,
        )
    report: dict[str, Any] = {
        "format": fmt,
        "expanded": True,
        "spans": len(spans),
        "truncated": remaining > 0,
    }
    if remaining:
        report["remaining"] = remaining
    if isinstance(doc.get("final_metrics"), dict):
        report["final_metrics"] = doc["final_metrics"]
    return report
