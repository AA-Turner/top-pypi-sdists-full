# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E test-specific fixtures for the AV image curation suite.

Shared fixtures live in e2e/conftest.py; this file provides suite-specific
options and helpers.
"""

import logging
import os
import uuid
from collections.abc import Generator
from pathlib import Path

import pyarrow as pa
import pytest

from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder

_LOG = logging.getLogger(__name__)

_MANIFESTS_UPLOADED = False
DEFAULT_HEAD_MEMORY = "3Gi"
AZURE_HEAD_MEMORY = "8Gi"


def _head_memory_for_csp(csp: str) -> str:
    if csp == "azure":
        return AZURE_HEAD_MEMORY
    return DEFAULT_HEAD_MEMORY


def _upload_all_manifests(bucket_path: str) -> None:
    """Upload all suite manifests and add columns to the table."""
    import subprocess

    _LOG.info("Uploading AV curation UDF manifests...")
    suite_dir = Path(__file__).parent
    result = subprocess.run(
        ["uv", "run", "python", "upload_manifests.py", "--bucket", bucket_path],
        cwd=str(suite_dir),
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            _LOG.info("  [upload] %s", line)
    if result.stderr:
        for line in result.stderr.splitlines():
            _LOG.warning("  [upload] %s", line)
    if result.returncode != 0:
        raise RuntimeError("Manifest upload failed for AV image curation suite")

    _LOG.info("All manifests uploaded and columns added")


# ============================================================================
# E2E test-specific pytest options
# ============================================================================


def pytest_addoption(parser) -> None:  # type: ignore[no-untyped-def]
    """Add e2e-specific command-line options."""
    parser.addoption(
        "--num-images",
        action="store",
        type=int,
        default=100,
        help="Number of images to load from COCO dataset",
    )
    parser.addoption(
        "--batch-size",
        action="store",
        type=int,
        default=10,
        help="Batch size for backfill operations",
    )
    parser.addoption(
        "--skip-gpu",
        action="store_true",
        default=False,
        help="Skip GPU-based tests",
    )


@pytest.fixture(scope="session")
def head_node_selector(csp: str) -> dict:
    """Node selector for Ray head nodes."""
    return (
        {"geneva.lancedb.com/ray-head": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )


@pytest.fixture(scope="session")
def worker_node_selector(csp: str) -> dict:
    """Node selector for Ray worker nodes (CPU)."""
    return (
        {"geneva.lancedb.com/ray-worker-cpu": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )


# ============================================================================
# Dataset Loading Utilities
# ============================================================================

ImageBatchGenerator = Generator[pa.RecordBatch, None, None]


def load_coco_images(num_images: int = 100, frag_size: int = 25) -> ImageBatchGenerator:
    """Load images from a COCO-format dataset on HuggingFace.

    Yields PyArrow RecordBatches with columns: image (bytes), category (string).
    """
    import io

    from datasets import load_dataset

    from geneva.tqdm import tqdm

    _LOG.info("Loading %d images from COCO dataset", num_images)

    try:
        dataset = load_dataset(
            "detection-datasets/coco",
            split=f"val[:{num_images}]",
        )
    except Exception as e:
        pytest.skip(
            f"Failed to load COCO dataset from HuggingFace. "
            f"This may be due to network issues or API unavailability. Error: {e}"
        )

    batch: list[dict] = []
    for row in tqdm(dataset):
        buf = io.BytesIO()
        row["image"].save(buf, format="PNG")
        # Use the first object category if available, else "unknown".
        category = "unknown"
        if row.get("objects") and row["objects"].get("category"):
            cats = row["objects"]["category"]
            if cats:
                category = str(cats[0])
        batch.append({"image": buf.getvalue(), "category": category})

        if len(batch) >= frag_size:
            yield pa.RecordBatch.from_pylist(batch)
            batch = []

    if batch:
        yield pa.RecordBatch.from_pylist(batch)


# ============================================================================
# E2E test-specific fixtures
# ============================================================================


@pytest.fixture(scope="session")
def num_images(request) -> int:  # type: ignore[no-untyped-def]
    """Number of images to process in e2e tests."""
    return request.config.getoption("--num-images")


@pytest.fixture(scope="session")
def batch_size(request) -> int:  # type: ignore[no-untyped-def]
    """Batch size for backfill operations in e2e tests."""
    return request.config.getoption("--batch-size")


@pytest.fixture(scope="session")
def skip_gpu(request) -> bool:  # type: ignore[no-untyped-def]
    """Whether to skip GPU-based tests."""
    return request.config.getoption("--skip-gpu")


@pytest.fixture(scope="session")
def image_table(geneva_test_bucket: str, num_images: int) -> tuple:  # type: ignore[misc]
    """Session-scoped fixture that creates a shared table with COCO images.

    Returns (connection, table, table_name).
    """
    import geneva

    _LOG.info("Creating shared image table with %d images", num_images)

    conn = geneva.connect(geneva_test_bucket)
    table_name = f"av_curation_shared_{uuid.uuid4().hex}"

    first = True
    for batch in load_coco_images(num_images):
        if first:
            tbl = conn.create_table(table_name, batch, mode="overwrite")
            first = False
        else:
            tbl.add(batch)

    _LOG.info(
        "Shared table created: name='%s', rows=%d, schema=%s",
        table_name,
        len(tbl),
        tbl.schema,
    )

    os.environ["GENEVA_TABLE_NAME"] = table_name
    _LOG.info("Set GENEVA_TABLE_NAME=%s", table_name)

    global _MANIFESTS_UPLOADED  # noqa: PLW0603
    if not _MANIFESTS_UPLOADED:
        _upload_all_manifests(geneva_test_bucket)
        _MANIFESTS_UPLOADED = True
        tbl = conn.open_table(table_name)
        _LOG.info("Table schema after manifest uploads: %s", tbl.schema)

    return conn, tbl, table_name


@pytest.fixture
def gpu_cluster(
    image_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    csp: str,
    region: str,
    head_node_selector: dict,
    k8s_cluster_name: str,
    slug: str,
) -> str:
    """Define a GPU Ray cluster for model inference.

    Returns the cluster name for use with conn.context(cluster=name, manifest=name).
    """
    conn, _, _ = image_table
    cluster_name = "e2e-av-gpu-cluster"

    _LOG.info("Defining GPU cluster '%s'", cluster_name)

    gpu_worker_node_selector = (
        {"geneva.lancedb.com/ray-worker-gpu": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )

    builder = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .head_group(
            service_account=geneva_k8s_service_account,
            cpus=1,
            memory=_head_memory_for_csp(csp),
            image="rayproject/ray:2.54.0-py310",
            node_selector=head_node_selector,
        )
        .add_worker_group(
            KubeRayClusterBuilder.gpu_worker()
            .cpus(4)
            .memory("16Gi")
            .image("rayproject/ray:2.54.0-py310-gpu")
            .service_account(geneva_k8s_service_account)
            .node_selector(gpu_worker_node_selector)
            .build()
        )
    )

    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()

    conn.define_cluster(cluster_name, cluster)
    _LOG.info("Cluster '%s' defined", cluster_name)

    return cluster_name
