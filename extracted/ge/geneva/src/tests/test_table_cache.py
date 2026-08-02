# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from collections import Counter

import attrs

from geneva.apply.table_cache import (
    TableCache,
    _table_cache_key,
    bind_tables_for_task,
    clear_bound_tables,
)
from geneva.apply.task import CopyTask, ScanTask
from geneva.table import TableReference


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
