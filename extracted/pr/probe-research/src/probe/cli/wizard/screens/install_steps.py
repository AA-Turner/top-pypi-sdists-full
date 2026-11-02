"""the install's numbered steps and its one shared progress bar across every agent's apply."""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from collections.abc import Callable, Iterable, Mapping, Sequence
from probe.cli.wizard.state.state import Capability


# -- the install flow, as steps ---------------------------------------------
#
# Before installation, choose the coding agents (only when the machine offers
# a choice), then this device's defaults (who records, and what new sessions
# do), then review everything that will be set up and confirm. The import
# offer follows the completed installation. There is no capability picker — see
# the module docstring for why it is gone and what carries the disclosure now.
# The `‹ Back` / `Next ›` band and the shared key rule (`_wire_picker`) remain
# for the screens that still take input.


#: The install flow, including the work after confirmation. The header counts
#: from this, so adding a step renumbers every screen without another edit.
INSTALL_STEPS: tuple[str, ...] = (
    "Coding agents", "Defaults", "Review & install", "Installing", "Import existing work"
)

#: The step values by name, so a screen names its own position rather than
#: carrying a magic number.
#:
#: DERIVED from INSTALL_STEPS, not written beside it. As bare literals
#: these claimed to prevent exactly the desync they enabled: reordering the
#: tuple remapped every step's NAME while the constants kept their old NUMBERS,
#: so `step_title` and `step_name` would disagree about which screen you were
#: on and nothing would raise. Now a reorder moves both together, and a rename
#: raises here at import rather than mislabelling a screen at runtime.
STEP_AGENTS = INSTALL_STEPS.index("Coding agents") + 1
STEP_DEFAULTS = INSTALL_STEPS.index("Defaults") + 1
STEP_IMPORTS = INSTALL_STEPS.index("Import existing work") + 1
STEP_CONFIRM = INSTALL_STEPS.index("Review & install") + 1
STEP_INSTALL = INSTALL_STEPS.index("Installing") + 1


def step_title(step: int, *, agent_screen_shown: bool = True) -> str:
    """Number only stages this install actually visits."""
    from probe.cli.wizard import terminal as tui

    skipped = 0 if agent_screen_shown else 1
    label = "Install Probe Research"
    detail = f"Step {step - skipped} of {len(INSTALL_STEPS) - skipped}"
    width = max(1, min(tui.CONTENT_WIDTH, tui.columns() - tui.left_pad() - 1))
    if len(label) + len(detail) + 1 > width:
        label = "Install Probe"
    return f"{label:<{max(len(label) + 1, width - len(detail))}}{detail}"


def install_progress(
    step: int,
    *,
    agent_screen_shown: bool = True,
    fraction: float = 0.0,
) -> str:
    """Completed stages plus the fraction of the current stage resolved."""
    from probe.cli.wizard import terminal as tui

    skipped = 0 if agent_screen_shown else 1
    return tui.progress_bar(
        (step - skipped - 1 + max(0.0, min(1.0, fraction))) / (len(INSTALL_STEPS) - skipped),
        width=tui.CONTENT_WIDTH,
    )


def install_header(
    step: int, *, agent_screen_shown: bool = True, fraction: float = 0.0,
) -> list[str]:
    return [
        step_title(step, agent_screen_shown=agent_screen_shown),
        install_progress(step, agent_screen_shown=agent_screen_shown, fraction=fraction),
    ]


def install_apply_header(
    *, agent_screen_shown: bool, agent_index: int, agent_count: int, agent_source: str
) -> Callable[[float], list[str]]:
    """Keep one install bar advancing across sequential coding-agent applies.
    Which agent is installing, and how far the whole run is, is the
    `InstallRun`'s heading and bar under it."""

    def header(fraction: float) -> list[str]:
        return [
            step_title(STEP_INSTALL, agent_screen_shown=agent_screen_shown),
            install_progress(
                STEP_INSTALL,
                agent_screen_shown=agent_screen_shown,
                fraction=(agent_index + fraction) / agent_count,
            ),
        ]

    return header


#: A marketplace refresh or a plugin install (a git fetch, an agent CLI's own
#: install: seconds each) against one step on an agent's screen after it (a
#: file written, an answer taken: milliseconds), for `InstallRun`'s bar.
BATCH_UNIT_WEIGHT = 4


