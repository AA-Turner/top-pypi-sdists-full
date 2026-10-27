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

import http.client
import json
import os
import threading
import time
import warnings
import urllib.error
import urllib.request
from collections.abc import Iterator
from concurrent.futures import Future
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from probe._compat import StrEnum
from pathlib import Path

from probe.cli import pi_config, plugin_cli
from probe.sdk.tls import ssl_context

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

ENV_INGEST_TOKEN = "PROBE_INGEST_TOKEN"
ENV_TAP_PLUGIN_DIR = "PROBE_RESEARCH_TAP_PLUGIN_DIR"
ENV_CONFIG_PATH = "PROBE_CONFIG_PATH"
ENV_AGENT = "PROBE_AGENT"
ENV_CODEX_INGEST_TOKEN = "PRBE_CODEX_TAP_TOKEN"
ENV_CODEX_TAP_PLUGIN_DIR = "PRBE_CODEX_TAP_PLUGIN_DIR"
ENV_PI_INGEST_TOKEN = "PROBE_PI_TAP_TOKEN"
ENV_PI_TAP_PLUGIN_DIR = "PROBE_PI_TAP_PLUGIN_DIR"

#: Per-source overrides for the tap's token/plugin-dir env vars, read from the
#: harness registry (probe/harness/harnesses.json, `capture` of each captured
#: row). The tap package reads its own copy of the same file, so the two can no
#: longer drift (tests/test_harness_conformance.py). claude_code is the
#: registry's default; ENV_INGEST_TOKEN / ENV_TAP_PLUGIN_DIR remain its names.
def _capture_rows() -> dict:
    from probe.harness import get_registry

    return {h.id: h.capture for h in get_registry().captured()}


_TAP_TOKEN_ENV_BY_SOURCE: dict[str, str] = {
    source: capture.token_env for source, capture in _capture_rows().items() if source != "claude_code"
}
_TAP_PLUGIN_DIR_ENV_BY_SOURCE: dict[str, str] = {
    source: capture.plugin_dir_env for source, capture in _capture_rows().items() if source != "claude_code"
}


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


class McpCredential(StrEnum):
    """What one agent's MCP credential check found (`MCP_RESOLVERS`)."""

    PRESENT = "present"
    MISSING = "missing"
    REJECTED = "rejected"  # present, and the server refused it (`probe doctor`, the wizard)
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class McpCheck:
    """One credential check: what it found, the command that fixes it, and,
    for UNKNOWN, what could not be read."""

    credential: McpCredential
    fix: str = "probe wizard"
    what: str = ""


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
    #: Per-component manifest comparison (see `probe.cli.versions`). A LIST, not
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
    #: This agent's registry `mcp` kind (`probe.harness.registry.MCP_*`), or
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

    #: Floating runs waiting to be filed (daemon v2): `doctor.unfiled_summary`'s
    #: dict, or None when nobody asked (not logged in, or a pure render).
    unfiled_runs: dict | None = None

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


class UnrecognizedAgentSourceWarning(UserWarning):
    """PROBE_AGENT was set to a value this CLI does not recognize.

    A WARNING plus a claude_code fallback, not an exception -- Mahit's call
    (2026-08-28): a typo'd or stale PROBE_AGENT on an existing machine used
    to silently work as claude_code, and a hard raise would turn that machine
    from quietly-working into broken on upgrade. So the boundary stays loud
    without regressing: the warning names the value and the accepted set on
    stderr, while behavior falls back to the pre-pi default. The DESTRUCTIVE
    half of the old silent-default bug class (pi reaching Claude Code's
    marketplace CLI) is guarded separately and still HARD-raises -- see
    plugin_cli.binary_name(), which a fallback here can never reach with an
    unrecognized value because this function only ever returns the three
    known sources.
    """


def tracking_plugin_name(source: str | None = None) -> str:
    """The Probe plugin this coding agent should carry: `probe-research-daemon`
    when its "Who records" is the daemon (`session_marker.recorder`), else
    `probe-research`. The one place install, detection, update and removal
    ask, so none of them can put the other profile's plugin back."""
    from probe.sdk import session_marker

    try:
        daemon = session_marker.recorder(source or agent_source()) == session_marker.RECORDER_DAEMON
    except Exception:  # noqa: BLE001 - an unreadable config is today's profile
        daemon = False
    return DAEMON_PLUGIN_NAME if daemon else TRACKING_PLUGIN_NAME


def agent_source() -> str:
    """Setup target: explicit override, then the coding-agent environment.

    pi has no environment-sniffing shortcut the way a Codex session does
    (there is no PROBE_TAP_SOURCE-equivalent pi sets on its own child
    processes) -- PROBE_AGENT=pi is the only way in.

    Three cases, not two:
      - unset or empty (after stripping) -> claude_code. This is "nothing was
        asked" and is the correct, load-bearing default: every existing
        install that never sets PROBE_AGENT depends on it. Do not change it.
      - a recognized value (claude/claude_code, codex, pi) -> that source.
      - a non-empty, unrecognized value -> a LOUD UnrecognizedAgentSourceWarning
        and the claude_code fallback. Same posture as the live-capture daemon
        normalizer, tap/config.py::capture_source(), and for the same reason:
        a machine that has quietly worked for months with a stale or typo'd
        PROBE_AGENT must not break on upgrade. The warning (not silence) is
        what keeps the misspelling discoverable; the fallback is what keeps
        it non-regressive. python -W error turns it back into a hard stop
        for anyone who wants the strict behavior.
    """
    from probe.harness import get_registry

    registry = get_registry()
    raw = os.environ.get(ENV_AGENT) or ""
    explicit = raw.strip().lower()
    if not explicit:
        return registry.default
    harness = registry.find(explicit)
    if harness is not None and harness.installable:
        return harness.id
    accepted = ", ".join(name for h in registry.installable() for name in h.names)
    warnings.warn(
        f"{ENV_AGENT}={raw!r} is not a recognized agent source "
        f"(accepted: {accepted}); continuing as {registry.default}",
        UnrecognizedAgentSourceWarning,
        stacklevel=2,
    )
    return registry.default


