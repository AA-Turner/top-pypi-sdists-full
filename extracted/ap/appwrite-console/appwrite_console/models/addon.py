from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Addon(AppwriteModel):
    """
    Addon

    Attributes
    ----------
    id : str
        Addon ID.
    createdat : str
        Addon creation time in ISO 8601 format.
    updatedat : str
        Addon update date in ISO 8601 format.
    permissions : List[Any]
        Addon permissions. [Learn more about permissions](https://appwrite.io/docs/permissions).
    key : str
        Addon key
    resourcetype : str
        Resource type (organization or project)
    resourceid : str
        Resource ID
    status : str
        Payment status. Possible values: pending (awaiting payment confirmation e.g. 3DS), active (payment confirmed and addon is running).
    currentvalue : float
        Current value for this billing cycle. For toggle addons: 1 (on) or 0 (off). For numeric addons: the active quantity.
    nextvalue : Optional[float]
        Value to apply at the start of the next billing cycle. Null means no change is scheduled. For toggle addons, 0 means the addon will be removed at the next cycle.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    permissions: List[Any] = Field(..., alias='$permissions')
    key: str = Field(..., alias='key')
    resourcetype: str = Field(..., alias='resourceType')
    resourceid: str = Field(..., alias='resourceId')
    status: str = Field(..., alias='status')
    currentvalue: float = Field(..., alias='currentValue')
    nextvalue: Optional[float] = Field(default=None, alias='nextValue')

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
        if '$permissions' not in data and 'permissions' not in data:
            data['$permissions'] = []
        if 'key' not in data:
            data['key'] = ''
        if 'resourceType' not in data and 'resourcetype' not in data:
            data['resourceType'] = ''
        if 'resourceId' not in data and 'resourceid' not in data:
            data['resourceId'] = ''
        if 'status' not in data:
            data['status'] = 'active'
        if 'currentValue' not in data and 'currentvalue' not in data:
            data['currentValue'] = 0
        return data
