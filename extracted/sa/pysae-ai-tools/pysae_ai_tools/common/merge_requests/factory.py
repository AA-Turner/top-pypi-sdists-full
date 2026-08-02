"""Resolve the right :class:`MergeRequestProvider` from a platform or repo URL.

Pure wiring, mirror of :mod:`pysae_ai_tools.common.issue_tracking.factory`: it
takes an already-resolved :class:`Platform` (or a URL to derive one from) plus
the repo coordinates, and returns a provider. It deliberately does **not** import
``detect_context`` — the caller (the CLI layer) reads the context and passes the
platform in, keeping ``common`` free of any dependency on a command group.
"""

from ..issue_tracking.context import RepoContext
from ..issue_tracking.platform import Platform, platform_for_url
from .github_provider import GithubMergeRequestProvider
from .gitlab_provider import GitlabMergeRequestProvider
from .provider import MergeRequestProvider


def provider_for(platform: Platform, ctx: RepoContext) -> MergeRequestProvider:
    """Build the provider for an explicit platform."""
    if platform is Platform.GITHUB:
        return GithubMergeRequestProvider(ctx)
    return GitlabMergeRequestProvider(ctx)


def provider_for_url(url: str, ctx: RepoContext) -> MergeRequestProvider:
    """Build the provider by deriving the platform from a repo URL/host."""
    return provider_for(platform_for_url(url), ctx)
