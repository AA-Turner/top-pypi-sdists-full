"""Runtime support for picklist-bound agent variables (the secret-description path).

A picklist-bound variable arrives from the client as a *reference envelope*, never as
text:

    {"type": "picklist_ref", "list_id": "<uuid>", "list_item_id": "<uuid>", "label": "High"}

The host resolver (aidream) turns each envelope into:
  * a CANONICAL substitution value — an opaque PLACEHOLDER token — which is what gets
    substituted into ``UnifiedConfig`` and therefore persisted / snapshotted / labeled.
    The token is NOT the secret; the real ``description`` never touches the canonical config.
  * a WIRE swap — ``{placeholder_token: description}`` — stashed on a per-request ContextVar
    here. Immediately before the provider call, the executor materializes the swaps into a
    throwaway clone of the config (system_instruction + messages only) so the secret reaches
    the model on the wire and NOWHERE else (not cx_conversation, not cx_message, not
    cx_request_snapshot, not the conversation title).

This module is the single source of truth shared by the host resolver, the executor's
clone-at-send seam, and the ``replace_variables`` tripwire.
"""

from __future__ import annotations

import contextvars
import copy
import re as _re
from collections.abc import Callable
from typing import Any

from matrx_utils import vcprint
from pydantic import BaseModel

from matrx_ai.config.structured_input_config import _StructuredInputBase

PICKLIST_REF_TYPE = "picklist_ref"

# Private-use delimiter — cannot appear in user-authored text, so the wire swap can never
# collide with real prompt content. Persisted in the canonical system_instruction (which is
# server-side config, not shown in chat); never the secret.
_DELIM = ""


def is_picklist_ref(value: Any) -> bool:
    """True iff ``value`` is a picklist reference envelope (a dict with the exact tag and
    string ids). A plain string that merely *looks* like JSON is never a dict here, so this
    can never misfire on normal text variables."""
    return (
        isinstance(value, dict)
        and value.get("type") == PICKLIST_REF_TYPE
        and isinstance(value.get("list_item_id"), str)
        and bool(value.get("list_item_id"))
    )


def value_has_picklist_ref(value: Any) -> bool:
    """True for a single envelope OR a list containing at least one envelope (multi-select)."""
    if is_picklist_ref(value):
        return True
    if isinstance(value, list):
        return any(is_picklist_ref(v) for v in value)
    return False


def picklist_placeholder(var_name: str) -> str:
    """Opaque, collision-proof canonical token for a picklist-bound variable."""
    return f"{_DELIM}matrx:picklist:{var_name}{_DELIM}"


def neutralize_terminal(text: str) -> str:
    """Make a resolved description a terminal literal: defang ``{{`` and ``<<MATRX`` so it
    can NOT be re-expanded by a later ``replace_variables`` pass or by ``resolve_matrx_patterns``
    (which ``SystemInstruction.__str__`` runs on every render)."""
    if not text:
        return text
    # Zero-width space breaks the literal trigger sequences while staying visually identical.
    zwsp = "​"
    return text.replace("{{", "{" + zwsp + "{").replace("<<MATRX", "<" + zwsp + "<MATRX")


# ── Per-request wire swaps (NEVER persisted) ─────────────────────────────────────────────
_WIRE_SWAPS: contextvars.ContextVar[dict[str, str]] = contextvars.ContextVar(
    "matrx_picklist_wire_swaps", default={}
)


def set_wire_swaps(swaps: dict[str, str]) -> None:
    """Replace the current request's token→description map. Always called by the resolver
    (even with an empty dict) so a previous run in the same task can never bleed through."""
    _WIRE_SWAPS.set(dict(swaps or {}))


def get_wire_swaps() -> dict[str, str]:
    return _WIRE_SWAPS.get()


def clear_wire_swaps() -> None:
    _WIRE_SWAPS.set({})


