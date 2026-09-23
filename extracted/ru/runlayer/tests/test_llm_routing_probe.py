"""Device-side gateway reachability probe: any HTTP answer counts, transport failures do not."""

from __future__ import annotations

import email.message
import errno
import http.client
import io
import socket
import urllib.error
import urllib.request
from typing import Any

import pytest

from runlayer_cli import __version__
from runlayer_cli.hook_install import llm_routing


class _Recorder:
    def __init__(self, outcome: object) -> None:
        self.outcome = outcome
        self.request: urllib.request.Request | None = None
        self.timeout: float | None = None

    def __call__(self, request: urllib.request.Request, *, timeout: float) -> Any:
        self.request = request
        self.timeout = timeout
        if isinstance(self.outcome, BaseException):
            raise self.outcome
        return self.outcome


def _http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "https://gw.example.com/anthropic/v1/models",
        code,
        "nope",
        email.message.Message(),
        io.BytesIO(b"{}"),
    )


def test_unauthorized_answer_is_reachable_and_sends_no_credential() -> None:
    urlopen = _Recorder(_http_error(401))

    assert llm_routing.probe_gateway("https://gw.example.com", urlopen=urlopen) is None

    request = urlopen.request
    assert request is not None
    assert request.full_url == "https://gw.example.com/anthropic/v1/models"
    assert request.get_method() == "GET"
    assert not request.has_header("Authorization")
    assert not request.has_header("X-api-key")
    assert request.get_header("User-agent") == f"runlayer-aiwatch/{__version__}"
    assert urlopen.timeout == llm_routing.GATEWAY_PROBE_TIMEOUT_SECONDS == 5.0


def test_success_response_is_reachable() -> None:
    class _Response:
        def __enter__(self) -> _Response:
            return self

        def __exit__(self, *_exc: object) -> None:
            return None

    assert (
        llm_routing.probe_gateway(
            "https://gw.example.com", urlopen=_Recorder(_Response())
        )
        is None
    )


def test_server_error_is_unreachable() -> None:
    # An unauthenticated probe is rejected by the gateway's auth middleware
    # with a 4xx before any provider call, so a 5xx on this path is the ALB
    # (or another middlebox) answering for a gateway that is not there —
    # e.g. the ALB's own 503 when zero targets are healthy.
    assert (
        llm_routing.probe_gateway(
            "https://gw.example.com", urlopen=_Recorder(_http_error(503))
        )
        == "HTTP 503"
    )


def test_trailing_slash_base_url_is_normalized() -> None:
    urlopen = _Recorder(_http_error(404))

    assert llm_routing.probe_gateway("https://gw.example.com/", urlopen=urlopen) is None

    assert urlopen.request is not None
    assert urlopen.request.full_url == "https://gw.example.com/anthropic/v1/models"


@pytest.mark.parametrize(
    ("exc", "prefix"),
    [
        (urllib.error.URLError(ConnectionRefusedError(61, "refused")), "URLError: "),
        (socket.timeout("timed out"), "TimeoutError: "),
        (OSError(errno.ECONNRESET, "reset"), "ConnectionResetError: "),
        (OSError("no route"), "OSError: "),
        (http.client.RemoteDisconnected("closed"), "RemoteDisconnected: "),
    ],
)
def test_transport_failures_are_unreachable(exc: BaseException, prefix: str) -> None:
    reason = llm_routing.probe_gateway(
        "https://gw.example.com", timeout=1.0, urlopen=_Recorder(exc)
    )

    assert reason is not None
    assert reason.startswith(prefix)
    assert any(
        word in reason for word in ("refused", "timed out", "reset", "route", "closed")
    )
