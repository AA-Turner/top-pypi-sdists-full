"""Prove the real test runner cannot write through its caller's runtime paths."""

import json
import os
import shutil
import subprocess
from pathlib import Path
from textwrap import dedent

import pytest

from agentic_devtools import state
from agentic_devtools.cli.testing import _run_tests_sync


def _make_git_repo(root):
    root.mkdir()
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    for args in (
        ["init"],
        ["config", "--local", "user.name", "Isolation Test"],
        ["config", "--local", "user.email", "isolation@example.com"],
    ):
        subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True)
    return root


def _snapshot(root, absent_paths):
    """Include directories, every file's bytes, and explicitly absent paths."""
    inventory = {}
    for path in [root, *sorted(root.rglob("*"))]:
        relative = path.relative_to(root).as_posix()
        inventory[relative] = ("directory", None) if path.is_dir() else ("file", path.read_bytes())
    for relative in absent_paths:
        assert not (root / relative).exists()
        inventory[relative] = ("absent", None)
    return inventory


def _seed(root, files):
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


_PROBE = dedent(
    """\
    import json
    import os
    import subprocess
    from pathlib import Path

    from agentic_devtools import state
    from agentic_devtools.state import get_state_dir as real_get_state_dir

    inherited_state_dir = os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR")
    initial_cwd = Path.cwd()


    def test_probe(temp_state_dir, isolated_test_runtime, monkeypatch):
        assert Path(state.__file__).resolve() == Path(os.environ["ISOLATION_SOURCE"]) / "agentic_devtools/state.py"
        assert os.environ["ISOLATION_INHERITED"] == "preserved"
        assert inherited_state_dir is None
        assert initial_cwd == Path(os.environ["ISOLATION_WORKSPACE"])
        assert "AGENTIC_DEVTOOLS_STATE_DIR" not in os.environ
        assert isolated_test_runtime.is_dir()
        assert (isolated_test_runtime / ".agdt").is_dir()
        assert Path.cwd() == isolated_test_runtime
        git_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
        assert Path(git_root).resolve() == isolated_test_runtime.resolve()
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
            assert key not in os.environ
        assert state.get_state_dir() == temp_state_dir

        # Exercise the fixture's pinned state path, then real cwd-based syncing.
        with monkeypatch.context() as pinned:
            pinned.setenv("AGENTIC_DEVTOOLS_STATE_DIR", str(temp_state_dir))
            state.set_value("issue_key", "42")
            assert state.get_value("issue_key") == "42"
            pinned.delenv("AGENTIC_DEVTOOLS_STATE_DIR")
            state.set_value("issue_key", "43")
            state.set_value("issue_key", "42")
            bootstrap = isolated_test_runtime / ".agdt/runtime-bootstrap.json"
            assert json.loads(bootstrap.read_text()) == {"worktree_key": "42"}

        # Perform the real Git-root writes in the fixture-provided repository so these
        # assertions fail if isolated_test_runtime stops initializing its own Git root.
        with monkeypatch.context() as writer:
            writer.setattr(state, "get_state_dir", real_get_state_dir)
            state.set_bootstrap_state(identity="probe", worktree_key="42")
            agdt = isolated_test_runtime / ".agdt"
            assert json.loads((agdt / "identity.json").read_text()) == {
                "identity": "probe", "email": "isolation@example.com"
            }
            assert json.loads((agdt / "runtime-bootstrap.json").read_text()) == {"worktree_key": "42"}
            assert (agdt / "workflows/probe/.identity-owner").read_text() == "isolation@example.com"
            state.set_workflow_state("isolation-probe", "in-progress", step="write")
            assert state.get_workflow_state()["active"] == "isolation-probe"
            scoped_state = agdt / "workflows/probe/42/state.json"
            assert state.get_state_dir() == scoped_state.parent
            assert json.loads(scoped_state.read_text())["workflow"]["step"] == "write"

        # Deliberately bypass monkeypatch: the shared fixture must undo this assignment.
        os.environ["AGENTIC_DEVTOOLS_STATE_DIR"] = str(temp_state_dir)
    """
)


