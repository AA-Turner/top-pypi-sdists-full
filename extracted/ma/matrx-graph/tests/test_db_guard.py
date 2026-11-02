"""Unit tests for the production-database refusal gate (tests/_db_guard.py).

Pure level1 — registers a local matrx-orm config, then gives the isolated
registry a synthetic fingerprint without opening a connection. This is the
second, always-running layer: the gate itself is exercised on every commit
even though the DB-writing suite it protects only runs with
MATRX_GRAPH_TEST_DB=1.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import pytest

from ._db_guard import (
    ALLOW_ENV_VAR,
    PRODUCTION_PROJECT_REFS,
    ProductionDatabaseRefused,
    assert_not_production_db,
)

_PROD_REF = PRODUCTION_PROJECT_REFS[0]


@contextmanager
def _preserved_database_registry() -> Iterator[None]:
    from matrx_orm.core.config import registry

    configs = dict(registry._configs)
    used_aliases = list(registry._used_aliases)
    name_aliases = dict(registry._name_aliases)
    try:
        yield
    finally:
        registry._configs.clear()
        registry._configs.update(configs)
        registry._used_aliases.clear()
        registry._used_aliases.extend(used_aliases)
        registry._name_aliases.clear()
        registry._name_aliases.update(name_aliases)


@pytest.fixture(autouse=True)
def _restore_database_registry() -> Iterator[None]:
    with _preserved_database_registry():
        yield


def _register(monkeypatch: pytest.MonkeyPatch, name: str, *, host: str, user: str) -> None:
    prefix = f"DBGUARD_TEST_{name.upper()}"
    monkeypatch.setenv(f"{prefix}_HOST", "127.0.0.1")
    monkeypatch.setenv(f"{prefix}_PORT", "5432")
    monkeypatch.setenv(f"{prefix}_NAME", "postgres")
    monkeypatch.setenv(f"{prefix}_USER", "postgres")
    monkeypatch.setenv(f"{prefix}_PASSWORD", "not-a-real-password")

    from matrx_orm import register_database_from_env
    from matrx_orm.core.config import registry

    assert register_database_from_env(name=name, env_prefix=prefix)
    # The pytest-wide connection door correctly refuses production even at
    # registration. Exercise this older pre-write guard on inert registry data.
    registry._configs[name].host = host
    registry._configs[name].user = user


def test_refuses_direct_production_host(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ALLOW_ENV_VAR, raising=False)
    _register(
        monkeypatch,
        "dbguard_prod_host",
        host=f"db.{_PROD_REF}.supabase.co",
        user="postgres",
    )
    with pytest.raises(ProductionDatabaseRefused, match="REFUSING"):
        assert_not_production_db("dbguard_prod_host")


def test_refuses_pooler_user_fingerprint(monkeypatch: pytest.MonkeyPatch) -> None:
    """The pooler host carries no project ref — the USER does."""
    monkeypatch.delenv(ALLOW_ENV_VAR, raising=False)
    _register(
        monkeypatch,
        "dbguard_prod_pooler",
        host="aws-0-us-west-1.pooler.supabase.com",
        user=f"postgres.{_PROD_REF}",
    )
    with pytest.raises(ProductionDatabaseRefused, match=_PROD_REF):
        assert_not_production_db("dbguard_prod_pooler")


def test_allows_non_production_db(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ALLOW_ENV_VAR, raising=False)
    _register(monkeypatch, "dbguard_local", host="127.0.0.1", user="postgres")
    assert_not_production_db("dbguard_local")  # must not raise


def test_explicit_escape_hatch_bypasses(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ALLOW_ENV_VAR, "1")
    _register(
        monkeypatch,
        "dbguard_prod_allowed",
        host=f"db.{_PROD_REF}.supabase.co",
        user="postgres",
    )
    assert_not_production_db("dbguard_prod_allowed")  # must not raise


def test_registry_isolation_restores_prior_config_and_name_alias(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_orm import register_database_alias
    from matrx_orm.core.config import DatabaseProjectConfig, registry

    prior = DatabaseProjectConfig(
        name="dbguard_prior",
        alias="dbguard_prior",
        host="127.0.0.1",
        port="5432",
        database_name="prior",
        user="postgres",
        password="prior-password",
    )
    registry.register(prior)
    register_database_alias("dbguard_prior_alias", "dbguard_prior")
    expected_configs = dict(registry._configs)
    expected_used_aliases = list(registry._used_aliases)
    expected_name_aliases = dict(registry._name_aliases)

    with _preserved_database_registry():
        _register(
            monkeypatch,
            "dbguard_restore_probe",
            host=f"db.{_PROD_REF}.supabase.co",
            user="postgres",
        )
        register_database_alias("dbguard_probe_alias", "dbguard_restore_probe")

    assert registry._configs == expected_configs
    assert registry._used_aliases == expected_used_aliases
    assert registry._name_aliases == expected_name_aliases
