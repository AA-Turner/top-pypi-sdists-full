"""PapersResource (client.papers, typed reads) and PapersMixin, Client's methods: project
references, papers and the citation graph (twin: app/papers)."""

from __future__ import annotations
import builtins
from .....generated.models import CitationGraphOut, PaperCitationsOut, PaperListOut, PaperOut
from ....delivery.transport.transport import Page
from ...resource import Resource
from collections.abc import Iterable
from typing import Any

from .....foundation.compat.compat import StrEnum
from .....models import CitationDirection
from ....values.tags import canonical_tags


class ProjectRelation(StrEnum):
    """What a project -> project link says (0401; research-os
    `ReferenceRelation`). Written out rather than generated: the SDK models
    are not regenerated for one enum."""

    #: "this drew on that" (0153's lateral reference).
    REFERENCES = "references"
    #: "this is a part of that": a phase of a bigger effort.
    PART_OF = "part_of"


def _citation_direction(value: object) -> str:
    """``reference`` or ``citer``, checked before the request so a typo fails
    naming the vocabulary rather than as the server's 422."""
    raw = getattr(value, "value", value)
    try:
        return CitationDirection(str(raw).strip()).value
    except ValueError:
        allowed = ", ".join(d.value for d in CitationDirection)
        raise ValueError(f"citation direction must be one of {allowed}; got {raw!r}") from None


class PapersMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # --- project code sources (0134) ----------------------------------------
    #
    # The commit timeline is read THROUGH GitHub by the backend (ETag cache,
    # honest ok/stale/unavailable states) — these methods proxy the read; no
    # history is mirrored anywhere.

    # -- project links (0153, 0401) ------------------------------------------
    #
    # Projects are flat; these edges are how they relate. Two relations:
    # `references` says "this drew on that" (a review feeding a training run),
    # `part_of` says "this is a part of that" (a phase of a bigger effort).
    # One edge per ordered pair. Cycles are legal, depth is unbounded, and
    # neither moves a project, shares access or deletes anything with it. A
    # project's detail read serves them apart: `references` and
    # `part_of_links` (outgoing = this is part of the other).

    def add_project_reference(
        self, project_id: str, to_project_id: str, *, relation: str | None = None
    ) -> None:
        """Record that ``project_id`` references ``to_project_id``, or, with
        ``relation="part_of"``, that it is a part of it.

        Idempotent, and DIRECTED: A->B and B->A are different statements, and
        adding one does not add the other. A ``part_of`` add upgrades a
        reference on the same pair; a plain add never downgrades a
        ``part_of`` link. ``relation`` omitted sends what every older client
        sent (the server's default, ``references``).
        """
        body = {"to_project_id": to_project_id}
        if relation is not None:
            body["relation"] = relation
        self.transport.post(f"/v1/projects/{project_id}/references", body)

    def remove_project_reference(self, project_id: str, to_project_id: str) -> None:
        """Drop one directed edge, of either relation; the opposite direction
        is untouched."""
        self.transport.delete(f"/v1/projects/{project_id}/references/{to_project_id}")

    # -- papers (0152) -------------------------------------------------------
    #
    # The literature a `research` project was built from. Project-anchored and
    # only project-anchored; an experiment-level anchor stays unbuilt until a
    # surface asks for one. NO DEDUPE: two adds of one ``source_url`` make two
    # rows, because the server cannot decide what identity means for a paper
    # with an arXiv URL, a DOI landing page, or a caller-local path.

    def add_paper(
        self,
        project_id: str,
        *,
        title: str,
        source_url: str,
        authors: str | None = None,
        repo_url: str | None = None,
        summary_md: str | None = None,
        discrepancies_md: str | None = None,
        tags: list[str] | None = None,
        lineage: dict | None = None,
        relates_to: dict | None = None,
    ) -> dict:
        """Record one paper against a project.

        ``tags`` are the CONCEPTS this paper is about in your own vocabulary --
        the same reader-authored list projects, experiments and runs carry, and
        the axis a forty-paper review is grouped on. They are not the
        provider's ``extracted_categories``: those are arXiv's taxonomy and the
        server owns them.

        ``title`` remains reviewer-authored. ``source_url`` is required and may
        be an HTTP(S) URL or a path on the recording client's machine.
        Provider extraction is stored separately and never rewrites the title
        or summary. ``discrepancies_md`` is what nothing else captures: what
        the released repo does that the paper does not say. Adding counts as
        activity on the project; editing and removing deliberately do not.

        ``lineage`` records HOW YOU GOT TO THIS PAPER, and it mirrors the wire
        shape exactly rather than flattening into keyword arguments, because the
        distinction that matters cannot survive being flattened::

            lineage=None                       nobody asked -> stays UNKNOWN
            lineage={"via": None}              you looked, there was no parent
            lineage={"via": "<paper id>",      you followed that paper to this one
                     "provenance": "observed_call",
                     "reason": "its references"}

        Passing nothing and passing ``{"via": None}`` are DIFFERENT answers. In
        Python they would collapse into the same ``via=None`` argument, which is
        the whole reason this is one parameter and not three.

        ``provenance`` is required whenever ``via`` names a paper, and has no
        default anywhere in the stack: a provenance the client picked would be a
        claim nobody made. Use ``observed_call`` when a tool call handed you the
        parent (``find_papers(mode="similar", expand="references")`` already knew
        it), ``provider_citation`` when you found it in a reference list,
        ``human`` when a person said so, ``inferred`` when a model concluded it
        after the fact. Every one of them records YOUR path through the
        literature; whether one paper's bibliography names another is a
        ``cites`` link the server reads on its own (:meth:`paper_citations`,
        :meth:`citation_graph`), never something this edge asserts.

        Answer at ADD TIME. Two turns later this is a guess.

        ``relates_to`` links this paper to the EARLIER paper in the project it
        connects to, with the reason (server 0357)::

            relates_to=None                    not answered -> nothing stored
            relates_to={"paper": None}         none (the project's first paper)
            relates_to={"paper": "<paper id>",
                        "reason": "how the two relate, in 1-2 sentences",
                        "provenance": "inferred"}

        ``reason`` and ``provenance`` are required with a paper. Pick it by what
        the papers say, never the paper added last. A link written with the
        Probe daemon's key is stored ``inferred`` whatever it says.
        """
        body = {
            key: value
            for key, value in {
                "authors": authors,
                "repo_url": repo_url,
                "summary_md": summary_md,
                "discrepancies_md": discrepancies_md,
                "tags": tags,
                # `is not None` on the OBJECT, never on `via` inside it -- the
                # presence of the object is what says "I looked".
                "lineage": lineage,
                "relates_to": relates_to,
            }.items()
            if value is not None
        }
        body["title"] = title
        body["source_url"] = source_url
        row = self.transport.post(f"/v1/projects/{project_id}/papers", body)
        if tags is not None:
            # A pre-0176 backend drops `tags` from the body and answers 201 with
            # an untagged paper -- the 0066 write failure, one entity later.
            self._verify_tags_written(tags, row, "POST /v1/projects/{id}/papers")
        return row

    def list_papers(
        self,
        project_id: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        tags: list[str] | None = None,
    ):
        """One project's papers, newest first. Returns a cursor ``Page``.

        ``tags`` narrows by CONTAINMENT: a paper must carry every tag named, not
        any of them — the same AND semantics the project, experiment and run
        listings use, so one mental model covers all four.
        """
        query: dict = {}
        if cursor is not None:
            query["cursor"] = cursor
        if limit is not None:
            query["limit"] = limit
        tags = canonical_tags(tags) if tags else None
        if tags:
            query["tags"] = tags
        page = self.transport.get_page(f"/v1/projects/{project_id}/papers", params=query or None)
        if tags and page.items:
            # A pre-0176 backend IGNORES the filter and returns every paper in
            # the project, which the caller would then read as "these are the
            # retrieval ones". Refuse rather than mislabel.
            self._verify_tags_filter(tags, page.items, "GET /v1/projects/{id}/papers")
        return page

    def get_paper(self, paper_id: str) -> dict:
        return self.transport.get(f"/v1/papers/{paper_id}")

    def update_paper(
        self,
        paper_id: str,
        *,
        title: str | None = None,
        authors: str | None = None,
        source_url: str | None = None,
        repo_url: str | None = None,
        summary_md: str | None = None,
        discrepancies_md: str | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Field-replace: an omitted field is untouched, ``""`` clears it —
        except ``title`` and ``source_url``, which are required and cannot be
        emptied (an empty replacement is a 422).

        ``tags`` replaces the WHOLE list (``[]`` clears it), which is the tag
        contract on every entity. To add or drop one tag without knowing the
        rest, read the paper first — that read-modify-write is what the CLI's
        ``probe paper tag`` verb does."""
        body = {
            key: value
            for key, value in {
                "title": title,
                "authors": authors,
                "source_url": source_url,
                "repo_url": repo_url,
                "summary_md": summary_md,
                "discrepancies_md": discrepancies_md,
                "tags": tags,
            }.items()
            if value is not None
        }
        row = self.transport.patch(f"/v1/papers/{paper_id}", body)
        if tags is not None:
            self._verify_tags_written(tags, row, "PATCH /v1/papers/{id}")
        return row

    def remove_paper(self, paper_id: str) -> None:
        self.transport.delete(f"/v1/papers/{paper_id}")

    # -- citation links (citation graph, Track C) --------------------------
    #
    # `cites` is a fact about the LITERATURE: "paper A's reference list names
    # work B", proven only by an id printed in the bibliography entry or
    # deposited by the publisher -- never a title match or a provider's guess.
    # It is not `discovered_via` (`add_paper(lineage=...)`), which records YOUR
    # path through the literature. The server reads both views from its own
    # tables; nothing here calls a provider. A team the server has not switched
    # on reads `state: "disabled"` with no nodes or links.

    def citation_graph(
        self,
        project_id: str,
        *,
        suggested: int | None = None,
        directions: Iterable[str] | str | None = None,
        min_links: int | None = None,
        include_discovery: bool | None = None,
        include_unresolved: bool | None = None,
    ) -> dict:
        """GET /v1/projects/{id}/citation-graph -- the project's papers, the
        works they cite or are cited by, and the ``cites`` edges among them.

        Returns the ``CitationGraphOut`` shape (``probe.models``): ``state``
        (``ok`` | ``partial`` | ``pending``; only a server older than the
        citation flag's removal also answers ``disabled``), ``nodes`` (each
        ``primary`` is one of the project's papers with its fetch status;
        each ``suggested`` is a work the papers link to that the project has
        not recorded), ``edges`` (``cites``, each with the bibliography entries
        that prove it) and ``completeness`` (what was cut, counted).

        Every argument left ``None`` takes the server's default:
        ``suggested`` -- how many suggested works to return, ranked by how many
        of THIS project's papers link to each (50, max 200, 0 for none; never
        padded). ``directions`` -- ``reference`` (what the papers cite),
        ``citer`` (who cites them), or both (default). ``min_links`` -- a
        suggested work needs at least this many linking papers (1).
        ``include_discovery`` -- also return the ``discovered_via`` edges
        among the papers, verbatim and never relabelled ``cites`` (False).
        ``include_unresolved`` -- also return each paper's bibliography entries
        that printed no id (False).
        """
        params: dict[str, Any] = {}
        if suggested is not None:
            params["suggested"] = suggested
        if directions is not None:
            chosen = directions.split(",") if isinstance(directions, str) else list(directions)
            params["directions"] = ",".join(
                _citation_direction(d) for d in chosen if str(d).strip()
            )
        if min_links is not None:
            params["min_links"] = min_links
        if include_discovery is not None:
            params["include_discovery"] = include_discovery
        if include_unresolved is not None:
            params["include_unresolved"] = include_unresolved
        return self.transport.get(
            f"/v1/projects/{project_id}/citation-graph", params=params or None
        )

    def paper_citations(
        self,
        paper_id: str,
        *,
        direction: str | None = None,
        include_unresolved: bool | None = None,
        limit: int | None = None,
    ) -> dict:
        """GET /v1/papers/{id}/citations -- every citation link row of one
        paper with its proof, and how each fetch ended.

        Returns the ``PaperCitationsOut`` shape (``probe.models``): ``state``,
        ``keys`` (the paper's own ids the rows were read for), ``sync`` (the
        per-direction status and counts), ``reference_lists`` (one entry per
        bibliography read: source, owner key, exact url, status, counts),
        ``links`` and ``truncated``. Each link names the bibliography that
        proves it (``list_source``, ``list_owner_key``, ``list_url``,
        ``ordinal``) and HOW (``resolution``: ``printed_id`` in the entry,
        ``publisher_id`` deposited by the publisher, or ``unresolved`` -- an
        entry with no id, kept as text and never an edge).

        ``direction`` -- ``reference`` or ``citer``; both when ``None``.
        ``include_unresolved`` -- the server default is True here: this is the
        view that explains why a reference did not become an edge.
        ``limit`` -- at most this many rows (server default 500, max 2000).
        """
        params: dict[str, Any] = {}
        if direction is not None:
            params["direction"] = _citation_direction(direction)
        if include_unresolved is not None:
            params["include_unresolved"] = include_unresolved
        if limit is not None:
            params["limit"] = limit
        return self.transport.get(f"/v1/papers/{paper_id}/citations", params=params or None)

    def refresh_paper_citations(self, paper_id: str) -> dict:
        """POST /v1/papers/{id}/citations/refresh -- re-read this paper's
        bibliographies and re-nominate its citers now. Answers 202
        (``{"status": "queued"}``); the job runs on the server.

        Needs write access to the paper's project. Refused, never queued:
        429 (``RosError`` with ``status == 429`` and ``retry_after`` set) while
        a refresh for the paper is already queued or within an hour of its
        last fetch -- the lists are third-party documents and asking twice
        cannot make them newer; 409 (``ConflictError``) with ``detail.code ==
        "generation_paused"`` when the team's page generation is paused (only
        a server older than the citation flag's removal also answers 409
        ``citations_disabled``). A plain non-idempotent POST: an
        answer from the server (a 429 included) is never retried, and nothing
        is queued offline -- a refresh is a request to act now. Only a connect
        failure that never reached the server is retried, as for every request.
        """
        return self.transport.post(f"/v1/papers/{paper_id}/citations/refresh")


class PapersResource(Resource):
    """`client.papers`: typed paper reads. `Page.items` are `PaperListOut`; one paper is
    `PaperOut`."""

    __slots__ = ()

    def get(self, paper_id: str) -> PaperOut:
        """`Client.get_paper` as a `PaperOut`."""
        return self._to_model(PaperOut, self._client.get_paper(paper_id))

    def list(
        self, project_id: str, *, cursor: str | None = None, limit: int | None = None,
        tags: builtins.list[str] | None = None,
    ) -> Page:
        """`Client.list_papers` with its items as `PaperListOut`; `next_cursor` unchanged."""
        return self._to_typed_page(
            PaperListOut,
            self._client.list_papers(project_id, cursor=cursor, limit=limit, tags=tags),
        )

    def get_citation_graph(
        self, project_id: str, *, suggested: int | None = None,
        directions: Iterable[str] | str | None = None, min_links: int | None = None,
        include_discovery: bool | None = None, include_unresolved: bool | None = None,
    ) -> CitationGraphOut:
        """`Client.citation_graph` as a `CitationGraphOut`."""
        return self._to_model(
            CitationGraphOut,
            self._client.citation_graph(
                project_id, suggested=suggested, directions=directions, min_links=min_links,
                include_discovery=include_discovery, include_unresolved=include_unresolved,
            ),
        )

    def get_citations(
        self, paper_id: str, *, direction: str | None = None,
        include_unresolved: bool | None = None, limit: int | None = None,
    ) -> PaperCitationsOut:
        """`Client.paper_citations` as a `PaperCitationsOut`."""
        return self._to_model(
            PaperCitationsOut,
            self._client.paper_citations(
                paper_id, direction=direction, include_unresolved=include_unresolved, limit=limit,
            ),
        )
