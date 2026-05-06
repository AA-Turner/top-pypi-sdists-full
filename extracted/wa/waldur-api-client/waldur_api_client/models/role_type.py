from enum import Enum


class RoleType(str, Enum):
    CALL = "call"
    CALL_ORGANIZER = "call_organizer"
    CUSTOMER = "customer"
    OFFERING = "offering"
    PROJECT = "project"
    PROPOSAL = "proposal"
    RESOURCE = "resource"
    RESOURCE_PROJECT = "resource_project"
    SERVICE_PROVIDER = "service_provider"

    def __str__(self) -> str:
        return str(self.value)
