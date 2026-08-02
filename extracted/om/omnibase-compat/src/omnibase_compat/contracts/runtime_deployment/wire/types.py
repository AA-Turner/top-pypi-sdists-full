# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.runtime_deployment.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01

"""Shared types for runtime deployment wire DTOs.

Transiently mirrors the OCC-owned wire schema
(onex_change_control/src/onex_change_control/wire_schemas/
runtime_deployment_request_v1.yaml). OCC owns the source of truth; this lane
enum graduates to omnibase_core once >=2 repos import it (OMN-12576).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

type ProbeStatus = Literal["pass", "fail"]
type DeploymentProofStatus = Literal["success", "failed"]


class EnumRuntimeLane(StrEnum):
    """Runtime lane targeted by a deployment request or proof.

    Values match the OCC wire schema enum and the live ``.201`` runtime lanes:
    dev (8085/8086, omnibase-infra), stability-test (18085/18086,
    omnibase-infra-stability-test), prod (28085/28086, omnibase-infra-prod).
    """

    DEV = "dev"
    STABILITY_TEST = "stability-test"
    PROD = "prod"


__all__: list[str] = [
    "DeploymentProofStatus",
    "EnumRuntimeLane",
    "ProbeStatus",
]
