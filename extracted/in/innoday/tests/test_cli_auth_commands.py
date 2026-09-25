"""
Unit tests for the CLI auth (device-flow) client pieces that don't need a
running server:

- CLIConfig CLI-token storage (store/get/delete) against a mocked keyring,
  including INNODAY_TOKEN env-var precedence.
- InnoDayAPIClient Authorization-header injection when a CLI token is present.

Keyring is mocked with an in-memory dict so nothing touches the real OS
keychain.
"""

import pytest

from src.cli.client import InnoDayAPIClient
from src.cli.config import CLIConfig


@pytest.fixture
def mem_keyring(monkeypatch):
    """Patch the keyring backend used by CLIConfig with an in-memory store."""
    store = {}

    def set_password(service, key, value):
        store[(service, key)] = value

    def get_password(service, key):
        return store.get((service, key))

    def delete_password(service, key):
        if (service, key) not in store:
            import keyring.errors

            raise keyring.errors.PasswordDeleteError("not found")
        del store[(service, key)]

    monkeypatch.setattr("src.cli.config.keyring.set_password", set_password)
    monkeypatch.setattr("src.cli.config.keyring.get_password", get_password)
    monkeypatch.setattr("src.cli.config.keyring.delete_password", delete_password)
    return store


@pytest.fixture
def config(tmp_path, mem_keyring, monkeypatch):
    """A CLIConfig pointed at a throwaway config file, no cwd context."""
    monkeypatch.delenv("INNODAY_TOKEN", raising=False)
    cfg_path = tmp_path / "config.json"
    return CLIConfig(config_path=str(cfg_path), detect_cwd_context=False)


class TestCliTokenStorage:
    def test_store_and_get_round_trip(self, config):
        assert config.get_cli_token() is None
        config.store_cli_token("innoday_abc123")
        assert config.get_cli_token() == "innoday_abc123"

    def test_delete_clears_token(self, config):
        config.store_cli_token("innoday_abc123")
        config.delete_cli_token()
        assert config.get_cli_token() is None

    def test_delete_is_idempotent(self, config):
        # Deleting when nothing is stored must not raise.
        config.delete_cli_token()
        assert config.get_cli_token() is None

    def test_env_var_takes_precedence(self, config, monkeypatch):
        config.store_cli_token("innoday_keyring")
        monkeypatch.setenv("INNODAY_TOKEN", "innoday_env")
        assert config.get_cli_token() == "innoday_env"

    def test_env_var_used_when_no_keyring_value(self, config, monkeypatch):
        monkeypatch.setenv("INNODAY_TOKEN", "innoday_env_only")
        assert config.get_cli_token() == "innoday_env_only"

    def test_token_is_profile_namespaced(self, config, mem_keyring):
        config.store_cli_token("innoday_default")
        # Key is namespaced with the active profile ("default").
        keys = [k for (_, k) in mem_keyring.keys()]
        assert any("default" in k and "cli_token" in k for k in keys)


class TestAuthorizationHeaderInjection:
    def test_bearer_header_set_when_token_present(self, config):
        config.store_cli_token("innoday_bearer_me")
        client = InnoDayAPIClient(config)
        try:
            headers = client.api_client.headers
            assert headers.get("Authorization") == "Bearer innoday_bearer_me"
        finally:
            # AsyncClient close is async; just drop the reference — no I/O done.
            pass

    def test_no_bearer_header_when_no_token(self, config):
        assert config.get_cli_token() is None
        client = InnoDayAPIClient(config)
        assert "Authorization" not in client.api_client.headers

    def test_bearer_and_team_secret_sent_but_never_x_user_id(self, config):
        """Identity is the Bearer token; the door key rides alongside it.

        `X-User-ID` is no longer sent — the API rejects it as an identity source
        because trusting it let any caller past the gate impersonate anyone.
        """
        config.set_user_info("user-1", "u@example.com", "User One")
        config.set_team_secret("s3cr3t")
        config.store_cli_token("innoday_both")
        client = InnoDayAPIClient(config)
        headers = client.api_client.headers
        assert headers.get("Authorization") == "Bearer innoday_both"
        assert headers.get("X-Team-Secret") == "s3cr3t"
        assert "X-User-ID" not in headers


