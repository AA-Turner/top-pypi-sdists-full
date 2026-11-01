"""The Probe Research SDK client core.

Two write paths, one core (per the SDK/CLI primitives sketch):
  * granular ``/v1`` calls for interactive / agent-driven capture (Anthrogen);
  * one-shot idempotent ``/ingest`` push for install-once passive capture (Osmosis).

Every method maps onto a real v4 endpoint (Probe Research v0.4.0.0 ingestion fold-in).
"""

from __future__ import annotations
import threading
from ..delivery.transport.protocols import observe_with
from ..delivery.delivery import Delivery
# The same rule for the crash reports' ring buffer, which hears every request. Transport sits
# below it and no longer imports it, so the client loads it and hands it down.
from .. import diagnostics as _request_log
from ...foundation.compose.compose import compose
from ...generated.models import Authorship as Authorship  # re-export: probe.Authorship
from probe.sdk.client.core import CoreMixin
from probe.sdk.client.credentials import CredentialsMixin
from probe.sdk.client.resources.artifacts import ArtifactsMixin, ArtifactsResource
from probe.sdk.client.resources.auth import AuthMixin, AuthResource
from probe.sdk.client.resources.catalog import CatalogMixin, CatalogResource
from probe.sdk.client.resources.delivery import DeliveryMixin
from probe.sdk.client.resources.integrations import IntegrationsMixin, IntegrationsResource
from probe.sdk.client.resources.lineage import LineageMixin, LineageResource
from probe.sdk.client.resources.notes import NotesMixin, NotesResource
from probe.sdk.client.resources.projects.admin import ProjectAdminMixin
from probe.sdk.client.resources.projects.experiment_admin import ExperimentAdminMixin
from probe.sdk.client.resources.projects.experiment_locator import ExperimentLocatorMixin
from probe.sdk.client.resources.projects.experiments import ExperimentsMixin, ExperimentsResource
from probe.sdk.client.resources.projects.headlines import HeadlinesMixin
from probe.sdk.client.resources.projects.papers import PapersMixin, PapersResource
from probe.sdk.client.resources.projects.projects import ProjectsMixin, ProjectsResource
from probe.sdk.client.resources.projects.summaries import SummariesMixin, SummariesResource
from probe.sdk.client.resources.reads import ReadsMixin, ReadsResource
from probe.sdk.client.resources.runs.attach import RunAttachMixin
from probe.sdk.client.resources.runs.check import RunCheckMixin
from probe.sdk.client.resources.runs.create import RunCreateMixin
from probe.sdk.client.resources.runs.listing import RunListingMixin
from probe.sdk.client.resources.runs.metrics import RunMetricsMixin, MetricsResource
from probe.sdk.client.resources.runs.reads import RunReadsMixin
from probe.sdk.client.resources.runs.reopen.conflict import ReopenConflictMixin
from probe.sdk.client.resources.runs.reopen.reopen import ReopenMixin
from probe.sdk.client.resources.runs.reopen.retry_lineage import RetryLineageMixin
from probe.sdk.client.resources.runs.reopen.status_holds import StatusHoldsMixin
from probe.sdk.client.resources.runs.reopen.takeover import TakeoverMixin
from probe.sdk.client.resources.runs.runs import RunsMixin, RunsResource
from probe.sdk.client.resources.runs.views import RunViewsMixin
from probe.sdk.client.resources.runs.writers import RunWritersMixin
from probe.sdk.client.resources.sessions import SessionsMixin, SessionsResource
from probe.sdk.client.resources.workspaces import WorkspacesMixin, WorkspacesResource
from probe.sdk.client.server_features import ServerFeaturesMixin
from probe.sdk.delivery.notices import DeliveryNoticesMixin
from probe.sdk.delivery.outbox.drainer import DrainerMixin

observe_with(_request_log)


