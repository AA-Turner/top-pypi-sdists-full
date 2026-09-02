"""Tests for setup_cmd."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.phase_markers import GENERATION_END, GENERATION_START
from agentic_devtools.cli.setup.phases import AUTORUN_SETUP_PHASE, PHASES
from agentic_devtools.cli.setup.platform_detection import DetectionResult
from agentic_devtools.cli.setup.pr_workflow import PrWorkflowResult
from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome
from agentic_devtools.cli.setup.version_guard import VersionGuardResult
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


def _record_autorun_phase(status: str):
    """Build an ``_autorun_setup_dev_tools`` side effect that records a phase.

    The returned callable records an ``autorun_setup`` phase with the given
    ``status`` into the ``report`` passed to ``_autorun_setup_dev_tools`` so the
    post-autorun version comparison in ``setup_cmd`` sees a realistic report.
    Returns ``True`` when *status* is ``"success"`` or ``"failed"`` (child was
    invoked) and ``False`` when ``"skipped"`` (child was not invoked), matching
    the bool return contract of the real ``_autorun_setup_dev_tools``.
    """

    def _side_effect(**kwargs) -> bool:
        from agentic_devtools.cli.setup.report import PhaseResult

        kwargs["report"].record(PhaseResult(name=AUTORUN_SETUP_PHASE, status=status))
        return status in ("success", "failed")

    return _side_effect


class TestSetupCmd:
    """Tests for setup_cmd."""

    @pytest.fixture(autouse=True)
    def _isolate_gitignore(self):
        """Prevent setup_cmd() from writing .agdt/.gitignore, injecting skills, or running the PR workflow."""

        def _mock_pr_workflow(fn, _ver):
            fn()
            return PrWorkflowResult(
                success=True,
                branch_created=None,
                pr_created=False,
                message="Mocked — no PR workflow in tests.",
            )

        with patch("agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow", side_effect=_mock_pr_workflow):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
                with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=False):
                    with patch(
                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                        return_value=(False, InjectionSummary(injected=0, pruned=0)),
                    ):
                        with patch.object(commands, "_populate_available_models"):
                            yield

    def test_exits_zero_on_full_success(self, capsys):
        """Exits 0 when all installs succeed and required deps are found."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()  # Should not raise

    def test_registers_setup_artifacts_when_certs_prefetched(self, capsys):
        """When cert prefetch yields a bundle path, artifacts are registered when in a git repo (FR-002)."""
        bundle = Path("/home/user/.agdt/certs/unified-ca-bundle.pem")
        pr_wf_result = {"branch_created": None, "pr_created": False, "message": "no changes"}
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow", return_value=pr_wf_result
                ):
                    with patch.object(commands, "_prefetch_certs", return_value=(bundle, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch.object(commands, "_register_setup_artifacts") as mock_register:
                                            commands.setup_cmd()
        mock_register.assert_called_once()
        # unified bundle path is forwarded; not a dry run.
        assert mock_register.call_args[0][1] == bundle
        assert mock_register.call_args.kwargs == {}

    def test_skips_artifact_registration_when_no_git_root(self, capsys):
        """When not in a git repo (git_root is None), artifact registration is skipped."""
        bundle = Path("/home/user/.agdt/certs/unified-ca-bundle.pem")
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
                with patch.object(commands, "_prefetch_certs", return_value=(bundle, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch.object(commands, "_register_setup_artifacts") as mock_register:
                                        commands.setup_cmd()
        mock_register.assert_not_called()

    def test_exits_one_when_copilot_install_fails(self, capsys):
        """Exits 1 when copilot CLI install fails."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=False):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with pytest.raises(SystemExit) as exc_info:
                                    commands.setup_cmd()
        assert exc_info.value.code == 1

    def test_exits_one_when_gh_install_fails(self, capsys):
        """Exits 1 when gh CLI install fails."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=False):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with pytest.raises(SystemExit) as exc_info:
                                    commands.setup_cmd()
        assert exc_info.value.code == 1

    def test_exits_two_when_required_dep_missing(self, capsys):
        """Exits 2 (MISSING_REQUIRED_DEP) when a required dependency (git) is not found."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(False)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with pytest.raises(SystemExit) as exc_info:
                                    commands.setup_cmd()
        assert exc_info.value.code == 2

    def test_required_missing_report_sets_warnings_false(self):
        """MISSING_REQUIRED_DEP report is not marked as warnings-only."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(False)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report", return_value=True
                                ) as mock_write:
                                    with pytest.raises(SystemExit) as exc_info:
                                        commands.setup_cmd()

        assert exc_info.value.code == 2
        report = mock_write.call_args[0][0]
        assert report.exit_code_name == "MISSING_REQUIRED_DEP"
        assert report.details.get("warnings") is False

    def test_required_missing_skips_repo_mutation_phase(self, tmp_path):
        """Required-missing exits before any repo mutation or PR workflow runs."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(False)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore"
                                    ) as mock_gitignore:
                                        with patch(
                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow"
                                        ) as mock_pr_workflow:
                                            with pytest.raises(SystemExit) as exc_info:
                                                commands.setup_cmd()

        assert exc_info.value.code == 2
        mock_gitignore.assert_not_called()
        mock_pr_workflow.assert_not_called()

    def test_prints_banner(self, capsys):
        """Prints the setup banner."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()
        out = capsys.readouterr().out
        assert "agentic-devtools Setup" in out

    def test_system_only_skips_managed_installs(self, capsys):
        """With --system-only, managed installs are skipped."""
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)) as mock_certs:
                with patch.object(commands, "install_copilot_cli") as mock_copilot:
                    with patch.object(commands, "install_gh_cli") as mock_gh:
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()
        mock_certs.assert_not_called()
        mock_copilot.assert_not_called()
        mock_gh.assert_not_called()

    def test_system_only_exits_zero_when_required_deps_found(self, capsys):
        """With --system-only, exits 0 when required deps are present."""
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                with patch.object(commands, "_persist_env_vars_to_profile"):
                    commands.setup_cmd()  # Should not raise

    def test_system_only_skips_repo_prompts_and_platform_setup_in_repo(self, tmp_path):
        """With --system-only in a repo, file steps still run but prompts/platform setup are skipped."""
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                with patch.object(commands, "_persist_env_vars_to_profile"):
                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                        with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True):
                            with patch.object(commands, "_prompt_project_config") as mock_prompt_project:
                                with patch.object(commands, "_prompt_copilot_model") as mock_prompt_model:
                                    with patch.object(commands, "_populate_available_models") as mock_models:
                                        with patch.object(commands, "_generate_setup_scripts") as mock_scripts:
                                            with patch(
                                                "agentic_devtools.cli.setup.gitignore_negations.ensure_root_gitignore_negations",
                                                return_value=False,
                                            ):
                                                with patch(
                                                    "agentic_devtools.cli.config.project_config.load_project_config",
                                                    return_value={},
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.config.project_config.save_project_config"
                                                    ) as mock_save:
                                                        with patch(
                                                            "agentic_devtools.cli.setup.report.write_report",
                                                            return_value=True,
                                                        ):
                                                            commands.setup_cmd()

        mock_prompt_project.assert_not_called()
        mock_prompt_model.assert_not_called()
        mock_models.assert_not_called()
        mock_scripts.assert_called_once_with(tmp_path)
        mock_save.assert_called_once()

    def test_system_only_exits_two_when_required_dep_missing(self, capsys):
        """With --system-only, exits 2 (MISSING_REQUIRED_DEP) when a required dependency is missing."""
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(False)):
                with patch.object(commands, "_persist_env_vars_to_profile"):
                    with pytest.raises(SystemExit) as exc_info:
                        commands.setup_cmd()
        assert exc_info.value.code == 2

    def test_system_only_prints_skip_message(self, capsys):
        """With --system-only, prints a message indicating managed installs are skipped."""
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                with patch.object(commands, "_persist_env_vars_to_profile"):
                    commands.setup_cmd()
        out = capsys.readouterr().out
        assert "--system-only" in out

    def test_no_verify_ssl_cleaned_up_after_setup(self, monkeypatch):
        """AGDT_NO_VERIFY_SSL is removed from env after setup_cmd completes."""
        monkeypatch.delenv("AGDT_NO_VERIFY_SSL", raising=False)
        monkeypatch.setattr("sys.argv", ["agdt-setup", "--no-verify-ssl"])

        with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
            with patch.object(commands, "install_copilot_cli", return_value=True):
                with patch.object(commands, "install_gh_cli", return_value=True):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "_persist_env_vars_to_profile"):
                            commands.setup_cmd()

        assert os.environ.get("AGDT_NO_VERIFY_SSL") is None

    def test_no_verify_ssl_prints_warning(self, capsys, monkeypatch):
        """Prints a warning when --no-verify-ssl is used."""
        monkeypatch.setattr("sys.argv", ["agdt-setup", "--no-verify-ssl"])

        with patch.object(commands, "install_copilot_cli", return_value=True):
            with patch.object(commands, "install_gh_cli", return_value=True):
                with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                    with patch.object(commands, "_persist_env_vars_to_profile"):
                        commands.setup_cmd()

        out = capsys.readouterr().out
        assert "SSL verification disabled" in out

    def test_without_no_verify_ssl_does_not_set_env_var(self, monkeypatch):
        """Does not set AGDT_NO_VERIFY_SSL when flag is absent."""
        monkeypatch.delenv("AGDT_NO_VERIFY_SSL", raising=False)
        monkeypatch.setattr("sys.argv", ["agdt-setup"])

        with patch.object(commands, "install_copilot_cli", return_value=True):
            with patch.object(commands, "install_gh_cli", return_value=True):
                with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                    with patch.object(commands, "_persist_env_vars_to_profile"):
                        commands.setup_cmd()

        assert os.environ.get("AGDT_NO_VERIFY_SSL") is None

    def test_no_persist_env_flag_disables_persistence(self, monkeypatch):
        """--no-persist-env flag disables env var persistence."""
        monkeypatch.setattr("sys.argv", ["agdt-setup", "--no-persist-env"])

        with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
            with patch.object(commands, "install_copilot_cli", return_value=True):
                with patch.object(commands, "install_gh_cli", return_value=True):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "_persist_env_vars_to_profile") as mock_persist:
                            commands.setup_cmd()

        mock_persist.assert_called_once()
        assert mock_persist.call_args.kwargs["persist_env"] is False

    def test_overwrite_env_flag_accepted(self, monkeypatch):
        """--overwrite-env flag is accepted and passed through."""
        monkeypatch.setattr("sys.argv", ["agdt-setup", "--overwrite-env"])

        with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
            with patch.object(commands, "install_copilot_cli", return_value=True):
                with patch.object(commands, "install_gh_cli", return_value=True):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "_persist_env_vars_to_profile") as mock_persist:
                            commands.setup_cmd()

        mock_persist.assert_called_once()
        assert mock_persist.call_args.kwargs["overwrite_env"] is True

    def test_gitignore_success_prints_message(self, capsys, tmp_path):
        """Prints success message when .agdt/.gitignore is created."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                # Override autouse fixture to test the success path
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                commands.setup_cmd()

        out = capsys.readouterr().out
        assert "Ensured .agdt/.gitignore" in out

    def test_gitignore_write_failure_warns_on_stderr(self, capsys, tmp_path):
        """Prints warning to stderr when .agdt/.gitignore write fails."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                # Override autouse fixture to test the failure path
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=False
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                commands.setup_cmd()

        err = capsys.readouterr().err
        assert "Failed to create/update .agdt/.gitignore" in err

    def test_inject_skills_success_prints_message(self, capsys, tmp_path):
        """Prints success message when agent/prompt/skill files are injected."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                    return_value=(True, InjectionSummary(injected=5, pruned=0)),
                                                ):
                                                    commands.setup_cmd()

        out = capsys.readouterr().out
        assert "Injected 5 agent/prompt/skill items" in out

    def test_inject_skills_failure_warns_on_stderr(self, capsys, tmp_path):
        """Prints neutral warning to stderr when skill injection fails."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                    return_value=(False, InjectionSummary(injected=0, pruned=0)),
                                                ):
                                                    commands.setup_cmd()

        err = capsys.readouterr().err
        assert "Failed to inject agent/prompt/skill files" in err
        assert "missing/corrupted bundled skills" in err

    def test_inject_skills_blocked_deletions_exit_non_zero(self, capsys, tmp_path):
        """Pending deletions without --yes fail file_modifications and exit 5."""
        from agentic_devtools.cli.setup.exit_codes import ExitCode

        blocked = InjectionSummary(injected=0, pruned=0, deletions_blocked=True)
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                    return_value=(False, blocked),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.report.write_report",
                                                        return_value=True,
                                                    ) as mock_write:
                                                        with pytest.raises(SystemExit) as excinfo:
                                                            commands.setup_cmd()

        assert excinfo.value.code == ExitCode.REPO_MUTATION_FAILED
        report = mock_write.call_args[0][0]
        file_mod_phase = next(phase for phase in report.phases if phase.name == "file_modifications")
        assert file_mod_phase.status == "failed"
        assert "would delete managed skill entries" in (file_mod_phase.error or "")
        err = capsys.readouterr().err
        assert "would delete managed skill entries" in err
        assert "agdt-setup --yes" in err

    def test_inject_skills_forwards_yes_flag(self, tmp_path):
        """--yes is forwarded to the injector as the deletion opt-in."""
        captured: dict[str, object] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["assume_yes"] = assume_yes
            return True, InjectionSummary(injected=1, pruned=0)

        with patch("sys.argv", ["agdt-setup", "--yes"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                    _fake_inject,
                                                ):
                                                    commands.setup_cmd()

        assert captured["assume_yes"] is True

    def test_injection_forwards_resolved_axes_from_saved_config(self, capsys, tmp_path):
        """--skip-platform-detection → inject-all (None, None) regardless of saved config (FR-003)."""
        # Pre-write a github/github platform config — should be ignored for injection
        # because --skip-platform-detection forces inject-all.
        github_dir = tmp_path / ".github"
        github_dir.mkdir(parents=True)
        (github_dir / "agdt-config.json").write_text(
            '{"platform": {"issue_adapter": "github", "code_hosting": "github"}}',
            encoding="utf-8",
        )
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=145, pruned=0)

        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
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

        assert captured == {"issue_adapter": None, "code_hosting": None}
        out = capsys.readouterr().out
        assert "Injected 145 agent/prompt/skill items (no platform filter applied)" in out

    def test_injection_falls_back_to_inject_all_without_config(self, capsys, tmp_path):
        """With no saved config, setup forwards (None, None) → legacy inject-all."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
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

        assert captured == {"issue_adapter": None, "code_hosting": None}
        out = capsys.readouterr().out
        assert "Injected 257 agent/prompt/skill items (no platform filter applied)" in out

    def test_skip_platform_detection_still_forwards_persisted_adapter_to_specialization(self, tmp_path):
        """Specialization still receives a persisted authoritative adapter when detection is skipped."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        persisted_platform = {
            "issue_adapter": "github",
            "issue_adapter_resolved": True,
            "code_hosting": "github",
        }

        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.config.load_repo_config",
                                                    return_value={"platform": persisted_platform},
                                                ) as mock_load:
                                                    with patch(
                                                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                        side_effect=_fake_inject,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                            return_value=[],
                                                        ):
                                                            with patch.object(
                                                                commands, "_specialize_setup_expectations"
                                                            ) as mock_specialize:
                                                                commands.setup_cmd()

        assert captured == {"issue_adapter": None, "code_hosting": None}
        mock_load.assert_any_call(str(tmp_path))
        assert mock_specialize.call_args.kwargs["resolved_platform"] == persisted_platform

    def test_injection_warns_and_skips_on_import_error(self, capsys, tmp_path):
        """Prints a warning and skips injection when the lazy skill injector import fails."""
        import builtins

        original_import = builtins.__import__

        def _raising_import(name, *args, **kwargs):
            if name == "agentic_devtools.skill_injector":
                raise SyntaxError("simulated syntax error in skill_injector")
            return original_import(name, *args, **kwargs)

        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch("builtins.__import__", side_effect=_raising_import):
                                                    commands.setup_cmd()

        err = capsys.readouterr().err
        assert "Failed to import skill injector" in err
        assert "skipping agent/prompt/skill file injection" in err

    def test_no_verify_ssl_restored_after_setup_when_previously_set(self, monkeypatch):
        """Restores pre-existing AGDT_NO_VERIFY_SSL value after setup_cmd completes."""
        monkeypatch.setenv("AGDT_NO_VERIFY_SSL", "pre-existing")
        monkeypatch.setattr("sys.argv", ["agdt-setup", "--no-verify-ssl"])

        with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
            with patch.object(commands, "install_copilot_cli", return_value=True):
                with patch.object(commands, "install_gh_cli", return_value=True):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "_persist_env_vars_to_profile"):
                            commands.setup_cmd()

        assert os.environ.get("AGDT_NO_VERIFY_SSL") == "pre-existing"

    def test_no_verify_ssl_cleaned_up_on_error(self, monkeypatch):
        """AGDT_NO_VERIFY_SSL is cleaned up even when setup_cmd raises."""
        monkeypatch.delenv("AGDT_NO_VERIFY_SSL", raising=False)
        monkeypatch.setattr("sys.argv", ["agdt-setup", "--no-verify-ssl"])

        with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
            with patch.object(commands, "install_copilot_cli", return_value=False):
                with patch.object(commands, "install_gh_cli", return_value=True):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "_persist_env_vars_to_profile"):
                            try:
                                commands.setup_cmd()
                            except SystemExit:
                                pass

        assert os.environ.get("AGDT_NO_VERIFY_SSL") is None

    # ── New flag acceptance tests ──────────────────────────────────────

    def test_skip_platform_detection_flag_accepted(self, capsys):
        """--skip-platform-detection flag is accepted without error."""
        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()

    def test_issue_adapter_jira_flag_accepted(self, capsys):
        """--issue-adapter jira flag is accepted without error."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "jira"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()

    def test_issue_adapter_github_flag_accepted(self, capsys):
        """--issue-adapter github flag is accepted without error."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()

    def test_issue_adapter_markdown_flag_accepted(self, capsys):
        """--issue-adapter markdown flag is accepted without error."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "markdown"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()

    def test_skip_templates_flag_accepted(self, capsys):
        """--skip-templates flag is accepted without error."""
        with patch("sys.argv", ["agdt-setup", "--skip-templates"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()

    def test_reconfigure_flag_accepted(self, capsys):
        """--reconfigure flag is accepted without error."""
        with patch("sys.argv", ["agdt-setup", "--reconfigure"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                commands.setup_cmd()

    def test_reconfigure_flag_threads_to_prompt_functions(self, capsys, tmp_path):
        """--reconfigure passes force_prompt=True to both prompt functions."""
        with patch("sys.argv", ["agdt-setup", "--reconfigure", "--skip-platform-detection", "--skip-templates"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config") as mock_project:
                                            with patch.object(commands, "_prompt_copilot_model") as mock_copilot:
                                                with patch.object(
                                                    commands, "_populate_available_models"
                                                ) as mock_models:
                                                    commands.setup_cmd()
        mock_project.assert_called_once_with(force_prompt=True)
        mock_copilot.assert_called_once_with(force_prompt=True, refresh_models=False)
        mock_models.assert_called_once_with(refresh_models=True)

    def test_no_refresh_models_disables_live_discovery(self, capsys, tmp_path):
        """--no-refresh-models passes refresh_models=False to the inventory step."""
        with patch("sys.argv", ["agdt-setup", "--no-refresh-models", "--skip-platform-detection", "--skip-templates"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch.object(
                                                    commands, "_populate_available_models"
                                                ) as mock_models:
                                                    commands.setup_cmd()
        mock_models.assert_called_once_with(refresh_models=False)

    def test_no_reconfigure_passes_false_to_prompt_functions(self, capsys, tmp_path):
        """Without --reconfigure, force_prompt=False is passed to both prompt functions."""
        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection", "--skip-templates"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config") as mock_project:
                                            with patch.object(commands, "_prompt_copilot_model") as mock_copilot:
                                                with patch.object(
                                                    commands, "_populate_available_models"
                                                ) as mock_models:
                                                    commands.setup_cmd()
        mock_project.assert_called_once_with(force_prompt=False)
        mock_copilot.assert_called_once_with(force_prompt=False, refresh_models=False)
        mock_models.assert_called_once_with(refresh_models=True)

    def test_defaults_and_reconfigure_warns_reconfigure_ignored(self, capsys, tmp_path):
        """--defaults + --reconfigure together → warning that --reconfigure is ignored."""
        with patch(
            "sys.argv", ["agdt-setup", "--defaults", "--reconfigure", "--skip-platform-detection", "--skip-templates"]
        ):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch("agentic_devtools.cli.setup.phase_0._prompt_phase_0_config"):
                                                    commands.setup_cmd()

        err = capsys.readouterr().err
        assert "--reconfigure is ignored when --defaults is set" in err

    def test_invalid_issue_adapter_rejected(self, capsys):
        """Invalid --issue-adapter value is rejected by argparse."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "foo"]):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_cmd()
        assert exc_info.value.code == 2

    # ── Platform detection step tests ──────────────────────────────────

    def test_detection_runs_and_save_succeeds(self, capsys, tmp_path):
        """Detection runs and save succeeds → prints success message."""
        mock_result = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=mock_result,
                                                    ) as mock_detect:
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value={"issue_adapter": "jira"},
                                                        ) as mock_confirm:
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Platform configuration saved" in out
        mock_detect.assert_called_once_with(str(tmp_path))
        mock_confirm.assert_called_once_with(mock_result, selection_state={})
        mock_save.assert_called_once_with(
            str(tmp_path),
            {
                "issue_adapter": "jira",
                "issue_adapter_resolved": False,
            },
        )

    def test_skip_platform_detection_skips_detect_and_save(self, capsys, tmp_path):
        """--skip-platform-detection → detection and save are NOT called."""
        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                ) as mock_detect:
                                                    with patch(
                                                        "agentic_devtools.config.save_platform_config",
                                                    ) as mock_save:
                                                        with patch(
                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                            return_value=[],
                                                        ):
                                                            commands.setup_cmd()
        mock_detect.assert_not_called()
        mock_save.assert_not_called()

    def test_issue_adapter_override_runs_hosting_detection(self, capsys, tmp_path):
        """--issue-adapter jira still runs hosting detection and uses fresh hosting."""
        existing_config = {
            "issue_adapter": "github",
            "code_hosting": "azure_devops",
            "jira": {},
            "github": {"repo": "owner/repo"},
            "azure_devops": {"project": "org/proj"},
        }
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "jira"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    return_value=DetectionResult(
                                                        detected_code_hosting="github",
                                                    ),
                                                ) as mock_detect:
                                                    with patch(
                                                        "agentic_devtools.config.load_platform_config",
                                                        return_value=existing_config,
                                                    ) as mock_load:
                                                        with patch(
                                                            "agentic_devtools.config.save_platform_config",
                                                            return_value=True,
                                                        ) as mock_save:
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Issue adapter configured: jira" in out
        # FR-002: hosting detection runs even with --issue-adapter
        mock_detect.assert_called_once_with(str(tmp_path))
        mock_load.assert_any_call(str(tmp_path))
        # Verify existing fields are preserved and adapter overridden.
        mock_save.assert_called_once_with(
            str(tmp_path),
            {
                "issue_adapter": "jira",
                "code_hosting": "github",
                "jira": {},
                "github": {"repo": "owner/repo"},
                "azure_devops": {"project": "org/proj"},
                "issue_adapter_resolved": True,
            },
        )

    def test_issue_adapter_override_skip_detection_skips_hosting(self, capsys, tmp_path):
        """--issue-adapter + --skip-platform-detection → hosting detection is skipped."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "jira", "--skip-platform-detection"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                ) as mock_detect:
                                                    with patch(
                                                        "agentic_devtools.config.load_platform_config",
                                                        return_value={"issue_adapter": "github"},
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.save_platform_config",
                                                            return_value=True,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        mock_detect.assert_not_called()

    def test_issue_adapter_override_detection_raises_silenced(self, capsys, tmp_path):
        """--issue-adapter + detect_platforms raises → detection_failed set, config saves with loaded hosting.

        Injection falls back to inject-all because detection_failed=True.
        """
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        side_effect=RuntimeError("network down"),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_platform_config",
                                                            return_value={"code_hosting": "azure_devops"},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        # Hosting unchanged from loaded config despite detection failure
        mock_save.assert_called_once()
        saved_config = mock_save.call_args[0][1]
        assert saved_config["code_hosting"] == "azure_devops"
        assert saved_config["issue_adapter"] == "github"

    def test_issue_adapter_override_detection_raises_triggers_inject_all(self, capsys, tmp_path):
        """--issue-adapter + detect_platforms raises → detection_failed=True → injection receives (None, None)."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        side_effect=RuntimeError("network down"),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_platform_config",
                                                            return_value={"code_hosting": "azure_devops"},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()
        # detection_failed=True triggers FR-003 inject-all fallback
        assert captured == {"issue_adapter": None, "code_hosting": None}

    def test_system_only_loads_persisted_platform_config_for_injection(self, capsys, tmp_path):
        """--system-only loads existing platform config so injection uses persisted axes, not inject-all."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=145, pruned=30)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                "issue_adapter": "github",
                                                                "code_hosting": "github",
                                                            }
                                                        },
                                                    ) as mock_load:
                                                        with patch(
                                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                            side_effect=_fake_inject,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        # Persisted raw platform config was loaded for --system-only
        # (once for injection-axis resolution, once for specialization metadata).
        assert mock_load.call_count == 2
        mock_load.assert_any_call(str(tmp_path))
        # Injection uses axes from persisted config, not (None, None) inject-all
        assert captured == {"issue_adapter": "github", "code_hosting": "github"}

    def test_system_only_load_repo_config_exception_falls_back_to_inject_all(self, capsys, tmp_path):
        """--system-only + load_repo_config raises → falls back to inject-all (None, None)."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        side_effect=OSError("no config"),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                            side_effect=_fake_inject,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        # Load failed → inject-all fallback
        assert captured == {"issue_adapter": None, "code_hosting": None}

    def test_system_only_empty_platform_config_uses_inject_all(self, capsys, tmp_path):
        """--system-only + missing raw platform section keeps axes unresolved."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={},
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                            side_effect=_fake_inject,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        assert captured == {"issue_adapter": None, "code_hosting": None}

    def test_system_only_default_issue_adapter_not_promoted_to_injection_axis(self, capsys, tmp_path):
        """--system-only: DEFAULT_ISSUE_ADAPTER ("jira") stored as fallback must not activate the axis.

        When a prior run detected no issue tracker and wrote issue_adapter="jira" as a default
        fallback, --system-only must treat it as unresolved (inject-all for that axis) rather
        than activating the Jira axis.  A genuine non-default value like "github" on the
        code_hosting axis is still forwarded.
        """
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                # "jira" is DEFAULT_ISSUE_ADAPTER — written even
                                                                # when no issue tracker was detected; must not
                                                                # activate the axis.
                                                                "issue_adapter": "jira",
                                                                "issue_adapter_resolved": False,
                                                                "code_hosting": "github",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                            side_effect=_fake_inject,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        # issue_adapter="jira" is the DEFAULT fallback → axis must NOT be activated (None)
        # code_hosting="github" is a non-default filter-capable value → axis is activated
        assert captured == {"issue_adapter": None, "code_hosting": "github"}

    def test_system_only_persisted_jira_resolution_is_forwarded_to_injection(self, capsys, tmp_path):
        """--system-only forwards a persisted Jira axis when setup marked it as genuinely resolved."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=12)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                "issue_adapter": "jira",
                                                                "issue_adapter_resolved": True,
                                                                "code_hosting": "github",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                            side_effect=_fake_inject,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        assert captured == {"issue_adapter": "jira", "code_hosting": "github"}

    def test_system_only_legacy_jira_config_without_marker_keeps_axis_unresolved(self, capsys, tmp_path):
        """--system-only: markerless fallback jira remains unresolved.

        Older setup runs could persist issue_adapter="jira" as a generated fallback with no
        issue_adapter_resolved marker. Without an independent resolved signal, this value
        must not activate issue-adapter filtering.
        """
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=12)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                # Legacy config: issue_adapter_resolved key
                                                                # is absent entirely (pre-marker config).
                                                                "issue_adapter": "jira",
                                                                "code_hosting": "github",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                            side_effect=_fake_inject,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        assert captured == {"issue_adapter": None, "code_hosting": "github"}

    def test_system_only_malformed_resolved_marker_does_not_activate_axis(self, capsys, tmp_path):
        """--system-only: a present but non-boolean issue_adapter_resolved marker is non-authoritative.

        A malformed persisted value (e.g. ``null`` → ``None``, or the string ``"false"``) is not a
        valid "resolved" signal.  Only a genuinely absent marker uses the legacy compatibility path;
        an invalid present value must leave the axis unresolved rather than activating (and pruning
        skills for) the stored adapter.
        """
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                # Malformed marker: string instead of bool.
                                                                "issue_adapter": "jira",
                                                                "issue_adapter_resolved": "false",
                                                                "code_hosting": "github",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                            side_effect=_fake_inject,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        # Malformed marker → adapter axis NOT activated (unresolved), hosting still applied.
        assert captured == {"issue_adapter": None, "code_hosting": "github"}

    def test_detection_interactive_override_updates_injection_axes(self, capsys, tmp_path):
        """Interactive override axes are forwarded to skill injection."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=10)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("jira",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value={
                                                                "issue_adapter": "github",
                                                                "code_hosting": "azure_devops",
                                                            },
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.skill_classification.resolve_platform_context",
                                                                return_value=("github", "azure_devops"),
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.config.save_platform_config",
                                                                    return_value=True,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                        side_effect=_fake_inject,
                                                                    ):
                                                                        with patch(
                                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                            return_value=[],
                                                                        ):
                                                                            commands.setup_cmd()
        assert captured == {"issue_adapter": "github", "code_hosting": "azure_devops"}

    def test_detection_interactive_override_only_hosting_does_not_activate_issue_adapter_fallback(
        self, capsys, tmp_path
    ):
        """Per-axis independence: user overrides only code_hosting; issue_adapter stays None.

        When detection finds no issue tracker (raw_inj_issue_adapter=None) and the user
        overrides only code_hosting via confirm_and_override, the issue_adapter axis must
        NOT be updated because the user did not explicitly change it.  The DEFAULT_ISSUE_ADAPTER
        fallback written by confirm_and_override (_build_config_from_result) must not be
        promoted into a genuine restriction.
        """
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=0)

        def _fake_confirm(_result, *, selection_state=None):
            if selection_state is not None:
                selection_state["issue_adapter_explicit"] = False
                selection_state["code_hosting_explicit"] = True
            return {
                # DEFAULT fallback — not explicitly changed
                "issue_adapter": "jira",
                # User overrode code_hosting from "other"
                "code_hosting": "azure_devops",
            }

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            # No issue tracker detected
                                                            detected_issue_platforms=(),
                                                            detected_code_hosting="other",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            side_effect=_fake_confirm,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()
        # issue_adapter was NOT changed by the user (DEFAULT fallback) → must stay None (inject-all)
        # code_hosting WAS changed by the user ("other" → "azure_devops") → must be forwarded
        assert captured == {"issue_adapter": None, "code_hosting": "azure_devops"}

    def test_detection_interactive_explicit_jira_override_activates_issue_adapter_axis(self, capsys, tmp_path):
        """Explicitly choosing Jira activates the axis even when it matches the fallback value."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=7)

        saved_platform_configs: list[dict[str, object]] = []

        def _fake_confirm(result, *, selection_state=None):
            if selection_state is not None:
                selection_state["issue_adapter_explicit"] = True
                selection_state["code_hosting_explicit"] = False
            return {
                "issue_adapter": "jira",
                "code_hosting": "other",
            }

        def _fake_save(_repo_path, platform_config):
            saved_platform_configs.append(dict(platform_config))
            return True

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=(),
                                                            detected_code_hosting=None,
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            side_effect=_fake_confirm,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                side_effect=_fake_save,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()
        assert captured == {"issue_adapter": "jira", "code_hosting": None}
        assert saved_platform_configs[-1]["issue_adapter_resolved"] is True

    def test_detection_interactive_accept_uses_first_valid_detected_axis(self, capsys, tmp_path):
        """Interactive accept keeps first valid detected adapter when leading value is invalid."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=10)

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("unsupported", "github"),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value={
                                                                "issue_adapter": "github",
                                                                "code_hosting": "github",
                                                            },
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()
        assert captured == {"issue_adapter": "github", "code_hosting": "github"}

    def test_issue_adapter_override_detection_returns_no_hosting(self, capsys, tmp_path):
        """--issue-adapter + detection returns no code_hosting → resets to DEFAULT_CODE_HOSTING."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("jira",),
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_platform_config",
                                                            return_value={},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Code hosting could not be detected" in err

    def test_issue_adapter_override_prefers_detected_hosting_over_existing_config(self, capsys, tmp_path):
        """--issue-adapter uses fresh detected hosting for injection and persistence."""
        captured: dict[str, str | None] = {}
        saved_platform_configs: list[dict[str, object]] = []

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=8)

        def _fake_save(_repo_path, platform_config):
            saved_platform_configs.append(dict(platform_config))
            return True

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("jira",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_platform_config",
                                                            return_value={
                                                                "issue_adapter": "jira",
                                                                "code_hosting": "azure_devops",
                                                                "issue_adapter_resolved": True,
                                                            },
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                side_effect=_fake_save,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()
        assert captured == {"issue_adapter": "github", "code_hosting": "github"}
        assert saved_platform_configs[-1]["code_hosting"] == "github"

    def test_issue_adapter_override_uses_detected_hosting_when_no_configured_value(
        self,
        capsys,
        tmp_path,
    ):
        """--issue-adapter + detection returns hosting + no prior configured hosting → use detected."""
        captured: dict[str, str | None] = {}
        saved_platform_configs: list[dict[str, object]] = []

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=10, pruned=0)

        def _fake_save(_repo_path, platform_config):
            saved_platform_configs.append(dict(platform_config))
            return True

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("jira",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_platform_config",
                                                            # No prior code_hosting configured
                                                            return_value={},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                side_effect=_fake_save,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()
        # Detection result is used when no configured hosting axis exists
        assert captured == {"issue_adapter": "github", "code_hosting": "github"}
        assert saved_platform_configs[-1]["code_hosting"] == "github"

    def test_issue_adapter_override_configured_hosting_reset_when_detection_finds_none(
        self,
        capsys,
        tmp_path,
    ):
        """--issue-adapter + existing configured hosting + detection returns no host.

        When the current detection run returns no code_hosting, the persisted
        config must be set to DEFAULT_CODE_HOSTING (catch-all) and injection
        must receive code_hosting=None (unrestricted), even if an existing
        configured value is present.  A stale configured value must not be
        forwarded when the current detection cannot confirm it.
        """
        captured: dict[str, str | None] = {}
        saved_platform_configs: list[dict[str, object]] = []

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=10, pruned=0)

        def _fake_save(_repo_path, platform_config):
            saved_platform_configs.append(dict(platform_config))
            return True

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("jira",),
                                                            # no detected_code_hosting — detection found nothing
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_platform_config",
                                                            return_value={
                                                                "issue_adapter": "jira",
                                                                "code_hosting": "azure_devops",
                                                                "issue_adapter_resolved": True,
                                                            },
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                side_effect=_fake_save,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()
        # Injection hosting axis must be unrestricted (None)
        assert captured["issue_adapter"] == "github"
        assert captured["code_hosting"] is None
        # Persisted config must use the catch-all, not the stale configured value
        assert saved_platform_configs[-1]["code_hosting"] == "other"
        # Warning must be emitted (adapter axis is active but hosting is unrestricted)
        err = capsys.readouterr().err
        assert "Code hosting could not be detected" in err

    def test_detection_path_prefers_detected_hosting_when_not_explicitly_overridden(
        self,
        capsys,
        tmp_path,
    ):
        """Detected hosting stays authoritative when the user does not override hosting."""
        captured: dict[str, str | None] = {}
        saved_platform_configs: list[dict[str, object]] = []

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=6)

        def _fake_confirm(result, *, selection_state=None):
            if selection_state is not None:
                selection_state["issue_adapter_explicit"] = False
                selection_state["code_hosting_explicit"] = False
            return {
                "issue_adapter": "github",
                "code_hosting": "github",
            }

        def _fake_save(_repo_path, platform_config):
            saved_platform_configs.append(dict(platform_config))
            return True

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                "issue_adapter": "markdown",
                                                                "issue_adapter_resolved": True,
                                                                "code_hosting": "azure_devops",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                            return_value=DetectionResult(
                                                                detected_issue_platforms=("github",),
                                                                detected_code_hosting="github",
                                                            ),
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                                side_effect=_fake_confirm,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.config.save_platform_config",
                                                                    side_effect=_fake_save,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                        side_effect=_fake_inject,
                                                                    ):
                                                                        with patch(
                                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                            return_value=[],
                                                                        ):
                                                                            commands.setup_cmd()
        assert captured == {"issue_adapter": None, "code_hosting": "github"}
        assert saved_platform_configs[-1]["issue_adapter"] == "markdown"
        assert saved_platform_configs[-1]["code_hosting"] == "github"
        assert saved_platform_configs[-1]["issue_adapter_resolved"] is True

    def test_detection_path_keeps_configured_hosting_when_detection_returns_none(
        self,
        capsys,
        tmp_path,
    ):
        """Detection path keeps configured hosting when current detection finds no host."""
        captured: dict[str, str | None] = {}
        saved_platform_configs: list[dict[str, object]] = []

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=6)

        def _fake_confirm(result, *, selection_state=None):
            if selection_state is not None:
                selection_state["issue_adapter_explicit"] = False
                selection_state["code_hosting_explicit"] = False
            return {
                "issue_adapter": "github",
                "code_hosting": "other",
            }

        def _fake_save(_repo_path, platform_config):
            saved_platform_configs.append(dict(platform_config))
            return True

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                "issue_adapter": "markdown",
                                                                "issue_adapter_resolved": True,
                                                                "code_hosting": "azure_devops",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                            return_value=DetectionResult(
                                                                detected_issue_platforms=("github",),
                                                                detected_code_hosting=None,
                                                            ),
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                                side_effect=_fake_confirm,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.config.save_platform_config",
                                                                    side_effect=_fake_save,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                        side_effect=_fake_inject,
                                                                    ):
                                                                        with patch(
                                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                            return_value=[],
                                                                        ):
                                                                            commands.setup_cmd()
        assert captured == {"issue_adapter": None, "code_hosting": "azure_devops"}
        assert saved_platform_configs[-1]["issue_adapter"] == "markdown"
        assert saved_platform_configs[-1]["code_hosting"] == "azure_devops"
        assert saved_platform_configs[-1]["issue_adapter_resolved"] is True

    def test_detection_path_prefers_existing_filter_capable_issue_adapter_when_authoritative(
        self,
        capsys,
        tmp_path,
    ):
        """Configured authoritative issue adapter beats detection when not explicitly overridden."""
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=6)

        def _fake_confirm(result, *, selection_state=None):
            if selection_state is not None:
                selection_state["issue_adapter_explicit"] = False
                selection_state["code_hosting_explicit"] = False
            return {
                "issue_adapter": "jira",
                "code_hosting": "github",
            }

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                "issue_adapter": "github",
                                                                "issue_adapter_resolved": True,
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                            return_value=DetectionResult(
                                                                detected_issue_platforms=("jira",),
                                                                detected_code_hosting="github",
                                                            ),
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                                side_effect=_fake_confirm,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.config.save_platform_config",
                                                                    return_value=True,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                        side_effect=_fake_inject,
                                                                    ):
                                                                        with patch(
                                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                            return_value=[],
                                                                        ):
                                                                            commands.setup_cmd()

        assert captured["issue_adapter"] == "github"

    def test_detection_path_legacy_jira_config_without_marker_keeps_axis_unresolved(
        self,
        capsys,
        tmp_path,
    ):
        """Detection path: markerless fallback jira stays unresolved.

        A markerless stored "jira" value may be an old generated fallback, so it must not
        activate issue-adapter filtering without an explicit resolved marker.
        """
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=5)

        def _fake_confirm(result, *, selection_state=None):
            # User accepts without changing anything
            if selection_state is not None:
                selection_state["issue_adapter_explicit"] = False
                selection_state["code_hosting_explicit"] = False
            return {"issue_adapter": "jira", "code_hosting": "github"}

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                # Legacy config: issue_adapter_resolved
                                                                # key is absent (pre-marker config).
                                                                "issue_adapter": "jira",
                                                                "code_hosting": "github",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                            return_value=DetectionResult(
                                                                # Detection finds no issue tracker.
                                                                detected_issue_platforms=(),
                                                                detected_code_hosting="github",
                                                            ),
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                                side_effect=_fake_confirm,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.config.save_platform_config",
                                                                    return_value=True,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                        side_effect=_fake_inject,
                                                                    ):
                                                                        with patch(
                                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                            return_value=[],
                                                                        ):
                                                                            commands.setup_cmd()
        assert captured["issue_adapter"] is None

    def test_detection_path_malformed_resolved_marker_is_non_authoritative(
        self,
        capsys,
        tmp_path,
    ):
        """Detection path: a present but non-boolean issue_adapter_resolved marker is non-authoritative.

        A malformed persisted marker (e.g. the string ``"false"``) is not a valid "resolved" signal,
        so the configured adapter must NOT be treated as authoritative.  With detection finding no
        issue tracker, the axis stays unresolved instead of forwarding the stored "jira" value.
        """
        captured: dict[str, str | None] = {}

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=111, pruned=0)

        def _fake_confirm(result, *, selection_state=None):
            if selection_state is not None:
                selection_state["issue_adapter_explicit"] = False
                selection_state["code_hosting_explicit"] = False
            return {"issue_adapter": "jira", "code_hosting": "github"}

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.config.load_repo_config",
                                                        return_value={
                                                            "platform": {
                                                                # Malformed marker: string instead of bool.
                                                                "issue_adapter": "jira",
                                                                "issue_adapter_resolved": "false",
                                                                "code_hosting": "github",
                                                            }
                                                        },
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                            return_value=DetectionResult(
                                                                detected_issue_platforms=(),
                                                                detected_code_hosting="github",
                                                            ),
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                                side_effect=_fake_confirm,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.config.save_platform_config",
                                                                    return_value=True,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                        side_effect=_fake_inject,
                                                                    ):
                                                                        with patch(
                                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                            return_value=[],
                                                                        ):
                                                                            commands.setup_cmd()
        # Malformed marker → configured adapter is NOT authoritative; axis stays unresolved.
        assert captured["issue_adapter"] is None

    def test_isatty_raises_oserror_treats_as_non_interactive(self, capsys, tmp_path):
        """sys.stdin.isatty() raises OSError → is_interactive defaults to False, setup continues."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.side_effect = OSError("stdin closed")
        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        commands.setup_cmd()
        # Setup must complete without raising — OSError on isatty is silently handled
        out = capsys.readouterr().out
        assert "Setup complete" in out

    def test_no_tty_detection_selects_first_valid_issue_platform(self, capsys, tmp_path):
        """No TTY with detected platforms → selects first valid adapter (not raw first element)."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("github",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ) as mock_detect:
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        # Detection ran (no --skip-platform-detection)
        mock_detect.assert_called_once()
        # First valid platform is selected; confirm_and_override is NOT called (no TTY)
        saved_config = mock_save.call_args[0][1]
        assert saved_config["issue_adapter"] == "github"
        assert saved_config["code_hosting"] == "github"

    def test_no_tty_markerless_jira_fallback_is_replaced_by_detected_adapter(self, capsys, tmp_path):
        """No TTY: markerless jira fallback can be replaced by a detected adapter.

        A markerless jira value is ambiguous and may be a generated fallback. When detection
        identifies a concrete adapter, unattended setup should use the detected adapter.
        """
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("github",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={
                                                                "platform": {
                                                                    # Legacy config: no resolved marker.
                                                                    "issue_adapter": "jira",
                                                                    "code_hosting": "github",
                                                                }
                                                            },
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        saved_config = mock_save.call_args[0][1]
        assert saved_config["issue_adapter"] == "github"
        assert saved_config[commands._ISSUE_ADAPTER_RESOLVED_KEY] is True

    def test_no_tty_detection_unknown_platform_falls_back_to_default(self, capsys, tmp_path):
        """No TTY + all detected platforms are invalid → falls back to DEFAULT_ISSUE_ADAPTER."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("unknown_platform",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        # Invalid platform is skipped; DEFAULT_ISSUE_ADAPTER ("jira") is used
        saved_config = mock_save.call_args[0][1]
        assert saved_config["issue_adapter"] == "jira"

    def test_no_tty_detection_preserves_existing_config_keys(self, capsys, tmp_path):
        """No TTY: detection only updates detected axes; existing keys (phase_0, jira.url) are preserved."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        existing_platform = {
            "issue_adapter": "jira",
            "code_hosting": "azure_devops",
            "issue_adapter_resolved": False,
            "jira": {"url": "https://jira.example.com"},
            "github": {},
            "azure_devops": {},
            "phase_0": {"enabled": True},
            "custom_key": "custom_val",
        }
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("github",),
                                                            detected_code_hosting="github",
                                                            github_repo="owner/repo",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={"platform": existing_platform},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        saved_config = mock_save.call_args[0][1]
        # Detected axes are updated
        assert saved_config["issue_adapter"] == "github"
        assert saved_config["code_hosting"] == "github"
        assert saved_config["github"]["repo"] == "owner/repo"
        # Existing keys not touched by detection are preserved
        assert saved_config["phase_0"] == {"enabled": True}
        assert saved_config["jira"]["url"] == "https://jira.example.com"
        assert saved_config["custom_key"] == "custom_val"

    def test_no_tty_detection_finds_nothing_preserves_configured_axes(self, capsys, tmp_path):
        """No TTY: detection finds no issue platforms and no hosting → existing configured axes preserved.

        An unattended re-run where detection temporarily finds nothing must not
        overwrite authoritative persisted axes with fallback defaults.
        """
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        existing_platform = {
            "issue_adapter": "github",
            "code_hosting": "github",
            "issue_adapter_resolved": True,
            "github": {"repo": "owner/my-repo"},
            "phase_0": {"enabled": True},
        }
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=(),
                                                            # no detected_code_hosting — detection found nothing
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={"platform": existing_platform},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        saved_config = mock_save.call_args[0][1]
        # Authoritative configured axes must be preserved, not overwritten by fallbacks
        assert saved_config["issue_adapter"] == "github"
        assert saved_config["code_hosting"] == "github"
        assert saved_config["issue_adapter_resolved"] is True
        # Other keys must also be preserved
        assert saved_config["phase_0"] == {"enabled": True}

    def test_no_tty_detection_finds_nothing_preserves_nonauthoritative_adapter(self, capsys, tmp_path):
        """No TTY: non-authoritative (marker=False) valid adapter preserved when detection finds nothing.

        When the resolved marker is explicitly False the adapter is a fallback (not authoritative),
        so it does not take the authoritative-preserve branch. If detection then finds no issue
        platform, the existing valid adapter value is still preserved but the resolved marker stays
        False (it was never genuinely resolved).
        """
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        existing_platform = {
            "issue_adapter": "jira",
            "code_hosting": "github",
            "issue_adapter_resolved": False,
            "github": {"repo": "owner/my-repo"},
        }
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=(),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={"platform": existing_platform},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        saved_config = mock_save.call_args[0][1]
        # Existing valid adapter value preserved, but marker stays False (never resolved)
        assert saved_config["issue_adapter"] == "jira"
        assert saved_config["issue_adapter_resolved"] is False

    def test_no_tty_detection_finds_nothing_malformed_marker_stays_non_authoritative(self, capsys, tmp_path):
        """No TTY: a present malformed resolved marker stays non-authoritative when detection finds nothing."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        existing_platform = {
            "issue_adapter": "jira",
            "code_hosting": "github",
            "issue_adapter_resolved": "false",
            "github": {"repo": "owner/my-repo"},
        }
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=(),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={"platform": existing_platform},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        saved_config = mock_save.call_args[0][1]
        assert saved_config["issue_adapter"] == "jira"
        assert saved_config["issue_adapter_resolved"] is False

    def test_no_tty_detection_load_repo_config_exception_falls_back_to_empty(self, capsys, tmp_path):
        """No TTY: load_repo_config raises → falls back to empty platform_config and continues."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("github",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            side_effect=OSError("disk error"),
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        # Exception is silenced; setup still saves with fallback empty config + detected axes
        saved_config = mock_save.call_args[0][1]
        assert saved_config["issue_adapter"] == "github"
        assert saved_config["code_hosting"] == "github"

    def test_no_tty_detection_github_in_config_and_azure_devops_project_set(self, capsys, tmp_path):
        """No TTY: github already in existing config (elif skipped) and azure_devops_project set."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        existing_platform = {"github": {"repo": "old/repo"}}
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("github",),
                                                            detected_code_hosting="github",
                                                            github_repo=None,
                                                            azure_devops_project="MyProject",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={"platform": existing_platform},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        saved_config = mock_save.call_args[0][1]
        # github already present — not overwritten, elif branch skipped
        assert saved_config["github"] == {"repo": "old/repo"}
        # azure_devops_project set — project written via setdefault path
        assert saved_config["azure_devops"]["project"] == "MyProject"

    def test_no_tty_detection_normalizes_null_jira_subsection(self, capsys, tmp_path):
        """No TTY: a JSON-null Jira sub-section is normalized before saving."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        existing_platform = {"jira": None}
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("github",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_repo_config",
                                                            return_value={"platform": existing_platform},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ) as mock_save:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        saved_config = mock_save.call_args[0][1]
        assert saved_config["jira"] == {}

    def test_save_platform_config_returns_false_warns_stderr(self, capsys, tmp_path):
        """save_platform_config returns False → prints warning to stderr."""
        mock_result = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=mock_result,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value={"issue_adapter": "jira"},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=False,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Failed to save platform configuration" in err

    def test_save_platform_config_false_in_detection_path_triggers_inject_all(self, tmp_path):
        """Detection path: save return False triggers FR-003 inject-all fallback."""
        captured: dict[str, str | None] = {}
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("github",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value={
                                                                "issue_adapter": "github",
                                                                "code_hosting": "github",
                                                            },
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=False,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()

        assert captured == {"issue_adapter": None, "code_hosting": None}

    def test_save_platform_config_false_with_issue_adapter_triggers_inject_all(self, tmp_path):
        """--issue-adapter path: save return False triggers FR-003 inject-all fallback."""
        captured: dict[str, str | None] = {}
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        def _fake_inject(git_root, *, issue_adapter=None, code_hosting=None, assume_yes=False):
            captured["issue_adapter"] = issue_adapter
            captured["code_hosting"] = code_hosting
            return True, InjectionSummary(injected=257, pruned=0)

        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=DetectionResult(
                                                            detected_issue_platforms=("jira",),
                                                            detected_code_hosting="github",
                                                        ),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.config.load_platform_config",
                                                            return_value={"code_hosting": "azure_devops"},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=False,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                                                                    side_effect=_fake_inject,
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                        return_value=[],
                                                                    ):
                                                                        commands.setup_cmd()

        assert captured == {"issue_adapter": None, "code_hosting": None}

    def test_detect_platforms_raises_warns_stderr(self, capsys, tmp_path):
        """detect_platforms raises RuntimeError → prints warning to stderr, setup completes."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("boom"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Platform setup failed" in err
        assert "boom" in err

    def test_system_only_skips_detection(self, capsys):
        """--system-only → detection NOT called."""
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                with patch.object(commands, "_persist_env_vars_to_profile"):
                    with patch(
                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                    ) as mock_detect:
                        commands.setup_cmd()
        mock_detect.assert_not_called()

    # ── Template generation step tests ─────────────────────────────────

    def test_templates_generated_prints_paths(self, capsys, tmp_path):
        """Templates generated → prints success message for each file."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[
                                                            Path("/tmp/a.py"),
                                                            Path("/tmp/b.py"),
                                                        ],
                                                    ):
                                                        commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Generated template:" in out

    def test_skip_templates_does_not_call_generate(self, capsys, tmp_path):
        """--skip-templates → generate_default_templates NOT called."""
        with patch("sys.argv", ["agdt-setup", "--skip-templates"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                    ) as mock_gen:
                                                        commands.setup_cmd()
        mock_gen.assert_not_called()

    def test_templates_empty_list_prints_info(self, capsys, tmp_path):
        """generate_default_templates returns empty list → prints info message."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Workflow templates already exist" in out

    def test_template_generation_raises_warns_stderr(self, capsys, tmp_path):
        """generate_default_templates raises OSError → prints warning, setup completes."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        side_effect=OSError("disk full"),
                                                    ):
                                                        commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Template generation failed" in err
        assert "disk full" in err

    def test_commit_template_already_exists_prints_info(self, capsys, tmp_path):
        """ensure_commit_template returns False → prints info message."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.commit_template_setup.ensure_commit_template",
                                                            return_value=False,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.commit_template_setup.validate_commit_template",
                                                                return_value=[],
                                                            ):
                                                                commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Commit template already exists" in out

    def test_commit_template_validation_warnings_printed(self, capsys, tmp_path):
        """validate_commit_template returns warnings → printed to stderr."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.commit_template_setup.ensure_commit_template",
                                                            return_value=True,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.commit_template_setup.validate_commit_template",
                                                                return_value=["Missing variable 'issueType'"],
                                                            ):
                                                                commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Missing variable 'issueType'" in err

    def test_commit_template_setup_exception_warns_stderr(self, capsys, tmp_path):
        """Exception in commit template setup → warning on stderr, setup continues."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.commit_template_setup.ensure_commit_template",
                                                            side_effect=OSError("permission denied"),
                                                        ):
                                                            commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Commit template setup failed" in err
        assert "permission denied" in err

    def test_template_target_dir_is_correct(self, capsys, tmp_path):
        """Template target_dir is git_root / '.agdt' / 'workflow-definitions'."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ) as mock_gen:
                                                        commands.setup_cmd()
        mock_gen.assert_called_once_with(tmp_path / ".agdt" / "workflow-definitions")

    # ── Import failure tests ───────────────────────────────────────────

    def test_platform_detection_import_failure_skips_detection(self, capsys, tmp_path):
        """Import of platform_detection fails → prints warning, skips detection, templates still run."""
        import builtins

        original_import = builtins.__import__

        def _raising_import(name, *args, **kwargs):
            if name == "agentic_devtools.cli.setup.platform_detection":
                raise ImportError("simulated import error")
            return original_import(name, *args, **kwargs)

        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch("builtins.__import__", side_effect=_raising_import):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ) as mock_gen:
                                                        commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Platform setup failed" in err
        mock_gen.assert_called_once()

    def test_workflow_templates_import_failure_skips_templates(self, capsys, tmp_path):
        """Import of workflow_templates fails → prints warning, skips templates."""
        import builtins

        original_import = builtins.__import__

        def _raising_import(name, *args, **kwargs):
            if name == "agentic_devtools.cli.setup.workflow_templates":
                raise ImportError("simulated import error")
            return original_import(name, *args, **kwargs)

        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch("builtins.__import__", side_effect=_raising_import):
                                                    commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Template generation failed" in err

    # ── Integration tests ──────────────────────────────────────────────

    def test_all_new_steps_succeed_exits_zero(self, capsys, tmp_path):
        """All new steps succeed → setup exits 0 with success message."""
        mock_result = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=mock_result,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value={"issue_adapter": "github"},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[Path("/tmp/a.py")],
                                                                ):
                                                                    commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Setup complete! ✅" in out

    def test_new_steps_fail_but_setup_still_exits_zero(self, capsys, tmp_path):
        """New steps fail but copilot/gh/deps succeed → setup still exits 0."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("detection failed"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        side_effect=OSError("template failed"),
                                                    ):
                                                        commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Setup complete! ✅" in out

    def test_save_platform_config_returns_false_with_issue_adapter_warns(self, capsys, tmp_path):
        """--issue-adapter with save returning False → prints warning to stderr."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "github"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.config.load_platform_config",
                                                    return_value={
                                                        "issue_adapter": "jira",
                                                        "code_hosting": "other",
                                                        "jira": {},
                                                        "github": {},
                                                        "azure_devops": {},
                                                    },
                                                ):
                                                    with patch(
                                                        "agentic_devtools.config.save_platform_config",
                                                        return_value=False,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                            return_value=[],
                                                        ):
                                                            commands.setup_cmd()
        err = capsys.readouterr().err
        assert "Failed to save platform configuration" in err

    def test_section_header_printed(self, capsys, tmp_path):
        """Platform & Workflow Setup section header is printed."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Platform & Workflow Setup" in out

    def test_skip_pr_workflow_flag_accepted(self, capsys, tmp_path):
        """--skip-pr-workflow flag is accepted without error."""
        with patch("sys.argv", ["agdt-setup", "--skip-pr-workflow"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        commands.setup_cmd()

    def test_skip_pr_workflow_bypasses_pr_workflow(self, capsys, tmp_path):
        """--skip-pr-workflow runs file-modifying steps directly without PR workflow."""
        with patch("sys.argv", ["agdt-setup", "--skip-pr-workflow"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                    side_effect=RuntimeError("skip"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                        return_value=[],
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow"
                                                        ) as mock_pr:
                                                            commands.setup_cmd()
        # PR workflow should NOT be called
        mock_pr.assert_not_called()

    def test_pr_workflow_invoked_when_conditions_met(self, capsys, tmp_path):
        """PR workflow is invoked when git_root is set and --skip-pr-workflow is not passed."""
        from agentic_devtools.cli.setup.pr_workflow import PrWorkflowResult

        mock_result = PrWorkflowResult(
            success=True,
            branch_created="chore/agdt-setup-0.1.0",
            pr_created=True,
            message="PR created from branch 'chore/agdt-setup-0.1.0'.",
        )
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow",
                                            return_value=mock_result,
                                        ) as mock_pr:
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    commands.setup_cmd()
        mock_pr.assert_called_once()
        out = capsys.readouterr().out
        assert "Setup changes committed to branch" in out
        assert "Pull request created for setup changes" in out

    def test_pr_workflow_branch_created_but_pr_failed_shows_warning(self, capsys, tmp_path):
        """When branch is created but PR creation fails, shows the failure message."""
        from agentic_devtools.cli.setup.pr_workflow import PrWorkflowResult

        mock_result = PrWorkflowResult(
            success=True,
            branch_created="chore/agdt-setup-0.1.0",
            pr_created=False,
            message="Branch 'chore/agdt-setup-0.1.0' pushed but PR creation failed.",
        )
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow",
                                            return_value=mock_result,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    commands.setup_cmd()
        out = capsys.readouterr().out
        assert "Setup changes committed to branch" in out
        assert "PR creation failed" in out

    # ── Version guard integration tests ────────────────────────────────

    def test_version_guard_block_exits_one(self, capsys):
        """guard_result == 'block' → sys.exit(10) with VERSION_BLOCKED report."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="block", target_version="0.2.69"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 3

    def test_version_guard_force_skips_repo_steps(self, capsys, tmp_path):
        """guard_result == 'force' → file-modifying steps are skipped."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore"
                                        ) as mock_gitignore:
                                            with patch(
                                                "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow"
                                            ) as mock_pr_workflow:
                                                commands.setup_cmd()
        # File-modifying steps should NOT have run
        mock_gitignore.assert_not_called()
        mock_pr_workflow.assert_not_called()

    def test_force_old_version_flag_passes_true_to_check_version_guard(self):
        """--force-old-version flag passes force_old_version=True to check_version_guard."""
        with patch("sys.argv", ["agdt-setup", "--force-old-version"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ) as mock_guard:
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        commands.setup_cmd()
        mock_guard.assert_called_once_with(Path("/fake/repo"), True)

    def test_without_force_old_version_flag_passes_false_to_check_version_guard(self):
        """Without --force-old-version, force_old_version=False is passed to check_version_guard."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ) as mock_guard:
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        commands.setup_cmd()
        mock_guard.assert_called_once_with(Path("/fake/repo"), False)

    # ── Root gitignore negation integration tests ──────────────────────

    def test_gitignore_negations_success_prints_message(self, capsys, tmp_path):
        """Prints success message when root .gitignore negation rules are added."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.gitignore_negations.ensure_root_gitignore_negations",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    commands.setup_cmd()

        out = capsys.readouterr().out
        assert "Added .gitignore negation rules for .agdt/config/project.json" in out

    # ── Version pinning integration tests ──────────────────────────────

    def test_version_pinning_success_prints_message(self, capsys, tmp_path):
        """Prints success message when agdt_version is pinned in project.json."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.config.project_config.load_project_config",
                                                    return_value={},
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.config.project_config.save_project_config",
                                                    ) as mock_save:
                                                        commands.setup_cmd()

        out = capsys.readouterr().out
        assert "Pinned agdt_version=" in out
        mock_save.assert_called_once()

    def test_specialization_uses_newly_persisted_version_pin(self, tmp_path):
        """Specialization receives the version that setup just persisted to project.json."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.__version__", "9.9.9"):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.cli.setup.version_guard.check_version_guard",
                                            return_value=VersionGuardResult(action="ok", pinned_version=None),
                                        ):
                                            with patch(
                                                "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                                return_value=True,
                                            ):
                                                with patch.object(commands, "_prompt_project_config"):
                                                    with patch.object(commands, "_prompt_copilot_model"):
                                                        with patch(
                                                            "agentic_devtools.cli.config.project_config.load_project_config",
                                                            return_value={},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.config.project_config.save_project_config"
                                                            ):
                                                                with patch.object(
                                                                    commands, "_specialize_setup_expectations"
                                                                ) as mock_specialize:
                                                                    commands.setup_cmd()

        assert mock_specialize.call_count == 1
        assert mock_specialize.call_args.kwargs["version_pin"] == "9.9.9"

    def test_specialization_uses_guard_pin_when_repo_steps_are_skipped(self, tmp_path):
        """Specialization uses the guard pin unchanged when ``--force-old-version`` skips repo steps."""
        with patch("sys.argv", ["agdt-setup", "--force-old-version"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.cli.setup.version_guard.check_version_guard",
                                        return_value=VersionGuardResult(action="force", pinned_version="1.2.3"),
                                    ):
                                        with patch.object(
                                            commands, "_specialize_setup_expectations"
                                        ) as mock_specialize:
                                            commands.setup_cmd()

        assert mock_specialize.call_count == 1
        assert mock_specialize.call_args.kwargs["version_pin"] == "1.2.3"

    def test_version_pinning_exception_warns_on_stderr(self, capsys, tmp_path):
        """Prints warning to stderr when version pinning fails."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.config.project_config.load_project_config",
                                                    side_effect=[{}, RuntimeError("disk full")],
                                                ):
                                                    commands.setup_cmd()

        err = capsys.readouterr().err
        assert "Failed to pin agdt_version" in err

    def test_version_pinning_skipped_when_no_repo_mutations_succeeded(self, capsys, tmp_path):
        """Version pin is NOT written when all repo-mutating steps failed."""
        with patch("sys.argv", ["agdt-setup", "--skip-platform-detection", "--skip-templates"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    # All mutation steps fail or return False
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=False
                                    ):
                                        with patch(
                                            "agentic_devtools.skill_injector.inject_skills_with_summary",
                                            return_value=(False, InjectionSummary(injected=0, pruned=0)),
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch.object(
                                                        commands,
                                                        "_generate_setup_scripts",
                                                        side_effect=RuntimeError("boom"),
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.gitignore_negations.ensure_root_gitignore_negations",
                                                            return_value=False,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.commands.ensure_copilot_settings",
                                                                return_value=False,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.cli.config.project_config.save_project_config",
                                                                ) as mock_save:
                                                                    commands.setup_cmd()

        out = capsys.readouterr().out
        assert "Pinned agdt_version=" not in out
        mock_save.assert_not_called()

    def test_skill_injector_import_failure_silenced_when_no_git_root(self, capsys):
        """Silently skips skill injection warning when import fails and git_root is None."""
        import builtins

        original_import = builtins.__import__

        def _raising_import(name, *args, **kwargs):
            if name == "agentic_devtools.skill_injector":
                raise ImportError("simulated import error")
            return original_import(name, *args, **kwargs)

        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                # autouse fixture already sets git_root=None
                                with patch("builtins.__import__", side_effect=_raising_import):
                                    commands.setup_cmd()

        err = capsys.readouterr().err
        # Warning should NOT appear when git_root is None
        assert "Failed to import skill injector" not in err

    def test_script_generation_exception_warns_on_stderr(self, capsys, tmp_path):
        """Prints warning to stderr when _generate_setup_scripts raises."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch.object(
                                                    commands,
                                                    "_generate_setup_scripts",
                                                    side_effect=RuntimeError("disk full"),
                                                ):
                                                    commands.setup_cmd()

        err = capsys.readouterr().err
        assert "Script generation failed" in err
        assert "disk full" in err

    def test_file_modifications_phase_skipped_when_no_git_root(self, capsys):
        """Report marks file_modifications as skipped when no git repo is available."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report",
                                    return_value=True,
                                ) as mock_write:
                                    commands.setup_cmd()

        report = mock_write.call_args[0][0]
        file_mod_phase = next(phase for phase in report.phases if phase.name == "file_modifications")
        assert file_mod_phase.status == "skipped"

    def test_unhandled_exception_exits_with_autorun_failed_report(self, capsys):
        """Non-SystemExit exception in setup_cmd → exit 6 with AUTORUN_FAILED report."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch(
                "agentic_devtools.state._get_git_repo_root",
                side_effect=RuntimeError("unexpected failure"),
            ):
                with patch("agentic_devtools.cli.setup.report.write_report", return_value=True) as mock_write:
                    with pytest.raises(SystemExit) as exc_info:
                        commands.setup_cmd()
        assert exc_info.value.code == 6
        mock_write.assert_called_once()
        report = mock_write.call_args[0][0]
        assert report.exit_code == 6
        assert report.exit_code_name == "AUTORUN_FAILED"
        assert report.details.get("error_type") == "RuntimeError"
        assert "error" not in report.details

    def test_outer_exception_before_specialization_calls_stale_cleanup(self, capsys):
        """Exception before specialization is attempted → stale-cleanup helper is called."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch(
                "agentic_devtools.state._get_git_repo_root",
                side_effect=RuntimeError("early failure"),
            ):
                with patch.object(commands, "_cleanup_stale_specialization_artifact") as mock_cleanup:
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with pytest.raises(SystemExit):
                            commands.setup_cmd()
        mock_cleanup.assert_called_once()

    def test_outer_exception_after_specialization_skips_stale_cleanup(self, capsys):
        """Exception after specialization was attempted → stale-cleanup helper is NOT called."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
                with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=False):
                    with patch(
                        "agentic_devtools.skill_injector.inject_skills_with_summary",
                        return_value=(False, InjectionSummary(injected=0, pruned=0)),
                    ):
                        with patch.object(commands, "_populate_available_models"):
                            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                                with patch.object(commands, "install_copilot_cli", return_value=True):
                                    with patch.object(commands, "install_gh_cli", return_value=True):
                                        with patch.object(
                                            commands,
                                            "check_all_dependencies",
                                            return_value=_make_statuses(True),
                                        ):
                                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                                with patch.object(commands, "_specialize_setup_expectations"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                                        return_value=True,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup."
                                                            "post_autorun_version_check."
                                                            "check_post_autorun_version",
                                                            side_effect=RuntimeError("post-version explosion"),
                                                        ):
                                                            with patch.object(
                                                                commands,
                                                                "_cleanup_stale_specialization_artifact",
                                                            ) as mock_cleanup:
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.report.write_report",
                                                                    return_value=True,
                                                                ):
                                                                    with pytest.raises(SystemExit):
                                                                        commands.setup_cmd()
        mock_cleanup.assert_not_called()

    def test_phase_tracker_records_failed_phase_on_exception(self, capsys):
        """_PhaseTracker records a failed phase when an exception occurs inside it."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    side_effect=RuntimeError("guard exploded"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True) as mock_write:
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 6
        report = mock_write.call_args[0][0]
        failed_phases = [p for p in report.phases if p.status == "failed"]
        assert len(failed_phases) == 1
        assert failed_phases[0].name == "version_check"
        assert "guard exploded" in (failed_phases[0].error or "")

    def test_file_modifications_phase_in_report_on_mid_phase_exception(self):
        """file_modifications PhaseResult is present with status 'failed' even when
        an unexpected exception fires inside the phase body (before the append).
        """
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.state._get_git_repo_root",
                                    return_value=Path("/fake/repo"),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.version_guard.check_version_guard",
                                        return_value=VersionGuardResult(action="ok"),
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow",
                                            side_effect=RuntimeError("pr_workflow exploded"),
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.setup.report.write_report",
                                                return_value=True,
                                            ) as mock_write:
                                                with pytest.raises(SystemExit) as exc_info:
                                                    commands.setup_cmd()
        assert exc_info.value.code == 5
        mock_write.assert_called_once()
        report = mock_write.call_args[0][0]
        file_mod_phases = [p for p in report.phases if p.name == "file_modifications"]
        assert len(file_mod_phases) == 1
        assert file_mod_phases[0].status == "failed"
        assert "pr_workflow exploded" in (file_mod_phases[0].error or "")

    # ── SetupReport integration tests (wiring) ────────────────────────────

    def test_version_blocked_report_payload(self):
        """VERSION_BLOCKED path writes SetupReport with exit_code=3 and correct details."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="block", target_version="0.2.69"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True) as mock_write:
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 3
        mock_write.assert_called_once()
        report = mock_write.call_args[0][0]
        from agentic_devtools.cli.setup.report import SetupReport

        assert isinstance(report, SetupReport)
        assert report.exit_code == 3
        assert report.exit_code_name == "VERSION_BLOCKED"
        assert report.details == {"reason": "version_blocked"}

    def test_version_blocked_with_refresh_sets_skipped_outcome(self):
        """--refresh-issue-types + version block records refresh_outcome=skipped(version_blocked)."""
        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="block", target_version="0.2.69"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True) as mock_write:
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 3
        report = mock_write.call_args[0][0]
        assert report.details["reason"] == "version_blocked"
        assert report.details["refresh_outcome"] == {
            "status": "skipped",
            "reason": "version_blocked",
            "error": None,
        }
        phases_by_name = {phase.name: phase.status for phase in report.phases}
        for phase_name in PHASES[1:]:
            assert phases_by_name[phase_name] == "skipped"

    def test_version_blocked_phases_include_version_check_success(self):
        """VERSION_BLOCKED path includes version_check phase with status 'success'."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="block", target_version="0.2.69"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True) as mock_write:
                        with pytest.raises(SystemExit):
                            commands.setup_cmd()
        report = mock_write.call_args[0][0]
        version_phases = [p for p in report.phases if p.name == "version_check"]
        assert len(version_phases) == 1
        assert version_phases[0].status == "success"

    def test_version_blocked_sys_exit_called_with_exit_code_3(self):
        """VERSION_BLOCKED path calls sys.exit with ExitCode.VERSION_BLOCKED (=3) after write_report."""
        call_order: list[str] = []

        def fake_exit(code: object) -> None:
            call_order.append("sys_exit")
            raise SystemExit(code)

        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="block", target_version="0.2.69"),
                ):
                    with patch(
                        "agentic_devtools.cli.setup.report.write_report",
                        side_effect=lambda r: call_order.append("write_report") or True,
                    ):
                        with patch("sys.exit", side_effect=fake_exit):
                            with pytest.raises(SystemExit) as exc_info:
                                commands.setup_cmd()
        assert exc_info.value.code == 3
        assert call_order == ["write_report", "sys_exit"]

    def test_version_blocked_write_report_false_does_not_alter_exit_code(self):
        """write_report returning False does not change the sys.exit code on VERSION_BLOCKED path."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="block", target_version="0.2.69"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=False):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 3

    def test_ok_path_writes_report_with_exit_code_zero(self):
        """OK path calls write_report with exit_code=0, exit_code_name='OK', non-empty phases."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report", return_value=True
                                ) as mock_write:
                                    commands.setup_cmd()
        mock_write.assert_called_once()
        report = mock_write.call_args[0][0]
        assert report.exit_code == 0
        assert report.exit_code_name == "OK"
        assert len(report.phases) > 0

    def test_warnings_path_writes_report_with_exit_code_one(self):
        """WARNINGS path calls write_report with exit_code=1, exit_code_name='WARNINGS'."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=False):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report", return_value=True
                                ) as mock_write:
                                    with pytest.raises(SystemExit) as exc_info:
                                        commands.setup_cmd()
        assert exc_info.value.code == 1
        mock_write.assert_called_once()
        report = mock_write.call_args[0][0]
        assert report.exit_code == 1
        assert report.exit_code_name == "WARNINGS"
        assert report.details == {"warnings": True}

    def test_system_only_report_has_skipped_phases(self):
        """--system-only flag produces report with skipped phases."""
        with patch("sys.argv", ["agdt-setup", "--system-only"]):
            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                with patch.object(commands, "_persist_env_vars_to_profile"):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True) as mock_write:
                        commands.setup_cmd()
        report = mock_write.call_args[0][0]
        skipped_phases = [p for p in report.phases if p.status == "skipped"]
        assert len(skipped_phases) >= 2
        skipped_names = [p.name for p in skipped_phases]
        assert "certificate_prefetch" in skipped_names
        assert "cli_installation" in skipped_names

    def test_missing_required_dep_report_has_phases(self):
        """MISSING_REQUIRED_DEP report has exit_code=2 and non-empty phases."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(False)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report", return_value=True
                                ) as mock_write:
                                    with pytest.raises(SystemExit) as exc_info:
                                        commands.setup_cmd()
        assert exc_info.value.code == 2
        report = mock_write.call_args[0][0]
        assert report.exit_code == 2
        assert len(report.phases) > 0

    def test_repo_mutation_failed_report_has_error_type(self):
        """REPO_MUTATION_FAILED report has exit_code=5 and details with error_type."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.state._get_git_repo_root",
                                    return_value=Path("/fake/repo"),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.version_guard.check_version_guard",
                                        return_value=VersionGuardResult(action="ok"),
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow",
                                            side_effect=RuntimeError("mutation error"),
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.setup.report.write_report",
                                                return_value=True,
                                            ) as mock_write:
                                                with pytest.raises(SystemExit) as exc_info:
                                                    commands.setup_cmd()
        assert exc_info.value.code == 5
        report = mock_write.call_args[0][0]
        assert report.exit_code == 5
        assert report.exit_code_name == "REPO_MUTATION_FAILED"
        assert report.details["error_type"] == "RuntimeError"

    def test_report_object_is_setup_report_instance(self):
        """Object passed to write_report is an instance of SetupReport."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report", return_value=True
                                ) as mock_write:
                                    commands.setup_cmd()
        from agentic_devtools.cli.setup.report import SetupReport

        report = mock_write.call_args[0][0]
        assert isinstance(report, SetupReport)

    def test_run_flag_in_help_output(self, capsys):
        """--run appears in help output with CI/TTY and env var description."""
        with pytest.raises(SystemExit):
            with patch("sys.argv", ["agdt-setup", "--help"]):
                commands.setup_cmd()
        captured = capsys.readouterr()
        assert "--run" in captured.out
        assert "AGDT_SETUP_RUN" in captured.out

    def test_no_run_flag_in_help_output(self, capsys):
        """--no-run appears in help output with CI/TTY and env var description."""
        with pytest.raises(SystemExit):
            with patch("sys.argv", ["agdt-setup", "--help"]):
                commands.setup_cmd()
        captured = capsys.readouterr()
        assert "--no-run" in captured.out
        assert "AGDT_SETUP_NO_AUTORUN" in captured.out

    def test_run_and_no_run_mutual_exclusion(self):
        """Passing both --run and --no-run causes argparse mutual exclusion error."""
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.argv", ["agdt-setup", "--run", "--no-run"]):
                commands.setup_cmd()
        assert exc_info.value.code == 2

    def test_report_has_autorun_enabled_field(self):
        """SetupReport includes autorun_enabled field in report output."""
        with patch("sys.argv", ["agdt-setup", "--run"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report", return_value=True
                                ) as mock_write:
                                    commands.setup_cmd()
        report = mock_write.call_args[0][0]
        assert report.autorun_enabled is True
        report_dict = report.to_dict()
        assert "autorun_enabled" in report_dict
        assert report_dict["autorun_enabled"] is True

    def test_no_run_flag_sets_autorun_enabled_false_in_report(self):
        """--no-run sets autorun_enabled to False in the report."""
        with patch("sys.argv", ["agdt-setup", "--no-run"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.report.write_report", return_value=True
                                ) as mock_write:
                                    commands.setup_cmd()
        report = mock_write.call_args[0][0]
        assert report.autorun_enabled is False

    def test_refresh_issue_types_standalone_exits_zero(self, capsys, tmp_path):
        """--refresh-issue-types standalone exits 0 after discovery."""
        config_file = tmp_path / ".github" / "agdt-config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text('{"platform": {"issue_adapter": "jira"}}')

        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch(
                                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types"
                                        ) as mock_discover:
                                            mock_discover.return_value = RefreshOutcome.success()
                                            with patch(
                                                "agentic_devtools.cli.setup.report.write_report", return_value=True
                                            ) as mock_write:
                                                with pytest.raises(SystemExit) as exc_info:
                                                    commands.setup_cmd()
        assert exc_info.value.code == 0
        mock_discover.assert_called_once_with(tmp_path, force_refresh=True, standalone=True)
        report = mock_write.call_args[0][0]
        assert report.details is not None
        assert report.details["refresh_outcome"] == {"status": "success", "reason": None, "error": None}
        phases_by_name = {phase.name: phase.status for phase in report.phases}
        assert phases_by_name["version_check"] == "success"
        for phase_name in PHASES[1:]:
            assert phases_by_name[phase_name] == "skipped"

    def test_refresh_issue_types_standalone_skips_dependency_gate(self, tmp_path):
        """Standalone refresh runs before dependency checks and exits 0."""
        config_file = tmp_path / ".github" / "agdt-config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text('{"platform": {"issue_adapter": "jira"}}')

        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies") as mock_check_deps:
                        with patch(
                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types"
                        ) as mock_discover:
                            with pytest.raises(SystemExit) as exc_info:
                                commands.setup_cmd()
        assert exc_info.value.code == 0
        mock_check_deps.assert_not_called()
        mock_discover.assert_called_once_with(tmp_path, force_refresh=True, standalone=True)

    def test_refresh_issue_types_no_config_warns(self, capsys, tmp_path):
        """--refresh-issue-types without agdt-config.json warns and exits 0."""
        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with pytest.raises(SystemExit) as exc_info:
                                            commands.setup_cmd()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "no platform configuration found" in captured.err

    def test_refresh_issue_types_with_skip_platform_detection(self, capsys, tmp_path):
        """--refresh-issue-types + --skip-platform-detection → skip silently."""
        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types", "--skip-platform-detection"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch(
                                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types"
                                        ) as mock_discover:
                                            with pytest.raises(SystemExit) as exc_info:
                                                commands.setup_cmd()
        assert exc_info.value.code == 0
        mock_discover.assert_not_called()

    def test_refresh_issue_types_no_git_root_warns(self, capsys):
        """--refresh-issue-types without git root warns and exits 0."""
        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types"]):
            with patch(
                "agentic_devtools.cli.setup.version_guard.check_version_guard",
                return_value=VersionGuardResult(action="ok"),
            ):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with pytest.raises(SystemExit) as exc_info:
                                        commands.setup_cmd()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "not inside a git repository" in captured.err

    def test_refresh_issue_types_exception_warns(self, capsys, tmp_path):
        """--refresh-issue-types exception → warns on stderr, exits 0."""
        config_file = tmp_path / ".github" / "agdt-config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text('{"platform": {"issue_adapter": "jira"}}')

        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch(
                                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types",
                                            side_effect=RuntimeError("something broke"),
                                        ):
                                            with pytest.raises(SystemExit) as exc_info:
                                                commands.setup_cmd()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Issue type refresh failed" in captured.err

    def test_refresh_issue_types_skips_in_force_old_version_mode(self, capsys, tmp_path):
        """--refresh-issue-types + --force-old-version → warns and skips discovery."""
        config_file = tmp_path / ".github" / "agdt-config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text('{"platform": {"issue_adapter": "jira"}}')

        with patch("sys.argv", ["agdt-setup", "--refresh-issue-types", "--force-old-version"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ):
                    with patch("agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types") as mock_discover:
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 0
        mock_discover.assert_not_called()
        captured = capsys.readouterr()
        assert (
            "Cannot refresh issue types: repo file modifications are disabled in --force-old-version mode."
            in captured.err
        )
        assert not (tmp_path / ".agdt" / "config" / "project.json").exists()

    def test_issue_type_discovery_exception_in_normal_flow(self, capsys, tmp_path):
        """Exception in issue type discovery during normal flow → warns, continues."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "jira"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.config.load_platform_config",
                                                    return_value={},
                                                ):
                                                    with patch(
                                                        "agentic_devtools.config.save_platform_config",
                                                        return_value=True,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types",
                                                            side_effect=RuntimeError("discovery error"),
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.cli.setup.report.write_report",
                                                                return_value=True,
                                                            ):
                                                                commands.setup_cmd()
        captured = capsys.readouterr()
        assert "Issue type discovery skipped" in captured.err

    def test_issue_type_discovery_skipped_when_platform_config_save_fails(self, tmp_path):
        """Discovery is not called when platform config save fails in this run."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "jira"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ):
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.config.load_platform_config",
                                                    return_value={},
                                                ):
                                                    with patch(
                                                        "agentic_devtools.config.save_platform_config",
                                                        return_value=False,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types"
                                                        ) as mock_discover:
                                                            with patch(
                                                                "agentic_devtools.cli.setup.report.write_report",
                                                                return_value=True,
                                                            ):
                                                                commands.setup_cmd()
        mock_discover.assert_not_called()

    def test_reconfigure_with_refresh_uses_normal_flow_force_refresh(self, tmp_path):
        """--reconfigure + --refresh-issue-types skips the standalone early return and forces normal-flow discovery."""
        with patch("sys.argv", ["agdt-setup", "--issue-adapter", "jira", "--reconfigure", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True):
                    with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                        with patch.object(commands, "install_copilot_cli", return_value=True):
                            with patch.object(commands, "install_gh_cli", return_value=True):
                                with patch.object(
                                    commands, "check_all_dependencies", return_value=_make_statuses(True)
                                ) as mock_check_deps:
                                    with patch.object(commands, "_persist_env_vars_to_profile"):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.config.load_platform_config",
                                                    return_value={},
                                                ):
                                                    with patch(
                                                        "agentic_devtools.config.save_platform_config",
                                                        return_value=True,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types"
                                                        ) as mock_discover:
                                                            with patch(
                                                                "agentic_devtools.cli.setup.report.write_report",
                                                                return_value=True,
                                                            ):
                                                                commands.setup_cmd()
        # Normal flow ran (dependency gate reached), not the standalone early return.
        mock_check_deps.assert_called_once()
        mock_discover.assert_called_once()
        assert mock_discover.call_args.kwargs["force_refresh"] is True

    def test_post_autorun_version_unchanged_exits_normally(self, capsys):
        """Autorun ran and version is unchanged → no upgrade exit (normal completion)."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_autorun_phase("success"),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check.capture_startup_version",
                                        return_value="0.2.326",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.post_autorun_version_check."
                                            "check_post_autorun_version",
                                            return_value="0.2.326",
                                        ) as mock_check:
                                            commands.setup_cmd()  # Should not raise
        mock_check.assert_called_once_with("0.2.326")

    def test_post_autorun_version_changed_exits_upgraded_rerun_needed(self, capsys):
        """Autorun ran and version changed → exit 4 (UPGRADED_RERUN_NEEDED)."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_autorun_phase("success"),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check.capture_startup_version",
                                        return_value="0.2.326",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.post_autorun_version_check."
                                            "check_post_autorun_version",
                                            return_value="0.2.330",
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.setup.report.write_report",
                                                return_value=True,
                                            ):
                                                with pytest.raises(SystemExit) as exc_info:
                                                    commands.setup_cmd()
        assert exc_info.value.code == 4
        captured = capsys.readouterr()
        assert "0.2.326" in captured.err
        assert "0.2.330" in captured.err

    def test_post_autorun_version_read_failure_exits_normally(self, capsys):
        """Autorun ran but version re-read failed (None) → no upgrade exit."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_autorun_phase("success"),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check.capture_startup_version",
                                        return_value="0.2.326",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.post_autorun_version_check."
                                            "check_post_autorun_version",
                                            return_value=None,
                                        ) as mock_check:
                                            commands.setup_cmd()  # Should not raise
        mock_check.assert_called_once_with("0.2.326")

    def test_post_autorun_skipped_does_not_check_version(self, capsys):
        """Autorun was skipped → version check is not invoked (no upgrade exit)."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_autorun_phase("skipped"),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check."
                                        "check_post_autorun_version",
                                    ) as mock_check:
                                        commands.setup_cmd()  # Should not raise
        mock_check.assert_not_called()

    def test_pre_invocation_failure_does_not_check_version(self, capsys):
        """Pre-invocation failure (child not started) → version check not invoked, exit 6."""

        def _pre_invocation_failure(**kwargs) -> bool:
            """Simulate a worktree-add failure: records 'failed' but child was not invoked."""
            from agentic_devtools.cli.setup.report import PhaseResult

            kwargs["report"].record(
                PhaseResult(
                    name=AUTORUN_SETUP_PHASE,
                    status="failed",
                    error="Could not create worktree for branch 'chore/agdt-setup-1.0': ...",
                )
            )
            return False  # child was NOT invoked

        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_pre_invocation_failure,
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check."
                                        "check_post_autorun_version",
                                    ) as mock_check:
                                        with patch(
                                            "agentic_devtools.cli.setup.report.write_report",
                                            return_value=True,
                                        ):
                                            with pytest.raises(SystemExit) as exc_info:
                                                commands.setup_cmd()
        # Pre-invocation failure → exit 6 (AUTORUN_FAILED) but version check not called.
        assert exc_info.value.code == 6
        mock_check.assert_not_called()

    def test_post_autorun_failed_unchanged_exits_autorun_failed(self, capsys):
        """Autorun failed and version is unchanged → exit 6, not the upgrade exit."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_autorun_phase("failed"),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check.capture_startup_version",
                                        return_value="0.2.326",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.post_autorun_version_check."
                                            "check_post_autorun_version",
                                            return_value="0.2.326",
                                        ) as mock_check:
                                            with patch(
                                                "agentic_devtools.cli.setup.report.write_report",
                                                return_value=True,
                                            ):
                                                with pytest.raises(SystemExit) as exc_info:
                                                    commands.setup_cmd()
        assert exc_info.value.code == 6
        mock_check.assert_called_once_with("0.2.326")
        assert "re-run" not in capsys.readouterr().err.lower()


class TestSetupCmdBranchCreatedPropagation:
    """Tests verifying branch_created is correctly propagated to _autorun_setup_dev_tools."""

    def test_passes_branch_created_none_when_pr_workflow_skipped(self, capsys, tmp_path):
        """When use_pr_workflow=False, branch_created=None is passed to autorun."""
        with patch("sys.argv", ["agdt-setup", "--skip-pr-workflow"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                        return_value=True,
                                    ):
                                        with patch.object(commands, "_prompt_project_config"):
                                            with patch.object(commands, "_prompt_copilot_model"):
                                                with patch(
                                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                                ) as mock_autorun:
                                                    commands.setup_cmd()
        mock_autorun.assert_called_once()
        assert mock_autorun.call_args[1]["branch_created"] is None

    def test_passes_extracted_branch_name_when_pr_workflow_creates_branch(self, capsys, tmp_path):
        """When use_pr_workflow=True and pr_result has branch_created, it is forwarded."""
        from agentic_devtools.cli.setup.pr_workflow import PrWorkflowResult

        mock_result = PrWorkflowResult(
            success=True,
            branch_created="chore/agdt-setup-0.1.0",
            pr_created=True,
            message="PR created from branch 'chore/agdt-setup-0.1.0'.",
        )
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                        return_value=True,
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow",
                                            return_value=mock_result,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                                    ) as mock_autorun:
                                                        commands.setup_cmd()
        mock_autorun.assert_called_once()
        assert mock_autorun.call_args[1]["branch_created"] == "chore/agdt-setup-0.1.0"

    def test_passes_none_when_pr_result_branch_created_is_none(self, capsys, tmp_path):
        """When pr_result has branch_created=None, None is forwarded."""
        from agentic_devtools.cli.setup.pr_workflow import PrWorkflowResult

        mock_result = PrWorkflowResult(
            success=True,
            branch_created=None,
            pr_created=False,
            message="No changes detected.",
        )
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                    with patch(
                                        "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                        return_value=True,
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.pr_workflow.run_setup_with_pr_workflow",
                                            return_value=mock_result,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                                    ) as mock_autorun:
                                                        commands.setup_cmd()
        mock_autorun.assert_called_once()
        assert mock_autorun.call_args[1]["branch_created"] is None


class TestSetupCmdExplicitRunPropagation:
    """Tests verifying the explicit --run flag reaches _autorun_setup_dev_tools."""

    @pytest.fixture(autouse=True)
    def _isolate(self):
        """Keep repo mutation and the PR workflow out of these tests."""
        with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
            with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=False):
                with patch(
                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                    return_value=(False, InjectionSummary(injected=0, pruned=0)),
                ):
                    with patch.object(commands, "_populate_available_models"):
                        yield

    def _run(self, argv: list[str]):
        with patch("sys.argv", argv):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                ) as mock_autorun:
                                    commands.setup_cmd()
        return mock_autorun

    def test_explicit_run_true_with_run_flag(self):
        """--run marks the auto-run request as explicit (overrides suppression)."""
        mock_autorun = self._run(["agdt-setup", "--run"])

        assert mock_autorun.call_args[1]["explicit_run"] is True

    def test_explicit_run_false_by_default(self):
        """Without --run the auto-run request is not explicit."""
        mock_autorun = self._run(["agdt-setup"])

        assert mock_autorun.call_args[1]["explicit_run"] is False

    def test_explicit_run_false_with_no_run_flag(self):
        """--no-run never marks the request as explicit."""
        mock_autorun = self._run(["agdt-setup", "--no-run"])

        assert mock_autorun.call_args[1]["explicit_run"] is False


class TestSetupCmdAutorunFailurePropagation:
    """Tests for propagating a failed auto-run to the process exit code."""

    @pytest.fixture(autouse=True)
    def _isolate(self):
        """Keep repo mutation and the PR workflow out of these tests."""
        with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
            with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=False):
                with patch(
                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                    return_value=(False, InjectionSummary(injected=0, pruned=0)),
                ):
                    with patch.object(commands, "_populate_available_models"):
                        yield

    def _run_with_autorun_status(self, status: str, post_version: str | None = "0.2.326"):
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_autorun_phase(status),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check.capture_startup_version",
                                        return_value="0.2.326",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.post_autorun_version_check."
                                            "check_post_autorun_version",
                                            return_value=post_version,
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.setup.report.write_report",
                                                return_value=True,
                                            ) as mock_write:
                                                with pytest.raises(SystemExit) as exc_info:
                                                    commands.setup_cmd()
        return exc_info, mock_write

    def test_failed_autorun_exits_autorun_failed(self):
        """A failed auto-run exits with AUTORUN_FAILED (6)."""
        exc_info, _ = self._run_with_autorun_status("failed")

        assert exc_info.value.code == 6

    def test_failed_autorun_reports_error_and_report_path(self, capsys):
        """The failure message names the failure and where the report was written."""
        from agentic_devtools.cli.setup.report import _resolve_report_path

        self._run_with_autorun_status("failed")

        err = capsys.readouterr().err
        assert "setup-dev-tools.py failed" in err
        assert str(_resolve_report_path(None)) in err

    def test_failed_autorun_surfaces_recorded_error(self, capsys):
        """When the phase recorded an error, that error is shown to the user."""

        def _record_failure(**kwargs) -> None:
            from agentic_devtools.cli.setup.report import PhaseResult

            kwargs["report"].record(PhaseResult(name=AUTORUN_SETUP_PHASE, status="failed", error="exit code 3"))

        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_failure,
                                ):
                                    with patch(
                                        "agentic_devtools.cli.setup.post_autorun_version_check."
                                        "check_post_autorun_version",
                                        return_value=None,
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.setup.report.write_report",
                                            return_value=True,
                                        ):
                                            with pytest.raises(SystemExit) as exc_info:
                                                commands.setup_cmd()

        assert exc_info.value.code == 6
        assert "exit code 3" in capsys.readouterr().err

    def test_failed_autorun_records_exit_code_in_report(self):
        """The persisted report carries the AUTORUN_FAILED classification."""
        _, mock_write = self._run_with_autorun_status("failed")

        report = mock_write.call_args[0][0]
        assert report.exit_code == 6
        assert report.exit_code_name == "AUTORUN_FAILED"
        assert "autorun_error" in report.details

    def test_version_change_takes_precedence_over_failure(self, capsys):
        """A version change after a failed auto-run still signals UPGRADED_RERUN_NEEDED."""
        exc_info, _ = self._run_with_autorun_status("failed", post_version="0.2.330")

        assert exc_info.value.code == 4
        assert "0.2.330" in capsys.readouterr().err

    def test_skipped_autorun_does_not_fail_setup(self):
        """A skipped auto-run leaves the exit code untouched."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch(
                                    "agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools",
                                    side_effect=_record_autorun_phase("skipped"),
                                ):
                                    commands.setup_cmd()  # Should not raise


