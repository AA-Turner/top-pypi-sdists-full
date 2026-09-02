"""HTTP relay for hook enforcement and event forwarding (runs in-process)."""

from __future__ import annotations

import contextlib
import json
import math
import os
import random
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Callable, Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, cast

import httpx
from runlayer_sdk.hook_transport import (
    API_KEY_HEADER_NAME,
    HOOK_RELAY_TARGETS,
    HookAPIClient,
    HookHTTPClient,
    HookHTTPClientFactory,
    encode_wire_body,
)

from runlayer_cli import flow_spool, flow_trace
from runlayer_cli.api import USER_AGENT
from runlayer_cli.config import load_config, normalize_url, persist_credentials
from runlayer_cli.hook.failure import (
    FailureContext,
    _classify_network_failure,
    _safe_wire_size,
)
from runlayer_cli.enrollment import (
    EnrollmentError,
    exchange_enrollment_key,
    write_enrollment_marker,
)
from runlayer_cli.hook import TRANSCRIPT_STREAM_WORKER_SENTINEL, hook_io
from runlayer_cli.hook.transcript_stream import (
    _buffer_is_complete_json_line,
    _first_string,
    claim_transcript_stream,
    clear_transcript_stream_active,
    clear_transcript_stream_claim,
    clear_transcript_stream_completed,
    is_transcript_stream_active,
    is_transcript_stream_claim_in_progress,
    is_transcript_stream_claimed,
    is_transcript_stream_recently_completed,
    iter_transcript_sent_states,
    load_sent_state_for,
    resolve_transcript_path,
    store_transcript_sent_state,
    transcript_start_offset,
)
from runlayer_cli.mdm_config import ManagedConfig, read_managed_config
from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.tls import http_client

_TRANSCRIPT_STREAM_CLIENTS = frozenset({"claude_code", "codex"})

_DEBUG_DIR = Path(tempfile.gettempdir())

_ENROLLMENT_COOLDOWN_SECONDS = 60.0
_ENROLLMENT_ATTEMPT_FILENAME = ".enrollment-attempt"

# In-memory re-entry guard for `_try_lazy_enrollment`. The cooldown touch file
# is the cross-process guard, but it shares a failure domain with `save_config`
# (read-only fs, missing dir): if both writes fail, the post-success
# `forward_event` -> `_forward_post` -> `_load_credentials` chain would loop
# straight back here. This flag breaks the chain regardless of disk state.
_lazy_enrollment_in_progress = False

_shared_http_client_provider: Callable[[], httpx.Client] | None = None


class CredentialCache(Protocol):
    """Daemon-owned credential cache used only by long-lived hook processes."""

    def get(
        self,
        loader: Callable[[], tuple[str, str]],
    ) -> tuple[str, str]: ...

    def invalidate(self) -> None: ...


_credential_cache: CredentialCache | None = None

# Daemon-owned deferred sender for best-effort telemetry POSTs. Payload state is
# finalized synchronously, then only the network send is queued off the blocking
# hook path. Seam absent (inline ``aiwatch hook``) means synchronous delivery.
DeferredEventSender = Callable[[Callable[[], None]], bool]

_deferred_event_sender: DeferredEventSender | None = None


# Flow step name per relay target (flow_trace.CLIENT_FLOW_STEPS contract).
_FLOW_STEP_BY_TARGET = {
    "enforce": "enforce",
    "tool-pre": "tool_pre",
    "tool-post": "tool_post",
    "event": "event_post",
}


# Kinds where the request body plausibly contributed, so the failure path pays
# the O(n) encode to report its size. connect/unclassified never render size.
_SIZE_RELEVANT_KINDS: frozenset[str] = frozenset(
    {"upload_timeout", "upload_failed", "timeout"}
)

# Idempotency key for tool lifecycle POSTs (ENG-5112): one uuid4 per hook
# invocation, constant across the retry attempts of that invocation, so the
# backend can dedupe a replayed tool-post. Additive — the backend ignores
# unknown headers today.
IDEMPOTENCY_KEY_HEADER_NAME = "x-runlayer-idempotency-key"

# enforce (/hooks/cursor) rides along: its retries include the
# response-lost class (a duplicate pre-check is harmless, same stance as
# tool-pre), but that endpoint emits audit-log/device events, so the
# additive key lets backend dedupe cover replays for free when it lands.
_IDEMPOTENT_TARGETS = frozenset({"tool-pre", "tool-post", "enforce"})

# Retry policy for the enforcement/tool POSTs (ENG-5112). The 5s `event`
# target is fire-and-forget and gets no retries — its cheapness is the
# feature. RUNLAYER_HOOK_RETRIES=0 is the kill switch.
_DEFAULT_MAX_RETRIES = 2
_RETRY_BACKOFF_BASE_S = (0.2, 1.0)
# Never start an attempt with less than this much of the overall budget left:
# it could not plausibly finish, and the fail-closed deny would just land later.
_MIN_ATTEMPT_BUDGET_S = 2.0
_CONNECT_TIMEOUT_S = 3.0
# Wall cap on the retried enforcement POSTs. The tightest harness kill ceiling
# is Goose's 30s PreToolUse default (see the ENG-5116 hook-path
# timeout-budget decision record): the
# CLI must give up and emit its explicit deny before any harness kills the
# hook, or timeout handling turns fail-open (Cursor). 28s keeps ~2s of
# headroom for dispatch and deny rendering.
_MAX_WALL_BUDGET_S = 28.0

# Exception types that prove the request never reached the backend: no
# connection was acquired (connect/pool) or the request body never finished
# sending (write). Retrying these can never double-apply a non-idempotent
# request.
_UNSENT_REQUEST_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.PoolTimeout,
    httpx.WriteError,
    httpx.WriteTimeout,
)


def _max_retries() -> int:
    """Retries allowed after the first attempt (0..2). Absent/garbage env
    means the default; the documented kill switch is RUNLAYER_HOOK_RETRIES=0."""
    raw = hook_io.getenv("RUNLAYER_HOOK_RETRIES")
    if raw is None:
        return _DEFAULT_MAX_RETRIES
    try:
        return max(0, min(int(raw), _DEFAULT_MAX_RETRIES))
    except ValueError:
        return _DEFAULT_MAX_RETRIES


def _retryable_status(status_code: int, target: str) -> bool:
    """5xx and 429 are transient by contract; every other 4xx is a definitive
    answer (policy deny, bad request, bad credentials) — never retry those.

    ``tool-post`` gets no status retries at all: any response proves the
    request arrived, and the backend does not dedupe tool-posts yet, so a
    replay could double-record the tool result. Remove this carve-out (fall
    through to the shared rule) once the backend dedupes on
    IDEMPOTENCY_KEY_HEADER_NAME — the header already ships on every attempt.
    """
    if target == "tool-post":
        return False
    return status_code == 429 or status_code >= 500


