"""
The kernel's DuckDB, for ``sqlutils``: the project's data catalogs attached to it, and one DuckDB cell.

:func:`attach_catalogs` attaches what the project lists (what and how:
:mod:`sagemaker_studio.sql_engine.duckdb_engine.catalogs`), afresh on every call, under the engine's
lock (``duckdb_engine._lock``) like every statement the SDK runs.

A cell with no connection (:func:`_duckdb_cell`; a cell with a connection runs on the connection's
own engine) takes the engine once and runs every statement on it. It may name the attached catalog
and schema to run in (``catalog_name`` / ``schema_name``): they go first on DuckDB's ``search_path``
for the cell and the previous value is put back afterwards. The push, each statement and the
restore take the lock one at a time, not the cell as a whole (a ``sql_stream`` is consumed at the
caller's pace).
"""

import logging
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, Iterator, List, Optional, Sequence, Tuple

from sagemaker_studio import local_kernel
from sagemaker_studio.connections.providers import ConnectionRecord
from sagemaker_studio.exceptions import CatalogUnavailableError
from sagemaker_studio.sql_engine.duckdb_engine import _one_row as duckdb_one_row
from sagemaker_studio.sql_engine.duckdb_engine import catalogs as duckdb_catalogs
from sagemaker_studio.sql_engine.duckdb_engine import engine as duckdb_engine

logger = logging.getLogger(__name__)


# --- The project's data catalogs on DuckDB ------------------------------------------------------


def attach_catalogs(records: Sequence[ConnectionRecord]) -> List[Dict[str, Any]]:
    """
    Attach the catalogs of ``records`` (the project's connections, as listed now) to the kernel's
    DuckDB, afresh: detach and drop what an earlier round left, re-create the engine's own
    credential-chain secret, then attach the listing (:meth:`.catalogs.LocalCatalogs.attach_all`).
    On a local kernel, what the chain resolves now is also what
    :func:`sagemaker_studio.local_kernel.current_context` reports as ``signed_in``.

    Returns:
        The attached databases, as :func:`list_attached_catalogs` reports them; a connection that
        could not be attached is on its entry, with the reason, never raised.
    """
    kernel = local_kernel.local_kernel()
    if kernel is not None:
        kernel.observe_credentials(*duckdb_catalogs.chain_credentials())
    with duckdb_engine._lock:
        duck = duckdb_engine._ensure_duckdb()
        duckdb_engine._reset_ambient_s3_secret(duck)
        duckdb_catalogs._state.attach_all(duck, records)
    return list_attached_catalogs()


def detach_local_catalogs() -> None:
    """
    Detach every database :func:`attach_catalogs` attached, drop every secret it made and the
    ``iceberg`` extension's vended credentials, and drop the engine's credential-chain secret: the
    frontend's sign-out call, after which DuckDB holds nothing of the previous identity's. A user's
    own databases and secrets stay.
    """
    with duckdb_engine._lock:
        if duckdb_engine._duckdb is None:
            logger.info("No DuckDB engine yet; nothing to detach")
            return
        logger.info("Detaching the project's catalogs from DuckDB")
        duckdb_catalogs._state.reset(duckdb_engine._duckdb)
        duckdb_engine._drop_ambient_s3_secret()


def list_attached_catalogs() -> List[Dict[str, Any]]:
    """
    The databases :func:`attach_catalogs` attached, or tried to, without asking the project: one
    entry per database with ``alias`` (the name to query it by), ``connection_id``,
    ``connection_name``, ``catalog`` (the Glue catalog, or the data catalog an Athena workgroup
    exposes), ``route`` (``glue`` or ``athena``), ``secret``, ``attached`` and ``error``.
    """
    return [catalog.describe() for catalog in duckdb_catalogs._state.attached()]


def _reset_attached_catalogs() -> None:
    """On a kernel reset (tests, embedders), detach the catalogs attached under the previous
    configuration; the engine drops its own credential-chain secret on the same reset."""
    with duckdb_engine._lock:
        if duckdb_engine._duckdb is not None and not duckdb_catalogs._state.empty():
            try:
                duckdb_catalogs._state.reset(duckdb_engine._duckdb)
            except Exception:  # noqa: BLE001 - best effort, like every drop
                logger.warning(
                    "Could not detach the attached catalogs on the kernel reset; what stayed is on "
                    "list_attached_catalogs()",
                    exc_info=True,
                )


local_kernel.add_reset_listener(_reset_attached_catalogs)