_TEARDOWN_PROBE = dedent(
    """\
    import json
    import os
    from pathlib import Path

    import pytest


    @pytest.fixture(scope="session", autouse=True)
    def verify_runtime_teardown():
        initial_cwd = Path.cwd()
        initial_environment = dict(os.environ)
        initial_environment.pop("PYTEST_CURRENT_TEST", None)
        assert "AGENTIC_DEVTOOLS_STATE_DIR" not in initial_environment
        external = Path(os.environ["ISOLATION_EXTERNAL_REPO"])
        assert os.environ["GIT_DIR"] == str(external / ".git")
        assert os.environ["GIT_WORK_TREE"] == str(external)
        assert os.environ["GIT_COMMON_DIR"] == str(external / ".git")
        assert os.environ["GIT_INDEX_FILE"] == str(external / ".git/index")
        assert os.environ["GIT_CONFIG_GLOBAL"] == str(external / ".git/config")
        assert os.environ["GIT_CONFIG_SYSTEM"] == str(external / ".git/config")
        yield
        restored_environment = dict(os.environ)
        restored_environment.pop("PYTEST_CURRENT_TEST", None)
        assert restored_environment == initial_environment
        assert "AGENTIC_DEVTOOLS_STATE_DIR" not in os.environ
        assert Path.cwd() == initial_cwd
        (initial_cwd / "runtime-teardown.json").write_text(json.dumps({
            "environment_restored": True, "cwd_restored": True, "state_dir_absent": True
        }), encoding="utf-8")
    """
)


_OVERRIDE_PROBE = dedent(
    """\
    import json
    import os
    from pathlib import Path

    from agentic_devtools import state


    def test_override_probe(temp_state_dir, clear_state_before, tmp_path):
        runtime = tmp_path / "runtime"
        assert Path.cwd() == runtime
        assert "AGENTIC_DEVTOOLS_STATE_DIR" not in os.environ
        assert state.get_state_dir().is_relative_to(tmp_path)
        assert json.loads((state.get_state_dir() / "state.json").read_text()) == {}
        state.set_value("jira.issue_key", "OVERRIDE-42")
        assert state.get_value("jira.issue_key") == "OVERRIDE-42"
        assert json.loads((runtime / ".agdt/runtime-bootstrap.json").read_text()) == {
            "worktree_key": "OVERRIDE-42"
        }
        state.set_workflow_state("override-probe", "in-progress", step="write")
        assert state.get_workflow_state()["step"] == "write"
    """
)

_BACKGROUND_PROBE = dedent(
    """\
    import json
    import os
    from pathlib import Path

    from agentic_devtools import state


    def test_background_probe(mock_background_and_state, tmp_path):
        assert Path.cwd() == tmp_path / "runtime"
        assert "AGENTIC_DEVTOOLS_STATE_DIR" not in os.environ
        assert state.get_state_dir() == mock_background_and_state["state_dir"]
        state.set_value("jira.issue_key", "BACKGROUND-42")
        assert state.get_value("jira.issue_key") == "BACKGROUND-42"
        assert json.loads((Path.cwd() / ".agdt/runtime-bootstrap.json").read_text()) == {
            "worktree_key": "BACKGROUND-42"
        }
    """
)


def _copy_fixture(source_root, workspace, source, destination):
    source_path = source_root / source
    destination_path = workspace / destination
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)
    assert destination_path.read_bytes() == source_path.read_bytes()


