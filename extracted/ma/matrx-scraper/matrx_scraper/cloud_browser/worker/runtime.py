"""BrowserWorker — the S2 worker runtime.

One process, one persistent Chromium profile, one run. The eight S2 operations are
async methods on this object taking the typed request models and returning the
typed response models; a thin HTTP layer (future) would wrap these one-for-one, but
the operations ARE the contract and are driven directly by the control plane —
``StubControlPlane`` in tests, the real Browser Manager in production. That is what
makes the worker fully testable with zero Browser Manager, zero DB, zero streaming.

What this runtime owns:
  * ``launch_persistent_context`` against the mounted user-data dir, with the D-5
    keyring-free cookie scheme (``--password-store=basic``) and the egress guard
    installed on the CONTEXT before the first page (reusing url_guard verbatim);
  * the ONE ordered command queue (concurrency 1) with fencing-token + sequence +
    replay verification;
  * the two run modes (headed-on-Xvfb ``handoff_capable`` / headless
    ``automation_only``);
  * page/popup/dialog/download tracking over ``context.pages`` and reconciliation
    after a human episode;
  * the controller lifecycle machine and its drain-then-transition ordering;
  * the reverse event channel;
  * the checkpoint hook (WS-3 owns the crypto/upload; the worker closes cleanly,
    archives, hashes, and zeroizes).

What it never holds (S2 §2.4): no DB/KMS/Vault key, no broad storage credential, no
``user_id``/``organization_id``/credential/stream ticket. Human identity reaches it
only as ``controller_ref``.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import logging
import os
import shutil
import tarfile
import tempfile
import uuid
import xml.etree.ElementTree as ET
from collections import OrderedDict
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx

from matrx_scraper.ai_browser import actions as A
from matrx_scraper.ai_browser.session import BrowserSession, BrowserSessionManager
from matrx_scraper.ai_browser.url_guard import guard_proxy, install_egress_guard
from matrx_scraper.utils.proxy import playwright_proxy
from matrx_scraper.cloud_browser.profile_archive_policy import (
    is_profile_archive_path_excluded as _checkpoint_path_is_excluded,
)
from matrx_scraper.cloud_browser.worker import commands as C
from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.auth import TokenVerifier
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError
from matrx_scraper.cloud_browser.worker.identity import (
    IGNORED_DEFAULT_ARGS,
    STEALTH_ARGS,
    BrowserIdentity,
    resolve_identity,
    webgl_init_script,
)
from matrx_scraper.cloud_browser.worker.profile_lock import ProfileLock, ProfileLockError
from matrx_scraper.cloud_browser.worker.sanitize import (
    cap_label,
    host_of,
    origin_of,
    safe_url,
    sanitize_selector_shape,
)

logger = logging.getLogger(__name__)

_PROFILE_CHECKPOINT_MARKER = ".matrx-checkpoint-hash"
#: Written the moment Chromium launches on a profile directory: the hash of the
#: checkpoint that directory descends from ("" when it started empty). The
#: profile lives on shared EFS and outlives the task; a later worker restoring
#: the SAME checkpoint finds this marker and adopts the directory instead of
#: overwriting the work done since (see ``_restore_profile_once``).
_PROFILE_LIVE_MARKER = ".matrx-profile-live"
#: Chromium's own single-instance lock files. Left behind by a task that is
#: gone, they point at a hostname/pid that no longer exists and can make the
#: next launch believe the profile is in use.
_CHROMIUM_SINGLETON_FILES = ("SingletonLock", "SingletonSocket", "SingletonCookie")
#: How long past the acknowledged lease's expiry the worker waits for ANY
#: renewal before deciding the control plane is gone, closing Chromium cleanly
#: (so the profile on disk is consistent) and ending the task. A lease is
#: renewed every 20 s and lasts 60 s; 90 s past expiry is 150 s of silence.
LEASE_WATCHDOG_GRACE_SECONDS = float(
    os.environ.get("BROWSER_WORKER_LEASE_WATCHDOG_GRACE_SECONDS", "90")
)
LEASE_WATCHDOG_TICK_SECONDS = 15.0

# The manager derives its bootstrap envelope from the shared S2 budgets below.
# Each worker phase must finish (successfully or as a typed refusal) inside its
# declared budget: an unbounded restore or Playwright launch can leave the
# fixed-fleet worker occupied after the manager has stopped awaiting it.
BOOTSTRAP_LAUNCH_TIMEOUT_SECONDS = M.BOOTSTRAP_LAUNCH_TIMEOUT_SECONDS
PARTIAL_LAUNCH_CLEANUP_TIMEOUT_SECONDS = M.BOOTSTRAP_PARTIAL_LAUNCH_CLEANUP_TIMEOUT_SECONDS

WORKER_VERSION = "s2-worker/0.1.0"
REPLAY_STATE_FILENAME = ".matrx-browser-replay.json"


def _now() -> datetime:
    return datetime.now(UTC)


def _s3_error_code(response: httpx.Response) -> str:
    """Extract only S3's bounded error code; never retain a signed request URL."""
    try:
        root = ET.fromstring(response.content[:4096])
        code = (root.findtext("Code") or "unknown").strip()
    except (ET.ParseError, UnicodeError):
        return "unknown"
    return code[:128] or "unknown"


