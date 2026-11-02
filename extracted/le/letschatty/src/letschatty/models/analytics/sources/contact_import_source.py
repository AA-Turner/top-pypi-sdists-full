from __future__ import annotations
from pydantic import Field

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType


class ContactImportSource(SourceBase):
    """Internal source for contacts created via bulk import (no inbound message).

    Contact points on imported chats are created already-matched to this source,
    so it is never run through the inbound message source-checker rotation.
    """
    name: str = Field(default="Contactos importados", frozen=True)
    description: str = Field(
        default="Contacto creado mediante importación masiva, sin mensaje entrante.",
        frozen=True
    )
    category: str = Field(default="Contactos importados", frozen=True)
    source_checker: SourceCheckerType = Field(
        default=SourceCheckerType.CONTACT_IMPORT,
        frozen=True
    )

    @property
    def default_category(self) -> str:
        return "Contactos importados"

    @property
    def type(self) -> SourceType:
        return SourceType.CONTACT_IMPORT

    def __eq__(self, other: object) -> bool:
        """Contact-import sources are unique per company, so they're equal if they're the same type"""
        return isinstance(other, ContactImportSource)

    def __hash__(self) -> int:
        return hash(self.type)
