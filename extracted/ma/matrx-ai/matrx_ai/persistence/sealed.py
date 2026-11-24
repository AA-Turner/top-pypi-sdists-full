"""Confidential ("sealed") runs: structure on our server, content on the person's devices.

Owner definition (Arman, 2026-10-15): a confidential conversation is NOT recorded on
our servers; we keep all of the metadata that gives the chat its structure, but the
messages sent and received, attachments and media never leave the person's devices
other than the request going back and forth.

A sealed run carries ``AppContext.sealed_conversation_id`` (set by a chat door after
the conversation gate created or verified that sealed row) and ``store=False`` (so
every derived-content job keyed on ``store`` skips exactly like an ephemeral run).
This module is the ONE place that decides what a row written under a sealed context
may carry. ``seal_payload`` runs at the top of the one write funnel
(``queue_helpers._queue_or_drop``), so a new caller cannot bypass it by writing
through the coordinator, and the database trigger
``chat.refuse_sealed_content`` is the second, independent layer for every other
writer.

``sealed_keeps_content`` is the organization knob
``chat.confidential.keep_content_on_server``: rows keep their content, the
conversation is still marked ``metadata.confidential = true``.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from matrx_utils import vcprint

logger = logging.getLogger(__name__)

#: The key the sidebar's Private bucket reads (``metadata->>'confidential'``).
CONFIDENTIAL_METADATA_KEY = "confidential"

#: The tables a sealed run writes STRUCTURE rows to. Every other table queued under a
#: sealed context (request snapshots, tool traces, observational memory, ...) is
#: dropped whole, loudly — content-derived tables have no structure-only form.
SEALED_STRUCTURE_TABLES: frozenset[str] = frozenset(
    {
        "chat.conversation",
        "chat.message",
        "chat.tool_call",
        "chat.request",
        "chat.user_request",
    }
)

# Column -> value written on an INSERT under a sealed context. On an UPDATE the
# column is removed instead (an UPDATE never needs to re-blank what was born blank,
# and some columns refuse a change once set — e.g. system_instruction).
_CONTENT_COLUMNS: dict[str, dict[str, Any]] = {
    "chat.conversation": {
        "title": None,
        "system_instruction": None,
        "description": None,
        "keywords": None,
        "variables": {},
        "overrides": {},
        "cache_state": None,
        "last_context_breakdown": None,
        "custom_fields": None,
        "host_value_names": None,
    },
    "chat.message": {
        "content": [],
        "content_history": None,
        "user_content": None,
        "model_context": None,
        "tools_on_call": None,
        "error": None,
        "voice": None,
        "custom_fields": None,
    },
    "chat.tool_call": {
        "arguments": {},
        "output": None,
        "output_preview": None,
        "execution_events": None,
        "file_path": None,
        "error_message": None,
        "value_ref_key": None,
        "custom_fields": None,
    },
    "chat.request": {
        "tool_calls_details": None,
        "trim_summary": None,
        "error": None,
        "custom_fields": None,
    },
    "chat.user_request": {
        "error": None,
        "custom_fields": None,
    },
}

# metadata keys that are structure (ids, counts, money, timing, routing), kept on a
# sealed row. Everything else in a metadata object is dropped — an allowlist, so a
# new content-bearing key is sealed by default.
_METADATA_KEEP: dict[str, frozenset[str]] = {
    "chat.conversation": frozenset({"mandate_key", "mandate_run", "direct_door", "run_configuration"}),
    "chat.message": frozenset({"provider_iteration", "finish_reason", "authored_by", "prefill",
                               "watchdog_reason", "watchdog_at", "watchdog_max_age_secs"}),
    "chat.tool_call": frozenset({"turn_actor_user_id", "parked_on", "watchdog_reason", "watchdog_at",
                                 "watchdog_max_age_secs"}),
    "chat.request": frozenset({
        "catalog_cost_usd", "cost_source", "pricing_snapshots", "pricing_snapshot", "offering_id",
        "offering_route", "response_message_id", "provider_charge", "provider_charge_usd",
        "provider_catalog_variance_usd", "provider_charge_available", "provider_charges",
        "billing_components", "provider_attempts", "builtin_tool_use",
        "original_model", "model_swap_reason", "model_swaps", "model_ceiling",
        "watchdog_reason", "watchdog_at", "watchdog_max_age_secs",
    }),
    "chat.user_request": frozenset({
        "usage_by_model", "ttft_ms", "response_id", "mandate_key", "mandate_resolution",
        "mandate_holder", "mandate_attribution", "agent_name", "initial_model",
        "runtime_execution_id", "runtime_root_execution_id", "runtime_lease_claim",
        "spine_run_claim_holder", "spine_claim_execution_id", "api_key_id", "api_key_kind",
        "api_key_name", "api_key_expires_at", "jwt_expires_at", "direct_door", "source_app",
        "source_feature", "cost_reconciliation", "known_cost_subtotal", "parent_request_id",
        "organization_admitted_by", "desktop_target_instance_id", "crash_recovery_attempt",
        "resumed_run_witness", "continued_run_witness", "original_model", "model_swap_reason",
        "watchdog_reason", "watchdog_at", "watchdog_max_age_secs",
    }),
}


def sealed_context(ctx: Any) -> bool:
    """True when ``ctx`` is a confidential run (content blanked or kept by the org knob)."""
    return bool(getattr(ctx, "sealed_conversation_id", None)) if ctx is not None else False


def blanks_content(ctx: Any) -> bool:
    """True when rows written under ``ctx`` must carry NO content."""
    return sealed_context(ctx) and not bool(getattr(ctx, "sealed_keeps_content", False))


def writes_sealed_structure(ctx: Any, conversation_id: Any = None) -> bool:
    """A sealed run writes its structure rows for ITS conversation only.

    A fork (sub-agent, held call) inherits ``sealed_conversation_id`` but runs on
    another conversation id; with ``store=False`` it writes nothing at all.
    """
    if not sealed_context(ctx):
        return False
    target = conversation_id if conversation_id is not None else getattr(ctx, "conversation_id", None)
    return bool(target) and str(target) == str(ctx.sealed_conversation_id)


#: A top-level metadata key whose value is an OBJECT is never kept whole: only its named
#: structure subkeys survive (a nested spec is itself a dict of allowed subkeys; ``True`` keeps
#: the subkey's value as is). Anything else inside — ``mandate_run.user_input``,
#: ``mandate_run.result`` (the structured answer), ``placement``, ``context`` — is dropped.
#: The database guard ``chat.refuse_sealed_content`` enforces the SAME spec
#: (its own copy of these specs). ``scripts/check_sealed_spec_matches_db.py`` compares the two live:
#: a key added here and not there makes the database refuse every sealed turn's final commit.
#: ``blocks_shadow.last_text_mismatch`` keys that are structure. Its ``stream_only_head`` and
#: ``response_only_head`` are slices of the reply itself, so a sealed row never carries them (W4 2026-11-04:
#: a ``{"*": True}`` here kept them, and the database guard, missing ``text_mismatch_causes``, refused every
#: sealed turn's final commit since 9cab9145).
LAST_TEXT_MISMATCH_STRUCTURE: tuple[str, ...] = (
    "cause", "stream_chars", "response_chars", "response_text_parts", "stream_has_reasoning_tag",
    "common_prefix_chars", "common_suffix_chars", "stream_only_chars", "response_only_chars",
)
_RESOLUTION_KEYS: dict[str, Any] = dict.fromkeys(
    ("door", "rung", "holder_id", "binding_id", "holder_name", "holder_type", "output_warned",
     "holder_version_id", "output_missing_keys", "holder_version_number"),
    True,
)
_PRICING_SNAPSHOT: dict[str, Any] = {
    **dict.fromkeys(
        ("cache_hit_price", "cache_write_1h_price", "cache_write_5m_price", "cached_input_price",
         "effective_from", "input_price", "max_tokens", "output_price", "usage_basis"),
        True,
    ),
    "component_prices": {"*": True},
}
_PROVIDER_CHARGE: dict[str, Any] = dict.fromkeys(
    ("amount_usd", "currency", "field_path", "is_final", "raw_amount", "raw_unit", "source"), True
)
_RUN_WITNESS: dict[str, Any] = dict.fromkeys(
    ("auth_type", "origin_class", "request_id", "route", "user_id"), True
)
#: Every allowed OBJECT is named down to its leaves; a leaf (``True``) holds only a scalar or a list
#: of scalars, never an object. ``"*"`` = any key name at that level (model names, catalog meter
#: names) with the named value shape; ``"[]"`` = each element of a list.
NESTED_METADATA_KEEP: dict[str, dict[str, Any]] = {
    "chat.conversation": {
        "mandate_run": {
            **dict.fromkeys(
                ("mandate_key", "door", "request_id", "model_id", "runtime_execution_id",
                 "success", "applet_id", "workflow_run_id"),
                True,
            ),
            "resolution": _RESOLUTION_KEYS,
        },
        "run_configuration": dict.fromkeys(
            ("outputKinds", "outputTypes", "added_skills", "added_tools", "added_mcp_servers",
             "auto_tools", "removed_tools", "surface_name", "search_types"),
            True,
        ),
    },
    "chat.user_request": {
        "mandate_resolution": _RESOLUTION_KEYS,
        # Blocks v1 shadow (CGU-14 P2): counts and microseconds only; ``last_error`` (free text) stays out.
        "blocks_shadow": {
            **dict.fromkeys(
                ("blocks_version", "calls", "tokens", "feed_us_total", "feed_us_worst_call_p99",
                 "feed_us_max", "oneshot_us", "validate_us", "text_mismatch", "block_divergence",
                 "divergence_unchecked", "shadow_errors"),
                True,
            ),
            "types": {"*": True},
            "kind_status": {"*": True},
            "text_mismatch_causes": {"*": True},
            # Counts and the cause name only: the two ``*_head`` keys are the reply's own words.
            "last_text_mismatch": dict.fromkeys(LAST_TEXT_MISMATCH_STRUCTURE, True),
        },
        "usage_by_model": {"*": dict.fromkeys(
            ("api", "cached_input_tokens", "cost", "input_tokens", "output_tokens", "request_count",
             "total_tokens"),
            True,
        )},
        "mandate_holder": dict.fromkeys(
            ("agent_id", "consumer", "held_call_id", "holder_type", "is_version", "mandate_key", "name"),
            True,
        ),
        "runtime_lease_claim": dict.fromkeys(("execution_id", "holder"), True),
        # Why a sealed turn got no skill offer / which chat mode it ran in (chat-agent-skills): the state and the
        # reason NAMED by the platform, never the offered list or its text (the offer never runs on a sealed turn).
        "skill_offer": dict.fromkeys(("state", "reason"), True),
        "chat_mode": dict.fromkeys(("mode", "reason", "provider", "core_block", "small_model"), True),
        "resumed_run_witness": _RUN_WITNESS,
        "continued_run_witness": _RUN_WITNESS,
    },
    "chat.request": {
        "pricing_snapshot": _PRICING_SNAPSHOT,
        "pricing_snapshots": {"[]": _PRICING_SNAPSHOT},
        "provider_charge": _PROVIDER_CHARGE,
        "provider_charges": {"[]": _PROVIDER_CHARGE},
        "billing_components": {"*": True},
        "provider_attempts": {"[]": dict.fromkeys(
            ("attempt", "cached_tokens", "catalog_cost_usd", "input_tokens", "model", "offering_id",
             "outcome", "output_tokens", "provider", "provider_model"),
            True,
        )},
        # Counts only: the search QUERIES and the fetched URLs are the person's content.
        "builtin_tool_use": {
            "web_search": {"count": True, "sources_cited": True},
            "url_context": {"count": True},
        },
    },
    # The prefill's TEXT is content; its switches are structure.
    "chat.message": {"prefill": dict.fromkeys(("forced", "mode", "starts_with_prefill"), True)},
    "chat.tool_call": {"parked_on": dict.fromkeys(("action_request_id", "kind"), True)},
}


def _scalar_leaf(value: Any) -> bool:
    if isinstance(value, dict):
        return False
    if isinstance(value, list):
        return all(not isinstance(v, (dict, list)) for v in value)
    return True


def keep_by_spec(value: Any, spec: Any) -> Any:
    """``value`` reduced to what ``spec`` names. ``True`` keeps a scalar (or a list of scalars),
    never an object; a dict spec recurses (``"*"`` = any key, ``"[]"`` = list elements)."""
    if spec is True:
        return value if _scalar_leaf(value) else None
    if not isinstance(spec, dict):
        return None
    if isinstance(value, list) and "[]" in spec:
        kept = [keep_by_spec(v, spec["[]"]) for v in value]
        return [v for v in kept if v is not None]
    if not isinstance(value, dict):
        return None
    out: dict[str, Any] = {}
    for key, sub_value in value.items():
        if key in ("*", "[]"):
            continue
        sub = spec.get(key, spec.get("*"))
        if sub is None:
            continue
        kept = keep_by_spec(sub_value, sub)
        if kept is not None:
            out[key] = kept
    return out


def sealed_metadata_spec(table: str) -> dict[str, Any]:
    """The full keep-spec of ``table``'s metadata (flat keys + nested objects)."""
    spec: dict[str, Any] = dict.fromkeys(_METADATA_KEEP.get(table, frozenset()), True)
    spec.update(NESTED_METADATA_KEEP.get(table, {}))
    return spec


