"""Exercise the staged-Python formatter through real Git commits."""

import os
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[2] / ".githooks" / "pre-commit"
pytestmark = pytest.mark.skipif(
    not shutil.which("bash") or not shutil.which("git"),
    reason="Shell-hook tests require bash and git on PATH",
)


@pytest.fixture
def repo(isolated_test_runtime, monkeypatch):
    """Install the hook only after inherited Git routing has been isolated."""
    root = isolated_test_runtime
    hooks = root / ".git" / "format-hooks"
    hooks.mkdir()
    shutil.copy2(HOOK, hooks / "pre-commit")
    (hooks / "pre-commit").chmod(0o755)
    monkeypatch.setenv("AGDT_PYTHON", sys.executable)
    monkeypatch.setenv("PATH", str(Path(sysconfig.get_path("scripts"))) + os.pathsep + os.environ["PATH"])
    git(root, "config", "--local", "core.hooksPath", str(hooks))
    git(root, "config", "--local", "commit.gpgsign", "false")
    git(root, "config", "--local", "core.autocrlf", "false")
    git(root, "config", "--local", "core.splitIndex", "false")
    return root


def git(root, *args, check=True):
    """Run Git with local configuration and retain byte-exact results."""
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=check)


def stage(root, name="example.py", content="x=  1\n"):
    """Write and stage one path without interpreting unusual filename bytes."""
    (root / name).write_text(content, encoding="utf-8")
    git(root, "--literal-pathspecs", "add", "--", name)


def commit(root):
    """Attempt a real commit so hook failures cannot be mistaken for success."""
    return git(root, "commit", "-m", "test hook", check=False)


def fake_ruff(root, monkeypatch, mode="ok"):
    """Provide deterministic module/CLI behavior, even when Ruff is not installed."""
    tools = root / ".git" / "tools"
    tools.mkdir()
    module = tools / "ruff.py"
    module.write_text(
        "import pathlib, sys\n"
        f"mode = {mode!r}\n"
        "if mode == 'unavailable': sys.exit(1)\n"
        "if '--version' in sys.argv:\n"
        "    print('ruff test-version')\n"
        "    sys.exit(0)\n"
        "pathlib.Path('formatter-called').touch()\n"
        "print('formatter failed', file=sys.stderr)\n"
        "sys.exit(2)\n",
        encoding="utf-8",
    )
    cli = tools / "ruff"
    cli.write_text("#!/bin/sh\nprintf 'ruff test-version\\n'\n", encoding="utf-8")
    cli.chmod(0o755)
    monkeypatch.setenv("PYTHONPATH", str(tools))
    monkeypatch.setenv("PATH", str(tools) + os.pathsep + os.environ["PATH"])
    return tools


def assert_rejected_unchanged(root, before, result):
    """A rejected initial commit must preserve index bytes and create no HEAD."""
    assert result.returncode != 0, result.stdout + result.stderr
    assert (root / ".git" / "index").read_bytes() == before
    assert git(root, "rev-parse", "--verify", "HEAD", check=False).returncode != 0


def snapshot_index(root):
    """Prepare Git's cache-tree extension before comparing index bytes."""
    git(root, "write-tree")
    return (root / ".git" / "index").read_bytes()


