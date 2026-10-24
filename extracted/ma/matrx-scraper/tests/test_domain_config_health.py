"""Domain-config store health and the package migration's model parity.

SUTs:
- `PostgresDomainConfigStore.start` / `.refresh` — OWN the `healthy` verdict
  readiness reads. A store that failed to load (at boot OR on a later refresh)
  must never report healthy: every fetch would silently run on default policy.
- `server.app._readiness_snapshot` — OWNS turning an unhealthy store into 503.
- `domain_config_schema.sql` — its legacy `scraper.*` compatibility views retain
  `is_public` and project every column the generated models read. Current live
  storage uses physical `scraper.*` tables without that legacy column.
The Postgres loader (`_load_all_domains`) is the doubled dependency.
"""

from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_scraper.db.models_scraper import ScrapeDomain, ScrapePathPattern
from matrx_scraper.domain_config import PostgresDomainConfigStore
from matrx_scraper.server import app as server_app


@pytest.mark.asyncio
async def test_initial_domain_config_failure_is_not_registered_as_healthy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = PostgresDomainConfigStore(pool=object())
    monkeypatch.setattr(
        store,
        "_load_all_domains",
        AsyncMock(side_effect=RuntimeError("schema mismatch")),
    )

    with pytest.raises(RuntimeError, match="initial load failed"):
        await store.start()

    assert store.healthy is False
    assert store._refresh_task is None


@pytest.mark.asyncio
async def test_successful_empty_domain_catalog_is_healthy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = PostgresDomainConfigStore(pool=object())
    monkeypatch.setattr(store, "_load_all_domains", AsyncMock(return_value=[]))

    await store.start()
    try:
        assert store.healthy is True
        assert store.all_domains == []
    finally:
        await store.stop()


@pytest.mark.asyncio
async def test_a_failed_refresh_after_a_healthy_start_reports_unhealthy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Break: the refresh error path forgets to drop `healthy`, so a store whose
    table vanished mid-life keeps readiness green while policy goes dark."""
    store = PostgresDomainConfigStore(pool=object())
    loader = AsyncMock(return_value=[])
    monkeypatch.setattr(store, "_load_all_domains", loader)
    await store.start()
    try:
        assert store.healthy is True  # precondition: it started healthy
        loader.side_effect = RuntimeError("relation scraper.scrape_domain does not exist")

        await store.refresh()

        assert store.healthy is False, (
            "domain-config refresh failed but the store still reports healthy — "
            "readiness would stay green while every fetch runs on default policy"
        )
    finally:
        await store.stop()


def test_readiness_fails_when_registered_domain_store_is_unhealthy(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    set_matrx_base_dir,
) -> None:
    set_matrx_base_dir(tmp_path)
    monkeypatch.setattr(server_app, "has_ext", lambda name: True)
    file_manager = SimpleNamespace(
        sync_engine=SimpleNamespace(
            _config=SimpleNamespace(
                storage_backend="s3",
                resolve_s3_bucket=lambda: "canonical-bucket",
            )
        ),
        cloud=SimpleNamespace(is_configured=lambda backend: backend == "s3"),
    )

    def get_ext(name: str):
        if name == "domain_config":
            return SimpleNamespace(healthy=False)
        if name == "file_manager":
            return file_manager
        if name == "canonical_file_pipeline_ready":
            return True
        return SimpleNamespace()

    monkeypatch.setattr(server_app, "get_ext", get_ext)
    monkeypatch.setattr("matrx_orm.is_database_registered", lambda name: True)
    monkeypatch.setattr(
        "matrx_files.cloud_sync.permissions.get_access_checker",
        lambda: object(),
    )

    payload, status = server_app._readiness_snapshot()

    assert status == 503
    assert payload["domain_config"] is False
    assert payload["failed_components"] == ["domain_config"]


_SCRAPER_VIEW = re.compile(
    r"CREATE OR REPLACE VIEW scraper\.(\w+) AS\s+SELECT\s+(.*?)\s+FROM\s",
    flags=re.IGNORECASE | re.DOTALL,
)


def _scraper_view_columns(sql: str) -> dict[str, set[str]]:
    return {
        table: {column.strip() for column in columns.split(",") if column.strip()}
        for table, columns in _SCRAPER_VIEW.findall(sql)
    }


def test_package_migration_views_project_the_model_and_retained_legacy_columns() -> None:
    """Census: every column of every policy model, derived from the generated
    model, plus the installer's retained legacy public flag. CREATE OR REPLACE
    VIEW cannot drop an existing view column without dropping its dependents;
    retaining that legacy projection must not add it to live-table models."""
    sql = (Path(__file__).parents[1] / "domain_config_schema.sql").read_text()
    views = _scraper_view_columns(sql)

    for model in (ScrapeDomain, ScrapePathPattern):
        table = model._table_name
        assert table in views, f"domain_config_schema.sql no longer defines view scraper.{table}"
        expected_columns = set(model._fields) | {"is_public"}
        missing = sorted(expected_columns - views[table])
        extra = sorted(views[table] - expected_columns)
        assert not missing and not extra, (
            f"scraper.{table} view drifted from {model.__name__}: missing={missing} extra={extra}"
        )

    # Self-test: the census must notice a column dropped from a view.
    doctored = sql.replace(
        ", category_reason, metadata, deleted_at,\n       test_run_id, test_expires_at\nFROM public.scrape_path_pattern",
        ", metadata, deleted_at,\n       test_run_id, test_expires_at\nFROM public.scrape_path_pattern",
    )
    assert doctored != sql, "self-test anchor moved — re-point the doctoring above"
    assert "category_reason" not in _scraper_view_columns(doctored)["scrape_path_pattern"]
