"""`probe wizard` — the setup wizard: an install that guides, a menu that manages.

TWO FRONT DOORS, ON PURPOSE. `probe install` (what the install page advertises
as `npx probe-research install`) walks a fresh user straight through a guided
install: pick the coding agents when there is a choice, review the setup, watch
it apply, then choose any existing work to import.
`probe wizard` signs in before opening the manager menu — update, uninstall,
import, account, settings, diagnose. That sign-in prepares the install credentials
while leaving new session capture off until the user confirms installation.

THE INSTALL IS ALWAYS COMPLETE. The interactive capability picker is gone, and
its removal is deliberate: a machine with tracking but no capture (or the other
way round) behaves like a broken product, and the people who ended up with one
rarely chose it — they navigated into it. What replaced the picker as the
consent surface for session capture (which ships every prompt, file body and
tool result off the machine) is a DISCLOSURE-GATE: the confirm screen names
what capture sends and where, on a real 80x24 screen, before the confirming
keystroke — see `run_confirm_install` and its render test — and the browser
approval is where the grant is actually made, by name. Refusal did not shrink:
Ctrl-C before `Install ›` configures nothing and `--no-capture` still exists
for scripts. Afterwards Probe comes off WHOLE, through Uninstall: the Settings
screen used to turn tracking, capture and the instruction rules off one at a
time, which is how a device ended up running the half a product this paragraph
opens with. It keeps automatic updates and image-upload preferences. Research plan review
is a skill shipped with every agent profile and always routed by the Probe block.

The flag path is the CONTRACT and the screens are a front end over it (see
`resolve_selection` for the truth table). CI, piped stdin and dumb terminals all
take the flag path, and none of them may hang waiting for a keypress. The
interactive Install action alone is FORCE-ON — install means install, disclosed
on screen first — while an omitted flag on a scripted re-run still PRESERVES,
so no automation can re-enable a refusal behind someone's back.
"""

from __future__ import annotations

import contextlib
import threading
from concurrent.futures import FIRST_COMPLETED, Future
from concurrent.futures import wait as wait_for_futures
import contextvars
from contextvars import ContextVar
import json
import re
import os
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from probe._compat import StrEnum
from pathlib import Path
from urllib.parse import urlparse

from probe.cli import (
    agent_rules,
    autoupdate,
    claude_cli,
    codex_config,
    pi_config,
    plugin_cli,
    reasoning_summaries,
    root_skills,
)
from probe.cli.capabilities import (
    CODEX_MCP_NAME,
    CODEX_TAP_PLUGIN_NAME,
    DAEMON_PLUGIN_NAME,
    LEGACY_CODEX_TAP_PLUGIN_ID,
    MARKETPLACE,
    MARKETPLACE_REPO,
    TAP_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME,
    Capabilities,
    Capability,
    McpState,
    TokenSource,
    agent_source,
    agent_target,
    capture_token_sources,
    tap_plugin_dir,
    tracking_plugin_name,
)
from probe.cli.tui import CONTENT_WIDTH
from probe.cli.versions import VersionStatus
from probe.cli.versions import overall as overall_version_status
from probe.cli.capture import AWAITING_CONFIRMATION, OffMode, clear_killswitch, turn_off

#: How long the whole apply phase may spend before it stops STARTING new work.
#: Not a kill switch: a `claude plugin install` cut off mid-write is how a
#: plugin cache gets corrupted, so an in-flight step always runs to its own
#: timeout. This only refuses to begin the next one.
PHASE_BUDGET_S = 300.0

#: What an omitted flag means on a FRESH machine (nothing configured yet).
#:
#: EVERYTHING ON, capture included. This reverses the original default and the
#: reversal is deliberate, so the reasoning it replaces is recorded here rather
#: than deleted: capture used to default OFF because opting someone into
#: transcript egress by omission was judged the consent failure the menu exists
#: to prevent.
#:
#: What now carries that weight instead is the menu itself. Capture is a TICKED,
#: LABELLED row that says what it sends and where -- "Sends this device's Claude
#: Code sessions to your team's search" -- drawn on screen before the first
#: keystroke, with the cursor on a capability rather than on the way out, and
#: one keystroke unticks it. The grant is on screen and refusable; it is no
#: longer inferred from silence.
#:
#: That used to be stated as an ORDERING -- capture sat above the Next row, so
#: it was passed over on the way there -- and the ordering stopped being true
#: when the nav band moved to the top of the step. The ordering was only ever a
#: proxy for "it is on screen", which is now asserted directly, on a real
#: 80x24 screen: see `test_step_two_shows_the_capture_grant_on_an_80x24_screen`.
#:
#: The `--yes` path has NO screen, so it is the one that changed most: a
#: scripted `probe wizard --yes` on a fresh box now enables capture where it
#: previously would not. Anyone automating an install who does not want that
#: passes `--no-capture`, and a RE-RUN still PRESERVES rather than defaults
#: (see resolve_selection), so this can never switch capture on behind someone
#: who already turned it off.
FRESH_DEFAULTS: dict[Capability, bool] = {
    Capability.TRACKING: True,
    Capability.CAPTURE: True,
    Capability.AUTO_UPDATE: True,
    Capability.AGENT_RULES: True,
}

#: Display name per capture source. The COMPLETE set this wizard knows about
#: for naming purposes (messages, confirmations, per-source copy) -- NOT the
#: set step 1 offers to auto-detect, which is `detectable_sources()` below
#: (a live PATH/marketplace check, not a fixed tuple), and NOT the set
#: `install_plugin`/`uninstall_plugin` know how to install something for,
#: which is `INSTALLABLE_AGENT_SOURCES`. Conflating
#: the display-name set with either is exactly how the confirm-screen label
#: at the bottom of `authorize()` used to name every non-codex capture source
#: "Claude Code": a two-way ternary is silently correct only while there are
#: exactly two sources, and pi's addition is what made that stop being true.
#: Look a source up here (via `agent_label`) instead of adding another branch.
def _installable_rows():
    from probe.harness import get_registry

    return get_registry().installable()


AGENT_LABELS = {h.id: h.label for h in _installable_rows()}


def agent_logo(source: str) -> bytes | None:
    """The agent's logo as the PNG a terminal draws in the device summary
    (Richard 2026-10-06: "actually get the correct icons", in "this circular
    colored background style"): its brand mark in white on a circle of its
    brand colour, rendered by `agent/tools/render_harness_icons.py` into
    `probe/cli/icons/<registry icon stem>.png`."""
    from probe.harness import get_registry

    harness = get_registry().find(source)
    if harness is None or not harness.icon:
        return None
    path = Path(__file__).parent / "icons" / f"{Path(harness.icon).stem}.png"
    return path.read_bytes() if path.is_file() else None

#: The sources that install through a plugin MARKETPLACE (`plugin_cli.py`'s
#: `install`/`marketplace update`/`marketplace add`) rather than pi's
#: settings.json `packages` entry. NOT "the sources step 1 offers" any more --
#: that used to be true, on the theory that "pi has no CLI for it to find". It
#: was never actually true: pi IS a binary on PATH (`shutil.which("pi")`
#: resolves it exactly like `claude`/`codex`) -- what pi lacks is a
#: *marketplace*, and that is what this constant actually gates now: the
#: refresh step (`refresh_marketplace`) and the degraded-screen filter
#: (`main.py`'s `plugin_promising_sources`), both of which only mean something
#: for a source with a marketplace behind it. The step-1 picker's row set
#: comes from `detectable_sources()` below, which DOES include pi when its
#: binary is found -- see that function's docstring for the history this one
#: used to carry.
MARKETPLACE_AGENT_SOURCES: tuple[str, ...] = tuple(h.id for h in _installable_rows() if h.family == "hook-plugin")

#: Every source `install_plugin`/`uninstall_plugin`/`apply_capture` know how
#: to install or remove something for -- but not through one shared
#: mechanism. claude_code and codex go through their own marketplace
#: commands (`plugin_cli.py`, `claude_cli.py`, `codex_config.py`); pi has no
#: marketplace at all, so it goes through `pi_config`'s settings.json
#: `packages` array entry instead -- ONE entry that installs pi's extension,
#: skills, and MCP manifest together (see
#: `agent/plugins/probe-research-pi/README.md`, "Route A"). This replaces
#: the old manual `~/.pi/agent/extensions/` symlink install (now retired via
#: `migrate_legacy_symlink` on the packages-entry install). The entry is a
#: local checkout path for a plugin developer and the PUBLIC MIRROR git source
#: (`git:github.com/prbe-ai/research-os-agent`) for everyone else -- see
#: `pi_config.resolve_install_source`. Not npm: the mirror repo is the channel
#: Claude and Codex already install from, and its root `package.json` carries
#: a `pi` manifest, so one mirror push releases all three clients.
#: Because pi's install is one package covering every capability, not one
#: plugin per capability, `install_plugin`'s `name` argument is ignored on
#: pi's branch: `apply_tracking`'s and `apply_capture`'s calls both land on
#: the same idempotent write. Pairing a pi device's capture credential (see
#: `authorize`) does not depend on this tuple; it is keyed off
#: `capture_sources`/`captures`, not this list. NOT the set step 1's picker
#: offers -- see `MARKETPLACE_AGENT_SOURCES` above for that narrower one.
INSTALLABLE_AGENT_SOURCES: tuple[str, ...] = tuple(h.id for h in _installable_rows())


#: The pi `--help` "coding" sniff, MOVED to `pi_config` and re-exported here
#: under its original name so every caller and test that says
#: `setup.pi_binary_available` -- including the autouse fixture that pins pi
#: detection off for the whole suite -- keeps working. It moved because
#: `backfill.which_agent` needs the same sniff to tell a real pi from a
#: two-letter impostor, and backfill cannot import this module (this one
#: reaches into backfill). `pi_config` imports neither, so it is where a
#: function both need can live. Read that docstring for the impostor-guard
#: rationale.
pi_binary_available = pi_config.pi_binary_available


def detectable_sources(*, sniff: bool = True) -> tuple[str, ...]:
    """Every `INSTALLABLE_AGENT_SOURCES` member actually found on this
    machine, right now -- claude_code/codex via `plugin_cli.available`
    (their marketplace CLI), pi via `pi_binary_available` (its own binary,
    never through `plugin_cli`, which raises for it).

    This is the corrected version of the claim `MARKETPLACE_AGENT_SOURCES`
    used to encode: "pi has no CLI for a picker to find". It does -- pi ships
    a real binary, `shutil.which("pi")` resolves it exactly the way it
    resolves `claude`/`codex` -- what pi lacks is a *marketplace*, which is
    a different question with a different answer, and conflating the two is
    the bug this function exists to not repeat. `run_agent_menu` (step 1) and
    `main.py`'s `available_sources` both call this, so a pi binary shows up
    in exactly one place instead of two independently-maintained checks
    drifting apart.

    `sniff=False` (`probe status` without --refresh, which runs no
    subprocess) takes a pi binary on PATH at its word instead of asking its
    `--help`: the one difference, and the impostor guard it gives up.
    """
    detected = [source for source in MARKETPLACE_AGENT_SOURCES if plugin_cli.available(source)]
    if pi_binary_available() if sniff else pi_config.pi_on_path():
        detected.append("pi")
    return tuple(detected)


#: What every agent row on step 1 says under its title, per source -- NOT one
#: shared string: claude_code/codex go through a plugin marketplace AND pair
#: source-bound capture, but pi's install is a single settings.json `packages`
#: entry (extension + skills + MCP manifest), never a marketplace, so the old
#: one-size copy ("Install plugins and pair source-bound capture.") became
#: inaccurate for pi's row the moment pi could appear in this picker at all.
#: A table, not a ternary -- the same reason `AGENT_LABELS` is one: correct
#: only while there were exactly two sources, silently wrong for whichever
#: third one shows up. Module-level because the row is BUILT once and
#: REPAINTED on every toggle, and the two spellings drifted the moment they
#: were separate literals -- a divergence that only shows up mid-interaction,
#: after the first keystroke, which is the worst place to find it.
AGENT_ROW_DETAIL: dict[str, tuple[str, ...]] = {
    "claude_code": ("Plugins and session capture.",),
    "codex": ("Plugins and session capture.",),
    "pi": ("Extension, skills and MCP, via settings.json.",),
    "kimi_code": ("Plugins and session capture.",),
}


def short_path(path: Path) -> str:
    """`~/.codex/AGENTS.md`, not the full home-prefixed path.

    A summary bullet is read at a glance, and `/Users/<name>/` at the front of
    every path is the part with no information in it."""
    try:
        return f"~/{path.relative_to(Path.home())}"
    except ValueError:
        return str(path)


def agent_label(sources: tuple[str, ...] | list[str] | str) -> str:
    """User-facing name for the exact agents selected in this wizard run."""
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    labels = [AGENT_LABELS[source] for source in AGENT_LABELS if source in normalized]
    if not labels:
        return "coding agent"
    if len(labels) == 1:
        return labels[0]
    return f"{', '.join(labels[:-1])} and {labels[-1]}"


def instruction_files(sources: tuple[str, ...] | list[str] | str) -> str:
    """Name the real global instruction files for the selected agents."""
    from probe.harness import get_registry

    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    names: list[str] = []
    for source in normalized:
        harness = get_registry().find(source)
        name = (harness.instructions or {}).get("global") if harness else None
        if name and name not in names:
            names.append(name)
    return " + ".join(names) or "agent instructions"


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
    from probe.cli import tui

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
    from probe.cli import tui

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


def spoken_list(items: Sequence[str]) -> str:
    """`a`, `a and b`, `a, b and c`."""
    items = list(items)
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} and {items[-1]}"


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


class SummaryAction(StrEnum):
    """What a `RunSummary` counts."""

    INSTALL = "install"
    UPDATE = "update"
    UNINSTALL = "uninstall"


@dataclass
class AgentResult:
    """One coding agent's part of a run, for `RunSummary`: whether it worked,
    a few words on where it ended (versions), its errors, whether it needs a
    restart (or /reload) to load or apply Probe, and anything else it needs
    done that is not routine."""

    source: str
    ok: bool
    summary: str = ""
    notes: Sequence[str] = ()
    restart: bool = False
    must: Sequence[str] = ()


#: Words that make a noted line worth a person's attention: an error said in
#: prose rather than with a failure marker (`reports_failure`), or what to do
#: about one ("browser approval failed: ...", "revoke the key at ...").
_ATTENTION = re.compile(
    r"\b(fail(ed|ure|s)?|errors?|denied|refused|rejected|expired|timed out|revoke|re-run|retry|invalid"
    r"|not (fully|finished|installed|updated|confirmed|paired|saved|configured|valid|looked at)|unverified|unreadable)\b"
    # A command the person has to run, as its own sentence ("... website code.
    # Run `unset PROBE_TOKEN` in your shell before future Probe commands.").
    r"|(?:^|[.:;!]\s+)run `"
    # An exception named in passing ("W&B history pending (ConnectError).").
    r"|\(\w*(?:Error|Exception)\b|\bincomplete\b",
    re.IGNORECASE,
)


def needs_attention(line: str) -> bool:
    """Whether a line from an install or an Update is an error or what to do
    about one, not the routine report ("Status line: on", "Auto-update on.")."""
    return reports_failure(line.strip()) or bool(_ATTENTION.search(line))


def attention_lines(lines: Iterable[str]) -> list[str]:
    """The errors among an action's `lines` (`needs_attention`), each with the
    indented lines right under it (its reason, the command to run), the
    failure marker dropped; nothing routine."""
    out: list[str] = []
    following = False
    for line in lines:
        if not line.strip():
            following = False
        elif line.startswith("  "):
            if following:
                out.append(f"  {line.strip()}")
        else:
            following = needs_attention(line)
            if following:
                out.append(line.strip().removeprefix("! ").strip())
    return out


def result_page(headline: str | Sequence[str], *, next_steps: Iterable[str] = (), details: Iterable[str] = ()) -> list[str]:
    """A wizard action's final page: the answer to what was asked, then Next
    (what the person must still do) and Details (errors), each only when there
    is something to say. Every routine line an action's helpers report stays
    off it: those lines remain what a scripted or `--json` run prints."""
    lines = [headline] if isinstance(headline, str) else list(headline)
    next_steps = list(dict.fromkeys(line for line in next_steps if line.strip()))
    details = list(dict.fromkeys(line for line in details if line.strip()))
    if next_steps:
        lines += ["", "Next:", *(f"  {line}" for line in next_steps)]
    if details:
        lines += ["", "Details:", *(f"  {line}" for line in details)]
    return lines


def agents_counted(sources: Sequence[str], done: Sequence[str]) -> str:
    """"Claude Code", "all 4 coding agents", "3 of 4 coding agents"."""
    if len(sources) == 1:
        return agent_label(sources[0])
    if len(done) == len(sources):
        return "both coding agents" if len(sources) == 2 else f"all {len(sources)} coding agents"
    return f"{len(done)} of {len(sources)} coding agents"


class RunSummary:
    """The final screen of an install or an Update: how many coding agents
    worked, which, one Next line for the restarts and any other step that
    matters, then Details with the errors and nothing else. The full
    per-agent report it replaces spent a screen on lines like "already at the
    latest" and "Status line: on" around the one that mattered."""

    def __init__(self, action: SummaryAction, sources: Sequence[str]) -> None:
        self.action = action
        self._sources = list(sources)
        self._results: dict[str, AgentResult] = {}
        self._notes: list[str] = []
        self._must: list[str] = []
        #: The line under the headline: the CLI's version for an Update.
        self.subtitle = ""

    def record(
        self,
        source: str,
        *,
        ok: bool,
        summary: str = "",
        notes: Iterable[str] = (),
        restart: bool = False,
        must: Iterable[str] = (),
    ) -> None:
        self._results[source] = AgentResult(
            source, ok, summary, [n for n in notes if n.strip()], restart, [m for m in must if m.strip()]
        )

    def note(self, *lines: str) -> None:
        """Run-wide errors (the CLI, pi's package, the server): each once."""
        for line in lines:
            if line.strip() and line not in self._notes:
                self._notes.append(line)

    def must_do(self, *lines: str) -> None:
        """Run-wide steps that matter (pi's /reload when pi was not selected)."""
        for line in lines:
            if line.strip() and line not in self._must:
                self._must.append(line)

    def __bool__(self) -> bool:
        return bool(self._results)

    def lines(self) -> list[str]:
        results = [self._results[s] for s in self._sources if s in self._results]
        worked = [r for r in results if r.ok]
        lines = [self._headline(len(worked), len(self._sources))]
        if self.subtitle:
            lines.append(self.subtitle)
        if worked:
            width = max(len(agent_label(r.source)) for r in worked)
            lines.append("")
            lines += [
                f"  ✔ {agent_label(r.source):<{width}}   {r.summary}".rstrip() for r in worked
            ]
        next_lines = self._next(results)
        if next_lines:
            lines += ["", "Next:", *next_lines]
        details: list[str] = []
        for result in results:
            if not result.notes and result.ok:
                continue
            head, *rest = list(result.notes) or [
                {
                    SummaryAction.INSTALL: "did not finish",
                    SummaryAction.UPDATE: "not updated",
                    SummaryAction.UNINSTALL: "not fully removed",
                }[self.action]
            ]
            details.append(f"  {agent_label(result.source)}: {head.strip()}")
            details += [f"    {line}" for line in rest]
        not_reached = [s for s in self._sources if s not in self._results]
        if not_reached:
            stopped = next((r.source for r in results if not r.ok), None)
            where = f" (the run stopped at {agent_label(stopped)})" if stopped else ""
            details.append(f"  {spoken_list([agent_label(s) for s in not_reached])}: not started{where}")
        carried = {note.strip() for result in results for note in result.notes}
        details += [f"  {line}" for line in self._notes if line.strip() not in carried]
        if details:
            lines += ["", "Details:", *details]
        return lines

    def _next(self, results: list[AgentResult]) -> list[str]:
        """One sentence for every restart, then each other step that matters."""
        from probe.cli import upgrading

        out: list[str] = []
        restart = [r.source for r in results if r.restart]
        if restart:
            if self.action is SummaryAction.INSTALL:
                # A new install's plugins load at session start: a restart.
                verbs = [f"restart {spoken_list([agent_label(s) for s in restart])}"]
            else:
                # An update Kimi Code and pi take in place with /reload.
                reload = [s for s in restart if upgrading.reloads_plugins(s)]
                plain = [s for s in restart if s not in reload]
                verbs = [
                    *([f"restart {spoken_list([agent_label(s) for s in plain])}"] if plain else []),
                    *([f"/reload (or restart) {spoken_list([agent_label(s) for s in reload])}"] if reload else []),
                ]
            what = "load Probe" if self.action is SummaryAction.INSTALL else "apply the update"
            sentence = " and ".join(verbs)
            out.append(f"  {sentence[0].upper()}{sentence[1:]} to {what}.")
        carried = {line.strip() for r in results for line in r.must}
        for result in results:
            out += [f"  {agent_label(result.source)}: {line}" for line in result.must]
        out += [f"  {line}" for line in self._must if line.strip() not in carried]
        return out

    def _headline(self, worked: int, total: int) -> str:
        if total == 1:
            label = agent_label(self._sources[0])
            done = {
                SummaryAction.INSTALL: (f"Installed Probe in {label}", f"Probe was not fully installed in {label}"),
                SummaryAction.UPDATE: (f"Updated {label}", f"{label} was not fully updated"),
                SummaryAction.UNINSTALL: (f"Removed Probe from {label}", f"Probe was not fully removed from {label}"),
            }[self.action]
            return done[0] if worked else done[1]
        counted = agents_counted(self._sources, ["done"] * worked)
        return {
            SummaryAction.INSTALL: f"Installed Probe in {counted}",
            SummaryAction.UPDATE: f"Updated {counted}",
            SummaryAction.UNINSTALL: f"Removed Probe from {counted}",
        }[self.action]


_run_summary: ContextVar[RunSummary | None] = ContextVar("probe_run_summary", default=None)


@contextlib.contextmanager
def run_summary(action: SummaryAction, sources: Sequence[str]):
    """In this block, each agent's install or Update records its result in
    one `RunSummary` (`current_run_summary`)."""
    token = _run_summary.set(RunSummary(action, sources))
    try:
        yield _run_summary.get()
    finally:
        _run_summary.reset(token)


def current_run_summary() -> RunSummary | None:
    return _run_summary.get()


def step_name(step: int) -> str:
    """What this step is about, for the rule under the nav band."""
    return INSTALL_STEPS[step - 1]


# -- the coding-agent picker, per action ------------------------------------
#
# The picker is NOT the install's step 1 alone. `wizard()` opens it for every
# action scoped to a coding agent, and states that gate as exclusions -- not in
# `IMPORT_ACTIONS`, not in `DEVICE_ACTIONS` -- so uninstall, update, diagnose
# and the manual instructions all land on it too, and any action added to
# neither set will land on it without an edit here.
#
# It was written as if only Install could reach it. Picking "Uninstall Probe"
# opened a screen headed `Install Probe — step 1 of 2` asking "Which coding
# agents should Probe connect?" over rows reading "Install plugins and pair
# source-bound capture." -- four lines describing the opposite of the next
# keypress, on the one path in the product that destroys something.
#
# Keyed by `Action`, which is a StrEnum, so the plain value works as a key and
# this table costs no import of `actions` at module scope (see that module's
# docstring for why it stays out of `probe log`'s path).


#: Title, lede, question -- the three slots of the framed block, per action.
#: Only Install is NUMBERED: `INSTALL_STEPS` counts the install's screens, and
#: no other action walks them. Uninstall's second screen is `confirm_removal`,
#: which carries no number either; update and diagnose have no second screen at
#: all, so "step 1 of 2" there was a position in a flow that does not exist.
#:
#: WIDTH BUDGET on the question: it shares its row with the picker's
#: instruction, so at 80 columns -- the floor every terminal clears -- a longer
#: one wraps, and the wrapped row eats the blank that separates the question
#: from the `-- Coding agents` heading. The install's question is the budget,
#: pinned by a test rather than by a number counted here.
AGENT_SCREEN_COPY: dict[str, tuple[str, str, str]] = {
    "configure": (
        step_title(STEP_AGENTS),
        "Probe sets up each one you pick.",
        "Which coding agents?",
    ),
    "uninstall": (
        "Uninstall Probe",
        "Removes Probe from each one you pick.",
        "Which coding agents?",
    ),
    "update": (
        "Update Probe",
        "Updates the CLI and each agent's plugins.",
        "Which coding agents?",
    ),
    "diagnose": (
        "Diagnose a problem",
        "Checks each agent you pick.",
        "Which coding agents?",
    ),
    "manual": (
        "Set up manually",
        "Prints the commands for each one you pick.",
        "Which coding agents?",
    ),
}

#: What an unlisted action gets. Deliberately says nothing about what happens
#: next: a new action inheriting GENERIC copy is a screen that is merely thin,
#: and one inheriting the INSTALL's copy is a screen that lies. The drift guard
#: in the tests is what turns thin into named; nothing here can do it, because
#: the whole failure mode is an action nobody remembered to come and describe.
GENERIC_AGENT_SCREEN_COPY: tuple[str, str, str] = (
    "Coding agents",
    "Runs on each one you pick.",
    "Which coding agents?",
)

#: `AGENT_ROW_DETAIL` is the INSTALL's row detail; every other action needs its
#: own, for the same per-source reason that table exists (pi has no
#: marketplace, so it can neither gain nor lose a plugin).
AGENT_ROW_DETAIL_BY_ACTION: dict[str, dict[str, tuple[str, ...]]] = {
    "configure": AGENT_ROW_DETAIL,
    "uninstall": {
        "claude_code": ("Remove plugins and stop capture.",),
        "codex": ("Remove plugins and stop capture.",),
        "kimi_code": ("Remove plugins and stop capture.",),
        "pi": ("Remove its settings.json entry.",),
    },
    "update": {
        "claude_code": ("Update the plugins.",),
        "codex": ("Update the plugins.",),
        "kimi_code": ("Update the plugins.",),
        # Not a hedge: `upgrading.py` skips pi outright and says so in its own
        # output. Promising an upgrade here that the apply then declines is the
        # same class of mismatch as the install copy this table replaces.
        "pi": ("Update it through pi.",),
    },
    "diagnose": {
        "claude_code": ("Check setup, sign-in and updates.",),
        "codex": ("Check setup, sign-in and updates.",),
        "kimi_code": ("Check setup, sign-in and updates.",),
        "pi": ("Check setup, sign-in and updates.",),
    },
    "manual": {
        "claude_code": ("Print the setup commands.",),
        "codex": ("Print the setup commands.",),
        "kimi_code": ("Print the setup commands.",),
        "pi": ("Print the setup commands.",),
    },
}

#: The row detail an unlisted action gets. Names the agent's role in what
#: follows without claiming what that is -- see `GENERIC_AGENT_SCREEN_COPY`.
GENERIC_AGENT_ROW_DETAIL: tuple[str, ...] = ("Include this coding agent.",)


def agent_screen_copy(action: str | None) -> tuple[str, str, str]:
    """Title, lede and question for the picker, for the action that opened it.

    `None` is the caller that did not say -- a direct call, or a seam in a test
    -- and it gets the install, because that is the flow the picker was built
    for and the only one that reaches it without going through `wizard()`.
    """
    if action is None:
        return AGENT_SCREEN_COPY["configure"]
    return AGENT_SCREEN_COPY.get(str(action), GENERIC_AGENT_SCREEN_COPY)


def agent_row_detail(action: str | None, source: str) -> tuple[str, ...]:
    """What one agent row says under its title, for this action and source."""
    if action is None:
        return AGENT_ROW_DETAIL[source]
    detail = AGENT_ROW_DETAIL_BY_ACTION.get(str(action), {})
    return detail.get(source, GENERIC_AGENT_ROW_DETAIL)


#: The value of the row that ENDS a step, and of the row that goes BACK one.
#: Neither is a capability and neither is ever returned in a Selection.
#: What those rows say. A verb, not a noun: every other row is a thing you turn
#: on, and these two are the only things you DO.
NEXT_TITLE = "Next  ›"
BACK_TITLE = "‹  Back"

#: The band's left half, verbatim. Shared with `tui.dim_band_back`, which
#: repaints exactly this span grey while the `Next ›` half keeps the bright
#: separator colour -- the two must agree on the text or the repaint misses.
NAV_BACK_LEFT = f"{BACK_TITLE}   ←"

#: The value of the nav band ROW. One row, and one questionary Choice: the
#: library draws exactly one choice per line, so two cursor stops on one line
#: cannot be two choices. Which END the cursor is on is `NAV_STOPS` below,
#: tracked by the picker rather than by `pointed_at`.
NAV_BAND = "__nav_band__"

#: The band's two ends, IN CURSOR ORDER -- which is not their order on screen.
#:
#: `Next ›` comes first because it is where every step opens: continuing costs
#: one keystroke, and `↑` off the band goes straight to the options, which is
#: the whole point of parking there. `‹ Back` sits one `↓` further on. Reading
#: order (Back on the left, Next on the right) is what the row SHOWS; this is
#: the order the cursor walks, and the rectangle is what reconciles the two.
NAV_NEXT = "next"
NAV_BACK = "back"
NAV_SKIP = "skip"
NAV_STOPS: tuple[str, ...] = (NAV_NEXT, NAV_BACK)


def nav_row(choices: list):
    """The nav band row in a built row list, or None.

    Found by VALUE first and by content second. The agent step repaints this row
    to carry its refusal, and reaching for it positionally survives exactly
    until something else is added to the band.

    The content fallback is not dead weight: `run_confirm_install` builds its
    band through the same helper but on a `select` prompt, and any future screen
    that hand-rolls a band still resolves here rather than silently returning
    None and losing its Back key.
    """
    by_value = next((c for c in choices if getattr(c, "value", None) == NAV_BAND), None)
    if by_value is not None:
        return by_value
    return next((c for c in choices if BACK_TITLE in str(getattr(c, "title", ""))), None)


def without_nav(choices: list) -> list:
    """The same rows with the nav band stripped out.

    For the ONE case where the band is worse than nothing: `checkbox_control()`
    came back None, so `_wire_picker` installed no bindings and questionary's
    own rules are in force -- Enter submits, and its cursor parks on the first
    selectable row, which is `‹ Back`. A row that says "Back" and, when you
    press Enter on it, submits every ticked capability instead is not a
    degraded affordance, it is a mislabelled one, and on this screen the thing
    it silently agrees to is shipping your sessions off the machine.

    Escape still goes back (`tui.bind_escape` is wired outside the picker), so
    stripping the band costs discoverability on a path nobody should be on and
    removes a row that actively lies.
    """
    import questionary

    kept = [
        choice
        for choice in choices
        if getattr(choice, "value", None) != NAV_BAND
        and not (
            # Every worded separator: the band's pieces and the group headings,
            # which are the only other separators that carry text.
            isinstance(choice, questionary.Separator)
            and str(choice.title).strip()
        )
    ]
    # Drop the blanks left stranded at either edge -- the footer's spacer above
    # the band, or a leading one if the band ever moves back to the top.
    while kept and isinstance(kept[0], questionary.Separator) and not str(kept[0].title).strip():
        kept.pop(0)
    while kept and isinstance(kept[-1], questionary.Separator) and not str(kept[-1].title).strip():
        kept.pop()
    return kept


def nav_layout(*, forward: str | None = "→", next_title: str = NEXT_TITLE,
               back_title: str = BACK_TITLE, focus=None, skip_title=None):
    """The band row AS DRAWN, plus where the rectangle on it sits.

    Returns `(text, lead, width)`: the finished line, and the offset and width
    of the `┌───┐` that belongs above and below it. One function rather than a
    text half and a geometry half, because they are one fact -- a box measured
    somewhere other than where the label was placed is a cursor pointing at
    nothing, and that is a bug you can only see on a terminal.

    Both labels sit on FIXED columns, and the rails are drawn around them
    rather than pushing them along: `‹ Back` starts where every option's text
    starts (`tui.BOX_GUTTER` in) and `Next ›` ends where every option row's
    rectangle ends, focused or not. So moving the cursor between the two ends
    moves the box and nothing else -- a band whose labels slid two columns
    every time you pressed `↓` would read as the screen redrawing itself.

    `forward=None` drops the right half, and with it that end's cursor stop,
    for a screen that only offers Back.
    """
    from probe.cli import tui

    left = f"{back_title}   ←"
    rails = 2 + tui.BOX_GUTTER  # `│ ` … ` │`: what a rectangle costs a row
    right = None if forward is None else f"{forward}   {next_title}"
    total = len(left) + rails if right is None else max(tui.box_width(), len(left) + rails)
    if skip_title and right and total < len(left) + len(right) + len(skip_title) + 3 * rails:
        skip_title = "Skip"
        if total < len(left) + len(right) + len(skip_title) + 3 * rails:
            left, right = back_title.replace("‹  ", ""), next_title.replace("  ›", "")
    cells = [" "] * total

    def place(text: str, at: int) -> None:
        for offset, char in enumerate(text):
            if 0 <= at + offset < len(cells):
                cells[at + offset] = char

    back_at = tui.BOX_GUTTER
    place(left, back_at)
    next_at = total - len(right) - tui.BOX_GUTTER if right is not None else total
    if right is not None:
        place(right, next_at)
    skip_at = (total - len(skip_title)) // 2 if skip_title else 0
    if skip_title:
        place(skip_title, skip_at)

    if focus == NAV_BACK:
        place("│", back_at - tui.BOX_GUTTER)
        place("│", back_at + len(left) + 1)
        return "".join(cells).rstrip(), back_at - tui.BOX_GUTTER, len(left) + rails
    if focus == NAV_NEXT and right is not None:
        place("│", next_at - tui.BOX_GUTTER)
        place("│", next_at + len(right) + 1)
        return "".join(cells).rstrip(), next_at - tui.BOX_GUTTER, len(right) + rails
    if focus == NAV_SKIP and skip_title:
        place("│", skip_at - tui.BOX_GUTTER)
        place("│", skip_at + len(skip_title) + 1)
        return "".join(cells).rstrip(), skip_at - tui.BOX_GUTTER, len(skip_title) + rails
    return "".join(cells).rstrip(), back_at - tui.BOX_GUTTER, len(left) + rails


def nav_stops_for(forward, skip_title=None) -> tuple[str, ...]:
    """Which ends this band draws, in `NAV_STOPS` order."""
    if skip_title:
        return (NAV_NEXT, NAV_SKIP, NAV_BACK) if forward is not None else (NAV_SKIP, NAV_BACK)
    return NAV_STOPS if forward is not None else (NAV_BACK,)


