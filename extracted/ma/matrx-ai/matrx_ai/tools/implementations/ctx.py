"""Deferred context retrieval tools.

``ctx_get`` retrieves a single context object held in AppContext.metadata
(populated by the caller via the ``context`` request field).

``ctx_batch`` retrieves up to 20 context objects in one round trip — same
semantics as N independent ``ctx_get`` calls executed sequentially, but
without the per-call provider tool-loop overhead. Read-only by design;
mutating tools (``ctx_patch`` / ``ctx_create``) deliberately stay
single-call so the model commits to one mutation at a time.

Retrieval modes
---------------
full    — return the entire content string
page    — return a slice (offset + chars), returns has_more + next_offset
summary — **always succeeds**. Resolution order:
            1. AI summary when ``summary_agent_id`` is set
            2. source-backed: precomputed ``descriptor.summary`` (ToC / size)
            3. otherwise the first page, with ``fell_back_from="summary"``
"""

from __future__ import annotations

import difflib
import json
import logging
import re
import time
import traceback
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import (
    format_args_error,
    infer_missing_discriminator,
)
from matrx_ai.tools.arg_models import ContextArgs
from matrx_ai.tools.models import (
    ToolContext,
    ToolError,
    ToolOutputContractError,
    ToolResult,
)

logger = logging.getLogger(__name__)

_VALID_MODES = frozenset({"full", "page", "summary"})
_DEFAULT_PAGE_CHARS = 4000
_BATCH_MAX = 20

_ATTACHED_DOCUMENT_KEY_PREFIX = "attached_document_"

# Fuzzy "did you mean" cutoff. Deliberately NOT a reconciliation threshold —
# a fuzzy hit is only ever SUGGESTED, never substituted. See _resolve_key_alias.
_SUGGEST_CUTOFF = 0.6
_SUGGEST_MAX = 6
_INVENTORY_MAX = 40


def _normalize_key(key: str) -> str:
    """Collapse a context key to its case/separator-insensitive identity.

    ``Route Brief`` / ``route-brief`` / ``routeBrief`` / ``route_brief`` all
    normalize to ``routebrief``. This is the ONLY equivalence we treat as
    "exactly one thing the caller can mean" — it is a spelling of the same
    name, not a different name that looks similar.
    """
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _resolve_key_alias(key: str, available: list[str]) -> tuple[str | None, list[str]]:
    """Reconcile a requested key against the manifest's real keys.

    Returns ``(resolved_key, ambiguous_candidates)``.

    Per the guard-reconciliation rule: *is there exactly one thing the caller
    can mean here?* Exactly one normalized match → reconcile (the caller spelled
    an existing key differently). More than one → we refuse and NAME both, never
    guess. Zero → not an alias at all; the caller invented a key.

    Deliberately conservative: ``bundle_members`` does NOT resolve to
    ``bundle_member_count`` — those are different names, and silently
    substituting one for the other would fabricate an answer. Near-misses are
    surfaced as suggestions instead (``_did_you_mean``).
    """
    target = _normalize_key(key)
    if not target:
        return None, []
    hits = [k for k in available if _normalize_key(k) == target]
    if len(hits) == 1:
        return hits[0], []
    if len(hits) > 1:
        return None, sorted(hits)
    return None, []


def _did_you_mean(key: str, available: list[str]) -> list[str]:
    """Closest available keys by similarity — SUGGESTED only, never applied."""
    if not key or not available:
        return []
    return difflib.get_close_matches(key, available, n=_SUGGEST_MAX, cutoff=_SUGGEST_CUTOFF)


def _describe_object(obj: Any) -> str:
    """One-line inventory entry: ``key (type, label)`` — prose, never JSON.

    Must not produce anything that parses as JSON: the ``ToolResult.output``
    validation gate rejects string fields that parse back as a dict/list.
    """
    key = str(getattr(obj, "key", "") or "")
    # str()-coerce everything: this runs on an ERROR path and must never be the
    # thing that raises. A non-str `type`/`label` (any object with a .value)
    # previously turned a clean context_not_attached into an `execution` error.
    type_ = str(getattr(getattr(obj, "type", None), "value", "") or "")
    label = str(getattr(obj, "label", "") or "")
    bits = [b for b in (type_, label if label and label != key else "") if b]
    return f"{key} ({', '.join(bits)})" if bits else key


