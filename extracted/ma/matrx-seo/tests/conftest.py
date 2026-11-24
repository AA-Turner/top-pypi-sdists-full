from __future__ import annotations

import os
from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from matrx_orm.core.config import DatabaseProjectConfig

_DATABASE_ENV_KEYS = frozenset(
    {
        "CREDENTIALS_ENCRYPTION_KEY",
        "MATRX_DB_CONFIG_NAME",
        "MATRX_STAGE",
        "MATRX_SESSION_AUTHORITY_URL",
        "SUPABASE_JWT_SECRET",
        "SUPABASE_URL",
    }
)


def _database_env_snapshot() -> dict[str, str]:
    return {
        key: value
        for key, value in os.environ.items()
        if key in _DATABASE_ENV_KEYS or key.startswith("SUPABASE_MATRIX_")
    }


def _restore_database_env(snapshot: dict[str, str]) -> None:
    current_keys = {
        key for key in os.environ if key in _DATABASE_ENV_KEYS or key.startswith("SUPABASE_MATRIX_")
    }
    for key in current_keys - snapshot.keys():
        os.environ.pop(key, None)
    for key, value in snapshot.items():
        os.environ[key] = value


def _database_registry_snapshot() -> tuple[
    dict[str, DatabaseProjectConfig], dict[str, str], list[str]
]:
    from matrx_orm.core.config import registry

    return (
        dict(registry._configs),
        dict(registry._name_aliases),
        list(registry._used_aliases),
    )


def _restore_database_registry(
    snapshot: tuple[dict[str, DatabaseProjectConfig], dict[str, str], list[str]],
) -> None:
    from matrx_orm.core.config import registry

    configs, aliases, used_aliases = snapshot
    registry._configs.clear()
    registry._configs.update(configs)
    registry._name_aliases.clear()
    registry._name_aliases.update(aliases)
    registry._used_aliases[:] = used_aliases


#: The ``platform.feature_knob`` rows for feature ``"seo"``, as registered in the
#: live database (read 2026-08-23). Every ceiling and default this package uses is
#: a knob row, never a constant — ``common-docs/policies/limits-are-knobs-agents-set-them.md``
#: — and ``matrx_seo.knobs`` has NO fallback: a missing row raises, and an
#: unregistered database raises a `CacheError` from the pool layer.
#:
#: That is correct in production and fatal in an offline test. Every test that
#: calls ``SeoCollectionService.collect()`` goes through ``enforce_collection_budget``
#: (six usd knobs) and ``inline_payload_max_bytes`` (one int knob), so before this
#: fixture existed those tests died with
#: ``Configuration 'matrx_seo' not found in registered databases`` — 19 failures
#: plus one HANG (a test that awaits an event the provider sets, when the provider
#: is never reached because the budget gate raised first).
#:
#: Values are the REGISTERED ones and are stored in their raw JSONB shape, so the
#: tests exercise the same ``Decimal(str(...))`` / ``int(...)`` conversion
#: production does. If a knob is retuned in the admin UI, this table goes stale in
#: the safe direction: the tests keep asserting against the value they were
#: written for. Adding a NEW knob read without adding it here fails loudly with
#: ``KnobNotRegisteredError`` naming the key — never a silent default.
from matrx_seo.testing_knobs import SEO_KNOB_VALUES  # noqa: E402


