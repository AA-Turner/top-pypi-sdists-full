"""An MCP tool description must not offer a value the API will reject.

`tests/test_cli_choices_match_enums.py` is the same rule one surface over, and it
records the same bug: the CLI's board-type prompt offered **`github`**, which
is not a `BoardType` member, so choosing it sent `board_type: "github"` to board
registration and got a 422 back. #622 found the identical claim in the MCP
server's own parameter descriptions -- `register_board`, `sync_all_boards` and
`setup_org_with_env` all listed "trello, jira, linear, notion, github".

That reaches further than the CLI's copy did. Tool descriptions are shipped to
every MCP client on every `tools/list`, and the caller acting on them is a model,
which has nothing but the description to go on.

The claimed types are read out of the source with AST rather than hand-listed
here, and compared against `BoardType` -- a fifth board type then needs no edit
to this file, and a sixth invented one fails it.

**Keyed on the parameter name, deliberately.** `get_all_work`'s
`source_platform` says "trello, jira, notion, linear, github" and is *correct*:
that filter spans tickets and GitHub issues, so `github` is a real source there.
Scanning every description for the word instead of scanning `board_type`
parameters would fail on it, and the obvious way to make that pass again is to
weaken the rule.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Dict, Set

from src.domain.board import BoardType

SERVER = Path(__file__).resolve().parents[1] / "src" / "mcp" / "server.py"

PARAM = "board_type"


def _field_description(default_node: ast.expr) -> str | None:
    """The `description=` string of a `Field(...)` default, if it has one."""
    if not isinstance(default_node, ast.Call):
        return None
    func = default_node.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
    if name != "Field":
        return None
    for keyword in default_node.keywords:
        if keyword.arg == "description":
            return _joined_str(keyword.value)
    return None


def _joined_str(node: ast.expr) -> str | None:
    """A string constant, including the implicitly-concatenated form."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):  # an f-string -- not a fixed vocabulary
        return None
    return None


def _board_type_descriptions() -> Dict[str, str]:
    """`{tool name: description}` for every `board_type` parameter in the server.

    Walks function definitions rather than importing the module: importing
    `src.mcp.server` constructs a FastMCP app and an HTTP client, and the
    question here is what the *source* declares.
    """
    tree = ast.parse(SERVER.read_text())
    found: Dict[str, str] = {}

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        args = node.args
        pairs = list(
            zip(reversed(args.args + args.posonlyargs), reversed(args.defaults))
        )
        pairs += list(zip(args.kwonlyargs, args.kw_defaults))
        for arg, default in pairs:
            if arg.arg != PARAM or default is None:
                continue
            description = _field_description(default)
            if description:
                found[node.name] = description
    return found


def _claimed_board_types(description: str) -> Set[str]:
    """The board types a description offers the caller.

    The shape every one of these uses is a lead-in, a colon, then a
    comma-or-`or`-separated list, ending at the first sentence break --
    "Board type: trello, jira, linear, notion" and "Only sync boards of this
    type: trello, jira, linear, notion. Omit to sync all." Only bare lowercase
    words count, so trailing prose ("Pass 'skip' to skip board setup") and
    anything with punctuation or capitals is not read as a type.
    """
    head = description.split(".")[0]
    if ":" not in head:
        return set()
    listed = head.split(":", 1)[1]
    claimed = set()
    for chunk in re.split(r",|\bor\b|\band\b|/", listed):
        token = chunk.strip().strip("'\"")
        if re.fullmatch(r"[a-z][a-z0-9_]*", token):
            claimed.add(token)
    return claimed


def _enum_values() -> Set[str]:
    return {member.value for member in BoardType}


def test_no_tool_description_offers_a_board_type_the_enum_lacks():
    """The `github` claim, pinned where it ships from."""
    invented = {
        tool: sorted(_claimed_board_types(description) - _enum_values())
        for tool, description in _board_type_descriptions().items()
        if _claimed_board_types(description) - _enum_values()
    }
    assert not invented, (
        "an MCP tool tells callers about a board type BoardType does not have -- "
        "the API answers 422 and the description is the only thing the caller "
        f"has to go on: {invented}"
    )


def test_the_scan_finds_the_board_type_parameters():
    """Vacuity guard: an empty scan passes the assertion above forever.

    Named rather than counted -- a count drifts on any unrelated tool being
    added, and these three are the ones that had the bug.
    """
    found = _board_type_descriptions()
    assert {"register_board", "sync_all_boards", "setup_org_with_env"} <= set(found), (
        f"the board_type scan is not finding the tools it used to: {sorted(found)}"
    )
    for tool, description in found.items():
        assert _claimed_board_types(description), (
            f"{tool}'s board_type description declares no types at all -- either "
            "the wording changed shape or the extractor stopped reading it"
        )


def test_the_extractor_reads_a_type_list_it_is_given():
    """The matcher itself, on both the shapes in the file and the bug's shape."""
    assert _claimed_board_types("Board type: trello, jira, linear, notion") == {
        "trello",
        "jira",
        "linear",
        "notion",
    }
    assert _claimed_board_types("Target board type: trello or jira") == {
        "trello",
        "jira",
    }
    assert "github" in _claimed_board_types(
        "Board type: trello, jira, linear, notion, github"
    )
    assert _claimed_board_types(
        "Board type: jira, notion. Pass 'skip' to skip board setup."
    ) == {"jira", "notion"}


def test_board_type_still_has_members():
    """A rename or an emptied enum would make every assertion above vacuous."""
    assert _enum_values()
    assert "github" not in _enum_values()
