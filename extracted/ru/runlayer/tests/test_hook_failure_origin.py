"""Response-origin classification for relay failures.

The relay must tell a Runlayer-produced 4xx from one an intermediary (AWS WAF
IP-allowlist block, ALB error page, corporate proxy) answered, because the
two get different deny wording and only Runlayer's 401 may touch credential
state. Shapes below are captured live: an AWS WAF block page vs the Runlayer
backend's JSON error envelope.
"""

from __future__ import annotations

import httpx
import pytest

from runlayer_cli.hook.failure import (
    ORIGIN_HEADER_NAME,
    REQUEST_ID_HEADER_NAME,
    classify_response_origin,
)

_WAF_BODY = (
    "<html>\r\n<head><title>403 Forbidden</title></head>\r\n"
    "<body>\r\n<center><h1>403 Forbidden</h1></center>\r\n</body>\r\n</html>\r\n"
)
_REQ_ID = "785aa763-a5a4-45b7-9232-4f38434910c5"


def _resp(status: int, text: str, headers: dict[str, str]) -> httpx.Response:
    return httpx.Response(status, text=text, headers=headers)


class TestIntermediary:
    def test_waf_block_page_is_intermediary(self):
        info = classify_response_origin(
            _resp(403, _WAF_BODY, {"server": "awselb/2.0", "content-type": "text/html"})
        )
        assert info.origin == "intermediary"
        assert info.request_id is None
        assert info.detail is None

    def test_json_envelope_without_request_id_is_not_enough(self):
        """Any hop can answer JSON; only the backend also stamps a request id."""
        info = classify_response_origin(_resp(403, '{"detail": "Forbidden"}', {}))
        assert info.origin == "intermediary"

    def test_request_id_without_envelope_is_not_enough(self):
        """Proxies add request-id headers of their own; with an HTML body the
        answer did not come from the backend's error handler."""
        info = classify_response_origin(
            _resp(401, _WAF_BODY, {REQUEST_ID_HEADER_NAME: _REQ_ID})
        )
        assert info.origin == "intermediary"

    @pytest.mark.parametrize("text", ["", "not json", "[]", '{"error": "x"}', "{"])
    def test_non_envelope_bodies_are_intermediary(self, text: str):
        info = classify_response_origin(
            _resp(403, text, {REQUEST_ID_HEADER_NAME: _REQ_ID})
        )
        assert info.origin == "intermediary"

    def test_deeply_nested_body_is_not_an_envelope(self):
        """``json.loads`` raises RecursionError, not ValueError, on this;
        classification must still answer instead of turning the deny into
        a transport error."""
        info = classify_response_origin(
            _resp(401, '{"detail": ' + "[" * 20000, {REQUEST_ID_HEADER_NAME: _REQ_ID})
        )
        assert info.origin == "intermediary"


class TestUnclassified:
    def test_response_without_headers_is_unclassified_not_intermediary(self):
        """A transport that exposes no headers cannot be told apart, and the
        safe default is the pre-classification behaviour (treated as
        Runlayer), never a network deny that skips credential handling."""
        assert classify_response_origin(object()).origin is None
        assert classify_response_origin(None).origin is None

    def test_broken_headers_object_is_unclassified(self):
        class _Weird:
            text = '{"detail": "x"}'

            @property
            def headers(self):
                return 42

        assert classify_response_origin(_Weird()).origin is None


class TestRunlayer:
    def test_origin_header_alone_is_contractual(self):
        """Backends that stamp the marker: it decides regardless of body."""
        info = classify_response_origin(
            _resp(
                403,
                "",
                {ORIGIN_HEADER_NAME: "backend", REQUEST_ID_HEADER_NAME: _REQ_ID},
            )
        )
        assert info.origin == "runlayer"
        assert info.request_id == _REQ_ID
        assert info.detail is None

    def test_legacy_backend_request_id_plus_envelope(self):
        info = classify_response_origin(
            _resp(
                401,
                '{"detail": "Invalid token encoding"}',
                {REQUEST_ID_HEADER_NAME: _REQ_ID},
            )
        )
        assert info.origin == "runlayer"
        assert info.request_id == _REQ_ID
        assert info.detail == "Invalid token encoding"

    def test_header_lookup_is_case_insensitive(self):
        info = classify_response_origin(
            _resp(
                403,
                '{"detail": "x"}',
                {"x-request-id": _REQ_ID, "x-runlayer-origin": "backend"},
            )
        )
        assert info.origin == "runlayer"
        assert info.request_id == _REQ_ID

    def test_list_detail_proves_envelope_but_is_not_rendered(self):
        """422 bodies carry a list detail: still the backend's envelope, but
        only a string detail is safe to put in the deny text."""
        info = classify_response_origin(
            _resp(
                422,
                '{"detail": [{"loc": ["body"], "type": "missing"}]}',
                {REQUEST_ID_HEADER_NAME: _REQ_ID},
            )
        )
        assert info.origin == "runlayer"
        assert info.detail is None

    def test_detail_is_sanitized_and_bounded(self):
        long = "x" * 500
        info = classify_response_origin(
            _resp(
                403,
                '{"detail": "a\\tb\\u0000c ' + long + '"}',
                {REQUEST_ID_HEADER_NAME: _REQ_ID},
            )
        )
        assert info.detail is not None
        assert "\t" not in info.detail and "\x00" not in info.detail
        assert info.detail.startswith("a b c")
        assert len(info.detail) <= 200

    def test_malformed_request_id_is_dropped_but_origin_kept(self):
        """The id is echoed into the deny text, so only a plain token shape
        is accepted; a weird value must not flip the origin decision."""
        info = classify_response_origin(
            _resp(
                403,
                '{"detail": "x"}',
                {
                    ORIGIN_HEADER_NAME: "backend",
                    REQUEST_ID_HEADER_NAME: "bad id with spaces <b>",
                },
            )
        )
        assert info.origin == "runlayer"
        assert info.request_id is None
