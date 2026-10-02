"""``PROBE_MODE=offline`` and ``probe sync``: train with no API, deliver later (plan 2.12).

W&B's ``WANDB_MODE=offline`` + ``wandb sync`` shape. ``probe.init(mode="offline")``
makes NO network call: it mints the run's 0268 ``creation_key``, journals a
``create_run`` op FIRST in a queue of its own, and hands back a run whose writes
(``log``, ``span``, ``log_artifact``, ``finish``, ...) are journaled behind it,
addressed to ``local:<creation_key>``. ``probe sync`` later delivers the queue
with whoever is logged in there: the create (idempotent by its key), then every
write with ``local:<key>`` rewritten to the run's real id, then the queued finish
that closes the run with the client's own end time.

THE QUEUE, one directory per run, self-contained so it can be copied off an
air-gapped node::

    <outbox>/offline/<creation_key>/    (the outbox ROOT, also under torchrun/SLURM)
        offline.json        the manifest: key, where it was recorded, by whom
        ops/ failed/ blobs/ the ordinary journal layout (blobs = staged bytes)
        local_runs.json     key -> server id, written atomically when the
                            create lands, BEFORE its op is dequeued

ISOLATION. Nothing but ``probe sync`` drains these directories: the detached
worker and every in-process drain work on the outbox root's own ``ops/`` and
never look into ``offline/``, and the run's client has a transport that refuses
every request without touching a socket (:class:`OfflineTransport`), so no
fallback path can reach the network either.

IDENTITY. The manifest records the base URL and login context it was recorded
under, and the tenant and user the machine was logged in as (read from the local
identity cache, so unknown if this machine never reached the API under its
credential). ``probe sync`` refuses a queue recorded against another base URL,
or -- when its tenant is unknown -- under another login context, unless told
``--allow-mismatch``; a queue recorded for another tenant is refused always.
Any writer of the same tenant may sync it: the run's ``created_by`` is the
syncer and ``metadata.offline_owner`` names the recorder. A queue whose tenant
is unknown syncs into the syncer's with a warning (stderr and the JSON), and its
``offline_owner`` reads ``"unknown"``.

CONFIG. ``update_config`` / ``run.config.x = ...`` / ``run.config.update(...)``
queue their merge like any write; ``probe sync`` checks the SERVER it delivers
to for ``run_config_merge`` and says so when it lacks it (a sync that cannot
store them is not clean).

``PROBE_INIT_FALLBACK=offline`` continues offline when an online ``init()``
runs out of its budget. A create it had already sent, and got no run back for,
is recorded as an offline create UNDER THE SAME KEY, with the sent request kept
beside it. ``probe sync`` sends the offline create first; only when the server
answers that the key already made a run (422 ``creation_key_reused``: the online
create landed and its answer was lost) does it replay the kept request verbatim
and deliver onto that run. So a create that landed is found, not duplicated,
and one that did not becomes a real offline run with its real start -- whatever
the failure looked like from the client (a lost answer, a gateway 503, a
refused connection). The fallback does not engage (init raises) when the create
DID come back (init failed after it: an offline copy would be a second run),
or when offline cannot do what init was asked: an ``on_conflict`` only the
server can decide, including the default (``"auto"``) with an ``external_id``,
which online resumes a crashed run of that id.

KNOWN RISK of the fallback: when the online create landed, the server holds an
ordinary heartbeat-owned run whose writer then went offline. Nothing reaches
the server again until ``probe sync``, so the reaper marks that run ``crashed``
about 15 minutes after init and queues a crash notice (the email itself is held
back by the 3 h crash-email floor, ``CRASH_NOTIFICATION_MIN_RUN_SECONDS``: the
run is minutes old when reaped, unless an operator lowered the floor). ``probe
sync`` then delivers its data and its queued close sets the real final status.
No server-side marker can prevent this: the server hears nothing in between.

A recording KILLED before its close (SIGKILL, OOM) queues no close: after sync
its run reads ``running`` until the server's sync grace (7 days) ends and the
reaper closes it. For the same grace the server refuses a requeue TAKEOVER of
the run (a relaunch with its ``external_id`` gets its ``on_conflict`` answer,
not the run), so a slow or stalled sync is never fenced by a new attempt. Once a
later attempt RESUMES the run online (``probe sync`` itself never reopens), it is
an ordinary online run again: reaped and taken over as usual.

SCALE. Each write is one op file while recording and one request at sync: a
1M-step run is ~1M files and ~1M POSTs. The outbox's coalesced drain (plan 1.2)
does not merge an offline run's metric ops yet: they address ``local:<key>``,
which its merge key refuses (`journal._merge_key` takes a run id only).

READS AND WRITES (lineage plan 3, F6). What the run reads and writes is
recorded exactly as online (:mod:`probe.sdk.inputs`) and queued at the close
as ``POST /v1/runs/local:<key>/inputs`` and ``.../outputs``, behind the run's
other writes and ahead of its close. ``probe sync`` checks the server it
delivers to for ``run_inputs`` / ``run_outputs`` and drops (and says so) a list
that server cannot take, instead of dead-lettering it. Every time in those
lists is one the recording machine OBSERVED (a read's first sight, a write's
first open and final mtime), so matching never leans on the synced run's
``created_at``, which is the sync's.

Not in this version: the code snapshot, output capture (the file uploads) and
the hardware rail are skipped for an offline run (named once on stderr and in
the run's ``metadata.offline.skipped``); they need network round trips of
their own.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

import httpx

from . import errors
from . import safe_warn as _diagnostics
from .client import Client
from .config import Settings
from .config import resolve as resolve_settings
from .durable import now_iso, write_text_atomic
from .journal import Journal, default_root
from .run import Run, _now, _summary_wire, _UNSET
from .transport import Transport

OFFLINE_DIRNAME = "offline"
MANIFEST_NAME = "offline.json"
MAPPING_NAME = "local_runs.json"
MANIFEST_SCHEMA = "probe.offline/1"
LOCAL_PREFIX = "local:"
#: The journal op kind that opens an offline run. Only offline queues carry it,
#: and only `probe sync` drains them, so no older worker ever meets it.
CREATE_KIND = "create_run"
FALLBACK_ENV = "PROBE_INIT_FALLBACK"
#: `metadata.offline_owner` when the recording machine had no cached identity.
UNKNOWN_OWNER = "unknown"
#: What an offline run cannot do yet (see the module docstring). "outputs" is
#: output capture's file uploads; the run's reads and writes ARE recorded.
SKIPPED_CAPTURE = ("code_snapshot", "outputs", "hardware")
#: The lineage lists an offline run queues, by the feature a sync server must
#: declare to take them (`sync_dir` checks).
LINEAGE_ROUTES = {"run_inputs": "inputs", "run_outputs": "outputs"}

#: `probe.init()` keywords an offline run records for its create.
_CREATE_FIELDS = (
    "name",
    "slug",
    "description",
    "notes",
    "source",
    "external_id",
    "parent_run_id",
    "parent_relation",
    "parent_provenance",
    "group_id",
    "config",
    "tags",
    "metadata",
    "labeled_point_budget",
    "authored_by",
)
#: Keywords that choose WHERE the run lives, resolved at sync.
_HOME_FIELDS = ("project", "experiment", "question", "experiment_name")
#: Keywords whose feature an offline run skips (warned once, never an error).
#: `capture_reads`, `capture_outputs` and `ignore` shape its read and write
#: recording; `probe.init` takes them before this sees `kw`.
_SKIPPED_FIELDS = ("hw", "snapshot", "outputs")
#: `on_conflict` values an offline run can honour at sync.
_OFFLINE_CONFLICT = ("error", "supersede")


def offline_root(base: str | os.PathLike | None = None) -> Path:
    """Where this machine's offline runs queue: ``<outbox>/offline``.

    At the outbox ROOT, never under a torchrun/SLURM rank's ``rank-N/``
    (`journal.default_root`): `probe sync` usually runs where no RANK is set (a
    login node, a later shell), and each run already has a directory of its
    own, so the per-rank split buys nothing here."""
    return (Path(base).expanduser() if base is not None else default_root()) / OFFLINE_DIRNAME


def local_ref(key: str) -> str:
    return f"{LOCAL_PREFIX}{key}"


# -- no network, by construction ----------------------------------------------
class OfflineTransport(Transport):
    """A transport that refuses every request without touching a socket.

    The run's writes are journaled (the client is async), so the only callers
    that reach here are fail-open paths that would otherwise go to the network
    -- a sync write, a read, a feature probe. Each one fails at once with a
    TransportError (no retry, no sleep) and its fail-open fallback journals or
    skips. The underlying httpx client is a MockTransport that raises too, so
    even a code path that bypassed these methods could not send."""

    def __init__(self, settings: Settings):
        from .tls import ssl_context

        http = httpx.Client(
            base_url=settings.base_url or "http://offline.invalid",
            transport=httpx.MockTransport(self._refuse),
            # Never used (nothing is sent), but every client in the package
            # carries the one shared trust (plan item l).
            verify=ssl_context(),
        )
        super().__init__(settings, client=http, max_retries=0)
        #: How many requests were refused -- evidence for tests and doctor.
        self.refused = 0

    @staticmethod
    def _refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("offline mode: no network", request=request)

    def _offline(self, what: str) -> errors.TransportError:
        self.refused += 1
        return errors.TransportError(
            f"{what}: not sent -- this run is offline (PROBE_MODE=offline); "
            "`probe sync` delivers it later"
        )

    def request(self, method: str, path: str, **_kw: Any) -> httpx.Response:
        raise self._offline(f"{method} {path}")

    def put_url(self, url: str, *_a: Any, **_kw: Any) -> None:
        raise self._offline("PUT <blob>")

    def put_file(self, url: str, *_a: Any, **_kw: Any) -> None:
        raise self._offline("PUT <blob>")

    def put_fileobj(self, url: str, *_a: Any, **_kw: Any) -> None:
        raise self._offline("PUT <blob>")

    def get_url(self, url: str) -> bytes:
        raise self._offline("GET <blob>")

    def download_to(self, url: str, dest: str, **_kw: Any) -> tuple[int, str]:
        raise self._offline("GET <blob>")


class OfflineClient(Client):
    """The client behind an offline run: async writes into the run's own queue,
    no drainer, no worker, no feature probes."""

    #: `probe sync` is this client's drainer, so the "async writes with a custom
    #: transport have no background drainer" notice would be noise. A class
    #: attribute, not a `warnings` filter: those are process-wide and not
    #: thread-safe, and would hide another thread's warnings meanwhile.
    _drains_by_hand = True

    def __init__(self, settings: Settings, journal: Journal):
        # Nothing drains this queue before `probe sync`, so the op ceiling for a
        # stalled drainer would only drop a long run's tail and its close
        # (`Journal.op_ceiling`). The free-space floor still applies.
        journal.op_ceiling = 0
        super().__init__(
            settings=settings,
            transport=OfflineTransport(settings),
            journal=journal,
            async_writes=True,
            auto_drain=False,
        )

    #: Features whose writes an offline run QUEUES instead of asking about: the
    #: server that decides is the one `probe sync` delivers to, and `sync_dir`
    #: checks it there (and says so when it lacks one). Asking now would be a
    #: request; every other feature reads as unsupported offline.
    DEFERRED_FEATURES = frozenset({"run_config_merge", *LINEAGE_ROUTES})

    def supports_feature(self, name: str) -> bool:
        return name in self.DEFERRED_FEATURES


class OfflineRun(Run):
    """A run recorded with no network. Writes journal; ``finish`` queues the
    close behind them and never waits for a server."""

    offline = True

    @property
    def offline_dir(self) -> Path:
        return self._client.journal.dir

    def snapshot(self, *_a: Any, **_kw: Any) -> None:
        return None  # needs the server (execution records); skipped offline

    def start_heartbeat(self, *_a: Any, **_kw: Any) -> None:
        return None  # nothing to beat to

    def refresh(self) -> "OfflineRun":
        """A no-op: there is no server copy to re-read yet. This handle's own
        state (config, tags, status) IS the record until `probe sync`."""
        return self

    def finish(
        self,
        status: str = "completed",
        *,
        summary_metrics: dict | None = None,
        summary: dict | None = None,
        flush_timeout: float | None = None,
        strict: bool | None = None,
    ):
        """Queue the close behind the run's writes, with the client's end time.

        Idempotent like `Run.finish`. Never waits on a server and never raises
        over the queue: a close the disk cannot take is warned about, and the
        server will close the run when its sync grace ends. What the run read
        and wrote is hashed first -- local work, at most `inputs.FINISH_WAIT_S`
        and half of the close's time (``flush_timeout``, a reinit's 10 s, a
        SIGTERM close's grace), as `Run._close_finalize` bounds it -- and
        queued ahead of the close; a Ctrl-C there leaves those lists for a
        later recovery, queues the close `canceled`, and is raised after."""
        previous = getattr(self, "_finish_result", _UNSET)
        if previous is not _UNSET:
            return previous
        summary = summary_metrics if summary is None else summary
        interrupted: KeyboardInterrupt | None = None
        try:
            from . import inputs as _inputs

            if _inputs.is_recording(self.id):
                timeout = self._resolve_finish_timeout(flush_timeout)
                _inputs.finalize(
                    self._client, self.id, wait_s=min(_inputs.FINISH_WAIT_S, 0.5 * timeout)
                )
        except KeyboardInterrupt as exc:
            interrupted, status = exc, "canceled"
        except Exception:  # noqa: BLE001 -- lineage evidence never gates a close
            pass
        try:
            # Uploads queued for a credential scan become ops first (local
            # CPU), so the close lands behind them.
            self._promote_uploads_before_close(strict=False, timeout=60.0)
        except Exception:  # noqa: BLE001 -- a close never raises over a scan
            pass
        # Merged over a `probe_finish` the caller passed (a reinit's `closed_by`).
        given = (summary or {}).get("probe_finish")
        marker: dict[str, Any] = {
            **(given if isinstance(given, dict) else {}),
            "offline": True,
            "session_id": self.session_id,
        }
        # Writes the disk floor (or an unwritable queue) refused while recording
        # never reached the queue, so no sync can deliver them: the record says
        # so, as online (`probe_finish.dropped_writes`, plan 0.1).
        dropped = max(
            0,
            int(getattr(self._client, "dropped_writes", 0) or 0)
            - int(getattr(self, "_dropped_baseline", 0) or 0),
        )
        if dropped:
            marker["dropped_writes"] = dropped
        body: dict[str, Any] = {
            "status": status,
            "ended_at": _now(),
            **_summary_wire({**(summary or {}), "probe_finish": marker}),
        }
        result: dict[str, Any] = {"offline": True, "dir": str(self.offline_dir)}
        try:
            # `admitted`: the close is the ONE op no room check may refuse -- a
            # run that logged to the disk floor still has to end (as online).
            self._client.journal.append_http(
                "PATCH", f"/v1/runs/{self.id}", body, run_ref=self.id, admitted=True
            )
            self._closed_status = status
            result["finish_queued"] = True
            print(
                f"probe: offline run {self.id} closed {status}; it is queued in "
                f"{self.offline_dir} -- deliver it with `probe sync`",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001 -- see the docstring
            result["finish_queued"] = False
            _diagnostics.warn(
                f"probe: offline run {self.id} could not queue its close "
                f"({_diagnostics.describe(exc)}); `probe sync` will deliver its data and "
                "the server closes the run after its sync grace"
            )
        if dropped:
            result["dropped_writes"] = dropped
            _note_in_manifest(self.offline_dir, dropped_writes=dropped)
            _diagnostics.warn(
                f"probe: {dropped} write(s) for offline run {self.id} were dropped before "
                "they reached its queue (the disk was under the outbox's free-space floor, "
                "or the queue was unwritable -- see the earlier warning); the run is marked "
                f"probe_finish.dropped_writes={dropped} and `probe sync` reports it"
            )
        self._release_run_lock()
        self._finish_result = result
        # The close is over: an unbound (`reinit="create_new"`) run lets go of
        # its binding here, as `Run.finish` does.
        self._settled()
        if interrupted is not None:
            raise interrupted
        return result


# -- recording ----------------------------------------------------------------
def cached_identity(settings: Settings) -> dict[str, str | None]:
    """The tenant and user this machine last saw for its credential, read from
    the telemetry identity cache WITHOUT a request (and whatever its age).
    ``{"customer_id": None, "user_id": None}`` when never cached."""
    unknown: dict[str, str | None] = {"customer_id": None, "user_id": None}
    token = settings.token or ""
    if not token:
        return unknown
    try:
        from ._telemetry_core import _state_home

        home = _state_home()
        if not home:
            return unknown
        key = hashlib.sha256(f"{settings.base_url}|{token}".encode()).hexdigest()[:16]
        cached = json.loads((Path(home) / "identity.json").read_text())
        if cached.get("key") != key:
            return unknown
        return {"customer_id": cached.get("customer_id"), "user_id": cached.get("user_id")}
    except Exception:  # noqa: BLE001 -- identity is best-effort evidence
        return unknown


def open_offline_run(
    kw: dict,
    *,
    sent: dict | None = None,
    fallback: bool = False,
    settings: Settings | None = None,
    base: str | os.PathLike | None = None,
) -> OfflineRun:
    """Mint an offline run from ``probe.init()``'s keywords. No network.

    ``fallback``: this is ``PROBE_INIT_FALLBACK=offline`` taking over an online
    init, not a run the caller asked to record offline. ``sent`` (the fallback
    too) is the last create that init SENT and got no run back for,
    ``{"path", "body"}``: the offline create reuses its key, its resolved home
    and its body (plus the offline marks), and the request itself is kept for
    `deliver_create` to replay verbatim if its key turns out to have landed."""
    kw = dict(kw)
    on_conflict = kw.pop("on_conflict", None)
    if on_conflict is not None and on_conflict not in _OFFLINE_CONFLICT:
        raise errors.ValidationError(
            f"on_conflict={on_conflict!r} cannot be honoured offline: resuming a run "
            "needs the server. Use on_conflict='error' (the default offline) or "
            "'supersede' (a colliding external_id opens as <id>-rN at sync)."
        )
    sent_body = (sent or {}).get("body") or {}
    external_id = kw.get("external_id") or sent_body.get("external_id")
    if fallback and on_conflict is None and external_id is not None:
        # Online, the default ("auto") RESUMES a crashed run of this external_id
        # -- a SLURM requeue's whole point. Offline nothing can be resumed
        # (plan 2.12: offline runs take `error` or `supersede` only), and
        # silently turning the default into `error` stranded the run behind a
        # 409 at sync. The caller chooses, or init raises as it would have.
        raise errors.ValidationError(
            f"external_id={external_id!r} with the default on_conflict ('auto') would "
            "resume a crashed run of that id online, which only the server can decide. "
            "Pass on_conflict='supersede' (a colliding id opens as <id>-rN at sync) or "
            "'error' to let the fallback record it offline"
        )

    settings = settings or resolve_settings()
    identity = cached_identity(settings)
    started_at = now_iso()
    # Who recorded it. "unknown" when this machine never reached the API under
    # its credential (nothing cached): said so again at sync.
    owner = identity.get("user_id") or UNKNOWN_OWNER
    if sent is not None:
        # The create was already built and SENT: its arguments were checked and
        # its home resolved online. Nothing else in `kw` is re-validated (an
        # online-only argument must not turn the fallback into a failure).
        home = {k: kw.get(k) for k in _HOME_FIELDS}
        skipped: list[str] = []
        key = str(sent_body["creation_key"])
        body = _offline_body(sent_body, started_at=started_at, owner=owner)
        create: dict[str, Any] = {
            "creation_key": key,
            "body": body,
            "path": sent["path"],
            "on_conflict": on_conflict or "error",
            # Replayed ONLY if the server says this key already made a run.
            "request": {"path": sent["path"], "body": sent_body},
        }
    else:
        intent = kw.pop("intent", None)
        skipped = sorted(k for k in _SKIPPED_FIELDS if kw.pop(k, None) is not None)
        home = {k: kw.pop(k, None) for k in _HOME_FIELDS}
        create_kw = {k: kw.pop(k) for k in _CREATE_FIELDS if k in kw}
        if kw:
            raise errors.ValidationError(
                f"probe.init(mode='offline') does not take {', '.join(sorted(kw))}"
            )
        if home["question"] is not None and not (home["experiment"] and home["project"]):
            raise errors.ValidationError(
                "question= creates an experiment, so it needs experiment= and project="
            )
        if home["experiment_name"] is not None and home["question"] is None:
            raise errors.ValidationError("experiment_name only titles an experiment question= creates")
        if create_kw.get("group_id") is not None and not home["experiment"]:
            raise errors.ValidationError("a group needs an experiment: name the experiment or drop the group")
        key = uuid.uuid4().hex
        metadata = dict(create_kw.pop("metadata", None) or {})
        if intent is not None:
            metadata["intent"] = str(intent).strip()
        name = create_kw.pop("name", None)
        body = Client._run_create_body(
            name,
            description=create_kw.pop("description", None),
            notes=create_kw.pop("notes", None),
            source=create_kw.pop("source", None) or "api",
            external_id=create_kw.pop("external_id", None),
            parent_run_id=create_kw.pop("parent_run_id", None),
            parent_relation=create_kw.pop("parent_relation", None),
            parent_provenance=create_kw.pop("parent_provenance", None),
            group_id=create_kw.pop("group_id", None),
            config=create_kw.pop("config", None),
            tags=create_kw.pop("tags", None),
            metadata=metadata,
            labeled_point_budget=create_kw.pop("labeled_point_budget", None),
            slug=create_kw.pop("slug", None),
            heartbeat=False,
            authored_by=create_kw.pop("authored_by", None),
        )
        body["creation_key"] = key
        body = _offline_body(body, started_at=started_at, owner=owner)
        create = {
            "creation_key": key,
            "body": body,
            "on_conflict": on_conflict or "error",
            **{k: v for k, v in home.items() if v is not None},
        }
    ref = local_ref(key)
    directory = offline_root(base) / key
    journal = Journal(
        directory,
        context={"name": _context_name(), "base_url": settings.base_url},
    )

    manifest = {
        "schema": MANIFEST_SCHEMA,
        "creation_key": key,
        "run_ref": ref,
        "recorded_at": started_at,
        "base_url": settings.base_url,
        "context": _context_name(),
        "customer_id": identity.get("customer_id"),
        "user_id": identity.get("user_id"),
        "name": body.get("name"),
        "project": home.get("project"),
        "experiment": home.get("experiment"),
        "fallback": fallback,
    }
    journal._ensure()
    write_text_atomic(directory / MANIFEST_NAME, json.dumps(manifest, indent=2) + "\n", mode=0o600)
    op = journal._base_op(CREATE_KIND, ref)
    op["create"] = create
    journal._append(op, admitted=True)

    client = OfflineClient(settings, journal)
    data = {
        "id": ref,
        "slug": None,
        "name": body.get("name") or f"offline-{key[:8]}",
        "status": "running",
        "config": body.get("config") or {},
        "tags": body.get("tags") or [],
        "metadata": body.get("metadata") or {},
        "project_id": None,
        "experiment_id": None,
        "write_epoch": 1,
        "started_at": started_at,
        "liveness_mode": "offline",
    }
    run = OfflineRun(client, data)
    run._hold_run_lock(process_bound=True)
    from . import _open_runs

    _open_runs.opened(run)  # counted like an online run (F5 binding)
    why = "the API could not be reached (PROBE_INIT_FALLBACK=offline)" if fallback else "PROBE_MODE=offline"
    print(
        f"probe: recording OFFLINE ({why}) -- run {ref} queues in {directory}; "
        "deliver it later with `probe sync`",
        flush=True,
    )
    if skipped or not fallback:
        _diagnostics.warn(
            "probe: an offline run records metrics, spans, artifacts, config updates, what "
            "it reads and writes, and its close; code snapshot, output capture (file "
            "uploads) and hardware metrics are skipped offline"
            + (f" (ignored: {', '.join(skipped)})" if skipped else "")
        )
    return run


def _offline_body(body: dict, *, started_at: str, owner: str) -> dict:
    """``body`` as an OFFLINE create: the offline signal and the real start,
    who recorded it and what was skipped, and none of the live-owner signals
    the server refuses beside ``offline`` (a heartbeat, a launcher, a hand-off).
    A copy: a sent request kept for replay must stay byte-for-byte as sent."""
    out = json.loads(json.dumps(body))
    for signal in ("heartbeat", "launcher", "awaiting_attach", "liveness_mode"):
        out.pop(signal, None)
    metadata = dict(out.get("metadata") or {})
    metadata["offline"] = {"recorded_at": started_at, "skipped": list(SKIPPED_CAPTURE)}
    metadata["offline_owner"] = owner
    out["metadata"] = metadata
    out.update(offline=True, started_at=started_at)
    return out


def _note_in_manifest(directory: Path, **fields: Any) -> None:
    """Best effort: record ``fields`` in the queue's manifest (a full disk may
    refuse; the close already carries the same facts)."""
    try:
        manifest = read_manifest(directory)
        if manifest is None:
            return
        manifest.update(fields)
        write_text_atomic(directory / MANIFEST_NAME, json.dumps(manifest, indent=2) + "\n", mode=0o600)
    except Exception:  # noqa: BLE001 -- evidence, never a failure of the close
        pass


def _context_name() -> str | None:
    try:
        from . import config as config_module

        return config_module.current_context_name() or None
    except Exception:  # noqa: BLE001
        return None


def fallback_enabled() -> bool:
    return os.environ.get(FALLBACK_ENV, "").strip().lower() == "offline"


# -- syncing ------------------------------------------------------------------
def read_manifest(directory: str | os.PathLike) -> dict | None:
    try:
        data = json.loads((Path(directory) / MANIFEST_NAME).read_text())
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("schema") == MANIFEST_SCHEMA else None


def read_mapping(directory: str | os.PathLike) -> dict:
    try:
        data = json.loads((Path(directory) / MAPPING_NAME).read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_mapping(directory: Path, key: str, run_id: str, **extra: Any) -> None:
    """Atomic: a crash leaves the old mapping or the new one, never half."""
    mapping = read_mapping(directory)
    mapping[key] = {"id": str(run_id), "synced_at": now_iso(), **extra}
    write_text_atomic(directory / MAPPING_NAME, json.dumps(mapping, indent=2) + "\n", mode=0o600)


def search_places(root: str | os.PathLike | None = None) -> list[Path]:
    """Where :func:`find_offline_dirs` looks under ``root``, for messages."""
    base = Path(root).expanduser() if root is not None else default_root()
    return [base / OFFLINE_DIRNAME, base / "rank-*" / OFFLINE_DIRNAME, base]


def find_offline_dirs(root: str | os.PathLike | None = None) -> list[Path]:
    """Offline run directories under ``root``: one run's dir, a folder of them,
    or an outbox -- its ``offline/`` and every rank's ``rank-*/offline/`` (a
    torchrun/SLURM rank's own outbox, or a queue recorded by an SDK that put
    offline runs there). Default: this machine's outbox root."""
    base = Path(root).expanduser() if root is not None else default_root()
    if read_manifest(base) is not None:
        return [base]
    parents = [base / OFFLINE_DIRNAME, *sorted(base.glob(f"rank-*/{OFFLINE_DIRNAME}")), base]
    found: list[Path] = []
    for parent in parents:
        if not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            if child.is_dir() and child not in found and read_manifest(child) is not None:
                found.append(child)
    return found


