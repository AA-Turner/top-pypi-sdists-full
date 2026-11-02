from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Coupon(AppwriteModel):
    """
    Coupon

    Attributes
    ----------
    id : str
        coupon ID
    code : str
        coupon ID
    credits : float
        Provided credit amount
    expiration : str
        Coupon expiration time in ISO 8601 format.
    validity : float
        Credit validity in days.
    campaign : str
        Campaign the coupon is associated with`.
    status : str
        Status of the coupon. Can be one of `disabled`, `active` or `expired`.
    onlyneworgs : bool
        If the coupon is only valid for new organizations or not.
    """

    id: str = Field(..., alias='$id')
    code: str = Field(..., alias='code')
    credits: float = Field(..., alias='credits')
    expiration: str = Field(..., alias='expiration')
    validity: float = Field(..., alias='validity')
    campaign: str = Field(..., alias='campaign')
    status: str = Field(..., alias='status')
    onlyneworgs: bool = Field(..., alias='onlyNewOrgs')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if 'code' not in data:
            data['code'] = ''
        if 'credits' not in data:
            data['credits'] = 0
        if 'expiration' not in data:
            data['expiration'] = ''
        if 'campaign' not in data:
            data['campaign'] = ''
        if 'status' not in data:
            data['status'] = ''
        if 'onlyNewOrgs' not in data and 'onlyneworgs' not in data:
            data['onlyNewOrgs'] = False
        return data
