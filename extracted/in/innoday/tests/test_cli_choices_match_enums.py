"""Hand-written choice lists must not drift from the enum they shadow.

`SummaryWindow` already documents the rule and the failure mode: "a hand-written
list drifts from the enum silently, and the failure mode is a flag that rejects
every legal value". It had drifted anyway, in both directions:

* `innoday auth login --service` offered `trello, jira` while `BoardType` has
  four members — half the supported board types were unconfigurable. (That
  command has since been deleted; it wrote credentials nothing read.)
* the interactive board-type prompt offered **`github`**, which is *not* a
  `BoardType` member at all. Choosing it sent `board_type: "github"` to board
  registration, which answered 422, and the CLI printed a bare "⚠ Could not
  register board" — an interactive prompt leading somewhere that cannot work.

This is deliberately **not** a sweep that rewrites every `choices=[...]` in the
CLI. Nine of the eleven enum-shadowing lists were correct, and mechanically
rewriting correct code is a chance to introduce the bug it is preventing. One
test that fails on the *next* drift is cheaper than eleven refactors, and it
covers lists that do not exist yet.

Only lists that shadow a real domain enum are asserted here. `choices=["today",
"week", "month"]` and friends answer to nothing and are none of this test's
business.
"""

from __future__ import annotations

import argparse
from typing import Dict, Set

import pytest

from src.domain.board import BoardType
from src.domain.release import ReleaseStatus


def _choices_for(setup_parser, *, subcommand: str, dest_or_flag: str) -> Set[str]:
    """The `choices` one *subcommand's* option declares, as a set.

    Scoped to a subcommand deliberately. An earlier version unioned every
    matching flag across the whole parser and promptly failed on `board`, where
    `register --type` takes a `BoardType` and `summarize --type` takes a
    `SummaryType` — two unrelated vocabularies behind one flag name. Comparing
    the union against either enum is meaningless.

    Walks the parser rather than reading the source, so the assertion is about
    what argparse will actually accept.
    """
    parser = argparse.ArgumentParser()
    setup_parser(parser)

    for action in parser._actions:
        if not isinstance(action, argparse._SubParsersAction):
            continue
        sub = action.choices.get(subcommand)
        if sub is None:
            continue
        for option in sub._actions:
            names = set(option.option_strings) | {option.dest}
            if dest_or_flag in names and option.choices:
                return set(option.choices)
    pytest.skip(f"{subcommand} has no option {dest_or_flag!r} with choices")


def _enum_values(enum) -> Set[str]:
    return {member.value for member in enum}


def test_board_register_type_matches_board_type():
    from src.cli.commands.boards import BoardCommands

    offered = _choices_for(
        BoardCommands.setup_parser, subcommand="register", dest_or_flag="--type"
    )
    assert offered >= _enum_values(BoardType), (
        "board register --type rejects a supported board type"
    )


def test_no_cli_choice_list_offers_a_board_type_that_does_not_exist():
    """The `github` bug, pinned.

    Offering a value the domain enum will reject is worse than omitting it: the
    user follows a prompt into a 422 whose message does not say why.
    """
    from src.cli.commands.boards import BoardCommands

    offered = _choices_for(
        BoardCommands.setup_parser, subcommand="register", dest_or_flag="--type"
    )
    invented = offered - _enum_values(BoardType)
    assert not invented, f"CLI offers non-BoardType values: {sorted(invented)}"


def test_the_board_secret_purge_covers_every_board_type():
    """`src/cli/config.py`'s `BOARD_INTEGRATION_TYPES` is the same hazard one
    layer down, and a worse one.

    It is hand-typed (deriving it means importing `src.domain.board`, which
    drags SQLModel into every CLI startup for four strings), and it decides
    which integration types the load-time purge removes -- and, with
    `DEAD_INTEGRATION_TYPES` beside it, which of the two things the notice
    says about what it removed. (It used to decide a second thing as well:
    which types `add_organization_integration` refused to write. That writer
    was deleted in #729, so nothing puts one there any more; a legacy or
    hand-edited file is what the purge is left cleaning up.) A fifth
    `BoardType` that is not in the constant is **never purged** -- silently,
    which is exactly the hole #609 closed.

    Without this assertion the only thing a fifth board type fails is
    `test_board_register_type_matches_board_type` above, which points at
    `boards.py`; fixing that gives no signal at all that `config.py` also
    needs it.
    """
    from src.cli.config import BOARD_INTEGRATION_TYPES

    assert set(BOARD_INTEGRATION_TYPES) == _enum_values(BoardType), (
        "src/cli/config.py's BOARD_INTEGRATION_TYPES has drifted from "
        f"BoardType: constant={sorted(BOARD_INTEGRATION_TYPES)} "
        f"enum={sorted(_enum_values(BoardType))}. A board type missing from "
        "the constant can be written to ~/.innoday/config.json and is never "
        "purged from it."
    )