def _retryable_exception(exc: Exception, target: str) -> bool:
    """httpx.TransportError covers connect/DNS/TLS failures, timeouts, and
    dropped connections. Anything else (serialization bugs, MemoryError) is
    not a network condition; retrying would mask it.

    ``tool-post`` only retries failures that prove the request never arrived
    (_UNSENT_REQUEST_EXCEPTIONS): a read timeout/reset may mean the backend
    already recorded the tool result, and a replay would double-apply it.
    Terminal there until backend idempotency-key dedupe exists (see
    ``_retryable_status``)."""
    if target == "tool-post":
        return isinstance(exc, _UNSENT_REQUEST_EXCEPTIONS)
    return isinstance(exc, httpx.TransportError)


def _attempt_timeout(remaining: float) -> httpx.Timeout:
    """One attempt gets the full remaining wall budget: connect fails fast
    (so a dead network leaves budget for retries) and read/write get
    everything left after connect. Splitting the budget evenly across
    attempts starved slow-but-succeeding uploads (10–25s observed today)
    into fresh denies; total time is bounded by the deadline checks around
    retries, not by per-attempt rationing."""
    connect = min(_CONNECT_TIMEOUT_S, remaining)
    read_write = max(remaining - connect, _MIN_ATTEMPT_BUDGET_S)
    return httpx.Timeout(
        connect=connect,
        read=read_write,
        write=read_write,
        pool=connect,
    )


def _retry_after_seconds(resp: Any) -> float | None:
    """Numeric ``Retry-After`` in seconds, or None when absent/unparseable
    (the HTTP-date form is deliberately not honored — budgets here are tens
    of seconds and clock skew would dwarf them)."""
    headers = getattr(resp, "headers", None)
    if headers is None:
        return None
    raw = headers.get("Retry-After")
    if raw is None:
        return None
    try:
        seconds = float(str(raw).strip())
    except ValueError:
        return None
    # float() accepts "nan"/"inf": NaN slips past every comparison guard
    # (IEEE 754) all the way into time.sleep(nan) -> ValueError, so both are
    # "unparseable" for budget arithmetic.
    if not math.isfinite(seconds) or seconds < 0:
        return None
    return seconds


def _sleep_before_retry(attempt: int, deadline: float) -> bool:
    """Back off (~0.2s then ~1s, jittered) before the next attempt. False when
    the budget left after sleeping would be under _MIN_ATTEMPT_BUDGET_S — the
    caller then gives up with the failure it already has."""
    base = _RETRY_BACKOFF_BASE_S[min(attempt - 1, len(_RETRY_BACKOFF_BASE_S) - 1)]
    delay = base * (0.75 + random.random() * 0.5)
    if deadline - time.monotonic() - delay < _MIN_ATTEMPT_BUDGET_S:
        return False
    time.sleep(delay)
    return True


class RelayError(Exception):
    """Raised when the relay POST fails. ``exit_code``: 1 = no creds, 2 = HTTP/network.

    ``failure`` (optional) lets the deny message say *what* failed instead of
    one opaque string for every mode; see ``FailureContext``.
    """

    def __init__(
        self,
        exit_code: int,
        detail: str = "",
        body: str = "",
        *,
        failure: FailureContext | None = None,
    ) -> None:
        self.exit_code = exit_code
        self.detail = detail
        self.body = body
        self.failure = failure
        super().__init__(detail)


# Process-wide memo: the backend rejected a compressed body this run (e.g. a
# pre-gzip backend behind an already-flipped GzipHooks flag, or a backend
# that mis-advertised zstd). Any codec's rejection disables ALL compression
# for the process — by design: one identity fallback path, at the cost that
# a zstd-only defect also forfeits gzip until restart (the org-flag-gated
# advertisement is the fleet-level fix for that). Deliberately
# process-lifetime, not persisted: the daemon keeps it for its whole run,
# one-shot hooks re-discover it per invocation (one cheap extra round trip),
# and a backend upgrade needs no cache purge.
_compression_rejected_by_backend = False

# Statuses a backend produces for a compressed body it cannot parse (no
# decompress middleware, so the JSON layer sees raw compressed bytes): FastAPI
# yields 400/422 depending on how the route reads the body; 415 is the
# canonical unsupported-encoding answer some proxies give. 401/403 are
# credential answers and 413 would only get worse uncompressed — excluded.
_WIRE_REJECT_STATUSES = frozenset({400, 415, 422})

# Frozen wording of the legacy cursor route's fail-closed validation deny
# (backend hooks/cursor/router.py FailClosedRoute): pre-gzip backends answer
# an unparseable body on that route with HTTP 200 + permission=deny, not a
# 4xx, so the status-based fallback below never sees it.
_LEGACY_VALIDATION_DENY_MARKER = "Hook validation failed"


def _is_legacy_validation_deny(text: str) -> bool:
    if _LEGACY_VALIDATION_DENY_MARKER not in text:
        return False
    try:
        data = json.loads(text)
    except ValueError:
        return False
    return (
        isinstance(data, dict)
        and data.get("permission") == "deny"
        and _LEGACY_VALIDATION_DENY_MARKER in str(data.get("user_message", ""))
    )


def _wire_encodings() -> tuple[str, ...]:
    """Wire codecs the backend advertised via config sync, gzip when silent.

    Old backends never advertise, so absence means the pre-advertisement
    contract: gzip only. encode_wire_body picks the fastest advertised codec
    that is locally available.
    """
    encodings = read_managed_config().get("hook_wire_encodings")
    # Only ABSENCE means the legacy gzip contract. An explicit empty tuple
    # (backend advertised only codecs this client doesn't know) propagates,
    # and the encoder sends identity — never a codec the backend didn't
    # advertise.
    return ("gzip",) if encodings is None else encodings


# Public compression-policy surface for other posters (the transcript-stream
# tailer). Everything else about the memo/gate stays module-internal; external
# writers go through mark_compression_rejected so "who mutates this flag" has
# one answer per module.
WIRE_REJECT_STATUSES = _WIRE_REJECT_STATUSES


def compression_policy() -> tuple[bool, tuple[str, ...]]:
    """(compress, advertised encodings) as of now — capture, don't re-read."""
    return _gzip_hooks_enabled(), _wire_encodings()


def compression_rejected() -> bool:
    return _compression_rejected_by_backend