def nav_band(*, forward: str | None = "→", next_title: str = NEXT_TITLE,
             back_title: str = BACK_TITLE, focus=None, skip_title=None) -> str:
    """`‹ Back  ←` on the left, `→  Next ›` on the right, in ONE row.

    They were two stacked rows, both left-aligned, which spent two lines saying
    what one line says better. Back and Next are a PAIR -- opposite ends of the
    same axis -- so stacking them hid the one relationship the band exists to
    show, and cost a row of the step's own content to do it. Left and right
    edges say "these two go opposite ways" before a word is read.

    ONE row, TWO cursor stops. questionary draws one choice per line, so the
    band cannot be two Choices; `NAV_STOPS` and the picker's own `↑`/`↓` supply
    the second stop, and the rectangle `nav_layout` places is what says which
    end Enter will fire. `←`/`→` and Escape still work from anywhere, so the
    keys printed on the band remain true -- they are shortcuts now rather than
    the only way through.
    """
    return nav_layout(forward=forward, next_title=next_title, back_title=back_title,
                      focus=focus, skip_title=skip_title)[0]


def step_heading(step: int) -> list:
    """The heading that leads a step's rows. Three separators, no cursor stops.

    A BLANK FIRST -- the 0.95.1 fix, carried into this layout. questionary
    renders the choice list flush against the question, so without it the
    first row of the list sits one line under the last thing you read: the
    boundary between "what you are being asked" and "what follows" had
    disappeared. The band no longer opens the step, so the heading is what
    gets the air now.

    A BLANK LAST, which is not decoration: it is the row the first option's
    rectangle draws its `┌───┐` into. Every other row inherits one from the
    blank that separates it from the row above; the first row of a group has a
    heading there instead, so without this it is the one row on screen that
    could be pointed at and not boxed.
    """
    import questionary

    from probe.cli import tui

    return [
        questionary.Separator(" "),
        questionary.Separator(tui.heading(step_name(step))),
        questionary.Separator(" "),
    ]


def dress_band(question, control) -> None:
    """The band's two token repaints, wired the one way every screen wants them.

    Both reach into questionary's token stream and both are guarded there, so
    this is a convenience rather than a safety net -- but the pairing is a rule:
    the pointer is suppressed on the band (the rectangle marks the cursor there)
    and `‹ Back` is dimmed EXCEPT while it is the end the cursor is on.
    """
    from probe.cli import tui

    tui.blank_pointer_when(question, lambda value: value == NAV_BAND)
    band = nav_row(getattr(control, "choices", []))
    back_title = getattr(band, "nav", {}).get("back_title", BACK_TITLE)
    tui.dim_band_back(question, f"{back_title}   ←", active=lambda: nav_focus(control) == NAV_BACK)


def nav_footer(*, forward: bool = True, next_title: str = NEXT_TITLE,
               back_title: str = BACK_TITLE, skip_title=None) -> list:
    """The nav band, drawn UNDER the step's rows, as a row the cursor can hold.

    Under the rows, not above them. The band used to open each step, which put
    the way FORWARD on screen before any of the choices it would confirm. At
    the bottom the band sits where the reading ends, after the rows it acts on
    -- and it is where every step now OPENS, so `↑` is what reaches the options
    and pressing Enter straight away accepts them as shown.

    THREE rows, not two, and only one of them carries text. The blanks above
    and below are where the selection rectangle's `┌───┐` and `└───┘` are
    painted when the cursor is on the band (see `tui.box_edge`): the box lives
    in rows the layout already spends, so nothing below it moves when the
    cursor arrives and `content_height` stays a count of fixed rows. The upper
    blank does its old job too -- the band reads as chrome rather than as the
    last option's continuation line.

    `forward=False` drops the right half and its cursor stop for a screen that
    only offers Back.
    """
    import questionary

    band = questionary.Choice(
        title=nav_band(forward="→" if forward else None, next_title=next_title,
                       back_title=back_title, skip_title=skip_title),
        value=NAV_BAND,
    )
    # Carried ON the row because the picker REBUILDS its text on every render:
    # the box has to follow the cursor between the band's two ends, and the
    # agent step swaps `forward` for a refusal. Storing the ingredients beats
    # re-deriving them from a string that has already been boxed once.
    band.nav = {"forward": "→" if forward else None, "next_title": next_title}
    if back_title != BACK_TITLE:
        band.nav["back_title"] = back_title
    if skip_title:
        band.nav["skip_title"] = skip_title
    return [
        questionary.Separator(" "),
        band,
        questionary.Separator(" "),
    ]


def nav_focus(control) -> str | None:
    """Which end of the nav band the cursor is on, or None if it is elsewhere.

    Read off the control because that is the object every caller already holds;
    the state itself belongs to `_wire_picker`, which is the only thing allowed
    to move it.

    The `or None if it is elsewhere` half is load-bearing, not tidiness: a band
    with only ONE end has `focus` permanently pinned
    to it, so a caller that read the state alone would think the cursor was
    parked on `‹ Back` for the whole screen and quietly stop dimming it.
    """
    state = getattr(control, "probe_nav", None) or {}
    try:
        if getattr(control.get_pointed_at(), "value", None) != NAV_BAND:
            return None
    except Exception:  # noqa: BLE001 - a colour question is never worth a crash
        return None
    return state.get("focus")


def band_stops(band) -> tuple[str, ...]:
    """The band's cursor stops for this screen, in cursor order.

    A step with no forward half has one stop, not two: `nav_stops_for` is the
    single place that decides, so a screen cannot grow a cursor stop for a
    label it does not draw.
    """
    if band is None:
        return ()
    return nav_stops_for(
        getattr(band, "nav", {}).get("forward"), getattr(band, "nav", {}).get("skip_title"),
    )


def _logical_lines(title: str, pad: str) -> list[str]:
    """A row's lines with the absolute left pad taken back off.

    questionary prefixes only a choice's FIRST line, so `_menu_row` gives every
    continuation line the pad itself. The rectangle is drawn in row-relative
    columns, so the pad has to come off before the rails go on and back on
    after -- otherwise the second line's rail lands `left_pad()` columns right
    of the first line's.
    """
    lines = str(title).split("\n")
    return [lines[0]] + [
        line[len(pad) :] if line.startswith(pad) else line.lstrip() for line in lines[1:]
    ]


def _paint_boxes(control, *, band, focus, slots, cache) -> None:
    """Put the rectangle on the row under the cursor, and the gutter on the rest.

    Runs on EVERY render (see `_wire_picker`), not on every keystroke, because
    the cursor moves by six different keys -- arrows, `j`/`k`, `Ctrl-N`/`Ctrl-P`
    -- and a repaint hung off any subset of them is a box that lags the cursor
    on whichever one was forgotten.

    `slots` are the blank separator rows collected before the first paint: the
    rectangle's `┌───┐` and `└───┘` go in the blanks the layout already spends
    above and below each row, so the box costs no lines and nothing on screen
    moves when the cursor arrives. Every slot is reset each pass; a border left
    behind by the previous cursor position is a rectangle around nothing.

    `cache` maps a row to the (plain, boxed) pair last painted, so a title the
    caller's redraw did NOT rewrite is un-boxed from the cache instead of being
    boxed a second time. Without it the static rows -- the confirm screen's
    `Install ›`, which no redraw owns -- gain a rail per render.
    """
    import questionary

    from probe.cli import tui

    choices = list(control.choices)
    for slot in slots:
        slot.title = " "
    pad = tui.body_indent()
    width = tui.box_width()
    pointed = control.get_pointed_at()
    for index, choice in enumerate(choices):
        if isinstance(choice, questionary.Separator):
            continue
        if choice is band:
            # The band draws ITSELF: its two labels sit on fixed columns and the
            # rails go around one of them, which is not what `box_rails` does to
            # a row with one field. `nav_layout` owns that geometry.
            text, lead, span = nav_layout(
                **getattr(band, "nav", {}), focus=focus if choice is pointed else None
            )
            choice.title = text
            if choice is pointed:
                _paint_edges(choices, index, span, lead=lead, slots=slots)
            continue
        remembered = cache.get(id(choice))
        title = str(choice.title)
        plain = remembered[0] if remembered and title == remembered[1] else title
        lines = _logical_lines(plain, pad)
        if choice is pointed:
            drawn = tui.box_rails(lines, width)
            _paint_edges(choices, index, width, lead=0, slots=slots)
        else:
            drawn = tui.box_gutter(lines)
        boxed = ("\n" + pad).join(drawn)
        cache[id(choice)] = (plain, boxed)
        choice.title = boxed


def _paint_edges(choices: list, index: int, width: int, *, lead: int, slots: list) -> None:
    """Draw the rectangle's top and bottom into the blank rows either side."""
    from probe.cli import tui

    for offset, top in ((-1, True), (1, False)):
        neighbour = index + offset
        if not 0 <= neighbour < len(choices):
            continue
        row = choices[neighbour]
        if any(row is slot for slot in slots):
            row.title = tui.box_edge(width, lead=lead, top=top)


