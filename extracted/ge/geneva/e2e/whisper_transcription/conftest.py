# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E fixtures for the Whisper transcription suite.

Shared fixtures live in e2e/conftest.py; this file provides suite-specific
options and helpers.
"""

import logging
import os
import subprocess
import uuid
from pathlib import Path

import pytest
from dataset import load_audio_samples
from pipeline import run_pipeline

from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder

_LOG = logging.getLogger(__name__)
_MANIFESTS_UPLOADED = False
DEFAULT_MANIFEST_NAME = "whisper-transcription-udfs-v1"
DEFAULT_HEAD_MEMORY = "3Gi"
AZURE_HEAD_MEMORY = "8Gi"


def _head_memory_for_csp(csp: str) -> str:
    if csp == "azure":
        return AZURE_HEAD_MEMORY
    return DEFAULT_HEAD_MEMORY


# ============================================================================
# Manifest upload helpers
# ============================================================================


def _upload_all_manifests(bucket_path: str) -> None:
    """
    Upload all suite manifests and add columns to the table.
    """
    _LOG.info("Uploading UDF manifests to %s", bucket_path)
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
        raise RuntimeError("Manifest upload failed for Whisper suite")

    _LOG.info("✓ All manifests uploaded")


# ============================================================================
# Pytest options
# ============================================================================


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--row-limit",
        action="store",
        type=int,
        default=256,
        help="Number of dataset rows to process",
    )
    parser.addoption(
        "--num-clips",
        action="store",
        type=int,
        default=5,
        help="Number of clips to process per audio file",
    )
    parser.addoption(
        "--checkpoint-size",
        "--batch-size",
        action="store",
        dest="checkpoint_size",
        type=int,
        default=10,
        help="Backfill checkpoint size",
    )
    parser.addoption(
        "--skip-gpu",
        action="store_true",
        default=False,
        help="Skip GPU tests and use CPU-only cluster",
    )


# ============================================================================
# E2E-specific fixtures
# ============================================================================


@pytest.fixture(scope="session")
def row_limit(request) -> int:
    return request.config.getoption("--row-limit")


@pytest.fixture(scope="session")
def num_clips(request) -> int:
    return request.config.getoption("--num-clips")


@pytest.fixture(scope="session")
def checkpoint_size(request) -> int:
    return request.config.getoption("checkpoint_size")


@pytest.fixture(scope="session")
def skip_gpu(request) -> bool:
    return request.config.getoption("--skip-gpu")


@pytest.fixture(scope="session")
def manifest_name() -> str:
    return DEFAULT_MANIFEST_NAME


@pytest.fixture(scope="session")
def audio_table(geneva_test_bucket: str, row_limit: int, num_clips: int) -> tuple:
    """
    Create a session-scoped table populated with audio clip metadata.

    Manifests are uploaded once per session and columns are added before tests
    run. Returns (connection, table, table_name).
    """
    import geneva

    metadata = load_audio_samples(row_limit, num_clips)
    if len(metadata) == 0:
        pytest.skip("No audio metadata available to build test table")

    conn = geneva.connect(geneva_test_bucket)
    table_name = f"whisper_transcription_{uuid.uuid4().hex}"

    tbl = conn.create_table(table_name, metadata, mode="overwrite")
    _LOG.info(
        "Created test table '%s' with %s rows and columns %s",
        table_name,
        len(tbl),
        tbl.schema.names,
    )

    os.environ["GENEVA_TABLE_NAME"] = table_name
    _LOG.info("Set GENEVA_TABLE_NAME=%s", table_name)

    global _MANIFESTS_UPLOADED
    if not _MANIFESTS_UPLOADED:
        _upload_all_manifests(geneva_test_bucket)
        _MANIFESTS_UPLOADED = True
        tbl = conn.open_table(table_name)
        _LOG.info("Schema after manifest upload: %s", tbl.schema.names)

    return conn, tbl, table_name


@pytest.fixture(scope="session")
def whisper_cluster(
    audio_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    csp: str,
    skip_gpu: bool,
) -> str:
    """
    Define a Ray cluster suitable for Whisper transcription workloads.

    Uses a GPU worker unless --skip-gpu is provided.
    """
    conn, _, _ = audio_table
    cluster_name = "e2e-whisper-transcription-cluster"

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
    )

    if skip_gpu:
        builder = builder.add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .cpus(4)
            .memory("8Gi")
            .image("rayproject/ray:2.54.0-py310")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .build()
        )
    else:
        # GPU Worker Group (temporarily disabling due to resourcing issues)
        # gpu_worker_node_selector = (
        #     {"geneva.lancedb.com/ray-worker-gpu": "true"}
        #     if csp == "aws"
        #     else {"_PLACEHOLDER": "true"}
        # )
        # builder = builder.add_worker_group(
        #     KubeRayClusterBuilder.gpu_worker()
        #     .cpus(4)
        #     .memory("16Gi")
        #     .image("rayproject/ray:2.54.0-py310")
        #     .service_account(geneva_k8s_service_account)
        #     .node_selector(gpu_worker_node_selector)
        #     .build()
        # )
        #
        builder = builder.add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .cpus(4)
            .memory("12Gi")
            .image("rayproject/ray:2.54.0-py310")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .replicas(6)
            .min_replicas(6)
            .max_replicas(6)
            .build()
        )

    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()
    conn.define_cluster(cluster_name, cluster)
    _LOG.info("Defined cluster '%s'", cluster_name)
    return cluster_name


@pytest.fixture(scope="session")
def chunk_table(
    audio_table: tuple,
    whisper_cluster: str,
    checkpoint_size: int,
    manifest_name: str,
) -> tuple:
    """Run the two-stage pipeline and return the chunk-level table."""
    conn, tbl, table_name = audio_table

    _LOG.info(
        "Running Whisper pipeline for table %s (rows=%s)",
        table_name,
        len(tbl),
    )

    chunk_tbl, chunk_table_name = run_pipeline(
        tbl, conn, whisper_cluster, manifest_name, checkpoint_size
    )

    return conn, chunk_tbl, chunk_table_name
