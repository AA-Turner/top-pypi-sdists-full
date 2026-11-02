from __future__ import annotations
from pydantic import Field, ConfigDict
from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType

class PureAdUtmSource(SourceBase):
    ad_id: str
    source_checker: SourceCheckerType = Field(default=SourceCheckerType.AD_ID_IN_UTM_PARAMS)

    @property
    def default_category(self) -> str:
        return "META Ads con destino web (tráfico, ventas, etc.)"

    @property
    def type(self) -> SourceType:
        return SourceType.PURE_AD_UTM_SOURCE

    def __eq__(self, other: object) -> bool:
        # Type-strict: see PureAd.__eq__ for why matching any source that merely *has*
        # an ad_id (PureAd, GoogleAdUtmSource) is wrong.
        if not isinstance(other, PureAdUtmSource):
            return False
        return bool(self.ad_id and other.ad_id and self.ad_id == other.ad_id)

    def __hash__(self) -> int:
        return hash(self.ad_id)