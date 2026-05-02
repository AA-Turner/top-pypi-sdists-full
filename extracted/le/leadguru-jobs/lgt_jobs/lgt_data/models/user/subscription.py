from datetime import datetime

from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.user.feature import Feature


class Subscription(BaseModel):
    features: list[Feature]
    duration_days: int
    name: str
    price: int
    limits: int
    trial: bool
    updated_at: datetime = None

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None
        model: Subscription | None = super().from_dic(dic)
        model.features = [Feature.from_dic(feature) for feature in dic.get('features', [])]
        return model
