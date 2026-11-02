"""print a command's result under the one read policy (reads.render_json): JSON, --fields selection, a moved read's answer, the dashboard link on stderr."""

from __future__ import annotations
import json
import sys
from typing import Any

import typer
from ...shared.reads import reads


def _print_json(obj: Any) -> None:
    """One output policy for every read command (`reads.render_json`; the reads
    the daemon host answers too print through it, via `_emit`).

    Pretty on a terminal, compact on a pipe — the same split `jq` and git
    resolve the same way. The audiences differ: a human scans indentation, but
    the common non-TTY reader here is a coding agent whose context window pays
    for every byte, and `indent=2` plus `\\uXXXX` escapes were measured at ~19%
    of a `project list`. Whitespace is the ONLY thing that varies by
    destination: same keys, same values either way, so piping to a file never
    changes what a script sees, only how it is laid out.

    `ensure_ascii=False` in both modes: the JSON spec is UTF-8 and stdout is;
    escaping every non-ASCII character triples its cost for no reader's
    benefit. The narrow exception is display-control characters — C1 controls
    (U+0080–U+009F, single-byte CSI on C1-interpreting terminals) and Unicode
    bidi overrides (U+202A–E, U+2066–69, visual spoofing) — which the old
    ensure_ascii=True default happened to neutralize. Those stay escaped in
    BOTH modes: server rows are multi-writer team data, and a spoofed line
    misleads an agent reading a pipe as surely as a human at a TTY. json.dumps
    already escapes C0, so this closes the set.

    None from a write this command could not deliver is not a success: it
    prints what happened to it (`{"queued": true, "count": 1, "writes": [...]}`,
    still one JSON value) instead of `null`, which reads like the answer of a
    write that landed (lineage plan L14).
    """
    if obj is None and _UNDELIVERED.total:
        obj = _UNDELIVERED.result()
    _print_rendered(reads.render_json(obj, sys.stdout.isatty()))


def _print_rendered(rendered: str) -> None:
    """Print one rendered JSON value (`reads.render_json`)."""
    try:
        print(rendered)
    except UnicodeEncodeError:
        # A legacy non-UTF-8 locale (latin-1, eucJP) cannot encode raw
        # non-ASCII output that ensure_ascii=True used to escape for free.
        # Fall back to full escaping rather than crash the read.
        print(json.dumps(json.loads(rendered), ensure_ascii=True, default=str))


#: Project a read down to the named top-level fields (`reads.select_fields`).
_select_fields = reads.select_fields


def _emit(printed: "reads.Printed") -> None:
    """Print what a moved read printed (`probe.shared.reads.reads`), and exit with its code."""
    for to_error, text, is_json in printed.parts:
        if to_error:
            print(text, file=sys.stderr)
        elif is_json:
            _print_rendered(text)
        else:
            print(text)
    if printed.code:
        raise typer.Exit(printed.code)


#: The shared `--fields` option, declared once so every read spells it the same.
_FIELDS_OPTION = typer.Option(
    None,
    "--fields",
    help="only these top-level fields, comma-separated (e.g. slug,name,status)",
)


def _print_link(kind: str, entity_id: str | None) -> None:
    """Echo an entity's dashboard URL to STDERR, if there is one to echo.

    stderr, not stdout, and that is load-bearing: `run start` prints a bare id
    that callers capture (`RUN=$(probe run start ...)`), and `project create`
    prints JSON that gets piped into `jq`. A link on stdout would corrupt both.
    stderr is read by exactly the audiences this is for -- a human at a terminal
    and an agent reading combined command output -- and by no parser.

    Silent when the dashboard origin is unknown (see sdk.reads.links): a link into the
    wrong deployment is worse than no link at all.
    """
    from ...sdk.reads.links import entity_url

    url = entity_url(kind, entity_id)
    if url:
        typer.echo(url, err=True)
from probe.cli.connection import _UNDELIVERED  # noqa: E402 -- pieces need each other; the front door loads this one first
