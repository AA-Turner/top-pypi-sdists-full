from unittest import TestCase
from unittest.mock import MagicMock, Mock, PropertyMock

import pytest
from requests import HTTPError, Response

from pycarlo.core import Client
from pycarlo.features.ingestion.etl import (
    AssetRef,
    EtlAsset,
    EtlError,
    EtlRunEvent,
)
from pycarlo.features.ingestion.exceptions import IngestionError
from pycarlo.features.ingestion.service import IngestionService


def _mock_client(scope: str = "Ingestion") -> MagicMock:
    client = MagicMock(spec=Client)
    type(client).session_scope = PropertyMock(return_value=scope)
    return client


def _asset(name: str = "Daily orders") -> EtlAsset:
    return EtlAsset(
        job_source_id="dag1.task1",
        name=name,
    )


def _run_event(status: str = "in_progress") -> EtlRunEvent:
    return EtlRunEvent(
        job_source_id="dag1.task1",
        run_source_id="run-001",
        status=status,
        event_time="2026-05-15T10:00:00Z",
    )


class TestSendEtlMetadata(TestCase):
    def test_sends_correct_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        result = svc.send_etl_metadata(
            resource_uuid="res-001",
            resource_type="airflow",
            events=[_asset()],
        )

        assert result == {"status": "ok"}
        client.make_request.assert_called_once()
        call = client.make_request.call_args
        assert call.kwargs["path"] == "/ingest/v1/etl/metadata"
        assert call.kwargs["method"] == "POST"
        body = call.kwargs["body"]
        assert body["event_type"] == "ETL_METADATA"
        assert body["resource"] == {"uuid": "res-001", "resource_type": "airflow"}
        assert len(body["events"]) == 1
        assert body["events"][0]["etl_asset"]["name"] == "Daily orders"

    def test_sends_multiple_events(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        svc.send_etl_metadata(
            resource_uuid="res-002",
            resource_type="dbt",
            events=[_asset(name=f"job-{i}") for i in range(3)],
        )

        body = client.make_request.call_args.kwargs["body"]
        assert len(body["events"]) == 3
        for i, ev in enumerate(body["events"]):
            assert ev["etl_asset"]["name"] == f"job-{i}"

    def test_exposes_invocation_id_from_response(self):
        client = _mock_client()
        client.make_request.return_value = {"invocation_id": "etl-meta-inv"}
        svc = IngestionService(mc_client=client)

        result = svc.send_etl_metadata(
            resource_uuid="res-001",
            resource_type="airflow",
            events=[_asset()],
        )
        assert IngestionService.extract_invocation_id(result) == "etl-meta-inv"

    def test_raises_on_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="between 1 and 100"):
            svc.send_etl_metadata(
                resource_uuid="res-001",
                resource_type="airflow",
                events=[],
            )
        client.make_request.assert_not_called()

    def test_wraps_http_error_as_ingestion_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = '{"error": "unauthorized"}'
        client.make_request.side_effect = HTTPError(response=response)
        svc = IngestionService(mc_client=client)

        with pytest.raises(IngestionError) as ctx:
            svc.send_etl_metadata(
                resource_uuid="res-001",
                resource_type="airflow",
                events=[_asset()],
            )
        assert "unauthorized" in str(ctx.value)
        assert "ETL metadata" in str(ctx.value)


class TestSendEtlMetadataRaw(TestCase):
    def test_sends_raw_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        raw = {
            "event_type": "ETL_METADATA",
            "resource": {"uuid": "r1", "resource_type": "airflow"},
            "events": [
                {
                    "etl_asset": {
                        "job_source_id": "j",
                        "name": "n",
                    }
                }
            ],
        }
        result = svc.send_etl_metadata_raw(payload=raw)

        assert result == {"status": "ok"}
        client.make_request.assert_called_once_with(
            path="/ingest/v1/etl/metadata",
            method="POST",
            body=raw,
        )

    def test_wraps_http_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = "Bad Request"
        client.make_request.side_effect = HTTPError(response=response)
        svc = IngestionService(mc_client=client)

        with pytest.raises(IngestionError):
            svc.send_etl_metadata_raw(
                payload={"event_type": "ETL_METADATA", "resource": {}, "events": [{}]}
            )

    def test_rejects_wrong_event_type(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="event_type"):
            svc.send_etl_metadata_raw(
                payload={"event_type": "WRONG", "resource": {}, "events": [{}]}
            )
        client.make_request.assert_not_called()

    def test_rejects_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="events"):
            svc.send_etl_metadata_raw(
                payload={"event_type": "ETL_METADATA", "resource": {}, "events": []}
            )
        client.make_request.assert_not_called()