# The map that ACTUALLY materialized into the last send's payload (post-budget):
# identical to _WIRE_SWAPS except a value the per-send budget TRUNCATED carries its
# truncated head here, not the full original. Snapshot redaction reverses against
# THIS map so a truncated reference value (whose head is what's really on the wire)
# is still replaced by its fence key — reversing against the full original would
# miss it and leave partial reference content in cx_request_snapshot. Set by
# build_wire_config every send; None until the first send in this context.
_MATERIALIZED_WIRE_SWAPS: contextvars.ContextVar[dict[str, str] | None] = contextvars.ContextVar(
    "matrx_materialized_wire_swaps", default=None
)


# Matches any residual canonical placeholder token (delimiter ... delimiter).
_RESIDUAL_TOKEN = _re.compile(f"{_DELIM}matrx:picklist:[^{_DELIM}]*{_DELIM}")

# Swap keys with this prefix are host-encoded reference fences (not picklist
# tokens) — role-gated in build_wire_config (never applied to assistant text).
_FENCE_SWAP_PREFIX = "```matrx"

# ── Wire-swap character budget (Layer 2 — the materialization-seam backstop) ─────────────
# (Measured in characters, like the tool-result size gate — len()/cap_text slice
#  on code points, matching output_caps.py's char-based cost model.)
#
# ``build_wire_config`` is the ONE point where referenced fence values actually
# expand into the provider payload, and it runs on EVERY loop iteration — so an
# oversized reference value is re-billed to the model every single send. That is
# the exact cost-bomb class the tool-result size gate kills (matrx_ai/tools/
# output_caps.py: soft 50K, ceiling 500K), reintroduced at the reference seam.
#
# The aidream host already budgets fence swaps at STAGING time (Layer 1:
# services/references/substitute.py::_enforce_swap_budget — single 1M / total 2M).
# THIS is the independent Layer-2 backstop at the materialization seam: it fires
# even when Layer 1 is bypassed (a standalone matrx-ai host with no reference
# stager), silently broken, or when several staging batches merged into one
# oversized ``_WIRE_SWAPS`` map that no single Layer-1 evaluation ever saw. Per
# the platform doctrine, a class of failure is not extinct until ≥2 independent
# layers each stop it alone and SCREAM when they fire.
#
# Numbers are tuning CAPS (a behavior change is a code push — fine; that beats a
# silent prod cost blow-up), NEVER env vars. Set at/above Layer 1's caps so this
# backstop never truncates traffic Layer 1 deliberately allowed — it only bites
# the cumulative / bypassed / broken cases Layer 1 cannot see.
WIRE_SWAP_SINGLE_VALUE_MAX_CHARS = 1_000_000  # one materialized fence value ceiling
WIRE_SWAP_TOTAL_MAX_CHARS = 2_000_000  # all fence values in ONE send, summed

_WIRE_SWAP_TRUNCATION_NOTICE = (
    "\n\n[⚠️ value truncated by the per-send wire-swap budget — this reference "
    "value exceeded the materialization ceiling and was re-billed on every send. "
    "Fetch the part you need with value_store get(key=…, max_chars=…) or narrow "
    "the reference with a field path instead of substituting the whole value.]"
)


class WireSwapBudgetEvent(BaseModel):
    """One firing of the Layer-2 wire-swap budget — handed to every registered
    sink, typed end to end. Emitted only when at least one fence value had to be
    truncated to fit the per-send byte budget."""

    reasons: list[str]
    """Which cap(s) fired: ``single_value_capped`` and/or ``total_budget_capped``."""
    truncated_count: int
    """How many oversized fence values were truncated (head + fetch notice)."""
    skipped_count: int = 0
    """How many fine fence values were skipped (left verbatim) once the per-send
    total budget was exhausted."""
    fence_swap_count: int
    """Total fence-shaped swaps staged for this send."""
    total_fence_chars: int
    """Sum of fence-swap value chars BEFORE truncation (the re-billed size)."""
    largest_value_chars: int
    """Chars of the single largest fence value before truncation."""
    single_cap: int
    total_cap: int


