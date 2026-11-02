"""the text options a write carries: --description, --notes, --markdown, and who composed them (--authored-by)."""

from __future__ import annotations
from enum import Enum
from typing import Any

import typer


# --- One vocabulary for the things every noun has ----------------------------
#
# These were written per-command, so the same concept had several spellings and
# some of them were wrong: `run set` and `run tag` said "run id" after #173 made
# a bare ref the PETNAME, and only one of the six `--description` flags carried
# any help at all. A constant is not ceremony here -- it is the only way the
# wording stays identical across four nouns and twenty-odd verbs, which is what
# lets someone learn a habit from one verb and use it on the next.
#
# The ref phrasing per kind follows refs.py's "which handle is the name" table,
# and must keep following it: project/experiment are slug-first, runs are
# petname-first-but-either (a petname cannot be UUID-shaped, so it cannot
# collide), artifacts are id-only.
# Factories, not shared instances: a typer.Argument/Option value is bound as a
# function default, and one object reused across signatures is shared mutable
# state that click is free to annotate. A call per signature costs nothing.
DESCRIPTION_HELP = "what this is, in a few words up to 3 sentences"

#: Notes are the CAVEAT, not a second description -- what a later reader should
#: distrust. Prose, so it reads a file or stdin as readily as an argument.
NOTES_HELP = "caveat a later reader needs; literal, @file, or '-' for stdin ('' clears)"


def description_opt() -> Any:
    return typer.Option(None, "--description", help=DESCRIPTION_HELP)


def notes_opt() -> Any:
    return typer.Option(None, "--notes", help=NOTES_HELP)


#: WHO composed the name and description on this write. One definition, because
#: eight verbs offer it and a help string that drifts between them is a
#: different promise on each.
#:
#: The DEFAULT is resolved in the SDK, not here (`sdk/client/client.py::_authored_by`),
#: so `probe` and a Python caller answer the question the same way: under a
#: coding agent it is `agent`, and in a bare terminal NOTHING is sent and the
#: server applies the inference it always has.
AUTHORED_BY_HELP = (
    "who composed --name/--description: 'human' LOCKS them against generation "
    "forever (no undo), 'agent' leaves them improvable. Default: agent under a "
    "coding agent, otherwise the server's own inference"
)


class AuthoredBy(str, Enum):
    """Who composed the text on this write.

    Mirrors `app.core.authorship.Authorship` and the generated
    `probe.generated.models.Authorship`; spelled here because this is a typer
    choice surface and the two spellings are pinned together by
    `agent/tests/test_authorship_default.py`.
    """

    human = "human"
    agent = "agent"


def _authored_by_value(choice: "AuthoredBy | None") -> str | None:
    """The wire value for `--authored-by`, or None to let the SDK decide.

    None here does NOT mean "human". It means the caller did not say, and the
    resolution then happens once, in `sdk/client/client.py::_authored_by` -- so the
    CLI and a Python caller can never answer the question differently.
    """
    return choice.value if choice is not None else None


def authored_by_opt() -> Any:
    return typer.Option(None, "--authored-by", help=AUTHORED_BY_HELP)


def entity_markdown_opt() -> Any:
    return typer.Option(
        None,
        "--summary",
        help=(
            "whole-document Markdown: on a project or experiment a block INSIDE the "
            "Overview page the AI may not rewrite, on a run below the AI Summary; "
            "read first, and check the result CONTAINS what you meant rather than "
            "matching byte-for-byte -- a read answers from the page, which renders "
            "it. Literal, @file, or - for stdin. "
            "A line containing only [README](https://github.com/owner/repo) "
            "embeds that repo's README at that point"
        ),
    )
