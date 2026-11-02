from __future__ import annotations
from typing import List, Optional, Any
from pydantic import Field, model_validator, field_validator

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType

class TemplateSource(SourceBase):
    source_checker: SourceCheckerType = Field(default=SourceCheckerType.TEMPLATE)
    template_name: str

    @property
    def default_category(self) -> str:
        return "Templates"

    @property
    def type(self) -> SourceType:
        return SourceType.TEMPLATE_SOURCE

    def __eq__(self, other: TemplateSource) -> bool:
        if not isinstance(other, TemplateSource):
            return False
        return bool(self.name == other.name)

    def __hash__(self) -> int:
        return hash(self.name)