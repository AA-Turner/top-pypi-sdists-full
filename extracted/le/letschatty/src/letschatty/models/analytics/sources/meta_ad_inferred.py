from __future__ import annotations
from pydantic import Field

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType


class MetaAdInferredSource(SourceBase):
    """Company-wide bucket for chats Meta confirmed as ad-originated without saying WHICH ad.

    The message arrived with no referral, but the conversation receipt (statuses'
    ``conversation.origin.type == "referral_conversion"``) — or an explicit human
    decision ("it was an ad, I don't know which") — asserts the chat came from a
    Click-to-WhatsApp ad. One source per company; the per-ad estimation lives on the
    contact point (``inferred_attribution.candidates``), never here.

    Same category as PureAd so category rollups add up; distinguishable by type and
    by the contact point's ``source_checker_method``. It never enters the inbound
    message source-checker rotation.
    """
    name: str = Field(default="Anuncios Meta (inferido)", frozen=True)
    description: str = Field(
        default="Chats confirmados como originados en un anuncio de Meta (por el recibo de la conversación o por decisión humana), sin identificar qué anuncio.",
        frozen=True,
    )
    category: str = Field(default="Anuncios Click to WhatsApp (META)", frozen=True)
    source_checker: SourceCheckerType = Field(
        default=SourceCheckerType.REFERRAL_CONVERSION,
        frozen=True,
    )

    @property
    def default_category(self) -> str:
        return "Anuncios Click to WhatsApp (META)"

    @property
    def type(self) -> SourceType:
        return SourceType.META_AD_INFERRED

    def __eq__(self, other: object) -> bool:
        """One per company: equal iff the other is also the company bucket."""
        return isinstance(other, MetaAdInferredSource)

    def __hash__(self) -> int:
        return hash(self.type)
