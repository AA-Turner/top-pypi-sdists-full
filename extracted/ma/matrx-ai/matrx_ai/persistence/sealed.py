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

from typing import Any

from matrx_utils import vcprint

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
#: (``chat.sealed_metadata_spec``); a guard test pins the two together.
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


async def keep_inline_media_on_server(parts: list[dict[str, Any]] | None, ctx: Any = None) -> list[dict[str, Any]] | None:
    """Every media part a run SENT as inline bytes is stored like any upload (the files service,
    ``save_media_envelope_async``) and the saved part keeps its file_id and url. A stored media part
    must name a url or file_id (``_StoredMediaPartBase``), and inline bytes are stripped on save, so
    a part holding only bytes used to fail the whole message save AFTER the model answered (podcast
    extraction from a file URL, 2026-10-30: ``DocumentMediaPart requires 'url' or 'file_id'``).
    Internal callers build such parts (``_resolve_file_block``, face frames, any code that resolves
    a reference to bytes itself); a client upload already carries its file_id and passes untouched.

    A part that still names its source (url or file_id) is never uploaded again. A confidential
    chat whose organization blanks content stores nothing at all, so its parts return untouched.
    A failed upload raises: the message is not saved with a hole in it.
    """
    if ctx is None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    if not parts or blanks_content(ctx):
        return parts
    pending = [p for p in parts if _inline_only_media(p)]
    if not pending:
        return parts
    from matrx_ai.media.media_persistence import _ref_kind_and_feature, save_media_envelope_async

    source = "confidential_inline_attachment" if sealed_context(ctx) else "inline_media_part"
    out: list[dict[str, Any]] = []
    for part in parts:
        if not _inline_only_media(part):
            out.append(part)
            continue
        blob = next(part.get(k) for k in _INLINE_KEYS if part.get(k))
        mime = str(part.get("mime_type") or "application/octet-stream")
        _kind, feature = _ref_kind_and_feature(mime)
        saved = await save_media_envelope_async(blob, mime, feature=feature, extra_metadata={"source": source})
        kept = {k: v for k, v in part.items() if k not in _INLINE_KEYS}
        kept.update({"origin": "matrx", "file_id": saved.file_id, "url": saved.url, "size_bytes": saved.size_bytes or part.get("size_bytes")})
        out.append(kept)
    return out


def _inline_only_media(part: Any) -> bool:
    """A media part carrying inline bytes and no url or file_id: the one shape persistence refuses."""
    if not isinstance(part, dict) or part.get("type") != "media" or part.get("file_id") or part.get("url"):
        return False
    return any(isinstance(part.get(k), str) and part.get(k) for k in _INLINE_KEYS)


async def stored_message_content(parts: list[Any] | None, ctx: Any = None) -> list[Any]:
    """The one funnel from a message's storage dict to the content a row stores: inline-only media is
    stored first (``keep_inline_media_on_server``), then every part is validated."""
    from matrx_ai.db.message_parts import validate_message_content

    return validate_message_content(await keep_inline_media_on_server(list(parts or []), ctx) or [])
