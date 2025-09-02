from pydantic import BaseModel, Field
from typing import Optional, ClassVar
from ...base_models.chatty_asset_model import CompanyAssetModel
from ...utils.types.identifier import StrObjectId

class Sale(CompanyAssetModel):
    chat_id: StrObjectId
    product_id: StrObjectId
    quantity: int
    total_amount: float
    currency: str
    paid_amount: float
    installments: int
    details: dict
    crm_id: Optional[str] = Field(default=None)
    creator_id: StrObjectId

class SaleRequest(BaseModel):
    product_id: StrObjectId
    quantity: int
    creator_id: StrObjectId
    total_amount: float
    currency: str
    paid_amount: float
    installments: int
    details: dict
    crm_id: Optional[str] = Field(default=None)

    def example_payload(self):
        return {
            "product_id": "6756ef4959e496069bee54d8",
            "quantity": 1,
            "creator_id": "6756ef4959e496069bee54d8",
            "total_amount": 100,
            "currency": "USD",
            "paid_amount": 100,
            "installments": 1,
            "details": {}
        }