from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Notification(AppwriteModel):
    """
    Notification

    Attributes
    ----------
    id : str
        Notification ID.
    createdat : str
        Notification creation date in ISO 8601 format.
    updatedat : str
        Notification update date in ISO 8601 format.
    messageid : Optional[str]
        Stable message ID used for dedup.
    type : str
        Notification type: info, warning, error.
    channel : str
        Channel: email, sms, push, console, webhook.
    resourcetype : str
        Resource type this notification is addressed to.
    resourceid : str
        Resource ID this notification is addressed to.
    parentresourcetype : str
        Parent resource type for the notification.
    parentresourceid : str
        Parent resource ID for the notification.
    projectid : Optional[str]
        Project the notification pertains to.
    title : str
        Notification title.
    body : str
        Notification body.
    read : Optional[bool]
        Whether the notification has been read.
    firstseen : Optional[str]
        First time the notification was viewed from a notification logo.
    lastseen : Optional[str]
        Most recent time the notification was viewed from a notification logo.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    messageid: Optional[str] = Field(default=None, alias='messageId')
    type: str = Field(..., alias='type')
    channel: str = Field(..., alias='channel')
    resourcetype: str = Field(..., alias='resourceType')
    resourceid: str = Field(..., alias='resourceId')
    parentresourcetype: str = Field(..., alias='parentResourceType')
    parentresourceid: str = Field(..., alias='parentResourceId')
    projectid: Optional[str] = Field(default=None, alias='projectId')
    title: str = Field(..., alias='title')
    body: str = Field(..., alias='body')
    read: Optional[bool] = Field(default=None, alias='read')
    firstseen: Optional[str] = Field(default=None, alias='firstSeen')
    lastseen: Optional[str] = Field(default=None, alias='lastSeen')

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
        if 'type' not in data:
            data['type'] = 'info'
        if 'channel' not in data:
            data['channel'] = ''
        if 'resourceType' not in data and 'resourcetype' not in data:
            data['resourceType'] = ''
        if 'resourceId' not in data and 'resourceid' not in data:
            data['resourceId'] = ''
        if 'parentResourceType' not in data and 'parentresourcetype' not in data:
            data['parentResourceType'] = ''
        if 'parentResourceId' not in data and 'parentresourceid' not in data:
            data['parentResourceId'] = ''
        if 'title' not in data:
            data['title'] = ''
        if 'body' not in data:
            data['body'] = ''
        return data
