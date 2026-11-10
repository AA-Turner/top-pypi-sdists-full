"""LineageResource (client.lineage, typed reads) and LineageMixin, Client's methods: edges, inputs,
outputs, upstream, by-hash, branches, records, versions
(twins: app/projects/lineage, app/runs/execution)."""

from __future__ import annotations
from ....generated.models import (
    ArtifactLineageOut,
    BranchesOut,
    ExecutionRecordOut,
    ExperimentManifestOut,
    HashLookupOut,
    LineageEdgeOut,
    ProjectLineageOut,
    RunInputsOut,
    RunOutputsOut,
    RunUpstreamOut,
)
from ..resource import Resource
from typing import Any
from ....models import (
    EdgeCreate,
    ExecutionRecordCreate,
    ExperimentVersionMint)


class LineageMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- lineage edges (fold #2) -------------------------------------------
    def add_edge(
        self,
        *,
        source_type: str,
        source_id: str,
        relation: str,
        target_type: str,
        target_id: str,
        meta: dict | None = None,
        provenance: str | None = None,
        reason: str | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """POST /v1/edges. Closed vocab for types
        (run/artifact/artifact_version/paper/project -- `project` is a project
        or an experiment) and relation
        (consumes/produces/evaluates_on/discovered_via/supersedes/informed_by/...);
        the generated EdgeCreate enforces it. A project end takes
        derived_from, supersedes or informed_by (-> a paper) only.

        ``provenance`` is REQUIRED on a paper edge and optional on a run or
        artifact edge, where it is stored and shown: ``observed_call`` (a tool
        was watched making it), ``human`` or ``inferred``. ``provider_citation``
        (you found the paper in a reference list) is paper-only and refused
        elsewhere; the literature fact "A's bibliography names B" is a
        ``cites`` link (:meth:`paper_citations`), not an edge.
        """
        model = EdgeCreate(
            source_type=source_type,
            source_id=source_id,
            relation=relation,
            target_type=target_type,
            target_id=target_id,
            meta=meta or {},
            provenance=provenance,
            reason=reason,
        )
        return self.write(
            "POST", "/v1/edges", model.model_dump(mode="json", exclude_none=True), strict=strict
        )

    def run_edges(self, run_id: str) -> list[dict]:
        return self.transport.get(f"/v1/runs/{run_id}/edges")

    # -- what runs READ (lineage, server 0255) -------------------------------
    def record_run_inputs(
        self,
        run_id: str,
        inputs: list[dict],
        *,
        coverage: dict | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """POST the files a run read (at most 2,000 per call). The read
        recorder journals these itself as non-blocking ops; this is the direct
        door for a caller holding its own list."""
        body: dict[str, Any] = {"inputs": inputs}
        if coverage is not None:
            body["coverage"] = coverage
        return self.write("POST", f"/v1/runs/{run_id}/inputs", body, strict=strict)

    def run_inputs(self, run_id: str) -> dict:
        """The files a run read, each with the catalog entries holding those
        bytes (`stored_as`; `matches` from an older server), and what the
        recorder could see."""
        return self.transport.get(f"/v1/runs/{run_id}/inputs")

    # -- what runs WROTE (lineage plan 3, server 0285) ------------------------
    def record_run_outputs(
        self,
        run_id: str,
        outputs: list[dict],
        *,
        coverage: dict | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """POST the files a run wrote (at most 2,000 per call; each row needs
        its ``observation_id``). The write recorder journals these itself as
        non-blocking ops; this is the direct door for a caller holding its
        own list."""
        body: dict[str, Any] = {"outputs": outputs}
        if coverage is not None:
            body["coverage"] = coverage
        return self.write("POST", f"/v1/runs/{run_id}/outputs", body, strict=strict)

    def run_outputs(self, run_id: str) -> dict:
        """The files a run recorded writing (path, host, hash, when first
        written and last modified), and what the recorder could see."""
        return self.transport.get(f"/v1/runs/{run_id}/outputs")

    def run_upstream(self, run_id: str, *, depth: int = 2) -> dict:
        """What a run built on, ``depth`` hops back: parents, runs it built
        on, and the writers of every file it read."""
        return self.transport.get(f"/v1/runs/{run_id}/upstream", params={"depth": depth})

    def artifact_lineage(self, artifact_id: str) -> dict:
        """Which run wrote a file (or only carried it) and which runs read it."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}/lineage")

    def project_lineage(self, project_id: str, *, limit: int | None = None) -> dict:
        """A project's or experiment's OWN lineage (lineage plan 2, L12/L13/L18):
        its links in and out (stored, then "built on" derived from what its
        runs used, ``derived: true``), its ``origin``, and its direct children as
        ``nodes``, each with an origin (at most ``limit``, 1-1000; the server's
        default 200). The graph AMONG its runs and files is
        :meth:`experiment_edges`; an experiment's own lineage is
        :meth:`experiment_lineage`."""
        params = {"limit": limit} if limit is not None else None
        return self.transport.get(f"/v1/projects/{project_id}/lineage", params=params)

    def experiment_lineage(
        self, experiment_id: str, *, limit: int | None = None, project_id: str | None = None
    ) -> dict:
        """An experiment's OWN lineage, in :meth:`project_lineage`'s shape: its
        links in and out, its ``origin`` and its direct children
        (``GET /v1/projects/{P}/experiments/{E}/lineage``)."""
        params = {"limit": limit} if limit is not None else None
        return self._on_experiment(
            lambda p, e: self.transport.get(
                f"/v1/projects/{p}/experiments/{e}/lineage", params=params
            ),
            experiment_id,
            project_id,
        )

    def project_branches(self, project_id: str) -> dict:
        """The lines of work under a project: each one's
        best value on the declared metric, rank, effort, state, sessions and
        links (``GET /v1/projects/{P}/branches``)."""
        return self.transport.get(f"/v1/projects/{project_id}/branches")

    def experiment_branch(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """The experiment's line of work and the ones it split from, in
        :meth:`project_branches`' shape (``GET /v1/projects/{P}/experiments/{E}/branch``)."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/branch"),
            experiment_id,
            project_id,
        )

    def workspace_branches(self, workspace_id: str) -> dict:
        """A workspace's lines of work across its projects, ranked per metric,
        and its best pick (``GET /v1/workspaces/{W}/branches``)."""
        return self.transport.get(f"/v1/workspaces/{workspace_id}/branches")

    def artifacts_by_hash(self, content_hash: str) -> dict:
        """Every stored copy of these bytes, its writer, and its readers."""
        return self.transport.get(f"/v1/artifacts/by-hash/{content_hash}")

    def paper_edges(self, project_id: str) -> list[dict]:
        """Every discovery edge among one project's papers, in one call.

        The whole chain, not one paper's parents: reading it per paper would be
        a request per card, and the shape a reader wants is the graph anyway.
        """
        return self.transport.get(f"/v1/projects/{project_id}/paper-edges")

    def remove_edge(self, edge_id: str, *, strict: bool | None = None) -> dict | None:
        """DELETE /v1/edges/{id} — take back an edge that was wrong.

        Discovery edges are somebody's recollection of how they got somewhere,
        so being wrong is a normal outcome rather than an exceptional one, and a
        graph nobody can correct is one people stop trusting.
        """
        return self.write("DELETE", f"/v1/edges/{edge_id}", None, strict=strict)

    # -- execution records (fold #7) ---------------------------------------
    def execution_record(
        self,
        *,
        code: dict | None = None,
        deps: dict | None = None,
        hardware: dict | None = None,
        settings: dict | None = None,
        paths: dict | None = None,
    ) -> dict:
        """POST /v1/execution-records (content-addressed, idempotent). Returns
        {content_hash, ...}."""
        model = ExecutionRecordCreate(
            code=code or {},
            deps=deps or {},
            hardware=hardware or {},
            settings=settings or {},
            paths=paths or {},
        )
        return self.transport.post(
            "/v1/execution-records", model.model_dump(mode="json"), idempotent=True
        )

    def get_execution_record(self, content_hash: str) -> dict:
        return self.transport.get(f"/v1/execution-records/{content_hash}")

    # -- experiment versions (fold #6) -------------------------------------
    def experiment_version(
        self,
        experiment_id: str,
        *,
        label: str | None = None,
        as_of: str | None = None,
        exclude_run_ids: list[str] | None = None,
        strict: bool | None = None,
        project_id: str | None = None,
    ) -> dict | None:
        """POST /v1/projects/{P}/experiments/{E}/versions - mint an immutable
        launch-time manifest (a snapshot of the experiment's runs). This replaces
        the removed run-level `promote`; Probe rejected promotion tiers."""
        model = ExperimentVersionMint(
            label=label, as_of=as_of, exclude_run_ids=exclude_run_ids or []
        )
        body = model.model_dump(mode="json", exclude_none=True)
        return self._on_experiment(
            lambda p, e: self.write(
                "POST", f"/v1/projects/{p}/experiments/{e}/versions", body, strict=strict
            ),
            experiment_id,
            project_id,
            journaled=self._journals(strict=strict),
        )

    def list_experiment_versions(
        self, experiment_id: str, *, project_id: str | None = None
    ) -> list[dict]:
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/versions"),
            experiment_id,
            project_id,
        )

    def get_experiment_version(
        self, experiment_id: str, version: int | str, *, project_id: str | None = None
    ) -> dict:
        return self._on_experiment(
            lambda p, e: self.transport.get(
                f"/v1/projects/{p}/experiments/{e}/versions/{version}"
            ),
            experiment_id,
            project_id,
        )


class LineageResource(Resource):
    """`client.lineage`: typed lineage, branch, execution-record and experiment-version reads."""

    __slots__ = ()

    def list_run_edges(self, run_id: str) -> list[LineageEdgeOut]:
        """`Client.run_edges` as `LineageEdgeOut`s."""
        return self._to_models(LineageEdgeOut, self._client.run_edges(run_id))

    def get_run_inputs(self, run_id: str) -> RunInputsOut:
        """`Client.run_inputs` as a `RunInputsOut`."""
        return self._to_model(RunInputsOut, self._client.run_inputs(run_id))

    def get_run_outputs(self, run_id: str) -> RunOutputsOut:
        """`Client.run_outputs` as a `RunOutputsOut`."""
        return self._to_model(RunOutputsOut, self._client.run_outputs(run_id))

    def get_run_upstream(self, run_id: str, *, depth: int = 2) -> RunUpstreamOut:
        """`Client.run_upstream` as a `RunUpstreamOut`."""
        return self._to_model(RunUpstreamOut, self._client.run_upstream(run_id, depth=depth))

    def get_artifact_lineage(self, artifact_id: str) -> ArtifactLineageOut:
        """`Client.artifact_lineage` as an `ArtifactLineageOut`."""
        return self._to_model(ArtifactLineageOut, self._client.artifact_lineage(artifact_id))

    def get_project_lineage(
        self, project_id: str, *, limit: int | None = None,
    ) -> ProjectLineageOut:
        """`Client.project_lineage` as a `ProjectLineageOut`."""
        return self._to_model(
            ProjectLineageOut,
            self._client.project_lineage(project_id, limit=limit),
        )

    def get_experiment_lineage(
        self, experiment_id: str, *, limit: int | None = None, project_id: str | None = None,
    ) -> ProjectLineageOut:
        """`Client.experiment_lineage` as a `ProjectLineageOut`."""
        return self._to_model(
            ProjectLineageOut,
            self._client.experiment_lineage(experiment_id, limit=limit, project_id=project_id),
        )

    def get_project_branches(self, project_id: str) -> BranchesOut:
        """`Client.project_branches` as a `BranchesOut`."""
        return self._to_model(BranchesOut, self._client.project_branches(project_id))

    def get_experiment_branch(
        self, experiment_id: str, *, project_id: str | None = None,
    ) -> BranchesOut:
        """`Client.experiment_branch` as a `BranchesOut`."""
        return self._to_model(
            BranchesOut,
            self._client.experiment_branch(experiment_id, project_id=project_id),
        )

    def get_workspace_branches(self, workspace_id: str) -> BranchesOut:
        """`Client.workspace_branches` as a `BranchesOut`."""
        return self._to_model(BranchesOut, self._client.workspace_branches(workspace_id))

    def find_artifacts_by_hash(self, content_hash: str) -> HashLookupOut:
        """`Client.artifacts_by_hash` as a `HashLookupOut`."""
        return self._to_model(HashLookupOut, self._client.artifacts_by_hash(content_hash))

    def list_paper_edges(self, project_id: str) -> list[LineageEdgeOut]:
        """`Client.paper_edges` as `LineageEdgeOut`s."""
        return self._to_models(LineageEdgeOut, self._client.paper_edges(project_id))

    def get_execution_record(self, content_hash: str) -> ExecutionRecordOut:
        """`Client.get_execution_record` as an `ExecutionRecordOut`."""
        return self._to_model(ExecutionRecordOut, self._client.get_execution_record(content_hash))

    def list_experiment_versions(
        self, experiment_id: str, *, project_id: str | None = None,
    ) -> list[ExperimentManifestOut]:
        """`Client.list_experiment_versions` as `ExperimentManifestOut`s."""
        return self._to_models(
            ExperimentManifestOut,
            self._client.list_experiment_versions(experiment_id, project_id=project_id),
        )

    def get_experiment_version(
        self, experiment_id: str, version: int | str, *, project_id: str | None = None,
    ) -> ExperimentManifestOut:
        """`Client.get_experiment_version` as an `ExperimentManifestOut`."""
        return self._to_model(
            ExperimentManifestOut,
            self._client.get_experiment_version(experiment_id, version, project_id=project_id),
        )
