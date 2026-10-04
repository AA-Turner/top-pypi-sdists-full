"""Structured-output findings — every time a translator could not send the
contract exactly as declared, the platform RECORDS it.

Arman, 2026-09-27: the shape we hold is modified by each provider's translator,
and a provider rejecting our request is OUR translator's bug. The corollary is
that every compromise a translator makes must be visible and attributable, so
the schema (or the translator) gets fixed:

* a translator that narrows or relaxes a schema calls :func:`note_translation`
  (sync — translators are sync) and the note is buffered on the CURRENT call;
* the ONE dispatch seam every provider call passes through
  (``UnifiedAIClient._dispatch_with_billing_net``) opens the buffer and, when the
  call ends, :func:`flush_translation_findings` records it as an ops issue event;
* the Anthropic grammar-budget ladder records each rung's OUTCOME directly with
  :func:`record_structured_output_finding`.

Each finding names the agent (``agent_id`` / ``agent_version_id`` from the
request context), the shape (response-format name + a fingerprint of the schema
as declared), the provider/model, and exactly what was given up. It lands in
``ops.ops_issue_event`` under a stable class key, which the platform's ``errors``
surface (``issue_class``) lists — nothing here is a log line nobody reads.

Before 2026-09-27 the grammar-budget retry wrote one event per attempt, BEFORE
the attempt ran (so ``was_recovered`` was always false), under a class with no
agent and no schema: 220 events in six weeks and not one could be acted on.
"""

from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Any

from matrx_utils import vcprint

#: Issue-class keys. One class per OUTCOME, so the issue surface says what the
#: user actually got.
NARROWED = "structured_output.narrowed"  # output still valid under the declared contract
RELAXED = "structured_output.relaxed"  # provider no longer enforces part of the contract
TOOLS_SHED = "structured_output.tools_shed"  # schema kept, the request's tools removed
ENFORCEMENT_DROPPED = "structured_output.enforcement_dropped"  # prompt-guided, checked after

#: The outcome the other four exist to prevent, recorded when it happens anyway.
#: Owned by ``matrx_ai.schema.answer_contract``; the key lives here so the
#: severity table stays in one place.
ANSWER_OFF_CONTRACT = "structured_output.answer_off_contract"

_SEVERITY = {
    NARROWED: "medium",
    RELAXED: "high",
    TOOLS_SHED: "high",
    ENFORCEMENT_DROPPED: "high",
    ANSWER_OFF_CONTRACT: "high",
}

_PENDING: ContextVar[list[dict[str, Any]] | None] = ContextVar(
    "structured_output_translation_findings", default=None
)


