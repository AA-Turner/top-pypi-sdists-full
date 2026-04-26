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
import json
import logging
import os
import platform
import sys
import uuid
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger(__name__)

_SENSITIVE_SUBSTRINGS = ("key", "secret", "password", "token", "passphrase")


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
        if isinstance(content, str) and len(content) > 500:
            content = content[:500] + "... (truncated)"
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
    active_space: dict[str, Any] | None = None,
    tool_registry: Any | None = None,
    mcp_manager: Any | None = None,
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

    bundle: dict[str, Any] = {
        "schema_version": "1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "description": description,
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
        "spaces": _gather_spaces(active_space, db),
    }

    if conversation_messages is not None:
        bundle["conversation_history"] = redact_history(conversation_messages, max_history_messages)
        bundle["history_included"] = True
    else:
        bundle["history_included"] = False

    # Enforce max bundle size
    raw = json.dumps(bundle, default=str)
    if len(raw.encode()) > max_bundle_bytes:
        bundle["truncated"] = True
        if "conversation_history" in bundle:
            del bundle["conversation_history"]
            bundle["history_included"] = False
            bundle["truncation_reason"] = "bundle_too_large_history_dropped"
        raw = json.dumps(bundle, default=str)
        if len(raw.encode()) > max_bundle_bytes:
            bundle["spaces"] = {"truncated": True}
            bundle["tools"] = {"truncated": True}
            bundle["truncation_reason"] = "bundle_too_large_details_dropped"

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
                proc.kill()
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
    conversation_messages: list[dict[str, Any]] | None = None,
    active_space: dict[str, Any] | None = None,
    tool_registry: Any | None = None,
    mcp_manager: Any | None = None,
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
        active_space=active_space,
        tool_registry=tool_registry,
        mcp_manager=mcp_manager,
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

    # No reporters configured — write local fallback
    if not enabled_reporters:
        data_dir = config.app.data_dir
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        local_path = os.path.join(str(data_dir), f"feedback-{ts}.json")
        try:
            with open(local_path, "w", encoding="utf-8") as fh:
                json.dump(bundle, fh, indent=2, default=str)
            db.execute(
                "UPDATE feedback_reports SET status='sent', updated_at=? WHERE id=?",
                (datetime.now(timezone.utc).isoformat(), report_id),
            )
            return {"status": "saved_locally", "reporter": "local", "path": local_path}
        except Exception as exc:
            err = f"failed to write local bundle: {exc}"
            db.execute(
                "UPDATE feedback_reports SET status='failed', error=?, updated_at=? WHERE id=?",
                (err[:500], datetime.now(timezone.utc).isoformat(), report_id),
            )
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
            return {"status": "sent", "reporter": reporter.name}

    # All attempts exhausted
    db.execute(
        "UPDATE feedback_reports SET status='failed', error=?, updated_at=? WHERE id=?",
        (last_error[:500], datetime.now(timezone.utc).isoformat(), report_id),
    )
    return {"status": "failed", "reporter": reporter.name, "error": last_error}
