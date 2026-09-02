"""The MCP server sends no credential it read from its own environment (#611).

The behavioural half of the fix. `tests/test_server_reads_no_local_credentials.py`
now scans `src/mcp/` and forbids the *reads*; this asserts what the tools put on
the wire, which is the thing that actually leaked.

Why both. The gate is a static scan: it fails on `os.getenv("BOARD_API_TOKEN")`
appearing in the layer. It cannot see a credential arriving by some other route
and being attached to a request, and it cannot tell whether removing the read
left the tool working or merely quiet. These tests set the env vars the removed
code read, then assert the request carries the caller's identity and **no**
`X-Integration-Token` at all.

The hazard being closed, from #611: a supplied `X-Integration-Token` **wins over**
Vault at every sync endpoint (`resolve_board_sync_credential` returns the
caller's token before it looks anything up). So `BOARD_API_TOKEN` in the MCP
server's environment was not a fallback for a board with nothing stored -- it
replaced the board's own credential with one process-wide value shared by every
tenant it served, and `sync_all_boards` picked which one by a `board_type` map
rather than anything tied to the board (#562's shape).

`get_config` is patched throughout so no test reads the real
`~/.innoday/config.json` or the real keyring.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.mcp import server

# Every env name the removed code read. Set together in each test: if any tool
# still consults one of them, the value is distinctive enough to find in the
# recorded request.
BOARD_ENV = {
    "BOARD_API_TOKEN": "operator-board-token",
    "BOARD_API_EMAIL": "operator@example.com",
    "TRELLO_TOKEN": "operator-trello",
    "JIRA_TOKEN": "operator-jira",
    "LINEAR_API_KEY": "operator-linear",
    "NOTION_TOKEN": "operator-notion",
    "GH_TOKEN": "operator-gh",
    "GITHUB_TOKEN": "operator-github",
}


@pytest.fixture
def operator_env(monkeypatch):
    """A process environment holding every credential the tools used to read."""
    for name, value in BOARD_ENV.items():
        monkeypatch.setenv(name, value)
    return BOARD_ENV


@pytest.fixture
def caller_config():
    """A fixed InnoConfig, so `get_user_headers()` builds real headers.

    Patching `get_config` rather than `get_user_headers` keeps the assertion
    about the *identity* header meaningful: the tools must still authenticate as
    the caller, and a test that stubbed out header building could not tell the
    difference between that and sending nothing at all.
    """
    cfg = server.InnoConfig(
        api_url="http://api.test",
        cli_token="caller-token",
        team_secret="team-secret",
    )
    with patch.object(server, "get_config", return_value=cfg):
        yield cfg


def _mock_async_client(response):
    client = AsyncMock()
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    client.get = AsyncMock(return_value=response)
    client.post = AsyncMock(return_value=response)
    return client


def _ok(payload):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = payload
    resp.text = ""
    return resp


def _headers_of(call):
    return call.kwargs.get("headers") or {}


def _assert_no_integration_token(call):
    """No header names an integration token, in any casing.

    Asserting on the *value* alone would pass if the header were sent empty or
    with a differently-sourced credential; asserting on the name alone would
    pass if the value moved into a query parameter. Check both.
    """
    headers = _headers_of(call)
    assert not [k for k in headers if k.lower() == "x-integration-token"], headers
    leaked = [v for v in BOARD_ENV.values() if v in str(call)]
    assert not leaked, f"an operator env credential reached the request: {leaked}"


def _assert_authenticated_as_caller(call):
    headers = _headers_of(call)
    assert headers.get("Authorization") == "Bearer caller-token", headers


class TestSyncBoard:
    @pytest.mark.asyncio
    async def test_sends_no_integration_token_even_with_the_env_vars_set(
        self, operator_env, caller_config
    ):
        client = _mock_async_client(_ok({"status": "sync_started"}))
        with (
            patch.object(server, "httpx") as mock_httpx,
            patch.object(server._api, "resolve_org", return_value="org-1"),
        ):
            mock_httpx.AsyncClient.return_value = client
            result = await server.sync_board(
                board_id="board-1", full_sync=False, dry_run=False, force=False
            )

        assert result == {"status": "sync_started"}
        call = client.post.call_args
        _assert_no_integration_token(call)
        _assert_authenticated_as_caller(call)

    @pytest.mark.asyncio
    async def test_syncs_a_board_when_no_board_env_vars_exist_at_all(
        self, monkeypatch, caller_config
    ):
        """The capability this restores, not just the leak it removes.

        The tool used to return "Integration credentials not configured" and
        make no request whenever `BOARD_API_EMAIL`/`BOARD_API_TOKEN` were unset
        -- which is every deployment that keeps its credentials where they
        belong. A board whose credential is in Vault was unsyncable from MCP.
        """
        for name in BOARD_ENV:
            monkeypatch.delenv(name, raising=False)

        client = _mock_async_client(_ok({"status": "sync_started"}))
        with (
            patch.object(server, "httpx") as mock_httpx,
            patch.object(server._api, "resolve_org", return_value="org-1"),
        ):
            mock_httpx.AsyncClient.return_value = client
            result = await server.sync_board(
                board_id="board-1", full_sync=False, dry_run=False, force=False
            )

        assert "error" not in result
        client.post.assert_awaited_once()


class TestSyncAllBoards:
    @pytest.mark.asyncio
    async def test_neither_the_list_nor_the_sync_call_carries_a_board_token(
        self, operator_env, caller_config
    ):
        """Both requests, because they were broken in opposite directions.

        The per-board sync attached the `board_type`-keyed operator token; the
        list call sent no headers whatsoever, not even the caller's identity.
        """
        boards = [
            {"id": "b-linear", "board_type": "linear", "board_name": "L"},
            {"id": "b-jira", "board_type": "jira", "board_name": "J"},
        ]
        client = _mock_async_client(_ok(boards))
        client.post = AsyncMock(return_value=_ok({"tickets_synced": 3}))

        with (
            patch.object(server, "httpx") as mock_httpx,
            patch.object(server._api, "resolve_org", return_value="org-1"),
        ):
            mock_httpx.AsyncClient.return_value = client
            result = await server.sync_all_boards()

        assert result["synced"] == 2
        for call in [client.get.call_args] + list(client.post.call_args_list):
            _assert_no_integration_token(call)
            _assert_authenticated_as_caller(call)


class TestRegisterBoard:
    @pytest.mark.asyncio
    async def test_refuses_to_register_from_an_env_credential(
        self, operator_env, caller_config
    ):
        """Registration is the one moment a credential is legitimately supplied.

        Supplied by the caller, though -- falling back to the environment writes
        the operator's own token into this tenant's Vault, permanently, where
        every later sync then resolves it and nothing looks like a fallback any
        more.
        """
        client = _mock_async_client(_ok({"id": "board-1"}))
        with (
            patch.object(server, "httpx") as mock_httpx,
            patch.object(server._api, "resolve_org", return_value="org-1"),
        ):
            mock_httpx.AsyncClient.return_value = client
            result = await server.register_board(
                board_url="https://linear.app/acme/team/ENG",
                board_name="Eng",
                board_type="linear",
                integration_token=None,
                user_id="user-1",
                sync=False,
            )

        assert "error" in result
        assert "integration_token" in result["error"]
        client.post.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_an_explicitly_passed_token_is_still_used(
        self, operator_env, caller_config
    ):
        client = _mock_async_client(_ok({"id": "board-1"}))
        with (
            patch.object(server, "httpx") as mock_httpx,
            patch.object(server._api, "resolve_org", return_value="org-1"),
        ):
            mock_httpx.AsyncClient.return_value = client
            result = await server.register_board(
                board_url="https://linear.app/acme/team/ENG",
                board_name="Eng",
                board_type="linear",
                integration_token="callers-own-token",
                user_id="user-1",
                sync=False,
            )

        assert result["registered"] is True
        headers = _headers_of(client.post.call_args)
        assert headers["X-Integration-Token"] == "callers-own-token"
        _assert_authenticated_as_caller(client.post.call_args)


class TestSyncRepository:
    @pytest.mark.asyncio
    async def test_sends_no_github_token_from_the_environment(
        self, operator_env, caller_config
    ):
        """#554's exact shape, in the layer that was outside #554's gate.

        The org's GitHub credential is resolved from Vault by the endpoint
        (`get_github_credentials`); the header this used to send would have
        overridden it with one token shared by every tenant.

        `"error" not in result` is about the *headers*, not about the tool
        working -- the response is canned here, and whether the tool reaches a
        path a route serves is pinned by
        `tests/test_mcp_tools.py::test_sync_repository_reaches_a_path_a_route_serves`
        through the routed transport. Do not read this test as coverage of either.
        """
        client = _mock_async_client(_ok({"sync_id": "s-1", "status": "completed"}))
        with (
            patch.object(server, "httpx") as mock_httpx,
            patch.object(server._api, "resolve_org", return_value="org-1"),
        ):
            mock_httpx.AsyncClient.return_value = client
            result = await server.sync_repository(project_id="proj-1")

        assert "error" not in result
        _assert_no_integration_token(client.post.call_args)
        _assert_authenticated_as_caller(client.post.call_args)


class TestAMissingTokenIsAnAnswerNotACrash:
    """`get_user_headers()` raises when nothing authenticates the caller, which
    is right for a helper and wrong for a tool.

    An MCP tool that raises fails at the *protocol* level: the client sees a
    transport error, not a message it can act on, and the actionable text
    ("run `innoday login`") is buried in a traceback. `sync_board` and
    `sync_repository` both returned a dict on this exact path before #611
    moved them onto the shared helper, and every other failure in these three
    tools still returns one -- `register_board`'s own credential error is a
    dict, and is the shape being matched.
    """

    @pytest.fixture
    def config_without_a_token(self):
        cfg = server.InnoConfig(api_url="http://api.test", cli_token=None)
        with patch.object(server, "get_config", return_value=cfg):
            yield cfg

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "call",
        [
            pytest.param(
                lambda: server.sync_board(board_id="board-1"), id="sync_board"
            ),
            pytest.param(lambda: server.sync_all_boards(), id="sync_all_boards"),
            pytest.param(
                lambda: server.sync_repository(project_id="proj-1"),
                id="sync_repository",
            ),
        ],
    )
    async def test_it_returns_the_remedy_instead_of_raising(
        self, call, config_without_a_token, operator_env
    ):
        with patch.object(server._api, "resolve_org", return_value="org-1"):
            result = await call()

        assert isinstance(result, dict), result
        # The message has to survive the shape change -- returning a dict that
        # says nothing useful is not an improvement on raising.
        assert "innoday login" in result["error"]

    @pytest.mark.asyncio
    async def test_no_request_is_attempted_without_one(
        self, config_without_a_token, operator_env
    ):
        """`operator_env` is set, so a tool that pressed on regardless would be
        the very leak #611 removed -- an unauthenticated (or env-credentialed)
        call rather than a refusal."""
        client = _mock_async_client(_ok({}))
        with (
            patch.object(server, "httpx") as mock_httpx,
            patch.object(server._api, "resolve_org", return_value="org-1"),
        ):
            mock_httpx.AsyncClient.return_value = client
            await server.sync_board(board_id="board-1")

        client.post.assert_not_called()
        client.get.assert_not_called()


class TestTheConfigIsBuiltOnce:
    """#611 part 2: no throwaway CLIConfig built just to peek at a value.

    `get_config()` re-runs this on **every** MCP tool call, and on stdio
    transport anything a construction writes to stdout corrupts the JSON-RPC
    stream -- #610's config purge did exactly that. Counting constructions is
    the only way to see the difference, since both shapes return the same
    config.
    """

    @staticmethod
    def _counting_cliconfig(raw):
        """A CLIConfig stand-in that records every construction."""
        calls = []

        class Fake:
            def __init__(self, **kwargs):
                calls.append(kwargs)
                self._raw = raw
                self._profile = kwargs.get("profile") or raw.get(
                    "current_profile", "default"
                )

            def get_default_profile(self):
                return raw.get("default_profile")

            def get_current_profile(self):
                return self._profile

            def list_profiles(self):
                return list(raw.get("profiles", {}))

        return Fake, calls

    @pytest.mark.parametrize(
        "raw",
        [
            # No default_profile at all.
            {"current_profile": "default", "profiles": {"default": {}}},
            # The pointers agree. This used to cost two constructions: any
            # default_profile at all forced the peek plus a rebuild.
            {
                "current_profile": "dev",
                "default_profile": "dev",
                "profiles": {"dev": {}, "default": {}},
            },
            # A stale pointer, naming a profile that no longer exists.
            # `_resolve_profile` would ignore it and land on the profile the
            # first construction already resolved.
            {
                "current_profile": "default",
                "default_profile": "deleted",
                "profiles": {"default": {}},
            },
        ],
        ids=["no-default", "pointers-agree", "stale-default"],
    )
    def test_one_construction_when_no_rebuild_is_needed(self, raw):
        fake, calls = self._counting_cliconfig(raw)
        with patch.object(server, "CLIConfig", fake):
            server.build_cli_config()
        assert len(calls) == 1, calls

    def test_the_default_profile_still_wins_when_the_pointers_disagree(self):
        """The behaviour the double construction existed for, kept.

        MCP must not follow whatever an interactive `config profile use` last
        set. Rebuilding for a *different profile* is not the pattern #611
        removes -- the removed one built a config it never used.
        """
        fake, calls = self._counting_cliconfig(
            {
                "current_profile": "scratch",
                "default_profile": "dev",
                "profiles": {"dev": {}, "scratch": {}},
            }
        )
        with patch.object(server, "CLIConfig", fake):
            config = server.build_cli_config()
        assert [c.get("profile") for c in calls] == [None, "dev"]
        assert config.get_current_profile() == "dev"


class TestImportingTheServerIsSilentOnStdout:
    """stdout IS the JSON-RPC channel; a single stray byte breaks the handshake.

    `load_config()` runs at import, so anything a `CLIConfig` construction
    prints reaches the protocol stream before the first message. #610 shipped
    exactly that bug and fixed it by routing notices to stderr; #611 changes
    this same import path, so re-prove it rather than assume.

    Run in a subprocess with a fabricated HOME: in-process capture would not
    exercise module import, and the fake HOME both keeps the real
    `~/.innoday/config.json` untouched and presents the config shape that
    triggers the purge notice -- a board secret on disk.
    """

    @staticmethod
    def _import_under_fake_home(tmp_path):
        home = tmp_path / "home"
        (home / ".innoday").mkdir(parents=True)
        (home / ".innoday" / "config.json").write_text(
            '{"current_profile": "default", "profiles": {"default": '
            '{"organizations": {"acme": {"id": "org-1", "integrations": '
            '{"jira": {"api_token": "encrypted:acme-jira", '
            '"email": "op@example.com"}}}}}}}'
        )
        repo_root = Path(__file__).resolve().parents[1]
        return subprocess.run(
            [sys.executable, "-c", "import src.mcp.server"],
            cwd=repo_root,
            env={
                "HOME": str(home),
                "PATH": "/usr/bin:/bin",
                "PYTHONPATH": str(repo_root),
                # Never reach a real keyring backend from a subprocess: the
                # fixture holds a board secret, so the import runs the purge,
                # which calls delete_password. Stripping the environment
                # happens to leave no D-Bus on Linux, but the macOS Keychain
                # needs none -- so pin the backend rather than rely on that.
                "PYTHON_KEYRING_BACKEND": "keyring.backends.null.Keyring",
            },
            capture_output=True,
            text=True,
            timeout=180,
        )

    def test_import_writes_nothing_to_stdout(self, tmp_path):
        result = self._import_under_fake_home(tmp_path)

        assert result.returncode == 0, result.stderr
        # Vacuity guard first: an empty stdout proves nothing if nothing had
        # anything to say. The fixture holds a board secret on disk, which the
        # purge announces -- on stderr, where it must land.
        assert "jira" in result.stderr.lower(), (
            "the fixture no longer triggers the purge notice, so the "
            f"stdout assertion below has become vacuous: {result.stderr!r}"
        )
        assert result.stdout == "", f"stdout must be empty, got: {result.stdout!r}"