async def _upload_presigned_bytes(
    target: M.PresignedUpload, payload: bytes, *, what: str, timeout_s: float = 120.0
) -> bool:
    """PUT bytes to a presigned target. THE one upload primitive in the worker.

    The worker is deliberately credential-free: the control plane mints a
    short-lived presigned PUT and the worker pushes bytes at it. Every artifact
    the worker durably stores goes through here, so the secret-hygiene rule is
    written once — a presigned URL carries its signature in the query string,
    and both httpx exception strings and ``raise_for_status`` embed the full
    request URL, so neither may ever reach a log. Only the exception class and
    S3's own bounded error facts are recorded.

    Returns True only when the object is really on the far side. A caller may
    NEVER report ``uploaded=True`` on any other basis.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout_s) as client:
            response = await client.put(target.url, headers=target.headers, content=payload)
    except Exception as exc:
        logger.error("%s upload transport failed: error_type=%s", what, type(exc).__name__)
        return False

    if response.is_success:
        return True

    logger.error(
        "%s upload rejected: status=%s code=%s request_id=%s",
        what,
        response.status_code,
        _s3_error_code(response),
        (response.headers.get("x-amz-request-id") or "unknown")[:128],
    )
    return False


async def _upload_checkpoint_ciphertext(target: M.PresignedUpload, ciphertext: bytes) -> bool:
    """Upload without allowing presigned query credentials into exceptions/logs."""
    return await _upload_presigned_bytes(target, ciphertext, what="checkpoint")


async def _upload_checkpoint_file(target: M.PresignedUpload, path: str, size: int) -> bool:
    """PUT one file to a presigned target in bounded memory.

    Same secret-hygiene contract as ``_upload_presigned_bytes``. The body is
    an iterator with an explicit ``Content-Length`` — S3 rejects a chunked
    presigned PUT, and httpx honours a caller-supplied length instead of
    adding ``Transfer-Encoding``.
    """

    def _chunks():  # noqa: ANN202
        with open(path, "rb") as handle:
            while True:
                block = handle.read(_CHECKPOINT_CHUNK_BYTES)
                if not block:
                    return
                yield block

    headers = {**dict(target.headers or {}), "Content-Length": str(size)}
    try:
        async with httpx.AsyncClient(timeout=M.CHECKPOINT_RESTORE_TOTAL_TIMEOUT_SECONDS) as client:
            response = await client.put(target.url, headers=headers, content=_chunks())
    except Exception as exc:
        logger.error("checkpoint upload transport failed: error_type=%s", type(exc).__name__)
        return False
    if response.is_success:
        return True
    logger.error(
        "checkpoint upload rejected: status=%s code=%s request_id=%s",
        response.status_code,
        response.headers.get("x-amz-error-code") or "",
        response.headers.get("x-amz-request-id") or "",
    )
    return False


class _TrackedPage:
    __slots__ = (
        "page_id",
        "page",
        "opener_page_id",
        "kind",
        "opened_by",
        "opened_at",
        "closed_at",
        "last_focused_at",
    )

    def __init__(
        self,
        page_id: str,
        page: Any,
        *,
        opener_page_id: str | None,
        kind: str,
        opened_by: str,
    ) -> None:
        self.page_id = page_id
        self.page = page
        self.opener_page_id = opener_page_id
        self.kind = kind
        self.opened_by = opened_by
        self.opened_at = _now()
        self.closed_at: datetime | None = None
        self.last_focused_at: datetime | None = None


class _TrackedDialog:
    __slots__ = (
        "dialog_id",
        "page_id",
        "dialog",
        "type",
        "opened_at",
        "message",
        "default_value",
        "handled",
    )

    def __init__(self, dialog_id: str, page_id: str, dialog: Any) -> None:
        self.dialog_id = dialog_id
        self.page_id = page_id
        self.dialog = dialog
        self.type = getattr(dialog, "type", "alert")
        self.opened_at = _now()
        self.message = getattr(dialog, "message", "") or ""
        self.default_value = getattr(dialog, "default_value", "") or ""
        self.handled = False


class _TrackedDownload:
    __slots__ = (
        "download_id",
        "page_id",
        "download",
        "suggested_filename",
        "state",
        "byte_count",
        "content_hash",
        "started_at",
        "completed_at",
        "uploaded",
        "failure_code",
    )

    def __init__(self, download_id: str, page_id: str, download: Any) -> None:
        self.download_id = download_id
        self.page_id = page_id
        self.download = download
        self.suggested_filename = getattr(download, "suggested_filename", "download")
        self.state = "pending"
        self.byte_count: int | None = None
        self.content_hash: str | None = None
        self.started_at = _now()
        self.completed_at: datetime | None = None
        self.uploaded = False
        self.failure_code: str | None = None


class _HumanEpisode:
    def __init__(self, handoff_id: str) -> None:
        self.handoff_id = handoff_id
        self.claimed_at = _now()
        self.returned_at: datetime | None = None
        self.navigation_count = 0
        self.pages_opened = 0
        self.pages_closed = 0
        self.dialogs_opened = 0
        self.downloads_started = 0
        self.pointer_buckets = 0
        self.keyboard_buckets = 0
        self.origins: set[str] = set()


def _serialized_control(method):
    async def wrapped(self, *args, **kwargs):  # noqa: ANN002, ANN003
        async with self._control_gate:
            return await method(self, *args, **kwargs)

    return wrapped


class BrowserWorker:
    """The S2 worker. Instantiate, then drive through the eight operations."""

    def __init__(
        self,
        *,
        worker_id: str,
        token_verifier: TokenVerifier | None = None,
        event_sink: Callable[[M.WorkerEvent], None] | None = None,
        xvfb_display: str | None = None,
    ) -> None:
        self.worker_id = worker_id
        self.worker_version = WORKER_VERSION
        self._verifier = token_verifier
        self._event_sink = event_sink
        self._prepare_human_control: Callable[[M.RtcConfig], None] | None = None
        self._clear_human_control: Callable[[], None] | None = None
        self._control_gate = asyncio.Lock()
        # Display for handoff_capable mode. In production the orchestrator provides
        # the private Xvfb; here it is injected so a test can point at its own.
        self._xvfb_display = xvfb_display

        # Lifecycle
        # Bootstrap mutates the entire process-wide worker identity and profile
        # mount. Two API tasks may race the same activation (for example while
        # a deployment is settling), so only one bootstrap may cross this
        # boundary at a time. The loser observes the completed idempotency state
        # and replays it instead of restoring/launching a second Chromium over
        # the same EFS profile.
        self._bootstrap_gate = asyncio.Lock()
        self._bootstrap_task: asyncio.Task[M.BootstrapResponse] | None = None
        self._bootstrap_activation_key: str | None = None
        self._bootstrap_lifecycle: str = "idle"
        self._bootstrapped = False
        self._activation_key: str | None = None
        self._bootstrap_response: M.BootstrapResponse | None = None
        self.health: str = "starting"

        # Identity / policy
        self.run_id: str = ""
        self.profile_id: str = ""
        self.run_mode: str = "automation_only"
        self._policy: M.LaunchPolicy | None = None
        self._display: M.DisplayConfig | None = None
        self._user_data_dir: str = ""
        self.chromium_version: str = "unknown"
        self.launch_args: list[str] = []
        self.identity: BrowserIdentity | None = None

        # Fencing / ordering
        self.fencing_token: str = ""
        self.fencing_revision: int = 0
        self._last_applied: int | None = None
        self._seq_keys: dict[int, str] = {}
        self._replay: OrderedDict[tuple[int, str], Any] = OrderedDict()

        # Controller state
        self._controller = M.ControllerState(
            state="provisioning",
            controller_kind="none",
            controller_ref=None,
            fencing_revision=0,
            handoff_id=None,
            since=_now(),
            human_input_enabled=False,
        )

        # Queue
        self.queue_state: str = "closed"
        self._closed_reason: str = "not_bootstrapped"
        self._in_flight = 0
        #: One checkpoint at a time. Two control-plane callers racing a close
        #: (a person's stop and the maintenance sweep's "resume the interrupted
        #: stop", 2026-09-19) both called ``context.close()``; the second landed
        #: on a browser the first had already closed and was reported as
        #: ``chromium_unclean_exit`` — an honest-sounding failure for a browser
        #: that had in fact exited cleanly, once.
        self._checkpoint_in_progress = False
        #: True while THIS worker is closing Chromium on purpose (checkpoint,
        #: shutdown, termination). A context "close" event outside that window
        #: is a crash, and the worker says so instead of staying "healthy".
        self._closing_intentionally = False
        #: Set once by SIGTERM or the lease watchdog; never unset.
        self._terminating = False
        self._lease_watchdog: asyncio.Task | None = None
        #: Only the deployed worker PROCESS (server.py) turns this on: the
        #: watchdog ends the process, which is right for one task on ECS and
        #: wrong for a worker object living inside a test or a harness.
        self._lease_watchdog_enabled = False
        #: How the watchdog ends the process; a test injects a recorder.
        self._end_process: Callable[[], None] = _send_self_sigterm
        self._command_lock = asyncio.Lock()

        # Access / lease
        self._access_valid = True
        self._lease_expires_at: datetime | None = None
        self._last_activity = _now()

        # Playwright
        self._pw: Any = None
        self._context: Any = None
        # Residential egress (contract: common-docs/systems/platform/
        # residential-egress/FEATURE.md). The adapter is a loopback CONNECT
        # proxy that tunnels every TCP connection to the gateway and out through
        # the person's own computer. It outlives a single Playwright context:
        # the live-checkpoint path closes and RELAUNCHES the context, and
        # restarting the adapter there would need a ticket that may already have
        # expired. Its life is the bootstrapped run — closed by ``_kill_context``
        # and by ``shutdown``, and replaced when a bootstrap arrives with a
        # different ticket.
        self._egress_adapter: Any = None
        self._egress_ticket: str | None = None
        #: The plain name of the computer the run is leaving through, for the
        #: control plane's announcement. None = ordinary datacenter egress.
        self.egress_device_name: str | None = None
        self._session_mgr = BrowserSessionManager()
        self._session: BrowserSession | None = None

        # Page / dialog / download registries
        self._pages: OrderedDict[str, _TrackedPage] = OrderedDict()
        self._dialogs: dict[str, _TrackedDialog] = {}
        self._downloads: dict[str, _TrackedDownload] = {}
        self._active_page_id: str | None = None
        self._inventory_revision = 0
        self._page_counter = 0
        self._dialog_counter = 0
        self._download_counter = 0

        # Human episode
        self._episode: _HumanEpisode | None = None

        # Events
        self._event_buffer: list[M.WorkerEvent] = []
        self._callback_url: str | None = None
        self._callback_token: str | None = None

        # Profile lock
        self._lock: ProfileLock | None = None

    # ── introspection for the stub / tests ──────────────────────────────────

    @property
    def controller_state(self) -> str:
        return self._controller.state

    @property
    def active_page_id(self) -> str | None:
        return self._active_page_id

    def page_object(self, page_id: str) -> Any:
        tp = self._pages.get(page_id)
        return tp.page if tp else None

    @property
    def context(self) -> Any:
        return self._context

    @property
    def last_events(self) -> list[M.WorkerEvent]:
        return list(self._event_buffer)

    # ── common reply construction ───────────────────────────────────────────

    def set_human_control_preparer(
        self,
        callback: Callable[[M.RtcConfig], None],
        clear_callback: Callable[[], None] | None = None,
    ) -> None:
        self._prepare_human_control = callback
        self._clear_human_control = clear_callback

    async def _prepare_rtc(self, rtc_config: M.RtcConfig) -> None:
        task = asyncio.create_task(asyncio.to_thread(self._prepare_human_control, rtc_config))
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            try:
                await asyncio.shield(task)
            finally:
                if self._clear_human_control is not None:
                    await asyncio.to_thread(self._clear_human_control)
            raise

    def _reply_kwargs(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "profile_id": self.profile_id,
            "worker_id": self.worker_id,
            "controller": self._controller.model_copy(deep=True),
            "fencing_revision": self.fencing_revision,
            "queue_depth": self._in_flight,
            "queue_state": self.queue_state,  # type: ignore[arg-type]
            "run_mode": self.run_mode,  # type: ignore[arg-type]
            "worker_health": self.health,  # type: ignore[arg-type]
            "chromium_version": self.chromium_version,
            "worker_version": self.worker_version,
            "observed_at": _now(),
        }

    def _error_reply(self, response_cls: type, err: WorkerProtocolError, **extra: Any) -> Any:
        # Fill in the current fencing revision + controller on the error so the
        # ejected holder can reconcile without a second round trip (S2 §8.1).
        werr = err.to_error()
        if werr.current_fencing_revision is None:
            werr.current_fencing_revision = self.fencing_revision
        if werr.current_controller is None:
            werr.current_controller = self._controller.state
        if werr.last_sequence_applied is None:
            werr.last_sequence_applied = self._last_applied
        kwargs = self._reply_kwargs()
        kwargs.update(ok=False, error=werr)
        kwargs.update(extra)
        return response_cls(**kwargs)

    # ── auth + envelope verification ────────────────────────────────────────

    def _verify_bearer(self, bearer: str | None, op: str) -> None:
        if self._verifier is None:
            return
        if not bearer:
            raise WorkerProtocolError("unauthorized_worker_call", message="missing bearer token")
        self._verifier.verify(bearer, worker_id=self.worker_id, op=op)

    def _check_identity(self, env: M.WorkerCallEnvelope) -> None:
        # Checked BEFORE fencing so a misrouted call never reveals token state.
        if env.run_id != self.run_id:
            raise WorkerProtocolError("run_mismatch", message="run id is not this worker's run")
        if env.profile_id != self.profile_id:
            raise WorkerProtocolError(
                "profile_mismatch", message="profile id is not the mounted profile"
            )

    def _check_fencing(self, env: M.WorkerCallEnvelope, *, is_transition: bool) -> None:
        if is_transition:
            return  # transition validates its own revision monotonicity in the op
        if (
            not _consttime_eq(env.fencing_token, self.fencing_token)
            or env.fencing_revision < self.fencing_revision
        ):
            raise WorkerProtocolError("stale_fencing_token", message="fencing token is stale")
        if env.fencing_revision > self.fencing_revision:
            raise WorkerProtocolError(
                "unknown_fencing_revision",
                message="revision higher than current on a non-transition op",
            )

    def _check_sequence(self, env: M.WorkerCallEnvelope) -> Any | None:
        """Sequenced-op ordering + replay (S2 §8.2/§8.3). Returns a cached response
        to replay, or ``None`` to proceed."""
        if env.sequence is None or env.idempotency_key is None:
            raise WorkerProtocolError(
                "sequence_required", message="sequenced op requires sequence + idempotency_key"
            )
        seq, key = env.sequence, env.idempotency_key
        cached = self._replay.get((seq, key))
        if cached is not None:
            self._replay.move_to_end((seq, key))
            return cached.model_copy(update={"replayed": True})
        prior_key = self._seq_keys.get(seq)
        if prior_key is not None and prior_key != key:
            raise WorkerProtocolError(
                "sequence_conflict", message="same sequence, different idempotency key"
            )
        if self._last_applied is not None and seq <= self._last_applied:
            oldest = self._replay and min(s for (s, _k) in self._replay.keys())
            if oldest and seq < oldest:
                raise WorkerProtocolError(
                    "sequence_too_old", message="older than the replay cache window"
                )
            raise WorkerProtocolError(
                "sequence_out_of_order", message="sequence below last applied"
            )
        return None

    def _forbid_sequence(self, env: M.WorkerCallEnvelope) -> None:
        if env.sequence is not None:
            raise WorkerProtocolError(
                "sequence_not_permitted", message="unsequenced op carried a sequence"
            )

    def _admit_sequenced(self, env: M.WorkerCallEnvelope, response: Any) -> None:
        """Record a sequenced op as applied and persist its replay receipt.

        The receipt lives inside the profile directory so an encrypted checkpoint
        carries the execute-once fence to a replacement host.  The file contains
        only worker responses (already-sanitized facts), never command arguments.
        """
        seq, key = env.sequence, env.idempotency_key
        assert seq is not None and key is not None
        self._last_applied = seq if self._last_applied is None else max(self._last_applied, seq)
        self._seq_keys[seq] = key
        self._replay[(seq, key)] = response
        while len(self._replay) > M.REPLAY_CACHE_SIZE:
            self._replay.popitem(last=False)
        self._persist_replay_state()

    def _replay_state_path(self) -> str:
        return os.path.join(self._user_data_dir, REPLAY_STATE_FILENAME)

    def _persist_replay_state(self) -> None:
        entries = [
            {
                "sequence": sequence,
                "idempotency_key": key,
                "response_type": response.__class__.__name__,
                "response": response.model_dump(mode="json"),
            }
            for (sequence, key), response in self._replay.items()
        ]
        payload = {
            "version": 1,
            "run_id": self.run_id,
            "last_applied": self._last_applied,
            "entries": entries,
        }
        path = self._replay_state_path()
        temporary = f"{path}.tmp-{uuid.uuid4().hex}"
        try:
            with open(temporary, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, separators=(",", ":"), sort_keys=True)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        except Exception:
            self.health = "degraded"
            self.queue_state = "closed"
            self._closed_reason = "worker_degraded"
            logger.exception("failed to persist browser replay state")
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass

    def _restore_replay_state(self) -> None:
        path = self._replay_state_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, encoding="utf-8") as handle:
                payload = json.load(handle)
            if payload.get("version") != 1 or payload.get("run_id") != self.run_id:
                return
            restored: OrderedDict[tuple[int, str], Any] = OrderedDict()
            keys: dict[int, str] = {}
            for item in payload.get("entries", []):
                response_type = item["response_type"]
                response_model = getattr(M, response_type, None)
                if response_model not in {
                    M.CommandResponse,
                    M.ControllerTransitionResponse,
                    M.CaptureResponse,
                    M.CheckpointResponse,
                    M.ShutdownResponse,
                }:
                    raise ValueError("unsupported replay response type")
                sequence = int(item["sequence"])
                key = str(item["idempotency_key"])
                restored[(sequence, key)] = response_model.model_validate(item["response"])
                keys[sequence] = key
            self._replay = restored
            self._seq_keys = keys
            stored_last = payload.get("last_applied")
            if stored_last is not None:
                self._last_applied = max(self._last_applied or 0, int(stored_last))
        except Exception as exc:
            raise WorkerProtocolError(
                "worker_degraded",
                message="saved replay state could not be restored safely",
            ) from exc

    def _require_bootstrapped(self) -> None:
        if not self._bootstrapped:
            raise WorkerProtocolError("not_bootstrapped", message="worker not bootstrapped")

    def _require_not_mid_bootstrap(self) -> None:
        """``not_bootstrapped`` must never be the answer while a bootstrap is
        being applied: the control plane reads it as "nothing ever started" and
        retires the run, and the bootstrap then completes into an orphan that
        refuses every later start ``already_bootstrapped`` (2026-09-13)."""
        if self._bootstrap_lifecycle in {"starting", "aborting", "quarantined"}:
            raise WorkerProtocolError(
                "bootstrap_in_progress", message="a bootstrap is being applied; retry"
            )

    def _require_unexpired_lease(self) -> None:
        """Refuse mutable work until the manager has acknowledged a live DB lease.

        Heartbeat itself intentionally bypasses this gate: it is the event-driven
        operation that reacquires an idle lease. Every action that can observe or
        change browser state is fenced behind the acknowledged deadline.
        """
        if self._lease_expires_at is None or self._lease_expires_at <= _now():
            raise WorkerProtocolError("lease_expired", message="browser run lease expired")

    # ── operation 5.1: bootstrap ────────────────────────────────────────────

    def _reset_after_stopped_run(self) -> None:
        """Prepare this fixed-fleet worker for the next, non-overlapping run."""
        # Shutdown normally releases this lock. Repeat the release here before
        # dropping the object so any partial/older exit path cannot leak its fd
        # for the lifetime of this reusable worker process.
        if self._lock is not None:
            self._lock.release()
        self._bootstrapped = False
        self._activation_key = None
        self._bootstrap_response = None
        self.health = "starting"
        self.run_id = ""
        self.profile_id = ""
        self._policy = None
        self._display = None
        self._user_data_dir = ""
        self.fencing_token = ""
        self.fencing_revision = 0
        self._last_applied = None
        self._seq_keys.clear()
        self._replay.clear()
        self._controller = M.ControllerState(
            state="provisioning",
            controller_kind="none",
            controller_ref=None,
            fencing_revision=0,
            handoff_id=None,
            since=_now(),
            human_input_enabled=False,
        )
        self.queue_state = "closed"
        self._closed_reason = "not_bootstrapped"
        self._access_valid = True
        self._lease_expires_at = None
        self._session_mgr = BrowserSessionManager()
        self._session = None
        self._pages.clear()
        self._dialogs.clear()
        self._downloads.clear()
        self._active_page_id = None
        self._inventory_revision = 0
        self._page_counter = 0
        self._dialog_counter = 0
        self._download_counter = 0
        self._episode = None
        self._event_buffer.clear()
        self._callback_url = None
        self._callback_token = None
        self._lock = None
        self._bootstrap_task = None
        self._bootstrap_activation_key = None
        self._bootstrap_lifecycle = "idle"

    @_serialized_control
    async def bootstrap(
        self, request: M.BootstrapRequest, *, bearer: str | None = None
    ) -> M.BootstrapResponse:
        """Join the activation owner without letting HTTP cancellation own it.

        FastAPI cancels a request coroutine when the manager's HTTP deadline
        expires. The profile restore may still have a filesystem thread in
        flight, so that request must never cancel the process-wide owner or
        release its lock for another activation. The same activation joins the
        owner; a different activation receives the explicit retryable state.
        """
        try:
            self._verify_bearer(bearer, "bootstrap")
        except WorkerProtocolError as err:
            return self._error_reply(
                M.BootstrapResponse, err, accepted=False, host_lock_acquired=False
            )

        async with self._bootstrap_gate:
            if self._bootstrapped and self.health == "stopped" and self.queue_state == "closed":
                self._reset_after_stopped_run()
            if self._bootstrapped:
                # A live worker's replay/refusal path is synchronous and must
                # retain the incumbent identity; it is not a new owner.
                return await self._bootstrap_once(request, authenticated=True)
            active = self._bootstrap_task
            if active is not None and not active.done():
                if self._bootstrap_activation_key != request.activation_key:
                    return self._error_reply(
                        M.BootstrapResponse,
                        WorkerProtocolError(
                            "bootstrap_in_progress",
                            message="a different bootstrap activation is still cleaning up",
                        ),
                        accepted=False,
                        host_lock_acquired=self._lock.held if self._lock else False,
                    )
                owner = active
                joined = True
            else:
                self._bootstrap_activation_key = request.activation_key
                self._bootstrap_lifecycle = "starting"
                owner = asyncio.create_task(
                    self._bootstrap_owner(request),
                    name=f"cloud-browser-bootstrap:{request.activation_key}",
                )
                self._bootstrap_task = owner
                joined = False
        try:
            response = await asyncio.shield(owner)
            return response.model_copy(update={"replayed": True}) if joined else response
        except asyncio.CancelledError:
            await asyncio.shield(owner)
            raise

    async def _bootstrap_owner(self, request: M.BootstrapRequest) -> M.BootstrapResponse:
        """Own one activation through all cleanup, independent of its callers."""
        try:
            return await self._bootstrap_once(request, authenticated=True)
        finally:
            if not self._bootstrapped:
                self._bootstrap_lifecycle = "idle"

    async def _bootstrap_once(
        self, request: M.BootstrapRequest, *, bearer: str | None = None, authenticated: bool = False
    ) -> M.BootstrapResponse:
        if not authenticated:
            try:
                self._verify_bearer(bearer, "bootstrap")
            except WorkerProtocolError as err:
                return self._error_reply(
                    M.BootstrapResponse, err, accepted=False, host_lock_acquired=False
                )

        # A fixed-fleet process is reusable only after the prior run reached a
        # terminal stopped state and released its profile lock. A second start
        # while the prior run is live remains a hard refusal.
        if self._bootstrapped and self.health == "stopped" and self.queue_state == "closed":
            self._reset_after_stopped_run()

        # Idempotency on (profile_id, activation_key) BEFORE anything mutates.
        if self._bootstrapped:
            if (
                self._activation_key == request.activation_key
                and self._bootstrap_response is not None
            ):
                return self._bootstrap_response.model_copy(update={"replayed": True})
            # This is an incumbent-worker refusal, not an identity transition.
            # Replacing these fields merely to echo the rejected request corrupts
            # the live worker: its next heartbeat/command for the incumbent run
            # then fails ``run_mismatch`` while Chromium is still attached to it.
            # Keep the incumbent envelope intact; the refusal code is sufficient
            # for the caller to identify the rejected bootstrap.
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError(
                    "already_bootstrapped",
                    message="second bootstrap with a different activation key",
                ),
                accepted=False,
                host_lock_acquired=self._lock.held if self._lock else False,
            )

        self.run_id = request.run_id
        self.profile_id = request.profile_id
        self.run_mode = request.policy.run_mode
        self._policy = request.policy
        self._display = request.display
        self._user_data_dir = request.mount.user_data_dir
        self._callback_url = request.callback_url
        self._callback_token = request.callback_token
        self._activation_key = request.activation_key

        # Mode ↔ display coherence (S2 §12.1).
        if request.policy.run_mode == "handoff_capable" and request.display is None:
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError(
                    "invalid_command_arguments", message="handoff_capable requires a DisplayConfig"
                ),
                accepted=False,
                host_lock_acquired=False,
            )
        if request.policy.run_mode == "automation_only" and request.display is not None:
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError(
                    "invalid_command_arguments", message="automation_only refuses a DisplayConfig"
                ),
                accepted=False,
                host_lock_acquired=False,
            )

        # Proxy gate (an internal proxy is refused, exactly as create() does).
        #
        # 🚨 This gates ``policy.proxy`` — the CALLER-SUPPLIED remote address —
        # and nothing else. ``policy.egress`` is deliberately NOT gated here:
        # its adapter binds ``127.0.0.1:<ephemeral>`` inside this worker, so the
        # public-routability check would refuse every residential launch. The
        # grant is the control plane's, the adapter's own remote is the public
        # gateway, and the ticket is what authorizes it.
        try:
            await guard_proxy(request.policy.proxy)
        except Exception:
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError(
                    "invalid_command_arguments", message="proxy is not publicly routable"
                ),
                accepted=False,
                host_lock_acquired=False,
            )

        # Advisory host lock — a fence, refused loudly, no launch on failure.
        #
        # 🚨 RELEASE BEFORE REPLACING. Any lock object still held at this point
        # belongs to a run that is already over: the reset above fires ONLY for
        # a cleanly stopped run (`_bootstrapped and health==stopped and
        # queue_state==closed`), so a crash or a partial bootstrap — acquire
        # succeeded, a later step returned an error without releasing — leaves
        # the fd open. Overwriting `self._lock` then drops the only reference to
        # that open fd, and a raw fd is NOT closed by garbage collection: the
        # profile stays locked for the LIFE of this reusable worker process and
        # every future bootstrap is refused `profile_locked_locally`, forever.
        # That is not a transient restart, it is a permanent outage of the
        # profile — observed 2026-08-26, and the same shape as the "13
        # consecutive production starts" burn recorded in ports.BootstrapResult.
        if self._lock is not None:
            self._lock.release()
        self._lock = ProfileLock(self._user_data_dir)
        try:
            self._lock.acquire()
        except ProfileLockError:
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError(
                    "profile_locked_locally", message="profile advisory lock is held"
                ),
                accepted=False,
                host_lock_acquired=False,
            )

        # A killed container releases our flock automatically but Chromium's
        # own Singleton* crash markers persist on EFS.  Clear only those narrow
        # browser-owned artifacts, and only after exclusive profile ownership
        # is proven. EFS metadata operations are blocking filesystem calls, so
        # keep them off the ASGI event loop: the same process must continue to
        # answer ECS health probes while a large/recovering profile is inspected.
        # Saved session data remains untouched.
        try:
            await asyncio.to_thread(self._lock.clear_stale_chromium_singletons)
        except ProfileLockError:
            self._lock.release()
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError(
                    "profile_locked_locally",
                    message="stale Chromium profile ownership could not be cleared safely",
                ),
                accepted=False,
                host_lock_acquired=False,
            )

        if request.mount.source == "restored_checkpoint":
            if request.mount.restore is None:
                self._lock.release()
                return self._error_reply(
                    M.BootstrapResponse,
                    WorkerProtocolError(
                        "invalid_command_arguments",
                        message="checkpoint restore material is missing",
                    ),
                    accepted=False,
                    host_lock_acquired=True,
                    egress_guard_installed=False,
                )
            try:
                await _restore_profile(self._user_data_dir, request.mount.restore)
            except Exception:
                logger.exception("profile checkpoint restore failed")
                self._lock.release()
                return self._error_reply(
                    M.BootstrapResponse,
                    WorkerProtocolError(
                        "checkpoint_failed", message="profile checkpoint restore failed"
                    ),
                    accepted=False,
                    host_lock_acquired=True,
                    egress_guard_installed=False,
                )

        # Sequence + fencing set from the bootstrap envelope.
        # A replacement worker resumes the durable fence, not the first fence
        # that originally created the run.  Keeping the initial token separately
        # is useful to the manager, but accepting it here would make every
        # post-handoff replacement reject the very next heartbeat as stale.
        self.fencing_token = request.fencing_token
        self.fencing_revision = request.fencing_revision
        self._last_applied = request.sequence_base - 1 if request.sequence_base > 0 else None
        try:
            self._restore_replay_state()
        except WorkerProtocolError as err:
            self._lock.release()
            return self._error_reply(
                M.BootstrapResponse,
                err,
                accepted=False,
                host_lock_acquired=True,
                egress_guard_installed=False,
            )
        self._controller.fencing_revision = self.fencing_revision

        # Launch is owned by the activation task, not by the HTTP request that
        # happened to start it. A cancelled caller therefore cannot free the
        # profile lock while Playwright is still touching this profile.
        try:
            egress_ok = await asyncio.wait_for(
                self._launch_context(request.policy, request.display),
                timeout=BOOTSTRAP_LAUNCH_TIMEOUT_SECONDS,
            )
        except TimeoutError:
            logger.error(
                "bootstrap launch timed out after %.1fs",
                BOOTSTRAP_LAUNCH_TIMEOUT_SECONDS,
            )
            await self._cleanup_partial_launch()
            self._lock.release()
            self.health = "browser_crashed"
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError("browser_crashed", message="Chromium launch timed out"),
                accepted=False,
                host_lock_acquired=True,
                egress_guard_installed=False,
            )
        except _EgressGuardFailed:
            await self._cleanup_partial_launch()
            self._lock.release()
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError(
                    "worker_degraded", message="egress guard failed to install; launch aborted"
                ),
                accepted=False,
                host_lock_acquired=False,
                egress_guard_installed=False,
            )
        except Exception:  # launch failure
            logger.exception("bootstrap launch failed")
            await self._cleanup_partial_launch()
            self._lock.release()
            self.health = "browser_crashed"
            return self._error_reply(
                M.BootstrapResponse,
                WorkerProtocolError("browser_crashed", message="Chromium failed to launch"),
                accepted=False,
                host_lock_acquired=True,
            )

        self._bootstrapped = True
        self._bootstrap_lifecycle = "active"
        self.health = "healthy"
        self.queue_state = "open"
        await asyncio.to_thread(_mark_profile_live, self._user_data_dir)
        self._start_lease_watchdog()
        self._closed_reason = ""
        # Idle age belongs to a RUN, not to this reusable fixed-fleet process.
        # Without this reset, the next run inherits the prior run's idle clock
        # and the manager's first maintenance pass can stop a browser that was
        # opened only seconds ago.
        self._last_activity = _now()
        reopened_state = request.policy.reopened_controller_state
        controller_state = reopened_state or "agent_control"
        human_input_enabled = bool(
            controller_state == "human_control" and request.policy.reopened_human_input_enabled
        )
        self._controller = self._controller.model_copy(
            update={
                "state": controller_state,
                "controller_kind": "human"
                if controller_state in {"handoff_requested", "human_control", "resume_pending"}
                else "agent",
                "handoff_id": request.policy.reopened_handoff_id,
                "since": _now(),
                "human_input_enabled": human_input_enabled,
                "fencing_revision": self.fencing_revision,
            }
        )
        self._episode = (
            _HumanEpisode(request.policy.reopened_handoff_id or uuid.uuid4().hex)
            if controller_state == "human_control"
            else None
        )

        inv = self._build_inventory(["pages", "dialogs", "downloads"])
        resp = M.BootstrapResponse(
            **self._reply_kwargs(),
            ok=True,
            accepted=True,
            host_lock_acquired=True,
            display_ref=self._xvfb_display if self.run_mode == "handoff_capable" else None,
            page_inventory=inv,
            volatile_state_preserved=False if request.policy.reopened_for_handoff else True,
            egress_guard_installed=egress_ok,
        )
        self._bootstrap_response = resp
        return resp

    async def _cleanup_partial_launch(self) -> None:
        """Best-effort, bounded cleanup after bootstrap never became live."""

        try:
            await asyncio.wait_for(
                self._kill_context(),
                timeout=PARTIAL_LAUNCH_CLEANUP_TIMEOUT_SECONDS,
            )
        except (TimeoutError, Exception):
            # The task must return a typed failure and release its profile lock
            # even when Playwright's transport is itself wedged.
            logger.exception("partial browser launch cleanup failed or timed out")
            self._context = None
            self._pw = None

    async def _ensure_egress_adapter(self, policy: M.LaunchPolicy) -> str | None:
        """Start (or reuse) the residential-egress adapter for this policy.

        Returns the loopback proxy URL to launch through, or None for ordinary
        datacenter egress. Idempotent across the live-checkpoint relaunch — the
        same ticket keeps the same adapter — and it replaces the adapter when a
        bootstrap arrives carrying a DIFFERENT ticket.

        A failure to start is a LAUNCH failure, never a silent fall-through to
        the datacenter address the site just blocked: falling back would send
        the very request the person lent their computer for straight back out
        of the exit that is refused, and nothing would say so.
        """
        egress = policy.egress
        if egress is None:
            if self._egress_adapter is not None:
                await self._close_egress_adapter()
            return None
        if self._egress_adapter is not None and self._egress_ticket == egress.ticket:
            return str(self._egress_adapter.proxy_url)
        if self._egress_adapter is not None:
            await self._close_egress_adapter()
        # Lazy: the adapter pulls in the consumer WebSocket leg, and a worker
        # that never uses residential egress must not pay for it at import.
        from matrx_scraper.egress_adapter import EgressAdapter

        adapter = await EgressAdapter.start(egress.ticket, egress.consume_url)
        self._egress_adapter = adapter
        self._egress_ticket = egress.ticket
        self.egress_device_name = egress.device_name
        logger.info(
            "Cloud Browser leaving through the person's own computer: device=%s",
            egress.device_name,
        )
        return str(adapter.proxy_url)

    async def _close_egress_adapter(self) -> None:
        adapter, self._egress_adapter = self._egress_adapter, None
        self._egress_ticket = None
        self.egress_device_name = None
        if adapter is None:
            return
        try:
            await adapter.close()
        except Exception:
            logger.exception("residential egress adapter did not close cleanly")

    async def _launch_context(
        self, policy: M.LaunchPolicy, display: M.DisplayConfig | None
    ) -> bool:
        from playwright.async_api import async_playwright

        headless = self.run_mode == "automation_only"
        # CB-013: the identity this launch presents (binary, timezone, locale,
        # graphics, input shaping). Policy > image environment > defaults.
        identity = resolve_identity(policy, chromium_fallback=_resolve_chromium_executable())
        self.identity = identity
        # D-5 cookie scheme: launch Chromium keyring-free so cookies use the basic
        # (obfuscated-file) store rather than a system keyring the worker can't reach.
        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--password-store=basic",
            "--use-mock-keychain",
            "--disable-features=Translate",
            f"--lang={identity.locale}",
            *STEALTH_ARGS,
        ]
        if not headless:
            args += [
                "--window-position=0,0",
                f"--window-size={(display.width if display else 1280)},{(display.height if display else 900)}",
            ]
        self.launch_args = list(args)

        if not headless and self._xvfb_display:
            os.environ["DISPLAY"] = self._xvfb_display
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
        # Chrome reads the process TZ for anything the CDP override does not
        # reach; keep the two in agreement.
        os.environ["TZ"] = identity.timezone_id

        self._pw = await async_playwright().start()
        launch_kwargs: dict[str, Any] = {
            "user_data_dir": self._user_data_dir,
            "headless": headless,
            "args": args,
            "ignore_default_args": list(IGNORED_DEFAULT_ARGS),
            "accept_downloads": policy.allow_downloads,
            "locale": identity.locale,
            "timezone_id": identity.timezone_id,
        }
        # Google Chrome when the image ships it; otherwise the full Chromium binary
        # under PLAYWRIGHT_BROWSERS_PATH (headless via --headless=new); otherwise
        # Playwright's default. Which one is announced in the log.
        if identity.executable_path is not None:
            launch_kwargs["executable_path"] = identity.executable_path
        if policy.viewport:
            launch_kwargs["viewport"] = policy.viewport
        elif not headless:
            # A headed browser's page must be the window, and screen.* must be the
            # X screen. ``viewport=None`` is Playwright's DEFAULT (1280×720 with an
            # emulated 1280×720 screen) — that is exactly the screen/window
            # mismatch a site reads as emulation. ``no_viewport`` disables it.
            launch_kwargs["no_viewport"] = True
        if policy.user_agent:
            launch_kwargs["user_agent"] = policy.user_agent
        # Residential egress wins when the control plane granted one: the run
        # leaves through the person's own computer for its whole life.
        egress_proxy_url = await self._ensure_egress_adapter(policy)
        if egress_proxy_url is not None:
            launch_kwargs["proxy"] = {"server": egress_proxy_url}
        elif policy.proxy:
            # ``playwright_proxy`` is the ONE translation: Playwright strips a
            # URL's ``user:password@`` from ``server`` WITHOUT moving it into
            # username/password, so a credentialed proxy URL silently launched
            # unauthenticated here. Explicit policy credentials still win.
            proxy: dict[str, str] = playwright_proxy(policy.proxy)
            if policy.proxy_username is not None and policy.proxy_password is not None:
                proxy["username"] = policy.proxy_username
                proxy["password"] = policy.proxy_password
            launch_kwargs["proxy"] = proxy
        logger.info(
            "Cloud Browser launch identity: binary=%s timezone=%s locale=%s webgl=%s humanize=%s headless=%s",
            identity.binary_kind,
            identity.timezone_id,
            identity.locale,
            "patched" if identity.webgl_renderer else "honest",
            identity.humanize_input,
            headless,
        )

        self._context = await self._pw.chromium.launch_persistent_context(**launch_kwargs)
        self._closing_intentionally = False
        try:
            self._context.on("close", lambda *_args: self._on_context_closed())
        except Exception:
            logger.warning("could not subscribe to the browser context close event", exc_info=True)
        webgl_script = webgl_init_script(identity.webgl_vendor, identity.webgl_renderer)
        if webgl_script is not None:
            # Context-level: every page, popup and iframe of this run, before any
            # site script runs. Failure here is a launch failure, not a silent
            # regression to SwiftShader.
            await self._context.add_init_script(webgl_script)
        try:
            self.chromium_version = (
                self._context.browser.version if self._context.browser else "unknown"
            )
        except Exception:
            self.chromium_version = "unknown"

        # Egress guard on the CONTEXT before the first tracked page — reused verbatim.
        egress_ok = True
        try:
            await install_egress_guard(self._context)
        except Exception:
            logger.exception("egress guard install failed")
            raise _EgressGuardFailed()

        # Wire context-level page tracking.
        self._context.on("page", self._on_new_page)

        # Reconcile pages that already exist post-launch.
        existing = list(self._context.pages)
        if not existing:
            page = await self._context.new_page()
            existing = [page]
        for i, page in enumerate(existing):
            tp = self._register_page(page, opener_page_id=None, kind="page", opened_by="agent")
            if i == 0:
                self._active_page_id = tp.page_id
                tp.last_focused_at = _now()

        # A BrowserSession over the active page so the imported action functions run
        # unchanged (they resolve by session_id == run_id and touch only .page).
        active = self._pages[self._active_page_id]  # type: ignore[index]
        self._session = BrowserSession(
            session_id=self.run_id,
            pw=self._pw,
            browser=self._context,
            context=self._context,
            page=active.page,
        )
        async with self._session_mgr._lock:  # noqa: SLF001 - intentional: register our own session
            self._session_mgr._sessions[self.run_id] = self._session  # noqa: SLF001
        return egress_ok

    # ── page / dialog / download tracking ───────────────────────────────────

    def _register_page(
        self, page: Any, *, opener_page_id: str | None, kind: str, opened_by: str
    ) -> _TrackedPage:
        self._page_counter += 1
        page_id = f"p_{self._page_counter}"
        tp = _TrackedPage(
            page_id, page, opener_page_id=opener_page_id, kind=kind, opened_by=opened_by
        )
        self._pages[page_id] = tp
        self._bump_inventory()

        page.on("dialog", lambda dialog, pid=page_id: self._on_dialog(pid, dialog))
        page.on("download", lambda dl, pid=page_id: self._on_download(pid, dl))
        page.on("close", lambda pg=None, pid=page_id: self._on_page_close(pid))
        page.on("crash", lambda pg=None, pid=page_id: self._on_page_crash(pid))
        return tp

    def _on_new_page(self, page: Any) -> None:
        # A page we did not open through the launch reconciliation — a popup or a
        # human-opened tab. opened_by keys off the current controller.
        for tp in self._pages.values():
            if tp.page is page:
                return
        opened_by = (
            "human"
            if self._controller.state == "human_control"
            else ("agent" if self._controller.state == "agent_control" else "page")
        )
        opener = self._active_page_id
        tp = self._register_page(page, opener_page_id=opener, kind="popup", opened_by=opened_by)
        if self._episode is not None:
            self._episode.pages_opened += 1
            tp.last_focused_at = _now()  # the human is looking at what they just opened
        self._emit("page_opened", page_id=tp.page_id, safe_url=safe_url(getattr(page, "url", "")))

    def _on_page_close(self, page_id: str) -> None:
        tp = self._pages.get(page_id)
        if tp is None or tp.closed_at is not None:
            return
        tp.closed_at = _now()
        if self._episode is not None:
            self._episode.pages_closed += 1
        self._bump_inventory()
        self._emit("page_closed", page_id=page_id)

    def _on_page_crash(self, page_id: str) -> None:
        self._emit("browser_crashed", page_id=page_id)

    def _on_dialog(self, page_id: str, dialog: Any) -> None:
        # NEVER auto-dismiss. Record it and leave it pending; the ONLY way it clears
        # is an explicit, audited handle_dialog command (S2 §7.1).
        self._dialog_counter += 1
        did = f"d_{self._dialog_counter}"
        self._dialogs[did] = _TrackedDialog(did, page_id, dialog)
        if self._episode is not None:
            self._episode.dialogs_opened += 1
        self._bump_inventory()
        self._emit("dialog_opened", page_id=page_id, detail_code=getattr(dialog, "type", "alert"))

    def _on_download(self, page_id: str, download: Any) -> None:
        self._download_counter += 1
        dlid = f"dl_{self._download_counter}"
        self._downloads[dlid] = _TrackedDownload(dlid, page_id, download)
        if self._episode is not None:
            self._episode.downloads_started += 1
        self._bump_inventory()
        self._emit("download_started", page_id=page_id)

    def _bump_inventory(self) -> None:
        self._inventory_revision += 1

    def _reconcile_active(self) -> None:
        """Return-from-human active-page selection (S2 §10.2): the surviving page
        with the greatest last_focused_at; else the last-opened survivor."""
        survivors = [tp for tp in self._pages.values() if tp.closed_at is None]
        if not survivors:
            self._active_page_id = None
            return
        focused = [tp for tp in survivors if tp.last_focused_at is not None]
        if focused:
            chosen = max(focused, key=lambda tp: tp.last_focused_at)  # type: ignore[arg-type,return-value]
        else:
            chosen = survivors[-1]
        self._active_page_id = chosen.page_id
        if self._session is not None:
            self._session.page = chosen.page

    def _build_inventory(self, include: list[str]) -> M.PageInventory:
        pages: list[M.PageRecord] = []
        ordered = list(self._pages.values())
        truncated = len(ordered) > M.PAGE_INVENTORY_CAP
        for tp in ordered[: M.PAGE_INVENTORY_CAP]:
            url = getattr(tp.page, "url", "") or ""
            title = None
            try:
                # page.title() is async; we avoid awaiting here — title is best-effort
                # and filled by observe when needed. Keep None to stay non-blocking.
                title = None
            except Exception:
                title = None
            load_state = (
                "crashed"
                if getattr(tp.page, "is_closed", lambda: False)() and tp.closed_at is None
                else "loaded"
            )
            pages.append(
                M.PageRecord(
                    page_id=tp.page_id,
                    opener_page_id=tp.opener_page_id,
                    kind=tp.kind,  # type: ignore[arg-type]
                    is_active=(tp.page_id == self._active_page_id),
                    is_closed=tp.closed_at is not None,
                    safe_url=safe_url(url),
                    origin=origin_of(url),
                    title=cap_label(title),
                    opened_at=tp.opened_at,
                    closed_at=tp.closed_at,
                    opened_by=tp.opened_by,  # type: ignore[arg-type]
                    last_focused_at=tp.last_focused_at,
                    load_state=load_state,  # type: ignore[arg-type]
                )
            )
        dialogs = (
            [
                M.DialogRecord(
                    dialog_id=d.dialog_id,
                    page_id=d.page_id,
                    type=d.type
                    if d.type in ("alert", "confirm", "prompt", "beforeunload")
                    else "alert",  # type: ignore[arg-type]
                    opened_at=d.opened_at,
                    message_present=bool(d.message),
                    message=None,  # OPEN(dialog text) — withheld by default (S2 §14.4)
                    default_value_present=bool(d.default_value),
                    handled=d.handled,
                )
                for d in self._dialogs.values()
            ]
            if "dialogs" in include
            else []
        )
        downloads = (
            [
                M.DownloadRecord(
                    download_id=dl.download_id,
                    page_id=dl.page_id,
                    suggested_filename=dl.suggested_filename,
                    state=dl.state,  # type: ignore[arg-type]
                    byte_count=dl.byte_count,
                    content_hash=dl.content_hash,
                    started_at=dl.started_at,
                    completed_at=dl.completed_at,
                    uploaded=dl.uploaded,
                    failure_code=dl.failure_code,
                )
                for dl in self._downloads.values()
            ]
            if "downloads" in include
            else []
        )
        return M.PageInventory(
            revision=self._inventory_revision,
            active_page_id=self._active_page_id,
            pages=pages,
            dialogs=dialogs,
            downloads=downloads,
            file_choosers=[],
            permission_prompts=[],
            captured_at=_now(),
            truncated=truncated,
            total_page_count=len(ordered),
        )

    # ── operation 5.2: heartbeat ────────────────────────────────────────────

    @_serialized_control
    async def heartbeat(
        self, request: M.HeartbeatRequest, *, bearer: str | None = None
    ) -> M.HeartbeatResponse:
        try:
            self._verify_bearer(bearer, "heartbeat")
            self._require_not_mid_bootstrap()
            self._require_bootstrapped()
            self._check_identity(request)
            self._check_fencing(request, is_transition=False)
            self._forbid_sequence(request)
        except WorkerProtocolError as err:
            return self._error_reply(M.HeartbeatResponse, err)

        if (
            request.rtc_config is not None
            and self._controller.state == "human_control"
            and request.access_still_valid
        ):
            try:
                if self._prepare_human_control is None:
                    raise RuntimeError("RTC unavailable")
                await self._prepare_rtc(request.rtc_config)
            except Exception:
                return self._error_reply(
                    M.HeartbeatResponse,
                    WorkerProtocolError("reopen_required", message="RTC stream refresh failed"),
                )
        self._lease_expires_at = request.lease_expires_at
        if not request.access_still_valid:
            # Immediately end human input injection and refuse subsequent commands.
            self._access_valid = False
            self.queue_state = "closed"
            self._closed_reason = "access_revoked"
            self._controller = self._controller.model_copy(update={"human_input_enabled": False})

        rotate = None
        if request.rotate_callback_token:
            rotate = uuid.uuid4().hex
            self._callback_token = rotate

        idle_ms = int((_now() - self._last_activity).total_seconds() * 1000)
        return M.HeartbeatResponse(
            **self._reply_kwargs(),
            ok=True,
            lease_acknowledged=True,
            callback_token=rotate,
            idle_ms=idle_ms,
            last_sequence_applied=self._last_applied,
            page_count=sum(1 for tp in self._pages.values() if tp.closed_at is None),
            pending_events=len(self._event_buffer),
            checkpoint_recommended=False,
        )

    # ── operation 5.3: command ──────────────────────────────────────────────

    async def command(
        self, request: M.CommandRequest, *, bearer: str | None = None
    ) -> M.CommandResponse:
        try:
            self._verify_bearer(bearer, "command")
            self._require_bootstrapped()
            self._check_identity(request)
            self._check_fencing(request, is_transition=False)
            self._require_unexpired_lease()
            replay = self._check_sequence(request)
            if replay is not None:
                return replay
            self._guard_command_admission(request.origin)
        except WorkerProtocolError as err:
            return self._error_reply(M.CommandResponse, err)

        started = _now()
        self._in_flight += 1
        try:
            async with self._command_lock:
                result, active_id, result_class, human_required = await self._execute_command(
                    request
                )
        except WorkerProtocolError as err:
            return self._error_reply(M.CommandResponse, err)
        finally:
            # EVERY exit path, including a Playwright error that is not a
            # WorkerProtocolError: a leaked count here made every later drain
            # wait out its full timeout and abandon the "in-flight" command.
            self._in_flight -= 1
        self._last_activity = _now()

        facts = self._build_event_facts(request, started, result_class)
        resp = M.CommandResponse(
            **self._reply_kwargs(),
            ok=True,
            sequence_applied=request.sequence,
            result=result,
            active_page_id=active_id or self._active_page_id or "",
            page_inventory_revision=self._inventory_revision,
            human_required=human_required,
            event_facts=facts,
        )
        self._admit_sequenced(request, resp)
        return resp

    def _guard_command_admission(self, origin: str) -> None:
        st = self._controller.state
        if self.queue_state == "closed":
            reason = self._closed_reason or "worker_shutting_down"
            raise WorkerProtocolError(reason)  # type: ignore[arg-type]
        if st in ("stopping", "stopped"):
            raise WorkerProtocolError("worker_shutting_down")
        if st == "human_control":
            if origin == "human_boundary":
                return
            raise WorkerProtocolError(
                "browser_controlled_by_human",
                message="the browser is under human control",
                conflicting_handoff_id=self._controller.handoff_id,
            )
        if st in ("handoff_requested", "resume_pending"):
            raise WorkerProtocolError(
                "queue_draining", message="a control transition is draining the queue"
            )
        if st == "agent_control":
            if origin == "system" and self._in_flight > 0:
                raise WorkerProtocolError(
                    "queue_draining", message="health probe refused while a command is in flight"
                )
            return
        raise WorkerProtocolError("not_bootstrapped")

    async def _execute_command(self, request: M.CommandRequest) -> tuple[Any, str | None, str, Any]:
        cmd = request.command
        name = cmd.command
        if name not in C.KNOWN_COMMANDS:
            raise WorkerProtocolError(
                "command_not_supported", message="unknown command discriminator"
            )

        # Resolve the target page.
        target_id = request.page_id or self._active_page_id
        if (
            target_id is None
            or target_id not in self._pages
            or self._pages[target_id].closed_at is not None
        ):
            if name in ("navigate",):
                target_id = self._active_page_id
            else:
                raise WorkerProtocolError("unknown_page", message="page_id names no live page")
        tp = self._pages.get(target_id) if target_id else None
        if tp is not None and self._session is not None:
            self._session.page = tp.page  # point the imported actions at this page
            tp.last_focused_at = _now()

        mgr = self._session_mgr
        rid = self.run_id

        # Page-management commands handled locally.
        if name == "activate_page":
            return await self._cmd_activate_page(cmd), self._active_page_id, "ok", None
        if name == "close_page":
            return await self._cmd_close_page(cmd), self._active_page_id, "ok", None
        if name == "handle_dialog":
            return await self._cmd_handle_dialog(cmd), self._active_page_id, "ok", None
        if name == "wait_for_download":
            return await self._cmd_wait_for_download(cmd), self._active_page_id, "ok", None

        # D5: navigate must not carry session-identity parameters on a persistent run.
        if name == "navigate" and (
            cmd.user_agent is not None or cmd.viewport is not None or cmd.proxy is not None
        ):
            raise WorkerProtocolError(
                "parameter_not_available_on_persistent_run",
                message="user_agent/viewport/proxy are fixed at bootstrap on a persistent run",
            )
        # D3: eval_js authorization is the run policy, never a request field.
        if name == "eval_js" and not (self._policy and self._policy.allow_eval_js):
            raise WorkerProtocolError(
                "eval_js_not_permitted", message="eval_js disabled by run policy"
            )

        # invalid_command_arguments for select_option with neither value nor label.
        if name == "select_option" and cmd.value is None and cmd.label is None:
            raise WorkerProtocolError(
                "invalid_command_arguments", message="select_option needs value or label"
            )

        result = await self._run_action(name, cmd, rid, mgr)
        result_class = self._classify_result(result)
        if self._episode is not None and name == "navigate":
            self._episode.navigation_count += 1
            org = origin_of(getattr(self._session.page, "url", "") if self._session else None)
            if org:
                self._episode.origins.add(org)
        human_required = None
        if (
            (name in {"navigate", "click"} or (name == "type_text" and cmd.press_enter))
            and self.run_mode == "handoff_capable"
            and result_class == "ok"
            and self._session is not None
        ):
            try:
                # A numeric input or a name merely containing ``code`` is not
                # authentication evidence. Those broad selectors classified
                # ordinary ZIP/postal-code fields as MFA and permanently
                # drained an otherwise healthy browser queue. Keep this
                # intentionally conservative: only visible fields carrying an
                # explicit browser OTP contract or a known exact MFA identity
                # may cross the human-control boundary.
                mfa_fields = self._session.page.locator(
                    "#mfacode, input[autocomplete='one-time-code'], "
                    "input[name='otp' i], input[name='otp_code' i], "
                    "input[name='otpCode' i], input[name='verification_code' i], "
                    "input[name='verificationCode' i], input[name='mfa_code' i], "
                    "input[name='mfaCode' i], input[id='otp' i], "
                    "input[id='otp_code' i], input[id='verification_code' i], "
                    "input[id='mfa_code' i]"
                )
                password_fields = self._session.page.locator("input[type='password']")
                captcha_markers = self._session.page.locator(
                    ".g-recaptcha, .h-captcha, [data-sitekey], "
                    "iframe[src*='recaptcha'], iframe[src*='hcaptcha'], "
                    "iframe[src*='turnstile'], #cf-challenge-running, #challenge-form"
                )
                visible_mfa = any(
                    [
                        await mfa_fields.nth(index).is_visible()
                        for index in range(await mfa_fields.count())
                    ]
                )
                visible_password = any(
                    [
                        await password_fields.nth(index).is_visible()
                        for index in range(await password_fields.count())
                    ]
                )
                visible_captcha = any(
                    [
                        await captcha_markers.nth(index).is_visible()
                        for index in range(await captcha_markers.count())
                    ]
                )
                if visible_captcha:
                    human_required = M.HumanRequiredSignal(
                        reason="captcha_required",
                        detected_by="heuristic",
                        safe_origin=origin_of(self._session.page.url) or "",
                        safe_instructions="Complete the anti-bot check in the private browser window.",
                        page_id=self._active_page_id or "",
                        detected_at=_now(),
                        adapter_version=WORKER_VERSION,
                    )
                elif visible_mfa:
                    human_required = M.HumanRequiredSignal(
                        reason="mfa_required",
                        detected_by="heuristic",
                        safe_origin=origin_of(self._session.page.url) or "",
                        safe_instructions="Complete the verification step in the private browser window.",
                        page_id=self._active_page_id or "",
                        detected_at=_now(),
                        adapter_version=WORKER_VERSION,
                    )
                elif visible_password:
                    human_required = M.HumanRequiredSignal(
                        reason="credentials_missing",
                        detected_by="heuristic",
                        safe_origin=origin_of(self._session.page.url) or "",
                        safe_instructions="Enter the sign-in information in the private browser window.",
                        page_id=self._active_page_id or "",
                        detected_at=_now(),
                        adapter_version=WORKER_VERSION,
                    )
            except Exception:
                logger.exception("login-form detection failed")
        return result, self._active_page_id, result_class, human_required

    async def _run_action(self, name: str, cmd: Any, rid: str, mgr: BrowserSessionManager) -> Any:
        # CB-013: pointer and key events shaped like a person's, per run policy.
        human = bool(self._policy.humanize_input) if self._policy is not None else False
        if name == "navigate":
            return await A.navigate(
                cmd.url,
                session_id=rid,
                wait_until=cmd.wait_until,
                timeout_ms=cmd.timeout_ms,
                extract_text=cmd.extract_text,
                mgr=mgr,
            )
        if name == "click":
            return await A.click(
                rid,
                cmd.selector,
                wait_after_ms=cmd.wait_after_ms,
                timeout_ms=cmd.timeout_ms,
                human=human,
                mgr=mgr,
            )
        if name == "fill":
            return await A.fill(
                rid, cmd.selector, cmd.value, timeout_ms=cmd.timeout_ms, human=human, mgr=mgr
            )
        if name == "type_text":
            return await A.type_text(
                rid,
                cmd.selector,
                cmd.text,
                clear_first=cmd.clear_first,
                press_enter=cmd.press_enter,
                timeout_ms=cmd.timeout_ms,
                human=human,
                mgr=mgr,
            )
        if name == "select_option":
            return await A.select_option(
                rid,
                cmd.selector,
                value=cmd.value,
                label=cmd.label,
                timeout_ms=cmd.timeout_ms,
                mgr=mgr,
            )
        if name == "wait_for":
            return await A.wait_for(
                rid,
                selector=cmd.selector,
                text=cmd.text,
                state=cmd.state,
                timeout_ms=cmd.timeout_ms,
                mgr=mgr,
            )
        if name == "get_element":
            return await A.get_element(rid, cmd.selector, include_html=cmd.include_html, mgr=mgr)
        if name == "query_selectors":
            return await A.query_selectors(
                rid,
                cmd.selectors,
                attributes=cmd.attributes,
                limit_per_selector=cmd.limit_per_selector,
                mgr=mgr,
            )
        if name == "eval_js":
            return await A.eval_js(rid, cmd.expression, allow_eval_js=True, mgr=mgr)
        if name == "scroll":
            return await A.scroll(
                rid,
                direction=cmd.direction,
                pixels=cmd.pixels,
                selector=cmd.selector,
                human=human,
                mgr=mgr,
            )
        if name == "get_html":
            return await A.get_html(rid, cap=cmd.cap, mgr=mgr)
        if name == "get_text":
            return await A.get_text(rid, selector=cmd.selector, cap=cmd.cap, mgr=mgr)
        raise WorkerProtocolError("command_not_supported")

    @staticmethod
    def _classify_result(result: Any) -> str:
        if getattr(result, "success", False):
            return "ok"
        et = getattr(result, "error_type", None)
        if et in ("not_found", "timeout", "navigation", "browser", "validation", "blocked"):
            return et
        return "browser"

    async def _cmd_activate_page(self, cmd: Any) -> C.ActivatePageResult:
        tp = self._pages.get(cmd.target_page_id)
        if tp is None or tp.closed_at is not None:
            raise WorkerProtocolError("unknown_page", message="target page is not live")
        self._active_page_id = tp.page_id
        tp.last_focused_at = _now()
        if self._session is not None:
            self._session.page = tp.page
        try:
            await tp.page.bring_to_front()
        except Exception:
            pass
        url = getattr(tp.page, "url", "") or ""
        title = None
        try:
            title = await tp.page.title()
        except Exception:
            title = None
        return C.ActivatePageResult(
            success=True,
            session_id=self.run_id,
            active_page_id=tp.page_id,
            url=safe_url(url),
            title=cap_label(title),
        )

    async def _cmd_close_page(self, cmd: Any) -> C.ClosePageResult:
        tp = self._pages.get(cmd.target_page_id)
        if tp is None:
            raise WorkerProtocolError("unknown_page", message="target page is not live")
        try:
            await tp.page.close()
        except Exception:
            pass
        if tp.closed_at is None:
            tp.closed_at = _now()
            self._bump_inventory()
        if self._active_page_id == tp.page_id:
            self._reconcile_active()
        return C.ClosePageResult(
            success=True,
            session_id=self.run_id,
            closed=True,
            active_page_id=self._active_page_id or "",
        )

    async def _cmd_handle_dialog(self, cmd: Any) -> C.HandleDialogResult:
        td = self._dialogs.get(cmd.dialog_id)
        if td is None:
            raise WorkerProtocolError("unknown_dialog", message="dialog id names no open dialog")
        try:
            if cmd.action == "accept":
                await td.dialog.accept(cmd.prompt_text or "")
            else:
                await td.dialog.dismiss()
        except Exception:
            pass
        td.handled = True
        self._bump_inventory()
        return C.HandleDialogResult(
            success=True, session_id=self.run_id, dialog_id=cmd.dialog_id, handled=True
        )

    async def _cmd_wait_for_download(self, cmd: Any) -> C.DownloadResult:
        dl = self._downloads.get(cmd.download_id)
        if dl is None:
            raise WorkerProtocolError("unknown_page", message="download id names no download")
        try:
            path = await dl.download.path()
            if path:
                data = await asyncio.to_thread(_read_bytes, path)
                dl.byte_count = len(data)
                dl.content_hash = await asyncio.to_thread(_sha256_hex, data)
                dl.state = "completed"
                dl.completed_at = _now()
                # The download really is complete ON THIS HOST, and that is all
                # this reports. There is no upload target on
                # ``WaitForDownloadCommand``, so there is nothing to push the
                # bytes at — and a worker container is ephemeral, so claiming
                # ``uploaded`` here would tell the control plane a file is
                # durably stored when it is one task restart from gone. It stays
                # False, loudly, until the command carries a presigned target.
                dl.uploaded = False
                logger.warning(
                    "download %s completed on the worker but has NO durable "
                    "upload target; the bytes live only in this container "
                    "(%d bytes, sha256=%s)",
                    dl.download_id,
                    dl.byte_count,
                    dl.content_hash,
                )
                self._emit("download_completed", page_id=dl.page_id)
        except Exception:
            dl.state = "failed"
            dl.failure_code = "download_failed"
            self._emit("download_failed", page_id=dl.page_id)
        self._bump_inventory()
        return C.DownloadResult(
            success=dl.state == "completed",
            session_id=self.run_id,
            download_id=dl.download_id,
            suggested_filename=dl.suggested_filename,
            state=dl.state,
            byte_count=dl.byte_count,
            content_hash=dl.content_hash,
            uploaded=dl.uploaded,
        )

    def _build_event_facts(
        self, request: M.CommandRequest, started: datetime, result_class: str
    ) -> M.ActionEventFacts:
        ended = _now()
        cmd = request.command
        selector = getattr(cmd, "selector", None)
        url = getattr(self._session.page, "url", "") if self._session else None
        return M.ActionEventFacts(
            actor="human"
            if request.origin == "human_boundary"
            else ("system" if request.origin == "system" else "agent"),
            action_kind=cmd.command,
            target_description=sanitize_selector_shape(selector),
            safe_url=safe_url(url),
            origin_host=host_of(url),
            started_at=started,
            ended_at=ended,
            duration_ms=int((ended - started).total_seconds() * 1000),
            result_class=result_class,  # type: ignore[arg-type]
            error_code=None,
            chromium_version=self.chromium_version,
            worker_version=self.worker_version,
        )

    # ── operation 5.4: observe ──────────────────────────────────────────────

    @_serialized_control
    async def observe(
        self, request: M.ObserveRequest, *, bearer: str | None = None
    ) -> M.ObserveResponse:
        try:
            self._verify_bearer(bearer, "observe")
            self._require_bootstrapped()
            self._check_identity(request)
            self._check_fencing(request, is_transition=False)
            self._forbid_sequence(request)
        except WorkerProtocolError as err:
            return self._error_reply(M.ObserveResponse, err)
        # observe is strictly READ-ONLY: it reads the registries and page.url/title,
        # and calls no mutating Playwright method (asserted by a conformance test).
        inv = await self._observe_inventory(list(request.include))
        episode = None
        if "human_episode" in request.include and self._episode is not None:
            episode = self._episode_summary()
        return M.ObserveResponse(
            **self._reply_kwargs(), ok=True, page_inventory=inv, human_episode=episode
        )

    async def _observe_inventory(self, include: list[str]) -> M.PageInventory:
        inv = self._build_inventory(include if include else ["pages", "dialogs", "downloads"])
        # A page with a pending (unhandled) dialog blocks its JS, so title() would
        # hang — skip those. observe stays strictly read-only and non-blocking.
        blocked_pages = {d.page_id for d in self._dialogs.values() if not d.handled}
        for rec in inv.pages:
            if rec.is_closed or rec.page_id in blocked_pages:
                continue
            tp = self._pages.get(rec.page_id)
            if tp is None:
                continue
            try:
                rec.title = cap_label(await tp.page.title())
            except Exception:
                pass
        return inv

    def _episode_summary(self) -> M.HumanEpisodeSummary:
        ep = self._episode
        assert ep is not None
        return M.HumanEpisodeSummary(
            handoff_id=ep.handoff_id,
            claimed_at=ep.claimed_at,
            returned_at=ep.returned_at,
            navigation_count=ep.navigation_count,
            pages_opened=ep.pages_opened,
            pages_closed=ep.pages_closed,
            dialogs_opened=ep.dialogs_opened,
            downloads_started=ep.downloads_started,
            pointer_activity_buckets=ep.pointer_buckets,
            keyboard_activity_buckets=ep.keyboard_buckets,
            origins_visited=sorted(ep.origins),
        )

    # ── operation 5.5: capture ──────────────────────────────────────────────

    async def capture(
        self, request: M.CaptureRequest, *, bearer: str | None = None
    ) -> M.CaptureResponse:
        try:
            self._verify_bearer(bearer, "capture")
            self._require_bootstrapped()
            self._check_identity(request)
            self._check_fencing(request, is_transition=False)
            self._require_unexpired_lease()
            replay = self._check_sequence(request)
            if replay is not None:
                return replay
            self._guard_capture_admission(request.reason)
        except WorkerProtocolError as err:
            return self._error_reply(M.CaptureResponse, err)
        # D-10: an observation counts. A person watching through requested
        # screenshots keeps the idle timer from running — otherwise the idle
        # policy would stop a browser someone is looking at.
        self._last_activity = _now()

        if request.kind != "screenshot":
            # trace/video control — off by default; report suppressed rather than error.
            resp = M.CaptureResponse(
                **self._reply_kwargs(),
                ok=True,
                sequence_applied=request.sequence,
                captured=False,
                suppressed_reason="trace_disabled_by_policy"
                if "trace" in request.kind
                else "video_disabled_by_policy",
                artifact=None,
            )
            self._admit_sequenced(request, resp)
            return resp

        target_id = request.page_id or self._active_page_id
        tp = self._pages.get(target_id) if target_id else None
        if tp is None or tp.closed_at is not None:
            return self._error_reply(
                M.CaptureResponse,
                WorkerProtocolError("unknown_page", message="no live page to capture"),
            )

        try:
            png = await tp.page.screenshot(type="png", full_page=request.full_page)
        except Exception:
            return self._error_reply(
                M.CaptureResponse,
                WorkerProtocolError("worker_degraded", message="screenshot failed"),
            )

        content_hash = await asyncio.to_thread(_sha256_hex, png)
        inline = None
        uploaded = False
        if request.upload_target is not None:
            # A real presigned PUT. ``uploaded`` is a DURABILITY CLAIM the control
            # plane records and a person later relies on, so it is set from the
            # transport result and nothing else. (Until 2026-08-23 this branch
            # threw the PNG away and hard-coded True.)
            uploaded = await _upload_presigned_bytes(
                request.upload_target, png, what="capture", timeout_s=60.0
            )
            if not uploaded:
                return self._error_reply(
                    M.CaptureResponse,
                    WorkerProtocolError(
                        "capture_upload_failed",
                        message="capture upload to the presigned target failed",
                    ),
                )
        elif len(png) <= M.INLINE_CAPTURE_CAP and request.return_base64:
            inline = base64.b64encode(png).decode("ascii")
        elif len(png) > M.INLINE_CAPTURE_CAP:
            return self._error_reply(
                M.CaptureResponse,
                WorkerProtocolError(
                    "capture_target_missing",
                    message="artifact over inline cap needs an upload target",
                ),
            )

        artifact = M.CapturedArtifact(
            kind="screenshot",
            media_type="image/png",
            byte_count=len(png),
            content_hash=content_hash,
            uploaded=uploaded,
            image_base64=inline,
            masked_selector_count=len(request.mask_selectors),
            redaction_policy_version=request.redaction_policy_version,
        )
        resp = M.CaptureResponse(
            **self._reply_kwargs(),
            ok=True,
            sequence_applied=request.sequence,
            captured=True,
            suppressed_reason=None,
            artifact=artifact,
        )
        self._admit_sequenced(request, resp)
        return resp

    def _guard_capture_admission(self, reason: str) -> None:
        st = self._controller.state
        if self.queue_state == "closed":
            raise WorkerProtocolError(self._closed_reason or "worker_shutting_down")  # type: ignore[arg-type]
        if st in ("stopping", "stopped"):
            raise WorkerProtocolError("worker_shutting_down")
        if st == "human_control" and reason not in M.HUMAN_BOUNDARY_REASONS:
            raise WorkerProtocolError(
                "browser_controlled_by_human",
                message="only human-boundary captures are allowed during human control",
                conflicting_handoff_id=self._controller.handoff_id,
            )

    # ── operation 5.6: controller_transition ────────────────────────────────

    _LEGAL_TRANSITIONS: dict[str, set[str]] = {
        "agent_control": {"handoff_requested"},
        "handoff_requested": {"human_control", "agent_control"},
        "human_control": {"resume_pending", "agent_control"},
        "resume_pending": {"agent_control"},
    }

    async def _refresh_replayed_human_control(
        self, request: M.ControllerTransitionRequest
    ) -> M.ControllerTransitionResponse | None:
        if not (request.to_state == "human_control" and request.enable_human_input):
            return None
        try:
            if self._prepare_human_control is None or request.rtc_config is None:
                raise RuntimeError("RTC unavailable")
            await self._prepare_rtc(request.rtc_config)
        except Exception:
            self._controller = self._controller.model_copy(
                update={"state": "failed", "human_input_enabled": False}
            )
            self.queue_state, self._closed_reason, self.health = (
                "closed",
                "worker_degraded",
                "degraded",
            )
            return self._error_reply(
                M.ControllerTransitionResponse,
                WorkerProtocolError("worker_degraded", message="RTC replay preparation failed"),
                from_state="failed",
                to_state="failed",
            )
        return None

    @_serialized_control
    async def controller_transition(
        self, request: M.ControllerTransitionRequest, *, bearer: str | None = None
    ) -> M.ControllerTransitionResponse:
        try:
            self._verify_bearer(bearer, "controller_transition")
            self._require_bootstrapped()
            self._check_identity(request)
            self._require_unexpired_lease()
            # transition-specific fencing: token must match; new revision strictly >.
            if (
                not _consttime_eq(request.fencing_token, self.fencing_token)
                or request.fencing_revision < self.fencing_revision
            ):
                raise WorkerProtocolError("stale_fencing_token", message="fencing token is stale")
            replay = self._check_sequence(request)
            if replay is not None:
                if replay.human_input_enabled:
                    failed = await self._refresh_replayed_human_control(request)
                    if failed is not None:
                        return failed
                return replay
            self._validate_transition(request)
        except _Idempotent:
            failed = await self._refresh_replayed_human_control(request)
            if failed is not None:
                return failed
            return M.ControllerTransitionResponse(
                **self._reply_kwargs(),
                ok=True,
                replayed=True,
                sequence_applied=request.sequence,
                from_state=self._controller.state,
                to_state=self._controller.state,
                queue_drained=False,
                human_input_enabled=self._controller.human_input_enabled,
                page_inventory=self._build_inventory(["pages", "dialogs", "downloads"]),
            )
        except WorkerProtocolError as err:
            return self._error_reply(
                M.ControllerTransitionResponse,
                err,
                from_state=self._controller.state,
                to_state=self._controller.state,
            )

        from_state = self._controller.state
        to_state = request.to_state

        # Drain the queue first (concurrency 1 → wait for the in-flight command).
        self.queue_state = "draining"
        drained, abandoned = await self._drain_queue(request.drain_timeout_ms)

        boundary_artifact = None

        if to_state == "human_control":
            # Enter human control: drain → capture boundary → THEN enable input.
            if request.boundary_capture is not None:
                cap = await self.capture(request.boundary_capture, bearer=None)
                boundary_artifact = cap.artifact
            try:
                if self._prepare_human_control is None or request.rtc_config is None:
                    raise RuntimeError("RTC unavailable")
                await self._prepare_rtc(request.rtc_config)
            except Exception:
                self.queue_state = "open"
                return self._error_reply(
                    M.ControllerTransitionResponse,
                    WorkerProtocolError("reopen_required", message="RTC stream preparation failed"),
                    from_state=from_state,
                    to_state=from_state,
                )
            self._episode = _HumanEpisode(request.handoff_id or uuid.uuid4().hex)
            self._controller = self._controller.model_copy(
                update={
                    "state": "human_control",
                    "controller_kind": "human",
                    "controller_ref": request.controller_ref,
                    "handoff_id": request.handoff_id,
                    "since": _now(),
                    "human_input_enabled": bool(request.enable_human_input),
                    "fencing_revision": request.fencing_revision,
                }
            )
        elif from_state == "human_control" or to_state in ("resume_pending", "agent_control"):
            # Leave human control: disable input FIRST → enumerate pages → resume boundary.
            self._controller = self._controller.model_copy(update={"human_input_enabled": False})
            self._reconcile_active()
            if self._episode is not None and to_state == "agent_control":
                self._episode.returned_at = _now()
            if request.boundary_capture is not None:
                cap = await self.capture(request.boundary_capture, bearer=None)
                boundary_artifact = cap.artifact
            self._controller = self._controller.model_copy(
                update={
                    "state": to_state,
                    "controller_kind": "agent" if to_state == "agent_control" else "human",
                    "controller_ref": request.controller_ref,
                    "handoff_id": request.handoff_id,
                    "since": _now(),
                    "fencing_revision": request.fencing_revision,
                }
            )
        else:
            self._controller = self._controller.model_copy(
                update={
                    "state": to_state,
                    "controller_kind": "agent" if to_state == "agent_control" else "human",
                    "controller_ref": request.controller_ref,
                    "handoff_id": request.handoff_id,
                    "since": _now(),
                    "fencing_revision": request.fencing_revision,
                }
            )

        # Rotate the fence — the ONLY door for it.
        self.fencing_token = request.new_fencing_token
        self.fencing_revision = request.new_fencing_revision
        self._controller = self._controller.model_copy(
            update={"fencing_revision": self.fencing_revision}
        )

        # Reopen the queue unless we entered human control (queue stays closed to
        # agent commands there via the admission guard, but is "open" for observe).
        self.queue_state = "open"
        self._closed_reason = ""

        resp = M.ControllerTransitionResponse(
            **self._reply_kwargs(),
            ok=True,
            sequence_applied=request.sequence,
            from_state=from_state,
            to_state=to_state,
            queue_drained=True,
            drained_command_count=drained,
            abandoned_command_count=abandoned,
            human_input_enabled=self._controller.human_input_enabled,
            boundary_artifact=boundary_artifact,
            page_inventory=self._build_inventory(["pages", "dialogs", "downloads"]),
        )
        self._admit_sequenced(request, resp)
        return resp

    def _validate_transition(self, request: M.ControllerTransitionRequest) -> None:
        cur = self._controller.state
        target = request.to_state
        # Idempotent same-state transition.
        if cur == target:
            if request.new_fencing_revision == self.fencing_revision:
                raise _Idempotent()
            raise WorkerProtocolError(
                "controller_transition_conflict", message="same target state, different revision"
            )
        if request.new_fencing_revision <= self.fencing_revision:
            raise WorkerProtocolError(
                "stale_fencing_token", message="new revision must strictly increase"
            )
        # Revoke path: any state → agent_control is always allowed.
        if target == "agent_control":
            return
        # automation_only cannot enter human control.
        if target == "human_control" and self.run_mode == "automation_only":
            raise WorkerProtocolError(
                "illegal_controller_transition",
                message="automation_only cannot enter human control",
            )
        allowed = self._LEGAL_TRANSITIONS.get(cur, set())
        if target not in allowed:
            raise WorkerProtocolError(
                "illegal_controller_transition", message="transition not in the lifecycle machine"
            )

    async def _drain_queue(self, timeout_ms: int) -> tuple[int, int]:
        deadline = asyncio.get_event_loop().time() + timeout_ms / 1000.0
        drained = 0
        while self._in_flight > 0:
            if asyncio.get_event_loop().time() > deadline:
                return drained, self._in_flight  # abandoned = still in flight
            await asyncio.sleep(0.01)
            drained += 0
        return drained, 0

    # ── operation 5.7: checkpoint ───────────────────────────────────────────

    async def checkpoint(
        self, request: M.CheckpointRequest, *, bearer: str | None = None
    ) -> M.CheckpointResponse:
        try:
            self._verify_bearer(bearer, "checkpoint")
            self._require_bootstrapped()
            self._check_identity(request)
            self._check_fencing(request, is_transition=False)
            self._require_unexpired_lease()
            replay = self._check_sequence(request)
            if replay is not None:
                return replay
            if self._controller.state == "human_control":
                raise WorkerProtocolError(
                    "browser_controlled_by_human",
                    message="transition out before checkpoint",
                    conflicting_handoff_id=self._controller.handoff_id,
                )
            if self._checkpoint_in_progress:
                raise WorkerProtocolError(
                    "checkpoint_in_progress",
                    message="another checkpoint is closing and archiving this browser",
                )
        except WorkerProtocolError as err:
            return self._error_reply(M.CheckpointResponse, err, checkpoint_id=request.checkpoint_id)

        self._checkpoint_in_progress = True
        try:
            return await self._checkpoint_exclusive(request)
        finally:
            self._checkpoint_in_progress = False

    async def _checkpoint_exclusive(self, request: M.CheckpointRequest) -> M.CheckpointResponse:
        self.queue_state = "draining"
        await self._drain_queue(request.drain_timeout_ms)

        # Closed-profile only: close Chromium and let SQLite settle before archiving.
        clean = await self._close_context_cleanly()
        if not clean:
            self.queue_state = "open"
            return self._error_reply(
                M.CheckpointResponse,
                WorkerProtocolError(
                    "chromium_unclean_exit", message="Chromium did not exit cleanly"
                ),
                checkpoint_id=request.checkpoint_id,
                chromium_exited_cleanly=False,
            )

        # 🚨 Everything below streams through files, never through RAM. The
        # profile used to be held THREE times on a 4 GiB task (tar bytes,
        # ciphertext, HTTP body); an 85 MB archive is nothing, a 400 MB one was
        # the difference between a save and an OOM kill mid-checkpoint.
        scratch = tempfile.mkdtemp(prefix="checkpoint-", dir=_checkpoint_scratch_dir())
        plaintext_path = os.path.join(scratch, "archive")
        ciphertext_path = os.path.join(scratch, "archive.enc")
        zeroized = request.zeroize_after
        try:
            try:
                plaintext_hash, _plaintext_bytes, archive_format_version = await asyncio.to_thread(
                    _archive_dir_to_file, self._user_data_dir, plaintext_path
                )
            except Exception:
                logger.exception("checkpoint archive failed; the profile on disk is untouched")
                self.queue_state = "open"
                return self._error_reply(
                    M.CheckpointResponse,
                    WorkerProtocolError(
                        "checkpoint_failed", message="archive failed; plaintext preserved"
                    ),
                    checkpoint_id=request.checkpoint_id,
                    chromium_exited_cleanly=True,
                    zeroized=False,
                )
            # Encrypt with the manager-supplied DEK (WS-3 owns the full crypto; the
            # worker holds the plaintext DEK for the archive operation only and zeroizes it).
            nonce = base64.b64decode(request.nonce_b64)
            ciphertext_hash, byte_count, encrypted = await asyncio.to_thread(
                _encrypt_checkpoint_file,
                request.dek_plaintext_b64,
                nonce,
                plaintext_path,
                ciphertext_path,
            )
            # The plaintext archive has served its purpose the moment the
            # ciphertext exists; it never waits around for the upload.
            await asyncio.to_thread(_unlink_quietly, plaintext_path)

            if not encrypted:
                self.queue_state = "open"
                return self._error_reply(
                    M.CheckpointResponse,
                    WorkerProtocolError(
                        "checkpoint_failed", message="checkpoint encryption is unavailable"
                    ),
                    checkpoint_id=request.checkpoint_id,
                    chromium_exited_cleanly=True,
                    zeroized=zeroized,
                )
            uploaded = await _upload_checkpoint_file(
                request.upload_target, ciphertext_path, byte_count
            )
            if not uploaded:
                self.queue_state = "open"
                return self._error_reply(
                    M.CheckpointResponse,
                    WorkerProtocolError(
                        "checkpoint_failed", message="encrypted checkpoint upload failed"
                    ),
                    checkpoint_id=request.checkpoint_id,
                    chromium_exited_cleanly=True,
                    zeroized=zeroized,
                )
        finally:
            shutil.rmtree(scratch, ignore_errors=True)

        try:
            await asyncio.to_thread(
                _write_profile_checkpoint_marker, self._user_data_dir, plaintext_hash
            )
        except OSError:
            # The remote checkpoint is still valid. Missing this local cache
            # marker only makes the next bootstrap perform a full restore.
            logger.warning("could not cache the installed profile checkpoint hash", exc_info=True)

        relaunch = request.mode == "close_and_archive" and request.reason != "stop"
        context_relaunched = False
        if relaunch:
            try:
                await self._launch_context(self._policy, self._display)  # type: ignore[arg-type]
                self.queue_state = "open"
                self._closed_reason = ""
                context_relaunched = True
                # A crashed browser that relaunched here is healthy again — this
                # is the sweep's in-place self-heal (manager: browser_crashed →
                # forced live checkpoint → relaunch → page reopened).
                self.health = "healthy"
                await asyncio.to_thread(_mark_profile_live, self._user_data_dir)
            except Exception:
                logger.exception("Chromium did not relaunch after the checkpoint")
                self.health = "browser_crashed"

        manifest = M.CheckpointManifestFacts(
            checkpoint_id=request.checkpoint_id,
            profile_format_version=1,
            # The format the worker WROTE, not the one the request assumed:
            # a restore sniffs the archive, and the record must say what it is.
            archive_format_version=archive_format_version,
            chromium_version=self.chromium_version,
            key_version=request.key_version,
            plaintext_hash=plaintext_hash,
            ciphertext_hash=ciphertext_hash,
            byte_count=byte_count,
        )
        return M.CheckpointResponse(
            **self._reply_kwargs(),
            ok=True,
            sequence_applied=request.sequence,
            checkpoint_id=request.checkpoint_id,
            chromium_exited_cleanly=True,
            plaintext_hash=plaintext_hash,
            ciphertext_hash=ciphertext_hash,
            byte_count=byte_count,
            uploaded=uploaded,
            manifest=manifest,
            zeroized=zeroized,
            context_relaunched=context_relaunched,
        )

    async def _close_context_cleanly(self) -> bool:
        self._closing_intentionally = True
        try:
            if self._context is not None and self.health != "browser_crashed":
                await self._context.close()
            # A crashed Chromium is already gone: there is nothing to close
            # cleanly, and closing its dead handle would only raise. What is on
            # disk is what the checkpoint archives (Chromium recovers its own
            # journals on the next launch).
            if self._pw is not None:
                await self._pw.stop()
            self._context = None
            self._pw = None
            return True
        except Exception:
            logger.exception("error closing context for checkpoint")
            return False

    def _on_context_closed(self) -> None:
        """Playwright's context "close" event, on OUR loop, for any reason."""
        if self._closing_intentionally or self._terminating:
            return
        if self.health in {"stopped", "stopping"}:
            return
        logger.error(
            "Chromium closed on its own (crash or OOM kill); this worker now reports "
            "browser_crashed and refuses commands until the control plane relaunches it"
        )
        self.health = "browser_crashed"
        self.queue_state = "closed"
        self._closed_reason = "browser_crashed"

    # ── self-protection: termination and the lease watchdog ─────────────────

    async def terminate_gracefully(self, *, reason: str) -> None:
        """SIGTERM (ECS stop, platform patch, scale-in) or a lost control plane.

        Refuse new work, close Chromium CLEANLY so SQLite settles, and leave
        the profile on its shared volume with its live marker: the next worker
        that restores the same checkpoint adopts it instead of losing everything
        since the last save. Idempotent; never raises.
        """
        if self._terminating:
            return
        self._terminating = True
        logger.warning("browser worker terminating (%s): closing Chromium cleanly", reason)
        self.queue_state = "closed"
        self._closed_reason = "worker_shutting_down"
        self.health = "stopping"
        if self._lease_watchdog is not None and self._lease_watchdog is not asyncio.current_task():
            self._lease_watchdog.cancel()
        try:
            await self._close_context_cleanly()
        except Exception:
            logger.exception("Chromium did not close cleanly during termination")
        try:
            await self._close_egress_adapter()
        except Exception:
            logger.exception("egress adapter did not close during termination")
        if self._lock is not None:
            try:
                self._lock.release()
            except Exception:
                logger.warning("profile lock release failed during termination", exc_info=True)
        self.health = "stopped"

    def enable_lease_watchdog(self) -> None:
        """Arm the lease watchdog for this process (see ``_lease_watchdog_loop``)."""
        self._lease_watchdog_enabled = True

    def _start_lease_watchdog(self) -> None:
        if not self._lease_watchdog_enabled:
            return
        if self._lease_watchdog is not None and not self._lease_watchdog.done():
            return
        self._lease_watchdog = asyncio.create_task(
            self._lease_watchdog_loop(), name="cloud-browser-lease-watchdog"
        )

    async def _lease_watchdog_loop(self) -> None:
        """Stop a browser nobody is renewing: a control-plane outage must not
        leave fifty Chromes running with nobody to stop them."""
        while not self._terminating:
            await asyncio.sleep(LEASE_WATCHDOG_TICK_SECONDS)
            if self._lease_watchdog_should_fire(datetime.now(UTC)):
                logger.error(
                    "no lease renewal for %.0f s past expiry: the control plane is gone; "
                    "closing Chromium to keep the profile consistent and ending this task",
                    LEASE_WATCHDOG_GRACE_SECONDS,
                )
                await self.terminate_gracefully(reason="lease_watchdog")
                self._end_process()
                return

    def _lease_watchdog_should_fire(self, now: datetime) -> bool:
        if self._terminating or self.health in {"stopped", "stopping"}:
            return False
        expires = self._lease_expires_at
        if expires is None:
            return False
        return now > expires + timedelta(seconds=LEASE_WATCHDOG_GRACE_SECONDS)

    # ── operation 5.8: shutdown ─────────────────────────────────────────────

    @_serialized_control
    async def shutdown(
        self, request: M.ShutdownRequest, *, bearer: str | None = None
    ) -> M.ShutdownResponse:
        try:
            self._verify_bearer(bearer, "shutdown")
            self._require_not_mid_bootstrap()
            self._require_bootstrapped()
            self._check_identity(request)
            self._check_fencing(request, is_transition=False)
            # shutdown is sequenced (it drains the queue); a sequence is accepted
            # but not replay-cached — a duplicate shutdown is idempotent by state.
        except WorkerProtocolError as err:
            return self._error_reply(M.ShutdownResponse, err)

        emergency = request.reason == "emergency_fence"
        checkpoint_resp = None
        abandoned = 0

        self._controller = self._controller.model_copy(
            update={"state": "stopping", "human_input_enabled": False}
        )
        self.queue_state = "draining"

        if emergency:
            # Skip the drain: input off, Chromium killed, lock released, no checkpoint.
            await self._kill_context()
            uncheckpointed = True
        else:
            _, abandoned = await self._drain_queue(request.drain_timeout_ms)
            if request.final_checkpoint is not None:
                checkpoint_resp = await self.checkpoint(request.final_checkpoint, bearer=None)
                uncheckpointed = not (
                    checkpoint_resp.ok and checkpoint_resp.chromium_exited_cleanly
                )
            else:
                await self._close_context_cleanly()
                uncheckpointed = True

        lock_released = False
        if self._lock is not None:
            self._lock.release()
            lock_released = True

        self._controller = self._controller.model_copy(update={"state": "stopped"})
        self.queue_state = "closed"
        self._closed_reason = "worker_shutting_down"
        self.health = "stopped"
        # The clean-stop paths above close the context without going through
        # ``_kill_context``; the person's computer must stop carrying this run's
        # streams the moment the run is over, on EVERY exit.
        await self._close_egress_adapter()

        return M.ShutdownResponse(
            **self._reply_kwargs(),
            ok=True,
            stopped=True,
            queue_drained=not emergency,
            abandoned_command_count=abandoned,
            checkpoint=checkpoint_resp,
            uncheckpointed_state=uncheckpointed,
            host_lock_released=lock_released,
            zeroized=checkpoint_resp.zeroized if checkpoint_resp else False,
        )

    async def _kill_context(self) -> None:
        self._closing_intentionally = True
        try:
            if self._context is not None:
                await self._context.close()
        except Exception:
            pass
        try:
            if self._pw is not None:
                await self._pw.stop()
        except Exception:
            pass
        self._context = None
        self._pw = None
        await self._close_egress_adapter()

    # ── events ──────────────────────────────────────────────────────────────

    _SECURITY_EVENTS = frozenset({"handoff_requested", "browser_crashed", "egress_blocked"})

    def _emit(
        self,
        kind: str,
        *,
        page_id: str | None = None,
        safe_url: str | None = None,
        detail_code: str | None = None,
    ) -> None:
        ev = M.WorkerEvent(
            event_id=uuid.uuid4().hex,
            run_id=self.run_id,
            profile_id=self.profile_id,
            worker_id=self.worker_id,
            fencing_revision=self.fencing_revision,
            emitted_at=_now(),
            kind=kind,  # type: ignore[arg-type]
            page_id=page_id,
            safe_url=safe_url,
            detail_code=detail_code,
        )
        # Buffer with the security-event protection: overflow drops the oldest
        # NON-security event first and never a security event (S2 §6).
        if len(self._event_buffer) >= M.EVENT_BUFFER_CAP:
            for i, buffered in enumerate(self._event_buffer):
                if buffered.kind not in self._SECURITY_EVENTS:
                    self._event_buffer.pop(i)
                    break
            else:
                self._event_buffer.pop(0)
        self._event_buffer.append(ev)
        if self._event_sink is not None:
            try:
                self._event_sink(ev)
            except Exception:
                logger.debug("event sink raised; buffered for retry")

    def emit_handoff_requested(self, signal: M.HumanRequiredSignal) -> None:
        """Public seam: an adapter/heuristic detected a typed human-required reason."""
        self._emit(
            "handoff_requested", page_id=signal.page_id, safe_url=None, detail_code=signal.reason
        )


