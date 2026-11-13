"""search-shaped reads: /v1/search, read-only SQL, the paper web door, Probe's public docs."""

from __future__ import annotations

from ...sdk import errors


class SearchReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    def search(
        self,
        query: str,
        *,
        corpus: list[str] | None = None,
        workspace_id: str | None = None,
        project_id: str | None = None,
        top_k: int | None = None,
        exact_limit: int | None = None,
        exact_cursor: str | None = None,
        semantic_cursor: str | None = None,
        exclude_agent_session: str | None = None,
        exclude_origin_session: str | None = None,
        retrieval: str | None = None,
        include_semantic: bool | None = None,
        owner: str | None = None,
        since: str | None = None,
        until: str | None = None,
        sort: str | None = None,
    ) -> dict:
        """POST /v1/search.

        404 policy (rolling deploys + oracle-safe SCOPE 404s). This used to need
        a capability probe to tell "the route is gone" from "the scope is gone",
        and that probe cost a billed recall action per session. It is not needed,
        because the MCP only ever talks to the hosted backend, where the route is
        always there:

        - RETRY ONCE on any 404. A stale pod mid-rolling-deploy 404s scoped and
          unscoped requests alike, and attributing that to the scope turns a
          deploy into "your project does not exist" — a wrong answer about the
          caller's own data. Project scope is the commoner of the two, so
          getting this wrong has a wide blast radius.
        - A SECOND 404 on a SCOPED request means that scope is absent (both
          workspace and project scopes are oracle-safe 404s): NotFound.
        - A SECOND 404 on an UNSCOPED request has no scope left to blame, so the
          route itself is missing: CapabilityUnavailable, which names the real
          problem instead of reporting "not found" for a search with nothing to
          find. Nothing catches it — there is deliberately no keyword fallback
          any more (see `service.search`) — so it reaches the caller
          as a truthful failure.
        """
        is_retried = False
        while True:
            try:
                response = self.client.search(
                    query,
                    corpus=corpus,
                    workspace_id=workspace_id,
                    project_id=project_id,
                    top_k=top_k,
                    exact_limit=exact_limit,
                    exact_cursor=exact_cursor,
                    semantic_cursor=semantic_cursor,
                    exclude_agent_session=exclude_agent_session,
                    exclude_origin_session=exclude_origin_session,
                    retrieval=retrieval,
                    include_semantic=include_semantic,
                    owner=owner,
                    since=since,
                    until=until,
                    sort=sort,
                )
            except errors.NotFoundError:
                if is_retried:
                    # Second 404: the deploy window is ruled out, so the 404 is
                    # about the REQUEST. A scope in hand means that scope is
                    # absent; no scope means the route is. An `owner` is a scope
                    # too: no teammate matched it (the 404 names browse(mode="people")).
                    if workspace_id is not None or project_id is not None or owner:
                        raise
                    raise self._capability_unavailable() from None
                is_retried = True
                continue
            return response

    def query_sql(
        self,
        *,
        sql: str | None = None,
        tables: list[str] | None = None,
        max_rows: int | None = None,
        source: str | None = None,
    ) -> dict:
        """``POST /v1/sql``. No retry: a query is not idempotent in cost, and a
        refusal (422), timeout (408), overload (429) or plan refusal (402) is an
        answer the agent must read, not a blip to paper over."""
        return self.client.query_sql(sql=sql, tables=tables, max_rows=max_rows, source=source)

    # Literature uses the same backend and provider contract as the assistant.
    # Keep filtering and per-mode validation at that shared boundary.

    def find_papers(
        self,
        *,
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
        """``POST /v1/web/papers``."""
        return self.client.find_papers(
            mode,
            query=query,
            paper_id=paper_id,
            limit=limit,
            authors=authors,
            categories=categories,
            published_from=published_from,
            published_to=published_to,
            expand=expand,
        )

    def docs(self, query: str, *, limit: int | None = None) -> dict:
        """``GET /public/v1/docs``: Probe's own docs, best section first, each
        whole. Sent without a credential (it is public)."""
        return self.client.docs(query, limit=limit)
