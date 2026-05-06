from enum import Enum


class ComponentUsageMonthlyFieldEnum(str, Enum):
    BILLING_PERIOD = "billing_period"
    BILLING_TYPE = "billing_type"
    CATEGORY_TITLE = "category_title"
    CATEGORY_UUID = "category_uuid"
    COMPONENT_NAME = "component_name"
    COMPONENT_TYPE = "component_type"
    LIMIT_AMOUNT = "limit_amount"
    LIMIT_PERIOD = "limit_period"
    MEASURED_UNIT = "measured_unit"
    OFFERING_NAME = "offering_name"
    OFFERING_TYPE = "offering_type"
    OFFERING_UUID = "offering_uuid"
    SERVICE_PROVIDER_NAME = "service_provider_name"
    SERVICE_PROVIDER_UUID = "service_provider_uuid"
    TOTAL_ALLOCATED = "total_allocated"
    TOTAL_CONSUMED = "total_consumed"
    USAGE_PERCENT = "usage_percent"

    def __str__(self) -> str:
        return str(self.value)
