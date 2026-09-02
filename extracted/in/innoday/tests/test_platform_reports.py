"""The reporting endpoints must be platform-administrators only.

The underlying views expose user emails across every organization (and, for
v_user_tokens, authentication artifacts), so the gate matters. The database
revokes them from anon/authenticated, but the app connects as a single `postgres`
role that bypasses RLS -- `require_platform_access` is the boundary that actually
holds, so these tests assert it directly.
"""

import pytest

REPORT_PATHS = [
    "/api/v1/platform/reports/project-access",
    "/api/v1/platform/reports/user-tokens",
]


@pytest.mark.parametrize("path", REPORT_PATHS)
def test_anonymous_is_rejected(client, path):
    resp = client.get(path)
    assert resp.status_code in (401, 403), resp.text


@pytest.mark.parametrize("path", REPORT_PATHS)
def test_non_platform_user_is_rejected(client, make_user_with_cli_token, path):
    user, token = make_user_with_cli_token(is_platform_member=False)
    resp = client.get(path, headers={"Authorization": f"Bearer {token}"})
    # 403, not 401: the token is valid and the user is known -- they simply
    # may not do this. 401 would send the CLI to re-authenticate, which cannot help.
    assert resp.status_code == 403, resp.text
    assert "platform access required" in resp.text.lower()


@pytest.mark.parametrize("path", REPORT_PATHS)
def test_platform_member_is_allowed(client, make_user_with_cli_token, path):
    """The views are Postgres-only objects, so on SQLite the query itself fails.
    What matters here is that the request got PAST the platform gate -- a 401
    would mean the gate rejected a platform member."""
    user, token = make_user_with_cli_token(is_platform_member=True)
    resp = client.get(path, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code != 401, resp.text
    assert resp.status_code != 403, resp.text
