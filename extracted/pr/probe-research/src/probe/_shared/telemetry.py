"""Probe CLI telemetry: the install + backfill funnels, emitted in-process.

    wizard.invoked             wizard() entry, BEFORE bootstrap — so a broken
                               npx→persistent install still enters the funnel
    wizard.started             after state discovery (fresh_install known)
    wizard.action_chosen       an action resolved (menu or --action flag)
    wizard.configure_started   a configure run planned its work
    wizard.signed_in           the device-flow browser approval settled
    wizard.configure_completed the verdict (success / failed / unverifiable)
    wizard.install_settled     every selected coding agent finished applying
    wizard.imports_chosen      what the post-install import offer was answered
                               with — including the empty set, which is "skip"
    wizard.onboarding_completed the dashboard handoff page, the bottom of the
                               guided-install funnel
    wizard.recorder_changed    the Who records row switched: to the Probe
                               daemon or back to the agent, and how it ended

    backfill.started/.scanned/.plan_ready/.approved/.summary — the FOLDER
    import funnel; `summary` fires on EVERY exit path with an outcome enum.

    transcripts.summary        the past-sessions lane's verdict, one per exit
                               path — the other half of the import offer, which
                               had no funnel of its own at all.

    import_job.enqueued/.stalled/.finished — the DURABLE half. Both lanes now
    hand their approved work to a detached worker and return, so the lane
    events above end at "handed off": whether an import a person approved
    during onboarding ever FINISHED is only answerable here. The worker is a
    separate process, so it replays the approving session's `session_id` off
    the job record (`origin`) rather than inheriting a context object.

Funnel semantics: invoked→started drop-off is infrastructure (bootstrap or
state collection died); started→action_chosen is a human leaving. Dashboards
scope to invoked_by=human — the fleet's auto-update robots spawn
`probe wizard --action update --yes` and must never dominate the denominator.

Contract (mirrors the plugin hook's, adapted to a long-lived process):
  * OBSERVABILITY ONLY, fail-silent. Every failure is swallowed; the sender
    thread writes NOTHING to stdout/stderr — the wizard owns a centred
    full-screen frame and a stray traceback corrupts it.
  * ASYNC EMIT, NO SUBPROCESS. emit() stamps facts and enqueues
    (microseconds); ONE daemon thread drains in order and POSTs with a short
    timeout; an atexit flush bounds final delivery at FLUSH_TIMEOUT_S and
    drops the rest. Accepted losses: kill -9 loses queued events; a dead
    network delays process exit by <= the flush bound. The plugin hook keeps
    its detached-child sender — hook lifecycle constraints (return in
    milliseconds, system python3) do not apply here.
  * EMIT-TIME TRUTH. timestamp (ms ISO-8601 UTC), identity_mode, and funnel
    facts are stamped when the event happens, so a send that runs after
    sign-in can never misreport the pre-login entry state. The sender keys
    anonymous events to `machine:<id>` and authenticated ones to the user
    UUID per the event's own identity_mode — attribution is an invariant,
    not a race.
  * METADATA ONLY. ids, versions, counts, booleans, enum outcomes. No folder
    paths, no error strings (exception text can embed a path).
  * KILLSWITCH + HOSTED GATE. PROBE_TELEMETRY=off disables everything; so
    does a resolved base_url outside the hosted service (the self-host
    egress promise, extended to the client). Both are checked before the
    sender thread ever starts.

Emit call sites live at points where the interactive and flag-driven flows
have CONVERGED, never inside interactive-only menu code — the interactive
path has no test coverage, so an emission line only a menu executes would
ship permanently untested.
"""

from __future__ import annotations

import atexit
import os
import queue
import re
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from probe._compat import StrEnum, fromisoformat

from probe import __version__ as _cli_version
from probe.sdk import _telemetry_core as core
from probe.sdk.tls import ssl_context

# Sized ABOVE one POST timeout (core.SEND_TIMEOUT=3): the events emitted last
# — configure_completed, backfill.summary — are exactly the ones an exit flush
# shorter than a send would drop, biased against slow links (review R1,
# amending D6's ~1s). Exit only pays this when the network is already degraded.
FLUSH_TIMEOUT_S = 3.5
QUEUE_MAX = 256

EVENT_WIZARD_INVOKED = "wizard.invoked"
EVENT_WIZARD_STARTED = "wizard.started"
EVENT_WIZARD_ACTION_CHOSEN = "wizard.action_chosen"
EVENT_WIZARD_CONFIGURE_STARTED = "wizard.configure_started"
EVENT_WIZARD_SIGNED_IN = "wizard.signed_in"
EVENT_WIZARD_CONFIGURE_COMPLETED = "wizard.configure_completed"
EVENT_BACKFILL_INVOKED = "backfill.invoked"
EVENT_BACKFILL_STARTED = "backfill.started"
EVENT_BACKFILL_SCANNED = "backfill.scanned"
EVENT_BACKFILL_PLAN_READY = "backfill.plan_ready"
EVENT_BACKFILL_APPROVED = "backfill.approved"
EVENT_BACKFILL_SUMMARY = "backfill.summary"

#: The guided install's own completion, distinct from `configure_completed`:
#: that one is per configure CALL, this is "every selected coding agent has
#: been through and the installation is settled". A multi-agent install emits
#: several of the former and exactly one of the latter.
EVENT_WIZARD_INSTALL_SETTLED = "wizard.install_settled"
#: The post-install import offer, answered. The EMPTY set is a real answer --
#: skipping imports is the single most common thing to do here, and an event
#: that only fired when something was ticked would make the skip invisible.
EVENT_WIZARD_IMPORTS_CHOSEN = "wizard.imports_chosen"
#: The dashboard handoff page: the last screen of the guided install.
EVENT_WIZARD_ONBOARDING_COMPLETED = "wizard.onboarding_completed"

