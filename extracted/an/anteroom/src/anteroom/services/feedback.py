"""Feedback and bug reporting service.

Collects a redacted diagnostic bundle (version, config, system info,
spaces, packs, tools, optional conversation history) and dispatches it
to configured reporters (shell command or HTTP webhook).  Falls back to
writing a local JSON file when no reporters are configured.

Bundle payloads are delivered to command reporters via stdin (not env
vars) to avoid shell environment size limits and reduce accidental
exposure.
"""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import logging
import os
import platform
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger(__name__)

_SENSITIVE_SUBSTRINGS = ("key", "secret", "password", "token", "passphrase")
_DEFAULT_OMITTED = (
    "raw prompts and full conversation history unless explicitly requested",
    "raw tool arguments and outputs",
    "artifact content",
    "artifact metadata values",
    "pack source paths",
    "attachment filenames, storage paths, bytes, and extracted text",
    "configuration overlay values",
)

_TURN_DIAGNOSTIC_TOP_KEYS = {
    "version",
    "started_at",
    "ended_at",
    "total_duration_seconds",
    "stop_reason",
    "final_phase",
    "model",
    "usage",
    "retries",
    "phases",
    "tools",
    "active_tools",
    "runtime_events",
    "errors",
    "counters",
    "redaction",
}
_TURN_DIAGNOSTIC_ITEM_KEYS = {
    "retries": {
        "attempt",
        "max_attempts",
        "delay_seconds",
        "elapsed_seconds",
        "reason",
    },
    "phases": {
        "phase",
        "duration_seconds",
        "attempt",
        "max_attempts",
        "elapsed_seconds",
        "connect_elapsed_seconds",
        "first_response_elapsed_seconds",
        "timeout_seconds",
        "tool_count",
        "reason",
        "tool_names",
    },
    "tools": {
        "id",
        "name",
        "status",
        "duration_seconds",
        "argument_shape",
        "output_shape",
        "approval_decision",
        "hook_blocked",
    },
    "active_tools": {
        "id",
        "name",
        "status",
        "duration_seconds",
        "argument_shape",
    },
    "runtime_events": {
        "kind",
        "rules",
        "tool_name",
        "technique",
        "confidence",
        "action",
        "message",
        "tool_call_id",
        "reason",
        "estimated_tokens",
        "message_count",
        "tool_calls",
        "position",
        "queue_depth",
        "content_chars",
    },
    "errors": {"code", "message", "retryable"},
}
_TURN_DIAGNOSTIC_DICT_KEYS = {
    "model": {"provider", "name"},
    "usage": {"prompt_tokens", "completion_tokens", "total_tokens", "estimated", "model"},
    "counters": {"tokens", "token_chars", "assistant_chars"},
    "redaction": {"raw_tool_arguments", "raw_tool_output", "max_text_chars"},
}


def _redact_value(name: str, value: Any) -> Any:
    """Redact values whose field names suggest secrets."""
    name_lower = name.lower()
    if any(sub in name_lower for sub in _SENSITIVE_SUBSTRINGS):
        if isinstance(value, str) and value:
            return "****"
    return value


def _redact_dict(d: dict[str, Any]) -> dict[str, Any]:
    """Recursively redact sensitive keys in a dict."""
    out: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = _redact_dict(v)
        elif isinstance(v, list):
            out[k] = [_redact_dict(item) if isinstance(item, dict) else item for item in v]
        else:
            out[k] = _redact_value(k, v)
    return out


def _safe_text(value: Any, *, max_chars: int = 240) -> str:
    from .debug_diagnostics import sanitize_diagnostic_text

    return sanitize_diagnostic_text(value, max_chars=max_chars)


def _row_value(row: Any, key: str, index: int, default: Any = None) -> Any:
    if isinstance(row, dict):
        return row.get(key, default)
    try:
        return row[key]
    except (TypeError, KeyError, IndexError):
        try:
            return row[index]
        except (TypeError, IndexError):
            return default


def _db_fetchall(db: Any, sql: str, params: Sequence[Any] = ()) -> list[Any]:
    try:
        if hasattr(db, "execute_fetchall"):
            rows = db.execute_fetchall(sql, tuple(params))
            return list(rows or [])
        return list(db.execute(sql, tuple(params)).fetchall() or [])
    except Exception:
        logger.debug("feedback: diagnostic query failed", exc_info=True)
        return []


