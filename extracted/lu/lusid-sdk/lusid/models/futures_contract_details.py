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


from typing import Any, Dict, List, Optional, Union
from pydantic.v1 import StrictStr, Field, BaseModel, Field, StrictFloat, StrictInt, StrictStr, conlist, constr 

class FuturesContractDetails(BaseModel):
    """
    Most, if not all, information about contracts is standardized. See, e.g. https://www.cmegroup.com/ for  common codes and similar data. This appears to be in common use by well known market information providers, e.g. Bloomberg and Refinitiv.  # noqa: E501
    """
    dom_ccy:  StrictStr = Field(...,alias="domCcy", description="Currency in which the contract is paid.") 
    fgn_ccy:  Optional[StrictStr] = Field(None,alias="fgnCcy", description="Currency of the underlying, for use with FX Futures") 
    asset_class:  Optional[StrictStr] = Field(None,alias="assetClass", description="The asset class of the underlying. Optional and will default to Unknown if not set.    Supported string (enumeration) values are: [InterestRates, FX, Inflation, Equities, Credit, Commodities, Money].") 
    contract_code:  StrictStr = Field(...,alias="contractCode", description="The contract code used by the exchange, e.g. “CL” for Crude Oil, “ES” for E-mini SP 500, “FGBL” for Bund Futures, etc.") 
    contract_month:  Optional[StrictStr] = Field(None,alias="contractMonth", description="Which month does the contract trade for.    Supported string (enumeration) values are: [F, G, H, J, K, M, N, Q, U, V, X, Z].") 
    contract_size: Union[StrictFloat, StrictInt] = Field(..., alias="contractSize", description="Size of a single contract.")
    convention:  Optional[StrictStr] = Field(None,alias="convention", description="If appropriate, the day count convention method used in pricing (rates futures).  For more information on day counts, see [knowledge base article KA-01798](https://support.lusid.com/knowledgebase/article/KA-01798)                Supported string (enumeration) values are: [Actual360, Act360, MoneyMarket, Actual365, Act365, Thirty360, ThirtyU360, Bond, ThirtyE360, EuroBond, ActualActual, ActAct, ActActIsda, ActActIsma, ActActIcma, OneOne, Act364, Act365F, Act365L, Act365_25, Act252, Bus252, NL360, NL365, ActActAFB, Act365Cad, ThirtyActIsda, Thirty365Isda, ThirtyEActIsda, ThirtyE360Isda, ThirtyE365Isda, ThirtyU360EOM].") 
    country:  Optional[StrictStr] = Field(None,alias="country", description="Country (code) for the exchange.") 
    description:  Optional[StrictStr] = Field(None,alias="description", description="Description of contract.") 
    exchange_code:  StrictStr = Field(...,alias="exchangeCode", description="Exchange code for contract. This can be any string to uniquely identify the exchange (e.g. Exchange Name, MIC, BBG code).") 
    exchange_name:  Optional[StrictStr] = Field(None,alias="exchangeName", description="Exchange name (for when code is not automatically recognised).") 
    ticker_step: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="tickerStep", description="Minimal step size change in ticker.")
    unit_value: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="unitValue", description="The value in the currency of a 1 unit change in the contract price.")
    calendars: Optional[conlist(StrictStr)] = Field(None, description="Holiday calendars that apply to yield-to-price conversions (i.e. for BRL futures).")
    delivery_type:  Optional[StrictStr] = Field(None,alias="deliveryType", description="Delivery type to be used on settling the contract.  Optional: Defaults to DeliveryType.Physical if not provided.    Supported string (enumeration) values are: [Cash, Physical].") 
    __properties = ["domCcy", "fgnCcy", "assetClass", "contractCode", "contractMonth", "contractSize", "convention", "country", "description", "exchangeCode", "exchangeName", "tickerStep", "unitValue", "calendars", "deliveryType"]

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
    def from_json(cls, json_str: str) -> FuturesContractDetails:
        """Create an instance of FuturesContractDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if fgn_ccy (nullable) is None
        # and __fields_set__ contains the field
        if self.fgn_ccy is None and "fgn_ccy" in self.__fields_set__:
            _dict['fgnCcy'] = None

        # set to None if asset_class (nullable) is None
        # and __fields_set__ contains the field
        if self.asset_class is None and "asset_class" in self.__fields_set__:
            _dict['assetClass'] = None

        # set to None if contract_month (nullable) is None
        # and __fields_set__ contains the field
        if self.contract_month is None and "contract_month" in self.__fields_set__:
            _dict['contractMonth'] = None

        # set to None if convention (nullable) is None
        # and __fields_set__ contains the field
        if self.convention is None and "convention" in self.__fields_set__:
            _dict['convention'] = None

        # set to None if country (nullable) is None
        # and __fields_set__ contains the field
        if self.country is None and "country" in self.__fields_set__:
            _dict['country'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if exchange_name (nullable) is None
        # and __fields_set__ contains the field
        if self.exchange_name is None and "exchange_name" in self.__fields_set__:
            _dict['exchangeName'] = None

        # set to None if calendars (nullable) is None
        # and __fields_set__ contains the field
        if self.calendars is None and "calendars" in self.__fields_set__:
            _dict['calendars'] = None

        # set to None if delivery_type (nullable) is None
        # and __fields_set__ contains the field
        if self.delivery_type is None and "delivery_type" in self.__fields_set__:
            _dict['deliveryType'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FuturesContractDetails:
        """Create an instance of FuturesContractDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FuturesContractDetails.parse_obj(obj)

        _obj = FuturesContractDetails.parse_obj({
            "dom_ccy": obj.get("domCcy"),
            "fgn_ccy": obj.get("fgnCcy"),
            "asset_class": obj.get("assetClass"),
            "contract_code": obj.get("contractCode"),
            "contract_month": obj.get("contractMonth"),
            "contract_size": obj.get("contractSize"),
            "convention": obj.get("convention"),
            "country": obj.get("country"),
            "description": obj.get("description"),
            "exchange_code": obj.get("exchangeCode"),
            "exchange_name": obj.get("exchangeName"),
            "ticker_step": obj.get("tickerStep"),
            "unit_value": obj.get("unitValue"),
            "calendars": obj.get("calendars"),
            "delivery_type": obj.get("deliveryType")
        })
        return _obj
