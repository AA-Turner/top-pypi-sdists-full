from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class DowngradeFeedback(AppwriteModel):
    """
    Downgrade Feedback

    Attributes
    ----------
    id : str
        Feedback ID.
    createdat : str
        Feedback creation date in ISO 8601 format.
    updatedat : str
        Feedback update date in ISO 8601 format.
    title : str
        Feedback reason
    message : str
        Feedback message
    fromplanid : str
        Plan ID downgrading from
    toplanid : str
        Plan ID downgrading to
    teamid : str
        Organization ID
    userid : str
        User ID who submitted feedback
    version : str
        Console version
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    title: str = Field(..., alias='title')
    message: str = Field(..., alias='message')
    fromplanid: str = Field(..., alias='fromPlanId')
    toplanid: str = Field(..., alias='toPlanId')
    teamid: str = Field(..., alias='teamId')
    userid: str = Field(..., alias='userId')
    version: str = Field(..., alias='version')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if '$createdAt' not in data and 'createdat' not in data:
            data['$createdAt'] = ''
        if '$updatedAt' not in data and 'updatedat' not in data:
            data['$updatedAt'] = ''
        if 'title' not in data:
            data['title'] = ''
        if 'message' not in data:
            data['message'] = ''
        if 'fromPlanId' not in data and 'fromplanid' not in data:
            data['fromPlanId'] = ''
        if 'toPlanId' not in data and 'toplanid' not in data:
            data['toPlanId'] = ''
        if 'teamId' not in data and 'teamid' not in data:
            data['teamId'] = ''
        if 'userId' not in data and 'userid' not in data:
            data['userId'] = ''
        if 'version' not in data:
            data['version'] = ''
        return data
