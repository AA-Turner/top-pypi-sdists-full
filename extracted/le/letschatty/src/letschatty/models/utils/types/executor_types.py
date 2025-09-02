from enum import StrEnum

class ExecutorType(StrEnum):
    AGENT = "agent"
    MEGA_ADMIN = "mega_admin"
    WORKFLOW = "workflow"
    COPILOT = "copilot"
    SOURCE_AUTOMATION = "source_automation"
    TEMPLATE_AUTOMATION = "template_automation"
    MESSAGE_CAMPAIGN = "message_campaign"
    INTEGRATION = "integration"
    SUGGESTION = "suggestion"
    SYSTEM = "system"
    OTHER = "other"
    META = "meta"