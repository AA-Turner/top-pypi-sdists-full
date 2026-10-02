from enum import StrEnum

class ManagedAgentsWebhookMatchConditionRequestOperator(StrEnum):
    EQUALS = "equals"
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"
    ONE_OF = "one_of"

    def __str__(self) -> str:
        return str(self.value)
