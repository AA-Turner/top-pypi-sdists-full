import asyncio
import logging
import time
import typing
import urllib.parse

import aiohttp.client_exceptions
import orjson as json
from aiobaseclient import BaseClient
from aiocrossref.exceptions import (
    ClientError,
    NotFoundError,
    ServiceUnavailableError,
    TooManyRequestsError,
    WrongContentTypeError,
)
from izihawa_types.safecast import safe_int
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random,
)


class CrossrefClient(BaseClient):
    def __init__(
        self,
        base_url: str = 'https://api.crossref.org/',
        user_agent: str = None,
        delay: float = 1.0 / 50.0,
        timeout: float = None,
        max_retries=2,
        retry_delay=0.5,
        proxy_url=None,
        ttl_dns_cache=10,
    ):
        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
        super().__init__(
            base_url=base_url,
            default_headers=headers,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            proxy_url=proxy_url,
            ttl_dns_cache=ttl_dns_cache,
        )
        self.delay = delay
        self.last_query_time = 0.0

    def set_limits(self, headers):
        interval = safe_int(headers.get('X-Rate-Limit-Interval', '0').rstrip('s')) or 0
        limit = safe_int(headers.get('X-Rate-Limit-Limit', '1')) or 1
        self.delay = float(interval / limit)

    async def pre_request_hook(self):
        t = time.time()
        if t - self.last_query_time < self.delay:
            await asyncio.sleep(t - self.last_query_time)
        self.last_query_time = t

    @retry(
        reraise=True,
        wait=wait_random(min=1, max=2),
        stop=stop_after_attempt(7),
        retry=retry_if_exception_type((aiohttp.client_exceptions.ClientPayloadError,)),
    )
    async def works(self, doi='', **params):
        r = await self.get(f'/works/{urllib.parse.quote(doi)}', params=params)
        return r['message']

    async def works_cursor(self, doi='', **params):
        failed_cursor = False
        params['cursor'] = '*'
        while True:
            response = await self.works(doi, **params)
            if 'items' in response:
                if len(response['items']) == 0:
                    break
                failed_cursor = False
                yield response
            if 'next-cursor' not in response:
                if not failed_cursor:
                    logging.getLogger('statbox').info({
                        'action': 'failed_next_cursor',
                        'response': response,
                        'request': params,
                        'doi': doi,
                    })
                    failed_cursor = True
                    continue
            params['cursor'] = response['next-cursor']

    async def response_processor(self, response):
        self.set_limits(response.headers)
        try:
            data = await response.read()
        except aiohttp.client_exceptions.ClientPayloadError:
            if response.status == 400:
                raise WrongContentTypeError(data=response.text, status=response.status)
            else:
                raise
        content_type = response.headers.get('Content-Type', '').lower()
        if not response.headers.get('Content-Type', '').lower().startswith('application/json'):
            if response.status == 404:
                raise NotFoundError(data=data, status=response.status, url=str(response.url))
            elif response.status == 429:
                raise TooManyRequestsError(status=response.status, url=str(response.url))
            elif response.status == 502 or response.status == 503 or response.status == 504:
                raise ServiceUnavailableError(status=response.status, url=str(response.url))
            raise WrongContentTypeError(content_type=content_type, data=data, status=response.status)
        try:
            parsed_json = json.loads(data)
        except json.JSONDecodeError:
            raise WrongContentTypeError(content_type=content_type, data=data, status=response.status)
        if (
            isinstance(parsed_json, typing.Dict)
            and (parsed_json.get('status') == 'error' or parsed_json.get('status') == 'failed')
        ):
            message = parsed_json.get('message', {})
            if (
                isinstance(message, typing.Dict)
                and message.get('name') in (
                    'class org.apache.solr.client.solrj.impl.HttpSolrClient$RemoteSolrException',
                    'class com.mongodb.MongoTimeoutException',
                )
            ):
                raise NotFoundError(data=parsed_json, status=response.status, url=str(response.url))
            raise ClientError(**parsed_json)
        return parsed_json
