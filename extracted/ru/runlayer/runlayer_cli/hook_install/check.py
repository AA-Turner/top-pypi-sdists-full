"""Non-mutating hook-config verifier used by ``aiwatch setup hooks check`` (see cli/AGENTS.md)."""

from __future__ import annotations

import enum
from dataclasses import dataclass

import yaml

from runlayer_cli.hook_install.clients import (
    CONSOLE_HOME_CLIENTS,
    Client,
    _RUNLAYER_SCRIPT_NAMES,  # noqa: F401 — re-exported for tests
    _is_runlayer_command,
    client_config_dir,
    config_path_for,
    expected_event_names,
    hook_command_for_client,
    iter_supported_clients,
)
from runlayer_cli.hook_install.paths import InstallScope, resolve_hook_command
from runlayer_cli.hook_install.safe_fs import (
    console_home_anchor,
    maybe_safe_read_text,
)
from runlayer_cli.hook_install.tolerant_json import read_dict
from runlayer_cli.mdm_config import resolve_include_pipeline


class ClientStatus(str, enum.Enum):
    OK = "ok"
    MISSING = "missing"
    DRIFTED = "drifted"
    CLIENT_NOT_INSTALLED = "client_not_installed"


@dataclass(frozen=True)
class InstalledClient:
    client: Client
    status: ClientStatus
    detail: str = ""


def check_client(
    client: Client,
    *,
    scope: InstallScope = InstallScope.MDM,
    expected_hook_command: str | None = None,
    include_pipeline: bool | None = None,
) -> InstalledClient:
    """Inspect one client's hook config and report compliance.

    ``include_pipeline`` controls which event names must be present for an
    ``OK`` verdict; when ``None`` it is resolved from the MDM ``Sessions`` key
    (same logic the install path uses), so a partial enforcement-only install
    where the full event set is expected is reported as ``DRIFTED``.
    """
    if include_pipeline is None:
        include_pipeline = resolve_include_pipeline(False)
    if scope == InstallScope.USER:
        user_dir = client_config_dir(client, InstallScope.USER)
        if not user_dir.exists():
            return InstalledClient(client, ClientStatus.CLIENT_NOT_INSTALLED)

    config_path = config_path_for(client, scope)

    # ENG-3217: the MDM drift check runs as root, and Claude Code / Hermes read
    # their config from the console user's home — a user-controlled dir. Read
    # link-safe (O_NOFOLLOW from the trusted anchor) so a planted symlink can't
    # make root read an arbitrary file. ``home is None`` (user scope, Cursor /
    # Codex enterprise dirs, Windows) falls through to a plain read.
    home = (
        console_home_anchor(config_path.parent, mdm=True)
        if scope == InstallScope.MDM and client in CONSOLE_HOME_CLIENTS
        else None
    )
    config_text = maybe_safe_read_text(config_path, home=home)
    if config_text is None:
        return InstalledClient(client, ClientStatus.MISSING, f"no {config_path.name}")

    try:
        if client == Client.HERMES:
            loaded = yaml.safe_load(config_text)
            existing = loaded if isinstance(loaded, dict) else {}
        else:
            existing = read_dict(config_text)
    except (ValueError, OSError, yaml.YAMLError) as exc:
        return InstalledClient(client, ClientStatus.DRIFTED, str(exc))

    hooks_section = existing.get("hooks", {})
    if not isinstance(hooks_section, dict):
        return InstalledClient(
            client, ClientStatus.DRIFTED, "hooks section is not a dict"
        )

    base_expected_cmd = (
        expected_hook_command
        if expected_hook_command is not None
        else _try_resolve_hook_command()
    )
    expected_cmd = (
        hook_command_for_client(base_expected_cmd, client)
        if base_expected_cmd is not None
        else None
    )

    runlayer_entries = list(_iter_runlayer_hooks(client, hooks_section))
    if not runlayer_entries:
        return InstalledClient(client, ClientStatus.MISSING, "no Runlayer hook entries")

    if expected_cmd is not None and not all(
        _commands_match(cmd, expected_cmd) for _, cmd in runlayer_entries
    ):
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            f"hook command does not match {expected_cmd!r}",
        )

    found_event_names = {event_name for event_name, _ in runlayer_entries}
    missing_events = (
        expected_event_names(client, include_pipeline=include_pipeline)
        - found_event_names
    )
    if missing_events:
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            f"missing event hooks: {', '.join(sorted(missing_events))}",
        )

    return InstalledClient(client, ClientStatus.OK)


def check_all(
    *,
    scope: InstallScope = InstallScope.MDM,
    expected_hook_command: str | None = None,
    include_pipeline: bool | None = None,
) -> list[InstalledClient]:
    return [
        check_client(
            c,
            scope=scope,
            expected_hook_command=expected_hook_command,
            include_pipeline=include_pipeline,
        )
        for c in iter_supported_clients()
    ]


def _iter_runlayer_hooks(client: Client, hooks_section: dict):
    """Yield ``(event_name, command)`` for every Runlayer hook entry.

    Cursor/Hermes store the command directly on each event entry; Claude
    Code/Codex nest it under an inner ``hooks`` list. Both the command-drift
    check and the event-coverage check walk the same shape, so they share this
    single walker.
    """
    nested = client not in (Client.CURSOR, Client.HERMES)
    for event_name, hook_list in hooks_section.items():
        if not isinstance(hook_list, list):
            continue
        for entry in hook_list:
            if not isinstance(entry, dict):
                continue
            if nested:
                candidates = entry.get("hooks", [])
                if not isinstance(candidates, list):
                    continue
            else:
                candidates = [entry]
            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue
                cmd = candidate.get("command", "")
                if isinstance(cmd, str) and _is_runlayer_command(cmd):
                    yield event_name, cmd


def _commands_match(found: str, expected: str) -> bool:
    """Compare hook command strings tolerating surrounding double-quotes."""
    return _strip_quotes(found) == _strip_quotes(expected)


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _try_resolve_hook_command() -> str | None:
    try:
        return resolve_hook_command()
    except FileNotFoundError:
        return None
