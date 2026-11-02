"""`probe doctor` — read-only diagnostic over the same state the wizard renders.

Two renderings, one state struct (see capabilities.py). The menu shows it as
toggles; this prints it.

The line that earns this command its place is LAST UPDATE ATTEMPT. Auto-update
runs detached, so it cannot report failure through the SessionStart hook that
spawned it. Without a recorded attempt, an auto-updater that has been silently
failing for a month is indistinguishable from one that works. `claude doctor`
solves it the same way.

Read-only and fail-soft throughout: this is the command someone runs when things
are already broken, so it must never be the thing that breaks.
"""

from __future__ import annotations

import dataclasses
import os
import shutil
import time

from probe.cli.wizard.apply import agent_rules
from probe.shared.updates import autoupdate
from probe.shared.harness.harnesses.codex import config as codex_config
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.state import (
    Capabilities,
    TokenSource)
from probe.cli.wizard.state.device_state import DeviceStateOutcome
from probe.shared.harness.mcp import McpCredential
from probe.cli.wizard.state.plugins import PluginState
from probe.cli.wizard.state.capture_credentials import tap_token_env
from probe.cli.wizard.state.agent_identity import tracking_plugin_name

#: Why a Codex MCP reads unknown in a files-only read (`collect(local=True)`).
CODEX_MCP_NOT_CHECKED = (
    "not checked: Codex keeps an OAuth login where only `codex mcp list` reads it "
    "(`probe status --refresh` asks it)"
)


def _version_comparison() -> tuple[tuple, float | None]:
    """Grade this machine against the CACHED manifest. Never hits the network.

    `probe doctor` must work offline and must not add a network round trip to a
    diagnostic command, so it reads the manifest the session-start hook already
    keeps warm. A stale or absent cache yields no rows and an age of None, which
    the renderer states as "could not check" -- the one thing it must never do is
    let an unreadable manifest print as though everything is current.
    """
    from probe.shared.updates import version_policy
    from probe.shared.updates import updates as versions_mod

    try:
        manifest, fetched_at, _ok = version_policy.read_cache()
    except Exception:
        return ((), None)
    if not isinstance(manifest, dict):
        return ((), None)
    try:
        rows = tuple(versions_mod.compare(manifest))
    except Exception:
        return ((), None)
    age = max(0.0, time.time() - fetched_at) if fetched_at else None
    return (rows, age)


