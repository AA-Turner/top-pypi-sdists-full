from pydantic import BaseModel
from letschatty.models.utils import StrObjectId

class LinkItem(BaseModel):
    flow_id: StrObjectId
    chat_id: StrObjectId
    company_id: StrObjectId
