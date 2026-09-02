import argparse
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_register_with_sync_calls_sync_after_success():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(
        board_command="register",
        board_url="https://x",
        board_name="B",
        type="linear",
        project_id="proj-1",
        email=None,
        api_token=None,
        api_key=None,
        token="lin_api_xxx",
        sync=True,
    )
    config = _fake_config()
    client = _fake_client_registering_ok(board_id="board-99")

    with patch.object(
        BoardCommands, "_handle_sync", new=AsyncMock(return_value=0)
    ) as mock_sync:
        rc = await BoardCommands._handle_register(args, client, config)

    assert rc == 0
    assert mock_sync.await_count == 1  # sync ran after register


@pytest.mark.asyncio
async def test_register_with_sync_failure_leaves_board_registered():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(
        board_command="register",
        board_url="https://x",
        board_name="B",
        type="linear",
        project_id="proj-1",
        email=None,
        api_token=None,
        api_key=None,
        token="lin_api_xxx",
        sync=True,
    )
    config = _fake_config()
    client = _fake_client_registering_ok(board_id="board-99")

    with patch.object(
        BoardCommands,
        "_handle_sync",
        new=AsyncMock(return_value=1),  # sync fails
    ) as mock_sync:
        rc = await BoardCommands._handle_register(args, client, config)

    # Register succeeded and the board is NOT un-registered, so the command
    # exits 0 and says what went wrong in prose. Returning the sync's code told
    # a script the registration failed -- and the obvious response to that lie
    # is to register again, duplicating a board that already exists.
    assert mock_sync.await_count == 1
    assert rc == 0
    assert client.deleted is False  # no rollback/delete call made


@pytest.mark.asyncio
async def test_register_reports_the_sync_failure_it_does_not_exit_on():
    """Exiting 0 must not mean going quiet -- the operator still gets told."""
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(
        board_command="register",
        board_url="https://x",
        board_name="B",
        type="linear",
        project_id="proj-1",
        email=None,
        api_token=None,
        api_key=None,
        token="lin_api_xxx",
        sync=True,
    )
    client = _fake_client_registering_ok(board_id="board-99")

    with (
        patch.object(BoardCommands, "_handle_sync", new=AsyncMock(return_value=1)),
        patch("src.cli.commands.boards.console.print") as printed,
    ):
        rc = await BoardCommands._handle_register(args, client, _fake_config())

    # console.print() is also called with no arguments, for blank lines.
    said = " ".join(
        " ".join(str(c.args[0]) for c in printed.call_args_list if c.args).split()
    )
    assert rc == 0
    assert "initial sync" in said, said
    # `--board-id`, not a positional. This pinned the bare form, which is the
    # shape `board sync` rejects -- so the test guaranteed advice that could not
    # work. `test_printed_commands_parse.py` now checks the whole CLI.
    assert "innoday board sync --board-id board-99" in said, said


@pytest.mark.asyncio
async def test_register_without_sync_does_not_sync():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(
        board_command="register",
        board_url="https://x",
        board_name="B",
        type="linear",
        project_id="proj-1",
        email=None,
        api_token=None,
        api_key=None,
        token="lin_api_xxx",
        sync=False,
    )
    config = _fake_config()
    client = _fake_client_registering_ok(board_id="board-99")

    with patch.object(
        BoardCommands, "_handle_sync", new=AsyncMock(return_value=0)
    ) as mock_sync:
        rc = await BoardCommands._handle_register(args, client, config)

    assert rc == 0
    assert mock_sync.await_count == 0


# --- helpers ---
def _fake_config():
    class C:
        def get_user_id(self):
            return "user-1"

        def get_current_organization(self):
            return "hs"

        def get_organization_id(self, alias):
            return "org-1"

        def get_current_project_id(self):
            return "proj-1"

        def get_organization_integration(self, alias, t):
            raise AssertionError(
                "board register read a board credential from local config"
            )

        def get_credential(self, key):
            raise AssertionError("board register read a credential from the keyring")

    return C()


def _fake_client_registering_ok(board_id):
    class Resp:
        status_code = 201

        def json(self):
            return {
                "id": board_id,
                "board_name": "B",
                "board_type": "linear",
                "board_url": "https://x",
                "is_active": True,
            }

    class Client:
        deleted = False

        def __init__(self):
            self.posted = []

        async def post(self, path, json=None, headers=None):
            self.posted.append((path, json, headers))
            return Resp()

        async def delete(self, path, **kw):
            self.deleted = True
            return Resp()

    return Client()


