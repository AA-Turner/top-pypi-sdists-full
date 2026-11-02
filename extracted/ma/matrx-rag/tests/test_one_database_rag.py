"""`rag.*` may only ever resolve to the ONE database (Matrx Main).

matrx-rag used to carry a second-database fallback ladder — `RAG_DATABASE_URL`
→ `DATABASE_URL` → `MATRX_RAG_POSTGRES_*` → `SUPABASE_MATRIX_*`. The identical
ladder in sibling matrx-scraper was LIVE in production: the standalone service
bound the shared `scraper.*` tables to a Coolify-local Postgres and wrote 14
rows the platform never saw. These tests make the RAG version un-reintroducible.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import db as rag_db

RETIRED_ENV_VARS = {
    "RAG_DATABASE_URL": "postgresql://a:b@rag-postgres.internal:5434/rag_db",
    "DATABASE_URL": "postgresql://a:b@rag-postgres.internal:5434/rag_db",
    "MATRX_RAG_POSTGRES_HOST": "rag-postgres.internal",
    "MATRX_RAG_POSTGRES_PORT": "5434",
    "MATRX_RAG_POSTGRES_NAME": "rag_db",
    "MATRX_RAG_POSTGRES_USER": "postgres",
    "MATRX_RAG_POSTGRES_PASSWORD": "secret",
}


def _capture_register_from_env(
    monkeypatch: pytest.MonkeyPatch, *, ok: bool = True
) -> list[dict[str, Any]]:
    """Stub the ORM registration seam; hard-fail the raw-URL registration path."""
    captured: list[dict[str, Any]] = []

    def fake_register_from_env(**kwargs: Any) -> bool:
        captured.append(kwargs)
        return ok

    monkeypatch.setattr("matrx_orm.is_database_registered", lambda name: False)
    monkeypatch.setattr("matrx_orm.register_database_from_env", fake_register_from_env)
    monkeypatch.setattr(
        "matrx_orm.register_database",
        lambda config: pytest.fail(
            "matrx-rag must never register a pool from a raw connection URL — "
            "`rag.*` binds to the ONE database via SUPABASE_MATRIX_*"
        ),
        raising=False,
    )
    monkeypatch.setattr(rag_db, "_register_models", lambda **kwargs: None)
    return captured


def test_bootstrap_binds_rag_schema_to_the_one_platform_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured = _capture_register_from_env(monkeypatch)

    assert rag_db.bootstrap_db() == rag_db.PACKAGE_DB_NAME

    assert len(captured) == 1
    kwargs = captured[0]
    assert kwargs["name"] == rag_db.PACKAGE_DB_NAME
    assert kwargs["env_prefix"] == "SUPABASE_MATRIX"
    assert kwargs["env_var_overrides"] == {"NAME": "SUPABASE_MATRIX_DATABASE_NAME"}
    assert kwargs["additional_schemas"] == ["rag", "docproc", "auth"]
    # ssl is left to the deployment (SUPABASE_MATRIX_SSL) so a local or
    # client-owned Postgres is reachable — never hardcoded here.
    assert kwargs["ssl"] is None


def test_bootstrap_ignores_every_retired_second_database_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A service-local Postgres URL must NOT be able to fork `rag.*`."""
    for var, value in RETIRED_ENV_VARS.items():
        monkeypatch.setenv(var, value)
    captured = _capture_register_from_env(monkeypatch)

    rag_db.bootstrap_db()

    # register_database (the URL path) hard-fails in the stub above; the only
    # accepted resolution is the platform env prefix.
    assert [k["env_prefix"] for k in captured] == ["SUPABASE_MATRIX"]


def test_connection_url_uses_the_platform_prefix_and_ignores_the_retired_ladder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for var, value in RETIRED_ENV_VARS.items():
        monkeypatch.setenv(var, value)
    monkeypatch.setenv("SUPABASE_MATRIX_HOST", "aws-0-us-west-1.pooler.supabase.com")
    monkeypatch.setenv("SUPABASE_MATRIX_PORT", "6543")
    monkeypatch.setenv("SUPABASE_MATRIX_DATABASE_NAME", "postgres")
    monkeypatch.setenv("SUPABASE_MATRIX_USER", "platform_user")
    monkeypatch.setenv("SUPABASE_MATRIX_PASSWORD", "platform_pw")

    url = rag_db.connection_url()

    assert url == (
        "postgresql://platform_user:platform_pw"
        "@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    )
    assert "rag-postgres.internal" not in url


def test_connection_url_raises_rather_than_falling_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for var, value in RETIRED_ENV_VARS.items():
        monkeypatch.setenv(var, value)
    for var in ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_USER", "SUPABASE_MATRIX_PASSWORD"):
        monkeypatch.delenv(var, raising=False)

    with pytest.raises(RuntimeError, match="SUPABASE_MATRIX"):
        rag_db.connection_url()


def test_bootstrap_raises_when_the_one_database_cannot_be_resolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No fallback, no 'optional' — an unresolvable platform DB is fatal."""
    _capture_register_from_env(monkeypatch, ok=False)

    with pytest.raises(RuntimeError, match="SUPABASE_MATRIX"):
        rag_db.bootstrap_db()


def test_binding_module_exposes_no_second_database_seam() -> None:
    """Structural pin: the retired names may not come back as module constants."""
    for retired in ("STANDALONE_ENV_PREFIX", "_register_from_database_url"):
        assert not hasattr(rag_db, retired), (
            f"matrx_rag.db.{retired} is the second-database fallback ladder — "
            "`rag.*` resolves to the ONE database via SUPABASE_MATRIX_* only"
        )
    assert rag_db.DB_ENV_PREFIX == "SUPABASE_MATRIX"


def test_bootstrap_signature_has_no_env_prefix_override() -> None:
    """A caller must not be able to point `rag.*` at another env prefix."""
    import inspect

    params = inspect.signature(rag_db.bootstrap_db).parameters
    assert "env_prefix" not in params
    assert "env_var_overrides" not in params
