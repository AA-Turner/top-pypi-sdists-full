"""Pytest configuration for matrx-scraper tests.

BASE_DIR is config, not an environment variable — ``matrx_utils.conf`` no
longer reads a ``BASE_DIR`` env var at all (repo CLAUDE.md doctrine: "config
is not an env var; almost nothing genuinely differs per environment"). Tests
that need ``matrx_utils.conf.settings.BASE_DIR`` to resolve to an isolated
``tmp_path`` use the ``set_matrx_base_dir`` fixture below instead of the old
``monkeypatch.setenv("BASE_DIR", ...)`` pattern. Tests that exercise a real
``configure_settings(...)`` call site (e.g.
``server/app.py::_configure_standalone_filesystem``) use
``reset_matrx_settings`` to force the process-wide singleton back to its
unconfigured state first — ``configure_settings`` refuses to reconfigure.
"""

from __future__ import annotations

import types
from collections.abc import Callable

import pytest


@pytest.fixture
def set_matrx_base_dir(monkeypatch: pytest.MonkeyPatch) -> Callable[[object], None]:
    """Point ``matrx_utils.conf.settings.BASE_DIR`` at a given path for the
    duration of one test, isolated via ``monkeypatch`` (auto-restored)."""
    from matrx_utils.conf import settings

    def _set(base_dir: object) -> None:
        stub = types.SimpleNamespace(BASE_DIR=str(base_dir), TEMP_DIR=f"{base_dir}/temp")
        monkeypatch.setattr(settings, "_settings_object", stub, raising=False)
        monkeypatch.setattr(settings, "_configured", True, raising=False)

    return _set


@pytest.fixture
def reset_matrx_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force ``matrx_utils.conf.settings`` back to UNCONFIGURED for one test,
    so a real (non-reentrant) ``configure_settings(...)`` call under test
    doesn't hit ``RuntimeError: Settings have already been configured``."""
    from matrx_utils.conf import settings

    monkeypatch.setattr(settings, "_configured", False, raising=False)
    monkeypatch.setattr(settings, "_settings_object", None, raising=False)


@pytest.fixture(autouse=True)
def _reset_shared_host_throttles() -> None:
    """Per-host backoff is PROCESS-WIDE by design (one 429 slows every lane).

    That makes it leak between tests, so every test starts from an unthrottled
    world. Autouse: a test that throttles a host must not silently change the
    baseline another test asserts on.
    """
    from matrx_scraper.rate_limiter import clear_shared_throttles

    clear_shared_throttles()
    yield
    clear_shared_throttles()


@pytest.fixture(autouse=True)
def _fast_pacing_knobs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep the ramp WIRED but instantaneous for tests that aren't about pacing.

    A real crawl now opens at ``PacingKnobs.floor_rps`` (0.5 req/s) and climbs
    (Arman, 2026-08-20 — ``matrx_scraper/FEATURE.md`` § Crawl rate). That is
    correct against a real host and ruinous in a test: a ten-page fixture crawl
    would spend eighteen seconds waiting on a token bucket for a host that does
    not exist.

    Raising the knobs is deliberately preferred over switching pacing OFF. The
    ramp, the limiter wiring, the events and the memory hand-off all still run
    on every crawler test, so a regression in how pacing is WIRED still fails
    the suite here — only the waiting is removed. Tests that assert on pacing
    BEHAVIOUR pass their own ``pacing_knobs=`` and are unaffected by this.
    """
    from matrx_scraper import crawler as crawler_module
    from matrx_scraper.host_pacing import PacingKnobs

    monkeypatch.setattr(
        crawler_module,
        "DEFAULT_KNOBS",
        PacingKnobs(floor_rps=1_000.0, max_rps=1_000.0, min_rps=1_000.0),
    )
