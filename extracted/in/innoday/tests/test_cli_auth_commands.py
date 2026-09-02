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
    """Regression: on a team-secret-gated API, /auth/me is behind
    TeamSecretMiddleware. _fetch_me must attach X-Team-Secret when the CLI has
    one, or a valid token gets a 401 at the gate and login looks 'rejected'."""

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
