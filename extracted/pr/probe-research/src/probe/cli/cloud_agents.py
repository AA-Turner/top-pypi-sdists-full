"""The coding agents of registry family `cloud` (Capy), as the installer drives them.

A cloud agent is installed like any other (it is in the picker, `--agent`, the
"On this device" block), but nothing on this machine can configure it: it runs
no Probe hook and has no command or API for its own settings. So where a
hook-plugin agent's install writes a plugin, a cloud agent's prints the steps
that put Probe inside it, and its capture is a connection to the vendor's API
that this machine syncs on a timer.

Core code asks `is_cloud(source)` and reaches the agent's own module through
`module(source)`, never by name: each module provides `label`, `setup_steps`, `setup_summary`,
`can_open_add_plugin`, `open_add_plugin`, `wizard_status`, `connected_here`, `load_config`,
`ask_capture`, `apply_capture`, `capture_off`, `disconnect`, `after_sign_in`, `doctor_facts`
and `SYNC_INTERVAL_SECONDS`.
"""

from __future__ import annotations

from types import ModuleType


def sources() -> tuple[str, ...]:
    """The installable cloud agents, in registry order."""
    from probe.harness import FAMILY_CLOUD, get_registry

    return tuple(h.id for h in get_registry().installable() if h.family == FAMILY_CLOUD)


def is_cloud(source: str | None) -> bool:
    return bool(source) and source in sources()


def module(source: str) -> ModuleType:
    """The module that drives one cloud agent. KeyError for any other source."""
    from probe.cli import capy_cli

    return {capy_cli.SOURCE: capy_cli}[source]


def found_here(source: str) -> bool:
    """Whether the agent's app is on this machine (its registry `detect_paths`)."""
    from probe.harness import get_registry

    return get_registry().get(source).found_on_disk()