def mark_compression_rejected() -> None:
    global _compression_rejected_by_backend
    _compression_rejected_by_backend = True


def _gzip_hooks_enabled() -> bool:
    """Whether hook POST bodies may be gzip-compressed.

    ``RUNLAYER_HOOK_GZIP=0`` is the kill switch and always wins. Otherwise the
    managed ``GzipHooks`` boolean gates the rollout; see its entry in
    ``mdm_config._BOOL_FIELDS`` for why it defaults OFF.
    """
    if hook_io.getenv("RUNLAYER_HOOK_GZIP") == "0":
        return False
    return read_managed_config().get("gzip_hooks") is True


def set_shared_http_client_provider(
    provider: Callable[[], httpx.Client] | None,
) -> None:
    """Use a caller-owned HTTP client for hook POSTs, or restore per-POST clients."""
    global _shared_http_client_provider
    _shared_http_client_provider = provider


def set_credential_cache(cache: CredentialCache | None) -> None:
    """Install a daemon-owned credential cache, or restore direct reads."""
    global _credential_cache
    _credential_cache = cache


def set_deferred_event_sender(sender: DeferredEventSender | None) -> None:
    """Install a daemon-owned deferred telemetry sender, or restore sync POSTs."""
    global _deferred_event_sender
    _deferred_event_sender = sender


def _relay_http_client_factory() -> HookHTTPClientFactory:
    provider = _shared_http_client_provider
    if provider is None:
        return cast(HookHTTPClientFactory, http_client)

    def shared_http_client() -> contextlib.AbstractContextManager[HookHTTPClient]:
        return contextlib.nullcontext(cast(HookHTTPClient, provider()))

    return shared_http_client


def _load_credentials() -> tuple[str, str]:
    """Return (host, secret) or raise ``RelayError(1)`` (fail-closed)."""
    # Keychain/MDM reads can be slow; timed as a blocking local step (records
    # status="error" if credential loading raises).
    with flow_trace.step("credentials", kind="local", blocking=True):
        try:
            cache = _credential_cache
            if cache is not None:
                return cache.get(_load_credentials_uncached)
            return _load_credentials_uncached()
        except RelayError:
            raise
        except Exception as e:
            raise RelayError(1, f"credential load failed: {e}") from e


def _load_credentials_uncached() -> tuple[str, str]:
    config = load_config()
    managed = read_managed_config()
    raw_host = config.default_host or managed.get("host")
    if not raw_host:
        raise RelayError(1, "no default_host")
    # MDM ``Host`` skips ``set_host_credentials`` normalization; strip trailing
    # slash so ``_post`` doesn't build double-slash URLs.
    host = normalize_url(raw_host)
    # Org-key hook mode: authenticate hooks with the managed key and let the
    # backend resolve identity from device context. Per-user enrollment remains
    # the fallback when no org key is present.
    org_api_key = managed.get("org_api_key")
    if org_api_key:
        return host, org_api_key
    secret = config.get_secret_for_host(host)
    if secret:
        return host, secret
    secret = _try_lazy_enrollment(host, managed)
    if not secret:
        raise RelayError(1, "no secret for host")
    return host, secret


def _try_lazy_enrollment(host: str, managed: ManagedConfig) -> str | None:
    """Self-healing fallback (see cli/AGENTS.md); returns api_key or ``None``."""
    global _lazy_enrollment_in_progress
    if _lazy_enrollment_in_progress:
        return None
    _lazy_enrollment_in_progress = True
    try:
        return _try_lazy_enrollment_inner(host, managed)
    finally:
        _lazy_enrollment_in_progress = False


def _try_lazy_enrollment_inner(host: str, managed: ManagedConfig) -> str | None:
    enrollment_key = managed.get("enrollment_key")
    if not enrollment_key:
        return None
    if _enrollment_attempt_recently():
        return None
    _touch_enrollment_attempt()

    try:
        result = exchange_enrollment_key(
            host=host,
            enrollment_key=enrollment_key,
            username=managed.get("username"),
            device_name=managed.get("device_name"),
        )
    except EnrollmentError:
        return None

    config = load_config()
    # Only drop the enrollment marker when the secret actually persisted
    # (keychain or config.yaml). If neither persisted (keychain write failed +
    # aiwatch no-op), the next hook fire lazy-enrolls again; a marker here would
    # falsely tell the bootstrap gate this user is enrolled.
    if persist_credentials(config, host, result.api_key)["persisted"]:
        write_enrollment_marker(host)

    try:
        forward_event(
            client_name="aiwatch_hook",
            event_name="aiwatch.lazy_enrollment_fallback_hit",
            payload={
                "username": result.username,
                "device_name": result.device_name,
                "host": host,
            },
        )
    except Exception:
        pass

    return result.api_key


def _enrollment_attempt_path() -> Path:
    return get_runlayer_dir() / _ENROLLMENT_ATTEMPT_FILENAME


def _enrollment_attempt_recently() -> bool:
    path = _enrollment_attempt_path()
    try:
        mtime = path.stat().st_mtime
    except (FileNotFoundError, OSError):
        return False
    return (time.time() - mtime) < _ENROLLMENT_COOLDOWN_SECONDS


def _touch_enrollment_attempt() -> None:
    path = _enrollment_attempt_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        os.utime(path, None)
    except OSError:
        pass


def _maybe_attach_device(payload: str) -> str:
    """In org-key hook mode, add a top-level ``device`` block to the request.

    Org-key mode is active whenever MDM ships an ``OrgApiKey`` (the single AI
    Watch key). Backend resolves identity from ``device_id`` + username
    server-side. No-op (returns the payload unchanged) when there's no org key,
    so the legacy per-user path is byte-for-byte unchanged.
    """
    managed = read_managed_config()
    if not managed.get("org_api_key"):
        return payload
    try:
        obj = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return payload
    if not isinstance(obj, dict) or "device" in obj:
        return payload
    device = _build_device_context()
    if device is None:
        return payload
    obj["device"] = device
    return json.dumps(obj)


