"""Tests for sage.core.env_sync (no network)."""

from __future__ import annotations

from pathlib import Path

from sage.core.env_sync import (
    discover_github_secret_names_from_workflows,
    ensure_gitignore_for_monorepo,
    run_startup_env_maintenance,
    select_keys_for_github_sync,
)


def test_select_keys_prefers_vite_and_workflow_names(tmp_path: Path) -> None:
    env = {
        "VITE_FIREBASE_API_KEY": "a",
        "VITE_FIREBASE_AUTH_DOMAIN": "b",
        "FOO_BAR": "skip",
        "ADMIN_TOKEN": "t",
    }
    wf = frozenset({"ADMIN_TOKEN", "MISSING_IN_ENV"})
    out = select_keys_for_github_sync(env, wf, only_prefix=None, extra_keys=None)
    assert out["VITE_FIREBASE_API_KEY"] == "a"
    assert out["ADMIN_TOKEN"] == "t"
    assert "FOO_BAR" not in out


def test_select_keys_prefix_filter(tmp_path: Path) -> None:
    env = {"VITE_X": "1", "OTHER": "2"}
    out = select_keys_for_github_sync(env, frozenset(), only_prefix="VITE_", extra_keys=None)
    assert list(out.keys()) == ["VITE_X"]


def test_discover_workflow_secret_refs(tmp_path: Path) -> None:
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "deploy.yml").write_text(
        'jobs:\n  x:\n    env:\n      K: ${{ secrets.VITE_FIREBASE_API_KEY }}\n',
        encoding="utf-8",
    )
    names = discover_github_secret_names_from_workflows(tmp_path)
    assert "VITE_FIREBASE_API_KEY" in names


def test_run_startup_env_maintenance_updates_gitignore_only(tmp_path: Path) -> None:
    import os

    (tmp_path / ".git").mkdir()
    prev = os.environ.pop("SAGE_SYNC_SECRETS_TO_GITHUB", None)
    try:
        msgs = run_startup_env_maintenance(tmp_path)
    finally:
        if prev is not None:
            os.environ["SAGE_SYNC_SECRETS_TO_GITHUB"] = prev
    assert any("gitignore" in m.lower() for m in msgs)


def test_ensure_gitignore_writes_entries(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    updated = ensure_gitignore_for_monorepo(tmp_path)
    assert updated
    gi = Path(updated[0])
    text = gi.read_text(encoding="utf-8")
    assert ".env" in text
    assert "!.env.example" in text
