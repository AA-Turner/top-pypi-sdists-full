"""GitHub contribution graph gamification tool."""

from .github_client import (
    ContributionData,
    ContributionDay,
    ContributionWeek,
    GitHubAPIError,
    GitHubClient,
)
from .output import resolve_output_provider

__version__ = "0.1.0"

__all__ = [
    "GitHubClient",
    "GitHubAPIError",
    "ContributionData",
    "ContributionDay",
    "ContributionWeek",
    "resolve_output_provider",
]
