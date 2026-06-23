"""Unit tests for the Smpl Jobs client — full surface.

Jobs has no runtime/management split: one ``JobsClient`` /
``AsyncJobsClient`` reachable as ``client.jobs``, ``mgmt.jobs``, or
standalone. These tests cover the surface plus standalone construction,
transport ownership, and the close/context-manager paths.
"""

from __future__ import annotations

import asyncio
import datetime
import json

import httpx
import pytest

from smplkit import AsyncJobsClient, JobsClient
from smplkit.errors import ConflictError, NotFoundError
from smplkit._generated.jobs.client import AuthenticatedClient
from smplkit.jobs import (
    AsyncJob,
    AsyncRetryPolicy,
    AsyncRun,
    Backoff,
    HttpConfig,
    Job,
    JobEnvironment,
    JobKind,
    RetryPolicy,
    Run,
    RunRetry,
    RunTrigger,
    Usage,
)

BASE = "https://jobs.example.com"
RUN_ID = "8f2b1c4a-0000-4a1b-9c3d-1e2f3a4b5c6d"
_CFG = HttpConfig(url="https://api.example.com/hook", method="POST", headers={"X-Api-Key": "secret"}, body="{}")

# Default environments map (flat sparse overlays, ADR-056): ``production``
# enabled with no overrides (inherits the base) but reporting a read-only per-env
# ``next_run_at``; ``staging`` disabled with per-env ``schedule`` / ``timezone`` /
# ``retry_policy`` plus a ``url`` leaf and a ``headers.<name>`` leaf override.
# Exercises the flat-overlay parse (scalar leaves + a header leaf) and the
# read-only ``next_run_at``.
_DEFAULT_ENVIRONMENTS = {
    "production": {"enabled": True, "next_run_at": "2026-06-05T00:00:00Z"},
    "staging": {
        "enabled": False,
        "schedule": "0 3 * * *",
        "timezone": "Europe/London",
        "retry_policy": "retry-on-5xx",
        "url": "https://staging.example.com/hook",
        "headers.X-Env": "staging",
        "next_run_at": None,
    },
}


def _job_resource(job_id="my-job", *, created=True, version=1, environments="default"):
    if environments == "default":
        environments = _DEFAULT_ENVIRONMENTS
    attributes = {
        "name": "My Job",
        "description": "does a thing",
        "kind": "recurring",
        "type": "http",
        "schedule": "0 * * * *",
        "timezone": "America/New_York",
        "retry_policy": "retry-on-5xx",
        "configuration": {
            "method": "POST",
            "url": "https://api.example.com/hook",
            "headers": {"X-Api-Key": "secret"},
            "body": "{}",
            "success_status": "2xx",
            "timeout": 30,
            "tls_verify": True,
            "ca_cert": None,
        },
        "concurrency_policy": "ALLOW",
        "created_at": "2026-06-04T00:00:00Z" if created else None,
        "updated_at": "2026-06-04T00:00:00Z" if created else None,
        "deleted_at": None,
        "version": version,
    }
    # The server always returns a map (NOT NULL default {}); ``environments=None``
    # here models the key being absent, exercising the wrapper's None-guard.
    if environments is not None:
        attributes["environments"] = environments
    return {"id": job_id, "type": "job", "attributes": attributes}


def _kind_resource(kind):
    """A job resource carrying the given ``kind`` (or none when ``kind`` is None)."""
    res = _job_resource()
    if kind is None:
        del res["attributes"]["kind"]
    else:
        res["attributes"]["kind"] = kind
    return res