#: Removal, from the client's own side. The server already learns that a device
#: went away -- `client.uninstalled` is inferred from a capability report,
#: `client.device_disconnected` from the tap revoking its bearer -- but neither
#: can see the DECISION: the confirmation screen someone opened and backed out
#: of is the last moment the outcome was still reachable, and it reaches no
#: server at all. These two are the only place that funnel exists.
EVENT_WIZARD_UNINSTALL_STARTED = "wizard.uninstall_started"
EVENT_WIZARD_UNINSTALL_COMPLETED = "wizard.uninstall_completed"

#: The Who records row switched (`probe wizard` › Who records): the Probe
#: daemon turned on, or back off. The only place the daemon is switched
#: (Richard 2026-09-29), so this is the daemon's adoption funnel. `recorder`
#: is where the switch went and `outcome` how far it got (`RecorderOutcome`);
#: a team refused for its plan is reported too -- someone asked for the daemon.
EVENT_WIZARD_RECORDER_CHANGED = "wizard.recorder_changed"

#: The past-sessions lane's verdict. Named for the lane rather than folded into
#: `backfill.summary`, whose properties are folder-shaped (files, units,
#: coverage) and whose existing insights count folder imports.
EVENT_TRANSCRIPTS_SUMMARY = "transcripts.summary"

#: Durable background imports. `kind` (transcripts|folder) is the breakdown.
EVENT_IMPORT_JOB_ENQUEUED = "import_job.enqueued"
#: A running import that has stopped making progress -- and, unlike `finished`,
#: a LEVEL rather than an edge, so it is rate-limited at the call site.
EVENT_IMPORT_JOB_STALLED = "import_job.stalled"
#: The terminal state, emitted by the detached worker itself. THIS is "did the
#: import finish": `backfill.summary` fires when the wizard hands work off, and
#: reports `partial` with 0% coverage for everything still queued.
EVENT_IMPORT_JOB_FINISHED = "import_job.finished"
#: Approved imports thrown away without finishing -- by Uninstall, or by the
#: wizard's explicit Exit. Work someone asked for and will not get.
EVENT_IMPORT_JOB_CLEARED = "import_job.cleared"
#: One drain episode ended (the detached worker is exiting). The HAPPY path is
#: reported too, on purpose: without the drained baseline a silent fleet and a
#: fleet whose workers all died look identical from the dashboard.
EVENT_OUTBOX_DRAINED = "outbox.drained"
#: A queue that is stuck rather than merely busy, reported from the FOREGROUND
#: banner. The drainer reports the TRANSITION into auth-blocked/paused as it
#: exits; what it cannot report is the STANDING condition, because `maybe_spawn`
#: will not fork a worker while either persists. The next `probe` command is the
#: only process that ever sees a queue that has been wedged since yesterday.
EVENT_OUTBOX_STUCK = "outbox.stuck"
#: A TRAINING process's delivery counts (plan 1.12): every 15 min while it
#: writes and at each run's close. Deltas since its last report, counts only --
#: never a key, body, name or path -- so we see loss before a customer does.
EVENT_DELIVERY_SUMMARY = "sdk.delivery.summary"


class IdentityMode(StrEnum):
    ANONYMOUS = "anonymous"
    AUTHENTICATED = "authenticated"


class Via(StrEnum):
    WIZARD = "wizard"
    COMMAND = "command"
    OUTBOX = "outbox"  # the detached drainer and the every-command banner
    #: A detached import worker that could not find out who approved its job --
    #: a recovered job, or one enqueued while telemetry was off. When the
    #: origin IS on the record the worker replays the approver's `via` instead,
    #: so the approval and its completion share one funnel.
    IMPORT_JOB = "import_job"
    NONE = "none"  # null_context — never reaches the wire


class InvokedBy(StrEnum):
    HUMAN = "human"
    AUTOMATION = "automation"  # non-tty; the auto-update robot spawns land here


