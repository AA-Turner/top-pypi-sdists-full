from __future__ import annotations

from typing import Any

from pydantic import Field

from capsule_sdk.models.common import CapsuleModel


class BuilderVMDelete(CapsuleModel):
    chain_build_id: str
    instance_name: str
    zone: str


class BuilderTasksResponse(CapsuleModel):
    create: list[dict[str, Any]] = Field(default_factory=list)
    delete: list[BuilderVMDelete] = Field(default_factory=list)
