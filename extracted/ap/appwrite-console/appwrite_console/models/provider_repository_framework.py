from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class ProviderRepositoryFramework(AppwriteModel):
    """
    ProviderRepositoryFramework

    Attributes
    ----------
    id : str
        VCS (Version Control System) repository ID.
    name : str
        VCS (Version Control System) repository name.
    organization : str
        VCS (Version Control System) organization name
    provider : str
        VCS (Version Control System) provider name.
    private : bool
        Is VCS (Version Control System) repository private?
    defaultbranch : str
        VCS (Version Control System) repository&#039;s default branch name.
    providerinstallationid : str
        VCS (Version Control System) installation ID.
    authorized : bool
        Is VCS (Version Control System) repository authorized for the installation?
    pushedat : str
        Last commit date in ISO 8601 format.
    variables : List[Any]
        Environment variables found in .env files
    framework : str
        Auto-detected framework. Empty if type is not &quot;framework&quot;.
    """

    id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    organization: str = Field(..., alias='organization')
    provider: str = Field(..., alias='provider')
    private: bool = Field(..., alias='private')
    defaultbranch: str = Field(..., alias='defaultBranch')
    providerinstallationid: str = Field(..., alias='providerInstallationId')
    authorized: bool = Field(..., alias='authorized')
    pushedat: str = Field(..., alias='pushedAt')
    variables: List[Any] = Field(..., alias='variables')
    framework: str = Field(..., alias='framework')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'id' not in data:
            data['id'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'provider' not in data:
            data['provider'] = ''
        if 'private' not in data:
            data['private'] = False
        if 'defaultBranch' not in data and 'defaultbranch' not in data:
            data['defaultBranch'] = ''
        if 'providerInstallationId' not in data and 'providerinstallationid' not in data:
            data['providerInstallationId'] = ''
        if 'authorized' not in data:
            data['authorized'] = False
        if 'variables' not in data:
            data['variables'] = []
        if 'framework' not in data:
            data['framework'] = ''
        return data
