"""Connector implementations for spec-kitty-tracker.

SaaS-backed connectors (Linear, Jira, GitHub, GitLab) are used through
NangoProxyAdapter with host-provided transport context. Use
create_hosted_connector() to construct them for SaaS-hosted operation.
Direct construction with static credentials is supported for test,
migration, and advanced SDK use cases only; it is not the product path for
the Spec Kitty CLI.

Local/native connectors (Beads, FP) are used directly for local-first
workflows and do not require proxy transport.

InMemoryConnector is a test and reference implementation.
"""

from spec_kitty_tracker.connectors.azure_devops import (
    AzureDevOpsConnector,
    AzureDevOpsConnectorConfig,
)
from spec_kitty_tracker.connectors.beads import BeadsConnector, BeadsConnectorConfig
from spec_kitty_tracker.connectors.fp import FPConnector, FPConnectorConfig
from spec_kitty_tracker.connectors.github import GitHubConnector, GitHubConnectorConfig
from spec_kitty_tracker.connectors.gitlab import GitLabConnector, GitLabConnectorConfig
from spec_kitty_tracker.connectors.in_memory import InMemoryConnector
from spec_kitty_tracker.connectors.jira import JiraConnector, JiraConnectorConfig
from spec_kitty_tracker.connectors.linear import LinearConnector, LinearConnectorConfig

__all__ = [
    "AzureDevOpsConnector",
    "AzureDevOpsConnectorConfig",
    "BeadsConnector",
    "BeadsConnectorConfig",
    "FPConnector",
    "FPConnectorConfig",
    "GitHubConnector",
    "GitHubConnectorConfig",
    "GitLabConnector",
    "GitLabConnectorConfig",
    "InMemoryConnector",
    "JiraConnector",
    "JiraConnectorConfig",
    "LinearConnector",
    "LinearConnectorConfig",
]
