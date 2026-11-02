from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Installation(AppwriteModel):
    """
    Installation

    Attributes
    ----------
    id : str
        Function ID.
    createdat : str
        Function creation date in ISO 8601 format.
    updatedat : str
        Function update date in ISO 8601 format.
    provider : str
        VCS (Version Control System) provider name.
    organization : str
        VCS (Version Control System) organization name.
    providerinstallationid : str
        VCS (Version Control System) installation ID.
    organizationurl : str
        VCS (Version Control System) organization URL. Points at the configured instance, which is not the provider&#039;s own host for a self-hosted install.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    provider: str = Field(..., alias='provider')
    organization: str = Field(..., alias='organization')
    providerinstallationid: str = Field(..., alias='providerInstallationId')
    organizationurl: str = Field(..., alias='organizationUrl')

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
        if 'providerInstallationId' not in data and 'providerinstallationid' not in data:
            data['providerInstallationId'] = ''
        if 'organizationUrl' not in data and 'organizationurl' not in data:
            data['organizationUrl'] = ''
        return data