class InstallRun:
    """One bar, with its percentage, for an install of every coding agent in
    the run, instead of each agent's screen starting its own from empty.

    Each agent's share is its batch units (its marketplace refresh and plugin
    installs, done for every agent inside the first agent's refresh step:
    `marketplace_refreshes`), weighted `BATCH_UNIT_WEIGHT`, plus the steps on
    its own screen; a screen not open yet counts the steps it is expected to
    have. An agent whose screen finished counts whole. Main thread only: the
    batch reports from the thread that waits on it (`_refresh_together`)."""

    def __init__(
        self,
        sources: Sequence[str],
        installs: Mapping[str, Sequence[tuple[Capability, str]]] | None = None,
        *,
        expected: Mapping[str, int] | None = None,
    ) -> None:
        installs = installs or {}
        self._sources = list(sources)
        self._batch = {s: 1 + len(installs[s]) if installs.get(s) else 0 for s in self._sources}
        self._batch_done = dict.fromkeys(self._sources, 0)
        self._batch_started: set[str] = set()
        # The steps a screen not open yet is expected to list: its plan (from
        # `expected`) and its refresh, else the batch's units and two more.
        self._expected = {
            s: (expected[s] + bool(self._batch[s])) if expected is not None and s in expected
            else self._batch[s] + 2 if self._batch[s] else 4
            for s in self._sources
        }
        #: Each opened screen's (fraction done, steps).
        self._screens: dict[str, tuple[float, int]] = {}
        self._render: Callable[[], None] | None = None
        #: The run's fraction as last shown: a screen listing more steps than
        #: expected must not move the bar back.
        self._shown = 0.0

    def watch(self, render: Callable[[], None]) -> None:
        """Redraw with `render` when the batch moves (the open screen's)."""
        self._render = render

    def batch_started(self, sources: Iterable[str]) -> None:
        """The batch's report: these agents' refreshes began, all at once."""
        self._batch_started.update(source for source in sources if source in self._batch)
        self._redraw()

    def batch_progress(self, source: str, units: int) -> None:
        """The batch's report: `units` more of `source`'s refresh and installs
        finished."""
        if source not in self._batch:
            return
        self._batch_done[source] = min(self._batch[source], self._batch_done[source] + units)
        self._redraw()

    def _redraw(self) -> None:
        if self._render is not None:
            self._render()

    def for_agent(self, source: str) -> Callable[[float, int], tuple[str, float]]:
        """`tui.Progress`'s `run` for `source`'s screen."""

        def run(fraction: float, steps: int) -> tuple[str, float]:
            self._screens[source] = (fraction, steps)
            return self._heading(source), self.fraction()

        return run

    def finished(self, source: str) -> None:
        """`source`'s turn is over, whether or not it opened a screen (one
        already set up opens none)."""
        if source in self._batch:
            self._screens[source] = (1.0, self._screens.get(source, (0.0, self._expected[source]))[1])

    def fraction(self) -> float:
        done = total = 0.0
        for source in self._sources:
            batch = self._batch[source] * BATCH_UNIT_WEIGHT
            fraction, steps = self._screens.get(source, (0.0, self._expected[source]))
            whole = fraction >= 1
            done += (batch if whole else self._batch_done[source] * BATCH_UNIT_WEIGHT) + fraction * steps
            total += batch + steps
        self._shown = max(self._shown, done / total if total else 1.0)
        return self._shown

    def _heading(self, source: str) -> str:
        installing = [
            s for s in self._sources if s in self._batch_started and self._batch_done[s] < self._batch[s]
        ]
        if installing:
            # The first agent's refresh step is every marketplace agent's work.
            return f"Installing plugins for {spoken_list([agent_label(s) for s in installing])}"
        if len(self._sources) == 1:
            return f"Installing for {agent_label(source)}"
        index = self._sources.index(source) + 1 if source in self._sources else 1
        return f"Installing for {agent_label(source)} ({index} of {len(self._sources)})"


_install_run: ContextVar[InstallRun | None] = ContextVar("probe_install_run", default=None)


@contextlib.contextmanager
def install_run(
    sources: Sequence[str],
    installs: Mapping[str, Sequence[tuple[Capability, str]]] | None = None,
    *,
    expected: Mapping[str, int] | None = None,
):
    """In this block, every agent's install screen shares one `InstallRun`."""
    token = _install_run.set(InstallRun(sources, installs, expected=expected))
    try:
        yield _install_run.get()
    finally:
        _install_run.reset(token)


def current_install_run() -> InstallRun | None:
    return _install_run.get()


def step_name(step: int) -> str:
    """What this step is about, for the rule under the nav band."""
    return INSTALL_STEPS[step - 1]
from probe.cli.wizard.agents import agent_label, spoken_list  # noqa: E402 -- pieces need each other; the front door loads this one first
