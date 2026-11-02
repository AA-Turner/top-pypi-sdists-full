"""Tests for delete_review_comments_command._build_provider provider dispatch."""

from __future__ import annotations

import argparse
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.ci.ado_provider import AzureDevOpsProvider
from agentic_devtools.cli.ci.delete_review_comments_command import _build_provider
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_CONFIG = "agentic_devtools.config.load_platform_config"
_FROM_STATE = "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state"


def _args(org: str | None = None, project: str | None = None, repo: str | None = None) -> argparse.Namespace:
    return argparse.Namespace(org=org, project=project, repo=repo, pr=1, author=None, execute=False)


def _placeholder_state() -> AzureDevOpsConfig:
    return AzureDevOpsConfig(
        organization="https://dev.azure.com/example-org",
        project="ExampleProject",
        repository="example-repo-name",
    )


class TestBuildProvider:
    """Tests for provider dispatch."""

    def test_github_stub_when_github_and_no_org(self) -> None:
        with patch(_CONFIG, return_value={"code_hosting": "github", "azure_devops": {}}):
            provider = _build_provider(_args(), "/repo")
        assert isinstance(provider, GitHubActionsProvider)

    def test_ado_when_explicit_org_overrides_github(self) -> None:
        cfg = {"code_hosting": "github", "azure_devops": {}}
        with patch(_CONFIG, return_value=cfg), patch(_FROM_STATE, return_value=_placeholder_state()):
            provider = _build_provider(_args(org="https://dev.azure.com/myorg", project="P", repo="R"), "/repo")
        assert isinstance(provider, AzureDevOpsProvider)

    def test_ado_when_code_hosting_not_github(self) -> None:
        cfg = {
            "code_hosting": "azure_devops",
            "azure_devops": {
                "organization": "https://dev.azure.com/o",
                "project": "P",
                "repository": "R",
            },
        }
        with patch(_CONFIG, return_value=cfg), patch(_FROM_STATE, return_value=_placeholder_state()):
            provider = _build_provider(_args(), "/repo")
        assert isinstance(provider, AzureDevOpsProvider)
