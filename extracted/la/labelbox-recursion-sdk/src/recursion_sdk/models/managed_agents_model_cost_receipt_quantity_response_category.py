from enum import StrEnum

class ManagedAgentsModelCostReceiptQuantityResponseCategory(StrEnum):
    COMPUTE = "compute"
    INPUT = "input"
    OUTPUT = "output"
    PROVIDER_TOOL = "provider_tool"
    REASONING = "reasoning"
    TOOL_PROMPT = "tool_prompt"

    def __str__(self) -> str:
        return str(self.value)
