"""search_in -> the backend corpora it reads (team corpora on /v1/search; Probe's docs are not one)."""

from __future__ import annotations
from ...shared.reads.search_contract import (
    TOOL_CORPUS_LEGACY,
    BackendCorpus,
    ToolCorpus,
    get_current_values)

# `search_in` vocabulary -> backend /v1/search `corpus` values. NOT a passthrough:
# the identity entries are what made "this is just `corpus` pluralised" such an
# easy wrong conclusion, which is why the tool parameter is not called `corpora`.
# Projects are one value among several, not an always-on floor: they are searched
# when the caller names nothing at all (no filter) or names them explicitly.
#
#   search_in      backend corpus        shape
#   transcripts -> transcripts           identity
#   projects -> experiments              renamed (the backend keeps its own word)
#   files -> files                       identity
#   github -> github                     identity
#
# Legacy spellings (`search_contract.TOOL_CORPUS_LEGACY`) are mapped to these
# before this table is read: `documents` arrives as github + files, so it still
# searches exactly the two corpora it always did.
#
# The table in `ToolCorpus`'s docstring carries this same mapping for callers, and
# tests/test_mcp_schema_docs.py fails if the two disagree.
_SEARCH_IN_TO_BACKEND: dict[str, set[BackendCorpus]] = {
    ToolCorpus.FILES: {BackendCorpus.FILES},
    ToolCorpus.GITHUB: {BackendCorpus.GITHUB},
    ToolCorpus.TRANSCRIPTS: {BackendCorpus.TRANSCRIPTS},
    ToolCorpus.PROJECTS: {BackendCorpus.EXPERIMENTS},
    # TWO backend corpora behind one agent-facing value (0125): an entity's notes
    # ride that entity's document in `experiments`, while the team note is its
    # own corpus. "Search what the team wrote down" is one question, so it gets
    # one value; making a caller choose the KIND of note first would require them
    # to know where the answer lives before they look for it.
    ToolCorpus.NOTES: {BackendCorpus.NOTES, BackendCorpus.EXPERIMENTS},
    ToolCorpus.DIGESTS: {BackendCorpus.DIGESTS},
    # ONE backend corpus, and NOT unioned with experiments even though papers
    # physically share that source_key. The backend does the separating; asking
    # for both here would make `["papers"]` return the 443 project documents
    # papers sit beside, which is the failure `_map_search_in` already describes
    # for the projects union it removed.
    ToolCorpus.PAPERS: {BackendCorpus.PAPERS},
}

#: `search_in` values POST /v1/search does not search, so they have no row above.
#: `docs` is Probe's own documentation, answered by `GET /public/v1/docs`. It is
#: split off in `ResearchReadService.search` BEFORE `_map_search_in`, which would
#: read a lone `["docs"]` as an unrecognized value (the experiments-only floor)
#: and a list stripped to `[]` as EVERY corpus -- team hits wearing a success
#: envelope either way. tests/test_mcp_schema_docs.py carves out exactly this set
#: from "every ToolCorpus value has a backend mapping".
NON_BACKEND_CORPORA = frozenset({ToolCorpus.DOCS})

# The knowledge-side values (every one except projects). Drives the kb_values
# missing-marker; carries no "always searched" implication for projects.
_KB_TOOL_VALUES = {
    ToolCorpus.FILES,
    ToolCorpus.GITHUB,
    ToolCorpus.TRANSCRIPTS,
    ToolCorpus.NOTES,
    ToolCorpus.DIGESTS,
    ToolCorpus.PAPERS,
}


def _map_search_in(search_in: list[str] | None) -> tuple[list[str] | None, list[str]]:
    """Translate the tool's `search_in` vocabulary into backend corpus values.

    Returns ``(backend_corpus_or_None, unsupported_values)``. Naming nothing means
    no filter (the backend searches every corpus).

    Naming values NARROWS to exactly those. Experiments used to be unioned in
    unconditionally, which made a narrowed search unusable in practice: the
    per-channel budget is roughly half of `top_k`, experiment projections
    outrank the knowledge corpora on most queries, and so `["transcripts"]`
    came back holding nothing but experiments. Ask for projects alongside by
    naming them (`["projects", "transcripts"]`)."""
    if not search_in:
        return None, []
    # A direct Python caller is not validated by the tool schema: map legacy spellings here too.
    search_in = get_current_values(list(search_in), TOOL_CORPUS_LEGACY)
    backend: set[str] = set()
    unsupported: list[str] = []
    for value in search_in:
        mapped = _SEARCH_IN_TO_BACKEND.get(value)
        if mapped is None:
            unsupported.append(value)
        else:
            backend.update(mapped)
    if not backend:
        # Every named value was unrecognized. Falling through with an empty
        # filter would search EVERYTHING and read as success; keep the old
        # experiments-only floor and let `unsupported_values` carry the miss.
        backend = {BackendCorpus.EXPERIMENTS}
    return sorted(backend), sorted(set(unsupported))
