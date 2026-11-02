from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class PaymentMethod(AppwriteModel):
    """
    paymentMethod

    Attributes
    ----------
    id : str
        Payment Method ID.
    createdat : str
        Payment method creation time in ISO 8601 format.
    updatedat : str
        Payment method update date in ISO 8601 format.
    permissions : List[Any]
        Payment method permissions. [Learn more about permissions](/docs/permissions).
    providermethodid : str
        Payment method ID from the payment provider
    clientsecret : str
        Client secret hash for payment setup
    provideruserid : str
        User ID from the payment provider.
    userid : str
        ID of the Team.
    expirymonth : Optional[float]
        Expiry month of the payment method.
    expiryyear : Optional[float]
        Expiry year of the payment method.
    last4 : Optional[str]
        Last 4 digit of the payment method
    brand : Optional[str]
        Payment method brand
    name : Optional[str]
        Name of the owner
    mandateid : Optional[str]
        Mandate ID of the payment method
    country : Optional[str]
        Country of the payment method
    state : Optional[str]
        State of the payment method
    lasterror : Optional[str]
        Last payment error associated with the payment method.
    default : bool
        True when it&#039;s the default payment method.
    expired : bool
        True when payment method has expired.
    failed : bool
        True when payment method has failed to process multiple times.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    permissions: List[Any] = Field(..., alias='$permissions')
    providermethodid: str = Field(..., alias='providerMethodId')
    clientsecret: str = Field(..., alias='clientSecret')
    provideruserid: str = Field(..., alias='providerUserId')
    userid: str = Field(..., alias='userId')
    expirymonth: Optional[float] = Field(default=None, alias='expiryMonth')
    expiryyear: Optional[float] = Field(default=None, alias='expiryYear')
    last4: Optional[str] = Field(default=None, alias='last4')
    brand: Optional[str] = Field(default=None, alias='brand')
    name: Optional[str] = Field(default=None, alias='name')
    mandateid: Optional[str] = Field(default=None, alias='mandateId')
    country: Optional[str] = Field(default=None, alias='country')
    state: Optional[str] = Field(default=None, alias='state')
    lasterror: Optional[str] = Field(default=None, alias='lastError')
    default: bool = Field(..., alias='default')
    expired: bool = Field(..., alias='expired')
    failed: bool = Field(..., alias='failed')

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
        if 'providerMethodId' not in data and 'providermethodid' not in data:
            data['providerMethodId'] = ''
        if 'clientSecret' not in data and 'clientsecret' not in data:
            data['clientSecret'] = ''
        if 'providerUserId' not in data and 'provideruserid' not in data:
            data['providerUserId'] = ''
        if 'userId' not in data and 'userid' not in data:
            data['userId'] = ''
        if 'default' not in data:
            data['default'] = False
        return data
