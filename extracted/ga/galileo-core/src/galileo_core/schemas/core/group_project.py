from pydantic import UUID4, BaseModel

from galileo_core.schemas.core.collaboration_role import CollaboratorRole


class GroupProjectCollaboratorRequest(BaseModel):
    role: CollaboratorRole
    group_id: UUID4


class GroupProjectCollaboratorResponse(GroupProjectCollaboratorRequest):
    group_name: str