def describe(directory: Path) -> dict:
    """One offline run's state, for `probe sync --list` (no network)."""
    manifest = read_manifest(directory) or {}
    journal = Journal(directory)
    pending = len(journal.pending()) + len(journal.waiting())
    failed = len(journal.failed())
    mapped = read_mapping(directory).get(str(manifest.get("creation_key")))
    state = "synced" if mapped and not pending and not failed else "unsynced"
    if mapped and (pending or failed):
        state = "partial"
    return {
        "key": manifest.get("creation_key"),
        "dir": str(directory),
        "state": state,
        "run_id": (mapped or {}).get("id"),
        "name": manifest.get("name"),
        "project": manifest.get("project"),
        "experiment": manifest.get("experiment"),
        "recorded_at": manifest.get("recorded_at"),
        "customer_id": manifest.get("customer_id"),
        "pending": pending,
        "failed": failed,
        # Writes refused while recording (disk floor): not in the queue, so no
        # sync delivers them (`OfflineRun.finish`).
        "dropped_writes": int(manifest.get("dropped_writes") or 0),
    }


def _create_ops(journal: Journal) -> list[tuple[Path, dict]]:
    return [
        (p, op)
        for p, op in [*journal.pending(), *journal.failed()]
        if op.get("kind") == CREATE_KIND
    ]


