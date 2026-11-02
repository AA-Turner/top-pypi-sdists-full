import os
import subprocess
from pathlib import Path

import pytest

from agentic_devtools.cli.ci.windows_fixture_bytes import verify_fixture_bytes
from agentic_devtools.git_env import sanitize_git_environment


def _create_fixture_repository(tmp_path: Path, attribute: str, *, with_fixture: bool = True) -> tuple[Path, str]:
    root = tmp_path / "fixture-repo"
    root.mkdir(parents=True)

    def git(*args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            shell=False,
            env=sanitize_git_environment(os.environ),
        )
        return result.stdout.strip()

    git("init", "-q")
    git("config", "--local", "user.email", "workflow-test@example.invalid")
    git("config", "--local", "user.name", "Windows CI contract test")
    git("config", "--local", "commit.gpgsign", "false")
    git("config", "--local", "core.autocrlf", "true")
    fixture_dir = root / "tests" / "fixtures" / "reviewing-agent-benchmark"
    fixture_dir.mkdir(parents=True)
    attributes = root / ".gitattributes"
    attributes.write_text(f"tests/fixtures/reviewing-agent-benchmark/** {attribute}\n", encoding="utf-8")
    if with_fixture:
        (fixture_dir / "sample.txt").write_bytes(b"line one\r\nline two\r\n")
    git("add", ".")
    git("commit", "-qm", "fixture evidence")
    return root, git("rev-parse", "HEAD")


def test_real_git_fixture_audit_accepts_crlf_with_text_unset_and_rejects_changed_bytes(tmp_path: Path) -> None:
    root, commit = _create_fixture_repository(tmp_path, "-text")
    fixture = root / "tests" / "fixtures" / "reviewing-agent-benchmark" / "sample.txt"

    assert verify_fixture_bytes(commit, root) == 1
    assert fixture.read_bytes() == b"line one\r\nline two\r\n"

    fixture.write_bytes(b"line one\nline two\n")
    with pytest.raises(ValueError, match="blob mismatch"):
        verify_fixture_bytes(commit, root)


def test_real_git_fixture_audit_rejects_missing_or_unspecified_fixtures(tmp_path: Path) -> None:
    missing_root, missing_commit = _create_fixture_repository(tmp_path / "missing", "-text")
    (missing_root / "tests" / "fixtures" / "reviewing-agent-benchmark" / "sample.txt").unlink()
    with pytest.raises(FileNotFoundError, match="Tracked fixture is missing"):
        verify_fixture_bytes(missing_commit, missing_root)

    unspecified_root, unspecified_commit = _create_fixture_repository(tmp_path / "unspecified", "!text")
    with pytest.raises(ValueError, match="observed 'unspecified'"):
        verify_fixture_bytes(unspecified_commit, unspecified_root)


def test_real_git_fixture_audit_rejects_incomplete_tree_evidence(tmp_path: Path) -> None:
    root, commit = _create_fixture_repository(tmp_path, "-text", with_fixture=False)

    with pytest.raises(ValueError, match="inventory is empty"):
        verify_fixture_bytes(commit, root)
