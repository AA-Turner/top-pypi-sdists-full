"""Ask the person at this terminal which project a run goes in, when nothing names one and no
coding agent is running it (plan T3). Lists the filing candidates (projects with runs from this
git repo first, then the most recently active: D22), takes a number or a slug, can create one, and
offers to save it as this computer's default (twin: app/projects)."""

from __future__ import annotations

import errno
import os
import sys
import time
from collections.abc import Callable, Mapping
from typing import Any, TextIO

from probe.generated.enums import ProjectKind
from probe.foundation.process_rank import LAUNCH_SCHEMES, read_env_int

#: How long each question waits for an answer, in seconds; then the run is refused as before.
PICK_TIMEOUT_S = 60.0
#: How many projects the list shows, in the server's filing order.
SHOWN_PROJECTS = 10
#: The kinds a person may give a new project, with what each is for (`probe project create --kind`).
KIND_HINTS = (
    (ProjectKind.training, "weights move"),
    (ProjectKind.evaluation, "sweeps, evals"),
    (ProjectKind.research, "papers, design"),
    (ProjectKind.general, "anything else"),
)
DEFAULT_KIND = ProjectKind.general
#: Values of `CI` that mean "not CI".
_NOT_CI = frozenset({"", "0", "false", "no"})


class _LookupFailed(Exception):
    """A typed slug could not be looked up (said already): ask again, offer no create."""


class ProjectPicker:
    """Asks for a run's project, only when a person can answer: a terminal on stdin and stderr,
    or a notebook, and never under CI or in a job of several processes. `pick()` returns the
    project row, or None when nobody can or did answer (no terminal, 60 s of silence on a
    terminal, end of input, Ctrl-C). A notebook's `input()` has no timeout: its cell shows the
    question until it is answered or interrupted."""

    def __init__(
        self,
        client: Any,
        *,
        env: Mapping[str, str] | None = None,
        stdin: TextIO | None = None,
        stderr: TextIO | None = None,
        timeout_s: float = PICK_TIMEOUT_S,
        clock: Callable[[], float] = time.monotonic,
    ):
        self.client = client
        self.env = os.environ if env is None else env
        self.stdin = sys.stdin if stdin is None else stdin
        self.stderr = sys.stderr if stderr is None else stderr
        self.timeout_s = timeout_s
        self.clock = clock

    # -- who can answer ---------------------------------------------------------
    def can_ask(self) -> bool:
        if (self.env.get("CI") or "").strip().lower() not in _NOT_CI:
            return False
        if _is_many_processes(self.env):
            return False  # torchrun / accelerate ranks would all ask on one terminal
        if self._is_notebook():
            return True
        # A background job (`python train.py &`) keeps the terminal but cannot read it: a read
        # stops the job (SIGTTIN) until `fg`.
        return _is_terminal(self.stdin) and _is_terminal(self.stderr) and _is_foreground(self.stdin)

    def _is_notebook(self) -> bool:
        """An IPython kernel (Jupyter): `input()` reaches the person through the front end."""
        ipython = sys.modules.get("IPython")
        try:
            shell = ipython.get_ipython() if ipython is not None else None
        except Exception:  # noqa: BLE001 -- an IPython that cannot answer is no notebook
            return False
        return shell is not None and getattr(shell, "kernel", None) is not None

    # -- the questions ------------------------------------------------------------
    def pick(self) -> dict | None:
        """The run's project, or None when nobody can or did answer."""
        if not self.can_ask():
            return None
        try:
            return self._pick()
        except KeyboardInterrupt:
            self._say("")
            return None

    def _pick(self) -> dict | None:
        projects = self._list_recent_projects()
        self._say("probe: this run needs a project.")
        for number, row in enumerate(projects, 1):
            self._say(f"  {number}) {row.get('slug')}")
        limit = "" if self._is_notebook() else f" ({int(self.timeout_s)} s)"
        prompt = (f"Pick a number or type a project slug{limit}: " if projects
                  else f"Type a project slug{limit}: ")
        while True:
            answer = self._ask(prompt)
            if answer is None:
                return None
            try:
                row = self._find_project(answer, projects) if answer else None
            except _LookupFailed:
                continue
            if row is None and answer:
                row = self._offer_create(answer)
            if row is not None:
                self._offer_default(row)
                # A saved default is read only under FROM_ENV (R22): the script's own line is what sticks.
                self._say(f'probe: to skip this question, pass project="{row.get("slug")}" to probe.init()')
                return row

    def _list_recent_projects(self) -> list[dict]:
        """The projects this run most likely goes in (`fetch_filing_candidates`): runs from this
        folder's git repo first, then the most recently active. A failed list is an empty one:
        the person can still type a slug."""
        from ....capture.code.git_remote import load_origin_url

        try:
            found = self.client.fetch_filing_candidates(remote=load_origin_url(os.getcwd()))
        except Exception:  # noqa: BLE001 -- the prompt still works without the list
            return []
        rows = found.get("projects") if isinstance(found, dict) else None
        return [row for row in (rows or []) if isinstance(row, dict) and row.get("slug")][:SHOWN_PROJECTS]

    def _find_project(self, answer: str, projects: list[dict]) -> dict | None:
        """The listed project numbered `answer`, else the project slugged `answer`."""
        if answer.isdigit() and 1 <= int(answer) <= len(projects):
            return projects[int(answer) - 1]
        for row in projects:
            if row.get("slug") == answer:
                return row
        from .... import errors

        try:
            return self.client.resolve_project(answer)
        except errors.RosError as exc:
            self._say(f"probe: could not look up {answer}: {exc}")
            raise _LookupFailed from exc

    def _offer_create(self, slug: str) -> dict | None:
        """`slug` names no project: create it if the person says so, asking its kind."""
        if not self._ask_yes(f'No project "{slug}". Create it? [y/N] ', default=False):
            return None
        kinds = ", ".join(f"{kind.value} ({hint})" for kind, hint in KIND_HINTS)
        while True:
            answer = self._ask(f"Kind: {kinds} [{DEFAULT_KIND.value}]: ")
            if answer is None:
                return None
            kind = answer or DEFAULT_KIND.value
            if kind in {k.value for k, _ in KIND_HINTS}:
                break
            self._say(f"probe: not a kind: {kind}")
        from .... import errors

        try:
            return self.client.create_project(slug, kind=kind)
        except errors.RosError as exc:
            self._say(f"probe: could not create {slug}: {exc}")
            return None

    def _offer_default(self, row: dict) -> None:
        """Offer to make `row` this computer's default (what `probe project use` saves)."""
        if not self._ask_yes("Save as this computer's default? [Y/n] ", default=True):
            return
        from ....settings.default_project import save_default_project

        try:
            saved = save_default_project(self.client, row, what="saving it as this computer's default")
        except Exception as exc:  # noqa: BLE001 -- the run still opens in the project picked
            self._say(f"probe: not saved as this computer's default: {exc}")
            return
        if saved.refused:
            self._say(f"probe: not saved as this computer's default: {saved.refused}")
            return
        self._say(f"probe: {row.get('slug')} is this computer's default now (`probe project use` changes it)")

    # -- reading an answer ----------------------------------------------------------
    def _ask_yes(self, prompt: str, *, default: bool) -> bool:
        answer = self._ask(prompt)
        if answer is None:
            return False
        if not answer:
            return default
        return answer.lower() in ("y", "yes")

    def _ask(self, prompt: str) -> str | None:
        """One line from the person, stripped; None on silence past the timeout or end of input."""
        if self._is_notebook():
            try:
                return input(prompt).strip()
            except Exception:  # noqa: BLE001 -- EOF, or a kernel with no front end (StdinNotImplementedError)
                return None
        self.stderr.write(prompt)
        self.stderr.flush()
        line = _read_line(self.stdin, self.timeout_s)
        if line is None:
            self._say("")
            self._say(f"probe: no answer in {int(self.timeout_s)} s")
            return None
        if line == "":
            self._say("")
            return None  # end of input
        return line.strip()

    def _say(self, line: str) -> None:
        try:
            print(line, file=self.stderr, flush=True)
        except (OSError, ValueError):
            pass


