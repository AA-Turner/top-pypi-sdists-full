"""Standalone repro: legacy (non-deferred) filtered carry-forward of a top-level
BLOB column crashes in the applier.

Run (no Ray cluster needed -- uses the in-process ray shim):

    uv run python src/tests/repro_legacy_blob_cf.py

Conditions (all on the DEFAULT config -- GENEVA_DEFER_CARRY_FORWARD unset/0):
  * a filtered backfill (where=... that leaves UNMATCHED rows in a fragment), of
  * a blob (large_binary + lance-encoding:blob) OUTPUT column produced by a UDF
    whose input is NOT a blob -- so the blob is a carry-forward / non-UDF-input
    column that the filtered re-backfill must carry forward for unmatched rows.

Expected today: the applier's legacy carry-forward merge builds
``pa.array(old_values, type=large_binary())`` from un-read ``BlobFile`` objects
(apply/task.py, list-of-dicts branch) -> ``ArrowTypeError: Expected bytes, got a
'BlobFile' object``. A struct-with-nested-blob output does NOT hit it (printed for
contrast -- the asymmetry).

NOTE: this is the *legacy* applier path (deferred CF off, no opt-in flag).
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ray_shim  # noqa: E402

ray_shim.install()  # MUST precede the geneva import

import pyarrow as pa  # noqa: E402

import geneva.runners.ray.pipeline as p  # noqa: E402
from geneva import connect, udf  # noqa: E402

ray_shim.stub_geneva_cluster_polling()

assert not p.DEFAULT_DEFER_CARRY_FORWARD, "repro is the DEFAULT (deferred CF off) path"


@udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
def make_blob(value: int) -> bytes:
    return f"v={value * 2}".encode()


_IMG = pa.struct(
    [
        pa.field(
            "image_bytes", pa.large_binary(), metadata={b"lance-encoding:blob": b"true"}
        ),
        pa.field("width", pa.int64()),
    ]
)


@udf(data_type=_IMG)
def make_struct_blob(value: int) -> dict:
    return {"image_bytes": f"v={value * 2}".encode(), "width": value}


def run(label: str, the_udf, col: str) -> None:
    db = connect(tempfile.mkdtemp())
    t = db.create_table(
        col,
        pa.table({"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]}),
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )
    t.add_columns({col: the_udf})
    t.backfill(col, where=None, _admission_check=False)  # full backfill, no carry-fwd
    # Filtered re-backfill: value>25 matches id 3,4; id 1,2 are UNMATCHED and must
    # be carried forward -- which reads their old blob value on the applier.
    try:
        t.backfill(col, where="value > 25", _admission_check=False)
        print(f"[{label}] OK (no crash)")  # noqa: T201
    except Exception as ex:  # noqa: BLE001
        print(f"[{label}] CRASH {type(ex).__name__}: {str(ex)[-160:]}")  # noqa: T201


run("blob (top-level large_binary)", make_blob, "img")
run("structblob (nested blob leaf) ", make_struct_blob, "image")
