from enum import Enum


class PublicCallFieldEnum(str, Enum):
    BACKEND_ID = "backend_id"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    DESCRIPTION = "description"
    DOCUMENTS = "documents"
    END_DATE = "end_date"
    EXTERNAL_URL = "external_url"
    FIXED_DURATION_IN_DAYS = "fixed_duration_in_days"
    HAS_ELIGIBILITY_RESTRICTIONS = "has_eligibility_restrictions"
    MANAGER = "manager"
    MANAGER_UUID = "manager_uuid"
    NAME = "name"
    OFFERINGS = "offerings"
    RESOURCE_TEMPLATES = "resource_templates"
    REVIEWER_IDENTITY_VISIBLE_TO_SUBMITTERS = "reviewer_identity_visible_to_submitters"
    REVIEWS_VISIBLE_TO_SUBMITTERS = "reviews_visible_to_submitters"
    ROUNDS = "rounds"
    SLUG = "slug"
    START_DATE = "start_date"
    STATE = "state"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
