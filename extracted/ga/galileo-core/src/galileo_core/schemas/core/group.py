from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from galileo_core.schemas.core.group_role import GroupRole
from galileo_core.schemas.core.group_visibility import GroupVisibility


class CreateGroupRequest(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: GroupVisibility = GroupVisibility.public


class CreateGroupResponse(CreateGroupRequest):
    id: UUID4
    created_at: datetime


class AddGroupMemberRequest(BaseModel):
    user_id: UUID4
    role: GroupRole = GroupRole.member


class AddGroupMemberResponse(BaseModel):
    user_id: UUID4
    group_role: GroupRole
