"""The standalone files service declares a test session's stamp (2026-10-30).

A ``dev-login`` browser sends ``X-Matrx-Test-Run``; aidream turned it into ``app.test_run`` at every
transaction open, the standalone files service did not — uploads to files.matrxserver.com landed
unstamped. Pinned: the header reaches the ORM session-context provider for exactly the request.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_files.standalone.test_stamp import TestRunMiddleware, test_run_gucs
from test_standalone_session_policy import full_app as _real_app_fixture  # noqa: F401  (the real create_app fixture)

RUN = "0f0f0f0f-1111-4222-8333-444444444444"


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()

    @app.get("/probe")
    async def probe() -> dict:
        return test_run_gucs()

    app.add_middleware(TestRunMiddleware)
    return TestClient(app)


def test_the_header_becomes_the_guc(client: TestClient) -> None:
    assert client.get("/probe", headers={"X-Matrx-Test-Run": RUN}).json() == {"app.test_run": RUN}


def test_no_header_declares_nothing(client: TestClient) -> None:
    assert client.get("/probe").json() == {}
    assert test_run_gucs() == {}


def test_a_malformed_header_declares_nothing(client: TestClient) -> None:
    assert client.get("/probe", headers={"X-Matrx-Test-Run": "drop table"}).json() == {}


def test_the_standalone_app_installs_it(request: pytest.FixtureRequest) -> None:
    """The REAL create_app() wires both halves: the header middleware and the ORM provider."""
    from matrx_orm import configure_session_context
    from matrx_orm.core import session_context

    real = request.getfixturevalue("_real_app_fixture")
    try:
        classes = [m.cls for m in real["app"].user_middleware]
        assert TestRunMiddleware in classes
        from matrx_files.standalone.request_actor import standalone_session_gucs

        assert session_context._provider is standalone_session_gucs
    finally:
        configure_session_context(None)  # process-global: never leak into other tests
