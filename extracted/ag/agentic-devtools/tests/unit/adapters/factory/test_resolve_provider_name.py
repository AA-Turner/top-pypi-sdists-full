"""Tests for the public ``resolve_provider_name`` factory helper (FR-013).

Covers the resolution precedence and normalization contract, exercised with
both ``str`` and :class:`~pathlib.Path` values for ``repo_path``:

  1. Explicit ``provider`` argument (highest priority)
  2. ``platform.issue_adapter`` in ``.github/agdt-config.json``
  3. State key ``platform.issue_adapter``
  4. Environment variable ``AGDT_ISSUE_ADAPTER``
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.factory import resolve_provider_name
from agentic_devtools.epic_tree.errors import ConfigError


def _write_config(tmp_path: Path, adapter: str) -> None:
    config_dir = tmp_path / ".github"
    config_dir.mkdir(exist_ok=True)
    payload = json.dumps({"platform": {"issue_adapter": adapter}})
    (config_dir / "agdt-config.json").write_text(payload)


class TestResolveProviderName:
    def test_explicit_provider_takes_priority(self, tmp_path):
        _write_config(tmp_path, "jira")
        assert resolve_provider_name(str(tmp_path), provider="github") == "github"

    def test_explicit_provider_is_normalized(self, tmp_path):
        _write_config(tmp_path, "jira")
        assert resolve_provider_name(str(tmp_path), provider="  GitHub  ") == "github"

    def test_accepts_path_repo_path(self, tmp_path):
        _write_config(tmp_path, "jira")
        assert resolve_provider_name(tmp_path, provider="github") == "github"

    def test_resolves_from_config_when_no_override(self, tmp_path):
        _write_config(tmp_path, "github")
        with patch.dict(os.environ, {}, clear=True):
            assert resolve_provider_name(tmp_path) == "github"

    def test_resolves_jira_from_config(self, tmp_path):
        _write_config(tmp_path, "jira")
        with patch.dict(os.environ, {}, clear=True):
            assert resolve_provider_name(str(tmp_path)) == "jira"

    def test_resolves_from_env_when_no_config(self, tmp_path):
        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "jira"}, clear=True):
            assert resolve_provider_name(tmp_path) == "jira"

    def test_empty_override_falls_through_to_config(self, tmp_path):
        _write_config(tmp_path, "github")
        with patch.dict(os.environ, {}, clear=True):
            assert resolve_provider_name(tmp_path, provider="   ") == "github"

    def test_unrecognized_override_raises_config_error(self, tmp_path):
        with pytest.raises(ConfigError):
            resolve_provider_name(tmp_path, provider="gitlab")

    def test_non_string_override_raises_config_error(self, tmp_path):
        with pytest.raises(ConfigError):
            resolve_provider_name(tmp_path, provider=123)  # type: ignore[arg-type]
