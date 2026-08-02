# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import base64
import logging
from pathlib import Path

import pytest
import ray  # noqa: F401

from geneva import connect
from geneva.jobs import JobRecord, JobStateManager, JobStatus
from geneva.jobs.jobs import JobMetric
from geneva.runners.ray.pipeline import _submit_ray_job

_LOG = logging.getLogger(__name__)


@pytest.fixture
def jobrecord() -> JobRecord:
    return JobRecord(table_name="test_table", column_name="test_column", config="{}")


def test_jobrecord(jobrecord) -> None:
    job = jobrecord
    assert job.job_id is not None
    assert job.table_name == "test_table"
    assert job.column_name == "test_column"
    assert job.config == "{}"
    assert job.status == JobStatus.PENDING
    assert job.object_ref is None


def test_jobrecord_with_manifest_fields() -> None:
    """Test that JobRecord can store manifest_id and manifest_checksum"""
    job = JobRecord(
        table_name="test_table",
        column_name="test_column",
        config="{}",
        manifest_id="my-manifest",
        manifest_checksum="abc123def456",
    )
    assert job.manifest_id == "my-manifest"
    assert job.manifest_checksum == "abc123def456"


def test_jobrecord_with_audit_field_paths() -> None:
    job = JobRecord(
        table_name="test_table",
        column_name="user_id",
        input_columns=["MetaData.UserId"],
        output_columns=["user_id"],
    )
    assert job.input_columns == ["MetaData.UserId"]
    assert job.output_columns == ["user_id"]


def test_jobstatemanager_persists_audit_field_paths(tmp_path: Path) -> None:
    db = connect(tmp_path)
    jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs_audit_paths")

    job = jsm.launch(
        table_name="test_table",
        column_name="user_id",
        input_columns=["MetaData.UserId"],
        output_columns=["user_id"],
    )

    assert job.input_columns == ["MetaData.UserId"]
    assert job.output_columns == ["user_id"]

    retrieved = jsm.get(job.job_id)[0]
    assert retrieved.input_columns == ["MetaData.UserId"]
    assert retrieved.output_columns == ["user_id"]

    jsm.set_running(job.job_id)
    listed = jsm.list_jobs("test_table")
    assert listed[0].input_columns == ["MetaData.UserId"]
    assert listed[0].output_columns == ["user_id"]


def test_submit_ray_job_marks_failed_on_submit_error() -> None:
    class Hist:
        def __init__(self) -> None:
            self.failed: list[tuple[str, str]] = []

        def set_failed(self, job_id: str, msg: str) -> None:
            self.failed.append((job_id, msg))

        def set_object_ref(self, job_id: str, object_ref: bytes) -> None:
            raise AssertionError("object ref should not be persisted")

    hist = Hist()

    def fail_submit() -> object:
        raise RuntimeError("submit failed")

    with pytest.raises(RuntimeError, match="submit failed"):
        _submit_ray_job(hist, "job-1", fail_submit)

    assert hist.failed == [("job-1", "submit failed")]


def test_submit_ray_job_continues_when_object_ref_persist_fails(caplog) -> None:
    class Hist:
        def __init__(self) -> None:
            self.failed: list[tuple[str, str]] = []

        def set_failed(self, job_id: str, msg: str) -> None:
            self.failed.append((job_id, msg))

        def set_object_ref(self, job_id: str, object_ref: bytes) -> None:
            raise RuntimeError("persist failed")

    hist = Hist()
    obj_ref = object()

    with caplog.at_level(logging.WARNING):
        result = _submit_ray_job(hist, "job-2", lambda: obj_ref)

    assert result is obj_ref
    assert hist.failed == []
    assert "Failed to persist Ray object ref for job job-2" in caplog.text


