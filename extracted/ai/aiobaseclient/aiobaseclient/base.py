import asyncio
import logging
import typing
from typing import Dict, Optional

import aiohttp
import orjson
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp_socks import ProxyConnector
from aiokit import AioThing
from izihawa_loglib.request_context import RequestContext
from izihawa_utils.common import filter_none
from multidict import CIMultiDict
from python_socks import ProxyError, ProxyTimeoutError, parse_proxy_url
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

from .exceptions import (
    AuthorizationRequiredError,
    ClientError,
    ExternalServiceError,
    MethodNotAllowedError,
    NotFoundError,
    ServiceUnavailableError,
    TemporaryError,
    WrongContentTypeError,
)

DEFAULT_REQUEST_CONTEXT_BYPASS = (
    "client_id",
    "request_id",
    "request_source",
)


class BaseClient(AioThing):
    temporary_errors = (TemporaryError,)

    def __init__(
        self,
        base_url: str,
        default_params: Optional[dict] = None,
        default_headers: Optional[dict] = None,
        timeout: Optional[float] = None,
        use_dns_cache: bool = True,
        ttl_dns_cache: int = 10,
        max_retries: Optional[int] = 2,
        retry_delay: Optional[float] = 0.5,
        proxy_url: Optional[str] = None,
        force_close: bool = False,
        connector_limit: int = 512,
        request_context_bypass: tuple[str] | None = None,
    ):
        super().__init__()
        if base_url is None:
            raise RuntimeError(
                f"`base_url` must be passed for {self.__class__.__name__} constructor"
            )
        self.base_url = base_url.rstrip("/")
        self.use_dns_cache = use_dns_cache
        self.ttl_dns_cache = ttl_dns_cache
        self.proxy_url = proxy_url
        self.default_params = CIMultiDict(filter_none(default_params or {}))
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.force_close = force_close
        self.connector_limit = connector_limit
        self.request_context_bypass = (
            request_context_bypass
            if request_context_bypass is not None
            else DEFAULT_REQUEST_CONTEXT_BYPASS
        )
        self.connector = self._create_connector()

        self.request = retry(
            retry=retry_if_exception_type(self.temporary_errors),
            stop=stop_after_attempt(max_retries) if max_retries is not None else None,
            wait=wait_fixed(retry_delay),
            before_sleep=before_sleep_log(
                logging.getLogger("aiobaseclient"), logging.WARNING
            ),
            reraise=True,
        )(self.request)

    def _create_connector(self):
        proxy_kwargs = {}
        if self.proxy_url:
            (
                proxy_kwargs["proxy_type"],
                proxy_kwargs["host"],
                proxy_kwargs["port"],
                proxy_kwargs["username"],
                proxy_kwargs["password"],
            ) = parse_proxy_url(self.proxy_url)
            connector = ProxyConnector(
                use_dns_cache=self.use_dns_cache,
                ttl_dns_cache=self.ttl_dns_cache,
                ssl=False,
                force_close=self.force_close,
                limit=self.connector_limit,
                **proxy_kwargs,
            )
        else:
            connector = aiohttp.TCPConnector(
                use_dns_cache=self.use_dns_cache,
                ttl_dns_cache=self.ttl_dns_cache,
                ssl=False,
                force_close=self.force_close,
                limit=self.connector_limit,
            )
        return connector

    def headers(self, **kwargs):
        return {}

    async def pre_request_hook(self):
        pass

    async def request(
        self,
        method: str = "get",
        url: str = "",
        response_processor=None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        json: Optional[dict] = None,
        data: Optional[bytes] = None,
        timeout: Optional[float] = None,
        request_context: RequestContext | None = None,
        *args,
        **kwargs,
    ) -> typing.Any:
        if response_processor is None:
            response_processor = self.response_processor
        all_params = CIMultiDict(self.default_params)
        if params:
            all_params.update(filter_none(params))
        all_headers = dict(self.default_headers)
        if request_context is not None and self.request_context_bypass:
            for request_context_param in self.request_context_bypass:
                value = request_context.default_fields.get(request_context_param)
                if value is not None:
                    header_name = "x-" + request_context_param.replace("_", "-")
                    all_headers[header_name] = value

        if headers:
            all_headers.update(headers)
        all_headers.update(self.headers(**kwargs))

        full_url = f"{self.base_url}/{url.lstrip('/')}"

        try:
            await self.pre_request_hook()
            if json:
                if data:
                    raise ValueError(
                        "data and json parameters can not be used at the same time"
                    )
                data = orjson.dumps(json)
                if "Content-Type" not in all_headers:
                    all_headers["Content-Type"] = "application/json"
            async with aiohttp.ClientSession(
                connector=self.connector,
                connector_owner=False,
            ) as session:
                response = await session.request(
                    method,
                    full_url,
                    params=params,
                    headers=filter_none(all_headers),
                    data=data,
                    timeout=timeout if timeout is not None else self.timeout,
                )
            if response_processor:
                return await response_processor(response)
            return response
        except (
            ClientConnectorError,
            RuntimeError,
        ) as e:
            raise TemporaryError(url=full_url, nested_error=str(e))
        except (
            aiohttp.client_exceptions.ClientOSError,
            aiohttp.client_exceptions.ServerDisconnectedError,
            aiohttp.client_exceptions.ClientConnectionError,
            asyncio.TimeoutError,
            ConnectionAbortedError,
            ConnectionResetError,
            ProxyError,
            ProxyTimeoutError,
        ) as e:
            raise TemporaryError(url=full_url, nested_error=str(e))

    async def delete(
        self,
        url: str = "",
        *args,
        request_context: RequestContext | None = None,
        **kwargs,
    ) -> typing.Any:
        return await self.request(
            "delete", url, *args, request_context=request_context, **kwargs
        )

    async def get(
        self,
        url: str = "",
        *args,
        request_context: RequestContext | None = None,
        **kwargs,
    ) -> typing.Any:
        return await self.request(
            "get", url, *args, request_context=request_context, **kwargs
        )

    async def head(
        self,
        url: str = "",
        *args,
        request_context: RequestContext | None = None,
        **kwargs,
    ) -> typing.Any:
        return await self.request(
            "head", url, *args, request_context=request_context, **kwargs
        )

    async def post(
        self,
        url: str = "",
        *args,
        request_context: RequestContext | None = None,
        **kwargs,
    ) -> typing.Any:
        return await self.request(
            "post", url, *args, request_context=request_context, **kwargs
        )

    async def put(
        self,
        url: str = "",
        *args,
        request_context: RequestContext | None = None,
        **kwargs,
    ) -> typing.Any:
        return await self.request(
            "put", url, *args, request_context=request_context, **kwargs
        )

    async def stop(self) -> None:
        await self.connector.close()

    async def response_processor(self, response) -> typing.Any:
        text = await response.text()
        if response.status != 200:
            if hasattr(response, "request"):
                raise ExternalServiceError(response.request.url, response.status, text)
            else:
                raise ExternalServiceError(None, response.status, text)
        return text


