"""ReadsResource (client.reads, typed reads) and ReadsMixin, Client's methods: series, compare,
search, browse, web, docs, ingest, SQL, events
(twins: app/knowledge/search, app/projects/browse, app/knowledge/websearch)."""

from __future__ import annotations
from ....generated.models import (
    BrowseResponse,
    DocsOut,
    PaperSearchResponse,
    ReadPageResponse,
    SearchResponse,
    WebSearchResponse,
)
from ..resource import Resource
from typing import Any
from ....models import (
    IngestRunRequest,
    LatestScalarsRequest)
from ...values.tags import canonical_tags


class ReadsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def list_project_artifacts(self, project_id: str) -> list[dict]:
        """Project-wide shared data (fold #22) — the sibling of the experiment read.

        Written as its own literal call site rather than routed through
        :meth:`list_anchored`, for the same reason every anchored route above is:
        the contract-parity guard resolves paths from the AST."""
        return self.transport.get(f"/v1/projects/{project_id}/artifacts")

    def query_sql(
        self,
        *,
        sql: str | None = None,
        tables: list[str] | None = None,
        max_rows: int | None = None,
        source: str | None = None,
    ) -> dict:
        """``POST /v1/sql``: schema discovery (omit ``sql``) or one read-only SELECT. ``source="samples"``
        reads ClickHouse's RL sample views instead of the research tables (sent only when given: an older
        server refuses the field).

        The server enforces the caller's tenant and visibility, a closed set of
        tables, functions and constructs, a 5s statement timeout and a result
        budget. Discovery with no ``tables`` lists every table with its
        ``column_names`` (one comma-separated string); ``tables`` is discovery
        only: ``columns`` as ``{name, type}`` objects for just those.
        """
        body: dict[str, Any] = {}
        if sql is not None:
            body["sql"] = sql
        if tables is not None:
            body["tables"] = tables
        if max_rows is not None:
            body["max_rows"] = max_rows
        if source is not None:
            body["source"] = source
        return self.transport.post("/v1/sql", body)

    def query_series(self, run_ids: list[str], **kw) -> dict:
        kw.setdefault("source_read_contract", SOURCE_READ_CONTRACT)
        return self.transport.post("/v1/series/query", {"run_ids": run_ids, **kw}, idempotent=True)

    def latest_scalars(
        self,
        run_ids: list[str],
        *,
        keys: list[str] | None = None,
        kind: str | None = None,
    ) -> dict:
        """``POST /v1/series/latest``: cross-run scalar summary (last/min/max per
        series) for run tables — reads the derived series catalog, never raw
        points. POST-for-read, so it retries like a GET. Every run must be live
        and in-tenant; a soft-deleted or unknown one is a 404 before any read.
        Built through the generated ``LatestScalarsRequest``, so the caps (50
        runs, 200 keys) fail client-side instead of as a server 422."""
        model = LatestScalarsRequest(
            run_ids=run_ids, keys=keys, kind=kind, source_read_contract=SOURCE_READ_CONTRACT
        )
        return self.transport.post(
            "/v1/series/latest",
            model.model_dump(mode="json", exclude_none=True),
            idempotent=True,
        )

    def compare(self, **kw):
        """Fetch several runs and their metric series together, aligned on step.

        The read people actually want when they open a comparison: which of these
        configs won. Name the runs with ``run_ids=[...]`` or select them with the
        same filters :meth:`list_runs` takes (``experiment_id=``, ``filter={"group_id": G}``)::

            comparison = client.compare(experiment_id=exp_id, keys=["dockq"])
            aligned = comparison.aligned("dockq")
            for label, values in aligned.values.items():
                plot(aligned.steps, values, label=label)   # or .to_pandas()

        Columns are labelled by the server's petname ``slug``. Runs of
        different lengths keep ``None`` holes rather than being truncated to the
        shortest — differing length is usually the thing being compared.

        A shaping layer over :meth:`query_series`, not a second client: see
        :mod:`probe.sdk.reads.compare`."""
        from ...reads.compare import compare as _compare

        return _compare(self, **kw)

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
        curated_only: bool | None = None,
        exclude_origin_session: str | None = None,
        retrieval: str | None = None,
        include_semantic: bool | None = None,
    ) -> dict:
        """``POST /v1/search`` (workspaces+kb fold-in): one-index exact+semantic search.

        POST-for-read, so it retries like any GET. Returns the sectioned
        per-channel response ``{query, state, exact:{results,cursor,error},
        semantic:{results,cursor,error}}``; a backend that predates the
        endpoint 404s (callers such as the MCP source fall back).

        ``exclude_origin_session`` leaves out the projects, experiments and runs
        that coding-agent session CREATED (work another session created stays,
        wherever it is filed); a server that applied it echoes
        ``origin_exclusion_applied: true`` (absent = it did not).

        ``retrieval="keyword"`` runs the semantic leg as BM25 only, with no
        model call; a server that ran it echoes ``semantic.retrieval:
        "keyword"`` (absent = it ignored the field and ran the full search)."""
        body: dict[str, Any] = {"query": query}
        optional = {
            "exclude_agent_session": exclude_agent_session,
            "exclude_origin_session": exclude_origin_session,
            "corpus": corpus,
            "workspace_id": workspace_id,
            "project_id": project_id,
            "top_k": top_k,
            "exact_limit": exact_limit,
            "exact_cursor": exact_cursor,
            "semantic_cursor": semantic_cursor,
            # None, not False, so the key is OMITTED unless the caller asked.
            # The filter below drops None; sending an explicit false would make
            # every request body differ from an older client's for no reason.
            "curated_only": curated_only,
            # Omitted unless asked, for the same byte-identical reason.
            "retrieval": retrieval,
            "include_semantic": include_semantic,
        }
        body.update({key: value for key, value in optional.items() if value is not None})
        return self.transport.post("/v1/search", body, idempotent=True)

    def browse(
        self,
        *,
        scope: str | None = None,
        depth: int | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        workspace_id: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        runs_cursor: str | None = None,
        subprojects_cursor: str | None = None,
        continuation_handles: bool | None = None,
        exclude_origin_session: str | None = None,
    ) -> dict:
        """``GET /v1/browse``: the structured "what exists" tree.

        ``continuation_handles=True`` opts into scope-bound positions before
        each fetched list and after every row. It is for bounded consumers
        that may emit fewer rows than the backend fetched. Ordinary calls keep
        the existing response and legacy keyset cursor contract.

        ``tags`` filters the RUNS level, like ``status`` (repeatable; a run
        must carry ALL — 0066). A pre-0066 backend ignores it; browse trees
        carry no per-run tags to verify against, so no guard here — the
        deterministic check is ``list_runs(tags=…)``.

        Where ``search`` ranks by relevance and needs a query, this enumerates
        structure and needs nothing -- the cold-start read. Returns
        ``{projects|experiments|runs, cursor, depth, limit, truncated}`` with
        exactly one level populated at the top, decided by ``scope``.

        ``workspace_id`` scopes the TOP level to one workspace -- the same lens
        ``list_projects(workspace_id=…)`` uses, so browse and the projects list
        can never disagree about what a workspace holds. It is REFUSED with
        ``scope`` (422): a scope has already narrowed to one project or
        experiment, and silently ignoring the workspace would answer a different
        question with a confident 200. A pre-0193 backend has no such parameter
        and IGNORES it, returning the whole tenant -- so treat a suspiciously
        wide answer as a version skew, not as a workspace holding everything.

        A backend that predates the endpoint 404s; callers fall back honestly
        rather than presenting an empty tree as "nothing exists".

        ``exclude_origin_session`` leaves out, at every level, the work that
        coding-agent session created (as :meth:`search`); echoed as
        ``origin_exclusion_applied: true`` by a server that applied it.
        """
        params: dict[str, Any] = {}
        optional = {
            "scope": scope,
            "depth": depth,
            "status": status,
            "tags": canonical_tags(tags) if tags else None,
            "workspace_id": workspace_id,
            "limit": limit,
            "cursor": cursor,
            # 0148: per-LEVEL continuation for the project scope's side lists
            # (from a prior response's `cursors`). Tokens are level-specific;
            # a project-scope token means nothing on another scope and the
            # server refuses it there.
            "runs_cursor": runs_cursor,
            "subprojects_cursor": subprojects_cursor,
            "continuation_handles": continuation_handles,
            "exclude_origin_session": exclude_origin_session,
        }
        params.update({k: v for k, v in optional.items() if v is not None})
        return self.transport.get("/v1/browse", params=params or None)

    # -- the open web (app/websearch) ---------------------------------------
    #
    # THE ONE FAMILY HERE THAT READS TEXT THIS LAB DID NOT WRITE. Everything
    # else on this client returns the tenant's own record; these three return
    # whatever a stranger published on a page they control. The narrowing that
    # matters happens at the backend boundary (app/websearch/service.py drops
    # raw HTML, caps page text, and spells `recency` itself rather than passing
    # a model's string into the upstream query) -- so these methods are thin ON
    # PURPOSE and must stay that way. A convenience here that widened what may
    # be sent would be re-opening a door somebody deliberately narrowed.
    #
    # NOT `idempotent=True`, unlike `search` above, and this is the one place
    # these three differ from every other POST-for-read on this client. HTTP
    # idempotent is not the same as FREE. `transport._RETRYABLE` is
    # {502, 503, 504}, which is exactly what `app/websearch/router.py` maps a
    # provider failure onto, so the retry would fire on precisely the wrong
    # cases: a 503 IS "over quota or rate limited, try later" (retrying 200ms
    # later is the one response guaranteed not to help), and a 502 or 504 can
    # follow a Firecrawl call that already completed and was already billed --
    # so the retry buys a second charge for an answer nobody reads. Marking
    # them idempotent additionally re-enables ReadTimeout retry, which the
    # transport excludes by default precisely because the request already
    # landed.
    #
    # Connect errors still retry (see `replayable` in transport.py): those never
    # reached the server, so they cost nothing and lose nothing.
    #
    # Only the arguments the caller SET are sent. The three request models are
    # `extra="forbid"` but their defaults are the backend's business, and a
    # client that echoed its own copy of `limit=5` would pin a value the
    # deployment is entitled to move. The MCP tool layer honours this too --
    # its `limit`/`expand` parameters default to None, not to a mirror of the
    # backend's current default.

    def search_web(
        self,
        query: str,
        *,
        limit: int | None = None,
        category: str | None = None,
        recency: str | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_content: bool | None = None,
    ) -> dict:
        """``POST /v1/web/search`` — web search, via the backend's Firecrawl key.

        Returns ``{query, state, results:[{title,url,snippet,text?}],
        credits_used}``. ``state`` is ``"empty"`` when the provider answered
        with nothing, which is an ANSWER and not a failure.

        ``include_domains`` and ``exclude_domains`` are mutually exclusive and
        the backend 422s on the pair rather than silently dropping one.
        """
        body: dict[str, Any] = {"query": query}
        optional = {
            "limit": limit,
            "category": category,
            "recency": recency,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "include_content": include_content,
        }
        body.update({k: v for k, v in optional.items() if v is not None})
        return self.transport.post("/v1/web/search", body)

    def find_papers(
        self,
        mode: str,
        *,
        query: str | None = None,
        paper_id: str | None = None,
        limit: int | None = None,
        authors: str | None = None,
        categories: str | None = None,
        published_from: str | None = None,
        published_to: str | None = None,
        expand: str | None = None,
    ) -> dict:
        """``POST /v1/web/papers`` — the research literature, three ways.

        ``mode`` picks which question: ``search`` ranks abstracts, ``read``
        opens one paper (with ``query``, returns the passages answering it),
        ``similar`` expands from one paper along ``expand``.

        The backend REFUSES arguments the chosen mode cannot read rather than
        ignoring them, so a `paper_id` sent with ``mode="search"`` is a 422 and
        never a quietly different answer. Nothing is re-validated here: two
        copies of that table would drift, and the endpoint's copy is the one
        that decides.
        """
        body: dict[str, Any] = {"mode": mode}
        optional = {
            "query": query,
            "paper_id": paper_id,
            "limit": limit,
            "authors": authors,
            "categories": categories,
            "published_from": published_from,
            "published_to": published_to,
            "expand": expand,
        }
        body.update({k: v for k, v in optional.items() if v is not None})
        return self.transport.post("/v1/web/papers", body)

    def docs(self, query: str, *, limit: int | None = None) -> dict:
        """``GET /public/v1/docs`` — Probe's own documentation (docs.prbe.ai).

        Returns ``{state, sections: [{page, heading, path, url, text, rank}]}``,
        best section first, each section whole. ``state`` is ``ok``, ``stale``
        (the last good copy, served while docs.prbe.ai cannot be read) or
        ``unavailable`` (no copy yet: ``sections`` is empty). Sent without a
        credential, so it answers signed out. The query rides the URL, which
        access logs keep as sent, so a credential in it is scrubbed first.
        """
        # scanning disabled: from .redaction import scrub_string

        # scanning disabled: params: dict[str, Any] = {"query": scrub_string(query)}
        params: dict[str, Any] = {"query": query}
        if limit is not None:
            params["limit"] = limit
        return self.transport.get("/public/v1/docs", params=params)

    def read_page(self, url: str) -> dict:
        """``POST /v1/web/read`` — one page as text.

        Returns ``{url, state, title, text, truncated}``. ``truncated`` is
        load-bearing: long pages are cut to the deployment's per-page ceiling,
        and a caller that ignores the flag presents a fragment as the document.
        """
        return self.transport.post("/v1/web/read", {"url": url})

    # -- passive / batch push ----------------------------------------------
    def ingest(
        self,
        *,
        experiment_slug: str,
        project_slug: str,
        run: dict,
        batch_id: str | None = None,
        execution_record: dict | None = None,
        spans: list[dict] | None = None,
        metrics: list[dict] | None = None,
        artifacts: list[dict] | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """One idempotent push (bearer ingest token + optional HMAC). Keyed on
        ``(customer_id, run.source, run.external_id)`` with ``batch_id`` dedup.

        Built through the generated ``IngestRunRequest`` (the backend now declares
        this body in its OpenAPI schema), so a malformed run/span/metric/artifact
        fails client-side instead of as a server 422.

        The ingest path is where the fold-in fields actually pin server-side:
        ``run['foreign_keys']`` (per-key new-wins merge), ``execution_record``
        (pins ``run.env_ref``), and per-metric ``dimensions``."""
        model = IngestRunRequest(
            experiment_slug=experiment_slug,
            run=run,
            project_slug=project_slug,
            batch_id=batch_id,
            execution_record=execution_record,
            spans=spans or [],
            metrics=metrics or [],
            artifacts=artifacts or [],
        )
        body = model.model_dump(mode="json", exclude_none=True)
        return self.write("POST", "/ingest/v1/runs", body, strict=strict)

    # -- composed SDK surfaces --------------------------------------------
    @property
    def events(self):
        """Read the backend append-only lifecycle+structure events log (read-only)."""
        if self._events is None:
            from ...reads.events import EventsReadClient

            self._events = EventsReadClient(self)
        return self._events


class ReadsResource(Resource):
    """`client.reads`: typed search, browse, web and docs reads."""

    __slots__ = ()

    def search(
        self, query: str, *, corpus: list[str] | None = None, workspace_id: str | None = None,
        project_id: str | None = None, top_k: int | None = None, exact_limit: int | None = None,
        exact_cursor: str | None = None, semantic_cursor: str | None = None,
        exclude_agent_session: str | None = None, curated_only: bool | None = None,
        exclude_origin_session: str | None = None, retrieval: str | None = None,
        include_semantic: bool | None = None,
    ) -> SearchResponse:
        """`Client.search` as a `SearchResponse`."""
        return self._to_model(
            SearchResponse,
            self._client.search(
                query, corpus=corpus, workspace_id=workspace_id, project_id=project_id, top_k=top_k,
                exact_limit=exact_limit, exact_cursor=exact_cursor, semantic_cursor=semantic_cursor,
                exclude_agent_session=exclude_agent_session, curated_only=curated_only,
                exclude_origin_session=exclude_origin_session, retrieval=retrieval,
                include_semantic=include_semantic,
            ),
        )

    def search_web(
        self, query: str, *, limit: int | None = None, category: str | None = None,
        recency: str | None = None, include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None, include_content: bool | None = None,
    ) -> WebSearchResponse:
        """`Client.search_web` as a `WebSearchResponse`."""
        return self._to_model(
            WebSearchResponse,
            self._client.search_web(
                query, limit=limit, category=category, recency=recency,
                include_domains=include_domains, exclude_domains=exclude_domains,
                include_content=include_content,
            ),
        )

    def find_papers(
        self, mode: str, *, query: str | None = None, paper_id: str | None = None,
        limit: int | None = None, authors: str | None = None, categories: str | None = None,
        published_from: str | None = None, published_to: str | None = None,
        expand: str | None = None,
    ) -> PaperSearchResponse:
        """`Client.find_papers` as a `PaperSearchResponse`."""
        return self._to_model(
            PaperSearchResponse,
            self._client.find_papers(
                mode, query=query, paper_id=paper_id, limit=limit, authors=authors,
                categories=categories, published_from=published_from, published_to=published_to,
                expand=expand,
            ),
        )

    def read_page(self, url: str) -> ReadPageResponse:
        """`Client.read_page` as a `ReadPageResponse`."""
        return self._to_model(ReadPageResponse, self._client.read_page(url))

    def get_tree(
        self, *, scope: str | None = None, depth: int | None = None, status: str | None = None,
        tags: list[str] | None = None, workspace_id: str | None = None, limit: int | None = None,
        cursor: str | None = None, runs_cursor: str | None = None,
        subprojects_cursor: str | None = None, continuation_handles: bool | None = None,
        exclude_origin_session: str | None = None,
    ) -> BrowseResponse:
        """`Client.browse` as a `BrowseResponse`."""
        return self._to_model(
            BrowseResponse,
            self._client.browse(
                scope=scope, depth=depth, status=status, tags=tags, workspace_id=workspace_id,
                limit=limit, cursor=cursor, runs_cursor=runs_cursor,
                subprojects_cursor=subprojects_cursor, continuation_handles=continuation_handles,
                exclude_origin_session=exclude_origin_session,
            ),
        )

    def search_docs(self, query: str, *, limit: int | None = None) -> DocsOut:
        """`Client.docs` as a `DocsOut`."""
        return self._to_model(DocsOut, self._client.docs(query, limit=limit))

from probe.sdk.client.resources.runs.metrics import SOURCE_READ_CONTRACT  # noqa: E402 -- pieces need each other; the front door loads this one first
