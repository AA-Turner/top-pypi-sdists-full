from enum import StrEnum

class RunConfigWithVersionListDtoItemsPropertiesScopeProblemLevel(StrEnum):
    PROBLEM = "problem"

    def __str__(self) -> str:
        return str(self.value)
