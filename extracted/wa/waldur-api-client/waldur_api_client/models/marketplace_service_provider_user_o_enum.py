from enum import Enum


class MarketplaceServiceProviderUserOEnum(str, Enum):
    DESCRIPTION = "description"
    EMAIL = "email"
    FULL_NAME = "full_name"
    IS_ACTIVE = "is_active"
    IS_STAFF = "is_staff"
    IS_SUPPORT = "is_support"
    JOB_TITLE = "job_title"
    NATIVE_NAME = "native_name"
    ORGANIZATION = "organization"
    PHONE_NUMBER = "phone_number"
    REGISTRATION_METHOD = "registration_method"
    USERNAME = "username"
    VALUE_0 = "-description"
    VALUE_1 = "-email"
    VALUE_10 = "-registration_method"
    VALUE_11 = "-username"
    VALUE_2 = "-full_name"
    VALUE_3 = "-is_active"
    VALUE_4 = "-is_staff"
    VALUE_5 = "-is_support"
    VALUE_6 = "-job_title"
    VALUE_7 = "-native_name"
    VALUE_8 = "-organization"
    VALUE_9 = "-phone_number"

    def __str__(self) -> str:
        return str(self.value)