class BaseStandardClient(BaseClient):
    def __init__(
        self,
        base_url: str,
        default_params: Optional[dict] = None,
        default_headers: Optional[dict] = None,
        timeout: Optional[float] = None,
        use_dns_cache: bool = True,
        ttl_dns_cache: int = 10,
        max_retries: Optional[int] = 2,
        retry_delay: Optional[float] = 0.5,
        proxy_url: Optional[str] = None,
        force_close: bool = False,
        connector_limit: int = 100,
        request_context_bypass: tuple[str] | None = None,
    ):
        super().__init__(
            base_url=base_url,
            default_params=default_params,
            default_headers=default_headers,
            timeout=timeout,
            use_dns_cache=use_dns_cache,
            ttl_dns_cache=ttl_dns_cache,
            max_retries=max_retries,
            retry_delay=retry_delay,
            proxy_url=proxy_url,
            force_close=force_close,
            connector_limit=connector_limit,
            request_context_bypass=request_context_bypass,
        )

    def headers(
        self,
        cache_bypass: bool = True,
        real_ip: Optional[str] = None,
        **kwargs,
    ) -> dict[str, str]:
        return {
            **super().headers(**kwargs),
            "X-Bypass-Cache": "1" if cache_bypass else "0",
            "X-Real-Ip": real_ip,
        }

    async def response_processor(self, response):
        data = await response.read()
        content_type = response.headers.get("Content-Type", "").lower()
        if response.status == 502 or response.status == 503:
            raise ServiceUnavailableError(status=response.status, data=data)
        elif response.status == 401:
            raise AuthorizationRequiredError(
                status=response.status,
                url=str(response.url),
            )
        elif response.status == 404:
            raise NotFoundError(
                status=response.status, data=data, url=str(response.url)
            )
        elif response.status == 405:
            raise MethodNotAllowedError(status=response.status, url=str(response.url))
        else:
            if content_type.startswith("application/json"):
                try:
                    data = orjson.loads(data)
                    if isinstance(data, Dict) and data.get("status") == "error":
                        raise ClientError(**data)
                    return data
                except ValueError:
                    if response.status == 200:
                        return {}
                    raise ClientError(status=response.status, data=data)
            elif content_type.startswith("application/protobuf"):
                return data
            else:
                raise WrongContentTypeError(
                    content_type=content_type, status=response.status, data=data
                )

    async def ping(self, **kwargs):
        return await self.get("/ping/", response_processor=False, **kwargs)
