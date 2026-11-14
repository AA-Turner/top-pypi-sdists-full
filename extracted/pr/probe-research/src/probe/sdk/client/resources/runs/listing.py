"""RunListingMixin, Client's methods: list and move runs and their artifacts across experiments and
projects (twins: app/runs, app/files/artifacts)."""

from __future__ import annotations

import json
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from .... import errors
from ....artifact.listing import read_artifact_rows
from ....values.tags import canonical_tags
from ....delivery.transport.pages import iter_pages
from ....delivery.transport.transport import Page
from probe.sdk.routes import WriteOp, path_for
from probe.sdk.client.resources.runs.ordering import DEFAULT_ORDER, OrderField, parse_run_order, sort_runs


#: Rows per request when walking every run: the server's page cap (`app/core/http/pagination.py`).
RUN_PAGE_LIMIT = 200
#: The server feature behind `filter=`, `order=` and `latest_metrics=` (`GET /v1/server/features`).
RUN_LIST_QUERY_FEATURE = "run_list_query"
_VIEWS = ("full", "light")
#: `order="recent"`: newest activity first, a people-and-time-filters order (`people_filters`, not `run_list_query`).
RECENT_ORDER = "recent"


class RunListingMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def move_run(
        self,
        run_id: str,
        *,
        project_id: str | None = None,
        experiment_id: str | None = None,
        group_id: str | None = None,
    ) -> dict:
        """PATCH /v1/runs/{id} with a new home: move a run to another project or experiment.

        Exactly one of ``project_id`` (a project to file the run in directly)
        and ``experiment_id`` (an experiment's uuid; the run lands in it, under
        the project the experiment is filed in) names the target; ``group_id``
        must be a sweep group inside that experiment. The server moves the run
        in one transaction and re-indexes it. An experiment goes to the server
        as ``experiment_id`` (server X21b), never as ``project_id`` -- that
        addresses the experiment as a project, the door R6 removes.

        The answer must SHOW the run in its new home. A server that predates
        filing (or, for ``experiment_id``, X21b) ignores the field and answers
        200 with the run where it was, so a move that did nothing would read as
        done; that is refused (``CapabilityUnavailable``).

        A run moved into an EXPERIMENT answers with the experiment in
        ``experiment_id`` and its project (the run's home) in ``project_id``."""
        if (project_id is None) == (experiment_id is None):
            raise ValueError("move_run needs exactly one of project_id and experiment_id")
        if experiment_id is not None:
            if not _is_uuid(str(experiment_id)):
                raise ValueError("move_run's experiment_id is the experiment's uuid")
            body: dict = {"experiment_id": str(experiment_id)}
        else:
            body = {"project_id": project_id}
        if group_id is not None:
            body["group_id"] = group_id
        row = self.transport.patch(path_for(WriteOp.RUN_PATCH, run_id), body)
        row = row if isinstance(row, dict) else {}
        if experiment_id is not None:
            landed = _same_id(row.get("experiment_id"), experiment_id)
        else:
            landed = _same_id(row.get("project_id"), project_id) or _same_id(
                row.get("experiment_id"), project_id
            )
        if not landed or (group_id is not None and not _same_id(row.get("group_id"), group_id)):
            raise errors.CapabilityUnavailable(
                "run_filing",
                "this server cannot file runs this way yet: it answered the move with the run "
                "where it was. Upgrade the backend before filing runs.",
            )
        return row

    def list_runs(
        self,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
        direct: bool = False,
        tags: list[str] | None = None,
        status: str | None = None,
        active: bool = False,
        name: str | None = None,
        foreign_key: str | None = None,
        created_by_kind: str | None = None,
        exclude_origin_session: str | None = None,
        include_lineage_descendants: bool = False,
        filter: Mapping[str, Any] | None = None,  # noqa: A002 -- the route's own name, as W&B's `filters`
        order: str | None = None,
        latest_metrics: Sequence[str] | None = None,
        view: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        owner: str | None = None,
        since: str | None = None,
        until: str | None = None,
        query: str | None = None,
    ) -> Page:
        """One page of ``GET /v1/runs``, newest first. ``project_id`` returns ALL the project's runs --
        project-direct AND experiment-attached (0054); ``direct=True`` narrows to experiment-less runs.

        ``filter`` is a dict of clauses, ANDed, sent as JSON (``{"config.lr": {"$gt": 1e-3}, "metric.loss":
        {"$lt": 0.5}}``; grammar: the server's ``app/runs/listing/DESIGN.md``, which answers a bad one with a
        422). ``order`` (``"-metric.loss"``, ``"config.lr"``, ``"name"``) other than ``-created_at`` answers
        ONE page of up to ``limit`` runs and no cursor (``iter_runs`` sorts every run). ``latest_metrics``
        (up to 50 keys) adds each row's final values. ``view="light"`` leaves config, metadata, notes,
        description, foreign keys and summary off the rows. A server without these (``run_list_query``)
        raises ``CapabilityUnavailable`` rather than answer an unfiltered list.

        ``owner`` (a user id, an email, a name or ``me``), ``since`` / ``until`` (ISO 8601 or ``24h``,
        ``7d``, ``2w``) and ``order="recent"`` pass as given; the server reads them (``people_filters``).

        ``query`` matches run names and slugs LOOSELY (typos, part of a word, any order), best first, one page
        and no cursor (``browse_name_query``); ``name`` stays the exact lookup a ``name:`` ref resolves by."""
        parameters = self._build_runs_query(
            experiment_id=experiment_id, project_id=project_id, direct=direct, tags=tags, status=status,
            active=active, name=name, foreign_key=foreign_key, created_by_kind=created_by_kind,
            exclude_origin_session=exclude_origin_session, include_lineage_descendants=include_lineage_descendants,
            filter=filter, order=order, latest_metrics=latest_metrics, view=view,
            owner=owner, since=since, until=until, name_query=query,
        )
        if limit is not None:
            parameters["limit"] = limit
        if cursor:
            parameters["cursor"] = cursor
        page = self.transport.get_page("/v1/runs", params=parameters or None)
        self._check_run_rows(page.items, parameters)
        return page

    def iter_runs(
        self,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
        direct: bool = False,
        tags: list[str] | None = None,
        status: str | None = None,
        active: bool = False,
        name: str | None = None,
        foreign_key: str | None = None,
        created_by_kind: str | None = None,
        exclude_origin_session: str | None = None,
        include_lineage_descendants: bool = False,
        filter: Mapping[str, Any] | None = None,  # noqa: A002 -- as `list_runs`
        order: str | None = None,
        latest_metrics: Sequence[str] | None = None,
        view: str | None = None,
        limit: int | None = None,
    ) -> Iterator[dict]:
        """Every run `list_runs` would list with these filters, page after page (200 a page unless ``limit``
        says otherwise), each page checked as `list_runs` checks it.

        An ``order`` other than ``-created_at`` is not paged by the server, so this walks every matching
        run newest first and sorts them here, as the server would (no value last, ``id`` breaks ties): it
        LOADS EVERY MATCHING ROW before yielding the first (``view="light"`` keeps that small). A
        ``metric.<key>`` order asks for that key in ``latest_metrics``, so each row carries the value it
        sorted by; a ``config.<path>`` order reads full rows, since light ones carry no config."""
        run_order = None if order in (None, "", DEFAULT_ORDER) else parse_run_order(order)
        if run_order is not None:
            metric_key = run_order.metric_key
            if metric_key is not None and metric_key not in (latest_metrics or ()):
                latest_metrics = [*(latest_metrics or ()), metric_key]
            if run_order.field is OrderField.CONFIG:
                view = None
        query = self._build_runs_query(
            experiment_id=experiment_id, project_id=project_id, direct=direct, tags=tags, status=status,
            active=active, name=name, foreign_key=foreign_key, created_by_kind=created_by_kind,
            exclude_origin_session=exclude_origin_session, include_lineage_descendants=include_lineage_descendants,
            filter=filter, order=None, latest_metrics=latest_metrics, view=view,
        )
        query["limit"] = limit or RUN_PAGE_LIMIT
        rows = self._walk_run_pages(query)
        if run_order is None:
            yield from rows
        else:
            yield from sort_runs(rows, run_order)

    def _walk_run_pages(self, query: dict) -> Iterator[dict]:
        for row in iter_pages(self.transport, "/v1/runs", query):
            self._check_run_rows([row], query)
            yield row

    def count_runs(
        self,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
        direct: bool = False,
        tags: list[str] | None = None,
        status: str | None = None,
        active: bool = False,
        name: str | None = None,
        foreign_key: str | None = None,
        created_by_kind: str | None = None,
        exclude_origin_session: str | None = None,
        include_lineage_descendants: bool = False,
        filter: Mapping[str, Any] | None = None,  # noqa: A002 -- as `list_runs`
        owner: str | None = None,
        since: str | None = None,
        until: str | None = None,
        query: str | None = None,
    ) -> dict:
        """``GET /v1/runs/counts``: ``{total, by_status}`` for the runs `list_runs` lists with these
        filters (``query``: every loose name match, with ``query_note`` when there is none). A server
        without the route answers 404."""
        parameters = self._build_runs_query(
            experiment_id=experiment_id, project_id=project_id, direct=direct, tags=tags, status=status,
            active=active, name=name, foreign_key=foreign_key, created_by_kind=created_by_kind,
            exclude_origin_session=exclude_origin_session, include_lineage_descendants=include_lineage_descendants,
            filter=filter, owner=owner, since=since, until=until, name_query=query,
        )
        return self.transport.get("/v1/runs/counts", params=parameters or None)

    def _build_runs_query(
        self,
        *,
        filter: Mapping[str, Any] | None = None,  # noqa: A002 -- as `list_runs`
        order: str | None = None,
        latest_metrics: Sequence[str] | None = None,
        view: str | None = None,
        owner: str | None = None,
        since: str | None = None,
        until: str | None = None,
        name_query: str | None = None,
        **flat: Any,
    ) -> dict:
        """The `GET /v1/runs` query for `list_runs`'s keywords: unset ones dropped, booleans as the server
        spells them, tags in canonical form, `filter` as JSON and `latest_metrics` comma-joined. Asks the
        server for `run_list_query` first when `filter`/`order`/`latest_metrics` is set: an older one would
        ignore them and answer every run."""
        query = _build_flat_runs_query(flat)
        if view is not None:
            if view not in _VIEWS:
                raise ValueError(f"view must be one of {', '.join(_VIEWS)}, not {view!r}")
            query["view"] = view
        extra: dict[str, str] = {}
        if filter:
            if not isinstance(filter, Mapping):
                raise TypeError(f"filter is a dict of clauses, not {type(filter).__name__}")
            extra["filter"] = json.dumps(filter, separators=(",", ":"), allow_nan=False)
        # `recent` is a people-and-time-filters order: gated on `people_filters` below, not `run_list_query`.
        if order and order not in (DEFAULT_ORDER, RECENT_ORDER):
            extra["order"] = order
        if latest_metrics:
            if isinstance(latest_metrics, str):
                raise TypeError("latest_metrics is a list of metric keys, not one string")
            keys = list(dict.fromkeys(latest_metrics))
            if any("," in key or not key for key in keys):
                raise ValueError("latest_metrics keys are non-empty and hold no comma (the query joins them by one)")
            extra["latest_metrics"] = ",".join(keys)
        people = {"owner": owner, "since": since, "until": until}
        if order == RECENT_ORDER:
            people["order"] = order
        _require_people_filters(self, people, PEOPLE_FILTERS_FEATURE, "listing runs")
        name_query = name_query.strip() if name_query else None  # blank is no filter, as the server reads it
        # An older server refuses `query` as an unknown param (422): say why instead.
        _require_people_filters(self, {"query": name_query}, BROWSE_NAME_QUERY_FEATURE, "listing runs")
        if extra and not self.supports_feature(RUN_LIST_QUERY_FEATURE):
            raise errors.CapabilityUnavailable(
                RUN_LIST_QUERY_FEATURE,
                f"this Probe server cannot {_describe_asks(extra)} when listing runs yet, and would answer every run "
                "instead; upgrade the server, or list without them.",
            )
        named = {"query": name_query} if name_query else {}
        return query | extra | {name: value for name, value in people.items() if value} | named

    def _check_run_rows(self, rows: list, query: dict) -> None:
        """Refuse rows an older backend sent while ignoring a filter, rather than mislabel them."""
        tags = query.get("tags")
        if tags and rows:
            # Same refuse-rather-than-mislabel contract as the 0054 guard below.
            self._verify_tags_filter(tags, rows, "GET /v1/runs")
        # A pre-0054 backend IGNORES unknown query params and returns the
        # unscoped list — a confident wrong answer presented as project-scoped.
        # Its rows also predate the project_id field, which is how we can tell:
        # refuse rather than mislabel. (An empty page proves nothing and passes.)
        if ("project_id" in query or "direct" in query) and rows and "project_id" not in rows[0]:
            raise errors.NotFoundError(
                "this research-os backend predates GET /v1/runs?project_id= "
                "(0054): it ignored the filter and returned unscoped runs. "
                "Upgrade the backend before relying on project-scoped listings."
            )

    def list_run_artifacts(
        self,
        run_id: str,
        *,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        name: str | None = None,
        scope: str | None = None,
        prefix: str | None = None,
    ) -> list[dict]:
        """List a run's artifacts, optionally server-filtered by kind and/or an
        inclusive step window — e.g. sandbox states around a collapse:
        ``list_run_artifacts(run_id, kind="sandbox_state", step_from=599, step_to=601)``.
        ``prefix`` keeps one folder of names and everything under it.

        ``scope`` controls inheritance (default ``own`` = this run only): ``all`` also
        returns the run's experiment- and project-level artifacts, ``inherited`` only
        those parent levels. On a non-``own`` scope each row carries ``source_level`` and
        rows are ordered nearest-wins, so a ``name`` lookup resolves to the closest level."""
        params = {
            key: value
            for key, value in {
                "kind": kind,
                "step_from": step_from,
                "step_to": step_to,
                "name": name,
                "scope": scope,
                "prefix": prefix,
            }.items()
            if value is not None
        }
        return read_artifact_rows(
            lambda query: self.transport.request(
                "GET", f"/v1/runs/{run_id}/artifacts", params=query, idempotent=True
            ),
            params,
        )

    def move_artifact(self, artifact_id: str, *, level: str, target_id: str | None = None) -> dict:
        """Move an artifact vertically along its own run->experiment->project chain.

        Promote up (``level`` above the artifact's current anchor) derives the target
        from its chain; demote down needs a ``target_id`` that sits inside the current
        subtree. A file (workspace/shared) or a lateral target is a 422; an identical
        artifact already at the destination is a 409. The artifact keeps its id."""
        body: dict = {"level": level}
        if target_id is not None:
            body["target_id"] = target_id
        return self.transport.post(f"/v1/artifacts/{artifact_id}/move", body)

    def list_experiment_artifacts(
        self, experiment_id: str, *, project_id: str | None = None
    ) -> list[dict]:
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/artifacts"),
            experiment_id,
            project_id,
        )


def _build_flat_runs_query(filters: dict) -> dict:
    """The flat `GET /v1/runs` params: unset ones dropped, booleans as `true`, tags in canonical form (as the
    server stores them)."""
    query: dict[str, Any] = {}
    for key, value in filters.items():
        if value is None or value is False:
            continue
        if key == "tags":
            tags = canonical_tags(value) if value else None
            if tags:
                query["tags"] = tags
        elif value is True:
            query[key] = "true"
        else:
            query[key] = value
    return query


def _describe_asks(extra: dict[str, str]) -> str:
    words = {"filter": "filter", "order": "sort", "latest_metrics": "send final metric values"}
    return " or ".join(words[key] for key in extra)


from probe.sdk.client.ids import _is_uuid, _same_id  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.reads import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    BROWSE_NAME_QUERY_FEATURE,
    PEOPLE_FILTERS_FEATURE,
    _require_people_filters,
)
