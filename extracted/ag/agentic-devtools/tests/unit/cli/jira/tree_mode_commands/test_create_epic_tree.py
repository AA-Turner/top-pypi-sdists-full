"""Tests for ``create_epic_tree`` CLI delegation (T056, issue #2118).

``create_epic_tree`` derives the repository root from
``git rev-parse --show-toplevel`` and delegates to ``run_creation_pipeline``,
discarding the returned plan to preserve its ``-> None`` contract.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import agentic_devtools.cli.jira.tree_mode_commands as tmc
from agentic_devtools.cli.jira.tree_mode_commands import create_epic_tree


class TestCreateEpicTreeDelegation:
    def test_delegates_with_resolved_repo_root(self, monkeypatch):
        run_mock = MagicMock(return_value="PLAN")
        monkeypatch.setattr(tmc, "_resolve_repo_root", lambda: Path("/repo"))
        monkeypatch.setattr(tmc, "run_creation_pipeline", run_mock)

        result = create_epic_tree("plan.json", start_from=None, provider="github", dry_run=True)

        assert result is None  # plan is discarded
        run_mock.assert_called_once_with(
            Path("/repo"),
            Path("plan.json"),
            provider="github",
            start_from=None,
            dry_run=True,
        )

    def test_defaults_forwarded(self, monkeypatch):
        run_mock = MagicMock()
        monkeypatch.setattr(tmc, "_resolve_repo_root", lambda: Path("/repo"))
        monkeypatch.setattr(tmc, "run_creation_pipeline", run_mock)

        create_epic_tree("plan.json")

        _, kwargs = run_mock.call_args
        assert kwargs == {"provider": None, "start_from": None, "dry_run": False}

    def test_repo_root_derived_before_pipeline(self, monkeypatch):
        calls: list[str] = []

        def fake_root() -> Path:
            calls.append("root")
            return Path("/repo")

        def fake_run(*args, **kwargs):
            calls.append("run")

        monkeypatch.setattr(tmc, "_resolve_repo_root", fake_root)
        monkeypatch.setattr(tmc, "run_creation_pipeline", fake_run)
        create_epic_tree("plan.json")
        assert calls == ["root", "run"]


class TestCreateEpicTreePropagation:
    def test_repo_root_failure_propagates_before_pipeline(self, monkeypatch):
        run_mock = MagicMock()

        def _raise() -> Path:
            raise tmc.PipelineValidationError("no git")

        monkeypatch.setattr(tmc, "_resolve_repo_root", _raise)
        monkeypatch.setattr(tmc, "run_creation_pipeline", run_mock)
        with pytest.raises(tmc.PipelineValidationError):
            create_epic_tree("plan.json")
        run_mock.assert_not_called()
