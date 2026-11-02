"""is pi's package new enough to switch profile or honour tracking-off."""

from __future__ import annotations
from dataclasses import dataclass
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.shared.harness.harnesses import pi as pi_config
from probe.cli.wizard.state.capture_credentials import capture_token_sources


@dataclass
class _Ready:
    ok: bool
    lines: list[str]


def daemon_package_ready(source: str) -> _Ready:
    """A settings-entry daemon profile's package (pi's) is new enough to run the
    daemon profile (`pi_config.DAEMON_MIN_PACKAGE_VERSION`), updating it first
    (`pi update <source>`) when it is not. An older extension ignores the
    profile and would connect the Probe MCP in a daemon session.

    The wizard asks this BEFORE pairing (`pair_capture`): pairing mints the
    agent's own capture token, and a switch that then stopped here would leave
    the agent capturing on agent, which it did not do before.
    """
    from probe.shared.harness.harnesses import pi as pi_config

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
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
