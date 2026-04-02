from enum import Enum


class UserAttributeEnum(str, Enum):
    AFFILIATIONS = "affiliations"
    BIRTH_DATE = "birth_date"
    CIVIL_NUMBER = "civil_number"
    COUNTRY_OF_RESIDENCE = "country_of_residence"
    EDUPERSON_ASSURANCE = "eduperson_assurance"
    EMAIL = "email"
    FULL_NAME = "full_name"
    GENDER = "gender"
    IDENTITY_SOURCE = "identity_source"
    JOB_TITLE = "job_title"
    NATIONALITIES = "nationalities"
    NATIONALITY = "nationality"
    ORGANIZATION = "organization"
    ORGANIZATION_COUNTRY = "organization_country"
    ORGANIZATION_REGISTRY_CODE = "organization_registry_code"
    ORGANIZATION_TYPE = "organization_type"
    PERSONAL_TITLE = "personal_title"
    PHONE_NUMBER = "phone_number"
    PLACE_OF_BIRTH = "place_of_birth"
    USERNAME = "username"

    def __str__(self) -> str:
        return str(self.value)