def _render_inventory(objects: list[Any]) -> str:
    """The full set of keys actually available this turn, as readable prose."""
    if not objects:
        return "NONE — no context objects are attached to this turn at all."
    entries = [_describe_object(o) for o in objects[:_INVENTORY_MAX]]
    more = len(objects) - len(entries)
    if more > 0:
        entries.append(f"...and {more} more")
    return "; ".join(entries)


def _slice_value(obj: Any, content_str: str, slice_content: str) -> Any:
    """Return the native dict/list when a 'slice' actually covers the whole value.

    ``mode='full'`` already returns native containers. ``page`` / ``summary``
    assumed a character slice could never parse back as JSON — false whenever
    the object is a small dict/list and the window covers all of it (the default
    window is 4000 chars, so this is the COMMON case, not an edge case). The
    ``ToolResult.output`` gate then rejects the result as a stringified dict and
    the whole call fails: 4 live ``matrx_validation_gate`` FAILs on ``context``.
    """
    raw = getattr(obj, "content", None)
    if isinstance(raw, dict | list) and slice_content == content_str:
        return raw
    return slice_content


def _materialized_slice_value(slice_: Any) -> Any:
    """Return native JSON when a lazy-source slice contains the whole value.

    Source resolvers expose text because partial reads are character-paged. A
    complete JSON object/array is different: leaving it as text trips the same
    ``ToolResult.output`` validation gate that protects inline context values.
    Only complete, zero-offset slices are decoded; partial pages remain text.
    """
    text = slice_.text
    if slice_.offset != 0 or slice_.has_more:
        return text
    try:
        value = json.loads(text)
    except (TypeError, ValueError):
        return text
    return value if isinstance(value, dict | list) else text


def _log_key_alias_coercion(requested: str, resolved: str, ctx: ToolContext) -> None:
    """Record an alias reconciliation to BOTH trace sinks as ``COERCED``.

    Mirrors what ``ToolExecutor`` does for arg-shape coercion. Reconciling
    silently would hide a real signal — that a surface and its agent disagree
    about how a context key is spelled.
    """
    try:
        from matrx_utils import detached_task, vcprint

        from matrx_ai.tools._db_log import db_log_event
        from matrx_ai.tools._debug_log import log_event

        conversation_id = getattr(ctx, "conversation_id", None)
        vcprint(
            f"[context] COERCED: key {requested!r} is not a manifest key, but "
            f"normalizes to exactly one attached key {resolved!r} — resolved it.",
            color="yellow",
        )
        log_event(
            "COERCED",
            tool="context",
            fields=f"key:{requested}->{resolved}",
            conv=(conversation_id or "")[:8],
            call=ctx.call_id,
        )
        detached_task(
            db_log_event(
                "COERCED",
                tool_name="context",
                kind="SERVER",
                args={"key": requested},
                conversation_id=conversation_id,
                call_id=ctx.call_id,
                user_id=getattr(ctx, "user_id", None),
                metadata={"coerced_key": {"from": requested, "to": resolved}},
            ),
            name="tool_db_log_coerced_context_key",
        )
    except Exception:
        # Telemetry must never break a reconciliation that already succeeded.
        pass


def _document_source_continuation(obj: Any) -> dict[str, Any]:
    """Expose the processed-document drill-down beside every context read."""
    source = getattr(obj, "source", None)
    if source is None or getattr(source, "kind", None) != "processed_document":
        return {}
    document_id = getattr(source, "id", None)
    if not document_id:
        return {}

    from matrx_ai.tools.document_validation import PHYSICAL_PAGE_VALIDATION_GUIDANCE

    return {
        "processed_document_id": str(document_id),
        "document_tools": {
            "search": {
                "tool": "document_search",
                "arguments": {
                    "scope": "this_doc",
                    "document_id": str(document_id),
                },
            },
            "content": {
                "tool": "document_content",
                "arguments": {"document_id": str(document_id)},
            },
        },
        "physical_page_validation": PHYSICAL_PAGE_VALIDATION_GUIDANCE,
    }


def _pd_id_from_attached_document_key(key: str) -> str | None:
    """Extract the processed-document id from an ``attached_document_<pd_id>``
    key (the shape the frontend + ``seed_conversation_attachments`` use). Returns
    None for any other key shape."""
    if key.startswith(_ATTACHED_DOCUMENT_KEY_PREFIX):
        suffix = key[len(_ATTACHED_DOCUMENT_KEY_PREFIX) :]
        return suffix or None
    return None