def _wire_picker(
    question,
    *,
    redraw=None,
    can_submit=None,
    on_leave=None,
    on_back=None,
    single=False,
    cycles=None,
    cycle_state=None,
):
    """One rule for every step: ENTER ACTIVATES THE ROW UNDER THE CURSOR.

    On a capability that means toggle; on the nav band it means whichever end
    the rectangle is around -- `Next ›` (where every step opens) or `‹ Back`.
    questionary's own rule is space-toggles / enter-submits, which is the
    checkbox convention -- but the wizard's two checkbox screens ran BACK TO
    BACK with opposite meanings for Enter, because one of them had its own
    binding and the other did not. Whichever you learned first was wrong on the
    next screen.

    THE BAND TAKES THE CURSOR, and it is where the cursor starts. Continuing
    costs one Enter, and the options are reached by going deliberately up --
    which is the point: a step you are happy with should not ask you to travel
    to leave it, and one you want to change should ask you to say so. `↑`/`↓`
    walk `NAV_STOPS` while the cursor is on the band, so its two ends behave
    like two rows despite sharing one line; `←`/`→` and Escape keep working
    from anywhere as shortcuts.

    `single=True` is for a `select` prompt, where a row is an ANSWER rather than
    a checkbox: Enter on a non-band row submits it instead of ticking it.

    `cycles` is `{value: (state, ...)}` for rows that CYCLE instead of ticking:
    the same key does the same thing -- act on this row -- but it advances one
    step round that tuple instead of flipping a box, and wraps. The states live
    on `control.probe_cycle`, which the caller reads back after the prompt
    exits. `cycle_state` seeds them; a row with no seed starts at `[0]`.

    `can_submit` is the step's own guard (the agent picker needs at least one
    agent). It is checked HERE rather than through questionary's `validate=`,
    which only ever runs on questionary's submit -- the path this binding
    replaces. A step whose guard says no simply does not leave, and says so on
    the Next row; see `run_agent_menu`.

    Every reach into questionary is guarded. If any of it stops working the
    prompt still runs with the library's own behaviour rather than failing to
    render -- a picker that looks slightly wrong beats a wizard that cannot ask
    the question at all.
    """
    import questionary

    from probe.cli import tui

    control = tui.checkbox_control(question)
    if control is None:
        return None  # library defaults; enter still submits, space still toggles

    cycles = dict(cycles or {})
    # The cycling rows' state, and the ONLY copy of it: `selected_options` has
    # two positions and these rows have three, so a screen that read the box
    # back would lose whichever state the box cannot spell. Kept on the control
    # because the control is what outlives the prompt -- see `run_settings_menu`.
    control.probe_cycle = {
        value: (cycle_state or {}).get(value) or order[0] for value, order in cycles.items()
    }
    band = next((c for c in control.choices if getattr(c, "value", None) == NAV_BAND), None)
    stops = band_stops(band)
    # Read back by `nav_focus`, which is how a caller styles the end the cursor
    # is on without reaching into this closure.
    state = {"focus": stops[0] if stops else None}
    control.probe_nav = state
    slots = [
        choice
        for choice in control.choices
        if isinstance(choice, questionary.Separator) and not str(choice.title).strip()
    ]
    cache: dict[int, tuple[str, str]] = {}

    def refresh() -> None:
        if redraw is not None:
            redraw(control)

    def leave(event, result) -> None:
        control.is_answered = True
        event.app.exit(result=result)

    def submit(event) -> None:
        if can_submit is not None and not can_submit(control):
            refresh()
            return
        if on_leave is not None:
            leave(event, on_leave(control))
            return
        # No `on_leave`: answer with the pointed row. `getattr`, not
        # `.value` -- `activate` routes here when NOTHING is pointed at, and an
        # AttributeError raised inside a key binding takes the prompt down
        # rather than surfacing anywhere a user could act on.
        leave(event, getattr(control.get_pointed_at(), "value", None))

    def retreat(event) -> None:
        # The toggles the user made before backing out are reported, not
        # discarded: leaving a screen is not the same as un-deciding on it.
        if on_back is not None:
            on_back(control)
        leave(event, tui.BACK)

    def activate(event) -> None:
        """Enter, and it means ONE thing: act on the row you are on.

        On the band that reads off the rectangle rather than the row -- the two
        ends share a line, so "the row you are on" is only half an answer there
        and the box is what supplies the other half.
        """
        pointed = control.get_pointed_at()
        if pointed is None:
            submit(event)
            return
        if pointed.value == NAV_BAND:
            if state["focus"] == NAV_SKIP:
                leave(event, tui.SKIP)
                return
            (retreat if state["focus"] == NAV_BACK else submit)(event)
            return
        if single:
            submit(event)
            return
        toggle(control, pointed.value)
        refresh()

    def step(delta: int) -> None:
        """questionary's own move, skipping separators, in one direction."""
        move = control.select_next if delta > 0 else control.select_previous
        move()
        for _ in range(control.choice_count):
            if control.is_selection_valid():
                return
            move()

    def travel(delta: int) -> None:
        """`↑`/`↓`, with the band counting as one stop per END.

        The band is a single questionary Choice -- the library draws one choice
        per line -- so the second stop cannot come from `pointed_at`. It comes
        from walking `NAV_STOPS` while the cursor sits on the band and only
        stepping off once the walk runs out of ends.

        Entering the band from ABOVE lands on the first stop (`Next ›`, so the
        common path is Enter and nothing else) and from BELOW on the last, which
        is what `↑` out of the top of the list has to do to be reversible.
        """
        if band is not None and stops and control.get_pointed_at() is band:
            index = (stops.index(state["focus"]) if state["focus"] in stops else 0) + delta
            if 0 <= index < len(stops):
                state["focus"] = stops[index]
                return
        step(delta)
        if band is not None and stops and control.get_pointed_at() is band:
            state["focus"] = stops[0] if delta > 0 else stops[-1]

    def toggle(ctrl, value) -> None:
        if value in cycles:
            advance(ctrl, value)
            return
        if value in ctrl.selected_options:
            ctrl.selected_options.remove(value)
        else:
            ctrl.selected_options.append(value)

    def advance(ctrl, value, *, to=None) -> None:
        """One press of a CYCLING row: the next state round, wrapping.

        Membership is kept in step with the FIRST state rather than left to
        drift, because it is what the row falls back to on the degraded path
        where our bindings never got installed -- and a `selected_options` that
        disagreed with `probe_cycle` would make which path you were on decide
        what the screen committed.
        """
        order = cycles[value]
        if to is None:
            here = ctrl.probe_cycle.get(value)
            to = order[(order.index(here) + 1) % len(order)] if here in order else order[0]
        ctrl.probe_cycle[value] = to
        if to == order[0] and value not in ctrl.selected_options:
            ctrl.selected_options.append(value)
        elif to != order[0] and value in ctrl.selected_options:
            ctrl.selected_options.remove(value)

    def bulk(event, select_all: bool) -> None:
        """questionary's own `a` / `i`, routed through OUR repaint.

        The library binds bare `a` (select all) and `i` (invert) eagerly and
        mutates `selected_options` directly. That was fine while questionary
        drew the boxes -- it repaints from the same list. We turned its
        indicator OFF (`draw_own_boxes`) and paint the box into the title
        ourselves, so its handlers changed the ANSWER without changing the
        SCREEN: untick capture, press `a`, and the row still rendered `○
        Session capture` while the submitted Selection carried capture=True.
        The consent gate cannot be a screen the answer disagrees with.
        """
        for choice in control.choices:
            value = getattr(choice, "value", None)
            # The band is a ROW, not an option: `a` ticking it would put the
            # sentinel in the answer and leave a rail drawn round a checkbox
            # nobody offered.
            if value is None or value == NAV_BAND or getattr(choice, "disabled", None):
                continue
            if value in cycles:
                # `a` means "everything on", which on a cycling row is its first
                # state; `i` inverts, and the nearest thing a three-state row has
                # to an inversion is the step the space bar would have taken.
                advance(control, value, to=cycles[value][0] if select_all else None)
                continue
            wanted = select_all if select_all else value not in control.selected_options
            if wanted and value not in control.selected_options:
                control.selected_options.append(value)
            elif not wanted and value in control.selected_options:
                control.selected_options.remove(value)
        refresh()

    refresh()

    try:
        from prompt_toolkit.keys import Keys

        bindings = question.application.key_bindings

        @bindings.add("c-m", eager=True)  # Enter
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            activate(event)

        @bindings.add(" ", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            activate(event)

        # Registered AFTER questionary's, so prompt_toolkit's `matches[-1]`
        # resolution picks ours. Same keys, same meaning, but they repaint.
        @bindings.add("a", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            bulk(event, select_all=True)

        @bindings.add("i", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            bulk(event, select_all=False)

        # EVERY key questionary moves the cursor with, not just the arrows: the
        # band's second stop lives outside `pointed_at`, so a movement key left
        # on the library's handler would step straight over `‹ Back` and make
        # which key you pressed decide whether that row exists.
        def mover(delta: int):
            def _move(event) -> None:  # pragma: no cover - requires a live terminal
                travel(delta)

            return _move

        for key in (Keys.Down, "j", Keys.ControlN):
            bindings.add(key, eager=True)(mover(1))
        for key in (Keys.Up, "k", Keys.ControlP):
            bindings.add(key, eager=True)(mover(-1))

    except Exception:  # noqa: BLE001 - never let a binding break the prompt
        pass

    # `→` only where the band actually draws a forward half, so the shortcut
    # always agrees with the visible forward action.
    tui.bind_step_keys(
        question, on_back=retreat, on_next=submit if (band is None or NAV_NEXT in stops) else None
    )
    try:
        # Registered after `tui.bind_escape`, so this one wins. Escape is the
        # other half of the `‹ Back` label and has to route through `retreat`
        # too, or it exits without reporting the toggles `←` keeps.
        @question.application.key_bindings.add("escape", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            retreat(event)

    except Exception:  # noqa: BLE001 - never let a binding break the prompt
        pass

    try:
        # The rectangle is painted from the RENDER, not from the key handlers.
        # `control.text` is the token source prompt_toolkit calls every frame
        # (the same door `tui.dim_band_back` goes through), so the box follows
        # the cursor however it moved -- including paths this module never
        # bound, and including the very first frame, before any key is pressed.
        original = control.text

        def repaint():
            try:
                refresh()
                _paint_boxes(control, band=band, focus=state["focus"], slots=slots, cache=cache)
            except Exception:  # noqa: BLE001 - an unboxed row beats no prompt
                pass
            return original()

        control.text = repaint
    except Exception:  # noqa: BLE001 - an unboxed row beats no prompt
        pass
    return control


def run_agent_menu(defaults: tuple[str, ...], *, action: str | None = None):
    """Choose every coding agent this one wizard pass acts on.

    `action` is what OPENED the picker, and it is the whole reason this screen
    is not a constant: `wizard()` shows it for uninstall, update, diagnose and
    the manual instructions too (see `AGENT_SCREEN_COPY`), and it used to greet
    every one of them with the install's title, lede and row detail. Omitted
    means the install -- the flow this screen is step 1 of.
    """
    import questionary

    from probe.cli import tui
    from probe.cli.actions import Action

    title, lede, question_text = agent_screen_copy(action)

    tui.use_checkmarks()  # the fallback path, if we cannot take the box over

    indent = tui.body_indent()
    rows = {
        source: questionary.Choice(
            title=_menu_row(
                AGENT_LABELS[source],
                agent_row_detail(action, source),
                checked=source in defaults,
                indent=indent,
            ),
            value=source,
            checked=source in defaults,
        )
        # `detectable_sources()`, not MARKETPLACE_AGENT_SOURCES: this step
        # auto-detects a coding-agent CLI, and pi IS one -- `shutil.which("pi")`
        # finds its binary exactly the way `plugin_cli.available` finds
        # `claude`/`codex` (see that function's docstring for the "pi has no
        # CLI" claim this replaces). Called fresh here rather than trusting
        # `defaults` to double as the row set: `defaults` is `agent_defaults`,
        # which a Codex session pins to `("codex",)` regardless of what else
        # this machine has -- using it for row VISIBILITY too would hide a
        # present Claude Code or pi row for a reason that has nothing to do
        # with whether they are actually here.
        for source in detectable_sources()
    }
    choices: list = []
    for index, row in enumerate(rows.values()):
        if index:
            # Same reason as every other menu here: without a blank row an
            # option's title sits directly under the previous option's
            # description, and two entries read as one paragraph.
            choices.append(questionary.Separator(" "))
        choices.append(row)
    choices.extend(nav_footer())
    progress = install_header(STEP_AGENTS) if action in (None, Action.CONFIGURE) else None
    message = tui.framed("Coding agents" if progress else title, tui.wrap(lede), question_text)
    instruction = "(enter picks this row · ↑ to change)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
        # KEPT, even though our own Enter binding never reaches it. questionary
        # only runs `validate` on ITS submit -- the path `_wire_picker` replaces
        # -- so on the happy path this is dead weight. It is the FALLBACK's
        # guard: when questionary's internals move and `checkbox_control()`
        # comes back None, `_wire_picker` installs no bindings at all and the
        # library's own enter-submits wins, `can_submit` never runs, and an
        # empty selection sails through. Downstream that is not a cosmetic
        # degradation: `wizard()` indexes `agent_sources[0]` and the whole
        # command dies with an IndexError.
        validate=lambda answer: bool(answer) or "Choose at least one coding agent.",
    )
    own_boxes = tui.draw_own_boxes(question)

    def redraw(control) -> None:
        """Repaint the boxes, and the Next row's reason for refusing.

        The empty selection is the only state this step can be in that it
        cannot leave, so it is the only one that has to explain itself. Saying
        it on the Next row -- the row you are pressing -- beats a validation
        error under a prompt that no longer exists, and beats the alternative
        this replaced, which was a key that silently did nothing.

        `own_boxes` is False only when `checkbox_control()` returned None, and
        `_wire_picker` bails on that same condition BEFORE it ever calls this --
        so this function only ever runs with the boxes ours to draw. The
        fallback is guarded by `validate=` above instead, which is the one
        thing questionary still runs when we cannot reach its control.
        """
        for source, row in rows.items():
            row.title = _menu_row(
                AGENT_LABELS[source],
                agent_row_detail(action, source),
                checked=source in control.selected_options,
                indent=indent,
            )
        chosen = [value for value in control.selected_options if value in rows]
        band = nav_row(choices)
        if band is not None:
            # The right half carries the refusal. It is the only place this step
            # can say why Enter on `Next ›` is doing nothing, and it sits under
            # the cursor's own column rather than in an error line below a
            # prompt. Set on the row's INGREDIENTS, not on its rendered title:
            # `_paint_boxes` rebuilds the band's text every frame and would
            # overwrite a title written here on the very next render.
            band.nav["forward"] = "→" if chosen else "choose at least one agent —"

    control = _wire_picker(
        question,
        redraw=redraw,
        can_submit=lambda control: any(value in rows for value in control.selected_options),
        on_leave=lambda control: [v for v in control.selected_options if v in rows],
    )
    if control is None:
        # Same call as step 2's: an unwirable band is a row that says Back and
        # does something else. `validate=` above is what guards this path.
        choices = without_nav(choices)
        instruction = "(space to toggle, enter to continue · esc goes back)"
        question = tui.checkbox(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
            validate=lambda answer: bool(answer) or "Choose at least one coding agent.",
        )
    elif not own_boxes:
        # questionary is drawing its own indicator in front of a title that
        # already carries one, so strip ours rather than ship `✔ ✔ Claude Code`.
        for source, row in rows.items():
            row.title = _menu_row(
                AGENT_LABELS[source],
                agent_row_detail(action, source),
                checked=False,
                indent=indent,
            ).split(" ", 1)[1]
    tui.point_at(control, lambda value: value == NAV_BAND)
    dress_band(question, control)

    picked = tui.ask(
        question,
        height=tui.content_height(message, choices, instruction=instruction),
        margin=1 if progress is not None else tui.MARGIN,
        progress=progress,
    )
    if picked is None or picked is tui.BACK:
        return picked
    # `rows`, not MARKETPLACE_AGENT_SOURCES: it is exactly the set this run
    # OFFERED (see the row-building loop above), in the same order, so a
    # checked pi box survives instead of being filtered back out by a tuple
    # that never knew pi could be a row at all.
    chosen = tuple(source for source in rows if source in picked)
    # NEVER an empty tuple. `wizard()` reads `agent_sources[0]` straight after
    # this, so "answered with nothing" has to be a non-answer here rather than
    # an IndexError three frames up. Unreachable while `validate=` holds; this
    # is the second lock on the same door, because the first one lives inside a
    # library we have already had to guard against six times.
    return chosen or tui.BACK


#: The shared footer supplies the arrow. This label names the install action
#: and gives the forward button the same width as Back and the earlier Next.
INSTALL_TITLE = "Install"


def confirm_rows(
    agent_sources: tuple[str, ...] | list[str] | str,
    *,
    plugins_available: bool = True,
    unavailable: tuple[str, ...] = (),
    spaced: bool = True,
) -> list[str]:
    """The disclosure block of the confirm screen: every capability this
    install turns on, one bullet each, capture's data grant included.

    THIS BLOCK IS THE CONSENT SURFACE the capability picker used to be. The
    rows are built from the same `menu_copy` the picker used, so the capture
    bullet still says what it sends and where — and the render test asserts it
    fits, whole, on a real 80x24 screen before the confirming keystroke.

    `plugins_available=False` is the GPU-pod shape: neither `claude` nor
    `codex` is on PATH, so promising plugin rows would promise work this run
    cannot do. The degraded block names what still happens (the CLI and the
    sign-in) and is honest about the future: nothing is queued — the way the
    plugins arrive later is re-running the wizard and picking Install.

    `plugins_available` is computed upstream from `MARKETPLACE_AGENT_SOURCES`
    only (see `main.py`'s `plugin_promising_sources`), so it can be False
    while `agent_sources` still names pi -- a run selecting Claude Code and pi
    on a machine with no `claude` on PATH. pi's install never depended on
    that binary (see `pi_config`), and `apply_tracking`'s force-on reaches pi
    regardless of this flag, so the degraded early-return below must not say
    "nothing is queued" about it -- see the `"pi" in normalized` branch.
    """
    from probe.cli import tui

    normalized = (agent_sources,) if isinstance(agent_sources, str) else tuple(agent_sources)
    indent = "  "
    detail_indent = "      "
    # The room a bullet's detail actually has: the framed block is CONTENT_WIDTH
    # wide and centred, so what bounds a line is the block, or the terminal when
    # the terminal is the narrower of the two -- not `columns() - 8`, which was
    # a guess that happened to be right at 84 columns and threw four columns
    # away at 80. Four columns is a wrapped line, and a wrapped line on this
    # screen is a row of the capture disclosure pushed under the fold.
    room = max(20, min(tui.CONTENT_WIDTH, tui.columns()) - len(detail_indent))
    lines: list[str] = []

    def bullet(title: str, details: tuple[str, ...]) -> None:
        if lines and spaced:
            lines.append("")
        lines.append(f"{indent}• {title}")
        for detail in details:
            lines.extend(f"{detail_indent}{wrapped}" for wrapped in tui.wrap(detail, room))

    if not plugins_available:
        bullet(
            "Probe CLI + sign-in",
            ("Approve this device in your browser.",),
        )
        if "pi" in normalized:
            # pi never depended on the `claude`/`codex` binary this screen is
            # degraded over -- its install is one settings.json `packages`
            # entry, not a marketplace plugin (see pi_config's module
            # docstring), and tracking's force-on reaches it the same as any
            # other run. Saying "skipped" about pi here, the way the bullet
            # below correctly does for the missing marketplace agent, would
            # be describing marketplace-plugin work pi's install does not do.
            bullet(
                "pi extension, skills and MCP",
                ("One entry in pi's settings.json.",),
            )
        marketplace_sources = tuple(source for source in normalized if source in MARKETPLACE_AGENT_SOURCES)
        if marketplace_sources:
            bullet(
                "Coding-agent plugins — skipped",
                ("No Claude Code or Codex found. Install one, then run probe wizard › Install Probe.",),
            )
        return lines

    # Capture LAST, deliberately: on a terminal shorter than the block,
    # prompt_toolkit keeps the cursor's end visible and cuts the TOP — so the
    # bullet nearest the question survives folding longest, and the one that
    # must is the data grant.
    copy = menu_copy(agent_sources)
    for capability in (Capability.TRACKING, Capability.AGENT_RULES):
        title, details = copy[capability]
        bullet(title, details)
    _, auto_update_detail = auto_update_copy(agent_sources)
    bullet("Automatic updates", (auto_update_detail,))
    title, details = copy[Capability.CAPTURE]
    bullet(title, details)
    # A PARTIAL miss: some selected agent's CLI is not on this machine, so its
    # plugin half cannot happen this run. Said here, on the screen making the
    # promises, rather than discovered as a skipped step after the keystroke.
    for source in unavailable:
        bullet(
            f"{agent_label(source)} plugins — skipped",
            (f"{agent_label(source)} is not on this machine. Install it, then run probe wizard › Install Probe.",),
        )
    return lines


def run_confirm_install(
    agent_sources: tuple[str, ...] | list[str] | str,
    *,
    step: int | None = None,
    plugins_available: bool = True,
    unavailable: tuple[str, ...] = (),
    defaults: "DefaultsPick | None" = None,
):
    """The confirm screen: features followed by the shared Back / Install band.

    Returns True (install), tui.BACK, or None (Ctrl-C).

    The capability rows are STATIC — they live in the framed message, like the
    state block above the action menu, because they are not choices: the
    install is complete by design (see the module docstring). Install is the
    forward end of the same navigation band used by the earlier step; Back and
    Escape return to the previous choices.

    `step` is supplied when the agent screen was shown. Otherwise review is
    step 2 of 3: import choices, review and installation remain.
    """
    import questionary

    from probe.cli import tui

    agent_screen_shown = step is not None
    progress = install_header(STEP_CONFIRM, agent_screen_shown=agent_screen_shown)
    rows = confirm_rows(
        agent_sources, plugins_available=plugins_available, unavailable=unavailable
    )
    if defaults is not None:
        # The Defaults step's picks, which this keystroke applies. The daemon's
        # full consent was on that step; one line here says what it does.
        from probe.sdk import session_marker

        rows.extend([
            "",
            f"  {RECORDER_ROW_TITLE}: {defaults.recorder}  ·  "
            f"New sessions: {session_marker.state_label(setting_state(defaults.session_state))}",
        ])
        if defaults.recorder == session_marker.RECORDER_DAEMON:
            rows.extend(
                f"  {line}" for line in tui.wrap("The daemon records as you and sends session parts to an AI model.")
            )
    rows.append("")
    rows.extend(
        f"  {line}"
        for line in tui.wrap("Undo anytime: probe wizard › Uninstall Probe.")
    )
    rows.extend(["", "  One browser approval covers everything above."])
    message = tui.framed(
        "Features",
        rows,
        "Ready to install?",
    )

    choices = nav_footer(next_title=INSTALL_TITLE)
    instruction = "(enter selects · ← back · → install)"
    question = tui.select(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    # The forward end must return the install decision, never the nav sentinel.
    control = _wire_picker(question, single=True, on_leave=lambda _control: True)
    if control is None:
        # Without custom bindings, each option still returns the decision it
        # names through questionary's ordinary select.
        choices = [
            questionary.Choice(INSTALL_TITLE, value=True),
            questionary.Choice(BACK_TITLE, value=tui.BACK),
        ]
        instruction = "(enter selects · esc goes back)"
        question = tui.select(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
        tui.bind_step_keys(question, on_back=lambda event: event.app.exit(result=tui.BACK))
    else:
        tui.point_at(control, lambda value: value == NAV_BAND)
        dress_band(question, control)
    return tui.ask(
        question,
        height=tui.content_height(message, choices, instruction=instruction),
        margin=0,
        progress=progress,
    )


# -- choose and run imports after setup succeeds ----------------------------


class BackfillChoice(StrEnum):
    """One optional import selected during onboarding or from the main menu."""

    PAST_SESSIONS = "past_sessions"
    PROJECT_FOLDER = "project_folder"


#: Row copy for the offer, `MENU_COPY`-shaped. PAST_SESSIONS is a data grant
#: like capture, so its detail says what leaves the machine and at what pace.
BACKFILL_OFFER_COPY: dict[BackfillChoice, tuple[str, tuple[str, ...]]] = {
    BackfillChoice.PAST_SESSIONS: (
        "Import past coding sessions",
        (
            "Reads selected agents' transcripts; asks before anything uploads.",
        ),
    ),
    BackfillChoice.PROJECT_FOLDER: (
        "Import a folder of project work",
        ("An agent reads, uploads and describes it.",),
    ),
}

#: The offer's forward label. Continuing with nothing ticked is a real answer —
#: skipping is not a failure state, so the band never refuses.
OFFER_TITLE = "Continue  ›"


def run_backfill_offer(
    agent_sources: tuple[str, ...] | list[str] | str,
    *,
    defaults: set[BackfillChoice] | None = None,
    agent_screen_shown: bool = True,
    onboarding: bool = True,
    back_to_menu: bool = False,
):
    """Choose research work to import after installation or from the main menu.

    Checkbox rows over the same picker machinery as the settings screen.
    Both rows start selected unless explicit defaults are supplied. Returns
    None (Ctrl-C), tui.BACK, or a set of BackfillChoice. An empty set skips imports.
    """
    import questionary

    from probe.cli import tui
    from probe.cli.actions import ACTION_COPY, Action

    tui.use_checkmarks()

    defaults = set(BackfillChoice) if defaults is None else defaults
    indent = tui.body_indent()
    rows: dict[BackfillChoice, questionary.Choice] = {}
    choices: list = []
    for choice, (title, detail) in BACKFILL_OFFER_COPY.items():
        choices.append(questionary.Separator(" "))
        row = questionary.Choice(
            title=_menu_row(title, detail, checked=choice in defaults, indent=indent),
            value=choice,
            checked=choice in defaults,
        )
        rows[choice] = row
        choices.append(row)
    choices.extend(nav_footer(forward=True, next_title=OFFER_TITLE,
                              back_title="‹  Main menu" if back_to_menu else BACK_TITLE))
    message = tui.framed(
        ACTION_COPY[Action.IMPORT_RESEARCH][0],
        [],
        "What should be imported?",
    )
    instruction = "(enter picks this row · ↑ to change)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    control = _bind_menu_keys(question, rows, copy=BACKFILL_OFFER_COPY, indent=indent)
    if control is None:
        choices = without_nav(choices)
        instruction = "(space to toggle, enter to continue)"
        question = tui.checkbox(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
    else:
        dress_band(question, control)

    if back_to_menu and hasattr(question, "_probe_content"):
        question._probe_content["instruction"] = (
            "↑↓ choose · space toggle · enter · esc main menu"
        )
    picked = tui.ask(
        question, height=tui.content_height(message, choices, instruction=instruction),
        progress=(install_header(STEP_IMPORTS, agent_screen_shown=agent_screen_shown)
                  if onboarding else []), margin=1,
    )
    if picked is None:
        return None
    if picked is tui.BACK:
        return tui.BACK
    return {choice for choice in picked if isinstance(choice, BackfillChoice)}


@dataclass(frozen=True)
class Selection:
    """The resolved end state, after flags/menu/current state are reconciled."""

    tracking: bool
    capture: bool
    auto_update: bool
    agent_rules: bool
    #: Capabilities this run leaves exactly as it finds them: no install, no
    #: removal, no re-enable, whatever their boolean above says. For a caller
    #: changing ONE thing (Settings, Update's capture question) whose booleans
    #: for the rest are only a read. A read is lossy: `capture_on` is False for
    #: a deliberate off AND for a sign-in's pending lock, and applying that
    #: False tore down a credential nobody had turned off (Anthrogen,
    #: 2026-10-26). Honoured for tracking and capture, the two that hold a
    #: credential or a plugin; automatic updates and the rules block are files
    #: their boolean already reads back unchanged.
    preserve: frozenset[Capability] = frozenset()

    def as_map(self) -> dict[Capability, bool]:
        return {
            Capability.TRACKING: self.tracking,
            Capability.CAPTURE: self.capture,
            Capability.AUTO_UPDATE: self.auto_update,
            Capability.AGENT_RULES: self.agent_rules,
        }

    def keeps(self, capability: Capability) -> bool:
        """This run must leave `capability` as it found it."""
        return capability in self.preserve and capability in PRESERVABLE


#: The capabilities `Selection.preserve` applies to (see there).
PRESERVABLE: frozenset[Capability] = frozenset({Capability.TRACKING, Capability.CAPTURE})


def resolve_selection(
    caps: Capabilities,
    *,
    tracking: bool | None,
    capture: bool | None,
    auto_update: bool | None,
    agent_rules: bool | None = None,
    configured: bool | None = None,
    current_override: dict[Capability, bool] | None = None,
) -> Selection:
    """The flag truth table. An omitted flag means one thing, and only one.

        FRESH run  (nothing configured yet) -> omitted flag = FRESH_DEFAULTS
        RE-RUN     (something configured)   -> omitted flag = PRESERVE current

    PRESERVE is the load-bearing half. Without it, `probe wizard --yes` in CI --
    or any re-run that names one flag and not the others -- would silently
    revoke a developer's capture pairing or switch on auto-update behind their
    back. An omitted flag must never be read as "disable".

    `current_override` supplies "current" when one snapshot cannot express it.
    A run configuring BOTH agents has two snapshots, and what PRESERVE has to
    keep is what the DEVICE has -- the union -- not what the agents agree on.
    Deriving it from the intersection instead reads a machine with Claude Code
    set up and Codex fresh as having nothing on, and PRESERVE then faithfully
    preserves nothing: every box unticked, and the apply path turns Claude
    Code's capture off on the way to installing Codex.
    """
    current = current_override if current_override is not None else caps.enabled()
    if configured is None:
        configured = caps.configured
    fallback = current if configured else FRESH_DEFAULTS
    explicit = {
        Capability.TRACKING: tracking,
        Capability.CAPTURE: capture,
        Capability.AUTO_UPDATE: auto_update,
        Capability.AGENT_RULES: agent_rules,
    }
    resolved = {
        capability: (value if value is not None else fallback[capability])
        for capability, value in explicit.items()
    }
    # PRESERVE reads capture as `capture_on`, which is False behind a sign-in's
    # pending lock, and applying that False tears the parked credential down
    # (`Selection.preserve`). An omitted flag means "leave it": leave it pending.
    pending = capture is None and configured and caps.capture_awaiting_confirmation
    return Selection(
        tracking=resolved[Capability.TRACKING],
        capture=resolved[Capability.CAPTURE],
        auto_update=resolved[Capability.AUTO_UPDATE],
        agent_rules=resolved[Capability.AGENT_RULES],
        preserve=frozenset({Capability.CAPTURE}) if pending else frozenset(),
    )


def menu_copy(
    sources: tuple[str, ...] | list[str] | str,
) -> dict[Capability, tuple[str, tuple[str, ...]]]:
    """Capability copy scoped to the agents this run will actually configure."""
    agents = agent_label(sources)
    rules = instruction_files(sources)
    return {
        Capability.TRACKING: (
            "CLI + MCP",
            ("Track runs and search your team's work.",),
        ),
        Capability.CAPTURE: (
            "Session capture",
            (f"Sends this device's {agents} sessions to your team.",),
        ),
        Capability.AGENT_RULES: (
            f"Rules in your global {rules}",
            (f"Prompts {agents} to search and track research in Probe.",),
        ),
    }


# Backwards-compatible default for non-interactive consumers that only need
# capability titles. Interactive callers always request copy for their targets.
MENU_COPY = menu_copy(("claude_code", "codex"))
# The picker is a picker. The full disclosure of what leaves the machine --
# prompts, assistant replies, shell commands, and the client-side redaction that
# is a filter rather than a guarantee -- lives on the BROWSER APPROVAL screen,
# which is where the grant is actually made and where research-os asserts the
# wording verbatim. Repeating three lines of it here made the shortest menu in
# the product the densest thing to read.


#: Copy for automatic updates. Once its own wizard step; now only the DETAIL
#: half has a production consumer (`confirm_rows`). The question half is kept
#: for the copy tests that measure it, nothing else.
def auto_update_copy(sources: tuple[str, ...] | list[str] | str) -> tuple[str, str]:
    return (
        "Keep it up to date automatically?",
        "Updates the CLI and plugins at session start.",
    )


AUTO_UPDATE_COPY = auto_update_copy(("claude_code", "codex"))

#: How `plan()` names each capability in "This run will: - enable X".
#:
#: MUST stay total over `Capability`. It is a SEPARATE map from MENU_COPY
#: because the plan covers every capability while MENU_COPY only holds the
#: checkbox rows -- reading the label out of MENU_COPY crashed the wizard on
#: every fresh install, since auto-update is asked outside that list and always
#: changes state on a machine that has never been set up. The phrasings differ
#: too: a menu row is a question ("Keep it up to date automatically?"), a plan
#: step is a noun ("enable automatic updates").
PLAN_LABELS: dict[Capability, str] = {
    Capability.TRACKING: MENU_COPY[Capability.TRACKING][0],
    Capability.CAPTURE: MENU_COPY[Capability.CAPTURE][0],
    Capability.AUTO_UPDATE: "automatic updates",
    # Its own noun, not the menu title: the concrete filename is selected later
    # because Claude Code and Codex load different global instruction files.
    Capability.AGENT_RULES: "the global agent guidance rules",
}

#: What the step reads when the PLUGIN is already installed and only the
#: credential is missing. Distinct from PLAN_LABELS because "enable CLI + MCP"
#: on such a machine promises an install that will not happen: the run's whole
#: job there is the browser approval.
SIGN_IN_LABELS: dict[Capability, str] = {
    Capability.TRACKING: "sign in (the CLI + MCP plugin is already installed)",
    Capability.CAPTURE: "sign in to pair Session capture (the plugin is already installed)",
}


def interactive() -> bool:
    """Whether a real human can answer a prompt. Both ends must be a TTY: a
    piped stdin with a TTY stdout is a script, and must take the flag path."""
    return sys.stdin.isatty() and sys.stdout.isatty()


#: How an apply_* message announces that something went wrong. The wizard's
#: progress screen has to tell a failed step from a successful one, and these
#: helpers report failure in PROSE rather than by raising -- so the markers live
#: here, beside the code that emits them. A copy of this tuple in main.py would
#: drift the first time someone reworded a message, and the tick would quietly
#: go green on a step that failed.
_FAILURE_MARKERS = ("could not", "!")


def reports_failure(message: str) -> bool:
    """Whether an apply_* message is reporting a failure or a warning.

    Case-insensitive on purpose: `apply_agent_rules` says "Could not update
    ..." with a capital C, and a classifier that only knew the lowercase
    spelling turned that failure into a green tick."""
    return message.lower().startswith(_FAILURE_MARKERS)


#: The refreshes and installs `marketplace_refreshes` runs together: the
#: sources still to take theirs, each one's answer once run (its refresh and
#: the installs after it), the installs each source asked for, which of their
#: capabilities the run may install (`allow_batch_installs`), and the installs
#: already taken. None outside one.
_refresh_batch: ContextVar[dict | None] = ContextVar("probe_marketplace_refreshes", default=None)


@contextlib.contextmanager
def marketplace_refreshes(
    sources: Iterable[str], installs: Mapping[str, Sequence[tuple[Capability, str]]] | None = None
):
    """In this block, the first `refresh_marketplace` of any of `sources`
    refreshes all of them at once, one thread each, then installs each one's
    `installs` (capability, plugin name), in order, on the same thread, and
    returns once every one has answered; each source's own first refresh and
    its installs (`install_plugin`) then take their answers instead of running
    again (a second one, an install's retry, runs for real).

    An install for several agents refreshed and installed one agent after
    another, a git clone or fetch (~2.5 s on a first install) and a plugin
    install or two each. Here they overlap. The first refresh is an install
    step, after the sign-in: nothing is written while a person approves
    (`sdk.device`), and a first `add` writes Claude Code's settings or Codex's
    config.toml. Only plugins whose credential the sign-in got are installed
    (`allow_batch_installs`). Every one answers before the first refresh
    returns, so none runs beside another agent's install steps."""
    token = _refresh_batch.set({
        "pending": set(sources), "answers": {}, "installed": {}, "installs": dict(installs or {}),
        "allowed": frozenset(), "taken": set(),
    })
    try:
        yield
    finally:
        _refresh_batch.reset(token)


def allow_batch_installs(capabilities: Iterable[Capability]) -> None:
    """The capabilities whose plugins the open batch may install with its
    refreshes: those the run holds a credential for, set at the install's
    refresh step. Unset, the batch installs nothing: each agent installs at
    its own step, as before."""
    batch = _refresh_batch.get()
    if batch is not None and not batch["answers"]:
        batch["allowed"] = frozenset(capabilities)


def _taken_install(name: str, source: str) -> "claude_cli.Result | None":
    """The open batch's install of `name` for `source`, once, if it ran."""
    batch = _refresh_batch.get()
    future = batch["installed"].get(source) if batch is not None else None
    if future is None or not future.done() or future.exception() is not None:
        return None
    installed = future.result()
    if name not in installed or (source, name) in batch["taken"]:
        return None
    batch["taken"].add((source, name))
    return installed[name]


def _refresh_together(batch: dict) -> None:
    """Start every refresh in `batch` on its own thread and wait for them all.
    A daemon thread each, and an interrupted wait is not resumed: a cancelled
    wizard exits now (a terminal's Ctrl-C stops the agents' CLIs with it). A
    source whose thread cannot start (a process limit) refreshes on its own, at
    its own step, as it did before the batch."""
    answers: dict[str, Future] = batch["answers"]
    #: Each future's source and how many of its units it finishes.
    units: dict[Future, tuple[str, int]] = {}
    for each in sorted(batch["pending"]):
        refreshed: Future = Future()
        installed: Future = Future()
        plan = [name for capability, name in batch["installs"].get(each, ()) if capability in batch["allowed"]]

        def run(each=each, refreshed=refreshed, installed=installed, plan=plan) -> None:
            try:
                refreshed.set_result(_refresh_marketplace_now(each))
            except BaseException as exc:  # noqa: BLE001 - re-raised to its source's refresh
                refreshed.set_exception(exc)
            try:
                retried: list[bool] = []
                # One retry for the agent, as `_run_wizard_action`'s budget allows.
                installed.set_result({
                    name: install_plugin(
                        name, source=each, on_retry=lambda: not retried and not retried.append(True)
                    )
                    for name in plan
                })
            except BaseException as exc:  # noqa: BLE001 - the agent's own step installs again
                installed.set_exception(exc)

        try:
            # An empty context: a thread that saw this batch (a free-threaded
            # build copies the caller's) would wait on itself from a retry.
            threading.Thread(
                target=contextvars.Context().run, args=(run,), name=f"probe-marketplace-{each}", daemon=True
            ).start()
        except RuntimeError:
            break
        answers[each] = refreshed
        batch["installed"][each] = installed
        units[refreshed] = (each, 1)
        units[installed] = (each, len(plan))
    batch["pending"].intersection_update(answers)
    run = _install_run.get()
    # Waited for HERE, the thread that draws the screen: the run's bar moves
    # as each agent's refresh and installs finish.
    if run is not None:
        run.batch_started(answers)
    waiting = set(units)
    while waiting:
        finished, waiting = wait_for_futures(waiting, return_when=FIRST_COMPLETED)
        for future in finished:
            if run is not None:
                run.batch_progress(*units[future])


def refresh_marketplace(*, source: str | None = None) -> claude_cli.Result:
    """Bring the local marketplace copy up to date. ONCE per wizard run.

    `marketplace add` on an already-added marketplace does NOT refresh it, so
    without the update a fresh wizard run happily installs a stale plugin
    version -- which is exactly how a newly published plugin appears to be
    missing. The dashboard's pairing modal ships `add` and `update` as separate
    commands for the same reason.

    Hoisted OUT of install_plugin, which used to do it per plugin: a run that
    installs both plugins refreshed the same marketplace twice, and threw both
    results away. Discarding them is why a failed refresh surfaced as Claude's
    downstream "not found in marketplace" -- an error whose suggested fix is
    the very command the wizard had just silently failed at.

    `add` failing is NOT fatal and is not reported: the common case is "already
    on disk", which exits non-zero on some versions. `update` is the one whose
    success decides whether the catalog we install from is current, except
    after an `add` that cloned the marketplace just now: that copy is current,
    and its answer is the refresh's (`_refresh_marketplace_now`). Inside
    `marketplace_refreshes`, several agents' refreshes run at once.

    pi has no marketplace to refresh -- `install_plugin`/`uninstall_plugin`
    route it through `pi_config`'s settings.json entry instead (see
    `INSTALLABLE_AGENT_SOURCES`), which needs no separate refresh step.
    Checked explicitly, not folded into the (now pi-inclusive)
    `INSTALLABLE_AGENT_SOURCES` membership test below, because pi IS
    installable through this wizard now -- just not through a marketplace.
    Reported as a no-op SUCCESS, not a failure: main.py's `_refresh()` step
    turns any non-`ok` Result here into a printed "! could not refresh..."
    line, and a pi capture install's own step label now legitimately starts
    with "install" (pi is no longer excluded from that check either), which
    schedules this step for a pi run exactly like it does for claude_code/
    codex. A failure-shaped no-op would paint a real success red.
    """
    selected = source or agent_source()
    batch = _refresh_batch.get()
    if batch is not None and selected in batch["pending"] and not batch["answers"]:
        _refresh_together(batch)
    if batch is None or selected not in batch["pending"]:
        return _refresh_marketplace_now(selected)
    batch["pending"].discard(selected)
    return batch["answers"][selected].result()


def _refresh_marketplace_now(selected: str) -> claude_cli.Result:
    """`refresh_marketplace` for `selected`, run now."""
    if selected == "pi":
        return claude_cli.Result(ok=True, detail=f"{selected} has no plugin marketplace to refresh")
    if selected not in INSTALLABLE_AGENT_SOURCES:
        return claude_cli.Result(
            ok=False, detail=f"{selected} has no plugin marketplace", reachable=False
        )
    checkout = plugin_cli.marketplace_checkout(selected, MARKETPLACE)
    cloning = checkout is not None and not checkout.exists()
    added = plugin_cli.add_marketplace(selected, MARKETPLACE_REPO, name=MARKETPLACE)
    if cloning and added.ok and checkout.exists():
        # This `add` cloned it just now, so the copy is current: an `update`
        # would fetch the same repository again, ~2 s of a first install.
        return added
    refreshed = plugin_cli.refresh_marketplace(selected, MARKETPLACE)
    if not refreshed.ok and not added.ok:
        from probe.cli import updater

        # On a machine that never added the marketplace, `add` is the clone
        # that hits a Mac's blocked git, and `update` then fails as "not
        # found": report the cause, not the symptom.
        if updater.git_blocker(added.detail):
            return added
        # Otherwise say BOTH. `add` alone can be the harmless "already
        # added", but when the refresh then fails too, `add`'s refusal is
        # usually the cause: Codex's "not configured as a Git marketplace"
        # was all a researcher saw of an add that had been refused.
        return claude_cli.Result(
            ok=False,
            detail=f"`{added.command}` failed: {added.detail}\n"
            f"`{refreshed.command}` failed: {refreshed.detail}",
            reachable=refreshed.reachable,
            command=refreshed.command,
        )
    return refreshed


def _install_pi_package(*, tracking: bool = True) -> claude_cli.Result:
    """The `source == "pi"` half of `install_plugin`.

    Kept as its own function so `install_plugin` itself stays one dispatch
    read top to bottom, not a growing if/elif column -- the same reason
    `refresh_marketplace` got hoisted out from per-plugin duplication.

    `pi_config.install_package_entry` is already idempotent and already
    returns exactly the `claude_cli.Result` shape this call site needs (see
    that module's own docstring on why `claude_cli.Result` specifically).
    Migration (plan D4) only changes the returned `detail` when it actually
    removed something -- a legacy `~/.pi/agent/extensions/probe-research-pi`
    symlink still pointing inside OUR package root. The far more common
    "nothing to migrate" / "left alone, it resolves elsewhere" outcomes are
    not worth repeating on every single install, and folding a migration
    FAILURE in here would misreport the install itself as failed when the
    settings.json write -- the part that actually matters -- succeeded.

    No local checkout is NOT a failure. This used to resolve a package root
    up front and return `reachable=False` when none existed, which is every
    machine without a research-os clone -- so the wizard told each of those
    users "could not find the probe-research-pi package", naming an env var
    and a checkout neither of which they have. `install_package_entry` now
    picks the source itself (`resolve_install_source`: local checkout for a
    plugin developer, the published mirror repo otherwise), so this call site
    just asks for the install and reports what happened.
    """
    result = pi_config.install_package_entry(tracking=tracking)
    if not result.ok:
        return result

    root = pi_config.local_package_root()
    if root is None:
        # Mirror install: `~/.pi/agent/extensions/probe-research-pi` can only
        # ever have pointed inside a local checkout, so with no checkout there
        # is nothing D4 could match -- skip the migration rather than resolve
        # a root that does not exist just to hand it a guaranteed no-op.
        return result

    migration = pi_config.migrate_legacy_symlink(root)
    if migration.detail.startswith("removed legacy symlink"):
        return claude_cli.Result(ok=True, detail=f"{result.detail}; {migration.detail}")
    return result


def install_plugin(name: str, *, source: str | None = None, on_retry=None) -> claude_cli.Result:
    """Install one plugin. Retries ONCE, after a refresh, on ANY failure.

    Deliberately NOT gated on matching Claude's error text. A retry that fires
    only when the message contains "not found in marketplace" is a guard that
    certifies its own rot: Anthropic rewords the string, the retry silently
    stops firing, and every test stays green. One plain rule instead -- it
    failed, so refresh and try once more -- costs one extra attempt on a
    genuinely broken machine and cannot fall out of sync with anyone's prose.

    `on_retry` is the caller's retry BUDGET, not a notification: it returns
    False once the run has already spent its single retry, so two plugins
    failing cannot cost two refreshes and two reinstalls.

    pi has NO marketplace at all, so `name` is ignored on that branch (see
    `_install_pi_package`): one settings.json `packages` entry is the whole
    install, for every capability that reaches this function -- both
    `apply_tracking`'s and `apply_capture`'s calls converge on the same
    idempotent write. Retrying is meaningless there too (a failed write is
    not repaired by trying the identical write again), so `on_retry` is
    never consulted on that branch.
    """
    # Installing Probe again after an Uninstall: the OS keeper may come back (D35).
    with contextlib.suppress(Exception):
        from probe.service import keeper

        keeper.allow()
    selected = source or agent_source()
    taken = _taken_install(name, selected)
    if taken is not None:
        return taken  # installed with its marketplace's refresh (`marketplace_refreshes`)
    if selected not in INSTALLABLE_AGENT_SOURCES:
        return claude_cli.Result(
            ok=False, detail=f"{selected} has no plugin marketplace", reachable=False
        )
    if selected == "pi":
        # One package, two halves: only the tracking half's install (either
        # profile's name) brings Probe's skills and MCP on a FRESH entry; the
        # capture half arrives as `pi_config.PACKAGE_NAME` (CAPTURE_PLUGIN_LABEL).
        return _install_pi_package(tracking=name in _TRACKING_NAMES)
    result = plugin_cli.install(selected, f"{name}@{MARKETPLACE}")
    if result.ok or on_retry is None or not on_retry():
        return result
    refresh_marketplace(source=selected)
    return plugin_cli.install(selected, f"{name}@{MARKETPLACE}")


#: The tracking half's plugin names (either profile). For pi, whose one package
#: carries both halves, these decide which half an install or uninstall means.
_TRACKING_NAMES = (TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME)


def uninstall_plugin(
    name: str, *, source: str | None = None, keep_capture: bool | None = None
) -> claude_cli.Result:
    selected = source or agent_source()
    if selected not in INSTALLABLE_AGENT_SOURCES:
        return claude_cli.Result(
            ok=False, detail=f"{selected} has no plugin marketplace", reachable=False
        )
    if selected == "pi":
        capture_stays = _settings_capture_on(selected) if keep_capture is None else keep_capture
        if name in _TRACKING_NAMES and capture_stays:
            # Capture rides in the same package: switch tracking off instead.
            return pi_config.set_tracking(False, daemon=daemon_records(selected))
        return pi_config.remove_package_entry()
    return plugin_cli.uninstall(selected, f"{name}@{MARKETPLACE}")


def _settings_capture_on(source: str) -> bool:
    """A settings-package agent's (pi's) capture is live here: its own
    credential, no killswitch. Decides whether unticking tracking may delete
    the one package both halves share."""
    try:
        return bool(capture_token_sources(source)) and not (tap_plugin_dir(source) / ".disabled").exists()
    except Exception:  # noqa: BLE001 - unknown is "keep the package"
        return True


#: What each capability's plugin cannot work without.
#:
#: `api` rides along with tracking because the CLI needs a credential to be useful
#: at all; `mcp` is the separate read-only one so the MCP surface cannot write. A
#: capture-only selection asks for capture alone -- deliberately, so someone who
#: wanted only transcript capture is not handed read/write/delete they never asked
#: for.
#:
#: ONE table, read by both `grants_for` (what to request) and
#: `blocked_by_missing_grants` (what may install once the answer is back). They were
#: two hardcoded lists for about a day, which is exactly long enough for a third
#: grant to be added to one and not the other -- and the failure mode of that skew
#: is an install gated on a credential nobody asked for, or worse, not gated at all.
CAPABILITY_GRANTS: dict[Capability, tuple[str, ...]] = {
    Capability.TRACKING: ("api", "mcp"),
    Capability.CAPTURE: ("capture",),
}

#: The Probe daemon's own credential: `[read, write, delete]` since the trash
#: (0261; `delete` opens only the move-to-trash routes), revocable on its own.
#: Requested when the `daemon` state is chosen (the menu's Defaults row, or
#: `probe companion authorize`), not by a capability, because `daemon` is a
#: position of the tracking-default row rather than a thing that installs. Stored
#: as the context's `companion_token`, where the tap's worker reads it.
COMPANION_GRANT = "companion"


#: Where the wizard asks whether this team may use the daemon at all: the
#: server answers with the model routes' own gateway door (every plan may).
DAEMON_AVAILABILITY_PATH = "/v1/companion/availability"
#: What the tracking row says under a NO, by the server's reason code. The
#: server's own sentence is written for a refusal; the row wants a short line.
DAEMON_UNAVAILABLE_NOTES = {
    "companion_disabled": "Daemon recording is not enabled for this team.",
}
#: A NO with a reason this CLI does not know yet (a newer server).
DAEMON_UNAVAILABLE_NOTE = "Daemon recording is not available for this team."
#: The whole question's budget, wall clock: httpx's timeout is per step (and a
#: DNS lookup has none), so a captive network could otherwise hold the Settings
#: screen for ten seconds and more before it draws.
DAEMON_AVAILABILITY_BUDGET_S = 3.0


def daemon_availability(base_url: str | None = None) -> "tuple[bool | None, str | None]":
    """Whether this team may use the Probe daemon, per the server (Richard
    2026-09-28: "build the gate in the install wizard"): `(True, None)`,
    `(False, why)`, or `(None, None)` when it cannot tell -- signed out,
    offline, or a server older than the route. One request, no retry, and
    at most `DAEMON_AVAILABILITY_BUDGET_S` of wall clock however the network
    stalls. `base_url` is the API the wizard is pointed at (`--base-url`).

    Only a NO hides the daemon. An unknown answer keeps offering it: guessing
    "no" would only take the daemon away from a team whose network blinked."""
    import threading

    try:
        from probe.sdk.config import resolve

        settings = resolve(base_url=base_url) if base_url else resolve()
    except Exception:  # noqa: BLE001 - an unreadable config is "cannot tell"
        return None, None
    if not settings.token:
        return None, None
    answer: list = []

    def ask() -> None:
        try:
            from probe.sdk.surface import Surface
            from probe.sdk.transport import Transport

            transport = Transport(settings, max_retries=0, surface=Surface.CLI.value)
            try:
                response = transport.request(
                    "GET", DAEMON_AVAILABILITY_PATH, idempotent=True,
                    timeout=DAEMON_AVAILABILITY_BUDGET_S,
                )
                answer.append(response.json() if response.content else {})
            finally:
                transport.close()
        except Exception:  # noqa: BLE001 - any failure is "cannot tell", see docstring
            return

    # A daemon thread with a join deadline, not a pool: a stalled lookup must
    # neither hold the screen nor hold the process open at exit.
    worker = threading.Thread(target=ask, name="probe-daemon-availability", daemon=True)
    worker.start()
    worker.join(DAEMON_AVAILABILITY_BUDGET_S)
    body = answer[0] if answer else None
    available = body.get("available") if isinstance(body, dict) else None
    if not isinstance(available, bool):
        return None, None
    if available:
        return True, None
    return False, DAEMON_UNAVAILABLE_NOTES.get(str(body.get("code")), DAEMON_UNAVAILABLE_NOTE)


def companion_token_held() -> bool:
    """Whether this context already holds the daemon's credential."""
    from probe.sdk.config import load_context

    try:
        return bool((load_context() or {}).get("companion_token"))
    except Exception:  # noqa: BLE001 - an unreadable config is "not held"
        return False


def grants_for(selection: Selection) -> list[str]:
    """The grant set for ONE browser approval."""
    grants: list[str] = []
    for capability, wanted in CAPABILITY_GRANTS.items():
        if selection.as_map()[capability]:
            grants.extend(wanted)
    return grants


def blocked_by_missing_grants(
    capability: Capability, *, needed: list[str], granted: dict
) -> list[str]:
    """The grants this capability requires that the run TRIED and FAILED to get.

    Only grants in `needed` count. A re-run that already holds `api`/`mcp` never
    asks for them again, so they are absent from `granted` for the good reason --
    reading that as failure would refuse to install on every healthy machine.
    """
    return [
        grant
        for grant in CAPABILITY_GRANTS.get(capability, ())
        if grant in needed and grant not in granted
    ]


def has_source_capture_grant(source: str, tokens: Iterable[TokenSource]) -> bool:
    """Whether capture has a credential that can belong to this agent.

    `capture_token_sources` already returns only the agent's own sources: the
    shared CLI config token counts for Claude Code alone (it is Claude Code's
    capture token; the server refuses it on every other agent's route).
    """
    del source  # each agent's sources are already its own
    return bool(set(tokens))


def needs_authorization(caps: Capabilities, selection: Selection) -> list[str]:
    """The grants this run must actually obtain, skipping ones already held.

    Re-running with everything already working must NOT drag the user through
    another browser approval -- the wizard is a manager as well as an installer,
    and a no-op re-run should be a no-op.
    """
    wanted = grants_for(selection)
    if not wanted:
        return []
    have: set[str] = set()
    if caps.logged_in_as:
        have.add("api")
    if caps.capture_token_sources and caps.capture_credential_valid is not False:
        have.add("capture")
    # Its own signal, never `api`'s: a token pasted into `probe wizard --action
    # login --token` signs in without an MCP token, and folding `mcp` into
    # `api` left that device with no MCP at all (R11).
    # A token the API REFUSED is not held: re-authorizing is the only repair,
    # and without this a revoked token made `probe wizard` a no-op.
    from probe.cli.capabilities import mcp_token_rejected

    if caps.mcp_token_held and not mcp_token_rejected():
        have.add("mcp")
    return [grant for grant in wanted if grant not in have]


def headless_needs(needs: list[str]) -> list[str]:
    """`needs_authorization`'s answer for a run nobody is watching. A missing MCP
    token ALONE never holds an install on a browser approval nobody is there to
    give (it polls for up to 10 minutes): the rest installs as it did before, and
    an interactive Install asks for it."""
    return [] if needs == ["mcp"] else needs


def write_paired_capture_token(source: str, token: str, base_url: str) -> None:
    """One agent's capture credential where its tap reads it: `.token` in its
    own tap folder, beside a `.config` pinning the API origin. Every source but
    claude_code, whose credential is the CLI config's `ingest_token`
    (`write_capture_credential`). Shared by the sign-in (`authorize`) and a
    staff capture repair (`probe.cli.main._capture_repair_notice`), so the two
    cannot disagree about where a token lives. Raises OSError."""
    state_dir = tap_plugin_dir(source)
    state_dir.mkdir(parents=True, exist_ok=True)
    token_path = state_dir / ".token"
    token_tmp = state_dir / ".token.tmp"
    # Created 0600 with the secret's first byte, never written then narrowed:
    # under a 022 umask the old write-then-chmod left the plaintext readable by
    # every local user for that moment. A stale temp file from an interrupted
    # write would keep its old mode under O_CREAT, so it goes first and O_EXCL
    # makes the new one ours.
    token_tmp.unlink(missing_ok=True)
    fd = os.open(token_tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(token)
    os.replace(token_tmp, token_path)

    # The source-bound device grant is an opaque ros_ing token, not the
    # pairing JWT whose `iss` the standalone tap can inspect. Pin the same
    # API origin used for authorization so the unified tap never falls back
    # to a guessed production host (and self-hosted Codex/pi keep working).
    config_path = state_dir / ".config"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        config = {}
    if not isinstance(config, dict):
        config = {}
    config["api_base_url"] = base_url.rstrip("/")
    config_tmp = state_dir / ".config.tmp"
    config_tmp.write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(config_tmp, config_path)


def write_capture_credential(source: str, token: str, base_url: str) -> None:
    """Where `authorize` would put one agent's capture credential. claude_code:
    the CLI config's `ingest_token` (its hooks read that); every other agent:
    its tap folder's `.token` (`write_paired_capture_token`). Raises OSError."""
    if source == "claude_code":
        from probe.sdk.config import save_context

        save_context({"ingest_token": token})
        return
    write_paired_capture_token(source, token, base_url)


def authorize(
    grants: list[str],
    *,
    base_url: str,
    capture_sources: list[str] | None = None,
    defer_capture_sources: Iterable[str] | None = None,
    client_context: dict | None = None,
    on_prompt=None,
    open_browser: bool = True,
    install_code: str | None = None,
    minted: dict | None = None,
    allow_browser_approval: bool = True,
) -> tuple[dict[str, dict], list[str]]:
    """Run ONE browser approval covering everything the user ticked, and persist
    every credential it mints.

    `minted` is an answer already in hand, in the approval exchange's shape
    (`mint_from_sign_in`): no browser, the same persistence.

    This is the step that makes the whole feature true. Computing the grant set
    and then telling the user to go run `probe login` would leave them with a
    PAT and no capture credential -- capture would still be off after a setup
    that said it turned it on.

    All three credentials go into a single `save_context` write: it is one
    locked read-modify-write, so a partial failure cannot leave the config with
    a PAT but no ingest token (which reads as "logged in, capture silently
    off"). `ingest_token` is exactly where the uploader looks.

    Wizard entry passes `defer_capture_sources` for new capture grants: store
    them disabled until installation is confirmed. Existing disabled markers
    are preserved, and a declined authorization writes no marker.
    """
    from probe.sdk.config import resolve, save_context
    from probe.sdk.device import (
        DeviceLoginError,
        OnboardingRequired,
        capture_credentials_by_source,
        credentials_by_grant,
        device_authorize,
    )

    if not grants:
        return {}, []

    # Recorder callers explicitly forbid device approval. Configure/repair
    # can need capture alone, so the remaining grants cannot identify a switch.
    if minted is None and install_code is None and not allow_browser_approval:
        return {}, ["Couldn't prepare recording with this Mac's saved sign-in. Refresh your account and try again."]

    try:
        source = agent_source()
        requested_sources = list(dict.fromkeys(capture_sources or [source]))
        source_args = {}
        if "capture" in grants:
            source_args = (
                {"capture_source": requested_sources[0]}
                if len(requested_sources) == 1
                else {"capture_sources": requested_sources}
            )
        if minted is None:
            minted = device_authorize(
                base_url,
                grants=grants,
                **source_args,
                client_context=client_context,
                on_prompt=on_prompt,
                open_browser=open_browser,
                **({"install_code": install_code} if install_code is not None else {}),
            )
    except OnboardingRequired:
        raise
    except DeviceLoginError as exc:
        label = "sign-in" if install_code is not None else "browser approval"
        return {}, [f"{label} failed: {exc}"]

    by_grant = credentials_by_grant(minted)
    captures = capture_credentials_by_source(minted)
    raw_capture_entries = [
        entry for entry in (minted.get("grants") or []) if entry.get("grant") == "capture"
    ]
    if (
        len(requested_sources) == 1
        and len(raw_capture_entries) == 1
        and not raw_capture_entries[0].get("capture_source")
    ):
        # A single-source backend predating the response discriminator is still
        # unambiguous because the request carried exactly one source.
        captures = {requested_sources[0]: raw_capture_entries[0]}
    if captures:
        by_grant["capture"] = next(iter(captures.values()))
    messages: list[str] = []

    updates: dict[str, str | None] = {"base_url": resolve(base_url=base_url).base_url}
    if "api" in by_grant:
        updates["token"] = by_grant["api"]["token"]
    if "mcp" in by_grant:
        updates["mcp_token"] = by_grant["mcp"]["token"]
    if COMPANION_GRANT in by_grant:
        updates["companion_token"] = by_grant[COMPANION_GRANT]["token"]
    if "claude_code" in captures:
        updates["ingest_token"] = captures["claude_code"]["token"]

    try:
        if defer_capture_sources is not None:
            deferred = set(defer_capture_sources) & captures.keys()
            if "claude_code" in captures and not capture_token_sources("claude_code"):
                # The new Claude Code token lands in the shared CLI config, which
                # Claude Code's hooks read. Keep it off until the install is
                # confirmed, even if this sign-in did not select it explicitly.
                # No other agent reads that token, so no other agent is deferred.
                deferred.add("claude_code")
            for deferred_source in sorted(deferred):
                state_dir = tap_plugin_dir(deferred_source)
                state_dir.mkdir(parents=True, exist_ok=True)
                marker = state_dir / ".disabled"
                if not marker.exists():
                    marker.write_text(AWAITING_CONFIRMATION)
        # The markers precede every credential write: an installed hook must
        # never observe a new capture token before the install was confirmed.
        save_context(updates)
    except OSError as exc:
        # The mint SUCCEEDED and the disk write did not: without this the
        # wizard died in a traceback while a live token it never stored sat
        # orphaned server-side. Report it as the failure it is — the caller's
        # grant gating then refuses the installs — and name the cleanup.
        return {}, [
            f"! could not save the minted credentials ({exc}).",
            "  Revoke this device's new token under Settings › Connected clients, "
            "fix the config path, and re-run.",
        ]
    if updates.get("token"):
        _record_login_account(updates["base_url"], updates["token"], updates.get("ingest_token"))

    if install_code is not None:
        # The website code explicitly selects this account. An inherited
        # credential must not keep the current wizard (or its subprocesses)
        # using the old account after a successful exchange. Drop only the
        # overrides for credentials we actually saved, in THIS process; the
        # parent shell retains its environment and needs the instruction below.
        overridden = []
        for field, variable in (
            ("token", "PROBE_TOKEN"),
            ("mcp_token", "PROBE_MCP_TOKEN"),
            ("ingest_token", "PROBE_INGEST_TOKEN"),
        ):
            saved = updates.get(field)
            inherited = os.environ.get(variable)
            if saved and inherited and inherited != saved:
                os.environ.pop(variable, None)
                overridden.append(variable)
        if overridden:
            messages.append(
                "This wizard uses the account selected by the website code. "
                f"Run `unset {' '.join(overridden)}` in your shell before future Probe commands."
            )

    # CODEX HOLDS ITS OWN COPY OF THE READ TOKEN, so the mint above is only half
    # the rotation. Claude Code reads the current token at connect time through
    # its headers helper and needs nothing here; Codex has no credential-helper
    # hook, so its token is a STATIC copy in ~/.codex/config.toml. Leaving that
    # copy behind is not merely stale — `revoke_replaced_token` releases the
    # credential it names — so every Codex call 401s while `codex mcp list`
    # still reports `bearer_token` and `probe doctor` stays green.
    #
    # Here rather than in the callers: sign_in and the guided install both mint
    # through this function, and hooking one of them is how the other keeps the
    # dead token. Costs nothing on a machine with no Codex entry —
    # `configured_bearer` returns None from a file read and the sync returns
    # before it shells out to `codex mcp list`.
    if "mcp" in by_grant:
        messages.extend(sync_mcp_token())

    # Every captured source EXCEPT claude_code needs its token written
    # straight into its own tap plugin dir: claude_code alone can fall back to
    # the probe CLI's config.json `ingest_token` (set above), and every other
    # source is excluded from that fallback (tap/config.py::load_token(),
    # capabilities.consumes_cli_capture_token), so its `.token` file is its
    # ONLY path.
    # A loop over `captures`, not a per-source branch: that is what silently
    # left pi's token nowhere on disk once pi became a real capture source --
    # see AGENT_LABELS' docstring for the same failure mode in the
    # confirmation label below.
    for paired_source, credential in captures.items():
        if paired_source == "claude_code":
            continue
        write_paired_capture_token(paired_source, credential["token"], base_url)

    for grant in grants:
        if grant not in by_grant:
            # Approved, but the backend minted nothing for it. Say so rather
            # than reporting a capability that will not work.
            messages.append(
                f"! the server did not return a '{grant}' credential — "
                "that capability is NOT active"
            )
    if "capture" in grants:
        missing_sources = [source for source in requested_sources if source not in captures]
        if missing_sources:
            by_grant.pop("capture", None)
            messages.append(
                "! the server did not return capture credentials for "
                f"{', '.join(missing_sources)} — those agents are NOT active"
            )
        for paired_source, credential in captures.items():
            label = agent_label(paired_source)
            messages.append(
                f"{label} Session capture paired (device {credential.get('device_id', '?')})."
            )
    return by_grant, messages


def leftover_team_note(caps: Capabilities) -> bool:
    """A team-note block with no pointer beside it: what an opt-out left before
    the opt-out removed both. `agent_rules_installed` reads only the pointer,
    so without this an explicit `--no-agent-rules` found nothing to change."""
    return not caps.agent_rules_installed and agent_rules.has_block(
        agent_rules.memory_path(caps.agent_source), agent_rules.NOTE_BLOCK
    )


def plan(caps: Capabilities, selection: Selection) -> list[str]:
    """A human-readable diff of what this run will change. Printed before
    anything is touched, so `--yes` in CI still leaves an audit trail."""
    steps: list[str] = []
    current = caps.enabled()
    wanted = selection.as_map()
    for capability, want in wanted.items():
        if selection.keeps(capability):
            continue
        have = current[capability]
        if want == have:
            # Capture's runtime switch intentionally describes credential +
            # killswitch state, independently of plugin installation. A direct
            # `codex plugin remove` therefore leaves capture_on=True while the
            # hook that starts the uploader is absent. Keep that independence,
            # but make the manager plan the missing install explicitly.
            if capability is Capability.CAPTURE and want and not caps.capture_plugin_installed:
                steps.append(f"enable {PLAN_LABELS[capability]}")
                continue
            # A STALE block is installed-and-wrong, so want == have and this
            # loop skipped it -- plan() came back empty, the caller returned
            # "Nothing to change", and the refresh branch below it never ran.
            # `probe doctor` meanwhile said "outdated wording -- re-run
            # 'probe wizard'", so the two commands sent the user in a circle
            # and a POINTER_VERSION bump could never reach a machine at all.
            if capability is Capability.AGENT_RULES and want and caps.agent_rules_stale:
                steps.append(f"refresh {PLAN_LABELS[capability]}")
            elif capability is Capability.AGENT_RULES and want and statusline_catch_up_due(caps.agent_source):
                # Same trap as the stale block: rules current, so nothing here
                # would run the step that writes Kimi Code's footer.
                steps.append(f"add Probe's state to {agent_label(caps.agent_source)}'s status line")
            elif capability is Capability.AGENT_RULES and not want and leftover_team_note(caps):
                steps.append(f"disable {PLAN_LABELS[capability]}")
            continue
        label = PLAN_LABELS[capability]
        if not want:
            steps.append(f"disable {label}")
            continue
        # "enable X" when the plugin is ALREADY there and only the credential
        # is missing describes work this run will not do -- and it is the
        # common first-run case, because `capture_on` is credential-only and
        # `tracking_on` is plugin AND login. Name the piece that is actually
        # absent instead.
        plugin_here = {
            Capability.TRACKING: caps.tracking_plugin_installed,
            Capability.CAPTURE: caps.capture_plugin_installed,
        }.get(capability)
        if plugin_here is True:
            steps.append(SIGN_IN_LABELS.get(capability, f"enable {label}"))
        else:
            steps.append(f"enable {label}")
    return steps


#: Per-source label for the thing `apply_capture` installs, used only in its
#: own failure message. NOT the same name in every case: claude_code and
#: codex both install through the marketplace under a "tap" plugin name
#: (`TAP_PLUGIN_NAME`/`CODEX_TAP_PLUGIN_NAME` -- currently the same string,
#: see capabilities.py), while pi installs ONE package
#: (`pi_config.PACKAGE_NAME`) that bundles capture with the tracking skills
#: and MCP bridge -- there is no separate "tap" plugin for pi to name. A
#: table, never a ternary: see `apply_capture`'s own comment on the shape
#: this replaces.
CAPTURE_PLUGIN_LABEL: dict[str, str] = {
    "claude_code": TAP_PLUGIN_NAME,
    "codex": CODEX_TAP_PLUGIN_NAME,
    "pi": pi_config.PACKAGE_NAME,
    "kimi_code": TAP_PLUGIN_NAME,
}


def apply_capture(caps: Capabilities, want: bool, *, mode: OffMode, on_retry=None) -> list[str]:
    """Bring capture to `want` and report honestly.

    Turning it OFF goes through the verified postcondition in capture.py rather
    than deleting a file and hoping.
    """
    messages: list[str] = []
    if want:
        # Two INDEPENDENT jobs, and conflating them is a bug in both directions.
        # Clearing the killswitch is what actually turns capture back on for a
        # machine that already has the plugin; installing is only needed when
        # the plugin is absent. Gating the whole step on "plugin absent" (which
        # this function's caller briefly did) left `.disabled` in place while
        # the wizard reported success -- capture silently off after we said on.
        # Gating it on "capture off" instead reinstalls a plugin that is already
        # there. So: always clear, install only when missing.
        clear_killswitch()
        if caps.agent_source == "codex" and caps.legacy_capture_plugin_installed:
            retired = plugin_cli.uninstall("codex", LEGACY_CODEX_TAP_PLUGIN_ID)
            if not retired.ok:
                messages.append(
                    "could not remove the legacy Codex capture plugin "
                    f"{LEGACY_CODEX_TAP_PLUGIN_ID}: {retired.detail}"
                )
                return messages
            messages.append(
                f"Removed legacy {LEGACY_CODEX_TAP_PLUGIN_ID}; the unified tap owns capture now."
            )
        if caps.capture_plugin_installed:
            return messages
        # Table, not a ternary: `CODEX_TAP_PLUGIN_NAME if agent_source ==
        # "codex" else TAP_PLUGIN_NAME` was the exact banned two-way shape --
        # correct only while there were exactly two sources, silently wrong
        # (claude_code's name) for pi the moment it became a third. pi is
        # installable now (see INSTALLABLE_AGENT_SOURCES), so this label is
        # no longer cosmetic: it is the name `install_plugin` reports on
        # failure, and pi has its own package, not claude_code's tap name.
        tap_name = CAPTURE_PLUGIN_LABEL[caps.agent_source]
        result = install_plugin(tap_name, source=caps.agent_source, on_retry=on_retry)
        if not result.ok:
            messages.append(f"could not install {tap_name}: {result.detail}")
        return messages
    if not caps.capture_on and not caps.capture_token_sources:
        return messages
    result = turn_off(mode)
    messages.append(result.summary())
    messages.extend(f"! {warning}" for warning in result.warnings)
    return messages


def apply_tracking(want: bool, *, on_retry=None, keep_capture: bool | None = None) -> list[str]:
    """Bring tracking to `want`.

    Turning it off removes the plugin but deliberately does NOT revoke the PAT
    or log the CLI out: the wizard is not a logout command, and silently
    destroying a credential the user may be scripting against would be a nasty
    surprise. `probe logout` remains the explicit way to do that.

    pi carries both halves in one package: off keeps the package while capture
    stays (`keep_capture`, the run's selection; unknown reads the device), and
    the extension switches tracking off itself (0.4.0+, updated first).
    """
    messages: list[str] = []
    # The profile's plugin (`probe-research-daemon` where the daemon records),
    # so a re-run of the install never puts the other profile's plugin back.
    name = tracking_plugin_name()
    selected = agent_source()
    pi = _current_harness().lean_profile == LEAN_SETTINGS_FILTER  # one package, both halves
    capture_stays = (_settings_capture_on(selected) if keep_capture is None else keep_capture) if pi else False
    if pi and not want and capture_stays:
        ready = _settings_tracking_ready()
        if not ready.ok:
            return [f"! pi keeps Probe's tracking on: {ready.detail}"]
    if want:
        result = install_plugin(name, on_retry=on_retry)
        if result.ok and pi:
            # An existing entry may carry tracking-off: switch it back on.
            result = pi_config.set_tracking(True, daemon=daemon_records(selected))
        if not result.ok:
            messages.append(f"could not install {name}: {result.detail}")
        else:
            messages.extend(_apply_root_skills(selected, name))
        return [*messages, *(_pi_project_override(want=True) if pi else [])]
    result = uninstall_plugin(name, keep_capture=capture_stays) if pi else uninstall_plugin(name)
    if result.ok:
        # The plugin is the skills' source; with it gone they must go too, or the
        # agent keeps naming a skill whose plugin no longer exists.
        messages.extend(remove_root_skills(selected))
    if not result.ok:
        messages.append(f"could not uninstall {name}: {result.detail}")
    elif pi and capture_stays:
        messages.append("Probe's tracking is off in pi; session capture keeps running. You are still signed in.")
    else:
        messages.append(
            "Removed the tracking plugin. You are still signed in."
        )
    return [*messages, *(_pi_project_override(want=False) if pi else [])]


def _pi_project_override(*, want: bool) -> list[str]:
    """The wizard writes pi's GLOBAL entry; a project entry in this folder wins
    over it (pi's merge rule). Say so instead of editing someone's project file."""
    merged = pi_config.merged_package_entry(cwd=Path.cwd())
    if merged.scope != "project" or not merged.installed:
        return []
    if merged.tracking_off == (not want):
        return []
    project = pi_config.project_settings_path(Path.cwd())
    state = "on" if want is False else "off"
    return [f"! {project} keeps Probe's tracking {state} in this folder (pi lets a project entry win); "
            f"edit or remove its probe-research-pi entry to match."]


def agent_profile(source: str | None = None) -> "agent_rules.Profile":
    """The instruction-block profile of this coding agent: DAEMON where its
    "Who records" is the daemon (`session_marker.recorder`), else AGENT."""
    from probe.sdk import session_marker

    try:
        daemon = session_marker.recorder(source or agent_source()) == session_marker.RECORDER_DAEMON
    except Exception:  # noqa: BLE001 - an unreadable config is today's profile
        daemon = False
    return agent_rules.Profile.DAEMON if daemon else agent_rules.Profile.AGENT


def daemon_records(source: str | None = None) -> bool:
    """Is this coding agent on the daemon profile (the daemon records and reads)?"""
    return agent_profile(source) is agent_rules.Profile.DAEMON


#: How the "Who records" row names its two positions.
RECORDER_WORDS: dict[str, str] = {"agent": "the agent", "daemon": "the daemon"}

#: The coding agents with a daemon profile: every registry row that names how
#: it gets one (`lean_profile`: a second plugin for Claude Code and Codex, the
#: package's settings entry for pi).
RECORDER_SOURCES: tuple[str, ...] = tuple(h.id for h in _installable_rows() if h.lean_profile)
#: A harness whose daemon profile is its package's settings entry (pi).
LEAN_SETTINGS_FILTER = "settings-filter"


def live_daemon_sessions() -> int:
    """How many sessions the daemon records for (the lean plugin's `<sid>.profile`
    mark) have a worker running right now."""
    from probe.daemon import mailbox
    from probe.sdk import session_marker

    try:
        marks = list(session_marker.sessions_dir().glob("*.profile"))
    except OSError:
        return 0
    live = 0
    for mark in marks:
        try:
            if mark.read_text(encoding="utf-8").strip() != session_marker.RECORDER_DAEMON:
                continue
        except OSError:
            continue
        if mailbox.worker_alive(mark.name[: -len(".profile")]):
            live += 1
    return live


def revoke_companion(base_url: str) -> list[str]:
    """Release the Probe daemon's key and forget it. Best-effort, like every revoke."""
    from probe.sdk.config import load_context, save_context

    token = str((load_context() or {}).get("companion_token") or "")
    if not token:
        return []
    lines = _revoke(token, base_url=base_url, what="the Probe daemon's key")
    save_context({"companion_token": None})
    return lines


def _forget_recorder(source: str) -> list[str]:
    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    try:
        session_marker.write_recorder(source, session_marker.RECORDER_AGENT)
    except (OSError, ValueError, ConfigUnreadable) as exc:
        return [f"! could not reset who records in {agent_label(source)}: {exc}"]
    return []


def _instruction_file_lock(path):
    """The lock the team-note sync holds while it reads and writes `path`.

    The wizard's own writes take it too: otherwise a sync that read the pointer
    as present could write the note back the moment after an opt-out removed
    both, and report nothing.
    """
    from probe.cli.team_note_file import instruction_lock_path
    from probe.sdk.durable import file_lock

    return file_lock(instruction_lock_path(path))


def apply_recorder_rules(source: str, value: str, rules: bool | None = None) -> list[str]:
    """The instruction block of `value`'s profile, for ONE agent's file.

    An existing block is swapped and an absent one stays absent. Absent IS the
    opt-out (`--no-agent-rules` leaves no other trace), so writing the daemon's
    blurb unasked put Probe back in the global CLAUDE.md / AGENTS.md of a machine
    that had declined it -- a customer's, on 2026-10-02. `rules` is
    `--agent-rules/--no-agent-rules` passed beside `--who-records`: True writes
    the profile's block, False removes every Probe block.
    """
    from probe.sdk import session_marker

    path = agent_rules.memory_path(source)
    profile = (
        agent_rules.Profile.DAEMON if value == session_marker.RECORDER_DAEMON else agent_rules.Profile.AGENT
    )
    try:
        with _instruction_file_lock(path):
            if rules is None and not agent_rules.is_installed(path):
                return []  # opted out, and no flag says otherwise
            if rules is not False:
                agent_rules.install(path, block=agent_rules.render_block(profile=profile))
            elif agent_rules.remove_all(path):
                return [f"Removed the Probe block from {short_path(path)}."]
    except agent_rules.DamagedBlock as exc:
        return [f"! left {short_path(path)} alone: {exc}"]
    except (OSError, UnicodeDecodeError) as exc:
        return [f"! could not update {short_path(path)}: {exc}"]
    return []


def remove_root_skills(source: str) -> list[str]:
    """Prune Probe's skills when no plugin is left to do it.

    A researcher who removes the plugin with `/plugin uninstall` leaves no hook
    behind, so the copies in their own skills folder would never be refreshed or
    removed again. Marker-bearing folders only, as everywhere else.
    """
    try:
        return root_skills.remove(source)
    except OSError as exc:
        return [f"! could not remove Probe's skills: {exc}"]


def _apply_root_skills(source: str, plugin: str) -> list[str]:
    """Put the installed plugin's skills in the agent's own skills folder.

    Claude Code only (the capability gates it); every other harness reads the
    plugin's `agent-skills/` by manifest key and gets an empty list here. The
    plugin stays the source: `root_skills_sync.py` on SessionStart keeps the
    copies current, and this is the same work done at the moment of install so
    the researcher does not have to start a second session to get their skills.
    """
    try:
        return root_skills.apply(source, root_skills.installed_plugin_root(plugin), prefer=plugin)
    except OSError as exc:
        # Fail-open, the contract every other step in this wizard follows and
        # the one the hook already had: an unwritable skills folder reported a
        # PermissionError out of `apply_recorder` AFTER the new plugin was
        # installed and BEFORE `write_recorder`, leaving both plugins present
        # and the setting unwritten, with no message saying so.
        return [f"! could not install Probe's skills: {exc}"]


@dataclass
class _Ready:
    ok: bool
    lines: list[str]


def needs_capture_pairing(source: str) -> bool:
    """A settings-entry daemon profile (pi) whose agent holds no capture token
    of its own yet: the switch pairs it first (`pair_capture`), OUTSIDE the
    switch's spinner, because the approval prints a link to open."""
    from probe.harness import get_registry

    harness = get_registry().get(source)
    return harness.lean_profile == LEAN_SETTINGS_FILTER and not capture_token_sources(source)


def mint_from_sign_in(grant: str, *, base_url: str, source: str | None = None) -> dict | None:
    """The daemon's key (`COMPANION_GRANT`) or one agent's capture key
    (`"capture"`, with `source`), minted with this device's sign-in -- its
    installation `api` credential -- and no browser (Richard 2026-10-26: "just
    reuse the auth token already signed into").

    Callers mint this way only once a person saw the daemon's consent on this
    run; a run nobody watches keeps the browser approval, which shows it.

    Answers in the approval exchange's shape (`{"grants": [entry]}`), for
    `authorize(..., minted=)` to persist exactly as a browser approval's. None
    when this device cannot: no saved sign-in, a `PROBE_TOKEN` in the
    environment naming another credential (the key would be saved beside the
    wrong account), a sign-in the server will not mint from (not this
    installation's, another machine's, an older server without the route), or
    an answer that is not one. The caller then opens the browser approval as
    before. A send that fails is retried ONCE: each mint frees the slot of the
    key before it, so a key whose answer was lost dies with the retry rather
    than staying live and unheld.
    """
    from probe.sdk import errors
    from probe.sdk.client import Client
    from probe.sdk.config import load_context, resolve
    from probe.sdk.surface import Surface

    settings = resolve(base_url=base_url)
    try:
        saved = str((load_context() or {}).get("token") or "")
    except Exception:  # noqa: BLE001 - an unreadable config holds no sign-in
        return None
    inherited = os.environ.get("PROBE_TOKEN")
    if not saved or (inherited and inherited != saved):
        return None
    for _attempt in range(2):
        try:
            with Client(
                base_url=settings.base_url,
                token=saved,
                fail_open=False,
                async_writes=False,
                surface=Surface.CLI.value,
            ) as client:
                entry = (
                    client.mint_capture_credential(source or agent_source())
                    if grant == "capture"
                    else client.mint_companion_credential()
                )
        except (errors.TransportError, errors.ServerError):
            continue
        except (errors.RosError, ValueError):  # a refusal, or a 2xx that is not JSON (a proxy)
            return None
        if isinstance(entry, dict) and entry.get("grant") == grant and entry.get("token"):
            return {"grants": [entry]}
        return None
    return None


def pair_capture(source: str, *, base_url: str, open_browser: bool = True, sign_in: bool = False) -> list[str]:
    """This agent's capture key alone (nothing else is re-minted): from this
    device's sign-in when `sign_in` (the caller showed the daemon's consent;
    `mint_from_sign_in`), else one browser approval. The person chose the
    daemon, which records from capture, so a leftover sign-in marker in the
    agent's folder goes too."""
    from probe.cli.capabilities import agent_target
    from probe.cli.capture import clear_stray_pi_killswitch
    from probe._shared.telemetry import DESKTOP_HUMAN_ENV

    desktop = os.environ.get(DESKTOP_HUMAN_ENV) == "1"

    label = agent_label(source)
    lines = [f"Pairing {label}'s session capture (the daemon records from it)."]
    try:
        _grants, messages = authorize(
            ["capture"],
            base_url=base_url,
            capture_sources=[source],
            open_browser=open_browser,
            minted=mint_from_sign_in("capture", base_url=base_url, source=source) if sign_in or desktop else None,
            allow_browser_approval=not desktop,
        )
        lines.extend(messages)
    except Exception as exc:  # noqa: BLE001 - every failure reads as "not paired" in apply_recorder
        lines.append(f"! pairing {label}'s capture did not finish: {exc}")
        return lines
    if capture_token_sources(source):
        with agent_target(source):
            clear_stray_pi_killswitch()
        lines.append(f"{label} capture paired.")
    return lines


def daemon_package_ready(source: str) -> _Ready:
    """A settings-entry daemon profile's package (pi's) is new enough to run the
    daemon profile (`pi_config.DAEMON_MIN_PACKAGE_VERSION`), updating it first
    (`pi update <source>`) when it is not. An older extension ignores the
    profile and would connect the Probe MCP in a daemon session.

    The wizard asks this BEFORE pairing (`pair_capture`): pairing mints the
    agent's own capture token, and a switch that then stopped here would leave
    the agent capturing on agent, which it did not do before.
    """
    from probe.cli import pi_config

    label = agent_label(source)
    lines: list[str] = []
    minimum = pi_config.DAEMON_MIN_PACKAGE_VERSION
    want = ".".join(str(part) for part in minimum)
    version = pi_config.installed_package_version()
    if version is None or version < minimum:
        updated = pi_config.update_package()
        version = pi_config.installed_package_version()
        if version is None or version < minimum:
            have = ".".join(str(part) for part in version) if version else "unknown"
            why = "" if updated.ok else f" ({updated.detail})"
            return _Ready(False, [*lines, f"! {label} stays on agent: its Probe package is {have}, the daemon needs "
                                  f"{want} or newer{why}. Run `pi update {pi_config.MIRROR_GIT_SOURCE}`, "
                                  "then switch Who records again."])
        lines.append(f"{label}'s Probe package updated to {'.'.join(str(part) for part in version)}.")
    return _Ready(True, lines)


def _settings_tracking_ready() -> claude_cli.Result:
    """pi's package is new enough to honour tracking-off
    (`pi_config.TRACKING_OFF_MIN_PACKAGE_VERSION`), updating it first
    (`pi update <source>`) when it is not. An older extension ignores
    `probeTracking` and keeps bridging Probe's MCP, so the status would read
    "off" while pi still served it."""
    floor = pi_config.TRACKING_OFF_MIN_PACKAGE_VERSION
    want = ".".join(str(part) for part in floor)
    version = pi_config.installed_package_version()
    if version is None or version < floor:
        pi_config.update_package()
        version = pi_config.installed_package_version()
    if version is not None and version >= floor:
        return claude_cli.Result(ok=True, detail="")
    have = ".".join(str(part) for part in version) if version else "unknown"
    return claude_cli.Result(
        ok=False,
        detail=f"its Probe package is {have}, and switching tracking off needs {want} or newer. "
        f"Run `pi update {pi_config.MIRROR_GIT_SOURCE}`, then untick tracking again.",
    )


def _settings_profile_ready(source: str, label: str, *, base_url: str) -> _Ready:
    """What a settings-entry daemon profile (pi) needs before it can switch.

    1. The agent's own capture token. The extension starts capture only when
       the agent is paired, and only capture starts the daemon. Since D3 a
       machine signed in for Claude Code holds none for pi; the wizard pairs it
       first (`pair_capture`), and a pairing that did not finish stops here.
    2. A package new enough to run the daemon profile (`daemon_package_ready`).
    """
    if not capture_token_sources(source):
        return _Ready(False, [f"! {label} stays on agent: its session capture is not paired "
                              f"(`probe wizard` › Install Probe › {label} pairs it)."])
    return daemon_package_ready(source)


def apply_recorder(caps: Capabilities, value: str, *, base_url: str, rules: bool | None = None) -> list[str]:
    """Move ONE coding agent to a "Who records" profile (daemon reads).

    `daemon`: the Probe daemon records and reads for this agent. Its key first
    (`provision_daemon`), then the
    capture plugin if missing, then `probe-research-daemon`, then the config
    (`recorder`), the daemon profile's instruction block, the new-session
    default, and only LAST `probe-research` goes -- so up to the last step the
    agent still has a working plugin. `agent` is the reverse, and the daemon's
    key is revoked once no agent on this machine records through it.

    Every step reports its own failure in place. A failure before the config is
    written stops the move with nothing but installs changed; after it, the move
    has happened and what did not follow is named with its fix.
    """
    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    from probe.harness import get_registry

    source = caps.agent_source
    label = agent_label(source)
    if source not in RECORDER_SOURCES:
        return [f"! {label} has no daemon profile yet; left as it is."]
    by_settings = get_registry().get(source).lean_profile == LEAN_SETTINGS_FILTER
    daemon = value == session_marker.RECORDER_DAEMON
    retry = {"left": 1}

    def _may_retry() -> bool:
        if retry["left"]:
            retry["left"] -= 1
            return True
        return False

    stopped = "  Nothing else changed. Switch Who records again to retry."
    lines: list[str] = []
    if daemon:
        from probe.cli.companion import provision_daemon
        from probe.cli.daemon_cli import ai_libraries

        # The wizard's row provisions before its spinner, so this is a no-op
        # there; each half is fetched only when missing (R12).
        if not companion_token_held() or ai_libraries() is None:
            lines.extend(provision_daemon(base_url))
        if not companion_token_held():
            return [*lines, f"! {label} stays on agent: the daemon has no key."]
        if ai_libraries() is None:
            return [*lines, f"! {label} stays on agent: the daemon's AI libraries are missing."]
        if not caps.capture_plugin_installed:
            tap = CAPTURE_PLUGIN_LABEL[source]
            result = install_plugin(tap, source=source, on_retry=_may_retry)
            if not result.ok:
                return [*lines, f"! could not install {tap} for {label}: {result.detail}", stopped]
        if by_settings:
            # The daemon starts only where capture starts (the extension spawns
            # the tap, the tap spawns the daemon), and capture needs the agent's
            # OWN token: nothing falls back to Claude Code's (D3).
            ready = _settings_profile_ready(source, label, base_url=base_url)
            lines.extend(ready.lines)
            if not ready.ok:
                return [*lines, stopped]
        want, drop = DAEMON_PLUGIN_NAME, TRACKING_PLUGIN_NAME
    else:
        want, drop = TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME
    if by_settings:
        from probe.cli import pi_config

        result = pi_config.set_profile(daemon)
        if not result.ok:
            return [*lines, f"! could not switch {label}'s Probe package to the {value} profile: {result.detail}",
                    stopped]
    else:
        result = install_plugin(want, source=source, on_retry=_may_retry)
        if not result.ok:
            return [*lines, f"! could not install {want} for {label}: {result.detail}", stopped]
        # The two profiles ship different skills (8 vs 3). This installs the new
        # plugin's set and prunes the other's: a `track-work` left behind on the
        # daemon profile would have the agent record inline while the daemon
        # records the same session.
        lines.extend(_apply_root_skills(source, want))
    try:
        session_marker.write_recorder(source, value)
    except (OSError, ValueError, ConfigUnreadable) as exc:
        beside = (f"  {label}'s Probe package is already on the {value} profile." if by_settings
                  else f"  {want} is installed beside {drop}.")
        return [*lines, f"! could not record who records in {label}: {exc}", f"{beside} Switch Who records again."]
    lines.append(f"Who records in {label} → {RECORDER_WORDS[value]}")
    if source in reasoning_summaries.SOURCES:
        # The daemon reads the agent's reasoning only where the agent writes its
        # summaries (`reasoning_summaries`): on where the user never chose, and
        # undone on the way back only if Probe was the one who turned it on.
        lines.extend(
            reasoning_summaries.on_for_daemon(source) if daemon else reasoning_summaries.undo_for_agent(source)
        )

    lines.extend(apply_recorder_rules(source, value, rules))

    # The new-session default is MACHINE-wide, so the move to the daemon leaves it
    # alone: the lean plugin starts an `on` session in `daemon` itself, and an
    # agent still on the agent profile keeps recording. Back on the agent
    # profile an old `daemon` default goes back to `on`, unless another agent
    # still records through the daemon.
    others = [s for s in RECORDER_SOURCES if s != source and session_marker.recorder(s) == session_marker.RECORDER_DAEMON]
    current = session_marker.default_session_state()
    target = (
        session_marker.STATE_FULL
        if not daemon and current == session_marker.STATE_DAEMON and not others
        else None
    )
    if target is not None and target != current:
        try:
            session_marker.write_default_state(target)
        except (OSError, ValueError, ConfigUnreadable) as exc:
            lines.append(f"! could not set the Probe default for new sessions: {exc}")
        else:
            lines.append(f"Probe in new sessions → {session_marker.state_label(target)}")

    if not daemon and not others and companion_token_held():
        # Nothing on this machine records through the daemon any more, so its
        # key goes too. This row is the daemon's only consent surface: the
        # tracking default lost its `daemon` position (Richard 2026-09-29). Not
        # under a session the daemon is recording right now: revoking would stop
        # it mid-session, while the plugin swap only reaches new sessions.
        live = live_daemon_sessions()
        if live:
            lines.append(f"Kept the daemon's key: {live} open session(s) still use it. "
                         "Revoke it in the dashboard (Settings › Connected clients) once they end.")
        else:
            lines.extend(revoke_companion(base_url))

    if daemon and source == "codex":
        # The wizard wrote Codex's MCP table itself; left behind, the MCP's tools
        # and instructions would still reach an agent the daemon reads for.
        from probe.cli import codex_config

        try:
            codex_config.remove_mcp_server(TRACKING_PLUGIN_NAME)
        except codex_config.ConfigError as exc:
            lines.append(f"! could not remove the Probe MCP from Codex's config: {exc}")

    # What is installed NOW, not the snapshot the screen was drawn from: another
    # row applied in the same commit may have installed `drop` since.
    from probe.cli.capabilities import installed_plugins

    now = installed_plugins(source=source)
    if not by_settings and (drop in now.names or not now.verified):
        removal = uninstall_plugin(drop, source=source)
        if not removal.ok:
            lines.append(f"! could not remove {drop} for {label}: {removal.detail}")
            lines.append(f"  Both plugins are installed; remove {drop} from {label} by hand.")
    lines.append(f"Takes effect in new {label} sessions.")
    if source == "codex":
        # Codex will not run a hook nobody trusted, and says nothing when it
        # declines: the daemon's messages and answers would never arrive
        # (live Codex test, 2026-09-29). The plugin just swapped in has hook
        # keys of its own, so Probe approves them, and names `/hooks` when that
        # did not take.
        lines.extend(approve_codex_hooks()[0])
    return lines


def _reuse_approval_for_codex_mcp(notes: list[str]) -> bool:
    """Serve Codex the read token the browser approval already minted.

    The approval this run just performed asks for `api` and `mcp` together and
    stores both, so by the time we get here the credential Codex needs is
    already on disk. Sending the user to a second page to mint another one is
    the whole complaint: it is redundant, and it is the step that times out.

    Declines quietly whenever anything is not exactly right -- no token yet, no
    plugin manifest to read the URL from, an unparseable config -- because the
    OAuth flow below still works and a slower install beats a wrong one.
    """
    from probe.sdk.config import load_context

    try:
        token = (load_context() or {}).get("mcp_token")
    except Exception:  # noqa: BLE001 - a config we cannot read is just "no shortcut"
        token = None
    if not token:
        return False

    url = codex_config.plugin_mcp_url(CODEX_MCP_NAME, marketplace=MARKETPLACE)
    if not url:
        return False

    try:
        written = codex_config.write_mcp_bearer(CODEX_MCP_NAME, url=url, token=token)
    except codex_config.ConfigError as exc:
        notes.append(f"! could not reuse your sign-in for the Codex MCP: {exc}")
        return False

    # Ask Codex, rather than trusting that valid TOML is acceptable TOML --
    # `bearer_token` is the standing proof those are different things. A status
    # we cannot read is the same shape as a config Codex cannot load, so the
    # write goes back rather than being left for the fallback to sit on top of.
    if plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME) != codex_config.BEARER_STATUS:
        codex_config.restore(written)
        notes.append(
            "! Codex did not accept the credential from your sign-in; its config is back as it was."
        )
        return False
    return True


def current_mcp_token() -> str | None:
    """The read token this device holds, or None."""
    from probe.sdk.config import load_context

    try:
        return (load_context() or {}).get("mcp_token") or None
    except Exception:  # noqa: BLE001 - an unreadable config is "no token", not a crash
        return None


def _record_login_account(base_url: str | None, token: str, ingest_token: str | None) -> None:
    """Which account the wizard's new login is, as `probe login` records it
    (#2041 round 3): without it, writes queued under this login could not
    follow a later same-account re-login and waited forever. One `/v1/me`,
    5 s, best-effort: the wizard goes on either way."""
    try:
        from probe.sdk.config import Settings, resolve, save_context
        from probe.sdk.journal import _identity_of, credential_fingerprint, record_account

        who = _identity_of(Settings(base_url=base_url or resolve().base_url, token=token))
        if who is None:
            return
        fingerprint = credential_fingerprint(token, ingest_token)
        record_account(fingerprint, who)
        save_context({"identity": {"fingerprint": fingerprint, "customer_id": who[0], "user_id": who[1]}})
    except Exception:  # noqa: BLE001 -- see docstring
        return


def _context_base_url() -> str:
    """The API this device's stored credentials belong to.

    Read from the SAME context as `mcp_token`, which is what makes it the right
    thing to compare the Codex endpoint against: the two values were written by
    one `save_context` call and describe one account.
    """
    from probe.sdk.config import DEFAULT_BASE_URL, load_context

    try:
        return str((load_context() or {}).get("base_url") or DEFAULT_BASE_URL)
    except Exception:  # noqa: BLE001 - an unreadable config is "the default"
        return DEFAULT_BASE_URL


def _same_deployment(mcp_url: str, base_url: str) -> bool:
    """Do a Codex MCP endpoint and an API base URL belong to one deployment?

    NOT a host comparison. Production deliberately splits the two across
    `api.research.prbe.ai` and `mcp.research.prbe.ai`, so equal hosts is the
    wrong test -- it would reject the configuration nearly every user has.
    There is no base_url -> mcp_url derivation anywhere in this codebase to
    borrow instead (the shipped manifests hard-code the endpoint), so the
    reliable signal is the pairing with the SHIPPED DEFAULTS: stock API with
    stock MCP is one deployment, and either half alone crossing to a
    self-hosted counterpart is the case worth refusing.

    KNOWN LIMIT: two self-hosted deployments on one machine are
    indistinguishable here and both read as "not stock", so this returns True.
    Catching that needs a deployment identity we do not record; this covers the
    crossing that involves production, which is the one with a blast radius
    beyond the person who configured it.
    """
    from probe.sdk.config import DEFAULT_BASE_URL

    mcp_is_stock = urlparse(mcp_url).netloc == urlparse(codex_config.PRODUCTION_MCP_URL).netloc
    api_is_stock = urlparse(base_url).netloc == urlparse(DEFAULT_BASE_URL).netloc
    return mcp_is_stock == api_is_stock


def codex_mcp_token_drifted() -> bool:
    """Is Codex holding a read token this device has already replaced?

    The predicate the wizard schedules its repair on. Deliberately independent
    of `agent_source` and of `codex mcp list`: the first is single-valued on a
    machine running both agents, and the second answers `bearer_token` for a
    dead header, so both report "fine" in the state this exists to catch.

    Two file reads, no subprocess, and False whenever there is nothing to
    compare -- no Codex entry, or no token stored here. Safe to call on every
    wizard run.
    """
    try:
        configured = codex_config.configured_bearer(CODEX_MCP_NAME)
    except Exception:  # noqa: BLE001 - an unreadable config is "nothing to say"
        return False
    if configured is None:
        # No static bearer (OAuth): only the workspace-limit copy can drift.
        return _codex_limit_drifted()
    token = current_mcp_token()
    if not token:
        return False
    return (
        configured != token
        or codex_config.needs_header_migration(CODEX_MCP_NAME)
        or _codex_limit_drifted()
    )


def mcp_token_drifted() -> bool:
    """Any agent-held copy of the read token (Codex's config, Kimi Code's
    installed manifest) differs from the one this device holds."""
    from probe.cli import kimi_config

    return codex_mcp_token_drifted() or kimi_config.mcp_bearer_drifted()


def sync_mcp_token() -> list[str]:
    """Re-point EVERY agent-held copy of the read token at the current one:
    Codex's config.toml and Kimi Code's installed manifest. The one call every
    token replacement makes (`authorize()`, `probe mcp token set`, the wizard's
    drift repair), so no copy is left answering 401."""
    from probe.cli import kimi_config

    return [*sync_codex_mcp_token(), *kimi_config.sync_mcp_bearer()]


def sync_codex_mcp_token() -> list[str]:
    """Re-point an existing Codex entry at the CURRENT read token.

    Rotating the credential writes a new `mcp_token` and used to leave Codex
    holding the old one. Nothing noticed: `codex mcp list` reports
    `bearer_token` for any header at all, so the health check stayed green while
    every Codex call 401'd.

    THE ROTATORS ARE `authorize()` AND `probe mcp token set`, and nothing else.
    `probe login` is NOT one of them despite what this docstring said for a
    while: it writes base_url/token/ingest_token/hmac_secret and never touches
    `mcp_token` (see `main.py::login`). Naming it here is how a caller comes to
    believe the login path was already covered.

    Only ever UPDATES an entry that already exists. Creating one is an install
    decision -- it needs the plugin's URL and a verification step -- and
    `probe mcp token set` on a machine that never set up Codex must stay a
    no-op.
    """
    if daemon_records("codex"):
        # The daemon profile gives Codex no MCP: `apply_recorder` removed the
        # table, and re-running the wizard must not bring it back.
        return []
    token = current_mcp_token()
    try:
        configured = codex_config.configured_bearer(CODEX_MCP_NAME)
    except Exception:  # noqa: BLE001
        return []
    if configured is None:
        # No static bearer: an install Codex authenticates itself (OAuth), or no
        # entry at all. The workspace limit must still reach the first.
        return _sync_codex_limit_only()
    if not token:
        return []
    # A ROTATION is not the only reason to rewrite. `write_mcp_bearer` replaces
    # the whole table, so a shape change (the agent-session header) reaches an
    # install only when something calls it -- and an install whose token never
    # rotates would otherwise keep the old table forever.
    stale_shape = codex_config.needs_header_migration(CODEX_MCP_NAME)
    # And a third: this computer's workspace limit, copied into the same table,
    # changed (`probe workspace limit`). The copy must follow it, as the bearer does.
    stale_limit = _codex_limit_drifted()
    if configured is None or (configured == token and not stale_shape and not stale_limit):
        return []

    url = codex_config.plugin_mcp_url(CODEX_MCP_NAME, marketplace=MARKETPLACE)
    if not url:
        return []
    # THE TOKEN AND THE URL COME FROM DIFFERENT PLACES, so they can disagree
    # about which deployment they belong to. `write_mcp_bearer` writes both in
    # one table, and Codex then sends this token to that URL on every connect --
    # so a mismatch hands a live read credential to a server it was not minted
    # for. Silent, and now automatic on every sign-in rather than only on
    # `probe mcp token set`.
    if not _same_deployment(url, _context_base_url()):
        return [
            "! Codex's Probe MCP points at a different deployment than this account; "
            "its token was left alone. Run Install Probe again to fix it."
        ]
    try:
        written = codex_config.write_mcp_bearer(CODEX_MCP_NAME, url=url, token=token)
    except codex_config.ConfigError as exc:
        return [f"! Codex is still using the previous read token: {exc}"]
    if plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME) != codex_config.BEARER_STATUS:
        codex_config.restore(written)
        return ["! could not update the Codex MCP token; its config is back as it was."]
    if configured == token and stale_limit and not stale_shape:
        return ["Codex MCP updated to this computer's workspace limit (restart Codex to load it)."]
    if configured == token:
        return ["Codex MCP config updated so agent sessions are identified."]
    return ["Codex MCP updated to your current read token."]


#: Said whenever this computer is limited while Codex reads Probe through the
#: PLUGIN's own MCP declaration (OAuth, no user-level table). A user-level
#: `[mcp_servers.<name>]` table OVERRIDES the plugin's entry rather than merging
#: with it (`codex_config`, verified on codex-cli 0.147.0), so writing one only to
#: carry the limit would drop the OAuth sign-in it rides on. The safe choice is to
#: leave that connection working and unlimited, and to say how to limit it: signed
#: out, the wizard gives Codex this computer's key, with the limit beside it.
CODEX_UNLIMITED_NOTICE = (
    f"! Codex's Probe MCP signs in with its own OAuth login, so this computer's workspace limit "
    f"cannot ride it and Codex still reads the whole team. To limit it: `codex mcp logout "
    f"{CODEX_MCP_NAME}`, then re-run the Probe wizard (`probe wizard`)."
)


def _sync_codex_limit_only() -> list[str]:
    """Bring the workspace-limit headers of a Codex entry with NO static bearer
    (`codex mcp login`) in step with the Probe config: those headers only, the
    rest of the table untouched. Undone when Codex's own view of its login moves.

    With no user-level table at all -- the plugin's own OAuth declaration -- nothing
    is written (it would shadow that sign-in): while limited, CODEX_UNLIMITED_NOTICE."""
    from probe.sdk.workspace_limit import stored_headers

    url = codex_config.plugin_mcp_url(CODEX_MCP_NAME, marketplace=MARKETPLACE)
    if not url or not _same_deployment(url, _context_base_url()):
        # A limit is one deployment's workspace: never sent to another's MCP.
        return []
    if codex_config.configured_limit_headers(CODEX_MCP_NAME) is None:
        return [CODEX_UNLIMITED_NOTICE] if stored_headers() else []
    if not _codex_limit_drifted():
        return []

    before = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
    try:
        written = codex_config.write_limit_headers(CODEX_MCP_NAME, stored_headers())
    except codex_config.ConfigError as exc:
        return [f"! Codex's Probe MCP keeps its previous workspace limit: {exc}"]
    if written.changed and plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME) != before:
        codex_config.restore(written)
        return ["! could not update the Codex MCP's workspace limit; its config is back as it was."]
    return ["Codex MCP updated to this computer's workspace limit (restart Codex to load it)."] if written.changed else []


def _codex_limit_drifted() -> bool:
    """Codex's table carries other workspace-limit headers than the Probe config
    stores now. False when there is nothing to compare."""
    from probe.sdk.workspace_limit import stored_headers

    try:
        configured = codex_config.configured_limit_headers(CODEX_MCP_NAME)
        return configured is not None and configured != stored_headers()
    except Exception:  # noqa: BLE001 - an unreadable config is "nothing to say"
        return False


def apply_codex_mcp_auth() -> list[str]:
    """Authorize the Codex-hosted MCP, reusing this run's approval if it can."""
    status = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
    if status == codex_config.BEARER_STATUS:
        # Authenticated with a header -- but Codex cannot say WHICH token, so a
        # re-run after a rotation has to check rather than assume.
        return sync_codex_mcp_token()
    if status == "o_auth":
        return []

    notes: list[str] = []
    if _reuse_approval_for_codex_mcp(notes):
        return [*notes, "Codex MCP authorized from your Probe sign-in."]

    result = plugin_cli.login_codex_mcp(CODEX_MCP_NAME)
    if not result.ok:
        return [
            *notes,
            f"could not log in to the {CODEX_MCP_NAME} MCP: {result.detail}. "
            f"Run `codex mcp login {CODEX_MCP_NAME}` and then re-run `probe doctor`.",
        ]
    verified = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
    if verified not in {"o_auth", "bearer_token"}:
        return [
            *notes,
            f"! Codex completed the login command but {CODEX_MCP_NAME} still reports "
            f"{verified or 'unknown'}; run `codex mcp login {CODEX_MCP_NAME}` again.",
        ]
    return [*notes, f"Codex MCP logged in ({CODEX_MCP_NAME})."]


def codex_hooks_waiting() -> bool:
    """Probe's plugins are in Codex and some of their hooks wait for an approval
    Probe may give (`codex_hooks.waiting`, `approve`'s own rule). Asks Codex
    (one app-server start, ~0.2s, at most STATUS_TIMEOUT_S) only where a Probe
    plugin copy is in Codex's cache."""
    from probe.cli import codex_hooks

    try:
        if not codex_hooks.installed_copies():
            return False
        return codex_hooks.waiting(timeout=codex_hooks.STATUS_TIMEOUT_S)
    except Exception:  # noqa: BLE001 - a question asked before the plan never fails it
        return False


def approve_codex_hooks(only: frozenset[str] | None = None) -> tuple[list[str], bool]:
    """Approve Probe's own hooks in Codex, so they run without a trip to `/hooks`:
    (lines to show, whether none of Probe's hooks waits for approval now).

    Codex skips a plugin's hook until it is approved and says nothing in the
    session, so a fresh install recorded nothing until the person found `/hooks`
    (and T3 Code, which drives Codex, has no `/hooks` at all). Only Probe's own
    plugins' hooks are approved (`codex_hooks.approvable`). Never a failure line:
    a hook left waiting is what `/hooks` already fixes, so the line names it
    instead of failing the install."""
    from probe.cli import codex_hooks

    try:
        outcome = codex_hooks.approve(only=only)
    except Exception:  # noqa: BLE001 - approve never raises; an install never fails on it either way
        outcome = None
    lines: list[str] = []
    if outcome is not None and outcome.approved:
        count = len(outcome.approved)
        lines.append(f"Approved Probe's {count} hook{'s' if count != 1 else ''} in Codex.")
    if outcome is not None and outcome.done:
        return lines, True
    why = "Codex could not be asked" if outcome is None else (outcome.error or "a Probe hook still waits")
    lines.append(f"Probe's hooks in Codex still need approval ({why}): {CODEX_HOOKS_INSTRUCTION}")
    return lines, False


def codex_plugins_kept_on(selection: Selection) -> frozenset[str]:
    """The Probe plugins whose hooks a wizard run may approve: those of the
    capabilities this selection keeps on. Capture turned off leaves the tap
    installed (DISABLE), and its hooks must not be approved in that same run."""
    plugins: set[str] = set()
    if selection.tracking:
        plugins |= {TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME}
    if selection.capture:
        plugins.add(TAP_PLUGIN_NAME)
    return frozenset(plugins)


#: The person's own way to approve Probe's hooks, for when Probe could not.
CODEX_HOOKS_INSTRUCTION = "in a new Codex session, type /hooks and approve the Probe hooks."


def apply_auto_update(want: bool) -> list[str]:
    try:
        autoupdate.save(enabled=want)
    except OSError as exc:
        # Said, never swallowed: the Probe service may read the other answer.
        return [f"! {exc}: automatic updates may still be {'on' if not want else 'off'} (check the folder's permissions)"]
    if not want:
        return ["Auto-update off. You'll still get a nudge when a release lands."]
    return ["Auto-update on."]


def statusline_installed() -> bool:
    """Whether the tracking segment is already in the agent's status line."""
    try:
        from probe.cli import statusline

        return bool(statusline.status().get("installed"))
    except Exception:  # noqa: BLE001 - a probe that fails must not block the wizard
        return False


def apply_statusline() -> list[str]:
    """Register the tracking segment in the agent's status line.

    THE REASON THIS IS A WIZARD STEP AND NOT A README LINE. `statusLine` is a
    single key in the researcher's own settings, so nothing in a release can put
    the segment there -- it has to be written on their machine, once. Left to a
    documented `probe statusline install`, it is a feature almost nobody ends up
    with, and the ones who do are the people who read the changelog.

    Chains rather than claims: whatever was already configured keeps rendering,
    and `probe statusline uninstall` restores it exactly. Failure is reported and
    never fatal -- a status line is not worth failing an install over.
    """
    from probe.cli import statusline

    source = agent_source()
    root = statusline.discover_plugin_root(source)
    if root is None:
        return [
            "Status line: skipped — the plugin is not on disk yet.",
            "  Run the wizard's Install again once it is.",
        ]
    try:
        # The slot the registry names: Claude Code's settings.json or Kimi
        # Code's footer settings (a running Kimi shows it from its next start).
        result = statusline.install_for(source, root)
    except (OSError, ValueError) as exc:
        return [f"Status line: not configured ({exc}). Nothing else was affected."]
    if result.get("chained_after"):
        return ["Status line: on, chained after the command you already had."]
    return ["Status line: on."]


def statusline_catch_up_due(source: str | None) -> bool:
    """The one-time footer catch-up would do something now: owed, not already
    there, and the plugin it renders from is on disk."""
    from probe.cli import statusline

    if not source or not statusline.catch_up_owed(source):
        return False
    if statusline.installed_for(source):
        return False
    return statusline.discover_plugin_root(source) is not None


def catch_up_statusline(source: str | None = None) -> list[str]:
    """Kimi Code's footer for a machine whose rules predate it: the footer is
    written by the rules step (`apply_agent_rules`), which a machine with current
    rules never runs again, so upgrading to 0.214.0 left every existing Kimi
    machine without it. Once per agent (`statusline.mark_caught_up`): whatever
    happens here, a later uninstall is never undone. Not once the plugin is
    missing from disk (a later run tries again)."""
    from probe.cli import statusline
    from probe.cli.capabilities import agent_target

    selected = source or agent_source()
    if not statusline.catch_up_owed(selected):
        return []
    if statusline.installed_for(selected):
        statusline.mark_caught_up(selected)
        return []
    if statusline.discover_plugin_root(selected) is None:
        return []
    with agent_target(selected):
        lines = apply_statusline()
    statusline.mark_caught_up(selected)
    return [f"{agent_label(selected)} {line[0].lower()}{line[1:]}" if i == 0 else line
            for i, line in enumerate(lines)]


def remove_statusline() -> list[str]:
    """Take the tracking segment out of Claude Code's status line, restoring
    exactly what it wrapped: Uninstall's half of `apply_statusline` (R3). Left
    behind, the status line keeps running a renderer nobody maintains."""
    from probe.cli import statusline

    source = agent_source()
    try:
        result = statusline.uninstall_for(source)
    except (OSError, ValueError) as exc:
        return [f"! left the status line in place ({exc}); remove Probe's status-line command from "
                f"{statusline.slot_path(source)} by hand."]
    if not result.get("removed"):
        return []
    if result.get("restored"):
        return ["Status line: back to the command you had before."]
    return ["Status line: removed."]


def seed_team_note_block() -> list[str]:
    """Render the team note into the instruction files at INSTALL time.

    A fresh machine otherwise waits a whole session for its first note. The
    harness reads CLAUDE.md / AGENTS.md before any hook of ours runs, so a block
    written by the first session's sync only reaches the SECOND session. The
    wizard runs before any session at all, which is the one moment that gap can
    be closed -- and closing it is what let the session-start hook stop carrying
    the note as a fallback.

    FAIL-OPEN IN EVERY DIRECTION: no credential, no network, a backend that has
    never heard of this team. Each of those means the block arrives on the next
    sync instead, which is exactly what happened before this existed. A wizard
    that cannot reach the API must still install everything else.
    """
    try:
        from probe.cli import team_note_file
        from probe.sdk.client import Client
        from probe.sdk.config import resolve
        from probe.sdk.surface import Surface

        settings = resolve()
        if not getattr(settings, "token", None):
            return []
        if team_note_file.hidden_by_limit(settings):
            # Team-wide items are hidden by this computer's workspace limit.
            team_note_file.remove_blocks()
            return []
        where = team_note_file.paths_for(settings)
        with Client(
            settings=settings, async_writes=False, surface=Surface.CLI.value
        ) as client:
            _, text = team_note_file.reconcile(client, where)
        report = team_note_file.render_blocks(text, settings=settings)
    except Exception:  # noqa: BLE001 - offline is a later sync, not a failed install
        return []
    if report.failures:
        return [f"! Team note: {report.failures[0]}"]
    if report.written or report.pointer_only:
        return ["Team note written into your instruction file."]
    return []


def _current_harness():
    """The registry row of the agent this wizard run configures."""
    from probe.harness import get_registry

    return get_registry().get(agent_source())


def apply_agent_rules(want: bool, *, stale: bool = False) -> list[str]:
    """Write or drop the selected agent's global instruction pointer.

    `stale` re-writes an already-installed block whose version moved, which is
    the only way a wording fix reaches a machine that ticked this once and never
    re-ran the wizard.
    """
    path = agent_rules.memory_path()
    # The status line rides along with the rules rather than asking its own
    # question. They are one concern -- make this machine's agent aware that
    # tracking exists -- and a separate checkbox for a one-line segment is a
    # worse trade than doing it and saying so. Additive and reversible
    # (`probe statusline uninstall` restores whatever was there), and it can ONLY
    # happen on the machine: `statusLine` is a key in the researcher's own
    # settings, so no release can put the segment there.
    # Only for a harness that has Probe's status line (Claude Code): on a pi or
    # Codex run this used to write Claude Code's settings.json.
    extra = apply_statusline() if want and _current_harness().statusline else []
    try:
        with _instruction_file_lock(path):
            if want:
                # The block of this agent's profile: a re-run must not swap the
                # daemon profile's blurb for the agent profile's section.
                changed = agent_rules.install(path, block=agent_rules.render_block(profile=agent_profile()))
            else:
                changed = agent_rules.remove_all(path)
    except agent_rules.DamagedBlock as exc:
        return [
            f"! Left {path} alone: {exc}.",
            "  Delete the stray probe-research marker by hand, then re-run this.",
        ]
    except (OSError, UnicodeDecodeError) as exc:
        # UnicodeDecodeError is a ValueError, so the OSError guard never caught
        # it: one latin-1 character in a researcher's own CLAUDE.md took the
        # whole wizard down with a traceback, mid-install. "Nothing else was
        # affected" is only true because the write is atomic.
        return [f"Could not update {path}: {exc}. Nothing else was affected."]

    # Seeded HERE, not on the first session, because the harness reads the
    # instruction file before any hook of ours runs -- a block written by the
    # first session's sync only reaches the second one. AFTER the pointer: the
    # note renders only into a file that carries it (`render_blocks`).
    if want:
        extra = extra + seed_team_note_block()

    if not want:
        return [f"Removed the Probe block from your global {path.name}."] if changed else []
    if stale and changed:
        return [f"Refreshed the Probe block in {short_path(path)}."] + extra
    if changed:
        # One line, because it is one bullet in a summary. The reassurance this
        # used to carry -- that the rest of the file is untouched -- is a
        # property of the writer, not news to report on every install.
        return [f"Probe tracking rule added to {short_path(path)}."] + extra
    return extra


def row_box(value: "bool | str") -> str:
    """The glyph one row wears for the value it currently carries.

    A BOOL is a checkbox: ticked or empty. A STRING is a CYCLING row's state
    name, and each state gets its own glyph -- two glyphs over three states
    would draw two of them identically, and the pair that would collide on the
    tracking default is `read-only` and `off`: the state where the team's
    history is still searchable and the state where it is not.

    The names come from `session_marker`, never a copy of them here: the wizard
    and the `/probe` switch have to agree about how many states there are, and a
    second spelling of the vocabulary is where that agreement would rot. An
    unrecognised state draws the empty box, matching `default_session_state`'s
    posture of never *quietly* claiming more is on than is.
    """
    from probe.cli import tui
    from probe.sdk import session_marker

    if isinstance(value, str):
        return {
            session_marker.STATE_FULL: tui.TICK,
            session_marker.STATE_DAEMON: tui.AUTO,
            session_marker.STATE_READ_ONLY: tui.HALF,
            session_marker.STATE_OFF: tui.UNTICK,
            # "Who records": `agent` is today's, ticked; `daemon` wears the
            # glyph above (a stored `daemon` session state is `on (daemon)`).
            session_marker.RECORDER_AGENT: tui.TICK,
        }.get(value, tui.UNTICK)
    return tui.TICK if value else tui.UNTICK


def _menu_row(title: str, detail: tuple[str, ...], *, checked: "bool | str", indent: str) -> str:
    """One capability row, box included.

    WE draw the box (see tui.draw_own_boxes). questionary's own is
    all-rows-or-nothing, and the "Next" row must not have one -- `○ Next` reads
    as an option someone forgot to tick rather than the way forward.

    `checked` is a bool on a checkbox row and a STATE NAME on a cycling one;
    `row_box` is the one place that difference is read.
    """
    from probe.cli import tui

    box = row_box(checked)
    # WRAPPED to the room actually available, not to a constant. prompt_toolkit
    # runs with autowrap off, so a detail longer than the terminal is CLIPPED,
    # not wrapped -- and on the capture row the half that disappears is the
    # clause naming where the data goes. At 60 columns this read "Sends this
    # device's Claude Code and Codex sessions to yo". A disclosure you cannot
    # finish reading is not a disclosure.
    #
    # `content_height` counts a choice's rows from the newlines in its title, so
    # wrapping here also keeps the frame arithmetic honest about how tall these
    # rows are.
    #
    # Measured against the RECTANGLE, not the terminal: the row is drawn inside
    # `tui.box_width()` columns, of which the rails and their padding take four
    # and a detail line's own two-space indent takes two. Wrapping to anything
    # wider puts text under the right rail -- or past the terminal edge on the
    # row that is not currently boxed, which is where it first showed up.
    room = max(20, tui.box_width() - (2 + tui.BOX_GUTTER) - 2)
    lines: list[str] = [f"{box} {title}"]
    for line in detail:
        lines.extend(tui.wrap(line, room))
    # The box sits on the title line only; wrapped detail lines clear it, so
    # they do not read as further options.
    return f"\n{indent}  ".join(lines)


def _row_copy(
    key,
    copy: dict,
    state_copy: dict | None,
    *,
    value: "bool | str",
) -> tuple[str, tuple[str, ...]]:
    """The words one row wears for the value it is currently carrying.

    Rows whose copy does not depend on their value have no `state_copy` entry
    and read out of `copy` whatever they hold -- which is every row except the
    "Who records" rows, whose states are different disclosures rather than one
    sentence with a glyph swapped. Kept as one
    function because the row is painted from THREE places (the first paint, the
    repaint on every press, and the strip when questionary keeps its own boxes),
    and a state-dependent lookup that only two of them do is a row that changes
    its mind when you touch it.
    """
    if isinstance(value, str) and state_copy and key in state_copy:
        per_state = state_copy[key]
        if value in per_state:
            return per_state[value]
    return copy[key]


def _bind_menu_keys(
    question,
    rows: dict[Capability, object],
    *,
    copy: dict[Capability, tuple[str, tuple[str, ...]]],
    indent: str,
    state_copy: dict | None = None,
    cycles: dict | None = None,
    cycle_state: dict | None = None,
    on_back=None,
    on_leave=None,
    exclusive: bool = False,
):
    """Wire step 2's picker: the shared key rule, plus our own checkboxes.

    Returns the control, or None when questionary's internals were unreachable
    -- which the caller has to act on rather than shrug at, because the nav band
    is only safe while WE own the keys.

    WE draw the boxes (`tui.draw_own_boxes`), because questionary's are
    all-rows-or-nothing and the nav rows must not have one -- `○ Next` reads as
    an option someone forgot to tick rather than the way forward. That is also
    why the boxes have to be repainted by hand on every toggle: the library is
    no longer doing it.

    `cycles` names the rows that CYCLE rather than tick -- `{value: (state,
    ...)}` -- and `cycle_state` says where each of them starts. Their state
    lives on the control (`probe_cycle`), which is what the caller reads back
    after the prompt exits; `state_copy` gives such a row DIFFERENT detail lines
    per state, for the rows where the states are not one sentence with a glyph
    swapped. Since we already repaint every row on every press, this costs a
    lookup; the caller that has no such row passes nothing and nothing changes.

    `exclusive` makes the boxes a RADIO: ticking a row unticks the one that was
    ticked, and the last tick cannot be taken away -- a default has to be
    something. `on_leave` replaces the answer (the ticked rows) with the
    caller's own reading of the control.
    """
    from probe.cli import tui

    own_boxes = tui.draw_own_boxes(question)
    radio: dict = {}

    def keep_one(control) -> None:
        ticked = [value for value in control.selected_options if value in rows]
        if "on" not in radio:
            radio["on"] = ticked[0] if ticked else None
        fresh = [value for value in ticked if value != radio["on"]]
        if len(fresh) == 1:
            radio["on"] = fresh[0]
        control.selected_options[:] = [] if radio["on"] is None else [radio["on"]]

    def redraw(control) -> None:
        if exclusive:
            keep_one(control)
        # `own_boxes` is False only when `checkbox_control()` returned None, and
        # `_wire_picker` bails on that same condition before it calls this -- so
        # this only ever runs with the boxes ours to draw. Kept as an assertion
        # of that coupling rather than a branch anyone should expect to take.
        if not own_boxes:
            return
        states = getattr(control, "probe_cycle", None) or {}
        for capability, row in rows.items():
            # A cycling row is drawn from ITS state, never from membership: the
            # membership list has two positions and the row has three, so the
            # box would stop moving after the first press.
            value = (
                states[capability]
                if capability in states
                else capability in control.selected_options
            )
            title, detail = _row_copy(capability, copy, state_copy, value=value)
            row.title = _menu_row(title, detail, checked=value, indent=indent)

    control = _wire_picker(
        question,
        redraw=redraw,
        on_leave=on_leave or (lambda control: [c for c in control.selected_options if c in rows]),
        on_back=on_back,
        cycles=cycles,
        cycle_state=cycle_state,
    )
    if control is None:
        return None
    if not own_boxes:
        # questionary is drawing its own indicator in front of a title that
        # already carries one; strip ours rather than ship `✔ ✔ CLI + MCP`.
        states = getattr(control, "probe_cycle", None) or {}
        for capability, row in rows.items():
            value = states.get(capability, False)
            title, detail = _row_copy(capability, copy, state_copy, value=value)
            row.title = _menu_row(title, detail, checked=value, indent=indent).split(" ", 1)[1]
    tui.point_at(control, lambda value: value == NAV_BAND)
    return control


def confirm_removal(agent_sources: tuple[str, ...] | list[str] | str = ("claude_code",), *, offline: bool = False):
    """The uninstall gate (`probe uninstall`). Returns None, tui.BACK, or a bool.

    A bare `typer.confirm` here was the one prompt in the wizard that printed
    at column 0 -- and it guarded the single destructive action, which is the
    worst place to look like a different program.

    The copy says what the uninstall does and nothing more: it used to claim
    every token was revoked while the daemon key was only wiped off the disk.
    A key another computer also holds is disconnected from this one, not
    revoked; offline, nothing is revoked and the dashboard is where it is done.
    """
    from probe.cli import tui

    agents = f"the {agent_label(agent_sources)} plugins, skills and rules" if agent_sources else "its plugins"
    keys = (
        "Nothing can be revoked offline: revoke this computer's keys in the dashboard afterwards."
        if offline else
        "This computer is retired from your account and its keys are revoked (the API and MCP tokens, the "
        "Probe daemon's key, every capture key); a key another computer also uses is only disconnected "
        "from this one."
    )
    return tui.review(
        "Remove Probe Research from this computer",
        tui.wrap(
            f"Stops every Probe process and removes the Probe CLI, {agents}, the status line, and "
            f"Probe's files for you on this computer. {keys} Your projects, .probe.config files and "
            "data already sent to your team stay."
        ),
        [("Keep Probe Research", False), ("Remove Probe Research", True)],
    )


def confirm_pending_capture(sources: tuple[str, ...] | list[str] | str):
    """Update's question for capture a sign-in left waiting (`AWAITING_CONFIRMATION`).
    Returns None, tui.BACK, or a bool.

    Turning it on is the first choice: the browser approval that left the lock
    is where session capture was granted and disclosed in full, and the
    person is in this wizard to set Probe up here. Saying no changes nothing.
    """
    from probe.cli import tui

    return tui.review(
        "Turn on session capture?",
        tui.wrap(
            f"You signed in on this device, but Install never confirmed session "
            f"capture, so {agent_label(sources)} sessions are not being sent to "
            "your team."
        ),
        [("Turn on session capture", True), ("Not now", False)],
    )


def confirm_agent_removal(agent_sources: tuple[str, ...] | list[str] | str):
    """`probe wizard --action uninstall --agent A`: Probe out of the named
    agents only. Keep first, like `confirm_removal`. None, tui.BACK or a bool."""
    from probe.cli import tui

    return tui.review(
        f"Remove Probe Research from {agent_label(agent_sources)}",
        tui.wrap(
            f"Removes Probe's plugins, hooks, skills and rules from {agent_label(agent_sources)} and stops its "
            "capture. The Probe CLI, this computer's sign-in and every other coding agent stay; "
            "`probe uninstall` removes all of Probe."
        ),
        [("Keep Probe Research", False), (f"Remove it from {agent_label(agent_sources)}", True)],
    )


def confirm_sign_out(account: "str | None" = None):
    """The sign-out gate (Richard 2026-09-29: "add a confirmation page to make
    sure a user doesnt accidentally sign themselves out"). Returns None,
    tui.BACK, or a bool. Staying signed in is listed first, so the cursor starts
    on the choice that costs nothing -- `confirm_removal`'s rule."""
    from probe.cli import tui

    who = f"Signed in as {account}. " if account else ""
    return tui.review(
        "Sign out of Probe on this device",
        tui.wrap(
            f"{who}Stops capture and imports, clears import history, and revokes this "
            "device's tokens. Data already sent to your team stays."
        ),
        [("Stay signed in", False), ("Sign out", True)],
    )


def action_choices(caps_by_source: "dict | None" = None) -> list:
    """The top-level menu: headings lead groups, blank rows separate options.

    Each title stays next to its description. A single blank row separates
    options within a group; the existing blank before each heading keeps the
    heading attached to the group it names.
    """
    import questionary

    from probe.cli import tui
    from probe.cli.actions import ACTION_COPY, DANGER_ACTIONS, Action, grouped_actions

    body = tui.body_indent()
    # The Defaults row wears the machine's CURRENT state, read fresh each time
    # the menu is drawn -- the menu comes back after every action, so a change
    # made through the row shows on the row.
    copy: dict = {
        **ACTION_COPY,
        Action.RECORDER: recorder_row(caps_by_source=caps_by_source),
        Action.DEFAULTS: tracking_default_row(),
    }
    # A blank before EVERY group, the first one included. It was skipped at the
    # top on the theory that a leading gap reads as "after the question" rather
    # than "between groups" -- which is exactly what it should read as. Without
    # it the first heading sits flush under the question and the menu starts
    # before the question has finished being a question.
    choices: list = []
    for group, actions in grouped_actions():
        choices.append(questionary.Separator(" "))
        if group:
            choices.append(questionary.Separator(tui.heading(group)))
            # Air between a heading and its rows (Richard 2026-09-29). A folded
            # group hides it with its rows (`tui.collapsed`), so only the open
            # group spends the line.
            choices.append(questionary.Separator(" "))
        for index, action in enumerate(actions):
            if index:
                choices.append(questionary.Separator(" "))
            title, detail = copy[action]
            lines = (detail,) if isinstance(detail, str) else detail
            choice = questionary.Choice(
                title="\n".join([title, *(f"{body}  {line}" for line in lines)]),
                value=action,
            )
            if action in DANGER_ACTIONS:
                choice.probe_style = tui.DANGER_STYLE  # drawn red by `tui.menu`
            choices.append(choice)
    return choices


def run_action_menu(caps: Capabilities | dict[str, Capabilities]):
    """The top-level menu. Returns None (quit), tui.BACK, an Action, or a
    `RecorderChoice` the moment the Who records row is switched. The Defaults
    row saves itself on each `←`/`→` press (`_DefaultSwitch`) and answers
    nothing."""

    from probe.cli import import_jobs_ui, tui

    choices = action_choices(caps if isinstance(caps, dict) else None)

    from probe.cli import doctor as doctor_impl  # noqa: F401

    # Read once per menu, not per frame: the menu is rebuilt after every action,
    # so an agent installed meanwhile shows on the next one.
    installed = detectable_sources()
    images = tui.image_protocol()
    agent_images = len(caps) if isinstance(caps, dict) else 1

    def live_lines():
        progress = import_jobs_ui.active_progress_lines()
        lines = describe_state(caps, installed=installed, images=images)
        if progress:
            lines += ["", tui.StyledLine("Import progress", style="class:question"), "", *progress]
        return lines

    switch = _DefaultSwitch(choices)
    recorder = _RecorderSwitch(choices)
    message = tui.framed("On this device:", live_lines(), "What do you want to do?")
    question = tui.menu(
        message,
        live_lines=live_lines,
        collapse=True,
        hint=lambda value: recorder.hint(value) or switch.hint(value),
        choices=choices,
        instruction="(arrow keys, enter to choose)",
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    switch.wire(question)
    recorder.wire(question)
    try:
        return tui.ask(question, height=tui.content_height(message, choices))
    finally:
        if images:
            sys.stdout.write(tui.forget_images(images, agent_images))
            sys.stdout.flush()


class _RecorderSwitch:
    """`←`/`→` on the main menu's Who records row: the agent or the Probe daemon,
    for every coding agent on this machine at once (Richard 2026-09-29: "no
    codex/claude split", and "no need to click enter to confirm").

    A press answers the menu straight away with `RecorderChoice(the other one)`;
    the caller moves the agents (plugins, the daemon's key through a browser
    approval, the instruction block) and draws the menu again. Enter on the row
    is the ordinary answer, `Action.RECORDER`: on the daemon it opens the
    daemon's page.
    """

    def __init__(self, choices: list) -> None:
        from probe.cli.actions import Action

        self.row = next((c for c in choices if getattr(c, "value", None) is Action.RECORDER), None)
        self.saved = machine_recorder()
        self.control = None

    def on_row(self) -> bool:
        try:
            return self.control is not None and self.control.get_pointed_at() is self.row
        except Exception:  # noqa: BLE001 - a key filter is never worth a crash
            return False

    def hint(self, value) -> str | None:
        from probe.cli.actions import Action
        from probe.sdk import session_marker

        if value is not Action.RECORDER or self.row is None:
            return None
        if self.saved == session_marker.RECORDER_DAEMON:
            return "← → switch · enter: what the daemon sees"
        return "← → switch"

    def other(self) -> str:
        from probe.sdk import session_marker

        return (session_marker.RECORDER_AGENT if self.saved == session_marker.RECORDER_DAEMON
                else session_marker.RECORDER_DAEMON)

    def wire(self, question) -> None:
        from probe.cli import tui

        if self.row is None:
            return
        self.control = tui.checkbox_control(question)
        if self.control is None:
            return
        try:
            from prompt_toolkit.filters import Condition

            on_row = Condition(self.on_row)
            bindings = question.application.key_bindings

            def switch(event) -> None:  # pragma: no cover - requires a live terminal
                self.control.is_answered = True
                event.app.exit(result=RecorderChoice(self.other()))

            bindings.add("right", eager=True, filter=on_row)(switch)
            bindings.add("left", eager=True, filter=on_row)(switch)
        except Exception:  # noqa: BLE001 - the menu without the switch still works
            pass


class _DefaultSwitch:
    """`←`/`→` on the main menu's Defaults row: switch the default for new
    sessions right there. Each press SAVES it -- a local config write, like the
    Who records row beside it, which applies on press too. It used to wait for
    Enter, and a researcher who switched it and moved on lost the change
    without a word (2026-10-02). Enter on the row is the ordinary menu answer,
    `Action.DEFAULTS`, which opens the picker.

    A write that fails puts the row back on what is saved and says why under it.

    The walk is the switch, `session_marker.SWITCH_STATES`: on / read / off.
    Whether the daemon records is the "Who records" setting, never a position
    here (Richard 2026-09-29).
    """

    def __init__(self, choices: list) -> None:
        from probe.cli.actions import Action
        from probe.sdk import session_marker

        self.row = next((c for c in choices if getattr(c, "value", None) is Action.DEFAULTS), None)
        self.held = session_marker.state_env_override() is not None
        self.saved = setting_state(session_marker.default_session_state())
        self.shown = self.saved
        self.order = cycling_settings()[Setting.TRACKING_DEFAULT]
        self.question = None
        self.control = None
        #: The failure line of the last save, shown under the row until the next.
        self.error: str | None = None

    def on_row(self) -> bool:
        try:
            return self.control is not None and self.control.get_pointed_at() is self.row
        except Exception:  # noqa: BLE001 - a key filter is never worth a crash
            return False

    def hint(self, value) -> str | None:
        from probe.cli.actions import Action

        if value is not Action.DEFAULTS or self.held or self.row is None:
            return None
        return "← → switch"

    def repaint(self) -> None:
        from probe.cli import tui

        title, detail = tracking_default_row(self.shown)
        if self.error:
            detail = (*detail, self.error)
        body = tui.body_indent()
        self.question._probe_retitle(
            self.row, "\n".join([title, *(f"{body}  {line}" for line in detail)])
        )

    def step(self, delta: int) -> None:
        from probe.cli import wizard_lock

        wanted = self.order[(self.order.index(self.shown) + delta) % len(self.order)]
        # The menu holds no run lock while it waits on a person (plan C1), so
        # this write takes it, as every write of the wizard's does.
        try:
            with wizard_lock.held():
                lines = apply_settings({Setting.TRACKING_DEFAULT: wanted})
        except wizard_lock.Busy:
            lines = [f"! {wizard_lock.BUSY_MESSAGE}: not switched"]
        failed = next((line for line in lines if reports_failure(line)), None)
        if failed is None:
            self.saved = self.shown = wanted
            self.error = None
        else:
            self.shown = self.saved
            self.error = failed
        if self.question is not None:
            self.repaint()

    def wire(self, question) -> None:
        from probe.cli import tui

        if self.row is None or self.held or not hasattr(question, "_probe_retitle"):
            return
        self.question = question
        self.control = tui.checkbox_control(question)
        if self.control is None:
            return
        try:
            from prompt_toolkit.filters import Condition

            on_row = Condition(self.on_row)
            bindings = question.application.key_bindings

            @bindings.add("right", eager=True, filter=on_row)
            def _(event) -> None:  # pragma: no cover - requires a live terminal
                self.step(1)

            @bindings.add("left", eager=True, filter=on_row)
            def _(event) -> None:  # pragma: no cover - requires a live terminal
                self.step(-1)
        except Exception:  # noqa: BLE001 - the menu without the switch still works
            pass


#: Components the wizard names in its version rows, and what to call them in a
#: 45-column value. `sdk` is deliberately absent: it ships inside the CLI
#: distribution, so it is the same number by construction and would spend a third
#: of the line restating the one above it. `probe doctor` still lists all four.
_VERSION_LABELS = {"cli": "CLI", "plugin": "plugin", "tap": "tap"}

#: The label column of the device summary: its longest label, "Last update
#: attempt", plus a space. Agents carry an icon rather than a name since
#: 2026-10-05, so nothing longer has to fit.
_STATE_LABEL_WIDTH = 20

#: What is left of a CONTENT_WIDTH row after "  " + the label + a space.
_STATE_VALUE_WIDTH = CONTENT_WIDTH - 3 - _STATE_LABEL_WIDTH

#: Each agent's MCP answer in a few words. `Capabilities.mcp_status` is the
#: sentence `probe doctor` prints; at up to 53 characters it wrapped every agent
#: row here onto a second line that read as a row of its own.
_MCP_WORDS = {
    McpState.ON: "on",
    McpState.LOGIN_NEEDED: "login needed",
    McpState.DAEMON: "off (daemon reads)",
    McpState.NOT_INSTALLED: "not installed",
    McpState.NOT_OFFERED: "not offered",
    McpState.UNKNOWN: "unknown",
}

#: A manifest older than this grades the verdict against a list that may predate
#: several releases, so "up to date" stops being a claim worth making plainly.
#: Same threshold `probe doctor` warns at, for the same reason.
_MANIFEST_STALE_S = 86400


def _state_row(label: str, value: str, style: str = "") -> str:
    """One aligned row of the device summary, optionally carrying a TUI style.

    Clipped, never wrapped: a wrapped value loses its alignment and reads as a
    new row with a blank label (see `_fit`)."""
    from probe.cli import tui

    return tui.StyledLine(f"  {label:<{_STATE_LABEL_WIDTH}} {value}", style=style, clip=True)


def _capture_word(snapshot: Capabilities) -> str:
    """The menu's capture state. A sign-in's pending lock says what lifts it:
    it read "killswitch set", the words for a deliberate off, and a person who
    picked Update instead of Install was never told why nothing recorded."""
    if snapshot.capture_awaiting_confirmation:
        return "off (finish Install)"
    if snapshot.capture_killswitched:
        return "off (killswitch set)"
    return "on" if snapshot.capture_on else "off"


def _agent_rows(caps_by_source: dict[str, Capabilities], images=None) -> list[str]:
    """One row per agent: its logo (or its name), then MCP and capture in
    aligned columns.

    `images` is the terminal's `tui.ImageProtocol`. With one, each agent is its
    logo, two cells wide, and pointing at the row shows its name; without one
    (Terminal.app, tmux, a pipe) the name stands in the logo's column. One
    agent without a logo gets names for every row, so the columns still line up.
    """
    from probe.cli import tui

    names = {source: agent_label(source) for source in caps_by_source}
    logos = {source: agent_logo(source) for source in caps_by_source} if images else {}
    drawn = bool(logos) and all(logos.values())
    lead = 2 if drawn else max(map(len, names.values()), default=0)
    mcp = {
        source: f"MCP {_MCP_WORDS.get(snapshot.mcp_state, snapshot.mcp_state)}"
        for source, snapshot in caps_by_source.items()
    }
    mcp_width = max(map(len, mcp.values()), default=0)
    rows: list[str] = []
    for index, (source, snapshot) in enumerate(caps_by_source.items()):
        capture = _capture_word(snapshot)
        label = "" if drawn else names[source]
        text = f"  {label:<{lead}}  {mcp[source]:<{mcp_width}}   capture {capture}"
        if drawn:
            # Drawn over the two blank cells before column 4, once that column is.
            logo = tui.image_escape(logos[source], images, cells=2, image_id=tui.IMAGE_ID_BASE + index)
            rows.append(tui.StyledLine(text, clip=True, escapes=((4, logo),), hover=names[source]))
        else:
            rows.append(tui.StyledLine(text, clip=True))
    return rows


def _fit(parts: list[str], limit: int = _STATE_VALUE_WIDTH) -> str:
    """Join what fits on ONE row, marking the rest rather than wrapping.

    A wrapped value in this block loses its alignment and reads as a new row with
    a blank label, which in a summary of what is installed is worse than saying
    less. The dropped tail is never the headline: callers order these worst-first,
    and the room for the ellipsis is only reserved once something is actually
    being dropped -- charging for it up front is what made a list that fits
    exactly render as a truncated one.
    """
    whole = " · ".join(parts)
    if len(whole) <= limit:
        return whole
    kept: list[str] = []
    for part in parts:
        if kept and len(" · ".join([*kept, part])) + 2 > limit:
            break
        kept.append(part)
    return (" · ".join(kept) + " …") if kept else ""


#: mark, wording and style per verdict. Amber (`class:instruction`) for anything
#: needing a decision and green (`class:selected`) only for the one row that
#: needs none -- the same pairing the import rows in this menu already use.
_VERDICT_COPY = {
    VersionStatus.CURRENT: ("✔", "Up to date", "class:selected"),
    VersionStatus.UPDATE: ("·", "Update available", "class:instruction"),
    VersionStatus.NEEDED: ("!", "Update needed — features may misbehave", "class:instruction"),
    VersionStatus.REQUIRED: ("✗", "Update required — no longer supported", "class:instruction"),
    VersionStatus.UNKNOWN: ("·", "Not checked", "class:instruction"),
}


def describe_versions(caps: Capabilities) -> list[str]:
    """"Am I current?" — the verdict, then the numbers behind it.

    The rows around this one say what is switched ON. None of them say whether
    what is switched on is the version we publish, and until now the only surface
    that did was `probe doctor` -- a command you have to already suspect
    something to run. The comparison is the same one (`probe.cli.versions`), so
    the two can disagree only by being differently WORDED, never differently
    graded.

    An unreadable or absent manifest gets its own wording rather than falling
    through to the good-news branch. That is the invariant versions.py is built
    around: "nothing was wrong" and "nothing was checked" must not render alike.
    """
    rows, verdict = version_verdict(caps)
    mark, text, style = _VERDICT_COPY[verdict]

    age = caps.version_manifest_age_s
    stale = age is not None and age > _MANIFEST_STALE_S
    if stale and verdict is VersionStatus.CURRENT:
        # The one verdict an old manifest can silently falsify: everything else
        # here only gets MORE true as the published list moves on. Said on the
        # verdict line, not tucked below it, and not in green.
        text = f"{text} · checked {_describe_age(age)}"
        style = "class:instruction"

    lines = [_state_row("Versions", f"{mark} {text}", style)]
    detail = _version_detail(rows, verdict)
    if detail:
        lines.append(_state_row("", detail))
    return lines


def version_verdict(caps: Capabilities) -> tuple[list, VersionStatus]:
    """The components the Versions row grades (CLI, plugin, tap) and its
    verdict on them -- `describe_versions` and `probe status` alike."""
    rows = [row for row in caps.version_rows if getattr(row, "kind", "") in _VERSION_LABELS]
    return rows, overall_version_status(rows) if rows else VersionStatus.UNKNOWN


def _join_names(names: list[str]) -> str:
    """`a`, `a and b`, `a, b and c` -- a list a person reads, not a CSV."""
    if len(names) <= 1:
        return "".join(names)
    return f"{', '.join(names[:-1])} and {names[-1]}"


def _describe_age(seconds: float) -> str:
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"


def _version_detail(rows: list, verdict: VersionStatus) -> str:
    """The numbers under the verdict: what to update, or what you are running."""
    if verdict is VersionStatus.UNKNOWN:
        if not rows:
            return "no published version list cached yet"
        return "installed versions could not be read"
    behind = [row for row in rows if row.behind]
    if behind:
        moves = [
            f"{_VERSION_LABELS[row.kind]} {row.installed} → {row.latest}"
            for row in behind
            if row.installed and row.latest
        ]
        # Comma-separated, where the rest of the block uses "·": each move
        # already carries a spaced arrow, and a middle dot between two of those
        # reads as a third one. The two columns it saves are also what let a PAIR
        # of moves fit -- "CLI 0.161.0 → 0.162.0, plugin 0.80.0 → 0.81.0" is
        # exactly the width of the row.
        if len(", ".join(moves)) <= _STATE_VALUE_WIDTH:
            return ", ".join(moves)
        # Every version number, or none of them. A truncated list of moves reads
        # as "the CLI is behind" while silently dropping the components that are
        # behind as well, so past the row's width it degrades to naming them all
        # -- complete, and still one line. `probe doctor` prints the numbers.
        names = [_VERSION_LABELS[row.kind] for row in behind]
        return _fit([f"{_join_names(names)} behind"])
    return _fit([f"{_VERSION_LABELS[row.kind]} {row.installed}" for row in rows if row.installed])


def describe_state(
    caps: Capabilities | dict[str, Capabilities],
    installed: Iterable[str] | None = None,
    images=None,
) -> list[str]:
    """A one-glance summary printed above the menu on a re-run.

    The wizard already knows all of this, so showing it means the user picks an
    action against real state rather than guessing which one they need.

    `installed` limits the agent rows to the agents found on this machine
    (`detectable_sources`); None shows every agent in `caps`. The device rows
    still come off the first snapshot either way. `images` draws each agent as
    its logo (`_agent_rows`).
    """
    if isinstance(caps, dict):
        found = None if installed is None else set(installed)
        agents = {source: snapshot for source, snapshot in caps.items() if found is None or source in found}
        lines: list[str] = _agent_rows(agents, images) if agents else [
            _state_row("Coding agents", "none found on this device")
        ]
        first = next(iter(caps.values()), None)
        if first is not None:
            lines.append("")
            # Directly under the agents, above the update settings: what you are
            # running, then whether it keeps itself current, then when it last
            # tried. The version rows are device-wide -- one CLI, one plugin
            # ledger -- so they come off the first snapshot like the rows below.
            lines.extend(describe_versions(first))
            lines.append(_state_row("Automatic updates", "on" if first.auto_update_enabled else "off"))
            # ALWAYS, signed in or not. Printed only when an email resolved,
            # "not signed in" was the one state this summary could not show --
            # so the machine that most needs the account row was the machine
            # that never got one.
            lines.append(_state_row("Account", first.logged_in_as or "not signed in"))
            if first.last_update_attempt_summary:
                lines.append(_state_row("Last update attempt", first.last_update_attempt_summary))
        return lines

    lines = [
        _state_row(
            "CLI + MCP",
            caps.mcp_status() + (f"  ({caps.logged_in_as})" if caps.logged_in_as else ""),
        )
    ]
    lines.append(_state_row("Session capture", _capture_word(caps)))
    lines.extend(describe_versions(caps))
    lines.append(_state_row("Automatic updates", "on" if caps.auto_update_enabled else "off"))
    if caps.last_update_attempt_summary:
        lines.append(_state_row("Last update attempt", caps.last_update_attempt_summary))
    return lines


# -- accounts ---------------------------------------------------------------
#
# The credentials on this device belong to ONE account, and until now the wizard
# could only ever mint them (Install) or destroy the whole installation
# (Uninstall). Anyone who signed in with the wrong account, joined a second
# team, or handed the laptop on had to be told to leave the wizard and run
# `probe login` / `probe logout` -- two commands the wizard names exactly once,
# in a message printed after removing a plugin. So the wizard managed everything
# about this device except whose data it writes to.
#
# What makes this a screen of its own rather than a fifth checkbox: the
# capability menu is about what Probe DOES here, and every row of it is the same
# answer under a different account. Switching who you are is not another
# capability, it is the thing all of them hang off.


class AccountAction(StrEnum):
    """A row on the account screen. Not a `Capability` -- see the note above."""

    SIGN_IN = "sign_in"
    SWITCH = "switch"
    #: Forget ANOTHER saved account; the active one leaves by SIGN_OUT (R4).
    REMOVE = "remove"
    SIGN_OUT = "sign_out"
    BACK = "back"


#: Row copy for the account screen. Module-level, like MENU_COPY and
#: ACTION_COPY, so the narrow-terminal guard can MEASURE it -- a detail wider
#: than the block wraps mid-word and undoes the separation between rows.
ACCOUNT_COPY: dict[AccountAction, tuple[str, str]] = {
    AccountAction.SIGN_IN: (
        "Sign in",
        "Approve this device in the browser; the credentials are saved here.",
    ),
    AccountAction.SWITCH: (
        "Switch to an account saved here",
        "Use an account saved here. No browser.",
    ),
    AccountAction.REMOVE: (
        "Remove a saved account",
        "Delete another account saved here.",
    ),
    AccountAction.SIGN_OUT: (
        "Sign out",
        "Revoke this device's token and clear it.",
    ),
    AccountAction.BACK: (
        "Back",
        "Return to the main menu. Nothing changes.",
    ),
}

#: What the sign-in row says on a device that already holds a credential. Same
#: action, different sentence: "Sign in" there reads as a no-op, which is how
#: someone stuck on the wrong account concludes the wizard cannot help them.
SIGN_IN_AGAIN_TITLE = "Sign in as a different account"


#: Credentials that live in the SHELL, in resolution-priority order. Every one
#: of them outranks the config file (see sdk/config.resolve), so a sign-out that
#: does not name them would be the same lie about the API that capture.py exists
#: to prevent about transcripts: the file is empty, the CLI still authenticates,
#: and nothing on screen said so.
ENV_CREDENTIALS = (
    "PROBE_TOKEN",
    "PROBE_MCP_TOKEN",
    "PROBE_INGEST_TOKEN",
    "PROBE_SERVICE_TOKEN",
)


@dataclass(frozen=True)
class SavedAccount:
    """One named context in the CLI config, as the account screen shows it."""

    name: str
    base_url: str | None
    has_token: bool
    active: bool

    def describe(self) -> str:
        """The endpoint, and whether this one can actually authenticate."""
        where = self.base_url or "no endpoint saved"
        return where if self.has_token else f"{where} — no credential saved"


def saved_accounts() -> list[SavedAccount]:
    """Every account saved on this device. Read-only and fail-soft.

    `load_file` already degrades an unreadable config to `{}` for readers, which
    is the right answer here: a menu must render something, and "no saved
    accounts" is recoverable by signing in. (WRITERS take the strict path -- see
    config.load_file -- because for them the same shrug would overwrite the
    file.)
    """
    from probe.sdk.config import DEFAULT_CONTEXT, load_file

    data = load_file()
    contexts = data.get("contexts")
    if not isinstance(contexts, dict):
        return []
    active = data.get("current_context") or DEFAULT_CONTEXT
    return [
        SavedAccount(
            name=name,
            base_url=(context.get("base_url") if isinstance(context, dict) else None),
            has_token=bool(isinstance(context, dict) and context.get("token")),
            active=name == active,
        )
        for name, context in sorted(contexts.items())
    ]


def account_email(base_url: str | None = None) -> str | None:
    """Who the resolved credential belongs to, or None.

    One network call, and failure is not an error: after a sign-in the answer is
    nice to have, never load-bearing, and an offline laptop must still be able
    to finish the flow.
    """
    from probe.sdk.client import Client
    from probe.sdk.surface import Surface
    from probe.sdk.config import resolve

    settings = resolve(base_url=base_url)
    if not settings.token:
        return None
    try:
        with Client(
            settings=settings, async_writes=False, surface=Surface.CLI.value
        ) as client:
            return str(client.me().get("email") or "") or None
    except Exception:  # noqa: BLE001 - an unreachable endpoint is not an identity
        return None


def describe_account(caps: Capabilities, *, saved: list[SavedAccount] | None = None) -> list[str]:
    """The account state, for the header above the account screen."""
    saved = saved_accounts() if saved is None else saved
    active = next((account for account in saved if account.active), None)
    # THREE states, not two. `logged_in_as` is an email the API confirmed, so it
    # is empty both for a device with no credential AND for one whose endpoint
    # could not be reached -- and telling an offline researcher "not signed in"
    # invites them to re-approve a device that was never signed out.
    if caps.logged_in_as:
        who = caps.logged_in_as
    elif active is not None and active.has_token:
        who = "a saved credential — could not reach the endpoint to confirm whose"
    else:
        who = "not signed in"
    lines = [
        f"  {'Signed in as':<28} {who}",
        f"  {'Endpoint':<28} {caps.base_url or 'unknown'}",
    ]
    if active is not None:
        others = len(saved) - 1
        suffix = f"  (+{others} other saved here)" if others > 0 else ""
        lines.append(f"  {'Saved account':<28} {active.name}{suffix}")
    return lines


def can_sign_out(caps: Capabilities, saved: list[SavedAccount]) -> bool:
    """Whether there is anything here to sign out OF.

    Deliberately not just `caps.logged_in_as`: that is a verified email, so it
    is None on a laptop with no network -- and offering no way out of an account
    because the machine is offline is exactly when someone needs one.
    """
    active = next((account for account in saved if account.active), None)
    return bool(caps.logged_in_as) or bool(active and active.has_token)


def run_account_menu(caps: Capabilities, *, saved: list[SavedAccount] | None = None):
    """The account screen. Returns None (quit), tui.BACK, or an AccountAction.

    Retained for `--action account`. Account changes start by signing out;
    opening the wizard again performs a fresh sign-in before the main menu.
    """
    import questionary

    from probe.cli import tui

    saved = saved_accounts() if saved is None else saved
    body = tui.body_indent()
    choices: list = [questionary.Separator(" ")]

    def row(action: AccountAction, *, title: str | None = None) -> None:
        if len(choices) > 1:
            choices.append(questionary.Separator(" "))
        default_title, detail = ACCOUNT_COPY[action]
        choices.append(
            questionary.Choice(title=f"{title or default_title}\n{body}  {detail}", value=action)
        )

    # Switching and removing act on the OTHER saved accounts, so neither row
    # shows on a device that holds only the active one.
    if any(not account.active for account in saved):
        row(AccountAction.SWITCH)
        row(AccountAction.REMOVE)
    if can_sign_out(caps, saved):
        row(AccountAction.SIGN_OUT)
    row(AccountAction.BACK)

    message = tui.framed(
        "This device's account:", describe_account(caps, saved=saved), "What do you want to do?"
    )
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            instruction="(arrow keys, enter to choose)",
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )


def run_switch_menu(saved: list[SavedAccount], *, removing: bool = False):
    """Pick one of the saved accounts that is NOT active: to make it active, or
    (`removing`) to delete it. Returns None, tui.BACK, or a name."""
    import questionary

    from probe.cli import tui

    body = tui.body_indent()
    choices: list = [questionary.Separator(" ")]
    for index, account in enumerate([a for a in saved if not a.active]):
        if index:
            choices.append(questionary.Separator(" "))
        choices.append(
            questionary.Choice(
                title=f"{account.name}\n{body}  {account.describe()}", value=account.name
            )
        )
    choices.append(questionary.Separator(" "))
    choices.append(questionary.Choice(title="Back", value=tui.BACK))

    message = tui.framed(
        "Accounts already saved on this device.",
        tui.wrap(
            "Deletes it from this device. Its token stays valid until you revoke it "
            "in the dashboard."
            if removing
            else "Switching is local. Nothing is sent."
        ),
        "Which one should be removed?" if removing else "Which one should this device use?",
    )
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            instruction="(arrow keys, enter to choose)",
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )


# -- settings ---------------------------------------------------------------
#
# What is left of a screen that used to hold every capability:
#
# * "Updates" — automatic updates, the one capability that is not a PART of
#   Probe. Tracking, capture and the instruction rules had rows here too, and
#   they are gone on purpose: Probe is installed whole and removed whole
#   (Uninstall), and a row per part is how devices ended up with half of it.
#   Per-agent control stays on the flag path (`--agent codex --no-capture`).
# * "Who records" — per agent, offered to every team the daemon is open to.
#
# `TRACKING_DEFAULT` — the default for new sessions, a preference, NOT the
# tracking plugin — is still a `Setting`, but it is drawn on the MAIN MENU
# (`tracking_default_row`, `run_defaults_menu`) rather than on this screen: it
# is the one setting worth seeing every time the wizard opens.


class Setting(StrEnum):
    """One option the settings screen manages. The vocabulary only --
    `SETTINGS_GROUPS` is the screen order, `SETTINGS_COPY` the words, and
    the caller's snapshot (`read_settings` plus the capability state it is
    handed) the state. Adding a setting means one entry in each; the screen
    itself never changes."""

    AUTO_UPDATE = "auto_update"
    TRACKING_DEFAULT = "tracking_default"
    RECORDER_CLAUDE_CODE = "recorder_claude_code"
    RECORDER_CODEX = "recorder_codex"
    RECORDER_PI = "recorder_pi"
    RECORDER_KIMI_CODE = "recorder_kimi_code"
    REASONING_SUMMARIES = "reasoning_summaries"
    PASTED_IMAGES = "pasted_images"


#: The "Who records" rows (daemon reads), one per coding agent with a daemon
#: profile, and the agent each drives. Like the capability rows they apply
#: through their own machinery (`apply_recorder`: plugins, the daemon's key,
#: the instruction block), never `apply_settings`. Shown wherever the server
#: does not say the daemon is closed to this team, and always where the daemon
#: already records.
RECORDER_SETTINGS: dict["Setting", str] = {
    Setting.RECORDER_CLAUDE_CODE: "claude_code",
    Setting.RECORDER_CODEX: "codex",
    Setting.RECORDER_PI: "pi",
    Setting.RECORDER_KIMI_CODE: "kimi_code",
}


#: The capability rows — the ones whose apply path is the CONFIGURE machinery
#: (verification, the progress screen), never a bare config write.
#: `apply_settings` refuses them by design; see `_run_settings_action`.
CAPABILITY_SETTINGS: frozenset[Setting] = frozenset({Setting.AUTO_UPDATE})

#: Which `Capability` each capability row drives. One table, so the screen,
#: the union read, and the target Selection cannot disagree about the mapping.
SETTING_CAPABILITY: dict[Setting, Capability] = {
    Setting.AUTO_UPDATE: Capability.AUTO_UPDATE,
}

#: The screen, as GROUPS -- the same shape as the action menu's ACTION_GROUPS
#: and for the same reason: the next setting lands in a named group instead of
#: lengthening one flat column.
SETTINGS_GROUPS: tuple[tuple[str, tuple[Setting, ...]], ...] = (
    ("Updates", (Setting.AUTO_UPDATE,)),
    ("Images", (Setting.PASTED_IMAGES,)),
)

#: The daemon's page: Enter on the main menu's Who records row while the daemon
#: records, and straight after switching to it (Richard 2026-09-29).
DAEMON_GROUPS: tuple[tuple[str, tuple[Setting, ...]], ...] = (
    ("What the daemon sees", (Setting.REASONING_SUMMARIES,)),
)

#: Settings drawn on the MAIN MENU instead of the settings screen. Still part
#: of the registry -- read by `read_settings`, written by `apply_settings` --
#: so `grouped_settings` counts them as placed rather than as missing.
MENU_SETTINGS: frozenset[Setting] = frozenset(
    {Setting.TRACKING_DEFAULT, Setting.RECORDER_CLAUDE_CODE, Setting.RECORDER_CODEX, Setting.RECORDER_PI,
     Setting.RECORDER_KIMI_CODE}
)

#: Row copy, `MENU_COPY`-shaped (title, detail lines) so `_bind_menu_keys` can
#: repaint these rows exactly the way it repaints the agent picker's. The
#: capability rows deliberately echo the confirm screen's bullets — same
#: feature, same words, on and off.
SETTINGS_COPY: dict[Setting, tuple[str, tuple[str, ...]]] = {
    Setting.AUTO_UPDATE: (
        "Automatic updates",
        ("Updates the CLI and plugins at session start.",),
    ),
    # On by default for every device, offered only here (Richard 2026-10-12:
    # "default on even for currently installed people ... dont add a step in
    # the install path"). The capture tap reads it before each upload.
    Setting.PASTED_IMAGES: (
        "Upload images you paste",
        ("Images you paste into a prompt upload with the session, unscanned.",),
    ),
    Setting.TRACKING_DEFAULT: (
        "Probe in new sessions",
        # The leading "" is a BLANK LINE, not a stray element: this row's
        # detail is a disclosure rather than a caption, and it reads as one
        # once it is not crowded against the title. `_menu_row` wraps every
        # detail line, and `tui.wrap("")` is one empty line -- so the spacing
        # lives in the copy, where a reader can see it, instead of in a render
        # rule that would silently apply to rows nobody wanted it on.
        ("", "New sessions read and write Probe."),
    ),
    Setting.RECORDER_CLAUDE_CODE: ("Who records in Claude Code", ("",)),
    Setting.RECORDER_CODEX: ("Who records in Codex", ("",)),
    Setting.RECORDER_PI: ("Who records in pi", ("",)),
    Setting.RECORDER_KIMI_CODE: ("Who records in Kimi Code", ("",)),
    # One setting per coding agent, written for the daemon into each agent's
    # own config (`reasoning_summaries`): it changes what the user sees too,
    # so the row says so.
    Setting.REASONING_SUMMARIES: (
        "Daemon sees the agent's reasoning",
        # Leading "" like the Who-records rows beside it: a disclosure, spaced as one.
        ("",
         "Claude Code and Codex write reasoning summaries for the daemon.",
         "They show in your terminal and upload with the session.",
         "New sessions only."),
    ),
}

#: The "Who records" rows' detail per position. `daemon` mints the daemon's key
#: when committed, so it says whose key it is and where its deletes stop (the
#: trash, or the researcher's yes). The ONLY place the daemon is chosen (Richard
#: 2026-09-29): the tracking default below is on / read / off.
_RECORDER_STATE_COPY: dict[str, tuple[str, ...]] = {
    "agent": (
        "",
        "Your agent records and searches Probe itself.",
    ),
    "daemon": (
        "",
        "The daemon records and searches; your agent instruments runs.",
        "Deletes go to the trash or ask first, unless prompts are off.",
        # The daemon position also edits the agent's own config
        # (`reasoning_summaries`), and the copy says so before the commit.
        "Turns on reasoning summaries unless you set them (below).",
    ),
}

#: The detail lines a CYCLING row paints in EACH of its states, for the rows
#: whose states are not one sentence with a glyph swapped. Only the tracking
#: default is here, and it is here because its three states are three different
#: disclosures: `read` stops the `probe` CLI's write commands and leaves the MCP
#: read surface running, while `off` stops the reads too -- and someone looking
#: at a row that only said "off" would have no way to tell which of those they
#: were getting. The row used to be a tick box whose empty state carried a
#: footnote pointing AWAY from this screen ("disable MCP in your coding agent to
#: stop it reading"); the third state is that footnote, made pressable.
#:
#: Keyed by `Setting` then by STORED state name (`session_marker.STATES`), values
#: are the detail lines alone -- the title is composed from `SETTINGS_COPY` plus
#: the state's word, so there is one place each half lives. A setting absent from
#: this table reads out of `SETTINGS_COPY` whatever it holds, which is every
#: other row. `grouped_settings` pins the keys against the real vocabulary.
SETTINGS_STATE_COPY: dict[Setting, dict[str, tuple[str, ...]]] = {
    Setting.TRACKING_DEFAULT: {
        # Blank first line in every state, exactly as in `SETTINGS_COPY` -- all
        # three have to space the same way, or a press jogs the text up a row.
        "full": ("", "New sessions read and write Probe."),
        "read-only": ("", "Write commands are blocked; search still works."),
        "off": ("", "No Probe calls at all, so no search either; the service captures none."),
    },
    Setting.RECORDER_CLAUDE_CODE: _RECORDER_STATE_COPY,
    Setting.RECORDER_CODEX: _RECORDER_STATE_COPY,
    Setting.RECORDER_PI: _RECORDER_STATE_COPY,
    Setting.RECORDER_KIMI_CODE: _RECORDER_STATE_COPY,
}


def capability_state_for(snapshot) -> dict[Capability, bool]:
    """ONE agent's capability state, read with the SCREEN's own predicates.

    Every capability, not only the ones with a row: the Automatic updates box
    is drawn from this read, and `_apply_capability_settings` builds each
    agent's target from it with only the toggled row overridden. The rows it
    does not change ride along marked `Selection.preserve`, because a read
    cannot say "leave it" (a pending capture lock reads as off); this read
    still decides the booleans the screen and the apply compare. The first ship of the settings screen preserved from
    `Capabilities.enabled()` instead, whose TRACKING member also requires a
    login, so on a signed-out machine an unrelated commit uninstalled the
    tracking plugin.

    TRACKING deliberately reads the PLUGIN fact, not `tracking_on`: "is it
    installed here" is what a commit would change, and `probe doctor` owns
    diagnosing a plugin that is installed but signed out.
    """
    return {
        Capability.TRACKING: bool(snapshot.tracking_plugin_installed),
        Capability.CAPTURE: bool(snapshot.capture_on),
        Capability.AGENT_RULES: bool(snapshot.agent_rules_installed),
        Capability.AUTO_UPDATE: bool(snapshot.auto_update_enabled),
    }


def capability_settings_state(caps_by_source: dict) -> dict[Setting, bool]:
    """The capability rows' boxes, read as the UNION across this device's agents.

    Union, not intersection: the box answers "does this device do X at all",
    which is the same reading `describe_state` gives the menu header. There is
    no per-agent split to note: the one remaining row, automatic updates, is a
    single device-wide file (`autoupdate`), so the agents cannot disagree.
    """
    states = [capability_state_for(snapshot) for snapshot in caps_by_source.values()]
    return {
        setting: any(state[capability] for state in states)
        for setting, capability in SETTING_CAPABILITY.items()
    }

#: The band's forward label on the settings screen. `Next ›` would promise
#: another step; this screen has none -- the way forward IS the commit.
APPLY_TITLE = "Set settings  ›"


def grouped_settings() -> tuple[tuple[str, tuple[Setting, ...]], ...]:
    """`SETTINGS_GROUPS`, checked against the rest of the registry first.

    Same contract as `grouped_actions`: the tables are separate and a setting
    needs ALL of them. A group entry with no copy renders a titleless row;
    copy in no group is a setting that silently stopped being reachable; and
    an enum member in neither is a writer with no screen. None of these show
    up as an error on their own -- the screen just quietly has the wrong
    number of things on it -- so the agreement is asserted where it is used.
    """
    listed = tuple(s for _, settings in (*SETTINGS_GROUPS, *DAEMON_GROUPS) for s in settings)
    placed = set(listed) | MENU_SETTINGS
    if (
        len(set(listed)) != len(listed)
        or set(listed) & MENU_SETTINGS
        or placed != set(SETTINGS_COPY)
        or placed != set(Setting)
    ):
        raise AssertionError(
            f"settings registry disagrees: groups list {listed}, the menu draws "
            f"{sorted(MENU_SETTINGS)}, copy has {tuple(SETTINGS_COPY)}, "
            f"enum has {tuple(Setting)}"
        )
    # Per-state copy is OPTIONAL per row, so it is checked for strays rather
    # than for totality: a key here that is not a setting paints nothing and
    # would otherwise sit in the file looking like it works. Its STATE keys are
    # checked for totality, though, against the vocabulary itself -- a state
    # added to `session_marker.STATES` with no words here would render as the
    # previous state's sentence under a moved glyph, which is the one failure
    # this row cannot afford: copy saying reads still work over a state where
    # they do not.
    cycles = cycling_settings()
    stray = set(SETTINGS_STATE_COPY) - set(Setting)
    if stray:
        raise AssertionError(f"per-state copy names settings that do not exist: {stray}")
    for setting, per_state in SETTINGS_STATE_COPY.items():
        order = cycles.get(setting)
        if order is None:
            raise AssertionError(f"{setting!r} has per-state copy but does not cycle")
        if tuple(per_state) != tuple(order):
            raise AssertionError(
                f"{setting!r} copy covers {tuple(per_state)}, the switch has {tuple(order)}"
            )
    return SETTINGS_GROUPS


def cycling_settings() -> dict[Setting, tuple[str, ...]]:
    """The rows that CYCLE rather than tick, and the order one press walks.

    The order is `session_marker.STATES` itself, never a copy of it: the wizard's
    space bar and the researcher's bare `/probe` are the same switch seen from
    two places, and a screen that walked its own order would make one of them
    wrong the first time a state moved.
    """
    from probe.sdk import session_marker

    return {
        Setting.TRACKING_DEFAULT: session_marker.SWITCH_STATES,
        **{setting: session_marker.RECORDERS for setting in RECORDER_SETTINGS},
    }


def setting_state(value: "bool | str") -> str:
    """One cycling row's value as a STATE NAME.

    A bool is the two-valued answer this row used to give, read as what that
    boolean has always meant -- ticked is `full`, empty is `read-only`, never the
    hard `off` (`session_marker.write_default_tracking` maps it the same way).
    Callers still handing a bool get the old meaning rather than a TypeError
    drawing the box.

    A stored `daemon` (from when the switch had that position) reads as `on`:
    a session started from it is `on_state`, the daemon only where "Who
    records" says so.
    """
    from probe.sdk import session_marker

    if isinstance(value, str):
        state = session_marker.normalize_state(value) or session_marker.DEFAULT_STATE
        return session_marker.STATE_FULL if state == session_marker.STATE_DAEMON else state
    return session_marker.STATE_FULL if value else session_marker.STATE_READ_ONLY


def cycle_value(setting: Setting, value: "bool | str") -> str:
    """One cycling row's value in ITS vocabulary: a session state for the
    tracking default (`setting_state`), `agent`/`daemon` for a "Who records"
    row -- where a bool is the box (ticked = the first position, `agent`) and
    anything unrecognised reads as `agent`, today's profile."""
    from probe.sdk import session_marker

    if setting in RECORDER_SETTINGS:
        if isinstance(value, str):
            return value if value in session_marker.RECORDERS else session_marker.RECORDER_AGENT
        return session_marker.RECORDER_AGENT if value else session_marker.RECORDER_DAEMON
    return setting_state(value)


def value_label(setting: Setting, value: str) -> str:
    """The word a cycling row wears for `value`."""
    from probe.sdk import session_marker

    if setting in RECORDER_SETTINGS:
        return RECORDER_WORDS.get(value, value)
    return session_marker.state_label(value)


def read_settings(caps_by_source: dict | None = None) -> dict[Setting, bool]:
    """Every setting's current value, read once.

    ONE read feeds both the boxes the screen draws and the diff
    `_run_settings_action` computes against what comes back -- reading again
    at apply time would reopen the gap 0.96.0 closed, where a config change
    landing while the prompt sat open made the screen and the write disagree.

    `caps_by_source` supplies the capability rows' state (see
    `capability_settings_state`); without it only the config-file settings are
    returned -- enough for `describe_settings`, not for the screen, whose
    registry check demands every row have a value.
    """
    from probe.sdk import session_marker

    values: dict[Setting, "bool | str"] = {
        # The THREE-valued read, because the row is three-valued: reading the
        # boolean here would draw `off` as `read` and commit it back as `read`
        # the moment anything else on the screen changed.
        # A stored `daemon` from before reads as `on` (`setting_state`).
        Setting.TRACKING_DEFAULT: setting_state(session_marker.default_session_state()),
        # Who records, per agent: read from the same config, whether or not
        # the row is drawn, so the registry check always has a value.
        **{setting: session_marker.recorder(source) for setting, source in RECORDER_SETTINGS.items()},
        Setting.REASONING_SUMMARIES: reasoning_summaries.row_on(reasoning_sources(caps_by_source)),
        Setting.PASTED_IMAGES: session_marker.pasted_images_on(),
    }
    if caps_by_source is not None:
        values.update(capability_settings_state(caps_by_source))
    return values


def reasoning_sources(caps_by_source: dict | None = None) -> tuple[str, ...]:
    """The agents the reasoning row covers: those set up on this device (every
    one when unknown). ONE answer for the read and the write, or the box would
    draw one set of agents and commit another."""
    return tuple(
        source for source in reasoning_summaries.SOURCES
        if caps_by_source is None or source in caps_by_source
    )


def apply_settings(
    changes: dict[Setting, bool], *, caps_by_source: dict | None = None,
) -> list[str]:
    """Write ONLY the settings whose box changed, and say what each became.

    Callers pass the diff, not the whole picker state: rewriting an unchanged
    setting is a pointless config write, and on the tracking default it would
    also stamp a `defaults` block into a config that never had one.

    Failures are PER SETTING, reported in place rather than raised: with two
    settings in one commit, a raise after the first write would leave it
    silently applied while the screen reported only the failure. And a
    `Setting` this function has no writer for is a BUG, not a no-op --
    accepting it as a change and writing nothing is exactly the silent
    registry drift `grouped_settings` exists to catch.

    CAPABILITY settings are refused here BY DESIGN, not by drift: turning a
    capability on needs authorization, grant gating, retries and verification
    -- the CONFIGURE machinery -- and a bare `apply_*` call would report "on"
    while the capability stayed off. `_run_settings_action` owns that route.
    """
    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    lines: list[str] = []
    for setting, value in changes.items():
        if setting in CAPABILITY_SETTINGS:
            raise AssertionError(
                f"{setting!r} is a capability: it applies through the CONFIGURE "
                "machinery in _run_settings_action, never a bare config write"
            )
        if setting in RECORDER_SETTINGS:
            raise AssertionError(
                f"{setting!r} moves plugins and mints a key: it applies through "
                "apply_recorder in _run_settings_action, never a bare config write"
            )
        if setting is Setting.TRACKING_DEFAULT:
            state = setting_state(value)
            try:
                session_marker.write_default_state(state)
            except (OSError, ValueError, ConfigUnreadable) as exc:
                lines.append(f"! could not set the Probe default for new sessions: {exc}")
                continue
            lines.append(f"Probe in new sessions → {session_marker.state_label(state)}")
        elif setting is Setting.REASONING_SUMMARIES:
            lines.extend(reasoning_summaries.set_explicit(bool(value), reasoning_sources(caps_by_source)))
        elif setting is Setting.PASTED_IMAGES:
            try:
                session_marker.write_pasted_images(bool(value))
            except (OSError, ValueError, ConfigUnreadable) as exc:
                lines.append(f"! could not set image upload: {exc}")
                continue
            lines.append(f"Upload images you paste → {'on' if value else 'off'}")
        else:
            raise AssertionError(f"apply_settings has no writer for {setting!r}")
    return lines


def describe_settings(current: "dict[Setting, bool | str] | None" = None) -> list[str]:
    """The state block above the settings menu.

    `current` is the SAME snapshot the boxes are drawn from, when the caller
    has one -- the block and the picker must not read the config twice, or a
    write landing between the reads shows a state line disagreeing with the
    box beside it. Headless callers pass nothing and get a fresh read.

    Says what the default currently IS before offering to change it, and
    discloses the env override honestly: a RECOGNIZED value beats the config
    file, so moving the setting under it changes nothing visible -- but an
    unrecognized value (a typo like `of`) is IGNORED by `default_session_state`,
    and calling that an override would misdiagnose the typo as the row not
    working. BOTH variables are named, because either one can be the thing
    holding the row down and a block that disclosed only the older one would
    send someone hunting for a setting that is not the one winning. The value is
    printed through a printable-only filter and bounded, because the environment
    is not this program's to trust with raw escape sequences.
    """
    from probe.sdk import session_marker

    state = setting_state(
        current[Setting.TRACKING_DEFAULT]
        if current is not None
        else session_marker.default_session_state()
    )
    lines = [f"  {'Probe in new sessions':<28} {session_marker.state_label(state)}"]
    for name in ("PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING"):
        raw = os.environ.get(name) or ""
        if not raw.strip():
            continue
        recognized = session_marker.normalize_state(raw) is not None
        note = "env wins over this setting" if recognized else "unrecognized, ignored"
        shown = "".join(ch for ch in raw if ch.isprintable())[:32] or "<unprintable>"
        lines.append(f"  {name:<28} {shown}  ({note})")
    return lines


def settings_choices(
    current: "dict[Setting, bool | str]",
    indent: str,
    *,
    hidden: "frozenset[Setting]" = frozenset(),
    groups: "tuple[tuple[str, tuple[Setting, ...]], ...] | None" = None,
) -> tuple[
    list,
    dict[Setting, object],
    dict[Setting, tuple[str, tuple[str, ...]]],
    dict[Setting, dict[str, tuple[str, tuple[str, ...]]]],
]:
    """The settings screen's rows, and a handle on each one.

    Built here rather than inline so a test can render the REAL layout -- the
    one that decides where the cursor starts and which rows carry a box -- and
    not a rehearsal of it that drifts the first time this changes. (The same
    contract the capability picker's `capability_choices` carried before the
    install stopped having a picker.)

    BOTH copies come back, and the caller must hand them to `_bind_menu_keys`:
    it repaints rows from the copy it was handed, per state for a cycling row.
    """
    import questionary

    from probe.cli import tui

    cycles = cycling_settings()
    copy = dict(SETTINGS_COPY)
    # A cycling row wears its state as a WORD beside the title, not only as a
    # glyph: three shapes are learnable, but only after you have pressed the key
    # three times, and the state this row is in is the one thing a person must
    # be able to read without pressing anything.
    state_copy = {
        setting: {
            state: (f"{SETTINGS_COPY[setting][0]} — {value_label(setting, state)}", detail)
            for state, detail in per_state.items()
        }
        for setting, per_state in SETTINGS_STATE_COPY.items()
        if setting not in MENU_SETTINGS
    }
    rows: dict[Setting, questionary.Choice] = {}
    choices: list = []
    for group, settings in (grouped_settings() if groups is None else groups):
        visible = [s for s in settings if s not in hidden]
        if not visible:
            continue
        # A blank leads each group -- the first doubles as the air between the
        # question and the list (the 0.95.1 rule), the rest separate groups.
        # A blank FOLLOWS the heading for the same reason `step_heading` has
        # one: it is where the first row of the group paints the top of its
        # selection rectangle.
        choices.append(questionary.Separator(" "))
        choices.append(questionary.Separator(tui.heading(group)))
        choices.append(questionary.Separator(" "))
        for index, setting in enumerate(visible):
            if index:
                choices.append(questionary.Separator(" "))
            value = cycle_value(setting, current[setting]) if setting in cycles else bool(current[setting])
            title, detail = _row_copy(setting, copy, state_copy, value=value)
            row = questionary.Choice(
                title=_menu_row(title, detail, checked=value, indent=indent),
                value=setting,
                # A cycling row seeds its BOX from the first state, the only
                # thing a checkbox can say about three. `probe_cycle` carries
                # the rest and `_wire_picker.advance` keeps the two in step --
                # which is what the unwired fallback path falls back TO.
                checked=(value == cycles[setting][0]) if setting in cycles else value,
            )
            rows[setting] = row
            choices.append(row)
    return choices, rows, copy, state_copy


def run_settings_menu(
    current: "dict[Setting, bool | str]",
    *,
    hidden: "frozenset[Setting]" = frozenset(),
    groups: "tuple[tuple[str, tuple[Setting, ...]], ...] | None" = None,
    frame: "tuple[str, list[str], str] | None" = None,
):
    """The settings screen: the install panels' shape, pointed at what is left.

    Checkbox rows, ticked = on, grouped under headings like every other panel:
    Automatic updates and pasted-image uploads; a page handed `groups` draws its
    own rows, and a cycling row CYCLES rather than ticks (one state per press). Nothing
    is written while you press -- `→` on the `Set settings ›` band is the
    commit, and so is LEAVING: `←`/Escape after a change applies it too. They
    used to drop it without a word, and a researcher who switched a row and
    backed out found it reverted (2026-10-02). Returns None (quit), tui.BACK
    (left with nothing changed), or {Setting: bool | state}: the DRAWN rows as
    the user left them, a bool per checkbox and a STATE NAME per cycling row.

    `current` comes from the CALLER's read, never one of our own, so the boxes
    and the diff computed against what comes back are the same fact -- see
    `read_settings`.

    `hidden` names rows not to draw. `groups` and `frame` put another page on
    this machinery (the daemon's page, `DAEMON_GROUPS`).
    """
    import questionary

    from probe.cli import tui

    tui.use_checkmarks()  # the fallback path, if we cannot take the box over

    # The registry's fifth leg: a Setting added everywhere except
    # `read_settings` would otherwise surface as a raw KeyError drawing the
    # box, tracebacking the wizard instead of naming the drift.
    missing = [s for s in Setting if s not in current]
    if missing:
        raise AssertionError(f"read_settings reports no value for {missing}")

    indent = tui.body_indent()
    choices, rows, copy, state_copy = settings_choices(current, indent, hidden=hidden, groups=groups)
    cycles = {setting: order for setting, order in cycling_settings().items() if setting in rows}
    cycle_state = {setting: cycle_value(setting, current[setting]) for setting in cycles}

    # `frame`: another page on this screen's machinery (the daemon's page).
    message = tui.framed(*frame) if frame is not None else tui.framed(
        "Settings on this device:",
        [
            f"  {SETTINGS_COPY[setting][0]:<28} {'on' if current[setting] else 'off'}"
            for setting in (Setting.AUTO_UPDATE, Setting.PASTED_IMAGES)
        ],
        "How should this device behave?",
    )

    if not rows:
        # Unreachable today -- the Automatic updates row renders
        # unconditionally -- but kept as the guard for whatever hides rows
        # next: a picker with zero rows is a trap, so the degraded shape is
        # Back alone under the state block.
        choices = [
            questionary.Separator(" "),
            questionary.Choice(
                title=f"Back\n{indent}  Return to the main menu. Nothing changes.",
                value=tui.BACK,
            ),
        ]
        return tui.ask(
            tui.select(
                message,
                choices=choices,
                instruction="(enter goes back)",
                style=tui.style(),
                qmark=tui.qmark(),
                pointer=tui.pointer(),
            ),
            height=tui.content_height(message, choices),
        )

    choices.extend(nav_footer(next_title=APPLY_TITLE))
    instruction = "(enter picks this row · ↑ to change)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    # What the rows held when `←`/Escape left the screen, so leaving can keep it.
    left_with: dict = {}

    def keep_on_back(ctrl) -> None:
        left_with["selected"] = list(getattr(ctrl, "selected_options", None) or [])
        left_with["cycle"] = dict(getattr(ctrl, "probe_cycle", None) or {})

    control = _bind_menu_keys(
        question,
        rows,
        copy=copy,
        indent=indent,
        state_copy=state_copy,
        cycles=cycles,
        cycle_state=cycle_state,
        on_back=keep_on_back,
    )
    if control is None:
        # Unwirable -- same posture as the capability picker: strip the band
        # rather than ship a label nothing is listening for, and let the
        # library's own enter-submits apply the boxes.
        choices = without_nav(choices)
        instruction = "(space to toggle, enter to apply · esc goes back)"
        question = tui.checkbox(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
    else:
        dress_band(question, control)

    def answer(chosen: set, landed: dict) -> dict:
        # The cycling rows answer from `probe_cycle`, which is the only place
        # their third state can be written down. `control` is None only on the
        # unwired fallback, where questionary drew its own two-state box --
        # there the row answers from the box, meaning exactly what that boolean
        # has always meant (`setting_state`), rather than inventing a state
        # nobody could see.
        return {
            setting: (
                landed.get(setting, cycle_value(setting, setting in chosen))
                if setting in cycles
                else setting in chosen
            )
            for setting in rows
        }

    picked = tui.ask(question, height=tui.content_height(message, choices, instruction=instruction))
    if picked is tui.BACK and left_with:
        # Left with `←`/Escape: what was switched is kept, like `→` would.
        # Unchanged rows are still "nothing changed".
        kept = answer(set(left_with["selected"]), left_with["cycle"])
        drawn = {
            setting: cycle_value(setting, current[setting]) if setting in cycles else bool(current[setting])
            for setting in rows
        }
        return kept if kept != drawn else tui.BACK
    if picked is None or picked is tui.BACK:
        return picked
    landed = dict(getattr(control, "probe_cycle", None) or {}) if control is not None else {}
    return answer(set(picked), landed)


#: What the Defaults row says under its state while an environment variable
#: holds it (`session_marker.state_env_override`): choosing here would write a
#: config value the variable then overrides, so the row says where to go.
DEFAULT_ENV_LOCKED_NOTE = "Locked by an environment variable."


def tracking_default_row(state: "str | None" = None) -> tuple[str, tuple[str, ...]]:
    """The main menu's Defaults row: the setting's name, a state's word, and
    what that word means.

    `state` is what the row SHOWS -- the machine's default when not given, or
    where `←`/`→` have switched (and saved) it (`run_action_menu`). The
    chevrons round the word are the sign that the arrows move it; a row an
    environment variable holds down has none, because they would not.

    The meaning is the per-state disclosure (`SETTINGS_STATE_COPY`), so the
    words for each state live in one place whether they are read on the menu or
    on the picker behind it. Their leading blank line is dropped: it spaced the
    row on the old settings screen, and on the menu a row's detail sits
    directly under its title like every other row's.
    """
    from probe.sdk import session_marker

    held = session_marker.state_env_override() is not None
    here = setting_state(session_marker.default_session_state())
    state = setting_state(state) if state is not None else here
    name = SETTINGS_COPY[Setting.TRACKING_DEFAULT][0]
    word = session_marker.state_label(state)
    title = f"{name} — {word}" if held else f"{name}  ‹ {word} ›"
    detail = tuple(line for line in SETTINGS_STATE_COPY[Setting.TRACKING_DEFAULT][state] if line)
    if held:
        detail = (*detail, DEFAULT_ENV_LOCKED_NOTE)
    set_by = session_marker.set_by_note() if state == here else None
    if set_by:
        detail = (*detail, f"{set_by[0].upper()}{set_by[1:]}.")
    return title, detail


#: The main menu's Who records row: its name, and what each position means.
RECORDER_ROW_TITLE = "Who records"
RECORDER_ROW_COPY: dict[str, tuple[str, ...]] = {
    "agent": ("Your agents record and search Probe themselves.",),
    "daemon": (
        "The Probe daemon records and searches for your agents.",
        "Deletes go to the trash or ask first, unless prompts are off.",
    ),
}


#: The install's Defaults pick for Who records, while the install runs and only
#: when the person CHANGED the row (`main`): a newly set-up agent does not
#: follow the device's old recorder first (`follow_machine_recorder`) when the
#: pick moves every agent the other way right after.
INSTALL_RECORDER_PICK: ContextVar["str | None"] = ContextVar("install_recorder_pick", default=None)


def follow_machine_recorder(
    source: str,
    caps: "Capabilities | Callable[[], Capabilities]",
    *,
    base_url: str,
    rules: bool | None = None,
) -> list[str]:
    """A coding agent set up for the FIRST time joins the device's Who records:
    where the other agents record through the daemon, a new one starts there too
    (Richard 2026-10-06) instead of on its own. Only at first setup: an agent
    already set up never moves on its own, because who records decides what
    leaves the machine (`_run_recorder_action`).

    `caps` may be a callable that takes the snapshot, called only when the
    agent moves: the install calls this for every first setup, and most move
    nowhere."""
    from probe.sdk import session_marker

    from probe.cli.daemon_cli import ai_libraries

    daemon = session_marker.RECORDER_DAEMON
    if source not in RECORDER_SOURCES or session_marker.recorder(source) == daemon:
        return []
    if INSTALL_RECORDER_PICK.get() == session_marker.RECORDER_AGENT:
        return []  # the install's Defaults step moves every agent off the daemon next
    if not any(session_marker.recorder(other) == daemon for other in RECORDER_SOURCES if other != source):
        return []
    if not companion_token_held() or ai_libraries() is None:
        # Setting the daemon up here would open a browser mid-install.
        return [f"{agent_label(source)} records itself for now: the daemon is not ready on this device. "
                "`probe wizard` › Who records moves it."]
    lines = apply_recorder(caps() if callable(caps) else caps, daemon, base_url=base_url, rules=rules)
    return [f"{agent_label(source)}: Who records — the daemon, like this device's other agents.", *lines]


def machine_recorder() -> str:
    """This machine's Who records: `daemon` when any coding agent with a daemon
    profile records through it, else `agent`. One value for the machine (Richard
    2026-09-29: "no codex/claude split"); `apply_recorder` still moves each agent."""
    from probe.sdk import session_marker

    try:
        daemon = any(session_marker.recorder(s) == session_marker.RECORDER_DAEMON for s in RECORDER_SOURCES)
    except Exception:  # noqa: BLE001 - an unreadable config is the agent, today's profile
        daemon = False
    return session_marker.RECORDER_DAEMON if daemon else session_marker.RECORDER_AGENT


def recorder_row(
    value: "str | None" = None, caps_by_source: "dict | None" = None
) -> tuple[str, tuple[str, ...]]:
    """The main menu's Who records row, wearing `value` (the machine's when not
    given) between the chevrons that say `←`/`→` move it.

    On a machine on the daemon, a set-up agent still recording itself is named
    under it: the row read "daemon" while pi recorded itself (2026-10-02), and
    the Enter that moves it was nowhere on screen. Same set-up test as that
    Enter (`_run_recorder_action`): in `caps_by_source` and `configured`."""
    from probe.sdk import session_marker

    value = value or machine_recorder()
    copy = RECORDER_ROW_COPY[value]
    if value == session_marker.RECORDER_DAEMON and caps_by_source:
        behind = [
            source
            for source in RECORDER_SOURCES
            if source in caps_by_source
            and getattr(caps_by_source[source], "configured", False)
            and session_marker.recorder(source) != session_marker.RECORDER_DAEMON
        ]
        if behind:
            who = agent_label(tuple(behind))
            line = (
                f"{who} still records itself: Enter moves it to the daemon."
                if len(behind) == 1
                else f"{who} still record themselves: Enter moves them to the daemon."
            )
            copy = (*copy, line)
    return f"{RECORDER_ROW_TITLE}  ‹ {value} ›", copy


@dataclass(frozen=True)
class RecorderChoice:
    """The main menu's answer the moment its Who records row was switched: the
    value to apply, for every coding agent on this machine."""

    value: str


@dataclass(frozen=True)
class DefaultChoice:
    """A Defaults state to save with no picker. The menu row used to answer it
    on Enter; the row saves on each press now, and `_run_defaults_action`
    still takes one through `chosen=`."""

    state: str


class DefaultsRow(StrEnum):
    """The install's Defaults step, row by row: the main menu's Defaults group
    (who records, and what new sessions do) on a page of its own."""

    RECORDER = "recorder"
    SESSIONS = "sessions"


@dataclass(frozen=True)
class DefaultsPick:
    """What the install's Defaults step answered. HELD, never written by the
    step: the session default is saved at the Install keypress and Who records
    once the agents are installed (`main._apply_recorder_pick`), so backing
    out of the install leaves the device as it was."""

    recorder: str
    session_state: str


class ConsentView(StrEnum):
    """Which half of the daemon's consent a screen shows."""

    SUMMARY = "summary"
    DETAILS = "details"


#: The Probe daemon's consent, in the wizard. A daemon key minted from this
#: device's sign-in (`main._authorize_companion`) never opens the browser
#: approval, so these are the SAME words that page shows a daemon-only request:
#: `CONSENT_SUMMARY` and `GRANT_COPY[ApiGrant.Companion]` in
#: dashboard/src/lib/scopes.ts. `agent/tests/test_consent_copy_sync.py` holds
#: the two copies equal; change them together.
DAEMON_CONSENT_LEAD = "It will be able to:"
DAEMON_CONSENT_SUMMARY: tuple[str, ...] = (
    "Run the Probe daemon, which records as you",
    "Upload this device's coding-session transcripts",
    "Send session parts to an AI model, through Probe",
    "Upload project files it judges part of your work",
    "Trash research; remove papers, views, links for good",
)
DAEMON_CONSENT_DETAILS: tuple[str, ...] = (
    "Run the Probe daemon, which uploads this device's coding sessions and records your work in Probe as you",
    "Reads this device's coding sessions and uploads their transcripts to your team's knowledgebase.",
    "Transcripts carry your prompts and the images you paste into them, the assistant's replies and your shell commands — not file contents, not tool output.",
    "Images you paste are uploaded unscanned: a screenshot that shows a credential is uploaded with it. Turn that off in the Probe wizard's Settings.",
    "Uploads project files it judges part of your work's record, such as results and configs.",
    "Each file it uploads is scanned for secrets first: its first 16 MB, or 64 MB of a file that is not text.",
    "Files named like credentials are not uploaded unless you approve them; with your coding agent's permission prompts off, that approval is automatic.",
    "Sends parts of the session — command output and the files it reads included — to the AI model it runs on, through Probe, to decide what to record.",
    "Can read and write, and move runs, groups, experiments and projects to the trash.",
    "Never deletes a run, group, experiment or project permanently: Probe can restore trashed ones for 21 days.",
    "Can permanently remove recorded papers, views, lineage edges, and links between projects or to repositories. It asks you first, unless your coding agent's permission prompts are off.",
    "Credential-shaped values are replaced before upload — a filter, not a guarantee. Keep live credentials out of captured sessions.",
    "This device only. Turn it off any time from Integrations.",
)


def daemon_consent_lines(view: ConsentView, width: int) -> list[str]:
    """The daemon's consent as display lines `width` wide: the five-line summary,
    or every line. A bullet's wrapped lines hang under its text, not its mark."""
    from probe.cli import tui

    mark, items = (
        ("✓", DAEMON_CONSENT_SUMMARY) if view is ConsentView.SUMMARY else ("•", DAEMON_CONSENT_DETAILS)
    )
    lines = [DAEMON_CONSENT_LEAD]
    for item in items:
        first, *rest = tui.wrap(item, max(10, width - 2))
        lines.extend([f"{mark} {first}", *(f"  {line}" for line in rest)])
    return lines


def run_defaults_step(pick: DefaultsPick, *, agent_screen_shown: bool) -> "tuple[object, DefaultsPick]":
    """Install step 2: the main menu's Defaults group on a page of its own.

    Returns `(answer, pick)`: the answer is True (Next), tui.BACK or None
    (Ctrl-C), and `pick` is what the rows read when the page closed, kept by
    the caller so Back and forward again shows the same picks.

    The rows switch with `←`/`→` like the menu's (Enter switches too), but
    NOTHING is written here: the menu's rows save on each press, this page only
    answers (`DefaultsPick`). While Who records reads `daemon`, its row carries
    the daemon's consent (`DAEMON_CONSENT_SUMMARY`), and `d` swaps in every
    line (Tab is the page's own key for reading the text above the rows): the
    disclosure sits where the choice is made. An environment variable
    holding the session default down keeps that row still, as on the menu.
    """
    import questionary

    from probe.cli import tui
    from probe.sdk import session_marker

    daemon = session_marker.RECORDER_DAEMON
    cycles: dict = {DefaultsRow.RECORDER: (session_marker.RECORDER_AGENT, daemon)}
    if session_marker.state_env_override() is None:
        cycles[DefaultsRow.SESSIONS] = cycling_settings()[Setting.TRACKING_DEFAULT]
    start = {
        DefaultsRow.RECORDER: pick.recorder,
        DefaultsRow.SESSIONS: setting_state(pick.session_state),
    }
    view = {"consent": ConsentView.SUMMARY}
    indent = tui.body_indent()
    room = max(20, tui.box_width() - (2 + tui.BOX_GUTTER) - 2)

    def row_text(row: DefaultsRow, value: str) -> str:
        if row is DefaultsRow.RECORDER:
            title, detail = recorder_row(value)
            body = (
                daemon_consent_lines(view["consent"], room)
                if value == daemon
                else [line for item in detail for line in tui.wrap(item, room)]
            )
        else:
            title, detail = tracking_default_row(value)
            body = [line for item in detail for line in tui.wrap(item, room)]
        return f"\n{indent}  ".join([title, *body])

    rows = {row: questionary.Choice(title=row_text(row, start[row]), value=row) for row in DefaultsRow}
    choices: list = []
    for row in rows.values():
        choices.extend([questionary.Separator(" "), row])
    choices.extend(nav_footer())
    message = tui.framed(
        "Defaults",
        tui.wrap("Who records, and what new sessions do on this device. The menu's Defaults changes either later."),
        "How should Probe run here?",
    )
    instruction = "← → switch · d daemon details · enter · esc back · nothing is saved until Install"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    content = getattr(question, "_probe_content", None)
    if isinstance(content, dict):
        content["instruction"] = instruction  # the page's key line: these rows switch, they do not tick
    tui.draw_own_boxes(question)  # these rows switch; a ticked box would say otherwise

    def values(control) -> DefaultsPick:
        cycle = getattr(control, "probe_cycle", None) or {}
        return DefaultsPick(
            recorder=cycle.get(DefaultsRow.RECORDER, start[DefaultsRow.RECORDER]),
            session_state=cycle.get(DefaultsRow.SESSIONS, start[DefaultsRow.SESSIONS]),
        )

    def redraw(control) -> None:
        for row, choice in rows.items():
            choice.title = row_text(row, values(control).recorder if row is DefaultsRow.RECORDER
                                    else values(control).session_state)

    left: dict = {}
    control = _wire_picker(
        question,
        redraw=redraw,
        on_leave=lambda ctrl: True,
        on_back=lambda ctrl: left.update(pick=values(ctrl)),
        cycles=cycles,
        cycle_state=start,
    )
    if control is None:
        # questionary's internals moved and nothing here can switch: skip the
        # page with the device's values. The menu's Defaults still sets both.
        return True, pick
    tui.point_at(control, lambda value: value == NAV_BAND)
    dress_band(question, control)
    try:
        from prompt_toolkit.filters import Condition

        bindings = question.application.key_bindings
        pointed = lambda: getattr(control.get_pointed_at(), "value", None)  # noqa: E731

        def shift(delta: int):
            def _shift(event) -> None:  # pragma: no cover - requires a live terminal
                row = pointed()
                order = cycles[row]
                here = control.probe_cycle.get(row, order[0])
                control.probe_cycle[row] = order[(order.index(here) + delta) % len(order)]
                redraw(control)

            return _shift

        # Registered after `_wire_picker`'s `←`/`→` (Back/Next), so on a row
        # that switches these win; on the band those still go back and on.
        on_row = Condition(lambda: pointed() in cycles)
        bindings.add("left", eager=True, filter=on_row)(shift(-1))
        bindings.add("right", eager=True, filter=on_row)(shift(1))

        @bindings.add(
            "d",
            eager=True,
            filter=Condition(lambda: pointed() == DefaultsRow.RECORDER and values(control).recorder == daemon),
        )
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            view["consent"] = (
                ConsentView.DETAILS if view["consent"] is ConsentView.SUMMARY else ConsentView.SUMMARY
            )
            redraw(control)

    except Exception:  # noqa: BLE001 - Enter still switches a row; the band still works
        pass
    answer = tui.ask(
        question,
        height=tui.content_height(message, choices, instruction=instruction),
        margin=0,
        progress=install_header(STEP_DEFAULTS, agent_screen_shown=agent_screen_shown),
    )
    if answer is True:
        return True, values(control)
    return answer, left.get("pick", pick)


def run_daemon_consent(agent_sources: "tuple[str, ...] | list[str] | str"):
    """The daemon's consent before its key is minted from this device's sign-in
    (the main menu's Who records → daemon). Returns True (turn it on), False
    (keep the agents recording), tui.BACK or None.

    That key used to come from a browser approval, and the approval page was
    where the daemon was disclosed; minting it from the sign-in skips the page,
    so the same words show here (`DAEMON_CONSENT_SUMMARY`, every line one
    choice away). Turning it on is the first choice: the person just switched
    the row to the daemon.
    """
    from probe.cli import tui

    view = ConsentView.SUMMARY
    while True:
        lines = [
            *tui.wrap(
                f"It records for {agent_label(agent_sources)} on this device. No browser needed: "
                "this device's sign-in gives it its own key."
            ),
            "",
            *daemon_consent_lines(view, tui.CONTENT_WIDTH),
            "",
            "Turn it off any time: Who records ‹ agent ›.",
        ]
        toggle = (
            ("Show every detail", ConsentView.DETAILS)
            if view is ConsentView.SUMMARY
            else ("Show the summary", ConsentView.SUMMARY)
        )
        picked = tui.review(
            "Turn on the Probe daemon?",
            lines,
            [("Turn on the daemon", True), toggle, ("Keep my agents recording", False)],
        )
        if picked in (ConsentView.SUMMARY, ConsentView.DETAILS):
            view = picked
            continue
        return picked


#: The Defaults picker's forward label: the way forward IS the save.
SET_DEFAULT_TITLE = "Set default  ›"


def run_defaults_menu(current: "bool | str"):
    """Choose this machine's default for new sessions, from the main menu's
    Defaults row. Returns None (quit), tui.BACK, or a STATE NAME.

    The settings screen's shape and keys, as a RADIO: one row per state, each
    carrying that state's disclosure, the current one ticked. Enter (or space)
    ticks the row under the cursor, and `→` -- or Enter on `Set default ›` --
    saves the ticked one. LEAVING saves it too: `←`/Escape after ticking
    another state keeps it, where it used to be dropped (2026-10-02). The
    cursor opens on the band like every step, so Enter straight away saves
    what is already saved: nothing.

    Every state is offered, `off` included -- DELIBERATELY unlike the bare
    `/probe` switch, which is pressed blind mid-thought and must never land on
    a state that stops reads. This is a screen you are reading, and nothing is
    written until the save.

    The daemon is not a state here: it is the "Who records" setting.
    """
    import questionary

    from probe.cli import tui
    from probe.sdk import session_marker

    tui.use_checkmarks()  # the fallback path, if we cannot take the box over
    current = setting_state(current)
    order = cycling_settings()[Setting.TRACKING_DEFAULT]
    lines = describe_settings({Setting.TRACKING_DEFAULT: current})
    message = tui.framed(
        "Defaults on this device:", lines, "What should new sessions do?"
    )

    indent = tui.body_indent()
    copy = {
        state: (
            session_marker.state_label(state) + ("  (current)" if state == current else ""),
            tuple(line for line in SETTINGS_STATE_COPY[Setting.TRACKING_DEFAULT][state] if line),
        )
        for state in order
    }
    rows: dict[str, object] = {}
    choices: list = []
    for state in order:
        title, detail = copy[state]
        rows[state] = questionary.Choice(
            title=_menu_row(title, detail, checked=state == current, indent=indent),
            value=state,
            checked=state == current,
        )
        choices.extend([questionary.Separator(" "), rows[state]])
    choices.extend(nav_footer(next_title=SET_DEFAULT_TITLE))

    instruction = "(enter picks this row · → saves it)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    ticked = lambda control: next(  # noqa: E731 - one expression, used twice
        (value for value in control.selected_options if value in rows), current
    )
    left_on: dict = {}
    control = _bind_menu_keys(
        question,
        rows,
        copy=copy,
        indent=indent,
        exclusive=True,
        on_leave=ticked,
        on_back=lambda control: left_on.update(state=ticked(control)),
    )
    if control is None:
        # Unwirable: no band (nothing would be listening for it) and no radio
        # (nothing would keep it one tick). A plain list, where Enter IS the
        # choice, says exactly what it does.
        body = tui.body_indent()
        choices = []
        for state in order:
            title, detail = copy[state]
            choices.append(questionary.Separator(" "))
            choices.append(
                questionary.Choice(
                    title="\n".join([title, *(f"{body}  {line}" for line in detail)]),
                    value=state,
                )
            )
        instruction = "(enter chooses · esc goes back)"
        question = tui.select(
            message,
            choices=choices,
            default=current,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
    else:
        dress_band(question, control)
    picked = tui.ask(
        question, height=tui.content_height(message, choices, instruction=instruction)
    )
    if picked is tui.BACK and left_on.get("state", current) != current:
        # Left with `←`/Escape after ticking another state: keep it.
        return left_on["state"]
    return picked


def locally_paired_capture(sources: tuple[str, ...] | list[str] | str) -> list[str]:
    """The agents whose capture credential THIS DEVICE stores, so a sign-in can
    re-pair them under the new account.

    An environment-variable credential is deliberately not one of them: the
    wizard cannot unset a variable in the parent shell, so re-pairing would mint
    a token the environment then shadows -- capture would keep uploading to the
    old account while the run reported it re-paired.
    """
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    return [
        source
        for source in normalized
        if {TokenSource.PAIRED_FILE, TokenSource.PROBE_CONFIG} & set(capture_token_sources(source))
    ]


def _revoke(token: str, *, base_url: str, what: str) -> list[str]:
    """Release one credential from THIS machine, best-effort, and say which one.

    A credential nobody holds any more is not harmless: it stays valid until it
    expires, and once the local copy is gone the user has nothing left to revoke
    it WITH. Failure is reported, never raised -- being unable to reach the API
    must not stop a sign-out from clearing the disk.

    REPORTS WHAT ACTUALLY HAPPENED, which is the whole reason this is not just a
    revoke any more. The same PAT may be serving another machine, and the server
    detaches rather than revokes in that case; saying "Revoked" there would tell
    the user they had disconnected a laptop that is still working perfectly.

    An older or self-hosted backend answers 204 with no body and revokes
    globally -- it has never heard of the device header. We cannot make that
    server safe from here, so we say what we know rather than claiming a clean
    rotation we cannot prove.
    """
    from probe.sdk import errors
    from probe.sdk.client import Client
    from probe.sdk.surface import Surface
    from probe.sdk.config import Settings, resolve

    endpoint = base_url or resolve().base_url
    try:
        with Client(
            settings=Settings(base_url=endpoint, token=token),
            async_writes=False,
            surface=Surface.CLI.value,
        ) as client:
            result = client.logout()
    except (errors.AuthError, errors.NotFoundError):
        # Already gone. On a current backend the EXCHANGE revokes the replaced
        # credential as part of the rotation, so by the time we get here the
        # token no longer authenticates and the server answers 401 -- which maps
        # to AuthError, not NotFoundError. Catching only 404 made every re-run of
        # `probe setup` print "could not release ..." for work that had already
        # succeeded. Both statuses mean the same thing here: nothing to release.
        return []
    except Exception as exc:  # noqa: BLE001 - offline is a message, not a crash
        return [
            f"! could not release {what} ({exc}). "
            "Revoke it in the dashboard under Settings > Connected clients."
        ]
    if not isinstance(result, dict) or "revoked" not in result:
        # No body: a backend that predates device-aware release. It revoked
        # globally, which is what it has always done.
        return [f"Revoked {what}."]
    if result.get("detached") and not result.get("revoked"):
        others = result.get("still_used_by") or []
        named = ", ".join(str(name) for name in others[:3])
        suffix = f" ({named})" if named else ""
        return [
            f"Disconnected {what} from this machine; "
            f"it is still in use on {len(others)} other device"
            f"{'' if len(others) == 1 else 's'}{suffix}."
        ]
    return [f"Revoked {what}."]


def _env_credential_warnings() -> list[str]:
    """Name every credential still live in the shell after a sign-out."""
    live = [name for name in ENV_CREDENTIALS if (os.environ.get(name) or "").strip()]
    if not live:
        return []
    one = len(live) == 1
    return [
        f"! {', '.join(live)} {'is' if one else 'are'} still set in your shell and "
        f"{'outranks' if one else 'outrank'} the file this just cleared.",
        f"  This process cannot unset {'it' if one else 'them'} for you — run "
        f"`unset {' '.join(live)}` and remove the line from your shell profile.",
    ]


def prior_account(caps_by_source: dict) -> str | None:
    """The account this device is CURRENTLY set up for, or None.

    The verified `logged_in_as` when one resolved, and deliberately nothing
    otherwise: a device that is offline, or whose saved token has been revoked,
    cannot have its account NAMED, and a guessed name is worse than no name on
    both of the screens that read this. Absent here therefore means "we cannot
    say", never "there is nobody" -- `saved_accounts()` is what answers whether
    a credential exists at all.
    """
    return next(
        (snapshot.logged_in_as for snapshot in caps_by_source.values() if snapshot.logged_in_as),
        None,
    )


def install_client_context(caps_by_source: dict) -> dict:
    """The display-only context the guided install sends to the approval page.

    `prior_email` is `prior_account` -- the account this device is currently set
    up for, omitted when it could not be resolved (an offline device gets no
    mismatch warning rather than a guessed one). `install: True` is what tells
    the page to stay open after approval and wait for the wizard's completion
    registration. The page treats every field as the CLI's claim; nothing
    authorizes against it.
    """
    prior = prior_account(caps_by_source)
    context: dict = {"install": True}
    if prior:
        context["prior_email"] = prior
    return context


def account_switch_refusal(previous: str) -> list[str]:
    """The headless answer to an install code on a device signed in as someone else.

    Here rather than inline in main.py so the refusal and the test that pins it
    read one string. It names the flag that consents on purpose: a refusal that
    only says no turns a one-flag fix into a support thread.
    """
    return [
        f"! This device is signed in as {previous}, and a website install code signs in "
        "as whoever generated it.",
        "  Redeeming it would replace that account here and release this device's current "
        "credentials, which cannot be undone from this end.",
        "  Re-run with `--yes` to switch accounts anyway, or run `probe wizard` from a "
        "terminal to be asked.",
    ]


def run_confirm_account_switch(previous: str):
    """The gate in front of an install code on an already-signed-in device.
    Returns None (Ctrl-C), tui.BACK, or a bool.

    BEFORE THE EXCHANGE, and that ordering is the whole design. A website code
    carries its own identity: redeeming it binds this device to whoever
    generated it, and the exchange DETACHES the credentials that were bound
    here (see `revoke_replaced_token`, and the rotation block in the backend's
    device exchange). By the time we could name the new account, the old one is
    already gone from this device and there is nothing left to roll back to --
    so the only honest place to ask is here, where the only account we can name
    is the one being replaced.

    Defaulting to False for the same reason `confirm_removal` does: the
    keystroke that costs something is the one that must be typed, not the one
    that is already under the cursor.
    """
    import questionary

    from probe.cli import tui

    message = tui.framed(
        "This device is already signed in.",
        [
            *tui.wrap(f"Signed in as {previous}."),
            "",
            *tui.wrap("The website code signs in as whoever made it."),
            *tui.wrap(
                "Continuing replaces the account saved here and releases this "
                "device's credentials. Data already sent to your team stays."
            ),
        ],
        "Continue with the account from the website code?",
    )
    choices = [
        questionary.Choice("Keep current account", value=False),
        questionary.Separator(" "),
        questionary.Choice("Continue with website code", value=True),
    ]
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            default=False,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
            instruction=" ",
        ),
        height=tui.content_height(message, choices),
    )


def revoke_replaced_token(previous: dict, granted: dict, *, base_url: str) -> list[str]:
    """After a mint replaced this device's credentials, release the old ones.

    The always-browser install re-mints even on a signed-in device, and
    `authorize` only overwrites the LOCAL copy — without this, every re-run
    leaves another live token behind that nobody holds. Same rule `sign_in` has
    always applied: release AFTER the mint (releasing first would leave a
    refused approval with no credentials at all), and only when the token
    actually changed.

    RELEASE, NOT REVOKE, is the change. The old credential is unbound from THIS
    machine and dies only if no other device still holds it, so rotating a PAT
    that a second laptop is also using no longer signs that laptop out. On a
    current backend the exchange has usually revoked it already, which arrives
    here as a 404 and is silently correct.
    """
    if "api" not in granted:
        return []
    lines: list[str] = []
    replaced = str(previous.get("token") or "")
    if replaced and replaced != granted["api"].get("token"):
        lines += _revoke(
            replaced,
            base_url=str(previous.get("base_url") or base_url),
            what="the token this device was using before",
        )
    # The mint replaces the READ token in the same write, and an orphaned
    # read-capable credential is still a credential. Best-effort like the PAT:
    # `_revoke` is a self-logout, and a token that cannot revoke itself gets
    # the dashboard pointer instead of a crash.
    replaced_mcp = str(previous.get("mcp_token") or "")
    minted_mcp = (granted.get("mcp") or {}).get("token")
    if replaced_mcp and replaced_mcp != minted_mcp:
        lines += _revoke(
            replaced_mcp,
            base_url=str(previous.get("base_url") or base_url),
            what="the read-only MCP token this device was using before",
        )
    # KNOWN LIMIT: a capture daemon already running holds its ingest token in
    # memory until its session ends, and replaced capture DEVICE tokens are
    # retired by re-pairing, not here — the same boundary sign_in has.
    return lines


@dataclass(frozen=True)
class SignInResult:
    """Whether this device came out of the flow signed in, and what to print.

    Two fields because neither implies the other: a sign-in that SUCCEEDED can
    still print warnings -- a capture grant the server declined, a previous
    token we could not revoke -- so "does any line look like a failure" is the
    wrong question to ask about whether the credential landed.
    """

    ok: bool
    lines: list[str]


def sign_in(
    *,
    base_url: str,
    sources: tuple[str, ...] | list[str] | str = ("claude_code",),
    on_prompt=None,
    open_browser: bool = True,
    install_code: str | None = None,
    prepare_install: bool = False,
) -> SignInResult:
    """Approve this device in the browser and save what it mints over the active
    account.

    Re-runnable on a machine that is ALREADY signed in, which is the whole point:
    `needs_authorization` skips the browser for a device that holds a credential,
    so before this existed a wrong-account install had no path forward inside the
    wizard at all.

    Capture already paired on the device rides along so it cannot keep uploading
    to the previous account. Wizard entry also prepares capture for unpaired
    sources in this same approval; those credentials remain disabled until the
    install confirmation. An environment-only credential is left to its owner.
    """
    from probe.sdk.config import current_context_name, load_context

    # The FILE, not `resolve()`: an exported PROBE_TOKEN belongs to whoever
    # exported it (CI, a colleague's shell profile) and is not ours to revoke.
    previous = load_context()
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    repair = locally_paired_capture(normalized)
    new_capture = (
        [
            source
            for source in normalized
            if not has_source_capture_grant(source, capture_token_sources(source))
        ]
        if prepare_install
        else []
    )
    requested_capture = list(dict.fromkeys([*repair, *new_capture]))
    grants = ["api", "mcp"] + (["capture"] if requested_capture else [])
    from . import identity_check, install_pipeline

    # A sign-in starts: the OS keeper may come back (R1), and what is queued
    # under the credential this replaces goes BEFORE the exchange, which
    # releases it on the server (plan clean-uninstall-reinstall R-T4, R8).
    install_pipeline.clear_keeper_off()
    drained = identity_check.drain_before_switch() if previous.get("token") else []

    granted, messages = authorize(
        grants,
        base_url=base_url,
        capture_sources=requested_capture or None,
        **({"defer_capture_sources": new_capture} if prepare_install else {}),
        on_prompt=on_prompt,
        open_browser=open_browser,
        **({"install_code": install_code} if install_code is not None else {}),
    )
    messages = [*drained, *messages]
    if "api" not in granted:
        return SignInResult(
            ok=False,
            lines=[
                *messages,
                "! Sign-in did not complete — this device is still using the credentials it had.",
            ],
        )

    if not prepare_install:
        for source in repair:
            # Explicit sign-in restores existing pairings. Wizard entry leaves
            # every capture switch as it was until installation is confirmed.
            with agent_target(source):
                clear_killswitch()

    # The email is a courtesy, not a requirement: an endpoint that answered the
    # approval can still be unreachable a second later, and the credential is
    # already saved by then. Name whoever we can, and say the rest regardless.
    email = account_email(base_url)
    lines = [
        f"Signed in {f'as {email} ' if email else ''}at {base_url} "
        f"(saved account: {current_context_name()}).",
        *messages,
    ]
    replaced = str(previous.get("token") or "")
    if replaced and replaced != granted["api"].get("token"):
        # AFTER the mint, never before: revoking first would leave a refused
        # approval with no credentials at all.
        lines.extend(
            _revoke(
                replaced,
                base_url=str(previous.get("base_url") or base_url),
                what="the token this device was using before",
            )
        )
    if previous.get("companion_token"):
        # The daemon key an earlier sign-in left: it must be this account's
        # (R5: it stayed, and the daemon wrote to the old team).
        held = identity_check.reconcile(base_url=base_url)
        lines.extend(held.lines)
        lines.extend(f"! {problem}" for problem in held.problems)
    return SignInResult(ok=True, lines=lines)


#: `release_credentials`' words when the saved credentials stayed on disk:
#: the sign-out and Uninstall pages must not say "signed out" then.
CREDENTIALS_NOT_CLEARED = "could not clear the saved credentials"


def release_credentials() -> list[str]:
    """Revoke this device's saved account and clear it off the disk.

    The credential half of BOTH `sign_out` and Uninstall, so the two can never
    drift into releasing different things. It is device-wide, not per agent --
    there is one config file -- which is why a wizard pass that walks several
    coding agents calls it once, after the last of them.

    Everything here is best-effort and ordered so a failure leaves the machine
    better off, never worse: revoke while we still hold the secret, and clear
    the disk even when the network call did not land.
    """
    from probe.sdk.config import clear_context, current_context_name, load_context

    context = current_context_name()
    stored = load_context()
    # What removed Capy capture left here (its key, credential and timer) goes
    # with the account, not on the old timer's schedule.
    from . import capy_retire

    lines: list[str] = capy_retire.retire()

    if stored.get("token"):
        lines.extend(
            _revoke(
                str(stored["token"]),
                base_url=str(stored.get("base_url") or ""),
                what="this device's API token",
            )
        )
    # THE READ TOKEN IS A CREDENTIAL TOO, and sign-out used to walk past it.
    # Only `token` was released here, so `clear_context` below wiped the local
    # copy of `mcp_token` while the credential itself stayed LIVE server-side --
    # and Codex keeps its own copy in ~/.codex/config.toml, which nothing here
    # touched. A machine someone had signed out of therefore kept working
    # read access to the team's research through Codex. Read-only, and still
    # not something "sign out" is allowed to leave behind.
    #
    # The mint path already got this right (`revoke_replaced_token` releases
    # the replaced `mcp_token`); this is the same release on the way out.
    if stored.get("mcp_token"):
        lines.extend(
            _revoke(
                str(stored["mcp_token"]),
                base_url=str(stored.get("base_url") or ""),
                what="this device's read-only MCP token",
            )
        )
    # Then the copy we do not own the lifetime of. Dropping the whole table is
    # what `remove_everything` already does at uninstall, and for the same
    # reason: an entry left pointing at the hosted MCP with a released token
    # reads as installed and answers 401.
    try:
        if codex_config.configured_bearer(CODEX_MCP_NAME):
            codex_config.remove_mcp_server(CODEX_MCP_NAME)
            lines.append("Removed the Codex MCP entry that held this account's read token.")
    except (codex_config.ConfigError, OSError) as exc:
        lines.append(f"! could not clear the Codex MCP entry ({exc}); remove it by hand.")
    # Only the ACTIVE account, like `probe logout`: clearing the file would sign
    # the user out of every other endpoint saved here, which is not what
    # "sign out" means to anyone.
    #
    # Guarded because this also runs on the way out of Uninstall, where a
    # config file too corrupt to rewrite (`ConfigUnreadable`) must not end a
    # removal in a traceback on a machine whose plugins are already gone.
    try:
        clear_context(context)
    except Exception as exc:  # noqa: BLE001 - an unwritable config is a message, not a crash
        lines.append(
            f"! {CREDENTIALS_NOT_CLEARED} ({exc}). "
            "Delete them by hand, or move the config aside to start fresh."
        )
    else:
        lines.append(f"Signed out. The credentials saved here (account: {context}) are cleared.")
    lines.extend(_env_credential_warnings())
    return lines


def sign_out(sources: tuple[str, ...] | list[str] | str = ("claude_code",)) -> list[str]:
    """Clear this device's saved credentials, and stop everything still using them.

    NOT an uninstall: the plugins stay, so signing back in is one screen away.
    What goes is the ACCOUNT -- the API token (revoked server-side too, so it
    cannot outlive the machine that forgot it) and every capture credential that
    would otherwise keep shipping this device's sessions to the account the user
    just left.
    """
    from . import import_jobs

    import_jobs.clear_all()
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    lines: list[str] = ["Imports stopped and local import history cleared."]

    # Capture FIRST: it is the half with a running process behind it, and
    # `turn_off` verifies its own postcondition by re-resolving every source.
    # Clearing the config out from under it would leave that verification
    # reading a state nobody set.
    for source in normalized:
        if not capture_token_sources(source):
            continue
        with agent_target(source):
            result = turn_off(OffMode.DISABLE)
        lines.append(f"{agent_label(source)}: {result.summary()}")
        lines.extend(f"! {warning}" for warning in result.warnings)

    lines.extend(release_credentials())
    lines.append("The plugins are still installed. Uninstall Probe removes them.")
    return lines


def confirm_remove_account(name: str):
    """The gate before a saved account is deleted: keeping it is listed first,
    so the cursor starts on the choice that costs nothing. Returns None,
    tui.BACK, or a bool."""
    from probe.cli import tui

    return tui.review(
        f"Remove the account saved as “{name}”",
        tui.wrap(
            "Deletes it from this device. Your current account is not touched."
        ),
        [("Keep it", False), ("Remove it", True)],
    )


def remove_account(name: str) -> list[str]:
    """Delete a saved account that is NOT the active one (`probe context delete`
    before it was removed). The active one leaves by Sign out, which also
    revokes its token and stops capture."""
    from probe.sdk.config import delete_context

    if next((a for a in saved_accounts() if a.name == name and not a.active), None) is None:
        return [f"No other account is saved as “{name}”; nothing was removed."]
    delete_context(name)
    return [f"Removed the account saved as “{name}”."]


def switch_account(
    name: str, sources: tuple[str, ...] | list[str] | str = ("claude_code",)
) -> list[str]:
    """Make one of the accounts already saved here the active one.

    Purely local: nothing is minted, revoked, or sent. That is what makes it
    worth having beside sign-in -- someone who works across two teams should not
    need a browser round trip to move between credentials this machine already
    holds.
    """
    from probe.sdk.config import DEFAULT_BASE_URL, load_context, resolve, use_context

    use_context(name)
    stored = load_context(name)
    endpoint = str(stored.get("base_url") or resolve().base_url)
    if not stored.get("token"):
        lines = [
            f"Now using the account saved as “{name}” ({endpoint}).",
            f"It holds no credential yet — `probe wizard --action login --context {name}` signs in to it.",
        ]
    else:
        # Who it is, in one line: the server only when it is not Probe's own.
        email = account_email(endpoint)
        who = [part for part in (email, endpoint if endpoint.rstrip("/") != DEFAULT_BASE_URL else None) if part]
        lines = [f"Now using “{name}”" + (f" ({' at '.join(who)})." if who else ".")]

    # `ingest_token` lives INSIDE the context, so it follows the switch. A
    # paired device token does not: it is one file per agent, minted by whoever
    # approved it, and it keeps uploading there. Switching accounts silently
    # would send this device's transcripts to the team just switched away from.
    # One line naming them all, not the same sentence per agent.
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    paired = [source for source in normalized if TokenSource.PAIRED_FILE in capture_token_sources(source)]
    if paired:
        lines.append(
            f"! Session capture for {spoken_list([agent_label(source) for source in paired])} still "
            "uploads to the account that paired it. `probe wizard --action login` re-pairs it to this one."
        )
    return lines


def remove_everything(caps: Capabilities) -> list[str]:
    """Take ONE coding agent back to nothing, and VERIFY the capture half.

    Replaces the page's "Remove the plugin" section, which only told you to
    uninstall -- and warned that uninstalling does not revoke credentials.
    Doing it here means we can actually clear them and prove capture stopped,
    rather than leaving the user to notice.

    Per agent, so a device with both Claude Code and Codex runs this twice. The
    ACCOUNT is not part of it -- there is one config file, not one per agent --
    and `finish_removal` releases that once, after the last pass through here.

    NOTHING DEVICE-WIDE either (`probe wizard --action uninstall --agent A`,
    the only caller): the import jobs (one job imports several agents' sessions,
    and a folder import is no agent's; there is no per-agent clear) and the
    automatic-updates choice (one device-wide file, `autoupdate`) stay. The
    whole-device `probe uninstall` removes both with the rest of Probe's state.
    """
    messages: list[str] = []
    result = turn_off(OffMode.UNINSTALL)
    messages.append(result.summary())
    messages.extend(f"! {warning}" for warning in result.warnings)

    # `uninstall_plugin` returns a Result, not a 2-tuple. Unpacking it raised
    # TypeError on the FIRST line of removal that touches a plugin, so
    # `probe wizard --action uninstall` crashed for everyone -- after the
    # plugins were gone, before the instruction block, the auto-update flag and
    # (below) the Codex MCP entry were dealt with. A half-removed machine that
    # ends in a traceback, and no test caught it because none called this.
    tracking_name = tracking_plugin_name(caps.agent_source)
    removal = uninstall_plugin(tracking_name)
    if not removal.ok and "not found" not in removal.detail.lower():
        messages.append(f"! could not remove {tracking_name}: {removal.detail}")
    elif tracking_name == DAEMON_PLUGIN_NAME:
        # Removed means back to nothing: a later install starts on today's profile.
        messages.extend(_forget_recorder(caps.agent_source))
    if caps.agent_source in reasoning_summaries.SOURCES:
        messages.extend(reasoning_summaries.undo_for_agent(caps.agent_source))

    from probe.harness import get_registry

    if get_registry().get(caps.agent_source).statusline:
        messages.extend(remove_statusline())

    # The MCP entry we may have written into the user's own config.toml is not
    # ours to leave behind: after this call its token is orphaned, so Codex
    # would keep a server that lists as configured and answers 401.
    if caps.agent_source == "codex":
        try:
            removed = codex_config.remove_mcp_server(CODEX_MCP_NAME)
        except codex_config.ConfigError as exc:
            messages.append(
                f"! left the Codex MCP entry in place: {exc}. "
                f"Delete [mcp_servers.{CODEX_MCP_NAME}] by hand."
            )
        else:
            if removed.changed:
                messages.append(f"Removed the {CODEX_MCP_NAME} MCP entry from {removed.path}.")

    # The block lives OUTSIDE the repo, in the researcher's global CLAUDE.md,
    # and removal used to skip it entirely -- so "Removed." left every agent in
    # every repository still being told to use skills this very call had just
    # uninstalled. It also keeps `Capabilities.configured` True forever, so a
    # fully removed device can never look fresh again.
    messages.extend(apply_agent_rules(False))

    # `.disabled` is written by the teardown above to stop a session that starts
    # mid-uninstall from respawning the uploader. Once the plugin is gone and
    # `verified` says no credential resolves ANYWHERE (an exported ingest token
    # included), it guards nothing and only makes the device look half-off
    # forever. Both halves of that condition matter: a marker cleared while a
    # surviving plugin can still read an environment credential would turn
    # capture back on, which is the one thing this file may never do quietly.
    if result.plugin_removed and result.verified:
        clear_killswitch()

    # NOT the account: that is `finish_removal`, once for the device, after the
    # last coding agent has run through here. Releasing it from inside this
    # function would revoke the credential that the NEXT agent's pass -- and
    # this one's own capability registration -- still has to authenticate with.
    messages.append("Removed.")
    return messages


def finish_removal() -> list[str]:
    """The device half of Uninstall: sign out, then say what survives.

    Uninstall used to stop at the plugins and TELL the user their account was
    still signed in here, pointing them at Settings to revoke the tokens by
    hand. So a reinstall skipped the browser entirely -- `needs_authorization`
    reads a stored token as "already signed in" -- and a machine somebody had
    deliberately removed Probe from kept a live API token, a live read-only MCP
    token, and enough saved state that the wizard could never show it as fresh.

    Runs ONCE per wizard pass, after every selected agent has been torn down and
    has reported its emptied state to the server: that report authenticates with
    the very token this releases, so doing it any earlier turns the last agent's
    registration into a 401 and leaves the dashboard showing a device that is
    gone.
    """
    # The OS keeper (D35) would start the Probe service again: the system stops running it.
    with contextlib.suppress(Exception):
        from probe.service import keeper

        keeper.remove()
    return [
        *release_credentials(),
        "Setting Probe up again will ask you to sign in.",
        "Data already sent to your team stays.",
    ]


#: What a Codex that just got the capture plugin still needs from a person.
CODEX_HOOK_STEPS = (
    "In the new session: `/hooks` › approve Probe Session Capture.",
    "Until you do, capture is installed but sends nothing.",
)


def install_next(
    caps: Capabilities, selection: Selection, *, codex_hooks_approved: bool = False
) -> tuple[bool, list[str]]:
    """`restart_notice` for the final summary (`RunSummary`): whether the
    agent needs a restart to load Probe, and the one step besides it that
    matters (Codex's hook approval). "Nothing to restart" and the like are the
    routine report, left off."""
    steps = restart_notice(caps, selection, codex_hooks_approved=codex_hooks_approved)
    restart = bool(steps) and steps[0].startswith("Restart ")
    must = []
    if CODEX_HOOK_STEPS[0] in steps:
        must.append("approve Probe Session Capture under `/hooks` in its new session; until then capture sends nothing.")
    # Tracking turned off: open sessions still carry Probe until they restart.
    must += [step for step in steps if step.startswith("Open ")]
    return restart, must


def restart_notice(
    caps: Capabilities, selection: Selection, *, codex_hooks_approved: bool = False
) -> list[str]:
    """What the user still has to do, one short line each.

    Returned as separate lines rather than a paragraph because this is rendered
    as a bulleted "What's next" list: a three-sentence blob in one bullet is the
    thing nobody reads, and the sentence people were missing -- approve the hook
    or capture sends nothing -- was the last one in it.

    Plugin installs and the MCP wiring only take effect on restart -- Claude
    Code reads them at session start and `probe` cannot restart it. Without this
    line someone finishes the wizard, sees "done", and finds none of it working
    in the session they are sitting in. That is the last mile of the exact
    problem this whole feature exists to solve.

    Only shown when a plugin actually changed, so a re-run that only flipped
    auto-update does not send anyone off to restart for nothing.
    """
    current = caps.enabled()
    plugin_changed = (
        selection.tracking != current[Capability.TRACKING]
        or selection.capture != current[Capability.CAPTURE]
        or caps.legacy_capture_plugin_installed
    )
    if not plugin_changed:
        return []
    if caps.agent_source == "pi":
        # `plugin_changed` can now fire for tracking as well as capture (pi is
        # no longer forced capture-only), and both land on the SAME idempotent
        # packages-entry write -- so the notice names the package rather than
        # the token. There is no `pi_available` capability
        # field to gate on the way codex_available/claude_available do (see
        # doctor.render()'s own note on why one was not invented) -- and
        # nothing to gate on anyway, since pairing capture never depended on
        # a marketplace install. The old two-way ternary's silent `else` said
        # "Restart Claude Code" here, which is wrong about a run that was
        # never about Claude Code and tells the researcher to go restart an
        # agent that has nothing to do with the token they just paired.
        if not selection.capture:
            # The OFF direction. `apply_capture`'s teardown (`turn_off`) has
            # already stopped any capture daemons and set the killswitch
            # synchronously, by the time this function runs -- there is no
            # pi session state a restart would flip, so "restart to take
            # effect" is backwards here: the effect already took. A truthful
            # line beats an empty list -- `plugin_changed` only fires this
            # branch because capture visibly changed, and the researcher who
            # just watched that happen deserves confirmation, not silence.
            return ["Capture is off for future pi sessions; nothing to restart."]
        return ["Restart pi to load Probe."]
    # No agent CLI, no restart to give: the degraded install skipped the
    # plugin work and already printed the real next step (install the agent,
    # re-run Install). "Restart Claude Code" about a Claude that is not on
    # the machine reads as success guidance for work that never ran.
    if caps.agent_source == plugin_cli.KIMI:
        from probe.cli import kimi_config

        if not kimi_config.binary_available():
            return []
        # Kimi loads plugins at session start; an open TUI picks them up on /reload.
        return ["Restart Kimi Code (or run /reload in an open session) to load Probe."]
    if not (caps.codex_available if caps.agent_source == "codex" else caps.claude_available):
        return []
    agent = "Codex" if caps.agent_source == "codex" else "Claude Code"
    # A restart only where it is still true: a plugin an open session never
    # loaded (installed now, or the legacy capture plugin replaced). A plugin
    # already there is followed without one: its hooks read the switch at the
    # next event, so "Restart Claude Code to load Probe" for those sent people
    # off to restart for nothing.
    installed_now = (
        (selection.tracking and not caps.tracking_plugin_installed)
        or (selection.capture and not caps.capture_plugin_installed)
        or caps.legacy_capture_plugin_installed
    )
    if installed_now:
        steps = [f"Restart {agent} to load Probe."]
        if caps.agent_source == "codex" and selection.capture and not codex_hooks_approved:
            # Codex will not run a hook nobody trusted, and it says nothing when it
            # declines. Without this line capture looks installed and sends nothing.
            # Not when this run approved Probe's hooks itself (`approve_codex_hooks`).
            steps.extend(CODEX_HOOK_STEPS)
        return steps
    steps = []
    if selection.capture and not current[Capability.CAPTURE]:
        # The killswitch is gone: the capture hook each open session already
        # runs starts its recorder again at a prompt (at most every 10 minutes).
        steps.append(f"No restart needed: open {agent} sessions resume capture within minutes.")
    elif not selection.capture and current[Capability.CAPTURE]:
        # `turn_off` stopped every capture daemon and set the killswitch already.
        steps.append("Capture is off, for open sessions too; nothing to restart.")
    if not selection.tracking and current[Capability.TRACKING]:
        steps.append(f"Open {agent} sessions keep Probe until they restart; new ones start without it.")
    return steps
