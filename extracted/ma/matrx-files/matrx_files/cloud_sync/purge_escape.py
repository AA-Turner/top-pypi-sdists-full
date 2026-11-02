"""The transaction-local escape that lets a deliberate delete-forever cross the
tombstone retention floor (FS-C6c / D23).

Migration 033 put a ``BEFORE DELETE`` row trigger on ``files.files``
(``files.guard_tombstone_retention``): a row whose ``deleted_at`` is inside the
``files.min_tombstone_retention_days()`` window (90 days, floor) may not be
deleted, so an offline device converges on the tombstone instead of
resurrecting the delete. The trigger is on the ROW, deliberately, because
``files.hard_delete_file`` takes one argument and recurses into its own
children with that same one-argument form — no new function argument could
reach every path.

A user's "delete forever" is the lawful exception, and it announces itself by
setting ``matrx.purge_root_id`` to the ROOT id of the operation, transaction-
locally, in the SAME transaction as the delete. The trigger then walks
``parent_file_id`` upward (bounded at 64 hops) and permits that root and every
descendant of it. The tree scope is load-bearing: ``hard_delete_file``
soft-stamps every row it is about to delete, so a delete-forever of a parent
with never-trashed children stamps ``now()`` on those children — a single-id
escape aborts on the first one.

The ONE place that sets it is :func:`purge_escape`, opened by
``DatabaseClient.hard_delete_file_async`` and
``DatabaseClient.hard_delete_file_fallback_async`` — the two DB-boundary
methods that actually issue the delete, and therefore the only places that can
put the GUC in the same transaction as it. Every delete-forever surface (the
file service, the folders service, the ``.matrx-tmp/`` retention policy, orphan
cleanup) reaches them through ``SyncEngine.hard_delete_and_purge[_async]``, the
package's ordinary sanctioned hard-delete entry point, and so inherits the
escape without naming it. Central lifecycle custody is the deliberate second
contract: ``matrx_files.retention.run_retention_purge_transaction`` keeps its
policy preflight, object proof, and row deletion in this package-owned
transaction. Nothing outside this module may set the GUC directly;
``tests/test_tombstone_retention_floor.py`` asserts that.
"""

from __future__ import annotations

import re
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from contextvars import ContextVar

PURGE_ROOT_GUC = "matrx.purge_root_id"

_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def _normalize_root(root_file_id: object) -> str:
    """The GUC is read back with ``::uuid``; refuse anything that is not one so
    the failure names the caller instead of surfacing as a cast error inside the
    trigger."""
    text = str(root_file_id or "").strip()
    if not _UUID_RE.match(text):
        raise ValueError(
            f"purge_escape: matrx.purge_root_id must be the uuid of the file at the "
            f"root of the delete-forever operation, got {root_file_id!r}. Pass the "
            f"file id you are hard-deleting."
        )
    return text


# The root currently escaped, so the cascade's recursive self-calls reuse the
# transaction the root opened instead of re-opening one per descendant with the
# wrong root. A ContextVar, not a module global: concurrent delete-forevers on
# the same event loop must not see each other's root.
_active_root: ContextVar[str | None] = ContextVar("matrx_files_purge_root", default=None)


@asynccontextmanager
async def purge_escape(root_file_id: object) -> AsyncIterator[None]:
    """Open a transaction with ``matrx.purge_root_id`` set to *root_file_id*.

    Everything inside the block runs in that one transaction, so the escape
    covers the whole cascade and vanishes the moment it commits or rolls back —
    it can never leak onto a pooled connection.

    Re-entrant by design: the cascade recurses into its own children, and a
    descendant is already covered by the root's escape, so a nested call yields
    straight through rather than opening a second transaction whose root would
    be the child. A nested call naming a DIFFERENT tree is a bug, not a nesting,
    and raises.
    """
    from matrx_orm import set_local_guc, transaction

    from matrx_files.db import ensure_bound

    root = _normalize_root(root_file_id)
    outer = _active_root.get()
    if outer is not None:
        yield
        return
    token = _active_root.set(root)
    try:
        async with transaction(database=ensure_bound()):
            await set_local_guc(PURGE_ROOT_GUC, root)
            yield
    finally:
        _active_root.reset(token)


async def purge_escaped[T](root_file_id: object, run: Callable[[], Awaitable[T]]) -> T:
    """Await ``run()`` inside :func:`purge_escape` for *root_file_id*."""
    async with purge_escape(root_file_id):
        return await run()


def drive_sync[T](run: Callable[[], Awaitable[T]]) -> T:
    """Run an already-escaped async delete on its own loop, for the sync twins.

    The escape is a transaction-local GUC, so the delete has to ride an
    explicitly opened transaction — which only the async ORM surface offers.
    The sync twin therefore drives the async path exactly as
    ``matrx_orm.call_function_sync`` does. Refuses inside a live loop rather
    than deadlocking, matching every other sync twin in this package.
    """
    import asyncio

    from matrx_orm.core.async_db_manager import run_sync

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        pass
    else:
        raise RuntimeError(
            "drive_sync() called inside a running event loop. Await the async "
            "twin (…_async) instead."
        )

    return run_sync(run())
