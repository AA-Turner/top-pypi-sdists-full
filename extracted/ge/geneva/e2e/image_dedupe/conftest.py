# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Fixtures for the image-dedupe e2e suite."""

from __future__ import annotations

import logging
import os
import uuid
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import pyarrow as pa
import pytest

import geneva
from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder

if TYPE_CHECKING:
    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)

MANIFEST_NAME = "image-hash-udfs-v1"
DEFAULT_HEAD_MEMORY = "3Gi"
AZURE_HEAD_MEMORY = "8Gi"


def _head_memory_for_csp(csp: str) -> str:
    if csp == "azure":
        return AZURE_HEAD_MEMORY
    return DEFAULT_HEAD_MEMORY

# Flag to track if manifests have been uploaded
_MANIFESTS_UPLOADED = False


def _upload_all_manifests(bucket_path: str) -> None:
    """Upload all suite manifests."""
    import subprocess

    _LOG.info("Uploading image dedupe UDF manifests...")
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
        raise RuntimeError("Manifest upload failed for image dedupe suite")

    _LOG.info("All manifests uploaded")

ImageBatchGenerator = Generator[pa.RecordBatch, None, None]

# ---------------------------------------------------------------------------
# CIFAR-10 dataset loading for full-pipeline tests
# ---------------------------------------------------------------------------


def load_cifar10_images(
    num_images: int = 1000, frag_size: int = 50
) -> ImageBatchGenerator:
    """Load images from the CIFAR-10 dataset via HuggingFace.

    Args:
        num_images: Number of images to load from the dataset.
        frag_size: Number of images per record batch.

    Yields:
        PyArrow RecordBatch with columns: image_id (string),
        image_bytes (binary), label (int32).
    """
    import io

    from datasets import load_dataset

    _LOG.info("Loading %d images from CIFAR-10 dataset", num_images)

    try:
        dataset = load_dataset(
            "uoft-cs/cifar10", split=f"train[:{num_images}]"
        )
    except Exception as e:
        pytest.skip(
            f"Failed to load CIFAR-10 dataset from HuggingFace. "
            f"This may be due to network issues or API unavailability. "
            f"Error: {e}"
        )

    batch: list[dict] = []
    for i, row in enumerate(dataset):
        buf = io.BytesIO()
        row["img"].save(buf, format="PNG")
        batch.append(
            {
                "image_id": f"cifar_{i}",
                "image_bytes": buf.getvalue(),
                "label": row["label"],
            }
        )

        if len(batch) >= frag_size:
            yield pa.RecordBatch.from_pylist(batch)
            batch = []

    if batch:
        yield pa.RecordBatch.from_pylist(batch)


def make_compute_phash() -> UDF:
    """Create a batch UDF that computes pHash from image bytes."""

    @geneva.udf(data_type=pa.list_(pa.uint8(), 8))
    def compute_phash(image_bytes: pa.Array) -> pa.Array:
        import io

        import imagehash
        from PIL import Image

        results = []
        for raw in image_bytes.to_pylist():
            if raw is None:
                results.append(None)
                continue
            img = Image.open(io.BytesIO(raw))
            h = imagehash.phash(img)
            row_vals: list[int] = []
            for row in h.hash:
                byte_val = 0
                for bit in row:
                    byte_val = (byte_val << 1) | int(bit)
                row_vals.append(byte_val)
            results.append(row_vals)
        return pa.array(results, type=pa.list_(pa.uint8(), 8))

    return compute_phash


# Re-export so e2e test imports keep working via ``from conftest import ...``
from geneva.partitioning import create_ivf_flat_index  # noqa: F401


# ---------------------------------------------------------------------------
# Table fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def manifest_name(geneva_test_bucket: str) -> str:
    """Session-scoped fixture: upload manifests once and return manifest name."""
    global _MANIFESTS_UPLOADED
    if not _MANIFESTS_UPLOADED:
        _upload_all_manifests(geneva_test_bucket)
        _MANIFESTS_UPLOADED = True
    return MANIFEST_NAME


def pytest_addoption(parser) -> None:  # noqa: ANN001
    """Add e2e-specific command-line options."""
    parser.addoption(
        "--num-images",
        action="store",
        type=int,
        default=10000,
        help="Number of CIFAR-10 images to load for the full-pipeline e2e test",
    )


@pytest.fixture(scope="session")
def num_images(request) -> int:  # noqa: ANN001
    """Number of CIFAR-10 images to process in the full-pipeline test."""
    return request.config.getoption("--num-images")


@pytest.fixture(scope="session")
def image_source_table(
    geneva_test_bucket: str, num_images: int
) -> Generator[tuple, None, None]:
    """Session-scoped fixture: table with CIFAR-10 images for full pipeline.

    Yields (connection, table, table_name).  Drops the table on teardown.
    """
    conn = geneva.connect(geneva_test_bucket)
    table_name = f"image_dedupe_full_{uuid.uuid4().hex}"

    first = True
    tbl = None
    for batch in load_cifar10_images(num_images):
        if first:
            tbl = conn.create_table(table_name, batch)
            first = False
        else:
            tbl.add(batch)

    if tbl is None:
        pytest.fail("No CIFAR-10 images were loaded")

    _LOG.info(
        "Created image source table '%s' with %d CIFAR-10 rows",
        table_name,
        len(tbl),
    )

    yield conn, tbl, table_name

    _LOG.info("Dropping image source table '%s'", table_name)
    conn.drop_table(table_name)


# ---------------------------------------------------------------------------
# Cluster fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def standard_cluster(
    geneva_test_bucket: str,
    geneva_k8s_service_account: str,
    csp: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
) -> str:
    """Define a standard Ray cluster for the image-dedupe suite.

    Returns the cluster name for use with ``conn.context(cluster=...)``.
    """
    conn = geneva.connect(geneva_test_bucket)
    cluster_name = "e2e-image-dedupe-cluster"

    _LOG.info("Defining cluster '%s'", cluster_name)

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
            KubeRayClusterBuilder.cpu_worker()
            .cpus(2)
            .memory("4Gi")
            .image("rayproject/ray:2.54.0-py310")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .build()
        )
    )

    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()
    conn.define_cluster(cluster_name, cluster)
    _LOG.info("Cluster '%s' defined", cluster_name)

    return cluster_name
