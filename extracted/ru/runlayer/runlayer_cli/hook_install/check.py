"""Non-mutating hook-config verifier used by ``aiwatch setup hooks check`` (see cli/AGENTS.md)."""

from __future__ import annotations

import enum
import platform
from dataclasses import dataclass

import yaml

from runlayer_cli.hook_install.clients import (
    CONSOLE_HOME_CLIENTS,
    Client,
    _FLAT_HOOK_COMMAND_FIELDS,
    _RUNLAYER_SCRIPT_NAMES,  # noqa: F401 — re-exported for tests
    _cline_cli_script_paths,
    _hook_entry_command,
    _is_runlayer_cline_script,
    _is_runlayer_command,
    _is_runlayer_flat_hook,
    _unsafe_windows_mdm_reason,
    client_config_dir,
    config_path_for,
    expected_event_names,
    hook_command_for_client,
    iter_supported_clients,
    powershell_hook_command,
)
from runlayer_cli.hook_install.paths import (
    InstallScope,
    ManagedPathError,
    resolve_hook_command,
)
from runlayer_cli.hook_install.presence import client_is_installed
from runlayer_cli.hook_install.safe_fs import (
    console_home_anchor,
    is_unsafe_windows_mdm_path,
    maybe_safe_read_text,
    path_has_link_or_reparse_point,
)
from runlayer_cli.tolerant_json import read_dict
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


_NESTED_HOOK_CLIENTS = frozenset(
    {
        Client.CLAUDE_CODE,
        Client.CODEX,
        Client.GOOSE,
        Client.QWEN_CODE,
        Client.GEMINI_CLI,
        Client.GROK_CLI,
        Client.DEVIN_CLI,
    }
)


def check_client(
    client: Client,
    *,
    scope: InstallScope = InstallScope.MDM,
    expected_hook_command: str | None = None,
    include_pipeline: bool | None = None,
    metadata_only: bool = False,
) -> InstalledClient:
    """Inspect one client's hook config and report compliance.

    ``include_pipeline`` controls which event names must be present for an
    ``OK`` verdict; when ``None`` it is resolved from the MDM ``Sessions`` key
    (same logic the install path uses), so a partial enforcement-only install
    where the full event set is expected is reported as ``DRIFTED``.
    """
    if include_pipeline is None:
        include_pipeline = resolve_include_pipeline(False)
    if not client_is_installed(client, scope=scope):
        return InstalledClient(client, ClientStatus.CLIENT_NOT_INSTALLED)

    config_path = config_path_for(client, scope)
    if client in CONSOLE_HOME_CLIENTS and is_unsafe_windows_mdm_path(
        config_path,
        mdm=scope == InstallScope.MDM,
        path_check=path_has_link_or_reparse_point,
    ):
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            _unsafe_windows_mdm_reason(client),
        )

    if client == Client.CLINE_CLI:
        return _check_script_dir_client(
            client,
            scope=scope,
            expected_hook_command=expected_hook_command,
            include_pipeline=include_pipeline,
            metadata_only=metadata_only,
        )

    # ENG-3217: the MDM drift check runs as root, and VS Code / Claude Code /
    # Hermes read their config from the console user's home — a user-controlled
    # dir. Read link-safe (O_NOFOLLOW from the trusted anchor) so a planted
    # symlink can't make root read an arbitrary file. ``home is None`` (user
    # scope, Cursor / Codex enterprise dirs, or Windows after the reparse-point
    # preflight above) falls through to a plain read.
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

    if client == Client.QWEN_CODE and existing.get("disableAllHooks") is True:
        return InstalledClient(client, ClientStatus.DRIFTED, "disableAllHooks is true")

    hooks_config = existing.get("hooksConfig")
    if (
        client == Client.GEMINI_CLI
        and isinstance(hooks_config, dict)
        and hooks_config.get("enabled") is False
    ):
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            "hooksConfig.enabled is false",
        )

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

    if (
        client == Client.CLAUDE_CODE
        and platform.system() == "Windows"
        and any(field != "exec" for _, field, _ in runlayer_entries)
    ):
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            "Claude Code hook does not use command + args exec form",
        )

    if client == Client.GITHUB_COPILOT_CLI and _copilot_cli_has_invalid_hook_shape(
        hooks_section
    ):
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            "Runlayer hook entry lacks bash/powershell commands",
        )

    if expected_cmd is not None and not all(
        _commands_match(cmd, _expected_command_for_field(field, expected_cmd))
        for _, field, cmd in runlayer_entries
    ):
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            f"hook command does not match {expected_cmd!r}",
        )

    found_event_names = {event_name for event_name, _, _ in runlayer_entries}
    expected_events = expected_event_names(
        client,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    missing_events = expected_events - found_event_names
    if missing_events:
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            f"missing event hooks: {', '.join(sorted(missing_events))}",
        )
    unexpected_events = found_event_names - expected_events if metadata_only else set()
    if unexpected_events:
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            f"unexpected event hooks: {', '.join(sorted(unexpected_events))}",
        )

    return InstalledClient(client, ClientStatus.OK)


