"""Sync AnyAPI client (SPEC 3.1) and the module-level agent_signup helper.

Generated per-platform namespaces attach lazily. On first access,
``__getattr__(name)`` looks the name up in the generated registry
``getanyapi.platforms.REGISTRY`` and imports the platform module, instantiating its
sync ``Namespace`` class bound to this client.

Namespace-attachment contract (target for the py-emitter):
    ``getanyapi.platforms.__init__`` exposes a module-level dict named ``REGISTRY``
    mapping the client attribute name (the snake_case platform, e.g. "amazon")
    to a 3-tuple ``(module_suffix, sync_class_name, async_class_name)``:

        REGISTRY: dict[str, tuple[str, str, str]] = {
            "amazon": ("amazon", "AmazonNamespace", "AsyncAmazonNamespace"),
            ...
        }

    Each generated module ``getanyapi.platforms.<module_suffix>`` defines both the
    sync class ``<sync_class_name>`` and the async class ``<async_class_name>``.
    Each namespace class has ``__init__(self, client)`` storing the client, and
    per-SKU methods that call ``client._run(slug, input, options)`` (sync) or
    ``client._arun(...)`` (async), plus ``iter_*`` methods returning a
    ``Paginator``/``AsyncPaginator`` via ``getanyapi._pagination.paginate`` /
    ``apaginate``. The sync client instantiates the sync class; the async client
    instantiates the async class. Both look the attribute up by the SAME key in
    the SAME registry, so one generated table drives both clients.

    Namespace instances are cached on the client instance after first access.
"""

from __future__ import annotations

import importlib
import os
import time
from typing import Any, Literal, Protocol, cast

import httpx

from . import _account, _transport
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
    AgentSignupResult,
    Balance,
    CatalogEntry,
    CatalogSearchResults,
    RequestOptions,
    RequestSnapshot,
    RunResult,
)

__all__ = ["AnyAPI", "agent_signup"]

_DEFAULT_BASE_URL = "https://api.getanyapi.com"


def lookup_namespace(name: str) -> tuple[str, str, str] | None:
    """Look ``name`` up in the generated platform registry (typed accessor)."""
    try:
        module = importlib.import_module("getanyapi.platforms")
    except ImportError:
        return None
    registry: dict[str, tuple[str, str, str]] = getattr(module, "REGISTRY", {})
    return registry.get(name)


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key if api_key is not None else os.environ.get("ANYAPI_API_KEY")
    if not key:
        raise AnyAPIError("no API key: pass api_key= or set ANYAPI_API_KEY", status=0)
    return key


class _GetRequest(Protocol):
    def __call__(self, request_id: str) -> RequestSnapshot[Any]: ...


class _WaitRequest(Protocol):
    def __call__(self, request_id: str, *, timeout: float) -> dict[str, Any]: ...


class _Requests:
    """Durable Request retrieval bound to one authenticated client."""

    def __init__(
        self, get: _GetRequest, wait: _WaitRequest, default_timeout: float
    ) -> None:
        self._get = get
        self._wait = wait
        self._default_timeout = default_timeout

    def get(self, request_id: str) -> RequestSnapshot[Any]:
        return self._get(request_id)

    def wait(self, request_id: str, *, timeout: float | None = None) -> RunResult[Any]:
        raw = self._wait(
            request_id,
            timeout=self._default_timeout if timeout is None else timeout,
        )
        return _transport.validate_run_result(raw)


