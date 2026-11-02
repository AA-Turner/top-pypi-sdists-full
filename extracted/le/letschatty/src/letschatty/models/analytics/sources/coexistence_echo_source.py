from __future__ import annotations
from pydantic import Field

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType


class CoexistenceEchoSource(SourceBase):
    """Internal source for chats the OWNER starts from the WhatsApp Business App
    (a WhatsApp-Coexistence outgoing echo), with no inbound message.

    Contact points on echo-created chats are created already-matched to this
    source, so it is never run through the inbound message source-checker
    rotation. Mirrors ``ContactImportSource`` but is kept distinct so the owner
    can configure a dedicated default AI agent for owner-initiated conversations
    (e.g. the executive assistant) without coupling it to bulk contact imports.
    """
    name: str = Field(default="Iniciado por el dueño (WhatsApp App)", frozen=True)
    description: str = Field(
        default="Conversación iniciada por el dueño desde la app de WhatsApp (eco de coexistencia).",
        frozen=True
    )
    category: str = Field(default="Iniciado por el dueño", frozen=True)
    source_checker: SourceCheckerType = Field(
        default=SourceCheckerType.COEXISTENCE_ECHO,
        frozen=True
    )

    @property
    def default_category(self) -> str:
        return "Iniciado por el dueño"

    @property
    def type(self) -> SourceType:
        return SourceType.COEXISTENCE_ECHO

    def __eq__(self, other: object) -> bool:
        """Coexistence-echo sources are unique per company, so they're equal if they're the same type"""
        return isinstance(other, CoexistenceEchoSource)

    def __hash__(self) -> int:
        return hash(self.type)
