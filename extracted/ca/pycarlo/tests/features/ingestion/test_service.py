from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, Mock, PropertyMock

from requests import HTTPError, Response

from pycarlo.common.errors import InvalidSessionError
from pycarlo.core import Client
from pycarlo.features.ingestion.exceptions import IngestionError
from pycarlo.features.ingestion.models import (
    AssetField,
    AssetFreshness,
    AssetMetadata,
    AssetVolume,
    ColumnLineageField,
    ColumnLineageSourceField,
    LineageAssetRef,
    LineageEvent,
    QueryLogEntry,
    RelationalAsset,
    Tag,
)
from pycarlo.features.ingestion.service import IngestionService


def _dt(iso: str) -> datetime:
    """Parse ISO8601 string to datetime for tests."""
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def _mock_client(scope: str = "Ingestion") -> MagicMock:
    client = MagicMock(spec=Client)
    type(client).session_scope = PropertyMock(return_value=scope)
    return client


class TestIngestionServiceInit(TestCase):
    def test_raises_without_scope(self):
        client = MagicMock(spec=Client)
        type(client).session_scope = PropertyMock(return_value=None)
        with self.assertRaises(InvalidSessionError):
            IngestionService(mc_client=client)

    def test_creates_with_scoped_client(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        assert svc._client is client


class TestExtractInvocationId(TestCase):
    def test_returns_invocation_id_when_present(self):
        assert (
            IngestionService.extract_invocation_id({"invocation_id": "test-invocation-id"})
            == "test-invocation-id"
        )

    def test_returns_none_when_response_missing(self):
        assert IngestionService.extract_invocation_id(None) is None

    def test_returns_none_when_value_is_not_string(self):
        assert IngestionService.extract_invocation_id({"invocation_id": 123}) is None


class TestSendMetadata(TestCase):
    def test_sends_correct_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        asset = RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(name="orders", database="analytics", schema="public"),
            fields=[AssetField(name="id", type="INTEGER")],
            volume=AssetVolume(row_count=1000),
            freshness=AssetFreshness(last_update_time="2026-03-02T10:00:00Z"),
        )

        result = svc.send_metadata(
            resource_uuid="res-001",
            resource_type="snowflake",
            events=[asset],
        )

        assert result == {"status": "ok"}
        client.make_request.assert_called_once()
        call_kwargs = client.make_request.call_args
        assert call_kwargs.kwargs["path"] == "/ingest/v1/metadata"
        assert call_kwargs.kwargs["method"] == "POST"

        body = call_kwargs.kwargs["body"]
        assert body["event_type"] == "METADATA"
        assert body["resource"]["uuid"] == "res-001"
        assert body["resource"]["resource_type"] == "snowflake"
        assert len(body["events"]) == 1

        relational_asset = body["events"][0]["relational_asset"]
        assert relational_asset["type"] == "TABLE"
        assert relational_asset["metadata"]["name"] == "orders"
        assert relational_asset["fields"] == [{"name": "id", "type": "INTEGER"}]
        assert relational_asset["volume"] == {"row_count": 1000}
        assert relational_asset["freshness"] == {
            "last_update_time": "2026-03-02T10:00:00Z",
        }

    def test_exposes_invocation_id_from_response(self):
        client = _mock_client()
        client.make_request.return_value = {"invocation_id": "metadata-invocation-id"}
        svc = IngestionService(mc_client=client)

        result = svc.send_metadata(
            resource_uuid="res-001",
            resource_type="snowflake",
            events=[
                RelationalAsset(
                    type="TABLE",
                    metadata=AssetMetadata(name="orders", database="analytics", schema="public"),
                )
            ],
        )

        assert IngestionService.extract_invocation_id(result) == "metadata-invocation-id"

    def test_sends_multiple_events(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        events = [
            RelationalAsset(
                type="TABLE",
                metadata=AssetMetadata(name="t1", database="db", schema="s"),
            ),
            RelationalAsset(
                type="VIEW",
                metadata=AssetMetadata(name="v1", database="db", schema="s"),
                tags=[Tag(key="env", value="prod")],
            ),
        ]

        svc.send_metadata(
            resource_uuid="res-002",
            resource_type="bigquery",
            events=events,
        )

        body = client.make_request.call_args.kwargs["body"]
        assert len(body["events"]) == 2
        assert body["events"][0]["relational_asset"]["type"] == "TABLE"
        assert body["events"][1]["relational_asset"]["tags"] == [
            {"key": "env", "value": "prod"},
        ]

    def test_raises_on_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)

        with self.assertRaises(ValueError, msg="At least one"):
            svc.send_metadata(
                resource_uuid="res-003",
                resource_type="snowflake",
                events=[],
            )
        client.make_request.assert_not_called()

    def test_wraps_http_error_as_ingestion_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = '{"error": "unauthorized"}'
        http_error = HTTPError(response=response)
        client.make_request.side_effect = http_error

        svc = IngestionService(mc_client=client)

        with self.assertRaises(IngestionError) as ctx:
            svc.send_metadata(
                resource_uuid="res-004",
                resource_type="snowflake",
                events=[
                    RelationalAsset(
                        type="TABLE",
                        metadata=AssetMetadata(name="t", database="d", schema="s"),
                    ),
                ],
            )
        assert "unauthorized" in str(ctx.exception)


