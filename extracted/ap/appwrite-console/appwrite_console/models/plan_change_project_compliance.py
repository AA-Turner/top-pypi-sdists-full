from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .plan_change_resource_compliance import PlanChangeResourceCompliance


class PlanChangeProjectCompliance(AppwriteModel):
    """
    PlanChangeProjectCompliance

    Attributes
    ----------
    id : str
        Project ID
    name : str
        Project name
    iscompliant : bool
        Whether the project complies with target plan limits
    resources : List[PlanChangeResourceCompliance]
        Resource compliance details
    error : Optional[str]
        Failure reason when compliance could not be evaluated. Present only when the project DB or Regions API was unreachable; in that case `isCompliant` is false (fail closed) and `resources` is empty.
    """

    id: str = Field(..., alias='$id')
    name: str = Field(..., alias='name')
    iscompliant: bool = Field(..., alias='isCompliant')
    resources: List[PlanChangeResourceCompliance] = Field(..., alias='resources')
    error: Optional[str] = Field(default=None, alias='error')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'isCompliant' not in data and 'iscompliant' not in data:
            data['isCompliant'] = True
        if 'resources' not in data:
            data['resources'] = []
        return data
