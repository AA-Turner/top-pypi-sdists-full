"""Framework-independent implementation of the read-only MCP operations."""

from __future__ import annotations

import base64
import binascii
import json
from dataclasses import dataclass, field
from dataclasses import replace as dataclass_replace
from datetime import datetime, timezone
from itertools import islice
from collections.abc import Callable
from typing import Any

from ._generated.sql import MAX_ROWS_CEILING
from ..sdk import errors, links
from ..sdk.notes import read_advisory
from . import accounting
from .budget import BYTES_PER_TOKEN as _BYTES_PER_TOKEN
from .budget import MIN_TOKENS as _MIN_TOKEN_BUDGET
from .budget import MAX_TOKENS as _MAX_TOKEN_BUDGET
from .budget import Budget, count_tokens, serialize
from .contract import (
    BackendCorpus,
    BackendSearchState,
    Channel,
    ChannelError,
    CollapseMode,
    EntityType,
    EnvelopeState,
    MatchMode,
    MissingMarker,
    ToolCorpus,
    VIEW_PURPOSE,
    View,
    WebState,
)
from .continuation import omit_defaults
from .delivery_context import current_delivery, pin_document, source_changed
from .source import ResearchOSSource

# `search_in` vocabulary -> backend /v1/search `corpus` values. NOT a passthrough:
# three entries are identity and one is not, which is the whole reason the tool
# parameter is no longer called `corpora` -- the identity majority is exactly what
# made "this is just `corpus` pluralised" such an easy wrong conclusion.
# Experiments are one value among four, not an always-on floor: they are searched
# when the caller names nothing at all (no filter) or names them explicitly.
#
#   search_in      backend corpus        shape
#   transcripts -> transcripts           identity
#   experiments -> experiments           identity
#   files -> files                       identity
#   documents -> github + files          fans out
#
# `documents` deliberately overlaps `files`: it is the broader ask (workspace
# files PLUS indexed github docs), and `files` is the narrower one.
#
# The tool docstring in server.py carries this same table for callers, and
# tests/test_mcp_schema_docs.py fails if the two disagree.
_SEARCH_IN_TO_BACKEND: dict[str, set[BackendCorpus]] = {
    ToolCorpus.FILES: {BackendCorpus.FILES},
    ToolCorpus.DOCUMENTS: {BackendCorpus.GITHUB, BackendCorpus.FILES},
    ToolCorpus.TRANSCRIPTS: {BackendCorpus.TRANSCRIPTS},
    ToolCorpus.EXPERIMENTS: {BackendCorpus.EXPERIMENTS},
    # TWO backend corpora behind one agent-facing value (0125): an entity's notes
    # ride that entity's document in `experiments`, while the team note is its
    # own corpus. "Search what the team wrote down" is one question, so it gets
    # one value; making a caller choose the KIND of note first would require them
    # to know where the answer lives before they look for it.
    ToolCorpus.NOTES: {BackendCorpus.NOTES, BackendCorpus.EXPERIMENTS},
    ToolCorpus.DIGESTS: {BackendCorpus.DIGESTS},
    # ONE backend corpus, and NOT unioned with experiments even though papers
    # physically share that source_key. The backend does the separating; asking
    # for both here would make `["papers"]` return the 443 experiment documents
    # papers sit beside, which is the failure `_map_search_in` already documents
    # for the experiments union it removed.
    ToolCorpus.PAPERS: {BackendCorpus.PAPERS},
}

# The knowledge-side values (every one except experiments). Drives the kb_values
# missing-marker; carries no "always searched" implication for experiments.
_KB_TOOL_VALUES = {
    ToolCorpus.FILES,
    ToolCorpus.DOCUMENTS,
    ToolCorpus.TRANSCRIPTS,
    ToolCorpus.NOTES,
    ToolCorpus.DIGESTS,
    ToolCorpus.PAPERS,
}

# Backend caps top_k / exact_limit.
_BACKEND_CHANNEL_CAP = 50

#: The run -> run family, spelled literally rather than imported.
#: (Mirrors `app.lineage.schemas.GENEALOGY_RELATIONS`, a module the MCP cannot
#: import -- same reason `_CAPTURED_AGENTS` is spelled out in `accounting.py`.
#: Deliberately NOT read from `probe.models.LineageRelation` either: that file is
#: a build artifact of `make regen`, and this filter must hold on an install whose
#: regen has not run yet.)
#: Genealogy is reported under `run_ancestry`; letting it into `edges` too would
#: report every retry twice.
_GENEALOGY_RELATIONS = frozenset({"forked_from", "resumed_from", "retried_from", "branched_from"})

#: What a lineage read says to a server without the read routes (0255).
_NO_READ_LINEAGE = (
    "this server does not record what runs read yet (it lacks the run_inputs "
    "feature): file readers and the upstream walk need a newer server"
)

#: Links a project or experiment `lineage` view carries on its first page, per
#: list (its own links; the links among an experiment's runs and files). They
#: are the fixed part of a view whose rows are its children, so they are bounded
#: here, and a cut is flagged rather than passed off as the whole graph.
_LINEAGE_LINKS_CAP = 20

#: Card cap: the card is the cheap glance, and `token_budget` bounds ROWS,
#: not payload -- so each block caps itself.
_MAX_CARD_CONTRIBUTORS = 8


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _text(record: dict) -> str:
    fields = [
        record.get("id"),
        record.get("slug"),
        record.get("name"),
        record.get("description"),
        record.get("question"),
        " ".join(record.get("tags") or []),
    ]
    return " ".join(str(value) for value in fields if value).lower()


def _map_search_in(search_in: list[str] | None) -> tuple[list[str] | None, list[str]]:
    """Translate the tool's `search_in` vocabulary into backend corpus values.

    Returns ``(backend_corpus_or_None, unsupported_values)``. Naming nothing means
    no filter (the backend searches every corpus).

    Naming values NARROWS to exactly those. Experiments used to be unioned in
    unconditionally, which made a narrowed search unusable in practice: the
    per-channel budget is roughly half of `top_k`, experiment projections
    outrank the knowledge corpora on most queries, and so `["transcripts"]`
    came back holding nothing but experiments. Ask for experiments alongside by
    naming them (`["experiments", "transcripts"]`)."""
    if not search_in:
        return None, []
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


#: How much of the engine's rationale a card carries. Long enough for a reason,
#: short enough that it cannot become the card. The engine's schema says the
#: same thing, but `maxLength` is advisory on its provider, so this is the cap
#: that actually holds.
_REASON_MAX_CHARS = 200


def _why_matched(
    mode: str,
    channel: str,
    *,
    score: float | None = None,
    reason: str | None = None,
) -> dict:
    """A stable, channel-uniform provenance shape: {mode, channel, score}.

    `terms` went with the keyword fallback, which was the only channel that ever
    populated it. Kept as an always-empty list it would have been a documented
    field that structurally cannot carry a value — the same shape of lie as a
    capability flag hardcoded to the wrong answer.

    `reason` is the gatherer's one line about why this chunk answers the query.
    It lives HERE rather than as a second top-level `why` because "why is this
    result in front of me" is one question: `mode`/`channel`/`score` are how the
    machinery found it, `reason` is why the reader that read it thinks it fits.
    Two differently-named `why` fields on one card is a question asked twice.
    Absent -- not empty -- when the engine sent none, which is most hits: the
    recall floor backfills from the fused pool, and no model ever read those.
    """
    why: dict[str, Any] = {"mode": mode, "channel": channel, "score": score}
    if reason:
        why["reason"] = reason[:_REASON_MAX_CHARS]
    return why


def _section(response: Any, key: str) -> dict[str, Any]:
    """Normalize one per-channel section of a /v1/search response, degrading a
    malformed body to an empty section with an explicit error marker (so a
    broken proxy/server yields state=partial, never an exception)."""
    section = response.get(key) if isinstance(response, dict) else None
    if not isinstance(section, dict):
        return {"results": [], "cursor": None, "error": ChannelError.MALFORMED_RESPONSE}
    raw = section.get("results")
    rows = [row for row in raw if isinstance(row, dict)] if isinstance(raw, list) else []
    error = section.get("error")
    error = error if isinstance(error, str) else (str(error) if error else None)
    if not isinstance(raw, list) or len(rows) != len(raw):
        error = error or ChannelError.MALFORMED_RESPONSE
    cursor = section.get("cursor")
    return {
        "results": rows,
        "cursor": cursor if isinstance(cursor, str) else None,
        "error": error,
        # Carried through so the tool can surface them. Type-guarded like
        # everything else here: a malformed body must degrade, never raise.
        "total_candidates": (
            section["total_candidates"]
            if isinstance(section.get("total_candidates"), int)
            else None
        ),
        # Did the server apply the self-exclusion we asked for? THREE-STATE and
        # the states must not collapse: True applied, False this-server-knows-
        # the-field-and-we-asked-for-nothing, None this-server-is-older-and
        # -ignored-us. Anything non-boolean degrades to None, which is the
        # honest reading: a value we cannot interpret is not a confirmation.
        "exclusion_applied": (
            section["exclusion_applied"]
            if isinstance(section.get("exclusion_applied"), bool)
            else None
        ),
        # How many rows the caller's own session accounted for. Zero is not
        # "unknown": it is the evidence that the exclusion changed nothing, and
        # the stop marker must not fire without it.
        "excluded_count": (
            section["excluded_count"] if isinstance(section.get("excluded_count"), int) else 0
        ),
        # Engine channels lost on a response that otherwise succeeded. Same
        # type-guard discipline: a malformed value degrades to "nothing lost"
        # rather than raising, and an older backend simply omits the field.
        "lost_channels": (
            [c for c in section["lost_channels"] if isinstance(c, str)]
            if isinstance(section.get("lost_channels"), list)
            else []
        ),
        "active_runs_count": (
            section["active_runs_count"]
            if isinstance(section.get("active_runs_count"), int)
            else None
        ),
        # The engine answered and the ANSWER is degraded (gatherer timeout,
        # truncated emit, schema repair, raw-pool fallback). Every channel can
        # be alive and this still be true, which is why it is carried
        # separately from `lost_channels`. Type-guarded: a malformed value
        # degrades to "not degraded", the safe direction mid-rollout, and an
        # older backend simply omits the field.
        "degraded": section.get("degraded") is True,
        "degraded_reason": (
            section["degraded_reason"] if isinstance(section.get("degraded_reason"), str) else None
        ),
        # How the engine graded the evidence it returned: EXTRACTED (matched
        # deterministically) vs INFERRED vs AMBIGUOUS. An agent weighing a
        # graph-reached claim against a literal one needs this, and it was
        # dropped at this boundary while the backend had been emitting it.
        "confidence_breakdown": (
            section["confidence_breakdown"]
            if isinstance(section.get("confidence_breakdown"), dict)
            else None
        ),
    }


def _exact_result(row: dict) -> dict:
    """An exact-channel hit (project | experiment | run | artifact) in the tool's
    result shape.

    `slug` rides in the card because it is the reason a run hit exists: the
    backend gained a runs branch precisely so a pasted petname resolves, and a
    caller who searched `tunneling-sambar-254` needs to see it echoed on the row
    -- the run's `name` may be server-derived or since edited, which makes a
    correct hit look unrelated to the query."""
    entity_type = row.get("entity_type")
    entity_id = row.get("id")
    card = {
        key: row.get(key)
        for key in (
            "name",
            "slug",
            "slug",
            "workspace_id",
            "project_id",
            "experiment_id",
            "run_id",
        )
        if row.get(key) is not None
    }
    resource = None
    if entity_type == EntityType.EXPERIMENT:
        resource = f"research://experiments/{entity_id}/card"
    elif entity_type == EntityType.PROJECT:
        resource = f"research://projects/{entity_id}/card"
    elif entity_type == EntityType.RUN:
        # Same target the semantic channel gives a run hit, so an agent gets one
        # addressable resource per run regardless of which channel surfaced it.
        resource = f"research://runs/{entity_id}/handoff"
    # artifacts have no addressable research:// resource (no single-GET route)
    return {
        "entity_type": entity_type,
        "id": entity_id,
        "card": card,
        "why_matched": _why_matched(MatchMode.EXACT, Channel.EXACT, score=row.get("score")),
        "resource": resource,
    }


def _chunk_reason(row: dict) -> str | None:
    """The first `why_relevant` the engine put on this hit's chunks.

    The backend already forwards it per chunk and the dashboard renders it; the
    card projection used to drop it on the floor, which meant the one line
    written by something that actually READ the passage never reached the agent
    the search was for.
    """
    for chunk in row.get("chunks") or []:
        if not isinstance(chunk, dict):
            continue
        reason = chunk.get("why_relevant")
        if isinstance(reason, str) and reason.strip():
            return reason.strip()
    return None


def _semantic_result(row: dict) -> dict:
    """A semantic-channel document hit (engine) in the tool's result shape.

    `id` is emitted ONLY when the engine's ref resolved the hit to an entity
    (any ref kind -- experiment, run, file, ...) -- there it is a real second
    address, distinct from the document. On a plain document hit it was byte-identical to `card.doc_id` in
    every measured response (10/10), so every knowledge hit paid ~40 tokens to
    say its address twice. Document rows are terminal (no `resource`, no
    `get_entity` route -- see #112's contract notes) and `card.doc_id` is their
    one address. Collapse/dedupe is unaffected: `_collapse_experiments` only
    keys experiment/run rows, which still carry `id`."""
    ref = row.get("ref") or {}
    kind = ref.get("kind") if isinstance(ref, dict) else None
    entity_id = ref.get("id") if isinstance(ref, dict) else None
    # A ref carrying kind WITHOUT id did not resolve: treating it as an entity
    # would emit "id": null (the null-free contract's one forbidden shape),
    # mint "research://experiments/None/card" — a resource that LOOKS
    # addressable and 404s — and give every such row the same
    # ("experiment", None) collapse key, silently merging distinct results.
    # As a document it keeps its one real address, card.doc_id.
    if not entity_id:
        kind = None
    resource = None
    if kind == EntityType.EXPERIMENT:
        resource = f"research://experiments/{entity_id}/card"
    elif kind == EntityType.PROJECT:
        # An experiment's semantic hit arrives as `project` since the doc-type
        # retire; the same card the exact channel gives a project hit, so the
        # collapse cannot keep a copy that lost its address.
        resource = f"research://projects/{entity_id}/card"
    elif kind == EntityType.RUN:
        resource = f"research://runs/{entity_id}/handoff"
    card = {
        key: row.get(key)
        for key in (
            "title",
            "snippet",
            "source_system",
            "source_url",
            "doc_id",
            # WHEN the indexed text was last written and WHICH corpus it came
            # from. Both were on the wire and dropped here, so an agent
            # weighing a six-month-old design note against a note from
            # yesterday had nothing to weigh with, and telling a team note
            # apart from a transcript meant parsing a doc id.
            "updated_at",
            "corpus",
        )
        if row.get(key) is not None
    }
    return {
        "entity_type": kind or EntityType.DOCUMENT,
        **({"id": entity_id} if kind else {}),
        "card": card,
        "why_matched": _why_matched(
            MatchMode.SEMANTIC,
            Channel.SEMANTIC,
            score=row.get("score"),
            reason=_chunk_reason(row),
        ),
        "resource": resource,
    }


def _interleave(first: list[dict], second: list[dict]) -> list[dict]:
    """Fair round-robin merge — the backend returns per-channel sections with no
    merged ranking, so neither channel gets to starve the other."""
    merged: list[dict] = []
    for index in range(max(len(first), len(second))):
        if index < len(first):
            merged.append(first[index])
        if index < len(second):
            merged.append(second[index])
    return merged


def _score(row: dict) -> float:
    value = (row.get("why_matched") or {}).get("score")
    return value if isinstance(value, (int, float)) else float("-inf")


def _in_project(row: dict, project_id: str) -> bool:
    """Whether an exact hit belongs to the requested project. Rows without a
    project linkage are conservatively dropped (never out-of-project hits)."""
    if row.get("project_id") == project_id:
        return True
    return row.get("entity_type") == EntityType.PROJECT and row.get("id") == project_id


#: Keys by which a view row NAMES another entity: its own id, an edge's two
#: ends, and the run a file or trial belongs to. A row naming a project,
#: experiment or run the caller's session created is that session's work (or
#: attached to it) and leaves the view.
_SESSION_WORK_REF_KEYS = ("id", "source_id", "target_id", "run_id")
#: Single-entity slots in a view payload ("where this came from", "which run
#: wrote it"). One naming the session's work is emptied rather than kept.
_SESSION_WORK_SLOTS = frozenset({"origin", "run", "written_by_run"})


def _names_session_work(node: dict, hidden: frozenset[str]) -> bool:
    for key in _SESSION_WORK_REF_KEYS:
        value = node.get(key)
        if isinstance(value, str) and value.lower() in hidden:
            return True
    label = node.get("uuid")
    if isinstance(label, str) and label.partition(":")[2].lower() in hidden:
        return True
    run = node.get("run")
    return isinstance(run, dict) and _names_session_work(run, hidden)


def _scrub_session_work(value: Any, hidden: frozenset[str]) -> Any:
    """`value` without the rows, edges and slots that name an entity in `hidden`
    (ids the caller's session created). Deterministic and structural: it walks
    every list and dict, so a view added later is covered without being named."""
    if isinstance(value, list):
        return [
            _scrub_session_work(item, hidden)
            for item in value
            if not (isinstance(item, dict) and _names_session_work(item, hidden))
        ]
    if isinstance(value, dict):
        return {
            key: (
                None
                if key in _SESSION_WORK_SLOTS
                and isinstance(item, dict)
                and _names_session_work(item, hidden)
                else _scrub_session_work(item, hidden)
            )
            for key, item in value.items()
        }
    return value


def _collapse_experiments(results: list[dict]) -> list[dict]:
    """``collapse="experiment"``: one hit per experiment id, keeping the
    best-scoring representative's channel provenance.

    RUN hits pass through (deduped by id) instead of being dropped: experiment
    is OPTIONAL grouping now (research-os 0054), so a project-direct run has no
    experiment-level hit to represent it — and the result rows carry no
    experiment linkage to tell a direct run from an attached one.

    Everything else — document/file/project/artifact hits — passes through too.
    Collapse DEDUPES; it does not filter. Dropping the non-experiment rows made
    every knowledge corpus unreachable through the default call: `search_in` maps
    transcripts/documents/files straight into the backend query, the backend
    returns them, and then this discarded all of them before the caller ever saw
    one. A search that silently answers a different question than it was asked is
    worse than one that errors."""

    def _key(row: dict) -> Any:
        # PROJECT is deduped too: since the experiments-as-subprojects doc-type
        # retire the server names an experiment by its project address in BOTH
        # channels, so an exact hit and a semantic hit on one experiment arrive
        # as two `project` rows with one id. Deduping only EXPERIMENT would
        # quietly stop collapsing the very thing this collapse is named after.
        if row.get("entity_type") not in (
            EntityType.PROJECT,
            EntityType.EXPERIMENT,
            EntityType.RUN,
        ):
            return None  # never deduped, never dropped
        return (row.get("entity_type"), row.get("id"))

    best: dict[Any, dict] = {}
    for row in results:
        key = _key(row)
        if key is None:
            continue
        kept = best.get(key)
        if kept is None or _score(row) > _score(kept):
            best[key] = row
    # Emit in the merged ranking order the caller was given: a collapsed
    # experiment takes the position of its FIRST occurrence, carrying the
    # best-scoring representative. Appending the pass-through rows at the end
    # instead would bury every document hit below every experiment hit.
    emitted: set[Any] = set()
    collapsed: list[dict] = []
    for row in results:
        key = _key(row)
        if key is None:
            collapsed.append(row)
        elif key not in emitted:
            emitted.add(key)
            collapsed.append(best[key])
    return collapsed


