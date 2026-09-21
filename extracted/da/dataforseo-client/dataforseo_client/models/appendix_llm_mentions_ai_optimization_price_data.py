from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set, Any, Dict, List
from typing_extensions import Self

from dataforseo_client.models.appendix_bing_keywords_data_price_data_info import AppendixBingKeywordsDataPriceDataInfo
from dataforseo_client.models.appendix_task_keywords_data_price_data_info import AppendixTaskKeywordsDataPriceDataInfo



class AppendixLlmMentionsAiOptimizationPriceData(BaseModel):
    """
    AppendixLlmMentionsAiOptimizationPriceData
    """ # noqa: E501
    aggregated_metrics: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    available_filters: Optional[AppendixTaskKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    cross_aggregated_metrics: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    historical: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    locations_and_languages: Optional[AppendixTaskKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    multi_target_metrics: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    search: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    search_mentions: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    target_metrics: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    target_metrics_lite: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    timeseries_delta: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    timeseries_new_lost: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_domains: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_brand_categories: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_brand_categories_lite: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_brands: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_brands_lite: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_domains: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_domains_lite: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_pages: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_mentioned_pages_lite: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    top_pages: Optional[AppendixBingKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    __properties: ClassVar[List[str]] = [
        "aggregated_metrics", 
        "available_filters", 
        "cross_aggregated_metrics", 
        "historical", 
        "locations_and_languages", 
        "multi_target_metrics", 
        "search", 
        "search_mentions", 
        "target_metrics", 
        "target_metrics_lite", 
        "timeseries_delta", 
        "timeseries_new_lost", 
        "top_domains", 
        "top_mentioned_brand_categories", 
        "top_mentioned_brand_categories_lite", 
        "top_mentioned_brands", 
        "top_mentioned_brands_lite", 
        "top_mentioned_domains", 
        "top_mentioned_domains_lite", 
        "top_mentioned_pages", 
        "top_mentioned_pages_lite", 
        "top_pages", 
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

        _dict['aggregated_metrics'] = self.aggregated_metrics.to_dict() if self.aggregated_metrics else None
        _dict['available_filters'] = self.available_filters.to_dict() if self.available_filters else None
        _dict['cross_aggregated_metrics'] = self.cross_aggregated_metrics.to_dict() if self.cross_aggregated_metrics else None
        _dict['historical'] = self.historical.to_dict() if self.historical else None
        _dict['locations_and_languages'] = self.locations_and_languages.to_dict() if self.locations_and_languages else None
        _dict['multi_target_metrics'] = self.multi_target_metrics.to_dict() if self.multi_target_metrics else None
        _dict['search'] = self.search.to_dict() if self.search else None
        _dict['search_mentions'] = self.search_mentions.to_dict() if self.search_mentions else None
        _dict['target_metrics'] = self.target_metrics.to_dict() if self.target_metrics else None
        _dict['target_metrics_lite'] = self.target_metrics_lite.to_dict() if self.target_metrics_lite else None
        _dict['timeseries_delta'] = self.timeseries_delta.to_dict() if self.timeseries_delta else None
        _dict['timeseries_new_lost'] = self.timeseries_new_lost.to_dict() if self.timeseries_new_lost else None
        _dict['top_domains'] = self.top_domains.to_dict() if self.top_domains else None
        _dict['top_mentioned_brand_categories'] = self.top_mentioned_brand_categories.to_dict() if self.top_mentioned_brand_categories else None
        _dict['top_mentioned_brand_categories_lite'] = self.top_mentioned_brand_categories_lite.to_dict() if self.top_mentioned_brand_categories_lite else None
        _dict['top_mentioned_brands'] = self.top_mentioned_brands.to_dict() if self.top_mentioned_brands else None
        _dict['top_mentioned_brands_lite'] = self.top_mentioned_brands_lite.to_dict() if self.top_mentioned_brands_lite else None
        _dict['top_mentioned_domains'] = self.top_mentioned_domains.to_dict() if self.top_mentioned_domains else None
        _dict['top_mentioned_domains_lite'] = self.top_mentioned_domains_lite.to_dict() if self.top_mentioned_domains_lite else None
        _dict['top_mentioned_pages'] = self.top_mentioned_pages.to_dict() if self.top_mentioned_pages else None
        _dict['top_mentioned_pages_lite'] = self.top_mentioned_pages_lite.to_dict() if self.top_mentioned_pages_lite else None
        _dict['top_pages'] = self.top_pages.to_dict() if self.top_pages else None
        return _dict


    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "aggregated_metrics": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["aggregated_metrics"]) if obj.get("aggregated_metrics") is not None else None,
            "available_filters": AppendixTaskKeywordsDataPriceDataInfo.from_dict(obj["available_filters"]) if obj.get("available_filters") is not None else None,
            "cross_aggregated_metrics": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["cross_aggregated_metrics"]) if obj.get("cross_aggregated_metrics") is not None else None,
            "historical": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["historical"]) if obj.get("historical") is not None else None,
            "locations_and_languages": AppendixTaskKeywordsDataPriceDataInfo.from_dict(obj["locations_and_languages"]) if obj.get("locations_and_languages") is not None else None,
            "multi_target_metrics": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["multi_target_metrics"]) if obj.get("multi_target_metrics") is not None else None,
            "search": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["search"]) if obj.get("search") is not None else None,
            "search_mentions": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["search_mentions"]) if obj.get("search_mentions") is not None else None,
            "target_metrics": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["target_metrics"]) if obj.get("target_metrics") is not None else None,
            "target_metrics_lite": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["target_metrics_lite"]) if obj.get("target_metrics_lite") is not None else None,
            "timeseries_delta": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["timeseries_delta"]) if obj.get("timeseries_delta") is not None else None,
            "timeseries_new_lost": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["timeseries_new_lost"]) if obj.get("timeseries_new_lost") is not None else None,
            "top_domains": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_domains"]) if obj.get("top_domains") is not None else None,
            "top_mentioned_brand_categories": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_brand_categories"]) if obj.get("top_mentioned_brand_categories") is not None else None,
            "top_mentioned_brand_categories_lite": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_brand_categories_lite"]) if obj.get("top_mentioned_brand_categories_lite") is not None else None,
            "top_mentioned_brands": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_brands"]) if obj.get("top_mentioned_brands") is not None else None,
            "top_mentioned_brands_lite": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_brands_lite"]) if obj.get("top_mentioned_brands_lite") is not None else None,
            "top_mentioned_domains": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_domains"]) if obj.get("top_mentioned_domains") is not None else None,
            "top_mentioned_domains_lite": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_domains_lite"]) if obj.get("top_mentioned_domains_lite") is not None else None,
            "top_mentioned_pages": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_pages"]) if obj.get("top_mentioned_pages") is not None else None,
            "top_mentioned_pages_lite": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_mentioned_pages_lite"]) if obj.get("top_mentioned_pages_lite") is not None else None,
            "top_pages": AppendixBingKeywordsDataPriceDataInfo.from_dict(obj["top_pages"]) if obj.get("top_pages") is not None else None,
        })

        additional_properties = {k: v for k, v in obj.items() if k not in cls.__properties}
        _obj.additional_properties = additional_properties
        return _obj