_WIRE_SWAP_BUDGET_SINKS: list[Callable[[WireSwapBudgetEvent], None]] = []


def register_wire_swap_budget_sink(sink: Callable[[WireSwapBudgetEvent], None]) -> None:
    """Register a durable sink for wire-swap budget firings (e.g. the ops-triage
    writer). Mirrors ``result_gate.register_tool_result_gate_sink``: the host
    injects a DB writer here (matrx-ai must not import a host's DB layer); absent
    a sink only the console banner runs, so the package stays standalone. Sinks
    must be best-effort and non-blocking — a sink that raises is isolated so one
    bad sink never breaks a provider send."""
    _WIRE_SWAP_BUDGET_SINKS.append(sink)


def _emit_wire_swap_budget(event: WireSwapBudgetEvent) -> None:
    for sink in _WIRE_SWAP_BUDGET_SINKS:
        try:
            sink(event)
        except Exception as exc:  # noqa: BLE001 — a sink must never break a send
            vcprint(f"[wire-swap-budget] sink raised, ignored: {exc}", color="yellow")


def _console_wire_swap_budget_sink(event: WireSwapBudgetEvent) -> None:
    vcprint(
        data={
            "reasons": event.reasons,
            "truncated_count": event.truncated_count,
            "skipped_count": event.skipped_count,
            "fence_swap_count": event.fence_swap_count,
            "total_fence_chars": event.total_fence_chars,
            "largest_value_chars": event.largest_value_chars,
            "single_cap": event.single_cap,
            "total_cap": event.total_cap,
        },
        title=(
            "🚨 WIRE-SWAP BUDGET FIRED — a referenced value exceeded the per-send "
            "materialization ceiling and was TRUNCATED before the provider call.\n"
            "This value would otherwise be re-billed on every loop iteration (the "
            "tool-result size-gate cost-bomb class, at the reference seam). The "
            "consumer should pass a field path / value_store get(max_chars=…) "
            "instead of substituting whole large values."
        ),
        color="red",
        verbose=True,
    )


_WIRE_SWAP_BUDGET_SINKS.append(_console_wire_swap_budget_sink)


