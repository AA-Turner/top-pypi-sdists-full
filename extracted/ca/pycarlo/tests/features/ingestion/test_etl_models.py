import json
from typing import Any
from unittest import TestCase

import pytest

from pycarlo.features.ingestion.etl import (
    ASSET_REF_ASSET_TYPE_VALUES,
    ASSET_REF_ROLE_VALUES,
    ETL_RUN_STATUS_VALUES,
    ETL_RUN_TRIGGER_VALUES,
    ETL_SCHEDULE_KIND_VALUES,
    AssetRef,
    EtlAsset,
    EtlError,
    EtlGroup,
    EtlMetadataEvent,
    EtlRunEvent,
    EtlTask,
    Owner,
    Schedule,
    build_etl_metadata_payload,
    build_etl_runs_payload,
)
from pycarlo.features.ingestion.models import Tag


class TestStatusAndTriggerValues(TestCase):
    def test_status_values_lowercase(self):
        for v in ETL_RUN_STATUS_VALUES:
            assert v == v.lower()

    def test_trigger_values_uppercase(self):
        for v in ETL_RUN_TRIGGER_VALUES:
            assert v == v.upper()

    def test_asset_type_values(self):
        assert ASSET_REF_ASSET_TYPE_VALUES == frozenset(
            {"TABLE", "FILE", "VIEW", "TOPIC", "DATASET", "DASHBOARD"}
        )

    def test_role_values(self):
        assert ASSET_REF_ROLE_VALUES == frozenset({"INPUT", "OUTPUT"})


class TestSchedule(TestCase):
    def test_to_dict_minimal(self):
        s = Schedule(kind="cron")
        assert s.to_dict() == {"kind": "cron"}

    def test_to_dict_full(self):
        s = Schedule(
            kind="event",
            cron_expression="0 * * * *",
            interval_seconds=3600,
            timezone="UTC",
            next_run_at="2026-05-15T11:00:00Z",
            paused=False,
            event_trigger={"source": "s3", "bucket": "raw"},
            upstream_job_source_ids=["job-A", "job-B"],
            raw={"vendor": "airflow"},
        )
        result = s.to_dict()
        assert result["kind"] == "event"
        assert result["cron_expression"] == "0 * * * *"
        assert result["interval_seconds"] == 3600
        assert result["timezone"] == "UTC"
        assert result["next_run_at"] == "2026-05-15T11:00:00Z"
        assert result["paused"] is False
        assert result["event_trigger"] == {"source": "s3", "bucket": "raw"}
        assert result["upstream_job_source_ids"] == ["job-A", "job-B"]
        assert result["raw"] == {"vendor": "airflow"}

    def test_to_dict_omits_empty_list(self):
        s = Schedule(kind="cron", upstream_job_source_ids=[])
        assert "upstream_job_source_ids" not in s.to_dict()

    def test_rejects_bad_kind(self):
        with pytest.raises(ValueError, match="kind must be one of"):
            Schedule(kind="weekly")

    def test_all_allowed_kinds(self):
        for k in ETL_SCHEDULE_KIND_VALUES:
            Schedule(kind=k)


class TestOwner(TestCase):
    def test_to_dict_empty(self):
        assert Owner().to_dict() == {}

    def test_to_dict_full(self):
        o = Owner(
            primary_email="a@b.com",
            primary_name="Alice",
            primary_external_id="ext-1",
            run_as_email="svc@b.com",
            notification_emails=["x@y.com"],
            team="data",
            raw={"src": "test"},
        )
        result = o.to_dict()
        assert result["primary_email"] == "a@b.com"
        assert result["primary_name"] == "Alice"
        assert result["primary_external_id"] == "ext-1"
        assert result["run_as_email"] == "svc@b.com"
        assert result["notification_emails"] == ["x@y.com"]
        assert result["team"] == "data"
        assert result["raw"] == {"src": "test"}


