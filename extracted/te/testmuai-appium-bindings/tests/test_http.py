"""request_with_retry — the shared HTTP client every v16-server/LT call goes through.

Every helper in the package routes through it, so the retry policy pinned here
decides which requests may be re-sent after a lost reply.
"""
import httpx
import pytest
import respx
from tenacity import wait_none

from testmu_appium._helpers import _http
from testmu_appium._helpers._http import (
    TransientHTTPError, auth, headers, request_with_retry,
)

_URL = "https://api.example.test/thing"


@pytest.fixture(autouse=True)
def _no_backoff(monkeypatch):
    """Retries are exercised for their COUNT, not their timing."""
    monkeypatch.setattr(_http, "_RETRY_WAIT", wait_none())


class TestRetryBudget:
    """Bounded at three attempts. An unbounded client turns one bad gateway into a
    stampede, and a mobile session's calls are not free."""

    def test_the_documented_attempt_ceiling_is_three(self):
        assert _http.MAX_ATTEMPTS == 3

    @respx.mock
    def test_a_transient_status_is_retried_up_to_the_ceiling(self):
        route = respx.get(_URL).mock(return_value=httpx.Response(503, text="down"))
        with pytest.raises(TransientHTTPError):
            request_with_retry("GET", _URL)
        assert route.call_count == _http.MAX_ATTEMPTS

    @respx.mock
    def test_a_transport_error_is_retried_up_to_the_ceiling(self):
        route = respx.get(_URL).mock(side_effect=httpx.ConnectError("refused"))
        with pytest.raises(httpx.ConnectError):
            request_with_retry("GET", _URL)
        assert route.call_count == _http.MAX_ATTEMPTS

    @respx.mock
    def test_a_recovering_call_stops_retrying_as_soon_as_it_succeeds(self):
        route = respx.get(_URL).mock(
            side_effect=[httpx.Response(503), httpx.Response(200, json={"ok": True})]
        )
        assert request_with_retry("GET", _URL).status_code == 200
        assert route.call_count == 2

    @respx.mock
    def test_the_original_exception_is_reraised_not_a_retry_wrapper(self):
        respx.get(_URL).mock(side_effect=httpx.ConnectError("refused"))
        with pytest.raises(httpx.ConnectError) as exc:
            request_with_retry("GET", _URL)
        assert "refused" in str(exc.value)

    @pytest.mark.parametrize("status", sorted(_http.TRANSIENT_HTTP_STATUS_CODES))
    @respx.mock
    def test_every_documented_transient_status_retries(self, status):
        route = respx.get(_URL).mock(return_value=httpx.Response(status))
        with pytest.raises(TransientHTTPError):
            request_with_retry("GET", _URL)
        assert route.call_count == _http.MAX_ATTEMPTS


class TestFourXxIsNotRetried:
    """A 404 from /api/v1/autoheal is an authoritative "no match" — the server's
    answer, not a hiccup. Retrying it would burn two more round trips per heal and
    still get the same verdict."""

    @pytest.mark.parametrize("status", [400, 401, 403, 404, 409, 422, 500, 501])
    @respx.mock
    def test_a_non_transient_status_is_returned_after_one_attempt(self, status):
        route = respx.get(_URL).mock(return_value=httpx.Response(status, text="nope"))
        response = request_with_retry("GET", _URL)
        assert response.status_code == status
        assert route.call_count == 1

    @respx.mock
    def test_a_404_is_returned_rather_than_raised(self):
        respx.get(_URL).mock(return_value=httpx.Response(404, json={"detail": "no_match"}))
        assert request_with_retry("GET", _URL).status_code == 404

    @respx.mock
    def test_a_success_makes_exactly_one_request(self):
        route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
        request_with_retry("GET", _URL)
        assert route.call_count == 1


class TestNonIdempotentMethodsAreNotResent:
    """A read error means the request WAS sent and the reply was lost. Re-sending a
    POST/PUT/PATCH/DELETE on that evidence duplicates a side effect the server may
    already have applied — a second row, a second charge, a second delete.

    Connect errors are different: the connection never opened, so nothing was sent,
    and every method stays retryable.
    """

    RESPONSE_ERRORS = [httpx.ReadError, httpx.RemoteProtocolError]
    CONNECT_ERRORS = [httpx.ConnectError, httpx.ConnectTimeout]
    NON_IDEMPOTENT = ["POST", "PUT", "PATCH", "DELETE"]
    IDEMPOTENT = ["GET", "HEAD", "OPTIONS"]

    @pytest.mark.parametrize("method", NON_IDEMPOTENT)
    @pytest.mark.parametrize("error", RESPONSE_ERRORS)
    @respx.mock
    def test_a_read_error_is_not_resent_for_a_non_idempotent_method(self, method, error):
        route = respx.route(method=method, url=_URL).mock(side_effect=error("lost"))
        with pytest.raises(error):
            request_with_retry(method, _URL)
        assert route.call_count == 1, "the request may already have been applied"

    @pytest.mark.parametrize("method", IDEMPOTENT)
    @pytest.mark.parametrize("error", RESPONSE_ERRORS)
    @respx.mock
    def test_a_read_error_is_still_retried_for_an_idempotent_method(self, method, error):
        route = respx.route(method=method, url=_URL).mock(side_effect=error("lost"))
        with pytest.raises(error):
            request_with_retry(method, _URL)
        assert route.call_count == _http.MAX_ATTEMPTS

    @pytest.mark.parametrize("method", NON_IDEMPOTENT + IDEMPOTENT)
    @pytest.mark.parametrize("error", CONNECT_ERRORS)
    @respx.mock
    def test_a_connect_error_is_retried_for_every_method(self, method, error):
        route = respx.route(method=method, url=_URL).mock(side_effect=error("refused"))
        with pytest.raises(error):
            request_with_retry(method, _URL)
        assert route.call_count == _http.MAX_ATTEMPTS

    @pytest.mark.parametrize("method", NON_IDEMPOTENT)
    @respx.mock
    def test_a_transient_status_is_still_retried_for_every_method(self, method):
        """A 503 is the server declining before doing the work — no side effect to
        duplicate, so the status-based retry is unaffected by idempotency."""
        route = respx.route(method=method, url=_URL).mock(return_value=httpx.Response(503))
        with pytest.raises(TransientHTTPError):
            request_with_retry(method, _URL)
        assert route.call_count == _http.MAX_ATTEMPTS

    def test_the_method_case_does_not_change_the_policy(self):
        assert _http._is_non_idempotent("post") is True
        assert _http._is_non_idempotent("POST") is True
        assert _http._is_non_idempotent("get") is False