class SignInOutcome(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"


class ConfigureOutcome(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    UNVERIFIABLE = "unverifiable"


class ConfigureFailureKind(StrEnum):
    MISSING_GRANTS = "missing_grants"
    PLUGINS_ABSENT = "plugins_absent"
    RUNTIME = "runtime"


class BackfillOutcome(StrEnum):
    SUCCESS = "success"
    PARTIAL = "partial"  # finished, but units failed or enqueue had problems
    EMPTY_FOLDER = "empty_folder"
    #: The root itself could not be listed. Distinct from EMPTY_FOLDER on
    #: purpose: "there is nothing here" and "I could not look" are the two
    #: answers this flow exists to keep apart, and folding them together in
    #: analytics recreates the conflation in the one place nobody sees it.
    UNREADABLE_ROOT = "unreadable_root"
    ALREADY_IMPORTED = "already_imported"
    CREDENTIALS_FAILED = "credentials_failed"
    NO_PLAN = "no_plan"
    UNTRUSTED_CLASSIFICATION = "untrusted_classification"
    PROJECT_CREATE_FAILED = "project_create_failed"
    ABORTED = "aborted"
    ERROR = "error"  # unexpected crash; the exception itself is re-raised


class InstallSettledOutcome(StrEnum):
    """Whether the guided install ended with a verifiable installation.

    UNSETTLED is not a crash: an agent whose plugins could not be ASKED reports
    an unverified snapshot, and one unverified agent keeps the whole
    installation unsettled (see `_InstallationCompletion`). It is the state the
    dashboard refuses to advance on, so it is the state the funnel must count.
    """

    SETTLED = "settled"
    UNSETTLED = "unsettled"


class OnboardingOutcome(StrEnum):
    """How the dashboard handoff page -- the last guided-install screen -- ended."""

    DASHBOARD_OPENED = "dashboard_opened"
    #: Explicit Exit closes the wizard while approved imports keep running.
    EXITED = "exited"
    #: Esc back to the main menu. The install stands; the person chose to keep
    #: working in the terminal, which is not a drop-off.
    RETURNED_TO_MENU = "returned_to_menu"
    #: Ctrl-C leaves the handoff without choosing an action. Approved imports
    #: keep running; this records the navigation outcome, not lost import work.
    ABANDONED = "abandoned"


class TranscriptsOutcome(StrEnum):
    """Every exit path of the past-sessions lane.

    The four "nothing to do" values are kept apart on purpose. "Session capture
    was never paired", "this machine has no saved sessions", "the census found
    no VERIFIED candidates" and "the person said no" all render as a short
    message and an early return, and folding them together would hide which of
    them is costing the import offer its other half.
    """

    ENQUEUED = "enqueued"  # handed to a background worker; see import_job.*
    COMPLETED = "completed"  # ran to completion in this process
    SKIPPED = "skipped"  # declined at the review or the source picker
    BACK = "back"  # navigated back to the import selection; not an answer
    NO_SOURCES = "no_sources"  # no agent histories selected at all
    NO_SAVED_SESSIONS = "no_saved_sessions"  # nothing on disk to offer
    NOT_PAIRED = "not_paired"  # no capture credential, so no way to upload
    NO_CANDIDATES = "no_candidates"  # sessions exist; none verified importable
    ABORTED = "aborted"  # Ctrl-C
    ERROR = "error"  # unexpected crash; the exception itself is re-raised


class ImportJobOutcome(StrEnum):
    """The terminal state of one detached import worker."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    INTERRUPTED = "interrupted"  # a signal, or the machine going away
    #: Stopped on purpose, from the import's own detail screen. Kept apart from
    #: INTERRUPTED because they are opposite readings of the same stopped
    #: worker: one is a laptop closing, the other is somebody deciding they did
    #: not want this import -- and cancelling IS how a cancel reaches the
    #: worker, so without this the decision would be filed as an accident.
    CANCELED = "canceled"
    #: The worker process never got far enough to own the job -- a failed
    #: spawn, or children that could not be reclaimed. Separate from FAILED
    #: because nothing was imported and nothing was even attempted.
    LAUNCH_FAILED = "launch_failed"


class RecorderOutcome(StrEnum):
    """How a Who records switch ended, read back from each agent's saved
    recorder rather than assumed from the steps that ran."""

    #: Every coding agent on the device now records the chosen way.
    MOVED = "moved"
    #: Some agents moved and some did not (a plugin install failed).
    PARTIAL = "partial"
    #: None moved, past the gates below (a plugin install or config write).
    FAILED = "failed"
    #: The server said the team's plan does not include the daemon.
    REFUSED_PLAN = "refused_plan"
    #: The daemon's own key was not granted (the browser approval was
    #: declined or failed), so nothing moved.
    NO_KEY = "no_key"
    #: The daemon's AI libraries are missing and did not install, so nothing moved.
    NO_LIBRARIES = "no_libraries"


class UninstallOutcome(StrEnum):
    """How a removal ended.

    DECLINED is the point of the pair. Someone who opens the confirmation
    screen has already decided to leave; whether they went through with it is
    the only part still in play, and a funnel built on the server's
    after-the-fact signals can only ever count the ones who did.
    """

    REMOVED = "removed"
    DECLINED = "declined"


class ImportJobStall(StrEnum):
    """Why an approved import stopped moving.

    WAITING_FOR_CONNECTION is the worker saying so itself, from inside its
    retry loop. WORKER_VANISHED is an OBSERVATION made later by whichever
    process next reads the job: a RUNNING record whose pid is gone. Nothing
    emits the second one at the moment it happens -- the process that would
    have is the one that died.
    """

    WAITING_FOR_CONNECTION = "waiting_for_connection"
    WORKER_VANISHED = "worker_vanished"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _post_batch(entries: list[dict]) -> None:
    """The shared core's wire shape, over the package's TLS trust.

    The envelope lives in the core so both surfaces send one; the trust is
    the SDK's, so telemetry and SDK writes can never disagree about whether
    a proxy's certificate is good (plan item (l))."""
    core.post_batch(entries, context=ssl_context())


class _Sender:
    """One queue, one daemon thread, ordered delivery, silence everywhere."""

    def __init__(self) -> None:
        self.q: queue.Queue = queue.Queue(maxsize=QUEUE_MAX)
        self.transport = _post_batch  # test seam
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._stop = object()

    def start(self) -> None:
        with self._lock:
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(
                    target=self._run, daemon=True, name="probe-telemetry"
                )
                self._thread.start()

    def put(self, record: dict) -> None:
        try:
            self.q.put_nowait(record)
        except Exception:
            pass  # full queue: drop, never block or raise into the wizard

    def request_flush(self, timeout: float = FLUSH_TIMEOUT_S) -> None:
        """Bounded final delivery; called from atexit. Drops what misses the bound.

        A full queue means the stop sentinel cannot be enqueued — the bounded
        join still runs so an in-flight send gets its chance; the daemon thread
        then dies with the process, which is the accepted-loss path.
        """
        try:
            self.q.put_nowait(self._stop)
        except Exception:
            pass
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout)

    # -- thread side --------------------------------------------------------

    def _run(self) -> None:
        machine = core.machine_id()
        while True:
            item = self.q.get()
            batch: list[dict] = []
            saw_stop = item is self._stop
            if not saw_stop:
                batch.append(item)
            while True:
                try:
                    nxt = self.q.get_nowait()
                except queue.Empty:
                    break
                if nxt is self._stop:
                    saw_stop = True
                else:
                    batch.append(nxt)
            if batch:
                try:
                    # Send-time gate, mirroring the plugin sender: the context
                    # gate ran once at start against the RESOLVED base_url, but
                    # a hosted --base-url flag over a self-host config (or a
                    # mid-session context switch) must not ship the self-host
                    # identity to the vendor. The config the identity resolver
                    # reads is the config the gate must approve.
                    if core.hosted_base_url(core.effective_base_url(core.read_cli_config())):
                        self.transport(self._entries(batch, machine))
                except Exception:
                    pass  # PostHog down costs the session nothing
            if saw_stop:
                return

    def _entries(self, records: list[dict], machine: str) -> list[dict]:
        """Batch entries, honoring each record's emit-time identity_mode."""
        anon_ident = {
            "distinct_id": f"machine:{machine}",
            "customer_id": None,
            "workspace_id": None,
            "authenticated": False,
        }
        auth_ident: dict | None = None
        entries: list[dict] = []
        for record in records:
            pinned = record.get("identity")
            if pinned is not None:
                # Resolved before the credential that produced it was revoked;
                # re-resolving here would find nothing. See pin_identity.
                entries.extend(
                    core.build_batch(
                        [record], pinned, client_kind="cli", lib="probe-cli",
                        client_version=_cli_version, machine=machine,
                    )
                )
                continue
            if record.get("identity_mode") == IdentityMode.AUTHENTICATED:
                if auth_ident is None:
                    try:
                        auth_ident = core.resolve_identity(
                            core.read_cli_config(), machine=machine, context=ssl_context()
                        )
                    except Exception:
                        auth_ident = anon_ident
                ident = auth_ident
            else:
                ident = anon_ident
            # This sender is the CLI's, and only the CLI enqueues here. The hosted
            # MCP shares `_telemetry_core.build_batch`, NOT this queue -- it has its
            # own sender in mcp/accounting.py, precisely because `cli/` is excluded
            # from the MCP deploy filter. So these two stay literals.
            entries.extend(
                core.build_batch(
                    [record],
                    ident,
                    client_kind="cli",
                    lib="probe-cli",
                    client_version=_cli_version,
                    machine=machine,
                )
            )
        return entries


_sender: _Sender | None = None
_sender_lock = threading.Lock()
_flush_registered = False


def _ensure_sender() -> _Sender:
    global _sender, _flush_registered
    with _sender_lock:
        if _sender is None:
            _sender = _Sender()
        _sender.start()
        if not _flush_registered:
            atexit.register(_flush_at_exit)
            _flush_registered = True
        return _sender


def _flush_at_exit() -> None:
    sender = _sender
    if sender is not None:
        try:
            sender.request_flush()
        except BaseException:  # noqa: BLE001 - a second Ctrl-C lands here as
            pass  # KeyboardInterrupt; atexit would print it onto the TUI frame


@dataclass
class TelemetryContext:
    """The session handle threaded through the wizard and backfill.

    A disabled context is a real object whose emit() is a no-op, so call
    sites never branch — and `telemetry=None` parameters normalize through
    :func:`null_context`, keeping every existing caller and test unchanged.
    """

    session_id: str
    via: str  # Via value
    invoked_by: str  # InvokedBy value (tty-based; robots are non-tty)
    enabled: bool = True
    #: An identity resolved AHEAD of the event that needs it, for the one flow
    #: that destroys the credential it would have been resolved from. See
    #: :meth:`pin_identity`. None everywhere else, which is every other event.
    pinned_identity: dict | None = None

    @classmethod
    def start(cls, *, via: str, interactive: bool, base_url: str | None) -> "TelemetryContext":
        # The gate is evaluated once per context (accepted: a mid-session
        # reconfigure to self-host keeps this session emitting until exit —
        # bounded to one session; the sender's per-batch config gate still
        # protects identity). Killswitch + hosted gate both checked before the
        # sender thread ever exists.
        try:
            enabled = not core.telemetry_disabled() and core.hosted_base_url(base_url)
        except Exception:
            enabled = False
        ctx = cls(
            session_id=uuid.uuid4().hex,
            via=via,
            invoked_by=InvokedBy.HUMAN if interactive else InvokedBy.AUTOMATION,
            enabled=enabled,
        )
        if enabled:
            try:
                _ensure_sender()
            except Exception:
                ctx.enabled = False
        global _current
        _current = ctx
        return ctx

    def emit(
        self,
        event: str,
        *,
        identity_mode: str | None = None,
        **props,
    ) -> None:
        """Stamp emit-time truth and enqueue; returns in microseconds.

        identity_mode defaults to the CURRENT config's token presence — the
        default computes at emit time, so a forgotten kwarg can never mislabel
        an authenticated event as anonymous. Pass it explicitly only to pin a
        mode the caller knows better than the config does.
        """
        if not self.enabled:
            return
        try:
            if self.pinned_identity is not None and not identity_mode:
                # The config this would otherwise read is gone; the pin IS the
                # emit-time truth for these events.
                mode = IdentityMode.AUTHENTICATED
            else:
                mode = str(identity_mode) if identity_mode else identity_mode_from_config()
            properties = {
                "session_id": self.session_id,
                "via": self.via,
                "invoked_by": self.invoked_by,
                "identity_mode": mode,
            }
            properties.update({k: v for k, v in props.items() if v is not None})
            # Same contract as core.build_batch: detected or absent, never a
            # placeholder that reads as Claude Code for a Cursor user.
            detected = core.detect_agent_label()
            if detected is not None:
                properties.setdefault("agent", detected)
            record = {
                "event": event,
                "identity_mode": mode,
                "timestamp": _now_iso(),
                "properties": properties,
            }
            if self.pinned_identity is not None:
                record["identity"] = self.pinned_identity
            _ensure_sender().put(record)
        except Exception:
            pass  # observability must never become observable


    def pin_identity(self) -> None:
        """Resolve this device's identity NOW, before something destroys it.

        Every other event is attributed lazily: the sender thread resolves the
        user from the config at SEND time, which keeps a /v1/me call off the
        hot path and lets a mid-session login re-key later events correctly.

        Uninstall breaks that. `finish_removal` REVOKES this device's token
        server-side and then clears it off the disk, and the event reporting
        that removal is emitted afterwards -- so the sender finds no token,
        falls back to `machine:<id>`, and the one event in the product that
        says a customer left arrives attached to no person at all. Every
        #probe-usage destination filters on `email is_set`, so it is not merely
        mis-attributed: it is dropped.

        Resolving early rather than emitting early is deliberate. Emitting
        first does not help -- the sender drains asynchronously and would still
        read a cleared config -- and the identity cache cannot cover it either,
        because its key is a hash of the TOKEN and `resolve_identity` returns
        the machine fallback before even looking at the cache once the token is
        gone. The call must happen while the credential is both present and
        still valid, which is exactly here.

        Cheap in practice: any signed-in wizard run has already resolved this
        identity for its earlier events, so this is a cache read. Cold, it is
        one bounded request. Fail-soft, like everything else in this module --
        an unresolvable identity leaves the pin unset and the event falls back
        to the old behaviour rather than failing the uninstall.
        """
        if not self.enabled:
            return
        try:
            identity = core.resolve_identity(
                core.read_cli_config(), machine=core.machine_id(), context=ssl_context()
            )
            if identity.get("authenticated"):
                self.pinned_identity = identity
        except Exception:
            pass  # observability must never become observable


def null_context() -> TelemetryContext:
    return TelemetryContext(
        session_id="", via=Via.NONE, invoked_by=InvokedBy.AUTOMATION, enabled=False
    )


#: The context this PROCESS started, if any. One command builds exactly one, so
#: this is a process constant rather than shared mutable state.
#:
#: It exists for ONE job: stamping an approving session onto a durable import
#: record. The alternative was threading a `telemetry=` parameter from the
#: wizard through the folder lane's orchestrator, its reviewed-import
#: deduplicator and its automatic-approval path down to `import_jobs.enqueue`
#: -- four call sites deep, where a single dropped pass-through silently nulls
#: the join and every test still passes.
_current: TelemetryContext | None = None


def current() -> TelemetryContext:
    """This process's context, or a disabled one. Never None, never raises."""
    return _current if _current is not None else null_context()


#: Origin fields are replayed into a worker's properties, so they are validated
#: on the way OUT of the job record, not trusted from it: the record is a local
#: file that survives upgrades and downgrades.
_ORIGIN_SESSION = re.compile(r"[A-Za-z0-9_-]{1,64}")


def origin_stamp() -> dict | None:
    """Who approved the work about to be persisted, or None when nobody did.

    Goes on the job RECORD, never in its `payload`: the payload's hash is the
    job's identity (`import_jobs._identity`), so an extra field there would
    give the same approval a different job id per session and defeat the
    deduplication that keeps a re-run from importing everything twice.
    """
    ctx = current()
    if not ctx.enabled:
        return None
    return {"session_id": ctx.session_id, "via": str(ctx.via), "invoked_by": str(ctx.invoked_by)}


def job_context(origin: object) -> TelemetryContext:
    """The funnel handle for a detached import worker.

    A worker is a NEW PROCESS and cannot inherit a context object, but the
    question the funnel exists to answer -- did the import this person approved
    during onboarding ever finish? -- is unanswerable unless the completion
    carries the same `session_id` the approval did. So the approving session is
    replayed off the job record.

    The gate is re-evaluated here, from the config as it is NOW: a person who
    turned telemetry off after approving an import must not have it reported
    hours later by a background process they have forgotten about.
    """
    try:
        base_url = core.effective_base_url(core.read_cli_config())
    except Exception:
        base_url = None
    ctx = TelemetryContext.start(via=Via.IMPORT_JOB, interactive=False, base_url=base_url)
    if not isinstance(origin, dict):
        return ctx
    session = origin.get("session_id")
    if isinstance(session, str) and _ORIGIN_SESSION.fullmatch(session):
        ctx.session_id = session
    via = origin.get("via")
    if via in tuple(Via):
        ctx.via = str(via)
    invoked_by = origin.get("invoked_by")
    if invoked_by in tuple(InvokedBy):
        ctx.invoked_by = str(invoked_by)
    return ctx


def identity_mode_from_config() -> str:
    """anonymous|authenticated from token presence (env or config) — cheap,
    no network. Env tokens count: a CI/agent shell exporting PROBE_TOKEN is
    authenticated everywhere else in the client and must not read as an
    anonymous install here."""
    try:
        if core.effective_token(core.read_cli_config()):
            return IdentityMode.AUTHENTICATED
    except Exception:
        pass
    return IdentityMode.ANONYMOUS


# -- outbox --------------------------------------------------------------------
# Two events from two processes, because neither process can see both halves.
#
# The drainer knows what delivery DID (delivered, dead-lettered, why it gave up)
# and reports it as it exits. But the states an operator actually has to act on
# are exactly the ones where no drainer exists: `maybe_spawn` refuses to fork
# when the journal is paused or inside its auth-block cooldown, so a credential
# that expired mid-run produces a growing queue and total telemetry silence --
# the failure this whole pair exists to make visible. The foreground banner is
# the only code that runs in that state, so the stuck report rides there.
#
# METADATA ONLY, matching the plugin hook's contract: counts, booleans, ages and
# a bounded outcome vocabulary. `last_error` is deliberately NOT sent -- it is a
# formatted exception message, and a redacted message is still free text. Its
# exception TYPE is sent instead, validated to be a bare identifier.

#: Rate-limit stamp, in the journal dir so it is per-outbox and dies with it.
_STUCK_STAMP = "telemetry-stuck.stamp"
#: A stuck outbox stays stuck: it is a level, not an edge, and every subsequent
#: `probe` command re-observes it. Six hours keeps a training loop that shells
#: out thousands of times to at most four reports a day while still bounding how
#: long a newly-wedged queue stays invisible.
STUCK_REPORT_INTERVAL_S = 6 * 3600.0


def outbox_context(base_url: str | None) -> TelemetryContext:
    """A context for outbox events, gated on the backend THIS CALLER is using.

    `base_url` is REQUIRED and must be the caller's resolved backend, because the
    two callers resolve it from different places and neither is the CLI config
    file alone:

      * the banner runs under a possible `probe --base-url ...`, which lives on
        `_conn.base_url` and never reaches the config file;
      * the drainer delivers each op to the base_url PINNED on that op, which can
        differ from the ambient context entirely.

    An earlier version resolved `core.effective_base_url(core.read_cli_config())`
    here and fell back to `None` on failure. Both halves were wrong: it read a
    backend the caller might not be using, and `None` is precisely the value
    `hosted_base_url` treats as "unset, assume hosted" -- so the failure path
    emitted to the vendor from a self-host box. FAIL CLOSED: an unknown backend
    returns a disabled context, matching `report_crash`, which already refuses to
    guess.
    """
    if not base_url:
        return null_context()
    return TelemetryContext.start(via=Via.OUTBOX, interactive=False, base_url=base_url)


def _error_kind(last_error: str | None) -> str | None:
    """The exception TYPE from a journal `last_error`, or None.

    `last_error` is `_redact(f"{type(exc).__name__}: {exc}")` -- the leading
    token is a class name, the rest is a message. Only the class name is
    metadata, and `isidentifier()` proves that is all we took: anything that
    does not parse as a bare identifier is dropped rather than guessed at.
    """
    if not isinstance(last_error, str):
        return None
    head = last_error.split(":", 1)[0].strip()
    return head if head.isidentifier() else None


def _age_hours(stamp: str | None) -> float | None:
    """Whole-ish hours since an ISO stamp; None when it will not parse."""
    if not stamp or not isinstance(stamp, str):
        return None
    try:
        parsed = fromisoformat(stamp)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    delta = (datetime.now(timezone.utc) - parsed).total_seconds()
    return round(max(delta, 0.0) / 3600.0, 2)


def emit_outbox_drained(
    *,
    base_url: str | None,
    outcome: str,  # an OutboxOutcome; defined at the producer, sdk.outbox_worker
    delivered: int,
    dead_lettered: int,
    remaining: int,
    passes: int,
    duration_s: float,
) -> None:
    """Report one finished drain episode. Never raises: the worker owns data."""
    try:
        outbox_context(base_url).emit(
            EVENT_OUTBOX_DRAINED,
            outcome=str(outcome),
            delivered=delivered,
            dead_lettered=dead_lettered,
            remaining=remaining,
            passes=passes,
            duration_s=round(duration_s, 2),
        )
    except Exception:
        pass  # observability must never become observable


#: What `emit_delivery_summary` may carry. Anything else is dropped at the door:
#: the event is counts only (plan 1.12).
DELIVERY_SUMMARY_FIELDS = frozenset(
    {
        "attempted",
        "dropped",
        "direct_sends",
        "dead_lettered",
        "dead_lettered_by_status",
        "pending",
        "oldest_pending_s",
        "auth_blocked_s",
        "final",
        "interval_s",
    }
)


def emit_delivery_summary(*, base_url: str | None, flush: bool = False, **counts) -> None:
    """Report one training process's delivery counts. Never raises; gated on
    the telemetry opt-out and the caller's backend like every outbox event.
    ``flush``: send now (the caller is exiting and the sender's own exit flush
    may already have run); waits at most the sender's flush bound."""
    try:
        props = {key: value for key, value in counts.items() if key in DELIVERY_SUMMARY_FIELDS}
        ctx = _detached_outbox_context(base_url)
        ctx.emit(EVENT_DELIVERY_SUMMARY, **props)
        if flush and ctx.enabled:
            _flush_at_exit()
    except Exception:
        pass  # observability must never become observable


def _detached_outbox_context(base_url: str | None) -> TelemetryContext:
    """`outbox_context`'s gates without making it THE process's context: this
    is sent from a daemon thread of any process, a CLI command's included,
    whose own session context must stay current."""
    if not base_url:
        return null_context()
    try:
        enabled = not core.telemetry_disabled() and core.hosted_base_url(base_url)
    except Exception:
        enabled = False
    ctx = TelemetryContext(
        session_id=uuid.uuid4().hex,
        via=Via.OUTBOX,
        invoked_by=InvokedBy.AUTOMATION,
        enabled=enabled,
    )
    if enabled:
        try:
            _ensure_sender()
        except Exception:
            ctx.enabled = False
    return ctx


def report_due(spool_dir: str | None, key: str, *, interval_s: float) -> bool:
    """Whether a report keyed on `key` is due, claiming the window when it is.

    The throttle is a stamp FILE, not an in-memory counter, and that is the whole
    point: every process-local budget in this codebase is defeated by the same
    workload, a training loop that shells out to `probe log` per step. Each
    invocation is a fresh interpreter with a fresh counter, so N commands produce
    N reports. A file on the journal dir is the only state those N processes
    share.

    Claimed with O_CREAT|O_EXCL first, so N concurrent processes that all see an
    expired stamp produce exactly ONE winner rather than N. The loser's
    `FileExistsError` is the correct answer (somebody else is reporting), not an
    error. When the stamp exists and is expired, the winner is decided by the
    utime bump instead -- still one write, and a lost race there costs one
    duplicate rather than N.

    An unwritable journal dir answers False: a queue we cannot stamp would
    otherwise report on EVERY command, which is the cost this exists to prevent.
    `None` resolves to the default journal dir -- the value `--spool-dir` carries
    when nobody passed one, which is almost every invocation.
    """
    directory = spool_dir
    if not directory:
        try:
            from ..sdk.journal import default_dir

            directory = str(default_dir())
        except Exception:
            return False
    path = os.path.join(os.path.expanduser(directory), f"telemetry-{_safe_key(key)}.stamp")
    try:
        # Never-reported: an atomic create decides the single winner.
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
        return True
    except FileExistsError:
        pass
    except OSError:
        return False
    try:
        if datetime.now(timezone.utc).timestamp() - os.stat(path).st_mtime < interval_s:
            return False
        os.utime(path, None)  # claim the new window
    except OSError:
        return False
    return True


def _safe_key(key: str) -> str:
    """A stamp-filename-safe form of a report key. The keys are hand-written
    literals, so this only has to stop a typo from escaping the directory."""
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in key)[:64]


