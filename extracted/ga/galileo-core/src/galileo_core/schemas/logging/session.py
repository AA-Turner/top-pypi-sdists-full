from typing import List, Literal, Optional

from pydantic import Field
from pydantic.types import UUID4

from galileo_core.schemas.logging.step import BaseStep, StepType
from galileo_core.schemas.logging.trace import Trace


class BaseSession(BaseStep):
    type: Literal[StepType.session] = Field(
        default=StepType.session, description=BaseStep.model_fields["type"].description
    )
    previous_session_id: Optional[UUID4] = None


class Session(BaseSession):
    traces: List[Trace] = Field(
        default_factory=list,
        description="List of traces associated with this session. Each trace can have its own spans.",
    )


# Define SessionWithTraces as an alias for Session for backward compatibility
SessionWithTraces = Session
