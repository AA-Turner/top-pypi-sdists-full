"""Tests for ``scaffold_tasks_command``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit import scaffold_tasks
from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature, FeatureResolutionError


def test_scaffold_tasks_command_json_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42-x", branch="42-x", has_git=True)
    active.feature_dir.mkdir(parents=True)
    (active.feature_dir / "plan.md").write_text("# plan\n", encoding="utf-8")
    monkeypatch.setattr(scaffold_tasks, "_resolve_active_feature_from_args", lambda *_args, **_kwargs: active)
    monkeypatch.setattr(scaffold_tasks, "is_dry_run", lambda: False)
    monkeypatch.setattr(
        scaffold_tasks, "prepare_tasks", lambda active_value, dry_run: active_value.feature_dir / "tasks.md"
    )
    with patch("builtins.print") as print_mock:
        scaffold_tasks.scaffold_tasks_command(["--json", "--hierarchy-level", "feature"])
    assert '"HIERARCHY_LEVEL": "feature"' in print_mock.call_args[0][0]


def test_scaffold_tasks_command_requires_plan_for_feature_level(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42-x", branch="42-x", has_git=True)
    monkeypatch.setattr(scaffold_tasks, "_resolve_active_feature_from_args", lambda *_args, **_kwargs: active)
    with pytest.raises(SystemExit):
        scaffold_tasks.scaffold_tasks_command(["--hierarchy-level", "feature"])


def test_scaffold_tasks_command_rejects_symlinked_feature_plan(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42-x", branch="42-x", has_git=True)
    active.feature_dir.mkdir(parents=True)
    monkeypatch.setattr(scaffold_tasks, "_resolve_active_feature_from_args", lambda *_args, **_kwargs: active)
    with patch.object(Path, "is_symlink", return_value=True), pytest.raises(SystemExit):
        scaffold_tasks.scaffold_tasks_command(["--hierarchy-level", "feature"])


def test_scaffold_tasks_command_error_on_resolution_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        scaffold_tasks,
        "_resolve_active_feature_from_args",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(FeatureResolutionError("bad")),
    )
    with pytest.raises(SystemExit):
        scaffold_tasks.scaffold_tasks_command([])


def test_scaffold_tasks_command_accepts_epic_hierarchy_level(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    active = ActiveFeature(repo_root=tmp_path, feature_dir=tmp_path / "specs" / "1-epic", branch="1-epic", has_git=True)
    active.feature_dir.mkdir(parents=True)
    monkeypatch.setattr(scaffold_tasks, "_resolve_active_feature_from_args", lambda *_args, **_kwargs: active)
    monkeypatch.setattr(scaffold_tasks, "is_dry_run", lambda: False)
    monkeypatch.setattr(
        scaffold_tasks, "prepare_tasks", lambda active_value, dry_run: active_value.feature_dir / "tasks.md"
    )
    with patch("builtins.print") as print_mock:
        scaffold_tasks.scaffold_tasks_command(["--json", "--hierarchy-level", "epic"])
    assert '"HIERARCHY_LEVEL": "epic"' in print_mock.call_args[0][0]
    active = ActiveFeature(
        repo_root=tmp_path, feature_dir=tmp_path / "specs" / "42-task", branch="42-task", has_git=True
    )
    active.feature_dir.mkdir(parents=True)
    parent_dir = tmp_path / "specs" / "10-parent"
    parent_dir.mkdir(parents=True, exist_ok=True)
    (parent_dir / "spec.md").write_text("# parent\n", encoding="utf-8")
    (parent_dir / "plan.md").write_text("# plan\n", encoding="utf-8")
    monkeypatch.setattr(scaffold_tasks, "_resolve_active_feature_from_args", lambda *_args, **_kwargs: active)
    monkeypatch.setattr(scaffold_tasks, "is_dry_run", lambda: True)
    monkeypatch.setattr(
        scaffold_tasks, "prepare_tasks", lambda active_value, dry_run: active_value.feature_dir / "tasks.md"
    )
    with patch("builtins.print") as print_mock:
        scaffold_tasks.scaffold_tasks_command(
            [
                "--json",
                "--hierarchy-level",
                "task",
                "--spec-context",
                str(parent_dir),
            ]
        )
    rendered = print_mock.call_args[0][0]
    assert '"SPEC_CONTEXT":' in rendered
    assert '"PARENT_PLAN_CONTEXT":' in rendered
    assert '"DRY_RUN": true' in rendered


def test_scaffold_tasks_command_rejects_spec_context_for_epic_level(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(SystemExit):
        scaffold_tasks.scaffold_tasks_command(
            ["--hierarchy-level", "epic", "--spec-context", str(tmp_path / "specs" / "10")]
        )


def test_scaffold_tasks_command_rejects_spec_context_for_feature_level(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(SystemExit):
        scaffold_tasks.scaffold_tasks_command(
            ["--hierarchy-level", "feature", "--spec-context", str(tmp_path / "specs" / "10")]
        )
