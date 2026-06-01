"""Tail Claude Code transcript JSONL and forward assistant events incrementally."""

from __future__ import annotations

import json
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.config import load_config
from runlayer_cli.tls import http_client

_STATE_DIR = Path(tempfile.gettempdir()) / "runlayer-claude-transcript-stream"
_ACTIVE_MARKER_MAX_AGE_SECONDS = 10
_DEFAULT_MAX_SECONDS = 900.0
_DEFAULT_IDLE_SECONDS = 900.0
_DEFAULT_POLL_SECONDS = 0.25


class PostEvent(Protocol):
    def __call__(
        self,
        client_name: str,
        event_name: str,
        payload: dict[str, Any],
    ) -> None: ...


def transcript_marker_path(payload: dict[str, Any]) -> Path | None:
    session_id = _session_id(payload)
    if not session_id:
        return None
    safe_session_id = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id).strip("._")
    if not safe_session_id:
        return None
    return _STATE_DIR / f"{safe_session_id}.active"


def is_transcript_stream_active(payload: dict[str, Any]) -> bool:
    marker = transcript_marker_path(payload)
    if marker is None or not marker.exists():
        return False
    try:
        raw_heartbeat = marker.read_text().strip()
        heartbeat = float(raw_heartbeat) if raw_heartbeat else marker.stat().st_mtime
        age_seconds = time.time() - heartbeat
    except OSError:
        return False
    except ValueError:
        return False
    return 0 <= age_seconds < _ACTIVE_MARKER_MAX_AGE_SECONDS


def mark_transcript_stream_active(payload: dict[str, Any]) -> bool:
    marker = transcript_marker_path(payload)
    if marker is None:
        return False
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(str(int(time.time())))
    except OSError:
        return False
    return True


def clear_transcript_stream_active(payload: dict[str, Any]) -> None:
    marker = transcript_marker_path(payload)
    if marker is None:
        return
    try:
        marker.unlink(missing_ok=True)
    except OSError:
        pass


def resolve_transcript_path(payload: dict[str, Any]) -> Path | None:
    raw_path = payload.get("transcript_path")
    if not isinstance(raw_path, str) or not raw_path:
        return None
    return Path(raw_path).expanduser()


def transcript_start_offset(payload: dict[str, Any]) -> int:
    path = resolve_transcript_path(payload)
    if path is None:
        return 0
    try:
        return path.stat().st_size if path.exists() else 0
    except OSError:
        return 0


def run_transcript_stream(
    *,
    client_name: str,
    payload: dict[str, Any],
    start_offset: int = 0,
    debug: bool = False,
    max_seconds: float = _DEFAULT_MAX_SECONDS,
    idle_seconds: float = _DEFAULT_IDLE_SECONDS,
    poll_seconds: float = _DEFAULT_POLL_SECONDS,
    post_event: PostEvent | None = None,
) -> None:
    path = resolve_transcript_path(payload)
    session_id = _session_id(payload)
    if path is None or not session_id:
        return

    offset = max(0, start_offset)
    buffer = ""
    seen: set[tuple[str, str, str]] = set()
    started = time.monotonic()
    last_activity = started
    backfill_required = False
    posting_healthy = False
    effective_post: PostEvent | None = None

    def process_line(line: str) -> bool:
        nonlocal backfill_required, last_activity, posting_healthy
        assert effective_post is not None
        terminal_line = transcript_line_is_terminal(line)
        for event_name, event_payload in transcript_line_events(
            line,
            fallback_session_id=session_id,
        ):
            text_key = (
                event_payload.get("part", {}).get("text")
                if event_name == "message.part.delta"
                else event_payload.get("message", {}).get("content")
            )
            dedupe_key = (
                event_name,
                str(event_payload.get("timestamp", "")),
                str(text_key),
            )
            if dedupe_key in seen:
                continue
            try:
                effective_post(client_name, event_name, event_payload)
            except Exception as exc:
                if debug:
                    print(
                        f"Runlayer transcript stream post failed: {exc}",
                        file=sys.stderr,
                    )
                backfill_required = True
                posting_healthy = False
                clear_transcript_stream_active(payload)
                continue
            seen.add(dedupe_key)
            posting_healthy = True
            if not backfill_required:
                mark_transcript_stream_active(payload)
            last_activity = time.monotonic()
        return terminal_line

    try:
        effective_post = post_event or _make_http_event_poster(debug=debug)
        while time.monotonic() - started < max_seconds:
            if posting_healthy and not backfill_required:
                mark_transcript_stream_active(payload)
            try:
                size = path.stat().st_size
            except OSError:
                time.sleep(poll_seconds)
                continue

            if size < offset:
                offset = 0
                buffer = ""

            if size > offset:
                try:
                    with path.open("rb") as f:
                        f.seek(offset)
                        chunk = f.read(size - offset)
                    offset = size
                except OSError:
                    time.sleep(poll_seconds)
                    continue

                if chunk:
                    buffer += chunk.decode("utf-8", errors="replace")
                    complete_lines, buffer = _split_complete_lines(buffer)
                    for line in complete_lines:
                        if process_line(line):
                            return
            elif buffer and _buffer_is_complete_json_line(buffer):
                line = buffer.strip()
                buffer = ""
                if process_line(line):
                    return
            elif time.monotonic() - last_activity >= idle_seconds:
                break

            time.sleep(poll_seconds)
    finally:
        close_post = getattr(effective_post, "close", None)
        if callable(close_post):
            close_post()
        clear_transcript_stream_active(payload)


