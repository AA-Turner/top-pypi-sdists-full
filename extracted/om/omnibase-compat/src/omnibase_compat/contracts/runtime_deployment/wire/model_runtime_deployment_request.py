# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.runtime_deployment.wire
# COMPAT_REMOVAL_DATE: 2027-06-01

"""ModelRuntimeDeploymentRequest — runtime deployment request wire DTO.

Transiently mirrors the OCC-owned wire schema
(onex_change_control/src/onex_change_control/wire_schemas/
runtime_deployment_request_v1.yaml, topic onex.cmd.omnimarket.redeploy-start.v1).
OCC owns the source of truth; compat is temporary (OMN-12576).
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnibase_compat.contracts.runtime_deployment.wire.types import EnumRuntimeLane


class ModelRuntimeDeploymentRequest(BaseModel):
    """Lane/digest/promotion deployment request consumed by node_redeploy.

    image_digest and promotion_batch_id are optional on the request (the dev
    lane builds from a ref); production pins both to the digest proven READY in
    stability-test before publishing the request.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", from_attributes=True)

    correlation_id: UUID = Field(
        ..., description="Deployment run correlation ID shared by all deployment events."
    )
    deployment_id: UUID = Field(..., description="Stable identifier for this deployment attempt.")
    runtime_lane: EnumRuntimeLane = Field(..., description="Target runtime lane.")
    source_branch: str = Field(
        ..., min_length=1, description="Branch that triggered the deployment."
    )
    source_sha: str = Field(..., min_length=1, description="Exact source commit SHA to deploy.")
    requested_by: str = Field(
        ..., min_length=1, description="Identity of the requesting workflow or operator."
    )
    requested_at: datetime = Field(..., description="When the deployment request was issued.")
    promotion_batch_id: str | None = Field(
        default=None,
        description="Promotion batch identifier shared with OCC evidence; required for prod.",
    )
    image_ref: str | None = Field(
        default=None,
        description="Mutable image reference. The digest is the authority, not the ref.",
    )
    image_digest: str | None = Field(
        default=None,
        description=(
            "Immutable image digest. Required for prod; pinned to the stability-test READY digest."
        ),
    )
    deployment_reason: str | None = Field(
        default=None, description="Human-readable trigger reason."
    )
    requires_occ: bool = Field(
        default=False, description="Whether OCC evidence drafting is required for this lane."
    )
    requires_readiness_gate: bool = Field(
        default=False,
        description="Whether the readiness gate must pass before the lane is READY.",
    )


__all__: list[str] = ["ModelRuntimeDeploymentRequest"]
