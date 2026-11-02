from typing import Optional
from pydantic import Field, model_validator, ConfigDict

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType
from letschatty.models.utils.types.serializer_type import SerializerType

from ...utils.types.identifier import StrObjectId
from .utms.utm_query_params import QueryUTMParams

class UTMSource(SourceBase):
    utm_campaign: str = Field(default="")
    url: str = Field(description="The URL of the UTM source")
    source_checker: SourceCheckerType = Field(default=SourceCheckerType.CHATTY_PIXEL)
    meta_ad_id: Optional[str] = Field(default=None)
    google_ad_id: Optional[str] = Field(default=None)

    @property
    def type(self) -> SourceType:
        return SourceType.UTM_SOURCE

    @property
    def default_category(self) -> str:
        if self.meta_ad_id:
            return "META Ads con destino web (tráfico, ventas, etc.)"
        elif self.google_ad_id:
            return "Google Ads con destino web (search, display, etc.)"
        else:
            return "utm_source"

    def model_dump(self, *args, **kwargs) -> dict:
        """Custom serialization based on context"""
        data = super().model_dump(*args, **kwargs)
        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UTMSource):
            return False
        return self.utm_campaign == other.utm_campaign and self.utm_campaign != ""

    def __hash__(self) -> int:
        return hash(self.utm_campaign)

    @property
    def has_utm_campaign(self) -> bool:
        return self.utm_campaign != ""