@compose
class Client(
    CoreMixin,
    ServerFeaturesMixin,
    CredentialsMixin,
    DeliveryNoticesMixin,
    DrainerMixin,
    DeliveryMixin,
    AuthMixin,
    WorkspacesMixin,
    ProjectsMixin,
    ProjectAdminMixin,
    SummariesMixin,
    HeadlinesMixin,
    ExperimentLocatorMixin,
    ExperimentsMixin,
    ExperimentAdminMixin,
    PapersMixin,
    ArtifactsMixin,
    CatalogMixin,
    RunsMixin,
    RunCreateMixin,
    RetryLineageMixin,
    ReopenConflictMixin,
    ReopenMixin,
    StatusHoldsMixin,
    TakeoverMixin,
    RunAttachMixin,
    RunWritersMixin,
    RunReadsMixin,
    RunMetricsMixin,
    RunViewsMixin,
    RunCheckMixin,
    RunListingMixin,
    LineageMixin,
    IntegrationsMixin,
    SessionsMixin,
    NotesMixin,
    ReadsMixin,
):
    #: True for a client whose queue is drained by hand on purpose -- the
    #: offline run's, which `probe sync` drains (plan 2.12) -- so the "no
    #: background drainer" notice below would only be noise.
    _drains_by_hand = False

    @property
    def _delivery(self) -> Delivery:
        """The write pipeline and its sinks (`sdk/delivery/delivery.py`); built on first use by a
        Client made without __init__ (a test double)."""
        delivery = self.__dict__.get("_delivery_pipeline")
        if delivery is None:
            delivery = self.__dict__["_delivery_pipeline"] = Delivery(self)
        return delivery

    # -- resources: typed reads per domain; the flat methods keep returning dicts --------------
    @property
    def runs(self) -> RunsResource:
        """Typed run reads: `client.runs.get(run_id)` is a `RunPageDetailOut`, `.list()` a page of
        `RunDetailOut`. Built on each access and holding only the client, so nothing cycles."""
        return RunsResource(self)

    @property
    def projects(self) -> ProjectsResource:
        """Typed project reads: `client.projects.get(project_id)` is a `ProjectDetailOut`."""
        return ProjectsResource(self)

    @property
    def experiments(self) -> ExperimentsResource:
        """Typed experiment reads: `client.experiments.get(experiment_id)` is a
        `ProjectExperimentDetailOut`."""
        return ExperimentsResource(self)

    @property
    def metrics(self) -> MetricsResource:
        """Typed metric reads: `client.metrics.list(run_id)` is a list of `MetricPointOut`."""
        return MetricsResource(self)

    @property
    def artifacts(self) -> ArtifactsResource:
        """Typed artifact reads: `client.artifacts.get(artifact_id)` is an `ArtifactDetailOut`."""
        return ArtifactsResource(self)

    @property
    def catalog(self) -> CatalogResource:
        """Typed source and artifact-version reads: `client.catalog.get_source(ref)` is a
        `SourceOut`."""
        return CatalogResource(self)

    @property
    def lineage(self) -> LineageResource:
        """Typed lineage reads: `client.lineage.get_run_inputs(run_id)` is a `RunInputsOut`."""
        return LineageResource(self)

    @property
    def papers(self) -> PapersResource:
        """Typed paper reads: `client.papers.get(paper_id)` is a `PaperOut`."""
        return PapersResource(self)

    @property
    def summaries(self) -> SummariesResource:
        """Typed summary reads: `client.summaries.get(project=...)` is a `SummaryOut`."""
        return SummariesResource(self)

    @property
    def notes(self) -> NotesResource:
        """Typed note reads: `client.notes.get_team_note()` is a `TeamNoteOut`."""
        return NotesResource(self)

    @property
    def sessions(self) -> SessionsResource:
        """Typed session reads: `client.sessions.get_work(session_id)` is a `SessionWorkOut`."""
        return SessionsResource(self)

    @property
    def workspaces(self) -> WorkspacesResource:
        """Typed workspace reads: `client.workspaces.get(workspace_id)` is a `WorkspaceOut`."""
        return WorkspacesResource(self)

    @property
    def integrations(self) -> IntegrationsResource:
        """Typed code and commit reads: `client.integrations.get_run_code(run_id)` is a
        `RunCodeOut`."""
        return IntegrationsResource(self)

    @property
    def auth(self) -> AuthResource:
        """Typed token reads: `client.auth.list_tokens()` is a list of `TokenOut`."""
        return AuthResource(self)

    @property
    def reads(self) -> ReadsResource:
        """Typed search and browse reads: `client.reads.search(query)` is a `SearchResponse`."""
        return ReadsResource(self)

    # -- lifecycle ----------------------------------------------------------
    def _register_run_heartbeat(self, stop: threading.Event) -> None:
        self._run_heartbeat_stops.add(stop)

    def hand_off_delivery(self) -> None:
        """Stop delivering through this client and leave the queue deliverable.

        ONE definition, called from every place that stops an exporter. It used
        to be copy-pasted into `_settle_journaled_finish` and
        `_queue_deferred_finish`, one copy was fixed, and the other kept the bug
        through three reviews -- a near-duplicate is exactly how a fix fails to
        stick.

        Two rules, both learned the hard way:

        * Only hand off where a detached worker can actually be spawned.
          `_kick_drainer` early-returns on a non-default transport, so closing
          the exporter on an F2 client (explicit async + injected transport +
          drain_interval) left NOTHING delivering -- and `_after_enqueue` never
          respawns a closed exporter, so every later write was stranded too.
        * Clear the attribute after closing, but only if the exporter was
          ALIVE. A dead one is dead because of an auth block, and the
          documented invariant is that those are not respawned -- clearing it
          unconditionally would rebuild an exporter against the same rejected
          credential, which is the zombie-uploader pitfall.
        """
        exporter = self._exporter
        if not self._default_transport:
            return
        if exporter is not None:
            was_alive = getattr(exporter, "alive", True)
            exporter.close()
            if was_alive:
                self._exporter = None
        self._kick_drainer(force=True)

    def close(self, *, timeout: float | None = None) -> None:
        # The exporter drains over this client's transport; join it first. Its
        # own stop path now does a final pass, so ops written since the last
        # tick are delivered rather than left for a worker this client never
        # kicked. Then hand what remains to the detached worker: a closed
        # exporter delivers nothing, and `with Client(...) as c:` used to strand
        # everything written in the last drain_interval.
        #
        # ``timeout`` caps that join below its own 5 s: a reinit passes what is
        # left of its bound, which an exporter stuck mid-request overran by up
        # to 5 s (review of #2016). An exporter still running is abandoned as
        # after any timed-out join; its ops are on disk, and the worker kicked
        # below delivers them.
        if self._exporter is not None:
            if timeout is None:
                self._exporter.close()
            else:
                self._exporter.close(timeout=max(0.0, min(5.0, timeout)))
            self._exporter = None
            try:
                self._kick_drainer(force=True)
            except Exception:  # noqa: BLE001 -- a close may never raise
                pass
        if self._seal_producer_on_close:
            try:
                self.journal.seal_producer()
            except Exception:  # noqa: BLE001 -- accounting must never block close
                pass
        # Beats ride this client's transport; leaving them running would spin a
        # thread per unfinished run against a closed httpx client every interval.
        for stop in list(self._run_heartbeat_stops):
            stop.set()
        # Requests this client set aside reach its delivery counts even when it
        # never wrote anything else to report them with (a receipt-only client).
        reported = getattr(self, "_reported", None)
        if self._discarded_requests and isinstance(reported, dict) \
                and self._discarded_requests != int(reported.get("discarded") or 0):
            try:
                self._report_delivery(final=True)
            except Exception:  # noqa: BLE001 -- a close may never raise
                pass
        self.transport.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- fail-open write ----------------------------------------------------
    def write(
        self,
        method: str,
        path: str,
        body: dict | None = None,
        *,
        strict: bool | None = None,
        durable: bool = True,
        sync: bool = False,
        blocking: bool = True,
        raise_permanent: bool | None = None,
        admitted: bool = False,
    ):
        """A data write. In ``async_writes`` mode it is journaled without ever
        touching the network (the outbox drainer delivers it); otherwise it is
        attempted and journaled on failure unless ``strict`` (or ``fail_open``
        is off). Returns the parsed response, or None if it was journaled.

        ``sync=True`` forces the network path even under ``async_writes`` -- for
        the writes whose RESPONSE the caller needs in hand, not eventually. The
        terminal status flip is the one that matters: ``finish()`` drains the
        journal and then closes the run, so a queued close would return no row
        and leave the barrier claiming a delivery it had not made. It keeps the
        fail-open journal fallback, so forcing sync costs latency, never a raise.

        ``blocking=False`` marks a write that must never hold a run's close --
        `finish()` refuses to mark a run terminal while any of its ops are
        undelivered, which is right for data and wrong for a best-effort
        diagnostic that would otherwise decide the run's recorded fate.

        ``durable=False``: attempt directly, RAISE on failure, never touch the
        journal. Under async writes, only for a write that names no run -- the
        hardware rail's content-addressed inventory record. A direct write TO a
        run races the drainer on the server's run-row lock (503
        ``MetricWriteBusy``), so under async writes the rail's points and its
        env_ref PATCH go through :meth:`_enqueue_best_effort` (plan 0.3); under
        sync writes (`PROBE_ASYNC=0`) nothing drains until `finish()`, so the
        rail writes to the run directly here, as it did before.

        ``raise_permanent=True`` narrows fail-open to what fail-open is FOR: a
        failure that could succeed later. A 4xx refusal cannot -- the journal
        replays it until the drainer dead-letters it -- so queueing one converts
        an error the caller could act on into a success it cannot. A notes
        append against a full document was exactly that: the CLI printed
        "appended to project notes", exited 0, and the paragraph was never
        stored. Transient failures and auth blocks still journal, which is the
        resilience the fail-open path exists for. NOT the default: the metric
        rail must not raise into a training loop over one refused point, which
        is the same reason ``clamp_notes`` truncates at the ingest door instead
        of 422-ing the envelope. None (not passed) takes the client's own
        `raise_permanent`, which the CLI turns on for every write it makes
        (lineage plan L14) and nothing else does.

        A 409 carrying ``existing_id`` raises under it too. The outbox reads
        that answer as its OWN earlier delivery landing ("idempotent") -- true
        of a replay, never of this first attempt: the transport does not
        re-send a write that may have landed, and a daemon retry's
        Idempotency-Key replays the stored answer, not a 409. Queued, a
        duplicate `edge add` or a second genealogy parent drained as delivered
        and the CLI printed `null`, exit 0.

        A write that fails and falls back to the outbox (or is lost with it)
        is handed to `on_undelivered` when one is set (the CLI's).

        ``admitted=True``: if this write ends up journaled, the queue-length cap
        and the free-space floor do not refuse it (`Journal.append_http`). Only
        for a run's terminal status: its fail-open copy used to be refused by
        the same full queue that made it fail open (review of #2014, H5b)."""
        return self._delivery.write(
            method, path, body, strict=strict, durable=durable, sync=sync, blocking=blocking,
            raise_permanent=raise_permanent, admitted=admitted,
        )

    #: How many undelivered writes a hooked client keeps (`undelivered_writes`).
    UNDELIVERED_KEPT = 32

    def _note_undelivered(self, method: str, path: str, exc: BaseException, *, queued: bool) -> None:
        """`Delivery.note_undelivered`; never raises."""
        self._delivery.note_undelivered(method, path, exc, queued=queued)

    #: How long a direct send (below the free-space floor, plan 1.5) may hold
    #: the training thread, and how long after a failed one none is tried:
    #: from the first wait, doubling to the ceiling.
    DIRECT_SEND_TIMEOUT_SECONDS = 5.0
    DIRECT_SEND_BACKOFF = (60.0, 600.0)
    #: Above this many queued ops, no direct send is tried (see
    #: `_send_instead_of_queueing`).
    DIRECT_SEND_MAX_QUEUED = 1000

    def _send_instead_of_queueing(
        self, method: str, path: str, body: dict | None, *, out_of_space: bool = False
    ) -> bool:
        """`DirectSink.send_instead_of_queueing` (plan 1.5): True when delivered."""
        return self._delivery.direct.send_instead_of_queueing(method, path, body, out_of_space=out_of_space)

    def _enqueue(
        self,
        method: str,
        path: str,
        body: dict | None,
        *,
        blocking: bool = True,
        validation_error: str | None = None,
        prepared: bool = False,
        admitted: bool = False,
        direct_ok: bool = False,
    ) -> bool:
        """`JournalSink.enqueue`: whether the op landed; never raises for a failure of ours."""
        return self._delivery.journaled.enqueue(
            method, path, body, blocking=blocking, validation_error=validation_error, prepared=prepared,
            admitted=admitted, direct_ok=direct_ok,
        )

    def _enqueue_upload(self, **kwargs) -> dict | None:
        """`JournalSink.enqueue_upload`: the journal's result, or None; never raises for ours."""
        return self._delivery.journaled.enqueue_upload(**kwargs)

    #: How often a writing process reads status.json for delivery trouble
    #: (plan 1.7); between reads it costs one monotonic check per write.
    NOTICE_POLL_SECONDS = 15.0
    #: A queue whose oldest write has waited this long is "stalled".
    STALLED_AFTER_SECONDS = 600.0

    #: How often a writing process reports its delivery counts (plan 1.12).
    DELIVERY_REPORT_SECONDS = 900.0

    #: The most an exiting process spends promoting its own waiting uploads;
    #: a scan already started finishes, none starts after it.
    _EXIT_PROMOTE_SECONDS = 60.0

    def _enqueue_best_effort(self, method: str, path: str, body: dict | None) -> bool:
        """`FanOutSink.enqueue_best_effort` (the hardware rail, plan 0.3). Not public API."""
        return self._delivery.fanout.enqueue_best_effort(method, path, body)

    #: At most one credential re-read per this many seconds (plan 2.7). A
    #: revoked token refuses EVERY request, and a beat, a drain and a flush
    #: asking at once must not each re-read the config and each warn.
    _CREDENTIAL_REFRESH_SECONDS = 30.0

    #: 0268. The server feature that makes a run create safe to send twice.
    _CREATION_REPLAY_FEATURE = "run_creation_key"

    #: Statuses that mean the predecessor is over. Mirrors `_DEAD_RUN_STATUSES`
    #: and INCLUDES `untracked` -- the reaper's verdict for a run that never
    #: heartbeated, which is the designed terminal state for agent-driven CLI runs
    #: and therefore exactly this feature's population. 48 runs carry it fleet-wide.
    _RETRY_DEAD_STATUSES = frozenset({"failed", "crashed", "canceled", "untracked"})

    #: The launch fields a relaunch keeps (`metadata.launch.process`).
    _RETRY_LAUNCH_KEYS = ("entrypoint", "argv", "cwd")

    #: Statuses whose numbers cannot be trusted; superseding one marks it.
    _DEAD_RUN_STATUSES = frozenset({"failed", "crashed", "canceled", "untracked"})

    #: Verdicts attach will reopen automatically. ALL are verdicts NOBODY
    #: CHOSE: 'created' means the run was registered and never started,
    #: 'untracked' means the reaper found nothing owning it, and 'crashed'
    #: means the system saw the job's processes die -- the reaper's silence, a
    #: writer-gone report, a hand-off's leases all GONE (plan 2.8). The last is
    #: exactly what a requeued Slurm job finds seconds after `scontrol requeue`
    #: SIGTERMed its first attempt (the crash notice waits
    #: `crash_notice_requeue_grace_seconds` for it to come back). 'failed' and
    #: 'canceled' are deliberately absent -- a human or a real exit code chose
    #: those, and a stale PROBE_RUN_ID pasted into a .env must not quietly
    #: resurrect last week's cancelled run and write this week's curves into it.
    _REOPENABLE_ON_ATTACH = ("created", "untracked", "crashed")

    #: How long after a run ended attach will still adopt it. Past this, the id
    #: in your environment is much more likely to be stale than to be the run
    #: you meant. 24h covers an overnight queue wait, which is the case this
    #: exists for.
    _REOPEN_MAX_AGE_SECONDS = 24 * 60 * 60

    #: NO "trial". `PATCH /v1/trials/{id}` accepts the same notes writes and this
    #: client deliberately never sends them -- see `_NOTE_TARGETS` in the CLI for
    #: the reasoning. `update_trial` reaches that route for title and description,
    #: so the parity check still covers it. No "group" or "artifact" either:
    #: sweep groups and files stopped carrying notes (`notes.FILE_NOTES_REMOVED`).
    NOTES_ENTITIES = ("project", "experiment", "run")
