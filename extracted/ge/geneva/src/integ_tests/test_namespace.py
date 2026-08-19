# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import uuid
from collections.abc import Generator, Iterator
from typing import Any

import pyarrow as pa
import pytest

import geneva
from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder, default_image
from geneva.manifest import GenevaManifest
from geneva.runners.ray.raycluster import ExitMode
from geneva.table import Table
from geneva.utils import dt_now_utc
from integ_tests.utils import (
    installed_distribution_requirement,
    ray_get_with_retry,
    safe_drop_table,
)

_LOG = logging.getLogger(__name__)


@geneva.udf(data_type=pa.int64(), num_cpus=1, version=uuid.uuid4().hex)
def plus_one(a: int) -> int:
    return a + 1


# Output schema for UDTF integration test
UDTF_OUTPUT_SCHEMA = pa.schema(
    [
        pa.field("id", pa.int64()),
        pa.field("doubled", pa.float64()),
    ]
)


@geneva.udtf(output_schema=UDTF_OUTPUT_SCHEMA, input_columns=["id", "value"])
def double_values_udtf(source) -> Iterator[pa.RecordBatch]:
    tbl = source.to_arrow()
    yield pa.RecordBatch.from_pydict(
        {
            "id": tbl.column("id").to_pylist(),
            "doubled": [v * 2 for v in tbl.column("value").to_pylist()],
        }
    )


@geneva.udf(data_type=pa.float64(), version=uuid.uuid4().hex)
def triple_value_udf(value: float) -> float:
    return value * 3


SIZE = 128


def _dir_namespace_props(
    geneva_test_bucket: str,
    vend_input_storage_options: bool = False,
) -> dict[str, str]:
    props = {"root": geneva_test_bucket}
    if vend_input_storage_options:
        props["vend_input_storage_options"] = "true"
        props["vend_input_storage_options_refresh_interval_millis"] = "3600000"
    return props


@pytest.mark.timeout(900)
@pytest.mark.parametrize(
    "vend_input_storage_options",
    [True, False],
    ids=["vend_storage_options", "use_default_credentials"],
)
def test_dir_namespace_system_tables_and_child_table(
    geneva_test_bucket: str,
    vend_input_storage_options: bool,
) -> None:
    """Verify dir namespace setup without paying for a remote Ray cluster."""
    from lance_namespace import CreateNamespaceRequest

    system_ns_name = f"system-{uuid.uuid4().hex[:8]}"
    namespace = [f"workspace-{uuid.uuid4().hex[:8]}"]
    table_name = f"test-table-{uuid.uuid4().hex[:8]}"
    db = geneva.connect(
        namespace_client_impl="dir",
        namespace_client_properties=_dir_namespace_props(
            geneva_test_bucket,
            vend_input_storage_options,
        ),
        system_namespace=[system_ns_name],
    )

    try:
        assert db.system_namespace == [system_ns_name]

        ns = db.namespace_client()
        assert ns is not None, "This test requires a namespace connection"
        ns.create_namespace(CreateNamespaceRequest(id=namespace))

        _ = db._history
        _ = db.list_manifests()
        _ = db.list_clusters()

        system_tables = []
        page_token = None
        while True:
            response = db.list_tables(
                namespace_path=[system_ns_name], page_token=page_token
            )
            system_tables.extend(response.tables)
            if not response.page_token:
                break
            page_token = response.page_token

        assert {
            "geneva_manifests",
            "geneva_cluster_definitions",
            "geneva_jobs",
        }.issubset(set(system_tables))

        data = pa.table({"a": pa.array(range(4))})
        tbl = db.create_table(table_name, data, namespace_path=namespace)
        assert tbl.to_arrow()["a"].to_pylist() == [0, 1, 2, 3]
    finally:
        safe_drop_table(db, table_name, namespace_path=namespace)
        db.close()