@pytest.mark.parametrize("name", ["example.py", "space tab\tline\n雪.py", "-leading.py", ":(glob)*.py"])
def test_formats_committed_blob(repo, name):
    """Real Ruff formats unusual paths and leaves no unstaged changes."""
    if os.name == "nt" and any(char in name for char in "\n:*"):
        pytest.skip("Windows filenames cannot contain newlines, colons, or asterisks")
    module = subprocess.run([sys.executable, "-m", "ruff", "--version"], capture_output=True)
    if module.returncode:
        pytest.skip(f"{sys.executable} cannot run Ruff: {module.stderr!r}")
    cli = subprocess.run(["ruff", "--version"], capture_output=True, check=True)
    assert module.stdout == cli.stdout, "Module/CLI Ruff versions must match for integration tests"
    stage(repo, name)
    (repo / "unrelated.txt").write_text("do not stage\n", encoding="utf-8")
    result = commit(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert git(repo, "show", f"HEAD:{name}").stdout == b"x = 1\n"
    assert git(repo, "diff", "HEAD").stdout == b""
    assert git(repo, "ls-tree", "--name-only", "HEAD").stdout.count(b"unrelated.txt") == 0
    (repo / "unrelated.txt").unlink()
    assert git(repo, "status", "--porcelain").stdout == b""


def test_partial_staging_rejected_before_formatting(repo, monkeypatch):
    """Reject all selected partial files before touching the formatter or index."""
    fake_ruff(repo, monkeypatch)
    for name in ("first.py", "space name.py"):
        stage(repo, name)
        (repo / name).write_text("x=  2\n", encoding="utf-8")
    stage(repo, "unrelated.txt", "staged text\n")
    before = snapshot_index(repo)
    result = commit(repo)
    assert_rejected_unchanged(repo, before, result)
    assert b"finish staging" in result.stderr.lower()
    assert b"separate" in result.stderr.lower()
    for name in ("first.py", "space name.py"):
        assert name.encode() in result.stderr
        assert (repo / name).read_bytes() == b"x=  2\n"
    assert not (repo / "formatter-called").exists()


@pytest.mark.parametrize("delete_python", [False, True])
def test_no_python_and_deletions_are_noops(repo, monkeypatch, delete_python):
    """Non-Python commits and staged Python deletions never invoke Ruff."""
    tools = fake_ruff(repo, monkeypatch, "unavailable")
    if delete_python:
        stage(repo)
        assert commit(repo).returncode == 0
        git(repo, "rm", "--", "example.py")
    else:
        stage(repo, "notes.txt", "unchanged text\n")
    (tools / "ruff.py").write_text("raise AssertionError('Ruff must not run')\n", encoding="utf-8")
    result = commit(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert b"warning" not in result.stderr.lower()
    assert b"Ruff must not run" not in result.stderr
    assert git(repo, "diff", "HEAD").stdout == b""


def test_unavailable_module_warns_and_allows(repo, monkeypatch):
    """An unavailable module permits an unformatted commit with one warning."""
    fake_ruff(repo, monkeypatch, "unavailable")
    stage(repo)
    result = commit(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert git(repo, "show", "HEAD:example.py").stdout == b"x=  1\n"
    assert result.stderr.lower().count(b"warning") == 1
    assert b"not formatted" in result.stderr.lower()
    assert b"pre-push" in result.stderr and b"CI" in result.stderr


@pytest.mark.parametrize("missing", [False, True])
def test_path_ruff_missing_or_mismatched_fails_before_staging(repo, monkeypatch, missing):
    """An available module requires a matching PATH executable before mutation."""
    tools = fake_ruff(repo, monkeypatch)
    if missing:
        (tools / "ruff").unlink()
        git_path = shutil.which("git")
        (tools / "git").write_text(f'#!/bin/sh\nexec "{git_path}" "$@"\n', encoding="utf-8")
        (tools / "git").chmod(0o755)
        monkeypatch.setenv("PATH", str(tools))
    else:
        (tools / "ruff").write_text("#!/bin/sh\nprintf 'ruff different-version\\n'\n", encoding="utf-8")
    stage(repo)
    before = snapshot_index(repo)
    result = commit(repo)
    assert_rejected_unchanged(repo, before, result)
    assert b"PATH" in result.stderr and b"match" in result.stderr.lower()
    assert not (repo / "formatter-called").exists()
    assert (repo / "example.py").read_bytes() == b"x=  1\n"


def test_formatter_error_blocks_without_staging(repo, monkeypatch):
    """Formatter errors are reported and prevent staging and committing."""
    fake_ruff(repo, monkeypatch)
    stage(repo)
    before = snapshot_index(repo)
    result = commit(repo)
    assert_rejected_unchanged(repo, before, result)
    assert (repo / "formatter-called").exists()
    assert b"formatter failed" in result.stderr


def test_default_python_on_path(repo, monkeypatch):
    """Unset AGDT_PYTHON selects the single python executable on PATH."""
    tools = fake_ruff(repo, monkeypatch, "unavailable")
    monkeypatch.delenv("AGDT_PYTHON")
    executable = tools / "python"
    executable.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n', encoding="utf-8")
    executable.chmod(0o755)
    stage(repo)
    result = commit(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert b"not formatted" in result.stderr.lower()


def test_interpreter_path_with_spaces(repo, monkeypatch):
    """Treat AGDT_PYTHON as one executable path rather than shell words."""
    tools = fake_ruff(repo, monkeypatch, "unavailable")
    executable = tools / "python with spaces"
    executable.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n', encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("AGDT_PYTHON", str(executable))
    stage(repo)
    result = commit(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert b"not formatted" in result.stderr.lower()


def test_git_add_error_blocks_commit(repo, monkeypatch):
    """A staging failure is reported rather than committing unformatted index content."""
    tools = fake_ruff(repo, monkeypatch, "unavailable")
    (tools / "ruff.py").write_text("import sys\nprint('ruff test-version')\nsys.exit(0)\n", encoding="utf-8")
    stage(repo)
    before = snapshot_index(repo)
    git_path = shutil.which("git")
    wrapper = tools / "git"
    wrapper.write_text(
        '#!/bin/sh\nif [ "$1" = "--literal-pathspecs" ] && [ "$2" = "add" ]; then\n'
        'echo "git add failed" >&2\nexit 1\nfi\n'
        f'exec "{git_path}" "$@"\n',
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    interpreter = tools / "python"
    interpreter.write_text(f'#!/bin/sh\nexport PATH="{tools}:$PATH"\nexec "{sys.executable}" "$@"\n', encoding="utf-8")
    interpreter.chmod(0o755)
    monkeypatch.setenv("AGDT_PYTHON", str(interpreter))
    result = commit(repo)
    assert_rejected_unchanged(repo, before, result)
    assert b"git add failed" in result.stderr
    assert b"staging failed" in result.stderr