class AnyAPI:
    """Synchronous AnyAPI client (SPEC 3.1).

    Generated per-platform namespaces (``client.amazon``, ``client.facebook``,
    ...) attach lazily via ``__getattr__``; see the module docstring for the
    registry contract the emitter targets.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 300.0,
        max_retries: int = 2,
        idempotency: Literal["auto", "off"] = "auto",
        max_in_progress_wait: float = DEFAULT_MAX_IN_PROGRESS_WAIT,
        http_client: httpx.Client | None = None,
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
        self._http = http_client or httpx.Client(timeout=timeout)
        self._namespaces: dict[str, Any] = {}
        self.requests = _Requests(
            self._get_request, self._wait_request_raw, self._timeout
        )

    # -- generated namespace attachment -----------------------------------

    def __getattr__(self, name: str) -> Any:
        # Only called for attributes not found normally.
        if name.startswith("_"):
            raise AttributeError(name)
        cache = self.__dict__.get("_namespaces")
        if cache is not None and name in cache:
            return cache[name]
        entry = lookup_namespace(name)
        if entry is None:
            raise AttributeError(name)
        module_suffix, sync_class, _async_class = entry
        module = importlib.import_module(f"getanyapi.platforms.{module_suffix}")
        namespace = getattr(module, sync_class)(self)
        if cache is not None:
            cache[name] = namespace
        return namespace

    # -- transport seam ---------------------------------------------------

    def _run_raw(
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
                response = self._http.send(request)
                raw = parse_raw(response)
                if "requestId" not in raw:
                    return raw
                if options and options.get("respond_async"):
                    return raw
                accepted = raw
                break
            except AnyAPIError as exc:
                if is_retryable_error(exc) and retry.can_retry:
                    _transport.sleep(retry.next_delay(response))
                    continue
                if (
                    is_idempotency_in_progress(exc)
                    and retry.can_retry
                    and response is not None
                ):
                    delay = retry.in_progress_delay(response)
                    if delay is not None:
                        _transport.sleep(delay)
                        continue
                raise
            except httpx.TimeoutException as exc:
                raise TimeoutError(str(exc) or "request timed out", status=0) from exc
            except httpx.HTTPError as exc:
                if (
                    is_retryable_error(exc, request_may_be_billed=True)
                    and retry.can_retry
                ):
                    _transport.sleep(retry.next_delay(None))
                    continue
                raise ConnectionError(
                    str(exc) or "connection failed", status=0
                ) from exc
        elapsed = time.monotonic() - started_at
        return self._wait_request_raw(
            str(accepted["requestId"]),
            timeout=max(0.0, timeout - elapsed),
            initial=accepted,
        )

    def start(
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
        raw = self._run_raw(slug, input, start_options)
        if "requestId" in raw:
            return RequestSnapshot[Any].model_validate(raw)
        return _transport.validate_run_result(raw)

    def _get_request(
        self, request_id: str, *, timeout: float | None = None
    ) -> RequestSnapshot[Any]:
        body = self._get(f"/v1/requests/{request_id}", timeout=timeout)
        return RequestSnapshot[Any].model_validate(body)

    def _wait_request_raw(
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
            else self._inspect_before_deadline(request_id, deadline)
        )
        while snapshot.status in ("queued", "running"):
            delay = max(1, snapshot.retry_after_seconds or 2)
            if time.monotonic() + delay > deadline:
                raise RequestPendingError(request_id)
            _transport.sleep(float(delay))
            snapshot = self._inspect_before_deadline(request_id, deadline)
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

    def _inspect_before_deadline(
        self, request_id: str, deadline: float
    ) -> RequestSnapshot[Any]:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RequestPendingError(request_id)
        try:
            return self._get_request(request_id, timeout=remaining)
        except TimeoutError as exc:
            raise RequestPendingError(request_id) from exc

    def _run(
        self,
        slug: str,
        input: dict[str, Any],
        options: RequestOptions | None = None,
    ) -> RunResult[Any]:
        """Execute one SKU run and parse the generic found-data envelope."""
        raw = self._run_raw(slug, input, options)
        return _transport.validate_run_result(raw)

    def run(
        self,
        slug: str,
        input: dict[str, Any],
        *,
        options: RequestOptions | None = None,
    ) -> RunResult[Any]:
        """Generic typed run for any SKU by slug (SPEC 3.1)."""
        return self._run(slug, input, options)

    # -- account + catalog ------------------------------------------------

    def _get(
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
                response = self._http.get(
                    url,
                    params=params or {},
                    headers=headers,
                    timeout=self._timeout if timeout is None else timeout,
                )
                return self._json_or_raise(response)
            except AnyAPIError as exc:
                if is_retryable_error(exc) and retry.can_retry:
                    _transport.sleep(retry.next_delay(response))
                    continue
                raise
            except httpx.TimeoutException as exc:
                raise TimeoutError(str(exc) or "request timed out", status=0) from exc
            except httpx.HTTPError as exc:
                if is_retryable_error(exc) and retry.can_retry:
                    _transport.sleep(retry.next_delay(None))
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

    def balance(self) -> Balance:
        return _account.parse_balance(self._get(_account.balance_path))

    def me(self) -> AccountProfile:
        return _account.parse_me(self._get(_account.me_path))

    def catalog(self, *, category: str | None = None) -> list[CatalogEntry]:
        path, params = _account.catalog_request(category)
        return _account.parse_catalog(self._get(path, params))

    def search(
        self,
        *,
        query: str | None = None,
        category: str | None = None,
        platform: str | None = None,
        limit: int | None = None,
    ) -> CatalogSearchResults:
        path, params = _account.search_request(query, category, platform, limit)
        return _account.parse_search(self._get(path, params))

    def describe(self, slug: str) -> CatalogEntry:
        return _account.parse_describe(self._get(_account.describe_path(slug)))

    # -- lifecycle --------------------------------------------------------

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> AnyAPI:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def agent_signup(
    *,
    base_url: str = _DEFAULT_BASE_URL,
    sponsor_email: str | None = None,
    label: str | None = None,
) -> AgentSignupResult:
    """Self-signup for an API key with no auth (SPEC 3.1, POST /agent/signup)."""
    body = _account.signup_request(sponsor_email, label)
    with httpx.Client(timeout=60.0) as http:
        response = http.post(
            f"{base_url.rstrip('/')}/agent/signup",
            json=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
    request_id = _transport.request_id_of(response)
    parsed: object = None
    try:
        parsed = response.json()
    except ValueError:
        parsed = None
    # The gateway returns 200 for agent signup; accept 200 only (SPEC S7).
    if response.status_code != 200:
        raise _account.map_error(response.status_code, parsed, request_id)
    return _account.parse_signup(parsed)
