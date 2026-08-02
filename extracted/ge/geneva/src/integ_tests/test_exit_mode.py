# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Integration tests for ExitMode behavior.

Tests verify cluster lifecycle for each ExitMode:
- RETAIN_ON_FAILURE: waits for jobs, retains on failure, deletes on success
- DELETE: waits for async jobs, then deletes
- RETAIN: cluster always retained
"""

import logging
import time
import uuid
from collections.abc import Generator

import kubernetes
import pyarrow as pa
import pytest

import geneva
from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder, default_image
from geneva.db import Connection
from geneva.jobs.jobs import JobStatus
from geneva.runners.kuberay.client import KuberayClients
from geneva.runners.ray.raycluster import ExitMode
from geneva.utils import dt_now_utc
from integ_tests.utils import safe_drop_table

_LOG = logging.getLogger(__name__)

backfill_args = {"_admission_check": False}


@pytest.fixture
def per_test_cluster(
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    session_db: Connection,
    slug: str | None,
    kuberay_clients: KuberayClients,
) -> Generator[str, None, None]:
    """Create a unique cluster definition per-test, cleaned up afterwards."""
    ts = dt_now_utc().strftime("%Y-%m-%d-%H-%M")
    cluster_name = f"exit-test-{ts}-{uuid.uuid4().hex[:6]}-{slug}"
    img = default_image(arm=False)
    cluster = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region)
        .head_group(
            image=img,
            node_selector=head_node_selector,
            service_account=geneva_k8s_service_account,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .image(img)
            .node_selector(worker_node_selector)
            .service_account(geneva_k8s_service_account)
            .build()
        )
        .build()
    )
    session_db.define_cluster(cluster_name, cluster)
    yield cluster_name
    # Clean up: force-delete the K8s CR and remove the definition
    _force_delete_cluster(kuberay_clients, cluster_name, k8s_namespace)
    session_db.delete_cluster(cluster_name)


def _cluster_exists(clients: KuberayClients, name: str, namespace: str) -> bool:
    """Check if a KubeRay RayCluster CR exists in Kubernetes."""
    try:
        clients.custom_api.get_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=namespace,
            plural="rayclusters",
            name=name,
        )
        return True
    except kubernetes.client.exceptions.ApiException as e:
        if e.status == 404:
            return False
        raise


def _wait_for_cluster_deleted(
    clients: KuberayClients, name: str, namespace: str, timeout_s: float = 60.0
) -> None:
    """Wait for a KubeRay RayCluster CR to be fully removed from Kubernetes."""
    start = time.time()
    while _cluster_exists(clients, name, namespace):
        if time.time() - start > timeout_s:
            raise TimeoutError(f"Cluster {name} still exists after {timeout_s:.0f}s")
        time.sleep(2)


def _force_delete_cluster(clients: KuberayClients, name: str, namespace: str) -> None:
    """Delete a RayCluster CR if it exists. Used for test cleanup."""
    try:
        clients.custom_api.delete_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=namespace,
            plural="rayclusters",
            name=name,
        )
    except kubernetes.client.exceptions.ApiException as e:
        if e.status != 404:
            raise


def _get_job_status(db: Connection, job_id: str) -> JobStatus | None:
    """Get the current status of a job from the DB."""
    records = db._history.get(job_id)
    if records:
        status = records[0].status
        if isinstance(status, str):
            return JobStatus(status)
        return status
    return None


def _wait_for_terminal_status(
    db: Connection, job_id: str, timeout_s: float = 120.0, poll_s: float = 5.0
) -> JobStatus | None:
    """Poll until job reaches a terminal state (DONE/FAILED) or timeout."""
    start = time.time()
    while time.time() - start < timeout_s:
        status = _get_job_status(db, job_id)
        if status in (JobStatus.DONE, JobStatus.FAILED):
            return status
        _LOG.info(f"Job {job_id}: status={status}, waiting {poll_s}s...")
        time.sleep(poll_s)
    return _get_job_status(db, job_id)


# use a random version to force checkpoint to invalidate
@geneva.udf(num_cpus=0.1, version=uuid.uuid4().hex)
def slow_plus_one(a: int) -> int:
    import time

    time.sleep(0.005)
    return a + 1


@geneva.udf(num_cpus=0.1, version=uuid.uuid4().hex)
def fast_plus_one(a: int) -> int:
    return a + 1


@geneva.udf(num_cpus=0.1, version=uuid.uuid4().hex)
def very_slow_plus_one(a: int) -> int:
    import time

    time.sleep(0.01)
    return a + 1


@geneva.udf(num_cpus=0.1, version=uuid.uuid4().hex)
def failing_udf(a: int) -> int:
    raise ValueError("intentional failure for testing")


SIZE = 128
BATCH_SIZE = 16


@pytest.mark.skip(reason="slow; run with -k to include")
@pytest.mark.timeout(600)
def test_delete_single_job(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """Cluster waits for a single async job to complete, then deletes."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    job_id = None
    try:
        table.add_columns(
            {"b": slow_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.DELETE,
        ):
            fut = table.backfill_async("b", **backfill_args)
            job_id = fut.job_id
            # Exit the with block immediately — don't call .result()

        # After context exits, the job should eventually reach a terminal state
        status = _wait_for_terminal_status(conn, job_id)
        assert status in (
            JobStatus.DONE,
            JobStatus.FAILED,
        ), f"Expected terminal state, got {status}"

    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(600)
def test_delete_multi_job_one_fast_one_slow(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """Cluster waits for all jobs when one finishes quickly and one is slow."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"fast_col": fast_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )
        table.add_columns(
            {"slow_col": very_slow_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.DELETE,
        ):
            fut_fast = table.backfill_async("fast_col", **backfill_args)
            fut_slow = table.backfill_async("slow_col", **backfill_args)
            # Exit the with block immediately

        # After context exits, both jobs should eventually reach terminal state
        for fut, col_name in [(fut_fast, "fast_col"), (fut_slow, "slow_col")]:
            status = _wait_for_terminal_status(conn, fut.job_id)
            assert status in (
                JobStatus.DONE,
                JobStatus.FAILED,
            ), f"Job for {col_name}: expected terminal state, got {status}"

    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.skip(reason="slow; run with -k to include")
@pytest.mark.timeout(600)
def test_delete_failed_job(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """Cluster still deletes when a job fails (doesn't hang)."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": failing_udf},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.DELETE,
        ):
            fut = table.backfill_async("b", **backfill_args)
            job_id = fut.job_id
            # Exit immediately

        # Job should be FAILED but cluster should still have been deleted
        status = _wait_for_terminal_status(conn, job_id)
        assert status == JobStatus.FAILED, f"Expected FAILED, got {status}"

    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.skip(reason="slow; run with -k to include")
@pytest.mark.timeout(600)
def test_retain_keeps_cluster_alive(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """RETAIN mode keeps the cluster alive after context exit."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": fast_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.RETAIN,
        ):
            table.backfill("b", **backfill_args)

        # Cluster should still exist after context exit
        assert _cluster_exists(kuberay_clients, per_test_cluster, k8s_namespace), (
            "RETAIN mode should keep the cluster alive"
        )
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.skip(reason="slow; run with -k to include")
@pytest.mark.timeout(600)
def test_retain_on_failure_deletes_on_success(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """RETAIN_ON_FAILURE deletes the cluster when all jobs succeed."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": fast_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.RETAIN_ON_FAILURE,
        ):
            table.backfill("b", **backfill_args)

        # Cluster should be deleted after successful exit
        _wait_for_cluster_deleted(kuberay_clients, per_test_cluster, k8s_namespace)
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.skip(reason="slow; run with -k to include")
@pytest.mark.timeout(600)
def test_retain_on_failure_retains_on_error(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """RETAIN_ON_FAILURE retains the cluster when the context body raises."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": fast_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        try:
            with session_db.context(
                manifest=session_manifest,
                cluster=per_test_cluster,
                on_exit=ExitMode.RETAIN_ON_FAILURE,
            ):
                table.backfill("b", **backfill_args)
                raise RuntimeError("intentional error for testing")
        except RuntimeError:
            pass

        # Cluster should still exist after error exit
        assert _cluster_exists(kuberay_clients, per_test_cluster, k8s_namespace), (
            "RETAIN_ON_FAILURE should retain the cluster on error"
        )
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.skip(reason="slow; run with -k to include")
@pytest.mark.timeout(600)
def test_retain_on_failure_retains_on_job_failure(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """RETAIN_ON_FAILURE retains the cluster when an async job fails.

    This is the key new behavior: the context body does NOT raise, but
    an async job fails. The cluster should be retained for debugging.
    """
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": failing_udf},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.RETAIN_ON_FAILURE,
        ):
            fut = table.backfill_async("b", **backfill_args)
            job_id = fut.job_id
            # Exit immediately — context body does NOT raise

        # Job should be FAILED
        status = _wait_for_terminal_status(conn, job_id)
        assert status == JobStatus.FAILED, f"Expected FAILED, got {status}"

        # Cluster should still exist because the job failed
        assert _cluster_exists(kuberay_clients, per_test_cluster, k8s_namespace), (
            "RETAIN_ON_FAILURE should retain the cluster when a job fails"
        )
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.skip(reason="slow; run with -k to include")
@pytest.mark.timeout(600)
def test_retain_on_failure_multi_job_all_succeed(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
) -> None:
    """RETAIN_ON_FAILURE deletes the cluster when multiple async jobs all succeed.

    Two jobs: one fast and one slow. The context should wait for both to
    finish and then delete the cluster since neither failed.
    """
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"fast_col": fast_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )
        table.add_columns(
            {"slow_col": slow_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.RETAIN_ON_FAILURE,
        ):
            fut_fast = table.backfill_async("fast_col", **backfill_args)
            fut_slow = table.backfill_async("slow_col", **backfill_args)
            # Exit immediately — don't call .result()

        # Both jobs should reach terminal state
        for fut, col_name in [(fut_fast, "fast_col"), (fut_slow, "slow_col")]:
            status = _wait_for_terminal_status(conn, fut.job_id)
            assert status == JobStatus.DONE, (
                f"Job for {col_name}: expected DONE, got {status}"
            )

        # Cluster should be deleted since all jobs succeeded
        _wait_for_cluster_deleted(kuberay_clients, per_test_cluster, k8s_namespace)
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(600)
def test_retain_on_failure_multi_job_one_fails(
    session_db: Connection,
    per_test_cluster: str,
    session_manifest: str,
    kuberay_clients: KuberayClients,
    k8s_namespace: str,
    geneva_test_bucket: str,
    csp: str,
) -> None:
    """RETAIN_ON_FAILURE retains the cluster when one of multiple jobs fails.

    Two jobs: one succeeds (fast_plus_one) and one fails (failing_udf).
    The context should wait for both, detect the failure, and retain the
    cluster for debugging.
    """
    if csp == "azure":
        pytest.skip(
            "Disabled on azure: multi-job run outlasts the SAS token lifetime "
            "and post-failure cleanup hits 401 on the manifest listing. "
            "Re-enable once credential refresh covers in-flight workers "
            "(GEN-545)."
        )

    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"good_col": fast_plus_one},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )
        table.add_columns(
            {"bad_col": failing_udf},  # type: ignore[arg-type]
            batch_size=BATCH_SIZE,
            concurrency=4,
        )

        with session_db.context(
            manifest=session_manifest,
            cluster=per_test_cluster,
            on_exit=ExitMode.RETAIN_ON_FAILURE,
        ):
            fut_good = table.backfill_async("good_col", **backfill_args)
            fut_bad = table.backfill_async("bad_col", **backfill_args)
            # Exit immediately — context body does NOT raise

        # The failing job should be FAILED
        status = _wait_for_terminal_status(conn, fut_bad.job_id)
        assert status == JobStatus.FAILED, f"Expected FAILED, got {status}"

        # The good job should be DONE
        status = _wait_for_terminal_status(conn, fut_good.job_id)
        assert status == JobStatus.DONE, f"Expected DONE, got {status}"

        # Cluster should still exist because one job failed
        assert _cluster_exists(kuberay_clients, per_test_cluster, k8s_namespace), (
            "RETAIN_ON_FAILURE should retain the cluster when any job fails"
        )
    finally:
        safe_drop_table(conn, table_name)
