from enum import StrEnum

class InheritedRunConfigDefaultDtoScopeLevel(StrEnum):
    ENV = "env"
    ORG = "org"
    PROBLEM = "problem"
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