def amend(
    directory: Path,
    *,
    project: str | None = None,
    experiment: str | None = None,
    on_conflict: str | None = None,
    only_refused: bool = False,
) -> int:
    """`probe sync --project/--experiment/--on-conflict`: change how a still
    undelivered create is filed -- somewhere that exists, or as a retry
    (``supersede``) of the run that already holds its ``external_id`` -- and put
    a refused one back in the queue. ``only_refused``: leave a create that has
    not been refused alone (the flags then fix what failed, not every run a
    folder scan found). Returns how many create ops changed.

    A create the fallback kept a SENT request for is re-filed too: the offline
    create goes to the new home, and the kept request is still replayed as sent
    (to its original home) if the server says its key already made a run."""
    if on_conflict is not None and on_conflict not in _OFFLINE_CONFLICT:
        raise errors.ValidationError(
            f"--on-conflict {on_conflict!r}: an offline run can only be delivered with "
            f"{' or '.join(_OFFLINE_CONFLICT)}"
        )
    journal = Journal(directory)
    changed = 0
    for path, op in _create_ops(journal):
        refused = path.parent == journal.failed_dir
        if only_refused and not refused:
            continue
        create = op.get("create") or {}
        if project is not None:
            create.pop("path", None)  # re-resolved from the slugs at sync
            create["project"] = project
            if experiment is None:
                create.pop("experiment", None)
                create.pop("question", None)
                create.pop("experiment_name", None)
                (create.get("body") or {}).pop("group_id", None)
        if experiment is not None:
            create.pop("path", None)
            create["experiment"] = experiment
        if on_conflict is not None:
            create["on_conflict"] = on_conflict
        op["create"] = create
        op["attempts"] = 0
        op["last_error"] = None
        write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
        if refused:
            journal.retry_failed(op.get("op_id"))
        changed += 1
    return changed


