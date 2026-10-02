from enum import StrEnum

class ManagedAgentsInjectionLocation(StrEnum):
    BODY = "body"
    HEADERS = "headers"

    def __str__(self) -> str:
        return str(self.value)
