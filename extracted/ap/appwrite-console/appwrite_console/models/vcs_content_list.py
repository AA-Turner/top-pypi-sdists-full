from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .vcs_content import VcsContent


class VcsContentList(AppwriteModel):
    """
    VCS Content List

    Attributes
    ----------
    total : float
        Total number of contents that matched your query.
    contents : List[VcsContent]
        List of contents.
    """

    total: float = Field(..., alias='total')
    contents: List[VcsContent] = Field(..., alias='contents')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'contents' not in data:
            data['contents'] = []
        return data
