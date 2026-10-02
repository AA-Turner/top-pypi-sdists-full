"""Fixtures for the opt-in environment suite. See envkit.py and README.md."""

from __future__ import annotations

import time

import pytest

from tests.environments import envkit


@pytest.fixture
def target():
    """The server this test writes to: the served fake (default) or the one
    ``PROBE_BASE_URL`` / ``PROBE_TOKEN`` named before pytest started."""
    if envkit.REAL:
        assert envkit.REAL_PROJECT, "a real server needs PROBE_E2E_PROJECT (a project slug)"
        yield envkit.Target(
            url=envkit.REAL_URL, token=envkit.REAL_TOKEN, project=envkit.REAL_PROJECT, app=None
        )
        return
    from tests.served_fake_app import serve

    app = _env_fake_app()
    tgt = envkit.make_fake_target(app)
    with serve(app) as url:
        app.upload_base = url
        tgt.url = url
        tgt.reader().create_project(tgt.project, kind="training")
        yield tgt


def _env_fake_app():
    """The agent suite's FakeApp, whose raw-point export also answers with the
    points the SDK POSTed, in the real ``ExportPoint`` shape (the base fake
    exports only points a test seeded). Everything else is the base fake."""
    import re

    import httpx

    from probe.sdk.nonfinite import to_wire
    from tests.conftest import FakeApp

    export = re.compile(r"^/v1/runs/([^/]+)/metrics/export$")

    class EnvFakeApp(FakeApp):
        def handler(self, request: httpx.Request) -> httpx.Response:
            m = export.match(request.url.path)
            if not (m and request.method == "GET"):
                return super().handler(request)
            self.requests.append(request)
            rid = m.group(1)
            rows = list(self.metric_points.get(rid, [])) + list(
                self.metric_points_posted.get(rid, [])
            )
            params = request.url.params
            out = []
            for i, p in enumerate(rows, 1):
                if params.get("key") and p.get("key") != params["key"]:
                    continue
                if params.get("after_id") and i <= int(params["after_id"]):
                    continue
                out.append(
                    to_wire(
                        {
                            "id": i,
                            "step_index": p.get("step_index", p.get("step")),
                            "kind": p.get("kind") or "model",
                            "key": p["key"],
                            "value": p.get("value"),
                            "nonfinite": p.get("nonfinite"),
                            "wall_clock": p.get("wall_clock") or "2026-01-01T00:00:00Z",
                            "dimensions": p.get("dimensions") or {},
                            "labels": p.get("labels") or {},
                            "span_id": p.get("span_id"),
                        }
                    )
                )
            limit = int(params.get("limit") or 1000)
            page, rest = out[:limit], out[limit:]
            return httpx.Response(
                200,
                json={"points": page, "next_after_id": page[-1]["id"] if rest else None},
            )

    return EnvFakeApp()


@pytest.fixture(autouse=True, scope="session")
def _tests_own_their_tmp(tmp_path_factory):
    """pytest's basetemp is where the children are MEANT to write."""
    envkit.ALLOWED_ROOTS.append(tmp_path_factory.getbasetemp().resolve())


@pytest.fixture
def dirs(tmp_path):
    return envkit.make_dirs(tmp_path)


@pytest.fixture
def started():
    """Wall time the test began (for the outside-writes check)."""
    return time.time() - 1.0
