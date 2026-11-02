import asyncio
from typing import Callable, Optional, List
import time
from tenacity import (
    Retrying,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception,
)
import httpx
from calendar import timegm
from pytimeparse import parse as timeparse

from .exceptions import ApiConnectionError, StopAsyncIterationWithResult
from ..types import Response


TIMESTAMP_SKEW = 10

network_retry_strategy = lambda retries=3, retry_type=wait_exponential_jitter: Retrying(
    stop=stop_after_attempt(retries),
    wait=lambda state: network_wait_strategy(state, retry_type),
    retry=retry_if_exception(network_retry_condition),
    reraise=True,
)


def network_get_retry_after(exception):
    if not isinstance(exception, ApiConnectionError):
        return None
    resp = getattr(exception, "response", None)
    if not resp or not resp.headers:
        return None
    headers = resp.headers
    headers = {k.lower(): v for k, v in resp.headers.items()}
    wait_candidates = []

    # Standard Retry-After header (RFC 7231)
    retry_after = headers.get("retry-after")
    if retry_after:
        retry_after = retry_after.strip()
        if retry_after.replace(".", "", 1).isdigit():
            wait_candidates.append(float(retry_after))
        else:
            try:
                retry_time = timegm(
                    time.strptime(retry_after, "%a, %d %b %Y %H:%M:%S GMT")
                )
                delta = retry_time - time.time()
                if delta > 0:
                    wait_candidates.append(delta)
            except Exception:
                pass

    # OpenAI / LiteLLM rate-limit reset headers
    for key in ("x-ratelimit-reset-requests", "x-ratelimit-reset-tokens"):
        val = headers.get(key)
        if not val:
            continue
        val = val.strip()
        if val.replace(".", "", 1).isdigit():
            numeric = float(val)
            now = time.time()
            if numeric > now + TIMESTAMP_SKEW:
                delta = numeric - now
                if delta > 0:
                    wait_candidates.append(delta)
            else:
                if numeric > 0:
                    wait_candidates.append(numeric)
        else:
            try:
                delta = timeparse(val)
                if delta > 0:
                    wait_candidates.append(delta)
            except Exception:
                pass

    if wait_candidates:
        return max(wait_candidates)
    return None


def network_retry_condition(exception):
    if isinstance(exception, httpx.RequestError):
        return True
    if isinstance(exception, ApiConnectionError):
        if hasattr(exception, "response") and exception.response:
            sc = exception.response.status_code
            return (300 <= sc <= 399) or (500 <= sc <= 599) or sc in [429, 408]
        return True
    if isinstance(exception, ConnectionError):
        return True
    return False


def network_wait_strategy(retry_state, default_retry_type=wait_exponential_jitter):
    exception = retry_state.outcome.exception()
    retry_after = network_get_retry_after(exception)
    if retry_after is not None:
        return retry_after
    else:
        return default_retry_type()(retry_state)


class FailCondition:
    def __init__(self, callable: Callable[[Response], bool]):
        self.callable = callable


class ChunksFailCondition:
    def __init__(self, callable: Callable[[List[Response]], bool]):
        self.callable = callable


class ChunksEndCondition:
    def __init__(
        self,
        callable: Callable[[List[Response]], bool],
        timeout: Optional[float] = None,
    ):
        self.callable = callable
        self.timeout = timeout


class TimeoutAsyncGenerator:
    def __init__(self, generator, timeout):
        self.generator = generator
        self.timeout = timeout
        self.start_time = time.monotonic()

    async def __aiter__(self):
        gen_iter = self.generator.__aiter__()
        while True:
            elapsed_time = time.monotonic() - self.start_time
            remaining_time = self.timeout - elapsed_time
            if remaining_time <= 0:
                raise asyncio.TimeoutError()
            try:
                item = await asyncio.wait_for(gen_iter.__anext__(), remaining_time)
                yield item
            except StopAsyncIteration:
                break


def sync_request(
    client,
    module,
    fail_condition=None,
    retry_strategy=network_retry_strategy,
    **request_kwargs,
):
    if not fail_condition:
        fail_condition = FailCondition(callable=lambda resp: resp.status_code != 200)
    for attempt in retry_strategy():
        with attempt:
            response = module.sync_detailed(**request_kwargs, client=client)
        if fail_condition.callable(response):
            raise ApiConnectionError(module.__name__, response, client)
    return response


async def asyncio_request(
    client,
    module,
    fail_condition=None,
    retry_strategy=network_retry_strategy,
    **request_kwargs,
):
    if not fail_condition:
        fail_condition = FailCondition(callable=lambda resp: resp.status_code != 200)
    for attempt in retry_strategy():
        with attempt:
            response = await module.asyncio_detailed(**request_kwargs, client=client)
        if fail_condition.callable(response):
            raise ApiConnectionError(module.__name__, response, client)
    return response


async def streaming_request(
    client,
    module,
    fail_condition=None,
    end_condition=None,
    retry_strategy=network_retry_strategy,
    **request_kwargs,
):
    async def _collect_chunks(
        generator, collected_chunks, fail_condition, end_condition
    ):
        if end_condition.timeout:
            generator = TimeoutAsyncGenerator(generator, end_condition.timeout)
        try:
            async for chunk in generator:
                if fail_condition.callable(collected_chunks + [chunk]):
                    raise ApiConnectionError(module.__name__, chunk, client)
                else:
                    collected_chunks.append(chunk)
                    if end_condition.callable(collected_chunks):
                        raise StopAsyncIterationWithResult(value=collected_chunks)
                    else:
                        yield chunk
        except asyncio.TimeoutError:
            raise StopAsyncIterationWithResult(value=collected_chunks)

    if not fail_condition:
        fail_condition = ChunksFailCondition(
            callable=lambda resps: not resps or resps[0].status_code != 200
        )
    if not end_condition:
        end_condition = ChunksEndCondition(callable=lambda resps: False)
    collected_chunks = []
    for attempt in retry_strategy():
        with attempt:
            generator = module.streaming_detailed(**request_kwargs, client=client)
            generator = _collect_chunks(
                generator, collected_chunks, fail_condition, end_condition
            )
            async for chunk in generator:
                yield chunk
    raise StopAsyncIterationWithResult(value=collected_chunks)


def streaming_get_full_content(responses):
    chunks = [part.content for part in responses if part.content.strip()]
    return b"".join(chunks)
