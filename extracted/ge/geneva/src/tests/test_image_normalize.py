# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit test for ``normalize_image`` across the three image-column encodings.

Builds three small tables from the same synthetic JPEGs -- plain ``binary``,
top-level blob ``large_binary``, and a nested ``struct<image_bytes(blob), ...>``
-- and asserts that the same ``normalize_image`` UDF, bound to each table's
respective input column, produces byte-identical 224x224 grayscale PNG output
across all three encodings.
"""

from __future__ import annotations

import hashlib
import io
from typing import TYPE_CHECKING

import pyarrow as pa
import pytest
from PIL import Image

from geneva import connect
from geneva.udfs.image.simple import normalize_image

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.table import Table

BLOB_META = {"lance-encoding:blob": "true"}
_2_0_STORAGE = {"new_table_data_storage_version": "2.0"}


def _synthetic_jpegs(n: int) -> list[bytes]:
    """Deterministic small JPEGs at varying sizes (no Hugging Face download)."""
    imgs: list[bytes] = []
    for i in range(n):
        size = (40 + 10 * i, 30 + 5 * i)
        img = Image.new("RGB", size, color=(20 + 30 * i, 100, 200 - 20 * i))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        imgs.append(buf.getvalue())
    return imgs


def _plain_table(db, imgs: list[bytes]) -> Table:  # noqa: ANN001
    schema = pa.schema([pa.field("id", pa.int64()), pa.field("image", pa.binary())])
    return db.create_table(
        "plain",
        pa.table(
            {
                "id": pa.array(range(len(imgs)), pa.int64()),
                "image": pa.array(imgs, pa.binary()),
            },
            schema=schema,
        ),
        storage_options=_2_0_STORAGE,
    )


def _blob_table(db, imgs: list[bytes]) -> Table:  # noqa: ANN001
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image_blob", pa.large_binary(), metadata=BLOB_META),
        ]
    )
    return db.create_table(
        "blob",
        pa.table(
            {
                "id": pa.array(range(len(imgs)), pa.int64()),
                "image_blob": pa.array(imgs, pa.large_binary()),
            },
            schema=schema,
        ),
        storage_options=_2_0_STORAGE,
    )


def _nested_table(db, imgs: list[bytes]) -> Table:  # noqa: ANN001
    n = len(imgs)
    struct_type = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=BLOB_META),
            pa.field("time", pa.int32()),
            pa.field("error", pa.string()),
        ]
    )
    image = pa.StructArray.from_arrays(
        [
            pa.array(imgs, pa.large_binary()),
            pa.nulls(n, pa.int32()),
            pa.nulls(n, pa.string()),
        ],
        fields=list(struct_type),
    )
    schema = pa.schema([pa.field("id", pa.int64()), pa.field("image", struct_type)])
    return db.create_table(
        "nested",
        pa.table(
            {"id": pa.array(range(n), pa.int64()), "image": image},
            schema=schema,
        ),
        storage_options=_2_0_STORAGE,
    )


def _normalize_outputs(
    tbl,  # noqa: ANN001
    input_col: str,
    strategy: str,
    concurrency: int = 2,
) -> list[bytes]:
    """Add ``image_norm``, backfill, return outputs ordered by id.

    ``concurrency`` is kept low so the pipelined applier (which reserves
    ``1 + pipelining_num_readers`` CPUs per actor) fits on small CI boxes.
    """
    tbl.add_columns({"image_norm": (normalize_image, [input_col])})
    tbl.backfill("image_norm", blob_read_strategy=strategy, concurrency=concurrency)
    rows = sorted(
        tbl.search().select(["id", "image_norm"]).to_arrow().to_pylist(),
        key=lambda r: r["id"],
    )
    return [r["image_norm"] for r in rows]


@pytest.mark.parametrize("pipelined", [False, True], ids=["simple", "pipelined"])
@pytest.mark.slow
def test_normalize_image_across_encodings(
    tmp_path: Path,
    local_ray_context,  # noqa: ANN001  (fixture from conftest)
    monkeypatch: pytest.MonkeyPatch,
    pipelined: bool,
) -> None:
    """Same UDF on plain / top-level blob / nested blob => identical output.

    Parametrized to run twice -- once on ``SimpleApplier`` (baseline) and once
    on ``CollocatedPipelinedApplier`` -- so the pipelined applier is verified
    correctness-equivalent on all three image-column encodings.
    """
    if pipelined:
        monkeypatch.setenv("GENEVA__JOB__ENABLE_GPU_PIPELINING", "true")
        # Keep readers small: each actor reserves 1+N CPUs.
        monkeypatch.setenv("GENEVA__JOB__PIPELINING_NUM_READERS", "2")

    imgs = _synthetic_jpegs(4)
    db = connect(str(tmp_path))

    plain_out = _normalize_outputs(_plain_table(db, imgs), "image", "auto")
    blob_out = _normalize_outputs(_blob_table(db, imgs), "image_blob", "auto")
    nested_out = _normalize_outputs(
        _nested_table(db, imgs), "image.image_bytes", "range"
    )

    # Every output decodes as a 224x224 grayscale PNG.
    for outputs in (plain_out, blob_out, nested_out):
        assert len(outputs) == len(imgs)
        for out in outputs:
            im = Image.open(io.BytesIO(out))
            assert im.size == (224, 224)
            assert im.mode == "L"

    # Byte-identical across encodings for matching ids.
    def _md5(b: bytes) -> str:
        return hashlib.md5(b).hexdigest()

    plain_md5s = [_md5(b) for b in plain_out]
    assert plain_md5s == [_md5(b) for b in blob_out]
    assert plain_md5s == [_md5(b) for b in nested_out]


def test_normalize_image_handles_bad_inputs() -> None:
    """Truncated JPEGs decode via LOAD_TRUNCATED_IMAGES; outright garbage
    returns None instead of raising. Web-scraped datasets (e.g. laion-1m)
    routinely contain partially-truncated JPEGs that would otherwise abort
    the whole backfill task with ``OSError: image file is truncated``.
    """
    # Build a valid JPEG, then chop off trailing bytes so PIL would normally
    # raise during a full pixel decode (convert/resize forces decode).
    img = Image.new("RGB", (100, 100), color=(50, 100, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    truncated = buf.getvalue()[:-50]

    # Truncated input still decodes -> valid 224x224 grayscale PNG.
    out_trunc = normalize_image.func(truncated)
    assert out_trunc is not None
    im = Image.open(io.BytesIO(out_trunc))
    assert im.size == (224, 224)
    assert im.mode == "L"

    # Outright undecodable bytes -> None (no exception).
    assert normalize_image.func(b"not an image at all\x00\xff" * 10) is None
