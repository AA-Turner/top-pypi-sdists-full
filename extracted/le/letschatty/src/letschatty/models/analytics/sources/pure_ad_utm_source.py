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

    def __eq__(self, other: PureAdUtmSource) -> bool:
        if hasattr(other, "ad_id"):
            return self.ad_id == other.ad_id
        return False

    def __hash__(self) -> int:
        return hash(self.ad_id)