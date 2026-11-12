"""the team's corpora: /v1/search's exact and semantic channels shaped into hits, interleaved and collapsed."""

from __future__ import annotations
from typing import Any
from ....shared.reads.search_contract import (
    BackendCorpus,
    Channel,
    ChannelError,
    EntityType,
    MatchMode)


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
    default Jev selector scores passages without writing a reason, and a hit
    the raw pool answered with (`recall_floor`) was never read by a model.
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


#: The engine's "no author" sentinel; an older server passes it through.
_UNKNOWN_AUTHOR = "unknown"


def _read_github_author(row: dict) -> str | None:
    """The GitHub login that wrote a GitHub hit, else None. Only GitHub: other
    sources' author ids are opaque (a Slack uid, a user uuid) and name no one a
    reader can recognise. A login names a person, never a session."""
    if BackendCorpus.GITHUB not in (row.get("corpus"), row.get("source_system")):
        return None
    author = row.get("author_id")
    if not isinstance(author, str) or author.strip() in ("", _UNKNOWN_AUTHOR):
        return None
    return author.strip()


def _semantic_result(row: dict, *, keyword: bool = False) -> dict:
    """A semantic-channel document hit (engine) in the tool's result shape.

    `keyword` labels a hit the backend's keyword search found (BM25, no model):
    same card, `why_matched` says `keyword` so it is never read as a meaning match.

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
    author = _read_github_author(row)
    if author:
        card["author"] = author
    return {
        "entity_type": kind or EntityType.DOCUMENT,
        **({"id": entity_id} if kind else {}),
        "card": card,
        "why_matched": _why_matched(
            MatchMode.KEYWORD if keyword else MatchMode.SEMANTIC,
            Channel.KEYWORD if keyword else Channel.SEMANTIC,
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
