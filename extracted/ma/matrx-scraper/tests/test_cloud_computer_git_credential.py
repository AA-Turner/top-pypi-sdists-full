"""Machines plan phase 3: git on a Cloud Computer authenticates with the owner's GitHub connection.

Red when: the token AI Dream pushes (``MATRX_GITHUB_GIT_TOKEN``, else the Vault's ``GITHUB_TOKEN``)
is not what ``git credential fill`` answers for github.com through the daemon's env-only helper;
the token is written under the home or into the daemon's env/config text; a removed token keeps
answering; or another host is answered.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker import machine_agent as ma

TOKEN = "ghu_connectiontoken123"


def _daemon(tmp_path: Path) -> ma.AgentDaemon:
    home = tmp_path / "home"
    home.mkdir()
    daemon = ma.AgentDaemon(str(home), launch_env={"PATH": os.environ.get("PATH", "")}, python="/nonexistent")
    daemon.git_token_path = str(tmp_path / "shm" / "github-token")
    return daemon


def _fill(daemon: ma.AgentDaemon, host: str = "github.com") -> str:
    env = daemon._env()
    done = subprocess.run(
        ["git", "credential", "fill"],
        input=f"protocol=https\nhost={host}\n\n",
        env={**env, "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "1"},
        capture_output=True, text=True, timeout=20,
    )
    return done.stdout


pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")


def test_git_answers_the_connection_token_from_memory_only(tmp_path: Path) -> None:
    daemon = _daemon(tmp_path)
    ma.apply_vault_env(daemon, {ma.GIT_TOKEN_ENV: TOKEN, "OTHER": "x"})
    assert f"password={TOKEN}" in _fill(daemon)
    assert "username=x-access-token" in _fill(daemon)
    mode = stat.S_IMODE(os.stat(daemon.git_token_path).st_mode)
    assert mode == 0o600
    assert not Path(daemon.git_token_path).is_relative_to(daemon.home)
    for root, _dirs, files in os.walk(daemon.home):
        for name in files:
            assert TOKEN not in Path(root, name).read_text(errors="ignore")
    assert TOKEN not in repr(daemon._env())


def test_the_vault_github_token_is_the_fallback_and_a_removed_token_stops(tmp_path: Path) -> None:
    daemon = _daemon(tmp_path)
    ma.apply_vault_env(daemon, {"GITHUB_TOKEN": "ghp_vaultvalue"})
    assert "password=ghp_vaultvalue" in _fill(daemon)
    ma.apply_vault_env(daemon, {ma.GIT_TOKEN_ENV: TOKEN, "GITHUB_TOKEN": "ghp_vaultvalue"})
    assert f"password={TOKEN}" in _fill(daemon)
    ma.apply_vault_env(daemon, {})
    assert not os.path.exists(daemon.git_token_path)
    assert "password=" not in _fill(daemon)


def test_only_github_is_answered(tmp_path: Path) -> None:
    daemon = _daemon(tmp_path)
    ma.apply_vault_env(daemon, {ma.GIT_TOKEN_ENV: TOKEN})
    assert TOKEN not in _fill(daemon, host="gitlab.com")
