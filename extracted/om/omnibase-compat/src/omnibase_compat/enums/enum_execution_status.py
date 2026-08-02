# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.enums.enum_execution_status
# COMPAT_REMOVAL_DATE: 2026-10-01

# SOURCE: omnibase_core/src/omnibase_core/enums/enum_execution_status.py
# SOURCE VERSION: omnibase-core==0.24.1
# SOURCE COMMIT: a39b9e953c73e33370a87bc3664460e29d1a729c
# Copied 2026-03-08 for omnibase_compat initial seeding.
# Downstream repos should import from omnibase_compat going forward.
#
# NOTE: Minimal StrEnum copy — omits to_base_status, from_base_status and all
# helper classmethods (is_terminal, is_active, etc.) which have omnibase_core
# dependencies. Values are exact.
from enum import StrEnum


class EnumExecutionStatus(StrEnum):
    """Canonical execution status enum for ONEX lifecycle tracking.

    Minimal copy for cross-repo structural compatibility.
    For full implementation with helper methods, use omnibase_core.

    Consolidated from EnumExecutionStatusV2 (OMN-1310).
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    PARTIAL = "partial"
