# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

import json
from collections.abc import Callable, Iterator
from datetime import timedelta
from functools import wraps
from typing import Any, Generic, ParamSpec, TypeVar, cast, get_args

import httpx

from trajectory._exceptions import APIResponseValidationError
from trajectory._models import FinalRequestOptions
from trajectory._streaming import Stream

ResponseT = TypeVar("ResponseT")
P = ParamSpec("P")
RAW_RESPONSE_HEADER = "X-Stainless-Raw-Response"


def to_raw_response_wrapper(func: Callable[P, ResponseT]) -> Callable[P, "APIResponse[ResponseT]"]:
  """Wrap a resource method so it returns its APIResponse before parsing."""

  @wraps(func)
  def wrapped(*args: P.args, **kwargs: P.kwargs) -> APIResponse[ResponseT]:
    extra_headers = {**(cast(dict[str, str] | None, kwargs.get("extra_headers")) or {})}
    extra_headers[RAW_RESPONSE_HEADER] = "true"
    kwargs["extra_headers"] = extra_headers
    return cast(APIResponse[ResponseT], func(*args, **kwargs))

  return wrapped


class APIResponse(Generic[ResponseT]):
  """Parse one successful HTTP response into its declared SDK type."""

  def __init__(
    self,
    cast_to: type[ResponseT] | None,
    response: httpx.Response,
    client: Any,
    options: FinalRequestOptions,
    page_options: FinalRequestOptions,
    stream: bool = False,
    stream_cls: type[Stream[Any]] | None = None,
    retries_taken: int = 0,
  ) -> None:
    self._cast_to = cast_to
    self.http_response = response
    self._client = client
    self._options = options
    self._page_options = page_options
    self._stream = stream
    self._stream_cls = stream_cls
    self.retries_taken = retries_taken

  @property
  def headers(self) -> httpx.Headers:
    return self.http_response.headers

  @property
  def http_request(self) -> httpx.Request:
    return self.http_response.request

  @property
  def status_code(self) -> int:
    return self.http_response.status_code

  @property
  def url(self) -> httpx.URL:
    return self.http_response.url

  @property
  def method(self) -> str:
    return self.http_request.method

  @property
  def http_version(self) -> str:
    return self.http_response.http_version

  @property
  def elapsed(self) -> timedelta:
    return self.http_response.elapsed

  @property
  def is_closed(self) -> bool:
    return self.http_response.is_closed

  @property
  def request_id(self) -> str | None:
    return cast(str | None, self.http_response.headers.get("x-request-id"))

  def __repr__(self) -> str:
    return (
      f"<{self.__class__.__name__} "
      f"[{self.status_code} {self.http_response.reason_phrase}] type={self._cast_to}>"
    )

  def read(self) -> bytes:
    return self.http_response.read()

  def text(self) -> str:
    self.read()
    return self.http_response.text

  def json(self) -> object:
    self.read()
    return self.http_response.json()

  def close(self) -> None:
    self.http_response.close()

  def iter_bytes(self, chunk_size: int | None = None) -> Iterator[bytes]:
    yield from self.http_response.iter_bytes(chunk_size)

  def iter_text(self, chunk_size: int | None = None) -> Iterator[str]:
    yield from self.http_response.iter_text(chunk_size)

  def iter_lines(self) -> Iterator[str]:
    yield from self.http_response.iter_lines()

  def parse(self) -> ResponseT | httpx.Response | Stream[Any]:
    if self._stream:
      if self._stream_cls is None:
        raise TypeError("The `stream_cls` argument must be given when `stream=True`")
      stream_args = get_args(self._stream_cls)
      if len(stream_args) != 1:
        raise TypeError("Expected `stream_cls` with one type argument, such as Stream[dict]")
      return self._stream_cls(
        cast_to=stream_args[0],
        response=self.http_response,
        client=self._client,
        options=self._options,
      )
    if self._cast_to is None:
      return self.http_response
    content_type = (
      self.http_response.headers.get("content-type", "*").split(";", 1)[0].strip().lower()
    )
    if not content_type.endswith("json"):
      try:
        return self._process_data(self.http_response.json())
      except (json.JSONDecodeError, UnicodeDecodeError):
        pass
      if self._client._strict_response_validation:
        raise APIResponseValidationError(self.http_response, self.http_response.text)
      return cast(ResponseT, self.http_response.text)
    try:
      data = self.http_response.json()
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
      raise APIResponseValidationError(self.http_response, self.http_response.text) from error
    return self._process_data(data)

  def _process_data(self, data: object) -> ResponseT:
    assert self._cast_to is not None
    result = self._client._process_response_data(
      data=data,
      cast_to=self._cast_to,
      response=self.http_response,
    )
    return cast(
      ResponseT,
      self._client._process_response_result(
        result=result,
        cast_to=self._cast_to,
        options=self._page_options,
      ),
    )
