# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from collections import Counter
from types import SimpleNamespace

import attrs

from geneva.apply.table_cache import (
    TableCache,
    _table_cache_key,
    bind_tables_for_task,
    clear_bound_tables,
    maybe_refresh_credentials_on_retry,
    refresh_task_credentials,
)
from geneva.apply.task import CopyTask, ScanTask
from geneva.credentials import (
    VENDED_EXPIRY_KEY,
)
from geneva.credentials import (
    table_handle_credentials_expiring as _table_credentials_expiring,
)
from geneva.table import TableReference


def _opts(expires_ms: int | None) -> dict[str, str]:
    opts = {"aws_access_key_id": "AKIA", "aws_session_token": "tok"}
    if expires_ms is not None:
        opts[VENDED_EXPIRY_KEY] = str(expires_ms)
    return opts


# Epoch (1970) -> always within the safety window; ~year 2286 -> never.
_EXPIRING = _opts(1)
_FRESH = _opts(9_999_999_999_999)
_STATIC = _opts(None)


class _FakeTable:
    """Minimal stand-in exposing the attrs ``_table_credentials_expiring`` reads."""

    def __init__(
        self, storage_options: dict[str, str] | None, ltbl_options: object = ...
    ) -> None:
        self._storage_options = storage_options
        if ltbl_options is not ...:
            self._ltbl = SimpleNamespace(latest_storage_options=lambda: ltbl_options)


def test_table_cache_reuses_table(monkeypatch) -> None:
    calls: list[tuple[tuple[str, ...], int | None]] = []

    def fake_open(self: TableReference) -> object:
        calls.append((tuple(self.table_id), self.version))
        return object()

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)

    cache = TableCache()
    ref = TableReference(table_id=["db", "tbl"], version=3, db_uri="db://example")

    table_one = cache.get_or_open(ref)
    table_two = cache.get_or_open(ref)

    assert table_one is table_two
    assert calls == [(("db", "tbl"), 3)]


def test_table_cache_key_ignores_ephemeral_namespace_properties() -> None:
    ref_one = TableReference(
        table_id=["tbl"],
        version=3,
        namespace_client_impl="rest",
        namespace_client_properties={
            "uri": "https://api.example",
            "worker_uri": "https://worker-a.example",
            "header.x-lancedb-database": "db",
            "header.x-api-key": "key-a",
            "header.authorization": "Bearer token-a",
            "storage.aws.access_key_id": "access-a",
        },
    )
    ref_two = TableReference(
        table_id=["tbl"],
        version=3,
        namespace_client_impl="rest",
        namespace_client_properties={
            "uri": "https://api.example",
            "worker_uri": "https://worker-b.example",
            "header.x-lancedb-database": "db",
            "header.x-api-key": "key-b",
            "header.authorization": "Bearer token-b",
            "storage.aws.access_key_id": "access-b",
        },
    )
    ref_other_db = TableReference(
        table_id=["tbl"],
        version=3,
        namespace_client_impl="rest",
        namespace_client_properties={
            "uri": "https://api.example",
            "header.x-lancedb-database": "other",
        },
    )

    assert _table_cache_key(ref_one) == _table_cache_key(ref_two)
    assert _table_cache_key(ref_one) != _table_cache_key(ref_other_db)


def test_bind_tables_for_scan_task_reuses_open(monkeypatch) -> None:
    calls: Counter[tuple[tuple[str, ...], int | None]] = Counter()

    def fake_open(self: TableReference) -> object:
        key = (tuple(self.table_id), self.version)
        calls[key] += 1
        return object()

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)

    cache = TableCache()
    ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")

    task_one = ScanTask(
        uri="db://example/tbl",
        table_ref=ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=10,
        version=5,
    )
    task_two = ScanTask(
        uri="db://example/tbl",
        table_ref=ref,
        columns=["a"],
        frag_id=1,
        offset=0,
        limit=10,
        version=5,
    )

    bind_tables_for_task(task_one, cache)
    bind_tables_for_task(task_two, cache)

    assert sum(calls.values()) == 1
    assert task_one._get_table() is task_two._get_table()
    clear_bound_tables(task_one)
    clear_bound_tables(task_two)
    assert task_one._table is None
    assert task_two._table is None


def test_bind_tables_for_copy_task_reuses_open(monkeypatch) -> None:
    calls: Counter[tuple[tuple[str, ...], int | None]] = Counter()

    def fake_open(self: TableReference) -> object:
        key = (tuple(self.table_id), self.version)
        calls[key] += 1
        return object()

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)

    cache = TableCache()
    src_ref = TableReference(table_id=["src"], version=1, db_uri="db://example")
    dst_ref = TableReference(table_id=["dst"], version=2, db_uri="db://example")

    task_one = CopyTask(
        src=src_ref,
        dst=dst_ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=5,
    )
    task_two = CopyTask(
        src=src_ref,
        dst=dst_ref,
        columns=["a"],
        frag_id=1,
        offset=5,
        limit=5,
    )

    bind_tables_for_task(task_one, cache)
    bind_tables_for_task(task_two, cache)

    assert calls[(("src",), 1)] == 1
    assert calls[(("dst",), 2)] == 1
    assert task_one._src_table is task_two._src_table
    assert task_one._dst_table is task_two._dst_table
    clear_bound_tables(task_one)
    clear_bound_tables(task_two)
    assert task_one._src_table is None
    assert task_one._dst_table is None
    assert task_two._src_table is None
    assert task_two._dst_table is None


