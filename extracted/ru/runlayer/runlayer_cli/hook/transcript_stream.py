"""Tail AI client transcript JSONL and forward assistant events incrementally."""

from __future__ import annotations

import json
import sys
import tempfile
import time
import uuid
from collections.abc import Iterator
from contextlib import AbstractContextManager, nullcontext
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO, Protocol, TypedDict, cast

from runlayer_sdk.hook_transport import (
    API_KEY_HEADER_NAME,
    HookAPIClient,
    HookHTTPClient,
    HookHTTPResponse,
    WireBody,
    encode_wire_body,
)

from runlayer_cli import regex_safe
from runlayer_cli.api import USER_AGENT
from runlayer_cli.config import load_config, normalize_url
from runlayer_cli.mdm_config import read_managed_config
from runlayer_cli.tls import http_client

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

_STATE_DIR = Path(tempfile.gettempdir()) / "runlayer-claude-transcript-stream"
_ACTIVE_MARKER_MAX_AGE_SECONDS = 10
_COMPLETED_MARKER_MAX_AGE_SECONDS = 120
_CLAIM_MARKER_MAX_AGE_SECONDS = 30
_CLAIM_HEARTBEAT_SECONDS = 10.0
_DEFAULT_MAX_SECONDS = 900.0
_DEFAULT_IDLE_SECONDS = 900.0
_DEFAULT_POLL_SECONDS = 0.25
_TRANSCRIPT_READ_MAX_BYTES = 4 * 1024 * 1024
_TRANSCRIPT_LINE_MAX_BYTES = 1024 * 1024
_TRANSCRIPT_DEDUPE_MAX_ENTRIES = 10_000
_CLAIM_GUARD_WAIT_SECONDS = 0.1


class PostEvent(Protocol):
    def __call__(
        self,
        client_name: str,
        event_name: str,
        payload: dict[str, Any],
    ) -> None: ...


def transcript_marker_path(payload: dict[str, Any]) -> Path | None:
    return _transcript_marker_path(payload, "active")


def transcript_completion_marker_path(payload: dict[str, Any]) -> Path | None:
    return _transcript_marker_path(payload, "completed")


def transcript_claim_marker_path(payload: dict[str, Any]) -> Path | None:
    return _transcript_marker_path(payload, "claim")


def _transcript_claim_cleanup_marker_path(
    payload: dict[str, Any],
) -> Path | None:
    marker = transcript_claim_marker_path(payload)
    if marker is None:
        return None
    return marker.with_name(f"{marker.name}.cleanup")


def _transcript_claim_guard_path() -> Path:
    return _STATE_DIR / ".claim-cleanup.guard"


def _transcript_marker_path(payload: dict[str, Any], suffix: str) -> Path | None:
    session_id = _session_id(payload)
    if not session_id:
        return None
    safe_session_id = regex_safe.sub(r"[^A-Za-z0-9_.-]", "_", session_id).strip("._")
    if not safe_session_id:
        return None
    return _STATE_DIR / f"{safe_session_id}.{suffix}"


def is_transcript_stream_active(payload: dict[str, Any]) -> bool:
    return _has_recent_transcript_marker(
        transcript_marker_path(payload),
        max_age_seconds=_ACTIVE_MARKER_MAX_AGE_SECONDS,
    )


def is_transcript_stream_recently_completed(payload: dict[str, Any]) -> bool:
    return _has_recent_transcript_marker(
        transcript_completion_marker_path(payload),
        max_age_seconds=_COMPLETED_MARKER_MAX_AGE_SECONDS,
    )


def is_transcript_stream_claimed(payload: dict[str, Any]) -> bool:
    return _has_recent_transcript_marker(
        transcript_claim_marker_path(payload),
        max_age_seconds=_CLAIM_MARKER_MAX_AGE_SECONDS,
    )


def is_transcript_stream_claim_in_progress(payload: dict[str, Any]) -> bool:
    return _has_recent_transcript_marker(
        _transcript_claim_cleanup_marker_path(payload),
        max_age_seconds=_CLAIM_MARKER_MAX_AGE_SECONDS,
    )


