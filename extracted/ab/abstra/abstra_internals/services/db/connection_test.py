"""S2 — connection module: pool, single connection, close, masking.

The DB-backed assertions (pool singleton, autocommit, check_connection) use the
ephemeral container fixture and skip without Docker. The no-env ``RuntimeError``
and password-masking assertions need no DB.
"""

import importlib

import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection


def _reload_connection_with_uri(monkeypatch, uri):
    if uri is None:
        monkeypatch.delenv("ABSTRA_WEB_EDITOR_DATABASE_URI", raising=False)
    else:
        monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", uri)
    importlib.reload(environment)
    return importlib.reload(connection)


def _restore(monkeypatch):
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)


# --- No-DB assertions -------------------------------------------------------


def test_get_pool_without_env_raises_without_leaking_uri(monkeypatch):
    try:
        conn_mod = _reload_connection_with_uri(monkeypatch, None)
        with pytest.raises(RuntimeError) as exc:
            conn_mod.get_pool()
        assert "ABSTRA_WEB_EDITOR_DATABASE_URI" in str(exc.value)
    finally:
        _restore(monkeypatch)


def test_new_connection_without_env_raises(monkeypatch):
    try:
        conn_mod = _reload_connection_with_uri(monkeypatch, None)
        with pytest.raises(RuntimeError):
            conn_mod.new_connection()
    finally:
        _restore(monkeypatch)


def test_runtime_error_text_never_contains_a_password(monkeypatch):
    secret = "sup3rs3cr3t"
    try:
        conn_mod = _reload_connection_with_uri(
            monkeypatch, f"postgresql://u:{secret}@h:5432/db"
        )
        # Force the missing-URI path is not relevant here; instead assert the
        # masking helper redacts both URI and keyword forms.
        assert secret not in conn_mod.mask_dsn_password(
            f"could not connect: postgresql://u:{secret}@h:5432/db"
        )
        assert secret not in conn_mod.mask_dsn_password(
            f"connection failed host=h password={secret} dbname=db"
        )
    finally:
        _restore(monkeypatch)


# --- DB-backed assertions (need Docker) -------------------------------------


def test_get_pool_is_singleton_and_autocommit(monkeypatch, pg_uri):
    try:
        conn_mod = _reload_connection_with_uri(monkeypatch, pg_uri)
        pool_a = conn_mod.get_pool()
        pool_b = conn_mod.get_pool()
        assert pool_a is pool_b  # singleton
        with pool_a.connection() as conn:
            assert conn.autocommit is True
            assert conn.execute("SELECT 1").fetchone()[0] == 1
        conn_mod.close_pool()
        pool_c = conn_mod.get_pool()
        assert pool_c is not pool_a  # close_pool resets the singleton
        conn_mod.close_pool()
    finally:
        _restore(monkeypatch)


def test_pool_configured_with_check_connection(monkeypatch, pg_uri):
    from psycopg_pool import ConnectionPool

    try:
        conn_mod = _reload_connection_with_uri(monkeypatch, pg_uri)
        pool = conn_mod.get_pool()
        # psycopg_pool stores the constructor's ``check`` callable on ``_check``
        # (``pool.check`` is the pool's own validate-idle method).
        assert pool._check is ConnectionPool.check_connection
        conn_mod.close_pool()
    finally:
        _restore(monkeypatch)


def test_new_connection_autocommit(monkeypatch, pg_uri):
    try:
        conn_mod = _reload_connection_with_uri(monkeypatch, pg_uri)
        conn = conn_mod.new_connection()
        try:
            assert conn.autocommit is True
            assert conn.execute("SELECT 1").fetchone()[0] == 1
        finally:
            conn.close()
    finally:
        _restore(monkeypatch)
