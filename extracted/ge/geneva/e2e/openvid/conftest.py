# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E test-specific fixtures for OpenVid suite.

Shared fixtures live in e2e/conftest.py; this file provides suite-specific
options and helpers.
"""

import logging
import os
import subprocess
import uuid
from pathlib import Path
from typing import Generator

import lance
import pyarrow as pa
import pytest
import ray

from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder
from geneva.runners.ray._mgr import _force_ray_cleanup

SYNC_CMD = ["uv", "sync", "--index-strategy", "unsafe-best-match"]
E2E_PYTEST_INI = Path(__file__).resolve().parents[1] / "pytest.ini"

_LOG = logging.getLogger(__name__)

# Flag to track if manifests have been uploaded
_MANIFESTS_UPLOADED = False

# ============================================================================
# HuggingFace Lance dataset (CSP-agnostic data source)
# ============================================================================

HF_OPENVID_LANCE = "hf://datasets/lance-format/openvid-lance/data/train.lance"

# Columns to read from the HF Lance dataset for test tables
HF_COLUMNS = ["video_path", "caption", "frame", "fps", "seconds"]


def run_test_in_udf_env(
    udf_name: str,
    test_path: str,
    pytest_args: list[str] | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """
    Run a test file in a specific UDF's Python environment.

    This is useful when tests need dependencies that differ from the main
    test environment (e.g., Ray 2.54.0).

    Args:
        udf_name: Name of UDF package (e.g., "embedding_vjepa2")
        test_path: Path to test file relative to e2e/openvid/
                  (e.g., "test_drivers/test_video_embeddings.py")
        pytest_args: Additional pytest arguments (e.g., ["-v", "-s"])
        env: Additional environment variables to pass to the subprocess

    Returns:
        CompletedProcess with returncode, stdout, stderr

    Raises:
        RuntimeError: If dependency sync fails
    """
    udfs_dir = Path(__file__).parent / "udfs"
    udf_dir = udfs_dir / udf_name

    if not udf_dir.exists():
        raise ValueError(f"UDF directory not found: {udf_dir}")

    _LOG.info(f"Running test in '{udf_name}' UDF environment...")

    # Step 1: Sync dependencies to populate .venv with UDF dependencies
    _LOG.info(f"Syncing dependencies for '{udf_name}'...")
    sync_result = subprocess.run(
        SYNC_CMD,
        cwd=str(udf_dir),
        capture_output=True,
        text=True,
    )
    if sync_result.returncode != 0:
        _LOG.error(f"Failed to sync dependencies for '{udf_name}':")
        if sync_result.stderr:
            for line in sync_result.stderr.splitlines():
                _LOG.error(f"  [{udf_name}] {line}")
        raise RuntimeError(f"Dependency sync failed for '{udf_name}'")

    # Step 2: Run test from UDF's .venv
    test_file = (Path(__file__).resolve().parent / test_path).resolve()
    cmd = [
        "uv",
        "run",
        "python",
        "-m",
        "pytest",
        "-c",
        str(E2E_PYTEST_INI),
        str(test_file),
    ]
    if pytest_args:
        cmd.extend(pytest_args)

    _LOG.info(f"Running: {' '.join(cmd)}")
    _LOG.info(f"  Working directory: {udf_dir}")

    # Disable uv runtime env for Ray compatibility
    subprocess_env = os.environ.copy()
    subprocess_env["RAY_ENABLE_UV_RUN_RUNTIME_ENV"] = "0"
    # Merge custom env variables if provided
    if env:
        subprocess_env.update(env)

    # Stream output in real-time instead of buffering
    # This is important for long-running tests (GPU backfills) so we can see progress
    _LOG.info(f"  [{udf_name}] Starting test (output will stream in real-time)...")

    process = subprocess.Popen(
        cmd,
        cwd=str(udf_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout
        text=True,
        env=subprocess_env,
        bufsize=1,  # Line-buffered
    )

    # Stream output line by line in real-time AND capture for return value
    captured_lines = []
    for line in iter(process.stdout.readline, ""):
        if line:
            _LOG.info(f"  [{udf_name}] {line.rstrip()}")
            captured_lines.append(line)

    process.stdout.close()
    returncode = process.wait()

    # Create a CompletedProcess-like object with captured output
    captured_output = "".join(captured_lines)
    result = subprocess.CompletedProcess(
        args=cmd,
        returncode=returncode,
        stdout=captured_output,
        stderr="",  # Merged into stdout
    )

    return result


def assert_subprocess_passed(
    result: subprocess.CompletedProcess,
    test_name: str,
) -> None:
    """Fail with subprocess output inlined into the pytest failure message."""
    if result.returncode != 0:
        tail = (
            "\n".join(result.stdout.splitlines()[-100:])
            if result.stdout
            else "(no output)"
        )
        pytest.fail(
            f"{test_name} failed with return code {result.returncode}"
            f"\n\n=== Last 100 lines of output ===\n{tail}"
        )


def _upload_all_manifests(bucket_path: str) -> None:
    """
    Upload all suite manifests and add columns to the table.
    """
    _LOG.info("Uploading UDF manifests and adding columns...")
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
        raise RuntimeError("Manifest upload failed for OpenVid suite")

    _LOG.info("All manifests uploaded and columns added")


# ============================================================================
# E2E test-specific pytest options
# ============================================================================


def pytest_addoption(parser) -> None:
    """Add e2e-specific command-line options."""
    parser.addoption(
        "--num-videos",
        action="store",
        type=int,
        default=20,
        help="Number of videos to process from OpenVid dataset",
    )
    parser.addoption(
        "--batch-size",
        action="store",
        type=int,
        default=4,
        help="Batch size for backfill operations",
    )
    parser.addoption(
        "--skip-gpu",
        action="store_true",
        default=False,
        help="Skip GPU-based tests (video embeddings, captions)",
    )


# ============================================================================
# Dataset Loading Utilities
# ============================================================================


def load_openvid_from_hf(num_videos: int) -> pa.Table:
    """
    Load a sample of OpenVid data from the HuggingFace Lance dataset.

    Reads directly from the lance-format/openvid-lance dataset on HuggingFace,
    which contains ~938k rows with video metadata, captions, and embeddings.

    Adds a derived ``video`` column (basename of ``video_path``) for backward
    compatibility with UDFs that expect a short filename.

    Args:
        num_videos: Number of rows to sample.

    Returns:
        PyArrow Table with columns: video_path, video, caption, frame, fps,
        seconds.
    """
    _LOG.info(
        "Reading %d rows from HF Lance dataset: %s",
        num_videos,
        HF_OPENVID_LANCE,
    )

    hf_ds = lance.dataset(HF_OPENVID_LANCE)
    sample = hf_ds.to_table(columns=HF_COLUMNS, limit=num_videos)

    _LOG.info("Read %d rows, columns: %s", sample.num_rows, sample.column_names)

    # Derive a short 'video' column (basename of video_path) for backward
    # compat with UDFs that expect a filename.
    paths = sample.column("video_path").to_pandas()
    basenames = paths.str.rsplit("/", n=1).str[-1]
    sample = sample.append_column("video", pa.array(basenames))

    return sample


# ============================================================================
# E2E test-specific fixtures
# ============================================================================


@pytest.fixture(scope="session")
def num_videos(request) -> int:
    """Number of videos to process in e2e tests."""
    return request.config.getoption("--num-videos")


@pytest.fixture(scope="session")
def batch_size(request) -> int:
    """Batch size for backfill operations in e2e tests."""
    return request.config.getoption("--batch-size")


@pytest.fixture(scope="session")
def skip_gpu(request) -> bool:
    """Whether to skip GPU-based tests."""
    return request.config.getoption("--skip-gpu")


@pytest.fixture(scope="session")
def openvid_table(geneva_test_bucket: str, num_videos: int) -> tuple:  # type: ignore[misc]
    """
    Session-scoped fixture that creates a test table from HuggingFace Lance data.

    Reads a sample from the lance-format/openvid-lance HuggingFace dataset
    and writes it into the CSP-specific test bucket for isolated testing.

    Also sets GENEVA_TABLE_NAME environment variable for upload scripts.

    Returns:
        tuple: (connection, table, table_name)
    """
    import geneva

    _LOG.info(
        "Creating test table with %d videos from HuggingFace Lance dataset",
        num_videos,
    )

    # Read sample from HuggingFace Lance dataset
    sample = load_openvid_from_hf(num_videos)

    # Connect to test bucket
    conn = geneva.connect(geneva_test_bucket)
    table_name = f"openvid_test_{uuid.uuid4().hex}"

    # Drop geneva_clusters table to force schema recreation (in case schema changed)
    try:
        conn._db.drop_table("geneva_clusters")  # type: ignore[attr-defined]
        _LOG.info("Dropped existing geneva_clusters table to refresh schema")
    except Exception:
        pass  # Table might not exist yet

    tbl = conn.create_table(
        table_name,
        sample,
        mode="overwrite",
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )

    _LOG.info(
        "Test table created: name='%s', rows=%d, schema=%s",
        table_name,
        len(tbl),
        tbl.schema.names,
    )

    # Export table name as environment variable for upload scripts
    os.environ["GENEVA_TABLE_NAME"] = table_name
    _LOG.info("Set GENEVA_TABLE_NAME=%s", table_name)

    # Upload manifests to test bucket (once per session)
    global _MANIFESTS_UPLOADED
    if not _MANIFESTS_UPLOADED:
        _upload_all_manifests(geneva_test_bucket)
        _MANIFESTS_UPLOADED = True

        # Refresh table to pick up newly added columns
        tbl = conn.open_table(table_name)
        _LOG.info("Table schema after manifest uploads: %s", tbl.schema.names)

    return conn, tbl, table_name


@pytest.fixture(autouse=True)
def ensure_ray_shutdown_between_tests() -> Generator[None, None, None]:
    """Ensure Ray is properly shut down between e2e tests.

    Without this, stale Ray client state (cached addresses, connection
    pools) from a previous test can interfere with connecting to a
    freshly created cluster, even after the old cluster has been deleted.
    """
    _force_ray_cleanup()
    yield
    _force_ray_cleanup()


@pytest.fixture
def standard_cluster(
    openvid_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
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
    conn, _, _ = openvid_table
    cluster_name = "e2e-openvid-standard-cluster"

    _LOG.info(f"Defining standard cluster '{cluster_name}'")

    # Build cluster using fluent API
    # Pin to ray 2.54.0 to match live cluster environments
    builder = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .head_group(
            service_account=geneva_k8s_service_account,
            cpus=1,
            memory="14Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector=head_node_selector,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .cpus(2)
            .memory("14Gi")
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
    openvid_table: tuple,
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
    Define a GPU Ray cluster for video embedding and processing.

    Returns the cluster name for use with conn.context(cluster=name, manifest=name).
    """
    conn, _, _ = openvid_table
    cluster_name = "e2e-openvid-gpu-cluster"

    _LOG.info(f"Defining GPU cluster '{cluster_name}'")

    # GPU worker node selector
    gpu_worker_node_selector = (
        {"geneva.lancedb.com/ray-worker-gpu": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )

    # Build cluster using fluent API
    # Pin to ray 2.54.0 to match live cluster environments
    builder = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .head_group(
            service_account=geneva_k8s_service_account,
            cpus=1,
            memory="14Gi",
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


@pytest.fixture
def ray_254_gpu_cluster(
    openvid_table: tuple,
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
    Define a GPU Ray cluster using ray:2.54.0.

    This cluster uses rayproject/ray:2.54.0 base images. All ML deps
    (pytorch, torchcodec, transformers, ffmpeg, etc.) are provided by
    the manifest's conda env when using conn.context(cluster=name, manifest=name).

    Suitable for video embedding tasks (V-JEPA2) and other ML workloads.

    Returns the cluster name for use with conn.context(cluster=name, manifest=name).
    """
    conn, _, _ = openvid_table
    cluster_name = "e2e-openvid-ray-254-gpu-cluster"

    _LOG.info(f"Defining ray:2.54.0 GPU cluster '{cluster_name}'")

    # GPU worker node selector
    gpu_worker_node_selector = (
        {"geneva.lancedb.com/ray-worker-gpu": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )

    # Build cluster using fluent API; conda env comes from manifest
    # ray-ml images are deprecated (removed after 2.50.x), so we use base
    # rayproject/ray images and rely on the manifest conda env for ML deps.
    builder = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .head_group(
            service_account=geneva_k8s_service_account,
            cpus=1,
            memory="14Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector=head_node_selector,
        )
        .add_worker_group(
            # 120G is near the node memory limit; do not increase without checking capacity
            KubeRayClusterBuilder.cpu_worker()
            .cpus(30)
            .memory("120G")
            .image("rayproject/ray:2.54.0-py310")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .build()
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
    return cluster_name


@pytest.fixture
def ray_254_cpu_cluster(
    openvid_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_cluster_name: str,
    slug: str,
) -> str:
    """
    Define a CPU-only Ray cluster using ray:2.54.0.

    Similar to ray_254_gpu_cluster but without GPU workers. All ML deps
    (pytorch, torchcodec, Pillow, ffmpeg, etc.) are provided by the manifest's
    conda env when using conn.context(cluster=name, manifest=name).

    Suitable for CPU-based video processing (frame extraction with torchcodec).

    Returns the cluster name for use with conn.context(cluster=name, manifest=name).
    """
    conn, _, _ = openvid_table
    cluster_name = "e2e-openvid-ray-254-cpu-cluster"

    _LOG.info(f"Defining ray:2.54.0 CPU cluster '{cluster_name}'")

    # Build cluster - CPU only; conda env comes from manifest
    # ray-ml images are deprecated (removed after 2.50.x), so we use base
    # rayproject/ray images and rely on the manifest conda env for ML deps.
    builder = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .head_group(
            service_account=geneva_k8s_service_account,
            cpus=1,
            memory="8Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector=head_node_selector,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .cpus(8)
            .memory("32Gi")
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
    return cluster_name