def _has_recent_transcript_marker(marker: Path | None, *, max_age_seconds: int) -> bool:
    if marker is None or not marker.exists():
        return False
    try:
        raw_heartbeat = marker.read_text().strip()
        if raw_heartbeat:
            try:
                marker_value = json.loads(raw_heartbeat)
            except json.JSONDecodeError:
                marker_value = raw_heartbeat
            if isinstance(marker_value, dict):
                marker_value = marker_value.get("ts")
            if isinstance(marker_value, bool):
                return False
            heartbeat = float(marker_value)
        else:
            heartbeat = marker.stat().st_mtime
        age_seconds = time.time() - heartbeat
    except OSError:
        return False
    except (TypeError, ValueError):
        return False
    return 0 <= age_seconds < max_age_seconds


def claim_transcript_stream(payload: dict[str, Any]) -> str | None:
    """Atomically reserve one worker spawn for a session."""
    marker = transcript_claim_marker_path(payload)
    if marker is None:
        return None
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    token = uuid.uuid4().hex
    if _create_transcript_claim(marker, token=token):
        return token
    if is_transcript_stream_claimed(payload):
        return None

    # Serialize stale cleanup with an OS lock, which the kernel releases if a
    # cleaner crashes. The visible cleanup marker remains a short lease so
    # older/in-flight cleaners are respected, but a stale one can be removed
    # safely while all current cleaners are serialized here.
    guard_path = _transcript_claim_guard_path()
    cleanup_lock = _transcript_claim_cleanup_marker_path(payload)
    assert cleanup_lock is not None
    guard_file = _acquire_claim_guard(guard_path)
    if guard_file is None:
        return None
    try:
        if _create_transcript_claim(marker, token=token):
            return token
        if is_transcript_stream_claimed(payload):
            return None
        if is_transcript_stream_claim_in_progress(payload):
            return None
        _clear_transcript_marker(cleanup_lock)
        if not _create_transcript_claim(cleanup_lock):
            return None
        try:
            if is_transcript_stream_claimed(payload):
                return None
            _clear_transcript_marker(marker)
            if _create_transcript_claim(marker, token=token):
                return token
            return None
        finally:
            _clear_transcript_marker(cleanup_lock)
    finally:
        _release_claim_guard(guard_file)


