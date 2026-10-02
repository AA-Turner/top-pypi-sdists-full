from enum import StrEnum

class ManagedAgentsWebhookSignedPartKind(StrEnum):
    BODY = "body"
    HEADER = "header"
    LITERAL = "literal"

    def __str__(self) -> str:
        return str(self.value)
