"""Provider-owned HTTP transport primitives."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Protocol

import requests


class DeliveryState(StrEnum):
    """What can be established about delivery of an HTTP request."""

    NOT_DELIVERED = "not_delivered"
    DELIVERED = "delivered"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class HttpResponse:
    """A response returned by a provider transport."""

    status_code: int
    body: object
    delivery_state: DeliveryState = DeliveryState.AMBIGUOUS

    @property
    def status(self) -> int:
        """Return the HTTP status code."""
        return self.status_code

    @property
    def delivery(self) -> DeliveryState:
        """Return the delivery state."""
        return self.delivery_state


class TransportError(Exception):
    """A transport failure with an explicit delivery classification."""

    def __init__(
        self,
        message: str,
        *,
        delivery_state: DeliveryState = DeliveryState.AMBIGUOUS,
        retryable: bool = False,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        if not isinstance(message, str) or not message:
            raise ValueError("message must be a non-empty string")
        if not isinstance(delivery_state, DeliveryState):
            raise ValueError("delivery_state must be a DeliveryState")
        if not isinstance(retryable, bool):
            raise ValueError("retryable must be a boolean")
        if retryable and delivery_state is not DeliveryState.NOT_DELIVERED:
            raise ValueError("retryable=True is only valid when delivery_state is NOT_DELIVERED")
        self.delivery_state = delivery_state
        self.retryable = retryable
        self.details = dict(details) if details is not None else None
        super().__init__(message)

    @property
    def delivery(self) -> DeliveryState:
        """Return the delivery classification."""
        return self.delivery_state


class HttpTransport(Protocol):
    """The injectable provider HTTP transport seam."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        json_body: Mapping[str, Any] | None,
        timeout: float,
    ) -> HttpResponse:
        """Send one request without applying an implicit retry policy."""
        ...  # pragma: no cover


class RequestsHttpTransport:
    """Requests-backed transport with no implicit retries."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.trust_env = False

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        json_body: Mapping[str, Any] | None,
        timeout: float,
    ) -> HttpResponse:
        try:
            response = self._session.request(
                method,
                url,
                headers=dict(headers),
                json=json_body,
                timeout=timeout,
                allow_redirects=False,
            )
        except requests.ConnectTimeout as exc:
            raise TransportError(
                "HTTP request failed",
                delivery_state=DeliveryState.NOT_DELIVERED,
                retryable=True,
                details={"exception_type": type(exc).__name__},
            ) from None
        except requests.RequestException as exc:
            raise TransportError(
                "HTTP request failed",
                delivery_state=DeliveryState.AMBIGUOUS,
                retryable=False,
                details={"exception_type": type(exc).__name__},
            ) from None

        try:
            body: object = response.json()
        except ValueError:
            body = response.text
        return HttpResponse(
            status_code=response.status_code,
            body=body,
            delivery_state=DeliveryState.DELIVERED,
        )


__all__ = [
    "DeliveryState",
    "HttpResponse",
    "HttpTransport",
    "RequestsHttpTransport",
    "TransportError",
]
