from __future__ import annotations

from enum import StrEnum
from typing import Any, ClassVar, Dict, Optional

from pydantic import ConfigDict, Field

from ....base_models.chatty_asset_model import CompanyAssetModel
from ....utils.types.identifier import StrObjectId
from ....utils.types.serializer_type import SerializerType


class AssignmentStrategy(StrEnum):
    """Assignment strategy types."""

    ROUND_ROBIN = "ROUND_ROBIN"


class AssignmentRoom(CompanyAssetModel):
    """Scope identifier for assignment configuration, rooms and logs."""

    COLLECTION: ClassVar[str] = "assignment_room"

    funnel_id: Optional[StrObjectId] = Field(default=None, alias="funnelId")
    area_id: Optional[StrObjectId] = Field(default=None, alias="areaId")
    strategy: AssignmentStrategy = Field(default=AssignmentStrategy.ROUND_ROBIN)
    state: Dict[str, Any] = Field(default_factory=dict)

    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"state"},
    }

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        populate_by_name=True,
    )


class AssignmentConfig(CompanyAssetModel):
    """Assignment configuration document stored in MongoDB."""

    COLLECTION: ClassVar[str] = "assignment_config"

    funnel_id: Optional[StrObjectId] = Field(default=None, alias="funnelId")
    area_id: Optional[StrObjectId] = Field(default=None, alias="areaId")
    strategy: AssignmentStrategy = Field(default=AssignmentStrategy.ROUND_ROBIN)
    auto_assign_on_escalation: bool = Field(default=False)
    params: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        populate_by_name=True,
    )


class AssignmentLogEntry(CompanyAssetModel):
    """Immutable record inserted into assignment_log_entry collection."""

    COLLECTION: ClassVar[str] = "assignment_log_entry"

    chat_id: StrObjectId = Field(alias="chatId")
    agent_id: StrObjectId = Field(alias="agentId")
    strategy: AssignmentStrategy
    room: AssignmentRoom

    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"room"},
    }

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        populate_by_name=True,
    )
