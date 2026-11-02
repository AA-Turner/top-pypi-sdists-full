"""Database access + binding for the RAG pipeline.

**ONE connection, REQUIRED — never a chain of candidates.** matrx-rag owns the
`rag.*` schema and MUST be able to create and run it on a Postgres of its own,
installed alone. **It is not fully there yet** — migrations 0002/0004 ALTER host
``public.cld_*`` tables the package does not create — so treat the rule below as
the requirement, not as a description of current behavior (tracked in
FOUND_DEFECTS.md). The reference implementation is ``matrx_runtime.db.bootstrap``.

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

matrx-rag ships ONE canonical copy of its model classes (``matrx_rag.db.models_docproc``
for the docproc.* tables it reads — processed_documents + processed_document_pages,
``matrx_rag.db.models_rag`` for the rag.* schema) — generated from the live database
by the host's ``db/generate.py``
run. Every model bakes ``_database = "matrx_rag"`` (:data:`PACKAGE_DB_NAME`) — a
matrx-orm *config name*, NOT a database. What that name points at is decided
exactly once, by whichever of these runs:

* **Hosted** — the host registered its own pool and calls
  ``matrx_rag.configure(db_config_name=...)``, which calls
  :func:`bind_to_host`: a matrx-orm *name alias* maps ``"matrx_rag"`` onto the
  host's config. One registration, one physical pool — the package NEVER opens
  a second connection. Only the rag.* models register here; docproc.* names
  (ProcessedDocuments, ProcessedDocumentPages) resolve to the HOST's classes
  through ``matrx_orm.model_registry`` so there is exactly one definition per
  table at runtime.
* **Standalone** — the package is the whole app: :func:`bootstrap_db` registers
  a pool from the ``SUPABASE_MATRIX_*`` env vars through
  :func:`register_platform_db` and registers BOTH model files. Resolution
  failure RAISES — there is no fallback and no "optional" mode. Only the
  CREDENTIALS differ per deployment. Migrations: ``matrx_rag/migrations/``.

There is deliberately NO ``SET search_path``: Supavisor's transaction pooler
resets backend state between transactions, so every query fully-qualifies its
table names (``rag.kg_chunks``, ``files.files``, ``auth.users``).
pgvector + UUID codecs are registered by matrx-orm's pool-init callback.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from matrx_orm import PLATFORM_DB_ENV_PREFIX, platform_connection_url, register_platform_db

# The config name every matrx-rag model class is bound to. Hosts alias it to
# their registered pool (bind_to_host); standalone registers it as a real
# config (bootstrap_db).
PACKAGE_DB_NAME = "matrx_rag"

# The ONE database's env prefix, owned by matrx_orm.platform_db and re-exported
# here for readability. Never introduce a RAG-specific alternative: a
# package-specific-URL / generic-URL / package-POSTGRES ladder is exactly
# how the sibling scraper package forked `scraper.*` onto a second Postgres.
DB_ENV_PREFIX = PLATFORM_DB_ENV_PREFIX

_models_registered: set[str] = set()


def connection_url() -> str:
    """Resolve the ONE database's postgres URL for ad-hoc / migration use."""
    return platform_connection_url(package="matrx-rag")


def _register_models(*, include_docproc: bool) -> None:
    """Import the generated model modules so their classes register.

    Both files end with ``model_registry.register_all(..., skip_existing=True)``
    so a host's earlier same-name registration always wins. rag.* models are
    canonical here; docproc.* models (processed_documents +
    processed_document_pages — the borrowed document-processing tables) are only
    meant to win when standalone.
    """
    if include_docproc and "docproc" not in _models_registered:
        from matrx_rag.db import models_docproc  # noqa: F401  (registers on import)

        _models_registered.add("docproc")
    if "rag" not in _models_registered:
        from matrx_rag.db import models_rag  # noqa: F401  (registers on import)

        _models_registered.add("rag")


