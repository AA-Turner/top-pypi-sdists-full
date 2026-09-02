"""The `/ui` page prefix and the 301s from the addresses those pages used to have.

The API half of the app is `/api/v1/*`; the browser pages are `/ui/*`. Both are
served by one process on one host -- `inno.day`'s DNS is at GoDaddy, which cannot
point an apex domain at Railway, so everything consolidated onto `www.inno.day`
and the two halves segment by path instead of by hostname.

What actually needs guarding here is the migration, not the prefix. `/auth/callback`
is where Supabase lands every invite and magic link, so three things must hold or
invitees get locked out the way they were in #414:

  1. the pages answer at their `/ui` addresses;
  2. the pre-`/ui` addresses still answer, as redirects that keep the query string
     (invite emails already delivered carry those paths, and Supabase's allowlist
     still lists them);
  3. *both* sets bypass the team-secret gate -- that middleware runs before
     routing, so an un-exempt legacy path would 401 rather than redirect.
"""

import pytest

from src.page_paths import (
    AUTH_CALLBACK_PATH,
    DEVICE_PATH,
    INVITE_ACCEPT_PATH,
    LEGACY_REDIRECTS,
    UI_PREFIX,
)

PAGE_PATHS = [AUTH_CALLBACK_PATH, INVITE_ACCEPT_PATH, DEVICE_PATH]


class TestPagesLiveUnderUi:
    @pytest.mark.parametrize("path", PAGE_PATHS)
    def test_page_is_served_and_is_html(self, client, path):
        resp = client.get(path)
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/html")

    @pytest.mark.parametrize("path", PAGE_PATHS)
    def test_path_carries_the_ui_prefix(self, path):
        assert path.startswith(f"{UI_PREFIX}/")


class TestLegacyPathsStillRedirect:
    """Old addresses must keep working: they are in emails we already sent."""

    @pytest.mark.parametrize("legacy,target", sorted(LEGACY_REDIRECTS.items()))
    def test_redirects_permanently_to_the_ui_path(self, client, legacy, target):
        resp = client.get(legacy, follow_redirects=False)
        assert resp.status_code == 301
        assert resp.headers["location"] == target

    @pytest.mark.parametrize("legacy,target", sorted(LEGACY_REDIRECTS.items()))
    def test_query_string_survives_the_redirect(self, client, legacy, target):
        # The invite token and the device user_code both ride in the query
        # string; dropping it turns a working link into a blank page.
        resp = client.get(f"{legacy}?token=abc123&x=1", follow_redirects=False)
        assert resp.status_code == 301
        assert resp.headers["location"] == f"{target}?token=abc123&x=1"

    @pytest.mark.parametrize("legacy", sorted(LEGACY_REDIRECTS))
    def test_following_the_redirect_reaches_the_page(self, client, legacy):
        resp = client.get(legacy)
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/html")


class TestTeamSecretExemptions:
    """Both path sets must be exempt, for different reasons.

    The `/ui` pages because a browser arriving from an email cannot send the
    header; the legacy paths because the middleware short-circuits before the
    router, so a 401 would replace the redirect.
    """

    @pytest.mark.parametrize("path", PAGE_PATHS + sorted(LEGACY_REDIRECTS))
    def test_path_is_exempt(self, path):
        from src.api.middleware.team_secret import EXEMPT_PATHS

        assert path in EXEMPT_PATHS

    @pytest.mark.parametrize("path", PAGE_PATHS + sorted(LEGACY_REDIRECTS))
    def test_reachable_without_the_header_when_the_gate_is_on(
        self, client, monkeypatch, path
    ):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "a-secret-no-browser-has")
        resp = client.get(path)
        assert resp.status_code == 200, f"{path} was gated: {resp.status_code}"


class TestOutboundLinksUseTheUiPaths:
    """A literal left behind in a link builder is the failure mode #414 was."""

    def test_device_verification_uri(self, client, monkeypatch):
        monkeypatch.setenv("APP_URL", "https://www.inno.day")
        resp = client.post("/api/v1/device/code", json={"client_id": "innoday-cli"})
        assert resp.status_code == 200
        assert resp.json()["verification_uri"] == f"https://www.inno.day{DEVICE_PATH}"

    def test_invite_accept_url(self, client, db_engine, monkeypatch):
        """The link that actually goes in the invite email."""
        from sqlmodel import Session

        from tests.test_auth_p3_invites import _admin_membership, _org, _user_with_token

        monkeypatch.setenv("APP_URL", "https://www.inno.day")
        with Session(db_engine) as s:
            admin, token = _user_with_token(s, email="admin@ui-prefix.example.com")
            org = _org(s)
            _admin_membership(s, admin.id, org.id)
            org_id = org.id

        resp = client.post(
            f"/api/v1/organizations/{org_id}/invites",
            json={"email": "invitee@ui-prefix.example.com", "role": "DEVELOPER"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200, resp.text
        accept_url = resp.json()["accept_url"]
        assert accept_url.startswith(f"https://www.inno.day{INVITE_ACCEPT_PATH}?token=")

    @pytest.mark.parametrize(
        "module_path", ["src.services.bootstrap", "src.services.user_provisioning"]
    )
    def test_supabase_redirect_builders_import_the_constant(self, module_path):
        """Both `redirect_to` builders must use the shared constant.

        They construct the URL inline, so a stale literal here is invisible until
        an invite email lands on a 404.
        """
        import importlib

        module = importlib.import_module(module_path)
        assert module.AUTH_CALLBACK_PATH == AUTH_CALLBACK_PATH


class TestApiHalfIsUntouched:
    def test_api_routes_keep_their_prefix(self, client):
        # 401, not 404: the route exists and the auth gate is what answers.
        assert client.get("/api/v1/organizations").status_code == 401

    def test_health_is_not_behind_the_ui_prefix(self, client):
        assert client.get("/health").status_code == 200
