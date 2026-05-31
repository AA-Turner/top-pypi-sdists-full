"""S1 — WEB_EDITOR_DATABASE_URI is captured once at module import.

The env var is the single switch between the file-based and PostgreSQL backends
(invariant §6). We verify it is read from the environment at import time and that
its absence yields ``None``.
"""

import importlib

import abstra_internals.environment as environment


def _reload_with(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("ABSTRA_WEB_EDITOR_DATABASE_URI", raising=False)
    else:
        monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", value)
    return importlib.reload(environment)


def test_db_uri_absent_is_none(monkeypatch):
    try:
        reloaded = _reload_with(monkeypatch, None)
        assert reloaded.WEB_EDITOR_DATABASE_URI is None
    finally:
        monkeypatch.undo()
        importlib.reload(environment)


def test_db_uri_present_is_captured(monkeypatch):
    uri = "postgresql://web_editor_p:secret@host:5432/web_editor_p"
    try:
        reloaded = _reload_with(monkeypatch, uri)
        assert reloaded.WEB_EDITOR_DATABASE_URI == uri
    finally:
        monkeypatch.undo()
        importlib.reload(environment)
