from enum import Enum


class PublicCallFieldEnum(str, Enum):
    BACKEND_ID = "backend_id"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_UUID = "customer_uuid"
    DESCRIPTION = "description"
    DOCUMENTS = "documents"
    END_DATE = "end_date"
    EVALUATION_START = "evaluation_start"
    EXTERNAL_URL = "external_url"
    FIXED_DURATION_IN_DAYS = "fixed_duration_in_days"
    HAS_ELIGIBILITY_RESTRICTIONS = "has_eligibility_restrictions"
    MANAGER = "manager"
    MANAGER_UUID = "manager_uuid"
    MAX_PREPAID_DURATION_MONTHS = "max_prepaid_duration_months"
    NAME = "name"
    OFFERINGS = "offerings"
    PROPOSAL_FIELD_CONFIG = "proposal_field_config"
    PUBLISH_RESULTS = "publish_results"
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
