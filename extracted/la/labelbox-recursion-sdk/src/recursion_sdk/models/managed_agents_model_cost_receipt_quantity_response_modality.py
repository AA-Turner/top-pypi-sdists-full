from enum import StrEnum

class ManagedAgentsModelCostReceiptQuantityResponseModality(StrEnum):
    AUDIO = "audio"
    COMPUTE = "compute"
    IMAGE = "image"
    TEXT = "text"
    TOOL = "tool"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
