"""Shared test fixtures for heylead MCP client tests.

Redirects the DB to a temp directory so tests never touch the real ~/.heylead.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolated_heylead_home(tmp_path: Path, monkeypatch):
    """Redirect _heylead_home() to a temp directory per test."""
    from heylead import config
    from heylead.db import schema as schema_mod

    # Reset the singleton DB connection so each test gets a fresh one
    monkeypatch.setattr(schema_mod, "_conn", None)

    monkeypatch.setattr(config, "_heylead_home", lambda: tmp_path / ".heylead")
    # Ensure dirs exist
    config.ensure_dirs()
    yield