class TestSendEtlRuns(TestCase):
    def test_sends_correct_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        result = svc.send_etl_runs(
            resource_uuid="res-001",
            resource_type="airflow",
            events=[_run_event()],
        )

        assert result == {"status": "ok"}
        call = client.make_request.call_args
        assert call.kwargs["path"] == "/ingest/v1/etl/runs"
        assert call.kwargs["method"] == "POST"
        body = call.kwargs["body"]
        assert body["event_type"] == "ETLRUN"
        assert body["resource"] == {"uuid": "res-001", "resource_type": "airflow"}
        assert len(body["events"]) == 1
        assert body["events"][0]["status"] == "in_progress"
        assert "event_time" not in body

    def test_includes_optional_event_time(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        svc.send_etl_runs(
            resource_uuid="res-001",
            resource_type="airflow",
            events=[_run_event()],
            event_time="2026-05-15T10:00:00Z",
        )
        body = client.make_request.call_args.kwargs["body"]
        assert body["event_time"] == "2026-05-15T10:00:00Z"

    def test_sends_run_with_lineage_and_error(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        event = EtlRunEvent(
            job_source_id="j",
            run_source_id="r",
            status="failed",
            event_time="2026-05-15T10:00:00Z",
            trigger="SCHEDULE",
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", mcon="MCON::in")],
            outputs=[AssetRef(asset_type="TABLE", role="OUTPUT", mcon="MCON::out")],
            error=EtlError(message="boom"),
        )

        svc.send_etl_runs(
            resource_uuid="res-001",
            resource_type="airflow",
            events=[event],
        )
        body = client.make_request.call_args.kwargs["body"]
        ev = body["events"][0]
        assert ev["status"] == "failed"
        assert ev["trigger"] == "SCHEDULE"
        assert ev["inputs"][0]["mcon"] == "MCON::in"
        assert ev["outputs"][0]["mcon"] == "MCON::out"
        assert ev["error"] == {"message": "boom"}

    def test_exposes_invocation_id_from_response(self):
        client = _mock_client()
        client.make_request.return_value = {"invocation_id": "etl-runs-inv"}
        svc = IngestionService(mc_client=client)

        result = svc.send_etl_runs(
            resource_uuid="res-001",
            resource_type="airflow",
            events=[_run_event()],
        )
        assert IngestionService.extract_invocation_id(result) == "etl-runs-inv"

    def test_raises_on_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="between 1 and 100"):
            svc.send_etl_runs(
                resource_uuid="res-001",
                resource_type="airflow",
                events=[],
            )
        client.make_request.assert_not_called()

    def test_wraps_http_error_as_ingestion_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = '{"error": "boom"}'
        client.make_request.side_effect = HTTPError(response=response)
        svc = IngestionService(mc_client=client)

        with pytest.raises(IngestionError) as ctx:
            svc.send_etl_runs(
                resource_uuid="res-001",
                resource_type="airflow",
                events=[_run_event()],
            )
        assert "ETL runs" in str(ctx.value)
        assert "boom" in str(ctx.value)


class TestSendEtlRunsRaw(TestCase):
    def test_sends_raw_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        raw = {
            "event_type": "ETLRUN",
            "resource": {"uuid": "r1", "resource_type": "airflow"},
            "events": [
                {
                    "job_source_id": "j",
                    "run_source_id": "r",
                    "status": "success",
                    "event_time": "2026-05-15T10:00:00Z",
                }
            ],
        }
        result = svc.send_etl_runs_raw(payload=raw)

        assert result == {"status": "ok"}
        client.make_request.assert_called_once_with(
            path="/ingest/v1/etl/runs",
            method="POST",
            body=raw,
        )

    def test_wraps_http_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = "Bad Request"
        client.make_request.side_effect = HTTPError(response=response)
        svc = IngestionService(mc_client=client)

        with pytest.raises(IngestionError):
            svc.send_etl_runs_raw(payload={"event_type": "ETLRUN", "resource": {}, "events": [{}]})

    def test_rejects_wrong_event_type(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="event_type"):
            svc.send_etl_runs_raw(payload={"event_type": "WRONG", "resource": {}, "events": [{}]})
        client.make_request.assert_not_called()

    def test_rejects_oversized_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="events"):
            svc.send_etl_runs_raw(
                payload={"event_type": "ETLRUN", "resource": {}, "events": [{}] * 101}
            )
        client.make_request.assert_not_called()
