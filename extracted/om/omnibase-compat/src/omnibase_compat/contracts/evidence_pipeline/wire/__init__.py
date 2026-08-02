# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Evidence pipeline wire DTOs for automated OCC contract validation."""

from omnibase_compat.contracts.evidence_pipeline.wire.model_correlation_trace import (
    ModelCorrelationTrace,
    ModelCorrelationTraceEvent,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_correlation_trace_projection import (
    ModelCorrelationTraceProjection,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_dashboard_event import (
    ModelDashboardEvent,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_dashboard_projection_event import (
    ModelDashboardProjectionEvent,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_deployment_readiness_result import (
    ModelDeploymentReadinessResult,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_evidence_bundle import (
    ModelEvidenceBundle,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_evidence_dashboard_projection import (
    ModelEvidenceDashboardProjection,
    ModelEvidenceDashboardStageProjection,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_evidence_pipeline_command import (
    ModelEvidencePipelineCommand,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_evidence_validation_result import (
    ModelEvidenceValidationResult,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_gap_report import ModelGapReport
from omnibase_compat.contracts.evidence_pipeline.wire.model_occ_pr_reference import (
    ModelOccPrReference,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_raw_evidence_payload import (
    ModelRawEvidencePayload,
)
from omnibase_compat.contracts.evidence_pipeline.wire.model_readiness_aggregate_projection import (
    ModelReadinessAggregateProjection,
)
from omnibase_compat.contracts.evidence_pipeline.wire.topics import (
    EVIDENCE_COLLECTED_EVT_V1,
    EVIDENCE_DASHBOARD_PROJECTED_EVT_V1,
    EVIDENCE_EXTRACTED_EVT_V1,
    EVIDENCE_GAP_ANALYZED_EVT_V1,
    EVIDENCE_OCC_PR_CREATED_EVT_V1,
    EVIDENCE_PIPELINE_START_CMD_V1,
    EVIDENCE_READINESS_SCORED_EVT_V1,
    EVIDENCE_VALIDATED_EVT_V1,
)
from omnibase_compat.contracts.evidence_pipeline.wire.types import (
    DashboardSeverity,
    DashboardStage,
    DashboardStatus,
    EvidenceLifecycleState,
    FreshnessState,
    GapClassification,
    MissingEventClassification,
    ReadinessState,
    TriggerSurface,
    ValidationState,
)

__all__: list[str] = [
    "DashboardSeverity",
    "DashboardStage",
    "DashboardStatus",
    "EVIDENCE_COLLECTED_EVT_V1",
    "EVIDENCE_DASHBOARD_PROJECTED_EVT_V1",
    "EVIDENCE_EXTRACTED_EVT_V1",
    "EVIDENCE_GAP_ANALYZED_EVT_V1",
    "EVIDENCE_OCC_PR_CREATED_EVT_V1",
    "EVIDENCE_PIPELINE_START_CMD_V1",
    "EVIDENCE_READINESS_SCORED_EVT_V1",
    "EVIDENCE_VALIDATED_EVT_V1",
    "EvidenceLifecycleState",
    "FreshnessState",
    "GapClassification",
    "MissingEventClassification",
    "ModelCorrelationTrace",
    "ModelCorrelationTraceEvent",
    "ModelCorrelationTraceProjection",
    "ModelDashboardEvent",
    "ModelDashboardProjectionEvent",
    "ModelDeploymentReadinessResult",
    "ModelEvidenceDashboardProjection",
    "ModelEvidenceDashboardStageProjection",
    "ModelEvidenceBundle",
    "ModelEvidencePipelineCommand",
    "ModelEvidenceValidationResult",
    "ModelGapReport",
    "ModelOccPrReference",
    "ModelRawEvidencePayload",
    "ModelReadinessAggregateProjection",
    "ReadinessState",
    "TriggerSurface",
    "ValidationState",
]
