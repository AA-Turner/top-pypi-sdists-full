from enum import StrEnum

class ResolvedMenuDtoSlotRole(StrEnum):
    GRADER = "grader"
    QA = "qa"
    SOLVER = "solver"
    SYNTHESIZER = "synthesizer"

    def __str__(self) -> str:
        return str(self.value)