def test_release_status_choices_match_the_enum():
    from src.cli.commands.releases import ReleasesCommands

    for subcommand in ("create", "update"):
        offered = _choices_for(
            ReleasesCommands.setup_parser,
            subcommand=subcommand,
            dest_or_flag="--status",
        )
        assert offered == _enum_values(ReleaseStatus), (
            f"releases {subcommand} --status has drifted from ReleaseStatus: "
            f"offered={sorted(offered)} enum={sorted(_enum_values(ReleaseStatus))}"
        )


def test_the_interactive_board_type_prompt_is_derived_not_typed():
    """`config init`'s board step prompts rather than using argparse `choices`.

    Its list is built from `BoardType` in the source; asserting on the source is
    the only way to catch it, since a `Prompt.ask` list is not reachable through
    a parser. Cheap, and it is exactly where the `github` bug lived.
    """
    from pathlib import Path

    import src.cli.commands.config as config_module

    source = Path(config_module.__file__).read_text()
    assert "[board.value for board in BoardType]" in source, (
        "the interactive board-type prompt is hand-typed again"
    )
    assert '"github"' not in source.split("Board type")[1][:400], (
        "the github board type is back in the prompt"
    )


ENUM_BACKED: Dict[str, object] = {
    "BoardType": BoardType,
    "ReleaseStatus": ReleaseStatus,
}


def test_the_enums_this_file_guards_still_exist():
    """A rename would otherwise turn every assertion above into a silent pass."""
    for name, enum in ENUM_BACKED.items():
        assert _enum_values(enum), f"{name} has no members"


def test_ticket_release_declares_no_choices():
    """`--release`'s vocabulary is live data.

    An argparse `choices` list is built at parser-construction time, before any
    org or project is resolved and before a single HTTP call -- so it could only
    ever be a hardcoded guess at another project's release names. The check
    belongs in the handler, against the releases endpoint. This also sidesteps
    the `default=` bypasses `type=` trap; `--release` has no default.
    """
    import argparse as _argparse

    from src.cli.commands.tickets import TicketCommands

    for subcommand in ("create", "update"):
        parser = _argparse.ArgumentParser()
        TicketCommands.setup_parser(parser)
        found = False
        for action in parser._actions:
            if not isinstance(action, _argparse._SubParsersAction):
                continue
            sub = action.choices.get(subcommand)
            if sub is None:
                continue
            for option in sub._actions:
                if "--release" in option.option_strings:
                    found = True
                    assert option.choices is None, (
                        f"tickets {subcommand} --release has a hardcoded choices "
                        "list; the vocabulary is live data"
                    )
                    assert option.default is None, (
                        f"tickets {subcommand} --release has a default"
                    )
        assert found, f"tickets {subcommand} has no --release option"


def test_the_outstanding_release_filter_is_derived_from_the_enum():
    """The CLI decides which releases to offer by status. Typing "planned" there
    is how a fifth `ReleaseStatus` member gets silently excluded from the picker
    while `release_planning` includes it."""
    from pathlib import Path

    import src.cli.commands.tickets as tickets_module

    source = Path(tickets_module.__file__).read_text()
    assert "OUTSTANDING_STATUSES" in source, (
        "the outstanding-release filter is not derived from ReleaseStatus"
    )
    for literal in ('"planned"', "'planned'", '"in_progress"', "'in_progress'"):
        assert literal not in source, (
            f"a release status literal ({literal}) is typed in the tickets CLI"
        )
