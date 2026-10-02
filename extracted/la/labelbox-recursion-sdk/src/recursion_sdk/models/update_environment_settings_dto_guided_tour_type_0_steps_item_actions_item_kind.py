from enum import StrEnum

class UpdateEnvironmentSettingsDtoGuidedTourType0StepsItemActionsItemKind(StrEnum):
    CLICK = "click"
    FOCUS = "focus"
    HIGHLIGHT = "highlight"

    def __str__(self) -> str:
        return str(self.value)
