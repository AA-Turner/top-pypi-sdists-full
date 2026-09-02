"""One summary line, whichever summary it appears in.

**A release note and a stand-up line are the same line.** They differ in which
tickets are in scope and how far the window reaches -- not in shape, not in field
order, not in vocabulary. They used to differ in all three: a stand-up rendered
`> BPAI-402 - Fix Lumen's Policy Info  [In Review]` above a date, a branch and a
separate pull-request line, while a release note rendered prose above
`BPAI-402 - Alex Y. - auditagent#124 - partly merged`. One team reading both
could not tell it was looking at one system.

So there is one formatter, here. Callers choose the medium -- Rich markup,
markdown, HTML -- and the scope. Never the layout.

The line, in order: **the sentence a person wrote**, then ticket, people, pull
requests, verdict. What a reader could not do before was act on it: a bullet said
a property report now runs end to end and did not say which ticket that was, who
built it, which pull requests delivered it, or how it was judged.

    - **New property report** -- a per-property report is now available end to
      end, from the underlying data through to the page a user opens.
      BPAI-334 · Unurbat T., George M. · bps-ui-v2#226, bps-api#587 · shipped

**The prose is never reformatted.** It is the one field a person wrote, and
rewrapping or re-punctuating it here would make the stored text and the rendered
text two different things. Everything after it is assembled from columns.

Nothing in here derives a verdict. The verdict is read from the row it was
written on -- see the migration that added the column for why recomputing one is
not the same answer. Spelling one out for a reader *is* here (`verdict_label`),
because the words are part of the line's shape: the same key has to read the same
way in a release note, a stand-up and on the dashboard, and it did not when the
vocabulary lived in `src/cli/utils` and this module imported it back.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from src.domain.release import ReleaseVerdict

#: How a verdict reads to a person, and the mark that carries it at a glance.
#:
#: The words are not the payload's `state` values verbatim: `partly_merged` is
#: a key, "partly merged" is English, and a release summary is read by people
#: who did not write the schema.
#: Keyed on `ReleaseVerdict` rather than on hand-written strings, so a member
#: added to the enum and forgotten here is a test failure rather than a verdict
#: that renders as its own key. `test_every_verdict_has_words` pins that.
_VERDICTS = {
    ReleaseVerdict.SHIPPED.value: ("✅", "shipped"),
    ReleaseVerdict.PARTLY_MERGED.value: ("◐", "partly merged"),
    ReleaseVerdict.NOT_MERGED.value: ("○", "not merged"),
    ReleaseVerdict.NOT_STARTED.value: ("○", "not started"),
    ReleaseVerdict.NO_CODE.value: ("⚠", "no code"),
    ReleaseVerdict.SHIPPED_UNTAGGED.value: ("⚠", "shipped, on no release"),
    ReleaseVerdict.RELEASE_CANDIDATE.value: ("◐", "open, on no release"),
    ReleaseVerdict.STARTED_UNTAGGED.value: ("○", "started, on no release"),
    ReleaseVerdict.ON_SHIPPED_RELEASE.value: ("⚠", "left behind by a release"),
    ReleaseVerdict.UNTICKETED.value: ("⚠", "merged, on no ticket"),
    ReleaseVerdict.UNTICKETED_DESIGN.value: ("○", "design, on no ticket"),
    ReleaseVerdict.CONTESTED.value: ("⚠", "names the wrong ticket"),
}


def verdict_label(state: Optional[str], *, icon: bool = True) -> str:
    """`partly_merged` → `◐ partly merged`, or the raw key if it is a new one.

    An unknown state prints itself rather than becoming an empty cell. A verdict
    this renderer has not been taught is still a fact about the release, and
    silently dropping it is how a new state ships invisibly.
    """
    key = str(state or "")
    mark, words = _VERDICTS.get(key, ("", key.replace("_", " ")))
    if not words:
        return ""
    return f"{mark} {words}" if icon and mark else words


#: Between the fields of the provenance line. A middle dot rather than a comma:
#: people are already comma-separated, and nesting one separator inside another
#: made "Unurbat T., George M." read as two fields.
SEP = " · "


def _number(pr: Dict[str, Any]) -> Optional[str]:
    """The pull request's number, from the field or from the end of its URL.

    A row recovered from a stand-up stores a URL and no number, and
    `.../pull/23` carries the number perfectly well. Reading it back beats
    rendering a bare repository name and calling that a pull request.
    """
    number = pr.get("number")
    if number:
        return str(number)
    url = (pr.get("url") or "").rstrip("/")
    tail = url.rsplit("/", 1)[-1] if url else ""
    return tail if tail.isdigit() else None


def pr_label(pr: Dict[str, Any]) -> str:
    """`repo#226`, and `repo#23 (open)` when it has not merged.

    **State is shown only when it is not `merged`.** Every pull request in a
    release's `included` block merged by definition, so marking each of them
    "(merged)" is noise on the common case -- while an *unmerged* one is the
    single most important thing about the line it sits on.
    """
    repo = (pr.get("repo") or "").strip()
    number = _number(pr)
    if not number and pr.get("branch"):
        # No pull request yet, so the branch *is* the reference. Rendered in the
        # same slot rather than a slot of its own -- one line shape, whichever of
        # the two a ticket has reached.
        branch = str(pr["branch"])
        return f"{repo}:{branch}" if repo else branch
    label = (
        f"{repo}#{number}"
        if repo and number
        else (repo or (f"#{number}" if number else ""))
    )
    if not label:
        return ""
    if pr.get("merged"):
        return label
    # **`merged` is the only field a release pull request carries**, and
    # `_PR_KEYS` trims a stored one to the same four -- so looking only for a
    # `state` key meant an unmerged release PR rendered byte-identical to a merged
    # one, on the field this docstring calls the most important thing on the line.
    state = (pr.get("state") or pr.get("pr_state") or "").strip()
    if state:
        # A stand-up row carries the real word, and it beats a guess.
        return f"{label} ({state})"
    if "merged" in pr:
        # Known not to have merged.
        return f"{label} (open)"
    # Neither field present, so the merge state is genuinely unknown -- and
    # "(open)" would be an assertion rather than a reading.
    return label


def provenance(
    *,
    ticket_ref: Optional[str] = None,
    people: Optional[Sequence[str]] = None,
    prs: Optional[Sequence[Dict[str, Any]]] = None,
    verdict: Optional[str] = None,
    when: Optional[str] = None,
    icon: bool = False,
) -> str:
    """The tail of a line: ticket, people, pull requests, verdict.

    Every field is optional and an absent one is *omitted*, never rendered as a
    dash or an empty slot: a bullet whose ticket nobody recorded should read as
    prose with less provenance, not as prose with a hole in it.

    Returns `""` when nothing is known, so a caller can append it unconditionally.

    `icon` is the one thing a caller decides, and it is a *rendering* of the
    verdict rather than a different field: both terminal surfaces pass `True`, so
    they stay identical to each other, and HTML takes the words. It is not a knob
    for changing which fields appear or what order they come in -- that is the
    whole of what this function exists to stop.
    """
    parts: List[str] = []
    if ticket_ref:
        parts.append(ticket_ref)
    named = [p for p in (people or []) if p]
    if named:
        parts.append(", ".join(named))
    labels = [pr_label(pr) for pr in (prs or [])]
    labels = [label for label in labels if label]
    if labels:
        parts.append(", ".join(labels))
    if verdict:
        # **One translation, and it is the one above.** This claimed to be that
        # one place while `release_view._VERDICTS` was another, and the two
        # disagreed: `shipped_untagged` read "shipped, on no release" in
        # `releases summarize` and "shipped untagged" in `summary --release` and
        # on the dashboard -- the same verdict, two phrasings, across the very
        # surfaces this module exists to keep identical.
        #
        # **The slot holds where the thing stands, and a verdict is only one way
        # of knowing that.** A stand-up row that no release has judged has no
        # verdict and does have a board column, so a caller passes that instead.
        # One slot, one meaning, sourced by precedence -- rather than a verdict
        # slot that is empty on every stand-up and a status chip that appears on
        # nothing else.
        parts.append(verdict_label(verdict, icon=icon))
    if when:
        # **The one field scope decides, and it is still the same line.** A
        # stand-up covers a stretch of days, so *when* something moved inside it
        # is information; a release covers a release, and the header already says
        # which. Last, so every field before it lines up between the two.
        parts.append(when)
    return SEP.join(parts)


def headline(body_markdown: Optional[str], fallback_title: Optional[str]) -> str:
    """What the line *says* -- the sentence somebody wrote about it.

    The ticket's own title stands in when nobody has written one: an unnarrated
    line still has to read as something, and "no prose yet" is not a reason to
    render an empty bullet. One rule, so a stand-up and a release note lead with
    the same kind of text rather than one leading with prose and the other with a
    ref and a title.
    """
    return (body_markdown or "").rstrip() or (fallback_title or "").strip()


def bullet(
    body_markdown: Optional[str],
    *,
    fallback_title: Optional[str] = None,
    ticket_ref: Optional[str] = None,
    people: Optional[Sequence[str]] = None,
    prs: Optional[Sequence[Dict[str, Any]]] = None,
    verdict: Optional[str] = None,
    when: Optional[str] = None,
    indent: str = "  ",
    marker: str = "- ",
) -> str:
    """A full line, prose first.

    `indent` aligns the provenance line under the prose rather than under the
    list marker, so a bullet reads as one block and a run of them scans as a
    column of prose with a column of provenance beneath each.
    """
    prose = headline(body_markdown, fallback_title)
    tail = provenance(
        ticket_ref=ticket_ref, people=people, prs=prs, verdict=verdict, when=when
    )
    if not prose:
        return f"{indent}{tail}" if tail else ""
    if not tail:
        return f"{marker}{prose}"
    return f"{marker}{prose}\n{indent}{tail}"