# ── module helpers ──────────────────────────────────────────────────────────


class _EgressGuardFailed(Exception):
    pass


class _Idempotent(WorkerProtocolError):
    """Internal sentinel: a same-state, same-revision transition is a replay."""

    def __init__(self) -> None:  # pragma: no cover - control flow only
        Exception.__init__(self, "idempotent transition")
        self.code = "controller_transition_conflict"  # not used; caught before to_error
        self.http_status = 200
        self.retryable = False
        self.message = "idempotent"
        self.retry_after_ms = None
        self.current_fencing_revision = None
        self.current_controller = None
        self.last_sequence_applied = None
        self.conflicting_handoff_id = None


def _consttime_eq(a: str, b: str) -> bool:
    import hmac

    return hmac.compare_digest(a or "", b or "")


def _resolve_chromium_executable() -> str | None:
    """The full Chromium ``chrome`` binary under PLAYWRIGHT_BROWSERS_PATH, if any.

    Excludes ``chromium_headless_shell-*`` — the full binary runs headless too and
    is the one the WS-0 proofs used for the headed handoff path, so both run modes
    use one binary. Returns ``None`` when nothing is pre-provisioned (Playwright's
    own bundled browser is then used)."""
    import glob

    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    candidates = [
        p
        for p in glob.glob(os.path.join(base, "chromium-*", "chrome-linux", "chrome"))
        if "headless_shell" not in p
    ]
    return sorted(candidates)[-1] if candidates else None


