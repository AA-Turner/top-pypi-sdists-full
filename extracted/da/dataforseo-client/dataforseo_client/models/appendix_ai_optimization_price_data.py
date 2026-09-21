from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set, Any, Dict, List
from typing_extensions import Self

from dataforseo_client.models.appendix_llm_scraper_ai_optimization_price_data import AppendixLlmScraperAiOptimizationPriceData
from dataforseo_client.models.appendix_llm_mentions_ai_optimization_price_data import AppendixLlmMentionsAiOptimizationPriceData
from dataforseo_client.models.appendix_ai_keyword_data_ai_optimization_price_data import AppendixAiKeywordDataAiOptimizationPriceData
from dataforseo_client.models.appendix_task_keywords_data_price_data_info import AppendixTaskKeywordsDataPriceDataInfo
from dataforseo_client.models.appendix_llm_responses_ai_optimization_price_data import AppendixLlmResponsesAiOptimizationPriceData



class AppendixAiOptimizationPriceData(BaseModel):
    """
    AppendixAiOptimizationPriceData
    """ # noqa: E501
    llm_scraper: Optional[AppendixLlmScraperAiOptimizationPriceData] = Field(default=None, description=r"")
    llm_mentions: Optional[AppendixLlmMentionsAiOptimizationPriceData] = Field(default=None, description=r"")
    ai_keyword_data: Optional[AppendixAiKeywordDataAiOptimizationPriceData] = Field(default=None, description=r"")
    errors: Optional[AppendixTaskKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    id_list: Optional[AppendixTaskKeywordsDataPriceDataInfo] = Field(default=None, description=r"")
    llm_responses: Optional[AppendixLlmResponsesAiOptimizationPriceData] = Field(default=None, description=r"")
    __properties: ClassVar[List[str]] = [
        "llm_scraper", 
        "llm_mentions", 
        "ai_keyword_data", 
        "errors", 
        "id_list", 
        "llm_responses", 
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

        _dict['llm_scraper'] = self.llm_scraper.to_dict() if self.llm_scraper else None
        _dict['llm_mentions'] = self.llm_mentions.to_dict() if self.llm_mentions else None
        _dict['ai_keyword_data'] = self.ai_keyword_data.to_dict() if self.ai_keyword_data else None
        _dict['errors'] = self.errors.to_dict() if self.errors else None
        _dict['id_list'] = self.id_list.to_dict() if self.id_list else None
        _dict['llm_responses'] = self.llm_responses.to_dict() if self.llm_responses else None
        return _dict


    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "llm_scraper": AppendixLlmScraperAiOptimizationPriceData.from_dict(obj["llm_scraper"]) if obj.get("llm_scraper") is not None else None,
            "llm_mentions": AppendixLlmMentionsAiOptimizationPriceData.from_dict(obj["llm_mentions"]) if obj.get("llm_mentions") is not None else None,
            "ai_keyword_data": AppendixAiKeywordDataAiOptimizationPriceData.from_dict(obj["ai_keyword_data"]) if obj.get("ai_keyword_data") is not None else None,
            "errors": AppendixTaskKeywordsDataPriceDataInfo.from_dict(obj["errors"]) if obj.get("errors") is not None else None,
            "id_list": AppendixTaskKeywordsDataPriceDataInfo.from_dict(obj["id_list"]) if obj.get("id_list") is not None else None,
            "llm_responses": AppendixLlmResponsesAiOptimizationPriceData.from_dict(obj["llm_responses"]) if obj.get("llm_responses") is not None else None,
        })

        additional_properties = {k: v for k, v in obj.items() if k not in cls.__properties}
        _obj.additional_properties = additional_properties
        return _obj