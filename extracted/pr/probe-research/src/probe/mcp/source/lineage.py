"""lineage and provenance reads: graphs, edges, upstream walks, and whether the server records reads."""

from __future__ import annotations


class LineageReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    def provenance(self, ref: str, *, direction: str, depth: int) -> dict:
        """``GET /v1/provenance``: the bounded graph from `ref`, up to its
        sources or down to everything that used it."""
        return self._catalog_get(
            "/v1/provenance", {"ref": ref, "direction": direction, "depth": depth}
        )

    def provenance_steps(self, ref: str) -> dict:
        """``GET /v1/provenance?format=steps``: the methods view, source first."""
        return self._catalog_get("/v1/provenance", {"ref": ref, "format": "steps"})

    def lineage(self, run_id: str) -> dict:
        return self.client.run_lineage(run_id)

    def run_edges(self, run_id: str) -> list[dict]:
        """Lineage EDGES touching this run (artifact / asset-version provenance).

        A different relation from `lineage()`, which walks `parent_run_id` and
        answers "which run was this forked from". Both are needed to answer
        "where did this run's data come from", and only one of them was ever
        surfaced -- which is why the lineage view reported empty on runs that
        demonstrably consumed a dataset and produced artifacts."""
        return self.client.run_edges(run_id)

    def run_upstream(self, run_id: str, depth: int) -> dict:
        """What the run built on, `depth` hops back, across parents, runs it
        built on, and the writers of the files it read (server 0255)."""
        return self.client.run_upstream(run_id, depth=depth)

    def artifact_lineage(self, artifact_id: str) -> dict:
        return self.client.artifact_lineage(artifact_id)

    def project_lineage(self, project_id: str) -> dict:
        """A project's own links, its origin, and its children with theirs
        (server 0278, lineage plan 2 L12/L18)."""
        return self.client.project_lineage(project_id)

    def experiment_lineage(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """An experiment's own links, its origin and its children, in the
        project lineage's shape, through the experiment API (server X21)."""
        return self.client.experiment_lineage(experiment_id, project_id=project_id)

    def experiment_edges(
        self, experiment_id: str, limit: int, *, project_id: str | None = None
    ) -> list[dict]:
        """The graph AMONG an experiment's runs and files, stored edges first,
        at most ``limit``."""
        return self.client.experiment_edges(experiment_id, limit=limit, project_id=project_id)

    def server_records_reads(self) -> bool:
        """Whether the server has the read lineage routes (0255). An older or
        self-hosted server answers them 404, which a view would otherwise pass
        on as "not found" for an entity that exists. Unknown counts as yes: the
        real call then says what is wrong."""
        try:
            return bool(self.client.supports_feature("run_inputs"))
        except Exception:  # noqa: BLE001
            return True
