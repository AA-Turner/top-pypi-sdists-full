"""The SDK Run handle: the agent's per-run write surface.

Wraps a run row and exposes the write verbs from the SDK/CLI sketch, each mapped
to a v3 endpoint:

  log()/log_hw() -> POST /v1/runs/{id}/metrics       (first-class dimensions, fold #9)
  span()/step()  -> POST /v1/runs/{id}/spans | /steps      (trajectory)
  log_artifact() -> POST /v1/runs/{id}/artifacts, or the presign upload flow
                    (fold #16: fingerprint -> presign -> PUT to R2 -> confirm)
  link()         -> PATCH /v1/runs/{id} (per-key new-wins merge into the real
                    runs.foreign_keys column, fold #8)
  snapshot()     -> content-addressed execution record (fold #7); pins run.env_ref
                    and records git provenance on a code_snapshot artifact
  finish()       -> PATCH /v1/runs/{id} {status, ended_at}

The presign upload flow carries ``kind``/``meta`` (Harbor-ownership Phase 0), so
byte uploads and reference artifacts label identically — no gaps flagged.
"""

from __future__ import annotations
import os
import threading
import weakref
from typing import TYPE_CHECKING, Any
from uuid import uuid4
from .. import errors
from ..capture import outputs as _outputs
from ...foundation.compose.compose import compose

if TYPE_CHECKING:
    from collections.abc import Callable

    from ..client.client import Client
from probe.sdk.run.closing.close import CloseMixin
from probe.sdk.run.closing.closing import ClosingMixin
from probe.sdk.run.closing.drain import CloseDrainMixin
from probe.sdk.run.closing.heartbeat import HeartbeatMixin, _Progress
from probe.sdk.run.closing.lease import WriterLeaseMixin
from probe.sdk.run.closing.status import StatusMixin
from probe.sdk.run.closing.terminal import TerminalMixin
from probe.sdk.run.commands.commands import CommandBox, RunCommandsMixin
from probe.sdk.run.resume.resume import ResumeMixin
from probe.sdk.run.config import ConfigMixin
from probe.sdk.run.files.capture import CaptureMixin
from probe.sdk.run.files.code_files import CodeFilesMixin
from probe.sdk.run.files.code_upload import CodeUploadMixin
from probe.sdk.run.files.files import FilesMixin
from probe.sdk.run.files.registry import ArtifactRegistryMixin
from probe.sdk.run.files.snapshot import SnapshotMixin
from probe.sdk.run.files.uploads import UploadsMixin
from probe.sdk.run.launch.execute import ExecuteMixin
from probe.sdk.run.launch.host_claims import HostClaimsMixin
from probe.sdk.run.metadata import MetadataMixin
from probe.sdk.run.metrics.derived import DerivedMetricsMixin
from probe.sdk.run.metrics.metrics import MetricsMixin
from probe.sdk.run.metrics.pending import PendingRowsMixin, _PendingRow
from probe.sdk.run.metrics.resume import ResumeGuardMixin
from probe.sdk.run.metrics.spans import SpansMixin
from probe.sdk.run.samples.mixin import SamplesMixin


