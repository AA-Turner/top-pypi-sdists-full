"""Probe's own docs as a corpus: alone in the whole budget, or beside the team's hits in half of it."""

from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ....sdk import errors
from ....foundation.token_budget.token_budget import MIN_TOKENS as _MIN_TOKEN_BUDGET
from ....foundation.token_budget.token_budget import MAX_TOKENS as _MAX_TOKEN_BUDGET
from ....foundation.token_budget.token_budget import Budget
from ....shared.reads.search_contract import (
    DOCS_QUERY_MAX_CHARS,
    DocsState,
    EntityType,
    EnvelopeState,
    MissingMarker,
    ToolCorpus)
from probe.mcp.tools.shaping.shaping import _budget_cost, _largest


# -- search_in=["docs"]: Probe's own docs --------------------------------------
#
# Not the team's record, so not POST /v1/search: `GET /public/v1/docs` answers
# with whole `##` sections, best first, and this side packs them into the
# caller's `token_budget` with the real tokenizer. A section is the unit of an
# answer, so it arrives whole or visibly cut (`truncated`, `retry_with`), never
# silently shortened; and the best one always arrives, because a docs search that
# returns nothing for budget reasons costs a second call to learn why.

#: The most docs sections one search asks for: `top_k` caps them, and this caps
#: `top_k` at what `GET /public/v1/docs` accepts (`limit` 1..20); more would be a
#: 422 that reads as "docs could not be read".
_DOCS_SECTION_CAP = 20

_DOCS_UNAVAILABLE_NOTE = "Probe's docs could not be read right now."
_DOCS_STALE_NOTE = (
    "Probe's docs site could not be read just now: these sections are from the last good copy."
)
_DOCS_QUERY_NOTE = (
    f"Probe's docs were not searched: they take a query of 1 to {DOCS_QUERY_MAX_CHARS} characters."
)


def _docs_query_problem(query: str) -> str | None:
    """Why the docs route would refuse this query (it answers 422), or None."""
    if not query.strip():
        return 'search_in=["docs"] needs a query: name the feature, command or error to look up'
    if len(query) > DOCS_QUERY_MAX_CHARS:
        return (
            f'search_in=["docs"] takes a query of at most {DOCS_QUERY_MAX_CHARS} characters '
            f"(this one has {len(query)}): name the feature, command or error, not the whole question"
        )
    return None


def _docs_hit(section: dict, position: int, text: str, *, retry_with: dict | None = None) -> dict:
    """One docs section as a search hit: a terminal `document` whose card is the
    section. `retry_with` marks a cut one with the search that carries it whole."""
    page = str(section.get("page") or "").strip()
    heading = str(section.get("heading") or "").strip()
    title = f"{page} — {heading}" if page and heading and heading != page else page or heading
    card = {"title": title, "snippet": text}
    url = section.get("url")
    if isinstance(url, str) and url:
        card["source_url"] = url
    rank = section.get("rank")
    if not isinstance(rank, int) or isinstance(rank, bool) or rank < 0:
        rank = position
    hit: dict[str, Any] = {
        "entity_type": EntityType.DOCUMENT,
        "card": card,
        # The repo's rank convention: ordinal, never a similarity.
        "why_matched": {"score": max(0.0, round(1.0 - 0.01 * rank, 2))},
        "truncated": retry_with is not None,
    }
    if retry_with is not None:
        hit["retry_with"] = retry_with
    return hit


