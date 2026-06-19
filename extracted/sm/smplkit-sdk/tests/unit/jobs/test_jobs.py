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
from smplkit.jobs import AsyncJob, AsyncRun, HttpConfig, Job, JobEnvironment, Run, Usage

BASE = "https://jobs.example.com"
RUN_ID = "8f2b1c4a-0000-4a1b-9c3d-1e2f3a4b5c6d"
_CFG = HttpConfig(url="https://api.example.com/hook", method="POST", headers=[("X-Api-Key", "secret")], body="{}")

# Default environments map: ``production`` enabled with no override (inherits
# base config) but reporting a read-only per-env ``next_run_at``, ``staging``
# disabled with both a per-env ``schedule`` override and a configuration
# override. Exercises both JobEnvironment._from_dict branches (config absent /
# present) plus the per-env schedule and next_run_at fields.
_DEFAULT_ENVIRONMENTS = {
    "production": {"enabled": True, "next_run_at": "2026-06-05T00:00:00Z"},
    "staging": {
        "enabled": False,
        "schedule": "0 3 * * *",
        "configuration": {
            "method": "POST",
            "url": "https://staging.example.com/hook",
            "headers": [],
            "body": "{}",
            "success_status": "2xx",
            "timeout": 30,
            "tls_verify": True,
            "ca_cert": None,
        },
        "next_run_at": None,
    },
}


