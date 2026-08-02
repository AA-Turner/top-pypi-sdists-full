# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E fixtures for the large image embedding suite.

This suite mirrors e2e/document_embedding:
  - lightweight test drivers
  - heavy ML deps isolated in udfs/vit_image (uploaded via manifest)
"""

import logging
import os
import subprocess
import uuid
from pathlib import Path

import kubernetes
import pytest
from dataset import write_large_image_table

from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder

_LOG = logging.getLogger(__name__)
_MANIFESTS_UPLOADED = False
DEFAULT_MANIFEST_NAME = "large-image-embedding-udfs-v1"
DEFAULT_HEAD_MEMORY = "3Gi"
AZURE_HEAD_MEMORY = "8Gi"


def _head_memory_for_csp(csp: str) -> str:
    if csp == "azure":
        return AZURE_HEAD_MEMORY
    return DEFAULT_HEAD_MEMORY


def _upload_all_manifests(bucket_path: str) -> None:
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
        raise RuntimeError("Manifest upload failed for Large Image Embedding suite")


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--num-images",
        action="store",
        type=int,
        default=20,
        help="Number of images to process",
    )
    parser.addoption(
        "--batch-size",
        action="store",
        type=int,
        default=4,
        help="Backfill batch size",
    )
    parser.addoption(
        "--write-concurrency",
        action="store",
        type=int,
        default=16,
        help="Concurrent add workers when building the source table",
    )


@pytest.fixture(scope="session")
def num_images(request) -> int:
    return request.config.getoption("--num-images")


@pytest.fixture(scope="session")
def batch_size(request) -> int:
    return request.config.getoption("--batch-size")


@pytest.fixture(scope="session")
def write_concurrency(request) -> int:
    return request.config.getoption("--write-concurrency")


@pytest.fixture(scope="session")
def manifest_name() -> str:
    return DEFAULT_MANIFEST_NAME


@pytest.fixture(scope="session")
def image_table(
    geneva_test_bucket: str,
    num_images: int,
    write_concurrency: int,
) -> tuple:
    table_name = f"large_image_embedding_{uuid.uuid4().hex}"

    conn, tbl, chunk_count = write_large_image_table(
        geneva_test_bucket,
        table_name,
        num_images=num_images,
        write_concurrency=write_concurrency,
    )

    _LOG.info(
        "Created test table '%s' with %s rows, %s write chunks, and columns %s",
        table_name,
        len(tbl),
        chunk_count,
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
    image_table: tuple,
    geneva_k8s_service_account: str,
    csp: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
) -> str:
    conn, _, _ = image_table
    cluster_name = "e2e-large-image-embedding-cluster"

    try:
        kubernetes.config.list_kube_config_contexts()
    except Exception:
        pytest.skip("Kubernetes config not available; skipping cluster-backed tests")

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
