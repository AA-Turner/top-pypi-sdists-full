"""find_papers: search, read or expand the literature through the web door, with honest completeness."""

from __future__ import annotations
from typing import Any
from ....sdk import errors
from ....shared.reads.search_contract import (
    EnvelopeState,
    MissingMarker,
    WebState)


class LiteratureMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

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
