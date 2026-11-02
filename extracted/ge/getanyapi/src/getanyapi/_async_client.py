"""Async AsyncAnyAPI client (SPEC 3.1).

Mirrors :class:`getanyapi.AnyAPI` with ``async def`` methods, ``aclose``, and an
async context manager. Generated async namespaces attach lazily via
``__getattr__`` using the same ``getanyapi.platforms.REGISTRY`` table as the sync
client (see ``_client`` module docstring for the full contract); the async
client instantiates the registry's async class.
"""

from __future__ import annotations

import asyncio
import importlib
import os
import time
from collections.abc import Awaitable
from typing import Any, Literal, Protocol, cast

import httpx

from . import _account, _transport
from ._client import lookup_namespace
from ._errors import AnyAPIError, ConnectionError, RequestPendingError, TimeoutError
from ._transport import (
    DEFAULT_MAX_IN_PROGRESS_WAIT,
    RetryState,
    build_request,
    is_idempotency_in_progress,
    is_retryable_error,
    parse_raw,
)
from .types import (
    AccountProfile,
    Balance,
    CatalogEntry,
    CatalogSearchResults,
    RequestOptions,
    RequestSnapshot,
    RunResult,
)

__all__ = ["AsyncAnyAPI"]

_DEFAULT_BASE_URL = "https://api.getanyapi.com"


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key if api_key is not None else os.environ.get("ANYAPI_API_KEY")
    if not key:
        raise AnyAPIError("no API key: pass api_key= or set ANYAPI_API_KEY", status=0)
    return key


class _AsyncGetRequest(Protocol):
    def __call__(self, request_id: str) -> Awaitable[RequestSnapshot[Any]]: ...


class _AsyncWaitRequest(Protocol):
    def __call__(
        self, request_id: str, *, timeout: float
    ) -> Awaitable[dict[str, Any]]: ...


class _AsyncRequests:
    """Durable Request retrieval bound to one authenticated async client."""

    def __init__(
        self,
        get: _AsyncGetRequest,
        wait: _AsyncWaitRequest,
        default_timeout: float,
    ) -> None:
        self._get = get
        self._wait = wait
        self._default_timeout = default_timeout

    async def get(self, request_id: str) -> RequestSnapshot[Any]:
        return await self._get(request_id)

    async def wait(
        self, request_id: str, *, timeout: float | None = None
    ) -> RunResult[Any]:
        raw = await self._wait(
            request_id,
            timeout=self._default_timeout if timeout is None else timeout,
        )
        return _transport.validate_run_result(raw)


