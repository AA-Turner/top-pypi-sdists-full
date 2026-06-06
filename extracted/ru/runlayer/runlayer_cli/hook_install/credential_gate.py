"""Strict-ordering credential gate shared by ``aiwatch setup`` + ``aiwatch bootstrap``.

Both commands refuse to wire AI clients at the hook binary until enrollment
has populated either a per-process keychain secret or (in MDM scope) the
console user's enrollment marker file. See cli/AGENTS.md.
"""

from __future__ import annotations

from runlayer_cli.config import Config
from runlayer_cli.hook_install.console_user import (
    find_console_user_home,
    has_enrolled_credential_for_host,
)
from runlayer_cli.hook_install.paths import InstallScope


def credential_present(
    config: Config, host: str, scope: InstallScope
) -> tuple[bool, str]:
    """Returns ``(present, human-readable detail)``.

    ``present`` is True when either the current process can read a per-host
    secret, or (MDM scope only) the console user has dropped an enrollment
    marker for *host*. The marker is empty so root can ``stat()`` it without
    keychain access.
    """
    if config.get_secret_for_host(host):
        return True, "current process credential"

    if scope == InstallScope.USER:
        return False, "no credential for current user"

    console_home = find_console_user_home()
    if console_home is None:
        return False, "no console user detected"
    if has_enrolled_credential_for_host(console_home, host):
        return True, f"console user enrolled ({console_home})"
    return False, f"console user {console_home} has not enrolled"