@pytest.mark.timeout(1500)
def test_backfill_with_dir_namespace_child(
    slug: str | None,
    geneva_test_bucket: str,
    manifest: str | None,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    geneva_k8s_service_account: str,
) -> None:
    """Test backfill with directory namespace and child namespace on S3.

    The non-remote namespace test above covers both credential vending modes.
    This remote backfill path keeps the vend-input-storage-options mode, which
    is the important cluster-side namespace credential integration.
    """
    from lance_namespace import CreateNamespaceRequest

    from geneva.runners.ray.pipeline import get_imported

    # Setup directory namespace with custom system_namespace
    system_ns_name = f"system-{uuid.uuid4().hex[:8]}"
    ns_client_props = _dir_namespace_props(
        geneva_test_bucket,
        vend_input_storage_options=True,
    )
    _LOG.info(f"Testing with vend_input_storage_options=True, props={ns_client_props}")
    db = geneva.connect(
        namespace_client_impl="dir",
        namespace_client_properties=ns_client_props,
        system_namespace=[system_ns_name],
    )

    cluster_name = "namespace-backfill"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"
    manifest_name = f"test-manifest-{slug}"

    # Create unique names to avoid conflicts
    namespace_name = f"workspace-{uuid.uuid4().hex[:8]}"
    table_name = f"test-table-{uuid.uuid4().hex[:8]}"
    namespace = [namespace_name]

    try:
        if manifest:
            # saved manifest provided via --manifest arg
            manifest_name = manifest
        else:
            db.define_manifest(
                manifest_name,
                GenevaManifest.create_pip(manifest_name)
                # pylance must be explicitly installed for the worker
                # to download the manifest when using namespaces
                .upload_site_packages()
                .add_pip(installed_distribution_requirement("lancedb"))
                .add_pip(installed_distribution_requirement("pylance"))
                .add_pip("pyarrow>=16.0")
                .build(),
            )

        img = default_image(arm=False)
        db.define_cluster(
            cluster_name,
            (
                GenevaCluster.create_kuberay(cluster_name)
                .namespace(k8s_namespace)
                .config_method(k8s_config_method)
                .aws_config(region=region, role_name="geneva-client-role")
                .head_group(
                    image=img,
                    service_account=geneva_k8s_service_account,
                    node_selector=head_node_selector,
                )
                .add_worker_group(
                    KubeRayClusterBuilder.cpu_worker()
                    .image(img)
                    .service_account(geneva_k8s_service_account)
                    .node_selector(worker_node_selector)
                    .build()
                )
                .build()
            ),
        )

        # Verify system_namespace is set correctly
        assert db.system_namespace == [system_ns_name], (
            f"Expected system_namespace={[system_ns_name]}, got {db.system_namespace}"
        )
        _LOG.info(f"Verified system_namespace: {db.system_namespace}")

        # Create child namespace (system namespace already created by connect())
        ns = db.namespace_client()
        assert ns is not None, "This test requires a namespace connection"
        ns.create_namespace(CreateNamespaceRequest(id=namespace))
        _LOG.info(f"Created namespace: {namespace}")

        # Trigger system table creation by accessing managers
        # This will create tables in the system namespace
        _ = db._history  # Creates geneva_jobs table
        manifests = db.list_manifests()  # Creates geneva_manifests table
        clusters = db.list_clusters()  # Creates geneva_cluster_definitions table
        _LOG.info(
            f"Accessed system tables: {len(manifests)} manifests, "
            f"{len(clusters)} clusters"
        )

        # Verify system tables exist in the correct namespace
        # list_tables is paginated, collect all tables
        system_tables = []
        page_token = None
        while True:
            response = db.list_tables(
                namespace_path=[system_ns_name], page_token=page_token
            )
            system_tables.extend(response.tables)
            if not response.page_token:
                break
            page_token = response.page_token
        _LOG.info(f"System tables in namespace {[system_ns_name]}: {system_tables}")

        # Check that expected system tables are present
        expected_tables = {
            "geneva_manifests",
            "geneva_cluster_definitions",
            "geneva_jobs",
        }
        for table in expected_tables:
            assert table in system_tables, (
                f"Expected system table '{table}' not found in namespace "
                f"{[system_ns_name]}"
            )
        _LOG.info(f"Verified all system tables exist in {[system_ns_name]}")

        # Create table in the child namespace (for actual data)
        schema = pa.schema(
            [
                pa.field("a", pa.int64()),
            ]
        )
        db.create_table(table_name, schema=schema, namespace_path=namespace)
        tbl = Table(db, table_name, namespace=namespace)
        _LOG.info(f"Created table: {table_name} in namespace {namespace}")

        # Add data
        data = pa.table({"a": pa.array(range(SIZE))})
        tbl.add(data)
        _LOG.info(f"Added {SIZE} rows to table")

        # Add UDF column and backfill with remote cluster
        with db.context(
            cluster=cluster_name,
            manifest=manifest_name,
            log_to_driver=True,
        ):
            _LOG.info("Manifest packages:")
            pkgs = ray_get_with_retry(get_imported.remote())
            for pkg, ver in sorted(pkgs.items()):
                _LOG.info(f"{pkg}=={ver}")

            tbl.add_columns(
                {"b": plus_one},
                batch_size=32,
                concurrency=2,
            )
            tbl.backfill("b")

        # Verify results
        tbl.checkout_latest()
        result = tbl.to_arrow()
        assert result["a"].to_pylist() == list(range(SIZE))
        assert result["b"].to_pylist() == list(range(1, SIZE + 1))
        _LOG.info("Backfill verification passed")

    finally:
        safe_drop_table(db, table_name, namespace_path=namespace)
        _LOG.info(f"Dropped table: {table_name}")
        db.close()


