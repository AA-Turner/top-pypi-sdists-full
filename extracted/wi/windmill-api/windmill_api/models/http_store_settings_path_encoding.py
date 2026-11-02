from enum import Enum


class HttpStoreSettingsPathEncoding(str, Enum):
    DOUBLE_DASH = "double_dash"
    RAW = "raw"
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)
