"""the final page of an install or an Update: per-agent results, the lines needing attention, and what the user still has to do (restart notice)."""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from probe.foundation.compat.compat import StrEnum
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.state import (
    Capabilities,
    Capability)


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
        lines = [self._get_headline(len(worked), len(self._sources))]
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
        from probe.cli.install import upgrade as upgrading

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

    def _get_headline(self, worked: int, total: int) -> str:
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
        from probe.shared.harness.harnesses.kimi_code import config as kimi_config

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
from probe.cli.wizard.agents import agent_label, agents_counted, spoken_list  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.wizard import Selection  # noqa: E402 -- pieces need each other; the front door loads this one first