# ------------------------------------------------------- credentials by flag


def _register_args(board_type, **creds):
    return argparse.Namespace(
        board_command="register",
        board_url="https://x",
        board_name="B",
        type=board_type,
        project_id="proj-1",
        sync=False,
        email=creds.get("email"),
        api_token=creds.get("api_token"),
        api_key=creds.get("api_key"),
        token=creds.get("token"),
    )


def _register_parser():
    """The real parser, so these assertions are about the shipped CLI."""
    from src.cli.commands.boards import BoardCommands

    parser = argparse.ArgumentParser(prog="innoday board")
    BoardCommands.setup_parser(parser)
    for action in parser._subparsers._group_actions[0].choices.items():
        if action[0] == "register":
            return action[1]
    raise AssertionError("no `register` subcommand found")


class TestRegisterTakesCredentialsFromFlags:
    """#609: `register` is the one legitimate moment a credential is supplied
    -- it is how a credential reaches Vault, which every later sync resolves
    from. It used to take it from `~/.innoday/config.json`, which meant the
    board a credential ended up attached to depended on what the operator
    happened to have saved. It must be typed, not found.
    """

    @pytest.mark.parametrize(
        "board_type,creds,expected_token",
        [
            ("linear", {"token": "lin_api_xxx"}, "lin_api_xxx"),
            (
                "jira",
                {"email": "dev@example.com", "api_token": "secret-token"},
                "dev@example.com:secret-token",
            ),
            (
                "trello",
                {"api_key": "key-123", "token": "token-456"},
                "key-123:token-456",
            ),
            ("notion", {"token": "notion-token"}, "notion-token"),
        ],
    )
    @pytest.mark.asyncio
    async def test_the_flags_reach_the_request_for_each_board_type(
        self, board_type, creds, expected_token
    ):
        from src.cli.commands.boards import BoardCommands

        client = _fake_client_registering_ok(board_id="board-99")

        rc = await BoardCommands._handle_register(
            _register_args(board_type, **creds), client, _fake_config()
        )

        assert rc == 0
        _path, _json, headers = client.posted[0]
        assert headers == {"X-Integration-Token": expected_token}

    @pytest.mark.parametrize(
        "board_type,creds,needed",
        [
            ("jira", {"email": "dev@example.com"}, "--email and --api-token"),
            ("jira", {"api_token": "t"}, "--email and --api-token"),
            ("trello", {"api_key": "k"}, "--api-key and --token"),
            ("linear", {}, "--token"),
            ("notion", {}, "--token"),
        ],
    )
    @pytest.mark.asyncio
    async def test_a_missing_flag_says_exactly_what_to_pass(
        self, capsys, board_type, creds, needed
    ):
        from src.cli.commands.boards import BoardCommands

        client = _fake_client_registering_ok(board_id="board-99")

        rc = await BoardCommands._handle_register(
            _register_args(board_type, **creds), client, _fake_config()
        )

        assert rc == 1
        assert client.posted == []  # nothing was registered
        # Rich hard-wraps to the console width, so a flag pair can be split
        # across lines; compare on collapsed whitespace rather than pinning
        # where the break lands.
        out = " ".join(capsys.readouterr().out.split())
        assert needed in out, out

    def test_the_parser_declares_the_literal_option_strings(self):
        """Assert the literal flag names, not that a sample invocation parses.

        argparse accepts any unambiguous prefix of a long option, so
        `parse_args(["--api-token", "x"])` keeps passing after the flag is
        renamed to `--api-token-v2` -- a test shaped that way certifies
        nothing about the name it claims to pin. This repo has already had one
        test green through exactly that rename.
        """
        declared = {
            option
            for action in _register_parser()._actions
            for option in action.option_strings
        }
        assert {"--email", "--api-token", "--api-key", "--token"} <= declared, declared

    def test_register_and_set_cred_declare_the_same_credential_flags(self):
        """They are the two ways to supply a credential and must not drift.

        Both call `_add_credential_arguments`; this fails if one grows a flag
        the other lacks.
        """
        from src.cli.commands.boards import BoardCommands

        parser = argparse.ArgumentParser(prog="innoday board")
        BoardCommands.setup_parser(parser)
        choices = parser._subparsers._group_actions[0].choices

        credential_flags = {"--email", "--api-token", "--api-key", "--token"}

        def declared(name):
            return {
                option
                for action in choices[name]._actions
                for option in action.option_strings
            } & credential_flags

        assert declared("register") == declared("set-cred") == credential_flags