@contextmanager
def agent_target(source: str):
    """Scope ENV_AGENT to one operation without leaking it to the caller.

    Nearly everything here resolves its target agent from the environment (see
    `agent_source`), so code that must act on a NAMED agent has to set it --
    and put it back, or the next call in the same process silently inherits a
    target nobody chose. One wizard run configures both agents in turn, which
    is exactly where that would bite.
    """
    previous = os.environ.get(ENV_AGENT)
    os.environ[ENV_AGENT] = source
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop(ENV_AGENT, None)
        else:
            os.environ[ENV_AGENT] = previous


def tap_token_env(source: str | None = None) -> str:
    """The env var name the tap reads a credential from, for `source` (or the
    ambient agent).

    Table-driven off `_TAP_TOKEN_ENV_BY_SOURCE` rather than a hand-typed
    two-way ternary: `doctor.py` and `capture.py` each used to spell
    `ENV_CODEX_INGEST_TOKEN if source == "codex" else ENV_INGEST_TOKEN`
    independently, and both silently named pi's leaked env var
    `PROBE_INGEST_TOKEN` instead of `PROBE_PI_TAP_TOKEN` -- correct-looking,
    wrong variable, in a warning whose whole point is telling someone which
    variable to unset.
    """
    selected = source or agent_source()
    return _TAP_TOKEN_ENV_BY_SOURCE.get(selected, ENV_INGEST_TOKEN)


def capture_plugin_name(source: str | None = None) -> str:
    return CODEX_TAP_PLUGIN_NAME if (source or agent_source()) == "codex" else TAP_PLUGIN_NAME


def tap_plugin_dir(source: str | None = None) -> Path:
    """The capture tap's state folder for an agent, from its registry row:
    the override variable, else the current folder, else a legacy folder an
    older install left (Codex's retired standalone plugin name). The tap
    resolves the same row from its own copy of the registry."""
    from probe.harness import get_registry

    selected = source or agent_source()
    capture = get_registry().get(selected).capture
    if capture is None:
        raise ValueError(f"{selected!r} has no capture tap")
    return capture.state_dir()


def probe_config_path() -> Path:
    env = os.environ.get(ENV_CONFIG_PATH)
    if env:
        return Path(env)
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "probe" / "config.json"


def _read_json(path: Path) -> dict:
    try:
        loaded = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def probe_config_credentials() -> dict:
    """The probe CLI config flattened the way the UPLOADER reads it.

    This MUST mirror `tap/config.py:_read_probe_config()` exactly. The CLI writes
    v2 (named contexts) as of the workspace-context pass, and when `contexts`
    exists the uploader reads ONLY the active context -- it does not fall back to
    the top level.

    Reading just the top-level key would therefore miss the credential on every
    modern config, and this function backs the off switch: a miss means we clear
    nothing, re-verify nothing, and report "capture is off" while it keeps
    shipping. The parity test in tests/test_setup_wizard.py guards the pairing.
    """
    raw = _read_json(probe_config_path())
    contexts = raw.get("contexts")
    if isinstance(contexts, dict):
        active = contexts.get(raw.get("current_context") or "default")
        return active if isinstance(active, dict) else {}
    return raw


def consumes_cli_capture_token(source: str) -> bool:
    """Does this agent's uploader fall back to the probe CLI config's
    `ingest_token`? Only Claude Code: that token is the capture token minted
    for Claude Code, and the server refuses a paired token on any other
    agent's route. Mirrors tap/config.py::load_token() and the pi extension's
    pairing.ts (decision D3, 2026-09-09). Read from the harness registry
    (`capture.cli_token_fallback`)."""
    from probe.harness import get_registry

    harness = get_registry().find(source)
    return bool(harness and harness.capture and harness.capture.cli_token_fallback)


def capture_token_sources(source: str | None = None) -> tuple[TokenSource, ...]:
    """Every place a capture credential currently resolves from, in the
    uploader's own precedence order.

    Mirrors `tap/config.py:load_token()`. It is duplicated rather than imported
    because the tap is a separate plugin package living in Claude Code's plugin
    cache -- the CLI cannot import it. Any change there must change here, which
    is what the parity tests in tests/test_setup_wizard.py exist to catch.
    """
    found: list[TokenSource] = []
    selected = source or agent_source()
    token_file = tap_plugin_dir(selected) / ".token"
    try:
        if token_file.read_text().strip():
            found.append(TokenSource.PAIRED_FILE)
    except OSError:
        pass
    token_env = _TAP_TOKEN_ENV_BY_SOURCE.get(selected, ENV_INGEST_TOKEN)
    if (os.environ.get(token_env) or "").strip():
        found.append(TokenSource.ENVIRONMENT)
    if (
        # Mirrors tap/config.py::load_token(): the probe CLI config's
        # `ingest_token` is the capture token minted for Claude Code, and the
        # server refuses it on every other agent's route (a paired device
        # token is bound to its source). So only Claude Code falls back to it;
        # Codex and pi resolve their own paired token or env var, or nothing.
        consumes_cli_capture_token(selected)
        and str(probe_config_credentials().get("ingest_token") or "").strip()
    ):
        found.append(TokenSource.PROBE_CONFIG)
    return tuple(found)


def resolved_capture_credential(source: str | None = None) -> tuple[str, str] | None:
    """The uploader's winning (token, base URL), or None when incomplete."""
    selected = source or agent_source()
    token = ""
    token_file = tap_plugin_dir(selected) / ".token"
    try:
        token = token_file.read_text(encoding="utf-8").strip()
    except OSError:
        pass
    if not token:
        token_env = _TAP_TOKEN_ENV_BY_SOURCE.get(selected, ENV_INGEST_TOKEN)
        token = (os.environ.get(token_env) or "").strip()
    if not token and consumes_cli_capture_token(selected):
        token = str(probe_config_credentials().get("ingest_token") or "").strip()

    base_url = (os.environ.get("PROBE_BASE_URL") or "").strip().rstrip("/")
    if not base_url:
        plugin_config = _read_json(tap_plugin_dir(selected) / ".config")
        base_url = str(plugin_config.get("api_base_url") or "").strip().rstrip("/")
    if not base_url:
        base_url = str(probe_config_credentials().get("base_url") or "").strip().rstrip("/")
    return (token, base_url) if token and base_url else None


