"""Find, create, or update the single Claude review note on a merge request.

Provider-neutral (GitLab MR / GitHub PR): every host call goes through the
resolved :class:`MergeRequestProvider`, so no code here shells out to a host CLI.

Usage:
    pysae-ai-tools mr review-note find <MR_IID>
    pysae-ai-tools mr review-note upsert <MR_IID>        # reads body from stdin
    pysae-ai-tools mr review-note add-reviewer <MR_IID>
"""

import json
import re
import sys
from typing import Annotated

import typer

from ..common.merge_requests.models import Note
from ..common.merge_requests.provider import MergeRequestProvider
from .resolve import resolve_provider

app = typer.Typer(help="Manage the single Claude review note on a merge request")

MARKER = "<!-- claude-review -->"

# Match bare #<number> that GitLab would auto-link as issue/MR references.
# Negative lookbehind: don't touch already-escaped \#, HTML entities &#, or URLs with #.
_BARE_ISSUE_REF_RE = re.compile(r"(?<!\\)(?<!&)#(\d+)")


def _escape_gitlab_refs(body: str) -> str:
    """Escape bare #N references to prevent GitLab auto-linking."""
    return _BARE_ISSUE_REF_RE.sub(r"\#\1", body)


def _note_sort_key(note: Note) -> int:
    return int(note.id) if note.id.isdigit() else 0


def find_review_notes(provider: MergeRequestProvider, mr_iid: str, *, own_only: bool = False) -> list[Note]:
    """Find Claude review notes on a MR, own notes first (most recent within each group).

    With ``own_only=True``, notes authored by other users are excluded — used by
    :func:`upsert_note` so we never overwrite a review note created by someone else.
    """
    current_user = provider.current_user()
    own: list[Note] = []
    others: list[Note] = []
    for note in provider.list_notes(mr_iid):
        if MARKER in note.body:
            (own if note.author == current_user else others).append(note)
    own.sort(key=_note_sort_key, reverse=True)
    others.sort(key=_note_sort_key, reverse=True)
    return own if own_only else own + others


def find_note(provider: MergeRequestProvider, mr_iid: str) -> Note | None:
    """Find the best Claude review note on a MR (own first, then others)."""
    candidates = find_review_notes(provider, mr_iid)
    return candidates[0] if candidates else None


def upsert_note(provider: MergeRequestProvider, mr_iid: str, body: str) -> str:
    """Create or update the review note. Returns 'created' or 'updated:<note_id>'.

    Only ever updates the current user's own review note: editing someone else's
    would rewrite their comment under their name. When none exists, a new note is
    created (prior reviews from other authors are carried forward by the caller).
    """
    body = _escape_gitlab_refs(body)
    if MARKER not in body:
        body = f"{body}\n\n{MARKER}"
    own = find_review_notes(provider, mr_iid, own_only=True)
    if own:
        provider.update_note(mr_iid, own[0].id, body)
        return f"updated:{own[0].id}"
    provider.add_note(mr_iid, body)
    return "created"


def add_reviewer(provider: MergeRequestProvider, mr_iid: str) -> str:
    """Add the current user as MR reviewer. Returns 'added', 'already-reviewer', or 'is-author'."""
    current_user = provider.current_user()
    mr = provider.get_mr(mr_iid)
    if mr.author == current_user:
        return "is-author"
    if current_user in mr.reviewers:
        return "already-reviewer"
    provider.set_reviewers(mr_iid, sorted(set(mr.reviewers) | {current_user}))
    return "added"


@app.command()
def find(
    mr_iid: Annotated[str, typer.Argument(help="MR IID")],
    project: Annotated[str, typer.Option("--project", help="Target another repo or a full URL")] = "",
) -> None:
    """Find the existing Claude review note (prints NONE or JSON)."""
    note = find_note(resolve_provider(project=project or None), mr_iid)
    typer.echo("NONE" if note is None else json.dumps({"id": note.id, "body": note.body}))


@app.command()
def upsert(
    mr_iid: Annotated[str, typer.Argument(help="MR IID")],
    project: Annotated[str, typer.Option("--project", help="Target another repo or a full URL")] = "",
) -> None:
    """Create or update the Claude review note (reads body from stdin)."""
    typer.echo(upsert_note(resolve_provider(project=project or None), mr_iid, sys.stdin.read()))


@app.command(name="add-reviewer")
def add_reviewer_cmd(
    mr_iid: Annotated[str, typer.Argument(help="MR IID")],
    project: Annotated[str, typer.Option("--project", help="Target another repo or a full URL")] = "",
) -> None:
    """Add the current user as reviewer on the MR."""
    typer.echo(add_reviewer(resolve_provider(project=project or None), mr_iid))