def bind_to_host(db_config_name: str) -> None:
    """Hosted entry — point :data:`PACKAGE_DB_NAME` at the host's pool.

    Registers a matrx-orm name alias (idempotent for the same target) and
    registers the package's rag.* model classes. docproc.* classes
    (processed_documents + processed_document_pages) are NOT registered here:
    the host owns those tables' canonical definitions and matrx-rag resolves
    them from ``matrx_orm.model_registry`` at access time.
    Called automatically by ``matrx_rag.configure(db_config_name=...)``.
    """
    from matrx_orm import is_database_registered, register_database_alias

    if not is_database_registered(PACKAGE_DB_NAME):
        register_database_alias(PACKAGE_DB_NAME, db_config_name)
    _register_models(include_docproc=False)


def bootstrap_db(
    *,
    additional_schemas: tuple[str, ...] = ("rag", "docproc", "auth"),
) -> str:
    """Standalone entry — register the package's own pool against the ONE database.

    Same ``SUPABASE_MATRIX_*`` env vars as every other Matrx service, through
    the ONE platform resolver (``matrx_orm.register_platform_db``), then
    registers the package's full model set (rag.* AND the docproc.* tables
    matrx-rag reads). Raises if those env vars are missing — ``rag.*`` may never
    resolve to a second Postgres. Idempotent: a host that already
    registered/aliased the name turns this into a no-op model-registration call.

    Returns :data:`PACKAGE_DB_NAME`.
    """
    register_platform_db(
        PACKAGE_DB_NAME,
        package="matrx-rag",
        additional_schemas=list(additional_schemas),
    )
    _register_models(include_docproc=True)
    return PACKAGE_DB_NAME


def get_models() -> dict[str, Any]:
    """Return name → Model class for everything the package ships.

    Lazily imports both generated model files (registering them with
    ``skip_existing=True``). Mostly useful for hosts that want to introspect
    or re-export the package's canonical classes.
    """
    _register_models(include_docproc=True)
    from matrx_rag.db import models_docproc, models_rag

    out: dict[str, Any] = {}
    for module in (models_docproc, models_rag):
        for attr in vars(module).values():
            if isinstance(attr, type) and getattr(attr, "_table_name", None):
                out[attr.__name__] = attr
    return out


def _ensure_bound() -> str:
    """Resolve the pool name matrx-rag should use, binding lazily if needed.

    Order: an already-bound :data:`PACKAGE_DB_NAME` (alias or real config) →
    the host-injected ``db_config_name`` / ``MATRX_DB_CONFIG_NAME`` env var
    (bound on first use) → ``RagNotConfiguredError``.
    """
    from matrx_orm import is_database_registered

    if is_database_registered(PACKAGE_DB_NAME):
        _register_models(include_docproc=False)
        return PACKAGE_DB_NAME

    from matrx_rag._ext import get_db_config_name

    # Raises RagNotConfiguredError (now also pointing at bootstrap_db) when
    # neither the injected name nor MATRX_DB_CONFIG_NAME is set.
    name = get_db_config_name()
    if is_database_registered(name):
        bind_to_host(name)
        return PACKAGE_DB_NAME
    # Unregistered name: hand it to matrx-orm unchanged so its own
    # "Configuration not found" error surfaces (historical behavior).
    return name


async def close_pool() -> None:
    """Tests + clean shutdown — close every matrx-orm pool, not just the RAG view."""
    from matrx_orm.core.async_db_manager import AsyncDatabaseManager

    await AsyncDatabaseManager.cleanup()


async def apply_migration_file(path: str | Path) -> None:
    """Execute a SQL migration file as a single batch.

    The migrations in ``matrx_rag/migrations/`` are written to be idempotent
    (every CREATE has IF NOT EXISTS, every policy DROPs first). Re-running
    is a no-op.
    """
    from matrx_orm.operations.dynamic_admin import execute_migration_file

    await execute_migration_file(path, config_name=_ensure_bound())