def revoke_capture_device(source: str | None = None, *, timeout: float = 5.0) -> bool | None:
    """Tell the server this device is done, BEFORE the local credential is wiped.

    True = the server revoked it. False = it answered, and there was nothing
    live to revoke (an already-revoked or unknown token). None = we could not
    ask (no credential, no base URL, offline, timeout, server error).

    ORDER IS THE WHOLE POINT. The bearer this authenticates with is the same
    `<plugin>/.token` that `turn_off` deletes one step later, so this has to run
    first or it can never run at all -- not here, and not from a later
    `python -m tap revoke` either, which reads the same file and skips the
    server call when it finds nothing. Without this the row keeps
    `revoked_at IS NULL` forever: the machine lingers in the dashboard's device
    list and its capture credential stays valid on a token nobody holds.

    `reason` is what stops this being read as a re-pair. The same endpoint
    serves both flows, and the churn channel counts an uninstall as a departure
    (see `DisconnectReason` in app/core/analytics.py).

    NEVER RAISES, and never blocks the teardown. Turning capture off is a
    consent guarantee about THIS machine, and it is satisfied by the local work
    that follows whether or not the network is reachable -- an unreachable
    server must not leave a user unable to turn capture off.
    """
    resolved = resolved_capture_credential(source)
    if resolved is None:
        return None
    return revoke_capture_token(*resolved, timeout=timeout)


def revoke_capture_token(token: str, base_url: str, *, timeout: float = 5.0) -> bool | None:
    """`revoke_capture_device`'s server call for a token already in hand.
    Same answers, and it never raises either."""
    try:
        request = urllib.request.Request(
            f"{base_url}/agent-tap/revoke",
            data=json.dumps({"reason": "uninstall"}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "probe-capture-off/1"},
            method="POST",
        )
        request.add_unredirected_header("Authorization", f"Bearer {token}")
        with _credential_opener().open(request, timeout=timeout) as response:
            return response.status == 200
    except urllib.error.HTTPError as exc:
        # 401 is the documented benign case: already revoked, or unknown.
        return False if exc.code in {401, 403, 404} else None
    # ValueError: a base URL with no scheme or a bad port (http.client.InvalidURL);
    # HTTPException: a malformed answer (a proxy's BadStatusLine).
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException):
        return None


def verify_capture_credential(source: str | None = None, *, timeout: float = 5.0) -> bool | None:
    """Ask the ingest status endpoint whether the resolved token is accepted.

    False is reserved for an authoritative 401/403. Offline, timeouts, and
    server errors stay unknown so `probe doctor` remains fail-soft and does not
    turn capture off merely because a laptop has no network.
    """
    resolved = resolved_capture_credential(source)
    if resolved is None:
        return None
    token, base_url = resolved
    request = urllib.request.Request(
        f"{base_url}/ingest/v1/sessions/status", headers={"User-Agent": "probe-doctor/1"}
    )
    # Never redirected: urllib would carry the bearer to the Location host, and
    # an SSO login page's 200 would read as "accepted".
    request.add_unredirected_header("Authorization", f"Bearer {token}")
    try:
        with _credential_opener().open(request, timeout=timeout) as response:
            return True if response.status == 200 else None
    except urllib.error.HTTPError as exc:
        return False if exc.code in {401, 403} else None
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


#: `POST /v1/device-state`: the account, every agent's capture validity and the
#: version manifest in ONE answer (app/client_version/device_state_router.py).
DEVICE_STATE_PATH = "/v1/device-state"
#: One budget for the one call. It replaced seven serial calls, each with its
#: own, so a slow API now costs this at most once instead of per call.
DEVICE_STATE_TIMEOUT_S = 5.0
#: How much longer than that the caller waits for the thread: urllib's timeout
#: bounds each socket operation, not the whole exchange.
DEVICE_STATE_GRACE_S = 2.0
#: Statuses that mean "ask the old way": the route is missing (404/405), or
#: something in front of the server answered for it (see fetch_device_state).
_ASK_THE_OLD_WAY = frozenset({301, 302, 303, 307, 308, 401, 403, 404, 405})
#: The largest answer read. A real one is well under 2 KiB; a proxy streaming
#: something else must not grow the process.
DEVICE_STATE_MAX_BYTES = 256 * 1024


class DeviceStateOutcome(StrEnum):
    #: The server answered; every field below is its verdict.
    ANSWERED = "answered"
    #: 404/405: a server that predates the route (an older self-hosted API).
    #: The caller falls back to asking the old way.
    UNSUPPORTED = "unsupported"
    #: Offline, timed out, 5xx or garbled: nothing is known.
    UNREACHABLE = "unreachable"


class AccountStatus(StrEnum):
    """The server's vocabulary (`app/client_version/device_state_router.py`)."""

    OK = "ok"
    SIGNED_OUT = "signed_out"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class CaptureStatus(StrEnum):
    OK = "ok"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class DeviceStateRequest:
    """Everything the call needs, resolved on the CALLER's thread.

    Resolution reads files and environment per source with the source passed
    explicitly, so the worker thread that sends it touches no process-wide
    state (the wizard scopes agents through `os.environ["PROBE_AGENT"]`).
    """

    base_url: str
    #: The CLI's API token, or None when signed out (the call works signed out).
    #: Kept out of repr: this object's whole job is to carry secrets.
    token: str | None = field(repr=False)
    #: source -> capture credential, ONLY for credentials whose own base URL is
    #: `base_url`. A credential is never sent to a server that did not issue it.
    capture_tokens: dict[str, str] = field(repr=False)
    #: Sources holding a credential for ANOTHER server. The answer carries no
    #: verdict for them; `doctor.collect()` checks such an agent the old way,
    #: against its own server, when it reads that agent.
    elsewhere: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeviceState:
    outcome: DeviceStateOutcome
    account_email: str | None = None
    #: True = accepted, False = refused (the ONLY state that sends someone back
    #: through sign-in), None = signed out or unknown.
    account_valid: bool | None = None
    #: source -> True accepted / False refused / None unknown. The same
    #: tristate `verify_capture_credential` returns. A source missing here got
    #: no verdict (its credential belongs to another server).
    capture: dict[str, bool | None] = field(default_factory=dict)
    #: Why nothing is known, for the warnings `probe doctor` would print.
    error: str | None = None

    @property
    def answered(self) -> bool:
        return self.outcome is DeviceStateOutcome.ANSWERED


