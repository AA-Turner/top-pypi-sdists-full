from enum import StrEnum

class SettingsResponseTheme(StrEnum):
    DARK = "dark"
    LIGHT = "light"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
