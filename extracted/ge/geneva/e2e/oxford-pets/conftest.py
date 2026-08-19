# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E test-specific fixtures for Oxford Pets suite.

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

# Flag to track if manifests have been uploaded
_MANIFESTS_UPLOADED = False
DEFAULT_HEAD_MEMORY = "3Gi"
AZURE_HEAD_MEMORY = "8Gi"


def _head_memory_for_csp(csp: str) -> str:
    if csp == "azure":
        return AZURE_HEAD_MEMORY
    return DEFAULT_HEAD_MEMORY


def _upload_all_manifests(bucket_path: str) -> None:
    """
    Upload suite manifests and add columns to the table.

    ``OXFORD_PETS_UPLOAD_PROFILES`` (comma-separated, default all) limits the
    profiles to upload so runs that exercise a single driver skip the other
    profiles' dependency syncs.
    """
    import subprocess

    _LOG.info("Uploading UDF manifests and adding columns...")
    suite_dir = Path(__file__).parent
    cmd = ["uv", "run", "python", "upload_manifests.py", "--bucket", bucket_path]
    profiles = os.environ.get("OXFORD_PETS_UPLOAD_PROFILES", "").strip()
    if profiles:
        cmd.extend(["--profile", profiles])
    result = subprocess.run(
        cmd,
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
        raise RuntimeError("Manifest upload failed for Oxford Pets suite")

    _LOG.info("All manifests uploaded and columns added")


# ============================================================================
# E2E test-specific pytest options
# ============================================================================


def pytest_addoption(parser) -> None:
    """Add e2e-specific command-line options."""
    parser.addoption(
        "--num-images",
        action="store",
        type=int,
        default=500,
        help="Number of images to process from Oxford pets dataset",
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
        help="Skip GPU-based tests (captions, GPU embeddings)",
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


def load_oxford_pets_images(
    num_images: int = 500, frag_size: int = 25
) -> ImageBatchGenerator:
    """
    Load images from the Oxford-IIIT Pet dataset.

    Args:
        num_images: Number of images to load from the dataset
        frag_size: Number of images per fragment

    Yields:
        PyArrow RecordBatch with columns: image (bytes), label (string)

    Raises:
        pytest.skip: If dataset cannot be loaded due to network or API errors
    """
    import io

    import pyarrow as pa
    from datasets import load_dataset

    from geneva.tqdm import tqdm

    _LOG.info(f"Loading {num_images} images from Oxford pets dataset")

    try:
        # there are 3680 images.  If num_images > 3680, it will just load all
        dataset = load_dataset("timm/oxford-iiit-pet", split=f"train[:{num_images}]")
    except Exception as e:
        pytest.skip(
            f"Failed to load Oxford pets dataset from HuggingFace. "
            f"This may be due to network issues or API unavailability. Error: {e}"
        )

    batch = []
    for row in tqdm(dataset):
        buf = io.BytesIO()
        row["image"].save(buf, format="png")
        batch.append(
            {
                "image": buf.getvalue(),
                "label": row["label"],
                "image_id": row["image_id"],
            }
        )

        if len(batch) >= frag_size:
            yield pa.RecordBatch.from_pylist(batch)
            batch = []

    if batch:
        yield pa.RecordBatch.from_pylist(batch)


# ============================================================================
# E2E test-specific fixtures
# ============================================================================


@pytest.fixture(scope="session")
def num_images(request) -> int:
    """Number of images to process in e2e tests."""
    return request.config.getoption("--num-images")


@pytest.fixture(scope="session")
def batch_size(request) -> int:
    """Batch size for backfill operations in e2e tests."""
    return request.config.getoption("--batch-size")


@pytest.fixture(scope="session")
def skip_gpu(request) -> bool:
    """Whether to skip GPU-based tests."""
    return request.config.getoption("--skip-gpu")


@pytest.fixture(scope="session")
def oxford_pets_table(geneva_test_bucket: str, num_images: int) -> tuple:  # type: ignore[misc]
    """
    Session-scoped fixture that creates a shared table with Oxford pets images.

    This table is created once per test session and reused across all e2e tests,
    avoiding repeated dataset downloads.

    Also sets GENEVA_TABLE_NAME environment variable for upload scripts.

    Returns:
        tuple: (connection, table, table_name)
    """
    import geneva

    _LOG.info(f"Creating shared Oxford pets table with {num_images} images")

    conn = geneva.connect(geneva_test_bucket)
    table_name = f"oxford_pets_shared_{uuid.uuid4().hex}"

    # Load images and create table (only happens once per session)
    first = True
    for batch in load_oxford_pets_images(num_images):
        if first:
            tbl = conn.create_table(table_name, batch, mode="overwrite")
            first = False
        else:
            tbl.add(batch)

    _LOG.info(
        f"Shared table created: name='{table_name}', rows={len(tbl)}, "
        f"schema={tbl.schema}. This will be reused across all e2e tests."
    )

    # Export table name as environment variable for upload scripts
    os.environ["GENEVA_TABLE_NAME"] = table_name
    _LOG.info(f"Set GENEVA_TABLE_NAME={table_name}")

    # Upload manifests and add columns (once per session)
    global _MANIFESTS_UPLOADED
    if not _MANIFESTS_UPLOADED:
        _upload_all_manifests(geneva_test_bucket)
        _MANIFESTS_UPLOADED = True

        # Refresh table to pick up newly added columns
        tbl = conn.open_table(table_name)
        _LOG.info(f"Table schema after manifest uploads: {tbl.schema}")

    return conn, tbl, table_name


@pytest.fixture
def standard_cluster(
    oxford_pets_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    csp: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_cluster_name: str,
    slug: str,
) -> str:
    """
    Define a standard Ray cluster for e2e tests.

    Returns the cluster name for use with conn.context(cluster=name, manifest=name).
    """
    conn, _, _ = oxford_pets_table
    cluster_name = "e2e-standard-cluster"

    _LOG.info(f"Defining standard cluster '{cluster_name}'")

    # Build cluster using fluent API
    # Pin to ray 2.54.0 to match live cluster environments
    # TODO: When live clusters upgrade, update this version
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

    # Add AWS config if needed
    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()

    conn.define_cluster(cluster_name, cluster)
    _LOG.info(f"Cluster '{cluster_name}' defined")

    return cluster_name


@pytest.fixture
def gpu_cluster(
    oxford_pets_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    csp: str,
    region: str,
    head_node_selector: dict,
    k8s_cluster_name: str,
    slug: str,
) -> str:
    """
    Define a GPU Ray cluster for caption and embedding generation.

    Returns the cluster name for use with conn.context(cluster=name, manifest=name).
    """
    conn, _, _ = oxford_pets_table
    cluster_name = "e2e-gpu-cluster"

    _LOG.info(f"Defining GPU cluster '{cluster_name}'")

    # GPU worker node selector
    gpu_worker_node_selector = (
        {"geneva.lancedb.com/ray-worker-gpu": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )

    # Build cluster using fluent API
    # Pin to ray 2.54.0 to match live cluster environments
    # TODO: When live clusters upgrade, update this version
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

    # Add AWS config if needed
    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()

    conn.define_cluster(cluster_name, cluster)
    _LOG.info(f"Cluster '{cluster_name}' defined")

    return cluster_name