def test_copy_task_table_uri_uses_source_identity_when_table_uri_cleared() -> None:
    dst_ref = TableReference(
        table_id=["dst"],
        version=2,
        db_uri="db://example",
        table_uri="s3://bucket/dst.lance",
    )
    src_ref = attrs.evolve(
        dst_ref,
        table_id=["src"],
        version=1,
        is_system_table=False,
        table_uri=None,
    )
    task = CopyTask(
        src=src_ref,
        dst=dst_ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=5,
    )

    assert task.table_uri() == "src"


def test_table_cache_distinguishes_default_and_empty_system_namespace(
    monkeypatch,
) -> None:
    calls: list[tuple[list[str], int | None]] = []

    def fake_open(self: TableReference) -> object:
        calls.append((self.system_namespace, self.version))
        return object()

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)

    cache = TableCache()
    default_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    explicit_root_ref = TableReference(
        table_id=["tbl"], version=None, db_uri="db://example", system_namespace=[]
    )

    default_table = cache.get_or_open(default_ref)
    explicit_root_table = cache.get_or_open(explicit_root_ref)

    assert default_table is not explicit_root_table
    assert calls == [(["__system"], None), ([], None)]


def test_table_credentials_expiring() -> None:
    # Near-expiry vended creds -> True; fresh / static / absent -> False.
    assert _table_credentials_expiring(_FakeTable(_EXPIRING)) is True
    assert _table_credentials_expiring(_FakeTable(_FRESH)) is False
    assert _table_credentials_expiring(_FakeTable(_STATIC)) is False
    assert _table_credentials_expiring(_FakeTable(None)) is False
    # Expiry surfaced only via the lance table's latest_storage_options().
    assert _table_credentials_expiring(_FakeTable(None, ltbl_options=_EXPIRING)) is True
    # A broken latest_storage_options() must not crash the check.
    broken = _FakeTable(_STATIC)
    broken._ltbl = SimpleNamespace(
        latest_storage_options=lambda: (_ for _ in ()).throw(RuntimeError("boom"))
    )
    assert _table_credentials_expiring(broken) is False


def test_table_cache_evicts_when_cached_credentials_expiring(monkeypatch) -> None:
    opened: list[_FakeTable] = []

    def fake_open(self: TableReference) -> object:
        table = _FakeTable(_EXPIRING)
        opened.append(table)
        return table

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)

    cache = TableCache()
    ref = TableReference(table_id=["db", "tbl"], version=3, db_uri="db://example")

    first = cache.get_or_open(ref)
    second = cache.get_or_open(ref)

    # The cached handle's vended creds are near expiry, so it is evicted and
    # re-opened (which re-vends) rather than reused with a lapsed token.
    assert second is not first
    assert len(opened) == 2


def test_table_cache_reuses_when_credentials_fresh(monkeypatch) -> None:
    opened: list[_FakeTable] = []

    def fake_open(self: TableReference) -> object:
        table = _FakeTable(_FRESH)
        opened.append(table)
        return table

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)

    cache = TableCache()
    ref = TableReference(table_id=["db", "tbl"], version=3, db_uri="db://example")

    first = cache.get_or_open(ref)
    second = cache.get_or_open(ref)

    # Fresh creds -> the cache reuses the handle without re-opening.
    assert second is first
    assert len(opened) == 1


def test_open_db_revends_expiring_storage_options(monkeypatch) -> None:
    import geneva.table as gt

    seen: dict[str, object] = {}

    def fake_refresh(  # noqa: ANN202
        storage_options,  # noqa: ANN001
        *,
        table_id,  # noqa: ANN001
        namespace_client_factory=None,  # noqa: ANN001
        **kw,  # noqa: ANN003
    ):
        seen["in"] = storage_options
        seen["table_id"] = table_id
        return _FRESH

    captured: dict[str, object] = {}

    def fake_connect(**kwargs) -> object:  # noqa: ANN003
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(gt, "refresh_storage_options", fake_refresh)
    monkeypatch.setattr(gt, "connect", fake_connect)
    monkeypatch.setattr(TableReference, "open_checkpoint_store", lambda self, **k: None)

    ref = TableReference(
        table_id=["db", "tbl"],
        version=3,
        namespace_client_impl="rest",
        namespace_client_properties={"uri": "https://api.example"},
        storage_options=_EXPIRING,
    )
    ref.open_db()

    # open_db routes the shipped (stale) options through refresh_storage_options
    # and connects with the re-vended result, not the plan-time token.
    assert seen["table_id"] == ["db", "tbl"]
    assert seen["in"] == _EXPIRING
    assert captured["storage_options"] == _FRESH


