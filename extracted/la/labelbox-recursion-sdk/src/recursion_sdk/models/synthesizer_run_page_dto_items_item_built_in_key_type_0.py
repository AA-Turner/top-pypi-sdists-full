from enum import StrEnum

class SynthesizerRunPageDtoItemsItemBuiltInKeyType0(StrEnum):
    GENERATE_RUBRICS = "generate-rubrics"
    GENERATE_TOOLS = "generate-tools"
    IMPROVE_PROMPT = "improve-prompt"

    def __str__(self) -> str:
        return str(self.value)
