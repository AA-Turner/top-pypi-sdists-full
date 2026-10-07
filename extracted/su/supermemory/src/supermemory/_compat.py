"""3.x client conventions on top of the Fern-generated v5 client.

Hand-written — lives in custom/ and is copied into src/supermemory by
scripts/generate. It never names an endpoint: methods are wrapped generically,
so spec changes regenerate cleanly without touching this file.

Kept from the 3.x (Stainless) SDK:
- constructor options: api_key, base_url, timeout, max_retries, default_headers,
  default_query, http_client; SUPERMEMORY_API_KEY / SUPERMEMORY_BASE_URL /
  SUPERMEMORY_CUSTOM_HEADERS
- per-call options: extra_headers, extra_query, extra_body, timeout
- client.with_options(...) / client.copy(...)
- the exception hierarchy (SupermemoryError → APIError → APIStatusError →
  NotFoundError, RateLimitError, …; APIConnectionError, APITimeoutError) with
  .status_code, .body, .message, .request, .response
- with_raw_response → .parse(), .headers, .status_code, .http_response, and
  model.to_dict() / model.to_json() (added to generated core by custom/patches/)
"""

from __future__ import annotations

import contextvars
import functools
import inspect
import os
from collections.abc import Callable, Mapping
from typing import Any, Literal, cast

import httpx
import pydantic
from typing_extensions import Self

from ._types import NOT_GIVEN, NotGiven
from .client import AsyncSupermemory as _GeneratedAsyncSupermemory
from .client import Supermemory as _GeneratedSupermemory
from .core.api_error import ApiError
from .core.pydantic_utilities import IS_PYDANTIC_V2

__all__ = [
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_TIMEOUT",
    "NOT_GIVEN",
    "NotGiven",
    "APIConnectionError",
    "APIError",
    "APIResponseValidationError",
    "APIStatusError",
    "APITimeoutError",
    "AsyncClient",
    "AsyncSupermemory",
    "AuthenticationError",
    "BadRequestError",
    "Client",
    "ConflictError",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "Supermemory",
    "SupermemoryError",
    "Timeout",
    "UnprocessableEntityError",
]

Timeout = httpx.Timeout
DEFAULT_TIMEOUT = httpx.Timeout(timeout=60, connect=5.0)
DEFAULT_MAX_RETRIES = 2

# ----------------------------------------------------------------- exceptions


class SupermemoryError(Exception):
    pass


class APIError(SupermemoryError):
    message: str
    request: httpx.Request | None
    body: object

    def __init__(self, message: str, request: httpx.Request | None, *, body: object) -> None:
        # Not super(): raised errors also inherit the generated ApiError, whose
        # keyword-only __init__ would be next in the MRO.
        Exception.__init__(self, message)
        self.request = request
        self.message = message
        self.body = body


class APIResponseValidationError(APIError):
    response: httpx.Response
    status_code: int

    def __init__(self, response: httpx.Response, body: object, *, message: str | None = None) -> None:
        super().__init__(message or "Data returned by API invalid for expected schema.", response.request, body=body)
        self.response = response
        self.status_code = response.status_code


class APIStatusError(APIError):
    """Raised when an API response has a status code of 4xx or 5xx."""

    response: httpx.Response | None
    status_code: int
    headers: dict[str, str] | None

    def __init__(self, message: str, *, response: httpx.Response | None, body: object, status_code: int) -> None:
        super().__init__(message, response.request if response is not None else None, body=body)
        self.response = response
        self.status_code = status_code
        self.headers = dict(response.headers) if response is not None else None


class APIConnectionError(APIError):
    def __init__(self, *, message: str = "Connection error.", request: httpx.Request | None) -> None:
        super().__init__(message, request, body=None)


class APITimeoutError(APIConnectionError):
    def __init__(self, request: httpx.Request | None) -> None:
        super().__init__(message="Request timed out.", request=request)


class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400  # type: ignore[assignment]


class AuthenticationError(APIStatusError):
    status_code: Literal[401] = 401  # type: ignore[assignment]


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403] = 403  # type: ignore[assignment]


