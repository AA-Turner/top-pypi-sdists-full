"""Tests for testmu_selenium._helpers.network — network_query HAR poller."""
import base64
import json
import pytest
from unittest.mock import MagicMock, patch, call

from testmu_selenium._helpers.network import network_query, _decode_har_entry


def _make_response(json_data):
    """Build a mock requests.Response whose .json() returns json_data."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = json_data
    return mock_resp


# ---------------------------------------------------------------------------
# network_query — direct fetch by network_log_id
# ---------------------------------------------------------------------------

class TestNetworkQueryByLogId:
    def test_returns_decoded_entry_when_found_by_id(self):
        entry = {
            "request": {"method": "GET", "url": "https://example.com/api"},
            "response": {
                "content": {"mimeType": "application/json", "text": '{"ok": true}'},
            },
        }
        with patch("requests.get") as mock_get:
            mock_get.return_value = _make_response({"entry": entry})
            result = network_query("GET", "https://example.com/api", 1, network_log_id="abc123")

        mock_get.assert_called_once_with(
            "http://127.0.0.1:8181/logs/entry?id=abc123", timeout=30
        )
        assert result["response"]["content"]["text"] == {"ok": True}

    def test_falls_through_to_polling_when_entry_is_empty(self):
        """When network_log_id lookup returns empty entry, polling loop runs."""
        logs_entry = {
            "request": {"method": "GET", "url": "https://example.com/api"},
            "response": {"content": {"mimeType": "text/plain", "text": "hello"}},
        }
        responses = [
            # First call: network_log_id fetch — empty entry
            _make_response({"entry": {}}),
            # Second call: /logs polling — returns one matching entry
            _make_response({"log": {"entries": [logs_entry]}}),
        ]
        with patch("requests.get", side_effect=responses) as mock_get, \
             patch("time.sleep"):
            result = network_query("GET", "https://example.com/api", 1,
                                   network_log_id="id-no-match",
                                   polling_interval=1, max_polling_time=2)

        assert mock_get.call_count == 2
        assert result["request"]["method"] == "GET"

    def test_falls_through_when_log_id_request_raises(self):
        """Exception on network_log_id fetch triggers fallback to polling."""
        matching_entry = {
            "request": {"method": "POST", "url": "https://api.test/submit"},
            "response": {"content": {"mimeType": "application/json", "text": "{}"}},
        }
        responses = [
            Exception("connection refused"),
            _make_response({"log": {"entries": [matching_entry]}}),
        ]
        with patch("requests.get", side_effect=responses), patch("time.sleep"):
            result = network_query("POST", "https://api.test/submit", 1,
                                   network_log_id="bad-id",
                                   polling_interval=1, max_polling_time=2)

        assert result["request"]["method"] == "POST"


# ---------------------------------------------------------------------------
# network_query — polling fall-through (no network_log_id)
# ---------------------------------------------------------------------------

class TestNetworkQueryPolling:
    def test_returns_entry_when_found_by_polling(self):
        entry = {
            "_id": "",
            "request": {"method": "GET", "url": "https://example.com/data"},
            "response": {"content": {"mimeType": "text/plain", "text": "ok"}},
        }
        with patch("requests.get", return_value=_make_response({"log": {"entries": [entry]}})), \
             patch("time.sleep"):
            result = network_query("GET", "https://example.com/data", 1,
                                   polling_interval=1, max_polling_time=2)

        assert result["request"]["url"] == "https://example.com/data"

    def test_fetches_full_entry_by_id_when_entry_id_present(self):
        list_entry = {
            "_id": "entry-xyz",
            "request": {"method": "GET", "url": "https://example.com/full"},
            "response": {"content": {"mimeType": "text/plain", "text": "list-version"}},
        }
        full_entry = {
            "request": {"method": "GET", "url": "https://example.com/full"},
            "response": {"content": {"mimeType": "application/json", "text": '{"full": true}'}},
        }
        responses = [
            _make_response({"log": {"entries": [list_entry]}}),
            _make_response({"entry": full_entry}),
        ]
        with patch("requests.get", side_effect=responses), patch("time.sleep"):
            result = network_query("GET", "https://example.com/full", 1,
                                   polling_interval=1, max_polling_time=2)

        assert result["response"]["content"]["text"] == {"full": True}

    def test_index_selects_nth_match(self):
        """index=2 picks the second matching entry, not the first."""
        entry1 = {
            "_id": "",
            "request": {"method": "GET", "url": "https://example.com/api"},
            "response": {"content": {"mimeType": "text/plain", "text": "first"}},
        }
        entry2 = {
            "_id": "",
            "request": {"method": "GET", "url": "https://example.com/api"},
            "response": {"content": {"mimeType": "text/plain", "text": "second"}},
        }
        with patch("requests.get", return_value=_make_response({"log": {"entries": [entry1, entry2]}})), \
             patch("time.sleep"):
            result = network_query("GET", "https://example.com/api", 2,
                                   polling_interval=1, max_polling_time=2)

        assert result["response"]["content"]["text"] == "second"

    def test_returns_empty_dict_after_max_tries_exhausted(self):
        """When no matching entry is found after max_tries, return {}."""
        with patch("requests.get", return_value=_make_response({"log": {"entries": []}})), \
             patch("time.sleep"):
            result = network_query("GET", "https://example.com/missing", 1,
                                   polling_interval=1, max_polling_time=2)

        assert result == {}

    def test_returns_empty_dict_when_polling_always_raises(self):
        """Exception on every poll attempt — return {} after exhaustion."""
        with patch("requests.get", side_effect=Exception("timeout")), \
             patch("time.sleep"):
            result = network_query("GET", "https://example.com/err", 1,
                                   polling_interval=1, max_polling_time=2)

        assert result == {}

    def test_poll_count_respects_max_polling_time(self):
        """max_tries = int(max_polling_time / polling_interval)."""
        sleep_mock = MagicMock()
        with patch("requests.get", return_value=_make_response({"log": {"entries": []}})), \
             patch("time.sleep", sleep_mock):
            network_query("GET", "https://example.com/x", 1,
                          polling_interval=2, max_polling_time=6)

        assert sleep_mock.call_count == 3  # max_tries = 6/2 = 3


# ---------------------------------------------------------------------------
# _decode_har_entry — base64 and JSON decoding
# ---------------------------------------------------------------------------

class TestDecodeHarEntry:
    def test_json_response_text_parsed(self):
        entry = {
            "request": {"postData": {}},
            "response": {
                "content": {
                    "mimeType": "application/json",
                    "text": '{"status": 200}',
                }
            },
        }
        result = _decode_har_entry(entry)
        assert result["response"]["content"]["text"] == {"status": 200}

    def test_base64_response_decoded_and_parsed(self):
        raw = json.dumps({"decoded": True})
        b64 = base64.b64encode(raw.encode()).decode()
        entry = {
            "request": {"postData": {}},
            "response": {
                "content": {
                    "mimeType": "application/json",
                    "encoding": "base64",
                    "text": b64,
                }
            },
        }
        result = _decode_har_entry(entry)
        assert result["response"]["content"]["text"] == {"decoded": True}

    def test_base64_request_post_data_decoded(self):
        raw = json.dumps({"body": "value"})
        b64 = base64.b64encode(raw.encode()).decode()
        entry = {
            "request": {
                "postData": {
                    "mimeType": "application/json",
                    "encoding": "base64",
                    "text": b64,
                }
            },
            "response": {"content": {"mimeType": "text/plain"}},
        }
        result = _decode_har_entry(entry)
        assert result["request"]["postData"]["text"] == {"body": "value"}

    def test_non_json_mimetype_left_untouched(self):
        entry = {
            "request": {"postData": {}},
            "response": {
                "content": {
                    "mimeType": "text/html",
                    "text": "<html>ok</html>",
                }
            },
        }
        result = _decode_har_entry(entry)
        assert result["response"]["content"]["text"] == "<html>ok</html>"

    def test_empty_text_sets_dict(self):
        entry = {
            "request": {"postData": {}},
            "response": {
                "content": {
                    "mimeType": "application/json",
                    "text": "",
                }
            },
        }
        result = _decode_har_entry(entry)
        assert result["response"]["content"]["text"] == {}

    def test_invalid_json_text_left_as_string(self):
        entry = {
            "request": {"postData": {}},
            "response": {
                "content": {
                    "mimeType": "application/json",
                    "text": "not-json",
                }
            },
        }
        result = _decode_har_entry(entry)
        # JSONDecodeError is caught; text left as-is original string
        assert result["response"]["content"]["text"] == "not-json"
