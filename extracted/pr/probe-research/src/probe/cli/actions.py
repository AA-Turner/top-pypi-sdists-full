"""Everything the onboarding page used to hide in collapsed sections.

The dashboard had five `<details>` blocks -- set up manually, if something is
not working, update, remove, without Claude Code -- each duplicating commands
that also lived in two other places. All of it belongs HERE, next to the state
it acts on: the wizard already knows what is installed, what is paired, and
whether the last update worked, so it can do these instead of describing them.

The page keeps one command. This module is what that command opens into.

stdlib only, and imported lazily from cli/main.py -- `probe log` runs inside
training loops and must not pay for any of this.
"""

from __future__ import annotations

from probe._compat import StrEnum

from probe.cli.capabilities import (
    AGENT_INSTALL,
    MARKETPLACE_REPO,
    PLUGIN_ID,
    TAP_PLUGIN_ID,
    Capabilities,
)


class Action(StrEnum):
    """A top-level thing the wizard can do.

    `ACTION_GROUPS` below is the menu ORDER and the menu SHAPE; this enum is
    just the vocabulary. They used to be the same thing -- the order of this
    declaration was the order on screen -- and seven peers in one flat column
    is a list you read end to end every time, because nothing in it says which
    rows belong together.
    """

    #: Who records on this machine: the agent or the Probe daemon (one value for
    #: every coding agent; `←`/`→` switch it on the menu, Richard 2026-09-29).
    RECORDER = "recorder"
    #: The machine's default state for new sessions (`on`/`read`/`off`). It
    #: used to be a row on the Settings screen; it is the one setting people
    #: change often enough to earn a row on the menu itself.
    DEFAULTS = "defaults"
    CONFIGURE = "configure"
    UNINSTALL = "uninstall"
    UPDATE = "update"
    IMPORT_RESEARCH = "import-research"
    #: Legacy direct import flags; the menu combines them under IMPORT_RESEARCH.
    BACKFILL = "backfill"
    TRANSCRIPTS = "transcripts"
    IMPORT_JOBS = "imports"
    ACCOUNT = "account"
    SETTINGS = "settings"
    DIAGNOSE = "diagnose"
    EXIT = "exit"

    #: Reachable via `--action manual`, deliberately NOT in the menu. The
    #: dashboard points air-gapped users at it, but it is the rarest path and
    #: it made the menu longer for everyone else.
    MANUAL = "manual"

    #: Sign-in happens before the main menu; sign-out is a direct menu action
    #: and exits it. Both remain explicit flags for unattended callers.
    SIGN_IN = "login"
    SIGN_OUT = "logout"


#: Imports choose their own sources; they never ask which agents to configure.
#: The legacy flags still open their individual import lanes directly.
IMPORT_ACTIONS = frozenset({Action.IMPORT_RESEARCH, Action.BACKFILL, Action.TRANSCRIPTS})

#: Actions about the CREDENTIALS this device holds rather than what is installed
#: on it. They run once per wizard pass, not once per coding agent: there is one
#: config file, not one per agent.
ACCOUNT_ACTIONS = frozenset({Action.ACCOUNT, Action.SIGN_IN, Action.SIGN_OUT})

#: Actions about the DEVICE rather than any one coding agent. There is one
#: config file, so these run once per wizard pass and never ask which agents
#: to configure -- the answer has no bearing on what they do.
DEVICE_ACTIONS = ACCOUNT_ACTIONS | {Action.RECORDER, Action.DEFAULTS, Action.SETTINGS, Action.IMPORT_JOBS}


ACTION_COPY: dict[Action, tuple[str, str]] = {
    # The menu draws these two rows from the LIVE state (`setup.recorder_row`,
    # `setup.tracking_default_row`); these words are the fallback for anything
    # that renders the table alone.
    Action.RECORDER: (
        "Who records",
        "Your agents, or the Probe daemon.",
    ),
    Action.DEFAULTS: (
        "Probe in new sessions",
        "On, read or off for new sessions.",
    ),
    Action.CONFIGURE: (
        "★ Install Probe",
        "Set up tracking, capture and updates.",
    ),
    Action.UPDATE: (
        "Update Probe",
        "Upgrade the CLI and plugins.",
    ),
    Action.UNINSTALL: (
        "Uninstall Probe",
        "Remove plugins, stop capture, sign out.",
    ),
    Action.IMPORT_RESEARCH: (
        "Import research work",
        "Past sessions, a project folder, or both.",
    ),
    Action.IMPORT_JOBS: (
        "Existing imports",
        "Check, resume or cancel imports.",
    ),
    Action.SETTINGS: (
        "Settings",
        "Automatic updates on or off.",
    ),
    Action.DIAGNOSE: (
        "Diagnose a problem",
        "Check setup, sign-in and updates.",
    ),
    Action.EXIT: (
        "Exit",
        "Imports keep running.",
    ),
    Action.SIGN_OUT: (
        "Sign out",
        "Stop capture and imports, then sign out.",
    ),
}
"""What each menu row SAYS. `ACTION_GROUPS` says where it sits.

MANUAL, SIGN_IN, BACKFILL, TRANSCRIPTS and ACCOUNT remain reachable through flags.
The signed-in main menu offers sign-out directly."""