class TestEtlError(TestCase):
    def test_to_dict_minimal(self):
        e = EtlError(message="boom")
        assert e.to_dict() == {"message": "boom"}

    def test_to_dict_full(self):
        e = EtlError(
            message="failed",
            code="E42",
            retryable=True,
            failure_type="SourceError",
            upstream_failed_task_source_ids=["t1", "t2"],
            structured_fields={"k": "v"},
        )
        result = e.to_dict()
        assert result["message"] == "failed"
        assert result["code"] == "E42"
        assert result["retryable"] is True
        assert result["failure_type"] == "SourceError"
        assert result["upstream_failed_task_source_ids"] == ["t1", "t2"]
        assert result["structured_fields"] == {"k": "v"}


class TestAssetRef(TestCase):
    def test_to_dict_mcon_only(self):
        r = AssetRef(asset_type="TABLE", role="INPUT", mcon="MCON::abc")
        assert r.to_dict() == {"asset_type": "TABLE", "role": "INPUT", "mcon": "MCON::abc"}

    def test_to_dict_fqn_only(self):
        r = AssetRef(asset_type="VIEW", role="OUTPUT", fully_qualified_name="db.s.t")
        assert r.to_dict() == {
            "asset_type": "VIEW",
            "role": "OUTPUT",
            "fully_qualified_name": "db.s.t",
        }

    def test_requires_mcon_or_fqn(self):
        with pytest.raises(ValueError, match="at least one of mcon"):
            AssetRef(asset_type="TABLE", role="INPUT")

    def test_requires_non_empty_mcon_or_fqn(self):
        with pytest.raises(ValueError, match="at least one of mcon"):
            AssetRef(asset_type="TABLE", role="INPUT", mcon="")
        with pytest.raises(ValueError, match="at least one of mcon"):
            AssetRef(asset_type="TABLE", role="OUTPUT", fully_qualified_name="")

    def test_rejects_bad_asset_type(self):
        with pytest.raises(ValueError, match="asset_type must be one of"):
            AssetRef(asset_type="WRONG", role="INPUT", mcon="x")

    def test_rejects_bad_role(self):
        with pytest.raises(ValueError, match="role must be one of"):
            AssetRef(asset_type="TABLE", role="WRONG", mcon="x")

    def test_all_allowed_asset_types(self):
        for t in ASSET_REF_ASSET_TYPE_VALUES:
            AssetRef(asset_type=t, role="INPUT", mcon="x")

    def test_all_allowed_roles(self):
        for r in ASSET_REF_ROLE_VALUES:
            AssetRef(asset_type="TABLE", role=r, mcon="x")


class TestEtlGroup(TestCase):
    def test_to_dict_minimal(self):
        g = EtlGroup(source_id="dag1")
        assert g.to_dict() == {"source_id": "dag1"}

    def test_to_dict_full(self):
        g = EtlGroup(
            source_id="dag1",
            name="Daily DAG",
            group_type="DAG",
            schedule=Schedule(kind="cron", cron_expression="0 0 * * *"),
            attributes={"vendor": "airflow"},
        )
        result: dict[str, Any] = g.to_dict()
        assert result["source_id"] == "dag1"
        assert result["name"] == "Daily DAG"
        assert result["group_type"] == "DAG"
        assert result["schedule"]["cron_expression"] == "0 0 * * *"
        assert result["attributes"] == {"vendor": "airflow"}

    def test_round_trip(self):
        g = EtlGroup(source_id="dag1", name="Daily DAG", group_type="DAG")
        restored = EtlGroup.from_dict(g.to_dict())
        assert restored == g


