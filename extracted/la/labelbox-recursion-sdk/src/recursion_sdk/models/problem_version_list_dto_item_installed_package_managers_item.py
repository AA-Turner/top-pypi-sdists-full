from enum import StrEnum

class ProblemVersionListDtoItemInstalledPackageManagersItem(StrEnum):
    APT = "apt"
    CARGO = "cargo"
    NPM = "npm"
    PIP = "pip"
    UV = "uv"

    def __str__(self) -> str:
        return str(self.value)
