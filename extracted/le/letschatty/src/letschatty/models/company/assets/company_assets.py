from enum import StrEnum
from typing import List

class CompanyAssetType(StrEnum):
    USERS = "users"
    BUSINESS_AREAS = "business_areas"
    FUNNELS = "funnels"
    PRODUCTS = "products"
    SALES = "sales"
    TAGS = "tags"
    SOURCES = "sources"
    TEMPLATES = "templates"
    TEMPLATE_CAMPAIGNS = "template_campaigns"
    FAST_ANSWERS = "fast_answers"
    ANALYTICS = "analytics"
    CHATS = "chats"
    TOPICS = "topics"
    COMPANY = "company"
    MEDIA = "media"
    WORKFLOWS = "workflows"
    CHATTY_AI_AGENTS = "chatty_ai_agents"
    FILTER_CRITERIA = "filter_criteria"

    @classmethod
    def get_all(cls) -> List[str]:
        return [asset_type.value for asset_type in cls]
