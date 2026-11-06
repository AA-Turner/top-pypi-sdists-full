import asyncio
import time

import httpx
import pytest

from novita_sandbox import Job, AsyncJob
from novita_sandbox.core.exceptions import TimeoutException


@pytest.mark.asyncio
@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        "zero",
        "deadline",
        "late_success",
        "fast_success",
        "request_limit",
        "disabled_request_limit",
    ],
)
async def test_wait_respects_deadline_and_request_budget(
    monkeypatch, asynchronous, scenario
):
    requests = []

    def response(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "jobId": "job",
                        "status": "migrating"
                        if scenario == "deadline"
                        else "completed",
                    }
                ]
            },
        )

    def sync_handle(request):
        if scenario == "late_success":
            time.sleep(0.06)
        return response(request)

    async def async_handle(request):
        if scenario == "late_success":
            await asyncio.sleep(0.06)
        return response(request)

    transport = httpx.MockTransport(async_handle if asynchronous else sync_handle)
    mode = "async" if asynchronous else "sync"
    monkeypatch.setattr(
        f"novita_sandbox.core.api.client_{mode}.get_transport", lambda _: transport
    )
    cls = AsyncJob if asynchronous else Job
    opts = {
        "api_key": "test-key",
        "domain": "test.invalid",
        "timeout": 0 if scenario == "zero" else 0.03,
        "poll_interval": 0.1,
    }
    if scenario == "request_limit":
        opts["request_timeout"] = 0.005
    if scenario == "disabled_request_limit":
        opts["request_timeout"] = 0

    async def call():
        result = cls.wait("job", **opts)
        return await result if asynchronous else result

    if scenario in ("zero", "deadline", "late_success"):
        with pytest.raises(TimeoutException):
            await call()
    else:
        assert (await call()).status == "completed"
    if scenario == "zero":
        assert requests == []
    if scenario == "deadline":
        assert len(requests) == 1
    if requests:
        limit = requests[0].extensions["timeout"]["read"]
        assert 0 < limit <= (0.005 if scenario == "request_limit" else 0.03)
