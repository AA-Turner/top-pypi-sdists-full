from enum import Enum


class SCIMUSERMATCHWALDURATTRIBUTEEnum(str, Enum):
    CIVIL_NUMBER = "civil_number"
    EMAIL = "email"
    USERNAME = "username"

    def __str__(self) -> str:
        return str(self.value)