def _maybe_stamp_client_time(payload: str, target: str) -> str:
    """Stamp event payloads with the host send time when none is present.

    Tool events (PostToolUse etc.) reach ``/hooks/events`` over a different async
    channel than transcript-derived reasoning events, so the two can be reordered
    in transit. The backend's behavior scanner pairs a tool's output with the
    agent's following reasoning by timestamp; without a client timestamp the tool
    event falls back to server-receipt time, i.e. the already-scrambled arrival
    order. Stamping send time here — same host clock the transcript timestamps
    come from — gives the scanner a logical ordering key. Only ``event`` posts
    feed the scanner; ``setdefault`` semantics never override a timestamp the
    client already supplied.

    Contract: relay send-delay must stay well under the gap between adjacent
    agent events (seconds). A delay larger than that gap could stamp a tool
    event later than a following reasoning event and misorder the pair; in
    practice the in-process POST fires within milliseconds of the hook.
    """
    if target != "event":
        return payload
    try:
        obj = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return payload
    inner = obj.get("payload") if isinstance(obj, dict) else None
    if not isinstance(inner, dict) or inner.get("timestamp"):
        return payload
    inner["timestamp"] = datetime.now(timezone.utc).isoformat()
    return json.dumps(obj)


@contextlib.contextmanager
def _silence_device_output() -> Iterator[None]:
    if hook_io.has_request_output():
        yield
    else:
        with (
            open(os.devnull, "w") as devnull,
            contextlib.redirect_stdout(devnull),
            contextlib.redirect_stderr(devnull),
        ):
            yield


def _maybe_attach_client_flows(payload: str, target: str) -> str:
    """Piggyback spooled flow summaries on ``event`` POSTs (lag-one delivery).

    Only the fire-and-forget ``event`` target carries them — the
    latency-critical ``enforce`` / ``tool-pre`` bodies stay untouched. Returns
    the payload unchanged when tracing is disabled, the spool is empty/locked,
    or the payload isn't a JSON object.
    """
    if target != "event" or not flow_trace.is_enabled():
        return payload
    try:
        obj = json.loads(payload)
        if not isinstance(obj, dict) or "client_flows" in obj:
            return payload
        # Drain only once we know the payload can carry the envelope (a drain
        # is destructive; spooled flows would be lost on a non-dict payload).
        envelope = flow_spool.spool_drain()
        if envelope is None:
            return payload
        obj["client_flows"] = envelope
        return json.dumps(obj)
    except Exception:
        return payload


def _build_device_context() -> dict[str, Any] | None:
    """Collect device id + metadata for org-key hook requests.

    Uses the same device ID logic as scans: hardware machine ID when available
    (stable per physical device), else the persisted ``~/.runlayer/device_id``.
    This lets the backend join hook events to existing ``AIWatchUserDevice`` mappings.
    """
    try:
        # Local import: keep the scan module chain out of the legacy per-user
        # hook closure; only pay its import cost when org-key mode is active.
        from runlayer_cli.scan.device import (
            get_device_metadata,
            get_or_create_device_id,
        )

        # Inline hook stdout/stderr are a strict protocol surface, so suppress
        # scan chatter there. Daemon workers use request-local writers; skipping
        # process-global redirects prevents concurrent workers stealing streams.
        with flow_trace.step("device_context", kind="local"):
            with _silence_device_output():
                metadata = get_device_metadata()
                device_id = get_or_create_device_id()
        managed = read_managed_config()
        device: dict[str, Any] = {
            "device_id": device_id,
            "hostname": managed.get("device_name") or metadata.get("hostname"),
            "os": metadata.get("os"),
            "os_version": metadata.get("os_version"),
            "username": managed.get("username") or metadata.get("username"),
            "serial_number": metadata.get("serial_number"),
        }
        if metadata.get("is_wsl"):
            device["is_wsl"] = True
        return device
    except Exception as exc:
        # Org-key mode relies on this block for server-side device attribution.
        # On failure the hook still 200s but identity degrades to buffer/park
        # with nothing visible client-side. This is a soft degradation, not a
        # hook error, so only surface the cause (type/message, no secrets) when
        # RUNLAYER_HOOK_DEBUG is set — an unconditional stderr write is what
        # clients flag as a failed hook invocation.
        if hook_io.getenv("RUNLAYER_HOOK_DEBUG") == "1":
            with contextlib.suppress(Exception):
                hook_io.write_stderr(
                    f"aiwatch: device context unavailable for org-key hook: "
                    f"{type(exc).__name__}: {exc}\n"
                )
        return None


def _finalize_payload(payload: str, target: str) -> str:
    """Apply the schedule-time payload mutators (device context, client-time
    stamp, client_flows drain). Runs on the hook path even for deferred sends
    so the stamped timestamp keeps the behavior scanner's ordering key and the
    spool drain keeps its lag-one delivery semantics.

    ``mcp-usage`` is metadata-only: ``forward_mcp_usage_metadata`` builds its
    own closed device block (``device_id``/``username``), and the full device
    context (hostname, serial number, os, ...) must never ride this target —
    the backend schema rejects it, and silently attaching it would break the
    feature's only-identity-leaves-the-host contract. Gate here structurally
    rather than relying on the payload already carrying a ``device`` key.
    """
    if target != "mcp-usage":
        payload = _maybe_attach_device(payload)
    payload = _maybe_stamp_client_time(payload, target)
    payload = _maybe_attach_client_flows(payload, target)
    return payload


