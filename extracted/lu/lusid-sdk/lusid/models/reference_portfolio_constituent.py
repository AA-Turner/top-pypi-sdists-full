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


from typing import Any, Dict, Optional, Union
from pydantic.v1 import StrictStr, Field, BaseModel, Field, StrictFloat, StrictInt, StrictStr, constr 
from lusid.models.perpetual_property import PerpetualProperty

class ReferencePortfolioConstituent(BaseModel):
    """
    ReferencePortfolioConstituent
    """
    instrument_identifiers: Optional[Dict[str, StrictStr]] = Field(None, alias="instrumentIdentifiers", description="Unique instrument identifiers")
    instrument_uid:  StrictStr = Field(...,alias="instrumentUid", description="LUSID's internal unique instrument identifier, resolved from the instrument identifiers") 
    currency:  StrictStr = Field(...,alias="currency", description="") 
    properties: Optional[Dict[str, PerpetualProperty]] = Field(None, description="Properties associated with the constituent")
    weight: Union[StrictFloat, StrictInt] = Field(...)
    floating_weight: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="floatingWeight")
    instrument_scope:  Optional[StrictStr] = Field(None,alias="instrumentScope", description="") 
    __properties = ["instrumentIdentifiers", "instrumentUid", "currency", "properties", "weight", "floatingWeight", "instrumentScope"]

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
    def from_json(cls, json_str: str) -> ReferencePortfolioConstituent:
        """Create an instance of ReferencePortfolioConstituent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # set to None if instrument_identifiers (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_identifiers is None and "instrument_identifiers" in self.__fields_set__:
            _dict['instrumentIdentifiers'] = None

        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if floating_weight (nullable) is None
        # and __fields_set__ contains the field
        if self.floating_weight is None and "floating_weight" in self.__fields_set__:
            _dict['floatingWeight'] = None

        # set to None if instrument_scope (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_scope is None and "instrument_scope" in self.__fields_set__:
            _dict['instrumentScope'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReferencePortfolioConstituent:
        """Create an instance of ReferencePortfolioConstituent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReferencePortfolioConstituent.parse_obj(obj)

        _obj = ReferencePortfolioConstituent.parse_obj({
            "instrument_identifiers": obj.get("instrumentIdentifiers"),
            "instrument_uid": obj.get("instrumentUid"),
            "currency": obj.get("currency"),
            "properties": dict(
                (_k, PerpetualProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "weight": obj.get("weight"),
            "floating_weight": obj.get("floatingWeight"),
            "instrument_scope": obj.get("instrumentScope")
        })
        return _obj