def schema_fingerprint(schema: Any) -> str | None:
    """A short stable id for the schema AS DECLARED, so repeated findings for
    one shape group together no matter which run produced them."""
    if not isinstance(schema, dict):
        return None
    raw = json.dumps(schema, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def schema_name_from_schema(schema: Any) -> str | None:
    """A name for a schema that arrived without one.

    Every Google finding landed with ``schema_name`` null because the hydrated
    Gemini envelope carries no ``name`` and this function read nothing else — so
    the reader was told which agent and not which shape. A registered kind states
    its identity INSIDE the schema, as the ``__kind`` const, which is the most
    precise name available; ``title`` is the next best.
    """
    if not isinstance(schema, dict):
        return None
    kind = (schema.get("properties") or {}).get("__kind")
    if isinstance(kind, dict):
        const = kind.get("const")
        if isinstance(const, str) and const:
            return const
        enum = kind.get("enum")
        if isinstance(enum, list) and len(enum) == 1 and isinstance(enum[0], str):
            return enum[0]
    title = schema.get("title")
    return title if isinstance(title, str) and title else None


def response_format_identity(response_format: Any) -> dict[str, Any]:
    """Name + fingerprint of the declared schema inside a unified response_format.

    A finding has to name BOTH the agent and the shape or nobody can act on it.
    Measured over all 89 live rows on 2026-09-27: **not one** named both — the
    Anthropic rows carried the shape and no agent, the Google rows the agent and
    no shape. This is the shape half; :func:`_agent_identity` is the other.
    """
    if not isinstance(response_format, dict):
        return {}
    inner = response_format.get("json_schema")
    name = response_format.get("name")
    schema = response_format.get("schema")
    if isinstance(inner, dict):
        name = inner.get("name") or name
        schema = (
            inner.get("schema")
            if isinstance(inner.get("schema"), dict)
            else (inner if {"type", "properties"} & inner.keys() else schema)
        )
    return {
        "schema_name": name or schema_name_from_schema(schema),
        "schema_fingerprint": schema_fingerprint(schema),
    }


#: Findings from the capability GATES, which run before the call — so whether the
#: request was really recovered is not known when they fire. Until 2026-09-28 the
#: gates wrote ``was_recovered=True`` synchronously, before the provider was even
#: called, and a call that then failed still read "recovered"
#: (SCHEMA-TRANSLATION-VERIFY.md, R11). A finding recorded with
#: ``was_recovered=None`` waits here and is written by the dispatch seam's flush,
#: with the outcome the call actually had.
_GATE_PENDING: ContextVar[list[dict[str, Any]] | None] = ContextVar(
    "structured_output_gate_findings", default=None
)


#: True while a dry run (prompt preview) simulates the gates: no call happens, so nothing
#: it would give up is a finding — it is shown in the preview instead.
_SIMULATING: ContextVar[bool] = ContextVar("structured_output_gate_simulation", default=False)


@contextmanager
def simulating_gates():
    """Run the capability gates for a preview: record nothing, leave no pending finding."""
    token = _SIMULATING.set(True)
    pending_token = _GATE_PENDING.set([])
    try:
        yield
    finally:
        _GATE_PENDING.reset(pending_token)
        _SIMULATING.reset(token)


def open_gate_findings() -> None:
    """Start a fresh gate buffer for the call about to be gated. Anything left
    from a call that never reached the provider is written now, as NOT
    recovered, rather than dropped or blamed on the next call."""
    stale = _GATE_PENDING.get()
    _GATE_PENDING.set([])
    for item in stale or ():
        record_structured_output_finding_sync(
            item["key"],
            provider=item["provider"],
            model=item["model"],
            detail={
                **item["detail"],
                "outcome": "the call never reached the provider after this adjustment",
            },
            was_recovered=False,
        )


def begin_translation_findings() -> Token:
    """Open a fresh buffer for the current provider call."""
    return _PENDING.set([])


def end_translation_findings(token: Token) -> None:
    _PENDING.reset(token)


def note_translation(
    provider: str,
    *,
    narrowed: list[str] | None = None,
    relaxed: list[str] | None = None,
    dropped: str | None = None,
    response_format: Any = None,
) -> None:
    """Buffer what a translator gave up for THIS call. Never raises. Outside a
    dispatch (a script, a unit test) there is no buffer, and the translator's own
    vcprint remains the announcement.

    ``dropped`` — the provider's native enforcement was not used at all for this
    call (the reason). The answer is then guided by the JSON text contract in the
    prompt (``schema.answer_contract.json_text_contract``) and CHECKED against the
    declared schema afterwards (``verify_answer_and_record``), which lands a
    separate ``answer_off_contract`` finding when the answer misses it. Before
    2026-09-27 this line claimed both and the platform did neither."""
    if not (narrowed or relaxed or dropped):
        return
    pending = _PENDING.get()
    if pending is None:
        return
    pending.append(
        {
            "provider": provider,
            "narrowed": list(narrowed or []),
            "relaxed": list(relaxed or []),
            "dropped": dropped,
            **response_format_identity(response_format),
        }
    )


#: Metadata keys that an ``AppContext`` ACTUALLY carries, verified by finding
#: their writers (2026-09-27). The fallback added on 2026-09-27 read
#: ``agent_run_label`` and ``surface_name``; **neither is ever written to
#: ``AppContext.metadata`` anywhere in either repository** — ``agent_run_label``
#: lives in the ``context`` JSONB of a ``runtime.global_execution`` row
#: (``services/runtime/internal_agent_runs.py``), not on the context — so the
#: fallback could not fire, and 65 of 68 live findings arrived with no agent
#: named. A fallback that cannot fire is the same defect as no fallback, wearing
#: a comment that says otherwise.
#:
#: ``conversation_step_label`` is where an internal run's label really lands
#: (``agents/executor.py`` → ``resolve_step_label_for_title(label, agent.name)``,
#: so ``agent_factory:<name>`` reaches it), and ``runtime_execution_id`` is the
#: `runtime.global_execution` row whose ``context.agent_run_label`` IS that label
#: — which is how a reader gets from a finding to the run.
_IDENTITY_METADATA_KEYS: tuple[str, ...] = (
    "mandate_key",
    "agent_name",
    "conversation_step_label",
    "runtime_execution_id",
)

#: What makes a finding attributable: at least one of these must be present, or
#: nobody can act on it.
_ACTIONABLE_IDENTITY_KEYS: frozenset[str] = frozenset(
    {
        "agent_id",
        "agent_version_id",
        "mandate_key",
        "agent_name",
        "conversation_step_label",
        "runtime_execution_id",
    }
)


def _agent_identity() -> dict[str, Any]:
    """WHO this finding belongs to. Never returns an un-actionable dict silently:
    when nothing identifies the run, it says so with ``agent_attribution`` so the
    gap is visible on the issue surface instead of looking like an empty column."""
    try:
        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — identity is best-effort, never fatal
        ctx = None
    if ctx is None:
        return {"agent_attribution": "no app context on this call"}
    metadata = getattr(ctx, "metadata", None) or {}
    identity: dict[str, Any] = {
        "agent_id": getattr(ctx, "agent_id", None),
        "agent_version_id": getattr(ctx, "agent_version_id", None),
        "source_feature": getattr(ctx, "source_feature", None) or None,
        # Where the run came from, so a finding with no agent at all is still a
        # place someone can start.
        "route": getattr(ctx, "route", None) or None,
        "source_app": getattr(ctx, "source_app", None) or None,
        "request_id": getattr(ctx, "request_id", None) or None,
        "conversation_id": getattr(ctx, "conversation_id", None) or None,
        "organization_id": getattr(ctx, "organization_id", None) or None,
    }
    if isinstance(metadata, dict):
        # A system or internal run carries no agent_id on the context; the run's
        # own label is then the name a person can act on.
        for key in _IDENTITY_METADATA_KEYS:
            if metadata.get(key):
                identity[key] = str(metadata[key])[:200]
    identity = {k: v for k, v in identity.items() if v}
    if not (_ACTIONABLE_IDENTITY_KEYS & identity.keys()):
        identity["agent_attribution"] = (
            "UNATTRIBUTED: this call carried no agent id, mandate key, agent name or "
            "run label on its app context — fix the caller's attribution "
            "(matrx_ai.agents.source_tracking) so the next one names a run"
        )
    return identity


async def record_structured_output_finding(
    key: str,
    *,
    provider: str,
    model: str | None,
    detail: dict[str, Any],
    was_recovered: bool = True,
) -> None:
    """Write one finding to the platform's issue sink, attributed to the agent
    on the current request. Never raises into the caller's request."""
    try:
        from matrx_ai.ops.issue_capture import capture_issue

        await capture_issue(
            key,
            error_type=key.rsplit(".", 1)[-1],
            provider=provider,
            model=model,
            is_retryable=False,
            was_recovered=was_recovered,
            severity=_SEVERITY.get(key, "medium"),
            detail={**_agent_identity(), **detail},
        )
    except Exception as exc:  # noqa: BLE001 — a broken sink never breaks the call
        vcprint(f"[structured_output_findings] could not record {key}: {exc}", color="red")


def record_structured_output_finding_sync(
    key: str,
    *,
    provider: str,
    model: str | None,
    detail: dict[str, Any],
    was_recovered: bool | None = True,
) -> bool:
    """Record a finding from SYNCHRONOUS code. Returns whether it was handed off.

    ``was_recovered=None`` means "not known yet": the finding is held for the
    dispatch seam's flush, which writes it with the call's real outcome.

    For the capability gates in ``UnifiedAIClient`` — the two places the schema or
    the tool surface is genuinely thrown away, ABOVE every translator, where
    ``note_translation``'s buffer is not open yet and the functions are sync and
    shared with the build-only ``translate_request`` path (so they cannot become
    coroutines without changing a caller another lane owns).

    The agent identity is captured HERE, in the caller's context, and passed in
    the detail: :func:`detached_task` deliberately does not inherit the caller's
    ContextVars, so ``try_get_app_context()`` inside the spawned task would find
    nothing and the finding would arrive with no agent named — the exact defect
    that left 65 of 68 rows unattributable.
    """
    if _SIMULATING.get():
        return False  # a preview: the call never happens, so nothing is given up
    detail = {**_agent_identity(), **detail}
    if was_recovered is None:
        pending = _GATE_PENDING.get()
        if pending is None:
            pending = []
            _GATE_PENDING.set(pending)
        pending.append({"key": key, "provider": provider, "model": model, "detail": detail})
        return True
    try:
        import asyncio

        asyncio.get_running_loop()
        from matrx_utils import detached_task

        detached_task(
            record_structured_output_finding(
                key, provider=provider, model=model, detail=detail, was_recovered=was_recovered
            ),
            name=f"structured_output_finding:{key.rsplit('.', 1)[-1]}",
        )
        return True
    except RuntimeError:
        # No running loop (an offline resolution, a unit test) — say so rather
        # than pretending the finding landed.
        vcprint(
            f"[structured_output_findings] {key} not recorded: no running event loop. "
            f"detail={ {k: v for k, v in detail.items() if k != 'schema_fingerprint'} }",
            color="yellow",
        )
        return False
    except Exception as exc:  # noqa: BLE001 — a broken sink never breaks the call
        vcprint(f"[structured_output_findings] could not hand off {key}: {exc}", color="red")
        return False


def translation_outcome(
    succeeded: bool | None, answer_off_contract: bool | None
) -> tuple[bool, str]:
    """THE ONE PLACE ``was_recovered`` is decided for a structured-output finding,
    and it is decided only from facts that have already happened.

    A compromise is RECOVERED when the call it was made for came back AND the
    answer that came back met the declared contract. Anything else is not
    recovered, and the sentence says which of the four it was so a reader never
    has to infer it:

    * ``succeeded is None`` — build-only translate (the batch lane): the outcome
      arrives hours later, so nothing is asserted;
    * ``succeeded is False`` — the call failed, so the compromise bought nothing;
    * ``answer_off_contract is True`` — the call returned and the answer MISSED
      the contract, which is the opposite of recovered;
    * ``answer_off_contract is None`` — no contract was bound on this call, so
      there was no answer to judge; the request being served is all "recovered"
      can mean here and the sentence says exactly that.

    Until 2026-09-28 the three translation writes below passed no
    ``was_recovered`` at all and took :func:`record_structured_output_finding`'s
    default ``True``, so every one of the 279 live translation findings claimed a
    recovery nothing had measured (SCHEMA-TRANSLATION-VERIFY.md, F2). The gate
    half read only ``succeeded``, so a served call whose answer then missed the
    contract still read "recovered".
    """
    if succeeded is None:
        return False, (
            "outcome not known when the request was built (build-only translate) — "
            "nothing is asserted about recovery"
        )
    if not succeeded:
        return False, "the call then FAILED — the compromise did not recover it"
    if answer_off_contract:
        return False, (
            "the call returned and the answer was then judged OFF CONTRACT — "
            "the compromise did not deliver the declared shape"
        )
    if answer_off_contract is None:
        return True, (
            "the call then succeeded; no output contract was bound on it, so there was "
            "no answer to judge against one"
        )
    return True, "the call then succeeded and its answer was judged ON CONTRACT"


async def flush_translation_findings(
    *,
    model: str | None,
    succeeded: bool | None = None,
    answer_off_contract: bool | None = None,
) -> None:
    """Record everything buffered for the current call (called once, by the
    dispatch seam, when the provider call ends — success or failure).

    ``succeeded`` is the call's real outcome: ``True``/``False`` on a live call,
    ``None`` on a build-only translate (the batch lane), whose outcome arrives
    long after this. ``answer_off_contract`` is what the seam's own answer check
    found (``None`` when no contract was bound, so nothing was judged). Both are
    read ONLY through :func:`translation_outcome`, the single decision point for
    every finding written here — gate half and translation half alike."""
    recovered, outcome = translation_outcome(succeeded, answer_off_contract)
    gate = _GATE_PENDING.get()
    if gate:
        _GATE_PENDING.set([])
        for item in gate:
            await record_structured_output_finding(
                item["key"],
                provider=item["provider"],
                model=item["model"] or model,
                detail={**item["detail"], "outcome": outcome},
                was_recovered=recovered,
            )
    pending = _PENDING.get()
    if not pending:
        return
    _PENDING.set([])
    for item in pending:
        base = {
            "schema_name": item.get("schema_name"),
            "schema_fingerprint": item.get("schema_fingerprint"),
            "outcome": outcome,
        }
        if item.get("dropped"):
            await record_structured_output_finding(
                ENFORCEMENT_DROPPED,
                provider=item["provider"],
                model=model,
                detail={
                    **base,
                    "action": item["dropped"],
                    "narrowed": item["narrowed"],
                    "relaxed": item["relaxed"],
                },
                was_recovered=recovered,
            )
        elif item["relaxed"]:
            await record_structured_output_finding(
                RELAXED,
                provider=item["provider"],
                model=model,
                detail={**base, "relaxed": item["relaxed"], "narrowed": item["narrowed"]},
                was_recovered=recovered,
            )
        elif item["narrowed"]:
            await record_structured_output_finding(
                NARROWED,
                provider=item["provider"],
                model=model,
                detail={**base, "narrowed": item["narrowed"]},
                was_recovered=recovered,
            )


__all__ = [
    "ANSWER_OFF_CONTRACT",
    "ENFORCEMENT_DROPPED",
    "NARROWED",
    "RELAXED",
    "TOOLS_SHED",
    "begin_translation_findings",
    "end_translation_findings",
    "flush_translation_findings",
    "note_translation",
    "open_gate_findings",
    "record_structured_output_finding",
    "record_structured_output_finding_sync",
    "response_format_identity",
    "schema_name_from_schema",
    "schema_fingerprint",
    "translation_outcome",
]
