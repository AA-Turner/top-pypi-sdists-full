# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
End-to-end pipeline test for large image embedding.

Runs all backfills in sequence:
1. decoded (decode base64 + extract width/height)
2. preprocessed (ViT preprocessing)
3. vit_logits (ViT inference)
"""

import logging

import pytest

_LOG = logging.getLogger(__name__)

DERIVED_COLUMNS = ["decoded", "preprocessed", "vit_logits"]
LOGITS_DIM = 1000
PREPROCESSED_DIM = 3 * 224 * 224


def _run_pipeline(tbl, conn, cluster_name: str, manifest_name: str, batch_size: int) -> None:
    with conn.context(cluster=cluster_name, manifest=manifest_name):
        for col in DERIVED_COLUMNS:
            _LOG.info("Backfilling column %s", col)
            tbl.backfill(col, batch_size=batch_size)


def test_large_image_embedding_pipeline(
    image_table,
    standard_cluster,
    batch_size,
    manifest_name,
) -> None:
    conn, tbl, table_name = image_table

    _LOG.info(
        "Starting large image embedding pipeline on table %s (rows=%s)",
        table_name,
        len(tbl),
    )

    _run_pipeline(tbl, conn, standard_cluster, manifest_name, batch_size)

    decoded_df = (
        tbl.search()
        .select(["decoded"])
        .where("decoded IS NOT NULL")
        .limit(1)
        .to_pandas()
    )
    if len(decoded_df) == 0:
        pytest.fail("No decoded rows produced; check UDF and data availability")
    decoded = decoded_df["decoded"].iloc[0]
    assert "width" in decoded and "height" in decoded, (
        "decoded should include width/height"
    )
    assert decoded["width"] > 0 and decoded["height"] > 0, "dimensions should be positive"
    assert decoded.get("image_bytes"), "decoded should include image_bytes"

    preprocessed_df = (
        tbl.search()
        .select(["preprocessed"])
        .where("preprocessed IS NOT NULL")
        .limit(1)
        .to_pandas()
    )
    if len(preprocessed_df) == 0:
        pytest.fail("No preprocessed rows produced; check UDF and data availability")
    preprocessed = preprocessed_df["preprocessed"].iloc[0]
    assert len(preprocessed) == PREPROCESSED_DIM, (
        f"Expected preprocessed dim {PREPROCESSED_DIM}, got {len(preprocessed)}"
    )

    logits_df = (
        tbl.search()
        .select(["vit_logits"])
        .where("vit_logits IS NOT NULL")
        .limit(1)
        .to_pandas()
    )
    if len(logits_df) == 0:
        pytest.fail("No logits produced; check UDF and data availability")
    first_logits = logits_df["vit_logits"].iloc[0]
    assert len(first_logits) == LOGITS_DIM, (
        f"Expected logits dim {LOGITS_DIM}, got {len(first_logits)}"
    )

    _LOG.info("✓ Large image embedding pipeline completed successfully")
