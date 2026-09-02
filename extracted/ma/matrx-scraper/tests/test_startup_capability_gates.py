"""Startup capabilities fail LOUD, never into a healthy-looking degraded server.

The bug class this pins (2026-08-09): the page cache, the domain-config store,
and the browser pool were each brought up inside a bare
``except Exception: print("WARNING: ...")``. That was defensible while the whole
``scraper.*`` database binding was itself optional. It stopped being defensible
when the binding became fatal (ee01821d6): every one of these inits now runs
against a pool that already bound and probed, so an exception means a missing
table, a bad grant, or schema drift — and nothing retries any of them. The
service would come up, answer ``/health`` with 200, and quietly re-fetch every
page at full cost or ignore every per-host policy rule, forever, with the only
evidence a line on a Coolify container's stderr that nobody reads.

Each test here makes exactly ONE capability's real init throw and asserts the
two independent layers hold:

  1. the boot REFUSES (``ScraperStartupError``), and
  2. it screamed first — a red self-identifying banner naming the capability,
     the underlying exception, what breaks, and how to fix it.

Forcing function: revert any gate to ``print(WARNING)`` and ``_lifespan``
completes normally, so ``pytest.raises`` fails. Keep the raise but drop the
banner and the loudness assertions fail. There is no path to green that leaves
a silent degradation in place.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper import db as scraper_db
from matrx_scraper.server import app as server_app
from matrx_scraper.server.config import ServerConfig


class _FakeQuery:
    """Stands in for a matrx-orm queryset that resolves without a database."""

    def limit(self, value: int) -> _FakeQuery:
        return self

    async def all(self) -> list[object]:
        return []

    async def exists(self) -> bool:
        return False


def _stub_prereqs(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Make every step BEFORE the capability gates succeed.

    Deliberately stubs only the prerequisites (web DB, files/S3, the scraper DB
    binding). The capability inits themselves are left REAL so each test can make
    exactly one of them fail through its own code path.

    Returns the list every ``vcprint`` call is recorded into.
    """
    fake_file_manager = SimpleNamespace(
        cloud=SimpleNamespace(
            is_configured=lambda scheme: scheme == "s3",
            s3=SimpleNamespace(
                assert_bucket_accessible_async=_noop_async,
            ),
        ),
        sync_engine=SimpleNamespace(
            _config=SimpleNamespace(
                storage_backend="s3",
                resolve_s3_bucket=lambda: "canonical-bucket",
            )
        ),
    )

    async def fake_probe(**kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(ready=True, error_type=None)

    monkeypatch.setattr("matrx_scraper.db.web.bootstrap_web_db", lambda: None)
    monkeypatch.setattr("matrx_files.db.bind_to_host", lambda name: None)
    monkeypatch.setattr("matrx_files.configure_access_checker", lambda checker, **kw: None)
    monkeypatch.setattr("matrx_files.FileManager", lambda *a, **kw: fake_file_manager)
    monkeypatch.setattr(
        "matrx_files.cloud_sync.CloudSyncConfig",
        lambda **kw: SimpleNamespace(
            storage_backend="s3", resolve_s3_bucket=lambda: "canonical-bucket"
        ),
    )
    monkeypatch.setattr("matrx_files.db.readiness.probe_database_readiness", fake_probe)
    monkeypatch.setattr("matrx_scraper.db.models_web.Snapshot.filter", lambda **k: _FakeQuery())
    monkeypatch.setattr("matrx_scraper.db.models_web.Screenshot.filter", lambda **k: _FakeQuery())
    monkeypatch.setattr(scraper_db, "bootstrap_db", lambda: scraper_db.PACKAGE_DB_NAME)
    monkeypatch.setattr(server_app, "configure_ext", lambda **kw: None)

    banners: list[dict[str, Any]] = []
    monkeypatch.setattr(
        server_app,
        "vcprint",
        lambda data=None, title="", **kw: banners.append({"data": data, "title": title, **kw}),
    )
    return banners


async def _noop_async(*args: object, **kwargs: object) -> None:
    return None


def _app() -> SimpleNamespace:
    return SimpleNamespace(state=SimpleNamespace(config=ServerConfig()))


def _assert_screamed(banners: list[dict[str, Any]], capability: str, cause: str) -> None:
    """The banner must self-identify AND carry the operator's next action.

    Asserting only "something was printed" would survive a regression to a bare
    one-line warning, which is the exact thing this file exists to prevent.
    """
    matching = [b for b in banners if b["data"].get("capability") == capability]
    assert matching, f"no red banner named the failing capability {capability!r}: {banners}"
    banner = matching[-1]

    assert banner.get("color") == "red", f"the startup gate banner must be red: {banner}"
    assert capability in banner["title"], f"the title must name the capability: {banner['title']}"

    data = banner["data"]
    # The underlying cause, not a generic "init failed" — an operator has to be
    # able to act on this without attaching a debugger to a crash-looping box.
    assert cause in data["exception"], f"the banner must carry the real cause: {data}"
    # Both halves of the contract: consequence and remedy, each substantive.
    assert len(data["what_breaks_if_we_continue"]) > 40, data
    assert len(data["how_to_fix"]) > 40, data


@pytest.mark.asyncio
async def test_cache_init_failure_refuses_to_boot_and_screams(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    banners = _stub_prereqs(monkeypatch)

    def exploding_filter(**kwargs: object) -> _FakeQuery:
        raise RuntimeError('relation "scraper.scrape_parsed_page" does not exist')

    monkeypatch.setattr("matrx_scraper.db.models_scraper.ScrapeParsedPage.filter", exploding_filter)

    with pytest.raises(server_app.ScraperStartupError, match="cache"):
        async with server_app._lifespan(_app()):
            pass

    _assert_screamed(banners, "cache", "scrape_parsed_page")


@pytest.mark.asyncio
async def test_domain_config_start_failure_refuses_to_boot_and_screams(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    banners = _stub_prereqs(monkeypatch)
    monkeypatch.setattr(
        "matrx_scraper.db.models_scraper.ScrapeParsedPage.filter", lambda **k: _FakeQuery()
    )

    class ExplodingStore:
        async def start(self) -> None:
            raise RuntimeError("initial load failed: permission denied for schema scraper")

    monkeypatch.setattr(
        "matrx_scraper.domain_config.PostgresDomainConfigStore", lambda *a, **kw: ExplodingStore()
    )

    with pytest.raises(server_app.ScraperStartupError, match="domain_config"):
        async with server_app._lifespan(_app()):
            pass

    _assert_screamed(banners, "domain_config", "permission denied")


@pytest.mark.asyncio
async def test_browser_pool_start_failure_refuses_to_boot_and_screams(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    banners = _stub_prereqs(monkeypatch)
    monkeypatch.setattr(
        "matrx_scraper.db.models_scraper.ScrapeParsedPage.filter", lambda **k: _FakeQuery()
    )

    class HealthyStore:
        healthy = True

        async def start(self) -> None:
            return None

        async def stop(self) -> None:
            return None

    monkeypatch.setattr(
        "matrx_scraper.domain_config.PostgresDomainConfigStore", lambda *a, **kw: HealthyStore()
    )
    # This gate is reachable only on an image that HAS Playwright — pin that,
    # so the test proves the failure path rather than the missing-extra path.
    monkeypatch.setattr(server_app, "PLAYWRIGHT_AVAILABLE", True)

    class ExplodingPool:
        async def start(self) -> None:
            raise RuntimeError("Chromium failed to launch: no usable sandbox")

    monkeypatch.setattr(
        "matrx_scraper.browser_pool.PlaywrightBrowserPool", lambda *a, **kw: ExplodingPool()
    )

    with pytest.raises(server_app.ScraperStartupError, match="browser_pool"):
        async with server_app._lifespan(_app()):
            pass

    _assert_screamed(banners, "browser_pool", "Chromium failed to launch")


def test_readiness_requires_every_gated_capability() -> None:
    """Layer 2: even if a boot gate were softened back to a warning, a server
    missing one of these must never report itself ready.

    Pinned against the live predicate rather than a copy of the required set, so
    dropping a `required.add(...)` fails here instead of silently widening what
    counts as healthy.
    """
    for capability in ("cache", "domain_config", "browser_pool"):
        payload, status = _readiness_with_missing(capability)
        assert status == 503, f"readiness stayed {status} with {capability} down: {payload}"
        assert capability in payload["failed_components"], payload


def _readiness_with_missing(missing: str) -> tuple[dict[str, Any], int]:
    """Run the REAL readiness snapshot with every capability up except one."""
    import os
    from pathlib import Path
    from unittest.mock import patch

    present = {"cache", "domain_config", "browser_pool", "file_manager"}
    present.discard(missing)

    base_dir = os.getcwd()
    file_manager = SimpleNamespace(
        sync_engine=SimpleNamespace(
            _config=SimpleNamespace(
                storage_backend="s3", resolve_s3_bucket=lambda: "canonical-bucket"
            )
        ),
        cloud=SimpleNamespace(is_configured=lambda backend: backend == "s3"),
    )

    def fake_get_ext(name: str) -> object:
        if name == "domain_config":
            return SimpleNamespace(healthy="domain_config" in present)
        if name == "file_manager":
            return file_manager
        if name == "canonical_file_pipeline_ready":
            return True
        return object()

    with (
        patch.object(
            server_app,
            "has_ext",
            lambda name: name in present or name == "canonical_file_pipeline_ready",
        ),
        patch.object(server_app, "get_ext", fake_get_ext),
        patch.object(server_app, "PLAYWRIGHT_AVAILABLE", True),
        patch("matrx_orm.is_database_registered", lambda name: True),
        patch("matrx_files.cloud_sync.permissions.get_access_checker", lambda: object()),
        patch("matrx_utils.conf.settings", SimpleNamespace(BASE_DIR=Path(base_dir))),
    ):
        return server_app._readiness_snapshot()
