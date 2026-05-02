from pydantic import BaseModel, Field, model_validator
from typing import List, ClassVar
from ....utils.definitions import Area
from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.base_models.ai_agent_component import AiAgentComponent, AiAgentComponentPreview
import logging

logger = logging.getLogger(__name__)

class FollowUpStrategy(AiAgentComponent):
    """Individual context item with title and content"""
    maximum_consecutive_follow_ups: int = Field(default=3, description="Maximum number of consecutive follow ups to be executed")
    maximum_follow_ups_to_be_executed: int = Field(default=3, description="Maximum number of follow ups to be executed in total")
    instructions_and_goals: str = Field(description="The detailed instructions for the follow up and the goals to be achieved")
    contexts: List[StrObjectId] = Field(default_factory=list, description="Specific knowleadge base for the follow ups")
    examples: List[StrObjectId] = Field(default_factory=list, description="Specific examples of follow ups")
    only_on_weekdays: bool = Field(default=False, description="If true, the follow up will only be executed on weekdays")
    templates_allowed: bool = Field(default=False, description="If true, the agent will send templates if the free conversation window is closed in order to perform the follow up")
    follow_up_intervals_minutes: List[int] = Field(
        default=[2, 24, 72],
        description="Minutes between follow-ups [1st, 2nd, 3rd, ...]. If more follow-ups than intervals, uses last interval."
    )
    area_after_reaching_max : Area = Field(default=Area.WAITING_AGENT, description="The area where the chat will be transferred after reaching the maximum number of follow ups")
    preview_class: ClassVar[type[AiAgentComponentPreview]] = AiAgentComponentPreview

    def get_interval_for_followup(self, followup_number: int) -> int:
        """Get interval for specific follow-up number (1-indexed)"""
        if followup_number <= len(self.follow_up_intervals_minutes):
            return self.follow_up_intervals_minutes[followup_number - 1]

        return self.follow_up_intervals_minutes[-1]

    @model_validator(mode='after')
    def validate_intervals_consistency(self):
        """Ensure follow_up_intervals_minutes length matches maximum_consecutive_follow_ups"""
        if len(self.follow_up_intervals_minutes) != self.maximum_consecutive_follow_ups:
            raise ValueError(
                f"follow_up_intervals_minutes must have exactly {self.maximum_consecutive_follow_ups} items "
                f"to match maximum_consecutive_follow_ups, got {len(self.follow_up_intervals_minutes)} items"
            )
        return self


    @classmethod
    def example(cls) -> dict:
        return {
            "id": "507f1f77bcf86cd799439011",
            "name": "Follow up strategy",
            "start_time": "2021-01-01T00:00:00Z",
            "end_time": "2021-01-01T00:00:00Z",
            "created_at": "2021-01-01T00:00:00Z",
            "maximum_consecutive_follow_ups": 3,
            "maximum_follow_ups_to_be_executed": 5,
            "follow_up_intervals_minutes": [2, 24, 72],  # 2h, 1d, 3d
            "instructions_and_goals": "Follow up on proposal, answer questions, close deal",
            "examples": ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"],
            "contexts": ["507f1f77bcf86cd799439013", "507f1f77bcf86cd799439014"],
            "only_on_weekdays": True,
            "templates_allowed": False
        }

