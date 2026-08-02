# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.enums.enum_node_kind
# COMPAT_REMOVAL_DATE: 2026-10-01

# SOURCE: omnibase_core/src/omnibase_core/enums/enum_node_kind.py
# SOURCE VERSION: omnibase-core==0.24.1
# SOURCE COMMIT: a39b9e953c73e33370a87bc3664460e29d1a729c
# Copied 2026-03-08 for omnibase_compat initial seeding.
# Downstream repos should import from omnibase_compat going forward.
#
# NOTE: Minimal StrEnum copy — omits is_core_node_type / is_infrastructure_type
# helper methods which belong to the omnibase_core implementation layer.
# Values are exact.
from enum import StrEnum


class EnumNodeKind(StrEnum):
    """High-level architectural classification for ONEX four-node architecture.

    Minimal copy for cross-repo structural compatibility.
    For full implementation with helper methods, use omnibase_core.
    """

    # Core four-node architecture types
    EFFECT = "effect"
    """External interactions (I/O): API calls, database ops, file system, message queues."""

    COMPUTE = "compute"
    """Data processing & transformation: calculations, validations, data mapping."""

    REDUCER = "reducer"
    """State aggregation & management: state machines, accumulators, event reduction."""

    ORCHESTRATOR = "orchestrator"
    """Workflow coordination: multi-step workflows, parallel execution, error recovery."""

    # Runtime infrastructure type
    RUNTIME_HOST = "runtime_host"
    """Runtime host nodes that manage node lifecycle and execution coordination."""
