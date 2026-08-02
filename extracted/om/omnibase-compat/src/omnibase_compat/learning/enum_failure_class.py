# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.enums.enum_failure_class
# COMPAT_REMOVAL_DATE: 2027-06-01

"""EnumFailureClass — shared failure-class taxonomy for learning records."""

from __future__ import annotations

from enum import StrEnum


class EnumFailureClass(StrEnum):
    """Shared taxonomy of failure classes across automated processes.

    Spec: docs/plans/2026-07-06-learning-loop-generalization-spec.md §3.4.
    Small and shared on purpose — every automated process (merge sweep,
    delegation, dispatch, ci fix, steel, plan governor) classifies its
    failures into this one enum so read-back logic stays cross-process.
    """

    NETWORK_EGRESS_TIMEOUT = "network_egress_timeout"
    RUNNER_CAPACITY_STARVATION = "runner_capacity_starvation"
    QUEUE_SCHEDULING_STALL = "queue_scheduling_stall"
    FLAKY_CHECK_CANCELLED = "flaky_check_cancelled"
    GENUINE_CODE_FAILURE = "genuine_code_failure"
    CONTRACT_GATE_VIOLATION = "contract_gate_violation"
    OCC_COMPANION_DEFECT = "occ_companion_defect"
    ENV_INSTALL_DRIFT = "env_install_drift"
    AUTH_SCOPE_MISSING = "auth_scope_missing"
    UPSTREAM_THROTTLE = "upstream_throttle"


__all__: list[str] = ["EnumFailureClass"]
