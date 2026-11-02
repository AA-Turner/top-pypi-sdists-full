"""Tests for setup expectations orchestration."""

from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.expectations_specializer import SpecializationResult, _StartupFingerprintState


def _args() -> Namespace:
    return Namespace(
        system_only=False,
        no_verify_ssl=False,
        no_persist_env=False,
        overwrite_env=False,
        skip_platform_detection=False,
        issue_adapter=None,
        skip_templates=False,
        reconfigure=False,
        defaults=False,
        skip_pr_workflow=False,
        force_old_version=False,
        npm=False,
        no_npm=False,
        cli_run=None,
        cli_no_run=None,
        autorun_enabled=None,
        refresh_issue_types=False,
        dry_run=False,
        yes=False,
    )


class TestSpecializeSetupExpectations:
    """Verify specialization is wired into setup orchestration."""

    def test_skips_without_repository_steps(self, capsys) -> None:
        """Missing repository or skipped repository steps logs a skip."""
        commands._specialize_setup_expectations(
            None, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
        )
        commands._specialize_setup_expectations(
            Path("/repo"), _args(), npm_enabled=False, skip_repo_steps=True, startup_fingerprint=None
        )
        assert capsys.readouterr().out.count("specialization skipped") == 2

    def test_skips_without_repository_steps_warns_on_cleanup_failure(self, capsys) -> None:
        """A warning is emitted if stale artifact cleanup fails on skip."""
        with patch(
            "agentic_devtools.cli.setup.expectations_specializer.cleanup_specialized_output",
            return_value=SpecializationResult(status="error", reason="cleanup failed"),
        ):
            commands._specialize_setup_expectations(
                None, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
            assert "Failed to clean up stale" in capsys.readouterr().err

    def test_skip_path_uses_specialization_transaction(self, tmp_path: Path) -> None:
        """Early skip cleanup goes through the fingerprint-safe specialization path."""
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.cleanup_specialized_output",
                return_value=SpecializationResult(status="skipped", reason="skipped"),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                None, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        mock_run.assert_called_once_with(
            tmp_path,
            status="skipped",
            reason="Setup expectations specialization skipped (repository steps are skipped)",
            startup_fingerprint=None,
        )

    def test_skips_without_repository_steps_warns_on_state_dir_oserror(self, capsys) -> None:
        """An OSError during early-skip cleanup is reported as a warning."""
        from unittest.mock import patch

        with patch("agentic_devtools.state.get_state_dir", side_effect=OSError("mock")):
            commands._specialize_setup_expectations(
                None, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
            captured = capsys.readouterr()
        assert "specialization skipped" in captured.out
        assert "Failed to clean up stale" in captured.err
        assert "mock" in captured.err

    def test_logs_success(self, capsys, tmp_path: Path) -> None:
        """Successful specialization logs the generated artifact."""
        repo_root = tmp_path / "repo"
        (repo_root / ".github").mkdir(parents=True)
        (repo_root / ".github" / "agdt-config.json").write_text(
            '{"platform": {"issue_adapter": "github"}}',
            encoding="utf-8",
        )
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value="https://github.com/example/project.git",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ),
        ):
            commands._specialize_setup_expectations(
                repo_root, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        assert "Wrote repository-specialized setup expectations" in capsys.readouterr().out

    def test_uses_azure_devops_remote_identifier(self, tmp_path: Path) -> None:
        """An Azure DevOps origin uses the supported org/project identifier."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value="git@ssh.dev.azure.com:v3/myorg/myproject/myrepo",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        config = mock_run.call_args.args[0]
        assert config.repo == "myorg/myproject"

    def test_uses_github_enterprise_remote_identifier(self, tmp_path: Path) -> None:
        """A GitHub Enterprise origin keeps the ``owner/repo`` slug."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value="git@ghe.example.com:swai-factory/agentic-devtools.git",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        config = mock_run.call_args.args[0]
        assert config.repo == "swai-factory/agentic-devtools"

    def test_uses_generic_scp_remote_without_user(self, tmp_path: Path) -> None:
        """A userless scp-style origin still yields an ``owner/repo`` slug."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value="github.com:swai-factory/agentic-devtools.git",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        config = mock_run.call_args.args[0]
        assert config.repo == "swai-factory/agentic-devtools"

    def test_unrecognized_remote_falls_back_to_local_slug(self, tmp_path: Path) -> None:
        """An unsupported remote format falls back to the sanitized local slug."""
        repo_root = tmp_path / "odd checkout (2)"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value="file:///tmp/repositories/agentic-devtools",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        config = mock_run.call_args.args[0]
        assert config.repo == "local/odd-checkout-2"

    def test_sanitizes_nonstandard_repository_directory(self, tmp_path: Path) -> None:
        """A non-standard checkout directory still produces a valid fallback slug."""
        repo_root = tmp_path / "odd checkout (2)"
        (repo_root / ".github").mkdir(parents=True)
        (repo_root / ".github" / "agdt-config.json").write_text('{"platform": []}', encoding="utf-8")
        with (
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="skipped", reason="missing"),
            ),
        ):
            commands._specialize_setup_expectations(
                repo_root,
                _args(),
                npm_enabled=False,
                skip_repo_steps=False,
                startup_fingerprint=None,
            )

    def test_logs_skip_and_error(self, capsys, tmp_path: Path) -> None:
        """Skip and error results are logged without raising."""
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                side_effect=[
                    SpecializationResult(status="skipped", reason="missing"),
                    SpecializationResult(status="error", reason="broken"),
                ],
            ),
        ):
            commands._specialize_setup_expectations(
                Path("/repo"), _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
            commands._specialize_setup_expectations(
                Path("/repo"), _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        captured = capsys.readouterr()
        assert "specialization skipped: missing" in captured.out
        assert "specialization failed: broken" in captured.err

    def test_uses_startup_state_dir_when_snapshot_is_available(self, tmp_path: Path) -> None:
        """A captured startup state dir takes precedence over a later state-dir re-resolution."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        startup_state_dir = tmp_path / "startup-state"
        with (
            patch("agentic_devtools.state.get_state_dir", side_effect=AssertionError("should not be called")),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root,
                _args(),
                npm_enabled=False,
                skip_repo_steps=False,
                startup_fingerprint=_StartupFingerprintState(
                    state_dir=startup_state_dir,
                    fingerprint=(1, 2, 3),
                ),
            )
        assert mock_run.call_args.args[1] == startup_state_dir

    def test_uses_resolved_platform_issue_adapter_when_resolved(self, tmp_path: Path) -> None:
        """A resolved-platform issue adapter is used when its marker is ``True``."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root,
                _args(),
                npm_enabled=False,
                skip_repo_steps=False,
                startup_fingerprint=None,
                resolved_platform={"issue_adapter": "github", "issue_adapter_resolved": True},
            )
        config = mock_run.call_args.args[0]
        assert config.issue_adapter == "github"

    def test_ignores_resolved_platform_issue_adapter_when_ambiguous(self, tmp_path: Path) -> None:
        """A resolved-platform issue adapter is ignored when unresolved (ambiguous default)."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root,
                _args(),
                npm_enabled=False,
                skip_repo_steps=False,
                startup_fingerprint=None,
                resolved_platform={"issue_adapter": "github", "issue_adapter_resolved": False},
            )
        config = mock_run.call_args.args[0]
        # The unresolved (ambiguous) persisted adapter must be ignored, falling
        # back to the "unresolved" value rather than the discarded "github" value.
        assert config.issue_adapter == "unresolved"

    def test_threads_version_pin_into_config(self, tmp_path: Path) -> None:
        """The resolved version pin is threaded into ``RepositoryConfiguration``."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root,
                _args(),
                npm_enabled=False,
                skip_repo_steps=False,
                startup_fingerprint=None,
                version_pin="1.2.3",
            )
        config = mock_run.call_args.args[0]
        assert config.version_pin == "1.2.3"

    def test_threads_effective_ssl_hosts_into_config(self, tmp_path: Path) -> None:
        """The config reuses the certificate phase's selected host set."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root,
                _args(),
                npm_enabled=True,
                skip_repo_steps=False,
                startup_fingerprint=None,
                ssl_hosts=("api.github.com", "jira.example.com", "registry.npmjs.org"),
            )
        config = mock_run.call_args.args[0]
        assert config.ssl_hosts == ("api.github.com", "jira.example.com", "registry.npmjs.org")

    def test_system_only_specialization_uses_empty_ssl_host_set(self, tmp_path: Path) -> None:
        """System-only mode reports no certificate-prefetch hosts."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        args = _args()
        args.system_only = True
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root,
                args,
                npm_enabled=True,
                skip_repo_steps=False,
                startup_fingerprint=None,
                ssl_hosts=("api.github.com", "jira.example.com", "registry.npmjs.org"),
            )
        config = mock_run.call_args.args[0]
        assert config.ssl_hosts == ()

    def test_records_resolved_setup_flags_in_metadata_config(self, tmp_path: Path) -> None:
        """The config carries both raw setup flags and resolved effective values."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        args = _args()
        args.no_verify_ssl = True
        args.overwrite_env = True
        args.skip_platform_detection = True
        args.issue_adapter = "github"
        args.skip_templates = True
        args.reconfigure = True
        args.defaults = True
        args.skip_pr_workflow = True
        args.force_old_version = True
        args.no_npm = True
        args.cli_no_run = True
        args.autorun_enabled = False
        args.refresh_issue_types = True
        args.yes = True
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root, args, npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        config = mock_run.call_args.args[0]
        assert config.effective_flags == {
            "--defaults": True,
            "--dry-run": False,
            "--force-old-version": True,
            "--issue-adapter": "github",
            "--no-npm": True,
            "--no-persist-env": False,
            "--no-run": True,
            "--no-refresh-models": False,
            "--no-verify-ssl": True,
            "--npm": False,
            "--overwrite-env": True,
            "--refresh-issue-types": True,
            "--reconfigure": True,
            "--run": False,
            "--skip-platform-detection": True,
            "--skip-pr-workflow": True,
            "--skip-templates": True,
            "--system-only": False,
            "--yes": True,
            "autorun_enabled": False,
            "npm_enabled": False,
        }

    def test_markdown_adapter_resolved_in_system_only_mode(self, tmp_path: Path) -> None:
        """``resolved_platform`` with the ``markdown`` adapter is forwarded to the config.

        ``_resolve_saved_injection_axes()`` silently drops non-filter-capable values
        (like ``markdown``) because they are not filter-capable for skill injection.
        When ``resolved_platform`` carries the raw persisted section (including
        ``issue_adapter_resolved: True``), ``_specialize_setup_expectations`` must use
        the ``markdown`` value rather than falling back to ``"unresolved"``.
        """
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        args = _args()
        args.system_only = True
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                return_value=tmp_path / "general.md",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.run_specialization",
                return_value=SpecializationResult(status="success", content=""),
            ) as mock_run,
        ):
            commands._specialize_setup_expectations(
                repo_root,
                args,
                npm_enabled=False,
                skip_repo_steps=False,
                startup_fingerprint=None,
                resolved_platform={"issue_adapter": "markdown", "issue_adapter_resolved": True},
            )
        config = mock_run.call_args.args[0]
        assert config.issue_adapter == "markdown"

    def test_exception_logs_warning_and_invokes_stale_cleanup(self, capsys, tmp_path: Path) -> None:
        """An unexpected exception emits a warning and removes any stale artifact."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.platform_detection._get_origin_remote_url",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.resolve_general_doc_path",
                side_effect=RuntimeError("path resolution failed"),
            ),
            patch.object(commands, "_cleanup_stale_specialization_artifact") as mock_cleanup,
        ):
            commands._specialize_setup_expectations(
                repo_root, _args(), npm_enabled=False, skip_repo_steps=False, startup_fingerprint=None
            )
        assert "specialization failed: path resolution failed" in capsys.readouterr().err
        mock_cleanup.assert_called_once()
