from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set, Any, Dict, List
from typing_extensions import Self

from dataforseo_client.models.appendix_info import AppendixInfo



class AppendixLlmMentionsAiOptimizationLimitsRatesDataInfo(BaseModel):
    """
    AppendixLlmMentionsAiOptimizationLimitsRatesDataInfo
    """ # noqa: E501
    search: Optional[AppendixInfo] = Field(default=None, description=r"")
    aggregated_metrics: Optional[AppendixInfo] = Field(default=None, description=r"")
    cross_aggregated_metrics: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_domains: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_pages: Optional[AppendixInfo] = Field(default=None, description=r"")
    locations_and_languages: Optional[StrictFloat] = Field(default=None, description=r"")
    available_filters: Optional[StrictFloat] = Field(default=None, description=r"")
    search_mentions: Optional[AppendixInfo] = Field(default=None, description=r"")
    target_metrics: Optional[AppendixInfo] = Field(default=None, description=r"")
    multi_target_metrics: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_domains: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_pages: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_brands: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_brand_categories: Optional[AppendixInfo] = Field(default=None, description=r"")
    target_metrics_lite: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_domains_lite: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_pages_lite: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_brands_lite: Optional[AppendixInfo] = Field(default=None, description=r"")
    top_mentioned_brand_categories_lite: Optional[AppendixInfo] = Field(default=None, description=r"")
    historical: Optional[AppendixInfo] = Field(default=None, description=r"")
    timeseries_delta: Optional[AppendixInfo] = Field(default=None, description=r"")
    timeseries_new_lost: Optional[AppendixInfo] = Field(default=None, description=r"")
    __properties: ClassVar[List[str]] = [
        "search", 
        "aggregated_metrics", 
        "cross_aggregated_metrics", 
        "top_domains", 
        "top_pages", 
        "locations_and_languages", 
        "available_filters", 
        "search_mentions", 
        "target_metrics", 
        "multi_target_metrics", 
        "top_mentioned_domains", 
        "top_mentioned_pages", 
        "top_mentioned_brands", 
        "top_mentioned_brand_categories", 
        "target_metrics_lite", 
        "top_mentioned_domains_lite", 
        "top_mentioned_pages_lite", 
        "top_mentioned_brands_lite", 
        "top_mentioned_brand_categories_lite", 
        "historical", 
        "timeseries_delta", 
        "timeseries_new_lost", 
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

        _dict['search'] = self.search.to_dict() if self.search else None
        _dict['aggregated_metrics'] = self.aggregated_metrics.to_dict() if self.aggregated_metrics else None
        _dict['cross_aggregated_metrics'] = self.cross_aggregated_metrics.to_dict() if self.cross_aggregated_metrics else None
        _dict['top_domains'] = self.top_domains.to_dict() if self.top_domains else None
        _dict['top_pages'] = self.top_pages.to_dict() if self.top_pages else None
        _dict['locations_and_languages'] = self.locations_and_languages
        _dict['available_filters'] = self.available_filters
        _dict['search_mentions'] = self.search_mentions.to_dict() if self.search_mentions else None
        _dict['target_metrics'] = self.target_metrics.to_dict() if self.target_metrics else None
        _dict['multi_target_metrics'] = self.multi_target_metrics.to_dict() if self.multi_target_metrics else None
        _dict['top_mentioned_domains'] = self.top_mentioned_domains.to_dict() if self.top_mentioned_domains else None
        _dict['top_mentioned_pages'] = self.top_mentioned_pages.to_dict() if self.top_mentioned_pages else None
        _dict['top_mentioned_brands'] = self.top_mentioned_brands.to_dict() if self.top_mentioned_brands else None
        _dict['top_mentioned_brand_categories'] = self.top_mentioned_brand_categories.to_dict() if self.top_mentioned_brand_categories else None
        _dict['target_metrics_lite'] = self.target_metrics_lite.to_dict() if self.target_metrics_lite else None
        _dict['top_mentioned_domains_lite'] = self.top_mentioned_domains_lite.to_dict() if self.top_mentioned_domains_lite else None
        _dict['top_mentioned_pages_lite'] = self.top_mentioned_pages_lite.to_dict() if self.top_mentioned_pages_lite else None
        _dict['top_mentioned_brands_lite'] = self.top_mentioned_brands_lite.to_dict() if self.top_mentioned_brands_lite else None
        _dict['top_mentioned_brand_categories_lite'] = self.top_mentioned_brand_categories_lite.to_dict() if self.top_mentioned_brand_categories_lite else None
        _dict['historical'] = self.historical.to_dict() if self.historical else None
        _dict['timeseries_delta'] = self.timeseries_delta.to_dict() if self.timeseries_delta else None
        _dict['timeseries_new_lost'] = self.timeseries_new_lost.to_dict() if self.timeseries_new_lost else None
        return _dict


    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "search": AppendixInfo.from_dict(obj["search"]) if obj.get("search") is not None else None,
            "aggregated_metrics": AppendixInfo.from_dict(obj["aggregated_metrics"]) if obj.get("aggregated_metrics") is not None else None,
            "cross_aggregated_metrics": AppendixInfo.from_dict(obj["cross_aggregated_metrics"]) if obj.get("cross_aggregated_metrics") is not None else None,
            "top_domains": AppendixInfo.from_dict(obj["top_domains"]) if obj.get("top_domains") is not None else None,
            "top_pages": AppendixInfo.from_dict(obj["top_pages"]) if obj.get("top_pages") is not None else None,
            "locations_and_languages": obj.get("locations_and_languages"),
            "available_filters": obj.get("available_filters"),
            "search_mentions": AppendixInfo.from_dict(obj["search_mentions"]) if obj.get("search_mentions") is not None else None,
            "target_metrics": AppendixInfo.from_dict(obj["target_metrics"]) if obj.get("target_metrics") is not None else None,
            "multi_target_metrics": AppendixInfo.from_dict(obj["multi_target_metrics"]) if obj.get("multi_target_metrics") is not None else None,
            "top_mentioned_domains": AppendixInfo.from_dict(obj["top_mentioned_domains"]) if obj.get("top_mentioned_domains") is not None else None,
            "top_mentioned_pages": AppendixInfo.from_dict(obj["top_mentioned_pages"]) if obj.get("top_mentioned_pages") is not None else None,
            "top_mentioned_brands": AppendixInfo.from_dict(obj["top_mentioned_brands"]) if obj.get("top_mentioned_brands") is not None else None,
            "top_mentioned_brand_categories": AppendixInfo.from_dict(obj["top_mentioned_brand_categories"]) if obj.get("top_mentioned_brand_categories") is not None else None,
            "target_metrics_lite": AppendixInfo.from_dict(obj["target_metrics_lite"]) if obj.get("target_metrics_lite") is not None else None,
            "top_mentioned_domains_lite": AppendixInfo.from_dict(obj["top_mentioned_domains_lite"]) if obj.get("top_mentioned_domains_lite") is not None else None,
            "top_mentioned_pages_lite": AppendixInfo.from_dict(obj["top_mentioned_pages_lite"]) if obj.get("top_mentioned_pages_lite") is not None else None,
            "top_mentioned_brands_lite": AppendixInfo.from_dict(obj["top_mentioned_brands_lite"]) if obj.get("top_mentioned_brands_lite") is not None else None,
            "top_mentioned_brand_categories_lite": AppendixInfo.from_dict(obj["top_mentioned_brand_categories_lite"]) if obj.get("top_mentioned_brand_categories_lite") is not None else None,
            "historical": AppendixInfo.from_dict(obj["historical"]) if obj.get("historical") is not None else None,
            "timeseries_delta": AppendixInfo.from_dict(obj["timeseries_delta"]) if obj.get("timeseries_delta") is not None else None,
            "timeseries_new_lost": AppendixInfo.from_dict(obj["timeseries_new_lost"]) if obj.get("timeseries_new_lost") is not None else None,
        })

        additional_properties = {k: v for k, v in obj.items() if k not in cls.__properties}
        _obj.additional_properties = additional_properties
        return _obj