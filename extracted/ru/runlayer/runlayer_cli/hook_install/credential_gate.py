"""Strict-ordering credential gate shared by ``aiwatch setup`` + ``aiwatch bootstrap``.

Both commands refuse to wire AI clients at the hook binary until a credential
is available: a managed org API key (the single AI Watch key, sufficient for
hook auth), a per-process keychain secret, or (MDM scope only) the console
user's enrollment marker file. See cli/AGENTS.md.
"""

from __future__ import annotations

from pathlib import Path

from runlayer_cli.config import Config
from runlayer_cli.hook_install.console_user import (
    find_console_user_home,
    has_enrolled_credential_for_host,
)
from runlayer_cli.hook_install.paths import InstallScope
from runlayer_cli.mdm_config import read_managed_config


def credential_present(
    config: Config, host: str, scope: InstallScope
) -> tuple[bool, str]:
    """Returns ``(present, human-readable detail)``.

    ``present`` is True when a managed ``OrgApiKey`` is pushed (hooks
    authenticate with it directly; the backend resolves device identity from
    the attached device context), or the current process can read a per-host
    secret, or an enrollment marker for *host* exists (the current user's own
    marker in USER scope, the console user's marker in MDM scope). The marker is
    empty so root can ``stat()`` it without keychain access.

    The aiwatch runtime never reads ``~/.runlayer/config.yaml`` (see
    ``runtime.is_aiwatch_runtime`` / ``config.load_config``), so a USER-scope
    install resolves its credential proof from the keychain or the enrollment
    marker ``aiwatch enroll`` drops, never the YAML.
    """
    if read_managed_config().get("org_api_key"):
        return True, "managed org api key"

    if config.get_secret_for_host(host):
        return True, "current process credential"

    if scope == InstallScope.USER:
        if has_enrolled_credential_for_host(Path.home(), host):
            return True, "current user enrolled"
        return False, "no credential for current user"

    console_home = find_console_user_home()
    if console_home is None:
        return False, "no console user detected"
    if has_enrolled_credential_for_host(console_home, host):
        return True, f"console user enrolled ({console_home})"
    return False, f"console user {console_home} has not enrolled"
