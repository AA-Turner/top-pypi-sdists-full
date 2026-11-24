"""Plan phase 2a, machine side: the owner's Vault rides every agent command.

* ``apply_vault_env`` replaces the machine's vault set (a removed name leaves, a
  rotated value lands) and answers NAMES only;
* every agent ``exec`` carries the vault env, and a value the caller passed on
  purpose wins over it;
* the daemon's status lists names, never a value.
"""

from __future__ import annotations

import asyncio
import json

import httpx

from matrx_scraper.cloud_browser.worker import machine_agent as ma

SECRET = "ghp_supersecretvalue"


def _daemon() -> ma.AgentDaemon:
    return ma.AgentDaemon("/home/browser-worker", launch_env={}, python="/nonexistent")


def test_apply_replaces_the_set_and_answers_names_only() -> None:
    daemon = _daemon()
    first = ma.apply_vault_env(daemon, {"GITHUB_TOKEN": SECRET, "OLD_KEY": "x"})
    assert first["added"] == ["GITHUB_TOKEN", "OLD_KEY"] and first["removed"] == []
    second = ma.apply_vault_env(daemon, {"GITHUB_TOKEN": "rotated"})
    assert second["removed"] == ["OLD_KEY"] and second["present"] == ["GITHUB_TOKEN"]
    assert first["version"] != second["version"], "a rotated value must change the version"
    assert daemon.vault_env == {"GITHUB_TOKEN": "rotated"}
    assert SECRET not in json.dumps(first) and "rotated" not in json.dumps(daemon.status())
    assert daemon.status()["vault_env_names"] == ["GITHUB_TOKEN"]


def test_platform_credentials_never_enter_the_vault_set() -> None:
    daemon = _daemon()
    ma.apply_vault_env(daemon, {"MATRX_CLOUD_FILES_TOKEN": "t", "A": "1"})
    assert daemon.vault_env == {"A": "1"}


def test_every_exec_carries_the_vault_and_the_caller_wins(monkeypatch) -> None:
    daemon = _daemon()
    ma.apply_vault_env(daemon, {"GITHUB_TOKEN": SECRET, "SHARED": "vault"})
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content))
        return httpx.Response(200, text='data: {"type": "exit", "exit_code": 0}\n\n')

    real = httpx.AsyncClient
    monkeypatch.setattr(
        httpx, "AsyncClient", lambda **kw: real(transport=httpx.MockTransport(handler), **kw)
    )
    asyncio.run(ma.run_exec(daemon, {"command": "env", "env": {"SHARED": "caller"}}, timeout=5))
    assert seen[0]["env"] == {"GITHUB_TOKEN": SECRET, "SHARED": "caller"}


def test_the_terminal_reads_the_same_vault_from_tmpfs(tmp_path) -> None:
    """Machines plan 4b part 2: the daemon's /pty shell gets the owner's Vault. Break: the
    vault reaching exec only, so a person's terminal lacks the keys their agent has."""
    daemon = _daemon()
    daemon.git_token_path = str(tmp_path / "git" / "token")
    daemon.pty_env_path = str(tmp_path / "vault" / "pty-env.json")
    assert daemon._env()["MATRX_AGENT_PTY_ENV_FILE"] == daemon.pty_env_path
    ma.apply_vault_env(daemon, {"OPENAI_API_KEY": SECRET, "B": "2"})
    path = tmp_path / "vault" / "pty-env.json"
    assert json.loads(path.read_text()) == {"OPENAI_API_KEY": SECRET, "B": "2"}
    assert (path.stat().st_mode & 0o777) == 0o600
    ma.apply_vault_env(daemon, {"B": "3"})
    assert json.loads(path.read_text()) == {"B": "3"}, "a removed name must leave the terminal"
    ma.apply_vault_env(daemon, {})
    assert not path.exists()
