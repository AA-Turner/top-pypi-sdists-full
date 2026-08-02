# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.learning — wire DTOs for the cross-process learning loop.

Zero upstream runtime deps. Captures one outcome record per automated
decision (merge sweep, delegation, dispatch worker, ci fix, steel, plan
governor) so a read-back mechanism can change a future decision.
See docs/plans/2026-07-06-learning-loop-generalization-spec.md.
"""

from omnibase_compat.learning.enum_failure_class import EnumFailureClass
from omnibase_compat.learning.enum_learning_process_id import EnumLearningProcessId
from omnibase_compat.learning.model_learning_record import (
    EnumLearningOutcome,
    ModelLearningRecord,
)

__all__: list[str] = [
    "EnumFailureClass",
    "EnumLearningOutcome",
    "EnumLearningProcessId",
    "ModelLearningRecord",
]