class TestEtlAsset(TestCase):
    def test_to_dict_omits_none_group(self):
        a = EtlAsset(job_source_id="j", name="n")
        assert "group" not in a.to_dict()

    def test_round_trip_with_group(self):
        a = EtlAsset(
            job_source_id="dag1.task1",
            name="Daily orders",
            group=EtlGroup(source_id="dag1", name="Daily DAG", group_type="DAG"),
        )
        restored = EtlAsset.from_dict(a.to_dict())
        assert restored.group == EtlGroup(source_id="dag1", name="Daily DAG", group_type="DAG")

    def test_to_dict_minimal(self):
        a = EtlAsset(job_source_id="j1", name="J1")
        assert a.to_dict() == {
            "job_source_id": "j1",
            "name": "J1",
        }

    def test_to_dict_full(self):
        a = EtlAsset(
            job_source_id="dag1.task1",
            name="Daily orders",
            group=EtlGroup(source_id="dag1", name="Daily DAG", group_type="DAG"),
            description="loads orders",
            folder="prod/etl",
            is_paused=False,
            job_url="https://airflow/dags/dag1",
            schedule=Schedule(kind="cron", cron_expression="0 0 * * *"),
            owner=Owner(primary_email="a@b.com"),
            properties=[Tag(key="team", value="data")],
            attributes={"vendor": "airflow"},
        )
        result: dict[str, Any] = a.to_dict()
        assert result["job_source_id"] == "dag1.task1"
        assert result["group"] == {"source_id": "dag1", "name": "Daily DAG", "group_type": "DAG"}
        assert result["folder"] == "prod/etl"
        assert result["is_paused"] is False
        assert result["schedule"]["cron_expression"] == "0 0 * * *"
        assert result["owner"]["primary_email"] == "a@b.com"
        assert result["properties"] == [{"key": "team", "value": "data"}]
        assert result["attributes"] == {"vendor": "airflow"}

    def test_round_trip_matches_wire_field_names(self):
        """Hand-rolled wire fixture for EtlAsset field names."""
        wire_fields = {
            "group",
            "job_source_id",
            "name",
            "description",
            "folder",
            "is_paused",
            "job_url",
            "schedule",
            "owner",
            "properties",
            "attributes",
            "inputs",
            "outputs",
        }
        a = EtlAsset(
            job_source_id="j",
            name="n",
            group=EtlGroup(source_id="g", name="gn", group_type="DAG"),
            description="d",
            folder="f",
            is_paused=True,
            job_url="u",
            schedule=Schedule(kind="cron"),
            owner=Owner(primary_email="o@x.com"),
            properties=[Tag(key="k", value="v")],
            attributes={"a": 1},
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", fully_qualified_name="db:s.t_in")],
            outputs=[
                AssetRef(asset_type="TABLE", role="OUTPUT", fully_qualified_name="db:s.t_out")
            ],
        )
        produced = set(a.to_dict().keys())
        assert produced == wire_fields, (
            f"extra: {produced - wire_fields}, missing: {wire_fields - produced}"
        )

    def test_to_dict_omits_empty_inputs_outputs(self):
        a = EtlAsset(job_source_id="j", name="n", inputs=[], outputs=[])
        result = a.to_dict()
        assert "inputs" not in result
        assert "outputs" not in result

    def test_to_dict_serializes_inputs_outputs(self):
        a = EtlAsset(
            job_source_id="j",
            name="n",
            inputs=[
                AssetRef(
                    asset_type="TABLE",
                    role="INPUT",
                    fully_qualified_name="analytics:prod.in_table",
                )
            ],
            outputs=[
                AssetRef(
                    asset_type="TABLE",
                    role="OUTPUT",
                    fully_qualified_name="analytics:prod.out_table",
                )
            ],
        )
        result = a.to_dict()
        assert result["inputs"] == [
            {
                "asset_type": "TABLE",
                "role": "INPUT",
                "fully_qualified_name": "analytics:prod.in_table",
            }
        ]
        assert result["outputs"] == [
            {
                "asset_type": "TABLE",
                "role": "OUTPUT",
                "fully_qualified_name": "analytics:prod.out_table",
            }
        ]


