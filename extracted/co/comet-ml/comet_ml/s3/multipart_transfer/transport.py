# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
"""The HTTP client that moves part bytes to and from presigned S3 URLs.

Only the data plane goes through here: one PUT per uploaded part, one GET per
downloaded range. The calls into Comet's own API around them (upload start and
complete) are not S3 requests, carry Comet's credentials, and stay on the Comet
session.

The interface is narrow on purpose, so that a client other than requests can stand
behind it without the retry loops, the throttle gate or the resume logic noticing.
Whatever implements it must keep these promises:

* No Comet headers are sent. These requests go to S3, not to Comet.
* No transport-level retries. Retrying is owned by the callers, which count
  attempts, back off and share a throttle gate across every part in the process.
* A PUT body is sent with a Content-Length, never chunked, because S3 rejects a
  chunked body on a presigned PUT. The body is either bytes or a file-like object
  with ``__len__``, ``read`` and ``rewind``; the callers rewind it before a retry.
* A GET body is handed over exactly as stored, without undoing any
  Content-Encoding, because a range is a range of the stored object.
* A network failure is raised as ``ConnectionError`` or one of the requests
  exceptions the callers already treat as network errors.
"""
import logging
import threading
from typing import Any, Callable, Iterator, Mapping, Optional, Protocol, Set, cast

import requests

from ...config import Config, get_config
from ...connection import http_session

LOGGER = logging.getLogger(__name__)

SessionProvider = Callable[[], requests.Session]

HTTP_CLIENT_CONFIG_KEY = "comet.s3_multipart.http_client"
HTTP_CLIENT_REQUESTS = "requests"
HTTP_CLIENT_PYREQWEST = "pyreqwest"


class TransportResponse(Protocol):
    """An answer from S3, to a part PUT or a ranged GET.

    Implementations subclass it explicitly, so that mypy checks them where they are
    defined. Every member raises NotImplementedError here, so that one an
    implementation forgot fails at the call rather than quietly returning None.
    """

    @property
    def status_code(self) -> int:
        """The HTTP status."""
        raise NotImplementedError

    @property
    def headers(self) -> Mapping[str, str]:
        """Case-insensitive, as HTTP header names are."""
        raise NotImplementedError

    @property
    def text(self) -> str:
        """The whole body as text. Only for a response that was not streamed."""
        raise NotImplementedError

    def iter_raw(self, chunk_size: int) -> Iterator[bytes]:
        """The body of a streamed response, as stored: no content decoding.

        In blocks of about ``chunk_size``. When the connection fails, every byte
        that arrived is handed over before the error is raised, so a range can
        resume from the first byte that did not.
        """
        raise NotImplementedError

    def read_error_text(self, limit: int = 1024) -> str:
        """At most the first ``limit`` bytes of an error body, as text, or "".

        For logging only. An error from S3 is a short XML document, but whatever
        else answers with an error status could send an arbitrarily large one.
        """
        raise NotImplementedError

    def close(self) -> None:
        """Releases the connection. Safe to call more than once."""
        raise NotImplementedError


class S3Transport(Protocol):
    """Sends part PUTs and ranged GETs to presigned S3 URLs.

    Shared by every thread of a parts pool, so implementations must be safe to call
    concurrently. Subclassed explicitly, like TransportResponse.
    """

    def put(self, url: str, body: Any) -> TransportResponse:
        """Uploads one part. The response is read in full before returning."""
        raise NotImplementedError

    def get(
        self, url: str, headers: Mapping[str, str], timeout: Optional[float]
    ) -> TransportResponse:
        """Opens a GET whose body is streamed. The caller must close the response.

        ``timeout`` applies to connecting and to each read, not to the whole body.
        """
        raise NotImplementedError