def test_jobstatemanager(tmp_path: Path) -> None:
    db = connect(tmp_path)
    jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs")

    tbl = db.open_table("test_jobs", namespace_path=db.system_namespace)
    assert tbl.count_rows() == 0
    _LOG.info(tbl.schema)

    tbl = jsm.get_table()  # Ensure the table is created
    assert tbl.count_rows() == 0
    _LOG.info(tbl.schema)

    job = jsm.launch(
        table_name="test_table",
        column_name="test_column",
        arg1=1,
        arg2=0.0,
        arg3="test",
    )
    _LOG.info(job)
    job = jsm.get(job.job_id)[0]
    assert job.status == JobStatus.PENDING.name
    assert job.object_ref is None
    assert job.updated_at is not None

    bad = jsm.get("nonexistent_job")
    assert len(bad) == 0

    jsm.set_running(job.job_id)
    job = jsm.get(job.job_id)[0]
    assert job.status == JobStatus.RUNNING.name
    assert job.object_ref is None
    updated_at_after_running = job.updated_at
    assert updated_at_after_running is not None  # updated_at should be set

    b64_object_ref = base64.b64encode(b"xyz").decode("utf-8")
    jsm.set_object_ref(job.job_id, b"xyz")
    job = jsm.get(job.job_id)[0]
    assert job.object_ref == b64_object_ref
    assert job.updated_at is not None
    assert job.updated_at >= updated_at_after_running  # updated_at should advance

    jobs = jsm.list_jobs("test_table")
    assert len(jobs) == 1
    assert jobs[0].job_id == job.job_id
    assert jobs[0].status == JobStatus.RUNNING.name
    assert jobs[0].object_ref == b64_object_ref

    updated_at_before_metrics = job.updated_at
    metrics = {
        "fragments": {
            "n": 12,
            "total": 100,
            "done": False,
            "desc": "[49f9f2dd0475423896c1c3f35fe68cf2 - b] Batches scheduled",
        },
        "rows_checkpointed": {
            "n": 400,
            "total": 10000,
            "done": False,
            "desc": "[49f9f2dd0475423896c1c3f35fe68cf2 - b (100 fragments)] Rows "
            "checkpointed",
        },
    }
    jsm.update_metrics(job.job_id, metrics)
    job = jsm.get(job.job_id)[0]
    assert job.updated_at is not None
    assert job.updated_at >= updated_at_before_metrics  # updated_at should advance

    updated_at_before_completed = job.updated_at
    jsm.set_completed(job.job_id)
    job = jsm.get(job.job_id)[0]
    assert job.status == JobStatus.DONE.name
    assert job.object_ref == b64_object_ref
    assert job.updated_at is not None
    assert job.updated_at >= updated_at_before_completed  # updated_at should advance
    assert job.metrics == [
        JobMetric(
            desc="[49f9f2dd0475423896c1c3f35fe68cf2 - b] Batches scheduled",
            done=False,
            n=12,
            name="fragments",
            total=100,
        ),
        JobMetric(
            desc="[49f9f2dd0475423896c1c3f35fe68cf2 - b (100 fragments)] Rows "
            "checkpointed",
            done=False,
            n=400,
            name="rows_checkpointed",
            total=10000,
        ),
    ]


def test_list_jobs_no_filter(tmp_path: Path) -> None:
    db = connect(tmp_path)
    jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs_no_filter")
    job = jsm.launch(table_name="test_table", column_name="test_column")

    jobs = jsm.list_jobs(status=None)
    assert [j.job_id for j in jobs] == [job.job_id]


def test_set_failed_updates_updated_at(tmp_path: Path) -> None:
    """Test that set_failed updates the updated_at field."""
    db = connect(tmp_path)
    jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs_failed")

    job = jsm.launch(
        table_name="test_table",
        column_name="test_column",
    )
    job = jsm.get(job.job_id)[0]
    assert job.updated_at is not None  # Not updated yet after launch
    prev_updated_at = job.updated_at

    jsm.set_failed(job.job_id, "Something went wrong")
    job = jsm.get(job.job_id)[0]

    assert job.status == JobStatus.FAILED.name
    assert job.updated_at > prev_updated_at
    assert "Job failed: Something went wrong" in job.events


def test_safe_job_record_with_none_metrics(tmp_path: Path) -> None:
    """Test that _safe_job_record handles None metrics gracefully."""
    from geneva.jobs.jobs import _safe_job_record

    # Simulate a job record dict with metrics set to None
    jr_dict = {
        "table_name": "test_table",
        "column_name": "test_column",
        "job_id": "test-job-123",
        "metrics": None,  # This is the problematic case
    }

    # Should not raise TypeError
    job_record = _safe_job_record(jr_dict)
    assert job_record.metrics == []