def stuck_report_due(spool_dir: str | None, *, interval_s: float = STUCK_REPORT_INTERVAL_S) -> bool:
    """The stuck-report throttle. See :func:`report_due`."""
    return report_due(spool_dir, "stuck", interval_s=interval_s)


def stuck_status(status: dict) -> bool:
    """Whether this queue is STUCK, as opposed to merely carrying old scars.

    Deliberately NOT the banner's condition. The banner also prints for a
    dead-letter count, which is the right call for a human -- `N dead-lettered`
    is worth seeing once -- but dead letters are PERMANENT, so reusing that
    condition made a fully drained queue (`pending=0`, running, authorised) emit
    `outbox.stuck` every six hours forever because of one op that died last
    month. That is a false positive with an unbounded tail, on the event whose
    whole job is to mean "someone must act".

    Stuck is: blocked on credentials, or holding work it has stopped draining.
    The dead-letter count still RIDES the event as a property.
    """
    from probe.sdk.journal import auth_blocked_since

    if auth_blocked_since(status):
        return True
    return bool(status.get("pending")) and bool(status.get("paused"))


def emit_outbox_stuck(status: dict, *, spool_dir: str | None, base_url: str | None) -> bool:
    """Report a stuck queue, at most once per :data:`STUCK_REPORT_INTERVAL_S`.

    Takes the banner's already-read status dict rather than re-reading it: this
    runs on the every-command path, and the contract there is one stat, no
    second read.

    ORDER MATTERS, and an earlier version had it wrong in both directions. The
    gates are checked BEFORE the throttle is stamped, because stamping first
    meant `PROBE_TELEMETRY=off` still burned the six-hour window -- so the
    killswitch silently cost the fleet its next report on that queue for six
    hours after someone turned telemetry back on. And the return value is now the
    truth: it used to return True whenever the stamp was written, including when
    the context was disabled and `emit` was a silent no-op, so it claimed to have
    sent an event it never sent (and the gate tests, which only asserted "no
    record reached the sender", passed either way).
    """
    try:
        if not stuck_status(status):
            return False
        ctx = outbox_context(base_url)
        if not ctx.enabled:  # killswitch or self-host: report nothing, stamp nothing
            return False
        if not stuck_report_due(spool_dir):
            return False
        from probe.sdk.journal import auth_blocked_since

        blocked_since = auth_blocked_since(status)
        ctx.emit(
            EVENT_OUTBOX_STUCK,
            pending=status.get("pending") or 0,
            dead_lettered=status.get("failed") or 0,
            paused=bool(status.get("paused")),
            auth_blocked=bool(blocked_since),
            auth_blocked_age_hours=_age_hours(blocked_since),
            oldest_pending_age_hours=_age_hours(status.get("oldest_pending")),
            last_error_kind=_error_kind(status.get("last_error")),
        )
        return True
    except Exception:
        return False  # observability must never become observable


