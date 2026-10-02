from enum import StrEnum

class ManagedAgentsMemoryVersionAuthorKind(StrEnum):
    ADMIN = "admin"
    API = "api"
    REFLECTION = "reflection"
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
