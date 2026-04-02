from enum import Enum


class DEFAULTIDPEnum(str, Enum):
    EDUTEAMS = "eduteams"
    KEYCLOAK = "keycloak"
    TARA = "tara"

    def __str__(self) -> str:
        return str(self.value)
