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
import sys
from dataclasses import dataclass

from probe.cli.wizard.apply import agent_rules
from probe.cli.wizard.state.state import (
    Capabilities,
    Capability)
from probe.cli.wizard.screens.confirm import MENU_COPY

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
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.agent_files import statusline_catch_up_due  # noqa: E402 -- pieces need each other; the front door loads this one first
