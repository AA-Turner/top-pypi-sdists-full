from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class PlanChangeResourceCompliance(AppwriteModel):
    """
    PlanChangeResourceCompliance

    Attributes
    ----------
    type : str
        Resource type
    currentusage : float
        Current usage count
    limit : float
        Allowed limit in target plan
    status : str
        Compliance status. Either `over_limit` or `within_limit`.
    excess : float
        Number of resources exceeding the limit
    resolutionhint : str
        Suggestion for resolving the compliance issue. Empty when the resource is within limits.
    """

    type: str = Field(..., alias='type')
    currentusage: float = Field(..., alias='currentUsage')
    limit: float = Field(..., alias='limit')
    status: str = Field(..., alias='status')
    excess: float = Field(..., alias='excess')
    resolutionhint: str = Field(..., alias='resolutionHint')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'type' not in data:
            data['type'] = ''
        if 'currentUsage' not in data and 'currentusage' not in data:
            data['currentUsage'] = 0
        if 'limit' not in data:
            data['limit'] = 0
        if 'status' not in data:
            data['status'] = ''
        if 'excess' not in data:
            data['excess'] = 0
        if 'resolutionHint' not in data and 'resolutionhint' not in data:
            data['resolutionHint'] = ''
        return data
