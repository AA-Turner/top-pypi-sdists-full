from enum import Enum


class HttpStoreSettingsAuthType(str, Enum):
    BEARERTOKENFILE = "BearerTokenFile"
    CLIENTCERTIFICATE = "ClientCertificate"
    NONE = "None"
    STATICHEADER = "StaticHeader"

    def __str__(self) -> str:
        return str(self.value)