class NotFoundError(APIStatusError):
    status_code: Literal[404] = 404  # type: ignore[assignment]


class ConflictError(APIStatusError):
    status_code: Literal[409] = 409  # type: ignore[assignment]


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422] = 422  # type: ignore[assignment]


class RateLimitError(APIStatusError):
    status_code: Literal[429] = 429  # type: ignore[assignment]


class InternalServerError(APIStatusError):
    pass


_STATUS_ERRORS: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}

# The httpx.Response behind the most recent request in this thread / task, so
# status errors can carry .response and .request like 3.x did.
_last_response: contextvars.ContextVar[httpx.Response | None] = contextvars.ContextVar(
    "supermemory_last_response", default=None
)


def _capture_response(response: httpx.Response) -> None:
    _last_response.set(response)


async def _acapture_response(response: httpx.Response) -> None:
    _last_response.set(response)


_combined_error_classes: dict[tuple[type[ApiError], type[APIStatusError]], type[APIStatusError]] = {}


def _combined_error_class(generated: type[ApiError], compat: type[APIStatusError]) -> type[APIStatusError]:
    # Subclass of both, so `except supermemory.NotFoundError` (3.x) and
    # `except supermemory.errors.NotFoundError` (generated) both catch it.
    key = (generated, compat)
    if key not in _combined_error_classes:
        _combined_error_classes[key] = cast(
            type[APIStatusError],
            type(compat.__name__, (compat, generated), {"__module__": "supermemory", "__str__": Exception.__str__}),
        )
    return _combined_error_classes[key]


def _status_error(err: ApiError) -> APIStatusError:
    status = err.status_code or 0
    compat = _STATUS_ERRORS.get(status) or (InternalServerError if status >= 500 else APIStatusError)
    response = _last_response.get()
    if response is not None and response.status_code != status:
        response = None
    body = err.body
    if response is not None:
        # The decoded JSON (or text) the API sent, not a re-serialized model.
        try:
            body = response.json()
        except ValueError:
            body = response.text
    elif isinstance(body, pydantic.BaseModel):
        body = (
            body.model_dump(by_alias=True, exclude_unset=True)
            if IS_PYDANTIC_V2
            else body.dict(by_alias=True, exclude_unset=True)
        )
    cls = _combined_error_class(type(err), compat)
    new = cls.__new__(cls)
    APIStatusError.__init__(new, f"Error code: {status} - {body}", response=response, body=body, status_code=status)
    if response is None:
        new.headers = err.headers
    return new


def _request_of(err: httpx.HTTPError) -> httpx.Request | None:
    try:
        return err.request
    except RuntimeError:
        return None


# ---------------------------------------------------------- per-call options


class _Defaults:
    def __init__(self, default_query: Mapping[str, object] | None) -> None:
        self.default_query = dict(default_query or {})


def _apply_per_call_options(kwargs: dict[str, Any], defaults: _Defaults) -> None:
    # scripts/apply_custom.py adds these parameters to every generated method
    # signature (for type checkers); here they become Fern request_options.
    extra_headers = kwargs.pop("extra_headers", None)
    extra_query = kwargs.pop("extra_query", None)
    extra_body = kwargs.pop("extra_body", None)
    timeout = kwargs.pop("timeout", NOT_GIVEN)
    query = {**defaults.default_query, **(extra_query or {})}
    if not (extra_headers or query or extra_body or not isinstance(timeout, NotGiven)):
        return
    request_options: dict[str, Any] = dict(kwargs.get("request_options") or {})
    if extra_headers:
        request_options["additional_headers"] = {**extra_headers, **request_options.get("additional_headers", {})}
    if query:
        request_options["additional_query_parameters"] = {
            **query,
            **request_options.get("additional_query_parameters", {}),
        }
    if extra_body:
        request_options["additional_body_parameters"] = {
            **extra_body,
            **request_options.get("additional_body_parameters", {}),
        }
    if not isinstance(timeout, NotGiven):
        # httpx.Timeout keeps connect/write/pool; Fern just forwards it. None disables timeouts, as in 3.x.
        request_options["timeout"] = httpx.Timeout(None) if timeout is None else timeout
    kwargs["request_options"] = request_options