def _db_commit(db: Any) -> None:
    commit = getattr(db, "commit", None)
    if callable(commit):
        commit()


def _count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts = Counter(str(item.get(key) or "unknown") for item in items)
    return dict(sorted(counts.items()))


def _json_size(value: Any) -> int:
    return len(json.dumps(value, default=str, sort_keys=True).encode())


def _safe_shape(value: Any) -> Any:
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, nested in value.items():
            safe_key = _safe_text(key, max_chars=80)
            if isinstance(nested, dict | list):
                out[safe_key] = _safe_shape(nested)
            elif isinstance(nested, bool | int | float) or nested is None:
                out[safe_key] = nested
            else:
                out[safe_key] = _safe_text(nested, max_chars=120)
        return out
    if isinstance(value, list):
        return [_safe_shape(item) for item in value[:20]]
    if isinstance(value, bool | int | float) or value is None:
        return value
    return _safe_text(value, max_chars=120)


def _safe_turn_item(item: Any, allowed_keys: set[str]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {}
    out: dict[str, Any] = {}
    for key in sorted(allowed_keys):
        if key not in item:
            continue
        value = item.get(key)
        if isinstance(value, dict):
            out[key] = _safe_shape(value)
        elif isinstance(value, list | tuple | set):
            out[key] = [_safe_shape(v) for v in list(value)[:20]]
        elif isinstance(value, bool | int | float) or value is None:
            out[key] = value
        else:
            out[key] = _safe_text(value, max_chars=160)
    return out


def sanitize_turn_diagnostics(summary: dict[str, Any] | None) -> dict[str, Any] | None:
    """Reduce a debug summary to the feedback-safe allowlisted shape."""
    if not isinstance(summary, dict):
        return None
    out: dict[str, Any] = {}
    for key in sorted(_TURN_DIAGNOSTIC_TOP_KEYS):
        if key not in summary:
            continue
        value = summary.get(key)
        if key in _TURN_DIAGNOSTIC_ITEM_KEYS and isinstance(value, list):
            out[key] = [
                item for item in (_safe_turn_item(v, _TURN_DIAGNOSTIC_ITEM_KEYS[key]) for v in value[:50]) if item
            ]
        elif key in _TURN_DIAGNOSTIC_DICT_KEYS and isinstance(value, dict):
            out[key] = _safe_turn_item(value, _TURN_DIAGNOSTIC_DICT_KEYS[key])
        elif isinstance(value, bool | int | float) or value is None:
            out[key] = value
        else:
            out[key] = _safe_text(value, max_chars=160)
    return out


def _collect_runtime(
    config: Any,
    *,
    interface: str,
    conversation_id: str | None,
    space_id: str | None,
    active_space: dict[str, Any] | None,
    turn_diagnostics: dict[str, Any] | None,
) -> dict[str, Any]:
    from anteroom import __version__

    ai_cfg = getattr(config, "ai", None)
    runtime: dict[str, Any] = {
        "interface": _safe_text(interface, max_chars=32),
        "anteroom_version": __version__,
        "provider": _safe_text(getattr(ai_cfg, "provider", ""), max_chars=80),
        "model": _safe_text(getattr(ai_cfg, "model", ""), max_chars=120),
        "conversation_id_present": bool(conversation_id),
        "space_id_present": bool(space_id),
        "turn_diagnostics_present": bool(turn_diagnostics),
    }
    if active_space:
        runtime["active_space"] = {
            "id": _safe_text(active_space.get("id") or space_id or "", max_chars=80),
            "name": _safe_text(active_space.get("name") or "", max_chars=120),
        }
    return runtime


def _safe_spaces(spaces: dict[str, Any]) -> dict[str, Any]:
    """Keep space context useful while omitting local paths and instruction text."""
    active = spaces.get("active") if isinstance(spaces, dict) else None
    safe: dict[str, Any] = {
        "available": bool(spaces.get("available")) if isinstance(spaces, dict) else False,
        "total": spaces.get("total", 0) if isinstance(spaces, dict) else 0,
        "names": [_safe_text(name, max_chars=120) for name in spaces.get("names", [])[:50]]
        if isinstance(spaces, dict)
        else [],
        "active": None,
    }
    if isinstance(active, dict):
        safe["active"] = {
            "id": _safe_text(active.get("id") or "", max_chars=80),
            "name": _safe_text(active.get("name") or "", max_chars=120),
            "pack_count": active.get("pack_count", 0),
            "source_count": active.get("source_count", 0),
        }
    return safe


def _collect_packs(db: Any | None, *, project_path: str | None, space_id: str | None) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "installed_count": 0,
        "active_count": 0,
        "artifact_counts_by_type": {},
        "active": [],
    }
    if db is None:
        return manifest
    try:
        from . import pack_attachments, packs

        installed = packs.list_packs(db)
        manifest["installed_count"] = len(installed)
        active_rows = pack_attachments.list_attachments(db, project_path=project_path, space_id=space_id)
    except Exception:
        logger.debug("feedback: failed to collect pack manifest", exc_info=True)
        return manifest

    by_pack: dict[str, dict[str, Any]] = {}
    for row in active_rows:
        pack_id = str(row.get("pack_id") or "")
        if not pack_id:
            continue
        entry = by_pack.setdefault(
            pack_id,
            {
                "id": pack_id,
                "namespace": _safe_text(row.get("namespace") or "", max_chars=80),
                "name": _safe_text(row.get("name") or "", max_chars=80),
                "version": _safe_text(row.get("version") or "", max_chars=80),
                "attachments": [],
            },
        )
        entry["attachments"].append(
            {
                "scope": _safe_text(row.get("scope") or "", max_chars=40),
                "priority": row.get("priority"),
            }
        )

    active_pack_ids = list(by_pack)
    if active_pack_ids:
        placeholders = ",".join("?" for _ in active_pack_ids)
        rows = _db_fetchall(
            db,
            "SELECT pa.pack_id, a.type, COUNT(*) AS count"
            " FROM pack_artifacts pa JOIN artifacts a ON a.id = pa.artifact_id"
            f" WHERE pa.pack_id IN ({placeholders})"
            " GROUP BY pa.pack_id, a.type",
            active_pack_ids,
        )
        type_counts: Counter[str] = Counter()
        for row in rows:
            pack_id = str(_row_value(row, "pack_id", 0, ""))
            artifact_type = _safe_text(_row_value(row, "type", 1, "unknown"), max_chars=80)
            count = int(_row_value(row, "count", 2, 0) or 0)
            type_counts[artifact_type] += count
            if pack_id in by_pack:
                by_pack[pack_id].setdefault("artifact_counts_by_type", {})[artifact_type] = count
        manifest["artifact_counts_by_type"] = dict(sorted(type_counts.items()))

    manifest["active"] = sorted(by_pack.values(), key=lambda p: (p.get("namespace", ""), p.get("name", "")))
    manifest["active_count"] = len(manifest["active"])
    return manifest


