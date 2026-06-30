# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""AutoPilot progressive rollout orchestration package.

This package contains the business logic for the 5 autopilot subcommands:

- `auto_start`: Start INITIALIZED rollouts (gate: `autopilotConfig.autoStart`)
- `auto_advance`: Advance IN_PROGRESS rollouts within current tier (no gate)
- `auto_promote`: Promote across tiers when 100% and healthy (gate: `autopilotConfig.autoPromoteStages`)
- `auto_triage_failed`: Log all failures, unpin if safe (no gate)
- `auto_rollback_failed`: Full rollback/cancel (gate: version not in `unsafeDowngrades`)
"""

from airbyte_ops_mcp.connector_ops.rollouts.autopilot import (
    run_auto_advance,
    run_auto_promote,
    run_auto_rollback_failed,
    run_auto_start,
    run_auto_triage_failed,
)
from airbyte_ops_mcp.connector_ops.rollouts.models import (
    AutopilotAction,
    AutopilotResult,
    ConnectorRolloutRecord,
    CustomerTierFilter,
    RolloutFilters,
)

__all__ = [
    "AutopilotAction",
    "AutopilotResult",
    "ConnectorRolloutRecord",
    "CustomerTierFilter",
    "RolloutFilters",
    "run_auto_advance",
    "run_auto_promote",
    "run_auto_rollback_failed",
    "run_auto_start",
    "run_auto_triage_failed",
]
