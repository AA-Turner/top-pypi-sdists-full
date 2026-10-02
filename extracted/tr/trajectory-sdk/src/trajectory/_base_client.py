# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

import email.utils
import json
import platform
import re
import socket
import time
import warnings
from collections.abc import Collection, Iterator, Mapping
from random import random
from types import TracebackType
from typing import Any, Generic, Literal, TypeVar, cast, overload
from urllib.parse import quote
from urllib.request import getproxies

import httpx
from pydantic import BaseModel, PrivateAttr, TypeAdapter, ValidationError

from trajectory._exceptions import (
  APIConnectionError,
  APIResponseValidationError,
  APIStatusError,
  APITimeoutError,
  AuthenticationError,
  BadGatewayError,
  BadRequestError,
  ConflictError,
  InternalServerError,
  NotFoundError,
  PermissionDeniedError,
  RateLimitError,
  ServiceUnavailableError,
  UnprocessableEntityError,
)
from trajectory._models import BaseModel as SDKBaseModel
from trajectory._models import FinalRequestOptions, construct_type
from trajectory._response import RAW_RESPONSE_HEADER, APIResponse
from trajectory._streaming import SSEDecoder, Stream
from trajectory._types import Body, Headers, NotGiven, Omit, Query, not_given, omit
from trajectory._utils import maybe_transform

ResponseT = TypeVar("ResponseT")
PageItemT = TypeVar("PageItemT")
SyncPageT = TypeVar("SyncPageT", bound="SyncPage[Any]")
StreamT = TypeVar("StreamT", bound="Stream[Any]")

DEFAULT_TIMEOUT = httpx.Timeout(600.0, connect=5.0)
DEFAULT_MAX_RETRIES = 2
_INITIAL_RETRY_DELAY = 0.5
_MAX_RETRY_DELAY = 8.0
_DOT_SEGMENT_RE = re.compile(r"^(?:\.|%2[eE]){1,2}$")
_PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")
_AUTH_ORIGIN_EXTENSION = "spotless_auth_origin"


def _platform_headers() -> dict[str, str]:
  machine = platform.machine().lower()
  architecture = {
    "amd64": "x64",
    "x86_64": "x64",
    "i386": "x32",
    "i686": "x32",
    "aarch64": "arm64",
    "arm64": "arm64",
  }.get(machine, "unknown")
  system = platform.system()
  operating_system = "MacOS" if system == "Darwin" else system or "Unknown"
  return {
    "X-Stainless-Lang": "python",
    "X-Stainless-OS": operating_system,
    "X-Stainless-Arch": architecture,
    "X-Stainless-Runtime": platform.python_implementation(),
    "X-Stainless-Runtime-Version": platform.python_version(),
  }


def _merge_headers(*header_sets: Mapping[str, str] | None) -> dict[str, str]:
  merged = httpx.Headers(encoding="utf-8")
  for headers in header_sets:
    merged.update(headers or {})
  return {name.decode("utf-8"): value.decode("utf-8") for name, value in merged.raw}


def path_template(template: str, **values: Any) -> str:
  """Interpolate percent-encoded path segments and reject dot-segments."""

  def replace(match: re.Match[str]) -> str:
    name = match.group(1)
    if name not in values:
      raise KeyError(f"a value for placeholder {name!r} was not provided")
    value = values[name]
    if value is None:
      return "null"
    if isinstance(value, bool):
      return "true" if value else "false"
    return quote(str(value), safe="!$&'()*+,;=:@")

  path = _PLACEHOLDER_RE.sub(replace, template)
  for segment in path.split("/"):
    if _DOT_SEGMENT_RE.match(segment):
      raise ValueError(f"Constructed path {path!r} contains dot-segment {segment!r}")
  return path


def serialize_header(value: object) -> str | Omit:
  if value is None or isinstance(value, Omit):
    return omit
  if isinstance(value, bool):
    return str(value).lower()
  return str(value)


class PageInfo:
  """The query parameters needed to request the next page."""

  def __init__(self, params: Query) -> None:
    self.params = params

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(params={self.params})"


