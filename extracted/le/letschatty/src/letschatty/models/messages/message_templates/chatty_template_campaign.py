from datetime import datetime
from typing import List, Dict, Optional, ClassVar, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from ...company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation

from letschatty.models.utils.types import Status
from ...base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel
from ...utils.types.identifier import StrObjectId
from ...utils.definitions import Area
from ...utils.types.serializer_type import SerializerType
from .recipient_of_template_campaign import RecipientOfTemplateCampaign
from bson import ObjectId
from zoneinfo import ZoneInfo
import logging
from enum import StrEnum
logger = logging.getLogger(__name__)

class CampaignStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    INCOMPLETE = "INCOMPLETE"
    ERROR = "ERROR"

class TemplateCampaignPreview(ChattyAssetPreview):
    template_name: Optional[str] = None
    is_updating_recipients_status: bool = Field(default=False)
    q_recipients: int = 0
    q_processed_recipients: int = 0
    q_recipients_succesfully_sent: int = 0
    q_recipients_failed_to_send: int = 0
    q_recipients_delivered: int = 0
    q_recipients_read: int = 0
    progress: float = 0.0
    status: CampaignStatus

    @classmethod
    def not_found(cls, id: StrObjectId, company_id: StrObjectId) -> 'TemplateCampaignPreview':
        return cls(
            _id=id,
            name=f"Not found {id}",
            company_id=company_id,
            created_at=datetime.now(tz=ZoneInfo("UTC")),
            updated_at=datetime.now(tz=ZoneInfo("UTC")),
            status=CampaignStatus.ERROR
        )

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        projection = super().get_projection()
        projection["q_recipients"] = 1
        projection["q_processed_recipients"] = 1
        projection["q_recipients_succesfully_sent"] = 1
        projection["q_recipients_failed_to_send"] = 1
        projection["q_recipients_delivered"] = 1
        projection["q_recipients_read"] = 1
        projection["is_updating_recipients_status"] = 1
        projection["template_name"] = 1
        projection["status"] = 1
        return projection

    @classmethod
    def from_asset(cls, asset: 'TemplateCampaign') -> 'TemplateCampaignPreview':
        return cls(
            _id=asset.id,
            name=getattr(asset, "name", "no name"),
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            template_name=asset.template_name,
            q_recipients_succesfully_sent=asset.q_recipients_succesfully_sent,
            q_recipients_failed_to_send=asset.q_recipients_failed_to_send,
            q_recipients_delivered=asset.q_recipients_delivered,
            q_recipients_read=asset.q_recipients_read,
            q_recipients=asset.q_recipients,
            q_processed_recipients=asset.q_processed_recipients,
            status=asset.status,
            is_updating_recipients_status=asset.is_updating_recipients_status,
            progress=asset.progress,
        )

    @model_validator(mode="after")
    def calculate_progress(self):
        if self.q_recipients == 0:
            self.progress = 0.0
        else:
            self.progress = self.q_processed_recipients / self.q_recipients
        return self

class TemplateCampaign(CompanyAssetModel):
    template_name: str
    name: str
    area: Area
    recipients: List[RecipientOfTemplateCampaign] = Field(default_factory=list)
    assign_to_agent: Optional[str] = None
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    chatty_ai_agent_config: Optional[ChattyAIConfigForAutomation] = None
    description: Optional[str] = None
    forced_send: bool = Field(default=False)
    date: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    q_recipients: int = 0
    q_processed_recipients: int = 0
    q_recipients_succesfully_sent: int = 0
    q_recipients_failed_to_send: int = 0
    q_recipients_delivered: int = 0
    q_recipients_read: int = 0
    status: CampaignStatus = Field(default=CampaignStatus.PENDING)
    is_updating_recipients_status: bool = Field(default=False)
    progress: float = 0.0
    observations: Optional[str] = None
    preview_class: ClassVar[type[TemplateCampaignPreview]] = TemplateCampaignPreview
    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"recipients", "tags", "products", "flow", "assign_to_agent", "description", "forced_send", "date"}
    }

    class ConfigDict:
        arbitrary_types_allowed = True


    @model_validator(mode="after")
    def check_status(self):
        if self.status == CampaignStatus.PENDING:
            pass
        elif self.status == CampaignStatus.PROCESSING and self.q_processed_recipients == self.q_recipients:
            self.status = CampaignStatus.COMPLETED
        elif self.status == CampaignStatus.PROCESSING and self.q_processed_recipients < self.q_recipients:
            self.status = CampaignStatus.INCOMPLETE
        if self.recipients is None or len(self.recipients) == 0:
            self.error(observations="No recipients found or recipients format was not valid, try again")
        self.q_recipients = len(self.recipients)

        return self

    def pause(self):
        if self.status in [CampaignStatus.PROCESSING, CampaignStatus.PENDING]:
            self.status = CampaignStatus.PAUSED
        else:
            raise ValueError(f"Campaign {self.name} can't be paused because its status is {self.status}")

    def is_processing(self) -> bool:
        return self.status == CampaignStatus.PROCESSING

    def start_processing(self):
        if self.status == CampaignStatus.PENDING or self.status == CampaignStatus.PAUSED or self.status == CampaignStatus.INCOMPLETE:
            self.status = CampaignStatus.PROCESSING
        else:
            raise ValueError(f"Campaign {self.name} can't be started because its status is {self.status}")

    def finish(self):
        logger.debug(f"Finishing campaign {self.name} #id {self.id} status is {self.status}")
        if self.status == CampaignStatus.COMPLETED:
            return
        if self.status != CampaignStatus.PROCESSING:
            raise ValueError(f"Campaign {self.name} can't be finished because its status is {self.status}")

        self.status = CampaignStatus.COMPLETED if self.q_recipients == self.q_processed_recipients else CampaignStatus.INCOMPLETE

    def error(self, observations: Optional[str] = None):
        logger.warning(f"Campaign {self.name} #id {self.id} has an error: {observations}")
        self.status = CampaignStatus.ERROR
        self.observations = observations

    def update_counts_status(self, recipient: RecipientOfTemplateCampaign):
        match recipient.status:
            case Status.META_API_CALL_SUCCESS:
                self.q_recipients_succesfully_sent += 1
            case Status.FAILED:
                self.q_recipients_failed_to_send += 1
            case Status.DELIVERED:
                self.q_recipients_delivered += 1
            case Status.READ:
                self.q_recipients_read += 1

    def reset_counts(self):
        self.q_recipients_succesfully_sent = 0
        self.q_recipients_failed_to_send = 0
        self.q_recipients_delivered = 0
        self.q_recipients_read = 0
