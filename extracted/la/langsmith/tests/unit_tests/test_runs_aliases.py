"""Preserve the public run names used by langsmith-sdk callers."""

import pytest

from langsmith import AsyncLangsmith, Langsmith
from langsmith._httpx import httpx


@pytest.mark.parametrize("method", ["retrieve", "query"])
@pytest.mark.parametrize("wrapper", [None, "with_raw_response", "with_streaming_response"])
def test_runs_aliases(method, wrapper):
    requests = []

    def handle(request):
        requests.append(request)
        data = {"id": "run"} if method == "retrieve" else {"runs": [{"id": "run"}]}
        return httpx.Response(200, json=data)

    with Langsmith(
        api_key="test", base_url="https://example.test", http_client=httpx.Client(transport=httpx.MockTransport(handle))
    ) as client:
        runs = getattr(client.runs, wrapper) if wrapper else client.runs
        call = getattr(runs, method)
        result = call("run", project_id="project") if method == "retrieve" else call()
        if wrapper == "with_streaming_response":
            with result as response:
                response.parse()
        elif wrapper == "with_raw_response":
            result.parse()
        assert requests[0].url.path == ("/api/v2/runs/run" if method == "retrieve" else "/api/v2/runs/query")
        assert requests[0].method == ("GET" if method == "retrieve" else "POST")


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["retrieve", "query"])
@pytest.mark.parametrize("wrapper", [None, "with_raw_response", "with_streaming_response"])
async def test_async_runs_aliases(method, wrapper):
    requests = []

    def handle(request):
        requests.append(request)
        data = {"id": "run"} if method == "retrieve" else {"runs": [{"id": "run"}]}
        return httpx.Response(200, json=data)

    async with AsyncLangsmith(
        api_key="test",
        base_url="https://example.test",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
    ) as client:
        runs = getattr(client.runs, wrapper) if wrapper else client.runs
        call = getattr(runs, method)
        result = call("run", project_id="project") if method == "retrieve" else call()
        if wrapper == "with_streaming_response":
            async with result as response:
                await response.parse()
        else:
            result = await result
            if wrapper == "with_raw_response":
                await result.parse()
        assert requests[0].url.path == ("/api/v2/runs/run" if method == "retrieve" else "/api/v2/runs/query")
        assert requests[0].method == ("GET" if method == "retrieve" else "POST")
