from enum import Enum


class COIDisclosureFormOEnum(str, Enum):
    CERTIFICATION_DATE = "certification_date"
    CREATED = "created"
    VALID_UNTIL = "valid_until"
    VALUE_0 = "-certification_date"
    VALUE_1 = "-created"
    VALUE_2 = "-valid_until"

    def __str__(self) -> str:
        return str(self.value)
