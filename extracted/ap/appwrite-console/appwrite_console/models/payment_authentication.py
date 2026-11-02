from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class PaymentAuthentication(AppwriteModel):
    """
    PaymentAuthentication

    Attributes
    ----------
    message : str
        Message for the end user to show on Console.
    clientsecret : str
        Stripe client secret to use for validation.
    organizationid : str
        Organization ID for which the payment authentication is needed.
    invoiceid : str
        Invoice ID against which the payment needs to be validated.
    addonid : str
        Addon ID to use when calling the addon validate endpoint. Empty when authentication is not for an addon.
    projectid : str
        Project ID for project-level addon payments. Empty for organization-level addons.
    """

    message: str = Field(..., alias='message')
    clientsecret: str = Field(..., alias='clientSecret')
    organizationid: str = Field(..., alias='organizationId')
    invoiceid: str = Field(..., alias='invoiceId')
    addonid: str = Field(..., alias='addonId')
    projectid: str = Field(..., alias='projectId')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'message' not in data:
            data['message'] = 'Your payment requires authentication'
        if 'clientSecret' not in data and 'clientsecret' not in data:
            data['clientSecret'] = ''
        if 'organizationId' not in data and 'organizationid' not in data:
            data['organizationId'] = ''
        if 'invoiceId' not in data and 'invoiceid' not in data:
            data['invoiceId'] = ''
        if 'addonId' not in data and 'addonid' not in data:
            data['addonId'] = ''
        if 'projectId' not in data and 'projectid' not in data:
            data['projectId'] = ''
        return data
