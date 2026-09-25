"""`/platform/health` must not report checks it did not perform.

Two of its five answers used to be incapable of failing:

* ``database_connection`` was the literal ``True``, with the comment
  "We're here, so DB is working" -- it rendered as a green tick beside four
  checks that *can* fail, so an operator read it as a passing database check.
* ``--detailed``'s integrations block returned ``"healthy": True`` under the
  comment "Would validate with actual API call", fabricating a pass for a
  service nothing had contacted.

Both are the shape of bug that reading the code does not catch and running it
does not either -- the endpoint answered 200 with a plausible body throughout.
These tests fail against either fabrication.

The checks are shown to platform admins only (PF-459), so each request here
carries a platform member's token.
"""

from unittest.mock import patch

import pytest

from src.routers import platform as platform_router


@pytest.fixture
def admin(make_user_with_cli_token):
    _, token = make_user_with_cli_token(is_platform_member=True)
    return {"Authorization": f"Bearer {token}"}


def test_database_connection_reports_false_when_the_query_fails(client, admin):
    """The check must reflect the database, not the handler's own liveness.

    Against the previous hardcoded ``True`` this fails: the endpoint reported
    ``database_connection: True`` (and ``status`` unaffected) no matter what
    the database did.
    """
    real_exec = None

    class _DeadSession:
        def __init__(self, inner):
            self._inner = inner

        def exec(self, statement, *a, **kw):
            if "SELECT 1" in str(statement):
                raise RuntimeError("database is gone")
            return self._inner.exec(statement, *a, **kw)

        def __getattr__(self, name):
            return getattr(self._inner, name)

    from src.database import get_session

    app = client.app
    original = app.dependency_overrides.get(get_session)

    def _dead_session():
        gen = original()
        inner = next(gen) if hasattr(gen, "__next__") else gen
        yield _DeadSession(inner)

    app.dependency_overrides[get_session] = _dead_session
    try:
        response = client.get("/api/v1/platform/health", headers=admin)
        assert response.status_code == 200
        body = response.json()
        assert body["checks"]["database_connection"] is False
        # A failed database check must drag the overall verdict down with it.
        assert body["status"] == "degraded"
    finally:
        if original is not None:
            app.dependency_overrides[get_session] = original
        assert real_exec is None


def test_database_connection_reports_true_when_the_query_succeeds(client, admin):
    """The companion direction, so the test above cannot pass by always failing."""
    response = client.get("/api/v1/platform/health", headers=admin)
    assert response.status_code == 200
    assert response.json()["checks"]["database_connection"] is True


def test_configured_integration_is_not_reported_healthy_without_a_check(client, admin):
    """`healthy` is three-valued; None means nothing was proved.

    Nothing in this endpoint contacts a third party, so a configured
    integration must report ``None`` -- never ``True``. Against the previous
    code this fails, because every configured integration answered ``True``.
    """

    class _Org:
        id = "org-1"
        name = "Test Org"
        support_email = "support@example.com"
        website = None
        settings = {"integrations": {"github": {"configured": True}}}

    with patch.object(
        platform_router, "get_platform_organization", return_value=_Org()
    ):
        response = client.get("/api/v1/platform/health?detailed=true", headers=admin)

    assert response.status_code == 200
    github = response.json()["integrations"]["github"]
    assert github["configured"] is True
    assert github["healthy"] is None, (
        "a configured-but-unvalidated integration must not report a pass"
    )