def _pack_cursor(payload: dict) -> str:
    """Pack a cursor payload into an opaque token that is deliberately NOT JSON.

    A raw ``json.dumps({...})`` cursor cannot survive the MCP tool layer. FastMCP's
    `pre_parse_json` runs json.loads on every string argument and, when the result
    is not a scalar, REPLACES the argument with the parsed object — so a JSON-object
    cursor reaches the tool as a dict and is rejected against ``cursor: str | None``.
    Pagination then works perfectly in-process and 422s over the wire, which is
    exactly how it shipped: no test calls the tool layer, they all call the service
    directly.

    Base64 keeps the token a string through that pre-parse, and makes it genuinely
    opaque, so nobody hand-builds one and depends on the shape."""
    raw = json.dumps(payload, sort_keys=True).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _unpack_cursor(cursor: str, *, hint: str) -> dict:
    """Opaque token -> its payload, or a ValidationError naming how to get a real one.

    Raw-JSON cursors are still accepted: tokens minted before cursors were packed
    are already in agent transcripts, and refusing them would turn a stale cursor
    into an error instead of a page."""
    for decode in (
        lambda: json.loads(
            base64.urlsafe_b64decode((cursor + "=" * (-len(cursor) % 4)).encode()).decode()
        ),
        lambda: json.loads(cursor),  # legacy: pre-pack raw-JSON cursor
    ):
        try:
            parsed = decode()
        except (json.JSONDecodeError, ValueError, TypeError, binascii.Error, UnicodeDecodeError):
            continue
        if isinstance(parsed, dict):
            return parsed
    raise errors.ValidationError(
        f"malformed cursor: pass the next_cursor value from a previous {hint} call",
        status=422,
    )


def _split_cursor(cursor: str | None) -> tuple[str | None, str | None]:
    """The tool's opaque cursor carries the per-channel backend cursors."""
    if not cursor:
        return None, None
    parsed = _unpack_cursor(cursor, hint="research_search")
    return parsed.get(Channel.EXACT), parsed.get(Channel.SEMANTIC)


def _join_cursor(exact: str | None, semantic: str | None) -> str | None:
    cursors = {
        key: value
        for key, value in ((Channel.EXACT.value, exact), (Channel.SEMANTIC.value, semantic))
        if value
    }
    return _pack_cursor(cursors) if cursors else None


# -- research_get: token budget, cursor, and the view table --------------------

# ~4 chars per token of JSON. Approximate on purpose: this only has to BOUND a
# payload, and a real tokenizer would drag a model dependency into a read path
# without making the bound any safer.
_CHARS_PER_TOKEN = 4

# Rows fetched past the caller's offset — far more than any sane token_budget
# emits, so a page costs one backend call. The slice is client-side because the
# spans/artifacts/events routes take no offset (only `limit`).
_PAGE_FETCH = 200

# `limit` ceilings from schema/openapi.json.
_SPAN_BACKEND_MAX = 10_000  # GET /v1/runs/{id}/spans
#: GET /v1/runs/{id}/trials caps ONE call at `MAX_LIMIT`, and pages with a real
#: keyset cursor -- so unlike the spans route it has no single-call ceiling, and
#: the bound below is this server's own: how far one view will walk, not what the
#: backend will serve. Ten hops.
_TRIAL_ROUTE_PAGE = 200
_TRIAL_BACKEND_MAX = 2_000
_METRIC_BACKEND_MAX = 100_000  # GET /v1/runs/{id}/metrics

# Row bounds for the coordinate reads. Grouped cells are aggregates (one per step
# bucket x group), so a few hundred already draws a chart; export points are raw
# and unbounded, so the tool serves ONE keyset page and hands the cursor back.
# Both are clamps, not defaults an agent can override past.
_GROUPED_ROWS_MAX = 2_000
_GROUPED_ROWS_DEFAULT = 500

# Transcript sectioning. GET /v1/sessions/{id}/transcript returns ONE complete
# document (no server-side windowing exists), so the view splits it into
# line-sections and lets the ordinary rows machinery bound and page them. 40
# lines is a screenful of dialogue -- big enough that a default budget reads
# meaningful context, small enough that the cursor lands with usable granularity.
_TRANSCRIPT_SECTION_LINES = 40
_TRANSCRIPT_CONTEXT_DEFAULT = 3
_TRANSCRIPT_CONTEXT_MAX = 20
_EXPORT_PAGE_MAX = 1_000
_EXPORT_PAGE_DEFAULT = 200

# `limit` at 200; the token budget trims below this anyway.