# -- crash reporting -----------------------------------------------------------
# The CLI and the stdio MCP are not the SDK: they run in their own process, so a
# crash costs one command rather than a training run, and there is no run to hang
# a diagnostic span on. They do already have a telemetry pipe with a killswitch,
# a self-host egress gate and identity resolution, so crashes ride that instead
# of a second vendor.
#
# The payload is built by sdk.diagnostics, so a CLI crash and an SDK crash are
# scrubbed and bounded by ONE implementation -- the frame filter that keeps
# caller code out of a report is not something to have two of.


#: Frame fields PostHog's manual-capture schema expects (docs: Manual error
#: tracking installation). `platform`/`lang` tell ingestion this is a
#: hand-rolled integration rather than one of their SDKs, and `resolved: True`
#: says the frames need no symbolication -- without it the pipeline treats them
#: as unresolved and the issue renders without a usable stack.
_FRAME_BASE = {"platform": "custom", "lang": "python", "resolved": True}


def _posthog_frames(report: dict) -> list[dict]:
    """Our frame records in PostHog's stack-frame shape.

    Caller frames stay placeholders exactly as they are in a diagnostic span
    (`sdk/diagnostics._frames`): they hold the position of the boundary and
    `in_app: False`, and nothing of the caller's.
    """
    frames: list[dict] = []
    for link in report.get("exception") or []:
        for frame in link.get("frames") or []:
            if frame.get("probe"):
                frames.append(
                    {
                        **_FRAME_BASE,
                        "filename": frame.get("file"),
                        "function": frame.get("func"),
                        "lineno": frame.get("line"),
                        "in_app": True,
                    }
                )
            else:
                frames.append({**_FRAME_BASE, "filename": "<caller>", "in_app": False})
    return frames


