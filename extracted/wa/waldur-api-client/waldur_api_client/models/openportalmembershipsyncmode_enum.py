from enum import Enum


class OPENPORTALMEMBERSHIPSYNCMODEEnum(str, Enum):
    DIRECT = "direct"
    INVITATION = "invitation"

    def __str__(self) -> str:
        return str(self.value)
