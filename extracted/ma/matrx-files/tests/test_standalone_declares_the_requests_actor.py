"""The standalone files service declares WHO is calling, and the declaration reaches the database (AD282).

Live 2026-11-01: deleting a file attached to a chat answered 500 — "This write declares actor_tier=system, but
names no actor_system. Table: platform.associations". Nothing on this service declared the request's actor, and
its ORM provider forwarded only the test stamp, so even a declaration never reached Postgres.
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_files.standalone.request_actor import request_actor_scope, standalone_session_gucs
from test_standalone_session_policy import full_app as _real_app_fixture  # noqa: F401  (the real create_app fixture)

PERSON = "11111111-2222-4333-8444-555555555555"


def _gucs_inside(ctx: AppContext) -> dict[str, str]:
    async def run() -> dict[str, str]:
        scope = request_actor_scope(ctx)
        if scope is None:
            return standalone_session_gucs()
        async with scope:
            return standalone_session_gucs()

    return asyncio.run(run())


@pytest.mark.parametrize("auth_type", ["token", "fingerprint", "cookie"])
def test_a_persons_request_reaches_the_database_as_that_person(auth_type: str) -> None:
    gucs = _gucs_inside(AppContext(emitter=None, user_id=PERSON, auth_type=auth_type))
    assert gucs["app.actor_tier"] == "user"
    assert gucs["app.actor_system"] == PERSON


def test_an_api_key_names_itself_as_a_system() -> None:
    ctx = AppContext(emitter=None, user_id=PERSON, auth_type="api_key")
    ctx.metadata["api_key_name"] = "nightly-sync"
    gucs = _gucs_inside(ctx)
    assert (gucs["app.actor_tier"], gucs["app.actor_system"]) == ("system", "api_key:nightly-sync")


def test_an_anonymous_caller_declares_nothing() -> None:
    assert "app.actor_tier" not in _gucs_inside(AppContext(emitter=None))


def test_the_real_app_declares_every_admitted_request(request: pytest.FixtureRequest) -> None:
    """The REAL create_app(): AuthMiddleware carries the hook, and the ORM provider forwards it."""
    from matrx_connect.middleware.auth import AuthMiddleware
    from matrx_orm import configure_session_context
    from matrx_orm.core import session_context

    real = request.getfixturevalue("_real_app_fixture")
    try:
        auth = [m for m in real["app"].user_middleware if m.cls is AuthMiddleware]
        assert len(auth) == 1
        assert auth[0].kwargs.get("request_scope") is request_actor_scope
        assert session_context._provider is standalone_session_gucs
    finally:
        configure_session_context(None)  # process-global: never leak into other tests
