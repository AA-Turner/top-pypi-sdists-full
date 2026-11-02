"""move one agent to a Who records profile (agent or daemon): daemon availability, its key, live sessions, recorder rules, follow the machine's pick."""

from __future__ import annotations
import threading
from contextvars import ContextVar
from collections.abc import Callable

from probe.cli.wizard.apply import agent_rules
from probe.shared.harness.harnesses.codex import config as codex_config
from probe.shared.harness.harnesses import pi as pi_config
from probe.shared.harness import reasoning_summaries
from probe.cli.wizard.state.state import (
    DAEMON_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME,
    Capabilities)
from probe.cli.wizard.agents import _installable_rows, agent_label, short_path


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
        from probe.sdk.settings.settings import resolve

        settings = resolve(base_url=base_url) if base_url else resolve()
    except Exception:  # noqa: BLE001 - an unreadable config is "cannot tell"
        return None, None
    if not settings.token:
        return None, None
    answer: list = []

    def ask() -> None:
        try:
            from probe.foundation.request_identity.surface import Surface
            from probe.sdk.delivery.transport.transport import Transport

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
    from probe.sdk.settings.settings import load_context

    try:
        return bool((load_context() or {}).get("companion_token"))
    except Exception:  # noqa: BLE001 - an unreadable config is "not held"
        return False


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
    from probe.shared import mailbox
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
    from probe.sdk.settings.settings import load_context, save_context

    token = str((load_context() or {}).get("companion_token") or "")
    if not token:
        return []
    lines = _revoke(token, base_url=base_url, what="the Probe daemon's key")
    save_context({"companion_token": None})
    return lines


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
    from probe.sdk.settings.settings import ConfigUnreadable

    from probe.foundation.harness_registry import get_registry

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
        from probe.cli.commands.daemon.companion import provision_daemon
        from probe.cli.commands.daemon.daemon import ai_libraries

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
        from probe.shared.harness.harnesses import pi as pi_config

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
        from probe.shared.harness.harnesses.codex import config as codex_config

        try:
            codex_config.remove_mcp_server(TRACKING_PLUGIN_NAME)
        except codex_config.ConfigError as exc:
            lines.append(f"! could not remove the Probe MCP from Codex's config: {exc}")

    # What is installed NOW, not the snapshot the screen was drawn from: another
    # row applied in the same commit may have installed `drop` since.
    from probe.cli.wizard.state.plugins import installed_plugins

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

    from probe.cli.commands.daemon.daemon import ai_libraries

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
from probe.cli.wizard.account.sign_in import _revoke  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.agent_files import _instruction_file_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.apply import CAPTURE_PLUGIN_LABEL, _apply_root_skills  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.plugins import install_plugin, uninstall_plugin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.codex.hook_approval import approve_codex_hooks  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.readiness import _settings_profile_ready  # noqa: E402 -- pieces need each other; the front door loads this one first