def _metadata_keys(metadata: Any) -> list[str]:
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except (json.JSONDecodeError, TypeError):
            metadata = {}
    if not isinstance(metadata, dict):
        return []
    return sorted(_safe_text(k, max_chars=80) for k in metadata.keys())


def _collect_artifacts(
    db: Any | None,
    *,
    project_path: str | None,
    space_id: str | None,
    active_pack_ids: list[str],
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "active_count": 0,
        "counts_by_type": {},
        "counts_by_source": {},
        "active": [],
        "config_overlays": [],
        "config_overlay_count": 0,
    }
    if db is None:
        return manifest
    try:
        from . import artifact_storage

        rows = artifact_storage.list_artifacts(
            db,
            attached_only=True,
            project_path=project_path,
            space_id=space_id,
        )
    except Exception:
        logger.debug("feedback: failed to collect artifact manifest", exc_info=True)
        rows = []

    active: list[dict[str, Any]] = []
    for row in rows:
        item = {
            "fqn": _safe_text(row.get("fqn") or "", max_chars=160),
            "type": _safe_text(row.get("type") or "", max_chars=80),
            "source": _safe_text(row.get("source") or "", max_chars=80),
            "version": row.get("version"),
            "metadata_keys": _metadata_keys(row.get("metadata")),
        }
        try:
            from .artifact_storage import get_pack_for_artifact

            pack = get_pack_for_artifact(db, str(row.get("id") or ""))
            if pack:
                item["pack"] = {
                    "id": _safe_text(pack.get("pack_id") or "", max_chars=80),
                    "namespace": _safe_text(pack.get("namespace") or "", max_chars=80),
                    "name": _safe_text(pack.get("pack_name") or "", max_chars=80),
                }
        except Exception:
            logger.debug("feedback: failed to resolve artifact pack", exc_info=True)
        active.append(item)

    manifest["active"] = active
    manifest["active_count"] = len(active)
    manifest["counts_by_type"] = _count_by(active, "type")
    manifest["counts_by_source"] = _count_by(active, "source")

    if active_pack_ids:
        try:
            from .config_overlays import collect_pack_overlays, flatten_to_dot_paths
            from .pack_attachments import get_attachment_priorities

            priorities = get_attachment_priorities(db, active_pack_ids)
            overlays = []
            for pack_label, overlay in collect_pack_overlays(db, active_pack_ids):
                keys = sorted(_safe_text(k, max_chars=160) for k in flatten_to_dot_paths(overlay).keys())
                overlays.append(
                    {
                        "pack": _safe_text(pack_label, max_chars=160),
                        "priority": priorities.get(pack_label),
                        "keys": keys,
                    }
                )
            manifest["config_overlays"] = overlays
            manifest["config_overlay_count"] = len(overlays)
        except Exception:
            logger.debug("feedback: failed to collect config overlay manifest", exc_info=True)
    return manifest