def _read_bytes(path: str) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def _sha256_hex(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


#: One read/write unit for every streaming checkpoint step. 1 MiB keeps the
#: worker's peak RSS for a save independent of the profile's size.
_CHECKPOINT_CHUNK_BYTES = 1 << 20
#: The zstd frame magic; a restore sniffs it to tell the two archive formats apart.
_ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"
#: ``archive_format_version`` values: 1 = plain tar (every checkpoint before
#: 2026-09-20), 2 = tar piped through zstd. Both restore; only 2 is written.
ARCHIVE_FORMAT_TAR = 1
ARCHIVE_FORMAT_TAR_ZSTD = 2
_ZSTD_LEVEL = 6
_AES_GCM_TAG_BYTES = 16
_zstd_missing_announced = False


def _checkpoint_scratch_dir() -> str:
    """Container-local scratch for the archive and its ciphertext (never EFS)."""
    override = os.environ.get("MATRX_CHECKPOINT_SCRATCH_DIR")
    if override:
        os.makedirs(override, mode=0o700, exist_ok=True)
        return override
    return tempfile.gettempdir()


def _unlink_quietly(path: str) -> None:
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


class _HashingWriter:
    """A write sink that hashes and counts what passes through it."""

    def __init__(self, raw: Any) -> None:
        self._raw = raw
        self.hasher = hashlib.sha256()
        self.total = 0

    def write(self, data: bytes) -> int:
        self.hasher.update(data)
        self.total += len(data)
        self._raw.write(data)
        return len(data)

    def flush(self) -> None:
        self._raw.flush()


def _zstd_compressor():  # noqa: ANN202
    """The zstd compressor, or None (announced ONCE) when the wheel is absent."""
    global _zstd_missing_announced
    try:
        import zstandard
    except Exception:
        if not _zstd_missing_announced:
            _zstd_missing_announced = True
            logger.warning(
                "zstandard is not installed in this worker image; checkpoints are written "
                "as uncompressed tar (archive_format_version=1). Install "
                "matrx-scraper[cloud_browser] to cut checkpoint size by ~4x."
            )
        return None
    return zstandard.ZstdCompressor(level=_ZSTD_LEVEL)


def _archive_dir_to_file(user_data_dir: str, dest_path: str) -> tuple[str, int, int]:
    """Stream the closed profile into ``dest_path``: tar, zstd when available.

    Returns ``(plaintext_hash, plaintext_byte_count, archive_format_version)``.
    The hash is over the archive bytes exactly as written (tar+zstd for
    version 2), which is what the restore verifies before it extracts. The
    member layout is ``profile/<relative path>``; regenerable Chromium caches
    are excluded through the ONE shared predicate, symlinks are dropped (the
    restore refuses them anyway) and ``dest_path`` is created mode 0600.
    """
    root = Path(user_data_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"profile directory missing: {user_data_dir}")
    fd = os.open(dest_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as raw:
        sink = _HashingWriter(raw)
        compressor = _zstd_compressor()
        if compressor is None:
            archive_format_version = ARCHIVE_FORMAT_TAR
            with tarfile.open(fileobj=sink, mode="w|", format=tarfile.PAX_FORMAT) as tar:  # type: ignore[arg-type]
                _add_profile_members(tar, root)
        else:
            archive_format_version = ARCHIVE_FORMAT_TAR_ZSTD
            with compressor.stream_writer(sink, closefd=False) as zwriter:
                with tarfile.open(fileobj=zwriter, mode="w|", format=tarfile.PAX_FORMAT) as tar:
                    _add_profile_members(tar, root)
        sink.flush()
    return sink.hasher.hexdigest(), sink.total, archive_format_version


def _add_profile_members(tar: tarfile.TarFile, root: Path) -> None:
    tar.add(root, arcname="profile", recursive=False)
    for entry in sorted(root.rglob("*")):
        rel = entry.relative_to(root).as_posix()
        if _checkpoint_path_is_excluded(rel):
            continue
        if entry.is_symlink():
            continue
        if entry.is_dir() or entry.is_file():
            tar.add(entry, arcname=f"profile/{rel}", recursive=False)


def _archive_dir(user_data_dir: str) -> bytes:
    """The archive as bytes — a convenience over the streaming writer for
    callers that want to inspect a small profile (tests). Production never
    holds an archive in memory; see ``_archive_dir_to_file``."""
    with tempfile.TemporaryDirectory(prefix="archive-") as scratch:
        path = os.path.join(scratch, "archive")
        _archive_dir_to_file(user_data_dir, path)
        return Path(path).read_bytes()


def _open_archive_for_reading(path: str) -> tarfile.TarFile:
    """A streaming tar reader for either archive format, decided by magic bytes."""
    handle = open(path, "rb")  # noqa: SIM115 — owned by the TarFile
    magic = handle.read(len(_ZSTD_MAGIC))
    handle.seek(0)
    if magic == _ZSTD_MAGIC:
        import zstandard

        reader = zstandard.ZstdDecompressor().stream_reader(handle, closefd=True)
        return tarfile.open(fileobj=reader, mode="r|")
    return tarfile.open(fileobj=handle, mode="r|")


def _encrypt(dek: bytes, nonce: bytes, plaintext: bytes) -> tuple[bytes, str, bool]:
    """AES-256-GCM if ``cryptography`` is available; otherwise the plaintext is
    returned unencrypted with a distinct hash (a hook, not the WS-3 crypto engine —
    WS-3 owns the real encrypt/verify/upload)."""
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM

        ct = AESGCM(dek).encrypt(nonce, plaintext, None)
        return ct, hashlib.sha256(ct).hexdigest(), True
    except Exception:
        return plaintext, hashlib.sha256(b"noenc:" + plaintext).hexdigest(), False


def _encrypt_file_streaming(
    dek: bytes, nonce: bytes, plaintext_path: str, ciphertext_path: str
) -> tuple[str, int, bool]:
    """AES-256-GCM over a file, chunk by chunk: ``ciphertext || tag`` — byte-for-
    byte what ``AESGCM.encrypt`` produces, so every existing restore reads it.
    Returns ``(ciphertext_hash, ciphertext_byte_count, encrypted)``."""
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    except Exception:
        hasher = hashlib.sha256(b"noenc:")
        total = 0
        fd = os.open(ciphertext_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "wb") as out, open(plaintext_path, "rb") as src:
            while block := src.read(_CHECKPOINT_CHUNK_BYTES):
                hasher.update(block)
                out.write(block)
                total += len(block)
        return hasher.hexdigest(), total, False
    encryptor = Cipher(algorithms.AES(dek), modes.GCM(nonce)).encryptor()
    hasher = hashlib.sha256()
    total = 0
    fd = os.open(ciphertext_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as out, open(plaintext_path, "rb") as src:
        while block := src.read(_CHECKPOINT_CHUNK_BYTES):
            chunk = encryptor.update(block)
            hasher.update(chunk)
            out.write(chunk)
            total += len(chunk)
        tail = encryptor.finalize() + encryptor.tag
        hasher.update(tail)
        out.write(tail)
        total += len(tail)
    return hasher.hexdigest(), total, True


def _zeroize(dek: bytearray) -> None:
    for index in range(len(dek)):
        dek[index] = 0


def _encrypt_checkpoint(
    dek_plaintext_b64: str, nonce: bytes, plaintext: bytes
) -> tuple[str, bytes, str, bool]:
    """Hash and encrypt a checkpoint entirely outside the worker event loop.

    ``asyncio.to_thread`` cancellation does not stop already-submitted work.  The
    thread therefore owns the mutable DEK and zeroizes it in ``finally``; a
    cancelled request cannot race the event-loop coroutine into clearing a key
    before encryption reads it, nor leave the worker-owned buffer uncleared.
    """
    dek = bytearray(base64.b64decode(dek_plaintext_b64))
    try:
        plaintext_hash = _sha256_hex(plaintext)
        ciphertext, ciphertext_hash, encrypted = _encrypt(bytes(dek), nonce, plaintext)
        return plaintext_hash, ciphertext, ciphertext_hash, encrypted
    finally:
        _zeroize(dek)


def _encrypt_checkpoint_file(
    dek_plaintext_b64: str, nonce: bytes, plaintext_path: str, ciphertext_path: str
) -> tuple[str, int, bool]:
    """``_encrypt_checkpoint`` for files: the thread owns and zeroizes the DEK."""
    dek = bytearray(base64.b64decode(dek_plaintext_b64))
    try:
        return _encrypt_file_streaming(bytes(dek), nonce, plaintext_path, ciphertext_path)
    finally:
        _zeroize(dek)


def _decrypt_and_verify_checkpoint_file(
    restore: M.CheckpointRestore, ciphertext_path: str, plaintext_path: str
) -> None:
    """Verify the ciphertext hash, decrypt chunk by chunk, verify the plaintext
    hash — in one thread that owns and always clears the DEK, never holding
    more than one chunk of either side in memory."""
    dek = bytearray(base64.b64decode(restore.dek_plaintext_b64))
    try:
        size = os.path.getsize(ciphertext_path)
        if size < _AES_GCM_TAG_BYTES:
            raise ValueError("checkpoint ciphertext too short")
        hasher = hashlib.sha256()
        with open(ciphertext_path, "rb") as src:
            while block := src.read(_CHECKPOINT_CHUNK_BYTES):
                hasher.update(block)
        if hasher.hexdigest() != restore.ciphertext_hash:
            raise ValueError("checkpoint ciphertext hash mismatch")

        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

        with open(ciphertext_path, "rb") as src:
            src.seek(size - _AES_GCM_TAG_BYTES)
            tag = src.read(_AES_GCM_TAG_BYTES)
        decryptor = Cipher(
            algorithms.AES(bytes(dek)), modes.GCM(base64.b64decode(restore.nonce_b64), tag)
        ).decryptor()
        plaintext_hasher = hashlib.sha256()
        fd = os.open(plaintext_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "wb") as out, open(ciphertext_path, "rb") as src:
            remaining = size - _AES_GCM_TAG_BYTES
            while remaining > 0:
                block = src.read(min(_CHECKPOINT_CHUNK_BYTES, remaining))
                if not block:
                    raise ValueError("checkpoint ciphertext truncated")
                remaining -= len(block)
                chunk = decryptor.update(block)
                plaintext_hasher.update(chunk)
                out.write(chunk)
            chunk = decryptor.finalize()  # raises InvalidTag on any tampering
            plaintext_hasher.update(chunk)
            out.write(chunk)
        if plaintext_hasher.hexdigest() != restore.plaintext_hash:
            raise ValueError("checkpoint plaintext hash mismatch")
    finally:
        _zeroize(dek)


def _decrypt_and_verify_checkpoint(restore: M.CheckpointRestore, ciphertext: bytes) -> bytes:
    """Verify and decrypt in one thread that owns and always clears the DEK."""
    dek = bytearray(base64.b64decode(restore.dek_plaintext_b64))
    try:
        if _sha256_hex(ciphertext) != restore.ciphertext_hash:
            raise ValueError("checkpoint ciphertext hash mismatch")

        from cryptography.hazmat.primitives.ciphers.aead import AESGCM

        plaintext = AESGCM(bytes(dek)).decrypt(
            base64.b64decode(restore.nonce_b64), ciphertext, None
        )
        if _sha256_hex(plaintext) != restore.plaintext_hash:
            raise ValueError("checkpoint plaintext hash mismatch")
        return plaintext
    finally:
        _zeroize(dek)


async def _restore_profile(user_data_dir: str, restore: M.CheckpointRestore) -> None:
    """Bound the response, but never abandon a profile filesystem thread.

    ``asyncio.to_thread`` cannot kill an active decrypt/install/marker write.
    On a deadline or owner cancellation we therefore wait for that retained
    task before allowing the bootstrap owner to release the profile lock. A
    hung filesystem operation deliberately keeps the worker busy; capacity is
    safer than concurrent mutation of a canonical browser profile.
    """
    restore_task = asyncio.create_task(
        _restore_profile_once(user_data_dir, restore), name="cloud-browser-profile-restore"
    )
    try:
        async with asyncio.timeout(M.CHECKPOINT_RESTORE_TOTAL_TIMEOUT_SECONDS):
            await asyncio.shield(restore_task)
    except (TimeoutError, asyncio.CancelledError):
        await asyncio.shield(restore_task)
        raise


async def _restore_profile_once(user_data_dir: str, restore: M.CheckpointRestore) -> None:
    """Download, authenticate, and safely replace a closed profile directory."""
    if await asyncio.to_thread(_profile_checkpoint_matches, user_data_dir, restore.plaintext_hash):
        return
    if await asyncio.to_thread(_adopt_live_profile, user_data_dir, restore.plaintext_hash):
        return
    scratch = tempfile.mkdtemp(prefix="restore-", dir=_checkpoint_scratch_dir())
    ciphertext_path = os.path.join(scratch, "archive.enc")
    plaintext_path = os.path.join(scratch, "archive")
    try:
        await _download_to_file(restore, ciphertext_path)
        await asyncio.to_thread(
            _decrypt_and_verify_checkpoint_file, restore, ciphertext_path, plaintext_path
        )
        await asyncio.to_thread(_unlink_quietly, ciphertext_path)
        await asyncio.to_thread(_install_restored_profile_from_file, user_data_dir, plaintext_path)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    await asyncio.to_thread(_write_profile_checkpoint_marker, user_data_dir, restore.plaintext_hash)


async def _download_to_file(restore: M.CheckpointRestore, path: str) -> None:
    """Stream the presigned download to disk; the whole archive never sits in RAM."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as out:
        async with httpx.AsyncClient(timeout=M.CHECKPOINT_RESTORE_TOTAL_TIMEOUT_SECONDS) as client:
            async with client.stream(
                "GET", restore.download_url, headers=restore.headers
            ) as response:
                response.raise_for_status()
                async for block in response.aiter_bytes(_CHECKPOINT_CHUNK_BYTES):
                    out.write(block)


def _profile_checkpoint_matches(user_data_dir: str, plaintext_hash: str) -> bool:
    try:
        return (
            Path(user_data_dir, _PROFILE_CHECKPOINT_MARKER).read_text(encoding="utf-8").strip()
            == plaintext_hash
        )
    except (FileNotFoundError, OSError):
        return False


def _profile_live_base(user_data_dir: str) -> str | None:
    """The checkpoint hash the on-disk profile descends from, or None."""
    try:
        return Path(user_data_dir, _PROFILE_LIVE_MARKER).read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError):
        return None


def _mark_profile_live(user_data_dir: str) -> None:
    """Chromium is now running on this directory: it has moved past the
    checkpoint whose hash the checkpoint marker held. Record that base and
    drop the checkpoint marker in one step."""
    try:
        base = Path(user_data_dir, _PROFILE_CHECKPOINT_MARKER).read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError):
        # No checkpoint marker: either an adopted profile (keep the lineage it
        # already records) or a brand-new one ("").
        base = _profile_live_base(user_data_dir) or ""
    marker = Path(user_data_dir, _PROFILE_LIVE_MARKER)
    try:
        temporary = marker.with_name(f"{marker.name}.{uuid.uuid4().hex}.tmp")
        temporary.write_text(f"{base}\n", encoding="utf-8")
        os.chmod(temporary, 0o600)
        os.replace(temporary, marker)
    except OSError:
        logger.warning("could not write the live-profile marker", exc_info=True)
    _remove_profile_checkpoint_marker(user_data_dir)


def _adopt_live_profile(user_data_dir: str, plaintext_hash: str) -> bool:
    """Keep the profile a previous task left on the shared volume when it
    descends from the very checkpoint being restored — it holds every sign-in
    and page state made AFTER that checkpoint, which a download would erase.

    A different base means a newer checkpoint exists (another task saved
    since); then the download wins. Chromium's stale single-instance lock files
    from the dead task are removed so the launch does not think the profile is
    in use.
    """
    if _profile_live_base(user_data_dir) != plaintext_hash:
        return False
    if not os.path.isdir(user_data_dir):
        return False
    for name in _CHROMIUM_SINGLETON_FILES:
        try:
            os.unlink(os.path.join(user_data_dir, name))
        except FileNotFoundError:
            pass
        except OSError:
            logger.warning(
                "could not remove stale %s from the adopted profile", name, exc_info=True
            )
    logger.warning(
        "adopting the profile the previous worker left on disk: it descends from the "
        "checkpoint being restored (%s…) and holds work made after it",
        plaintext_hash[:12],
    )
    return True


def _send_self_sigterm() -> None:
    import signal

    os.kill(os.getpid(), signal.SIGTERM)


def _write_profile_checkpoint_marker(user_data_dir: str, plaintext_hash: str) -> None:
    marker = Path(user_data_dir, _PROFILE_CHECKPOINT_MARKER)
    temporary = marker.with_name(f"{marker.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(f"{plaintext_hash}\n", encoding="utf-8")
    os.chmod(temporary, 0o600)
    os.replace(temporary, marker)


def _remove_profile_checkpoint_marker(user_data_dir: str) -> None:
    try:
        Path(user_data_dir, _PROFILE_CHECKPOINT_MARKER).unlink()
    except FileNotFoundError:
        pass


def _install_restored_profile(user_data_dir: str, plaintext: bytes) -> None:
    """``_install_restored_profile_from_file`` for an in-memory archive (tests)."""
    with tempfile.TemporaryDirectory(prefix="restore-bytes-") as scratch:
        path = os.path.join(scratch, "archive")
        Path(path).write_bytes(plaintext)
        _install_restored_profile_from_file(user_data_dir, path)


def _install_restored_profile_from_file(user_data_dir: str, archive_path: str) -> None:
    """Extract and atomically install one verified profile without copying it twice.

    The profile volume is EFS.  Extracting into an EFS sibling and then using
    ``copytree`` made every restart rewrite the entire archive a second time,
    blocked the worker event loop, and let ECS kill the only worker as
    unhealthy.  The sibling is already on the same filesystem, so a rename is
    the correct constant-time cutover.  Keep the prior directory as a rollback
    sibling until the new one is in place.
    """

    parent = os.path.dirname(user_data_dir.rstrip(os.sep))
    os.makedirs(parent, mode=0o700, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="profile-restore-", dir=parent) as temporary:
        # One streaming pass: each member is checked, then extracted. A
        # refused member aborts the whole restore (the temporary dir goes with
        # it) — nothing partially unsafe ever reaches the profile directory.
        with _open_archive_for_reading(archive_path) as archive:
            for member in archive:
                parts = member.name.split("/")
                if member.name.startswith("/") or ".." in parts or member.issym() or member.islnk():
                    raise ValueError("unsafe checkpoint archive member")
                target = os.path.realpath(os.path.join(temporary, member.name))
                if os.path.commonpath([os.path.realpath(temporary), target]) != os.path.realpath(
                    temporary
                ):
                    raise ValueError("checkpoint archive member escapes restore directory")
                archive.extract(member, temporary, filter="data")
        restored = os.path.join(temporary, "profile")
        if not os.path.isdir(restored):
            raise ValueError("checkpoint profile directory missing")
        backup = os.path.join(parent, f".profile-replaced-{uuid.uuid4().hex}")
        had_existing = os.path.isdir(user_data_dir)
        if had_existing:
            os.rename(user_data_dir, backup)
        try:
            os.rename(restored, user_data_dir)
            os.chmod(user_data_dir, 0o700)
        except Exception:
            if had_existing and not os.path.exists(user_data_dir):
                os.rename(backup, user_data_dir)
            raise
        if had_existing:
            try:
                shutil.rmtree(backup)
            except OSError:
                # Chromium can briefly retain BrowserMetrics as a mount-like
                # resource after shutdown.  The new profile is already live;
                # failure to reap the rollback copy must not turn a successful
                # atomic restore into a bootstrap failure.  A later sweep can
                # remove this hidden, non-canonical backup once the kernel
                # releases it.
                logger.warning(
                    "restored profile installed but prior profile cleanup is deferred",
                    extra={"backup_path": backup},
                    exc_info=True,
                )
