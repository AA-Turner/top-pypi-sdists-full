"""The person's memory on the machine: a read-only rendering of ``users.user_memory``.

Breaks it guards against: a machine with no memory (the overnight audit's V9), a stale file
surviving after its row is gone, a pushed path escaping ``~/.matrx/memory``, the rendering being
writable as if it were the home of the memory, and Claude Code in the terminal never seeing it
(or the person's own ~/.claude/CLAUDE.md lines being clobbered).
"""

from __future__ import annotations

import stat
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_scraper.cloud_browser.worker import machine_memory as mm
from matrx_scraper.cloud_browser.worker.http_app import MACHINE_CAPABILITIES


def _payload(files: list[dict], rendering: str = "# Memory\n") -> dict:
    return {"source": "personal", "files": files, "rendering": rendering}


def test_files_land_read_only_and_a_removed_row_leaves(tmp_path: Path) -> None:
    home = tmp_path
    first = mm.apply_memory(str(home), _payload([
        {"path": "preferences.md", "content": "Prefers tabs."},
        {"path": "/memories/work/clients.md", "content": "Acme"},
    ], "# Memory\nPrefers tabs.\n"))
    root = home / ".matrx" / "memory"
    assert (root / "preferences.md").read_text() == "Prefers tabs."
    assert (root / "work" / "clients.md").read_text() == "Acme", "a /memories/ prefix maps under the root"
    assert first["files"] == 2 and first["source"] == "personal"
    mode = (root / "preferences.md").stat().st_mode
    assert not mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH), "the rendering is read-only"
    assert (home / ".matrx" / "MEMORY.md").read_text() == "# Memory\nPrefers tabs.\n"

    second = mm.apply_memory(str(home), _payload([{"path": "preferences.md", "content": "Prefers spaces."}]))
    assert (root / "preferences.md").read_text() == "Prefers spaces."
    assert not (root / "work").exists(), "a row that is gone must leave the machine"
    assert second["files"] == 1


def test_a_path_never_escapes_the_memory_root(tmp_path: Path) -> None:
    answer = mm.apply_memory(str(tmp_path), _payload([
        {"path": "../../.bashrc", "content": "evil"},
        {"path": "/etc/passwd", "content": "evil"},
        {"path": "ok.md", "content": "fine"},
    ]))
    assert not (tmp_path / ".bashrc").exists()
    assert (tmp_path / ".matrx" / "memory" / "etc" / "passwd").exists() or answer["skipped"]
    assert "../../.bashrc" in answer["skipped"]
    assert (tmp_path / ".matrx" / "memory" / "ok.md").read_text() == "fine"


def test_empty_memory_still_writes_an_honest_rendering(tmp_path: Path) -> None:
    mm.apply_memory(str(tmp_path), _payload([{"path": "a.md", "content": "x"}]))
    mm.apply_memory(str(tmp_path), {"source": "none:not_the_owner", "files": [], "rendering": "# Memory\n(none)\n"})
    assert not (tmp_path / ".matrx" / "memory" / "a.md").exists()
    assert (tmp_path / ".matrx" / "MEMORY.md").read_text() == "# Memory\n(none)\n"


def test_claude_code_imports_it_and_the_persons_lines_stay(tmp_path: Path) -> None:
    claude = tmp_path / ".claude" / "CLAUDE.md"
    claude.parent.mkdir()
    claude.write_text("My own rule: be brief.\n")
    mm.apply_memory(str(tmp_path), _payload([]))
    mm.apply_memory(str(tmp_path), _payload([]))
    text = claude.read_text()
    assert text.startswith("My own rule: be brief.\n")
    assert text.count("@~/.matrx/MEMORY.md") == 1, "the import is added once, never repeated"


def test_the_door_needs_the_agent_token_and_applies(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert "person_memory" in MACHINE_CAPABILITIES
    app = FastAPI()
    seen: list[str] = []

    def verify(token: str) -> None:
        seen.append(token)
        if token != "good":
            raise PermissionError("bad token")

    mm.install_memory_route(app, home=str(tmp_path), verify=verify)
    client = TestClient(app)
    assert client.post("/machine/memory", json=_payload([])).status_code == 401
    ok = client.post("/machine/memory", json=_payload([{"path": "p.md", "content": "hi"}]),
                     headers={"X-Sandbox-Access-Token": "good"})
    assert ok.status_code == 200, ok.text
    assert ok.json()["files"] == 1
    assert (tmp_path / ".matrx" / "memory" / "p.md").read_text() == "hi"
    assert client.post("/machine/memory", json={"files": "no"},
                       headers={"X-Sandbox-Access-Token": "good"}).status_code == 422