def _job_resource(job_id="my-job", *, created=True, version=1, environments="default"):
    if environments == "default":
        environments = _DEFAULT_ENVIRONMENTS
    attributes = {
        "name": "My Job",
        "description": "does a thing",
        "recurring": True,
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


def _run_resource(run_id=RUN_ID, status="SUCCEEDED", trigger="SCHEDULE", rerun_of=None, environment="production"):
    return {
        "id": run_id,
        "type": "run",
        "attributes": {
            "job": "my-job",
            "job_version": 1,
            "environment": environment,
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
        run = Run._from_resource(_run_resource(environment="staging"))
        assert run.status == "SUCCEEDED" and run.total_duration_ms == 400 and "Run(" in repr(run)
        assert run.environment == "staging"
        usage = Usage._from_resource(_USAGE)
        assert usage.runs_used == 12 and "Usage(" in repr(usage)

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
        assert len(c.list(page_number=1, page_size=10)) == 2
        c.delete("my-job")
        c.get("my-job").delete()  # active-record delete with bound client

    def test_list_recurring_and_name_filters(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        c.list(recurring=True, name="health")
        params = caps[-1]["params"]
        assert params.get("filter[recurring]") == "true"
        assert params.get("filter[name]") == "health"
        # The dropped enabled filter is never emitted.
        assert "filter[enabled]" not in params

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
        assert bare.enabled is True and bare.configuration is None
        assert bare.schedule is None and bare.next_run_at is None  # both absent
        with_cfg = JobEnvironment._from_dict(
            {
                "enabled": False,
                "schedule": "0 6 * * *",
                "configuration": {"url": "https://e.com"},
                "next_run_at": "2026-06-05T00:00:00Z",
            }
        )
        assert with_cfg.enabled is False
        assert with_cfg.schedule == "0 6 * * *"  # per-env schedule read back
        assert isinstance(with_cfg.configuration, HttpConfig)
        assert with_cfg.configuration.url == "https://e.com"
        # read-only next_run_at parsed back to a datetime
        assert with_cfg.next_run_at is not None and with_cfg.next_run_at.year == 2026

    def test_job_environment_to_payload_omits_next_run_at(self):
        # next_run_at is read-only: it must never be written back on save, but a
        # per-env schedule override must be.
        env = JobEnvironment(
            enabled=True,
            schedule="0 7 * * *",
            next_run_at=datetime.datetime(2026, 6, 5),
        )
        payload = env._to_payload()
        assert payload == {"enabled": True, "schedule": "0 7 * * *"}
        assert "next_run_at" not in payload
        # with no schedule override, only enabled is written
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
        out = _normalize_environments(
            {
                "production": JobEnvironment(enabled=True),  # passthrough instance
                "staging": {"enabled": True, "configuration": _CFG},  # dict w/ HttpConfig instance
                "dev": {"enabled": False, "configuration": {"url": "https://dev.example.com"}},  # dict w/ dict cfg
                "qa": {"enabled": True, "schedule": "0 8 * * *"},  # dict w/ per-env schedule, no configuration
            }
        )
        assert out["production"].enabled is True
        assert out["staging"].configuration is _CFG  # instance passed through unchanged
        # a dict-form configuration is coerced to HttpConfig so it serializes on save
        assert isinstance(out["dev"].configuration, HttpConfig)
        assert out["dev"].configuration.url == "https://dev.example.com"
        assert out["qa"].configuration is None
        assert out["qa"].schedule == "0 8 * * *"  # dict-form per-env schedule carried through

    def test_create_sends_dict_form_environment_configuration(self):
        # The documented plain-dict form (incl. a dict configuration override)
        # must round-trip through new().save() without crashing.
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new(
            "my-job",
            name="My Job",
            schedule="0 * * * *",
            configuration=_CFG,
            environments={"staging": {"enabled": True, "configuration": {"url": "https://staging.example.com/x"}}},
        )
        job.save()
        post = next(x for x in caps if x["method"] == "POST" and x["path"] == "/api/v1/jobs")
        staging = post["body"]["data"]["attributes"]["environments"]["staging"]
        assert staging["enabled"] is True
        assert staging["configuration"]["url"] == "https://staging.example.com/x"

    def test_set_enabled_and_set_configuration(self):
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=_CFG)
        # create-new-entry branch
        job.set_enabled(True, environment="production")
        assert job.environments["production"].enabled is True
        # existing-entry branch
        job.set_enabled(False, environment="production")
        assert job.environments["production"].enabled is False
        # per-env configuration override
        job.set_configuration(_CFG, environment="staging")
        assert job.environments["staging"].configuration is _CFG
        # base configuration (environment=None)
        new_cfg = HttpConfig(url="https://base.example.com")
        job.set_configuration(new_cfg)
        assert job.configuration is new_cfg

    def test_repr_lists_enabled_environments(self):
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=_CFG)
        job.set_enabled(True, environment="production")
        job.set_enabled(False, environment="staging")
        assert "enabled_in=['production']" in repr(job)

    def test_from_resource_parses_environments(self):
        c = _sync()
        job = c.get("my-job")
        assert job.enabled is True  # derived roll-up (production enabled)
        assert job.recurring is True
        assert job.environments["production"].enabled is True
        assert job.environments["production"].configuration is None  # inherits base
        assert job.environments["production"].schedule is None  # inherits base schedule
        # read-only per-env next_run_at parsed back off the wire
        assert job.environments["production"].next_run_at is not None
        assert job.environments["production"].next_run_at.year == 2026
        assert job.environments["staging"].configuration.url == "https://staging.example.com/hook"
        # per-env schedule override parsed back off the wire
        assert job.environments["staging"].schedule == "0 3 * * *"
        # next_run_at is null for the disabled environment
        assert job.environments["staging"].next_run_at is None

    def test_enabled_rollup_false_when_all_disabled(self):
        # The derived roll-up is False when no environment is enabled.
        def h(req):
            if req.url.path.startswith("/api/v1/jobs/") and req.method == "GET":
                envs = {"production": {"enabled": False}, "staging": {"enabled": False}}
                return httpx.Response(200, json={"data": _job_resource(environments=envs)})
            return _handler(req)

        job = _sync(h).get("my-job")
        assert job.enabled is False
        assert job.is_enabled() is False

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
        job = c.new(
            "my-job",
            name="My Job",
            schedule="0 * * * *",
            configuration=_CFG,
            environments={
                "production": JobEnvironment(enabled=True),
                "staging": JobEnvironment(enabled=True, configuration=_CFG),
            },
        )
        job.save()
        body = next(c for c in caps if c["method"] == "POST" and c["path"] == "/api/v1/jobs")
        envs = body["body"]["data"]["attributes"]["environments"]
        assert envs["production"] == {"enabled": True}  # _to_payload config-absent branch
        assert envs["staging"]["enabled"] is True
        assert envs["staging"]["configuration"]["url"] == "https://api.example.com/hook"  # config-present branch
        # base 'enabled' is never written
        assert "enabled" not in body["body"]["data"]["attributes"]

    def test_create_sends_per_environment_schedule_and_omits_next_run_at(self):
        # A per-env schedule override is sent on save; the read-only next_run_at
        # round-tripped from a prior GET must never be written back.
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new(
            "my-job",
            name="My Job",
            schedule="0 * * * *",
            configuration=_CFG,
            environments={
                "production": JobEnvironment(
                    enabled=True,
                    schedule="0 9 * * *",
                    next_run_at=datetime.datetime(2026, 6, 5),
                ),
            },
        )
        job.save()
        body = next(c for c in caps if c["method"] == "POST" and c["path"] == "/api/v1/jobs")
        prod = body["body"]["data"]["attributes"]["environments"]["production"]
        assert prod["schedule"] == "0 9 * * *"
        assert "next_run_at" not in prod  # read-only: never sent

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

    def test_one_off_birth_environment_header_on_create(self):
        caps: list[dict] = []
        c = _sync(_recording(caps))
        job = c.new("one-off", name="One", schedule="now", configuration=_CFG, environment="staging")
        job.save()
        post = next(x for x in caps if x["method"] == "POST" and x["path"] == "/api/v1/jobs")
        assert post["env_header"] == "staging"

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
            job = c.new(
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
    def test_is_enabled(self):
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=_CFG)
        assert job.is_enabled() is False  # derived roll-up default (no envs)
        assert job.enabled is False
        job.set_enabled(True, environment="production")
        assert job.is_enabled(environment="production") is True  # per-env present
        assert job.is_enabled(environment="staging") is False  # env absent from map
        # the roll-up is derived: enabling any environment flips it True
        assert job.is_enabled() is True
        assert job.enabled is True
        # disabling the only enabled environment flips it back
        job.set_enabled(False, environment="production")
        assert job.is_enabled() is False
        assert job.enabled is False

    def test_get_configuration(self):
        base = HttpConfig(url="https://base.example.com")
        job = Job(None, id="x", name="X", schedule="0 * * * *", configuration=base)
        assert job.get_configuration() is base  # base
        assert job.get_configuration(environment="production") is base  # no override -> base
        override = HttpConfig(url="https://prod.example.com")
        job.set_configuration(override, environment="production")
        assert job.get_configuration(environment="production") is override  # override wins
        # an env entry with no configuration still falls back to base
        job.set_enabled(True, environment="staging")
        assert job.get_configuration(environment="staging") is base

    def test_set_schedule(self):
        job = Job(None, id="x", name="X", schedule="now", configuration=_CFG)
        # base schedule (environment=None)
        job.set_schedule("0 2 * * *")
        assert job.schedule == "0 2 * * *"
        # per-environment schedule override — create-new-entry branch
        job.set_schedule("0 4 * * *", environment="staging")
        assert job.environments["staging"].schedule == "0 4 * * *"
        # existing-entry branch (the env already has an override)
        job.set_schedule("15 5 * * *", environment="staging")
        assert job.environments["staging"].schedule == "15 5 * * *"
        # the base schedule is untouched by per-env overrides
        assert job.schedule == "0 2 * * *"


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