def device_state_request(
    base_url: str, token: str | None, sources: tuple[str, ...]
) -> DeviceStateRequest:
    """Split each source's capture credential by the server it belongs to."""
    base = (base_url or "").strip().rstrip("/")
    here: dict[str, str] = {}
    elsewhere: list[str] = []
    for source in sources:
        resolved = resolved_capture_credential(source)
        if resolved is None:
            continue
        capture_token, capture_base = resolved
        if capture_base == base:
            here[source] = capture_token
        else:
            elsewhere.append(source)
    return DeviceStateRequest(
        base_url=base, token=token or None, capture_tokens=here, elsewhere=tuple(elsewhere)
    )


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse every redirect. urllib's default handler would turn the POST into
    a GET and copy the headers -- the bearer included -- to whatever host
    `Location` names (an SSO proxy in front of a self-hosted API, an https ->
    http downgrade). The SDK's httpx client never follows redirects either; a
    3xx here surfaces as an HTTPError and reads as unreachable."""

    def redirect_request(self, *_args, **_kwargs):
        return None


def _proxies() -> dict[str, str]:
    """The environment's proxies as urllib reads them, plus `ALL_PROXY`, which
    urllib ignores and httpx (the SDK, and the calls this replaced) honours."""
    proxies = urllib.request.getproxies()
    everything = proxies.get("all")
    if everything:
        proxies.setdefault("http", everything)
        proxies.setdefault("https", everything)
    return proxies


def _urllib_cannot_reach(base_url: str) -> bool:
    """Whether the environment routes `base_url` through a proxy urllib cannot
    speak -- a TLS (`https://`) or SOCKS proxy -- that httpx (the SDK, which the
    old calls use) can. Such a machine asks the old way from the start."""
    from urllib.parse import urlsplit

    parts = urlsplit(base_url)
    proxy = _proxies().get(parts.scheme)
    # host:port, as urllib's own ProxyHandler asks: NO_PROXY can name a port.
    authority = parts.hostname or ""
    if parts.port:
        authority = f"{authority}:{parts.port}"
    if not proxy or urllib.request.proxy_bypass(authority):
        return False
    # A scheme-less proxy ("proxy:8080") is plain HTTP to urllib; only an
    # explicit other scheme (https://, socks5://) is one it cannot speak.
    if "://" not in proxy:
        return False
    return urlsplit(proxy).scheme.lower() != "http"


def _credential_opener() -> urllib.request.OpenerDirector:
    """The opener for a request that carries a credential: no redirects, the
    environment's proxies, the CLI's TLS trust."""
    return urllib.request.build_opener(
        _NoRedirect,
        urllib.request.ProxyHandler(_proxies()),
        urllib.request.HTTPSHandler(context=ssl_context()),
    )


def _device_state_headers() -> dict[str, str]:
    from probe import __version__
    from probe.client_headers import client_version_headers, device_headers
    from probe.sdk.surface import SURFACE_HEADER, Surface

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "probe-wizard/1",
        SURFACE_HEADER: Surface.CLI.value,
        **client_version_headers(Surface.CLI.value, __version__),
    }
    try:
        from probe.sdk.device_identity import device_instance_id

        headers.update(device_headers(device_instance_id()))
    except Exception:  # noqa: BLE001 - identity is telemetry, never a hard failure
        pass
    return headers


_ACCOUNT_VALID: dict[str, bool | None] = {
    AccountStatus.OK: True,
    AccountStatus.REJECTED: False,
    AccountStatus.SIGNED_OUT: None,
    AccountStatus.UNKNOWN: None,
}
_CAPTURE_VALID: dict[str, bool | None] = {
    CaptureStatus.OK: True,
    CaptureStatus.REJECTED: False,
    CaptureStatus.UNKNOWN: None,
}


def _verdict(table: dict[str, bool | None], value: object) -> bool | None:
    """A status word's tristate. Anything else -- a word this CLI does not know,
    or not a word at all -- is unknown, never a refusal."""
    return table.get(value) if isinstance(value, str) else None


def fetch_device_state(
    request: DeviceStateRequest,
    *,
    timeout: float = DEVICE_STATE_TIMEOUT_S,
    deadline: float | None = None,
) -> DeviceState:
    """Ask `POST /v1/device-state`. NEVER RAISES, and never retries.

    Sent with urllib, not the SDK `Client`, on purpose: the SDK transport
    scrubs every JSON body (it would send `<redacted>` in place of each capture
    credential) and refuses a `/v1` call without an API token (this one must
    work signed out). A 200 also refreshes the version cache the Versions row
    is graded against, so no separate manifest fetch is needed.
    """
    if deadline is None:
        deadline = time.monotonic() + timeout + DEVICE_STATE_GRACE_S
    if not request.base_url:
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="no API base URL configured")
    if _urllib_cannot_reach(request.base_url):
        return DeviceState(DeviceStateOutcome.UNSUPPORTED)
    http_request = urllib.request.Request(
        f"{request.base_url}{DEVICE_STATE_PATH}",
        data=json.dumps({"capture_tokens": request.capture_tokens}).encode("utf-8"),
        headers=_device_state_headers(),
        method="POST",
    )
    if request.token:
        # Unredirected as well as unredirectable: belt and braces for the bearer.
        http_request.add_unredirected_header("Authorization", f"Bearer {request.token}")
    opener = _credential_opener()
    # The WHOLE exchange gets the budget (`deadline`, shared with the readers),
    # not just each socket operation: a peer trickling bytes inside every
    # per-read timeout is cut off here.
    try:
        with opener.open(http_request, timeout=timeout) as response:
            received = bytearray()
            while chunk := response.read1(65536):
                received.extend(chunk)
                if len(received) > DEVICE_STATE_MAX_BYTES:
                    return DeviceState(DeviceStateOutcome.UNREACHABLE, error="answer too large")
                if time.monotonic() > deadline:
                    return DeviceState(DeviceStateOutcome.UNREACHABLE, error="answer too slow")
    except urllib.error.HTTPError as exc:
        # 404/405: a server without the route. A redirect, 401 or 403 cannot
        # come from the route (it is public and never redirects), so something
        # in front of it -- an SSO proxy, a firewall -- answered: ask the old
        # way, which behaves in that network exactly as it did before.
        if exc.code in _ASK_THE_OLD_WAY:
            return DeviceState(DeviceStateOutcome.UNSUPPORTED)
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error=f"HTTP {exc.code}")
    except ValueError:
        # http.client refuses an invalid header VALUE with the value in the
        # message -- a bearer with a stray newline. Never echo it.
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="the request could not be sent")
    except (
        urllib.error.URLError,
        http.client.HTTPException,  # a truncated or garbled response; not an OSError
        TimeoutError,
        OSError,
    ) as exc:
        return DeviceState(
            DeviceStateOutcome.UNREACHABLE,
            error=str(getattr(exc, "reason", None) or exc) or type(exc).__name__,
        )
    try:
        body = json.loads(bytes(received).decode("utf-8"))
    except ValueError:
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="malformed answer")
    if not isinstance(body, dict):
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="malformed answer")
    account = body.get("account") if isinstance(body.get("account"), dict) else {}
    answered_capture = body.get("capture") if isinstance(body.get("capture"), dict) else {}
    capture = {
        source: _verdict(_CAPTURE_VALID, answered_capture.get(source))
        for source in request.capture_tokens
    }
    manifest = body.get("versions") if isinstance(body.get("versions"), dict) else None
    # A pod that has not fetched the manifest yet answers every pair empty.
    # Caching THAT as a good fetch would blank a perfectly good cached one.
    publishes_a_version = manifest is not None and any(
        isinstance(pair, dict) and pair.get("latest") for pair in manifest.values()
    )
    # Too late to be anyone's answer (the readers have moved on): too late to
    # overwrite the cache they graded against, too.
    if publishes_a_version and time.monotonic() <= deadline:
        try:
            from probe import version_policy

            version_policy.write_cache(manifest, True)
        except Exception:  # noqa: BLE001 - a version cache must never break the menu
            pass
    email = account.get("email")
    return DeviceState(
        DeviceStateOutcome.ANSWERED,
        account_email=email if isinstance(email, str) and email else None,
        account_valid=_verdict(_ACCOUNT_VALID, body.get("account_status")),
        capture=capture,
    )


def start_device_state(
    request: DeviceStateRequest,
    *,
    warm_manifest_on_fallback: bool = False,
    deadline: float | None = None,
) -> DeviceStateResolver:
    """Send the call on a daemon thread and return its resolver at once.

    ONE deadline, fixed here, for the worker and every reader: an answer the
    readers gave up on is nobody's, and must not write the version cache after
    them either. A daemon thread, not an executor: an executor's workers are
    joined at interpreter exit, so quitting the wizard while a call was pending
    would wait out its timeout. `deadline` (`time.monotonic`) makes it sooner
    than the call's own budget (`probe status --refresh --timeout`)."""
    future: Future = Future()
    own = time.monotonic() + DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S
    deadline = own if deadline is None else min(own, deadline)

    def run() -> None:
        try:
            state = fetch_device_state(request, deadline=deadline)
        except BaseException as exc:  # noqa: BLE001 - fetch never raises; belt and braces
            future.set_exception(exc)
            return
        # The verdict first, so an older server's "unsupported" reaches the
        # readers (and their fallback to the old calls) without waiting on it...
        future.set_result(state)
        if state.outcome is DeviceStateOutcome.UNSUPPORTED and warm_manifest_on_fallback:
            # ...then the manifest the old way carries none of, as the wizard
            # always fetched it, or an older server's Versions row goes stale.
            from probe.cli import versions as versions_mod

            versions_mod.warm_manifest()

    threading.Thread(target=run, name="probe-device-state", daemon=True).start()
    return DeviceStateResolver(future, deadline=deadline)