async def _known_missing_key_result(
    key: str,
    available_objects: list[Any],
    app_ctx: Any,
    get_ext: Any,
    has_ext: Any,
) -> ToolResult:
    """Turn a KNOWN-BUT-MISSING context key into precise, actionable guidance
    instead of a dead-end ``not_found``.

    An intelligent agent that asks for ``attached_document_<id>`` (e.g. the user
    detached the doc, or it was attached on a prior turn) used to get a bare
    "no context objects are available" and then burned repeated failing calls.
    We KNOW such a doc existed — every attached pointer is durably stamped to
    ``cx_message.model_context``. Two tiers:

    - CHEAP (no DB): parse the pd id from the key and tell the agent to ask the
      user to re-attach, or read it directly with ``document_content(...)`` —
      putting the id right in the message + suggested_action.
    - CONFIRM (one scoped, bounded DB read via the injected
      ``lookup_prior_attached_document`` ext): if a prior turn stamped this doc,
      name it. Best-effort — any failure degrades to the cheap tier, never
      breaks the tool.

    Any other well-formed key gets the FULL inventory of what IS attached, the
    closest-named candidates, and an explicit do-not-retry — the three things a
    model needs to stop guessing. The dominant production failure was a model
    pattern-completing a plausible key that does not exist (asking for
    ``bundle_members`` when the turn carries ``bundle_member_count``), then
    burning another paid turn on the same guess.
    """
    available = [str(getattr(o, "key", "") or "") for o in available_objects]
    pd_id = _pd_id_from_attached_document_key(key)

    if pd_id is not None:
        label = "the document"
        confirmed = False
        conversation_id = getattr(app_ctx, "conversation_id", None)
        if conversation_id and has_ext("lookup_prior_attached_document"):
            try:
                lookup = get_ext("lookup_prior_attached_document")
                prior = await lookup(conversation_id, key)
            except Exception:
                prior = None
            if prior:
                confirmed = True
                pd_id = prior.get("pd_id") or pd_id
                label = prior.get("label") or label

        if confirmed:
            message = (
                f"Document '{label}' (id {pd_id}) was attached to this "
                f"conversation on an earlier turn but is not attached now — "
                f"ask the user to re-attach it, or read it directly with "
                f"document_content(document_id='{pd_id}')."
            )
        else:
            message = (
                f"'{key}' is not attached to the current turn. If it was an "
                f"attached document, it may have been detached or was attached "
                f"on an earlier turn — ask the user to re-attach it. If you "
                f"know the document_id, you can still read it directly with "
                f"document_content(action='read', document_id='{pd_id}')."
            )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="context_not_attached",
                message=message,
                is_retryable=False,
                suggested_action=(
                    f"Read it directly: document_content(action='read', "
                    f"document_id='{pd_id}', format='clean'), or ask the user to "
                    f"re-attach it. "
                    f"Do NOT retry this context key. "
                    f"Currently attached keys: {available}."
                ),
            ),
        )

    # Generic well-formed key: not attached THIS turn. Give the model the whole
    # inventory + the closest names + an unambiguous stop. A bare "not attached"
    # is what produced the repeat-the-same-guess traces.
    inventory = _render_inventory(available_objects)
    suggestions = _did_you_mean(key, available)

    message = (
        f"'{key}' is not a context key on this turn — it does not exist "
        f"(this is not a timing problem; nothing will attach it later). "
        f"Keys available right now: {inventory}."
    )
    if suggestions:
        message += (
            f" Closest existing names: {', '.join(suggestions)}. These are "
            f"SIMILAR names, not the same object — read one only if it is "
            f"actually what you need."
        )

    return ToolResult(
        success=False,
        error=ToolError(
            error_type="context_not_attached",
            message=message,
            is_retryable=False,
            suggested_action=(
                f"Do NOT call context again with '{key}' — the answer will not "
                f"change this turn. Either pick a key from the list above, or "
                f"get the information another way (another tool, or ask the "
                f"user). If you believe the data should be here, say so in your "
                f"reply instead of retrying."
            ),
        ),
    )