def _fingerprint(report: dict, exception_type: str) -> str:
    """Group by exception type plus the Probe frame that raised.

    PostHog generates a fingerprint when none is given, but its default leans on
    the exception MESSAGE -- and this payload deliberately has none, so every
    TransportError anywhere in the SDK would collapse into one issue. Keying on
    the top in-app frame separates call sites while carrying no free text.
    """
    import hashlib

    top = ""
    for link in report.get("exception") or []:
        for frame in link.get("frames") or []:
            if frame.get("probe"):
                top = f"{frame.get('file')}:{frame.get('func')}:{frame.get('line')}"
                break
        if top:
            break
    return hashlib.sha256(f"{exception_type}|{top}".encode()).hexdigest()[:32]


def _contract_safe(report: dict) -> dict:
    """The report minus every free-text field, per this module's own contract.

    Line 36 of this file: "METADATA ONLY. ids, versions, counts, booleans, enum
    outcomes. No folder paths, no error strings (exception text can embed a
    path)." That rule anticipated exactly this feature, so a crash report going
    to a VENDOR endpoint honors it rather than reinterpreting it -- even though
    the messages are scrubbed, and even though scrubbing is good.

    What survives is what the contract already allows and what grouping actually
    needs: exception TYPES, our own frames, HTTP statuses, durations, booleans.
    The full message stays available where it is not a vendor's to see -- the
    diagnostic span on the customer's own run.
    """
    safe: dict = {"schema": report.get("schema"), "environment": report.get("environment", {})}
    chain = []
    for link in report.get("exception") or []:
        entry = {"type": link.get("type"), "module": link.get("module")}
        if link.get("status") is not None:
            entry["status"] = link["status"]
        if link.get("frames_elided"):
            entry["frames_elided"] = link["frames_elided"]
        chain.append(entry)
    if chain:
        safe["exception"] = chain
    if report.get("client"):
        safe["client"] = report["client"]
    transport = []
    for hop in report.get("transport") or []:
        # `p` is one of OUR API routes, not a folder path, so it stays. `error`
        # is an error string and goes.
        transport.append(
            {k: v for k, v in hop.items() if k in ("m", "p", "ms", "status", "stalled")}
        )
    if transport:
        safe["transport"] = transport
    if report.get("degraded"):
        safe["degraded"] = report["degraded"]
    return safe


