from pydantic import Field, model_validator
from datetime import datetime, timedelta
from typing import Optional
from ...base_models import CompanyAssetModel
from ...utils.types.identifier import StrObjectId
from ...analytics.sources import Source
from ...analytics.sources.utms.referer_info import RefererInfo
from ...analytics.sources.utms.referer_info import DeviceType
from ...utils.types.source_types import SourceCheckerType

class ContactPoint(CompanyAssetModel):
    source_checker_method : Optional[SourceCheckerType] = Field(default=None)
    source_id: Optional[StrObjectId] = Field(default=None)
    template_name : Optional[str] = Field(default=None)
    match_timestamp: Optional[datetime] = Field(default=None)
    referer_info: Optional[RefererInfo] = Field(default=None)
    time_from_request_to_match : Optional[timedelta] = Field(default=None)
    topic_id : Optional[StrObjectId] = Field(default=None)
    chat_id : Optional[StrObjectId] = Field(default=None)
    message_id : Optional[str] = Field(default=None)
    ctwa_clid : Optional[str] = Field(default=None)
    fb_clid : Optional[str] = Field(default=None)
    gclid : Optional[str] = Field(default=None)
    client_ip_address : Optional[str] = Field(default=None)
    client_user_agent : Optional[str] = Field(default=None)
    client_external_id : Optional[str] = Field(default=None)
    button_id : Optional[str] = Field(default=None)
    button_name : Optional[str] = Field(default=None)
    device_type : Optional[DeviceType] = Field(default=None)
    new_chat : bool = Field(default=False)
    matched : bool = Field(default=False)
    expired : bool = Field(default=False)

    # @model_validator(mode="before")
    # def validate_source_id_or_template_name(cls, data):
    #     if data.get("source_id") is None and data.get("template_name") is None:
    #         raise ValueError("source_id or template_name is required")
    #     return data

    def __lt__(self, other: 'ContactPoint') -> bool:
        """Compare two ContactPoint instances based on their match_timestamp."""
        if self.match_timestamp is None or other.match_timestamp is None:
            return super().__lt__(other)
        return self.match_timestamp < other.match_timestamp

    def __gt__(self, other: 'ContactPoint') -> bool:
        """Compare two ContactPoint instances based on their match_timestamp."""
        if self.match_timestamp is None or other.match_timestamp is None:
            return super().__gt__(other)
        return self.match_timestamp > other.match_timestamp

    @property
    def matched_source_id(self) -> StrObjectId:
        if not self.source_id:
            raise ValueError("Source ID is not set")
        return self.source_id

    @property
    def locked_topic_id(self) -> StrObjectId:
        if not self.topic_id:
            raise ValueError("No topic id found for contact point")
        return self.topic_id