def _is_terminal(stream: TextIO | None) -> bool:
    try:
        return stream is not None and stream.isatty()
    except (AttributeError, ValueError, OSError):
        return False


def _is_foreground(stream: TextIO) -> bool:
    """Reading `stream` will not stop this process: it is not our controlling terminal (ENOTTY),
    or our process group is its foreground one. A console without job control always is."""
    if not hasattr(os, "tcgetpgrp"):
        return True
    try:
        return os.tcgetpgrp(stream.fileno()) == os.getpgrp()
    except OSError as exc:
        return exc.errno == errno.ENOTTY
    except (AttributeError, ValueError):
        return True  # no descriptor to ask about: as before


def _is_many_processes(env: Mapping[str, str]) -> bool:
    """A distributed launch (torchrun, srun, mpirun: a world size > 1): every rank would ask on
    the same terminal."""
    return any((read_env_int(env, scheme.size_var) or 1) > 1 for scheme in LAUNCH_SCHEMES)


def _read_line(stream: TextIO, timeout_s: float) -> str | None:
    """`stream.readline()` within `timeout_s`: the line ("" at end of input), or None on silence.
    POSIX waits with `select`, which reads nothing more; a Windows console is polled key by key
    (`_read_console_line`), so no reader is left behind to take a later answer."""
    if sys.platform == "win32":
        return _read_console_line(timeout_s)
    import select

    try:
        ready, _, _ = select.select([stream], [], [], timeout_s)
    except (OSError, ValueError, TypeError):
        return None  # a stream `select` cannot watch: nobody can be asked on it
    return stream.readline() if ready else None


def _read_console_line(timeout_s: float, clock: Callable[[], float] = time.monotonic) -> str | None:
    """One line typed at the Windows console within `timeout_s`, echoed as typed: the line, ""
    for Ctrl-Z, or None on silence. Ctrl-C raises `KeyboardInterrupt`, as `input()` does."""
    import msvcrt

    deadline = clock() + timeout_s
    typed: list[str] = []
    while clock() < deadline:
        while msvcrt.kbhit():
            char = msvcrt.getwche()
            if char in ("\r", "\n"):
                msvcrt.putwch("\n")
                return "".join(typed) + "\n"
            if char == "\x1a":
                return ""
            if char == "\x03":
                raise KeyboardInterrupt
            if char == "\b":
                typed = typed[:-1]
                continue
            typed.append(char)
        time.sleep(0.05)
    return None
