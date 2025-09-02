from ...base_models import CompanyAssetModel
from typing import List
from ...utils.types.identifier import StrObjectId
from pydantic import BaseModel, Field
from enum import StrEnum
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from ...utils.types.executor_types import ExecutorType

class FunnelStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class StageTransition(BaseModel):
    from_stage_id: Optional[StrObjectId] = None
    to_stage_id: StrObjectId
    transitioned_at: datetime = Field(default=datetime.now(ZoneInfo("UTC")))
    executor_type: ExecutorType
    executor_id: StrObjectId
    time_in_previous_stage_seconds: Optional[int] = None

class ClientFunnel(CompanyAssetModel):
    funnel_id: StrObjectId
    status: FunnelStatus
    started_at: datetime = Field(default=datetime.now(ZoneInfo("UTC")))
    completed_at: Optional[datetime] = None
    abandoned_at: Optional[datetime] = None
    current_stage_id: Optional[StrObjectId] = None
    entered_current_stage_at: datetime
    stage_transitions: List[StageTransition] = Field(default_factory=list)

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    @property
    def is_abandoned(self) -> bool:
        return self.abandoned_at is not None

    @property
    def time_in_funnel_seconds(self) -> int:
        end_time = self.completed_at or self.abandoned_at or datetime.now(tz=ZoneInfo("UTC"))
        return int((end_time - self.started_at).total_seconds())

    @property
    def time_in_current_stage_seconds(self) -> Optional[int]:
        if not self.entered_current_stage_at:
            return None
        return int((datetime.now(tz=ZoneInfo("UTC")) - self.entered_current_stage_at).total_seconds())

    @property
    def unique_stages_visited(self) -> int:
        return len(set(t.to_stage_id for t in self.stage_transitions))

class FunnelStage(CompanyAssetModel):
    name: str
    description: str
    index: int
    inflexion_conversion_point: bool = Field(default=False, description="If true, it'll be prioritized for chat assignment and will send notifications in automatic mode to all agents.")
    workflow_ids: List[StrObjectId] = Field(default_factory=list)


class Funnel(CompanyAssetModel):
    name: str
    description: str
    stages: List[FunnelStage]
    assignment_priority: int = Field(ge=0, le=10, description="Priority for chat assignment, between funnels")