def _keep_metadata(table: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return keep_by_spec(value, sealed_metadata_spec(table)) or {}


def seal_conversation_metadata(value: dict[str, Any]) -> dict[str, Any]:
    """A confidential conversation's metadata patch, structure only (for direct writers)."""
    out = _keep_metadata("chat.conversation", value)
    if "confidential" in value:
        out[CONFIDENTIAL_METADATA_KEY] = True
    return out


def seal_payload(table: str, payload: dict[str, Any], *, op_type: str, ctx: Any) -> dict[str, Any] | None:
    """The row a sealed context may write, or ``None`` to drop the write whole.

    Pure on its inputs; never logs a value (only table names and column names).
    """
    if not sealed_context(ctx):
        return payload
    blank = blanks_content(ctx)
    out = dict(payload)
    if table == "chat.conversation":
        # The confidential mark and the list-visibility facts ride every write,
        # content kept or not: the sidebar's Private bucket reads the mark.
        if op_type == "insert" or "metadata" in out:
            base = _keep_metadata(table, out.get("metadata")) if blank else dict(out.get("metadata") or {})
            out["metadata"] = {**base, CONFIDENTIAL_METADATA_KEY: True}
        if op_type == "insert" or "is_ephemeral" in out:
            out["is_ephemeral"] = False
        if op_type == "insert" or "exclude_from_kg" in out:
            out["exclude_from_kg"] = True
    if not blank:
        return out
    if table not in SEALED_STRUCTURE_TABLES:
        vcprint(
            f"[sealed] dropped a {op_type} on {table}: a confidential run writes no content-derived rows.",
            color="yellow",
        )
        return None
    for column, empty in _CONTENT_COLUMNS[table].items():
        if column not in out:
            if op_type == "insert" and empty is not None and column != "custom_fields":
                out[column] = empty
            continue
        if op_type == "insert":
            out[column] = empty
        else:
            out.pop(column)
    if table == "chat.conversation" and "config" in out:
        cfg = out["config"]
        # The model is structure (the list shows it); everything else in config is
        # the assembled prompt/tool belt.
        out["config"] = {"model": cfg["model"]} if isinstance(cfg, dict) and cfg.get("model") else {}
    if table != "chat.conversation" and "metadata" in out:
        out["metadata"] = {**_keep_metadata(table, out["metadata"]), "sealed": True}
    return out


_INLINE_KEYS = ("base64_data", "base64")

# ---------------------------------------------------------------------------
# A store that failed this turn is never tried again this turn, and a failed store never stops a
# row from being saved (CGU-10 AND-IMG14 #2, #4). The row keeps a marked stand-in where the file
# would have been (``unavailable_attachment_part``) and the failure is captured once.
# ---------------------------------------------------------------------------

#: The text a stand-in for a file that could not be stored shows (layout, not prose).
UNAVAILABLE_ATTACHMENT_TEXT = "Attachment not saved"
#: ``metadata`` key on that stand-in: what was lost, so a client can draw it and a script can count it.
#: Its one home is ``message_config`` (``content_text`` skips the stand-in: it is never words).
from matrx_ai.config.message_config import UNAVAILABLE_ATTACHMENT_KEY  # noqa: E402

_FAILED_CAP = 4096  # protocol-constant: memory bound on an in-process id set (cleared when full), not an admin behavior
#: file_id (minted, never written) → the error type that stopped its upload.
_FAILED_UPLOADS: dict[str, str] = {}
#: (request id, hash of the bytes) → the error type: an id-less inline part whose store failed in a
#: request is not uploaded again by a later save of the SAME request.
_FAILED_BLOBS: dict[tuple[str, str], str] = {}
#: file_id → the upload running beside the provider call (a person's attachment, its id minted first).
_IN_FLIGHT: dict[str, asyncio.Task[Any]] = {}
#: Every id THIS server minted for a person's attachment (bounded). Only these may be adopted by
#: another part carrying the same bytes — a client-supplied id never binds other content to a file
#: the client named (CGU-10 AND-IMG15 #3).
_MINTED: dict[str, None] = {}
_MINTED_CAP = 16384  # protocol-constant: memory bound on an in-process id set (cleared when full), not an admin behavior


def _remember_minted(file_id: str) -> None:
    _MINTED[file_id] = None
    while len(_MINTED) > _MINTED_CAP:
        _MINTED.pop(next(iter(_MINTED)))


def server_minted_attachment_id(file_id: Any) -> bool:
    """True when this server minted ``file_id`` for a person's attachment."""
    return bool(file_id) and str(file_id) in _MINTED


def _remember(store: dict[Any, str], key: Any, value: str) -> None:
    store[key] = value
    while len(store) > _FAILED_CAP:
        store.pop(next(iter(store)))


def _blob_key(blob: str, ctx: Any) -> tuple[str, str]:
    import hashlib

    request_id = str(getattr(ctx, "request_id", None) or "")
    return request_id, hashlib.sha256(blob.encode("utf-8", "surrogatepass")).hexdigest()


def unavailable_attachment_part(part: dict[str, Any], error_type: str) -> dict[str, Any]:
    """The stored stand-in for a media part whose file could not be stored: a text part that SAYS so,
    carrying what was lost in ``metadata``. Never a media part naming a file that does not exist."""
    lost = {
        "kind": part.get("kind") or part.get("media_type"),
        "mime_type": part.get("mime_type"),
        "reason": "store_failed",
        "error_type": error_type,
    }
    return {
        "type": "text",
        "text": UNAVAILABLE_ATTACHMENT_TEXT,
        "metadata": {UNAVAILABLE_ATTACHMENT_KEY: {k: v for k, v in lost.items() if v}},
    }


async def _capture_store_failure(exc: BaseException, *, where: str, payload: dict[str, Any] | None = None) -> None:
    logger.error("storing an inline attachment failed (%s): %r", where, exc, exc_info=exc)
    try:
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            exc,
            kind="person_inline_media_store_failed",
            route=where,
            error_type=type(exc).__name__,
            payload={"where": where, **(payload or {})},
        )
    except Exception:  # noqa: BLE001 — capture is best-effort; the ERROR log above stands
        pass


