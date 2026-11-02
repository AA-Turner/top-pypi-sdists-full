from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .notification import Notification


class NotificationList(AppwriteModel):
    """
    Notifications List

    Attributes
    ----------
    total : float
        Total number of notifications that matched your query.
    notifications : List[Notification]
        List of notifications.
    """

    total: float = Field(..., alias='total')
    notifications: List[Notification] = Field(..., alias='notifications')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'notifications' not in data:
            data['notifications'] = []
        return data