def device_state_result(
    future: Future, *, timeout: float = DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S
) -> DeviceState:
    """The call's answer, or UNREACHABLE when it has none in time. Never raises."""
    try:
        return future.result(timeout=timeout)
    except Exception as exc:  # noqa: BLE001 - a menu must render without it
        return DeviceState(
            DeviceStateOutcome.UNREACHABLE, error=f"no answer ({type(exc).__name__})"
        )


class DeviceStateResolver:
    """The one answer every reader of a call gets, with ONE deadline fixed when
    the call starts. Call it to get the answer.

    Several agents read the same call. Waiting a fresh timeout each would cost a
    stuck call once per agent, and could hand one agent UNREACHABLE and the next
    the late answer; the first resolution is everyone's."""

    def __init__(
        self,
        future: Future,
        *,
        timeout: float = DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S,
        deadline: float | None = None,
    ) -> None:
        self._future = future
        self.started = time.monotonic()
        self._deadline = deadline if deadline is not None else self.started + timeout
        self._answer: DeviceState | None = None
        self._lock = threading.Lock()

    def __call__(self) -> DeviceState:
        with self._lock:
            if self._answer is None:
                remaining = max(0.0, self._deadline - time.monotonic())
                self._answer = device_state_result(self._future, timeout=remaining)
            return self._answer

    def stale(self, max_age_s: float) -> bool:
        """Worth asking again: older than `max_age_s`, or read and not an answer."""
        if time.monotonic() - self.started > max_age_s:
            return True
        return self._answer is not None and not self._answer.answered


def device_state_resolver(
    future: Future, *, timeout: float = DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S
) -> DeviceStateResolver:
    return DeviceStateResolver(future, timeout=timeout)


def answered_already(state: DeviceState) -> DeviceStateResolver:
    """A resolver for a state known without a call (the request could not even
    be built)."""
    done: Future = Future()
    done.set_result(state)
    return DeviceStateResolver(done)


