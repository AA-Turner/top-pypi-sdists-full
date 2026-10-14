from enum import Enum


class ChangelogEntryListCategoryEnum(str, Enum):
    AI_ASSISTANT = "ai_assistant"
    AUTH = "auth"
    IDENTITY = "identity"
    INFRASTRUCTURE = "infrastructure"
    INVOICES = "invoices"
    MARKETPLACE = "marketplace"
    NOTIFICATIONS = "notifications"
    OPENSTACK = "openstack"
    POLICY = "policy"
    PROPOSAL = "proposal"
    REPORTING = "reporting"
    SLURM = "slurm"
    SUPPORT = "support"
    UI = "ui"

    def __str__(self) -> str:
        return str(self.value)