def _post(
    host: str,
    secret: str,
    payload: str,
    *,
    target: str,
    timeout: int | None = None,
    debug: bool = False,
    prepared: bool = False,
    compress: bool | None = None,
    encodings: tuple[str, ...] | None = None,
) -> str:
    global _compression_rejected_by_backend
    spec = HOOK_RELAY_TARGETS[target]
    url = f"{host}{spec.endpoint}"
    if not prepared:
        payload = _finalize_payload(payload, target)
    # Encode the wire body once, here — encode_wire_body is the single
    # compression entry point: telemetry below must record the size actually
    # sent (compressed when compression fires), and re-compressing to measure
    # it would double the CPU cost. bytes pass through post_target untouched.
    # Encode failures (MemoryError on the UTF-8 copy or gzip of a multi-MB
    # body) must still surface as RelayError: dispatch only converts
    # RelayError into the explicit deny, and anything else would crash the
    # hook fail-open (same contract as
    # test_encode_failure_still_raises_relay_error_fail_closed).
    # ``compress`` lets a caller capture the compression decision on the
    # request thread and thread it through: deferred sends run on the daemon's
    # queue worker thread, outside the request-scoped ``hook_io`` ContextVar, so
    # a send-time ``_gzip_hooks_enabled()`` re-read would miss the client's
    # ``RUNLAYER_HOOK_GZIP=0`` kill switch. None ⇒ read env now (the
    # synchronous path, unchanged).
    should_compress = _gzip_hooks_enabled() if compress is None else compress
    if _compression_rejected_by_backend:
        should_compress = False
    # Same request-thread capture rule as ``compress``: deferred sends thread
    # the advertised codec set through, None means read managed config now.
    wire_encodings = _wire_encodings() if encodings is None else encodings
    try:
        wire = encode_wire_body(
            payload, compress=should_compress, encodings=wire_encodings
        )
    except Exception as exc:
        raise RelayError(2, "network error", failure=FailureContext()) from exc
    # The fallback must key on what actually went on the wire, not the gate:
    # encode_wire_body only compresses bodies over its threshold, and an
    # identity body that 4xxs proves nothing about codec support. Any codec
    # counts — a backend that mis-advertised zstd degrades identically.
    sent_compressed = "Content-Encoding" in wire["headers"]
    headers = {
        API_KEY_HEADER_NAME: secret,
        "User-Agent": USER_AGENT,
        **wire["headers"],
    }
    # Idempotency key rides the request, not the payload, so it is set even
    # when the caller pre-finalized the body (prepared=True). Constant across
    # retry attempts of one invocation; lets the backend dedupe replays.
    if target in _IDEMPOTENT_TARGETS:
        headers[IDEMPOTENCY_KEY_HEADER_NAME] = str(uuid.uuid4())
    client = HookAPIClient(
        host,
        headers=headers,
        http_client_factory=_relay_http_client_factory(),
    )
    # The event target stays single-attempt with its caller-provided/5s
    # timeout (fire-and-forget must stay cheap); enforcement/tool targets
    # retry transient failures within one overall wall budget, capped at
    # _MAX_WALL_BUDGET_S so the CLI gives up before the tightest harness
    # hook ceiling.
    max_retries = 0 if target == "event" else _max_retries()
    budget = min(
        float(timeout if timeout is not None else spec.timeout),
        _MAX_WALL_BUDGET_S,
    )
    deadline = time.monotonic() + budget
    attempt = 0
    resp = None
    started = time.perf_counter()
    # Wire size of the request body (UTF-8, post-compression when compressed),
    # so the backend can split slow-transfer failures into large-payload vs
    # slow-connection. A count only; content stays out of flow
    # summaries. Computed only inside an active flow: the str encode is an
    # O(n) copy of a potentially multi-MB body, and the kill-switch/no-flow
    # hot path must stay free of tracing overhead (flow_trace.step docstring
    # contract). A compressed body is already bytes, so sizing it is O(1).
    payload_bytes = (
        _safe_wire_size(wire["content"])
        if flow_trace.current_flow() is not None
        else None
    )
    try:
        with flow_trace.step(
            _FLOW_STEP_BY_TARGET.get(target, "event_post"),
            kind="http",
            payload_bytes=payload_bytes,
        ):
            last_exc: Exception | None = None
            while True:
                if (
                    max_retries
                    and attempt
                    and deadline - time.monotonic() < _MIN_ATTEMPT_BUDGET_S
                ):
                    # Budget ran out between backoff and dispatch (slow sleep
                    # wakeup, scheduler stall): give up with the failure
                    # already in hand instead of starting a doomed attempt.
                    if last_exc is not None:
                        raise last_exc
                    if resp is not None:
                        break
                attempt += 1
                resp = None
                if max_retries == 0:
                    # No-retry path (event target or kill switch): identical
                    # wire behavior to the pre-retry relay.
                    attempt_timeout: int | httpx.Timeout | None = timeout
                else:
                    attempt_timeout = _attempt_timeout(deadline - time.monotonic())
                try:
                    resp = client.post_target(
                        target, wire["content"], timeout=attempt_timeout
                    )
                except Exception as exc:
                    # Fail-closed: exhausted/non-retryable failures re-raise
                    # into the RelayError conversion below with this attempt's
                    # context intact.
                    if (
                        attempt > max_retries
                        or not _retryable_exception(exc, target)
                        or not _sleep_before_retry(attempt, deadline)
                    ):
                        raise
                    last_exc = exc
                    continue
                # This response supersedes any earlier transport error: if the
                # deadline check above fires before the next attempt, the
                # terminal RelayError must reflect this attempt's HTTP status,
                # not a stale exception from a prior attempt.
                last_exc = None
                if resp.is_success or not _retryable_status(resp.status_code, target):
                    break
                if attempt > max_retries:
                    break
                if resp.status_code == 429:
                    # Rate limiting is only worth retrying on the server's own
                    # schedule: honor a numeric Retry-After that still leaves
                    # room for an attempt; otherwise the 429 is terminal.
                    retry_after = _retry_after_seconds(resp)
                    if retry_after is None or (
                        deadline - time.monotonic() - retry_after
                        < _MIN_ATTEMPT_BUDGET_S
                    ):
                        break
                    time.sleep(retry_after)
                    continue
                if not _sleep_before_retry(attempt, deadline):
                    break
        _maybe_debug(debug, target, url, payload, resp)
        if not resp.is_success:
            if resp.status_code == 401 and _credential_cache is not None:
                _credential_cache.invalidate()
            remaining_budget = deadline - time.monotonic()
            if (
                sent_compressed
                and resp.status_code in _WIRE_REJECT_STATUSES
                and remaining_budget >= _MIN_ATTEMPT_BUDGET_S
            ):
                # A backend without gzip support answers a compressed body
                # with a parse rejection. Fall back to identity once:
                # without this, a GzipHooks flag flipped ahead of a backend
                # upgrade turns every hook call into a fail-closed deny.
                # The retry spends what is LEFT of this invocation's wall
                # budget, never a fresh one — a slow compressed upload plus
                # a fresh 28s identity attempt would blow past the ~30s
                # harness hook ceiling and get the hook killed instead of a
                # clean deny. With no room left, the deny below stands.
                # Memo only after the identity attempt succeeds — if it
                # fails too (genuinely malformed payload, and it raises
                # there), gzip was never proven the cause and the daemon
                # must not silently drop compression until restart.
                identity_text = _post(
                    host,
                    secret,
                    payload,
                    target=target,
                    timeout=max(int(remaining_budget), 1),
                    debug=debug,
                    prepared=True,
                    compress=False,
                )
                _compression_rejected_by_backend = True
                return identity_text
            raise RelayError(
                2,
                f"HTTP {resp.status_code}",
                body=resp.text,
                failure=FailureContext(
                    kind="http",
                    status_code=resp.status_code,
                    elapsed_s=time.perf_counter() - started,
                    attempts=attempt,
                ),
            )
        remaining_budget = deadline - time.monotonic()
        if (
            sent_compressed
            and remaining_budget >= _MIN_ATTEMPT_BUDGET_S
            and _is_legacy_validation_deny(resp.text)
        ):
            # Legacy cursor backends convert the unparseable-body validation
            # error into an HTTP 200 deny instead of a 4xx. Retry identity
            # within the REMAINING wall budget (see the 4xx fallback above);
            # memo only when the identity answer differs — an identical deny
            # means a genuine client/backend mismatch, not a gzip problem,
            # and must not disable compression.
            identity_text = _post(
                host,
                secret,
                payload,
                target=target,
                timeout=max(int(remaining_budget), 1),
                debug=debug,
                prepared=True,
                compress=False,
            )
            if not _is_legacy_validation_deny(identity_text):
                _compression_rejected_by_backend = True
            return identity_text
        return resp.text
    except RelayError:
        raise
    except Exception as exc:
        _maybe_debug(debug, target, url, payload, resp)
        kind = _classify_network_failure(exc)
        # The hot path above skips the encode when tracing is off; on failure
        # the deny message needs the size, but only for kinds that render it.
        # Reuse the traced value when present so the body is encoded at most
        # once per invocation.
        if payload_bytes is None and kind in _SIZE_RELEVANT_KINDS:
            payload_bytes = _safe_wire_size(wire["content"])
        raise RelayError(
            2,
            "network error",
            failure=FailureContext(
                kind=kind,
                payload_bytes=payload_bytes,
                elapsed_s=time.perf_counter() - started,
                attempts=attempt,
            ),
        )


