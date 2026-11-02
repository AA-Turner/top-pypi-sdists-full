from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Stage(AppwriteModel):
    """
    Stage

    Attributes
    ----------
    id : str
        Stage ID.
    sdk : str
        SDK method key (namespace.name) for this stage.
    status : str
        Stage status.
    at : str
        When the stage was completed or skipped, in ISO 8601 format.
    actortype : str
        Actor type when the stage was recorded.
    """

    id: str = Field(..., alias='id')
    sdk: str = Field(..., alias='sdk')
    status: str = Field(..., alias='status')
    at: str = Field(..., alias='at')
    actortype: str = Field(..., alias='actorType')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'id' not in data:
            data['id'] = ''
        if 'sdk' not in data:
            data['sdk'] = ''
        if 'status' not in data:
            data['status'] = 'pending'
        if 'at' not in data:
            data['at'] = ''
        if 'actorType' not in data and 'actortype' not in data:
            data['actorType'] = ''
        return data
