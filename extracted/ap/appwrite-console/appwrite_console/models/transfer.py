from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Transfer(AppwriteModel):
    """
    Transfer

    Attributes
    ----------
    id : str
        Transfer ID.
    createdat : str
        Transfer creation date in ISO 8601 format.
    updatedat : str
        Transfer update date in ISO 8601 format.
    resourcetype : str
        Type of the resource being transferred.
    resourceid : str
        ID of the resource being transferred.
    resourcename : str
        Name of the resource being transferred, so the recipient can see what they are claiming.
    sendertype : str
        Type of the sender that owns the resource.
    senderid : str
        ID of the sender that owns the resource.
    sendername : str
        Name of the sender that owns the resource.
    recipienttype : str
        Type of the recipient that can claim the resource.
    recipientid : str
        ID of the only recipient that can claim the resource. Empty when any recipient of the recipient type can claim it.
    recipientname : str
        Name of the only recipient that can claim the resource. Empty when any recipient of the recipient type can claim it.
    expire : str
        Transfer expiration date in ISO 8601 format.
    secret : str
        Secret the recipient uses to claim the resource. Only returned to the sender.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    resourcetype: str = Field(..., alias='resourceType')
    resourceid: str = Field(..., alias='resourceId')
    resourcename: str = Field(..., alias='resourceName')
    sendertype: str = Field(..., alias='senderType')
    senderid: str = Field(..., alias='senderId')
    sendername: str = Field(..., alias='senderName')
    recipienttype: str = Field(..., alias='recipientType')
    recipientid: str = Field(..., alias='recipientId')
    recipientname: str = Field(..., alias='recipientName')
    expire: str = Field(..., alias='expire')
    secret: str = Field(..., alias='secret', json_schema_extra={'format': 'password'})

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
        if 'resourceType' not in data and 'resourcetype' not in data:
            data['resourceType'] = ''
        if 'resourceId' not in data and 'resourceid' not in data:
            data['resourceId'] = ''
        if 'resourceName' not in data and 'resourcename' not in data:
            data['resourceName'] = ''
        if 'senderType' not in data and 'sendertype' not in data:
            data['senderType'] = ''
        if 'senderId' not in data and 'senderid' not in data:
            data['senderId'] = ''
        if 'senderName' not in data and 'sendername' not in data:
            data['senderName'] = ''
        if 'recipientType' not in data and 'recipienttype' not in data:
            data['recipientType'] = ''
        if 'recipientId' not in data and 'recipientid' not in data:
            data['recipientId'] = ''
        if 'recipientName' not in data and 'recipientname' not in data:
            data['recipientName'] = ''
        if 'expire' not in data:
            data['expire'] = ''
        if 'secret' not in data:
            data['secret'] = ''
        return data
