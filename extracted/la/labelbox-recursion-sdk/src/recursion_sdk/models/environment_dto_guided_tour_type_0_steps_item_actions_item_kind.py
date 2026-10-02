from enum import StrEnum

class EnvironmentDtoGuidedTourType0StepsItemActionsItemKind(StrEnum):
    CLICK = "click"
    FOCUS = "focus"
    HIGHLIGHT = "highlight"

    def __str__(self) -> str:
        return str(self.value)