async def keep_inline_media_on_server(parts: list[dict[str, Any]] | None, ctx: Any = None, *, source: str | None = None) -> list[dict[str, Any]] | None:
    """Every media part a run SENT as inline bytes is stored like any upload (the files service,
    ``save_media_envelope_async``) and the saved part keeps its file_id and url. A stored media part
    must name a url or file_id (``_StoredMediaPartBase``), and inline bytes are stripped on save, so
    a part holding only bytes used to fail the whole message save AFTER the model answered (podcast
    extraction from a file URL, 2026-10-30: ``DocumentMediaPart requires 'url' or 'file_id'``).
    Internal callers build such parts (``_resolve_file_block``, face frames, any code that resolves
    a reference to bytes itself); a client upload already carries its file_id and passes untouched.

    A part that still names its source (url or file_id) is never uploaded again. A confidential
    chat whose organization blanks content stores nothing at all, so its parts return untouched.

    A part naming a person's attachment whose upload is still running (its id minted before the
    send) WAITS for it here — the row save is where the upload must have finished. A failed store
    (now, or earlier in this request) never stops the message from being saved: the part becomes
    the marked stand-in (``unavailable_attachment_part``), the failure is captured once, and the same
    bytes are not tried again in the same request (CGU-10 AND-IMG14 #2, #4).
    """
    if ctx is None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    if not parts or blanks_content(ctx):
        return parts
    if not any(_inline_only_media(p) or _names_a_pending_or_failed_upload(p) for p in parts):
        return parts
    out: list[dict[str, Any]] = []
    for part in parts:
        if _names_a_pending_or_failed_upload(part):
            out.append(await _settled_person_part(part))
            continue
        if not _inline_only_media(part):
            out.append(part)
            continue
        blob = next(part.get(k) for k in _INLINE_KEYS if part.get(k))
        mime = str(part.get("mime_type") or "application/octet-stream")
        key = _blob_key(blob, ctx)
        if key in _FAILED_BLOBS:
            out.append(unavailable_attachment_part(part, _FAILED_BLOBS[key]))
            continue
        try:
            saved = await _store_inline_blob(blob, mime, ctx, source=source)
        except Exception as exc:  # noqa: BLE001 — captured; the message is saved with a marked stand-in
            _remember(_FAILED_BLOBS, key, type(exc).__name__)
            await _capture_store_failure(exc, where="message_save", payload={"mime_type": mime})
            out.append(unavailable_attachment_part(part, type(exc).__name__))
            continue
        kept = {k: v for k, v in part.items() if k not in _INLINE_KEYS}
        kept.update({"origin": "matrx", "file_id": saved.file_id, "url": saved.url, "size_bytes": saved.size_bytes or part.get("size_bytes")})
        out.append(kept)
    return out