class SyncPage(BaseModel, Generic[PageItemT]):
  """One page of a cursor-paginated list response."""

  items: list[PageItemT]
  next_cursor: str | None = None
  has_more: bool

  _client: "APIClient" = PrivateAttr()
  _options: FinalRequestOptions = PrivateAttr()
  _cast_to: type[Any] = PrivateAttr()
  _request_id: str | None = PrivateAttr(default=None)

  def _set_private_attributes(
    self,
    client: "APIClient",
    cast_to: type[Any],
    options: FinalRequestOptions,
  ) -> None:
    self._client = client
    self._cast_to = cast_to
    self._options = options

  def _get_page_items(self) -> list[PageItemT]:
    return self.items

  def has_next_page(self) -> bool:
    if not self.has_more or not self._get_page_items():
      return False
    return self.next_page_info() is not None

  def next_page_info(self) -> PageInfo | None:
    if not self.next_cursor:
      return None
    return PageInfo(params={"cursor": self.next_cursor})

  def _info_to_options(self, info: PageInfo) -> FinalRequestOptions:
    return self._options.model_copy(update={"params": {**self._options.params, **info.params}})

  # Item iteration replaces Pydantic's dict(model) behavior; model_dump() remains available.
  def __iter__(self) -> Iterator[PageItemT]:  # type: ignore[override]
    for page in self.iter_pages():
      yield from page._get_page_items()

  def iter_pages(self: SyncPageT) -> Iterator[SyncPageT]:
    page = self
    while True:
      yield page
      if not page.has_next_page():
        return
      page = page.get_next_page()

  def get_next_page(self: SyncPageT) -> SyncPageT:
    page_info = self.next_page_info()
    if page_info is None:
      raise RuntimeError(
        "No next page expected; please check `.has_next_page()` before calling `.get_next_page()`."
      )
    next_options = self._info_to_options(page_info)
    return cast(SyncPageT, self._client.request(self._cast_to, next_options))


def make_request_options(
  *,
  headers: Headers | None = None,
  extra_headers: Headers | None = None,
  params: Query | None = None,
  extra_query: Query | None = None,
  extra_body: Mapping[str, Any] | None = None,
  timeout: float | httpx.Timeout | None | NotGiven = not_given,
  synthesize_event_and_data: bool = False,
) -> dict[str, Any]:
  """Build the options a resource method spreads into `FinalRequestOptions.construct`."""
  options: dict[str, Any] = {}
  merged_headers = {
    name: value for name, value in (headers or {}).items() if not isinstance(value, Omit)
  }
  merged_headers.update(extra_headers or {})
  if merged_headers:
    options["headers"] = merged_headers
  merged_params = maybe_transform({**(params or {}), **(extra_query or {})})
  if merged_params:
    options["params"] = merged_params
  transformed_extra_body = maybe_transform(extra_body or {})
  if transformed_extra_body:
    options["extra_json"] = transformed_extra_body
  if not isinstance(timeout, NotGiven):
    options["timeout"] = timeout
  if synthesize_event_and_data:
    options["synthesize_event_and_data"] = True
  return options


def _origin(url: httpx.URL) -> tuple[str, str, int | None]:
  default_port = 443 if url.scheme == "https" else 80 if url.scheme == "http" else None
  port = url.port if url.port is not None else default_port
  return url.scheme, url.host, port


def _strip_auth_on_cross_origin_request(request: httpx.Request) -> None:
  auth_origin = request.extensions.get(_AUTH_ORIGIN_EXTENSION)
  if auth_origin is not None and _origin(request.url) != auth_origin:
    for header in ("X-API-Key", "Authorization", "X-Model-Endpoint-Access-Token"):
      request.headers.pop(header, None)


class _DefaultHttpxClient(httpx.Client):
  def __init__(self, **kwargs: Any) -> None:
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    kwargs.setdefault("follow_redirects", True)
    if all(kwargs.get(key) is None for key in ("transport", "mounts", "proxy")) and (
      not kwargs.get("trust_env", True) or not (getproxies().keys() - {"no"})
    ):
      # An explicit transport disables HTTPX environment proxies, so preserve those clients.
      kwargs["transport"] = httpx.HTTPTransport(
        **{
          key: kwargs[key]
          for key in ("verify", "cert", "trust_env", "http1", "http2", "limits")
          if key in kwargs
        },
        retries=0,
        socket_options=self._get_keepalive_options(),
      )
    super().__init__(**kwargs)

  @staticmethod
  def _get_keepalive_options() -> list[tuple[int, int, int]]:
    options = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
    # macOS names the idle timer TCP_KEEPALIVE; Linux and modern Windows use TCP_KEEPIDLE.
    idle_option = getattr(socket, "TCP_KEEPIDLE", None)
    if idle_option is None:
      idle_option = getattr(socket, "TCP_KEEPALIVE", None)
    if idle_option is not None:
      options.append((socket.IPPROTO_TCP, idle_option, 60))
    return options