def test_reactive_refresh_recovers_via_retry(monkeypatch) -> None:
    # Drive the read through the same retry mechanism the applier uses: a stale
    # token fails the read with an ExpiredToken object-store error, before_sleep
    # (maybe_refresh_credentials_on_retry) re-vends + rebinds, and the retry then
    # succeeds -- exercising the condition instead of calling the refresh helper
    # directly.
    from tenacity import (
        Retrying,
        retry_if_exception,
        stop_after_attempt,
        wait_none,
    )

    from geneva.utils import object_store_retry

    monkeypatch.setattr(
        "geneva.credentials.revend_storage_options",
        lambda *, table_id, namespace_client=None, **kw: _FRESH,  # noqa: ANN002, ANN003
    )
    monkeypatch.setattr(
        TableReference, "connect_namespace", lambda self, **k: object(), raising=True
    )
    monkeypatch.setattr(
        TableReference,
        "open",
        lambda self: _FakeTable(self.storage_options),
        raising=True,
    )

    cache = TableCache()
    ref = TableReference(
        table_id=["db", "tbl"],
        version=3,
        namespace_client_impl="rest",
        namespace_client_properties={"uri": "https://api.example"},
        storage_options=_EXPIRING,
    )
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=10,
        version=3,
    )
    # The actor binds the table once (stale token) before the read loop.
    bind_tables_for_task(task, cache)

    attempts = {"n": 0}

    def read() -> str:
        attempts["n"] += 1
        opts = task._table._storage_options or {}
        if opts.get(VENDED_EXPIRY_KEY) == _EXPIRING[VENDED_EXPIRY_KEY]:
            # Signing with the dead token -> the object store returns ExpiredToken.
            raise RuntimeError(
                "RuntimeError: lance error: LanceError(IO): Generic S3 error: "
                "Error performing HEAD https://s3.us-east-2.amazonaws.com/"
                "foo/18446744073709550956.manifest in 16.28551ms -"
                " Server returned non-2xx status code: 400 Bad Request:"
            )
        return "rows"

    retrier = Retrying(
        retry=retry_if_exception(object_store_retry.is_retryable_object_store_error),
        stop=stop_after_attempt(3),
        wait=wait_none(),
        reraise=True,
        before_sleep=lambda rs: maybe_refresh_credentials_on_retry(
            rs.outcome.exception() if rs.outcome is not None else None, task, cache
        ),
    )

    result = None
    for attempt in retrier:
        with attempt:
            result = read()

    # Read failed once with ExpiredToken; the retry hook re-vended + rebound, and
    # the second attempt succeeded with fresh credentials.
    assert result == "rows"
    assert attempts["n"] == 2
    assert task.table_ref.storage_options == _FRESH


def test_refresh_task_credentials_without_namespace_is_noop(monkeypatch) -> None:
    # No namespace to re-vend from -> keep the existing ref, still rebind.
    monkeypatch.setattr(
        TableReference, "connect_namespace", lambda self, **k: None, raising=True
    )
    monkeypatch.setattr(
        TableReference, "open", lambda self: _FakeTable(self.storage_options)
    )

    cache = TableCache()
    ref = TableReference(table_id=["db", "tbl"], version=3, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=10,
        version=3,
    )

    refresh_task_credentials(task, cache)

    assert task.table_ref is ref  # unchanged
    assert task._table is not None  # rebound


def test_table_cache_retries_transient_open_failure(monkeypatch) -> None:
    calls: list[tuple[tuple[str, ...], int | None]] = []
    expected_table = object()

    def fake_open(self: TableReference) -> object:
        calls.append((tuple(self.table_id), self.version))
        if len(calls) == 1:
            raise RuntimeError("azure object store timeout")
        return expected_table

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)
    monkeypatch.setattr(
        "geneva.apply.table_cache.object_store_retry.APPLIER_TRANSIENT_RETRIES",
        1,
    )
    monkeypatch.setattr(
        (
            "geneva.apply.table_cache."
            "object_store_retry.APPLIER_RETRY_BASE_BACKOFF_SECONDS"
        ),
        0.0,
    )
    monkeypatch.setattr(
        (
            "geneva.apply.table_cache."
            "object_store_retry.APPLIER_RETRY_MAX_BACKOFF_SECONDS"
        ),
        0.0,
    )

    cache = TableCache()
    ref = TableReference(table_id=["db", "tbl"], version=3, db_uri="db://example")

    table_one = cache.get_or_open(ref)
    table_two = cache.get_or_open(ref)

    assert table_one is expected_table
    assert table_two is expected_table
    assert calls == [(("db", "tbl"), 3), (("db", "tbl"), 3)]