def transcript_line_events(
    line: str,
    *,
    fallback_session_id: str,
) -> list[tuple[str, dict[str, Any]]]:
    try:
        entry = json.loads(line)
    except json.JSONDecodeError:
        return []
    if not isinstance(entry, dict):
        return []

    session_id = (
        _first_string(entry, ("session_id", "sessionId")) or fallback_session_id
    )
    timestamp = _first_string(entry, ("timestamp", "created_at")) or _timestamp()
    raw_msg = entry.get("message") or entry.get("payload") or entry.get("item")
    if raw_msg is None:
        raw_msg = entry
    msg = raw_msg if isinstance(raw_msg, dict) else entry

    events: list[tuple[str, dict[str, Any]]] = []
    if msg.get("type") == "reasoning":
        for text in _iter_text_values(msg.get("summary")):
            events.append(_thought_event(session_id, timestamp, text))
        for text in _iter_text_values(msg.get("content")):
            events.append(_thought_event(session_id, timestamp, text))
        return events

    role = msg.get("role", entry.get("role", ""))
    if role != "assistant":
        return []

    content_blocks = msg.get("content", entry.get("content", []))
    if isinstance(content_blocks, str):
        return [_response_event(session_id, timestamp, content_blocks)]
    if not isinstance(content_blocks, list):
        return []

    for block in content_blocks:
        if not isinstance(block, dict):
            continue
        block_type = block.get("type", "")
        if block_type in ("thinking", "reasoning", "summary_text"):
            text = _first_string(
                block,
                ("thinking", "text", "summary", "content"),
            )
            if text:
                events.append(_thought_event(session_id, timestamp, text))
        elif block_type in ("text", "output_text"):
            text = _first_string(block, ("text", "content"))
            if text:
                events.append(_response_event(session_id, timestamp, text))
    return events


def transcript_line_is_terminal(line: str) -> bool:
    try:
        entry = json.loads(line)
    except json.JSONDecodeError:
        return False
    return isinstance(entry, dict) and entry.get("type") in (
        "result",
        "session_end",
    )


def _split_complete_lines(buffer: str) -> tuple[list[str], str]:
    lines = buffer.splitlines(keepends=True)
    if not lines:
        return [], ""
    if lines[-1].endswith(("\n", "\r")):
        return [line.strip() for line in lines if line.strip()], ""
    return [line.strip() for line in lines[:-1] if line.strip()], lines[-1]


def _buffer_is_complete_json_line(buffer: str) -> bool:
    candidate = buffer.strip()
    if not candidate:
        return False
    try:
        json.loads(candidate)
    except json.JSONDecodeError:
        return False
    return True


class _HTTPEventPoster:
    def __init__(self, *, debug: bool) -> None:
        config = load_config()
        host = config.default_host
        secret = config.get_secret_for_host(host) if host else None
        if not host or not secret:
            raise RuntimeError("missing Runlayer hook credentials")
        self._client = http_client()
        self._debug = debug
        self._host = host
        self._secret = secret

    def __call__(
        self,
        client_name: str,
        event_name: str,
        payload: dict[str, Any],
    ) -> None:
        wrapper = json.dumps(
            {"client": client_name, "event_name": event_name, "payload": payload}
        )
        try:
            resp = self._client.post(
                f"{self._host}/api/v1/hooks/events",
                content=wrapper,
                headers={
                    "Content-Type": "application/json",
                    API_KEY_HEADER_NAME: self._secret,
                    "User-Agent": USER_AGENT,
                },
                timeout=5,
            )
        except Exception as exc:
            if self._debug:
                print(
                    f"Runlayer transcript stream post failed: {exc}",
                    file=sys.stderr,
                )
            raise
        if self._debug and not resp.is_success:
            print(
                f"Runlayer transcript stream post failed: HTTP {resp.status_code}",
                file=sys.stderr,
            )
        if not resp.is_success:
            resp.raise_for_status()

    def close(self) -> None:
        close_client = getattr(self._client, "close", None)
        if callable(close_client):
            close_client()


def _make_http_event_poster(*, debug: bool) -> PostEvent:
    return _HTTPEventPoster(debug=debug)


def _session_id(payload: dict[str, Any]) -> str:
    return _first_string(
        payload,
        ("session_id", "conversation_id", "transcript_id", "chat_id"),
    )


def _thought_event(
    session_id: str,
    timestamp: str,
    text: str,
) -> tuple[str, dict[str, Any]]:
    return (
        "message.part.delta",
        {
            "session_id": session_id,
            "timestamp": timestamp,
            "part": {"type": "reasoning", "text": text},
        },
    )


def _response_event(
    session_id: str,
    timestamp: str,
    text: str,
) -> tuple[str, dict[str, Any]]:
    return (
        "message.updated",
        {
            "session_id": session_id,
            "timestamp": timestamp,
            "message": {"content": text},
        },
    )


def _iter_text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(_iter_text_values(item))
        return result
    if isinstance(value, dict):
        direct = _first_string(value, ("text", "content", "summary", "thinking"))
        if direct:
            return [direct]
        return _iter_text_values(value.get("summary"))
    return []


def _first_string(value: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate:
            return candidate
    return ""


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