def _tokens(value: Any) -> int:
    return max(1, len(json.dumps(value, default=str)) // _CHARS_PER_TOKEN)


def _fit_whole_results(
    results: list[dict],
    build: Callable[[list[dict], dict | None], dict],
    budget: Budget,
    *,
    available: int | None = None,
) -> dict:
    """As many WHOLE result cards as the budget holds, and an honest note.

    A card is a fixed shape: title, preview, ids, url, provenance. It is never
    shrunk to make one more fit and never cut in half, so the only thing that
    bends is how many arrive. That is the trade this function exists to make --
    an agent can act on "there were 12, ask for 3,400 tokens next time", and
    cannot act on half a JSON object.

    Measured against the COMPLETE envelope, not the rows: completeness markers,
    the query echo and the budget note all cost tokens, and a fit computed on
    rows alone is a fit that overflows once the envelope is wrapped around it.
    Measured with the real tokenizer, too -- the chars/4 estimate used elsewhere
    in this file over-counts ids and repeated structure, and a response cut by a
    bad guess looks exactly like one cut by a real limit.
    """
    available = len(results) if available is None else available

    def note(_kept: int) -> dict:
        """What the trial envelope carries, so the measurement includes it."""
        return {"results_available": available}

    if not results:
        return build(results, None)

    # Binary search on the number of whole cards. `fits` is monotonic -- one
    # more card is never smaller -- so this lands on the largest prefix that
    # fits in ~6 exact measurements rather than walking the list. An estimate
    # (chars/4) is not enough on its own: it over-counts ids and repeated
    # structure, and a response cut by a bad guess is indistinguishable to the
    # caller from one cut by a real limit.
    low, high, kept = 1, len(results), 0
    while low <= high:
        mid = (low + high) // 2
        if budget.fits(build(results[:mid], note(mid))):
            kept, low = mid, mid + 1
        else:
            high = mid - 1

    if kept:
        if kept == available:
            return build(results, {"results_available": available})
        # Cut. Name the budget that would carry everything this search found,
        # so the caller has a number to act on rather than a wall to hit again.
        return build(
            results[:kept],
            {
                "results_available": available,
                "fits_all_at_token_budget": _budget_for(build, results),
            },
        )

    # Not even one card fits. Nothing is truncated to pretend otherwise.
    one = build(results[:1], {"results_available": available})
    needed = _budget_cost(one)
    refusal = build(
        [],
        {
            "results_available": available,
            "first_result_tokens": needed,
            **(
                {"min_token_budget": needed}
                if needed <= _MAX_TOKEN_BUDGET
                else {"read_instead": "entity"}
            ),
        },
    )
    # The compact envelope omits a complete `completeness`; a refusal never is one.
    missing = (refusal.get("completeness") or {}).get("missing", [])
    refusal["completeness"] = {
        "state": EnvelopeState.PARTIAL,
        "missing": sorted({*missing, MissingMarker.FIRST_RESULT_EXCEEDS_BUDGET}),
    }
    return refusal


def _budget_cost(payload: dict) -> int:
    """The smallest `token_budget` that admits this payload.

    A budget is TWO limits -- tokens, and `BYTES_PER_TOKEN` times as many bytes
    -- and either can bind. Text that tokenizes efficiently (ids, repeated
    structure, long runs of one character) hits the byte wall first, so a hint
    computed from tokens alone would name a budget that still refuses the
    payload. Answering with a number that does not work is worse than not
    answering.
    """
    text = serialize(payload)
    by_tokens = count_tokens(text)
    by_bytes = -(-len(text.encode("utf-8")) // _BYTES_PER_TOKEN)
    return max(by_tokens, by_bytes)


def _budget_for(
    build: Callable[[list[dict], dict | None], dict],
    results: list[dict],
) -> int:
    """The token budget at which every fetched result would have fitted.

    Rounded UP to the next hundred: a caller passing back the exact measurement
    would sit one token from the edge, and the next search's results are not the
    same size as this one's.
    """
    whole = _budget_cost(build(results, {"results_available": len(results)}))
    return min(_MAX_TOKEN_BUDGET, -(-whole // 100) * 100)


def _fit(rows: list, budget: int) -> list:
    """Select a source-page row window using a cheap size estimate.

    Always select the first row so no item becomes unreachable. The MCP
    continuation layer fragments oversized source pages and enforces the exact
    whole-response limit after every envelope and cursor is included. Direct
    service callers retain the legacy approximate selection behavior.
    """
    out: list = []
    spent = 0
    for row in rows:
        cost = _tokens(row)
        if out and spent + cost > budget:
            break
        out.append(row)
        spent += cost
    return out


def _fit_sections(sections: list[tuple[str, list]], budget: int) -> tuple[dict[str, list], bool]:
    """Spend one budget across several lists in priority order.

    research_context has no cursor, so unlike _fit there is no always-emit-one
    floor — nothing is paginating and a forced row would just blow the budget.
    Dropping rows silently is the failure to avoid, hence the `truncated` flag."""
    kept: dict[str, list] = {}
    truncated = False
    spent = 0
    for key, rows in sections:
        taken: list = []
        for row in rows:
            cost = _tokens(row)
            if spent + cost > budget:
                break
            taken.append(row)
            spent += cost
        truncated = truncated or len(taken) < len(rows)
        kept[key] = taken
    return kept, truncated


def _split_get_cursor(cursor: str | None, view: str) -> int:
    """research_get's opaque cursor, carrying ``{"view": v, "offset": n}``.

    The view is carried so a cursor can never be silently re-based onto another
    view — offset 40 of a trajectory means nothing in an events list, and quietly
    reinterpreting it would skip 40 events with no signal at all."""
    if not cursor:
        return 0
    parsed = _unpack_cursor(cursor, hint="research_get")
    try:
        offset, cursor_view = parsed["offset"], parsed["view"]
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
            raise ValueError
    except (ValueError, KeyError, TypeError):
        raise errors.ValidationError(
            "malformed cursor: pass the next_cursor value from a previous research_get call",
            status=422,
        ) from None
    if cursor_view != view:
        raise errors.ValidationError(
            f"cursor was issued for view={cursor_view!r} but this call asked for "
            f"view={view!r}: pass a cursor back with the view that produced it",
            status=422,
        )
    return offset


def _join_get_cursor(view: str, offset: int) -> str:
    return _pack_cursor({"offset": offset, "view": str(view)})


@dataclass(frozen=True)
class _Req:
    """What a view builder needs beyond the entity itself."""

    filters: dict[str, Any]
    offset: int


@dataclass
class _ViewData:
    """One view's payload, split by what SCALES.

    `rows` is the unbounded part — it is what token_budget bounds and what cursor
    walks. `payload` is the fixed-size part. A view with rows=None is ATOMIC: it is
    never truncated (see ResearchReadService.research_get).

    `more_beyond` says the backend has rows past the fetched window. It exists
    because forgetting it is a LIE, not an inefficiency: a bounded fetch of 200
    spans from a 500-span run would otherwise be emitted whole and reported
    complete, and the agent would believe it had read the entire trajectory.

    `no_match` says the view answered fully and the answer was "nothing satisfies
    that constraint". It is NOT `missing`: nothing is absent from the response, so
    reporting it as partial would read as a degraded backend rather than a real
    ceiling. See EnvelopeState.NO_MATCH for why the distinction is load-bearing.
    """

    payload: dict[str, Any] = field(default_factory=dict)
    rows: list[dict] | None = None
    rows_key: str = "rows"
    missing: list[str] = field(default_factory=list)
    more_beyond: bool = False
    no_match: bool = False


# (entity kind, view) -> builder method. Explicit and greppable: this table IS the
# answer to "what can I read about a run?", and _checked_view derives its error
# message from it, so a view can never be advertised without a builder behind it.
#: How much of the notes rides along on a card before it defers to
#: `view="notes"`. Bounded because a card is the cheap glance.
_NOTES_CARD_EXCERPT = 1200

#: Per-sub-note excerpt inside `view="notes"` (0146). Twenty of these is a
#: bounded ~14k characters — a section, never a context bomb.
_SUB_NOTE_VIEW_EXCERPT = 700

# These are projections of already-fetched fields, never another set of source
# reads. Long documents/configs are available through RECORD instead of riding
# every purpose-shaped view. A complete card is complete for this projection;
# its optional detail doors do not imply failed or incomplete delivery.
_ENTITY_IDENTITY_FIELDS = (
    "id",
    "slug",
    "name",
    "title",
    "kind",
    "status",
    "project_id",
    "experiment_id",
    "run_id",
    "parent_project_id",
    "parent_run_id",
    "parent_relation",
    "group_id",
    "created_at",
    "updated_at",
    "started_at",
    "ended_at",
)
_ENTITY_REF_FIELDS = ("id", "slug", "name", "kind", "project_id", "experiment_id", "run_id")
_CARD_FIELDS: dict[str, tuple[str, ...]] = {
    EntityType.PROJECT: (
        "workspace_id",
        "workspace_name",
        "repo",
        "code_source_count",
        "subproject_count",
        "experiment_count",
        "run_count",
        "direct_run_count",
        "active_run_count",
        "contributor_count",
    ),
    EntityType.EXPERIMENT: ("question", "run_count", "active_run_count"),
    EntityType.RUN: ("source", "env_ref", "counts"),
    EntityType.TRIAL: (
        "rollout_span_id",
        "provider",
        "step_index",
        "name_customized",
        "description_customized",
    ),
    EntityType.ARTIFACT: (
        "shared",
        "version",
        "version_id",
        "content_hash",
        "sha256",
        "size_bytes",
        "mime_type",
        "is_reference",
        "workspace_id",
        "shared_folder_id",
    ),
    EntityType.GROUP: (),
    EntityType.SESSION: ("session_id", "agent", "name", "work_observed"),
    EntityType.TEAM_NOTE: ("version",),
}
_CARD_DESCRIPTION_CHARS = 480
_CARD_TEXT_CHARS = 240
_CARD_LIST_ITEMS = 8


def _card_text(out: dict, entity: dict, key: str, limit: int) -> None:
    value = entity.get(key)
    if value is None:
        return
    if not isinstance(value, str):
        return
    out[key] = value[:limit]
    if len(value) > limit:
        out[f"{key}_truncated"] = True


def _card_summary(value: Any) -> tuple[Any, bool]:
    """Keep supplied headline values; never synthesize results or recurse into metadata."""
    if isinstance(value, str):
        return value[:_CARD_DESCRIPTION_CHARS], len(value) > _CARD_DESCRIPTION_CHARS
    if not isinstance(value, dict):
        return None, value is not None
    result: dict = {}
    truncated = False
    for key, item in value.items():
        if len(result) == _CARD_LIST_ITEMS or not isinstance(key, str):
            truncated = True
            continue
        if item is None or isinstance(item, (bool, int, float)):
            result[key] = item
        elif isinstance(item, str):
            result[key] = item[:_CARD_TEXT_CHARS]
            truncated |= len(item) > _CARD_TEXT_CHARS
        else:
            truncated = True
    return result, truncated


def _entity_projection(kind: str, entity: dict, *, card: bool, document: bool = False) -> dict:
    """Per-kind useful glance, or minimal identity beside an explicit detail read."""
    keys = _ENTITY_IDENTITY_FIELDS if card else _ENTITY_REF_FIELDS
    out = {key: entity[key] for key in keys if key in entity}
    if document and "status" in entity:
        out["status"] = entity["status"]
    # `summary_metrics` since the rename; `summary` is the deprecated alias an
    # older server still emits. Reading both keeps this client working across a
    # server that has already dropped the alias AND one that has not.
    summary_key = "summary_metrics" if "summary_metrics" in entity else "summary"
    if (card or document) and summary_key in entity:
        summary, truncated = _card_summary(entity[summary_key])
        # An empty summary (`{}`, "") is omitted like an absent one: it rode every
        # document read as `"summary": {}`, a key with nothing in it. Kept when
        # truncation emptied it, so `summary_truncated` has what it describes.
        if summary is not None and (summary or truncated):
            out["summary"] = summary
        if truncated:
            out["summary_truncated"] = True
    if not card:
        return out
    out.update({key: entity[key] for key in _CARD_FIELDS[kind] if key in entity})
    _card_text(out, entity, "description", _CARD_DESCRIPTION_CHARS)
    _card_text(out, entity, "question", _CARD_DESCRIPTION_CHARS)
    if kind == EntityType.ARTIFACT:
        _card_text(out, entity, "resolution_note", _CARD_DESCRIPTION_CHARS)
        if entity.get("shared") is False:
            # An id-only resolution still proves existence. Versions are the
            # available by-id detail; RECORD cannot manufacture missing metadata.
            out["read_versions"] = 'view="versions"'
    if isinstance(entity.get("tags"), list):
        tags = entity["tags"]
        out["tags"] = [str(tag)[:_CARD_TEXT_CHARS] for tag in tags[:_CARD_LIST_ITEMS]]
        if len(tags) > _CARD_LIST_ITEMS or any(len(str(t)) > _CARD_TEXT_CHARS for t in tags):
            out["tags_truncated"] = True
    if kind == EntityType.GROUP and "spec" in entity:
        # A small sweep definition is the group's meaning. For a large one,
        # show its dimension names and an explicit excerpt, not an apparently
        # complete subset that changes the sweep's scientific interpretation.
        spec = entity["spec"]
        encoded = json.dumps(spec, ensure_ascii=False, default=str, separators=(",", ":"))
        if len(encoded) <= 800:
            out["spec"] = spec
        else:
            out["spec_excerpt"] = encoded[:800]
            out["spec_truncated"] = True
    if kind == EntityType.SESSION:
        # The work inventory is the useful first answer for a session. Keep
        # names and exact observed counts, with RECORD for larger inventories.
        for key in ("projects", "experiments", "runs", "artifacts"):
            if key not in entity:
                continue
            rows = entity[key]
            if rows is None:
                out[key] = None
                continue
            out[key] = [
                {field: row[field] for field in ("id", "name", "slug", "status") if field in row}
                for row in rows[:_CARD_LIST_ITEMS]
            ]
            out[f"{key}_count"] = len(rows)
            if len(rows) > _CARD_LIST_ITEMS:
                out[f"{key}_truncated"] = True
    if kind == EntityType.TEAM_NOTE:
        # This singleton names the document itself: asking for it must deliver
        # briefing text immediately. The common delivery boundary pages it.
        out["body"] = entity.get("body") or ""
    return out


def _record_field(entity: dict, field: Any) -> tuple[list[str | int], Any]:
    """Select a literal JSON path, without expressions, wildcards, eval or getattr."""
    if isinstance(field, str):
        path = field.removeprefix("$.").split(".")
    elif isinstance(field, list):
        path = field
    else:
        raise errors.ValidationError(
            "record field must be a dotted string or a path list", status=422
        )
    if (
        not path
        or len(path) > 32
        or any(
            isinstance(part, bool)
            or not isinstance(part, (str, int))
            or (isinstance(part, str) and (not part or len(part) > 512))
            or (isinstance(part, int) and part < 0)
            for part in path
        )
    ):
        raise errors.ValidationError("invalid record field path", status=422)
    value: Any = entity
    for part in path:
        if isinstance(value, dict) and isinstance(part, str) and part in value:
            value = value[part]
        elif isinstance(value, list) and isinstance(part, int) and part < len(value):
            value = value[part]
        else:
            raise errors.NotFoundError("record field not found")
    return path, value


def _notes_excerpt(text: str | None, *, read_all: str = 'view="notes"') -> dict | None:
    """The `{text, truncated, read_all?}` block a card carries, or None.

    ONE renderer for every carrier (0124): a note reads the same whether it hangs
    off a project, experiment, run, group or artifact, and the shape matches the
    browse orientation's excerpt so the product feels like one thing rather than
    four independently invented excerpt formats.

    None rather than an empty block when there is nothing: a `notes` key with no
    text reads as "this entity has notes" and is worse than silence.
    """
    if not text:
        return None
    truncated = len(text) > _NOTES_CARD_EXCERPT
    excerpt: dict = {"text": text[:_NOTES_CARD_EXCERPT], "truncated": truncated}
    if truncated:
        excerpt["read_all"] = read_all
    return excerpt


def _span_subtree(spans: list[dict], root_id: str) -> list[dict] | None:
    """`root_id`'s span and every descendant of it within `spans`, or None.

    None means the ROOT was not in the slice, which is a different fact from an
    empty subtree and must not be flattened into one: a rollout with no children
    is a trial that did nothing, a rollout that was not read is a trial nobody
    can see yet. The two get different markers upstream for that reason.

    Depth-first from the root, so the rows arrive in the order a reader walks
    them -- a rollout followed by its first turn followed by that turn's tool
    calls, rather than the flat step-ordered list the route returns. Cycles
    cannot happen (a span's parent is written once, at creation) but the `seen`
    guard is kept anyway: a malformed slice would otherwise hang the read.
    """
    children: dict[str, list[dict]] = {}
    root: dict | None = None
    for span in spans:
        if str(span.get("id")) == root_id:
            root = span
        parent = span.get("parent_span_id")
        if parent:
            children.setdefault(str(parent), []).append(span)
    if root is None:
        return None
    out: list[dict] = []
    seen: set[str] = set()
    stack = [root]
    while stack:
        span = stack.pop()
        span_id = str(span.get("id"))
        if span_id in seen:
            continue
        seen.add(span_id)
        out.append(span)
        stack.extend(reversed(children.get(span_id, [])))
    return out


_VIEWS: dict[tuple[str, str], str] = {
    # 0124: run/experiment/group cards carry a notes excerpt, and each kind gains
    # a full `notes` view. The project set the precedent and the argument is the
    # same everywhere -- a caveat an agent has to know to ask for is one it does
    # not read, and a run's caveat is the one most likely to change what a reader
    # concludes from its numbers.
    (EntityType.RUN, View.CARD): "_view_card_with_notes",
    (EntityType.RUN, View.NOTES): "_view_run_notes",
    (EntityType.RUN, View.TRAJECTORY): "_view_trajectory",
    (EntityType.RUN, View.METRICS): "_view_metrics",
    (EntityType.RUN, View.ARTIFACTS): "_view_run_artifacts",
    (EntityType.RUN, View.REPRODUCE): "_view_reproduce",
    (EntityType.RUN, View.HANDOFF): "_view_handoff",
    (EntityType.RUN, View.LINEAGE): "_view_run_lineage",
    (EntityType.RUN, View.EVENTS): "_view_events",
    # 0135. The AUTHORED inventory, not `trajectory` narrowed to rollouts: those
    # are the producer's spans and carry no title, description or note, so an
    # agent reading them cannot see that a researcher already wrote down what
    # went wrong on trial 34. A sidecar also outlives the bounded span slice,
    # which is exactly when the span read would have reported the trial absent.
    (EntityType.RUN, View.TRIALS): "_view_run_trials",
    # Phase 6: the run's resolved owner/repo@sha, plus — via
    # view_options={"compare_to": ...} — the diff against another run. See the
    # builder for why the compare rides this view instead of `reproduce`.
    (EntityType.RUN, View.CODE): "_view_run_code",
    (EntityType.EXPERIMENT, View.CARD): "_view_card_with_notes",
    (EntityType.EXPERIMENT, View.NOTES): "_view_experiment_notes",
    (EntityType.EXPERIMENT, View.SUMMARY): "_view_experiment_summary",
    (EntityType.EXPERIMENT, View.ARTIFACTS): "_view_experiment_artifacts",
    # Lineage plan 2 (L12/L18): an experiment's OWN links and its children with
    # their origins -- the same read as a project's (an experiment IS one) --
    # plus, as `run_edges`, the graph AMONG its runs and files this view always
    # returned.
    (EntityType.EXPERIMENT, View.LINEAGE): "_view_project_lineage",
    (EntityType.EXPERIMENT, View.GROUPS): "_view_groups",
    (EntityType.EXPERIMENT, View.VERSIONS): "_view_versions",
    (EntityType.EXPERIMENT, View.REPRODUCE): "_view_experiment_reproduce",
    # Phase 6: what changed in the repo between this experiment's runs. The
    # experiment CARD deliberately stays untouched — the backend experiment
    # read carries no code facts (unlike the project read, whose row already
    # holds `code_sources`), so a card hint here would cost an extra backend
    # call on the cheapest read (the sub-notes N+1 rule); `available_views`
    # on the card already advertises `code`, which is the discovery door.
    (EntityType.EXPERIMENT, View.CODE): "_view_experiment_code",
    (EntityType.PROJECT, View.CARD): "_view_project_card",
    (EntityType.PROJECT, View.NOTES): "_view_project_notes",
    (EntityType.PROJECT, View.SUMMARY): "_view_project_summary",
    # 0134: the attached repositories + the proxied commit timeline. The card
    # carries a bounded `code` block for the same reason it carries notes —
    # a connection an agent has to know to ask for is one it does not see.
    (EntityType.PROJECT, View.CODE): "_view_project_code",
    # A project's only view used to be `card`, so a project-anchored artifact
    # (`probe artifact add --project`, fold #22) was write-only over MCP -- stored
    # and unreadable, which reads as captured and is worse than untracked.
    (EntityType.PROJECT, View.ARTIFACTS): "_view_project_artifacts",
    # 0152: the literature a research project was built from. Its own view
    # rather than a card block, because a review's papers are the CONTENT of
    # the project, not a hint that content exists — and the card's bounded
    # excerpt idiom would truncate exactly the summaries worth reading.
    (EntityType.PROJECT, View.PAPERS): "_view_project_papers",
    (EntityType.PROJECT, View.LINEAGE): "_view_project_lineage",
    (EntityType.GROUP, View.CARD): "_view_card_with_notes",
    (EntityType.GROUP, View.NOTES): "_view_group_notes",
    # One rollout as an entity (0135). NO `notes` view and no notes excerpt on the
    # card, unlike every other entity here: a Trial carries no notes document at
    # all. A rollout ran once and is immutable, so `description` holds what a
    # later reader needs, and a second free-text field beside it is one more place
    # to look. `trajectory` is the read that needs work: see below.
    (EntityType.TRIAL, View.CARD): "_view_card",
    (EntityType.TRIAL, View.TRAJECTORY): "_view_trial_trajectory",
    # Artifacts: the reuse-before-create seam, reached by NAME. This is where the
    # retired `asset:<name>` check went -- #143 folded assets into artifacts, and
    # for one release the instructions still named a route with no builder behind
    # it, so every compliant agent got a 422 and read it as "licence to create a
    # duplicate", inverting the exact guard the instructions exist to enforce.
    # The artifact lineage view reads `GET /v1/artifacts/{id}/lineage` (0255):
    # the run that wrote the file and the runs that read it. Before that route
    # existed this view was deliberately absent -- an empty answer would have
    # read as "this file has no lineage".
    (EntityType.ARTIFACT, View.LINEAGE): "_view_artifact_lineage",
    (EntityType.ARTIFACT, View.CARD): "_view_artifact_card",
    (EntityType.ARTIFACT, View.VERSIONS): "_view_artifact_versions",
    # The TEAM NOTE (research-os 0125). Its `card` IS the
    # document -- a note's identity is its contents, and excerpting here would
    # send an agent that asked for the briefing to a second call to read it. The
    # bounded excerpt lives on `browse_research`, where nobody asked for the
    # document. No `versions` view: the team note keeps no history, by design.
    (EntityType.TEAM_NOTE, View.CARD): "_view_team_note_card",
    # Captured coding-agent sessions. The card is the session's WORK read (what
    # it touched, grouped by entity type) -- a session's identity to a reader is
    # "the session that produced run X", never its megabytes of dialogue. The
    # transcript is served in bounded line sections behind its own view, with
    # `filters.grep` for search WITHIN this one document -- the read
    # search_knowledge cannot express (its transcript corpus ranks chunks
    # across every session, and an exact id can legitimately miss its window).
    (EntityType.SESSION, View.CARD): "_view_card",
    (EntityType.SESSION, View.TRANSCRIPT): "_view_session_transcript",
}
_VIEWS.update({(kind, View.RECORD): "_view_record" for kind, view in _VIEWS if view == View.CARD})

# Filters each (kind, view) accepts, mapped onto the backend's REAL server-side
# filters. Anything else is rejected loudly — a silently-ignored filter returns a
# full result set that the agent believes was narrowed.
#
# Keyed by (kind, view), not view: GET /v1/projects/{id}/artifacts takes no
# filters at all, so `kind` is honest on a RUN's artifacts and a lie on an
# experiment's.
_VIEW_OPTIONS: dict[tuple[str, str], set[str]] = {
    (EntityType.RUN, View.TRAJECTORY): {"span_type", "parent_span_id", "step_from", "step_to"},
    # `span_type` ONLY, and applied AFTER the subtree walk rather than passed to
    # the route. Server-side it would delete intermediate parents and orphan
    # every descendant hanging off them, so a rollout -> turn -> tool_call tree
    # filtered to `tool_call` would come back EMPTY -- a confident wrong answer,
    # from a filter that looks like the run's. `step_from`/`step_to` are absent
    # for the same reason: the window this view reads is chosen from the trial's
    # own step, and a caller-supplied one that excluded it would return nothing.
    (EntityType.TRIAL, View.TRAJECTORY): {"span_type"},
    (EntityType.RUN, View.METRICS): {"key", "kind"},
    (EntityType.RUN, View.ARTIFACTS): {"kind", "step_from", "step_to", "name", "scope"},
    # `requirement` is applied HERE, not server-side: /v1/artifacts/{id}/versions
    # takes no filter, so this is an honest client-side narrowing of a fully-read
    # chain rather than a filter the backend silently ignored.
    (EntityType.ARTIFACT, View.VERSIONS): {"requirement"},
    # `version` pins the reproduce map against a minted experiment_versions manifest.
    # Applied server-side by /v1/projects/{id}/reproduce?version=N — an honest
    # backend filter, not a client-side narrowing.
    (EntityType.EXPERIMENT, View.REPRODUCE): {"version"},
    # `at` is deliberately absent: the SDK accepted it and never read it, and
    # no backend as-of resolution exists. Advertising a parameter that silently
    # does nothing is worse than not having one.
    #
    # Transcript narrowing is CLIENT-SIDE over one complete document the backend
    # already returned whole -- honest in the way the artifact `requirement`
    # filter is honest, not a filter the backend silently ignored. `grep` is
    # literal and case-insensitive (a regex would answer confidently and wrongly
    # on the first bracket in a code-heavy transcript). The recording agent is
    # NOT a filter here: `session:<agent>/<id>` already names it on the ref, so a
    # `source` filter would only add a way to contradict the ref and have one
    # side win silently.
    (EntityType.SESSION, View.TRANSCRIPT): {"grep", "context_lines", "start_line"},
    # The filters `_view_project_code` has always read and documented. This
    # entry was MISSING, so `_checked_view_options` rejected every one of them with
    # "accepts no view options" while the view's own docstring advertised them —
    # the dead-switch failure the "vocabulary spans the wire" rule warns
    # about, fixed alongside phase 6's two new (kind, CODE) pairs.
    (EntityType.PROJECT, View.CODE): {
        "commit",
        "source",
        "cursor",
        "author",
        "path",
        "include_excluded",
    },
    # `compare_to` names the other run (`run:<uuid-or-slug>`, prefix optional)
    # and is resolved server-side by GET /v1/runs/{ref}/code/compare — an
    # honest backend parameter, not a client-side narrowing.
    (EntityType.RUN, View.CODE): {"compare_to"},
    # `depth` (1-5) adds the upstream walk, resolved server-side by
    # GET /v1/runs/{ref}/upstream?depth=N (0255) -- an honest backend parameter.
    (EntityType.RUN, View.LINEAGE): {"depth"},
}
_VIEW_OPTIONS.update(
    {(kind, View.RECORD): {"field"} for kind, view in _VIEWS if view == View.RECORD}
)


def _compact(envelope: dict) -> dict:
    """Strip envelope bookkeeping an agent does not reason over.

    The reader is a model, not code, so ABSENCE IS THE CONTRACT: a key appears
    only when it says something (see `continuation.omit_defaults`, which the
    delivery layer applies again to what it builds). What is KEPT and why is
    the interesting half -- a drop-list without one rots into dropping
    something load-bearing:

    - `completeness` survives whenever it is not complete-with-nothing-missing.
      It is the only field that says what the response could not cover, and
      stripping a partial one would turn it into a confident answer. A complete
      one used to ride every call -- every ROW of an `entity` batch -- saying
      "nothing to see here" ahead of the content.
    - `next_cursor` survives when there is a next page. It used to be emitted
      null too, so code doing `page["next_cursor"]` would not KeyError on the
      last page; no code reads this wire (the daemon's reader is a model too,
      and `scripts/mcp_budget_bench.py` uses `.get`), and for a model "absent"
      and "null" are the same instruction: stop.
    - `capabilities` goes. `source.capabilities()` is STATIC for the hosted
      backend, so the map is constant per release like `scope`/`as_of`/
      `schema_version` -- and its one False flag (`portable_snapshots`, "not
      yet") rode every read of every entity. A capability that fails at call
      time says so where the caller can act: a `completeness.missing` marker
      (`web_search`, `semantic_search`, ...) on that response. `verbose=True`
      still returns the map.
    - `scope`, `as_of`, `schema_version` go. They are constant per token and per
      release; re-sending them on every call costs context and tells the agent
      nothing it can act on.
    - `evidence` goes when empty, stays when populated.
    """
    return omit_defaults(
        {
            "data": envelope["data"],
            "completeness": envelope["completeness"],
            "next_cursor": envelope.get("next_cursor"),
            "evidence": envelope.get("evidence"),
        }
    )


def _echoes_project_scope(response: Any, project_id: str) -> bool:
    """Did the backend confirm it applied `project_id`?

    A server that supports the scope echoes it (research-os #103 returns it on
    the request echo); one that predates it accepts the unknown body field,
    ignores it, and answers tenant-wide. Absence of the echo is the only signal
    available, so absence is treated as unsupported -- the failure that matters
    is the silent one, and a false refusal is loud and correctable.
    """
    if not isinstance(response, dict):
        return False
    # Absence is treated as UNSUPPORTED, not as assent. The failure that matters
    # is the silent one -- tenant-wide results wearing state="complete" -- and a
    # false refusal is loud, immediate and correctable.
    return str(response.get("project_id") or "") == str(project_id)


def _satisfies(version: dict, requirement: str) -> bool:
    """Does this artifact version satisfy `requirement`?

    Artifact versions are MONOTONIC INTEGERS with optional labels, not semver --
    so this supports exactly what the data supports: an exact label/version
    match, or `>=N` / `>N` / `<=N` / `<N` against the integer. Pretending to
    understand semver ranges over integer versions would answer confidently and
    wrongly, which is the failure mode this whole view exists to prevent.
    """
    raw = str(version.get("version", ""))
    label = version.get("label")
    requirement = requirement.strip()
    # Order matters: ">=" must be tested before ">", and "==" before "=".
    for op in (">=", "<=", "==", ">", "<", "="):
        if requirement.startswith(op):
            operand = requirement[len(op) :].strip()
            try:
                have, want = int(raw), int(operand)
            except (TypeError, ValueError):
                # A malformed operand must NOT quietly answer "no version
                # satisfies this". That is a THIRD kind of nothing, and it is
                # indistinguishable from a real version ceiling: the caller sees
                # state="no_match" with completeness="complete", believes the
                # artifact is too old, and registers a duplicate -- the exact
                # outcome this view exists to prevent. ">=2.0" is the obvious
                # way to write this and it is not a version here.
                raise errors.ValidationError(
                    f"artifact versions are monotonic integers, not semver: "
                    f"{requirement!r} does not name one (try '>=2', '<3', "
                    f"'==1', or a bare label)",
                    status=422,
                ) from None
            return {
                ">=": have >= want,
                "<=": have <= want,
                "==": have == want,
                "=": have == want,
                ">": have > want,
                "<": have < want,
            }[op]
    # Bare value: exact match on version or label.
    return requirement == raw or requirement == label


def _supported_views(kind: str) -> list[str]:
    return sorted(str(view) for entity_kind, view in _VIEWS if entity_kind == kind)


def _views_offered(kind: str) -> str:
    """The kind's views, one per line, each with what it returns.

    FOR THE ERROR PATH ONLY. `available_views` on a response stays a bare list:
    it rides every card and every browse node, where a gloss per view would be
    paid for by every caller that already knew which view it wanted. Here the
    caller has just proved it did not know, the message is read once with full
    attention, and nothing is spent on the callers who got it right.

    A view with no line in VIEW_PURPOSE still appears, bare. The list must stay
    COMPLETE -- a missing gloss hiding a real view would turn this message into
    a smaller lie than the one it replaced.
    """
    lines = []
    for name in _supported_views(kind):
        purpose = VIEW_PURPOSE.get(View(name))
        lines.append(f"  {name:<11}{purpose}" if purpose else f"  {name}")
    return "\n".join(lines)


def _annotate(node: dict, kind: str, *, api_base_url: str | None = None) -> dict:
    """Tag a browse node with its kind, slug, uuid, and dashboard URL.

    TWO ADDRESSES, BOTH LABELLED, AND NO FIELD CALLED `ref`.

    This used to emit one `ref` key holding `kind:<uuid>`. That was a field named
    "reference" whose value was always the id, which taught every agent to copy
    the uuid around -- so the readable handle sat unused in the same object while
    the unreadable one got pasted into tickets and chat.

    `slug` is now the handle to prefer and `uuid` the stable key, each named for
    what it actually holds. `get_entity(ref=...)` takes either, so nothing is
    lost by preferring the readable one. The `kind:` prefix stays on BOTH: it is
    what tells the server which table to look in, and dropping it would make
    `get_entity` guess.

    `slug` is omitted, not null, when a node has none -- a pre-0012 run, say.
    An absent key says "there is no readable handle here"; a null one invites a
    caller to paste the string "None".

    `url` is the ONLY reason an agent can hand a researcher something
    clickable: a uuid is unguessable, so a link that is not in the payload is a
    link the model has to invent, and an invented one 404s with the same
    confidence as a real one. Omitted entirely when the dashboard origin is
    unknown (see sdk.links) -- an absent key says "say nothing", which is what
    a caller with no link must do.

    THE NODE IS TOKENS AN AGENT PAYS FOR, so three things a node used to carry
    per row are gone from it:

    - The backend's bare `id` -- byte-identical to the tail of `uuid`, so every
      row spent ~30 tokens carrying the same address twice unlabelled. `uuid`
      and `slug` are the two documented addresses; the bare spelling taught
      callers to paste the one field this function exists to deprecate.
    - `available_views` -- identical for every node of a kind, so a 22-project
      browse repeated the same four strings 22 times. It now rides ONCE on the
      browse envelope, keyed by kind (see `browse_research`), still derived
      from `_VIEWS` and never hand-written.
    - Null-valued keys -- same rule the docstring above already states for
      `slug`: an absent key says "nothing here", a null one invites a caller to
      paste the string "None". `experiments: null` ("not expanded") stays
      distinguishable from `[]` ("expanded, empty") as absence vs presence.
    """
    url = links.entity_url(kind, node.get("id"), api_base_url=api_base_url)
    # Every kind now spells its handle `slug` -- runs stopped saying `short_id`
    # at 0109. This used to reconcile the two names.
    slug = node.get("slug")
    return {
        **{k: v for k, v in node.items() if v is not None and k != "id"},
        "entity_type": str(kind),
        **({"slug": f"{kind}:{slug}"} if slug else {}),
        "uuid": f"{kind}:{node.get('id')}",
        **({"url": url} if url else {}),
    }


#: How many peer slugs the project CARD lists per direction. The card is an
#: orientation read, so it names a few and states the count; `view="card"` is
#: not where a 200-edge graph gets enumerated.
_CARD_REFERENCE_SLUGS = 10


class ResearchReadService:
    """Compact, provenance-bearing read model exposed through MCP."""

    def __init__(self, source: ResearchOSSource):
        self.source = source

    @property
    def _api_base_url(self) -> str | None:
        """API origin this service actually calls, for deriving dashboard links.

        Read off the live client rather than re-resolving config: the server
        builds one source per token with an explicit base URL, and a second
        resolution could name a different host than the one being read from --
        which would mint links into the wrong deployment.
        """
        client = getattr(self.source, "client", None)
        settings = getattr(client, "settings", None)
        return getattr(settings, "base_url", None)

    def _envelope(
        self,
        data: Any,
        *,
        evidence: list[dict] | None = None,
        state: str = EnvelopeState.COMPLETE,
        missing: list[str] | None = None,
        next_cursor: str | None = None,
        verbose: bool = False,
    ) -> dict:
        """The MCP wire shape. COMPACT BY DEFAULT.

        This default used to be True, and the result was that a tool got the
        lean envelope only if it remembered to ask: `search_knowledge` and
        `get_entity` passed `verbose=False`, and the other five tools --
        `browse_research`, `read_metrics` and the three metric aliases -- shipped
        `schema_version`, `as_of`, `scope` and all seven capability flags (six of
        them True) in front of their answer on EVERY call. None of that is readable by the
        agent as anything it can act on, and it is ~350 characters ahead of the
        first byte of data, which is what a person watching the tool scroll past
        actually sees.

        Opt-OUT is the right polarity because the compact shape is the contract
        (`_compact` keeps every field that carries signal); verbose is the
        debugging affordance. A new tool added here is then quiet by default
        instead of noisy until someone notices.
        """
        identity = self.source.identity()
        envelope = {
            "schema_version": "1.0",
            "as_of": _now(),
            "scope": {
                "customer_id": identity.get("customer_id"),
                "researcher": identity.get("email") or identity.get("user_id"),
            },
            "capabilities": self.source.capabilities(),
            "data": data,
            "evidence": evidence or [],
            "completeness": {"state": state, "missing": missing or []},
            "next_cursor": next_cursor,
        }
        return envelope if verbose else _compact(envelope)

    def research_context(
        self,
        task: str,
        project_ref: str | None = None,
        session_id: str | None = None,
        token_budget: int = 1800,
    ) -> dict:
        projects = self.source.projects(limit=50)
        project = None
        if project_ref:
            needle = project_ref.lower()
            project = next(
                (
                    item
                    for item in projects
                    if needle
                    in {str(item.get("id", "")).lower(), str(item.get("slug", "")).lower()}
                ),
                None,
            )
        elif len(projects) == 1:
            project = projects[0]
        experiments = self.source.experiments(
            project_id=str(project["id"]) if project else None, limit=30
        )
        terms = set(task.lower().split())
        relevant = sorted(
            experiments,
            key=lambda item: len(terms.intersection(_text(item).split())),
            reverse=True,
        )[:5]
        active_runs: list[dict] = []
        for experiment in relevant[:3]:
            active_runs.extend(
                run
                for run in self.source.runs(experiment_id=str(experiment["id"]), limit=10)
                if run.get("status") in {"created", "running"}
            )
        if project is not None:
            # PROJECT-DIRECT runs (research-os 0054) belong to no experiment, so
            # the sweep above can never see them. direct=True filters server-side
            # (so ten attached runs can't mask an active direct one); the
            # client-side experiment_id filter stays as belt-and-braces, and the
            # SDK's project_id guard raises on a pre-0054 backend that would
            # have returned unscoped rows — degrade to the experiment sweep.
            try:
                direct_runs = self.source.runs(project_id=str(project["id"]), direct=True, limit=10)
            except errors.NotFoundError:
                direct_runs = []
            active_runs.extend(
                run
                for run in direct_runs
                if run.get("status") in {"created", "running"} and not run.get("experiment_id")
            )
        # The separate asset registry is retired: a reusable asset IS an artifact
        # now, so there is no second inventory to fetch and nothing here can be
        # missing on its account.
        missing: list[str] = []

        fixed: dict[str, Any] = {
            "task": task,
            "session_id": session_id,
            "project": project,
            "warnings": [],
        }
        # `missing` is what THIS response lacks, NOT an inventory of everything the
        # backend cannot do. Deriving it from every False capability is what pinned
        # every context envelope to partial forever: portable_snapshots is honestly
        # and permanently False, so `missing` could never be empty and stopped
        # carrying information. Only versioned_assets gates content returned here.
        sections, truncated = _fit_sections(
            [
                ("relevant_experiments", relevant),
                ("active_runs", active_runs[:10]),
                ("projects", [] if project is not None else projects),
            ],
            max(0, token_budget - _tokens(fixed)),
        )
        if truncated:
            missing.append(MissingMarker.TRUNCATED_BY_TOKEN_BUDGET)
        if project is not None:
            sections["projects"] = None
        return self._envelope(
            {**fixed, **sections},
            state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
            missing=missing,
        )

    def browse_research(
        self,
        scope: str | None = None,
        depth: int = 1,
        status: str | None = None,
        tags: list[str] | None = None,
        workspace_id: str | None = None,
        limit: int = 50,
        cursor: str | None = None,
        runs_cursor: str | None = None,
        subprojects_cursor: str | None = None,
    ) -> dict:
        """The structured tree: what EXISTS, as opposed to what MATCHES a query.

        Every node -- nested children included -- carries the two labelled
        addresses the other read tools consume (slug/uuid); `available_views`
        rides ONCE on the envelope, keyed by kind, so an agent orienting here
        already knows what it can ask for next without discovering it by
        failed call.
        """
        # A caller that opted in (`X-Probe-Hide-Session-Work`, the daemon's
        # reader) does not see the work its own session created; see
        # search_knowledge. None for everyone else: the same request as ever.
        hide_session = accounting.session_work_to_hide()
        try:
            payload = self.source.browse(
                scope=scope,
                depth=depth,
                status=status,
                tags=tags,
                workspace_id=workspace_id,
                limit=limit,
                cursor=cursor,
                runs_cursor=runs_cursor,
                subprojects_cursor=subprojects_cursor,
                continuation_handles=True,
                exclude_origin_session=hide_session,
            )
        except errors.CapabilityUnavailable:
            # NOT an empty tree: "nothing exists" and "this server cannot tell
            # you what exists" are opposite claims, and returning the first
            # would stop an agent looking any further.
            return self._envelope(
                {"scope": scope, "projects": None, "experiments": None, "runs": None},
                state=EnvelopeState.PARTIAL,
                missing=[MissingMarker.STRUCTURED_BROWSE],
            )
        data: dict[str, Any] = {"scope": scope, "depth": payload.get("depth", depth)}
        # ONCE per kind, not once per node: every node of a kind advertises the
        # same views, and a 22-project browse used to repeat the same four
        # strings 22 times. Still derived from `_VIEWS` (via _supported_views),
        # never hand-written, so it cannot drift from what get_entity accepts.
        views: dict[str, list[str]] = {}

        def _tag(node: dict, kind: EntityType) -> dict:
            # Nested children are annotated the same as top-level nodes -- a
            # depth-2 response must not mix labelled addresses at one level
            # with bare backend ids at the next, or the "no bare id" contract
            # teaches agents to paste an unprefixed id into get_entity.
            if kind is EntityType.PROJECT and isinstance(node.get("experiments"), list):
                node = {
                    **node,
                    "experiments": [
                        _tag(child, EntityType.EXPERIMENT) for child in node["experiments"]
                    ],
                }
            if kind is EntityType.EXPERIMENT and isinstance(node.get("runs"), list):
                node = {
                    **node,
                    "runs": [_tag(child, EntityType.RUN) for child in node["runs"]],
                }
            views.setdefault(str(kind), _supported_views(kind))
            return _annotate(node, kind, api_base_url=self._api_base_url)

        for level, kind in (
            ("projects", EntityType.PROJECT),
            # 0148: a project scope's DIRECT children — same node kind as the
            # top level. Listed here or the projection would drop the level
            # silently (the exact trap the explicit list exists to avoid).
            ("subprojects", EntityType.PROJECT),
            ("experiments", EntityType.EXPERIMENT),
            ("runs", EntityType.RUN),
        ):
            nodes = payload.get(level)
            data[level] = None if nodes is None else [_tag(n, kind) for n in nodes]
            if nodes is not None:
                # An expanded-but-empty level still advertises its views:
                # [] means "nothing here yet", not "this kind has no reads".
                views.setdefault(str(kind), _supported_views(kind))
        if views:
            data["available_views"] = views
        # 0148: PER-LEVEL continuation tokens. Passed through verbatim — the
        # REST contract owns their meaning; `cursor`/`next_cursor` still carry
        # the primary level's for callers that predate the split.
        if payload.get("cursors"):
            data["cursors"] = payload["cursors"]
        missing: list[str] = []
        if payload.get("truncated"):
            # The tree was cut, so an absent child is not evidence of absence.
            missing.append(MissingMarker.TRUNCATED_BY_TOKEN_BUDGET)
        if hide_session is not None and payload.get("origin_exclusion_applied") is not True:
            # Asked and not echoed: the server ignored the filter, and the
            # session's own projects and runs are in this tree.
            missing.append(MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED)
        if scope is None and cursor is None:
            # Runs opened with no project (daemon v2) sit under no node of the
            # tree, so the lab's first page names them. Absent = none; a backend
            # that cannot say is a marker, never an empty list.
            unfiled = self._unfiled_nodes(hide_session)
            if unfiled is None:
                missing.append(MissingMarker.UNFILED_RUNS)
            elif unfiled:
                data["unfiled"] = unfiled
                views.setdefault(str(EntityType.RUN), _supported_views(EntityType.RUN))
                data["available_views"] = views
        envelope = self._envelope(
            data,
            state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
            missing=missing,
            next_cursor=payload.get("cursor"),
        )
        # Private transport between the source adapter and browse delivery.
        # The final MCP adapter consumes and strips these before serialization.
        if "continuation_handles" in payload:
            envelope["_browse_handles"] = payload["continuation_handles"]
        return envelope

    #: Floating runs one browse names at most; `probe run list --unfiled` has the rest.
    _UNFILED_BROWSE_LIMIT = 10

    def _session_created_ids(self, session_id: str) -> tuple[frozenset[str], bool] | None:
        """`(ids, truncated)` of every project, experiment and run `session_id`
        created (`GET /v1/sessions/{id}/created`, research-os 0291), lower-cased;
        None when the backend cannot say (it predates the route, or the read
        failed) -- which a caller must report, never read as "nothing"."""
        try:
            answer = self.source.session_created(session_id)
        except Exception:  # noqa: BLE001 -- reported by the caller as unsupported
            return None
        if not isinstance(answer, dict):
            return None
        ids = [*(answer.get("project_ids") or []), *(answer.get("run_ids") or [])]
        return frozenset(str(i).lower() for i in ids), bool(answer.get("truncated"))

    def _without_session_work(
        self, result: _ViewData, session_id: str, *, own_id: str | None
    ) -> _ViewData:
        """`result` with every row, edge and origin naming work `session_id`
        created taken out -- except the entity the caller asked for by address.
        Marked `session_work_exclusion_unsupported` when the created set could
        not be read, or was cut at its cap: the view may still hold that work."""
        created = self._session_created_ids(session_id)
        if created is None:
            return dataclass_replace(
                result,
                missing=[*result.missing, MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED],
            )
        ids, truncated = created
        # Opened BY ADDRESS, the session's own work -- one of its runs, or a file
        # or trial of one -- is shown whole: the caller named it (the reader takes
        # such refs from the session it reads beside), and scrubbing its own run
        # out of its rows would empty the view with nothing saying so.
        own = {own_id.lower()} if own_id else set()
        if isinstance(result.payload, dict):
            own |= {str(result.payload[k]).lower() for k in ("run_id", "project_id") if result.payload.get(k)}
        if own & ids:
            return result
        hidden = ids
        return dataclass_replace(
            result,
            payload=_scrub_session_work(result.payload, hidden),
            rows=None if result.rows is None else _scrub_session_work(result.rows, hidden),
            missing=(
                [*result.missing, MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED]
                if truncated
                else result.missing
            ),
        )

    def _unfiled_nodes(self, hide_session: str | None = None) -> list[dict] | None:
        """The caller's floating runs as browse nodes (id, name, created_at, tags),
        [] when there are none, None when the backend cannot say.

        `hide_session` leaves out the floating runs THAT session created -- the
        daemon writer opens its runs unfiled, so they are exactly what its
        reader must not be shown. Filtered SERVER-side, inside the page (so the
        session's own cannot empty it), then checked against the session's
        created set; a backend that cannot give that set cannot be trusted to
        have filtered either, so the list is withheld and marked."""
        limit = self._UNFILED_BROWSE_LIMIT
        try:
            rows = self.source.unfiled_runs(limit=limit, exclude_origin_session=hide_session)
        except Exception:  # noqa: BLE001 -- an additive list never breaks the tree
            return None
        if hide_session is not None:
            created = self._session_created_ids(hide_session)
            if created is None:
                return None
            rows = [
                row
                for row in rows
                if not (isinstance(row, dict) and str(row.get("id") or "").lower() in created[0])
            ]
        return [
            _annotate(
                {
                    "id": row.get("id"),
                    "slug": row.get("slug"),
                    "name": row.get("name"),
                    "status": row.get("status"),
                    "created_at": row.get("created_at"),
                    "tags": row.get("tags") or None,
                },
                EntityType.RUN,
                api_base_url=self._api_base_url,
            )
            for row in rows
            if isinstance(row, dict) and row.get("id")
        ]

    def query_sql(
        self,
        sql: str | None = None,
        tables: list[str] | None = None,
        token_budget: int = 2000,
    ) -> dict:
        """Read-only SQL, passed straight through: the server already bounds it.

        ``max_rows`` is DERIVED from the delivery budget rather than exposed, so
        the database is not asked for 200 rows the response can only carry 20 of.
        ~20 tokens per row is a deliberate over-estimate of a narrow row; the
        delivery branch in ``continuation`` still trims whatever does not fit.
        """
        max_rows = None if sql is None else max(1, min(MAX_ROWS_CEILING, token_budget // 20))
        return self.source.query_sql(sql=sql, tables=tables, max_rows=max_rows)

    # -- research literature -------------------------------------------------
    # Paper text is externally authored evidence. Keep that provenance on each
    # response, retain the backend's filtering and validation, and bound the
    # combined prose before delivery applies its token budget.

    #: Stamped on every open-web payload. Names WHERE the text came from rather
    #: than asserting it is dangerous: "open-web" is a fact about provenance the
    #: agent can reason with, where "untrusted: true" is a verdict that invites
    #: arguing with it.
    _OPEN_WEB = "open-web"

    #: 5xx statuses that mean "the web door did not answer" rather than "your
    #: request was wrong". `app/websearch/router.py` maps every provider failure
    #: onto exactly these: 503 unconfigured OR over quota, 502 the provider
    #: refused our key or failed, 504 a transport timeout. A 400 is NOT here --
    #: that is a query Firecrawl refused, the caller can fix it, and it raises.
    #:
    #: EQUAL TO `transport._RETRYABLE` BY COINCIDENCE, not by construction: that
    #: set is "worth trying again", this one is "the door did not answer", and
    #: they happen to coincide because the router maps every provider failure
    #: onto the gateway statuses. Do not couple them.
    _WEB_DOOR_DOWN = frozenset({502, 503, 504})

    #: Ceiling on the literature text one tool result may carry, matching the
    #: assistant's `MAX_TOOL_RESULT_CHARS`. The backend caps each passage and
    #: the number of results; MCP also bounds their combined prose before
    #: token-based delivery.
    _WEB_MAX_TEXT_CHARS = 100_000

    #: Ceiling on the backend sentence relayed as `data.reason`. `str(exc)` is
    #: the SDK's detail, and `Transport._to_error` falls back to the WHOLE
    #: `resp.text` when a 5xx body is not JSON -- so an ingress or CDN error
    #: page during a rollout would otherwise put its entire HTML (server banner,
    #: upstream name, request id) into a customer agent's context. Measured: a
    #: plain nginx 503 page is ~2,900 characters of nothing an agent can act on.
    _WEB_REASON_CHARS = 300

    def _web_door_down(self, exc: errors.RosError) -> bool:
        """Whether the literature provider failed to answer.

        A 404 from the paper search endpoint means the route is unavailable.
        Transport failures can lack an HTTP status and still need the partial
        envelope, rather than looking like a successful empty search.
        """
        return (
            isinstance(exc, errors.TransportError)
            or exc.status == 404
            or exc.status in self._WEB_DOOR_DOWN
        )

    def _web_unavailable(self, exc: errors.RosError) -> dict:
        """The envelope for a web door that did not answer.

        NO `results` KEY, and that omission is the point. An outage that
        returned `results: []` is byte-identical to "the provider found
        nothing", and those are opposite facts: one says try again or tell the
        researcher the door is shut, the other says this line of enquiry is
        empty. `state="no_match"` is reserved for the second. Here the shape
        itself refuses to be mistaken for an answer, and `reason` carries the
        backend's own sentence -- which is the only thing that separates "no
        Firecrawl key on this deployment" from "over quota, try later".
        """
        reason = str(exc).strip()
        if len(reason) > self._WEB_REASON_CHARS:
            reason = reason[: self._WEB_REASON_CHARS] + "..."
        return self._envelope(
            {"provenance": self._OPEN_WEB, "reason": reason},
            state=EnvelopeState.PARTIAL,
            missing=[MissingMarker.WEB_SEARCH],
        )

    @staticmethod
    def _rows(payload: dict, key: str) -> list[dict]:
        """The dict rows under `key`, and nothing else.

        The payload is open-web: a provider (or a page) can put anything in
        here, and the callers immediately do `row.get(...)` on every element --
        which is an AttributeError on a bare string.
        """
        rows = payload.get(key)
        return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []

    @classmethod
    def _web_state(cls, payload: dict) -> EnvelopeState:
        """What `completeness.state` a well-formed provider answer earns.

        THREE OUTCOMES, NOT TWO. `ok` is complete and `empty` is NO_MATCH --
        the provider ran the query and matched nothing, which is an ANSWER, and
        a model told merely that its call was incomplete rephrases and retries
        for as many steps as it has left.

        ANYTHING ELSE IS PARTIAL. A missing `state`, a malformed body, or a
        value some future backend adds must NOT read as "searched fine, found
        nothing": that is a wrong answer wearing the shape of a right one, and
        a malformed response must remain distinguishable from a clean empty
        search.

        Annotated `-> EnvelopeState` and compared with `==` by callers, not
        `is`: the members are `str` at runtime, so an identity check works only
        while the exact member objects are returned, and honouring a `-> str`
        annotation by returning `.value` would silently stop every truncation
        rollup from firing.
        """
        state = payload.get("state")
        if state == WebState.OK:
            return EnvelopeState.COMPLETE
        if state == WebState.EMPTY:
            return EnvelopeState.NO_MATCH
        return EnvelopeState.PARTIAL

    #: The prose-bearing fields in a literature response.
    #: `PaperPassage` calls it `text`; `Paper` calls it
    #: `abstract`. Budgeting only `text` made the ceiling a NO-OP on
    #: `find_papers`, whose 50-abstract ceiling is the likeliest way to blow it.
    _WEB_TEXT_FIELDS = ("text", "abstract")

    @classmethod
    def _capped(cls, rows: list[dict]) -> tuple[list[dict], bool]:
        """Trim open-web prose across rows to `_WEB_MAX_TEXT_CHARS`.

        Per-ROW truncation is the backend's and is already done; this is the
        per-RESPONSE ceiling it cannot apply, because only this layer knows the
        rows are about to be concatenated into one agent's context.

        Rows are KEPT and their prose shortened rather than rows being dropped:
        which pages or papers matched is the answer, and losing the tail of one
        body costs less than losing a result the agent never learns existed.

        A row cut HERE is marked `truncated`, deliberately not the backend's
        `text_truncated`: that field means "the deployment's per-page ceiling
        cut this page" and is documented in CONTRACT.md as such. Two different
        cuts by two different layers earn two different flags, or a reader
        cannot tell which ceiling they hit.
        """
        budget = cls._WEB_MAX_TEXT_CHARS
        trimmed: list[dict] = []
        cut = False
        for row in rows:
            field = next(
                (f for f in cls._WEB_TEXT_FIELDS if isinstance(row.get(f), str) and row[f]),
                None,
            )
            if field is None:
                trimmed.append(row)
                continue
            body = row[field]
            if len(body) <= budget:
                budget -= len(body)
                trimmed.append(row)
                continue
            trimmed.append({**row, field: body[:budget], "truncated": True})
            budget = 0
            cut = True
        return trimmed, cut

    @classmethod
    def _resolve_state(cls, payload: dict, missing: list[str] | None) -> EnvelopeState:
        """The provider's own outcome, downgraded to PARTIAL if we trimmed.

        NO_MATCH outranks truncation: "the provider
        matched nothing" is a complete answer to the question asked, and there
        is nothing for a truncation marker to be partial ABOUT.
        """
        state = cls._web_state(payload)
        if missing and state == EnvelopeState.COMPLETE:
            return EnvelopeState.PARTIAL
        return state

    def find_papers(
        self,
        mode: str,
        query: str | None = None,
        paper_id: str | None = None,
        limit: int | None = None,
        authors: str | None = None,
        categories: str | None = None,
        published_from: str | None = None,
        published_to: str | None = None,
        expand: str | None = None,
    ) -> dict:
        """The research literature: search abstracts, read one, or expand.

        Per-mode argument validation is the BACKEND's, deliberately. It refuses
        what the chosen mode cannot read instead of ignoring it, and a second
        copy of that table here would drift from the one that decides.

        NO TRUNCATION SIGNAL, and that is a backend gap rather than an omission
        here: `app/websearch/service.py` clips each passage to
        `firecrawl_max_page_chars` and DISCARDS the flag (`text, _ = _clip(...)`),
        and `PaperPassage` carries no `truncated` field, so there is nothing for
        this layer to read. A clipped passage therefore reports `complete`. Say
        so in the tool docstring until the backend surfaces the flag.
        """
        try:
            payload = self.source.find_papers(
                mode=mode,
                query=query,
                paper_id=paper_id,
                limit=limit,
                authors=authors,
                categories=categories,
                published_from=published_from,
                published_to=published_to,
                expand=expand,
            )
        except errors.RosError as exc:
            if self._web_door_down(exc):
                return self._web_unavailable(exc)
            raise
        if not isinstance(payload, dict):
            payload = {}

        results, over_budget = self._capped(self._rows(payload, "results"))
        data: dict[str, Any] = {
            "provenance": self._OPEN_WEB,
            "mode": payload.get("mode", mode),
            "results": results,
        }
        passages, passages_over = self._capped(self._rows(payload, "passages"))
        if passages:
            data["passages"] = passages
        missing = (
            [MissingMarker.TRUNCATED_BY_RESPONSE_BUDGET] if over_budget or passages_over else None
        )
        return self._envelope(data, state=self._resolve_state(payload, missing), missing=missing)

    def search_knowledge(
        self,
        query: str,
        search_in: list[str] | None = None,
        project_id: str | None = None,
        workspace_id: str | None = None,
        top_k: int = 8,
        collapse: str | None = "experiment",
        verbose: bool = False,
        cursor: str | None = None,
        exclude_session: str | None = None,
        curated_only: bool = False,
        token_budget: int = 2000,
    ) -> dict:
        """Ranked retrieval across the lab.

        `verbose` follows `_envelope`: compact unless asked. It used to default
        True here to keep a straight-through deprecation ALIAS returning the old
        envelope -- but the search aliases are gone, and the three that remain
        are metric ones that delegate to `_read_metrics`, so nothing calls this
        method except the tool surface (which always passed verbose=False) and
        tests (which pass it explicitly). A default that contradicts
        `_envelope`'s is a trap for the next tool added here.

        Scopes are TYPED parameters, not an untyped `filters` dict. The dict
        accepted exactly one documented key while looking like it accepted many,
        and a per-key cost (project scope used to disable semantic retrieval)
        cannot be documented on a `dict[str, Any]`.

        `search_in` was called `corpora` until the rename. That old name is a
        TOOL-SURFACE concern and its rejection lives in server.py, not here: this
        is the internal API, so a Python caller passing `corpora=` gets a
        TypeError, which is already loud.
        """
        # The tool surface types this as CollapseMode so the vocabulary ships in
        # the schema; this check is what protects DIRECT Python callers, for whom
        # nothing validates. Both spellings compare equal -- StrEnum is a str.
        if collapse is not None and collapse != CollapseMode.EXPERIMENT:
            raise errors.ValidationError(
                f'unknown collapse value {collapse!r}: pass "experiment" or null',
                status=422,
            )
        corpus, unsupported = _map_search_in(search_in)
        exact_cursor, semantic_cursor = _split_cursor(cursor)
        # `top_k` is a TOTAL, and asking each channel for all of it is what makes
        # it one. Splitting the budget per channel meant `top_k=8` fetched four
        # semantic rows and four exact ones -- and the exact channel returns
        # nothing on most searches, so a default search showed four results and
        # called it eight.
        #
        # The cost is that rows can now be left over after the merge, which the
        # per-channel cursors cannot describe: they advance by what was FETCHED.
        # So a response that leaves anything over returns no cursor at all and
        # says `results_beyond_budget` instead. A cursor that skips rows the
        # caller never saw is worse than an honest "there is more".
        per_channel = max(1, min(top_k, _BACKEND_CHANNEL_CAP))
        # NO keyword fallback, and nothing to catch. It existed for backends
        # predating POST /v1/search, which the MCP cannot reach: it only ever
        # talks to the hosted backend (see source.capabilities()). Keeping it
        # meant a scoped 404 had to be attributed WITHOUT asking the server —
        # and blaming the scope is right on the live backend, where an unknown
        # project really does 404, but it made the fallback unreachable for
        # every scoped call and left a workspace guard that could not fire.
        # Half a fallback is worse than none: it reads as a safety net while
        # covering only unscoped calls. A genuinely absent route now surfaces
        # as CapabilityUnavailable — a truthful failure rather than a
        # silently-empty keyword answer.
        # WHO IS CALLING, for self-exclusion. Two sources, and the explicit one
        # wins (D5).
        #
        # The HEADER is ambient: `X-Probe-Agent-Session` costs the agent nothing
        # and cannot be forgotten, so it is the right default. It is also absent
        # for most callers today -- Codex connects its MCP before a thread id
        # exists, and 3,282 of 3,304 hosted calls over 30 days carried no agent
        # label at all.
        #
        # The PARAMETER covers exactly that gap: a Codex agent's own shell DOES
        # see CODEX_THREAD_ID, so it can pass what its transport cannot. An
        # explicit value overrides the header rather than merging with it: a
        # caller that names a session has said something specific, and silently
        # preferring an ambient value would ignore it.
        ambient = accounting.calling_agent_session()
        exclude_agent_session = exclude_session or (ambient[1] if ambient else None)
        # The session's own WORK, not just its conversation: only for a caller
        # that opted in with `X-Probe-Hide-Session-Work` (the daemon's reader),
        # and always its AMBIENT session -- never `exclude_session`, which the
        # model supplies. Everyone else sends exactly the request they always sent.
        exclude_origin_session = accounting.session_work_to_hide()
        response = self.source.search(
            query,
            corpus=corpus,
            workspace_id=workspace_id,
            project_id=project_id,
            top_k=per_channel,
            exact_limit=per_channel,
            exact_cursor=exact_cursor,
            semantic_cursor=semantic_cursor,
            exclude_agent_session=exclude_agent_session,
            # None rather than False keeps the request body identical to an
            # older client's when nobody asked for curation.
            curated_only=True if curated_only else None,
            exclude_origin_session=exclude_origin_session,
        )
        exact = _section(response, Channel.EXACT)
        semantic = _section(response, Channel.SEMANTIC)
        scoped_server_side = project_id is None or _echoes_project_scope(response, project_id)
        if not scoped_server_side:
            # The backend did not confirm it applied the scope. SearchRequest
            # does not forbid extra body fields, so a server predating
            # server-side project scope accepts `project_id`, ignores it, and
            # returns TENANT-WIDE results -- a confident wrong answer with no
            # marker on it, which is worse than any error.
            #
            # Degrade rather than refuse. Refusing would be honest but would
            # also remove a capability that works today; filtering client-side
            # is equally honest and still useful. The exact channel carries
            # project_id per row so it can be narrowed here; the semantic
            # channel cannot be, so it is EMPTIED and marked rather than passed
            # through unscoped. A caller gets fewer results and is told why.
            exact["results"] = [row for row in exact["results"] if _in_project(row, project_id)]
            semantic = {
                "results": [],
                "cursor": None,
                "error": ChannelError.PROJECT_SCOPE_UNSUPPORTED,
                "total_candidates": None,
                "active_runs_count": None,
            }
        # Project scope is applied SERVER-SIDE now (research-os #103): the
        # backend re-resolves semantic hits against live rows and over-fetches
        # so the filter runs before the cap. The old client-side path emptied
        # the semantic channel outright and reported
        # project_scope_unsupported -- a scoped search silently became
        # trigram-only. Nothing to do here but pass the scope through.
        results = _interleave(
            [_exact_result(row) for row in exact["results"]],
            [_semantic_result(row) for row in semantic["results"]],
        )
        if collapse == EntityType.EXPERIMENT:
            results = _collapse_experiments(results)
        # `top_k` is a TOTAL, so the merge is where it is applied. Both channels
        # were asked for all of it; what they returned together can exceed it.
        fetched = len(results)
        results = results[:top_k]
        missing = []
        if exclude_agent_session is not None and semantic.get("exclusion_applied") is not True:
            # We asked and the server did not echo, so it predates the field and
            # ignored it: SearchRequest permits extra body fields. The caller's
            # own session is therefore STILL in these results. Say so -- an
            # unmarked wrong answer is the failure this exists to prevent.
            missing.append(MissingMarker.SELF_EXCLUSION_UNSUPPORTED)
        elif (
            exclude_agent_session is not None
            and not results
            and not exact["error"]
            and not semantic["error"]
            and (semantic.get("excluded_count") or 0) > 0
        ):
            # The search RAN, the corpus answered, and every surviving row was
            # the caller's own conversation. This is a STOP, not a degradation:
            # rewording cannot produce a different corpus. Guarded on
            # total_candidates so a genuinely empty corpus stays an ordinary
            # empty result rather than claiming a self-exclusion that removed
            # nothing.
            missing.append(MissingMarker.ALL_RESULTS_WERE_OWN_SESSION)
        if exclude_origin_session is not None and not (
            isinstance(response, dict) and response.get("origin_exclusion_applied") is True
        ):
            # Same failure shape as the transcript exclusion above: asked, not
            # echoed, so the server ignored the field and the session's own
            # projects and runs are still in these results.
            missing.append(MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED)
        if exact["error"]:
            missing.append(MissingMarker.EXACT_SEARCH)
        if semantic["error"]:
            missing.append(MissingMarker.SEMANTIC_SEARCH)
        # The semantic channel answered but was missing one of ITS channels.
        # Marked separately from SEMANTIC_SEARCH: a channel that returned
        # nothing is visibly broken, whereas thinned results look like a
        # complete answer, which is why this one has to be said out loud.
        # Absent on an older backend -> no marker -> reads as healthy, the
        # safe direction during a rolling deploy.
        semantic_lost = [c for c in (semantic.get("lost_channels") or []) if isinstance(c, str)]
        if semantic_lost:
            missing.append(MissingMarker.SEMANTIC_CHANNEL_DEGRADED)
        # The channels were all alive and the ANSWER is still degraded. Said
        # separately, and said at all: the engine had been reporting this for
        # months while this boundary dropped it, so every fallback answer
        # reached the agent indistinguishable from a healthy one.
        if semantic.get("degraded"):
            missing.append(MissingMarker.SEMANTIC_ANSWER_DEGRADED)
        if unsupported:
            missing.append(MissingMarker.KB_VALUES)
        if isinstance(response, dict) and response.get("truncated"):
            # The backend trimmed the response onto its size budget, so an
            # absent document is NOT evidence of absence. Surfacing this is the
            # whole point of the backend emitting it -- a caller that cannot see
            # the trim reads a short result set as a complete one.
            missing.append(MissingMarker.TRUNCATED_BY_RESPONSE_BUDGET)
        backend_ok = isinstance(response, dict) and response.get("state") == BackendSearchState.OK

        def _payload(rows: list[dict], budget_note: dict | None) -> dict:
            data: dict[str, Any] = {
                "query": query,
                "collapse": collapse,
                "results": rows,
                "channels": {
                    Channel.EXACT.value: {"error": exact["error"]},
                    # `lost_channels` names the engine's OWN dead channels
                    # ("bm25", "vector", "graph", "inferred_edge") on a
                    # semantic response that otherwise succeeded. Emitted only
                    # when non-empty: on a healthy search this block should
                    # stay exactly as small as it has always been.
                    Channel.SEMANTIC.value: {
                        "error": semantic["error"],
                        # Emitted only when non-empty / non-default, so a
                        # healthy search's block stays exactly as small as it
                        # has always been.
                        **({"lost_channels": semantic_lost} if semantic_lost else {}),
                        # WHY the answer is degraded, beside the marker that
                        # says THAT it is: "loop_timeout" and "schema_violation"
                        # call for different reactions, and an agent holding
                        # only the marker cannot tell them apart.
                        **(
                            {"degraded_reason": semantic["degraded_reason"]}
                            if semantic.get("degraded") and semantic.get("degraded_reason")
                            else {}
                        ),
                        # How the engine graded what it returned: EXTRACTED
                        # (matched deterministically) vs INFERRED vs AMBIGUOUS.
                        **(
                            {"confidence_breakdown": semantic["confidence_breakdown"]}
                            if semantic.get("confidence_breakdown")
                            else {}
                        ),
                    },
                },
                # The recall hint the instructions tell the agent to check
                # before concluding the lab has not tried something. It was
                # instructed in two places and returned in none, which is worse
                # than not mentioning it: the agent looks, finds nothing, and
                # either gives up on the check or invents a number.
                # None on backends that do not report it.
                "total_candidates": semantic.get("total_candidates"),
                "active_runs_count": exact.get("active_runs_count"),
                "unsupported_values": unsupported,
            }
            if budget_note:
                data["budget"] = budget_note
            # The view vocabulary, for the hits an agent can actually open.
            #
            # SEARCH IS THE LAST RUNG, and until now it was the only route to an
            # address that handed back no views at all: browse and card both
            # carry `available_views`, so an agent that arrived by the ladder's
            # cheap step knew what it could ask for and an agent that arrived by
            # its expensive one did not. Keyed by kind, once per response, the
            # same shape browse uses -- not per hit, which would repeat one
            # kind's list for every row of it.
            #
            # Terminal hits fall out for free: `_supported_views` answers [] for
            # a document or a file, and entity has no route for them either, so
            # the two agree without a second list to keep in step.
            offered = {}
            for row in rows:
                kind = str(row.get("entity_type") or "")
                if kind and kind not in offered:
                    views = _supported_views(kind)
                    if views:
                        offered[kind] = views
            if offered:
                data["available_views"] = {k: offered[k] for k in sorted(offered)}
            note_missing = list(missing)
            if budget_note and budget_note.get("results_available", 0) > len(rows):
                note_missing.append(MissingMarker.RESULTS_BEYOND_BUDGET)
            return self._envelope(
                data,
                state=(
                    EnvelopeState.COMPLETE
                    if backend_ok and not note_missing
                    else EnvelopeState.PARTIAL
                ),
                missing=sorted(set(note_missing)),
                # A cursor ONLY when every fetched row shipped. The per-channel
                # cursors advance by what was fetched, so handing one back after
                # dropping rows for budget would silently skip exactly the rows
                # the caller was told to page for.
                next_cursor=(
                    _join_cursor(exact["cursor"], semantic["cursor"])
                    if len(rows) == fetched
                    else None
                ),
                verbose=verbose,
            )

        return _fit_whole_results(
            results,
            _payload,
            # CLAMPED, not validated. The tool surface already constrains this
            # (ge=512, le=8000); this method is also callable straight from
            # Python, where nothing does -- and the graceful answer to "600000"
            # is the biggest legal budget, not a traceback from a constructor.
            Budget(max(_MIN_TOKEN_BUDGET, min(int(token_budget), _MAX_TOKEN_BUDGET))),
            available=fetched,
        )

    def _checked_view(self, kind: str, view: str) -> str:
        """The view must EXIST for this kind. Rejecting loudly beats the old
        behavior — an unknown view used to fall through to a card-shaped payload,
        and contract/versions/usage returned an envelope that always said
        `missing`, which reads as "temporarily degraded" rather than "not a
        thing". The error names what this kind actually supports."""
        if (kind, view) in _VIEWS:
            return view
        raise errors.ValidationError(
            f"view={view!r} is not available for a {kind}; {kind} supports:\n"
            f"{_views_offered(kind)}",
            status=422,
        )

    def _checked_view_options(
        self, kind: str, view: str, filters: dict[str, Any] | None
    ) -> dict[str, Any]:
        # The WIRE name is `view_options` (server.py); inside the service the bag
        # is still `filters`, and every view echoes it under that key. Renaming
        # the echoed payload key is a response-shape change for its own PR.
        # Empty values are dropped, not passed through: `{"key": ""}` is not a
        # filter. Kept, it would echo back in the payload as though it had been
        # applied while every truthiness check downstream ignored it.
        supplied = {
            key: value
            for key, value in (filters or {}).items()
            if view == View.RECORD or (value is not None and value != "")
        }
        allowed = _VIEW_OPTIONS.get((kind, view), set())
        unknown = sorted(set(supplied) - allowed)
        if not unknown:
            return supplied
        detail = (
            f"view={view!r} on a {kind} accepts no view options"
            if not allowed
            else f"supported view options for view={view!r} on a {kind}: {sorted(allowed)}"
        )
        raise errors.ValidationError(f"unknown view option(s) {unknown}: {detail}", status=422)

    # -- research_get --------------------------------------------------------

    def get_entity(
        self,
        ref: str,
        view: str = View.CARD,
        token_budget: int = 2000,
        cursor: str | None = None,
        filters: dict[str, Any] | None = None,
        verbose: bool = False,
    ) -> dict:
        """One entity, one purpose-shaped view. See `_VIEWS` for the real matrix.

        This layer chooses approximate source-page row windows and preserves
        complete atomic payloads. MCP delivery then fragments any oversized
        page, includes all envelope/cursor overhead, and applies its exact cap.
        Legacy size markers here describe source selection; delivery replaces
        the obsolete atomic overflow marker once the full payload is reachable.
        """
        try:
            kind, entity = self.source.get(ref)
        except errors.NotFoundError as exc:
            context = current_delivery()
            if context and context.snapshot:
                raise source_changed("document is unavailable") from exc
            raise
        view = self._checked_view(kind, view)
        request = _Req(
            filters=self._checked_view_options(kind, view, filters),
            offset=_split_get_cursor(cursor, view),
        )
        result: _ViewData = getattr(self, _VIEWS[(kind, view)])(entity, request)
        # `X-Probe-Hide-Session-Work` (the daemon's reader): the entity asked for
        # is shown, but the rows, edges and origins in its view that name work the
        # caller's own session created are not -- after browse, a prior project's
        # lineage is where the session's new experiments and runs would surface.
        hide_session = accounting.session_work_to_hide()
        if hide_session is not None:
            result = self._without_session_work(
                result,
                hide_session,
                own_id=str(entity.get("id")) if isinstance(entity, dict) else None,
            )

        data: dict[str, Any] = {
            "entity_type": kind,
            "entity": _entity_projection(
                kind,
                entity,
                card=view == View.CARD,
                document=view in {View.NOTES, View.SUMMARY},
            ),
            "view": str(view),
            **result.payload,
        }
        if view == View.CARD:
            # The default view teaches what else you can ask for, DERIVED from
            # the same matrix that validates the request. Discovery by failed
            # call is a fine contract with four views; with eleven across five
            # kinds it is a tax on every first look at an unfamiliar entity.
            data["available_views"] = _supported_views(kind)
            # The card is what an agent reads before reporting on an entity, so
            # it is where the shareable link has to be if the report is going to
            # carry one. Omitted when unknown rather than guessed -- see
            # sdk.links.dashboard_base_url.
            url = links.entity_url(
                kind,
                entity.get("id") if isinstance(entity, dict) else None,
                # Only a nested kind reads this; `run_id` is absent on every
                # other entity and passing None is what those already did.
                parent_id=entity.get("run_id") if isinstance(entity, dict) else None,
                api_base_url=self._api_base_url,
            )
            if url:
                data["url"] = url
        missing = list(result.missing)
        next_cursor: str | None = None
        # A row view that emitted every row it has. False for an atomic view,
        # which has no rows and therefore no "walk" to be at the end of.
        rows_exhausted = False

        if result.rows is None:
            if request.offset:
                raise errors.ValidationError(
                    f"view={view!r} returns a single payload and cannot be paginated",
                    status=422,
                )
        else:
            # Spend the budget on rows only after the fixed part is paid for.
            # _fit still emits one row at a floor of 0, so a caller always makes
            # progress and the overflow is reported below rather than hidden.
            window = result.rows[request.offset :]
            emitted = _fit(window, max(0, token_budget - _tokens(data)))
            data[result.rows_key] = emitted
            budget_cut = len(emitted) < len(window)
            rows_exhausted = not budget_cut and not result.more_beyond
            if budget_cut or result.more_beyond:
                next_cursor = _join_get_cursor(view, request.offset + len(emitted))
            if budget_cut:
                # Only a BUDGET cut is "partial". Reaching the end of a fetch
                # window is ordinary pagination — research_search returns a cursor
                # with state=complete for exactly that, and this stays consistent
                # with it. Either way next_cursor is the signal that more exists.
                missing.append(MissingMarker.TRUNCATED_BY_TOKEN_BUDGET)

        if _tokens(data) > token_budget and MissingMarker.TRUNCATED_BY_TOKEN_BUDGET not in missing:
            missing.append(MissingMarker.TOKEN_BUDGET_EXCEEDED)
        # On the LAST page of a row walk, token_budget_exceeded says the opposite
        # of every other marker here: not "data is missing" but "you have all of
        # it, and it cost more than you asked for". Nothing was withheld, so there
        # is nothing to continue, so next_cursor is correctly None -- and the pair
        # `state=partial` + `next_cursor=None` told a caller walking the cursor
        # that something was missing with no way to fetch it. That walk never
        # terminates cleanly: every page but the last reports partial-with-cursor
        # (true), and the last reports partial-without (a dead end). Reachable
        # with no rows at all, too -- `_fit` emits one row at a floor of 0, so any
        # entity whose FIXED part outgrows the budget lands here.
        #
        # Only for a row view that reached its end. An ATOMIC view (reproduce)
        # keeps reporting partial: it has no pagination to be at the end of, and
        # over-budget there is a standing warning that the manifest is bigger than
        # the caller can hold -- deliberate, and pinned by test_mcp_views.
        #
        # The marker rides along either way; it just stops deciding the verdict.
        verdict = [
            m for m in missing if not (m == MissingMarker.TOKEN_BUDGET_EXCEEDED and rows_exhausted)
        ]
        # NO_MATCH outranks PARTIAL: it is the ANSWER to the question asked, while
        # `missing` describes the response's own completeness, and the two are
        # independent. A truncated no-match that reported state="partial" would
        # hide the ceiling behind what reads as a transient degradation -- and the
        # truncation is still visible, because `missing` rides along either way.
        if result.no_match:
            state = EnvelopeState.NO_MATCH
        else:
            state = EnvelopeState.PARTIAL if verdict else EnvelopeState.COMPLETE
        return self._envelope(
            data,
            state=state,
            missing=missing,
            next_cursor=next_cursor,
            verbose=verbose,
        )

    # -- view builders -------------------------------------------------------
    # Contract: report what is genuinely absent in `missing`, and NEVER report it
    # unconditionally — an always-`missing` view is the lie this rewrite removes.

    @staticmethod
    def _bounded(fetch: Any, offset: int, backend_max: int) -> tuple[list[dict], bool, bool]:
        """Fetch the caller's window plus ONE lookahead row, then drop it.

        Returns ``(rows, more_beyond, capped)``. The lookahead makes "are there more
        rows?" a fact instead of a guess, with no false positive when the window
        lands exactly on the end.

        `capped` means the BACKEND refused to go further (it returned its own
        ceiling), which is the only thing that makes rows genuinely unreachable.
        Inferring it from the offset instead reports the ceiling on a short run that
        was read in full -- a false `missing` marker, which corrupts the exact
        signal the envelope exists to carry.

        CALLERS MUST USE `capped`. At the ceiling `want == backend_max`, so the
        lookahead row cannot be fetched and `more_beyond` is False BY CONSTRUCTION:
        a caller that ignores `capped` there emits state="complete" with no cursor
        while rows sit unread. `capped` is the only signal left at that boundary.

        TODO(backend): these routes take `limit` and no offset, so each page refetches
        from row 0 and a full walk is quadratic (a 6000-span walk pulls ~90k rows).
        One backend call per page, but a linearly growing one. An `offset`/cursor on
        GET /v1/runs/{id}/spans would make this linear."""
        want = min(offset + _PAGE_FETCH, backend_max)
        fetched = fetch(min(want + 1, backend_max))
        return fetched[:want], len(fetched) > want, len(fetched) >= backend_max

    def _view_card(self, entity: dict, request: _Req) -> _ViewData:
        """The entity projection is assembled once, without extra source reads."""
        return _ViewData()

    def _view_artifact_card(self, entity: dict, request: _Req) -> _ViewData:
        """Preserve authored caveats without advertising an absent notes view."""
        excerpt = _notes_excerpt(
            entity.get("notes"), read_all='view="record", view_options={"field":"notes"}'
        )
        return _ViewData() if excerpt is None else _ViewData(payload={"notes": excerpt})

    def _view_record(self, entity: dict, request: _Req) -> _ViewData:
        """Explicit full-record/field access, paged at the common delivery boundary."""
        if "field" not in request.filters:
            return _ViewData(payload={"record": entity})
        path, value = _record_field(entity, request.filters["field"])
        return _ViewData(payload={"record": value, "field": path})

    def _view_trajectory(self, entity: dict, request: _Req) -> _ViewData:
        """The spans themselves. The run bundle carries span_type COUNTS, so before
        this an agent could see that 500 rollouts happened and not one of what they
        did — the sharpest gap for an RL-pitched product."""
        run_id = str(entity["id"])
        spans, more, capped = self._bounded(
            lambda limit: self.source.run_spans(run_id, limit=limit, **request.filters),
            request.offset,
            _SPAN_BACKEND_MAX,
        )
        return _ViewData(
            payload={"filters": request.filters or None},
            rows=spans,
            rows_key="spans",
            missing=[MissingMarker.SPANS_BEYOND_BACKEND_LIMIT] if capped else [],
            more_beyond=more,
        )

    def _view_run_trials(self, entity: dict, request: _Req) -> _ViewData:
        """The run's authored trials, newest step first (0135).

        Cursor-walked rather than `limit`-fetched: this route caps ONE call at
        `MAX_LIMIT` (200), which is below `_bounded`'s `_PAGE_FETCH + 1`
        lookahead. Passing the lookahead straight through would get a short page
        back and `_bounded` would read short as "that was everything" -- the
        precise failure `more_beyond` exists to prevent, arriving through the
        argument meant to detect it.
        """
        run_id = str(entity["id"])
        rows, more, capped = self._bounded(
            lambda limit: self._trial_pages(run_id, limit),
            request.offset,
            _TRIAL_BACKEND_MAX,
        )
        return _ViewData(
            rows=rows,
            rows_key="trials",
            missing=[MissingMarker.TRIALS_BEYOND_WALK_BOUND] if capped else [],
            more_beyond=more,
        )

    def _trial_pages(self, run_id: str, limit: int) -> list[dict]:
        """`limit` trial rows, following the route's keyset cursor.

        The cursor is LOCAL to this walk and never stored on the service: one
        `_bounded` call is one complete walk from row 0, so a cursor surviving
        the call would resume a later view somewhere in the middle of the data
        and report it as the beginning.
        """
        rows: list[dict] = []
        cursor: str | None = None
        while len(rows) < limit:
            page = self.source.run_trials(
                run_id, cursor=cursor, limit=min(_TRIAL_ROUTE_PAGE, limit - len(rows))
            )
            items = list(page.items)
            rows.extend(items)
            cursor = page.next_cursor
            # An empty page ends the walk even when a cursor came back with it --
            # otherwise a backend that always answers with one spins here forever.
            if not cursor or not items:
                break
        return rows[:limit]

    def _view_trial_trajectory(self, entity: dict, request: _Req) -> _ViewData:
        """One rollout's span SUBTREE -- what this trial actually did.

        Not reachable by narrowing the run's trajectory. The spans route filters
        on DIRECT `parent_span_id`, so asking the run for "trial X's spans"
        returns X's children and stops, and a rollout -> turn -> tool_call tree
        reads as a rollout with turns and no tools. The walk therefore happens
        here, over a slice of the run's spans, exactly as the dashboard's own
        trial page does it.

        THE SLICE IS NARROWED BY STEP, which is a real server-side filter and not
        a guess: every producer that writes a rollout subtree stamps the whole
        subtree with the rollout's own `step_index` (`connectors/atif.py` sets it
        once for the batch; `capture_trial` keys the trial on it). A trial with no
        step falls back to the run-wide bounded read -- correct, just heavier.

        Both ways the slice can come up short are REPORTED rather than absorbed:
        a descendant past the ceiling, and a rollout span the slice never
        contained at all. The second is why this does not simply return `[]` --
        0135 lets the sidecar outlive the span slice on purpose, so an empty walk
        genuinely means "not read", never "did nothing".
        """
        rollout_id = str(entity["id"])
        run_id = str(entity.get("run_id") or "")
        step = entity.get("step_index")
        window = {"step_from": step, "step_to": step} if step is not None else {}
        fetched = self.source.run_spans(run_id, limit=_SPAN_BACKEND_MAX, **window)
        slice_capped = len(fetched) >= _SPAN_BACKEND_MAX

        subtree = _span_subtree(fetched, rollout_id)
        missing: list[str] = []
        if subtree is None:
            # The sidecar answered and its rollout span did not. Say which.
            return _ViewData(
                payload={
                    "rollout_span_id": rollout_id,
                    "read_from": {"run_id": run_id, **window},
                },
                rows=[],
                rows_key="spans",
                missing=[MissingMarker.TRIAL_ROLLOUT_SPAN_UNREAD],
            )
        if slice_capped:
            missing.append(MissingMarker.TRIAL_SPANS_BEYOND_RUN_SLICE)

        span_type = request.filters.get("span_type")
        if span_type:
            # Client-side, AFTER the walk -- see this pair's `_VIEW_OPTIONS` note.
            subtree = [row for row in subtree if row.get("span_type") == span_type]
        return _ViewData(
            payload={
                "rollout_span_id": rollout_id,
                "read_from": {"run_id": run_id, **window},
                "filters": request.filters or None,
            },
            rows=subtree,
            rows_key="spans",
            missing=missing,
            no_match=bool(span_type) and not subtree,
        )

    def _metric_points(self, run_id: str, *, limit: int, **filters: Any) -> list[dict]:
        """Raw points for a run, from wherever that run actually keeps them.

        A MIRRORED run (W&B live sync, say) stores a passport rather than a copy
        of its points, so the raw-row route refuses it with
        `unsupported_source_query` -- a raw row has nowhere to carry the
        provider's coverage receipt. That refusal names the door that does
        (`/v1/series/query`), so it is a ROUTING INSTRUCTION, not a failure to
        hand back to the agent: surfacing it is what made every mirrored run
        read as having no metrics at all."""
        try:
            return self.source.run_metrics(run_id, limit=limit, **filters)
        except errors.ValidationError as exc:
            detail = exc.detail if isinstance(exc.detail, dict) else {}
            if detail.get("code") != "unsupported_source_query":
                raise
        keys = [k for k in (filters.get("key"),) if k]
        body: dict[str, Any] = {"keys": keys} if keys else {}
        if filters.get("kind"):
            body["kind"] = filters["kind"]
        result = self.source.query_series([run_id], **body) or {}
        rows: list[dict] = []
        for series in result.get("series") or ():
            for point in series.get("points") or ():
                rows.append(
                    {
                        "run_id": series.get("run_id", run_id),
                        "kind": series.get("kind"),
                        "key": series.get("key"),
                        "dimensions": series.get("dimensions") or {},
                        "step_index": point.get("step_index"),
                        "wall_clock": point.get("wall_clock"),
                        "value": point.get("value"),
                    }
                )
                if len(rows) >= limit:
                    return rows
        return rows

    def _view_metrics(self, entity: dict, request: _Req) -> _ViewData:
        """Series summaries by default; `filters.key` drills through to the raw
        points. Progressive disclosure inside one view, rather than dumping every
        metric point a run ever logged."""
        run_id = str(entity["id"])
        if request.filters.get("key"):
            points, more, capped = self._bounded(
                lambda limit: self._metric_points(run_id, limit=limit, **request.filters),
                request.offset,
                _METRIC_BACKEND_MAX,
            )
            return _ViewData(
                payload={"granularity": "points", "filters": request.filters},
                rows=points,
                rows_key="points",
                missing=[MissingMarker.METRIC_POINTS_BEYOND_BACKEND_LIMIT] if capped else [],
                more_beyond=more,
            )
        series = self.source.run_series(run_id)
        kind = request.filters.get("kind")
        if kind:  # GET /v1/runs/{id}/series takes no filters; narrow client-side
            series = [row for row in series if row.get("kind") == kind]
        return _ViewData(
            payload={"granularity": "series_summary", "filters": request.filters or None},
            rows=series,
            rows_key="series",
        )

    def _view_run_artifacts(self, entity: dict, request: _Req) -> _ViewData:
        rows = self.source.run_artifacts(str(entity["id"]), **request.filters)
        payload: dict = {"filters": request.filters or None}
        # Async-outbox visibility (eng review 2026-07-29, 1A): a row with
        # status "pending" is a REGISTERED INTENT whose bytes have not arrived
        # (a client outbox may still deliver it); "failed" means the grace
        # window expired undelivered. Surfacing the counts here keeps the
        # metadata-match-is-not-the-blob rule unmissable for agents.
        pending = sum(1 for r in rows if isinstance(r, dict) and r.get("status") == "pending")
        failed = sum(1 for r in rows if isinstance(r, dict) and r.get("status") == "failed")
        if pending or failed:
            payload["undelivered"] = {
                "pending": pending,
                "failed": failed,
                "note": (
                    "pending = upload intent registered, bytes not yet arrived "
                    "(an async client outbox may still deliver); failed = the "
                    "grace window expired undelivered. Only status='complete' "
                    "rows have retrievable bytes."
                ),
            }
        return _ViewData(payload=payload, rows=rows, rows_key="artifacts")

    def _view_experiment_artifacts(self, entity: dict, request: _Req) -> _ViewData:
        return _ViewData(
            rows=self.source.experiment_artifacts(str(entity["id"])), rows_key="artifacts"
        )

    def _view_project_card(self, entity: dict, request: _Req) -> _ViewData:
        """The project card, carrying the project's notes.

        Read straight off the entity, which `source.get` already fetched: since
        research-os 0094 the notes are a COLUMN on the project row, so this costs no
        request at all. That is what makes putting them on the card affordable --
        orientation is `browse_research` then a card, and a briefing an agent has to
        KNOW to ask for is one it does not read. Bounded to an excerpt so a long
        document cannot blow the token budget of what is supposed to be the cheap
        glance; `view="notes"` has the rest.
        """
        payload: dict = {}
        excerpt = _notes_excerpt(entity.get("notes"))
        if excerpt is not None:
            payload["notes"] = excerpt
        # 0134: the connection fact, off the already-fetched detail row (the
        # backend puts code_sources on the project read), so it costs nothing.
        sources = entity.get("code_sources") or []
        if sources:
            active = [s for s in sources if s.get("status") == "active"]
            suggested = sum(1 for s in sources if s.get("status") == "suggested")
            code: dict = {
                "repos": [f"{s['repo']}@{s['ref']}" for s in active[:5]],
                # Non-revoked, matching every backend code_source_count surface
                # (a revoked source is history, not a live connection).
                "count": sum(1 for s in sources if s.get("status") != "revoked"),
                "read_history": 'view="code"',
            }
            if suggested:
                code["suggested"] = suggested
            payload["code"] = code
        # 0159: who worked on this, off the already-fetched detail row, so it
        # costs no request. NAMES, because a uuid answers nobody's question.
        # `via` names the subproject when the work was done below this project;
        # its absence means they worked here.
        contributors = entity.get("contributors") or []
        if contributors:
            payload["contributors"] = [
                {
                    "name": c.get("name") or c.get("email") or c.get("user_id"),
                    **({} if c.get("direct", True) else {"via": c.get("via_project_id")}),
                }
                for c in contributors[:_MAX_CARD_CONTRIBUTORS]
            ]
            if len(contributors) > _MAX_CARD_CONTRIBUTORS:
                payload["contributors_truncated"] = len(contributors)
        # 0153: lateral peer edges, both directions, off the already-fetched
        # detail row. On the CARD rather than behind a view for the same reason
        # `code` is: a relationship an agent has to know to ask about is one it
        # never sees, and a lit review's whole point is being reachable from
        # the work it informed.
        references = entity.get("references") or []
        if references:
            # FLAT keys, matching what the tool description advertises. Nesting
            # them under `references` made an agent looking for
            # `referenced_by` find nothing and read that as "no incoming
            # links" — a confident wrong answer about the exact relation this
            # exists to surface.
            #
            # CAPPED per direction, like the `code` block above. The card is
            # the cheap glance, and `token_budget` bounds ROWS, not payload —
            # so an uncapped list here (up to MAX_PROJECT_REFERENCES per
            # direction) would blow the default budget on a heavily-referenced
            # project and degrade the one read meant to be cheapest. The
            # counts stay exact so the excerpt never reads as the whole set.
            for key, direction in (
                ("references", "outgoing"),
                ("referenced_by", "incoming"),
            ):
                slugs = [r["project_slug"] for r in references if r.get("direction") == direction]
                if not slugs:
                    continue
                block: dict = {"projects": slugs[:_CARD_REFERENCE_SLUGS]}
                if len(slugs) > _CARD_REFERENCE_SLUGS:
                    block["count"] = len(slugs)
                payload[key] = block
            if entity.get("references_truncated"):
                payload["references_truncated"] = True
        return _ViewData(payload=payload) if payload else _ViewData()

    def _view_project_notes(self, entity: dict, request: _Req) -> _ViewData:
        """The project's notes in full. No schema: free-text markdown that agents
        read and write, not a record type. The MAIN note is off the
        already-fetched row; the sub-notes section (0146) is fetched here."""
        return self._notes_with_sub_notes(entity, "project")

    def _view_run_notes(self, entity: dict, request: _Req) -> _ViewData:
        """A run's notes in full (0124) + its titled sub-notes (0146)."""
        return self._notes_with_sub_notes(entity, "run")

    def _view_experiment_notes(self, entity: dict, request: _Req) -> _ViewData:
        """An experiment's notes in full (0124) + its titled sub-notes (0146)."""
        return self._notes_with_sub_notes(entity, "experiment")

    def _view_group_notes(self, entity: dict, request: _Req) -> _ViewData:
        """A group's notes in full (0124) + its titled sub-notes (0146)."""
        return self._notes_with_sub_notes(entity, "group")

    def _notes_with_sub_notes(self, entity: dict, kind: str) -> _ViewData:
        """The full-notes view: the MAIN document off the already-fetched row,
        plus each titled SUB-NOTE (0146) as a bounded excerpt.

        Excerpts, not full bodies, and the bound is deliberate: twenty 100k
        documents inside one tool result is a context bomb, and the view's job
        is surfacing that a caveat EXISTS and what it starts with. `read_all`
        names the doors that hold the whole document. Cards stay untouched —
        a titles line there would be an N+1 on the cheapest read.

        ABSENT on any failure, never invented: a backend without 0146 (or a
        transient error) yields no `sub_notes` key at all, exactly like an
        entity that has none — the headroom rule's "absent means the response
        did not carry it" applied one level up.
        """
        body, version = entity.get("notes"), entity.get("notes_version")
        if current_delivery() is not None:
            if hasattr(self.source, "notes_document") and entity.get("id"):
                body, version = self.source.notes_document(kind, entity)
            else:
                pinned = pin_document(
                    body or "", f"notes:{kind}:{entity.get('id')}", version=version
                )
                body = None if body is None and not pinned else pinned
        payload: dict = {"notes": body}
        if version is not None:
            payload["notes_version"] = version
        # THE REMINDER TRAVELS WITH THE DOCUMENT. A skill file read once at load
        # does not reach the model forty minutes later holding the note that
        # contradicts it -- measured 2026-09-08, when an agent found six claims
        # this repository disproved and corrected none of them. Derived from the
        # headroom the server already publishes, so it is silent rather than
        # invented when the response did not carry the document.
        # Only where there IS a document. `notes_headroom` publishes the full cap
        # for a NULL `notes`, and the notes view is offered on every entity, so
        # without this a run that never had a note answers "0% full — correct
        # what your evidence contradicts", which is advice about nothing.
        advisory = read_advisory(entity, version=version) if body else None
        if advisory is not None:
            payload["notes_advisory"] = advisory
        entity_id = entity.get("id") if isinstance(entity, dict) else None
        if entity_id:
            try:
                page = self.source.client.list_sub_notes(kind, str(entity_id))
            except errors.RosError:
                page = None
            rows = (page or {}).get("sub_notes") or []
            section = []
            for row in rows:
                item: dict = {
                    "title": row.get("title"),
                    "chars": row.get("chars"),
                    "limit_chars": row.get("limit_chars"),
                }
                try:
                    body = self.source.client.get_sub_note(str(row["id"])).get("body") or ""
                except errors.RosError:
                    # A failed body read must not render as an EMPTY sub-note —
                    # "this caveat tab is blank" is a conclusion, and an outage
                    # must not draw it. Say unavailable instead.
                    item["unavailable"] = True
                    body = ""
                if body:
                    item["excerpt"] = body[:_SUB_NOTE_VIEW_EXCERPT]
                    if len(body) > _SUB_NOTE_VIEW_EXCERPT:
                        item["truncated"] = True
                        item["read_all"] = (
                            "the entity page's Notes tab, or `probe notes show --note <title>`"
                        )
                section.append(item)
            if section:
                payload["sub_notes"] = section
        return _ViewData(payload=payload)

    def _view_card_with_notes(self, entity: dict, request: _Req) -> _ViewData:
        """The generic card, plus a bounded notes excerpt (0124).

        Runs, groups and experiments carry notes now, and the argument that put
        them on the PROJECT card applies unchanged: orientation is
        `browse_research` then a card, and a caveat an agent has to know to ask
        for is one it does not read. A run whose note says "the scorer was stale,
        distrust these numbers" must reach a reader who only glanced at it.
        """
        excerpt = _notes_excerpt(entity.get("notes"))
        return _ViewData() if excerpt is None else _ViewData(payload={"notes": excerpt})

    def _view_project_code(self, entity: dict, request: _Req) -> _ViewData:
        """The project's attached repositories + one page of commit timeline.

        The timeline is read THROUGH GitHub by the backend (ETag-cached), so
        `timeline.state` is part of the answer: `ok`, `stale` (real data,
        degraded freshness — GitHub could not refresh it just now) or
        `unavailable` (no data; the reason says why). A run's `sha` here means
        the run was BASED ON that commit (nearest pushed ancestor), never that
        it ran exactly that code — the uploaded archive stays the code's home.

        Filters: `commit=<sha>` drills to one commit (message body, files,
        stats, linked runs); `source=<id>` picks a repository when several are
        attached; `cursor`, `author`, `path`, `include_excluded` page and
        narrow the list. Attach is NOT here: `probe project code attach
        <project> <owner/repo>` is the write door.
        """
        sources = entity.get("code_sources") or []
        filters = dict(request.filters)
        sha = filters.pop("commit", None)
        source_id = filters.pop("source", None)
        source_rows = self._code_source_rows(sources)
        if sha:
            card = self.source.project_commit(
                str(entity["id"]), str(sha), str(source_id) if source_id else None
            )
            return _ViewData(payload={"commit": card, "sources": source_rows})
        if not sources:
            return _ViewData(
                payload={
                    "sources": [],
                    "note": (
                        "no code source attached. A person attaches from the "
                        "dashboard; an agent uses `probe project code attach "
                        "<project> <owner/repo> --reason ...` when the repo is "
                        "plainly this project's (e.g. a run's snapshot names it)."
                    ),
                }
            )
        selectable = [s for s in sources if s.get("status") in ("active", "missing")]
        if len(selectable) > 1 and not source_id:
            return _ViewData(
                payload={
                    "sources": source_rows,
                    "note": (
                        "several code sources are attached; pass "
                        'view_options={"source": "<id>"} to read one timeline'
                    ),
                }
            )
        if source_id:
            filters["source_id"] = str(source_id)
        page = self.source.project_code_commits(str(entity["id"]), **filters)
        timeline: dict = {"state": page.get("state")}
        if page.get("reason"):
            timeline["reason"] = page["reason"]
        if page.get("cursor"):
            timeline["next"] = 'view_options={"cursor": "%s"}' % page["cursor"]
        return _ViewData(
            payload={"sources": source_rows, "timeline": timeline},
            rows=page.get("items") or [],
            rows_key="commits",
            more_beyond=bool(page.get("cursor")),
        )

    #: The source-row keys every code view echoes — one trim, three views.
    _CODE_SOURCE_KEYS = (
        "id",
        "repo",
        "ref",
        "path_prefix",
        "status",
        "status_reason",
        "attached_via",
        "attach_reason",
        "head_sha",
        "start_sha",
        "html_url",
    )

    @classmethod
    def _code_source_rows(cls, sources: list[dict]) -> list[dict]:
        return [
            {key: s.get(key) for key in cls._CODE_SOURCE_KEYS if s.get(key) not in (None, "")}
            for s in sources
        ]

    def _view_experiment_code(self, entity: dict, request: _Req) -> _ViewData:
        """What changed in the repo between this experiment's runs (phase 6).

        STORED ROWS ONLY, unlike the project view's proxied timeline: the
        backend assembles this from run↔commit links and never asks GitHub, so
        a window here is the shas this experiment's runs actually resolved to
        — never the full git range between them. The project `view="code"`
        timeline is the complete, live history when that distinction matters.

        Sources are the PROJECT's (an experiment inherits them; attach stays a
        project-level write: `probe project code attach`). Runs are the rows —
        one per run, ordered by the run's own clock, each with its stored
        `owner/repo@sha`. Windows ride the fixed payload with commits
        compacted to short shas: the full rows (first_run_at, run_count) live
        on `GET /v1/projects/{ref}/code`, and re-printing them here would
        spend the row budget on the part that is already a summary.
        """
        out = self.source.experiment_code(str(entity["id"]))
        windows = []
        for window in out.get("windows") or []:
            row: dict = {
                key: window.get(key)
                for key in ("repo", "source_attached", "from_sha", "to_sha")
                if window.get(key) is not None
            }
            row["commits"] = [
                c.get("short_sha") or str(c.get("sha") or "")[:7]
                for c in window.get("commits") or []
            ]
            if window.get("commits_truncated"):
                row["commits_truncated"] = True
            windows.append(row)
        return _ViewData(
            payload={
                "sources": self._code_source_rows(out.get("sources") or []),
                "windows": windows,
            },
            rows=out.get("runs") or [],
            rows_key="runs",
        )

    def _view_run_code(self, entity: dict, request: _Req) -> _ViewData:
        """The run's resolved `owner/repo@sha` — and, with
        view_options={"compare_to": "run:<ref>"}, what changed in code between the
        two runs (base = the older run; `commits` reads oldest first).

        A compare FILTER on this view rather than a new view or a `reproduce`
        mode, deliberately: `code` is already the vocabulary's one word for
        "which commit is this code" (project timeline, experiment window), so
        the run grain completes that word instead of inventing a second one —
        and comparing IS the run-level code question asked about two runs, the
        way `commit=` drills the project timeline to one commit. Hanging it
        off `reproduce` was rejected: that view is an atomic passthrough of
        the backend manifest, and a second mode there would fork its contract.

        The plain read may verify resolvability against GitHub server-side
        (cached, bounded — it is the run panel's read); the compare is STORED
        ROWS ONLY, so its commit list is the shas runs resolved to between the
        two, never the full git range. Both are bounded server-side.
        """
        run_id = str(entity["id"])
        compare_to = request.filters.get("compare_to")
        if compare_to:
            ref = str(compare_to)
            if ref.startswith("run:"):
                ref = ref[len("run:") :]
            return _ViewData(payload={"compare": self.source.run_code_compare(run_id, ref)})
        return _ViewData(payload={"code": self.source.run_code(run_id)})

    def _view_project_summary(self, entity: dict, request: _Req) -> _ViewData:
        """Compatibility-shaped project read for authored Overview Markdown."""
        return self._view_entity_summary(EntityType.PROJECT, entity)

    def _view_experiment_summary(self, entity: dict, request: _Req) -> _ViewData:
        """The experiment's authored, dashboard-visible Markdown document."""
        return self._view_entity_summary(EntityType.EXPERIMENT, entity)

    @staticmethod
    def _view_entity_summary(kind: str, entity: dict) -> _ViewData:
        """Return visible authored Markdown without conflating it with Notes.

        ``project_summary`` remains the project payload key for compatibility;
        the experiment and run variants use their own nouns. The semantics are
        identical: one complete visible document, distinct from the entity's
        private operational Notes. It lives INSIDE the Overview page, as a
        block the page's AI writer may not rewrite, so what comes back is the
        page's rendering of it rather than the bytes anyone sent.

        0220: PROJECT AND EXPERIMENT ONLY. A run was never on the page lane, so
        when the column went there was nothing left for its `summary` view to
        read and the view went with it -- rather than answering "" for ever.
        """
        noun = str(kind)
        payload = {f"{noun}_summary": {"document": entity.get("document") or ""}}
        caveat = _notes_excerpt(entity.get("notes"))
        if caveat is not None:
            payload["notes"] = caveat
        return _ViewData(payload=payload)

    def _view_project_artifacts(self, entity: dict, request: _Req) -> _ViewData:
        return _ViewData(
            rows=self.source.project_artifacts(str(entity["id"])), rows_key="artifacts"
        )

    def _view_project_papers(self, entity: dict, request: _Req) -> _ViewData:
        """The papers recorded against this project, newest first.

        EMPTY IS AN ANSWER, and which answer depends on the project: on a
        review-flavored one it is a capture failure surfacing itself (someone
        read papers and recorded none); on a design-flavored one it is simply
        sparse. Either way it means "zero rows read successfully" and never
        "this read did not look" — a failed read raises rather than returning
        an empty list.

        Write with `probe paper add` / the SDK's `add_paper`; there is no write
        door here.
        """
        rows, more = self.source.project_papers(str(entity["id"]))
        return _ViewData(rows=rows, rows_key="papers", more_beyond=more)

    def _question_of(self, entity: dict, missing: list[str]) -> str | None:
        """A run's question lives on its experiment. Appends to `missing` rather
        than raising: a run whose experiment vanished is still worth reading, and
        the envelope is where that absence gets reported.

        A PROJECT-DIRECT run (experiment_id null WITH a project_id, the W&B
        shape) legitimately has no experiment — no question, and no missing
        marker either: nothing failed to load. The marker is reserved for a run
        that names an experiment this call could not read, and for old rows
        that carry neither id (pre-project_id backends)."""
        experiment_id = entity.get("experiment_id")
        if not experiment_id:
            if not entity.get("project_id"):
                missing.append(MissingMarker.EXPERIMENT)
            return None
        try:
            return self.source.experiment(str(experiment_id)).get("question")
        except errors.NotFoundError:
            missing.append(MissingMarker.EXPERIMENT)
            return None

    def _view_reproduce(self, entity: dict, request: _Req) -> _ViewData:
        """The server-assembled reproduction record (research-os /reproduce), not a
        client-side re-derivation. This used to hand back the same bundle as three
        other views, then assembled the manifest here; now the backend — the one
        place that reads execution record, launch, code snapshot, inputs, lockfiles,
        edges and span envs together — assembles it and this view delegates.

        Atomic: never truncated. A reproduction manifest with fields dropped to fit
        reproduces nothing, so overflow is REPORTED by ``get_entity``
        (``token_budget_exceeded``) instead of corrupting the answer.

        The envelope's ``missing`` carries the server's ``completeness.missing``
        verbatim — the reproduction-BLOCKING gaps (no execution record, no code
        snapshot, a launch slot that failed to capture) — so this view still reads
        ``partial`` when a run cannot be fully rebuilt. ``advisories`` stay in the
        payload's ``completeness`` block: they are judgment calls (no notes, no
        inputs decision) and legacy gaps (a pre-capture-core run has no launch
        context), never a degraded response."""
        record = self.source.reproduce(str(entity["id"]))
        completeness = record.get("completeness") or {}
        return _ViewData(payload=record, missing=list(completeness.get("missing") or []))

    def _view_handoff(self, entity: dict, request: _Req) -> _ViewData:
        """What a new session needs to continue.

        This is the one view the run bundle was always right for — state, series,
        lineage, and span_type counts that say a trajectory EXISTS and is worth a
        view="trajectory" call. The bug was never the bundle; it was four views
        sharing it. Artifacts are the part that scales, so they are the rows."""
        bundle = self.source.bundle(str(entity["id"]))
        missing: list[str] = []
        question = self._question_of(entity, missing)
        artifacts = bundle.get("artifacts") or []
        total = bundle.get("artifact_total")
        # The bundle's artifact list is capped SERVER-side (200) while artifact_total
        # counts them all, and the route takes no offset — so a cursor here would
        # page an already-truncated list and hand back an empty page as if it were
        # the end. Say it plainly and name the uncapped door instead: on a 5000-
        # artifact run this view would otherwise emit 200 and report `complete`.
        if isinstance(total, int) and total > len(artifacts):
            missing.append(MissingMarker.ARTIFACTS_BEYOND_BUNDLE_LIMIT)
        return _ViewData(
            payload={
                "question": question,
                "run": _entity_projection(EntityType.RUN, bundle.get("run") or {}, card=True),
                "series": bundle.get("series"),
                "span_types": bundle.get("span_types"),
                "artifact_total": total,
                "parent_run_id": bundle.get("parent_run_id"),
                "child_run_ids": bundle.get("child_run_ids"),
            },
            rows=artifacts,
            rows_key="artifacts",
            missing=missing,
        )

    def _view_run_lineage(self, entity: dict, request: _Req) -> _ViewData:
        """Both lineage relations, under distinct keys.

        `run_ancestry` is the `parent_run_id` walk -- fork/retry parentage,
        run-to-run. `edges` is the artifact / asset-version provenance graph.
        They answer different questions and this view used to return only the
        first, which made `ancestors: [] / descendants: []` the answer for a run
        that consumed a dataset version and produced three artifacts. An agent
        reads that as "this run has no lineage", a confident wrong answer.

        Deliberately NOT merged into one list: they are different relation types
        over different endpoint kinds, and flattening them recreates exactly the
        ambiguity that made the empty response unreadable.

        That separation is why `edges` FILTERS OUT the genealogy relations. Server
        0166 moved run -> run parentage into `lineage_edges` as
        `retried_from`/`forked_from`/`resumed_from`/`branched_from`, so without this
        filter every retry would arrive under BOTH keys -- the same edge counted
        twice, which is the exact ambiguity the split above exists to prevent.
        `run_ancestry` remains the single home for the parent CHAIN (every
        genealogy parent, both directions); `origin` (lineage plan 2, L18) is the
        one-line answer to "what did this run come from" -- its first parent,
        else what it built on, else its container.
        """
        run_id = str(entity["id"])
        edges = [
            edge
            for edge in self.source.run_edges(run_id)
            if str(edge.get("relation") or "") not in _GENEALOGY_RELATIONS
        ]
        ancestry = dict(self.source.lineage(run_id))
        payload: dict[str, Any] = {}
        # Lineage plan 2 (L18): where the run came from, derived by the server
        # -- its first parent, else what it built on, else its group, its
        # experiment or project, else `unfiled`. Lifted out of the ancestry read
        # so every lineage view answers "where did this come from" under one key.
        if "origin" in ancestry:
            payload["origin"] = ancestry.pop("origin")
        payload["run_ancestry"] = ancestry
        payload["edges"] = edges
        # `view_options.depth` (1-5): the upstream walk -- what this run built
        # on, N hops back, across parents, runs it built on and the writers of
        # every file it read (0255). "What produced this number?" is this walk
        # from the run that logged it. Edges carry `provenance` (observed_call /
        # inferred / human) and derived ones `meta.basis`, so a guess never
        # reads like an observation.
        depth = request.filters.get("depth")
        if depth is not None:
            try:
                depth = max(1, min(int(depth), 5))
            except (TypeError, ValueError):
                raise errors.ValidationError(
                    "view_options.depth must be an integer from 1 to 5", status=422
                ) from None
            payload["upstream"] = (
                self.source.run_upstream(run_id, depth)
                if self.source.server_records_reads()
                else {"unsupported": _NO_READ_LINEAGE}
            )
        return _ViewData(payload=payload)

    def _view_artifact_lineage(self, entity: dict, request: _Req) -> _ViewData:
        """Which run WROTE this file (or only carried it: its start snapshot
        copied it in, or a script logged an input) and which runs READ it --
        matched by content hash across every version (0255). The server's
        `origin` (L18: the run that wrote it, else where it is filed) passes
        through as it is."""
        if not self.source.server_records_reads():
            return _ViewData(payload={"unsupported": _NO_READ_LINEAGE})
        return _ViewData(payload=self.source.artifact_lineage(str(entity["id"])))

    def _view_project_lineage(self, entity: dict, request: _Req) -> _ViewData:
        """A project's or experiment's OWN lineage (server 0278, lineage plan 2
        L12/L13/L18), read from `GET /v1/projects/{id}/lineage`.

        `origin`: a project it builds on or replaces, else its parent project;
        null for a root. `edges`: its links in and out -- stored ones (with
        `provenance`, and `meta.via` on the daemon's), then "built on" DERIVED
        from its runs' reads (`derived: true`, `meta.basis: runs_read`), so a
        fact never reads like a guess. On an experiment, `run_edges` is the
        graph AMONG its runs and files (`GET /v1/projects/{id}/edges`, stored
        edges first). The ROWS are its children (sub-projects and experiments,
        groups, runs filed directly under it), each with its own origin, which
        is what connects the graph.

        The links are the FIXED part, so they are capped and sent on the first
        page only: a cursor walk over the children would otherwise re-send them
        with every page. Neither route takes an offset, so anything past a
        window -- children past the route's limit, links past a cap, "built on"
        over only the newest runs -- is flagged (`*_truncated`) and the view
        reports `partial` with `lineage_beyond_window`, never `complete`.
        """
        read = self.source.project_lineage(str(entity["id"]))
        payload: dict[str, Any] = {"origin": read.get("origin")}
        # Present only when true: a flag that is always there stops being read.
        flags: dict[str, bool] = {"nodes_truncated": bool(read.get("truncated"))}
        if request.offset:
            payload["links_on_first_page"] = True
        else:
            edges = list(read.get("edges") or [])
            payload["edges"] = edges[:_LINEAGE_LINKS_CAP]
            flags["edges_truncated"] = bool(read.get("edges_truncated")) or len(edges) > _LINEAGE_LINKS_CAP
            flags["derived_truncated"] = bool(read.get("derived_truncated"))
            if read.get("kind") == "experiment":
                # One past the cap, so a full window says so rather than passing
                # for the whole graph.
                among = self.source.experiment_edges(str(entity["id"]), _LINEAGE_LINKS_CAP + 1)
                payload["run_edges"] = among[:_LINEAGE_LINKS_CAP]
                flags["run_edges_truncated"] = len(among) > _LINEAGE_LINKS_CAP
        payload.update({flag: True for flag, cut in flags.items() if cut})
        return _ViewData(
            payload=payload,
            rows=list(read.get("nodes") or []),
            rows_key="nodes",
            missing=[MissingMarker.LINEAGE_BEYOND_WINDOW] if any(flags.values()) else [],
        )

    def _view_events(self, entity: dict, request: _Req) -> _ViewData:
        return _ViewData(rows=self.source.run_events(str(entity["id"])), rows_key="events")

    def _view_groups(self, entity: dict, request: _Req) -> _ViewData:
        """Sweeps/ensembles under an experiment — reached by a view, not by a
        research_list_groups tool. One group is research_get(ref="group:<id>")."""
        return _ViewData(rows=self.source.experiment_groups(str(entity["id"])), rows_key="groups")

    def _view_artifact_versions(self, entity: dict, request: _Req) -> _ViewData:
        """The reuse check's answer: this artifact's version chain, optionally
        narrowed to the versions that satisfy `requirement`.

        The two empty answers are OPPOSITES and this view is the only thing that
        can tell them apart, so it never collapses them:

        - the artifact does not exist -> resolution already raised NotFoundError
          (`artifact_by_name` for a name, the by-id `/versions` probe in
          `artifact_by_id` for an id), and a new identity is genuinely licensed.
          Note the two differ in REACH: a name only ever ruled out SHARED, while
          an id is global and rules out every anchor at once.
        - the artifact EXISTS but no version satisfies `requirement` ->
          state="no_match", carrying the versions that DO exist so the caller sees
          the real ceiling. Pin a new version of the SAME artifact.

        A caller that reads the second as the first opens a duplicate identity,
        which is the single most expensive avoidable error in this system.
        """
        versions = self.source.artifact_versions(str(entity["id"]))
        requirement = request.filters.get("requirement")
        if requirement is None or requirement == "":
            return _ViewData(rows=versions, rows_key="versions")
        requirement = str(requirement)
        # Validated BEFORE the per-version scan, not inside it. Inside, an artifact
        # with zero versions never reaches _satisfies, so a malformed ">=2.0" would
        # skip validation entirely and answer an authoritative no_match -- the
        # THIRD kind of nothing _satisfies exists to refuse, and indistinguishable
        # from a real ceiling.
        # "0" and not "": the probe must PARSE, so that only a malformed operand
        # raises. An unparseable probe version would reject ">=2" as well.
        _satisfies({"version": "0"}, requirement)
        matching = [v for v in versions if _satisfies(v, requirement)]
        if matching:
            return _ViewData(
                payload={"requirement": requirement},
                rows=matching,
                rows_key="versions",
            )
        # No match: return every version that EXISTS, not an empty list. An empty
        # list here is indistinguishable from an empty artifact, and that is the
        # confusion that creates duplicates.
        #
        # `highest_version` rides the FIXED-size payload rather than the rows,
        # because rows are what token_budget truncates: a tight budget could
        # otherwise emit state="no_match" with every version cut, promising a
        # ceiling the response no longer carries. The ceiling is the whole answer,
        # so it must survive truncation.
        numeric = [int(v["version"]) for v in versions if str(v.get("version", "")).isdigit()]
        return _ViewData(
            payload={
                "requirement": requirement,
                "satisfied_by": None,
                "highest_version": max(numeric) if numeric else None,
                "version_count": len(versions),
            },
            rows=versions,
            rows_key="versions",
            no_match=True,
        )

    def _view_versions(self, entity: dict, request: _Req) -> _ViewData:
        """Real, against the live registry: this view used to unconditionally
        report missing:["versioned_assets"] and had never been implemented."""
        return _ViewData(
            rows=self.source.experiment_versions(str(entity["id"])), rows_key="versions"
        )

    def _view_experiment_reproduce(self, entity: dict, request: _Req) -> _ViewData:
        """Per-run reproduction summaries across the experiment — a MAP, not N full
        assemblies. Each summary carries a ``reproduce_url`` for drill-down (via
        ``get_entity(view="reproduce")`` on the run), so this stays one cheap read
        regardless of run count. ``view_options={"version": N}`` pins against a frozen
        experiment_versions manifest; omitted reads live rows.

        Atomic + overflow-reported like the run view: the summaries are compact by
        construction, so this fits for any real experiment — and if it ever does not,
        ``get_entity`` reports ``token_budget_exceeded`` rather than dropping runs
        (a map with runs missing is a map that lies about which runs exist)."""
        version = request.filters.get("version")
        record = self.source.experiment_reproduce(
            str(entity["id"]), version=int(version) if version is not None else None
        )
        return _ViewData(payload=record)

    def _view_team_note_card(self, entity: dict, request: _Req) -> _ViewData:
        """The team note, WHOLE -- see its `_VIEWS` entry for why a card is the
        document here rather than a glance.

        The empty case gets words, deliberately: an
        agent reading a blank `body` cannot tell "this team has written nothing
        down" from "the read gave me nothing", and version 0 says which only to a
        reader who knows 0 is the sentinel. The explicit empty state conveys
        that distinction without repeating write instructions in read data.
        """
        if current_delivery() is not None:
            entity["body"] = pin_document(
                entity.get("body") or "", "team-note", version=entity.get("version")
            )
        if entity.get("body"):
            return _ViewData()
        return _ViewData(payload={"state": "empty"})

    @staticmethod
    def _transcript_int(filters: dict[str, Any], name: str, *, default: int, floor: int) -> int:
        """One transcript filter as an int, rejected loudly when it is not one.

        Coerced here rather than trusted: filters arrive as arbitrary JSON, and
        a string "3" silently comparing False against every int would make the
        filter a no-op wearing the caller's value -- the silent-ignore failure
        the _VIEW_OPTIONS table exists to prevent.
        """
        value = filters.get(name, default)
        if isinstance(value, bool) or not isinstance(value, int) or value < floor:
            raise errors.ValidationError(
                f"{name} must be an integer >= {floor}, got {value!r}",
                status=422,
            )
        return value

    def _view_session_transcript(self, entity: dict, request: _Req) -> _ViewData:
        """The transcript itself, in bounded line sections -- never whole.

        The backend returns ONE complete normalized document (the dashboard's
        read), so every narrowing here is client-side over content the call
        already paid for -- the same honesty class as the artifact
        `requirement` filter. Plain reads section the document from
        `start_line`; `grep` (literal, case-insensitive) returns one section
        per matching line with `context_lines` of surroundings, which is the
        "search within THIS session" read that chunk-ranked search_knowledge
        cannot promise. Either shape rides the ordinary rows machinery, so
        token_budget bounds what one response carries and the cursor walks the
        rest.
        """
        agent = entity.get("agent") or None
        try:
            doc = self.source.session_transcript(str(entity["id"]), agent=agent)
        except errors.NotFoundError as exc:
            context = current_delivery()
            if context and context.snapshot:
                raise source_changed("captured transcript is unavailable") from exc
            raise
        content = pin_document(
            doc.get("content") or "",
            f"transcript:{entity['id']}:{doc.get('agent') or agent or ''}",
        )
        # split on "\n" ONLY. str.splitlines() also breaks on \r, \f, NEL, and
        # U+2028/9 -- ordinary bytes inside captured terminal output and code
        # blocks -- which would (a) renumber lines away from the backend's own
        # \n counting, so a `line`/`start_line` coordinate points at different
        # text on the dashboard, and (b) drop those bytes from the rejoined
        # section, corrupting what is meant to be an exact-content read.
        lines = content.split("\n")
        total = len(lines)
        payload: dict[str, Any] = {
            "agent": doc.get("agent"),
            "title": doc.get("title"),
            "total_lines": total,
            "body_size_bytes": (
                len(content.encode("utf-8")) if current_delivery() else doc.get("body_size_bytes")
            ),
            "filters": request.filters or None,
        }
        # Build ONLY the caller's window (offset + one page) plus a lookahead,
        # never a section per 40 lines of the whole document: a multi-MB
        # transcript is tens of thousands of sections, each re-joining its lines
        # into a second full copy of the content, and _fit emits a handful. The
        # per-page re-fetch of the whole document stays (the backend transcript
        # route has no line-range parameter) -- TODO(backend): a start_line/limit
        # query would make a full walk linear instead of O(pages * doc), the same
        # shape as the _bounded() span-walk TODO.
        window = request.offset + _PAGE_FETCH
        grep = request.filters.get("grep")
        if grep is None:
            if "context_lines" in request.filters:
                # Accepted-but-inert is the lie the filter table guards against,
                # one key at a time.
                raise errors.ValidationError(
                    "context_lines only applies together with grep", status=422
                )
            start = self._transcript_int(request.filters, "start_line", default=1, floor=1)
            starts = range(start, total + 1, _TRANSCRIPT_SECTION_LINES)
            rows = [
                {
                    "line_start": a,
                    "line_end": min(total, a + _TRANSCRIPT_SECTION_LINES - 1),
                    "text": "\n".join(lines[a - 1 : a + _TRANSCRIPT_SECTION_LINES - 1]),
                }
                for a in starts[:window]
            ]
            return _ViewData(
                payload=payload,
                rows=rows,
                rows_key="sections",
                more_beyond=len(starts) > window,
            )
        if not isinstance(grep, str) or not grep:
            # An empty needle matches EVERY line ("" in s is always True), i.e. a
            # request to read the whole transcript wearing a search's clothes,
            # and a list/dict would str()-coerce into a surprising literal. Both
            # are caller errors, refused rather than answered.
            raise errors.ValidationError(
                "grep must be a non-empty string: to read the whole transcript "
                "omit grep and page the sections instead",
                status=422,
            )
        if "start_line" in request.filters:
            # Symmetric with the context_lines-without-grep guard above:
            # start_line is a plain-read control the grep scan never consults, so
            # accepting it beside grep is the accepted-but-inert lie again.
            raise errors.ValidationError(
                "start_line applies to a plain read, not to grep (grep scans the "
                "whole transcript); pass one or the other",
                status=422,
            )
        context = self._transcript_int(
            request.filters, "context_lines", default=_TRANSCRIPT_CONTEXT_DEFAULT, floor=0
        )
        context = min(context, _TRANSCRIPT_CONTEXT_MAX)
        needle = grep.lower()
        rows = []
        more = False
        for n, line in enumerate(lines, start=1):
            if needle in line.lower():
                if len(rows) >= window:
                    # One match past the window is all it takes to know there is
                    # more; stop rather than scanning (and section-joining) the
                    # rest of a large transcript for rows this page cannot carry.
                    more = True
                    break
                a, b = max(1, n - context), min(total, n + context)
                rows.append(
                    {
                        "line": n,
                        "line_start": a,
                        "line_end": b,
                        "text": "\n".join(lines[a - 1 : b]),
                    }
                )
        # no_match: the whole document was scanned and no line contains the
        # needle -- an answer, with total_lines as its denominator, distinct from
        # a page that filled and left more behind (more_beyond).
        return _ViewData(
            payload=payload,
            rows=rows,
            rows_key="sections",
            more_beyond=more,
            no_match=not rows,
        )

    # -- coordinate reads (below-run coordinates, 0059-0062) -----------------

    def metrics_grouped(
        self,
        run_id: str,
        key: str,
        *,
        kind: str | None = None,
        agg: str | None = None,
        by: list[str] | None = None,
        where: dict[str, Any] | None = None,
        step_bucket: int | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        max_rows: int | None = None,
    ) -> dict:
        """One bounded server-side reduction. ``max_rows`` clamps to the tool's
        row bound — grouped cells are aggregates, so the clamp cuts pathology,
        not typical reads — and a cut read reports partial with the resume step
        in ``next_cursor``."""
        bound = min(max_rows or _GROUPED_ROWS_DEFAULT, _GROUPED_ROWS_MAX)
        payload = self.source.run_metrics_grouped(
            run_id,
            key,
            kind=kind,
            agg=agg,
            by=by,
            where=where,
            step_bucket=step_bucket,
            step_from=step_from,
            step_to=step_to,
            max_rows=bound,
        )
        missing = [MissingMarker.ROWS_BEYOND_PAGE_BOUND] if payload.get("truncated") else []
        next_step = payload.get("next_step")
        return self._envelope(
            {"run_id": run_id, **payload},
            state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
            missing=missing,
            next_cursor=str(next_step) if missing and next_step is not None else None,
        )

    def run_coordinates(self, run_id: str) -> dict:
        """The coordinate catalog is bounded by the series cap's cardinality
        arithmetic (no pagination on the route), so this is one complete read."""
        return self._envelope(
            {"run_id": run_id, "coordinates": self.source.run_coordinates(run_id)}
        )

    def metrics_export(
        self,
        run_id: str,
        *,
        key: str | None = None,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        after_id: int | None = None,
        limit: int | None = None,
    ) -> dict:
        """ONE keyset page of the lossless export. The SDK generator would follow
        the walk to the last point; a tool response cannot, so the page is sliced
        off it here and the cursor handed back as ``next_cursor`` (pass it back
        as ``after_id``)."""
        bound = max(1, min(limit or _EXPORT_PAGE_DEFAULT, _EXPORT_PAGE_MAX))
        filters = {
            name: value
            for name, value in {
                "key": key,
                "kind": kind,
                "step_from": step_from,
                "step_to": step_to,
                "after_id": after_id,
            }.items()
            if value is not None
        }
        walk = self.source.export_points(run_id, limit=bound, **filters)
        # Lookahead past the page bound, so "more points exist" is a fact rather
        # than an inference from a full page (the _bounded contract).
        points = list(islice(walk, bound + 1))
        more = len(points) > bound
        points = points[:bound]
        return self._envelope(
            {"run_id": run_id, "filters": filters or None, "points": points},
            state=EnvelopeState.PARTIAL if more else EnvelopeState.COMPLETE,
            missing=[MissingMarker.ROWS_BEYOND_PAGE_BOUND] if more else [],
            next_cursor=str(points[-1]["id"]) if more else None,
        )

    def research_compare(
        self,
        refs: list[str],
        dimensions: list[str] | None = None,
    ) -> dict:
        if len(refs) < 2:
            raise ValueError("compare requires at least two refs")
        rows = []
        for ref in refs:
            kind, entity = self.source.get(ref)
            rows.append({"ref": ref, "entity_type": kind, "entity": entity})
        requested = dimensions or ["config", "metadata", "summary", "status", "question"]
        comparison = {
            dimension: [row["entity"].get(dimension) for row in rows] for dimension in requested
        }
        return self._envelope({"entities": rows, "comparison": comparison})
