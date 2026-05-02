from enum import StrEnum
from typing import List

class CompanyAssetType(StrEnum):
    USERS = "users"
    BUSINESS_AREAS = "business_areas"
    FUNNELS = "funnels"
    FUNNEL_STAGES = "funnel_stages"
    FUNNEL_MEMBERS = "funnel_members"
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
    AI_AGENT_CONTEXT = "ai_agent_context"
    AI_AGENT_CHAT_EXAMPLE = "ai_agent_chat_example"
    AI_AGENT_INSTRUCTION = "ai_agent_instruction"
    FILTER_CRITERIA = "filter_criteria"
    FORM_FIELDS = "form_fields"
    NOTIFICATIONS = "notifications"

    @classmethod
    def get_all(cls) -> List[str]:
        return [asset_type.value for asset_type in cls]