def _prepare_fixture_probes(source_root, workspace):
    (workspace / "conftest.py").write_text(_TEARDOWN_PROBE, encoding="utf-8")
    tests = workspace / "tests"
    tests.mkdir()
    source_conftest = source_root / "tests/conftest.py"
    copied_conftest = tests / "conftest.py"
    shutil.copyfile(source_conftest, copied_conftest)
    assert copied_conftest.read_bytes() == source_conftest.read_bytes()
    (tests / "test_probe.py").write_text(_PROBE, encoding="utf-8")
    fixture_copies = tests / "fixture_copies"
    fixture_copies.mkdir()
    (fixture_copies / "__init__.py").touch()
    for name, source in (
        ("git_commands", "tests/test_git_commands.py"),
        ("git_core", "tests/test_git_core.py"),
        ("preflight", "tests/unit/cli/workflows/preflight/test_perform_auto_setup.py"),
        ("e2e", "tests/e2e_smoke/conftest.py"),
    ):
        _copy_fixture(source_root, workspace, source, f"tests/fixture_copies/{name}.py")
        case = tests / name
        case.mkdir()
        fixtures = "clear_state_before, temp_state_dir" if name.startswith("git_") else "temp_state_dir"
        (case / f"test_{name}_probe.py").write_text(
            f"from fixture_copies.{name} import {fixtures}\n\n" + _OVERRIDE_PROBE,
            encoding="utf-8",
        )
    for name in ("async_commands", "async_status"):
        case = tests / name
        _copy_fixture(source_root, workspace, f"tests/unit/cli/jira/{name}/conftest.py", f"tests/{name}/conftest.py")
        (case / f"test_{name}_probe.py").write_text(_OVERRIDE_PROBE + _BACKGROUND_PROBE, encoding="utf-8")
    background_sources = [("git_async", "tests/test_git_async.py")]
    for kind in ("issue", "bug_issue", "documentation_issue", "feature_issue", "task_issue"):
        for suffix in ("async", "async_cli"):
            name = f"create_agdt_{kind}_{suffix}"
            background_sources.append((name, f"tests/unit/cli/github/async_commands/test_{name}.py"))
    for name, source in background_sources:
        _copy_fixture(source_root, workspace, source, f"tests/fixture_copies/{name}.py")
        (tests / f"test_{name}_probe.py").write_text(
            f"from fixture_copies.{name} import mock_background_and_state\n\n" + _BACKGROUND_PROBE,
            encoding="utf-8",
        )


@pytest.fixture
def hostile_git_sentinel(tmp_path, monkeypatch):
    """Preserve an external repository while routing inherited Git inputs to it."""
    external_repo = _make_git_repo(tmp_path / "external-repo")
    external_git = external_repo / ".git"
    external_config = external_git / "config"
    external_config.write_bytes(
        external_config.read_bytes() + b"\n[user]\n\tname = External Sentinel\n\temail = external@example.com\n"
    )
    external_agdt = external_repo / ".agdt"
    _seed(
        external_agdt,
        {
            "identity.json": b'{"identity": "external", "email": "external@example.com"}\n',
            "runtime-bootstrap.json": b'{"worktree_key": "keep"}\n',
            "workflows/external/keep/state.json": b'{"sentinel": "external-repo"}\n',
            "workflows/external/.identity-owner": b"external@example.com",
        },
    )
    external_absent = ["workflows/probe", "workflows/_unscoped", "nested/new.json"]
    before_external = _snapshot(external_agdt, external_absent)
    before_git = _snapshot(external_git, ["config.lock", "index", "index.lock"])
    before_config = (external_git / "config").read_bytes()
    hostile_environment = {
        "GIT_DIR": str(external_git),
        "GIT_WORK_TREE": str(external_repo),
        "GIT_INDEX_FILE": str(external_git / "index"),
        "GIT_COMMON_DIR": str(external_git),
        "GIT_CONFIG_GLOBAL": str(external_git / "config"),
        "GIT_CONFIG_SYSTEM": str(external_git / "config"),
    }
    for key, value in hostile_environment.items():
        monkeypatch.setenv(key, value)
    yield external_repo
    assert _snapshot(external_agdt, external_absent) == before_external
    assert _snapshot(external_git, ["config.lock", "index", "index.lock"]) == before_git
    assert (external_git / "config").read_bytes() == before_config