class _CapturingClient:
    """Minimal async-context httpx.AsyncClient stand-in that records the
    headers of the last GET and returns a canned 200 response."""

    captured_headers: dict = {}

    def __init__(self, *a, **kw):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def get(self, url, headers=None):
        _CapturingClient.captured_headers = dict(headers or {})

        class _Resp:
            status_code = 200

            @staticmethod
            def json():
                return {"id": "user-1", "email": "u@example.com", "full_name": "U"}

        return _Resp()


class TestFetchMeTeamSecret:
    """_fetch_me attaches X-Team-Secret when the CLI has one. It was a
    regression fix while a global gate put /auth/me behind the secret (a valid
    token 401'd and login looked 'rejected'); since PF-455 the header is
    harmless there, and still sent for consistency."""

    @pytest.mark.asyncio
    async def test_team_secret_attached_when_configured(self, monkeypatch):
        from src.cli.commands import session

        monkeypatch.setattr(session.httpx, "AsyncClient", _CapturingClient)
        me = await session._fetch_me("https://api", "idt_plat0.tok", "s3cr3t")

        assert me is not None and me["id"] == "user-1"
        assert _CapturingClient.captured_headers.get("X-Team-Secret") == "s3cr3t"
        assert _CapturingClient.captured_headers.get("Authorization") == (
            "Bearer idt_plat0.tok"
        )

    @pytest.mark.asyncio
    async def test_no_team_secret_header_when_none_configured(self, monkeypatch):
        from src.cli.commands import session

        _CapturingClient.captured_headers = {}
        monkeypatch.setattr(session.httpx, "AsyncClient", _CapturingClient)
        await session._fetch_me("https://api", "idt_plat0.tok", None)

        assert "X-Team-Secret" not in _CapturingClient.captured_headers


class _FakeAPIClient:
    """Records what `auth tokens` asked the shared client to do.

    Standing in for `InnoDayAPIClient` rather than for `httpx` is the point:
    the assertion is that this handler goes through the client at all. Building
    its own httpx client is what lost the team-secret header, and a test that
    mocked httpx would have passed either way.
    """

    calls: list = []

    def __init__(self, *a, **kw):
        _FakeAPIClient.calls = []

    async def close(self):
        _FakeAPIClient.calls.append(("close", None, None))

    async def get(self, endpoint, params=None):
        _FakeAPIClient.calls.append(("get", endpoint, None))
        return self._resp(200, [])

    async def post(self, endpoint, json=None, headers=None):
        _FakeAPIClient.calls.append(("post", endpoint, json))
        return self._resp(
            200,
            {"id": "t-1", "name": (json or {}).get("name"), "token": "idt_plat0.raw"},
        )

    async def delete(self, endpoint, headers=None):
        _FakeAPIClient.calls.append(("delete", endpoint, None))
        return self._resp(204, None)

    @staticmethod
    def _resp(code, body):
        class _Resp:
            status_code = code
            text = ""

            @staticmethod
            def json():
                return body

        return _Resp()


