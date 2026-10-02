from enum import Enum


class UserAttributeEnum(str, Enum):
    ACTIVE_ISDS = "active_isds"
    ADDRESS = "address"
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
    JOB_TITLE = "job_title"
    LAST_NAME = "last_name"
    NATIONALITIES = "nationalities"
    NATIONALITY = "nationality"
    ORGANIZATION = "organization"
    ORGANIZATION_ADDRESS = "organization_address"
    ORGANIZATION_COUNTRY = "organization_country"
    ORGANIZATION_REGISTRY_CODE = "organization_registry_code"
    ORGANIZATION_TYPE = "organization_type"
    ORGANIZATION_VAT_CODE = "organization_vat_code"
    PERSONAL_TITLE = "personal_title"
    PHONE_NUMBER = "phone_number"
    PLACE_OF_BIRTH = "place_of_birth"
    PRIMARY_GID = "primary_gid"
    REGISTRATION_METHOD = "registration_method"
    UID_NUMBER = "uid_number"
    USERNAME = "username"

    def __str__(self) -> str:
        return str(self.value)
