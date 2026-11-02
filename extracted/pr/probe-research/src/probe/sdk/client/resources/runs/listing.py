"""RunListingMixin, Client's methods: list and move runs and their artifacts across experiments and
projects (twins: app/runs, app/files/artifacts)."""

from __future__ import annotations

from .... import errors
from ....artifact.listing import read_artifact_rows
from ....values.tags import canonical_tags
from ....delivery.transport.transport import Page
from probe.sdk.routes import WriteOp, path_for


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
        **params,
    ) -> Page:
        """``project_id`` returns ALL the project's runs — project-direct AND
        experiment-attached (0054); ``direct=True`` narrows to experiment-less
        runs only."""
        query = dict(params)
        if experiment_id is not None:
            query["experiment_id"] = experiment_id
        if project_id is not None:
            query["project_id"] = project_id
        if direct:
            query["direct"] = "true"
        tags = canonical_tags(tags) if tags else None
        if tags:
            query["tags"] = tags
        page = self.transport.get_page("/v1/runs", params=query or None)
        if tags and page.items:
            # Same refuse-rather-than-mislabel contract as the 0054 guard below.
            self._verify_tags_filter(tags, page.items, "GET /v1/runs")
        # A pre-0054 backend IGNORES unknown query params and returns the
        # unscoped list — a confident wrong answer presented as project-scoped.
        # Its rows also predate the project_id field, which is how we can tell:
        # refuse rather than mislabel. (An empty page proves nothing and passes.)
        if (project_id is not None or direct) and page.items and "project_id" not in page.items[0]:
            raise errors.NotFoundError(
                "this research-os backend predates GET /v1/runs?project_id= "
                "(0054): it ignored the filter and returned unscoped runs. "
                "Upgrade the backend before relying on project-scoped listings."
            )
        return page

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
from probe.sdk.client.ids import _is_uuid, _same_id  # noqa: E402 -- pieces need each other; the front door loads this one first