def _wrap_method(fn: Callable[..., Any], defaults: _Defaults) -> Callable[..., Any]:
    if inspect.iscoroutinefunction(fn):

        @functools.wraps(fn)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            _apply_per_call_options(kwargs, defaults)
            try:
                return await fn(*args, **kwargs)
            except ApiError as err:
                raise _status_error(err).with_traceback(err.__traceback__) from None
            except httpx.TimeoutException as err:
                raise APITimeoutError(request=_request_of(err)) from err
            except httpx.TransportError as err:
                raise APIConnectionError(request=_request_of(err)) from err

        return async_wrapper

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        _apply_per_call_options(kwargs, defaults)
        try:
            return fn(*args, **kwargs)
        except ApiError as err:
            raise _status_error(err).with_traceback(err.__traceback__) from None
        except httpx.TimeoutException as err:
            raise APITimeoutError(request=_request_of(err)) from err
        except httpx.TransportError as err:
            raise APIConnectionError(request=_request_of(err)) from err

    return wrapper


def _is_generated_client(value: object) -> bool:
    cls = type(value)
    return cls.__module__.startswith(f"{__package__}.") and cls.__name__.endswith(("Client", "Supermemory"))


def _wrap(name: str, value: Any, defaults: _Defaults) -> Any:
    if name.startswith("_"):
        return value
    if inspect.ismethod(value) and "request_options" in inspect.signature(value).parameters:
        return _wrap_method(value, defaults)
    if _is_generated_client(value):
        return _Resource(value, defaults)
    return value


class _Resource:
    """Wraps a generated sub-client (client.documents, client.with_raw_response, …)."""

    def __init__(self, target: Any, defaults: _Defaults) -> None:
        self._target = target
        self._defaults = defaults

    def __getattr__(self, name: str) -> Any:
        return _wrap(name, getattr(self._target, name), self._defaults)

    def __dir__(self) -> Any:
        return dir(self._target)

    def __repr__(self) -> str:
        return repr(self._target)


# -------------------------------------------------------------------- clients


def _env_headers(default_headers: Mapping[str, str] | None) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in os.environ.get("SUPERMEMORY_CUSTOM_HEADERS", "").split("\n"):
        colon = line.find(":")
        if colon >= 0:
            headers[line[:colon].strip()] = line[colon + 1 :].strip()
    return {**headers, **(default_headers or {})}


def _resolve(api_key: str | None, base_url: str | httpx.URL | None) -> tuple[str, str]:
    api_key = api_key if api_key is not None else os.environ.get("SUPERMEMORY_API_KEY")
    if api_key is None:
        raise SupermemoryError(
            "The api_key client option must be set either by passing api_key to the client "
            "or by setting the SUPERMEMORY_API_KEY environment variable"
        )
    base_url = base_url if base_url is not None else os.environ.get("SUPERMEMORY_BASE_URL")
    return api_key, str(base_url or "https://api.supermemory.ai").rstrip("/")


def _resolve_timeout(timeout: float | httpx.Timeout | None | NotGiven) -> httpx.Timeout:
    if isinstance(timeout, NotGiven):
        return DEFAULT_TIMEOUT
    if timeout is None:
        return httpx.Timeout(None)  # 3.x: explicit None disables timeouts
    return timeout if isinstance(timeout, httpx.Timeout) else httpx.Timeout(timeout)


def _add_hook(client: httpx.Client | httpx.AsyncClient, hook: Callable[..., Any]) -> None:
    hooks = client.event_hooks
    if hook not in hooks["response"]:
        hooks["response"] = [*hooks["response"], hook]
        client.event_hooks = hooks


_OWN_ATTRIBUTES = frozenset({"with_options", "copy", "api_key", "base_url", "timeout", "max_retries", "close"})