def _maybe_debug(debug: bool, target: str, url: str, payload: str, resp: Any) -> None:
    if not debug:
        return
    try:
        _write_debug(target, url, payload, resp)
    except Exception:
        pass


def _write_debug(target: str, url: str, request_body: str, resp: Any) -> None:
    try:
        ts = int(time.time())
        data = {
            "timestamp": ts,
            "url": url,
            "request_body_size": len(request_body) if request_body else 0,
            "response_status": resp.status_code if resp else None,
            "response_body_size": len(resp.text) if resp else None,
        }
        path = _DEBUG_DIR / f"runlayer-relay-{target}-{ts}.json"
        path.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


def enforce(payload: str, *, debug: bool = False) -> str:
    """Synchronous POST to enforce; raises ``RelayError(1)`` (creds) or ``RelayError(2)`` (network)."""
    host, secret = _load_credentials()
    return _post(
        host,
        secret,
        payload,
        target="enforce",
        debug=debug,
    )


def forward_event(
    client_name: str,
    event_name: str,
    payload: dict,
    *,
    debug: bool = False,
    defer: bool = True,
) -> None:
    """Best-effort in-process event POST; errors swallowed.

    With the daemon's deferred sender installed (and ``defer`` true), the body
    is built synchronously but the network send is queued off the blocking
    hook path. ``defer=False`` (the Stop/transcript path) and the seam-absent
    inline hook keep the synchronous POST.
    """
    wrapper = json.dumps(
        {
            "client": client_name,
            "event_name": event_name,
            "payload": payload,
        }
    )
    if defer:
        try:
            if _defer_event_post(wrapper, debug=debug):
                return
        except Exception:
            # Best-effort like the sync path: a schedule-time failure (e.g.
            # credential load) would fail the sync POST identically.
            return
    _forward_post("event", wrapper, debug=debug)


def forward_mcp_usage_metadata(
    client_name: str,
    tool_name: str,
    mcp_server_name: str | None,
    *,
    debug: bool = False,
) -> None:
    """Best-effort MCP observation with a deliberately closed payload shape."""
    device_context = _build_device_context() or {}
    device: dict[str, str] = {}
    for key in ("device_id", "username"):
        value = device_context.get(key)
        if isinstance(value, str) and value:
            device[key] = value
    payload: dict[str, object] = {
        "client": client_name,
        # Truncate to the server schema caps: this send is best-effort with
        # all exceptions swallowed, so an oversized name would otherwise be a
        # silent 422 and the observation vanishes. Lossy-but-visible beats
        # lossy-and-invisible.
        "tool_name": tool_name[:512],
    }
    if mcp_server_name:
        payload["mcp_server_name"] = mcp_server_name[:255]
    payload["device"] = device or None
    wrapper = json.dumps(payload)
    try:
        if _defer_best_effort_post("mcp-usage", wrapper, debug=debug):
            return
    except Exception:
        return
    _forward_post("mcp-usage", wrapper, debug=debug)


def _defer_event_post(wrapper: str, *, debug: bool = False) -> bool:
    """Send an ``event`` POST via the deferred sender; True when handled.

    All payload state is materialized here, at schedule time on the hook
    thread (device context, client-time stamp, client_flows drain, credential
    resolution, gzip decision) — only the network send is deferred, so queue
    delay cannot change what the backend receives or its logical ordering key.
    The gzip decision in particular must be captured here: the send runs on the
    queue worker thread, outside the request-scoped ``hook_io`` env, so a
    send-time re-read would miss the client's ``RUNLAYER_HOOK_GZIP`` kill
    switch.

    The queued send runs on the daemon's sender thread, outside the hook
    thread's flow_trace context, so deferred sends record no ``event_post``
    step/payload_bytes in the hook flow — intended: the POST is off the flow.

    A declining sender (queue closed during flush_and_stop) still counts as
    handled: finalization already ran and the client_flows drain is
    destructive, so the finalized payload is sent synchronously here. Falling
    back to the generic re-finalizing POST would re-drain an empty spool and
    silently drop the envelope attached to the discarded payload.
    """
    return _defer_best_effort_post("event", wrapper, debug=debug)


def _defer_best_effort_post(
    target: str,
    wrapper: str,
    *,
    debug: bool = False,
) -> bool:
    """Finalize and queue a telemetry POST; return False without a sender."""
    sender = _deferred_event_sender
    if sender is None:
        return False
    host, secret = _load_credentials()
    payload = _finalize_payload(wrapper, target)
    # Resolve the gzip decision here, on the request thread, while the
    # request-scoped ``hook_io`` env (and its ``RUNLAYER_HOOK_GZIP`` kill
    # switch) is still in scope. The send runs on the queue worker thread where
    # that ContextVar is absent, so a send-time re-read would silently ignore
    # the client's kill switch.
    compress = _gzip_hooks_enabled()
    encodings = _wire_encodings()

    def send() -> None:
        with contextlib.suppress(Exception):
            _post(
                host,
                secret,
                payload,
                target=target,
                debug=debug,
                prepared=True,
                compress=compress,
                encodings=encodings,
            )

    if not sender(send):
        send()
    return True


