# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat — thin shared structural package.

Zero omnibase_core dependency.

Contains only:
- shared structural DTOs (wire/event models)
- shared enums
- primitive shared types
- experimental schemas
- transitional structural artifacts with explicit retirement metadata

Does not contain runtime behavior, persistence logic, network clients,
service orchestration, convenience helpers, or implementation-facing adapters.
Those belong in omnibase_spi (interface contracts) or omnibase_infra (implementations).
"""

__version__ = "0.5.2"

from omnibase_compat.routing.model_routing_degraded_event import ModelRoutingDegradedEvent
from omnibase_compat.routing.model_routing_policy import ModelCiOverridePolicy, ModelRoutingPolicy

__all__: list[str] = [
    "ModelCiOverridePolicy",
    "ModelRoutingPolicy",
    "ModelRoutingDegradedEvent",
]
