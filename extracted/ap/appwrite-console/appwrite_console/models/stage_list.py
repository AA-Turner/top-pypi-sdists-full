from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .stage import Stage


class StageList(AppwriteModel):
    """
    Stages List

    Attributes
    ----------
    stages : List[Stage]
        List of stages.
    """

    stages: List[Stage] = Field(..., alias='stages')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'stages' not in data:
            data['stages'] = []
        return data
