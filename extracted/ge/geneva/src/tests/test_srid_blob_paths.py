# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Blob-column read paths keyed by row id on SRID tables (GEN-864).

A blob column produced by backfill lands as DataReplacement column files;
these tests cover reading it back through row-id-keyed APIs:

- ``Table.take_blobs`` right after backfill (offset-keyed wrapper),
- ``LanceDataset.take_blobs(ids=...)`` across a delete + compaction, where
  stable row ids are the only thing keeping the handles valid,
- the non-SRID variant of the same flow, pinning the stale-row-id hazard.
"""

from typing import TYPE_CHECKING

import pyarrow as pa
import pytest
from blob_test_utils import STRING_BLOB_METADATA

from geneva import udf

if TYPE_CHECKING:
    from geneva.db import Connection
    from geneva.table import Table
    from geneva.transformer import UDF

pytestmark = pytest.mark.ray

_SRID_ON = {"new_table_enable_stable_row_ids": "true"}
_SRID_OFF = {"new_table_enable_stable_row_ids": "false"}

_ROWS_PER_FRAG = 4
_N = 2 * _ROWS_PER_FRAG


def _expected_payload(id_: int) -> bytes:
    """Deterministic per-id payload, distinguishable across ids."""
    return bytes((id_ * 37 + i * 29) % 251 for i in range(1024))


def _make_blob_table(db: "Connection", name: str, *, stable: bool) -> "Table":
    """A 2-fragment table with an ``id`` column, ready for a blob backfill."""
    storage_options = {
        **(_SRID_ON if stable else _SRID_OFF),
        "new_table_data_storage_version": "2.0",
    }
    tbl = db.create_table(
        name,
        pa.table({"id": list(range(_ROWS_PER_FRAG))}),
        storage_options=storage_options,
    )
    tbl.add(pa.table({"id": list(range(_ROWS_PER_FRAG, _N))}))
    assert len(tbl.to_lance().get_fragments()) == 2
    return tbl


def _payload_udf(version: str) -> "UDF":
    @udf(
        data_type=pa.large_binary(),
        field_metadata=dict(STRING_BLOB_METADATA),
        version=version,
        num_cpus=0.1,
    )
    def make_payload(id: int) -> bytes:  # noqa: A002
        return bytes((id * 37 + i * 29) % 251 for i in range(1024))

    return make_payload


def _backfill_payload(tbl: "Table", version: str) -> None:
    tbl.add_columns({"payload": _payload_udf(version)})
    result = tbl.backfill("payload", _admission_check=False)
    assert result.status == "DONE"
    tbl.checkout_latest()


def _id_to_rowid(tbl: "Table") -> dict[int, int]:
    t = tbl.to_lance().to_table(columns=["id"], with_row_id=True)
    return dict(zip(t["id"].to_pylist(), t["_rowid"].to_pylist(), strict=True))


def test_blob_udf_backfill_then_take_blobs_srid(db, local_ray_context) -> None:
    """Blobs written by backfill read back correctly per row id.

    ``Table.take_blobs`` forwards its first argument as Lance *indices*
    (offsets), not row ids, so the wrapper is exercised with offsets in
    scan order; stable row ids are reserved for the dataset-level
    ``ids=`` path, the API actually keyed on ``_rowid``. Both must return
    the exact bytes the UDF produced for each id.
    """
    tbl = _make_blob_table(db, "blob_srid", stable=True)
    _backfill_payload(tbl, "blobgen-v1")

    # Offset-keyed wrapper: ids read back in scan (offset) order.
    ids_by_offset = tbl.to_lance().to_table(columns=["id"])["id"].to_pylist()
    assert sorted(ids_by_offset) == list(range(_N))
    blobs = tbl.take_blobs(list(range(_N)), column="payload")
    assert [b.read() for b in blobs] == [_expected_payload(i) for i in ids_by_offset]

    # Row-id-keyed dataset API: stable row ids looked up per id.
    id_to_rowid = _id_to_rowid(tbl)
    ids_sorted = sorted(id_to_rowid)
    rowids = [id_to_rowid[i] for i in ids_sorted]
    blobs = tbl.to_lance().take_blobs("payload", ids=rowids)
    assert [b.read() for b in blobs] == [_expected_payload(i) for i in ids_sorted]


def test_take_blobs_rowid_stable_across_compaction_srid(db, local_ray_context) -> None:
    """Stable row ids keep blob handles valid across delete + compaction.

    Row ids captured before a delete + ``compact_files()`` (fragments merge
    and renumber) must still resolve to the same rows afterwards:
    ``take_blobs(ids=...)`` returns byte-identical payloads for every
    survivor.
    """
    tbl = _make_blob_table(db, "blob_srid_compact", stable=True)
    _backfill_payload(tbl, "blobgen-compact-v1")

    id_to_rowid = _id_to_rowid(tbl)  # pre-compaction row ids
    deleted = {1, 6}
    survivors = sorted(set(range(_N)) - deleted)

    tbl.delete(f"id IN ({', '.join(map(str, sorted(deleted)))})")
    tbl.compact_files()
    tbl.checkout_latest()

    pre_rowids = [id_to_rowid[i] for i in survivors]
    blobs = tbl.to_lance().take_blobs("payload", ids=pre_rowids)
    assert [b.read() for b in blobs] == [_expected_payload(i) for i in survivors]


def test_take_blobs_stale_rowid_after_compaction_non_srid_pins(
    db, local_ray_context
) -> None:
    """Pins the non-SRID hazard: pre-compaction row ids go stale (GEN-864).

    Without stable row ids, a row's id IS its physical address. After a
    delete + compaction the surviving rows move into a new fragment, so row
    ids captured beforehand reference fragments that no longer exist.
    Pinned observation: ``take_blobs(ids=...)`` with the stale ids fails
    loudly — ``ValueError: Invalid user input: rowaddr ... belongs to
    non-existent fragment`` — rather than silently serving bytes for the
    wrong rows. If this ever starts *returning* blobs, the guard below
    refuses wrong bytes; enable stable row ids to keep handles durable.
    """
    tbl = _make_blob_table(db, "blob_nosrid_compact", stable=False)
    _backfill_payload(tbl, "blobgen-nosrid-v1")

    id_to_rowid = _id_to_rowid(tbl)  # physical addresses, not stable ids
    deleted = {1, 6}
    survivors = sorted(set(range(_N)) - deleted)

    tbl.delete(f"id IN ({', '.join(map(str, sorted(deleted)))})")
    tbl.compact_files()
    tbl.checkout_latest()

    pre_rowids = [id_to_rowid[i] for i in survivors]
    ds = tbl.to_lance()
    # If Lance ever stops rejecting stale addresses, this fails with
    # DID NOT RAISE — re-pin then, and verify the returned bytes are not
    # silently wrong.
    with pytest.raises(ValueError, match="non-existent fragment"):
        ds.take_blobs("payload", ids=pre_rowids)
