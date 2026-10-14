from enum import Enum


class CustomerEstimatedCostPolicyFieldEnum(str, Enum):
    ACTIONS = "actions"
    AFFECTED_RESOURCES_COUNT = "affected_resources_count"
    BILLING_PRICE_ESTIMATE = "billing_price_estimate"
    CREATED = "created"
    CREATED_BY_FULL_NAME = "created_by_full_name"
    CREATED_BY_USERNAME = "created_by_username"
    CURRENT_COST = "current_cost"
    CUSTOMER_CREDIT = "customer_credit"
    ETA_DATE = "eta_date"
    ETA_DAYS = "eta_days"
    FIRED_DATETIME = "fired_datetime"
    HAS_FIRED = "has_fired"
    LIMIT_COST = "limit_cost"
    OPTIONS = "options"
    PERIOD = "period"
    PERIOD_NAME = "period_name"
    SCOPE = "scope"
    SCOPE_NAME = "scope_name"
    SCOPE_UUID = "scope_uuid"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