class TestSendMetadataRaw(TestCase):
    def test_sends_raw_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        raw = {
            "event_type": "METADATA",
            "resource": {"uuid": "r1", "resource_type": "snowflake"},
            "events": [
                {
                    "relational_asset": {
                        "type": "TABLE",
                        "metadata": {"name": "t", "database": "d", "schema": "s"},
                    },
                },
            ],
        }

        result = svc.send_metadata_raw(payload=raw)

        assert result == {"status": "ok"}
        client.make_request.assert_called_once_with(
            path="/ingest/v1/metadata",
            method="POST",
            body=raw,
        )

    def test_wraps_http_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = "Bad Request"
        client.make_request.side_effect = HTTPError(response=response)

        svc = IngestionService(mc_client=client)

        with self.assertRaises(IngestionError):
            svc.send_metadata_raw(payload={"event_type": "METADATA"})


# ---------------------------------------------------------------
# send_lineage
# ---------------------------------------------------------------


def _table_event() -> LineageEvent:
    return LineageEvent(
        destination=LineageAssetRef(
            type="TABLE", database="analytics", schema="pub", name="summary"
        ),
        sources=[
            LineageAssetRef(type="TABLE", database="raw", schema="pub", name="orders"),
            LineageAssetRef(type="TABLE", database="raw", schema="pub", name="customers"),
        ],
    )


def _column_event() -> LineageEvent:
    return LineageEvent(
        destination=LineageAssetRef(type="TABLE", database="db", schema="s", name="dst"),
        sources=[
            LineageAssetRef(type="TABLE", database="db", schema="s", name="src", asset_id="src1"),
        ],
        fields=[
            ColumnLineageField(
                name="total",
                source_fields=[
                    ColumnLineageSourceField(asset_id="src1", field_name="amount"),
                ],
            ),
        ],
    )