class Supermemory(_GeneratedSupermemory):
    """Synchronous Supermemory client (3.x-compatible options; v5 API methods)."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        **kwargs: Any,
    ) -> None:
        self.api_key, self.base_url = _resolve(api_key, base_url)
        self.timeout = _resolve_timeout(timeout)
        self.max_retries = max_retries
        headers = _env_headers({**(default_headers or {}), **kwargs.pop("headers", {})})
        http_client = http_client or kwargs.pop("httpx_client", None)
        self._options: dict[str, Any] = dict(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=max_retries,
            default_headers=headers,
            default_query=dict(default_query or {}),
            http_client=http_client,
            **kwargs,
        )
        self._owned_http_client = http_client is None
        self._http_client = http_client or httpx.Client(timeout=self.timeout, follow_redirects=True)
        _add_hook(self._http_client, _capture_response)
        self._defaults = _Defaults(default_query)
        super().__init__(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=cast(float, self.timeout),  # whole httpx.Timeout, forwarded as-is
            max_retries=max_retries,
            headers=headers,
            httpx_client=self._http_client,
            **kwargs,
        )

    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)
        if name.startswith("_") or name in _OWN_ATTRIBUTES:
            return value
        return _wrap(name, value, super().__getattribute__("_defaults"))

    def copy(
        self,
        *,
        set_default_headers: Mapping[str, str] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        **overrides: Any,
    ) -> Supermemory:
        """A new client with some options changed; the rest, including the connection pool, are kept."""
        options = dict(self._options)
        if self._owned_http_client:
            options["http_client"] = self._http_client
        options["default_headers"] = set_default_headers or {
            **options["default_headers"],
            **(overrides.pop("default_headers", None) or {}),
        }
        options["default_query"] = set_default_query or {
            **options["default_query"],
            **(overrides.pop("default_query", None) or {}),
        }
        options.update(overrides)
        return type(self)(**options)

    with_options = copy

    def close(self) -> None:
        if self._owned_http_client:
            self._http_client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncSupermemory(_GeneratedAsyncSupermemory):
    """Asynchronous Supermemory client (3.x-compatible options; v5 API methods)."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        **kwargs: Any,
    ) -> None:
        self.api_key, self.base_url = _resolve(api_key, base_url)
        self.timeout = _resolve_timeout(timeout)
        self.max_retries = max_retries
        headers = _env_headers({**(default_headers or {}), **kwargs.pop("headers", {})})
        http_client = http_client or kwargs.pop("httpx_client", None)
        self._options: dict[str, Any] = dict(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=max_retries,
            default_headers=headers,
            default_query=dict(default_query or {}),
            http_client=http_client,
            **kwargs,
        )
        self._owned_http_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)
        _add_hook(self._http_client, _acapture_response)
        self._defaults = _Defaults(default_query)
        super().__init__(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=cast(float, self.timeout),  # whole httpx.Timeout, forwarded as-is
            max_retries=max_retries,
            headers=headers,
            httpx_client=self._http_client,
            **kwargs,
        )

    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)
        if name.startswith("_") or name in _OWN_ATTRIBUTES:
            return value
        return _wrap(name, value, super().__getattribute__("_defaults"))

    def copy(
        self,
        *,
        set_default_headers: Mapping[str, str] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        **overrides: Any,
    ) -> AsyncSupermemory:
        """A new client with some options changed; the rest, including the connection pool, are kept."""
        options = dict(self._options)
        if self._owned_http_client:
            options["http_client"] = self._http_client
        options["default_headers"] = set_default_headers or {
            **options["default_headers"],
            **(overrides.pop("default_headers", None) or {}),
        }
        options["default_query"] = set_default_query or {
            **options["default_query"],
            **(overrides.pop("default_query", None) or {}),
        }
        options.update(overrides)
        return type(self)(**options)

    with_options = copy

    async def close(self) -> None:
        if self._owned_http_client:
            await self._http_client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()


Client = Supermemory
AsyncClient = AsyncSupermemory
