from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_scraper import configure_db
from matrx_scraper import db as scraper_db
from matrx_scraper.db import web as web_db
from matrx_scraper.server import app as server_app
from matrx_scraper.server.config import ServerConfig


class _OwnedOrmPool:
    async def close(self) -> None:
        raise AssertionError("the standalone server must not close matrx-orm's shared pool")


def test_host_configuration_binds_scraper_and_web_models(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str]] = []
    monkeypatch.setattr(
        scraper_db,
        "bind_to_host",
        lambda name: calls.append(("scraper", name)),
    )
    monkeypatch.setattr(
        web_db,
        "bind_web_to_host",
        lambda name: calls.append(("web", name)),
    )

    configure_db("host_database")

    assert calls == [
        ("scraper", "host_database"),
        ("web", "host_database"),
    ]


@pytest.mark.asyncio
async def test_server_lifespan_bootstraps_orm_without_retired_crawl_probe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[object] = []

    def fake_bootstrap_db() -> str:
        calls.append("bootstrap")
        return scraper_db.PACKAGE_DB_NAME

    def fake_configure_ext(**kwargs: Any) -> None:
        calls.append(("configure_ext", kwargs))

    class FakeQuery:
        def limit(self, value: int) -> FakeQuery:
            return self

        async def all(self) -> list[object]:
            return []

        async def exists(self) -> bool:
            calls.append("orm_probe")
            return False

    class FakeS3:
        async def assert_bucket_accessible_async(self, bucket: str) -> None:
            calls.append(("head_bucket", bucket))

    class FakeCloud:
        s3 = FakeS3()

        def is_configured(self, scheme: str) -> bool:
            return scheme == "s3"

    fake_file_manager = SimpleNamespace(
        cloud=FakeCloud(),
        sync_engine=SimpleNamespace(
            _config=SimpleNamespace(
                storage_backend="s3",
                resolve_s3_bucket=lambda: "canonical-bucket",
            )
        ),
    )

    class FakeCloudSyncConfig:
        storage_backend = "s3"

        def __init__(self, **kwargs: object) -> None:
            pass

        def resolve_s3_bucket(self) -> str:
            return "canonical-bucket"

    async def fake_probe_database_readiness(**kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(ready=True, error_type=None)

    monkeypatch.setattr(scraper_db, "bootstrap_db", fake_bootstrap_db)
    monkeypatch.setattr(server_app, "configure_ext", fake_configure_ext)
    monkeypatch.setattr("matrx_scraper.db.web.bootstrap_web_db", lambda: None)
    monkeypatch.setattr("matrx_files.db.bind_to_host", lambda name: None)
    access_checkers: list[object] = []
    monkeypatch.setattr(
        "matrx_files.configure_access_checker",
        lambda checker, **kwargs: access_checkers.append(checker),
    )
    monkeypatch.setattr("matrx_files.FileManager", lambda *args, **kwargs: fake_file_manager)
    monkeypatch.setattr("matrx_files.cloud_sync.CloudSyncConfig", FakeCloudSyncConfig)
    monkeypatch.setattr(
        "matrx_files.db.readiness.probe_database_readiness",
        fake_probe_database_readiness,
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.WebCrawlRepository.fail_stale_sessions",
        AsyncMock(return_value=0),
    )
    monkeypatch.setattr(
        "matrx_scraper.db.models_web.Snapshot.filter",
        lambda **kwargs: FakeQuery(),
    )
    monkeypatch.setattr(
        "matrx_scraper.db.models_web.Screenshot.filter",
        lambda **kwargs: FakeQuery(),
    )
    monkeypatch.setattr(
        "matrx_scraper.db.models_scraper.ScrapeParsedPage.filter",
        lambda **kwargs: FakeQuery(),
    )
    # The legacy `scraper.crawl_*` models are GONE as of 2026-08-09, so the
    # "startup must not probe retired crawl tables" trap that used to sit here
    # is now enforced by the type system: there is no CrawlRuns to import.
    # `test_no_legacy_crawl_models_remain` below is the standing guard.
    fake_cache = object()
    monkeypatch.setattr("matrx_scraper.cache.TwoTierCache", lambda: fake_cache)
    # The cache, domain-config store, and browser pool are unconditional now —
    # there is no config field to switch them off. Keep the unit test off the
    # real subsystems: no Playwright, and a domain-config store that no-ops.
    monkeypatch.setattr(server_app, "PLAYWRIGHT_AVAILABLE", False)
    monkeypatch.setattr(
        "matrx_scraper.domain_config.PostgresDomainConfigStore",
        lambda *a, **k: SimpleNamespace(start=AsyncMock(), stop=AsyncMock(), healthy=True),
    )

    app = SimpleNamespace(state=SimpleNamespace(config=ServerConfig()))

    async with server_app._lifespan(app):
        assert calls.index("bootstrap") < calls.index("orm_probe")
        assert ("head_bucket", "canonical-bucket") in calls
        configure_call = next(
            call for call in calls if isinstance(call, tuple) and call[0] == "configure_ext"
        )
        assert "db_pool" not in configure_call[1]
        assert configure_call[1]["cache"] is fake_cache
        assert configure_call[1]["file_manager"] is fake_file_manager
        assert configure_call[1]["canonical_file_pipeline_ready"] is True
        assert access_checkers == [server_app.canonical_file_access_allowed]


@pytest.mark.asyncio
async def test_server_lifespan_fails_hard_when_scraper_database_bootstrap_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The scraper DB is NOT optional — booting without it left cache/policy/retry dark."""

    def boom() -> str:
        raise RuntimeError("no platform database")

    monkeypatch.setattr(scraper_db, "bootstrap_db", boom)
    monkeypatch.setattr("matrx_scraper.db.web.bootstrap_web_db", lambda: None)
    monkeypatch.setattr("matrx_files.db.bind_to_host", lambda name: None)
    monkeypatch.setattr("matrx_files.configure_access_checker", lambda checker, **kwargs: None)

    fake_file_manager = SimpleNamespace(
        cloud=SimpleNamespace(
            is_configured=lambda scheme: True,
            s3=SimpleNamespace(assert_bucket_accessible_async=AsyncMock(return_value=None)),
        ),
    )
    monkeypatch.setattr("matrx_files.FileManager", lambda *args, **kwargs: fake_file_manager)
    monkeypatch.setattr(
        "matrx_files.cloud_sync.CloudSyncConfig",
        lambda **kwargs: SimpleNamespace(
            storage_backend="s3", resolve_s3_bucket=lambda: "canonical-bucket"
        ),
    )

    async def fake_probe(**kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(ready=True, error_type=None)

    monkeypatch.setattr("matrx_files.db.readiness.probe_database_readiness", fake_probe)

    class FakeQuery:
        def limit(self, value: int) -> FakeQuery:
            return self

        async def all(self) -> list[object]:
            return []

    monkeypatch.setattr("matrx_scraper.db.models_web.Snapshot.filter", lambda **k: FakeQuery())
    monkeypatch.setattr("matrx_scraper.db.models_web.Screenshot.filter", lambda **k: FakeQuery())

    monkeypatch.setattr(server_app, "PLAYWRIGHT_AVAILABLE", False)
    app = SimpleNamespace(state=SimpleNamespace(config=ServerConfig()))

    with pytest.raises(RuntimeError, match="scraper database bootstrap failed"):
        async with server_app._lifespan(app):
            pass


@pytest.mark.asyncio
async def test_standalone_file_access_checker_delegates_to_canonical_db_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[object, ...]] = []

    async def fake_call_function(*args: object) -> bool:
        calls.append(args)
        return True

    monkeypatch.setattr(server_app, "call_function", fake_call_function)

    assert await server_app.canonical_file_access_allowed("user-1", "file", "file-1", "read")
    assert await server_app.canonical_file_access_allowed("user-1", "folder", "folder-1", "write")
    assert calls == [
        (
            server_app.WEB_DB_NAME,
            "files",
            "has_access_for",
            "user-1",
            "file-1",
            "viewer",
        ),
        (
            server_app.WEB_DB_NAME,
            "iam",
            "has_access_for",
            "user-1",
            "folder",
            "folder-1",
            "editor",
        ),
    ]


def _capture_register_from_env(
    monkeypatch: pytest.MonkeyPatch, *, ok: bool = True
) -> list[dict[str, Any]]:
    """Stub matrx-orm registration; return the list of captured kwargs."""
    captured: list[dict[str, Any]] = []

    def fake_register_from_env(**kwargs: Any) -> bool:
        captured.append(kwargs)
        return ok

    monkeypatch.setattr("matrx_orm.is_database_registered", lambda name: False)
    monkeypatch.setattr("matrx_orm.register_database_from_env", fake_register_from_env)
    monkeypatch.setattr(
        "matrx_orm.register_database",
        lambda config: pytest.fail(
            "matrx-scraper must never register a pool from a raw connection URL — "
            "`scraper.*` binds to the ONE database via SUPABASE_MATRIX_*"
        ),
    )
    monkeypatch.setattr(scraper_db, "_register_models", lambda: None)
    return captured


def test_bootstrap_binds_scraper_schema_to_the_one_platform_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`scraper.*` resolves from SUPABASE_MATRIX_* — the same ONE database as `web.*`."""
    captured = _capture_register_from_env(monkeypatch)

    assert scraper_db.bootstrap_db() == scraper_db.PACKAGE_DB_NAME

    assert len(captured) == 1
    kwargs = captured[0]
    assert kwargs["name"] == scraper_db.PACKAGE_DB_NAME
    assert kwargs["env_prefix"] == "SUPABASE_MATRIX"
    assert kwargs["env_var_overrides"] == {"NAME": "SUPABASE_MATRIX_DATABASE_NAME"}
    assert kwargs["additional_schemas"] == ["scraper"]
    # ssl is left to the deployment (SUPABASE_MATRIX_SSL) so a local or
    # client-owned Postgres is reachable — never hardcoded here.
    assert kwargs["ssl"] is None


def test_bootstrap_ignores_every_retired_second_database_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A service-local Postgres URL must NOT be able to re-fork `scraper.*`."""
    monkeypatch.setenv(
        "SCRAPER_DATABASE_URL", "postgresql://a:b@scraper-postgres.internal:5434/scraper_db"
    )
    monkeypatch.setenv("DATABASE_URL", "postgresql://a:b@scraper-postgres.internal:5434/scraper_db")
    monkeypatch.setenv("MATRX_SCRAPER_POSTGRES_HOST", "scraper-postgres.internal")
    monkeypatch.setenv("MATRX_SCRAPER_POSTGRES_USER", "postgres")
    monkeypatch.setenv("MATRX_SCRAPER_POSTGRES_PASSWORD", "secret")
    captured = _capture_register_from_env(monkeypatch)

    scraper_db.bootstrap_db()

    # register_database (the URL path) is a hard fail in the stub above; the only
    # accepted resolution is the platform env prefix.
    assert [k["env_prefix"] for k in captured] == ["SUPABASE_MATRIX"]

    # connection_url() likewise refuses to fall back to the service-local URL.
    for var in ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_USER", "SUPABASE_MATRIX_PASSWORD"):
        monkeypatch.delenv(var, raising=False)
    with pytest.raises(RuntimeError, match="SUPABASE_MATRIX"):
        scraper_db.connection_url()


def test_scraper_and_web_share_one_resolver_so_they_cannot_diverge(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured = _capture_register_from_env(monkeypatch)
    monkeypatch.setattr(web_db, "_register_models", lambda: None)

    scraper_db.bootstrap_db()
    web_db.bootstrap_web_db()

    assert [k["name"] for k in captured] == [scraper_db.PACKAGE_DB_NAME, web_db.WEB_DB_NAME]
    assert [k["additional_schemas"] for k in captured] == [["scraper"], ["web"]]
    # Same prefix, same overrides, same TLS posture → same physical database.
    assert len({k["env_prefix"] for k in captured}) == 1
    assert len({tuple(sorted(k["env_var_overrides"].items())) for k in captured}) == 1
    assert len({k["ssl"] for k in captured}) == 1  # same TLS posture


@pytest.mark.parametrize("bootstrap", ["scraper", "web"])
def test_bootstrap_raises_when_the_one_database_cannot_be_resolved(
    monkeypatch: pytest.MonkeyPatch, bootstrap: str
) -> None:
    """No fallback, no 'optional' — an unresolvable platform DB is fatal."""
    _capture_register_from_env(monkeypatch, ok=False)
    monkeypatch.setattr(web_db, "_register_models", lambda: None)

    fn = scraper_db.bootstrap_db if bootstrap == "scraper" else web_db.bootstrap_web_db
    with pytest.raises(RuntimeError, match="SUPABASE_MATRIX"):
        fn()


def test_server_image_contains_every_readiness_probe_dependency() -> None:
    import tomllib
    from pathlib import Path

    package_root = Path(__file__).parents[1]
    dockerfile = (package_root / "Dockerfile").read_text()
    project = tomllib.loads((package_root / "pyproject.toml").read_text())
    server_dependencies = project["project"]["optional-dependencies"]["server"]

    assert "curl" in dockerfile
    assert "wget" in dockerfile
    assert any(dependency.startswith("cachetools") for dependency in server_dependencies)


@pytest.mark.parametrize(
    ("missing", "expected_status"),
    [
        (set(), 200),
        ({"filesystem"}, 503),
        ({"web_database"}, 503),
        ({"files_database"}, 503),
        ({"file_access_checker"}, 503),
        ({"file_manager"}, 503),
        ({"canonical_file_pipeline"}, 503),
        ({"s3"}, 503),
        # Both were toggle-gated until 2026-08-09 and could report READY while
        # dark. They are unconditional capabilities, so they fail closed.
        ({"domain_config"}, 503),
        ({"browser_pool"}, 503),
    ],
)
def test_readiness_fails_closed_for_required_components(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    missing: set[str],
    expected_status: int,
    set_matrx_base_dir,
) -> None:
    set_matrx_base_dir(tmp_path / "missing" if "filesystem" in missing else tmp_path)
    fake_file_manager = SimpleNamespace(
        cloud=SimpleNamespace(is_configured=lambda scheme: "s3" not in missing),
        sync_engine=SimpleNamespace(
            _config=SimpleNamespace(
                storage_backend="s3",
                resolve_s3_bucket=lambda: "bucket" if "s3" not in missing else "",
            )
        ),
    )
    ext_values = {
        "db_pool": "database" not in missing,
        "cache": "cache" not in missing,
        "domain_config": "domain_config" not in missing,
        "browser_pool": "browser_pool" not in missing,
        "file_manager": "file_manager" not in missing,
        "canonical_file_pipeline_ready": "canonical_file_pipeline" not in missing,
    }
    monkeypatch.setattr(server_app, "has_ext", lambda name: ext_values.get(name, False))
    monkeypatch.setattr(
        server_app,
        "get_ext",
        lambda name: fake_file_manager
        if name == "file_manager"
        else SimpleNamespace(healthy=ext_values["domain_config"])
        if name == "domain_config"
        else ext_values.get(name, False),
    )
    # This image CAN render, so a missing pool is a readiness failure.
    monkeypatch.setattr(server_app, "PLAYWRIGHT_AVAILABLE", True)
    monkeypatch.setattr(
        "matrx_orm.is_database_registered",
        lambda name: (
            "orm" not in missing
            if name == server_app.PACKAGE_DB_NAME
            else "web_database" not in missing
            if name == server_app.WEB_DB_NAME
            else "files_database" not in missing
        ),
    )
    monkeypatch.setattr(
        "matrx_files.cloud_sync.permissions.get_access_checker",
        lambda: None if "file_access_checker" in missing else object(),
    )

    payload, status = server_app._readiness_snapshot()

    assert status == expected_status
    assert payload["status"] == ("ok" if expected_status == 200 else "not_ready")
    assert payload["failed_components"] == sorted(missing)


def test_optional_legacy_components_do_not_block_canonical_readiness(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    set_matrx_base_dir,
) -> None:
    set_matrx_base_dir(tmp_path)
    fake_file_manager = SimpleNamespace(
        cloud=SimpleNamespace(is_configured=lambda scheme: True),
        sync_engine=SimpleNamespace(
            _config=SimpleNamespace(
                storage_backend="s3",
                resolve_s3_bucket=lambda: "bucket",
            )
        ),
    )
    monkeypatch.setattr(
        server_app,
        "has_ext",
        lambda name: name
        in {"file_manager", "canonical_file_pipeline_ready", "domain_config", "cache"},
    )
    monkeypatch.setattr(
        server_app,
        "get_ext",
        lambda name: fake_file_manager
        if name == "file_manager"
        else SimpleNamespace(healthy=True)
        if name == "domain_config"
        else True,
    )
    monkeypatch.setattr(server_app, "PLAYWRIGHT_AVAILABLE", False)
    monkeypatch.setattr(
        "matrx_orm.is_database_registered",
        lambda name: name != server_app.PACKAGE_DB_NAME,
    )
    monkeypatch.setattr(
        "matrx_files.cloud_sync.permissions.get_access_checker",
        lambda: object(),
    )

    payload, status = server_app._readiness_snapshot()

    assert status == 200
    assert payload["database"] is False
    assert payload["orm"] is False
    assert payload["domain_config"] is True
    assert payload["failed_components"] == []


def test_absent_playwright_does_not_block_readiness(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    set_matrx_base_dir,
) -> None:
    set_matrx_base_dir(tmp_path)
    fake_file_manager = SimpleNamespace(
        cloud=SimpleNamespace(is_configured=lambda scheme: True),
        sync_engine=SimpleNamespace(
            _config=SimpleNamespace(
                storage_backend="s3",
                resolve_s3_bucket=lambda: "bucket",
            )
        ),
    )
    monkeypatch.setattr(
        server_app,
        "has_ext",
        lambda name: name
        in {"db_pool", "file_manager", "canonical_file_pipeline_ready", "domain_config", "cache"},
    )
    monkeypatch.setattr(
        server_app,
        "get_ext",
        lambda name: fake_file_manager
        if name == "file_manager"
        else SimpleNamespace(healthy=True)
        if name == "domain_config"
        else True,
    )
    # An image with no Playwright genuinely cannot render; that is not a
    # readiness failure, and it is decided by the import probe, not a toggle.
    monkeypatch.setattr(server_app, "PLAYWRIGHT_AVAILABLE", False)
    monkeypatch.setattr("matrx_orm.is_database_registered", lambda name: True)
    monkeypatch.setattr(
        "matrx_files.cloud_sync.permissions.get_access_checker",
        lambda: object(),
    )

    payload, status = server_app._readiness_snapshot()

    assert payload["failed_components"] == [], payload
    assert status == 200
    assert payload["browser_pool"] is False
    assert payload["failed_components"] == []
    # The cache is NOT in this exemption. It is required (and its init is fatal)
    # as of 2026-08-09 — a cache-less server re-fetches every page at full cost
    # forever, which readiness must never call healthy. See
    # test_startup_capability_gates.py.


LEGACY_CRAWL_MODELS = (
    "CrawlRuns",
    "CrawlPages",
    "CrawlLinks",
    "CrawlIssues",
    "CrawlQueue",
    "CrawlScreenshots",
    "CrawlProgressSnapshots",
    "CrawlPresets",
    "CrawlExtractors",
    "CrawlRecipes",
    "CrawlSchedules",
    "Sites",
    "SitePages",
    "SiteRunDiffs",
    "PsiMetrics",
    "GscMetrics",
    "Integrations",
)


def test_no_legacy_crawl_models_remain() -> None:
    """The retired `scraper.crawl_*` model set must never come back.

    These 17 tables were the SECOND crawl store — a full parallel copy of the
    canonical `web.*` schema (two site tables, two run tables, two page stores,
    two link tables, two queues, two schedule tables). They were graveyarded on
    2026-08-09 after the canonical crawler reached parity.

    `db/generate.py` writes `models_scraper.py` from the live database, so this
    test fails the moment someone re-creates one of those tables in the
    `scraper` schema and regenerates. The engine tables (`scrape_*`, no `d`) are
    LIVE and deliberately excluded — the naming similarity is the whole hazard.
    """
    from matrx_scraper.db import models_scraper

    resurrected = [name for name in LEGACY_CRAWL_MODELS if hasattr(models_scraper, name)]

    assert not resurrected, (
        f"retired legacy crawl models are back in models_scraper: {resurrected}. "
        "The canonical crawler owns web.*; scraper.* keeps only the engine "
        "tables (scrape_domain, scrape_parsed_page, scrape_retry_queue, ...)."
    )


def test_the_live_engine_tables_are_still_there() -> None:
    """The other half of the guard above — do not over-delete.

    A grep-and-delete sweep over `scraper.*` takes the live engine down with the
    retired crawler. These seven back domain policy, the L2 page cache, and the
    retry/failure lanes, and they are written in production today.
    """
    from matrx_scraper.db import models_scraper

    for name in (
        "ScrapeDomain",
        "ScrapeDomainSettings",
        "ScrapePathPattern",
        "ScrapePathOverride",
        "ScrapeParsedPage",
        "ScrapeRetryQueue",
        "ScrapeFailureLog",
    ):
        assert hasattr(models_scraper, name), f"live engine model {name} was deleted"


def test_no_legacy_crawl_tools_remain() -> None:
    """SECOND independent layer under `test_no_legacy_crawl_models_remain`.

    Deleting the legacy models is not enough on its own: the AI-tool descriptor
    list is a separate surface, and it outlived them. `crawl_start` /
    `crawl_status` / `crawl_pages` / `crawl_cancel` sat in `ALL_TOOLS` — and
    therefore in the MCP server's advertised tool list — for a full day after
    the `scraper.crawl_*` world was graveyarded, addressing a `run_id` that was
    a `scraper.crawl_runs.id`, resolving host `_ext` handlers no host had wired
    since `aidream/services/scraper/` was deleted. Every call raised, and the
    descriptors made a retired schema look live to the next agent and to any
    model reading the tool list (growth-loop gap G-CRAWL-DUAL).

    Site crawling is the canonical `web.*` crawler, reached over HTTP through
    `matrx_scraper/api/crawl_router.py`. If an agent-facing crawl tool is ever
    wanted, it is a NEW descriptor over `web.crawl_session` — this assertion
    should then name it explicitly rather than be deleted wholesale.
    """
    import matrx_scraper
    from matrx_scraper import ai_tools

    assert not hasattr(ai_tools, "CRAWL_TOOLS"), (
        "CRAWL_TOOLS is back in matrx_scraper.ai_tools — the legacy crawl world "
        "returned through the tool surface."
    )
    assert "CRAWL_TOOLS" not in getattr(matrx_scraper, "__all__", ()), (
        "CRAWL_TOOLS is re-exported from matrx_scraper"
    )

    revived = [
        spec.name
        for spec in ai_tools.ALL_TOOLS
        if spec.name in {"crawl_start", "crawl_status", "crawl_pages", "crawl_cancel"}
        or getattr(spec, "group", None) == "crawl"
    ]
    assert not revived, (
        f"legacy crawl tool descriptors are back in ALL_TOOLS: {revived}. They "
        "address the graveyarded scraper.crawl_runs world and have no executor. "
        "A real crawl tool must target web.crawl_session."
    )
