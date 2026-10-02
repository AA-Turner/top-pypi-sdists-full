from enum import StrEnum

class CreateCustomerSecretDtoInjectionMode(StrEnum):
    DIRECT = "direct"
    PROXY = "proxy"

    def __str__(self) -> str:
        return str(self.value)