def _names_a_pending_or_failed_upload(part: Any) -> bool:
    if not isinstance(part, dict) or part.get("type") != "media":
        return False
    file_id = part.get("file_id")
    return bool(file_id) and (str(file_id) in _IN_FLIGHT or str(file_id) in _FAILED_UPLOADS)


async def _settled_person_part(part: dict[str, Any]) -> dict[str, Any]:
    """The part a row stores once its upload has finished: itself, or the marked stand-in."""
    file_id = str(part["file_id"])
    task = _IN_FLIGHT.get(file_id)
    if task is not None:
        try:
            await asyncio.shield(task)
        except Exception:  # noqa: BLE001 — the task captured and recorded its own failure
            pass
    if file_id in _FAILED_UPLOADS:
        return unavailable_attachment_part(part, _FAILED_UPLOADS[file_id])
    return part


async def settle_person_media_uploads(file_ids: Any = None) -> None:
    """Wait for every running person-attachment upload (or only ``file_ids``). Never raises."""
    wanted = set(map(str, file_ids)) if file_ids is not None else set(_IN_FLIGHT)
    tasks = [t for fid, t in list(_IN_FLIGHT.items()) if fid in wanted]
    if tasks:
        await asyncio.gather(*(asyncio.shield(t) for t in tasks), return_exceptions=True)