class TestSetupCmdPhaseMarkers:
    """Tests for the generation phase markers emitted by setup_cmd."""

    @pytest.fixture(autouse=True)
    def _isolate(self):
        """Keep repo mutation and the PR workflow out of these tests."""
        with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
            with patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=False):
                with patch(
                    "agentic_devtools.skill_injector.inject_skills_with_summary",
                    return_value=(False, InjectionSummary(injected=0, pruned=0)),
                ):
                    with patch.object(commands, "_populate_available_models"):
                        yield

    def test_generation_markers_bracket_the_run(self, capsys):
        """generation:start/end are emitted exactly once, in order."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with patch("agentic_devtools.cli.setup.autorun._autorun_setup_dev_tools"):
                                    commands.setup_cmd()

        out = capsys.readouterr().out
        assert out.count(GENERATION_START) == 1
        assert out.count(GENERATION_END) == 1
        assert out.index(GENERATION_START) < out.index(GENERATION_END)

    def test_generation_end_emitted_on_early_exit(self, capsys):
        """An early exit still closes the generation phase for log parsers."""
        with patch("sys.argv", ["agdt-setup"]):
            with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                with patch.object(commands, "install_copilot_cli", return_value=True):
                    with patch.object(commands, "install_gh_cli", return_value=True):
                        with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(False)):
                            with patch.object(commands, "_persist_env_vars_to_profile"):
                                with pytest.raises(SystemExit) as exc_info:
                                    commands.setup_cmd()

        assert exc_info.value.code == 2
        out = capsys.readouterr().out
        assert out.count(GENERATION_START) == 1
        assert out.count(GENERATION_END) == 1