def _docs_budget_hint(tokens: int) -> int:
    """`tokens` as a `token_budget` to pass back: rounded UP to the next hundred
    (as `_budget_for`), within the tool's range."""
    return max(_MIN_TOKEN_BUDGET, min(_MAX_TOKEN_BUDGET, -(-tokens // 100) * 100))


def _docs_more_note(left_out: int) -> str:
    """A mixed search's line for the docs sections its half of the budget left out."""
    sections = "section" if left_out == 1 else "sections"
    return (
        f"{left_out} more Probe docs {sections} matched; "
        'search with search_in=["docs"] alone to read them.'
    )


def _pack_docs(
    sections: list[dict],
    fits: Callable[[list[dict]], bool],
    retry: Callable[[list[dict]], dict],
) -> list[dict]:
    """Docs sections as hits, WHOLE and best first, as many as `fits` admits.

    The first section that does not fit whole is cut at a paragraph boundary to
    the space left, marked `truncated`, and given `retry_with`: the search at
    which it arrives whole (`retry`, given the hits up to it, it whole); nothing
    after it is shown. The best section is never dropped: if not even its first
    paragraph fits, it is cut mid-paragraph instead."""
    hits: list[dict] = []
    for position, section in enumerate(sections):
        text = section["text"]
        whole = _docs_hit(section, position, text)
        if fits([*hits, whole]):
            hits.append(whole)
            continue
        retry_with = retry([*hits, whole])

        def cut(snippet: str, section: dict = section, position: int = position) -> dict:
            return _docs_hit(section, position, snippet, retry_with=retry_with)

        paragraphs = text.split("\n\n")
        # `len(paragraphs)` of them is the whole section, which did not fit.
        kept = _largest(
            len(paragraphs) - 1, lambda n: fits([*hits, cut("\n\n".join(paragraphs[:n]))])
        )
        if kept:
            hits.append(cut("\n\n".join(paragraphs[:kept])))
        elif not hits:
            end = _largest(len(text) - 1, lambda n: fits([cut(text[:n])]))
            hits.append(cut(text[:end]))
        break
    return hits


class DocsSearchMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _read_docs(self, query: str, top_k: int) -> tuple[list[dict], str | None, bool]:
        """Probe's docs sections for `query` (best first, at most `top_k`), the note
        the response carries about them (None when they answered fresh), and
        whether they were read at all.

        The docs being down is a NOTE, never an exception: a mixed search keeps
        its team results, and a docs-only one says what happened instead of
        failing the call."""
        limit = max(1, min(int(top_k), _DOCS_SECTION_CAP))
        try:
            response = self.source.docs(query, limit=limit)
        except (errors.RosError, ValueError):
            # ValueError: a 2xx whose body is not JSON (an ingress page).
            return [], _DOCS_UNAVAILABLE_NOTE, False
        state = response.get("state") if isinstance(response, dict) else None
        if state not in (DocsState.OK, DocsState.STALE):
            # `unavailable` (no copy yet), or a body this side cannot read.
            return [], _DOCS_UNAVAILABLE_NOTE, False
        raw = response.get("sections")
        sections = [
            section
            for section in (raw if isinstance(raw, list) else [])
            if isinstance(section, dict) and isinstance(section.get("text"), str)
        ]
        return sections[:limit], (_DOCS_STALE_NOTE if state == DocsState.STALE else None), True

    def _search_docs_only(
        self, query: str, *, top_k: int, token_budget: int, verbose: bool, cursor: str | None
    ) -> dict:
        """`search_in=["docs"]`: Probe's docs alone, in the whole `token_budget`.

        No team search runs, so the team-search arguments (`project_id`,
        `workspace_id`, `collapse`, `semantic`, `exclude_session`) have nothing
        to apply to. One page: a cut section names the budget that carries it
        whole (`retry_with`), which is the way to read on."""
        if cursor:
            raise errors.ValidationError(
                'search_in=["docs"] answers in one page and returns no cursor: to read '
                "more, repeat it with a larger token_budget (a cut hit names one in retry_with)",
                status=422,
            )
        problem = _docs_query_problem(query)
        if problem is not None:
            raise errors.ValidationError(problem, status=422)
        sections, note, read = self._read_docs(query, top_k)
        budget = Budget(max(_MIN_TOKEN_BUDGET, min(int(token_budget), _MAX_TOKEN_BUDGET)))
        build = self._docs_only_builder(query, sections, note, read, verbose=verbose)
        hits = _pack_docs(
            sections,
            lambda hits: budget.fits(build(hits)),
            lambda hits: {"token_budget": _docs_budget_hint(_budget_cost(build(hits)))},
        )
        return build(hits)

    def _docs_only_builder(
        self, query: str, sections: list[dict], note: str | None, read: bool, *, verbose: bool
    ) -> Callable[[list[dict]], dict]:
        """The `search_in=["docs"]` envelope around some hits of `sections`. Left-out
        sections are counted, with the budget that carries them all when one does
        (measured once, when first needed)."""
        fits_all: list[int | None] = []

        def build(hits: list[dict]) -> dict:
            data: dict[str, Any] = {"query": query, "results": hits}
            if note:
                data["note"] = note
            missing = [] if read else [MissingMarker.DOCS]
            if len(hits) < len(sections):
                data["budget"] = {"results_available": len(sections)}
                if not fits_all:
                    whole = [_docs_hit(s, i, s["text"]) for i, s in enumerate(sections)]
                    needed = -(-_budget_cost(build(whole)) // 100) * 100
                    fits_all.append(needed if needed <= _MAX_TOKEN_BUDGET else None)
                if fits_all[0] is not None:
                    data["budget"]["fits_all_at_token_budget"] = fits_all[0]
            if len(hits) < len(sections) or any(hit["truncated"] for hit in hits):
                missing.append(MissingMarker.RESULTS_BEYOND_BUDGET)
            return self._envelope(
                data,
                state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
                missing=sorted(missing),
                verbose=verbose,
            )

        return build

    def _docs_beside_team(
        self, query: str, top_k: int, budget: Budget, *, verbose: bool
    ) -> tuple[list[dict], str | None, bool, bool]:
        """The `docs` list of a mixed search, its note, whether the docs were read,
        and whether sections were left out. At most HALF the budget, so the team's
        results (what most of such a search is for) keep the rest. A cut hit's
        `retry_with` is the budget whose half carries it whole or, past the
        ceiling, the docs-only search that does."""
        if _docs_query_problem(query) is not None:
            return [], _DOCS_QUERY_NOTE, False, False
        sections, note, read = self._read_docs(query, top_k)
        share = budget.token_budget // 2
        docs_only = self._docs_only_builder(query, sections, note, read, verbose=verbose)

        def retry(hits: list[dict]) -> dict:
            mixed = 2 * _budget_cost({"docs": hits})
            if mixed <= _MAX_TOKEN_BUDGET:
                return {"token_budget": _docs_budget_hint(mixed)}
            return {
                "search_in": [ToolCorpus.DOCS.value],
                "token_budget": _docs_budget_hint(_budget_cost(docs_only(hits))),
            }

        hits = _pack_docs(
            sections,
            lambda hits: budget.fits({"docs": hits}, reserve=budget.token_budget - share),
            retry,
        )
        left_out = len(sections) - len(hits)
        if left_out:
            more = _docs_more_note(left_out)
            note = f"{note} {more}" if note else more
        return hits, note, read, left_out > 0