def _apply_wire_swap_budget(
    swaps: dict[str, str], *, weights: dict[str, int] | None = None
) -> dict[str, str]:
    """Layer-2 backstop: bound the characters of FENCE-shaped swap values that
    materialize into one provider send. Picklist tokens are EXEMPT (server-minted
    short placeholders, never a cost bomb). Two graceful-degrade modes, so the
    materialized total NEVER exceeds ``WIRE_SWAP_TOTAL_MAX_CHARS`` and a fence
    value is never silently lost:

    * A value that is ITSELF oversized (over the single-value cap) is TRUNCATED to
      a code-point-safe head (``cap_text``) + a self-describing fetch notice, sized
      so ``head + notice`` fits within its char allotment — the model sees real
      content + how to fetch the rest.
    * A value that is fine on its own but for which the per-send TOTAL budget is
      exhausted is SKIPPED — the swap is dropped so the ```matrx fence stays
      VERBATIM in the message (Layer-1's degrade: the model sees the reference and
      can re-fetch it). We never mangle a fine value into a useless fragment, and a
      skip materializes zero characters.

    ``weights`` maps a fence key → how many times it will actually materialize into
    this send (the SAME fence pasted into N texts, or repeated within one, is
    substituted N times — each copy re-billed on every loop iteration). The
    per-send TOTAL is budgeted against the REAL materialized characters
    (Σ weight × len(value)), NOT the distinct-map sum, so a value referenced across
    several turns cannot multiply past the ceiling uncounted. A missing weight
    defaults to 1; weight 0 means the fence isn't present this send (materializes
    nothing) and is left untouched, exempt from the budget. The single-value cap is
    per-occurrence (one copy ≤ the single cap).

    One ops-triage alarm fires per send that truncated OR skipped anything. Never
    raises — a budget failure must not break a provider send."""
    try:
        _weights = weights or {}

        def _weight(key: str) -> int:
            return max(0, _weights.get(key, 1))

        fence_items = [(k, v) for k, v in swaps.items() if k.startswith(_FENCE_SWAP_PREFIX)]
        if not fence_items:
            return swaps
        # Occurrence-weighted materialized total (the true re-billed size), and the
        # largest SINGLE-occurrence value (the per-occurrence cap is unweighted).
        total_fence = sum(_weight(k) * len(v) for k, v in fence_items)
        largest = max((len(v) for _, v in fence_items), default=0)
        # Fast path — everything comfortably within budget (the overwhelming case).
        if largest <= WIRE_SWAP_SINGLE_VALUE_MAX_CHARS and total_fence <= WIRE_SWAP_TOTAL_MAX_CHARS:
            return swaps

        from matrx_ai.tools.output_caps import cap_text

        notice_len = len(_WIRE_SWAP_TRUNCATION_NOTICE)
        result = dict(swaps)
        reasons: set[str] = set()
        truncated = 0
        skipped = 0
        running = 0  # real materialized fence characters committed so far
        # Largest first: materialize the giants (capped) before spending budget on
        # smaller values, so the total budget preserves the most values intact.
        for key, value in sorted(fence_items, key=lambda kv: len(kv[1]), reverse=True):
            w = _weight(key)
            if w == 0:
                continue  # not present this send → never materializes, no budget
            size = len(value)
            remaining = max(0, WIRE_SWAP_TOTAL_MAX_CHARS - running)
            # Per-occurrence room left in the total (each of the w copies pays).
            per_occ_remaining = remaining // w
            if size > WIRE_SWAP_SINGLE_VALUE_MAX_CHARS:
                # Genuinely oversized on its own → truncate to a useful head +
                # notice, bounded by BOTH the single cap and the remaining total
                # (divided across its w occurrences).
                reasons.add("single_value_capped")
                allotment = min(WIRE_SWAP_SINGLE_VALUE_MAX_CHARS, per_occ_remaining)
                body_limit = allotment - notice_len
                if body_limit > 0:
                    capped, _info = cap_text(value, limit=body_limit)
                    materialized = capped + _WIRE_SWAP_TRUNCATION_NOTICE
                    result[key] = materialized  # per-occ len <= per_occ_remaining
                    running += w * len(materialized)  # <= remaining
                    truncated += 1
                else:
                    # No room even for a head → skip verbatim (fence stays).
                    del result[key]
                    reasons.add("total_budget_capped")
                    skipped += 1
            elif w * size > remaining:
                # Value is fine on its own; its full materialization (w copies)
                # overflows the per-send TOTAL → SKIP verbatim (never fragment a
                # fine value). Zero characters emitted.
                del result[key]
                reasons.add("total_budget_capped")
                skipped += 1
            else:
                running += w * size  # full value fits within budget
        if truncated or skipped:
            _emit_wire_swap_budget(
                WireSwapBudgetEvent(
                    reasons=sorted(reasons),
                    truncated_count=truncated,
                    skipped_count=skipped,
                    fence_swap_count=len(fence_items),
                    total_fence_chars=total_fence,
                    largest_value_chars=largest,
                    single_cap=WIRE_SWAP_SINGLE_VALUE_MAX_CHARS,
                    total_cap=WIRE_SWAP_TOTAL_MAX_CHARS,
                )
            )
        return result
    except Exception as exc:  # noqa: BLE001 — the budget must never break a send
        vcprint(
            f"[wire-swap-budget] enforcement failed, sending ungated: {exc}",
            color="yellow",
        )
        return swaps