# --- DuckDB: one cell in a catalog ------------------------------------------------------------------


def _requested_search_path(kwargs: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """The ``catalog_name`` and ``schema_name`` the caller passed, for a DuckDB cell's ``search_path``."""
    return kwargs.get("catalog_name") or None, kwargs.get("schema_name") or None


@contextmanager
def _duckdb_cell(kwargs: Dict[str, Any]):
    """
    One DuckDB cell: yields the engine (the cell's one ``_ensure_duckdb()``), with ``catalog_name``
    (and ``schema_name``) first on DuckDB's ``search_path`` until the cell is done, when the previous
    value is put back whatever the outcome (a refused restore is logged, never raised).

    Raises:
        CatalogUnavailableError: DuckDB would not put them on its ``search_path``: the catalog is
            not attached, or has no such schema, or (none named) no default schema.
    """
    catalog_name, schema_name = _requested_search_path(kwargs)
    with duckdb_engine._lock:
        duck = duckdb_engine._ensure_duckdb()
        previous = _push_search_path(duck, catalog_name, schema_name) if catalog_name else None
    if previous is None:
        yield duck
        return
    try:
        yield duck
    finally:
        # Best effort: the cell's outcome stands, but a failed restore changes what later
        # unqualified names resolve to, so it is warned.
        try:
            with duckdb_engine._lock:
                _set_search_path(duck, previous)
        except Exception:  # noqa: BLE001
            logger.warning(
                "Could not put DuckDB's search_path back to %r; it stays on %r until set again",
                previous,
                duckdb_catalogs.search_path_entry(catalog_name, schema_name),
                exc_info=True,
            )


def _in_duckdb_cell(kwargs: Dict[str, Any], statements: Callable[[Any], Iterator]) -> Generator:
    """The stream ``statements`` builds for the cell's engine, inside :func:`_duckdb_cell`: entered
    when the first result is asked for, left when the stream is exhausted or closed."""
    with _duckdb_cell(kwargs) as duck:
        yield from statements(duck)


def _run_duckdb_statement(duck, statement: str):
    """Run one statement on ``duck``, the cell's engine (see :func:`_duckdb_cell`)."""
    duckdb_engine._resolve_pending_for_duckdb(duck, statement)
    return duckdb_engine._run_local_duckdb(duck, statement)


def _push_search_path(duck, catalog_name: str, schema_name: Optional[str]) -> str:
    """Put ``catalog_name`` (and ``schema_name``) first on DuckDB's ``search_path``; returns the previous value."""
    row = duckdb_one_row(duck, "SELECT current_setting('search_path')")
    previous = str(row[0]) if row and row[0] is not None else ""
    entry = duckdb_catalogs.search_path_entry(catalog_name, schema_name)
    logger.debug(
        "The cell runs in %r: search_path %r goes first on %r", catalog_name, entry, previous
    )
    try:
        _set_search_path(duck, f"{entry},{previous}" if previous else entry)
    except Exception as e:  # noqa: BLE001 - DuckDB's refusal, typed with what the SDK knows
        raise _catalog_unavailable(catalog_name, schema_name, e) from e
    return previous


def _set_search_path(duck, search_path: str) -> None:
    duck.sql(f"SET search_path = {duckdb_catalogs.sql_literal(search_path)};")


def _catalog_unavailable(catalog_name: str, schema_name: Optional[str], error: Exception):
    """
    The error for a ``search_path`` DuckDB refused: the attach's own failure when the SDK recorded
    one, DuckDB's reason otherwise, and what to do about it.
    """
    records = {c.alias: c for c in duckdb_catalogs._state.attached()}
    record = records.get(catalog_name)
    if record is not None and record.attached:
        # The catalog is there: it is the schema, or the default schema when none was named.
        if schema_name:
            detail = f"the catalog has no schema {schema_name!r}"
            guidance = "Pick one of the catalog's databases as the schema."
        else:
            detail = "the catalog has no default schema"
            guidance = "Pass schema_name=<one of the catalog's databases> as well."
    elif record is not None and record.error:
        detail = f"it is not attached ({record.error})"
        guidance = (
            "Fix the connection and run sqlutils.attach_local_catalogs(), or pick another catalog; "
            "sqlutils.list_attached_catalogs() lists them."
        )
    else:
        detail = f"it is not attached ({error})"
        guidance = "Pick an attached catalog; sqlutils.list_attached_catalogs() lists them."
    return CatalogUnavailableError(catalog_name, schema_name, detail, guidance)
