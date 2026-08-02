# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E fixtures for the document embedding suite.

This file relies on shared fixtures from e2e/conftest.py and mirrors the
structure used in other e2e suites.
"""

import contextlib
import logging
import os
import subprocess
import uuid
from pathlib import Path

import pytest
from dataset import SOURCE_METADATA_PATH, load_document_metadata

from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder
from geneva.cluster.mgr import WorkerGroupConfig

_LOG = logging.getLogger(__name__)
_MANIFESTS_UPLOADED = False
DEFAULT_MANIFEST_NAME = "document-embedding-udfs-v1"
DEFAULT_HEAD_MEMORY = "3Gi"
AZURE_HEAD_MEMORY = "8Gi"


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
        raise RuntimeError("Manifest upload failed for Document Embedding suite")

    _LOG.info("✓ All manifests uploaded")


# ============================================================================
# Pytest options
# ============================================================================


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--num-docs",
        action="store",
        type=int,
        default=20,
        help="Number of documents to process",
    )
    parser.addoption(
        "--batch-size",
        action="store",
        type=int,
        default=4,
        help="Backfill batch size",
    )


# ============================================================================
# E2E-specific fixtures
# ============================================================================


@pytest.fixture(scope="session")
def num_docs(request) -> int:
    return request.config.getoption("--num-docs")


@pytest.fixture(scope="session")
def batch_size(request) -> int:
    return request.config.getoption("--batch-size")


@pytest.fixture(scope="session")
def manifest_name() -> str:
    return DEFAULT_MANIFEST_NAME


def _head_memory_for_csp(csp: str) -> str:
    if csp == "azure":
        return AZURE_HEAD_MEMORY
    return DEFAULT_HEAD_MEMORY


@pytest.fixture(scope="session")
def document_table(geneva_test_bucket: str, num_docs: int) -> tuple:
    """
    Create a session-scoped table populated with document metadata.

    Manifests are uploaded once per session and columns are added before tests
    run. Returns (connection, table, table_name).
    """
    import geneva

    metadata = load_document_metadata(num_docs, SOURCE_METADATA_PATH)
    if len(metadata) == 0:
        pytest.skip("No document metadata available to build test table")

    conn = geneva.connect(geneva_test_bucket)
    table_name = f"document_embedding_{uuid.uuid4().hex}"

    # Force schema refresh if schema changed between runs
    with contextlib.suppress(Exception):
        conn._db.drop_table("geneva_clusters")

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


@pytest.fixture
def standard_cluster(
    document_table: tuple,
    geneva_k8s_service_account: str,
    csp: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
) -> str:
    """
    Define a small CPU Ray cluster suitable for the document embedding pipeline.
    """
    conn, _, _ = document_table
    cluster_name = "e2e-document-embedding-cluster"

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
            .cpus(4)
            .memory("8Gi")
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
    _LOG.info("Defined cluster '%s'", cluster_name)
    return cluster_name


@pytest.fixture
def benchmark_cluster(
    document_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    csp: str,
    region: str,
    head_node_selector: dict,
) -> str:
    """
    Cluster matching ray_data_main.py benchmark expectations: 8 GPU workers,
    worker node selector geneva.lancedb.com/ray-worker-cpu.
    """
    conn, _, _ = document_table
    cluster_name = "e2e-document-embedding-benchmark-cluster"

    worker_selector = {"geneva.lancedb.com/ray-worker-gpu": "true"}
    worker_cfg = WorkerGroupConfig(
        service_account=geneva_k8s_service_account,
        num_cpus=4,
        memory="16Gi",
        image="rayproject/ray:2.54.0-py310",
        num_gpus=1,
        node_selector=worker_selector,
        labels={},
        tolerations=[],
        k8s_spec_override={"replicas": 8, "min_replicas": 8, "max_replicas": 8},
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
            .image("rayproject/ray:2.54.0-py310")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_selector)
            .build()
        )
    )

    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()
    cluster.kuberay.worker_groups = [worker_cfg]

    conn.define_cluster(cluster_name, cluster)
    _LOG.info("Defined benchmark cluster '%s'", cluster_name)
    return cluster_name
