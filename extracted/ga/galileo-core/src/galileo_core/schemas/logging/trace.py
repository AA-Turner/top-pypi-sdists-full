from typing import Literal, Optional

from pydantic import Field

from galileo_core.schemas.logging.span import (
    Span,  # noqa: F401  # to solve forward reference issues
    StepWithChildSpans,
)
from galileo_core.schemas.logging.step import BaseStep, StepType


class BaseTrace(BaseStep):
    type: Literal[StepType.trace] = Field(default=StepType.trace, description=BaseStep.model_fields["type"].description)
    input: str = Field(default="", description=BaseStep.model_fields["input"].description)
    redacted_input: Optional[str] = Field(default=None, description=BaseStep.model_fields["redacted_input"].description)
    output: Optional[str] = Field(default=None, description=BaseStep.model_fields["output"].description)
    redacted_output: Optional[str] = Field(
        default=None, description=BaseStep.model_fields["redacted_output"].description
    )


class Trace(BaseTrace, StepWithChildSpans):
    pass