def person_media_upload_in_flight(file_id: Any) -> bool:
    """True while a person's attachment with this (minted) id is still being stored — its bytes are
    only on the part, so nothing may fetch the file by id yet (``unified_client`` uses the bytes)."""
    return bool(file_id) and str(file_id) in _IN_FLIGHT


def person_media_upload_failed(file_id: Any) -> bool:
    return bool(file_id) and str(file_id) in _FAILED_UPLOADS


def upload_failure_type(file_id: Any) -> str:
    """The error type that stopped this attachment's upload (``""`` when it did not fail)."""
    return _FAILED_UPLOADS.get(str(file_id or ""), "")


def person_media_upload_task(file_id: Any) -> asyncio.Task[Any] | None:
    """The upload still running for this minted id, or ``None`` once it has finished."""
    return _IN_FLIGHT.get(str(file_id or "")) if file_id else None


async def _store_inline_blob(blob: str, mime: str, ctx: Any, *, source: str | None = None, file_id: str | None = None) -> Any:
    """Store one inline media blob like any upload; the saved envelope carries its file_id."""
    from matrx_ai.media.media_persistence import _ref_kind_and_feature, save_media_envelope_async

    if sealed_context(ctx):
        source = "confidential_inline_attachment"
    _kind, feature = _ref_kind_and_feature(mime)
    kwargs: dict[str, Any] = {"feature": feature, "extra_metadata": {"source": source or "inline_media_part"}}
    if file_id:
        kwargs["file_id"] = file_id
    return await save_media_envelope_async(blob, mime, **kwargs)


