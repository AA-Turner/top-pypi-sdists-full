from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .console_o_auth2_provider import ConsoleOAuth2Provider


class ConsoleOAuth2ProviderList(AppwriteModel):
    """
    Console OAuth2 Providers List

    Attributes
    ----------
    total : float
        Total number of OAuth2 providers exposed by the server.
    oauth2providers : List[ConsoleOAuth2Provider]
        List of OAuth2 providers, each with the parameters required to configure it.
    """

    total: float = Field(..., alias='total')
    oauth2providers: List[ConsoleOAuth2Provider] = Field(..., alias='oAuth2Providers')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'oAuth2Providers' not in data and 'oauth2providers' not in data:
            data['oAuth2Providers'] = []
        return data
