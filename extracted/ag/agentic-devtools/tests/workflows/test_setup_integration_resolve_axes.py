"""Integration tests for setup command axis resolution + injection ordering.

Covers: detected-platform filtering, --skip-platform-detection inject-all,
detection-exception inject-all, and --issue-adapter with unresolved hosting.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.platform_detection import DetectionResult
from agentic_devtools.skill_injector import InjectionSummary


def _make_statuses(git_found: bool = True) -> list:
    return [
        DependencyStatus(name="copilot", found=True, version="v1.0.0", path="/bin/copilot", category="Recommended"),
        DependencyStatus(name="gh", found=True, version="v2.65.0", path="/bin/gh", category="Recommended"),
        DependencyStatus(
            name="git",
            found=git_found,
            path="/usr/bin/git" if git_found else None,
            version="2.43.0" if git_found else None,
            required=True,
            category="Required",
        ),
        DependencyStatus(name="az", found=False, category="Optional — needed for Azure DevOps"),
        DependencyStatus(name="code", found=False, category="Optional — needed for VS Code integration"),
    ]


def _seed_config(git_root: Path, platform: dict) -> None:
    """Write a .github/agdt-config.json with the given platform section."""
    github_dir = git_root / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)
    (github_dir / "agdt-config.json").write_text(json.dumps({"platform": platform}), encoding="utf-8")


class TestSetupIntegrationResolveAxes:
    """Integration tests for axis resolution before injection."""

    def _run_setup(self, argv: list[str], git_root: Path, *, inject_side_effect):
        """Run setup_cmd with standard mocks and capture injection kwargs."""
        captured: dict[str, str | None] = {}

        def _fake_inject(root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return inject_side_effect(
                root,
                issue_adapter=issue_adapter,
                code_hosting=code_hosting,
                assume_yes=assume_yes,
            )

        with patch("sys.argv", argv):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=git_root):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                    side_effect=_fake_inject,
                                                ):
                                                    commands.setup_cmd()
        return captured

    def test_detected_platform_filtering(self, capsys, tmp_path):
        """Normal detection path → resolved axes forwarded to injection; save precedes inject."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        config_dict = {"issue_adapter": "jira", "code_hosting": "github"}
        det_result = DetectionResult(
            detected_issue_platforms=("jira",),
            detected_code_hosting="github",
        )

        call_order: list[str] = []

        def _inject(root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            call_order.append("inject")
            return True, InjectionSummary(injected=100, pruned=50)

        def _save(platform_config, git_root=None):
            call_order.append("save")
            return True

        with patch("sys.stdin", mock_stdin):
            with patch(
                "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                return_value=det_result,
            ):
                with patch(
                    "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                    return_value=config_dict,
                ):
                    with patch("agentic_devtools.config.save_platform_config", side_effect=_save):
                        captured = self._run_setup(
                            ["agdt-setup"],
                            tmp_path,
                            inject_side_effect=_inject,
                        )

        assert captured == {"issue_adapter": "jira", "code_hosting": "github"}
        out = capsys.readouterr().out
        assert "pruned 50" in out
        assert call_order.index("save") < call_order.index("inject"), (
            f"Expected save_platform_config before inject_skills_with_summary, got order: {call_order}"
        )

    def test_skip_platform_detection_inject_all(self, capsys, tmp_path):
        """--skip-platform-detection → (None, None) inject-all."""
        _seed_config(tmp_path, {"issue_adapter": "github", "code_hosting": "github"})

        def _inject(root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            return True, InjectionSummary(injected=200, pruned=0)

        captured = self._run_setup(
            ["agdt-setup", "--skip-platform-detection"],
            tmp_path,
            inject_side_effect=_inject,
        )
        assert captured == {"issue_adapter": None, "code_hosting": None}
        out = capsys.readouterr().out
        assert "no platform filter applied" in out

    def test_detection_exception_inject_all(self, capsys, tmp_path):
        """Detection raises → (None, None) inject-all."""

        def _inject(root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            return True, InjectionSummary(injected=200, pruned=0)

        with patch(
            "agentic_devtools.cli.setup.platform_detection.detect_platforms",
            side_effect=RuntimeError("network error"),
        ):
            captured = self._run_setup(
                ["agdt-setup"],
                tmp_path,
                inject_side_effect=_inject,
            )
        assert captured == {"issue_adapter": None, "code_hosting": None}

    @patch("sys.platform", "linux")
    def test_issue_adapter_override_with_unresolved_hosting(self, capsys, tmp_path):
        """--issue-adapter github + no hosting detection → adapter resolved, hosting None."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        def _inject(root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            return True, InjectionSummary(injected=150, pruned=30)

        with patch("sys.stdin", mock_stdin):
            with patch("agentic_devtools.config.load_platform_config", return_value={}):
                with patch("agentic_devtools.config.save_platform_config", return_value=True):
                    with patch(
                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                        return_value=DetectionResult(),
                    ):
                        captured = self._run_setup(
                            ["agdt-setup", "--issue-adapter", "github"],
                            tmp_path,
                            inject_side_effect=_inject,
                        )

        assert captured["issue_adapter"] == "github"
        # Hosting was not detected → None (unrestricted)
        assert captured["code_hosting"] is None
        err = capsys.readouterr().err
        assert "Code hosting could not be detected" in err
