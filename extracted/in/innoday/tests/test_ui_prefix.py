"""The browser pages' addresses, now that innoday-ui serves them.

The pages moved out of this app into innoday-ui, at ``APP_URL``, at the same
``/ui`` paths. What needs guarding is that no address anybody already holds stops
working -- ``/ui/auth/callback`` is where Supabase lands every invite and magic
link, so a broken one locks invitees out the way #414 did:

  1. every ``/ui`` address here 301s to the same path on ``APP_URL``;
  2. the pre-``/ui`` addresses 301 there too, keeping the query string (invite
     emails already delivered carry them, and Supabase's allowlist lists them);
  3. both work without the team secret -- a browser from an email has none;
  4. an ``APP_URL`` pointing back at this host refuses rather than looping.
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


UI = "https://ui.example"


@pytest.fixture
def ui_url(monkeypatch):
    monkeypatch.setenv("APP_URL", UI)


class TestPagePathsCarryTheUiPrefix:
    @pytest.mark.parametrize("path", PAGE_PATHS)
    def test_path_carries_the_ui_prefix(self, path):
        assert path.startswith(f"{UI_PREFIX}/")


class TestOldAddressesRedirectToTheNewUi:
    """Old addresses must keep working: they are in emails we already sent."""

    @pytest.mark.parametrize(
        "path", PAGE_PATHS + [UI_PREFIX, f"{UI_PREFIX}/hs/projects/pf/releases"]
    )
    def test_ui_paths_move_to_the_same_path(self, client, ui_url, path):
        resp = client.get(path, follow_redirects=False)
        assert resp.status_code == 301
        assert resp.headers["location"] == f"{UI}{path}"

    @pytest.mark.parametrize("legacy,target", sorted(LEGACY_REDIRECTS.items()))
    def test_legacy_paths_move_to_the_ui_path(self, client, ui_url, legacy, target):
        resp = client.get(legacy, follow_redirects=False)
        assert resp.status_code == 301
        assert resp.headers["location"] == f"{UI}{target}"

    @pytest.mark.parametrize("path", sorted(LEGACY_REDIRECTS) + [DEVICE_PATH])
    def test_query_string_survives_the_redirect(self, client, ui_url, path):
        # The invite token and the device user_code both ride in the query
        # string; dropping it turns a working link into a blank page.
        resp = client.get(f"{path}?token=abc123&x=1", follow_redirects=False)
        assert resp.status_code == 301
        assert resp.headers["location"].endswith("?token=abc123&x=1")

    def test_app_url_naming_this_host_refuses_instead_of_looping(
        self, client, monkeypatch
    ):
        monkeypatch.setenv("APP_URL", "http://testserver")
        resp = client.get(DEVICE_PATH, follow_redirects=False)
        assert resp.status_code == 404
        assert "innoday-ui" in resp.text


class TestRedirectsNeedNoSecret:
    """A browser arriving from an email cannot send the header."""

    @pytest.mark.parametrize("path", PAGE_PATHS + sorted(LEGACY_REDIRECTS))
    def test_reachable_without_the_header_when_the_gate_is_on(
        self, client, monkeypatch, ui_url, path
    ):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "a-secret-no-browser-has")
        resp = client.get(path, follow_redirects=False)
        assert resp.status_code == 301, f"{path} was gated: {resp.status_code}"


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


class TestEncodedPathsStayUnderUi:
    def test_an_encoded_traversal_is_passed_through_undecoded(self, client, ui_url):
        """Decoded, `..%2f` would climb out of /ui on APP_URL."""
        resp = client.get("/ui/..%2f..%2fx", follow_redirects=False)
        assert resp.status_code == 301
        assert resp.headers["location"] == f"{UI}/ui/..%2f..%2fx"
