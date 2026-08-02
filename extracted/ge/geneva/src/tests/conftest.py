# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import contextlib
import logging
import os
from collections.abc import Callable, Generator, Iterator
from datetime import timedelta
from pathlib import Path

# Cap Ray's GCS RPC retry/wait at process exit so end-of-session cleanup
# doesn't hang for 60s (the default) when the local GCS has already been
# torn down by an earlier ``local_ray_context``. Without this, CI runs
# end with ``Failed to connect to GCS within 60 seconds`` and exit 1
# *after* all pytest assertions have passed. Must be set before any
# ``ray`` import resolves the constant.
os.environ.setdefault("RAY_gcs_server_request_timeout_seconds", "5")

import lance  # noqa: E402
import pyarrow as pa  # noqa: E402
import pytest  # noqa: E402

import geneva  # noqa: E402
from geneva import connect  # noqa: E402
from geneva.apply.task import DEFAULT_CHECKPOINT_ROWS  # noqa: E402
from geneva.db import Connection  # noqa: E402
from geneva.table import Table  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@pytest.fixture(scope="session", autouse=True)
def _shutdown_ray_at_session_end() -> Iterator[None]:
    """Ensure Ray is fully torn down before the interpreter exits.

    Some test modules use ``local_ray_context`` which stops the local
    cluster on module teardown, but Ray's process-level atexit hooks
    can still try to reach a GCS that's already gone. Calling
    ``ray.shutdown()`` here (after every test runs) gives Ray a chance
    to drop those handles cleanly while GCS is still alive in the
    happy case, and is a no-op when the cluster is already down.
    """
    yield
    with contextlib.suppress(Exception):
        import ray

        if ray.is_initialized():
            ray.shutdown()


@pytest.fixture(autouse=True)
def stable_backfill_checkpoint_bounds(monkeypatch) -> None:
    """Force stable backfill checkpoint sizing for tests not about adaptive sizing."""
    orig_backfill = Table.backfill
    orig_backfill_async = Table.backfill_async

    def _backfill(self, *args, **kwargs) -> object:
        if "min_checkpoint_size" not in kwargs and "max_checkpoint_size" not in kwargs:
            checkpoint_size = kwargs.get("checkpoint_size")
            batch_size = kwargs.get("batch_size")
            resolved = checkpoint_size if checkpoint_size is not None else batch_size
            if resolved is None or resolved <= 0:
                resolved = DEFAULT_CHECKPOINT_ROWS
            kwargs["min_checkpoint_size"] = resolved
            kwargs["max_checkpoint_size"] = resolved
        return orig_backfill(self, *args, **kwargs)

    def _backfill_async(self, *args, **kwargs) -> object:
        if "min_checkpoint_size" not in kwargs and "max_checkpoint_size" not in kwargs:
            checkpoint_size = kwargs.get("checkpoint_size")
            batch_size = kwargs.get("batch_size")
            resolved = checkpoint_size if checkpoint_size is not None else batch_size
            if resolved is None or resolved <= 0:
                resolved = DEFAULT_CHECKPOINT_ROWS
            kwargs["min_checkpoint_size"] = resolved
            kwargs["max_checkpoint_size"] = resolved
        return orig_backfill_async(self, *args, **kwargs)

    monkeypatch.setattr(Table, "backfill", _backfill, raising=True)
    monkeypatch.setattr(Table, "backfill_async", _backfill_async, raising=True)


def setup_worker_logging() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )


with contextlib.suppress(ImportError):
    import ray

    # this is needed for the stateful udf test so that the test stateful udf class
    # is included in the python system class and packaged.
    @pytest.fixture(scope="session")
    def ray_with_test_path() -> None:
        with contextlib.suppress(Exception):
            ray.shutdown()

        test_path = os.path.abspath("src/tests")  # include test modules
        # Seed PYTHONPATH on the driver process *before* ``ray.init`` so that
        # Ray's worker env_vars propagation sees it; also put it on the
        # driver's own sys.path for symmetry. This is needed because Ray
        # workers need to import test modules (e.g. for UDTFs defined inside
        # test methods) during actor argument deserialization, which runs
        # before ``worker_process_setup_hook``.
        import sys as _sys

        existing_pythonpath = os.environ.get("PYTHONPATH", "")
        if test_path not in existing_pythonpath.split(os.pathsep):
            os.environ["PYTHONPATH"] = (
                f"{test_path}{os.pathsep}{existing_pythonpath}"
                if existing_pythonpath
                else test_path
            )
        if test_path not in _sys.path:
            _sys.path.insert(0, test_path)

        ray.init(
            log_to_driver=True,
            runtime_env={
                "env_vars": {"PYTHONPATH": os.environ["PYTHONPATH"]},
                "worker_process_setup_hook": setup_worker_logging,
            },
        )
        yield
        ray.shutdown()

    @pytest.fixture(scope="module", autouse=True)
    def ensure_ray_shutdown_between_modules(request) -> Generator[None, None, None]:
        """Ensure Ray is properly shut down between test modules.

        This fixture runs for every test module and ensures that Ray is in a
        clean state. It only applies to modules that have tests marked with
        'ray' to avoid unnecessary shutdown calls for non-Ray tests.

        This prevents issues where Ray is left in a stale state after one
        test module completes, causing hangs in subsequent modules.
        """
        # Check if this module has any ray-marked tests
        has_ray_tests = False
        for item in request.session.items:
            if item.fspath == request.fspath and item.get_closest_marker("ray"):
                has_ray_tests = True
                break

        if not has_ray_tests:
            yield
            return

        # Ensure clean state at module start
        with contextlib.suppress(Exception):
            ray.shutdown()

        yield

        # Ensure clean state at module end
        with contextlib.suppress(Exception):
            ray.shutdown()


