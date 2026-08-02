"""Resolve the right :class:`IssueTrackingProvider` from a platform or repo URL.

Pure wiring: it takes an already-resolved :class:`Platform` (or a URL to derive
one from) plus the repo coordinates, and returns a provider. It deliberately
does **not** import ``detect_context`` — the caller (the CLI layer) reads the
context and passes the platform in, keeping ``common`` free of any dependency on
a command group.
"""

from .context import RepoContext
from .github_provider import GithubIssueTrackingProvider
from .gitlab_provider import GitlabIssueTrackingProvider
from .platform import Platform, platform_for_url
from .provider import IssueTrackingProvider


def provider_for(platform: Platform, ctx: RepoContext) -> IssueTrackingProvider:
    """Build the provider for an explicit platform."""
    if platform is Platform.GITHUB:
        return GithubIssueTrackingProvider(ctx)
    return GitlabIssueTrackingProvider(ctx)


def provider_for_url(url: str, ctx: RepoContext) -> IssueTrackingProvider:
    """Build the provider by deriving the platform from a repo URL/host."""
    return provider_for(platform_for_url(url), ctx)