def _collect_attachments(db: Any | None, *, conversation_id: str | None) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "count": 0,
        "total_bytes": 0,
        "mime_types": {},
        "recent": [],
    }
    if db is None or not conversation_id:
        return summary
    rows = _db_fetchall(
        db,
        "SELECT a.mime_type, a.size_bytes"
        " FROM attachments a JOIN messages m ON m.id = a.message_id"
        " WHERE m.conversation_id = ?"
        " ORDER BY m.position DESC, a.id DESC",
        (conversation_id,),
    )
    recent: list[dict[str, Any]] = []
    mime_counts: Counter[str] = Counter()
    total_bytes = 0
    for row in rows:
        mime_type = _safe_text(_row_value(row, "mime_type", 0, "unknown") or "unknown", max_chars=120)
        size_bytes = int(_row_value(row, "size_bytes", 1, 0) or 0)
        mime_counts[mime_type] += 1
        total_bytes += size_bytes
        if len(recent) < 20:
            recent.append({"mime_type": mime_type, "size_bytes": size_bytes})
    summary["count"] = len(rows)
    summary["total_bytes"] = total_bytes
    summary["mime_types"] = dict(sorted(mime_counts.items()))
    summary["recent"] = recent
    return summary


def _refresh_bundle_manifest(bundle: dict[str, Any]) -> None:
    bundle["bundle_manifest"] = {
        "schema_version": "1",
        "history_included": bool(bundle.get("history_included", False)),
        "turn_diagnostics_included": "turn_diagnostics" in bundle,
        "sections": sorted(k for k in bundle.keys() if k != "bundle_manifest"),
        "omitted": list(_DEFAULT_OMITTED),
        "counts": {
            "packs_active": int(bundle.get("packs", {}).get("active_count", 0) or 0),
            "packs_installed": int(bundle.get("packs", {}).get("installed_count", 0) or 0),
            "artifacts_active": int(bundle.get("artifacts", {}).get("active_count", 0) or 0),
            "config_overlays": int(bundle.get("artifacts", {}).get("config_overlay_count", 0) or 0),
            "attachments": int(bundle.get("attachments", {}).get("count", 0) or 0),
        },
        "section_sizes_bytes": {key: _json_size(value) for key, value in bundle.items() if key != "bundle_manifest"},
    }


