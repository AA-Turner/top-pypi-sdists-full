from enum import Enum


class ReviewStrategyEnum(str, Enum):
    AFTER_PROPOSAL = "after_proposal"
    AFTER_ROUND = "after_round"

    def __str__(self) -> str:
        return str(self.value)
