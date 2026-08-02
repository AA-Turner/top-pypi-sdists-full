# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E tests for the AV image curation pipeline.

Exercises the Use Case #9 workflow: batched UDFs for object detection and
scene classification, filtered queries on struct columns, and materialized
view creation for curated training datasets.

Models:
  - google/owlv2-base-patch16-ensemble (object detection, Apache-2.0)
  - google/siglip2-so400m-patch14-224  (zero-shot classification, Apache-2.0)
"""

import logging
import uuid

import pytest

# Tests run against the session-scoped shared table from the `image_table`
# fixture. The shared table already has the UDF columns (vehicle, scene)
# attached by upload_manifests.py; the `_udfs/<hash>` blobs live alongside
# that table on object storage. We deliberately do NOT copy the table per
# test: `conn.create_table(new_name, shared_tbl.to_arrow(), ...)` carries
# the virtual_column metadata pointing at `_udfs/<hash>` but does not copy
# the blob, which makes workers 404 when fetching the UDF.
# Backfill is idempotent, so tests reusing the shared table is safe.

_LOG = logging.getLogger(__name__)

MANIFEST_NAME = "av-curation-udfs-v1"

# Domain-specific labels for the AV use case -- the UDFs themselves are generic.
VEHICLE_QUERIES = [
    "red ambulance",
    "yellow ambulance",
    "fire truck",
    "police car",
    "traffic light",
    "articulated bus",
    "oversized load",
    "construction vehicle",
    "sedan",
    "suv",
    "pickup",
    "truck",
]

SCENE_LABELS = [
    "mountain road",
    "crossroads intersection",
    "construction zone",
    "highway",
    "residential street",
    "tunnel",
    "parking lot",
    "rural road",
    "bridge",
    "school zone",
]


# ---------------------------------------------------------------------------
# Individual UDF tests
# ---------------------------------------------------------------------------


def test_object_detection_backfill(
    image_table: tuple,
    gpu_cluster: str,
    batch_size: int,
    skip_gpu: bool,
) -> None:
    """Backfill the ObjectDetector batched UDF and validate struct output."""
    if skip_gpu:
        pytest.skip("GPU tests skipped (--skip-gpu)")

    conn, tbl, _ = image_table
    num_images = len(tbl)
    vehicle_col = "vehicle"

    with conn.context(cluster=gpu_cluster, manifest=MANIFEST_NAME):
        _LOG.info("Backfilling %s", vehicle_col)
        tbl.backfill(vehicle_col, batch_size=batch_size)

    tbl.checkout_latest()
    df = tbl.to_pandas()

    _LOG.info("Completed object detection backfill for %d rows", len(df))

    assert vehicle_col in df.columns
    assert df[vehicle_col].notna().all()
    assert len(df) == num_images

    # Validate struct fields.
    sample = df[vehicle_col].iloc[0]
    assert "label" in sample
    assert "confidence" in sample
    assert "bbox_area_pct" in sample

    for _, row in df.iterrows():
        v = row[vehicle_col]
        assert 0.0 <= v["confidence"] <= 1.0
        assert 0.0 <= v["bbox_area_pct"] <= 1.0
        assert v["label"] in VEHICLE_QUERIES or v["label"] == "none"

    _LOG.info("Object detection test passed!")


def test_scene_classification_backfill(
    image_table: tuple,
    gpu_cluster: str,
    batch_size: int,
    skip_gpu: bool,
) -> None:
    """Backfill the ZeroShotClassifier batched UDF and validate output."""
    if skip_gpu:
        pytest.skip("GPU tests skipped (--skip-gpu)")

    conn, tbl, _ = image_table
    num_images = len(tbl)
    scene_col = "scene"

    with conn.context(cluster=gpu_cluster, manifest=MANIFEST_NAME):
        _LOG.info("Backfilling %s", scene_col)
        tbl.backfill(scene_col, batch_size=batch_size)

    tbl.checkout_latest()
    df = tbl.to_pandas()

    _LOG.info("Completed scene classification backfill for %d rows", len(df))

    assert scene_col in df.columns
    assert df[scene_col].notna().all()
    assert len(df) == num_images

    sample = df[scene_col].iloc[0]
    assert "top_label" in sample
    assert "top_score" in sample

    for _, row in df.iterrows():
        s = row[scene_col]
        assert 0.0 <= s["top_score"] <= 1.0
        assert s["top_label"] in SCENE_LABELS or s["top_label"] == "unknown"

    _LOG.info("Scene classification test passed!")


# ---------------------------------------------------------------------------
# Full curation pipeline test (Use Case #9)
# ---------------------------------------------------------------------------


def test_full_curation_pipeline(
    image_table: tuple,
    gpu_cluster: str,
    batch_size: int,
    skip_gpu: bool,
) -> None:
    """Exercise the complete AV image curation workflow.

    Steps:
    1. Backfill ObjectDetector + ZeroShotClassifier columns
    2. Query with struct field filters
    3. Create materialized view from filtered query
    4. Validate the materialized view
    """
    if skip_gpu:
        pytest.skip("GPU tests skipped (--skip-gpu)")

    conn, tbl, _ = image_table

    with conn.context(cluster=gpu_cluster, manifest=MANIFEST_NAME):
        _LOG.info("Backfilling vehicle + scene columns")
        tbl.backfill("vehicle", batch_size=batch_size)
        tbl.backfill("scene", batch_size=batch_size)

    tbl.checkout_latest()

    # Find images where detection found something with >10% coverage.
    filtered = tbl.search().where(
        "vehicle.label != 'none' "
        "AND vehicle.confidence > 0.3 "
        "AND vehicle.bbox_area_pct >= 0.10"
    )
    filtered_count = filtered.count_rows()
    _LOG.info(
        "Filtered query: %d rows (vehicles >10%% coverage)",
        filtered_count,
    )
    assert filtered_count >= 1, "Expected at least 1 detected vehicle in COCO images"

    # Create materialized view.
    view_name = f"curated_{uuid.uuid4().hex}"
    _LOG.info("Creating materialized view '%s'", view_name)
    view = conn.create_materialized_view(view_name, filtered)
    view.refresh()

    field_names = [f.name for f in view.schema]
    assert "vehicle" in field_names
    assert "scene" in field_names

    view_count = view.count_rows()
    _LOG.info(
        "Materialized view '%s': %d rows",
        view_name,
        view_count,
    )
    assert view_count >= 1, "Materialized view should contain at least 1 row"

    conn.drop_table(view_name)
    _LOG.info("Full curation pipeline test passed!")
