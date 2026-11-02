from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class AffiliateLink(AppwriteModel):
    """
    AffiliateLink

    Attributes
    ----------
    id : str
        Link ID. This is the shareable referral code.
    createdat : str
        Link creation date in ISO 8601 format.
    updatedat : str
        Link update date in ISO 8601 format.
    userid : str
        User ID of the link owner.
    name : str
        Optional link name.
    status : str
        Link status. Can be one of `active` or `disabled`.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    userid: str = Field(..., alias='userId')
    name: str = Field(..., alias='name')
    status: str = Field(..., alias='status')

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
        if 'userId' not in data and 'userid' not in data:
            data['userId'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'status' not in data:
            data['status'] = ''
        return data
