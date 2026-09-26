# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["FieldExtractorGetResponse", "Rule", "RuleField"]


class RuleField(BaseModel):
    expression: str
    """Wirefilter value expression."""

    name: str
    """Field name."""


class Rule(BaseModel):
    fields: List[RuleField]

    ref: str
    """Stable rule identifier."""

    description: Optional[str] = None
    """Human-readable rule description."""


class FieldExtractorGetResponse(BaseModel):
    extractor: str
    """Extractor type."""

    rules: List[Rule]
