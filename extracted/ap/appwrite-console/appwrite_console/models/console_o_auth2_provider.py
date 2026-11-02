from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .console_o_auth2_provider_parameter import ConsoleOAuth2ProviderParameter


class ConsoleOAuth2Provider(AppwriteModel):
    """
    Console OAuth2 Provider

    Attributes
    ----------
    id : str
        OAuth2 provider ID.
    parameters : List[ConsoleOAuth2ProviderParameter]
        List of parameters required to configure this OAuth2 provider.
    """

    id: str = Field(..., alias='$id')
    parameters: List[ConsoleOAuth2ProviderParameter] = Field(..., alias='parameters')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if 'parameters' not in data:
            data['parameters'] = []
        return data
