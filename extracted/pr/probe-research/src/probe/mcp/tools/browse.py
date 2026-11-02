"""browse mode=tree: what exists, annotated with kind, slug, uuid and dashboard link, minus the caller's own session work."""

from __future__ import annotations
from dataclasses import replace as dataclass_replace
from typing import Any
from ...sdk import errors
from ...sdk.reads import links
from ..delivery import accounting
from ...shared.reads.search_contract import (
    EntityType,
    EnvelopeState,
    MissingMarker)
from probe.mcp.tools.shaping.session_work import _scrub_provenance_graph, _scrub_session_work
from probe.mcp.tools.view import _ViewData, _supported_views


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
    unknown (see sdk.reads.links) -- an absent key says "say nothing", which is what
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


class BrowseMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

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
        # search. None for everyone else: the same request as ever.
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

    @staticmethod
    def _without_session_work(
        result: _ViewData, created: tuple[frozenset[str], bool] | None, *, own_id: str | None
    ) -> _ViewData:
        """`result` with every row, edge and origin naming work the caller's
        session created (`created`, `_session_created_ids`) taken out -- except
        the entity the caller asked for by address. Marked
        `session_work_exclusion_unsupported` when the created set could not be
        read, or was cut at its cap: the view may still hold that work."""
        if created is None:
            return dataclass_replace(
                result,
                missing=list(
                    dict.fromkeys(
                        [*result.missing, MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED]
                    )
                ),
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
            payload=_scrub_session_work(_scrub_provenance_graph(result.payload, hidden), hidden),
            rows=None if result.rows is None else _scrub_session_work(result.rows, hidden),
            missing=(
                list(
                    dict.fromkeys(
                        [*result.missing, MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED]
                    )
                )
                if truncated
                else result.missing
            ),
        )
