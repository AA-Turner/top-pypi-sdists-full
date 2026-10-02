# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from typing import Any, Literal

import httpx


class TrajectoryError(Exception):
  """Base exception for all errors raised by the Trajectory SDK."""


class APIError(TrajectoryError):
  """Base exception for errors raised by the SDK."""

  body: object | None
  code: str | None
  context: dict[str, Any] | None
  doc_url: str | None
  message: str
  param: str | None
  request: httpx.Request
  type: str | None

  def __init__(self, message: str, request: httpx.Request, body: object | None = None) -> None:
    super().__init__(message)
    self.body = body
    self.request = request
    if isinstance(body, dict):
      self.code = _get_optional_string(body.get("code"))
      self.context = _get_optional_dict(body.get("context"))
      self.doc_url = _get_optional_string(body.get("doc_url"))
      self.param = _get_optional_string(body.get("param"))
      self.type = _get_optional_string(body.get("type"))
    else:
      self.code = None
      self.context = None
      self.doc_url = None
      self.param = None
      self.type = None
    self.message = message


def _get_optional_string(value: Any) -> str | None:
  return value if isinstance(value, str) else None


def _get_optional_dict(value: Any) -> dict[str, Any] | None:
  return value if isinstance(value, dict) else None


class APIConnectionError(APIError):
  def __init__(self, request: httpx.Request, message: str = "Connection error.") -> None:
    super().__init__(message, request)


class APITimeoutError(APIConnectionError):
  def __init__(self, request: httpx.Request) -> None:
    super().__init__(
      request,
      "Request timed out or interrupted. This could be due to a network timeout, "
      "dropped connection, or request cancellation.",
    )


class APIResponseValidationError(APIError):
  request_id: str | None

  def __init__(self, response: httpx.Response, body: object | None) -> None:
    message = (
      f"Data returned by API did not match the expected schema "
      f"(status {response.status_code}, request ID {response.headers.get('x-request-id')!r})."
    )
    super().__init__(message, response.request, body)
    self.response = response
    self.status_code = response.status_code
    self.request_id = response.headers.get("x-request-id")


class APIStatusError(APIError):
  """Raised when an API response has a status code of 4xx or 5xx."""

  request_id: str | None
  response: httpx.Response
  status_code: int

  def __init__(self, response: httpx.Response, body: object | None) -> None:
    message = f"Error code: {response.status_code}"
    if body is not None:
      message = f"{message} - {body}"
    super().__init__(message, response.request, body)
    if isinstance(body, dict):
      self.message = _get_optional_string(body.get("message")) or message
    self.response = response
    self.status_code = response.status_code
    self.request_id = response.headers.get("x-request-id")


class BadRequestError(APIStatusError):
  status_code: Literal[400] = 400  # pyright: ignore[reportIncompatibleVariableOverride]


class AuthenticationError(APIStatusError):
  status_code: Literal[401] = 401  # pyright: ignore[reportIncompatibleVariableOverride]


class PermissionDeniedError(APIStatusError):
  status_code: Literal[403] = 403  # pyright: ignore[reportIncompatibleVariableOverride]


class NotFoundError(APIStatusError):
  status_code: Literal[404] = 404  # pyright: ignore[reportIncompatibleVariableOverride]


class ConflictError(APIStatusError):
  status_code: Literal[409] = 409  # pyright: ignore[reportIncompatibleVariableOverride]


class UnprocessableEntityError(APIStatusError):
  status_code: Literal[422] = 422  # pyright: ignore[reportIncompatibleVariableOverride]


class RateLimitError(APIStatusError):
  status_code: Literal[429] = 429  # pyright: ignore[reportIncompatibleVariableOverride]


class InternalServerError(APIStatusError):
  status_code: Literal[500] = 500  # pyright: ignore[reportIncompatibleVariableOverride]


class BadGatewayError(APIStatusError):
  status_code: Literal[502] = 502  # pyright: ignore[reportIncompatibleVariableOverride]


class ServiceUnavailableError(APIStatusError):
  status_code: Literal[503] = 503  # pyright: ignore[reportIncompatibleVariableOverride]
