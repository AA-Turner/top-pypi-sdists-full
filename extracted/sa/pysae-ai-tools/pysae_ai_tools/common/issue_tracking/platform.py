"""Resolve the issue-tracking platform of a repository from its URL.

The platform drives which ``IssueTrackingProvider`` is selected. It is derived
purely from the repository host, so it works for every detection path (git
remote, glab, CI env): ``github.com`` maps to GitHub, everything else — an empty
value or a self-hosted GitLab included — maps to GitLab, which keeps the current
GitLab-only behaviour as the default.

This module is a leaf primitive: it depends on nothing but the stdlib so both
``internal/detect_context`` and the provider factory can consume it without
crossing a layer.
"""

import re
from enum import Enum

_SCP_SSH = re.compile(r"^[^/@]+@([^:/]+):")


class Platform(str, Enum):
    """A supported issue-tracking host platform."""

    GITLAB = "gitlab"
    GITHUB = "github"


def host_of(url: str) -> str:
    """Extract the lowercased host from a repo URL, remote, or bare host.

    Handles HTTPS (``https://gitlab.com/g/r``), scp-like SSH
    (``git@github.com:g/r.git``) and a bare host (``github.com``). Returns an
    empty string when no host can be extracted.
    """
    url = url.strip()
    if not url:
        return ""
    scp = _SCP_SSH.match(url)
    if scp:
        return scp.group(1).lower()
    host = url.split("://", 1)[1] if "://" in url else url
    host = host.split("/", 1)[0]
    host = host.split("@")[-1]
    host = host.split(":", 1)[0]
    return host.lower()


def platform_for_url(url: str) -> Platform:
    """Resolve the :class:`Platform` from a repo URL, host, or remote.

    ``github.com`` (and its subdomains) → GitHub; everything else — an empty
    value or a self-hosted GitLab included — → GitLab, the behaviour-preserving
    default.
    """
    host = host_of(url)
    if host == "github.com" or host.endswith(".github.com"):
        return Platform.GITHUB
    return Platform.GITLAB
