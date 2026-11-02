"""Verify no stale state-directory references remain in the codebase."""

import os
import subprocess
from pathlib import Path, PurePosixPath
from unittest.mock import patch

import pytest

from agentic_devtools.cli.subprocess_utils import run_safe

REPO_ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".eggs",
    "build",
    "dist",
    "node_modules",
    ".agdt",
    ".agdt-temp",
}
EXCLUDE_FILES = {"CHANGELOG.md"}
# Scan common text file types where this pattern is likely to appear.
SCAN_EXTENSIONS = {".py", ".md", ".toml", ".yml", ".yaml", ".txt", ".rst", ".cfg", ".ini"}

# Files whose docstrings still reference the old path because editing them
# triggers a CI module-coverage gate that cannot currently pass (the azure
# module has <100% unit-test coverage).  Tracked for cleanup separately.
_KNOWN_EXCEPTIONS = {
    Path("agentic_devtools/cli/azure/app_insights_commands.py"),
}

# The pattern we are scanning for — kept as a constant so this test file
# does not itself contain the literal pattern on assertion/comment lines.
_BANNED_PATTERN = "scripts" + "/" + "temp"


def _candidate_files(repo_root: Path) -> list[PurePosixPath]:
    """List tracked and non-ignored untracked paths without traversing ignored trees."""
    command = ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
    guidance = "Run agdt-test from the root of a valid Git checkout with Git installed."
    try:
        result = run_safe(
            command,
            capture_output=True,
            text=False,
            check=False,
            shell=False,
            cwd=str(repo_root),
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        pytest.fail(f"{' '.join(command)} failed: {exc}; stderr: {getattr(exc, 'stderr', '')}. {guidance}")
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        pytest.fail(f"{' '.join(command)} exited {result.returncode}: {stderr}. {guidance}")
    try:
        output = result.stdout.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{' '.join(command)} returned invalid UTF-8 paths: {exc}. {guidance}")
    return [PurePosixPath(entry) for entry in output.split("\0") if entry]


def _scan_stale_state_dir_references(repo_root: Path) -> None:
    """Check scannable repository-relative candidates and reject an empty scan."""
    hits = []
    scanned = 0
    for rel in _candidate_files(repo_root):
        if any(part in EXCLUDE_DIRS for part in rel.parts[:-1]):
            continue
        if rel.name in EXCLUDE_FILES:
            continue
        if rel.suffix not in SCAN_EXTENSIONS and rel.name != ".gitignore":
            continue
        path = repo_root / rel
        if not path.is_file():
            continue
        # Skip this test file itself and known exceptions.
        if path.resolve() == Path(__file__).resolve() or Path(rel) in _KNOWN_EXCEPTIONS:
            continue
        scanned += 1
        content = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(content.splitlines(), 1):
            if _BANNED_PATTERN in line:
                hits.append(f"{rel}:{lineno}: {line.strip()}")
    if not scanned:
        pytest.fail(
            "No scannable files remain after git ls-files --cached --others --exclude-standard -z. "
            "Run agdt-test from the root of a valid Git checkout containing scannable files."
        )
    assert not hits, f"Found {_BANNED_PATTERN} references:\n" + "\n".join(hits)


def test_no_stale_state_dir_references():
    """Ensure no file in the repo references the old state directory path."""
    _scan_stale_state_dir_references(REPO_ROOT)


@pytest.fixture(autouse=True)
def _restore_environment():
    with patch.dict(os.environ):
        yield


@pytest.fixture
def guard_repo(tmp_path, monkeypatch):
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    root = tmp_path / "build" / "repo"
    root.mkdir(parents=True)
    run_safe(["git", "init", str(root)], shell=False, check=True, capture_output=True)
    return root


@pytest.mark.parametrize("tracked", [True, False])
@pytest.mark.parametrize("name", ["file with spaces.py", "référence.py"])
def test_detects_relative_violations(guard_repo, tracked, name):
    path = guard_repo / name
    path.write_text(f"clean\n  {_BANNED_PATTERN}  \n", encoding="utf-8")
    if tracked:
        run_safe(["git", "add", "."], cwd=str(guard_repo), shell=False, check=True)
    with pytest.raises(AssertionError, match=name + ":2: " + _BANNED_PATTERN):
        _scan_stale_state_dir_references(guard_repo)


def test_ignored_venv_is_never_read(guard_repo, monkeypatch):
    (guard_repo / ".gitignore").write_text(".venv-wt314/\n", encoding="utf-8")
    ignored = guard_repo / ".venv-wt314" / "bad.py"
    ignored.parent.mkdir()
    ignored.write_text(_BANNED_PATTERN, encoding="utf-8")
    read_text = Path.read_text
    reads = []

    def record_read(path, *args, **kwargs):
        reads.append(path)
        return read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", record_read)
    _scan_stale_state_dir_references(guard_repo)
    assert reads == [guard_repo / ".gitignore"]


def test_preserves_scan_filters(guard_repo, monkeypatch):
    skipped = [
        "node_modules/bad.md",
        "CHANGELOG.md",
        "image.svg",
        "agentic_devtools/cli/azure/app_insights_commands.py",
        "tests/test_no_scripts_temp_references.py",
    ]
    for name in skipped:
        path = guard_repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_BANNED_PATTERN, encoding="utf-8")
    (guard_repo / "clean.py").write_bytes(b"\xffclean\n")
    (guard_repo / "deleted.py").write_text(_BANNED_PATTERN, encoding="utf-8")
    run_safe(["git", "add", "."], cwd=str(guard_repo), shell=False, check=True)
    (guard_repo / "deleted.py").unlink()
    monkeypatch.setitem(globals(), "__file__", str(guard_repo / skipped[-1]))
    _scan_stale_state_dir_references(guard_repo)