def _origin(url: str | None) -> str:
    return (url or "").strip().rstrip("/").lower()


def check_origin(directory: Path, client: Client, *, allow_mismatch: bool = False) -> list[str]:
    """Refuse a queue recorded against another server, or -- when its tenant is
    unknown -- under another login context, unless ``allow_mismatch``. Returns
    warnings (a mismatch allowed, or a context change the tenant check covers)."""
    manifest = read_manifest(directory) or {}
    warnings_: list[str] = []
    recorded_url, current_url = manifest.get("base_url"), getattr(client.settings, "base_url", None)
    if recorded_url and current_url and _origin(recorded_url) != _origin(current_url):
        message = (
            f"recorded against {recorded_url}, but this login syncs to {current_url}"
        )
        if not allow_mismatch:
            raise errors.ScopeError(
                f"{directory}: {message}. Log in to that server, or pass --allow-mismatch "
                "to deliver it here anyway."
            )
        warnings_.append(message + " (--allow-mismatch)")
    recorded_ctx, current_ctx = manifest.get("context"), _context_name()
    if recorded_ctx and current_ctx and recorded_ctx != current_ctx:
        message = f"recorded under login context {recorded_ctx!r}, synced under {current_ctx!r}"
        if manifest.get("customer_id"):
            warnings_.append(message + " (same team: checked against the recorded one)")
        elif not allow_mismatch:
            # With no recorded team, the context is the only evidence of whose
            # run this is: another context may well be another team's login.
            raise errors.ScopeError(
                f"{directory}: {message}, and the team it was recorded for is unknown. "
                f"Switch back to context {recorded_ctx!r} (`probe wizard --action account`), or pass "
                "--allow-mismatch to deliver it with this login."
            )
        else:
            warnings_.append(message + " (--allow-mismatch)")
    return warnings_


