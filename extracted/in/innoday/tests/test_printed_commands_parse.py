"""Every command this CLI prints as advice must actually run.

`innoday board sync-status <id>` was printed at four sites and parsed at none:
the flag is `--board-id`, so following the instruction answered
`unrecognized arguments`. A printed instruction that errors is worse than none —
people trust it, then doubt the tool rather than the line.

This is the third instance of the same shape. `config setup` was printed in an
error message and has never existed; blastoff told a driven caller to
`Add --release to execute`, a flag that path does not have. So the check here is
deliberately **general**: it reads the commands out of the source and feeds each
to the real parser, rather than pinning the one string that was wrong today.
"""

import argparse
import re
import shlex
from pathlib import Path

import pytest

SRC = Path(__file__).parent.parent / "src"


def _command_tree():
    """{command: {subcommand, ...}} read from the parser itself.

    Read rather than listed: a hand-kept copy is one more thing to drift, and
    drift is the entire subject of this module.
    """
    from src.cli.main import create_parser

    def _subparsers(parser):
        for action in parser._actions:
            if getattr(action, "choices", None) and isinstance(action.choices, dict):
                return action.choices
        return {}

    top = _subparsers(create_parser())
    return {name: set(_subparsers(sub)) for name, sub in top.items()}


_TREE = _command_tree()
_TOP_LEVEL = set(_TREE)

#: Any `innoday …` command appearing in a string literal in the CLI.
#:
#: **Placeholders have to be inside the capture.** Written first to stop at the
#: quote, this matched nothing at all for
#: `f"innoday board sync-status --board-id {board_id}[/dim]"` -- the `{` was in
#: neither the character class nor the terminator set, so the lazy quantifier
#: backtracked to no match. The whole family this test exists for was invisible
#: to it, and it passed on the commands that happened to end cleanly. Caught by
#: mutating a fixed call site and watching the test stay green.
_PRINTED = re.compile(r"innoday ([a-z][a-z0-9 \-{}<>_.:]*)", re.MULTILINE)

#: Placeholder shapes a printed hint uses for a value the reader substitutes.
#: They stand in for a real argument, so the parser is given something valid.
_PLACEHOLDER = re.compile(r"\{[a-z_]+\}|<[a-z_ ]+>|\.\.\.")


def _looks_like_a_command(command: str) -> bool:
    """Whether this is an instruction to run, rather than prose mentioning one.

    "Run innoday blastoff from your machine" and `innoday blastoff --dry-run`
    both contain a real command; only the second is something to paste. The rule
    is deliberately blunt: **one token, or it carries a flag.** Prose has several
    words and no dashes; a real instruction with arguments always has a flag,
    because this CLI takes its values that way.

    Blunt beats clever here. A subtler rule would need updating whenever someone
    writes a new sentence, and a check nobody can keep passing gets deleted.
    """
    tokens = command.split()
    if not tokens:
        return False

    if len(tokens) == 1:
        # A lone word is usually prose -- "run any innoday command again", "the
        # next innoday command". Checked only when it is a real command
        # (`innoday init`) or is punctuated in a way prose is not
        # (`innoday org:create`, which is how that one was found).
        word = tokens[0]
        return word in _TOP_LEVEL or not word.isalpha()

    # **Not "does it carry a flag".** That was the first rule here, and it could
    # be evaded by being *more* broken: strip `--board-id` from a hint and the
    # remaining `board sync-status {id}` -- the exact defect -- looked like prose
    # and was skipped. A check a bug can escape by worsening is worse than none.
    #
    # A real command path is the discriminator: `board sync-status …` is one,
    # `release from your machine` is not.
    if tokens[0] in _TREE and tokens[1] in _TREE[tokens[0]]:
        return True
    return any(token.startswith("-") for token in tokens[1:])


def _printed_commands():
    """(file, command) for every `innoday …` instruction in the source."""
    found = []
    for path in sorted(SRC.rglob("*.py")):
        text = path.read_text()
        for match in _PRINTED.finditer(text):
            # Trailing markup/punctuation the literal carried, not the command.
            command = match.group(1).strip().rstrip("<.,:;")
            if command and _looks_like_a_command(command):
                found.append((path.relative_to(SRC.parent), command))
    return found


def test_the_source_actually_contains_printed_commands():
    """Guards the guard. A regex that silently matches nothing would make every
    assertion below vacuous, and the suite would stay green while covering zero
    commands -- which is exactly how this class of bug survives."""
    commands = _printed_commands()
    assert len(commands) > 10, f"only found {len(commands)}; the regex has drifted"


