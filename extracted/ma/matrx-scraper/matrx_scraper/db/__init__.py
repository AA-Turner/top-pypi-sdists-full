"""Database binding for matrx-scraper — the package OWNS the `scraper.*` schema.

**ONE connection, REQUIRED — never a chain of candidates.** matrx-scraper owns the
`scraper.* / web.*` schema: it ships its own models and migrations and can create and run
them on a Postgres of its OWN — installed alone, with nothing else, it works.
That independence is a requirement of this package, not an accident.

What it takes is **exactly one** database connection, from ONE set of variables
(``SUPABASE_MATRIX_HOST/_PORT/_DATABASE_NAME/_USER/_PASSWORD``) through ONE
resolver (``matrx_orm.register_platform_db``). **If it is not given a database it
FAILS LOUD** — it raises at boot, never starts degraded, never guesses. Pointing
it at a different Postgres (a customer's, a local one) is a change of VALUES,
never a new variable name.

**In the AI Dream implementation those values are Matrx Main** — one company, one
server, one database, shared by every package we run. That is our deployment
choice, not a limit of this package.

❌ Never add a second candidate — no package-specific connection variable and
no generic database URL. **The defect is the CHAIN, not the destination:** a
chain lets the host decide the connection, and Coolify injects a generic
database URL into every service automatically. That is how the standalone scraper silently bound the LIVE,
shared `scraper.*` tables to a service-local Postgres and wrote 14 rows the
platform never saw — no error, health green (fixed 2026-08-09).

matrx-scraper ships ONE canonical copy of its `scraper.*` model classes
(``matrx_scraper.db.models_scraper``). Every model bakes
``_database = "matrx_scraper"`` (:data:`PACKAGE_DB_NAME`) — a matrx-orm *config
name*, NOT a database. What that name points at is decided exactly once:

* **Hosted** — aidream registered its own pool and calls
  ``matrx_scraper.configure_db(db_config_name=...)`` → :func:`bind_to_host`: a
  matrx-orm *name alias* maps ``"matrx_scraper"`` onto the host's pool. One
  registration, one physical pool — the package NEVER opens a second connection.
* **Standalone** — :func:`bootstrap_db` registers a pool from the
  ``SUPABASE_MATRIX_*`` env vars, exactly like :func:`~matrx_scraper.db.web.bootstrap_web_db`
  (both go through the ONE resolver ``matrx_orm.register_platform_db``, so
  `scraper.*` and `web.*` can never point at different databases). Resolution failure RAISES — there is no
  fallback and no "optional" mode.

There is deliberately NO ``SET search_path``: every model fully-qualifies its
schema (``scraper.scrape_parsed_page``), so a transaction pooler resetting backend state
between transactions is a non-issue.
"""

from __future__ import annotations

from typing import Any

from matrx_orm import PLATFORM_DB_ENV_PREFIX, platform_connection_url, register_platform_db

# The config name every matrx-scraper model class is bound to. Hosts alias it to
# their registered pool (bind_to_host); standalone registers it as a real config
# (bootstrap_db).
PACKAGE_DB_NAME = "matrx_scraper"

# The ONE database's env prefix, owned by matrx_orm.platform_db and re-exported
# here for readability. Never add a scraper-specific alternative: that is how
# `scraper.*` and `web.*` drifted onto two different Postgres instances.
DB_ENV_PREFIX = PLATFORM_DB_ENV_PREFIX

_models_registered = False


def connection_url() -> str:
    """Resolve the ONE database's postgres URL for ad-hoc / migration use."""
    return platform_connection_url(package="matrx-scraper")


def _register_models() -> None:
    """Import the model module so its classes register (idempotent)."""
    global _models_registered
    if _models_registered:
        return
    from matrx_scraper.db import models_scraper  # noqa: F401  (registers on import)

    _models_registered = True


def bind_to_host(db_config_name: str) -> None:
    """Hosted entry — point :data:`PACKAGE_DB_NAME` at the host's pool.

    Registers a matrx-orm name alias (idempotent) and the package's ``scraper.*``
    model classes. Called by ``matrx_scraper.configure_db(db_config_name=...)``.
    """
    from matrx_orm import is_database_registered, register_database_alias

    if not is_database_registered(PACKAGE_DB_NAME):
        register_database_alias(PACKAGE_DB_NAME, db_config_name)
    _register_models()


def bootstrap_db(*, additional_schemas: tuple[str, ...] = ("scraper",)) -> str:
    """Standalone entry — register the package's own pool against the ONE database.

    Same ``SUPABASE_MATRIX_*`` env vars as every other Matrx service, through the
    ONE platform resolver (``matrx_orm.register_platform_db``) — the same call
    :func:`~matrx_scraper.db.web.bootstrap_web_db` makes, so `scraper.*` and
    `web.*` cannot diverge onto different databases. Raises if they are missing.
    Idempotent. Returns :data:`PACKAGE_DB_NAME`.
    """
    register_platform_db(
        PACKAGE_DB_NAME,
        package="matrx-scraper",
        additional_schemas=list(additional_schemas),
    )
    _register_models()
    return PACKAGE_DB_NAME


def ensure_bound() -> str:
    """Resolve the pool name to use, binding lazily if needed.

    Order: an already-registered/aliased :data:`PACKAGE_DB_NAME` → the
    host-injected ``db_config_name`` (bound on first use) → raise.
    """
    from matrx_orm import is_database_registered

    if is_database_registered(PACKAGE_DB_NAME):
        _register_models()
        return PACKAGE_DB_NAME

    from matrx_scraper.db._config import get_db_config_name

    name = get_db_config_name()  # raises if neither injected name nor env is set
    if is_database_registered(name):
        bind_to_host(name)
        return PACKAGE_DB_NAME
    return name


def get_models() -> dict[str, Any]:
    """Return name → Model class for everything the package ships."""
    _register_models()
    from matrx_scraper.db import models_scraper

    out: dict[str, Any] = {}
    for attr in vars(models_scraper).values():
        if isinstance(attr, type) and getattr(attr, "_table_name", None):
            out[attr.__name__] = attr
    return out
