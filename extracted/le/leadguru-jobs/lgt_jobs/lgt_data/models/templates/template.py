from typing import Optional

from bson import ObjectId

from lgt_jobs.lgt_data.models.base import BaseModel


class UserTemplateModel(BaseModel):
    text: str
    subject: Optional[str]
    user_id: Optional[ObjectId]
    