def _apply_bundle_size_limit(bundle: dict[str, Any], max_bundle_bytes: int) -> None:
    if _json_size(bundle) <= max_bundle_bytes:
        return
    bundle["truncated"] = True
    truncations: list[str] = []

    def _drop_history() -> None:
        if "conversation_history" in bundle:
            del bundle["conversation_history"]
            bundle["history_included"] = False
            truncations.append("conversation_history")

    def _drop_turn_diagnostics() -> None:
        if "turn_diagnostics" in bundle:
            del bundle["turn_diagnostics"]
            truncations.append("turn_diagnostics")

    def _drop_artifact_rows() -> None:
        artifacts = bundle.get("artifacts")
        if isinstance(artifacts, dict) and artifacts.get("active"):
            artifacts["active"] = []
            truncations.append("artifacts.active")

    def _drop_pack_rows() -> None:
        packs = bundle.get("packs")
        if isinstance(packs, dict) and packs.get("active"):
            packs["active"] = []
            truncations.append("packs.active")

    def _drop_attachment_rows() -> None:
        attachments = bundle.get("attachments")
        if isinstance(attachments, dict) and attachments.get("recent"):
            attachments["recent"] = []
            truncations.append("attachments.recent")

    for reducer in (_drop_history, _drop_turn_diagnostics, _drop_artifact_rows, _drop_pack_rows, _drop_attachment_rows):
        reducer()
        _refresh_bundle_manifest(bundle)
        if _json_size(bundle) <= max_bundle_bytes:
            bundle["truncation_reason"] = "bundle_too_large_details_dropped"
            bundle["truncated_sections"] = truncations
            _refresh_bundle_manifest(bundle)
            return

    if _json_size(bundle) > max_bundle_bytes:
        bundle["spaces"] = {"truncated": True}
        bundle["tools"] = {"truncated": True}
        bundle["truncation_reason"] = "bundle_too_large_details_dropped"
        bundle["truncated_sections"] = truncations + ["spaces", "tools"]
        _refresh_bundle_manifest(bundle)


def redact_history(
    messages: list[dict[str, Any]],
    max_messages: int = 10,
) -> list[dict[str, Any]]:
    """Return the last ``max_messages`` entries with sensitive content removed.

    Only keeps ``role``, ``content`` (truncated to 500 chars), and
    ``created_at``/``position`` to avoid leaking tool inputs/outputs or
    metadata with embedded keys.
    """
    tail = messages[-max_messages:]
    result = []
    for msg in tail:
        role = str(msg.get("role", "unknown"))
        content = msg.get("content", "")
        content = _safe_text(content, max_chars=500)
        if isinstance(msg.get("content", ""), str) and len(msg.get("content", "")) > 500:
            content = content[:485] + "... (truncated)"
        entry: dict[str, Any] = {"role": role, "content": content}
        if "created_at" in msg:
            entry["created_at"] = msg["created_at"]
        if "position" in msg:
            entry["position"] = msg["position"]
        result.append(entry)
    return result


def collect_bundle(
    config: Any,
    description: str,
    *,
    db: Any | None = None,
    conversation_id: str | None = None,
    interface: str = "api",
    space_id: str | None = None,
    project_path: str | None = None,
    active_space: dict[str, Any] | None = None,
    tool_registry: Any | None = None,
    mcp_manager: Any | None = None,
    turn_diagnostics: dict[str, Any] | None = None,
    conversation_messages: list[dict[str, Any]] | None = None,
    max_history_messages: int = 10,
    max_bundle_bytes: int = 1_000_000,
) -> dict[str, Any]:
    """Collect and return a redacted diagnostic bundle.

    Calls existing introspect gatherers for all runtime context.
    Conversation history is only included when ``conversation_messages``
    is provided (explicit opt-in required by callers).
    """
    from ..tools.introspect import (
        _gather_config,
        _gather_package,
        _gather_safety,
        _gather_spaces,
        _gather_tools,
    )

    safe_turn_diagnostics = sanitize_turn_diagnostics(turn_diagnostics)
    packs = _collect_packs(db, project_path=project_path, space_id=space_id)
    active_pack_ids = [str(item.get("id")) for item in packs.get("active", []) if item.get("id")]

    bundle: dict[str, Any] = {
        "schema_version": "1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "description": _safe_text(description, max_chars=4096),
        "runtime": _collect_runtime(
            config,
            interface=interface,
            conversation_id=conversation_id,
            space_id=space_id,
            active_space=active_space,
            turn_diagnostics=safe_turn_diagnostics,
        ),
        "system": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
        },
        "package": _gather_package(),
        "config": _gather_config(config),
        "safety": _gather_safety(config),
        "tools": _gather_tools(tool_registry, mcp_manager, config),
        "spaces": _safe_spaces(_gather_spaces(active_space, db)),
        "packs": packs,
        "artifacts": _collect_artifacts(
            db,
            project_path=project_path,
            space_id=space_id,
            active_pack_ids=active_pack_ids,
        ),
        "attachments": _collect_attachments(db, conversation_id=conversation_id),
    }
    if safe_turn_diagnostics is not None:
        bundle["turn_diagnostics"] = safe_turn_diagnostics

    if conversation_messages is not None:
        bundle["conversation_history"] = redact_history(conversation_messages, max_history_messages)
        bundle["history_included"] = True
    else:
        bundle["history_included"] = False

    _refresh_bundle_manifest(bundle)
    _apply_bundle_size_limit(bundle, max_bundle_bytes)

    return bundle


