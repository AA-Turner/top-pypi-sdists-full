"""Unit tests for the Smpl Jobs management namespace (mgmt.jobs) — full surface."""

from __future__ import annotations

import asyncio

import httpx
import pytest

from smplkit._errors import ConflictError, NotFoundError
from smplkit._generated.jobs.client import AuthenticatedClient
from smplkit.management.jobs import AsyncJob, AsyncJobsClient, HttpConfig, Job, JobsClient, Run, Usage

BASE = "https://jobs.example.com"
RUN_ID = "8f2b1c4a-0000-4a1b-9c3d-1e2f3a4b5c6d"
_CFG = HttpConfig(url="https://api.example.com/hook", method="POST", headers=[("X-Api-Key", "secret")], body="{}")


def _job_resource(job_id="my-job", *, created=True, version=1, enabled=True):
    return {
        "id": job_id,
        "type": "job",
        "attributes": {
            "name": "My Job",
            "description": "does a thing",
            "enabled": enabled,
            "type": "http",
            "schedule": "0 * * * *",
            "configuration": {
                "method": "POST",
                "url": "https://api.example.com/hook",
                "headers": [{"name": "X-Api-Key", "value": "secret"}],
                "body": "{}",
                "success_status": "2xx",
                "timeout": 30,
                "tls_verify": True,
                "ca_cert": None,
            },
            "concurrency_policy": "ALLOW",
            "next_run_at": "2026-06-05T00:00:00Z",
            "created_at": "2026-06-04T00:00:00Z" if created else None,
            "updated_at": "2026-06-04T00:00:00Z" if created else None,
            "deleted_at": None,
            "version": version,
        },
    }


def _run_resource(run_id=RUN_ID, status="SUCCEEDED", trigger="SCHEDULE", rerun_of=None):
    return {
        "id": run_id,
        "type": "run",
        "attributes": {
            "job": "my-job",
            "job_version": 1,
            "trigger": trigger,
            "rerun_of": rerun_of,
            "scheduled_for": "2026-06-05T00:00:00Z",
            "status": status,
            "started_at": "2026-06-05T00:00:00.1Z",
            "finished_at": "2026-06-05T00:00:00.4Z",
            "pending_duration_ms": 100,
            "run_duration_ms": 300,
            "total_duration_ms": 400,
            "failure_reason": None,
            "error": None,
            "request": {"method": "POST", "url": "https://api.example.com/hook"},
            "result": {"status": 200},
            "created_at": "2026-06-05T00:00:00Z",
        },
    }


_USAGE = {
    "id": "current",
    "type": "usage",
    "attributes": {
        "period": "2026-06",
        "runs_used": 12,
        "runs_included": 3000,
        "active_jobs": 2,
        "active_jobs_limit": 10,
    },
}


def _handler(req: httpx.Request) -> httpx.Response:
    m, path = req.method, req.url.path
    if path == "/api/v1/jobs" and m == "POST":
        return httpx.Response(201, json={"data": _job_resource()})
    if path == "/api/v1/jobs" and m == "GET":
        return httpx.Response(
            200,
            json={"data": [_job_resource("a"), _job_resource("b")], "meta": {"pagination": {"page": 1, "size": 50}}},
        )
    if path.endswith("/actions/run"):
        return httpx.Response(200, json={"data": _run_resource(trigger="MANUAL")})
    if path.startswith("/api/v1/jobs/") and m == "GET":
        return httpx.Response(200, json={"data": _job_resource()})
    if path.startswith("/api/v1/jobs/") and m == "PUT":
        return httpx.Response(200, json={"data": _job_resource(version=2)})
    if path.startswith("/api/v1/jobs/") and m == "DELETE":
        return httpx.Response(204)
    if path == "/api/v1/usage":
        return httpx.Response(200, json={"data": _USAGE})
    if path == "/api/v1/runs" and m == "GET":
        return httpx.Response(200, json={"data": [_run_resource()], "meta": {"page_size": 50}})
    if path.endswith("/actions/cancel"):
        return httpx.Response(200, json={"data": _run_resource(status="CANCELED")})
    if path.endswith("/actions/rerun"):
        return httpx.Response(200, json={"data": _run_resource(trigger="RERUN", rerun_of=RUN_ID)})
    if path.startswith("/api/v1/runs/") and m == "GET":
        return httpx.Response(200, json={"data": _run_resource()})
    raise AssertionError(f"unexpected {m} {path}")


def _auth(handler=_handler, *, is_async=False) -> AuthenticatedClient:
    a = AuthenticatedClient(
        base_url=BASE, token="sk_test", prefix="Bearer", headers={"Accept": "application/vnd.api+json"}
    )
    if is_async:
        a.set_async_httpx_client(httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url=BASE))
    else:
        a.set_httpx_client(httpx.Client(transport=httpx.MockTransport(handler), base_url=BASE))
    return a


