from datetime import datetime
from enum import StrEnum, auto
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, JsonValue


class SetWarmPoolResponse(BaseModel):
    """Observed warm pool state after a resize."""

    crow_key: str
    node_pool: str
    replicas: int = Field(description="Target replica count now set on the pool.")
    ready_replicas: int = Field(
        description="Pods reporting Ready as of the last observation."
    )
    waited: bool = Field(description="Whether the server polled for readiness.")
    timed_out: bool = Field(
        default=False,
        description="True when the wait budget elapsed before ready_replicas "
        "reached replicas. The resize itself still applied.",
    )


class FinalEnvironmentRequest(BaseModel):
    status: str


class StoreAgentStatePostRequest(BaseModel):
    agent_id: str
    step: str
    state: JsonValue
    trajectory_timestep: int


class StoreEnvironmentFrameRequest(BaseModel):
    agent_state_point_in_time: str
    current_agent_step: str
    state: JsonValue
    trajectory_timestep: int


# v0.2 init/finalize: state payload is uploaded by the client to object storage
# via a signed URL, not sent through the API. v0.2 only supports gzip blobs —
# the server's object key is hard-coded to ``.json.gz``.
StateContentEncoding = Literal["gzip"]


# ``id`` is a client-supplied idempotency key. The server creates the row
# (and derives the object key) from it, so retrying an init whose response
# was lost returns the same row instead of orphaning a duplicate PENDING one.
class AgentStateInitRequest(BaseModel):
    id: UUID
    agent_id: str
    trajectory_timestep: int
    step: str
    content_encoding: StateContentEncoding = "gzip"
    size_bytes: int | None = None


class EnvironmentFrameInitRequest(BaseModel):
    id: UUID
    agent_state_point_in_time: str
    current_agent_step: str
    trajectory_timestep: int | None = None
    metadata: JsonValue | None = None
    content_encoding: StateContentEncoding = "gzip"
    size_bytes: int | None = None


class StateUploadInitResponse(BaseModel):
    id: UUID
    upload_url: str
    object_path: str
    expires_in_seconds: int


class StateFinalizeRequest(BaseModel):
    size_bytes: int | None = None


class ShareStatus(StrEnum):
    PRIVATE = auto()
    PUBLIC = auto()
    SHARED = auto()


class PermittedAccessors(BaseModel):
    """Permitted accessors for trajectories and projects."""

    users: list[str] | None = Field(
        default=None,
        description="List of user emails to grant access",
    )
    organizations: list[str | int] | None = Field(
        default=None,
        description="List of organization IDs to grant access",
    )


class TrajectoryPatchRequest(BaseModel):
    share_status: ShareStatus | None = Field(
        default=None,
        description="Share status for the trajectory: private, shared, or public. None implies no change.",
    )
    permitted_accessors: PermittedAccessors | None = Field(
        default=None,
        description="Permitted accessors for the trajectory. Only valid when share_status is SHARED.",
    )
    notification_enabled: bool | None = None
    notification_type: str | None = None
    min_estimated_time: float | None = None
    max_estimated_time: float | None = None


class ExecutionStatus(StrEnum):
    QUEUED = auto()
    IN_PROGRESS = "in progress"
    FAIL = auto()
    SUCCESS = auto()
    CANCELLED = auto()
    TRUNCATED = auto()

    def is_terminal_state(self) -> bool:
        return self in self.terminal_states()

    @classmethod
    def terminal_states(cls) -> set["ExecutionStatus"]:
        return {cls.SUCCESS, cls.FAIL, cls.CANCELLED, cls.TRUNCATED}


class ContentLocation(StrEnum):
    INLINE = auto()
    DATA_STORAGE = auto()


class WorldModel(BaseModel):
    """
    Payload for creating a new world model snapshot.

    This model is sent to the API.
    """

    content: str
    content_location: ContentLocation = ContentLocation.INLINE
    prior: UUID | str | None = None
    name: str | None = None
    description: str | None = None
    trajectory_id: UUID | str | None = None
    model_metadata: JsonValue | None = None
    project_id: UUID | str | None = None


class SearchOperator(StrEnum):
    """Operators for structured search criteria."""

    EQUALS = "equals"
    CONTAINS = "contains"  # Exact phrase/substring matching
    FULLTEXT = "fulltext"  # Tokenized full-text search (match query)
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    BETWEEN = "between"
    IN = "in"


class SearchCriterion(BaseModel):
    """A single search criterion with field, operator, and value."""

    field: str
    operator: SearchOperator
    value: str | list[str] | bool


class FilterLogic(StrEnum):
    AND = "AND"
    OR = "OR"


class WorldModelSearchPayload(BaseModel):
    """Payload for structured world model search."""

    criteria: list[SearchCriterion]
    size: int = 10
    project_id: UUID | str | None = None
    search_all_versions: bool = False


class WorldModelResponse(WorldModel):
    """
    Response model for a world model snapshot.

    This model is received from the API.
    """

    id: UUID | str
    name: str  # type: ignore[mutable-override]  # The API always returns a non-optional name, overriding the base model's optional field.
    email: str | None
    enabled: bool
    created_at: datetime
    data_storage_id: UUID | None = None


class WorldModelCreateResponse(BaseModel):
    """Response for creating a world model.

    For inline content: only id is populated
    For data_storage-backed content: includes data_storage_id and signed_url for upload
    """

    id: UUID
    signed_url: str | None = None
    data_storage_id: UUID | None = None


class DiscoveryResponse(BaseModel):
    """Response model for a discovery request. This model is received from the API."""

    discovery_id: UUID | str
    project_id: UUID | str
    world_model_id: UUID | str
    dataset_id: UUID | str
    description: str
    associated_trajectories: list[UUID | str]
    validation_level: int
    created_at: datetime


class DataStorageSearchPayload(BaseModel):
    """Payload for structured data storage search."""

    criteria: list[SearchCriterion]
    limit: int = 10
    offset: int = 0
    filter_logic: FilterLogic = FilterLogic.OR
    text_query: str | None = None
    highlight: bool = False
    highlight_fields: list[str] | None = None
    highlight_fragment_size: int = 1000
    highlight_num_fragments: int = 3
