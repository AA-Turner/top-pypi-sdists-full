#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Unit tests for featrix_post_event() / _post_event.py.

Unlike test_e2e_collect_and_build.py, these tests mock the HTTP layer
(requests.post) entirely -- no network access, no API key, no live server
required. They mirror the coverage in featrixevents-ts/tests/post-event.test.ts
so the Python and TypeScript clients are checked against the same wire-protocol
contract.

Run with:
    pytest featrixevents/tests/test_post_event_unit.py -v
"""

import pytest
import requests

from featrixevents import featrix_post_event, FeatrixEventError, FeatrixEventSectionObject
from featrixevents._post_event import DEFAULT_BASE_URL


class _FakeResponse:
    """Minimal stand-in for requests.Response."""

    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text

    def json(self):
        if self._json_data is None:
            raise ValueError("response body is not JSON")
        return self._json_data


def _install_fake_post(monkeypatch, fake_response=None, exc=None, capture=None):
    """Patch requests.post to return fake_response or raise exc, recording the call."""

    def _fake_post(url, json=None, headers=None, timeout=None):
        if capture is not None:
            capture['url'] = url
            capture['json'] = json
            capture['headers'] = headers
            capture['timeout'] = timeout
        if exc is not None:
            raise exc
        return fake_response

    monkeypatch.setattr(requests, "post", _fake_post)


# ---------------------------------------------------------------------------
# Success paths
# ---------------------------------------------------------------------------

def test_success_200_returns_json_body(monkeypatch):
    capture = {}
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(200, {"success": True, "event_id": "evt-1"}),
        capture=capture,
    )

    result = featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="11111111-1111-1111-1111-111111111111",
        event_payload={"action": "click"},
    )

    assert result == {"success": True, "event_id": "evt-1"}
    assert capture['url'] == f"{DEFAULT_BASE_URL}/events/ingest"
    assert capture['headers']["X-Api-Key"] == "fx_test_key"
    assert capture['headers']["Content-Type"] == "application/json"
    assert capture['json'] == {
        "event_group_id": "11111111-1111-1111-1111-111111111111",
        "event_payload": {"action": "click"},
    }
    assert capture['timeout'] == 30.0


def test_event_group_name_and_targets_are_sent_when_given(monkeypatch):
    capture = {}
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(201, {"success": True, "event_id": "evt-3", "event_group_name": "checkout-events"}),
        capture=capture,
    )

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="11111111-1111-1111-1111-111111111111",
        event_payload={"amount": 12},
        event_group_name="checkout-events",
        auto_predictor_targets=[{"target_column": "amount", "task_type": "regression"}],
    )

    assert capture['json']["event_group_name"] == "checkout-events"
    assert capture['json']["auto_predictor_targets"] == [{"target_column": "amount", "task_type": "regression"}]


def test_state_graph_fields_are_sent_when_given(monkeypatch):
    capture = {}
    _install_fake_post(monkeypatch, fake_response=_FakeResponse(201, {"success": True, "event_id": "evt-g"}), capture=capture)

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="11111111-1111-1111-1111-111111111111",
        event_payload={"qa_result": "PASS"},
        entity_id="job-9",
        state="completed",
        terminal=True,
    )

    assert capture['json']["entity_id"] == "job-9"
    assert capture['json']["state"] == "completed"
    assert capture['json']["terminal"] is True


def test_state_graph_fields_omitted_by_default(monkeypatch):
    capture = {}
    _install_fake_post(monkeypatch, fake_response=_FakeResponse(200, {"success": True, "event_id": "evt-p"}), capture=capture)
    featrix_post_event(auth_key_id="fx_test_key", event_group_id="g", event_payload={})
    assert not {"entity_id", "state", "terminal", "data_version"} & set(capture['json'])


def test_data_version_is_sent_top_level_never_in_the_payload(monkeypatch):
    capture = {}
    _install_fake_post(monkeypatch, fake_response=_FakeResponse(201, {
        "success": True, "event_id": "evt-v", "data_epoch": 0, "data_version": 0, "trainable": True}), capture=capture)
    result = featrix_post_event(auth_key_id="fx_test_key", event_group_id="g", event_payload={"a": 1}, data_version=0)
    assert capture['json']["data_version"] == 0  # 0 is a real version, not "absent"
    assert capture['json']["event_payload"] == {"a": 1}
    assert result["trainable"] is True


def test_success_201_is_also_treated_as_success(monkeypatch):
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(201, {"success": True, "event_id": "evt-2"}),
    )

    result = featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="22222222-2222-2222-2222-222222222222",
        event_payload={},
    )

    assert result == {"success": True, "event_id": "evt-2"}


def test_custom_base_url_is_used(monkeypatch):
    capture = {}
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(200, {"success": True}),
        capture=capture,
    )

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="33333333-3333-3333-3333-333333333333",
        event_payload={},
        base_url="https://custom.example.com",
    )

    assert capture['url'] == "https://custom.example.com/events/ingest"


def test_trailing_slash_on_base_url_is_stripped(monkeypatch):
    capture = {}
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(200, {"success": True}),
        capture=capture,
    )

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="44444444-4444-4444-4444-444444444444",
        event_payload={},
        base_url="https://custom.example.com/",
    )

    assert capture['url'] == "https://custom.example.com/events/ingest"


def test_env_var_fallback_when_base_url_not_passed(monkeypatch):
    capture = {}
    monkeypatch.setenv("FEATRIX_BASE_URL", "https://env.example.com")
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(200, {"success": True}),
        capture=capture,
    )

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="55555555-5555-5555-5555-555555555555",
        event_payload={},
    )

    assert capture['url'] == "https://env.example.com/events/ingest"


def test_default_base_url_when_no_override_and_no_env(monkeypatch):
    capture = {}
    monkeypatch.delenv("FEATRIX_BASE_URL", raising=False)
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(200, {"success": True}),
        capture=capture,
    )

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="66666666-6666-6666-6666-666666666666",
        event_payload={},
    )

    assert capture['url'] == f"{DEFAULT_BASE_URL}/events/ingest"


def test_custom_timeout_is_passed_through(monkeypatch):
    capture = {}
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(200, {"success": True}),
        capture=capture,
    )

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="77777777-7777-7777-7777-777777777777",
        event_payload={},
        timeout=5.0,
    )

    assert capture['timeout'] == 5.0


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------

def test_non_2xx_with_json_error_body_raises_with_parsed_message(monkeypatch):
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(400, {"error": "event_group_id must be a valid UUID"}, text='{"error": "event_group_id must be a valid UUID"}'),
    )

    try:
        featrix_post_event(
            auth_key_id="fx_test_key",
            event_group_id="not-a-uuid",
            event_payload={},
        )
        assert False, "expected FeatrixEventError"
    except FeatrixEventError as e:
        assert e.status_code == 400
        assert "event_group_id must be a valid UUID" in str(e)
        assert e.response_body == '{"error": "event_group_id must be a valid UUID"}'


def test_non_2xx_with_non_json_body_falls_back_to_raw_text(monkeypatch):
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(500, json_data=None, text="Internal Server Error"),
    )

    try:
        featrix_post_event(
            auth_key_id="fx_test_key",
            event_group_id="88888888-8888-8888-8888-888888888888",
            event_payload={},
        )
        assert False, "expected FeatrixEventError"
    except FeatrixEventError as e:
        assert e.status_code == 500
        assert "Internal Server Error" in str(e)
        assert e.response_body == "Internal Server Error"


def test_error_json_body_missing_error_key_falls_back_to_text(monkeypatch):
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(403, {"detail": "forbidden"}, text='{"detail": "forbidden"}'),
    )

    try:
        featrix_post_event(
            auth_key_id="fx_test_key",
            event_group_id="99999999-9999-9999-9999-999999999999",
            event_payload={},
        )
        assert False, "expected FeatrixEventError"
    except FeatrixEventError as e:
        assert e.status_code == 403
        # No "error" key in the JSON body -> falls back to raw response text.
        assert e.response_body in str(e)


def test_connection_error_is_wrapped(monkeypatch):
    _install_fake_post(monkeypatch, exc=requests.ConnectionError("refused"))

    try:
        featrix_post_event(
            auth_key_id="fx_test_key",
            event_group_id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            event_payload={},
        )
        assert False, "expected FeatrixEventError"
    except FeatrixEventError as e:
        assert "Connection error" in str(e)
        assert e.status_code is None


def test_timeout_is_wrapped(monkeypatch):
    _install_fake_post(monkeypatch, exc=requests.Timeout("timed out"))

    try:
        featrix_post_event(
            auth_key_id="fx_test_key",
            event_group_id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            event_payload={},
            timeout=2.5,
        )
        assert False, "expected FeatrixEventError"
    except FeatrixEventError as e:
        assert "timed out after 2.5s" in str(e)
        assert e.status_code is None


# ---------------------------------------------------------------------------
# FeatrixEventSectionObject
# ---------------------------------------------------------------------------

class _JobSection(FeatrixEventSectionObject):
    def __init__(self, session_id, job_id):
        self.session_id = session_id
        self.job_id = job_id

    def to_event_fields(self):
        return {"session_id": self.session_id, "job_id": self.job_id}


class _MetricsSection(FeatrixEventSectionObject):
    def __init__(self, **fields):
        self._fields = fields

    def to_event_fields(self):
        return dict(self._fields)


def test_section_objects_are_merged_into_one_payload(monkeypatch):
    capture = {}
    _install_fake_post(
        monkeypatch,
        fake_response=_FakeResponse(200, {"success": True}),
        capture=capture,
    )

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="cccccccc-cccc-cccc-cccc-cccccccccccc",
        event_payload=[
            _JobSection(session_id="s1", job_id="j1"),
            _MetricsSection(peak_gpu_mb=1024, oom=False),
        ],
    )

    assert capture['json']["event_payload"] == {
        "session_id": "s1",
        "job_id": "j1",
        "peak_gpu_mb": 1024,
        "oom": False,
    }


def test_section_objects_reused_across_multiple_calls(monkeypatch):
    """The whole point: build a section once, reuse it at many call sites."""
    capture_1, capture_2 = {}, {}
    job_ctx = _JobSection(session_id="s1", job_id="j1")

    _install_fake_post(monkeypatch, fake_response=_FakeResponse(200, {"success": True}), capture=capture_1)
    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="dddddddd-dddd-dddd-dddd-dddddddddddd",
        event_payload=[job_ctx, _MetricsSection(step=1)],
    )

    _install_fake_post(monkeypatch, fake_response=_FakeResponse(200, {"success": True}), capture=capture_2)
    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="dddddddd-dddd-dddd-dddd-dddddddddddd",
        event_payload=[job_ctx, _MetricsSection(step=2)],
    )

    assert capture_1['json']["event_payload"] == {"session_id": "s1", "job_id": "j1", "step": 1}
    assert capture_2['json']["event_payload"] == {"session_id": "s1", "job_id": "j1", "step": 2}


def test_section_objects_with_duplicate_field_raises(monkeypatch):
    _install_fake_post(monkeypatch, fake_response=_FakeResponse(200, {"success": True}))

    try:
        featrix_post_event(
            auth_key_id="fx_test_key",
            event_group_id="eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
            event_payload=[
                _MetricsSection(step=1),
                _MetricsSection(step=2),
            ],
        )
        assert False, "expected FeatrixEventError for duplicate field"
    except FeatrixEventError as e:
        assert "step" in str(e)


def test_section_objects_wrong_type_raises_type_error(monkeypatch):
    _install_fake_post(monkeypatch, fake_response=_FakeResponse(200, {"success": True}))

    try:
        featrix_post_event(
            auth_key_id="fx_test_key",
            event_group_id="ffffffff-ffff-ffff-ffff-ffffffffffff",
            event_payload=[{"not": "a section object"}],
        )
        assert False, "expected TypeError"
    except TypeError as e:
        assert "FeatrixEventSectionObject" in str(e)


def test_plain_dict_payload_still_works_unchanged(monkeypatch):
    """Backward compatibility: existing dict-based callers are unaffected."""
    capture = {}
    _install_fake_post(monkeypatch, fake_response=_FakeResponse(200, {"success": True}), capture=capture)

    featrix_post_event(
        auth_key_id="fx_test_key",
        event_group_id="00000000-0000-0000-0000-000000000000",
        event_payload={"action": "click"},
    )

    assert capture['json']["event_payload"] == {"action": "click"}


def test_section_object_missing_to_event_fields_cannot_be_instantiated():
    class _Incomplete(FeatrixEventSectionObject):
        pass

    try:
        _Incomplete()
        assert False, "expected TypeError for missing to_event_fields implementation"
    except TypeError:
        pass


# ---------------------------------------------------------------------------
# featrix_update_event
# ---------------------------------------------------------------------------

def test_update_event_puts_full_payload_to_event_url(monkeypatch):
    from featrixevents import featrix_update_event
    capture = {}

    def _fake_put(url, json=None, headers=None, timeout=None):
        capture.update(url=url, json=json, headers=headers)
        return _FakeResponse(200, {"success": True, "event_id": "evt-1"})

    monkeypatch.setattr(requests, "put", _fake_put)
    result = featrix_update_event(
        event_id="evt-1",
        event_payload={"peak_gpu_mb": 4200.0},
        customer_metadata={"label_status": "final"},
        auth_key_id="fx_test",
        base_url="https://example.test/",
    )
    assert result == {"success": True, "event_id": "evt-1"}
    assert capture["url"] == "https://example.test/events/evt-1"
    assert capture["json"] == {"event_payload": {"peak_gpu_mb": 4200.0},
                               "customer_metadata": {"label_status": "final"}}
    assert capture["headers"]["X-Api-Key"] == "fx_test"


def test_update_event_404_raises_with_status(monkeypatch):
    from featrixevents import featrix_update_event
    monkeypatch.setattr(requests, "put", lambda url, json=None, headers=None, timeout=None:
                        _FakeResponse(404, {"error": "No updatable event evt-1 in your organization"}))
    with pytest.raises(FeatrixEventError) as info:
        featrix_update_event(event_id="evt-1", event_payload={"a": 1}, auth_key_id="fx_test",
                             base_url="https://example.test")
    assert info.value.status_code == 404
    assert "Event update failed (HTTP 404)" in str(info.value)