def _sync(handler=_handler) -> JobsClient:
    return JobsClient(auth_client=_auth(handler))


def _async(handler=_handler) -> AsyncJobsClient:
    return AsyncJobsClient(auth_client=_auth(handler, is_async=True))


class TestModels:
    def test_http_config_round_trip_and_defaults(self):
        d = _CFG.to_dict()
        assert d["headers"] == [{"name": "X-Api-Key", "value": "secret"}]
        assert HttpConfig.from_dict(d).headers == [("X-Api-Key", "secret")]
        assert HttpConfig.from_dict({"url": "https://e.com"}).timeout == 30
        assert "HttpConfig" in repr(_CFG)

    def test_run_and_usage_parse(self):
        run = Run._from_resource(_run_resource())
        assert run.status == "SUCCEEDED" and run.total_duration_ms == 400 and "Run(" in repr(run)
        usage = Usage._from_resource(_USAGE)
        assert usage.runs_used == 12 and "Usage(" in repr(usage)

    def test_parse_dt_passthrough(self):
        from datetime import datetime, timezone

        from smplkit.management.jobs import _parse_dt

        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        assert _parse_dt(now) is now and _parse_dt(None) is None

    def test_job_repr_and_unsaved_guards(self):
        j = Job(None, id="x", name="X", schedule="now", configuration=_CFG)
        assert "Job(" in repr(j)
        with pytest.raises(RuntimeError):
            j.save()
        with pytest.raises(RuntimeError):
            j.delete()

    def test_async_job_unsaved_guards(self):
        async def _run():
            j = AsyncJob(None, id="x", name="X", schedule="now", configuration=_CFG)
            with pytest.raises(RuntimeError):
                await j.save()
            with pytest.raises(RuntimeError):
                await j.delete()

        asyncio.run(_run())


class TestSyncSurface:
    def test_create_then_update_via_save(self):
        c = _sync()
        job = c.new("my-job", name="My Job", schedule="0 * * * *", configuration=_CFG, description="d")
        assert job.created_at is None
        job.save()
        assert job.created_at is not None and job.version == 1
        job.name = "renamed"
        job.save()
        assert job.version == 2

    def test_get_list_delete(self):
        c = _sync()
        assert c.get("my-job").configuration.method == "POST"
        assert len(c.list()) == 2
        assert len(c.list(enabled=True, page_number=1, page_size=10)) == 2
        c.delete("my-job")
        c.get("my-job").delete()  # active-record delete with bound client

    def test_run_runs_usage(self):
        c = _sync()
        assert c.run("my-job").trigger == "MANUAL"
        assert len(c.runs.list()) == 1
        assert len(c.runs.list(job="my-job", page_size=2, after="cur")) == 1
        assert c.runs.get(RUN_ID).status == "SUCCEEDED"
        assert c.runs.cancel(RUN_ID).status == "CANCELED"
        assert c.runs.rerun(RUN_ID).trigger == "RERUN"
        assert c.usage().runs_used == 12

    def test_error_mapping(self):
        def h(req):
            code = 404 if req.method == "GET" else 409
            return httpx.Response(code, json={"errors": [{"detail": "x"}]})

        c = _sync(h)
        with pytest.raises(NotFoundError):
            c.get("missing")
        with pytest.raises(ConflictError):
            c.new("dup", name="D", schedule="now", configuration=_CFG).save()


class TestAsyncSurface:
    def test_full_lifecycle(self):
        async def _run():
            c = _async()
            job = c.new("my-job", name="My Job", schedule="0 * * * *", configuration=_CFG)
            await job.save()
            assert job.created_at is not None
            job.name = "renamed"
            await job.save()
            assert job.version == 2
            assert len(await c.list()) == 2
            assert len(await c.list(enabled=False, page_number=1, page_size=5)) == 2
            assert (await c.get("my-job")).id == "my-job"
            await c.delete("my-job")
            await job.delete()

        asyncio.run(_run())

    def test_run_runs_usage(self):
        async def _run():
            c = _async()
            assert (await c.run("my-job")).trigger == "MANUAL"
            assert len(await c.runs.list()) == 1
            assert len(await c.runs.list(job="my-job", page_size=2, after="cur")) == 1
            assert (await c.runs.get(RUN_ID)).status == "SUCCEEDED"
            assert (await c.runs.cancel(RUN_ID)).status == "CANCELED"
            assert (await c.runs.rerun(RUN_ID)).trigger == "RERUN"
            assert (await c.usage()).runs_used == 12

        asyncio.run(_run())