async def ctx_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Retrieve deferred context content by key.

    Thin wrapper over ``_ctx_get_body`` that surfaces any key reconciliation to
    the MODEL as an ``arg_coercion_notice`` on the output, so it learns the real
    key name instead of just getting away with the alias (same contract the
    executor uses for arg-shape coercion — see ARG_RECOVERY.md).
    """
    notices: list[str] = []
    result = await _ctx_get_body(args, ctx, notices)
    if notices and result.success and isinstance(result.output, dict):
        result.output.setdefault("arg_coercion_notice", notices[0])
    return _stamp_context_kind(result)


def _stamp_context_kind(result: ToolResult) -> ToolResult:
    """Validate a successful context payload through the declared union kind.

    The result-kind funnel for the ``context`` dispatcher (KIND_TOOL_LEDGER,
    the cms ``stamp_result_kind`` pattern): every success branch of
    get / batch / create speaks ONE declared kind, ``context_tool_result``.
    Loud-not-fatal — a payload the model refuses is screamed about and
    returned unstamped, so the executor's declared-kind enforcement records
    the miss instead of the call failing. No success gate: a partial-failure
    batch still carries the union payload, and failure paths have no output.
    """
    from matrx_ai.tools.kinds.context_tools import ContextToolResult, ContextWriteResult

    output = result.output
    if isinstance(output, ContextToolResult):
        return result
    if isinstance(output, ContextWriteResult):
        # The create branch rides the shared _create_from_patch funnel, which
        # returns context_write_result for context_patch and the widget_*
        # tools; the `context` dispatcher re-wraps it into its own union kind.
        output = output.model_dump(mode="json", by_alias=False, exclude={"kind_"})
    if not isinstance(output, dict):
        return result
    try:
        # VALIDATED WITH ITS MARKER ON. ``ContextToolResult`` is a KindModel:
        # ``__kind`` is a DECLARED field (alias of ``kind_``, populate_by_name),
        # so a payload that already says what it is validates natively and a
        # payload carrying someone ELSE's marker is a real mismatch that must
        # be screamed about, not silently laundered. Filtering the key here was
        # a reduction outside the three lawful doors (KINDS_EVERYWHERE_PLAN
        # §4.2a) — the marker is part of the data.
        result.output = ContextToolResult.model_validate(output)
    except ValidationError:
        logger.error(
            "[Content IR] context result refused by context_tool_result — "
            "returning the raw payload unstamped (fix the union or the branch)",
            exc_info=True,
        )
    return result


async def _ctx_get_body(args: dict[str, Any], ctx: ToolContext, notices: list[str]) -> ToolResult:
    """Internal impl for the ``context`` dispatcher's ``get`` action. The
    dispatcher validates the incoming call against ``ContextArgs`` before
    routing here, so this body trusts ``args`` is already shape-checked.
    """
    try:
        from matrx_ai._ext import get_ext, has_ext
        from matrx_ai.context.app_context import get_app_context

        load_manifest_from_ctx = get_ext("load_manifest_from_ctx")

        key: str = args.get("key", "")
        mode: str = args.get("mode", "full")
        offset: int = int(args.get("offset", 0))
        chars: int = int(args.get("chars", _DEFAULT_PAGE_CHARS))

        # --- validate key ---
        if not key:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message="key is required.",
                    suggested_action="Provide the key of the context object to retrieve.",
                ),
            )

        # --- validate mode ---
        if mode not in _VALID_MODES:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Invalid mode '{mode}'.",
                    suggested_action=f"Use one of: {sorted(_VALID_MODES)}",
                ),
            )

        # --- load manifest ---
        app_ctx = get_app_context()
        manifest = load_manifest_from_ctx(app_ctx)

        # KNOWN-BUT-MISSING responder — a requested key that isn't in the
        # current turn's manifest is NOT a dead end. When it's an attached-
        # document key (or any well-formed key) we return precise, actionable
        # guidance (re-attach / read directly with document_content) instead of
        # a bare not_found the agent retries into oblivion. See
        # _known_missing_key_result.
        if manifest is None:
            return await _known_missing_key_result(key, [], app_ctx, get_ext, has_ext)

        obj = manifest.get(key)
        if obj is None:
            # RECONCILE BEFORE REJECTING. A key that normalizes to exactly one
            # attached key is the same key spelled differently — there is
            # exactly one thing the caller can mean, so resolve it and log
            # COERCED rather than burning the caller's turn on a spelling.
            available_objects = list(manifest.all())
            available = [str(getattr(o, "key", "") or "") for o in available_objects]
            resolved, ambiguous = _resolve_key_alias(key, available)
            if resolved is not None:
                obj = manifest.get(resolved)
            if obj is not None and resolved is not None:
                _log_key_alias_coercion(key, resolved, ctx)
                notices.append(
                    f"NOTICE: no context key is named '{key}'; it matched the "
                    f"attached key '{resolved}' on spelling alone and was "
                    f"resolved for you. Use '{resolved}' exactly, next call."
                )
                key = resolved
            elif ambiguous:
                # More than one candidate — never guess. Name them all.
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="validation",
                        message=(
                            f"'{key}' matches more than one attached context "
                            f"key by spelling: {', '.join(ambiguous)}. Pick the "
                            f"exact one you want."
                        ),
                        is_retryable=False,
                        suggested_action=(
                            f"Call context again with key set to exactly one of: "
                            f"{', '.join(ambiguous)}."
                        ),
                    ),
                )
            else:
                return await _known_missing_key_result(
                    key, available_objects, app_ctx, get_ext, has_ext
                )

        # --- lazy source-backed object: resolve the body ON DEMAND ---------
        # An attached document (and any future lazy source) ships as a pointer,
        # not content — the body is never carried with the request. Resolve the
        # requested slice now via the host-injected materializer; the resolver
        # caps what it returns, so this is bounded (output_self_capped).
        if obj.is_lazy_source() and obj.source is not None:
            # mode=summary NEVER hard-fails. For a source-backed object the
            # precomputed descriptor.summary (ToC + size + alternates) IS the
            # summary — free, already in the manifest. Fall back to first page
            # only when the descriptor is missing.
            if mode == "summary":
                desc = obj.descriptor
                if desc is not None and desc.summary:
                    return ToolResult(
                        success=True,
                        output={
                            "key": key,
                            "type": obj.type.value,
                            "label": obj.label,
                            "mode": "summary",
                            "summary_kind": "descriptor",
                            "summary": desc.summary,
                            "total_chars": desc.primary_size_chars,
                            "note": (
                                "mode='summary' for this source-backed object "
                                "returns the precomputed descriptor (ToC + size "
                                "+ alternates), not an AI rewrite. Use "
                                "mode='page'/'full' for body text; "
                                "document_content for other representations."
                            ),
                            **_document_source_continuation(obj),
                        },
                        output_self_capped=True,
                    )
                mode = "page"
                # fall through to materialize the first page
            elif mode not in ("full", "page"):
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="validation",
                        message=(
                            f"mode '{mode}' is not valid for '{key}' "
                            f"(a source-backed object). Valid modes: "
                            f"full, page, summary."
                        ),
                        suggested_action=(
                            "Use mode='full' or mode='page' for body text; "
                            "mode='summary' returns the precomputed descriptor."
                        ),
                    ),
                )

            materialize = (
                get_ext("materialize_context_source")
                if has_ext("materialize_context_source")
                else None
            )
            if materialize is None:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="execution",
                        message="Source materialization is not available in this environment.",
                        suggested_action="This deployment cannot resolve source-backed context objects.",
                    ),
                )
            page_offset = offset if (mode == "page" and offset > 0) else 0
            page_chars = chars if (mode == "page" and chars > 0) else None
            slice_ = await materialize(
                obj.source,
                mode=mode,
                offset=page_offset,
                chars=page_chars,
                user_id=getattr(app_ctx, "user_id", None) or "",
            )
            if slice_ is None:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="not_found",
                        message=f"No resolver is registered for the source of '{key}'.",
                    ),
                )
            output: dict[str, Any] = {
                "key": key,
                "type": obj.type.value,
                "label": obj.label,
                "representation": slice_.representation,
                "content": _materialized_slice_value(slice_),
                "offset": slice_.offset,
                "chars_returned": len(slice_.text),
                "total_chars": slice_.total_chars,
                "has_more": slice_.has_more,
                "next_offset": slice_.next_offset,
                **_document_source_continuation(obj),
            }
            if slice_.page_range:
                output["page_range"] = slice_.page_range
            if args.get("mode") == "summary":
                output["mode"] = "page"
                output["fell_back_from"] = "summary"
                output["note"] = (
                    "No descriptor summary was available; returned the first "
                    "page of content instead. Prefer mode='page' explicitly."
                )
            return ToolResult(success=True, output=output, output_self_capped=True)

        content_str = obj.content_as_str()

        # --- full mode ---
        if mode == "full":
            # When the underlying content is a native dict or list (every
            # ContextObjectType.{json,user,org,workspace,project,task} slot,
            # which is the common case), return it as-is instead of round-
            # tripping through a JSON string. Two reasons:
            #   1. The ToolResult.output validator (models.py) flags any
            #      string field that parses back as a dict/list — that's
            #      the str()-ed-envelope antipattern it's defending against.
            #      A full-content JSON string trips it every time.
            #   2. The model serializes tool results to JSON anyway when
            #      handing them to the provider; passing native saves one
            #      escape layer and is what the validator's docstring
            #      explicitly asks for ("Return the native object instead").
            # mode='page' keeps returning a sliced string — slicing is
            # character-level and partial slices won't parse, so they pass
            # the validator cleanly.
            raw = obj.content
            content_value: Any = raw if isinstance(raw, dict | list) else content_str
            return ToolResult(
                success=True,
                output={
                    "key": key,
                    "type": obj.type.value,
                    "label": obj.label,
                    "content": content_value,
                    "total_chars": len(content_str),
                    **_document_source_continuation(obj),
                },
            )

        # --- page mode ---
        if mode == "page":
            if offset < 0:
                offset = 0
            if chars <= 0:
                chars = _DEFAULT_PAGE_CHARS
            slice_content = content_str[offset : offset + chars]
            total = len(content_str)
            has_more = (offset + chars) < total
            next_offset = offset + chars if has_more else None
            return ToolResult(
                success=True,
                output={
                    "key": key,
                    "type": obj.type.value,
                    "label": obj.label,
                    "content": _slice_value(obj, content_str, slice_content),
                    "offset": offset,
                    "chars_returned": len(slice_content),
                    "total_chars": total,
                    "has_more": has_more,
                    "next_offset": next_offset,
                    **_document_source_continuation(obj),
                },
            )

        # --- summary mode ---
        # Always succeeds. Prefer the configured AI summary agent; otherwise
        # fall back to the first page so the model still gets content (a
        # rejected summary call wastes a paid turn for nothing).
        if mode == "summary":
            if obj.summary_agent_id:
                summary = await _run_summary_agent(
                    agent_id=obj.summary_agent_id,
                    content=content_str,
                    ctx=ctx,
                )
                return ToolResult(
                    success=True,
                    output={
                        "key": key,
                        "type": obj.type.value,
                        "label": obj.label,
                        "mode": "summary",
                        "summary_kind": "agent",
                        "summary": summary,
                        "total_chars": len(content_str),
                        **_document_source_continuation(obj),
                    },
                )
            if chars <= 0:
                chars = _DEFAULT_PAGE_CHARS
            slice_content = content_str[0:chars]
            total = len(content_str)
            has_more = chars < total
            return ToolResult(
                success=True,
                output={
                    "key": key,
                    "type": obj.type.value,
                    "label": obj.label,
                    "mode": "page",
                    "fell_back_from": "summary",
                    "content": _slice_value(obj, content_str, slice_content),
                    "offset": 0,
                    "chars_returned": len(slice_content),
                    "total_chars": total,
                    "has_more": has_more,
                    "next_offset": chars if has_more else None,
                    "note": (
                        "No summary agent is configured for this object; "
                        "returned the first page instead. Use mode='full' or "
                        "mode='page' explicitly, or configure summary_agent_id "
                        "on the slot for an AI summary."
                    ),
                    **_document_source_continuation(obj),
                },
            )

        # unreachable — kept for safety
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=f"Unhandled mode: {mode}"),
        )

    except Exception as e:
        # Unwrap the MATRX validation gate so the stream emitter shows the
        # short clean message (the gate already printed a full red banner
        # to stdout). No traceback for a gate trip — we ARE the cause.
        gate_msg = _extract_gate_message(e)
        if gate_msg is not None:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="matrx_validation_gate",
                    message=gate_msg,
                    is_retryable=False,
                    suggested_action=(
                        "Read the red banner in the server stdout / logs — "
                        "it names the offending field and how to fix it."
                    ),
                ),
            )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"ctx_get failed: {e}",
                traceback=traceback.format_exc(),
                is_retryable=False,
            ),
        )


def _extract_gate_message(exc: BaseException) -> str | None:
    """If exc is (or wraps) a ToolOutputContractError, return its clean
    message. Otherwise None. Pydantic wraps validator errors in
    ValidationError, so we have to walk .__cause__ / .errors() to find it."""
    if isinstance(exc, ToolOutputContractError):
        return str(exc)
    cause = getattr(exc, "__cause__", None)
    if isinstance(cause, ToolOutputContractError):
        return str(cause)
    errors_fn = getattr(exc, "errors", None)
    if callable(errors_fn):
        try:
            for err in errors_fn():
                inner = (err or {}).get("ctx", {}).get("error")
                if isinstance(inner, ToolOutputContractError):
                    return str(inner)
        except Exception:
            pass
    return None


async def _run_summary_agent(
    agent_id: str,
    content: str,
    ctx: ToolContext,
) -> str:
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import run_agent

    try:
        agent = await Agent.from_prompt(agent_id)
        agent.set_variable("content", content)
        result = await run_agent(
            agent,
            label=f"summary:{agent_id}",
            source_feature="context_summary",
        )
        if not result.success:
            return f"[Summary failed: {result.error}]"
        return result.output
    except Exception as e:
        return f"[Summary failed: {e}]"


async def ctx_batch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Run up to 20 ctx_get calls in one round trip.

    Internal impl for the ``context`` dispatcher's ``batch`` action.
    """
    try:
        requests = args.get("requests")
        stop_on_error = bool(args.get("stop_on_error", False))

        if not isinstance(requests, list) or not requests:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message="requests must be a non-empty list of {key, mode?, offset?, chars?} objects.",
                    suggested_action=(
                        'Example: {"requests":[{"key":"active_file"},'
                        '{"key":"user_profile","mode":"summary"}]}'
                    ),
                ),
            )
        if len(requests) > _BATCH_MAX:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Batch size {len(requests)} exceeds the limit of {_BATCH_MAX}.",
                    suggested_action=f"Split into chunks of {_BATCH_MAX} or fewer.",
                ),
            )

        results: list[dict[str, Any]] = []
        any_failed = False
        for i, sub in enumerate(requests):
            if not isinstance(sub, dict):
                any_failed = True
                results.append(
                    {
                        "key": None,
                        "success": False,
                        "error": {
                            "error_type": "validation",
                            "message": f"requests[{i}] is not an object.",
                        },
                    }
                )
                if stop_on_error:
                    break
                continue

            sub_result = await ctx_get(sub, ctx)
            entry: dict[str, Any] = {
                "key": sub.get("key"),
                "success": sub_result.success,
            }
            if sub_result.success:
                # ctx_get returns the ContextToolResult model; nest its wire
                # form (marker included — it IS an instance of that kind).
                from pydantic import BaseModel

                entry["output"] = (
                    sub_result.output.model_dump(mode="json")
                    if isinstance(sub_result.output, BaseModel)
                    else sub_result.output
                )
            else:
                any_failed = True
                entry["error"] = (
                    sub_result.error.model_dump(exclude_none=True)
                    if sub_result.error
                    else {"error_type": "execution", "message": "ctx_get failed."}
                )
            results.append(entry)
            if stop_on_error and not sub_result.success:
                break

        top_error: ToolError | None = None
        if any_failed:
            failed_summaries: list[str] = []
            for r in results:
                if r.get("success"):
                    continue
                err = r.get("error") or {}
                failed_summaries.append(
                    f"  - key={r.get('key')!r}: "
                    f"[{err.get('error_type', 'unknown')}] "
                    f"{err.get('message', 'no message')}"
                )
            any_succeeded = any(r.get("success") for r in results)
            # Every sub-failure being a missing key means retrying the batch
            # cannot help — the keys do not exist this turn. Saying "retry the
            # failed keys" (the old text) is what kept the model looping.
            all_missing = all(
                (r.get("error") or {}).get("error_type") == "context_not_attached"
                for r in results
                if not r.get("success")
            )
            top_error = ToolError(
                # Preserve the actionable domain refusal at the executor
                # boundary. Renaming an all-missing batch to batch_*_failed
                # made the executor treat the expected absence as an
                # operational failure and emit ERROR + system_error records.
                error_type=(
                    "context_not_attached"
                    if all_missing
                    else ("batch_partial_failure" if any_succeeded else "batch_all_failed")
                ),
                message=(
                    f"{len(failed_summaries)} of {len(results)} ctx_batch "
                    f"sub-request(s) failed:\n" + "\n".join(failed_summaries)
                ),
                suggested_action=(
                    (
                        "Those keys do not exist on this turn. Do NOT retry "
                        "them — the result will be identical. Use the keys "
                        "named in each sub-error's message, or proceed with "
                        "the sub-requests that succeeded."
                    )
                    if all_missing
                    else (
                        "Inspect output.results[] for per-key error details. "
                        "Retry only the failed keys that are retryable, and "
                        "never re-send a key reported as not attached."
                    )
                ),
                is_retryable=False,
            )

        return _stamp_context_kind(
            ToolResult(
                success=not any_failed,
                output={
                    "count": len(results),
                    "requested": len(requests),
                    "results": results,
                },
                error=top_error,
            )
        )

    except Exception as e:
        gate_msg = _extract_gate_message(e)
        if gate_msg is not None:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="matrx_validation_gate",
                    message=gate_msg,
                    is_retryable=False,
                    suggested_action=(
                        "Read the red banner in the server stdout / logs — "
                        "it names the offending field and how to fix it."
                    ),
                ),
            )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"ctx_batch failed: {e}",
                traceback=traceback.format_exc(),
                is_retryable=False,
            ),
        )


