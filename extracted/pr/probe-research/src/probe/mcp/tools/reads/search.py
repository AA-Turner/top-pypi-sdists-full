"""search: ranked retrieval across the corpora search_in names, collapsed per experiment, fitted whole to the budget."""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from ....sdk import errors
from ...delivery import accounting
from ....foundation.token_budget.token_budget import MIN_TOKENS as _MIN_TOKEN_BUDGET
from ....foundation.token_budget.token_budget import MAX_TOKENS as _MAX_TOKEN_BUDGET
from ....foundation.token_budget.token_budget import Budget
from ....shared.reads.search_contract import (
    BackendRetrieval,
    BackendSearchState,
    Channel,
    ChannelError,
    CollapseMode,
    EntityType,
    EnvelopeState,
    MissingMarker,
    SearchSort,
    ToolCorpus,
    is_docs_only)
from probe.mcp.tools.corpora.team import (
    _collapse_experiments,
    _exact_result,
    _in_project,
    _interleave,
    _section,
    _semantic_result,
)
from probe.mcp.tools.corpus import NON_BACKEND_CORPORA, _map_search_in
from probe.mcp.tools.shaping.cursors import _join_cursor, _split_cursor
from probe.mcp.tools.shaping.people import get_owner_echo
from probe.mcp.tools.shaping.shaping import _fit_whole_results
from probe.mcp.tools.view import _supported_views

# Backend caps top_k / exact_limit.
_BACKEND_CHANNEL_CAP = 50

