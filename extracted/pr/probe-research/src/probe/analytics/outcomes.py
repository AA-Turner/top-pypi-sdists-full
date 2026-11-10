"""the closed value sets event properties take (outcomes, reasons, entry points)."""

from __future__ import annotations
from probe.foundation.compat.compat import StrEnum


class IdentityMode(StrEnum):
    ANONYMOUS = "anonymous"
    AUTHENTICATED = "authenticated"


class Via(StrEnum):
    WIZARD = "wizard"
    COMMAND = "command"
    OUTBOX = "outbox"  # the detached drainer and the every-command banner
    #: An import worker whose job has no approver on record (recovered, or enqueued with telemetry
    #: off); with one, it replays the approver's `via`, so approval and completion share a funnel.
    IMPORT_JOB = "import_job"
    #: The daemon's worker (`probe.daemon.worker.alerts`).
    DAEMON = "daemon"
    #: The Probe service's automatic diagnostic reports (`probe.shared.reports`).
    SERVICE = "service"
    NONE = "none"  # null_context — never reaches the wire


class DiscardReason(StrEnum):
    """`outbox.discarded`'s `reason`: what set the writes aside."""

    HELD = "held"  # `probe outbox discard --held`
    CREDENTIAL = "credential"  # `--held --credential <fp>`: a named credential's writes too
    DEAD_LETTERS = "dead_letters"  # `probe outbox discard [op]`
    #: Earlier discards moved from a credential queue to the root, out of cleanup's reach. Nothing
    #: lost; reported once with their dates, so a machine shows what it keeps.
    RELOCATED = "relocated"
    #: The drain set aside writes the server refused because a newer attempt of
    #: their run took it over (a past write epoch): never deliverable (T24).
    SUPERSEDED = "superseded"
    #: `probe doctor --fix` dropped dead letters no retry can deliver: a
    #: superseded attempt's, or a run the server says does not exist (T24).
    UNRECOVERABLE = "unrecoverable"


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
    #: The root could not be listed. Kept apart from EMPTY_FOLDER: "nothing here" and "could not
    #: look" are the two answers this flow exists to separate.
    UNREADABLE_ROOT = "unreadable_root"
    ALREADY_IMPORTED = "already_imported"
    CREDENTIALS_FAILED = "credentials_failed"
    NO_PLAN = "no_plan"
    #: Historical (a classifier path the walk lacked); not raised since the classifier selects
    #: through `probe-backfill-plan` (2026-10-25). Kept so old events still read.
    UNTRUSTED_CLASSIFICATION = "untrusted_classification"
    #: Finished, but a failed classifier session left files unclassified; they
    #: stay `new` and the next run classifies only them.
    PARTIAL_CLASSIFICATION = "partial_classification"
    PROJECT_CREATE_FAILED = "project_create_failed"
    #: Handed to a background job (`job_id` rides along): its `import_job.finished` says how it ended.
    HANDED_OFF = "handed_off"
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
    #: Stopped on purpose from the import's detail screen. Not INTERRUPTED (a laptop closing): same
    #: stopped worker, opposite reading; without this a decision would be filed as an accident.
    CANCELED = "canceled"
    #: The worker never owned the job (a failed spawn, or children not reclaimed). Not FAILED:
    #: nothing was imported or even attempted.
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
    #: The server said the daemon is not open to this team (the value predates
    #: every plan getting the daemon; kept so the funnel's history still counts).
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
    #: Refused or stopped partway (`probe uninstall`'s `Stop`): its own `reason` rides along.
    STOPPED = "stopped"


class AgentRunOutcome(StrEnum):
    """How an agent's install command ended (`sign-in --wait`, `install`), from its `reason`."""

    SUCCESS = "success"
    #: Exit 75: the agent runs the same command again (waiting_for_approval, downloading, setup_busy, ...).
    RUN_AGAIN = "run_again"
    FAILED = "failed"


class InstallSettings(StrEnum):
    """`agent_install.configured`'s `settings`: what the person answered "Install settings" with."""

    RECOMMENDED = "recommended"
    #: Let me pick: who files the work and new chats' default, each given.
    PICKED = "picked"
    #: Neither: a re-run or a switch that keeps this computer's own settings.
    KEPT = "kept"


class SwitchTrigger(StrEnum):
    """`session.switched`'s `trigger`: what moved the switch (probe auto mode)."""

    #: The agent ran the command after the person asked (`--directed`: `probe session state`, `session default`, ...).
    AGENT = "agent"
    #: The agent moved an auto chat's switch on its own, by the work (`probe session state` in auto mode).
    AUTO = "auto"
    #: A run launched through Probe turned an auto chat on (`probe exec`, `run start`, the SDK).
    RUN_LAUNCH = "run_launch"


class RepairOutcome(StrEnum):
    """`repair.finished`'s `outcome`: `probe repair`'s exit 0, 1 and 2."""

    COMPLETE = "complete"
    INCOMPLETE = "incomplete"
    REFUSED = "refused"


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


class PrivateUvOutcome(StrEnum):
    """`updates.private_uv`'s `outcome`: an update found no `uv`, or only an older copy of Probe's
    own, and tried to install the pinned one."""

    INSTALLED = "installed"
    FAILED = "failed"


class PrivateUvReason(StrEnum):
    """`updates.private_uv`'s `reason` when it failed: a closed set, never a host, path or URL
    (an index URL can hold a token in its path). The detail stays in the machine's update.log."""

    UNSUPPORTED_MACHINE = "unsupported_machine"
    NO_WHEEL = "no_wheel"
    NO_HASH = "no_hash"
    UNPINNED = "unpinned"
    #: The index lists a sha256 that is not pypi.org's (a mirror that rebuilt the wheel).
    INDEX_HASH_NOT_PINNED = "index_hash_not_pinned"
    #: The bytes downloaded are not the ones the index and pypi.org promised.
    DOWNLOAD_HASH_MISMATCH = "download_hash_mismatch"
    #: The index URL, a file URL it lists, or a redirect is not an https URL with a valid host
    #: (plain http only to this machine).
    BAD_INDEX_URL = "bad_index_url"
    TOO_LARGE = "too_large"
    HTTP_4XX = "http_4xx"
    HTTP_5XX = "http_5xx"
    NETWORK = "network"
    EXTRACT_FAILED = "extract_failed"
    BAD_VERSION = "bad_version"
    TOML_UNREADABLE = "toml_unreadable"
    OTHER = "other"
