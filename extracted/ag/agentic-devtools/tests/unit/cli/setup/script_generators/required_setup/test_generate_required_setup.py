"""Tests for generate_required_setup_script."""

import io
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.git_hooks_policy import (
    HOOKS_DISABLED_MESSAGE,
    NON_BOOLEAN_WARNING_PREFIX,
    PRESERVED_MESSAGE_PREFIX,
    PRESERVED_MESSAGE_SUFFIX,
    format_preserved_message,
)
from agentic_devtools.cli.setup.script_generators.required_setup import (
    SELF_UPGRADE_LOCK_MESSAGE,
    SELF_UPGRADE_LOCK_REMEDY_TEMPLATE,
    generate_required_setup_script,
)

WINERROR_32_OUTPUT = (
    "ERROR: Could not install packages due to an OSError: [WinError 32] The process "
    "cannot access the file because it is being used by another process: "
    r"'c:\users\dev\appdata\roaming\python\python313\scripts\agdt-setup.exe'"
)

OTHER_EXE_LOCK_OUTPUT = (
    "ERROR: Could not install packages due to an OSError: [WinError 32] The process "
    "cannot access the file because it is being used by another process: "
    r"'c:\users\dev\appdata\roaming\python\python313\scripts\python.exe'"
)


class _FakePopen:
    def __init__(self, *, returncode: int, stdout: str, stderr: str) -> None:
        self._returncode = returncode
        self.stdout = io.StringIO(stdout)
        self.stderr = io.StringIO(stderr)

    def wait(self) -> int:
        return self._returncode


def _template_namespace() -> dict:
    """Execute the generated script's module body (``main()`` is guarded)."""
    namespace: dict = {}
    exec(compile(generate_required_setup_script(), "<generated>", "exec"), namespace)
    return namespace


def _write_project_config(git_root: Path, payload: object) -> None:
    config_path = git_root / ".agdt" / "config" / "project.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(payload), encoding="utf-8")


class TestGenerateRequiredSetup:
    """Tests for generate_required_setup_script."""

    def test_output_is_string(self):
        """Returns a non-empty string."""
        script = generate_required_setup_script()
        assert isinstance(script, str)
        assert len(script) > 0

    def test_has_shebang(self):
        """Script starts with a shebang line."""
        script = generate_required_setup_script()
        assert script.startswith("#!/usr/bin/env python3")

    def test_contains_corruption_detection(self):
        """Script contains corruption detection logic."""
        script = generate_required_setup_script()
        assert "_detect_corrupted_artifacts" in script

    def test_contains_cleanup(self):
        """Script contains cleanup logic."""
        script = generate_required_setup_script()
        assert "_cleanup_artifacts" in script

    def test_contains_install(self):
        """Script contains install logic."""
        script = generate_required_setup_script()
        assert "pip" in script
        assert "install" in script

    def test_contains_git_hooks(self):
        """Script contains git hooks setup."""
        script = generate_required_setup_script()
        assert "core.hooksPath" in script

    def test_contains_foreground_flag(self):
        """Script supports --foreground flag."""
        script = generate_required_setup_script()
        assert "--foreground" in script

    def test_stdlib_only(self):
        """Script does not import agentic_devtools."""
        script = generate_required_setup_script()
        assert "import agentic_devtools" not in script
        assert "from agentic_devtools" not in script

    def test_uses_pathlib(self):
        """Script uses pathlib.Path for cross-platform paths."""
        script = generate_required_setup_script()
        assert "from pathlib import Path" in script

    def test_reads_project_config_for_the_toggle(self):
        """Script reads .agdt/config/project.json stdlib-only."""
        script = generate_required_setup_script()
        assert "import json" in script
        assert "manage_git_hooks" in script
        assert "project.json" in script

    def test_messages_match_the_policy_module(self):
        """The embedded copy must stay behaviourally in sync with git_hooks_policy."""
        namespace = _template_namespace()
        assert namespace["_HOOKS_DISABLED_MESSAGE"] == HOOKS_DISABLED_MESSAGE
        assert namespace["_PRESERVED_MESSAGE_PREFIX"] == PRESERVED_MESSAGE_PREFIX
        assert namespace["_PRESERVED_MESSAGE_SUFFIX"] == PRESERVED_MESSAGE_SUFFIX
        assert namespace["_NON_BOOLEAN_WARNING_PREFIX"] == NON_BOOLEAN_WARNING_PREFIX

    def test_self_upgrade_lock_messages_match_the_module(self):
        """The embedded copy must stay in sync with the module constants."""
        namespace = _template_namespace()
        assert namespace["_SELF_UPGRADE_LOCK_MESSAGE"] == SELF_UPGRADE_LOCK_MESSAGE
        remedy = namespace["_SELF_UPGRADE_LOCK_REMEDY"]
        assert f'& "{sys.executable}"' in remedy, "remedy must quote runtime sys.executable for PowerShell"
        assert "--upgrade agentic-devtools" in remedy
        assert "--user" not in remedy, "remedy must not use --user (invalid in isolated envs)"
        assert SELF_UPGRADE_LOCK_REMEDY_TEMPLATE.replace("<sys.executable>", sys.executable) == remedy

    def test_does_not_overwrite_a_foreign_hooks_path(self):
        """The embedded setup no longer announces an overwrite."""
        script = generate_required_setup_script()
        assert "Overwriting" not in script


