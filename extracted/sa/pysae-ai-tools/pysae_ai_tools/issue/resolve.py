"""Wire ``detect-context`` (plus an optional ``--project``) to the provider factory.

This is the CLI-layer seam the layering rule mandates: ``detect_context`` lives
in ``internal`` and the factory in ``common`` — neither may import the other, so
the ``issue`` group reads the context here and hands the resolved platform to the
factory. ``--project`` targets another repo, inheriting the current host (and, for
a bare name, the current owner) unless a full URL overrides everything.
"""

import json
import re
import sys
from typing import Any

import typer

from ..common.issue_tracking.context import RepoContext
from ..common.issue_tracking.factory import provider_for
from ..common.issue_tracking.platform import Platform, host_of, platform_for_url
from ..common.issue_tracking.provider import IssueTrackingProvider
from ..internal.detect_context.detect import Context, DetectArgs, detect

_PLATFORMS = {p.value for p in Platform}
# Captures (host, path) from a URL, scp-like SSH, or ``host/path`` form.
_REMOTE = re.compile(r"(?:https?://|ssh://)?(?:[^@/]+@)?([^/:]+)[:/](.+?)(?:\.git)?/?$")


def _looks_like_url(value: str) -> bool:
    """True when ``value`` carries its own host (URL, SSH remote, or ``host.tld/path``)."""
    match = _REMOTE.match(value)
    if match is None:
        return False
    return "." in match.group(1) or "://" in value or "@" in value


def _explicit_repo(value: str) -> tuple[Platform, RepoContext]:
    match = _REMOTE.match(value)
    assert match is not None
    host, path = match.group(1), match.group(2)
    url = value if "://" in value else f"https://{host}/{path}"
    owner = path.split("/", 1)[0] if "/" in path else ""
    return platform_for_url(url), RepoContext(project=path, owner=owner, url=url)


def _project_from_context(value: str, ctx: Context) -> tuple[Platform, RepoContext]:
    """Resolve ``--project`` against the current context.

    A full URL / host form is taken verbatim (any host, any owner). Anything else
    is a path **relative to the current owner**, on the current host — so ``op``
    becomes ``pysae/op`` and the subgroup path ``infra/infra-cluster`` becomes
    ``pysae/infra/infra-cluster``. A value already starting with the current owner
    is left as-is (not double-prefixed).
    """
    value = value.strip()
    if _looks_like_url(value):
        return _explicit_repo(value)
    if not ctx.owner:
        typer.echo("cannot resolve a relative project outside a repo; pass a full URL", err=True)
        raise typer.Exit(code=1)
    base_host = host_of(ctx.project_url) or "gitlab.com"
    path = value.strip("/")
    if path.split("/", 1)[0] != ctx.owner:
        path = f"{ctx.owner}/{path}"
    url = f"https://{base_host}/{path}"
    return platform_for_url(url), RepoContext(project=path, owner=path.split("/", 1)[0], url=url)


def resolve_provider(refs: list[str] | None = None, project: str | None = None) -> IssueTrackingProvider:
    """Build the provider for the target repo.

    Detection runs in ``local`` mode (git remote, no API calls). With ``project``
    set, target that repo instead — inheriting the current host, and the owner too
    for a bare name (see :func:`_project_from_context`).
    """
    ctx = detect(DetectArgs(refs=list(refs or []), local=True))
    if project:
        platform, repo = _project_from_context(project, ctx)
        return provider_for(platform, repo)
    if not ctx.project_path and not ctx.project_id:
        typer.echo("no repository detected in the current directory (use --project to target one)", err=True)
        raise typer.Exit(code=1)
    platform = Platform(ctx.issue_provider) if ctx.issue_provider in _PLATFORMS else Platform.GITLAB
    repo = RepoContext(project=ctx.project_path or ctx.project_id, owner=ctx.owner, url=ctx.project_url)
    return provider_for(platform, repo)


def print_json(data: Any) -> None:
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