def _swap_text(text: str, swaps: dict[str, str]) -> str:
    if swaps:
        # ONE pass, longest key first. A naive per-key ``str.replace`` loop can
        # re-scan a value it just substituted and expand a SHORTER key that
        # happens to sit inside that value (double-substitution / cross-reference
        # injection), and its result is dict-order dependent. A single regex
        # alternation, keys sorted longest-first, replaces each occurrence exactly
        # once at each position — deterministic, and inserted content is never
        # re-scanned. The value is supplied via a FUNCTION (not a replacement
        # string) so ``\1``-style sequences in referenced content are never
        # interpreted as backreferences.
        keys = sorted(swaps.keys(), key=len, reverse=True)
        pattern = _re.compile("|".join(_re.escape(k) for k in keys))
        text = pattern.sub(lambda m: swaps[m.group(0)], text)
    # Belt-and-suspenders: a placeholder for which no swap was staged this turn (e.g. a
    # continue turn that did not re-send the variable) must NEVER reach the model as the raw
    # token. Strip it rather than leak gibberish.
    if _DELIM in text:
        text = _RESIDUAL_TOKEN.sub("", text)
    return text


def _structured_resolved_text(content: object) -> str | None:
    """Return provider-bound text held by a resolved structured-input block.

    Structured inputs intentionally persist their original typed payload and
    keep the derived provider text under ``metadata.resolved_text``. Reference
    fences inside that text must use the same send-clone swap seam as ordinary
    TextContent; otherwise the stager finds a fence that the materializer never
    replaces.
    """
    if not isinstance(content, _StructuredInputBase):
        return None
    text = content.metadata.get("resolved_text")
    return text if isinstance(text, str) and text else None


def _count_fence_occurrences(config: Any, swaps: dict[str, str]) -> dict[str, int]:
    """How many times each FENCE-shaped swap key will actually materialize into
    this send — i.e. its total occurrence count across the texts fence swaps are
    applied to: the base instruction plus every NON-assistant message's text
    content (fences are role-gated away from assistant text in ``build_wire_config``).
    Used to budget the true materialized size, so the same fence referenced across
    several turns cannot multiply past the per-send ceiling uncounted. Best-effort
    (defaults to weight 1 on any read failure via ``_apply_wire_swap_budget``)."""
    fence_keys = [k for k in swaps if k.startswith(_FENCE_SWAP_PREFIX)]
    if not fence_keys:
        return {}
    target_texts: list[str] = []
    try:
        si = getattr(config, "system_instruction", None)
        base = getattr(si, "base_instruction", None) if si is not None else None
        if isinstance(base, str):
            target_texts.append(base)
        for msg in getattr(config, "messages", None) or []:
            role = getattr(msg, "role", None)
            role_str = str(getattr(role, "value", role) or "").lower()
            if role_str == "assistant":
                continue  # fences never materialize into assistant text
            for content in getattr(msg, "content", None) or []:
                if getattr(content, "type", None) == "text" and isinstance(
                    getattr(content, "text", None), str
                ):
                    target_texts.append(content.text)
                    continue
                structured_text = _structured_resolved_text(content)
                if structured_text:
                    target_texts.append(structured_text)
    except Exception:  # noqa: BLE001 — weighting is best-effort; default is 1
        return {}
    return {key: sum(t.count(key) for t in target_texts) for key in fence_keys}


