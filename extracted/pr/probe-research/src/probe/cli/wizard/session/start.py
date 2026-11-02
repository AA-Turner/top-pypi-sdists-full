"""agent/src/probe/cli/main.py."""

from __future__ import annotations
import os
import re

import typer
from ....sdk.settings.settings import resolve


def _begin_wizard_session(
    *,
    agent,
    action,
    auth_code,
):
    """`_wizard_session`'s opening: flags checked, the funnel's first event, the persistent
    install, and which coding agents this run offers."""
    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.core import events as json_events
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod

    # Direct Python callers receive Typer's argument sentinel as the default.
    install_code = auth_code if isinstance(auth_code, str) else None
    if install_code is not None and not re.fullmatch(r"[A-Z0-9]{10}", install_code):
        raise typer.BadParameter(
            "the sign-in code must contain exactly 10 uppercase letters or digits"
        )

    # Flag validation BEFORE the funnel entry event: a `--agent bogus` typo is
    # a usage error, and emitting first would file it in the funnel's
    # "infrastructure died before wizard.started" bucket.
    # `--agent` (repeatable; see `_explicit_agent_sources` for its aliases).
    explicit_agent_sources = _explicit_agent_sources(agent)

    # `wizard.invoked` fires BEFORE the bootstrap below: the ephemeral-npx →
    # persistent install is the most failure-prone distribution step, and a
    # session that dies inside it must still enter the funnel. The raw --action
    # string is clamped to known values — event properties carry enums, never
    # free-form user input (a mis-pasted secret must not ride to the vendor).
    known_actions = {a.value for a in actions_mod.Action}
    tel = telemetry_mod.TelemetryContext.start(
        via=telemetry_mod.Via.WIZARD,
        interactive=wizard.interactive(),
        base_url=resolve(base_url=_conn.base_url).base_url,
    )
    tel.emit(
        telemetry_mod.EVENT_WIZARD_INVOKED,
        invoked_action=(action if action in known_actions else "invalid" if action else None),
        interactive=wizard.interactive(),
    )

    # FIRST among the real work. `npx probe-research` launches us through an
    # EPHEMERAL `uv tool run` / `pipx run`, which leaves no binary behind — and
    # everything below assumes one exists afterwards (`probe doctor`, the
    # plugin's version-check hook, the MCP headers helper).
    from probe.cli.install.bootstrap import ensure_persistent_install

    # THE WIZARD'S ONE SERVER CALL (`POST /v1/device-state`): the account,
    # every agent's capture key and the version manifest, in one answer. Sent
    # here so it is in flight while the bootstrap and the local checks run.
    # It replaced a `/v1/me`, an unfiled-runs list and a capture check PER
    # AGENT plus a detached manifest fetch -- seven serial calls, nine seconds
    # of spinner on a two-agent machine. Every state read below uses it, and a
    # step that changes state asks again, once.
    from probe.cli.wizard import state as capabilities_mod

    def _ask_server() -> capabilities_mod.DeviceStateResolver:
        # An older server's answer carries no manifest, and the wizard spawns
        # no detached refresher: fetch it when someone will read the Versions
        # row, or when auto-update will act on it.
        from probe.shared.updates import version_policy

        return _start_device_state(
            warm_manifest=wizard.interactive() or version_policy.autoupdate_enabled()
        )

    device_state = _ask_server()

    # Only an INSTALL (the menu's first run, configure, an update a person
    # asked for) finishes an uninstall that stopped halfway; every other action,
    # the background update a SessionStart hook spawns included, refuses while
    # one is LIVE.
    from probe.cli.install import install as install_pipeline_mod

    boot = ensure_persistent_install(
        finish_uninstall=action in (None, actions_mod.Action.CONFIGURE)
        or (action == actions_mod.Action.UPDATE and install_pipeline_mod.update_may_finish()))
    refused = bool(getattr(boot, "refused", False))
    if action == actions_mod.Action.CONFIGURE and getattr(boot, "already_persistent", False) and not refused:
        # An install over an install of the same version: a health check that
        # repairs what fails (plan clean-uninstall-reinstall R-T3), not "it is
        # there, so it works".
        from probe.cli.install import identity_check
        from probe.cli.install.bootstrap import verify_installed

        # Identity first (R-T4): the daemon key is held to the signed-in
        # account BEFORE the check may restart the service, so no daemon
        # worker starts on another team's key. Its problems end the configure
        # unfinished (`_run_wizard_action`'s verification reads the same answer).
        identity_check.reconcile_once()
        boot = verify_installed() or boot
        refused = bool(getattr(boot, "refused", False))
    if boot.message:
        print(boot.message)
    json_events.persistent_install(boot)
    if refused and action == actions_mod.Action.CONFIGURE:
        # Nothing installs while an uninstall runs (its barrier is LIVE), nor
        # without uv: the message above says what to do.
        raise typer.Exit(2)

    codex_session = bool(os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SANDBOX"))
    # `wizard.detectable_sources()`, not a fresh literal and not
    # MARKETPLACE_AGENT_SOURCES filtered by `plugin_cli.available` inline:
    # this asks "which coding agents exist on this machine", and that
    # question now has three possible answers, not two -- pi IS a binary
    # `shutil.which` can find, it just has no MARKETPLACE the way
    # claude_code/codex do (see `detectable_sources`'s docstring for the
    # stale "pi has no CLI" claim this replaces). Calling the shared helper
    # rather than re-deriving this here keeps the step-1 picker
    # (`run_agent_menu`) and this computation from silently drifting apart.
    available_sources = wizard.detectable_sources()
    if explicit_agent_sources is not None:
        agent_defaults = explicit_agent_sources
    elif codex_session and wizard.interactive():
        agent_defaults = ("codex",)
    else:
        # ONE RULE, TTY OR NOT: configure the coding agents this machine has.
        #
        # A headless run used to narrow to `("claude_code",)` here, to "preserve
        # the historical headless default" for scripts that opt into more with
        # `--agent both`. What that actually produced was a SILENT wrong answer
        # on the one path with nobody watching: a Codex user's agent runs
        # `probe install --yes` from a tool call, the wizard configures Claude
        # Code, and every screen it prints says the install succeeded. The
        # narrowing is invisible precisely because the picker and the confirm
        # screen -- the two places that would have named the selection -- are
        # both gated on `interactive()` and never ran.
        #
        # A default that differs by TTY-ness is also a rule nobody can hold: the
        # same command, same machine, same flags, configures a different set of
        # agents depending on whether stdout happens to be a pipe. Scripts that
        # want the old narrow behaviour still get it, and now state it, with
        # `--agent claude`.
        #
        # `codex_session` stays a PRE-TICK, not a pin, and so is scoped to the
        # interactive path above: inside Codex a human sees codex ticked and can
        # untick it. Applied headless it would be the same silent narrowing this
        # branch exists to remove, just landing on a different agent.
        agent_defaults = available_sources or ("claude_code",)
    return (
        install_code,
        explicit_agent_sources,
        tel,
        capabilities_mod,
        _ask_server,
        device_state,
        available_sources,
        agent_defaults,
    )
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.agent_flags import _explicit_agent_sources  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.session import _start_device_state  # noqa: E402 -- pieces need each other; the front door loads this one first