class AsyncAnyAPI:
    """Asynchronous AnyAPI client (SPEC 3.1)."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 300.0,
        max_retries: int = 2,
        idempotency: Literal["auto", "off"] = "auto",
        max_in_progress_wait: float = DEFAULT_MAX_IN_PROGRESS_WAIT,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = _resolve_api_key(api_key)
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._max_in_progress_wait = max_in_progress_wait
        if idempotency not in ("auto", "off"):
            raise ValueError('idempotency must be "auto" or "off"')
        self._idempotency = idempotency
        self._owns_client = http_client is None
        self._http = http_client or httpx.AsyncClient(timeout=timeout)
        self._namespaces: dict[str, Any] = {}
        self.requests = _AsyncRequests(
            self._get_request, self._wait_request_raw, self._timeout
        )

    # -- generated namespace attachment -----------------------------------

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        cache = self.__dict__.get("_namespaces")
        if cache is not None and name in cache:
            return cache[name]
        entry = lookup_namespace(name)
        if entry is None:
            raise AttributeError(name)
        module_suffix, _sync_class, async_class = entry
        module = importlib.import_module(f"getanyapi.platforms.{module_suffix}")
        namespace = getattr(module, async_class)(self)
        if cache is not None:
            cache[name] = namespace
        return namespace

    # -- transport seam ---------------------------------------------------

    async def _arun_raw(
        self,
        slug: str,
        input: dict[str, Any],
        options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        """Execute one SKU run with retries, returning the raw JSON dict.

        The raw seam generated methods call (SPEC N2): the generated code
        validates this dict into its concrete ``RunResult[XData]`` /
        ``BareRunResult[XData]`` model, so there is no double-parse.
        """
        timeout = self._timeout
        max_retries = self._max_retries
        in_progress_wait = self._max_in_progress_wait
        if options:
            opt_timeout = options.get("timeout")
            if opt_timeout is not None:
                timeout = float(opt_timeout)
            opt_retries = options.get("max_retries")
            if opt_retries is not None:
                max_retries = int(opt_retries)
            opt_wait = options.get("max_in_progress_wait")
            if opt_wait is not None:
                in_progress_wait = float(opt_wait)
        request = build_request(
            base_url=self._base_url,
            slug=slug,
            input=input,
            api_key=self._api_key,
            options=options,
            timeout=timeout,
            idempotency=self._idempotency,
        )
        started_at = time.monotonic()
        retry = RetryState(max_retries, in_progress_wait)
        accepted: dict[str, Any] | None = None
        while True:
            response: httpx.Response | None = None
            try:
                response = await self._http.send(request)
                raw = parse_raw(response)
                if "requestId" not in raw:
                    return raw
                if options and options.get("respond_async"):
                    return raw
                accepted = raw
                break
            except AnyAPIError as exc:
                if is_retryable_error(exc) and retry.can_retry:
                    await asyncio.sleep(retry.next_delay(response))
                    continue
                if (
                    is_idempotency_in_progress(exc)
                    and retry.can_retry
                    and response is not None
                ):
                    delay = retry.in_progress_delay(response)
                    if delay is not None:
                        await asyncio.sleep(delay)
                        continue
                raise
            except httpx.TimeoutException as exc:
                raise TimeoutError(str(exc) or "request timed out", status=0) from exc
            except httpx.HTTPError as exc:
                if (
                    is_retryable_error(exc, request_may_be_billed=True)
                    and retry.can_retry
                ):
                    await asyncio.sleep(retry.next_delay(None))
                    continue
                raise ConnectionError(
                    str(exc) or "connection failed", status=0
                ) from exc
        elapsed = time.monotonic() - started_at
        return await self._wait_request_raw(
            str(accepted["requestId"]),
            timeout=max(0.0, timeout - elapsed),
            initial=accepted,
        )

    async def start(
        self,
        slug: str,
        input: dict[str, Any],
        *,
        options: RequestOptions | None = None,
    ) -> RequestSnapshot[Any] | RunResult[Any]:
        """Start durable work; return a completed same-key replay immediately."""
        start_options = cast(
            "RequestOptions", {**dict(options or {}), "respond_async": True}
        )
        raw = await self._arun_raw(slug, input, start_options)
        if "requestId" in raw:
            return RequestSnapshot[Any].model_validate(raw)
        return _transport.validate_run_result(raw)

    async def _get_request(
        self, request_id: str, *, timeout: float | None = None
    ) -> RequestSnapshot[Any]:
        body = await self._get(f"/v1/requests/{request_id}", timeout=timeout)
        return RequestSnapshot[Any].model_validate(body)

    async def _wait_request_raw(
        self,
        request_id: str,
        *,
        timeout: float,
        initial: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        deadline = time.monotonic() + timeout
        snapshot = (
            RequestSnapshot[Any].model_validate(initial)
            if initial is not None
            else await self._inspect_before_deadline(request_id, deadline)
        )
        while snapshot.status in ("queued", "running"):
            delay = max(1, snapshot.retry_after_seconds or 2)
            if time.monotonic() + delay > deadline:
                raise RequestPendingError(request_id)
            await asyncio.sleep(float(delay))
            snapshot = await self._inspect_before_deadline(request_id, deadline)
        if snapshot.status == "succeeded" and snapshot.result is not None:
            return snapshot.result.model_dump(by_alias=True)
        if snapshot.result_expired:
            raise AnyAPIError(
                "request result expired",
                status=410,
                request_id=request_id,
                code="result_expired",
            )
        code = snapshot.error.get("code") if snapshot.error else None
        raise AnyAPIError(
            f"request ended with {code or snapshot.status}",
            status=502,
            request_id=request_id,
            code=code,
        )

    async def _inspect_before_deadline(
        self, request_id: str, deadline: float
    ) -> RequestSnapshot[Any]:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RequestPendingError(request_id)
        try:
            return await self._get_request(request_id, timeout=remaining)
        except TimeoutError as exc:
            raise RequestPendingError(request_id) from exc

    async def _arun(
        self,
        slug: str,
        input: dict[str, Any],
        options: RequestOptions | None = None,
    ) -> RunResult[Any]:
        """Execute one SKU run and parse the generic found-data envelope."""
        raw = await self._arun_raw(slug, input, options)
        return _transport.validate_run_result(raw)

    async def run(
        self,
        slug: str,
        input: dict[str, Any],
        *,
        options: RequestOptions | None = None,
    ) -> RunResult[Any]:
        """Generic typed run for any SKU by slug (SPEC 3.1)."""
        return await self._arun(slug, input, options)

    # -- account + catalog ------------------------------------------------

    async def _get(
        self,
        path: str,
        params: dict[str, str] | None = None,
        *,
        timeout: float | None = None,
    ) -> object:
        url = f"{self._base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
        }
        retry = RetryState(self._max_retries)
        while True:
            response: httpx.Response | None = None
            try:
                response = await self._http.get(
                    url,
                    params=params or {},
                    headers=headers,
                    timeout=self._timeout if timeout is None else timeout,
                )
                return self._json_or_raise(response)
            except AnyAPIError as exc:
                if is_retryable_error(exc) and retry.can_retry:
                    await asyncio.sleep(retry.next_delay(response))
                    continue
                raise
            except httpx.TimeoutException as exc:
                raise TimeoutError(str(exc) or "request timed out", status=0) from exc
            except httpx.HTTPError as exc:
                if is_retryable_error(exc) and retry.can_retry:
                    await asyncio.sleep(retry.next_delay(None))
                    continue
                raise ConnectionError(
                    str(exc) or "connection failed", status=0
                ) from exc

    def _json_or_raise(self, response: httpx.Response) -> object:
        request_id = _transport.request_id_of(response)
        body: object = None
        try:
            body = response.json()
        except ValueError:
            body = None
        if response.status_code != 200:
            raise _account.map_error(response.status_code, body, request_id)
        return body

    async def balance(self) -> Balance:
        return _account.parse_balance(await self._get(_account.balance_path))

    async def me(self) -> AccountProfile:
        return _account.parse_me(await self._get(_account.me_path))

    async def catalog(self, *, category: str | None = None) -> list[CatalogEntry]:
        path, params = _account.catalog_request(category)
        return _account.parse_catalog(await self._get(path, params))

    async def search(
        self,
        *,
        query: str | None = None,
        category: str | None = None,
        platform: str | None = None,
        limit: int | None = None,
    ) -> CatalogSearchResults:
        path, params = _account.search_request(query, category, platform, limit)
        return _account.parse_search(await self._get(path, params))

    async def describe(self, slug: str) -> CatalogEntry:
        body = await self._get(_account.describe_path(slug))
        return _account.parse_describe(body)

    # -- lifecycle --------------------------------------------------------

    async def aclose(self) -> None:
        if self._owns_client:
            await self._http.aclose()

    async def __aenter__(self) -> AsyncAnyAPI:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()