async def _upload_person_attachment(file_id: str, blob: str, mime: str, ctx: Any, *, source: str | None = None) -> None:
    """The upload that runs beside the provider call. Success: the file exists under ``file_id``.
    Failure: recorded (``_FAILED_UPLOADS``) and captured once, here — no save tries it again."""
    try:
        saved = await _store_inline_blob(blob, mime, ctx, source=source, file_id=file_id)
        if str(getattr(saved, "file_id", None) or "") != file_id:
            raise RuntimeError(
                f"media persistence stored a person's attachment under {getattr(saved, 'file_id', None)!r}, "
                f"not the id its label already named ({file_id})"
            )
    except Exception as exc:  # noqa: BLE001 — recorded + captured; every save writes the stand-in
        _remember(_FAILED_UPLOADS, file_id, type(exc).__name__)
        await _capture_store_failure(exc, where="person_attachment_upload", payload={"file_id": file_id, "mime_type": mime})
    finally:
        _IN_FLIGHT.pop(file_id, None)


async def keep_inline_person_media_on_server(messages: Any, ctx: Any = None) -> int:
    """A person's media part that arrived as inline bytes only (a pasted or camera picture, a recorded
    clip, a dropped PDF) gets its ``file_id`` BEFORE the send, and its upload runs BESIDE the provider
    call — the bytes go inline to the provider anyway, so nothing before the first token waits on
    storage (CGU-10 AND-IMG14 #3; IMG13 measured +1.2 s for a 4 KB picture when it waited).

    Every media part of a person's message rides the wire behind an ``<attachment … id="…"/>`` label
    (``message_config._media_identity_label``) so the model can name the file it saw. The id is
    MINTED here and handed to the files service as the row id (``save_media_envelope_async(file_id=)``),
    so the label, the stored row and every later turn name the same file. Each distinct attachment
    is its own upload, all started side by side: one failing never touches another's id (IMG13
    finding #1 — a ``gather`` that threw away the good picture's id re-uploaded it twice more).
    Every row save waits for the upload (``keep_inline_media_on_server``); a failed one is saved as
    the marked stand-in, captured once, and never tried again in the turn.

    ONE UPLOAD PER PART PER TURN: the id is written onto the ONE part object every later step reads
    (the reservation, the send boundary, the end save), and the pristine ``user_content`` copy of the
    same bytes takes the SAME id (keyed by the bytes). A confidential chat whose organization blanks
    content and an unsaved run (``store: false``) store nothing. Returns how many uploads started."""
    if ctx is None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    if messages is None or blanks_content(ctx) or not stores_person_media(ctx):
        return 0
    import uuid

    from matrx_ai.providers.provider_io_capabilities import container_for_content

    ids_by_key: dict[tuple[str, str], str] = {}
    to_store: dict[tuple[str, str], str] = {}
    source_by_key: dict[tuple[str, str], str | None] = {}
    pending: list[tuple[Any, tuple[str, str]]] = []

    def _key(part: Any, blob: str) -> tuple[str, str]:
        return blob, str(getattr(part, "mime_type", None) or "application/octet-stream")

    for message in messages:
        role = str(getattr(getattr(message, "role", None), "value", getattr(message, "role", None)))
        # A person's turn, and an AUTHORED assistant turn a client sends as its own history (an
        # inline picture there is client-authored content, not the person's attachment — its file
        # says so: ``authored_inline_media``, CGU-10 AND-IMG14 #6). Either way: one id, one upload.
        if role not in ("user", "assistant"):
            continue
        source = None if role == "user" else "authored_inline_media"
        parts = [*(getattr(message, "content", None) or []), *(getattr(message, "user_content", None) or [])]
        for content in parts:
            blob = getattr(content, "base64_data", None)
            # Adopt ONLY an id this server minted (the same bytes already given one this request): a
            # part a client sent with bytes AND its own file_id keeps that id for itself, but never
            # lends it to other content (CGU-10 AND-IMG15 #3 — a row naming a file that is not theirs).
            if isinstance(blob, str) and blob and server_minted_attachment_id(getattr(content, "file_id", None)):
                ids_by_key.setdefault(_key(content, blob), str(content.file_id))
        for content in parts:
            blob = getattr(content, "base64_data", None)
            if not isinstance(blob, str) or not blob or not hasattr(content, "file_id"):
                continue
            if getattr(content, "file_id", None) or getattr(content, "url", None):
                continue
            if container_for_content(content) is None:
                continue
            key = _key(content, blob)
            pending.append((content, key))
            if key not in ids_by_key and key not in to_store:
                to_store[key] = str(uuid.uuid4())
                source_by_key[key] = source
    if not pending:
        return 0
    from matrx_utils import detached_task

    # Distinct attachments upload side by side, and none of them in front of the first token.
    for key, file_id in to_store.items():
        ids_by_key[key] = file_id
        _remember_minted(file_id)
        _IN_FLIGHT[file_id] = detached_task(
            _upload_person_attachment(file_id, key[0], key[1], ctx, source=source_by_key.get(key)),
            name=f"person_attachment_upload:{file_id}",
            carry_test_run=True,
        )
    for content, key in pending:
        content.file_id = ids_by_key[key]
    return len(to_store)