def collect(*, local: bool = False, plugins: PluginState | None = None) -> Capabilities:
    """Snapshot this device. Every probe is individually fail-soft.

    Inside `device_state_scope` (the wizard) the server's half comes from its
    one call, resolved only AFTER the local checks so they run while the
    request is in flight: an answer means no network call here at all, and an
    older server without the route (`UNSUPPORTED`) means asking the old way.
    Outside it (`probe doctor`) this asks the old way, offline-first.

    `local` (`probe status` without --refresh) reads files only: no agent CLI
    runs and nothing is sent. The plugin lists come from the records the
    agents' own `plugin list` reads (`installed_plugins(local=True)`), Codex's
    MCP login from the header in its config.toml (what `codex mcp list` reports
    as `bearer_token`), and the server's half is unknown: no confirmed account
    (`logged_in_as` None), no verdict on any credential, no agent version. An
    OAuth Codex login is not in that file, so its MCP reads unknown, "not
    checked" (`CODEX_MCP_NOT_CHECKED`).

    `plugins`: this agent's plugin list, already read (`probe status --refresh`
    asks every agent's CLI at once), in place of asking here."""
    remote = None if local else _remote_state.get()
    from probe.cli.install import updater
    from probe.cli.wizard.state.state import TRACKING_PLUGIN_NAME
    from probe.cli.wizard.state.agent_identity import tracking_plugin_name
    from probe.cli.wizard.state.capture_credentials import (
        capture_device_id,
        capture_token_sources,
        verify_capture_credential,
        tap_plugin_dir)
    from probe.cli.wizard.state.agent_identity import (
        capture_plugin_name,
        agent_source)
    from probe.cli.wizard.state.plugins import installed_plugins
    from probe.cli.wizard.state.state import (
        CODEX_MCP_NAME,
        LEGACY_CODEX_TAP_PLUGIN_ID)

    warnings: list[str] = []

    try:
        install_method = updater.detect_install().method
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        install_method = None

    base_url: str | None = None
    config_context: str | None = None
    has_token = False
    try:
        from probe.sdk.settings.settings import current_context_name, resolve

        settings = resolve()
        base_url = settings.base_url
        config_context = current_context_name()
        has_token = bool(settings.token)
    except Exception as exc:  # noqa: BLE001
        settings = None
        if base_url:
            warnings.append(f"could not verify login against {base_url}: {exc}")

    selected_agent = agent_source()
    # The profile's plugin: `probe-research-daemon` where the daemon records.
    TRACK = tracking_plugin_name(selected_agent)
    selected_tap = capture_plugin_name(selected_agent)
    if plugins is None:
        plugins = installed_plugins(source=selected_agent, local=local)
    try:
        from probe.cli.install.integrations import integrations as integration_repair

        unusable = integration_repair.unusable_plugins(selected_agent)
    except Exception:  # noqa: BLE001 -- a check, never a failed snapshot
        unusable = {}
    sources = capture_token_sources(selected_agent)
    # Resolved HERE, after the slowest local check above (the agent's own
    # plugin CLI), so that check ran while the request was in flight.
    state = remote() if remote is not None else None
    if local:
        login = _LoginCheck()
        credential_valid = None
    elif state is None or state.outcome is DeviceStateOutcome.UNSUPPORTED:
        # `probe doctor`, or a server that predates the one call: the old way.
        login = _check_login(settings) if settings is not None else _LoginCheck()
        credential_valid = verify_capture_credential(selected_agent) if sources else None
    else:
        login = _login_from_state(state, has_token=has_token, base_url=base_url)
        if not sources:
            credential_valid = None
        elif selected_agent in state.capture or not state.answered:
            credential_valid = state.capture.get(selected_agent)
        else:
            # Answered, but with no verdict for this agent: its credential is
            # paired to ANOTHER server and never rode in the call. Ask its own
            # server, the old way.
            credential_valid = verify_capture_credential(selected_agent)
    warnings[:0] = login.warnings
    logged_in_as = login.logged_in_as
    api_credential_valid = login.api_credential_valid
    settings_autoupdate = autoupdate.load()

    if local:
        pass  # nothing was asked: "could not verify" would read as a failure
    elif credential_valid is False:
        warnings.append(
            "the capture credential was rejected by the ingest service; "
            "re-run `probe wizard` to pair this device again"
        )
    elif sources and credential_valid is None:
        warnings.append("could not verify the capture credential (offline or endpoint unavailable)")
    if LEGACY_CODEX_TAP_PLUGIN_ID in plugins:
        warnings.append(
            f"legacy {LEGACY_CODEX_TAP_PLUGIN_ID} is still installed and can race the unified tap; "
            "re-run `probe wizard` to remove it"
        )

    is_mcp_authenticated: bool | None = None
    codex_login_unread = False
    # The daemon profile installs no MCP, so there is no MCP login to check.
    if selected_agent == "codex" and TRACK == TRACKING_PLUGIN_NAME and TRACK in plugins:
        if local:
            from probe.shared.harness.harnesses.codex import config as codex_config

            # `codex mcp list` answers `bearer_token` for any header there; an
            # OAuth login lives where only Codex can read it, so it is unknown.
            status = codex_config.BEARER_STATUS if codex_config.configured_bearer(CODEX_MCP_NAME) else None
            codex_login_unread = status is None
        else:
            status = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
        if status is not None:
            is_mcp_authenticated = status in {"o_auth", "bearer_token"}
        if is_mcp_authenticated is False:
            warnings.append(
                "the probe-research MCP is installed but not logged in; "
                "re-run `probe wizard` to complete Codex OAuth"
            )

    # DRIFT IS CHECKED FOR ANY MACHINE THAT HAS A CODEX ENTRY, not just one
    # where Codex is the selected agent. A box with both agents installed
    # reports a single `agent_source`, so gating this on `== "codex"` made the
    # only local signal for a dead Codex token unreachable on exactly the
    # machines most likely to drift -- doctor printed "CLI + MCP: ok" while
    # every Codex call 401'd. `codex mcp list` cannot substitute: it reports
    # `bearer_token` for any header, valid or not.
    #
    # Unconditional is safe because the check is self-guarding: no configured
    # bearer, no held token, or the two agreeing all return None, and it reads
    # two files without shelling out.
    stale = stale_codex_token_warning()
    if stale:
        warnings.append(stale)

    if TokenSource.ENVIRONMENT in sources:
        token_env = tap_token_env(selected_agent)
        warnings.append(
            f"{token_env} is set in this shell. It overrides local pairing "
            "state, so capture can appear off in the menu yet still be on."
        )

    from probe.cli.wizard.state.mcp_checks import check_mcp

    # The per-agent MCP answer (Capabilities.mcp_state): Codex's reuses the
    # `codex mcp list` read above instead of asking again.
    mcp_kind, mcp_check = check_mcp(selected_agent, codex_auth=is_mcp_authenticated)
    if codex_login_unread and mcp_check is not None and mcp_check.credential == McpCredential.UNKNOWN:
        # Nothing ran: "`codex mcp list` did not answer" would be untrue.
        mcp_check = dataclasses.replace(mcp_check, what=CODEX_MCP_NOT_CHECKED)

    from probe.shared.updates import updates as versions_mod

    rules_installed = agent_rules.is_installed()
    rules_stale = rules_installed and not agent_rules.is_current()

    version_rows, manifest_age = _version_comparison()
    tap_warning = tap_behind_warning(version_rows, selected_agent, "installed" if TRACK in plugins else None)
    if tap_warning:
        warnings.append(tap_warning)
    python_missing = capture_python_missing(selected_agent)
    if python_missing:
        warnings.append(
            "session capture cannot run: it needs Python 3.11 or newer, and the last "
            f"session start found {python_missing}. Install Python 3.11 or newer, "
            "then start a new session."
        )
    return Capabilities(
        # Not `__version__`: after the wizard's own Update that is the number
        # this process started with, while the Versions block above it grades
        # the upgrade. The two rows must agree.
        cli_version=versions_mod.cli_version(),
        version_rows=version_rows,
        version_manifest_age_s=manifest_age,
        install_method=install_method,
        claude_available=shutil.which("claude") is not None,
        agent_version=None if local else _agent_version(selected_agent),
        codex_available=shutil.which("codex") is not None,
        agent_source=selected_agent,
        logged_in_as=logged_in_as or None,
        api_credential_valid=api_credential_valid,
        base_url=base_url,
        config_context=config_context,
        # Installed means USABLE (plan clean-uninstall-reinstall R-T5): a record
        # whose files are gone, a disabled plugin, a project-scope install or
        # pi's filtered-out extension reads as not installed, so configure
        # puts it right instead of saying "Nothing to change".
        tracking_plugin_installed=TRACK in plugins and TRACK not in unusable,
        capture_plugin_installed=selected_tap in plugins and selected_tap not in unusable,
        legacy_capture_plugin_installed=LEGACY_CODEX_TAP_PLUGIN_ID in plugins,
        plugins_verified=plugins.verified,
        plugins_error=plugins.error,
        capture_token_sources=sources,
        capture_credential_valid=credential_valid,
        capture_killswitched=(tap_plugin_dir(selected_agent) / ".disabled").exists(),
        capture_awaiting_confirmation=_capture_awaiting_confirmation(selected_agent),
        capture_python_missing=python_missing,
        capture_device_id=capture_device_id(selected_agent),
        capture_last_stop=_capture_last_stop(),
        mcp_authenticated=is_mcp_authenticated,
        mcp_token_held=_mcp_token_held(),
        mcp_kind=mcp_kind,
        mcp_check=mcp_check,
        agent_rules_installed=rules_installed,
        agent_rules_stale=rules_stale,
        auto_update_enabled=settings_autoupdate.enabled,
        auto_update_by_default=settings_autoupdate.by_default,
        last_update_attempt=(
            _attempt_as_it_stands(
                settings_autoupdate.last_attempt, _probe_plugin_of(selected_agent, TRACK in plugins)
            ).describe()
            if settings_autoupdate.last_attempt
            else None
        ),
        last_update_attempt_summary=(
            settings_autoupdate.last_attempt.summary()
            if settings_autoupdate.last_attempt
            else None
        ),
        last_update_skip=(
            settings_autoupdate.last_skip.describe() if settings_autoupdate.last_skip else None
        ),
        live_runs=_live_runs(),
        outbox_status=_outbox_status(),
        daemon_ai_libraries=_daemon_ai_libraries(),
        warnings=warnings,
    )