def verify_mcp_credential(*, base_url: str, token: str) -> bool | None:
    """Check the read token itself, independently of the saved API credential.

    Only an authoritative rejection prevents reuse. One short attempt keeps
    an offline install from waiting through the SDK's normal retry budget.
    Explicit settings prevent an environment API token from masking a revoked
    MCP token. The MCP surface also avoids minting local device identity during
    this read-only check.
    """
    from probe.sdk.client import Client
    from probe.sdk.config import Settings
    from probe.sdk.errors import AuthError, ScopeError
    from probe.sdk.surface import Surface
    from probe.sdk.transport import Transport

    try:
        settings = Settings(base_url=base_url, token=token)
        with Client(
            settings=settings,
            transport=Transport(
                settings, timeout=5.0, max_retries=0, surface=Surface.MCP.value
            ),
            async_writes=False,
            auto_drain=False,
        ) as client:
            client.me()
        return True
    except (AuthError, ScopeError):
        return False
    except Exception:  # noqa: BLE001 - an unavailable check does not invalidate a token
        return None


@dataclass(frozen=True)
class PluginState:
    """What Claude Code reports installed, AND whether it managed to answer.

    THE TWO ARE DIFFERENT and collapsing them is a bug. An empty `names` used
    to mean three unrelated things at once -- the plugins are genuinely absent,
    `claude` is not on this machine, or the query timed out -- so any caller
    that treated "empty" as "not installed" would tell someone on a GPU pod
    that their setup failed. `verified` separates "we looked and they are not
    there" from "we could not look".
    """

    names: frozenset[str] = frozenset()
    verified: bool = True
    #: Why it could not look, when it could not (None when it did, or when
    #: there is no list to read, as for pi).
    error: str | None = None

    def __contains__(self, name: str) -> bool:
        return name in self.names

    def __iter__(self):
        return iter(self.names)

    def __len__(self) -> int:
        return len(self.names)

    def missing(self, wanted) -> list[str]:
        """Names VERIFIED absent. Empty when we could not check -- an
        unanswerable question must not read as a negative answer."""
        if not self.verified:
            return []
        return [name for name in wanted if name not in self.names]


def installed_plugins(*, source: str | None = None, local: bool = False) -> PluginState:
    """Plugin names the selected coding agent reports as installed.

    `local` reads the record the agent's own `plugin list` reads instead of
    running it (`probe status` without --refresh): Claude Code's install ledger,
    Codex's config.toml (`_local_plugins`). pi and Kimi Code are file reads
    either way.

    ``verified=False`` when its CLI is absent (normal on a GPU pod and never
    an error) or the query could not complete.

    pi is neither: it is a source this module KNOWS has no plugin CLI at all
    (plugin_cli.py's own docstring scopes that module to claude/codex; see
    setup.py's INSTALLABLE_AGENT_SOURCES for the wizard-facing side of the
    same fact -- not imported here, that would be circular, since setup.py
    imports FROM this module). Falling through to plugin_cli.list_plugins("pi")
    would resolve its binary as "claude" (plugin_cli.binary_name()'s own
    codex-or-claude default) and silently report on CLAUDE'S plugins under
    pi's name.

    pi DOES have a real, checkable install signal though (plan D7): its own
    settings.json `packages` entry, read via `pi_config.package_entry_installed`
    -- a direct file read, not a subprocess that can merely time out. That is
    reflected in `names` (so `capture_plugin_name(selected) in plugins`, what
    doctor.py/`Capabilities.capture_plugin_installed` actually check, stops
    being pinned False forever), but `verified` stays False regardless, on
    purpose: a positive read (`package_entry_installed()` True) is a fact we
    can stand behind, but a negative one collapses several different causes
    together (genuinely absent, malformed settings.json, an unresolvable
    package root -- see that function's own docstring) the way a `claude
    plugin list` timeout does NOT. `verified=True` here would let a stale or
    unreadable settings.json read as "verified absent" downstream -- the
    wizard's post-install pass/fail gate in main.py -- rather than "unknown",
    which is the wrong failure mode for a check this cheap to get wrong.
    """
    selected = source or agent_source()
    if selected == "pi":
        # One package carries both halves. Capture rides on the entry; tracking
        # too unless the entry switches it off (`probeTracking: false`). Read as
        # pi resolves it, project over global, from the current folder.
        merged = pi_config.merged_package_entry(cwd=Path.cwd())
        if not merged.installed:
            return PluginState(verified=False)
        names = {TAP_PLUGIN_NAME}
        if not merged.tracking_off:
            names.add(tracking_plugin_name(selected))
        return PluginState(names=frozenset(names), verified=False)
    if (local or _read_records.get()) and selected in LOCAL_PLUGIN_RECORDS:
        return _local_plugins(selected)
    result = plugin_cli.list_plugins(selected)
    if not result.reachable:
        return PluginState(verified=False, error=result.detail or None)
    names: set[str] = set()
    for line in result.detail.splitlines():
        # `probe-research` is a PREFIX of `probe-research-tap`, so a line naming
        # the tap contains both. Longest match wins per line, otherwise having
        # only the tap installed would read as tracking being on too.
        tap_name = capture_plugin_name(selected)
        if selected == "codex" and LEGACY_CODEX_TAP_PLUGIN_ID in line:
            names.add(LEGACY_CODEX_TAP_PLUGIN_ID)
        elif tap_name in line:
            names.add(tap_name)
        elif DAEMON_PLUGIN_NAME in line:
            # Also a longer name that CONTAINS `probe-research`: the lean
            # plugin must not read as the full one.
            names.add(DAEMON_PLUGIN_NAME)
        elif TRACKING_PLUGIN_NAME in line:
            names.add(TRACKING_PLUGIN_NAME)
    # A non-zero exit with readable output still tells us what IS installed, but
    # not reliably what is not -- so parse it and decline to call it verified.
    return PluginState(
        names=frozenset(names), verified=result.ok, error=None if result.ok else (result.detail or None)
    )


#: Whether `installed_plugins` reads each agent's own record in place of its
#: `plugin list` (`plugin_records`).
_read_records: ContextVar[bool] = ContextVar("probe_plugin_records", default=False)


