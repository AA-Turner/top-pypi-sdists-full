"""Tests for the sanitized exception -> flow error-category classifier."""

import asyncio
import socket
import ssl
import sys

import httpx
import pytest

if sys.version_info >= (3, 11):
    import builtins

    _ExceptionGroup = builtins.BaseExceptionGroup
else:  # pragma: no cover - py3.10 backport (dep of anyio)
    from exceptiongroup import BaseExceptionGroup as _ExceptionGroup
from fastmcp.exceptions import ToolError
from mcp.client.auth import OAuthFlowError, OAuthRegistrationError, OAuthTokenError
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData

from runlayer_cli.error_classification import classify_exception
from runlayer_cli.flow_contract import CLIENT_FLOW_ERROR_CATEGORIES
from runlayer_cli.oauth import OAuthCallbackTimeoutError

SECRET = "hunter2-super-secret"


def _http_status_error(status_code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("GET", f"https://example.com/mcp?token={SECRET}")
    response = httpx.Response(status_code, request=request, text=f"body with {SECRET}")
    return httpx.HTTPStatusError(
        f"error with {SECRET}", request=request, response=response
    )


class TestSingleExceptions:
    @pytest.mark.parametrize(
        ("status_code", "category"),
        [
            (401, "http_401"),
            (403, "http_403"),
            (404, "http_404"),
            (422, "http_4xx"),
            (429, "http_4xx"),
            (500, "http_5xx"),
            (503, "http_5xx"),
        ],
    )
    def test_http_status_errors(self, status_code, category):
        assert classify_exception(_http_status_error(status_code)) == (
            category,
            status_code,
        )

    def test_http_3xx_is_other_with_status(self):
        assert classify_exception(_http_status_error(302)) == ("other", 302)

    def test_connect_timeout(self):
        assert classify_exception(httpx.ConnectTimeout(SECRET)) == (
            "connect_timeout",
            None,
        )

    @pytest.mark.parametrize(
        "exc",
        [httpx.ReadTimeout(SECRET), httpx.WriteTimeout(SECRET), httpx.PoolTimeout("")],
    )
    def test_other_httpx_timeouts(self, exc):
        assert classify_exception(exc) == ("timeout", None)

    def test_builtin_timeout(self):
        assert classify_exception(TimeoutError(SECRET)) == ("timeout", None)

    def test_dns_failure_under_connect_error(self):
        try:
            raise socket.gaierror(8, "nodename nor servname provided")
        except socket.gaierror as cause:
            exc = httpx.ConnectError(SECRET)
            exc.__cause__ = cause
        assert classify_exception(exc) == ("dns", None)

    def test_tls_failure_under_connect_error(self):
        exc = httpx.ConnectError(SECRET)
        exc.__cause__ = ssl.SSLCertVerificationError("self signed certificate")
        assert classify_exception(exc) == ("tls", None)

    def test_bare_ssl_error(self):
        assert classify_exception(ssl.SSLError(1, SECRET)) == ("tls", None)

    def test_bare_gaierror(self):
        assert classify_exception(socket.gaierror(8, "unknown host")) == ("dns", None)

    def test_plain_connect_error(self):
        assert classify_exception(httpx.ConnectError(SECRET)) == ("connect", None)

    def test_builtin_connection_error(self):
        assert classify_exception(ConnectionRefusedError(SECRET)) == ("connect", None)

    def test_remote_protocol_error_maps_to_connect(self):
        assert classify_exception(httpx.RemoteProtocolError(SECRET)) == (
            "connect",
            None,
        )

    def test_oauth_registration_rejected_on_4xx(self):
        exc = OAuthRegistrationError(f"Registration failed: 403 body with {SECRET}")
        assert classify_exception(exc) == ("oauth_registration_rejected", 403)

    def test_oauth_registration_5xx_is_transient_not_rejected(self):
        """OAuth.async_auth_flow passes 5xx through as likely-transient; a
        rejected classification would wrongly steer support to Manual OAuth."""
        exc = OAuthRegistrationError(f"Registration failed: 502 {SECRET}")
        assert classify_exception(exc) == ("http_5xx", 502)

    def test_oauth_registration_without_status_is_other(self):
        assert classify_exception(OAuthRegistrationError(SECRET)) == ("other", None)

    def test_oauth_callback_timeout(self):
        assert classify_exception(OAuthCallbackTimeoutError(SECRET)) == (
            "oauth_flow_timeout",
            None,
        )

    @pytest.mark.parametrize("exc_type", [OAuthFlowError, OAuthTokenError])
    def test_other_oauth_errors_are_other(self, exc_type):
        assert classify_exception(exc_type(SECRET)) == ("other", None)

    def test_mcp_error(self):
        exc = McpError(ErrorData(code=-32603, message=SECRET))
        assert classify_exception(exc) == ("mcp_protocol", None)

    def test_fastmcp_tool_error(self):
        assert classify_exception(ToolError(SECRET)) == ("mcp_protocol", None)

    def test_cancelled(self):
        assert classify_exception(asyncio.CancelledError()) == ("cancelled", None)

    def test_unknown_exception_is_other(self):
        assert classify_exception(RuntimeError(SECRET)) == ("other", None)


class TestExceptionGroups:
    def test_unwraps_nested_groups(self):
        inner = _ExceptionGroup(
            "inner", [httpx.ConnectError(SECRET), RuntimeError("x")]
        )
        outer = _ExceptionGroup("outer", [inner])
        assert classify_exception(outer) == ("connect", None)

    def test_group_of_unknowns_is_other(self):
        group = _ExceptionGroup("g", [RuntimeError("a"), ValueError("b")])
        assert classify_exception(group) == ("other", None)

    def test_group_behind_cause_is_unwrapped(self):
        """A group reachable only via __cause__ (e.g. RuntimeError raised
        from an anyio task group's ExceptionGroup of transport errors) must
        classify by its leaves, not degrade to `other`."""
        group = _ExceptionGroup(
            "g", [httpx.ConnectError(SECRET), RuntimeError("x")]
        )
        try:
            raise RuntimeError(SECRET) from group
        except RuntimeError as wrapper:
            assert classify_exception(wrapper) == ("connect", None)

    def test_group_behind_context_is_unwrapped(self):
        group = _ExceptionGroup("g", [httpx.ConnectTimeout(SECRET)])
        try:
            try:
                raise group
            except BaseException:
                raise RuntimeError("while handling")  # __context__, no cause
        except RuntimeError as wrapper:
            assert classify_exception(wrapper) == ("connect_timeout", None)

    def test_nested_group_inside_cause_inside_group(self):
        """Nested group behind a cause behind a group: uniform traversal."""
        inner_group = _ExceptionGroup(
            "inner", [_ExceptionGroup("deep", [socket.gaierror(8, "no host")])]
        )
        try:
            raise RuntimeError(SECRET) from inner_group
        except RuntimeError as carrier:
            outer = _ExceptionGroup("outer", [ValueError("v"), carrier])
        assert classify_exception(outer) == ("dns", None)

    def test_cyclic_cause_chain_terminates(self):
        a = RuntimeError("a")
        b = RuntimeError("b")
        a.__cause__ = b
        b.__cause__ = a
        assert classify_exception(a) == ("other", None)


class TestCauseChains:
    """The full classification applies to every exception in the cause chain,
    not just DNS/TLS root-causing — a generic wrapper must not hide the
    diagnostic inner exception."""

    @staticmethod
    def _wrap(inner: BaseException) -> RuntimeError:
        try:
            raise RuntimeError(SECRET) from inner
        except RuntimeError as wrapper:
            return wrapper

    def test_wrapped_http_status_error(self):
        assert classify_exception(self._wrap(_http_status_error(403))) == (
            "http_403",
            403,
        )

    def test_wrapped_connect_timeout(self):
        assert classify_exception(self._wrap(httpx.ConnectTimeout(SECRET))) == (
            "connect_timeout",
            None,
        )

    def test_wrapped_mcp_error(self):
        inner = McpError(ErrorData(code=-32603, message=SECRET))
        assert classify_exception(self._wrap(inner)) == ("mcp_protocol", None)

    def test_implicit_context_chain(self):
        try:
            try:
                raise httpx.ConnectError(SECRET)
            except httpx.ConnectError:
                raise RuntimeError("while handling")  # __context__, no cause
        except RuntimeError as wrapper:
            assert classify_exception(wrapper) == ("connect", None)

    def test_oauth_wrapper_beats_inner_http_status(self):
        """Wrapper-first ordering: the OAuth category is the diagnostic one."""
        try:
            raise OAuthRegistrationError(
                "Registration failed: 403 invalid session"
            ) from _http_status_error(403)
        except OAuthRegistrationError as wrapper:
            assert classify_exception(wrapper) == (
                "oauth_registration_rejected",
                403,
            )

    def test_guidance_rewrapped_registration_error_classifies_via_cause(self):
        """OAuth.async_auth_flow re-raises 4xx rejections with a guidance
        message (no ``Registration failed:`` shape) ``from`` the original —
        the chain walk must still land on the rejection."""
        original = OAuthRegistrationError(f"Registration failed: 403 {SECRET}")
        try:
            raise OAuthRegistrationError("actionable guidance text") from original
        except OAuthRegistrationError as wrapper:
            assert classify_exception(wrapper) == (
                "oauth_registration_rejected",
                403,
            )

    def test_dns_root_cause_beats_connect_wrapper(self):
        try:
            raise httpx.ConnectError(SECRET) from socket.gaierror(8, "no host")
        except httpx.ConnectError as wrapper:
            assert classify_exception(self._wrap(wrapper)) == ("dns", None)


class TestSanitization:
    """Category + optional int status only — message text must never leak."""

    @pytest.mark.parametrize(
        "exc",
        [
            _http_status_error(403),
            httpx.ConnectError(f"https://user:{SECRET}@example.com"),
            RuntimeError(SECRET),
            OAuthRegistrationError(SECRET),
            TimeoutError(SECRET),
        ],
    )
    def test_no_message_text_in_result(self, exc):
        category, http_status = classify_exception(exc)
        assert isinstance(category, str)
        assert category in CLIENT_FLOW_ERROR_CATEGORIES
        assert SECRET not in category
        assert http_status is None or isinstance(http_status, int)

    def test_every_category_is_in_the_closed_vocabulary(self):
        exceptions: list[BaseException] = [
            _http_status_error(401),
            _http_status_error(500),
            httpx.ConnectTimeout(""),
            httpx.ReadTimeout(""),
            httpx.ConnectError(""),
            ssl.SSLError(),
            socket.gaierror(8, "x"),
            OAuthRegistrationError(""),
            OAuthCallbackTimeoutError(""),
            McpError(ErrorData(code=-1, message="x")),
            ToolError(""),
            asyncio.CancelledError(),
            RuntimeError(""),
        ]
        for exc in exceptions:
            category, _ = classify_exception(exc)
            assert category in CLIENT_FLOW_ERROR_CATEGORIES, category
