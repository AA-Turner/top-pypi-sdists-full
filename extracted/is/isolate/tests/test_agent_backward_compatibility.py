"""Backward-compatibility tests for the agent startup chain.

The server ships ``agent_startup.py`` + ``agent.py`` from its own isolate
install but runs them with the user venv's Python, so the scripts and the
installed ``isolate`` package can be at different versions. Two directions
need to stay compatible:

* *Forward* -- current scripts against an older installed ``isolate``.
  Catches symbols the current agent added that older releases do not
  export (e.g. a new ``from isolate.backends.settings import ...``).
* *Reverse* -- older scripts against the current installed ``isolate``.
  Catches symbols older agents still depend on but we have just removed
  or renamed in the package.

For each of the N most recent ``vX.Y.Z`` git tags we build a venv and run
the agent scripts under it with ``--help``. Argparse exits as soon as
module-level imports resolve, so no gRPC server is needed. The test fails
on any ``Traceback`` or non-zero exit, catching *any* unhandled exception
(missing imports, renamed attrs, changed signatures, ...).

Fix a failure by either guarding the new usage with a ``try/except``
fallback, keeping the old symbol aliased, or intentionally dropping
support for that version (lower ``BACKWARD_COMPAT_RECENT_TAG_COUNT`` /
prune older tags).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest
from isolate.backends.common import Requirements, get_executable_path
from isolate.backends.settings import IsolateSettings
from isolate.backends.virtualenv import VirtualPythonEnvironment
from isolate.connections._local import agent_startup
from isolate.connections.grpc import agent

REPO_DIR = Path(__file__).resolve().parent.parent

# How many of the most recent ``vX.Y.Z`` tags to exercise. Each version
# provisions its own venv, so keep this bounded to keep CI time sane.
BACKWARD_COMPAT_RECENT_TAG_COUNT = 5

# Only consider final releases -- skip pre-releases, release candidates,
# dev builds, etc. The agent is expected to remain compatible with the
# last N stable releases.
_STABLE_TAG_RE = re.compile(r"^v(\d+\.\d+\.\d+)$")


def _discover_backward_compat_versions() -> list[str]:
    """Return the most recent released ``isolate`` versions by reading git
    tags from the local checkout.

    Falls back to an empty list (test gets skipped) when the repo is not a
    git checkout or ``git`` is unavailable -- that way wheel-only installs
    of the test suite do not fail spuriously.
    """
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(REPO_DIR),
                "tag",
                "--list",
                "v*",
                "--sort=-version:refname",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return []

    versions: list[str] = []
    for line in result.stdout.splitlines():
        match = _STABLE_TAG_RE.match(line.strip())
        if match is None:
            continue
        versions.append(match.group(1))
        if len(versions) >= BACKWARD_COMPAT_RECENT_TAG_COUNT:
            break
    return versions


BACKWARD_COMPAT_VERSIONS = _discover_backward_compat_versions()

pytestmark = pytest.mark.skipif(
    not BACKWARD_COMPAT_VERSIONS,
    reason="Could not discover released isolate versions from git tags.",
)


@pytest.fixture(scope="module")
def _tmp_cache(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("backward_compat_cache")


def _build_venv(requirement: str, cache_dir: Path, label: str) -> Path:
    """Create a venv with ``requirement`` installed; return the Python bin."""
    env = VirtualPythonEnvironment(Requirements.from_raw([requirement]))
    env.apply_settings(IsolateSettings(cache_dir=cache_dir))
    venv_path = env.create()
    try:
        return get_executable_path(venv_path, "python")
    except FileNotFoundError:
        return get_executable_path(venv_path, "python3")


@pytest.fixture(scope="module", params=BACKWARD_COMPAT_VERSIONS)
def old_isolate_python(request: pytest.FixtureRequest, _tmp_cache: Path) -> Path:
    """venv with a pinned *old* ``isolate[server]`` release."""
    version: str = request.param
    return _build_venv(f"isolate[server]=={version}", _tmp_cache, f"old-{version}")


@pytest.fixture(scope="module")
def current_isolate_python(_tmp_cache: Path) -> Path:
    """venv with the *current* ``isolate`` source tree installed."""
    return _build_venv(f"{REPO_DIR}[build]", _tmp_cache, "current")


@pytest.fixture(
    scope="module",
    params=BACKWARD_COMPAT_VERSIONS,
    ids=lambda v: v or "no-versions",
)
def old_agent_scripts(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> tuple[Path, Path]:
    """Extract ``agent_startup.py`` + ``agent.py`` from an old git tag.

    Uses ``git show v<ver>:<path>`` so we grab the scripts exactly as they
    shipped in that release without having to check the tag out.
    """
    version: str = request.param
    tag = f"v{version}"
    out_dir = tmp_path_factory.mktemp(f"old-agent-{version}")

    def _extract(repo_path: str, dest_name: str) -> Path:
        result = subprocess.run(
            ["git", "-C", str(REPO_DIR), "show", f"{tag}:{repo_path}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        dest = out_dir / dest_name
        dest.write_text(result.stdout)
        return dest

    startup_path = _extract(
        "src/isolate/connections/_local/agent_startup.py", "agent_startup.py"
    )
    agent_path = _extract("src/isolate/connections/grpc/agent.py", "agent.py")
    return startup_path, agent_path


def _run_scripts(
    python_executable: Path,
    startup_file: Path,
    agent_file: Path,
    *extra_args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(python_executable),
            str(startup_file),
            str(agent_file),
            *extra_args,
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _assert_no_exception(result: subprocess.CompletedProcess[str], label: str) -> None:
    """Fail if the subprocess raised any unhandled exception.

    Any uncaught exception in Python prints ``Traceback (most recent call
    last):`` to stderr before the interpreter exits non-zero. Checking for
    that marker catches every exception type (ImportError, AttributeError,
    SyntaxError, TypeError, ...) without hard-coding a specific one.
    """
    output = (result.stdout or "") + (result.stderr or "")
    assert (
        "Traceback (most recent call last):" not in output
    ), f"Agent raised an exception ({label}):\n{output}"


def _assert_clean_help_exit(
    result: subprocess.CompletedProcess[str], label: str
) -> None:
    _assert_no_exception(result, label)
    assert result.returncode == 0, (
        f"Expected clean --help exit ({label}); got exit={result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_current_agent_runs_against_old_isolate(old_isolate_python: Path) -> None:
    """Forward direction: the *current* ``agent_startup.py`` + ``agent.py``
    must load cleanly when executed under an *older* ``isolate`` install."""
    result = _run_scripts(
        old_isolate_python, Path(agent_startup.__file__), Path(agent.__file__), "--help"
    )
    _assert_clean_help_exit(result, f"current agent vs {old_isolate_python}")


def test_old_agent_runs_against_current_isolate(
    current_isolate_python: Path,
    old_agent_scripts: tuple[Path, Path],
) -> None:
    """Reverse direction: an *older* ``agent_startup.py`` + ``agent.py``
    must still load cleanly under the *current* ``isolate`` source.

    Guards against silently removing or renaming symbols that frozen
    older-agent builds in user environments still depend on.
    """
    startup_file, agent_file = old_agent_scripts
    result = _run_scripts(current_isolate_python, startup_file, agent_file, "--help")
    _assert_clean_help_exit(result, f"old agent {agent_file.parent.name}")
