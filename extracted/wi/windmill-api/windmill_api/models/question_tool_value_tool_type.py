from enum import Enum


class QuestionToolValueToolType(str, Enum):
    QUESTION = "question"

    def __str__(self) -> str:
        return str(self.value)
