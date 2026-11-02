from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCloneRequest(BaseModel):
    name: str = Field(description="Name for the new project.")
    target_owner_email: str | None = Field(
        default=None,
        description=(
            "Email of the user who should own the cloned project. "
            "When omitted the caller owns the clone. Requires the target "
            "user to already exist in the platform."
        ),
    )


class ProjectCloneResponse(BaseModel):
    project_id: UUID = Field(description="UUID of the newly-created project")
    chat_project_id: UUID = Field(
        description="UUID of the persona-owned child project that holds the "
        "cloned session and must receive subsequent web chat writes."
    )
    world_model_id_map: dict[UUID, UUID] = Field(
        default_factory=dict,
        description="Mapping of old -> new world_model UUIDs for every row that belonged to the source project",
    )


class ChatCloneRequest(BaseModel):
    """Admin-only request to clone a chat session's full message history into another project.

    The caller must supply a ``world_model_id_map`` covering every
    ``world_model_id`` referenced by the source session's conversations. Missing
    ids cause the request to fail with 422 rather than being silently dropped.
    """

    source_session_id: UUID = Field(
        description="UUID of the session to copy conversations from"
    )
    limit: int | None = Field(
        ge=1,
        default=None,
        description="Messages will only be copied up to this limit.",
    )
    target_project_id: UUID = Field(
        description="UUID of the project the new session will be created under"
    )
    world_model_id_map: dict[UUID, UUID] = Field(
        default_factory=dict,
        description=(
            "Old -> new world_model_id mapping. Must include every world_model_id "
            "referenced by the source session's conversations."
        ),
    )


class ChatCloneResponse(BaseModel):
    session_id: UUID = Field(description="UUID of the new cloned session")
    message_count: int = Field(
        description="Number of conversation rows copied from the source session"
    )
