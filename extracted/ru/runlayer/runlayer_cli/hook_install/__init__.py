"""Slim stdlib-only hook-install writers + checkers (see cli/AGENTS.md)."""

from runlayer_cli.hook_install.artifact_paths import (
    runlayer_written_hook_artifact_paths,
)
from runlayer_cli.hook_install.check import (
    ClientStatus,
    InstalledClient,
    check_absent_all,
    check_absent_client,
    check_all,
    check_client,
)
from runlayer_cli.hook_install.clients import (
    Client,
    InstallResult,
    UninstallResult,
    client_config_dir,
    install_client,
    iter_supported_clients,
    uninstall_client,
)
from runlayer_cli.hook_install.console_user import (
    find_console_user_home,
    has_enrolled_credential_for_host,
)
from runlayer_cli.hook_install.credential_gate import credential_present
from runlayer_cli.hook_install.paths import (
    InstallScope,
    ManagedPathError,
    resolve_hook_command,
)

__all__ = [
    "Client",
    "ClientStatus",
    "InstallResult",
    "InstallScope",
    "InstalledClient",
    "ManagedPathError",
    "UninstallResult",
    "check_absent_all",
    "check_absent_client",
    "check_all",
    "check_client",
    "client_config_dir",
    "credential_present",
    "find_console_user_home",
    "has_enrolled_credential_for_host",
    "install_client",
    "iter_supported_clients",
    "resolve_hook_command",
    "runlayer_written_hook_artifact_paths",
    "uninstall_client",
]
