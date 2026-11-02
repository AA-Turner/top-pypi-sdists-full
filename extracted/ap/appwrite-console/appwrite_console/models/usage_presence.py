from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .metric import Metric


class UsagePresence(AppwriteModel):
    """
    UsagePresence

    Attributes
    ----------
    range : str
        Time range of the usage stats.
    usersonlinetotal : float
        Current total number of online users.
    presences : List[Metric]
        Aggregated number of online users per period.
    """

    range: str = Field(..., alias='range')
    usersonlinetotal: float = Field(..., alias='usersOnlineTotal')
    presences: List[Metric] = Field(..., alias='presences')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'range' not in data:
            data['range'] = ''
        if 'usersOnlineTotal' not in data and 'usersonlinetotal' not in data:
            data['usersOnlineTotal'] = 0
        if 'presences' not in data:
            data['presences'] = []
        return data
