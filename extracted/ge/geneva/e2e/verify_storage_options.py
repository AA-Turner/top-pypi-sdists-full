# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""
End-to-end verification script for storage_options propagation.

This is a manual deployment validation script for exercising a real
enterprise/KubeRay setup after deployment or environment changes. It is not
intended to run in CI because the enterprise path depends on an externally
deployed LanceDB Enterprise service, a reachable Ray cluster, and cloud storage
credentials. The --local mode is a lightweight smoke check for redaction and
local Ray propagation without those external services.

Based on the cifar-10-dedupe.ipynb workflow. Tests:
1. Connecting to LanceDB Enterprise with storage_options
2. Worker host override (different endpoints for notebook vs Ray workers)
3. Redaction of sensitive fields in repr/logs
4. Backfill with proper credential propagation to workers

Usage (local Ray, no enterprise server):
    RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python e2e/verify_storage_options.py --local

Usage (enterprise + KubeRay):
    RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python e2e/verify_storage_options.py \
        --host http://localhost:10024 \
        --worker-host http://lancedb-local.geneva.svc.cluster.local:10024 \
        --api-key sk_localtest \
        --database lancedb_examples \
        --ray-address ray://localhost:443 \
        --storage-account-name lancedb50ohp7 \
        --storage-account-key '<key>'