def make_lance_dataset(
    tbl_path: Path,
    size: int = 17,
    max_rows_per_file: int = 5,
) -> lance.LanceDataset:
    """Create initial dataset with column 'a' as primary key."""
    data = {"a": pa.array(range(size))}
    tbl = pa.Table.from_pydict(data)
    ds = lance.write_dataset(
        tbl, tbl_path, max_rows_per_file=max_rows_per_file, data_storage_version="2.0"
    )
    return ds


@pytest.fixture
def tbl_path(tmp_path: Path) -> Path:
    """Return path for foo.lance table in tmp_path."""
    return tmp_path / "foo.lance"


@pytest.fixture
def lance_db(tmp_path: Path, tbl_path: Path) -> Generator[Connection, None, None]:
    """
    Create a Geneva connection with a pre-populated lance dataset.

    The dataset has column 'a' with values 0..16 (17 rows).
    """
    make_lance_dataset(tbl_path)
    db = geneva.connect(str(tmp_path), read_consistency_interval=timedelta(0))
    yield db
    db.close()


@pytest.fixture(scope="module")
def local_ray_context() -> Iterator[None]:
    """Enter local ray context for the duration of the test module.

    Use this fixture instead of `with db.local_ray_context():` blocks.
    Add `local_ray_context` to your test's parameters;
    backfill/refresh then run inside the context for the whole module.
    """
    with Connection.local_ray_context():
        yield


# ============================================================================
# Shared Fixtures for Matview Tests
# ============================================================================


@pytest.fixture
def db(tmp_path: Path) -> Connection:
    """Create a simple Geneva connection for testing."""
    return connect(tmp_path)


@pytest.fixture
def video_table(db: Connection) -> Table:
    """Create a video table with stable row IDs enabled."""
    tbl = pa.Table.from_pydict(
        {
            "video_uri": ["a", "b", "c", "d", "e", "f"],
            "rating": ["g", "nr", "pg", "pg-13", "r", "t"],
        }
    )
    return db.create_table(
        "table",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )


@pytest.fixture
def blob_table_factory() -> Callable[[Path, str], Table]:
    """Create a small blob-backed table for pandas export tests."""

    def _create_blob_table(tmp_path: Path, table_name: str = "blob_table") -> Table:
        db = connect(tmp_path)
        schema = pa.schema(
            [
                pa.field("id", pa.int32()),
                pa.field(
                    "blob",
                    pa.large_binary(),
                    metadata={"lance-encoding:blob": "true"},
                ),
            ]
        )
        table = pa.table(
            {
                "id": [0, 1, 2],
                "blob": [b"abc", b"defgh", b"ijklmnop"],
            },
            schema=schema,
        )
        return db.create_table(
            table_name,
            table,
            storage_options={"new_table_data_storage_version": "2.0"},
        )

    return _create_blob_table


with contextlib.suppress(ImportError):

    @pytest.fixture
    def namespace_db(tmp_path: Path) -> Generator[Connection, None, None]:
        """Create a namespace-based Geneva connection."""
        db = geneva.connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": str(tmp_path)},
        )
        yield db
        db.close()


# ============================================================================
# Shared Assertion Helpers for Matview Tests
# ============================================================================


def assert_udf_field_metadata(
    view: Table, field_name: str, expected_udf_name: str
) -> None:
    """Assert that a field has the expected UDF metadata.

    Args:
        view: The materialized view or table to check
        field_name: Name of the field to validate
        expected_udf_name: Expected UDF function name
    """
    udf_field = view.schema.field(field_name)
    assert udf_field.metadata.get(b"virtual_column") == b"true"
    assert udf_field.metadata.get(b"virtual_column.udf_inputs") is not None
    assert (
        udf_field.metadata.get(b"virtual_column.udf_name") == expected_udf_name.encode()
    )
    assert udf_field.metadata.get(b"virtual_column.udf_backend") is not None
    assert udf_field.metadata.get(b"virtual_column.udf") is not None


def assert_not_udf_field(view: Table, field_name: str) -> None:
    """Assert that a field is NOT a UDF (materialized column).

    Args:
        view: The materialized view or table to check
        field_name: Name of the field to validate
    """
    udf_field = view.schema.field(field_name)
    assert udf_field.metadata is None