class APIClient:
  _base_url: httpx.URL
  _client: httpx.Client
  _default_headers: dict[str, str]
  _default_query: dict[str, object]
  _max_retries: int
  _strict_response_validation: bool
  _timeout: httpx.Timeout | float | None

  def __init__(
    self,
    base_url: str | httpx.URL,
    http_client: httpx.Client | None = None,
    timeout: httpx.Timeout | float | None | NotGiven = not_given,
    default_headers: Mapping[str, str] | None = None,
    default_query: Mapping[str, object] | None = None,
    max_retries: int = DEFAULT_MAX_RETRIES,
    _strict_response_validation: bool = False,
  ) -> None:
    if max_retries < 0:
      raise ValueError("max_retries must be zero or greater")
    self._base_url = httpx.URL(base_url)
    if not self._base_url.raw_path.endswith(b"/"):
      self._base_url = self._base_url.copy_with(raw_path=self._base_url.raw_path + b"/")
    if isinstance(timeout, NotGiven):
      timeout = http_client.timeout if http_client is not None else DEFAULT_TIMEOUT
    self._default_headers = _merge_headers(_platform_headers(), default_headers)
    self._default_query = dict(default_query or {})
    self._client = http_client or _DefaultHttpxClient(timeout=timeout)
    if _strip_auth_on_cross_origin_request not in self._client.event_hooks["request"]:
      self._client.event_hooks["request"].append(_strip_auth_on_cross_origin_request)
    self._max_retries = max_retries
    self._strict_response_validation = _strict_response_validation
    self._timeout = timeout

  @property
  def base_url(self) -> httpx.URL:
    return self._base_url

  @property
  def default_headers(self) -> dict[str, str]:
    return dict(self._default_headers)

  @property
  def default_query(self) -> dict[str, object]:
    return dict(self._default_query)

  @property
  def max_retries(self) -> int:
    return self._max_retries

  @property
  def timeout(self) -> httpx.Timeout | float | None:
    return self._timeout

  def __enter__(self) -> "APIClient":
    return self

  def __exit__(
    self,
    exc_type: type[BaseException] | None,
    exc_value: BaseException | None,
    traceback: TracebackType | None,
  ) -> None:
    self.close()

  def close(self) -> None:
    if hasattr(self, "_client"):
      self._client.close()

  @overload
  def request(
    self,
    cast_to: type[ResponseT],
    options: FinalRequestOptions,
    *,
    stream: Literal[True],
    stream_cls: type[StreamT],
  ) -> StreamT: ...

  @overload
  def request(
    self,
    cast_to: type[ResponseT],
    options: FinalRequestOptions,
    *,
    stream: Literal[False] = False,
  ) -> ResponseT: ...

  @overload
  def request(
    self,
    cast_to: None,
    options: FinalRequestOptions,
    *,
    stream: Literal[False] = False,
  ) -> httpx.Response: ...

  @overload
  def request(
    self,
    cast_to: type[ResponseT],
    options: FinalRequestOptions,
    *,
    stream: bool,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT: ...

  def request(
    self,
    cast_to: type[ResponseT] | None,
    options: FinalRequestOptions,
    *,
    stream: bool = False,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | httpx.Response | StreamT:
    # httpx.Headers merges case-insensitively, so an override header replaces
    # the default regardless of casing rather than sitting alongside it.
    request_headers = options.headers or {}
    omitted_headers = {
      name.lower() for name, value in request_headers.items() if isinstance(value, Omit)
    }
    merged_headers = httpx.Headers(self.default_headers)
    for name, value in request_headers.items():
      if isinstance(value, Omit):
        merged_headers.pop(name, None)
      else:
        merged_headers[name] = value
    options.headers = merged_headers
    options.params = {**self._default_query, **options.params}
    if options.extra_json:
      options.json_data = {**(options.json_data or {}), **options.extra_json}
    body_is_replayable = self._is_body_replayable(options)
    if body_is_replayable:
      self._buffer_content_for_retries(options)
    max_retries = self._max_retries if body_is_replayable else 0
    for retries_taken in range(max_retries + 1):
      request = self._build_request(options, retries_taken, omitted_headers)
      try:
        response = self._send_request(request, stream=stream)
      except httpx.TimeoutException as error:
        if retries_taken >= max_retries:
          raise APITimeoutError(error.request) from error
        self._sleep_for_retry(retries_taken, None)
        continue
      except httpx.RequestError as error:
        if retries_taken >= max_retries:
          raise APIConnectionError(error.request) from error
        self._sleep_for_retry(retries_taken, None)
        continue
      if not response.is_success:
        if retries_taken < max_retries and self._should_retry(response):
          response.close()
          self._sleep_for_retry(retries_taken, response)
          continue
        if not response.is_closed:
          response.read()
        raise self._make_status_error_from_response(response)
      api_response = APIResponse(
        cast_to=cast_to,
        response=response,
        client=self,
        options=options,
        page_options=options.model_copy(
          update={
            "headers": {
              name: value
              for name, value in request_headers.items()
              if name.lower() != RAW_RESPONSE_HEADER.lower()
            }
          }
        ),
        stream=stream,
        stream_cls=stream_cls,
        retries_taken=retries_taken,
      )
      if response.request.headers.get(RAW_RESPONSE_HEADER) == "true":
        return cast(ResponseT | httpx.Response | StreamT, api_response)
      result = api_response.parse()
      return cast(ResponseT | httpx.Response | StreamT, result)
    raise RuntimeError("Request retry loop exited unexpectedly")

  def _process_response_data(
    self,
    data: object,
    cast_to: type[ResponseT],
    response: httpx.Response,
  ) -> ResponseT:
    try:
      result = (
        TypeAdapter(cast_to).validate_python(data)
        if self._strict_response_validation
        else construct_type(data, cast_to)
      )
    except ValidationError as error:
      raise APIResponseValidationError(response, data) from error
    if isinstance(result, (SDKBaseModel, SyncPage)):
      setattr(result, "_request_id", response.headers.get("x-request-id"))
    return cast(ResponseT, result)

  def _process_response_result(
    self,
    result: ResponseT,
    cast_to: type[ResponseT],
    options: FinalRequestOptions,
  ) -> ResponseT:
    if isinstance(result, SyncPage):
      result._set_private_attributes(self, cast(type[Any], cast_to), options)
    return result

  def _is_body_replayable(self, options: FinalRequestOptions) -> bool:
    content = options.content
    if content is not None and not isinstance(content, (bytes, bytearray, memoryview, str)):
      try:
        position = content.tell()
        content.seek(position)
      except (AttributeError, OSError):
        return False

    files = options.files
    if files is None:
      return True
    file_values = files.values() if isinstance(files, Mapping) else (item[1] for item in files)
    for value in file_values:
      file_content = value[1] if isinstance(value, tuple) else value
      if isinstance(file_content, (bytes, bytearray, memoryview, str)):
        continue
      try:
        position = file_content.tell()
        file_content.seek(position)
      except (AttributeError, OSError):
        return False
    return True

  def _buffer_content_for_retries(self, options: FinalRequestOptions) -> None:
    content = options.content
    if content is None or isinstance(content, (bytes, bytearray, memoryview, str)):
      return
    position = content.tell()
    options.content = content.read()
    content.seek(position)

  def _prepare_url(self, url: str) -> httpx.URL:
    """Merge a relative URL with the client's base_url, per httpx's own `_merge_url`."""
    merge_url = httpx.URL(url)
    if merge_url.is_relative_url:
      merge_raw_path = self._base_url.raw_path + merge_url.raw_path.lstrip(b"/")
      return self._base_url.copy_with(raw_path=merge_raw_path)
    return merge_url

  def _build_request(
    self,
    options: FinalRequestOptions,
    retries_taken: int = 0,
    omitted_headers: Collection[str] = (),
  ) -> httpx.Request:
    headers = httpx.Headers(cast(Mapping[str, str], options.headers))
    if (
      "x-stainless-retry-count" not in headers and "x-stainless-retry-count" not in omitted_headers
    ):
      headers["X-Stainless-Retry-Count"] = str(retries_taken)
    if (
      "x-stainless-read-timeout" not in headers
      and "x-stainless-read-timeout" not in omitted_headers
    ):
      timeout = self._timeout if isinstance(options.timeout, NotGiven) else options.timeout
      if isinstance(timeout, httpx.Timeout):
        timeout = timeout.read
      if timeout is not None:
        headers["X-Stainless-Read-Timeout"] = str(timeout)
    return self._client.build_request(
      options.method,
      self._prepare_url(options.url),
      headers=headers,
      params=cast(Any, options.params),
      json=options.json_data,
      content=options.content,
      files=options.files,
      timeout=self._timeout if isinstance(options.timeout, NotGiven) else options.timeout,
      extensions={_AUTH_ORIGIN_EXTENSION: _origin(self._base_url)},
    )

  def _send_request(self, request: httpx.Request, stream: bool = False) -> httpx.Response:
    return self._client.send(request, stream=stream)

  def _make_sse_decoder(self) -> SSEDecoder:
    return SSEDecoder()

  def _make_status_error_from_response(self, response: httpx.Response) -> APIStatusError:
    response_text = response.text.strip()
    body: object | None = None
    if response_text:
      try:
        body = response.json()
      except (json.JSONDecodeError, UnicodeDecodeError):
        body = response_text
    return self._make_status_error(response, body)

  def _make_status_error(
    self,
    response: httpx.Response,
    body: object | None,
  ) -> APIStatusError:
    if isinstance(body, dict):
      body = body.get("error", body)
    error_types = {
      400: BadRequestError,
      401: AuthenticationError,
      403: PermissionDeniedError,
      404: NotFoundError,
      409: ConflictError,
      422: UnprocessableEntityError,
      429: RateLimitError,
      500: InternalServerError,
      502: BadGatewayError,
      503: ServiceUnavailableError,
    }
    error_type = error_types.get(response.status_code, APIStatusError)
    return error_type(response, body)

  @overload
  def get(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    options: dict[str, Any] | None = None,
    stream: Literal[True],
    stream_cls: type[StreamT],
  ) -> StreamT: ...

  @overload
  def get(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    options: dict[str, Any] | None = None,
    stream: Literal[False] = False,
  ) -> ResponseT: ...

  @overload
  def get(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    options: dict[str, Any] | None = None,
    stream: bool,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT: ...

  def get(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    options: dict[str, Any] | None = None,
    stream: bool = False,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT:
    final_options = FinalRequestOptions.construct(method="GET", url=path, **(options or {}))
    return self.request(cast_to, final_options, stream=stream, stream_cls=stream_cls)

  @overload
  def post(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[True],
    stream_cls: type[StreamT],
  ) -> StreamT: ...

  @overload
  def post(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[False] = False,
  ) -> ResponseT: ...

  @overload
  def post(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT: ...

  def post(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool = False,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT:
    if body is not None and content is not None:
      raise TypeError("Passing both `body` and `content` is not supported")
    if files is not None and content is not None:
      raise TypeError("Passing both `files` and `content` is not supported")
    if isinstance(body, bytes):
      warnings.warn(
        "Passing raw bytes as `body` is deprecated and will be removed in a future version. "
        "Please pass raw bytes via the `content` parameter instead.",
        DeprecationWarning,
        stacklevel=2,
      )
    # exclude_unset: an untouched optional field stays absent from the wire instead of
    # serializing as an explicit `null` that would clobber it server-side.
    json_data = (
      body.model_dump(mode="json", exclude_unset=True) if isinstance(body, BaseModel) else body
    )
    final_options = FinalRequestOptions.construct(
      method="POST", url=path, json_data=json_data, content=content, files=files, **(options or {})
    )
    return self.request(cast_to, final_options, stream=stream, stream_cls=stream_cls)

  @overload
  def put(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[True],
    stream_cls: type[StreamT],
  ) -> StreamT: ...

  @overload
  def put(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[False] = False,
  ) -> ResponseT: ...

  @overload
  def put(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT: ...

  def put(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool = False,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT:
    if body is not None and content is not None:
      raise TypeError("Passing both `body` and `content` is not supported")
    if files is not None and content is not None:
      raise TypeError("Passing both `files` and `content` is not supported")
    if isinstance(body, bytes):
      warnings.warn(
        "Passing raw bytes as `body` is deprecated and will be removed in a future version. "
        "Please pass raw bytes via the `content` parameter instead.",
        DeprecationWarning,
        stacklevel=2,
      )
    # exclude_unset: an untouched optional field stays absent from the wire instead of
    # serializing as an explicit `null` that would clobber it server-side.
    json_data = (
      body.model_dump(mode="json", exclude_unset=True) if isinstance(body, BaseModel) else body
    )
    final_options = FinalRequestOptions.construct(
      method="PUT", url=path, json_data=json_data, content=content, files=files, **(options or {})
    )
    return self.request(cast_to, final_options, stream=stream, stream_cls=stream_cls)

  @overload
  def patch(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[True],
    stream_cls: type[StreamT],
  ) -> StreamT: ...

  @overload
  def patch(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[False] = False,
  ) -> ResponseT: ...

  @overload
  def patch(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT: ...

  def patch(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool = False,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT:
    if body is not None and content is not None:
      raise TypeError("Passing both `body` and `content` is not supported")
    if files is not None and content is not None:
      raise TypeError("Passing both `files` and `content` is not supported")
    if isinstance(body, bytes):
      warnings.warn(
        "Passing raw bytes as `body` is deprecated and will be removed in a future version. "
        "Please pass raw bytes via the `content` parameter instead.",
        DeprecationWarning,
        stacklevel=2,
      )
    # PATCH is a partial update: omit fields the caller never set instead of nulling them out.
    json_data = (
      body.model_dump(mode="json", exclude_unset=True) if isinstance(body, BaseModel) else body
    )
    final_options = FinalRequestOptions.construct(
      method="PATCH", url=path, json_data=json_data, content=content, files=files, **(options or {})
    )
    return self.request(cast_to, final_options, stream=stream, stream_cls=stream_cls)

  @overload
  def delete(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[True],
    stream_cls: type[StreamT],
  ) -> StreamT: ...

  @overload
  def delete(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: Literal[False] = False,
  ) -> ResponseT: ...

  @overload
  def delete(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT: ...

  def delete(
    self,
    path: str,
    *,
    cast_to: type[ResponseT],
    body: Body | None = None,
    content: Any = None,
    files: Any = None,
    options: dict[str, Any] | None = None,
    stream: bool = False,
    stream_cls: type[StreamT] | None = None,
  ) -> ResponseT | StreamT:
    if body is not None and content is not None:
      raise TypeError("Passing both `body` and `content` is not supported")
    if files is not None and content is not None:
      raise TypeError("Passing both `files` and `content` is not supported")
    if isinstance(body, bytes):
      warnings.warn(
        "Passing raw bytes as `body` is deprecated and will be removed in a future version. "
        "Please pass raw bytes via the `content` parameter instead.",
        DeprecationWarning,
        stacklevel=2,
      )
    # exclude_unset: an untouched optional field stays absent from the wire instead of
    # serializing as an explicit `null` that would clobber it server-side.
    json_data = (
      body.model_dump(mode="json", exclude_unset=True) if isinstance(body, BaseModel) else body
    )
    final_options = FinalRequestOptions.construct(
      method="DELETE",
      url=path,
      json_data=json_data,
      content=content,
      files=files,
      **(options or {}),
    )
    return self.request(cast_to, final_options, stream=stream, stream_cls=stream_cls)

  def _should_retry(self, response: httpx.Response) -> bool:
    should_retry = response.headers.get("trajectory-should-retry")
    if should_retry == "true":
      return True
    if should_retry == "false":
      return False
    return response.status_code in {408, 429} or response.status_code >= 500

  def _parse_retry_after(self, response: httpx.Response) -> float | None:
    retry_after_ms = response.headers.get("retry-after-ms")
    try:
      return float(retry_after_ms) / 1000
    except (TypeError, ValueError):
      pass

    retry_after = response.headers.get("retry-after")
    try:
      return float(retry_after)
    except (TypeError, ValueError):
      pass

    retry_date = email.utils.parsedate_tz(retry_after)
    if retry_date is None:
      return None
    return float(email.utils.mktime_tz(retry_date) - time.time())

  def _calculate_retry_delay(
    self,
    retries_taken: int,
    response: httpx.Response | None,
  ) -> float:
    if response is not None:
      retry_after = self._parse_retry_after(response)
      if retry_after is not None and 0 < retry_after <= 120:
        return retry_after
    exponential_delay = min(_INITIAL_RETRY_DELAY * 2**retries_taken, _MAX_RETRY_DELAY)
    return float(exponential_delay * (1 - 0.25 * random()))

  def _sleep_for_retry(
    self,
    retries_taken: int,
    response: httpx.Response | None,
  ) -> None:
    time.sleep(self._calculate_retry_delay(retries_taken, response))