def build_wire_config(config: Any) -> Any | None:
    """Return a clone of ``config`` with picklist placeholders swapped for the real
    descriptions, or ``None`` if there is nothing to swap.

    Only ``system_instruction`` and ``messages`` are deep-copied (the rest of the config —
    tools, media, params — is shared by reference).     Uses ``copy.copy`` so the dataclass
    ``__post_init__`` does NOT re-run (which would re-normalize system_instruction and
    re-trigger ``resolve_matrx_patterns``).

    This is the single clone-at-send seam for every wire swap. The legacy picklist
    token swaps and the Matrx Envelope ``matrx``-fence reference swaps both land in
    the same per-request map (the references substitution path merges its resolved
    ``{fence_text: value}`` into ``_WIRE_SWAPS`` via ``set_wire_swaps``), so a single
    plain substring replacement materializes them all."""
    swaps = dict(get_wire_swaps())
    if not swaps:
        _MATERIALIZED_WIRE_SWAPS.set({})  # nothing materialized this send
        return None

    # Layer-2 wire-swap budget: bound the fence-value characters that materialize
    # into this send BEFORE substitution, so an oversized (or repeated) referenced
    # value is truncated/skipped here (and alarmed) rather than re-billed whole on
    # every loop iteration. Fence swaps materialize into the base instruction and
    # every NON-assistant message text (they are role-gated away from assistant
    # text below), and the SAME fence in several of those texts materializes once
    # per occurrence — so budget against the true occurrence count, not the
    # distinct-map sum. Picklist tokens are exempt (short, un-budgeted).
    fence_weights = _count_fence_occurrences(config, swaps)
    swaps = _apply_wire_swap_budget(swaps, weights=fence_weights)
    # Record what ACTUALLY materialized (post-budget) so snapshot redaction reverses
    # the real on-wire values (incl. truncated heads) → their keys, not the originals.
    _MATERIALIZED_WIRE_SWAPS.set(dict(swaps))

    clone = copy.copy(config)  # shallow: shares tools/media/params, no __post_init__
    si = getattr(config, "system_instruction", None)
    if si is not None:
        clone_si = copy.deepcopy(si)
        base = getattr(clone_si, "base_instruction", None)
        if isinstance(base, str):
            clone_si.base_instruction = _swap_text(base, swaps)
        clone.system_instruction = clone_si

    # Fence-shaped swap keys are host-encoded REFERENCES (the ```matrx fence).
    # They must never expand inside ASSISTANT-authored text: the model echoing
    # a fence it saw in a descriptor would otherwise re-inflate the full
    # referenced value into its own history on every send (the exact context
    # blow-up pass-by-reference exists to prevent). Server-minted picklist
    # placeholder tokens keep swapping everywhere — they are never model-authored.
    non_fence_swaps = {k: v for k, v in swaps.items() if not k.startswith(_FENCE_SWAP_PREFIX)}

    messages = getattr(config, "messages", None)
    if messages is not None:
        clone_messages = copy.deepcopy(messages)
        for msg in clone_messages:
            role = getattr(msg, "role", None)
            role_str = str(getattr(role, "value", role) or "").lower()
            msg_swaps = non_fence_swaps if role_str == "assistant" else swaps
            for content in getattr(msg, "content", None) or []:
                if getattr(content, "type", None) == "text" and isinstance(
                    getattr(content, "text", None), str
                ):
                    content.text = _swap_text(content.text, msg_swaps)
                    continue
                structured_text = _structured_resolved_text(content)
                if structured_text:
                    content.metadata["resolved_text"] = _swap_text(structured_text, msg_swaps)
        clone.messages = clone_messages

    return clone


