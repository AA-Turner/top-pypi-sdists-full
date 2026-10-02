from enum import StrEnum

class ManagedAgentsVaultCredentialNetworkMode(StrEnum):
    LIMITED = "limited"
    UNRESTRICTED = "unrestricted"

    def __str__(self) -> str:
        return str(self.value)
