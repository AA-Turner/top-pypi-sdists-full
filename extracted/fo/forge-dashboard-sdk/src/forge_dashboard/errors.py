"""Typed errors for the forge-dashboard API.

Every 4xx/5xx response forge-dashboard returns shares the same
``{error}`` body (see ``openapi/openapi.yaml``'s ``Error`` schema).
:func:`decode_error` turns that, plus the status code, into a single
:class:`APIError` -- never a bare string or a raw ``httpx.Response``
(rules/sdk-generation.md's "Client shape").
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Protocol


class _ErrorResponse(Protocol):
    """What :func:`decode_error` needs from a response.

    Both ``httpx.Response`` and the generated per-operation
    ``forge_dashboard._generated.types.Response`` satisfy this
    structurally -- decoding works the same whether you call a wrapper
    method or drop down to a generated ``sync_detailed``/``asyncio_detailed``
    call directly. Declared as read-only properties (rather than plain
    attributes) so a subtype's more specific attribute types --
    ``http.HTTPStatus`` for ``status_code``, a ``MutableMapping`` for
    ``headers`` -- still satisfy the protocol; Protocol attribute matching
    is otherwise invariant.
    """

    @property
    def status_code(self) -> int: ...

    @property
    def content(self) -> bytes: ...

    @property
    def headers(self) -> Mapping[str, str]: ...


class APIError(Exception):
    """Raised for any forge-dashboard response carrying an error body.

    Attributes:
        status_code: The HTTP status code.
        message: The API's own error message (empty string if the body
            wasn't the documented ``{error}`` shape).
    """

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(str(self))

    def __str__(self) -> str:
        return f"forge-dashboard: {self.status_code}: {self.message}"


def decode_error(response: _ErrorResponse) -> APIError | None:
    """Build an :class:`APIError` from *response*, or return ``None`` if
    its status code isn't an error.

    Decodes ``response.content`` directly rather than trusting the
    generated per-operation ``.parsed`` field, which is only populated for
    status codes the spec documents on that specific operation -- a 500 or
    429 that survived every retry attempt still needs an ``APIError``, and
    the API returns the same ``{error}`` shape for those too.

    Usage::

        response = sync_detailed(client=client.raw, ...)
        if error := decode_error(response):
            raise error
    """
    if response.status_code < 400:
        return None

    message = ""
    try:
        body = json.loads(response.content)
        if isinstance(body, dict):
            message = str(body.get("error", ""))
    except ValueError:
        pass

    return APIError(int(response.status_code), message)
