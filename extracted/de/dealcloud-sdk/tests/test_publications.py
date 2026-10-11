"""Tests for DealCloudPublications class."""

import asyncio
import json
import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.publications.dealcloud_publications import DealCloudPublications
from tests.publications_init_bootstrap_params import (
    INIT_BOOTSTRAP_PARAM_CASES,
    init_bootstrap_param_ids,
)


class TestDealCloudPublicationsInit:
    """Tests for initialization."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_sets_publications_url(self, mock_client_class):
        """Test that init sets publications URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert pub._publications_url == "https://test.dealcloud.com/api/rest/v1/publication"


class TestTopics:
    """Tests for topic operations."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_topics(self, mock_client_class):
        """Test get_topics returns list of topic name strings."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = ["data", "schema", "user"]
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = pub.get_topics()

        assert result == ["data", "schema", "user"]


class TestEventPolling:
    """Tests for event polling operations."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_poll_events(self, mock_client_class):
        """Test poll_events (PollRequestVm: topics, timeOut ms, count)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [
            {"eventId": 1, "topicName": "data", "topicOffset": 10, "entityType": "Company"},
        ]
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = pub.poll_events(topics=["data"], time_out_ms=30_000)

        assert len(result) == 1
        assert result[0]["topicName"] == "data"
        payload = mock_client.post.call_args[1]["json"]
        assert payload["topics"] == ["data"]
        assert payload["count"] == 100
        assert payload["timeOut"] == 30_000

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_poll_events_with_params(self, mock_client_class):
        """Test poll_events with count and time_out_ms."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        pub.poll_events(
            topics=["data", "schema"],
            count=50,
            time_out_ms=60_000,
        )

        payload = mock_client.post.call_args[1]["json"]
        assert payload["topics"] == ["data", "schema"]
        assert payload["count"] == 50
        assert payload["timeOut"] == 60_000

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_topic_offsets_from_events(self, mock_client_class):
        """Test topic_offsets_from_events builds max offset per topic."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        events = [
            {"topicName": "data", "topicOffset": 5},
            {"topicName": "data", "topicOffset": 10},
            {"topicName": "schema", "topicOffset": 3},
        ]
        result = pub.topic_offsets_from_events(events)
        assert result == [{"name": "data", "offset": 10}, {"name": "schema", "offset": 3}]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_acknowledge_topic_offsets(self, mock_client_class):
        """Test acknowledge_topic_offsets (array of TopicVm)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = None
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        pub.acknowledge_topic_offsets([{"name": "data", "offset": 10}])

        payload = mock_client.post.call_args[1]["json"]
        assert payload == [{"name": "data", "offset": 10}]

# init_bootstrap (OpenAPI: PublicationEntityType 0-21; 0,7,8,9,14,15,16,17,20,21 are internal).
# Typical standalone POST /initbootstrap entity types (live API):
#   1  Data          3  EntryLists     4  Users
#   5  UserGroups    6  UserProxy      18 UserFavorites
# 12 EntryGroups / 13 EntryToEntryGroups: not valid as standalone initbootstrap (400);
# rolled into Data bootstrap per product docs.
# PublicationEntityFormatType: 0 = Cells Structure, 1 = Rows Structure.
# test_init_bootstrap_all_entity_types_and_formats covers every OpenAPI enum
# combination (entity types 0-21 × formats 0-1); many entity types are internal
# for real initBootstrap use—see table above.

class TestBootstrap:
    """Tests for init_bootstrap (OpenAPI initbootstrap)."""

    @pytest.mark.parametrize(
        "entity_type,entity_format",
        INIT_BOOTSTRAP_PARAM_CASES,
        ids=init_bootstrap_param_ids(),
    )
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_bootstrap_all_entity_types_and_formats(
        self,
        mock_client_class,
        entity_type,
        entity_format,
    ):
        """init_bootstrap POSTs each PublicationEntityType (0-21) with each format (0-1)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = None
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        pub.init_bootstrap(entity_type=entity_type, entity_format=entity_format)

        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[0][0].endswith("/initbootstrap")
        assert call_args[1]["json"] == {
            "entityType": entity_type,
            "entityFormat": entity_format,
        }