class TestSendLineage(TestCase):
    def test_sends_correct_table_lineage_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        result = svc.send_lineage(
            resource_uuid="res-001",
            resource_type="snowflake",
            events=[_table_event()],
        )

        assert result == {"status": "ok"}
        client.make_request.assert_called_once()
        call_kwargs = client.make_request.call_args
        assert call_kwargs.kwargs["path"] == "/ingest/v1/lineage"
        assert call_kwargs.kwargs["method"] == "POST"

        body = call_kwargs.kwargs["body"]
        assert body["event_type"] == "LINEAGE"
        assert body["resource"]["uuid"] == "res-001"
        assert body["resource"]["resource_type"] == "snowflake"
        assert len(body["events"]) == 1
        assert body["events"][0]["destination"]["name"] == "summary"
        assert len(body["events"][0]["sources"]) == 2

    def test_exposes_invocation_id_from_response(self):
        client = _mock_client()
        client.make_request.return_value = {"invocation_id": "lineage-invocation-id"}
        svc = IngestionService(mc_client=client)

        result = svc.send_lineage(
            resource_uuid="res-001",
            resource_type="snowflake",
            events=[_table_event()],
        )

        assert IngestionService.extract_invocation_id(result) == "lineage-invocation-id"

    def test_sends_column_lineage_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        result = svc.send_lineage(
            resource_uuid="res-001",
            resource_type="snowflake",
            events=[_column_event()],
        )

        assert result == {"status": "ok"}
        body = client.make_request.call_args.kwargs["body"]
        assert body["event_type"] == "COLUMN_LINEAGE"
        assert "fields" in body["events"][0]
        assert body["events"][0]["fields"][0]["name"] == "total"

    def test_explicit_event_type_overrides(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        svc.send_lineage(
            resource_uuid="res-001",
            resource_type="snowflake",
            events=[_column_event()],
            event_type="LINEAGE",
        )

        body = client.make_request.call_args.kwargs["body"]
        assert body["event_type"] == "LINEAGE"

    def test_sends_multiple_events(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        svc.send_lineage(
            resource_uuid="res-002",
            resource_type="bigquery",
            events=[_table_event(), _table_event()],
        )

        body = client.make_request.call_args.kwargs["body"]
        assert len(body["events"]) == 2

    def test_raises_on_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)

        with self.assertRaises(ValueError, msg="At least one"):
            svc.send_lineage(
                resource_uuid="res-003",
                resource_type="snowflake",
                events=[],
            )
        client.make_request.assert_not_called()

    def test_wraps_http_error_as_ingestion_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = '{"error": "unauthorized"}'
        client.make_request.side_effect = HTTPError(response=response)

        svc = IngestionService(mc_client=client)

        with self.assertRaises(IngestionError) as ctx:
            svc.send_lineage(
                resource_uuid="res-004",
                resource_type="snowflake",
                events=[_table_event()],
            )
        assert "unauthorized" in str(ctx.exception)


# ---------------------------------------------------------------
# send_query_logs
# ---------------------------------------------------------------


class TestSendQueryLogs(TestCase):
    def test_sends_correct_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        entry = QueryLogEntry(
            start_time=_dt("2026-03-02T10:00:00Z"),
            end_time=_dt("2026-03-02T10:00:05Z"),
            query_text="SELECT * FROM orders",
            query_id="q-123",
            returned_rows=100,
        )

        result = svc.send_query_logs(
            resource_uuid="res-001",
            resource_type="snowflake",
            events=[entry],
        )

        assert result == {"status": "ok"}
        client.make_request.assert_called_once()
        call_kwargs = client.make_request.call_args
        assert call_kwargs.kwargs["path"] == "/ingest/v1/querylogs"
        assert call_kwargs.kwargs["method"] == "POST"

        body = call_kwargs.kwargs["body"]
        assert body["event_type"] == "QUERY_LOG"
        assert body["resource"]["uuid"] == "res-001"
        assert body["resource"]["resource_type"] == "snowflake"
        assert len(body["events"]) == 1
        assert body["events"][0]["start_time"] == "2026-03-02T10:00:00Z"
        assert body["events"][0]["query_text"] == "SELECT * FROM orders"
        assert body["events"][0]["query_id"] == "q-123"
        assert body["events"][0]["returned_rows"] == 100

    def test_sends_multiple_events(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        events = [
            QueryLogEntry(
                start_time=_dt("2026-03-02T10:00:00Z"),
                end_time=_dt("2026-03-02T10:00:01Z"),
                query_text=f"SELECT {i}",
            )
            for i in range(3)
        ]

        svc.send_query_logs(
            resource_uuid="res-002",
            resource_type="bigquery",
            events=events,
        )

        body = client.make_request.call_args.kwargs["body"]
        assert len(body["events"]) == 3

    def test_raises_on_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)

        with self.assertRaises(ValueError):
            svc.send_query_logs(
                resource_uuid="res-003",
                resource_type="snowflake",
                events=[],
            )
        client.make_request.assert_not_called()

    def test_wraps_http_error_as_ingestion_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = '{"error": "unauthorized"}'
        client.make_request.side_effect = HTTPError(response=response)

        svc = IngestionService(mc_client=client)

        with self.assertRaises(IngestionError) as ctx:
            svc.send_query_logs(
                resource_uuid="res-004",
                resource_type="snowflake",
                events=[
                    QueryLogEntry(
                        start_time=_dt("2026-03-02T10:00:00Z"),
                        end_time=_dt("2026-03-02T10:00:01Z"),
                        query_text="SELECT 1",
                    ),
                ],
            )
        assert "unauthorized" in str(ctx.exception)


class TestSendLineageRaw(TestCase):
    def test_sends_raw_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        raw = {
            "event_type": "LINEAGE",
            "resource": {"uuid": "r1", "resource_type": "snowflake"},
            "events": [
                {
                    "destination": {
                        "type": "TABLE",
                        "database": "db",
                        "schema": "s",
                        "name": "t",
                    },
                    "sources": [
                        {
                            "type": "TABLE",
                            "database": "db",
                            "schema": "s",
                            "name": "src",
                        },
                    ],
                },
            ],
        }

        result = svc.send_lineage_raw(payload=raw)

        assert result == {"status": "ok"}
        client.make_request.assert_called_once_with(
            path="/ingest/v1/lineage",
            method="POST",
            body=raw,
        )

    def test_wraps_http_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = "Bad Request"
        client.make_request.side_effect = HTTPError(response=response)

        svc = IngestionService(mc_client=client)

        with self.assertRaises(IngestionError):
            svc.send_lineage_raw(payload={"event_type": "LINEAGE"})


class TestSendQueryLogsRaw(TestCase):
    def test_sends_raw_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        raw = {
            "event_type": "QUERY_LOG",
            "resource": {"uuid": "r1", "resource_type": "snowflake"},
            "events": [
                {
                    "start_time": "2026-03-02T10:00:00Z",
                    "end_time": "2026-03-02T10:00:05Z",
                    "query_text": "SELECT 1",
                },
            ],
        }

        result = svc.send_query_logs_raw(payload=raw)

        assert result == {"status": "ok"}
        client.make_request.assert_called_once_with(
            path="/ingest/v1/querylogs",
            method="POST",
            body=raw,
        )

    def test_wraps_http_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = "Bad Request"
        client.make_request.side_effect = HTTPError(response=response)

        svc = IngestionService(mc_client=client)

        with self.assertRaises(IngestionError):
            svc.send_query_logs_raw(payload={"event_type": "QUERY_LOG"})
