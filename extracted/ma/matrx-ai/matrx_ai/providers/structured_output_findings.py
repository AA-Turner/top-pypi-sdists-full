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


def response_format_identity(response_format: Any) -> dict[str, Any]:
    """Name + fingerprint of the declared schema inside a unified response_format."""
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
    return {"schema_name": name, "schema_fingerprint": schema_fingerprint(schema)}


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


def _agent_identity() -> dict[str, Any]:
    try:
        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — identity is best-effort, never fatal
        ctx = None
    if ctx is None:
        return {}
    metadata = getattr(ctx, "metadata", None) or {}
    identity = {
        "agent_id": getattr(ctx, "agent_id", None),
        "agent_version_id": getattr(ctx, "agent_version_id", None),
        "source_feature": getattr(ctx, "source_feature", None) or None,
    }
    if isinstance(metadata, dict):
        # System and internal runs carry no agent_id on the context; the run's
        # own label (``agent_factory:<name>``, ``mandate:<key>``) is then the
        # name a person can act on.
        for key in ("mandate_key", "agent_run_label", "agent_name", "surface_name"):
            if metadata.get(key):
                identity[key] = str(metadata[key])[:200]
    return {k: v for k, v in identity.items() if v}


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
    was_recovered: bool = True,
) -> bool:
    """Record a finding from SYNCHRONOUS code. Returns whether it was handed off.

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
    detail = {**_agent_identity(), **detail}
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


async def flush_translation_findings(*, model: str | None) -> None:
    """Record everything buffered for the current call (called once, by the
    dispatch seam, when the provider call ends — success or failure)."""
    pending = _PENDING.get()
    if not pending:
        return
    _PENDING.set([])
    for item in pending:
        base = {
            "schema_name": item.get("schema_name"),
            "schema_fingerprint": item.get("schema_fingerprint"),
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
            )
        elif item["relaxed"]:
            await record_structured_output_finding(
                RELAXED,
                provider=item["provider"],
                model=model,
                detail={**base, "relaxed": item["relaxed"], "narrowed": item["narrowed"]},
            )
        elif item["narrowed"]:
            await record_structured_output_finding(
                NARROWED,
                provider=item["provider"],
                model=model,
                detail={**base, "narrowed": item["narrowed"]},
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
    "record_structured_output_finding",
    "record_structured_output_finding_sync",
    "response_format_identity",
    "schema_fingerprint",
]
