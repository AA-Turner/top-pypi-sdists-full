"""Tests for markdownlint_files."""

from __future__ import annotations

from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.cli.checks.lint import MARKDOWNLINT_INSTALL_HINT, markdownlint_files

MODULE = "agentic_devtools.cli.checks.lint"
NODE = "/usr/bin/node"
NPM = "/usr/bin/npm"

# npm root -g exit-code failures
_NPM_ROOT_FAIL = CompletedProcess(args=[], returncode=1, stdout="", stderr="npm error\n")


def _which(tool: str) -> str | None:
    """Side-effect that mimics both node and npm being on PATH."""
    return NODE if tool == "node" else NPM


def _make_entry(tmp_path, *, version: str = "0.17.2"):
    """Create a dummy pinned markdownlint-cli2 package in tmp_path and return its parent."""
    entry_dir = tmp_path / "markdownlint-cli2"
    entry_dir.mkdir(parents=True, exist_ok=True)
    (entry_dir / "markdownlint-cli2-bin.mjs").write_text("", encoding="utf-8")
    (entry_dir / "package.json").write_text(f'{{"version": "{version}"}}', encoding="utf-8")
    return str(tmp_path)


class TestMarkdownlintFiles:
    """Tests for markdownlint_files."""

    def test_empty_files_returns_pass(self):
        passed, output = markdownlint_files([])
        assert passed is True
        assert output == ""

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    @patch(f"{MODULE}.subprocess.run")
    def test_all_files_deleted_returns_pass_without_running(self, mock_run, mock_which, tmp_path):
        """Markdown files removed by the change set are skipped, not failed."""
        passed, output = markdownlint_files(["docs/gone.md"], cwd=str(tmp_path))
        assert passed is True
        assert output == ""
        mock_run.assert_not_called()

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_success(self, mock_which, tmp_path):
        (tmp_path / "README.md").write_text("# Title\n", encoding="utf-8")
        root = _make_entry(tmp_path)
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [
                CompletedProcess(args=[], returncode=0, stdout=root, stderr=""),
                CompletedProcess(args=[], returncode=0, stdout="", stderr="Summary: 0 error(s)\n"),
            ]
            passed, output = markdownlint_files(["README.md"], cwd=str(tmp_path))
        assert passed is True
        assert "0 error(s)" in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_failure(self, mock_which, tmp_path):
        (tmp_path / "README.md").write_text("## Title\n", encoding="utf-8")
        root = _make_entry(tmp_path)
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [
                CompletedProcess(args=[], returncode=0, stdout=root, stderr=""),
                CompletedProcess(args=[], returncode=1, stdout="README.md:1 MD041/first-line-heading\n", stderr=""),
            ]
            passed, output = markdownlint_files(["README.md"], cwd=str(tmp_path))
        assert passed is False
        assert "MD041" in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_uses_no_globs_and_colon_prefixed_paths(self, mock_which, tmp_path):
        """Lint call uses node + entry-point, --no-globs, and colon-prefixed paths."""
        for name in ("a.md", "b.md"):
            (tmp_path / name).write_text("# Title\n", encoding="utf-8")
        root = _make_entry(tmp_path)
        entry_point = str(tmp_path / "markdownlint-cli2" / "markdownlint-cli2-bin.mjs")
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [
                CompletedProcess(args=[], returncode=0, stdout=root, stderr=""),
                CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
            ]
            markdownlint_files(["a.md", "b.md", "deleted.md"], cwd=str(tmp_path))
            lint_args = mock_sub.call_args_list[1][0][0]
        assert lint_args[0] == NODE
        assert lint_args[1] == entry_point
        assert lint_args[2] == "--no-globs"
        assert lint_args[3:] == [":a.md", ":b.md"]

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_passes_cwd(self, mock_which, tmp_path):
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        root = _make_entry(tmp_path)
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [
                CompletedProcess(args=[], returncode=0, stdout=root, stderr=""),
                CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
            ]
            markdownlint_files(["a.md"], cwd=str(tmp_path))
            assert mock_sub.call_args_list[1][1]["cwd"] == str(tmp_path)

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_defaults_to_process_cwd_when_cwd_omitted(self, mock_which, tmp_path, monkeypatch):
        """Without an explicit cwd, existence is resolved from the process cwd."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        root = _make_entry(tmp_path)
        monkeypatch.chdir(tmp_path)
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [
                CompletedProcess(args=[], returncode=0, stdout=root, stderr=""),
                CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
            ]
            passed, _ = markdownlint_files(["a.md"])
        assert passed is True
        lint_args = mock_sub.call_args_list[1][0][0]
        assert lint_args[3:] == [":a.md"]

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_missing_tool_fails_with_install_hint(self, mock_which, tmp_path):
        """A missing markdownlint-cli2 binary fails loudly instead of silently skipping."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        root = _make_entry(tmp_path)
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [
                CompletedProcess(args=[], returncode=0, stdout=root, stderr=""),
                OSError("markdownlint-cli2"),
            ]
            passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", return_value=None)
    @patch(f"{MODULE}.subprocess.run")
    def test_missing_node_fails_without_running(self, mock_run, mock_which, tmp_path):
        """node must be on PATH; its absence fails with an actionable install hint."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert "'node' was not found on PATH" in output
        assert MARKDOWNLINT_INSTALL_HINT in output
        mock_run.assert_not_called()
        mock_which.assert_called_once_with("node")

    @patch(f"{MODULE}.shutil.which", side_effect=lambda x: NODE if x == "node" else None)
    @patch(f"{MODULE}.subprocess.run")
    def test_missing_npm_fails_without_running(self, mock_run, mock_which, tmp_path):
        """npm must be on PATH; its absence fails with an actionable install hint."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert "'npm' was not found on PATH" in output
        assert MARKDOWNLINT_INSTALL_HINT in output
        mock_run.assert_not_called()

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    @patch(f"{MODULE}.subprocess.run", side_effect=OSError("npm binary failed"))
    def test_npm_oserror_fails_with_install_hint(self, mock_run, mock_which, tmp_path):
        """An OSError running npm root -g fails with an actionable hint."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    @patch(f"{MODULE}.subprocess.run", side_effect=[_NPM_ROOT_FAIL])
    def test_npm_root_nonzero_fails_with_install_hint(self, mock_run, mock_which, tmp_path):
        """npm root -g exit code != 0 fails with an actionable install hint."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    @patch(
        f"{MODULE}.subprocess.run",
        side_effect=[CompletedProcess(args=[], returncode=0, stdout="/no/such/root", stderr="")],
    )
    def test_markdownlint_not_installed_fails_with_install_hint(self, mock_run, mock_which, tmp_path):
        """markdownlint-cli2 entry point missing on disk → install hint."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_missing_package_metadata_fails_with_install_hint(self, mock_which, tmp_path):
        """Missing package.json fails instead of silently accepting an unknown version."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        entry_dir = tmp_path / "markdownlint-cli2"
        entry_dir.mkdir(parents=True, exist_ok=True)
        (entry_dir / "markdownlint-cli2-bin.mjs").write_text("", encoding="utf-8")
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [CompletedProcess(args=[], returncode=0, stdout=str(tmp_path), stderr="")]
            passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_invalid_package_metadata_fails_with_install_hint(self, mock_which, tmp_path):
        """Invalid package.json content fails with the pinned reinstall hint."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        entry_dir = tmp_path / "markdownlint-cli2"
        entry_dir.mkdir(parents=True, exist_ok=True)
        (entry_dir / "markdownlint-cli2-bin.mjs").write_text("", encoding="utf-8")
        (entry_dir / "package.json").write_text("{not json", encoding="utf-8")
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [CompletedProcess(args=[], returncode=0, stdout=str(tmp_path), stderr="")]
            passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_non_object_package_metadata_fails_with_install_hint(self, mock_which, tmp_path):
        """package.json that parses to a non-object (e.g. list) fails with the install hint."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        entry_dir = tmp_path / "markdownlint-cli2"
        entry_dir.mkdir(parents=True, exist_ok=True)
        (entry_dir / "markdownlint-cli2-bin.mjs").write_text("", encoding="utf-8")
        (entry_dir / "package.json").write_text('["not", "an", "object"]', encoding="utf-8")
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [CompletedProcess(args=[], returncode=0, stdout=str(tmp_path), stderr="")]
            passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_missing_version_in_package_metadata_fails_with_install_hint(self, mock_which, tmp_path):
        """Package metadata must expose a string version before the linter is used."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        entry_dir = tmp_path / "markdownlint-cli2"
        entry_dir.mkdir(parents=True, exist_ok=True)
        (entry_dir / "markdownlint-cli2-bin.mjs").write_text("", encoding="utf-8")
        (entry_dir / "package.json").write_text("{}", encoding="utf-8")
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [CompletedProcess(args=[], returncode=0, stdout=str(tmp_path), stderr="")]
            passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_wrong_markdownlint_version_fails_with_install_hint(self, mock_which, tmp_path):
        """A mismatched global markdownlint-cli2 version fails instead of drifting from CI."""
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        root = _make_entry(tmp_path, version="0.18.0")
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [CompletedProcess(args=[], returncode=0, stdout=root, stderr="")]
            passed, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert passed is False
        assert MARKDOWNLINT_INSTALL_HINT in output
        assert "0.18.0" in output

    @patch(f"{MODULE}.shutil.which", side_effect=_which)
    def test_combines_stdout_stderr(self, mock_which, tmp_path):
        (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
        root = _make_entry(tmp_path)
        with patch(f"{MODULE}.subprocess.run") as mock_sub:
            mock_sub.side_effect = [
                CompletedProcess(args=[], returncode=0, stdout=root, stderr=""),
                CompletedProcess(args=[], returncode=1, stdout="stdout\n", stderr="stderr\n"),
            ]
            _, output = markdownlint_files(["a.md"], cwd=str(tmp_path))
        assert "stdout" in output
        assert "stderr" in output