def check_tenant(directory: Path, client: Client) -> dict:
    """Refuse a queue recorded for another tenant. Returns the syncer's identity."""
    manifest = read_manifest(directory) or {}
    me = client.me() or {}
    recorded = manifest.get("customer_id")
    current = me.get("customer_id")
    if recorded and current and recorded != current:
        raise errors.ScopeError(
            f"{directory}: this run was recorded for team {recorded!r}, but you are "
            f"logged in to {current!r}. Sign in to that team (`probe wizard --action login "
            "--context <name>`) to sync it."
        )
    return me


def require_server(client: Client) -> None:
    if not client.supports_feature("run_offline_create"):
        raise errors.CapabilityUnavailable(
            "run_offline_create",
            "this research-os server predates offline sync: it would treat the run as "
            "abandoned and close it mid-sync. Upgrade the server, then `probe sync` again; "
            "the queue is kept.",
        )


# -- the drain's half (called from journal._execute) ----------------------------
def bind_local_refs(journal: Journal, op: dict) -> None:
    """Rewrite ``local:<key>`` to the run's server id in the op's path, body and
    upload anchor. ``run_ref`` keeps the key: it is the run's lane identity."""
    ref = str(op.get("run_ref") or "")
    key = ref[len(LOCAL_PREFIX) :]
    entry = read_mapping(journal.dir).get(key)
    if not entry or not entry.get("id"):
        raise errors.OfflineRunNotCreated(
            f"offline run {ref} is not on the server yet: its create has not been "
            "delivered (still queued, or refused: its own error says why and names the "
            "fix). `probe sync --list` shows it."
        )
    run_id = str(entry["id"])
    if isinstance(op.get("path"), str):
        op["path"] = op["path"].replace(ref, run_id)
    if op.get("body") is not None:
        op["body"] = _replace(op["body"], ref, run_id)
    upload = op.get("upload")
    if isinstance(upload, dict) and upload.get("anchor_id") == ref:
        upload["anchor_id"] = run_id


