# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""GEN-758: eligible dir-namespace tables are read via direct physical-URI opens.

Namespace-backed datasets re-resolve the table through the namespace during
scan IO; transient failures of that lookup killed long scans. Eligible reads
now open by physical URI; everything else keeps the namespace-backed open.
"""

import logging
import types
from pathlib import Path

import lance
import pyarrow as pa
import pytest

from geneva.db import connect
from geneva.query import (
    _direct_open_uri,
    clear_read_dataset_cache,
    open_read_dataset,
)
from geneva.table import Table


@pytest.fixture(autouse=True)
def _fresh_cache():  # noqa: ANN202
    clear_read_dataset_cache()
    yield
    clear_read_dataset_cache()


def _make_table(tmp_path: Path) -> Table:
    db = connect(tmp_path)
    return db.create_table("t", pa.table({"id": pa.array(range(20), pa.int32())}))


def _stub_table(
    impl: str | None = "dir",
    props: dict[str, str] | None = None,
    branch: str | None = None,
    uri: str = "file:///tmp/t.lance",
) -> types.SimpleNamespace:
    ns_config = types.SimpleNamespace(
        namespace_client_impl=impl,
        namespace_client_properties=props,
    )
    conn = types.SimpleNamespace(_ns_config=ns_config, _storage_options=None)
    ltbl = types.SimpleNamespace(current_branch=lambda: branch)
    return types.SimpleNamespace(_conn=conn, _ltbl=ltbl, uri=uri, _storage_options=None)


def test_dir_table_opens_direct(tmp_path) -> None:
    tbl = _make_table(tmp_path)

    # to_lance() (previous behavior) is namespace-backed.
    assert getattr(tbl.to_lance(), "_namespace_client", None) is not None

    ds = open_read_dataset(tbl)
    assert getattr(ds, "_namespace_client", None) is None
    assert ds.version == tbl.version
    assert ds.count_rows() == 20


def test_direct_open_pins_version(tmp_path) -> None:
    tbl = _make_table(tmp_path)
    v1 = tbl.version
    tbl.add([{"id": 100}])
    clear_read_dataset_cache()

    pinned = open_read_dataset(tbl, version=v1)
    assert pinned.version == v1
    assert pinned.count_rows() == 20
    assert getattr(pinned, "_namespace_client", None) is None

    clear_read_dataset_cache()
    latest = open_read_dataset(tbl)
    assert latest.version == tbl.version
    assert latest.count_rows() == 21


def test_direct_open_failure_falls_back_to_namespace(
    tmp_path, monkeypatch, caplog
) -> None:
    tbl = _make_table(tmp_path)
    real_dataset = lance.dataset

    def failing_direct(uri=None, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003, ANN202
        # Fail only the direct-shape call (positional uri, no namespace_client).
        if uri is not None and "namespace_client" not in kwargs:
            raise RuntimeError("simulated direct-open failure")
        if uri is None:
            return real_dataset(*args, **kwargs)
        return real_dataset(uri, *args, **kwargs)

    monkeypatch.setattr(lance, "dataset", failing_direct)

    with caplog.at_level(logging.WARNING, logger="geneva.query"):
        ds = open_read_dataset(tbl)

    assert getattr(ds, "_namespace_client", None) is not None
    assert ds.count_rows() == 20
    assert "Direct read open failed" in caplog.text


def test_worker_reference_open_seeds_uri_and_opens_direct(tmp_path) -> None:
    tbl = _make_table(tmp_path)
    ref = tbl.get_reference()
    assert ref.table_uri

    worker_tbl = ref.open()
    assert worker_tbl.__dict__.get("uri") == ref.table_uri

    ds = open_read_dataset(worker_tbl)
    assert getattr(ds, "_namespace_client", None) is None
    assert ds.count_rows() == 20


def test_eligible_stub_returns_uri() -> None:
    assert _direct_open_uri(_stub_table()) == "file:///tmp/t.lance"


def test_rest_namespace_is_ineligible() -> None:
    assert _direct_open_uri(_stub_table(impl="rest")) is None


def test_missing_namespace_impl_is_ineligible() -> None:
    assert _direct_open_uri(_stub_table(impl=None)) is None


@pytest.mark.parametrize(
    "props",
    [
        {"credential_vendor.enabled": "true"},
        {"credential_vendor.enabled": "false"},
        {"CREDENTIAL_VENDOR.permission": "read"},
        {"vend_input_storage_options": "true"},
    ],
    ids=["vendor-enabled", "vendor-disabled", "vendor-case", "vend-input"],
)
def test_credential_vending_is_ineligible(props: dict[str, str]) -> None:
    assert _direct_open_uri(_stub_table(props=props)) is None


def test_branch_checkout_is_ineligible() -> None:
    assert _direct_open_uri(_stub_table(branch="dev")) is None


def test_raw_lancedb_table_shape_is_ineligible() -> None:
    # db.py passes a raw lancedb table (has _conn but no _ns_config).
    raw = types.SimpleNamespace(_conn=types.SimpleNamespace())
    assert _direct_open_uri(raw) is None


def test_object_without_conn_is_ineligible() -> None:
    assert _direct_open_uri(types.SimpleNamespace()) is None