def _probe_plugin_of(selected: str, selected_has_it: bool):
    """`plugin_after` for `updater.settle_stale_notes`: an agent's installed
    Probe plugin ("installed"), or None when it has none. The agent doctor runs
    for is known (`selected_has_it`, from its own plugin read); another is read
    from the record its own plugin list reads (`installed_plugins(local=True)`:
    files only, no agent CLI started). Unreadable: None, which keeps a watcher
    from before the hand-back on the restart line."""
    def plugin_after(source: str) -> str | None:
        if source == selected:
            return "installed" if selected_has_it else None
        try:
            from probe.cli.wizard.state.plugins import installed_plugins

            return "installed" if tracking_plugin_name(source) in installed_plugins(source=source, local=True) \
                else None
        except Exception:  # noqa: BLE001 - see docstring
            return None

    return plugin_after


def _attempt_as_it_stands(attempt, plugin_after):
    """The last update attempt as `probe doctor` prints it: what it said about
    sessions still on an older tap as it stands now (`updater.settle_stale_notes`:
    gone once none is left, "they move ... no restart needed" where they follow).
    Every release before 0.304.0 told the person to restart them; the sessions
    move with no restart, and doctor kept printing "restart them" until the next
    update. Never raises: the attempt as recorded."""
    try:
        import dataclasses

        from probe.cli.install import updater

        settled = updater.settle_stale_notes(attempt.plugin_detail, plugin_after=plugin_after)
        return attempt if settled == attempt.plugin_detail else dataclasses.replace(attempt, plugin_detail=settled)
    except Exception:  # noqa: BLE001 - see docstring
        return attempt


