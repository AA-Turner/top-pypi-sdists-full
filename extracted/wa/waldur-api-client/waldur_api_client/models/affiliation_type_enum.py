from enum import Enum


class AffiliationTypeEnum(str, Enum):
    CONSULTING = "consulting"
    EDUCATION = "education"
    EMPLOYMENT = "employment"
    HONORARY = "honorary"
    VISITING = "visiting"

    def __str__(self) -> str:
        return str(self.value)
