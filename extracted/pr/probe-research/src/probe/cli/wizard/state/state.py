"""What is actually installed and switched on for this device.

ONE state struct with TWO renderings: `probe wizard` shows it as a menu with
toggles, `probe doctor` prints it as a diagnostic. They must never disagree,
which is why neither computes state of its own.

Everything here is READ-ONLY and fail-soft. A machine mid-install, offline, or
without Claude Code still produces a complete `Capabilities` -- fields go
False/None rather than raising, because both callers need to render *something*
and a diagnostic that crashes is worse than one reporting "unknown".

stdlib only, and imported lazily by cli/main.py: `probe log` runs inside
training loops, and this module must never become a reason for that to get
slower.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from probe.foundation.compat.compat import StrEnum

TAP_PLUGIN_NAME = "probe-research-tap"
CODEX_TAP_PLUGIN_NAME = TAP_PLUGIN_NAME
TRACKING_PLUGIN_NAME = "probe-research"
#: The daemon profile's lean plugin (daemon reads): installed INSTEAD of
#: `probe-research` for a coding agent whose "Who records" is the daemon.
DAEMON_PLUGIN_NAME = "probe-research-daemon"
MARKETPLACE = "research-os-agent"
MARKETPLACE_REPO = "prbe-ai/research-os-agent"
#: PyPI distribution. NOT `probe-agent` -- that name belongs to an unrelated
#: project already on PyPI, so installing it fetches a stranger's package.
AGENT_INSTALL = "probe-research"
PLUGIN_ID = f"{TRACKING_PLUGIN_NAME}@{MARKETPLACE}"
TAP_PLUGIN_ID = f"{TAP_PLUGIN_NAME}@{MARKETPLACE}"
LEGACY_CODEX_TAP_PLUGIN_ID = "prbe-codex-tap-plugin@prbe-ai"
CODEX_MCP_NAME = "probe-research"


class Capability(StrEnum):
    """A row in the menu. Deliberately NOT plugin names -- nobody knows what
    `probe-research-tap` is, and the consent decision is about what the thing
    does, not what it is called."""

    TRACKING = "tracking"
    """Experiment tracking skills + the read-only MCP search surface."""

    CAPTURE = "capture"
    """Streams this device's Claude Code sessions to the knowledgebase."""

    AUTO_UPDATE = "auto_update"
    """Keeps the CLI and plugins current in the background."""

    AGENT_RULES = "agent_rules"
    """Knowledge-search and tracking guidance in the selected agent's global rules."""


class McpState(StrEnum):
    """Whether Probe's read-only MCP works in ONE coding agent, and if not, why.

    One answer per agent for every surface (the wizard header, `probe doctor`),
    resolved from that agent's registry row (`Capabilities.mcp_state`), so a new
    harness gets it by declaring its `mcp` kind. About MCP only: whether the CLI
    is signed in stays on its own Account row (the MCP connects with its own
    read token)."""

    ON = "on"
    LOGIN_NEEDED = "login-needed"  # installed; the credential its provider uses is missing or rejected
    DAEMON = "daemon"  # the daemon profile carries no MCP: the daemon reads for the agent
    NOT_INSTALLED = "not-installed"  # tracking plugin absent (or pi's tracking switched off)
    UNKNOWN = "unknown"  # an input that decides the answer could not be read
    NOT_OFFERED = "not-offered"  # Probe offers no MCP for this agent (registry `mcp: null`)


class TokenSource(StrEnum):
    """WHERE a capture credential resolves from.

    This exists because "turn capture off" is not the same as "delete the paired
    token file". The uploader accepts three sources, and clearing only the first
    lets capture silently resume at the next session start while the menu
    reports it as off. ENV is the one the wizard cannot fix by itself -- it
    cannot unset a variable in the parent shell -- so it has to say so.
    """

    PAIRED_FILE = "paired_file"
    ENVIRONMENT = "environment"
    PROBE_CONFIG = "probe_config"