#: Said on a project-scoped search naming `transcripts`: project scope keeps only hits resolving to
#: the project, a transcript (keyless connector document) resolves to none, so every transcript hit
#: is dropped before ranking. Silence read as "no session mentioned it"; the sessions view plus a
#: per-transcript grep is exact and fully scoped.
_TRANSCRIPTS_NOT_PROJECT_SCOPED = (
    "transcripts are not project-scoped: a project_id search drops every transcript hit. "
    "For a project's sessions use entity view=sessions on the project (newest first), "
    "then entity view=transcript on a session with view_options.grep."
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
    # Absence = UNSUPPORTED, not assent: the silent failure (tenant-wide results wearing
    # state="complete") is the one that matters.
    return str(response.get("project_id") or "") == str(project_id)


def _get_written_at(row: Any) -> tuple[bool, datetime]:
    """A hit's `updated_at` as a sort key, `(False, min)` when it has none or it does not parse."""
    value = row.get("updated_at") if isinstance(row, dict) else None
    try:
        moment = datetime.fromisoformat(str(value).replace("Z", "+00:00")) if value else None
    except ValueError:
        moment = None
    if moment is None:
        return False, datetime.min.replace(tzinfo=timezone.utc)
    return True, moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


class SearchMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def search(
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
        token_budget: int = 2000,
        semantic: bool = True,
        owner: str | None = None,
        since: str | None = None,
        until: str | None = None,
        sort: str | None = None,
    ) -> dict:
        """Ranked retrieval across the lab.

        `owner`, `since`, `until` and `sort="recent"` go to the backend as given (it matches the
        person and reads the dates); who `owner` matched rides the answer as `owner_matched`.

        `semantic=False` is the keyword search: the exact channel plus BM25 over
        document text (`retrieval="keyword"` on the backend), with no model call
        anywhere on the path. Its content hits are labelled `keyword`, never
        `semantic`, and a backend that did not echo the mode is marked rather
        than trusted (`keyword_search_unsupported`).

        Called `search_knowledge` until 2026-10-08, along with a `curated_only`
        no-op that nothing sent; the tool was renamed outright.

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
        # Typed CollapseMode so the vocabulary ships in the schema; this check guards DIRECT Python
        # callers, whom nothing validates. Both spellings compare equal (StrEnum is a str). `none` and
        # null are one request: no dedupe.
        if collapse == CollapseMode.NONE:
            collapse = None
        if collapse is not None and collapse != CollapseMode.EXPERIMENT:
            raise errors.ValidationError(
                f'unknown collapse value {collapse!r}: pass "experiment" or "none"',
                status=422,
            )
        # Read before `semantic` is rebound to the response section below.
        keyword = not semantic
        # `relevance` is the backend's default: left off, so an unfiltered search's body is unchanged.
        people = {
            "owner": owner or None,
            "since": since or None,
            "until": until or None,
            "sort": SearchSort.RECENT.value if sort == SearchSort.RECENT else None,
        }
        asked = [name for name, value in people.items() if value]
        if asked and search_in and any(value in NON_BACKEND_CORPORA for value in search_in):
            # Probe's docs have no owner or date: beside filtered team hits they would read as filtered too.
            raise errors.ValidationError(
                f"{', '.join(asked)} filter the team's own record; Probe's docs (search_in \"docs\") "
                "have no owner or date. Take docs out of search_in, or leave the filters out.",
                status=422,
            )
        if asked:
            self.source.require_people_filters(asked, is_search=True)
        # Probe's docs are not the team's record and POST /v1/search does not hold them: they split off
        # HERE, before `_map_search_in` (NON_BACKEND_CORPORA). Docs alone never reach team search; mixed,
        # the team corpora are searched as ever and the docs ride beside them.
        if is_docs_only(search_in):
            return self._search_docs_only(
                query, top_k=top_k, token_budget=token_budget, verbose=verbose, cursor=cursor
            )
        docs_asked = bool(search_in) and any(v in NON_BACKEND_CORPORA for v in search_in)
        if docs_asked:
            search_in = [v for v in search_in if v not in NON_BACKEND_CORPORA]
        corpus, unsupported = _map_search_in(search_in)
        exact_cursor, semantic_cursor = _split_cursor(cursor)
        if keyword and semantic_cursor is not None:
            # A cursor from a semantic=true search: the keyword lookup cannot resume it. Said in this tool's
            # words; the backend's refusal names `semantic_cursor`, which the caller never saw.
            raise errors.ValidationError(
                "this cursor continues a semantic=true search: pass semantic=true to "
                "continue it, or start a new keyword search without a cursor",
                status=422,
            )
        # The keyword lookup returns no cursor, so a later page would repeat page one's keyword hits as
        # new. A keyword continuation pages the exact channel alone.
        keyword_page = keyword and cursor is None
        # `top_k` is a TOTAL, so each channel is asked for all of it. Splitting per channel made
        # `top_k=8` fetch 4 semantic + 4 exact rows, and exact is empty on most searches: a default
        # search showed four results and called it eight. Cost: rows can be left over after the
        # merge, which per-channel cursors (advancing by what was FETCHED) cannot describe. So a
        # response with leftovers returns no cursor and says `results_beyond_budget`: a cursor that
        # skips unseen rows is worse than an honest "there is more".
        per_channel = max(1, min(top_k, _BACKEND_CHANNEL_CAP))
        # NO keyword fallback. It served backends predating POST /v1/search, which the MCP never
        # reaches (hosted only, see source.capabilities()). Keeping it forced a scoped 404 to be
        # blamed on the scope without asking the server, which made the fallback unreachable for
        # every scoped call and left a workspace guard that could not fire: half a fallback reads
        # as a safety net covering only unscoped calls. A truly absent route now surfaces as
        # CapabilityUnavailable, not a silently-empty keyword answer.
        # WHO IS CALLING, for self-exclusion; the explicit source wins (D5).
        # The HEADER `X-Probe-Agent-Session` is the ambient default (free, cannot be forgotten) but
        # absent for most callers: Codex connects its MCP before a thread id exists, and 3,282 of
        # 3,304 hosted calls over 30 days carried no agent label.
        # The PARAMETER covers that gap (a Codex shell sees CODEX_THREAD_ID). An explicit value
        # overrides the header, not merges: naming a session says something specific.
        ambient = accounting.calling_agent_session()
        exclude_agent_session = exclude_session or (ambient[1] if ambient else None)
        # The session's own WORK, not just its conversation: only for a caller that opted in with
        # `X-Probe-Hide-Session-Work` (the daemon's reader), and always its AMBIENT session, never the
        # model-supplied `exclude_session`. Everyone else sends the request they always sent.
        exclude_origin_session = accounting.session_work_to_hide()
        # The API records WHICH session searched (`search_performed`) from the request's session
        # headers; hosted, they name the caller only when bound here, else this server's own.
        with accounting.caller_session_scope():
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
                exclude_origin_session=exclude_origin_session,
                # Omitted for a semantic search: its body stays byte-identical to earlier clients'.
                retrieval=BackendRetrieval.KEYWORD.value if keyword_page else None,
                include_semantic=False if keyword and not keyword_page else None,
                **people,
            )
        exact = _section(response, Channel.EXACT)
        semantic = _section(response, Channel.SEMANTIC)
        scoped_server_side = project_id is None or _echoes_project_scope(response, project_id)
        if not scoped_server_side:
            # The backend did not confirm the scope. SearchRequest allows extra body fields, so a server
            # predating server-side project scope ignores `project_id` and returns TENANT-WIDE
            # results with no marker: worse than any error. Degrade, do not refuse (that would drop a
            # working capability): the exact channel carries project_id per row and is narrowed here;
            # the semantic channel cannot be, so it is EMPTIED and marked, not passed through unscoped.
            exact["results"] = [row for row in exact["results"] if _in_project(row, project_id)]
            semantic = {
                "results": [],
                "cursor": None,
                "error": ChannelError.PROJECT_SCOPE_UNSUPPORTED,
                "total_candidates": None,
                "active_runs_count": None,
            }
        # Project scope is SERVER-SIDE now (research-os #103): the backend re-resolves semantic hits
        # against live rows and over-fetches so the filter runs before the cap. The old client path
        # emptied the semantic channel and reported project_scope_unsupported (trigram-only).
        # Keyword hits say so, unless the backend did not run a keyword search: an older backend ignores
        # `retrieval` and answers with the full search, whose hits ARE semantic.
        raw_semantic = response.get(Channel.SEMANTIC.value) if isinstance(response, dict) else None
        keyword_ran = keyword_page and (
            isinstance(raw_semantic, dict)
            and raw_semantic.get("retrieval") == BackendRetrieval.KEYWORD
        )
        merged = _interleave(
            [(_exact_result(row), row) for row in exact["results"]],
            [(_semantic_result(row, keyword=keyword_ran), row) for row in semantic["results"]],
        )
        if people["sort"]:
            # Newest first across BOTH channels (D16): a round-robin would put an old exact hit
            # above a newer semantic one and cut the newer at `top_k`. Undated hits go last.
            merged.sort(key=lambda pair: _get_written_at(pair[1]), reverse=True)
        results = [hit for hit, _ in merged]
        if collapse == EntityType.EXPERIMENT:
            results = _collapse_experiments(results)
        # `top_k` is a TOTAL, so the merge applies it; both channels were asked for all of it.
        fetched = len(results)
        results = results[:top_k]
        missing, semantic_lost = self._collect_search_gaps(
            exact=exact, exclude_agent_session=exclude_agent_session,
            exclude_origin_session=exclude_origin_session, keyword_page=keyword_page,
            keyword_ran=keyword_ran, raw_semantic=raw_semantic, response=response, results=results,
            semantic=semantic, unsupported=unsupported,
        )
        backend_ok = isinstance(response, dict) and response.get("state") == BackendSearchState.OK
        # CLAMPED, not validated: the tool surface constrains this (ge=512, le=8000) but Python callers
        # get no validation, and the graceful answer to "600000" is the biggest legal budget, not a traceback.
        budget = Budget(max(_MIN_TOKEN_BUDGET, min(int(token_budget), _MAX_TOKEN_BUDGET)))
        # Docs beside the team's results: FIRST page only (a cursor page continues the team's channels,
        # not the docs), in at most half the budget, measured inside `_payload` so team cards get the rest.
        docs_hits: list[dict] | None = None
        docs_note: str | None = None
        if docs_asked and not cursor:
            docs_hits, docs_note, docs_read, docs_left_out = self._docs_beside_team(
                query, top_k, budget, verbose=verbose
            )
            if not docs_read:
                missing.append(MissingMarker.DOCS)
            if docs_left_out:
                missing.append(MissingMarker.RESULTS_BEYOND_BUDGET)

        def _payload(rows: list[dict], budget_note: dict | None) -> dict:
            data: dict[str, Any] = {
                "query": query,
                # Who `owner` matched, so a wrong match is seen (D4).
                **get_owner_echo(response),
                "collapse": collapse,
                "results": rows,
                "channels": {
                    Channel.EXACT.value: {"error": exact["error"]},
                    # `lost_channels`: the engine's OWN dead channels ("bm25", "vector", "graph",
                    # "inferred_edge") on an otherwise successful semantic response. Emitted only
                    # when non-empty, keeping a healthy search's block as small as ever.
                    Channel.SEMANTIC.value: {
                        "error": semantic["error"],
                        # Emitted only when non-empty / non-default (healthy blocks stay small).
                        **({"lost_channels": semantic_lost} if semantic_lost else {}),
                        # WHY the answer is degraded, beside the marker saying THAT: "loop_timeout" and
                        # "schema_violation" call for different reactions.
                        **(
                            {"degraded_reason": semantic["degraded_reason"]}
                            if semantic.get("degraded") and semantic.get("degraded_reason")
                            else {}
                        ),
                        # How the engine graded what it returned: EXTRACTED (deterministic) vs INFERRED vs AMBIGUOUS.
                        **(
                            {"confidence_breakdown": semantic["confidence_breakdown"]}
                            if semantic.get("confidence_breakdown")
                            else {}
                        ),
                    },
                },
                # The recall hint the instructions tell the agent to check before concluding the lab has not
                # tried something. It was instructed in two places and returned in none, so the agent
                # gave up the check or invented a number. None on backends that do not report it.
                "total_candidates": semantic.get("total_candidates"),
                "active_runs_count": exact.get("active_runs_count"),
                "unsupported_values": unsupported,
            }
            if project_id is not None and (
                not search_in or ToolCorpus.TRANSCRIPTS in search_in
            ):
                # Said, not marked: the search RAN and its other corpora are right; the caller asked
                # something of transcripts it cannot do. Omitted `search_in` asks for EVERY corpus
                # (`_map_search_in`), transcripts included, so the silence would be the same.
                data["note"] = _TRANSCRIPTS_NOT_PROJECT_SCOPED
            if docs_hits is not None:
                data["docs"] = docs_hits
                if docs_note:
                    data["docs_note"] = docs_note
            if budget_note:
                data["budget"] = budget_note
            # The view vocabulary, for hits an agent can open. SEARCH IS THE LAST RUNG and was the only
            # route to an address with no views: browse and card carry `available_views`, so an agent
            # on the cheap step knew what to ask and one on the expensive step did not. Keyed by kind,
            # once per response (as browse does), not per hit. Terminal hits fall out free:
            # `_supported_views` answers [] for a document or file, and entity has no route for them.
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
                # A cursor ONLY when every fetched row shipped: per-channel cursors advance by what was
                # fetched, so one after dropping rows for budget would skip the rows paged for.
                next_cursor=(
                    _join_cursor(exact["cursor"], semantic["cursor"])
                    if len(rows) == fetched
                    else None
                ),
                verbose=verbose,
            )

        # Mixed, the team's budget hints (`fits_all_at_token_budget`, `min_token_budget`) are measured
        # with the docs list as packed at THIS budget's half share, not the budget they name.
        return _fit_whole_results(results, _payload, budget, available=fetched)


    def _collect_search_gaps(
        self, *, exact, exclude_agent_session, exclude_origin_session, keyword_page, keyword_ran,
        raw_semantic, response, results, semantic, unsupported,
    ):
        """What this search could not do, as missing markers, and the semantic channels it lost."""
        missing = []
        if exclude_agent_session is not None and semantic.get("exclusion_applied") is not True:
            # Asked, not echoed: the server predates the field and ignored it (SearchRequest permits extra
            # body fields), so the caller's own session is STILL in these results. Say so.
            missing.append(MissingMarker.SELF_EXCLUSION_UNSUPPORTED)
        elif (
            exclude_agent_session is not None
            and not results
            and not exact["error"]
            and not semantic["error"]
            and (semantic.get("excluded_count") or 0) > 0
        ):
            # The search RAN and every surviving row was the caller's own conversation: a STOP, not a
            # degradation (rewording cannot yield another corpus). Guarded on total_candidates so a
            # genuinely empty corpus stays an ordinary empty result.
            missing.append(MissingMarker.ALL_RESULTS_WERE_OWN_SESSION)
        if exclude_origin_session is not None and not (
            isinstance(response, dict) and response.get("origin_exclusion_applied") is True
        ):
            # Same shape as the transcript exclusion: asked, not echoed, so the session's own projects and runs are still here.
            missing.append(MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED)
        if exact["error"]:
            missing.append(MissingMarker.EXACT_SEARCH)
        if semantic["error"]:
            missing.append(MissingMarker.SEMANTIC_SEARCH)
        # The semantic channel answered but lost one of ITS channels. Marked apart from SEMANTIC_SEARCH:
        # an empty channel is visibly broken, thinned results look complete. Absent on an older
        # backend -> no marker -> healthy, the safe direction in a rolling deploy.
        semantic_lost = [c for c in (semantic.get("lost_channels") or []) if isinstance(c, str)]
        if semantic_lost:
            missing.append(MissingMarker.SEMANTIC_CHANNEL_DEGRADED)
        # Channels all alive, ANSWER still degraded. The engine reported this for months while this
        # boundary dropped it, so every fallback answer looked healthy to the agent.
        if semantic.get("degraded"):
            missing.append(MissingMarker.SEMANTIC_ANSWER_DEGRADED)
        if keyword_page and not keyword_ran:
            # Asked for keyword and the backend did not say it ran one: it predates the field and answered with the full search.
            missing.append(MissingMarker.KEYWORD_SEARCH_UNSUPPORTED)
        if keyword_ran and isinstance(raw_semantic, dict) and raw_semantic.get("more_candidates"):
            # The bounded keyword lookup matched more than it returned: an absent document is not evidence of absence.
            missing.append(MissingMarker.KEYWORD_MATCHES_BEYOND_BACKEND_LIMIT)
        if unsupported:
            missing.append(MissingMarker.KB_VALUES)
        if isinstance(response, dict) and (response.get("dropped_result_count") or 0) > 0:
            # The backend dropped whole DOCUMENTS to fit a size budget: absence is NOT evidence of absence,
            # and a caller that cannot see the trim reads a short set as complete.
            # Keyed on dropped RESULTS, not `truncated`: that also counts dropped chunk text a card
            # never carries, and marked 77 of 2,942 searches (30 days to 2026-10-02) partial for text
            # this tool discards. This tool sends no byte budget, so today it fires only if that changes.
            missing.append(MissingMarker.TRUNCATED_BY_RESPONSE_BUDGET)
        return missing, semantic_lost