class TestTemplateGitHooksManagementEnabled:
    """Behaviour of the embedded, stdlib-only project-config reader."""

    def _enabled(self, git_root: Path) -> bool:
        return _template_namespace()["_git_hooks_management_enabled"](git_root)

    def test_missing_config_defaults_to_enabled(self, tmp_path: Path) -> None:
        """No project.json → enabled."""
        assert self._enabled(tmp_path) is True

    def test_absent_and_null_keys_default_to_enabled(self, tmp_path: Path) -> None:
        """Absent or null key → enabled."""
        _write_project_config(tmp_path, {"other": 1})
        assert self._enabled(tmp_path) is True
        _write_project_config(tmp_path, {"manage_git_hooks": None})
        assert self._enabled(tmp_path) is True

    def test_explicit_booleans(self, tmp_path: Path) -> None:
        """Explicit booleans are honoured."""
        _write_project_config(tmp_path, {"manage_git_hooks": True})
        assert self._enabled(tmp_path) is True
        _write_project_config(tmp_path, {"manage_git_hooks": False})
        assert self._enabled(tmp_path) is False

    def test_malformed_json_defaults_to_enabled(self, tmp_path: Path) -> None:
        """Malformed JSON → enabled, no exception."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("{not json", encoding="utf-8")
        assert self._enabled(tmp_path) is True

    def test_non_dict_root_defaults_to_enabled(self, tmp_path: Path) -> None:
        """Non-object JSON root → enabled."""
        _write_project_config(tmp_path, ["manage_git_hooks"])
        assert self._enabled(tmp_path) is True

    def test_non_boolean_warns_and_defaults_to_enabled(self, tmp_path: Path, capsys) -> None:
        """A non-boolean value warns on stderr and is treated as enabled."""
        _write_project_config(tmp_path, {"manage_git_hooks": "false"})

        assert self._enabled(tmp_path) is True

        assert NON_BOOLEAN_WARNING_PREFIX in capsys.readouterr().err


class TestTemplateSetupGitHooks:
    """The embedded writer must behave exactly like ``setup_git_hooks()``."""

    def _run(self, namespace: dict, side_effect: list) -> MagicMock:
        mock_run = MagicMock(side_effect=side_effect)
        with patch.object(namespace["subprocess"], "run", mock_run):
            namespace["_setup_git_hooks"]()
        return mock_run

    def test_preserves_foreign_hooks_path(self, tmp_path: Path, capsys) -> None:
        """Prints exactly the two-line preserved notice and writes nothing."""
        namespace = _template_namespace()
        mock_run = self._run(
            namespace,
            [
                MagicMock(returncode=0, stdout=".git\n"),
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),
                MagicMock(returncode=0, stdout=".husky/_\n"),
            ],
        )

        assert mock_run.call_count == 3
        assert not (tmp_path / ".githooks").exists()
        assert capsys.readouterr().out == format_preserved_message(".husky/_") + "\n"

    def test_skips_when_disabled_by_project_config(self, tmp_path: Path, capsys) -> None:
        """The toggle short-circuits before core.hooksPath is read."""
        _write_project_config(tmp_path, {"manage_git_hooks": False})
        namespace = _template_namespace()
        mock_run = self._run(
            namespace,
            [
                MagicMock(returncode=0, stdout=".git\n"),
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),
            ],
        )

        assert mock_run.call_count == 2
        assert not (tmp_path / ".githooks").exists()
        assert capsys.readouterr().out == HOOKS_DISABLED_MESSAGE + "\n"

    def test_sets_hooks_path_when_unset(self, tmp_path: Path, capsys) -> None:
        """Unset hooks path is configured and .githooks/ is created."""
        namespace = _template_namespace()
        self._run(
            namespace,
            [
                MagicMock(returncode=0, stdout=".git\n"),
                MagicMock(returncode=0, stdout=str(tmp_path) + "\n"),
                MagicMock(returncode=1, stdout=""),
                MagicMock(returncode=0),
            ],
        )

        assert (tmp_path / ".githooks").is_dir()
        assert capsys.readouterr().out == "  ✓ core.hooksPath set to '.githooks'\n"

    def test_reports_when_not_a_git_repository(self, capsys) -> None:
        """Outside a git repo the embedded writer skips and says so."""
        namespace = _template_namespace()
        self._run(namespace, [subprocess.CalledProcessError(128, "git")])

        assert "Not a git repository" in capsys.readouterr().out


class TestTemplateInstallPackage:
    """The embedded installer must classify the Windows console-script lock."""

    def _install(self, namespace: dict, returncode: int, stdout: str, stderr: str):
        with patch.object(
            namespace["subprocess"],
            "Popen",
            return_value=_FakePopen(returncode=returncode, stdout=stdout, stderr=stderr),
        ):
            return namespace["_install_package"]()

    def test_success(self, capsys) -> None:
        """A successful upgrade streams stdout and reports no lock."""
        namespace = _template_namespace()

        assert self._install(namespace, 0, "Successfully installed\n", "") == (True, False)
        assert capsys.readouterr().out == "Successfully installed\n"

    def test_self_upgrade_lock_is_flagged(self) -> None:
        """WinError 32 on a console script is reported as a recoverable lock."""
        namespace = _template_namespace()

        assert self._install(namespace, 1, "", WINERROR_32_OUTPUT) == (False, True)

    def test_other_executable_lock_is_not_flagged(self) -> None:
        """A different locked executable remains a fatal pip failure."""
        namespace = _template_namespace()

        assert self._install(namespace, 1, "", OTHER_EXE_LOCK_OUTPUT) == (False, False)

    def test_other_failure_is_not_flagged(self) -> None:
        """Unrelated pip failures stay fatal."""
        namespace = _template_namespace()

        assert self._install(namespace, 1, "", "ERROR: No matching distribution found") == (False, False)

    def test_failure_streams_stderr(self, capsys) -> None:
        """The embedded installer preserves pip stderr instead of echoing on stdout."""
        namespace = _template_namespace()

        assert self._install(namespace, 1, "", "ERROR: Could not install\n") == (False, False)
        assert capsys.readouterr().err == "ERROR: Could not install\n"

    def test_windows_autorun_skips_popen(self, monkeypatch) -> None:
        """Windows autorun short-circuits before launching pip."""
        namespace = _template_namespace()
        monkeypatch.setattr(namespace["sys"], "platform", "win32", raising=False)
        monkeypatch.setenv("AGDT_SETUP_AUTORUN", "1")

        with patch.object(namespace["subprocess"], "Popen") as mock_popen:
            assert namespace["_install_package"]() == (False, True)

        mock_popen.assert_not_called()


class TestTemplateDetectCorruptedArtifacts:
    """The embedded corruption scanner must stay aligned with the source helper."""

    def test_detects_dev_local_backup_and_skips_unrelated_name(self, tmp_path: Path) -> None:
        """The embedded scanner keeps the backup match broad without overmatching extras."""
        namespace = _template_namespace()
        sp = tmp_path / "site-packages"
        sp.mkdir()
        (sp / "~gentic_devtools-0.2.9.dev1+g1234abc.dist-info").mkdir()
        (sp / "~gentic-devtools-2-extra-1.0.dist-info").mkdir()
        (sp / "~gentic-devtools-extra-1.0.0.dist-info").mkdir()
        (sp / "agentic-devtools-extra-1.0.0.dist-info").mkdir()
        (sp / "agentic-devtools-2-extra-1.0.dist-info").mkdir()
        namespace["_site_packages_dirs"] = lambda: [str(sp)]

        artifacts = namespace["_detect_corrupted_artifacts"]()

        assert [artifact.name for artifact in artifacts] == ["~gentic_devtools-0.2.9.dev1+g1234abc.dist-info"]


class TestTemplateMain:
    """The embedded ``main()`` must not abort on a recoverable self-upgrade lock."""

    def _run_main(self, namespace: dict, install_result: tuple[bool, bool]) -> None:
        namespace["_detect_corrupted_artifacts"] = lambda: []
        namespace["_install_package"] = lambda: install_result
        namespace["_setup_git_hooks"] = lambda: None
        with patch.object(sys, "argv", ["agentic-devtools-required-setup.py", "--foreground"]):
            namespace["main"]()

    def test_self_upgrade_lock_continues(self, capsys) -> None:
        """The lock warns with remediation and required setup still completes."""
        namespace = _template_namespace()

        self._run_main(namespace, (False, True))

        captured = capsys.readouterr()
        assert namespace["_SELF_UPGRADE_LOCK_MESSAGE"] in captured.err
        assert namespace["_SELF_UPGRADE_LOCK_REMEDY"] in captured.err
        assert "Required Setup Complete" in captured.out

    def test_other_install_failure_still_exits(self, capsys) -> None:
        """A non-lock install failure remains fatal."""
        namespace = _template_namespace()

        with pytest.raises(SystemExit) as excinfo:
            self._run_main(namespace, (False, False))

        assert excinfo.value.code == 1
        assert "Failed to install agentic-devtools" in capsys.readouterr().err

    def test_successful_install_completes(self, capsys) -> None:
        """A successful upgrade prints the success line."""
        namespace = _template_namespace()

        self._run_main(namespace, (True, False))

        assert "installed/upgraded successfully" in capsys.readouterr().out