def _replace(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new) if old in value else value
    if isinstance(value, list):
        return [_replace(v, old, new) for v in value]
    if isinstance(value, dict):
        return {k: _replace(v, old, new) for k, v in value.items()}
    return value


def deliver_create(journal: Journal, client: Client, op: dict) -> dict:
    """Deliver an offline run's create and record ``key -> id`` before the op
    is dequeued. Idempotent by the creation key: a crash between the create and
    the mapping replays the create and gets the same run back.

    The OFFLINE create always goes first. A create the init fallback kept a
    sent request for (``create["request"]``) replays that request verbatim only
    when the server answers that the key already made a run (422
    ``creation_key_reused``): the online create landed and its answer was lost,
    so that run is this one. Never on a guess from the client side."""
    create = op.get("create") or {}
    key = str(create.get("creation_key") or "")
    if not key:
        raise errors.ValidationError(f"offline create op {op.get('op_id')} has no creation_key", status=422)
    known = read_mapping(journal.dir).get(key)
    if known and known.get("id"):
        return {"id": known["id"]}
    kept = create.get("request")
    via = "offline"
    try:
        path = create.get("path") or _home_path(client, create, key)
        try:
            row = _create_with_policy(client, path, create)
        except errors.RosError as gone:
            # The fallback's create carries the home init resolved (a project
            # or experiment id); deleted or trashed since, the POST is a 404 /
            # 410. Name the fix instead of dead-lettering a bare "not found".
            if not (isinstance(gone, errors.NotFoundError) or gone.status == 410):
                raise
            raise errors.ValidationError(
                f"offline run {local_ref(key)} was recorded for a project or experiment "
                f"that is gone from this server ({gone}). File it somewhere that exists: "
                "`probe sync <its folder> --project <slug>` (and `--experiment <slug>`).",
                status=422,
            ) from gone
    except errors.ValidationError as exc:
        if kept is None or not _key_made_a_run(exc):
            raise
        try:
            row = _post(client, kept["path"], kept["body"])
        except errors.ValidationError as again:
            if not _key_made_a_run(again):
                raise
            raise errors.ValidationError(
                f"offline run {local_ref(key)}: the create init sent online before the "
                "outage made a run under this key, but this login cannot replay it (only "
                "the user who sent it can). Sync this folder logged in as that user.",
                status=422,
            ) from again
        via = "online"
    _write_mapping(journal.dir, key, row["id"], via=via)
    return row


def _lineage_feature(op: dict) -> str | None:
    """The feature a queued op needs when it is a run's read or write list
    (``POST /v1/runs/<ref>/inputs`` / ``.../outputs``), else None."""
    target = op.get("path")
    if op.get("method") != "POST" or not isinstance(target, str) or not target.startswith("/v1/runs/"):
        return None
    if target.count("/") != 4:
        return None
    route = target.rsplit("/", 1)[1]
    return next((feature for feature, name in LINEAGE_ROUTES.items() if name == route), None)


