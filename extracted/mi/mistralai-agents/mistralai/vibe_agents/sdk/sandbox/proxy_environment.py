"""What a Sandbox Proxy integration runs in a sandbox, and the environment it leaves for later commands.

A sandbox driver runs `bootstrap_command` in an activity, then passes each later command through
`with_proxy_environment`. The credentials reach the sandbox only through the environment of the
bootstrap command, so they never enter Workflow history.
"""

import shlex
from collections.abc import Iterable, Sequence
from typing import Literal

from .bootstrap import SandboxBootstrapResult
from .proxy_integrations import MistralApiProxyConfig, SandboxProxyIntegration, SecretInjectionProxyConfig

# The producer contract defined by sandbox_proxy_protocol.bootstrap.secret_injection.SECRET_INJECTION_ENV_FILE.
WORKSPACE_PROXY_ENV_FILE = "/tmp/sandbox-proxy/secret-injection.env"  # noqa: S108
# The producer contract defined by sandbox_proxy_protocol.bootstrap.mistral_api.MISTRAL_API_ENV_FILE.
MISTRAL_API_PROXY_ENV_FILE = "/tmp/sandbox-proxy/mistral-api.env"  # noqa: S108


def bootstrap_command(
    integration: SandboxProxyIntegration,
    bootstrap: SandboxBootstrapResult,
    operation: Literal["setup", "renewal"],
) -> tuple[str, dict[str, str]]:
    """The command that sets up or renews ``integration`` in the sandbox, and the environment it runs with."""

    command = bootstrap.setup_command if operation == "setup" else bootstrap.renewal_command
    if isinstance(integration, MistralApiProxyConfig):
        # A Sandbox Proxy that predates the provider-written file leaves the runtime environment to the
        # consumer, so the SDK writes the same file too. set -e keeps a failed provider command from
        # being reported as a success by the write that follows it.
        write_env = write_env_file_command(MISTRAL_API_PROXY_ENV_FILE, bootstrap.runtime_env)
        return f"set -eu\n{command}\n{write_env}", {**bootstrap.setup_env, **bootstrap.runtime_env}
    return command, bootstrap.setup_env


def with_proxy_environment(integrations: Sequence[SandboxProxyIntegration], command: str) -> str:
    """``command``, after it sources the environment that each of ``integrations`` left in the sandbox."""

    sources = "".join(
        f". {shlex.quote(env_file)} || exit $?\n"
        for integration in integrations
        if (env_file := _env_file(integration)) is not None
    )
    return f"{sources}{command}"


def write_env_file_command(path: str, names: Iterable[str]) -> str:
    """A shell command that writes the named variables of its own environment to ``path``.

    The values reach the sandbox only through the environment of the command, never through its
    text, and the file is replaced in one step so that a concurrent command never reads half of it.
    """

    return f"""set -eu
_proxy_env_file={shlex.quote(path)}
_proxy_env_tmp="$_proxy_env_file.$$"
mkdir -p "$(dirname "$_proxy_env_file")"
SANDBOX_PROXY_ENV_FILE="$_proxy_env_tmp" python3 - <<'__SANDBOX_PROXY_ENV__'
import os
import pathlib
import shlex

path = pathlib.Path(os.environ["SANDBOX_PROXY_ENV_FILE"])
names = {tuple(names)!r}
os.umask(0o077)
path.write_text("".join(f"export {{name}}={{shlex.quote(os.environ[name])}}\\n" for name in names), encoding="utf-8")
path.chmod(0o600)
__SANDBOX_PROXY_ENV__
mv -f "$_proxy_env_tmp" "$_proxy_env_file"
"""


def _env_file(integration: SandboxProxyIntegration) -> str | None:
    if isinstance(integration, SecretInjectionProxyConfig):
        return WORKSPACE_PROXY_ENV_FILE
    if isinstance(integration, MistralApiProxyConfig):
        return MISTRAL_API_PROXY_ENV_FILE
    return None


__all__ = [
    "MISTRAL_API_PROXY_ENV_FILE",
    "WORKSPACE_PROXY_ENV_FILE",
    "bootstrap_command",
    "with_proxy_environment",
    "write_env_file_command",
]
