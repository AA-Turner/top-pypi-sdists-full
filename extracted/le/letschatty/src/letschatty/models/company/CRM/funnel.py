from ...base_models import CompanyAssetModel, ChattyAssetPreview, ChattyAssetModel
from typing import List, Optional, ClassVar, Any
from ...utils.types.identifier import StrObjectId
from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum
from datetime import datetime
from zoneinfo import ZoneInfo
from ...utils.types.executor_types import ExecutorType
from ..assets.automation import Automation


# ============================================================================
# Enums
# ============================================================================

class FunnelStatus(StrEnum):
    """Status of a chat within a funnel"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class FunnelMemberRole(StrEnum):
    """Role of a user within a funnel"""
    ADMIN = "admin"      # Full control over funnel settings, stages, and members
    EDITOR = "editor"    # Can move chats between stages, view all chats
    VIEWER = "viewer"    # Read-only access to funnel and chats


# ============================================================================
# Embedded Models (BaseModel)
# ============================================================================

class StageTransition(BaseModel):
    """
    Record of a chat transitioning between stages within a funnel.
    Tracks the transition details and time spent in the previous stage.
    """
    from_stage_id: Optional[StrObjectId] = Field(
        default=None, 
        description="The stage the chat came from (None if entering funnel)"
    )
    to_stage_id: StrObjectId = Field(description="The stage the chat moved to")
    transitioned_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    executor_type: ExecutorType = Field(description="Type of executor that triggered the transition")
    executor_id: StrObjectId = Field(description="ID of the executor that triggered the transition")
    time_in_previous_stage_seconds: Optional[int] = Field(
        default=None, 
        description="Time spent in the previous stage before this transition"
    )
    from_stage_order: Optional[int] = Field(
        default=None,
        description="Order of the from_stage at transition time (for detecting regressions)"
    )
    to_stage_order: Optional[int] = Field(
        default=None,
        description="Order of the to_stage at transition time"
    )

    @property
    def is_regression(self) -> bool:
        """Check if this transition moved backwards in the funnel"""
        if self.from_stage_order is None or self.to_stage_order is None:
            return False
        return self.to_stage_order < self.from_stage_order

    @property
    def is_entry(self) -> bool:
        """Check if this is an entry transition (no previous stage)"""
        return self.from_stage_id is None


class ActiveFunnel(BaseModel):
    """
    Lightweight funnel state embedded in Chat for fast filtering and display.
    
    The full history (stage_transitions, time metrics) is stored in the
    separate chat_funnels collection via ChatFunnel.
    """
    chat_funnel_id: StrObjectId = Field(
        description="Reference to the full ChatFunnel document in chat_funnels collection"
    )
    funnel_id: StrObjectId = Field(description="The funnel the chat is in")
    funnel_name: str = Field(description="Denormalized funnel name for display")
    current_stage_id: StrObjectId = Field(description="Current stage ID")
    current_stage_name: str = Field(description="Denormalized stage name for display")
    entered_current_stage_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")),
        description="When the chat entered the current stage"
    )

    @property
    def time_in_current_stage_seconds(self) -> int:
        """Calculate time spent in the current stage"""
        return int((datetime.now(tz=ZoneInfo("UTC")) - self.entered_current_stage_at).total_seconds())

    def update_stage(self, stage_id: StrObjectId, stage_name: str) -> None:
        """Update the current stage (called when transitioning)"""
        self.current_stage_id = stage_id
        self.current_stage_name = stage_name
        self.entered_current_stage_at = datetime.now(tz=ZoneInfo("UTC"))


# ============================================================================
# Preview Classes - For efficient listing
# ============================================================================

class FunnelPreview(ChattyAssetPreview):
    """Preview of a Funnel for listing without full data"""
    is_active: bool = Field(default=True)
    description: Optional[str] = Field(default=None)
    created_by: Optional[StrObjectId] = Field(default=None)
    
    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        base = super().get_projection()
        base["is_active"] = 1
        base["description"] = 1
        base["created_by"] = 1
        return base

    @classmethod
    def from_asset(cls, asset: 'Funnel') -> 'FunnelPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            deleted_at=asset.deleted_at,
            is_active=asset.is_active,
            description=asset.description,
            created_by=asset.created_by
        )


class FunnelStagePreview(ChattyAssetPreview):
    """Preview of a FunnelStage for listing"""
    funnel_id: StrObjectId
    color: str
    order: int
    is_exit_stage: bool = Field(default=False)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        base = super().get_projection()
        base.update({
            "funnel_id": 1,
            "color": 1,
            "order": 1,
            "is_exit_stage": 1
        })
        return base

    @classmethod
    def from_asset(cls, asset: 'FunnelStage') -> 'FunnelStagePreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            deleted_at=asset.deleted_at,
            funnel_id=asset.funnel_id,
            color=asset.color,
            order=asset.order,
            is_exit_stage=asset.is_exit_stage
        )


# ============================================================================
# Company Assets (CompanyAssetModel) - Stored in separate collections
# ============================================================================

class Funnel(CompanyAssetModel):
    """
    A funnel represents a pipeline/process for managing chats (e.g., sales funnel, support pipeline).
    Companies can create multiple funnels to organize their chat workflows.
    """
    name: str = Field(description="Name of the funnel")
    description: Optional[str] = Field(default=None, description="Description of the funnel's purpose")
    created_by: StrObjectId = Field(description="User ID who created the funnel")
    is_active: bool = Field(default=True, description="Whether the funnel is active or archived")

    preview_class: ClassVar[type[FunnelPreview]] = FunnelPreview

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True
    )

    def embedding_chunks(self) -> list[dict[str, str]]:
        from ..assets.embeddable import build_chunks
        return build_chunks("funnel", {"name": self.name, "description": self.description})


class FunnelStage(CompanyAssetModel):
    """
    A stage within a funnel. Stages are ordered and can have automations
    that execute when a chat enters the stage.
    """
    funnel_id: StrObjectId = Field(frozen=True, description="The funnel this stage belongs to")
    name: str = Field(description="Name of the stage")
    description: Optional[str] = Field(default=None, description="Description of the stage")
    color: str = Field(default="#808080", description="Hex color for the stage (e.g., '#FFAA00')")
    order: int = Field(ge=0, description="Position of the stage in the funnel (0-indexed)")
    inflexion_conversion_point: bool = Field(
        default=False, 
        description="If true, prioritized for chat assignment and sends notifications in automatic mode"
    )
    is_exit_stage: bool = Field(
        default=False,
        description="If true, moving to this stage completes the funnel for the chat"
    )
    automations: Automation = Field(
        default_factory=Automation,
        description="Automations to execute when a chat enters this stage"
    )

    preview_class: ClassVar[type[FunnelStagePreview]] = FunnelStagePreview

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True
    )


class FunnelMember(CompanyAssetModel):
    """
    A user's membership in a funnel with their assigned role.
    Determines what actions the user can perform within the funnel.
    """
    name: str = Field(default="Funnel Member", description="Name for asset compatibility")
    funnel_id: StrObjectId = Field(frozen=True, description="The funnel this membership belongs to")
    user_id: StrObjectId = Field(frozen=True, description="The user who is a member")
    role: FunnelMemberRole = Field(description="The user's role within the funnel")

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True
    )

    @property
    def can_edit(self) -> bool:
        """Check if the member can edit (move chats, etc.)"""
        return self.role in (FunnelMemberRole.ADMIN, FunnelMemberRole.EDITOR)

    @property
    def can_admin(self) -> bool:
        """Check if the member can administer the funnel"""
        return self.role == FunnelMemberRole.ADMIN


# ============================================================================
# ChatFunnel - Stored in separate chat_funnels collection
# This is a ChattyAssetModel (not CompanyAssetModel) because it's a chat history
# record rather than a company-level asset.
# ============================================================================

class ChatFunnel(ChattyAssetModel):
    """
    Full record of a chat's journey through a funnel.
    Stored in a separate 'chat_funnels' collection, NOT embedded in chat.
    
    This extends ChattyAssetModel (not CompanyAssetModel) because it's a 
    chat-level record tracking funnel history, not a company-owned asset.
    
    A new ChatFunnel is created each time a chat enters a funnel.
    If a chat completes a funnel and enters it again, a NEW ChatFunnel is created.
    
    The Chat document stores a lightweight ActiveFunnel for fast
    filtering and display, with a reference to this full record.
    """
    company_id: StrObjectId = Field(frozen=True, description="Company for multi-tenant isolation")
    chat_id: StrObjectId = Field(frozen=True, description="The chat this funnel record belongs to")
    funnel_id: StrObjectId = Field(frozen=True, description="The funnel the chat entered")
    status: FunnelStatus = Field(default=FunnelStatus.IN_PROGRESS)
    started_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    completed_at: Optional[datetime] = Field(default=None)
    abandoned_at: Optional[datetime] = Field(default=None)
    current_stage_id: Optional[StrObjectId] = Field(
        default=None, 
        description="Current stage ID (None if funnel is completed/abandoned)"
    )
    entered_current_stage_at: Optional[datetime] = Field(
        default=None,
        description="When the chat entered the current stage"
    )
    stage_transitions: List[StageTransition] = Field(
        default_factory=list,
        description="Complete history of all stage transitions"
    )

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True
    )

    @property
    def is_completed(self) -> bool:
        """Check if the chat has completed the funnel"""
        return self.status == FunnelStatus.COMPLETED and self.completed_at is not None

    @property
    def is_abandoned(self) -> bool:
        """Check if the chat has abandoned the funnel"""
        return self.status == FunnelStatus.ABANDONED and self.abandoned_at is not None

    @property
    def is_active(self) -> bool:
        """Check if the chat is still active in the funnel"""
        return self.status == FunnelStatus.IN_PROGRESS

    @property
    def time_in_funnel_seconds(self) -> int:
        """Calculate total time spent in the funnel"""
        end_time = self.completed_at or self.abandoned_at or datetime.now(tz=ZoneInfo("UTC"))
        return int((end_time - self.started_at).total_seconds())

    @property
    def time_in_current_stage_seconds(self) -> Optional[int]:
        """Calculate time spent in the current stage"""
        if not self.entered_current_stage_at or not self.current_stage_id:
            return None
        end_time = self.completed_at or self.abandoned_at or datetime.now(tz=ZoneInfo("UTC"))
        return int((end_time - self.entered_current_stage_at).total_seconds())
        
    @property
    def unique_stages_visited(self) -> int:
        """Count of unique stages the chat has visited"""
        return len(set(t.to_stage_id for t in self.stage_transitions))

    @property
    def total_transitions(self) -> int:
        """Total number of stage transitions"""
        return len(self.stage_transitions)

    @property
    def regression_count(self) -> int:
        """Count of times the chat moved backwards in the funnel"""
        return sum(1 for t in self.stage_transitions if t.is_regression)

    @property
    def last_transition(self) -> Optional[StageTransition]:
        """Get the most recent stage transition"""
        return self.stage_transitions[-1] if self.stage_transitions else None

    def record_transition(
        self,
        to_stage_id: StrObjectId,
        executor_type: ExecutorType,
        executor_id: StrObjectId,
        from_stage_order: Optional[int] = None,
        to_stage_order: Optional[int] = None
    ) -> StageTransition:
        """
        Record a transition to a new stage.
        Returns the created StageTransition.
        
        Args:
            to_stage_id: The stage to transition to
            executor_type: Who/what triggered the transition
            executor_id: ID of the executor
            from_stage_order: Order of current stage (for regression detection)
            to_stage_order: Order of target stage (for regression detection)
        """
        time_in_previous = self.time_in_current_stage_seconds
        
        transition = StageTransition(
            from_stage_id=self.current_stage_id,
            to_stage_id=to_stage_id,
            executor_type=executor_type,
            executor_id=executor_id,
            time_in_previous_stage_seconds=time_in_previous,
            from_stage_order=from_stage_order,
            to_stage_order=to_stage_order
        )
        
        self.stage_transitions.append(transition)
        self.current_stage_id = to_stage_id
        self.entered_current_stage_at = transition.transitioned_at
        
        return transition

    def complete(self) -> None:
        """Mark the funnel as completed"""
        self.status = FunnelStatus.COMPLETED
        self.completed_at = datetime.now(tz=ZoneInfo("UTC"))

    def abandon(self) -> None:
        """Mark the funnel as abandoned"""
        self.status = FunnelStatus.ABANDONED
        self.abandoned_at = datetime.now(tz=ZoneInfo("UTC"))

    def to_active_funnel(self, funnel_name: str, stage_name: str) -> ActiveFunnel:
        """
        Create an ActiveFunnel for embedding in the Chat document.
        Call this after creating/updating the ChatFunnel.
        
        Args:
            funnel_name: Name of the funnel (for denormalization)
            stage_name: Name of the current stage (for denormalization)
        """
        if not self.current_stage_id or not self.entered_current_stage_at:
            raise ValueError("Cannot create ActiveFunnel without current stage")
        
        return ActiveFunnel(
            chat_funnel_id=self.id,
            funnel_id=self.funnel_id,
            funnel_name=funnel_name,
            current_stage_id=self.current_stage_id,
            current_stage_name=stage_name,
            entered_current_stage_at=self.entered_current_stage_at
        )