class TestPublicationsUrl:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_publications_url_property(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert pub.publications_url == "https://test.dealcloud.com/api/rest/v1/publication"


class TestPollEventsHttpTimeout:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_poll_events_passes_http_timeout_to_client(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        pub.poll_events(topics=["data"], time_out_ms=1000, http_timeout_seconds=120.0)
        assert mock_client.post.call_args[1]["timeout"] == 120.0


class TestTopicOffsetsEdgeCases:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_topic_offsets_skips_events_missing_name_or_offset(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        events = [
            {"topicName": "data"},
            {"topicOffset": 1},
            {"topicName": "data", "topicOffset": 7},
        ]
        assert pub.topic_offsets_from_events(events) == [{"name": "data", "offset": 7}]


class TestStreamPollEvents:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_stream_poll_events_yields_ok_response(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.default_headers = {"X": "y"}
        mock_client.get_auth_headers.return_value = {"Authorization": "Bearer t"}
        mock_client.timeout = 30.0

        mock_resp = MagicMock()
        mock_resp.status_code = 200

        mock_stream_cm = MagicMock()
        mock_stream_cm.__enter__.return_value = mock_resp
        mock_stream_cm.__exit__.return_value = None

        mock_sync = MagicMock()
        mock_sync.stream.return_value = mock_stream_cm
        mock_client._get_sync_client.return_value = mock_sync
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pub.stream_poll_events(topics=["data"], count=5, time_out_ms=1000) as resp:
            assert resp is mock_resp
        mock_sync.stream.assert_called_once()
        call_kw = mock_sync.stream.call_args[1]
        assert call_kw["json"]["topics"] == ["data"]
        assert call_kw["timeout"] == 30.0

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_stream_poll_events_uses_http_timeout_override(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.default_headers = {}
        mock_client.get_auth_headers.return_value = {}
        mock_client.timeout = 30.0
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_stream_cm = MagicMock()
        mock_stream_cm.__enter__.return_value = mock_resp
        mock_stream_cm.__exit__.return_value = None
        mock_sync = MagicMock()
        mock_sync.stream.return_value = mock_stream_cm
        mock_client._get_sync_client.return_value = mock_sync
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pub.stream_poll_events(
            topics=["data"],
            time_out_ms=500,
            http_timeout_seconds=99.0,
        ):
            pass
        assert mock_sync.stream.call_args[1]["timeout"] == 99.0

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_stream_poll_events_http_error_json_body(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.default_headers = {}
        mock_client.get_auth_headers.return_value = {}
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.read.return_value = json.dumps({"error": "bad"}).encode()
        mock_resp.headers = {"h": "v"}
        mock_stream_cm = MagicMock()
        mock_stream_cm.__enter__.return_value = mock_resp
        mock_stream_cm.__exit__.return_value = None
        mock_sync = MagicMock()
        mock_sync.stream.return_value = mock_stream_cm
        mock_client._get_sync_client.return_value = mock_sync
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(HttpError) as excinfo:
            with pub.stream_poll_events(topics=["data"], time_out_ms=1):
                pass
        assert excinfo.value.status_code == 400
        assert excinfo.value.response_body == {"error": "bad"}

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_stream_poll_events_http_error_non_json_body(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.default_headers = {}
        mock_client.get_auth_headers.return_value = {}
        mock_resp = MagicMock()
        mock_resp.status_code = 502
        mock_resp.read.return_value = b"not json {{{"
        mock_resp.headers = {}
        mock_stream_cm = MagicMock()
        mock_stream_cm.__enter__.return_value = mock_resp
        mock_stream_cm.__exit__.return_value = None
        mock_sync = MagicMock()
        mock_sync.stream.return_value = mock_stream_cm
        mock_client._get_sync_client.return_value = mock_sync
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(HttpError) as excinfo:
            with pub.stream_poll_events(topics=["data"], time_out_ms=1):
                pass
        assert excinfo.value.status_code == 502
        assert "not json" in str(excinfo.value.response_body)

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_stream_poll_events_http_error_empty_body(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.default_headers = {}
        mock_client.get_auth_headers.return_value = {}
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_resp.read.return_value = b""
        mock_resp.headers = {}
        mock_stream_cm = MagicMock()
        mock_stream_cm.__enter__.return_value = mock_resp
        mock_stream_cm.__exit__.return_value = None
        mock_sync = MagicMock()
        mock_sync.stream.return_value = mock_stream_cm
        mock_client._get_sync_client.return_value = mock_sync
        mock_client_class.return_value = mock_client

        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(HttpError) as excinfo:
            with pub.stream_poll_events(topics=["data"], time_out_ms=1):
                pass
        assert excinfo.value.status_code == 403
        assert excinfo.value.response_body is None


class TestSubscribe:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_subscribe_keyboard_interrupt_on_empty_poll_sleep(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with (
            patch.object(pub, "poll_events", return_value=[]),
            patch(
                "dealcloud_sdk.publications.dealcloud_publications.time.sleep",
                side_effect=KeyboardInterrupt,
            ),
        ):
            pub.subscribe(
                topics=["data"],
                callback=lambda e: None,
                time_out_ms=1,
                poll_interval=1,
            )

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_subscribe_processes_events_auto_ack_and_stops_on_interrupt(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = None
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        ev = {"topicName": "data", "topicOffset": 42, "eventId": 1}
        calls = {"n": 0}

        def poll_side_effect(*_a, **_k):
            calls["n"] += 1
            if calls["n"] == 1:
                return [ev]
            return []

        def sleep_side_effect(_t):
            raise KeyboardInterrupt

        cb = MagicMock()
        with (
            patch.object(pub, "poll_events", side_effect=poll_side_effect),
            patch(
                "dealcloud_sdk.publications.dealcloud_publications.time.sleep",
                side_effect=sleep_side_effect,
            ),
        ):
            pub.subscribe(
                topics=["data"],
                callback=cb,
                time_out_ms=1,
                poll_interval=1,
                auto_acknowledge=True,
            )
        cb.assert_called_once_with(ev)
        ack_calls = [c for c in mock_client.post.call_args_list if "acknowledge" in str(c)]
        assert ack_calls

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_subscribe_callback_error_logged_then_batch_still_acknowledged(self, mock_client_class, caplog):
        """Per-event errors are logged; acknowledge still runs for the poll batch (see docstring on subscribe)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = None
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        def bad_cb(_e):
            raise RuntimeError("handler fail")

        ev = {"topicName": "data", "topicOffset": 1}
        calls = {"n": 0}

        def poll_side_effect(*_a, **_k):
            calls["n"] += 1
            if calls["n"] == 1:
                return [ev]
            return []

        def sleep_side_effect(_t):
            raise KeyboardInterrupt

        with caplog.at_level(logging.ERROR):
            with (
                patch.object(pub, "poll_events", side_effect=poll_side_effect),
                patch(
                    "dealcloud_sdk.publications.dealcloud_publications.time.sleep",
                    side_effect=sleep_side_effect,
                ),
            ):
                pub.subscribe(
                    topics=["data"],
                    callback=bad_cb,
                    time_out_ms=1,
                    poll_interval=1,
                    auto_acknowledge=True,
                )
        assert any("handler fail" in r.message for r in caplog.records)
        ack_urls = [c[0][0] for c in mock_client.post.call_args_list]
        assert any("acknowledge" in u for u in ack_urls)


class TestSubscribeAsync:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    @pytest.mark.asyncio
    async def test_subscribe_async_cancelled_error_exits_loop(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        async def cb(_e):
            pass

        with patch.object(pub, "poll_events", side_effect=asyncio.CancelledError()):
            await pub.subscribe_async(
                topics=["data"],
                callback=cb,
                time_out_ms=1,
                poll_interval=5,
            )

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    @pytest.mark.asyncio
    async def test_subscribe_async_callback_error_then_cancelled(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        async def bad_cb(_e):
            raise RuntimeError("async handler fail")

        calls = {"n": 0}

        def poll_side_effect(*_a, **_k):
            calls["n"] += 1
            if calls["n"] == 1:
                return [{"topicName": "data", "topicOffset": 1}]
            raise asyncio.CancelledError()

        with patch.object(pub, "poll_events", side_effect=poll_side_effect):
            await pub.subscribe_async(
                topics=["data"],
                callback=bad_cb,
                time_out_ms=1,
                poll_interval=5,
            )

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    @pytest.mark.asyncio
    async def test_subscribe_async_empty_poll_uses_asyncio_sleep(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        pub = DealCloudPublications(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        async def cb(_e):
            pass

        calls = {"n": 0}

        def poll_side_effect(*_a, **_k):
            calls["n"] += 1
            if calls["n"] == 1:
                return []
            raise asyncio.CancelledError()

        with (
            patch.object(pub, "poll_events", side_effect=poll_side_effect),
            patch(
                "dealcloud_sdk.publications.dealcloud_publications.asyncio.sleep",
                new_callable=AsyncMock,
            ) as mock_sleep,
        ):
            await pub.subscribe_async(
                topics=["data"],
                callback=cb,
                time_out_ms=1,
                poll_interval=3,
            )
        mock_sleep.assert_awaited()

