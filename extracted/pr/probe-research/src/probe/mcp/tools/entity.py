"""get_entity: resolve one entity, run its view's builder, page the result whole under the token budget."""

from __future__ import annotations
import hashlib
from typing import Any
from ...sdk import errors
from ...sdk.reads import links
from ..delivery import accounting
from ...foundation.token_budget.token_budget import MIN_TOKENS as _MIN_TOKEN_BUDGET
from ...foundation.token_budget.token_budget import MAX_TOKENS as _MAX_TOKEN_BUDGET
from ...foundation.token_budget.token_budget import Budget
from ...shared.reads.search_contract import (
    EntityType,
    EnvelopeState,
    MissingMarker)
from ..generated.views import View
from ..delivery.delivery import ContinuationError
from ..delivery.delivery import encode as _encode_delivery_cursor
from ..delivery.delivery import omit_defaults
from ..delivery.context import current_delivery, source_changed
from ..source.catalog import CATALOG_NO_MATCH
from probe.mcp.tools.shaping.cards import _CARD_DESCRIPTION_CHARS, _entity_projection
from probe.mcp.tools.shaping.cursors import _join_get_cursor, _split_get_cursor, _stand_in_request
from probe.mcp.tools.shaping.shaping import _fit, _tokens
from probe.mcp.tools.view import _Req, _VIEWS, _ViewData, _supported_views
from probe.mcp.tools.views.files import _PAGE_FETCH
#: The kinds a coding-agent session creates, and so the kinds with an intent.
_INTENT_KINDS = frozenset({EntityType.RUN, EntityType.EXPERIMENT, EntityType.PROJECT})
_INTENT_CARD_FIELDS = (
    "ask", "ask_truncated", "match", "context", "session_goal", "queued",
    "asked_by_name", "asked_at", "session", "step_id", "provisional",
)


class GetEntityMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    # -- research_get --------------------------------------------------------

    def _card_intent(self, kind: str, entity: Any, hide_session: str | None) -> dict | None:
        """Why the entity was started, in the researcher's words: the ask from
        the session that created it (`GET /v1/intent`). `match: approximate`
        is candidate context, not a claim. Omitted when unknown, and when it
        comes from the caller's own hidden session (the daemon's reader)."""
        if kind not in _INTENT_KINDS or not isinstance(entity, dict) or not entity.get("id"):
            return None
        reader = getattr(self.source, "intent", None)
        if reader is None:
            return None
        found = reader(kind, str(entity["id"]))
        if not isinstance(found, dict) or not found.get("ask"):
            return None
        session = found.get("session")
        if hide_session is not None and isinstance(session, str) and session.split("/", 1)[-1] == hide_session:
            return None
        return {key: found[key] for key in _INTENT_CARD_FIELDS if found.get(key) is not None}

    def _card_blurb(self, kind: str, entity: Any) -> str | None:
        """The Overview page's one-line summary for a project or experiment card,
        read through the page's own read (`project_overview`), so a page the
        caller would be refused -- written over a family with a project hidden
        from them -- yields nothing here either (`_saved_overview`). Enrichment
        only: any failure omits it."""
        if kind not in (EntityType.PROJECT, EntityType.EXPERIMENT) or not isinstance(entity, dict):
            return None
        if not entity.get("id"):
            return None
        try:
            if kind == EntityType.PROJECT:
                page = self.source.project_overview(str(entity["id"]))
            else:
                page = self.source.experiment_overview(
                    str(entity["id"]),
                    project_id=entity.get("project_id") or entity.get("parent_project_id"),
                )
            saved = self._saved_overview(page).payload["overview"]
        except Exception:  # enrichment only: never a reason the card fails
            return None
        blurb = saved.get("blurb")
        if not isinstance(blurb, str) or not blurb.strip():
            return None
        return blurb.strip()[:_CARD_DESCRIPTION_CHARS]

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
        offset, after = _split_get_cursor(cursor, view)
        options = self._checked_view_options(kind, view, filters)
        # `X-Probe-Hide-Session-Work` (the daemon's reader): the entity asked for
        # is shown, but the rows, edges and origins in its view that name work the
        # caller's own session created are not -- after browse, a prior project's
        # lineage is where the session's new experiments and runs would surface.
        # The created set is read ONCE and AFTER the view's own reads (the set is
        # then a superset of the work they could show): by the view when it hides
        # that work itself (`_Req.hidden`), else here, after the builder.
        hide_session = accounting.session_work_to_hide()
        own_id = str(entity.get("id")) if isinstance(entity, dict) else None
        read_once: list[tuple[frozenset[str], bool] | None] = []

        def created() -> tuple[frozenset[str], bool] | None:
            if hide_session is None:
                return None
            if not read_once:
                read_once.append(self._session_created_ids(hide_session))
            return read_once[0]

        def hidden() -> frozenset[str] | None:
            ids = created()
            return ids[0] if ids is not None and (own_id or "").lower() not in ids[0] else None

        request = _Req(
            filters=options,
            offset=offset,
            after=after,
            ref=ref,
            token_budget=token_budget,
            hidden=hidden,
        )
        if isinstance(entity, dict) and CATALOG_NO_MATCH in entity:
            # Whichever view was asked, the version it names does not exist:
            # the answer is the same no_match, carrying the versions that do.
            result = self._catalog_no_match(entity)
        else:
            result = getattr(self, _VIEWS[(kind, view)])(entity, request)
        if hide_session is not None:
            result = self._without_session_work(result, created(), own_id=own_id)

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
            intent = self._card_intent(kind, entity, hide_session)
            if intent:
                data["intent"] = intent
            blurb = self._card_blurb(kind, entity)
            if blurb:
                data["blurb"] = blurb
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
            if (result.resume_key or result.exact_fit) and (
                _MIN_TOKEN_BUDGET <= token_budget <= _MAX_TOKEN_BUDGET
            ):
                emitted = self._fit_resume_rows(
                    view, data, window, result, missing, token_budget, offset=request.offset
                )
            else:
                emitted = _fit(window, max(0, token_budget - _tokens(data)))
            data[result.rows_key] = emitted
            budget_cut = len(emitted) < len(window)
            rows_exhausted = not budget_cut and not result.more_beyond
            if (budget_cut or result.more_beyond) and result.resume_key:
                # Resume on the route's own cursor, after the last row SENT --
                # or, having sent none, from where this page itself began; but
                # past the last row FETCHED when filtering left nothing to send.
                if emitted:
                    route_after = str(emitted[-1].get(result.resume_key))
                elif not window and result.resume_fetched:
                    route_after = result.resume_fetched
                else:
                    route_after = request.after
                next_cursor = _join_get_cursor(view, 0, after=route_after)
            elif budget_cut or result.more_beyond:
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
    def _fit_resume_rows(
        view: str,
        data: dict[str, Any],
        window: list[dict],
        result: _ViewData,
        missing: list[str],
        token_budget: int,
        *,
        offset: int = 0,
    ) -> list[dict]:
        """As many WHOLE rows of a `resume_key` view as the delivered page holds,
        measured EXACTLY -- the compact envelope, its markers, and the cursor
        delivery will wrap around the last row's key -- as `metrics_series`
        measures its series. An `exact_fit` view's cursor is the offset past
        the last row sent (`offset` is where this page began).

        Its cursor carries that KEY (a diff carries a path), so it grows with
        the rows, and the chars/4 estimate other views fit on undercounts
        path-like text badly. Fitted that way, every page of long paths
        overflowed once the cursor landed and went out as fragments: 29 calls
        for 60 entries of 250-character paths where an offset cursor took 22.
        One row is always sent; one too big alone is fragmented by delivery."""
        budget = Budget(token_budget)
        request_id = _stand_in_request(hashlib.sha256(b"resume-cursor-stand-in").hexdigest()[:32])

        def page(count: int) -> dict:
            rows = window[:count]
            more = count < len(window) or result.more_beyond
            native = (
                _join_get_cursor(view, 0, after=str(rows[-1].get(result.resume_key)))
                if result.resume_key and rows
                else _join_get_cursor(view, offset + count)
            )
            cursor = (
                _encode_delivery_cursor({"native": native}, request_id)
                if more and rows
                else None
            )
            marked = [*missing]
            if count < len(window):
                marked.append(MissingMarker.TRUNCATED_BY_TOKEN_BUDGET)
            return omit_defaults(
                {
                    "data": {**data, result.rows_key: rows},
                    "completeness": {
                        "state": EnvelopeState.PARTIAL if marked else EnvelopeState.COMPLETE,
                        "missing": marked,
                    },
                    "next_cursor": cursor,
                }
            )

        # Room a multi-ref batch's row wrapper takes around this page.
        context = current_delivery()
        reserve = context.reserve if context is not None else 0

        def fits(count: int) -> bool:
            try:
                return budget.fits(page(count), reserve=reserve)
            except ContinuationError:
                # A cursor too large to encode (one very long path as the
                # last row) cannot end a page; a shorter page may still fit.
                return False

        low, high, kept = 1, len(window), min(1, len(window))
        while low <= high:
            mid = (low + high) // 2
            if fits(mid):
                kept, low = mid, mid + 1
            else:
                high = mid - 1
        return window[:kept]

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