async def keep_inline_person_media_or_capture(messages: Any, ctx: Any = None, *, where: str) -> int | None:
    """:func:`keep_inline_person_media_on_server`, but nothing about it ever blocks the send: an
    unexpected failure to START the uploads is CAPTURED (``person_inline_media_store_failed``) and
    the part goes out as it arrived (its label's id empty). Returns how many uploads started;
    ``None`` when starting them FAILED (captured)."""
    try:
        return await keep_inline_person_media_on_server(messages, ctx)
    except Exception as exc:  # noqa: BLE001 — the send must stay available; captured below
        await _capture_store_failure(exc, where=where)
        return None


def stores_person_media(ctx: Any) -> bool:
    """A run that stores nothing (``store: false`` — an unsaved chat) stores none of the person's media
    either (CGU-10 AND-IMG13 #2): it writes no conversation, no message and no request row, so a file
    would be an orphan nobody chose to keep. The part goes out as it arrived and its label says
    ``id=""`` — there is no file to name."""
    return ctx is None or bool(getattr(ctx, "store", True))


def _inline_only_media(part: Any) -> bool:
    """A media part carrying inline bytes and no url or file_id: the one shape persistence refuses."""
    if not isinstance(part, dict) or part.get("type") != "media" or part.get("file_id") or part.get("url"):
        return False
    return any(isinstance(part.get(k), str) and part.get(k) for k in _INLINE_KEYS)


