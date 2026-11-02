from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class BillingAddress(AppwriteModel):
    """
    Address

    Attributes
    ----------
    id : str
        Region ID
    userid : str
        User ID
    streetaddress : str
        Street address
    addressline2 : Optional[str]
        Address line 2
    country : str
        Address country
    city : str
        city
    state : Optional[str]
        state
    postalcode : Optional[str]
        postal code
    """

    id: str = Field(..., alias='$id')
    userid: str = Field(..., alias='userId')
    streetaddress: str = Field(..., alias='streetAddress')
    addressline2: Optional[str] = Field(default=None, alias='addressLine2')
    country: str = Field(..., alias='country')
    city: str = Field(..., alias='city')
    state: Optional[str] = Field(default=None, alias='state')
    postalcode: Optional[str] = Field(default=None, alias='postalCode')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if 'userId' not in data and 'userid' not in data:
            data['userId'] = ''
        if 'streetAddress' not in data and 'streetaddress' not in data:
            data['streetAddress'] = ''
        if 'country' not in data:
            data['country'] = ''
        if 'city' not in data:
            data['city'] = ''
        return data