def test_the_commands_with_arguments_are_captured_too():
    """A count alone is not enough: the first version of this regex found
    plenty of bare commands and **none** of the ones carrying an argument, which
    is precisely where a wrong shape lives."""
    captured = [command for _where, command in _printed_commands()]
    assert any("sync-status" in c and "--board-id" in c for c in captured), (
        "commands with arguments are not being captured; the regex stops at the "
        "first placeholder and the test covers nothing that can be wrong"
    )


@pytest.mark.parametrize("where,command", _printed_commands(), ids=lambda v: str(v))
def test_a_printed_command_parses(where, command):
    """The parser must recognise the command's **shape**.

    Two argparse failures, and only one of them is a bug:

    * *unrecognized arguments* / *invalid choice* -- the printed line is wrong.
      `innoday board sync-status <id>` passed the id positionally when the flag
      is `--board-id`, so following it could never work.
    * *the following arguments are required* -- the line is a pointer ("use
      `innoday board register`"), not something to paste. Allowed.

    Distinguishing them is the whole value here. Failing on both would make the
    test unmaintainable and it would be deleted, which is how the original bug
    got four copies.
    """
    import contextlib
    import io

    from src.cli.main import create_parser

    filled = _PLACEHOLDER.sub("x", command)
    argv = shlex.split(filled)
    if not argv:
        pytest.skip("no command")

    stderr = io.StringIO()
    try:
        with (
            contextlib.redirect_stderr(stderr),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            create_parser().parse_args(argv)
    except SystemExit:
        message = stderr.getvalue()
        broken = "unrecognized arguments" in message or "invalid choice" in message
        assert not broken, (
            f"{where} prints `innoday {command}`, which the parser rejects:\n"
            f"  {message.strip().splitlines()[-1] if message.strip() else '(exit)'}\n"
            "  Printed advice has to work -- see this module's docstring."
        )
    except argparse.ArgumentError as exc:  # pragma: no cover - defensive
        pytest.fail(f"{where} prints `innoday {command}`: {exc}")


class TestProjectsUpdateCanRenameAnAlias:
    """The API has always accepted it; only the CLI flag was missing.

    That gap is why a project could not be renamed from the command line -- and
    agents here are supposed to go through the CLI rather than the API, so
    "do it in the browser" was the only answer.
    """

    def test_the_flag_exists(self):
        from src.cli.main import create_parser

        parser = create_parser()
        projects = [
            a
            for a in parser._actions
            if getattr(a, "choices", None) and "projects" in a.choices
        ][0].choices["projects"]
        update = [
            a
            for a in projects._actions
            if getattr(a, "choices", None) and "update" in a.choices
        ][0].choices["update"]
        flags = {opt for action in update._actions for opt in action.option_strings}
        assert "--alias" in flags

    def test_the_help_warns_that_the_alias_is_also_the_topic(self):
        """Renaming silently stops discovering a project's repositories unless
        the topic moves too -- the trap that cost a whole detour."""
        from src.cli.main import create_parser

        parser = create_parser()
        projects = [
            a
            for a in parser._actions
            if getattr(a, "choices", None) and "projects" in a.choices
        ][0].choices["projects"]
        update = [
            a
            for a in projects._actions
            if getattr(a, "choices", None) and "update" in a.choices
        ][0].choices["update"]
        alias = next(a for a in update._actions if "--alias" in a.option_strings)
        assert "topic" in (alias.help or "").lower()

    @pytest.mark.asyncio
    async def test_the_alias_reaches_the_request_body(self):
        """A declared flag that never lands in the payload is the same silent
        nothing as no flag at all."""
        from unittest.mock import AsyncMock, MagicMock, patch

        from src.cli.commands.projects import ProjectCommands

        config = MagicMock()
        config.get_current_organization.return_value = "hs"
        config.get_organization_id.return_value = "org-1"
        config.get_current_project_id.return_value = "proj-1"

        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"name": "Blastoff", "alias": "blast"}

        client = MagicMock()
        client.put = AsyncMock(return_value=response)
        client.close = AsyncMock()

        args = argparse.Namespace(
            project_id="BLASTOFF",
            name=None,
            alias="blast",
            description=None,
            goals=None,
            scope_limitations=None,
            priority=None,
            status=None,
            tags=None,
        )

        with patch("src.cli.commands.projects.InnoDayAPIClient", return_value=client):
            assert await ProjectCommands._handle_update(args, config) == 0

        assert client.put.call_args.kwargs["json"]["alias"] == "blast"
