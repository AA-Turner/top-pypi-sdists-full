"""run reads: lists and pages, the bundle, spans and trials, metrics and series, files, code, reproduction."""

from __future__ import annotations
import base64
from typing import Any
from ...sdk.reads import nonfinite
from ...sdk.client.resources.runs.metrics import SOURCE_READ_CONTRACT
from ...sdk.values.tags import canonical_tags


class RunReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    def runs(
        self,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
        direct: bool = False,
        limit: int = 100,
    ) -> list[dict]:
        """``project_id`` lists ALL the project's runs — project-direct and
        experiment-attached (research-os 0054); ``direct=True`` narrows to
        experiment-less runs server-side."""
        return self.client.list_runs(
            experiment_id=experiment_id,
            project_id=project_id,
            direct=direct,
            limit=limit,
        ).items

    def bundle(self, run_id: str) -> dict:
        """The run bundle, read under the coverage contract. A source-backed run
        (a W&B mirror) answers 422 without it -- which made every view built on
        the bundle (`handoff`, `sessions`) fail on exactly the imported runs. The
        MCP reads the catalog's coverage receipts rather than rendering them."""
        return self.client.run_bundle(run_id, source_read_contract=SOURCE_READ_CONTRACT)

    # -- reads the SDK already had, which the MCP simply never surfaced --------

    def run_spans(self, run_id: str, **filters: Any) -> list[dict]:
        """The trajectory itself. The run bundle carries span_type COUNTS only, so
        before this an agent could see that 500 rollouts happened and not one of
        what they did."""
        return self.client.run_spans(run_id, **filters)

    def run_trials(self, run_id: str, **kw: Any) -> Any:
        """One cursor-aware page of the run's AUTHORED trials (0135).

        Not the same read as filtering `run_spans(span_type="rollout")`. That
        returns the producer's spans; this returns the sidecar rows, which is
        where a researcher's title, description and note live -- and the sidecar
        exists even when its rollout falls outside a bounded run-wide span slice,
        which is exactly when the span read would have said the trial was not
        there."""
        return self.client.list_run_trials(run_id, **kw)

    def run_series(self, run_id: str) -> list[dict]:
        return self.client.run_series(run_id)

    def query_series(self, run_ids: list[str], **kw: Any) -> dict:
        """`POST /v1/series/query` -- the only points door a SOURCE-BACKED run
        has, because it is the only one that can carry the provider's coverage
        receipt. Used as the fallback when the raw-row route refuses."""
        return self.client.query_series(run_ids, **kw)

    def latest_scalars(self, run_ids: list[str], *, keys: list[str]) -> dict:
        """`POST /v1/series/latest`: each series' catalog summary -- its
        `point_count` above all -- read off the derived catalog, never a point
        scan. One call for every run of a series read."""
        return self.client.latest_scalars(run_ids, keys=keys)

    def run_metrics(self, run_id: str, **filters: Any) -> list[dict]:
        # A tool response is strict JSON (the budget serializer refuses NaN), so
        # a non-finite point goes back to `value: null` beside its marker.
        return [nonfinite.to_wire(p) for p in self.client.run_metrics(run_id, **filters)]

    def run_metrics_grouped(self, run_id: str, key: str, **kw: Any) -> dict:
        """Server-side reduce/group (0059/0062). The client follows `next_step`
        paging; the service bounds the total through `max_rows`."""
        return self.client.get_metrics_grouped(run_id, key, **kw)

    def run_coordinates(self, run_id: str) -> list[dict]:
        return self.client.list_run_coordinates(run_id)

    def export_points(self, run_id: str, **kw: Any):
        """The lossless raw-point generator; the service slices one bounded page
        off it and hands the keyset cursor back to the agent. Strict JSON, as
        :meth:`run_metrics`."""
        return (nonfinite.to_wire(p) for p in self.client.export_metric_points(run_id, **kw))

    def run_artifacts(self, run_id: str, **filters: Any) -> list[dict]:
        return self.client.list_run_artifacts(run_id, **filters)

    def run_code(self, run_id: str) -> dict:
        """The run's resolved owner/repo@sha (0134). This one read MAY verify
        resolvability against GitHub server-side (cached, bounded)."""
        return self.client.get_run_code(run_id)

    def run_code_compare(self, run_id: str, to: str) -> dict:
        """What changed in code between two runs, from stored link rows only:
        {state, base, head, swapped, commits, ...} with base = the older run."""
        return self.client.compare_run_code(run_id, to)

    def run_events(self, run_id: str) -> list[dict]:
        return self.client.events.for_run(run_id)

    def run_commands(self, run_id: str, *, after: int | None = None, limit: int | None = None) -> dict:
        """``GET /v1/runs/{ref}/commands``: one page of what was asked of the run, by seq after ``after``
        (``{commands, seq, next_after}``)."""
        return self.client.list_run_commands(run_id, after=after, limit=limit)

    def run_edits(self, run_id: str) -> list[dict]:
        """``GET /v1/runs/{ref}/edits``: the run's edits, newest first."""
        return self.client.list_edits(run_id)

    def run_views(self, run_id: str) -> list[dict]:
        """``GET /v1/runs/{ref}/views``: the metric views saved on the run."""
        return self.client.list_views(run_id)

    def run_sandbox_diff(
        self,
        run_id: str,
        *,
        trial: str,
        path_prefix: str | None = None,
        cursor: str | None = None,
        limit: int,
    ) -> dict:
        """``GET /v1/runs/{ref}/sandbox-state/diff``: one keyset page of a
        trial's begin/end filesystem diff, plus whole-scan `counts`.

        Here and not on the SDK client: it is a read only this surface pages,
        and `probe trial` reaches the same bundle through its own files."""
        parameters: dict[str, Any] = {"trial": trial, "limit": limit}
        if path_prefix:
            parameters["path_prefix"] = path_prefix
        if cursor:
            parameters["cursor"] = cursor
        return self.client.transport.get(
            f"/v1/runs/{run_id}/sandbox-state/diff", params=parameters
        )

    def run_list(
        self,
        *,
        project_id: str | None = None,
        experiment_id: str | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        active: bool = False,
        cursor: str | None = None,
        limit: int,
        exclude_origin_session: str | None = None,
    ) -> tuple[list[dict], str | None]:
        """``GET /v1/runs``: one page of the lab's runs, NEWEST FIRST, and the
        keyset cursor past it. ``active`` is the server's liveness filter
        (status running AND a heartbeat inside the window), not a status."""
        parameters: dict[str, Any] = {"limit": limit}
        if status:
            parameters["status"] = status
        if active:
            parameters["active"] = "true"
        if cursor:
            parameters["cursor"] = cursor
        if exclude_origin_session is not None:
            parameters["exclude_origin_session"] = exclude_origin_session
        page = self.client.list_runs(
            project_id=project_id, experiment_id=experiment_id, tags=tags, **parameters
        )
        return list(page.items), page.next_cursor

    def run_counts(
        self,
        *,
        project_id: str | None = None,
        experiment_id: str | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        is_active: bool = False,
        exclude_origin_session: str | None = None,
    ) -> dict:
        """``GET /v1/runs/counts``: `{total, by_status}` for the same filter as `run_list`. Raises on
        an API without the route (404) or a count past its bound (503); the caller marks it."""
        parameters: dict[str, Any] = {}
        for key, value in (
            ("project_id", project_id),
            ("experiment_id", experiment_id),
            ("status", status),
            ("exclude_origin_session", exclude_origin_session),
        ):
            if value is not None:
                parameters[key] = value
        if tags:
            # The page's own canonical form (`list_runs`), so both filter the same rows.
            parameters["tags"] = canonical_tags(tags)
        if is_active:
            parameters["active"] = "true"
        return self.client.transport.get("/v1/runs/counts", params=parameters)

    def run_failures(self, run_ids: list[str]) -> list[dict]:
        """``GET /v1/runs/failures``: why each named failed/crashed run failed (at most 20)."""
        answer = self.client.transport.get("/v1/runs/failures", params={"ids": ",".join(run_ids)})
        return list((answer or {}).get("failures") or [])

    @staticmethod
    def run_cursor_after(row: dict) -> str | None:
        """The `GET /v1/runs` cursor that resumes AFTER `row`: the list's own
        keyset, base64 of `<created_at>|<id>` (app/core/pagination.py), which
        the server reads as `(created_at, id) < (that row's)`.

        Built from the row rather than taken from the response because the MCP
        delivers a PREFIX of a page when its budget runs out, and has to resume
        after the last row it actually sent -- the server only names the cursor
        after the page's last row. Positional resumption (re-fetch, skip N) is
        what this replaced: a run that stopped being active, or was deleted,
        between two calls shifted every later row by one, so a row was skipped.

        None when the row lacks either half, so a caller can refuse to page
        rather than restart from the top."""
        created_at, row_id = row.get("created_at"), row.get("id")
        if not isinstance(created_at, str) or not created_at or not row_id:
            return None
        # `+00:00`, not `Z`: the server's `datetime.fromisoformat` reads both on
        # 3.11+, and only the offset form on anything older.
        if created_at.endswith("Z"):
            created_at = created_at[:-1] + "+00:00"
        return base64.urlsafe_b64encode(f"{created_at}|{row_id}".encode()).decode()

    def execution_record(self, content_hash: str) -> dict:
        """The pinned environment behind ``run.env_ref`` — code, deps, hardware,
        settings, paths. This is what makes the reproduce view a reproduction."""
        return self.client.get_execution_record(content_hash)

    def reproduce(self, run_id: str) -> dict:
        """The server-assembled run reproduction record. Passthrough: the client is
        thin here on purpose — the backend is the one place that reads every piece
        together (research-os /reproduce)."""
        return self.client.run_reproduce(run_id)
