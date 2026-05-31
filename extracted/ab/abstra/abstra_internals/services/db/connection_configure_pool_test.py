"""Per-process pool sizing: configure_pool() sets the ConnectionPool max_size.

No Docker needed — the psycopg_pool.ConnectionPool constructor is mocked so we
only assert the max_size it is created with.
"""

import importlib
from unittest.mock import MagicMock, patch

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection

FAKE_URI = "postgresql://u:p@h:5432/db"


def _reload_with_uri(monkeypatch):
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", FAKE_URI)
    importlib.reload(environment)
    return importlib.reload(connection)


def _restore(monkeypatch):
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)


def _create_pool_kwargs(conn_mod):
    """Trigger pool creation with a mocked ConnectionPool and return its kwargs."""
    with patch("psycopg_pool.ConnectionPool", return_value=MagicMock()) as ctor:
        conn_mod.get_pool()
    return ctor.call_args.kwargs


def test_configure_pool_sets_max_size(monkeypatch):
    conn_mod = _reload_with_uri(monkeypatch)
    try:
        conn_mod.configure_pool(max_size=3)
        assert _create_pool_kwargs(conn_mod)["max_size"] == 3
    finally:
        conn_mod._reset_pool_for_tests()
        _restore(monkeypatch)


def test_executor_worker_size_two(monkeypatch):
    conn_mod = _reload_with_uri(monkeypatch)
    try:
        conn_mod.configure_pool(max_size=2)
        assert _create_pool_kwargs(conn_mod)["max_size"] == 2
    finally:
        conn_mod._reset_pool_for_tests()
        _restore(monkeypatch)


def test_default_max_size_when_not_configured(monkeypatch):
    conn_mod = _reload_with_uri(monkeypatch)
    try:
        assert _create_pool_kwargs(conn_mod)["max_size"] == conn_mod._DEFAULT_MAX_SIZE
    finally:
        conn_mod._reset_pool_for_tests()
        _restore(monkeypatch)


def test_reset_for_tests_restores_default_size(monkeypatch):
    conn_mod = _reload_with_uri(monkeypatch)
    try:
        conn_mod.configure_pool(max_size=3)
        conn_mod._reset_pool_for_tests()
        # After a reset the next process-equivalent starts from the default again.
        assert _create_pool_kwargs(conn_mod)["max_size"] == conn_mod._DEFAULT_MAX_SIZE
    finally:
        conn_mod._reset_pool_for_tests()
        _restore(monkeypatch)
