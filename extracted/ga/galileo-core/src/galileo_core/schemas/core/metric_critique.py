from typing import List, Optional, Union

from annotated_types import Len
from pydantic import UUID4, BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class MetricCritique(BaseModel):
    run_id: Optional[UUID4] = None  # Evaluate requires a run id, while observe does not.
    row_id: Union[UUID4, int]
    critique: str
    intended_value: bool = Field(
        description="Set to opposite of actual value for new critiques, and set as same as existing critique intended value for updates."
    )


class CreateMetricCritiquesRequest(BaseModel):
    critiques: Annotated[List[MetricCritique], Len(min_length=1)]
    metric: str


class MetricCritiqueResponse(BaseModel):
    id: UUID4
    project_id: UUID4
    metric: str
    scorer_id: UUID4
    row_id: Union[UUID4, int]
    is_computed: bool
    model_config = ConfigDict(extra="allow")
