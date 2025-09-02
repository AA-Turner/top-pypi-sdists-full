from pydantic import BaseModel, Field
from typing import Optional, List
from ..base_models.chatty_asset_model import CompanyAssetModel
from ..utils.types.identifier import StrObjectId
from .quality_scoring import QualityScore
from .highlight import Highlight
from ..company.assets.chat_assets import AssignedAssetToChat, SaleAssignedToChat, ContactPointAssignedToChat
from ..company.CRM.funnel import ClientFunnel
from ..utils.types.serializer_type import SerializerType

class Client(CompanyAssetModel):
    waid: str
    name: str
    country: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    DNI: Optional[str] = Field(default=None)
    lead_quality: QualityScore = Field(default=QualityScore.NEUTRAL)
    products: List[AssignedAssetToChat] = Field(default=list())
    tags: List[AssignedAssetToChat] = Field(default=list())
    sales: List[SaleAssignedToChat] = Field(default=list())
    highlights: List[Highlight] = Field(default=list())
    contact_points: List[ContactPointAssignedToChat] = Field(default=list())
    business_area: Optional[StrObjectId] = Field(default=None, description="It's a business related area, that works as a queue for the chats")
    external_id: Optional[str] = Field(default=None)
    funnels : List[ClientFunnel] = Field(default=list())
    exclude_fields = {
        SerializerType.FRONTEND: {"products", "tags", "sales", "contact_points", "highlights"}
    }

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
