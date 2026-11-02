from enum import Enum


class VncGatewayConnectionSecurityType(str, Enum):
    X509PLAIN = "X509Plain"

    def __str__(self) -> str:
        return str(self.value)
