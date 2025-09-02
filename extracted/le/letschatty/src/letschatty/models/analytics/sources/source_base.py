from typing import List, Optional, Dict, Any
from pydantic import Field, model_validator, field_validator, ConfigDict
from abc import abstractmethod

from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.custom_exceptions import InvalidSourceChecker
from ...utils.types.identifier import StrObjectId
from .helpers import SourceHelpers
from ...base_models import CompanyAssetModel
from ....models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation


import logging
logger = logging.getLogger("source_base")

class SourceBase(CompanyAssetModel):
    agent_id: Optional[str] = Field(alias="agent_email", default=None)
    description: Optional[str] = Field(default="")
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    chatty_ai_agent_config: Optional[ChattyAIConfigForAutomation] = Field(default=None)
    trackeable: bool = Field(default=True)
    category: str = Field(default="")
    source_checker: SourceCheckerType
    name: str = Field()

    model_config = ConfigDict(extra='ignore', exclude_none=True) #type: ignore

    @property
    @abstractmethod
    def default_category(self) -> str:
        pass

    @property
    def topic_id_set(self) -> StrObjectId:
        if not hasattr(self, "topic_id"):
            raise ValueError(f"Source {self.name} of type {self.type} has no attribute topic_id")
        if not self.topic_id:
            raise ValueError(f"Topic id not set for source {self.name} of type {self.type} id {self.id}")
        return self.topic_id


    def model_dump(self, *args, **kwargs) -> Dict:
        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        data["type"] = self.type
        return data

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs["by_alias"] = True
        data = super().model_dump_json(*args, **kwargs)
        data["type"] = self.type.value
        return data

    @field_validator('source_checker', mode="before")
    @classmethod
    def lowercase_source_checker(cls, v: str) -> str:
        return v.lower()

    @model_validator(mode='after')
    def validate_source(self):
        if not SourceHelpers.is_valid_source_checker(source_type=self.type,source_checker=self.source_checker):
            raise InvalidSourceChecker(f"Source checker {self.source_checker} not valid for source type {self.type} | Allowed ones are {SourceHelpers.get_source_checkers(self.type)}")
        if not self.category:
            self.category = self.default_category
        return self


    @model_validator(mode='before')
    def validate_lists(cls, data: Dict) -> Dict:
        if "products" in data and data["products"] is None:
            data["products"] = []
        if "flow" in data and data["flow"] is None:
            data["flow"] = []
        if "tags" in data and data["tags"] is None:
            data["tags"] = []
        return data

    @property
    @abstractmethod
    def type(self) -> SourceType:
        pass