#: Rows the main menu draws RED: the ones that end something on this device
#: (Richard 2026-09-29). Sign out also asks first (`setup.confirm_sign_out`).
DANGER_ACTIONS = frozenset({Action.SIGN_OUT})


#: The menu, as GROUPS. Order here is order on screen.
#:
#: Seven flat rows made the reader classify every one of them before choosing:
#: "Update Probe" and "Import research work" are not the same
#: kind of decision, and nothing on screen said so, so finding either meant
#: reading both. Three or four short lists with a heading each is the same
#: information arranged so that most of it can be skipped.
#:
#: The menu draws every group but the cursor's COLLAPSED to its heading (see
#: `tui.menu`), so a heading has to say what is under it on its own -- which
#: is why these name the verbs ("Install/update/uninstall") rather than a
#: topic, and why a group's rows come in the order its heading names them.
#:
#: Defaults leads: it is the one row whose current value is worth seeing every
#: time the menu opens. Within `Install/update/uninstall`: Install, Update,
#: then Uninstall -- the lifecycle in order, with the one that removes
#: everything last, where the cursor reaches it only on purpose. Exit comes
#: before Sign out for the same reason: the cursor lands on a group's first
#: row, and the harmless way out should be what it lands on.
ACTION_GROUPS: tuple[tuple[str | None, tuple[Action, ...]], ...] = (
    ("Defaults", (Action.RECORDER, Action.DEFAULTS)),
    ("Install/update/uninstall", (Action.CONFIGURE, Action.UPDATE, Action.UNINSTALL)),
    ("Backfill", (Action.IMPORT_RESEARCH, Action.IMPORT_JOBS)),
    ("Settings", (Action.SETTINGS,)),
    ("Help", (Action.DIAGNOSE,)),
    ("Exit/sign out", (Action.EXIT, Action.SIGN_OUT)),
)


def grouped_actions() -> tuple[tuple[str | None, tuple[Action, ...]], ...]:
    """`ACTION_GROUPS`, checked against `ACTION_COPY` before it is rendered.

    The two are separate tables and a menu row needs BOTH: a group with no copy
    renders a titleless row, and copy in no group is a row that silently stops
    being reachable. Neither shows up as an error -- the menu just quietly has
    the wrong number of things in it -- so the agreement is asserted where it is
    used rather than left to a test that a later edit need not run.
    """
    listed = tuple(action for _, actions in ACTION_GROUPS for action in actions)
    if listed != tuple(ACTION_COPY):
        raise AssertionError(
            f"ACTION_GROUPS and ACTION_COPY disagree: {listed} vs {tuple(ACTION_COPY)}"
        )
    return ACTION_GROUPS


def manual_steps(
    *,
    base_url: str,
    agent_source: str | tuple[str, ...] | list[str] = "claude_code",
) -> str:
    """Every command the wizard runs, printed.

    This replaces the page's "Set it up manually" section. Generating it from
    the same constants the wizard uses is the point: the page's copy had already
    drifted from the commands beside it, and a printed script cannot drift from
    the code that prints it.
    """
    requested = (agent_source,) if isinstance(agent_source, str) else tuple(agent_source)
    sources = tuple(source for source in ("claude_code", "codex") if source in requested)
    if not sources:
        sources = ("claude_code",)

    marketplace_commands: list[str] = []
    install_commands: list[str] = []
    for source in sources:
        codex_source = source == "codex"
        binary = "codex" if codex_source else "claude"
        label = "Codex" if codex_source else "Claude Code"
        refresh = "upgrade" if codex_source else "update"
        install = "add" if codex_source else "install"
        if len(sources) > 1:
            marketplace_commands.append(f"# {label}")
            install_commands.append(f"# {label}")
        marketplace_commands.extend(
            (
                f"{binary} plugin marketplace add {MARKETPLACE_REPO}",
                f"{binary} plugin marketplace {refresh} research-os-agent",
            )
        )
        install_commands.extend(
            (
                f"{binary} plugin {install} {PLUGIN_ID}          # research tracking + MCP",
                f"{binary} plugin {install} {TAP_PLUGIN_ID}      # session capture",
            )
        )

    codex = "codex" in sources
    mcp_login = (
        (
            "",
            "# 5. Complete Codex's host-owned OAuth for the read-only MCP.",
            "codex mcp login probe-research",
        )
        if codex
        else ()
    )
    confirm_step = 6 if codex else 5
    return "\n".join(
        (
            "# Everything the Probe Research setup wizard does, as individual commands.",
            "# Run the ones you want. Needs network access and a browser to approve.",
            "",
            "# 1. Install the CLI (skip if you already have `probe`)",
            f"uv tool install --force '{AGENT_INSTALL}[all]'",
            "",
            "# 2. Add the plugin marketplace and refresh it.",
            "#    `add` alone does NOT refresh an already-added marketplace, which is",
            "#    how a freshly published plugin appears to be missing.",
            *marketplace_commands,
            "",
            "# 3. Install only what you want.",
            *install_commands,
            "",
            "# 4. Approve this device in your browser. One approval, all credentials.",
            f"probe wizard --action login --base-url {base_url}",
            *mcp_login,
            "",
            f"# {confirm_step}. Confirm.",
            "probe doctor",
        )
    )


