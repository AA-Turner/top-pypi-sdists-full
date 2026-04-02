from enum import Enum


class UserOfferingConsentOEnum(str, Enum):
    AGREEMENT_DATE = "agreement_date"
    CREATED = "created"
    MODIFIED = "modified"
    REVOCATION_DATE = "revocation_date"
    VALUE_0 = "-agreement_date"
    VALUE_1 = "-created"
    VALUE_2 = "-modified"
    VALUE_3 = "-revocation_date"

    def __str__(self) -> str:
        return str(self.value)
