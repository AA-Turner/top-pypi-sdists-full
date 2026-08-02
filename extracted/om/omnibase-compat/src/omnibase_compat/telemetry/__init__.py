# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.telemetry — wire types for session-level telemetry reporting.

Exports cross-repo observable artifacts for sweep skill runs.
Zero upstream runtime deps.
"""

from omnibase_compat.telemetry.model_sweep_result import ModelSweepResult

__all__ = [
    "ModelSweepResult",
]
