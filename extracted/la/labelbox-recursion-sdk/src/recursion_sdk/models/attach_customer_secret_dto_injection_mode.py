from enum import StrEnum

class AttachCustomerSecretDtoInjectionMode(StrEnum):
    DIRECT = "direct"
    PROXY = "proxy"

    def __str__(self) -> str:
        return str(self.value)
