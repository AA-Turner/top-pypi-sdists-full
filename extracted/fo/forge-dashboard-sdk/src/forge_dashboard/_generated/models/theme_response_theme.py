from enum import StrEnum

class ThemeResponseTheme(StrEnum):
    DARK = "dark"
    LIGHT = "light"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
