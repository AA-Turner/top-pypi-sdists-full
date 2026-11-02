"""the run's vocabulary: options, phases, why it stopped, the Run record, its step lines."""

from __future__ import annotations
import time
from dataclasses import dataclass, field

from probe.foundation.compat.compat import StrEnum


class Phase(StrEnum):
    PLANNED = "planned"
    STOPPING = "stopping"
    DRAINING = "draining"
    SERVER = "server"
    INTEGRATIONS = "integrations"
    STATE = "state"
    FINISHING = "finishing"


PHASES = tuple(Phase)


class UnsentChoice(StrEnum):
    DELETE = "delete"
    BACKUP = "backup"
    CANCEL = "cancel"


@dataclass
class Options:
    yes: bool = False
    force: bool = False
    offline: bool = False
    discard_unsent: bool = False
    #: D1 without a question: save the backup file, then go on (`--backup-unsent`).
    backup_unsent: bool = False
    json: bool = False
    #: A person can answer questions here (a TTY, no --yes).
    interactive: bool = False
    #: Finishing an interrupted uninstall for an installer that goes on after it
    #: (`finish_interrupted`): no result rows of its own in the installer's
    #: events, and the finisher runs in this process (no exec), keeping the env
    #: this process runs from.
    embedded: bool = False


class Reason(StrEnum):
    """Why a run ended with exit 2 or 1: the `--json` result's `reason.code`
    (`reason_record`), which the desktop app maps to its buttons."""

    UNSENT_RESEARCH = "unsent_research"  # D1: delete anyway / save a backup / cancel
    LIVE_USERS = "live_users"  # D2: stop them (--force) / cancel
    IN_SESSION = "in_session"  # run from inside a recorded agent session
    OFFLINE = "offline"  # remove from this computer only (--offline) / cancel
    BUSY = "busy"  # another Probe update or uninstall holds the install lock
    PARTIAL = "partial"  # past the point of no return: `resume` finishes it
    INTERRUPTED = "interrupted"  # a signal before "server": called off
    CANCELLED = "cancelled"  # a person said no (interactive runs only)
    CONFIRM = "confirm"  # no terminal to confirm in, and no --yes


class Stop(Exception):
    """End the run with `code` after `message` (a refusal or a partial run),
    for `reason` (its `detail` rides along in the `--json` result)."""

    def __init__(self, code: int, message: str, reason: Reason | None = None, detail: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.reason = reason or (Reason.PARTIAL if code == EXIT_PARTIAL else None)
        self.detail = dict(detail or {})


@dataclass
class Run:
    options: Options
    plan: dict = field(default_factory=dict)
    lock_fd: int | None = None
    telemetry: object | None = None
    resumed: bool = False
    #: What the current phase has to say, printed as the phase ends (or stops).
    out: list = field(default_factory=list)
    #: `! ` lines so far: a removal that left something behind is not a clean one.
    warnings: int = 0
    started_at: float = field(default_factory=time.monotonic)
    #: The coding agents with a trace of Probe, as found before anything changed.
    agents: list = field(default_factory=list)
    #: What the stop phase stopped, said if the run is called off before "server".
    stopped: list = field(default_factory=list)
    #: THIS run wrote the barrier / the plan: a call-off undoes only what it wrote.
    wrote_barrier: bool = False
    wrote_plan: bool = False
    #: The phase this run is in (for a resumed run, from where it resumed).
    at: Phase | None = None
    #: What the drain step found still unsent (the refusal's advice reads it).
    unsent: Unsent | None = None


# -- output ------------------------------------------------------------------------------


def _say(text: str) -> None:
    print(text, flush=True)


def _step(name, status, message: str = "") -> None:
    from probe.core import events

    events.step(name, status, message)


def _lines(lines: list[str]) -> None:
    for line in lines:
        _say(f"  {line}" if not line.startswith("  ") else line)
from probe.cli.install.uninstall.phases.draining import Unsent  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import EXIT_PARTIAL  # noqa: E402 -- pieces need each other; the front door loads this one first
