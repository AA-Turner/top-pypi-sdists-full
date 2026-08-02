# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Integration tests for bulk load column on a real Ray cluster.

These tests exercise table.load_columns() against a real KubeRay cluster
with cloud storage, verifying the full distributed pipeline:
SourceIndex build → BulkLoadMapTask dispatch → checkpoint → commit.
"""

import logging
import tempfile
import uuid
from contextlib import AbstractContextManager
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from lance.file import LanceFileSession

import geneva
from geneva.db import Connection
from integ_tests.utils import safe_drop_table

_LOG = logging.getLogger(__name__)


def _split_parent_uri(uri: str) -> tuple[str, str]:
    normalized = uri.rstrip("/")
    parent, sep, name = normalized.rpartition("/")
    if sep:
        return parent, name
    return ".", normalized


def _write_source_parquet(table: pa.Table, uri: str) -> None:
    """Write a PyArrow table to Parquet at a cloud URI.

    Write locally first, then upload through LanceFileSession so tests exercise
    the same storage path Geneva uses for namespace-aware artifacts.
    """
    base_uri, remote_name = _split_parent_uri(uri)
    with tempfile.TemporaryDirectory() as temp_dir:
        local_path = Path(temp_dir) / remote_name
        pq.write_table(table, local_path)
        LanceFileSession(base_uri).upload_file(local_path, remote_name)


@pytest.fixture(scope="module")
def bulk_load_context(
    geneva_test_bucket: str,
    session_cluster: str,
    session_manifest: str,
    session_db: Connection,
) -> AbstractContextManager:
    """Module-scoped Ray cluster context for bulk_load integ tests.

    The shared ``session_context`` fixture from conftest.py is fragile
    when bulk_load tests run before test_cluster_startup tests in the
    same shard:

    1. ``session_context`` (session-scoped) enters ``db.context()`` the
       first time a bulk_load test runs, connecting a Ray Client to the
       K8s cluster.
    2. test_cluster_startup tests later use ``with ray_cluster(...)``
       independently. ``init_ray()`` force-cleans Ray on entry (treating
       the still-active session_context client as "stale state from a
       prior session") and force-cleans again on exit. The local Ray
       Client connection used by session_context is destroyed.
    3. The next test that depends on session_context — notably
       ``test_ray_init_kwargs_env_var_on_worker`` — finds Ray
       uninitialized, auto-inits a local Ray, and the env_vars set via
       runtime_env are no longer present. The assertion fails with
       ``'' == 'geneva_worker_env_var_value'``.

    Using a *module*-scoped context here keeps the Ray Client lifecycle
    for bulk_load tests fully contained within this file: enter once for
    the first bulk_load test, exit cleanly after the last one. Tests in
    other files then get a fresh ``session_context`` entry, matching
    the behavior on a branch where bulk_load tests don't exist.
    """
    with session_db.context(
        manifest=session_manifest,
        cluster=session_cluster,
        log_to_driver=True,
    ) as ctx:
        yield ctx


@pytest.mark.timeout(900)
def test_bulk_load_columns_remote_smoke(
    geneva_test_bucket: str,
    bulk_load_context: AbstractContextManager,
) -> None:
    """Full remote bulk-load round trip with cloud storage and multiple fragments.

    The detailed carry, partial-match, multi-column, multi-fragment, and
    incremental semantics are covered by local Ray/unit tests. This integ test
    keeps one representative distributed job so CI still exercises the cloud
    Parquet source, SourceIndex build, map tasks, checkpointing, and commit path
    on a real KubeRay cluster.
    """
    db = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    source_path = f"{geneva_test_bucket}/{table_name}_source.parquet"

    table = db.create_table(
        table_name,
        pa.table(
            {
                "pk": pa.array(range(20)),
                "name": pa.array([f"row_{i}" for i in range(20)]),
            }
        ),
    )
    for start in range(20, 100, 20):
        table.add(
            pa.table(
                {
                    "pk": pa.array(range(start, start + 20)),
                    "name": pa.array([f"row_{i}" for i in range(start, start + 20)]),
                }
            )
        )

    try:
        even_pks = list(range(0, 100, 2))
        source_table = pa.table(
            {
                "pk": pa.array(even_pks),
                "feat_a": pa.array([pk * 10 for pk in even_pks]),
                "feat_b": pa.array([float(pk) / 10 for pk in even_pks]),
            }
        )
        _write_source_parquet(source_table, source_path)

        job_id = table.load_columns(
            source=source_path,
            pk="pk",
            columns=["feat_a", "feat_b"],
            source_format="parquet",
            concurrency=4,
        )
        assert job_id is not None

        # Verify
        result = table.to_arrow().sort_by("pk")
        assert result.num_rows == 100
        feat_a = result.column("feat_a").to_pylist()
        feat_b = result.column("feat_b").to_pylist()
        names = result.column("name").to_pylist()
        for i in range(100):
            assert names[i] == f"row_{i}"
            if i % 2 == 0:
                assert feat_a[i] == i * 10, f"pk={i} should have source value"
                assert feat_b[i] == float(i) / 10, f"pk={i} should have source value"
            else:
                assert feat_a[i] is None, f"pk={i} should be NULL (no source match)"
                assert feat_b[i] is None, f"pk={i} should be NULL (no source match)"
    finally:
        safe_drop_table(db, table_name)
