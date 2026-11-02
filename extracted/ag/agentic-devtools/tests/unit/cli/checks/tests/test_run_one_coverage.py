"""Tests for run_one_coverage."""

from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired
from unittest.mock import patch

from agentic_devtools.cli.checks.tests import run_one_coverage
from agentic_devtools.cli.checks.xdist_policy import get_xdist_args

MODULE = "agentic_devtools.cli.checks.tests"


class TestRunOneCoverage:
    """Tests for run_one_coverage."""

    def test_no_test_path_returns_fail(self, tmp_path):
        passed, output = run_one_coverage("agentic_devtools/missing.py", cwd=tmp_path)
        assert passed is False
        assert "No tests found" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_coverage_passes(self, mock_run, tmp_path):
        # Create unit test dir structure
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")

        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="1 passed\nCoverage: 100%\n", stderr="")
        passed, output = run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)
        assert passed is True
        assert "mymod.py" in output
        assert "FAIL" not in output

    @patch(f"{MODULE}.subprocess.run")
    def test_coverage_fails(self, mock_run, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")

        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout="Coverage: 85%\n", stderr="")
        passed, output = run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)
        assert passed is False
        assert "FAIL" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_selected_test_path_with_zero_executed_tests_fails(self, mock_run, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_empty.py").write_text("VALUE = 1\n", encoding="utf-8")
        mock_run.return_value = CompletedProcess(args=[], returncode=5, stdout="no tests ran\n", stderr="")

        passed, output = run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)

        assert passed is False
        assert "no tests ran" in output
        assert "FAIL" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_includes_stderr_in_output(self, mock_run, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")

        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="ok\n", stderr="warning here\n")
        passed, output = run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)
        assert "warning here" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_uses_cov_module_with_dots(self, mock_run, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "cli" / "git" / "core"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")

        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        run_one_coverage("agentic_devtools/cli/git/core.py", cwd=tmp_path)
        args = mock_run.call_args[0][0]
        cov_arg = [a for a in args if a.startswith("--cov=")]
        assert cov_arg[0] == "--cov=agentic_devtools.cli.git.core"

    @patch(f"{MODULE}.subprocess.run")
    def test_bundled_fingerprint_uses_script_tests(self, mock_run, tmp_path):
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        passed, _ = run_one_coverage("agentic_devtools/_bundled_skills/skills/fingerprint.py", cwd=tmp_path)

        assert passed is True
        assert mock_run.call_args.args[0][3] == str(tmp_path / "tests" / "scripts" / "fingerprint")

    @patch(f"{MODULE}.subprocess.run")
    def test_coverage_file_env_isolated(self, mock_run, tmp_path, monkeypatch):
        monkeypatch.setenv("GIT_DIR", "sentinel")
        monkeypatch.setenv("GIT_CONFIG_VALUE_7", "true")
        monkeypatch.delenv("COVERAGE_CORE", raising=False)
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")

        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="ok\n", stderr="")
        run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)
        env = mock_run.call_args.kwargs["env"]
        assert "GIT_DIR" not in env
        assert "GIT_CONFIG_VALUE_7" not in env
        assert "COVERAGE_FILE" in env
        assert ".coverage" in env["COVERAGE_FILE"]
        assert env["COVERAGE_CORE"] == "sysmon"

    @patch(f"{MODULE}.subprocess.run")
    def test_preserves_user_coverage_core(self, mock_run, tmp_path, monkeypatch):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")
        monkeypatch.setenv("COVERAGE_CORE", "ctrace")
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)

        assert mock_run.call_args.kwargs["env"]["COVERAGE_CORE"] == "ctrace"

    @patch(f"{MODULE}.subprocess.run")
    def test_empty_coverage_core_defaults_to_sysmon(self, mock_run, tmp_path, monkeypatch):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")
        monkeypatch.setenv("COVERAGE_CORE", "")
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)

        assert mock_run.call_args.kwargs["env"]["COVERAGE_CORE"] == "sysmon"

    @patch(f"{MODULE}.subprocess.run")
    def test_disables_pytest_cache_and_uses_isolated_basetemp(self, mock_run, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)

        args = mock_run.call_args.args[0]
        assert args[args.index("-p") + 1] == "no:cacheprovider"
        assert any(arg.startswith("--basetemp=") for arg in args)

    @patch(f"{MODULE}.subprocess.run")
    def test_uses_xdist_for_large_mapped_test_directory(self, mock_run, tmp_path, monkeypatch):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        for index in range(31):
            (test_dir / f"test_{index}.py").touch()
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        def get_xdist_args_with_fixed_cpu_count(path: Path, *, coverage_workers: int) -> list[str]:
            return get_xdist_args(path, coverage_workers=coverage_workers, cpu_count=16)

        monkeypatch.setattr(f"{MODULE}.get_xdist_args", get_xdist_args_with_fixed_cpu_count)
        run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path, coverage_workers=2)

        args = mock_run.call_args.args[0]
        assert args[args.index("-n") + 1] == "4"
        assert args[args.index("--dist") + 1] == "loadfile"

    @patch(f"{MODULE}.subprocess.run")
    def test_temp_coverage_directory_is_cleaned_up(self, mock_run, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="ok\n", stderr="")

        run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)
        cov_file = mock_run.call_args.kwargs["env"]["COVERAGE_FILE"]
        assert not Path(cov_file).parent.exists()

    @patch(f"{MODULE}.subprocess.run")
    def test_timeout_returns_failure(self, mock_run, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "mymod"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("# test")

        mock_run.side_effect = TimeoutExpired(cmd=["pytest"], timeout=300)

        passed, output = run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)

        assert passed is False
        assert "timed out" in output
        assert mock_run.call_args.kwargs["timeout"] == 900

    @patch(f"{MODULE}.subprocess.run")
    def test_legacy_test_file_fallback(self, mock_run, tmp_path):
        # No unit test dir, but legacy test file exists
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_mymod.py").write_text("# legacy test")

        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="ok\n", stderr="")
        passed, output = run_one_coverage("agentic_devtools/mymod.py", cwd=tmp_path)
        assert passed is True

    def test_defaults_to_cwd(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        passed, output = run_one_coverage("agentic_devtools/missing.py")
        assert passed is False
        assert "No tests found" in output
