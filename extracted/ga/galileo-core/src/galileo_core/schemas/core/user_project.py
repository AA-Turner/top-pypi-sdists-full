from pydantic import UUID4, BaseModel

from galileo_core.schemas.core.collaboration_role import CollaboratorRole


class UserProjectCollaboratorRequest(BaseModel):
    role: CollaboratorRole
    user_id: UUID4


class UserProjectCollaboratorResponse(UserProjectCollaboratorRequest):
    user_id: UUID4
    email: str
