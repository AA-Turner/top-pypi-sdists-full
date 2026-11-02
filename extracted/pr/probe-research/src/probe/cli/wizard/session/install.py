"""plan and settle an install: each agent's marketplace plugins, grants reused, one shared capability selection, completion once every agent finished."""

from __future__ import annotations
import dataclasses
from dataclasses import dataclass
from ....sdk.settings.settings import resolve
from ....shared.harness import plugins as plugin_cli


def _installing(caps_by_source, selection) -> list[str]:
    """The agents an install with `selection` gets a marketplace plugin for,
    their CLI on this machine: each refreshes its marketplace first, all of
    them at once (`setup.marketplace_refreshes`)."""
    from probe.cli import wizard as wizard

    return [
        source
        for source, caps in caps_by_source.items()
        if source in wizard.MARKETPLACE_AGENT_SOURCES
        and plugin_cli.available(source)
        and (
            (selection.tracking and not caps.tracking_plugin_installed)
            or (selection.capture and not caps.capture_plugin_installed)
        )
    ]


def _install_plan(caps_by_source, selection) -> dict:
    """Each `_installing` agent's marketplace plugins, (capability, name), in
    the order its own steps install them: installed with its marketplace's
    refresh, all agents at once (`setup.marketplace_refreshes`). An agent with
    the legacy Codex capture plugin installs its tap at its own step, after
    that plugin is removed."""
    from probe.cli.wizard import state as capabilities
    from probe.cli import wizard as wizard
    from probe.cli.wizard.state.state import Capability

    plan = {}
    for source in _installing(caps_by_source, selection):
        caps = caps_by_source[source]
        wanted = []
        if selection.tracking and not caps.tracking_plugin_installed:
            wanted.append((Capability.TRACKING, capabilities.tracking_plugin_name(source)))
        if selection.capture and not caps.capture_plugin_installed and not caps.legacy_capture_plugin_installed:
            wanted.append((Capability.CAPTURE, wizard.CAPTURE_PLUGIN_LABEL[source]))
        plan[source] = wanted
    return plan


def _install_grants_held(caps_by_source, selection, *, base_url: str) -> bool:
    """Reuse the selected agents' credentials, independently of installation.

    A disabled capture credential is still authorized: the install confirmation
    enables it. An unavailable identity check is also not a reason to sign in
    again, but an explicitly rejected credential is. Check the actual MCP token
    rather than assuming that every saved API token was minted alongside one.

    If anything is missing, the caller requests the complete selection in one
    approval: the browser can switch accounts, so renewing capture alone could
    leave it belonging to a different account from the saved API/MCP tokens.
    """
    from probe.cli.wizard.apply.capture_credentials import has_source_capture_grant

    settings = resolve(base_url=base_url)
    if selection.tracking and (
        not settings.token
        or not settings.mcp_token
        or any(caps.api_credential_valid is False for caps in caps_by_source.values())
    ):
        return False
    if selection.capture and not all(
        has_source_capture_grant(source, caps.capture_token_sources)
        and caps.capture_credential_valid is not False
        for source, caps in caps_by_source.items()
    ):
        return False
    if selection.tracking:
        from probe.cli.wizard.state.mcp_checks import verify_mcp_credential

        return (
            verify_mcp_credential(base_url=settings.base_url, token=settings.mcp_token) is not False
        )
    return True


