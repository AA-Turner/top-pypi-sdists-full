"""One vocabulary for what can go wrong between sending a request and reading its last byte."""

import http.client
from collections.abc import Iterator
from contextlib import contextmanager

from labqoat.net.http_error import HttpError
from labqoat.net.http_timeout_error import HttpTimeoutError


class Failures:
    """Turn socket, TLS and protocol failures into ``HttpTimeoutError`` or ``HttpError``."""

    @staticmethod
    @contextmanager
    def translated() -> Iterator[None]:
        """Raise a timeout as ``HttpTimeoutError`` and any other transport failure as ``HttpError``."""
        try:
            yield
        except HttpError:
            raise
        except TimeoutError as error:
            raise HttpTimeoutError(f"HTTP request timed out: {error}") from error
        except (OSError, EOFError, http.client.HTTPException) as error:
            raise HttpError(f"HTTP request failed: {type(error).__name__}: {error}") from error
