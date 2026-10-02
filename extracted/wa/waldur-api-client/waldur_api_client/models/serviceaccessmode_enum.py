from enum import Enum


class SERVICEACCESSMODEEnum(str, Enum):
    BOTH = "both"
    CALLS = "calls"
    MARKETPLACE = "marketplace"

    def __str__(self) -> str:
        return str(self.value)
