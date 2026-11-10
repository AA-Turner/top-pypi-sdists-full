"""run and trial views: card, record, trajectory, trials, metrics, events, saved views, sandbox diff, reproduce, handoff."""

from __future__ import annotations
from typing import Any
from ....sdk import errors
from ....shared.reads.search_contract import (
    EntityType,
    MissingMarker)
from probe.mcp.tools.shaping.cards import _entity_projection, _record_field
from probe.mcp.tools.view import _Req, _ViewData
from probe.mcp.tools.views.files import _PAGE_FETCH

# `limit` ceilings from schema/openapi.json.
_SPAN_BACKEND_MAX = 10_000  # GET /v1/runs/{id}/spans
#: GET /v1/runs/{id}/trials caps ONE call at `MAX_LIMIT`, and pages with a real
#: keyset cursor -- so unlike the spans route it has no single-call ceiling, and
#: the bound below is this server's own: how far one view will walk, not what the
#: backend will serve. Ten hops.
_TRIAL_ROUTE_PAGE = 200
_TRIAL_BACKEND_MAX = 2_000
#: `GET /v1/runs/{id}/commands` serves at most 500 a call (`after=` cursor, by seq); the view walks up to 2,000.
_COMMAND_ROUTE_PAGE = 500
_COMMAND_BACKEND_MAX = 2_000
_METRIC_BACKEND_MAX = 100_000  # GET /v1/runs/{id}/metrics

#: What a saved metric view row keeps. `run_id` goes: it is the run asked about.
_SAVED_VIEW_FIELDS = ("id", "name", "spec", "created_by", "created_at", "updated_at")

#: What an edit row keeps: what it did to which data, who and why, and whether it is undone. `run_id`
#: (the run asked about), `customer_id` and the apply job's `phase` go.
_EDIT_FIELDS = (
    "id", "seq", "op", "target", "args", "reason", "actor_kind", "actor", "state", "counts", "revert_of",
    "reverted_by", "config_before", "error", "created_at", "applied_at",
)  # fmt: skip

#: What a command row keeps: the ask, who made it, what happened and why. `run_id` (the run asked about) and the
#: claiming writer session go.
_COMMAND_FIELDS = (
    "id", "seq", "kind", "args", "state", "requested_by", "note", "reason", "result", "write_epoch", "created_at",
    "claimed_at", "ended_at",
)  # fmt: skip


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


class RunViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _view_card(self, entity: dict, request: _Req) -> _ViewData:
        """The entity projection is assembled once, without extra source reads."""
        return _ViewData()

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
        subtree with the rollout's own `step_index` (`connectors/harbor/atif.py` sets it
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
            # The run row names the project it is filed under: one request.
            project_id = entity.get("project_id")
            return self.source.experiment(
                str(experiment_id), project_id=str(project_id) if project_id else None
            ).get("question")
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
                # A source-backed run whose provider read failed comes back with
                # an EMPTY catalog and the reason here; without it `series: []`
                # reads as "this run logged no metrics".
                **(
                    {"source_error": bundle["source_error"]}
                    if bundle.get("source_error")
                    else {}
                ),
            },
            rows=artifacts,
            rows_key="artifacts",
            missing=missing,
        )

    def _view_events(self, entity: dict, request: _Req) -> _ViewData:
        return _ViewData(rows=self.source.run_events(str(entity["id"])), rows_key="events")

    def _view_run_views(self, entity: dict, request: _Req) -> _ViewData:
        """The metric views saved on this run, each with its expression `spec`.
        `updated_at` is kept: it is the precondition a view edit sends."""
        rows = [
            {key: row[key] for key in _SAVED_VIEW_FIELDS if row.get(key) is not None}
            for row in self.source.run_views(str(entity["id"]))
            if isinstance(row, dict)
        ]
        return _ViewData(rows=rows, rows_key="views")

    def _build_run_commands_view(self, entity: dict, request: _Req) -> _ViewData:
        """What was asked of the run while it ran, oldest first: a checkpoint, an LR change or a stop explains a turn
        in its curves; a refused or expired row says why nothing happened."""
        run_id = str(entity["id"])
        rows, more, capped = self._bounded(
            lambda limit: self._fetch_command_pages(run_id, limit), request.offset, _COMMAND_BACKEND_MAX
        )
        shaped = [{key: row[key] for key in _COMMAND_FIELDS if row.get(key) is not None}
                  for row in rows if isinstance(row, dict)]  # fmt: skip
        return _ViewData(rows=shaped, rows_key="commands", more_beyond=more,
                         missing=[MissingMarker.COMMANDS_BEYOND_WALK_BOUND] if capped else [])  # fmt: skip

    def _fetch_command_pages(self, run_id: str, limit: int) -> list[dict]:
        """`limit` command rows by seq, following the route's `after=` cursor (one walk from the first, never kept:
        `_trial_pages`' rule). An empty page ends it even with a cursor."""
        rows: list[dict] = []
        after: int | None = None
        while len(rows) < limit:
            page = self.source.run_commands(run_id, after=after, limit=min(_COMMAND_ROUTE_PAGE, limit - len(rows)))
            items = list(page.get("commands") or [])
            rows.extend(items)
            after = page.get("next_after")
            if after is None or not items:
                break
        return rows[:limit]

    def _build_run_edits_view(self, entity: dict, request: _Req) -> _ViewData:
        """The run's edits, newest first. A curve an edit rescaled, shifted or cut reads as what the run
        logged unless the agent sees the edit; a `reverted` row is one that was undone."""
        rows = [
            {key: row[key] for key in _EDIT_FIELDS if row.get(key) is not None}
            for row in self.source.run_edits(str(entity["id"]))
            if isinstance(row, dict)
        ]
        return _ViewData(rows=rows, rows_key="edits")

    def _view_run_diff(self, entity: dict, request: _Req) -> _ViewData:
        """One trial's begin/end filesystem diff: the CHANGED paths as rows,
        whole-scan `counts` in the fixed payload.

        ONE route page per call, read from the route's own path cursor: the
        next cursor names the last path SENT (`resume_key`), so a continuation
        asks the route for the paths after it. Re-walking from the first path
        and skipping the ones already sent re-read the trial's manifests from
        storage once per page, and every changed path stays reachable without a
        walk bound. `view_options.path_prefix` narrows server-side."""
        trial = request.filters.get("trial")
        if not isinstance(trial, str) or not trial.strip():
            raise errors.ValidationError(
                'view="diff" needs view_options.trial: the trial (attempt) whose '
                "sandbox filesystem to diff. It is `meta.sandbox_state.attempt_ref` "
                'on the run\'s sandbox-state files, which view="artifacts" lists.',
                status=422,
            )
        path_prefix = request.filters.get("path_prefix")
        if path_prefix is not None and not isinstance(path_prefix, str):
            raise errors.ValidationError("view_options.path_prefix must be a string", status=422)
        page = self.source.run_sandbox_diff(
            str(entity["id"]),
            trial=trial,
            path_prefix=path_prefix,
            cursor=request.after,
            limit=_PAGE_FETCH,
        )
        entries = [e for e in page.get("entries") or [] if isinstance(e, dict)]
        payload: dict[str, Any] = {
            key: page[key]
            for key in ("trial", "compare_mode", "counts", "integrity", "limits")
            if page.get(key)
        }
        payload["filters"] = request.filters
        return _ViewData(
            payload=payload,
            rows=[{k: v for k, v in e.items() if v is not None} for e in entries],
            rows_key="entries",
            more_beyond=bool(page.get("next_cursor")) and bool(entries),
            resume_key="path",
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