class TestEtlTask(TestCase):
    def test_to_dict_minimal(self):
        t = EtlTask(task_source_id="t1", name="T1")
        assert t.to_dict() == {"task_source_id": "t1", "name": "T1"}

    def test_to_dict_full(self):
        t = EtlTask(
            task_source_id="dag1.task1",
            name="Load orders",
            task_type="PythonOperator",
            description="loads orders",
            attributes={"vendor": "airflow"},
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", fully_qualified_name="db:s.t_in")],
            outputs=[
                AssetRef(asset_type="TABLE", role="OUTPUT", fully_qualified_name="db:s.t_out")
            ],
            upstream_task_source_ids=["dag1.extract"],
            triggered_job_source_ids=["dag2"],
        )
        result: dict[str, Any] = t.to_dict()
        assert result["task_source_id"] == "dag1.task1"
        assert result["name"] == "Load orders"
        assert result["task_type"] == "PythonOperator"
        assert result["description"] == "loads orders"
        assert result["attributes"] == {"vendor": "airflow"}
        assert result["inputs"][0]["fully_qualified_name"] == "db:s.t_in"
        assert result["outputs"][0]["fully_qualified_name"] == "db:s.t_out"
        assert result["upstream_task_source_ids"] == ["dag1.extract"]
        assert result["triggered_job_source_ids"] == ["dag2"]

    def test_round_trip_matches_wire_field_names(self):
        wire_fields = {
            "task_source_id",
            "name",
            "task_type",
            "description",
            "inputs",
            "outputs",
            "upstream_task_source_ids",
            "triggered_job_source_ids",
            "attributes",
        }
        t = EtlTask(
            task_source_id="t",
            name="n",
            task_type="op",
            description="d",
            attributes={"a": 1},
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", fully_qualified_name="db:s.t_in")],
            outputs=[
                AssetRef(asset_type="TABLE", role="OUTPUT", fully_qualified_name="db:s.t_out")
            ],
            upstream_task_source_ids=["u1"],
            triggered_job_source_ids=["j1"],
        )
        produced = set(t.to_dict().keys())
        assert produced == wire_fields, (
            f"extra: {produced - wire_fields}, missing: {wire_fields - produced}"
        )

    def test_to_dict_omits_empty_collections(self):
        t = EtlTask(
            task_source_id="t",
            name="n",
            inputs=[],
            outputs=[],
            upstream_task_source_ids=[],
            triggered_job_source_ids=[],
        )
        result = t.to_dict()
        assert "inputs" not in result
        assert "outputs" not in result
        assert "upstream_task_source_ids" not in result
        assert "triggered_job_source_ids" not in result

    def test_propagates_asset_ref_validation(self):
        with pytest.raises(ValueError, match="at least one of mcon"):
            EtlTask(
                task_source_id="t",
                name="n",
                inputs=[AssetRef(asset_type="TABLE", role="INPUT")],
            )


class TestEtlAssetTasks(TestCase):
    def test_to_dict_omits_empty_tasks(self):
        a = EtlAsset(job_source_id="j", name="n", tasks=[])
        assert "tasks" not in a.to_dict()

    def test_to_dict_nests_tasks(self):
        a = EtlAsset(
            job_source_id="dag1",
            name="DAG 1",
            tasks=[
                EtlTask(task_source_id="dag1.t1", name="Task 1"),
                EtlTask(
                    task_source_id="dag1.t2",
                    name="Task 2",
                    inputs=[
                        AssetRef(asset_type="TABLE", role="INPUT", fully_qualified_name="db:s.in")
                    ],
                ),
            ],
        )
        result: dict[str, Any] = a.to_dict()
        assert len(result["tasks"]) == 2
        assert result["tasks"][0] == {"task_source_id": "dag1.t1", "name": "Task 1"}
        assert result["tasks"][1]["inputs"][0]["fully_qualified_name"] == "db:s.in"
        json.dumps(result)  # must serialize cleanly end-to-end

    def test_round_trip_with_tasks(self):
        a = EtlAsset(
            job_source_id="dag1",
            name="DAG 1",
            tasks=[EtlTask(task_source_id="dag1.t1", name="Task 1")],
        )
        restored = EtlAsset.from_dict(a.to_dict())
        assert restored.tasks[0].task_source_id == "dag1.t1"
        assert restored.tasks[0].name == "Task 1"

    def test_metadata_payload_carries_tasks(self):
        a = EtlAsset(
            job_source_id="dag1",
            name="DAG 1",
            tasks=[EtlTask(task_source_id="dag1.t1", name="Task 1")],
        )
        payload = build_etl_metadata_payload(resource_uuid="r", resource_type="airflow", events=[a])
        tasks = payload["events"][0]["etl_asset"]["tasks"]
        assert tasks == [{"task_source_id": "dag1.t1", "name": "Task 1"}]