class RequestsResponse(TransportResponse):
    """A requests response behind TransportResponse."""

    __slots__ = ["_response"]

    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def status_code(self) -> int:
        return cast(int, self._response.status_code)

    @property
    def headers(self) -> Mapping[str, str]:
        return cast(Mapping[str, str], self._response.headers)

    @property
    def text(self) -> str:
        return cast(str, self._response.text)

    def iter_raw(self, chunk_size: int) -> Iterator[bytes]:
        # The raw urllib3 stream, because iter_content() would decode the body.
        stream = self._response.raw.stream(chunk_size, decode_content=False)
        return cast(Iterator[bytes], stream)

    def read_error_text(self, limit: int = 1024) -> str:
        try:
            head = self._response.raw.read(limit, decode_content=True)
            return cast(bytes, head).decode("utf-8", errors="replace")
        except Exception:
            return ""

    def close(self) -> None:
        self._response.close()

    def __repr__(self) -> str:
        return "RequestsResponse(%r)" % self._response


class RequestsTransport(S3Transport):
    """The transport built on requests, as every S3 transfer has used so far.

    Each thread gets its own session, cached for the life of the thread, so every
    worker of a parts pool keeps one connection and reuses it across the parts it
    transfers.
    """

    def __init__(
        self,
        verify_tls: bool = True,
        session_provider: Optional[SessionProvider] = None,
    ):
        """``session_provider`` replaces the cached sessions; tests use it to fake S3."""
        if session_provider is None:
            session_provider = _cached_session_provider(verify_tls)
        self._session_provider = session_provider

    def put(self, url: str, body: Any) -> TransportResponse:
        # requests takes the Content-Length from len(body), which bytes and
        # FileRangeReader both provide, so neither is sent chunked.
        response = self._session_provider().request(
            method="PUT", url=url, json=None, data=body, headers=None
        )
        return RequestsResponse(response)

    def get(
        self, url: str, headers: Mapping[str, str], timeout: Optional[float]
    ) -> TransportResponse:
        response = self._session_provider().get(
            url, headers=headers, stream=True, timeout=timeout
        )
        return RequestsResponse(response)


def _cached_session_provider(verify_tls: bool) -> SessionProvider:
    def provider() -> requests.Session:
        return http_session.get_cached_http_session(
            retry=False, verify_tls=verify_tls, tcp_keep_alive=False
        )

    return provider


def get_s3_transport(
    verify_tls: bool = True, config: Optional[Config] = None
) -> S3Transport:
    """The transport for direct S3 transfers, as comet.s3_multipart.http_client says.

    requests unless pyreqwest is asked for. When it is but cannot be used, because
    it is not installed or the Python version is older than 3.11, this warns once
    and returns the requests transport, so a setting copied between environments
    never stops a transfer.
    """
    if config is None:
        config = get_config()

    http_client = str(
        config.get_string(None, HTTP_CLIENT_CONFIG_KEY) or HTTP_CLIENT_REQUESTS
    )
    http_client = http_client.strip().lower()

    if http_client == HTTP_CLIENT_PYREQWEST:
        try:
            from . import pyreqwest_transport
        except ImportError as ex:
            warn_once(
                "pyreqwest-import",
                "%s is set to %r, but pyreqwest cannot be imported (%s). It needs "
                "Python 3.11 or later: pip install comet_ml[fast-transfer]. Using "
                "requests for direct S3 transfers.",
                HTTP_CLIENT_CONFIG_KEY,
                HTTP_CLIENT_PYREQWEST,
                ex,
            )
        else:
            return pyreqwest_transport.PyreqwestTransport(
                verify_tls=verify_tls,
                custom_ca_bundle=config["comet.include.custom_ca_bundle"],
            )
    elif http_client != HTTP_CLIENT_REQUESTS:
        warn_once(
            "unknown-http-client",
            "Unknown value %r for %s, expected %r or %r. Using requests for direct "
            "S3 transfers.",
            http_client,
            HTTP_CLIENT_CONFIG_KEY,
            HTTP_CLIENT_REQUESTS,
            HTTP_CLIENT_PYREQWEST,
        )

    return RequestsTransport(verify_tls=verify_tls)


_warned: Set[str] = set()
_warned_lock = threading.Lock()


def warn_once(key: str, message: str, *args: Any, level: int = logging.WARNING) -> None:
    """Logs ``message`` the first time ``key`` is seen in this process.

    For problems with the setup, which would otherwise repeat for every asset.
    """
    with _warned_lock:
        if key in _warned:
            return
        _warned.add(key)
    LOGGER.log(level, message, *args)
