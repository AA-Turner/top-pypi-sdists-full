"""Stable public alias for the generated wire models.

Import request/response types from here, never from ``probe._generated.models``
directly. The generated module is a build artifact (see ``scripts/gen_models.py``);
this seam means a change to how it is generated is a one-line update, not a
sweep across the SDK.

When the backend contract moves: refresh ``schema/openapi.json``
(``scripts/dump_openapi.py``) and run ``make gen-models``. If a field the SDK
references was renamed or removed, the import or attribute use below fails fast,
that is the drift signal working as intended.

The expression-view models (``MetricViewCreate``/``Spec``/``Patch``/``Out``/``Data``,
``MetricViewPreviewRequest``) and ``DerivedProvenance`` back the read-time view
surface and the derived-metric write; ``probe.expr`` builds specs against them.

The ``/ingest/v1/runs`` body (``IngestRunRequest`` and its nested ``IngestRun`` /
``IngestArtifact``) is now declared in the backend schema, so the passive push is
generated and validated like every other write path.

"""

from __future__ import annotations

from ._generated.models import (
    AnchorLevel,
    ArtifactCreate,
    ArtifactPinImpact,
    ArtifactVersionCreate,
    ArtifactVersionOut,
    CitationGraphOut,
    CitationLinkOut,
    DerivedProvenance,
    DownloadResponse,
    EdgeCreate,
    EventOut,
    ExecutionRecordCreate,
    ExecutionRecordOut,
    ExperimentTrashedOut,
    ExperimentTrashPreviewOut,
    ExperimentVersionMint,
    ExperimentVersionOut,
    IngestArtifact,
    IngestRun,
    IngestRunRequest,
    LatestScalarsRequest,
    LineageEdgeOut,
    LineageEntityType,
    LineageRelation,
    MetricBatch,
    MetricPointIn,
    MetricViewCreate,
    MetricViewData,
    MetricViewOut,
    MetricViewPatch,
    MetricViewPreviewRequest,
    MetricViewSpec,
    PaperCitationsOut,
    ParentRelation,
    ProjectCreate,
    ProjectExperimentCreate,
    ProjectExperimentDetailOut,
    ProjectExperimentListOut,
    ProjectExperimentMutationOut,
    ProjectExperimentOut,
    ProjectExperimentPatch,
    ProjectWorkspaceOut,
    RunCreate,
    RunDetailOut,
    RunGroupCreate,
    RunGroupOut,
    RunGroupPatch,
    RunOut,
    RunPatch,
    RunStatus,
    Scope,
    SpanBatch,
    SpanCreate,
    StepCreate,
    TokenCreate,
    TokenCreated,
    TokenOut,
    TrialListOut,
    TrialOut,
    TrialPatch,
    UploadGcRequest,
    UploadGcResult,
    ScopedUploadRequest,
    UploadRequest,
    UploadResponse,
)

# The citation graph's two enums carry generic generated names (`Direction`,
# `GraphState`); they are re-exported under names that say what they are.
from ._generated.models import Direction as CitationDirection
from ._generated.models import GraphState as CitationGraphState

#: What a scope id or slug names (`GET /v1/scopes/...`): project, experiment or
#: run. The generator names it after its server module.
from ._generated.models import AppProjectsTwinScopeKind as ScopeKind
from ._generated.models import ProjectKind

#: The experiment create body. `/v1/experiments` was retired by 0231 and its
#: `ExperimentCreate` with it; the light experiments' experiment API creates
#: through `POST /v1/projects/{project_id}/experiments`, whose body is
#: `ProjectExperimentCreate` (slug, question, name, authored_by -- the project
#: is the path). Kept under the old public name so `from probe.models import
#: ExperimentCreate` still imports.
ExperimentCreate = ProjectExperimentCreate

__all__ = [
    # The vertically-movable artifact anchors, backing `probe artifact move --to`.
    # Taken from the contract rather than spelled out in the CLI so a level the
    # backend adds arrives with `make regen` instead of by hand.
    "AnchorLevel",
    "ArtifactCreate",
    "ArtifactPinImpact",
    "ArtifactVersionCreate",
    "ArtifactVersionOut",
    # The citation graph (`Client.citation_graph`, `Client.paper_citations`).
    "CitationDirection",
    "CitationGraphOut",
    "CitationGraphState",
    "CitationLinkOut",
    "DerivedProvenance",
    "DownloadResponse",
    "EdgeCreate",
    "EventOut",
    "ExecutionRecordCreate",
    "ExecutionRecordOut",
    "ExperimentCreate",
    "ExperimentTrashedOut",
    "ExperimentTrashPreviewOut",
    "ExperimentVersionMint",
    "ExperimentVersionOut",
    "IngestArtifact",
    "IngestRun",
    "IngestRunRequest",
    "LatestScalarsRequest",
    "LineageEdgeOut",
    "LineageEntityType",
    "LineageRelation",
    "MetricBatch",
    "MetricPointIn",
    "MetricViewCreate",
    "MetricViewData",
    "MetricViewOut",
    "MetricViewPatch",
    "MetricViewPreviewRequest",
    "MetricViewSpec",
    "PaperCitationsOut",
    "ParentRelation",
    "ProjectCreate",
    "ProjectKind",
    "ScopeKind",
    # The experiment API (light experiments; `Client.*_experiment`).
    "ProjectExperimentCreate",
    "ProjectExperimentDetailOut",
    "ProjectExperimentListOut",
    "ProjectExperimentMutationOut",
    "ProjectExperimentOut",
    "ProjectExperimentPatch",
    "ProjectWorkspaceOut",
    "RunCreate",
    "RunDetailOut",
    "RunGroupCreate",
    "RunGroupOut",
    "RunGroupPatch",
    "RunOut",
    "RunPatch",
    "RunStatus",
    "Scope",
    "SpanBatch",
    "SpanCreate",
    "StepCreate",
    "TokenCreate",
    "TokenCreated",
    "TokenOut",
    "TrialListOut",
    "TrialOut",
    "TrialPatch",
    "UploadGcRequest",
    "UploadGcResult",
    "ScopedUploadRequest",
    "UploadRequest",
    "UploadResponse",
]
