from enum import Enum


class GetHubFlowByIdResponse200FlowValueModulesItemSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
