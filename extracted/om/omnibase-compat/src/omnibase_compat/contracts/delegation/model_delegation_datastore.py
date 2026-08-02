# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.delegation.model_delegation_datastore
# COMPAT_REMOVAL_DATE: 2027-06-01

"""Datastore contract model for delegation runtime configuration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ModelDelegationDatastore(BaseModel):
    """Datastore connection reference for projection persistence."""

    model_config = ConfigDict(frozen=True, extra="forbid", from_attributes=True)

    projection_database_ref: str = Field(
        ...,
        description="Env var reference for the projection database connection",
    )
