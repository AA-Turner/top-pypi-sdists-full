from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.factory import resolve_provider_target
from agentic_devtools.epic_tree.errors import ConfigError


def _write_platform_config(tmp_path, platform: dict) -> None:
    config_dir = tmp_path / ".github"
    config_dir.mkdir(exist_ok=True)
    (config_dir / "agdt-config.json").write_text(json.dumps({"platform": platform}), encoding="utf-8")


def test_resolve_provider_target_reads_github_coordinates_without_constructing_provider(tmp_path) -> None:
    _write_platform_config(tmp_path, {"github": {"repo_owner": "Owner", "repo_name": "Repo"}})

    assert resolve_provider_target(tmp_path, "github") == "Owner/Repo"


def test_resolve_provider_target_prefers_github_repo_slug(tmp_path) -> None:
    _write_platform_config(tmp_path, {"github": {"repo": " owner/repo ", "repo_owner": "other", "repo_name": "repo"}})

    assert resolve_provider_target(tmp_path, "github") == "owner/repo"


def test_resolve_provider_target_rejects_missing_github_coordinates(tmp_path) -> None:
    _write_platform_config(tmp_path, {"github": {}})

    with pytest.raises(ConfigError, match="repository coordinates"):
        resolve_provider_target(tmp_path, "github")


def test_resolve_provider_target_reads_jira_coordinates_without_authentication(tmp_path) -> None:
    _write_platform_config(
        tmp_path,
        {"jira": {"project_key": " PROJ ", "base_url": " https://jira.example.com/path/ "}},
    )
    with patch.dict(os.environ, {}, clear=True):
        assert resolve_provider_target(tmp_path, "jira") == "https://jira.example.com/path/PROJ"


def test_resolve_provider_target_uses_jira_base_url_environment_fallback(tmp_path) -> None:
    _write_platform_config(tmp_path, {"jira": {"project_key": "PROJ"}})

    with patch.dict(os.environ, {"JIRA_BASE_URL": " https://jira.example.com/ "}, clear=True):
        assert resolve_provider_target(tmp_path, "jira") == "https://jira.example.com/PROJ"


def test_resolve_provider_target_rejects_missing_jira_project_key(tmp_path) -> None:
    _write_platform_config(tmp_path, {"jira": {"base_url": "https://jira.example.com"}})

    with pytest.raises(ConfigError, match="project_key"):
        resolve_provider_target(tmp_path, "jira")


def test_resolve_provider_target_rejects_missing_jira_base_url(tmp_path) -> None:
    _write_platform_config(tmp_path, {"jira": {"project_key": "PROJ"}})

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ConfigError, match="base URL"):
            resolve_provider_target(tmp_path, "jira")


def test_resolve_provider_target_rejects_unsupported_provider(tmp_path) -> None:
    _write_platform_config(tmp_path, {})

    with pytest.raises(ConfigError, match="unsupported adapter"):
        resolve_provider_target(tmp_path, "azure")