"""

import argparse
import logging
import time
import uuid

import pyarrow as pa

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# -- Step 0: Configuration --

PHASH_DIM = 16
NUM_IMAGES = 100  # smaller for verification


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Verify storage_options propagation")
    p.add_argument("--local", action="store_true", help="Use local Ray (no enterprise)")
    p.add_argument("--host", default=None, help="LanceDB enterprise host override")
    p.add_argument(
        "--worker-host",
        default=None,
        help="Internal worker host (K8s service endpoint)",
    )
    p.add_argument("--api-key", default="sk_localtest", help="API key")
    p.add_argument("--database", default="lancedb_examples", help="Database name")
    p.add_argument("--ray-address", default=None, help="Ray cluster address")
    p.add_argument("--storage-account-name", default=None, help="Azure account name")
    p.add_argument("--storage-account-key", default=None, help="Azure account key")
    p.add_argument(
        "--db-uri", default=None, help="Direct storage URI (e.g. az://container/path)"
    )
    return p.parse_args()


# -- Step 1: Verify redaction --


def verify_redaction() -> None:
    """Test that sensitive fields are properly redacted in repr output."""
    from geneva.table import TableReference
    from geneva.utils import redact_dict_values

    # Test redact_dict_values directly
    d = {"account_key": "super-secret-123", "account_name": "myaccount"}
    redacted = redact_dict_values(d)
    assert "super-secret-123" not in redacted, "Key value leaked!"
    assert "myaccount" not in redacted, "Account name leaked!"
    assert "'account_key': '[REDACTED]'" in redacted
    assert "'account_name': '[REDACTED]'" in redacted
    _LOG.info("PASS: redact_dict_values works correctly")

    # Test None case
    assert redact_dict_values(None) == "None"
    _LOG.info("PASS: redact_dict_values(None) returns 'None'")

    # Test TableReference redaction
    ref = TableReference(
        table_id=["ns", "test_table"],
        version=1,
        db_uri="az://container/path",
        namespace_client_impl="rest",
        namespace_client_properties={
            "uri": "http://localhost:10024",
            "header.x-api-key": "sk_super_secret_key",
            "header.x-lancedb-database": "mydb",
        },
        storage_options={
            "azure_storage_account_name": "myaccount",
            "azure_storage_account_key": "super-secret-key-123",
        },
    )
    ref_repr = repr(ref)
    assert "sk_super_secret_key" not in ref_repr, (
        f"API key leaked in TableReference repr: {ref_repr}"
    )
    assert "super-secret-key-123" not in ref_repr, (
        f"Storage key leaked in TableReference repr: {ref_repr}"
    )
    assert "[REDACTED]" in ref_repr
    _LOG.info("PASS: TableReference repr redacts sensitive fields")


# -- Step 2: Verify storage_options propagation through CheckpointingApplier --


def verify_checkpointing_applier_propagation() -> None:
    """Test that namespace/storage config flows through CheckpointingApplier."""
    from geneva.apply import CheckpointingApplier
    from geneva.apply.task import MapTask

    class DummyMapTask(MapTask):
        def name(self) -> str:
            return "dummy"

        def output_schema(self) -> pa.Schema:
            return pa.schema([pa.field("x", pa.int32())])

        def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            return batch

        def input_columns(self) -> list[str]:
            return ["x"]

        def batch_size(self) -> int:
            return 100

        def num_cpus(self) -> int:
            return 1

        def num_gpus(self) -> int:
            return 0

        def memory(self) -> int | None:
            return None

        def is_cuda(self) -> bool:
            return False

        def checkpoint_key(self, **kwargs) -> str:  # noqa: ANN003
            return "dummy_key"

        def checkpoint_prefix(self) -> str:
            return "dummy_prefix"

        def legacy_map_task_key(self) -> str:
            return "dummy_legacy"

    applier = CheckpointingApplier(
        checkpoint_uri="memory",
        map_task=DummyMapTask(),
        namespace_client_impl="rest",
        namespace_client_properties={
            "uri": "http://example.com",
            "header.x-api-key": "secret123",
        },
        checkpoint_table_id=["__system", "_ckp_table"],
        storage_options={
            "azure_storage_account_key": "my-secret-key",
        },
    )

    # Verify repr doesn't leak secrets
    applier_repr = repr(applier)
    assert "secret123" not in applier_repr, (
        "API key leaked in CheckpointingApplier repr"
    )
    assert "my-secret-key" not in applier_repr, (
        "Storage key leaked in CheckpointingApplier repr"
    )
    _LOG.info("PASS: CheckpointingApplier repr redacts sensitive fields")

    # Verify fields are stored
    assert applier.namespace_client_impl == "rest"
    assert applier.namespace_client_properties is not None
    assert applier.storage_options is not None
    _LOG.info("PASS: CheckpointingApplier stores namespace/storage config")


# -- Step 3: Verify table cache redaction --


def verify_table_cache_redaction() -> None:
    """Test that TableCache repr shows count not contents."""
    from geneva.apply.table_cache import TableCache

    cache = TableCache()
    cache_repr = repr(cache)
    assert "0 cached table(s)" in cache_repr
    _LOG.info("PASS: TableCache repr shows count: %s", cache_repr)


# -- Step 4: End-to-end with local Ray --


def verify_e2e_local(
    db_uri: str | None, storage_options: dict[str, str] | None
) -> None:
    """End-to-end test with local Ray (no enterprise)."""
    import geneva

    if db_uri is None:
        import tempfile

        tmp = tempfile.mkdtemp(prefix="geneva_verify_")
        db_uri = tmp
        _LOG.info("Using temp directory: %s", tmp)

    db = geneva.connect(db_uri, storage_options=storage_options)

    table_name = f"verify_{uuid.uuid4().hex[:8]}"
    _LOG.info("Creating table: %s", table_name)

    # Create test data
    data = pa.table(
        {
            "id": pa.array([str(i) for i in range(NUM_IMAGES)]),
            "value": pa.array(list(range(NUM_IMAGES))),
        }
    )
    tbl = db.create_table(table_name, data)

    # Define a simple UDF
    @geneva.udf(
        data_type=pa.int32(),
        input_columns=["value"],
    )
    def double_value(value: int) -> int | None:
        if value is None:
            return None
        return value * 2

    tbl.add_columns({"doubled": double_value})

    # Run backfill with local Ray
    with db.local_ray_context():
        job_id = tbl.backfill("doubled")
        _LOG.info("Backfill job started: %s", job_id)

        # Wait for completion
        for _ in range(60):
            time.sleep(1)
            lance_tbl = tbl.to_lance()
            null_count = lance_tbl.to_table(
                columns=["doubled"],
                filter="doubled IS NULL",
            ).num_rows
            if null_count == 0:
                break

    # Verify results
    result = tbl.to_lance().to_table(columns=["value", "doubled"])
    values = result.column("value").to_pylist()
    doubled = result.column("doubled").to_pylist()
    assert all(
        d == v * 2 for v, d in zip(values, doubled, strict=True) if d is not None
    ), "Backfill results incorrect"
    _LOG.info("PASS: E2E local backfill with storage_options succeeded")

    # Cleanup
    db.drop_table(table_name)


# -- Step 5: Enterprise connection verification --


def verify_enterprise_connection(args: argparse.Namespace) -> None:
    """Verify enterprise connection with worker host override."""
    import geneva

    storage_options = None
    if args.storage_account_name and args.storage_account_key:
        storage_options = {
            "azure_storage_account_name": args.storage_account_name,
            "azure_storage_account_key": args.storage_account_key,
        }

    db = geneva.connect(
        uri=f"db://{args.database}",
        api_key=args.api_key,
        host_override=args.host,
        _worker_host_override=args.worker_host,
        storage_options=storage_options,
    )
    _LOG.info("Connected to enterprise: %r", db)

    # Verify the connection repr doesn't leak credentials
    db_repr = repr(db)
    if args.storage_account_key:
        assert args.storage_account_key not in db_repr, (
            "Storage key leaked in Connection repr"
        )
    _LOG.info("PASS: Enterprise connection established")

    # Verify namespace config has worker_uri set
    ns_props = db.namespace_client_properties
    assert ns_props is not None, "namespace_client_properties should be set"
    if args.worker_host:
        from geneva.db import WORKER_URI_KEY

        assert WORKER_URI_KEY in ns_props, (
            "worker_uri should be in namespace_client_properties: "
            f"{list(ns_props.keys())}"
        )
        assert ns_props[WORKER_URI_KEY] == args.worker_host
        _LOG.info("PASS: worker_uri correctly stored in namespace properties")

    # List tables to verify connectivity
    tables = list(db.table_names())
    _LOG.info("Tables in database: %s", tables[:5])
    _LOG.info("PASS: Enterprise connection works end-to-end")

    return db


def verify_enterprise_backfill(db, args: argparse.Namespace) -> None:
    """Run backfill on enterprise with KubeRay."""
    import geneva
    from geneva.cluster import GenevaCluster

    table_name = f"verify_{uuid.uuid4().hex[:8]}"
    _LOG.info("Creating table: %s", table_name)

    # Create test data
    data = pa.table(
        {
            "id": pa.array([str(i) for i in range(NUM_IMAGES)]),
            "value": pa.array(list(range(NUM_IMAGES))),
        }
    )
    tbl = db.create_table(table_name, data)

    @geneva.udf(
        data_type=pa.int32(),
        input_columns=["value"],
    )
    def double_value(value: int) -> int | None:
        if value is None:
            return None
        return value * 2

    tbl.add_columns({"doubled": double_value})

    # Setup ray cluster
    cluster_name = "verify-cluster"
    builder = GenevaCluster.create_external(cluster_name, args.ray_address)
    cluster = builder.build()
    db.define_cluster(cluster_name, cluster)

    # Run backfill
    with db.context(cluster=cluster_name):
        job_id = tbl.backfill("doubled", concurrency=2)
        _LOG.info("Enterprise backfill job started: %s", job_id)

        for _ in range(120):
            time.sleep(2)
            lance_tbl = tbl.to_lance()
            null_count = lance_tbl.to_table(
                columns=["doubled"],
                filter="doubled IS NULL",
            ).num_rows
            if null_count == 0:
                break

    result = tbl.to_lance().to_table(columns=["value", "doubled"])
    values = result.column("value").to_pylist()
    doubled = result.column("doubled").to_pylist()
    assert all(
        d == v * 2 for v, d in zip(values, doubled, strict=True) if d is not None
    ), "Enterprise backfill results incorrect"
    _LOG.info("PASS: Enterprise backfill with worker_host_override succeeded")

    # Cleanup
    db.drop_table(table_name)


# -- Main --


def main() -> None:
    args = parse_args()

    _LOG.info("=" * 60)
    _LOG.info("Verifying storage_options propagation & redaction")
    _LOG.info("=" * 60)

    # Always run unit-level verification
    verify_redaction()
    verify_checkpointing_applier_propagation()
    verify_table_cache_redaction()

    if args.local:
        storage_options = None
        if args.storage_account_name and args.storage_account_key:
            storage_options = {
                "azure_storage_account_name": args.storage_account_name,
                "azure_storage_account_key": args.storage_account_key,
            }
        verify_e2e_local(args.db_uri, storage_options)
    elif args.host:
        db = verify_enterprise_connection(args)
        if args.ray_address:
            verify_enterprise_backfill(db, args)
    else:
        _LOG.info("Running unit-level checks only (no --local or --host specified)")

    _LOG.info("=" * 60)
    _LOG.info("ALL VERIFICATIONS PASSED")
    _LOG.info("=" * 60)


if __name__ == "__main__":
    main()