def test_runner_preserves_external_agdt(tmp_path, monkeypatch, capsys, hostile_git_sentinel):
    """One child run must pass every real fixture chain without external writes."""
    source_root = Path(__file__).resolve().parents[2]
    # The helper must ignore hostile routing during sentinel setup as well.
    workspace = _make_git_repo(tmp_path / "workspace")
    _prepare_fixture_probes(source_root, workspace)
    (workspace / "pyproject.toml").write_text(
        '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n[tool.coverage.html]\ndirectory = "htmlcov"\n',
        encoding="utf-8",
    )
    workspace_agdt = workspace / ".agdt"
    _seed(
        workspace_agdt,
        {
            "_unscoped/state.json": b'{"legacy": true}\n',
            "workflows/_unscoped/state.json": b'{"sentinel": "unscoped"}\n',
            "identity.json": b'{"identity": "caller", "email": "caller@example.com"}\n',
            "runtime-bootstrap.json": b'{"worktree_key": "original"}\n',
            "workflows/caller/original/state.json": b'{"sentinel": "scoped"}\n',
            "workflows/caller/original/nested/keep.bin": b"\x00unchanged\xff",
        },
    )
    override_agdt = tmp_path / "external" / ".agdt"
    override_state = override_agdt / "workflows" / "_unscoped"
    _seed(override_agdt, {"workflows/_unscoped/state.json": b'{"sentinel": "override"}\n'})
    absent_workspace = ["workflows/caller/42", "workflows/probe/42/state.json", "nested/new.json"]
    absent_override = ["identity.json", "runtime-bootstrap.json", "workflows/probe/42/state.json", "nested/new.json"]
    before_workspace = _snapshot(workspace_agdt, absent_workspace)
    before_override = _snapshot(override_agdt, absent_override)

    monkeypatch.chdir(workspace)
    monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", str(override_state))
    monkeypatch.setenv("ISOLATION_SOURCE", str(source_root))
    monkeypatch.setenv("ISOLATION_WORKSPACE", str(workspace))
    monkeypatch.setenv("ISOLATION_INHERITED", "preserved")
    monkeypatch.setenv("ISOLATION_EXTERNAL_REPO", str(hostile_git_sentinel))
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join(filter(None, [str(source_root), os.environ.get("PYTHONPATH")])))
    monkeypatch.setenv("COVERAGE_FILE", str(workspace / ".coverage"))
    monkeypatch.setenv("COVERAGE_RCFILE", str(workspace / "pyproject.toml"))
    monkeypatch.setenv("PYTEST_ADDOPTS", "")
    parent_environment = os.environ.copy()
    assert state.get_state_dir() == override_state
    assert state.get_value("sentinel") == "override"

    result = _run_tests_sync()
    output = capsys.readouterr().out

    assert _snapshot(workspace_agdt, absent_workspace) == before_workspace
    assert _snapshot(override_agdt, absent_override) == before_override
    assert os.environ == parent_environment
    assert Path.cwd() == workspace
    assert state.get_state_dir() == override_state
    assert state.get_value("sentinel") == "override"
    assert result == 1, output
    assert "collected 20 items" in output, output
    assert "test_probe.py::test_probe PASSED" in output, output
    assert "20 passed" in output, output
    for name in ("git_commands", "git_core", "preflight", "e2e", "async_commands", "async_status"):
        assert f"{name}/test_{name}_probe.py::test_override_probe PASSED" in output, output
    for name in ("async_commands", "async_status"):
        assert f"{name}/test_{name}_probe.py::test_background_probe PASSED" in output, output
    assert "FAILED" not in output, output
    assert "test_probe.py::test_probe ERROR" not in output, output
    assert "FAIL Required test coverage of 100% not reached." in output, output
    assert (workspace / ".coverage").is_file()
    assert (workspace / "htmlcov" / "index.html").is_file()
    assert json.loads((workspace / "runtime-teardown.json").read_text()) == {
        "environment_restored": True,
        "cwd_restored": True,
        "state_dir_absent": True,
    }