@pytest.fixture(autouse=True)
def _offline_feature_knobs(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Serve knob rows from :data:`SEO_KNOB_VALUES` when there is no database.

    Patches ``matrx_seo.knobs._feature_values`` — the ONE function that touches
    Postgres. The public readers (``usd_knob`` / ``int_knob`` / ``str_knob``) are
    imported BY NAME into ``matrx_seo.budget`` and ``matrx_seo.service``, so
    patching them on the ``knobs`` module would not reach those bound names;
    ``_feature_values`` is the choke point every path funnels through.

    **The guard matters.** The stub defers to the real reader whenever the
    ``matrx_seo`` config IS registered, so a live test that configured the host
    database still resolves real ``platform.feature_knob`` rows instead of
    silently asserting against this table. The check is inside the stub, not at
    fixture setup, because the host's ``isolated_host_database``
    (``tests/package_host_contracts/matrx_seo``, which runs on this conftest) registers
    the database during test setup — after this fixture has already run.
    """
    from matrx_orm import is_database_registered

    from matrx_seo import knobs

    real_feature_values = knobs._feature_values

    async def _feature_values(feature: str) -> dict[str, object]:
        if is_database_registered("matrx_seo"):
            return await real_feature_values(feature)
        return dict(SEO_KNOB_VALUES.get(feature, {}))

    monkeypatch.setattr(knobs, "_feature_values", _feature_values)
    # The knob cache is a module global keyed by feature only. Clear it on both
    # sides so a stubbed value can never be served to a live test, or vice versa.
    knobs.clear_knob_cache()
    yield
    knobs.clear_knob_cache()


@pytest.fixture(autouse=True)
def _database_state_leak_guard() -> Iterator[None]:
    """Restore process-global DB state and fail the test that changed it."""
    env_before = _database_env_snapshot()
    registry_before = _database_registry_snapshot()

    yield

    env_after = _database_env_snapshot()
    registry_after = _database_registry_snapshot()
    _restore_database_registry(registry_before)
    _restore_database_env(env_before)

    leaked: list[str] = []
    if env_after != env_before:
        leaked.append("database environment")
    if registry_after[0] != registry_before[0]:
        leaked.append("matrx-orm database configs")
    if registry_after[1] != registry_before[1]:
        leaked.append("matrx-orm database aliases")
    if registry_after[2] != registry_before[2]:
        leaked.append("matrx-orm config aliases")
    assert not leaked, f"test leaked process-global state: {', '.join(leaked)}"


class _AddOnce:
    """Adds each option once: a host test directory run in the same session may have added it."""

    def __init__(self, target) -> None:
        self._target = target

    def addoption(self, *args, **kwargs) -> None:
        try:
            self._target.addoption(*args, **kwargs)
        except ValueError as exc:
            if "already added" not in str(exc):
                raise

    def getgroup(self, *args, **kwargs) -> _AddOnce:
        return _AddOnce(self._target.getgroup(*args, **kwargs))


def pytest_addoption(parser) -> None:
    parser = _AddOnce(parser)
    parser.addoption(
        "--run-seo-database-tests",
        action="store_true",
        default=False,
        help="explicitly authorize the selected SEO database tests (not provider spend)",
    )
    group = parser.getgroup("paid-provider-tests")
    group.addoption(
        "--run-paid-serpapi",
        action="store_true",
        default=False,
        help="run the one-credit SerpAPI live acceptance test",
    )
    group.addoption(
        "--serpapi-credit-cap",
        action="store",
        type=int,
        default=0,
        help="maximum SerpAPI credits authorized for this test run",
    )
    group.addoption(
        "--run-paid-brave",
        action="store_true",
        default=False,
        help="run the one-request Brave live acceptance test",
    )
    group.addoption(
        "--brave-request-cap",
        action="store",
        type=int,
        default=0,
        help="maximum Brave requests authorized for this test run",
    )
    group.addoption(
        "--run-paid-dataforseo",
        action="store_true",
        default=False,
        help="run the one-task DataForSEO live acceptance test",
    )
    group.addoption(
        "--dataforseo-budget-usd",
        action="store",
        type=float,
        default=0,
        help="maximum DataForSEO USD authorized for this test run",
    )
    group.addoption(
        "--run-live-gsc",
        action="store_true",
        default=False,
        help="run one GSC query through a real client integration connection",
    )
    group.addoption(
        "--gsc-request-cap",
        action="store",
        type=int,
        default=0,
        help="maximum GSC Search Analytics requests authorized for this test run",
    )
    group.addoption(
        "--run-live-bing-webmaster",
        action="store_true",
        default=False,
        help="run one Bing Webmaster property-stat request",
    )
    group.addoption(
        "--bing-webmaster-request-cap",
        action="store",
        type=int,
        default=0,
        help="maximum Bing Webmaster requests authorized for this test run",
    )
    for option, description in (
        ("organization-id", "organization UUID for the project and web site"),
        ("user-id", "owner UUID for the client integration"),
        ("site-id", "web.site UUID with a canonical GSC integration binding"),
    ):
        group.addoption(
            f"--gsc-live-{option}",
            action="store",
            default="",
            help=f"{description} for the explicitly approved GSC live test",
        )
    for option, description in (
        ("organization-id", "organization UUID for the project and web site"),
        ("user-id", "owner UUID for the client integration"),
        ("site-id", "web.site UUID with a canonical Bing binding"),
    ):
        group.addoption(
            f"--bing-webmaster-live-{option}",
            action="store",
            default="",
            help=f"{description} for the explicitly approved Bing live test",
        )
    group.addoption(
        "--run-live-pagespeed",
        action="store_true",
        default=False,
        help="run the one-request PageSpeed Insights live acceptance test",
    )
    group.addoption(
        "--pagespeed-request-cap",
        action="store",
        type=int,
        default=0,
        help="maximum PageSpeed requests authorized for this test run",
    )
    group.addoption(
        "--run-live-ga4",
        action="store_true",
        default=False,
        help="run metadata plus one GA4 Data API report through a bound client connection",
    )
    group.addoption(
        "--run-live-serpapi-locations",
        action="store_true",
        default=False,
        help=(
            "run the live SerpAPI location-catalogue test (free endpoint, no API "
            "key and no search credit — it only needs network)"
        ),
    )
    group.addoption(
        "--ga4-request-cap",
        action="store",
        type=int,
        default=0,
        help="maximum GA4 Data API requests authorized for this test run",
    )
    for option, description in (
        ("organization-id", "organization UUID for the project and web site"),
        ("user-id", "owner UUID for the client integration"),
        ("site-id", "web.site UUID with a canonical GA4 integration binding"),
    ):
        group.addoption(
            f"--ga4-live-{option}",
            action="store",
            default="",
            help=f"{description} for the explicitly approved GA4 live test",
        )


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Classify database fixtures before pytest applies the marker expression.

    Generated contracts inherit this classification without editing generated code.
    Mixed modules mark only tests whose fixture closure reaches the database.
    """
    for item in items:
        fixtures = getattr(item, "fixturenames", ())
        module = getattr(item, "module", None)
        contract = "db" in fixtures and callable(getattr(module, "_dsn", None))
        if contract:
            item.add_marker("live")
            item.add_marker("integration")
            item.add_marker("seo_database")


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "seo_database: explicitly authorized SEO database suite")
    config.addinivalue_line("markers", "integration: requires an explicitly selected database")


def pytest_collection_finish(session: pytest.Session) -> None:
    if session.config.option.collectonly or session.config.getoption("run_seo_database_tests"):
        return
    selected = [item for item in session.items if item.get_closest_marker("seo_database")]
    if selected:
        raise pytest.UsageError(
            "SEO database tests selected without --run-seo-database-tests. "
            "Use -m 'not live' for offline checks; synthetic-identity contracts additionally "
            "require MATRX_SEO_CONTRACT_TEST_DSN pointing to an isolated local database."
        )
