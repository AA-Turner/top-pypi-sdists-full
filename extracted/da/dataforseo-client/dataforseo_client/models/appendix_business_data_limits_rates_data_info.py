from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set, Any, Dict, List
from typing_extensions import Self

from dataforseo_client.models.appendix_business_data_google_info import AppendixBusinessDataGoogleInfo
from dataforseo_client.models.appendix_tr_business_data_day_limits_rates_data_info import AppendixTrBusinessDataDayLimitsRatesDataInfo
from dataforseo_client.models.appendix_business_listings_business_data_limits_rates_data_info import AppendixBusinessListingsBusinessDataLimitsRatesDataInfo



class AppendixBusinessDataLimitsRatesDataInfo(BaseModel):
    """
    AppendixBusinessDataLimitsRatesDataInfo
    """ # noqa: E501
    google: Optional[AppendixBusinessDataGoogleInfo] = Field(default=None, description=r"")
    locations: Optional[StrictFloat] = Field(default=None, description=r"")
    languages: Optional[StrictFloat] = Field(default=None, description=r"")
    errors: Optional[StrictFloat] = Field(default=None, description=r"")
    tripadvisor: Optional[AppendixTrBusinessDataDayLimitsRatesDataInfo] = Field(default=None, description=r"")
    trustpilot: Optional[AppendixTrBusinessDataDayLimitsRatesDataInfo] = Field(default=None, description=r"")
    id_list: Optional[StrictFloat] = Field(default=None, description=r"")
    business_listings: Optional[AppendixBusinessListingsBusinessDataLimitsRatesDataInfo] = Field(default=None, description=r"")
    available_filters: Optional[StrictFloat] = Field(default=None, description=r"")
    tasks_ready: Optional[StrictFloat] = Field(default=None, description=r"")
    __properties: ClassVar[List[str]] = [
        "google", 
        "locations", 
        "languages", 
        "errors", 
        "tripadvisor", 
        "trustpilot", 
        "id_list", 
        "business_listings", 
        "available_filters", 
        "tasks_ready", 
        ]

    additional_properties: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        excluded_fields: Set[str] = set([
        ])

        _dict = {}

        _dict['google'] = self.google.to_dict() if self.google else None
        _dict['locations'] = self.locations
        _dict['languages'] = self.languages
        _dict['errors'] = self.errors
        _dict['tripadvisor'] = self.tripadvisor.to_dict() if self.tripadvisor else None
        _dict['trustpilot'] = self.trustpilot.to_dict() if self.trustpilot else None
        _dict['id_list'] = self.id_list
        _dict['business_listings'] = self.business_listings.to_dict() if self.business_listings else None
        _dict['available_filters'] = self.available_filters
        _dict['tasks_ready'] = self.tasks_ready
        return _dict


    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "google": AppendixBusinessDataGoogleInfo.from_dict(obj["google"]) if obj.get("google") is not None else None,
            "locations": obj.get("locations"),
            "languages": obj.get("languages"),
            "errors": obj.get("errors"),
            "tripadvisor": AppendixTrBusinessDataDayLimitsRatesDataInfo.from_dict(obj["tripadvisor"]) if obj.get("tripadvisor") is not None else None,
            "trustpilot": AppendixTrBusinessDataDayLimitsRatesDataInfo.from_dict(obj["trustpilot"]) if obj.get("trustpilot") is not None else None,
            "id_list": obj.get("id_list"),
            "business_listings": AppendixBusinessListingsBusinessDataLimitsRatesDataInfo.from_dict(obj["business_listings"]) if obj.get("business_listings") is not None else None,
            "available_filters": obj.get("available_filters"),
            "tasks_ready": obj.get("tasks_ready"),
        })

        additional_properties = {k: v for k, v in obj.items() if k not in cls.__properties}
        _obj.additional_properties = additional_properties
        return _obj