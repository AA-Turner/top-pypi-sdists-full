from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set, Any, Dict, List
from typing_extensions import Self




class AiOptimizationLlmMentionsAvailableFiltersResultInfo(BaseModel):
    """
    AiOptimizationLlmMentionsAvailableFiltersResultInfo
    """ # noqa: E501
    search: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    search_mentions: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    target_metrics: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    multi_target_metrics: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_domains: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_pages: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_brands: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_brand_categories: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    target_metrics_lite: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_domains_lite: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_pages_lite: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_brands_lite: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    top_mentioned_brand_categories_lite: Optional[Dict[str, Optional[StrictStr]]] = Field(default=None, description=r"")
    __properties: ClassVar[List[str]] = [
        "search", 
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

        _dict['search'] = self.search
        _dict['search_mentions'] = self.search_mentions
        _dict['target_metrics'] = self.target_metrics
        _dict['multi_target_metrics'] = self.multi_target_metrics
        _dict['top_mentioned_domains'] = self.top_mentioned_domains
        _dict['top_mentioned_pages'] = self.top_mentioned_pages
        _dict['top_mentioned_brands'] = self.top_mentioned_brands
        _dict['top_mentioned_brand_categories'] = self.top_mentioned_brand_categories
        _dict['target_metrics_lite'] = self.target_metrics_lite
        _dict['top_mentioned_domains_lite'] = self.top_mentioned_domains_lite
        _dict['top_mentioned_pages_lite'] = self.top_mentioned_pages_lite
        _dict['top_mentioned_brands_lite'] = self.top_mentioned_brands_lite
        _dict['top_mentioned_brand_categories_lite'] = self.top_mentioned_brand_categories_lite
        return _dict


    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "search": obj.get("search"),
            "search_mentions": obj.get("search_mentions"),
            "target_metrics": obj.get("target_metrics"),
            "multi_target_metrics": obj.get("multi_target_metrics"),
            "top_mentioned_domains": obj.get("top_mentioned_domains"),
            "top_mentioned_pages": obj.get("top_mentioned_pages"),
            "top_mentioned_brands": obj.get("top_mentioned_brands"),
            "top_mentioned_brand_categories": obj.get("top_mentioned_brand_categories"),
            "target_metrics_lite": obj.get("target_metrics_lite"),
            "top_mentioned_domains_lite": obj.get("top_mentioned_domains_lite"),
            "top_mentioned_pages_lite": obj.get("top_mentioned_pages_lite"),
            "top_mentioned_brands_lite": obj.get("top_mentioned_brands_lite"),
            "top_mentioned_brand_categories_lite": obj.get("top_mentioned_brand_categories_lite"),
        })

        additional_properties = {k: v for k, v in obj.items() if k not in cls.__properties}
        _obj.additional_properties = additional_properties
        return _obj