def redact_wire_payload(payload: Any) -> Any | None:
    """Reverse-substitute the current swaps in a captured wire payload —
    each materialized VALUE is replaced by its swap KEY (the placeholder token /
    reference fence, i.e. exactly what persistence stores anyway) — so
    cx_request_snapshot keeps a debuggable payload instead of dropping it
    entirely (multi-agent reference-heavy requests would otherwise have NO
    provider-payload record at all).

    Fail-CLOSED: returns None (caller drops the payload, the pre-2026-07
    behavior) when there is nothing to redact against, when any swap value is
    too short to replace unambiguously, or when the round-trip fails — a
    secret must never survive by accident."""
    import json as _json

    # Reverse against what ACTUALLY materialized this send (post-budget: truncated
    # heads for capped values), so a budget-truncated reference value on the wire
    # is still mapped back to its key. Fall back to the canonical map if a send
    # didn't run build_wire_config in this context (materialized is None).
    materialized = _MATERIALIZED_WIRE_SWAPS.get()
    swaps = materialized if materialized is not None else get_wire_swaps()
    if payload is None or not swaps:
        return None
    if any(len(v) < 16 for v in swaps.values()):
        return None
    try:

        def _esc(text: str) -> str:
            return _json.dumps(text, ensure_ascii=False)[1:-1]

        s = _json.dumps(payload, ensure_ascii=False, default=str)
        # Longest value first: when one swap value is a substring of another
        # (a field-narrowed fence + the whole-value fence of the same json in
        # one request), replacing the shorter first would corrupt the longer.
        ordered = sorted(swaps.items(), key=lambda kv: len(kv[1]), reverse=True)
        for token, value in ordered:
            token_esc = _esc(token)
            # Single-escaped occurrence (a normal JSON string field) AND the
            # double-escaped occurrence (the value nested inside a JSON-string
            # field, e.g. OpenAI function.arguments / dumped tool content).
            for form_value, form_token in (
                (_esc(value), token_esc),
                (_esc(_esc(value)), _esc(token_esc)),
            ):
                if form_value in s:
                    s = s.replace(form_value, form_token)
        # Verify against the ESCAPED forms (the raw value can never appear in
        # a JSON dump once it contains a newline/quote/backslash — comparing
        # raw was a vacuous check). Any surviving occurrence ⇒ drop.
        for value in swaps.values():
            single = _esc(value)
            if single in s or _esc(single) in s:
                return None
        return _json.loads(s)
    except Exception:  # noqa: BLE001 — fail closed, drop the payload
        return None


def guard_unresolved_refs(variables: dict[str, Any]) -> dict[str, Any]:
    """Tripwire for ``replace_variables``: if a value reaches substitution still shaped like
    a picklist envelope, a code path bypassed the resolver. NEVER let ``str(dict)`` reach the
    model — replace it with a safe placeholder and scream so the missed path is found.

    Returns a cleaned copy when any envelope was found; otherwise returns the input
    unchanged (zero overhead for the overwhelmingly common case)."""
    has_ref = any(value_has_picklist_ref(v) for v in variables.values())
    if not has_ref:
        return variables

    cleaned: dict[str, Any] = {}
    for name, value in variables.items():
        if is_picklist_ref(value):
            cleaned[name] = value.get("label") or ""
            _report_unresolved(name)
        elif isinstance(value, list) and any(is_picklist_ref(v) for v in value):
            parts = [
                (v.get("label") or "") if is_picklist_ref(v) else ("" if v is None else str(v))
                for v in value
            ]
            cleaned[name] = ", ".join(p for p in parts if p)
            _report_unresolved(name)
        else:
            cleaned[name] = value
    return cleaned


def _report_unresolved(var_name: str) -> None:
    """Record that an unresolved picklist envelope reached substitution. Routed through the
    error-capture seam when available so it lands in a human-reviewable record; always
    screams to the log as a backstop."""
    msg = (
        f"[picklist] unresolved picklist_ref reached replace_variables for variable "
        f"'{var_name}' — a code path skipped resolve_picklist_references. Injected a safe "
        f"placeholder (label/empty) instead of the description."
    )
    vcprint(msg, color="red")
    try:
        from matrx_ai._ext import get_ext  # local import to avoid import cycles

        record_error = get_ext("record_error")
    except Exception:
        record_error = None
    if record_error is None:
        return
    try:
        import asyncio

        coro = record_error(
            RuntimeError(msg),
            kind="picklist_unresolved",
            error_type="picklist_unresolved",
            error_text=msg,
            payload={"variable": var_name},
            route="replace_variables",
        )
        if asyncio.iscoroutine(coro):
            try:
                asyncio.get_running_loop()
                from matrx_utils import detached_task

                detached_task(coro, name=f"picklist_unresolved:{var_name}")
            except RuntimeError:
                coro.close()  # no running loop; the log line above is the record
    except Exception:
        pass