@pytest.mark.timeout(1500)
def test_udtf_matview_with_dir_namespace(
    geneva_test_bucket: str,
    ns_kuberay_cluster_ready: tuple[str, str, GenevaCluster, GenevaManifest],
) -> None:
    """Test UDTF materialized view refresh with directory namespace.

    This test verifies that namespace info is correctly stored in MV metadata
    and used during refresh to re-establish the source table connection.
    """
    from lance_namespace import CreateNamespaceRequest

    from geneva.runners.ray.pipeline import get_imported

    cluster_name, manifest_name, cluster_def, manifest_def = ns_kuberay_cluster_ready

    # Setup directory namespace
    system_ns_name = f"system-{uuid.uuid4().hex[:8]}"
    db = geneva.connect(
        namespace_client_impl="dir",
        namespace_client_properties={"root": geneva_test_bucket},
        system_namespace=[system_ns_name],
    )

    namespace_name = f"workspace-{uuid.uuid4().hex[:8]}"
    source_table_name = f"source-{uuid.uuid4().hex[:8]}"
    mv_table_name = f"udtf-mv-{uuid.uuid4().hex[:8]}"
    namespace = [namespace_name]

    try:
        db.define_manifest(manifest_name, manifest_def)
        db.define_cluster(cluster_name, cluster_def)

        # Create child namespace
        ns = db.namespace_client()
        assert ns is not None, "This test requires a namespace connection"
        ns.create_namespace(CreateNamespaceRequest(id=namespace))
        _LOG.info(f"Created namespace: {namespace}")

        # Create source table
        data = pa.table(
            {
                "id": pa.array(list(range(SIZE))),
                "value": pa.array([float(i * 10) for i in range(SIZE)]),
            }
        )
        source_table = db.create_table(
            source_table_name, data, namespace_path=namespace
        )
        _LOG.info(f"Created source table: {source_table_name} in namespace {namespace}")

        # Create UDTF view using module-level UDTF
        query = source_table.search(None).select(["id", "value"])
        mv = db.create_udtf_view(mv_table_name, query, double_values_udtf)
        _LOG.info(f"Created UDTF view: {mv_table_name}")

        # Refresh with remote cluster
        with db.context(
            cluster=cluster_name,
            manifest=manifest_name,
            on_exit=ExitMode.RETAIN,
            log_to_driver=True,
        ):
            _LOG.info("Manifest packages:")
            pkgs = ray_get_with_retry(get_imported.remote())
            for pkg, ver in sorted(pkgs.items()):
                _LOG.info(f"{pkg}=={ver}")

            mv.refresh(concurrency=2)

        # Verify results
        mv.checkout_latest()
        result = mv.to_arrow()
        assert result.num_rows == SIZE, f"Expected {SIZE} rows, got {result.num_rows}"

        expected_doubled = [float(i * 10 * 2) for i in range(SIZE)]
        actual_doubled = sorted(result.column("doubled").to_pylist())
        assert actual_doubled == sorted(expected_doubled), (
            f"Doubled values mismatch: {actual_doubled[:5]}..."
        )
        _LOG.info("UDTF MV refresh verification passed")

    finally:
        safe_drop_table(db, mv_table_name)
        _LOG.info(f"Dropped view: {mv_table_name}")
        safe_drop_table(db, source_table_name, namespace_path=namespace)
        _LOG.info(f"Dropped source table: {source_table_name}")
        db.close()


@pytest.fixture(scope="session")
def ns_kuberay_cluster_ready(
    slug: str | None,
    geneva_test_bucket: str,
    manifest: str | None,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    geneva_k8s_service_account: str,
) -> Generator[tuple[str, str, GenevaCluster, GenevaManifest], Any, None]:
    """Provision a KubeRay cluster for namespace tests at session scope.

    Creates a temporary connection to define the cluster/manifest and
    provisions the K8s resources with ExitMode.RETAIN so the cluster stays
    up after the context exits.  Individual tests enter their own short-lived
    contexts, which are fast because the cluster already exists.

    Yields (cluster_name, manifest_name, cluster_def, manifest_def) so tests
    can re-define them on their own connections.
    """
    db = geneva.connect(
        namespace_client_impl="dir",
        namespace_client_properties={"root": geneva_test_bucket},
    )

    cluster_name = "namespace-matview"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"
    manifest_name = f"test-manifest-mv-{slug}"

    manifest_def = GenevaManifest.create_pip(manifest_name).upload_site_packages()
    manifest_def = (
        manifest_def.add_pip(installed_distribution_requirement("lancedb"))
        .add_pip(installed_distribution_requirement("pylance"))
        .add_pip("pyarrow>=16.0")
        .build()
    )
    if manifest:
        manifest_name = manifest
    else:
        db.define_manifest(manifest_name, manifest_def)

    img = default_image(arm=False)
    cluster_def = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region, role_name="geneva-client-role")
        .head_group(
            image=img,
            service_account=geneva_k8s_service_account,
            node_selector=head_node_selector,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .image(img)
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .build()
        )
        .build()
    )
    db.define_cluster(cluster_name, cluster_def)

    # Provision the cluster — this is the slow part
    with db.context(
        cluster=cluster_name,
        manifest=manifest_name,
        on_exit=ExitMode.RETAIN,
        log_to_driver=True,
    ):
        pass

    yield cluster_name, manifest_name, cluster_def, manifest_def

    # Clean up the K8s RayCluster resource
    with db.context(
        cluster=cluster_name,
        manifest=manifest_name,
        on_exit=ExitMode.DELETE,
    ):
        pass
    db.close()


