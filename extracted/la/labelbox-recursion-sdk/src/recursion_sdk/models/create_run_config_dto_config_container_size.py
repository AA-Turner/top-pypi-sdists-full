from enum import StrEnum

class CreateRunConfigDtoConfigContainerSize(StrEnum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"
    XLARGE = "xlarge"
    XLARGE_HIGHMEM = "xlarge-highmem"
    XXLARGE = "xxlarge"

    def __str__(self) -> str:
        return str(self.value)
