from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from ..enums.domain_purchase_status import DomainPurchaseStatus


class DomainPurchase(AppwriteModel):
    """
    DomainPurchase

    Attributes
    ----------
    id : str
        Purchase/invoice ID.
    createdat : str
        Purchase creation time in ISO 8601 format.
    updatedat : str
        Purchase update date in ISO 8601 format.
    domainid : str
        Domain document ID.
    domain : str
        Domain name.
    organizationid : str
        Team ID that owns the domain.
    status : DomainPurchaseStatus
        Domain purchase status.
    clientsecret : str
        Stripe client secret for 3DS; empty when not applicable.
    amount : float
        Purchase amount.
    currency : str
        Currency code.
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    domainid: str = Field(..., alias='domainId')
    domain: str = Field(..., alias='domain')
    organizationid: str = Field(..., alias='organizationId')
    status: DomainPurchaseStatus = Field(..., alias='status')
    clientsecret: str = Field(..., alias='clientSecret')
    amount: float = Field(..., alias='amount')
    currency: str = Field(..., alias='currency')

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
        if 'domainId' not in data and 'domainid' not in data:
            data['domainId'] = ''
        if 'domain' not in data:
            data['domain'] = ''
        if 'organizationId' not in data and 'organizationid' not in data:
            data['organizationId'] = ''
        if 'status' not in data:
            data['status'] = 'pending'
        if 'clientSecret' not in data and 'clientsecret' not in data:
            data['clientSecret'] = ''
        if 'amount' not in data:
            data['amount'] = 0
        if 'currency' not in data:
            data['currency'] = 'USD'
        return data
