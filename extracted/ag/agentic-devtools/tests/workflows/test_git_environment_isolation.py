"""Regression coverage for Git hook environments leaking into fixture repositories."""

import os
import subprocess

import pytest

from agentic_devtools.cli.checks.tests import run_changed_tests
from agentic_devtools.git_env import GIT_ROUTING_PREFIXES, GIT_ROUTING_VARIABLES, sanitize_git_environment
from tests.conftest import isolate_git_environment
from tests.unit.cli.checks.changed_files.test_get_changed_files_strict import committed_repo
from tests.workflows.test_windows_specific_fixture_bytes import _create_fixture_repository


def test_real_child_outside_conftest_cannot_inherit_routing(tmp_path, monkeypatch):
    target = tmp_path / "test_environment.py"
    target.write_text(
        "import os\n"
        "def test_environment():\n"
        "    assert 'GIT_DIR' not in os.environ\n"
        "    assert 'GIT_INDEX_FILE' not in os.environ\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GIT_DIR", "sentinel")
    monkeypatch.setenv("GIT_INDEX_FILE", "sentinel-index")

    passed, output = run_changed_tests([str(target)], cwd=tmp_path)

    assert passed, output


@pytest.mark.parametrize("factory", ["strict_diff", "windows_bytes"])
def test_fixture_build_leaves_sentinel_head_refs_config_and_index_unchanged(tmp_path, monkeypatch, factory):
    sentinel, _ = _create_fixture_repository(tmp_path / "sentinel", "-text")
    clean_env = sanitize_git_environment(os.environ)

    def snapshot():
        refs = subprocess.run(
            ["git", "show-ref", "--head"],
            cwd=sentinel,
            env=clean_env,
            check=True,
            capture_output=True,
            shell=False,
        ).stdout
        return (
            (sentinel / ".git" / "HEAD").read_bytes(),
            refs,
            (sentinel / ".git" / "config").read_bytes(),
            (sentinel / ".git" / "index").read_bytes(),
        )

    before = snapshot()
    monkeypatch.setenv("GIT_DIR", str(sentinel / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(sentinel / ".git" / "index"))
    root = tmp_path / "new"
    root.mkdir()

    if factory == "strict_diff":
        built = committed_repo.__wrapped__(root)
    else:
        built, _ = _create_fixture_repository(root, "-text")

    assert (built / ".git" / "config").is_file()
    assert snapshot() == before


def test_autouse_fixture_removes_all_routing_and_restores_environment(monkeypatch):
    routing = [*GIT_ROUTING_VARIABLES, *(prefix + "42" for prefix in GIT_ROUTING_PREFIXES)]
    for key in routing:
        monkeypatch.setenv(key, "sentinel")
    monkeypatch.setenv("KEEP_TEST_ENVIRONMENT", "preserved")

    with pytest.MonkeyPatch.context() as isolated:
        isolate_git_environment.__wrapped__(isolated)
        assert all(key not in os.environ for key in routing)
        assert os.environ["KEEP_TEST_ENVIRONMENT"] == "preserved"

    assert all(os.environ[key] == "sentinel" for key in routing)