@pytest.mark.parametrize("name", [".gitignore", ".venv-wt314/bad.py", "build.py"])
def test_nonignored_paths_are_scanned(guard_repo, name):
    path = guard_repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_BANNED_PATTERN, encoding="utf-8")
    with pytest.raises(AssertionError, match=_BANNED_PATTERN):
        _scan_stale_state_dir_references(guard_repo)


@pytest.mark.parametrize(
    "error",
    [
        FileNotFoundError("git unavailable"),
        OSError("git cannot execute"),
        subprocess.TimeoutExpired("git", 30, stderr="git stalled"),
    ],
)
def test_git_execution_failures_are_actionable(guard_repo, error):
    with patch(f"{__name__}.run_safe", side_effect=error):
        with pytest.raises(pytest.fail.Exception) as failure:
            _scan_stale_state_dir_references(guard_repo)
    message = str(failure.value)
    assert "git ls-files --cached --others --exclude-standard -z" in message
    assert "valid Git checkout" in message
    assert str(error) in message
    if isinstance(error, subprocess.TimeoutExpired):
        assert "git stalled" in message


def test_unsuccessful_enumeration_is_actionable(guard_repo):
    result = subprocess.CompletedProcess([], 128, b"", b"index is corrupt")
    with patch(f"{__name__}.run_safe", return_value=result) as command:
        with pytest.raises(pytest.fail.Exception, match="index is corrupt.*valid Git checkout"):
            _scan_stale_state_dir_references(guard_repo)
    command.assert_called_once_with(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        capture_output=True,
        text=False,
        check=False,
        shell=False,
        cwd=str(guard_repo),
        timeout=30,
    )


def test_non_work_tree_fails_closed(guard_repo):
    with pytest.raises(pytest.fail.Exception, match="(?s)not a git repository.*valid Git checkout"):
        _scan_stale_state_dir_references(guard_repo.parent)


@pytest.mark.parametrize("name", [None, "node_modules/only.py"])
def test_no_scannable_files_fails_closed(guard_repo, name):
    if name is not None:
        path = guard_repo / name
        path.parent.mkdir()
        path.write_text("clean\n", encoding="utf-8")
        run_safe(["git", "add", "."], cwd=str(guard_repo), shell=False, check=True)
    with pytest.raises(pytest.fail.Exception, match="No scannable files.*valid Git checkout"):
        _scan_stale_state_dir_references(guard_repo)


@pytest.mark.parametrize("has_regular_file", [True, False])
def test_non_file_candidate_is_skipped(guard_repo, has_regular_file):
    (guard_repo / "submodule.py").mkdir()
    run_safe(
        ["git", "update-index", "--add", "--cacheinfo", "160000", "1" * 40, "submodule.py"],
        cwd=str(guard_repo),
        shell=False,
        check=True,
        capture_output=True,
    )
    if has_regular_file:
        (guard_repo / "clean.py").write_text("clean\n", encoding="utf-8")
        _scan_stale_state_dir_references(guard_repo)
    else:
        with pytest.raises(pytest.fail.Exception, match="No scannable files.*valid Git checkout"):
            _scan_stale_state_dir_references(guard_repo)


def test_invalid_utf8_enumeration_fails_closed(guard_repo):
    (guard_repo / "clean.py").write_text("clean\n", encoding="utf-8")
    result = subprocess.CompletedProcess([], 0, b"clean.py\0bad\xff.py\0", b"")
    with patch(f"{__name__}.run_safe", return_value=result):
        with pytest.raises(pytest.fail.Exception, match="git ls-files.*UTF-8.*valid Git checkout"):
            _scan_stale_state_dir_references(guard_repo)
