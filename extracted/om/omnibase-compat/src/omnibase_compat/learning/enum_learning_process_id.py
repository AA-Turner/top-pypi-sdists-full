# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.enums.enum_learning_process_id
# COMPAT_REMOVAL_DATE: 2027-06-01

"""EnumLearningProcessId — which automated process emitted a learning record."""

from __future__ import annotations

from enum import StrEnum


class EnumLearningProcessId(StrEnum):
    """Identifies the automated process a `ModelLearningRecord` was captured for.

    Spec: docs/plans/2026-07-06-learning-loop-generalization-spec.md §3.1.
    """

    MERGE_SWEEP = "merge_sweep"
    DELEGATION = "delegation"
    DISPATCH_WORKER = "dispatch_worker"
    CI_FIX = "ci_fix"
    STEEL = "steel"
    PLAN_GOVERNOR = "plan_governor"


__all__: list[str] = ["EnumLearningProcessId"]