async def _dispatch_command_reporter(
    reporter_name: str,
    command: str,
    bundle: dict[str, Any],
    timeout: float,
) -> tuple[bool, str]:
    """Dispatch bundle to a shell command via stdin. Returns (success, error)."""
    try:
        payload = json.dumps(bundle, default=str).encode()
        proc = await asyncio.create_subprocess_shell(
            command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr_bytes = await asyncio.wait_for(proc.communicate(input=payload), timeout=timeout)
        except asyncio.TimeoutError:
            try:
                killed = getattr(proc, "kill")()
                if inspect.isawaitable(killed):
                    await killed
                await proc.wait()
            except Exception:
                pass
            return False, f"reporter '{reporter_name}' timed out after {timeout:.0f}s"

        if proc.returncode != 0:
            stderr_preview = (stderr_bytes or b"")[:300].decode("utf-8", errors="replace")
            return False, f"reporter '{reporter_name}' exited {proc.returncode}: {stderr_preview}"

        return True, ""

    except Exception as exc:
        logger.warning("feedback command reporter %r failed: %s", reporter_name, exc, exc_info=True)
        return False, f"reporter '{reporter_name}' error: {exc}"


async def _dispatch_webhook_reporter(
    reporter_name: str,
    url: str,
    bundle: dict[str, Any],
    timeout: float,
    allowed_domains: Sequence[str] = (),
    block_localhost: bool = False,
) -> tuple[bool, str]:
    """POST bundle JSON to a webhook. Returns (success, error)."""
    try:
        from .egress_allowlist import check_egress_allowed

        if not check_egress_allowed(url, allowed_domains, block_localhost=block_localhost):
            return False, f"reporter '{reporter_name}' webhook URL blocked by egress allowlist"
    except Exception as exc:
        return False, f"reporter '{reporter_name}' egress check failed: {exc}"

    try:
        import httpx

        payload = {"event": "feedback_submitted", "bundle": bundle}
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload)
        if resp.status_code >= 400:
            return False, f"reporter '{reporter_name}' returned HTTP {resp.status_code}"
        return True, ""

    except Exception as exc:
        logger.warning("feedback webhook reporter %r failed: %s", reporter_name, exc, exc_info=True)
        return False, f"reporter '{reporter_name}' error: {exc}"


