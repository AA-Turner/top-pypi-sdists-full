import enum

from pydantic import BaseModel


class PremiumPlanTypes(str, enum.Enum):
    month = "1month"
    three_months = "3months"
    six_months = "6months"
    year = "12months"


class RequestPremiumModel(BaseModel):
    shop_id: str
    premium_type: PremiumPlanTypes