def self_host_notes(*, base_url: str, mcp_endpoint: str) -> str:
    """Explain the agent-independent CLI and self-hosted MCP paths."""
    return "\n".join(
        (
            "# Running the MCP yourself, or without a coding-agent plugin.",
            "",
            "# A local, read-only MCP server pointed at your own API:",
            f"PROBE_MCP_TOKEN=YOUR_READ_TOKEN PROBE_BASE_URL={base_url} \\",
            f"  uvx --from '{AGENT_INSTALL}[all]' probe-research-mcp",
            "",
            f"# Hosted MCP endpoint: {mcp_endpoint}",
            "",
            "# The CLI works on its own -- no coding agent required:",
            f"uv tool install --force '{AGENT_INSTALL}[all]'",
            f"probe wizard --action login --base-url {base_url}",
        )
    )


def troubleshooting(caps: Capabilities) -> list[str]:
    """The page's "If something is not working" section, but state-aware.

    A static list makes the reader work out which item applies to them. Here we
    already know, so only the relevant lines are printed -- and the ones that
    depend on live state say what that state actually is.
    """
    notes: list[str] = []

    agent_source = caps.agent_source
    # pi has no marketplace CLI this wizard installs or updates a plugin
    # through (see wizard.INSTALLABLE_AGENT_SOURCES), so there is no "is the
    # binary on PATH" question to ask here, and its auto-update never "fires
    # at session start" the way it does for the other two -- nothing in
    # probe-research-pi ever spawns `probe wizard --action update` (its hooks
    # are independent TypeScript; see upgrading.py's own pi guard). The old
    # two-way ternary's silent `else` told a pi user to go install Claude
    # Code, which was never the question.
    if agent_source == "pi":
        agent_name = "pi"
    else:
        agent_binary = "codex" if agent_source == "codex" else "claude"
        agent_name = "Codex" if agent_source == "codex" else "Claude Code"
        agent_available = (
            caps.codex_available if agent_source == "codex" else caps.claude_available
        )
        if not agent_available:
            notes.append(
                f"`{agent_binary}` is not on PATH, so plugin install/update cannot run. The CLI "
                f"and login still work; install {agent_name} to enable the plugins."
            )
    if caps.cli_version is None:
        notes.append(
            "`probe` is not resolving. Re-run the install to relink the binaries and "
            "make sure ~/.local/bin is on your PATH."
        )
    if caps.tracking_plugin_installed and not caps.logged_in_as:
        notes.append(
            "The tracking plugin is installed but this device is not logged in, so "
            "the MCP has no credential. Run `probe wizard` to sign in."
        )
    if agent_source == "codex":
        notes.append(
            "If MCP tools are missing after a restart, run `codex mcp list --json`. "
            "If `probe-research` is not authenticated, run "
            "`codex mcp login probe-research`."
        )
    else:
        # The footgun that cannot heal itself: an exported token beats the stored one
        # forever, and nothing in the product can clear a variable in the user's shell.
        notes.append(
            "If MCP tools are missing after a restart: a stale PROBE_MCP_TOKEN exported "
            "in your shell profile SHADOWS the stored token and can never heal. Delete "
            "that line, then run `probe mcp status` to see where the token came from."
        )
    notes.append(
        "Do not register the MCP by hand while the plugin is installed -- the plugin "
        "already wires the `probe-research` server, and a second server with the same "
        "name breaks the connection."
    )
    if agent_source != "pi" and caps.auto_update_enabled and caps.last_update_attempt is None:
        notes.append(
            f"Auto-update is on but has never run on this device. It fires at {agent_name} "
            "session start, so it will not have run yet if you have not opened "
            "a session since enabling it."
        )
    return notes
