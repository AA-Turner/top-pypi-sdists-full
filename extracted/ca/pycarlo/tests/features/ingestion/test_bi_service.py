from unittest import TestCase
from unittest.mock import MagicMock, Mock, PropertyMock

import pytest
from requests import HTTPError, Response

from pycarlo.core import Client
from pycarlo.features.ingestion.bi import AssetRef, BiAsset, BiOwner
from pycarlo.features.ingestion.exceptions import IngestionError
from pycarlo.features.ingestion.service import IngestionService


def _mock_client(scope: str = "Ingestion") -> MagicMock:
    client = MagicMock(spec=Client)
    type(client).session_scope = PropertyMock(return_value=scope)
    return client


def _asset(source_id: str = "dash-1", name: str = "Revenue") -> BiAsset:
    return BiAsset(asset_source_id=source_id, name=name, asset_type="dashboard")


class TestSendBiMetadata(TestCase):
    def test_sends_correct_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        result = svc.send_bi_metadata(
            resource_uuid="res-001",
            resource_type="custom-bi-connector",
            events=[
                BiAsset(
                    asset_source_id="dash-1",
                    name="Revenue",
                    asset_type="dashboard",
                    owner=BiOwner(email="a@b.com"),
                    inputs=[AssetRef(asset_type="TABLE", role="INPUT", mcon="MCON++x")],
                )
            ],
        )

        assert result == {"status": "ok"}
        client.make_request.assert_called_once()
        call = client.make_request.call_args
        assert call.kwargs["path"] == "/ingest/v1/bi/metadata"
        assert call.kwargs["method"] == "POST"
        body = call.kwargs["body"]
        assert body["event_type"] == "BI_METADATA"
        assert body["resource"] == {"uuid": "res-001", "resource_type": "custom-bi-connector"}
        assert len(body["events"]) == 1
        # Flat event — no ``bi_asset`` wrapper.
        assert "bi_asset" not in body["events"][0]
        assert body["events"][0]["asset_source_id"] == "dash-1"
        assert body["events"][0]["inputs"][0]["role"] == "INPUT"

    def test_sends_multiple_events(self):
        client = _mock_client()
        client.make_request.return_value = None
        svc = IngestionService(mc_client=client)

        svc.send_bi_metadata(
            resource_uuid="res-002",
            resource_type="custom-bi-connector",
            events=[_asset(source_id=f"a{i}", name=f"asset-{i}") for i in range(3)],
        )

        body = client.make_request.call_args.kwargs["body"]
        assert len(body["events"]) == 3
        for i, ev in enumerate(body["events"]):
            assert ev["name"] == f"asset-{i}"

    def test_exposes_invocation_id_from_response(self):
        client = _mock_client()
        client.make_request.return_value = {"invocation_id": "bi-meta-inv"}
        svc = IngestionService(mc_client=client)

        result = svc.send_bi_metadata(
            resource_uuid="res-001",
            resource_type="custom-bi-connector",
            events=[_asset()],
        )
        assert IngestionService.extract_invocation_id(result) == "bi-meta-inv"

    def test_raises_on_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="between 1 and 100"):
            svc.send_bi_metadata(
                resource_uuid="res-001",
                resource_type="custom-bi-connector",
                events=[],
            )
        client.make_request.assert_not_called()

    def test_raises_over_100_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="between 1 and 100"):
            svc.send_bi_metadata(
                resource_uuid="res-001",
                resource_type="custom-bi-connector",
                events=[_asset(source_id=f"a{i}") for i in range(101)],
            )
        client.make_request.assert_not_called()

    def test_wraps_http_error_as_ingestion_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = '{"error": "unauthorized"}'
        client.make_request.side_effect = HTTPError(response=response)
        svc = IngestionService(mc_client=client)

        with pytest.raises(IngestionError) as ctx:
            svc.send_bi_metadata(
                resource_uuid="res-001",
                resource_type="custom-bi-connector",
                events=[_asset()],
            )
        assert "unauthorized" in str(ctx.value)
        assert "BI metadata" in str(ctx.value)


class TestSendBiMetadataRaw(TestCase):
    def test_sends_raw_payload(self):
        client = _mock_client()
        client.make_request.return_value = {"status": "ok"}
        svc = IngestionService(mc_client=client)

        raw = {
            "event_type": "BI_METADATA",
            "resource": {"uuid": "r1", "resource_type": "custom-bi-connector"},
            "events": [{"asset_source_id": "a", "name": "n", "asset_type": "dashboard"}],
        }
        result = svc.send_bi_metadata_raw(payload=raw)

        assert result == {"status": "ok"}
        client.make_request.assert_called_once_with(
            path="/ingest/v1/bi/metadata",
            method="POST",
            body=raw,
        )

    def test_rejects_wrong_event_type(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="event_type"):
            svc.send_bi_metadata_raw(
                payload={"event_type": "WRONG", "resource": {}, "events": [{}]}
            )
        client.make_request.assert_not_called()

    def test_rejects_non_dict_resource(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="resource"):
            svc.send_bi_metadata_raw(
                payload={"event_type": "BI_METADATA", "resource": "nope", "events": [{}]}
            )
        client.make_request.assert_not_called()

    def test_rejects_empty_events(self):
        client = _mock_client()
        svc = IngestionService(mc_client=client)
        with pytest.raises(ValueError, match="events"):
            svc.send_bi_metadata_raw(
                payload={"event_type": "BI_METADATA", "resource": {}, "events": []}
            )
        client.make_request.assert_not_called()

    def test_wraps_http_error(self):
        client = _mock_client()
        response = Mock(spec=Response)
        response.text = "Bad Request"
        client.make_request.side_effect = HTTPError(response=response)
        svc = IngestionService(mc_client=client)

        with pytest.raises(IngestionError):
            svc.send_bi_metadata_raw(
                payload={"event_type": "BI_METADATA", "resource": {}, "events": [{}]}
            )