def _run_resource(
    run_id=RUN_ID, status="SUCCEEDED", trigger="SCHEDULE", rerun_of=None, environment="production", retry=None
):
    return {
        "id": run_id,
        "type": "run",
        "attributes": {
            "job": "my-job",
            "job_version": 1,
            "environment": environment,
            "trigger": trigger,
            "rerun_of": rerun_of,
            "retry": retry,
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


_RETRY_POLICY_ID = "retry-on-5xx"


def _retry_policy_resource(policy_id=_RETRY_POLICY_ID, *, created=True, version=1, match="default", max_delay=60):
    attributes = {
        "name": "Retry on server errors",
        "max_retries": 5,
        "backoff": "exponential",
        "delay_seconds": 2,
        "created_at": "2026-06-04T00:00:00Z" if created else None,
        "updated_at": "2026-06-04T00:00:00Z" if created else None,
        "deleted_at": None,
        "version": version,
    }
    if max_delay is not None:
        attributes["max_delay_seconds"] = max_delay
    if match == "default":
        attributes["retry_on_timeout"] = True
        attributes["retry_on_connection_error"] = True
        attributes["retry_statuses"] = ["429", "5xx"]
        attributes["retry_statuses_except"] = ["501"]
    # ``match=None`` omits the four fields entirely (server / absent case).
    return {"id": policy_id, "type": "retry_policy", "attributes": attributes}


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
    if path == "/api/v1/retry-policies" and m == "POST":
        return httpx.Response(201, json={"data": _retry_policy_resource()})
    if path == "/api/v1/retry-policies" and m == "GET":
        return httpx.Response(
            200,
            json={
                "data": [_retry_policy_resource("a"), _retry_policy_resource("b")],
                "meta": {"pagination": {"page": 1, "size": 1000}},
            },
        )
    if path.startswith("/api/v1/retry-policies/") and m == "GET":
        return httpx.Response(200, json={"data": _retry_policy_resource()})
    if path.startswith("/api/v1/retry-policies/") and m == "PUT":
        return httpx.Response(200, json={"data": _retry_policy_resource(version=2)})
    if path.startswith("/api/v1/retry-policies/") and m == "DELETE":
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
        assert d["headers"] == {"X-Api-Key": "secret"}
        assert HttpConfig.from_dict(d).headers == {"X-Api-Key": "secret"}
        assert HttpConfig.from_dict({"url": "https://e.com"}).timeout == 30
        # set_header / get_header helpers
        cfg = HttpConfig(url="https://e.com")
        cfg.set_header("Authorization", "Bearer x")
        assert cfg.get_header("Authorization") == "Bearer x"
        assert cfg.get_header("Missing") is None
        assert "HttpConfig" in repr(_CFG)

    def test_run_and_usage_parse(self):
        run = Run._from_resource(_run_resource(environment="staging"))
        assert run.status == "SUCCEEDED" and run.total_duration_ms == 400 and "Run(" in repr(run)
        assert run.environment == "staging"
        # trigger is a plain string, equal to the RunTrigger constant and the raw value
        assert run.trigger == RunTrigger.SCHEDULE and run.trigger == "SCHEDULE"
        usage = Usage._from_resource(_USAGE)
        assert usage.runs_used == 12 and "Usage(" in repr(usage)

    def test_kind_predicates(self):
        from smplkit.jobs.clients import _job_base_from_resource

        rec = _job_base_from_resource(_kind_resource("recurring"))
        assert rec.kind is JobKind.RECURRING
        assert rec.is_recurring() and not rec.is_manual() and not rec.is_one_off()
        man = _job_base_from_resource(_kind_resource("manual"))
        assert man.is_manual() and not man.is_recurring() and not man.is_one_off()
        off = _job_base_from_resource(_kind_resource("one_off"))
        assert off.is_one_off() and not off.is_recurring() and not off.is_manual()
        # a resource with no kind leaves it None — every predicate is False
        nokind = _job_base_from_resource(_kind_resource(None))
        assert nokind.kind is None
        assert not (nokind.is_recurring() or nokind.is_manual() or nokind.is_one_off())

    def test_parse_dt_passthrough(self):
        from datetime import datetime, timezone

        from smplkit.jobs.clients import _parse_dt

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
        job = c.new_recurring_job("my-job", name="My Job", schedule="0 * * * *", configuration=_CFG, description="d")
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
        assert len(c.list(page_number=1, page_size=10)) == 2
        c.delete("my-job")
        c.get("my-job").delete()  # active-record delete with bound client

    def test_list_kind_scheduled_and_name_filters(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.list(kind=JobKind.MANUAL, scheduled=True, name="health")
        params = caps[-1]["params"]
        assert params.get("filter[kind]") == "manual"  # JobKind serialized to its value
        assert params.get("filter[scheduled]") == "true"
        assert params.get("filter[name]") == "health"
        # The dropped recurring filter is never emitted.
        assert "filter[recurring]" not in params

    def test_manual_job_round_trip(self):
        # A manual job is created with no schedule: ``new()`` leaves schedule
        # None, the create body carries ``schedule: null``, and the server
        # echoes back ``kind="manual"`` with no schedule.
        caps: list[dict] = []

        def h(req: httpx.Request) -> httpx.Response:
            caps.append({"method": req.method, "body": json.loads(req.content) if req.content else None})
            if req.url.path == "/api/v1/jobs" and req.method == "POST":
                attrs = _job_resource("manual-job")["attributes"]
                attrs["kind"] = "manual"
                del attrs["schedule"]
                return httpx.Response(201, json={"data": {"id": "manual-job", "type": "job", "attributes": attrs}})
            return _handler(req)

        c = _sync(h)
        job = c.new_manual_job("manual-job", name="Manual", configuration=_CFG)
        assert job.schedule is None  # no schedule supplied
        job.environment("production").enabled = True
        job.save()
        assert job.is_manual() and job.kind is JobKind.MANUAL and job.schedule is None
        post = next(x for x in caps if x["method"] == "POST")
        assert post["body"]["data"]["attributes"]["schedule"] is None  # null sent on the wire

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
            c.new_manual_job("dup", name="D", configuration=_CFG).save()


class TestAsyncSurface:
    def test_full_lifecycle(self):
        async def _run():
            c = _async()
            job = c.new_recurring_job("my-job", name="My Job", schedule="0 * * * *", configuration=_CFG)
            await job.save()
            assert job.created_at is not None
            job.name = "renamed"
            await job.save()
            assert job.version == 2
            assert len(await c.list()) == 2
            assert len(await c.list(page_number=1, page_size=5)) == 2
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

    def test_async_manual_and_schedule_constructors(self):
        async def _run():
            caps: list[dict] = []
            c = AsyncJobsClient(auth_client=_auth(_recording(caps), is_async=True))
            manual = c.new_manual_job("m", name="M", configuration=_CFG)
            assert manual.schedule is None  # no schedule kwarg on the manual constructor
            await manual.save()
            when = datetime.datetime(2030, 6, 1)
            oneoff = c.schedule("o", name="O", schedule=when, configuration=_CFG, environment="staging")
            await oneoff.save()
            post = next(x for x in caps if x["method"] == "POST" and x["body"]["data"]["id"] == "o")
            assert post["body"]["data"]["attributes"]["schedule"] == when.isoformat()
            assert post["env_header"] == "staging"

        asyncio.run(_run())


class TestStandaloneConstructionAndClose:
    """The unified jobs client builds its own transport when constructed
    standalone, and only tears down a transport it owns."""

    def test_standalone_sync_builds_owned_transport_and_closes(self):
        c = JobsClient(api_key="sk_test", base_domain="example.com", scheme="https")
        assert c._owns_transport is True
        # Swap in a mock transport so we can drive a call and populate _client.
        c._auth.set_httpx_client(httpx.Client(transport=httpx.MockTransport(_handler), base_url=BASE))
        assert len(c.list()) == 2
        c.close()
        assert c._auth._client is None
        c.close()  # idempotent: _client already None

    def test_sync_injected_transport_not_closed(self):
        auth = _auth()
        c = JobsClient(auth_client=auth)
        assert c._owns_transport is False
        c.close()  # borrowed transport: no-op
        assert auth._client is not None

    def test_sync_context_manager(self):
        with JobsClient(api_key="sk_test", base_domain="example.com") as c:
            assert isinstance(c, JobsClient)
        assert c._auth._client is None  # nothing opened; exit closed owned transport harmlessly

    def test_standalone_async_builds_owned_transport_and_closes(self):
        async def _run():
            c = AsyncJobsClient(api_key="sk_test", base_domain="example.com")
            assert c._owns_transport is True
            c._auth.set_async_httpx_client(httpx.AsyncClient(transport=httpx.MockTransport(_handler), base_url=BASE))
            assert len(await c.list()) == 2
            await c.aclose()
            assert c._auth._async_client is None
            await c.aclose()  # idempotent

        asyncio.run(_run())

    def test_async_injected_transport_not_closed(self):
        async def _run():
            auth = _auth(is_async=True)
            c = AsyncJobsClient(auth_client=auth)
            assert c._owns_transport is False
            await c.aclose()  # borrowed: no-op
            assert auth._async_client is not None

        asyncio.run(_run())

    def test_async_context_manager(self):
        async def _run():
            async with AsyncJobsClient(api_key="sk_test", base_domain="example.com") as c:
                assert isinstance(c, AsyncJobsClient)

        asyncio.run(_run())


def _recording(captures: list[dict]):
    """A handler that records each request's env header / filter / body, then
    delegates to the shared ``_handler`` for the response."""

    def h(req: httpx.Request) -> httpx.Response:
        captures.append(
            {
                "method": req.method,
                "path": req.url.path,
                "params": dict(req.url.params),
                "env_header": req.headers.get("X-Smplkit-Environment"),
                "filter_env": req.url.params.get("filter[environment]"),
                "body": json.loads(req.content) if req.content else None,
            }
        )
        return _handler(req)

    return h


class TestEnvironmentModelsAndHelpers:
    def test_job_environment_from_dict_branches(self):
        bare = JobEnvironment._from_dict({"enabled": True})
        assert bare.enabled is True and bare.url is None  # no overrides
        assert bare.schedule is None and bare.next_run_at is None  # both absent
        assert bare.timezone is None and bare.headers == {}  # absent leaves
        full = JobEnvironment._from_dict(
            {
                "enabled": False,
                "schedule": "0 6 * * *",
                "timezone": "America/New_York",
                "url": "https://e.com",
                "timeout": 9,
                "headers.Authorization": "Bearer x",
                "headers.X-Foo.Bar": "v",  # dotted header name
                "next_run_at": "2026-06-05T00:00:00Z",
            }
        )
        assert full.enabled is False
        assert full.schedule == "0 6 * * *"  # per-env schedule read back
        assert full.timezone == "America/New_York"  # per-env timezone read back
        assert full.url == "https://e.com" and full.timeout == 9  # request leaves
        assert full.get_header("Authorization") == "Bearer x"
        assert full.get_header("X-Foo.Bar") == "v"  # first-dot parse preserved the name
        # read-only next_run_at parsed back to a datetime
        assert full.next_run_at is not None and full.next_run_at.year == 2026

    def test_job_environment_to_payload_omits_next_run_at(self):
        # next_run_at is read-only: it must never be written back on save, but a
        # per-env schedule override must be.
        env = JobEnvironment(
            enabled=True,
            schedule="0 7 * * *",
            timezone="Europe/London",
            next_run_at=datetime.datetime(2026, 6, 5),
        )
        payload = env._to_payload()
        assert payload == {"enabled": True, "schedule": "0 7 * * *", "timezone": "Europe/London"}
        assert "next_run_at" not in payload
        # with no schedule / timezone override, only enabled is written
        assert JobEnvironment(enabled=False)._to_payload() == {"enabled": False}

    def test_join_environments(self):
        from smplkit.jobs.clients import UNSET, _join_environments

        assert _join_environments(None) is UNSET
        assert _join_environments([]) is UNSET
        assert _join_environments(["production", "staging"]) == "production,staging"

    def test_normalize_environments(self):
        from smplkit.jobs.clients import _normalize_environments

        assert _normalize_environments(None) == {}
        assert _normalize_environments({}) == {}
        passthrough = JobEnvironment(enabled=True)
        out = _normalize_environments(
            {
                "production": passthrough,  # JobEnvironment instance used as-is
                # dict-form = JobEnvironment constructor kwargs (nested headers)
                "staging": {"enabled": True, "url": "https://staging.example.com", "headers": {"X-Env": "staging"}},
                "qa": {"enabled": True, "schedule": "0 8 * * *", "timezone": "Asia/Tokyo"},
            }
        )
        assert out["production"] is passthrough  # instance passed through unchanged
        assert out["staging"].url == "https://staging.example.com"  # dict-form leaf carried through
        assert out["staging"].get_header("X-Env") == "staging"  # dict-form nested headers carried through
        assert out["qa"].url is None  # no request override
        assert out["qa"].schedule == "0 8 * * *"  # dict-form per-env schedule carried through
        assert out["qa"].timezone == "Asia/Tokyo"  # dict-form per-env timezone carried through

    def test_create_sends_dict_form_environment_overrides(self):
        # The documented plain-dict form (flat leaves incl. nested headers) must
        # round-trip through new().save(), emitting the flat headers.<name> shape.
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new_recurring_job(
            "my-job",
            name="My Job",
            schedule="0 * * * *",
            configuration=_CFG,
            environments={
                "staging": {
                    "enabled": True,
                    "url": "https://staging.example.com/x",
                    "headers": {"Authorization": "Bearer s"},
                }
            },
        )
        job.save()
        post = next(x for x in caps if x["method"] == "POST" and x["path"] == "/api/v1/jobs")
        staging = post["body"]["data"]["attributes"]["environments"]["staging"]
        assert staging["enabled"] is True
        assert staging["url"] == "https://staging.example.com/x"
        assert staging["headers.Authorization"] == "Bearer s"  # flat header leaf on the wire
        assert "headers" not in staging  # not a nested object

    def test_environment_handle_overrides(self):
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=_CFG)
        # create-new-entry branch (lazy)
        job.environment("production").enabled = True
        assert job.environments["production"].enabled is True
        # the handle returns the SAME stored object
        assert job.environment("production") is job.environments["production"]
        job.environment("production").enabled = False
        assert job.environments["production"].enabled is False
        # per-env request-leaf overrides emit the flat sparse shape
        stg = job.environment("staging")
        stg.url = "https://staging.example.com/x"
        stg.timeout = 5
        stg.set_header("Authorization", "Bearer s")
        assert job.environments["staging"]._to_payload() == {
            "enabled": False,
            "url": "https://staging.example.com/x",
            "timeout": 5,
            "headers.Authorization": "Bearer s",
        }
        # repr lists the overridden leaves (scalars + headers.<name>)
        r = repr(job.environments["staging"])
        assert "enabled=False" in r and "'url'" in r and "'timeout'" in r and "'headers.Authorization'" in r
        # base configuration is edited directly via the attribute
        new_cfg = HttpConfig(url="https://base.example.com")
        job.configuration = new_cfg
        assert job.configuration is new_cfg

    def test_repr_lists_enabled_environments(self):
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=_CFG)
        job.environment("production").enabled = True
        job.environment("staging").enabled = False
        assert "enabled_in=['production']" in repr(job)

    def test_from_resource_parses_environments(self):
        c = _sync()
        job = c.get("my-job")
        assert job.enabled is True  # derived roll-up (production enabled)
        assert job.kind is JobKind.RECURRING and job.is_recurring()
        assert job.timezone == "America/New_York"  # base timezone decoded off the wire
        prod = job.environments["production"]
        assert prod.enabled is True
        assert prod.url is None  # inherits base (no override)
        assert prod.schedule is None and prod.timezone is None  # inherits base
        # read-only per-env next_run_at parsed back off the wire
        assert prod.next_run_at is not None and prod.next_run_at.year == 2026
        stg = job.environments["staging"]
        assert stg.url == "https://staging.example.com/hook"  # url leaf parsed off the wire
        assert stg.get_header("X-Env") == "staging"  # header leaf parsed off the wire
        assert stg.schedule == "0 3 * * *"  # per-env schedule override
        assert stg.timezone == "Europe/London"  # per-env timezone override
        assert stg.retry_policy == "retry-on-5xx"  # per-env retry policy override
        # next_run_at is null for the disabled environment
        assert stg.next_run_at is None

    def test_enabled_rollup_false_when_all_disabled(self):
        # The derived roll-up is False when no environment is enabled.
        def h(req):
            if req.url.path.startswith("/api/v1/jobs/") and req.method == "GET":
                envs = {"production": {"enabled": False}, "staging": {"enabled": False}}
                return httpx.Response(200, json={"data": _job_resource(environments=envs)})
            return _handler(req)

        job = _sync(h).get("my-job")
        assert job.enabled is False

    def test_from_resource_without_environments(self):
        def h(req):
            if req.url.path.startswith("/api/v1/jobs/") and req.method == "GET":
                return httpx.Response(200, json={"data": _job_resource(environments=None)})
            return _handler(req)

        job = _sync(h).get("my-job")
        assert job.environments == {}


class TestEnvironmentsSync:
    def test_create_sends_environments_map(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new_recurring_job(
            "my-job",
            name="My Job",
            schedule="0 * * * *",
            configuration=_CFG,
            environments={
                "production": JobEnvironment(enabled=True),
                "staging": JobEnvironment(enabled=True, url="https://staging.example.com/hook"),
            },
        )
        job.save()
        body = next(c for c in caps if c["method"] == "POST" and c["path"] == "/api/v1/jobs")
        envs = body["body"]["data"]["attributes"]["environments"]
        assert envs["production"] == {"enabled": True}  # no overrides -> just enabled
        assert envs["staging"]["enabled"] is True
        assert envs["staging"]["url"] == "https://staging.example.com/hook"  # flat leaf override
        # base 'enabled' is never written
        assert "enabled" not in body["body"]["data"]["attributes"]

    def test_create_sends_per_environment_schedule_and_omits_next_run_at(self):
        # A per-env schedule override is sent on save; the read-only next_run_at
        # round-tripped from a prior GET must never be written back.
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new_recurring_job(
            "my-job",
            name="My Job",
            schedule="0 * * * *",
            configuration=_CFG,
            environments={
                "production": JobEnvironment(
                    enabled=True,
                    schedule="0 9 * * *",
                    timezone="Europe/London",
                    next_run_at=datetime.datetime(2026, 6, 5),
                ),
            },
        )
        job.save()
        body = next(c for c in caps if c["method"] == "POST" and c["path"] == "/api/v1/jobs")
        prod = body["body"]["data"]["attributes"]["environments"]["production"]
        assert prod["schedule"] == "0 9 * * *"
        assert prod["timezone"] == "Europe/London"  # per-env timezone sent on save
        assert "next_run_at" not in prod  # read-only: never sent

    def test_create_sends_base_timezone_and_omits_when_unset(self):
        # The base timezone is sent on the wire when set, and omitted entirely
        # (leaving the server default of UTC) when None.
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new_recurring_job("my-job", name="My Job", schedule="0 * * * *", configuration=_CFG)
        job.timezone = "America/New_York"
        assert job.timezone == "America/New_York"
        job.save()
        attrs = next(x for x in caps if x["method"] == "POST" and x["path"] == "/api/v1/jobs")["body"]["data"][
            "attributes"
        ]
        assert attrs["timezone"] == "America/New_York"  # base timezone on the wire

        caps.clear()
        plain = c.new_recurring_job("plain", name="Plain", schedule="0 * * * *", configuration=_CFG)
        plain.save()
        plain_attrs = next(x for x in caps if x["method"] == "POST" and x["path"] == "/api/v1/jobs")["body"]["data"][
            "attributes"
        ]
        assert "timezone" not in plain_attrs  # omitted when unset

    def test_runs_list_explicit_environments_filter(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.runs.list(environments=["production", "staging"])
        assert caps[-1]["filter_env"] == "production,staging"

    def test_runs_list_uses_client_default_environment(self):
        caps: list[dict] = []
        c = JobsClient(auth_client=_auth(_recording(caps)), environment="production")
        c.runs.list()
        assert caps[-1]["filter_env"] == "production"

    def test_runs_list_no_environment_omits_filter(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.runs.list()
        assert caps[-1]["filter_env"] is None

    def test_run_now_environment_header(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.run("my-job", environment="staging")
        assert caps[-1]["env_header"] == "staging"
        # client default applies when no explicit arg
        caps2: list[dict] = []
        c2 = JobsClient(auth_client=_auth(_recording(caps2)), environment="production")
        c2.run("my-job")
        assert caps2[-1]["env_header"] == "production"
        # neither → no header
        caps3: list[dict] = []
        _sync(_recording(caps3)).run("my-job")
        assert caps3[-1]["env_header"] is None

    def test_schedule_one_off_serializes_datetime_and_birth_environment(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        when = datetime.datetime(2030, 1, 1, 12, 30)
        job = c.schedule("one-off", name="One", schedule=when, configuration=_CFG, environment="staging")
        job.save()
        post = next(x for x in caps if x["method"] == "POST" and x["path"] == "/api/v1/jobs")
        assert post["env_header"] == "staging"  # birth environment
        assert post["body"]["data"]["attributes"]["schedule"] == when.isoformat()  # datetime -> ISO-8601

    def test_update_sends_client_default_environment_header(self):
        caps: list[dict] = []
        c = JobsClient(auth_client=_auth(_recording(caps)), environment="production")
        job = c.get("my-job")  # created_at set → save() updates
        job.name = "renamed"
        job.save()
        put = next(x for x in caps if x["method"] == "PUT")
        assert put["env_header"] == "production"


class TestEnvironmentsAsync:
    def test_async_environments_and_headers(self):
        async def _run():
            caps: list[dict] = []
            c = AsyncJobsClient(auth_client=_auth(_recording(caps), is_async=True), environment="production")
            # create with environments map (async _create header = client default)
            job = c.new_recurring_job(
                "my-job",
                name="My Job",
                schedule="0 * * * *",
                configuration=_CFG,
                environments={"production": JobEnvironment(enabled=True)},
            )
            await job.save()
            post = next(x for x in caps if x["method"] == "POST" and x["path"] == "/api/v1/jobs")
            assert post["env_header"] == "production"
            assert post["body"]["data"]["attributes"]["environments"]["production"] == {"enabled": True}
            # run-now with explicit environment header
            await c.run("my-job", environment="staging")
            assert caps[-1]["env_header"] == "staging"
            # runs.list explicit environments filter
            await c.runs.list(environments=["staging"])
            assert caps[-1]["filter_env"] == "staging"
            # parsed run carries its environment
            run = await c.run("my-job")
            assert run.environment == "production"

        asyncio.run(_run())


class TestConvenienceGettersSetters:
    def test_enabled_rollup_and_per_environment(self):
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=_CFG)
        assert job.enabled is False  # derived roll-up default (no envs)
        job.environment("production").enabled = True
        assert job.environment("production").enabled is True  # per-env read
        assert job.environment("staging").enabled is False  # env absent -> created, default off
        # the roll-up is derived: enabling any environment flips it True
        assert job.enabled is True
        # disabling the only enabled environment flips it back
        job.environment("production").enabled = False
        assert job.enabled is False

    def test_environment_config_leaf_overrides(self):
        # Per-env request leaves are pure overrides: a leaf the environment does
        # not override reads as None (the SDK does not merge in the base).
        base = HttpConfig(url="https://base.example.com")
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=base)
        assert job.configuration is base  # base edited directly via the attribute
        prod = job.environment("production")
        assert prod.url is None  # no override yet -> None, not the base url
        prod.url = "https://prod.example.com"
        assert job.environment("production").url == "https://prod.example.com"  # override recorded
        assert job.configuration is base  # base untouched by the per-env override

    def test_base_schedule_and_timezone_via_attributes(self):
        # Base definition is edited directly through attributes (one way).
        job = Job(None, id="x", name="X", schedule="now", configuration=_CFG)
        job.schedule = "0 2 * * *"
        job.timezone = "America/New_York"
        assert job.schedule == "0 2 * * *" and job.timezone == "America/New_York"

    def test_per_environment_schedule_and_timezone_via_handle(self):
        job = Job(None, id="x", name="X", schedule="0 2 * * *", configuration=_CFG)
        # create-new-entry branch
        stg = job.environment("staging")
        stg.schedule = "0 4 * * *"
        stg.timezone = "Europe/London"
        assert job.environments["staging"].schedule == "0 4 * * *"
        assert job.environments["staging"].timezone == "Europe/London"
        # existing-entry branch (the handle returns the same stored object)
        job.environment("staging").schedule = "15 5 * * *"
        assert job.environments["staging"].schedule == "15 5 * * *"
        # the base is untouched by per-env overrides
        assert job.schedule == "0 2 * * *" and job.timezone is None


class TestActiveRecordSync:
    def test_job_trigger_and_list_runs(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.get("my-job")
        run = job.trigger(environment="production")
        assert run.trigger == "MANUAL"
        assert caps[-1]["env_header"] == "production"
        runs = job.list_runs(environment="production")
        assert len(runs) == 1
        assert caps[-1]["filter_env"] == "production"
        # no-environment list omits the filter
        job.list_runs()
        assert caps[-1]["filter_env"] is None

    def test_job_active_record_requires_client(self):
        job = Job(None, id="x", name="X", schedule="now", configuration=_CFG)
        with pytest.raises(RuntimeError):
            job.trigger()
        with pytest.raises(RuntimeError):
            job.list_runs()

    def test_run_rerun_and_cancel(self):
        c = _sync()
        run = c.runs.get(RUN_ID)
        assert run.rerun().trigger == "RERUN"
        assert run.cancel().status == "CANCELED"
        # a run trigger()'d off a Job is also bound and can rerun
        triggered = c.get("my-job").trigger()
        assert triggered.rerun().trigger == "RERUN"

    def test_run_active_record_requires_client(self):
        run = Run._from_resource(_run_resource())  # no runs backref
        with pytest.raises(RuntimeError):
            run.rerun()
        with pytest.raises(RuntimeError):
            run.cancel()


class TestActiveRecordAsync:
    def test_async_job_trigger_and_list_runs(self):
        async def _run():
            caps: list[dict] = []
            c = AsyncJobsClient(auth_client=_auth(_recording(caps), is_async=True), environment="production")
            job = await c.get("my-job")
            run = await job.trigger(environment="development")
            assert run.trigger == "MANUAL"
            assert caps[-1]["env_header"] == "development"
            runs = await job.list_runs(environment="development")
            assert len(runs) == 1
            assert caps[-1]["filter_env"] == "development"
            unbound = AsyncJob(None, id="x", name="X", schedule="now", configuration=_CFG)
            with pytest.raises(RuntimeError):
                await unbound.trigger()
            with pytest.raises(RuntimeError):
                await unbound.list_runs()

        asyncio.run(_run())

    def test_async_run_rerun_and_cancel(self):
        async def _run():
            c = _async()
            run = await c.runs.get(RUN_ID)
            assert (await run.rerun()).trigger == "RERUN"
            assert (await run.cancel()).status == "CANCELED"
            unbound = AsyncRun._from_resource(_run_resource())
            with pytest.raises(RuntimeError):
                await unbound.rerun()
            with pytest.raises(RuntimeError):
                await unbound.cancel()

        asyncio.run(_run())


class TestRetryModels:
    def test_run_retry_parsed_on_retry_trigger(self):
        chain = "11111111-2222-3333-4444-555555555555"
        run = Run._from_resource(_run_resource(trigger="RETRY", retry={"of": chain, "attempt": 2}))
        assert run.trigger == RunTrigger.RETRY and run.trigger == "RETRY"
        assert isinstance(run.retry, RunRetry)
        assert run.retry.of == chain and run.retry.attempt == 2

    def test_run_without_retry_is_none(self):
        # A non-retry run carries no retry chain position.
        assert Run._from_resource(_run_resource()).retry is None


class TestJobRetryPolicy:
    def test_base_retry_policy_round_trip(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        # parsed back off the wire (the fixture sets retry_policy)
        job = c.get("my-job")
        assert job.retry_policy == "retry-on-5xx"
        assert job.environments["staging"].retry_policy == "retry-on-5xx"  # per-env parsed
        assert job.environments["production"].retry_policy is None  # inherits base
        # set base + serialize on save
        job.retry_policy = "retry-aggressive"
        job.save()
        attrs = next(x for x in caps if x["method"] == "PUT")["body"]["data"]["attributes"]
        assert attrs["retry_policy"] == "retry-aggressive"

    def test_base_retry_policy_omitted_when_unset(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new_recurring_job("plain", name="Plain", schedule="0 * * * *", configuration=_CFG)
        assert job.retry_policy is None
        job.save()
        attrs = next(x for x in caps if x["method"] == "POST")["body"]["data"]["attributes"]
        assert "retry_policy" not in attrs

    def test_new_recurring_job_accepts_retry_policy_and_timezone(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new_recurring_job(
            "tz-job",
            name="TZ",
            schedule="0 2 * * *",
            timezone="America/New_York",
            retry_policy="retry-on-5xx",
            configuration=_CFG,
        )
        assert job.timezone == "America/New_York" and job.retry_policy == "retry-on-5xx"
        job.save()
        attrs = next(x for x in caps if x["method"] == "POST")["body"]["data"]["attributes"]
        assert attrs["timezone"] == "America/New_York"
        assert attrs["retry_policy"] == "retry-on-5xx"

    def test_new_manual_and_schedule_accept_retry_policy(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.new_manual_job("m", name="M", configuration=_CFG, retry_policy="retry-on-5xx").save()
        man = next(x for x in caps if x["method"] == "POST" and x["body"]["data"]["id"] == "m")
        assert man["body"]["data"]["attributes"]["retry_policy"] == "retry-on-5xx"
        when = datetime.datetime(2030, 1, 1)
        c.schedule("o", name="O", schedule=when, configuration=_CFG, retry_policy="retry-on-5xx").save()
        off = next(x for x in caps if x["method"] == "POST" and x["body"]["data"]["id"] == "o")
        assert off["body"]["data"]["attributes"]["retry_policy"] == "retry-on-5xx"

    def test_retry_policy_base_and_per_environment(self):
        job = Job(None, id="x", name="X", schedule="0 2 * * *", configuration=_CFG)
        assert job.retry_policy is None
        job.retry_policy = "base-policy"
        assert job.retry_policy == "base-policy"
        # per-env via the handle — create-new-entry branch
        job.environment("staging").retry_policy = "staging-policy"
        assert job.environments["staging"].retry_policy == "staging-policy"
        # existing-entry branch (same stored object)
        job.environment("staging").retry_policy = "staging-policy-2"
        assert job.environments["staging"].retry_policy == "staging-policy-2"
        assert job.retry_policy == "base-policy"  # base untouched

    def test_retry_policy_accepts_object_or_id(self):
        # Assigning a RetryPolicy / AsyncRetryPolicy uses its id; a bare string
        # id is used as-is. The coercion lives on the attribute (base + handle).
        job = Job(None, id="x", name="X", schedule="0 2 * * *", configuration=_CFG)
        policy = RetryPolicy(None, id="retry-on-5xx", name="P", max_retries=1, backoff=Backoff.FIXED, delay_seconds=1)
        job.retry_policy = policy  # base, from object
        assert job.retry_policy == "retry-on-5xx"
        apolicy = AsyncRetryPolicy(
            None, id="retry-async", name="P", max_retries=1, backoff=Backoff.FIXED, delay_seconds=1
        )
        job.environment("staging").retry_policy = apolicy  # per-env, from object
        assert job.environments["staging"].retry_policy == "retry-async"

    def test_env_to_payload_includes_retry_policy(self):
        env = JobEnvironment(enabled=True, retry_policy="retry-on-5xx")
        assert env._to_payload() == {"enabled": True, "retry_policy": "retry-on-5xx"}
        assert "retry_policy" not in JobEnvironment(enabled=True)._to_payload()

    def test_normalize_environments_carries_retry_policy(self):
        from smplkit.jobs.clients import _normalize_environments

        out = _normalize_environments({"staging": {"enabled": True, "retry_policy": "retry-on-5xx"}})
        assert out["staging"].retry_policy == "retry-on-5xx"


class TestRunsListNewFilters:
    def test_triggers_and_last_run_only_params(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.runs.list(triggers=[RunTrigger.SCHEDULE, RunTrigger.RETRY], last_run_only=True)
        params = caps[-1]["params"]
        assert params["filter[trigger]"] == "SCHEDULE,RETRY"
        assert params["last_run_only"] == "true"

    def test_defaults_omit_new_params(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.runs.list()
        params = caps[-1]["params"]
        assert "filter[trigger]" not in params and "last_run_only" not in params

    def test_job_list_runs_passes_new_filters(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.get("my-job").list_runs(triggers=[RunTrigger.RETRY], last_run_only=True)
        params = caps[-1]["params"]
        assert params["filter[trigger]"] == "RETRY"
        assert params["last_run_only"] == "true"

    def test_async_triggers_and_last_run_only(self):
        async def _run():
            caps: list[dict] = []
            c = AsyncJobsClient(auth_client=_auth(_recording(caps), is_async=True))
            await c.runs.list(triggers=[RunTrigger.RETRY], last_run_only=True)
            params = caps[-1]["params"]
            assert params["filter[trigger]"] == "RETRY" and params["last_run_only"] == "true"
            job = await c.get("my-job")
            await job.list_runs(triggers=[RunTrigger.SCHEDULE], last_run_only=True)
            assert caps[-1]["params"]["filter[trigger]"] == "SCHEDULE"

        asyncio.run(_run())


class TestRetryPoliciesSync:
    def test_new_save_creates_then_updates(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        policy = c.retry_policies.new(
            _RETRY_POLICY_ID,
            name="Retry on server errors",
            max_retries=5,
            backoff=Backoff.EXPONENTIAL,
            delay_seconds=2,
            max_delay_seconds=60,
            retry_on_timeout=True,
            retry_on_connection_error=True,
            retry_statuses=["429", "5xx"],
            retry_statuses_except=["501"],
        )
        assert policy.created_at is None
        policy.save()  # create
        assert policy.created_at is not None and policy.version == 1
        post = next(x for x in caps if x["method"] == "POST")["body"]["data"]
        assert post["type"] == "retry_policy" and post["id"] == _RETRY_POLICY_ID
        attrs = post["attributes"]
        assert attrs["backoff"] == "exponential"  # Backoff serialized to its value
        assert attrs["max_delay_seconds"] == 60
        assert attrs["retry_on_timeout"] is True
        assert attrs["retry_on_connection_error"] is True
        assert attrs["retry_statuses"] == ["429", "5xx"]
        assert attrs["retry_statuses_except"] == ["501"]
        policy.name = "renamed"
        policy.save()  # update
        assert policy.version == 2
        assert any(x["method"] == "PUT" for x in caps)

    def test_attributes_omit_max_delay_for_fixed(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.retry_policies.new("fixed", name="Fixed", max_retries=3, backoff=Backoff.FIXED, delay_seconds=5).save()
        attrs = next(x for x in caps if x["method"] == "POST")["body"]["data"]["attributes"]
        assert "max_delay_seconds" not in attrs  # omitted when None
        # All four match fields default to their neutral identity (retry nothing).
        assert attrs["retry_on_timeout"] is False
        assert attrs["retry_on_connection_error"] is False
        assert attrs["retry_statuses"] == []
        assert attrs["retry_statuses_except"] == []

    def test_get_list_delete(self):
        c = _sync()
        policy = c.retry_policies.get(_RETRY_POLICY_ID)
        assert policy.name == "Retry on server errors"
        assert policy.backoff is Backoff.EXPONENTIAL and policy.max_delay_seconds == 60
        assert policy.retry_on_timeout is True and policy.retry_on_connection_error is True
        assert policy.retry_statuses == ["429", "5xx"]
        assert policy.retry_statuses_except == ["501"]
        assert "RetryPolicy(" in repr(policy)
        assert len(c.retry_policies.list()) == 2
        c.retry_policies.delete(_RETRY_POLICY_ID)
        policy.delete()  # active-record delete with bound client

    def test_list_filters(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.retry_policies.list(name="server", page_number=1, page_size=10)
        params = caps[-1]["params"]
        assert params["filter[name]"] == "server"
        assert params["page[number]"] == "1" and params["page[size]"] == "10"

    def test_get_policy_without_match_fields_or_max_delay(self):
        # Match fields absent -> neutral (retry nothing); max_delay absent -> None.
        def h(req):
            if req.url.path.startswith("/api/v1/retry-policies/") and req.method == "GET":
                res = _retry_policy_resource(match=None, max_delay=None)
                return httpx.Response(200, json={"data": res})
            return _handler(req)

        policy = _sync(h).retry_policies.get(_RETRY_POLICY_ID)
        assert policy.retry_on_timeout is False and policy.retry_on_connection_error is False
        assert policy.retry_statuses == [] and policy.retry_statuses_except == []
        assert policy.max_delay_seconds is None

    def test_unsaved_guards(self):
        policy = RetryPolicy(None, id="x", name="X", max_retries=1, backoff=Backoff.FIXED, delay_seconds=1)
        with pytest.raises(RuntimeError):
            policy.save()
        with pytest.raises(RuntimeError):
            policy.delete()


class TestRetryPoliciesAsync:
    def test_full_lifecycle(self):
        async def _run():
            caps: list[dict] = []
            c = AsyncJobsClient(auth_client=_auth(_recording(caps), is_async=True))
            policy = c.retry_policies.new(
                _RETRY_POLICY_ID,
                name="Retry on server errors",
                max_retries=5,
                backoff=Backoff.EXPONENTIAL,
                delay_seconds=2,
                max_delay_seconds=60,
                retry_on_timeout=True,
                retry_statuses=["503", "5xx"],
            )
            await policy.save()
            assert policy.created_at is not None
            policy.name = "renamed"
            await policy.save()
            assert policy.version == 2
            assert len(await c.retry_policies.list(name="server")) == 2
            fetched = await c.retry_policies.get(_RETRY_POLICY_ID)
            assert isinstance(fetched, AsyncRetryPolicy)
            await c.retry_policies.delete(_RETRY_POLICY_ID)
            await fetched.delete()

        asyncio.run(_run())

    def test_unsaved_guards(self):
        async def _run():
            policy = AsyncRetryPolicy(None, id="x", name="X", max_retries=1, backoff=Backoff.FIXED, delay_seconds=1)
            with pytest.raises(RuntimeError):
                await policy.save()
            with pytest.raises(RuntimeError):
                await policy.delete()

        asyncio.run(_run())
