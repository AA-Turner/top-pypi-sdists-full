"""``PROBE_MODE=offline`` and ``probe sync`` (plan 2.12): an offline run queues its create and every
write as ``local:<key>`` with no network; `probe sync` delivers them later (DESIGN.md)."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any

from ... import errors
from ....foundation.safe_warn import safe_warn as _diagnostics
from ...client.client import Client
from ...settings.settings import Settings
from ...settings.settings import resolve as resolve_settings
from ....foundation.durable.durable import now_iso, write_text_atomic
from ..journal.journal import Journal
from ..journal.paths import default_root
from ...run.run import Run
from ...run.metrics.values import _now
from ...run.summary import _summary_wire
from ...run.handle import _UNSET
from probe.sdk.routes import WriteOp, path_for
MANIFEST_NAME = "offline.json"
MANIFEST_SCHEMA = "probe.offline/1"
LOCAL_PREFIX = "local:"
#: The journal op kind that opens an offline run. Only offline queues carry it and only
#: `probe sync` drains them, so no older worker meets it.
CREATE_KIND = "create_run"
FALLBACK_ENV = "PROBE_INIT_FALLBACK"
#: `metadata.offline_owner` when the recording machine had no cached identity.
UNKNOWN_OWNER = "unknown"
#: What an offline run cannot do yet (see DESIGN.md). "outputs" is output capture's file
#: uploads; the run's reads and writes ARE recorded.
SKIPPED_CAPTURE = ("code_snapshot", "outputs", "hardware")

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
_HOME_FIELDS = ("project", "experiment", "question", "experiment_name", "workspace")
#: Keywords whose feature an offline run skips (warned once, never an error).
#: `capture_reads`, `capture_outputs` and `ignore` shape its read and write
#: recording; `probe.init` takes them before this sees `kw`.
_SKIPPED_FIELDS = ("hw", "snapshot", "outputs")


def offline_root(base: str | os.PathLike | None = None) -> Path:
    """Where this machine's offline runs queue: ``<outbox>/offline``. At the outbox ROOT,
    never under a torchrun/SLURM rank's ``rank-N/`` (`journal.default_root`): `probe sync`
    usually runs where no RANK is set and each run has its own directory."""
    return (Path(base).expanduser() if base is not None else default_root()) / OFFLINE_DIRNAME


def local_ref(key: str) -> str:
    return f"{LOCAL_PREFIX}{key}"


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
        """Queue the close behind the run's writes, with the client's end time. Idempotent
        like `Run.finish`. Never waits on a server, never raises over the queue: a close the
        disk cannot take is warned about and the server closes the run when its sync grace
        ends. What the run read and wrote is hashed first (local work, at most
        `inputs.FINISH_WAIT_S` and half the close's time -- ``flush_timeout``, a reinit's
        10 s, a SIGTERM close's grace -- as `Run._close_finalize` bounds it) and queued
        ahead of the close; a Ctrl-C there leaves those lists for a later recovery, queues
        the close `canceled`, and is raised after."""
        previous = getattr(self, "_finish_result", _UNSET)
        if previous is not _UNSET:
            return previous
        summary = summary_metrics if summary is None else summary
        interrupted: KeyboardInterrupt | None = None
        try:
            from ...capture import lineage as _inputs

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
            # Uploads queued for a credential scan become ops first (local CPU), so the
            # close lands behind them.
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
        # Writes the disk floor (or an unwritable queue) refused while recording never
        # reached the queue, so no sync can deliver them: the record says so, as online
        # (`probe_finish.dropped_writes`, plan 0.1).
        dropped = max(
            0,
            int(getattr(self._client, "dropped_writes", 0) or 0)
            - int(getattr(self, "_dropped_baseline", 0) or 0),
        )
        if dropped:
            marker["dropped_writes"] = dropped
        earlier = getattr(self, "_closed_status", None)
        if earlier is not None:
            # A launcher already queued the run's verdict (`execute()`'s close): the exit hook's
            # default `completed` must not replace it. Queued again with the end time and marker.
            status = earlier
        body: dict[str, Any] = {
            "status": status,
            "ended_at": _now(),
            **_summary_wire({**(summary or {}), "probe_finish": marker}),
        }
        result: dict[str, Any] = {"offline": True, "dir": str(self.offline_dir)}
        try:
            # `admitted`: the close is the ONE op no room check may refuse; a run that logged
            # to the disk floor still has to end (as online).
            self._client.journal.append_http(
                "PATCH", path_for(WriteOp.RUN_PATCH, self.id), body, run_ref=self.id, admitted=True
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
    """The tenant and user this machine last saw for its credential, read from the telemetry
    identity cache WITHOUT a request (any age). ``{"customer_id": None, "user_id": None}``
    when never cached."""
    unknown: dict[str, str | None] = {"customer_id": None, "user_id": None}
    token = settings.token or ""
    if not token:
        return unknown
    try:
        from ....analytics.core import _state_home

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

    ``fallback``: ``PROBE_INIT_FALLBACK=offline`` taking over an online init, not a run the
    caller asked to record offline. ``sent`` (fallback too) is the last create that init
    SENT and got no run back for, ``{"path", "body"}``: the offline create reuses its key,
    resolved home and body (plus the offline marks); the request is kept for
    `deliver_create` to replay verbatim if its key turns out to have landed."""
    kw = dict(kw)
    on_conflict, sent_body = _check_offline_conflict(kw, sent, fallback)
    settings = settings or resolve_settings()
    identity = cached_identity(settings)
    started_at = now_iso()
    # Who recorded it. "unknown" when this machine never reached the API under its
    # credential (nothing cached): said so again at sync.
    owner = identity.get("user_id") or UNKNOWN_OWNER
    if sent is not None:
        key, body, create, home, skipped = _create_from_sent(kw, sent, sent_body, on_conflict, started_at, owner)
    else:
        key, body, create, home, skipped = _create_from_init(kw, on_conflict, started_at, owner, settings.project)
    ref = local_ref(key)
    directory = offline_root(base) / key
    journal = _start_offline_queue(directory, settings, identity, key, ref, started_at, body, home, fallback)
    op = journal._base_op(CREATE_KIND, ref)
    op["create"] = create
    journal._append(op, admitted=True)
    run = _open_offline_handle(settings, journal, ref, key, body, started_at)
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


def _check_offline_conflict(kw: dict, sent: dict | None, fallback: bool) -> tuple[str | None, dict]:
    """Pop ``on_conflict`` from ``kw`` and refuse one an offline run cannot honour; returns it with
    the sent create's body ({} when nothing was sent)."""
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
        # Online, the default ("auto") RESUMES a crashed run of this external_id (a SLURM
        # requeue's point). Offline nothing can resume (plan 2.12: `error` or `supersede`
        # only), and silently turning the default into `error` stranded the run behind a 409
        # at sync. The caller chooses, or init raises as it would have.
        raise errors.ValidationError(
            f"external_id={external_id!r} with the default on_conflict ('auto') would "
            "resume a crashed run of that id online, which only the server can decide. "
            "Pass on_conflict='supersede' (a colliding id opens as <id>-rN at sync) or "
            "'error' to let the fallback record it offline"
        )
    return on_conflict, sent_body


def _create_from_sent(
    kw: dict, sent: dict, sent_body: dict, on_conflict: str | None, started_at: str, owner: str
) -> tuple[str, dict, dict, dict, list[str]]:
    """The create an online init already SENT: arguments checked, home resolved online. Nothing
    else in `kw` is re-validated (an online-only argument must not turn the fallback into a
    failure)."""
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
    return key, body, create, home, skipped


def _create_from_init(
    kw: dict, on_conflict: str | None, started_at: str, owner: str, ambient_project: str | None
) -> tuple[str, dict, dict, dict, list[str]]:
    """The create built from ``probe.init()``'s keywords, refusing ones an offline run cannot take.
    With no project or experiment named it takes this computer's (as online), else refuses."""
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
    if not home["experiment"] and not home["project"]:
        home["project"] = ambient_project
    if not home["experiment"] and not home["project"]:
        raise errors.ProjectRequired()
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
    return key, body, create, home, skipped


def _start_offline_queue(
    directory: Path, settings: Settings, identity: dict, key: str, ref: str, started_at: str,
    body: dict, home: dict, fallback: bool,
) -> Journal:
    """The offline run's own queue, with its manifest (`offline.json`) written first."""
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
    return journal


def _open_offline_handle(
    settings: Settings, journal: Journal, ref: str, key: str, body: dict, started_at: str
) -> OfflineRun:
    """The OfflineRun the caller writes through, holding the run lock and counted as open."""
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
    from ...run.launch import open_runs as _open_runs

    _open_runs.opened(run)  # counted like an online run (F5 binding)
    return run


def _offline_body(body: dict, *, started_at: str, owner: str) -> dict:
    """``body`` as an OFFLINE create: the offline signal and real start, who recorded it and
    what was skipped, without the live-owner signals the server refuses beside ``offline``
    (heartbeat, launcher, hand-off). A copy: a kept sent request must stay byte-for-byte."""
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
        from ...settings import settings as config_module

        return config_module.current_context_name() or None
    except Exception:  # noqa: BLE001
        return None


def fallback_enabled() -> bool:
    return os.environ.get(FALLBACK_ENV, "").strip().lower() == "offline"
from probe.sdk.delivery.offline.queue import OFFLINE_DIRNAME, _OFFLINE_CONFLICT, read_manifest  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.offline.client import OfflineClient  # noqa: E402 -- pieces need each other; the front door loads this one first
