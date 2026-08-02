# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Shared literal types for evidence pipeline DTOs."""

from __future__ import annotations

from typing import Literal

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type EvidenceLifecycleState = Literal[
    "PROVISIONAL",
    "VALIDATED",
    "FINALIZED",
    "SUPERSEDED",
    "REJECTED",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type GapClassification = Literal[
    "MISSING",
    "STALE",
    "SUPERSEDED",
    "HASH_MISMATCH",
    "RECEIPT_MISSING",
    "VALIDATION_FAILED",
    "UNKNOWN",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type ReadinessState = Literal[
    "READY",
    "BLOCKED",
    "DEGRADED",
    "ADVISORY_ONLY",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type DashboardSeverity = Literal[
    "INFO",
    "WARNING",
    "ERROR",
    "BLOCKING",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type DashboardStage = Literal[
    "TRIGGERED",
    "COLLECTED",
    "EXTRACTED",
    "VALIDATED",
    "OCC_PR",
    "COMPLETED",
    "BLOCKED",
    "READINESS_GATE_STARTED",
    "READINESS_GATE_COMPLETED",
    "READINESS_GATE_BLOCKED",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type DashboardStatus = Literal[
    "PENDING",
    "IN_FLIGHT",
    "PASSED",
    "FAILED",
    "BLOCKED",
    "STALE",
    "DEGRADED",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type FreshnessState = Literal[
    "CURRENT",
    "STALE",
    "DEGRADED",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type MissingEventClassification = Literal[
    "DELAYED",
    "STALE",
    "MISSING",
    "SUPERSEDED",
    "INVALID_ORDER",
    "PROJECTION_GAP",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type TriggerSurface = Literal[
    "pull_request_merge",
    "merge_group",
    "deploy",
    "manual",
    "runtime_event",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type ValidationState = Literal[
    "PASSED",
    "FAILED",
    "ADVISORY_ONLY",
]

__all__: list[str] = [
    "DashboardSeverity",
    "DashboardStage",
    "DashboardStatus",
    "EvidenceLifecycleState",
    "FreshnessState",
    "GapClassification",
    "MissingEventClassification",
    "ReadinessState",
    "TriggerSurface",
    "ValidationState",
]
