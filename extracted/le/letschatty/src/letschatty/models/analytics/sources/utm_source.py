from typing import Optional
from pydantic import Field, model_validator, ConfigDict

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType
from letschatty.models.utils.types.serializer_type import SerializerType

from ...utils.types.identifier import StrObjectId
from .utms.utm_query_params import QueryUTMParams

class UTMSource(SourceBase):
    utm_parameters: QueryUTMParams
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

    @property
    @model_validator(mode='before')
    @classmethod
    def validate_utm_parameters(cls, data: dict | SourceBase) -> dict:
        """Validate and convert utm_parameters if needed"""
        if not isinstance(data, dict):
            data = data.model_dump()

        utm_params = data.get('utm_parameters')
        if not utm_params:
            raise ValueError("UTM parameters are required")
        if not isinstance(utm_params, QueryUTMParams):
            data['utm_parameters'] = QueryUTMParams(**utm_params)
        return data

    def get_utm(self) -> str:
        """Get the full UTM URL"""
        return self.utm_parameters.get_utm()

    def model_dump(self, *args, **kwargs) -> dict:
        """Custom serialization based on context"""
        data = super().model_dump(*args, **kwargs)
        serializer = kwargs.get('serializer', SerializerType.API)
        if serializer == SerializerType.FRONTEND or serializer == SerializerType.FRONTEND_ASSET_PREVIEW:
            data["full_url"] = self.get_utm()
        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UTMSource):
            return False
        return self.utm_parameters == other.utm_parameters

    def __hash__(self) -> int:
        return hash(self.utm_parameters)