def _acquire_claim_guard(guard_path: Path) -> BinaryIO | None:
    guard_file: BinaryIO | None = None
    try:
        guard_file = guard_path.open("a+b")
        if sys.platform == "win32":
            guard_file.seek(0, 2)
            if guard_file.tell() == 0:
                guard_file.write(b"\0")
                guard_file.flush()
        deadline = time.monotonic() + _CLAIM_GUARD_WAIT_SECONDS
        while True:
            try:
                if sys.platform == "win32":
                    guard_file.seek(0)
                    msvcrt.locking(guard_file.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(
                        guard_file.fileno(),
                        fcntl.LOCK_EX | fcntl.LOCK_NB,
                    )
                return guard_file
            except OSError:
                if time.monotonic() >= deadline:
                    _close_claim_guard(guard_file)
                    return None
                time.sleep(0.001)
    except OSError:
        if guard_file is not None:
            _close_claim_guard(guard_file)
        return None


def _release_claim_guard(guard_file: BinaryIO) -> None:
    try:
        if sys.platform == "win32":
            guard_file.seek(0)
            msvcrt.locking(guard_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(guard_file.fileno(), fcntl.LOCK_UN)
    except OSError:
        pass
    finally:
        _close_claim_guard(guard_file)


def _close_claim_guard(guard_file: BinaryIO) -> None:
    try:
        guard_file.close()
    except OSError:
        pass


def _create_transcript_claim(marker: Path, *, token: str | None = None) -> bool:
    created = False
    try:
        with marker.open("x") as claim_file:
            created = True
            marker_value = (
                _transcript_claim_marker_value(token)
                if token is not None
                else str(time.time())
            )
            claim_file.write(marker_value)
    except FileExistsError:
        return False
    except OSError:
        if created:
            _clear_transcript_marker(marker)
        return False
    return True


def _transcript_claim_marker_value(token: str) -> str:
    return json.dumps(
        {"ts": time.time(), "token": token},
        separators=(",", ":"),
    )


def heartbeat_transcript_stream_claim(
    payload: dict[str, Any],
    token: str,
) -> bool:
    """Refresh a claim only while its ownership token still matches."""
    marker = transcript_claim_marker_path(payload)
    if marker is None or not token:
        return False
    guard_file = _acquire_claim_guard(_transcript_claim_guard_path())
    if guard_file is None:
        return False
    try:
        try:
            claim = json.loads(marker.read_text())
        except (OSError, json.JSONDecodeError):
            return False
        if not isinstance(claim, dict) or claim.get("token") != token:
            return False
        temporary_marker = marker.with_name(f".{marker.name}.{token}.tmp")
        try:
            temporary_marker.write_text(_transcript_claim_marker_value(token))
            temporary_marker.replace(marker)
        except OSError:
            return False
        finally:
            _clear_transcript_marker(temporary_marker)
        return True
    finally:
        _release_claim_guard(guard_file)


def mark_transcript_stream_active(payload: dict[str, Any]) -> bool:
    clear_transcript_stream_completed(payload)
    marker = transcript_marker_path(payload)
    if marker is None:
        return False
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(str(int(time.time())))
    except OSError:
        return False
    return True


def mark_transcript_stream_completed(payload: dict[str, Any]) -> bool:
    marker = transcript_completion_marker_path(payload)
    if marker is None:
        return False
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(str(int(time.time())))
    except OSError:
        return False
    return True


def clear_transcript_stream_active(payload: dict[str, Any]) -> None:
    _clear_transcript_marker(transcript_marker_path(payload))


def clear_transcript_stream_completed(payload: dict[str, Any]) -> None:
    _clear_transcript_marker(transcript_completion_marker_path(payload))


def clear_transcript_stream_claim(payload: dict[str, Any], token: str) -> None:
    """Clear a claim only while its ownership token still matches."""
    marker = transcript_claim_marker_path(payload)
    if marker is None or not token:
        return
    guard_file = _acquire_claim_guard(_transcript_claim_guard_path())
    if guard_file is None:
        return
    try:
        try:
            claim = json.loads(marker.read_text())
        except (OSError, json.JSONDecodeError):
            return
        if isinstance(claim, dict) and claim.get("token") == token:
            _clear_transcript_marker(marker)
    finally:
        _release_claim_guard(guard_file)


def _clear_transcript_marker(marker: Path | None) -> None:
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


def transcript_sent_state_path(payload: dict[str, Any]) -> Path | None:
    return _transcript_marker_path(payload, "sent")


class TranscriptSentState(TypedDict):
    offset: int
    model: str | None


def load_sent_state_for(
    payload: dict[str, Any], transcript_path: Path
) -> TranscriptSentState | None:
    """Validated sent-state (bytes durably delivered + last Codex model) for
    this transcript path. One place owns the path match and field coercion so
    the consumers (tailer seed, Stop sender, stale flush) can't drift."""
    state_path = transcript_sent_state_path(payload)
    if state_path is None or not state_path.exists():
        return None
    try:
        state = json.loads(state_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(state, dict) or state.get("path") != str(transcript_path):
        return None
    raw_offset = state.get("offset")
    raw_model = state.get("model")
    return {
        "offset": raw_offset if isinstance(raw_offset, int) and raw_offset >= 0 else 0,
        "model": raw_model if isinstance(raw_model, str) and raw_model else None,
    }


def store_transcript_sent_state(
    payload: dict[str, Any],
    *,
    client: str,
    transcript_path: Path,
    offset: int,
    model: str | None = None,
) -> bool:
    state_path = transcript_sent_state_path(payload)
    if state_path is None:
        return False
    state = {
        "session_id": _session_id(payload),
        "client": client,
        "path": str(transcript_path),
        "offset": int(offset),
        "model": model,
        "updated": time.time(),
    }
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = state_path.parent / (state_path.name + ".tmp")
        tmp.write_text(json.dumps(state))
        tmp.replace(state_path)
    except OSError:
        return False
    return True


def iter_transcript_sent_states() -> Iterator[tuple[Path, dict[str, Any]]]:
    try:
        state_paths = sorted(_STATE_DIR.glob("*.sent"))
    except OSError:
        return
    for state_path in state_paths:
        try:
            state = json.loads(state_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(state, dict):
            yield state_path, state


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
    claim_token: str | None = None,
) -> None:
    path = resolve_transcript_path(payload)
    session_id = _session_id(payload)
    if path is None or not session_id:
        return

    offset = max(0, start_offset)
    buffer = ""
    seen: dict[tuple[str, str, str], None] = {}
    dedupe_max_entries = max(1, _TRANSCRIPT_DEDUPE_MAX_ENTRIES)
    # Carries the last-seen Codex turn_context model forward onto token_count
    # facts (Codex records the model on turn_context, not on the usage line).
    stream_state: dict[str, Any] = {}
    # Persisting the sent-offset is only sound when delivery is contiguous:
    # everything before start_offset must already be durable (the worker's
    # pre-tail flush), or a Stop-side send would treat the gap as delivered.
    prior = load_sent_state_for(payload, path)
    if prior is not None and prior["model"]:
        stream_state["model"] = prior["model"]
    persist_allowed = offset == 0 or (prior is not None and prior["offset"] >= offset)
    last_persisted = -1
    started = time.monotonic()
    last_activity = started
    last_claim_heartbeat = started
    backfill_required = False
    posting_healthy = False
    completed_healthy = False
    effective_post: PostEvent | None = None

    def require_backfill(reason: str) -> None:
        nonlocal backfill_required, posting_healthy
        first_failure = not backfill_required
        backfill_required = True
        posting_healthy = False
        clear_transcript_stream_active(payload)
        clear_transcript_stream_completed(payload)
        if debug and first_failure:
            print(
                f"Runlayer transcript stream requires backfill: {reason}",
                file=sys.stderr,
            )

    def persist_sent(sent_through: int) -> None:
        nonlocal last_persisted
        if not persist_allowed or backfill_required or not posting_healthy:
            return
        if sent_through == last_persisted:
            return
        # Only remember offsets that actually reached disk, so a failed write
        # is retried at the same offset on the next batch.
        if store_transcript_sent_state(
            payload,
            client=client_name,
            transcript_path=path,
            offset=sent_through,
            model=stream_state.get("model"),
        ):
            last_persisted = sent_through

    def process_line(line: str) -> bool:
        nonlocal backfill_required, completed_healthy, last_activity, posting_healthy
        assert effective_post is not None
        terminal_line = transcript_line_is_terminal(line)
        for event_name, event_payload in transcript_line_events(
            line,
            fallback_session_id=session_id,
            stream_state=stream_state,
            client_name=client_name,
        ):
            text_key = _dedupe_text_key(event_name, event_payload)
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
                clear_transcript_stream_completed(payload)
                continue
            seen[dedupe_key] = None
            if len(seen) > dedupe_max_entries:
                del seen[next(iter(seen))]
            posting_healthy = not backfill_required
            if not backfill_required:
                mark_transcript_stream_active(payload)
            last_activity = time.monotonic()
        if terminal_line and posting_healthy and not backfill_required:
            mark_transcript_stream_active(payload)
            completed_healthy = True
        return terminal_line

    try:
        effective_post = post_event or _make_http_event_poster(debug=debug)
        while time.monotonic() - started < max_seconds:
            now = time.monotonic()
            if (
                claim_token is not None
                and now - last_claim_heartbeat >= _CLAIM_HEARTBEAT_SECONDS
            ):
                if heartbeat_transcript_stream_claim(payload, claim_token):
                    last_claim_heartbeat = now
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
                available = size - offset
                if available > _TRANSCRIPT_READ_MAX_BYTES:
                    offset = size - _TRANSCRIPT_READ_MAX_BYTES
                    buffer = ""
                    require_backfill("delta exceeded read cap; reading capped tail")
                read_size = min(size - offset, _TRANSCRIPT_READ_MAX_BYTES)
                try:
                    with path.open("rb") as f:
                        f.seek(offset)
                        chunk = f.read(read_size)
                    offset += len(chunk)
                except OSError:
                    time.sleep(poll_seconds)
                    continue

                if chunk:
                    buffer += chunk.decode("utf-8", errors="replace")
                    complete_lines, buffer = _split_complete_lines(buffer)
                    if len(buffer.encode("utf-8")) > _TRANSCRIPT_LINE_MAX_BYTES:
                        buffer = ""
                        require_backfill("partial line exceeded size cap")
                    bounded_lines: list[str] = []
                    for line in complete_lines:
                        if len(line.encode("utf-8")) > _TRANSCRIPT_LINE_MAX_BYTES:
                            require_backfill("line exceeded size cap")
                        else:
                            bounded_lines.append(line)
                    terminal = False
                    for line in bounded_lines:
                        if process_line(line):
                            terminal = True
                            break
                    # Sent-through the last complete line; trailing lines past a
                    # terminal line in the same read are marked sent too — the
                    # session is over, nothing usage-bearing follows it.
                    if complete_lines:
                        persist_sent(offset - len(buffer.encode("utf-8")))
                    if terminal:
                        return
            elif buffer and _buffer_is_complete_json_line(buffer):
                line = buffer.strip()
                buffer = ""
                terminal = process_line(line)
                persist_sent(offset)
                if terminal:
                    return
            elif time.monotonic() - last_activity >= idle_seconds:
                break

            time.sleep(poll_seconds)
    finally:
        close_post = getattr(effective_post, "close", None)
        if callable(close_post):
            close_post()
        if completed_healthy:
            mark_transcript_stream_completed(payload)
            clear_transcript_stream_active(payload)
        else:
            clear_transcript_stream_active(payload)
            clear_transcript_stream_completed(payload)


def _dedupe_text_key(event_name: str, payload: dict[str, Any]) -> Any:
    """Per-event-type key for the stream's in-run dedupe set.

    Scoped explicitly per type so only ``message.token_count`` (which carries no
    text) keys on its stable per-turn ``external_message_id``; other event types
    keep keying on their content and are unaffected.
    """
    if event_name == "message.part.delta":
        return payload.get("part", {}).get("text")
    if event_name == "message.token_count":
        return payload.get("external_message_id")
    return payload.get("message", {}).get("content")


def transcript_line_events(
    line: str,
    *,
    fallback_session_id: str,
    stream_state: dict[str, Any] | None = None,
    client_name: str | None = None,
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

    # Codex records the active model on turn_context lines, which precede the
    # token_count line for that turn. Track it so the usage fact carries a model
    # (must match the backend Stop-replay closure, or the streamed and backfilled
    # facts get different dedupe keys and double count).
    if stream_state is not None and entry.get("type") == "turn_context":
        model = _first_string(msg, ("model",))
        if model:
            stream_state["model"] = model
        return []

    events: list[tuple[str, dict[str, Any]]] = []
    if msg.get("type") == "token_count":
        model = (stream_state or {}).get("model")
        token_event = _token_count_event(session_id, timestamp, msg, model=model)
        return [token_event] if token_event is not None else []

    if msg.get("type") == "reasoning":
        for text in _iter_text_values(msg.get("summary")):
            events.append(_thought_event(session_id, timestamp, text))
        for text in _iter_text_values(msg.get("content")):
            events.append(_thought_event(session_id, timestamp, text))
        return events

    role = msg.get("role", entry.get("role", ""))
    if role != "assistant":
        return []

    if client_name in _CLAUDE_USAGE_STREAM_CLIENTS:
        usage_event = _claude_usage_token_event(
            session_id,
            timestamp,
            msg,
            stream_state=stream_state,
        )
        if usage_event is not None:
            events.append(usage_event)

    content_blocks = msg.get("content", entry.get("content", []))
    if isinstance(content_blocks, str):
        events.append(_response_event(session_id, timestamp, content_blocks))
        return events
    if not isinstance(content_blocks, list):
        return events

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
        managed = read_managed_config()
        raw_host = config.default_host or managed.get("host")
        host = normalize_url(raw_host) if raw_host else None
        # Mirror relay._load_credentials: prefer the org API key (the single AI
        # Watch key) so streamed events authenticate the same way as other
        # hooks; per-user secret remains the fallback.
        org_api_key = managed.get("org_api_key")
        secret = org_api_key or (config.get_secret_for_host(host) if host else None)
        if not host or not secret:
            raise RuntimeError("missing Runlayer hook credentials")
        self._client = http_client()
        self._debug = debug
        self._org_key_mode = bool(org_api_key)
        self._base_headers = {
            API_KEY_HEADER_NAME: secret,
            "User-Agent": USER_AGENT,
        }
        self._hook_client = HookAPIClient(
            host,
            headers=self._base_headers,
            http_client_factory=self._http_client_context,
        )
        # Compression decision + advertised codecs captured once at
        # construction — the same capture rule as relay's deferred sends: the
        # poster outlives any request scope, and re-reading managed config on
        # every streamed line would re-parse the plist per post.
        # Local import: relay imports this module (circular otherwise). The
        # module reference is stashed for per-event reads of relay's live
        # rejection state through its public accessors.
        from runlayer_cli.hook import relay

        self._relay = relay
        self._compress, self._encodings = relay.compression_policy()

    def _http_client_context(self) -> AbstractContextManager[HookHTTPClient]:
        return nullcontext(cast(HookHTTPClient, self._client))

    def _post_wire(self, wire: WireBody) -> HookHTTPResponse:
        return self._hook_client.post_target(
            "event", wire["content"], headers=wire["headers"] or None
        )

    def __call__(
        self,
        client_name: str,
        event_name: str,
        payload: dict[str, Any],
    ) -> None:
        body: dict[str, Any] = {
            "client": client_name,
            "event_name": event_name,
            "payload": payload,
        }
        relay = self._relay
        if self._org_key_mode:
            device = relay._build_device_context()
            if device is not None:
                body["device"] = device
        wrapper = json.dumps(body)
        compress = self._compress and not relay.compression_rejected()
        wire = encode_wire_body(wrapper, compress=compress, encodings=self._encodings)
        try:
            resp = self._post_wire(wire)
            if (
                wire["headers"]
                and not resp.is_success
                and resp.status_code in relay.WIRE_REJECT_STATUSES
            ):
                # Backend can't decode this codec: identity retry once, then
                # memo so the rest of this poster's life (and, in-process,
                # relay's posts) skips compression — same contract as
                # relay._post, memo only after the identity attempt succeeds.
                # relay's extra legacy-200 validation-deny sniff is absent on
                # purpose: only the cursor/enforce route converts validation
                # errors into 200 denies; the event target never does.
                resp = self._post_wire(encode_wire_body(wrapper))
                if resp.is_success:
                    relay.mark_compression_rejected()
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
            raise_for_status = getattr(resp, "raise_for_status", None)
            if callable(raise_for_status):
                raise_for_status()
            raise RuntimeError(
                f"Runlayer transcript stream post failed: HTTP {resp.status_code}"
            )

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


# Wire-contract markers on streamed provider-usage events (both the Claude and
# Codex builders); must stay in lockstep with the backend normalizer.
_PROVIDER_TOKEN_SOURCE = "provider"
_TOKEN_ORIGIN_CLIENT_TRANSCRIPT = "client_transcript"

# Anthropic per-message ``message.usage`` -> canonical flat token keys. The four
# buckets are disjoint (input is exclusive of cache), matching the backend's
# Stop-replay extraction so streamed and replayed facts agree bucket-for-bucket.
_CLAUDE_USAGE_TOKEN_FIELDS: tuple[tuple[str, str], ...] = (
    ("input_tokens", "input_tokens"),
    ("output_tokens", "output_tokens"),
    ("cache_creation_input_tokens", "cache_creation_tokens"),
    ("cache_read_input_tokens", "cache_read_tokens"),
)

# Scoped like the backend's ``_CLAUDE_TRANSCRIPT_USAGE_CLIENTS``: cowork has
# its own ApiRequest usage hook, so streaming its transcript would double-count.
_CLAUDE_USAGE_STREAM_CLIENTS = frozenset({"claude", "claude_code"})


def _claude_usage_token_event(
    session_id: str,
    timestamp: str,
    msg: dict[str, Any],
    *,
    stream_state: dict[str, Any] | None,
) -> tuple[str, dict[str, Any]] | None:
    """Stream one assistant message's provider usage as a token_count event.

    ``external_message_id`` is the provider message id — the same id the
    backend's Stop-replay extraction stamps — so streamed and replayed facts
    collapse to one message at read time. ``stream_state`` suppresses re-emits
    for the many transcript lines that repeat an id with unchanged usage.
    """
    usage = msg.get("usage")
    if not isinstance(usage, dict):
        return None
    message_id = msg.get("id")
    if not isinstance(message_id, str) or not message_id:
        return None

    counts: dict[str, int] = {}
    for source_key, dest_key in _CLAUDE_USAGE_TOKEN_FIELDS:
        value = _coerce_int(usage.get(source_key))
        if value is not None:
            counts[dest_key] = value
    if not any(counts.values()):
        return None

    snapshot = tuple(sorted(counts.items()))
    if stream_state is not None:
        seen_usage = stream_state.setdefault("claude_usage_seen", {})
        if seen_usage.get(message_id) == snapshot:
            return None
        seen_usage[message_id] = snapshot
        if len(seen_usage) > max(1, _TRANSCRIPT_DEDUPE_MAX_ENTRIES):
            del seen_usage[next(iter(seen_usage))]

    payload: dict[str, Any] = {
        "session_id": session_id,
        "timestamp": timestamp,
        "token_source": _PROVIDER_TOKEN_SOURCE,
        "token_origin": _TOKEN_ORIGIN_CLIENT_TRANSCRIPT,
        "external_message_id": message_id,
        **counts,
    }
    model = msg.get("model")
    if isinstance(model, str) and model:
        payload["model"] = model
    return ("message.token_count", payload)


# Codex rollout (nested OpenAI-style) -> canonical flat token keys the backend
# normalizer understands. cached_input is a subset of input and reasoning_output a
# subset of output, so the buckets aren't disjoint; the backend keeps the provider
# total and excludes Codex from the disjoint-bucket rollup.
_CODEX_TOKEN_FIELDS: tuple[tuple[str, str], ...] = (
    ("input_tokens", "input_tokens"),
    ("output_tokens", "output_tokens"),
    ("reasoning_output_tokens", "reasoning_tokens"),
    ("cached_input_tokens", "cache_read_tokens"),
    ("total_tokens", "total_tokens"),
)


def _token_count_event(
    session_id: str,
    timestamp: str,
    msg: dict[str, Any],
    *,
    model: str | None = None,
) -> tuple[str, dict[str, Any]] | None:
    """Forward one Codex rollout ``token_count`` line as a provider-usage event.

    Codex records usage only in the rollout, never the Stop payload. We emit the
    per-turn ``last_token_usage`` delta (deltas sum to the session total) with a
    stable ``external_message_id`` (the cumulative total, which grows monotonically)
    so backfilled re-deliveries dedupe on the backend instead of double counting.

    ``model`` is the active turn_context model (Codex omits it from the usage
    line); stamping it must stay in lockstep with the backend Stop-replay closure
    so the streamed and backfilled facts share a dedupe key.
    """
    info = msg.get("info")
    if not isinstance(info, dict):
        return None
    delta = info.get("last_token_usage")
    if not isinstance(delta, dict):
        return None

    payload: dict[str, Any] = {
        "session_id": session_id,
        "timestamp": timestamp,
        "token_source": _PROVIDER_TOKEN_SOURCE,
        "token_origin": _TOKEN_ORIGIN_CLIENT_TRANSCRIPT,
        "external_message_id": _token_count_message_id(session_id, info),
    }
    if model:
        payload["model"] = model
    for source_key, dest_key in _CODEX_TOKEN_FIELDS:
        value = _coerce_int(delta.get(source_key))
        if value is not None:
            payload[dest_key] = value
    if not any(dest_key in payload for _, dest_key in _CODEX_TOKEN_FIELDS):
        return None
    return ("message.token_count", payload)


def _token_count_message_id(session_id: str, info: dict[str, Any]) -> str:
    # Must produce identical IDs to its counterpart `_codex_token_message_id` in
    # backend/app/domains/sessions/normalization.py so the streamed and inline
    # Stop-fallback usage facts share an external_message_id and dedupe to one.
    cumulative = info.get("total_token_usage")
    marker: Any = None
    if isinstance(cumulative, dict):
        marker = cumulative.get("total_tokens")
    if marker is None:
        marker = json.dumps(info, sort_keys=True, separators=(",", ":"), default=str)
    return f"codex-token-count:{session_id}:{marker}"


def _coerce_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


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
