from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .metric import Metric


class UsageUsers(AppwriteModel):
    """
    UsageUsers

    Attributes
    ----------
    range : str
        Time range of the usage stats.
    userstotal : float
        Total aggregated number of statistics of users.
    sessionstotal : float
        Total aggregated number of active sessions.
    users : List[Metric]
        Aggregated number of users per period.
    sessions : List[Metric]
        Aggregated number of active sessions  per period.
    """

    range: str = Field(..., alias='range')
    userstotal: float = Field(..., alias='usersTotal')
    sessionstotal: float = Field(..., alias='sessionsTotal')
    users: List[Metric] = Field(..., alias='users')
    sessions: List[Metric] = Field(..., alias='sessions')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'range' not in data:
            data['range'] = ''
        if 'usersTotal' not in data and 'userstotal' not in data:
            data['usersTotal'] = 0
        if 'sessionsTotal' not in data and 'sessionstotal' not in data:
            data['sessionsTotal'] = 0
        if 'users' not in data:
            data['users'] = []
        if 'sessions' not in data:
            data['sessions'] = []
        return data
