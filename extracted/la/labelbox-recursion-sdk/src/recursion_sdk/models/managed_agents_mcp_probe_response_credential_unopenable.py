from enum import StrEnum

class ManagedAgentsMCPProbeResponseCredentialUnopenable(StrEnum):
    EXTERNAL_REFERENCE = "external_reference"
    MATERIAL_MISSING = "material_missing"

    def __str__(self) -> str:
        return str(self.value)