def report_crash(
    exc: BaseException,
    *,
    surface: str,
    base_url: str | None = None,
    handled: bool = False,
    site: str | None = None,
) -> None:
    """Emit one `$exception`. Never raises.

    `handled=False` (the default) is an unhandled crash, and those callers MUST
    re-raise afterwards: swallowing here would replace the traceback the operator
    is about to read with silence, which trades their diagnosis for ours.

    `handled=True` is a SWALLOWED exception -- a fail-open `except Exception`
    that recovered and continued (see `diagnostics.capture_swallowed`). It is
    reported at `warning` level so the two never mix in triage: one killed a
    process, the other is evidence that used to be deleted. It also skips the
    exit flush, because a swallow happens mid-run, possibly inside a training
    loop, and blocking there to flush is exactly the cost fail-open exists to
    avoid.

    `base_url` should be the RESOLVED one, not a CLI flag: the flag is None
    unless someone passed --base-url, so gating on it would let a self-hoster
    configured the ordinary way (config file, the wizard's sign-in) fall through to the
    hosted default and emit.
    """
    try:
        from ..sdk import diagnostics

        if diagnostics.disabled():
            return
        if base_url is None:
            try:
                base_url = core.effective_base_url(core.read_cli_config())
            except Exception:
                return  # unknown backend: fail CLOSED, never guess hosted
        report = diagnostics.build_report(exc)
        ctx = TelemetryContext.start(via=Via.NONE, interactive=False, base_url=base_url)
        if not ctx.enabled:
            return
        head = (report.get("exception") or [{}])[0]
        exception_type = head.get("type") or type(exc).__name__
        ctx.emit(
            # PostHog's Error Tracking groups on `$exception_list`, the
            # Sentry-compatible shape. `value` carries the TYPE, not the message:
            # grouping keys on type + frames, and the message is the field the
            # contract forbids.
            "$exception",
            surface=surface,
            # The swallow LOCATION. It was previously consumed only as a local
            # throttle key and never reached the wire, so every swallow site
            # arrived as an indistinguishable `surface="sdk"` report and the
            # docstring's claim that `site` is the grouping key was false.
            site=site,
            probe_report=_contract_safe(report),
            **{
                "$exception_list": [
                    {
                        "type": exception_type,
                        # The TYPE, not the message: grouping keys on type +
                        # frames, and the message is the field the contract at
                        # the top of this file forbids.
                        "value": exception_type,
                        "mechanism": {"handled": handled, "synthetic": False},
                        "stacktrace": {"type": "raw", "frames": _posthog_frames(report)},
                    }
                ],
                # Explicit, because the generated one leans on the message we
                # deliberately do not send.
                "$exception_fingerprint": (
                    f"{site}:{exception_type}" if site else _fingerprint(report, exception_type)
                ),
                "$exception_level": "error" if not handled else "warning",
            },
        )
        if handled:
            # A swallow continues; the sender's own atexit flush will carry it.
            return
        try:
            _flush_at_exit()
        except Exception:
            pass
    except Exception:
        pass  # observability must never become observable