class TestEtlMetadataEvent(TestCase):
    def test_to_dict_wraps_asset(self):
        a = EtlAsset(job_source_id="j", name="n")
        e = EtlMetadataEvent(etl_asset=a)
        assert e.to_dict() == {"etl_asset": a.to_dict()}


class TestEtlRunEvent(TestCase):
    def test_to_dict_minimal(self):
        e = EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="in_progress",
            event_time="2026-05-15T10:00:00Z",
        )
        assert e.to_dict() == {
            "job_source_id": "j",
            "run_source_id": "r",
            "status": "in_progress",
            "event_time": "2026-05-15T10:00:00Z",
        }

    def test_to_dict_full(self):
        e = EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="success",
            event_time="2026-05-15T10:00:00Z",
            job_run_id="jr-1",
            task_source_id="t1",
            start_time="2026-05-15T09:55:00Z",
            end_time="2026-05-15T10:00:00Z",
            expected_end_time="2026-05-15T10:01:00Z",
            queued_at="2026-05-15T09:54:00Z",
            trigger="SCHEDULE",
            triggered_by_run_source_id="upstream-r",
            parent_attempt_run_source_id="r-1",
            attempt_number=2,
            backfill_id="bf-1",
            error=None,
            run_url="https://airflow/runs/r",
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", mcon="MCON::in")],
            outputs=[AssetRef(asset_type="TABLE", role="OUTPUT", mcon="MCON::out")],
            properties=[Tag(key="env", value="prod")],
            attributes={"k": "v"},
        )
        result: dict[str, Any] = e.to_dict()
        assert result["job_run_id"] == "jr-1"
        assert result["task_source_id"] == "t1"
        assert result["start_time"] == "2026-05-15T09:55:00Z"
        assert result["end_time"] == "2026-05-15T10:00:00Z"
        assert result["expected_end_time"] == "2026-05-15T10:01:00Z"
        assert result["queued_at"] == "2026-05-15T09:54:00Z"
        assert result["trigger"] == "SCHEDULE"
        assert result["triggered_by_run_source_id"] == "upstream-r"
        assert result["parent_attempt_run_source_id"] == "r-1"
        assert result["attempt_number"] == 2
        assert result["backfill_id"] == "bf-1"
        assert result["run_url"] == "https://airflow/runs/r"
        assert len(result["inputs"]) == 1
        assert len(result["outputs"]) == 1
        assert result["properties"] == [{"key": "env", "value": "prod"}]
        assert result["attributes"] == {"k": "v"}
        assert "error" not in result

    def test_to_dict_with_error(self):
        e = EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="failed",
            event_time="t",
            error=EtlError(message="boom", code="E1"),
        )
        result = e.to_dict()
        assert result["error"] == {"message": "boom", "code": "E1"}

    def test_to_dict_with_nested_task_runs(self):
        task = EtlRunEvent(
            job_source_id="j",
            run_source_id="r.t1",
            task_source_id="t1",
            status="success",
            event_time="t",
        )
        e = EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="success",
            event_time="t",
            task_runs=[task],
        )
        result: dict[str, Any] = e.to_dict()
        assert len(result["task_runs"]) == 1
        assert result["task_runs"][0]["task_source_id"] == "t1"
        assert isinstance(result["task_runs"][0], dict)
        json.dumps(result)  # must serialize cleanly end-to-end

    def test_rejects_bad_status(self):
        with pytest.raises(ValueError, match="status must be one of"):
            EtlRunEvent(
                job_source_id="j",
                run_source_id="r",
                status="RUNNING",
                event_time="t",
            )

    def test_rejects_bad_trigger(self):
        with pytest.raises(ValueError, match="trigger must be one of"):
            EtlRunEvent(
                job_source_id="j",
                run_source_id="r",
                status="success",
                event_time="t",
                trigger="WRONG",
            )

    def test_allows_none_trigger(self):
        EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="success",
            event_time="t",
            trigger=None,
        )

    def test_rejects_zero_attempt_number(self):
        with pytest.raises(ValueError, match="attempt_number must be >= 1"):
            EtlRunEvent(
                job_source_id="j",
                run_source_id="r",
                status="success",
                event_time="t",
                attempt_number=0,
            )

    def test_allows_none_attempt_number(self):
        EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="success",
            event_time="t",
            attempt_number=None,
        )


