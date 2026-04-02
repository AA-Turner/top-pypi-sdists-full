from enum import Enum


class MarketplaceServiceProviderUserFieldEnum(str, Enum):
    ACTIVE_ISDS = "active_isds"
    AFFILIATIONS = "affiliations"
    BIRTH_DATE = "birth_date"
    CIVIL_NUMBER = "civil_number"
    COUNTRY_OF_RESIDENCE = "country_of_residence"
    EDUPERSON_ASSURANCE = "eduperson_assurance"
    EMAIL = "email"
    FIRST_NAME = "first_name"
    FULL_NAME = "full_name"
    GENDER = "gender"
    IDENTITY_SOURCE = "identity_source"
    IS_ACTIVE = "is_active"
    JOB_TITLE = "job_title"
    LAST_NAME = "last_name"
    NATIONALITIES = "nationalities"
    NATIONALITY = "nationality"
    ORGANIZATION = "organization"
    ORGANIZATION_COUNTRY = "organization_country"
    ORGANIZATION_REGISTRY_CODE = "organization_registry_code"
    ORGANIZATION_TYPE = "organization_type"
    PERSONAL_TITLE = "personal_title"
    PHONE_NUMBER = "phone_number"
    PLACE_OF_BIRTH = "place_of_birth"
    PROJECTS_COUNT = "projects_count"
    REGISTRATION_METHOD = "registration_method"
    USERNAME = "username"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
