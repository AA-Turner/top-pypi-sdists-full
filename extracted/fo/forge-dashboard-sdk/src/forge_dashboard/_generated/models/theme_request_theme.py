from enum import StrEnum

class ThemeRequestTheme(StrEnum):
    DARK = "dark"
    LIGHT = "light"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
