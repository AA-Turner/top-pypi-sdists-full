# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, List
from pydantic.v1 import StrictStr, Field, BaseModel, Field, StrictStr, conlist 
from lusid.models.portfolio_reconciliation_request import PortfolioReconciliationRequest

class PortfoliosReconciliationRequest(BaseModel):
    """
    PortfoliosReconciliationRequest
    """
    left: PortfolioReconciliationRequest = Field(...)
    right: PortfolioReconciliationRequest = Field(...)
    instrument_property_keys: conlist(StrictStr) = Field(..., alias="instrumentPropertyKeys", description="Instrument properties to be included with any identified breaks. These properties will be in the effective and AsAt dates of the left portfolio")
    __properties = ["left", "right", "instrumentPropertyKeys"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def __str__(self):
        """For `print` and `pprint`"""
        return pprint.pformat(self.dict(by_alias=False))

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PortfoliosReconciliationRequest:
        """Create an instance of PortfoliosReconciliationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of left
        if self.left:
            _dict['left'] = self.left.to_dict()
        # override the default output from pydantic by calling `to_dict()` of right
        if self.right:
            _dict['right'] = self.right.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PortfoliosReconciliationRequest:
        """Create an instance of PortfoliosReconciliationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PortfoliosReconciliationRequest.parse_obj(obj)

        _obj = PortfoliosReconciliationRequest.parse_obj({
            "left": PortfolioReconciliationRequest.from_dict(obj.get("left")) if obj.get("left") is not None else None,
            "right": PortfolioReconciliationRequest.from_dict(obj.get("right")) if obj.get("right") is not None else None,
            "instrument_property_keys": obj.get("instrumentPropertyKeys")
        })
        return _obj
