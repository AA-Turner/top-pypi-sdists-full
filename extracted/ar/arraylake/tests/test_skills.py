"""Lifecycle test for `al skills install` against a local HTTP server."""

from __future__ import annotations

import http.server
import json
import socketserver
import threading
from pathlib import Path

from typer.testing import CliRunner

from arraylake.cli.main import app as cli_app


def _serve_skills(tmp_root: Path) -> tuple[str, socketserver.TCPServer]:
    handler = lambda *args, **kw: http.server.SimpleHTTPRequestHandler(  # noqa: E731
        *args, directory=str(tmp_root), **kw
    )
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    return f"http://127.0.0.1:{port}", server


def _write_fake_skill(
    root: Path,
    *,
    skill_text: str,
    reference_text: str,
    files: list[str] | None = None,
) -> None:
    manifest_files = files or ["SKILL.md", "references/x.md"]
    skill = root / "demo"
    (skill / "references").mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text(skill_text)
    (skill / "references" / "x.md").write_text(reference_text)
    manifest = {
        "manifest_version": 1,
        "generated_at": "2026-01-01T00:00:00Z",
        "skills": [
            {
                "name": "demo",
                "version": "0.1",
                "min_client_version": "0.0.0",
                "description": "demo skill",
                "files": manifest_files,
                "resources": [{"path": "references/x.md", "description": "demo reference"}],
            }
        ],
    }
    (root / "manifest.json").write_text(json.dumps(manifest))


def _assert_installed_skill(skill: Path, *, skill_text: str, reference_text: str) -> None:
    assert skill.is_dir()
    assert not skill.is_symlink()
    assert (skill / "SKILL.md").read_text() == skill_text
    assert (skill / "references" / "x.md").read_text() == reference_text


def test_skills_install_lifecycle(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    legacy_source = tmp_path / "legacy"
    legacy_source.mkdir()
    (legacy_source / "marker").write_text("legacy")
    claude_skills_dir = tmp_path / ".claude" / "skills"
    claude_skills_dir.mkdir(parents=True)
    (claude_skills_dir / "demo").symlink_to(legacy_source, target_is_directory=True)

    server_root = tmp_path / "server"
    server_root.mkdir()
    _write_fake_skill(server_root, skill_text="v1\n", reference_text="# x v1\n")
    url, server = _serve_skills(server_root)
    try:
        result = runner.invoke(cli_app, ["skills", "install", "--project", "--url", url])
        assert result.exit_code == 0, result.output

        claude_skill = tmp_path / ".claude" / "skills" / "demo"
        agents_skill = tmp_path / ".agents" / "skills" / "demo"
        for skill in (claude_skill, agents_skill):
            _assert_installed_skill(skill, skill_text="v1\n", reference_text="# x v1\n")
        assert not (claude_skill / "marker").exists()

        _write_fake_skill(server_root, skill_text="v2\n", reference_text="# x v2\n")
        result = runner.invoke(cli_app, ["skills", "install", "--project", "--url", url])
        assert result.exit_code == 0, result.output
        for skill in (claude_skill, agents_skill):
            _assert_installed_skill(skill, skill_text="v2\n", reference_text="# x v2\n")

        _write_fake_skill(
            server_root,
            skill_text="broken\n",
            reference_text="# broken\n",
            files=["SKILL.md", "references/missing.md"],
        )
        result = runner.invoke(cli_app, ["skills", "install", "--project", "--url", url])
        assert result.exit_code != 0
        assert "error" in result.output
        for base, skill in (
            (tmp_path / ".claude" / "skills", claude_skill),
            (tmp_path / ".agents" / "skills", agents_skill),
        ):
            _assert_installed_skill(skill, skill_text="v2\n", reference_text="# x v2\n")
            assert not any(path.name.startswith(".arraylake-skill-") for path in base.iterdir())
    finally:
        server.shutdown()
        server.server_close()