#: Lists `lineage_gate` dropped at delivery, by queue folder, for `sync_dir`.
_GATED: dict[str, dict[str, int]] = {}


def _take_gated(directory: Path) -> dict[str, int]:
    return _GATED.pop(os.path.realpath(directory), {})


def lineage_gate(journal: Journal, client: Client, op: dict) -> bool:
    """At DELIVERY (`journal._execute`, for an offline run's op): whether this
    op is a read or write list the server does not take, and so must be
    dropped rather than sent. `sync_dir` filters the queue before its drain,
    but a recovery can append a list after that check; asking here, per op,
    closes the gap. An unreachable server is not a no: the op is sent and
    fails as any other would."""
    feature = _lineage_feature(op)
    if feature is None:
        return False
    try:
        if not client.supports_feature(feature):
            counts = _GATED.setdefault(os.path.realpath(journal.dir), {})
            counts[feature] = counts.get(feature, 0) + 1
            return True
        if feature == "run_inputs" and not client.supports_feature(_OBSERVATIONS_FEATURE):
            return _unobserved(journal, op)
    except errors.RosError:
        return False
    return False


#: The server keys a read on its observation id (0290), declared with
#: `run_outputs` (`inputs.OBSERVATIONS_FEATURE`).
_OBSERVATIONS_FEATURE = "run_outputs"
#: `_GATED`'s key for late hashes dropped at delivery.
_LATE = "late_hashes"


def _unobserved(journal: Journal, op: dict) -> bool:
    """A read list queued offline for a server that does not key reads on
    their observation id (0290): its rows go without the id, and a LATE
    re-send (tagged ``inputs.LATE_TAG`` in the queue, F7) is dropped: such a
    server would keep its hashed rows beside the unhashed ones instead of
    replacing them. True when the op is dropped."""
    from .inputs import LATE_TAG

    body = op.get("body")
    if not isinstance(body, dict):
        return False
    if op.get("tag") == LATE_TAG:
        counts = _GATED.setdefault(os.path.realpath(journal.dir), {})
        counts[_LATE] = counts.get(_LATE, 0) + 1
        return True
    rows = body.get("inputs")
    if isinstance(rows, list):
        body["inputs"] = [
            {k: v for k, v in row.items() if k != "observation_id"} if isinstance(row, dict) else row
            for row in rows
        ]
    return False


def _drop_untaken_lineage(journal: Journal, client: Client) -> dict[str, int]:
    """Remove the queued read and write lists (``POST /v1/runs/<ref>/inputs``,
    ``.../outputs``) the SYNC server does not declare it takes: queued offline
    on the promise that this server decides (`OfflineClient.DEFERRED_FEATURES`),
    and against one without the route each would dead-letter, leaving the sync
    unclean over lineage evidence. Returns {feature: lists dropped}."""
    dropped: dict[str, int] = {}
    for feature in LINEAGE_ROUTES:
        try:
            if client.supports_feature(feature):
                continue
        except errors.RosError:
            continue  # unreachable: the drain will say so
        for path, op in journal.pending():
            if _lineage_feature(op) == feature:
                try:
                    path.unlink()
                except OSError:
                    continue
                dropped[feature] = dropped.get(feature, 0) + 1
    return dropped


def _key_made_a_run(exc: errors.RosError) -> bool:
    detail = exc.detail if isinstance(exc.detail, dict) else {}
    return exc.status == 422 and detail.get("code") == "creation_key_reused"


def _post(client: Client, path: str, body: dict) -> dict:
    # The server declares run_creation_key (checked before a sync starts), so
    # a create whose answer is lost is safe to re-send: retried like a read.
    return client.transport.request("POST", path, json_body=body, idempotent=True).json()


def _home_path(client: Client, create: dict, key: str) -> str:
    project, experiment = create.get("project"), create.get("experiment")
    question = create.get("question")
    try:
        project_id = None
        if project:
            project_id = (
                client.ensure_project(project)["id"]
                if question is not None
                else client.resolve_or_raise("project", project)["id"]
            )
        if experiment:
            if question is not None:
                exp = client.ensure_experiment(
                    experiment, create.get("experiment_name"), question=question, project_id=project_id
                )
            else:
                exp = client.resolve_or_raise("experiment", experiment, project_id=project_id)
            return f"/v1/projects/{exp['id']}/runs"
        if project_id:
            return f"/v1/projects/{project_id}/runs"
        return "/v1/runs"
    except errors.NotFoundError as exc:
        where = f"project {project!r}" + (f", experiment {experiment!r}" if experiment else "")
        raise errors.ValidationError(
            f"offline run {local_ref(key)} was recorded for {where}, which does not exist "
            f"on this server ({exc}). File it somewhere that does: "
            "`probe sync --project <slug>` (and `--experiment <slug>`).",
            status=422,
        ) from exc


def _create_with_policy(client: Client, path: str, create: dict) -> dict:
    body = create["body"]
    ref = local_ref(str(create.get("creation_key")))
    try:
        return _post(client, path, body)
    except errors.ConflictError as conflict:
        base = body.get("external_id")
        if create.get("on_conflict") == "supersede" and base is not None:
            incumbent = conflict.existing_id
        else:
            # Re-raised WITHOUT `existing_id`: the drain reads a 409 naming one on
            # a retried op as that op's own earlier delivery and would drop this
            # create with no mapping, stranding every write behind it.
            raise errors.ConflictError(_conflict_message(client, ref, base, conflict)) from conflict
    # SUPERSEDE: a fresh run as <external_id>-rN with retry lineage, each slot
    # under a key DERIVED from the run's own, so a re-sync replays the same one.
    for n in range(2, 7):
        retry = dict(
            body,
            external_id=f"{base}-r{n}",
            creation_key=hashlib.sha256(f"{create['creation_key']}:r{n}".encode()).hexdigest()[:32],
        )
        if incumbent:
            retry.update(
                parent_run_id=str(incumbent), parent_relation="retry", parent_provenance="observed_call"
            )
        try:
            row = _post(client, path, retry)
        except errors.ConflictError:
            continue
        _mark_supersede(client, row, incumbent, n)
        return row
    raise errors.ConflictError(f"{ref}: no free retry slot for {base!r} after 5 attempts")