# ---------------------------------------------------------------------------
# context — the unified action-dispatched tool (get | batch | create)
# ---------------------------------------------------------------------------


def _context_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "context"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _context_validation_error(
    message: str,
    started_at: float,
    ctx: ToolContext,
    *,
    error_type: str = "validation",
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type=error_type, message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="context",
        call_id=ctx.call_id,
    )


def _context_create_allowed() -> bool:
    """Honor the request's ``allow_context_create`` gate at runtime.

    ``apply_context_objects`` stamps ``allow_context_create`` onto the
    AppContext metadata when it injects the ``context`` tool. The ``create``
    action is always present in the tool schema, so this is the single runtime
    gate that preserves the legacy behavior — creation is off unless the caller
    explicitly opted in (the old code achieved this by only injecting the
    separate ``ctx_create`` tool when allowed).
    """
    try:
        from matrx_ai.context.app_context import get_app_context

        app_ctx = get_app_context()
        return bool((getattr(app_ctx, "metadata", None) or {}).get("allow_context_create", False))
    except Exception:
        return False


async def context(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Unified deferred-context tool. Dispatches on ``action``:

    - ``get``    → fetch one object by key (modes full / page / summary)
    - ``batch``  → fetch up to 20 objects in one round trip
    - ``create`` → add a new object (gated by ``allow_context_create``)

    Mutating an existing object is the separate ``context_patch`` tool — kept
    apart so the model commits to one edit vocabulary at a time and so the
    ``command`` patch dispatcher never nests under this ``action`` dispatcher.
    """
    started_at = time.time()
    inference = infer_missing_discriminator(args, ContextArgs)
    if inference.kind == "inferred" and inference.args is not None:
        args = inference.args
    elif inference.kind in ("ambiguous", "uninferable") and inference.error:
        return _context_validation_error(inference.error, started_at, ctx)

    try:
        parsed = ContextArgs.model_validate(args).root
    except ValidationError as exc:
        return _context_validation_error(format_args_error(exc), started_at, ctx)

    action = parsed.action
    inner_args = parsed.model_dump(exclude={"action"}, exclude_unset=True)

    if action == "get":
        return _context_stamp(await ctx_get(inner_args, ctx), started_at, ctx)
    if action == "batch":
        return _context_stamp(await ctx_batch(inner_args, ctx), started_at, ctx)

    # action == "create"
    if not _context_create_allowed():
        # ACTIONABLE FOR THE MODEL, not for the caller. The old message told the
        # model that "the caller must opt in (allow_context_create=true)" — an
        # instruction it cannot execute, so it retried the same call with
        # guessed extra args (production traces: the same key resent with
        # `overwrite_existing: true`). Tell it what IT can do, and to stop.
        return _context_validation_error(
            "This session cannot create context objects, and that will not "
            "change during this conversation — creating context is off for "
            "every turn here. Do NOT retry create with different arguments. "
            "You do not need a context object to remember a value: keep it in "
            "your reply, or pass it directly as an argument to the tool that "
            "consumes it. To READ what is attached use action='get' or "
            "action='batch'; to EDIT an existing mutable object use the "
            "context_patch tool.",
            started_at,
            ctx,
            error_type="context_create_disabled",
        )
    from matrx_ai.tools.implementations.ctx_write import ctx_create

    # Re-wrap the shared create funnel's context_write_result receipt into
    # this dispatcher's own union kind (one declared kind per tool).
    return _context_stamp(_stamp_context_kind(await ctx_create(inner_args, ctx)), started_at, ctx)
