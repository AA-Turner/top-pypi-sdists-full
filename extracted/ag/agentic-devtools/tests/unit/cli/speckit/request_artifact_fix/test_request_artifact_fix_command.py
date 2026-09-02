"""Tests for ``request_artifact_fix_command()`` in ``request_artifact_fix``."""

from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.request_artifact_fix import request_artifact_fix_command


def _argv(spec_dir: str = "specs/1900-task", **extra: str) -> list[str]:
    argv = [
        "--pr",
        "42",
        "--repo",
        "owner/repo",
        "--spec-dir",
        spec_dir,
        "--phase-number",
        "4",
        "--phase-name",
        "tasks",
        "--violations",
        "tasks.md: missing path",
    ]
    for key, value in extra.items():
        argv.extend([f"--{key.replace('_', '-')}", value])
    return argv


class TestRequestArtifactFixCommand:
    """CLI entry point for ``agdt-speckit-request-artifact-fix``."""

    def test_posts_the_comment_and_exits_zero(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch("agentic_devtools.cli.speckit.request_artifact_fix.post_pr_comment", return_value=0) as post:
            request_artifact_fix_command(_argv())

        body = post.call_args[0][2]
        assert body.startswith("@copilot")
        assert "--spec-context" not in body
        assert "Requested @copilot artifact fix on PR #42." in capsys.readouterr().out

    def test_resolves_the_parent_spec_for_task_level_specs(self, tmp_path: Path) -> None:
        spec_base = tmp_path / "specs"
        spec_dir = spec_base / "1900-task"
        spec_dir.mkdir(parents=True)
        (spec_dir / "hierarchy.yml").write_text("parent: 1859\n", encoding="utf-8")
        parent_dir = spec_base / "1859-feature"
        parent_dir.mkdir()
        (parent_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.request_artifact_fix.post_pr_comment", return_value=0) as post:
            request_artifact_fix_command(
                _argv(
                    spec_dir=str(spec_dir),
                    hierarchy_level="task",
                    spec_base_path=str(spec_base),
                )
            )

        assert f"--spec-context {(parent_dir / 'spec.md').as_posix()}" in post.call_args[0][2]

    def test_exits_one_when_gh_fails(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch("agentic_devtools.cli.speckit.request_artifact_fix.post_pr_comment", return_value=1):
            with pytest.raises(SystemExit) as excinfo:
                request_artifact_fix_command(_argv())

        assert excinfo.value.code == 1
        assert "failed to post the artifact-gate repair comment" in capsys.readouterr().err

    def test_rejects_unknown_hierarchy_levels(self, capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as excinfo:
            request_artifact_fix_command(_argv(hierarchy_level="milestone"))

        assert excinfo.value.code == 2
        assert "invalid choice: 'milestone'" in capsys.readouterr().err

    def test_uses_sys_argv_when_argv_is_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("sys.argv", ["agdt-speckit-request-artifact-fix", *_argv()])
        captured: dict[str, Any] = {}

        def fake_post(pr: str, repo: str, body: str) -> int:
            captured["pr"] = pr
            return 0

        with patch(
            "agentic_devtools.cli.speckit.request_artifact_fix.post_pr_comment",
            side_effect=fake_post,
        ):
            request_artifact_fix_command(None)

        assert captured["pr"] == "42"
