from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from ..base_models.chatty_asset_model import CompanyAssetModel
from ..utils.types.identifier import StrObjectId
from .quality_scoring import QualityScore
from .highlight import Highlight
from ..company.assets.chat_assets import AssignedAssetToChat, SaleAssignedToChat, ContactPointAssignedToChat
from ..utils.types.serializer_type import SerializerType

class Client(CompanyAssetModel):
    waid: str
    name: str
    country: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    document_id: Optional[str] = Field(default=None, alias="DNI")
    lead_form_data: Dict[str, Any] = Field(default={}, description="Structured customer data collected during conversation")
    lead_quality: QualityScore = Field(default=QualityScore.NEUTRAL)
    products: List[AssignedAssetToChat] = Field(default=list())
    tags: List[AssignedAssetToChat] = Field(default=list())
    sales: List[SaleAssignedToChat] = Field(default=list())
    highlights: List[Highlight] = Field(default=list())
    contact_points: List[ContactPointAssignedToChat] = Field(default=list())
    business_area: Optional[StrObjectId] = Field(default=None, description="It's a business related area, that works as a queue for the chats")
    external_id: Optional[str] = Field(default=None)
    exclude_fields = {
        SerializerType.FRONTEND: {"products", "tags", "sales", "contact_points", "highlights"}
    }

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    def get_waid(self) -> str:
        return self.waid

    def get_name(self) -> str:
        return self.name

    def get_country(self) -> Optional[str]:
        return self.country

    def get_email(self) -> Optional[str]:
        return self.email

    @property
    def get_info(self) -> dict:
        return self.model_dump()

class ClientData(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    DNI: Optional[str] = None
    photo: Optional[str] = None
    external_id: Optional[str] = None
    lead_form_data: Optional[Dict[str, Any]] = None