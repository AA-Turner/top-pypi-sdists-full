from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .usage_resources import UsageResources


class Invoice(AppwriteModel):
    """
    Invoice

    Attributes
    ----------
    id : str
        Invoice ID.
    createdat : str
        Invoice creation time in ISO 8601 format.
    updatedat : str
        Invoice update date in ISO 8601 format.
    permissions : List[Any]
        Invoice permissions. [Learn more about permissions](/docs/permissions).
    teamid : str
        Project ID
    aggregationid : str
        Aggregation ID
    plan : str
        Billing plan selected. Can be one of `tier-0`, `tier-1` or `tier-2`.
    usage : List[UsageResources]
        Usage breakdown per resource
    amount : float
        Invoice Amount
    tax : float
        Tax percentage
    taxamount : float
        Tax amount
    vat : float
        VAT percentage
    vatamount : float
        VAT amount
    grossamount : float
        Gross amount after vat, tax, and discounts applied.
    creditsused : float
        Credits used.
    currency : str
        Currency the invoice is in
    clientsecret : Optional[str]
        Client secret for processing failed payments in front-end
    status : str
        Invoice status
    type : str
        Invoice type. Can be one of `subscription`, `domain_purchase`, `domain_renewal`, `domain_transfer`, or `addon_*`.
    lasterror : Optional[str]
        Last payment error associated with the invoice
    dueat : str
        Invoice due date.
    xfrom : str
        Beginning date of the invoice
    to : str
        End date of the invoice
    """

    id: str = Field(..., alias='$id')
    createdat: str = Field(..., alias='$createdAt')
    updatedat: str = Field(..., alias='$updatedAt')
    permissions: List[Any] = Field(..., alias='$permissions')
    teamid: str = Field(..., alias='teamId')
    aggregationid: str = Field(..., alias='aggregationId')
    plan: str = Field(..., alias='plan')
    usage: List[UsageResources] = Field(..., alias='usage')
    amount: float = Field(..., alias='amount')
    tax: float = Field(..., alias='tax')
    taxamount: float = Field(..., alias='taxAmount')
    vat: float = Field(..., alias='vat')
    vatamount: float = Field(..., alias='vatAmount')
    grossamount: float = Field(..., alias='grossAmount')
    creditsused: float = Field(..., alias='creditsUsed')
    currency: str = Field(..., alias='currency')
    clientsecret: Optional[str] = Field(default=None, alias='clientSecret')
    status: str = Field(..., alias='status')
    type: str = Field(..., alias='type')
    lasterror: Optional[str] = Field(default=None, alias='lastError')
    dueat: str = Field(..., alias='dueAt')
    xfrom: str = Field(..., alias='from')
    to: str = Field(..., alias='to')

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
        if 'teamId' not in data and 'teamid' not in data:
            data['teamId'] = ''
        if 'aggregationId' not in data and 'aggregationid' not in data:
            data['aggregationId'] = ''
        if 'plan' not in data:
            data['plan'] = 'tier-0'
        if 'usage' not in data:
            data['usage'] = []
        if 'amount' not in data:
            data['amount'] = 0
        if 'tax' not in data:
            data['tax'] = 0
        if 'taxAmount' not in data and 'taxamount' not in data:
            data['taxAmount'] = 0
        if 'vat' not in data:
            data['vat'] = 0
        if 'vatAmount' not in data and 'vatamount' not in data:
            data['vatAmount'] = 0
        if 'grossAmount' not in data and 'grossamount' not in data:
            data['grossAmount'] = 0
        if 'creditsUsed' not in data and 'creditsused' not in data:
            data['creditsUsed'] = 0
        if 'currency' not in data:
            data['currency'] = 'USD'
        if 'status' not in data:
            data['status'] = ''
        if 'type' not in data:
            data['type'] = 'subscription'
        if 'from' not in data and 'xfrom' not in data:
            data['from'] = ''
        if 'to' not in data:
            data['to'] = ''
        return data
