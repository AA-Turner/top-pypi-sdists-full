from enum import StrEnum

class QaTriggerResponseDtoEvent(StrEnum):
    PROBLEM_LOCKED = "problem_locked"
    SOLVER_COMPLETED = "solver_completed"

    def __str__(self) -> str:
        return str(self.value)
