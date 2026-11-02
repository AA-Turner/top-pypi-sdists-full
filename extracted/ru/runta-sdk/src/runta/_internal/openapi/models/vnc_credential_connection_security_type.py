from enum import Enum


class VncCredentialConnectionSecurityType(str, Enum):
    X509PLAIN = "X509Plain"

    def __str__(self) -> str:
        return str(self.value)