class TestTokensGoesThroughTheSharedClient:
    """`innoday auth tokens` answered 401 against every gated deployment.

    It built its own `httpx.AsyncClient` carrying only the Bearer header, so
    the global team-secret gate (removed in PF-455) rejected it before routing
    — and the deployed API always has `TEAM_ACCESS_SECRET` set. Listing or revoking your own tokens
    was impossible from the CLI. `TestFetchMeTeamSecret` above is the same bug
    found in `_fetch_me`; this handler was the copy nobody had hit yet.

    The fix is to use the client, which attaches the secret for you — a rule
    that cannot be forgotten rather than one to remember.
    """

    def _args(self, **over):
        import argparse

        ns = argparse.Namespace(revoke=None, create=None, expires_days=None)
        for k, v in over.items():
            setattr(ns, k, v)
        return ns

    def _run(self, monkeypatch, config, args):
        import asyncio

        from src.cli.commands import auth as auth_cmd

        monkeypatch.setattr(auth_cmd, "InnoDayAPIClient", _FakeAPIClient)
        config.store_cli_token("idt_plat0.tok")
        # Cleared here, not in `__init__`: the refusal path never constructs the
        # client, so a stale list from the previous test would let
        # "no calls were made" pass without meaning anything.
        _FakeAPIClient.calls = []
        return asyncio.run(auth_cmd.AuthCommands._handle_tokens(args, config))

    def test_listing_uses_the_client(self, monkeypatch, config):
        assert self._run(monkeypatch, config, self._args()) == 0
        verbs = [(v, e) for v, e, _ in _FakeAPIClient.calls]
        assert ("get", "/api/v1/auth/tokens") in verbs

    def test_revoking_uses_the_client(self, monkeypatch, config):
        assert self._run(monkeypatch, config, self._args(revoke="t-9")) == 0
        verbs = [(v, e) for v, e, _ in _FakeAPIClient.calls]
        assert ("delete", "/api/v1/auth/tokens/t-9") in verbs

    def test_the_client_is_closed_even_on_the_early_returns(self, monkeypatch, config):
        """`--revoke` and `--create` return from inside the `try`. `finally`
        runs first, so both close — but only because it is unconditional."""
        self._run(monkeypatch, config, self._args(revoke="t-9"))
        assert ("close", None, None) in _FakeAPIClient.calls


class TestCreatingATokenAdds:
    """The browser form revokes every active token before minting. That is the
    right shape for a person who lost theirs, and the wrong one for adding a
    second with a job — a scheduled sweep, a CI runner. Revoking the token your
    own shell is holding in order to hand one to a cron job is a bad afternoon.
    """

    def _args(self, **over):
        return TestTokensGoesThroughTheSharedClient()._args(**over)

    def _run(self, monkeypatch, config, args):
        return TestTokensGoesThroughTheSharedClient()._run(monkeypatch, config, args)

    def test_it_posts_the_name(self, monkeypatch, config):
        assert self._run(monkeypatch, config, self._args(create="routine")) == 0
        posts = [(e, b) for v, e, b in _FakeAPIClient.calls if v == "post"]
        assert posts == [("/api/v1/auth/tokens", {"name": "routine"})]

    def test_it_revokes_nothing(self, monkeypatch, config):
        """The whole reason this exists rather than pointing at the web form."""
        self._run(monkeypatch, config, self._args(create="routine"))
        assert not [v for v, _, _ in _FakeAPIClient.calls if v == "delete"]

    def test_no_expiry_unless_asked(self, monkeypatch, config):
        """`mint_cli_token` leaves `expires_at` NULL when `expires_days` is
        absent. Sending a default would silently expire an unattended job's
        credential; the web path's 90 days is exactly that trap."""
        self._run(monkeypatch, config, self._args(create="routine"))
        [(_, body)] = [(e, b) for v, e, b in _FakeAPIClient.calls if v == "post"]
        assert "expires_days" not in body

    def test_an_expiry_is_passed_through_when_given(self, monkeypatch, config):
        self._run(monkeypatch, config, self._args(create="short", expires_days=7))
        [(_, body)] = [(e, b) for v, e, b in _FakeAPIClient.calls if v == "post"]
        assert body["expires_days"] == 7

    def test_create_and_revoke_together_is_refused(self, monkeypatch, config):
        """They disagree about what should happen to the token you name."""
        code = self._run(monkeypatch, config, self._args(create="x", revoke="t-9"))
        assert code == 1
        assert not _FakeAPIClient.calls