class TestBuildEtlMetadataPayload(TestCase):
    def _asset(self, name: str = "n") -> EtlAsset:
        return EtlAsset(job_source_id="j", name=name)

    def test_payload_structure(self):
        payload = build_etl_metadata_payload(
            resource_uuid="res-123",
            resource_type="airflow",
            events=[self._asset()],
        )
        assert payload == {
            "event_type": "ETL_METADATA",
            "resource": {"uuid": "res-123", "resource_type": "airflow"},
            "events": [
                {
                    "etl_asset": {
                        "job_source_id": "j",
                        "name": "n",
                    }
                }
            ],
        }

    def test_multiple_events(self):
        events = [self._asset(name=f"n{i}") for i in range(3)]
        payload = build_etl_metadata_payload(resource_uuid="r", resource_type="dbt", events=events)
        assert len(payload["events"]) == 3
        for i, ev in enumerate(payload["events"]):
            assert ev["etl_asset"]["name"] == f"n{i}"

    def test_rejects_empty_batch(self):
        with pytest.raises(ValueError, match="between 1 and 100"):
            build_etl_metadata_payload(resource_uuid="r", resource_type="x", events=[])

    def test_rejects_oversized_batch(self):
        with pytest.raises(ValueError, match="between 1 and 100"):
            build_etl_metadata_payload(
                resource_uuid="r", resource_type="x", events=[self._asset()] * 101
            )

    def test_accepts_max_batch(self):
        payload = build_etl_metadata_payload(
            resource_uuid="r", resource_type="x", events=[self._asset()] * 100
        )
        assert len(payload["events"]) == 100


class TestBuildEtlRunsPayload(TestCase):
    def _event(self) -> EtlRunEvent:
        return EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="success",
            event_time="2026-05-15T10:00:00Z",
        )

    def test_payload_structure(self):
        payload = build_etl_runs_payload(
            resource_uuid="res-1",
            resource_type="airflow",
            events=[self._event()],
        )
        assert payload["event_type"] == "ETLRUN"
        assert payload["resource"] == {"uuid": "res-1", "resource_type": "airflow"}
        assert len(payload["events"]) == 1
        assert "event_time" not in payload

    def test_includes_optional_event_time(self):
        payload = build_etl_runs_payload(
            resource_uuid="res-1",
            resource_type="airflow",
            events=[self._event()],
            event_time="2026-05-15T10:00:00Z",
        )
        assert payload["event_time"] == "2026-05-15T10:00:00Z"

    def test_rejects_empty_batch(self):
        with pytest.raises(ValueError, match="between 1 and 100"):
            build_etl_runs_payload(resource_uuid="r", resource_type="x", events=[])

    def test_rejects_oversized_batch(self):
        with pytest.raises(ValueError, match="between 1 and 100"):
            build_etl_runs_payload(
                resource_uuid="r", resource_type="x", events=[self._event()] * 101
            )

    def test_accepts_max_batch(self):
        payload = build_etl_runs_payload(
            resource_uuid="r",
            resource_type="x",
            events=[self._event()] * 100,
        )
        assert len(payload["events"]) == 100
