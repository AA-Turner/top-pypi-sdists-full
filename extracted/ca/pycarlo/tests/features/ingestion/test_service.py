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
    RelationalAsset,
    Tag,
)
from pycarlo.features.ingestion.service import IngestionService


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
