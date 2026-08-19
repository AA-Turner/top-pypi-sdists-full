# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import attrs
from tenacity import (
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from geneva.apply.task import (
    CopyTask,
    ReadTask,
    ScanTask,
    _stable_namespace_properties,
)
from geneva.credentials import (
    force_revend_storage_options,
    is_credential_expiry_error,
    table_handle_credentials_expiring,
)
from geneva.utils import object_store_retry

if TYPE_CHECKING:
    from geneva.table import Table, TableReference

_LOG = logging.getLogger(__name__)

TableCacheKey = tuple[
    tuple[str, ...],
    str | None,
    tuple[tuple[str, str], ...] | None,
    tuple[str, ...] | None,
    int | None,
]


def _table_cache_key(table_ref: TableReference) -> TableCacheKey:
    ns = table_ref.namespace_config
    namespace_client_properties = _stable_namespace_properties(
        ns.namespace_client_properties
    )

    system_namespace = None
    if ns.system_namespace is not None:
        system_namespace = tuple(ns.system_namespace)

    return (
        tuple(table_ref.table_id),
        ns.namespace_client_impl,
        namespace_client_properties,
        system_namespace,
        table_ref.version,
    )


@attrs.define
class TableCache:
    _tables: dict[TableCacheKey, Table] = attrs.field(
        factory=dict,
        repr=lambda d: f"<{len(d)} cached table(s)>",
    )

    def get_or_open(self, table_ref: TableReference) -> Table:
        key = _table_cache_key(table_ref)
        table = self._tables.get(key)
        if table is not None and table_handle_credentials_expiring(table):
            # Drop the stale handle so we re-open below, which re-vends fresh
            # credentials (TableReference.open -> open_db). Without this the
            # cache pins the plan-time token for the actor's whole lifetime.
            _LOG.debug(
                "TableCache: evicting %s; cached vended credentials near expiry",
                table_ref.table_id,
            )
            del self._tables[key]
            table = None
        if table is None:
            max_retries, retry_base_backoff, retry_max_backoff = (
                object_store_retry.get_applier_retry_settings()
            )

            def _before_sleep(retry_state) -> None:  # noqa: ANN001
                exc = (
                    retry_state.outcome.exception()
                    if retry_state.outcome is not None
                    else None
                )
                backoff = (
                    retry_state.next_action.sleep
                    if retry_state.next_action is not None
                    else 0.0
                )
                _LOG.warning(
                    (
                        "Transient object store error opening table %s "
                        "(retry %d/%d). Sleeping %.2fs before retry. Error: %s"
                    ),
                    table_ref.table_id,
                    retry_state.attempt_number,
                    max_retries,
                    backoff,
                    exc,
                )

            retrier = Retrying(
                retry=retry_if_exception(
                    object_store_retry.is_retryable_object_store_error
                ),
                stop=stop_after_attempt(max_retries + 1),
                wait=wait_exponential_jitter(
                    initial=retry_base_backoff,
                    max=retry_max_backoff,
                ),
                reraise=True,
                before_sleep=_before_sleep,
            )

            for attempt in retrier:
                with attempt:
                    table = table_ref.open()
            assert table is not None
            self._tables[key] = table
        assert table is not None
        return table

    def evict(self, table_ref: TableReference) -> None:
        """Force-drop a cached table so the next open re-vends fresh creds.

        Used by the reactive credential-refresh path: an object-store
        expired-token error proves the cached handle's creds are dead even when
        their stated expiry has not yet passed (early revocation / clock skew),
        so eviction here bypasses the proactive expiry-window check in
        :meth:`get_or_open`.
        """
        self._tables.pop(_table_cache_key(table_ref), None)


def _revend_ref(ref: TableReference) -> TableReference:
    """Return a copy of ``ref`` with force-re-vended storage options.

    Bypasses the proactive expiry window -- a live expired-token error proves
    the credential is dead even if its stated expiry is still in the future.
    Falls back to the existing ref when there is no namespace to re-vend from or
    the re-vend fails, so the retry surfaces the original error.
    """
    fresh = force_revend_storage_options(
        table_id=ref.table_id,
        namespace_client_factory=lambda: ref.connect_namespace(use_worker_props=True),
        label="task table",
    )
    if fresh is None:
        return ref
    return attrs.evolve(ref, storage_options=fresh)


def refresh_task_credentials(task: ReadTask, table_cache: TableCache) -> None:
    """Force-re-vend a task's table credentials after an expired-token error.

    The applier retry loop binds each table once, so replaying a read after an
    expired-credential error would reuse the same dead token. Force a fresh vend
    (bypassing the proactive expiry window), rebuild the task's table refs, drop
    the cache entries, and re-bind so the retry opens with the new credentials.
    """
    if isinstance(task, ScanTask):
        task.table_ref = _revend_ref(task.table_ref)
        table_cache.evict(task.table_ref_for_read())
    elif isinstance(task, CopyTask):
        task.src = _revend_ref(task.src)
        task.dst = _revend_ref(task.dst)
        table_cache.evict(task.src)
        table_cache.evict(task.dst)
    else:
        _LOG.warning(
            "refresh_task_credentials: unhandled task type %s", type(task).__name__
        )
        return
    bind_tables_for_task(task, table_cache)


def maybe_refresh_credentials_on_retry(
    exc: BaseException | None, task: ReadTask, table_cache: TableCache
) -> bool:
    """Force-re-vend a task's credentials when a retry was caused by an expired
    vended token.
    """
    if exc is None or not is_credential_expiry_error(exc):
        return False
    try:
        refresh_task_credentials(task, table_cache)
        return True
    except Exception:  # noqa: BLE001 - best-effort; the retry surfaces the error
        _LOG.warning(
            "reactive credential refresh failed for task %s", task, exc_info=True
        )
        return False


def bind_tables_for_task(task: ReadTask, table_cache: TableCache) -> None:
    if isinstance(task, ScanTask):
        table = table_cache.get_or_open(task.table_ref_for_read())
        task.bind_table(table)
        return

    if isinstance(task, CopyTask):
        src_table = table_cache.get_or_open(task.src)
        dst_table = table_cache.get_or_open(task.dst)
        task.bind_tables(src=src_table, dst=dst_table)
        return

    _LOG.warning("bind_tables_for_task: unhandled task type %s", type(task).__name__)


def clear_bound_tables(task: ReadTask) -> None:
    if isinstance(task, ScanTask):
        task.clear_table()
        return

    if isinstance(task, CopyTask):
        task.clear_tables()
        return

    _LOG.warning("clear_bound_tables: unhandled task type %s", type(task).__name__)