class TestRequestShape:
    @respx.mock
    def test_json_data_is_sent_as_a_json_body(self):
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        request_with_retry("POST", _URL, json_data={"a": 1})
        assert route.calls[0].request.headers["content-type"] == "application/json"

    @respx.mock
    def test_a_string_body_is_sent_as_content(self):
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        request_with_retry("POST", _URL, data="raw body")
        assert route.calls[0].request.content == b"raw body"

    @respx.mock
    def test_params_reach_the_query_string(self):
        route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
        request_with_retry("GET", _URL, params={"page": "2"})
        assert route.calls[0].request.url.params["page"] == "2"

    @respx.mock
    def test_auth_reaches_the_authorization_header(self):
        route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
        request_with_retry("GET", _URL, auth=("u", "k"))
        assert route.calls[0].request.headers["authorization"].startswith("Basic ")

    @respx.mock
    def test_the_timeout_is_applied_per_attempt(self):
        """Documented semantics: `timeout` is the httpx client timeout, so it bounds
        ONE attempt. Worst-case wall clock is attempts x timeout, plus backoff."""
        seen = []
        route = respx.get(_URL).mock(
            side_effect=[httpx.Response(503), httpx.Response(200, json={})]
        )
        original = httpx.Client.__init__

        def _record(self, *args, **kwargs):
            seen.append(kwargs.get("timeout"))
            return original(self, *args, **kwargs)

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(httpx.Client, "__init__", _record)
            request_with_retry("GET", _URL, timeout=7)
        assert route.call_count == 2
        assert seen == [7, 7], "each attempt gets the full timeout, not a share of it"

    @respx.mock
    def test_a_total_timeout_is_shared_across_attempts(self, monkeypatch):
        route = respx.get(_URL).mock(
            side_effect=[httpx.Response(503), httpx.Response(200, json={})]
        )
        ticks = iter([10.0, 10.1, 10.2, 10.4, 10.5, 10.6])
        monkeypatch.setattr(_http, "_monotonic", lambda: next(ticks))
        seen = []
        original = httpx.Client.__init__

        def _record(self, *args, **kwargs):
            seen.append(kwargs.get("timeout"))
            return original(self, *args, **kwargs)

        monkeypatch.setattr(httpx.Client, "__init__", _record)
        assert request_with_retry(
            "GET", _URL, timeout=7, total_timeout_s=1
        ).status_code == 200
        assert route.call_count == 2
        assert 0 < seen[1] < seen[0] <= 1

    @respx.mock
    def test_an_exhausted_total_timeout_sends_nothing(self, monkeypatch):
        route = respx.get(_URL).mock(return_value=httpx.Response(200))
        ticks = iter([10.0, 11.1])
        monkeypatch.setattr(_http, "_monotonic", lambda: next(ticks))
        with pytest.raises(httpx.TimeoutException, match="budget exhausted"):
            request_with_retry("GET", _URL, total_timeout_s=1)
        assert route.call_count == 0


class TestSharedHeadersAndAuth:
    def test_auth_is_none_without_both_credentials(self, monkeypatch):
        monkeypatch.delenv("LT_USERNAME", raising=False)
        monkeypatch.setenv("LT_ACCESS_KEY", "k")
        assert auth() is None

    def test_auth_is_the_credential_pair_when_both_are_present(self, monkeypatch):
        monkeypatch.setenv("LT_USERNAME", "u")
        monkeypatch.setenv("LT_ACCESS_KEY", "k")
        assert auth() == ("u", "k")

    def test_accept_encoding_excludes_brotli(self):
        """A brotli-capable client negotiated br with the gateway and got bogus 400s."""
        assert "br" not in headers()["Accept-Encoding"]

    def test_the_session_id_header_is_omitted_when_unset(self, monkeypatch):
        monkeypatch.delenv("TESTMUAI_SESSION_ID", raising=False)
        assert "x-session-id" not in headers()

    def test_the_session_id_header_is_present_when_set(self, monkeypatch):
        monkeypatch.setenv("TESTMUAI_SESSION_ID", "sess-1")
        assert headers()["x-session-id"] == "sess-1"
