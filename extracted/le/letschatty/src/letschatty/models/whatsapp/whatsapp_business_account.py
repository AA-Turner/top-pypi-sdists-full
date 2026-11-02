"""A WABA connected to a company, and the business portfolio it belongs to.

Both are registered per company: a WABA (and its portfolio) may be shared by several Chatty
companies, so the Meta id alone is not a key. Unique key: `{company_id, waba_id}` /
`{company_id, portfolio_id}`.
"""
from datetime import datetime
from typing import Any, Dict, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from ..utils.types.identifier import StrObjectId
from .time import utc_now


class WhatsAppBusinessAccount(BaseModel):
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    company_id: StrObjectId
    waba_id: str = Field(description="Meta id of the WABA")
    portfolio_id: Optional[str] = Field(default=None, description="Meta id of its business portfolio")
    name: str = ""
    dataset_id: Optional[str] = Field(default=None, description="Meta Conversions API dataset of this WABA")
    continuous_conversation_template_name: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    def to_document(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)

    @classmethod
    def from_document(cls, document: Dict[str, Any]) -> "WhatsAppBusinessAccount":
        return cls(**{**document, "_id": str(document["_id"])})


class WhatsAppPortfolio(BaseModel):
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    company_id: StrObjectId
    portfolio_id: str = Field(description="Meta id of the business portfolio")
    name: str = ""
    verified: Optional[bool] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    def to_document(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)

    @classmethod
    def from_document(cls, document: Dict[str, Any]) -> "WhatsAppPortfolio":
        return cls(**{**document, "_id": str(document["_id"])})
