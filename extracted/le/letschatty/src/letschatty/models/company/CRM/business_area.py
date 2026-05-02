from ...base_models import CompanyAssetModel
from typing import List
from pydantic import Field

class BusinessArea(CompanyAssetModel):
    name: str
    description: str
    assignment_priority: int = Field(ge=0, le=10, description="The priority of the business area, it's used to assign chats")