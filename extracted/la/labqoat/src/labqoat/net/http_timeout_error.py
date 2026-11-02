"""A request whose connection or answer took longer than allowed."""

from labqoat.net.http_error import HttpError


class HttpTimeoutError(HttpError):
    """Connecting, sending or waiting for the next bytes of the answer exceeded its timeout."""