@pytest.mark.timeout(1800)
def test_matview_with_dir_namespace(
    geneva_test_bucket: str,
    ns_kuberay_cluster_ready: tuple[str, str, GenevaCluster, GenevaManifest],
) -> None:
    """Test standard materialized view refresh with directory namespace.

    This test verifies that namespace info is correctly stored in MV metadata
    and used during refresh for standard materialized views with UDFs.
    """
    from lance_namespace import CreateNamespaceRequest

    from geneva.runners.ray.pipeline import get_imported

    cluster_name, manifest_name, cluster_def, manifest_def = ns_kuberay_cluster_ready

    # Setup directory namespace
    system_ns_name = f"system-{uuid.uuid4().hex[:8]}"
    db = geneva.connect(
        namespace_client_impl="dir",
        namespace_client_properties={"root": geneva_test_bucket},
        system_namespace=[system_ns_name],
    )

    namespace_name = f"workspace-{uuid.uuid4().hex[:8]}"
    source_table_name = f"source-{uuid.uuid4().hex[:8]}"
    mv_table_name = f"mv-{uuid.uuid4().hex[:8]}"
    namespace = [namespace_name]

    try:
        db.define_manifest(manifest_name, manifest_def)
        db.define_cluster(cluster_name, cluster_def)

        # Create child namespace
        ns = db.namespace_client()
        assert ns is not None, "This test requires a namespace connection"
        ns.create_namespace(CreateNamespaceRequest(id=namespace))
        _LOG.info(f"Created namespace: {namespace}")

        # Create source table with stable row IDs
        data = pa.table(
            {
                "id": pa.array(list(range(SIZE))),
                "value": pa.array([float(i * 10) for i in range(SIZE)]),
            }
        )
        source_table = db.create_table(
            source_table_name,
            data,
            namespace=namespace,
            storage_options={"new_table_enable_stable_row_ids": "true"},
        )
        _LOG.info(f"Created source table: {source_table_name} in namespace {namespace}")

        # Create materialized view using module-level UDF
        mv = (
            source_table.search(None)
            .select({"id": "id", "tripled": triple_value_udf})
            .create_materialized_view(conn=db, view_name=mv_table_name)
        )
        _LOG.info(f"Created materialized view: {mv_table_name}")

        # Refresh with remote cluster — fast because cluster already exists.
        # Use RETAIN so we don't delete the session-scoped shared cluster.
        with db.context(
            cluster=cluster_name,
            manifest=manifest_name,
            on_exit=ExitMode.RETAIN,
            log_to_driver=True,
        ):
            _LOG.info("Manifest packages:")
            pkgs = ray_get_with_retry(get_imported.remote())
            for pkg, ver in sorted(pkgs.items()):
                _LOG.info(f"{pkg}=={ver}")

            mv.refresh(concurrency=2)

        # Verify results
        mv.checkout_latest()
        result = mv.to_arrow()
        assert result.num_rows == SIZE, f"Expected {SIZE} rows, got {result.num_rows}"

        expected_tripled = [float(i * 10 * 3) for i in range(SIZE)]
        actual_tripled = sorted(result.column("tripled").to_pylist())
        assert actual_tripled == sorted(expected_tripled), (
            f"Tripled values mismatch: {actual_tripled[:5]}..."
        )
        _LOG.info("Materialized view refresh verification passed")

    finally:
        safe_drop_table(db, mv_table_name)
        _LOG.info(f"Dropped view: {mv_table_name}")
        safe_drop_table(db, source_table_name, namespace_path=namespace)
        _LOG.info(f"Dropped source table: {source_table_name}")
        db.close()