def assert_mv_empty(mv: Table, filter_expr: str = "video is not null") -> None:
    """Assert that MV has no computed rows yet.

    Args:
        mv: The materialized view to check
        filter_expr: Filter expression to count non-null rows
    """
    cnt = mv.count_rows(filter=filter_expr)
    assert cnt == 0


def assert_mv_computed(
    mv: Table, expected_count: int | None = None, filter_expr: str = "video is null"
) -> None:
    """Assert that MV has been computed (no null values).

    Args:
        mv: The materialized view to check
        expected_count: Expected total row count (optional)
        filter_expr: Filter expression to count null rows
    """
    cnt_null = mv.count_rows(filter=filter_expr)
    assert cnt_null == 0
    if expected_count is not None:
        assert mv.count_rows() == expected_count


# ============================================================================
# Shared Data Helpers
# ============================================================================


def make_batch(start: int, count: int) -> pa.Table:
    """Create test data with alternating dog/cat categories.

    Args:
        start: Starting ID value
        count: Number of rows to create

    Returns:
        PyArrow table with id, category, and value columns
    """
    return pa.table(
        {
            "id": list(range(start, start + count)),
            "category": [
                "dog" if (i % 2 == 0) else "cat" for i in range(start, start + count)
            ],
            "value": [i * 10 for i in range(start, start + count)],
        }
    )


def make_id_value_table(
    n: int, *, start: int = 1, value_multiplier: int = 10
) -> pa.Table:
    """Create a simple id/value test table.

    Args:
        n: Number of rows to create
        start: Starting ID value (default 1)
        value_multiplier: Multiply ID by this to get value (default 10)

    Returns:
        PyArrow table with id and value columns

    Example:
        >>> make_id_value_table(3)
        # Returns: {"id": [1, 2, 3], "value": [10, 20, 30]}
    """
    ids = list(range(start, start + n))
    return pa.table(
        {
            "id": ids,
            "value": [i * value_multiplier for i in ids],
        }
    )


def make_multifragment_table(
    db: Connection,
    name: str,
    num_fragments: int,
    rows_per_fragment: int = 2,
    *,
    stable_row_ids: bool = True,
) -> Table:
    """Create a table with multiple fragments for testing.

    Args:
        db: Geneva database connection
        name: Table name
        num_fragments: Number of fragments to create
        rows_per_fragment: Rows per fragment (default 2)
        stable_row_ids: Enable stable row IDs (default True)

    Returns:
        Table with num_fragments fragments, each with rows_per_fragment rows
    """
    storage_opts = {"new_table_enable_stable_row_ids": stable_row_ids}

    # Create first fragment
    start = 0
    table = db.create_table(
        name,
        make_id_value_table(rows_per_fragment, start=start),
        storage_options=storage_opts,
    )

    # Add remaining fragments
    for i in range(1, num_fragments):
        start = i * rows_per_fragment
        table.add(make_id_value_table(rows_per_fragment, start=start))

    return table


# ============================================================================
# MV Workflow Helpers
# ============================================================================


def create_filtered_mv(
    db: Connection,
    source_table: Table,
    view_name: str,
    filter_expr: str,
    select_columns: list[str] | None = None,
) -> Table:
    """Create a materialized view with a filter.

    Args:
        db: Geneva database connection
        source_table: Source table to create MV from
        view_name: Name for the materialized view
        filter_expr: SQL filter expression (e.g., "category == 'dog'")
        select_columns: Columns to select (default: all columns)

    Returns:
        The created materialized view (not yet refreshed)
    """
    query = source_table.search(None).where(filter_expr)
    if select_columns:
        query = query.select(select_columns)
    return query.create_materialized_view(conn=db, view_name=view_name)


def refresh_and_verify(
    mv: Table,
    expected_count: int,
    *,
    column_checks: dict[str, list] | None = None,
    src_version: int | None = None,
) -> dict:
    """Refresh a materialized view and verify the results.

    Args:
        mv: Materialized view to refresh
        expected_count: Expected row count after refresh
        column_checks: Dict of {column_name: expected_sorted_values} to verify
        src_version: Optional source version to refresh to

    Returns:
        The result dict from mv.to_arrow().to_pydict()

    Raises:
        AssertionError: If row count or column values don't match expected

    Note:
        Must run inside a context (e.g. local_ray_context). _admission_check=False is
        used because unit tests run on local Ray clusters where admission control
        can hang. Integration tests cover admission control.
    """
    if src_version is not None:
        mv.refresh(src_version=src_version, _admission_check=False)
    else:
        mv.refresh(_admission_check=False)

    assert mv.count_rows() == expected_count, (
        f"Expected {expected_count} rows, got {mv.count_rows()}"
    )

    result = mv.to_arrow().to_pydict()

    if column_checks:
        for col_name, expected_values in column_checks.items():
            actual_values = sorted(result[col_name])
            assert actual_values == expected_values, (
                f"Column '{col_name}': expected {expected_values}, got {actual_values}"
            )

    return result
