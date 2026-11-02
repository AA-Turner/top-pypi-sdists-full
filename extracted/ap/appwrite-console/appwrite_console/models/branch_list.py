from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .branch import Branch


class BranchList(AppwriteModel):
    """
    Branches List

    Attributes
    ----------
    total : float
        Total number of branches that matched your query.
    branches : List[Branch]
        List of branches.
    """

    total: float = Field(..., alias='total')
    branches: List[Branch] = Field(..., alias='branches')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'branches' not in data:
            data['branches'] = []
        return data
