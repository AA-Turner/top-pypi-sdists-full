from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, StrictBool
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set, Any, Dict, List
from typing_extensions import Self

from dataforseo_client.models.appendix_llm_responses_ai_optimization_limits_rates_data_info import AppendixLlmResponsesAiOptimizationLimitsRatesDataInfo
from dataforseo_client.models.appendix_ai_keyword_data_ai_optimization_limits_rates_data_info import AppendixAiKeywordDataAiOptimizationLimitsRatesDataInfo
from dataforseo_client.models.appendix_serp_days_rates_data_info import AppendixSerpDaysRatesDataInfo
from dataforseo_client.models.appendix_llm_mentions_ai_optimization_limits_rates_data_info import AppendixLlmMentionsAiOptimizationLimitsRatesDataInfo



class AppendixAiOptimizationLimitsRatesDataInfo(BaseModel):
    """
    AppendixAiOptimizationLimitsRatesDataInfo
    """ # noqa: E501
    llm_responses: Optional[AppendixLlmResponsesAiOptimizationLimitsRatesDataInfo] = Field(default=None, description=r"")
    ai_keyword_data: Optional[AppendixAiKeywordDataAiOptimizationLimitsRatesDataInfo] = Field(default=None, description=r"")
    errors: Optional[StrictFloat] = Field(default=None, description=r"")
    llm_scraper: Optional[AppendixSerpDaysRatesDataInfo] = Field(default=None, description=r"")
    llm_mentions: Optional[AppendixLlmMentionsAiOptimizationLimitsRatesDataInfo] = Field(default=None, description=r"")
    id_list: Optional[StrictFloat] = Field(default=None, description=r"")
    __properties: ClassVar[List[str]] = [
        "llm_responses", 
        "ai_keyword_data", 
        "errors", 
        "llm_scraper", 
        "llm_mentions", 
        "id_list", 
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

        _dict['llm_responses'] = self.llm_responses.to_dict() if self.llm_responses else None
        _dict['ai_keyword_data'] = self.ai_keyword_data.to_dict() if self.ai_keyword_data else None
        _dict['errors'] = self.errors
        _dict['llm_scraper'] = self.llm_scraper.to_dict() if self.llm_scraper else None
        _dict['llm_mentions'] = self.llm_mentions.to_dict() if self.llm_mentions else None
        _dict['id_list'] = self.id_list
        return _dict


    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "llm_responses": AppendixLlmResponsesAiOptimizationLimitsRatesDataInfo.from_dict(obj["llm_responses"]) if obj.get("llm_responses") is not None else None,
            "ai_keyword_data": AppendixAiKeywordDataAiOptimizationLimitsRatesDataInfo.from_dict(obj["ai_keyword_data"]) if obj.get("ai_keyword_data") is not None else None,
            "errors": obj.get("errors"),
            "llm_scraper": AppendixSerpDaysRatesDataInfo.from_dict(obj["llm_scraper"]) if obj.get("llm_scraper") is not None else None,
            "llm_mentions": AppendixLlmMentionsAiOptimizationLimitsRatesDataInfo.from_dict(obj["llm_mentions"]) if obj.get("llm_mentions") is not None else None,
            "id_list": obj.get("id_list"),
        })

        additional_properties = {k: v for k, v in obj.items() if k not in cls.__properties}
        _obj.additional_properties = additional_properties
        return _obj