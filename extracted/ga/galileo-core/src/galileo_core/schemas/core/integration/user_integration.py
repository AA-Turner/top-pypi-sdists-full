from galileo_core.schemas.core.collaborator import UserCollaboratorCreate


class UserIntegrationCollaboratorResponse(UserCollaboratorCreate):
    email: str
