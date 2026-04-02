from enum import Enum


class EventGroupsEnum(str, Enum):
    ACCESS_SUBNETS = "access_subnets"
    AUTH = "auth"
    CALL = "call"
    CHAT = "chat"
    CREDITS = "credits"
    CUSTOMERS = "customers"
    INVOICES = "invoices"
    OFFERING_ACCOUNTING = "offering_accounting"
    ONBOARDING = "onboarding"
    PERMISSIONS = "permissions"
    PROJECTS = "projects"
    PROPOSAL = "proposal"
    PROVIDERS = "providers"
    RESOURCES = "resources"
    REVIEW = "review"
    SSH = "ssh"
    SUPPORT = "support"
    TERMS_OF_SERVICE = "terms_of_service"
    USERS = "users"

    def __str__(self) -> str:
        return str(self.value)