@dataclass(frozen=True)
class Capabilities:
    """A complete, fail-soft snapshot of this device."""

    cli_version: str | None = None
    #: Per-component manifest comparison (see `probe.shared.updates.updates`). A LIST, not
    #: a bool, because "am I current?" has four independent answers -- CLI, SDK,
    #: plugin and transcript tap update on their own cadences and a machine is
    #: routinely current on one and months behind on another. Empty when the
    #: cached manifest is unreadable, which doctor renders as "could not check"
    #: rather than silently as good news.
    version_rows: tuple = ()
    #: Age in seconds of the manifest the rows above were graded against, or None
    #: when there is no cached manifest at all. Rendered, because a comparison
    #: against a three-week-old manifest is not the same claim as a fresh one.
    version_manifest_age_s: float | None = None
    install_method: str | None = None
    claude_available: bool = False
    #: The agent binary's own version, not probe's. Recorded because a
    #: boolean was all doctor had when an entire customer's imports were
    #: failing on a Claude Code flag their install predated.
    agent_version: str | None = None
    codex_available: bool = False
    agent_source: str = "claude_code"

    logged_in_as: str | None = None
    #: True/False when /me accepted/rejected the saved credential; None offline
    #: or when absent. An unknown account is not necessarily a signed-out one.
    api_credential_valid: bool | None = None
    base_url: str | None = None

    #: WHICH saved account the credentials above came from -- the active named
    #: context in the CLI config. One machine can hold several (kubectl-style),
    #: so "logged in as X" is only half the answer: the other half is which of
    #: this device's saved accounts is currently answering.
    config_context: str | None = None

    tracking_plugin_installed: bool = False
    capture_plugin_installed: bool = False
    legacy_capture_plugin_installed: bool = False

    #: Whether the two flags above were actually ASKED, or merely defaulted.
    #: False when `claude` is absent or `plugin list` could not complete -- in
    #: which case "not installed" is an unanswered question, not a finding, and
    #: nothing may report a failed install on the strength of it.
    plugins_verified: bool = True
    #: Why the plugin list could not be read, when it could not: the agent CLI's
    #: own answer (a timeout, a missing binary) or an unreadable install record.
    plugins_error: str | None = None

    capture_token_sources: tuple[TokenSource, ...] = ()
    #: True/False when the backend accepted/rejected the resolved credential;
    #: None when no credential exists or the endpoint could not be reached.
    capture_credential_valid: bool | None = None
    capture_killswitched: bool = False
    #: The killswitch is a sign-in's pending lock (`capture.AWAITING_CONFIRMATION`),
    #: which only an Install (or Update's question) lifts, not a deliberate off.
    capture_awaiting_confirmation: bool = False
    #: What the tap's last SessionStart found instead of a Python 3.11+ to run
    #: on ("python3 3.9.6"), from the `.python-missing` file it leaves beside
    #: `.disabled`; None when it found one (or never ran). With it set nothing
    #: records, whatever `capture_on` says (hooks/tap-python.sh).
    capture_python_missing: str | None = None
    capture_device_id: str | None = None

    #: Newest killer-side stop-daemon journal entry, doctor-ready. A tap daemon
    #: found SIGTERM'd with its pid file unlinked and no shutdown sentinel
    #: matches only capture._stop_daemon(), so a "transcripts missing" report
    #: must carry the last stop — and its absence, when a daemon died anyway,
    #: exonerates the stop path, which is itself the answer.
    capture_last_stop: str | None = None

    #: Codex owns OAuth for plugin MCPs. Claude's headers helper does not need
    #: a host login, so this remains None there.
    mcp_authenticated: bool | None = None
    #: This device holds a read token for the MCP (`mcp_token`, or
    #: PROBE_MCP_TOKEN). Separate from `logged_in_as`: a token pasted into
    #: `probe wizard --action login --token` signs in with no MCP token.
    mcp_token_held: bool = False
    #: This agent's registry `mcp` kind (`probe.foundation.harness_registry.harness_registry.MCP_*`), or
    #: None where Probe offers no MCP. Set by `doctor.collect`.
    mcp_kind: str | None = None
    #: The credential check for that kind (`MCP_RESOLVERS`), or None when
    #: nothing was checked (no MCP offered, or not collected).
    mcp_check: McpCheck | None = None

    agent_rules_installed: bool = False
    agent_rules_stale: bool = False

    auto_update_enabled: bool = False
    #: That `auto_update_enabled` is the managed CLI's default, not anyone's
    #: choice (`version_policy.autoupdate_state`): no evidence of a setup.
    auto_update_by_default: bool = False
    last_update_attempt: str | None = None
    #: Compact timestamp and status for the wizard; details above stay in doctor.
    last_update_attempt_summary: str | None = None

    #: The last time an available upgrade was deliberately NOT applied, and why.
    #: A SIBLING of last_update_attempt, never a substitute: without it, a box
    #: that has correctly deferred every upgrade for a fortnight of training is
    #: indistinguishable from one whose auto-updater is dead, because both show
    #: nothing but an old timestamp.
    last_update_skip: str | None = None

    #: Run refs currently holding this box against an upgrade. Diagnostic only —
    #: run_lock.any_live() is what the gate actually consults.
    live_runs: list[str] = field(default_factory=list)

    #: Journal.read_status() of the async outbox, None when it has never been
    #: used. Same rationale as LAST UPDATE ATTEMPT: a detached drainer cannot
    #: report failure anywhere else.
    outbox_status: dict | None = None

    #: The daemon's AI libraries: their version, "missing", or None when not
    #: checked. Collected, not read at render, because the check imports them.
    daemon_ai_libraries: str | None = None

    warnings: list[str] = field(default_factory=list)

    @property
    def capture_on(self) -> bool:
        """Capture ships only if a credential resolves AND the killswitch is off.

        Both halves matter: a paired device with `.disabled` present sends
        nothing, and a machine with no credential sends nothing regardless of
        which plugins are installed.
        """
        return (
            bool(self.capture_token_sources)
            and self.capture_credential_valid is not False
            and not self.capture_killswitched
        )

    @property
    def mcp_state(self) -> McpState:
        """THE per-agent MCP answer, precedence NOT_OFFERED > NOT_INSTALLED >
        DAEMON > LOGIN_NEEDED > ON; UNKNOWN only where a deciding input could
        not be read (never shown as "on")."""
        if self.mcp_kind is None:
            return McpState.NOT_OFFERED
        if not self.tracking_plugin_installed:
            # pi's answer is a settings read (verified=False by design, see
            # `installed_plugins`); elsewhere an unanswered plugin list is unknown.
            if not self.plugins_verified and not _settings_package(self.agent_source):
                return McpState.UNKNOWN
            return McpState.NOT_INSTALLED
        if tracking_plugin_name(self.agent_source) == DAEMON_PLUGIN_NAME:
            return McpState.DAEMON
        check = self.mcp_check
        if check is None or check.credential == McpCredential.UNKNOWN:
            return McpState.UNKNOWN
        if check.credential == McpCredential.PRESENT:
            return McpState.ON
        return McpState.LOGIN_NEEDED

    def mcp_status(self) -> str:
        """`mcp_state` in the words every surface prints."""
        state = self.mcp_state
        check = self.mcp_check
        if state == McpState.ON:
            return "on"
        if state == McpState.LOGIN_NEEDED:
            why = "token rejected; " if check is not None and check.credential == McpCredential.REJECTED else ""
            return f"login needed: {why}run `{check.fix if check else 'probe wizard'}`"
        if state == McpState.DAEMON:
            return "off: the daemon reads for this agent"
        if state == McpState.NOT_INSTALLED:
            return "off: not installed"
        if state == McpState.NOT_OFFERED:
            return "not offered for this agent"
        if check is not None and check.what:
            return f"unknown: {check.what}"
        if not self.tracking_plugin_installed:
            return "unknown: the agent's plugin list could not be read"
        return "unknown"

    @property
    def tracking_on(self) -> bool:
        mcp_ready = self.agent_source != "codex" or self.mcp_authenticated is not False
        return self.tracking_plugin_installed and self.logged_in_as is not None and mcp_ready

    @property
    def configured(self) -> bool:
        """Whether this device has been set up before.

        Deliberately NOT `any(enabled)`. Someone who ran setup and turned
        everything OFF has still configured this machine, and treating that as
        fresh would let `probe wizard --yes` silently switch tracking and
        auto-update back on from the defaults. Evidence of installation is the
        right signal, not evidence of anything being enabled.

        Auto-update counts only as someone's choice (`auto_update_chosen`):
        the managed CLI's default is on before any setup ran.
        """
        return any(
            (
                self.tracking_plugin_installed,
                self.capture_plugin_installed,
                self.legacy_capture_plugin_installed,
                self.logged_in_as is not None,
                bool(self.capture_token_sources),
                self.capture_killswitched,
                self.auto_update_chosen,
                self.agent_rules_installed,
                self.last_update_attempt is not None,
            )
        )

    @property
    def auto_update_chosen(self) -> bool:
        """Auto-update is on because someone turned it on, not by the managed
        CLI's default (`auto_update_by_default`)."""
        return self.auto_update_enabled and not self.auto_update_by_default

    @property
    def agent_configured(self) -> bool:
        """Whether Probe was set up for THIS agent: its plugins, its capture
        pairing (or killswitch) or its rules. `configured` without the device's
        own evidence (the sign-in, the updater), which every agent's snapshot
        shares: a signed-in device does not make pi, never set up, "configured"
        (`probe status`)."""
        return any(
            (
                self.tracking_plugin_installed,
                self.capture_plugin_installed,
                self.legacy_capture_plugin_installed,
                bool(self.capture_token_sources),
                self.capture_killswitched,
                self.agent_rules_installed,
            )
        )

    def enabled(self) -> dict[Capability, bool]:
        return {
            Capability.TRACKING: self.tracking_on,
            Capability.CAPTURE: self.capture_on,
            Capability.AUTO_UPDATE: self.auto_update_enabled,
            Capability.AGENT_RULES: self.agent_rules_installed,
        }


def _settings_package(source: str | None) -> bool:
    """The agent's Probe package is a settings entry (pi): one package for
    tracking and capture, read from a settings file rather than a plugin CLI."""
    from probe.foundation.harness_registry import get_registry

    try:
        return get_registry().get(source or agent_source()).lean_profile == "settings-filter"
    except Exception:  # noqa: BLE001 - an unknown agent is not one
        return False
from probe.cli.wizard.state.agent_identity import agent_source, tracking_plugin_name  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.mcp import McpCheck, McpCredential  # noqa: E402 -- pieces need each other; the front door loads this one first
