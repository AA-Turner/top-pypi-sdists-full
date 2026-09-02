from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

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


def test_package_migration_matches_canonical_domain_model_columns() -> None:
    migration = (Path(__file__).parents[1] / "domain_config_schema.sql").read_text()

    for column in (
        "scrape_domain_id",
        "path_pattern",
        "policy_action",
        "min_content_chars",
        "min_real_content_chars",
        "content_selector",
        "policy_notes",
        "category",
        "category_reason",
    ):
        assert column in migration
