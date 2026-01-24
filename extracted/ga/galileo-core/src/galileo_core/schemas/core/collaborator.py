from pydantic import UUID4, BaseModel

from galileo_core.schemas.core.collaboration_role import CollaboratorRole


class CollaboratorCreateBase(BaseModel):
    role: CollaboratorRole = CollaboratorRole.viewer


class UserCollaboratorCreate(CollaboratorCreateBase):
    user_id: UUID4


class GroupCollaboratorCreate(CollaboratorCreateBase):
    group_id: UUID4
