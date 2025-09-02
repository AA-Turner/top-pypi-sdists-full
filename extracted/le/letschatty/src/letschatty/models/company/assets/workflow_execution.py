from __future__ import annotations
from datetime import timedelta
from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.base_models.chatty_asset_model import CompanyAssetModel
from zoneinfo import ZoneInfo
import logging

if TYPE_CHECKING:
    from letschatty.models.chat.flow_link_state import FlowStateAssignedToChat
logger = logging.getLogger("logger")

from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field

class ExecutedStatus(StrEnum):
    """
    Enum representing the possible execution statuses of a flow.
    """
    ALTERNATIVE = "alternative" #The flow executed the alternative actions (plan B)
    SUCCESS = "success" #The flow executed the actions (plan A)
    WAIT = "wait" #The result is wait because 1 or more conditions are not met (non critical)
    ERROR = "error" #The result was an error that needs to be handled
    EARLY_CONDITION = "early_condition" #The flow raised an early condition error meaning that a time condition was not met so we know how much time to wait before retrying
    FLOW_ACTION_ERROR = "flow_action_error" #The flow raised an error meaning that an action failed


class ExecutionFlowResult(BaseModel):
    """
    Model representing the result of a flow execution.

    Attributes:
        status (ExecutedStatus): The status of the flow execution.
        time_pause (datetime.timedelta): The time to pause before the next execution attempt.
    """
    status: ExecutedStatus
    time_pause: timedelta = Field(
        default_factory=lambda: timedelta(minutes=5)
    )

class WorkflowExecution(CompanyAssetModel):
    """This class is used to reflect the history of a workflow execution."""
    name: str
    assigned_at: datetime = Field()
    workflow_id: StrObjectId = Field()
    chat_id: StrObjectId = Field()
    started_at: datetime = Field()
    result: Optional[ExecutedStatus] = Field(default=None)
    execution_description: list[str] = Field(default_factory=list)
    ended_at: Optional[datetime] = Field(default=None)

    @classmethod
    def start_execution(cls, flow_state:FlowStateAssignedToChat, flow_name:str) -> WorkflowExecution:
        return cls(
            workflow_id = flow_state.flow_id,
            chat_id = flow_state.chat_id,
            company_id = flow_state.company_id,
            name = flow_name,
            assigned_at = flow_state.assigned_at,
            started_at = datetime.now(tz=ZoneInfo("UTC"))
                    )

    def add_execution_step(self, step: str) -> None:
        self.execution_description.append(step)

    def end_execution(self, result: ExecutedStatus, description: str) -> None:
        self.ended_at = datetime.now(tz=ZoneInfo("UTC"))
        self.result = result
        self.execution_description.append(description)
