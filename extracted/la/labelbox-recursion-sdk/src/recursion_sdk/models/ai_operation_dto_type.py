from enum import StrEnum

class AiOperationDtoType(StrEnum):
    GENERATE_RUBRICS = "generate_rubrics"
    GENERATE_SETTINGS = "generate_settings"
    IMPROVE_PROMPT = "improve_prompt"

    def __str__(self) -> str:
        return str(self.value)
