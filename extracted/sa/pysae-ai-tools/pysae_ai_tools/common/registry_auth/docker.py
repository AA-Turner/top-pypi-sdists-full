"""Pose the credential for the GitLab container registry.

The token goes in through ``docker login --password-stdin``: never on the
command line, never in a log. State is read from ``~/.docker/config.json``,
which is also what ``tools status docker --json`` reports.
"""

import subprocess

from ..docker import registry_logins
from ..glab.runner import glab_api
from .consumer import ApplyResult, ConsumerState, RegistryConsumer
from .targets import RegistryTargets

# Fallback login name. GitLab accepts a PAT with any non-empty username; the
# real one is preferred when reachable so the login is recognisable in
# ~/.docker/config.json, and this matches what `ci run-local` already does.
_FALLBACK_USERNAME = "oauth2"


def _gitlab_username() -> str:
    data = glab_api("user")
    if isinstance(data, dict) and isinstance(data.get("username"), str):
        return str(data["username"])
    return ""


class DockerRegistryConsumer(RegistryConsumer):
    name = "docker"

    def state(self, targets: RegistryTargets) -> ConsumerState:
        logins = registry_logins()
        registry = targets.container_registry
        stored = logins.get(registry)
        return ConsumerState(
            name=self.name,
            configured=bool(stored),
            locations=(registry,) if stored else (),
            detail=stored or "",
        )

    def apply(self, token: str, targets: RegistryTargets) -> ApplyResult:
        registry = targets.container_registry
        username = _gitlab_username() or _FALLBACK_USERNAME
        try:
            result = subprocess.run(
                ["docker", "login", registry, "-u", username, "--password-stdin"],
                input=token,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=60,
            )
        except FileNotFoundError:
            return ApplyResult(error="docker is not installed or not in PATH")
        except subprocess.TimeoutExpired:
            return ApplyResult(error=f"docker login to {registry} timed out")
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip().splitlines()
            return ApplyResult(error=f"docker login to {registry} failed: {detail[-1] if detail else 'unknown error'}")
        # `docker login` is idempotent and gives no "already logged in" signal,
        # so a success always counts as a change.
        return ApplyResult(changed=True, locations=(registry,))

    def remove(self, targets: RegistryTargets) -> tuple[str, ...]:
        registry = targets.container_registry
        if registry not in registry_logins():
            return ()
        try:
            result = subprocess.run(
                ["docker", "logout", registry],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=30,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return ()
        return (registry,) if result.returncode == 0 else ()


consumer = DockerRegistryConsumer()