def check_all(
    *,
    scope: InstallScope = InstallScope.MDM,
    expected_hook_command: str | None = None,
    include_pipeline: bool | None = None,
    metadata_only: bool = False,
) -> list[InstalledClient]:
    results = []
    for client in iter_supported_clients():
        try:
            result = check_client(
                client,
                scope=scope,
                expected_hook_command=expected_hook_command,
                include_pipeline=include_pipeline,
                metadata_only=metadata_only,
            )
        except ManagedPathError as exc:
            result = InstalledClient(
                client,
                ClientStatus.DRIFTED,
                f"configuration invalid: {exc}",
            )
        results.append(result)
    return results


def _check_script_dir_client(
    client: Client,
    *,
    scope: InstallScope,
    expected_hook_command: str | None,
    include_pipeline: bool,
    metadata_only: bool,
) -> InstalledClient:
    """Verify a dir-of-scripts client (Cline) by reading each event script.

    Cline has no hooks config file — each registered event is its own executable
    file — so the JSON/YAML ``hooks``-dict walk does not apply. A script counts
    as ours only when it is Runlayer-owned; third-party scripts sharing an event
    name are reported as missing rather than silently accepted.
    """
    config_dir = client_config_dir(client, scope)
    home = (
        console_home_anchor(config_dir, mdm=True)
        if scope == InstallScope.MDM and client in CONSOLE_HOME_CLIENTS
        else None
    )
    if not config_dir.is_dir():
        return InstalledClient(
            client, ClientStatus.MISSING, f"no {config_dir.name} directory"
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

    expected_events = expected_event_names(
        client,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    found: set[str] = set()
    drifted: list[str] = []
    for event_name in expected_events:
        for path in _cline_cli_script_paths(config_dir, event_name):
            text = maybe_safe_read_text(path, home=home)
            if text is None or not _is_runlayer_cline_script(text):
                continue
            found.add(event_name)
            if expected_cmd is not None and not any(
                _commands_match(
                    line.removeprefix("exec ").removeprefix("& ").strip(),
                    expected_cmd,
                )
                for line in text.splitlines()
                if _is_runlayer_command(line)
            ):
                drifted.append(event_name)
            break

    if not found:
        return InstalledClient(client, ClientStatus.MISSING, "no Runlayer hook scripts")
    if drifted:
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            f"hook command does not match {expected_cmd!r}",
        )

    missing_events = expected_events - found
    if missing_events:
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            f"missing event hooks: {', '.join(sorted(missing_events))}",
        )
    if metadata_only:
        extra_events = (
            expected_event_names(client, include_pipeline=True) - expected_events
        )
        for event_name in extra_events:
            for path in _cline_cli_script_paths(config_dir, event_name):
                text = maybe_safe_read_text(path, home=home)
                if text is not None and _is_runlayer_cline_script(text):
                    return InstalledClient(
                        client,
                        ClientStatus.DRIFTED,
                        f"unexpected event hooks: {event_name}",
                    )
    return InstalledClient(client, ClientStatus.OK)


def _check_script_dir_absent(
    client: Client,
    *,
    scope: InstallScope,
) -> InstalledClient:
    """Report OK only when no Runlayer-owned Cline hook scripts remain."""
    config_dir = client_config_dir(client, scope)
    if not config_dir.is_dir():
        return InstalledClient(client, ClientStatus.OK)
    home = (
        console_home_anchor(config_dir, mdm=True)
        if scope == InstallScope.MDM and client in CONSOLE_HOME_CLIENTS
        else None
    )
    all_events = expected_event_names(client, include_pipeline=True)
    for event_name in all_events:
        for path in _cline_cli_script_paths(config_dir, event_name):
            text = maybe_safe_read_text(path, home=home)
            if text is not None and _is_runlayer_cline_script(text):
                return InstalledClient(
                    client, ClientStatus.DRIFTED, "Runlayer hook scripts present"
                )
    return InstalledClient(client, ClientStatus.OK)


