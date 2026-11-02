"""Database binding for matrx-files — the package OWNS the ``files`` schema.

**ONE connection, REQUIRED — never a chain of candidates.** matrx-files owns the
`files.*` schema and MUST be able to create and run it on a Postgres of its own,
installed alone. **Today it cannot, and that is a tracked defect, not a design
choice:** the shipped migrations in ``cloud_sync/sql/`` create unqualified
``files.*`` tables (i.e. ``files.files``) while the models bind
``_db_schema="files"``, and the package also reads ``iam.permissions`` /
``iam.has_access()`` / ``platform.share_links`` / ``auth.users`` without shipping
DDL for any of them. Do not read the rule below as a description of what already
works. See FOUND_DEFECTS.md; the reference implementation to copy is
``matrx_runtime.db.bootstrap`` (portable identity shim + its own ``iam.has_access``,
applied by ``apply_schema()``).

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

matrx-files ships ONE canonical copy of its model classes
(``matrx_files.db.models_files`` — the ``files.*`` schema: files, folders,
file_versions, uploads_inflight, idempotency, user_account,
account_tiers, user_storage_usage, file_rag_jobs, webhooks, analysis, pages,
…), generated from the live database by the host's ``db/generate.py`` run.
Every model bakes ``_database = "matrx_files"`` (:data:`PACKAGE_DB_NAME`).
What that name points at is decided exactly once, by whichever of these runs:

* **Hosted** — the host registered its own pool and calls
  :func:`bind_to_host`: a matrx-orm *name alias* maps ``"matrx_files"`` onto
  the host's config. One registration, one physical pool — the package NEVER
  opens a second connection.
* **Standalone** — the package is the whole app: :func:`bootstrap_db`
  registers a pool against the ONE database from the ``SUPABASE_MATRIX_*`` env
  vars and registers the model set. Only the CREDENTIALS differ per deployment.
  Resolution failure RAISES — there is no fallback and no "optional" mode.
  Migrations live in ``matrx_files/cloud_sync/sql/``.

There is deliberately NO ``SET search_path``: Supavisor's transaction pooler
resets backend state between transactions, so every query fully-qualifies its
table names (``files.files``, ``iam.permissions``, ``auth.users``).

INDEPENDENCE.md note: matrx-orm is a declared dependency of this package —
per the platform law, any matrx package that touches a database depends on
the ORM. There is no raw-SQL or PostgREST fallback path.
"""

from __future__ import annotations

from typing import Any

from matrx_orm import PLATFORM_DB_ENV_PREFIX, platform_connection_url, register_platform_db

# The config name every matrx-files model class is bound to. Hosts alias it to
# their registered pool (bind_to_host); standalone registers a real config
# (bootstrap_db).
PACKAGE_DB_NAME = "matrx_files"

# The ONE database's env prefix, owned by matrx_orm.platform_db and re-exported
# here for readability. Never introduce a files-specific alternative — a
# package-specific-URL / generic-URL / package-POSTGRES ladder is
# exactly how `scraper.*` was forked onto a second Postgres.
DB_ENV_PREFIX = PLATFORM_DB_ENV_PREFIX

_models_registered = False


class FilesDBNotConfiguredError(RuntimeError):
    """matrx-files DB access attempted before bind_to_host()/bootstrap_db().

    This is a WIRING bug at the call site (host startup or standalone boot) —
    never work around it inside the package.
    """


def connection_url() -> str:
    """Resolve the ONE database's postgres URL for ad-hoc / migration use."""
    return platform_connection_url(package="matrx-files")


def _register_models() -> None:
    """Import the generated model module so its classes register.

    The module ends with ``model_registry.register_all(..., skip_existing=True)``
    so a host's earlier same-name registration always wins.
    """
    global _models_registered
    if not _models_registered:
        from matrx_files.db import models_files  # noqa: F401  (registers on import)
        from matrx_files.db import models_platform  # noqa: F401  (platform.share_links)

        _models_registered = True


def bind_to_host(db_config_name: str) -> None:
    """Hosted entry — point :data:`PACKAGE_DB_NAME` at the host's pool.

    Registers a matrx-orm name alias (idempotent for the same target) and
    registers the package's files.* model classes.
    """
    from matrx_orm import is_database_registered, register_database_alias

    if not is_database_registered(PACKAGE_DB_NAME):
        register_database_alias(PACKAGE_DB_NAME, db_config_name)
    _register_models()


def bootstrap_db(
    *,
    additional_schemas: tuple[str, ...] = ("files", "iam", "auth", "platform"),
) -> str:
    """Standalone entry — register the package's own pool against the ONE database.

    Same ``SUPABASE_MATRIX_*`` env vars as every other Matrx service, through
    the ONE platform resolver (``matrx_orm.register_platform_db``), then
    registers the model set. Raises if those env vars are missing — ``files.*``
    may never resolve to a second Postgres. Idempotent: a host that already
    registered/aliased the name turns this into a no-op model-registration call.
    Returns :data:`PACKAGE_DB_NAME`.
    """
    try:
        register_platform_db(
            PACKAGE_DB_NAME,
            package="matrx-files",
            additional_schemas=list(additional_schemas),
        )
    except RuntimeError as exc:
        # Keep this package's own documented wiring error — the same type
        # ensure_bound() raises — so callers have ONE thing to catch.
        raise FilesDBNotConfiguredError(str(exc)) from exc
    _register_models()
    return PACKAGE_DB_NAME


def ensure_bound() -> str:
    """Resolve the pool name matrx-files models use, screaming if unbound."""
    from matrx_orm import is_database_registered

    if is_database_registered(PACKAGE_DB_NAME):
        _register_models()
        return PACKAGE_DB_NAME
    raise FilesDBNotConfiguredError(
        "matrx-files DB is not bound. Host startup must call "
        "matrx_files.db.bind_to_host(<pool name>) (aidream: package_integration), "
        "or standalone boot must call matrx_files.db.bootstrap_db()."
    )


def get_models() -> dict[str, Any]:
    """Return name → Model class for everything the package ships."""
    _register_models()
    from matrx_files.db import models_files

    return {
        attr.__name__: attr
        for attr in vars(models_files).values()
        if isinstance(attr, type) and getattr(attr, "_table_name", None)
    }