async def submit_feedback(
    description: str,
    config: Any,
    db: Any,
    *,
    conversation_id: str | None = None,
    interface: str = "api",
    space_id: str | None = None,
    project_path: str | None = None,
    conversation_messages: list[dict[str, Any]] | None = None,
    active_space: dict[str, Any] | None = None,
    tool_registry: Any | None = None,
    mcp_manager: Any | None = None,
    turn_diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Collect bundle, persist to DB, dispatch to first enabled reporter.

    Returns a dict with keys:
      - ``status``: ``"sent"`` | ``"saved_locally"`` | ``"failed"``
      - ``reporter``: name of the reporter used (or ``"local"``)
      - ``path``: local file path (only when ``status="saved_locally"``)
      - ``error``: error message (only when ``status="failed"``)
    """
    feedback_cfg = config.feedback
    description = description.strip()
    if not description:
        return {"status": "failed", "reporter": "", "error": "description cannot be empty"}

    bundle = collect_bundle(
        config,
        description,
        db=db,
        conversation_id=conversation_id,
        interface=interface,
        space_id=space_id,
        project_path=project_path,
        active_space=active_space,
        tool_registry=tool_registry,
        mcp_manager=mcp_manager,
        turn_diagnostics=turn_diagnostics,
        conversation_messages=conversation_messages,
        max_history_messages=feedback_cfg.max_history_messages,
        max_bundle_bytes=feedback_cfg.max_bundle_bytes,
    )

    bundle_json_str = json.dumps(bundle, default=str)
    payload_hash = hashlib.sha256(bundle_json_str.encode()).hexdigest()[:16]
    now_iso = datetime.now(timezone.utc).isoformat()
    report_id = str(uuid.uuid4())

    enabled_reporters = [r for r in feedback_cfg.reporters if r.enabled]
    max_attempts = feedback_cfg.retry_attempts if enabled_reporters else 1

    db.execute(
        """
        INSERT INTO feedback_reports
            (id, created_at, updated_at, conversation_id, description,
             reporter_name, status, error, payload_hash, bundle_json,
             attempt_count, max_attempts)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', '', ?, ?, 0, ?)
        """,
        (
            report_id,
            now_iso,
            now_iso,
            conversation_id,
            description,
            enabled_reporters[0].name if enabled_reporters else "local",
            payload_hash,
            bundle_json_str,
            max_attempts,
        ),
    )
    _db_commit(db)

    # No reporters configured — write local fallback
    if not enabled_reporters:
        data_dir = config.app.data_dir
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        local_path = os.path.join(str(data_dir), f"feedback-{ts}-{report_id}.json")
        try:
            with open(local_path, "w", encoding="utf-8") as fh:
                json.dump(bundle, fh, indent=2, default=str)
            db.execute(
                "UPDATE feedback_reports SET status='sent', updated_at=? WHERE id=?",
                (datetime.now(timezone.utc).isoformat(), report_id),
            )
            _db_commit(db)
            return {"status": "saved_locally", "reporter": "local", "path": local_path}
        except Exception as exc:
            err = f"failed to write local bundle: {exc}"
            db.execute(
                "UPDATE feedback_reports SET status='failed', error=?, updated_at=? WHERE id=?",
                (err[:500], datetime.now(timezone.utc).isoformat(), report_id),
            )
            _db_commit(db)
            return {"status": "failed", "reporter": "local", "error": err}

    # Dispatch to first enabled reporter with bounded retry
    reporter = enabled_reporters[0]
    allowed_domains = list(config.ai.allowed_domains) if hasattr(config.ai, "allowed_domains") else []
    block_localhost = bool(getattr(config.ai, "block_localhost_api", False))
    last_error = ""

    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            await asyncio.sleep(feedback_cfg.retry_backoff_seconds)

        attempt_ts = datetime.now(timezone.utc).isoformat()
        db.execute(
            "UPDATE feedback_reports SET attempt_count=?, last_attempt_at=?, updated_at=? WHERE id=?",
            (attempt, attempt_ts, attempt_ts, report_id),
        )
        _db_commit(db)

        if reporter.type == "command":
            success, last_error = await _dispatch_command_reporter(
                reporter.name, reporter.command, bundle, float(reporter.timeout)
            )
        else:
            success, last_error = await _dispatch_webhook_reporter(
                reporter.name,
                reporter.url,
                bundle,
                float(reporter.timeout),
                allowed_domains=allowed_domains,
                block_localhost=block_localhost,
            )

        if success:
            db.execute(
                "UPDATE feedback_reports SET status='sent', updated_at=? WHERE id=?",
                (datetime.now(timezone.utc).isoformat(), report_id),
            )
            _db_commit(db)
            return {"status": "sent", "reporter": reporter.name}

    # All attempts exhausted
    db.execute(
        "UPDATE feedback_reports SET status='failed', error=?, updated_at=? WHERE id=?",
        (last_error[:500], datetime.now(timezone.utc).isoformat(), report_id),
    )
    _db_commit(db)
    return {"status": "failed", "reporter": reporter.name, "error": last_error}