def _conflict_message(client: Client, ref: str, base: str | None, conflict: errors.ConflictError) -> str:
    if base is None:
        return f"offline run {ref}: {conflict}"
    holder = conflict.existing_id
    status = None
    if holder:
        try:
            status = (client.transport.get(f"/v1/runs/{holder}") or {}).get("status")
        except errors.RosError:
            status = None  # only for the message
    held = f"run {holder}" + (f" ({status})" if status else "") if holder else "another run"
    return (
        f"offline run {ref} was recorded with external_id {base!r}, which {held} already "
        "has on this server. An offline recording cannot resume that run; deliver it as "
        f"a retry of it with `probe sync <its folder> --on-conflict supersede` (it opens as "
        f"{base}-r2, linked to it)."
    )


def _mark_supersede(client: Client, row: dict, incumbent: str | None, attempt: int) -> None:
    """What an online supersede records (`Client._create_run_with_policy`): the
    new run's ``retry_of`` / ``retry_attempt`` foreign keys, and a dead
    incumbent tagged ``superseded``. Both idempotent (a per-key merge, a set),
    so a re-sync that replays the slot repeats them harmlessly. Best effort:
    the run and its data matter more than its lineage tags."""
    if not incumbent:
        return
    try:
        client.transport.request(
            "PATCH",
            f"/v1/runs/{row['id']}",
            json_body={"foreign_keys": {"retry_of": str(incumbent), "retry_attempt": attempt}},
            idempotent=True,
        )
        old = client.transport.get(f"/v1/runs/{incumbent}") or {}
        if old.get("status") in Client._DEAD_RUN_STATUSES:
            tags = sorted({*(old.get("tags") or []), "superseded"})
            client.transport.request(
                "PATCH", f"/v1/runs/{incumbent}", json_body={"tags": tags}, idempotent=True
            )
    except errors.RosError as exc:
        _diagnostics.warn(
            f"probe sync: run {row.get('id')} superseded {incumbent}, but its retry lineage "
            f"(retry_of, the incumbent's `superseded` tag) was not recorded: {exc}"
        )


def sync_dir(
    directory: Path,
    client: Client,
    *,
    project: str | None = None,
    experiment: str | None = None,
    on_conflict: str | None = None,
    amend_all: bool = False,
    allow_mismatch: bool = False,
) -> dict:
    """Deliver one offline run with ``client`` (the syncer's login).

    ``project`` / ``experiment`` / ``on_conflict`` re-file the run's create
    (:func:`amend`) -- only a REFUSED one unless ``amend_all`` (the caller named
    this run's folder)."""
    from .journal import drain

    manifest = read_manifest(directory) or {}
    warnings_ = check_origin(directory, client, allow_mismatch=allow_mismatch)
    me = check_tenant(directory, client)
    if not manifest.get("customer_id"):
        # Nothing to check against: the recording machine never reached the API
        # under its credential. Allowed (any writer may sync), never silent.
        warnings_.append(
            "recorded on a machine that had never reached the API, so the team it was "
            "recorded for is unknown; syncing it into this login's team "
            f"({me.get('customer_id') or 'unknown'})"
        )
    amended = 0
    if project is not None or experiment is not None or on_conflict is not None:
        amended = amend(
            directory,
            project=project,
            experiment=experiment,
            on_conflict=on_conflict,
            only_refused=not amend_all,
        )
    journal = Journal(directory)
    unmergeable = 0
    if not client.supports_feature("run_config_merge"):
        # Config merges were queued offline on the promise that the syncing
        # server decides (`OfflineClient.DEFERRED_FEATURES`). This one cannot
        # store them, and would answer 200 while dropping the field.
        unmergeable = sum(
            1 for _, op in journal.pending() if "config_merge" in (op.get("body") or {})
        )
        if unmergeable:
            warnings_.append(
                f"this server cannot merge a run's config after it started (feature "
                f"run_config_merge): {unmergeable} config update(s) recorded offline are "
                "not stored; the run keeps the config it was created with. Upgrade the "
                "server to keep them."
            )
    # The run's own read/write lists its process never queued (it died before
    # its close): into the queue first, so the checks below and the drain
    # see them.
    if manifest.get("creation_key"):
        from . import inputs as _inputs

        _inputs.recover_offline(local_ref(str(manifest["creation_key"])), directory)
    dropped_lineage = _drop_untaken_lineage(journal, client)
    started = time.monotonic()
    report = drain(journal, client_factory=lambda _context: client)
    # A list queued after that check (a recovery elsewhere) was dropped at
    # delivery instead (`lineage_gate`): counted with the rest.
    for feature, count in _take_gated(directory).items():
        dropped_lineage[feature] = dropped_lineage.get(feature, 0) + count
    late = dropped_lineage.pop(_LATE, 0)
    if late:
        warnings_.append(
            f"this server does not key a run's reads by observation (feature "
            f"{_OBSERVATIONS_FEATURE}): {late} late hash list(s) recorded offline were not "
            "re-sent; those reads stay unhashed. Upgrade the server to keep them."
        )
    for feature, count in dropped_lineage.items():
        warnings_.append(
            f"this server does not take a run's {LINEAGE_ROUTES[feature]} list (feature "
            f"{feature}): {count} list(s) recorded offline were dropped instead of "
            "delivered; the run's other data is unaffected. Upgrade the server to keep them."
        )
    state = describe(directory)
    entry = read_mapping(directory).get(str(manifest.get("creation_key"))) or {}
    if entry.get("via") == "online" and report.delivered:
        warnings_.append(
            f"its create had reached the server online before the outage (run "
            f"{entry.get('id')}), so it was delivered onto that run. Having heard nothing "
            "since init, the server may have marked it crashed and queued a crash notice "
            "meanwhile; its queued close sets the final status now"
        )
    dropped = state["dropped_writes"]
    if dropped:
        warnings_.append(
            f"{dropped} write(s) were dropped while recording (the disk was under the "
            "outbox's free-space floor, or the queue was unwritable) and were never in "
            f"this queue; the run is marked probe_finish.dropped_writes={dropped}"
        )
    return {
        **state,
        "delivered": report.delivered,
        "dead_lettered": report.dead_lettered,
        "remaining": report.remaining,
        "auth_blocked": report.auth_blocked,
        "amended": amended,
        "errors": list(report.errors),
        "warnings": warnings_,
        "seconds": round(time.monotonic() - started, 3),
        "clean": report.clean and state["state"] == "synced" and not dropped and not unmergeable,
    }
