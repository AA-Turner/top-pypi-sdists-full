"""probe docs: search Probe's own docs and print the sections that answer."""

from __future__ import annotations
from enum import Enum

import typer

from .... import errors
from probe.cli.cli import app


# -- Probe's own docs ----------------------------------------------------------
#: The most `probe docs` prints, in characters: whole sections, best first, up
#: to the one that would pass it. The first section always prints.
DOCS_PRINT_CHARS = 8_000
#: The longest question `GET /public/v1/docs` takes (`probe.shared.reads.search_contract.
#: DOCS_QUERY_MAX_CHARS`, not imported: `probe.mcp` loads the whole MCP service).
DOCS_QUERY_MAX_CHARS = 512


class DocsState(str, Enum):
    """`GET /public/v1/docs`'s `state` (`Client.docs`)."""

    OK = "ok"
    #: The last good copy, served while docs.prbe.ai cannot be read.
    STALE = "stale"
    #: No copy yet: `sections` is empty.
    UNAVAILABLE = "unavailable"


# Every word after the first is the question's, a `--flag` included: asking
# about `--no-capture` is the point, not an unknown option.
@app.command("docs", context_settings={"ignore_unknown_options": True, "allow_interspersed_args": False})
def docs(
    question: list[str] = typer.Argument(..., help="what you want to know, in plain words"),
) -> None:
    """Search Probe's own docs (docs.prbe.ai) and print the sections that answer."""
    # Reads Probe's public docs only: no credential is sent (`Transport`
    # skips auth for `/public/`), so it answers signed out, and it opens,
    # stamps and records nothing.
    query = " ".join(question).strip()
    if not query:
        raise typer.BadParameter("ask a question", param_hint="QUESTION")
    if len(query) > DOCS_QUERY_MAX_CHARS:
        raise typer.BadParameter(
            f"at most {DOCS_QUERY_MAX_CHARS} characters (this has {len(query)}): "
            "name the feature, command or error",
            param_hint="QUESTION",
        )
    try:
        with _client() as c:
            answer = c.docs(query)
    except (errors.RosError, ValueError) as exc:
        # ValueError: a 2xx that is not JSON (a proxy's page in front of the API).
        reason = (str(exc).strip().splitlines() or [type(exc).__name__])[0]
        typer.echo(f"error: Probe's docs could not be read: {reason}", err=True)
        raise typer.Exit(1) from None
    state = answer.get("state") if isinstance(answer, dict) else None
    sections = answer.get("sections") if isinstance(answer, dict) else None
    if state == DocsState.UNAVAILABLE.value or not isinstance(sections, list):
        typer.echo("error: Probe's docs are unavailable right now; try again in a minute.", err=True)
        raise typer.Exit(1)
    if state == DocsState.STALE.value:
        typer.echo("docs.prbe.ai could not be read just now; this is the last good copy.", err=True)
    if not sections:
        typer.echo("Nothing in Probe's docs matched; try other words.")
        return
    blocks: list[str] = []
    used = 0
    for section in sections:
        block = _docs_block(section)
        if blocks and used + len(block) > DOCS_PRINT_CHARS:
            break
        blocks.append(block)
        used += len(block) + 2  # the blank line between sections
    typer.echo("\n\n".join(blocks))
    more = len(sections) - len(blocks)
    if more:
        typer.echo(f"\n{more} more matching section{'' if more == 1 else 's'} not shown.")


def _docs_block(section: object) -> str:
    """One docs section as markdown: `## <page> — <heading>`, its URL, its text."""
    fields = section if isinstance(section, dict) else {}
    page = str(fields.get("page") or "").strip()
    heading = str(fields.get("heading") or "").strip()
    title = " — ".join(part for part in (page, heading) if part) or "Probe docs"
    lines = [f"## {title}"]
    url = str(fields.get("url") or "").strip()
    if url:
        lines.append(url)
    text = str(fields.get("text") or "").strip()
    return "\n".join(lines) + (f"\n\n{text}" if text else "")
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