def check_tool_lifecycle(
    target: str,
    client_name: str,
    event_name: str,
    tool_name: str,
    payload: dict,
    *,
    debug: bool = False,
    mode: str | None = None,
) -> str:
    """Synchronous POST to /tool/pre or /tool/post. Returns response text."""
    wrapper = _tool_lifecycle_wrapper(
        target, client_name, event_name, tool_name, payload, mode=mode
    )
    host, secret = _load_credentials()
    return _post(
        host,
        secret,
        wrapper,
        target=target,
        debug=debug,
    )


def forward_tool_lifecycle(
    target: str,
    client_name: str,
    event_name: str,
    tool_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> None:
    """Best-effort synchronous in-process POST to /tool/pre or /tool/post; errors swallowed."""
    wrapper = _tool_lifecycle_wrapper(
        target, client_name, event_name, tool_name, payload
    )
    _forward_post(target, wrapper, debug=debug)


def _tool_lifecycle_wrapper(
    target: str,
    client_name: str,
    event_name: str,
    tool_name: str,
    payload: dict,
    *,
    mode: str | None = None,
) -> str:
    if target not in ("tool-pre", "tool-post"):
        raise ValueError(f"Invalid tool lifecycle target: {target}")
    return json.dumps(
        {
            "client": client_name,
            "event_name": event_name,
            "tool_name": tool_name,
            "payload": payload,
            **({"mode": mode} if mode is not None else {}),
        }
    )


def _wait_for_transcript_file(transcript_path: str) -> Path:
    p = Path(transcript_path)
    if p.is_file():
        return p
    for _ in range(5):
        time.sleep(0.1)
        if p.is_file():
            break
    return p


# Per-request bound on transcript content: keeps the backend's synchronous
# normalize() and the POST body small. Chunks split on line boundaries.
_TRANSCRIPT_SEND_CHUNK_BYTES = 1024 * 1024
# Per-send bound on the unsent range: the Stop hook runs inside the client's
# hook timeout (10s POST per chunk), so catch-up must stay bounded there. The
# detached worker flush has no hook timeout and uses the higher bound.
_TRANSCRIPT_SEND_MAX_BYTES = 4 * 1024 * 1024
TRANSCRIPT_FLUSH_MAX_BYTES = 16 * 1024 * 1024
# Sent-state age past which the worker may flush it. An idle-but-live session
# can look stale (state only moves with new bytes), so the flush loop also
# checks the live active marker before touching one.
_TRANSCRIPT_STATE_STALE_SECONDS = 600.0
_TRANSCRIPT_STALE_FLUSH_LIMIT = 2


def forward_stop_event(
    client_name: str,
    event_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> None:
    """Forward a stop event, attaching unsent transcript content if available.

    The sent-state offset (shared with the stream tailer) makes the send
    incremental: only bytes not yet durably delivered go out, in line-aligned
    chunks, so token usage older than any fixed window is never dropped.
    """
    if client_name in _TRANSCRIPT_STREAM_CLIENTS and is_transcript_stream_active(
        payload
    ):
        # Live tailer owns delivery; next Stop or worker flush picks up residue.
        # Stop events stay synchronous (defer=False): the hook process/session
        # may be ending, so delivery must not depend on a queue drain.
        forward_event(client_name, event_name, payload, debug=debug, defer=False)
        return

    transcript_path = (
        payload.get("transcript_path") or hook_io.getenv("CURSOR_TRANSCRIPT_PATH") or ""
    )
    if transcript_path.startswith("~"):
        transcript_path = str(Path.home()) + transcript_path[1:]

    sent = False
    if transcript_path:
        with flow_trace.step("transcript_read", kind="local", blocking=True):
            p = _wait_for_transcript_file(transcript_path)
            if p.is_file():
                sent = send_unsent_transcript(
                    client_name, event_name, payload, p, debug=debug
                )
    if not sent:
        forward_event(client_name, event_name, payload, debug=debug, defer=False)


def send_unsent_transcript(
    client_name: str,
    event_name: str,
    payload: dict,
    path: Path,
    *,
    max_bytes: int = _TRANSCRIPT_SEND_MAX_BYTES,
    debug: bool = False,
) -> bool:
    """POST the transcript bytes past the sent-offset as stop-event chunks.

    The chunk posts ARE the stop event. The POST must stay the raising variant
    (never the swallowing ``_forward_post``) and the offset is persisted only
    per delivered chunk — else a failed send would advance the offset and lose
    the range permanently. Returns True when at least one chunk delivered;
    undelivered ranges retry on the next Stop or worker flush.
    """
    try:
        size = path.stat().st_size
    except OSError:
        return False

    sent_state = load_sent_state_for(payload, path)
    offset = sent_state["offset"] if sent_state else 0
    model = sent_state["model"] if sent_state else None
    if offset > size:
        # The file was rotated/truncated: resend from 0; backend message-id
        # dedupe absorbs the overlap.
        offset = 0
    if offset >= size:
        return False

    skipped_forward = False
    if size - offset > max_bytes:
        # Deliberately skip the oldest bytes rather than blow the hook timeout.
        offset = size - max_bytes
        skipped_forward = True

    try:
        with path.open("rb") as f:
            f.seek(offset)
            data = f.read(size - offset)
    except OSError:
        return False

    if skipped_forward:
        newline = data.find(b"\n")
        if newline == -1:
            return False
        data = data[newline + 1 :]
        offset += newline + 1

    # Defer a trailing line still being written — sending it would parse as
    # garbage and advancing past it would orphan its complete form. A complete
    # but unterminated final JSON line is kept.
    last_newline = data.rfind(b"\n")
    tail = data[last_newline + 1 :]
    if tail and not _buffer_is_complete_json_line(
        tail.decode("utf-8", errors="replace")
    ):
        if last_newline == -1:
            return False
        data = data[: last_newline + 1]
    if not data:
        return False

    sent = False
    position = offset
    for chunk in _iter_line_chunks(data, _TRANSCRIPT_SEND_CHUNK_BYTES):
        text = chunk.decode("utf-8", errors="replace")
        if client_name == "codex" and model:
            # Chunk boundaries can cut off the turn_context line carrying the
            # active model; re-seed it in the rollout's own vocabulary so the
            # backend replay needs no schema change.
            seed = json.dumps({"type": "turn_context", "payload": {"model": model}})
            text = seed + "\n" + text
        wrapper = json.dumps(
            {
                "client": client_name,
                "event_name": event_name,
                "payload": payload,
                "transcript": text,
            }
        )
        try:
            _forward_post_strict("event", wrapper, timeout=10, debug=debug)
        except Exception:
            break
        position += len(chunk)
        if client_name == "codex":
            model = _last_turn_context_model(chunk) or model
        store_transcript_sent_state(
            payload,
            client=client_name,
            transcript_path=path,
            offset=position,
            model=model,
        )
        sent = True
    return sent


def _iter_line_chunks(data: bytes, chunk_bytes: int) -> "list[bytes]":
    """Split on line boundaries, at most ~chunk_bytes each (a single oversized
    line extends its chunk to the next newline or EOF)."""
    chunks: list[bytes] = []
    start = 0
    total = len(data)
    while start < total:
        end = min(start + chunk_bytes, total)
        if end < total:
            cut = data.rfind(b"\n", start, end + 1)
            if cut == -1:
                overflow = data.find(b"\n", end)
                cut = total - 1 if overflow == -1 else overflow
            end = cut + 1
        chunks.append(data[start:end])
        start = end
    return chunks


def _last_turn_context_model(chunk: bytes) -> str | None:
    """Model of the last turn_context line in the chunk, scanning backwards so
    a chunk with many turn_context lines parses only the one that matters."""
    for line in reversed(chunk.splitlines()):
        if b'"turn_context"' not in line:
            continue
        try:
            entry = json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(entry, dict) or entry.get("type") != "turn_context":
            continue
        raw_msg = entry.get("payload") or entry.get("item") or entry
        if isinstance(raw_msg, dict):
            model = _first_string(raw_msg, ("model",))
            if model:
                return model
    return None


def flush_stale_transcript_sent_states(
    client_name: str,
    *,
    exclude_session_id: str,
    debug: bool = False,
) -> int:
    """Recover transcripts whose session died without a final Stop, from the
    detached stream worker (never the hook hot path) — otherwise a killed
    session's last unsent window is lost permanently. Bounded per run;
    fully-sent stale states are pruned."""
    flushed = 0
    for state_path, state in iter_transcript_sent_states():
        if flushed >= _TRANSCRIPT_STALE_FLUSH_LIMIT:
            break
        if state.get("client") != client_name:
            continue
        session_id = state.get("session_id")
        if not isinstance(session_id, str) or not session_id:
            continue
        if session_id == exclude_session_id:
            continue
        try:
            age = time.time() - state_path.stat().st_mtime
        except OSError:
            continue
        if age < _TRANSCRIPT_STATE_STALE_SECONDS:
            continue
        transcript_path = state.get("path")
        if not isinstance(transcript_path, str) or not transcript_path:
            continue
        stale_payload = {
            "session_id": session_id,
            "transcript_path": transcript_path,
        }
        # Idle sessions stop persisting new bytes, so mtime alone can't
        # distinguish dead from idle; a live tailer keeps the active marker
        # fresh even while idle — leave those sessions alone.
        if is_transcript_stream_active(stale_payload):
            continue
        p = Path(transcript_path)
        if not p.is_file():
            with contextlib.suppress(OSError):
                state_path.unlink()
            continue
        sent_state = load_sent_state_for(stale_payload, p)
        try:
            fully_sent = sent_state is not None and (
                sent_state["offset"] >= p.stat().st_size
            )
        except OSError:
            continue
        if fully_sent:
            with contextlib.suppress(OSError):
                state_path.unlink()
            continue
        try:
            if send_unsent_transcript(
                client_name,
                "Stop",
                stale_payload,
                p,
                max_bytes=TRANSCRIPT_FLUSH_MAX_BYTES,
                debug=debug,
            ):
                flushed += 1
        except Exception:
            # Backend unreachable; a later worker run retries.
            break
    return flushed


def _start_transcript_stream_reaper(proc: Any) -> None:
    try:
        wait = getattr(proc, "wait", None)
    except Exception:
        return
    if not callable(wait):
        return

    def reap() -> None:
        with contextlib.suppress(Exception):
            wait()

    try:
        threading.Thread(target=reap, daemon=True).start()
    except Exception:
        pass


def start_transcript_stream(
    client_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> bool:
    """Start a detached transcript tailer for prompt turns with transcript JSONL."""
    if client_name not in _TRANSCRIPT_STREAM_CLIENTS:
        return False
    if resolve_transcript_path(payload) is None:
        return False
    completed_recently = is_transcript_stream_recently_completed(payload)
    if completed_recently:
        clear_transcript_stream_completed(payload)
    elif is_transcript_stream_active(payload):
        return True

    claim_token = claim_transcript_stream(payload)
    if claim_token is None:
        return is_transcript_stream_claim_in_progress(
            payload
        ) or is_transcript_stream_claimed(payload)

    start_offset = transcript_start_offset(payload)
    wrapper = json.dumps(
        {
            "client": client_name,
            "payload": payload,
            "start_offset": start_offset,
            "claim_token": claim_token,
        }
    )
    if getattr(sys, "frozen", False):
        args = [sys.executable, TRANSCRIPT_STREAM_WORKER_SENTINEL]
    else:
        args = [
            sys.executable,
            "-m",
            "runlayer_cli.hook._transcript_stream_worker",
        ]
    if debug:
        args.append("--debug")

    kwargs: dict[str, Any] = {
        "stdin": subprocess.PIPE,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "close_fds": True,
    }
    if sys.platform != "win32":
        kwargs["start_new_session"] = True
    else:
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        kwargs["creationflags"] = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP

    stdin = None
    try:
        proc = subprocess.Popen(args, **kwargs)
        _start_transcript_stream_reaper(proc)
        stdin = proc.stdin
        if stdin is None:
            raise OSError("transcript worker stdin unavailable")
        stdin.write(wrapper.encode("utf-8"))  # ty: ignore[no-matching-overload]
        stdin.close()
    except Exception:
        if stdin is not None:
            with contextlib.suppress(Exception):
                stdin.close()
        clear_transcript_stream_active(payload)
        clear_transcript_stream_claim(payload, claim_token)
        return False
    return True


def _forward_post(
    target: str,
    wrapper: str,
    *,
    timeout: int | None = None,
    debug: bool = False,
) -> None:
    """Best-effort fire-and-forget POST; errors swallowed."""
    try:
        _forward_post_strict(target, wrapper, timeout=timeout, debug=debug)
    except Exception:
        pass


def _forward_post_strict(
    target: str,
    wrapper: str,
    *,
    timeout: int | None = None,
    debug: bool = False,
) -> None:
    """POST that raises on failure. Callers that track delivery state (the
    transcript chunk sender) need the error; everything else uses the
    swallowing ``_forward_post``."""
    host, secret = _load_credentials()
    _post(
        host,
        secret,
        wrapper,
        target=target,
        timeout=timeout,
        debug=debug,
    )
