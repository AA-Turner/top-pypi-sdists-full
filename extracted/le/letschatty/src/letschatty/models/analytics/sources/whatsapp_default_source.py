from __future__ import annotations
from typing import Optional
from pydantic import Field, ConfigDict

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.types.identifier import StrObjectId

from bson import ObjectId

class WhatsAppDefaultSource(SourceBase):
    """Default source for organic WhatsApp messages"""
    name: str = Field(default="WhatsApp Default (organic)", frozen=True)
    description: str = Field(
        default="New chat that couldn't be attributed to any other source, but still a touchpoint",
        frozen=True
    )
    agent_email: str = Field(default="default_settings@letschatty.com", frozen=True)
    category: str = Field(default="Primer contacto (nuevo chat) sin fuente de origen", frozen=True)
    source_checker: SourceCheckerType = Field(
        default=SourceCheckerType.FIRST_CONTACT,
        frozen=True
    )

    @property
    def default_category(self) -> str:
        return "Primer contacto (nuevo chat) sin fuente de origen"


    @property
    def type(self) -> SourceType:
        return SourceType.WHATSAPP_DEFAULT_SOURCE

    def __eq__(self, other: object) -> bool:
        """WhatsApp default sources are unique, so they're equal if they're the same type"""
        return isinstance(other, WhatsAppDefaultSource)

    def __hash__(self) -> int:
        return hash(self.type)
