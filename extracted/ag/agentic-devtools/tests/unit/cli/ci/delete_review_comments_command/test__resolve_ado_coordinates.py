"""Tests for delete_review_comments_command._resolve_ado_coordinates."""

from __future__ import annotations

import argparse
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.config import (
    DEFAULT_ORGANIZATION,
    DEFAULT_PROJECT,
    DEFAULT_REPOSITORY,
    AzureDevOpsConfig,
)
from agentic_devtools.cli.ci.delete_review_comments_command import _resolve_ado_coordinates

_CONFIG = "agentic_devtools.config.load_platform_config"
_FROM_STATE = "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state"


def _args(org: str | None = None, project: str | None = None, repo: str | None = None) -> argparse.Namespace:
    return argparse.Namespace(org=org, project=project, repo=repo, pr=1, author=None, execute=False)


def _state(
    org: str = DEFAULT_ORGANIZATION,
    project: str = DEFAULT_PROJECT,
    repo: str = DEFAULT_REPOSITORY,
) -> AzureDevOpsConfig:
    return AzureDevOpsConfig(organization=org, project=project, repository=repo)


class TestResolveAdoCoordinates:
    """Tests for the org/project/repo resolution chain."""

    def test_uses_explicit_args(self) -> None:
        with patch(_CONFIG, return_value={"azure_devops": {}}), patch(_FROM_STATE, return_value=_state()):
            result = _resolve_ado_coordinates(_args(org="https://dev.azure.com/o", project="P", repo="R"), "/repo")
        assert result == ("https://dev.azure.com/o", "P", "R")

    def test_falls_back_to_config_then_state(self) -> None:
        cfg = {"azure_devops": {"organization": "https://dev.azure.com/cfg", "project": "CfgProj"}}
        with patch(_CONFIG, return_value=cfg), patch(_FROM_STATE, return_value=_state(repo="state-repo")):
            result = _resolve_ado_coordinates(_args(), "/repo")
        assert result == ("https://dev.azure.com/cfg", "CfgProj", "state-repo")

    def test_missing_organization_raises(self) -> None:
        state = _state(org=DEFAULT_ORGANIZATION, project="P", repo="R")
        with patch(_CONFIG, return_value={"azure_devops": {}}), patch(_FROM_STATE, return_value=state):
            with pytest.raises(ValueError, match="organization"):
                _resolve_ado_coordinates(_args(), "/repo")

    def test_missing_project_raises(self) -> None:
        state = _state(org="https://dev.azure.com/o", project=DEFAULT_PROJECT, repo="R")
        with patch(_CONFIG, return_value={"azure_devops": {}}), patch(_FROM_STATE, return_value=state):
            with pytest.raises(ValueError, match="project"):
                _resolve_ado_coordinates(_args(), "/repo")

    def test_missing_repository_raises(self) -> None:
        state = _state(org="https://dev.azure.com/o", project="P", repo=DEFAULT_REPOSITORY)
        with patch(_CONFIG, return_value={"azure_devops": {}}), patch(_FROM_STATE, return_value=state):
            with pytest.raises(ValueError, match="repository"):
                _resolve_ado_coordinates(_args(), "/repo")