@contextmanager
def plugin_records(on: bool = True) -> Iterator[None]:
    """In this block, `installed_plugins` reads each agent's own plugin record,
    the file its `plugin list` reads (`_local_plugins`, as `probe status` does),
    instead of starting the agent's CLI; `on=False` turns that back off. The wizard reads every agent's state on
    entry and again after every change, and each `plugin list` is a Node start
    (~0.6 s on a fast Linux box, more on a laptop); the records take
    milliseconds and say the same."""
    token = _read_records.set(on)
    try:
        yield
    finally:
        _read_records.reset(token)


def claude_plugin_ledger(env: "dict[str, str] | None" = None) -> Path:
    """Claude Code's install ledger, `installed_plugins.json`: the record its
    `plugin list` reads: `PROBE_INSTALLED_PLUGINS_JSON` first, then Claude
    Code's own plugins folder, which `CLAUDE_CODE_PLUGIN_CACHE_DIR` moves, else
    `CLAUDE_CONFIG_DIR` or `~/.claude`, then `plugins/`. The one answer:
    `versions.py` grades the plugin's version off the same file, and the root
    skills read it (`root_skills.installed_plugin_root`)."""
    values = os.environ if env is None else env
    override = (values.get("PROBE_INSTALLED_PLUGINS_JSON") or "").strip()
    if override:
        return Path(override)
    moved = (values.get("CLAUDE_CODE_PLUGIN_CACHE_DIR") or "").strip()
    if moved:
        return Path(moved).expanduser() / "installed_plugins.json"
    home = (values.get("CLAUDE_CONFIG_DIR") or "").strip()
    return (Path(home).expanduser() if home else Path.home() / ".claude") / "plugins" / "installed_plugins.json"