def test_jobstatemanager_with_manifest(tmp_path: Path) -> None:
    """Test that JobStateManager.launch() stores manifest_id and manifest_checksum"""
    db = connect(tmp_path)
    jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs_manifest")

    # Launch job with manifest info
    job = jsm.launch(
        table_name="test_table",
        column_name="test_column",
        manifest_id="test-manifest",
        manifest_checksum="abc123def456",
        arg1=1,
    )

    # Verify manifest fields are stored
    assert job.manifest_id == "test-manifest"
    assert job.manifest_checksum == "abc123def456"

    # Retrieve from database and verify persistence
    retrieved_job = jsm.get(job.job_id)[0]
    assert retrieved_job.manifest_id == "test-manifest"
    assert retrieved_job.manifest_checksum == "abc123def456"


def test_raycluster_manifest_attachment() -> None:
    """Test that RayCluster can store a manifest reference"""
    from geneva.manifest.mgr import GenevaManifest
    from geneva.runners.ray.raycluster import RayCluster

    # Create a manifest
    manifest = GenevaManifest(
        name="test-manifest",
        pip=["numpy"],
    )

    # Create a RayCluster
    cluster = RayCluster(
        name="test-cluster",
        namespace="test-ns",
    )

    # Manifest should be None by default
    assert cluster.manifest is None

    # Attach manifest
    cluster.manifest = manifest

    # Verify manifest is attached
    assert cluster.manifest is not None
    assert cluster.manifest.name == "test-manifest"
    assert cluster.manifest.checksum == manifest.checksum


def test_manifest_auto_registration(tmp_path: Path, monkeypatch) -> None:
    """Test that manifests are auto-registered when launching jobs"""
    from geneva.manifest.mgr import GenevaManifest, ManifestConfigManager
    from geneva.runners.ray.raycluster import RayCluster

    db = connect(tmp_path)

    # Create a manifest without a name
    manifest = GenevaManifest(
        name="",  # Empty name to trigger auto-naming
        pip=["numpy"],
    )

    # Create and set up context with RayCluster
    cluster = RayCluster(name="test-cluster", namespace="test-ns")
    cluster.manifest = manifest

    # Simulate what happens in dispatch_run_ray_add_column
    # by extracting manifest and auto-registering
    manifest_mgr = ManifestConfigManager(db)

    # The name should be empty initially
    assert manifest.name == ""

    # Save original checksum before modifying name
    # (name is included in checksum, so changing it changes the checksum)
    original_checksum = manifest.checksum

    # Simulate auto-naming logic from dispatch_run_ray_add_column
    from datetime import datetime

    from geneva.utils import current_user

    if manifest.name == "":
        user = current_user()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        checksum_short = original_checksum[:8] if original_checksum else "unknown"
        manifest.name = f"auto-{user}-{timestamp}-{checksum_short}"

    # Verify auto-generated name format
    assert manifest.name.startswith("auto-")
    assert original_checksum[:8] in manifest.name

    # Register the manifest
    manifest_mgr.upsert(manifest)

    # Verify it's persisted
    loaded = manifest_mgr.load(manifest.name)
    assert loaded is not None
    # Note: checksum will differ because name is included in checksum
    # But the pip dependencies should match
    assert loaded.pip == ["numpy"]
    assert loaded.name == manifest.name


def test_forward_compatibility_with_extra_column(tmp_path: Path) -> None:
    """Test that old clients can read tables with new columns they don't understand."""
    db = connect(tmp_path)
    jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs_forward_compat")

    # Create a job with the current schema
    job = jsm.launch(
        table_name="test_table",
        column_name="test_column",
        arg1=1,
        arg2="test",
    )
    _LOG.info(f"Created job: {job}")

    # Simulate schema evolution: add a new column that old clients don't know about
    # This is what would happen when a newer version adds a field to JobRecord
    jsm.get_table().add_columns({"new_future_field": "'default_value'"})
    _LOG.info(f"Added new column. Schema: {jsm.get_table().schema}")

    # Old client tries to read the record (should not fail despite extra column)
    retrieved_jobs = jsm.get(job.job_id)
    assert len(retrieved_jobs) == 1
    retrieved_job = retrieved_jobs[0]

    # Verify the job was read correctly (known fields only)
    assert retrieved_job.job_id == job.job_id
    assert retrieved_job.table_name == "test_table"
    assert retrieved_job.column_name == "test_column"
    assert retrieved_job.status == "PENDING"

    # Verify list_active also works with extra column
    jsm.set_running(job.job_id)
    active_jobs = jsm.list_jobs("test_table")
    assert len(active_jobs) == 1
    assert active_jobs[0].job_id == job.job_id
    assert active_jobs[0].status == "RUNNING"

    _LOG.info("Forward compatibility test passed!")