@compose
class Run(
    ConfigMixin,
    MetadataMixin,
    MetricsMixin,
    PendingRowsMixin,
    ResumeGuardMixin,
    DerivedMetricsMixin,
    SpansMixin,
    SamplesMixin,
    FilesMixin,
    ArtifactRegistryMixin,
    UploadsMixin,
    CodeUploadMixin,
    CodeFilesMixin,
    SnapshotMixin,
    CaptureMixin,
    ClosingMixin,
    CloseMixin,
    CloseDrainMixin,
    TerminalMixin,
    HeartbeatMixin,
    WriterLeaseMixin,
    StatusMixin,
    ExecuteMixin,
    HostClaimsMixin,
    RunCommandsMixin,
    ResumeMixin,
):
    def __init__(self, client: "Client", data: dict):
        self._client = client
        self._data = data
        self._hb_stop: threading.Event | None = None
        self._hb_thread: threading.Thread | None = None
        self._hb_finalizer: weakref.finalize | None = None
        # Auto-update run lock. Held for the life of a process-bound run so an
        # upgrade cannot replace the installed tree mid-experiment; see
        # probe.foundation.durable.run_lock. None for detached runs, which use a lease instead.
        self._run_lock = None
        self._run_lock_leased = False
        # Auto-step counters, per metric kind. Guarded because logging from
        # several threads is ordinary (a sampler beside a training loop), and two
        # threads reading the same counter would put two points on one step.
        self._steps: dict[str, int] = {}
        self._steps_lock = threading.Lock()
        # Plan (d): (reason, key) pairs `log` already warned about while
        # flattening a nested dict -- once per key per run, not once per step.
        self._flatten_warned: set[tuple[str, str]] = set()
        # ...and the distinct keys nested dicts have minted on this run, against
        # `_NESTED_KEY_BUDGET` (#2009 review).
        self._nested_keys: set[str] = set()
        # Plan (f): rows `log(commit=False)` is holding, one per metric kind, and
        # the attributes recently sent per step (the server replaces a step
        # record whole, so a repeat write sends the union). One lock for both.
        self._pending_rows: dict[str, _PendingRow] = {}
        self._step_records_sent: dict[int, tuple[str | None, dict[str, Any]]] = {}
        self._pending_lock = threading.Lock()
        self._commit_after_finish_warned = False
        # Plan (c): config keys `update_config` already warned about changing,
        # and whether it already said the server cannot merge config.
        self._config_warned: set[str] = set()
        self._config_merge_refused = False
        # Writer-session identity (research-os#364): one id per handle, so the
        # engine can tell which process produced a write once a run has been
        # reopened. A reattached handle gets the id its reopen registered.
        self.session_id: str = str(uuid4())
        # Writer epoch (0185): the generation this handle writes under — 1 for
        # the original execution, bumped by the server on every reopen. Rides
        # on every telemetry write so a superseded process is refused at the
        # door instead of splicing into the successor's curve. Taken from the
        # row a create/read/reopen returned (RunDetailOut always carries it);
        # attach_run overrides from its receipt or PROBE_RUN_EPOCH.
        #
        # None when nothing SUPPLIED it (SDK reliability 1.10): the CLI's
        # offline handle is `Run(client, {"id": ref})`, and defaulting that to
        # 1 fenced every `probe --async log` on a reopened run (409, dead
        # letter). An unknown epoch is sent as no epoch, the fence's fail-open.
        raw_epoch = (data or {}).get("write_epoch")
        self.write_epoch: int | None = int(raw_epoch) if raw_epoch is not None else None
        # 0205. Do this handle's beats come from INSIDE the work? `_wrap_run`
        # sets it; a launcher's handle leaves it False. Under a wrapped run the
        # launcher and the job both beat as owners, and this is the only thing
        # that distinguishes "the run is held open" from "the job is reporting".
        self.attached: bool = False
        # Armed by attach_run() after a reopen: the last step the previous
        # execution wrote. Explicit steps at or below it are refused, and
        # auto-steps start above it.
        self._resume_from_step: int | None = None
        # (kind, key) -> that key's last step on the server (#364); None = one floor for every key.
        self._resume_key_floors: dict[tuple[str, str], int] | None = None
        self._auto_step_floor = 0
        # D17: what this run produces, captured when it ends. Set by
        # `_start_capture` (Client.run / probe.init) or `execute`.
        self._capture: _outputs.OutputCapture | None = None
        # Plan (n): `ignore=` patterns from Client.run / probe.init, added to the
        # `.probeignore` file and PROBE_IGNORE; rules loaded once per directory.
        self._ignore_patterns: tuple[str, ...] = ()
        self._ignore_cache: dict[str, Any] = {}
        # The rules for the directory `execute` ran its child in, for the
        # child's reads (collected after it exits).
        self._child_ignore: Any = None
        # Reasons already warned about for an upload that ended as a pointer
        # row (`_warn_not_uploaded`): a checkpoint saved every N steps must
        # not print the same line N times.
        self._uploads_warned: set[str] = set()
        # Cleared by `fluent.init` for a non-zero rank attached to a shared run
        # (interim until per-writer leases, plan 2.8), and by `fluent`'s exit
        # hook when a finalizing launcher holds the real exit code: such a
        # handle delivers its data but sends no terminal status.
        self._sends_terminal_status: bool = True
        # The terminal status this handle has sent (written, or journaled to
        # land), or None. The exit hook reads it so it never closes a run the
        # script already closed.
        self._closed_status: str | None = None
        # 2.2: the process that opened this handle. A write from any OTHER pid
        # is a forked child carrying the run on (a daemonizing script), which
        # the output helper must not report dead when the opener exits.
        self._opened_pid = os.getpid()
        self._forked_writer_marked: int | None = None
        # SDK reliability 2.8. The writer lease this handle beats and closes
        # under (`Client._wrap_run` sets it), None for the run-level heartbeat;
        # the protocol the server last said the run is on ('leases', or
        # 'legacy' once a writer that does not speak leases joined); and the
        # progress counter its lease beats carry.
        self._lease: dict | None = None
        self._lease_protocol: str | None = None
        #: Whether the server is known to hold this lease (a create or reopen
        #: that carried it, or a beat that landed). A release of a lease the
        #: server never saw would close nothing.
        self._lease_registered = False
        self._progress = _Progress()
        self._commands = CommandBox()
        # (status, exception) an integration reported through
        # `fluent.note_exit` for an ending no process hook sees (Lightning's
        # SIGTERMException: a code-less SystemExit). `__exit__` prefers it to
        # that SystemExit's "code None means success".
        self._noted_exit: tuple[str, BaseException | None] | None = None
        # What `finish()` returned; `_UNSET` until it is called. See `finish`.
        self._finish_result: Any = _UNSET
        # Writes the client had already DROPPED (outbox full, unwritable) when
        # this handle was made; finish() reports the ones dropped since (plan
        # 0.1). Per client, not per run: a client hosting two runs at once
        # reports its drops on whichever closes -- an over-report, never a
        # silent one.
        self._dropped_baseline = int(getattr(client, "dropped_writes", 0) or 0)
        # Likewise the writes sent straight to the server below the outbox's
        # free-space floor (plan 1.5): not lost, but not durable either.
        self._direct_baseline = int(getattr(client, "direct_sends", 0) or 0)
        # Set by `fluent` for a run whose closer is not the caller's choice (a
        # reinit closing the previous run): the status queued when Ctrl-C or a
        # SystemExit cuts the close short, instead of the one asked for.
        self._status_on_interrupt: str | None = None
        # The status of a terminal write already on its way (see `_close`).
        self._terminal_in_flight: str | None = None
        # Called once a close has settled (`fluent` releases the client it
        # built for a `create_new` run, which only its handle can close).
        self._after_finish: Callable[[], None] | None = None

    def _finish_called(self) -> bool:
        """Whether `finish()` has run on this handle, or is running now."""
        return getattr(self, "_finish_result", _UNSET) is not _UNSET

    def _stamp_writer(self, body: dict) -> dict:
        """Ride the writer fingerprint on a telemetry body (0185).

        A pre-0185 server ignores both fields (Pydantic drops undeclared body
        keys), so stamping is unconditionally safe; a 0185+ server uses them to
        refuse a superseded writer at the door. An epoch this handle does not
        know is omitted, never guessed (see ``write_epoch``)."""
        body["session_id"] = self.session_id
        if self.write_epoch is not None:
            body["write_epoch"] = self.write_epoch
        return body

    #: Plan 2.4 (D6): calls dropped below the resume point, and what the
    #: warning, the resume line and the `resume_guard` span report. Class
    #: defaults, so a handle that never resumes carries nothing.
    _resume_drops = 0
    _resume_first_dropped: int | None = None
    _resume_last_dropped: int | None = None
    _resume_first_drop_at: str | None = None
    _resume_announced = False
    _resume_resumed_at: int | None = None
    #: True when the guard was armed by an attach that reopened the run
    #: (PROBE_RUN_ID): `probe.init()` there takes no `on_conflict`, so the drop
    #: message names the exits that work from an attach (`_resume_exits`).
    _resume_via_attach = False

    # -- identity -----------------------------------------------------------
    @property
    def id(self) -> str:
        return str(self._data["id"])

    @property
    def experiment_id(self) -> str | None:
        """This run's experiment, or None for a PROJECT-DIRECT run (0054).

        Returns None rather than the string ``"None"``. It used to stringify
        unconditionally, and the only caller is :meth:`child` -- which therefore
        POSTed to ``/v1/experiments/None/runs`` on every project-direct run, the
        W&B-shaped half of the platform.
        """
        value = self._data.get("experiment_id")
        return None if value is None else str(value)

    @property
    def project_id(self) -> str | None:
        """This run's project. Present on every run since 0054; None on a row
        from a backend that predates it."""
        value = self._data.get("project_id")
        return None if value is None else str(value)

    @property
    def name(self) -> str:
        return str(self._data["name"])

    @property
    def description(self) -> str | None:
        return self._data.get("description")

    @property
    def repo(self) -> str | None:
        """Repository derived from the standalone README embed, if present."""
        return self._data.get("repo")

    @property
    def status(self) -> str:
        return str(self._data.get("status", "running"))

    @property
    def slug(self) -> str | None:
        """Human-readable petname (fold #21); present on /v1 reads (RunDetailOut)."""
        return self._data.get("slug")

    @property
    def foreign_keys(self) -> dict:
        """Incumbent-id map (fold #8); present on /v1 reads (RunDetailOut)."""
        return self._data.get("foreign_keys") or {}

    #: The execution record this handle's own `snapshot()` pinned. Kept apart
    #: from `_data` because under async writes the env_ref PATCH is still
    #: queued, so the row this handle holds does not show it yet.
    _pinned_env_ref: str | None = None

    @property
    def env_ref(self) -> str | None:
        """The execution record this handle believes the run is pinned to
        (fold #7): the hash its own `snapshot()` pinned LOCALLY, else the
        server row this handle last read. Not proof the server stored it --
        under async writes that PATCH may still be queued, or may yet fail;
        `probe run check` reads the server's answer. None when nothing is
        pinned -- including right after `probe.init()` under async writes,
        until the open's record answers on its own thread (at most ~7.5 s;
        `_wait_for_open_record` waits for it).

        The hardware rail reads it to never mint an inventory record over a
        real snapshot's: its env_ref PATCH would queue FIFO behind the
        snapshot's, so without this it would always land last and win."""
        return self._pinned_env_ref or self._data.get("env_ref")

    @property
    def url(self) -> str | None:
        """This run's dashboard page, or None when the origin cannot be known.

        A property and not a print: a library that writes to stdout corrupts
        whatever the training script's own output is being parsed by. Scripts
        that want it visible say so themselves -- `print(run.url)` at the end of
        a job puts a clickable link in the cluster log, which is the one place a
        researcher is already looking when they want to know how it went.
        """
        from ..reads.links import entity_url

        return entity_url("run", self.id, api_base_url=self._client.settings.base_url)

    @property
    def data(self) -> dict:
        return self._data

    def refresh(self) -> "Run":
        self._data = self._client.get_run(self.id)
        return self

    def edges(self) -> list[dict]:
        """Lineage edges touching this run (fold #2): GET /v1/runs/{id}/edges."""
        return self._client.transport.get(f"/v1/runs/{self.id}/edges")

    # -- spine --------------------------------------------------------------
    def child(self, name: str | None = None, *, relation: str, **kw) -> "Run":
        """Open a run descended from this one. ``relation`` is REQUIRED.

        ``name`` is not: omitted, the server mints a petname and titles the run
        from its own content once it finishes, exactly like any other run. A
        name passed here is a person's and is never renamed.

        ``fork`` (branched off mid-flight), ``resume`` (continued after a stop),
        ``retry`` (another attempt at the same thing) or ``branch``. There is no
        default: the four mean different things, and a guessed one is stored as a
        claim someone reads later as a measurement. The server refuses the pair
        without it anyway (`RunCreate` 422, and `runs_parent_pair_chk`).

        For a run that CONSUMED this one's output rather than re-attempting it --
        an eval of its checkpoint, an SFT run over its rollouts -- none of the four
        is honest. That is a lineage edge, not parentage: ``probe edge add
        --relation consumes`` (or ``evaluates_on`` / ``derived_from``).

        The child inherits this run's attachment, which is why it branches: a
        project-direct parent begets a project-direct child. Passing
        ``self.experiment_id`` unconditionally is what used to POST to
        ``/v1/experiments/None/runs`` for every project-direct run. An unfiled
        parent (an older CLI made it) has no home to inherit: ``ProjectRequired``.
        """
        if self.experiment_id is not None:
            return self._client.create_run(
                self.experiment_id,
                name,
                parent_run_id=self.id,
                parent_relation=relation,
                project_id=self.project_id,
                **kw,
            )
        if self.project_id is not None:
            return self._client.create_project_run(
                self.project_id,
                name,
                parent_run_id=self.id,
                parent_relation=relation,
                **kw,
            )
        if "project_id" in self._data:
            # Unfiled: the key is there and null, which a pre-0054 row never is.
            raise errors.build_unfiled_parent_error(self.id)
        raise errors.ValidationError(
            f"run {self.id} reports neither an experiment nor a project — this "
            "research-os backend predates project-direct runs (0054). Upgrade the "
            "backend, or open the child under an experiment."
        )
from probe.sdk.run.handle import _UNSET  # noqa: E402 -- pieces need each other; the front door loads this one first
