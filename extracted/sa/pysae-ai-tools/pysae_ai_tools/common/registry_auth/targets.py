"""Where the GitLab registry credential applies — derived, never hardcoded.

The npm scope and the registry hosts come from the repo's own identity: the
``origin`` remote gives the GitLab host and the project path, whose top-level
namespace is the owner holding the private packages. That is the same
derivation ``internal detect-context`` performs, reproduced here because
``common/`` cannot import a command group — and because a credential posed in
the *user's* configuration must resolve even when no group CLI is reachable.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from ..git import get_remote_url
from ..glab.runner import DEFAULT_HOST, resolve_current_project, run_glab

_SSH_REMOTE = re.compile(r"^(?:ssh://)?(?:[^@/]+@)?(?P<host>[^:/]+)[:/](?P<path>.+?)/?$")
_HTTP_REMOTE = re.compile(r"^https?://(?:[^@/]+@)?(?P<host>[^/:]+)(?::\d+)?/(?P<path>.+?)/?$")


@dataclass(frozen=True)
class RegistryTargets:
    """The GitLab host and owner every ecosystem's configuration is keyed on.

    ``owner`` is empty when the credential is applied outside a GitLab clone.
    The Python and container registries only need the host, so they stay
    configurable; the npm scope mapping does not and is skipped.
    """

    host: str
    owner: str = ""

    @property
    def api_root(self) -> str:
        return f"https://{self.host}/api/v4"

    @property
    def container_registry(self) -> str:
        """Container registry host — GitLab's ``registry.<host>`` convention."""
        return f"registry.{self.host}"

    @property
    def npm_registry(self) -> str:
        """Instance-wide npm registry endpoint (scoped packages resolve under it)."""
        return f"https://{self.host}/api/v4/packages/npm/"

    @property
    def npm_auth_key(self) -> str:
        """``.npmrc`` host key the token is attached to — never a global setting."""
        return f"//{self.host}/api/v4/packages/npm/"

    @property
    def python_service(self) -> str:
        """Service uv stores the credential under.

        uv matches stored credentials by URL prefix, so registering the host
        root covers every GitLab PyPI index below it (project- or group-scoped)
        while leaving public indexes untouched.
        """
        return f"https://{self.host}/"


def _parse_remote(url: str) -> tuple[str, str]:
    """Split a git remote URL into ``(host, project_path)``; empty on no match."""
    cleaned = url.strip().removesuffix(".git")
    for pattern in (_HTTP_REMOTE, _SSH_REMOTE):
        match = pattern.match(cleaned)
        if match:
            return match.group("host"), match.group("path")
    return "", ""


def detect_targets(repo_dir: Path | None = None) -> RegistryTargets:
    """Resolve the targets from the repo in ``repo_dir`` (default: the cwd).

    Falls back to ``glab`` for each part the remote does not yield, then to the
    default GitLab host — so the Python and container registries stay
    configurable even from outside a clone.

    Never raises. This runs while installing tools, on machines where neither
    ``git`` nor ``glab`` is guaranteed to exist yet; failing here would take down
    the tool being configured.
    """
    host, project_path = "", ""

    try:
        remote = get_remote_url(repo_dir or Path.cwd())
    except OSError:
        remote = None
    if remote:
        host, project_path = _parse_remote(remote)

    if not project_path:
        try:
            _, project_path = resolve_current_project()
        except OSError:
            project_path = ""

    if not host:
        try:
            res = run_glab("config", "get", "host", timeout=10)
            host = res.stdout if res.ok else ""
        except OSError:
            host = ""

    owner = project_path.split("/", 1)[0] if project_path else ""
    return RegistryTargets(host=host or DEFAULT_HOST, owner=owner)
