from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set, Any, Dict, List
from typing_extensions import Self

from dataforseo_client.models.appendix_task_keywords_data_price_data_info import AppendixTaskKeywordsDataPriceDataInfo
from dataforseo_client.models.appendix_bing_keywords_data_price_data_info import AppendixBingKeywordsDataPriceDataInfo



class AppendixAiKeywordDataAiOptimizationPriceData(BaseModel):
    """
    AppendixAiKeywordDataAiOptimizationPriceData
    """ # noqa: E501
    available_filters: Optional[AppendixTaskKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    keywords_search_volume: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    locations_and_languages: Optional[AppendixTaskKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    __properties: ClassVar[List[str]] = [
        "available_filters", 
        "keywords_search_volume", 
        "locations_and_languages", 
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

        _dict['available_filters'] = self.available_filters.to_dict() if self.available_filters else None
        _dict['keywords_search_volume'] = self.keywords_search_volume.to_dict() if self.keywords_search_volume else None
        _dict['locations_and_languages'] = self.locations_and_languages.to_dict() if self.locations_and_languages else None
        return _dict


    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "available_filters": AppendixTaskKeywordsDataPriceDataInfo.from_dict(obj["available_filters"]) if obj.get("available_filters") is not None else None,
            "keywords_search_volume": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["keywords_search_volume"]) if obj.get("keywords_search_volume") is not None else None,
            "locations_and_languages": AppendixTaskKeywordsDataPriceDataInfo.from_dict(obj["locations_and_languages"]) if obj.get("locations_and_languages") is not None else None,
        })

        additional_properties = {k: v for k, v in obj.items() if k not in cls.__properties}
        _obj.additional_properties = additional_properties
        return _obj