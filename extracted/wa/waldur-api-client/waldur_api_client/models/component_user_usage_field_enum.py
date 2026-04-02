from enum import Enum


class ComponentUserUsageFieldEnum(str, Enum):
    BACKEND_ID = "backend_id"
    BILLING_PERIOD = "billing_period"
    COMPONENT_TYPE = "component_type"
    COMPONENT_USAGE = "component_usage"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    DATE = "date"
    DESCRIPTION = "description"
    MEASURED_UNIT = "measured_unit"
    MODIFIED = "modified"
    OFFERING_NAME = "offering_name"
    OFFERING_UUID = "offering_uuid"
    PROJECT_NAME = "project_name"
    PROJECT_UUID = "project_uuid"
    RESOURCE_NAME = "resource_name"
    RESOURCE_UUID = "resource_uuid"
    USAGE = "usage"
    USER = "user"
    USERNAME = "username"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
