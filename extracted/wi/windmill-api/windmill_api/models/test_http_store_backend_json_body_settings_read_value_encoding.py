from enum import Enum


class TestHttpStoreBackendJsonBodySettingsReadValueEncoding(str, Enum):
    BASE64 = "base64"
    PLAIN = "plain"

    def __str__(self) -> str:
        return str(self.value)
