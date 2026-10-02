from enum import StrEnum

class ManagedAgentsApiErrorUnsupportedMediaTypeCode(StrEnum):
    UNSUPPORTED_MEDIA_TYPE = "unsupported_media_type"

    def __str__(self) -> str:
        return str(self.value)