def check_absent_client(
    client: Client,
    *,
    scope: InstallScope = InstallScope.MDM,
) -> InstalledClient:
    """Report OK only when no Runlayer hook entries remain for *client*."""
    config_path = config_path_for(client, scope)
    if client in CONSOLE_HOME_CLIENTS and is_unsafe_windows_mdm_path(
        config_path,
        mdm=scope == InstallScope.MDM,
        path_check=path_has_link_or_reparse_point,
    ):
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            _unsafe_windows_mdm_reason(client),
        )

    if client == Client.CLINE_CLI:
        return _check_script_dir_absent(client, scope=scope)
    if scope == InstallScope.USER:
        user_dir = client_config_dir(client, InstallScope.USER)
        if not user_dir.exists():
            return InstalledClient(client, ClientStatus.OK)

    home = (
        console_home_anchor(config_path.parent, mdm=True)
        if scope == InstallScope.MDM and client in CONSOLE_HOME_CLIENTS
        else None
    )
    config_text = maybe_safe_read_text(config_path, home=home)
    if config_text is None:
        return InstalledClient(client, ClientStatus.OK)

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

    runlayer_entries = list(_iter_runlayer_hooks(client, hooks_section))
    if runlayer_entries:
        return InstalledClient(
            client,
            ClientStatus.DRIFTED,
            "Runlayer hook entries present",
        )
    return InstalledClient(client, ClientStatus.OK)


def check_absent_all(
    *,
    scope: InstallScope = InstallScope.MDM,
) -> list[InstalledClient]:
    results = []
    for client in iter_supported_clients():
        try:
            result = check_absent_client(client, scope=scope)
        except ManagedPathError as exc:
            result = InstalledClient(
                client,
                ClientStatus.DRIFTED,
                f"configuration invalid: {exc}",
            )
        results.append(result)
    return results


def _copilot_cli_has_invalid_hook_shape(hooks_section: dict) -> bool:
    for hook_list in hooks_section.values():
        if not isinstance(hook_list, list):
            continue
        for entry in hook_list:
            if not isinstance(entry, dict) or not _is_runlayer_flat_hook(entry):
                continue
            if not all(
                isinstance(entry.get(field), str) and _is_runlayer_command(entry[field])
                for field in ("bash", "powershell")
            ):
                return True
    return False


def _iter_runlayer_hooks(client: Client, hooks_section: dict):
    """Yield ``(event_name, field, command)`` for every Runlayer hook entry.

    Cursor/VS Code/Hermes store commands directly on each event entry;
    Claude Code/Codex nest it under an inner ``hooks`` list; Copilot CLI
    carries per-shell ``bash``/``powershell`` keys. Both the command-drift
    check and the event-coverage check walk the same shape, so they share
    this single walker. ``field`` names the key the command came from so the
    drift check can hold ``powershell`` to its call-operator form and Windows
    Claude Code to its ``exec`` command + args form.
    """
    nested = client in _NESTED_HOOK_CLIENTS
    command_fields = (
        _FLAT_HOOK_COMMAND_FIELDS
        if client == Client.GITHUB_COPILOT_CLI
        else ("command",)
    )
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
                for field in command_fields:
                    cmd = (
                        _hook_entry_command(candidate)
                        if field == "command"
                        else candidate.get(field, "")
                    )
                    if isinstance(cmd, str) and _is_runlayer_command(cmd):
                        entry_field = (
                            "exec"
                            if field == "command"
                            and isinstance(candidate.get("args"), list)
                            and all(isinstance(arg, str) for arg in candidate["args"])
                            else field
                        )
                        yield event_name, entry_field, cmd


def _expected_command_for_field(field: str, expected_cmd: str) -> str:
    """Expected form per hook field: the ``powershell`` field carries the
    call-operator form; ``command``/``bash``/``exec`` carry the plain form.
    Strict — a stale un-wrapped ``powershell`` field must read as drift."""
    result = (
        powershell_hook_command(expected_cmd) if field == "powershell" else expected_cmd
    )
    return result


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