def _mcp_token_held() -> bool:
    from probe.shared.harness.mcp_token import current_mcp_token

    return bool(current_mcp_token() or os.environ.get("PROBE_MCP_TOKEN"))


def _daemon_ai_libraries() -> str | None:
    try:
        from probe.cli.commands.daemon.daemon import located_ai_libraries

        return located_ai_libraries() or "missing"
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None


def _capture_awaiting_confirmation(source: str) -> bool:
    try:
        from probe.cli.capture import capture

        return capture.awaiting_confirmation(source)
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return False


def _capture_last_stop() -> str | None:
    try:
        from probe.cli.capture import capture

        return capture.describe_last_stop()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None


#: Left in the tap's state folder by its SessionStart when it found no Python
#: 3.11+ to run the tap on (`hooks/tap-python.sh` TAP_PYTHON_MISSING), holding
#: what it found instead; removed by the next one that finds one.
TAP_PYTHON_MISSING = ".python-missing"


def capture_python_missing(source: str) -> str | None:
    """What the tap's last SessionStart found instead of a Python 3.11+
    ("python3 3.9.6", "no python3"), or None when it found one.

    The hook is the one that knows: it resolves the interpreter the way it runs
    the tap, so this reads its verdict rather than guessing at its search."""
    from probe.cli.wizard.state.capture_credentials import tap_plugin_dir

    try:
        text = (tap_plugin_dir(source) / TAP_PYTHON_MISSING).read_text(encoding="utf-8")
    except (OSError, KeyError, ValueError):  # no tap for this agent, no file, not text
        return None
    lines = text.strip().splitlines()
    return (lines[0].strip()[:80] if lines else "") or "no python3 that runs"


def _agent_version(source: str) -> str | None:
    """The selected agent binary's version. Fail-soft, like every other probe.

    `agent_source()` speaks "claude_code"/"codex"; `Agent` is "claude"/"codex".
    Mapped explicitly rather than passed straight to `Agent(...)`: that raises
    on "claude_code", the fail-soft `except` swallows it, and the field reads
    None on every machine -- a version probe that reports nothing, forever,
    while looking like it works.

    pi DOES have an `Agent` member now, and it is still not asked here: it is
    not an importer (`backfill.IMPORTER_AGENTS` is the claude/codex pair this
    probe reports on, and `resolve_agent` refuses `--agent pi`), and its
    version is not a fact about the import this line describes. The old `else`
    here defaulted straight to `Agent.CLAUDE`, which reported Claude Code's OWN
    version string as if it were pi's -- correct-looking output for the wrong
    question. None, same as every other "cannot check" case this function
    already returns.
    """
    if source in ("pi", plugin_cli.KIMI):
        return None
    try:
        from probe.cli.imports.folder.agents.agents import Agent
        from probe.cli.imports.folder.agents.flags import agent_version

        agent = Agent.CODEX if source == "codex" else Agent.CLAUDE
        return agent_version(agent)
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None


def _live_runs() -> list[str]:
    try:
        from probe.foundation.durable import run_lock

        return run_lock.live_runs()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return []


def _outbox_status() -> dict | None:
    """The outbox's status.json, read only (`collect` runs from `probe
    status`, which promises no request and no process)."""
    try:
        from probe.sdk.delivery.journal.journal import Journal

        return Journal.read_status()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None
from probe.cli.wizard.doctor.server_state import _LoginCheck, _check_login, _login_from_state, _remote_state  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.doctor.version_rows import tap_behind_warning  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.codex.doctor import stale_codex_token_warning  # noqa: E402 -- pieces need each other; the front door loads this one first
