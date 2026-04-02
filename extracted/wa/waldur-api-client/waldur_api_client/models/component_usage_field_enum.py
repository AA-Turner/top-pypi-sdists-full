from enum import Enum


class ComponentUsageFieldEnum(str, Enum):
    BILLING_PERIOD = "billing_period"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    DATE = "date"
    DESCRIPTION = "description"
    MEASURED_UNIT = "measured_unit"
    MODIFIED_BY = "modified_by"
    NAME = "name"
    OFFERING_NAME = "offering_name"
    OFFERING_UUID = "offering_uuid"
    PROJECT_NAME = "project_name"
    PROJECT_UUID = "project_uuid"
    RECURRING = "recurring"
    RESOURCE_NAME = "resource_name"
    RESOURCE_UUID = "resource_uuid"
    TYPE = "type"
    USAGE = "usage"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