def _shared_selection(
    caps_by_source,
    *,
    tracking,
    capture,
    auto_update,
    agent_rules,
    configured: bool,
):
    """One capability decision covering every selected agent, plus the snapshot
    it was resolved against.

    Extracted so the interactive steps can be asked ONCE, before the per-agent
    apply loop -- which is what lets `‹ Back` walk them. It has always been
    correct for a single agent too (every `all()`/`any()` over one item is that
    item), so there is no second code path for the common case.

    A feature reads as ENABLED only when every selected agent has it, so a
    partially configured machine visibly offers to finish the gap...
    """
    from probe.cli import wizard as wizard

    caps = next(iter(caps_by_source.values()))
    aggregate = dataclasses.replace(
        caps,
        tracking_plugin_installed=all(
            item.tracking_plugin_installed for item in caps_by_source.values()
        ),
        capture_plugin_installed=all(
            item.capture_plugin_installed for item in caps_by_source.values()
        ),
        capture_token_sources=(
            caps.capture_token_sources
            if all(item.capture_on for item in caps_by_source.values())
            else ()
        ),
        capture_killswitched=any(item.capture_killswitched for item in caps_by_source.values()),
        # Never the device's: a pending lock is one agent's, and the per-agent
        # apply leaves it pending (`leave_pending`). On the aggregate it would
        # make `resolve_selection` keep capture for every agent.
        capture_awaiting_confirmation=False,
        agent_rules_installed=all(item.agent_rules_installed for item in caps_by_source.values()),
        agent_rules_stale=any(item.agent_rules_stale for item in caps_by_source.values()),
        mcp_authenticated=all(
            item.agent_source != "codex" or item.mcp_authenticated is True
            for item in caps_by_source.values()
        ),
        plugins_verified=all(item.plugins_verified for item in caps_by_source.values()),
    )
    # ...but what the boxes come up TICKED as is a different question, and the
    # intersection answers it wrongly. Adding Codex to a machine where Claude
    # Code is already set up makes every `all()` false, so PRESERVE preserves
    # nothing and the menu opens empty -- which the apply path reads, per agent,
    # as "remove the CLI + MCP plugin" and "turn Session capture off" for the
    # agent that HAS them. Preselect from the union: what this device already does.
    union_enabled = {
        capability: any(item.enabled()[capability] for item in caps_by_source.values())
        for capability in wizard.Capability
    }
    return aggregate, wizard.resolve_selection(
        aggregate,
        tracking=tracking,
        capture=capture,
        auto_update=auto_update,
        agent_rules=agent_rules,
        configured=configured,
        current_override=union_enabled,
    )


def _needs_for_this_run(needs: list[str], *, yes: bool) -> list[str]:
    """The grants this run asks for. A run nobody is watching drops a lone MCP
    grant (`setup.headless_needs`); a `--json` run does not, because the
    program reading it shows the approval link (`device_prompt`) to a person."""
    from probe.core import events as json_events
    from probe.cli import wizard as wizard

    if (not yes and wizard.interactive()) or json_events.enabled():
        return needs
    return wizard.headless_needs(needs)


@dataclass
class _InstallationCompletion:
    """Settle one installation only after every selected agent has finished.

    Capability registration also adopts credentials, so intermediate agents
    still report. Their snapshot stays unknown until the final apply succeeds;
    an earlier unverified result keeps the whole installation unsettled.
    """

    remaining: int
    settled: bool = True

    #: Every agent's state so far: the settling report covers the whole run,
    #: so an install whose last agent has no capture does not report it removed.
    passes: list = dataclasses.field(default_factory=list)
    #: Probe was installed on this device before this run
    #: (`_probe_already_installed`). With `added`, it is how
    #: `wizard.install_settled` tells a NEW agent on a known machine from a
    #: first install, which the server already announces once per machine.
    was_configured: bool = False
    #: Agents whose tracking or capture plugin this run installed (absent before,
    #: present after), in the order they finished.
    added: list = dataclasses.field(default_factory=list)

    def register(self, caps, *, settings, complete: bool = True) -> list[str]:
        self.remaining -= 1
        self.settled = self.settled and complete
        settling = self.settled and self.remaining == 0
        # The earlier agents finished exactly when the install settles: until
        # then every pass, theirs included, reports `unknown`.
        earlier = tuple((state, settling) for state in self.passes)
        self.passes.append(caps)
        return _register_local_capabilities(
            caps, settings=settings, complete=settling, alongside=earlier
        )


def _probe_already_installed(snapshots) -> bool:
    """Whether Probe was set up on this device before the current run.

    Not `Capabilities.configured`: that counts the sign-in, and a fresh
    machine is signed in before the wizard's menu even opens, so every first
    install read as an agent added to a set-up machine. Only what an install
    leaves behind counts -- a plugin, the agent rules, auto-update someone
    turned on (the managed CLI's default is on before any install:
    `auto_update_chosen`) -- and auto-update is device-wide, which is how
    `--agent codex` alone still sees a machine Claude Code was set up on."""
    return any(
        caps.tracking_plugin_installed
        or caps.capture_plugin_installed
        or caps.legacy_capture_plugin_installed
        or caps.agent_rules_installed
        or caps.auto_update_chosen
        for caps in snapshots
    )


def _register_local_capabilities(
    caps, *, settings=None, complete: bool = True, alongside=(), reports_removals: bool = True
) -> list[str]:
    """Lazy wrapper so ordinary CLI startup never imports setup-only SDK work."""
    from probe.cli.wizard.apply.client_installation import register

    return register(
        caps,
        settings=settings,
        complete=complete,
        alongside=alongside,
        reports_removals=reports_removals,
    )
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
