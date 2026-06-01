import logging
from collections.abc import Callable
from contextlib import asynccontextmanager
from copy import deepcopy
from inspect import signature
from types import TracebackType
from typing import Any, Self

import httpx
from fastapi import HTTPException
from httpx import AsyncClient, ConnectError, Response, TimeoutException
from httpx._client import USE_CLIENT_DEFAULT, UseClientDefault
from httpx._types import (
    AuthTypes,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
)
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential
from yarl import URL

from csrd.context import get_headers
from csrd.delegate._response_types import ModelHandler, ResponseHandlerMap
from csrd.delegate._retry import RETRY_PROFILES, RetryProfiles
from csrd.models.model_parser import ModelParserMixin, ParsedResponse, ResponseModelType

logger = logging.getLogger(__name__)

# Headers that should never be forwarded in inter-service communication (per RFC 7230)
_HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",  # always computed by httpx for the target service
}

# Additional headers to filter for body-bearing requests to internal services
_INTERNAL_REQUEST_FILTERS = _HOP_BY_HOP_HEADERS | {
    "content-length",  # httpx will compute this for the target service
}


class BaseDelegate(ModelParserMixin):
    """
    A base HTTP delegate class for managing outbound HTTP requests with retry logic,
    dynamic response parsing, and FastAPI integration.
    """

    _filter_headers_list: list[str]
    _client: AsyncClient
    _base_url: URL
    _ignore_incoming_headers: bool

    _retry_enabled: bool
    _retry_profile: RetryProfiles | None
    _retry_attempts: int
    _retry_backoff: float

    _owns_client: bool

    def __init__(
        self,
        service_host: str | URL,
        *,
        client: AsyncClient | None = None,
        header_filter_list: list[str] | None = None,
        ignore_incoming_headers=False,
        retry_enabled: bool = False,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int = 3,
        retry_backoff: float = 0.2,
    ):
        super().__init__()
        self._base_url = URL(service_host)
        self._owns_client = client is None
        self._client = client or AsyncClient(base_url=str(self._base_url))

        # Default filter list includes hop-by-hop headers that cause transport issues
        if header_filter_list is None:
            header_filter_list = list(_HOP_BY_HOP_HEADERS)
        self._filter_headers_list = header_filter_list
        self._ignore_incoming_headers = ignore_incoming_headers

        self._retry_enabled = retry_enabled or (retry_profile is not None)
        self._retry_profile = retry_profile
        self._retry_attempts = retry_attempts
        self._retry_backoff = retry_backoff

    # ── Lifecycle ────────────────────────────────────────────────────────

    async def close(self) -> None:
        """Close the underlying HTTP client if this delegate owns it.

        Safe to call multiple times.  If the caller injected an external
        ``AsyncClient``, this is a no-op (the caller owns that client).
        """
        if self._owns_client and not self._client.is_closed:
            await self._client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    @asynccontextmanager
    async def _request_context(self, method: Callable, **kwargs):
        headers = self._headers or {}
        headers = self._normalize_headers(headers)

        if kwargs.get("headers"):
            user_headers = self._normalize_headers(kwargs["headers"])
            headers.update(user_headers)

        # For body-bearing requests, apply stricter filtering to avoid transport errors
        is_body_bearing = method.__name__ in ("post", "put", "patch")
        kwargs["headers"] = self._filter_headers(headers, strict_mode=is_body_bearing)
        retry_config = self._parse_retry_profile(**kwargs)

        kwargs = self._filter_method_kwargs(method, **kwargs)
        try:
            response = await self._call_with_optional_retry(method, **kwargs, **retry_config)
            yield response
        finally:
            pass

    async def _call_with_optional_retry(
        self,
        method: Callable,
        *,
        retry_enabled: bool | None = None,
        retry_attempts: int | None = None,
        retry_backoff_base: float | None = None,
        **kwargs,
    ) -> Response:
        use_retry = self._retry_enabled if retry_enabled is None else retry_enabled
        attempts = retry_attempts or self._retry_attempts
        backoff = retry_backoff_base or self._retry_backoff
        kwargs = self._filter_method_kwargs(method, **kwargs)

        async def _do_req(**kwargs_) -> Response:
            try:
                response_ = await method(**kwargs_)
                return self._parse_status_code(
                    response_, response_handlers=kwargs_.get("response_handlers")
                )
            except Exception as e_:
                ex = HTTPException(
                    status_code=getattr(e_, "status_code", 500), detail=getattr(e_, "detail", None)
                )
                logger.warning(ex)
                raise ex from e_

        if not use_retry:
            return await _do_req(**kwargs)

        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(attempts),
            wait=wait_exponential(multiplier=backoff),
            retry=retry_if_exception_type(
                (HTTPException, TimeoutException, ConnectError, httpx.HTTPError)
            ),
            reraise=True,
        ):
            with attempt:
                logger.info(f"[attempt {attempt.retry_state.attempt_number}]")
                return await _do_req(**kwargs)
        raise RuntimeError("Unreachable: retry loop exhausted without reraise")

    async def _request(
        self,
        method: Callable,
        *,
        url: URLTypes,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> ParsedResponse:
        async with self._request_context(
            method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            content=content,
            data=data,
            files=files,
            json=json,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        ) as response:
            response = self._parse_status_code(response, response_handlers=response_handlers)
            return self.apply_model(response, model=response_model, model_handler=model_handler)

    # Public HTTP methods
    async def get(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> ParsedResponse:
        return await self._request(
            self._client.get,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            model_handler=model_handler,
            response_model=response_model,
            response_handlers=response_handlers,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        )

    async def delete(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> Any | bytes | dict | None:
        return await self._request(
            self._client.delete,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            model_handler=model_handler,
            response_model=response_model,
            response_handlers=response_handlers,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        )

    async def head(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> ParsedResponse:
        return await self._request(
            self._client.head,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            model_handler=model_handler,
            response_model=response_model,
            response_handlers=response_handlers,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        )

    async def post(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> ParsedResponse:
        return await self._request(
            self._client.post,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            content=content,
            data=data,
            files=files,
            json=json,
            model_handler=model_handler,
            response_model=response_model,
            response_handlers=response_handlers,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        )

    async def put(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> ParsedResponse:
        return await self._request(
            self._client.put,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            model_handler=model_handler,
            response_model=response_model,
            response_handlers=response_handlers,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        )

    async def patch(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> ParsedResponse:
        return await self._request(
            self._client.patch,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            content=content,
            data=data,
            files=files,
            json=json,
            model_handler=model_handler,
            response_model=response_model,
            response_handlers=response_handlers,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        )

    async def options(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        model_handler: ModelHandler | None = None,
        response_model: ResponseModelType | None = None,
        response_handlers: ResponseHandlerMap | None = None,
        retry_enabled: bool | None = None,
        retry_profile: RetryProfiles | None = None,
        retry_attempts: int | None = None,
        retry_backoff: float | None = None,
    ) -> ParsedResponse:
        return await self._request(
            self._client.options,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            model_handler=model_handler,
            response_model=response_model,
            response_handlers=response_handlers,
            retry_enabled=retry_enabled,
            retry_profile=retry_profile,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
        )

    # Helpers
    @property
    def _headers(self) -> dict:
        if self._ignore_incoming_headers:
            return {}
        headers = get_headers()
        return self._filter_headers(dict(headers))

    def _filter_headers(self, headers: dict, strict_mode: bool = False) -> dict:
        """Filter headers, removing hop-by-hop and problematic ones.

        Args:
            headers: Input headers to filter
            strict_mode: If True (for body-bearing requests), also remove content-length
        """
        filters = set(self._filter_headers_list)
        if strict_mode:
            filters = filters | _INTERNAL_REQUEST_FILTERS
        return {k: v for k, v in headers.items() if k.lower() not in filters}

    def _parse_retry_profile(self, **kwargs) -> dict:
        retry_profile = kwargs.pop("retry_profile", self._retry_profile)
        profile_config = deepcopy(RETRY_PROFILES.get(retry_profile, {})) if retry_profile else {}

        return {
            "retry_enabled": kwargs.pop("retry_enabled", None)
            or profile_config.get("retry_enabled")
            or self._retry_enabled,
            "retry_attempts": kwargs.pop("retry_attempts", None)
            or profile_config.get("retry_attempts")
            or self._retry_attempts,
            "retry_backoff": kwargs.pop("retry_backoff", None)
            or profile_config.get("retry_backoff")
            or self._retry_backoff,
        }

    @staticmethod
    def _filter_method_kwargs(method: Callable, **kwargs) -> dict:
        valid_params = set(signature(method).parameters)
        return {k: v for k, v in kwargs.items() if v is not None and k in valid_params}

    @staticmethod
    def _normalize_headers(headers: dict) -> dict:
        result = {}
        for k, v in headers.items():
            lower = k.lower()
            if lower not in result:
                result[lower] = v
        return result

    @staticmethod
    def _parse_status_code(
        response: Response,
        *,
        response_handlers: dict[int, Callable[[Response], Response | None]] | None = None,
    ) -> Response:
        # Prefer handler override if explicitly provided
        if response_handlers and response.status_code in response_handlers:
            result = response_handlers[response.status_code](response)
            return result if result is not None else response

        # Fast-path success
        if 200 <= response.status_code <= 299:
            return response

        try:
            detail = response.json()
        except Exception:
            detail = None

        if isinstance(detail, dict):
            message = detail.get("detail", f"Unexpected status code: {response.status_code}")
        else:
            message = str(detail) if detail else f"Unexpected status code: {response.status_code}"

        raise HTTPException(status_code=response.status_code, detail=message)