def _claude_ledger_ids() -> list[str]:
    """Every `<plugin>@<marketplace>` the ledger holds an install for. A missing
    ledger is Claude Code with nothing installed; an unreadable one raises."""
    try:
        raw = json.loads(claude_plugin_ledger().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    plugins = raw.get("plugins") if isinstance(raw, dict) else None
    if not isinstance(plugins, dict):
        raise ValueError("no `plugins` table")
    return [key for key, entries in plugins.items() if isinstance(key, str) and entries]


def _codex_plugin_ids() -> list[str]:
    """Every `[plugins."<plugin>@<marketplace>"]` table in Codex's config.toml,
    which `codex plugin add` writes and `codex plugin list` reads (enabled or
    not, as the list shows them). A missing file is Codex with nothing added."""
    from probe._compat import tomllib
    from probe.cli import codex_config

    try:
        parsed = tomllib.loads(codex_config.config_path().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    plugins = parsed.get("plugins")
    return [key for key in plugins if isinstance(key, str)] if isinstance(plugins, dict) else []


#: The agents whose `plugin list` is a subprocess, and the file it reads.
LOCAL_PLUGIN_RECORDS = {plugin_cli.CLAUDE: _claude_ledger_ids, plugin_cli.CODEX: _codex_plugin_ids}


def _local_plugins(source: str) -> PluginState:
    """`installed_plugins` from the agent's own record, with no subprocess.

    Mirrors the CLI path on purpose: no binary on PATH reads unverified, as
    `plugin list` would (so the default and --refresh status agree), and an
    unreadable record reads unverified with the reason, never as "nothing
    installed". Names are matched whole, so the tap and the daemon plugin never
    read as the tracking plugin they contain."""
    if not plugin_cli.available(source):
        return PluginState(verified=False, error=f"`{plugin_cli.binary_name(source)}` not found on PATH")
    try:
        ids = LOCAL_PLUGIN_RECORDS[source]()
    except Exception as exc:  # noqa: BLE001 - an unreadable record is "could not look"
        return PluginState(verified=False, error=f"could not read its plugin record ({type(exc).__name__}: {exc})")
    tap_name = capture_plugin_name(source)
    known = {tap_name, DAEMON_PLUGIN_NAME, TRACKING_PLUGIN_NAME}
    names: set[str] = set()
    for plugin_id in ids:
        if source == plugin_cli.CODEX and plugin_id == LEGACY_CODEX_TAP_PLUGIN_ID:
            names.add(LEGACY_CODEX_TAP_PLUGIN_ID)
            continue
        name = plugin_id.split("@", 1)[0]
        if name in known:
            names.add(name)
    return PluginState(names=frozenset(names), verified=True)


def capture_device_id(source: str | None = None) -> str | None:
    """The paired device id the uploader recorded, if any.

    Read straight from the tap's SQLite state rather than shelling out to it:
    `probe doctor` must work when the plugin's Python cannot run at all, which
    is exactly the situation someone runs a doctor command in.
    """
    db = tap_plugin_dir(source) / "state.db"
    if not db.exists():
        return None
    import sqlite3

    try:
        with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as conn:
            row = conn.execute("SELECT v FROM meta WHERE k = 'device_id'").fetchone()
    except sqlite3.Error:
        return None
    return str(row[0]) if row and row[0] else None


# --- MCP credential resolvers, one per registry `mcp` kind ------------------


def cli_mcp_token() -> str | None:
    """The read token an agent's MCP sends, resolved as Claude Code's
    `bin/probe-mcp-headers` and pi's `src/core/mcpAuth.ts` resolve it:
    `PROBE_MCP_TOKEN` first, then the config's `mcp_token`."""
    env = (os.environ.get("PROBE_MCP_TOKEN") or "").strip()
    if env:
        return env
    from probe.sdk.config import load_context

    try:
        return (load_context() or {}).get("mcp_token") or None
    except Exception:  # noqa: BLE001 - an unreadable config holds no token we can name
        return None


def _token_check(_source: str, _codex_auth: bool | None) -> McpCheck:
    if cli_mcp_token():
        return McpCheck(McpCredential.PRESENT)
    return McpCheck(McpCredential.MISSING)


def _codex_check(_source: str, codex_auth: bool | None) -> McpCheck:
    if codex_auth is None:
        return McpCheck(McpCredential.UNKNOWN, what="`codex mcp list` did not answer")
    if not codex_auth:
        return McpCheck(McpCredential.MISSING)
    # `codex mcp list` answers `bearer_token` for ANY header, a dead one too:
    # a bearer this device has since replaced is a login needed, not "on".
    from probe.cli.setup import codex_mcp_token_drifted

    if codex_mcp_token_drifted():
        return McpCheck(McpCredential.MISSING)
    return McpCheck(McpCredential.PRESENT)


def _pi_check(_source: str, _codex_auth: bool | None) -> McpCheck:
    """pi has two providers: pi-mcp-adapter serves our manifest with ITS OWN
    OAuth login when installed (our extension stands down); otherwise our
    extension's bridge sends the CLI's read token."""
    if pi_config.mcp_adapter_installed(cwd=Path.cwd()):
        return McpCheck(McpCredential.UNKNOWN, what="served by pi-mcp-adapter, which keeps its own login")
    if pi_config.merged_package_entry(cwd=Path.cwd()).extension_filtered_out:
        # The bridge IS the extension: filtered out, nothing serves our MCP.
        return McpCheck(
            McpCredential.UNKNOWN,
            what="pi's settings filter out Probe's extension (`extensions` on probe-research-pi)",
        )
    return _token_check(_source, _codex_auth)


def _kimi_check(_source: str, _codex_auth: bool | None) -> McpCheck:
    """Kimi Code sends the bearer the wizard wrote into its installed manifest
    (`kimi_config.sync_mcp_bearer`); it has to be the token this device holds."""
    from probe.cli import kimi_config
    from probe.cli.setup import current_mcp_token

    try:
        sent = kimi_config.installed_mcp_bearer()
    except kimi_config.ManifestUnreadable as exc:
        return McpCheck(McpCredential.UNKNOWN, what=str(exc))
    if not sent and not kimi_config.mcp_server_same_deployment():
        return McpCheck(McpCredential.UNKNOWN,
                        what="Kimi's plugin points at another Probe deployment than this device")
    held = current_mcp_token()  # what the wizard writes (`kimi_config.sync_mcp_bearer`)
    if sent and held and sent == held:
        return McpCheck(McpCredential.PRESENT)
    return McpCheck(McpCredential.MISSING)


def _mcp_resolvers() -> dict:
    from probe.harness import registry as reg

    return {
        reg.MCP_PLUGIN_FILE: _token_check,
        reg.MCP_CONFIG_TOML: _codex_check,
        reg.MCP_EXTENSION_BRIDGE: _pi_check,
        reg.MCP_PLUGIN_MANIFEST: _kimi_check,
    }


#: One credential resolver per registry `mcp` kind (`test_mcp_state.py` fails
#: when a kind has none).
MCP_RESOLVERS = _mcp_resolvers()


#: The API's verdict on this device's read token, for this process:
#: (token, "ok" | "rejected" | "unreachable"), or None when nobody asked.
#: Only `probe doctor`, the wizard (`refresh_mcp_token_verdict`) and `probe
#: status --refresh` (`ask_mcp_token_verdict`, recorded only when it answers in
#: time) ask, so a status read anywhere else never touches the network.
_MCP_TOKEN_VERDICT: tuple[str, str] | None = None


def refresh_mcp_token_verdict() -> str | None:
    """Ask the API once whether the read token is still accepted (`/v1/me`, the
    check `probe mcp status` makes). None when there is no token to ask about."""
    token = cli_mcp_token()
    if not token:
        record_mcp_token_verdict(None, None)
        return None
    state = ask_mcp_token_verdict(token)
    record_mcp_token_verdict(token, state)
    return state


def ask_mcp_token_verdict(token: str) -> str:
    """The API's verdict on `token` -- ok | rejected | unreachable -- recording
    nothing. Split from `refresh_mcp_token_verdict` so a caller that bounds the
    wait (`probe status --refresh`) records only an answer that came in time."""
    from probe.cli.main import _verify_read
    from probe.sdk.config import resolve

    try:
        state, _identity = _verify_read(token, resolve().base_url)
    except Exception:  # noqa: BLE001 - a failed check is "unknown", never "rejected"
        state = "unreachable"
    return state


def record_mcp_token_verdict(token: str | None, state: str | None) -> None:
    """What this process's `check_mcp` reads as the API's verdict on `token`."""
    global _MCP_TOKEN_VERDICT
    _MCP_TOKEN_VERDICT = (token, state) if token and state else None


def mcp_token_rejected() -> bool:
    """The API refused the token this device holds now (asked this process)."""
    token = cli_mcp_token()
    return bool(token) and _MCP_TOKEN_VERDICT == (token, "rejected")


def _sends_held_token(source: str, kind: str) -> bool:
    """Whether this agent's MCP sends the device's held read token, so a
    rejection of that token is ITS rejection. Codex may hold its own OAuth
    login instead; only its synced bearer counts."""
    from probe.harness import registry as reg

    if kind != reg.MCP_CONFIG_TOML:
        return True
    try:
        from probe.cli import codex_config

        return codex_config.configured_bearer(CODEX_MCP_NAME) == cli_mcp_token()
    except Exception:  # noqa: BLE001 - unreadable config: do not claim a rejection
        return False


def check_mcp(source: str, *, codex_auth: bool | None = None) -> tuple[str | None, McpCheck | None]:
    """(registry mcp kind, credential check) for one agent. Never raises."""
    from probe.harness import get_registry

    try:
        kind = get_registry().get(source).mcp
    except Exception:  # noqa: BLE001 - an unknown source offers no MCP
        return None, None
    if kind is None:
        return None, None
    try:
        check = MCP_RESOLVERS[kind](source, codex_auth)
    except Exception as exc:  # noqa: BLE001 - a status must never crash the wizard
        return kind, McpCheck(McpCredential.UNKNOWN, what=f"check failed ({type(exc).__name__})")
    if check.credential == McpCredential.PRESENT and mcp_token_rejected() and _sends_held_token(source, kind):
        return kind, McpCheck(McpCredential.REJECTED)
    return kind, check


def _settings_package(source: str | None) -> bool:
    """The agent's Probe package is a settings entry (pi): one package for
    tracking and capture, read from a settings file rather than a plugin CLI."""
    from probe.harness import get_registry

    try:
        return get_registry().get(source or agent_source()).lean_profile == "settings-filter"
    except Exception:  # noqa: BLE001 - an unknown agent is not one
        return False
