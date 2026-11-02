from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class VcsNamespace(AppwriteModel):
    """
    VcsNamespace

    Attributes
    ----------
    id : str
        VCS (Version Control System) namespace ID.
    name : str
        VCS (Version Control System) namespace display name.
    path : str
        VCS (Version Control System) namespace path, used to filter repositories by namespace.
    type : str
        Namespace type. Either the user&#039;s personal namespace or a group/organization.
    avatarurl : str
        Namespace avatar URL.
    """

    id: str = Field(..., alias='$id')
    name: str = Field(..., alias='name')
    path: str = Field(..., alias='path')
    type: str = Field(..., alias='type')
    avatarurl: str = Field(..., alias='avatarUrl')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'path' not in data:
            data['path'] = ''
        if 'type' not in data:
            data['type'] = ''
        if 'avatarUrl' not in data and 'avatarurl' not in data:
            data['avatarUrl'] = ''
        return data
