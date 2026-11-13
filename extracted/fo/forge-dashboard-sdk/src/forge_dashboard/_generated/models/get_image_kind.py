from enum import StrEnum

class GetImageKind(StrEnum):
    AVATAR = "avatar"

    def __str__(self) -> str:
        return str(self.value)
