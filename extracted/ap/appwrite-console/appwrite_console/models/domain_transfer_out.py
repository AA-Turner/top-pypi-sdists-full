from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class DomainTransferOut(AppwriteModel):
    """
    domainTransferOut

    Attributes
    ----------
    authcode : str
        Domain transfer authorization code.
    """

    authcode: str = Field(..., alias='authCode')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'authCode' not in data and 'authcode' not in data:
            data['authCode'] = ''
        return data