async def stored_message_content(
    parts: list[Any] | None, ctx: Any = None, *, settle: bool = True, source: str | None = None
) -> list[Any]:
    """The one funnel from a message's storage dict to the content a row stores: inline-only media is
    stored first (``keep_inline_media_on_server``), then every part is validated.

    ``settle=False`` is the RESERVATION's door only: it runs before the provider call, so it must not
    wait for a person's attachment upload running beside it. Its queued INSERT names the minted id;
    the turn's own save (mid-loop flush or ``persist_completed_request``) re-serializes the row with
    ``settle=True`` and its UPDATE — coalesced with that INSERT — carries the settled content.
    ``source`` names where an id-less inline part came from (default ``inline_media_part``)."""
    from matrx_ai.db.message_parts import validate_message_content

    parts = list(parts or [])
    if not settle:
        held = [p for p in parts if _names_a_pending_or_failed_upload(p)]
        if held:
            # Leave the running uploads alone: only already-FAILED ids become the stand-in now.
            parts = [
                unavailable_attachment_part(p, _FAILED_UPLOADS[str(p["file_id"])])
                if isinstance(p, dict) and str(p.get("file_id") or "") in _FAILED_UPLOADS
                else p
                for p in parts
            ]
            running = {i for i, p in enumerate(parts) if isinstance(p, dict) and str(p.get("file_id") or "") in _IN_FLIGHT}
            stored_rest = iter(await keep_inline_media_on_server([p for i, p in enumerate(parts) if i not in running], ctx, source=source) or [])
            parts = [p if i in running else next(stored_rest) for i, p in enumerate(parts)]
            return validate_message_content(parts)
    return validate_message_content(await keep_inline_media_on_server(parts, ctx, source=source) or [])