def test_schema_migration_nullable_fields(tmp_path: Path) -> None:
    """Test that adding Optional fields creates nullable columns with NULL defaults."""
    db = connect(tmp_path)

    # Step 1: Create table with OLD schema (simulate pre-manifest_id code)
    import enum

    import attrs
    import pyarrow as pa

    from geneva.utils.schema import attrs_to_arrow_schema

    old_jr = JobRecord(table_name="test", column_name="test")
    full_schema = attrs_to_arrow_schema(old_jr)

    # Create schema without manifest fields (simulate old version)
    old_fields = [
        f for f in full_schema if f.name not in ["manifest_id", "manifest_checksum"]
    ]
    old_schema = pa.schema(old_fields)

    # Create table with old schema in the system namespace location.
    jobs_table = db.create_table(
        "test_jobs_migration",
        schema=old_schema,
        namespace_path=db.system_namespace,
    )

    # Add a row with old schema
    old_data = attrs.asdict(
        JobRecord(table_name="old_table", column_name="old_col"),
        filter=lambda attr, val: attr.name in [f.name for f in old_schema],
        value_serializer=lambda obj, a, v: v.value if isinstance(v, enum.Enum) else v,
    )
    jobs_table.add([old_data])

    _LOG.info(f"Created table with old schema: {[f.name for f in old_schema]}")

    # Step 2: Trigger migration by creating JobStateManager
    jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs_migration")

    # Step 3: Verify the new fields are nullable
    schema_fields = {f.name: f for f in jsm.get_table().schema}

    assert "manifest_id" in schema_fields, (
        "manifest_id field should exist after migration"
    )
    assert "manifest_checksum" in schema_fields, (
        "manifest_checksum field should exist after migration"
    )

    manifest_id_field = schema_fields["manifest_id"]
    manifest_checksum_field = schema_fields["manifest_checksum"]

    # CRITICAL: These fields must be nullable
    assert manifest_id_field.nullable, (
        "manifest_id must be nullable (was marked non-null, causing lance error)"
    )
    assert manifest_checksum_field.nullable, (
        "manifest_checksum must be nullable (was marked non-null, causing lance error)"
    )

    # Verify type is string, not null
    assert manifest_id_field.type == pa.string(), (
        f"manifest_id type should be string, got {manifest_id_field.type}"
    )
    assert manifest_checksum_field.type == pa.string(), (
        f"manifest_checksum type should be string, got {manifest_checksum_field.type}"
    )

    _LOG.info(
        f"✓ manifest_id: {manifest_id_field.type} nullable={manifest_id_field.nullable}"
    )
    _LOG.info(
        f"✓ manifest_checksum: {manifest_checksum_field.type} "
        f"nullable={manifest_checksum_field.nullable}"
    )

    # Step 4: Verify existing rows have NULL values
    rows = jsm.get_table().to_arrow().to_pylist()
    assert len(rows) == 1
    assert rows[0]["manifest_id"] is None, (
        "Existing rows should have NULL for manifest_id"
    )
    assert rows[0]["manifest_checksum"] is None, (
        "Existing rows should have NULL for manifest_checksum"
    )

    # Step 5: Verify we can insert new rows with manifest values
    new_job = jsm.launch(
        table_name="new_table",
        column_name="new_col",
        manifest_id="test-manifest",
        manifest_checksum="abc123",
    )

    retrieved = jsm.get(new_job.job_id)[0]
    assert retrieved.manifest_id == "test-manifest"
    assert retrieved.manifest_checksum == "abc123"

    # Step 6: Verify we can insert new rows without manifest values
    new_job2 = jsm.launch(
        table_name="another_table",
        column_name="another_col",
    )

    retrieved2 = jsm.get(new_job2.job_id)[0]
    assert retrieved2.manifest_id is None
    assert retrieved2.manifest_checksum is None

    _LOG.info("Schema migration with nullable fields test passed!")
