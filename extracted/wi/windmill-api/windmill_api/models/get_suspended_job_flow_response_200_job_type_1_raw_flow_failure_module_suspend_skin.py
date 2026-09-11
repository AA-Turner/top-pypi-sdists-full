from enum import Enum


class GetSuspendedJobFlowResponse200JobType1RawFlowFailureModuleSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
